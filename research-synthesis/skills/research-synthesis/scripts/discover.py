#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""Discovery: query file -> deduped candidate pool (TSV) + auditable search log.

Subcommands
  search     run a query file against paper_search (and/or the local OpenAlex
             BM25 index) and merge results into the pool
  snowball   backward (references) / forward (citations) chaining from included papers (--from-pool) or a seed file;
             one round per invocation, yield logged to snowball-rounds.tsv; repeat until a round adds no new includes
  validate   seed-set recall check: does the search strategy retrieve papers already known to be relevant?
  corpus     (re)check which pool DOIs are already in the home-still corpus
  abstracts  fetch missing abstracts (paper_get) so screening is not title-only

Query file: one query per line; blank lines and `#` comments ignored. Optional
construct tag: `construct :: query text`. Example:
    sleep restriction :: sleep restriction risk-taking meta-analysis
    habitual short sleepers gambling task performance

Outputs (default dir = --out-dir, e.g. <run>/corpus):
  candidate-pool.tsv   one row per unique work; agent-owned columns (tier,
                       tier_rationale, screen_*, notes) are PRESERVED on re-run
  search-log.tsv       one row per (provider, query[, page]) executed -> PRISMA
                       search-reporting evidence (what, where, when, n hits)
  abstracts.jsonl      {key, doi, title, year, abstract} for screening

search and snowball refuse to run until protocol.py has frozen protocol.md (and while it has unrecorded edits).
Idempotent/resumable: queries already in search-log.tsv (same provider,
query, date filter, page) are skipped unless --force.

Run:  uv run --script discover.py search --queries q.txt --out-dir corpus/
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import threading
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hs_mcp  # noqa: E402

POOL_COLS = [
    "key", "doi", "openalex_id", "title", "year", "first_author", "cited_by", "n_download_urls",
    "providers", "n_queries", "constructs", "queries", "origin",
    "in_catalog", "converted", "embedded", "stem",
    # agent-owned (never overwritten by the script)
    # screening: pass A = screen1_*, independent pass B = screen2_* (screen.py); screen_final = agreed/adjudicated
    "tier", "tier_rationale", "screen1_decision", "screen1_reason", "screen1_conf",
    "screen2_decision", "screen2_reason", "screen2_conf",
    "screen_final", "screen_final_reason", "screen_adjudicator",
    "ft_decision", "ft_reason", "ft_quote", "seed", "notes",
]
AGENT_COLS = POOL_COLS[POOL_COLS.index("tier"):]
LOG_COLS = ["ts", "provider", "query", "construct", "date", "page", "n_returned", "n_new", "error"]
ALL_PROVIDERS = ["all"]  # paper_search's own fan-out over 6 providers
_lock = threading.Lock()


def clean(v) -> str:
    return re.sub(r"[\t\r\n]+", " ", str(v if v is not None else "")).strip()


def norm_title(t: str) -> str:
    t = unicodedata.normalize("NFKD", t or "").lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def key_for(doi: str, title: str) -> str:
    return doi if doi else ("t:" + norm_title(title)[:120])


def read_tsv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, cols: list[str], rows: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: clean(r.get(c, "")) for c in cols})
    tmp.replace(path)


def append_tsv(path: Path, cols: list[str], rows: list[dict]) -> None:
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        if new:
            w.writeheader()
        for r in rows:
            w.writerow({c: clean(r.get(c, "")) for c in cols})


def read_queries(path: Path) -> list[tuple[str, str]]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "::" in line:
            c, q = line.split("::", 1)
            out.append((c.strip(), q.strip()))
        else:
            out.append(("", line))
    return out


class Pool:
    def __init__(self, out_dir: Path):
        self.dir = out_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        self.path = out_dir / "candidate-pool.tsv"
        self.log_path = out_dir / "search-log.tsv"
        self.abs_path = out_dir / "abstracts.jsonl"
        self.rows: dict[str, dict] = {r["key"]: r for r in read_tsv(self.path) if r.get("key")}
        self.abs_seen: set[str] = set()
        if self.abs_path.exists():
            for line in self.abs_path.read_text(encoding="utf-8").splitlines():
                try:
                    self.abs_seen.add(json.loads(line)["key"])
                except Exception:
                    pass

    def add(self, rec: dict, provider: str, query: str, construct: str, origin: str = "search") -> bool:
        """Merge a normalised record. Returns True if the work is new to the pool."""
        doi = hs_mcp.norm_doi(rec.get("doi"))
        title = clean(rec.get("title"))
        if not title and not doi:
            return False
        k = key_for(doi, title)
        # A DOI-less row may later gain a DOI: upgrade it.
        if doi:
            tk = "t:" + norm_title(title)[:120]
            if tk in self.rows and k not in self.rows:
                self.rows[k] = self.rows.pop(tk)
                self.rows[k]["key"] = k
        row = self.rows.get(k)
        is_new = row is None
        if is_new:
            row = {c: "" for c in POOL_COLS}
            row.update(key=k, origin=origin, n_queries="0")
            self.rows[k] = row
        for f in ("doi", "openalex_id", "title", "year", "first_author", "cited_by", "n_download_urls"):
            v = clean(rec.get(f))
            if v and (not row.get(f) or f in ("cited_by", "n_download_urls")):
                row[f] = v
        if provider != "paper_get":  # abstract enrichment is not a search provider
            row["providers"] = "|".join(sorted(set(filter(None, row.get("providers", "").split("|") + [provider]))))
        qs = [q for q in row.get("queries", "").split(" || ") if q]
        if query and query not in qs:
            qs.append(query)
        row["queries"] = " || ".join(qs)
        row["n_queries"] = str(len(qs))
        if construct:
            cs = set(filter(None, row.get("constructs", "").split("|"))) | {construct}
            row["constructs"] = "|".join(sorted(cs))
        abstract = clean(rec.get("abstract"))
        if abstract and k not in self.abs_seen:
            with self.abs_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"key": k, "doi": doi, "title": title, "year": row.get("year"), "abstract": abstract}) + "\n")
            self.abs_seen.add(k)
        return is_new

    def save(self) -> None:
        rows = sorted(self.rows.values(), key=lambda r: (-int(r.get("n_queries") or 0), -int(r.get("cited_by") or 0)))
        write_tsv(self.path, POOL_COLS, rows)

    def done_log_keys(self) -> set[tuple]:
        return {(r["provider"], r["query"], r["date"], r["page"]) for r in read_tsv(self.log_path)}


def norm_paper(p: dict) -> dict:
    authors = p.get("authors") or []
    fa = ""
    if authors:
        a = authors[0]
        fa = a.get("name", "") if isinstance(a, dict) else str(a)
    year = ""
    if p.get("publication_date"):
        year = str(p["publication_date"])[:4]
    elif p.get("year") or p.get("publication_year"):
        year = str(p.get("year") or p.get("publication_year"))
    return {
        "doi": p.get("doi"), "openalex_id": next((v for v in (p.get("openalex_id"), p.get("id")) if v and re.fullmatch(r"W\d+", str(v))), ""), "title": p.get("title"),
        "year": year, "first_author": fa, "cited_by": p.get("cited_by_count") if p.get("cited_by_count") is not None else p.get("citation_count"),
        "n_download_urls": len(p.get("download_urls") or []), "abstract": p.get("abstract_text"),
    }


def run_one(url, provider, construct, query, args, page):
    """Execute one search; returns (provider, construct, query, page, records|None, error)."""
    try:
        with hs_mcp.session(url) as s:
            if provider == "openalex_local":
                res = hs_mcp.call_retry(s, "openalex_search", {
                    "query": query, "max_results": min(args.max_results, 200),
                    "year_from": args.year_from, "min_citations": args.min_citations})
                res = res if isinstance(res, list) else []
            else:
                res = hs_mcp.call_retry(s, "paper_search", {
                    "query": query, "provider": provider, "max_results": args.max_results,
                    "offset": page * args.max_results if page else None, "date": args.date,
                    "min_citations": args.min_citations, "sort": args.sort})
                if isinstance(res, dict):  # tolerate {"results": [...]}
                    res = res.get("results") or res.get("papers") or []
                if not isinstance(res, list):
                    raise hs_mcp.McpError(f"unexpected paper_search response: {str(res)[:200]}")
        return provider, construct, query, page, [norm_paper(p) for p in res], ""
    except Exception as e:  # noqa: BLE001 - log and continue; resume will retry
        return provider, construct, query, page, None, clean(e)[:300]


def protocol_gate(args) -> int:
    """Searching before a frozen protocol (or after a silent edit) is refused: see protocol.py."""
    if getattr(args, "no_protocol_check", False):
        return 0
    import protocol as _p  # noqa: PLC0415
    return _p.check(Path(args.out_dir).resolve().parent)


def cmd_search(args) -> int:
    rc = protocol_gate(args)
    if rc:
        return rc
    out = Path(args.out_dir)
    pool = Pool(out)
    queries = read_queries(Path(args.queries))
    providers = [p.strip() for p in args.providers.split(",") if p.strip()]
    done = set() if args.force else pool.done_log_keys()
    date = args.date or ""
    jobs = []
    for construct, q in queries:
        for prov in providers:
            for page in range(args.pages):
                if (prov, q, date, str(page)) in done:
                    continue
                jobs.append((prov, construct, q, page))
    print(f"{len(queries)} queries x {len(providers)} providers x {args.pages} page(s): {len(jobs)} to run "
          f"({len(queries) * len(providers) * args.pages - len(jobs)} already logged)", file=sys.stderr)
    url = hs_mcp.resolve_url(args.url)
    n_new_total = n_err = 0
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = [ex.submit(run_one, url, p, c, q, args, pg) for (p, c, q, pg) in jobs]
        for i, fut in enumerate(as_completed(futs), 1):
            prov, construct, q, page, recs, err = fut.result()
            n_new = 0
            if recs is not None:
                for r in recs:
                    if pool.add(r, prov, q, construct):
                        n_new += 1
            else:
                n_err += 1
            n_new_total += n_new
            append_tsv(pool.log_path, LOG_COLS, [{
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "provider": prov, "query": q, "construct": construct,
                "date": date, "page": page, "n_returned": len(recs) if recs is not None else "", "n_new": n_new, "error": err}]
                if recs is not None or args.log_errors else [])
            if i % 5 == 0:
                pool.save()
            print(f"[{i}/{len(jobs)}] {prov:<16} {q[:60]!r}: " + (f"ERROR {err}" if err else f"{len(recs)} hits, {n_new} new"), file=sys.stderr)
    pool.save()
    print(f"pool: {len(pool.rows)} unique works (+{n_new_total} new this run, {n_err} failed searches -> rerun to retry) -> {pool.path}")
    if args.check_corpus:
        return cmd_corpus(argparse.Namespace(out_dir=args.out_dir, url=args.url, concurrency=args.concurrency, recheck=False))
    return 0


def cmd_snowball(args) -> int:
    rc = protocol_gate(args)
    if rc:
        return rc
    if not (args.from_pool or args.seeds):
        print("need --from-pool or --seeds", file=sys.stderr)
        return 1
    out = Path(args.out_dir)
    pool = Pool(out)
    if args.from_pool:
        # Wohlin: only papers already judged INCLUDED on the full text may seed the next round [P15 step 3]
        seeds = [r["doi"] for r in pool.rows.values() if r.get("doi") and r.get("ft_decision", "").lower().startswith("incl")]
        if not seeds:
            print("no pool rows with ft_decision=include; full-text-screen the core papers first (Wohlin: decide on the full paper BEFORE using it as a seed)", file=sys.stderr)
            return 1
    else:
        seeds = [hs_mcp.norm_doi(l.split("#")[0]) for l in Path(args.seeds).read_text().splitlines() if l.split("#")[0].strip()]
    url = hs_mcp.resolve_url(args.url)
    dirs = ["backward", "forward"] if args.direction == "both" else [args.direction]
    log_done = set() if args.force else pool.done_log_keys()

    def work(seed, d):
        """S2 first (paper_references/paper_citations); on rate limit wait 30 s once, then fall back to the
        local OpenAlex index (openalex_references/openalex_citations) which has no rate limit."""
        tool = "paper_references" if d == "backward" else "paper_citations"
        a = {"doi": seed}
        if d == "forward":
            a.update(limit=args.limit, sort="citations", year_from=args.year_from)
        try:
            with hs_mcp.session(url) as s:
                for attempt in range(2):
                    try:
                        res = hs_mcp.call_retry(s, tool, a)
                        items = res.get("references" if d == "backward" else "citations", []) if isinstance(res, dict) else []
                        return seed, d, items, ""
                    except hs_mcp.ToolError as e:
                        if "Rate limited" in e.text and attempt == 0:
                            time.sleep(31)
                            continue
                        err = e.text
                        break
                try:  # fallback: local OpenAlex
                    g = s.call("openalex_get", {"id_or_doi": seed})
                    oid = g["openalex_id"]
                    lim = args.limit if d == "forward" else 1000
                    res = s.call("openalex_references" if d == "backward" else "openalex_citations",
                                 {"openalex_id": oid, "limit": lim, **({"year_from": args.year_from} if d == "forward" and args.year_from else {})})
                    items = [{"doi": r.get("doi"), "title": r.get("title"), "year": r.get("publication_year"),
                              "citation_count": r.get("cited_by_count"), "authors": [""]} for r in res]
                    return seed, d, items, ""
                except Exception as e2:  # noqa: BLE001
                    return seed, d, None, clean(f"{err} | openalex fallback: {e2}")[:300]
        except Exception as e:  # noqa: BLE001
            return seed, d, None, clean(e)[:300]

    new_keys: set[str] = set()
    todo = [(s, d) for s in seeds for d in dirs if ("snowball:" + d, s, "", "0") not in log_done]
    print(f"{len(todo)} seed/direction jobs", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        for seed, d, items, err in ex.map(lambda a: work(*a), todo):
            n_new = 0
            if items is not None:
                items = [i for i in items if (i.get("citation_count") or 0) >= args.min_citations]
                for it in items:
                    rec = {"doi": it.get("doi"), "title": it.get("title"), "year": it.get("year"),
                           "first_author": (it.get("authors") or [""])[0], "cited_by": it.get("citation_count")}
                    if pool.add(rec, "snowball:" + d, f"{d} of {seed}", "", origin=f"snowball:{d}:{seed}"):
                        n_new += 1
                        new_keys.add(key_for(hs_mcp.norm_doi(rec.get("doi")), clean(rec.get("title"))))
            append_tsv(pool.log_path, LOG_COLS, [{"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "provider": "snowball:" + d,
                "query": seed, "construct": "", "date": "", "page": 0, "n_returned": len(items) if items is not None else "",
                "n_new": n_new, "error": err}] if items is not None or args.log_errors else [])
            print(f"{d:<8} {seed}: " + (f"ERROR {err}" if err else f"{len(items)} items, {n_new} new"), file=sys.stderr)
    pool.save()
    # yield per round: should fall; stop when a round adds no new INCLUDES [P15 section 4.9, step 3]
    rp = out / "snowball-rounds.tsv"
    rounds = read_tsv(rp)
    append_tsv(rp, ["round", "ts", "direction", "n_seeds", "n_new_candidates", "pool_size", "note"], [{
        "round": len(rounds) + 1, "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "direction": args.direction,
        "n_seeds": len(seeds), "n_new_candidates": sum(1 for r in pool.rows.values() if r.get("origin", "").startswith("snowball") and r["key"] in new_keys),
        "pool_size": len(pool.rows), "note": "screen the new candidates (screen.py), full-text-include, then run the next round with --from-pool; stop at 0 new includes"}])
    print(f"pool: {len(pool.rows)} unique works -> {pool.path}; round {len(rounds) + 1} logged in {rp}")
    return 0


def stem_lookup(url, doi):
    """Return dict(in_catalog, converted, embedded, stem) for a DOI, via catalog_read (authoritative)."""
    try:
        with hs_mcp.session(url) as s:
            for stem in hs_mcp.doi_to_stem_candidates(doi)[:2]:
                try:
                    c = s.call("catalog_read", {"stem": stem})
                except hs_mcp.ToolError:
                    continue
                if isinstance(c, dict):
                    return {"in_catalog": "yes", "stem": stem,
                            "converted": "yes" if c.get("conversion") else "no",
                            "embedded": "yes" if c.get("embedding") else "no"}
            return {"in_catalog": "no", "converted": "", "embedded": "", "stem": ""}
    except Exception:  # noqa: BLE001
        return {"in_catalog": "?", "converted": "", "embedded": "", "stem": ""}


def cmd_corpus(args) -> int:
    pool = Pool(Path(args.out_dir))
    url = hs_mcp.resolve_url(args.url)
    todo = [r for r in pool.rows.values() if r.get("doi") and (args.recheck or r.get("in_catalog") in ("", "?"))]
    print(f"checking {len(todo)} DOIs against catalog", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        for r, res in zip(todo, ex.map(lambda r: stem_lookup(url, r["doi"]), todo)):
            r.update(res)
    pool.save()
    n_in = sum(1 for r in pool.rows.values() if r.get("in_catalog") == "yes")
    n_emb = sum(1 for r in pool.rows.values() if r.get("embedded") == "yes")
    print(f"in corpus: {n_in}/{len(pool.rows)} (embedded/searchable: {n_emb})")
    return 0


def cmd_abstracts(args) -> int:
    """Fill missing abstracts (paper_search often returns abstract_text=null) via paper_get."""
    pool = Pool(Path(args.out_dir))
    url = hs_mcp.resolve_url(args.url)
    todo = [r for r in pool.rows.values() if r.get("doi") and r["key"] not in pool.abs_seen
            and (not args.tiers or r.get("tier") in args.tiers.split(","))]
    if args.max:
        todo = todo[: args.max]
    print(f"fetching abstracts for {len(todo)} works", file=sys.stderr)

    def get(r):
        try:
            with hs_mcp.session(url) as s:
                p = hs_mcp.call_retry(s, "paper_get", {"doi": r["doi"]})
            return r, p if isinstance(p, dict) else {}
        except Exception:  # noqa: BLE001
            return r, {}

    n = 0
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        for r, p in ex.map(get, todo):
            if p.get("abstract_text"):
                pool.add(norm_paper(p) | {"doi": r["doi"], "title": r.get("title") or p.get("title")}, "paper_get", "", "")
                n += 1
    pool.save()
    print(f"abstracts added: {n}/{len(todo)} (rest: none available from providers; screen on title + flag)")
    return 0


def cmd_validate(args) -> int:
    """Seed-set validation of the search strategy: do the searches retrieve papers already known to be relevant?
    (PRISMA 2020 item 7: 'if the search strategy was validated ... report the validation set' [P01]; Siddaway [P18].)
    Seeds file: one DOI (or `title:<text>`) per line. Missing seeds => the strategy lacks a term: add queries, rerun."""
    pool = Pool(Path(args.out_dir))
    by_title = {norm_title(r.get("title", "")): r for r in pool.rows.values()}
    rows, hit = [], 0
    for line in Path(args.seeds).read_text().splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        if line.lower().startswith("title:"):
            r = by_title.get(norm_title(line[6:]))
            ident = line
        else:
            ident = hs_mcp.norm_doi(line)
            r = pool.rows.get(ident)
        if r:
            hit += 1
            r["seed"] = "yes"
        rows.append({"seed": ident, "found": "yes" if r else "NO", "n_queries": (r or {}).get("n_queries", ""),
                     "providers": (r or {}).get("providers", ""), "queries": ((r or {}).get("queries", ""))[:200]})
    write_tsv(Path(args.out_dir) / "search-validation.tsv", ["seed", "found", "n_queries", "providers", "queries"], rows)
    pool.save()
    print(f"seed recall: {hit}/{len(rows)} known-relevant papers retrieved by the search strategy -> search-validation.tsv")
    for r in rows:
        if r["found"] == "NO":
            print(f"  MISSING: {r['seed']}  (derive new search terms from this paper's title/abstract/keywords and rerun)")
    return 0 if hit == len(rows) else 3


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        hs_mcp.add_common_args(p)
        p.add_argument("--out-dir", required=True, help="corpus dir, e.g. slop/research/<run>/corpus")
        p.add_argument("--concurrency", type=int, default=3, help="parallel MCP calls (providers rate-limit; default 3)")
        p.add_argument("--force", action="store_true", help="re-run queries already in search-log.tsv")
        p.add_argument("--no-protocol-check", action="store_true", help="skip the frozen-protocol gate (smoke tests only)")
        p.add_argument("--log-errors", action="store_true", help="also log failed searches (default: failures are retried on rerun)")

    s = sub.add_parser("search", help="run a query file")
    common(s)
    s.add_argument("--queries", required=True)
    s.add_argument("--providers", default="all",
                   help="comma list: all | openalex | semantic_scholar | europmc | crossref | core | arxiv | openalex_local "
                        "(local BM25 index; fast, no rate limit). Default: all")
    s.add_argument("--max-results", type=int, default=25)
    s.add_argument("--pages", type=int, default=1, help="pages per (provider, query) via offset")
    s.add_argument("--date", help="e.g. '>=2005' or '2015-2025' (paper_search syntax)")
    s.add_argument("--year-from", type=int, help="openalex_local only")
    s.add_argument("--min-citations", type=int)
    s.add_argument("--sort", help="relevance|citations|date")
    s.add_argument("--check-corpus", action="store_true", help="afterwards mark which DOIs are already in home-still")
    s.set_defaults(fn=cmd_search)

    b = sub.add_parser("snowball", help="citation chaining from seed DOIs (one per line)")
    common(b)
    b.add_argument("--seeds", help="file of seed DOIs (one per line)")
    b.add_argument("--from-pool", action="store_true", help="seed from pool rows with ft_decision=include (Wohlin: full-text include BEFORE seeding)")
    b.add_argument("--direction", choices=["backward", "forward", "both"], default="both")
    b.add_argument("--limit", type=int, default=100, help="max citing works per seed (forward)")
    b.add_argument("--year-from", type=int)
    b.add_argument("--min-citations", type=int, default=0, help="drop snowballed items cited fewer than N times")
    b.set_defaults(fn=cmd_snowball)

    c = sub.add_parser("corpus", help="mark pool DOIs already in the home-still catalog")
    hs_mcp.add_common_args(c)
    c.add_argument("--out-dir", required=True)
    c.add_argument("--concurrency", type=int, default=4)
    c.add_argument("--recheck", action="store_true", help="recheck rows already resolved")
    c.set_defaults(fn=cmd_corpus)

    v = sub.add_parser("validate", help="seed-set recall check of the search strategy")
    v.add_argument("--out-dir", required=True)
    v.add_argument("--seeds", required=True)
    v.set_defaults(fn=cmd_validate)

    ab = sub.add_parser("abstracts", help="fetch missing abstracts via paper_get")
    hs_mcp.add_common_args(ab)
    ab.add_argument("--out-dir", required=True)
    ab.add_argument("--concurrency", type=int, default=3)
    ab.add_argument("--tiers", help="only rows with these tier values (comma list)")
    ab.add_argument("--max", type=int)
    ab.set_defaults(fn=cmd_abstracts)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
