#!/usr/bin/env python3
"""Minimal Mochi Cards API client for the research-to-flashcards skill.

Talks to the Mochi REST API (https://app.mochi.cards/api/) using plain JSON,
and encapsulates the API's quirks so the caller never has to think about them:
  - kebab-case keys with `?` suffixes (deck-id, manual-tags, archived?, ...)
  - HTTP Basic auth: API key as the username, empty password
  - one-concurrent-request limit -> every request is sequential, with 429/5xx backoff
  - source-hash dedup so re-runs don't create duplicate cards

Stdlib only (no pip installs), so it runs anywhere Python 3 does.

Auth:   set MOCHI_API_KEY in the environment (Mochi Pro required).
Config: set MOCHI_API_BASE to override the base URL (testing / self-host).

Subcommands:
  decks
      List decks as JSON: [{"id", "name", "parent-id"}]
  ensure-deck NAME [--parent-id ID]
      Find a deck by name (create it if missing); prints the deck id to stdout.
  add-cards --deck-id ID --file cards.json [--no-dedup] [--dry-run]
      Create cards from a JSON array; dedups by source hash unless --no-dedup.

cards.json item schema (one object per card):
  {"front": "...", "back": "...", "tags": ["optional", "..."]}
    -> content becomes  front + "\n---\n" + back  (Mochi splits sides on `---`)
  {"content": "...raw markdown...", "tags": [...]}
    -> use `content` verbatim (for single-sided notes or custom layouts)

Dedup: each card is tagged `src:<hash>` where hash = sha256(content)[:12].
Before creating, the deck's existing `src:` tags are read and matching cards
skipped. This is stateless (no local manifest) so re-runs are safe from any machine.
"""
import argparse
import base64
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("MOCHI_API_BASE", "https://app.mochi.cards/api").rstrip("/")
SRC_TAG_PREFIX = "src:"
MAX_RETRIES = 5


class MochiError(Exception):
    """Raised on a non-retryable API error or after retries are exhausted."""


def _auth_header():
    key = os.environ.get("MOCHI_API_KEY")
    if not key:
        raise MochiError(
            "MOCHI_API_KEY not set. Create a key in Mochi > Account Settings "
            "(requires Mochi Pro), then export MOCHI_API_KEY."
        )
    # Basic auth = base64("<key>:"); the empty password is intentional.
    return "Basic " + base64.b64encode(f"{key}:".encode()).decode()


def _request(method, path, params=None, body=None):
    """One sequential HTTP request. Retries 429 and 5xx with exponential backoff.

    Returns parsed JSON (or None for empty bodies). Raises MochiError otherwise.
    """
    url = f"{BASE}{path}"
    if params:
        clean = {k: v for k, v in params.items() if v is not None}
        if clean:
            url += "?" + urllib.parse.urlencode(clean)
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": _auth_header(), "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"

    backoff = 1.0
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                raw = resp.read().decode()
                return json.loads(raw) if raw.strip() else None
        except urllib.error.HTTPError as e:
            text = e.read().decode(errors="replace")
            retryable = e.code == 429 or 500 <= e.code < 600
            if retryable and attempt < MAX_RETRIES - 1:
                time.sleep(backoff)
                backoff *= 2
                continue
            # 403 = not authorized / not Pro; 422 = validation (per-field error map).
            raise MochiError(f"HTTP {e.code} on {method} {path}: {text}")
        except urllib.error.URLError as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(backoff)
                backoff *= 2
                continue
            raise MochiError(f"network error on {method} {path}: {e.reason}")
    return None


def _paginate(path, params=None):
    """Yield every doc across all pages of a list endpoint (docs + bookmark cursor)."""
    params = dict(params or {})
    while True:
        page = _request("GET", path, params=params) or {}
        docs = page.get("docs", [])
        for d in docs:
            yield d
        bookmark = page.get("bookmark")
        # A returned bookmark does NOT guarantee more pages; stop on empty page too.
        if not bookmark or not docs:
            break
        params["bookmark"] = bookmark


def list_decks():
    return [
        {"id": d.get("id"), "name": d.get("name"), "parent-id": d.get("parent-id")}
        for d in _paginate("/decks/")
    ]


def ensure_deck(name, parent_id=None):
    for d in list_decks():
        if d["name"] == name and (parent_id is None or d.get("parent-id") == parent_id):
            return d["id"]
    body = {"name": name}
    if parent_id:
        body["parent-id"] = parent_id
    created = _request("POST", "/decks/", body=body) or {}
    deck_id = created.get("id")
    if not deck_id:
        raise MochiError(f"deck creation returned no id: {created!r}")
    return deck_id


def _compose(item):
    """Build card markdown from {front, back} or pass through {content}."""
    if item.get("content"):
        return item["content"]
    front = (item.get("front") or "").strip()
    back = (item.get("back") or "").strip()
    if not front:
        raise MochiError(f"card has neither content nor front: {item!r}")
    return f"{front}\n---\n{back}" if back else front


def _card_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()[:12]


def _existing_hashes(deck_id):
    found = set()
    for c in _paginate("/cards/", params={"deck-id": deck_id, "limit": 100}):
        for t in (c.get("tags") or []):
            t = t.lstrip("#")
            if t.startswith(SRC_TAG_PREFIX):
                found.add(t[len(SRC_TAG_PREFIX):])
    return found


def add_cards(deck_id, items, dedup=True, dry_run=False):
    existing = _existing_hashes(deck_id) if dedup else set()
    created, skipped, errors = [], [], []
    for item in items:
        content = _compose(item)
        h = _card_hash(content)
        if dedup and h in existing:
            skipped.append(h)
            continue
        tags = list(item.get("tags") or [])
        tags.append(f"{SRC_TAG_PREFIX}{h}")
        if dry_run:
            created.append({"hash": h, "manual-tags": tags, "content": content, "dry_run": True})
            existing.add(h)
            continue
        try:
            card = _request("POST", "/cards/", body={
                "content": content, "deck-id": deck_id, "manual-tags": tags,
            }) or {}
            created.append({"id": card.get("id"), "hash": h})
            existing.add(h)
        except MochiError as e:
            errors.append({"hash": h, "error": str(e)})
    return {
        "n_created": len(created), "n_skipped": len(skipped), "n_errors": len(errors),
        "created": created, "skipped": skipped, "errors": errors,
    }


def main():
    ap = argparse.ArgumentParser(description="Minimal Mochi Cards API client.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("decks", help="List decks as JSON.")
    p_ed = sub.add_parser("ensure-deck", help="Find or create a deck; print its id.")
    p_ed.add_argument("name")
    p_ed.add_argument("--parent-id", default=None)
    p_ac = sub.add_parser("add-cards", help="Create cards from a JSON array.")
    p_ac.add_argument("--deck-id", required=True)
    p_ac.add_argument("--file", required=True, help="JSON array file, or - for stdin.")
    p_ac.add_argument("--no-dedup", action="store_true")
    p_ac.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    try:
        if args.cmd == "decks":
            print(json.dumps(list_decks(), indent=2, ensure_ascii=False))
        elif args.cmd == "ensure-deck":
            print(ensure_deck(args.name, args.parent_id))
        elif args.cmd == "add-cards":
            text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
            items = json.loads(text)
            if not isinstance(items, list):
                raise MochiError("cards file must be a JSON array of card objects.")
            result = add_cards(args.deck_id, items, dedup=not args.no_dedup, dry_run=args.dry_run)
            print(json.dumps(result, indent=2, ensure_ascii=False))
    except MochiError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
