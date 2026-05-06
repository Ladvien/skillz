---
name: home-still-bridge
description: "Routing policy that bridges the academic-research skills (deep-research, academic-paper, academic-paper-reviewer, academic-pipeline) with the home-still MCP server. When any academic research workflow needs to discover, read, or cite papers, prefer the local home-still corpus first (distill_search, catalog_*, markdown_read) and fall back to web APIs (paper_search) only to fill gaps — then persist new finds via paper_download so the library grows. Triggers on: research, deep research, literature review, systematic review, meta-analysis, PRISMA, fact-check, write paper, academic paper, revision, peer review, review paper, manuscript review, academic pipeline, research to paper, paper workflow, home-still, hs paper, hs distill, hs scribe."
metadata:
  version: "0.2.0"
  last_updated: "2026-05-06"
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

## Snowballing protocol

Use when an upstream skill needs **recursive citation expansion** from one or more seed papers — i.e. backward chaining (references), forward chaining (citations), pearl growing (semantic neighbors), or bibliographic coupling.

### Technique support in home-still

Everything below uses home-still MCP tools end to end. The bridge does not bypass the MCP with raw web fetch even when an upstream provider would expose more — going around the wrapper breaks the catalog, the integrity gates, and reproducibility. If a capability is missing, the protocol degrades; it does not detour.

| Technique | Description | home-still support |
|---|---|---|
| **Pearl growing** | Semantic expansion from seed terms | ✅ `distill_search` |
| **Backward chaining** | Follow references *out of* a paper | ⚠️ `markdown_read` → LLM parses the References section → `paper_get` / `paper_download` per DOI. Reliability depends on how cleanly scribe converted the bibliography. |
| **Forward chaining** | Find papers that *cite* a paper | ❌ **Not yet available.** `paper_search` is keyword-only across the 6 providers; it does not expose the citation graph. Requires extending home-still with a `paper_citations(doi)` tool wrapping Semantic Scholar Graph API or OpenAlex `cited_by_api_url`. Until then, snowballing operates backward-only. |
| **Bibliographic coupling / co-citation** | Find structural peers via shared references | ❌ **Not yet available.** Requires a `paper_neighbors(doi, mode)` tool wrapping OpenAlex / Semantic Scholar inside home-still. |

### Protocol

1. **Seed selection** — 1–5 papers from `distill_search` or user nomination. Confirm each has a DOI and is converted (`catalog_read`); `scribe_convert` if not. Initialize `visited = {seed DOIs}`.
2. **Per-hop iteration**, for each paper P in the current frontier:
   - **Backward**: `markdown_read(P.stem)` → parse the References section → DOI set B.
   - **Forward**: skipped until home-still gains a `paper_citations` tool (see Roadmap below).
   - For each candidate `C ∈ B` not in `visited`:
     - Resolve via `paper_get(C.doi)` to confirm the DOI is real and capture metadata.
     - Apply inclusion criteria (year, venue tier, language, study type).
     - Score relevance via `distill_search` on C's title + abstract against the seed corpus.
     - If score ≥ threshold and inclusion passes: `paper_download(C.doi)`, add to next frontier and `visited`.
   - Log per-hop metrics: `|added|`, `|examined|`, mean relevance score.
3. **Promote next frontier** to current, repeat until a termination cue fires.

### Hard caps

- Max hops: **2** default, **3** extended (systematic review).
- Max papers added per hop: **50**.
- Max total ingested per run: **200**.

### Termination cues

Stop when **any two of cues 1–5 fire**, or **any one hard cap**.

| # | Cue | Threshold |
|---|---|---|
| 1 | **Theoretical saturation** | Last 10 adds contribute no new theme/code to the synthesis matrix |
| 2 | **Diminishing returns** | Per-hop yield ratio `added / examined` < **10%** |
| 3 | **Citation ring closure** | ≥ **80%** of next-hop candidates are already in `visited` |
| 4 | **Topic drift** | Mean cosine similarity of new adds to seed corpus < **0.55** — cheap to compute because the corpus is vector-indexed (`distill_search`); the unique advantage of having a local semantic index |
| 5 | **Triangulation** | Independent `paper_search` keyword query and snowballing converge on ≥ **70%** the same DOIs |
| 6 | **Hard cap hit** | Any hop / per-hop / total cap above |

For systematic reviews under PRISMA, the cues and thresholds **must be pre-registered** in the protocol (PRISMA-P item 12). Do not adjust thresholds mid-run.

### Integration with upstream skills

- `deep-research` (`systematic-review` mode): snowballing supplements Phase 2 keyword search; counts go in the PRISMA flow diagram under "Records identified through other sources."
- `academic-pipeline`: snowballing runs after the initial bibliography pass and before Stage 2.5 integrity verification. Every snowballed paper still goes through `catalog_read`-based citation gating.
- `academic-paper-reviewer`: snowball one hop backward from a manuscript's reference list to spot-check missed adjacent literature.

### Roadmap: capabilities that need MCP extensions

The following capabilities are deliberately out of scope for the current bridge because the supporting tools do not yet exist on home-still:

- `paper_references(doi)` — structured reference list (replaces the LLM-parses-markdown step; eliminates the conversion-quality dependency).
- `paper_citations(doi, limit, year_from)` — forward citation list (enables forward chaining).
- `paper_neighbors(doi, mode={coupling|co-citation}, limit)` — bibliometric peers.

Each is a thin wrapper around Semantic Scholar Graph API (free, generous rate limits) or OpenAlex (free, requires polite-pool email). When these land in home-still, this protocol's Forward-chaining and Bibliographic-coupling rows flip from ❌ to ✅ with no skill rewrite — just remove the "skipped" line in the iteration step and re-enable the relevant termination cues.

Until then: backward + pearl-growing only. Document this in any PRISMA flow diagram as "Forward citation searching: not performed; tooling unavailable."

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
| Snowball expansion | `markdown_read` (refs) + `paper_get` / `paper_download` per DOI | — (forward chaining requires future `paper_citations` MCP tool) |
