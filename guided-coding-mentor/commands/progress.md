---
description: Show current walkthrough status and progress
---

# Progress Command

Show the user their current walkthrough status.

## Steps

1. Find the most recent walkthrough file in `slop/walkthroughs/`
2. Parse the progress section
3. Display a clear status summary

## How to find current walkthrough

```bash
ls -t slop/walkthroughs/*.md 2>/dev/null | head -1
```

If no files found:
```
No walkthroughs yet. Start one with /walkthrough.
```

## Progress display format

```
**Walkthrough: [Title]**
**File:** slop/walkthroughs/[filename]
**Status:** [Planning | Proven | In Progress | Complete]
**Started:** [date from filename]

**Acceptance Criteria:**
✓ [Completed criterion]
○ [Pending criterion]

**Steps:**
✓ Step 1: [description] — completed
✓ Step 2: [description] — completed  
→ Step 3: [description] — in progress
○ Step 4: [description] — not started
○ Step 5: [description] — not started

**Current focus:** [What they should be working on next]

**Known dragons for this step:** [Any warnings from the walkthrough file]
```

## Legend
- ✓ = completed
- → = current step (in progress)
- ○ = not started

## Show Related Journal Entries

```bash
ls slop/dev_journal/*.md 2>/dev/null | grep "$(date +%Y-%m)"
```

If journal entries exist for this month:
```
**Related journal entries:**
- slop/dev_journal/YYYY-MM-DD-description.md
```

## If walkthrough exists but no progress tracked

```
**Walkthrough: [Title]**

Progress tracking not found in file. Want me to add progress markers based on what we've done?
```

Then offer to update the walkthrough file with proper progress tracking.

## Context Reminder

If conversation is long:
```
**Tip:** Run /journal periodically to capture bugs and solutions before context resets.
```
