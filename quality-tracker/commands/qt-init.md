---
description: Initialize quality tracking for a project with project-specific evaluation dimensions
---

# QT Init Command

Set up quality tracking for the current project. Agent proposes evaluation dimensions based on the codebase, user approves or edits.

## When to Use

- User runs `/qt-init`
- Starting a new project that should be quality-tracked
- No `slop/quality-tracker/config.json` exists yet

## Behavior

### 1. Read the Codebase

Before proposing anything, understand what the project is:

```bash
find . -type f -name "*.rs" -o -name "*.gd" -o -name "*.ts" -o -name "*.py" | head -50
```

Read key files: entry points, READMEs, architecture docs. Check for `slop/architecture.md`.

### 2. Propose Evaluation Dimensions

Based on what the project is, propose 3-5 dimensions that matter. Each dimension has a short name and a one-line description.

**Guidelines for choosing dimensions:**
- Pick things the user will actually have opinions about after every change
- Avoid abstract metrics that are hard to score (don't use "maintainability")
- Lean toward observable qualities ("does it look right?", "does it feel responsive?")
- Include at least one code-quality dimension if the user is writing code themselves
- Match the domain — a game needs different dimensions than a CLI tool

**Example for a game project:**
```
I'd suggest tracking these dimensions:

1. **visual_quality** — Does it look right? Art style, rendering, visual polish.
2. **gameplay_feel** — Does it feel good to play? Controls, responsiveness, feedback.
3. **performance** — Does it run smoothly? Framerate, load times, stutters.
4. **code_clarity** — Is the code understandable? Could you work on it tomorrow?

Want to adjust any of these, or add/remove dimensions?
```

**Example for a web API:**
```
1. **correctness** — Does it return the right data? Edge cases handled?
2. **performance** — Response times acceptable? No unnecessary work?
3. **error_handling** — Does it fail gracefully? Clear error messages?
4. **code_clarity** — Is the code understandable?
```

Wait for user approval. They may rename, add, remove, or restructure.

### 3. Write Config

```bash
mkdir -p slop/quality-tracker
```

Write `slop/quality-tracker/config.json`:
```json
{
    "project": "<project-name>",
    "dimensions": [
        {"name": "dimension_name", "description": "One-line description"}
    ],
    "created": "<YYYY-MM-DD>",
    "last_updated": "<YYYY-MM-DD>"
}
```

### 4. Initialize the Log

Write `slop/quality-tracker/feedback-log.md`:
```markdown
# Quality Feedback Log

**Project:** <project-name>
**Tracking since:** <YYYY-MM-DD>

**Dimensions:**
- **dimension_name**: description
- ...

---

```

### 5. Commit

```bash
git add slop/quality-tracker/
git commit -m "quality-tracker: initialize for <project-name>"
```

Tell the user:
```
Quality tracking initialized.

After every code change, I'll ask you to rate these dimensions and share your thoughts.
Run /qt-eval after any change, or I'll prompt you automatically.
```

## Updating Dimensions

If `config.json` already exists and the user wants to change dimensions:

1. Read current config
2. Ask what they want to add/remove/rename
3. Update config
4. Update the log header
5. Commit with: `quality-tracker: update dimensions — [what changed]`

Note: Old log entries keep their original dimensions. New entries use the updated set.

## What NOT to Do

- Don't propose more than 5 dimensions
- Don't use vague dimensions ("quality", "goodness")
- Don't skip reading the codebase — your proposals should be project-specific
- Don't add dimensions the user didn't approve
