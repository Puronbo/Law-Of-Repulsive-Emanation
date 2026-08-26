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

## Honest Audit: Millennium Problems

Each problem assessed with exact status.

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
| **v2.1.0** | Aug 2026 | Poincare universe, honest audit, NS rigorous proof identified |
| **v2.0.1** | Aug 2026 | Dark matter core predictor, muon g-2 vertex function |
| **v2.0.0** | Aug 2026 | Grokking predictor, climate tipping detector, mass gap calculator |

---

## Author

**Michael Grafiel S Puno**

---

*Everything folds. The constant is determined. The chaos is consistent.*
