---
name: academic-writing
description: "Use when implementing Layer 4-5 prose for confirmed storyline subsections, reconciling brownfield drafts against L3, or running QC before paper-review. Two tracks: full QC (Track A) and fast reconciliation (Track B). CroqTile paper, June 10 deadline."
---

# Academic Writing (Layer 4–5 + QC)

**Upstream**: `paper-storyline` (Layers 0–3). **This skill owns Layer 4–5 execution and quality gates.**

Brownfield context: ~1640-line draft exists. All Layer 3 confirmed (2026-05-28). Layer 4–5 pending. Deadline: **June 10, 2026** (~13 days from May 28).

**Priority order**: storyline correctness → number accuracy → claim-evidence alignment → prose quality → de-AI polish.

---

## When to Activate

**See `paper-writing-router.md` for activation decision tree.**

Activate when:
- User says "write §X", "implement paragraph plan", "reconcile section", "QC subsection", "fix prose vs storyline"
- Layer 3 is confirmed in `plan/storyline-state.md` and user wants Layer 4 plan or Layer 5 LaTeX
- `paper-review` returns Issue Cards tagged L4/L5
- `author-supervisor` invoked for paragraph-level or section-level advice (5 professor lenses)
- Numbers mismatch suspected between `data/processed/`, `main.tex`, figures

Do **NOT** activate when:
- Layer 3 unconfirmed → use `paper-storyline` first
- Pure figure generation → `figure-generation.mdc`
- Structural realignment (contributions, section budget) → `paper-storyline` Layer 0–2
- Single typo with no storyline/number implications

---

## Two Tracks

| | **Track A — Full QC** | **Track B — Reconciliation** |
|---|---|---|
| **When** | New subsection, major rewrite, L4 not confirmed | L3 confirmed + existing prose in `main.tex` |
| **Layer 4** | Write/confirm full writing plan per paragraph | Skip unless reconciliation finds alignment gaps |
| **Layer 5** | Write/replace LaTeX from plan | Patch only flagged paragraphs |
| **QC** | Full 3-round QC (below) | Reconciliation diff + lint + anchor scoring |
| **De-AI** | Per deadline tier | Only on touched paragraphs |

**Default for this repo**: Track B for §1–§6 (draft exists). Track A when user says "rewrite" or reconciliation emits `alignment:major`.

**Note**: Track A/B (this skill) = writing workflow tracks. Tier A/B (`paper-review`) = scoring rubric tiers. Different concepts.

---

## Workflow Overview

```
Read plan/storyline-state.md (L3 map for target subsection)
        │
        ├─ Track B? → Reconciliation Mode (script or manual diff)
        │       ├─ pass → lint + anchor score → done
        │       └─ issues → route (see Routing Table)
        │
        └─ Track A? → Layer 4 writing plan → user approves batch
                → Layer 5 LaTeX (paper-writing.mdc)
                → QC Round 1 (structure) → Round 2 (numbers) → Round 3 (de-AI)
                → update storyline-state.md L4/L5
                → hand off to paper-review when subsection marked qc-pass
```

Work **one subsection per session**. Never batch-write multiple subsections without explicit user request.

---

## Layer 4: Writing Plan

For each L3 paragraph, produce:

| Field | Content |
|-------|---------|
| `id` | `§3.2-¶4` |
| `archetype` | One of 10 families (+ optional sub-tag) |
| `topic_sentence` | Exact opening sentence (~1 sentence) |
| `body` | Bullet list: data points, citations, `\ref{}` targets |
| `form` | prose \| table \| figure \| equation \| listing |
| `length` | Target sentences or lines |
| `style` | e.g. mechanism-first, contrast-first, number-led |
| `anchors` | bool — needs full paragraph score in QC |

**Archetype families** (assign exactly one primary; sub-tags optional):

| Family | Job | Sub-tags (18) |
|--------|-----|---------------|
| **Problem** | Gap, pain, missing capability | `gap-result`, `gap-capability`, `pain-point` |
| **Rationale** | Why this design/choice | `design-choice`, `scope`, `threat-model` |
| **Mechanism** | How it works | `pipeline`, `check`, `model`, `workflow` |
| **Contrast** | vs baseline/alternative | `vs-vendor`, `vs-template`, `vs-naive-baseline` |
| **Setup** | Eval/config definitions | `hardware`, `workload`, `protocol`, `metrics` |
| **Result** | Headline + table/figure commentary | `headline`, `table-walk`, `figure-walk`, `takeaway` |
| **Interpretation** | What result means | `implication`, `ablation-read`, `scaling` |
| **Validity** | Limits, fairness | `limitation`, `fairness`, `sensitivity` |
| **Positioning** | Prior work / novelty | `prior-work`, `differentiation`, `scope-claim` |
| **Bridge** | Transitions | `section-open`, `section-close`, `contrib-handoff` |

**Paragraph contract** (every L5 paragraph must satisfy):

1. **Opens with claim** — first sentence states the paragraph's job (matches L3 topic sentence ± minor polish).
2. **Evidence within 2 sentences** — number, citation, `\autoref{}`, or defined term; no unsupported assertions.
3. **Single job** — one archetype family; split if two jobs detected.
4. **Forward link** — last sentence connects to next paragraph OR closes subsection arc.
5. **Terminology lock** — terms match Terminology Matrix in `croqtile-templates.md`.
6. **Number provenance** — every numeric claim traceable to `data/processed/` manifest entry OR explicit citation.

Checkpoint (Track A only):
```
§X.Y — Writing Plan (N paragraphs)
[table: id | archetype | topic_sentence | form | length | anchors]

Approve plan / Adjust ¶k / Escalate to L3
```

Record approval in `plan/storyline-state.md` Layer 4 table.

---

## Layer 5: Implementation

1. Edit `paper/main.tex` (or included `.tex` chunks) per approved L4 plan.
2. Follow `paper-writing.mdc`: labels, `\autoref{}`, tectonic compile, line length ≤100.
3. **Do not** edit `figures/out/*.svg` directly — route figure issues to `figure-generation.mdc`.
4. After subsection: `cd paper && tectonic main.tex` — fix compile errors before QC.
5. Update `plan/storyline-state.md` Layer 5 row: `draft | qc-pending | qc-pass | frozen`.

**Re-alignment triggers** (STOP, go up):
- Planned number absent from manifest → flag user, do not invent
- L3 paragraph count ≠ written paragraph count → Reconciliation or L3
- Paragraph >150% of planned length → trim or re-plan L4
- Claim contradicts `research-methodology.mdc` eval dimensions

---

## Reconciliation Mode (Track B)

**Goal**: Diff confirmed L3 paragraph map vs current `main.tex` prose.

**Steps**:
1. Load L3 map from `plan/storyline-state.md` for target subsection.
2. Segment `main.tex` into paragraphs (blank-line boundaries; skip environments).
3. Align L3 ¶N ↔ tex ¶N (1:1 expected; flag `count-mismatch` if not).
4. For each pair, emit Issue Card fields:

| Check | Issue type | Route |
|-------|------------|-------|
| Topic sentence drift | `alignment:topic` | L4 patch or L3 if storyline wrong |
| Missing evidence | `alignment:evidence` | L5 add data/cite |
| Extra claim not in L3 | `alignment:orphan` | L3 confirm or delete |
| Wrong figure/table ref | `alignment:ref` | L5 fix `\ref{}` |
| Number ≠ manifest | `data:number` | fix tex or `data/processed/` |
| Terminology violation | `prose:term` | L5 + terminology matrix |
| Archetype mismatch | `alignment:archetype` | L4 replan |
| Major structural gap | `alignment:major` | **Switch to Track A** |

Run `scripts/reconcile.py --subsection §3.2` when available; else manual table.

**Reconciliation output format**:
```
§3.2 Reconciliation — 4 paragraphs, 2 issues
| ¶ | L3 topic (trunc) | Status | Issue |
|---|------------------|--------|-------|
| 1 | Compiler co-designed... | OK | — |
| 2 | 353 static checks... | FAIL | data:number — tex says 350, manifest 353 |
...
Route: L5 patch ¶2 | Run numbers-check | Continue
```

---

## Numbers Triangle

All numeric claims must be consistent across:

```
data/processed/*.json|csv  →  paper/main.tex  →  figures/out/*.svg (via figures/src/*.js)
```

**Manifest**: `data/processed/manifest.yaml` lists canonical values:
```yaml
- id: static_checks_count
  value: 353
  sources: [paper §3.3 ¶2, tab:compiler-checks]
- id: compile_prune_seconds
  value: "3-8"
  unit: s
  sources: [paper §3.3 ¶2, §4.3 ablation]
```

**Protocol**:
1. Before writing numbers, read manifest entry.
2. After L5 edit, run `scripts/check-numbers.py` (or grep manifest IDs).
3. Figure scripts must read same processed files — never hardcode divergent values.

**Failure**: emit `data:number` Issue Card; block `qc-pass` until resolved.

---

## QC Protocol (Track A + post-reconciliation)

Three rounds. **Do not skip Round 2.**

### Round 1 — Structure & Alignment (all paragraphs)

Pass/fail lint per paragraph:
- [ ] Paragraph count matches L3
- [ ] Opening sentence matches L3 topic (semantic, not verbatim)
- [ ] Archetype family assigned and consistent
- [ ] No orphan claims (not traceable to L3 or evidence)
- [ ] Transitions present (no double Problem paragraphs unless L3 specifies)
- [ ] Page budget: subsection within ±0.3 pages of Layer 1 target
- [ ] C→M→E: subsection serves assigned contribution(s)

### Round 2 — Numbers & References (all paragraphs with numbers)

- [ ] Every number matches manifest (Numbers Triangle)
- [ ] `\autoref{fig:}`, `\autoref{tab:}` resolve and match L4 body refs
- [ ] Figure-claim mapping per `croqtile-templates.md` (each figure cited where L3 says)
- [ ] Eval claims match `research-methodology.mdc` dimensions (hardware, shapes, baselines)
- [ ] No fabricated or rounded-without-source numbers

### Round 3 — De-AI & Prose (tiered scope)

Invoke `de-ai-style.mdc` passes per **deadline tier**:

| Tier | Date | Scope |
|------|------|-------|
| **T-14** | May 27+ | Full paper all rounds |
| **T-7** | Jun 3+ | §1 Intro + §4 Evaluation only |
| **T-2** | Jun 8+ | Flagged paragraphs only (from R1/R2 or review) |

Passes: (1) vocabulary, (2) structure, (3) academic-specific — per `de-ai-style.mdc`.

**T-2 freeze**: prose-only edits on flagged items; no storyline/number changes without explicit user override.

### Paragraph Scoring (anchors + touched only)

**Anchor paragraphs** (full 5-dimension score 1–5):
- §1 ¶3–7 (gaps, definition, approach)
- §4.1/§4.2/§4.3 first Result paragraph per subsection
- §4.3 ablation takeaway paragraphs (last 2 ¶)
- Any paragraph edited this session

**Dimensions**: claim clarity | evidence density | transition | terminology | de-AI cleanliness

**Non-anchors**: Round 1 lint pass/fail only — do not score.

**Gate**: anchors average ≥4.0 AND no dimension ≤3 → `qc-pass`. Else one revision cycle.

---

## Iteration Budget

| Rule | Limit |
|------|-------|
| Full section cycles (Track A: plan→write→QC→revise) | **Max 2 per subsection per week** |
| Reconciliation patch cycles (Track B) | Max 3 per subsection per week |
| T-2 (Jun 8+) | Prose-only; no L3/L4 changes unless user declares emergency |
| After 2 failed QC cycles | Escalate to user with Issue summary; do not loop silently |

Log cycles in `plan/storyline-state.md` Layer 5 Notes column.

---

## Review Feedback Routing

`paper-review` emits **Issue Cards**. Route by layer tag:

| Tag | Handler |
|-----|---------|
| L0 | `paper-storyline` — contributions/claim |
| L1 | `paper-storyline` — page budget/sections |
| L2 | `paper-storyline` — subsection scope |
| L3 | `paper-storyline` — paragraph storyline |
| L4 | This skill — writing plan adjustment |
| L5 | This skill — LaTeX patch + re-QC |
| `data:*` | Fix manifest/processed data, then L5 |
| `fig:*` | `figure-generation.mdc`, then re-check Numbers Triangle |
| `advisor:*` | Informational — check `author-supervisor` Briefing Notes; apply selected professor suggestions per author choice |

**Advisor vs L3 conflict**: If professor suggestion conflicts with L3 topic sentence, escalate to user — do not pick silently.

Issue Card schema:
```
id: REV-§3.2-003
layer: L5
type: data:number
paragraph: §3.2-¶2
message: "353 vs 350 static checks"
status: open|fixed|wontfix
```

Closed cards require verification command output in session notes.

---

## Section Guides (summary)

Full paragraph templates: `croqtile-templates.md`. Counts below are **mandatory paragraph budgets**.

| Subsection | ¶ count | Archetype spine |
|------------|---------|-----------------|
| **§1 Intro** | 8 | Problem×2 → [optional Mechanism proof] → Setup(def) → Mechanism+Rationale → Bridge(C1–C4) |
| **§2.1 DSL Substrate** | 2 | Setup → Mechanism |
| **§2.2 Template paradigms** | 2 | Contrast → Contrast |
| **§2.3 Why hard** | 2 | Problem → Bridge(to §3) |
| **§3.1 Language** | 6 | Rationale → Mechanism×4 → Bridge |
| **§3.2 Syntax-Context** | 4 | Rationale → Mechanism×2 → Result(token/site) |
| **§3.3 Compiler-Harness** | 4 | Mechanism → Result(353/3-8s) → Mechanism → Bridge |
| **§3.4 Tuning System** | 5 | Rationale → Mechanism×3 → Contrast(vs one-shot) |
| **§4.0 Setup** | 1 | Setup (hardware, baselines, metrics) |
| **§4.1 Cross-DSL** | 3 | Result(headline) → Result(table) → Interpretation |
| **§4.2 Sparse** | 3 | Result(headline) → Result(figure) → Interpretation |
| **§4.3 Ablation** | 6 | Result×4 (8 data points) → Interpretation → Validity |
| **§5 Related Work** | 3 | Positioning×3 |
| **§6 Conclusion** | 1 | Bridge (recap C1–C4 + numbers + future) |

---

## Anti-Patterns

| Thought / Behavior | Correct action |
|--------------------|----------------|
| "L3 confirmed, prose looks fine" | Run Track B reconciliation anyway |
| "I'll polish then check numbers" | Round 2 before Round 3 — numbers first |
| "Score every paragraph" | Anchors + touched only |
| "Skip L4, I know how to write it" | Track A requires L4 approval in state file |
| "Round 353 to 350, close enough" | Never — manifest is source of truth |
| "Add a strong concluding sentence" | Bridge archetype only where L3 specifies |
| "De-AI the whole paper at T-2" | Flagged paragraphs only |
| "Third full rewrite this week" | Stop — escalate to user |
| "Figure shows 1.18×, text says 1.16×" | Fix triangle before any prose work |
| "paper-review can wait" | Mark `qc-pass` only after R1–R3 gates |

---

## State Tracking

Extend `plan/storyline-state.md`:

```markdown
## Layer 4: Writing Plan
| Subsection | Status | Track | Confirmed |
|------------|--------|-------|-----------|
| §3.1 Language | pending | B | — |

## Layer 5: Implementation + QC
| Subsection | Status | Track | QC | Cycles | Notes |
|------------|--------|-------|-----|--------|-------|
| §1 Intro | draft | B | pending | 0 | reconcile first |
```

Status values: `pending | plan-approved | draft | qc-pending | qc-pass | frozen`

---

## Integration Map

| Resource | Role |
|----------|------|
| `paper-storyline` | L0–L3; escalation for alignment:major |
| `de-ai-style.mdc` | QC Round 3 |
| `paper-writing.mdc` | LaTeX conventions, tectonic |
| `research-methodology.mdc` | Eval dimensions, baseline fairness |
| `figure-generation.mdc` | Figure/script fixes |
| `paper-review` | Downstream; consumes `qc-pass` subsections |
| `croqtile-templates.md` | Paragraph templates, terminology matrix, figure-claim map |
| `examples.md` | Annotated good/bad paragraph examples |

**Priority**: storyline (L3) > numbers (manifest) > QC gates > de-AI polish.

---

## Reference Files

### `croqtile-templates.md`
Per-subsection paragraph templates aligned to L3 state (topic sentence, evidence, transition for all 11 subsections + §4.0 + §5 + §6). Includes **Terminology Matrix** (canonical term → forbidden variants) and **Figure-Claim Mapping** (each `fig:`/`tab:` → allowed claims + manifest IDs). Single source for CroqTile-specific wording.

### `examples.md`
3–5 annotated examples per archetype family showing pass/fail: topic sentence drift, number mismatch, de-AI before/after, Result paragraph done well. Used for calibration — not copied verbatim into paper.

---

## Scripts (`scripts/`)

### `reconcile.py`
```
reconcile.py --subsection §3.2 [--tex paper/main.tex] [--state plan/storyline-state.md]
```
Parses L3 map from state file, segments tex subsection, outputs markdown table of alignments + Issue Cards (JSON lines to stdout). Exit 0 if no `alignment:major` or `data:*`; exit 1 otherwise.

### `check-numbers.py`
```
check-numbers.py [--manifest data/processed/manifest.yaml] [--tex paper/main.tex]
```
Extracts numeric literals from tex (excluding labels/page numbers), matches against manifest IDs referenced in `sources` fields; reports mismatches + unmanifested numbers in eval sections. Exit 1 on any mismatch.

### `lint-paragraphs.py`
```
lint-paragraphs.py --subsection §3.2 [--tex paper/main.tex]
```
Pass/fail checks for Round 1 structural lint (count, orphan detection heuristic, `\ref{}` resolution). No scoring.

### `score-anchors.py`
```
score-anchors.py --subsection §1 [--tex paper/main.tex] [--tier T-7]
```
Scores anchor paragraphs only; outputs dimension table. Used optionally — agent may score manually using QC dimensions.

### `qc-status.py`
```
qc-status.py [--state plan/storyline-state.md]
```
Summary dashboard: subsections by QC status, cycle counts, open Issue Cards count, subsections missing reconciliation.

**Note**: `reconcile.py`, `lint-paragraphs.py`, `score-anchors.py`, `qc-status.py` are stub implementations. When these scripts are not available, follow the equivalent manual protocol described in this skill.

**Agent rule**: Prefer running scripts over manual checks when scripts exist. If script missing, perform equivalent manual protocol and note in state file.

---

## Quick Commands

```bash
# Reconcile one subsection
python .cursor/skills/academic-writing/scripts/reconcile.py --subsection §3.3

# Numbers triangle check
python .cursor/skills/academic-writing/scripts/check-numbers.py

# Compile after L5 edits
cd paper && tectonic main.tex
```

---

## Best-of-N Subagent Modes

**Budget**: See `best-of-N-protocol.md` § Session Budget before launching.

When a mode below applies, launch **N parallel subagents** instead of single-agent execution. Use the prompt template and selection protocol in [`best-of-N-protocol.md`](../best-of-N-protocol.md). Each variant must pass the mode's QC gate before presentation.

### Mode 1: Abstract Best-of-N (N=5)

**When**: User says "write abstract", "rewrite abstract", or L5 for abstract subsection.

**Why**: Abstract is highest-leverage 250 words; worth 5 diverse attempts.

**Constraints shared across all 5**: L0 core claim, C→M→E table, contribution list, headline numbers from manifest, 250-word limit, venue (ATC 2026 12pp).

**Creative latitude**: Opening strategy (result-first vs problem-first vs contradiction-hook), sentence structure, which 3 numbers to headline, emphasis balance (C1 vs C4 lead), hedging level.

**Each variant must**: Match L0 contributions; include ≥3 manifest numbers; define "template-free" before results; not exceed 250 words.

**Selection**: Present all 5 side-by-side; author picks or fuses.

### Mode 2: L5 Paragraph Writing (N=3)

**When**: Track A, Layer 5 implementation for any confirmed L4 paragraph plan.

**Why**: Paragraph-level prose has meaningful style variation; 3 attempts efficient.

**Constraints shared**: L4 writing plan (archetype, topic sentence, body, form, length), paragraph contract (6 rules), terminology matrix, number provenance from manifest.

**Creative latitude**: Sentence structure, evidence ordering within paragraph, transition style, voice register, level of technical depth.

**Each variant must**: Satisfy paragraph contract; use correct L4 archetype; topic sentence matches L3.

**Selection**: Author picks or "take opening from V1, evidence from V3".

### Mode 3: De-AI Polish (N=3)

**When**: QC Round 3 on a subsection that has de-AI issues.

**Why**: De-AI rewrites are style-sensitive; 3 diverse rewrites avoid single-agent patterns.

**Constraints shared**: The original paragraph text, de-AI rules from `de-ai-style.mdc`, meaning must be preserved, numbers must stay exact.

**Creative latitude**: Sentence restructuring, vocabulary choices, active/passive balance, hedge removal strategies, paragraph rhythm.

**Each variant must**: Preserve all claims and numbers exactly; pass de-AI checklist; not introduce new claims.

**Selection**: Author picks the one that sounds most "human-authored professor".

### Mode 4: Track B Reconciliation Strategy (N=3)

**When**: Track B reconciliation finds `alignment:major` — the existing prose significantly deviates from confirmed L3.

**Why**: Multiple bridging strategies exist (preserve structure + adjust claims, rewrite from L3, hybrid).

**Constraints shared**: L3 paragraph map, current tex paragraphs, reconciliation diff output.

**Creative latitude**: How much existing prose to keep, what to rewrite, ordering of fixes, whether to merge/split paragraphs.

**Each variant must**: Result in full L3 alignment after applying; preserve manifest numbers; not introduce unconfirmed claims.

**Selection**: Author picks the path that preserves most of their existing voice.

**Cost awareness**: Best-of-N multiplies token cost by N. Reserve N=5 for abstract only; use N=3 elsewhere. On T-7/T-2 deadline tiers, skip best-of-N unless the user explicitly requests it or the subsection is on the critical path (§1 Intro, §4 Evaluation).

---

## Session Checklist (agent)

0. Read `references/systems-writing-patterns.md` (all sections); `references/systems-eval-methodology.md` (§4 Eval); `references/systems-sentence-bank.md` (L5 drafting); `references/systems-anti-patterns.md` (QC Round 1/3)
1. Read `plan/storyline-state.md` — confirm L3 for target subsection
2. Choose Track A or B (default B for existing draft)
3. Track B: reconcile → route issues
4. Track A: L4 plan → approval → L5 write → tectonic
5. QC R1 → R2 → R3 (respect deadline tier)
6. Score anchors only; lint rest
7. Update state file; hand `qc-pass` subsections to review
8. Respect iteration budget and T-2 freeze
