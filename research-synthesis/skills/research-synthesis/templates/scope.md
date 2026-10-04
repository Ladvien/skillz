# Scope and framing: {{topic}}

Run: `{{run_dir}}`  |  Date: {{date}}

> Keys `[Pxx]`/`[Sxx]` resolve in `reference/methodology-process.md` §10 and `reference/methodology-synthesis.md` §9. This file feeds `protocol.md` (which is frozen before the first external search). Replace every TODO.

## 1. The question as asked
> {{topic}}

- Who is asking / what understanding or decision this serves (purpose determines review type [P11]; a broad question needs an explicitly articulated scope or later stages lose direction [P10]): TODO
- Everyday words in the question that are NOT research constructs (translate them in section 4): TODO
- **User checkpoint** (replaces the stakeholder-consultation stage of scoping frameworks, which the literature calls essential [P10] and which an autonomous run cannot do; [INFERENCE] in P §9): ask the user only if the purpose is ambiguous; otherwise record the assumption made: TODO

## 2. Premise check (test it; do not assume it)
- Implicit premise(s), each as a falsifiable claim: TODO
- What each premise would look like if FALSE (the disconfirming result we will look for): TODO
- Rival framings to search for explicitly: reversed direction, third-variable accounts, base-rate/stereotype accounts, measurement artefacts, context-not-trait accounts, interactional accounts (e.g. matched vs mixed partners). Realist tasks ask us to adjudicate between competing theories on the same evidence [S11, S64]: list the candidate theories (>= 2): TODO
- Critical / stigma / stereotype literature to seek: TODO
- Perspectives of the studied group itself (participatory research, autistic-authored work, qualitative first-person accounts); sample them deliberately, they are expert data [S31, S32, S37]: TODO

## 3. Research questions
Classify each by question type and logic before searching [S16, S19, S26]: aggregative = how strong/how certain; configurative = why/how/for whom; for "is A connected to B?" use an etiology/risk (PEO) frame, plus a construct-mapping pre-step when definitions are unstable [S26; INFERENCE].

| ID | Question (answerable from literature) | Type (PEO / PICo / PICO / COSMIN / mechanism / experience) | Logic (aggregative / configurative / both) | Premise it tests |
|---|---|---|---|---|
| RQ1 | TODO | | | |

## 4. Concept map (PCC: Population, Concept, Context) [P08, P10]
| Construct | Everyday phrase it stands for | Operationalisations / measures | Informant (self-report / observer / task) | Home field(s) | Core search terms (+ synonyms, older/newer terms, spellings) | RQ |
|---|---|---|---|---|---|---|
| TODO | | | | | | |

Include the construct the question is *about*, the construct that *might explain it*, the construct that *might confound it*, and one construct that would *refute* it. Break the question into individual concepts and list synonyms/spelling/broader-narrower terms [P18]. The construct ledger (measure x population x informant) is built during extraction and governs what may be pooled [S01 item 1a, S26; S §6.4 INFERENCE].

- Population (diagnostic groups, trait-based/subclinical, general-population dimensional studies, ages): TODO
- Context (lab task, daily life, clinical, workplace, relationships; matched vs mixed partners): TODO

## 5. Eligibility (copy the final version into protocol.md section 4)
Independent of what studies exist; applied consistently; revising after borderline cases means redoing search and sift [P18].

| | Include | Exclude |
|---|---|---|
| Populations | TODO | TODO |
| Concepts / outcomes | TODO | TODO |
| Designs | TODO | TODO |
| Years / language / status | TODO | TODO |
| Background evidence allowed (theory, reviews, critique, community work) | TODO | TODO |

## 6. Adjacent fields to search
TODO - fields whose findings bear on the mechanism even if they never mention the target population. CIS-style theoretical sampling also searches literatures "not directly or obviously relevant" [S02].

## 7. What the existing home-still corpus already covers
(filled after `retrieve.py` over the draft RQs; the corpus mixes unrelated projects, so hits are candidates, not evidence)
- Covered: TODO
- Missing: TODO
- Seed set (>= 5 known-relevant papers; DOIs; diverse authors/years/venues) -> `queries/seeds-known.txt` [P01 item 7, P15]: TODO

## 8. Known confounds and bias risks to track from the start
Diagnostic heterogeneity / changing criteria; self-report vs performance; male-skewed and verbally fluent samples; co-occurring conditions; publication bias; construct overlap between instruments; double-empathy / bidirectionality; small-N, flexible analyses and low replication [S28-S30]. TODO: add topic-specific ones; generate the confounder list BEFORE extraction [S24].

## 9. Review type
Default and rationale live in `protocol.md` section 1 (scoping/mapping with systematic search methods unless the purpose is a single precise question [P11]).
