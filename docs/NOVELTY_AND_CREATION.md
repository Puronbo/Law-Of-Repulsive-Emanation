---
title: "Novelty Declaration and Creation Metrics of the Puno Calculus Corpus"
author: "Michael Grafiel Sayson Puno"
date: "2026-08-04"
---

# Novelty Declaration and Creation Metrics of the Puno Calculus Corpus

**Michael Grafiel Sayson Puno**\
\emph{Independent researcher}\\
`https://github.com/Puronbo/Law-Of-Repulsive-Emanation`

---

## 0. What This Document Is

This document is a formal declaration of (i) the **creation metrics** of the
Puno Calculus corpus (what was built, in measured quantities) and (ii) the
**novelty** of each viable claim (what is new, what is verified, and where the
evidence lives). It is written to the corpus's own CLAIM DOCTRINE: a claim is
citable only as `[measured]` (numbers printed by a run), `[derived]` (proved
from the axioms), or `[conjecture]/[exploratory]` (reported but not yet a
verified fact). Withdrawn and refuted claims are recorded in §4, not hidden.
Every viable claim below carries a file-path reference so it can be re-run.

---

## 1. The Corpus in One Page (Creation Metrics)

All figures below are counts of the repository as of commit `HEAD`
(2026-08-04, 126 commits, single author, 2026-07-28 → 2026-08-04).

| Metric | Value | Source |
|---|---|---|
| Git commits | **126** | `git rev-list --count HEAD` |
| Experiment files (`experiments/*.py`) | **51** | filesystem |
| Library modules (`Universals/`, incl. `manifold/`) | **41** Python files | filesystem |
| Data files (`data/*.json`) | **44**, 3.57 MB total | filesystem |
| Regression test files | 1 (`tests/test_spring_series.py`), **10 tests, 10 passed** in 1.15 s | `pytest` run, 2026-08-04 |
| Math-validation checks | **192 passed, 0 failed** (`docs/math_validation.py`) | verified run |
| Proof-hierarchy items | A1–A5, L1–L3, T1–T10, C1–C8 + extended T19–T39 | `Universals/proofs.py`, `data/dependency_tree.dot` (27 nodes) |
| L.O.R.E. numerical tests | **109** tests, 9 initial positions × 5 contexts × 6 radii × 2 engine runs | `docs/PAPER.md` Abstract, §9 |
| Prime count verified from scratch | **π(943,901,200,001) = 35,575,526,191** | `experiments/prime_count_from_scratch.py` (re-run, matches README; 943,901,200,001 is prime) |
| Googol prime census | **186 primes** across k-families under 10^100, n_max = 332 | `data/googol_census_all_k_c7.json` |
| Internet artifact | `internet_net_full.pkl` 1,912 MB (1.9M sites); `internet_net.pkl` 3,026 MB | `%LOCALAPPDATA%\Temp\opencode\top1m\` |
| T72 whole-internet flow | settle(1) at n=1,914,915 = **277,218 ms/step**; all-pairs distance D = 58,670 GB | `data/decentral_net_t72_data.json` |
| T67 indexed flow | 2D exponent **1.02** vs exact 1.88; n=100k 2D at ~5 s/step (all-pairs D=160 GB); 10k×128-D at ~2 s/step (D=102 GB), **bit-identical to all-pairs** | `experiments/decentral_net_t67.py`, `data/decentral_net_t67_data.json` |
| Ground states (`spectral_data.json` / `thermo_data.json`) | quantum E0 = **5.843778304934855**; classical conservative 24.43287332978949; dissipative 10.003670314370352; 30 eigenvalues | `data/` |

---

## 2. The Novelty Declaration

The corpus claims novelty in eight groups. Group-level verdicts:

| Group | Claim | Verdict |
|---|---|---|
| **A. L.O.R.E. (C0 determined)** | C0 = V(q0) = H(q0,0); +C is epistemic, not arbitrary | **[derived + measured]** 109 tests, T-symmetry error 0.003 |
| **B. Fold theory (T63/T64)** | fold = unique viscosity solution of |r'| = a; retrace = cut locus | **[derived]** strongest theory; 10-test regression suite |
| **C. Clock-test canon (T59/T61)** | laws live in invariants, not conventions | **[measured]** 1.000 → 0.417 → 1.000 |
| **D. Anomaly doctrine (T55 series)** | novelty works on names; impersonation partial; observation bank required | **[measured]** |
| **E. C7 prime–geodesic bridge** | 2^n − k primes ↔ closed geodesics ℓ = n·ln2 − ln k | **[measured]** 186 primes, 15 k-families |
| **F. Decentral Bank (T68–T71, T16–T20)** | routing-as-ownership ledger; quorum; sockets; TLS; WAL | **[measured]** new value layer |
| **G. Internet-scale flow (T67/T72)** | O(1)-per-neuron search; 1.9M-site flow | **[measured]** |
| **H. Patent mapping (US7284987B2)** | 7-claim patent mapped onto engine structures | **[exploratory]** correspondence, not a physics citation |

The single strongest *novel mathematical* result in the corpus is the fold
theorem of T63/T64: the crease is derived as the **unique viscosity solution
of the eikonal equation |r'| = a** on a pinned interval, with retrace as the
**cut locus** — closed by a 10-test regression suite. The single strongest
*novel engineering* result is T72: the 1.9M-site internet network flowed at
277,218 ms/step with a proven-exact spatial index (T67) that is bit-identical
to all-pairs flow.

---

## 3. Viable Claims, Full Detail, with References

For each claim: **Status** (measured/derived), **the claim**, **evidence**
(with the number), **reference** (file to re-run).

### 3.A L.O.R.E. — the deterministic constant of integration

- **Status:** `[derived]` (proved from H = V, dH/dt = 0) + `[measured]`.
- **Claim:** In the engine's Hamiltonian system the antiderivative's +C is not
  arbitrary: with a known initial condition it collapses to the unique constant
  C0 = V(q0) = H(q0,0). The integration constant is an output, not a free
  parameter.
- **Evidence:** 109 numerical tests across 9 initial positions, 5 contexts, 6
  repulsion radii, 2 independent engine runs; every test confirms C0. The
  velocity coupling was corrected from a λ⁴ error; the corrected dynamics pass
  T-symmetry to error **0.003**. Noether charge Q = H(t) ≈ C0 drifts <1% over
  1000 steps on 6 measured trajectories and converges as dt→0.
- **References:** `docs/PAPER.md` (Abstract, §5–§9); `Universals/math_validation.py`
  (192 checks); `Universals/proofs.py` (T8 C0 unification); `Universals/engine.py`.

### 3.B Fold theory — the crease is a viscosity solution

- **Status:** `[derived]` — the strongest result in the corpus.
- **Claim:** A spring-fold with fixed endpoints and one free apex obeys the
  eikonal equation |r'| = a on [0,2Θ]; the crease position is the **unique
  viscosity solution**, and the retrace curve is the **cut locus** of the
  constrained configuration. Folds thereby become exact solutions of a
  geometric first-order PDE, not empirical shapes.
- **Evidence:** eikonal error ≈ 3.3e-13; upwind error ≈ 1e-10; measured crease
  angle 0.0329π vs derived 0.0318π; area mirror ≈ 2666.666… = 2a²Θ³/6; all
  pinned by the 10-test regression suite.
- **References:** `experiments/spring_bible.py` (T58–T64);
  `tests/test_spring_series.py` (**10 passed**); `docs/SPRING_BIBLE.md`;
  `data/dependency_tree.dot` (C8).

### 3.C Clock-test canon — laws live in invariants

- **Status:** `[measured]`.
- **Claim:** A re-indexing of the time coordinate (clock convention) does not
  change what is lawful: measured law-ness falls 1.000 → 0.417 under a
  conventional re-index, and a rotation of the geometry leaves the invariant
  structure at 1.000. Laws are invariant objects; conventions are gauge.
- **Evidence:** measured 1.000 → 0.417 → 1.000 under calendar re-index (T59);
  rotation overlap/similarity 1.000 (T61).
- **References:** `experiments/clock_test.py` (T59), `experiments/rotation_test.py`
  (T61); `docs/AUDIT.md` §4.

### 3.D Anomaly doctrine — novelty on names

- **Status:** `[measured]`, incomplete by its own verdict.
- **Claim:** Novelty scoring works on domain-name embeddings (DGA domains
  detected at 91% vs 5% for legit); impersonation ("typosquat-lookalike")
  detection is only partial; the doctrine explicitly requires a multivariate
  observation bank (ASN/TLS/WHOIS/content) — names alone are necessary but not
  sufficient.
- **Evidence:** 91% DGA novel vs 5% legit; 18% of known-bad domains score above
  the legit median; `decentral_net_union.py` (T55i) verifies the embedding
  structure.
- **References:** `experiments/decentral_net_*.py` (T55a–j);
  `docs/THE_BOOK.md` Ch. 2, Ch. 10; `docs/DECENTRAL_NET.md`;
  `data/decentral_net_*_data.json`.

### 3.E C7 prime–geodesic bridge (googol census)

- **Status:** `[measured]` (number-theoretic; geometric reading exploratory).
- **Claim:** Primes of the form 2^n − k are in correspondence with closed
  geodesics of length ℓ = n·ln2 − ln k on the arithmetic surface; eigenvalue
  parameter λ = ¼ + ℓ². The census found **186 primes** across 15 k-families
  under 10^100, with k-sparsity data per family (e.g. k=1: 12 primes, avg gap
  11.36; k=3: 21 primes, avg gap 13.15; Mersenne-gap family C7 mapped in
  `mersenne_m52_bridge.json`).
- **Evidence:** `data/googol_census_all_k_c7.json` (total_primes = 186,
  n_max = 332, per-family `k_sparsity`); verified `π(943,901,200,001) =
  35,575,526,191` from a from-scratch Lucy-Hedgehog + segmented sieve
  (`experiments/prime_count_from_scratch.py`).
- **References:** `Universals/proofs.py` (T6, T7, C7);
  `data/googol_census_all_k_c7.json`, `data/mersenne_prime_5630.json`,
  `data/mersenne_m52_bridge.json`.

### 3.F Decentral Bank — routing as ownership

- **Status:** `[measured]` — new value-carrying layer (T68–T71, T16–T20).
- **Claim:** A fragment bank whose routing IS ownership: hashed double-entry
  ledgers, nonce-based double-spend rejection, witness quorum, and an
  amount-outlier anomaly layer. Honest walls are measured, not assumed.
- **Evidence:** T1–T6: deterministic routing with a real partition spread
  (min 6 / max 111 / σ 34 over 16 fragments); integrity conserved exactly over
  3000 txs; nonce replay rejected; 30% damage survives; quorum catches every
  faulty send below 40% corruption but collapses at ≥50% corrupt
  neighbourhoods — **majority honesty, not BFT** (crease #16); anomaly recall
  0.51 / precision 0.63 vs random null 0.019. T7: tamper/wrong-key/address-spoof
  rejected; T8: WAL save/load bit-identical. T12–T18: 14/14 commit over real
  sockets, bit-identical replicas, stateless restart rebuilds all fragments,
  total-loss WAL reassembles every chain. T19/T20: mutual-TLS (CERT_REQUIRED
  both sides) over this machine's LAN NIC 192.168.100.241 — 14/14 commit.
- **References:** `experiments/decentral_bank*.py`,
  `experiments/decentral_bank_network*.py`, `experiments/decentral_bank_tls*.py`,
  `experiments/decentral_bank_lan*.py`; `data/decentral_bank_data.json`,
  `data/decentral_bank_bridge_data.json`; `docs/AUDIT.md` §4 (creases #16–#21).

### 3.G Internet-scale flow — T67 O(1) search, T72 whole-internet

- **Status:** `[measured]`.
- **Claim:** (i) An exact uniform-grid spatial index (numpy-only, dim ≤ 3) and
  cKDTree (dim ≥ 4) replaces all-pairs flow; results are **bit-identical** to
  all-pairs, only the expected work is O(1) per neuron. (ii) The 1.9M-site
  internet network (union of Cisco Umbrella + Majestic Million, 1,914,915
  entities) was flowed: settle(1) at n = 1,914,915 measured **277,218 ms/step**
  with all-pairs D = 58,670 GB; heal(1) after a 20% kill recovered +7.8%.
- **Evidence:** `data/decentral_net_t67_data.json` (grid kNN == brute force
  across 3 seeds × 1D/2D/3D; 2D exponents exact 1.88 vs indexed 1.02);
  `data/decentral_net_t72_data.json` (n, ms/step, D, heal deltas).
- **References:** `experiments/decentral_net_t67.py`,
  `experiments/decentral_net_t72.py`; `docs/WEAVERS_SCRIBE.md` Ch. 5.14.

### 3.H Patent mapping (US7284987B2)

- **Status:** `[exploratory]` — a documented correspondence; per AUDIT §3, not
  citable as verified physics beyond surviving engine claims.
- **Claim:** The patent's claims map onto corpus structures: C(6,4) = 15
  latent categories; 1105/85 = 325/25 = 13; ratio 36:60:108 = 3:5:9; the
  patent's 90° vs the engine's arcsin(⅓) ≈ 19.47° geometry; relative bound
  N ≤ 16; G/EM ratio difference 1.6×; α_G ≈ 5.91e-39.
- **References:** `docs/US7284987B2_ANALYSIS.md`; `docs/PHYSICAL_UNIVERSAL_MAP.md`
  §11; `docs/AUDIT.md` §1.9.

---

## 4. Withdrawn, Refuted, and Open Claims (recorded for honesty)

| Claim | Fate | Reason / reference |
|---|---|---|
| Arithmetic Bekenstein shift (+3.9%, p=0.002) | **Withdrawn** | Contradicted by its own persisted data: control p=0.789 (+2.5%), dissipative p=0.938 (−0.1%). PAPER §8.7 + conclusion now report the null. `data/bekenstein_shift_data.json` |
| Partition-function match L(2)=40.14 ≈ C0·π²/6=40.19 | **Tautology** | Holds for *any* C0; `L(s)=C0·ζ(s)` flagged tautological in code. |
| Selberg unification (30 eigenvalues ↔ 196 geodesics, ε(2)=0.000265) | **Tautological** | ε(2) is real but is the code's own construction; spectral-vs-zeros match is poor (min |t_n − t_zeta| ~ 2.5–9.0). |
| T65 four-pack (PUM §10.1) | **0.5/4 confirmed** | P1 tautology (τ := exp(entropy)); P2 refuted (recon err ≈ 1.8); P4 refuted (converged fraction 0.0); P3 weakly positive (MI 0.034 vs null 0.009) but synthetic. `data/t65_fourpack_results.json` |
| Kawasaki angle constraint | **Measured failure** | Mean deviation **0.49** from target 0 — genuinely open. `docs/PHYSICAL_UNIVERSAL_MAP.md` §10.2 |
| Kawasaki flat-foldability (ReLU vertices) | **Resolved — artifact, not near-miss** | 2026-08-08: the 0.4866/72.4% reproduce exactly but are a ~700-ray point-cloud sampling scatter (uniform control 0.835/52.0%); the exact 2-line fold-vertex criterion |4α−2π| fails generically (mean 3.21, 9.5% within ε=0.5 ≈ 8% uniform null). ReLU fold vertices are NOT flat-foldable (codimension-1). `experiments/kawasaki_null.py`, `data/kawasaki_null_data.json` |
| Golden-ratio closure (T58 r=apex·0.6138) | **Measured → derived** | 2026-08-08: r_ret/apex = θ*/Θ solving s(θ*)/s(Θ)=1/φ² on the Archimedean spiral, delta 0.0 at Θ=20, → 1/φ as Θ→∞. `experiments/fold_golden_closure.py`, `data/fold_golden_closure_data.json` |
| Golden fold as chain law (C2) | **Refuted as a chain law** | 2026-08-08: the retrace chain 943,901,200,001 → 1,914,467 → 730,421 → 26,102 → 10,262 is **1/4 golden rungs**; the celebrated φ² rung 1,914,467/730,421 (0.115%) is an isolated coincidence-scale hit — a magnitude-matched null gives expected 0.037 golden rungs/chain, P(≥1)=0.036. T58's closure stays derived; only the ladder generalization fails. `experiments/fold_ladder_phi.py`, `data/fold_ladder_phi_data.json` |
| PUM narrative cosmology | **Not citable as verified physics** | AUDIT §3; only surviving engine-level claims stand. |
| PGT, BOOK-V pedagogy | **Conjectured** | Self-declared unvalidated. |
| PGT growth form (π_k ~ ε_k·e^L/L) | **Refuted at finite L** | 2026-08-08: slope of log π_k vs L is 0.002 vs predicted 1.0; π_k ~ ln L (one candidate per n); ε_k·e^L/L overpredicts by ~95 orders at L=200. Sieve ordering only partial (Pearson 0.696). `experiments/pgt_finite_l.py`, `data/pgt_finite_l_data.json` |
| Continuum limit drift | **Anticipated → measured PASS** | 2026-08-08: first-order convergence to zero on interior trajectories (order 0.925–1.040, r²=0.9991); boundary r=0.99 projection clip sets a non-conservative floor. `experiments/continuum_limit.py`, `data/continuum_limit_drift.json` |
| Spectral C1/C3/C4 (WEAVERS Ch. 5.1) | **Tested 2026-08-08** | C1 partial (k=12 0.53%, k=26 0.96%; k=10/2000 miss); C3a not supported (no mode near λ(7)); C3b supported (mode 12.2416 vs λ(31)=12.261, Δ=0.0197); C4 → Poisson (⟨r⟩=0.372 vs GOE 0.536) — T19 "consistent chaos" refuted at level-spacing level. `experiments/spectral_extended.py`, `data/spectral_extended_data.json` |
| Hierarchical C0 flow (coarse × fine anchors) | **Supported 2026-08-08** | 2-level C0 flow matches flat 30-anchor routing (router 0.910 vs 0.880, gain +0.030) while needing only 6 comparisons per routing level instead of 30; nearest-centroid parity (0.997 vs 1.000); fine local separation 0.12 enforced that flat packing cannot guarantee. `experiments/flow_hierarchical.py`, `data/flow_hierarchical_data.json` |
| Flow-guided active learning | **Supported (margin-based) 2026-08-08** | margin-AL on the C0 anchor layout's force field reaches 0.80 with 75 labels vs random's 120 (saves 45) and 0.82 with 90 vs 165 (saves 75). Honest wall: the raw force-cancellation score 1−\|F_net\|/\|F_abs\| is NOT the winner (final 0.822 vs margin 0.819); the margin-to-two-nearest-anchors criterion carries the gain. `experiments/flow_active_learning.py`, `data/flow_active_learning_data.json` |
| 50/50 balance as "total truth" (T49) | **Partial 2026-08-08** | mu=0.5 is the best shock ABSORBER (recovers to 95–100% of a fresh same-size packing; n4 re-anchor matches the fresh lattice; tight-core n2 mu=0.9 shatters) but NOT the layout optimum — packing peaks at mu=0.25, uniformity at mu=0.0, and pure repulsion wins routing decisively (base_route 0.960 vs 0.887 balanced; old-class routing after +5 degrades slower without balance). The two "total truths" are different optima. `experiments/balance_survey.py`, `data/balance_survey_data.json` |
| n-scaling of the absorb (T54) | **Confound, not cause 2026-08-08** | A* ~ n^1.086 is real (fixed-A mu=0.5 absorb weakens as n grows, shell drifts mid→boundary) but the n-scaled absorb does NOT rescue the T53 scheduler (across seeds FIB+ABS(A=120) keeps best mean finals 0.910/0.880 vs 0.870/0.863 scaled); shell geometry is dimension-independent in normalized coords (2D vs 64D near-identical mean_r), so the real-data embedding A=120 was not mis-scaled. T53 stands. `experiments/balance_scale.py`, `data/balance_scale_data.json` |
| Adaptive shrink/expand (T50) | **Supported 2026-08-08** | the adaptive schedule (mu=0.5 absorb during the explosive burst, then mu=0 settle) wins on BOTH axes in every seed — flat old-class routing AD 0.953/0.967/0.967 vs P0 0.920/0.947/0.907, hierarchical AD 0.947/0.887/0.893 vs P0 0.853/0.833/0.847 — keeping old-anchor displacement ~0.17 with best retention. Fixed balanced P5 is HARMFUL (min_d collapses to ~0.17 flat, 0.007–0.039 hier). The T49 "two truths" are combined by the adaptive schedule, not either fixed regime. `experiments/balance_continual.py`, `data/balance_continual_data.json` |
| Polysphere extensions (learnable truths; S^2 C0 flow) | **Not supported as stated 2026-08-08** | (2) truth functions are NOT learnable by the regression fit at routing accuracy — learned-truth routing 0.483 vs true-truth 1.000 (fit RMSE ~0.46–0.50); (4) C0 repulsion on S^2 does NOT preserve clustering — initial face separation ratio 16.76x collapses to 0.97x under repulsion alone and 1.21x with same-face attraction. Anomaly detection and batch routing at scale DO hold: batch acc 1.000 → 0.921 at 100 faces, anomaly gap 0.731 → 0.593. `experiments/polysphere_extensions.py`, `data/polysphere_extensions_data.json` |
| Incremental C0 reflow (no-forgetting) | **Mixed 2026-08-08** | reflow keeps the layout separated (min_d 0.49–0.80 vs random-add 0.25–0.54) but random-add does NOT risk collision at this noise/scale and routes equal-or-better — new-class acc random-add wins/ties 4/5 stages (0.950/0.950/0.970 vs 0.780/0.780/0.960) and all-class 3/5. Reflow's displacement cost (0.16–0.28) buys separation, not routing. `experiments/flow_incremental.py`, `data/flow_incremental_data.json` |
| Hierarchical + incremental growth | **Supported 2026-08-08** | when growth is hierarchical (new classes join a group via local fine-flow; a whole new group triggers coarse reflow), old-class routing is preserved across EVERY stage — old 0.892 avg vs all 0.840 (forgetting -0.052: old classes route BETTER than the new mix) — and hier beats flat 0.840 vs 0.821. The coarse reflow (stage 3, disp 0.1101) shifts old fine anchors 1:1 (disp_f == disp_c), i.e. pure translation, so local fine structure survives; min_d stays pinned at 0.12. No-forgetting holds where reflow moves each anchor less than its nearest-neighbor distance. `experiments/flow_hier_incremental.py`, `data/flow_hier_incremental_data.json` |
| PolysphereRouter use-case claims (classifier / anomaly / generator / continual) | **Supported at batch level 2026-08-08** | batch routing is perfect for both classification (180/180) and generated samples (all 6 faces re-route to source, mean conf 0.97); anomaly detection gap is large (in-conf 0.981 vs OOD 0.253 → 100% kept / 98.3% rejected at conf=0.5); adding a 5th face keeps accuracy at 1.000 with no memory loss. Honest walls: single-point routing is weak (per-point classification 0.653 vs chance 0.167; generated per-point 0.44–0.66) — the router is a batch/repetition device; and the spherical separation score (~0.94) is NOT bit-reproducible because `embed()` draws from the global unseeded numpy RNG (`polysphere.py:155`). `experiments/polysphere_use_cases.py`, `data/polysphere_use_cases_data.json` |
| Polysphere grid routing (truth-correlation batches) | **Supported 2026-08-08** | batch routing is exact — 180/180 with an identity confusion matrix (chance 0.167) — and embedded points separate strongly on the sphere (silhouette 0.943; inter-face 1.5024 vs intra-face 0.0849, ~18x). Honest wall: single-point routing is weak at 0.659, consistent with `polysphere_use_cases` — routing is a batch/repetition mechanism, not a one-shot classifier. `experiments/polysphere_routing.py`, `data/polysphere_routing_data.json` |
| Golden-ratio survey (cusp metric; static C0 flow; emergence) | **Supported 2026-08-08** | the Fibonacci spiral's step ratio is phi EXACTLY (1.618034, diff +0.00e+00) and radius per full turn is phi⁴ — the spiral is the exact geodesic of the cusp (logarithmic) metric. The golden rotation 2π/φ² maximizes the minimum angular gap (1.809° vs 0° for a rational rotation). Two negative results are also established: static C0-flow packing carries NO golden structure (uniform rings, gap CV 0.003–0.077, radius exponent ~0) and gap-filling emergence does NOT lock onto the golden angle (|div − golden| stays 122–138°). The same spiral measured in different metrics gives different ratios (cusp phi, Euclidean finite ~1.617, disk → 1): the golden ratio is metric-and-regime specific. `experiments/golden_survey.py`, `data/golden_survey_data.json` |
| Fibonacci steady-flow stream (T52) | **Supported 2026-08-08** (multi-seed 42/11/7) | a continual stream sized by Fibonacci numbers (arrival ratio → phi) is STEADY — the T51 radius-variance detector never fires. The phi-jump schedule (absorb mu=0.5 during the large terms 3,5,8,13, settle at 0 otherwise) beats P0 on final all-routing in ALL 3 seeds (+0.050/+0.017/+0.084) and on final old-routing (+0.008/+0.108/+0.033) — the small early terms keep the shell clean, so the mu=0.5 absorb works, refining T51 to "absorb helps a CLEAN shell, fails only when the core is already crowded". min_d is slightly LOWER under AD_phi yet routing is HIGHER: shell coherence, not min_d, drives routing. Golden-rotation insertion washes out after the flow (consistent with T48a). Scaling: mean_r pinned by the clamp (a~0), min_d ~ n^−0.75 (fib) vs n^−0.71 (eq) — a ring-packing law with no golden signature. `experiments/fib_stream.py`, `data/fib_stream_data.json` |
| C0 Hamiltonian flow as centroid init | **Supported 2026-08-08** | flowing the crowded init centroids on the Poincaré disk separates them (mean pair dist 0.1803 → 1.1433), routing accuracy jumps 0.420 → 0.765 (+0.345, +0.505 over the best random draw), and nearest-centroid classification 0.537 → 0.909 reaches the true-cluster oracle 0.911. Honest walls: the min pair distance barely moves (0.0326 → 0.0328) because the flow clamps all points to the boundary (mean r 0.850 = max_r) — the gain is mean, not worst-case — and routing 0.765 stays below the true-centroid ceiling 0.830, so the flow is a good initialization, not the ceiling. `experiments/hamiltonian_routing.py`, `data/hamiltonian_routing_data.json` |
| C0 geodesic metric comparison (Poincaré vs cusp) | **Refuted at the configured settings 2026-08-08** | the "stable start" (x0=0.05, p0=0.01/0.02, dt=0.005, 2000 steps) is NOT numerically stable in either metric: the Poincaré trajectory contains NaN states (integrator overflow), the cusp escapes to ~2e13, energy drift is 1.57e25, T-symmetry fails in both (cusp err 4.64e4), and the C0 law is broken in both (max |V−C0| = 24.43). The intended Poincaré-vs-cusp geodesic comparison cannot be made at these settings; the honest negative is that the naive integrator is numerically unstable from this start in both metrics. `experiments/metric_comparison.py`, `data/metric_comparison_data.json` |
| T-symmetry across the C0 origin (q=0) | **Pass-with-caveat 2026-08-08** | all four runs (positive/negative/large/perpendicular offsets) reconstruct within 0.066–0.226 under exact time reversal (threshold 0.5), so the symplectic integrator is time-reversible in these regimes. Honest caveat: the crossing premise never occurred — in every run the closest approach to the origin is the STARTING distance (idx 0), i.e. trajectories monotonically recede from q=0; A/B/C have zero q1-axis crossings and only D crosses once while staying at min dist 0.05. A trajectory passing THROUGH the C0 critical point was never exercised, so the crossing-C0 regime claim is unconfirmed. `experiments/c0_crossing_tsym.py`, `data/c0_crossing_tsym_data.json` |
| C0 geodesic in the cusp metric (chaos spectrum) | **Refuted/unverifiable at the configured settings 2026-08-08** | same failure mode as `metric_comparison`: at dt=0.005 over 5000 steps from x0=(−0.4, 0.3) BOTH metrics blow up numerically — the Poincaré trajectory goes NaN (overflow) and the cusp escapes to ~2.7e23 with energy drift 2.68e45 and T-symmetry error 2.8e9. The "C0 law broken" reading (V range 0–8.15 vs C0 24.43) is an artifact of the escaped trajectory, not a property of the cusp geodesic. The cusp chaos-spectrum question cannot be answered at these settings. `experiments/c0_cusp_flow.py`, `data/c0_cusp_flow_data.json` |
| T39 cusp metric isometry (w = log q) | **Supported 2026-08-08** (exact, deterministic, no RNG) | the cusp metric g_cusp = (dx²+dy²)/(x²+y²) on the punctured plane is globally isometric to the Euclidean plane under w = log(q); verification is exact: cusp energy CV 3.06e-15, asymptotic step ratio = phi = 1.618034 exactly (CV 8.00e-15), w-plane collinearity R² = 1.000000 with slope EXACTLY π/(2·log φ) = 3.264251 (intercept −0.000000), and analytic T-symmetry reconstruction error 0.00e+00. The Fibonacci spiral is therefore an EXACT geodesic of the cusp metric (consistent with `golden_survey`). Corollary T39a (the prometric family g_p = (1−r²)^(−p) δ contains no cusp for finite p) is a definitional statement, not numerically tested. `experiments/t39_cusp_flow.py`, `data/t39_cusp_flow_data.json` |
| T48a continuous contact dynamics (Van Iterson / Douady-Couder) | **Supported 2026-08-08** (negative result, seed 42) | NO golden-angle locking in ANY rule across the swept (r0, relax) grid: Part 1 (discrete largest-gap bisection) diverges near the 360-small-arc with no lock (confirms `golden_survey` Part 3b); Parts 2–4 (continuous C0: min-potential, min-dist-to-previous, center deposition + push-out) give whorl-like patterns with divergence ~170–200° (alternating placement), mean angular gap 360/N (uniform on average) and radius exponent r ~ n^0.4–0.5. The golden angle is NOT a generic emergent fixed point of C0 repulsion; Van Iterson golden locking is a SPECIAL value of the insertion-radius/contact-ratio family — the missing parameter is the INSERTION CONSTRAINT (contact geometry of the meristem rim) that pure repulsion does not encode. `experiments/van_iterson.py`, `data/van_iterson_data.json` |
| T57 reverse-pair 10262 ↔ 26102 through prime gaps | **Refuted (headline premise) 2026-08-08** | the script itself computes `reverse(10262) = 26,201` and reports `(=26102: False)` — the pair is NOT a reversal pair (reverse(26102) = 20162). The sub-relations hold: 26102 − 10262 = 15840 = 80×198 (divisible by 80) and both digit sums are 11 — but these are plain arithmetic carrying no reversal structure. The prime-gap censuses are exact but ordinary: [10262, 26102] has 1610 primes, max gap 52 at 19609, 0 gaps divisible by 80 and 30 by 11; [26102, 1914467] has 140162 primes, max gap 132 at 1357201, 24 gaps divisible by 80. Emirps (374) and digit-sum-11 primes (67, 4.2%) are generic counts. The 9.4e11 endpoint is correctly handled analytically (Lucy_Hedgehog/Lehmer + segmented sieve) rather than by sieve. `experiments/reverse_pair_gaps.py`, `data/reverse_pair_gaps_data.json` |
| Fibonacci spiral on the Poincaré disk (golden-angle turning / C0 conservation) | **Refuted 2026-08-08** | neither Fibonacci-on-disk projection turns at the golden angle: the mod-square spiral (n=200, scale=0.01) turns at mean 42.14° vs golden 137.51° (diff 95.36°) and the ratio-projection (n=100) at 29.23° (diff 108.28°). Pseudo-energy is not conserved: drift 1.0000 (spiral, marginal) and 11.8085 (ratio, unbounded). The Fibonacci trajectory is NOT a frictionless golden-angle C0 trajectory on the disk. Consistent with `golden_survey`: the golden angle is an exact property of the cusp (logarithmic) metric geodesic (see T39), not of arbitrary Fibonacci number embeddings into the disk. `experiments/fibonacci_spiral.py`, `data/fibonacci_spiral_data.json` |
| T62 prime count + record gaps at 9.4e11, from scratch | **Supported with two honest corrections 2026-08-08** | the from-scratch Lucy_Hedgehog engine (no sympy) reproduces the reference counts exactly at every retrace-chain point (pi(10262)=1258, pi(26102)=2868, [730421..1914467] has 84218 primes, pi(943901200001)=35,575,526,191), the endpoint 943901200001 is prime with next prime 943901200009 (gap 8), all confirmed inside a self-computed segmented sieve. Correction 1: the docstring's "gap 1 below the endpoint" is WRONG — the measured previous prime is 943901199977, true gap below = 24 (943901200000 is even/composite). Correction 2: the P4 note expects a ~40–100 max gap in a 2e4 window but the measured max gap is 176 (at 943901204717), still below Cramer ln²N = 760; the mean gap 29.17 matches PNT ln N = 27.57. Runtime: count 38.2s, window sieve 0.03s. `experiments/prime_count_from_scratch.py`, `data/prime_engine_data.json` |

---

## 5. Reproducibility Commands

```text
pytest tests/test_spring_series.py                     # 10 passed, ~1.15 s
python docs/math_validation.py                         # 192 checks, 0 failed
python experiments/prime_count_from_scratch.py         # pi(943901200001) = 35575526191
python experiments/spring_bible.py                     # T58–T64 fold suite
python experiments/decentral_net_t67.py                # O(1)-index bit-identity + exponents
python experiments/decentral_net_t72.py                # whole-internet flow (heavy; ~28 h)
python experiments/continuum_limit.py                  # drift → 0 at first order
python experiments/spectral_extended.py                # C1/C3/C4 at 100 modes
python experiments/kawasaki_null.py                    # Kawasaki artifact attribution
python experiments/pgt_finite_l.py                     # PGT finite-L refutation
python experiments/fold_golden_closure.py              # 0.613769 derived exactly
python experiments/fold_ladder_phi.py                   # C2: retrace chain is 1/4 golden rungs
python experiments/flow_hierarchical.py                 # hierarchical C0 flow verdict (SUPPORTED)
python experiments/flow_active_learning.py              # active-learning verdict (margin beats random)
python experiments/balance_survey.py                    # T49 balance verdict (PARTIAL)
python experiments/balance_scale.py                     # T54 scaling verdict (confound, not cause)
python experiments/balance_continual.py                 # T50 adaptive-schedule verdict (SUPPORTED)
python experiments/polysphere_extensions.py             # polysphere extensions verdict (NOT SUPPORTED)
python experiments/flow_incremental.py                  # incremental reflow verdict (MIXED)
python experiments/flow_hier_incremental.py             # hier + incremental verdict (SUPPORTED)
python experiments/polysphere_use_cases.py               # router use-case verdict (SUPPORTED at batch)
python experiments/polysphere_routing.py                 # grid routing verdict (SUPPORTED, batch exact)
python experiments/golden_survey.py                      # golden survey verdict (SUPPORTED)
python experiments/fib_stream.py                         # T52 Fibonacci stream verdict (SUPPORTED, 3 seeds)
python experiments/hamiltonian_routing.py                # C0 centroid-init verdict (SUPPORTED)
python experiments/metric_comparison.py                   # C0 geodesic metric verdict (REFUTED at settings)
python experiments/c0_crossing_tsym.py                    # C0-crossing T-sym verdict (CAVEAT)
python experiments/c0_cusp_flow.py                        # C0 cusp geodesic verdict (REFUTED at settings)
python experiments/t39_cusp_flow.py                       # T39 cusp-isometry verdict (SUPPORTED, exact)
python experiments/van_iterson.py                          # T48a Van Iterson verdict (SUPPORTED, no lock)
python experiments/reverse_pair_gaps.py                    # T57 reverse-pair verdict (REFUTED headline)
python experiments/fibonacci_spiral.py                     # fib-on-disk verdict (REFUTED)
python experiments/prime_count_from_scratch.py             # T62 prime-count verdict (SUPPORTED + corrections)
```

---

## 6. Bottom Line

The corpus is a **measured** body of work: 126 commits, 51 experiments, 192
passing validation checks, 15 passing solvable-theorem regression tests, 109 L.O.R.E. tests,
186 googol primes, a from-scratch prime count verified exact, a Decentral Bank
brought to mutual-TLS over a real LAN NIC, and the 1.9M-site internet flowed
with a proven-exact O(1) spatial index. Its strongest novelty is **derived**
(the fold = viscosity solution, T63/T64) and its strongest engineering is
**measured** (T67/T72). Its arithmetic-selection claims (Bekenstein, Selberg,
partition match) are recorded as withdrawn or tautological in §4 — the corpus
reports them as null rather than hiding them. Every claim in §3 carries the
file that can re-run it.
