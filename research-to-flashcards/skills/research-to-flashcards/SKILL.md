---
name: research-to-flashcards
description: >-
  Synthesize digestible tenets from research and store them as Mochi flashcards for
  memorization. Use this whenever the user wants to turn papers, research findings, or
  notes into flashcards; build or add to a Mochi study deck; "help me remember / memorize"
  a topic or paper; or run a research-to-cards pipeline — especially alongside the
  home-still research corpus. Prefer this over generic flashcard advice when the
  destination is Mochi, and over a plain literature review when the user wants something to
  study from. Covers retrieving source material, distilling it into atomic spaced-repetition
  cards, getting human approval, and pushing to the Mochi API (handling its kebab-case keys,
  one-concurrent-request limit, and duplicate-safe re-runs).
---

# Research → Flashcards (Mochi)

Turn research into flashcards a human can actually memorize, and store them in Mochi.
The pipeline is: **retrieve → synthesize tenets → human approves → push to Mochi**.

Division of labor: *you* do the judgment (find the source material, distill it into good
cards); the bundled `scripts/mochi.py` does the deterministic I/O (find/create the deck,
create cards, dedup, report). Keep that boundary — hand-writing API calls per card is
error-prone, and the script already encodes the API's quirks.

## Prerequisites

- `MOCHI_API_KEY` set in the environment. The user creates it in Mochi > Account Settings;
  it requires **Mochi Pro**. If it's missing, ask for it before doing any writes.
- Retrieval uses the home-still research tools. Defer to the `home-still-bridge` skill for
  how to search the corpus — don't reinvent search here.

## Pipeline

### 1. Scope it
Establish, briefly: the topic / paper(s) to draw from, and the target Mochi deck name.
If either is unclear, ask one focused question rather than guessing — cards landing in the
wrong deck or covering the wrong scope waste the user's review time.

### 2. Retrieve the source material
Use the home-still tools (via `home-still-bridge`): `distill_search` / `personal_search`
to find relevant passages, `markdown_read` to pull full text, `paper_search` to fill gaps.
Gather enough to extract the load-bearing ideas — not the whole paper.

### 3. Synthesize tenets
**Read `references/card-quality.md` first**, then distill the material into atomic cards.
The core rules: one idea per card, front phrased as a precise question, no enumerations,
each card stands alone, capture the *why* for conceptual points, keep the back to a sentence
or two. Tag every card with its source (e.g. `paper:<key>` or the home-still doc id).

Produce a `cards.json` array of `{"front", "back", "tags"}` objects (or `{"content", "tags"}`
for single-sided notes). This is the artifact the script consumes.

### 4. Review gate (always — do not skip)
Before writing anything to Mochi, present the proposed cards to the user as a compact table
and get explicit approval:

| # | Front | Back | Tags |
|---|-------|------|------|

Let them cut, edit, merge, or split cards. Writing to a memorization system is costly to
undo by hand, and a bad card is worse than no card — so the human signs off first. Apply
their edits to `cards.json` before proceeding.

### 5. Push to Mochi
Run, in order (these are sequential by design — the API allows one concurrent request):

```bash
DECK_ID=$(python3 scripts/mochi.py ensure-deck "Deck name")
python3 scripts/mochi.py add-cards --deck-id "$DECK_ID" --file cards.json
```

`ensure-deck` is idempotent (reuses a deck with that name, creates it otherwise).
`add-cards` dedups by source hash by default, so re-running after adding a few new tenets
only creates the new ones. Use `--dry-run` to preview, `--no-dedup` only if the user
explicitly wants duplicates allowed.

### 6. Report
Summarize from the script's JSON output: how many cards were created vs. skipped (already
present) vs. errored, the deck they landed in, and any failures. If cards errored (e.g. a
`422` validation error), surface the message and offer to fix and retry just those.

## Reference files

- `references/card-quality.md` — how to write good cards; the `cards.json` schema; examples.
- `references/api.md` — the full Mochi API reference, including the encoding quirks,
  template/`fields` mechanics, and attachments, for anything beyond the script's scope.

## Scope notes

- Cards are text (two-sided on `---`, or single-sided). Images/audio attachments and
  templated/cloze cards are possible via the API but not handled by the script — read
  `references/api.md` if a deck needs them.
- This skill creates and updates cards and decks; it does not run reviews or change a card's
  scheduling. `references/api.md` documents the `/due` endpoint if you need to query what's
  due.
