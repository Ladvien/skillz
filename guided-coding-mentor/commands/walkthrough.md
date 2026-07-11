---
description: Start a guided coding walkthrough where you write every line of code yourself
---

# Walkthrough Command

Start a guided coding session using the guided-coding-mentor skill. The agent first plans, then builds and proves the feature works, documents it, then guides the user to implement it themselves.

## Phase 1: Setup

Before anything else, **read prior history** so you build on past work and decisions:
```bash
ls -t slop/journal/*.md 2>/dev/null | head
```
Skim the recent entries.

1. **Establish the Learning Focus first.** Before anything else, ask:

   ```
   What skill would you like to work on today?
   ```

   Capture the answer — a coding competency to practice this session (e.g. lifetimes, async
   streaming, error handling, recursion). This is the **Learning Focus** and it anchors the rest of
   the session. The feature is the vehicle; the focus is the point.

2. Ask what the user wants to build. Steer the feature so it actually exercises the Learning Focus —
   if they have no feature in mind, propose 2-3 small ones that would train it.
3. Verify this is a git repository:
   ```bash
   git rev-parse --is-inside-work-tree
   ```
   If not a git repo, stop and tell user: "This must be run inside a git repository."

4. Commit and push all current changes (safety checkpoint):
   ```bash
   git add -A
   git commit -m "checkpoint: pre-walkthrough state" --allow-empty
   git push
   ```
   If push fails, stop and tell user: "Push failed. Fix remote issues before starting walkthrough."

5. Record the checkpoint commit:
   ```bash
   git rev-parse HEAD
   ```
   Store this hash for later reset.

6. Create the session journal `slop/journal/YYYY-MM-DD-description.md` with a header
   (`# Journal: [date] — [description]`, `**Mode:** walkthrough`, `**Learning Focus:** [focus]`) and a
   `## Log` section. It's appended to automatically as steps complete.

## Phase 2: Research (do your homework before designing)

Before designing anything, run **all three research lanes** (see SKILL.md "Research First"). Designing
from cold knowledge misses what's already in the repo, gets the domain subtly wrong, and reaches for
stale APIs. A lane that finds nothing relevant is reported as empty — never skipped silently.

1. **Codebase lane** — explore the repo for existing functions, utilities, conventions, and patterns
   to **reuse**, and the idioms the new code should match. Launch the Explore agent / Grep / Glob /
   Read.
2. **Literature lane** — search academic sources for prior art and correct approaches. Use an
   academic-search MCP if available — e.g. **home-still**: `paper_search` (discover),
   `abstract_search` / `distill_search` (semantic search over indexed papers), `paper_get`. With no
   such MCP, use scholarly web search.
3. **Web lane** — `WebSearch` / `WebFetch` for current library/API docs, version-specific behavior,
   and real-world best practice.

Cross-reference the lanes (codebase vs literature vs current docs; call out conflicts), then present a
short **Research / Prior Art** summary and confirm with the user before drafting the plan:

```
Here's what I found before designing:
- **Reuse from codebase:** [existing utilities/patterns + full paths]
- **Literature:** [papers/citations, or "none applicable"]
- **Web / docs:** [links + version notes]
- **How it shapes the approach:** [1–2 lines]

Look right before I write the plan?
```

## Phase 3: Plan (NEW - Write Before Building)

Before writing any code, create the walkthrough plan document.

1. Generate filename:
   ```bash
   date +%Y-%m-%d
   ```
   Use format: `YYYY-MM-DD-feature-description.md` (kebab-case description)

2. Create walkthrough directory:
   ```bash
   mkdir -p slop/walkthroughs
   ```

3. Write the pre-plan to `slop/walkthroughs/YYYY-MM-DD-description.md`:

```markdown
# Walkthrough: [Feature Name]

**Date:** [YYYY-MM-DD]
**Status:** Planning
**Checkpoint:** [commit hash from Phase 1]
**Learning Focus:** [the competency being practiced this session]

## Goal

[One clear sentence describing what we're building]

**How this exercises the focus:** [one line — why this feature trains the Learning Focus]

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]

## Research / Prior Art

- **Reuse from codebase:** [existing utilities/patterns to build on — full paths]
- **Literature:** [papers/citations from the literature lane, or "none applicable"]
- **Web / docs:** [library/API docs + version notes from the web lane]
- **How this shaped the approach:** [what the research changed about the design]

## Technical Approach

### Architecture

[How this fits into the existing codebase. What components are involved.]

### Key Decisions

- **[Decision 1]**: [Choice] because [reasoning]
- **[Decision 2]**: [Choice] because [reasoning]

### Dependencies

- [External crate/library if any]
- [Internal modules this will use]

### Files to Create/Modify

- `path/to/new_file.rs`: [purpose]
- `path/to/existing.rs`: [what changes]

## Build Order

1. **[Component 1]**: [Why first - what it enables]
2. **[Component 2]**: [What it depends on, what it enables]
3. **[Component 3]**: [Why this order matters]

## Anticipated Challenges

- **[Potential issue]**: [Mitigation strategy]
- **[Potential issue]**: [Mitigation strategy]

## Steps (To Be Filled During Proof Phase)

[This section will be populated after we build and verify the implementation]

---
*Plan created: [timestamp]*
*Implementation proven: [to be updated]*
*User implementation started: [to be updated]*
```

4. Commit the plan:
   ```bash
   git add slop/walkthroughs/
   git commit -m "walkthrough: plan for [description]"
   ```

5. Show user the plan and ask: "Does this approach look right before I build it?"

## Phase 4: Prove It Works

1. Implement the feature fully (agent writes all code)
2. Build/compile to verify:
   ```bash
   # Language-appropriate build command
   cargo build  # Rust
   npm run build  # Node
   go build  # Go
   # etc.
   ```
3. If build fails, iterate until it compiles
4. Demo to user: show them the working feature, explain what it does
5. Ask user: "Does this work as expected?"
6. If user says no, iterate on implementation until approved
7. Commit the working implementation:
   ```bash
   git add -A
   git commit -m "walkthrough: working implementation"
   ```

## Phase 5: Document

1. Update the walkthrough file with implementation details:
   - Fill in the Steps section with pedagogical guidance
   - Add any dragons/pitfalls discovered during implementation
   - Update status to "Proven"

2. Copy walkthrough file to temp location:
   ```bash
   mkdir -p /tmp/walkthrough-preserve
   cp slop/walkthroughs/YYYY-MM-DD-description.md /tmp/walkthrough-preserve/
   ```

## Phase 6: Reset

1. Hard reset to checkpoint:
   ```bash
   git reset --hard <checkpoint-commit-hash>
   ```
2. Restore and commit walkthrough doc:
   ```bash
   mkdir -p slop/walkthroughs
   cp /tmp/walkthrough-preserve/*.md slop/walkthroughs/
   git add slop/walkthroughs/
   git commit -m "walkthrough: [description] - ready for user implementation"
   git push
   ```
3. Clean up:
   ```bash
   rm -rf /tmp/walkthrough-preserve
   ```

## Phase 7: Guide

Now guide the user through implementing it themselves:

1. Tell user: "I've proven this works and documented the approach. Now you'll build it yourself."
2. Run the guide loop for every step (see SKILL.md "Phase 3: Guide"):
   - **Present** the step — lead with the progress bar (`Step n/total`, total = number of Steps in
     the walkthrough doc; see SKILL.md "Progress Bar"), then TODO markers — the shape, never the
     solution. Put the TODO at the delta only, anchored with context (`...`); never re-state
     unchanged code; mark the TODO/changed line inline where it sits (`# <-- add this`) so they never
     diff against their file by eye (see SKILL.md "Guidance Format")
   - **Wait** for the user to write the code; do not write it for them
   - **Guide them to verify** — tell them what to run; *they* run it and report the result
   - **Comprehension gate** — they explain what it does, why, and what would break if a key line
     changed (see references/comprehension-gate.md). Aim these questions at the **Learning Focus**
     first whenever the step touches it.
   - **Advance only when the explanation is solid.** Shallow/wrong → re-teach the gap, re-check
   - **Auto-journal** — append a short entry for the step to the session journal (no prompt)
3. Reference the walkthrough file for steps (including its **Learning Focus** header), but deliver
   via the TODO-driven loop above
4. Update walkthrough status to "In Progress" and track completed steps

## Walkthrough Doc Format (Final)

```markdown
# Walkthrough: [Feature Name]

**Date:** [YYYY-MM-DD]
**Status:** [Planning | Proven | In Progress | Complete]
**Checkpoint:** [commit hash]
**Learning Focus:** [the competency being practiced this session]

## Goal

[One clear sentence describing what we're building]

## Acceptance Criteria

- [x] [Completed criterion]
- [ ] [Pending criterion]

## Technical Approach

### Architecture
[How this fits into the existing codebase]

### Key Decisions
- **[Decision]**: [Choice] because [reasoning]

### Files to Create/Modify
- `path/to/file.rs`: [purpose]

## Build Order

1. **[Component]**: [Why this order]

## Steps

### Step 1: [Component Name]

**What you'll build:** [description]
**Key pattern:** [pattern name]
**Status:** [ ] Not started / [~] In progress / [x] Complete

```rust
// Full path: src/example.rs

// TODO: [Specific instruction]
```

**Verify:** [how to check it works]

### Step 2: ...

## Known Dragons

- **[Issue encountered]**: [How to avoid/fix]

## Session Log

- [timestamp]: Started planning
- [timestamp]: Implementation proven
- [timestamp]: User began implementation
- [timestamp]: Step 1 complete
- ...

## Bugs Encountered

[Link to slop/journal entries if applicable, or inline notes]
```

## Context Management

If the conversation is getting long during a walkthrough, prompt the user:

```
**Context Check:** We've been at this a while. Before continuing:

1. Run /journal to capture bugs and solutions
2. Your progress is saved in the walkthrough file

Ready to continue, or take a break?
```
