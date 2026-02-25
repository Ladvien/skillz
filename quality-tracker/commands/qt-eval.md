---
description: Evaluate the most recent code change with scores and qualitative feedback
---

# QT Eval Command

Gather user feedback on the most recent logical unit of work. Commit the code, ask structured questions, log the entry.

## When to Use

- User runs `/qt-eval`
- Agent has just completed a logical unit of work (plan, todos, feature, refactor, bugfix)
- Agent should prompt for this automatically after every commit-worthy change

## Prerequisites

- `slop/quality-tracker/config.json` must exist (run `/qt-init` first)
- Code changes to evaluate

## Behavior

### 1. Commit the Work

If there are uncommitted changes:
```bash
git add -A
git commit -m "<descriptive commit message>"
```

Record the commit hash:
```bash
git rev-parse --short HEAD
```

Record changed files:
```bash
git diff --name-only HEAD~1
```

### 2. Show What Changed

Give the user a brief summary:
```
**Changes committed:** <commit hash>
**Message:** <commit message>
**Files:**
- src/particles.rs (modified)
- src/main.rs (modified)

[Brief 1-2 sentence summary of what was done]
```

### 3. Ask the User to Test

```
Take a moment to test this. Run it, look at it, poke at it.

When you're ready, I'll ask a few quick questions.
```

Wait for the user to signal they've tested.

### 4. Gather Scores

Read dimensions from `slop/quality-tracker/config.json`.

Ask all dimensions at once (don't drip-feed):
```
Rate these 1-10:

1. **Visual Quality** — Does it look right?
2. **Performance** — Does it feel fast?
3. **Code Clarity** — Is the code understandable?
```

Accept scores in any format: "8, 6, 7" or "visual: 8, perf: 6, code: 7" or one per line.

### 5. Ask Qualitative Questions

Always ask both. The first is required, the second is optional.

```
**What do you think?**
(What's working, what's not, what feels off — anything at all)
```

After they respond:

```
**Anything I should know going forward?** (optional)
(Standing instructions, things to avoid, priorities to shift)
```

If they say "no" or "nothing" to the second, that's fine — don't log an empty field, just omit it.

### 6. Compute Deltas

Read the previous entry from `slop/quality-tracker/feedback-log.md` (last entry before the `---` separator).

For each dimension, compute: `current_score - previous_score`

If no previous entry exists, deltas are all `—` (first entry).

### 7. Append to Log

Append to `slop/quality-tracker/feedback-log.md`:

```markdown
## YYYY-MM-DD HH:MM — <commit message>

**Commit:** <short hash>
**Files:** file1.rs, file2.rs

| Dimension | Score | Delta |
|-----------|-------|-------|
| Visual Quality | 8 | +2 |
| Performance | 6 | -1 |
| Code Clarity | 7 | — |

**What do you think?**
<user's feedback verbatim>

**Going forward:**
<user's forward-looking notes, if provided>

---
```

### 8. Commit the Log

```bash
git add slop/quality-tracker/feedback-log.md
git commit -m "quality-tracker: eval — <commit message summary>"
```

### 9. Flag Concerns

After logging, check for issues:

**Sharp score drop (3+ points on any dimension):**
```
⚠️ <Dimension> dropped significantly (from X to Y). Want me to investigate or roll back?
```

**Negative qualitative signal** (user feedback contains "broke", "broken", "worse", "regression", "wrong"):
```
Sounds like something regressed. Want to run /qt-broke to find the last good state?
```

**Declining trend** (dimension dropping for 3+ consecutive entries):
```
📉 <Dimension> has been declining. Worth pausing to address?
```

## If No Config Exists

```
Quality tracking isn't set up yet. Run /qt-init to configure evaluation dimensions.
```

## Handling Quick Responses

If the user gives terse scores ("7 7 7") and minimal feedback ("fine"), log it as-is. Don't push for more detail — they may be in flow. The numbers still capture the signal.

If the user gives detailed feedback, capture all of it. Don't summarize or truncate.

## What NOT to Do

- Don't skip the testing prompt — the user needs to actually test before scoring
- Don't ask scores one at a time — batch them
- Don't summarize or paraphrase user feedback — log it verbatim
- Don't edit previous log entries when appending a new one
- Don't skip evaluation because "it was a small change"
