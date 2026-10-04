#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""Citation audit: check report.md against the home-still catalog and full texts.

Citation convention (see templates/report.md): inline `[@stem]` or `[@stemA; @stemB, p. 4]`, where
`stem` is the home-still catalog stem (DOI with `/` -> `_`, e.g. 10.1016_j.tics.2008.11.006).
The References appendix has one entry per line:
    - [@stem] Author A, Author B (2009). Title. *Venue*. https://doi.org/10.xxxx/yyyy  [abstract-only]

Checks (FAIL = must fix before the report ships; WARN = justify or fix):
  FAIL  cited stem has no catalog entry (fabricated/typo) -- with a hint if the DOI exists in metadata only
  FAIL  reference entry's title/year/DOI does not match the verified record (catalog/OpenAlex/paper note)
  FAIL  stem with NO verified record (empty catalog metadata) whose reference entry nonetheless states a
        title/year/authors -- build entries with refs.py; unresolved stems print stem + UNRESOLVED flag only
  FAIL  cited stem has no line in the References appendix
  FAIL  cited work is retracted (openalex_get.is_retracted)
  FAIL  verbatim quote (>=6 words, "..." or > blockquote) not found in the cited stem's markdown
  FAIL  unresolved template placeholders ({{...}}, TODO, TBD, [CITE])
  FAIL  bare DOI in text that exists neither in catalog nor in provider metadata
  WARN  bare DOI exists in metadata but is not in the corpus (unread: label secondary/abstract-only)
  WARN  cited stem not converted/embedded (abstract-only) and entry not flagged `abstract-only`
  WARN  quantitative claim (d=, r=, OR=, p<, N=, %) with no citation in the same sentence
  WARN  number in a cited sentence not found in any cited stem's text or its paper note
  WARN  quote matches only approximately (>=80% of 5-grams): OCR/hyphenation variation? check by eye
  WARN  cited stem has no notes/papers/<stem>.md (not deep-read)
  WARN  no certainty labels (High/Moderate/Low/Very low) / certainty framework (GRADE, GRADE-CERQual) never named
  WARN  'k of n studies significant' vote-count language; summed numeric quality scores (methodology-synthesis.md 6.2, 1.6)
  WARN  missing: protocol reference, PRISMA statement, AI-use statement, non-equivalence disclosure for LLM dual screening
  WARN  autism-touching topics: no double-empathy rival account, no participatory/autistic-authored sources, no
        co-production limitation, findings not split by informant (methodology-synthesis.md section 7)

Outputs: <report dir>/audit.md and audit.json. Exit status 1 if any FAIL.
Run: uv run --script audit.py --report slop/research/<run>/report.md
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hs_mcp  # noqa: E402
import refmeta  # noqa: E402

CITE_BLOCK = re.compile(r"\[([^\[\]]*?@[^\[\]]*?)\]")
DOI_PAT = re.compile(r"10\.\d{4,9}/[^\s)\]>\"',;]+")
QUANT_PAT = re.compile(
    r"(\b(d|g|r|rho|ρ|β|OR|RR|HR|SMD|SD|t|F|χ2)\s*=\s*[-−]?\d|\bp\s*[<=>≤]\s*0?\.\d|\bN\s*=\s*\d|\bn\s*=\s*\d|\d(\.\d+)?\s*%|95\s*%\s*CI|\bI2\s*=)")
NUM_PAT = re.compile(r"(?<![\w.])[-−]?\d+(?:[.,]\d+)?")
PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}|\bTODO\b|\bTBD\b|\[CITE\]|\[@\?\]|\bXXX\b")
VOTE_PAT = re.compile(r"\b\d+\s+(of|out of)\s+\d+\s+(studies|papers|trials|samples)\b[^.]{0,40}\b(significant|found|showed|reported|supported|confirmed)", re.I)
SUMSCORE_PAT = re.compile(r"\b(quality|appraisal|NOS|CASP|MMAT|risk[- ]of[- ]bias)\s+(score|total|rating)(\s+(of|was|=))?\s*[:=]?\s*\d|\bscored\s+\d+\s*(/|out of)\s*\d+|\b\d+\s*/\s*(9|10|11|14|27)\s+(stars|points|items)", re.I)
GRADE_PAT = re.compile(r"\b(very low|low|moderate|high)\b[^.\n]{0,40}(certainty|confidence)|(certainty|confidence)[^.\n]{0,20}\b(very low|low|moderate|high)\b", re.I)


def norm_text(t: str) -> str:
    t = unicodedata.normalize("NFKD", t).lower()
    t = t.replace("\u00ad", "")
    t = re.sub(r"-\s*\n\s*", "", t)  # hyphenation across line breaks
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def tokens(t: str) -> list[str]:
    return norm_text(t).split()


def parse_cites(text: str) -> list[tuple[str, int]]:
    """[(stem, line_no)] for every [@stem] citation (not in code fences)."""
    out, in_code = [], False
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in CITE_BLOCK.finditer(line):
            for part in m.group(1).split(";"):
                part = part.strip()
                if not part.startswith("@"):
                    continue
                key = re.split(r",\s", part[1:], maxsplit=1)[0].strip()
                if key:
                    out.append((key, i))
    return out


def stem_info(url: str, stem: str, notes_dir: Path) -> dict:
    info = {"stem": stem, "catalog": None, "meta": None, "retracted": None, "hint": ""}
    try:
        with hs_mcp.session(url) as s:
            try:
                c = s.call("catalog_read", {"stem": stem})
                info["catalog"] = c if isinstance(c, dict) else None
            except hs_mcp.ToolError:
                info["catalog"] = None
            if info["catalog"] is not None:
                info["meta"] = refmeta.resolve_reference(s, stem, notes_dir)
            doi = hs_mcp.norm_doi((info["catalog"] or {}).get("doi")) or (info["meta"] or {}).get("doi") or (
                stem.replace("_", "/", 1) if stem.startswith("10.") else "")
            if doi:
                try:
                    g = s.call("openalex_get", {"id_or_doi": doi})
                    if isinstance(g, dict):
                        info["retracted"] = g.get("is_retracted")
                except hs_mcp.ToolError:
                    pass
                if info["catalog"] is None:
                    try:
                        p = s.call("paper_get", {"doi": doi})
                        if isinstance(p, dict) and p.get("title"):
                            info["hint"] = f"DOI {doi} exists in provider metadata ('{p['title'][:70]}') but is NOT ingested; ingest it or drop the claim"
                    except hs_mcp.ToolError:
                        pass
    except Exception as e:  # noqa: BLE001
        info["error"] = str(e)[:200]
    return info


def get_markdown(url: str, stem: str, cache: Path) -> str:
    cache.mkdir(parents=True, exist_ok=True)
    f = cache / (re.sub(r"[^\w.-]", "_", stem) + ".md")
    if f.exists():
        return f.read_text(encoding="utf-8")
    try:
        with hs_mcp.session(url) as s:
            md = s.call_text("markdown_read", {"stem": stem}, timeout=300)
    except Exception:  # noqa: BLE001
        return ""
    f.write_text(md, encoding="utf-8")
    return md


def doi_exists_anywhere(url: str, doi: str) -> tuple[bool, bool]:
    """(in_catalog, in_metadata)"""
    try:
        with hs_mcp.session(url) as s:
            for stem in hs_mcp.doi_to_stem_candidates(doi)[:2]:
                try:
                    s.call("catalog_read", {"stem": stem})
                    return True, True
                except hs_mcp.ToolError:
                    pass
            try:
                p = s.call("paper_get", {"doi": doi})
                return False, isinstance(p, dict) and bool(p.get("title"))
            except hs_mcp.ToolError:
                return False, False
    except Exception:  # noqa: BLE001
        return False, True  # transport trouble: do not accuse


def find_quotes(text: str) -> list[tuple[str, int, set[str]]]:
    """Quoted passages (>=6 words) with the stems cited in their paragraph. [(quote, line_no, stems)]"""
    paras, cur, start = [], [], 1
    for i, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            if cur:
                paras.append((start, "\n".join(cur)))
                cur = []
            continue
        if not cur:
            start = i
        cur.append(line)
    if cur:
        paras.append((start, "\n".join(cur)))
    out = []
    for ln, p in paras:
        stems = {k for k, _ in parse_cites(p)}
        if not stems:
            continue
        for m in re.finditer(r"[\"\u201c]([^\"\u201d\n]{20,600})[\"\u201d]", p):
            if len(m.group(1).split()) >= 6:
                out.append((m.group(1), ln, stems))
        for line in p.splitlines():
            if line.lstrip().startswith(">"):
                q = re.sub(r"\[[^\]]*@[^\]]*\]", "", line.lstrip().lstrip(">").strip())
                if len(q.split()) >= 6:
                    out.append((q, ln, stems))
    return out


def quote_status(quote: str, corpus_norms: list[str]) -> str:
    """'exact' | 'approx' | 'missing' against normalised texts of the cited stems."""
    segs = [s for s in re.split(r"\u2026|\.\.\.|\[\s*\.\.\.\s*\]|\[\u2026\]", quote) if len(s.split()) >= 3]
    segs = [re.sub(r"\[[^\]]*\]", " ", s) for s in segs] or [quote]  # drop editorial [brackets]
    if all(any(norm_text(s) in n for n in corpus_norms) for s in segs):
        return "exact"
    best = 0.0
    for s in segs:
        t = tokens(s)
        grams = {" ".join(t[i:i + 5]) for i in range(max(1, len(t) - 4))}
        if not grams:
            continue
        for n in corpus_norms:
            hit = sum(1 for g in grams if g in n) / len(grams)
            best = max(best, hit)
    return "approx" if best >= 0.8 else "missing"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    hs_mcp.add_common_args(ap)
    ap.add_argument("--report", required=True)
    ap.add_argument("--notes-dir", help="default: <report dir>/notes/papers")
    ap.add_argument("--no-fulltext", action="store_true", help="skip quote/number checks (no markdown_read)")
    ap.add_argument("--concurrency", type=int, default=4)
    a = ap.parse_args()

    rp = Path(a.report)
    raw = rp.read_text(encoding="utf-8")
    # HTML comments (template guidance, REFS markers) are not report content; blank them but keep line numbers
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), raw, flags=re.S)
    notes_dir = Path(a.notes_dir) if a.notes_dir else rp.parent / "notes" / "papers"
    url = hs_mcp.resolve_url(a.url)
    findings: list[dict] = []

    def add(level, code, msg, line=None):
        findings.append({"level": level, "code": code, "msg": msg, "line": line})

    cites = parse_cites(text)
    stems = sorted({k for k, _ in cites})
    first_line = {}
    for k, ln in cites:
        first_line.setdefault(k, ln)

    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        infos = {i["stem"]: i for i in ex.map(lambda s: stem_info(url, s, notes_dir), stems)}

    # reference entries: `- [@stem] ... (Year). Title ... DOI`
    ref_lines: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"^\s*(?:[-*]|\d+\.)\s*\[@([^\]\s;,]+)\]\s*(.+)$", line)
        if m:
            ref_lines[m.group(1)] = m.group(2)

    for stem in stems:
        info, ln = infos[stem], first_line[stem]
        cat = info["catalog"]
        if info.get("error"):
            add("WARN", "lookup-error", f"{stem}: lookup failed ({info['error']}); not verified", ln)
            continue
        if cat is None:
            add("FAIL", "no-catalog-entry", f"[@{stem}] has no home-still catalog entry. {info['hint']}", ln)
            continue
        if info.get("retracted"):
            add("FAIL", "retracted", f"[@{stem}] is marked retracted in OpenAlex", ln)
        converted, embedded = bool(cat.get("conversion")), bool(cat.get("embedding"))
        entry = ref_lines.get(stem)
        if entry is None:
            add("FAIL", "no-reference-entry", f"[@{stem}] is cited but has no line in the References appendix", ln)
        else:
            meta = info["meta"]
            st = meta["status"]
            unresolved_form = "UNRESOLVED" in entry
            if st == "unresolved":
                if not unresolved_form:
                    add("FAIL", "unresolved-metadata-cited", f"[@{stem}] has no verified bibliographic record (catalog/openalex empty) "
                        "yet its reference entry states title/year/authors. Run refs.py, or have a paper-reader verify identity "
                        "and set meta_verified in the paper note", ln)
                else:
                    add("WARN", "unresolved-metadata", f"[@{stem}] cited with UNRESOLVED metadata; resolve before shipping", ln)
            else:
                if st == "document-only":
                    add("WARN", "metadata-document-only", f"[@{stem}] identity read from the paper text only (not provider-confirmed)", ln)
                ct = set(tokens(meta["title"]))
                overlap = len(ct & set(tokens(entry))) / max(1, len(ct))
                if overlap < 0.8:
                    add("FAIL", "title-mismatch", f"[@{stem}] reference entry does not contain the verified title "
                        f"'{meta['title'][:90]}' (token overlap {overlap:.0%})", ln)
                ey = re.search(r"\(\s*((?:19|20)\d\d)[a-z]?\s*\)", entry) or re.search(r"\b((?:19|20)\d\d)\b", entry)
                if meta["year"].isdigit() and ey and abs(int(ey.group(1)) - int(meta["year"])) > 1:
                    add("FAIL", "year-mismatch", f"[@{stem}] entry year {ey.group(1)} vs record {meta['year']}", ln)
                edoi = DOI_PAT.search(entry)
                if meta.get("doi"):
                    if not edoi:
                        add("WARN", "no-doi", f"[@{stem}] reference entry lacks DOI (record: {meta['doi']})", ln)
                    elif hs_mcp.norm_doi(edoi.group(0)) != meta["doi"]:
                        add("FAIL", "doi-mismatch", f"[@{stem}] entry DOI {edoi.group(0)} vs record {meta['doi']}", ln)
        flagged = entry is not None and re.search(r"abstract[- ]only", entry, re.I)
        if not (converted and embedded) and not flagged:
            add("WARN", "abstract-only-unflagged", f"[@{stem}] has no converted+embedded full text; flag it `abstract-only` in References and text", ln)
        if not (notes_dir / f"{stem}.md").exists():
            add("WARN", "no-paper-note", f"[@{stem}] has no {notes_dir}/{stem}.md (not deep-read)", ln)

    for i, line in enumerate(raw.splitlines(), 1):
        for m in PLACEHOLDER.finditer(line):
            add("FAIL", "placeholder", f"unresolved placeholder '{m.group(0)}'", i)
        for m in re.finditer(r"<!--(?!\s*REFS:(BEGIN|END))", line):
            add("WARN", "leftover-comment", "template/guidance HTML comment still present", i)

    # bare DOIs outside [@...] and outside the stems
    bare = {}
    stripped = CITE_BLOCK.sub(" ", text)
    for i, line in enumerate(stripped.splitlines(), 1):
        for m in DOI_PAT.finditer(line):
            bare.setdefault(hs_mcp.norm_doi(m.group(0)), i)
    ref_dois = {hs_mcp.norm_doi((infos[s]["catalog"] or {}).get("doi")) for s in stems}
    bare = {d: ln for d, ln in bare.items() if d not in ref_dois}
    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        for (d, ln), (in_cat, in_meta) in zip(bare.items(), ex.map(lambda d: doi_exists_anywhere(url, d), bare)):
            if in_cat:
                add("WARN", "bare-doi-in-corpus", f"DOI {d} is in the corpus but cited without [@stem]", ln)
            elif in_meta:
                add("WARN", "bare-doi-not-ingested", f"DOI {d} exists in metadata but is not in the corpus (label secondary/abstract-only)", ln)
            else:
                add("FAIL", "bare-doi-not-found", f"DOI {d} not found in catalog or provider metadata (fabricated?)", ln)

    # quantitative claims
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(("```", "#")) or re.match(r"^\s*[-*]?\s*\[@", line):
            continue
        for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z(\[])", line):
            if QUANT_PAT.search(sent) and "@" not in sent:
                add("WARN", "uncited-quantity", f"quantitative claim without citation: '{sent.strip()[:110]}'", i)

    # full-text checks
    if not a.no_fulltext and stems:
        cache = rp.parent / ".audit-cache"
        ok = [s for s in stems if infos[s]["catalog"] and infos[s]["catalog"].get("conversion")]
        with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
            mds = dict(zip(ok, ex.map(lambda s: get_markdown(url, s, cache), ok)))
        norms = {s: norm_text(md) for s, md in mds.items()}
        for s in ok:
            nf = notes_dir / f"{s}.md"
            if nf.exists():
                norms[s] = norms.get(s, "") + " " + norm_text(nf.read_text(encoding="utf-8"))
        for quote, ln, qstems in find_quotes(text):
            pool = [norms[s] for s in qstems if s in norms and norms[s]]
            if not pool:
                add("WARN", "quote-unverifiable", f"quote '{quote[:70]}...' cites no full-text stem", ln)
                continue
            st = quote_status(quote, pool)
            if st == "missing":
                add("FAIL", "quote-not-found", f"quote not found in cited text(s) {sorted(qstems)}: '{quote[:90]}...'", ln)
            elif st == "approx":
                add("WARN", "quote-approx", f"quote only approximately matches (OCR/hyphenation?): '{quote[:90]}...'", ln)
        for i, line in enumerate(text.splitlines(), 1):
            for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z(\[])", line):
                ss = {k for k, _ in parse_cites(sent)}
                if not ss or not QUANT_PAT.search(sent):
                    continue
                pool = " ".join(norms.get(s, "") for s in ss)
                if not pool.strip():
                    continue
                nums = [n.replace("\u2212", "-").lstrip("-") for n in NUM_PAT.findall(CITE_BLOCK.sub(" ", sent))]
                nums = [n for n in nums if len(n) >= 3 or "." in n]  # skip bare 1-2 digit counts
                missing = [n for n in nums if norm_text(n) not in pool and norm_text(n.lstrip("0")) not in pool]
                if missing:
                    add("WARN", "number-not-in-source", f"{missing} not found in cited stem text/note: '{sent.strip()[:100]}'", i)

    body_text = text
    if not GRADE_PAT.search(body_text):
        add("WARN", "no-certainty-labels", "no certainty/confidence labels (High/Moderate/Low/Very low) found")
    if not re.search(r"GRADE|CERQual", body_text):
        add("WARN", "no-certainty-framework", "report never names the certainty framework (GRADE for effect findings, GRADE-CERQual for qualitative/interpretive findings)")
    for i, line in enumerate(body_text.splitlines(), 1):
        if VOTE_PAT.search(line):
            add("WARN", "vote-counting", f"'k of n studies' tally: show k, N, effect sizes/direction and say which question it answers; never rank by significance count: '{line.strip()[:90]}'", i)
        if SUMSCORE_PAT.search(line):
            add("WARN", "summed-quality-score", f"summed/numeric quality score used; appraisal is domain-level judgement, no total score: '{line.strip()[:90]}'", i)
    required = [
        (r"protocol", "no-protocol-reference", "report does not reference the frozen protocol / amendments"),
        (r"PRISMA", "no-prisma", "no PRISMA 2020 / PRISMA-S / PRISMA-ScR reporting statement or flow"),
        (r"\b(AI|LLM|language model|agent)s?\b[^\n]{0,160}\b(screen|extract|synthes|appraisal)", "no-ai-use-statement",
         "no statement of how AI agents were used for screening/extraction/synthesis (tool/model, prompts, validation, oversight)"),
        (r"(not (shown|validated|demonstrated) to be equivalent|non-equivalent|not equivalent|not a substitute)[^\n]{0,120}", "no-dual-screen-disclosure",
         "no disclosure that two independent LLM screening passes are not equivalent to two human screeners"),
    ]
    for pat, code, msg in required:
        if not re.search(pat, body_text, re.I):
            add("WARN", code, msg)
    if len(re.findall(r"autis", body_text, re.I)) >= 3:
        for pat, code, msg in [
            (r"double[- ]empathy", "autism-no-double-empathy", "autism topic: double-empathy / interactional account not carried as a named competing theory"),
            (r"participat|co-?produc|community priorit|autistic (scholar|author|perspective|voices?)", "autism-no-participatory", "autism topic: no autistic-authored / participatory-research sources or perspectives discussed"),
            (r"co-?production|without (autistic|community)|not co-?produced|no autistic (involvement|co-)", "autism-no-coproduction-note", "autism topic: no limitation statement about missing community co-production"),
            (r"informant|self-report|who is speaking|observer|parent report", "autism-no-informant", "autism topic: findings not separated by informant (autistic self-report / family / clinician / task)"),
        ]:
            if not re.search(pat, body_text, re.I):
                add("WARN", code, msg)

    nfail = sum(1 for f in findings if f["level"] == "FAIL")
    nwarn = sum(1 for f in findings if f["level"] == "WARN")
    summary = {"report": str(rp), "cited_stems": len(stems), "fail": nfail, "warn": nwarn,
               "verified_in_catalog": sum(1 for s in stems if infos[s]["catalog"])}
    (rp.parent / "audit.json").write_text(json.dumps({"summary": summary, "findings": findings}, indent=1, ensure_ascii=False), encoding="utf-8")
    lines = [f"# Citation audit: {rp.name}", "", f"- cited stems: {len(stems)} (in catalog: {summary['verified_in_catalog']})",
             f"- **FAIL: {nfail}**, WARN: {nwarn}", ""]
    for lvl in ("FAIL", "WARN"):
        fs = [f for f in findings if f["level"] == lvl]
        if fs:
            lines += [f"## {lvl}", ""] + [f"- L{f['line'] or '?'} `{f['code']}`: {f['msg']}" for f in fs] + [""]
    (rp.parent / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main())
