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

Advancing requires passing TWO gates. Both must pass — do not skip the second.

### Gate 1 — Does it work?

Check the step is actually built and verified:
```bash
grep -rn "TODO" src/
```

If TODOs remain:
```
You still have TODOs in your code:
[list files with TODOs]

Finish those first, or say "skip" to move on anyway.
```

The user runs the build/test themselves and reports the result — do not run it for them.

### Gate 2 — Can you explain it? (blocking)

⚠️ Do NOT advance until the user explains the step in their own words. Ask:

```
Before we move on — in your own words:
1. What does this code do?
2. Why this approach?
3. What would break if you changed [point at a specific line]?
```

Judge the answer (see references/comprehension-gate.md). Solid → advance. Shallow or wrong → stay on
this step, aim a narrow re-teach at the exact gap, re-check. A step is done when the user can explain
it, not when it merely runs.

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
