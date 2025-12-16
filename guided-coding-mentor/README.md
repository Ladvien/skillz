# Guided Coding Mentor Plugin

A Claude Code plugin that provides a senior engineering mentor for deliberate coding practice.

## What It Does

- **TODO-driven workflow**: You write every line of code yourself while Claude guides you with precise TODO comments
- **Walkthrough tracking**: Creates `slop/walkthrough/NNN.md` files to track each learning session
- **Full path references**: Always provides complete file paths when guiding edits
- **Progressive disclosure**: Adjusts scaffolding based on your skill level

## Commands

| Command | Description |
|---------|-------------|
| `/walkthrough` | Start a new guided coding session |
| `/next` | Move to the next step in current walkthrough |
| `/stuck` | Get escalating help (nudge → hint → breadcrumb → show) |
| `/quiz` | Quick pattern check on recent code |
| `/progress` | Show current walkthrough status |
| `/recap` | Generate end-of-session summary |

## Installation

### From a marketplace

```shell
/plugin marketplace add your-org/your-marketplace
/plugin install guided-coding-mentor@your-marketplace
```

### Local development

```shell
/plugin marketplace add ./path/to/marketplace
/plugin install guided-coding-mentor@marketplace-name
```

## Usage

### Start a walkthrough

```shell
/walkthrough
```

Claude will:
1. Create `slop/walkthrough/001.md` (incrementing for each session)
2. Ask what you want to build
3. Guide you with TODO comments — you write all the code
4. Always reference files by full path

### During a session

- `/next` — Ready for the next step
- `/stuck` — Need help (escalates from hints to showing the answer)
- `/quiz` — Test your understanding of patterns you've used
- `/progress` — See where you are

### End a session

```shell
/recap
```

Generates a summary of what you built, learned, and can now do.

## Plugin Structure

```
guided-coding-mentor/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── walkthrough.md
│   ├── next.md
│   ├── stuck.md
│   ├── quiz.md
│   ├── progress.md
│   └── recap.md
├── skills/
│   └── guided-coding-mentor/
│       ├── SKILL.md
│       └── references/
│           ├── teaching-patterns.md
│           ├── todo-patterns.md
│           └── anti-patterns.md
└── README.md
```

## Key Principles

1. **You write the code** — Claude guides, you type
2. **Full paths always** — No ambiguity about which file to edit
3. **Tracked progress** — Every session creates a walkthrough file
4. **One concept at a time** — No cognitive overload
5. **90-second rule** — Never struggle alone for more than 90 seconds
