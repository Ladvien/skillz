---
description: Move to the next step in the current walkthrough
---

# Next Command

Advance to the next step in the current walkthrough.

## Steps

1. Find current walkthrough in `slop/walkthrough/`
2. Identify which step they're on
3. Mark current step complete
4. Present the next step with TODOs

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

1. Update walkthrough file — mark current step `[x]`
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

## If no more steps

```
**Walkthrough complete!**

You've finished all steps. Run /recap to summarize what you learned.

**What's next?**
- Rebuild from scratch tomorrow (muscle memory challenge)
- Extend this with [suggested enhancement]
- Start a new walkthrough with /walkthrough
```

## If no active walkthrough

```
No active walkthrough. Start one with /walkthrough.
```
