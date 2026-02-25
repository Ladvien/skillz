---
description: Show current quality trends and active standing instructions
---

# QT Status Command

Show the user where quality stands — score trends, active `going_forward` notes, and any concerns.

## When to Use

- User runs `/qt-status`
- Agent wants to review quality state before starting new work (internal use)

## Behavior

### 1. Check Config Exists

```bash
ls slop/quality-tracker/config.json 2>/dev/null
```

If not found:
```
No quality tracking configured. Run /qt-init to set up.
```

### 2. Gather Recent Scores

Read the last 5-10 entries from `slop/quality-tracker/feedback-log.md`.

For efficient access on large logs:
```bash
grep -c "^## " slop/quality-tracker/feedback-log.md
```

If many entries, read from the tail.

### 3. Display Status

```
**Quality Status — <project-name>**
**Entries tracked:** <N>
**Latest eval:** <date> — <commit message>

**Current Scores (last entry):**
| Dimension | Score | Trend (last 5) |
|-----------|-------|-----------------|
| Visual Quality | 8 | ↑ 6→7→7→8→8 |
| Performance | 6 | ↓ 8→7→7→6→6 |
| Code Clarity | 7 | → 7→7→7→7→7 |

**Active Standing Instructions:**
- "Keep particle count conservative. Check perf before adding visual effects." (from 2026-02-25)
- "Prefer composition over inheritance in the ECS layer." (from 2026-02-23)

**Concerns:**
- ⚠️ Performance has declined over the last 3 entries
```

### 4. Trend Indicators

- `↑` — Improved over last 5 entries (latest > earliest)
- `↓` — Declined over last 5 entries
- `→` — Stable (within ±1 of earliest)

### 5. Active Standing Instructions

Collect all `Going forward:` entries from the log. Show the most recent ones. If there are more than 5, show the 5 most recent and note how many older ones exist.

Flag any that appear to conflict:
```
⚠️ Possible conflict in standing instructions:
- "Prioritize visual richness" (2026-02-20)
- "Keep performance high, avoid heavy rendering" (2026-02-24)

Want to resolve this before I start new work?
```

### 6. If No Entries Yet

```
Quality tracking is configured but no evaluations recorded yet.
Run /qt-eval after your next code change.
```

## What NOT to Do

- Don't load the entire log if it's large — grep and tail
- Don't hide declining trends — surface them clearly
- Don't silently drop old `going_forward` notes — they're active until contradicted
