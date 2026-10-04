"""Reference metadata resolution shared by refs.py and audit.py.

Rule: a citation is only ever built from a RESOLVED record. Many home-still stems have empty
title/doi in catalog_read; for those we never guess. Status values:

  verified       title+year (and usually DOI) from catalog_read or openalex_get
  provider       identity read from the paper's own first page by a paper-reader AND confirmed by a
                 provider title search (note front matter `meta_verified: provider`)
  document-only  identity read from the paper's own text only (note front matter
                 `meta_verified: document-only`): printable, but flagged [metadata from document text only]
  unresolved     nothing trustworthy: print stem + UNRESOLVED flag only; NEVER a guessed title

Paper-note front matter (templates/paper-note.md) supplies title/authors/year/doi/meta_verified.
"""
from __future__ import annotations

import re
from pathlib import Path

import hs_mcp

UNRESOLVED_FLAG = "**[UNRESOLVED METADATA: identity not verified; do not rely on this citation until resolved]**"
DOCONLY_FLAG = "[metadata from document text only]"


def parse_front_matter(path: Path) -> dict:
    """Minimal `key: value` YAML front matter parser (flat keys; lists as `[a, b]` or ignored)."""
    if not path.exists():
        return {}
    txt = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", txt, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if mm:
            v = mm.group(2).strip().strip("'\"")
            out[mm.group(1)] = v
    return out


def short_authors(names: list[str], limit: int = 3) -> str:
    seen, out = set(), []
    for n in names:
        n = (n or "").strip()
        if not n:
            continue
        if "," in n:
            sur, _, first = n.partition(",")
        else:
            parts = n.split()
            sur, first = (parts[-1], " ".join(parts[:-1])) if len(parts) > 1 else (n, "")
        sur, first = sur.strip(), first.strip()
        init = first[:1].upper()
        k = (sur.lower(), init)
        if k in seen or not sur:
            continue
        seen.add(k)
        out.append(f"{sur} {init}".strip())
    if not out:
        return ""
    return ", ".join(out[:limit]) + (" et al." if len(out) > limit else "")


def openalex_authors(s: hs_mcp.Session, key: str) -> list[str]:
    """Author names in true authorship order. catalog_read author lists merge providers (duplicate
    'Last, F.' / 'First Last' forms, arbitrary order) so they must NOT be used for the author string.
    OpenAlex rows carry author_position (first|middle|last): first first, last last, de-duplicated."""
    try:
        g = s.call("openalex_get", {"id_or_doi": key})
    except (hs_mcp.ToolError, hs_mcp.McpError):
        return []
    rows = g.get("authors") if isinstance(g, dict) else None
    if not rows:
        return []
    order = {"first": 0, "middle": 1, "last": 2}
    seen, out = set(), []
    for i, a in sorted(enumerate(rows), key=lambda t: (order.get(t[1].get("author_position"), 1), t[0])):
        k = a.get("openalex_id") or a.get("display_name")
        if k and k not in seen:
            seen.add(k)
            out.append(a.get("display_name", ""))
    return out


def resolve_reference(s: hs_mcp.Session, stem: str, notes_dir: Path | None = None) -> dict:
    m = hs_mcp.resolve_meta(s, stem)
    rec = {"stem": stem, "status": "unresolved", "title": "", "authors": "", "year": "", "doi": "", "source": m.get("source", ""),
           "in_catalog": m["in_catalog"], "converted": m["converted"], "embedded": m["embedded"], "guess": ""}
    if m["source"] in ("catalog", "openalex") and m["title"] and m["year"]:
        names = openalex_authors(s, m["doi"] or stem)
        rec.update(status="verified", title=m["title"], authors=short_authors(names), year=m["year"], doi=m["doi"])
        return rec
    if m["source"] == "markdown_head":
        rec["guess"] = m["title"]  # kept ONLY for the sidecar to-do list; never printed in a citation
    if notes_dir is not None:
        fm = parse_front_matter(notes_dir / f"{stem}.md")
        mv = fm.get("meta_verified", "")
        if mv in ("provider", "document-only") and fm.get("title") and re.fullmatch(r"(19|20)\d\d", fm.get("year", "")):
            rec.update(status="provider" if mv == "provider" else "document-only", title=fm["title"],
                       authors=fm.get("authors", ""), year=fm["year"], doi=hs_mcp.norm_doi(fm.get("doi")), source="note:" + mv)
    return rec


def format_entry(rec: dict, abstract_only: bool = False) -> str:
    """One References-appendix line. Unresolved records never carry a title/year/author."""
    tail = " [abstract-only]" if abstract_only else ""
    if rec["status"] == "unresolved":
        return f"- [@{rec['stem']}] {UNRESOLVED_FLAG}{tail}"
    doi = f" https://doi.org/{rec['doi']}" if rec["doi"] else ""
    flag = f" {DOCONLY_FLAG}" if rec["status"] == "document-only" else ""
    who = f"{rec['authors']} " if rec["authors"] else ""
    return f"- [@{rec['stem']}] {who}({rec['year']}). {rec['title'].rstrip('.')}.{doi}{flag}{tail}"
