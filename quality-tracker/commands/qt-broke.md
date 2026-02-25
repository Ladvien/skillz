---
description: Signal a regression and roll back to the last known-good state
---

# QT Broke Command

The user says something broke. Find the last stable commit from the feedback log and offer to roll back.

## When to Use

- User runs `/qt-broke`
- User says something like "you broke it", "this is broken", "it was working before"

## Behavior

### 1. Ask What Broke

```
What broke? Describe what you're seeing vs what you expected.
```

Get a clear description. This gets logged.

### 2. Scan the Log

Read `slop/quality-tracker/feedback-log.md` backward from the most recent entry.

**Finding the rollback target:**

Look for the most recent entry that meets ALL of these:
- No dimension score dropped 3+ points from its predecessor
- No qualitative feedback containing regression signals ("broke", "broken", "wrong", "worse")
- If the user described what broke, check if the relevant dimension was stable

If the log is long, grep first:
```bash
grep -n "^## " slop/quality-tracker/feedback-log.md | tail -10
```

Then read the last several entries to find the stable point.

### 3. Show the Rollback Option

```
**Last stable state:**
- **Commit:** <hash> — "<commit message>"
- **Date:** <date>
- **Scores at that point:**

| Dimension | Score |
|-----------|-------|
| Visual Quality | 8 |
| Performance | 7 |
| Code Clarity | 7 |

**What changed since then:**
- <commit message 1>
- <commit message 2>
- <commit message 3>

**Files affected:**
[list of files changed between stable commit and current HEAD]

Roll back to <hash>? This will discard all changes after that commit.
```

### 4. If User Confirms

```bash
git reset --hard <rollback-commit-hash>
```

Then append a rollback entry to the log:

```markdown
## YYYY-MM-DD HH:MM — ROLLBACK to <hash>

**Rolled back from:** <current-hash>
**Reason:** <user's description of what broke>
**Commits discarded:**
- <hash> — <message>
- <hash> — <message>

---
```

Commit the log update:
```bash
git add slop/quality-tracker/feedback-log.md
git commit -m "quality-tracker: rollback to <hash> — <reason summary>"
```

### 5. If User Declines

```
No rollback. The regression is noted in the log. Want to debug instead?
```

Log it anyway as a note:
```markdown
## YYYY-MM-DD HH:MM — REGRESSION NOTED (no rollback)

**Issue:** <user's description>
**Current commit:** <hash>
**Note:** User chose to debug rather than roll back.

---
```

### 6. After Rollback

```
Rolled back to <hash>. You're now at the state from <date>.

Before making new changes, run /qt-eval on the current state to re-baseline your scores.
```

## Edge Cases

### No feedback log exists
```
No quality tracking set up. Can't determine last-known-good state.
Run /qt-init to start tracking, or use `git log` to find the commit manually.
```

### Only one entry in the log
```
Only one tracked entry. Can't determine a "last good" state from the log.

Here's the commit from that entry: <hash>. Want to roll back to it, or check git log for earlier options?
```

### All entries show regression
Offer the earliest logged commit as the rollback target, and note that the log shows no clearly stable state.

## What NOT to Do

- Don't roll back without user confirmation
- Don't delete or modify the log entries being rolled past — the log is append-only
- Don't skip logging the rollback event itself
- Don't assume the user wants to roll back — they might want to debug
