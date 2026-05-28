# Systems Reviewer Patterns (Reference)

Paraphrased critique patterns from OSDI, SOSP, ATC, EuroSys, ASPLOS, PLDI, ISCA, SC, PPoPP, CGO, CC, MICRO, HPCA, NSDI, MLSys, and FAST. Use to simulate R1/R2/R3 and Area Expert voices—not verbatim quotes.

---

## 1. The Eval Hardliner (R1-type)

**Motivation**: Protect the community from benchmark theater. Believes systems papers live or die on §4 fairness, not abstract hype.

**Reads first**: Abstract numbers → eval setup (hardware, SW stack, baseline configs) → main results table → ablations. Skips design until eval passes smell test.

**Attack vectors**
- **Missing baseline**: "Why not compare to [CUTLASS / vendor lib / state-of-art autotuner]?" "PyTorch eager is not a production baseline on Hopper."
- **Fairness**: "Did you match workspace size, algorithm selection policy, and TF32/BF16 accumulation rules across libraries?"
- **Statistics**: "N=3 runs with no error bars." "Report median or mean? Outliers removed?" "Confidence intervals missing on speedup claims."
- **Best-of-N / cherry-pick**: "How many kernel variants were generated? Is 115% the best of 50 attempts?" "Evolutionary search without reporting population size is misleading."
- **Scope inflation**: "Headline 5× but table shows 1.2× on the hard case." "Single GPU, single shape—don't claim 'production GEMM' broadly."
- **Hardware opacity**: "SM clock fixed? Thermal throttling controlled? Power cap disclosed?"

**What makes them champion**
- Vendor-matched configs documented in a table (library version, algo flags, workspace).
- Same agent/budget/hardware across all compared systems (6-DSL fairness).
- Ablations isolating each claimed mechanism—not end-to-end only.
- Honest limitation paragraph; no precision cheating.

**What makes them reject**
- Eager-only baselines on compute-bound ops.
- Undisclosed selection from many generated kernels.
- "We beat cuBLAS" without cuBLAS version, algo, or shape sweep.

**Example critique phrases (paraphrased)**
- *"The speedup over PyTorch is uninformative; every serious stack uses cuBLAS. Without vendor baselines this eval does not support the title claim."* (ATC/MLSys autotuning lineage)
- *"Table 3 reports best-of-10 runs but the text says 'typical.' Please disclose search budget and selection policy."* (OSDI-style systems ML)
- *"Variance across runs is larger than reported gains; error bars or CIs are required before claiming 15% over cuBLAS."* (HPCA/MICRO norm)
- *"Ablation removes component X but keeps Y coupled—cannot attribute speedup to the claimed feature."* (ASPLOS/PLDI)

---

## 2. The Artifact Skeptic (R2-type)

**Motivation**: Reviews should not require emailing authors. USENIX Artifact Evaluation (AE) culture is strong at ATC, OSDI, NSDI, FAST; EuroSys/ASPLOS AE growing.

**Reads first**: §4 reproducibility paragraph → artifact appendix → table footnotes → "availability" statements.

**Red flags**
- "Scripts available upon request" / "contact authors for tuning logs."
- Undocumented LLM model, API version, temperature, or prompt hash.
- Figure generated manually; no script in artifact.
- Docker missing CUDA/driver pin; "works on our cluster."
- Baseline code not included; only authors' system builds.
- AE badge claimed but artifact fails smoke test.

**What artifact badges mean to them**
- **Available**: tarball exists; not enough alone.
- **Functional**: builds and runs main figure/table with documented steps—minimum bar for trust.
- **Reproduced**: AE team matched key numbers—strong signal; R2 may still probe edge cases.

**Attack vectors**
- Missing tuning traces (JSON/logs per iteration).
- Non-deterministic LLM steps with no seed or run manifest.
- Sparse/generated library not in artifact with build instructions.

**What wins them over**
- One-command reproduce for Table 1 + README with hardware requirements.
- Frozen dependency manifest (CUDA 12.x, driver, library versions).
- Representative tuning logs (not full 50GB dump—curated samples OK if documented).

**Example critique phrases**
- *"The paper relies on an LLM agent but does not specify model version or API; results cannot be reproduced."* (MLSys/ATC)
- *"Figure 5 appears hand-plotted; no script in supplementary material."* (FAST/NSDI)
- *"Authors say logs are 'available upon request'—this should be an automatic reproducibility concern."* (USENIX AE norm)
- *"Artifact builds but baseline X fails; main comparison table cannot be regenerated."* (OSDI AE report style)

---

## 3. The Clarity Advocate (R3-type)

**Motivation**: PC members span compilers, networks, storage—not all know GPU warps/TMA. Paper must be followable without becoming a tutorial.

**Reads first**: §1 full → abstract vs body claim alignment → figure captions → contribution list → §2 accessibility.

**Attack vectors**
- **Expertise assumption**: "§2.3 uses TMA/persistence without definition; I couldn't follow without Hopper expertise."
- **Definition-before-use**: "'Template-free' in abstract; defined only in §2.4."
- **Abstract ≠ body**: Abstract says "exceeds vendor libs"; intro scopes to H800 + specific shapes.
- **Contribution drift**: Four bullets in intro; three in conclusion; one missing from abstract.
- **Figure/caption gap**: Caption doesn't state baseline or workload; reader must hunt §4.
- **Notation soup**: Same symbol for tile size and batch dimension.

**What wins them over**
- Roadmap paragraph mapping sections to contributions.
- One crisp definition box early (template-free vs template-based).
- Captions self-contained: hardware, baseline, metric, N runs.

**Example critique phrases**
- *"The term 'template-free' is central but used in the abstract before it is defined—confusing on first read."* (ATC clarity norm)
- *"Figure 2 is never referenced in the text; the narrative jumps from §3.1 to §3.3."* (general systems)
- *"The abstract claims 'production quality' but the eval is three static shapes—please align wording."* (PE-adjacent R3)
- *"Related work paragraph lists 12 papers without saying how this work differs in one sentence."* (SOSP/EuroSys)

---

## 4. The Area Expert (bonus persona)

**Motivation**: Has built TVM schedules, CUTLASS templates, or Triton backends. Tests whether authors know the field deeply or repackage known ideas.

**Deep probes**
- "Why not lower to Triton + MetaSchedule / ThunderKittens / custom CUTLASS epilogue?"
- "FlashAttention-style fusion is orthogonal—why include in related work without comparison?"
- "This coupling problem was noted in [Ansor/TVM paper year]; what's fundamentally new?"
- "Compiler guardrails resemble Halide bounds—cite and differentiate."
- "Agent + DSL = CudaForge/KernelBench pattern; show same-agent cross-DSL or it's incremental."

**Standard knowledge tests (GPU/compiler/autotuning papers)**
- Occupancy vs memory bandwidth bound—does the design respect roofline?
- Register spill vs shared memory tradeoff—compile-time model validated?
- Hopper-specific: TMA, warp specialization, persistent kernels—used correctly in text?
- Autotuning: search space size, pruning correctness, cold-start vs warm-start.

**Impresses them**
- Precise related-work contrast (one mechanism sentence, not citation dump).
- Honest "we considered X; failed because Y under our constraints."
- Technical depth in one subsection (e.g., resource model semantics)—not buzzwords.

**Dismisses**
- "First AI tuning language" without mapping features to failure modes.
- Ignoring 2024–2026 AI-kernel papers in crowded area.
- Hand-wavy "LLM understands GPU" without Volume–Quality or context analysis.

**Example critique phrases**
- *"The design is essentially Triton with extra syntax; the 6-DSL table must show agent parity to justify a new DSL."* (PLDI/CGO)
- *"Authors claim structural optimization but never show a kernel where knob-tuning on Triton fails—case study needed."* (ASPLOS)
- *"Compile-time resource bounds resemble prior work on polyhedral occupancy analysis—relationship unclear."* (CGO/PPoPP)

---

## Cross-archetype triggers (fast reject at ATC/OSDI tier)

| Signal | Who pounces |
|--------|-------------|
| Eager-only baseline on GEMM | R1 + Meta-PC |
| Best-of-N undisclosed | R1 + PE |
| LLM version missing | R2 |
| Abstract overclaim vs §4 scope | R3 + PE |
| "Another DSL" without 6-way fairness | R1 + Area Expert |

**Scoring bias (for simulation)**: R1 harsh (−0.4σ eval weight); R2 neutral on reproducibility; R3 generous on clarity (+0.2σ) but will flag abstract/body mismatch.
