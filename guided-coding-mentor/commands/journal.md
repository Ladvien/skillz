---
description: Document what was done, issues encountered, and solutions found
---

# Journal Command

Create a detailed dev journal entry documenting work done, bugs encountered, and solutions found.

## When to Use

- User runs `/journal`
- Agent detects context is getting low (proactively prompt user)
- End of a significant work session
- After resolving a tricky bug

## Steps

1. Determine journal filename:
   ```bash
   date +%Y-%m-%d
   ```
   Ask user for a brief description (2-4 words, kebab-case) for the filename.

2. Create journal directory if needed:
   ```bash
   mkdir -p slop/dev_journal
   ```

3. Generate journal entry by reviewing:
   - Current walkthrough file (if active)
   - Recent git commits
   - Code changes made this session
   - Conversation history for bugs/solutions

4. Write to `slop/dev_journal/YYYY-MM-DD-description.md`

## Journal Entry Format

```markdown
# Dev Journal: [Date] - [Description]

**Session Duration:** [approximate time spent]
**Walkthrough:** [link to active walkthrough if any, or "None"]

## What We Did

[Narrative description of work accomplished. Be specific about features, components, and patterns implemented.]

## Bugs & Challenges

### [Bug/Challenge 1 Title]

**Symptom:** [What was happening]

**Initial Hypothesis:** [What we thought was wrong]

**Investigation:** [What we tried, what we learned]

**Root Cause:** [The actual problem]

**Solution:** [How we fixed it]

**Lesson:** [What to remember for next time]

### [Bug/Challenge 2 Title]
...

## Code Changes Summary

- `path/to/file.rs`: [what changed and why]
- `path/to/other.rs`: [what changed and why]

## Patterns Learned

- **[Pattern Name]**: [Brief description of when/why to use it]

## Open Questions

- [Any unresolved questions or future considerations]

## Next Session

[What to pick up next time]
```

## Context-Low Detection

When the agent detects context is getting low (conversation is long, lots of code discussed), proactively prompt:

```
**Context Check:** We've covered a lot of ground. Before we continue, let's capture what we've done.

Run /journal to document:
- The bugs we solved
- The patterns we used  
- Where we left off

This ensures nothing gets lost if the conversation resets.
```

## If No Significant Work Done

```
Nothing substantial to journal yet. Keep coding and run /journal when you've:
- Solved a tricky bug
- Implemented a feature
- Learned something worth remembering
```

## Commit the Journal

After writing the journal:
```bash
git add slop/dev_journal/
git commit -m "journal: [description]"
```

Optionally push if user confirms.
