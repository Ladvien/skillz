---
name: research-synthesis
description: Research, synthesize, or survey the literature on a high-level topic or folk question (e.g. "research the link between chronic sleep loss and risky decision-making", "synthesize what is known about X", "do a literature survey on Y"). Drives the home-still academic pipeline (MCP server `home-still` / `hs` CLI) end to end as a scoping/mapping review with systematic search - frozen protocol, premise-check, seed-validated logged search with citation snowballing, two-pass screening with kappa, download/convert/index, evidence-anchored deep reading, appraisal by design, named synthesis methods, GRADE / GRADE-CERQual certainty per finding, an insight layer, and a PRISMA-style cited report with a blocking citation audit. Use when the user wants a thorough, source-grounded literature review rather than a quick answer.
---

# research-synthesis

Turn a vague topic into a cited, audited, insight-bearing meta-survey using the user's home-still corpus
(search -> download -> convert -> embed -> semantic search). Everything for one run lives in
`slop/research/<YYYY-MM-DD>-<slug>/`. Nothing outside that directory (and this skill) is modified.

```
SK="${CLAUDE_SKILL_DIR}"                      # this skill's directory (Claude Code expands the variable; in another harness set SK to the directory this SKILL.md was loaded from)
S="uv run --script $SK/scripts"                # scripts carry PEP 723 deps; the repo pyproject is untouched
```

## Evidence base for this skill

The process is not invented: each phase implements practices that were found, acquired and read **through home-still itself** and are cited by key.
- `reference/methodology-process.md` - keys **[Pxx]**: question framing, protocol, search/PRISMA-S, snowballing, screening, extraction, reporting, rapid/living, LLM safeguards. Source table in its §10 (DOI + home-still stem + read-status).
- `reference/methodology-synthesis.md` - keys **[Sxx]**: appraisal by design, synthesis-method choice, SWiM / thematic / best-fit / meta-ethnography / CIS / realist steps, GRADE / GRADE-CERQual, insight generation, hazards, autism/neurodiversity participatory practice. Source table in its §9.
- `reference/home-still-interfaces.md` - exact tool names, args, response shapes, `hs` CLI.
Read-status matters: **FT** = full text read; **AB** = only the abstract was obtainable (paywalled) - a practice marked AB below is stated only as far as the abstract states it, and the skill never reconstructs item lists of AB/NA tools from memory (RoB-E, AXIS, QUADAS-2 details, MMAT, JBI checklists, PRESS elements are the main cases). `[INFERENCE]` marks a mapping the reference authors made themselves (e.g. applying scoping review to a "meta-survey", or two LLM passes standing in for two human screeners). Where this skill and a source disagree, the source wins.

## Hard rules

1. **Never cite from memory.** Every claim, number and quote traces to a paper note or a retrieved chunk of a paper that is in home-still. Citations are `[@stem]` (stem = DOI with `/` -> `_`). A citation enters the report only if it resolves to a `catalog_read` / `openalex_get` / provider record with title, authors, year and DOI matched; remembered references are leads, never evidence. Fabricated-reference rates of 8-33% DOI accuracy and ~20% fabricated citations were measured for un-grounded chatbots [P26 AB, P27 AB]; grounding should lower the risk but is not shown to remove it, so `audit.py` is blocking.
2. **Test the premise, do not assume it.** The folk premise is a hypothesis; search for disconfirming evidence, stigma/stereotype critiques and first-person perspectives on purpose; carry at least two rival theories to the end [S07, S11, S64].
3. **Never print a citation built from an empty or unresolved record.** ~70% of corpus stems (OpenAlex `W...`, PubMed ids, hash names) have EMPTY title/doi in `catalog_read`, and one stem is known whose catalog title belongs to a different paper [S §6.7]. Resolution: catalog -> `openalex_get` -> paper-reader confirms identity from page 1 **and** a provider title search. Otherwise it prints as `UNRESOLVED METADATA` (`refs.py`; `audit.py` fails guessed entries).
4. **Count studies, not stems.** One work can exist under several stems; one paper yields many chunks. De-duplicate before counting convergence.
5. **Never touch `personal_*` tools** (private medical/financial records).
6. **Do not mutate home-still beyond download/convert/index of papers you need.** No `catalog_repair`, `catalog_backfill_title`, `distill_backfill` with `dry_run=false`, no service restarts, no config edits.
7. **Quote-or-null.** Extracted values carry a verbatim quote + page; unstated values are `null`. LLM extraction confabulated ~4% of data points even as a second extractor [P41 AB]. Appraisal judgements carry a quote or `NI`.
8. **No summed quality scores; no vote-counting by significance; no causal verbs without the causal-wording gate** (protocol section 10) [S25, S05, S27, S71, S01, S20, S30].
9. State uncertainty; label each insight `evidence-derived`, `inference` or `speculation`.

## Run layout (created by `init_run.py`)

```
slop/research/<date>-<slug>/
  protocol.md protocol.sha256.json  scope.md      phase 1 (frozen before the first external search)
  queries/    seeds-known.txt search.txt rq.txt
  corpus/     candidate-pool.tsv search-log.tsv search-validation.tsv snowball-rounds.tsv abstracts.jsonl
              screening-stats.json screening-disagreements.tsv recall-audit.tsv
              acquisition.tsv acquired.tsv paywalled.tsv unconvertible.tsv pending.tsv abstract-only.tsv
  evidence/   evidence.jsonl retrieval-log.tsv evidence-summary.tsv
  notes/      papers/<stem>.md   verification.tsv
  synthesis/  logic-model.md construct-ledger.md evidence-matrix.md certainty.md insights.md ai-use-log.md unresolved-stems.tsv
  flow-counts.json flow.mmd  report.md audit.md audit.json
```

## Phase 0 - Preflight

```bash
$S/init_run.py "<topic as the user said it>"        # prints the run dir; export RUN=<it>
```
Check `system_status`, `scribe_health`, `distill_status` (MCP tools). Note `in_flight_conversions` and `vlm_slots_available`; if conversions are already in flight (another batch, watcher backlog) acquisition will be slow - do not add load.
Server URL resolution for scripts: `--url` > `$HS_MCP_URL` > `~/.omp/agent/mcp.json` > `~/.claude.json`/`.mcp.json` home-still entry that has a `url`. If none resolves, the script exits and asks for `$HS_MCP_URL` (there is no built-in default). A Claude Code MCP entry may be a stdio bridge to a gateway; the scripts need a direct streamable-HTTP endpoint, so they typically need network access to the home-still host.
**Exit:** run dir exists; server reachable; backlog noted.

## Phase 1 - Scope, framing, protocol draft

**Method basis.** *Review type*: choose by purpose [P11 Munn: scoping for identifying types of evidence, clarifying concepts, examining how research is conducted, key characteristics, gaps; systematic for a precise, critically appraised answer]. A "meta-survey of a high-level topic" maps to a **scoping/mapping review conducted with systematic search methods** [P09, P10, P08; the mapping is an INFERENCE]. Justify it per run; if the user's purpose is one precise association, say a systematic review of that sub-question fits better. *Question framework*: broad question + clearly articulated scope [P10], stated as **PCC** (population, concept, context) [P08 items 4-5]; SPIDER for qualitative sub-questions [P14 AB]; PEO for exposure-outcome sub-questions [S26]. *Logic*: classify every RQ as aggregative (how strong, how certain) or configurative (why/how/for whom) before searching [S16, S19]; most real reviews need both. *User checkpoint* replaces stakeholder consultation, which the scoping literature calls essential [P10]; ask the user only if the purpose is ambiguous [INFERENCE].

Artifacts: `scope.md` (from `templates/scope.md`), `protocol.md` (from `templates/protocol.md`).
1. Restate the question; list its hidden premises as falsifiable claims and what each looks like if false.
2. Translate everyday words into constructs; PCC concept map with synonyms [P18]. Example, for "link between chronic sleep loss and risky decision-making": sleep restriction vs total deprivation vs habitual short sleep; circadian misalignment and shift work; impulsivity and delay discounting; risk preference and loss aversion (laboratory gambling tasks vs real-world risk); executive function and working memory; mood and emotion regulation; stimulant use (caffeine) and recovery sleep; individual differences in vulnerability. Include a construct that would *refute* the premise (e.g. reverse direction: a risk-taking temperament that drives short sleep).
3. Research questions with type and logic; eligibility independent of what studies exist [P18]; adjacent fields; confounder list **before extraction** [S24].
4. If the topic touches autistic people, apply the participatory/neurodiversity checklist (protocol section 13) from the start [S31-S37].
5. Draft `protocol.md` fully (review type, PCC, logic and planned synthesis per RQ, eligibility, sources, seed set, search validation, snowball rules, screening process, extraction, appraisal tool table, synthesis, certainty, insight procedure, AI-use/oversight checkpoints). All TODOs must be filled; defaults in the template are the spine.
**Exit:** `scope.md` has >=3 RQs with type+logic, a concept map, an explicit premise check; `protocol.md` has no TODO left (freeze happens at the end of Phase 2).

## Phase 2 - Existing corpus, seed set, and freezing the protocol

The corpus may already hold documents from earlier projects, a mix of unrelated topics.
```bash
# queries/rq.txt: `RQ1 :: query` lines (several paraphrases per RQ)
$S/retrieve.py --queries $RUN/queries/rq.txt --out-dir $RUN/evidence --tool both --limit 15
```
Read `evidence-summary.tsv`; corpus hits are candidates, not evidence. Record what the corpus covers and misses. Build the **seed set** (>=5 known-relevant papers from the corpus and from the user; diverse authors, years, venues; not authorially clustered [P15]) into `queries/seeds-known.txt` (one DOI or `title:<text>` per line) and list it in the protocol [P01 item 7; P18].
Then freeze:
```bash
$S/protocol.py freeze --run $RUN --by "<agent/session>"   # refuses while TODO remains; writes version, time, SHA-256
```
Practice: a protocol is fixed **before searching** so deviations and selective reporting are detectable; later changes are identified amendments with date, reason and effect, and the updated protocol gets a new version [P05, P06 item 4, P01 items 24a-c]. No registry exists for agent runs - the hash is the substitute record [INFERENCE]. `discover.py search|snowball` refuse to run on an unfrozen protocol or one with unrecorded edits. To change it later: edit `protocol.md`, then `protocol.py amend --run $RUN --change ... --reason ... --effect ...`.
**Exit:** corpus coverage written down; >=5 seeds; protocol frozen (v1).

## Phase 3 - Discovery

**Method basis.** >=2 sources; strategy developed from seed papers and **validated by recall of the seeds**; err toward sensitivity at search stage; full strategies, dates and counts reported; publish both published and unpublished work [P01 item 7, P04 PRISMA-S, P18, P17 rec 5]. Citation chasing complements database search and is run on **included** papers to saturation [P15]. Strategy peer review (PRESS) presumes a human information specialist; a second agent audits the query matrix against the elements named in the abstract [P19 AB; INFERENCE].

Build `queries/search.txt`: constructs x population x method terms, optional `construct :: query`, dozens of queries (typically 40-120). Vary vocabulary (older/newer/colloquial synonyms for every construct, e.g. "short sleep", "sleep restriction", "insufficient sleep"); include premise-disconfirming and critical queries ("stereotype", "bias", "null result", "replication", "qualitative lived experience", and the studied group's own perspective where relevant; for autism topics add e.g. "double empathy", "neurodiversity", "autistic perspectives"); method terms ("meta-analysis", "systematic review", "ERP", "experience sampling"). A second agent reviews the matrix for translation of question to concepts, operators, per-provider adaptation, typos and missed terms; changes are logged.
```bash
$S/discover.py search --queries $RUN/queries/search.txt --out-dir $RUN/corpus --providers all,openalex_local --max-results 25 --check-corpus
$S/discover.py validate --out-dir $RUN/corpus --seeds $RUN/queries/seeds-known.txt   # must reach full seed recall; add terms derived from missing seeds and rerun
$S/discover.py abstracts --out-dir $RUN/corpus          # abstracts are often null in search results
```
Behaviour: DOI-deduped; queries already in `search-log.tsv` are skipped (`--force` to rerun); agent-owned columns (tier, screening, ft_*) survive reruns; failed searches are not logged so a rerun retries them. `openalex_local` is BM25 (short 2-4 term queries; long queries return 0-4 hits); `--providers all` returns ~9-10 of 10 requested; its `id` is sometimes a DOI; some rows have no DOI (keyed by title). `paper_search` offers no Boolean/subject-heading control - report that as a limit.

### Screening (title/abstract) - two independent agent passes
**Method basis.** Pilot on 50-100 records assessed by all screeners, then revise [P17]; dual independent screening with kappa and a stated disagreement rule [P18, P01 item 8]; err toward inclusion [P18]; reason for every exclusion [P01 item 16b]; kappa and prevalence-adjusted kappa together because class imbalance distorts both [P38 AB, P39 AB]. **Disclosure (goes in the report):** two LLM passes are *not shown* to be equivalent to two human screeners - the sources report LLM screening accuracy inflated by class imbalance and unreliable in balanced sets [P38 AB, P39 AB]; single-reviewer screening missed ~13% of relevant studies [P28 AB]; human abstract-screening error is ~10.8% [P29]. Compensating controls below. The 20% dual-screen / kappa >= 0.8 gate for switching to single-pass is expert opinion [P17] and only applies in declared rapid mode.
```bash
$S/screen.py export --pool $RUN/corpus/candidate-pool.tsv --pass A --out $RUN/corpus/pilot-A.jsonl --pilot   # 75 random records
# two subagents (A and B), different prompt wording / model, no shared state, each reads its batch + the eligibility criteria and
# writes decisions jsonl: {"key","decision":"include|exclude|unsure","reason":"<code: text>","confidence":0-1}
$S/screen.py ingest --pool $RUN/corpus/candidate-pool.tsv --pass A --decisions $RUN/corpus/decisions-A.jsonl   # same for B
$S/screen.py stats --pool $RUN/corpus/candidate-pool.tsv --audit-n 25      # raw agreement, Cohen's kappa, PABAK, disagreements, recall-audit sample
```
Revise criteria/prompts after the pilot, then export the rest (no `--pilot`), ingest both passes, `stats`. Resolve disagreements with a third pass that sees both rationales (or the user): `screen.py adjudicate --key K --decision ... --reason ... --by ...`; then `screen.py finalize`. **Recall audit:** re-read `recall-audit.tsv` (random sample of records both passes excluded), fill `audit_verdict`; a wrongly excluded record means revise the criteria and redo the sift [P18]; checkpoints are audits of samples with thresholds, not blanket approval [P25].
**Relevance tiers** (`tier` + mandatory `tier_rationale`): `core` answers an RQ directly; `adjacent` gives mechanism/construct evidence from neighbouring fields; `background` is theory, methods, critique. Autistic-authored and community-priority sources are labelled and kept, not dropped as grey literature [S31, S32, S37].

### Citation chasing (Wohlin snowballing to saturation)
**Method basis** [P15 FT]: seed only from papers **already judged included on the full text**; one round at a time; backward (references) and forward (citations), judging by title/venue/author and citation context; track yield per round (should fall; if not, re-search with synonyms); **stop when a round adds no new includes**; log base articles, direction, platform, date [P04 item 5]. Evidence that snowballing beats database search is the author's hypothesis, not a finding; the supporting literature on citation chasing is AB-only [P23a-f]. Data sources here are Semantic Scholar/OpenAlex, not Google Scholar [P23d AB].
```bash
# after full-text screening sets ft_decision=include for some core papers (Phase 6 notes)
$S/discover.py snowball --out-dir $RUN/corpus --from-pool --direction both --min-citations 10   # one round; yield -> snowball-rounds.tsv
# screen the new candidates (screen.py, two passes), full-text-include them, then run the next round; stop at 0 new includes
```
S2 rate-limits `paper_references/citations`; the script waits 31 s once, then falls back to local OpenAlex. (`--seeds file` exists for the first round before any full-text includes.)
**Exit:** pool tiered with rationale; seed recall reported; `screening-stats.json` + audit done; >=1 snowball round run on full-text includes (further rounds until yield 0, or the stopping rationale written); `search-log.tsv` complete; disconfirming/critical queries represented.

## Phase 4 - Acquisition (download -> convert -> index)

```bash
$S/acquire.py --pool $RUN/corpus/candidate-pool.tsv --tiers core,adjacent --out-dir $RUN/corpus --concurrency 2
```
Run long batches in the background and read `acquisition.tsv`; do not poll in a loop. Resumable: terminal rows (acquired / paywalled / unconvertible) are skipped; `--retry paywalled` to override (one retry is worthwhile before declaring paywalled: 4 BMJ papers failed once and then downloaded [S §6.7]); `--status-only` verifies without side effects; `--max-papers N` stages. Records excluded by screening (`screen_final` / `ft_decision` = exclude) are skipped.

### Operational hazards (embedded - this skill is self-contained)
- **30 s MCP client timeout cancels server-side `scribe_convert`.** Harness MCP tools are fine for search/read, NOT for converting PDFs (HTML converts in <1 s; PDFs take 3.5-6 min under load). The scripts speak raw streamable-HTTP JSON-RPC with a 1800 s timeout.
- **Open each MCP session inside the concurrency slot** (the server keeps per-`initialize` state). `acquire.py` does this.
- **Right-size concurrency to the backend's real VLM slots.** `vlm_slots_total` is declared, not necessarily served; oversubscription -> `502 Bad Gateway` retries and stalled conversions (`in_flight_conversions` > backend slots is the signature). Default 2; capped by `vlm_slots_available`; sibling runs share the backend, so keep <= 2.
- **Killing a client does NOT cancel server conversions** (no cancel RPC); orphans stack on the single backend. Never restart-storm: resume once; `convert_pending_verify` rows are reconverted only when `scribe_health` shows nothing in flight. No service restarts or config edits from a research run.
- **Server deadline** `convert_deadline_secs` defaults to 900 s; a PDF dying at ~900 s with `Conversion failed: Stream read error` hit it (the event watcher uses a page-scaled deadline). Report as `transient`; raising it is an operator action.
- **Verify from the catalog, not the filesystem.** The S3-backed NFS mount returns stale negative lookups. Truth = `catalog_read` (`conversion`, `embedding` blocks) + `distill_exists`. A client-side "failed" convert can be fully converted and embedded.
- **Classify failures:** `paywalled` (`No open-access PDF found...`; first checked for an alternate stem already in the corpus), `transient` (timeouts/5xx/rate limits/server deadline), `unconvertible` (anti-bot gate pages - "Article Locator Bypass", "Checking your browser", Cloudflare, OSF/OSV SPA shells, abstract-only HTML stubs, `0 non-whitespace chars`; the script also sniffs converted markdown). "Full text not retrievable" is recorded separately from ineligibility (PRISMA 'reports not retrieved') [P01].
- **Do not use `hs scribe convert --out`**: no catalog row, no event, invisible to search. Use MCP `scribe_convert` (what the script does). Downloads publish `papers.ingested` and the watcher converts FIFO behind any backlog; `scribe_convert` bypasses the queue; embedding then happens via event-watch (the script waits `--embed-wait`, then calls `distill_index`).
- A converted gate page can already be embedded and pollute search; `unconvertible` rows are excluded from evidence. `distill_scan_repetitions`/purge are operator tools (report, do not fix).

### Paywalled / unconvertible but important
Core-tier failures are kept as **abstract-only evidence**: `corpus/abstract-only.tsv` carries the abstract; mark every use `(abstract-only)`; extract no effect sizes from an abstract you have not seen in full; list them in Limitations; claim only what the abstract states (the same discipline the reference applies to its own AB sources).
**Exit:** every core/adjacent row terminal or explicitly deferred; counts reported.

## Phase 5 - Retrieval (evidence ledger)

Per RQ write 4-10 differently worded queries (population, construct, method wording; **plus a dedicated counter-evidence query set** with negated/alternative framing for every major expected finding [S §8 item 8]).
```bash
$S/retrieve.py --queries $RUN/queries/rq.txt --out-dir $RUN/evidence --tool both --limit 15 \
    --restrict-stems <(awk -F'\t' '$4=="acquired"{print $2}' $RUN/corpus/acquisition.tsv)
```
Ledger rows: rq, query, tool, rank, stem, doi, title, year, score, page, line_start, line_end, likely_refs, meta_source, text. `distill_search` = chunk level (quotable); `abstract_search` = one point per paper. Reference-list chunks are dropped by default. `evidence-summary.tsv` ranks papers per RQ by distinct queries hit - a reading list, not a quality ranking. `meta_source=markdown_head|none` = identity unverified.
**Exit:** every RQ has >=4 queries and a ranked list; zero-hit RQs and "no counter-evidence found + queries tried" are recorded as findings.

## Phase 6 - Deep reading: full-text screening, extraction, appraisal (parallel subagents)

**Method basis.** *Extraction*: fixed schema piloted on 2 papers [P17 rec 10-12]; **one extracts, a second verifies**; extraction errors reach up to 50% [P20]; single extraction made 21.7% more errors than double [P21 AB]; for LLM extraction use quote-or-null because ~4% of data points were confabulated and review-specific/numeric fields were weakest [P41 AB, P40 AB, P43 AB]. *Full-text screening*: reason for every exclusion, with quote [P01 item 16b, P18]. *Appraisal*: tool chosen by **design**, domain-level judgements with supporting quote or NI, **per finding**, **no summed score**, relevant-but-weak evidence kept and tested by sensitivity analysis [S23, S24, S25, S02, S08-S10, S27, S71]. Table of tools and their read-status: `protocol.md` section 9 (RoB 2, ROBINS-I, NOS, AMSTAR 2, CASP-style/CIS prompts/CERQual limitations, ...; ROBINS-E, AXIS, QUADAS-2 details, MMAT and JBI items are AB/not read -> `partial-coding`).

Read every `core` paper (and `adjacent` papers central to a mechanism) in full. One `paper-reader` subagent (`research-synthesis:paper-reader` when this skill is installed as a plugin; definition in `agents/paper-reader.md`) per paper or small batch; give each: stem, RQ list, run dir, the inclusion criteria, and the path `$SK` (it reads `$SK/reference/` and `$SK/templates/`). It writes `notes/papers/<stem>.md` (template: identity, design/sample, construct ledger with informant, findings with quote+page, author interpretations vs data, limitations, per-finding appraisal, mechanism/theory material, stance) and sets `ft_decision` guidance in its reply (include/exclude + reason); the main agent writes `ft_decision`, `ft_reason`, `ft_quote` into the pool. Run 4-8 readers concurrently. A second pass independently re-screens every borderline/excluded full text.
```bash
$S/verify_notes.py --run $RUN        # every quote exists in the paper (and on the cited page); no value without a quote; exit 1 on FAIL
```
Spot-check 10-20% of notes by hand (re-read the source passage and compare numbers); any extraction error means re-verifying that reader's whole batch.
**Exit:** one note per core paper; `verify_notes.py` 0 FAIL; every note has identity status; appraisal per finding without totals; `ft_decision` recorded for every full text read; abstract-only items flagged.

## Phase 7 - Synthesis

**Method basis** [S §0, §2, §3, §4, §5]. Work in `synthesis/` before prose.
1. **Logic model** (`logic-model.md`): the assumed pathway, moderators and population written **before** reading results, revised on evidence [S01 item 1; Popay element 1 via S17; Popay 2006 itself was not obtainable].
2. **Streams and methods.** Split studies by design. Aggregative questions: SWiM-reported narrative synthesis, tabulated by design/N/population/measure/direction/effect/appraisal [S01]; meta-analysis only if constructs, designs and effects are commensurable [S27, S38 AB]. Configurative questions: thematic synthesis (codes -> descriptive -> analytical themes) [S08]; best-fit framework synthesis when an adequate model exists [S09, S10]; **CIS** when the concept is contested and the field's framing is the object of critique [S02]; **realist CMO** for mechanism claims [S11]; meta-ethnography only for <=~40-50 well-defined qualitative studies [S12-S14]; meta-narrative when research traditions conceptualise the topic differently [S48]. Name the method per stream in the report and fill the **nine SWiM items** for each quantitative synthesis [S01].
3. **Construct ledger** (`construct-ledger.md`): operational measure x population x informant for every key construct; pool only within a ledger group and say so [S01 item 1a, S07, S26; S §6.4 is partly INFERENCE]. For autism topics split by informant (autistic self-report / family / clinician-observer / task) before combining [S §7].
4. **Convergence/divergence** per RQ; effect sizes as reported; no pooling across incommensurable measures; flag overlapping samples across reviews.
5. **Vote counting** only by direction of effect, with k, N, effect sizes and a display; never "k of n significant"; never infer "no effect" from non-significance [S01, S20, S27, S30].
6. **Robustness**: recompute each finding without `reporting_adequacy: inadequate` studies and record changes [S09, S10]; screen each finding for small N, preregistration, number of tested relationships, replication status, missing results [S28-S30, S54 AB]. Appraise reviews you rely on with AMSTAR 2 critical domains; a review with a critical flaw is a lead, not a finding [S25].
7. **Causal wording gate**: causal verbs only when >=2 designs with different bias structures agree and confounding is not critical; otherwise "associated with" + named confounding story [S22, S24, S30, S50 AB].
8. **Certainty per finding** (`certainty.md`): GRADE for effect findings (start high randomised / low observational; down: limitations, inconsistency, indirectness, imprecision, reporting bias; up: large effect, dose-response, opposing confounding) [S22; 2011 series AB]; GRADE-CERQual for qualitative/interpretive findings (methodological limitations, coherence, adequacy, relevance; concern levels none/minor/moderate/serious with written reasons; no numeric scores; no double downgrading; findings as explicit propositions) [S03-S07]. Two independent agent assessments with a reconciling note [S03, S05; INFERENCE]. Mixed findings: rate each stream, then state the integration fit [S21]. Findings without a certainty record cannot appear in Key findings.
9. **Integration** of streams: joint display with confirmation / expansion / discordance per proposition; discordance triggers bias check -> construct check -> theory -> new search [S21, S18, S20]. Use convergent segregated when streams answer different aspects, integrated when the same question [S17, S18].
10. **Insight layer** (`insights.md`) - procedure [S02, S08-S14, S19-S21; composite order INFERENCE]: harvest constructs not conclusions (first-/second-/third-order); cluster and reciprocally translate, flag untranslatable concepts; **make contradictions the engine (refutational translation)**: test explanation by population, setting, measure/construct definition, design, time; import candidate theories and score data accommodated vs left over, keeping >=2 rivals; **name synthetic constructs** (definition + absorbed second-order constructs); draw the **line of argument** as a graph (edges carry supporting stems, contradicting stems, certainty; CMO triples for mechanisms); stress-test with the counter-evidence retrieval, negative cases, removal of weak studies, no smoothing or stretched explanations; ask whether the field's unit of analysis is wrong (e.g. deficit located in the person vs the matched/mixed interaction - the double-empathy move [S33-S35, S02]); state conditions of application and what would falsify it; adjudicate rival accounts with the four realist tasks (integrity of each theory; adjudication between competing theories on the same evidence; comparative settings; official account vs practice) [S64, S11]. Quality criteria checked in QA: every edge cites stems and whose interpretation it is; >=1 rival named with evidence; disconfirming cases listed; synthetic construct traceable; certainty per proposition with weakest link named; reasoning type labelled aggregated vs configured. Drop any insight you cannot chain to cited text.
11. **Autism/neurodiversity checklist** when relevant (protocol section 13): double-empathy/interactional account as a named competing theory (matched vs mixed partners?); autistic-authored and community-priority sources sampled and labelled; deficit-language audit; "who is speaking"; no pathologising of a single trait without measurement, context and dyad effects; the co-production limitation statement [S31-S37].
**Exit:** logic model, construct ledger, evidence matrix, certainty records and insights written; every key finding has framework + certainty + reasons; premise verdict stated; SWiM items complete.

## Phase 8 - Report

```bash
$S/flow_counts.py --run $RUN                  # PRISMA-style numbers from the run's own files -> flow.mmd, flow-counts.json
cp $SK/templates/report.md $RUN/report.md     # fill every section; replace {{...}}; delete guidance comments
$S/refs.py --report $RUN/report.md --write    # References from [@stem] cites; UNRESOLVED when metadata is empty
```
The template carries the reporting standards: PRISMA 2020 items (protocol 24a-c, sources 6-7, selection 8/16a-b, charting 9, appraisal 11/18, synthesis 13, certainty 15/22, characteristics 17, data availability 27) [P01, P02], PRISMA-S search reporting [P04], PRISMA-ScR vocabulary ("sources of evidence", charting) [P08], SWiM items [S01], an AI-use statement (tools, prompts, validation, oversight, the screening non-equivalence disclosure) [P01 items 8, 9, 11, 14, 15; P24 AB; PRISMA-trAIce is an unendorsed proposal, P36 AB], and a checklist-to-section map. PRISMA 2020 is designed primarily for intervention-effect reviews and applies to other topics with adaptation [P02]. A section with no evidence says so and goes to Gaps - no padding. Style: a map of the field with analysis layered on top; plain language; define constructs on first use.
**Exit:** `report.md` complete; References generated.

## Phase 9 - QA (blocking)

```bash
$S/verify_notes.py --run $RUN                 # extraction verification (if notes changed)
$S/audit.py --report $RUN/report.md           # audit.md + audit.json; exit 1 on any FAIL
```
FAIL: cited stem not in catalog; reference entry contradicting the verified record; stem with no verified record whose entry states title/year/authors; no reference line; retracted work; verbatim quote not in cited text; leftover placeholders; bare DOI that exists nowhere. WARN: abstract-only unflagged; uncited quantity; number not in cited text/note; approximate quote; no paper note; no certainty labels or framework named; "k of n significant" tallies; summed quality scores; missing protocol reference, PRISMA statement, AI-use statement or dual-screening non-equivalence disclosure; for autism topics: no double-empathy rival, no participatory/autistic-authored sources, no co-production limitation, no informant split. Fix every FAIL; justify or fix every WARN; ship `audit.md` with the report. Final human-oversight checkpoint = the claim audit [P25, P24 AB]: re-read a sample of cited passages against the source.
**Exit:** audit 0 FAIL; WARNs resolved or listed in Limitations.

## Rapid and living variants (only if the user asks)
- **Rapid** [P17 FT-part; P30 AB]: protocol still required; declare every restricted method with its potential bias; shortcuts from P17 are expert opinion (>=2 sources, pilot, 20% dual screen with kappa >= 0.8 then single pass, extraction by one + verifier, fewer fields); led by experienced synthesists. Write the "restricted methods" paragraph in Methods.
- **Living** [P32 FT-part; P33/P34 AB]: for fast-moving topics only. Keep protocol and query log; re-run saved queries with a `--date` filter since the last run; forward-chase from the included set (cheapest update [P23f AB]); append a dated update section; if meta-analysis is used, repeated updating inflates type I error [P35, abstract only].

## Script reference

| Script | Purpose |
|---|---|
| `scripts/hs_mcp.py` | JSON-RPC MCP client (SSE parsing, per-tool timeouts, `resolve_meta`) |
| `scripts/init_run.py` | create the run dir, fill protocol/scope templates |
| `scripts/protocol.py freeze|check|amend` | frozen protocol with version, time, SHA-256, amendment log |
| `scripts/discover.py search|validate|snowball|corpus|abstracts` | logged search, seed-recall validation, round-by-round citation chasing |
| `scripts/screen.py export|ingest|stats|finalize|adjudicate` | two-pass screening bookkeeping, kappa/PABAK, disagreements, recall audit |
| `scripts/acquire.py` | download/convert/index with resume, classification, catalog verification |
| `scripts/retrieve.py` | RQ queries -> evidence ledger + summary |
| `scripts/verify_notes.py` | quote-or-null verification of paper notes |
| `scripts/flow_counts.py` | PRISMA-style counts + mermaid from run files |
| `scripts/refs.py` | References appendix from `[@stem]` cites; flags unresolved metadata |
| `scripts/audit.py` | citation audit + method-conformance warnings for `report.md` |
All accept `--url`; run any with `--help`.

## Orchestration pattern

Main agent does phases 0-3 (judgement, shared context), 7-9. Fan out only: screening pass A and pass B (separate subagents, separate prompts, no shared state), full-text reading (`paper-reader`), and the second-pass verifiers/assessors. Each subagent gets self-contained instructions and writes only its own files; the main agent integrates and never lets a subagent edit `report.md`. Record models/prompts per stage in `synthesis/ai-use-log.md`.
Slash command: `/research <topic>` (`/research-synthesis:research` when installed as a plugin; definition in `commands/research.md`).
