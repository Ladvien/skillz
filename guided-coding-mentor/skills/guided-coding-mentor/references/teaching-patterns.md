# Teaching Patterns Reference

## Building Muscle Memory

Move skills from conscious thought to automatic execution through repetition with variation:

1. **First exposure**: Show pattern with heavy guidance
2. **Second exposure**: Show shape, they fill details
3. **Third exposure**: They write from memory
4. **Fourth+**: They apply in new contexts

### Example Progression

```
[First]: "Copy this error enum structure"
[Second]: "Add a new variant for network errors"
[Third]: "Create an error enum for the config module"
[Fourth]: "Design error handling for the entire auth system"
```

## The 15-Minute Rule

Switch roles regularly to maintain engagement and prevent domination.

Every 15 minutes or 3 steps, whichever comes first:
```
**Role Switch:** You've been coding for 15 minutes.
Quick break? Or shall we swap - you review, I guide differently?
```

## Knowledge Verification

### Pattern Quizzes (Every 2-3 steps)

Test understanding, not memorization:
```
**Pattern Check:** You've used `Box<dyn Error>` three times now.
What problem does Boxing solve here that `impl Error` wouldn't?
[Wait for reasoning, not just correct answer]
```

### Code Prediction

Before writing, predict behavior:
```
**Before you run this:** What error will the compiler show?
[Their prediction]
Now run it. Were you right? What's your mental model missing?
```

## Context Management

### Proactive Journal Prompts

When context is getting full, prompt before it's too late:

```
**Context Check:** We've covered a lot of ground. Let's capture this before continuing.

Run /journal to document:
- The bugs we've solved
- The patterns we've used
- Where we are in the walkthrough

Ready when you are.
```

### After Solving Tricky Bugs

```
**That was a good debugging session.** Worth capturing.

Run /journal to document:
- What the symptom was
- What you thought it was
- What it actually was
- How we fixed it

This becomes valuable reference material.
```

## Example Session Flow

### Step 1: Error Foundation

**Pattern Recognition:**
```rust
enum ConfigError {
    Missing(String),
    Invalid { field: String, value: String },
}
```

**Let's build this:**
Adding TODOs to `src/error.rs`:

```rust
// src/error.rs
use std::fmt;

#[derive(Debug)]
pub enum AppError {
    // TODO: Add IoError variant that wraps std::io::Error
    // TODO: Add ParseError variant with a String message
    // TODO: Add ConfigError variant for configuration issues
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            // TODO: Match each variant and write appropriate error messages
        }
    }
}
```

**Verify:**
`cargo check` - should see "non-exhaustive patterns" until you add all variants

[User fills in TODOs and responds]

✓ Compiled! Notice you used tuple variants for wrapping errors? That's the newtype pattern in action.

**Quick Check:** Why wrap `std::io::Error` instead of just storing a String?

[User explains]

Exactly. Preserving the original error = better debugging. Now let's implement From traits...

### Step 2: Error Conversions

**Next up:**
Adding conversion TODOs to `src/error.rs` (append to file):

```rust
impl From<std::io::Error> for AppError {
    fn from(error: std::io::Error) -> Self {
        // TODO: Convert io::Error to your AppError::IoError variant
    }
}

impl From<String> for AppError {
    fn from(msg: String) -> Self {
        // TODO: Convert String to AppError::ParseError variant
    }
}
```

This enables the ? operator to auto-convert errors. Fill those in and let's test it.

## Refactoring Guidance

When their code works but isn't idiomatic (always use full paths):

```
Your code works, but let's make it idiomatic. I'm adding improvement TODOs to src/processor.rs:

```rust
fn process_items(items: Vec<Item>) -> Vec<String> {
    let mut results = Vec::new();
    for item in items {
        if item.is_valid() {
            // TODO: Replace this imperative loop with .filter_map()
            results.push(item.name);
        }
    }
    results
}
```
```

## Documenting Learning

### Walkthrough Updates

After each step, update the walkthrough file:
- Mark step complete `[x]`
- Add timestamp to Session Log
- Note any dragons encountered

### Journal-Worthy Moments

Prompt for /journal when:
- A bug took more than 2 attempts to fix
- User had an "aha" moment about a pattern
- You're about to move to a significantly different topic
- Context is getting full
- Session is ending

### End of Session

Always end with consolidation:

```
**What You Built:** [feature]
**What You Learned:** [pattern/concept]
**What You Can Now Do:** [new capability]

**Document this session?** Run /journal to capture what we learned.

**Muscle Memory Challenge:**
Rebuild this tomorrow without looking at today's code.
```
