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

Before scoping, **read prior history** so you build on what's done, not over it:
```bash
ls -t slop/journal/*.md 2>/dev/null | head
```
Skim the recent entries. Continue unfinished work where it left off.

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

## Phase 2: Research (do your homework before designing)

Before designing the blueprint, run **all three research lanes** (see SKILL.md "Research First"). A
blueprint built from cold knowledge misses what's already in the repo, gets the domain subtly wrong,
and reaches for stale APIs. A lane that finds nothing relevant is reported as empty — never skipped.

1. **Codebase lane** — explore the repo for existing functions, utilities, conventions, and patterns
   to **reuse**, and the idioms the new code should match. Launch the Explore agent / Grep / Glob /
   Read.
2. **Literature lane** — search academic sources for prior art and correct approaches. Use an
   academic-search MCP if available — e.g. **home-still**: `paper_search` (discover),
   `abstract_search` / `distill_search` (semantic search over indexed papers), `paper_get`. With no
   such MCP, use scholarly web search.
3. **Web lane** — `WebSearch` / `WebFetch` for current library/API docs, version-specific behavior,
   and real-world best practice.

Cross-reference the lanes (codebase vs literature vs current docs; call out conflicts), then present a
short **Research / Prior Art** summary and confirm with the user before writing the blueprint:

```
Here's what I found before designing:
- **Reuse from codebase:** [existing utilities/patterns + full paths]
- **Literature:** [papers/citations, or "none applicable"]
- **Web / docs:** [links + version notes]
- **How it shapes the approach:** [1–2 lines]

Look right before I write the blueprint?
```

## Phase 3: Blueprint (the "book")

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

## Research / Prior Art

- **Reuse from codebase:** [existing utilities/patterns to build on — full paths]
- **Literature:** [papers/citations from the literature lane, or "none applicable"]
- **Web / docs:** [library/API docs + version notes from the web lane]
- **How this shaped the approach:** [what the research changed about the design]

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
4. Create the session journal `slop/journal/YYYY-MM-DD-description.md` with a header
   (`# Journal: [date] — [description]`, `**Mode:** copywork`) and a `## Log` section. This is
   appended to automatically as chunks complete.
5. Show the user the **File Map & Build Order** so they see the whole shape, and confirm before
   transcription begins.

Make the blueprint correct and runnable to the best of your ability. It is a best-effort proven
design, not a guarantee — real hiccups get absorbed live at the milestone checks (Phase 5).

## Phase 4: Transcribe Loop

Walk the chunk checklist in build order. For each logical chunk (a function, a block, a coherent
section). **Typing costs the user time — dictate the smallest faithful unit, never a whole file to
change a few lines** (see the skill's "Typing costs time" IRON RULE and "Guidance Format"):

- **New file** → dictate the whole file.
- **New block added to an existing file** → dictate just that block, plus one anchor line saying
  where it goes ("after `def chat_command(): ...`, add:").
- **Edit to existing lines** → dictate only the changed lines, anchored with 1–2 unchanged lines on
  each side and `...` for elision, or state it as "change line N from `A` to `B`".
- **Several scattered edits in one region** → enumerate each as its own `change line N to: …` (or
  anchored + marked) edit. **Never bulk-replace** ("replace lines X–Y with …") when most of that range
  is unchanged — edit density doesn't justify re-typing correct lines; re-type a contiguous block only
  when *most* of its lines change. Dictate the diff, not the region (see SKILL.md "Typing costs time"
  IRON RULE and "Guidance Format").
- **Mark what they touch.** Whenever the shown code includes any unchanged line, flag every
  added/changed line inline — `# <-- add this line` after an added line, `# add this property` above
  an added block, `# <-- change: was X` on a changed line — and collapse the rest with `...`. The user
  should never diff your block against their file by eye (see SKILL.md "Guidance Format").

1. **Present the chunk** — lead with the progress bar (total = Chunk Checklist count; see the skill's
   "Progress Bar"), then the real code with the full file path. This is dictation: show the actual
   code the user will type, not TODOs.

   New file — dictate the whole thing:
   ```
   [████████░░░░░░░░░░░░] Chunk 4/10

   Next — [chunk name]. Type this into [FULL PATH]:

   [the real code for this chunk]
   ```

   Editing an existing file — dictate only the delta, anchored, with every changed line marked so they
   never diff by eye:
   ```
   [██████████░░░░░░░░░░] Chunk 5/10

   Next — add the warmup command to [FULL PATH]. After `def chat_command(): ...`, add:

   # add this function
   def warmup_server() -> None:
       persona = Persona(TalkConfig.load())
       ...

   Then in build_serve_app(), after the `status` line:

       app.command("status")(status)
       app.command("warmup")(warmup_server)  # <-- add this line
   ```

2. **STOP.** Wait for the user to type it verbatim. They type every line; no copy-paste.

3. **After they've typed it, explain what the chunk does** — a few tight sentences: what it does,
   and how it fits the larger structure. This is where the mental model forms. Expand any acronym,
   initialism, or domain term on first use (see the skill's "Explain the Jargon" guidance). Do NOT
   quiz them or gate progression on their understanding — that's `/walkthrough`.

4. **Auto-journal** — append a short entry to the session journal (no prompt; "📝 logged" at most):

   ```
   ### [HH:MM] [chunk name] — [FULL PATH]
   - Built: [one line of what now works]
   - Note: [hiccup or decision, if any]
   ```

5. **Tick the chunk off** in the blueprint's Chunk Checklist and move to the next chunk.

Keep momentum. The point is to finish working code while typing every line.

## Phase 5: Milestone Verify

At natural milestones — a file complete, a feature runnable — guide the user to run the check
*themselves*:

```
That completes [file/feature]. Run [build/test command] and tell me what you get.
```

You don't run it for them. If it fails or reality diverges from the blueprint, update the remaining
**Target Code** and **Chunk Checklist** in the blueprint doc, tell the user what changed and why,
and continue. Don't verify after every chunk — milestones only.

Append the milestone result to the session journal (what was verified, and any fix you made).

## Phase 6: Done

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
