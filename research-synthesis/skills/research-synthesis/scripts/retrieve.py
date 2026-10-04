#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""Retrieval: research-question query set -> evidence ledger (JSONL).

Query file: one per line, `RQ1 :: query text` (RQ label is free text; blank/`#` lines ignored).
Run several paraphrases per RQ (different vocabularies, populations, methods) -- semantic search is
sensitive to wording and a single query is never exhaustive.

Each ledger row: rq, query, tool, rank, stem (doc_id), doi, title, year, score, page, line_start,
line_end, likely_refs (chunk looks like a reference list -> usually noise), text, retrieved_at.
Titles/DOIs are EMPTY for many doc_ids (OpenAlex W-ids, PubMed ids, hash names); they are back-filled via
hs_mcp.resolve_meta (catalog_read -> openalex_get -> markdown first heading). `meta_source` records which
answered; `markdown_head` is an unverified guess, `none` means identify the paper by reading it.

Outputs (in --out-dir):
  evidence.jsonl         append-only ledger, deduped on (rq, stem, line_start, line_end); resumable
                         (a (rq, query, tool) triple already in retrieval-log.tsv is skipped unless --force)
  retrieval-log.tsv      one row per executed query (n hits) -> search-reporting evidence
  evidence-summary.tsv   per (rq, stem): n_hits, n_queries, max_score, mean_score, title, year, doi
                         (ranks which papers to deep-read; NOT a quality ranking)

--restrict-stems FILE   keep only hits whose stem is in FILE (e.g. core+adjacent acquired stems);
                        retrieval is over-fetched (x3) so filtering still yields --limit hits.
--tool both             distill_search (chunk-level) + abstract_search (paper-level, 1 point per paper)

Run: uv run --script retrieve.py --queries rq-queries.txt --out-dir evidence/
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hs_mcp  # noqa: E402

REF_PAT = re.compile(r"(\(\s*(19|20)\d\d[a-z]?\s*\)|\b(19|20)\d\d\b\.?\s*_?[A-Z][^\n]{0,80}_?\s*\*\*\d+\*\*|PubMed|Google Scholar|CrossRef|doi:\s*10\.)", re.I)


def likely_refs(text: str) -> bool:
    if not text:
        return False
    return len(REF_PAT.findall(text)) >= 4 or bool(re.search(r"(Article|PubMed|Google Scholar|CAS)\s*\n", text) and len(REF_PAT.findall(text)) >= 2)


def read_queries(p: Path) -> list[tuple[str, str]]:
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "::" in line:
            rq, q = line.split("::", 1)
            out.append((rq.strip(), q.strip()))
        else:
            out.append(("RQ?", line))
    return out


def search(url, tool, query, limit, year, include_text):
    with hs_mcp.session(url) as s:
        res = hs_mcp.call_retry(s, tool, {"query": query, "limit": limit, "year": year, "include_text": include_text})
    if not isinstance(res, list):
        raise hs_mcp.McpError(f"unexpected response: {str(res)[:200]}")
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    hs_mcp.add_common_args(ap)
    ap.add_argument("--queries", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--limit", type=int, default=15, help="hits per query")
    ap.add_argument("--tool", choices=["distill_search", "abstract_search", "both"], default="distill_search")
    ap.add_argument("--year", help="e.g. '>=2010'")
    ap.add_argument("--restrict-stems", help="file of stems (one per line) to keep")
    ap.add_argument("--keep-refs", action="store_true", help="keep chunks that look like reference lists (dropped by default)")
    ap.add_argument("--no-text", action="store_true", help="metadata only (smaller ledger)")
    ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ledger, logp, sump = out / "evidence.jsonl", out / "retrieval-log.tsv", out / "evidence-summary.tsv"
    url = hs_mcp.resolve_url(a.url)
    restrict = None
    if a.restrict_stems:
        restrict = {l.strip() for l in Path(a.restrict_stems).read_text().splitlines() if l.strip() and not l.startswith("#")}

    rows, seen = [], set()
    if ledger.exists():
        for l in ledger.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(l)
            except json.JSONDecodeError:
                continue
            rows.append(r)
            seen.add((r["rq"], r["stem"], r["line_start"], r["line_end"]))
    done = set()
    if logp.exists() and not a.force:
        with logp.open(newline="", encoding="utf-8") as f:
            done = {(r["rq"], r["query"], r["tool"]) for r in csv.DictReader(f, delimiter="\t")}

    tools = ["distill_search", "abstract_search"] if a.tool == "both" else [a.tool]
    jobs = [(rq, q, t) for rq, q in read_queries(Path(a.queries)) for t in tools if (rq, q, t) not in done]
    print(f"{len(jobs)} query executions to run", file=sys.stderr)
    fetch = a.limit * (3 if restrict else 1)

    def run(job):
        rq, q, t = job
        try:
            return job, search(url, t, q, fetch, a.year, not a.no_text), ""
        except Exception as e:  # noqa: BLE001
            return job, None, str(e)[:200]

    meta_cache: dict[str, dict] = {}
    new = 0
    with ThreadPoolExecutor(max_workers=a.concurrency) as ex, ledger.open("a", encoding="utf-8") as lf:
        for (rq, q, t), hits, err in ex.map(run, jobs):
            if hits is None:
                print(f"ERROR {rq} {q[:50]!r}: {err}", file=sys.stderr)
                continue
            kept = 0
            for rank, h in enumerate(hits, 1):
                stem = h.get("doc_id") or ""
                if restrict is not None and stem not in restrict:
                    continue
                txt = h.get("chunk_text") or ""
                refs = likely_refs(txt) if t == "distill_search" else False
                if refs and not a.keep_refs:
                    continue
                key = (rq, stem, h.get("line_start"), h.get("line_end"))
                if key in seen:
                    continue
                seen.add(key)
                if kept >= a.limit:
                    break
                kept += 1
                row = {"rq": rq, "query": q, "tool": t, "rank": rank, "stem": stem, "doi": h.get("doi"), "title": h.get("title"),
                       "year": h.get("year"), "score": h.get("score"), "page": h.get("page"), "line_start": h.get("line_start"),
                       "line_end": h.get("line_end"), "likely_refs": refs, "text": txt if not a.no_text else None,
                       "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
                rows.append(row)
                lf.write(json.dumps(row, ensure_ascii=False) + "\n")
                new += 1
            with logp.open("a", encoding="utf-8") as f:
                if logp.stat().st_size == 0:
                    f.write("ts\trq\ttool\tquery\tn_returned\tn_kept\n")
                f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')}\t{rq}\t{t}\t{q}\t{len(hits)}\t{kept}\n")
            print(f"{rq:<6} {t:<15} {q[:60]!r}: {len(hits)} hits, {kept} kept", file=sys.stderr)

    # back-fill missing titles/DOIs (many corpus stems have empty catalog metadata) and rewrite ledger once
    missing = {r["stem"] for r in rows if not r.get("title") or not r.get("doi") or not r.get("meta_source")}
    if missing:
        def meta(stem):
            try:
                with hs_mcp.session(url) as s:
                    return stem, hs_mcp.resolve_meta(s, stem)
            except Exception:  # noqa: BLE001
                return stem, {}
        with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
            for stem, c in ex.map(meta, sorted(missing)):
                meta_cache[stem] = c
        for r in rows:
            c = meta_cache.get(r["stem"])
            if c:
                if not r.get("title") and c.get("title"):
                    r["title"] = c["title"]
                if not r.get("doi") and c.get("doi"):
                    r["doi"] = c["doi"]
                if not r.get("year") and c.get("year"):
                    r["year"] = int(c["year"])
                r["meta_source"] = c.get("source") or "none"
        tmp = ledger.with_suffix(".jsonl.tmp")
        tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        tmp.replace(ledger)

    agg = defaultdict(lambda: {"scores": [], "queries": set(), "title": "", "year": "", "doi": "", "meta_source": ""})
    for r in rows:
        g = agg[(r["rq"], r["stem"])]
        g["meta_source"] = g.get("meta_source") or r.get("meta_source", "")
        g["scores"].append(r.get("score") or 0)
        g["queries"].add(r["query"])
        g["title"] = g["title"] or (r.get("title") or "")
        g["year"] = g["year"] or (r.get("year") or "")
        g["doi"] = g["doi"] or (r.get("doi") or "")
    with sump.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["rq", "stem", "n_hits", "n_queries", "max_score", "mean_score", "year", "doi", "meta_source", "title"])
        for (rq, stem), g in sorted(agg.items(), key=lambda kv: (kv[0][0], -len(kv[1]["queries"]), -max(kv[1]["scores"]))):
            w.writerow([rq, stem, len(g["scores"]), len(g["queries"]), f"{max(g['scores']):.4f}", f"{sum(g['scores']) / len(g['scores']):.4f}",
                        g["year"], g["doi"], g["meta_source"], re.sub(r"\s+", " ", g["title"])])
    print(f"ledger: {len(rows)} rows (+{new} new), {len({s for _, s in agg})} distinct stems -> {ledger}, {sump}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
