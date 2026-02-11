---
description: Specify a feature clearly enough that an agent can build it without going sideways
---

# Spec Command

Help the user articulate what they want to build and document it as a feature spec. The goal is a clear, unambiguous document that any agent (or future-you) can implement from without guessing.

**This is not a design review.** The user knows what they want. Your job is to help them say it precisely and catch gaps that would cause an agent to stall or make wrong assumptions.

## When to Use

- User runs `/spec`
- User describes a feature they want to build
- User wants to document a feature before handing it to an agent

## Behavior

### 1. Listen First

Let the user describe what they want. Don't interrupt with "but what's the problem?" — they're telling you what to build, not asking for permission.

### 2. Ask Clarifying Questions (Only What's Missing)

After they describe the feature, identify gaps that would block implementation. Ask about:

- **Boundaries**: What's in scope, what's not? ("Does the time-of-day system also handle seasons, or just daily cycles?")
- **Interfaces**: How does this connect to other systems? ("What does a consumer of this system need to call or listen to?")
- **Behavior**: What happens in edge cases or transitions? ("What happens at the boundary between night and dawn?")
- **Constraints**: Technical requirements that affect implementation. ("Does this need to run at a fixed timestep?")
- **Acceptance**: How do we know it's done? ("What does 'working' look like for this feature?")

Ask only what's genuinely unclear. If the user gave you enough to write a spec, write the spec. Don't manufacture questions to seem thorough.

### 3. Batch Your Questions

Don't drip-feed one question at a time across ten turns. Group your clarifying questions into a single message. If you have zero questions, skip straight to writing the spec.

### 4. Write the Spec

Generate filename from date + user's description (kebab-case):

```bash
mkdir -p slop/features
```

Write to `slop/features/YYYY-MM-DD-description.md` using the template at `commands/templates/feature-spec.md`.

Fill it in based on the conversation. For sections the user didn't address, use your best judgment and mark assumptions with `[ASSUMPTION]` so they can review.

### 5. Commit and Confirm

```bash
git add slop/features/
git commit -m "spec: [description]"
```

Show the user the spec. Tell them:
```
Spec written to slop/features/YYYY-MM-DD-description.md

Review it and let me know if anything needs adjusting. When you're ready to build, hand this to an agent or run /walkthrough.
```

## What NOT to Do

- Don't challenge whether they should build the feature
- Don't suggest alternatives unless they ask
- Don't ask "who is this for" — they're building a game, it's for players
- Don't lecture about trade-offs they didn't ask about
- Don't drag a 2-minute spec into a 20-minute Socratic dialogue
- Don't ask questions you can answer yourself from the codebase

## Referencing Architecture

If an architecture doc exists at `slop/architecture.md`, read it before asking questions. Many answers about project structure, conventions, and system boundaries are already there. Don't re-ask what's documented.

When writing the spec, reference the architecture doc for context on how this feature fits into the larger system.

## Integration with /walkthrough

When user runs `/walkthrough` after `/spec`:
1. Check for relevant spec in `slop/features/`
2. Use the spec as the basis for the implementation plan
3. Link the walkthrough back to the spec
