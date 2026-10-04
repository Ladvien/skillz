#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Create a research-synthesis run directory under slop/research/<YYYY-MM-DD>-<slug>/.

Layout:
  protocol.md  scope.md                    (from templates/, topic/date filled in; NEVER overwritten)
  queries/     search + RQ query files
  corpus/      candidate-pool.tsv, search-log.tsv, abstracts.jsonl, acquisition.tsv + views
  evidence/    evidence.jsonl, retrieval-log.tsv, evidence-summary.tsv
  notes/papers/<stem>.md                   one structured note per deep-read paper
  synthesis/                               evidence-matrix, certainty table, insight workbook
  report.md  audit.md  (later)

Run: uv run --script init_run.py "link between chronic sleep loss and risky decision-making"
Prints the run directory path (last line) so callers can capture it.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
STOP = {"the", "a", "an", "of", "and", "or", "to", "in", "on", "for", "between", "with", "is", "are", "be", "being", "that", "this", "how", "why", "what", "does", "do"}


def slugify(topic: str, maxlen: int = 48) -> str:
    t = unicodedata.normalize("NFKD", topic).encode("ascii", "ignore").decode().lower()
    words = [w for w in re.findall(r"[a-z0-9]+", t)]
    kept = [w for w in words if w not in STOP] or words
    slug = "-".join(kept)
    return slug[:maxlen].rstrip("-") or "topic"


def find_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / ".claude").is_dir():
            return p
    return start


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("topic")
    ap.add_argument("--slug")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--root", help="repo root (default: nearest ancestor of cwd containing .claude/)")
    a = ap.parse_args()

    root = Path(a.root) if a.root else find_root(Path.cwd())
    run = root / "slop" / "research" / f"{a.date}-{a.slug or slugify(a.topic)}"
    for d in ("queries", "corpus", "evidence", "notes/papers", "synthesis"):
        (run / d).mkdir(parents=True, exist_ok=True)
    subs = {"{{topic}}": a.topic, "{{date}}": a.date, "{{slug}}": run.name, "{{run_dir}}": str(run.relative_to(root))}
    for name in ("protocol.md", "scope.md"):
        dst = run / name
        if dst.exists():
            print(f"keep existing {dst}", file=sys.stderr)
            continue
        txt = (SKILL / "templates" / name).read_text(encoding="utf-8")
        for k, v in subs.items():
            txt = txt.replace(k, v)
        dst.write_text(txt, encoding="utf-8")
    print(run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
