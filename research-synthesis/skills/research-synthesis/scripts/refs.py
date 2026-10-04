#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""Build the References appendix from the report's own [@stem] citations -- never from memory.

Every entry is generated from a RESOLVED record (catalog_read / openalex_get, or a paper note whose
front matter says meta_verified: provider|document-only). Stems whose metadata is empty in home-still
(common: OpenAlex W-ids, PubMed ids, hash names) are printed as UNRESOLVED -- stem + flag only, no
guessed title -- and listed in synthesis/unresolved-stems.tsv with the text-head guess as a to-do hint
for the paper-reader (who must verify identity from the document and confirm via a provider title search).

  refs.py --report report.md            print entries to stdout
  refs.py --report report.md --write    replace the block between <!-- REFS:BEGIN --> and <!-- REFS:END -->
  refs.py --stems stems.txt             build from a stem list instead

`[abstract-only]` is appended when the stem has no converted+embedded full text.
Run: uv run --script refs.py --report slop/research/<run>/report.md --write
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

CITE_BLOCK = re.compile(r"\[([^\[\]]*?@[^\[\]]*?)\]")
BEGIN, END = "<!-- REFS:BEGIN -->", "<!-- REFS:END -->"


def cited_stems(text: str) -> list[str]:
    body = re.sub(rf"{re.escape(BEGIN)}.*?{re.escape(END)}", "", text, flags=re.S)  # ignore the old appendix
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)  # guidance comments are not citations
    out = []
    for m in CITE_BLOCK.finditer(body):
        for part in m.group(1).split(";"):
            part = part.strip()
            if part.startswith("@"):
                k = re.split(r",\s", part[1:], maxsplit=1)[0].strip()
                if k and k not in out:
                    out.append(k)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    hs_mcp.add_common_args(ap)
    ap.add_argument("--report")
    ap.add_argument("--stems")
    ap.add_argument("--notes-dir")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--concurrency", type=int, default=4)
    a = ap.parse_args()
    if not (a.report or a.stems):
        ap.error("need --report or --stems")
    url = hs_mcp.resolve_url(a.url)
    rp = Path(a.report) if a.report else None
    base = rp.parent if rp else Path(a.stems).parent
    notes_dir = Path(a.notes_dir) if a.notes_dir else base / "notes" / "papers"
    stems = cited_stems(rp.read_text(encoding="utf-8")) if rp else \
        [l.strip() for l in Path(a.stems).read_text().splitlines() if l.strip() and not l.startswith("#")]

    def one(stem):
        try:
            with hs_mcp.session(url) as s:
                return refmeta.resolve_reference(s, stem, notes_dir)
        except Exception as e:  # noqa: BLE001
            return {"stem": stem, "status": "unresolved", "title": "", "authors": "", "year": "", "doi": "",
                    "source": "error", "converted": False, "embedded": False, "guess": "", "err": str(e)[:100]}

    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        recs = list(ex.map(one, stems))
    recs.sort(key=lambda r: (r["authors"].lower() or "~", r["year"], r["stem"]))
    lines = [refmeta.format_entry(r, abstract_only=r["in_catalog"] and not (r["converted"] and r["embedded"])) for r in recs]
    block = "\n".join(lines)
    unresolved = [r for r in recs if r["status"] == "unresolved"]
    if unresolved:
        side = base / "synthesis"
        side.mkdir(parents=True, exist_ok=True)
        with (side / "unresolved-stems.tsv").open("w", encoding="utf-8") as f:
            f.write("stem\ttext_head_guess_UNVERIFIED\tnext_step\n")
            for r in unresolved:
                f.write(f"{r['stem']}\t{r['guess']}\tpaper-reader: read page 1, record identity in note front matter, confirm via paper_search(search_type=title)\n")
        print(f"WARNING: {len(unresolved)}/{len(recs)} cited stems have unresolved metadata -> {side / 'unresolved-stems.tsv'}", file=sys.stderr)
    if a.write and rp:
        txt = rp.read_text(encoding="utf-8")
        new = f"{BEGIN}\n{block}\n{END}"
        if BEGIN in txt and END in txt:
            txt = re.sub(rf"{re.escape(BEGIN)}.*?{re.escape(END)}", lambda m: new, txt, flags=re.S)
        else:
            txt = txt.rstrip() + f"\n\n## References\n\n{new}\n"
        rp.write_text(txt, encoding="utf-8")
        print(f"wrote {len(recs)} entries into {rp}", file=sys.stderr)
    else:
        print(block)
    return 0


if __name__ == "__main__":
    sys.exit(main())
