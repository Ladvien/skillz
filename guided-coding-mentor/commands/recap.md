---
description: Generate end-of-session summary of what you built and learned
---

# Recap Command

End the current session with a consolidation summary. This reinforces learning and creates a record.

## Steps

1. Read the current walkthrough file from `slop/walkthrough/` to see progress
2. Generate the session summary
3. Update the walkthrough file with final status

## Session summary format

```
**What You Built:** [One sentence describing the feature/component completed]
**What You Learned:** [One sentence naming the key pattern or concept]
**What You Can Now Do:** [One sentence describing the new capability they have]

**Patterns Used:**
- [Pattern 1]: [Where they used it]
- [Pattern 2]: [Where they used it]

**Sticking Points:** [Any concepts that needed extra help, or "None — smooth session!"]

**Muscle Memory Challenge:**
Tomorrow, rebuild [specific thing] from scratch without looking at today's code.
Time yourself. It should take half the time.
```

## Update walkthrough file

After generating the recap, update `slop/walkthrough/NNN.md`:
- Mark completed steps as done `[x]`
- Add session end timestamp
- Add any notes about sticking points for future reference

## If no active walkthrough

If there's no walkthrough file or they haven't been coding:
```
No active walkthrough found. Start one with /walkthrough, or tell me what you've been working on and I'll summarize that.
```
