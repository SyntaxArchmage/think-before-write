# Academic Writing Examples

Annotated examples for QC calibration. Each shows a pass and fail variant.

## 1. Contribution Lead (Intro §1)

**Pass**: *This paper presents CroqTile, a GPU kernel DSL for Hopper (H800) where an unmodified LLM agent searches tile layouts as first-class IR; in a six-DSL study with matched tuning budget, only CroqTile beats vendor libs—115% cuBLAS on dense GEMM, 155% on blockscale, 120% cuSPARSELt on structured-sparse ops.*

**Fail**: *We present CroqTile, a novel system that dramatically improves GPU kernel performance through intelligent AI-driven optimization.*

**Why**: Pass anchors claim in hardware, mechanism, baselines, and manifest-backed numbers; fail is vague hype with no evidence.

## 2. Mechanism Walkthrough (Design §3)

**Pass**: *Each tile layout is an IR object checked at compile time: shared-memory footprint must fit SM90a capacity, and no two warps may write the same output tile without entering a reduction phase—violations fail compilation before any agent iteration.*

**Fail**: *CroqTile uses a smart IR that makes kernel tuning safer and more efficient for the LLM agent.*

**Why**: Pass states concrete invariants and failure mode; fail names components without auditable properties.

## 3. Evaluation Setup (§4)

**Pass**: *We evaluate on one H800 (CUDA 12.4, driver 550) using dense GEMM (16384³), blockscale GEMM (8192³), and 95 E4M3 sparse production shapes; baselines are cuBLAS 12.4, cuSPARSELt, and five DSLs (CUDA, Triton, CuTe, TileLang, ThunderKittens) tuned by the same LLM agent with identical iteration caps.*

**Fail**: *We compare CroqTile against several baselines on NVIDIA GPUs and show strong speedups across workloads.*

**Why**: Pass fixes hardware, versions, workloads, and fair baseline parity; fail hides whether comparisons are apples-to-apples.

## 4. Alternative Rejected (Design §3)

**Pass**: *We considered parameter-only search over fixed CUDA templates; it cannot retile shared-memory layouts when blockscale K exceeds 8192, so the agent exhausts its budget without exploring structurally valid kernels.*

**Fail**: *Fixed CUDA templates are too limited, so we built something better.*

**Why**: Pass names a concrete fatal flaw under paper constraints; fail dismisses without technical reasoning.

## 5. Related Work Contrast (§5)

**Pass**: *TVM MetaSchedule searches loop nests in a generic schedule space; CroqTile instead exposes Hopper tile buffers as schedulable IR with compile-time capacity checks, which is why the same agent finds layouts MetaSchedule cannot represent when scratchpad use is shape-dependent.*

**Fail**: *TVM autotunes kernels; CroqTile also autotunes kernels but does it differently for GPUs.*

**Why**: Pass contrasts representation and search axis; fail is name-dropping without a falsifiable difference.
