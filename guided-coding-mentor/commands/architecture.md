---
description: Document the overall project architecture so feature specs and agents have shared context
---

# Architecture Command

Help the user describe the big picture of their project — what it is, how it's structured, what the major systems are, and how they relate. This produces a living document that feature specs reference for context.

## When to Use

- User runs `/architecture`
- User is starting a new project and wants to lay out the structure
- The project has grown and needs its architecture documented
- No `slop/architecture.md` exists yet and the user is writing specs

## Behavior

### 1. Explore the Codebase First

Before asking the user anything, look at the project:

```bash
# Get the lay of the land
find . -type f -name "*.rs" -o -name "*.gd" -o -name "*.ts" -o -name "*.py" | head -50
```

Read key files: entry points, module declarations, config files, READMEs. Understand what already exists before asking the user to explain it.

### 2. Ask What's Not Obvious from Code

After exploring, ask about things you can't infer:

- **Intent**: "What is this project? One sentence." (The README might say, but the user's mental model matters more.)
- **Major systems**: "What are the big pieces?" (You may have identified these from code — confirm or correct.)
- **System relationships**: "How do these systems talk to each other?"
- **Conventions**: "Any patterns or conventions you're following?" (Naming, file organization, architectural patterns.)
- **External dependencies**: "What external systems/crates/plugins does this rely on and why?"
- **Future direction**: "What major systems are planned but not built yet?"

Same rule as `/spec` — batch questions, skip what you already know from the code.

### 3. Write the Architecture Doc

Write to `slop/architecture.md` using the template at `commands/templates/architecture.md`.

Fill it in from the conversation and your codebase exploration. Mark anything you inferred but aren't sure about with `[INFERRED]`.

### 4. Commit

```bash
git add slop/architecture.md
git commit -m "docs: project architecture"
```

Show the user the doc and tell them:
```
Architecture documented at slop/architecture.md

Feature specs will reference this for context. Update it as the project evolves — run /architecture again anytime.
```

## Updating an Existing Architecture Doc

If `slop/architecture.md` already exists:
1. Read it
2. Ask the user what's changed or what they want to add
3. Update the relevant sections
4. Commit with message `docs: update architecture — [what changed]`

## What NOT to Do

- Don't make this an interrogation — you have a codebase, use it
- Don't write a novel — this doc should be scannable in 2 minutes
- Don't document implementation details — that's what code comments and specs are for
- Don't prescribe architecture — document what IS, not what you think it should be
