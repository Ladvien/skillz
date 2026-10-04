# Evidence-synthesis methodology: process (question → protocol → search → screen → extract → report → rapid/living → automation)

Scope: the **process** half of the research-synthesis skill. Appraisal/synthesis/certainty lives in `methodology-synthesis.md`. Every practice is tied to a source acquired through home-still (`paper_search` → `paper_download` → `scribe_convert` → `distill_index`) and read with `markdown_read`, or (where marked AB) abstract only via `paper_get`.

Compiled 2026-10-02. Source keys `[P01]`… resolve in §10 to authors, year, title, DOI, **home-still stem** (`doc_id`; use with `markdown_read` / `catalog_read` / `distill_search`) and read-status. The scratch/full-text dumps used while compiling this file were removed after the skill was grounded; every source remains retrievable through home-still by the stem in §10.

Read-status legend (same as sibling file):
- **FT** = full text read via `markdown_read` (sections named in each cite).
- **FT-part** = full text in corpus; only the cited passages were read.
- **AB** = abstract only (`paper_get`); full text paywalled ("No open-access PDF found"). Claims limited to what the abstract states.
- **NA** = not obtainable; listed so the skill knows the gap. Claims about NA sources are **not** made here.

Honesty notes: the page/section pointers below are the headings/box/item numbers visible in the converted markdown (page numbers were not reliably preserved). Markdown conversion of some PDFs is noisy (garbled tables in P01, P02, P08); where a table was garbled I quote only prose I could read. Anything not stated by a source is tagged **[INFERENCE]**.

---

## 0. One-screen process spine

1. **Classify the review type and justify it** (systematic vs scoping vs rapid vs living) [P11 Munn, P12 Grant&Booth AB, P13 Munn typology, P09 Arksey, P17 Garritty]. A *meta-survey of high-level topics* is closest to a **scoping/mapping review** with systematic search methods [INFERENCE — no source reviews "meta-surveys" by that name].
2. **Frame the question with an explicit framework** (PICO / PCC / SPIDER), broad question + clearly articulated scope (concept, population, context) [P10 Levac, P05 PRISMA-P, P08 PRISMA-ScR, P14 SPIDER AB].
3. **Write and freeze a protocol before searching**; log every amendment with date + rationale [P05, P06, P16].
4. **Search ≥ 2 sources, develop strategy from known-relevant seed papers, validate it recovers them, report every strategy verbatim with dates and counts** [P01 E&E item 7, P04 PRISMA-S, P18 Siddaway, P19 PRESS AB].
5. **Add citation chasing (backward + forward, iterated to saturation) as a complement, not a replacement** [P15 Wohlin].
6. **Screen against pre-set criteria, pilot first, record an exclusion reason for every full-text exclusion, measure agreement** [P17, P01 item 16b, P18].
7. **Extract with a piloted form; verify with a second pass** [P17, P20 Mathes, P21 Buscemi AB].
8. **Report with PRISMA-2020 flow + PRISMA-S + (scoping) PRISMA-ScR, including how many reviewers/automation tools did each step** [P02, P01, P04, P08].
9. **If AI does any step, report it (tool, version, prompt, validation) and keep a human accountable** [P01 item 8, P24 position statement AB, P25 Vaccaro].
10. **Every citation an LLM emits must be verified against a real record** (hallucination evidence: P26 AB, P27 AB).

---

## 1. Phase: question formulation & review-type choice

| Practice | Prescribed by | Source / location read |
|---|---|---|
| Choose between a systematic and a scoping review by *purpose*: scoping for identifying types of evidence, clarifying concepts/definitions, examining how research is conducted, identifying key characteristics/factors, as a precursor to a systematic review, identifying/analysing knowledge gaps; systematic for confirming practice, uncovering international evidence, informing future research with a critically appraised answer to a precise question. "The most important consideration is whether … to answer a clinically meaningful question or provide evidence to inform practice" | Munn 2018 | [P11] §"Deciding between a systematic review and a scoping review approach"; §"Indications for scoping reviews / systematic reviews" (FT) |
| Scoping reviews do not usually assess risk of bias / methodological limitations ("unless there is a specific requirement"); implications for practice therefore differ | Munn 2018 | [P11] §on scoping reviews not producing a critically appraised result (FT) |
| Arksey & O'Malley list four reasons for a scoping study: (1) examine extent, range, nature of research activity; (2)–(3) (determine value of a full systematic review; summarise/disseminate findings — read only partly) (4) identify gaps. The framework they present is for the gap-identifying type | Arksey & O'Malley 2005 | [P09] §"four common reasons" (FT; items 2–3 text truncated in my read) |
| Combine a **broad** research question with a **clearly articulated scope of inquiry** (define concept, target population, outcomes) because overly vague questions left later stages without direction; link the *purpose* to the question at stage one | Levac 2010 | [P10] §"Framework stage one" + Table 3 (FT) |
| State the question with PICO elements; "Reviews may focus on one PICO element more than others … state this emphasis in the protocol" | PRISMA-P E&E item 7 | [P06] Item 7 (FT) |
| PCC-style (population, concepts, context) or other key elements are accepted for scoping questions; the scoping rationale must explain why the question "lend[s] itself to a scoping review approach" | PRISMA-ScR items 4–5 | [P08] checklist table (garbled) + glossary (FT-part) |
| SPIDER (Sample, Phenomenon of Interest, Design, Evaluation, Research type) proposed for qualitative/mixed-methods questions where PICO fits poorly | Cooke 2012 | [P14] AB only |
| Break research questions into individual concepts → search terms; consider synonyms/spelling/broader-narrower terms | Siddaway 2019 | [P18] §Scoping, §Planning (FT-part) |
| Specify eligibility on study characteristics (PICO or variant, design, setting, follow-up) **and** report characteristics (year, language, publication status) | PRISMA 2020 E&E item 5 | [P01] Item 5 essential elements (FT-part) |
| Review typology (14 review types analysed with SALSA: Search, AppraisaL, Synthesis, Analysis); "few review types possess prescribed and explicit methodologies and many fall short of being mutually exclusive" | Grant & Booth 2009 | [P12] AB only |
| Justify inclusion/exclusion on theoretical/empirical grounds, set them independent of what studies exist, apply consistently; revising criteria after seeing borderline cases means **redoing the search and sift** | Siddaway 2019 | [P18] §Planning "Justify inclusion and exclusion criteria", "Borderline cases" (FT-part) |

## 2. Phase: protocol & registration

| Practice | Source / location |
|---|---|
| A protocol "describes the rationale, hypothesis, and planned methods"; clearly reported protocols let readers detect deviations and selective reporting | [P05] Abstract, Intro (FT) |
| PRISMA-P 2015: 17 numbered items (26 with sub-items) in three groups: administrative information, introduction, methods. Methods items include information sources (9), draft search strategy for ≥1 database (10), data management (11a), selection process "such as two independent reviewers" (11b), data collection "piloting forms, done independently, in duplicate" (11c), outcomes (13), variables (12), risk of bias (14), synthesis criteria/methods (15a–d), meta-bias (16), strength of evidence "such as GRADE" (17) | [P05] §Results/Table 3; [P06] Items 9–17 (FT) |
| Amendments: identify as such, list what changed; an updated protocol gets a new version number and a list of amendments; "Changes will not be incorporated into the protocol" (example wording); record amendments in the registry entry and report in the final review | [P06] Item 4 / "Amendments" (FT) |
| Register where possible (PROSPERO, OSF); PRISMA 2020 asks for registration info (24a), protocol access (24b) and amendments (24c) | [P01] Items 24a–24b; [P02] Box 2 (FT-part) |
| Rapid reviews also need a protocol (question framework such as PICOs, eligibility, methods for search, selection, extraction, RoB, synthesis); post-hoc changes are allowed but must be tracked and reported | [P17] §Protocol; §on protocol changes (FT-part) |
| PRISMA-ScR: indicate if a protocol exists and where it can be accessed | [P08] checklist item (garbled table; wording legible) (FT-part) |
| Scoping-review protocol guidance (JBI): exists (Peters/…, 2022) but **AB/NA** — not claimed | see §9 NA list |

## 3. Phase: search strategy design & reporting

| Practice | Source / location |
|---|---|
| Erring toward **sensitivity** at the search stage ("so that you do not miss anything"), shift to specificity only at full-text sifting | [P18] §Scoping, §Eligibility (FT-part) |
| Search ≥ 2 databases relevant to the topic; use truncation, proximity, parentheses/Boolean; then *additional* methods: hand-search key journals, read reference lists of included work, contact authors, grey literature (reports, theses, conference proceedings) | [P18] §Identification (FT-part) |
| Include published **and** unpublished work (publication bias); "accepted practice that rigorous research syntheses include both" | [P18] "Publication bias", "Locating unpublished work" (FT-part) |
| Develop strategy from **known relevant studies** (5 seed records → candidate terms), check the strategy retrieves them; report the validation set | [P01] Item 7 example + Item 6/7 elements ("If the search strategy was validated … report the validation process and specify which studies were included in the validation set"); [P18] §Planning "test one's search strategy by checking that the search at least yields the studies that are known to be relevant" (FT-part) |
| Present **full** line-by-line strategies for **all** databases/registers/websites with filters/limits (PRISMA 2020 changed this from "at least one database") | [P02] Box 2; [P01] Item 7 (FT-part) |
| Record the date each source was last searched; ideal last search < 6 months before publication; for re-runs report both original and updated strategies and why they changed | [P01] Item 6; [P04] Items 12–13 (FT-part) |
| PRISMA-S 16-item checklist (database name+platform; multi-database searching; study registries; online resources/browsing; citation searching; contacts; other methods; full strategies "copied and pasted exactly as run"; limits/restrictions with justification; search filters; prior work; updates; dates of searches; peer review; total records; deduplication) | [P04] Part 2 checklist + Part 3 E&E (FT) |
| Citation searching: report the **database/platform used**, the **"base" articles** searched, whether cited or citing, and date; if the same database is used for topical and citation searching describe each separately | [P04] Item 5 (FT); [P01] Item 6 bullet (FT-part) |
| Report total records per source; describe and cite the deduplication method/software; report post-dedup total in the flow diagram | [P04] Items 15–16 (FT) |
| Peer review the search (PRESS); PRESS six strongly supported elements: accurate translation of question into concepts, correct Boolean operators/line numbers, adequate translation per database, relevant subject headings, no spelling errors (+7 partially supported) | [P19] AB (abstract states elements); [P04] Item 14 (FT) recommends PRESS |
| Prior work reused: cite and copy-paste adapted strategies | [P04] Item 11 (FT) |
| Rapid-review variant: involve an information specialist; select a small number (≥ 2) of databases; use PRESS or at minimum double-check for typos/missed keywords; justify grey literature | [P17] Recs 4–7 (FT-part; table partly garbled) |
| Search-system choice matters: only about half of 28 academic search systems suited to evidence synthesis; Google Scholar "inappropriate as principal search system" | Gusenbauer & Haddaway 2020 [P22] AB only |

### 3.1 Citation snowballing (backward/forward)
Source: Wohlin 2014 [P15] FT (whole text read).
1. **Start set**: from a search (Google Scholar in the paper); should cover different communities/publishers/years/authors, derive from research-question keywords + synonyms; includes only papers that will finally be included. Avoid an authorially clustered start set (his own example had one author in common — flagged as a weakness).
2. **Iteration**: backward = reference list (apply basic criteria: language, year, type; drop already-examined; judge by title, venue, author, *and the place/context of the citation*); forward = citing papers (Google Scholar info → abstract → citation context → full text).
3. **Decide include/exclude on the full paper *before* using it as a snowballing seed**, otherwise roll back; iterate one round at a time for traceability; **stop when no new papers**.
4. Complement by contacting authors of included papers; restart if new papers appear.
5. Lessons (§4.9): track yield per iteration (should fall); if yield does not fall, re-search with synonyms (a cluster was missed); a **citation matrix** with many blanks signals missed papers (but cannot reveal an independent cluster); a timeline explains impossible citations.
6. Evidence: replication of a published SLR found the same papers (9 shared; 11 total in that case); overall efficiency 3.7% of candidates; "snowballing should not necessarily be seen as an alternative to database searches"; "different approaches … preferably used to ensure the best possible coverage."
7. Snowballing "is by deduction a better approach than a database search for extending" a review — **author states the evidence is left for further research** [P15 §5] → treat as hypothesis, not finding.
8. Further evidence on citation chasing is **AB-only**: Briscoe 2019 (Cochrane: 172/215 reviews reported backward, 18 forward citation searching; lack of MECIR guidance for forward) [P23a]; Hirt 2023 scoping review (47 studies; 96% found added value; terminology heterogeneous) [P23b]; Haddaway 2022 citationchaser tool [P23c]; Gusenbauer 2024 (Google Scholar, ResearchGate, Semantic Scholar, Lens best for forward citation; WoS CC over Scopus for backward) [P23d]; Felizardo 2022 hybrid database+snowballing found 30% more primary studies than a traditional search in one replication [P23e]; Wohlin 2020 update-SLR guideline: single-iteration forward snowballing from the original SLR is most cost-effective for updates [P23f]. **None read in full.**

## 4. Phase: screening & selection

| Practice | Source / location |
|---|---|
| Pre-specify criteria, **pilot** screening on a purposive 50–100 records assessed by all screeners, revise forms/criteria after the pilot; use title/abstract form then full-text form with examples | [P17] §Study selection (FT-part) |
| **Dual independent** screening is the reference practice ("ideally conducted by two separate reviewers"); quantify agreement with Cohen's kappa or ICC; specify how disagreements are resolved (discussion/consensus, third reviewer) | [P18] §"Inter-rater reliability"; [P01] Item 8 (FT-part) |
| Scoping: ≥ 2 reviewers independently review abstracts; meet at the **beginning, midpoint and end** of abstract review to resolve uncertainty and refine the search | [P10] Stage 3 (FT) |
| Rapid-review reduction: dual-independent screen ≥ 20% (the 20% is "based on our experience … not evidence based"), check agreement, **proceed with single screening if κ ≥ 0.8**, otherwise continue dual until agreement improves; same for full text | [P17] Rec 9, §Study selection (FT-part) |
| Empirical cost of single screening: single reviewer missed **13%** of relevant studies (sensitivity 86.6%) vs dual **3%** (97.5%); may be viable for rapid reviews | Gartlehner 2020 [P28] AB only; the same figure is repeated in [P01] §Limitations example (FT-part) |
| Humans are not a perfect gold standard: abstract-screening error (false include + false exclude) **10.76%** (95% CI 7.43–14.09) over 329,332 decisions in 25 dual-screened reviews, range 5.76–21.11% by topic; "achieving error rates similar to humans may be adequate" | Wang 2020 [P29] Abstract, Results, Discussion (FT) |
| **Record the reason for every full-text exclusion** in a table; for title/abstract exclusions a count suffices | [P18] §Planning bullets; [P01] Item 16b ("cite studies that might appear to meet the inclusion criteria, but which were excluded, and explain why") (FT-part) |
| Report how many reviewers screened each record/report, whether independent ("unaware of each other's decisions"), and how disagreements were resolved; report single-screen/verify designs explicitly | [P01] Item 8 essential elements (FT-part) |
| Borderline cases: discuss, consult theory/evidence; test whether including them matters | [P18] "Borderline cases"; also Felizardo 2022 "wild cards / borderline articles" [P23e] AB |
| Flow diagram: records identified per source → duplicates removed → "Records marked as ineligible by automation tools" → screened → excluded → reports sought/not retrieved → assessed → excluded with reasons → included; split human vs automation exclusions | [P01] Item 16a + Fig 1 (FT-part); [P02] Fig 1 (garbled) |
| Reusable "previous known assessments", ML classifiers (calibrated to a recall level), priority screening, priority screening with automatic stopping ("risk of erroneously excluding relevant studies because of uncertainty about when it is safe to stop"), crowdsourcing — each has report requirements | [P01] Item 8 "Explanation" lists (FT-part) |

## 5. Phase: data extraction ("charting")

| Practice | Source / location |
|---|---|
| Pilot the form on ≥ 2 studies with all reviewers; limit fields to those that answer the question (rapid); **one extracts, second verifies key data** (outcome definitions, outcome data) and checks full texts; disagreements → discussion, third reviewer | [P17] Recs 10–12, §Data extraction (FT-part) |
| Extraction error evidence: errors up to 50%; effect on estimates; "evidence base for established standards of data extraction seems weak"; no study on reviewer training found | Mathes 2017 [P20] Abstract (FT-part) |
| Single extraction produced 21.7% more errors than double (P = .019) but took 36.1% less time; no substantial effect-estimate difference for most outcomes | Buscemi 2006 [P21] AB only |
| Scoping "charting": team decides variables up-front; iterative team approach; report analysis in three steps (descriptive numerical summary + thematic analysis; report results; meaning vs purpose) | [P10] Stages 4–5 + Table 3 (FT) |
| PRISMA-ScR charting item: describe piloted forms and whether charting was independent/in duplicate | [P08] checklist item 11 (garbled; wording legible) (FT-part) |
| Extract broadly ("all potentially relevant information") when the review is not a rapid one; keep a characteristics-of-included-studies table | [P18] §Eligibility "Extract all potentially relevant information" (FT-part) |
| Report how many reviewers collected data, independence, processes to obtain/confirm data from investigators, automation used | [P01] Item 9 (FT-part) |

## 6. Phase: reporting

| Practice | Source / location |
|---|---|
| PRISMA 2020 = 27-item checklist + abstract checklist + flow diagrams for new and updated reviews; "designed primarily for systematic reviews of studies that evaluate the effects of health interventions" but applicable to other topics with adaptation | [P02] Summary points, "Scope" (FT-part) |
| PRISMA 2020 noteworthy changes (Box 2): full strategies for all sources; reviewers/independence/automation in selection; reporting how outcomes defined; data/code availability item 27; cite excluded near-miss studies (16b); registration amendments (24c); certainty items (15, 22); competing interests (26) | [P02] Box 2 (FT-part) |
| E&E gives "essential" vs "additional" elements per item; essential elements prefixed "If…" apply only when relevant | [P01] intro (FT-part) |
| PRISMA-ScR: 20 essential + 2 optional items, 26-member panel, 85% a-priori Delphi consensus rule; critical appraisal optional ("source of evidence" terminology instead of "study"); charting instead of extraction | [P08] Abstract, §2.1–2.4, glossary (FT-part) |
| PRISMA-S for the search methods section and as a protocol aid; may be reported in supplements; deposit search strategies in a repository | [P04] Part 2–3 (FT) |
| Make materials public (data, code, extraction sheets) — PRISMA 2020 item 27 | [P02] Box 2; [P01] (FT-part) |
| Annual Reviews guidance: document scoping decisions, keep decision records ("literally impossible to remember … thousands of decisions") that feed the methods text and kappa | [P18] §Planning "Create clear record-keeping systems" (FT-part) |
| Declare limitations of shortcuts (example: dual screened only 30%, rest single; cited 13% miss) | [P01] §Limitations example (FT-part) |
| Reporting update-specific details (previous-review count, new additions) in the flow diagram for updates | [P01] Item 16a bullet; [P02] Fig 1 (FT-part) |

## 7. Phase: rapid & living adaptations

### 7.1 Rapid reviews (Cochrane Rapid Reviews Methods Group)
Source: Garritty 2024 [P17] FT-part (24 recommendations; tables partly garbled). Interim guidance 2021 [P30] **AB** (26 recommendations from a 63-respondent survey; "best practice is limited by the lack of … evidence for some RR methods shortcuts").
- Definition: speeds up planning/doing/sharing of a structured review "by simplifying or omitting a variety of methods that should be clearly defined by the authors."
- Restricted methods must be **declared with their potential biases**.
- Shortcuts recommended (each marked "expert opinion" in the table unless noted): involve knowledge users in question; limit outcomes/interventions/date/setting/language with justification; ≥ 2 databases + information specialist + PRESS; pilot screening; 20% dual screen with κ ≥ 0.8 gate; limit extraction fields; one extractor + one verifier; one RoB assessor + one verifier; one GRADE rater + one verifier; reuse existing SR data/certainty where available.
- "It is advisable that rapid reviews are led only by experienced systematic reviewers"; protocol required.
- Evidence of fast automated review: complete SR in 61 person-hours / 12 calendar days by experienced team using automation tools (Clark 2020) [P31] AB.

### 7.2 Living systematic reviews
- Concept: continually updated, online-only; "a literature search strategy is maintained and outputs fed continuously into an SR workflow"; when no new studies, update only the date of last search; modest editorial review when new data don't change conclusions; rapid but robust review when conclusions change; relevant for **fast-moving topics with uncertain evidence** [P32 Elliott 2014 FT-part; P33 Elliott 2017 pt 1 AB].
- Human + machine workflows: automation can help searching, eligibility, extraction, RoB; humans scarce and needed where automation impossible/undesirable [P34 Thomas 2017 AB].
- Repeated updating inflates type I error in standard meta-analysis (relevant only if meta-analysis is used) [P35 Simmonds 2017 — converted markdown was only a catalogue page; **abstract text read only**].
- Search updating details: report the update method (re-run, alerts), date, changed syntax [P04 Items 12–13 FT]. Forward snowballing from the original included set is the cheapest update search (one SE case) [P23f AB].

## 8. Phase: automation / LLM-assisted review & safeguards

### 8.1 Governing standards
- **Joint position (Cochrane, Campbell, JBI, CEE 2025)**: synthesists remain "ultimately responsible"; AI may be used if it "will not compromise the methodological rigor"; **human oversight**; "any use of AI or automation that makes or suggests judgements should be fully and transparently reported"; endorses the RAISE recommendations [P24] AB (Cochrane `cl2.70074` version; a JBI Evidence Synthesis version `10.11124/jbies-25-00480` was downloaded but not converted/read).
- **PRISMA 2020 already requires** automation reporting: tool, how used, how trained, **performance and internal validation**; ML classifier use reported in the flow diagram; whether machine decisions replaced or double-checked humans [P01 Items 8, 9, 11, 14, 15 FT-part].
- **PRISMA-trAIce** (proposed, not yet endorsed, "foundational proposal"): items to identify AI tools, describe human–AI interaction, report performance evaluation, limitations [P36] AB.
- Uptake reality: ~5% of 2,271 Cochrane/Campbell/EE syntheses (2017–2024) explicitly reported ML; ~90% of those using ML-enabled tools did not say if ML features were used [P37 Scotti 2025] AB.

### 8.2 Screening
- GPT-3.5/4 API title/abstract screening over 24,000+ records: accuracy 0.91; sensitivity of included 0.76; macro-F1 0.60; human–human κ = 0.46 vs prevalence-and-bias-adjusted κ 0.96 for model vs consensus [P38 Guo 2024] AB. Note the PABAK inflation under class imbalance [INFERENCE from the two κ values reported together].
- GPT-4 "human-out-of-the-loop" (Khraisha 2024): accuracy comparable to humans in some tasks but **chance agreement and class imbalance skewed results**; adjusted performance ranged from none (balanced ~1:1) to moderate (~1:3); full-text screening with reliable prompts reached human-like levels; "substantial caution" advised [P39] AB.
- Two further LLM-screening papers were downloaded (Syst Rev 2024 `10.1186/s13643-024-02575-4`; BMC MRM 2025 `10.1186/s12874-025-02583-5`) but **conversion failed or did not complete — not read; no claims**.
- ML prioritisation / stopping: Cochrane-aligned guidance says classifiers can be calibrated to a recall target; stopping is risky [P01 Item 8 FT-part]. Stopping-heuristic papers (SAFE) were downloaded but not read.

### 8.3 Extraction
- Claude 2: 96.3% accuracy on pre-specified items from 10 PDFs; GPT-4 + plug-in 68.8% (mostly plug-in/PDF parsing errors); given selected text 98.7%/100%; models correctly flagged missing items; "it remains essential for a human investigator to validate LLM extractions" [P40 Konet 2024] AB.
- Elicit/ChatGPT as a *second extractor*: precision/recall/F1 ≈ 92/92/92 (Elicit) and 91/89/90 (ChatGPT) vs human double-extracted gold; review-specific variables only 77–80%; **confabulation in ~4% of data points**; authors propose AI replacing the *second* human, the second human reconciling discrepancies with the first [P41 Helms Andersen 2025] AB.
- Custom GPT-4: 88.6% concordance on study-characteristics table, < 5% inaccuracies/omissions; RoB agreement fair–moderate [P42 Kim 2025] AB.
- Pooled LLM extraction precision 83.0% / recall 86.0%, lower accuracy for numeric data [P43 Scherbakov 2025] AB.

### 8.4 Search & references (hallucination)
- ChatGPT (3.5) generated 102 citations: 72.7% (natural sciences) and 76.6% (humanities) existed; DOI accuracy 32.7% vs 8.5%; DOI hallucination 89.4% in humanities [P26 Mugaanyi 2024] AB.
- GPT-4o: of 176 citations in literature reviews on mental-health topics **35 (19.9%) fabricated**, 45.4% of real ones had errors (mostly DOIs); fabrication rose for less visible topics (28–29% vs 6%) and specialised prompts [P27 Linardon 2025] AB.
- Further abstract-/full-text-level evidence on fabricated references in corpus but not fully read: Walters & Wilder 2023 (Sci Rep, `10.1038_s41598-023-41032-5`), Chelli 2024 (JMIR `10.2196/53164` stem `10.2196_53164`) — downloaded, **conversion not completed in this pass; no claims**.
- ChatGPT Boolean-query generation: "potential to generate effective Boolean queries", highly precise, suited to rapid reviews trading recall for precision; "needs further validation" [P44 Wang 2023] AB.
- Human–AI combinations: pre-registered meta-analysis of 106 experiments: on average human–AI systems performed **worse than the best of human or AI alone** (g = −0.23), better than humans alone (g = 0.64); losses concentrated in *decision* tasks (g = −0.27), gains in *creation* tasks (g = 0.19) [P25 Vaccaro 2024] FT-part. Relevance: a human "approving" LLM include/exclude decisions may not outperform the better of the two [INFERENCE].
- Tool landscape review: 21 SLR tools / 11 LLM-based; RAG common; recommends transparency, replicable evaluation, code availability [P45 Bolaños 2024] FT-part. Automated-lit-review generation from PDFs (summarisation baselines) [P46] FT-part (abstract-level only; low evidential value).

---

## 9. Agent-pipeline implementation table (phase → practice → source → how to implement → deviation)

| Phase | Human-standard practice | Source | Autonomous LLM-agent implementation | Where agent work must deviate / is the literature silent |
|---|---|---|---|---|
| Type & question | Justify review type by purpose; broad question + defined scope; PICO/PCC | P11, P10, P05, P06 | First artefact: `protocol.md` with review type + rationale (scoping/mapping for a high-level topic), question in PCC (population, concept, context), eligibility, explicit out-of-scope. Ask the user only if purpose is ambiguous. | Literature is human-team-based; PCC mapping to "high-level topics" is [INFERENCE]. Stakeholder consultation (Arksey optional stage, Levac "essential") is replaced by the **user checkpoint** [INFERENCE]. |
| Protocol | Pre-specify; register; amendment log | P05, P06, P01 24a–c | Write protocol file and hash/commit **before** any `paper_search`; every later change appended to an amendments table (date, change, reason). Registration impossible → state "not registered". | No registry for agent runs; keep the git/commit record as the substitute [INFERENCE]. |
| Search | ≥ 2 sources; seed-validated strategy; full strategies, dates, counts | P01 item 7, P04, P18, P17 | Log every query verbatim with provider, filters, date, result count (`paper_search` providers are separate sources; `distill_search` / `abstract_search` count as a "local corpus" source; `openalex_*` local DB as another). Build a **seed set** of known-relevant papers; verify recall of seeds before running full search. | Provider-level tuning is limited (no Boolean/MeSH control through `paper_search`); report this as a limit. No PRESS reviewer: use a **second agent pass to audit the strategy against PRESS elements** [INFERENCE; PRESS itself has human information specialists in mind (P19 AB)]. |
| Citation chasing | Backward + forward to saturation | P15, P04 item 5 | `paper_references`, `paper_citations`, `openalex_references/citations` from the *included* set only; one iteration per round; record yield; stop at zero new includes; build citation matrix for the included set; report base articles + platform + date. | Wohlin's rule "full paper before seeding" → include only after full-text screening. Data sources are Semantic Scholar/OpenAlex, not Google Scholar; coverage differs (P23d AB). |
| Dedup & records | Document dedup method | P04 items 15–16 | Dedupe on normalised DOI, then title+year; keep merged-provider list; report counts. | — |
| Screening (title/abstract) | Pilot; dual independent; κ; disagreement resolution | P17, P18, P10, P28 AB, P29 | Pilot on 50–100 records with the criteria prompt, revise. **Two independent agent passes** (different prompts or models, no shared state), blind to each other; compute κ (and prevalence-adjusted κ, report both); third pass or the user adjudicates disagreements; **err toward inclusion** at title/abstract stage; log reason + confidence. | **Does the literature support agent-dual-screening?** Partially: LLM screening can reach high accuracy/κ vs consensus but is inflated by class imbalance and unreliable in balanced sets (P38 AB, P39 AB); no source validates two-LLM dual screening as equivalent to two humans [INFERENCE gap]. Human single screening misses ~13% (P28 AB); human error ~10.8% (P29) → the bar is "no worse than humans", not zero error. Use a **recall audit**: human spot-check of a random sample of excludes. |
| Screening (full text) | Reason for every exclusion; second reviewer | P01 16b, P18, P10 | Full-text read via `markdown_read`; structured exclusion table (stem, DOI, reason code, quote). Second agent pass on all borderline/excluded. | Conversion failures/paywalls ≠ ineligible: record "full text not retrievable" separately (PRISMA "reports not retrieved"). |
| Extraction/charting | Piloted form; second extractor/verifier | P17 recs 11–12, P10, P20, P21 AB | Fixed schema; pilot on 2 papers; every extracted value stored with **verbatim supporting quote + stem + page/line**; verifier pass re-checks quote existence and value; numbers re-verified deterministically where possible. | LLM extraction: high accuracy on standardized fields, lower on review-specific/numeric (P40–P43 AB); ~4% confabulation (P41 AB) → "quote or null" rule, no unsupported values, human spot-check. Authors of P41 suggest the AI as *second* extractor [AB]. |
| Appraisal | See sibling file | — | See `methodology-synthesis.md` | — |
| Reporting | PRISMA 2020 + PRISMA-S (+ ScR); reviewers & automation per step | P01, P02, P04, P08 | Emit flow diagram counts from logs; methods text states: agent/model/version, prompts (archived), number of independent passes, who adjudicated, validation done; supplement with all query logs, screening tables. Use PRISMA-ScR vocabulary (sources of evidence, charting). | PRISMA-trAIce (P36 AB) is a proposal, unendorsed — cite as such. |
| Rapid adaptation | Declare restricted methods and their bias | P17, P30 AB | If the user wants speed: use P17 shortcuts (≥ 2 sources, pilot, 20% dual + κ ≥ 0.8 gate then single pass, extraction verify-only) and write the "restricted methods" paragraph. | The 20%/κ 0.8 gate is expert opinion (P17 says so). |
| Living adaptation | Maintained search, periodic update, cheap review of updates | P32, P23f AB, P04 items 12–13 | Persist protocol + query log; re-run saved queries with `date` filter since last run; forward-chase from included set; append dated update section. | LSR is for fast-moving topics (P32); decide per topic. |
| Hallucination guard | Verify references | P26 AB, P27 AB, P01 | Hard rule: **a citation enters the report only if it resolves to a `catalog_read`/`paper_get`/`openalex_get` record** (title, authors, year, DOI matched); LLM-recalled references are leads, never evidence; claims must quote chunks from `markdown_read`. | Fabrication rates (20–27% of references by DOI/existence in the cited tests) were measured on *un-grounded* chatbot output, not retrieval-grounded pipelines [INFERENCE: grounding should lower but is not shown here to eliminate risk — still verify]. |
| Human-in-the-loop | Oversight & accountability | P24 AB, P25 | Checkpoints: (1) protocol approval, (2) eligibility/seed-set confirmation, (3) screening recall audit sample, (4) final claim audit. | Evidence that human+AI is not automatically better than the better party (P25) → design checkpoints as **audits of samples with defined acceptance thresholds**, not blanket "human approval". |

---

## 10. Sources (acquisition status)

Stats (this run): 101 + 33 candidate DOIs submitted to `paper_download`; 55 + 18 acquired in storage = 73 (2 already present); 46 first-pass "No open-access PDF" (paywalled) – retry with `paper_get` first (suggested by a peer) was run and also failed for all. Of 73 stored, 25 markdown files were read in full or in part; the rest were still queued/failed conversion when the run was cut off (see "Downloaded, not read"). Cause for slow conversion: scribe backend saturated (6/6 in-flight) by concurrent workers.

### 10.1 Read (FT / FT-part)

| Key | Authors, year, title | DOI | Stem | Status |
|---|---|---|---|---|
| P01 | Page et al. 2021. PRISMA 2020 explanation and elaboration: updated guidance and exemplars… (BMJ) | 10.1136/bmj.n160 | `10.1136_bmj.n160` (also `W3123893780`) | FT-part (Items 5–9, 11, 16a/b, limitations example; tables garbled) |
| P02 | Page et al. 2021. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews (BMJ) | 10.1136/bmj.n71 | `10.1136_bmj.n71` | FT-part (Summary, Box 2, scope) |
| P04 | Rethlefsen et al. 2021. PRISMA-S: an extension to the PRISMA Statement for reporting literature searches in systematic reviews | 10.1186/s13643-020-01542-z | `10.1186_s13643-020-01542-z` | FT (checklist; Items 5, 11–16) |
| P05 | Moher et al. 2015. PRISMA-P 2015 statement | 10.1186/2046-4053-4-1 | `10.1186_2046-4053-4-1` | FT |
| P06 | Shamseer et al. 2015. PRISMA-P 2015: elaboration and explanation | 10.1136/bmj.g7647 | `10.1136_bmj.g7647` | FT-part (Items 1–17) |
| P08 | Tricco et al. 2018. PRISMA-ScR: checklist and explanation | 10.7326/m18-0850 | `10.7326_m18-0850` | FT-part |
| P09 | Arksey & O'Malley 2005. Scoping studies: towards a methodological framework | 10.1080/1364557032000119616 | `10.1080_1364557032000119616` | FT-part |
| P10 | Levac, Colquhoun, O'Brien 2010. Scoping studies: advancing the methodology | 10.1186/1748-5908-5-69 | `10.1186_1748-5908-5-69` | FT-part |
| P11 | Munn et al. 2018. Systematic review or scoping review? Guidance for authors… | 10.1186/s12874-018-0611-x | `10.1186_s12874-018-0611-x` | FT-part |
| P13 | Munn et al. 2018. What kind of systematic review should I conduct? A proposed typology | 10.1186/s12874-017-0468-4 | `10.1186_s12874-017-0468-4` | FT-part (intro/definition only) |
| P15 | Wohlin 2014. Guidelines for snowballing in systematic literature studies and a replication in software engineering | 10.1145/2601248.2601268 | `10.1145_2601248.2601268` | FT |
| P17 | Garritty et al. 2024. Updated recommendations for the Cochrane rapid review methods guidance for rapid reviews of effectiveness | 10.1136/bmj-2023-076335 | `10.1136_bmj-2023-076335` | FT-part |
| P18 | Siddaway, Wood, Hedges 2019. How to do a systematic review… (Annu Rev Psychol) | 10.1146/annurev-psych-010418-102803 | `10.1146_annurev-psych-010418-102803` | FT-part |
| P20 | Mathes et al. 2017. Frequency of data extraction errors and methods to increase data extraction quality | 10.1186/s12874-017-0431-4 | `10.1186_s12874-017-0431-4` | FT-part (abstract/methods) |
| P25 | Vaccaro, Almaatouq, Malone 2024. When combinations of humans and AI are useful: a systematic review and meta-analysis (Nat Hum Behav) | 10.1038/s41562-024-02024-1 | `10.1038_s41562-024-02024-1` | FT-part |
| P29 | Wang et al. 2020. Error rates of human reviewers during abstract screening in systematic reviews (PLoS ONE) | 10.1371/journal.pone.0227742 | `10.1371_journal.pone.0227742` | FT |
| P32 | Elliott et al. 2014. Living systematic reviews: an emerging opportunity to narrow the evidence-practice gap | 10.1371/journal.pmed.1001603 | `10.1371_journal.pmed.1001603` | FT-part |
| P45 | Bolaños et al. 2024. Artificial intelligence for literature reviews: opportunities and challenges | 10.1007/s10462-024-10902-3 | `10.1007_s10462-024-10902-3` | FT-part |
| P46 | (arXiv 2411.18583) automated literature-review generation from PDFs; authors/title not captured in converted text | 10.48550/arxiv.2411.18583 | `10.48550_arxiv.2411.18583` | FT-part (low value) |

Also in corpus and consulted only as context (not cited for specific claims): `10.1136_bjsports-2021-103987` (PRISMA E&E for sport and exercise medicine), `10.1136_bmj.j4008` (AMSTAR 2; see sibling file), `10.1186_s12874-017-0431-4` above.
Corpus stub, **not usable**: `10.1186_s12874-019-0782-0` (Waffenschmidt 2019 single vs double screening — markdown is a publisher banner); `10.1016_j.jclinepi.2014.03.013` (Colquhoun 2014 scoping reviews: time for clarity — 11 KB accepted-manuscript text, read only for its recommendation to use one definition/clarify methods); `10.1016_j.jclinepi.2017.08.008` (LSR 3 — catalogue page only).

### 10.2 Abstract only (AB) via `paper_get` (the abstract dump used while compiling was removed; re-fetch with `paper_get(doi)`)

| Key | Authors, year, title | DOI |
|---|---|---|
| P12 | Grant & Booth 2009. A typology of reviews: an analysis of 14 review types and associated methodologies | 10.1111/j.1471-1842.2009.00848.x |
| P14 | Cooke, Smith, Booth 2012. Beyond PICO: the SPIDER tool for qualitative evidence synthesis | 10.1177/1049732312452938 |
| P19 | Sampson et al. 2009. An evidence-based practice guideline for the peer review of electronic search strategies (original PRESS) | 10.1016/j.jclinepi.2008.10.012 |
| P21 | Buscemi et al. 2006. Single data extraction generated more errors than double data extraction | 10.1016/j.jclinepi.2005.11.010 |
| P22 | Gusenbauer & Haddaway 2020. Which academic search systems are suitable for systematic reviews or meta-analyses? | 10.1002/jrsm.1378 |
| P23a–f | Briscoe 2019 (10.1002/jrsm.1355); Hirt 2023 (10.1002/jrsm.1635); Haddaway 2022 citationchaser (10.1002/jrsm.1563); Gusenbauer 2024 (10.1002/jrsm.1729); Felizardo 2022 (10.1016/j.infsof.2022.106908); Wohlin 2020 (10.1016/j.infsof.2020.106366) | as listed |
| P24 | Flemyng et al. 2025. Position statement on AI use in evidence synthesis across Cochrane, Campbell, JBI, CEE | 10.1002/cl2.70074 |
| P26 | Mugaanyi et al. 2024. Evaluation of LLM performance and reliability for citations and references in scholarly writing | 10.2196/52935 |
| P27 | Linardon et al. 2025. Influence of topic familiarity and prompt specificity on citation fabrication… | 10.2196/80371 |
| P28 | Gartlehner et al. 2020. Single-reviewer abstract screening missed 13 percent of relevant studies | 10.1016/j.jclinepi.2020.01.005 |
| P30 | Garritty et al. 2021. Cochrane Rapid Reviews Methods Group offers evidence-informed guidance | 10.1016/j.jclinepi.2020.10.007 |
| P31 | Clark et al. 2020. A full systematic review was completed in 2 weeks using automation tools | 10.1016/j.jclinepi.2020.01.008 |
| P33 | Elliott et al. 2017. Living systematic review: 1. Introduction | 10.1016/j.jclinepi.2017.08.010 |
| P34 | Thomas et al. 2017. Living systematic reviews: 2. Combining human and machine effort | 10.1016/j.jclinepi.2017.08.011 |
| P35 | Simmonds et al. 2017. Living systematic reviews: 3. Statistical methods for updating meta-analyses | 10.1016/j.jclinepi.2017.08.008 |
| P36 | Holst et al. 2025. PRISMA-trAIce | 10.2196/80247 |
| P37 | Scotti et al. 2025. AI and automation in evidence synthesis: methods in Cochrane, Campbell, EE reviews | 10.1002/cesm.70046 |
| P38 | Guo et al. 2024. Automated paper screening for clinical reviews using LLMs | 10.2196/48996 |
| P39 | Khraisha et al. 2024. Can LLMs replace humans in systematic reviews? | 10.1002/jrsm.1715 |
| P40 | Konet et al. 2024. Performance of two LLMs for data extraction in evidence synthesis | 10.1002/jrsm.1732 |
| P41 | Helms Andersen et al. 2025. AI tools as second reviewers for data extraction | 10.1002/cesm.70036 |
| P42 | Kim et al. 2025. Novel AI applications in systematic review: GPT-4 assisted data extraction… | 10.1136/bmjebm-2024-113066 |
| P43 | Scherbakov et al. 2025. The emergence of LLMs as tools in literature reviews | 10.1093/jamia/ocaf063 |
| P44 | Wang et al. 2023. Can ChatGPT write a good Boolean query for systematic review literature search? | 10.1145/3539618.3591703 |
| — | Peters et al. 2020/2021 (JBI scoping guidance, 10.11124/jbies-20-00167 / 10.1097/xeb.0000000000000277): abstract read — "updated guidance … aligned with PRISMA-ScR; additional guidance on when a scoping review is (or is not) appropriate, how to extract, analyse and present results." Full text paywalled. |  |
| — | Moher et al. 2021 PRISMA 2020 development paper (10.1016/j.jclinepi.2021.02.003): 60 guidance documents reviewed, 110 survey respondents, 21-member meeting. |  |

### 10.3 Downloaded to storage but NOT read (conversion queued/failed when the run was cut off — no claims made)
`10.1016_j.jclinepi.2016.01.021` (PRESS 2015 update; converter returned 0 chars, HTML shell), `10.1186_s13643-017-0644-y` (optimal database combinations; "Stream read error"), `10.1186_s13643-024-02575-4`, `10.1186_s12874-025-02583-5`, `10.1186_s12874-021-01451-2` (AI for T/A screening guidance), `10.1186_s12874-020-01129-1`, `10.1186_s13643-018-0707-8`, `10.1186_s13643-019-1222-2`, `10.1186_s13643-023-02257-7`, `10.1186_s13643-024-02502-7`, `10.31234_osf.io_c93gq`, `10.31234_osf.io_r3m2d_v1`, `10.1186_s13643-019-1074-9`, `10.1186_2046-4053-3-74`, `10.1186_2046-4053-4-5`, `10.1038_s42256-020-00287-7` (ASReview), `10.1186_s13643-023-02255-9`, `10.1186_s13750-025-00374-5` & `10.11124_jbies-25-00480` (position statement full texts), `10.1186_s12916-015-0465-6` (scoping review of rapid review methods), `10.1186_s13643-016-0360-z`, `10.1186_1471-2288-13-48`, `10.1186_s12874-016-0116-4`, `10.1186_1472-6947-7-16` (PICO PubMed), `10.1186_2046-4053-1-2` (PROSPERO), `10.1186_s12874-017-0347-z`, `10.1371_journal.pone.0138237`, `10.5195_jmla.2019.567`, `10.5195_jmla.2021.962`, `10.1038_s41598-023-41032-5`, `10.2196_53164`, `10.64898_2026.04.02.26350091`, `10.1101_2025.08.11.25333429`, `10.1101_2025.11.03.25339455`, `10.48550_arxiv.2411.14199` (OpenScholar), `10.48550_arxiv.2409.13740`, `10.1145_2745802.2745818`, `10.1016_j.jclinepi.2017.10.023`, PRISMA 2020 duplicates (`10.1186_s13643-021-01626-4`, `10.1371_journal.pmed.1003583`, `10.31222_osf.io_v7gm2`, `10.31222_osf.io_jb4dx`). Check `catalog_read` before use — some may have converted after this file was written; the sibling reading pass (or a later one) should upgrade their status from "not read" to FT.

### 10.4 Not obtainable (NA / paywalled, abstract also not usable)
Cochrane Handbook ch. 4 (`10.1002/9781119536604.ch4`, abstract only 959 chars), Cochrane/Campbell/JBI/CEE position statement in `10.1002/14651858.ed000178` (no abstract), Tricco/Peters scoping extraction guidance (`10.11124/jbies-22-00123`, `jbies-21-00242`: abstract-level only), Kitchenham SE guidelines (`10.1145/1134285.1134500`, abstract 1 KB), Petersen mapping studies (`10.14236/ewic/ease2008.8`), Greig scoping-of-scoping (`10.1002/jrsm.1123`), Lancet fabricated-citation audit (`10.1016/s0140-6736(26)00603-3`, 289-char abstract), Cardiac Failure/JCMS ChatGPT-reference notes (`10.1016/j.cardfail.2023.06.015`, `10.1016/j.jcms.2025.08.004`), Mugaanyi-type Rapid Reviews tutorial (`10.1002/cesm.70092`), Responsible AI in rapid reviews (`10.1002/cesm.70063`, no abstract). **Not found/no download:** Elliott 2017 LSR guidance full text; PRESS 2015 full text (stored but empty conversion).

---

## 11. Five practices the skill must adopt
1. **Frozen protocol before search** with review type + justification, PCC/PICO question, eligibility, amendment log [P05, P06, P11, P10].
2. **Fully logged, seed-validated multi-source search** (verbatim queries, dates, counts) plus **iterated backward/forward citation chasing from included papers only** [P01 item 7, P04, P15, P18].
3. **Piloted, two-independent-pass screening with κ, reasons for every full-text exclusion, and a recall audit** — agent substitution for human dual screening is *not* validated in the literature read [P17, P18, P29, P38/P39 AB].
4. **Evidence-anchored extraction: every value carries a verbatim quote + stem/page; second-pass verification; null when absent** [P17, P20, P41 AB].
5. **Reference integrity + AI transparency**: nothing is cited unless it resolves to a real record; report tools, prompts, validation and human oversight per PRISMA 2020 automation items [P01, P24 AB, P26/P27 AB].
