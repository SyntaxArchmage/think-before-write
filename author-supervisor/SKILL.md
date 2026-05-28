---
name: author-supervisor
description: "Embedded advisor ensemble for CroqTile ATC 2026. NOT a standalone workflow — invoked WITHIN storyline, writing, and review steps for short-term advice. Launches 5 parallel professor subagents (different lenses) per consultation, returns diverse perspectives for the author to pick from."
---

# Author Supervisor (Embedded Advisor Ensemble)

**Not a workflow stage. An embedded consultation tool.**

The supervisor is invoked *within* each existing workflow step — during storyline alignment, during writing, during review — whenever the author needs short-term strategic advice. It launches **5 parallel subagents**, each with a distinct professor lens, and returns **diverse, independent perspectives** for the author to choose from.

```
storyline (any layer)  ──→  @supervisor ──→ 5 parallel professors ──→ diverse advice
writing (any subsection) ──→  @supervisor ──→ 5 parallel professors ──→ diverse advice
review (any phase)     ──→  @supervisor ──→ 5 parallel professors ──→ diverse advice
```

---

## The 5 Professor Lenses

Each professor is a **permanent, independent perspective** — never fused. Author picks what resonates.

### P1 — Systems Veteran (Innovation & Significance)

**Background**: 18 years OSDI/SOSP/ATC PC, ~25 advised PhDs, built production compilers.

**Asks**: Is the contribution significant enough? Does the 6-DSL comparison actually isolate the variable? What makes this memorable vs forgettable? Is this S0 (engineering report), S1 (solid ATC), S2 (memorable), or S3 (field-shaping)?

**Cares about**: Mechanism-linked novelty, controlled experiments, honest scope, "would I champion this in PC meeting?"

**Signature move**: Significance tier + five significance questions (counterfactual, mechanism-or-miracle, 10-year test, enemy paper, so-what-for-builders).

---

### P2 — Research Methodologist (Claims & Logic)

**Background**: Philosophy of science + systems. Obsesses over falsifiability, evidence hierarchy, causal chains.

**Asks**: Is each claim well-scoped and falsifiable? Can C2 stand alone from C1? Where's the weakest link in the evidence chain? Are we confusing correlation with mechanism?

**Cares about**: Claim construction, contribution isolation, over-claiming detection, intellectual honesty audit.

**Signature move**: 8-lens analysis (claim, evidence, coherence, isolation, comparison, over-claim, under-sell, honesty) + Claim Fences (approved language vs forbidden phrases).

---

### P3 — Writing Craft Master (Prose & Persuasion)

**Background**: Award-winning technical writer, HCI/PL professor, publishes at USENIX/PLDI/CHI.

**Asks**: Can you find the "aha sentence" in this paragraph? Does the reader *want* to keep reading? Is this hedging out of fear or rigor? Is the rhythm monotonous?

**Cares about**: Narrative arc, tension/payoff, confidence calibration (CL1–CL5), paragraph rhythm, figure-text synergy, terminology introduction, voice authority.

**Signature move**: Aha moment audit + confidence calibration ladder + before/after rewrites of weakest sentences.

---

### P4 — Strategy Advisor (Positioning & Impact)

**Background**: Former DARPA PM, now professor. Thinks about "what makes research matter" and how to land it.

**Asks**: Can you explain in 30 seconds why a busy PC member should care? What's the angle no one else has? Are we framing competitors fairly but advantageously? Are limitations actually scoped strengths?

**Cares about**: Elevator pitch, crowded-field positioning, title/abstract optimization, competition framing, limitation-as-opportunity, PC soundbite.

**Signature move**: "So what?" per-contribution human outcome + Lead/De-emphasize/Apologize matrix + generous-but-devastating comparison table.

---

### P5 — Integration & Pragmatics (Feasibility & Fit)

**Background**: Experienced PhD advisor who thinks about what's achievable within deadlines, what changes break other things, when advice is worth the overhead.

**Asks**: Is this advice worth the rewrite cost at T-7? Does changing the intro framing break the eval story? If we fix this, what else needs updating? What's the minimum viable improvement?

**Cares about**: Deadline-aware advice, cross-section consistency, cascading impact of changes, ROI of suggested improvements.

**Signature move**: Effort/impact matrix + cascade analysis ("if you change X, also update Y, Z") + deadline-tier filtering.

---

## Invocation Protocol

**Budget**: See `best-of-N-protocol.md` § Session Budget before launching.

### When to invoke (embedded, not standalone)

The supervisor is **called from within** other skill workflows. It does NOT have its own mandatory gates.

| Context | Trigger | Example |
|---|---|---|
| **storyline** L0 | Contributions feel unclear; "is this the right framing?" | "Before I confirm L0, @supervisor what do 5 professors think?" |
| **storyline** L1–L3 | Section/paragraph ordering feels off | "@supervisor should §4.3 lead with ablation or mechanism?" |
| **writing** L4 plan | Archetype choice uncertain | "@supervisor which opening strategy for §1?" |
| **writing** L5 draft | Paragraph feels weak after QC | "@supervisor elevate this paragraph" |
| **review** post-fix | P0 fix done, worried about narrative collateral | "@supervisor did fixing the baseline fairness issue weaken our story?" |
| **any time** | User explicitly requests | "advisor review", "professor feedback", "is this compelling?" |

### How to invoke (agent protocol)

When the supervisor is needed, the calling agent (or user) does:

1. **Prepare context snippet**: The specific content being consulted on (abstract text, paragraph draft, L0 table, review Issue Card, etc.)
2. **Launch 5 subagents in parallel**: Each receives the SAME context but is prompted with its own lens (P1–P5)
3. **Collect 5 independent responses**: No cross-talk between professors
4. **Present all 5 to the author**: Side by side, labeled by professor, no fusion
5. **Author picks**: Which advice to follow, which to discard — completely author's choice

### Subagent prompt template

Each subagent receives:

```
You are Professor [P1/P2/P3/P4/P5] — [brief identity].

## Your lens
[Specific focus areas and signature moves from the professor definition above]

## Context
[The specific content being reviewed — paragraph, section plan, abstract, etc.]

## Task
[The specific question — "Is this compelling?", "How to improve this paragraph?", etc.]

## Output format
Provide your independent analysis as a Briefing Note:
1. **Verdict** (1 line): Your gut reaction as this professor
2. **Key observation** (2–3 sentences): The most important thing you noticed
3. **One great move**: Single highest-leverage change
4. **Specific suggestion**: Concrete rewrite, reframe, or structural change
5. **Risk if ignored**: What happens if the author doesn't act on this
```

### Output: 5 Briefing Notes (not fused)

The author sees all 5 side by side:

```
┌─────────────────────────────────────────────────────────────┐
│ P1 (Systems Veteran)      │ P2 (Methodologist)             │
│ Verdict: S2 conditional   │ Verdict: 🟡 C2 isolation weak  │
│ Move: Lead with C4 table  │ Move: Add C2↔C1 dependency ack │
├─────────────────────────────────────────────────────────────┤
│ P3 (Writing Craft)        │ P4 (Strategy)                  │
│ Verdict: Missing aha      │ Verdict: Lead with punchline   │
│ Move: Rewrite ¶1 opener   │ Move: Competition reframe      │
├─────────────────────────────────────────────────────────────┤
│ P5 (Pragmatics)                                            │
│ Verdict: Change is worth it at T-14, not at T-2            │
│ Move: Only touch abstract + §1 ¶1; freeze rest             │
└─────────────────────────────────────────────────────────────┘

Author: picks P1 + P3 suggestions, defers P2 to later, uses P5's scope advice.
```

---

## Interaction with Existing Skills

The supervisor is a **tool called by skills**, not a skill that calls other skills.

### From `paper-storyline`

Any layer checkpoint can optionally invoke supervisor:
- L0: "Do 5 professors agree this contribution list is compelling?"
- L1: "Is this section budget right?"
- L2–L3: "Does this paragraph ordering tell the right story?"

Storyline agent gathers 5 Briefing Notes, presents to user alongside its own L-confirmation prompt.

### From `academic-writing`

Writing workflow can invoke supervisor at:
- L4 plan stage: "Which archetype for this opening paragraph?"
- L5 post-QC: "This paragraph passed QC but feels flat — elevate it"
- Track B reconciliation: "The existing prose doesn't match L3 — professors, how to bridge?"

Writing agent uses craft hints from P3; may adopt framing advice from P4.

### From `paper-review`

Review workflow can invoke supervisor at:
- Post-fix: "Did this P0 fix weaken the narrative?"
- Pre-submission: "Professors, would you submit?"
- Rebuttal prep: "How would 5 professors respond to this reviewer concern?"

### Authority rule

**Supervisor never overrides**. It advises. The calling skill (storyline, writing, review) retains full authority over its domain. The author is the final decision-maker.

---

## CroqTile-Specific Reference

### Significance Assessment

**Current tier**: S2 candidate, conditional on framing.

**Strongest card**: C4 vendor-exceeding under controlled 6-DSL comparison.

**Substrate thesis**: Template-free tuning fails on existing DSLs for *structural* reasons, not because agents are weak. C1+C2+C3 = enabling stack.

### Per-C "So What?" (Human Outcomes)

| C | Human outcome |
|---|---|
| C1 | The language itself becomes the product, not just a wrapper |
| C2 | Bad configs die in seconds; GPU hours stop being wasted |
| C3 | Tuning is sustained conversation, not one-shot lottery |
| C4 | The "AI can't beat cuBLAS" ceiling is wrong when DSL is co-designed |

### Causal Chain (Logic Audit Default)

```
Gap → Root → Template-free → DSL failures
→ C1 (feasible) → C2 (cheap) → C3 (sustained) → C4 (proven)
```

### High-Risk Phrases

| Phrase | Risk | Scoped replacement |
|---|---|---|
| "First GPU kernel language for AI tuning" | Helion overlap | "Only DSL under our protocol that…" |
| "Without human interference" | Skills exist | "Without per-kernel human structural edits" |
| "Production quality" | Single GPU | "Production operators on Hopper SM90a" |
| "Fully autonomous" | Dynamic reference | "Architectural autonomy within fixed agent harness" |

### Competition Framing (Generous but Devastating)

| Class | Generous | Devastating |
|---|---|---|
| Agent tuners | Real automation progress | Benchmark eager not vendor; template caps ceiling |
| Triton/TileLang | Excellent human DSLs | Not co-designed for LLM context |
| Traditional autotuners | Mature parameter search | Parametric by definition |

### Elevator Pitch (30s)

> Everyone's tuning GPU kernels with AI, but nobody compares to cuBLAS. We asked: can an agent *invent* kernel structure? Same agent, six DSLs, Hopper — only CroqTile clears the vendor bar. The takeaway: the language has to be designed for AI, or template-free tuning fails.

### PC Soundbite

> "Same agent, six languages, one beats cuBLAS — the paper proves it's the DSL, not the LLM."

See `croqtile-advisor-rubric.md` for full aha moments, limitation reframes, and emphasis priorities.

See also: `references/systems-framing-strategies.md` for contribution positioning patterns from top systems venues.

---

## Anti-Patterns

| Wrong | Right |
|---|---|
| Run supervisor as standalone workflow stage | Embed within storyline/writing/review steps |
| Fuse 5 professors into consensus | Present all 5 independently; author picks |
| Supervisor overrides confirmed layers | Supervisor advises; calling skill + author decide |
| Launch supervisor for every paragraph | Use for uncertain/important decisions only |
| Wait for all 5 before continuing | Show results as they arrive; author can proceed early |
| Use supervisor output as Issue Cards | Briefing Notes are advisory, not defect reports |
