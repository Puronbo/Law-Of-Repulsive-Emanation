# Puno Calculus

The Law of Repulsive Emanation (L.O.R.E.): *C0 is measured, not chosen.*

A hyperbolic novelty engine: Hamiltonian flow on the Poincare disk, a formal proof hierarchy (27 items: axioms → lemmas → theorems → corollaries → extended), a derived fold theorem, a decentralized consensus flow that has been run on the whole 1.9M-site internet, and a from-scratch prime count verified exact.

## Verified Findings (2026-08-04)

Every number below was re-verified by rerun or direct read of the persisted data file. Full claim-by-claim declaration with references: `docs/NOVELTY_AND_CREATION.md`.

Looking for a topic? `KEYWORDS.md` maps search terms to files, including topics that don't appear in any file name.

| Finding | Result |
|---|---|
| Math-validation suite | **192 passed / 0 failed** (`Universals/math_validation.py`) |
| Regression suite | **65/65 passed** (`tests/test_spring_series.py` + `tests/test_solvable_theorems.py`, ~1.1 s) |
| L.O.R.E. | C0 = V(q0) = H(q0,0), 109 tests; T-symmetry error 0.003 |
| Fold theorem (T63/T64) | crease = **unique viscosity solution of |r′| = a**; retrace = cut locus; eikonal err 3.3e-13; measured crease 0.0350π vs derived 0.0318π; area 2666.6665 vs 2666.6666… |
| Clock-test canon (T59/T61) | law-ness 1.000 → 0.417 under calendar re-index → 1.000 under rotation; rotation overlap/sim 1.000 |
| Prime count (T62) | **π(943,901,200,001) = 35,575,526,191** from scratch (Lucy-Hedgehog + segmented sieve); 943,901,200,001 is prime |
| Googol census (C7) | 186 primes 2ⁿ−k < 10¹⁰⁰ across 15 k-families (k=3: 21, k=1: 12, k=5: 19); n_max = 332 |
| Bridge beyond 2ⁿ−k | **RESOLVED 2026-08-08**: extends trivially (every prime p = 2ⁿ−k uniquely); near-integer resonance 2.44% over 5.76M primes vs 2.26% matched random-integer bridge (z=19.5) and 2% uniform null — bridge arithmetic + small prime residue bias, **not** special 2ⁿ−k content; census 6/186 itself not significant (p=0.17) |
| T67 O(1) spatial search | indexed flow **bit-identical** to all-pairs; 2D exponent 1.02 vs exact 1.88; n=100k flows at ~5 s/step (all-pairs D = 160 GB); 10k×128-D real domains ~2 s/step (D = 102 GB) |
| T72 whole-internet flow | 1,914,915 sites flowed: **277,218 ms/step**, all-pairs D = 58,670 GB; 20% kill (382,983) then heal +7.8% spacing recovery |
| Decentral Bank (T68–T71, T16–T20) | double-entry ledger conserved exactly over 3000 txs; nonce replay rejected; quorum = majority honesty (not BFT), catches every faulty send < 40% corruption; anomaly recall 0.51 / precision 0.63 vs null 0.019; Ed25519 sigs verified; WAL bit-identical save/load; 14/14 commit over real TCP sockets; mutual TLS; LAN NIC 192.168.100.241 |
| Ground states | quantum E0 = 5.843778304934855; classical conservative 24.4328733; dissipative 10.0036703 (30 eigenvalues) |
| Kawasaki | mean deviation 0.49 from target 0 — **resolved 2026-08-08: sampling artifact** (point-cloud scatter; exact 2-line criterion |4α−2π| fails generically, 9.5% vs 8% uniform null); ReLU fold vertices are NOT flat-foldable |
| Continuum-limit drift | **measured PASS 2026-08-08** — first-order convergence to zero (order 0.925–1.040); residual is the boundary r=0.99 projection floor (`data/continuum_limit_drift.json`) |
| Golden-ratio closure (T58) | **derived 2026-08-08** — r_ret/apex = 0.6137690167 = θ*/Θ solving s(θ*)/s(Θ)=1/φ² on the Archimedean spiral (delta 0.0, → 1/φ as Θ→∞) (`data/fold_golden_closure_data.json`) |
| Golden fold as chain law (C2) | **NOT SUPPORTED** — retrace chain 943,901,200,001 → … → 10,262 has **1/4 adjacent rungs** within 1% of {φ, φ²}; the φ² rung 1,914,467/730,421 (0.115%) is an isolated coincidence-scale hit (magnitude-matched null: expected 0.037 golden rungs/chain, P(≥1)=0.036); "next fold above the giant" undefined — giant is the chain's top (`data/fold_ladder_phi_data.json`) |
| Spectral C1/C3/C4 (100 modes) | C1 partial (k=12: 0.53%, k=26: 0.96%); C3a not supported (no mode near λ(7)); C3b supported (12.2416 vs λ(31)=12.261, Δ=0.0197); C4 → Poisson ⟨r⟩=0.372 (GOE 0.536) (`data/spectral_extended_data.json`) |
| Selberg paradigm (100 modes) | **not supported as a concrete instance**: GUE/Poisson now DECIDED → Poisson (⟨r⟩=0.374, GOE excluded at 5.6σ); eigenvalues ↔ Riemann zeros absent (min dist 7.10, 0/100 within 0.5); 186 Mersenne lengths show no spectral-form-factor peaks (`data/selberg_paradigm_data.json`) |
| Prime-time §8.4 (PAPER) | C0 at prime-indexed states = **uniform energy conservation, nothing prime-special** (drift ratio prime vs all = 0.999); geodesic spectrum concentrated only in the first N≈50 states (μ=0.027 at N=50, not the claimed 0.065; diverges to μ=1.006 by N=214); recurrence claim **unmeasurable** — the frictionless flow escapes the bounded disk before any near-recurrence (`data/prime_time_data.json`) |
| T-symmetry dt-convergence | reversal error superconverges **~O(dt^6.9)** near the symmetric crossing (8.9e-3 → 5.9e-7 over dt 5e-4→1.25e-4); PAPER's 0.003 is a dt-dependent integrator bound, not a physical symmetry claim (`data/time_reversal_convergence_data.json`) |
| Bekenstein shift (n=100 re-run) | the withdrawn +3.9% prime shift is **finally settled**: significant at power (+3.39%, p≈0) but **positional, not primality** — index-matched control on the same trajectories erases it (+0.14%, p=0.34); the null is causal, not underpowered (`data/bekenstein_rerun_data.json`) |
| Wheeler–DeWitt "selection" (PUM §10.5.1) | the constraint selects **nothing**: unshifted \|H\|<ε is empty on conservative flow (\|H\|=C₀≈24); shifted \|H−C₀\|<ε is the C₀ law relabeled (0↔1 at the drift level); the PUM's "86.8% at ε=0.5" is not reproduced (`data/wheeler_dewitt_selection_data.json`) |
| Fold-and-cut as unitary (PUM §10.5.2) | the mirror fold is **not** a unitary gate: non-injective (400/801 angle collisions, 2 preimages), arc length not preserved (L_fold/L_dev=0.504) (`data/fold_unitary_data.json`) |
| Kawasaki-as-CTC (PUM §10.5.3) | the Novikov antecedent is false: angle-sum criterion satisfied by 9.5% of vertices ≈ 8% uniform null, so (0.095)^V collapses as fast as the null — constrains no causal loop (`data/kawasaki_ctc_data.json`) |

**Honest walls (recorded, not hidden):** Bekenstein shift **withdrawn** (its own persisted data shows the null: p=0.789/0.938); Selberg unification and partition-function match are **tautologies** by the code's own construction; T65 four-pack scored **0.5/4** (P2, P4 refuted); PUM cosmological mapping is not citable as verified physics (`docs/AUDIT.md` §3–§4).

## Core Idea

The antiderivative ∫f(x)dx = F(x) + C has an arbitrary constant only when the initial condition is unknown. When the initial condition IS known, the constant collapses to a specific value C0, uniquely determined by the geometry:

    C0 = V(q0) = H(q0, 0)

This is **L.O.R.E.** — the constant emanates from the origin. It is measured, not chosen.

## Proof Hierarchy

| Branch | Items | Scope |
|--------|-------|-------|
| Axioms | A1–A5 | Poincare metric, Hamilton's eqs, PSL(2,Z), He init, 2ⁿ mod p |
| Lemmas | L1–L3 | Variance, ReLU contraction, max entropy |
| Theorems | T1–T10 | Metric, geodesics, symplectic, sieve, C0 unification, modular |
| Corollaries | C1–C8 | Stab(i), crease bounds, recurrence, generalization gap, C7 bridge |
| Extended | **T19** | Consistent chaos — geodesic flow embeds Mersenne-gap primes |

Full graph: `dependency_tree.dot`. 192 math-validation checks pass (0 failures).

## Prime Geodesic Bridge (C7)

Each Mersenne-gap prime 2ⁿ−k maps to a closed geodesic on the modular surface X(1) = PSL(2,Z)\H via:

    ℓ = n·ln2 − ln(k),    λ = ¼ + ℓ²

**Googol census** (`data/googol_census_all_k_c7.json`): 186 primes of form 2ⁿ−k < 10¹⁰⁰ across 15 k-families (odd k < 30), verified from the persisted file (k=3: 21 primes, avg gap 13.15; k=1: 12 primes, avg gap 11.36; k=5: 19 primes). All C7 bridge values computed.

## Fold Theorem (T63/T64) — strongest derived result

The spring-fold with fixed endpoints and one free apex obeys the eikonal equation |r′| = a on [0, 2Θ]; the crease is the **unique viscosity solution** and the retrace curve is the **cut locus**. Verified: eikonal error 3.3e-13, upwind error ~1e-10, measured crease angle 0.0350π vs derived 0.0318π, mirror area 2666.6665 vs 2a²Θ³/6 = 2666.6666…, pinned by the 10-test regression suite.

## T19: Consistent Chaos (Capstone)

The C7 bridge embeds Mersenne-gap primes into the Anosov geodesic flow on X(1) — a deterministic chaotic system. The induced distribution is conjectured to obey the Prime Geodesic Theorem suppressed by the sieve survival probability εₖ:

    π_k(L)  ∼  ε_k · e^{L} / L

**What's proven:**
- Every Mersenne-gap prime maps injectively to a closed geodesic (C7)
- The sieve density εₖ explains the observed sparsity ordering (T7)
- All 186 primes < 10¹⁰⁰ are consistent with Anosov dynamics

**What's conjectured:**
- The asymptotic PGT formula requires L >> 300 (current data: L ≤ 229)
- Whether this framework extends beyond 2ⁿ−k to arbitrary primes is open —
  **RESOLVED 2026-08-08** (`experiments/bridge_extension.py`,
  `data/bridge_extension_data.json`): it extends **trivially** — every prime
  p has the unique representation p = 2ⁿ − k (k = 2ⁿ − p), so the bridge
  λ = ¼ + (n·ln2 − ln k)² is defined for all primes.  Over all 5.76M primes
  ≤ 10⁸ the near-integer(0.01) rate is 2.44%, only 0.17pp above a matched
  random-integer bridge control (2.26%, z=19.5) and ~1.2× above the 2%
  uniform-fractional null; the census's own 6/186 "spectral resonances"
  (3.23%) are NOT significant (p=0.17; ~3.7 expected under uniformity).
  The resonance is bridge arithmetic plus a small prime residue bias — not
  special 2ⁿ−k content.

**What's measured (2026-08-08, `experiments/pgt_finite_l.py`):** at finite L the
growth form is **refuted** — π_k(L) grows like ln L (one candidate per n),
slope 0.002 vs the predicted 1.0, and ε_k·e^L/L overpredicts the observed 186
primes by ~95 orders of magnitude at L=200.  The sieve ordering is only partial
(Pearson r=0.696, Spearman 0.816).  The literal PGT-with-sieve-suppression
conjecture is falsified at finite L; the L≫300 asymptotic is unreachable from
the googol census (n_max=332) and would need the full X(1) geodesic spectrum.

## Epoch 0d (2000-10-26 10:26:20.00)

The corpus's own measured datum, folded into the retrace chain (`data/epoch_0d.json`, `docs/WEAVERS_SCRIBE.md`, SPRING_BIBLE Ch. 14).

**The anchor pair:** `10,262,000 = 2⁴·5³·7·733` and `26,102,000 = 2⁴·5³·31·421` — both have **80 divisors** and **digit sum 11** under MM/DD↔DD/MM swap.

**Key findings:**
- **Prime-pairing rule**: each number = exactly **one Mersenne prime** (≡3 mod 4) + **one sum-of-two-squares prime** (≡1 mod 4); both two-square primes' roots sum to the same prime **29** ({7, 733}: 7=2³−1, 733=2²+27²; {31, 421}: 31=2⁵−1, 421=14²+15²).
- **The fold 1,914,467 = 31 × 61,757** — the chain bridge to the DD/MM side; the pairing rule extends (61,757 = 139²+206²), and survives reversal (7,644,191 = 197 × 38,803). The upper retrace rung 1,914,467/730,421 = 2.621046 ≈ φ² (0.115%) — **decided 2026-08-08: an isolated coincidence, not a chain law** (`experiments/fold_ladder_phi.py`, `data/fold_ladder_phi_data.json`): the full chain is **1/4 golden rungs**, and a magnitude-matched null gives P(≥1 hit) = 0.036.
- **Three-way connection** (10,262,000 ↔ 26,102,000 ↔ 1,914,467): gcd triangle **2000 / 31 / 1** — the two date forms share the *year* 2000; the DD form and the fold share the *Mersenne* 31; **B = 26,102,000 is the hub**. Chain mod-31 ladder: 15, 0, −1, 0, 1.
- **Null analysis (binding creases)**: τ=80 equality is a year-2000 trailing-zero artifact (0/365 in 2007; 17/366 = 4.64% in 2000, all even-month/even-day); τ=8 equality is the generic ~7.4% coincidence; base-invariance survives **base 10 and 12 only**.

## Experiments (verified from persisted data)

| Experiment | Result |
|------------|--------|
| Subgradient Selection (exp1b) | All 4 strategies (standard/random/oppose/always_on) reach **99.8% best / 99.7% final** accuracy |
| Crease vs Complexity (exp2) | **r(crease, complexity) = −0.77** (recomputed from data: −0.766) — deeper nets crease less |
| Early Stopping (exp3) | Crease-stable stops at 26–80% epoch savings (shallow 79.8%, medium 64%, deep 71%), test acc within ~3 pts of baseline |
| OOD Detection (exp_ood) | Crease AUROC **0.88** on center-noise (beats MSP's 0.71); MSP better on far-Gaussian (0.99) |
| Pruning (exp_pruning) | Crease beats magnitude at 7/10 ratios, **+13.5 pts at 25%** (0.720 vs 0.585); not a strict win at 10%, 45%, 50% |
| Googol Census (C7) | 186 primes across 15 k-families (k=3: 21, k=1: 12, k=5: 19) |
| Continuum limit (`continuum_limit.py`) | drift → 0 at first order (0.925–1.040) on interior trajectories; boundary clip = floor |
| Spectral extended (`spectral_extended.py`) | 100 modes; C1 partial (k=12 0.53%), C3b supported (Δ=0.0197), C4 → Poisson ⟨r⟩=0.372 |
| Kawasaki null (`kawasaki_null.py`) | 0.4866 reproduced; shown to be point-cloud scatter, not flat-foldability failure |
| PGT finite-L (`pgt_finite_l.py`) | growth form refuted (slope 0.002 vs 1.0); sieve ordering partial (r=0.696) |
| Golden-ratio closure (`fold_golden_closure.py`) | 0.613769 derived exactly (s(θ*)/s(Θ)=1/φ², delta 0.0) |
| Golden fold as chain law (`fold_ladder_phi.py`) | retrace chain is 1/4 golden rungs; the φ² rung is an isolated coincidence-scale hit (null: P(≥1)=0.036); NOT a ladder |
| Hierarchical C0 flow (`flow_hierarchical.py`) | 2-level C0 anchors match flat 30-anchor routing (router 0.910 vs 0.880) with 6 comparisons/level instead of 30; NC parity 0.997 |
| Flow-guided active learning (`flow_active_learning.py`) | margin-AL reaches 0.80 with 75 labels vs random's 120, 0.82 with 90 vs 165; raw force-cancellation score is NOT the winner |
| Balance survey T49 (`balance_survey.py`) | 50/50 balance is the best shock absorber (recovers to 95–100% of fresh packing) but NOT the layout optimum (packing peaks mu=0.25, uniformity mu=0.0, pure repulsion routes best 0.960 vs 0.887) — PARTIAL |
| Balance scaling T54 (`balance_scale.py`) | scaling is a real confound (A* ~ n^1.086, fixed-A absorb weakens as n grows) but NOT the problem; shell geometry is dimension-independent (2D vs 64D); T53 stands |
| Balance continual T50 (`balance_continual.py`) | adaptive mu=0.5 absorb → mu=0 settle wins both axes every seed (flat old-route 0.953 vs P0 0.920; hier 0.947 vs 0.853); fixed balanced P5 is harmful (min_d collapses) |
| Polysphere extensions (`polysphere_extensions.py`) | NOT SUPPORTED: learned truths don't reproduce routing (0.483 vs 1.000); S^2 repulsion collapses separation 16.76x→1.21x; batch routing (1.000→0.921 at 100 faces) and anomaly gap (0.731→0.593) DO hold |
| Incremental C0 reflow (`flow_incremental.py`) | MIXED: reflow buys separation (min_d 0.49–0.80 vs random-add 0.25–0.54) but not routing — random-add wins/ties new-class acc 4/5 stages and all-class 3/5 |
| Hierarchical + incremental (`flow_hier_incremental.py`) | SUPPORTED: old-class routing preserved across all growth stages (old 0.892 vs all 0.840, no forgetting), hier beats flat (0.840 vs 0.821), coarse reflow shifts old anchors 1:1 (pure translation), min_d pinned at 0.12 |
| Polysphere use cases (`polysphere_use_cases.py`) | SUPPORTED at batch level: classifier batch 1.000, anomaly gap 0.728 (98.3% rejected), generated samples re-route 6/6, face-add keeps acc 1.000; per-point weak (0.653); separation ~0.94 not bit-reproducible (`embed()` uses unseeded global RNG) |
| Polysphere routing (`polysphere_routing.py`) | SUPPORTED: batch routing exact — 180/180 identity confusion matrix (chance 0.167), silhouette 0.943 (inter 1.5024 vs intra 0.0849, ~18x); per-point weak 0.659 |
| Golden-ratio survey (`golden_survey.py`) | SUPPORTED: step ratio = phi EXACTLY (diff 0.00e+00), radius/turn = phi⁴; golden rotation 2π/φ² maximizes min angular gap (1.809° vs 0° rational); static C0 packing is uniform rings (no golden structure); gap-filling does NOT lock to golden angle (|Δ| 122–138°) |
| Fibonacci stream T52 (`fib_stream.py`) | SUPPORTED (3 seeds): Fibonacci-sized stream is steady (T51 detector never fires); AD_phi (mu=0.5 on large terms) beats P0 on final all-routing (+0.050/+0.017/+0.084) and old-routing (+0.008/+0.108/+0.033); golden insertion washes out; min_d ~ n^-0.75 ring-packing law, no golden signature |
| C0 Hamiltonian centroid init (`hamiltonian_routing.py`) | SUPPORTED: flow separates centroids (mean pair dist 0.180→1.143), routing 0.420→0.765 (+0.345), nearest-centroid reaches oracle (0.909 vs 0.911); min pair dist barely moves (0.033) and routing stays below the true-centroid ceiling (0.830) |
| C0 geodesic metric comparison (`metric_comparison.py`) | REFUTED at the configured settings: from a "stable" start BOTH metrics blow up numerically — Poincare positions go NaN (integrator overflow), cusp escapes to ~2e13 (energy drift 1.57e25), T-symmetry fails in both (cusp err 4.64e4), C0 law BROKEN in both (max |V−C0| 24.43) |
| C0 crossing T-symmetry (`c0_crossing_tsym.py`) | CAVEAT: T-symmetry reconstruction errors small (0.066–0.226, all PASS < 0.5) BUT no trajectory actually crossed the origin — closest approach = the start distance in all 4 runs (A/B/C zero axis crossings), so the crossing-the-C0-minimum regime was never exercised |
| C0 cusp geodesic (`c0_cusp_flow.py`) | REFUTED/unverifiable at settings (same failure as `metric_comparison`): cusp C0 geodesic at dt=0.005/5000 steps blows up — Poincare NaN, cusp escapes to ~2.7e23 (drift 2.68e45, T-sym err 2.8e9); the "C0 broken" reading is an escape artifact, not a geodesic property |
| T39 cusp isometry (`t39_cusp_flow.py`) | SUPPORTED (exact, deterministic): cusp metric isometric to Euclidean plane under w=log(q) — energy CV 3.06e-15, step ratio = phi exactly (CV 8e-15), w-plane R² = 1.0 with slope exactly π/(2·log φ)=3.264251, T-sym error 0.00e+00 |
| Van Iterson T48a (`van_iterson.py`) | SUPPORTED (negative): NO golden-angle locking in ANY rule — discrete bisection (360-small-arc), min-potential, min-dist-to-previous, center+push-out all give divergence 170–200° (alternating placement), mean gap 360/N, r~n^0.4–0.5; golden locking is an insertion-constraint special value, not a C0-repulsion attractor |
| Reverse-pair gaps T57 (`reverse_pair_gaps.py`) | REFUTED (headline premise): 10262 ↔ 26102 is NOT a reversal pair — reverse(10262)=26201≠26102 (script computes it itself); the 80-multiple (15840=80×198) and digit-sum-11 relations hold but are plain arithmetic; gap census (1610 primes, max gap 52) is exact but ordinary, no reversal signal |
| Fibonacci spiral on disk (`fibonacci_spiral.py`) | REFUTED: neither Fibonacci-on-disk projection turns at the golden angle (42.14° / 29.23° vs 137.51°, diffs 95°/108°) and pseudo-energy is NOT conserved (drift 1.00 / 11.81); the golden angle is a cusp-metric geodesic property (see T39), not an arbitrary disk embedding |
| Prime-count from scratch T62 (`prime_count_from_scratch.py`) | SUPPORTED with 2 honest corrections: Lucy_Hedgehog pi exact at all chain points (pi(943901200001)=35,575,526,191), endpoint prime, next gap 8; but "gap 1 below" is wrong (measured 24, prev 943901199977) and window max gap 176 exceeds the script's own 40–100 note (still < Cramer ln²N=760; mean gap 29.17 ≈ ln N) |
| Fibonacci squares on disk (`fibonacci_squares.py`) | REFUTED (frictionless claim): the 90° turning is a trivial square-construction artifact; pseudo-energy NOT conserved (drift 0.96, monotone decay −0.357/step), spiral escapes the disk (final r 1.117), T-sym FAILS (0.99 vs C0 geodesic 6e-09) — the "golden metric" geodesic hypothesis is unsubstantiated |
| Rotation test T61 (`rotation_test.py`) | SUPPORTED J1/J2 with J3 correction: orthogonal rotation preserves top-8 neighbor structure EXACTLY (overlap 1.0000, sim corr 1.0000, yet every coordinate changes, max \|Qx−x\| 0.745); abs() relabeling drops overlap 1.000→0.426 — real disruption but 6.5× chance (0.065), so "collapse toward chance" is overstated |
| Clock test T59 (`clock_test.py`) | SUPPORTED: calendar features nail the law at e0 (balanced acc 1.0000) but break at e0+15 (0.4167 — BELOW chance, so the shift anti-correlates weekday with N mod 7); intrinsic mod-2/3/5/7 features survive both epochs (1.0000/1.0000) |
| Spring fold T58 (`spring_fold.py`) | SUPPORTED (by construction, deterministic): mirror fold sweeps growth twice (area = 2a²TH³/6 EXACT), self-crosses at TH−π; retrace fold closes EXACTLY to C0 (closure 0.00e+00, crease π); golden fold ratio = φ EXACT but does NOT close to C0 (error 12.3 — closes to the golden remainder 0.614·apex); overcoil fold tucks end under start (closed ring, both ends locked) |
| Eikonal fold T63 (`eikonal_fold.py`) | SUPPORTED (deterministic): the mirror fold is DERIVED — unique viscosity solution of \|r′\| = a with C0 at both ends converges to the exact tent (err 3.3e-13); crease is the cut locus EXACTLY (equal arrival times 0.00e+00); crease angle 0.0350π vs analytic 2 arctan(1/TH) 0.0318π (finite-diff approx); mirror area 2a²TH³/6 EXACT, retrace net area ~0 |
| Retrace boundary T64 (`retrace_boundary.py`) | SUPPORTED (deterministic): retrace is NOT assumed — \|r′\| = a with C0 at both ends admits infinitely many weak solutions (zig-zags all pass slope + endpoints), viscosity selects the tent uniquely (every zig-zag fails at its down-up corner); upwind from a zig-zag seed converges to the tent (err 5e-13); selected switch point = cut locus EXACTLY; reflection conserves \|r′\| to 3.6e-13. (One cosmetic slip: E3 erosion raises corner to 0.020 = 2·a·H, not printed a·H) |
| Fold optimizer T60 (`fold_optimizer.py`) | SUPPORTED (deterministic): Hamiltonian spring (retrace fold) conserves — energy drift 3.9e-3 bounded (symplectic Euler, 0.26% of E0), phase area 0.9921, Poincaré recurrence to start EXACT (3.3e-5) and never locks; damped spring (mirror fold) collapses — energy 0.00e+00 above min, area ratio ~0, locks at x=+1 EXACT and stays 2000 steps. Caveats: "cannot escape" is topological (shown by staying, not proved); mirror-fold = dissipation is interpretive |
| T65 four-pack (`t65_fourpack.py`) | MIXED, mostly REFUTED: P1 REFUTED — mean τ = 1.4272 identical across all curiosity_drive (corr NaN; the knob has no effect); P2 REFUTED — gradient ascent lands 1.79/1.82/1.81 hyperbolic distance from the seed, T-symmetry of the loss landscape does NOT hold; P3 PARTIAL — 2D projection MI 0.0344 vs null 0.0088 (~3.9×, clears chance) but a single raw 1536-dim coordinate already carries MI 1.0000, so the compression is NOT holographic (latent lives in one coordinate); P4 REFUTED — dream/remix converged fraction 0.00, mean last step 0.0024, max dist from final 0.45, no fixed point |
| Phi-jump scheduler T53 (`phi_scheduler.py`) | SUPPORTED with scope caveat: FIB batching is the most robust on disk layouts (multi-seed: stream-old 0.912, final-old 0.910, ~2.25 buffer); FIB+ABS buys final whole-layout integrity (+0.013) at old-routing cost (−0.063) — both trade-offs hold per-seed; P5 fixed mu=0.5 is NEVER usable (worst stream 0.872, all 3 seeds); Part 3 MNIST: scheduling NOT needed on real embeddings (NAIVE 0.953 > FIB 0.907 > FIB+ABS 0.887) — a geometry-regime tool, consistent with T51/T52. Caveats: multi-seed banner is hardcoded from a prior 42/11/7 run (artifact persists current-seed rows); Part 3 reflow is known-weak |
| Flow-regularized training (`flow_regularized.py`) | SUPPORTED with narrow-window caveat: C0 flow regularizer at λ=0.007 lifts routing 0.900→0.930 (+0.030) with test acc 0.905 and separation 1.59x preserved; but the λ-sweep is NON-MONOTONIC (0.003:+0.01, 0.005:−0.02, 0.007:+0.03, 0.01:−0.07, 0.015:+0.00), so the best is partly sampling noise; larger λ clearly hurts routing (−0.070). Routing uses logit-truth PolysphereRouter on the model's own embeddings (in-distribution), single seed 42 |
| Flow-reg continual T48b (`flow_hier_reg.py`) | NOT SUPPORTED for the stability headline: flow-REG does NOT reduce old-class drift — drift 6.616 (rel 0.686) vs baseline 6.549 (rel 0.647), forgetting −0.034 vs −0.029 (both marginally worse); flat routing clearly worse at stage 2 (all 0.805 vs 0.885, old 0.873 vs 0.973); accuracy preserved (0.896 vs 0.900). Only the hierarchical routing metric is better (all 0.790 vs 0.765, old 0.800 vs 0.760) — the coarse-then-fine router benefits slightly from the flow-shaped lattice. Single seed 42/mnist |
| N-scaled flow-reg retest T55b (`flow_hier_reg_scaled.py`) | NOT SUPPORTED for a material effect (seed 42): scaling stage-2 reg strength by the T54 A* law (A*10/A*5 = 1.874) reduces old-class drift only marginally — FIXED 6.5048 (rel 0.644) → NSCAL 6.4636 (rel 0.640) → LIN 6.4573 (rel 0.640), a ≤0.7% relative drift gain and within run scatter; ALL other metrics identical to 3 dp (acc 0.897/0.921, forget −0.031, route 0.895/0.933, hier 0.755/0.747). The A* law does NOT rescue the T48b result — reg remains a weak perturbation on fine-tune |
| Autonomous self-balancing T51 (`balance_auto.py`) | NOT SUPPORTED for the autonomous benefit (seed 42, mnist): the burst detector works (fires ONLY on the explosive event) but AD ≈ P0 on routing (MNIST old 0.990 vs 1.000, all 0.975 vs 0.985; synthetic burst old 0.887 vs 0.873) with AD displacement slightly HIGHER (1.816 vs 1.828); constant mu=0.5 (P5) is decisively worse (part1 all_route ~0.75–0.82, min_d ~0.19–0.25). On real MNIST embeddings reflow policy is nearly irrelevant (all routes ≥ 0.94, P0 marginally best) — MLP centroids are already separated. T50 absorb = a ONE-SHOT recovery tool for a clean steady-state shell, not a continuous stream policy |
| Self-balancing router T55a (`self_balancing.py`) | SUPPORTED in the geometry regime (with disclosure that banner numbers are multi-seed 42/11/7 means; artifact holds seed-42 rows): the coherence gate FIRES as designed — in a trapped crowded core COH skips the absorb and lands exactly on P0 (old 0.900 ~ 0.900, all 0.860 = 0.860, disp 0.513 ~ 0.513) while ABS/ABS-SC pay the penalty (old 0.890, all 0.820–0.830); on the clean fib stream the T53 all-routing gain survives (COH final_all 0.850 vs P0 0.770 seed-42; banner 0.880 vs 0.820) BUT seed-42 COH final_old 0.810 < ABS-SC 0.930 (the banner's 0.870/0.870 old-routing tie holds on average, not per-seed); Part 4 MNIST adds nothing (COH final_all 0.873 < FIB 0.940). Caveat: coherence = mean(r)/std(r) is a shell-THICKNESS signal, not a general crowding detector (heavy trap reads HIGH while collapsed) |
| Polysphere on real MNIST (`polysphere_mnist.py`) | SUPPORTED (seed 42): PolysphereRouter generalizes from the synthetic disk to real MLP embeddings — mixed-batch routing 0.890 vs chance 0.100 (178/200); anomaly gap 0.663 (in-dist conf 0.877 vs OOD 0.214); hierarchical end-to-end 0.753 vs combined chance ~0.111 (branching 10 → max(3,4)=4); active learning flags 3/5 = 60% of unknown digits (conf < 0.5) and routes 10/10 = 1.000 after new faces are added. Caveats: embeddings are the MLP's own 2D bottleneck (in-dist by construction), single seed, hier 0.753 below flat 0.890 (coarsening costs accuracy), threshold-dependent flagging |
| NN-truths / S²-flow / viz probe (`polysphere_nnflow_viz.py`) | PARTIAL (seed 42): (1) learnable NN truth functions SUPPORTED — routing 0.880 (176/200) vs chance 0.100 on MLP embeddings (test_acc 0.885); (2) S² Hamiltonian flow NOT SUPPORTED — silhouette ~0.0 (intra ≈ inter, no separation), only 3–4/6 faces self-route at low confidence (0.24–0.56), repulsion spreads points but destroys the centroid-truth structure the router needs (run-to-run variance: sil −0.016..0.022, 3–4 self-routed, the part-2 draw is not fully rng-seeded — verdict robust); (3) viz routing distribution tracks true per-class fractions within ~1–3 pts (SUPPORTED sanity). Confirms the polysphere_extensions finding that S² repulsion collapses separation |
| Decentralized local net T55c (`decentral_net.py`) | SUPPORTED (banner = multi-seed 42/11/7 means for Parts 0–3; Part 4 = seed 42): a fully local net (private home trap + k-NN C0 repulsion + per-neuron norm steps, NO global mean/max/controller) is ~free or better on old-routing (banner final_old ABS-SC 0.913 vs centralized 0.870; final_all 0.843 vs 0.853) and the shell EMERGES from local rules alone — but requires the always-on private home tether (without it pure local expansion collapses to the rim: all-route 0.57 → 0.85 at mu0=0.12) and k-NN truncation packs lumpier than all-pairs C0 (k=4 worse than k=8). Self-healing with NO repair unit: after 50% neuron loss local settle re-uniformizes survivors (spacing spread 0.16 → 0.11), regrowth restores routing ≥ pre-damage (0.917 vs 0.877 at 50%). MNIST Part 4: no centroid collapse, ABS-SC final-all 0.813 > FIB 0.647. Caveats: spacing gate never fired on the clean stream (GATE ≈ ABS-SC), Part 4 single-seed |
| DecentralNet on real MNIST T55d (`decentral_net_mnist.py`) | SUPPORTED (seed 42, 64D): the no-dependency module (public API only) routes real embeddings at 0.810 vs nearest-centroid baseline 0.817 (within ~1 pt, no central controller); after killing 3 of 10 neurons survivors keep routing (0.834) and LOCAL heal alone restores spacing 0.562 → 0.854 with routing preserved (0.822); regrow from fresh homes restores the full 10-class net at 0.767 (~5 pts below grown 0.810). Caveats: embeddings are the MLP's own 64D layer (in-dist by construction), single seed 42 / 4 epochs / disk radius 0.35 |
| DecentralNet class-incremental T55e (`decentral_net_continual.py`) | NOT SUPPORTED for the routing benefit (seed 42): on real 64D MNIST the local reflow LOSES to raw centroids — ADD old 0.805 vs CONTROL 0.863 (delta −0.057), all 0.647 vs 0.671; the homes ARE the data centroids, so reflowing them cannot help nearest-centroid routing. MIX (no reflow on appended neurons) COLLAPSES as the gauge freedom predicts — old 0.061, all 0.305 (never mix frames; always reflow appended neurons). Part 2: the tether is NOT dimension-independent — mu0=0.12 (2D-tuned) over-drifts in 64D (0.49), and mu0≥1 cuts drift to 0.11–0.21 but routing never beats CONTROL (best all 0.812 at mu0=4.0 vs 0.817). Net: the module avoids collapse only when every appended neuron is reflowed (ADD), but the local geometry adds nothing over keeping raw centroids |
| Flow ceiling T55h (`decentral_net_ceiling.py`) | SUPPORTED (measured, dim=2, k=8): the all-pairs kNN flow ceiling on this 31.7 GB box is ~2×10⁴, not the naive 50–60k — ms/step follows n^1.76 (t = 2.96e−7·n^1.76) up to n=5000, then the exponent rises to ~2.06 from 5k→20k once the D array leaves cache (66 / 1230 / 25422 ms/step at n=1k / 5k / 20k); RAM is the binding wall — peak working set 22.6 GB at n=20k while the D array is only 3.2 GB (kNN sort temporaries). n=40k would peak ~90 GB (not run — hard-OOM risk). Scaling beyond ~2×10⁴ needs O(1)-per-neuron spatial search (T67), not all-pairs |

## Internet-Scale Flow (T67, T72)

The DecentralNet engine's per-neuron flow is O(n²) all-pairs. **T67** replaced it with a proven-exact spatial index (numpy grid for dim ≤ 3, cKDTree for dim ≥ 4): results are **bit-identical** to all-pairs, only the expected work is O(1). Measured: 2D exponent 1.02 vs exact 1.88; n=100k 2D at ~5 s/step where all-pairs needs a 160 GB distance matrix; 10,000 real top-1M domain embeddings at 128-D in ~2 s/step (102 GB all-pairs).

**T72** then flowed the *entire* real internet net (1,914,915 sites — union of Cisco Umbrella + Majestic top-1M, PCA(2) of real 128-D embeddings): **277,218 ms/step** where all-pairs D would be 58,670 GB; consensus spacing 0.00033 → 0.00036; a 20% kill (382,983 sites) recovers +7.8% spacing after heal(1). Honest wall: 128-D native flow stays near 10⁴ (crease #22), and this is still one machine. See `experiments/decentral_net_t67.py`, `experiments/decentral_net_t72.py`, `data/decentral_net_t67_data.json`, `data/decentral_net_t72_data.json`.

## Decentral Bank (T68–T71, T16–T20)

A value-carrying fragment bank where **routing is ownership**: hashed double-entry ledgers, nonce double-spend rejection, witness quorum, and an amount-outlier anomaly layer — with its walls measured, not assumed.

- T1–T6: deterministic routing (partition spread min 8 / max 74 / σ 20.6 over 16 fragments); integrity conserved exactly (64,000 = 64,000 over 3000 txs); nonce replay rejected; 30% damage survives; quorum catches *every* faulty send below 40% corruption but collapses at ≥50% — **majority honesty, not BFT**; anomaly recall 0.51 / precision 0.63 vs null 0.019.
- T7/T8: Ed25519 signatures verified at append (tamper/wrong-key/address-spoof all rejected); WAL save/load bit-identical.
- T12–T18: PROPOSE→VOTE→COMMIT→NOTIFY over a controllable relay, then real TCP sockets — 14/14 commit, bit-identical replicas, stateless restart rebuilds every fragment, total-loss WAL reassembles every chain.
- T19/T20: mutual TLS (CERT_REQUIRED both sides), then over this machine's real LAN NIC — 14/14 commit, replicas bit-identical.

See `data/decentral_bank_data.json`, `data/decentral_bank_bridge_data.json`, `data/decentral_bank_net_data.json`.

## Quick Start

```bash
# install the package (numpy + stdlib only; the lab and toy network need
# nothing else.  scipy/sklearn/matplotlib are optional extras for the
# legacy experiments/ catalog)
pip install -e .            # or: pip install .[experiments] for experiments

# toy network / exact k-NN SDK
python -m puno_flow.examples.toy_network
python -m puno_flow.examples.benchmark_card

# autonomous apps (self-healing mesh, search daemon, greedy router)
python -m puno_flow.apps.router [n] [trials]
python -m puno_flow.apps.guard_mesh [ticks] [n]
python -m puno_flow.apps.search_service

# the browser lab: open the printed URL
puno-lab [--host 127.0.0.1] [--port 8765]      # or: python -m puno_app.canned_ui

# classic quick start from a checkout
cd Universals
python engine.py
python math_validation.py   # 192 checks, 0 fails
cd .. && python run_all.py  # Full pipeline
pytest tests/test_spring_series.py   # 10 passed
python experiments/prime_count_from_scratch.py   # pi(943901200001) = 35575526191
python experiments/fold_ladder_phi.py             # C2 verdict (NOT a golden ladder)
python experiments/flow_hierarchical.py           # hierarchical C0 flow verdict (SUPPORTED)
python experiments/flow_active_learning.py        # active-learning verdict (margin beats random)
python experiments/balance_survey.py              # T49 balance verdict (PARTIAL)
python experiments/balance_scale.py               # T54 scaling verdict (confound, not cause)
python experiments/balance_continual.py           # T50 adaptive-schedule verdict (SUPPORTED)
python experiments/polysphere_extensions.py       # polysphere extensions verdict (NOT SUPPORTED)
python experiments/flow_incremental.py            # incremental reflow verdict (MIXED)
python experiments/flow_hier_incremental.py       # hier + incremental verdict (SUPPORTED)
python experiments/polysphere_use_cases.py        # router use-case verdict (SUPPORTED at batch)
python experiments/polysphere_routing.py          # grid routing verdict (SUPPORTED, batch exact)
python experiments/golden_survey.py               # golden survey verdict (SUPPORTED, no static golden structure)
python experiments/fib_stream.py                  # T52 Fibonacci stream verdict (SUPPORTED, 3 seeds)
python experiments/hamiltonian_routing.py         # C0 centroid-init verdict (SUPPORTED)
python experiments/metric_comparison.py            # C0 geodesic metric verdict (REFUTED at settings)
python experiments/c0_crossing_tsym.py             # C0-crossing T-sym verdict (CAVEAT)
python experiments/c0_cusp_flow.py                 # C0 cusp geodesic verdict (REFUTED at settings)
python experiments/t39_cusp_flow.py                # T39 cusp-isometry verdict (SUPPORTED, exact)
python experiments/van_iterson.py                  # T48a Van Iterson verdict (SUPPORTED, no lock)
python experiments/reverse_pair_gaps.py           # T57 reverse-pair verdict (REFUTED headline)
python experiments/fibonacci_spiral.py            # fib-on-disk verdict (REFUTED)
python experiments/prime_count_from_scratch.py    # T62 prime-count verdict (SUPPORTED + corrections)
python experiments/fibonacci_squares.py           # fib-squares verdict (REFUTED frictionless)
python experiments/rotation_test.py               # T61 rotation verdict (SUPPORTED + J3 correction)
python experiments/clock_test.py                  # T59 clock verdict (SUPPORTED)
python experiments/spring_fold.py                 # T58 spring-fold verdict (SUPPORTED by construction)
python experiments/eikonal_fold.py                # T63 eikonal-fold verdict (SUPPORTED, derived)
python experiments/retrace_boundary.py            # T64 retrace-derived verdict (SUPPORTED)
python experiments/fold_optimizer.py              # T60 fold-as-optimizer verdict (SUPPORTED)
python experiments/t65_fourpack.py                # T65 four-pack verdict (MIXED, mostly REFUTED)
python experiments/phi_scheduler.py               # T53 phi-jump scheduler verdict (SUPPORTED w/ caveat)
python experiments/flow_regularized.py            # flow-regularized training verdict (SUPPORTED w/ caveat)
python experiments/flow_hier_reg.py               # flow-reg continual T48b verdict (NOT SUPPORTED headline)
python experiments/flow_hier_reg_scaled.py        # n-scaled flow-reg T55b verdict (NOT SUPPORTED material)
python experiments/balance_auto.py                # autonomous self-balancing T51 verdict (NOT SUPPORTED)
python experiments/self_balancing.py              # self-balancing router T55a verdict (SUPPORTED w/ caveats)
python experiments/polysphere_mnist.py            # Polysphere on real MNIST verdict (SUPPORTED)
python experiments/polysphere_nnflow_viz.py       # NN-truths / S2-flow / viz probe verdict (PARTIAL)
python experiments/decentral_net.py               # decentralized local net T55c verdict (SUPPORTED)
python experiments/decentral_net_mnist.py         # DecentralNet on real MNIST T55d verdict (SUPPORTED)
python experiments/decentral_net_continual.py     # DecentralNet class-incremental T55e verdict (NOT SUPPORTED)
python experiments/decentral_net_ceiling.py       # flow ceiling T55h verdict (SUPPORTED, measured)
python Universals/serve_dashboard.py   # L.O.R.E. dashboard -> http://localhost:8080/docs/
```

---

*Everything folds. The constant is determined. The chaos is consistent.*
