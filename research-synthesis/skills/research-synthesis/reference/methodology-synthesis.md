# Evidence-synthesis methodology: appraisal, synthesis, certainty, insight

Scope: the **appraise → synthesise → grade → generate insight** half of the research-synthesis skill. Search/screening/reporting methodology lives in the sibling reference (search/screen/report), if present. Every practice below is tied to a source that was acquired and read **through home-still** (`paper_download` → `scribe_convert` → `distill_index`, text read with `markdown_read`; abstracts for paywalled items via `paper_get`). Nothing here comes from memory unless tagged `[INFERENCE]` or `[NOT VERIFIED]`.

Compiled 2026-10-02. Source keys `[S01]`…`[S62]` resolve in §9 to authors, year, title, DOI, **home-still stem** (`doc_id`, usable with `markdown_read` / `catalog_read` / `distill_search`) and read-status. Volume/page numbers are given only where they appeared in the text that was read.

Read-status legend (used throughout):
- **FT** = full text read via `markdown_read` (sections named in each cite).
- **FT-part** = full text in corpus; only the cited passages were read.
- **AB** = abstract only, obtained via `paper_get` (home-still could not download the full text — paywalled). Claims from AB sources are limited to what the abstract states.
- **NA** = not obtainable through home-still; mentioned only so the skill knows the gap.

---

## 0. One-screen decision spine (what the skill does, in order)

1. **Classify the question** (§2.0): exposure–outcome association / effect of intervention / lived experience / measurement / mechanism-in-context / mixed. Pick the *logic*: **aggregative** (add up and average predefined concepts) vs **configurative** (arrange and interpret to build concepts/theory) vs both [S16, S19, S20].
2. **Split evidence into streams** by design (RCT, non-randomised, cross-sectional/correlational, diagnostic/psychometric, qualitative, mixed-methods, reviews). One appraisal tool per stream (§1). Never one score for everything.
3. **Appraise domain-by-domain, no summed scores** (§1.6) — and *do not use appraisal to hide relevant-but-imperfect evidence from an interpretive synthesis*; use it to weight and to run sensitivity analysis [S02, S08, S10, S27].
4. **Synthesise each stream with a named, reportable method** (§2): SWiM for quantitative-without-meta-analysis; thematic / best-fit framework / meta-ethnography / CIS for qualitative; realist CMO for mechanisms; JBI convergent-segregated or -integrated for mixed streams.
5. **Grade certainty per finding, not per review** (§4): GRADE-style for effect findings, CERQual-style for qualitative/interpretive findings; written reasons, no numeric score.
6. **Generate insight** (§5) with a line-of-argument / synthesising argument built from *synthetic constructs*, forced through refutational translation and competing-theory tests; present as a conceptual model whose every arrow cites stems.
7. **Run the hazard checklist** (§6) and the autism/neurodiversity participatory-ethics checklist (§7) when the topic touches autistic people.
8. **Report** with SWiM items + qualitative reporting items (ENTREQ/eMERGe/RAMESES-style) in a methods appendix [S01, S12, S11].

---

## 1. (a) Appraisal: tool selection by study design, and the domains each tool checks

### 1.1 Selection table

| Evidence unit | Tool | Domains / items (as read) | Output | Source (status) |
|---|---|---|---|---|
| Randomised trial (parallel group) | **RoB 2** | 5 mandatory domains: bias arising from the randomisation process; deviations from intended interventions; missing outcome data; measurement of the outcome; selection of the reported result. Signalling questions (Y / PY / PN / N / NI) feed an algorithm; free-text support quotes required. Applies to a *result*, not a study. | Per domain: low risk / some concerns / high risk; overall judgement per result | [S23] FT (§Domains, Table 1, Signalling questions); Cochrane Handbook ch. 8 [S39] AB |
| Non-randomised study of an *intervention* | **ROBINS-I** | 7 domains: confounding; selection of participants into the study; classification of interventions (the first three are pre-intervention/at-intervention); deviations from intended interventions; missing data; measurement of outcomes; selection of the reported result. Starts by specifying a **target trial** (population, intervention, comparator, outcome) and listing confounders/co-interventions *in advance*. 6 steps; steps 3–6 repeated per outcome. | Per domain and overall: low / moderate / serious / critical / no information. "Judgement" not score. | [S24] FT (§Domains of bias, Table 1–2, steps); Handbook ch. 25 [S40] AB |
| Non-randomised study of an *exposure* (cohort; "does X cause Y?" with X not assignable) | **ROBINS-E** | Developed for cohort studies of the causal effect of an exposure on an outcome (tool structure not read). | — | [S41] AB only (`paper_get`) — full text paywalled; **do not claim domain list** |
| Observational (cohort / case-control) | **Newcastle-Ottawa Scale (NOS)** | Up to 9 points in three domains: selection of study groups (4), comparability of groups (2), ascertainment of exposure/outcome (3), for case-control and cohort versions. Most commonly used tool for cohort and case-control studies and can be modified by users [S68]. In a study of cohort studies in an influenza review, reviewer-vs-author agreement on NOS items was "remarkably low" (highest item κ = 0.15) → contact authors for unreported methodological details [S69]. | Stars per item — **do not sum into an inclusion rule** | [S68] FT-part; [S69] FT-part; [S27] FT-part (scales unreliable) |
| Cross-sectional / correlational | **AXIS** (appraisal tool for cross-sectional studies) | Listed as the cross-sectional tool in the tool overview [S68]; item list not read (the AXIS development paper [S70] was downloaded but its text was not read in this pass). Most "connection between A and B" literatures are cross-sectional/correlational, so the agent must at minimum code: sampling frame, measurement validity of exposure and outcome, confounder adjustment, and non-response [INFERENCE — not an AXIS item list]. | — | [S68] FT-part; [S70] see §9.2 |
| Diagnostic accuracy / test-based measurement | **QUADAS-2** | 4 domains: patient selection, index test, reference standard, flow & timing. First 3 domains also rated for *applicability* concerns. Applied in 4 phases: state review question → tailor tool & write review-specific guidance → flow diagram of primary study → judge bias & applicability. | Low / high / unclear per domain | [S42] AB (abstract delivered as the whole "document"; 4.6 KB) |
| Systematic review / meta-analysis used as evidence | **AMSTAR 2** | 16 items; 7 **critical** domains: protocol registered before review (2); adequacy of literature search (4); justification for excluding studies (7); risk of bias of included studies (9); appropriateness of meta-analytic methods (11); RoB considered when interpreting results (13); assessment of publication bias (15). **No overall score.** | Overall confidence: High (0–1 non-critical weakness) / Moderate (>1 non-critical, no critical flaw) / Low (1 critical flaw) / Critically low (>1 critical flaw) | [S25] FT (§Identification of critical domains, Box 1, Box 2, §Discussion) |
| Systematic review (alternative) | **ROBIS** | — | — | [S43] AB |
| Qualitative primary study | **No consensus tool.** Options actually read: (i) CASP-style checklists (see [S14] Toye: used CASP scored 10–30, found low inter-rater agreement, "tools focus on methodological rather than conceptual strength"); (ii) CIS 5 prompts [S02 Table 1]; (iii) reporting-based minimal criteria [S09, S10]; (iv) CERQual methodological-limitations component, applied *per finding* [S06]. | CIS prompts: aims clear? design appropriate to aims? clear account of process by which findings were reproduced? enough data displayed to support interpretations? analysis appropriate and explicated? Best-fit minimal criteria: is each of (question/design, recruitment/selection, data collection, data analysis) clearly described? "Better-reported" = ≥2 of the four described | Fatally flawed / not (CIS); adequately vs inadequately reported (best-fit); concern level per finding (CERQual) | [S02] FT, [S09] FT, [S10] FT, [S06] FT, [S14] FT-part. CASP-specific papers (Long 2020; Majid & Vanstone 2018) **NA** |
| Mixed-methods / any design in one review | **MMAT (2018)** | Developed 2006; revised 2018 after usefulness testing, tool review and modified e-Delphi; appraises qualitative, quantitative and mixed-methods studies. Rationale: an MM study "is more than just the sum of the individual qualitative and quantitative strands", so applying separate qualitative and quantitative criteria "is most likely not sufficient" — MM-specific criteria for the integration are needed [S66]. Full MMAT criteria **not read**. | — | [S44] AB; [S66] FT-part |
| Case series / case reports / qualitative / text & expert opinion / reviews (JBI) | **JBI critical appraisal checklists** | Tool overview: JBI checklists exist for qualitative research, case reports, text and expert-opinion papers ("only the JBI has" one for the latter) and for systematic reviews/research syntheses; CASP qualitative is "the most frequently recommended" for qualitative studies; for reviews AMSTAR 2 "most commonly used" and ROBIS "most frequently recommended" [S68]. **Case-series checklist (10 questions, read)**: clear inclusion criteria; condition measured in a standard, reliable way; valid methods of identifying the condition; consecutive inclusion; complete inclusion; demographics clearly reported; clinical information clearly reported; outcomes/follow-up clearly reported; presenting-site demographics reported; appropriate statistical analysis. The JBI authors **advise against cut-off scores or tallying "yes" answers** because the questions are not equal; present all answers in a table; ideally two reviewers [S71]. Other JBI checklists' item lists **not read**. | Table of answers, no score | [S68] FT-part; [S71] FT |
| Qualitative *synthesis* output | **CERQual** (not an appraisal of a study — see §4) | | | [S03–S07] FT |

### 1.2 Addendum: tools whose primary papers were paywalled
Newcastle-Ottawa primary description (Wells), Stang 2010 and Luchini 2017 critiques, CASP primary papers (Long 2020; Majid & Vanstone 2018), JBI manual chapters, the MMAT 2018 primary paper and the ROBINS-E full text were **not** downloadable through home-still ("No open-access PDF found"). The skill must therefore (i) not reproduce their full item lists from memory, and (ii) when a user needs them, tell the user which DOI to obtain. What home-still did yield on these tools is limited to secondary reads: the tool overview [S68], the NOS agreement study [S69] and the MM appraisal-framework review [S66] (§9.2).

### 1.3 Appraise the *result* and the *finding*, not just the paper
- RoB 2 and ROBINS-I are applied "for the result being assessed" and ROBINS-I steps 3–6 repeat "for each key outcome" [S23, S24]. CERQual says the same for qualitative evidence: "How a primary study was conducted may constitute a methodological limitation for one review finding but not for another" (focus groups bad for sensitive topics, fine for others) [S06 §Guidance; S03 §Methodological limitations].
- Implication [INFERENCE]: the extraction schema keeps one appraisal record **per study × outcome/finding**, not one per paper.

### 1.4 Signalling questions, judgement, and "no information"
- RoB 2 and ROBINS-I derive domain judgements from factual *signalling questions* with an explicit "no information" option; reviewers may override the algorithm but must justify [S23 §Signalling questions; S24 steps 4–6].
- ROBINS-I: "judgement" is deliberate wording — "the severity of the bias in a particular domain and the relative consequences of bias in different domains" matter [S24 §risk of bias judgements]. It also states a **critical risk of bias in any one domain → critical overall** (Table 2) [S24].

### 1.5 What to do with weak studies
| Position | Evidence |
|---|---|
| Exclude only "fatally flawed" qualitative papers; about 20 of 119 papers were so excluded in CIS because "even weak papers were often judged to have potentially high relevance"; prioritise "signal" (relevance) over "noise" | [S02 §Determination of quality] |
| Include all relevant studies; code reporting adequacy; run **sensitivity analysis** (does dropping "inadequately reported" studies change any theme?). In the case study 3/15 studies were inadequately reported and removing them removed no theme and added little unique | [S09, S10 §Testing the synthesis: … sensitivity] ; [S08 §Quality assessment: poorer-quality studies "contributed comparatively little"] |
| Quality-scale scores are unreliable; Cochrane discourages scales; a quality tool should not decide inclusion; look separately at a few workable bias indicators instead of a summary score | [S27 §Study Quality] |
| Appraisal tools for qualitative work show low inter-rater agreement and measure method, not conceptual contribution | [S14 §Quality appraisal] |
| Idealist (interpretive) synthesis methods: appraisal "less clear, less a priori; quality of content rather than method"; realist methods: "clear and a priori" | [S15 Table 1] |

### 1.6 Rules the skill adopts for appraisal
1. Choose the tool from the **study's design**, written down in the protocol, not from the topic [S26 §Review typology; S16].
2. Record domain judgements + a **supporting quote** + a `NI` (no information) flag; never invent a judgement the paper does not support (RoB 2 asks for "brief direct quotations from the texts of the study reports" [S23]).
3. **No summed quality score.** AMSTAR 2 says responses "should not be used to derive an overall score" [S25]; JBI advises against cut-offs because "the critical appraisal questions are not all 'equal'" and tallying 'yes' answers "does not truly give an accurate indication of the specific problems of a study" [S71]; CERQual "do[es] not recommend attempting to numerically score" components [S05]; Siddaway et al. advise against scales [S27].
4. Appraise *reviews* you plan to rely on (AMSTAR 2 critical domains) before treating their conclusions as evidence: a review with a critical flaw "may not provide an accurate and comprehensive summary", and one with more than one "should not be relied on" [S25 Box 2]. Treat such a review (and any LLM-written summary) as a lead to the primary studies, not as a finding `[INFERENCE for the LLM clause]`.
5. Hold "relevant but weak" evidence in the interpretive synthesis with a label and test sensitivity, instead of silently dropping it [S02, S09, S10].

---

## 2. (b) Choosing the synthesis method — decision table

### 2.0 First decision: aggregate or configure?
- **Aggregative** reviews "add up and average empirical observations … within predefined conceptual positions"; they search exhaustively for a representative sample, expect homogeneous data, treat theory before/after rather than during the review, and assess quality against a-priori criteria. **Configurative** reviews "interpret and arrange" information and develop concepts; they sample for variation (theoretical sampling), iterate, and may prioritise relevance/contribution over method quality [S16 §Aggregative and configurative reviews].
- Sandelowski's version: aggregation = "thematically similar findings … confirmatory … averaging, merging … product: pooled summary"; configuration = "thematically dissimilar findings … complementary … linking, meshing … product: theory, model". "Sets of aggregated findings can be configured, but configured findings cannot be aggregated." Neither logic is "preferable"; "the nature of the research findings to be synthesized" decides [S19 Table 1].
- Most real reviews contain both [S16].
- For a "connection between A and B" topic [INFERENCE]: quantitative associations are aggregated (what is the evidence of association, how large, how certain); *why/how* (mechanism, moderators, interpretation by the people concerned) is configured. The deliverable needs both, plus an integration step (§3.8).

### 2.1 Decision table

| Evidence type / question | Preferred method | Why / conditions | Certainty tool | Source |
|---|---|---|---|---|
| Homogeneous quantitative effects, extractable effect sizes | Meta-analysis ("preferable" per Cochrane ch. 12; appropriate when studies examine same/similar constructs, similar designs, report standardised-effect-convertible results) | Others in this table are fallbacks | GRADE | [S27 §Meta-Analyses]; ch. 12 [S38] AB |
| Quantitative, heterogeneous or incompletely reported, **no** meta-analysis | **SWiM** (9 items): group → metric → method → prioritisation criteria → heterogeneity → certainty → display → results → limits | Choice of metric/method fixes the *question answered* (direction-of-effect vote counting answers "is there any evidence of an effect?" not "what is the average effect?") | GRADE-style, consistency domain "may be difficult" with vote counting | [S01 §Items 1–9, Table 2, §Discussion] |
| Many diverse quantitative studies of an association (correlational/cross-sectional/experimental), concept names unstable | Narrative review / structured narrative synthesis anchored on a theory | "particularly useful means of linking together studies on different topics … to develop or evaluate a new theory" (Siddaway on Baumeister & Leary); but voluntary transparency (SWiM) still applies. Popay's four elements: develop a theoretical model → preliminary synthesis → explore relationships → assess robustness (as paraphrased by Hong 2017; Popay 2006 itself **NA**) | CERQual-like per-finding profile or GRADE-like if effect estimates | [S27 §Narrative Reviews]; [S17 §Discussion]; Rodgers 2009 [S46] AB |
| Lived-experience / interview studies; want **actionable themes**, stay close to data | **Thematic synthesis** (3 stages: line-by-line coding → descriptive themes → analytical themes "go beyond") | Transparent, supports sensitivity analysis by study | CERQual | [S08] |
| Qualitative; **a relevant model/theory already exists** and time is limited | **Best-fit framework synthesis**: find model(s) systematically → build a priori framework → code → thematic analysis of unaccommodated data → new framework → conceptual model → test against original models, dissonance, sensitivity | "rapid, transparent, pragmatic"; only viable if an adequate model exists; combined positivist+interpretive | CERQual | [S09], [S10] |
| Qualitative; want **new concepts/theory**; ≤ ~40–50 well-defined studies (up to 77 achieved) | **Meta-ethnography** (7 phases; reciprocal translation, refutational translation, line of argument); report with eMERGe | Keep first-/second-/third-order constructs distinct | CERQual | [S12 Phases 1–7; criteria 11–17], [S13], [S14] |
| Large, diverse, multi-method literature; the concept itself is contested; want critique of how the field frames the problem | **Critical interpretive synthesis (CIS)** | Iterative, theoretical sampling, "critique" rather than only appraisal; output = synthesising argument built from synthetic constructs | CERQual (applied to findings) | [S02] |
| Complex social phenomena; "what works for whom, in what circumstances, how, why"; mechanisms | **Realist synthesis**: elicit programme/middle-range theory → context–mechanism–outcome (CMO) configurations, demi-regularities → test and refine against all kinds of evidence. Four synthesis tasks: question the *integrity* of a theory; *adjudicate between competing theories*; consider the same theory in *comparative settings*; compare the "official" theory with *actual practice* | Conventional reviews of complex interventions "often result in limited answers such as 'to some extent' and 'sometimes'"; realist search and appraisal are purposive and theory-driven, with high stakeholder involvement; no deterministic theory predicts outcomes in every context | CERQual-like per CMO claim [INFERENCE] | [S11], [S64]; Pawson 2005 [S47] AB |
| Topic conceptualised and studied differently by different research groups (psychology vs psychiatry vs neuroscience vs community scholarship) | **Meta-narrative review**: identify research traditions (Kuhnian paradigms: shared concepts, theories, methods, instruments); for each ask how the topic is conceptualised, the key theories, the preferred designs/"ways of knowing", the main empirical findings; apply each tradition's own quality criteria within the tradition; synthesise by an over-arching narrative | "Pluralistic rather than normative" — asks what can be learned from the range of approaches, not which is best; suited to exploring tensions between traditions | CERQual-like per finding [INFERENCE] | [S48] FT-part; [S15] |
| Both effects and meanings/experience of one phenomenon | **Mixed-methods review**: *convergent segregated* if the streams answer *different aspects* of the phenomenon (separate syntheses → integrate); *convergent integrated* if both can answer the *same* question (transform e.g. 'qualitise' quantitative data, pool, then thematically categorise) | Data-based / results-based / parallel-results convergent designs; sequential designs when one phase informs the other | GRADE for effect stream + CERQual for qualitative stream, then integration matrix | [S18 §Convergent integrated/segregated], [S17 §Synthesis of results], [S21] |
| Existing systematic reviews are the evidence | **Umbrella review / overview** | Only highest-level evidence (reviews/MAs) included; compare and contrast | AMSTAR 2 / ROBIS for inputs | Aromataris 2015 [S49] AB; [S25] |
| Question about *what a construct/measure is* (heterogeneous measures) | **Psychometric review** (COSMIN); then restrict synthesis by measure | PEO / PICo / PIRD / CoCoPop mnemonics per question type | — | [S26 §Psychometric reviews, Table 1] |
| Exposure–outcome ("is A connected to B?") | **Etiology/risk review** (PEO) with observational studies; MOOSE in addition to PRISMA | Causal claims need triangulation across designs with different biases (§6.5) | GRADE + ROBINS-E/ROBINS-I | [S26 §Etiology], Lawlor 2016 [S50] AB, Hammerton & Munafò 2021 [S51] |

### 2.2 Epistemology matters for method choice
Methods split into **idealist** (meta-ethnography, meta-narrative, CIS, meta-study, grounded theory: iterative search, less a-priori quality assessment, problematise the literature, complex outputs for researchers/theorists) and **realist** (thematic, framework, textual narrative, ecological triangulation: linear search, clear a-priori appraisal, clear outputs for practitioners). "It is generally a question of degree." The more idealist, the more iteration [S15 Table 1, §Looking across dimensions]. Methods also differ in how far they "go beyond" the primary studies: textual narrative / ecological triangulation / framework synthesis mostly **describe and summarise**; meta-ethnography, grounded theory, thematic synthesis, meta-study, meta-narrative and CIS "push beyond the original data to a fresh interpretation" [S15 §Going 'beyond' the primary studies].

### 2.3 Match the review frame to the question type
Munn et al. give per-type frames: effectiveness (PICO), experiential/qualitative (PICo), prevalence (CoCoPop), diagnostic accuracy (PIRD), **etiology/risk (PEO, exposure, population, outcome; use MOOSE in addition to PRISMA)**, expert opinion/policy (PICo), **psychometric (COSMIN)**, prognostic (QUIPS, CHARMS), methodology reviews (SDMO) [S26 §Review typology]. A topic like "connection between X and Y" must choose etiology/risk (PEO) and, if construct definitions are unstable, a psychometric/construct-mapping pre-step [INFERENCE].

---

## 3. (c) Executable procedures

### 3.1 Popay's four elements (narrative synthesis)
Popay et al. 2006 (ESRC methods programme guidance) was **not obtainable** through home-still. What was read: its four main elements are **develop a theoretical model of how the intervention/phenomenon works and for whom; develop a preliminary synthesis; explore relationships within and between studies; assess robustness of the synthesis** (paraphrase in [S17 §Discussion]); a test of the guidance found "conclusions of the two syntheses were broadly similar" to a meta-analysis of the same data, but conclusions about moderators of effect appeared stronger from the meta-analysis while implications for future research appeared more extensive from the narrative synthesis [S46 abstract]. A methodological assessment of a 20% random sample (446) of public-health effectiveness reviews found 56% (251) used narrative synthesis, and examined reporting of methods, investigation of heterogeneity, transparency of data presentation and assessment of robustness; its title concludes "lack of transparency" [S52 abstract]. A within-review comparison (plain tobacco packaging) found multilevel meta-analysis agreed in direction with the narrative synthesis (d = −0.59, 95% CI −0.71 to −0.47 on 7 of 19 eligible studies) but the methods differed in "the role of judgement and contextual variation", in precision versus breadth, and in how they treated heterogeneity and consistency [S63]. The specific tools Popay lists inside each element (tabulation, grouping, vote counting …) are `[NOT VERIFIED]` — do not cite them as Popay unless the full guidance is later acquired.

Agent procedure `[INFERENCE]` from the four elements + SWiM:
1. Write the theory/logic model (assumed pathway, moderators, population) **before** reading results; revise it on evidence (SWiM item 1 encourages a logic model for the groupings [S01 §Item 1]).
2. Preliminary synthesis: tabulate studies (design, N, population, measure, direction, effect, appraisal) in a fixed schema.
3. Explore relationships: organise tables by hypothesised modifiers (design, subgroup, setting, measure) — SWiM item 5 calls this "informal methods to investigate heterogeneity" and warns they are "rarely definitive" and must be flagged as not pre-specified [S01 §Item 5].
4. Assess robustness: sensitivity to inclusion of weak studies; check for missing results (§6); state certainty.

### 3.2 SWiM — the 9 reporting items an agent must populate [S01 Table 1, §Items 1–9]
1. **Grouping studies for synthesis** — (1a) describe and justify groups (populations, interventions/exposures, outcomes, designs); (1b) report and justify any change from the protocol. Use a logic model/theory of change to justify groups.
2. **Standardised metric & transformation** — what common metric (effect measure, direction of effect, p-value) and how converted.
3. **Synthesis method** — name and justify (summarising effect estimates; combining p-values; vote counting by direction of effect — Table 2 maps each to the question it answers).
4. **Criteria used to prioritise results** — design, risk of bias, sample size, relevance/directness, certainty; pre-specify to limit selective reporting.
5. **Heterogeneity** — method used to explore variation when no meta-regression/subgroup test is possible; limit, flag as post-hoc.
6. **Certainty of evidence** — method (GRADE usual); note some domains (consistency under vote counting) are hard to assess.
7. **Data presentation** — tables, forest plots, harvest plots, effect direction plots, albatross plots, bubble plots, box plots; order tables the same way as the narrative; order by key characteristics (design, RoB).
8. **Reporting results** — per comparison/outcome: synthesised finding + certainty, consistent with the question; which studies contribute; N studies and participants; key characteristics.
9. **Limitations** — of the metric, method, regrouping; post-protocol changes.
Notes: SWiM is a *reporting* guideline, "not … appropriate … to guide the conduct" and not for qualitative synthesis (use ENTREQ, eMERGe) [S01 §Discussion].

### 3.3 Thematic synthesis [S08 §Detailed methods; §Stage three; §Context and rigour]
1. Line-by-line free coding of the *findings/results text* of each study, coded by meaning and content (3 reviewers coded independently in the worked example).
2. Group free codes in a hierarchical tree → **descriptive themes** ("close" to the primary studies; 12 in the example).
3. Generate **analytical themes**: ask the *review question* of the descriptive themes, infer barriers/implications, and "go beyond" the findings — new constructs, explanations, hypotheses (example: "Children do not see it as their role to be interested in health"; 6 analytical themes → 10 intervention recommendations).
4. Preserve context (structured study summaries; check whether themes attach to subgroups/settings; note restricted contextual reporting).
5. Sensitivity: examine which studies contribute to which themes; poorer-quality studies contributed little and held few unique themes.

### 3.4 Best-fit framework synthesis [S09, S10]
1. Systematically search for **existing models/theories** relevant to the behaviour/phenomenon (iterative, purposive; "not the systematic identification of all such models").
2. Extract concepts from the model(s) → **a-priori framework** with *explicit definitions* per theme (needed because coders otherwise code the same data to different themes [S09 §Lessons]).
3. Extract data from Results sections (verbatim participant quotes or author findings clearly backed by data); two coders against the framework.
4. Data that fit no theme → **secondary thematic analysis** → new themes; team agrees a final list (map new themes onto old where possible — "c.p. reciprocal translation").
5. Stage 1: new framework (list of defined themes: supported a-priori + new). Stage 2: revisit evidence to establish **relationships among themes** → conceptual model/diagram + narrative that cites studies.
6. **Test the synthesis**: compare with the original models (gap), explore dissonance/disconfirming cases ("uncomfortable evidence … should always be assessed"), and run quality-based sensitivity analysis [S10 §Testing the synthesis].
7. Output can be turned into a hypothesis / programme theory for empirical testing [S10].

### 3.5 Meta-ethnography (Noblit & Hare, 7 phases) and eMERGe [S12, S13, S14]
Phases: 1 getting started/selecting meta-ethnography; 2 deciding what is relevant; 3 reading studies; 4 determining how studies are related; 5 translating studies into one another; 6 synthesising translations (including line-of-argument); 7 expressing the synthesis [S12; S13 Steps 1–6 headings].
- Distinguish **first-order** (participants' constructs), **second-order** (study authors' interpretations), **third-order** (reviewers' syntheses) and say whose interpretation is presented [S12 criteria 13–14; S13 Table 4].
- Phase 4: compare design aspects, findings (meaning of concepts/metaphors/themes; overarching storyline) and context (time period etc.); describe the comparison method; report **disconfirming cases** [S12 criteria 11–12].
- Phase 5: state working definitions of **reciprocal** and **refutational** translation; "refutational translation is often overlooked; its purpose is to explain differences and … exceptions, incongruities and inconsistencies"; one can do both [S12 criterion 12–13].
- Phase 6: develop synthesised translations, then a **line-of-argument** — "a fresh interpretation … goes further than translation and puts any similarities and dissimilarities into a new interpretive context"; document who was involved and how alternative perspectives were considered; state the context where the theory does *not* apply [S12 criteria 15–16].
- Scale: Atkins (44 studies) found chronological study-by-study translation impractical when themes varied and used thematic categories first; Toye (77 studies, 450 concepts) used collaborative interpretation of every second-order construct, piles of similar concepts by constant comparison, then a line of argument. "If you don't [have enough data for a robust conceptual category] your analysis represents a catalogue or 'aggregate' of findings" [S13 §Step 5; S14 §Analysis, §How many studies]. CIS found reciprocal translational analysis suited to ≤ ~50 stable studies [S02 §Reciprocal translational analysis].

### 3.6 Critical interpretive synthesis (CIS) [S02]
1. Review question is "tentative, fuzzy and contested at the outset" — formulate, keep open to modification; defer final definitions of key constructs.
2. **Sampling**: purposive first, then theoretical sampling to "add, test and elaborate the emerging analysis"; searching is iterative, includes literatures "not directly or obviously relevant".
3. Quality: five appraisal prompts; exclude only "fatally flawed"; defer credibility/contribution judgements to the synthesis (~20/119 excluded).
4. Extraction: summary-level; formal extraction "unlikely to be an essential feature".
5. Analysis ≈ primary qualitative analysis/grounded theory: detailed reading → recurring themes + **critique** (of assumptions, how the literature constructed the problem, what shaped proposed solutions) → categories and relationships → **synthesising argument** linking *synthetic constructs* (new, generated by transforming evidence into a new conceptual form) with existing second-order constructs.
6. Constant reflexivity; a multidisciplinary team gave "checks and balances".
7. Output: a coherent theoretical framework (network of constructs and relations); "demonstrably grounded in the evidence" though "not strictly reproducible".
8. Limits: not stage-wise; reproducibility lower; evaluate in other contexts. Worked outcome: concept of **candidacy** (+ permeability, adjudication, offers) re-framed "access to healthcare" from utilisation counts to a negotiated property.

### 3.7 Realist synthesis and RAMESES [S11]
- Starting point: program theory — how and why a class of intervention is thought to work; ideas re-cast as **context (C) – mechanism (M) – outcome (O)** configurations; question "what works for whom under what circumstances, how and why?"
- Mechanism = "underlying entities, processes, or [social] structures which operate in particular contexts to generate outcomes"; mechanisms involve "the interaction between … inputs (or resources) and human reasoning".
- Analyse recurrent **demi-regularities** (patterns of outcomes with associated contexts and mechanisms); results are **middle-range theories**.
- Appraisal is of *pieces of data* by relevance and rigour, not whole documents; selection and appraisal run in parallel with analysis; transparency by worked examples, quotes, and "an exploration of disconfirming data".
- Example refinement: "synergy is both an outcome and a context for partnership development" (outcome of one cycle becomes the context for the next).

### 3.8 Mixed-methods integration [S17, S18, S19, S20, S21]
- **Designs**: convergent (data-based: same method for all after transformation; results-based: analysed separately, then integrated by another method, e.g. tables/matrices/juxtaposition; parallel-results: separate, integrated in Discussion) vs sequential (one phase's results inform the next); Sandelowski's terms segregated / integrated / contingent map onto these [S17 §Synthesis of results].
- JBI (2020): choose **convergent integrated** when both qualitative and quantitative studies can answer the same question (e.g. barriers/enablers); **convergent segregated** when they address different aspects (effects vs experience). JBI 'qualitises' quantitative data (less error-prone than quantitising). Integration questions: does qualitative evidence explain why an intervention is/is not effective? does it explain differences in direction/size of effect? which aspects of each stream are/are not tested in the other? are the syntheses supportive or contradictory? [S18].
- Report: justify the mixed design; name methods with references; describe how integration happened and the *insight gained*; (only 39% of reviews described methods fully; 24% justified mixing) [S17 §Implications].
- **Fit of integration** (Fetters 2013): *confirmation* (greater credibility), *expansion* (complementary aspects: e.g. strength of association vs nature of association), *discordance* (resolve by checking bias, methodological assumptions, new data/re-analysis, theory explanation, or challenging construct validity). **Joint displays**, weaving (theme-by-theme), contiguous, staged narrative [S21 §Interpretation and reporting; §Fit].
- Practical contrast [S20]: in the quantitative stream the same variable "operating in opposing ways" yields a null main effect; qualitative findings can reveal the opposing mechanisms — a standard source of insight when pooled quantitative results look null/inconsistent. Quantitative findings translated into qualitative reference frames ("factors favouring X / not X") worked better than the reverse.

### 3.9 Vote counting: allowed form and pitfalls
See §6.2.

---

## 4. (d) Certainty: GRADE domains, CERQual components, and a per-finding rating procedure

### 4.1 GRADE (effect-estimate findings)
Read in full: GRADE Working Group 2004 [S22 §Quality of evidence for each important outcome, Box 2, §Combining the four components]. Abstract-level only for the 2011 J Clin Epidemiol series [S53–S58 AB].
- Unit: **each important outcome** (not each study, not the whole review); question must name options compared, population, setting [S22 §Definitions].
- Start: randomised trials = high; observational = low; other = very low [S22 Box 2].
- **Rate down**: study limitations (serious −1 / very serious −2); inconsistency (−1) — judged by direction, size, significance of differences; "important unexplained inconsistency"; unexplained → report separately for subgroups only with a compelling explanation; indirectness (some −1 / major −2) — population, intervention, outcome (surrogates), indirect comparisons; imprecision/sparse data (−1; later series: use 95% CI and decision thresholds [S58 AB]); reporting/publication bias (−1; suspect when evidence is a few small, commercially funded studies; funnel plots have "substantial limitations" [S54 AB]).
- **Rate up** (observational): strong association RR>2 or <0.5 consistent, no plausible confounders (+1); very strong RR>5 or <0.2 (+2); dose–response (+1); all plausible confounders would reduce the effect (+1) [S22 Box 2; S55 AB].
- Levels: **High** (further research very unlikely to change confidence), **Moderate**, **Low**, **Very low** (any estimate very uncertain) [S22 §Combining].
- Caveats for an agent: GRADE is for effect estimates; it is *not* appropriate for qualitative evidence [S03 §Introduction]. Under SWiM, "assessing some domains … may be difficult" when vote counting [S01 §Item 6].

### 4.2 GRADE-CERQual (qualitative/interpretive findings)
Read in full: [S03] (2015 PLoS Med), [S04–S09 series 2018]. A **review finding** = an analytic output describing a phenomenon or aspect of it; descriptive or interpretive; CERQual is applied to *each finding*, never to the whole synthesis [S03 Box 1; S05].

Four components (equal weight; analogies to GRADE in brackets):
| Component | Definition (as read) | Threats / how to assess |
|---|---|---|
| **Methodological limitations** [≈ risk of bias] | Problems in design or conduct of the primary studies contributing to the finding | Use a design-appropriate appraisal tool; no hierarchy of qualitative designs; judge each study's *relative contribution* (one seriously limited study supplying most data → serious concern); is the limitation relevant to *this* finding? (privacy/sensitivity, social desirability, Hawthorne, researcher effects); consider missing information [S06 §Guidance] |
| **Coherence** [≈ inconsistency] | How well the finding is grounded in and explains the pattern in the data | Three threats: (a) **contradictory data**/outliers, (b) **ambiguous or incomplete data** (vague measures; elements defined differently across studies; gaps in support for parts of an explanation), (c) **competing theories**/plausible alternative explanations not explored; actively look for data that complicate the finding; check for "smoothing out" or stretching an explanation; a cogent explanation of the disconfirming data is *not* a threat [S07 §Guidance, Table 1; S03] |
| **Adequacy of data** [≈ imprecision, as stated in S07b] | Richness *and* quantity of data supporting the finding | Judge relative to the claim made; no fixed numbers; richness = detail sufficient to interpret meaning and context; quantity = number of studies and participants; consider saturation and disconfirming cases [S07b; S03] |
| **Relevance** [≈ indirectness, as stated in S07c] | Applicability of the supporting studies' context (perspective/population, phenomenon, setting) to the review question | Three threats: **indirect**, **partial**, **unclear** relevance; assess each study against the review-question context; needs subject knowledge; this is "internal relevance" to the review question, not a claim of transferability [S07c] |

Procedure [S03 §Making an Assessment; S05]:
1. Write the finding as an **explicit proposition** — "a hypothesized connection or pathway between factors should not be implied but … described clearly"; avoid unneeded contextual clutter in the summary [S05 Table 1–2].
2. List contributing studies (with data extracts) per finding.
3. Assess each component with a level of concern: **no/very minor, minor, moderate, serious**, each with a written explanation. (Minor "probably will not lower confidence"; serious "likely to"; moderate "may lead us to consider lowering … where there are also concerns in other components".)
4. Overall confidence: **high, moderate, low, very low**; all findings start at *high* and are rated down; avoid **double downgrading** the same concern across components; **no numeric scoring** ("false sense of precision") [S03; S05].
5. Output: **CERQual Evidence Profile** (finding + component assessments + overall + explanation) and **Summary of Qualitative Findings** table.
6. At least **two reviewers** discussing each assessment is preferred over one [S03 §General considerations; S05] — `[INFERENCE]` agent mapping: two independent passes (e.g. writer + adversarial verifier with access to the same stems) with disagreements logged.
7. State how future research could resolve concerns; dissemination bias is a plausible additional component but no methods exist yet [S03 Box 2].
- Useful findings with serious coherence concerns may still be reported if novel, about marginalised experience, or rare — flag, don't suppress [S07 §Balancing coherence and utility].

### 4.3 A per-finding certainty record the skill should emit `[INFERENCE]` (assembled from the above)
```
finding_id:           F-07
statement:            explicit proposition (no implied pathways)
logic:                aggregative | configurative
stream:               quantitative | qualitative | mixed
supporting_stems:     [..]  (with relative contribution)
contradicting_stems:  [..]  (disconfirming cases)
appraisal:            per-study domain judgements w/ quotes (RoB2 | ROBINS-I | ... | CIS prompts)
rating framework:     GRADE (start, down/up reasons) | CERQual (4 components, concern levels)
overall certainty:    high | moderate | low | very low
reasons:              one sentence per downgrade, de-duplicated across components
what would change it: concrete study/data type
```
Mixed findings (a quantitative association + a qualitative mechanism): rate each stream with its own framework, then state the **integration fit** (confirmation / expansion / discordance) [S21]; no single mixed-methods certainty instrument was found in the sources read [INFERENCE: report both and the fit].

---

## 5. (e) How the literature generates insight beyond aggregation

This is the part that turns a meta-survey into an argument. The methods above agree on a common move: **separate what the studies said (descriptive/second-order) from what the synthesis says (analytical/third-order/synthetic), and make the second layer explicit, grounded and testable.**

### 5.1 The vocabulary the skill uses
| Term | Meaning | Source |
|---|---|---|
| First / second / third-order constructs | participants' understandings / authors' interpretations / reviewers' synthesis of both into a new model or theory | [S13 Table 4; S12 criterion 14] |
| Reciprocal translation | matching themes/concepts across studies so they can "stand in" for each other | [S13; S12; S02] |
| Refutational translation | characterising and *explaining* contradictions and exceptions between studies | [S12 criterion 12–13; S02 (argues to fold it into the synthesising argument)] |
| Line-of-argument synthesis | a fresh storyline/overarching explanation that "goes further than translation" | [S12 criterion 15; S02; S13] |
| Synthetic construct | a construct produced by transforming the evidence into a new conceptual form; may be linked with existing second-order constructs in a **synthesising argument** | [S02 §Lines of argument; Table 2] |
| Analytical theme | thematic-synthesis output where reviewers "go beyond" the primary findings with new interpretive constructs, explanations or hypotheses | [S08 §Stage three] |
| Configuration / abduction | linking findings never linked in the primary studies; "abductive reasoning … begins when reviewers intuit that a set of seemingly unrelated findings are in fact related and ends with models of these relationships that can themselves be formally tested" | [S19 §Configuration] |
| Top-down vs bottom-up configuration | start from an imported concept/theory vs from data-derived assemblies (neither purely deductive/inductive) | [S19] |
| CMO configuration / demi-regularity / middle-range theory | context–mechanism–outcome patterns explaining success, failure and "various eventualities in between" | [S11] |
| Best-fit | test/reinforce/extend an existing model on a new population and generate a refined programme theory | [S09, S10] |
| Problematising the literature | treating the literature itself as an object of scrutiny: how it constructs the problem, its assumptions, proposed solutions | [S02 §Discussion]; [S15] |

### 5.2 Procedure to generate insight (derived from S02, S08, S09/10, S11, S12–S14, S19–S21; the composite order is `[INFERENCE]`)
1. **Harvest constructs, not conclusions.** For each study extract (a) first-order evidence (quotes, raw outcomes), (b) second-order interpretations (authors' explanations, usually in Discussion/Conclusions), (c) measures/definitions used for each key construct. [S13 Table 4 places first-order constructs in Results and second-order in Discussion/Conclusions; the best-fit method deliberately extracted from Results only, because Discussion adds "only additional interpretation" — S09 §Methods; choose per method.]
2. **Cluster ("piles") and translate.** Constant-comparison clustering of concepts; write a defined label per cluster; record which studies' concepts it absorbs; flag *untranslatable* concepts instead of forcing them [S14 §Untranslatable concepts, piles].
3. **Make the contradictions the engine.** For each cluster list studies that disagree; test whether the disagreement is explained by **population, context/setting, measure/construct definition, design, or time** (eMERGe criterion 11: "differences … for reasons that may be explained by differences in participants, settings, or study design" [S12]). A contradiction explained by a moderator becomes a conditional finding; a contradiction explained by a **different construct under the same name** becomes a measurement insight (§6.4).
4. **Import candidate theories top-down** and score *fit*: how much of the data each accommodates; what is left over becomes new themes (best-fit logic: "usefulness of a particular framework is not only determined by 'conceptual fit' but also by … what proportion of the study data can be accommodated within it" [S09 §Lessons]). Keep ≥2 rival theories alive (CERQual coherence threat (c)).
5. **Name synthetic constructs.** Where the data show a pattern none of the studies named, coin a construct (CIS "candidacy"; thematic-synthesis "Children do not see it as their role to be interested in health"), define it, and list the second-order constructs it subsumes [S02; S08].
6. **Draw the synthesising argument** as a small graph: nodes = constructs (synthetic and existing), edges = claimed relations, each edge carrying supporting stems, contradicting stems and a certainty label; for mechanism claims use CMO triples; show feedback (outcomes becoming contexts) when evidence supports it [S02; S09/S10 Figure 5; S11].
7. **Stress-test**: seek disconfirming and negative cases deliberately; check that the argument is not "smoothing out" variation or stretching an explanation; examine plausible alternative explanations not yet explored; test removal of weak studies [S07; S10; S12].
8. **Integrate across streams** with a joint display and label every cell confirmation / expansion / discordance; use expansion to explain *why* effects vary and discordance to locate where the construct or the method is at fault [S21; S18 questions].
9. **Reframe where the literature's unit of analysis is wrong.** Example from the corpus: the double-empathy literature relocates a communication "deficit" from the autistic individual to the **interaction between differently-disposed people**, and a test showed information transfer degrades in *mixed* autistic/non-autistic chains but not in matched chains [S33, S34, S35]. That is the CIS-style move (critique the framing, not only the data) [S02]; it should be tried on any claim of the form "group G cannot do X" by asking whether X is measured in matched or mixed dyads.
10. **State conditions of application and what would falsify the argument** (eMERGe: "describe the context where the new theory … applies, or not" [S12 criterion 15]; best-fit: yields a hypothesis/programme theory to test empirically [S10]).
11. **Adjudicate rival accounts with realist tasks**: for each candidate theory (a) question its integrity (are its own assumptions coherent and supported?), (b) adjudicate against the competing theories on the *same* evidence, (c) test it in comparative settings/populations/measures, and (d) compare the "official" textbook account with what actually happens in practice [S64 §Data synthesis, citing Pawson]. For a "G cannot do X" topic this means testing the deficit account, the double-empathy account, and a measurement-artefact account against the same evidence table.

### 5.3 Quality criteria for an insight (what a reader should be able to check)
- Every edge cites stems and says whether the claim is first-, second- or third-order (whose interpretation) [S12].
- At least one rival explanation is named and evidence for/against it shown [S07].
- Disconfirming cases are listed, not omitted [S10, S12].
- The synthetic construct is defined and traceable to the concepts it absorbed [S02, S14].
- The argument's certainty is stated per proposition (§4), with the weakest link identified.
- The reasoning type is labelled: aggregated (data-based) vs configured (reviewer-linked; "requires further study to establish value") [S20 §Assimilation versus configuration].

---

## 6. (f) Hazards

### 6.1 Wasteful or misleading appraisal
- Summed scores, inclusion decided by scale scores, and treating "peer-reviewed" as a quality proxy (§1.5–1.6).
- Low inter-rater agreement for qualitative checklists [S14]; AMSTAR 2 inter-rater agreement (kappa) varied substantially across items, though 46 of 50 kappa scores were moderate or better and reviewers noted that publication-bias and conflict-of-interest items were often "mentioned … but not [supported with] evidence" [S25 §Inter-rater reliability, §Usability].

### 6.2 Vote counting
- **Definition** (as used in the sources): classify each study as positive / negative / no relationship by significance, then take the modal category as "the" relation [S20; S27].
- **Pitfalls read**: ignores sample size and statistical power; gives no effect size; "performs increasingly poorly as the number of studies increases" [S27 §Vote Counting, citing Hedges & Olkin 1980]; ratios computed on different denominators (k=2 vs k=6) cannot be ranked; conclusions differ depending on whether significance or effect size defines a "positive" [S20 §Summarizing the results]; a bright-line p<0.05 criterion "treats the 0.05 threshold as a bright-line" [S30 §Evaluating replication].
- **Permitted form**: vote counting *by direction of effect* is an accepted SWiM option but changes the question to "is there any evidence of an effect?" and the metric/method must be reported; Cochrane ch. 12 classifies such methods into "acceptable" and "unacceptable" (item list not read) [S01 Table 2; S38 AB].
- **Skill rules**: never rank by "k of n studies significant"; if a direction-of-effect tally is used, show k, N, effect sizes where available, a harvest/effect-direction display, and say which question it answers [S01 §Items 2–3, 7]. Never infer "no effect" from non-significant studies [S27].

### 6.3 Meta-research hazards (publication bias, small studies, flexibility, replication)
| Hazard | Evidence read | Agent rule |
|---|---|---|
| Low power inflates effects and lowers the chance a significant result is true | Median power of neuroscience studies ≈ 8–31% [S29 Key Points]; PPV falls with smaller studies, smaller effects, more tested relationships, more flexible designs, larger financial/ideological interests, "hotter" fields [S28 Corollaries 1–6] | Weight by N; mark small-N, exploratory, flexible-analysis findings; require converging independent evidence |
| Replications give half the effect | 100 replications: original significant 97% vs replication 36% (35/97); mean r 0.403 → 0.197; interaction effects replicated less (22%) than main effects (47%); "surprising" effects replicated less; replication success tracked strength of original evidence more than team expertise; "a single study almost never provides definitive resolution"; understanding comes from "multiple, diverse investigations that provide converging support … and rule out alternative explanations" [S30] | Treat single published significant results as provisional; look for preregistered/registered-report replications; note interaction-type claims |
| Missing results (publication bias) | GRADE: suspect when evidence is a few small, commercially funded studies; funnel plots "substantial limitations" [S54 AB]; Cochrane ch. 13 frames "risk of bias due to missing results in a synthesis" [S59 AB]; AMSTAR 2 makes assessment of publication bias a critical item [S25]; CERQual flags dissemination bias but has no method yet [S03 Box 2] | Search registries/preprints; state how missing results were sought; downgrade for reporting bias when pattern fits |
| Questionable measurement / flexible definitions | Ioannidis corollary 4 (flexibility in designs, definitions, outcomes); Flake & Fried 2020 [S60] AB only | Treat measure choice as a data-extraction field (§6.4) |
| Redundant, misleading, conflicted reviews | Ioannidis 2016 [S61] AB | Prefer reviews that pass AMSTAR 2 critical domains; disclose conflicts |
| Narrative reviews are not automatically inferior, systematic reviews not automatically superior | Greenhalgh, Thorne, Malterud 2018 abstract-level only [S62 AB]; Siddaway: systematic review recommended "whenever possible" but narrative reviews legitimate for theory building [S27] | Use the right logic for the question (§2.0) |

### 6.4 Construct validity: jingle-jangle, measurement heterogeneity `[mostly INFERENCE — primary jingle-jangle papers were paywalled]`
- What the sources read support: CERQual coherence threat (b) "elements of the underlying data may be defined in slightly different ways across different studies … data may appear reasonably comparable but we are not sure if they are in fact comparable" [S07]; CIS treats construct definitions as emergent and contested [S02]; psychometric reviews (COSMIN) exist for exactly this [S26]; SWiM item 1 requires justified groupings [S01].
- The label "jingle" (same word, different construct) / "jangle" (different words, same construct) did **not** reach a full-text source here (Marsh 1994, Lawson & Robins 2021, Larsen/Bong etc. all paywalled or not downloaded). Use the terms as vocabulary only, flag `[NOT VERIFIED IN HOME-STILL]`, and re-run the acquisition if needed.
- Rule: for every key construct in the user's question (e.g. "risk-taking", "impulsivity", "sleep loss"), build a **construct ledger** listing each study's *operational measure*, population, and informant (self-report / observer / task). Group before synthesising; never pool across ledger groups without saying so (SWiM 1a). `[INFERENCE]`

### 6.5 Correlation ≠ mechanism: triangulation and causal language
- Triangulation = integrating results from several approaches whose key sources of bias are *unrelated*; concordance across approaches strengthens confidence, especially when the biases would push in opposite directions; inconsistencies reveal which further study is needed [S50 AB]. Nosek et al. make the same point for theory: converging, diverse investigations that "rule out alternative explanations" [S30]. GRADE's own caution: observational studies do not reliably predict trials (HRT example) [S22 §Study design]. Hammerton & Munafò 2021 [S51] — see §9 for read-status.
- Rule: the skill writes causal verbs only when ≥2 designs with different bias structures agree and ROBINS-E/I domains (confounding first) are not critical; otherwise "associated with", plus a named confounding story. `[INFERENCE from S22, S24, S30, S50]`
- ROBINS-I confounding must be defined *a priori* via expert knowledge and scoping — an agent should generate the confounder list before extraction [S24].

### 6.6 Interpretive hazards
- Over-smoothing: findings simplified so they cohere; **stretched explanations** [S07].
- Loss of groundedness with many studies: superficial synthesis if the volume is not managed in clusters [S12 criterion 15; S14].
- Reviewers read concepts through their own experience — use collaborative interpretation and disagreement logs: "rather than removing bias, we challenge personal interpretation through collaboration" [S14 §Discussion].
- Reproducibility: CIS and meta-ethnography accept lower strict reproducibility and compensate with transparency of reasoning [S02, S13].
- Poor reporting of context limits translation [S08, S13].

### 6.7 home-still-specific hazards observed during this acquisition
- `paper_download` returned "No open-access PDF found" for 66 of 135 DOIs attempted (69 acquired, 9 of which were already in storage), including core Cochrane Handbook chapters, the J Clin Epi GRADE 2011 series, SAGE and Elsevier items. 4 BMJ papers failed once and succeeded on retry (retry once before declaring paywalled); the other failures reproduced on retry with `paper_get` priming.
- **Catalog metadata can be wrong**: `catalog_read` for stem `10.1186_1471-2288-8-45` reports the title "Systematic review of the strategies applied to improve the organizational climate …" although the converted markdown is Thomas & Harden (2008) thematic synthesis. `paper_get` returned the same wrong title. *Always confirm the first lines of `markdown_read` match the DOI before citing.* Several corpus catalog entries have blank titles (`10.1038_nrn3475`, `10.1126_science.aac4716`, `10.1177_1362361318786721` …).
- Some downloads are **abstract-only HTML stubs** (QUADAS-2: 4.6 KB) or publisher-accepted-manuscript front matter; check size and content.
- PDF OCR can scramble tables (SWiM Table 1 and 2 are interleaved; item numbers had to be reconstructed from several fragments). Re-read the PDF/table with `markdown_read` page-by-page before quoting a checklist item verbatim.
- `scribe_convert` of PDFs took ~3.5–6 min each under load (≈6 slots shared); HTML-derived items convert in < 1 s.
- Sibling workers share the convert backend; keep own concurrency ≤ 2.

### 6.8 Theory-building hazards: empirical generalisations versus explanations
A review's conceptual model mixes two kinds of link and the skill must label which is which. Oberauer & Lewandowsky distinguish two inference levels: an **empirical** level (data support *hypotheses* = empirical generalisations such as a Stroop effect) and a **theoretical** level (a *theory* — "an integrated set of propositions about latent … mechanisms, processes, and variables, and their causal relations to each other and to manifest … variables" — explains generalisations to the degree there is a "strong inferential link" from theory to them) [S65 Table 1, §Introduction]. In discovery-oriented research the motivating theory implies only that *some* phenomena in a broad class exist, not under which conditions, so each positive result raises the probability the theory is true far less than in theory-testing research; evidence supports a theory more "the more strongly T is justified independently of X" [S65 §Discussion]. Practical rules `[INFERENCE]`: (i) tag every arrow in the synthesising argument as *empirical generalisation* or *theoretical explanation*; (ii) give an explanation arrow only when the mechanism is stated and independently motivated, otherwise write "associated with"; (iii) do not count many exploratory, post-hoc positive findings as cumulative support for a mechanism; (iv) direct replication is "the gold standard" for establishing an empirical generalisation but not for choosing among theories [S65]. Realist "demi-regularities" and CIS "synthetic constructs" [S11, S02] are both attempts at the theoretical level and carry the same burden.

---

## 7. Autism-adjacent topics: participatory and neurodiversity-informed research ethics

Read in full or in part: [S31] Fletcher-Watson et al. 2019 (seminar series; FT), [S32] Botha & Cage 2022 (mixed-method, FT-part), [S33] Milton, Gurbuz & López 2022 (FT), [S34] Milton 2012 (FT-part), [S35] Crompton et al. 2020 (FT-part), [S36] Mitchell, Sheppard & Cassidy 2021 (FT-part), [S37] Gillespie-Lynch et al. 2017 (abstract/intro). Pellicano & den Houting 2022, Chown et al. 2017, Pellicano et al. 2014 were paywalled (AB).

What the sources establish:
1. **Participatory research** = "incorporating the views of autistic people and their allies about what research gets done, how it is done and how it is implemented"; central principle: recognise and undermine the researcher–participant power imbalance (Arnstein's ladder; much autism research "no power, or only tokenistic" for the community). Five topics to build practice around: **Respect, Authenticity, Assumptions, Infrastructure, Empathy** [S31 Abstract, Introduction].
2. Community priorities diverge from funded research; researchers believe they engage more than the community perceives [S31 §Introduction, citing Pellicano 2013/2014 — second-hand].
3. Consultation with one autistic person is not "a consistent community view"; parents' views are not a substitute for autistic people's views; diversity of autistic opinion must be handled, and non-speaking / intellectually disabled autistic people are rarely reached [S31 §Methodological challenges, Limitations].
4. Terminology: identity-first language is preferred by many autistic people and was used by the autistic co-authors [S31 note 1; S36 note 1]; but language alone does not prevent dehumanisation if personhood is denied [S32 §Discussion].
5. Researchers can be ableist; medicalised narratives predicted higher odds of ableist cues, and **greater inclusion of autistic people in research predicted significantly lower odds of ableist cues** (controlling for other contact and career length) [S32 Abstract].
6. **Autistic adults showed more accurate scientific knowledge of autism than others** in a 636-person survey and more often opposed the medical model; endorsing "normalising" autistic people tracked with higher stigma [S37 Abstract] — evidence that autistic accounts are *expert* data, not merely "experience".
7. **Double empathy**: mutual breakdown of understanding between differently-disposed people — "a double problem … not a singular problem located in any one person" [S34 §definition]; ten-year review: the framing "locus of the problem has traditionally been seen to reside in the brain of the autistic person" and proposes treating it as interactional; inferences from observation alone may be inaccurate (Doherty 2020; Mitchell 2021) [S33]. Empirical support: autistic-to-autistic information transfer equalled non-autistic-to-non-autistic; **mixed chains** lost more information and had lower rapport [S35 Results]; neurotypical-majority society may hinder development of the abilities needed for smooth interaction [S36 Abstract/intro]. Limits: modest sample, aware of diagnostic status, replication warranted [S35 Limitations].

Rules for the skill when a topic concerns autistic people `[INFERENCE — derived from the above]`:
- **Add a "who is speaking" field** to every extraction: autistic self-report, family report, clinician/observer, performance task. Synthesise by informant type before combining.
- **Always carry the double-empathy / interactional hypothesis as a named competing theory** for any "autistic people lack/cannot X" finding (CERQual coherence threat (c) requires rival explanations to be explored [S07]); ask whether X was measured with matched or mixed partners and whether the task presupposes neurotypical norms.
- **Sample autistic-authored and community-priority sources deliberately** (theoretical sampling [S02]; participatory-research literature [S31, S32]); label them in the evidence table; do not treat them as grey literature to be dropped.
- **Deficit-language audit**: flag deficit/disorder framing in constructs and outcome labels; report identity-first / person-first usage and the reason; avoid dehumanising metaphors [S31, S32].
- **Not-about-us-without-us note** in the output when no autistic involvement was possible: the synthesis is a literature product made without community co-production [S31 principles]; invite correction.
- **Do not pathologise a single trait as an explanation** without noting measurement, context and dyad effects (§6.4–6.5).

---

## 8. Practice → source → how an autonomous LLM-agent pipeline should implement it

| # | Practice | Source(s) | Implementation in an agent pipeline (`[INFERENCE]` unless in quotes) |
|---|---|---|---|
| 1 | Classify question type and logic (aggregate/configure) before searching | S16, S19, S26 | Step-0 JSON `review_frame`: question type (PEO/PICo/PICO/COSMIN), logic per sub-question, evidence streams, planned synthesis method per stream, planned certainty framework. Save to disk before any search; log changes with reason (SWiM 1b). |
| 2 | Appraise by design, domain-by-domain, with quotes and "no information" | S23, S24, S25 | Per study×outcome record: `domain → judgement → verbatim quote (stem+line range) | NI`. A second agent pass re-reads the quote against `markdown_read` to verify it exists. Reject any judgement without a quote. |
| 3 | No summed quality scores; do not exclude by score | S25, S05, S27 | Forbid numeric aggregation in schema; carry `appraisal_summary` as text + categorical overall only where the tool defines one (e.g. ROBINS-I overall, AMSTAR 2 confidence). |
| 4 | Keep relevant-but-weak evidence; sensitivity analysis | S02, S08, S09, S10 | Tag each study `reporting_adequacy ∈ {adequate, inadequate}` (four criteria); after synthesis recompute each theme/finding without inadequate studies; report changes. |
| 5 | Name every synthesis method and report SWiM items | S01 | Auto-generate a "Synthesis methods" appendix filling items 1–9; unfilled item = blocker, not silent omission. |
| 6 | Vote counting only by direction of effect, with k, N, effect sizes, display | S01, S20, S27, S30 | Disallow "x of y significant" language; require table with direction/effect/N per study; label the question answered. |
| 7 | Qualitative synthesis: coding → descriptive → analytical themes; or best-fit; or meta-ethnography/CIS | S08, S09, S10, S12, S02 | Separate fields `first_order`, `second_order`, `third_order`; cluster concepts with explicit labels/definitions; store which stems each cluster absorbs; analytical layer must cite ≥2 descriptive themes. |
| 8 | Refutational translation / disconfirming cases mandatory | S12, S07, S10, S11 | For each major finding run a dedicated "counter-evidence" retrieval (`distill_search` with negated/alternative phrasing) and record hits or "none found + queries tried". |
| 9 | Competing-theory test | S07, S09, S10 | Maintain a `theories[]` table; each finding records data accommodated / unaccommodated per theory; final text names the best-fitting and the strongest rival. |
| 10 | Per-finding certainty (GRADE-style for effects, CERQual-style for qualitative), no numeric score, avoid double downgrading | S22, S03, S05, S06, S07 | Emit §4.3 record for every claim; a verifier pass checks no concern is counted twice; findings without a certainty record cannot appear in the executive summary. |
| 11 | Two-reviewer principle | S03, S05, S10, S14 | Two independent agent runs (different prompts/models) assess each finding's components; disagreements listed; final rating requires a reconciling note. |
| 12 | Synthesising argument with synthetic constructs | S02, S08, S19, S13 | Output a construct graph (nodes/edges with stems, certainty, contradictions) + prose; each synthetic construct has definition + absorbed second-order constructs + "what it adds". |
| 13 | Realist CMO tables for mechanism claims | S11 | Table `C | M | O | supporting stems | contradicting stems | middle-range theory`; mechanisms must say whose reasoning/resources are involved. |
| 14 | Mixed-streams integration with fit labels and joint display | S18, S21, S17, S20 | Matrix rows = propositions; columns = quantitative stream, qualitative stream, fit (confirmation/expansion/discordance), explanation; discordance triggers: bias check → construct check → theory → new search. |
| 15 | Triangulate causal claims across designs with different biases | S50 (AB), S30, S22, S24 | Causal wording gate: ≥2 independent designs with distinct bias structures + ROBINS-style confounding judged not critical. |
| 16 | Construct ledger for measurement heterogeneity | S07, S26, S01 | Extraction field `construct_label`, `operational_measure`, `informant`; synthesis groups by ledger entry; cross-group pooling requires justification. |
| 17 | Meta-research hazard screen | S28, S29, S30, S54 (AB), S25 | Per finding: median N, preregistered?, number of tested relationships, replication status, missing-results search; downgrade per GRADE/CERQual logic. |
| 18 | Participatory/neurodiversity-informed practice for autism topics | S31, S32, S33, S35, S37 | "Who is speaking" extraction field; double-empathy rival theory slot; sample autistic-authored sources; deficit-language audit; limitations statement on missing community co-production. |
| 19 | Citation integrity | home-still hazards §6.7 | Citation = {stem, `catalog_read` verified title/year/DOI, first-lines check against `markdown_read`, line/page range}; a citation without all four is blocked. |
| 20 | Report conduct transparently including limits of reproducibility | S02, S12, S11, S01 | Methods appendix lists: queries, dates, stems read in full vs abstract-only, paywalled list, reviewer passes, disagreements, post-hoc changes. |

---

## 9. Sources (key → full citation → stem → status)

Stems are `doc_id` in home-still (DOI with `/`→`_`). "FT" statuses reflect what was actually read through `markdown_read`; "AB" were retrieved with `paper_get`.

| Key | Citation | DOI | Stem | Status |
|---|---|---|---|---|
| S01 | Campbell M, McKenzie JE, Sowden A, et al. 2020. Synthesis without meta-analysis (SWiM) in systematic reviews: reporting guideline. *BMJ* 368:l6890 | 10.1136/bmj.l6890 | `10.1136_bmj.l6890` | FT (Table 1 items, Items 1–9 text, Discussion; OCR scrambled — items reconstructed) |
| S02 | Dixon-Woods M, Cavers D, Agarwal S, et al. 2006. Conducting a critical interpretive synthesis of the literature on access to healthcare by vulnerable groups. *BMC Med Res Methodol* 6:35 | 10.1186/1471-2288-6-35 | `10.1186_1471-2288-6-35` | FT (Methods, Determination of quality, Conducting an interpretive synthesis, Discussion, Table 2) |
| S03 | Lewin S, Glenton C, Munthe-Kaas H, et al. 2015. Using qualitative evidence in decision making for health and social interventions: an approach to assess confidence in findings from qualitative evidence syntheses (GRADE-CERQual). *PLoS Med* 12(10):e1001895 | 10.1371/journal.pmed.1001895 | `10.1371_journal.pmed.1001895` | FT (HTML; Tables 2–4 are images — unread) |
| S04 | Lewin S, Booth A, Glenton C, et al. 2018. Applying GRADE-CERQual to qualitative evidence synthesis findings: introduction to the series. *Implement Sci* (Suppl 1) | 10.1186/s13012-017-0688-3 | `10.1186_s13012-017-0688-3` | FT-part (headings, overview) |
| S05 | Lewin S, Bohren M, Rashidian A, et al. 2018. Applying GRADE-CERQual … paper 2: how to make an overall CERQual assessment of confidence and create a Summary of Qualitative Findings table | 10.1186/s13012-017-0689-2 | `10.1186_s13012-017-0689-2` | FT-part (§Making an overall assessment, Tables 1–2) |
| S06 | Munthe-Kaas H, Bohren MA, Glenton C, et al. 2018. … paper 3: how to assess methodological limitations | 10.1186/s13012-017-0690-9 | `10.1186_s13012-017-0690-9` | FT-part (§Guidance, Steps 1–3) |
| S07 | Colvin CJ, Garside R, Wainwright M, et al. 2018. … paper 4: how to assess coherence | 10.1186/s13012-017-0691-8 | `10.1186_s13012-017-0691-8` | FT-part (§Assessing coherence, Guidance, Table 1) |
| S07b | Glenton C, Carlsen B, Lewin S, et al. 2018. … paper 5: how to assess adequacy of data. *Implement Sci* (Suppl 1) | 10.1186/s13012-017-0692-7 | `10.1186_s13012-017-0692-7` | FT-part (definition, richness/quantity) |
| S07c | Noyes J, Booth A, Lewin S, et al. 2018. … paper 6: how to assess relevance of the data. *Implement Sci* (Suppl 1) | 10.1186/s13012-017-0693-6 | `10.1186_s13012-017-0693-6` | FT-part (definition; three threats) |
| S08 | Thomas J, Harden A. 2008. Methods for the thematic synthesis of qualitative research in systematic reviews. *BMC Med Res Methodol* 8:45 | 10.1186/1471-2288-8-45 | `10.1186_1471-2288-8-45` (**catalog title wrong; markdown correct**) | FT (stages 1–3, Context and rigour, Quality assessment) |
| S09 | Carroll C, Booth A, Cooper K. 2011. A worked example of "best fit" framework synthesis … *BMC Med Res Methodol* 11:29 | 10.1186/1471-2288-11-29 | `10.1186_1471-2288-11-29` | FT (Methods, quality, Lessons) |
| S10 | Carroll C, Booth A, Leaviss J, Rick J. 2013. "Best fit" framework synthesis: refining the method. *BMC Med Res Methodol* 13:37 | 10.1186/1471-2288-13-37 | `10.1186_1471-2288-13-37` | FT (Models and theories, Stage 1–2, Testing the synthesis) |
| S11 | Wong G, Greenhalgh T, Westhorp G, Buckingham J, Pawson R. 2013. RAMESES publication standards: realist syntheses. *BMC Med* 11:21 | 10.1186/1741-7015-11-21 | `10.1186_1741-7015-11-21` | FT-part (What is a realist synthesis?, Items 9–11, Explanation) |
| S12 | France EF, Cunningham M, Ring N, et al. 2019. Improving reporting of meta-ethnography: the eMERGe reporting guidance. *BMC Med Res Methodol* 19:25 | 10.1186/s12874-018-0600-0 | `10.1186_s12874-018-0600-0` | FT-part (criteria 11–17, Phases 4–6) |
| S13 | Atkins S, Lewin S, Smith H, et al. 2008. Conducting a meta-ethnography of qualitative literature: lessons learnt. *BMC Med Res Methodol* 8:21 | 10.1186/1471-2288-8-21 | `10.1186_1471-2288-8-21` | FT-part (Steps 2–6, Table 4) |
| S14 | Toye F, Seers K, Allcock N, et al. 2014. Meta-ethnography 25 years on: challenges and insights for synthesising a large number of qualitative studies. *BMC Med Res Methodol* 14:80 | 10.1186/1471-2288-14-80 | `10.1186_1471-2288-14-80` | FT-part (appraisal, collaborative interpretation, line of argument) |
| S15 | Barnett-Page E, Thomas J. 2009. Methods for the synthesis of qualitative research: a critical review. *BMC Med Res Methodol* 9:59 | 10.1186/1471-2288-9-59 | `10.1186_1471-2288-9-59` | FT-part (Summary, Table 1, §Going beyond) |
| S16 | Gough D, Thomas J, Oliver S. 2012. Clarifying differences between review designs and methods. *Syst Rev* 1:28 | 10.1186/2046-4053-1-28 | `10.1186_2046-4053-1-28` | FT-part (Aggregative and configurative; mixed methods) |
| S17 | Hong QN, Pluye P, Bujold M, Wassef M. 2017. Convergent and sequential synthesis designs: implications for conducting and reporting systematic reviews of qualitative and quantitative evidence. *Syst Rev* | 10.1186/s13643-017-0454-2 | `10.1186_s13643-017-0454-2` | FT-part (Synthesis of results; Implications) |
| S18 | Stern C, Carrier J, Lizarondo L, et al. 2020. Methodological guidance for the conduct of mixed methods systematic reviews. *JBI Evid Synth* | 10.11124/jbisrir-d-19-00169 | `10.11124_jbisrir-d-19-00169` | FT-part (author manuscript; integrated vs segregated; integration questions) |
| S19 | Sandelowski M, Voils CI, Leeman J, Crandell JL. 2012. Mapping the mixed methods–mixed research synthesis terrain. *J Mix Methods Res* 6(4):317–331 | 10.1177/1558689811427913 | `10.1177_1558689811427913` | FT-part (Logics of research synthesis; Table 1) |
| S20 | Voils CI, Sandelowski M, Barroso J, Hasselblad V. 2008. Making sense of qualitative and quantitative findings in mixed research synthesis studies. *Field Methods* 20(1):3–25 | 10.1177/1525822x07307463 | `10.1177_1525822x07307463` | FT-part (Vote counting; Synthesis via assimilation or configuration) |
| S21 | Fetters MD, Curry LA, Creswell JW. 2013. Achieving integration in mixed methods designs—principles and practices. *Health Serv Res* | 10.1111/1475-6773.12117 | `10.1111_1475-6773.12117` | FT-part (Integration at methods/interpretation level; Fit) |
| S22 | GRADE Working Group. 2004. Grading quality of evidence and strength of recommendations. *BMJ* 328:1490 | 10.1136/bmj.328.7454.1490 | `10.1136_bmj.328.7454.1490` | FT-part (Quality of evidence; Box 2) |
| S23 | Sterne JAC, Savović J, Page MJ, et al. 2019. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ* 366:l4898 | 10.1136/bmj.l4898 | `10.1136_bmj.l4898` | FT-part (domains, signalling questions, Table 1) |
| S24 | Sterne JA, Hernán MA, Reeves BC, et al. 2016. ROBINS-I: a tool for assessing risk of bias in non-randomised studies of interventions. *BMJ* 355:i4919 | 10.1136/bmj.i4919 | `10.1136_bmj.i4919` | FT-part (Domains, steps, Table 2) |
| S25 | Shea BJ, Reeves BC, Wells G, et al. 2017. AMSTAR 2: a critical appraisal tool for systematic reviews … *BMJ* 358:j4008 | 10.1136/bmj.j4008 | `10.1136_bmj.j4008` | FT-part (Box 1, Box 2, Discussion) |
| S26 | Munn Z, Stern C, Aromataris E, Lockwood C, Jordan Z. 2018. What kind of systematic review should I conduct? A proposed typology and guidance for systematic reviewers in the medical and health sciences. *BMC Med Res Methodol* | 10.1186/s12874-017-0468-4 | `10.1186_s12874-017-0468-4` | FT-part (Review typology) |
| S27 | Siddaway AP, Wood AM, Hedges LV. 2019. How to do a systematic review: a best practice guide for conducting and reporting narrative reviews, meta-analyses, and meta-syntheses. *Annu Rev Psychol* 70 | 10.1146/annurev-psych-010418-102803 | `10.1146_annurev-psych-010418-102803` | FT-part (Vote counting, Meta-analyses, Narrative reviews, Study quality) — already in corpus |
| S28 | Ioannidis JPA. 2005. Why most published research findings are false. *PLoS Med* 2(8):e124 | 10.1371/journal.pmed.0020124 | `10.1371_journal.pmed.0020124` | FT-part (Corollaries 1–6) |
| S29 | Button KS, Ioannidis JPA, Mokrysz C, et al. 2013. Power failure: why small sample size undermines the reliability of neuroscience. *Nat Rev Neurosci* 14:365–376 | 10.1038/nrn3475 | `10.1038_nrn3475` | FT-part (Key Points) — already in corpus |
| S30 | Open Science Collaboration. 2015. Estimating the reproducibility of psychological science. *Science* 349:aac4716 | 10.1126/science.aac4716 | `10.1126_science.aac4716` | FT-part (Results, Discussion) — already in corpus |
| S31 | Fletcher-Watson S, Adams J, Brook K, et al. 2019. Making the future together: shaping autism research through meaningful participation. *Autism* | 10.1177/1362361318786721 | `10.1177_1362361318786721` | FT — already in corpus |
| S32 | Botha M, Cage E. 2022. "Autism research is in crisis": a mixed method study of researcher's constructions of autistic people and autism research. *Front Psychol* 13:1050897 | 10.3389/fpsyg.2022.1050897 | `10.3389_fpsyg.2022.1050897` | FT-part (Abstract, participatory section, Discussion) |
| S33 | Milton D, Gurbuz E, López B. 2022. The 'double empathy problem': ten years on. *Autism* 26(8):1901–1903 | 10.1177/13623613221129123 | `10.1177_13623613221129123` | FT |
| S34 | Milton DEM. 2012. On the ontological status of autism: the 'double empathy problem'. *Disability & Society* 27(6):883–887 | 10.1080/09687599.2012.710008 | `10.1080_09687599.2012.710008` | FT-part — already in corpus |
| S35 | Crompton CJ, Ropar D, Evans-Williams CV, Flynn EG, Fletcher-Watson S. 2020. Autistic peer-to-peer information transfer is highly effective. *Autism* 24(7):1704–1712 | 10.1177/1362361320919286 | `10.1177_1362361320919286` | FT-part (Method, Results, Limitations) — already in corpus |
| S36 | Mitchell P, Sheppard E, Cassidy S. 2021. Autism and the double empathy problem: implications for development and mental health. *Br J Dev Psychol* 39 | 10.1111/bjdp.12350 | `10.1111_bjdp.12350` | FT-part (opening) — already in corpus |
| S37 | Gillespie-Lynch K, Kapp SK, Brooks PJ, Pickens J, Schwartzman B. 2017. Whose expertise is it? Evidence for autistic adults as critical autism experts. *Front Psychol* 8:438 | 10.3389/fpsyg.2017.00438 | `10.3389_fpsyg.2017.00438` | FT-part (Abstract, Introduction) — already in corpus |
| S38 | McKenzie J, Brennan S. 2019. Synthesizing and presenting findings using other methods. Cochrane Handbook ch. 12 | 10.1002/9781119536604.ch12 | — (not in corpus) | AB |
| S39 | Cochrane Handbook ch. 8, Assessing risk of bias in a randomized trial (2019) | 10.1002/9781119536604.ch8 | — | AB |
| S40 | Cochrane Handbook ch. 25, Assessing risk of bias in a non-randomized study (2019) | 10.1002/9781119536604.ch25 | — | AB |
| S41 | Higgins JPT, et al. 2024. A tool to assess risk of bias in non-randomized follow-up studies of exposure effects (ROBINS-E). *Environ Int* | 10.1016/j.envint.2024.108602 | — | AB |
| S42 | Whiting PF, Rutjes AWS, Westwood ME, et al. 2011. QUADAS-2 … *Ann Intern Med* 155(8):529–536 | 10.7326/0003-4819-155-8-201110180-00009 | `10.7326_0003-4819-155-8-201110180-00009` | Stub (abstract only, 4.6 KB) |
| S43 | Whiting P, et al. 2016. ROBIS … *J Clin Epidemiol* | 10.1016/j.jclinepi.2015.06.005 | — | AB (via search metadata) |
| S44 | Hong QN, et al. 2018. The Mixed Methods Appraisal Tool (MMAT) version 2018 … *Education for Information* | 10.3233/efi-180221 | — | AB |
| S46 | Rodgers M, et al. 2009. Testing methodological guidance on the conduct of narrative synthesis in systematic reviews. *Evaluation* | 10.1177/1356389008097871 | — | AB |
| S47 | Pawson R, et al. 2005. Realist review — a new method of systematic review designed for complex policy interventions. *J Health Serv Res Policy* | 10.1258/1355819054308530 | — | AB |
| S49 | Aromataris E, et al. 2015. Summarizing systematic reviews: methodological development, conduct and reporting of an umbrella review approach. *Int J Evid Based Healthc* | 10.1097/XEB.0000000000000055 | — | AB |
| S50 | Lawlor DA, Tilling K, Davey Smith G. 2016. Triangulation in aetiological epidemiology. *Int J Epidemiol* | 10.1093/ije/dyw314 | — | AB |
| S52 | Campbell M, Katikireddi SV, Sowden A, Thomson H. 2019. Lack of transparency in reporting narrative synthesis of quantitative data … *J Clin Epidemiol* 105:1–9 | 10.1016/j.jclinepi.2018.08.019 | — | AB |
| S53 | Guyatt G, et al. 2011. GRADE guidelines 1–4 (J Clin Epidemiol): 10.1016/j.jclinepi.2010.04.026 / .07.015 / .07.017 | | — | AB |
| S54 | GRADE guidelines 5 — publication bias | 10.1016/j.jclinepi.2011.01.011 | — | AB |
| S55 | GRADE guidelines 9 — rating up | 10.1016/j.jclinepi.2011.06.004 | — | AB |
| S56 | GRADE guidelines 7 — inconsistency | 10.1016/j.jclinepi.2011.03.017 | — | AB |
| S57 | GRADE guidelines 8 — indirectness | 10.1016/j.jclinepi.2011.04.014 | — | AB |
| S58 | GRADE guidelines 6 — imprecision | 10.1016/j.jclinepi.2011.01.012 | — | AB |
| S59 | Cochrane Handbook ch. 13, Assessing risk of bias due to missing results in a synthesis (2019) | 10.1002/9781119536604.ch13 | — | AB |
| S60 | Flake JK, Fried EI. 2020. Measurement schmeasurement … | 10.1177/2515245920952393 | — | AB |
| S61 | Ioannidis JPA. 2016. The mass production of redundant, misleading, and conflicted systematic reviews and meta-analyses. *Milbank Q* | 10.1111/1468-0009.12210 | — | AB |
| S62 | Greenhalgh T, Thorne S, Malterud K. 2018. Time to challenge the spurious hierarchy of systematic over narrative reviews? *Eur J Clin Invest* | 10.1111/eci.12931 | — | AB |

*Additional sources (S45, S48, S51, S63–S71) are in §9.2 below.*

### 9.1 Not obtained through home-still (do not cite as read)
Popay et al. 2006 (ESRC narrative synthesis guidance; no DOI), Noblit & Hare 1988 (book), Hedges & Olkin 1980 (vote-counting), Hill 1965, Egger 1997, Simmons et al. 2011, Franco et al. 2014, Kvarven et al. 2020, Stanley et al. 2018, Britten 2002, Campbell 2011 HTA (meta-ethnography evaluation), Dixon-Woods 2005 & 2007, Whittemore & Knafl 2005, Grant & Booth 2009, O'Cathain 2010, Guyatt/Balshem GRADE 2011 full text, ROBINS-E full text, NOS/CASP primary papers, Pellicano et al. 2014, Chown et al. 2017, Pellicano & den Houting 2022, Eronen & Bringmann 2021, Borsboom et al. 2021, Fried 2020, jingle-jangle primary papers (Marsh 1994; Lawson & Robins; others). These failed with "No open-access PDF found" (66 of 135 DOIs attempted).

### 9.2 Additional sources read or retrieved after the main table
| Key | Citation | DOI | Stem | Status |
|---|---|---|---|---|
| S48 | Wong G, Greenhalgh T, Westhorp G, Buckingham J, Pawson R. 2013. RAMESES publication standards: meta-narrative reviews. *BMC Med* 11:20 | 10.1186/1741-7015-11-20 | `10.1186_1741-7015-11-20` | FT-part (definition, four questions, pluralistic purpose) |
| S63 | Melendez-Torres GJ, Thomas J, Lorenc T, O'Mara-Eves A, Petticrew M. 2018. Just how plain are plain tobacco packs: re-analysis of a systematic review using multilevel meta-analysis suggests lessons about the comparative benefits of synthesis methods. *Syst Rev* | 10.1186/s13643-018-0821-7 | `10.1186_s13643-018-0821-7` | FT-part (abstract, conclusions) |
| S64 | Rycroft-Malone J, McCormack B, Hutchinson AM, et al. 2012. Realist synthesis: illustrating the method for implementation research. *Implement Sci* 7:33 | 10.1186/1748-5908-7-33 | `10.1186_1748-5908-7-33` | FT-part (Background, Data synthesis) |
| S65 | Oberauer K, Lewandowsky S. 2019. Addressing the theory crisis in psychology. *Psychon Bull Rev* | 10.3758/s13423-019-01645-2 | `10.3758_s13423-019-01645-2` | FT-part (Introduction, Table 1, discovery-oriented vs theory-testing) |
| S66 | Heyvaert M, Hannes K, Maes B, Onghena P. 2013. Critical appraisal of mixed methods studies. *J Mix Methods Res* 7:302–327 | 10.1177/1558689813479449 | `10.1177_1558689813479449` | FT-part (Abstract, Introduction) |
| S67 | Sattar R, Lawton R, Panagioti M, Johnson J. 2021. Meta-ethnography in healthcare research: a guide to using a meta-ethnographic approach for literature synthesis. *BMC Health Serv Res* | 10.1186/s12913-020-06049-w | `10.1186_s12913-020-06049-w` | FT-part (stage-by-stage guide; category labels are descriptive, third-order constructs come in phases 5–6) |
| S68 | Ma L-L, Wang Y-Y, Yang Z-H, et al. 2020. Methodological quality (risk of bias) assessment tools for primary and secondary medical studies: what are they and which is better? *Mil Med Res* | 10.1186/s40779-020-00238-8 | `10.1186_s40779-020-00238-8` | FT-part (non-randomised, cohort, case-control, qualitative, secondary-study sections) |
| S69 | Lo CK-L, Mertz D, Loeb M. 2014. Newcastle-Ottawa Scale: comparing reviewers' to authors' assessments. *BMC Med Res Methodol* 14:45 | 10.1186/1471-2288-14-45 | `10.1186_1471-2288-14-45` | FT-part (Methods: NOS structure; Results: agreement; Conclusions) |
| S70 | Downes MJ, Brennan ML, Williams HC, Dean RS. 2016. Development of a critical appraisal tool to assess the quality of cross-sectional studies (AXIS). *BMJ Open* | 10.1136/bmjopen-2016-011458 | `10.1136_bmjopen-2016-011458` | Downloaded; **not read** in this pass |
| S45 | Pace R, Pluye P, Bartlett G, et al. 2012. Testing the reliability and efficiency of the pilot Mixed Methods Appraisal Tool (MMAT) for systematic mixed studies reviews. *Int J Nurs Stud* | 10.1016/j.ijnurstu.2011.07.002 | `10.1016_j.ijnurstu.2011.07.002` | Downloaded; **not read** in this pass |
| S51 | Hammerton G, Munafò MR. 2021. Causal inference with observational data: the need for triangulation of evidence. *Psychol Med* | 10.1017/s0033291720005127 | `10.1017_s0033291720005127` | Downloaded; conversion pending when this reference was written — **not read**; use [S50] (abstract) for the triangulation definition |
| S71 | Munn Z, Barker TH, Moola S, et al. 2020. Methodological quality of case series studies: an introduction to the JBI critical appraisal tool. *JBI Evid Synth* 18(10):2127–2133 | 10.11124/jbisrir-d-19-00099 | `10.11124_jbisrir-d-19-00099` | FT-part (critical appraisal questions; cut-off advice) |

---

## 10. Gaps and what a future pass should obtain
1. Popay 2006 guidance (ask the user for the PDF to place in the inbox; do **not** use `personal_add` for this without the user's say-so — it is the personal-records pipeline).
2. A full-text source for jingle–jangle (any of the construct-validity papers) — the skill currently has the concept only as vocabulary.
3. Full text of the GRADE 2011 series and ROBINS-E for exact current rating guidance (e.g. starting certainty with ROBINS-I).
4. A tested approach to certainty for *mixed* findings (none found in sources read).
