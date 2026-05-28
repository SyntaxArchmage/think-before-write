# Systems Writing Patterns (Paragraph-Level)

Reference patterns from top-tier systems, compiler, and HPC venues: OSDI, SOSP, ATC, EuroSys, ASPLOS, PLDI, ISCA, SC, PPoPP, CGO, CC, MICRO, HPCA, NSDI, SIGCOMM, MLSys, FAST.

Examples are paraphrased from papers in the Halide/TVM/Triton/MLIR/XLA/FlashAttention/vLLM/Megatron/DeepSpeed/CUTLASS lineage.

---

## 1. Introduction Patterns

### 1.1 "Field is hot but broken" opener
- **Where**: Intro ¶1–2
- **Template**: [Trend/adoption] → [Why current practice fails at scale] → [Concrete pain point with workload/hardware anchor]
- **Example**: *Deep learning frameworks now target dozens of accelerators, yet operators are still hand-tuned per chip. A single matmul shape change can erase weeks of kernel work; production stacks therefore ship conservative defaults that leave 2–3× on the table on modern GPUs.*
- **Why it works**: Establishes urgency without hype; grounds abstraction in operator-level cost.

### 1.2 "N papers but none do X" gap statement
- **Where**: Intro ¶2–3 (after problem)
- **Template**: [Prior line A] + [Prior line B] → [Shared limitation] → [Missing capability X tied to your thesis]
- **Example**: *Auto-schedulers (TVM, Ansor) and template libraries (CUTLASS) both improve GEMM performance, but neither exposes a stable IR for fusing attention with surrounding epilogues; practitioners still rewrite kernels when the model graph changes.*
- **Why it works**: Shows literature fluency; gap is specific and falsifiable.

### 1.3 "We observe that" insight
- **Where**: Intro ¶3 or early design bridge
- **Template**: *We observe that [counterintuitive fact]* → [Mechanism in one clause]* → [Implication for design]*
- **Example**: *We observe that most LLM inference time is not FLOPs but memory bandwidth on KV-cache reads; batching increases throughput only when block tables stay contiguous in physical memory.*
- **Why it works**: Converts benchmark intuition into a design driver (vLLM/FlashAttention style).

### 1.4 Contribution paragraph
- **Where**: Intro final ¶ before roadmap
- **Template**: *This paper presents [System].* → [Design artifact 1–3, each verb-led] → [Headline eval number with scope]*
- **Example**: *This paper presents CroqTile, a GPU kernel programming language designed for AI-driven tuning on NVIDIA Hopper (H800). We formulate tile layouts as first-class IR objects with compile-time safety invariants, enabling an unmodified LLM agent to search kernel structure—not just parameters. In a six-DSL comparison using the same agent and hardware budget, only CroqTile-generated kernels exceed vendor libraries: 115% cuBLAS on dense GEMM, 155% on blockscale, and 120% cuSPARSELt on structured-sparse ops.*
- **Why it works**: Mirrors abstract claims; each bullet maps to a section.

---

## 2. Design / Methodology Patterns

### 2.1 Strawman then real solution
- **Where**: Design § opening subsections
- **Template**: *A naive approach [X] fails because [reason].* → *Instead, [System] [mechanism].*
- **Example**: *A naive autotuner that enumerates all tile sizes explodes search space on irregular head dimensions. Instead, CroqTile prunes candidates using memory-hierarchy bounds before micro-benchmarking.*
- **Why it works**: Justifies complexity; reviewers see you considered simpler paths.

### 2.2 Design principle framing
- **Where**: Design overview (Halide/TVM style)
- **Template**: *Our design follows [N] principles: (P1) … (P2) …* → each principle gets one mechanism sentence
- **Example**: *We separate **what** (tensor semantics) from **how** (mapping to warps). This separation lets the same schedule compile to CUDA, ROCm, or a DSL backend without rewriting algorithm code.*
- **Why it works**: Gives reviewers a checklist to evaluate coherence.

### 2.3 Alternative rejected
- **Where**: Design subsubsections, appendix pointers OK
- **Template**: *We considered [Alt]. It [almost works] but [fatal flaw under our constraints].*
- **Example**: *We considered lowering directly to PTX. PTX is expressive, but Hopper SM90a scratchpad rules are not visible at that level, so illegal spills appear only after costly register allocation.*
- **Why it works**: Preempts "why not X?" without a related-work detour.

### 2.4 Invariant / property statement
- **Where**: Formal design, correctness, or scheduler sections (PLDI/ASPLOS tone)
- **Template**: *Invariant I:* [predicate]. *Maintaining I ensures [safety/performance property].*
- **Example**: *Tile invariant: no two warps concurrently write the same output tile without a reduction phase. Violating this invariant causes silent races on fused bias-add epilogues.*
- **Why it works**: Makes implicit compiler reasoning auditable.

---

## 3. Evaluation Patterns

### 3.1 Setup then headline opener
- **Where**: Eval § first paragraph
- **Template**: [Hardware, SW stack, workloads, baselines] → [One-sentence headline result with metric + scope]
- **Example**: *We evaluate on an H100 server (CUDA 12.4, PyTorch 2.3) using LLaMA-2-7B/13B decode and prefill traces. CroqTile improves median decode latency by 1.8× over the vendor library at batch 32 without changing numerics.*
- **Why it works**: Reviewers know fairness context before trusting numbers.

### 3.2 Table walk paragraph
- **Where**: After Table/Figure reference
- **Template**: *Table N shows [axis].* → [Best case] → [Worst case / outlier] → [Takeaway tied to design]*
- **Example**: *Table 2 sweeps head dimension and sequence length. Gains peak at long context (≥8k) where fused attention cuts HBM traffic; at short seq, overhead from metadata sorting limits speedup to 12%.*
- **Why it works**: Interprets data; avoids "see table."

### 3.3 Ablation interpretation
- **Where**: Eval ablation subsection
- **Template**: *Removing [component] costs [Δ] because [mechanism], confirming [hypothesis].*
- **Example**: *Disabling the layout cache regresses cold-start latency by 6×, confirming that search reuse—not micro-kernel quality alone—dominates operator bring-up time.*
- **Why it works**: Links knob to claim; distinguishes necessary vs. ornamental parts.

### 3.4 Fairness disclosure
- **Where**: Eval setup or baseline subsection
- **Template**: *We give [baseline] [same IR / same autotune budget / same precision].* → *Where asymmetry remains, we state it.*
- **Example**: *TVM baselines use Ansor with a 2-hour tuning budget per shape, matching our search cap; vendor BLAS receives shape-specific heuristics shipped in cuBLAS 12.4.*
- **Why it works**: Defuses R1 eval attacks before they form.

### 3.5 Limitation acknowledgment
- **Where**: Eval end or Discussion
- **Template**: *We do not claim [X].* → [Scope boundary] → [Why orthogonal or future work]*
- **Example**: *We do not evaluate training at ZeRO-3 scale; our scheduler assumes static graphs. Extending to dynamic control flow is orthogonal to tile selection.*
- **Why it works**: Signals maturity; reduces over-claim suspicion.

---

## 4. Related Work Patterns

### 4.1 Category + gap
- **Where**: Related work § (2–4 thematic paragraphs)
- **Template**: **[Category]**: [Representative works] [what they optimize]. *[Gap relative to your axis].*
- **Example**: **DSL schedulers** (Halide, Tiramisu) decouple algorithm from schedule but target CPU/GPU generically; they do not encode Hopper SM90a-specific tile constraints, leaving performance on NVIDIA Hopper GPUs unpredictable.*
- **Why it works**: Organizes citations by axis, not chronology.

### 4.2 Closest competitor deep dive
- **Where**: Related work (1 dedicated paragraph)
- **Template**: *Closest to our work is [X].* → [Shared goal] → [Key difference in representation/search/deployment]*
- **Example**: *Closest to our work is TVM's MetaSchedule: both autotune tensor programs. MetaSchedule searches over a generic loop nest; CroqTile searches in a hardware-tiled space with provenance tracked to physical buffers, which is necessary when scratchpad capacity is shape-dependent.*
- **Why it works**: Shows intellectual honesty; clarifies novelty boundary.

### 4.3 Positioning claim
- **Where**: Related work closing or intro cross-ref
- **Template**: *Unlike [A,B], [ours] is the first to [qualified claim] under [assumption].*
- **Example**: *Unlike FlashAttention-2 and xFormers, which hand-fuse attention for NVIDIA GPUs, our compiler pass automates fusion for any op sequence expressible in our IR—at the cost of longer compile time.*
- **Why it works**: Positions without dismissing prior art.

---

## 5. Conclusion Patterns

### 5.1 Contribution recap without copy-paste
- **Where**: Conclusion ¶1
- **Template**: Restate problem → mechanism in new words → outcome (not bullet-for-bullet from intro)
- **Example**: *Operator performance on specialized AI accelerators remains brittle because tuning knowledge is tied to shapes, not semantics. By compiling tiles as first-class IR objects, CroqTile turns bring-up from a kernel rewrite into a reusable search artifact—recovering most of hand-tuned performance automatically.*
- **Why it works**: Feels fresh; tests whether the narrative coheres.

### 5.2 Broader implication
- **Where**: Conclusion final ¶
- **Template**: *More broadly, [lesson for field].* → [One concrete future direction]*
- **Example**: *More broadly, treating memory layout as a schedulable dimension—not a backend detail—may unify autotuning across GEMM, attention, and collectives. We plan to integrate dynamic shapes and multi-node sharding in future work.*
- **Why it works**: Elevates paper beyond one system; avoids empty "exciting future."

---

## Usage Notes

- Match pattern to **subsection job**: intro sells gap; design sells mechanism; eval sells evidence; related work sells boundary; conclusion sells memory.
- Pair every headline number with **workload + hardware + baseline** in the same section.
- Prefer **one insight paragraph** over three adjectives in intros (MLSys/ATC norm).
