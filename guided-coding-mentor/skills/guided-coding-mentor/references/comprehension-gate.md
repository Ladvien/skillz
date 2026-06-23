# The Comprehension Gate (Explain-Back)

The gate is what separates this skill from autocomplete. Code that *works* but that the user can't
*explain* is a maintenance liability. A step is not complete until the user can explain it.

## When the gate fires

After the user has written a step's code AND verified it works (they ran the check themselves),
before `/next` advances.

## The prompt

Keep it short and non-patronizing. Ask for three things:

```
Before we move on — in your own words:
1. What does this code do?
2. Why this approach over the obvious alternative?
3. What would break if you changed [point at a specific line]?
```

Adapt #3 to the actual code: name the line, guard, type, or call that carries the real weight.

## What counts as passing

A passing explanation:
- Is in the user's **own words**, not a re-read of the code or your TODO.
- Covers **what** it does at the right altitude (behavior, not a line-by-line transcript).
- Gives a real **why** — the tradeoff, not "because it works".
- Names a plausible **failure mode** for #3.

A failing explanation:
- Parrots the TODO or the variable names back.
- "It just works" / "you told me to" with no reasoning.
- Gets the failure mode wrong, revealing a mental-model gap.

## On a failed explanation — do NOT advance

Aim a narrow re-teach at the exact gap, then re-check. Do not re-lecture the whole step.

1. Point at the specific line or concept the explanation missed.
2. Ask one tighter question that isolates it.
3. If still stuck, climb the escalation ladder (Nudge → Hint → Breadcrumb → Show) on that one point.
4. Re-ask the failing part of the explanation. Advance only when it lands.

If a gap was genuinely hard, add it to the walkthrough's Known Dragons and consider prompting for
`/journal`.

## Examples

**Rust — passing:**
> "`board.iter()` returns an iterator of `(Position, Cell)` instead of cloning the grid, so callers
> walk it lazily. I used `impl Iterator` to avoid naming the concrete type. If I dropped the
> lifetime tie to `&self`, the iterator could outlive the board and dangle."

**Python — failing (parroting), and the re-teach:**
> User: "It makes `__iter__` yield the tuples, like the TODO said."
>
> Agent: "That's the *what* from the TODO. Why does `__iter__` return a generator instead of a list
> — what does the caller get differently?" → narrow re-check, not a restart.
