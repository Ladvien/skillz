# TODO Patterns Reference

## Critical: Always Use Full Paths

Every TODO instruction MUST include the complete file path from project root.

### Correct Format

```
Adding TODOs to src/parser.rs:

```rust
fn parse_config(input: &str) -> Result<Config, Error> {
    // TODO: Check if input is empty, return Error::EmptyInput if so
}
```
```

### Incorrect Format

```
Adding TODOs to parser.rs:  // ❌ Missing full path!
```

## Progressive TODO Scaffolding

Adjust scaffolding level based on user's experience:

### Heavy Scaffolding (Beginners)

In `src/config.rs`:
```rust
fn parse_config(input: &str) -> Result<Config, Error> {
    // TODO: Check if input is empty, return Error::EmptyInput if so
    // TODO: Split input by newlines using .lines()
    // TODO: Parse each line with parse_line()?, collecting into Vec
    // TODO: Build and return Ok(Config::new(lines))
}
```

### Light Scaffolding (Intermediate)

In `src/config.rs`:
```rust
fn parse_config(input: &str) -> Result<Config, Error> {
    // TODO: Validate input and parse lines with proper error handling
}
```

### Minimal Scaffolding (Advanced)

In `src/config.rs`:
```rust
// TODO: parse_config function that returns Result<Config, Error>
```

## Good TODO Layout Example

In `src/layout.rs`:
```rust
fn recursive_cut(
    &self,
    elements: &[BBox],
    x_min: f32,
    y_min: f32,
    x_max: f32,
    y_max: f32,
) -> Vec<usize> {
    // TODO: Base case 1 - if empty, return empty vec

    // TODO: Base case 2 - if only 1 element, return vec with that element's class_id

    // TODO: Try horizontal cut first (top-to-bottom reading)
    // if let Some(y_cut) = self.find_horizontal_cut(...) {
    //     split elements into top and bottom
    //     recursively process both halves
    //     combine results: top first, then bottom
    // }

    // TODO: Try vertical cut (left-to-right for multi-column)
    // if let Some(x_cut) = self.find_vertical_cut(...) {
    //     split elements into left and right
    //     recursively process both halves
    //     combine results: left first, then right
    // }

    // TODO: No valid cuts - sort by position
    self.sort_by_position(elements)
}
```

## Inserting TODOs

Always show the exact file state after adding TODOs with full path:

```
**Here's what to fill in** in `src/main.rs`:

```rust
fn main() {
    // TODO: Parse command line arguments using std::env::args()
    
    // TODO: Load configuration from "config.toml"
    
    // TODO: Initialize the application with config
    
    // TODO: Run the main loop with error handling
}
```
```

## Verifying TODO Completion

After user implements, check their work:

```
**Let's check your work:**
Run: `grep -rn "TODO" src/`

Still see TODOs? Let's tackle the remaining ones.
All clear? Let's test: `cargo run -- test-arg`
```

## Progressive TODO Removal Schedule

As users advance, reduce scaffolding:

| Week | Scaffolding Level |
|------|-------------------|
| 1 | Detailed TODOs with hints |
| 2 | TODOs with just function signatures |
| 3 | TODOs marking locations only |
| 4 | No TODOs - they know where code goes |

## Error-Specific TODOs

When code fails, add a TODO at the exact issue location with full path:

In `src/user.rs`:
```rust
fn get_name(user: &User) -> String {
    // TODO: The line below returns &str, but we need String
    // HINT: Consider .to_string() or .to_owned()
    user.name  // <-- Current issue here
}
```

## TODO Quality Checklist

✅ Good TODOs:
- Include full file path
- Specify the exact operation needed
- Include type information when relevant
- Mention the pattern or idiom to use
- Are self-contained (don't require scrolling to understand)

❌ Bad TODOs:
- Missing file path
- "Add code here"
- "Fix this"
- "Implement the thing we discussed"
- Reference line numbers (they change)
- Require reading other comments to understand
