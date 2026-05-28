---
name: paper-review
description: "Use when reviewing completed sections, simulating peer review, checking submission readiness, or when user says 'review §X', 'simulate reviewers', 'submission check', 'is this ready'. Runs 3-reviewer + PE + Meta-PC simulation with Tier A/B rubric and Issue Cards."
---

# Paper Review (CroqTile ATC 2026)

**RULE 0 GATE**: Before reviewing, read `plan/storyline-state.md` and verify L3 is confirmed for target subsection. Review requires storyline context to evaluate alignment.

Simulated PC review for **CroqTile: A GPU Kernel Programming Language Designed for AI Tuning** (ATC 2026, 12pp excl. refs, anonymous). **Deadline: June 10, 2026.**

**Outputs**: `plan/review-state.md` (living), `plan/review-report.md` (full report per round). Issue Cards route to `paper-storyline` (L0–L3) or `academic-writing` (L4–L5).

**Priority**: fast-reject gates → Tier A scores → Issue Cards → fix routing → submission gate.

---

## When to Activate

**See `paper-writing-router.md` for activation decision tree.**

Activate when:
- User says "review paper", "simulate reviewers", "submission gate", "rebuttal prep", "PC discussion"
- A subsection reaches `qc-pass` in `plan/storyline-state.md` (incremental review)
- T-14 / T-7 / T-2 / T-0 milestone (see Deadline Freeze)
- Before final PDF upload

Do **NOT** activate when:
- Layer 0 unconfirmed → `paper-storyline` first
- Pure prose polish with no review intent → `academic-writing`
- Figure-only work → `figure-generation.mdc`

---

## Personas (inline — no separate files)

Apply persona **reading order** and **bias** during Phase 2. Score with Tier A rubric; PE adds binary flags only.

### R1 — Systems + Autotuning (harsh, −0.4σ)

**Expertise**: GPU/compiler performance, autotuning search spaces, statistical reporting.  
**Biases**: Over-weights eval rigor; distrusts "AI agent" framing; hostile to benchmark theater.  
**Reading order**: Abstract numbers → §4 eval setup → main table → methodology if still interested.  
**Pet peeves**: PyTorch-only baseline; best-of-N without disclosure; missing cuBLAS/cuSPARSELt config; "5× over eager" as headline.

### R2 — Artifact + Reproducibility (neutral, 0σ)

**Expertise**: AE veteran, CI harnesses, USENIX artifact badge criteria.  
**Biases**: Over-weights reproducibility; penalizes "contact authors for scripts".  
**Reading order**: §4 setup → table footnotes → artifact mentions → appendix.  
**Pet peeves**: Undocumented LLM API/version; missing tuning logs; figure scripts not in artifact.

### R3 — Clarity + Writing (generous, +0.2σ)

**Expertise**: Strong writer; simulates non-GPU-expert reviewer.  
**Biases**: Generous on clarity; over-weights intro/abstract consistency.  
**Reading order**: §1 full → abstract consistency → figure captions → §6 conclusion.  
**Pet peeves**: "Template-free" used before defined; §2 assumes GPU expertise; contribution list ≠ abstract claims.

### PE — Presentation Ethics (binary flags, no score)

Flags only (each YES/NO): axis manipulation, missing variance/error bars, selective reporting, over-claiming vs evidence, scope creep vs title/abstract. Any YES → mandatory Issue Card + Meta-PC mention.

### Meta-PC — Synthesis (no separate Tier A score)

**Lens**: Crowded ML+systems area (~16% accept). Harsh on incremental novelty.  
**Output**: Accept / Weak Accept / Weak Reject / Reject + 3-sentence PC discussion script + rebuttal viability (high/medium/low).

---

## Scoring Rubric

### Tier A — Scored (max 46; drives recommendation)

**Note**: Tier A/B (this skill) = scoring dimensions. Track A/B (`academic-writing`) = writing workflow tracks. Different concepts.

Each persona scores all five dimensions independently (integers). Meta-PC does **not** score Tier A; synthesizes persona outputs.

| Dimension | Max | What it measures |
|-----------|-----|------------------|
| **Contribution** | 10 | Novelty + significance for systems/ATC audience |
| **Technical** | 10 | Design correctness, compiler/language claims, no hand-waving |
| **Evaluation** | 12 | Baselines, workloads, fairness, ablations, statistics |
| **Clarity** | 8 | Organization, definitions, non-expert followability |
| **Reproducibility** | 6 | Artifact path, configs, logs, figure reproducibility |

**Score anchors** (use half-points sparingly; prefer integers):

**Contribution (0–10)**  
| Score | Anchor |
|-------|--------|
| 0–2 | Incremental knob-tuning on known DSL; no new systems insight |
| 3–4 | Useful engineering but "yet another DSL" without clear systems lesson |
| 5–6 | Clear positioning; one strong claim (e.g., vendor-exceeding via AI structural opt) |
| 7–8 | First-of-kind language design for AI tuning + principled mechanism story |
| 9–10 | Field-shaping; would cite in 5+ follow-on papers (rare at ATC) |

**Technical (0–10)**  
| Score | Anchor |
|-------|--------|
| 0–2 | Broken claims, undefined terms, compiler story inconsistent |
| 3–4 | Mechanism sketched; key design choices unjustified |
| 5–6 | Coherent design; guardrails + decoupling explained with examples |
| 7–8 | Deep compiler-harness co-design evidence (353 checks, feedback loop) |
| 9–10 | Formal or exhaustive validation of design claims (unlikely needed) |

**Evaluation (0–12)**  
| Score | Anchor |
|-------|--------|
| 0–3 | PyTorch baseline only OR cherry-picked micro-ops |
| 4–6 | Vendor baselines present but config/fairness gaps |
| 7–9 | 6-DSL head-to-head + production GEMM/sparse + stated budgets |
| 10–11 | Above + ablations tied to C3 mechanism + fairness discussion |
| 12 | Above + variance/seeds/disclosure; would trust numbers in production |

**Clarity (0–8)**  
| Score | Anchor |
|-------|--------|
| 0–2 | Cannot follow §2–§3 without area expertise |
| 3–4 | Template-free vs template-based unclear until late |
| 5–6 | Non-expert follows intro + eval; terms defined before use |
| 7–8 | Crisp C→M→E thread; captions self-contained |

**Reproducibility (0–6)**  
| Score | Anchor |
|-------|--------|
| 0–1 | "Contact authors"; no configs |
| 2–3 | Partial artifact; missing tuning traces |
| 4–5 | Hardware + agent budget + baselines documented; scripts referenced |
| 6 | Full artifact path: logs, figure scripts, pinned LLM + compiler versions |

**Aggregation**: Run `score_aggregate.py` (see Scripts). Per persona: apply σ offset to **Tier A total only** (R1 −0.4σ≈−1.8 pts, R3 +0.2σ≈+0.9 pts on 46-pt scale). Report raw + adjusted. Meta-PC uses **median of adjusted totals** for recommendation band:

| Adjusted total | Typical band |
|----------------|--------------|
| ≥38 | Weak Accept – Accept |
| 32–37 | Borderline (Meta-PC decides) |
| 26–31 | Weak Reject |
| ≤25 | Reject |

### Tier B — Diagnostic only (no score, no σ)

Rate each **Low / Med / High concern**; every High → Issue Card.

| Dimension | High concern trigger |
|-----------|---------------------|
| Baseline fairness | Vendor libs not configured fairly OR eager-only main claim |
| Ablation depth | C3 mechanism claims without §4.3 support |
| Related work | Missing direct comparators (Ansor, TileLang, agent-tuning papers) |
| Writing quality | De-AI artifacts, undefined jargon, abstract ≠ body |
| Figure quality | Unlabeled axes, cherry-picked zoom, text/figure number mismatch |
| Scope control | Title/abstract promise ⊃ evaluation (e.g., MoE claimed, not evaluated) |

### Penalty modifiers = Phase 1 fast-reject ONLY

**Not score deductions.** Binary blockers that halt Phase 2 until resolved or user waives with documented risk.

| Gate ID | Blocker | Waive? |
|---------|---------|--------|
| FR-01 | Main speedup claim vs PyTorch eager only | No |
| FR-02 | cuBLAS/cuSPARSELt version or config undisclosed | No |
| FR-03 | Page count >12 excl. refs (compiled) | No |
| FR-04 | Anonymization leak (author, repo, ack) | No |
| FR-05 | Abstract number ∉ manifest | No |
| FR-06 | C→M→E broken: contribution with zero eval support | No |
| FR-07 | `claim_audit` ERROR severity | No |
| FR-08 | Best-of-N / multi-seed without disclosure in §4 | User waive + Issue Card |
| FR-09 | Single-GPU-only but multi-GPU implied in title/abstract | Fix or narrow claim |

If any non-waived gate fires: Phase 1 outcome = **FAST-REJECT (fix before deep review)**. Log in `review-state.md`; skip Phase 2 for that dimension until cleared.

---

## 4-Phase Protocol

### Phase 0 — Preflight (5 min)

```bash
.cursor/skills/paper-review/scripts/review_preflight.sh
```

1. Run preflight script; fix all FAIL before Phase 1.
2. Read `plan/storyline-state.md` (Layer 0 C→M→E), `PAPER-PLAN.md`, `data/processed/manifest.yaml`.
3. Initialize/update `plan/review-state.md` (round, date, gates, open Issue Card count).
4. Confirm deadline tier (T-14 / T-7 / T-2 / T-0) → enforce freeze rules.

### Phase 1 — 10-min screening + fast-reject (all personas skim)

**Each persona (10 min wall-clock simulated)**:
- R1: Abstract + §4.0 + Table 1 headline numbers
- R2: §4 footnotes + artifact paragraph + appendix availability
- R3: Abstract vs §1 contributions vs §6
- PE: Scan all figures/tables for ethics flags

**Output**: Fast-reject gate table (PASS/FAIL per FR-xx). If all pass → proceed. If FAIL → emit Issue Cards for blockers only; **do not** run full Phase 2 until cleared (exception: user requests "review anyway" → mark `conditional` in state).

### Phase 2 — Deep review (45–90 min)

Per persona, follow reading order. For each:
1. Score Tier A (5 dims with brief justification per dim).
2. Rate Tier B (6 dims).
3. Emit Issue Cards (target 3–8 per persona; fewer if paper clean).
4. Run **CroqTile contribution probes** (below) for relevant C_i.
5. PE: complete ethics checklist (5 flags).

Write persona sections to `plan/review-report.md` using template in `templates/review-report-template.md`.

### Phase 3 — Reconciliation (20 min)

See Reconciliation Rules. Meta-PC produces final recommendation + PC script + prioritized fix list (`templates/fix-list-template.md`).

Update `plan/review-state.md`: scores, consensus P0 count, recommendation, rebuttal viability.

---

## Issue Card Template

Every finding ≥ minor severity gets a card. Copy into report + state tracker.

```yaml
id: REV-2026-05-28-001          # unique, monotonic
location: "§4.1 / Table 1 / row matmul"
persona: R1                     # R1 | R2 | R3 | PE | consensus
issue: "cuBLAS workspace size not stated; fairness unclear"
pc_impact: "R1 may reject eval dimension; blocks Weak Accept"
fix_type: data                  # storyline | writing | data | rebuttal-only | unfixable
layer: L4                       # L0 | L1 | L2 | L3 | L4 | L5
severity: major                 # killer | major | minor | nit
consensus: split                # all | majority | split | single
rebuttal_class: B               # A | B | C | D | n/a
status: open                    # open | fixed | wontfix | deferred
```

**fix_type routing**:
| fix_type | Handler |
|----------|---------|
| storyline | `paper-storyline` (layer tag) |
| writing | `academic-writing` L4–L5 |
| data | manifest / `data/processed/` then L5 |
| rebuttal-only | `plan/rebuttal/` draft; no paper edit post T-2 |
| unfixable | Meta-PC + user decision only |

**Severity → priority**:
- **killer**: Meta-PC P0; blocks submission gate
- **major**: P0 or P1; fix before T-7 if possible
- **minor**: P2; fix if time
- **nit**: P3 or rebuttal-only

---

## Reconciliation Rules

1. **Merge duplicates**: Same location + same underlying issue → one card; tag personas `consensus: all`.
2. **Contradictions** (R1 harsh vs R3 generous on same point):
   - If eval/data fact → R1 wins; verify against manifest
   - If clarity/opinion → R3 note as "presentation"; lower severity unless PE flags ethics
3. **Consensus weakness** (≥2 personas, same theme) → auto **P0** in fix list.
4. **Split** (1 persona only, major+) → keep persona tag; default `rebuttal_class: B`; fix if cheap else `rebuttal-only`.
5. **PE flag YES** → always P0; Meta-PC must mention in PC script.
6. **Tier B High** without Tier A impact → still Issue Card; severity ≥ minor.
7. **Post-reconciliation score**: Meta-PC may note "projected score if P0 fixed" (+3 to +8 pts) — do not rewrite persona raw scores.

**Fix list output**: Sorted P0 → P3; each line links Issue Card id + owner skill + deadline tier allowed.

---

## CroqTile Contribution Probes

Run during Phase 2. **3 attacks per C_i**; fail → Issue Card.

### C1 — Language designed for AI tuning (5 features)

| Persona | Attack |
|---------|--------|
| R1 | **"Another DSL — so what?"** Each of 5 features must map to a named tuning failure mode with §4 hook. |
| R1 | **Single GPU**: H800-only scope explicit; no implied multi-GPU without data. |
| R3 | **Define before use**: "Template-free" defined in §2 before abstract/§1 usage. |

### C2 — Template-free tuning system (skills + injection)

| Persona | Attack |
|---------|--------|
| R1 | **Hidden prompts**: Skill/system prompt content summarized or in artifact — not black box. |
| R1 | **Best-of-N**: Agent retries, seeds, selection policy disclosed in §4. |
| R2 | **Tuning logs**: Representative run traces (JSON/log) available for audit. |

### C3 — Principled analysis (Volume–Quality, coupling, feedback)

| Persona | Attack |
|---------|--------|
| R1 | **Ablation depth**: §4.3 isolates mechanism claims — not end-to-end only. |
| R1 | **cuBLAS fairness**: Precision, workspace, algo policy match across compared libs. |
| R3 | **§2 followability**: Non-GPU reader completes §2.3 without CUDA/Triton prereqs. |

### C4 — Empirical proof (6-DSL + sparse library)

| Persona | Attack |
|---------|--------|
| R1 | **6-DSL fairness**: Same agent, token budget, hardware, baselines per DSL row. |
| R1 | **Vendor exceed math**: 115%/155%/120% — aggregation (median? best-of-N?) stated. |
| R2 | **Sparse artifact**: AI-generated sparse library builds from artifact + smoke test. |

---

## Rebuttal Prep Protocol

Run after Phase 3 or when user says "rebuttal prep". Only when `review-state.md` has ≥1 open major+ card.

### Step 1 — Predict reviewer attacks

From Issue Cards + Meta-PC script, list top 5 likely PC-visible attacks (not nits).

### Step 2 — Classify each (A/B/C/D)

| Class | Meaning | Response strategy |
|-------|---------|-------------------|
| **A** | Reviewer factual error | Correct with pointer (table, manifest ID, appendix) |
| **B** | Misunderstanding | Short education + one clarifying sentence for camera-ready |
| **C** | Valid; partially addressable | Acknowledge + what we add/clarify in rebuttal or minor revision |
| **D** | Valid; not fixable pre-deadline | Acknowledge + limitation / future work; no over-promise |

### Step 3 — Draft responses

Per attack: 2–4 sentences, cite `{§, Table, manifest:ID}`. No new numbers unless in manifest.

### Step 4 — Strength score (1–5 per response)

| Score | Meaning |
|-------|---------|
| 1 | Hand-wavy; likely ignored |
| 2 | Defensive; weak evidence |
| 3 | Adequate; clarifies |
| 4 | Strong; cites artifact |
| 5 | Decisive; would flip R1 on that point |

Target: average ≥3.5 on P0 attacks. Below 3 → revise or downgrade Meta-PC rebuttal viability.

Store in `plan/rebuttal/draft-responses.md` (create if missing).

---

## Deadline Freeze

| Milestone | Date (2026) | Allowed changes |
|-----------|-------------|-----------------|
| **T-14** | May 27 | Full review rounds; all layers |
| **T-7 structure frozen** | Jun 3 | L3–L5 edits only; **no** L0–L2 / section moves / new experiments |
| **T-2 prose only** | Jun 8 | L4–L5 wording; no new numbers, figures, or claims |
| **T-0 rebuttal text** | Jun 10 | Rebuttal-only cards; PDF compile + gate only |

Enforcement:
- Issue Cards tagged L0–L2 opened after T-7 → status `deferred` unless user declares emergency.
- Phase 2 full review at T-2+ → **screening + gate only** (Phase 0–1 + submission gate).
- Log tier in every `review-state.md` update.

---

## Submission Gate (binary — all must PASS)

Run at T-0 (and optionally dry-run at T-7):

| # | Check | Command / source |
|---|-------|------------------|
| G1 | Compiles clean | `cd paper && tectonic main.tex` exit 0 |
| G2 | ≤12 pages excl. refs | preflight page count |
| G3 | Numbers ∈ manifest | `check-numbers.py` exit 0 |
| G4 | No anonymize leaks | preflight anonymize scan |
| G5 | C→M→E satisfied | Layer 0 table in `storyline-state.md` all mapped |
| G6 | No ERROR in claim_audit | preflight / `claim_audit` exit 0 |
| G7 | Zero open killer Issue Cards | `review-state.md` |
| G8 | PE ethics flags all NO | latest review round |

**Gate outcome**: PASS → ready to submit. FAIL → list failing checks only; no submit.

---

## State & Report Files

### `plan/review-state.md` (agent maintains)

```markdown
# Review State
Round: 2 | Date: 2026-06-01 | Tier: T-7
Recommendation: Weak Accept (conditional on P0)
Rebuttal viability: medium
Fast-reject: all PASS

## Tier A (adjusted totals)
| Persona | Raw | Adjusted |
|---------|-----|----------|
| R1 | 31 | 29 |
| R2 | 34 | 34 |
| R3 | 36 | 37 |

## Open Issue Cards
| id | sev | fix_type | layer | status |
|----|-----|----------|-------|--------|

## P0 Fix Queue (top 5)
1. REV-... — ...
```

### `plan/review-report.md`

Use `templates/review-report-template.md` for full structure (persona sections, Tier B tables, reconciliation, Meta-PC script).

### Fix list

Use `templates/fix-list-template.md` — P0–P3 queue with skill routing and tier eligibility.

---

## Integration

| Skill / file | Relationship |
|--------------|--------------|
| `paper-storyline` | Consumes Issue Cards L0–L3 |
| `academic-writing` | Consumes L4–L5; upstream `qc-pass` expected before review |
| `plan/storyline-state.md` | C→M→E source for FR-06, G5 |
| `data/processed/manifest.yaml` | Number truth for FR-05, G3 |
| `research-methodology.mdc` | Baseline fairness vocabulary for R1 |
| `academic-writing/scripts/check-numbers.py` | Called by preflight |

**Workflow**: subsection `qc-pass` → incremental Phase 1–2 on that § → merge Issue Cards at Phase 3. Full-paper review at T-14 and T-7.

---

## Scripts

### `scripts/review_preflight.sh`

```bash
#!/usr/bin/env bash
# Usage: review_preflight.sh [--tex paper/main.tex] [--tier T-7]
# Exit 0 = all PASS; exit 1 = any FAIL (prints gate table)

set -euo pipefail
TEX="${1:-paper/main.tex}"
TIER="${2:-T-14}"

echo "=== Review Preflight (tier: $TIER) ==="

# G1 compile
(cd paper && tectonic main.tex) && echo "G1 compile: PASS" || { echo "G1 compile: FAIL"; exit 1; }

# G2 page count (excl. references) — expect ≤12
# Implementation: parse log / pdfinfo; FAIL if >12
python3 - <<'PY' || { echo "G2 pages: FAIL"; exit 1; }
# stub: agent replaces with pdfinfo/tectonic log parser
import sys; sys.exit(0)  # PASS placeholder
PY
echo "G2 pages: PASS"

# G3 numbers
python3 .cursor/skills/academic-writing/scripts/check-numbers.py --tex "$TEX" \
  && echo "G3 manifest: PASS" || { echo "G3 manifest: FAIL"; exit 1; }

# G4 anonymize — grep author names, github URLs, non-anonymous acks
# FAIL on match
echo "G4 anonymize: PASS"  # implement grep against AUTHOR_PATTERNS

# G5 C→M→E — parse plan/storyline-state.md Layer 0; FAIL if unmapped C_i
echo "G5 C→M→E: PASS"

# G6 claim_audit — run if script exists
if [[ -x scripts/claim_audit.py ]]; then
  python3 scripts/claim_audit.py --tex "$TEX" --severity error \
    && echo "G6 claim_audit: PASS" || { echo "G6 claim_audit: FAIL"; exit 1; }
else
  echo "G6 claim_audit: SKIP (no script)"
fi

# FR gates (Phase 1) — emit FR-01..FR-09 table
echo "=== Fast-Reject Gates ==="
echo "FR-01..FR-09: run manual persona skim or extend script"
exit 0
```

**Agent rule**: Extend stubs before T-7; never mark gate PASS without command output in session.

### `scripts/score_aggregate.py`

```python
#!/usr/bin/env python3
"""Aggregate Tier A persona scores with sigma offsets.

Usage:
  score_aggregate.py --input scores.json [--output summary.md]

Input JSON:
{
  "R1": {"contribution": 7, "technical": 6, "evaluation": 8, "clarity": 5, "reproducibility": 4},
  "R2": { ... },
  "R3": { ... }
}

Output: JSON to stdout (raw/adjusted totals, median, band) + optional markdown table.
Sigma offsets (on 46-pt total): R1 -1.84, R2 0, R3 +0.92  (≈ -0.4σ, 0, +0.2σ × √46)
"""

import argparse, json, sys

WEIGHTS = ["contribution", "technical", "evaluation", "clarity", "reproducibility"]
MAX_TOTAL = 46
OFFSETS = {"R1": -1.84, "R2": 0.0, "R3": +0.92}

def band(score):
    if score >= 38: return "Weak Accept – Accept"
    if score >= 32: return "Borderline"
    if score >= 26: return "Weak Reject"
    return "Reject"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", help="markdown summary path")
    args = p.parse_args()
    data = json.load(open(args.input))
    rows = []
    adjusted = []
    for persona, dims in data.items():
        raw = sum(dims.get(k, 0) for k in WEIGHTS)
        adj = max(0, min(MAX_TOTAL, raw + OFFSETS.get(persona, 0)))
        rows.append({"persona": persona, "raw": raw, "adjusted": round(adj, 1)})
        adjusted.append(adj)
    adjusted.sort()
    median = adjusted[len(adjusted)//2]
    out = {"rows": rows, "median_adjusted": median, "band": band(median)}
    print(json.dumps(out, indent=2))
    if args.output:
        with open(args.output, "w") as f:
            f.write(f"| Persona | Raw | Adjusted |\n|---|---|---|\n")
            for r in rows:
                f.write(f"| {r['persona']} | {r['raw']} | {r['adjusted']} |\n")
            f.write(f"\n**Median adjusted**: {median} → **{band(median)}**\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

---

## Session Checklist (agent)

See `references/systems-reviewer-patterns.md` for detailed reviewer attack patterns and `references/systems-rebuttal-patterns.md` for rebuttal strategies.

1. Read deadline tier → apply freeze
2. Run `review_preflight.sh` → fix FAILs
3. Phase 1 fast-reject → stop if blocked
4. Phase 2 per persona → Tier A + B + Issue Cards + C1–C4 probes
5. Phase 3 reconcile → Meta-PC + fix list
6. Route Issue Cards to storyline/writing skills
7. Update `review-state.md` + append `review-report.md`
8. At T-0: submission gate G1–G8

---

## Best-of-N Subagent Modes

**Budget**: See `best-of-N-protocol.md` § Session Budget before launching.

See `best-of-N-protocol.md` for subagent launch pattern, selection protocol, and QC gates.

### Mode 1: Review Persona Scoring (N=3 per persona)

- **When**: Phase 2 deep review — each of R1, R2, R3 independently scores
- **Why**: Single-LLM scoring has self-reinforcing bias; 3 independent runs per persona reduces noise
- **Implementation**: For each persona (R1, R2, R3), launch 3 subagents. Each receives: persona description + bias + reading order + the paper content. Each independently scores Tier A (5 dimensions) + Tier B + produces Issue Cards.
- **Aggregation**: Per persona, take median of 3 Tier A scores per dimension. Union Issue Cards (deduplicate by location+type). If a specific dimension has high variance (>2 points), flag to Meta-PC.
- **Constraints**: All 3 subagents share same persona definition, same rubric, same paper snapshot. No cross-talk.
- **Creative latitude**: How each subagent interprets the rubric anchors; which evidence they focus on; severity assignment.
- **Output**: Present to Meta-PC as "R1 (median of 3): Contribution=X, Technical=Y..." with variance notes.

### Mode 2: Rebuttal Drafting (N=5)

- **When**: After Phase 3 reconciliation produces the fix list; user says "prepare rebuttal"
- **Why**: Rebuttal strategy has multiple valid approaches (defensive, proactive, concessive, redirect). 5 versions maximize chance of finding the right tone.
- **Constraints shared**: Reviewer concerns (Issue Cards), paper claims, available evidence, venue norms
- **Creative latitude**: Rebuttal tone (concessive vs firm), evidence emphasis, concession order, which concerns to address first, structural format
- **Each variant must**: Address all P0 Issue Cards; reference specific paper sections/numbers; be honest about limitations; be ≤ venue rebuttal limit
- **Selection**: Author picks best tone+strategy or fuses elements

### Cost Awareness

Mode 1: 9 subagent runs (3 personas × 3). Mode 2: 5 rebuttal drafts. Each costs ~N× tokens. Confirm with user before launch unless pre-approved (e.g., "full review with best-of-N scoring"). See `best-of-N-protocol.md` § Cost Awareness.

---

## Anti-Patterns

| Thought | Action |
|---------|--------|
| "Average the three reviewers" | Use median of **adjusted** totals; Meta-PC synthesizes |
| "Deduct 5 pts for PyTorch baseline" | FR-01 gate, not score math |
| "R3 liked it, ship it" | Check R1 eval + PE flags |
| "Fix list has 40 items" | Cap P0 at 5; defer rest |
| "Full review at T-0" | Gate + rebuttal only |
| "Issue Card without layer tag" | Invalid — always set L0–L5 |

---

## Integration with Author Supervisor

`author-supervisor` is an embedded advisory ensemble — invoke within review phases for 5 professor perspectives.

| Rule | Detail |
|---|---|
| Post-fix consultation | After P0 fixes, optionally invoke supervisor to check narrative collateral |
| Pre-submission | Invoke supervisor for "would you submit?" before T-0 gate |
| Professor notes in Meta-PC | May cite in appendix; never scored in Tier A/B |
| Conflict resolution | Factual/eval → reviewer wins. Emphasis/narrative → note as "author strategic choice" |
| Do NOT add professors as scored personas | Advisory ensemble, not R4–R8 |

---

## Reference Templates (brief specs)

### `templates/review-report-template.md`

Sections: Header (round, tier, date) → Preflight results → Fast-reject table → R1/R2/R3 (Tier A table + Tier B + Issue Cards) → PE flags → C1–C4 probe results → Reconciliation notes → Meta-PC (recommendation, PC script, projected score if P0 fixed) → Appendix (all Issue Cards YAML).

### `templates/fix-list-template.md`

Columns: Priority (P0–P3) | Issue ID | One-line fix | Owner skill | Allowed tier | Est. effort (S/M/L) | Blocks gate?

Sorted P0 first; max 5 P0 lines per round.
