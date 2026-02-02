---
description: Design a feature through guided conversation before implementation
---

# Design Command

Guide the user through designing a feature via structured conversation. Push back on weak reasoning, explore alternatives, and produce a design document that feeds into `/walkthrough`.

## When to Use

- User runs `/design`
- User wants to think through a feature before building
- User says "I want to build X" but hasn't thought through the design

## Flow

1. **Problem discovery** — What are we solving?
2. **Constraints & scope** — What are the boundaries?
3. **Solution exploration** — How might we solve it?
4. **Alternatives** — What else could we do?
5. **Trade-offs & risks** — What are we giving up?
6. **Document** — Write `slop/features/YYYY-MM-DD-description.md`
7. **Handoff** — Prompt for `/walkthrough` to implement

## Phase 1: Problem Discovery

Start with:
```
What problem are you trying to solve?

Don't tell me the solution yet — describe the pain point, who has it, and why it matters.
```

Probe deeper:
- "Who specifically experiences this problem?"
- "What happens if we don't solve it?"
- "Why solve it now vs. later?"
- "How do you know this is a real problem?"

**Red flags to push back on:**
- Solution masquerading as problem ("I need to add a cache")
- Vague problem statements ("It's slow")
- No clear user/stakeholder

## Phase 2: Constraints & Scope

```
What are the hard constraints?

Think about:
- Time/deadline pressures
- Technical limitations (language, framework, existing code)
- Dependencies on other systems/people
- What's explicitly OUT of scope
```

Capture:
- **Goals**: What MUST this do to be successful?
- **Non-Goals**: What are we explicitly NOT doing?

Push back if:
- Scope is too large ("Can we ship something smaller first?")
- No clear success criteria
- Everything is a "must have"

## Phase 3: Solution Exploration

```
Now let's talk solutions. What's your current thinking?

Walk me through the high-level approach.
```

Probe the design:
- "How does this fit with the existing codebase?"
- "What's the data flow?"
- "Where does complexity live?"
- "What's the API/interface look like?"

**Do NOT accept the first solution uncritically.** Ask:
- "What's the simplest version of this?"
- "What would you do if you had half the time?"

## Phase 4: Alternatives

```
What other approaches did you consider?

Even if you're confident in your solution, let's sanity-check it against alternatives.
```

If they can't name alternatives, suggest some:
- "Could you use an existing library/tool?"
- "Could you solve this without writing code?"
- "What's the opposite approach?"
- "How would [senior engineer] approach this?"

For each alternative, capture:
- Pros
- Cons  
- Why it wasn't chosen

**This is the most valuable section.** Future-you will thank present-you for documenting why you DIDN'T do something.

## Phase 5: Trade-offs & Risks

```
What are you giving up with this approach?

Every design has trade-offs. Let's name them explicitly.
```

Probe:
- "What could go wrong?"
- "What are you uncertain about?"
- "What assumptions are you making?"
- "Where might this break at scale?"

Capture:
- Known trade-offs (what we're optimizing for vs. against)
- Risks (things that could go wrong)
- Open questions (things we don't know yet)

## Phase 6: Document

Generate filename:
```bash
date +%Y-%m-%d
```
Ask user for a brief description (2-4 words, kebab-case).

Create directory:
```bash
mkdir -p slop/features
```

Write to `slop/features/YYYY-MM-DD-description.md` using the template below.

## Document Template

```markdown
# Feature: [Name]

**Date:** [YYYY-MM-DD]
**Status:** Draft

## Problem

[What problem are we solving? Who has it? Why now?]

## Goals

- [Must have 1]
- [Must have 2]

## Non-Goals

- [Explicitly out of scope 1]
- [Explicitly out of scope 2]

## Proposed Solution

[High-level description of the approach]

### How It Works

[More detail on the mechanism/flow]

### Key Decisions

- **[Decision 1]**: [Choice] because [reasoning]
- **[Decision 2]**: [Choice] because [reasoning]

## Alternatives Considered

### [Alternative A]

**Approach:** [Brief description]

**Pros:**
- [Pro 1]

**Cons:**
- [Con 1]

**Why not:** [Reason this wasn't chosen]

### [Alternative B]
...

## Trade-offs

| Optimizing For | Giving Up |
|----------------|-----------|
| [Thing 1]      | [Thing 2] |

## Risks & Open Questions

- **[Risk 1]**: [Description and mitigation if known]
- **[Open Question]**: [Thing we need to figure out]

## Next Steps

- [ ] Review design
- [ ] Run `/walkthrough` to implement

---
*Design conversation: [timestamp]*
```

## Phase 7: Handoff

After writing the document:

```
**Design documented:** slop/features/YYYY-MM-DD-description.md

Ready to build this? Run `/walkthrough` and I'll guide you through implementation.

Or if you want to sit with it:
- Share with a colleague for review
- Sleep on it and revisit tomorrow
- Run `/design` again if the problem changes
```

Commit the design:
```bash
git add slop/features/
git commit -m "design: [description]"
```

## Conversation Style

**Be Socratic, not interrogative.** Guide them to better thinking, don't grill them.

**Push back constructively:**
- ❌ "That won't work"
- ✅ "What happens when [edge case]?"

**Name the pattern:**
- "That's premature optimization — let's validate the problem first"
- "You're describing a solution, not a problem"
- "That's scope creep — should it be a non-goal?"

**Keep it moving.** If they're stuck on a question for more than 2 exchanges, note the uncertainty and move on. Not everything needs to be resolved in the design phase.

## If Design Is Too Small

For trivial features (< 1 hour of work):

```
This seems straightforward enough that a full design doc might be overkill.

Want to:
1. Skip straight to `/walkthrough`?
2. Do a mini-design (just problem + solution + one alternative)?
```

## If Design Is Too Large

For features that span multiple systems/weeks:

```
This is a big one. Let's break it down.

What's the smallest useful slice we could ship first?
```

Guide them to identify an MVP, then design that.

## Integration with /walkthrough

When user runs `/walkthrough` after `/design`:
1. Check for recent design doc in `slop/features/`
2. Reference the design doc in the walkthrough plan
3. Use the design's "Proposed Solution" as the basis for implementation steps

The walkthrough file should link back:
```markdown
**Design:** [slop/features/YYYY-MM-DD-description.md](../features/YYYY-MM-DD-description.md)
```
