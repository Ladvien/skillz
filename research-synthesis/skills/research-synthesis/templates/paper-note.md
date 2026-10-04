---
stem: {{stem}}
title:
authors:
year:
doi:
venue:
meta_verified: none        # catalog | openalex | provider | document-only | none  (see "Identity")
evidence_level: full_text  # full_text | abstract_only
design:                    # RCT | non-randomised intervention | cohort | case-control | cross-sectional | diagnostic/psychometric | qualitative | mixed-methods | systematic review/meta-analysis | theory/narrative review
appraisal_tool:            # RoB 2 | ROBINS-I | ROBINS-E (partial) | NOS | AXIS-minimum (partial) | QUADAS-2 | AMSTAR 2 | CIS-prompts | CERQual-limitations | MMAT (partial) | JBI (partial) | none
reporting_adequacy:        # adequate | inadequate (question/design; recruitment; data collection; analysis each clearly described)
read_by:
read_date:
---

# {{stem}}

Rules: every extracted value has a **verbatim quote** + page/location; a value the paper does not state is `null` / `not reported`, never inferred (extraction is verified by `scripts/verify_notes.py`). The reader never fills identity, numbers or judgements from memory.

## Identity (never skip)
- Catalog record (`catalog_read` title / year / DOI): <paste, or "EMPTY">
- Page-1 check: bibliographic identity as PRINTED on page 1 of the document (title / authors / year / journal / DOI): <...>. The catalog can be blank or WRONG (a stem has been seen whose catalog title belonged to another paper) - the first lines of the text must agree with the DOI.
- Provider confirmation: `paper_search(search_type=title)` returned <matching record / nothing>.
  `meta_verified: provider` only if a provider record matches title AND year; `document-only` if the document states it but no provider confirms; `none` if neither (the report will print the paper as UNRESOLVED).
- Same work under another stem (DOI stem + hash stem)? <stems>

## Design and sample
| Item | Value | Quote | Location |
|---|---|---|---|
| Design; preregistered? single/multi-site | | | |
| N total / per group | | | |
| Age (mean, SD, range) | | | |
| Sex / gender (counts, % female; non-binary reported?) | | | |
| Diagnostic method (clinician DSM/ICD, ADOS/ADI-R, self-report, trait-scale cut-off, registry, self-identified) | | | |
| IQ / language level; recruitment source | | | |
| Comparison group & matching | | | |
| Co-occurring conditions handled how | | | |

## Construct ledger (what was actually measured)
| Construct label (as the paper names it) | Operational measure / task | Informant (autistic self-report / family / clinician-observer / performance task) | Matched or mixed partners (if interaction) | Reliability / validity reported | Quote | Location |
|---|---|---|---|---|---|---|
| | | | | | | |

## Findings (first-order evidence)
Location = `p.<n>` (a `markdown_read` page; 1 for HTML-derived docs) + section/table/figure; add `L<a>-<b>` from the search hit when known. Quotes verbatim, short, exact characters.

| # | Finding (as measured) | Effect size / statistic (CI, p, N) | Location | Verbatim quote | RQ | Outcome-level appraisal ref |
|---|---|---|---|---|---|---|
| 1 | | | | | RQ? | A1 |

## Authors' interpretations (second-order) vs what the data show
| Author interpretation / explanation | Location | Verbatim quote | Goes beyond the data? (causal language from cross-sectional data, subgroup claim without power, deficit framing, ...) |
|---|---|---|---|
| | | | |

## Limitations
- Authors' stated: <...>
- Reader's additional: selection, measurement, sex ratio, diagnostic heterogeneity, self-report, confounders not adjusted, multiple comparisons, missing data, small N / flexible analyses (these bias signals feed certainty ratings).

## Appraisal (domain-level, per finding; NO summed score)
Pick the tool by design (table in `protocol.md` section 9). Judge the **finding**, not only the paper [S23, S24, S06]: one row per (finding x domain). Every judgement carries a verbatim quote or `NI` (no information) [S23 'support quotes']. If the tool's item list is not available to the skill (ROBINS-E, AXIS, MMAT, JBI checklists, QUADAS-2 details), set `appraisal_tool: ... (partial)` and code only the minimum: sampling frame, validity of exposure and outcome measures, confounder adjustment, non-response.

| Ref | Domain (as the tool names it) | Judgement (tool's own scale) | Verbatim quote or NI | Location |
|---|---|---|---|---|
| A1 | | | | |

- Tool-defined overall judgement, if the tool defines one (e.g. ROBINS-I overall; AMSTAR 2 confidence). Never a numeric total: <...>
- Sensitivity note: would a theme/finding change if this paper were removed? <...>

## Mechanism and theory material (for synthesis)
- Context-mechanism-outcome statements the paper supports (whose reasoning/resources are involved): <...>
- Theories invoked or tested; evidence for/against each; rival explanations the paper ignores (e.g. interactional / double-empathy account; measurement artefact): <...>
- Constructs the authors coin or redefine (candidate synthetic constructs): <...>

## Relevance and stance
| RQ | Stance (supports / contradicts / mixed / null / background) | One-line reason tied to a finding # |
|---|---|---|

## Extraction check (second pass)
- Re-opened the source for every number/quote above: <done / corrections made: ...>
- `verify_notes.py` result: <paste>

## Follow-ups
- Cited works worth chasing (title + year as printed; look up by DOI before adding to the pool):
- Contradictions with other papers noticed:
