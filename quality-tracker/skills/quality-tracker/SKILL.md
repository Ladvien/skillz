---
name: quality-tracker
description: Track user feedback on every code change. Structured scores plus qualitative notes, tied to git commits. Agent reads past feedback before starting work to avoid repeating mistakes. Supports rollback to last-known-good state on regression. Use after any logical unit of work — plan completion, todo completion, feature implementation.
---

# Quality Tracker

Every code change gets evaluated by the user. Scores and qualitative feedback are logged against git commits in a markdown file that lives in the repo. The agent reads this log before starting new work and adjusts its approach based on what the user has said.

## Core Principle

The user's words matter more than the numbers. Scores are for trend detection and rollback decisions. The `user_feedback` and `going_forward` fields are standing instructions the agent follows until contradicted.

## File Layout

```
project_root/
└── slop/
    └── quality-tracker/
        ├── config.json          # Project-specific evaluation dimensions
        └── feedback-log.md      # Append-only log of commit → user feedback
```

## Commands

| Command | Purpose |
|---------|---------|
| `/qt-init` | Set up quality tracking for a project. Agent proposes 3-5 evaluation dimensions based on the codebase. User approves/edits. |
| `/qt-eval` | Evaluate the most recent logical unit of work. Agent commits, asks scores + qualitative questions, logs entry. |
| `/qt-broke` | User signals regression. Agent finds last-known-good commit from the log and offers rollback. |
| `/qt-status` | Show current quality trends and any active `going_forward` notes. |

## Config Format

`slop/quality-tracker/config.json`:
```json
{
    "project": "project-name",
    "dimensions": [
        {"name": "visual_quality", "description": "Does it look right?"},
        {"name": "performance", "description": "Does it feel fast?"},
        {"name": "code_clarity", "description": "Is the code understandable?"}
    ],
    "created": "2026-02-25",
    "last_updated": "2026-02-25"
}
```

Dimensions are project-specific. The agent proposes them during `/qt-init` by reading the codebase and understanding what matters. 3-5 dimensions. User has final say.

## Log Format

`slop/quality-tracker/feedback-log.md`:

Each entry is a markdown section. Append-only — never rewrite, even on rollback (log the rollback as a new entry).

```markdown
## 2026-02-25 14:30 — feat: add particle system

**Commit:** abc1234
**Files:** src/particles.rs, src/main.rs

| Dimension | Score | Delta |
|-----------|-------|-------|
| Visual Quality | 8 | +2 |
| Performance | 6 | -1 |
| Code Clarity | 7 | 0 |

**What do you think?**
Particles look great but the scene stutters when more than 20 spawn. Spawn point is offset from where I'd expect.

**Going forward:**
Keep particle count conservative. Check perf before adding more visual effects.
```

## Agent Behavior

### Before Starting Work

1. Read `slop/quality-tracker/feedback-log.md` — focus on recent entries
2. Collect all active `going_forward` notes from recent entries
3. If `going_forward` notes conflict, ask the user to clarify priority before proceeding
4. Check for score trends — if a dimension has been declining over 3+ entries, flag it

### After Completing a Logical Unit

1. Commit the work with a descriptive message
2. Run `/qt-eval` flow:
   - Show the user what changed (files, summary)
   - Ask for scores on each dimension (1-10)
   - Ask: "What do you think?"
   - Ask: "Anything I should know going forward?" (optional)
3. Compute deltas from previous entry
4. Append to `feedback-log.md`
5. Commit the log update

### On `/qt-broke`

1. Read `feedback-log.md`
2. Find the most recent entry where no dimension dropped below the user's previous scores by more than 1 point (the last stable state)
3. Show the user: what commit that was, what the scores were, what changed since then
4. Offer: `git reset --hard <commit-hash>`
5. If user accepts, reset and log the rollback as a new entry:
   ```markdown
   ## 2026-02-25 16:00 — ROLLBACK to abc1234

   **Rolled back from:** def5678
   **Reason:** [user's description of what broke]
   ```

### Score Drift Awareness

Scores are relative to the user's evolving standards. The agent does NOT use absolute score thresholds for rollback decisions. Instead it looks for:
- **Sharp drops**: A dimension dropping 3+ points in a single entry → likely regression
- **Qualitative signals**: User feedback containing words like "broke", "worse", "broken", "regression"

Old scores (30+ days) are treated as directional context, not absolute benchmarks.

### Conflicting `going_forward` Notes

When the agent detects conflicting standing instructions (e.g., "prioritize visual richness" vs "keep performance high"), it surfaces the conflict and asks the user to resolve it. This happens at the agent's judgment — either when it notices during planning, or during `/qt-eval` if tensions surface.

### Log Size Management

The agent greps the log rather than loading the entire file. Common patterns:
- `grep "Going forward" feedback-log.md` — collect standing instructions
- `grep -B2 "| Performance" feedback-log.md` — check score trends for a dimension
- Read only the last 5-10 entries in full for recent context
- On `/qt-broke`, scan backward from the end for the rollback target

## When to Trigger Evaluation

Evaluation happens after every **logical unit of work**:
- After completing a plan or spec
- After completing a set of TODOs
- After implementing a feature
- After a refactor
- After a bug fix

There is no "too small" threshold. A one-line change can break things just as badly as a large refactor. Every change gets evaluated.

## Integration with Other Skills

### guided-coding-mentor
- After `/walkthrough` Phase 3 (prove it works), trigger `/qt-eval`
- After user completes guided implementation (Phase 6), trigger `/qt-eval`

### General agent workflow
- Any time the agent commits code, it should prompt for `/qt-eval`
- The agent should read `feedback-log.md` at the start of every session

## Anti-Patterns

❌ Skip evaluation because "it's a small change"
❌ Treat old scores as absolute benchmarks (drift happens)
❌ Rewrite or edit existing log entries (append-only)
❌ Ask more than 5 scored dimensions (user fatigue)
❌ Ignore qualitative feedback in favor of numbers
❌ Let conflicting `going_forward` notes pile up unresolved
❌ Load the entire log into context when grep would suffice
