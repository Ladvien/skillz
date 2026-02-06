---
description: Analyze an entire project (local or open source) and generate walkthrough documents that teach how to reimplement it from scratch
---

# Reconstruct Project Command

Analyze a codebase and produce a numbered series of walkthrough documents that teach a developer how to rebuild the entire project from zero. Every line of code appears in the walkthroughs. Each step ends in a runnable program.

Works for both your own projects and external open source repos you want to learn from.

## Requirements

- Git repository (local project or cloned repo)
- Project must build/run successfully before starting

## Setup

1. Verify git repo:
   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. Determine project name:
   - Use the repo directory name, or ask user if ambiguous

3. Create output directory:
   ```bash
   mkdir -p slop/<project-name>
   ```

## SCRATCHPAD.md

This task exceeds a single context window. Use `SCRATCHPAD.md` at project root to track state across sessions.

### Initialize SCRATCHPAD.md

```markdown
# Reconstruct: [Project Name]

**Started:** [YYYY-MM-DD]
**Status:** [Analyzing | Writing | Complete]
**Source:** [local project | URL of upstream repo]

## Project Inventory

[Files, their purposes, dependency relationships]

## Build Order

[Ordered list of implementation steps — how a developer would actually build this]

## Walkthrough Plan

| Index | Title | Files Covered | Status |
|-------|-------|---------------|--------|
| 01    | ...   | ...           | [ ]    |
| 02    | ...   | ...           | [ ]    |

## Stubs Tracker

| Stub | Introduced In | Resolved In | Status |
|------|---------------|-------------|--------|
| ...  | Part NN       | Part NN     | [ ]    |

## Current Position

**Writing walkthrough:** [index]
**Last file covered:** [path]
**Notes for next session:** [context needed to resume]
```

Update SCRATCHPAD.md after completing each walkthrough document.

## Phase 1: Analyze

1. Map every file in the project (ignore `.git`, `node_modules`, `target`, `build`, `dist`, and other build artifacts)
2. Read each source file and understand:
   - What it does
   - What it depends on
   - What depends on it
3. Identify the dependency graph — what must exist before what
4. Identify the project's entry point and core abstractions
5. For open source repos: identify the project's "philosophy" — idioms, patterns, and conventions the author uses consistently

Write the Project Inventory and Build Order sections of SCRATCHPAD.md.

## Phase 2: Plan Walkthrough Series

Determine how to chunk the project into walkthrough documents. Each walkthrough:

- Covers a cohesive unit of work (Claude decides granularity based on project)
- Ends with a program that compiles/runs (even if functionality is incomplete)
- Builds on previous walkthroughs
- Contains every line of code for the files it covers

Plan principles:

- **Build order matters.** If function A calls function B, introduce B first (or stub it). Think about what a developer would actually type first.
- **Stubs are allowed** to keep things runnable — but the stub must be replaced with real code in a later walkthrough. Track all stubs in SCRATCHPAD.md.
- **Configuration files, Cargo.toml/package.json, etc.** go in the first walkthrough or when first needed.
- **Tests** go alongside the code they test, or in a dedicated testing walkthrough if the project separates them.
- **For open source repos:** call out interesting design decisions and idioms that make this project worth studying. The point is learning — don't just show the code, teach why it's good.

Write the Walkthrough Plan table in SCRATCHPAD.md. Commit it:

```bash
git add SCRATCHPAD.md slop/
git commit -m "reconstruct: walkthrough plan for <project-name>"
```

Show the plan to the user and confirm before writing.

## Phase 3: Write Walkthroughs

For each planned walkthrough, create `slop/<project-name>/YYYY-MM-DD-description-NN.md` where NN is the zero-padded index (01, 02, 03...).

### Walkthrough Document Format

````markdown
# [Project Name] — Part NN: [Title]

**Series:** Reconstructing [Project Name]
**Part:** NN of [total]
**Previous:** [filename of previous part or "None"]
**Status:** Complete

## What We're Building

[1-2 sentences: what this walkthrough adds and why]

## What You'll Have After This

[What the program does at the end of this walkthrough — what you can run/see]

## Prerequisites

- Parts 1 through [NN-1] completed
- [Any tools/dependencies introduced in this part]

## Steps

### Step 1: [Action]

**Why:** [Brief explanation of why this comes now]

**File:** `full/path/to/file.ext`

```language
[Complete file contents as they should look after this step,
 OR the diff/additions if the file was created in a previous walkthrough]
```

**What's happening:** [Explain the code — patterns, decisions, gotchas.
For open source repos, call out: why did the author do it THIS way?
What's the alternative and why is this better?]

### Step 2: [Action]

...

## Verify

```bash
[Exact command to build/run]
```

**Expected:** [What you should see — output, behavior, or "compiles with no errors"]

## What You Learned

- [Pattern or concept introduced]
- [Key decision and why]
- [Idiom worth remembering]

## Stubs Introduced

- [ ] `path/to/file.ext`: `function_name()` — stubbed, implemented in Part [XX]

## Stubs Resolved

- [x] `path/to/file.ext`: `function_name()` — was stubbed in Part [YY]
````

### Writing Rules

1. **Every line of source code must appear.** No "add the rest yourself" or "similar to above."
2. **Show full file contents on first introduction.** On subsequent modifications, show the complete updated section with enough surrounding context to locate it, or the full file if changes are pervasive.
3. **Build order = developer order.** If you'd create the struct before the impl block, show it that way.
4. **Each walkthrough must end runnable.** Stub what you must, but the build command must pass.
5. **Explain decisions, not syntax.** Assume the reader knows the language. Explain *why*, not *what*.
6. **Track stubs.** Every stub introduced must note which future walkthrough resolves it. Update SCRATCHPAD.md stubs tracker.
7. **For open source repos: teach the craft.** Call out patterns worth stealing, clever solutions, and design trade-offs. This is a learning exercise — the walkthrough should make the reader a better developer.

### After Each Walkthrough Document

1. Commit the document:
   ```bash
   git add slop/<project-name>/
   git commit -m "reconstruct: part NN - [title]"
   ```
2. Update SCRATCHPAD.md:
   - Mark walkthrough `[x]` in the plan table
   - Update Current Position
   - Update Stubs Tracker
   - Add context for next session
3. Commit SCRATCHPAD.md:
   ```bash
   git add SCRATCHPAD.md
   git commit -m "reconstruct: update scratchpad after part NN"
   ```

## Phase 4: Finalize

After all walkthroughs are written:

1. Verify every source file is covered — cross-reference SCRATCHPAD.md inventory against walkthrough contents
2. Verify no unresolved stubs remain in Stubs Tracker
3. Write an index file `slop/<project-name>/README.md`:

```markdown
# Reconstructing [Project Name]

[1-2 sentence description of the project and why it's worth studying]

## Walkthroughs

| Part | Title | What You'll Build |
|------|-------|-------------------|
| 01   | ...   | ...               |
| 02   | ...   | ...               |

## How to Use

Follow each part in order. Every part ends with a runnable program.
Each part contains the complete code — type it yourself for muscle memory.
```

4. Update SCRATCHPAD.md status to Complete
5. Final commit and push:
   ```bash
   git add -A
   git commit -m "reconstruct: complete walkthrough series for <project-name>"
   git push
   ```

## Resuming Across Context Windows

If context resets mid-reconstruct:

1. Read SCRATCHPAD.md first
2. Read the last completed walkthrough to understand current state
3. Continue from Current Position
4. Do NOT re-analyze files already covered unless needed for context

## Context Management

After completing every 2-3 walkthrough documents, check context usage. If getting low:

```
**Context Check:** I've written [N] walkthroughs so far. SCRATCHPAD.md is up to date.

If context resets, I'll pick up from Part [next] — no work lost.

Continue, or start a fresh conversation and run /reconstruct to resume?
```
