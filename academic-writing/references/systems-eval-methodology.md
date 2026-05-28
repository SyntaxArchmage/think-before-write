# Systems Evaluation Methodology (Reference)

Patterns from top-tier GPU, compiler, autotuning, and ML-systems papers: OSDI, SOSP, ATC, EuroSys, ASPLOS, PLDI, ISCA, SC, PPoPP, CGO, MICRO, HPCA, MLSys, FAST. Examples paraphrased from FlashAttention, vLLM, TVM/Ansor, Triton, CUTLASS, XLA, Megatron, DeepSpeed, Halide, and vendor-library comparison lineages.

---

## 1. Evaluation Section Structure

### 1.1 Setup paragraph (mandatory opener)
- **Template**: [Hardware + driver/CUDA] → [Software stack + versions] → [Workloads / benchmarks] → [Baselines named with versions] → [Headline result in one sentence]
- **Example**: *All experiments run on an H100 SXM5 (CUDA 12.4, driver 550.x) with PyTorch 2.3. We evaluate LLaMA-2 decode/prefill traces and MLPerf-style GEMM sweeps against cuBLAS 12.4, Triton 3.0 autotune, and Ansor (2 h/shape). Our scheduler improves median decode latency by 1.8× at batch 32 without changing numerics.*
- **Why**: Reviewers anchor fairness before trusting tables.

### 1.2 Research questions → experiments → answers
- **Template**: *We ask: (RQ1) … (RQ2) …* → subsection per RQ → closing sentence per subsection answers the RQ with a number
- **Example (MLSys/ATC autotuner)**: RQ1: Does search reuse dominate cold-start? RQ2: Does tile-aware pruning preserve quality? RQ3: How does end-to-end inference compare to vendor stacks?
- **Why**: Converts eval from "many plots" into falsifiable claims.

### 1.3 "We evaluate along N dimensions"
- **Common axes**: end-to-end throughput/latency; kernel microbenchmarks; search/tuning cost; memory footprint; scaling (batch, seq, GPUs); ablation of design components; sensitivity to hyperparameters
- **Template**: *We evaluate CroqTile along four dimensions: (1) operator performance, (2) tuning time, (3) end-to-end inference, and (4) ablations isolating each mechanism.*
- **Example (CroqTile)**: *All experiments run on NVIDIA H800 PCIe (SM90a, CUDA 12.8). Six DSLs share the same agent harness and tuning budget against cuBLAS and cuSPARSELt. Headline results: 115–117% cuBLAS on dense GEMM, 155% on blockscale, and 120% cuSPARSELt on structured-sparse ops.*
- **Why**: Gives reviewers a checklist; maps to contribution bullets.

### 1.4 Subsections vs one long section
| Use subsections when | Keep one section when |
|---|---|
| ≥3 distinct RQs or axes | Single kernel family + one baseline sweep |
| Ablations + sensitivity + case study each need depth | Short ATC tool paper (<6 pages eval) |
| Different baselines per axis (vendor vs academic) | All experiments share identical setup table |
| End-to-end and microbench would confuse if interleaved | Microbench only; no deployment story |

**Rule of thumb**: If a reviewer could ask "where is X evaluated?" — X gets a `\subsection`.

---

## 2. Baseline Selection Patterns

### 2.1 Vendor library baselines (required for compute-bound GPU work)
- **Examples**: cuBLAS/cuDNN (GEMM/conv), cuFFT, NCCL (collectives), vendor attention (cuDNN SDPA, FlashAttention as shipped baseline when comparing systems)
- **Template**: *We compare against cuBLAS [version] with default heuristics and, where applicable, `cublasLt` algorithm selection after [N] warmup picks.*
- **Trap**: PyTorch `matmul` or eager op without naming backend — treated as straw man at OSDI/MLSys.

### 2.2 State-of-the-art academic baselines
- **Compiler/autotune**: TVM + Ansor/MetaSchedule, Halide auto-scheduler, Triton autotune, OpenTuner, AutoTVM
- **ML systems**: xFormers, FasterTransformer, DeepSpeed-Inference, TensorRT-LLM (when claiming production inference)
- **Template**: *Ansor receives the same 2-hour tuning budget and search space class (loop tiling, vectorization) as our system.*
- **Why**: Shows you beat the best published approach, not only vendor defaults.

### 2.3 Same framework, different config (ablation baselines)
- **Pattern**: Your system with component X disabled; default config vs tuned config; greedy search vs full search
- **Example**: *CroqTile w/o layout cache*; *Triton with default tile sizes vs autotuned*
- **Why**: Isolates mechanism without conflating "different codebase" fairness issues.

### 2.4 Straw man baseline problem
| Straw man | Strong baseline |
|---|---|
| Unoptimized PyTorch eager on Hopper GEMM | cuBLAS + shape-specific heuristics |
| Single-thread CPU | MKL/oneDNN with AVX-512 |
| TVM with 5-minute tune vs your 24-hour tune | Matched GPU-hours or iterations |
| Old library version | Current release at submission time |

**Disclosure sentence**: *We include [weak baseline] only to show the gap practitioners see before tuning; headline claims use [strong baseline].*

---

## 3. Fairness Disclosure Patterns

### 3.1 Hardware and software config
- *All experiments run on [GPU model, memory, TDP/power cap if fixed] with CUDA [X], driver [Y], and [framework versions].*
- For multi-GPU: topology (NVLink vs PCIe), NCCL version, bucket sizes.

### 3.2 Tuning budget
- *Each autotuner is given [N] trials / [T] GPU-hours per shape / same population size for evolutionary search.*
- *Vendor libraries use default heuristics; we do not hand-pick cuBLAS algorithms per shape unless noted.*

### 3.3 Warm-up and measurement
- *We discard the first [W] runs, then report median of [K] timed iterations.*
- For JIT/autotune: separate **search time** from **steady-state kernel time** in tables.

### 3.4 Best-of-N disclosure
- Required when reporting best kernel from search: *Table X reports the best configuration found in [N] candidates; Figure Y shows the full distribution.*
- **OSDI/ASPLOS norm**: hiding search pool size is a common reject reason.

---

## 4. Number Presentation Patterns

### 4.1 Speedup vs absolute vs % of vendor
| Metric | When to use |
|---|---|
| **Speedup vs baseline** | Clear win story; autotuning papers (PPoPP/CGO) |
| **Absolute (TFLOPS, GB/s, tok/s)** | Roofline-bound kernels; avoids "2× of slow" |
| **% of vendor peak or cuBLAS** | Honest when not beating vendor — "91% of cuBLAS with 40× less tuning" |
| **Latency (ms, p99)** | Inference/serving (MLSys, vLLM lineage) |

**Practice**: Lead with the metric your claim uses; put the other in the same paragraph or caption.

### 4.2 Geomean vs arithmetic mean vs per-workload
- **Geomean speedup**: standard for multi-workload compiler papers (avoid one huge outlier dominating); state explicitly
- **Arithmetic mean**: acceptable for absolute throughput across homogeneous benchmarks
- **Per-workload tables**: mandatory when variance across workloads is high — geomean alone hides losses
- **Template**: *Gmean speedup is 1.6×; per-kernel results in Table 2 show regressions on small M/N due to launch overhead.*

### 4.3 Table vs bar chart vs roofline
```
Many baselines × many workloads     → table (+ optional bar for headline subset)
Single metric across sweep param    → line chart (seq len, batch, tile size)
Compute vs memory bound diagnosis   → roofline (ISCA/MICRO/CGO)
End-to-end stacked breakdown        → stacked bar or waterfall (MLSys inference)
Search cost vs quality              → scatter or Pareto frontier (autotuning)
```
Captions must state: hardware, baseline, metric, aggregation (median/gmean), N runs.

### 4.4 Presenting wins AND losses honestly
- Report worst case in text: *Speedups range from 0.92× to 2.4×; losses occur when M < 128 due to …*
- Use **cumulative distribution** of speedups across shapes (Ansor/TVM papers)
- Never footnote the only negative result — reviewers hunt for it

---

## 5. Ablation Study Patterns

### 5.1 Component removal (w/o X)
- **Template**: *w/o [component]* → *Δ metric* → *because [mechanism linked to design §]*
- **Example**: *Disabling the layout cache regresses cold-start by 6×, confirming reuse dominates bring-up—not micro-kernel quality alone.*

### 5.2 Parameter sensitivity
- Sweep one knob at a time: tile size, search depth, beam width, cache TTL
- **Template**: *Figure N varies [param] from [a] to [b]. Performance is flat in [range], degrading sharply when [threshold] because [reason].*

### 5.3 Mechanism links (non-negotiable)
Each ablation must answer: **which claim in §3 does this support?**
| Bad | Good |
|---|---|
| "Ablation shows cache helps" | "w/o cache: +6× cold-start (C3: search reuse); kernel GFLOPS unchanged (isolates C3 from C1)" |
| Remove two components at once | One component per row in ablation table |

### 5.4 Common mistakes
- Ablation only at one shape — sweep at least two regimes (compute-bound + memory-bound)
- No absolute numbers — always give Δ (ms, ×, GB/s)
- "Full system vs random" without intermediate steps — add staged ablations

---

## 6. Statistical Rigor in Systems Papers

### 6.1 When variance matters vs single-run
| Single-run often OK | Variance / CI expected |
|---|---|
| Deterministic GPU kernels after warm-up, fixed clocks | OS noise, shared clusters, network I/O |
| Large effect size (2×+) with stable timers | Claims within 5–15% of cuBLAS |
| Microbench with CUDA events, many inner iterations | End-to-end serving p99 latency |
| Synthesis / analytical results | LLM-agent or sampling-based search |

### 6.2 Confidence intervals on throughput
- Report **95% CI** or **IQR** on tok/s, ms/op, or GFLOPS when comparing within 20%
- **Template**: *Error bars show 95% CI over 10 runs after 100 warm-up iterations.*
- SC/HPCA/MICRO: fixed GPU clocks + disclose if not

### 6.3 p-values in systems (rare but sometimes)
- **Rare**: kernel microbenchmarks with many repeats — Mann-Whitney or bootstrap if claiming statistical significance
- **More common**: effect size + CI instead of p-hacking small N
- **When p-values appear**: A/B in production traces (OSDI/FAST), user study latency — not typical for GPU kernel papers

### 6.4 Checklist before submission
- [ ] Vendor + SOTA academic baselines named with versions
- [ ] Tuning budget matched or asymmetry stated
- [ ] Median/gmean and N runs disclosed
- [ ] Losses and outliers discussed in prose
- [ ] Each ablation row ties to a contribution claim
- [ ] Captions self-contained for R3 skimming

---

## Usage Notes

- Pair with `systems-writing-patterns.md` §3 for paragraph templates and `systems-reviewer-patterns.md` §1 for eval hardliner attacks.
- For CroqTile-style papers: foreground **6-DSL fairness**, **search budget**, and **mechanism-linked ablations** in setup paragraph one.
