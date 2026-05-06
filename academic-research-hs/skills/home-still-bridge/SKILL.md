---
name: home-still-bridge
description: "Routing policy that bridges the academic-research skills (deep-research, academic-paper, academic-paper-reviewer, academic-pipeline) with the home-still MCP server. When any academic research workflow needs to discover, read, or cite papers, prefer the local home-still corpus first (distill_search, catalog_*, markdown_read) and fall back to web APIs (paper_search) only to fill gaps — then persist new finds via paper_download so the library grows. Triggers on: research, deep research, literature review, systematic review, meta-analysis, PRISMA, fact-check, write paper, academic paper, revision, peer review, review paper, manuscript review, academic pipeline, research to paper, paper workflow, home-still, hs paper, hs distill, hs scribe."
metadata:
  version: "0.1.0"
  last_updated: "2026-04-19"
  status: active
  task_type: policy
  related_skills:
    - deep-research
    - academic-paper
    - academic-paper-reviewer
    - academic-pipeline
---

# home-still bridge

A routing policy, not a pipeline. Whenever `deep-research`, `academic-paper`, `academic-paper-reviewer`, or `academic-pipeline` is active, follow these rules. They change *where material comes from* — never the integrity gates or output formats those skills define.

## Canonical tool priorities

### Discovering papers
1. `mcp__home-still__distill_search` — semantic search over the indexed corpus. Try first.
2. `mcp__home-still__catalog_list` / `mcp__home-still__catalog_recent` — browse existing library metadata when the query is broad or temporal.
3. `mcp__home-still__paper_search` — multi-database search (arXiv, OpenAlex, Semantic Scholar, Europe PMC, CrossRef, CORE) for anything still missing.
4. Only if those fail: web fetch / API-specific search the upstream skill has built in.

### Adding a paper to the library
When a web-discovered paper is worth keeping:
1. `mcp__home-still__paper_download` with DOI (preferred) or URL. Runs on `big`; triggers scribe conversion and distill indexing automatically.
2. Poll `mcp__home-still__distill_status` or check `mcp__home-still__distill_exists` until the stem is indexed (usually minutes; longer if CPU-fallback).
3. Resume the upstream skill's flow using `catalog_read` / `markdown_read` for the new stem.

### Reading papers
- Prefer `mcp__home-still__markdown_read` (clean, layout-corrected markdown) and `mcp__home-still__catalog_read` (metadata) over re-fetching PDFs or HTML.
- Use stems, not file paths. Stems come from `catalog_list` / `catalog_recent` / `paper_search` results.

### Citations and bib data
- Pull DOI, authors, venue, year, and title exclusively from `catalog_read` for anything in the library. This is what keeps `academic-paper`'s and `academic-pipeline`'s integrity-verification stages happy — fabricated refs fail those gates.
- For papers not yet in the library, resolve via `paper_get` (DOI) or `paper_search` *before* you cite them, then run the ingest sequence above.

## Health preflight

Before a long-running skill run (`deep-research` in full mode, any `academic-pipeline` stage, batch `paper_download`):

1. `mcp__home-still__system_status`
2. `mcp__home-still__scribe_health`
3. `mcp__home-still__distill_status`

Warn the user if:
- scribe or distill is unhealthy → `paper_download` will ingest but won't convert/index.
- distill backend is CPU, not CUDA → per home-still's own `CLAUDE.md`, CPU is too slow at corpus scale. Suggest running on the CUDA host (`big`) before proceeding.

## Artifact placement

- **Papers (PDF + markdown) → stay on `big`.** home-still's `paper_download` puts them in `/home/ladvien/home-still/papers/` and `markdown/`. Don't copy them locally.
- **Drafts, outlines, review reports, revision roadmaps, process records → `~/research/<topic-slug>/` on this Mac.** Create the directory on first use. This is where `academic-paper` writes its output and where `academic-paper-reviewer` drops review artifacts.
- Never write generated drafts or reports onto `big`.

## Respect upstream integrity gates

- `academic-pipeline` Stage 2.5 (pre-review) and Stage 4.5 (final) integrity checks are non-skippable. This bridge changes sourcing, not verification.
- Every citation the skills emit must trace back to a real `catalog_read` entry or a verified `paper_get` result. If you can't verify it, don't cite it.
- Data-access levels declared by upstream skills (`raw` / `redacted` / `verified_only`) still govern what that skill can see — the bridge does not override them.

## Quick reference

| Need | First call | Fallback |
|---|---|---|
| Find papers on topic X | `distill_search` | `paper_search` → `paper_download` |
| Browse recent adds | `catalog_recent` | — |
| Read paper by stem | `markdown_read` | `catalog_read` |
| Bib data for citation | `catalog_read` | `paper_get` (DOI) |
| Ingest new paper | `paper_download` | — |
| Confirm ingested | `distill_exists` / `distill_status` | — |
| Health before long run | `system_status` + `scribe_health` + `distill_status` | — |
