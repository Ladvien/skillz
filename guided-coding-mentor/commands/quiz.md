---
description: Quick pattern check quiz on recent code you've written
---

# Quiz Command

Test the user's understanding of patterns they've recently implemented. Do NOT test memorization — test reasoning.

## How to quiz

1. Look at the current walkthrough file in `slop/walkthrough/` to see what they've been working on
2. Pick a pattern or concept they've used 2-3 times
3. Ask ONE question that requires explaining "why", not "what"

## Quiz format

```
**Pattern Check:** You've used [pattern] [N] times now.
[Single question about WHY this pattern works or what problem it solves]
```

Then WAIT for their answer. After they respond:
- If correct: Acknowledge briefly, add one insight they might not have considered
- If partial: Confirm what's right, probe the missing piece with a follow-up
- If wrong: Don't say "wrong" — ask a clarifying question that leads them to the answer

## Example quizzes

- "You've used `Box<dyn Error>` three times. What problem does Boxing solve that `impl Error` wouldn't?"
- "We've been using `?` everywhere. What happens if you use it in a function that returns `()`?"
- "You chose `&str` over `String` for that parameter. When would you need `String` instead?"

Never use "Great question!" or "Excellent!" — just engage with their reasoning.
