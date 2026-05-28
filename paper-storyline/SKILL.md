---
name: paper-storyline
description: "Use when planning paper structure, aligning storyline, designing section/subsection layout, discussing what each paragraph should say, or when user says 'plan', 'storyline', 'align', 'restructure', 'what should §X say'. Coarse-to-fine workflow: contributions → sections → subsections → paragraphs → writing plan, with mandatory human checkpoints."
---

# Paper Storyline Alignment

A structured, multi-layer workflow for research paper development.
Inspired by Claude Code's `/feature-dev` (7-phase plan-before-code pattern),
adapted for academic writing where **storyline alignment with the human author
is the highest-priority task**.

## Core Philosophy

1. **Coarse-to-fine** — Never write prose before the storyline is confirmed layer by layer.
2. **Human alignment at every layer** — Each layer requires explicit user confirmation before descending.
3. **Contributions drive everything** — The contribution list is the root; methodology and evaluation are leaves that serve it.
4. **No blind trust** — Critically analyze existing content. The current paper may be partially wrong or misaligned with the author's intent.
5. **Storyline correctness > prose quality** — A well-aligned draft with rough prose is far better than polished text that says the wrong thing.

## When to Activate

Activate this skill when:
- User says "write paper", "rewrite section", "plan paper", "storyline", or similar planning intent
- User attaches `research-writing-skill` AND indicates structural/planning work (not just prose polish)
- User asks to "align", "restructure", or "figure out what to write"
- Starting any new section or major rewrite

Do NOT activate for:
- Pure prose polish ("make this paragraph sound better")
- Figure generation
- Data auditing with no structural implications
- Single-paragraph fixes where storyline is already confirmed

## The 6-Layer Hierarchy

```
Layer 0: Core Claim + Contributions ("red thread")
│
├─ Layer 1: Section outline + page budget
│   │
│   ├─ Layer 2: Subsection topics + C→M→E mapping
│   │   │
│   │   ├─ Layer 3: Paragraph-level storyline per subsection
│   │   │   │
│   │   │   ├─ Layer 4: Writing plan (topic sentence, evidence, form, length)
│   │   │   │   │
│   │   │   │   └─ Layer 5: Implementation (actual writing)
```

Each layer MUST be confirmed with the user before descending to the next.
Confirmation is tracked in `plan/storyline-state.md`.

---

## Layer 0: Core Claim + Contributions

**Goal**: Agree on what the paper claims and what its contributions are.

**Protocol**:
1. Read the current abstract and contributions list.
2. Read `PAPER-PLAN.md` (if it exists) for the intended storyline.
3. Present to user:
   - The paper's **one-sentence core claim**
   - The **contribution list** (numbered)
   - A **C→M→E correspondence table**: which contribution maps to which methodology section and which evaluation result
4. Ask user to confirm or correct.

**Checkpoint format**:
```
Core claim: [one sentence]

| # | Contribution | Methodology | Evaluation |
|---|---|---|---|
| C1 | ... | §X.Y | §Z.W (table/figure) |
| C2 | ... | §X.Y | §Z.W |
| ...

Is this correct? [Confirm / Reframe / Add / Remove]
```

**Red flags at this layer**:
- Contributions that have no evaluation support → flag as gap
- Evaluation results that serve no contribution → flag as orphan
- Methodology sections that serve no contribution → flag as dead weight

---

## Layer 1: Section Outline + Page Budget

**Goal**: Agree on the section-level structure and how much space each gets.

**Protocol**:
1. List all sections with:
   - Title
   - Label
   - Target page count
   - One-sentence "job" of this section
2. Total must fit the venue's page limit.
3. Present to user for confirmation.

**Checkpoint format**:
```
| § | Title | Pages | Job |
|---|-------|-------|-----|
| 1 | Introduction | 1.5 | Expose 4 problems → root cause → CroqTile → results |
| 2 | Background | 1.5 | Template paradigm + 3 failure dimensions |
| ...

Total: X pages (target: Y). [Confirm / Adjust]
```

**Red flags at this layer**:
- Total exceeds page limit by >0.5 pages
- Any section with "job" that doesn't serve a contribution
- Missing sections needed for the venue (e.g., no Related Work)

---

## Layer 2: Subsection Topics + C→M→E Mapping

**Goal**: For each section, define its subsections and what each subsection's "job" is.

**Protocol**:
1. For each section, list subsections:
   - Title
   - ~Paragraphs (target)
   - "Job" — what question does this subsection answer?
   - Which contribution it serves
2. Verify that methodology subsections have corresponding evaluation support.
3. Present to user for confirmation.

**Checkpoint format** (per section):
```
§3 Methodology:
  §3.1 Language Design (~8 paragraphs)
    Job: Present 5 language features, each with tuning impact
    Serves: C1
  §3.2 Compiler-Harness Co-design (~6 paragraphs)
    Job: Show how compiler enables fast iteration
    Serves: C2
  ...

[Confirm / Adjust subsection X / Add / Remove]
```

**Red flags at this layer**:
- Subsection with no clear "job"
- Two subsections that overlap in scope
- A contribution with no subsection serving it

---

## Layer 3: Paragraph-Level Storyline

**Goal**: For each subsection, define what each paragraph says (topic sentence level).

**Protocol**:
1. Work one section at a time (user chooses which section to align next).
2. For each subsection, list paragraphs:
   - Topic sentence (the claim/point of the paragraph)
   - Key evidence (what data/citation backs it)
   - Transition (how it connects to the next paragraph)
3. Present to user for confirmation.
4. Mark confirmed in state file.

**Checkpoint format** (per subsection):
```
§3.2 Compiler-Harness Co-design:
  ¶1: "The compiler is co-designed with the harness, not standalone."
      Evidence: contrast with traditional compilers
      → leads to: two capabilities
  ¶2: "First capability: 353 static checks catch errors before GPU runs."
      Evidence: Table (check taxonomy), 3-8s vs 30-90s
      → leads to: what gets checked statically vs at runtime
  ¶3: "Some checks require runtime insertion when expressions are non-constant."
      Evidence: memcheck infrastructure detail
      → leads to: agent-facing diagnostics
  ...

[Confirm / Reorder / Add paragraph / Remove paragraph]
```

**Red flags at this layer**:
- Paragraph with no evidence
- Two consecutive paragraphs making the same point
- A paragraph that doesn't advance the subsection's "job"
- Missing transition between paragraphs (logical gap)

---

## Layer 4: Writing Plan

**Owned by `academic-writing` skill.** After Layer 3 is confirmed, hand off to `academic-writing` for writing plan creation.

This skill only defines the handoff trigger: when L3 is confirmed in `plan/storyline-state.md`, the agent should activate `academic-writing` Track A or Track B as appropriate.

**Re-alignment triggers from L4 back to L3** (this skill handles):
- L4 writing plan contradicts L3 paragraph storyline → reopen L3
- New evidence found during L4 planning → escalate to L2 or L0

---

## Layer 5: Implementation

**Owned by `academic-writing` skill.** Do not write prose in this skill.

**Re-alignment triggers from L5 back to higher layers** (this skill handles):
- Written paragraph contradicts confirmed L3 → reopen L3
- Number not in manifest → flag user, do not invent
- Claim contradicts `research-methodology.mdc` → escalate to L0

---

## State Tracking

Progress is tracked in `plan/storyline-state.md` with this format:

```markdown
# Storyline State

## Layer 0: Core Claim + Contributions
Status: [confirmed | pending | needs-revision]
Confirmed: [date]
Notes: [any revision notes]

## Layer 1: Section Outline
Status: [confirmed | pending | needs-revision]
Confirmed: [date]

## Layer 2: Subsection Topics
| Section | Status | Confirmed |
|---------|--------|-----------|
| §1 Intro | confirmed | 2026-05-27 |
| §2 Background | pending | — |
| ...

## Layer 3: Paragraph Storyline
| Subsection | Status | Confirmed |
|------------|--------|-----------|
| §3.1 Language Design | confirmed | 2026-05-27 |
| §3.2 Compiler | pending | — |
| ...

## Layer 4: Writing Plan
| Subsection | Status | Confirmed |
|------------|--------|-----------|
| §3.1 Language Design | confirmed | 2026-05-27 |
| ...

## Layer 5: Implementation
| Subsection | Status | Notes |
|------------|--------|-------|
| §3.1 Language Design | done | compiled OK |
| ...
```

---

## Workflow Rules

### Rule 1: Never Skip Layers

Even if the user says "just write §3.2", check the state file:
- Is Layer 0 confirmed? If not, start there.
- Is Layer 1 confirmed? If not, do that first.
- Is §3.2 confirmed at Layer 2? If not, align that first.
- Is §3.2 confirmed at Layer 3? If not, align paragraph storyline first.
- Only then proceed to writing.

Exception: If user explicitly says "skip alignment, just write" — comply but:
- Layer 0 (contributions) can NEVER be skipped. It is the root invariant.
- Layers 1-4 can be skipped if user insists; note in state file as "written without alignment".
- For partial rewrites (only one section), only that section's Layer 2-4 need re-confirmation; Layer 0 and 1 stay confirmed unless user revises them.

### Rule 2: Re-alignment Triggers

Go UP layers when:
- New data contradicts a confirmed storyline point
- User changes their mind about a contribution
- A section is growing beyond its page budget
- Evaluation results don't support a methodology claim

### Rule 3: Batch Alignment for Efficiency

When aligning Layer 3 (paragraph storyline), do all paragraphs of one subsection in a single checkpoint. Don't ask one paragraph at a time — that's too slow.

### Rule 4: The C→M→E Invariant

At all times, maintain this invariant:
> Every contribution C_i has at least one methodology subsection that presents it
> AND at least one evaluation result that validates it.

If this invariant breaks, flag immediately.

### Rule 5: Page Budget Tracking

After any significant writing, re-estimate page counts. If a section exceeds its budget by >0.3 pages, flag to user before continuing.

---

## Best-of-N Subagent Mode

**Budget**: See `best-of-N-protocol.md` § Session Budget before launching.

See `best-of-N-protocol.md` for subagent launch pattern, selection protocol, and QC gates.

### L3 Storyline Proposals (N=5)

- **When**: Layer 3 — paragraph-level storyline for any section with ≥5 paragraphs
- **Why**: Paragraph ordering has multiple valid strategies (chronological, most-important-first, problem-solution, general-to-specific). 5 proposals maximize narrative diversity.
- **Constraints shared**: L2 subsection topic + job, C→M→E for this subsection, confirmed L1 page budget, design philosophy (可能→快→持续→实证)
- **Creative latitude**: Paragraph ordering, tension arc, where to place the "aha moment", how to open the section (result-first vs setup-first vs contrast-first), bridge paragraph placement
- **Each variant must**: Cover all L2 jobs; respect paragraph count target; each paragraph has a clear single job; paragraphs connect to contributions
- **Selection**: Author picks the narrative arc that best serves their story. May hybridize: "Take V2's opening but V4's closing."

### Cost Awareness

L3 best-of-5 costs ~5× tokens vs single proposal. Confirm before launch unless user already asked for storyline proposals at L3. See `best-of-N-protocol.md` § Cost Awareness.

---

## Integration with Other Skills

| Skill | Relationship |
|-------|------|
| `author-supervisor` | Embedded advisor ensemble — invoke at any layer checkpoint for 5 parallel professor perspectives (P1 systems, P2 methodology, P3 writing, P4 strategy, P5 pragmatics). Advisory only; does not override layer confirmations. |
| `academic-writing` | Owns Layer 4–5 execution, QC, and prose quality. Activate after L3 confirmed in `plan/storyline-state.md`. |
| `paper-review` | Downstream reviewer simulation and submission gate. Activate after subsections reach `qc-pass`. |
| `research-writing-skill` | Generic prose guidance; CroqTile L4–5 defers to `academic-writing`. |
| `ralph-loop-request` / `durable-request` | Handles turn-ending checkpoints. This skill's layer checkpoints are ADDITIONAL to those. |
| `paper-writing.mdc` (rule) | Provides LaTeX conventions. Always applies during Layer 5. |
| `de-ai-style.mdc` (rule) | Provides style rules. Always applies during Layer 5 (via `academic-writing` QC Round 3). |

**Priority**: This skill's structural alignment takes precedence over writing. If storyline is unconfirmed, do NOT write — align first. After L3 confirmation, hand off Layers 4–5 to `academic-writing`. At any layer, optionally invoke `author-supervisor` for 5 professor perspectives before confirming.

---

## Language and Communication

- Layer checkpoints (proposals, questions, options) should be presented in the **user's preferred language** (follow conversation language).
- Paper content (LaTeX prose) is always in **English** (unless the venue requires otherwise).
- State file entries are in English for consistency.

---

## Quick Reference: What To Do At Each Layer

| Layer | AI Action | User Action | Output |
|-------|-----------|-------------|--------|
| 0 | Analyze paper, propose claim + contributions | Confirm/Correct | Confirmed C→M→E table |
| 1 | Propose section outline + pages | Confirm/Adjust | Confirmed outline |
| 2 | Propose subsection breakdown | Confirm/Adjust | Confirmed subsection map |
| 3 | Propose paragraph storyline | Confirm/Reorder | Confirmed paragraph flow |
| 4 | Hand off to `academic-writing` Track A/B | Approve | Blueprint for writing |
| 5 | (Owned by `academic-writing` — not this skill) | Review/Iterate | Final prose |

---

## Anti-Patterns (Red Flags for AI)

| AI Thought | Correct Action |
|------------|----------------|
| "I know what this section should say" | Propose to user, don't assume. |
| "The current paper is fine, just polish it" | Critically evaluate against Layer 0 contributions. |
| "User said rewrite, so I'll just rewrite" | Check which layers are confirmed first. |
| "This is obvious, no need to check" | If it's not in the state file as confirmed, check. |
| "I'll just follow PAPER-PLAN.md" | PAPER-PLAN.md is a guide, not gospel. User may have evolved. |
| "Let me write all sections at once" | One subsection at a time. Confirm before moving on. |
| "The data supports this claim" | Verify against raw data, don't trust processed summaries. |
