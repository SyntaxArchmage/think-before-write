# Systems Sentence Bank (Structural Templates)

Reusable **structures** for OSDI/SOSP/ATC/EuroSys/ASPLOS/PLDI/ISCA/SC/PPoPP/CGO/CC/MICRO/HPCA/NSDI/SIGCOMM/MLSys/FAST papers. Fill bracketed slots; do not copy verbatim from published text.

---

## 1. Claiming Novelty

### Hedged (preferred when boundary is subtle)
1. *To our knowledge, [System] is the first [artifact] that [qualified capability] under [assumption].* — **Compilers/MLSys**
2. *We are not aware of prior work that [verb] [object] while [constraint].* — **PLDI/CGO**
3. *Existing systems [do A]; [ours] additionally [B], which [enables C].* — **OSDI/SOSP**
4. *Prior [category] approaches handle [X] but not [Y]; we target [Y] directly.* — **ASPLOS/HPCA**

### Strong (use only with verifiable scope)
1. *No prior [compiler/runtime/scheduler] provides [specific interface/property].* — **PLDI/MLIR-style**
2. *This is the first end-to-end system to [goal] on [platform] at [scale metric].* — **SC/PPoPP**
3. *Unlike earlier [line of work], we [mechanism] rather than [weaker substitute].* — **ISCA/MICRO**

---

## 2. Presenting Numbers

1. *[System] achieves [metric]=[value] on [workload] ([hardware], [config]), [comparison phrase].* — **All subfields**
2. *Compared to [baseline], [System] improves [metric] by [factor/Δ] ([pXX] over [N] runs).* — **Eval-heavy (ATC, MLSys)**
3. *At [operating point], [System] reaches [X]% of [oracle/hand-tuned] while reducing [cost] by [Y]×.* — **Kernel/autotuning (TVM, CUTLASS lineage)**
4. *[Component] accounts for [fraction] of [end-to-end metric]; optimizing it yields [global Δ].* — **Profiling-driven (FlashAttention, vLLM)**
5. *Speedups range from [low] to [high] across [sweep axis]; geometric mean is [value].* — **Fair reporting (PPoPP, SC)**

---

## 3. Acknowledging Limitations

1. *We do not evaluate [scenario] because [resource/relevance reason].* — **R1-safe eval**
2. *This limitation is orthogonal to [core claim]; it affects [scope] only.* — **Design vs. eval boundary**
3. *Our prototype [does not implement X]; production systems would need [Y].* — **OSDI honesty norm**
4. *Results may not transfer to [hardware/workload class] where [assumption breaks].* — **HPCA/ISCA**
5. *We leave [extension] to future work; the current design already supports [hook].* — **Conclusion/future**

---

## 4. Explaining Mechanism

1. *The key insight is that [phenomenon] implies [design consequence].* — **Intro/design bridge**
2. *[Component] exploits [hardware property] to [effect] without [cost].* — **GPU/kernel papers**
3. *By [representation choice], we reduce [problem] to [simpler problem].* — **Compiler (MLIR, XLA)**
4. *[Invariant/property] holds because [reason]; enforcement is via [mechanism].* — **ASPLOS/PLDI**
5. *At runtime, [stage A] produces [artifact] consumed by [stage B], which [action].* — **Distributed systems (Megatron, DeepSpeed)*

---

## 5. Comparing Approaches

1. *Unlike [prior], which [limitation], [ours] [advantage] by [mechanism].* — **Universal**
2. *[Prior A] optimizes [objective 1]; [Prior B] optimizes [objective 2]; [ours] trades [P] for [Q].* — **Related work**
3. *A straightforward adaptation of [prior] would [failure mode]; therefore we [alternative].* — **Design rationale**
4. *Both [X] and [Y] use [shared technique]; [X] applies it to [domain 1], whereas we apply it to [domain 2].* — **Closest-competitor positioning**
5. *Where [baseline] requires [manual step], [System] automates [step] via [interface/pass].* — **MLSys/autotuning**

---

## 6. Motivating Design Choices

1. *We chose [X] over [Y] because [measurable or correctness reason].* — **Design § staple**
2. *[Property] is necessary because [workload/hardware fact]; without it, [failure].* — **HPC/scheduling**
3. *Alternatives such as [A] and [B] fail our [constraint table / invariant list].* — **ASPLOS-style**
4. *This design keeps [hot path] on [fast resource] and relegates [cold path] to [slow resource].* — **Performance architecture**
5. *Generality in [dimension] would force [cost]; we scope to [assumption] where [benefit] dominates.* — **Scope negotiation**

---

## 7. Transitions

### Section openers
1. *We next describe [component], which [one-line job].* — **Design**
2. *This section evaluates [claim list] using [methodology summary].* — **Eval**
3. *We organize related work by [axis: representation / search / runtime].* — **Related work**

### Paragraph bridges
1. *However, [previous paragraph conclusion] breaks down when [new condition].* — **Problem deepening**
2. *Building on this observation, [next mechanism].* — **Insight → design**
3. *The above suggests [hypothesis]; §[N] tests it via [experiment].* — **Forward reference**

### Figure/table lead-ins
1. *Figure [N] illustrates [mechanism]; notably, [one detail].* — **Avoid naked `\ref{}`*
2. *Table [N] summarizes [axes]; we discuss outliers below.* — **Eval**

### Subfield affinity quick map
| Subfield | Favor |
|----------|-------|
| Compilers (PLDI, CGO, CC) | invariants, lowering, "reduce to" |
| ML systems (MLSys, ATC) | end-to-end metrics, training/inference scope |
| HPC (SC, PPoPP) | scaling, bandwidth, strong scaling efficiency |
| Architecture (ISCA, MICRO, HPCA) | mechanism + microarch constraint |
| OSDI/SOSP/EuroSys | workload realism, deployment constraints |
| NSDI/SIGCOMM/FAST | tail latency, failure modes, fairness at scale |

---

## Usage

- Pick **one strong claim template + one hedged variant** per contribution bullet.
- Pair number templates with **hardware, workload, baseline, statistic** slots filled before drafting.
- Rotate transition openers; avoid identical section-first sentences across §3–§6.
