---
description: Generate end-of-session summary of what you built and learned
---

# Recap Command

End the current session with a consolidation summary. This reinforces learning and creates a record.

## Steps

1. Read the current walkthrough file from `slop/walkthroughs/` to see progress
2. Generate the session summary
3. Update the walkthrough file with final status
4. Prompt for journaling if significant work was done

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

After generating the recap, update `slop/walkthroughs/YYYY-MM-DD-description.md`:
- Mark completed steps as done `[x]`
- Add session end timestamp to Session Log
- Update status if complete

## Prompt for Journal

After the recap, always ask:

```
**Document this session?**

We solved some interesting problems today. Run /journal to capture:
- Bugs and how we fixed them
- Patterns you learned
- What to remember next time

This becomes valuable reference material. Want me to start the journal entry?
```

If user says yes, transition to /journal flow.

## If no active walkthrough

If there's no walkthrough file or they haven't been coding:
```
No active walkthrough found. Start one with /walkthrough, or tell me what you've been working on and I'll summarize that.
```

## Commit Progress

```bash
git add slop/walkthroughs/
git commit -m "walkthrough: session progress update"
```
