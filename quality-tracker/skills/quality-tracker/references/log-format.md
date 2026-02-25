# Log Format Reference

## Grep Patterns

These patterns let the agent efficiently query the feedback log without loading the whole file.

### Count total entries
```bash
grep -c "^## " slop/quality-tracker/feedback-log.md
```

### List all entries (date + message)
```bash
grep "^## " slop/quality-tracker/feedback-log.md
```

### Get all scores for a specific dimension
```bash
grep -A1 "| Visual Quality" slop/quality-tracker/feedback-log.md
```

### Get all commit hashes
```bash
grep "^\*\*Commit:\*\*" slop/quality-tracker/feedback-log.md
```

### Get all "Going forward" notes
```bash
grep -A2 "^\*\*Going forward:\*\*" slop/quality-tracker/feedback-log.md
```

### Get all "What do you think?" feedback
```bash
grep -A5 "^\*\*What do you think\?\*\*" slop/quality-tracker/feedback-log.md
```

### Find rollback entries
```bash
grep "^## .*ROLLBACK" slop/quality-tracker/feedback-log.md
```

### Find regression entries
```bash
grep "^## .*REGRESSION" slop/quality-tracker/feedback-log.md
```

### Get last N entries
```bash
# Get line numbers of entry headers
grep -n "^## " slop/quality-tracker/feedback-log.md | tail -5
# Then read from the Nth-to-last header to end of file
```

## Entry Types

### Standard evaluation
Header: `## YYYY-MM-DD HH:MM — <commit message>`

### Rollback
Header: `## YYYY-MM-DD HH:MM — ROLLBACK to <hash>`
Extra fields: `Rolled back from:`, `Reason:`, `Commits discarded:`

### Regression noted (no rollback)
Header: `## YYYY-MM-DD HH:MM — REGRESSION NOTED (no rollback)`
Extra fields: `Issue:`, `Current commit:`, `Note:`

## Delta Computation

Delta = current score - previous entry's score for the same dimension.

- First entry ever: all deltas are `—`
- After rollback: compare to the rollback target entry, not the discarded entries
- If a dimension was added (config updated): delta is `—` for the first entry with the new dimension

## Score Drift Rules

The agent should NOT treat scores as absolute values over time. Rules:

1. **Within a session** (same day): scores are directly comparable
2. **Within a week**: scores are roughly comparable
3. **Across months**: scores are directional only — a "7" today isn't the same as a "7" three months ago
4. **For rollback decisions**: only use sharp single-entry drops (3+ points) or qualitative regression signals, not long-term score comparisons
