# Writing good flashcards from research

The API is the easy part. The value of this skill is turning research into cards a
human can actually memorize. A paragraph copied onto a card is a card that never gets
recalled. These rules (drawn from Wozniak's *20 rules of formulating knowledge* and the
spacing-effect literature) exist because the brain reviews simple, well-formed cards far
more reliably — and the scheduler estimates intervals better when each card tests one
thing.

## The cards.json contract

`scripts/mochi.py add-cards` consumes a JSON array. Each item is one card:

```json
[
  {"front": "question / cue", "back": "the one idea", "tags": ["paper:smith2021"]},
  {"content": "raw markdown ...", "tags": ["paper:smith2021"]}
]
```

- `front` + `back` → content becomes `front\n---\nback` (Mochi shows sides split on `---`).
- `content` → used verbatim (single-sided notes, or layouts you control yourself).
- `tags` are optional and have **no leading `#`**. Add a source tag (e.g. `paper:<key>` or
  the home-still doc id) so every card traces back to where it came from. The script adds
  its own `src:<hash>` tag for dedup — don't add that yourself.

## Rules for the tenets

1. **One idea per card (minimum information principle).** If a tenet has two clauses,
   make two cards. Atomic cards are recalled more reliably and scheduled more accurately.
2. **Phrase the front as a precise question with one unambiguous answer.** Avoid yes/no
   prompts (too easy to guess) and avoid "tell me everything about X."
3. **No enumerations or lists on one card.** "Name the 5 assumptions" is a memorization
   trap. Split into separate cards, or use a cloze for each item.
4. **The card must stand alone.** The reader won't have the paper open. Put the minimum
   context needed to make the question answerable into the front — but no more.
5. **Avoid interference.** When two concepts are easily confused, write cards that force
   the distinction rather than cards that could be answered by either.
6. **Capture the *why*, not just the *what*, when the tenet is conceptual.** A mechanism
   or reason is more durable and more useful than a bare fact — but still keep it to one idea.
7. **Keep the back short.** One or two sentences. If you can't, the front is asking for
   too much.
8. **Quote sparingly, paraphrase by default.** Cards are your own restatement of the
   source, not copied passages.

## From research to tenets (the synthesis procedure)

1. Pull source material with the home-still tools (see the `home-still-bridge` skill):
   `distill_search` / `personal_search` for the corpus, `markdown_read` for full text,
   `paper_search` to fill gaps.
2. Extract candidate tenets — the claims, definitions, mechanisms, key results, and
   important caveats. Prefer load-bearing ideas over trivia.
3. Atomize: split multi-part tenets, drop duplicates and near-duplicates, and rank by how
   much the human actually needs to remember it.
4. Write each as a `{front, back, tags}` card following the rules above. Tag every card
   with its source.

## Examples

**Bad → good (atomicity + question form)**

Input tenet: "Transformers use multi-head self-attention and positional encodings because
they have no recurrence, which lets them model long-range dependencies in parallel."

Bad (one overloaded card):
- front: "Explain transformers." back: the whole sentence.

Good (three atomic cards):
- front: "Why do transformers need positional encodings?"
  back: "They have no recurrence, so order isn't implicit — positional encodings inject sequence position."
- front: "What does multi-head self-attention let a transformer do that recurrence can't, computationally?"
  back: "Model dependencies between all positions in parallel, rather than step-by-step."
- front: "What problem does self-attention address for long sequences?"
  back: "Capturing long-range dependencies without information decaying over many recurrent steps."

**Enumeration → clozes**

Input tenet: "PRISMA flow has four phases: identification, screening, eligibility, included."

Bad: front "List the 4 PRISMA phases." Good: four cards, one per phase, each cueing the
phase from its role (or cloze-delete one phase at a time).

## Notes

- This skill writes **two-sided (`---`) and single-sided** cards. Mochi also supports cloze
  deletions and templated cards; if a deck needs those, read `references/api.md` for the
  `fields`/template mechanics and Mochi's cloze syntax before generating them.
