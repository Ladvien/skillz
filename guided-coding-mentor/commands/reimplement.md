---
description: Follow a reconstruct walkthrough series and reimplement the project yourself with TODO-driven guidance
---

# Reimplement Command

Use the walkthrough documents produced by `/reconstruct-project` or `/reconstruct-feature` to guide hands-on reimplementation. You write every line of code. Claude navigates using the reconstruct docs as the blueprint.

## Requirements

- Reconstruct walkthrough docs exist in `slop/<project-name>/`
- Git repository with working remote
- Empty or clean working directory to build into (or Claude sets one up)

## Phase 1: Setup

1. Find available reconstruct walkthroughs:
   ```bash
   ls slop/*/README*.md 2>/dev/null
   ```
   If multiple projects exist, ask user which one.

2. Read the README index to understand the full series.

3. Read SCRATCHPAD.md to check for any prior reimplement progress.

4. Determine starting point:
   - Fresh start: Part 01
   - Resuming: find last completed part in SCRATCHPAD.md

5. Set up the implementation workspace:
   ```bash
   git add -A
   git commit -m "checkpoint: pre-reimplement state" --allow-empty
   git push
   ```
   Store checkpoint hash.

6. If reimplementing an open source project, user should be working in a separate empty project directory. Verify:
   ```bash
   # Project should have minimal or no source files yet
   # Config files (Cargo.toml, package.json, etc.) may exist if user initialized
   ```
   If the user hasn't set up the project skeleton, guide them through it before starting Part 01.

## Phase 2: Work Through Each Part

For each walkthrough part:

1. **Read the walkthrough doc** for the current part
2. **Present the goal:**
   ```
   **Part NN: [Title]**

   [What we're building from the walkthrough's "What We're Building" section]

   After this part: [from "What You'll Have After This"]

   Ready? Let's go step by step.
   ```

3. **Show the code with strategic placeholders.**

   Show the actual code the user will type, but replace 1-3 key expressions or blocks with `________` placeholders. The placeholders should target the *interesting* parts — the logic that matters, not boilerplate.

   Keep explanations minimal. A single "What's happening" line if needed. The code IS the lesson.

   Example — walkthrough doc shows:
   ```rust
   // src/config.rs
   pub struct Config {
       pub host: String,
       pub port: u16,
   }

   impl Config {
       pub fn from_env() -> Result<Self, ConfigError> {
           let host = std::env::var("HOST").unwrap_or_else(|_| "localhost".to_string());
           let port = std::env::var("PORT")
               .unwrap_or_else(|_| "8080".to_string())
               .parse()
               .map_err(ConfigError::InvalidPort)?;
           Ok(Config { host, port })
       }
   }
   ```

   Claude presents:
   ```
   **File:** `src/config.rs` — New file

   ```rust
   pub struct Config {
       pub host: String,
       pub port: u16,
   }

   impl Config {
       pub fn from_env() -> Result<Self, ConfigError> {
           let host = std::env::var("HOST").unwrap_or_else(|_| "localhost".to_string());
           let port = std::env::var("PORT")
               .unwrap_or_else(|_| "8080".to_string())
               .__________
               .__________;
           Ok(Config { host, port })
       }
   }
   ```

   The placeholders here target the parse + error mapping chain — that's the interesting bit.
   ```

   **Placeholder guidelines:**
   - 1-3 placeholders per step. Never more.
   - Target the concept being taught, not trivial syntax.
   - The surrounding code gives enough context to figure out the placeholder.
   - If a step is pure boilerplate (config files, imports), show it complete — no placeholders.

4. **Wait for user to write code.** Do not proceed until they respond.

5. **Verify their implementation** against the walkthrough doc:
   - Does it compile? `cargo check` / equivalent
   - Does it match the intent of the walkthrough? (exact code match not required — correct behavior is what matters)
   - If their approach differs but works, acknowledge it briefly and keep moving.

6. **If they're stuck**, reveal the placeholder answer directly. Don't do a long escalation ladder — keep momentum. Brief explanation of why, then move on.

7. **After completing all steps in a part**, run the verify command from the walkthrough doc:
   ```
   **Part NN complete.** Let's verify:

   ```bash
   [verify command from walkthrough]
   ```

   **Expected:** [expected output from walkthrough]
   ```

8. **Commit the completed part:**
   ```bash
   git add -A
   git commit -m "reimplement: part NN - [title]"
   git push
   ```

## Phase 3: Track Progress

Update SCRATCHPAD.md after each completed part. Add or update a Reimplement section:

```markdown
## Reimplement Progress

**Started:** [YYYY-MM-DD]
**Current Part:** [NN]

| Part | Title | Status | Date |
|------|-------|--------|------|
| 01   | ...   | [x]    | ...  |
| 02   | ...   | [ ]    | ...  |
```

Commit after updating:
```bash
git add SCRATCHPAD.md
git commit -m "reimplement: completed part NN"
```

## Phase 4: Between Parts

After each part, before starting the next:

1. **One retention question.** Ask a single multiple choice question about something from the part they just completed. Keep it concrete and code-oriented, not abstract theory.

   Good question:
   ```
   In the config parser, why did we use `.map_err(ConfigError::InvalidPort)?` instead of `.unwrap()`?

   A) .unwrap() is slower at runtime
   B) .unwrap() would panic on bad input instead of returning a recoverable error
   C) .map_err() is required by the Result type
   D) .unwrap() doesn't work with .parse()
   ```

   Bad question:
   ```
   What is the Result type in Rust?  // Too abstract, not tied to what they just built
   ```

   **Rules:**
   - Exactly one question per part. No more.
   - 4 answer choices.
   - Tied to a specific decision or pattern from the code they just wrote.
   - If they get it wrong, give the answer in one sentence and move on. Don't lecture.
   - If they get it right, acknowledge briefly and move on.

2. **Prompt to continue:**
   ```
   Ready for Part [NN+1]? Say /next or take a break.
   ```

If the user says `/next`, read the next walkthrough doc and continue from Phase 2.

## Phase 5: Completion

After the final part:

```
**Rebuild complete.** You've reimplemented [Project Name] from scratch.

**Full series:** [N] parts, [M] files, [summary of what they built]

**What's next:**
- Run /journal to capture the full experience
- Run /recap for the session summary
- Try rebuilding again in a week without the walkthrough docs (muscle memory challenge)
- Study a specific feature deeper with /reconstruct-feature
```

Update SCRATCHPAD.md status to Complete.

## Handling Stubs

The walkthrough docs track stubs (introduced in one part, resolved in another). When presenting a step that introduces a stub:

```
**Note:** We're stubbing `function_name()` here — it just needs to compile.
We'll implement it for real in Part [XX].

```rust
// TODO: Stub — return a placeholder value for now
//       Real implementation comes in Part [XX]
```
```

When reaching the part that resolves a stub:

```
**Remember that stub?** `function_name()` from Part [YY] — time to make it real.
```

## Context Management

After every 2-3 parts, or when context is getting long:

```
**Context Check:** We've completed [N] parts. Progress is saved in SCRATCHPAD.md.

If we need a fresh conversation, run /reimplement and I'll pick up where we left off.

Continue, or take a break?
```

## Resuming

If invoked and SCRATCHPAD.md shows prior reimplement progress:

1. Read SCRATCHPAD.md to find current part
2. Read the current walkthrough doc
3. Check if the part is partially complete (look at committed files vs walkthrough steps)
4. Resume from where the user left off

```
**Resuming reimplementation of [Project Name].**

You completed through Part [NN]. Picking up at Part [NN+1]: [Title].

[Continue with Phase 2]
```
