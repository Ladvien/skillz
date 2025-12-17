# Guided Coding Mentor Plugin

A Claude Code plugin that provides a senior engineering mentor for deliberate coding practice.

## What It Does

**Proven-first workflow**: Before teaching you anything, the mentor builds and verifies the feature works, documents how to build it, then guides you to implement it yourself.

This eliminates wasted time following instructions that lead nowhere.

## How It Works

1. You tell Claude what you want to build
2. Claude implements it, verifies it compiles, and demos it to you
3. You approve that it works as expected
4. Claude documents the implementation in `slop/walkthrough/NNN.md`
5. Claude resets the codebase (keeping only the walkthrough doc)
6. Claude guides you through implementing it yourself with TODO markers

## Requirements

- Git repository with a working remote (commit & push must succeed)

## Commands

| Command | Description |
|---------|-------------|
| `/walkthrough` | Start a new proven-first guided coding session |
| `/next` | Move to the next step in current walkthrough |
| `/stuck` | Get escalating help (nudge → hint → breadcrumb → show) |
| `/quiz` | Quick pattern check on recent code |
| `/progress` | Show current walkthrough status |
| `/recap` | Generate end-of-session summary |

## Usage

### Start a walkthrough

```shell
/walkthrough
```

Claude will:
1. Verify git repo with working remote
2. Create a safety checkpoint (commit + push)
3. Build the feature and verify it works
4. Demo it for your approval
5. Document in `slop/walkthrough/NNN.md`
6. Reset to checkpoint (keeping walkthrough doc)
7. Guide you to build it yourself

### During a session

- `/next` — Ready for the next step
- `/stuck` — Need help (escalates from hints to showing the answer)
- `/quiz` — Test your understanding of patterns you've used
- `/progress` — See where you are

### End a session

```shell
/recap
```

## Key Principles

1. **Prove it first** — Claude builds and verifies before teaching
2. **You write the code** — During guidance, Claude guides, you type
3. **Full paths always** — No ambiguity about which file to edit
4. **One concept at a time** — No cognitive overload
5. **90-second rule** — Never struggle alone for more than 90 seconds
