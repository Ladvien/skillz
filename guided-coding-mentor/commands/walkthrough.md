---
description: Start a guided coding walkthrough where you write every line of code yourself
---

# Walkthrough Command

Start a guided coding session using the guided-coding-mentor skill. The agent first builds and proves the feature works, documents it, then guides the user to implement it themselves.

## Phase 1: Setup

1. Ask what the user wants to build
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

## Phase 2: Prove It Works

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

## Phase 3: Document

1. Determine next walkthrough index:
   ```bash
   ls slop/walkthrough/*.md 2>/dev/null | wc -l
   ```
2. Create `slop/walkthrough/NNN.md` with cleaned-up pedagogical guide:
   - Build order with reasoning
   - Step-by-step instructions (what user will implement)
   - Key patterns and concepts
   - Known pitfalls encountered during implementation
3. Copy walkthrough file to temp location:
   ```bash
   mkdir -p /tmp/walkthrough-preserve
   cp slop/walkthrough/NNN.md /tmp/walkthrough-preserve/
   ```

## Phase 4: Reset

1. Hard reset to checkpoint:
   ```bash
   git reset --hard <checkpoint-commit-hash>
   ```
2. Restore and commit walkthrough doc:
   ```bash
   mkdir -p slop/walkthrough
   cp /tmp/walkthrough-preserve/NNN.md slop/walkthrough/
   git add slop/walkthrough/NNN.md
   git commit -m "docs: add walkthrough NNN"
   git push
   ```
3. Clean up:
   ```bash
   rm -rf /tmp/walkthrough-preserve
   ```

## Phase 5: Guide

Now guide the user through implementing it themselves:

1. Tell user: "I've proven this works and documented the approach. Now you'll build it yourself."
2. Follow standard guided-coding-mentor skill workflow:
   - Present first step with TODOs
   - User writes code
   - Verify each step
   - Progress through walkthrough doc
3. Reference the walkthrough file for steps, but deliver via TODO-driven workflow

## Walkthrough Doc Format

```markdown
# Walkthrough NNN: [Feature Name]

**Started:** [timestamp]
**Goal:** [one sentence]
**Proven:** Yes - implementation verified before teaching

## Build Order
1. [Component]: [Why first]
2. [Component]: [What it enables]
3. [Component]: [Why it matters]

## Steps

### Step 1: [Component Name]
**What you'll build:** [description]
**Key pattern:** [pattern name]

[Code structure with TODO markers - what user will fill in]

**Verify:** [how to check it works]

### Step 2: ...

## Known Dragons
- [Issue encountered]: [How to avoid/fix]

## Session Notes
[Space for observations during guided implementation]
```
