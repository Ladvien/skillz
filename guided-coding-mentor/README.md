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

**Proven-first workflow**: Before teaching you anything, the mentor plans the approach, builds and
verifies the feature works privately, documents how to build it, then guides you to implement it
yourself.

**Explain-back gate**: You don't advance to the next step until you can explain — in your own words —
what the code does, why this approach, and what would break if a key line changed. A step is done
when you can explain it, not when it merely runs.

**Dev journaling**: Captures bugs, challenges, and solutions so you build a personal knowledge base
of problems you've solved.

## How It Works

1. You tell Claude what you want to build
2. Claude writes a plan with goals, acceptance criteria, and technical approach
3. Claude implements and verifies it privately, then documents the real path
4. Claude resets the codebase (keeping only the walkthrough doc)
5. Claude guides you through building it yourself with TODO markers — the shape, never the solution
6. You run the build/test yourself and report the result
7. You explain the step; Claude advances only when the explanation is solid
8. Throughout: Claude prompts you to journal bugs and solutions

## Requirements

- Git repository with a working remote (commit & push must succeed)

## Commands

| Command | Description |
|---------|-------------|
| `/walkthrough` | Practice mode — proven-first guided coding session |
| `/copywork` | Get-it-done mode — agent dictates real code, you transcribe it chunk by chunk |
| `/next` | Move to the next walkthrough step (blocked until you can explain the current one) |
| `/journal` | Document bugs, challenges, and solutions from this session |

## File Organization

```
your_project/
└── slop/
    ├── walkthroughs/
    │   └── 2024-01-15-error-handling.md
    └── dev_journal/
        └── 2024-01-15-lifetime-debugging.md
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
- `/journal` — Document what you've done and bugs you've solved

Claude escalates help gradually when you're stuck (nudge → hint → breadcrumb → show, 90-second max),
and guides you to run each verification yourself rather than running it for you.

### Document your work

```shell
/journal
```

Creates a detailed entry in `slop/dev_journal/` capturing:
- What you did
- Bugs and how you fixed them
- Patterns you learned
- What to pick up next time

Claude will also prompt you to journal when:
- You solve a tricky bug
- Context is getting low (long conversation)
- Session is ending

## Key Principles

1. **Plan it first** — Write goals and approach before coding
2. **Prove it first** — Claude builds and verifies privately before teaching
3. **You write the code** — During guidance, Claude guides, you type
4. **You run the checks** — Claude tells you what to run; you run it and report
5. **Explain before advancing** — A step is done when you can explain it, not when it runs
6. **Full paths always** — No ambiguity about which file to edit
7. **90-second rule** — Never struggle alone for more than 90 seconds
8. **Document the journey** — Journal bugs and solutions for future reference
