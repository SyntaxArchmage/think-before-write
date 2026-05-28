# Think Before Write

A structured coarse-to-fine workflow for research paper development with AI assistance.

Five integrated Cursor skills that take a research paper from idea to submission-ready manuscript, with mandatory human checkpoints at every layer.

## Skills

| Skill | Purpose | Key Features |
|-------|---------|-------------|
| **paper-storyline** | Coarse-to-fine alignment (L0-L5) | 6-layer hierarchy, human checkpoints, state tracking |
| **academic-writing** | Prose execution & QC | Track A/B (greenfield/brownfield), paragraph archetypes, Numbers Triangle, de-AI |
| **paper-review** | Simulated PC review | 3 reviewer personas + PE + Meta-PC, Tier A/B rubric, Issue Cards, submission gate |
| **author-supervisor** | Strategic advice | 5 independent professor lenses (Systems, Methodology, Writing, Strategy, Pragmatics) |
| **paper-writing-router** | Activation routing | Decision tree for which skill handles what |

Plus:
- **best-of-N-protocol**: Reusable pattern for launching N parallel subagents
- **Reference files**: Writing patterns, sentence banks, anti-patterns, eval methodology, reviewer archetypes, rebuttal strategies, framing strategies (sourced from top-tier systems/compiler/HPC venues)
- **Scripts**: `check-numbers.py`, `claim_audit.py`, `score_aggregate.py`, `review_preflight.sh`

## Architecture

```
paper-storyline (L0-L3)     Confirm contributions → sections → subsections → paragraphs
        │
        ▼
academic-writing (L4-L5)    Writing plan → prose execution → QC gates
        │
        ▼
paper-review                Simulated 3-reviewer PC → Issue Cards → submission gate

author-supervisor           Embedded advisory (any layer) — 5 professors in parallel
best-of-N-protocol          Reusable subagent ensemble pattern
paper-writing-router        "Which skill handles this?" decision tree
```

## Installation

Copy the skills into your project's `.cursor/skills/` directory:

```bash
# Clone
git clone https://github.com/SyntaxArchmage/think-before-write.git

# Copy all skills to your project
cp -r think-before-write/paper-storyline   your-project/.cursor/skills/
cp -r think-before-write/academic-writing  your-project/.cursor/skills/
cp -r think-before-write/paper-review      your-project/.cursor/skills/
cp -r think-before-write/author-supervisor your-project/.cursor/skills/
cp think-before-write/best-of-N-protocol.md your-project/.cursor/skills/
cp think-before-write/paper-writing-router.md your-project/.cursor/skills/
```

## Usage

1. **Start with storyline**: Activate `paper-storyline` to align your paper's structure layer by layer
2. **Write prose**: Once L3 is confirmed, `academic-writing` handles Track A (new) or Track B (existing draft)
3. **Review before submission**: `paper-review` simulates a 3-reviewer PC with quantified scoring
4. **Get strategic advice**: Invoke `author-supervisor` at any point for 5 independent professor perspectives

The `paper-writing-router` resolves ambiguous requests (e.g., "review my intro" → academic-writing QC or paper-review simulation?).

## Workflow

```
User: "Help me write this paper"
  → Router: structure question? → paper-storyline
  → Router: prose/QC? → academic-writing
  → Router: simulated review? → paper-review
  → Router: strategic advice? → author-supervisor (5 professors)
```

## Best-of-N Subagent Modes

Several workflow steps support launching N parallel subagents for diverse output:

| Mode | N | Skill |
|------|---|-------|
| Abstract writing | 5 | academic-writing |
| L5 paragraph drafting | 3 | academic-writing |
| L3 storyline proposals | 5 | paper-storyline |
| De-AI polish | 3 | academic-writing |
| Review persona scoring | 3×3 | paper-review |
| Rebuttal drafting | 5 | paper-review |
| Author supervisor | 5 | author-supervisor |

See `best-of-N-protocol.md` for the reusable pattern and session budget rules.

## Scripts

| Script | Purpose |
|--------|---------|
| `check-numbers.py` | Verify numeric claims against `manifest.yaml` |
| `claim_audit.py` | Flag overclaims, undefined terms, abstract/eval mismatches |
| `score_aggregate.py` | Aggregate reviewer scores with persona-specific offsets |
| `review_preflight.sh` | Pre-review gate (compile, pages, numbers, claims, anonymization) |

## Verified

This skill system was verified through 2 rounds of 5-agent parallel review:
- Round 1: 17 issues found and fixed
- Round 2: 10 issues found and fixed
- All fixes verified

## License

MIT
