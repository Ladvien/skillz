---
description: Get-it-done copywork mode — the agent designs the whole thing, then dictates the real code one chunk at a time while you type every line yourself
---

# Copywork Command

Get working code out the door while building a mental model by typing every line yourself — the
"retype The Great Gatsby" method. This is the **get-it-done** mode, not deliberate practice: the
agent dictates the real code, you transcribe it, and the agent explains each chunk *after* you've
typed it. No explain-back gate, no 90-second escalation ladder — that's `/walkthrough`.

**Invariants (shared with `/walkthrough`):** you type every line yourself (no copy-paste), you run
every verification yourself, and we checkpoint git first. **The agent never writes to the project
files** — it writes only the blueprint doc; you transcribe from its dictation into the real files.

## Phase 1: Scope & Checkpoint

1. Ask what to build — a single chunk or a whole project. Accept a description, a spec, or a
   reference to existing code.
2. Confirm this is copywork (get-it-done), not a `/walkthrough` (deliberate practice). If the user
   actually wants to learn the material deeply, point them at `/walkthrough`.
3. Verify this is a git repository:
   ```bash
   git rev-parse --is-inside-work-tree
   ```
   If not, stop: "This must be run inside a git repository."
4. Commit and push a safety checkpoint:
   ```bash
   git add -A
   git commit -m "checkpoint: pre-copywork state" --allow-empty
   git push
   ```
   If push fails, stop: "Push failed. Fix remote issues before starting."

## Phase 2: Blueprint (the "book")

Design the complete implementation up front so the user can see the whole thing, then transcribe it.

1. Generate the filename:
   ```bash
   date +%Y-%m-%d
   ```
2. Write the blueprint to `slop/copywork/YYYY-MM-DD-description.md`:

```markdown
# Copywork: [Project/Feature Name]

**Date:** [YYYY-MM-DD]
**Status:** Blueprint
**Checkpoint:** [commit hash from Phase 1]

## Goal

[One or two sentences — what this builds and what "done & working" means.]

## File Map & Build Order

1. `path/to/first.ext` — [purpose] — [why first]
2. `path/to/second.ext` — [purpose]
...

## Target Code

### `path/to/first.ext`
\`\`\`[lang]
[the complete, real code for this file — the reference text the user will transcribe]
\`\`\`

### `path/to/second.ext`
...

## Chunk Checklist

- [ ] first.ext — [chunk 1: e.g. imports + types]
- [ ] first.ext — [chunk 2: e.g. the main function]
- [ ] second.ext — [chunk 1]
...
```

3. Commit the blueprint:
   ```bash
   git add slop/copywork/
   git commit -m "copywork: blueprint for [description]"
   ```
4. Show the user the **File Map & Build Order** so they see the whole shape, and confirm before
   transcription begins.

Make the blueprint correct and runnable to the best of your ability. It is a best-effort proven
design, not a guarantee — real hiccups get absorbed live at the milestone checks (Phase 4).

## Phase 3: Transcribe Loop

Walk the chunk checklist in build order. For each logical chunk (a function, a block, a coherent
section — not a whole file at once unless it's tiny):

1. **Present the chunk** — the real code, with the full file path. This is dictation: show the actual
   code the user will type, not TODOs.

   ```
   Next — [chunk name]. Type this into [FULL PATH]:

   [the real code for this chunk]
   ```

2. **STOP.** Wait for the user to type it verbatim. They type every line; no copy-paste.

3. **After they've typed it, explain what the chunk does** — a few tight sentences: what it does,
   and how it fits the larger structure. This is where the mental model forms. Expand any acronym,
   initialism, or domain term on first use (see the skill's "Explain the Jargon" guidance). Do NOT
   quiz them or gate progression on their understanding — that's `/walkthrough`.

4. **Tick the chunk off** in the blueprint's Chunk Checklist and move to the next chunk.

Keep momentum. The point is to finish working code while typing every line.

## Phase 4: Milestone Verify

At natural milestones — a file complete, a feature runnable — guide the user to run the check
*themselves*:

```
That completes [file/feature]. Run [build/test command] and tell me what you get.
```

You don't run it for them. If it fails or reality diverges from the blueprint, update the remaining
**Target Code** and **Chunk Checklist** in the blueprint doc, tell the user what changed and why,
and continue. Don't verify after every chunk — milestones only.

## Phase 5: Done

When the project/chunk is complete and working:

```
**Built:** [what now works]
**The map you now hold:** [the files and how they fit together]

Run /journal if you want to capture anything. Commit when ready.
```

No explain-back gate, no muscle-memory challenge — that's the practice mode.

## Whole-Project Runs

For a whole project, the blueprint's Chunk Checklist is the source of truth for progress and survives
context resets. On resume, read the most recent `slop/copywork/*.md`, find the first unchecked chunk,
and continue from there.

```bash
ls -t slop/copywork/*.md 2>/dev/null | head -1
```

## Context Management

If the conversation gets long, remind the user their progress is saved in the blueprint checklist,
and offer `/journal` before continuing.
