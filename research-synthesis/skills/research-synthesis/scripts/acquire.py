#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""Acquisition: candidate pool -> download -> convert -> embed, verified from the catalog.

Per DOI (inside one concurrency slot, with its own MCP session):
  1. catalog_read(stem) already converted+embedded and distill_exists  -> acquired (already in corpus)
  2. paper_download(doi)         "No open-access PDF found" -> paywalled ; other errors -> transient
  3. scribe_convert(stem)        raw JSON-RPC, 1800 s timeout (the harness's 30 s timeout CANCELS conversions)
       - tool error "0 non-whitespace chars"      -> unconvertible (anti-bot gate page / empty)
       - client timeout / transport error         -> DO NOT resend; poll catalog_read (server keeps converting)
  4. poll catalog_read for conversion+embedding (event-watch embeds); if converted but not embedded after
     --embed-wait seconds, call distill_index(stem)
  5. markdown sanity: gate-page markers / near-empty markdown -> unconvertible
  6. distill_exists(stem) must be true -> acquired

Status values in acquisition.tsv:
  acquired | paywalled | unconvertible        terminal (skipped on resume unless --retry)
  transient | convert_pending_verify | converted_not_embedded | downloaded | pending   retried on resume

Never trusts the filesystem (stale NFS): all verification is via catalog_read / distill_exists.
Killing this script does NOT cancel server-side conversions; do not restart-storm. Resume instead
(`convert_pending_verify` rows are only re-converted if scribe_health shows nothing in flight).

Input: --pool candidate-pool.tsv --tiers core,adjacent   (rows whose `tier` column matches)
   or: --dois file.txt (one DOI per line)
Output (in --out-dir): acquisition.tsv (state) + views acquired.tsv paywalled.tsv unconvertible.tsv
   pending.tsv abstract-only.tsv (paywalled rows of --abstract-only-tiers, with abstract text)

Run: uv run --script acquire.py --pool corpus/candidate-pool.tsv --tiers core,adjacent --out-dir corpus/
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hs_mcp  # noqa: E402

STATE_COLS = ["doi", "stem", "tier", "status", "evidence_level", "detail", "attempts", "updated_at", "title", "year"]
TERMINAL = {"acquired", "paywalled", "unconvertible"}
GATE_MARKERS = re.compile(
    r"Article Locator Bypass|Checking your browser|Cookies? (are )?disabled|Just a moment|Enable JavaScript|"
    r"Access Denied|are you a robot|captcha|cf-browser-verification|Attention Required|Request blocked", re.I)
_lock = threading.Lock()


def read_tsv(p: Path) -> list[dict]:
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(p: Path, cols: list[str], rows: list[dict]) -> None:
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: re.sub(r"[\t\r\n]+", " ", str(r.get(c, "") or "")) for c in cols})
    tmp.replace(p)


def stem_state(s: hs_mcp.Session, stem: str) -> dict | None:
    """catalog_read -> {'catalog': dict, 'downloaded','converted','embedded'} or None if absent."""
    try:
        c = s.call("catalog_read", {"stem": stem})
    except hs_mcp.ToolError:
        return None
    if not isinstance(c, dict):
        return None
    return {"catalog": c, "downloaded": bool(c.get("pdf_path")), "converted": bool(c.get("conversion")),
            "embedded": bool(c.get("embedding"))}


def poll(s, stem, want_embedded: bool, wait: float, every: float = 15.0) -> dict | None:
    deadline = time.time() + wait
    while True:
        st = stem_state(s, stem)
        if st and st["converted"] and (st["embedded"] or not want_embedded):
            return st
        if time.time() >= deadline:
            return st
        time.sleep(every)


def indexed(s, stem) -> bool:
    r = s.call("distill_exists", {"doc_id": stem})
    return bool(isinstance(r, dict) and r.get("indexed"))


def gate_check(s, stem) -> str:
    """Return a reason string if the converted markdown looks like a gate page / is near-empty."""
    try:
        md = s.call_text("markdown_read", {"stem": stem, "page": 1}, timeout=120)
    except Exception:  # noqa: BLE001 - sanity check only; never fail acquisition on it
        return ""
    head = md[:20000]
    body = re.sub(r"\s+", "", md)
    if GATE_MARKERS.search(head) and len(body) < 6000:
        return "gate page markers: " + GATE_MARKERS.search(head).group(0)
    if len(body) < 400:
        return f"near-empty markdown ({len(body)} chars on page 1)"
    return ""


def process(url: str, row: dict, a) -> dict:
    """Advance one DOI as far as possible; returns updated state fields."""
    doi, stem = row["doi"], row.get("stem") or hs_mcp.doi_to_stem_candidates(row["doi"])[0]
    out = {"attempts": str(int(row.get("attempts") or 0) + 1), "stem": stem}
    try:
        with hs_mcp.session(url) as s:  # session opened INSIDE the worker slot
            st = stem_state(s, stem)
            if st and st["converted"] and st["embedded"] and indexed(s, stem):
                return {**out, "status": "acquired", "evidence_level": "full_text", "detail": "already in corpus"}
            if a.status_only:
                return {**out, "status": row.get("status") or "pending", "detail": "status-only: not in corpus"}
            # -- download -------------------------------------------------
            if not (st and st["downloaded"]):
                try:
                    d = s.call("paper_download", {"doi": doi})
                except hs_mcp.ToolError as e:
                    if re.search(r"No open-access PDF|Not found|no .*pdf", e.text, re.I):
                        alt = alt_stem_in_corpus(s, doi, row.get("title", ""))
                        if alt:
                            return {**out, "stem": alt, "status": "acquired", "evidence_level": "full_text",
                                    "detail": f"download failed but already in corpus as {alt}"}
                        return {**out, "status": "paywalled", "evidence_level": "abstract_only", "detail": e.text[:200]}
                    return {**out, "status": "transient", "detail": "download: " + e.text[:200]}
                if isinstance(d, dict) and d.get("path"):
                    stem = Path(d["path"]).stem
                    out["stem"] = stem
                st = stem_state(s, stem)
            # -- convert --------------------------------------------------
            if not (st and st["converted"]):
                if row.get("status") == "convert_pending_verify" and in_flight(s) > 0:
                    return {**out, "status": "convert_pending_verify", "detail": "server still has conversions in flight; not resending"}
                try:
                    s.call("scribe_convert", {"stem": stem}, timeout=a.convert_timeout)
                except hs_mcp.ToolError as e:
                    if re.search(r"0 non-whitespace|non-whitespace chars", e.text, re.I):
                        return {**out, "status": "unconvertible", "evidence_level": "abstract_only",
                                "detail": "empty/gate page: " + e.text[:160]}
                    if re.search(r"Stream read error|deadline", e.text, re.I):
                        return {**out, "status": "transient", "detail": "convert (server deadline? see SKILL.md hazards): " + e.text[:160]}
                    return {**out, "status": "transient", "detail": "convert: " + e.text[:200]}
                except (httpx.HTTPError, hs_mcp.McpError) as e:
                    # Outcome unknown; server may still be converting. Poll, never resend.
                    st = poll(s, stem, want_embedded=False, wait=a.verify_wait)
                    if not (st and st["converted"]):
                        return {**out, "status": "convert_pending_verify", "detail": f"client error {type(e).__name__}; polled {a.verify_wait}s"}
            # -- embed ----------------------------------------------------
            st = poll(s, stem, want_embedded=True, wait=a.embed_wait)
            if st and st["converted"] and not st["embedded"]:
                try:
                    s.call("distill_index", {"stem": stem})
                except hs_mcp.ToolError as e:
                    return {**out, "status": "converted_not_embedded", "detail": "distill_index: " + e.text[:200]}
                st = stem_state(s, stem)
            if not (st and st["converted"]):
                return {**out, "status": "downloaded", "detail": "not converted yet"}
            reason = gate_check(s, stem)
            if reason:
                return {**out, "status": "unconvertible", "evidence_level": "abstract_only", "detail": reason}
            if not indexed(s, stem):
                return {**out, "status": "converted_not_embedded", "detail": "distill_exists=false"}
            return {**out, "status": "acquired", "evidence_level": "full_text", "detail": "verified: catalog + distill_exists"}
    except (httpx.HTTPError, hs_mcp.McpError) as e:
        return {**out, "status": "transient", "detail": f"{type(e).__name__}: {e}"[:200]}


def in_flight(s) -> int:
    try:
        h = s.call("scribe_health", {})
        return int(h["readiness"]["in_flight_conversions"])
    except Exception:  # noqa: BLE001
        return 0


def alt_stem_in_corpus(s, doi: str, title: str) -> str:
    """A DOI can fail the resolver chain yet already be readable under another stem."""
    if not title:
        return ""
    try:
        hits = s.call("distill_search", {"query": title, "limit": 5, "include_text": False})
    except Exception:  # noqa: BLE001
        return ""
    for h in hits if isinstance(hits, list) else []:
        if hs_mcp.norm_doi(h.get("doi")) == hs_mcp.norm_doi(doi) and h.get("doc_id"):
            return h["doc_id"]
    return ""


def load_targets(a) -> list[dict]:
    rows = []
    if a.dois:
        for l in Path(a.dois).read_text().splitlines():
            d = hs_mcp.norm_doi(l.split("#")[0].strip())
            if d:
                rows.append({"doi": d, "tier": "", "title": "", "year": ""})
    else:
        tiers = {t.strip() for t in a.tiers.split(",")}
        for r in read_tsv(Path(a.pool)):
            excluded = any(str(r.get(c, "")).lower().startswith("excl") for c in ("screen_final", "ft_decision"))
            if r.get("doi") and r.get("tier") in tiers and not excluded:
                rows.append({"doi": hs_mcp.norm_doi(r["doi"]), "tier": r["tier"], "title": r.get("title", ""), "year": r.get("year", "")})
    seen, out = set(), []
    for r in rows:
        if r["doi"] not in seen:
            seen.add(r["doi"])
            out.append(r)
    return out


def write_views(out: Path, state: dict[str, dict], abstracts: dict[str, dict], abs_tiers: set[str]) -> dict:
    rows = list(state.values())
    groups = {
        "acquired": [r for r in rows if r["status"] == "acquired"],
        "paywalled": [r for r in rows if r["status"] == "paywalled"],
        "unconvertible": [r for r in rows if r["status"] == "unconvertible"],
        "pending": [r for r in rows if r["status"] not in TERMINAL],
    }
    for name, g in groups.items():
        write_tsv(out / f"{name}.tsv", STATE_COLS, g)
    ao = []
    for r in rows:
        if r["status"] in ("paywalled", "unconvertible") and r.get("tier") in abs_tiers:
            ab = abstracts.get(r["doi"], {})
            ao.append({**r, "detail": (r.get("detail", "") + " | ABSTRACT-ONLY EVIDENCE: " + (ab.get("abstract", "NO ABSTRACT AVAILABLE")))[:1500]})
    write_tsv(out / "abstract-only.tsv", STATE_COLS, ao)
    return {k: len(v) for k, v in groups.items()} | {"abstract_only": len(ao)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    hs_mcp.add_common_args(ap)
    ap.add_argument("--pool", help="candidate-pool.tsv")
    ap.add_argument("--tiers", default="core,adjacent", help="pool `tier` values to acquire")
    ap.add_argument("--dois", help="file of DOIs (alternative to --pool)")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--concurrency", type=int, default=2,
                    help="parallel conversions. MUST be <= the VLM backend's true slot count (default 2; capped by scribe_health slots)")
    ap.add_argument("--max-papers", type=int, help="process at most N not-yet-terminal papers this run")
    ap.add_argument("--retry", default="", help="comma list of terminal statuses to retry: paywalled,unconvertible,all")
    ap.add_argument("--status-only", action="store_true", help="only verify against the catalog; no download/convert")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--convert-timeout", type=float, default=1800)
    ap.add_argument("--verify-wait", type=float, default=900, help="after an ambiguous convert timeout, poll catalog this long (no resend)")
    ap.add_argument("--embed-wait", type=float, default=180, help="wait for event-watch embedding before calling distill_index")
    ap.add_argument("--abstract-only-tiers", default="core", help="paywalled rows in these tiers are kept as flagged abstract-only evidence")
    a = ap.parse_args()
    if not (a.pool or a.dois):
        ap.error("need --pool or --dois")

    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    state_path = out / "acquisition.tsv"
    state = {r["doi"]: r for r in read_tsv(state_path)}
    targets = load_targets(a)
    retry = {x.strip() for x in a.retry.split(",") if x.strip()}
    todo = []
    for t in targets:
        cur = state.setdefault(t["doi"], {c: "" for c in STATE_COLS} | {"doi": t["doi"], "status": "pending"})
        cur.update({k: t[k] for k in ("tier", "title", "year") if t.get(k)})
        if cur["status"] in TERMINAL and not (cur["status"] in retry or "all" in retry):
            continue
        todo.append(cur)
    if a.max_papers:
        todo = todo[: a.max_papers]
    print(f"{len(targets)} targets; {len(todo)} to process; {len(targets) - len(todo)} already terminal", file=sys.stderr)

    url = hs_mcp.resolve_url(a.url)
    with hs_mcp.session(url) as s:
        try:
            h = s.call("scribe_health", {})
            r = h["readiness"]
            print(f"scribe: in_flight={r['in_flight_conversions']} slots={r['vlm_slots_available']}/{r['vlm_slots_total']} (declared; backend may serve fewer)", file=sys.stderr)
            if r["in_flight_conversions"] > 0:
                print("WARNING: conversions already in flight (watcher backlog or orphans); keeping concurrency low", file=sys.stderr)
            conc = max(1, min(a.concurrency, r["vlm_slots_available"] or 1))
        except Exception as e:  # noqa: BLE001
            print(f"scribe_health failed ({e}); using --concurrency", file=sys.stderr)
            conc = a.concurrency
    if a.dry_run:
        for r in todo:
            print(f"would process {r['doi']} [{r.get('tier')}] status={r['status']}")
        return 0

    def work(row):
        res = process(url, row, a)
        with _lock:
            row.update(res)
            row["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            write_tsv(state_path, STATE_COLS, list(state.values()))
        print(f"{row['doi']:<45} {row['status']:<24} {row.get('detail', '')[:90]}", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=conc) as ex:
        list(ex.map(work, todo))

    abstracts = {}
    ap_path = out / "abstracts.jsonl"
    if ap_path.exists():
        for l in ap_path.read_text(encoding="utf-8").splitlines():
            try:
                j = json.loads(l)
                abstracts[hs_mcp.norm_doi(j.get("doi"))] = j
            except Exception:
                pass
    write_tsv(state_path, STATE_COLS, list(state.values()))
    counts = write_views(out, state, abstracts, {t.strip() for t in a.abstract_only_tiers.split(",")})
    print(json.dumps({"counts": counts, "state": str(state_path)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
