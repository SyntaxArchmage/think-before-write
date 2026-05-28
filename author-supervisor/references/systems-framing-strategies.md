# Systems Framing Strategies (Reference)

How award-winning and memorable systems papers position contributions — narrative patterns from OSDI, SOSP, ATC, EuroSys, ASPLOS, PLDI, ISCA, SC, PPoPP, CGO, MICRO, HPCA, MLSys, FAST. Examples paraphrased from FlashAttention, vLLM, DLRM, Halide, TVM, Triton, Megatron, XLA, and autotuning/compiler lineages.

---

## 1. Contribution Framing Archetypes

### 1.1 "The field assumed X; we show not-X" (paradigm challenge)
- **Structure**: *Conventional wisdom: [X]* → *Counterexample or measurement* → *New model* → *System built on new model*
- **Examples**: FlashAttention lineage — assumed attention must materialize full N×N; show IO-aware tiling makes memory the bottleneck, not FLOPs. vLLM — assumed higher batch always helps; show KV-cache paging changes the batching tradeoff.
- **Risk**: Must prove X was widely believed (cite + production pain), not a straw belief.
- **Best venues**: OSDI, SOSP, MLSys (when production-grounded).

### 1.2 "Everyone optimizes [knob]; we optimize [structure]" (new optimization axis)
- **Structure**: *Prior work tunes [loops/tiles/batch]* → *We expose [layout/fusion boundary/search space class] as first-class*
- **Examples**: Halide — separate algorithm from schedule. TVM/Ansor — search over program structure, not only flags. CroqTile-style — tile/layout as IR object, not backend detail.
- **Soundbite**: *"Not a faster kernel—a different thing to optimize."*
- **Best venues**: PLDI, ASPLOS, CGO, PPoPP.

### 1.3 "N systems tried [approach]; we tried [different approach] and it works" (controlled experiment)
- **Structure**: *Hypothesis: [approach B] beats [approach A] for [class] because [mechanism]* → *Same workloads, same budget* → *Measured outcome*
- **Examples**: MetaSchedule vs hand schedules; Triton vs CUDA for fusion-friendly ops; template-free LLM codegen vs template libraries (when fairly scoped).
- **Key**: Frame as **experiment design**, not "we are smarter." Match budgets.
- **Best venues**: ATC, EuroSys, HPCA, MICRO.

### 1.4 "Looks like [known problem] but requires [novel technique]" (reduction + innovation)
- **Structure**: *Problem P resembles [GEMM/scheduling/memory allocation]* → *Constraint C breaks standard tools* → *Technique T (often combine known pieces unusually)*
- **Examples**: Distributed attention ↔ collective scheduling with sequence parallelism; sparse GEMM ↔ load balancing unlike dense GEMM.
- **Why it works**: Reviewers get footing fast, then see novelty in the twist.
- **Best venues**: ISCA, SC, ASPLOS.

---

## 2. Abstract Landing Strategies

### 2.1 Numbers-first ("X achieves 2.1× over Y on Z")
- **Template**: *[Headline metric + speedup]* → *[System name + one-line mechanism]* → *[Scope: workload, hardware]* → *[Secondary claim: memory, tuning cost]*
- **Example (FlashAttention-style)**: *Our IO-aware attention runs 2–4× faster than standard attention on long sequences, using 5–20× less HBM traffic, with exact numerics on A100/H100.*
- **When**: Strong, reproducible kernel wins; PC skims abstract only.
- **Caution**: Scope in sentence two — avoid abstract oversell (reviewer R3 attack).

### 2.2 Insight-first ("We observe that [surprising finding]")
- **Template**: *We observe [fact]* → *Therefore [design implication]* → *[System]* → *[Eval summary]*
- **Example (DLRM/recommendation-style)**: *We observe that embedding lookups dominate datacenter inference time despite small compute; therefore we co-design cache hierarchy with embedding access patterns…*
- **When**: Contribution is **measurement + redesign**, not raw speedup.
- **Best for**: OSDI, SOSP, MLSys production papers.

### 2.3 Problem-first ("Production systems face [concrete pain]")
- **Template**: *[User/production pain with noun phrases]* → *[Gap in current stacks]* → *[Our approach]* → *[Outcome]*
- **Example (vLLM-style)**: *LLM serving wastes GPU memory on fragmented KV caches, capping batch size and throughput. We introduce paged attention and a lightweight scheduler…*
- **When**: Deployability and pain point are the sell; numbers support, not lead.
- **Best for**: ATC, MLSys, EuroSys.

**Pick one lead**; do not stack all three in four sentences.

---

## 3. Title Patterns That Work

### 3.1 Descriptive: `[SystemName]: [What It Does for What]`
- *FlashAttention: Fast and Memory-Efficient Exact Attention*
- *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*
- **Pros**: Searchable, clear for citations. **Cons**: Less memorable alone.

### 3.2 Provocative: `[Surprising Claim] via [Mechanism]`
- *Efficient Memory Management for LLM Serving with PagedAttention* (mechanism in subtitle)
- *Ansor: Generating High-Performance Tensor Programs by Hierarchical Search*
- **Pros**: Sticky for PC discussion. **Cons**: Must deliver in eval or backlash.

### 3.3 Problem-named: `[Problem]: [How We Solve It]`
- *Optimizing FPGA-based Accelerator Design for Deep Convolutional Neural Networks*
- **Pros**: Readers know relevance immediately. **Cons**: Can sound incremental if problem is too narrow.

**Heuristics**: System name + colon + mechanism is ATC/MLSys default; provocative subtitle needs eval headline to match.

---

## 4. Competition Framing in Related Work

### 4.1 Taxonomy table (rows = systems, columns = properties)
| System | Auto schedule | Hardware-specific IR | End-to-end DL | Tuning budget aware |
|--------|---------------|----------------------|---------------|---------------------|
| Halide | partial | CPU/GPU generic | no | no |
| TVM/Ansor | yes | multi-target | yes | partial |
| Ours | yes | tile-aware | yes | yes |

- Place after 2–3 prose paragraphs; footnote versions.
- **Tone**: Factual checkmarks — let gaps speak.

### 4.2 Closest competitor deep dive
- **Template**: *Closest to our work is [X].* → *Shared: [goal].* → *Differs: [representation / search / deployment].* → *We do not claim [their strength]; we win on [our axis].*
- **Example**: *Closest is MetaSchedule; both autotune tensor IR. MetaSchedule searches generic loop nests; we search in a hardware-tiled space with buffer provenance—needed when scratchpad capacity is shape-dependent.*
- One paragraph only; rest stays categorical.

### 4.3 "Generous but devastating" comparison tone
- **Generous**: Acknowledge what competitor does well — *CUTLASS remains the gold standard for hand-tuned GEMM on NVIDIA.*
- **Devastating**: Pivot to axis they cannot address — *…but does not automate fusion across epilogues or adapt to new DSL frontends without rewrite.*
- **Avoid**: Sneering (*"naive"*, *"obviously flawed"*). Let structured gaps carry weight.
- **P4 signature**: Closest competitor paragraph + taxonomy table = positioning without looking defensive.

---

## 5. Limitation as Strength Framing

### 5.1 Deliberate scope with principled reason
- *We deliberately scope to [static graphs / single GPU / FP16-BF16] because [isolates mechanism M / matches deployment class D].*
- **Example**: *We evaluate single-GPU decode to isolate KV-cache management from network collectives.*

### 5.2 Single-GPU / single-node isolates the variable
- **Template**: *Multi-GPU scaling is orthogonal: our [scheduler/IR] composes with [Megatron/DeepSpeed-style sharding] without changing [core claim].*
- Shows awareness without doing everyone's eval.

### 5.3 Limitation is composable
- *Our pass runs before vendor BLAS selection; it does not replace cuBLAS but reduces the search space BLAS sees.*
- *PagedAttention integrates with existing CUDA graphs; continuous batching is future work.*
- Turns "we didn't do X" into "X plugs in later."

### 5.4 Anti-patterns
| Weak | Strong |
|---|---|
| "Due to space constraints…" (only) | Space + *full results in artifact §N* |
| Hidden in conclusion | Limitation paragraph in eval or discussion |
| Apologize repeatedly | One scoped paragraph + composability forward |

---

## 6. Cross-Section Alignment Checklist

- [ ] Title mechanism appears in abstract sentence 2–3
- [ ] Intro contribution bullets map to eval subsections (RQ or dimension)
- [ ] Closest-competitor paragraph matches taxonomy table
- [ ] Headline number in abstract matches eval setup scope (hardware, baseline)
- [ ] Limitation paragraph states what you **do** claim within scope
- [ ] Framing archetype consistent: don't insight-first in abstract and numbers-first in intro

---

## Usage Notes

- Invoke with **P4 (Strategy Advisor)** for positioning passes and **P1 (Systems Veteran)** for significance tier.
- Pair with `systems-writing-patterns.md` (intro/related work templates) and `systems-eval-methodology.md` (fairness backs framing claims).
- For CroqTile: prefer **new optimization axis** + **controlled experiment** archetypes; lead abstract with scoped headline number and tuning-cost secondary claim.
