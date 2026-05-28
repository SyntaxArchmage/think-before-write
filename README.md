# Think Before Write

A structured coarse-to-fine workflow for research paper development with AI assistance.

This Cursor skill enforces a six-layer hierarchy for research paper development — **Core Claim → Sections → Subsections → Paragraphs → Writing Plan → Implementation** — with mandatory human checkpoints at each layer. The agent never writes prose until the storyline is confirmed layer by layer, keeping contributions, methodology, and evaluation aligned throughout.

## Installation

Copy `SKILL.md` to `.cursor/skills/paper-storyline/SKILL.md` in your project:

```bash
mkdir -p .cursor/skills/paper-storyline
cp path/to/think-before-write/SKILL.md .cursor/skills/paper-storyline/SKILL.md
```

## Usage

When writing or planning paper sections, the skill activates automatically when you use planning-oriented prompts (e.g., "write paper", "plan section", "storyline").

Create a state tracking file at `plan/storyline-state.md` in your project to record confirmed layers and progress through the workflow. The skill reads and updates this file as you align each layer with the agent.

## License

MIT
