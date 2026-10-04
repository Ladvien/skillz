---
description: Research and synthesize the literature on a topic with home-still (scoping review with systematic search: frozen protocol, screening, acquisition, deep reading, GRADE/CERQual synthesis, audit) into slop/research/<date>-<slug>/
argument-hint: <topic or folk question, e.g. "link between chronic sleep loss and risky decision-making">
---

Use the `research-synthesis` skill to research this topic end to end:

**Topic:** $ARGUMENTS

Follow the skill's phases in order: scope and premise-check with a protocol frozen before the first external search, existing-corpus check and seed set, seed-validated logged discovery with two independent screening passes and Wohlin snowballing from included papers, acquisition (the skill's scripts, never short-timeout MCP calls for PDF conversion), evidence-ledger retrieval including counter-evidence queries, parallel deep reading with the `paper-reader` agent (quote-or-null extraction, appraisal by design), synthesis with a named method per stream and GRADE / GRADE-CERQual certainty per finding plus the insight layer, the report from the template (PRISMA 2020 / PRISMA-S / PRISMA-ScR / SWiM items and an AI-use statement), then the blocking citation audit. Create the run directory with `init_run.py`; write nothing outside `slop/research/<date>-<slug>/`. If `$ARGUMENTS` is empty, ask the user for the topic first.
