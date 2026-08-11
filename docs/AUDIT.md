# AUDIT — What is missing, conjectured, open, and claimed

Comprehensive findings from a full-corpus sweep (docs, experiments, library,
data, git history).  Verified items are marked **[verified]**, references the
audit did not re-run are marked **[claimed]** (the original source line is
given so it can be re-run).

---

## 1. WHAT IS MISSING

### 1.1 The declared next build (explicit, repeated)
* **O(1)-per-neuron spatial search.**  `decentral_net_ceiling.py` (T55h):
  "Scaling beyond ~2×10⁴ needs O(1)-per-neuron spatial search, not all-pairs."
  `decentral_net_union.py` (T55i) and `reverse_pair_gaps.py` (T57) repeat it.
  THE_BOOK Ch. 14: "the declared next build."  This is THE single most
  explicit unbuilt capability.  **[verified: repeated in 4 sources]**
  **BUILT 2026-08-04 as T67** (`experiments/decentral_net_t67.py`): the grid
  path is numpy-only and exact for dim ≤ 3, the cKDTree path exact for
  dim ≥ 4; the index is off by default so every existing experiment is
  unchanged.  Indexed 2D flow measures exponent 1.02 vs exact 1.88, and
  flows n=100,000 at ~5 s/step where all-pairs would need a 160 GB distance
  matrix (see §5 item 6 for the full record).

### 1.2 The declared-required capability
* **The multivariate observation bank** (ASN, TLS age, WHOIS, content).  THE_BOOK
  Ch. 2 defines it canonically; Ch. 10 says the anomaly doctrine *requires* it:
  "names alone are necessary but not sufficient" (measured, T55j).  No
  implementation exists — the net stores only name embeddings (`q == h` in both
  pkls **[verified]**).  This is the biggest *scientific* gap: it is the stated
  path from "novelty works" to "anomalies distinguishable."

### 1.3 T-series gaps
* **T40–T47 (8 labels) have no experiment files.**  T46 and T47 are referenced
  as prior results (`balance_continual.py`: "T46 no-forgetting mechanism";
  `fib_stream.py`: "T47's optimal incremental rotation") but no file exists here.
* **T8 referenced** by `c0_cusp_flow.py` ("the Poincaré metric (T8)") — no file.
* **T48/T55 exist only as sublabels** (T48a/b, T55a–j); the pre-T39 history lives
  in `Universals/` modules and `docs/PAPER.md`, not as experiments.

### 1.4 The migration that was never applied
* `docs/MIGRATION.md` and `MIGRATION_1.md` are **byte-identical** and describe a
  v2 rewrite (`NoveltyDetectionEngine`, `Packet`, `evaluate_batch`,
  `export_manifest`, `tests/test_engine.py` expecting "7 passed",
  `requirements.txt`).  Those symbols exist **only in `archive\`** (the old
  "hyperbolic-ai" project), never in the live repo.  The live engine is the v1
  numpy `Universals/engine.py` (which *does* contain `dream`, `self_chain`,
  `record_self_event`, `classification_history`, `_quarantine_to_boundary`,
  `inject_and_evaluate_novelty` **[verified]**).  Treat the MIGRATION docs as
  historical intent — or execute them.  **[verified]**

### 1.5 Test coverage
* `tests/` holds only the T58–T64 spring suite (10 tests).  No test for the
  T-series, the manifold library, or the engine.  The T55-series experiments
  are self-verifying prints, not regression tests.

### 1.6 Orphaned/hygiene gaps
* `scripts/` is gitignored NodeDefense code from another project.  Its
  `config.yaml` has a real TODO: `novelty_threshold: null # TODO: Set via
  empirical fit from golden_set.npy` — and **`golden_set.npy` does not exist**.
* **`scripts/start.ps1` contains live credentials** (Bluesky + Groq API key).
  Currently gitignored, but it must be scrubbed before the repo is ever shared.
* `web_data.json` exists twice with identical MD5: `Universals/` (served by the
  dashboard) and `data/` (dead copy).
* **NEW 2026-08-02:** `c0_law_data.json` exists twice with identical MD5:
  `data/` and `Universals/` — same duplicate-class as `web_data.json`.  The
  producer (`generate_c0_data.py`) writes the `Universals/` copy; the `data/`
  copy is a dead duplicate.  (Also: 6 data files have no in-repo producer
  script — `googol_census.json`, `mersenne_m52_bridge.json`,
  `mersenne_prime_5630.json` are produced by gitignored `scripts/`;
  `epoch_0d.json` and `calibration_probe_data.json` are probe artifacts written
  by external/one-off scripts — all claimed via git history or README, not
  orphaned.)
* No CI, no lockfile.  `pyproject.toml` + `puno` CLI exist (recent).
* README quickstart implies `math_validation.py` at root; it lives in
  `Universals/`.  The "142/147 validations pass" count is unverified here —
  `dependency_tree.dot` has 86 edges, `Universals/math_validation.py` has 37
  test functions.  **[claimed; count via `run_all.py`]**

### 1.7 Documented inconsistencies (fixable) — **RESOLVED 2026-08-01**
| Item | Value A | Value B | Resolution |
|---|---|---|---|
| PAPER.md test count | 88 (abstract) | 109 (conclusion) | Unified on **109**; abstract now cites §9 and notes unification. `run_all.py` was found to have a path bug (relative path doubled under `cwd` — all 20 steps failed before starting) and is **now fixed**; a full re-count is pending a fresh run. |
| PAPER.md ground state | E₀ = 5.84 | E₀ = 5.58 | **5.84 is correct** (`spectral_data.json` eig[0] = `thermo_data.json` ground_state = 5.843778304934855; r = 2.365 → λ = ¼ + r²). PAPER edited to 5.84. |
| `internet_net.pkl` size | 3.02 GB (THE_BOOK) | 3.17 GB (DECENTRAL_NET) | Actual 3,172,999,165 B = **3.17 GB**. THE_BOOK corrected. |
| README validation count | 142/147 | actual | Reran `math_validation.py`: **192 PASS, 0 FAIL**. README updated. Also fixed the script's UnicodeEncodeError on Windows consoles (stdout reconfigured to UTF-8). |

### 1.8 New inconsistency found 2026-08-02 — **PAPER Bekenstein claim vs persisted data**
| Item | Value A | Value B | Resolution |
|---|---|---|---|
| Bekenstein shift | PAPER.md: η_prime=0.1336, η_random=0.1285, Δη **+3.9%, p=0.002** | `data/bekenstein_shift_data.json`: control p=0.789 (+2.5%), dissipative p=0.938 (−0.1%), interpretation "no systematic difference"; claimed numbers absent | **RESOLVED 2026-08-04 — claim withdrawn.** PAPER §8.7 + conclusion #5 rewritten to report the null (control p=0.789, dissipative p=0.938); old numbers explicitly withdrawn as not reproducible. A fresh pre-registered n≥60 run remains the only way the effect could be claimed again. |

### 1.9 External prior-art cross-reference — **US7284987B2 (verified 2026-08-04)**
* McGrath's "Physical Quantum Model for the Atom" (US7284987B2, Elemetric LLC,
  granted 2007, **expired fee-related 2024-04-24** → public domain) is
  cross-referenced in PHYSICAL_UNIVERSAL_MAP §11.  Full analysis in
  `docs/US7284987B2_ANALYSIS.md`.  Key findings: all 17 claims recite a
  *physical teaching model* (class G09B23/20); **no overlap** with the repo's
  computational/mathematical claims.  Of the patent's own numbers: C(6,4)=15
  reproduces, the mass-radius ratios reproduce (1105/85 = 325/25 = 13;
  36:60:108 = 3:5:9), but the claim-2 geometry (15 axes at equal angle
  arcsin(⅓) ≈ 19.47° in R⁶) **does not** reproduce from the stated coordinate
  construction, and the gravity/EM ratio 9.39e-39 matches α_G ≈ 5.91e-39 only
  to within 1.6×.  **[verified: reproducible numbers re-computed; geometry
  claim flagged as illustrative, not established]**

---

## 2. CONJECTURES (explicit)

1. **Prime geodesic theorem with sieve suppression** (README): π_k(L) ∼ ε_k·e^L/L
   — "conjectured to obey."  Data limit L ≤ 229 vs required L ≫ 300.  Whether the
   framework extends beyond 2ⁿ−k to arbitrary primes is declared open.
   **MEASURED 2026-08-08** (`experiments/pgt_finite_l.py`,
   `data/pgt_finite_l_data.json`): at finite L the sieve ordering is only PARTIAL
   (Pearson r=0.696, Spearman 0.816), and the growth form is REFUTED — slope of
   log π_k vs L is 0.002 vs the predicted 1.0 (r²=0.043); π_k grows like ln L
   (one candidate per n), so ε_k·e^L/L overpredicts the observed 186 primes by
   ~95 orders of magnitude at L=200.  The literal README conjecture is falsified
   at finite L; the PGT asymptotic (L ≫ 300) is out of reach of the googol
    census (n_max = 332) and would need the full X(1) geodesic spectrum, not the
    single C7 progression.  The "extends beyond 2ⁿ−k" sub-question is
    **RESOLVED 2026-08-08** (`experiments/bridge_extension.py`,
    `data/bridge_extension_data.json`): every prime p has the unique
    representation p = 2ⁿ − k, so the bridge extends trivially; over 5.76M
    primes ≤ 10⁸ the near-integer(0.01) rate is 2.437% vs 2.263% on a matched
    random-integer bridge control (z=19.5, 0.17pp prime residue bias) and vs
    the 2% uniform-fractional null; the census's own 6/186 resonances are
    not significant (p=0.17, ~3.7 expected).  Nothing 2ⁿ−k-special.
2. **Selberg paradigm** (PAPER): the finite-disk spectrum (30 eigenvalues)
   "suggests" a concrete instance of Selberg's framework; the eigenvalues ↔
   Riemann-zero correspondence is "conjectured" — and explicitly undecidable at
   30 eigenvalues (GUE/Poisson discrimination impossible).
   **RESOLVED 2026-08-08** (`experiments/selberg_paradigm.py`,
   `data/selberg_paradigm_data.json`): now decidable at 100 modes.  (a)
   GUE/Poisson discrimination is **DECIDED toward Poisson**: ⟨r⟩=0.374 ± 0.029
   (se), z(Poisson)=−0.42, z(GOE)=−5.55 — the 30-mode "intermediate 0.460"
   was a small-sample fluctuation; a chaotic (GOE) surface signature is
   excluded at 5.6σ.  (b) Eigenvalues ↔ Riemann zeros: min distance 7.10,
   0 of 100 within 0.5 — **no correspondence**.  (c) Selberg trace-formula
   length spectrum: the spectral form factor C(ℓ)=Σ cos(t_j·ℓ) at the 186
   Mersenne census lengths is inside the random-length null (mean percentile
   18.8, 0/186 above the 95th-pct null max) — the 196 Mersenne "geodesic
   lengths" produce **no trace-formula oscillation**.  Overall: the paradigm
   is **not supported as a concrete instance**; the earlier ε(2)=0.000265
   "unification" was the code's own construction (`L(s)=C₀·ζ(s)` tautological),
   not a measured spectral-geometric match.
3. **BOOK V pedagogy** (THE_BOOK): misconception = weak solution; creases =
   threshold concepts; C₀ = prior knowledge.  Preface says plainly: "the
   pedagogy has not been validated on learners."  **[verified: self-declared]**
4. **Four testable predictions, never executed** (PHYSICAL_UNIVERSAL_MAP §10.1):
   (i) recurrence time scales with entropy; (ii) T-symmetry of the loss
   landscape; (iii) holographic compression ratio (1,536 → 2); (iv) CTC/self-chain
   fixed point at 10⁶ iterations.  None has a dedicated experiment.
   **RESOLVED 2026-08-02 — T65 four-pack executed: 0.5/4 confirmed.** P1 is a
   tautology (τ := exp(entropy) in source, `curiosity_drive` has zero effect);
   P2 refuted (recon err ≈ 1.8); P4 refuted (converged fraction 0.0); P3 weakly
   positive but synthetic (MI 0.034 vs null 0.009, constructed latent).  See
   `data/t65_fourpack_results.json`, WEAVERS_SCRIBE Ch. 5.9.
5. **Golden-ratio closure mechanism** (SPRING_BIBLE/T58): the fold "closes to
   r = apex·0.6138" — measured, but the *reason* the closing radius is set by
   the crease is asserted, not derived.
   **DERIVED 2026-08-08** (`experiments/fold_golden_closure.py`,
   `data/fold_golden_closure_data.json`): r_ret/apex = 0.6137690167 is exactly
   θ*/Θ solving s(θ*)/s(Θ) = 1/φ² on the Archimedean spiral r = aθ with arc
   length s(θ) = (a/2)(θ√(1+θ²) + asinh θ), at Θ = 20 — delta 0.0 to the
   measurement.  The ratio → 1/φ as Θ→∞ (quadratic limit).  φ enters via the
   construction (an arc-length ratio), not as an independent law.  The distinct
   C2 claim (next fold above the giant locks on a φ or φ² rung) is
   **RESOLVED 2026-08-08 — NOT SUPPORTED** (`experiments/fold_ladder_phi.py`,
   `data/fold_ladder_phi_data.json`): the retrace chain
   943,901,200,001 → 1,914,467 → 730,421 → 26,102 → 10,262 has only **1/4
   adjacent rungs** within 1% of {φ, φ²} (the celebrated upper 1,914,467/730,421
   = 2.621046, 0.115% from φ²); the other rungs are 493,036, 27.98, 2.5436.
   A magnitude-matched Monte-Carlo null (5 ints log-uniform in [1e4, 1e12],
   2e5 draws) gives expected 0.037 golden rungs/chain and P(≥1 hit) = 0.036,
   so an isolated hit is coincidence-scale, not a ladder.  The "next fold
   above the giant" is undefined — the giant is the chain's largest member and
   the defined rung touching it (943,901,200,001/1,914,467 = 493,036) is far
   from golden.  This retires the last open §2 item.
6. **"Golden metric" hypothesis** (`fibonacci_squares.py`): a metric where the
   log-spiral is geodesic — later confirmed *exactly* for the cusp metric by
   T39/golden_survey, so this one is effectively resolved.
7. **Spectral C1 (E₁-dozenal) / C3 (Mersenne-λ) / C4 (intermediate statistics)**
   (WEAVERS_SCRIBE Ch. 5.1): recomputed 2026-08-08 at 100 modes on a 120×120
   grid (`experiments/spectral_extended.py`, `data/spectral_extended_data.json`):
   **C1 PARTIAL and resolution-dependent** — r_k ≈ ln k hits at k=12 (2.4982 vs
   ln 12 = 2.4849, 0.53%) and k=26 (0.96%) but misses at k=10 (3.3%) and k=2000
   (7.5%); **C3a NOT SUPPORTED** (no mode near λ(7)=4.574 below the floor —
   nearest is E0, Δ=1.34); **C3b SUPPORTED** (mode 12.2416 vs λ(31)=12.261,
   Δ=0.0197); **C4 decided toward Poisson** — ⟨r⟩=0.372 at 100 modes vs Poisson
   0.386 / GOE 0.536, so the T19 "consistent chaos" spectral signature is
   refuted at level-spacing level (for this finite-disk analog).  The WEAVERS
   eig[5]=12.060 claim is NOT reproducible from `data/spectral_data.json` (which
   holds 8.5406).

---

## 3. OPEN THEORETICAL QUESTIONS

* **Wheeler–DeWitt on the disk** (PUM §10.5.1): "can an analogue of the
  Hamiltonian constraint select 'physical' knowledge configurations?"
  **RESOLVED 2026-08-08** (`experiments/wheeler_dewitt_selection.py`,
  `data/wheeler_dewitt_selection_data.json`): the constraint selects nothing.
  The unshifted filter |H(q,p)| = |K+V| < ε is **empty** on conservative flow
  (H = C₀ ≈ 24 ≫ any meaningful ε; nonzero only at ε ≥ 10 = 42% of C₀); the
  shifted filter |H−C₀| < ε is the C₀ law relabeled — fraction is 1.000 at
  every ε for the origin-start trajectory and jumps 0→1 at the integrator
  drift level otherwise.  The PUM's "86.8% satisfied at ε=0.5" is **not
  reproduced** (grid max 1.000; the filter reads only 0 or 1) and is at best
  a finite-precision drift number, never a selection of "physical" states.
* **Fold-and-cut as discrete unitary evolution** (PUM §10.5.2): "whether
  fold-and-cut realizes unitary gates — remains open."
  **RESOLVED 2026-08-08** (`experiments/fold_unitary.py`,
  `data/fold_unitary_data.json`): the mirror fold r = a·min(θ, 2Θ−θ) is
  **not** a unitary gate.  It is non-injective — 400/801 grid angles collide
  (θ and 2Θ−θ map to the same radius; a generic mid-branch point has 2
  preimages), so it has no well-defined inverse — and it does not preserve
  arc length (L_fold/L_dev = 0.504).  Unitarity requires a bijective,
  norm-preserving map; the fold is a many-to-one projection that re-scales
  metric content.  If a discrete-unitary analogue exists, it is not the
  fold map itself.
* **Kawasaki analogue as a CTC/Novikov constraint** (PUM §10.5.3) —
  **RESOLVED 2026-08-08** (`experiments/kawasaki_ctc.py`,
  `data/kawasaki_ctc_data.json`): the antecedent is false.  The exact 2-line
  angle-sum criterion is satisfied by 9.5% of ReLU fold vertices vs an 8%
  uniform-angle null — a constraint satisfied at the background rate
  constrains nothing; the V-vertex admitted fraction (0.095)^V collapses
  exactly as fast as the null (0.08)^V, so it cannot limit which causal loops
  are self-consistent.
* **Kawasaki constraint** (PUM §10.2): mean deviation **0.49** from target 0 —
  a measured *failure*, called "genuine open problem."
  **RESOLVED 2026-08-08 — refutation + artifact attribution.**
  `experiments/kawasaki_null.py`, `data/kawasaki_null_data.json`: the 0.4866 /
  72.4% numbers reproduce exactly, but the diagnostic collects ~700 rays per
  vertex (a dense point cloud, not crease rays); the uniform-scatter control
  gives 0.835 / 52.0%, and the exact 2-line ReLU fold-vertex criterion
  |4α−2π| fails generically (mean 3.21, 9.5% within ε=0.5 vs an 8% uniform-angle
  null).  The 0.49 is a sampling-statistic scatter of the line-structured
  point cloud, not a near-miss of flat-foldability — ReLU fold vertices are NOT
  flat-foldable (a codimension-1 condition, zero only at perpendicular
  crossings).
* **Retrace boundary condition** — **RESOLVED by T64** (viscosity-selected cut
  locus).  **Fold theorem** — **RESOLVED by T63** (eikonal/viscosity).  Both
  should be treated as closed, not open.  **[verified]**
* **PUM §10.1 (i)–(iv)** — **RESOLVED by T65 2026-08-02, 0.5/4.** (i) circular,
  (ii) refuted, (iii) synthetic-weak, (iv) refuted.  See §2 conjecture 4 and
  §4.  The PUM's narrative cosmology should no longer be cited as verified
  beyond the specific engine claims that survive testing.
* **Prime-metric framework beyond 2ⁿ−k** (README).
  **RESOLVED 2026-08-08** (`experiments/bridge_extension.py`,
  `data/bridge_extension_data.json`): the bridge extends **trivially** —
  every prime p with 2ⁿ⁻¹ < p < 2ⁿ has the unique representation p = 2ⁿ − k
  (k = 2ⁿ − p), so λ = ¼ + (n·ln2 − ln k)² is defined for every prime.  Over
  all 5,761,455 primes ≤ 10⁸ the near-integer(0.01) rate is **2.437%** vs
  2.263% on a matched random-integer bridge (uniform k per n-bin; z=19.5,
  a 0.17pp prime residue bias) and vs the 2% uniform-fractional null.  The
  census's 6/186 "spectral resonances" (3.23%) are **not** significant on
  their own (binomial p=0.17; ~3.7 expected under uniformity), and the
  k<30-restricted subsets (4/85 = 4.7%) are also within noise (p=0.09).
  Verdict: the near-integer "resonance" is bridge arithmetic on any integer
  near a power of two plus a small prime bias — there is no special 2ⁿ−k
  content, and the framework does extend, but with nothing distinctive.
* **Prime-time claims** (PAPER §8.4): C0 at every prime-indexed state; prime
  geodesic spectrum μ=0.065/σ=0.058 at N=50; recurrence times factor like
  random integers.
  **RESOLVED 2026-08-08** (`experiments/prime_time.py`,
  `data/prime_time_data.json`): (1) the "C0 law at primes" is *uniform energy
  conservation* — drift at prime steps equals drift at every step (ratio
  0.999), nothing prime-special; (2) the geodesic spectrum is concentrated
  only inside the first N≈50 states (μ=0.0270/σ=0.0224 at N=50, consecutive
  steps μ=0.0135 — not the claimed 0.065/0.058), and diverges to μ=1.006/σ=
  0.797 by N=214; (3) the recurrence-time claim is **unmeasurable**: the
  frictionless flow escapes the bounded disk (r ≥ 0.9) after ~1310 steps with
  **zero** near-recurrences, so there is no return-time distribution to
  factor.  All three claims were asserted on a transient that exits the
  Poincaré disk.
* **T-symmetry error 0.003** (PAPER, L.O.R.E. section): the reversal error is
  quoted as a fixed constant.
  **RESOLVED 2026-08-08** (`experiments/time_reversal_convergence.py`,
  `data/time_reversal_convergence_data.json`): it is a *dt-dependent
  integrator bound*, not a physical symmetry claim — measured reversal error
  8.9e-3 at dt=5e-4, 7.2e-5 at dt=2.5e-4, 5.9e-7 at dt=1.25e-4, superconverging
  as O(dt^6.9) near the symmetric origin crossing (order-2 leapfrog lower
  bound; the coarsest dt=1e-3 window exits the disk, r=0.99).  The 0.003 is
  consistent with dt≈5e-4 — fine, but it is a numerical bound, not an exact
  symmetry.
* **Continuum limit**: PAPER's "residual drift is numerical and converges to
  zero as dt→0" is anticipated, not measured at arbitrary precision.
  **MEASURED 2026-08-08** (`experiments/continuum_limit.py`,
  `data/continuum_limit_drift.json`): dt-halving at fixed T=1.0 on the interior
  trajectory (Q0=(0,0)) shows first-order convergence — drift 5.44→0.42 over
  dt 4e-3→2.5e-4 with order 0.925 (r²=0.9991); a clean interior trajectory
  (Q0=(0.3,0), T=0.25) gives order 1.040, drift → 0 to 3.7e-4.  The residual
  is a boundary effect: trajectories that hit the r=0.99 projection clip
  accumulate a per-hit non-conservative floor (0→48 hits as dt shrinks).
  Verdict: PASS first-order convergence for interior trajectories; the
  boundary projection sets a non-conservative floor.
* **Bekenstein re-run (n ≥ 60)**: the PAPER once claimed a +3.9% shift (p=0.002)
  that its own 30-trajectory persisted data refuted; the PAPER now reports the
  null.  A fresh, higher-power pre-registered run remains the only way to know
  whether the effect exists at all.
  **RESOLVED 2026-08-08** (`experiments/bekenstein_rerun.py`,
  `data/bekenstein_rerun_data.json`, n=100, alpha=0.01, pre-registered): the
  raw frictionless shift IS significant at higher power (+3.39%, paired t
  p≈0, sign p≈0, 95% CI [0.0032, 0.0055]) — the old n=30 run was simply
  underpowered — but the **index-matched control on the same trajectories
  erases it** (matched diff +0.00018, p=0.34, CI includes 0).  The +3.9% is
  a position/index-density artifact (primes cluster at early indices), not a
  primality effect; it is **not** revived.  Residual note: the matched sign
  test stays nominally significant (p=1e-4) after a ~2400× magnitude
  collapse with paired-t p=0.34 and CI ∋ 0 — if anything, an order of
  magnitude below the withdrawn claim and not robust across tests.

---

## 4. THEORIES STANDING (the framework's claims, with strength)

| Theory | Claim | Strength |
|---|---|---|
| **L.O.R.E.** (C₀ determined, not chosen) | C₀ = H(q₀,0), never arbitrary | PAPER: 109 tests; T-symmetry error 3e-3 **of the Hamiltonian integrator** (a trajectory-integration property, distinct from the PUM §10.1.2 "ascent recovers seed" claim, which T65 refutes). 2026-08-08: the 3e-3 is a dt-dependent numerical bound (see `data/time_reversal_convergence_data.json`). |
| **Noether charge Q = H(t) ≈ C₀** | <1% drift over 1000 steps, converges as dt→0 | Measured on 6 trajectories; limit anticipated |
| **Eikonal fold cosmology** (T63/T64) | fold = unique viscosity solution of |r′|=a; retrace = cut locus | **Derived + 10-test regression suite** — the strongest theory in the repo |
| **Golden-ratio closure** (T58 + 2026-08-08) | r_ret/apex = θ*/Θ solving s(θ*)/s(Θ)=1/φ² on the Archimedean spiral | **Derived exactly** (delta 0.0 to the measured 0.6137690167 at Θ=20; → 1/φ as Θ→∞). `data/fold_golden_closure_data.json` |
| **Kawasaki flat-foldability of ReLU vertices** (2026-08-08) | the 0.4866 "genuine open" deviation is a point-cloud sampling artifact; ReLU fold vertices are NOT flat-foldable | **Refuted as a near-miss, attributed to sampling** (mean |4α−2π|=3.21, 9.5% within ε=0.5 ≈ uniform null; control 0.835/52.0% vs corpus 0.4866/72.4%). `data/kawasaki_null_data.json` |
| **Clock-test canon** (T59/T61) | laws live in invariants, not conventions | Measured 1.000→0.417→1.000 |
| **Anomaly doctrine** (T55j) | novelty works; impersonation partial; observation bank required | Measured, incomplete by its own verdict |
| **Arithmetic Bekenstein shift** (PAPER) | η_prime=0.1336 vs η_random=0.1285, Δη +3.9%, p=0.002 | **REFUTED by the persisted data file, and withdrawn from the PAPER (2026-08-04).** `data/bekenstein_shift_data.json` (30 trajectories) shows no systematic difference: control p=0.789 (+2.5%), dissipative p=0.938 (−0.1%); the file's own interpretation is "no systematic difference"; the claimed numbers 0.1336/0.1285/p=0.002 appeared nowhere in it. PAPER §8.7 + conclusion now report the null. **n=100 pre-registered re-run (2026-08-08, `data/bekenstein_rerun_data.json`) settles it:** the raw frictionless shift becomes significant at power (+3.39%, p≈0) but an index-matched control on the same trajectories erases it (+0.14%, p=0.34), i.e. the effect is positional (prime indices cluster early), not primality. The claim stays dead; the null is now causal, not just underpowered. |
| **Selberg unification** (PAPER) | 30 eigenvalues ↔ 196 Mersenne geodesics, ε(2)=0.000265 | ε(2)=0.000265 is real **but it is algebra**: `L_total = L_traj + Σ L_k` is the code's own construction (`L(s)=C₀·ζ(s)` is flagged tautological in the code). Spectral-vs-zeros match is poor (code: min |t_n − t_zeta| ~ 2.5–9.0 "not a match by any standard"). **Closed 2026-08-08** (`data/selberg_paradigm_data.json`): at 100 modes the spectrum is **Poisson** (⟨r⟩=0.374, GOE excluded at 5.6σ), zero-correspondence absent (min dist 7.10, 0 within 0.5), and the 186 Mersenne lengths show no spectral-form-factor peaks — not a concrete Selberg instance. |
| **Partition function match** (PAPER) | L(2)=40.14 vs C₀·π²/6=40.19 (<0.2%) | **Tautology.** C₀·π²/6 = 40.1936 holds for *any* C₀; the code flags `L(s)=C0*zeta(s)` as a tautology "for ANY constant C0." A match by construction is not a test. |
| **Thermodynamics/entropy** | ln-thinning ↔ entropy; second law as folding | Analogical, not falsifiable as stated |
| **Prime geodesic spectrum** (PAPER §8.4, 2026-08-08) | prime-indexed states define a geodesic spectrum mirroring the arithmetic of primes; recurrence times factor into primes | **Not supported.** C0-at-primes = uniform energy conservation (ratio 0.999); the spectrum is a transient of the first N≈50 states (μ=0.027, not 0.065) and diverges by N=214; the frictionless flow has **zero** near-recurrences before escaping the bounded disk, so the recurrence claim is unmeasurable. `data/prime_time_data.json` |
| **T-symmetry of the integrator** (PAPER/L.O.R.E., 2026-08-08) | reversal error 0.003 | A **dt-dependent numerical bound, not a physical symmetry** — superconverges O(dt^6.9) near the origin crossing (8.9e-3 → 5.9e-7 over dt 5e-4→1.25e-4). `data/time_reversal_convergence_data.json` |
| **PUM §10.1 four-pack (T65)** | P1 τ~entropy; P2 T-symmetry; P3 holographic MI; P4 CTC fixed point | **0.5/4 confirmed.** P1 = tautology (τ := exp(entropy) in source); P2 refuted (recon err ≈ 1.8); P4 refuted (converged fraction 0.0); P3 weakly positive (MI 0.034 vs null 0.009) but synthetic. See `data/t65_fourpack_results.json` |
| **Decentral Bank (T68)** | routing is ownership; double-entry ledger + nonce rejects double-spend; witness quorum catches faulty transfers; anomaly layer flags outliers | **New, measured.** T1–T6: routing deterministic with a real partition spread (min 6 / max 111 / σ 34 over 16 fragments); integrity conserved exactly over 3000 txs; nonce replay rejected; 30% damage survives; quorum catches *every* faulty send below 40% corruption while honest availability holds — but collapses at ≥50% corrupt neighbourhoods (caught-frac 1.0 → 0.23–0.27), i.e. **quorum is majority honesty, not BFT** (crease #16). Anomaly recall 0.51 / precision 0.63 vs random null 0.019. Addresses the AUDIT §1 "no ledger/consensus/transaction layer" gap at toy scale. See `data/decentral_bank_data.json` |
| **Decentral Bank hardened (T68 Ph.1) + bridge (T69)** | Ed25519 account signatures verified at append & re-validation; WAL persistence + replay; on/off-ramp against a centralized bank via a custody-holding gateway | **New, measured.** T7: tampered block, wrong-key signature, and address-spoof all rejected, legit tx still commits. T8: save/load reproduces bit-identical heads + conserved balances. T69: on-ramp credits DCN 1:1, off-ramp pays fiat 1:1; ref replays settle nothing twice; backing invariant `custody + reserve_DCN == initial` holds to diff 0.0 under 300 randomized ops with 170 ref replays and forged over-withdrawals rejected. Honest walls: single-key custody (no threshold/HSM), mock bank (no network/TLS/KYC/AML), caller-supplied refs, no compensation path (crease #17). See `data/decentral_bank_bridge_data.json` |
| **Decentral Bank network (T70) + crash (T71) + sockets (T16/T17) + total-loss WAL (T18)** | every fragment a real OS process; PROPOSE→VOTE→COMMIT→NOTIFY first over a controllable relay, then over real TCP loopback sockets; replicas + SYNC/RESYNC; partition/equivocation/forgery/crash tests; per-node append+fsync WAL | **New, measured.** T12: 23 txs commit over real messages, all nodes' replicas bit-identical, replay conserves. T13: ring cut in two — 12–14/16 commit within halves, post-rejoin RESYNC converges to identical ledgers. T14a: forged block rejected at rate 1.0. T14b: scattered corruption collapses honest commits along the majority-honesty prediction P(f)=(1−f)⁴+4f(1−f)³ (four runs spanned {0.95–1.0, 0.56–0.63, 0.20–0.40, 0.0–0.13} at f={0,0.3,0.5,0.7}, theory {1.0, 0.65, 0.31, 0.08}; fluctuates run-to-run with relay timing but tracks theory) — crease #16 reproduced across processes — while *contiguous* corruption at f=0.7 keeps 0.25–0.67 (crease #18: corruption geometry, not just quantity, decides the quorum). T14c: partition equivocation creates a double-spend window; the fork is detected after rejoin, not healed. T15: a killed node's own accounts cannot transact while it is down (0/3) yet 8/8 live-owner commits survive; a STATELESS restart recovers every fragment — own included — from peers' replicas, re-converges, and commits a fresh tx. T16a/T16b: the same guarantees over REAL TCP sockets (no relay) — 14/14 commit, bit-identical replicas, partition re-converges. T17: a socket-killed node freezes its own accounts (0 commits) while live owners keep committing (k−1 > half witnesses), and a stateless socket restart rebuilds every fragment and commits again (crease #20: readiness must be quorum-attainable, not fabric-complete). T18: TOTAL simultaneous kill — every replica gone from memory, only each node's OWN chain survives on its fsync'd WAL; restarting WAL-loads the own chains and the ring reassembles every fragment from its owners; post-rebuild heads/block-counts match pre-crash exactly, converged, valid, conserved, fresh tx commits (crease #21: replicas are caches; the own WAL is the durability floor for total loss). T19: the whole socket layer wrapped in MUTUAL TLS (shared self-signed identity, CERT_REQUIRED both ways) — a client without the identity is rejected at the handshake and can exchange no bytes, yet 14/14 commit, replicas bit-identical, and a crash+restart re-establishes the encrypted fabric and re-converges. T20: host parameterized and the same consensus + TLS run over the machine's real LAN NIC (192.168.100.241) — 14/14 commit, bit-identical replicas, crash+restart re-converges over the NIC; transport proven beyond loopback. Still majority-honesty, not BFT; real mutual-TLS over a LAN NIC but one machine — no true two-host transport, one shared test identity (no per-node PKI); an OS crash mid-commit could tear the log. See `data/decentral_bank_net_data.json` |

---

## 5. RECOMMENDED NEXT MOVES (ranked effort→value)

1. **Fix the five verified inconsistencies** (PAPER 88/109 + E₀, pkl size, README
   paths) — minutes, removes noise from every future reading.
   **DONE 2026-08-01** — all five resolved (§1.7 table): test count unified on
   109, E₀ = 5.84 confirmed correct, pkl size 3.17 GB, `run_all.py` path bug
   fixed, validation re-count 192 PASS / 0 FAIL.
2. **Execute the four PUM testable predictions** as a T65 four-pack (quick,
   local, closes §2.4) — the cheapest way to convert "conjectures" into
   measured facts, matching the project's own doctrine. **DONE 2026-08-02 —
   0.5/4 confirmed; P2 and P4 refuted, P1 tautological, P3 synthetic. See Ch.
   5.9 of WEAVERS_SCRIBE + `data/t65_fourpack_results.json`.**
3. **Correct the Bekenstein claim (NEW, from §1.8)** — the PAPER's
   Δη +3.9% p=0.002 is contradicted by its own persisted data (p=0.789/0.938).
   Either edit PAPER to report the null, or run a fresh n≥60 Bekenstein
   analysis.  Highest value: this is a live contradiction in a *claimed*
   result, not a hygiene item.  **DONE 2026-08-04 — PAPER §8.7 + conclusion
   #5 edited to report the null; old numbers withdrawn.  A fresh pre-registered
   n≥60 run remains optional and would be the only way to claim the effect
   again.**
4. **Scrub `scripts/` credentials** (and either delete or quarantine the orphan)
   before the repo is shared.
   **DONE 2026-08-08** — a repo-wide scan of tracked files found **no secret
   patterns** (no JWTs, API keys, AWS keys, private keys, or passwords in any
   tracked `.py/.json/.yaml/.ps1/.md`).  The one live credential found was
   `scripts/cert.pem` (an Argo tunnel token) — it was **untracked and
   gitignored** (never in git history), and has been **quarantined** to
   `%TEMP%\opencode\cert.pem.quarantined`.  `scripts/start.ps1` holds only
   literal `<REDACTED>` placeholders.  The remaining `scripts/*` orphans
   (canary.py, controller.py, gossip.py, node.py, telemetry.py, etc.) are
   untracked and gitignored; the four tracked scripts (deep_sieve,
   genesis_prime, next_k3_sieve, googol_census) are clean.
5. **Observation bank (T66)** — the declared-required capability; the one gap
   with genuine new science.  Needs an external data source (ASN/TLS/WHOIS) —
   network-bound.
6. **O(1)-per-neuron spatial search (T67)** — the declared next build; the one
   that unlocks flowing 1.9M sites.  Significant engineering.
   **DONE 2026-08-04** — `DecentralNet(use_index=True, index_min_n=512)`:
   a numpy-only uniform-grid k-NN for dim ≤ 3 (cells sized for ~k points,
   Chebyshev ring grown until the k-th candidate is provably closer than any
   unscanned cell — min distance to a ring-(r+1) cell is ≥ r·cell — so results
   are EXACT, only the expected work is O(1)) and scipy.cKDTree
   (`workers=-1`) for dim ≥ 4.  `experiments/decentral_net_t67.py` verifies:
   indexed flow is bit-identical to all-pairs flow (2D grid and 64D tree),
   spacing/predict match, grid kNN == brute force across 3 seeds × 1D/2D/3D,
   measured 2D exponents exact 1.88 vs indexed 1.02, and flows n=100,000 2D
   (~5 s/step; all-pairs D = 160 GB, physically impossible) and 10,000 real
   top-1M domain embeddings in 128-D (~2 s/step; all-pairs D = 102 GB).
   `data/decentral_net_t67_data.json` is the verdict artifact.  Honest
   boundary: high-dim k-d trees degenerate on dense data (~2–16 s/step at
   n=10k×128D), so high-dim indexed flow stays ~10⁴; the low-dim grid (the
   live daemon's geometry) flows 10⁵+ on one box.
7. **Either execute or retire MIGRATION** — currently a dead-but-authoritative
   doc; mark superseded to stop future confusion.
   **DONE 2026-08-08** — both `docs/MIGRATION.md` and `docs/MIGRATION_1.md`
   already carry STATUS: SUPERSEDED banners (v2 engine never migrated; live
   work is `Universals/engine.py` v1), and no tracked doc cites either as
   authoritative (the only reference is this AUDIT entry).  Retired.
 8. **Regression coverage for the T55 series + library** — the experiments print
    results but nothing pins them.  (T65 was the first probe to ship a JSON
    verdict; make that the norm.)  **PROGRESS 2026-08-08** — the
     solvable-theorem pattern is now the norm: 59 verdict experiments
     (`prime_time`, `time_reversal_convergence`, `bekenstein_rerun`,
     `wheeler_dewitt_selection`, `fold_unitary`, `kawasaki_ctc`,
     `bridge_extension`, `selberg_paradigm`, `fold_ladder_phi`,
     `flow_hierarchical`, `flow_active_learning`, `balance_survey`,
     `balance_scale`, `balance_continual`, `polysphere_extensions`,
     `flow_incremental`, `flow_hier_incremental`, `polysphere_use_cases`,
     `polysphere_routing`, `golden_survey`, `fib_stream`,
     `hamiltonian_routing`, `metric_comparison`, `c0_crossing_tsym`,
     `c0_cusp_flow`, `t39_cusp_flow`, `van_iterson`, `reverse_pair_gaps`,
     `fibonacci_spiral`, `prime_count_from_scratch`, `fibonacci_squares`,
     `rotation_test`, `clock_test`, `spring_fold`, `eikonal_fold`,
     `retrace_boundary`, `fold_optimizer`, `t65_fourpack`,
     `phi_scheduler`, `flow_regularized`, `flow_hier_reg`,
     `flow_hier_reg_scaled`, `balance_auto`, `self_balancing`,
     `polysphere_mnist`, `polysphere_nnflow_viz`, `decentral_net`,
     `decentral_net_mnist`, `decentral_net_continual`,
     `decentral_net_ceiling`, `decentral_net_t67`, `decentral_net_live`,
     `bazaar_hybrid`, `bazaar_net`, plus the five
     earlier probes)
     each ship a claim/verdict JSON and are pinned by
     `tests/test_solvable_theorems.py` (59 tests; full suite 249).  The
     bazaar_hybrid verdict now covers six structural claims (C1 brigade
     threshold, C2 spam, C3 feed, C4 archive, C5 quorum, C6 verified-vote-only
     membership).  The
     bazaar_net verdict (2026-08-11) then runs the bazaar as a REAL network —
     4 node processes on the T70 socket transport (optional mutual TLS)
     replicate every action into bit-identical content-addressed LedgerChain
     archives; N1 content replicates across nodes, N2 the emergent mesh feed
     routes the minority user to its own community, N3 removal is
     standing-gated and quorum-confirmed (sockpuppet standing 0.00 contributes
     nothing, a fabricated brigade on a standing author is rejected where a
     central 3-flag rule removes), N4 the archive is tamper-evident at the
     flipped sequence, N5 the network survives node death with stateless
     restart resync to a bit-identical chain (honest walls: driver-sequenced
     ordering needs a distributed total-order primitive in a real network;
     majority-honesty quorum, not BFT).  The
    broad `experiments/` scripts (remaining flow, balance, polysphere,
    decentral) still
    print without persisted verdicts — extending the JSON verdict norm to
    those is the remaining work here.

---

## 6. BOTTOM LINE

The strongest engine claims (fold derivation, clock test, anomaly doctrine,
scaling law) remain reproducible.  But the sweep on 2026-08-02 moved three
items from "claimed" to **refuted/tautological**: **(a)** the Bekenstein shift
is contradicted by its own persisted data file (p=0.789/0.938 vs claimed
p=0.002); **(b)** the partition-function match and **(c)** the Selberg
L-function unification are tautologies by the code's own admission; and the
T65 four-pack executed the last four explicit predictions at **0.5/4**
(P2, P4 refuted).  On 2026-08-02 T68 shipped the first value-carrying layer
(a fragment bank: hashed double-entry ledgers, nonce double-spend rejection,
witness quorum, amount-outlier anomaly) — **T1–T6 all honest verdicts**, with
the quorum's own wall measured: majority-honesty-in-a-neighbourhood, not BFT
(crease #16).  It was then hardened and bridged on the same day: **Ed25519
signatures** verified at append and re-validation (T7: tamper, wrong-key, and
address-spoof all rejected), **WAL persistence + replay** (T8: save/load
bit-identical), and the **T69 on/off-ramp** to a mock centralized bank whose
backing invariant holds to diff 0.0 under ref replays and forged withdrawals —
with the honest wall that the trust boundary moved to a single-key custody
gateway, not to a protocol (crease #17).  On the same day the last simulation
limit of the bank was closed: **T70** runs every fragment as its own OS
process and drives PROPOSE→VOTE→COMMIT→NOTIFY through a controllable relay —
T12/T13/T14a/T14c pass, the scattered-corruption wall reproduces crease #16
across processes (four runs spanned {0.95–1.0, 0.56–0.63, 0.20–0.40, 0.0–0.13}
vs theory {1.0, 0.65, 0.31, 0.08}; fluctuates run-to-run, tracks theory), and a
new crease fell out: contiguous corruption is absorbed by the honest cluster's
local witnesses (crease #18) — corruption *geometry*, not just fraction,
decides quorum survival.  **T71** then closed the crash wall: a killed node's
accounts freeze (its authority lives in its own process) while 8/8 live-owner
commits survive, and a fully stateless restart rebuilds every fragment — its
own included — from peers' replicas, re-converges, and commits again.
**T16/T17** repeated the commit, partition, and crash/restart guarantees over
REAL TCP loopback sockets (no relay): T16a 14/14 commit with bit-identical
replicas, T16b partition re-converges, T17 a socket-killed node freezes its
own accounts (0 commits) while live owners keep committing (k−1 > half
witnesses; the block-start gate is quorum-attainable readiness) and a
stateless restart over sockets rebuilds every fragment and commits a fresh
tx.  Socket-layer bugs fixed: `send()` never flushed the current frame to a
live connection, an idle-socket recv timeout was mis-read as EOF (3.4k
connect/EOF reconnect storm), one-shot driver connects missed late-booting
nodes, and a killed predecessor could still hold the port at rebind.
**T18** closed the last crash wall — TOTAL simultaneous loss: with every
replica gone from memory, each node's OWN chain (fsync'd to a T8-style WAL
before the commit is announced) is the only survivor; restarting WAL-loads
the own chains and the ring reassembles every fragment from its owners,
matching the pre-crash heads exactly (crease #21: replicas are caches; the
own WAL is the durability floor for total loss).  **T19** then wrapped the
whole socket layer in mutual TLS: a shared self-signed identity on every
listener and outbound connection with CERT_REQUIRED on both sides — a
client without the identity is rejected at the handshake and cannot
exchange a single byte, yet 14/14 txs commit, replicas stay bit-identical,
and a crash + restart re-establishes the encrypted fabric and re-converges.
**T20** parameterized the host and re-ran the SAME consensus + TLS over this
machine's real LAN NIC (192.168.100.241): 14/14 commit, bit-identical
replicas, chains re-validate, conservation holds, crash + restart
re-converges over the NIC — the transport is proven beyond loopback, on a
real interface with the interface IP in the cert SAN.  A true two-host
deployment (per-node host tables, two boxes) still needs a second machine.
The remaining gaps: **(1)** the observation bank (T66) is the one
declared build still absent (the O(1) search, T67, shipped on 2026-08-04);
**(2)** PGT and
BOOK-V pedagogy remain conjectured; **(3)** the PAPER's Bekenstein claim was
corrected on 2026-08-04 — §8.7 and the conclusion now report the null that
the persisted data always showed (the claimed +3.9% p=0.002 is withdrawn; a
fresh pre-registered n≥60 run would be required to claim the effect again);
**(4)**
hygiene items (orphaned `scripts/` with live credentials, dead doc copies,
MIGRATION superseded-but-present) — **partial 2026-08-08: the live credential
is gone** (`scripts/cert.pem` Argo token quarantined; tracked files scanned
clean — see §5 item 4) and **MIGRATION is retired** (both docs carry SUPERSEDED
banners, no doc cites them — see §5 item 7); dead doc copies remain; **(5)** the network is real mutual-TLS
over the machine's LAN NIC (T20) but still one machine — no true two-host
transport, one shared
test identity (no per-node PKI), consensus is majority-honesty not BFT, an
OS crash mid-commit can tear the WAL, and the bridge still has no threshold
custody, KYC/AML, or regulator.
The honest
headline: the framework's *engine-level* results stand, but its
*arithmetic-selection* and *number-theory* claims (Bekenstein, Selberg,
partition match) are no longer citable as verified — Bekenstein is now
corrected to a null in the PAPER itself.
