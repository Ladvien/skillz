# Quality Tracker Plugin

A Claude Code plugin that tracks user feedback on every code change, tied to git commits. The agent uses past feedback to improve and can roll back to last-known-good states on regression.

## What It Does

After every logical unit of work, the agent asks the user to rate the change and share their thoughts. Scores and qualitative feedback are logged in a markdown file alongside commit hashes. Before starting new work, the agent reads recent feedback to avoid repeating mistakes.

If something breaks, `/qt-broke` finds the last stable commit and offers rollback.

## Commands

| Command | Description |
|---------|-------------|
| `/qt-init` | Set up quality tracking with project-specific evaluation dimensions |
| `/qt-eval` | Evaluate the most recent code change |
| `/qt-broke` | Signal regression, find last good state, offer rollback |
| `/qt-status` | Show score trends and active standing instructions |

## How It Works

1. Run `/qt-init` — agent reads your codebase and proposes 3-5 things to track (you approve/edit)
2. After every code change, agent runs `/qt-eval`:
   - You score each dimension 1-10
   - You share what you think (the important part)
   - Optionally note standing instructions for the agent
3. Everything gets logged in `slop/quality-tracker/feedback-log.md` with the commit hash
4. Agent reads the log before starting new work
5. If something breaks: `/qt-broke` → rollback to last good state

## File Organization

```
your_project/
└── slop/
    └── quality-tracker/
        ├── config.json          # Evaluation dimensions
        └── feedback-log.md      # Append-only feedback log
```

## Key Principles

1. **Every change gets evaluated** — no "too small" threshold
2. **Words matter more than numbers** — qualitative feedback is the primary signal
3. **Log is append-only** — never rewrite history, even on rollback
4. **Agent self-improves** — reads past feedback before starting work
5. **Conflicting instructions get surfaced** — agent asks rather than guessing
6. **Scores drift** — old scores are directional, not absolute
