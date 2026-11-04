# skillz

A personal collection of Claude skills, packaged as a Claude Code plugin
marketplace and used as a [skillshare](https://skillshare.runkids.cc) source
across my machines.

## Install as a Claude Code plugin marketplace

```text
/plugin marketplace add Ladvien/skillz
/plugin install guided-coding-mentor@ladvien-marketplace
```

The marketplace is declared in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).

| Plugin | Version | What it does |
|---|---|---|
| `guided-coding-mentor` | 2.0.0 | Senior engineering mentor for deliberate coding practice: you write and verify every line, gated on explaining it before you advance. |
| `academic-research-hs` | 0.3.0 | Multi-agent academic research pipeline hard-wired to home-still: deep-research + academic-paper + academic-paper-reviewer + academic-pipeline orchestrator + home-still-bridge routing skill. |
| `research-to-flashcards` | 0.1.0 | Turn research into spaced-repetition flashcards in Mochi: retrieve via home-still, distill into atomic tenets, approve, push to the Mochi API. |
| `procedural-animation-assets` | 0.1.0 | Make a Blender-modeled asset procedurally animatable in-engine: choose the technique, author via BlenderMCP, export glTF, drive it in-engine. |
| `research-synthesis` | 0.1.0 | Turn a topic into a cited, audited literature survey over a home-still corpus: frozen protocol, snowballing search, screening with kappa, GRADE certainty, PRISMA report, blocking citation audit. |

## Use as a skillshare source

The repo is also a skillshare source, so the same skills sync to every machine's
agent targets (`~/.claude/skills`, `~/.config/opencode/skills`, …):

```sh
skillshare init --remote git@github.com:Ladvien/skillz.git   # once
skillshare pull                                              # elsewhere
```

`skillshare` discovers all 9 skills at any depth. Because the skills are nested
inside plugin folders, point the target at standard naming to get clean link
names:

```sh
skillshare target claude --target-naming standard
skillshare sync
```

### Layout

```
.claude-plugin/marketplace.json   the marketplace
academic-research-hs/
  .claude-plugin/plugin.json      plugin manifest
  shared/                         cross-skill references shared by the skills below
  skills/<skill>/SKILL.md         one skill each (+ agents/, references/, templates/, scripts/)
guided-coding-mentor/            same shape: .claude-plugin/, skills/, commands/
procedural-animation-assets/
research-synthesis/               + agents/, commands/
research-to-flashcards/
```

Every skill lives at `<plugin>/skills/<skill>/SKILL.md` and every skill's
`name` matches its directory. `academic-research-hs/shared/` is referenced by
several skills as `shared/<file>.md` (plugin-root relative); links written
relative to a file (`../../shared/...`, `../../../shared/...`) depend on depth.

## License

See [LICENSE](LICENSE).
