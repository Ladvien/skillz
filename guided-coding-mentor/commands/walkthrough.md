---
description: Start a guided coding walkthrough where you write every line of code yourself
---

# Walkthrough Command

Start a guided coding session using the guided-coding-mentor skill. The agent first plans, then builds and proves the feature works, documents it, then guides the user to implement it themselves.

## Phase 1: Setup

1. Ask what the user wants to build (or reference a spec from `slop/features/`)
2. Verify this is a git repository:
   ```bash
   git rev-parse --is-inside-work-tree
   ```
   If not a git repo, stop and tell user: "This must be run inside a git repository."

3. Commit and push all current changes (safety checkpoint):
   ```bash
   git add -A
   git commit -m "checkpoint: pre-walkthrough state" --allow-empty
   git push
   ```
   If push fails, stop and tell user: "Push failed. Fix remote issues before starting walkthrough."

4. Record the checkpoint commit:
   ```bash
   git rev-parse HEAD
   ```
   Store this hash for later reset.

## Phase 2: Plan (NEW - Write Before Building)

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

## Goal

[One clear sentence describing what we're building]

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]

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

## Phase 3: Prove It Works

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

## Phase 4: Document

1. Update the walkthrough file with implementation details:
   - Fill in the Steps section with pedagogical guidance
   - Add any dragons/pitfalls discovered during implementation
   - Update status to "Proven"

2. Copy walkthrough file to temp location:
   ```bash
   mkdir -p /tmp/walkthrough-preserve
   cp slop/walkthroughs/YYYY-MM-DD-description.md /tmp/walkthrough-preserve/
   ```

## Phase 5: Reset

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

## Phase 6: Guide

Now guide the user through implementing it themselves:

1. Tell user: "I've proven this works and documented the approach. Now you'll build it yourself."
2. Follow standard guided-coding-mentor skill workflow:
   - Present first step with TODOs
   - User writes code
   - Verify each step
   - Progress through walkthrough doc
3. Reference the walkthrough file for steps, but deliver via TODO-driven workflow
4. Update walkthrough status to "In Progress" and track completed steps

## Walkthrough Doc Format (Final)

```markdown
# Walkthrough: [Feature Name]

**Date:** [YYYY-MM-DD]
**Status:** [Planning | Proven | In Progress | Complete]
**Checkpoint:** [commit hash]

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

[Link to dev_journal entries if applicable, or inline notes]
```

## Context Management

If the conversation is getting long during a walkthrough, prompt the user:

```
**Context Check:** We've been at this a while. Before continuing:

1. Run /journal to capture bugs and solutions
2. Your progress is saved in the walkthrough file

Ready to continue, or take a break?
```
