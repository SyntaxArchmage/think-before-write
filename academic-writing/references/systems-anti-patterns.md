# Systems Writing Anti-Patterns

Common mistakes flagged in OSDI, SOSP, ATC, EuroSys, ASPLOS, PLDI, ISCA, SC, PPoPP, CGO, CC, MICRO, HPCA, NSDI, SIGCOMM, MLSys, FAST reviews. Each entry: symptom → harm → fix → who catches it.

Reviewer shorthand: **R1** eval/methodology, **R2** novelty/related work, **R3** clarity/writing, **R4** expert domain (architecture/compilers), **PE** meta-review.

---

## 1. Evaluation Anti-Patterns

| Anti-pattern | Looks like | Why bad | Do instead | Catcher |
|--------------|------------|---------|------------|---------|
| PyTorch-only baseline | *We beat `torch.matmul`.* | Ignores vendor BLAS, cuDNN, Triton, CUTLASS | Compare to strongest applicable stack; disclose tuning budget | **R1**, **R4** |
| Missing vendor comparison | Custom kernel vs. naive reference | Speedup is uninterpretable | Include vendor library or SOTA open kernel (FlashAttention, vLLM PagedAttention baselines) | **R1** |
| Cherry-picked shapes | Best point on one `(M,N,K)` | May not generalize | Sweep shapes; report geo-mean + worst case | **R1**, **PE** |
| Unreported variance | Single run bar charts | Noise may dominate | Multiple runs; p50/p95 or CI; warm-up policy stated | **R1** |
| Apples-to-oranges | Different precision, fusion, or batch | Inflates gains | Match numerics, fusion level, batch, clock caps | **R1**, **R4** |
| "5× faster" without what | Headline factor, no metric | Ambiguous (latency? throughput? compile time?) | *5× lower p50 decode latency at batch 32 on H100* | **R3**, **PE** |

---

## 2. Introduction Anti-Patterns

| Anti-pattern | Looks like | Why bad | Do instead | Catcher |
|--------------|------------|---------|------------|---------|
| Feature laundry list | *We support A, B, C, D, E…* | No problem story | Problem → insight → 3 contributions max | **R3**, **PE** |
| Undefined terms early | *tile*, *fragment*, *pass* before definition | Reader lost | Define on first use or defer to §3 with forward ref | **R3** |
| Contribution ≠ abstract | Intro bullets disagree with abstract | Trust collapse | Single source of truth; diff check before submit | **PE** |
| "The first" unqualified | *First attention optimizer* | Easy to falsify | Scope: platform, assumption, artifact type | **R2** |
| "Rapid progress" filler | *ML has seen rapid progress…* | Zero information | Delete; start with concrete bottleneck | **R3** |

---

## 3. Design Anti-Patterns

| Anti-pattern | Looks like | Why bad | Do instead | Catcher |
|--------------|------------|---------|------------|---------|
| Implementation detail dump | 2 pages of API listings | Hides ideas | One overview figure; details in appendix | **R3**, **R4** |
| Missing design rationale | *We use a hash map here.* | Arbitrary choices | *We use X because Y under constraint Z* | **R4** |
| "We do X" without because | Sequential mechanism list | Reads like changelog | Strawman → principle → mechanism | **R4** |
| Hand-wavy mechanism | *The scheduler is smart.* | Not reproducible | Name inputs/outputs, invariants, complexity | **R4**, **R1** |

---

## 4. Related Work Anti-Patterns

| Anti-pattern | Looks like | Why bad | Do instead | Catcher |
|--------------|------------|---------|------------|---------|
| Tour without positioning | 30 citations, no gaps | Related work as bibliography | Category + gap per paragraph | **R2** |
| "X did Y" only | *TVM autotunes loops.* | No contrast | *TVM autotunes loops; we differ in [axis]* | **R2** |
| Missing closest competitor | Omits TVM/Megatron/FlashAttention-class work | Novelty doubt | Dedicated paragraph on nearest system | **R2**, **PE** |
| Strawman prior art | *All prior work is slow.* | Angers experts | Fair summary, then precise delta | **R2**, **R4** |

---

## 5. Language Anti-Patterns (LLM Tells)

| Phrase/habit | Looks like | Why bad | Do instead | Catcher |
|--------------|------------|---------|------------|---------|
| "It is worth noting" | Filler hedge | Adds no content | Delete or state fact directly | **R3** |
| "In the realm of" | Generic flourish | Non-systems tone | *In [specific subsystem/workload]* | **R3** |
| "Leverage" | *Leverage MLIR* | Buzzword | *use*, *build on*, *lower through* | **R3** |
| "Delve" / "comprehensive" | Marketing adjectives | Smells generated | Concrete scope: *eight layers, three GPUs* | **R3**, **PE** |
| "Novel approach" | Self-labeling novelty | Show, don't tell | State mechanism + eval | **R2**, **R3** |
| Three-part list addiction | Every paragraph ends 1-2-3 | Mechanical rhythm | Vary paragraph goals and length | **R3** |
| Uniform paragraph length | All ¶ ≈ 4 sentences | Monotonous | Short punchy insight ¶ + longer eval walk | **R3** |

---

## 6. Cross-Cutting Reviewer Triggers

| Trigger | Example | Fix |
|---------|---------|-----|
| Over-claim in title | *Optimal* without proof | *Automatic*, *Scalable*, *Tile-Aware* |
| Missing threat to validity | No eval limitations paragraph | Add scoped limitation + orthogonality |
| Orphan figures | Figure not referenced in text | Every figure: lead-in + interpretation |
| Baseline tuning asymmetry | 2h autotune for you, default for them | Equal budget or justify asymmetry |

---

## Quick Self-Audit (pre-submit)

1. Every speedup names **metric, workload, hardware, baseline**.
2. Intro contributions match abstract and §6 recap (wording may differ).
3. Related work names **closest competitor** and **gap axis**.
4. Search draft for: *leverage, delve, comprehensive, novel approach, worth noting*.
5. At least one **limitation** stated where R1 will look (eval or discussion).

---

## Subfield Notes

- **MLSys/ATC**: R1 asks training vs. inference scope; state both or exclude explicitly.
- **PLDI/CGO**: R4 wants semantics/preservation sketched, not only speedups.
- **ISCA/MICRO/HPCA**: Tie mechanism to microarch constraint (bandwidth, occupancy, SRAM).
- **OSDI/SOSP**: R1+R2 expect realistic deployment story, not microbench-only.
