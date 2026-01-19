---
description: Move to the next step in the current walkthrough
---

# Next Command

Advance to the next step in the current walkthrough.

## Steps

1. Find current walkthrough in `slop/walkthroughs/` (most recent by date)
2. Identify which step they're on
3. Mark current step complete
4. Present the next step with TODOs

## Finding Current Walkthrough

```bash
ls -t slop/walkthroughs/*.md 2>/dev/null | head -1
```

## Before advancing

Check if current step is actually done:
```bash
grep -rn "TODO" src/
```

If TODOs remain:
```
You still have TODOs in your code:
[list files with TODOs]

Finish those first, or say "skip" to move on anyway.
```

## When advancing

1. Update walkthrough file:
   - Mark current step `[x] Complete`
   - Add timestamp to Session Log
2. Present next step using the guided implementation format:

```
## Step N: [Component Name]

**Pattern Recognition:**
[Show the SHAPE of what they'll build]

**Let's code:**
Adding TODOs to [FULL PATH TO FILE]:

[code with TODO markers]

**Verify:**
[How to check it works]
```

Then STOP and wait for their code.

## Context Check

If this is step 5+ or conversation is long, remind user:

```
**Quick check:** We've completed [N] steps. Want to /journal before continuing?
```

## If no more steps

```
**Walkthrough complete!**

You've finished all steps. 

**Before you go:**
1. Run /journal to document what you learned
2. Run /recap for the summary

**What's next?**
- Rebuild from scratch tomorrow (muscle memory challenge)
- Extend this with [suggested enhancement]
- Start a new walkthrough with /walkthrough
```

Update walkthrough status to "Complete".

## If no active walkthrough

```
No active walkthrough. Start one with /walkthrough.
```
