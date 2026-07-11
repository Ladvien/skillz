---
description: Add a deeper, structured entry (a tricky bug, a key decision) to the current session's journal — on top of the automatic per-chunk logging
---

# Journal Command

Routine progress is journaled **automatically** after each copywork chunk and each walkthrough step
(see the skill's "Journal (automatic memory)" section). Use `/journal` when you want to capture
something with more depth than the auto-log — a tricky bug, a non-obvious decision, an "aha" moment.

It appends to the **current session's** journal file in `slop/journal/`, so everything stays on one
timeline.

## Steps

1. Find the current session journal (most recent in `slop/journal/`):
   ```bash
   ls -t slop/journal/*.md 2>/dev/null | head -1
   ```
   If none exists yet, create `slop/journal/YYYY-MM-DD-description.md` (`date +%Y-%m-%d`, ask the user
   for a 2-4 word kebab-case description) with a `# Journal: [date] — [description]` header and a
   `## Log` section.

2. Read the existing entries first so the new one builds on what's there (don't repeat prior notes).

3. Append a structured entry under `## Log`, reviewing: the active walkthrough/copywork doc, recent
   git commits, code changes this session, and the conversation for bugs/solutions.

## Structured Entry Format

```markdown
### [HH:MM] [Title]

**What:** [what was done / what this is about]

**Bug/Challenge:** [symptom → initial hypothesis → investigation → root cause → solution], if any

**Lesson:** [what to remember next time]
```

## Commit

The journal is committed alongside the normal checkpoints. If the user wants it saved now:
```bash
git add slop/journal/
git commit -m "journal: [description]"
```
