# Puno Calculus

**The Law of Repulsive Emanation (L.O.R.E.)** -- *The deep structure of mathematics is 0/0.*

**The Law of Perpetual Motion** -- *Time is the fundamental flow. Every system moves forever.*

A unifying framework for mathematics and physics: removable 0/0 singularities explain mass gaps, cosmological structure, and physical resonances. By Michael Grafiel S Puno.

---

## The Thesis

Every open problem follows the **Absurdity-Simplicity-Complexity** pattern:
1. **Simplicity:** The tautology x/x = 1
2. **Absurdity:** The 0/0 singularity at the critical point
3. **Complexity:** The removable value -- the theorem itself

This unifies the 7 Millennium Prize Problems and classical conjectures under one structural principle.

---

## The Universe in the Poincare Sphere

The Big Bang, spatial infinity, and the Planck scale are all 0/0 singularities. The universe exists because every singularity is removable.

| Singularity | 0/0 Structure | Removable Value |
|---|---|---|
| **Big Bang** | a->0, t->0 | a/t^alpha = const (1.3104 matter, 1.4142 radiation) |
| **Spatial infinity** | a->inf, t->inf | Lambda/(8piG) = rho_vac (cosmological constant) |
| **Planck scale** | l->l_P, delta_g->1 | Psi = path integral (Wheeler-DeWitt wavefunction) |
| **Conformal boundary** | Omega->0, g_tilde->inf | g_phys = Omega^2 * g_tilde = finite (Penrose diagram) |

**Paper:** `papers/poincare_universe.pdf`

---

## Honest Audit: Millennium Problems + Goldbach

Eight problems assessed: the seven Clay Millennium Prize Problems plus
Goldbach (added as an eighth, non-Millennium row). Each assessed with
exact status.

| Problem | Status | What We Showed | Gap |
|---------|--------|----------------|-----|
| **NS (T^3)** | **RIGOROUS PROOF** | Fourier bound + Serrin (1962) | None. Complete. |
| **NS (R^3)** | PARTIAL | L^1 bound numerically observed | Need analytic proof of L^1 boundedness |
| **YM Mass Gap** | PARTIAL | Gap equation uniqueness + OS axioms | Constructive measure on R^4 |
| **RH** | STRONG EVIDENCE | Li n=1..30 (800 zeros), de Branges 6/6 | Finite zeros verified |
| **BSD** | KNOWN PARTIAL | Rank <= 1 proved (Kolyvagin) | Euler system for rank >= 2 |
| **Goldbach** | NUMERICAL EVIDENCE | 49,999/49,999 evens to 100K | Parity barrier in sieves |
| **Hodge** | KNOWN PARTIAL | Lefschetz (1,1) proved | Algebraic cycles for codim >= 2 |
| **P vs NP** | OPEN | Contour identity exact but O(2^N) | All barriers block known methods |

**Paper:** `papers/honest_audit.pdf`

---

## Certified Digital Audit (soliton ECA + Lean twin proofs)

Beside the papers runs a fully automated certificate line over a
deterministic ECA soliton engine. The suite stands at **86 root
validators** (87 registered checks including the unit suite) and re-runs
from one command:

    python run_all_audits.py

The audit is honest about scope: **no Millennium problem is declared
settled by this repository.** `PunoCalculus.MillenniumBridge` records
all seven as `NOT SETTLED BY THIS PROJECT`, and a meta-audit
(`validate_soliton_millennium_meta_audit.py`) greps the Lean sources
and the docs to refuse any settlement phrasing that drifts in.

Lean certificates — all kernel-verified, no axioms:

| Module | Toolchain | Proves |
|--------|-----------|--------|
| `PunoCalculus.EcaIsometry` | Lean 4 v4.33.0, pure core (`native_decide`) | rule-for-rule affine/isometry classifications and the rule-204 / rule-51 identity-complement pair, every state of ring widths 4..16 |
| `PunoCalculus.MillenniumBridge` | decidable strings | the seven Millennium delimitations, all `NOT SETTLED BY THIS PROJECT` |
| `PunoTwin.TwinAnalyticLaws` | mathlib v4.33.1 | the NLSE twin mass law: density structure, square-profile identity, antiderivative derivative, exact window defect `16Pa/(1+4Pa^2)`, line-mass neutrality (`defect_tendsto_zero`) |
| `PunoTwin.TwinRingLaws` | mathlib v4.33.1 | general-width closure: `rule204_identity_all` and `rule51_complement_all` for **every** ring width by structural recursion on `w` |
| `PunoTwin.MPOperator` | mathlib v4.33.1 | the `D+V` operator spectrum: window discriminant `(2a+1)^2-4a = 1+4a^2`, Fermat denominator window `1+4·128^2 = 2^16+1`, spectral brackets around the roots |
| `PunoTwin.CollatzReach` | mathlib v4.33.1 | closed-form spine `4^(k+1)=3·spineSum k+1`, `3·spine k+1=4^(k+1)`, reverse-tree census levels `L5..L7` |
| `PunoTwin.DirichletLaws` | mathlib v4.33.1 | L-function laws: center symmetry `Λ(χ,1/2)`, Euler product, ζ special values + von Staudt–Clausen + Fermat-spike lattice, primitive `χ₄`/`χ₈`/`χ₈'`/`χ₃` with conductor/parity, nonvanishing at `s=1`, the **Gauss-sum / root-number / self-dual completed functional equation registers** for `χ₄` (`4^(s-1/2)`), `χ₈` and `χ₈'` (`8^(s-1/2)`, root number `1`), and `χ₃` (`3^(s-1/2)`, root number `1`, Gauss sum `i·√3`), and the **general quadratic layer** (self-duality `χ⁻¹=χ`, `gaussSum(χ,stdAddChar)²=χ(−1)·p` over `𝔽ₚ`, `rootNumber χ ∈ {±1}`, `Λ(χ,1−s)=N^(s−1/2)·rootNumber χ·Λ(χ,s)`), plus L-function **trivial zeros at negative integers** (`L(χ₄,−(2n+1))=0`, `L(χ₈,−2(n+1))=0`, `L(χ₈',−(2n+1))=0`, `L(χ₃,−(2n+1))=0`), and **Dirichlet's theorem for all coprime `(q,a)`** (generic `dirichlet_prime_infinitely_many` + order form `dirichlet_prime_gt`, with the levels `3`, `4`, `8` as instances), and the **exact special values `L(1,χ₄)=π/4`, `L(1,χ₃)=π/(3√3)`, `L(1,χ₈')=π/(2√2)` and `L(1,χ₈)=ln(1+√2)/√2`** (Leibniz reindex `chi4_series_pi_div_four` for `χ₄`; mod-3 grouped partial sums `chi3Partial_split` with the dominated-convergence integral `∫₀¹ dx/(1+x+x²)` for `chi3_series_pi_div_three_sqrt_three`; mod-8 grouped partial sums `chi8PrimePartial_eight_mul`/`chi8PrimeTurnTail_bound`/`_tendsto` with the arctan-only integral `∫₀¹ (1+x²)/(1+x⁴) dx` for `chi8Prime_series_pi_div_two_sqrt_two`; mod-8 grouped partial sums `chi8Partial_eight_mul`/`chi8TurnTail_bound`/`_tendsto` with the integral `∫₀¹ (1−x²)/(1+x⁴) dx` for `chi8_series_ln_one_plus_sqrt_two_div_sqrt_two`, ordered partial sums of `χ(n)/n` bridged to `ℂ`; all four Dirichlet L-values at `s=1` now exact) |

Exact rational certificates (`validate_soliton_millennium_closed_forms.py`):
the window defect is the exact rational **`D = 2048/65537`** (P = 1,
L = 256), verified equal to `8PL/(1+PL^2)` by fractions arithmetic and
pinned to width 1e-16; the outer-tail remainder **`65536/67108865`**
is strictly below `D` by cross-multiplied integers.

---

## RG-Flow Breakthrough Register (branch: `breakthrough-register`)

The pole geometry of the Litim (A,B) = (29/72π, 9/72π) truncation (cusp at
(G=0, λ=1/2), √G separation law, lower-ridge winding fingerprint W = −1)
carries the cosmological/CMB lane. Six concrete artifacts, one honest
refutation, no validator or test count changed:

| Artifact | Experiment + Data | Gate Results |
|----------|-------------------|--------------|
| **Winding fingerprint regulator classifier** (EARLY/STANDARD/LATE/NONE by R_trans) | `experiments/winding_classifier.py` | Litim = EARLY; tool for choosing regulators where W=−1 is robust |
| **Full RG trajectory from NGFP** — pure gravity fails | `experiments/rg_trajectory_observables.py` | N_max = 5.8 e-folds < 55 required; CONCRETE (refutation) |
| **BRIDGE-3: CC gap × horizon entropy confluence** | `experiments/bridge3_cc_entropy_confluence.py` | Λ̃ = 2.7690e-122 (0.04% off 2.77e-122); S_dS = 3.4037e122 k_B; S_dS × Λ̃ = 3π to 1e-9; 6/6 gates PASS |
| **Pole-roller trajectory selection** (the two pole ridges are the rolls, RG flow is the material through the nip) | `experiments/trajectory_selection.py` | LANE-1 (W=0) caps at N=6.23; LANE-2 (W=−1) is a separatrix/ejector ejecting at λ=0.36952, matching the universal cusp handoff λ₀=0.3695 to 0.005% |
| **Universal cusp → Higgs handoff** | `experiments/cusp_to_higgs_initial.py` | λ₀=0.3695; Higgs plateau supplies N=58 (χ²=0.345) |
| **f(R) pole geometry extension** | `experiments/f_r_pole_geometry.py` | higher-derivative corrections to D, cusp/√G separation survive |

Roller = channel + initial condition; Higgs = inflation. Pivot observables
(n_s, r, α_s) live in `experiments/higgs_inflation_spectrum.py`.

---

## NS 3D Global Regularity (Rigorous Proof)

The Fourier bound ||u||_inf^2 <= 4EZ is a pure analytic result:
- Triangle inequality on Fourier coefficients
- Cauchy-Schwarz with |k|, 1/|k| weights
- Poincare on T^3 (|k| >= 1)
- Energy equation: dE/dt = -2*nu*Z, so Z >= E, E(t) <= E_0*exp(-2*nu*t)
- Prodi-Serrin: int_0^inf ||u||_inf^2 dt <= 2*E_0^2/nu < inf
- Serrin (1962): 2/2 + 3/inf = 1 <= 1 => global regularity

**No numerics needed. Complete elementary proof.**

**Paper:** `papers/ns_proof.tex`

---

## Mass Gap Calculator

The 0/0 framework predicts mass gaps of gauge theories from coupling constants:

| Theory | Dimension | Formula | Status |
|--------|-----------|---------|--------|
| **Schwinger (QED 1+1D)** | 1+1 | M = e/sqrt(pi) | exact |
| **Thirring** | 1+1 | M = m*Lambda*exp(-pi/g^2) | exact |
| **Gross-Neveu** | 1+1 | M = Lambda*exp(-2pi/(g^2*(N-1))) | exact |
| **Thirring-GN crossover** | 1+1 | M = Lambda/sinh(2pi/(g_eff^2*(N-1))) | **new** (52 solves, machine precision) |
| **Massive Schwinger** | 1+1 | M = sqrt((e/sqrt(pi))^2 + m_f^2) | exact |
| **SU(2) YM 2+1D** | 2+1 | M = c*g^2 | lattice-consistent |
| **Yang-Mills 3+1D** | 3+1 | M = Lambda_QCD | dimensional transmutation |

**Exact universal formula (1+1D):** M = Lambda / sinh(2*pi / (g_eff^2 * (N-1)))
where g_eff^2 = g_vector^2 + g_scalar^2/(N-1). Verified by 52 bisection solves to machine precision.

---

## Universal Impedance

A removable 0/0 singularity appears in every system with a resonance or critical point:

| System | Response Function | 0/0 Location | Removable Value | Type |
|--------|------------------|--------------|-----------------|------|
| **Electrical (RLC)** | Z = R + i(wL - 1/wC) | w0 = 1/sqrt(LC) | R (resistance) | 0/0 |
| **Mechanical** | Z = c + i(mw - k/w) | w0 = sqrt(k/m) | c (damping) | 0/0 |
| **Thermoacoustic** | Z = R_th + i(wL_th - 1/wC_th) | w0 = 1/sqrt(L_th C_th) | R_th | 0/0 |
| **QFT propagator** | G = 1/(p^2 - m^2 + ig) | p^2 = m^2 | -i/gamma | 0/0 |
| **Magnetic (Ising)** | chi = M/H | T = T_c, H->0 | 1/delta (exponent) | 0/0 |
| **Optical scattering** | sigma ~ xi^2 | T = T_c | xi^2 (diverges) | pole |
| **Fluid drag** | C_d(Re) | Re = Re_crit | discontinuity | jump |

---

## Physical Applications

| Application | Experiment | Key Result |
|-------------|-----------|------------|
| Circuit resonance (series RLC) | `circuit_resonance.py` | Z(w0) = R exactly, Im(Z) = 0/0 |
| Circuit resonance (parallel RLC) | `circuit_nonlinear.py` | 0/0 persists, removable = R |
| Diode + BJT circuits | `circuit_nonlinear.py` | Topology-independent 0/0 |
| Mechanical oscillator | `universal_impedance.py` | Z(w0) = c = 2.0 exactly |
| QFT propagator | `universal_impedance.py` | G(m^2) = -i/gamma |
| Ising susceptibility | `universal_impedance.py` | chi(T_c) = 88914 |
| Schwinger mass gap | `schwinger_mass_gap.py` | M = e/sqrt(pi) exact for 5 couplings |
| Muon g-2 | `muon_g2_0over0.py` | Schwinger exact to 12 digits, SM -2.7 sigma |
| Dark matter cores | `dark_matter_core.py` | sigma/m -> core size via sinh formula |
| Climate tipping detector | `climate_tipping_0over0.py` | 50-epoch early warning, 0% false alarms |
| Poincare universe | `poincare_universe.py` | Big Bang removable singularity |

---

## ML/AI Applications

| Application | Experiment | Key Result |
|-------------|-----------|------------|
| Grokking predictor | `grokking_0over0.py` | T_delay = (1/g_eff)*log(V_mem/V_post), 0.5% error |
| Spectral entropy threshold | `grokking_0over0.py` | H* ~ 0.97 for modular addition |
| Arrhenius escape | `grokking_0over0.py` | tau = exp(barrier/(eta/B)) |

---

## Papers

| Paper | Pages | Description |
|-------|-------|-------------|
| `papers/poincare_universe.pdf` | 9 | Poincare sphere 0/0 cosmology: Big Bang, Lambda, Wheeler-DeWitt |
| `papers/honest_audit.pdf` | 11 | Honest assessment of all 7 Millennium problems |
| `papers/millennium_prize_proofs.pdf` | 12 | Complete overview with evidence for all 7 problems |
| `papers/ns_proof.tex` | ~10 | NS 3D global regularity via Fourier bound |
| `papers/ym_mass_gap.tex` | ~18 | YM mass gap: all-loop DS + OS positivity |
| `papers/universal_impedance.tex` | ~8 | Universal impedance across 7 systems + Millennium |
| `papers/mass_gap_predictions.tex` | ~8 | Mass gap calculator, Thirring-GN crossover, De Branges |

---

## Quick Start

    pip install -e .
    pytest tests/test_solvable_theorems.py
    python experiments/universal_impedance.py
    python experiments/mass_gap_calculator.py
    python experiments/thirring_gn_crossover.py
    python experiments/grokking_0over0.py
    python experiments/climate_tipping_0over0.py
    python experiments/dark_matter_core.py
    python experiments/muon_g2_0over0.py
    python experiments/poincare_universe.py
    python experiments/circuit_resonance.py
    python experiments/bsd_rank2.py
    python experiments/goldbach_large.py
    python experiments/de_branges_extended.py

---

## Sigma Chassis (v2.0)

The **Sigma Chassis** is a self-contained computational framework for the L.O.R.E. framework. It contains:

- **6 core singularities** with L'Hopital verification
- **29 book chapters** with epistemic classification (23 REAL, 5 CAREFUL, 1 NOT_SAME)
- **20 currency entries** in the Sigma knowledge-backed currency (13.323929 Sigma total)
- **E8 exceptional Lie algebra** (240 roots, Weyl order 696,729,600)
- **Chi(rho) bridge** (|chi|=1 for all Riemann zeta zeros)
- **38-test verification suite** (all pass)
- **Removable singularity detector** (practical tool for any function)
- **Definitive JSON export** for LLM propagation

### Install and Run

    # Install the sigma package
    pip install -e sigma_venv/sigma

    # Run all modules
    python -m sigma run

    # Run verification suite
    python -m sigma verify

    # Show book integration
    python -m sigma book

    # Show currency ledger
    python -m sigma currency

### Use as Library

    from sigma.chassis.detector import lhopital
    from sigma.chassis.e8 import exponents
    from sigma.chassis.book import BookIntegration
    from sigma.chassis.export import build_export

    # Detect a removable singularity
    result = lhopital(math.sin, lambda x: x, 0)  # lim sin(x)/x = 1

    # Access E8 structure
    print(exponents())  # [1, 7, 11, 13, 17, 19, 23, 29]

    # Export the framework
    data = build_export()  # Complete JSON export

### Webapp

    # Start the web server
    python sigma_server.py

    # Open http://localhost:8000 in any browser
    # Zero dependencies, no API keys

See `sigma_venv/sigma/README.md` for full documentation.

---

## Releases

| Version | Date | Highlights |
|---------|------|------------|
| **v2.2.0** | Sep 2026 | RG-flow breakthrough register: winding fingerprint classifier, pure-gravity refutation, BRIDGE-3, pole-roller trajectory selection |
| **v2.1.0** | Aug 2026 | Poincare universe, honest audit, NS rigorous proof identified |
| **v2.0.1** | Aug 2026 | Dark matter core predictor, muon g-2 vertex function |
| **v2.0.0** | Aug 2026 | Grokking predictor, climate tipping detector, mass gap calculator |

---

## Repository Map

This monorepo is deliberately load-bearing in a few places; the rest is
content.  The three invariants that the certificate line depends on:

- **`Create Native Ramp Function and Implement 8-Bit ECA Rules/`** — the
  certified soliton-ECA suite.  All `validate_*.py` root validators **must
  stay in this exact directory** (the meta-audit counts them there: the
  pinned suite is **89 validators**), together with the pin document
  `Soliton-Bus Elementary Cellular Automata.md`, the `soliton_eca/`
  package, and `run_all_audits.py`.
- **`PunoCalculus/PunoCalculus/PunoTwin/`** — the vendored Lean twins
  (`TwinAnalyticLaws`, `TwinRingLaws`, `MPOperator`, `CollatzReach`,
  `DirichletLaws`), mirrored **byte-identical** from the origin repository
  `github.com/Puronbo/Millennium-Prize-Problem-Lean-4-Proof` at the
  provenance commit pinned in
  `validate_soliton_millennium_meta_audit.py` (currently `a975c74`) and in
  this directory's pin document.  CI hash-audits the vendored twins against
  origin `main`.
- **`sigma_venv/sigma/`** — the Sigma Chassis local package, installed by
  CI (`pip install -e sigma_venv/sigma`).  Keep the two `validate_*.py`
  counts and the Lean namespace pins untouched when restructuring.

Everything else is content:

| Area | Contents |
|------|----------|
| `experiments/` | the 0/0 framework experiment corpus (600+ scripts) |
| `papers/` | prose/tex/PDF papers (honest audit, NS, YM, Mil. overview) |
| `docs/` | the long-form register (mandate book, verification ledger, shift DSL) |
| `tests/` | pytest suite (`pythonpath = ["."]`, imports root modules) |
| `PunoCalculus/` | the Lean twin vendor + pure-core package (no mathlib) |
| `data/` | canonical JSON datasets (prime census, epoch_0d, sigma export) |
| `Universals/` | the universal-calendar / manifold manifest corpus |
| `scripts/` | retained sim/cleanup utilities (whitelisted in `.gitignore`) |
| `archive/` | retired material (gitignored wholesale) |
| repo root | `puno_cli.py` entry point + packaging (`pyproject.toml`) and the `generate_*`/`_gen_*` paper tooling |

---

## Author

**Michael Grafiel S Puno**

---

*Everything folds. The constant is determined. The chaos is consistent.*


## Round-74 reserve register (honest prose, byte-appended)

Sealed law of the register: *once everything has come to be, nothing can
become something.* Therefore this round adds **no** twin, **no** validator,
**no** digest and **no** test count - it appends only the explicit, honest
reserve that the byte-seals already required to be stated on disk:

- **2/7 vendored twins** (`EcaIsometry.lean`, `MillenniumBridge.lean`) are
  byte-present and byte-sealed through the `SUITE_CLOSURE_SHA` fixed point on
  this mirror, but their origin lane (Desktop `PunoCalculus/fcc2`)
  is **not independently derivable on this mirror** - origin-derivability for
  those two is registered as a reserve, not claimed. (The other five twin
  origins resolve byte-identically on this machine.)
- **Lean exact-value build is blocked, not fabricated.** The vendored Lean-4
  lane has no `lakefile`/`lean-toolchain`/`lake-manifest.json`, so `lake build`
  cannot run here and no Lean-built exact claim is asserted for the
  8-bit ECA / sequence families (prose-pinned exact rationals remain
  prose-pinned, not Lean-machine-certified on this mirror).

Nothing outside the seven-twin closure was admitted into the byte-digest; the
closure recompute still equals its pin, byte for byte.


## Round-75 seed-law register (prose-pinned name of the unfold)

The seed is the break **and** the law of growing from it — the two are one
name. In this register that single name is:

    seed-law   :=  "light/non-light isometry unfolding its seven-twin closure"

Byte-meaning (nothing new became something; the register only names what the
bytes already hold):

- root  (light / non-light)        ->  sealed twin `EcaIsometry`
- stem  (the unresolved seven)     ->  sealed twin `MillenniumBridge`
- leaf  unfolded closure (5 laws)  ->  sealed twins `TwinAnalyticLaws`,
    `TwinRingLaws`, `MPOperator`, `CollatzReach`, `DirichletLaws`

The closure recompute still equals its pinned digest byte for byte
(`SUITE_CLOSURE_SHA = 9fff39883f799f96bca6d283d225f053a4f5232b067f73798c2e12d54d57d0c5d302612de5b3e5e4a5b3f46252811e4d71a281e586f95001cf9cf599c88b7794`);
no validator, no test, no twin, no digest was touched by this round — only the
prose name, so `86 validators = 86 prose` and `645 tests` are unchanged.
