#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]  # discover.py (imported for the pool schema) needs it
# ///
"""Two-independent-pass screening bookkeeping: export batches, ingest decisions, agreement stats, recall audit.

Practices implemented (sources in reference/methodology-process.md):
  * pilot first on 50-100 records assessed by all screeners, then revise criteria  [P17 'Study selection']
  * dual INDEPENDENT screening, agreement quantified with Cohen's kappa, disagreements resolved by a stated
    procedure                                                                      [P18, P01 item 8]
  * err toward inclusion at title/abstract stage; 'unsure' counts as include        [P18 'Scoping'; section 9 'Screening' row]
  * kappa AND prevalence-adjusted kappa reported together: with class imbalance kappa is deflated/inflated
    and PABAK can look excellent regardless                                         [P38 AB, P39 AB; the PABAK remark is an [INFERENCE] in methodology-process.md 8.2]
  * a recall audit: a random sample of records BOTH passes excluded is re-read      [section 9 'Human-in-the-loop' row: audit samples with acceptance thresholds, P25]
  * a reason is recorded for every exclusion (full-text exclusions: ft_reason)      [P01 item 16b, P18]
DISCLOSURE (must appear in the report): two LLM passes are NOT shown to be equivalent to two human screeners
(methodology-process.md section 9 'Screening' row: literature gap [INFERENCE]); the audit sample and kappa are
the compensating controls. Single-screen error is not trivial (13% missed [P28 AB]) but humans err too
(10.76% [P29]).

Subcommands
  export   --pool corpus/candidate-pool.tsv --pass A|B --out batch-A.jsonl [--limit N] [--pilot]
           -> one JSON object per pool row still undecided for that pass: {key,title,year,abstract,abstract_missing}
  ingest   --pool ... --pass A|B --decisions decisions-A.jsonl
           decisions: {"key","decision":"include|exclude|unsure","reason":"<code: text>","confidence":0-1}
           Pass A writes screen1_*, pass B writes screen2_*. A pass MUST NOT see the other pass's decisions
           (export never includes them; give each pass its own subagent and prompt variant).
  stats    --pool ... [--audit-n 25 --seed 7]
           -> screening-stats.json (n, agreement, kappa, PABAK, prevalence), screening-disagreements.tsv,
              recall-audit.tsv (random sample of both-excluded records, to be re-read)
  finalize --pool ...
           agreed decisions -> screen_final (+reason); disagreements stay blank until adjudicated with
           `adjudicate --key K --decision include|exclude --reason R --by WHO`
  adjudicate  (single record) sets screen_final + screen_adjudicator
Exit code 0 always except usage errors; read the printed numbers.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from discover import AGENT_COLS, POOL_COLS, read_tsv, write_tsv  # noqa: E402

DECISIONS = {"include", "exclude", "unsure"}


def load_pool(p: Path):
    rows = read_tsv(p)
    if not rows:
        raise SystemExit(f"empty or missing pool: {p}")
    for r in rows:
        for c in POOL_COLS:
            r.setdefault(c, "")
    return rows


def load_abstracts(pool: Path) -> dict:
    out = {}
    ap = pool.parent / "abstracts.jsonl"
    if ap.exists():
        for l in ap.read_text(encoding="utf-8").splitlines():
            try:
                j = json.loads(l)
                out[j["key"]] = j.get("abstract", "")
            except Exception:  # noqa: BLE001
                pass
    return out


def cohen(a: list[bool], b: list[bool]) -> dict:
    n = len(a)
    if n == 0:
        return {"n": 0}
    agree = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    kappa = 1.0 if pe == 1 else (agree - pe) / (1 - pe)
    return {"n": n, "agreement": round(agree, 4), "kappa": round(kappa, 4), "pabak": round(2 * agree - 1, 4),
            "prevalence_include_A": round(pa, 4), "prevalence_include_B": round(pb, 4)}


def cmd_export(a) -> int:
    pool = Path(a.pool)
    rows = load_pool(pool)
    col = "screen1_decision" if a.pass_ == "A" else "screen2_decision"
    abstracts = load_abstracts(pool)
    todo = [r for r in rows if not r[col]]
    if a.pilot:
        random.Random(a.seed).shuffle(todo)
        todo = todo[: a.limit or 75]  # pilot: 50-100 records assessed by ALL screeners [P17]
    elif a.limit:
        todo = todo[: a.limit]
    with open(a.out, "w", encoding="utf-8") as f:
        for r in todo:
            ab = abstracts.get(r["key"], "")
            f.write(json.dumps({"key": r["key"], "doi": r["doi"], "title": r["title"], "year": r["year"], "abstract": ab,
                                "abstract_missing": not ab}, ensure_ascii=False) + "\n")
    print(f"exported {len(todo)} undecided records for pass {a.pass_} -> {a.out} "
          f"({sum(1 for r in todo if not abstracts.get(r['key']))} lack an abstract: run `discover.py abstracts` first)")
    return 0


def cmd_ingest(a) -> int:
    pool = Path(a.pool)
    rows = load_pool(pool)
    idx = {r["key"]: r for r in rows}
    pre = "screen1" if a.pass_ == "A" else "screen2"
    n = bad = 0
    for line in Path(a.decisions).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        dec = str(d.get("decision", "")).lower()
        r = idx.get(d.get("key"))
        if r is None or dec not in DECISIONS or (dec == "exclude" and not str(d.get("reason", "")).strip()):
            bad += 1
            print(f"rejected: {str(d)[:140]}  (unknown key, bad decision, or exclusion without a reason)", file=sys.stderr)
            continue
        r[f"{pre}_decision"], r[f"{pre}_reason"], r[f"{pre}_conf"] = dec, str(d.get("reason", "")), str(d.get("confidence", ""))
        n += 1
    write_tsv(pool, POOL_COLS, rows)
    print(f"ingested {n} decisions for pass {a.pass_}; rejected {bad}")
    return 0


def inc(x: str) -> bool:
    return x in ("include", "unsure")  # err toward inclusion at title/abstract stage


def cmd_stats(a) -> int:
    pool = Path(a.pool)
    rows = load_pool(pool)
    both = [r for r in rows if r["screen1_decision"] and r["screen2_decision"]]
    A = [inc(r["screen1_decision"]) for r in both]
    B = [inc(r["screen2_decision"]) for r in both]
    st = cohen(A, B)
    st["n_screened_A"] = sum(1 for r in rows if r["screen1_decision"])
    st["n_screened_B"] = sum(1 for r in rows if r["screen2_decision"])
    st["n_unsure_A"] = sum(1 for r in rows if r["screen1_decision"] == "unsure")
    st["n_unsure_B"] = sum(1 for r in rows if r["screen2_decision"] == "unsure")
    dis = [r for r in both if inc(r["screen1_decision"]) != inc(r["screen2_decision"])]
    write_tsv(pool.parent / "screening-disagreements.tsv",
              ["key", "doi", "title", "screen1_decision", "screen1_reason", "screen2_decision", "screen2_reason", "screen_final", "screen_adjudicator"], dis)
    both_ex = [r for r in both if not inc(r["screen1_decision"]) and not inc(r["screen2_decision"])]
    random.Random(a.seed).shuffle(both_ex)
    audit = both_ex[: a.audit_n]
    prev = {r["key"]: r for r in read_tsv(pool.parent / "recall-audit.tsv")}
    for r in audit:
        r["audit_verdict"] = prev.get(r["key"], {}).get("audit_verdict", "")
    write_tsv(pool.parent / "recall-audit.tsv", ["key", "doi", "title", "screen1_reason", "screen2_reason", "audit_verdict"], audit)
    st["n_disagreements"] = len(dis)
    st["both_excluded"] = len(both_ex)
    st["recall_audit_sample"] = len(audit)
    done = [r for r in audit if r["audit_verdict"]]
    wrong = [r for r in done if r["audit_verdict"].lower().startswith("incl")]
    st["recall_audit_reviewed"] = len(done)
    st["recall_audit_wrongly_excluded"] = len(wrong)
    st["note"] = ("kappa deflates when one class dominates; pabak inflates. Report both. Re-read recall-audit.tsv and fill "
                  "audit_verdict (include|exclude); any wrongly-excluded record means the exclusion criteria/prompt need revision "
                  "and BOTH passes must be rerun on the excluded set (criteria revisions after borderline cases => redo the sift [P18]).")
    (pool.parent / "screening-stats.json").write_text(json.dumps(st, indent=1), encoding="utf-8")
    print(json.dumps(st, indent=1))
    return 0


def cmd_finalize(a) -> int:
    pool = Path(a.pool)
    rows = load_pool(pool)
    n_agree = n_open = 0
    for r in rows:
        if r["screen_final"] or not (r["screen1_decision"] and r["screen2_decision"]):
            continue
        d1, d2 = r["screen1_decision"], r["screen2_decision"]
        if inc(d1) == inc(d2):
            r["screen_final"] = "include" if inc(d1) else "exclude"
            r["screen_final_reason"] = r["screen1_reason"] if not inc(d1) else (r["screen1_reason"] or r["screen2_reason"])
            r["screen_adjudicator"] = "agreement"
            n_agree += 1
        else:
            n_open += 1
    write_tsv(pool, POOL_COLS, rows)
    print(f"finalized {n_agree} agreed records; {n_open} disagreements await `adjudicate` (see screening-disagreements.tsv)")
    return 0


def cmd_adjudicate(a) -> int:
    pool = Path(a.pool)
    rows = load_pool(pool)
    for r in rows:
        if r["key"] == a.key:
            r["screen_final"], r["screen_final_reason"], r["screen_adjudicator"] = a.decision, a.reason, a.by
            write_tsv(pool, POOL_COLS, rows)
            print(f"{a.key}: {a.decision} ({a.by})")
            return 0
    print("key not found", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("export", "ingest", "stats", "finalize", "adjudicate"):
        s = sub.add_parser(n)
        s.add_argument("--pool", required=True)
    e = sub.choices["export"]
    e.add_argument("--pass", dest="pass_", choices=["A", "B"], required=True)
    e.add_argument("--out", required=True)
    e.add_argument("--limit", type=int)
    e.add_argument("--pilot", action="store_true", help="random 50-100 records for the pilot (default 75)")
    e.add_argument("--seed", type=int, default=7)
    i = sub.choices["ingest"]
    i.add_argument("--pass", dest="pass_", choices=["A", "B"], required=True)
    i.add_argument("--decisions", required=True)
    t = sub.choices["stats"]
    t.add_argument("--audit-n", type=int, default=25)
    t.add_argument("--seed", type=int, default=7)
    d = sub.choices["adjudicate"]
    d.add_argument("--key", required=True)
    d.add_argument("--decision", choices=["include", "exclude"], required=True)
    d.add_argument("--reason", required=True)
    d.add_argument("--by", required=True, help="who adjudicated: a third agent pass id or 'user'")
    a = ap.parse_args()
    return {"export": cmd_export, "ingest": cmd_ingest, "stats": cmd_stats, "finalize": cmd_finalize, "adjudicate": cmd_adjudicate}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
