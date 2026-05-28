# Systems Rebuttal Patterns (Reference)

Effective author-response strategies for OSDI, SOSP, ATC, EuroSys, ASPLOS, PLDI, ISCA, SC, PPoPP, CGO, CC, MICRO, HPCA, NSDI, MLSys, FAST. Paraphrased patterns—not copy-paste templates.

**Venue norms (typical)**
- **USENIX** (ATC, OSDI, NSDI, FAST): short rebuttal window; ~**1 page** (~500–700 words) common; no new experiments after deadline—clarify, point, promise camera-ready fixes.
- **ACM** (SOSP, EuroSys, ASPLOS, PLDI, MICRO, HPCA): often **500–1000 words**; some allow supplemental rebuttal PDF—check CFP.
- **Rebuttal is not revision**: PCs read it alongside reviews; tone and evidence pointers matter more than length.

---

## 1. Rebuttal structure patterns

### Recommended flow
1. **Thank reviewers** (one sentence—no groveling).
2. **Priority order**: address **major/consensus** concerns first (R1 eval fairness before R3 typo).
3. **Evidence**: cite `{§, Table, Figure, appendix, artifact path}`—not new mystery numbers unless already in submitted material or allowed addendum.
4. **Camera-ready commitments**: qualify claims, add footnote, release artifact—only promise what you will ship.
5. **Ask for re-evaluation** on specific points: *"We hope this clarifies concern #2 on baseline fairness."*

### Per-reviewer vs thematic
| Style | When to use |
|-------|-------------|
| **Per-reviewer** (Reviewer 1: … R2: …) | Clear disagreement between reviewers; avoid repeating same answer 3× |
| **Thematic** (Baselines / Reproducibility / Clarity) | 2+ reviewers share concern; saves word budget |

**Word budget (1-page ATC)**
- ~40% eval/fairness (R1 concerns)
- ~25% reproducibility (R2)
- ~20% clarity/novelty (R3 + Area Expert)
- ~15% closing + CR commitments

---

## 2. Response strategies by concern type

### Missing baseline
- **Pattern**: acknowledge gap → state what was run → point to existing or rebuttal table → fairness checklist.
- *"We agree cuBLAS is the right baseline. Table 1 and §4.2 report cuBLAS Lt v12.x with default algo selection; workspace matched per NVIDIA docs. We will add [X] to related work comparison in CR."*
- **Weak**: *"X is concurrent work"* without partial comparison or scoped limitation.

### Overclaiming
- **Pattern**: concede → give **exact replacement wording** for abstract/intro.
- *"We agree 'production-quality' overstates scope. We will revise to: 'on three Hopper GEMM shapes (Table 1), median tuned kernels exceed cuBLAS by …'"*
- **Weak**: defend original wording; argue reviewer misread without quoting new text.

### Reproducibility
- **Pattern**: specific artifact list + timeline.
- *"Artifact (anonymous link in supplementary) includes: Docker pin CUDA 12.4/driver 550.x, `reproduce.sh` for Table 1–3, representative tuning logs under `tuning/logs/` (3 shapes × 1 run). CR adds prompt hash manifest."*
- **Weak**: *"We will open-source everything"* without scope.

### Scope limitation
- **Pattern**: principled boundary + orthogonal future work.
- *"We scope to single-GPU H800 Hopper because multi-GPU introduces NCCL scheduling variables orthogonal to DSL design (§7). We will state this explicitly in §4.1."*

### Fairness attack
- **Pattern**: config table reference + vendor doc alignment.
- *"cuBLAS comparison uses FP16 accumulation policy X, workspace Y, algo Z (§4.2, Table 2 footnotes). We verified configs against [vendor doc §]."*

### Reviewer factual error (Class A)
- **Pattern**: polite pointer, no sarcasm.
- *"We believe Reviewer 1's concern about missing ablation is addressed in §4.3 and Figure 6, which isolates [component]. Happy to clarify caption in CR."*

---

## 3. Tone patterns

| Works | Doesn't work |
|-------|----------------|
| *"You raise a valid point. We …"* | *"The reviewer misunderstood …"* |
| *"We agree and will qualify …"* | *"This is standard practice"* (dismissive) |
| *"Table 1 (submitted) shows …"* | Emotional, sarcastic, ALL CAPS |
| *"We may not have emphasized … §4.2 …"* | Arguing taste on related work |
| Firm + citation: *"Same agent, token budget, and hardware across all six DSLs (§4.4, Table 4)."* | Promising 5 CR sections you can't deliver |

**Evidence-forward rule**: lead with **location + number**, then one-sentence interpretation.

---

## 4. Common rebuttal mistakes (systems)

1. **New experiments contradict narrative** (e.g., added baseline beats you on half the shapes)—undermines paper; better scoped limitation.
2. **Over-promise CR changes** ("new §5, 3 figures, full AE")—PCs remember; Meta-PC downgrades trust.
3. **Minor points first**—burns page limit; harsh reviewers stay unsatisfied.
4. **Ignoring the actual question**—answer what was asked (baseline? variance? logs?).
5. **Invented numbers** not in submission—fast path to reject if caught.
6. **Attacking concurrent work** instead of defending your eval.
7. **Wall of text**—no headings; PC skims in 2 minutes.

---

## 5. CroqTile-specific rebuttal prep (ATC 2026)

Paper: *CroqTile: A GPU Kernel Programming Language Designed for AI Tuning* — template-free AI tuning, 6-DSL comparison, vendor-exceeding GEMM/sparse on H800.

### Predicted R1 attacks → defense snippets

| Attack | Defense snippet (adapt with manifest IDs) |
|--------|---------------------------------------------|
| **Vendor config unfair** | *"§4.2 documents cuBLAS/cuSPARSELt versions, algo policies, and workspace; configs aligned to NVIDIA Hopper guidance. Table 2 footnotes list per-library flags. We will add a one-row fairness checklist in CR."* |
| **Best-of-N undisclosed** | *"§4.1 states agent retry policy, selection criterion (best verified kernel per shape), and token budget. Tuning logs in artifact show iteration counts—not cherry-picked post hoc. We will clarify '115%' is median of N verified runs, not best-of undisclosed pool."* |
| **Why not Triton + same agent?** | *"Table 4 is exactly this: same agent, hardware, and budget across six DSLs including Triton; only CroqTile exceeds vendor libs on stated shapes. We will sharpen §7 to contrast language features (decoupled primitives, compile-time guardrails) not agent quality."* |
| **PyTorch/eager comparison** | *"Primary comparisons are cuBLAS/cuSPARSELt (Table 1). Eager appears only as [context/for related-work critique]; we will demote or remove if it distracts."* |
| **Single GPU / few shapes** | *"We scope to single-GPU H800 and shapes in Table 1; abstract/intro will match. Multi-GPU and full shape sweep are future work—not claimed in CR wording."* |

### Predicted R2 attacks → defense snippets

| Attack | Defense snippet |
|--------|-----------------|
| **LLM API reproducibility** | *"§4.1 names model provider, model ID, and API date; artifact includes `manifest/prompts/` hashes and frozen deps. CR adds temperature/max-tokens table. Full non-determinism discussion in §4.1 limitation paragraph."* |
| **Tuning log availability** | *"Representative logs for Table 1 shapes are in artifact `tuning/logs/` with README reproduce steps. We cannot ship full multi-TB traces; sampled runs match submitted iteration counts in §4."* |
| **AI sparse library build** | *"Artifact includes generated sparse library source + `smoke_test.sh` verifying Table 3 entry point; AE README documents build order."* |

### Predicted R3 attacks → defense snippets

| Attack | Defense snippet |
|--------|-----------------|
| **Template-free undefined early** | *"We agree. CR moves definition to §2.1 opening paragraph and replaces abstract uses with 'structure-search tuning' until defined."* |
| **§2 GPU expertise** | *"We will add a 5-line Hopper primer (TMA, warp specialization) before §2.3 and a notation table; §2.3 cross-refs glossary."* |
| **Abstract vs body scope** | *"We will revise abstract to: 'on NVIDIA H800, for shapes in Table 1, …' matching §4—removing 'production' unqualified."* |

### Rebuttal class routing (from paper-review skill)

| Class | CroqTile example |
|-------|------------------|
| **A** (factual error) | "No ablation" when §4.3 exists → pointer + CR caption fix |
| **B** (misunderstanding) | "No Triton comparison" when Table 4 has Triton → educate + bold CR pointer |
| **C** (valid, partial fix) | Missing error bars → add to CR if data exists; else median + run count in rebuttal |
| **D** (valid, not fixable) | Multi-GPU, full op coverage → acknowledge + future work; tighten claims |

**Strength target**: average ≥3.5/5 on P0 responses; decisive (5/5) responses cite `{§, Table, artifact path}` and offer exact CR wording.

### One-page skeleton (CroqTile)

```
Thanks to reviewers.

Eval fairness (R1): [fairness checklist pointer; 6-DSL parity; best-of-N disclosure §4.1]

Reproducibility (R2): [artifact contents; LLM manifest; log paths]

Clarity (R3): [template-free definition move; abstract scope fix]

We believe these address the main concerns and request reconsideration of [weak accept borderline].
```

Store expanded drafts in `plan/rebuttal/draft-responses.md` per paper-review skill.
