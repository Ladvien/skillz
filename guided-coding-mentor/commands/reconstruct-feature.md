---
description: Analyze a specific feature or change in a project and generate walkthrough documents that teach how to implement it
---

# Reconstruct Feature Command

Analyze a specific feature, PR, branch diff, or set of changes and produce walkthrough documents that teach a developer how to implement that feature against the existing codebase. Every line of changed/added code appears in the walkthroughs. Each step ends in a runnable program.

Works for both your own projects and features in open source repos you want to understand.

## Requirements

- Git repository
- Clear feature scope (branch, commit range, PR, file list, or description)

## Getting the Feature Scope

Ask user how to identify the feature:

1. **Branch diff:** `git diff main..<branch> --stat`
2. **Commit range:** `git diff <start>..<end> --stat`
3. **PR:** User provides PR number or URL; read the diff
4. **File list:** User specifies which files constitute the feature
5. **Description:** User describes the feature; agent identifies relevant files

## Setup

```bash
mkdir -p slop/<project-name>
```

## SCRATCHPAD.md

Initialize at project root if it doesn't exist, or append a new feature section:

```markdown
## Feature: [Feature Name]

**Started:** [YYYY-MM-DD]
**Status:** [Analyzing | Writing | Complete]
**Scope:** [branch/commits/files/PR]

### Changed Files

| File | Change Type | Purpose |
|------|-------------|---------|
| ...  | Added/Modified/Deleted | ... |

### Dependency Analysis

[What existing code does this feature touch? What must the reader understand first?]

### Stubs Tracker

| Stub | Introduced In | Resolved In | Status |
|------|---------------|-------------|--------|
| ...  | Part NN       | Part NN     | [ ]    |

### Walkthrough Plan

| Index | Title | Files Covered | Status |
|-------|-------|---------------|--------|
| 01    | ...   | ...           | [ ]    |

### Current Position

**Writing walkthrough:** [index]
**Notes for next session:** [context]
```

## Phase 1: Analyze the Feature

1. Identify all files changed/added/deleted by the feature
2. Read each changed file — understand what changed and why
3. Map dependencies: what existing code does this touch? What order would a developer implement this in?
4. Identify what context about the existing codebase the reader needs
5. For open source repos: understand the author's intent — read PR description, commit messages, related issues if available

Write the Changed Files table and Dependency Analysis in SCRATCHPAD.md.

## Phase 2: Plan Walkthrough Series

Same principles as `/reconstruct-project`:

- Each walkthrough covers a cohesive unit of the feature
- Each ends with a runnable program
- Build order follows how a developer would implement the feature
- Stubs allowed, tracked in SCRATCHPAD.md, resolved

For smaller features, this may be a single walkthrough document.

Write the plan. Commit. Show user and confirm.

```bash
git add SCRATCHPAD.md slop/
git commit -m "reconstruct-feature: plan for <feature-name>"
```

## Phase 3: Write Walkthroughs

Create `slop/<project-name>/YYYY-MM-DD-feature-description-NN.md`.

### Walkthrough Document Format

````markdown
# [Project Name] — Feature: [Feature Name] — Part NN

**Series:** Implementing [Feature Name] in [Project Name]
**Part:** NN of [total]
**Previous:** [filename or "None"]
**Status:** Complete
**Base:** Assumes working [Project Name] codebase at [commit/branch]

## What We're Building

[1-2 sentences: what this part of the feature adds]

## What Changes After This

[What's different — new behavior, new endpoints, new output]

## Context: Existing Code You Need to Know

[Brief explanation of relevant existing code the reader needs to understand.
Only include this section if the feature touches existing code in non-obvious ways.
For open source repos: explain the conventions/patterns already in use that this feature follows.]

## Steps

### Step 1: [Action]

**Why:** [Why this comes now in the implementation]

**File:** `full/path/to/file.ext` — [New file | Modified]

For **new files**, show complete contents:
```language
[Complete file contents]
```

For **modified files**, show the change with context:
```language
// ... existing code above ...

[new or changed code with surrounding context lines]

// ... existing code below ...
```

**What's happening:** [Explain the change — why this approach, what it enables.
For open source: why did the author make this choice? What's the design insight?]

### Step 2: [Action]

...

## Verify

```bash
[Build/run command]
```

**Expected:** [What you should see]

## What You Learned

- [Pattern or decision worth remembering]

## Stubs Introduced

- [ ] `path/to/file.ext`: `function_name()` — stubbed, implemented in Part [XX]

## Stubs Resolved

- [x] `path/to/file.ext`: `function_name()` — was stubbed in Part [YY]
````

### Writing Rules

Same as `/reconstruct-project`, plus:

1. **Show existing code context** around modifications — enough to locate the change unambiguously.
2. **Don't reproduce unchanged files.** Only show files that are part of the feature.
3. **Explain why the feature works this way**, referencing existing patterns in the codebase.
4. **Track all stubs** in SCRATCHPAD.md.

### After Each Walkthrough Document

Same commit and SCRATCHPAD.md update cycle as `/reconstruct-project`.

## Phase 4: Finalize

1. Verify all changed files are covered
2. Verify no unresolved stubs in SCRATCHPAD.md
3. If 3+ walkthrough docs, write `slop/<project-name>/README-<feature-name>.md` index
4. Update SCRATCHPAD.md feature status to Complete
5. Final commit and push

## Resuming Across Context Windows

Same as `/reconstruct-project` — read SCRATCHPAD.md, read last completed walkthrough, continue.
