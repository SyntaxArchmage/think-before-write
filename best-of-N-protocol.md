# Best-of-N Subagent Protocol

Referenced by `academic-writing`, `paper-review`, and `paper-storyline`.

## What Best-of-N Means

Launch **N parallel subagents** on the **same task** with shared constraints but independent creative latitude. Each variant produces a full output. The **author** selects the best variant, fuses elements across variants, or requests regeneration with a hint.

Not sequential retry or internal sampling — variants are independent and side-by-side.

## When to Use vs Not Use

| Use best-of-N | Do not use |
|---|---|
| Creative writing: paragraphs, abstracts, de-AI rewrites | Mechanical checks: number audit, compile, FR gates |
| Storyline proposals (L3 paragraph plans, contribution framing) | Binary pass/fail decisions with one correct answer |
| Rebuttal drafts, reconciliation strategies | Tasks shorter than one paragraph |
| Evaluation where single-LLM bias is a risk (review scoring) | Deterministic lint or anchor scoring on existing text |

Multiple valid answers + author taste → best-of-N. Script-verifiable answer → single pass.

## Standard N Values

| Task | N | Rationale |
|------|---|-----------|
| Paragraphs, reconciliation strategies, de-AI rewrites | **3** | Fast, focused; enough diversity without fatigue |
| Abstracts, L3 storylines, rebuttal drafts | **5** | High-leverage; worth 5× cost |
| Review scoring (per persona) | **3 per persona** | 3 personas × 3 = **9** total score variants; reduces scorer drift |

Override N only with user consent (e.g., deadline crunch → N=2).

## Subagent Prompt Template

Calling skill fills bracketed sections. Launch all N variants in **parallel**.

```
You are Variant [K/N] for [TASK_NAME].

## Constraints (MUST follow)
[Shared constraints from the calling skill — L3 alignment, paragraph contract, number provenance, etc.]

## Your creative latitude
[What you CAN vary: opening strategy, archetype emphasis, sentence structure, voice register, evidence ordering]

## Context
[Provided by calling skill]

## Task
[Specific instruction]

## Output format
[Defined by calling skill]
```

Assign each K a distinct creative mandate (contrast-first, mechanism-first, number-led, etc.) so outputs diverge meaningfully.

## Selection Protocol

1. **Present** all valid variants side-by-side (label V1…VN; include QC status per variant).
2. **Author selects** one of:
   - `Use variant K`
   - `Fuse: take ¶1 from K, ¶2 from J, …`
   - `None — regenerate with hint: …`
3. **Default if no response within ~30s**:
   - **Review scoring**: agent picks highest-scoring variant (median of dimension scores if tie).
   - **Writing / storyline**: agent picks **V1** (first variant).
4. **Record** selection in the relevant state file (`storyline-state.md`, `review-state.md`, or inline in session).

Do not merge variants without author confirmation except the 30s default.

## Quality Control

Every variant must **individually pass** the calling skill's QC criteria before presentation:

- `academic-writing`: paragraph contract, number provenance, anchor score, de-AI lint (as applicable)
- `paper-storyline`: L-layer alignment, C→M→E mapping, contribution isolation
- `paper-review`: rubric completeness, persona bias applied, Tier A dimensions filled

**Failed variant**: discard; do not show to author. Note count: *"N−M valid variants (M failed QC: [reason])."*

Zero valid variants → fix constraints or regenerate all N with shared hint.

## Cost Awareness

Each best-of-N invocation costs **~N× tokens** (N parallel completions + orchestration + side-by-side presentation).

**Before launch**, state tier to user:

> Launching [N] variants (~[N]× cost). Proceed?

Require consent unless pre-approved (e.g., user said "best-of-5 abstract"). On decline → N=1 with stated tradeoff.

## Session Budget

To prevent subagent explosion:
- Max **1 best-of-N invocation** per user turn (unless user explicitly requests more)
- Max **1 author-supervisor consultation** (5 subagents) per turn
- Never combine: supervisor (5) + best-of-N (3-5) on the same artifact in one turn
- Full review best-of-N scoring (9 subagents): requires explicit user phrase "full review with best-of-N scoring"
- Default review Phase 2: single-agent sequential personas (no best-of-N unless opted in)
- Theoretical max per turn: 5 (supervisor) OR 5 (best-of-N) OR 9 (review scoring) — never stacked

## Integration Syntax

Other skills reference this file inline:

```
See `best-of-N-protocol.md` for subagent launch pattern. Use N=[value], task=[name].
```

**Examples**:

- `academic-writing`: `N=3, task=§3.2-¶4 prose` — fill Constraints from L3 + paragraph contract; Output = LaTeX paragraph + QC checklist.
- `paper-storyline`: `N=5, task=L3 §2.1 paragraph storyline` — fill Constraints from Layer 2; Output = paragraph table per L3 checkpoint format.
- `paper-review`: `N=3 per persona, task=R1 Tier A scoring` — fill Context with section under review; Output = five dimension scores + one-sentence justification each.

Calling skill owns constraints, output format, and QC gates. This protocol owns launch, presentation, selection, and cost consent.
