# Protocol: {{topic}}

Run: `{{run_dir}}`  |  Drafted: {{date}}

> Keys `[Pxx]` / `[Sxx]` resolve in `reference/methodology-process.md` section 10 and `reference/methodology-synthesis.md` section 9 (authors, DOI, home-still stem, read-status; `AB` = only the abstract was available - the practice is stated as the abstract states it).
> Everything marked TODO is run-specific and MUST be filled before `protocol.py freeze` (it refuses while any TODO remains). Defaults below are the skill's spine; deviate only by writing the reason here.
> Freezing before the first external search implements [P05, P06, P01 items 24a-c]: a protocol lets readers detect deviations and selective reporting. Local-corpus queries (`retrieve.py`) are logged and may precede the freeze; `paper_search`/`openalex_*` searching may not.

## 1. Review type and rationale
- **Default: scoping / mapping review conducted with systematic search methods** [P11 Munn: scoping suits identifying types of evidence, clarifying concepts, examining how research is conducted, identifying characteristics/factors, and gaps; P09 Arksey & O'Malley; P10 Levac; reporting per P08 PRISMA-ScR]. A "meta-survey of a high-level topic" is not a named review type in any source read; mapping it onto scoping-with-systematic-search is an [INFERENCE] recorded in `methodology-process.md` §0.
- Why this run fits (TODO: one paragraph tying the user's purpose to P11's indications; state if a systematic review of a precise sub-question would fit better, e.g. a single association):
- Deliberate deviation from scoping convention: scoping reviews do not usually appraise methodological limitations [P11], but this skill appraises core papers because per-finding certainty (GRADE / CERQual) requires a methodological-limitations judgement [S03, S06; INFERENCE].
- Rapid shortcuts used? TODO (no / yes: list each restricted method and its potential bias [P17, P30 AB]). Living-review mode? TODO (no / yes: saved queries re-run with a date filter, forward chasing from included set, dated update section [P32, P23f AB]).
- Registration: not registered (no registry exists for agent runs); this file plus its hash is the record [P01 item 24a; INFERENCE substitute].

## 2. Question and framework
- User's question, verbatim: TODO
- **PCC** (Population, Concept, Context) for the scoping question [P08 items 4-5; P10 stage 1: broad question + clearly articulated scope]; use SPIDER for qualitative/mixed sub-questions [P14 AB], PEO (exposure, population, outcome) for "is A connected to B?" sub-questions [S26, with MOOSE alongside PRISMA].

| | Definition used in this review (with synonyms / spellings) |
|---|---|
| Population | TODO |
| Concept | TODO (construct map: `scope.md` section 4) |
| Context | TODO |

- Research questions: TODO (see `scope.md` section 3; each tagged aggregative or configurative below).
- Premise check is part of the question: premises, what-if-false results and rival framings are in `scope.md` section 2.

## 3. Logic and planned synthesis, decided before searching [S16, S19, S26]
| RQ | Question type (PEO / PICo / PICO / COSMIN / mechanism) | Logic | Evidence stream(s) | Synthesis method | Certainty framework |
|---|---|---|---|---|---|
| RQ1 | TODO | aggregative / configurative / both | quantitative / qualitative / mixed / reviews | see rules below | GRADE / GRADE-CERQual |

Defaults (justify any change; changes after this point are amendments, cf. SWiM item 1b [S01]):
- **Aggregative** (how strong is the association, how certain): quantitative streams; SWiM-reported narrative synthesis when meta-analysis is not possible [S01]; meta-analysis only when the same construct, similar designs and convertible effects exist [S27, S38 AB]. Vote counting only *by direction of effect* with k, N, effect sizes and a display, never "k of n significant" [S01, S20, S27, S30].
- **Configurative** (why/how, moderators, meaning): thematic synthesis [S08] or best-fit framework synthesis when an adequate model exists [S09, S10]; meta-ethnography only for <=~40-50 well-defined qualitative studies [S12-S14]; **critical interpretive synthesis (CIS)** when the concept itself is contested and the field's framing is under scrutiny [S02]; **realist CMO** for mechanism claims [S11]; **meta-narrative** when research traditions conceptualise the topic differently [S48].
- **Mixed streams**: convergent *segregated* when streams answer different aspects (effects vs experience), convergent *integrated* when both answer the same question [S18, S17]; integration by joint display with confirmation / expansion / discordance labels [S21].
- Before reading results: write the theory / logic model (assumed pathway, moderators, population) [S01 item 1; Popay element 1 via S17] - `synthesis/logic-model.md`.
- Construct ledger for every key construct (operational measure x population x informant); never pool across ledger groups without saying so [S01 item 1a; S07; S26; S §6.4 is an INFERENCE - the 'jingle-jangle' label itself is NOT VERIFIED in home-still].

## 4. Eligibility criteria
- Set independent of what studies exist; applied consistently; revising them after seeing borderline cases means redoing the search and sift [P18]. State study characteristics (population/concept/context, design, setting) and report characteristics (year, language, publication status) [P01 item 5].

| | Include | Exclude |
|---|---|---|
| Populations | TODO | TODO |
| Concepts / outcomes | TODO | TODO |
| Designs | TODO | TODO |
| Years / language / status | TODO | TODO |
| Sources allowed as background (theory, reviews, critique, autistic-authored/community work) | TODO | TODO |

Preprints, theses and community-authored work are eligible unless excluded above (publication-bias control; include published and unpublished [P18]).

## 5. Information sources and search strategy
- **Sources (>= 2 required [P18, P17 rec 5])**, each logged separately in `corpus/search-log.tsv` with provider, query verbatim, date, filters and hit count [P01 items 6-7, P04]:
  1. home-still corpus: `distill_search`, `abstract_search` (local source; `retrieve.py` log)
  2. `paper_search` providers: all, openalex, semantic_scholar, europmc, crossref, core, arxiv (separate sources)
  3. local OpenAlex BM25 (`openalex_search`)
  4. citation chasing (section 6)
- **Limits to report**: `paper_search` offers no Boolean/subject-heading control; `openalex_local` is BM25 over title+abstract (long queries return little); provider coverage differs; paywalled work is only reachable as abstracts. [P §9 'Search' row; INFERENCE]
- **Strategy built from seeds** [P01 item 7; P18 'test one's search strategy']: seed set of >= 5 known-relevant papers (from the corpus check and the user; diverse in author, year, venue; not authorially clustered [P15]) in `queries/seeds-known.txt`. TODO: list seed DOIs/titles here. Candidate terms are derived from seed titles/abstracts/keywords; `discover.py validate` must report full seed recall before the full search is accepted; the validation set is reported in the review.
- Sensitivity over specificity at the search stage; specificity enters at full-text screening [P18].
- **Strategy peer review**: a second agent pass audits the query matrix against the PRESS elements as stated in P19 (AB: accurate translation of the question into concepts, correct operators, adequate translation per source, relevant subject headings, no spelling errors) and records changes; PRESS presumes a human information specialist [P19 AB; INFERENCE substitute].
- Query files: `queries/search.txt` (constructs x population x method terms, including disconfirming/critical/stigma/first-person queries), `queries/rq.txt` (semantic retrieval). No unlogged searching.
- De-duplication: normalised DOI, then title+year; merged-provider list kept; counts reported [P04 items 15-16].

## 6. Citation chasing (Wohlin snowballing) [P15]
- Start set = papers included on the **full text** (never unscreened candidates); decide include/exclude on the full paper BEFORE it becomes a seed (else roll back) [P15 step 3].
- Backward (`paper_references`, `openalex_references`) and forward (`paper_citations`, `openalex_citations`), one round at a time for traceability, apply basic criteria (language, year, type), judge by title/venue/author and citation context; log base articles, direction, platform, date [P04 item 5].
- Track yield per round (`snowball-rounds.tsv`); yield should fall; if it does not, re-search with synonyms (a cluster was missed) [P15 4.9]. **Stop when a round adds no new includes.**
- Snowballing complements and does not replace database search [P15; evidence limited to one replication, treated as a hypothesis]. Data sources are Semantic Scholar/OpenAlex rather than Google Scholar, so coverage differs [P23d AB].

## 7. Selection process [P17, P18, P01 items 8 and 16, P10 stage 3]
- Stages: pilot -> title/abstract screening (two independent passes) -> full-text screening -> recall audit.
- **Pilot**: 50-100 records (`screen.py export --pilot`) assessed by both passes; criteria and prompts revised after the pilot [P17].
- **Two independent agent passes** (pass A, pass B): different prompt wording and, where available, different models; no shared state; neither sees the other's decisions. Both record decision (include / exclude / unsure), a reason code for every exclusion, and confidence. **Err toward inclusion** at this stage; `unsure` counts as include [P18].
- Agreement: Cohen's kappa **and** prevalence-adjusted kappa (PABAK), reported together, plus raw agreement, because class imbalance distorts both [P38 AB, P39 AB; the PABAK remark is an INFERENCE in P 8.2]. Gate: kappa >= 0.8 licenses single-pass screening of the *remainder* in rapid mode only [P17 rec 9; the 20% / 0.8 numbers are expert opinion per P17]; otherwise continue dual screening.
- Disagreements: adjudicated by a third pass with both rationales visible, or by the user when it matters; adjudicator recorded (`screen.py adjudicate`) [P01 item 8; P18].
- **Recall audit**: a random sample (default 25) of records BOTH passes excluded is re-read; any wrongly excluded record means the criteria/prompt are revised and the sift is redone [P18; checkpoint design from P25: audits of samples with acceptance thresholds, not blanket approval]. Threshold: TODO (default: 0 wrongly excluded in 25; > 1 forces a redo).
- Full-text screening: read via `markdown_read`; **reason recorded for every exclusion** (stem, DOI, reason code, supporting quote) [P01 item 16b; P18]; "full text not retrievable" is recorded separately (PRISMA 'reports not retrieved') and is not ineligibility; second pass on all borderline/excluded.
- **Disclosure (must appear in the report):** two LLM passes are *not shown* to be equivalent to two human screeners; the literature read reports LLM screening accuracy that is inflated by class imbalance and unreliable in balanced sets [P38 AB, P39 AB], and single-reviewer screening misses ~13% of relevant studies [P28 AB] while human abstract screening itself errs ~10.8% [P29]. Compensating controls: independent passes, kappa/PABAK, adjudication, recall audit. [P §9 'Screening' row: literature gap, INFERENCE]

## 8. Data extraction ("charting") [P17 recs 10-12, P10 stages 4-5, P20, P21 AB, P41 AB]
- Fixed schema = `templates/paper-note.md`; pilot on 2 papers before the batch [P17]; fields limited to those that answer the question.
- **Quote-or-null rule**: every extracted value carries a verbatim quote + stem + page/line; a value the paper does not state is `null` / `not reported`, never inferred [P41 AB: ~4% confabulation; P40 AB: models flag missing items].
- **Verification pass**: a second pass re-checks every quote and value against `markdown_read`; `scripts/verify_notes.py` does the deterministic part; numbers re-verified by hand on a 10-20% sample [P17 'one extracts, second verifies'; P20: extraction errors up to 50%].
- Extra fields mandated by the synthesis methods: construct label / operational measure / informant (construct ledger) [S01 item 1a, S26], outcome-level appraisal [S23, S24], first-/second-/third-order evidence [S12, S13], reporting adequacy [S09, S10].
- When the topic concerns autistic people: **who is speaking** (autistic self-report, family report, clinician/observer, performance task), diagnostic method, matched vs mixed dyad [S31-S35; INFERENCE in S §7].

## 9. Appraisal [S23-S25, S68-S69; rules in methodology-synthesis.md 1.6]
Tool is chosen by the **study's design**, not by topic [S26, S16]. Appraise per **result/finding**, not per paper [S23, S24, S06]. Record domain judgement + supporting quote or `NI` (no information); **no summed quality score, no inclusion by score** [S25, S05, S27, S71]. Keep relevant-but-weak evidence, label it, and run sensitivity analysis [S02, S08-S10].

| Evidence unit | Tool | Status in the reference |
|---|---|---|
| Randomised trial | RoB 2 (5 domains, signalling questions) [S23] | full text read |
| Non-randomised intervention study | ROBINS-I (7 domains; target trial + confounders listed in advance) [S24] | full text read |
| Exposure cohort ("does X cause Y") | ROBINS-E [S41] | **AB only**: domain list not available here; apply the confounder-first logic of S24 and say so [INFERENCE] |
| Cohort / case-control | Newcastle-Ottawa [S68, S69] - stars are not summed; contact authors for unreported details (agreement was low) | partial read |
| Cross-sectional / correlational (most "connection between A and B" evidence) | AXIS is named as the cross-sectional tool [S68] but its **item list was not read**; minimum coding: sampling frame, measurement validity of exposure and outcome, confounder adjustment, non-response [INFERENCE] | AB / named only |
| Test / psychometric measurement | QUADAS-2 (patient selection, index test, reference standard, flow & timing) [S42 AB]; COSMIN for psychometric reviews [S26] | AB |
| Systematic review / meta-analysis used as evidence | AMSTAR 2: 7 critical domains, no overall score; confidence High/Moderate/Low/Critically low [S25]; ROBIS [S43 AB] | AMSTAR 2 read |
| Qualitative primary study | no consensus tool: CIS prompts [S02 Table 1], best-fit minimal criteria [S09, S10], CASP-style [S14: low agreement], CERQual methodological limitations per finding [S06] | read |
| Mixed-methods study | MMAT 2018 [S44 AB; S66] | criteria **not read** |
| Theory / opinion / narrative review | JBI text-and-opinion checklist exists [S68]; items not read: code argument transparency and evidence base [INFERENCE] | named only |
| Reviews relied on | A review with a critical flaw is a lead to its primary studies, not a finding [S25 Box 2] | read |

Where a tool's item list is not in the reference, the agent does not reproduce it from memory: it codes the minimum above, records `tool: partial-coding`, and tells the user which DOI to obtain.

## 10. Synthesis procedure
- Stream by design; one appraisal tool per stream; one named synthesis method per stream (section 3). Fill the nine SWiM reporting items for every quantitative-without-meta-analysis synthesis (grouping, metric, method, prioritisation criteria, heterogeneity, certainty, presentation, results, limitations) [S01]; unfilled item = blocker.
- Heterogeneity: explore by hypothesised modifiers (design, subgroup, setting, measure, informant); label informal exploration as post-hoc and "rarely definitive" [S01 item 5].
- Robustness: recompute each finding without `reporting_adequacy: inadequate` studies and report changes [S09, S10]; small-N / flexible / exploratory / non-replicated findings are marked and require converging independent evidence [S28-S30].
- **Causal wording gate**: causal verbs only if >= 2 designs with different bias structures agree and confounding is not judged critical; otherwise "associated with" plus a named confounding story [S22, S24, S30, S50 AB; INFERENCE]. Confounder list generated before extraction [S24].
- Integration across streams: joint display, each cell labelled confirmation / expansion / discordance; discordance triggers bias check -> construct check -> theory -> new search [S21, S18, S20].

## 11. Certainty of evidence (per finding, never per review)
- Effect-estimate findings: **GRADE** [S22]: start high for randomised, low for observational (cross-sectional/correlational evidence is observational); rate down for study limitations, inconsistency, indirectness, imprecision, reporting/publication bias; up for large effect, dose-response, all plausible confounding opposing the effect. The 2011 GRADE series is AB-only in the reference [S53-S58 AB]; the thresholds quoted come from S22.
- Qualitative / interpretive findings: **GRADE-CERQual** [S03-S07]: four components - methodological limitations, coherence, adequacy of data, relevance - each rated no/minor/moderate/serious concern with a written reason; start high, rate down; avoid double downgrading; **no numeric scoring**; state each finding as an explicit proposition.
- Two independent agent assessments per finding with a reconciling note [S03, S05; mapping to agents is an INFERENCE]. Output a certainty record per finding (`synthesis/certainty.md`, fields: statement, logic, stream, supporting/contradicting stems, appraisal, framework, overall certainty, reasons, what would change it) [S §4.3, INFERENCE].
- Mixed findings: rate each stream with its own framework, then state the integration fit [S21]; no mixed-methods certainty instrument was found [INFERENCE].

## 12. Insight generation (the interpretive layer) [S02, S08-S14, S19-S21; composite order is INFERENCE]
1. Harvest constructs, not conclusions: first-order evidence, second-order interpretations, measures per study. 2. Cluster and translate (reciprocal), flag untranslatable concepts. 3. Make contradictions the engine: **refutational translation** - test explanation by population, setting, measure/construct definition, design, time. 4. Import candidate theories top-down and score fit (data accommodated vs left over); keep >= 2 rivals alive. 5. Name **synthetic constructs** with definitions and the second-order constructs they absorb. 6. Draw the **synthesising argument / line of argument** as a graph (nodes = constructs, edges = relations with supporting stems, contradicting stems, certainty); CMO triples for mechanisms. 7. Stress-test: dedicated counter-evidence retrieval, negative cases, no smoothing out or stretched explanations, remove weak studies. 8. Integrate streams with a joint display. 9. Ask whether the field's unit of analysis is wrong (e.g. matched vs mixed dyads). 10. State conditions of application and what would falsify. 11. Adjudicate rival accounts with the four realist tasks (integrity of each theory; adjudicate between competing theories on the same evidence; comparative settings; official account vs practice) [S64, S11].
- Insight quality criteria checked in QA: every edge cites stems and says whose interpretation it is; >= 1 rival named with evidence for/against; disconfirming cases listed; synthetic construct defined and traceable; certainty per proposition with the weakest link named; reasoning type labelled aggregated vs configured [S12, S07, S10, S02, S14, S20].

## 13. Participatory / neurodiversity-informed practice (required when the topic touches autistic people) [S31-S37]
- Carry the **double-empathy / interactional account** as a named competing theory for any "autistic people lack/cannot X" finding; ask whether X was measured with matched or mixed partners and whether the task presupposes neurotypical norms [S33-S36].
- Deliberately sample autistic-authored and community-priority sources (theoretical sampling) and label them; they are expert data, not grey literature [S02, S31, S32, S37].
- Deficit-language audit of construct and outcome labels; record the language convention used and why [S31, S32].
- State in the report that the synthesis is a literature product made without community co-production and invite correction [S31 principles].
- Do not pathologise a single trait as the explanation without noting measurement, context and dyad effects [S31-S36; INFERENCE].
- Applicable to this run? TODO (yes / no, with reason).

## 14. Automation, AI use and reference integrity [P01 items 8, 9, 11, 14, 15; P24 AB; P25; P26 AB; P27 AB]
- AI agents do screening passes, extraction, appraisal drafts, synthesis drafting. Synthesists remain accountable; AI use that makes or suggests judgements is reported transparently (tool/model, version, prompt, validation) [P24 AB, P01]. PRISMA-trAIce is a proposal, not endorsed [P36 AB].
- Human-in-the-loop checkpoints as audits of samples with thresholds [P25: human+AI was on average worse than the better of the two at decision tasks]: (1) protocol approval, (2) seed-set / eligibility confirmation, (3) screening recall audit, (4) final claim audit (`audit.py`). TODO: which checkpoints are executed by the user vs by an audit agent for this run.
- **Hallucination guard**: a citation enters the report only if it resolves to a `catalog_read` / `openalex_get` / provider record (title, authors, year, DOI matched) and the paper's own first lines agree; remembered references are leads, never evidence [P26 AB: 8.5-32.7% DOI accuracy; P27 AB: ~20% fabricated; measured on un-grounded chatbots - grounding should lower, not eliminate, the risk (INFERENCE)]. `catalog_read` metadata can be wrong or empty - always confirm against page 1 [S §6.7].
- Agent prompts and model names for each stage are archived in `synthesis/ai-use-log.md`.

## 15. Data and materials availability [P01 item 27, P02 Box 2]
- Pool, logs, notes, evidence ledger, audit and prompts are kept in the run directory. `personal_*` home-still tools are never used.

## Freeze
- Version: 
- Frozen at: 
- SHA-256 of sections above: 
- Frozen by: 

## Amendments log
| Date (version) | Change | Reason | Effect on conclusions |
|---|---|---|---|
