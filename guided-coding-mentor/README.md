# Guided Coding Mentor Plugin

A Claude Code plugin that provides a senior engineering mentor for deliberate coding practice.

## What It Does

**Proven-first workflow**: Before teaching you anything, the mentor plans the approach, builds and verifies the feature works, documents how to build it, then guides you to implement it yourself.

This eliminates wasted time following instructions that lead nowhere.

**Dev journaling**: Captures bugs, challenges, and solutions so you build a personal knowledge base of problems you've solved.

## How It Works

1. You tell Claude what you want to build
2. Claude writes a plan with goals, acceptance criteria, and technical approach
3. Claude implements it, verifies it compiles, and demos it to you
4. You approve that it works as expected
5. Claude documents the implementation in `slop/walkthroughs/YYYY-MM-DD-description.md`
6. Claude resets the codebase (keeping only the walkthrough doc)
7. Claude guides you through implementing it yourself with TODO markers
8. Throughout: Claude prompts you to journal bugs and solutions

## Requirements

- Git repository with a working remote (commit & push must succeed)

## Commands

| Command | Description |
|---------|-------------|
| `/walkthrough` | Start a new proven-first guided coding session |
| `/next` | Move to the next step in current walkthrough |
| `/stuck` | Get escalating help (nudge → hint → breadcrumb → show) |
| `/journal` | Document bugs, challenges, and solutions from this session |
| `/quiz` | Quick pattern check on recent code |
| `/progress` | Show current walkthrough status |
| `/recap` | Generate end-of-session summary |

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
4. Build the feature and verify it works
5. Demo it for your approval
6. Document in `slop/walkthroughs/YYYY-MM-DD-description.md`
7. Reset to checkpoint (keeping walkthrough doc)
8. Guide you to build it yourself

### During a session

- `/next` — Ready for the next step
- `/stuck` — Need help (escalates from hints to showing the answer)
- `/journal` — Document what you've done and bugs you've solved
- `/quiz` — Test your understanding of patterns you've used
- `/progress` — See where you are

### End a session

```shell
/recap
```

Claude will summarize what you built and learned, then prompt you to journal.

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
2. **Prove it first** — Claude builds and verifies before teaching
3. **You write the code** — During guidance, Claude guides, you type
4. **Full paths always** — No ambiguity about which file to edit
5. **One concept at a time** — No cognitive overload
6. **90-second rule** — Never struggle alone for more than 90 seconds
7. **Document the journey** — Journal bugs and solutions for future reference
