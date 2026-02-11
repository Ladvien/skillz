---
description: Read the codebase and document existing features as specs
---

# Document Command

Analyze the codebase and produce feature specs for what already exists. The output is the same format as `/spec` — files in `slop/features/` — so agents have context when working near existing systems.

## When to Use

- User runs `/document`
- Project has existing features that aren't documented
- User wants agents to understand what's already built before adding to it

## Behavior

### 1. Explore the Codebase

Read the project structure, entry points, module declarations, and key files. Understand what systems exist and how they relate.

If `slop/architecture.md` exists, read it first for high-level context.

### 2. Identify Features

Group the codebase into logical features. A "feature" is a cohesive unit of functionality — not a file, not a function, not an entire subsystem.

**Grouping principles:**
- Group by user-facing or system-facing capability, not by file structure
- A feature that spans 3 files is one spec, not three
- A file that contains 2 unrelated features gets split across two specs
- Err on the side of fewer, broader specs over many granular ones
- Utility/infrastructure code that serves multiple features doesn't need its own spec — mention it in the specs that use it

### 3. Propose the Grouping

Before writing anything, show the user your proposed feature list:

```
I'd group the codebase into these features:

1. **Cloud Shadows** — Procedural cloud shadow system driven by noise textures
2. **Wind Noise** — Ambient wind audio that responds to environment state
3. **Time of Day** — [stub] Declared but not yet implemented

Does this grouping make sense? Want to split, merge, or rename any of these?
```

Wait for confirmation before writing specs.

### 4. Write the Specs

For each feature, write to `slop/features/YYYY-MM-DD-description.md` using the template at `commands/templates/feature-spec.md`.

Fill in from what you learned reading the code:

- **Summary**: What this feature does
- **What It Does**: Behavior as observed in the code
- **Scope**: What it covers and what it doesn't
- **Interface**: How other systems interact with it (public API, signals, components, shader globals, etc.)
- **Behavior Details**: Implementation specifics an agent would need to know
- **Acceptance Criteria**: Infer from current behavior — "it currently does X, Y, Z"
- **Technical Notes**: Dependencies, performance characteristics, architectural constraints

Mark anything you're inferring or unsure about with `[INFERRED]`. The user will review.

For features that are stubbed or planned but not implemented, mark status as `Planned` and fill in only what's known.

### 5. Commit

```bash
git add slop/features/
git commit -m "docs: document existing features"
```

Show the user the list of specs created and tell them:
```
Documented N features in slop/features/. Review them and fix anything marked [INFERRED].

These specs give agents context when working on or near these systems. Run /spec to add new features.
```

## What NOT to Do

- Don't create a spec per file — group by feature
- Don't document internal implementation details that are obvious from reading the code
- Don't write specs for trivial glue code or boilerplate
- Don't write specs without proposing the grouping first
- Don't guess at intent — mark it `[INFERRED]` and let the user correct it
