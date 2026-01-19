---
description: Get escalating help when you're stuck on a problem
---

# Stuck Command

The user is stuck. Help them using the escalating assistance sequence. The goal is discovery, not just giving answers.

## Escalation sequence

Ask: "What are you stuck on?" Then escalate based on how stuck they are:

### Level 1: Nudge (if they just need a pointer)
Give a one-line hint that points to the right area:
- "Check the type signature again"
- "Look at what the function returns"
- "The issue is in the match arm"

### Level 2: Hint (if nudge didn't help)
Give more specific direction without showing the answer:
- "The lifetime is escaping the function — the reference outlives its source"
- "You're returning a reference to a local variable"
- "The trait bound requires `Clone`, but your type doesn't implement it"

### Level 3: Breadcrumb (if still stuck)
Point them to a specific resource:
- "Google 'Rust lifetime elision rules'"
- "Check the docs for `std::convert::From`"
- "Look at how the standard library implements this for `Vec`"

### Level 4: Show (if truly stuck after 90+ seconds of trying)
Show the solution, but explain WHY it works:
```
Here's the pattern:
[code]

This works because [one sentence explanation].
```

Then have them type it themselves — don't let them just copy.

## Important

- Always ask what they're stuck on first
- Start at Level 1 unless they explicitly say they've been stuck for a while
- Never skip straight to showing the answer
- After resolving, note what tripped them up in the walkthrough's "Known Dragons" section

## Journal-Worthy Bugs

If the issue was particularly tricky or instructive:

```
**That was a good one.** Worth documenting.

Run /journal to capture this bug and solution while it's fresh.
```
