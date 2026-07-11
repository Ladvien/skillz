# Guided Coding Mentor Plugin

A Claude Code plugin that provides a senior engineering mentor. You type every line yourself; the
agent navigates. It runs **two modes**:

- **Practice (`/walkthrough`)** — deliberate practice. The agent shows the *shape* (TODOs), you write
  the logic, and you can't advance until you can explain it. For code you want to deeply own.
- **Copywork (`/copywork`)** — get it done. The agent designs the whole thing, then dictates the
  *real* code one chunk at a time; you transcribe it and the agent explains each chunk after. For
  working code fast, while still building a mental model by typing it (the "retype The Great Gatsby"
  method).

## What It Does

**Research-first**: Before designing anything, the mentor does its homework across three lanes — the
**codebase** (find existing utilities/patterns to reuse), the **literature** (academic prior art via
an academic-search MCP if available, e.g. home-still), and the **web** (current library/API docs and
best practice) — then writes a *Research / Prior Art* section into the plan and confirms it with you
before building.

**Proven-first workflow**: Before teaching you anything, the mentor plans the approach, builds and
verifies the feature works privately, documents how to build it, then guides you to implement it
yourself.

**Explain-back gate**: You don't advance to the next step until you can explain — in your own words —
what the code does, why this approach, and what would break if a key line changed. A step is done
when you can explain it, not when it merely runs.

**Automatic journaling**: The agent records progress to `slop/journal/` after every chunk/step — you
never manage it — and reads that folder at the start of a session so it knows what's already been
done. `/journal` is there if you want to add a deeper entry yourself.

**Progress bar**: Each chunk/step opens with an ASCII bar (`[████░░░░] 4/10`) so you can see how far
through the build you are.

## How It Works

1. You tell Claude what you want to build
2. Claude researches first — codebase, literature, and web — and confirms a *Research / Prior Art*
   summary with you before designing
3. Claude writes a plan with goals, acceptance criteria, and technical approach
4. Claude implements and verifies it privately, then documents the real path
5. Claude resets the codebase (keeping only the walkthrough doc)
6. Claude guides you through building it yourself with TODO markers — the shape, never the solution
7. You run the build/test yourself and report the result
8. You explain the step; Claude advances only when the explanation is solid
9. Throughout: Claude auto-journals progress to `slop/journal/` (no action needed from you)

## Requirements

- Git repository with a working remote (commit & push must succeed)

## Commands

| Command | Description |
|---------|-------------|
| `/walkthrough` | Practice mode — proven-first guided coding session |
| `/copywork` | Get-it-done mode — agent dictates real code, you transcribe it chunk by chunk |
| `/next` | Move to the next walkthrough step (blocked until you can explain the current one) |
| `/journal` | Optional deeper entry (routine progress is journaled automatically) |

## File Organization

```
your_project/
└── slop/
    ├── walkthroughs/
    │   └── 2024-01-15-error-handling.md
    ├── copywork/
    │   └── 2024-01-15-tts-pipeline.md
    └── journal/
        └── 2024-01-15-error-handling.md
```

## Usage

### Start a walkthrough

```shell
/walkthrough
```

Claude will:
1. Verify git repo with working remote
2. Create a safety checkpoint (commit + push)
3. Write a plan with goals, acceptance criteria, and approach
4. Build the feature and verify it works privately
5. Document in `slop/walkthroughs/YYYY-MM-DD-description.md`
6. Reset to checkpoint (keeping walkthrough doc)
7. Guide you to build it yourself

### During a session

- `/next` — Ready for the next step (you'll be asked to explain the current one first)
- `/journal` — Optionally add a deeper entry; routine progress is journaled automatically

Claude escalates help gradually when you're stuck (nudge → hint → breadcrumb → show, 90-second max),
and guides you to run each verification yourself rather than running it for you.

### Journaling (automatic)

Progress is recorded to `slop/journal/` automatically after every chunk/step — one dated file per
session — so the history survives context resets and the agent can pick up where you left off. Use
`/journal` only when you want to capture something deeper (a tricky bug, a key decision):

```shell
/journal
```

## Key Principles

1. **Plan it first** — Write goals and approach before coding
2. **Prove it first** — Claude builds and verifies privately before teaching
3. **You write the code** — During guidance, Claude guides, you type
4. **You run the checks** — Claude tells you what to run; you run it and report
5. **Explain before advancing** — A step is done when you can explain it, not when it runs
6. **Full paths always** — No ambiguity about which file to edit
7. **90-second rule** — Never struggle alone for more than 90 seconds
8. **Memory is automatic** — Progress is journaled to `slop/journal/` after every chunk/step, and
   read back at session start
