# Design Patterns Reference

### Scope Management Questions

**Expanding scope (if too narrow):**
- "What's the next problem they'll hit after this one?"
- "Are there related use cases we should consider?"

**Contracting scope (if too broad):**
- "What's the smallest thing we could ship that would be useful?"
- "If you had half the time, what would you cut?"
- "Which of these is a must-have vs. nice-to-have?"

**Detecting scope creep:**
- User keeps adding "and also..."
- Features aren't clearly tied to the stated problem
- No clear definition of done

### Alternative Exploration Questions

**If they can't think of alternatives:**
- "What would you do if [constraint] didn't exist?"
- "How would a senior engineer at [company] approach this?"
- "What's the opposite approach?"
- "Could we solve this without writing code?"
- "Is there an off-the-shelf solution?"

**Evaluating alternatives:**
- "What's the main advantage of this approach?"
- "What's the biggest risk?"
- "How does this scale?"
- "What's the maintenance burden?"

### Trade-off Questions

**Making trade-offs explicit:**
- "What are you optimizing for?"
- "What are you willing to give up?"
- "If you had to pick two of [fast, cheap, good], which two?"

**Common trade-off dimensions:**
| Dimension    | vs.             |
| ------------ | --------------- |
| Simplicity   | Flexibility     |
| Performance  | Maintainability |
| Time to ship | Polish          |
| Generality   | Specificity     |
| Consistency  | Availability    |

## Recognizing Design Smells

### Problem Smells

| Smell               | Example              | Response                          |
| ------------------- | -------------------- | --------------------------------- |
| Solution as problem | "I need a cache"     | "What's slow?"                    |
| Vague problem       | "It's confusing"     | "Who's confused? When?"           |
| No user             | "We should refactor" | "Who benefits?"                   |
| Premature           | "We might need this" | "What's the trigger to build it?" |

### Scope Smells

| Smell         | Example                    | Response                            |
| ------------- | -------------------------- | ----------------------------------- |
| Kitchen sink  | "And also..."              | "Let's focus. What's the MVP?"      |
| No boundaries | Everything is "must have"  | "If you cut one, which?"            |
| Gold plating  | "It should also handle..." | "Is that in the problem statement?" |

### Solution Smells

| Smell              | Example                    | Response                        |
| ------------------ | -------------------------- | ------------------------------- |
| First idea only    | No alternatives considered | "What's another way?"           |
| Complexity worship | Over-engineered            | "What's the simplest version?"  |
| Resume-driven      | "Let's use [hot tech]"     | "Why that over [boring tech]?"  |
| Handwaving         | "We'll figure it out"      | "What specifically is unclear?" |

## Design Document Quality Checklist

Before finalizing a design doc, verify:

### Problem Section
- [ ] States WHO has the problem
- [ ] States WHAT the problem is (not the solution)
- [ ] States WHY it matters now
- [ ] Doesn't smuggle in solution assumptions

### Goals Section
- [ ] Each goal is testable/measurable
- [ ] Goals are prioritized (or all truly equal)
- [ ] Directly tied to the problem statement

### Non-Goals Section
- [ ] Explicitly states what's out of scope
- [ ] Prevents scope creep during implementation
- [ ] Not just "everything else"

### Solution Section
- [ ] High-level enough to understand quickly
- [ ] Detailed enough to implement from
- [ ] Key decisions are called out with reasoning

### Alternatives Section
- [ ] At least 2 alternatives considered
- [ ] Each has pros AND cons
- [ ] Clear reasoning for why not chosen
- [ ] Includes "do nothing" if applicable

### Trade-offs Section
- [ ] Explicitly names what we're optimizing for
- [ ] Explicitly names what we're giving up
- [ ] No pretending there are no trade-offs

### Risks Section
- [ ] Known unknowns are listed
- [ ] Mitigation strategies where possible
- [ ] Open questions that need answering

## Conversation Flow Patterns

### The Funnel Pattern

Start broad, narrow down:
```
Problem space (broad)
    ↓
Specific problem (narrower)
    ↓
Solution space (broad again)
    ↓
Specific solution (narrow)
    ↓
Implementation details (narrowest)
```

### The Ping-Pong Pattern

Alternate between divergent and convergent thinking:
```
Diverge: "What are all the ways we could solve this?"
Converge: "Which of these best fits our constraints?"
Diverge: "What could go wrong with this approach?"
Converge: "Which risks are acceptable?"
```

### The Rubber Duck Pattern

Have them explain it back:
```
"Walk me through how a user would actually use this."
"Explain the data flow from start to finish."
"What happens when [edge case]?"
```

## When to Stop Designing

Design is done when:
- Problem is clearly articulated
- At least one alternative was seriously considered
- Trade-offs are explicit and accepted
- Risks are known (even if not all mitigated)
- Someone else could implement from the doc

Design is NOT done when:
- "We'll figure it out during implementation"
- No alternatives were considered
- Trade-offs are hidden or denied
- The doc is really an implementation plan

## Handoff to Implementation

The design doc should make `/walkthrough` easier:

1. **Goals** → Acceptance criteria for walkthrough
2. **Solution** → Technical approach for walkthrough
3. **Key Decisions** → Guide implementation choices
4. **Risks** → Known dragons to watch for

Link them:
```markdown
# In walkthrough file:
**Design:** [slop/features/YYYY-MM-DD-feature.md](../features/YYYY-MM-DD-feature.md)

# In design file (after implementation):
**Implementation:** [slop/walkthroughs/YYYY-MM-DD-impl.md](../walkthroughs/YYYY-MM-DD-impl.md)
```
