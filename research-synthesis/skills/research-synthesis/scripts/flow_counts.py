#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Compute PRISMA-style flow numbers from the run's own files (never hand-typed) and emit a mermaid diagram.

Reads  corpus/screening-stats.json, corpus/search-log.tsv, corpus/candidate-pool.tsv, corpus/acquisition.tsv, notes/papers/*.md,
       evidence/retrieval-log.tsv  (any may be missing -> that stage is reported as n/a)
Writes <run>/flow-counts.json and <run>/flow.mmd (paste into report.md "Methods").

Run: uv run --script flow_counts.py --run slop/research/<run>
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


def rd(p: Path) -> list[dict]:
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    a = ap.parse_args()
    run = Path(a.run)
    log = [r for r in rd(run / "corpus/search-log.tsv") if not r["provider"].startswith("snowball")]
    snow = [r for r in rd(run / "corpus/search-log.tsv") if r["provider"].startswith("snowball")]
    pool = rd(run / "corpus/candidate-pool.tsv")
    acq = rd(run / "corpus/acquisition.tsv")
    notes = list((run / "notes/papers").glob("*.md")) if (run / "notes/papers").exists() else []

    by_prov = Counter()
    for r in log:
        by_prov[r["provider"]] += int(r["n_returned"] or 0)
    identified_db = sum(by_prov.values())
    identified_snow = sum(int(r["n_returned"] or 0) for r in snow)
    unique = len(pool)
    screened = [r for r in pool if r.get("screen1_decision") or r.get("screen2_decision") or r.get("screen_final")]
    ta_excl = [r for r in pool if (r.get("screen_final") or "").lower().startswith("excl")]
    ft_excl = [r for r in pool if (r.get("ft_decision") or "").lower().startswith("excl")]
    excl = ta_excl + ft_excl
    reasons = Counter((r.get("ft_reason") or r.get("screen_final_reason") or "unspecified") for r in ft_excl)
    ta_reasons = Counter((r.get("screen_final_reason") or "unspecified") for r in ta_excl)
    unadjudicated = sum(1 for r in pool if r.get("screen1_decision") and r.get("screen2_decision") and not r.get("screen_final"))
    stats_p = run / "corpus/screening-stats.json"
    scr = json.loads(stats_p.read_text()) if stats_p.exists() else {}
    tiers = Counter(r.get("tier") or "untiered" for r in pool)
    st = Counter(r["status"] for r in acq)
    c = {
        "records_identified_search": identified_db, "records_identified_snowball": identified_snow,
        "identified_by_provider": dict(by_prov), "unique_after_dedup": unique,
        "duplicates_removed": identified_db + identified_snow - unique,
        "screened": len(screened), "excluded_title_abstract": len(ta_excl), "excluded_full_text": len(ft_excl),
        "title_abstract_exclusion_reasons": dict(ta_reasons), "full_text_exclusion_reasons": dict(reasons),
        "disagreements_unadjudicated": unadjudicated, "screening_agreement": scr, "tiers": dict(tiers),
        "sought_for_retrieval": len(acq), "acquisition_status": dict(st),
        "full_text_available": st.get("acquired", 0),
        "not_retrieved": st.get("paywalled", 0) + st.get("unconvertible", 0),
        "abstract_only_kept": len(rd(run / "corpus/abstract-only.tsv")),
        "deep_read_notes": len(notes),
        "retrieval_queries": len(rd(run / "evidence/retrieval-log.tsv")),
    }
    (run / "flow-counts.json").write_text(json.dumps(c, indent=1), encoding="utf-8")
    ex_lines = "<br/>".join(f"{n}: {k[:40]}" for k, n in reasons.most_common(5)) or "none recorded"
    kappa = f"kappa {scr['kappa']}, PABAK {scr['pabak']}" if scr.get("kappa") is not None else "agreement n/a"
    mmd = f"""```mermaid
flowchart TD
  A["Records identified: databases/search<br/>n = {identified_db}"] --> C
  B["Records identified: citation chasing<br/>n = {identified_snow}"] --> C
  C["After duplicate removal<br/>n = {unique}"] --> D
  D["Screened, 2 independent agent passes<br/>n = {len(screened)}<br/>{kappa}"] --> E["Excluded at title/abstract<br/>n = {len(ta_excl)}"]
  D --> F["Sought for full text<br/>n = {len(acq)}"]
  F --> X["Excluded on full text (reason recorded)<br/>n = {len(ft_excl)}<br/>{ex_lines}"]
  F --> G["Not retrieved (paywalled / unconvertible)<br/>n = {c['not_retrieved']}<br/>kept as abstract-only: {c['abstract_only_kept']}"]
  F --> H["Full text in corpus (converted + indexed)<br/>n = {c['full_text_available']}"]
  H --> I["Deep-read with structured notes<br/>n = {c['deep_read_notes']}"]
```
"""
    (run / "flow.mmd").write_text(mmd, encoding="utf-8")
    print(json.dumps(c, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
