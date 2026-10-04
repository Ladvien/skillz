#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""Extraction verification pass for paper notes (evidence-anchored extraction).

Rules enforced (methodology-process.md section 9 'Extraction/charting' row; methodology-synthesis.md section 8 item 2):
  * every extracted value carries a VERBATIM supporting quote + stem + page            [P17 recs 11-12; P41 AB: ~4% confabulation]
  * a value that the paper does not state is recorded as `null` / `not reported`, never filled in
  * a second pass re-checks that each quote exists in the paper (and on the cited page) [P17 'one extracts, second verifies'; P20]
  * appraisal judgements need a supporting quote or an explicit NI (no information)    [S23 'support quotes'; synthesis 1.6 rule 2]

For each notes/papers/<stem>.md (skipping notes with `evidence_level: abstract_only`) every markdown table with a
column whose header contains "quote" is checked, row by row:
  FAIL  quote not found in the paper's text                      (page-restricted when the row's location says p.N)
  FAIL  a statistic/effect/judgement cell is filled but the quote cell is empty (and not NI / null / not reported)
  WARN  quote found only approximately (OCR / hyphenation)
  WARN  location column empty for a row with a quote
Writes <run>/notes/verification.tsv; exit 1 on any FAIL. Spot-check 10-20% of notes by hand as well; a single
extraction error means re-verifying that reader's whole batch.

Run: uv run --script verify_notes.py --run slop/research/<run> [--stem STEM ...]
"""
from __future__ import annotations

import argparse
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hs_mcp  # noqa: E402
import refmeta  # noqa: E402
from audit import norm_text, quote_status  # noqa: E402

NULLS = re.compile(r"^\W*(null|n/?a|ni|no information|not reported|not stated|none|-+)\W*$", re.I)


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def tables(text: str):
    """Yield (header, [(lineno, cells)]) for each markdown table."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        if lines[i].lstrip().startswith("|") and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            header = split_row(lines[i])
            rows, j = [], i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append((j + 1, split_row(lines[j])))
                j += 1
            yield header, rows
            i = j
        else:
            i += 1


def fetch(url: str, stem: str, page: int | None) -> str:
    try:
        with hs_mcp.session(url) as s:
            args = {"stem": stem} | ({"page": page} if page else {})
            return s.call_text("markdown_read", args, timeout=300)
    except Exception:  # noqa: BLE001
        return ""


def check_note(url: str, path: Path) -> list[dict]:
    stem = path.stem
    text = path.read_text(encoding="utf-8")
    fm = refmeta.parse_front_matter(path)
    out = []
    if fm.get("evidence_level") == "abstract_only":
        return [{"stem": stem, "level": "INFO", "line": "", "msg": "abstract_only note: no full-text verification possible"}]
    full = norm_text(fetch(url, stem, None))
    if not full:
        return [{"stem": stem, "level": "FAIL", "line": "", "msg": "could not read the paper's markdown (not in corpus?)"}]
    pages: dict[int, str] = {}
    for header, rows in tables(text):
        low = [h.lower() for h in header]
        qi = next((k for k, h in enumerate(low) if "quote" in h), None)
        if qi is None:
            continue
        li = next((k for k, h in enumerate(low) if "location" in h or h.startswith("page")), None)
        vi = [k for k, h in enumerate(low) if any(w in h for w in ("effect", "statistic", "judgement", "judgment", "result"))]
        for ln, cells in rows:
            if len(cells) <= qi or not any(c for c in cells):
                continue
            quote = cells[qi].strip().strip("\"'\u201c\u201d")
            vals = [cells[k] for k in vi if k < len(cells) and cells[k] and not NULLS.match(cells[k])]
            loc = cells[li] if li is not None and li < len(cells) else ""
            if not quote or NULLS.match(quote):
                if vals:
                    out.append({"stem": stem, "level": "FAIL", "line": ln, "msg": f"value without supporting quote: {vals[0][:60]!r} (add the verbatim quote, or record null/NI)"})
                continue
            if len(quote.split()) < 4:
                out.append({"stem": stem, "level": "WARN", "line": ln, "msg": f"quote too short to verify: {quote!r}"})
                continue
            m = re.search(r"\bp\.?\s*(\d+)", loc)
            pool = full
            if m:
                pg = int(m.group(1))
                if pg not in pages:
                    pages[pg] = norm_text(fetch(url, stem, pg))
                pool = pages[pg] or full
            st = quote_status(quote, [pool])
            if st == "missing" and m and pool is not full and quote_status(quote, [full]) != "missing":
                out.append({"stem": stem, "level": "FAIL", "line": ln, "msg": f"quote exists in the paper but NOT on cited page {m.group(1)}: {quote[:70]!r}"})
            elif st == "missing":
                out.append({"stem": stem, "level": "FAIL", "line": ln, "msg": f"quote not found in paper text: {quote[:70]!r}"})
            elif st == "approx":
                out.append({"stem": stem, "level": "WARN", "line": ln, "msg": f"quote only approximately matches: {quote[:70]!r}"})
            if not loc:
                out.append({"stem": stem, "level": "WARN", "line": ln, "msg": "row has a quote but no location"})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    hs_mcp.add_common_args(ap)
    ap.add_argument("--run", required=True)
    ap.add_argument("--stem", nargs="*")
    ap.add_argument("--concurrency", type=int, default=4)
    a = ap.parse_args()
    url = hs_mcp.resolve_url(a.url)
    nd = Path(a.run) / "notes" / "papers"
    files = sorted(nd.glob("*.md"))
    if a.stem:
        files = [f for f in files if f.stem in a.stem]
    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        res = list(ex.map(lambda f: check_note(url, f), files))
    findings = [x for r in res for x in r]
    outp = Path(a.run) / "notes" / "verification.tsv"
    with outp.open("w", encoding="utf-8") as f:
        f.write("stem\tlevel\tline\tmsg\n")
        for x in findings:
            f.write(f"{x['stem']}\t{x['level']}\t{x['line']}\t{x['msg']}\n")
    nf = sum(1 for x in findings if x["level"] == "FAIL")
    nw = sum(1 for x in findings if x["level"] == "WARN")
    for x in findings:
        if x["level"] != "INFO":
            print(f"{x['level']:<4} {x['stem']} L{x['line']}: {x['msg']}")
    print(f"{len(files)} notes verified: FAIL {nf}, WARN {nw} -> {outp}")
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
