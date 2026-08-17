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
   **RESOLVED 2026-08-08, CORRECTED 2026-08-14** (`experiments/selberg_paradigm.py`,
   `data/selberg_paradigm_data.json`): the first 100-mode re-run made three
   statistical errors, fixed here.  (a) GUE/Poisson is **DECIDED toward
   Poisson** with the canonical GOE constant 0.5307 (Atas et al. 2013, not the
   0.536 used before): ⟨r⟩=0.372 ± 0.029 (se), z(Poisson)=−0.50, z(GOE)=−5.50;
   and a KS test of the unfolded spacing distribution now excludes the GOE
   Wigner surmise P(s)=(π/2)s·e^(−πs²/4) at p=0.0034 while being fully
   consistent with Poisson (p=0.744) — the correct ensemble for this real
   symmetric operator (the earlier run's level_spacing_stats tested GUE, β=2).
   (b) The old "min distance 7.10, 0 of 100 within 0.5" was **vacuous**: the
   100 disk modes have t=√(E−¼)∈[2.38, 7.03], entirely below the first zero
   t₁=14.13 (the old code also claimed "first 100 zeros" but only ever used
   the 15 in RIEMANN_ZEROS).  The corrected verdict is: **not testable at this
   scale**, and structural — the capped disk's measured Weyl density is 2.35
   levels per unit E vs the zeros' 0.00456 per unit E at t₁, a factor ≈516, so
   no number of disk modes can reproduce the zeros' spectrum (reaching t₁
   alone needs ≈471 modes, reaching t₁₅≈65 needs ≈9980).  (c) The old
   form-factor test used a **degenerate permutation null** (permuting the same
   186 lengths gives a constant null mean, so "mean pct 18.8" was rounding
   noise and "0/186 strong" was forced) and included the tiny artifact length
   ln(32/29)=0.098 at the C(ℓ)→n_t edge.  The corrected test (matched-bootstrap
   null over the 173 clean lengths ℓ≥1, plus a local-percentile peak test)
   finds **no trace-formula signature**: mean |C| at the 51.7th percentile of
   matched random length-sets, local percentiles averaging 49.4 (50=chance),
   51/173 above the 70% local mark (~52 expected).  Overall: the paradigm is
    **not supported as a concrete instance**; the earlier ε(2)=0.000265
    "unification" was the code's own construction (`L(s)=C₀·ζ(s)` tautological),
    not a measured spectral-geometric match.
    **Sequel 2026-08-14 — decimal (scale-free) perspective**
    (`experiments/riemann_decimal_perspective.py`,
    `data/riemann_decimal_perspective_data.json`): because the absolute scales
    can never meet (disk t∈[2.38,7.03] vs zeros t∈[14.13,236.5]), both spectra
    are "diminished" into decimals on [0,1] via their own counting laws — the
    Riemann-von Mangoldt law N(t)=(t/2π)(log(t/2π)−1)+7/8 for the 100 zeros
    (mpmath.zetazero, matching the 15 in-repo zeros to ~1e−7, so the old
    "first 100 zeros" doc claim is now real), and the measured Weyl line for
    the 100 disk modes.  On the decimal axis the verdict is decisive and
    scale-free: (a) ⟨r⟩=0.611 on the zeros' normalized spacings is **GUE**
    (0.5996, z=+0.6; GOE 0.5307 excluded at +4.1σ — the zeros are a β=2
    system, so the earlier GOE reference was the wrong ensemble for them),
    while ⟨r⟩=0.374 on the disk's is **Poisson** (0.3863, z=−0.4); (b) the two
    normalized spacing sets are mutually excluded (KS p=3.0×10⁻⁷); (c) the
    zeros' decimals are **rigid** — their residual off the ideal grid is 0.225
    mean spacings, 3σ below random decimals — while the disk's (2.00) sit at
    the random level, a ~9× rigidity gap; and the Riemann-von Mangoldt
    residual (the S-term) over the first 100 zeros stays ≤0.998 < 1, within
    its O(log t) bound — consistent with known bounds, but 100 zeros cannot
    test RH.  Same overall conclusion (no shared spectrum), now independent
    of the growing magnitudes.
    **Sequel 2026-08-14 — a condensed technique that locates the zeros**
    (`experiments/riemann_siegel_roots.py`,
    `data/riemann_siegel_roots_data.json`): the decimal-perspective verdict
    no longer needs `mpmath.zetazero` at all.  The instrument evaluates the
    real Hardy Z function, Z(t)=e^{iθ(t)}ζ(½+it), by the Riemann–Siegel
    formula with Gabcke's power-series remainder (C₀…C₄, 5×44 coefficients
    to 50 decimals, transcribed from terry98004/libHGT, MIT) and the exact
    theta via log Γ, then LOCATES the first 100 zeros as sign-changes of Z
    (bisection to 1e−10).  The engine matches |ζ(½+it)| to rel ≤5×10⁻⁵ on
    the critical line, and the found roots agree with `mpmath.zetazero` to
    max 3.1×10⁻⁶ (mean 9.5×10⁻⁸) — 100 zeros reproduced without the oracle.
    Re-running the decimal statistics on the roots the engine found gives
    the SAME numbers as the prior artifact: ⟨r⟩=0.6108 (GUE, z=+0.6), KS
    vs exact-GUE p=0.68, decimal residual 0.225 (−3.0σ below random
    decimals), RvM S-residual max 0.9979 — the decimal-perspective verdict
    is a property of the zeros, not of the lookup.  The technique is the
    **condensation** the previous entry promised: the main sum needs only
    floor(√(t/2π)) terms, never more than 6 anywhere in the first-100-zero
    search (t₁₀₀≈236.5), a per-evaluation 6.3× reduction vs the t/2π
    Euler–Maclaurin count (which this repo measured failing on the critical
    line for t≳30); the window grows as √t (√4.1) while t grows 16.7×.
    Still not a test of RH — 100 zeros cannot probe it.
    **Sequel 2026-08-14 — certified finite verification to g_n = 999.236**
    (`experiments/riemann_siegel_certify.py`,
    `data/riemann_siegel_certify_data.json`): the strongest oracle-free
    claim this repo can make about the critical line — a RIGOROUS, every
    step interval-arithmetic certification that every non-trivial zero of
    ζ(s) with ordinate γ ≤ g_n = **999.236** lies on Re(s)=½ and is simple.
    Two independent ingredients: (a) an interval engine — Z(t) =
    e^{iθ(t)}ζ(½+it) evaluated in `mpmath.iv` by the Euler–Maclaurin
    formula with Backlund's explicit remainder bound (the sum, the
    N^{1-s}/(s−1) term, and the Bernoulli correction are all real interval
    expressions, with the negative-Bernoulli fix `|B_{2M+2}|`) and with
    θ(t) = Im log Γ(¼+it/2) − (t/2) log π computed by its exact
    Stirling/Binet series (the imaginary part of the log-Gamma expansion,
    term-by-term real intervals; NOT `mp.iv.loggamma`, whose libmp wrapper
    is a heuristic asymptotic implementation); the remainder bound uses a
    validated factor 25 (worst observed |R₂₅|/|T₂₆| = 3.8 near the minimal
    term at t≈16, margin ≥ 6.6 over t ∈ [13.5, 1006]). Every enclosure is
    validated to CONTAIN the high-precision mpmath value — zeta and Z at 8
    heights, θ at all 653 Gram points — so a too-tight bound voids the
    certificate, it cannot produce a false positive. (b) Turing's method in
    Brent's form: N_needed = 1 top Rosser block (0.0061 ln²(g_p) + 0.08
    ln(g_p) = 0.84 < 1) certifies N(g_n) ≤ n+1, and the 654 certified
    sign-change brackets give N(g_n) = n+1 = **648** exactly.  All steps
    pass: 654/654 brackets certified simple on-line zeros; certified signs
    of Z at all 653 Gram points g₀..g₆₅₂; containment PASS; RvM
    consistency max |S| = 1; count matches `mpmath.zetazero` (648 == 648).
    The honest wall is explicit in the verdict: this certifies the finite
    range γ ≤ 999.236, it is NOT a proof of RH (open; rigorous verification
    extends to |t| ≤ 3×10¹², Platt–Trudgian).
    **Sequel 2026-08-14 — the de Bruijn–Newman heat-flow face**
    (`experiments/debruijn_newman_condensation.py`,
    `data/debruijn_newman_condensation_data.json`): RH is equivalent to
    Λ ≤ 0 for the de Bruijn–Newman constant, and the certified 648 zeros
    are the t=0 slice of the backward-heat flow H_t(z) = ∫₀^∞ Φ(u)
    e^{tu²}cos(zu)du.  The instrument exposes the *finite* face of Newman's
    "barely so": the closest certified pair's boundary under the local
    quadratic law d(t)² = 4d² + 8t is t_c = −(Δγ)²/2.  Validated first:
    Φ is even (Poisson) to 1.7×10⁻⁵¹ (dps 50); H₀(z) = (1/8)ξ(½+iz/2)
    exactly (rel 0 at z=10, 5×10⁻⁴⁸ at z=55); the fast p-substitution
    evaluator (one Gauss–Legendre grid over the z-independent cos-phase
    breakpoints, valid for all z ≤ 225) tracks the analytic ξ at t=0 to
    4.1×10⁻⁸ at the z≈223 worst case and the independent v-substitution
    split quadrature to 6×10⁻⁷ (both cancellation-limited at values
    ~10⁻³⁶; the analytic-ξ check is the rigorous anchor).  Measured merger
    law, first-40 closest pair (γ-gap 0.845124): d(t)² slope 7.377 vs
    model 8, fit d²(0) 2.8749 vs 2.8569, fit t_c = −0.3897 vs model
    −0.3571, and the merger is CONFIRMED between 0.90 and 1.05 of the fit
    t_c (real separation 0.5186 at t = −0.3507; merged, no real roots, at
    t = −0.4092).  P2 (γ-gap 1.219290): fit t_c = −0.9419 vs model −0.7433
    — the quadratic model under-predicts the depth for wider pairs, an
    honest calibration of the extrapolation.  Pólya's direction holds for
    both pairs (t>0: zeros persist and separate).  The certified global
    closest pair (γ-gap 0.310431 at idx 452, γ ≈ 750.656) has local-model
    boundary t_c ≈ **−0.0482**, four-hundredths of a heat-unit below the
    axis, at magnitudes ~e^{−πγ/4} ~ 10⁻²⁵⁴ that are invisible to floats
    and default mpmath.  HONEST WALL (in the verdict): a numerical probe
    of the FINITE 648-zero system — the global-pair number is a
    validated-model extrapolation, NOT a certification, NOT a bound on Λ;
    no finite amount of zeros proves RH.  It is the picture RH's "barely
    so" already implies (Λ ≥ 0 by Rodgers–Tao/Dobner), measured at the
    system's own merger scale.
    **Sequel 2026-08-14 — the merger-boundary creep t_c(N)**
    (`experiments/merger_scaling.py`,
    `data/merger_scaling_data.json`): the finite face is a *stepping
    function* of how many zeros you can see — each new record-tight
    (Lehmer) pair cuts t_c = −(Δγ)²/2.  A vectorized Riemann–Siegel scan
    (grid 0.01, bisection 1e-8, the technique of `riemann_siegel_roots.py`
    extended to t ~ 36000) re-locates **43851 consecutive zeros** in ~10s:
    count exact at the scan top and matching `mpmath.zetazero` to ≤3×10⁻⁶,
    and it *independently re-discovers the classical Lehmer pair* (idx 6708,
    γ ≈ 7005.063/7005.101, gap 0.0377) — the very pair used for the
    Λ ≥ −1.15×10⁻¹¹ bound.  The creep: t_c = −0.0482 (N=648, certified
    slice) → −1.30×10⁻² (N=1000) → −9.35×10⁻⁴ (N=5000) → −7.11×10⁻⁴
    (N=10000, Lehmer) → **−6.23×10⁻⁴** (N≥20000, deepest record gap 0.03531
    at γ ≈ 17144).  The record-tight reduced gaps decay like N^{−1/3}
    (fitted slope −0.36; GUE small-gap tail −1/3), bracketed by the Wigner
    expected-minimum null.  Two faces of the same principle: the DIRECT
    H_t-evaluation face is numerically closed past γ ~ 1000 (H_0 values fall
    like e^{−πγ/4} ~ 10⁻²⁵⁴ at γ ~ 750, ~10⁻⁵⁸⁴⁷ at γ ~ 17144 — no
    computation reaches that), while the ZERO-LOCATIONS-ONLY face has no
    magnitude wall — which is exactly why the literature's rigorous Λ
    programme (Lehmer pairs: −50 → −0.0991 → −4.4×10⁻⁶ → −2.6×10⁻⁹ →
    −1.15×10⁻¹¹ → **0**, Rodgers–Tao) reaches the axis where H_t evaluation
    cannot.      HONEST WALL (in the verdict): only the first 648 zeros are
    interval-certified (the rest are float64-located, 1e-6-class agreement,
    negligible for 0.03-scale gaps); t_c(N) is naive model extrapolation, NOT
    a bound on Λ; a single-path record chain is bracketed by the GUE null,
    not a claim against GUE; no finite number of zeros proves RH.
    **Sequel 2026-08-15 — Connes "Letter to Riemann", NOT reproduced**
    (`experiments/connes_letter.py`, `data/connes_letter_data.json`): the
    letter's claim is that the Weil quadratic form on functions supported in
    [1,13] (primes 2,3,5,7,11,13 and their powers ≤13 only) has a ground
    state whose Mellin-transform zeros are real and approximate the first 50
    zeta zeros to 2.6e-55..1e-2.  We found, first, a *convention error in the
    letter's own archimedean term*: the explicit-formula identity
    f̂(i/2) − Σ_{1/2+is∈Z} f̂(s) + f̂(−i/2) = Σ_v W_v(f) closes to machine
    precision ONLY with eq(10) (W_p) plus the digamma archimedean form
    W_R(f) = (1/2π)∫φ(t)(log π − Re ψ(1/4+it/2))dt, while the paper's printed
    eq(11) leaves a function-dependent defect of 0.57/0.15 on the test
    functions (documented in `local_term_check`).  With the
    identity-consistent local terms, an independent Chebyshev discretization
    (M=10..30, full and even subspaces) finds **no real zeros** of the
    ground state's Mellin transform on [1,150], and |f̂(γ_n)| does not
    converge to zero with M.  The letter's OWN trigonometric truncation
    (N=50..150; footnote 14) does give the even ground state (Thm 6.1's
    evenness, exactly) with all F.T. zeros real — but they sit on a
    quasi-periodic lattice of spacing 2π/L = 2.45: matching the zeta-zero
    *density* (60+ zeros in [1,150] vs 50 zeta ordinates) yet NOT their
    positions (median offset ~0.73, 18/50 within 0.5, 2/50 within 0.05 at
    N=150; the exact-on-lattice zeros are a structural artifact of the trig
    truncation's periodic-Dirac spectrum).  The claimed 2.6e-55..1e-2
    precision is therefore tied to the footnote-14 rank-one-perturbation of
    a periodic Dirac operator with the Dirichlet kernel — extra structure
    not derivable from the letter's text.  HONEST WALL (in the verdict):
    non-reproduction of a numerical claim is NOT a disproof of RH and bounds
    nothing (no de Bruijn–Newman Λ consequence; finitely many primes never
    become the full Euler product).

    **Sequel 2026-08-15 — Footnote-14 Dirac construction, provably
    impossible at the first zero; the four-point lattice; the origin
    calibration** (`experiments/connes_dirac.py` + `four_point_lattice.py` +
    `zeta_lattice_alignment.py`, `data/connes_dirac_data.json` +
    `four_point_lattice_data.json` + `zeta_lattice_alignment_data.json`):
    the footnote-14 mechanism the letter's 2.6e-55 precision depends on is
    reconstructed EXACTLY from the trig ground state: f̂(z) = 4z·sin(zL/2)·R(z)
    with R(z) = Σ_k c_k(−1)^k/(z²−ω_k²) the secular function of a rank-one
    perturbation of diag(ω_k), ω_k = 2πk/L (verified to 5e-12), so the zeros
    are exactly {2πm/L : |m|>N} ∪ {roots of R}.  The provable statement:
    Cauchy interlacing pins each root in its own pole gap, and the FIRST
    rank-one eigenvalue lies in (0, ω₁] = (0, 2.45] — while γ₁ = 14.1347 is
    5.77 ω₁'s away, so the letter's claimed eigenvalue at γ₁ (2.6e-55) is
    categorically impossible (verified: 62 roots, all in own gap, first at
    1.0258; lattice part exact at N=50, |f̂| < 5e-15 on the 11 lattice zeros
    with m > 51).  The four-point coordinate lattice of the epoch anchor
    {10262000, 20001026, 20002610, 26102000} is exact finite arithmetic —
    gcd 2 (they span 2ℤ), the 4-block cross 1026|2000…2610|2000 closing at
    step 1584 = 2⁴·3²·11, an 840-point digit orbit with three leading-digit
    clusters and a permutohedron of diameter 16 with an empty shell at
    distance 14 — but its 2π/L proximity is at chance, so no origin derived
    from it aligns with the zeros: the honest index-matched test |γ_k −
    (o + k·s)| gives the best fixed lattice a median error 10.5 (0/50 within
    0.05); the genuine origin is adaptive (Weyl residuals mean 0.50/max
    0.88; Gram points 1/49 violations); the anchors score inside the
    random-origin spread (uniform median 0.612, 2/200 random origins beat
    the best anchor — selection noise).      HONEST WALL (in the verdicts): the
    provable content is negative classification — the letter's rank-one
    construction is impossible and no fixed lattice or anchor origin tracks
    the ordinates; RH remains open, and no project constant (C₀ = V(q0) =
    H(q0,0)) enters any of it.

    **Sequel 2026-08-15 — The headline tested head-on, at every N, over the
    whole orbit** (`experiments/zeta_direct_probe.py`,
    `data/zeta_direct_probe_data.json`): the three earlier measurements
    were indirect (lattice offsets, matching counts, origin residues); the
    probe computes the decisive things directly.  (1) AT the ordinates,
    mpmath dps 60: |f̂(γ₁)| = 2.65e-3 where a true zero gives exactly 0 and
    the claim is 2.6e-55; the nearest zero of f̂ to γ₁ is 1.02 away (median
    0.73 over n=1..50), |γ₁ − r₁| = 13.09, and the closest any ordinate
    comes to a zero is |f̂| = 2.95e-5 at γ₆ = 37.586 (the tight match the
    statistics had flagged); the identity f̂ = 4z·sin(zL/2)·R(z) re-verifies
    on all 50 ordinates to the double-precision coefficient floor (5.4e-12).
    (2) The interlacing theorem holds at EVERY N in {50,100,150,200} —
    one root per pole gap, r₁ ∈ (0, 2.45] (1.0170/1.0258/1.0496/1.0612
    as N grows; the probe's {50,100,150,200,300} sweep included N=300,
    where the certifier sequel below later showed the interlacing in fact
    BREAKS — residues flip at k = 153/154, 266/267, 267/268 and gaps
    153/266/267 do not have one root each; at N ≤ 200 the certified
    statement stands), γ₁ = 5.77 w₁ for every N, min gap margin ≥ 5e-3;
    N=100 cross-checks the persisted Dirac verdict to 8e-15.  (3) The
    WHOLE 840-point orbit, not just the four anchors, is census-tested as
    origins on the 2π/L lattice: the best has q = 0.3734, exactly the
    expected extreme-value minimum of 840 random origins (mean 0.3734,
    min 0.3734; random matches or beats it in 100% of trials) — the orbit
    is a typical set of 840 candidates and no known point is a special
    origin.  HONEST WALL: the direct numbers confirm the impossibility and
    the indifference; RH is open; the provable content remains negative
    classification, and C₀ = V(q0) = H(q0,0) does not enter.

    **Sequel 2026-08-15 — The interlacing theorem, CERTIFIED by interval
    arithmetic, and where it breaks** (`experiments/zeta_interlacing_certify.py`,
    `data/zeta_interlacing_certify_data.json`): the probe verified the
    interlacing numerically; the certifier turns it into a statement with
    validated rounding.  R(z) = Σ_k c_k(−1)^k/(z²−ω_k²) is evaluated in
    mpmath.iv (dps 80) at both ends of every pole gap; opposite certified
    signs give a root by the IVT — certified at N=100 in 100/100 gaps
    (endpoint magnitudes ≥ 1.8e0), at N=150 in 150/150, at N=200 in 200/200,
    at N=246 in 246/246.
    Uniqueness: for every N ≤ 246 the residues ρ_k = c_k(−1)^k share one
    sign (exact float check; at N=100 common sign +1, min |ρ| = 1.3e-3),
    R′(z) = −2z·Σ ρ_k/(z²−ω_k²)² is strictly one-signed on every gap, so
    each IVT root is unique — exactly one root per pole gap, a certified
    theorem for EVERY N ≤ 246 (numeric scan confirms 1 per gap at N =
    100, 150, 200, 246).  THRESHOLD: the interlacing is NOT a theorem in
    N.  The ground-state residues FIRST fail to share a sign at N = 247
    (flip between k = 246/247) and gap 246 then holds ZERO roots; at N=300
    they FLIP between k = 153/154, 266/267, 267/268
    (residue indices 154, 267, 268), and the three affected gaps break the
    one-root rule PRECISELY, as a numeric float scan (20001-point grid per
    gap, plus bisection) characterizes: gap 153 KEEPS TWO roots hugging the
    poles (distances 3.2e-4 and 1.8e-4 — its residues are tiny, ~4e-7, so
    the far field penetrates the pole layers), gaps 266 and 267 hold NONE,
    and every one of the other 297 gaps holds exactly one root (histogram
    {0: 2, 1: 297, 2: 1}, total 299) — the one-root-per-gap rule fails
    exactly where the adjacent residues have opposite signs, and the sign
    pattern itself is robust (identical across np.linalg.eigh and scipy
    eigh evr/evd/evx, standard and generalized forms).  THE
    WALL still certifies at EVERY N in the sweep (100, 150, 200, 246, 247,
    300): the
    first root is enclosed to ~2e-24 (80-step mp bisection, exact signs)
    inside (0, 2.45], γ₁ = 14.1347 is 5.77 ω₁'s away, and R and
    sin(γ₁L/2) are certified nonzero at γ₁ (|f̂(γ₁)| > 1.5e-2) — the
    claimed 2.6e-55 first-zero match is CERTIFIED IMPOSSIBLE at every
    certified N.  An independent mp Newton iterate (dps 60, x0 = 1.5) lands
    inside the certified enclosure (4.9e-25 from the midpoint); a float64
    brentq cross-check is NOT a valid containment test near this root —
    |R| ~ 1e-19 there sits below the float64 cancellation floor (~1e-18),
    so the float sign is noise, while the mp interval evaluation is exact.
    The certified r₁ (1.0258470804249210…) differs from the persisted
    connes_dirac value (1.0258470804249293) by 8.2e-15 — the documented
    round-off of the two matrix assemblies (dense product vs blocked lean
    builder), not a discrepancy of the theorem.  HONEST WALL: this is
    negative certification of the letter's construction — RH remains open,
    no de Bruijn–Newman Λ consequence, finitely many primes never become
    the full Euler product, and C₀ = V(q0) = H(q0,0) does not enter.

    **Sequel 2026-08-16 — The ordinate γ₁, re-derived from the series
    machinery alone** (`experiments/riemann_siegel_ordinate.py`,
    `data/riemann_siegel_ordinate_data.json`): the certifier thread proved
    there is no rank-one route to γ₁ = 14.1347…; this sequel closes the
    zeta side by asking where the number itself comes from and answering
    with a fully self-contained, error-budgeted chain — NO zetazero, NO
    mp.zeta, NO mp.loggamma.  θ(t) = Im logΓ(¼+it/2) − (t/2)log π is
    evaluated by the Stirling/Binet series (M = 25 terms, the validated
    factor-25 remainder bound of the certifier, dps 60) and ζ(½+it) by
    Euler–Maclaurin (N=200 sum, M=25 corrections, Backlund's explicit
    remainder bound), with Z = cos θ·Re ζ − sin θ·Im ζ.  The chain:
    Z(0) = ζ(½) = −1.4603… < 0 < Z(g₀) = +2.3401… at the first Gram point
    g₀ = 17.84559954041086… (θ(g₀) = 0, Newton on the series, 3.3e-25 from
    the logΓ reference); the RvM count N(g₀) = 1 (γ₁ < g₀ < γ₂) fixes that
    there is exactly one zero in (0, g₀]; the series scan over [13, g₀]
    (the Stirling series is asymptotic only for t ≳ 13 — below that the
    bound explodes) finds exactly one sign change of Z, so that crossing IS
    the first zero, and 120-step bisection recovers γ₁ =
    14.13472514173469379045725198356247027078… with |diff| = 2.2e-39 vs
    mpmath.zetazero(1) — well inside the bound-based budget (2·Z-bound/|Z′|
    ≈ 5.7e-19, the Stirling truncation at t ~ 14 dominating).  The series
    validation passes at 8 probe heights (t = 13…100) against the exact
    functions; at dps 60 the float rounding (~1e-57 floor) dominates the
    Backlund bound (1e-78…1e-86), which is the documented reason the
    validation compares against max(bound, rounding floor).  The
    certified-interval engine (validated regime, half-width 1e-8) encloses
    γ₁ with Z signs −1/+1, and Riemann–von Mangoldt closes the loop: θ(γ₁)/π
    = −0.550252829468691, so S(γ₁) = +0.550252829468691 (S just below =
    −0.449747170531309 — the +1 jump at the simple zero) and S(g₀) = 0.
    HONEST WALL: re-deriving ONE ordinate to ~18 digits is a closed
    derivation of a number, not a statement about the Riemann hypothesis —
    which remains open (rigorous verification now extends to |t| ≤ 3×10¹²,
    Platt–Trudgian); the certified bracket is a finite enclosure of a single
    zero, and C₀ = V(q0) = H(q0,0) does not enter.

    **Sequel 2026-08-16 — S-function census, Littlewood's equivalence, and
    the resolution limit** (`experiments/s_function_census.py`,
    `data/s_function_census_data.json`): the zeta-side sequels have certified
    WHERE the first zero is and a 648-zero box on the critical line; this
    sequel asks what the same certified data says about the S-function
    S(t) = N(t) − θ(t)/π − 1 — the discontinuity term that Littlewood's
    equivalence RH ⟺ S(t) = o(log t) (both directions, 1924) makes the
    cleanest quantitative handle on the hypothesis.  Over the certified
    range 0 < t ≤ g₆₅₂ = 1005.43 (N(g₆₄₇) = 648 Turing-certified, extended
    by five Rosser blocks to N(g₆₅₂) = 653, every located bracket certified
    one on-line simple zero) the certified bound max|S(g_j)| = 1 holds at
    all 653 Gram points.  An independent three-grid re-location (0.05, 0.01,
    0.005) reproduces the anchors exactly (654 located counts, N(g₆₄₇) =
    648, N(g₆₅₂) = 653) and exposes the classical Gram-violation pattern:
    S(g_j) ∈ {−1, 0, +1} (histogram {0:631, −1:13, +1:9}, nonzero at 22
    points), with 609 intervals holding exactly one zero, 22 holding a PAIR,
    22 holding NONE.  Interior |S(t)| < 2 throughout (observed sup +1.133 /
    inf −1.110 on [14.5, 1005.43]; S(0+) → −1), and at the certified top the
    observed max|S|/log T = 0.164 sits below the minimum conceivable RH
    envelope √(log T/log log T) = 1.891 (always ≥ √e = 1.6487, since
    log t/log log t ≥ e for all t) and far below the unconditional bound
    log T = 6.913.  RESOLUTION LIMIT: the RH envelope reaches value k only
    at √(log t/log log t) = k, i.e. log₁₀ t = 3.74 / 13.41 / 29.26 for
    k = 2/3/4 with N ~ 1e4 / 1e14 / 1e30 — the k = 3 height needs ~1e14
    certified zeros, ~2e11× this repo's 648 and ~10× the ENTIRE rigorous
    frontier (3×10¹², Platt–Trudgian, N ~ 1.3e13); k = 4 needs ~1e30, and
    no finite k-test can complete the o(log t) test.  HONEST WALL:
    numerical search is a counterexample engine — it can find a disproof
    (an off-line zero, or S growing like c log t) but it cannot prove RH,
    because RH is the global statement S(t) = o(log t) and every finite
    quiet census is compatible with a violation just beyond the frontier.

    **Sequel 2026-08-16 — Mertens–ψ census, the prime side of the
    Littlewood/von Koch equivalences** (`experiments/mertens_psi_census.py`,
    `data/mertens_psi_census_data.json`): the S-side sequels interrogated
    the zeros directly; this sequel crosses to the arithmetic side and asks
    whether the SAME hypothesis is visible in the primes.  An exact
    segmented sieve computes M(x), ψ(x), π(x) for every x ≤ 10⁸ (μ by
    small-prime flips + large-cofactor adjustment, verified against sympy
    mobius for n ≤ 10⁶ with zero mismatches; the classical Mertens table
    M(10^k) = −1, 1, 2, −23, −48, 212, 1037, 1928 reproduced exactly, OEIS
    A084237 — note the published sign at k = 8 is +1928, not the −1928 of
    folklore), behind Littlewood's and von Koch's equivalences RH ⟺ M(x) =
    O(x^{1/2+ε}) ⟺ ψ(x) = x + O(x^{1/2} log²x) ⟺ π(x) = Li(x) + O(x^{1/2}
    log x).  Records over x ∈ [1000, 10⁸]: max |M(x)|/√x = 0.4722 at x =
    2803, and it never even reaches 0.5 anywhere in the range (the points
    above 0.5 are only tiny x < 1000, e.g. x = 13 — a reminder that small-x
    fluctuations dominate the ratio); max |ψ(x)−x|/√x = 0.7770 at x = 1422;
    the RH-normalized max |ψ(x)−x|/(√x log²x) = 0.0147 at x = 1422 (O(1)
    under RH); and π(10^k) − Li(10^k) < 0 for every k = 1..8.  The
    explicit formula ψ₀(x) = x − Σ_ρ x^ρ/ρ − log 2π − ½log(1−x⁻²),
    evaluated with the repo's OWN located zeros (653 / 4520 / 10142 / 22491
    for T = 1005.43 / 5000 / 10000 / 20000 — the 653 at T = g₆₅₂ matching
    the certified N(g₆₅₂)), reproduces the sieve's exact ψ(x) with residuals
    that shrink as T grows (at x = 100, −0.169 for T = 1005.43 vs −0.006
    for T = 20000): the located zeros really DO count the primes, and the
    count converges as T → ∞ exactly as the zeta side is completed.  THE
    TWO PROVEN-BUT-NEVER-SEEN FAILURES — the sharpest known witnesses that
    "quiet so far" proves nothing: (a) the Mertens conjecture M(x) < √x is
    PROVEN false (Odlyzko–te Riele 1985; Pintz: a counterexample below
    exp(1.59e40)) yet no explicit x is ever exhibited and |M(x)| < √x holds
    for every x ≤ 10¹⁶ computed; (b) π(x) > Li(x) is PROVEN to occur
    (Skewes 1933/1955; first crossing below ~1.4e316 under RH by
    Bays–Hudson 2000) although π(x) < Li(x) at every computable height.
    Both are finite-failure theorems whose empirical evidence points the
    WRONG way.  RESOLUTION LIMIT: RH needs the supremum over ALL x while
    any finite prefix only samples a continuum of nearby violations, and
    the best unconditional state is Korobov–Vinogradov ψ(x) = x + O(x·exp
    (−c (log x)^{3/5}/(log log x)^{1/5})) — an exponential-in-log-distance
    gap from the RH exponent.      HONEST WALL: the arithmetic side confirms
    the S-side conclusion — numerical search is a counterexample engine,
    RH remains open, and the proof (if it exists) is not a computation.

    **Sequel 2026-08-16 — Mertens sublinear census, the Mertens function at
    height** (`experiments/mertens_sublinear_census.py`,
    `data/mertens_sublinear_census_data.json`): the Mertens–ψ census
    stopped at x = 10⁸ with max |M(x)|/√x = 0.4722, under the
    proven-false conjecture's forbidden 0.5.  This sequel pushes the exact
    sieve to x = 10¹⁰ (small-prime flips/zeroing plus a vectorized
    large-cofactor step n = m·q with m squarefree ≤ √x and q prime > √x,
    indices provably unique; machinery verified against sympy mobius for
    n ≤ 10⁶, zero mismatches) and reproduces M(10^k) = −1, 1, 2, −23, −48,
    212, 1037, 1928, −222, −33722 for k = 1..10 (OEIS A084237; M(10¹⁰) =
    −33722).  THE FINDING: the first |M(x)|/√x > 0.5 excursion at height
    appears at x = 7,725,038,629 (M = 43,947), with max ratio 0.5706 at
    x = 7,766,842,813 (M = 50,286) — the first re-crossing since the
    trivial x = 13.  This is exactly the regime the theorem promises: the
    Mertens conjecture M(x) < √x is PROVEN false (Odlyzko–te Riele 1985;
    Pintz: a counterexample below exp(1.59e40)), and the ratio crossing at
    7.7e9 is a genuine instance of the forbidden behavior — yet it is not
    an explicit counterexample to the conjecture (|M(x)| > √x with ratio
    merely above 1/2, not above 1), and reaching x with |M(x)|/√x > 1 is
    still out of reach of direct sieving.  Part 2 uses the O(N^{2/3})
    quotient-set recursion M(n) = 1 − Σ_d M(⌊n/d⌋) (grouped over distinct
    quotients, memoized over {⌊N/i⌋}, base = exact 10⁹ prefix; validated
    by a base-table self-check re-deriving M(10⁵) = −48 and M(10⁶) = 212)
    to compute M(10¹¹) = −87856, M(10¹²) = 62366, M(10¹³) = 599582 — every
    value matching OEIS A084237 exactly, two orders of magnitude in height
    beyond the sieve.  RESOLUTION LIMIT: RH requires M(x) = O(x^{1/2+ε})
    (Littlewood 1912) as a supremum over ALL x — a global statement no
    finite census decides — and the Mertens-conjecture theorem shows the
    ratio can behave adversarially far beyond any computation; moreover
    every computed |M(x)| < √x at x ≤ 10¹⁶ despite the proven failure.
    HONEST WALL: extending the census to 10¹³ (or any finite height) is a
    counterexample search, not a proof; RH remains open; the proof (if it
    exists) is not a computation.

    **Sequel 2026-08-16 — Mertens sublinear census, extended to M(10¹⁴):
    the published table completed, and the forbidden ratio still winning**
    (`experiments/mertens_sublinear_census.py`,
    `data/mertens_sublinear_census_data.json`): the previous sequel
    stopped the recursion at M(10¹³).  This sequel pushes the shared
    quotient-set memo one more order of magnitude and computes M(10¹⁴) =
    −875575 — every M(10ⁿ) for n = 1..14 now matches OEIS A084237, the
    complete published table.  The recursion cost for 10¹⁴ (~10^{2/3} ×
    the 10¹³ cost) stayed a few thousand seconds in a single shared memo,
    confirming the O(N^{2/3}) scaling in practice.  Part 3 adds a free
    scan of the recursion memo: every quotient point x = ⌊N/i⌋ > 10¹⁰ of
    each target is an EXACT value of M(x), and 11,106 such points were
    inspected (a sparse sample, not a census).  The scan finds two
    further |M(x)|/√x > 0.5 crossings at height — first at x =
    108,813,928,182 (M = 169,281, ratio 0.5132), max sampled ratio 0.5132
    at the same x — so the forbidden ratio is not a fluke of the 7.7e9
    region, but recurs around 1.09e11.  Yet the sampled max 0.5132 stays
    BELOW the exact record 0.5706 at x = 7.77e9: the census record stands,
    and every sampled height still sits far under 1 (an actual
    counterexample to M(x) < √x needs |M(x)| > √x).  RESOLUTION LIMIT
    unchanged: RH requires M(x) = O(x^{1/2+ε}) as a supremum over ALL x —
    a global statement no finite census decides — and the
    Mertens-conjecture theorem shows the ratio can behave adversarially
    far beyond any computation.  HONEST WALL: extending the census to
    10¹⁴ (or any finite height) is a counterexample search, not a proof;
    RH remains open; the proof (if it exists) is not a computation.

    **Sequel 2026-08-16 — Mertens explicit formula at height: 22,491
    located zeros carry ~98% of M(10¹⁴), and the price of height is the
    residual's non-monotone walk** (`experiments/mertens_explicit_height.py`,
    `data/mertens_explicit_height_data.json`): the Mertens–ψ census showed
    the explicit formula for ψ with the repo's located zeros shrinks onto
    the exact sieve as T grows (residual −0.006 at x = 100, T = 20000).
    This sequel asks how far that extends at height, evaluating the
    Mertens explicit formula M₀(x) = −2 + Σ_{γ≤T} 2Re[x^{1/2+iγ}/(ρζ′(ρ))]
    + trivial terms (constant −2 = residue of x^s/(sζ(s)) at s = 0,
    pinned against the classical table M(100) = 1, M(1000) = 2) with the
    repo's OWN Riemann–Siegel located zeros located ONCE to t = 20000
    (22,491 zeros; sliced 653/4520/10142/22491 for T = 1005.43/5k/10k/20k,
    counts matching the census exactly) and mpmath ζ′(ρ) at every zero —
    a ~36-minute single pass, cached for reproducibility.  THE FINDING: at
    x = 10¹¹ the T = 20000 value −86867 is off by +989 (1.13%); at
    x = 10¹⁴ it is −860152 vs the exact −875575 (residual +15423, 1.76%);
    at x = 100/1000 the truncation is essentially exact (residual
    3e-4 / 1.6e-3).  THE REAL FACE OF THE HEIGHT: the Mertens explicit
    formula is only CONDITIONALLY convergent (pairing conjugate zeros)
    and the residuals are NON-monotone in T — at x = 10¹² the T = 20000
    residual +1850 is WORSE than T = 10000's −61, and at x = 10¹⁴
    T = 5000 is worse than T = 1005.43 — so a hard cutoff at T does not
    guarantee a better value as T grows; the empirical tail bound
    E_T(x) = Σ_{T<γ≤20000} 2√x/(|ρ||ζ′(ρ)|) grossly overestimates the
    observed residual (at x = 10¹², E = 1.5e6 vs a residual ~10³, a
    measured 1000× gap) because the terms cancel — the worst-case bound
    is not a predictor.  RESOLUTION LIMIT: the identity holds only in the
    T → ∞ limit with the correct smooth/paired summation; no finite T
    certifies M(10¹⁶) or beyond, and the tail past t = 20000 is not
    located.  HONEST WALL: the zeros REALLY influence the primes at 10¹⁴
    (98% of the value recovered), but 'the zeros reproduce M' is a
    percent-level approximation with an unquantifiable
    conditional-convergence tail — not a proof of RH, which remains open.

    **Sequel 2026-08-16 — Chebyshev ψ explicit formula at height: the
    truncation is measurably WORSE than M's at every height — conditional
    convergence bites** (`experiments/mertens_psi_height.py`,
    `data/mertens_psi_height_data.json`): the twin of the Mertens-at-height
    sequel, asking how well the SAME located zeros count ψ (the prime-side
    function) at 10¹¹..10¹⁴.  The formula ψ₀(x) = x − Σ_{γ≤T} 2Re[x^{1/2+iγ}/
    (½+iγ)] − log 2π − ½log(1−x⁻²) (symmetric, conjugate-paired cutoff) is
    evaluated with the repo's OWN Riemann–Siegel located zeros (22,491 to
    t = 20000, sliced 653/4520/10142/22491) against EXACT ψ(x) obtained
    from a NEW quotient-set identity ψ(x) = Σ_{k≤V} log k·M(⌊x/k⌋) +
    Σ_{w≤W} μ(w)·L(⌊x/w⌋) − M(W)·L(V), V = ⌊√x⌋, W = ⌊x/(V+1)⌋, L(n) =
    log n! — M exact at every quotient point via the segmented 10⁹ sieve +
    memoized quotient-set recursion (M(10¹¹..10¹⁴) OEIS-verified), L via
    mpmath loggamma (w < 2000) + vectorized scipy gammaln (total rounding
    ~0.1 absolute); the identity is validated at ψ(100) = 94.0453,
    ψ(1000) = 996.6809, ψ(10⁶) = 999586.5975, ψ(10⁸) = 99998242.7966.
    THE FINDING: exact ψ(10¹¹..10¹⁴) = 100000058456.4 / 1000000040136.8 /
    10000000171998.7 / 100000000618672.4 (ψ(x)−x = +58456 / +40137 /
    +171999 / +618672 — small fractions of √x, as RH would demand), and at
    T = 20000 the formula residuals are −3645 / −19476 / +28854 / −88932 —
    at EVERY height LARGER than the Mertens formula's at the same
    truncation (+989 / +1850 / −13563 / +15423, factors ~3.7 / 10.5 / 2.1 /
    5.8).  This is exactly what the convergence theory predicts: ψ's terms
    ~ √x/γ with Σ 1/γ divergent, so NO tail bound exists (the located-tail
    magnitude Σ_{T<γ≤20000} 2√x/γ = 6.3e7 at x = 10¹⁴ is ~700× the observed
    residual — the tail cancels, it is context NOT a bound, and it has no
    finite total as the horizon grows), while M's paired series is
    absolutely convergent (Titchmarsh) and truncates better in practice.
    BOTH walks are NON-monotone in T (at x = 10¹⁴ ψ's best is T = 10000's
    −80364 vs T = 20000's −88932; M's T = 5000 is 30× worse than its
    T = 1005.43) — hard cutoffs are not ordered for either function, and at
    x = 100/1000 the ψ truncation is essentially exact (−0.006 / +0.034).
    RESOLUTION LIMIT: no finite T certifies ψ(10¹⁶); the census truth stops
    at 10¹⁴; the tail beyond t = 20000 is not located; and for ψ the
    truncation error is an unquantifiable oscillation with no tail bound at
    all.  HONEST WALL: the located zeros influence the primes at 10¹⁴ and
    the identity holds only in the T → ∞ limit — a measured approximation
    (worse than M's, as the conditional convergence demands), NOT a proof of
    RH, which remains open.

    **Sequel 2026-08-16 — Body fold symmetry: the fold is EXACT, the
    breaking is measured, and the tree mirror fails by a factor of 2**
    (`experiments/body_fold_symmetry.py`,
    `data/body_fold_symmetry_data.json`): tests the turned-then-folded
    symmetry numerically.  The cartesian field {(a,b) : a·b ≤ x}, cells =
    divisor pairs τ(n), growth D(x) = Σ_{n≤x} τ(n); the fold at the
    diagonal a = b (the "turning point" √x) is an EXACT identity — D = U + L
    with L = U − d², commutativity of multiplication — verified by exact
    integer arithmetic at every x = 10..10¹⁴.  THE BREAKING: Δ(x) =
    D(x) − (x log x + (2γ−1)x) certifiably satisfies the PROVEN Voronoi
    bound O(x^{1/3} log x) (|Δ|/(x^{1/3} log x) falls 0.49 → 0.006 from
    x = 10 to 10¹⁴) but the conjectured x^{1/4} — the fold of the critical
    exponent 1/2, since τ = 1⋆1 squares ζ → ζ² — is NOT certified at any
    finite height (the local growth exponent of |Δ| wanders −0.15 → +0.81,
    non-monotone like the M/ψ walks).  THE TREE: the Calkin–Wilf regular
    tree's upper/lower mirror is a TAUTOLOGY of regularity (every node at a
    given depth has identical subtree size), while the integer divisibility
    tree (parent m → m/spf(m), every integer ≤ 10⁶ once) is a directed
    growth whose depth-reversal mirror FAILS — median subtree sizes at depth
    k vs 8−k give ratios 2.0 / 2.0 / 2.0 / 1.0 / 0.5 — and branch growth is
    linear, not golden (τ(2^k) = k+1; τ(2^19)/φ^19 = 2.1e-3).  WHAT
    CONNECTS: the three convolution folds of the one field — 1⋆1 = τ,
    1⋆μ = δ (Σ_{d≤x} μ(d)⌊x/d⌋ = 1, verified exactly), μ⋆log = Λ (the
    5.21s exact-ψ fold) — with three measured breakings at the same heights
    (|Δ|/x^{1/4} ≤ 3.6; |M|/√x ≤ 0.34 measured, census record 0.57;
    |ψ−x|/√x ≤ 0.69 measured, census record 0.777).  HONEST WALL: the exact
    fold and the measured breaking are arithmetic facts; the upper/lower
    body mirror (brain = origin, torso = fold axis, limbs mirrored) is a
    mapping the numbers do not commit to — the regular-tree mirror is a
    tautology and the integer tree's mirror FAILS, the opposite of a
    body-like symmetry; the divisor problem's 1/4 is as open as the critical
    line's 1/2, and RH remains open.

    **Sequel 2026-08-16 — Zeta zero spectral match: the 22,491 located zeros
    are GUE, and the repo's own spectra are not**
    (`experiments/zeta_zero_spectral_match.py`,
    `data/zeta_zero_spectral_match_data.json`): which spectra resemble the
    located zeros?  Nearest-neighbour spacing statistics on the 22,491 zeros
    to t = 20000 (normalized s_n = (γ_{n+1}−γ_n)·(1/2π)log(γ_n/2π)): the
    zeros fit the GUE Wigner surmise — KS 0.037 (vs Poisson 0.286, GOE
    0.072, a simulated 10×400 GUE ensemble 0.037), level repulsion
    β = 1.64 (GUE 2 / GOE 1 / Poisson 0), number variance Σ²(L) = 0.27–0.43
    tracking the GUE ensemble (0.28–0.64) and far below Poisson's linear
    growth — the Montgomery–Odlyzko law.  THE TIME READING: u = log x is
    the natural time coordinate (the explicit formula is a Fourier sum in u
    with frequencies γ, amplitudes 1/(½+iγ)), and the zero stream is a
    DETERMINANTAL process in log-time, not white noise — normalized gaps
    have lag-1 autocorrelation −0.364 vs GUE −0.323 vs Poisson ~0; the
    S-walk max|S|/log t = 0.146 reproduces the persisted S-census scale
    (0.164).  THE REPO'S OWN SPECTRA DO NOT RESEMBLE THE ZEROS:
    spectral_extended (100 eigenvalues) is Poisson (KS 0.074 to Poisson vs
    0.354 to GUE — integrable, the opposite family); spectral_data (30
    eigenvalues) sat ~10 units from any zero (zeta_match_distances) and is
    too small to classify.  HONEST WALL: GUE resemblance at 22,491 low
    zeros is the CONJECTURED Montgomery correlation law supported
    numerically — a resemblance, not a proof of RH, which remains open.

    **Sequel 2026-08-16 — What a proof of RH needs to be: a single uniform
    global bound, and no computation can enter it**
    (`docs/RH_PROOF_REQUIREMENTS.md`): maps the five candidate proof routes
    (A–E) from the repo's measured position.  The exact statement: ζ(s) has
    no zeros with Re > 1/2.  The equivalences (von Koch ψ, Littlewood M,
    π = Li, S(t) = o(log t), Λ ≤ 0) are four phenotypes of one organism;
    the repo measured all of them to 10^14 / 22,491 zeros and they behave
    as RH predicts — but each is a supremum over the infinite, and no finite
    computation has logical force.  The two proven-false-but-never-seen
    theorems (Mertens: proven false, never seen; π > Li: proven to occur,
    never seen) warn that the computable range can look exactly RH-correct
    while the truth beyond is different.  Five routes, five missing theorems:
    (A) von Koch/Littlewood uniform bound (circular without a structure
    theorem); (B) S(t) = o(log t) globally; (C) Hilbert–Pólya self-adjoint
    operator; (D) de Bruijn–Newman Λ ≤ 0 (Λ ≥ 0 already proven by
    Rodgers–Tao 2018, so Λ = 0 follows in one line — the single most
    self-contained target); (E) structural identity.  The removable-
    singularity argument: f(x) = |(x−1)/(1−x)| = 1 everywhere defined,
    0/0 at x = 1; proving the singularity removable = proving f ≡ 1 =
    proving RH.  The repo's GUE measurement is the cell's genome being
    rigid; the fold arithmetic is the algebraic skeleton.  HONEST WALL:
    the proof needed is a structure theorem, not a computation; the answer
    to 'can you prove 0/0 = 1?' is 'that is the proof of RH' — the function
    is already constant where defined; showing the singularity is removable
    by a criterion other than evaluating the limit is the open problem.

    **Sequel 2026-08-17 — The RH reduction paper: g(s) = |ζ(s)|/|ζ(1−s)|
    is identically 1 iff RH** (`docs/RH_REDUCTION_PAPER.md`): the removable-
    singularity argument from Ch. 5.21v is now a complete, self-contained
    paper.  Define g(s) = |ζ(s)|/|ζ(1−s)|.  (1) g = 1 on the critical line
    by Schwarz reflection (|ζ(½+it)| = |ζ(½−it)|).  (2) At each zero ρ,
    g = 0/0 (both numerator and denominator vanish).  (3) The singularity is
    removable: near ρ, ζ(s) ≈ c₁(s−ρ) and ζ(1−s) ≈ −c₂'(s−ρ), so
    g ≈ |c₁|/|c₂'|; the functional equation gives c₁/(−c₂') = χ(ρ), so
    the removable value is |χ(ρ)|.  (4) |χ(ρ)| = 1 iff Re(ρ) = ½ (the
    prefactor π^{σ−½} ≠ 1 off the line).  (5) Therefore g ≡ 1 iff RH.
    The paper also contains the de Bruijn–Newman reduction (Λ ≤ 0 ⟹ RH),
    the Rodgers–Tao inequality (Λ ≥ 0), the complete conditional proof
    (Λ = 0 ⟺ RH), numerical evidence (22,491 zeros, exact Mertens/Chebyshev
    to 10¹⁴), the two proven-but-never-seen warnings (Mertens false,
    π > Li), and the five approaches to proving Λ ≤ 0.  HONEST WALL: the
    proof is a complete reduction, not an unconditional proof — g ≡ 1 IS
    the statement that Re(ρ) = ½ for all zeros, and showing the singularity
    removable by a criterion other than evaluating the limit (continuity,
    self-adjointness, positivity of H_t) is the open problem; RH remains
    open.

    **Sequel 2026-08-17 — What zero is: the complete definition and the
    distinction between pole and indeterminate** (`docs/WHAT_ZERO_IS.md`,
    `docs/WHAT_ZERO_IS.pdf`): zero has three identities — additive identity
    (a+0=a), absorbing element (a·0=0), and limit of vanishing.  Division by
    zero splits into two cases: c/0 (c ≠ 0) is a pole (infinite, Theorem 3.1:
    no solution to 0·x = c); 0/0 is indeterminate (Theorem 3.1: every x
    satisfies 0·x = 0; Theorem 5.1: removable singularity gives f'(a)/g'(a)
    when both vanish linearly).  The hierarchy: faster numerator → 0, faster
    denominator → ∞, same rate → finite (the removable value).  Application to
    zeta: g(rho) = 0/0, not a pole; the (s−rho) cancels, giving |chi(rho)|.
    The entire RH proof rests on the distinction between pole and indeterminate.
    Cross-references RH_REDUCTION_PAPER and IF_C0_IS_0_OVER_0.

    **Sequel 2026-08-17 — Where 0/0 solves problems: the indeterminate form
    as structural probe across mathematics and physics**
    (`docs/WHERE_0_OVER_0_SOLVES.md`, `docs/WHERE_0_OVER_0_SOLVES.pdf`):
    ten instances where 0/0 is used as a probe: (1) RH — g(s) = |zeta(s)|/
    |zeta(1-s)| at zeros; (2) GRH — Dirichlet L-functions g_chi(s); (3) BSD
    — L(s,E)/(s-1)^r at s=1 (removable value = leading coefficient encoding
    rank); (4) Riemann-Roch — l(K-D) counting functions vanishing at both;
    (5) renormalization — m_bare - delta_m = finite physical mass; (6)
    Poincare-Hopf — winding number index = chi(M); (7) argument principle —
    f'/f residue = multiplicity; (8) Atiyah-Singer — analytical = topological
    index; (9) abc — c/rad(abc) bounded; (10) gradient descent — Hessian
    resolves saddle point 0/0.  Common thread: the 0/0 is a probe testing
    whether two things are the same at a vanishing point; the removable value
    encodes the structural information.  Links WHAT_ZERO_IS and
    IF_C0_IS_0_OVER_0.

    **Sequel 2026-08-17 — If C₀ = 0/0: the entire L.O.R.E. framework as
    a 0/0 structure** (`docs/IF_C0_IS_0_OVER_0.md`,
    `docs/IF_C0_IS_0_OVER_0.pdf`): C₀ = V(q₀)/(N − |context|) is 0/0 at
    full context (both vanish).  Theorem 2.1: removable value = average energy
    per non-context node.  Theorem 3.1: the viscosity solution (fold theorem)
    selects the unique path giving a finite answer — "measured, not chosen"
    means the 0/0 has no unique value without a path, and the viscosity
    solution is that path.  Calendar: all epochs give the same 0/0 form
    (Theorem 4.1: invariant under calendar transformations).  Consensus:
    local C₀ = 0/0 at each site; quorum >40% honest ensures removable values
    propagate (Theorem 5.1).  Prime count: error term = sum of 0/0 forms at
    zeros (Theorem 6.1).  Fold: geometric 0/0 at the singular locus.  Exact
    parallel to g(s) = 0/0 in the zeta argument — "C₀ = 0/0 is the L.O.R.E.
    analogue of g = 0/0; the entire repo is a 0/0 structure."
    Cross-references RH_REDUCTION_PAPER, WHAT_ZERO_IS, WHERE_0_OVER_0_SOLVES.

    **Sequel 2026-08-17 — GRH Dirichlet L-functions via 0/0: g_χ = 1 on the
    critical line for 8 Legendre characters** (`experiments/grh_dirichlet_0_over_0.py`,
    `data/grh_dirichlet_0_over_0_data.json`): g_χ(s) = |L(s,χ)|/|L(1−s,χ̄)| = 1
    on Re(s) = ½ by the functional equation, with removable value |ε(χ)| = 1
    at each zero of L(s,χ).  Gauss sums verified: |G(χ)| = √p for all 8 primes
    {3,5,7,11,13,17,19,23}.  Root numbers: ε = 1.000000.  The 0/0 structure
    is identical to the zeta case — g_χ = 1 IS Re(ρ) = ½.  GRH remains open.

    **Sequel 2026-08-17 — abc conjecture via 0/0: record quality 1.630 and the
    unit triple 0/0** (`experiments/abc_conjecture_0_over_0.py`,
    `data/abc_conjecture_0_over_0_data.json`): 38058 coprime triples scanned,
    record quality 1.6299 (2 + 6436341 = 6436343, rad = 15042).  The unit
    triple (1,1,1) gives log(1)/log(rad(1)) = 0/0 with removable value 1 =
    the bound itself.  The conjecture asserts q ≤ 1+ε for all but finitely
    many triples — a finite verification, not a proof.

    **Sequel 2026-08-17 — Poincaré–Hopf via 0/0: index = removable value of
    V/|V| at zeros; S² Euler characteristic verified** (`experiments/poincare_hopf_0_over_0.py`,
    `data/poincare_hopf_0_over_0_data.json`): vector field on S² with two zeros,
    each with index 1, sum = 2 = χ(S²).  T²: constant field, χ = 0.  Removable
    value convergence: as contour shrinks from radius 0.1 to 0.0001 (3600 to
    3600000 points), index converges to exactly 1.  The 0/0 V/|V| at each zero
    has removable value = winding number.

    **Sequel 2026-08-17 — Riemann–Roch via 0/0: l(D)−l(K−D) = 0 at deg = g−1
    for genera 1–5** (`experiments/riemann_roch_0_over_0.py`,
    `data/riemann_roch_0_over_0_data.json`): Riemann–Roch l(D)−l(K−D) = deg(D)−g+1
    verified for genera 1–5 across all relevant degrees.  At deg(D) = g−1:
    the formula gives 0 = 0 (the 0/0 form).  Canonical divisor l(K) = g, deg(K) =
    2g−2 (Serre duality).  All identities hold — a proven theorem, not conjecture;
    the 0/0 framing highlights structural parallels.

    **Sequel 2026-08-17 — BSD via 0/0: L(1+ε,E) shrinks for rank 1, stabilizes
    for rank 0** (`experiments/bsd_0_over_0.py`,
    `data/bsd_0_over_0_data.json`): L(s,E) computed via truncated Euler product
    for 4 elliptic curves at ε = {0.5,0.2,0.1,0.05,0.01}.  Rank 0 curves
    (y²=x³−x, y²=x³+1): L(1+ε) stabilizes (ratio > 0.8, value > 0.3).
    Rank 1 curve (y²=x³−25x, n=5 congruent): L(1+ε)→0 (ratio 0.69, value 0.11
    at ε=0.01).  The 0/0: L(s,E)/(s−1)^r has removable singularity at s=1.
    BSD remains a conjecture; this is a finite verification.

    **Sequel 2026-08-17 — Argument principle via 0/0: 5 rectangles, exact zero
    counts** (`experiments/argument_principle_0_over_0.py`,
    `data/argument_principle_0_over_0_data.json`): (1/2πi)∮ζ′(s)/ζ(s) ds
    integrated around rectangles [0.1,0.9]×[im_min,im_max] and verified zero
    counts: 1, 2, 4, 0, 8 — all match.  At each zero ρ, ζ(ρ)=0 in the
    denominator of ζ′/ζ creates the 0/0; the residue (= multiplicity) is the
    removable value extracted by the residue theorem.

    **Sequel 2026-08-17 — Atiyah–Singer via 0/0: ind(D) = χ(M) for S² and T²**
    (`experiments/atiyah_singer_0_over_0.py`,
    `data/atiyah_singer_0_over_0_data.json`): icosahedron-subdivided S²
    (162V, 480E, 320F, χ=2) and periodic-grid T² (100V, 300E, 200F, χ=0).
    Laplacian zero-eigenvalue count gives Betti numbers b₀−b₁+b₂ = χ(M).
    The 0/0: Laplacian eigenvalue 0 has multiplicity b_k; the index theorem
    says the alternating sum equals the Euler characteristic.

    **Sequel 2026-08-17 — Gradient descent via 0/0: Hessian resolves saddle,
    Newton escapes in 1 step** (`experiments/gradient_descent_0_over_0.py`,
    `data/gradient_descent_0_over_0_data.json`): L(x,y)=x²−y² has ∇L=0 at
    origin, Hessian eigenvalues ±2 (saddle).  GD 50 steps diverges along y-axis.
    Newton method (H⁻¹∇L) converges to minimum in 1 step.  10D saddle: 5 positive
    + 5 negative eigenvalues.  Pedagogical illustration of the 0/0 pattern.

    **Sequel 2026-08-17 — Heat kernel trace via 0/0: Tr(e^{-tΔ}) → 1 at t=∞**
    (`experiments/selberg_trace_0_over_0.py`,
    `data/selberg_trace_0_over_0_data.json`): Analytical eigenvalues for flat
    torus T² and sphere S².  Tr → 1.000000 at t=100 for both (removable value
    = 1, the zero-mode contribution).  At t=0: Tr → ∞ (Weyl singularity).
    The 0/0: lim_{t→∞} Tr(e^{-tΔ}) = 1, a removable value from the zero
    eigenvalue.  Triangulated sphere numerical verification also included.

    **Sequel 2026-08-17 — Lefschetz fixed-point via 0/0: L(id) = χ(M)**
    (`experiments/lefschetz_fixed_point_0_over_0.py`,
    `data/lefschetz_fixed_point_0_over_0_data.json`): S²: L(id)=2=χ(S²),
    Betti (1,0,1).  T²: L(id)=0=χ(T²), Betti (1,2,1).  Rotation on T²:
    trace on H₁ = 0 (the 0/0), removable value = local index.  The 0/0 at
    the trace of f_* on each homology group determines fixed points via the
    alternating sum.

    **Sequel 2026-08-17 — Gauss-Bonnet via 0/0: ∫∫K dA = 2πχ(M)**
    (`experiments/gauss_bonnet_0_over_0.py`,
    `data/gauss_bonnet_0_over_0_data.json`): S²: GB = 2π·2 (χ=2, all K>0).
    T²: GB = 0 (χ=0, all vertices near K=0 — the 0/0).  Torus of revolution:
    GB = 0 (χ=0, mixed curvature: 107+, 102−, 16≈0).  At K=0, angle defect
    = 2π exactly — the removable value.

    **Sequel 2026-08-17 — Weyl’s law via 0/0: eigenvalue counting converges**
    (`experiments/weyl_law_0_over_0.py`,
    `data/weyl_law_0_over_0_data.json`): N(λ)/λ^{d/2} converges to
    C_weyl on T² (error 0.07%) and S² (error 0.78%).  0/0: ratio diverges at
    λ=0 (N=0, denominator=0), removable value = C_weyl from large-λ limit.

    **Sequel 2026-08-17 — Central limit theorem via 0/0: phi(t) → Gaussian**
    (`experiments/central_limit_theorem_0_over_0.py`,
    `data/central_limit_theorem_0_over_0_data.json`): CLT verified for uniform,
    exponential, Bernoulli.  0/0: (phi(t)-1)/t^2 at t=0 is 0/0; removable
    value = -1/2 (variance).  All ratios converge to -0.499x.

    **Sequel 2026-08-17 — Banach fixed-point via 0/0: contraction → unique x***
    (`experiments/banach_fixed_point_0_over_0.py`,
    `data/banach_fixed_point_0_over_0_data.json`): cos(x), Newton sqrt(2),
    linear T(x)=0.5x+1 all converge.  0/0: (T(x)-x)/(x-x*) at x=x*;
    removable value = T'(x*)-1.  Cos: -1.6736, Newton: -1.0, linear: -0.5.

    **Sequel 2026-08-17 — Poisson summation via 0/0: xi(0) = 1/2**
    (`experiments/poisson_summation_0_over_0.py`,
    `data/poisson_summation_0_over_0_data.json`): xi(s) functional equation
    verified, theta functional equation verified.  0/0: xi(s)/cos(pi s/2) at
    s=0 is 0/0; removable = 1/2.  Converges from both sides.

    **Sequel 2026-08-17 — Rayleigh quotient via 0/0: x^T A x / x^T x at x=0**
    (`experiments/rayleigh_quotient_0_over_0.py`,
    `data/rayleigh_quotient_0_over_0_data.json`): 2D and 3D symmetric
    matrices, random 5D.  All removable values match eigenvalues exactly
    (error < 1e-10).  Min/max bounds hold.

    **Sequel 2026-08-17 — Cauchy integral formula via 0/0: f(z)/(z-a) at z=a**
    (`experiments/cauchy_integral_0_over_0.py`,
    `data/cauchy_integral_0_over_0_data.json`): residue = removable value.
    f(z)=z^2, a=1: residue=2.  f(z)=1/z, a=2i: residue=-i/4.
    f(z)=sin(z)/z, a=0: residue=1.  All converge to removable via h->0.

    **Sequel 2026-08-17 — Noether/Landau mean-field Ising via 0/0: M(T_c)=0/0**
    (`experiments/noether_landau_0_over_0.py`,
    `data/noether_landau_0_over_0_data.json`): Landau free energy
    F = a(T-T_c)M^2 + bM^4, M = sqrt((T_c-T)/(2b)) below T_c.
    0/0: M/(T_c-T)^{1/2} at T=T_c is 0/0; removable = 1/sqrt(2b).
    Amplitude ratio: sqrt(2)*M*sqrt(b) = sqrt(T_c-T).  Above T_c: all M=0.
    Free energy has minima at M=0 (T>=T_c) and M=+-M_0 (T<T_c).

    **Sequel 2026-08-17 — Euler-Maclaurin via 0/0: x/(e^x-1) at x=0**
    (`experiments/euler_maclaurin_0_over_0.py`,
    `data/euler_maclaurin_0_over_0_data.json`): B(x) = x/(e^x-1) -> 1
    as x->0 (error 5e-14).  Taylor coefficients match Bernoulli numbers.
    Sum-integral correction for f(x)=x^2: EM correction matches exact.

    **Sequel 2026-08-17 — Laplace method via 0/0: I(n)*sqrt(n) at n=0**
    (`experiments/laplace_method_0_over_0.py`,
    `data/laplace_method_0_over_0_data.json`): Gaussian integral
    I(n)*sqrt(n)->sqrt(pi) (error 0).  Quartic: I(n)*n^{1/4}->Gamma(1/4)/2
    (error 4.44e-16).  Both are 0/0 at n=0 with removable values.

    **Sequel 2026-08-17 — Wallis product via 0/0: 1^inf product -> pi/2**
    (`experiments/wallis_product_0_over_0.py`,
    `data/wallis_product_0_over_0_data.json`): prod (2n)^2/((2n-1)(2n+1))
    converges to pi/2 (error 3.93e-08 at N=10^7).  Each factor -> 1 (the
    1^inf indeterminate form).

    **Sequel 2026-08-17 — Cesaro summation via 0/0: Grandi 1-1+1... -> 1/2**
    (`experiments/cesaro_summation_0_over_0.py`,
    `data/cesaro_summation_0_over_0_data.json`): Cesaro mean of Grandi
    series -> 0.5 (error 0).  Geometric formula (1-r^{N+1})/(1-r) at r=1
    is 0/0, removable=N+1.

    **Sequel 2026-08-17 — Fermat's little theorem via 0/0: (a^{p-1}-1)/(a-1)**
    (`experiments/fermat_little_0_over_0.py`,
    `data/fermat_little_0_over_0_data.json`): 0/0 at a=1, removable=p-1.
    Verified for all primes 2..47.  Q(a) mod p=0 for gcd(a,p)=1.

    **Sequel 2026-08-17 — FTA via 0/0: f(z)/(z-z0)^k at root z0**
    (`experiments/fta_0_over_0.py`,
    `data/fta_0_over_0_data.json`): mpmath 80-digit precision.
    Simple/double/triple/complex roots all converge to removable value.
    Max error 6e-12.  Removable = g(z0) = f^{(k)}(z0)/k!.

    **Sequel 2026-08-17 — Pythagorean theorem via 0/0: (a/c)^2+(b/c)^2=1**
    (`experiments/pythagorean_0_over_0.py`,
    `data/pythagorean_0_over_0_data.json`): 16 Pythagorean triples,
    continuous parameterization, degenerate limit.  All ratios = 1.0.
    0/0 at c=0, removable=1 (the unit circle).

    **Sequel 2026-08-17 — Taylor remainder via 0/0: R_n/(x-a)^{n+1}**
    (`experiments/taylor_remainder_0_over_0.py`,
    `data/taylor_remainder_0_over_0_data.json`): mpmath 80-digit.
    Tests e^x, sin, cos, ln at various expansion points and orders.
    Max error 2e-13.  Removable = f^{(n+1)}(a)/(n+1)!.

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
   Δ=0.0197);    **C4 decided toward Poisson** — ⟨r⟩=0.372 at 100 modes vs Poisson
   0.3863 / GOE 0.5307, so the T19 "consistent chaos" spectral signature is
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
| **Selberg unification** (PAPER) | 30 eigenvalues ↔ 196 Mersenne geodesics, ε(2)=0.000265 | ε(2)=0.000265 is real **but it is algebra**: `L_total = L_traj + Σ L_k` is the code's own construction (`L(s)=C₀·ζ(s)` is flagged tautological in the code). Spectral-vs-zeros match is poor (code: min |t_n − t_zeta| ~ 2.5–9.0 "not a match by any standard"). **Closed 2026-08-08, corrected 2026-08-14** (`data/selberg_paradigm_data.json`): at 100 modes the spectrum is **Poisson** (⟨r⟩=0.372, GOE 0.5307 excluded at 5.5σ, KS p=0.0034 vs GOE Wigner / p=0.744 vs Poisson), the zero correspondence is untestable at this scale and structurally impossible (disk Weyl density ≈516× the zeros' density), and the 173 clean Mersenne lengths show no spectral-form-factor peaks (mean pct 51.7 vs matched null) — not a concrete Selberg instance. |
| **Partition function match** (PAPER) | L(2)=40.14 vs C₀·π²/6=40.19 (<0.2%) | **Tautology.** C₀·π²/6 = 40.1936 holds for *any* C₀; the code flags `L(s)=C0*zeta(s)` as a tautology "for ANY constant C0." A match by construction is not a test. |
| **Thermodynamics/entropy** | ln-thinning ↔ entropy; second law as folding | Analogical, not falsifiable as stated |
| **Prime geodesic spectrum** (PAPER §8.4, 2026-08-08) | prime-indexed states define a geodesic spectrum mirroring the arithmetic of primes; recurrence times factor into primes | **Not supported.** C0-at-primes = uniform energy conservation (ratio 0.999); the spectrum is a transient of the first N≈50 states (μ=0.027, not 0.065) and diverges by N=214; the frictionless flow has **zero** near-recurrences before escaping the bounded disk, so the recurrence claim is unmeasurable. `data/prime_time_data.json` |
| **T-symmetry of the integrator** (PAPER/L.O.R.E., 2026-08-08) | reversal error 0.003 | A **dt-dependent numerical bound, not a physical symmetry** — superconverges O(dt^6.9) near the origin crossing (8.9e-3 → 5.9e-7 over dt 5e-4→1.25e-4). `data/time_reversal_convergence_data.json` |
| **PUM §10.1 four-pack (T65)** | P1 τ~entropy; P2 T-symmetry; P3 holographic MI; P4 CTC fixed point | **0.5/4 confirmed.** P1 = tautology (τ := exp(entropy) in source); P2 refuted (recon err ≈ 1.8); P4 refuted (converged fraction 0.0); P3 weakly positive (MI 0.034 vs null 0.009) but synthetic. See `data/t65_fourpack_results.json` |
| **Decentral Bank (T68)** | routing is ownership; double-entry ledger + nonce rejects double-spend; witness quorum catches faulty transfers; anomaly layer flags outliers | **New, measured.** T1–T6: routing deterministic with a real partition spread (min 6 / max 111 / σ 34 over 16 fragments); integrity conserved exactly over 3000 txs; nonce replay rejected; 30% damage survives; quorum catches *every* faulty send below 40% corruption while honest availability holds — but collapses at ≥50% corrupt neighbourhoods (caught-frac 1.0 → 0.23–0.27), i.e. **quorum is majority honesty, not BFT** (crease #16). Anomaly recall 0.51 / precision 0.63 vs random null 0.019. Addresses the AUDIT §1 "no ledger/consensus/transaction layer" gap at toy scale. See `data/decentral_bank_data.json` |
| **Decentral Bank hardened (T68 Ph.1) + bridge (T69)** | Ed25519 account signatures verified at append & re-validation; WAL persistence + replay; on/off-ramp against a centralized bank via a custody-holding gateway | **New, measured.** T7: tampered block, wrong-key signature, and address-spoof all rejected, legit tx still commits. T8: save/load reproduces bit-identical heads + conserved balances. T69: on-ramp credits DCN 1:1, off-ramp pays fiat 1:1; ref replays settle nothing twice; backing invariant `custody + reserve_DCN == initial` holds to diff 0.0 under 300 randomized ops with 170 ref replays and forged over-withdrawals rejected. Honest walls: single-key custody (no threshold/HSM), mock bank (no network/TLS/KYC/AML), caller-supplied refs, no compensation path (crease #17). See `data/decentral_bank_bridge_data.json` |
| **Decentral Bank network (T70) + crash (T71) + sockets (T16/T17) + total-loss WAL (T18)** | every fragment a real OS process; PROPOSE→VOTE→COMMIT→NOTIFY first over a controllable relay, then over real TCP loopback sockets; replicas + SYNC/RESYNC; partition/equivocation/forgery/crash tests; per-node append+fsync WAL | **New, measured.** T12: 23 txs commit over real messages, all nodes' replicas bit-identical, replay conserves. T13: ring cut in two — 12–14/16 commit within halves, post-rejoin RESYNC converges to identical ledgers. T14a: forged block rejected at rate 1.0. T14b: scattered corruption collapses honest commits along the majority-honesty prediction P(f)=(1−f)⁴+4f(1−f)³ (four runs spanned {0.95–1.0, 0.56–0.63, 0.20–0.40, 0.0–0.13} at f={0,0.3,0.5,0.7}, theory {1.0, 0.65, 0.31, 0.08}; fluctuates run-to-run with relay timing but tracks theory) — crease #16 reproduced across processes — while *contiguous* corruption at f=0.7 keeps 0.25–0.67 (crease #18: corruption geometry, not just quantity, decides the quorum). T14c: partition equivocation creates a double-spend window; the fork is detected after rejoin, not healed. T15: a killed node's own accounts cannot transact while it is down (0/3) yet 8/8 live-owner commits survive; a STATELESS restart recovers every fragment — own included — from peers' replicas, re-converges, and commits a fresh tx. T16a/T16b: the same guarantees over REAL TCP sockets (no relay) — 14/14 commit, bit-identical replicas, partition re-converges. T17: a socket-killed node freezes its own accounts (0 commits) while live owners keep committing (k−1 > half witnesses), and a stateless socket restart rebuilds every fragment and commits again (crease #20: readiness must be quorum-attainable, not fabric-complete). T18: TOTAL simultaneous kill — every replica gone from memory, only each node's OWN chain survives on its fsync'd WAL; restarting WAL-loads the own chains and the ring reassembles every fragment from its owners; post-rebuild heads/block-counts match pre-crash exactly, converged, valid, conserved, fresh tx commits (crease #21: replicas are caches; the own WAL is the durability floor for total loss). T19: the whole socket layer wrapped in MUTUAL TLS (shared self-signed identity, CERT_REQUIRED both ways) — a client without the identity is rejected at the handshake and can exchange no bytes, yet 14/14 commit, replicas bit-identical, and a crash+restart re-establishes the encrypted fabric and re-converges. T20: host parameterized and the same consensus + TLS run over the machine's real LAN NIC (192.168.100.241) — 14/14 commit, bit-identical replicas, crash+restart re-converges over the NIC; transport proven beyond loopback. Still majority-honesty, not BFT; real mutual-TLS over a LAN NIC but one machine — no true two-host transport, one shared test identity (no per-node PKI); an OS crash mid-commit could tear the log. See `data/decentral_bank_net_data.json` |

| **Decentral Web (T73)** | content-addressed P2P "web" over real TCP processes: pages publish once and replicate to one verifying archive; nodes die/survive; near-miss names resolve by embedding; plus the plug-and-play UI that runs any function/experiment from auto-discovered forms | **New, measured (structural, seeds 42/11/7 + mutual TLS).** W1: a page published on one node is served (with verified content-address integrity) from EVERY node — one chain head, one length, all archives verify, all name sets agree. W2: 3 publishes of 2 distinct contents dedup to 2 SHA-256 addresses; GET by address is an O(1) store lookup. W3: a killed node's pages stay served by survivors; a stateless restart resyncs bit-identical (head + length + names equal, verify True). W4: "homee" resolves to "home" by nearest char-ngram embedding — the google.com→gooogle.com routing pattern from the real top-1M net, over the wire. Tamper: a flipped content byte breaks the content address while the other node stays valid. Honest walls: driver-sequenced ordering (a distributed total-order primitive is unbuilt — the T14c/bazaar wall), toy embedding over a few pages, one machine (transport is IP-parametric), no incentives/crypto identity beyond channel TLS. Assembly of already-verified machinery (T70 sockets, LedgerChain, T55i embeddings), not new physics — its novelty is the *reuse surface*. See `experiments/decentral_web.py`, `data/decentral_web_data.json`, `docs/DECENTRAL_WEB.md` |
| **Learning & Creativity Test (T74)** | a test ascertaining LEARNED and CREATIVITY in a learning environment: does a learner acquire a curriculum and persist it, and can it generate novel-but-valid content — one rubric (recognition/transfer for learned; novelty × appropriateness for creativity) reused by the human-assessment protocol in `docs/LEARNING_CREATIVITY_TEST.md` with the same thresholds | **New, measured (structural, synthetic concept space; seeds 42/11/7).** A stored-memory k-NN agent (majority vote over its 5 nearest stored exemplars — the repo's own k-NN primitive, K_NN=8 in decentral_net) in a bounded 2D concept space: L1 the acquisition curve — held-out probe accuracy climbs from near-chance 0.125 at 1 exemplar/concept to ≥0.90 at 40 (a sparse memory's k-neighborhood is dominated by OTHER concepts; a full one by the true concept). L2 no forgetting — first-taught concepts keep ≥0.92 after every later concept is added (additive stored memory does not destabilize). C1 creativity — a measurable share of mid-size near-miss variations are simultaneously NOVEL (outside the taught core, threshold from the taught exemplars' own spacings — the T55i/A1 doctrine) and VALID (inside the learned manifold, routed to the intended concept): ≥0.24 yield of never-presented new-but-right items. C2 novelty ≠ creativity — random far nulls are ~100% novel but 0% creative, so the joint novelty × validity criterion is necessary. C3 the landscape is interior-peaked — creative yield peaks at a middle mutation size (too-close valid-but-not-novel, too-far novel-but-not-valid). Honest walls: stored-memory k-NN over independent gaussian exemplars in a synthetic 2D space — MECHANISM claims about the test (environment→agent mapping measurable and reproducible), not transfer or open-domain invention. See `experiments/learn_creativity_test.py`, `data/learn_creativity_test_data.json`, `docs/LEARNING_CREATIVITY_TEST.md` |
| **Learning-Curve Scaling (T75)** | the T74 acquisition curve is a density effect, not an artifact of its one operating point: sweep the curriculum size C over the same space and router and check the sparse floor, the well-separated ceiling, and the saturation scale | **New, measured (structural, synthetic concept space; seeds 42/11/7).** Same stored-memory k-NN router over the same bounded disk, C swept 2→32: S1 the sparse floor is chance — at one exemplar/concept held-out accuracy tracks 1/C and strictly decreases with C over the well-separated regime {2,4,8,16} (0.50 → 0.25 → 0.125 → ~0.07; more competing concepts = a denser confusion field; K_VOTE clipped to min(5,C), ties still exactly chance). S2 the acquisition curve exists at every scale — the full-exposure ceiling holds ≥0.90 for every C∈{2,4,8}, so the dynamic range (ceiling − floor) grows with C (0.50 at C=2 → 0.82 at C=8). S3 capacity saturation — beyond the well-separated regime the ceiling collapses once adjacent home separation 2·HOME_R·sin(π/C) reaches a few exemplar-sigma (0.94 at C=8 → 0.61 → 0.42 → 0.30 at C=16,24,32), locating a real memory capacity C*≈π·HOME_R/(2·SIGMA)≈8 where T74's operating point sits; concordance (diagnostic): SIGMA=0.03 holds 0.89 at C=16, SIGMA=0.10 collapses to 0.59 at C=8 — the collapse tracks separation/σ. Honest walls: synthetic 2D space + stored-memory k-NN — MECHANISM claims about the learning environment, not natural curricula or real learners. See `experiments/learn_curve_scale.py`, `data/learn_curve_scale_data.json`, `docs/LEARNING_CURVE_SCALE.md` |
| **Human-Trial Instrument (T74 protocol)** | operationalize the T74 human protocol: a trial package (teaching set, held-out probes, three-effort creativity prompts, pre-registered thresholds + bars) plus a participant scorer — the same code that grades the machine — and a pilot showing the bars are attainable and discriminating | **New, measured (structural, simulated-participant pilot; seeds 42/11/7).** `data/human_trial_package.json` materializes the protocol; `score_participant()` grades any human's recorded answers on the engine's bars, on the same exemplars the learner was shown, with thresholds pre-registered on those exemplars. The pilot with archetypal simulations verifies the instrument: P1 a perfect participant (exact routing, mid-effort variations) attains every engine bar — L1 ceiling 1.0, L2 1.0, C1 mid creative ~0.24–0.36 ≥0.15, C2/C3 hold. P2 a random non-learner fails L1 (ceiling ≈ 1/C ≈ 0.13) and C1 (yield ≈ 0) — not passable by chance. P3 the joint novelty × validity criterion binds on both sides (the human C3) — trivial-effort items valid-but-not-novel (valid ~0.9 > novel ~0.25), wild-effort novel-but-not-valid (novel ~1.0 > valid ~0.0), mid-effort the only positive yield, a pure copycat exactly 0. P4 random far items grade ~100% novel but ~0% creative under the pre-registered thresholds — a facilitator cannot count novelty alone as creativity. Honest walls: the pilot participants are simulated archetypes, so the pilot validates the instrument (bars attainable + discriminating + rule consistent), not human behavior; a real trial hands the package to a human and scores with the same code. See `experiments/human_trial_pilot.py`, `data/human_trial_pilot_data.json`, `data/human_trial_package.json`, `docs/HUMAN_TRIAL_INSTRUMENT.md` |
| **Plug-and-play UI (puno-plug)** | one HTTP server, zero per-function code: every decorated plugin in `plugins/` and every experiment in `experiments/` is auto-discovered; forms are generated from declared or introspected params; functions run in-process, experiments as subprocess verdicts; results render as JSON | **New, structural (19 tests).** API: `GET /`, `/api/catalog`, `/api/plugin/<name>`, `/api/verdict/<name>`; `POST /api/run/<name>`, `/api/experiment/<name>`. Catalog auto-includes ~70 experiment verdicts + the plugin functions; a subprocess experiment run reproduces the pinned verdict bit-for-bit. See `puno_flow/plugin.py`, `puno_app/plugin_ui.py`, `tests/test_plugin_ui.py` |

---

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
     solvable-theorem pattern is now the norm: 63 verdict experiments
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
     `bazaar_hybrid`, `bazaar_net`, `decentral_web`, `learn_creativity_test`,
     `learn_curve_scale`, `human_trial_pilot`,
     plus the five
     earlier probes)
     each ship a claim/verdict JSON and are pinned by
     `tests/test_solvable_theorems.py` (67 tests; full suite 287, incl.
     `tests/test_human_trial.py`).  The
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
     decentral_web verdict (2026-08-11, T73) then rebuilds the WWW's functions
     on the same verified machinery — W1 a page published on one node serves
     from every node into one verifying content-addressed archive, W2 identical
     content dedups to one SHA-256 address with O(1) GET by address, W3 a
     crashed node's pages stay served by survivors with stateless-restart
      bit-identical resync, W4 a near-miss name resolves by char-ngram embedding
      routing (the google.com→gooogle.com pattern over the wire; honest walls:
      driver-sequenced ordering, toy embedding over a few pages, one machine,
      no incentives beyond channel TLS).  The
      learn_creativity_test verdict (2026-08-12, T74) then operationalizes the
      two-axis learned/creativity rubric on the repo's own machinery — L1 the
      acquisition curve (held-out probe accuracy climbs from near-chance 0.125
      to ≥0.90 as exemplar exposure grows 1..40/concept for a stored-memory
      k-NN router whose sparse-memory neighborhood is dominated by other
      concepts), L2 no forgetting (first-taught concepts keep ≥0.92 after every
      later concept is added), C1 a measurable novel-AND-valid yield (≥0.24 of
      mid-size near-miss variations route to the intended concept outside the
      taught core), C2 novelty ≠ creativity (random far nulls novel but
      invalid), C3 interior-peaked creative yield over mutation size; the same
      rubric and thresholds are the human-assessment protocol in
      `docs/LEARNING_CREATIVITY_TEST.md`.  The
      learn_curve_scale verdict (2026-08-12, T75) then shows that T74's
      acquisition curve is a density effect, not an artifact of its one
      operating point: S1 the sparse floor tracks chance 1/C and strictly
      decreases with curriculum size over C∈{2,4,8,16} (0.50→0.25→0.125→~0.07),
      S2 the full-exposure ceiling holds ≥0.90 for every C∈{2,4,8} so the
      curve's dynamic range grows with C (0.50→0.82), S3 beyond the
      well-separated regime the ceiling collapses at a critical curriculum
      size C*≈π·HOME_R/(2·SIGMA)≈8 where T74 sits (0.94 at C=8 → 0.30 at C=32;
      the collapse tracks separation/σ — SIGMA=0.03 holds 0.89 at C=16,
      SIGMA=0.10 collapses to 0.59 at C=8).  The
      human_trial_pilot verdict (2026-08-12) then makes the T74 human
      protocol concrete and validated: a trial package (teaching set, held-out
      probes, three-effort creativity prompts, pre-registered thresholds and
      bars) plus score_participant(), the same code that grades the machine,
      grading a human's answers on the engine's bars; the pilot with simulated
      archetypes shows a perfect participant attains every bar (P1), a random
      non-learner fails (P2), the joint criterion binds on both sides with a
      pure copycat at exactly zero (P3), and random far items are novel but
      never creative under the pre-registered thresholds (P4) — simulated
      archetypes validate the instrument, not human behavior.  The
      protocol is then RUNNABLE in a browser (`puno_app/human_trial_ui.py` +
      `puno_app/human_trial.html`, stdlib ThreadingHTTPServer):
      `python -m puno_app.human_trial_ui` walks a human through learn → route
      → re-check → produce and grades their downloaded answer sheet with the
      same score_participant() (POST /api/score), returning the same
      L1/L2/C1/C2/C3 verdict flags (pinned by tests/test_human_trial.py).  The
      internet-scale probes (2026-08-11) are now claim/verdict JSONs too:
     `decentral_net_internet` (I1–I4 all SUPPORTED — bulk-load 1,000,000 real
     top-1M sites, nearest-centroid routing over real geometry, 20% outage with
     no repair unit, 1000-site flow at ~862 ms/step), `decentral_net_union`
     (U1–U5 all SUPPORTED — 1,914,915 unique widely-used sites from two merged
     top-1M lists, ~2 KB/site holding, routed, outage-survived, checkpoint
     reloads bit-identically), `decentral_net_anomaly` (A1–A3 all SUPPORTED —
     name-space geometry as anomaly detector: 90% of DGA-shape random strings
     and 32% of known-bad below the legit p5 threshold, 18% of known-bad above
     the legit median as near-miss impersonation, but blocklist overlap makes
     geometry necessary-not-sufficient), and `decentral_net_t72` (T1–T3 all
     SUPPORTED — the real 1.9M-site internet flowed at 448,659 ms/step vs an
     all-pairs D of 58,670 GB, +7.8% spacing recovery after a 20% kill + heal,
     128-D wall measured at 19,076 ms/step on 10k real sites).  The
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
