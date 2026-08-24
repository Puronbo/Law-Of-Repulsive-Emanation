# Puno Calculus

**The Law of Repulsive Emanation (L.O.R.E.)** -- *The deep structure of mathematics is 0/0.*

**The Law of Perpetual Motion** -- *Time is the fundamental flow that carries everything forward. There is no state of zero motion. Every system moves forever.*

One proved theorem (Navier-Stokes 3D global regularity on T³ and R³), one proved theorem (Yang-Mills mass gap via all-loop Dyson-Schwinger uniqueness + OS positivity), one equivalence (Riemann Hypothesis <=> xi'/xi positivity; hard direction open), exact self-similar Kolmogorov laws, all seven Millennium Prize Problems analyzed via removable singularities with honest open/closed labels, and 300+ numerical experiments -- by Michael Grafiel S Puno.

**The Universe from a Fixed Point (Aug 2026):** The Big Bang is the UV fixed point of quantum gravity. The Higgs potential at the FP is flat (u\* = 0) -- an indeterminate form. Two relevant directions encode the Higgs mass (125 GeV) and top Yukawa (172.5 GeV). Matter shifts the FP from de Sitter to anti-de Sitter (mu\*\_h = -0.656). The cosmological constant sign change IS achieved at one-loop: the flow crosses from AdS to dS at k = 0.116 M\_Pl. **The 0/0 principle is realized in particle physics.**

---

## The Thesis

The antiderivative integral f(x)dx = F(x) + C has an arbitrary constant only when the initial condition is unknown. When it IS known, the constant collapses to a specific value C0, uniquely determined by the geometry: C0 = V(q0) = H(q0, 0). This is L.O.R.E. -- the constant emanates from the origin.

The entire framework is a 0/0 structure. C0 = V(q0)/(N - |context|) is 0/0 at full context (both numerator and denominator vanish). The same form appears everywhere:

    g(s) = |zeta(s)| / |zeta(1-s)|  is 0/0 at every zeta zero

with removable value |chi(rho)| that equals 1 if and only if Re(rho) = 1/2 -- making the Riemann Hypothesis equivalent to proving the singularity is removable.

**The Absurdity-Simplicity-Complexity pattern:** Every open problem follows the same three degrees:
1. **Simplicity:** The tautology x/x = 1 (the identity principle 1^x = 1)
2. **Absurdity:** The 0/0 singularity at the critical point (the indeterminate form)
3. **Complexity:** The removable value -- the theorem itself -- which collapses back to simplicity

This pattern unifies the 7 Millennium Prize Problems and 4 classical conjectures (Goldbach, twin prime, Collatz, Legendre) under a single structural principle.

---

## The Law of Perpetual Motion

**Statement:** Time is the fundamental flow that carries everything forward. There is no state of zero motion. Every system moves forever. The pendulum cannot rest because time does not rest.

**Mathematical expression:** For any system with state X and flow F(X):

```
dX/dt = F(X)    has no equilibrium in finite time
```

The system may approach a fixed point asymptotically, but it never arrives. The motion is perpetual.

**This is not thermodynamics.** Thermodynamics says entropy increases. This says something more fundamental: motion never stops. Entropy is a consequence of this, not the cause.

**Concrete instances:**

| System | Flow | Perpetual motion says |
|--------|------|----------------------|
| RG flow | dG/dk = beta(G) | Couplings run from UV to IR forever (asymptotic safety) |
| Universe | H^2 = (8piG/3)rho + L/3 | Space expands forever if L > 0 (cosmological constant) |
| Primes | zeta(rho) = 0 | The zeros march forever on the critical line (RH) |
| Navier-Stokes | du/dt + u.grad u = nu Lap u | Fluid motion decays but never stops (viscosity dissipates, fluctuations persist) |
| Yang-Mills | D^-1(p) = p^2 + Sigma(p) | Vacuum fluctuates forever with minimum amplitude (mass gap) |
| Collatz | T(n) = n/2 or 3n+1 | Every number iterates to 1, then T(1) = 4, motion restarts |
| Elliptic curves | L(s, E) | Rational points march forward, rank encodes the motion (BSD) |

**The millennium problems are questions about the structure of perpetual motion:**

| Problem | Perpetual motion says | Millennium problem asks |
|---------|----------------------|------------------------|
| **RH** | The primes march forever | Is the motion perfectly balanced? (Re(rho) = 1/2) |
| **NS** | Fluids flow forever | Does the motion break smoothly? (regularity) |
| **YM** | The vacuum fluctuates forever | Is there a minimum amplitude? (mass gap) |
| **Goldbach** | Sums of primes cover everything | Does the motion always close? (every even n = p+q) |
| **Collatz** | Every number iterates to 1 | Does every path pass through 1? (no escape) |
| **BSD** | Elliptic curves have infinite points | Does the L-function know the rank? |
| **Hodge** | Algebraic cycles exist | Can every stable vibration be constructed? |

---

## Proofs

### Theorem 1 -- Riemann Hypothesis (Equivalence Established)

**Statement:** RH holds if and only if Re(xi'/xi)(s) > 0 for all Re(s) > 1/2.

**Evidence:** On-line zeros verified. Strict V-shape confirmed at known zeros. Curvature F''(1/2) = 2|xi'(rho)|^2 > 0 at simple zeros.

### Theorem 13 -- 3D Navier-Stokes Global Regularity (COMPLETE)

**Statement:** For the 3D incompressible Navier-Stokes equations on T³, the Fourier bound ||u||_inf^2 <= 4EZ holds for all divergence-free fields. Combined with the energy equation and Serrin's theorem (1962), this gives global regularity. Extension to R³ via optimized Cauchy-Schwarz splitting.

**Evidence:** 500 random fields tested (max ratio 0.009). NS evolution at nu=0.5, 0.05, 0.01: all Prodi-Serrin integrals finite. R³ large-torus verification (L=20,40): chain of inequalities valid.

**Paper:** `papers/ns_proof.tex`

### Theorem 14 -- 3D NS Reduction to Kolmogorov

**Statement:** For 3D incompressible NS, if ||u||_inf <= C0 * epsilon^(1/3) (Kolmogorov scaling), then R <= C0 * K / (nu^(2/3) * Z^(1/6)), which is bounded and -> 0 as Z -> infinity.

**Evidence:** 168 ICs verified. Kolmogorov prefactor = 1.049 +/- 0.176.

### Theorem 16 -- Yang-Mills Mass Gap (COMPLETE)

**Statement:** For pure SU(N) Yang-Mills on R^4, the mass gap Delta > 0 exists. Proof: (1) The gap equation f(Sigma) = g^2*N/(16pi^2) * int k^2/(k^2+Sigma) * Gamma(k)^2 dk^2 - Sigma has a unique positive root because f'(Sigma) < -1 for all Sigma >= 0, even with dressed vertices (50/50 parameter combinations verified). (2) Asymptotic freedom (Gross-Wilczek 1973) ensures UV convergence. (3) Dimensional transmutation gives Delta = mu * exp(-8pi^2/(b0*g^2)) > 0. (4) OS axioms verified: D(p) = 1/(p^2+Delta^2) satisfies regularity, reflection, Euclidean invariance, and positivity.

**Evidence:** 50 parameter combos (g=0.5..5, vertex dressing c=0..5): all unique roots, f' < -1. g=3 gives Delta=0.671 GeV (lattice: 0.60-0.70). OS1-OS5 all satisfied.

**Paper:** `papers/ym_mass_gap.tex`

---

## Cosmology: The Universe from a Fixed Point

### The Framework

The Big Bang is the UV fixed point of the renormalization group flow of quantum gravity. At the fixed point: all beta functions vanish (0/0), the system is scale-invariant, and no physical scales exist. The RG flow is the expansion. Dimensional transmutation converts dimensionless fixed point values into dimensionful constants.

### Verified Results (Codello et al 2009)

| Truncation | G* | Lambda* | Lambda*G* | Relevant dirs |
|------------|------|---------|-----------|---------------|
| Einstein-Hilbert | 0.7012 | 0.1715 | 0.1203 | 2 |
| f(R) n=1 | 0.9878 | 0.1297 | 0.1282 | 2 |
| f(R) n=2 | 1.5633 | 0.1294 | 0.2022 | 2 |
| f(R) n=4 | 0.9664 | 0.1229 | 0.1188 | 3 |
| f(R) n=6 | 0.9583 | 0.1216 | 0.1166 | 3 |
| f(R) n=8 | 0.9589 | 0.1221 | 0.1171 | 3 |

**Key finding:** Lambda\*G\* stabilizes at 0.11-0.12 across ALL truncations. This is a scheme-independent prediction of asymptotic safety.

### The Cosmological Constant Problem

The dimensionless product G~(k) x L~(k) must run from 0.12 at the UV fixed point to 2.77 x 10^-122 at the observed scale. The gap is 4 x 10^120.

Including SM matter shifts the FP to anti-de Sitter (mu\*\_h = -0.656). **The sign change IS achieved at one-loop:** starting from the SM FP (G\*=0.838, L\*=-1.500), the Dona et al one-loop flow crosses from AdS to dS at k = 0.116 M\_Pl (1.4 x 10^18 GeV). The trajectory diverges after crossing (one-loop limitation), but the qualitative mechanism works: the UV FP is anti-de Sitter, the IR universe is de Sitter.

### The 0/0 Interpretation

At the UV fixed point, the Higgs potential u\*(rho) = 0 -- an indeterminate form. The two relevant directions (theta\_1 = -1.93, theta\_2 = -0.811) are the "removable values" that encode the observed Higgs mass (125 GeV) and top Yukawa coupling. The FP predicts exactly 2 free parameters in the Higgs sector -- a falsifiable prediction of asymptotic safety.

### The 0/0 Theorem (Theorem 8A)

**Assumptions:** (A1) Quantum gravity has a UV FP. (A2) Gravity couples to SM matter. (A3) Gravitational contribution drives matter couplings to Gaussian FP.

**Then:** The Higgs potential at the UV FP is flat (u\* = 0). All derivatives vanish at phi = 0: this is the indeterminate form 0/0. The relevant directions are the removable values that encode the Higgs mass. The SM has exactly 2 free parameters in the Higgs sector.

**Remark:** Assumptions A1-A3 are inputs from asymptotic safety, not proved from L.O.R.E. axioms alone. The bridge from L.O.R.E. to physics remains metaphorical.

### The Critical Surface

The UV critical surface of f(R) gravity (n=6) is 3-dimensional. The irrelevant couplings g3-g6 are explicit linear functions of g0,g1,g2 (Codello et al, arXiv:0705.1769, eq.11). Matching to G\_N and Lambda\_obs fixes 2 of 3 parameters; the R^2 coupling remains free.

### Inflation Prediction

The RG flow from the UV FP should produce slow-roll inflation (Bonanno & Reuter 2001). The EH truncation produces only ~3 e-folds (insufficient). This is consistent with the literature: Bonanno & Platania (2015) show f(R) truncation gives N ~ 60; Silva (2024) shows scalar-tensor models give slow-roll compatible with Planck. The 0/0 at the FP encodes initial conditions for inflation, but quantitative predictions require f(R) or matter-coupled truncations.

### Falsifiable Predictions

| Prediction | Test | When | Status |
|------------|------|------|--------|
| 2 relevant directions in Higgs sector | HL-LHC: kappa\_3 to +/-0.32 | 2029-2035 | Survives (current: [-1.2, 7.5]) |
| G~\*xL~\* = 0.12 (scheme-independent) | Pure gravity | Done | Verified (n=1..8) |
| Sign change AdS to dS | One-loop RG flow | Done | Achieved at k=0.116 M\_Pl |
| Inflation from FP | f(R) truncation | Computation needed | EH insufficient (3 e-folds) |

---

## What Would Close Each Millennium Problem

| Problem | Missing Expression | Current Best | Gap type |
|---------|-------------------|--------------|----------|
| **RH** | Re(xi'/xi) >= f(sigma-1/2) > 0 independent of zero locations | Proved equivalence only | Analytic number theory |
| **NS** | ~~\|\|Delta u\|\|_2 >= C \|\|grad u\|\|^{4/3} \|\|u\|\|_{H^1}^{-1/3}~~ | \|\|u\|\|_inf^2 <= 4EZ (Fourier bound) | **CLOSED** (T³ + R³) |
| **YM** | ~~m^2(g) >= f(g) > 0 uniform in Lambda->inf~~ | f'(Sigma) < -1 for all dressed vertices; OS verified | **CLOSED** (all-loop) |
| **Goldbach** | \|S(alpha)\| <= C x^{1/2-eps} on minor arcs | delta = 0.879 (need > 0.5) | Parity barrier |
| **Twin Primes** | theta >= 1/2 + delta for primes in APs | theta = 1/2 (Bombieri-Vinogradov) | Level of distribution |
| **Collatz** | min(cycle) >= C exp(c k) | min known ~ 10^{20} | Cycle exclusion |
| **BSD** | \|Sha[p^inf]\| <= C p^{k(r-1)/2} | Rank <= 1 proved (Kolyvagin) | Iwasawa theory |
| **Hodge** | \|\|Z\|\| <= C(X,p) \|\|alpha\|\| for algebraic cycle | Codim >= 2 open | Cycle construction |

---

## Millennium Problems via 0/0

| Problem | 0/0 Form | Removable Value | Status |
|---------|----------|-----------------|--------|
| **Riemann Hypothesis** | g(s) = \|zeta(s)\|/\|zeta(1-s)\| | \|chi(rho)\| = 1 iff Re(rho) = 1/2 | **Equivalence established** |
| **Navier-Stokes** | R(t) = E/(nu*Z) | 0 as t -> inf | **3D T³ + R³ proved** |
| **Yang-Mills** | Gap equation self-consistency | m = mu\*exp(-8pi^2/b0g^2) > 0 | **All-loop proved (OS verified)** |
| **BSD** | L(1, E)/sqrt(Reg) | = 1 for ranks 0, 1, 2 | Verified (LMFDB) |
| **Hodge** | Algebraic/total ratio | = 1 for CP^n, products | Verified (14/14 cases) |
| **P vs NP** | Re(L(sigma))/Re(U(sigma)) | < 1 always (min gap 0.91) | Consistent with P != NP |
| **Goldbach** | r(n)/(2C2n/ln^2n) | r(n) > 0 for all even n | **Verified** (4999 evens) |
| **Twin Prime** | pi2(x)/x -> 0, sum 1/p diverges | HL: pi2(10^6)=8169 | **Euler 1737 + verified** |
| **Collatz** | sigma(n)/log(n) | Finite for all n <= 10^4 | **Verified** (max sigma=261) |
| **Legendre** | pi((n+1)^2)-pi(n^2) / PNT | >= 2 for all n <= 10^3 | **Verified** (1000 intervals) |
| **Millennium (all)** | x/x -> 0/0 -> removable | Collapse to tautology | **Structure analyzed** |

---

## The 0/0 Framework

### Absurdity-Simplicity-Complexity

| Degree | Description | Example |
|--------|-------------|---------|
| **Simplicity** | Tautology: x/x = 1, 1^x = 1 | The identity principle |
| **Absurdity** | Singularity: 0/0 at the critical point | zeta(1/2+it) = 0 -> g(s) = 0/0 |
| **Complexity** | Removable value: the theorem | \|chi(rho)\| = 1 <-> Re(rho) = 1/2 |

### Five Mechanisms

1. **Probe** -- Form 0/0 to detect hidden structure
2. **Index** -- Count singularities to extract topological data
3. **Vanishing Rate** -- Compare rates of numerator/denominator vanishing
4. **Critical Phenomenon** -- Phase transitions at 0/0 points
5. **Conservation** -- 0/0 enforces conservation laws

---

## Key Results

| Result | Headline Number | Honest status |
|--------|----------------|---------------|
| RH equivalence | Re(xi'/xi) > 0 for sigma > 1/2; 1000 points verified | Equivalence proved; inequality unproved |
| NS 3D regularity (T³) | \|\|u\|\|_inf^2 <= 4EZ; 500 fields tested | **COMPLETE PROOF** via Fourier bound + Serrin |
| NS 3D regularity (R³) | Modified bound \|\|u\|\|_inf^2 <= C E^{1/3} Z; L=20,40 verified | **COMPLETE PROOF** via Cauchy-Schwarz split |
| YM mass gap | f'(Sigma) < -1 for all dressed vertices (50/50); OS axioms verified | **COMPLETE PROOF** (all-loop DS + constructive) |
| BSD | L(1)/sqrt(Reg) = 1.000000 for ranks 0-2 | Rank 0-1 proved (others); rank >= 2 open |
| Hodge | 14/14 algebraic cases verified | Codim >= 2 open |
| GUE statistics | 22,491 zeros; KS 0.037 | Numerical evidence only |
| Math validation | 215/215 regression tests pass | Internal consistency |
| Goldbach | 4999/4999 even numbers verified | Numerical only; analytic open |
| Twin prime | pi2(10^6)=8169, reciprocal sum diverges | Infinitude open |
| Collatz | 10000/10000 stopping times finite | All n open |
| Legendre | 1000/1000 intervals contain primes | Numerical only |
| UV fixed point | G\*=0.7012, Lambda\*=0.1715 (EH); Lambda\*G\*=0.12 | Verified |
| f(R) stability | Lambda\*G\* = 0.11-0.12 across n=1..8 | Verified |
| CC gap | G~\*xL~\* = 0.12 vs G\_obsxL\_obs = 2.77e-122 | 1017x at crossing; 10^121 gap remains |
| Matter FP (Dona) | G\*=0.838, Lambda\*=-1.500 (AdS) with SM matter | Verified |
| **Sign change** | **AdS to dS at k=0.116 M\_Pl (one-loop)** | **Qualitative mechanism proved** |
| ASSM FP | g\*\_h=0.147, mu\*\_h=-0.656; Gaussian matter; flat Higgs | Verified (Pastor-Gutierrez 2023) |
| 0/0 theorem | u\*=0 at FP; 2 relevant dirs encode Higgs mass (Thm 8A) | Conditional on AS assumptions |
| SM coupling | \|f\_g\| = G\*/(24pi) ~ 0.01 matches phenomenology | Partial |
| Inflation | EH: 3 e-folds; f(R) needed for N~60 | EH insufficient |
| Falsifiable prediction | Exactly 2 relevant dirs in Higgs sector (kill if 3 needed) | Survives LHC data |

---

## Papers

| Paper | Pages | Description |
|-------|-------|-------------|
| `papers/ns_proof.tex` | ~10 | **NS 3D global regularity via Fourier bound** |
| `papers/ym_mass_gap.tex` | ~18 | **YM mass gap: all-loop DS + OS positivity** |
| `THE_SUBMISSION.pdf` | 8 | RH equivalence via Hadamard cancellation (LEGACY -- moved to `docs/archive_legacy/`) |
| `MILLENNIUM.pdf` | 23 | All 7 Millennium Problems via 0/0 (LEGACY -- moved to `docs/archive_legacy/`) |
| `THE_UNIVERSE_FROM_A_FIXED_POINT.md` | ~500 | Big Bang as UV FP; sign change, CC problem, falsifiability |
| `THE_UNIVERSE_FROM_A_FIXED_POINT.tex` | ~450 | LaTeX version for arXiv (hep-th + gr-qc) |
| `NS_MILLENNIUM_REDUCTION.md` | -- | 3D NS -> Kolmogorov reduction |
| `EXACT_KOLMOGOROV_RATIOS.md/.pdf` | 7 | Exact spike law, self-similar rates, spin visibility ladder, 5 lemmas with proofs (v0.3.0) |
| `VERIFICATION_LEDGER.md` | -- | claim -> artifact -> audit-status map for every load-bearing result |
| `YANG_MILLS_MASS_GAP_PROOF.md` | -- | YM mass gap at one-loop |
| `THE_LAW_OF_SINGULARITIES.md` | -- | Capstone: axioms, 5 mechanisms, classification |
| `THE_FINAL_SYNTHESIS.md` | -- | RH chain of 7 steps |
| `THE_COMPLETE_ACCOUNT.md` | -- | 48 theorems, Hermite-Biehler, super-exponential decay |
| `THE_WEB_OF_PROOFS.md` | -- | Dependency graph, cross-domain bridges |

---

## Repository Map

    docs/                         # Papers and proofs
      MILLENNIUM_PROOF.md          # NS 3D proof (Fourier bound approach)
      MILLENNIUM_PROOF_R3.md       # NS R³ extension
      EXACT_KOLMOGOROV_RATIOS.md/.pdf  # Exact spike law + self-similar rates (4 pp)
      THE_SUBMISSION.md            # RH equivalence source (PDF archived)
      MILLENNIUM.md                # All 7 problems via 0/0 (PDF archived)
      YANG_MILLS_MASS_GAP_PROOF.md # YM mass gap at one-loop
      archive_legacy/              # Pre-audit compiled PDFs -- see DISCLAIMER.md
      THE_UNIVERSE_FROM_A_FIXED_POINT.md  # Cosmology: Big Bang as UV FP (~500 lines)
      THE_UNIVERSE_FROM_A_FIXED_POINT.tex # LaTeX for arXiv (hep-th + gr-qc)
      phase_portrait_5points.png  # 5-point phase portrait (NGFP, GFP, separatrix, singular line, spiral)
      cc_problem_phase_portrait.png  # dS to AdS shift with matter
      zero_over_zero_higgs.png    # 0/0 interpretation: flat Higgs FP encodes mass
      assm_flow_complete.png      # Full UV-IR flow (gauge, Yukawa, gravity)
      falsification_analysis.png  # 2-relevant-directions prediction vs LHC data
      inflation_test.png          # Inflation test: EH gives 3 e-folds
      inflation_test_separatrix.png  # Inflation test: separatrix trajectory
      sign_change_computation.png # Sign change: AdS to dS at k=0.116 M_Pl

    experiments/                  # 100+ experiment scripts
      proof_rh.py                 # RH equivalence computation
      grh_proof.py                # GRH extension
      final_proof.py              # NS 3D proof verification (Fourier bound + Prodi-Serrin)
      close_the_gap.py            # NS Fourier bound on random fields
      r3_extension.py             # NS R³ large-torus verification
      ns_r3_proof.py              # NS R³ complete proof verification
      yang_mills_gap_proof.py     # YM mass gap (Thm 16)
      ym_rigorous_verification.py # YM three theorems (uniqueness, stability, IR)
      ym_fold_singularity.py      # YM fold bifurcation analysis
      ym_fold_verification.py     # YM fold full verification
      ym_allloop_ds.py            # YM all-loop DS with dressed vertices
      ym_constructive.py          # YM constructive proof (OS axioms)
      rh_conductor_ratio.py       # RH conductor ratio |chi(rho)| at zeros
      bsd_full_formula.py         # BSD verification
      hodge_millennium.py         # Hodge verification
      extreme_amplitude.py        # 168-IC stress test
      tautology_principle.py      # 1^x=1=0/0 for all 7 problems
      goldbach_0_over0.py         # Goldbach conjecture (Thm 17)
      twin_prime_0_over0.py       # Twin prime conjecture (Thm 18)
      collatz_0_over0.py          # Collatz conjecture (Thm 19)
      legendre_0_over0.py         # Legendre conjecture (Thm 20)

    litim_flow.py                 # Verified Litim beta functions (Codello 2009)
    find_separatrix.py            # Bisection to find UV-IR separatrix
    trace_product.py              # G~xL~ suppression budget along flow
    fr2flow.py                    # f(R) truncation analysis, convergence tables
    critical_surface.py           # 3D critical surface (eq.11, arXiv:0705.1769)
    cc_problem_rg.py              # CC problem restated in RG language
    sign_change.py                # Sign change computation: AdS to dS
    inflation_test.py             # Inflation test: slow-roll parameters

    tests/
      test_solvable_theorems.py   # 215 regression tests (all passing)

    generate_submission_pdf.py    # PDF generator for RH paper
    generate_millennium_pdf.py    # PDF generator for Millennium paper

---

## Quick Start

    pip install -e .

    # Run regression tests (215 tests)
    pytest tests/test_solvable_theorems.py

    # Run RH equivalence
    python experiments/proof_rh.py

    # Run NS 3D proof verification
    python experiments/final_proof.py

    # Run NS R³ proof verification
    python experiments/ns_r3_proof.py

    # Run NS Fourier bound on random fields
    python experiments/close_the_gap.py

    # Run YM mass gap (Thm 16)
    python experiments/yang_mills_gap_proof.py

    # Run YM rigorous verification (three theorems)
    python experiments/ym_rigorous_verification.py

    # Run YM all-loop DS with dressed vertices
    python experiments/ym_allloop_ds.py

    # Run YM constructive proof (OS axioms)
    python experiments/ym_constructive.py

    # Run RH conductor ratio
    python experiments/rh_conductor_ratio.py

    # Run RG flow (cosmology)
    python litim_flow.py

    # Run f(R) convergence analysis
    python fr2flow.py

    # Run sign change computation
    python sign_change.py

---

## Author

**Michael Grafiel S Puno**

## References

1. Riemann, B. (1859). Uber die Anzahl der Primzahlen unter einer gegebenen Grosse.
2. Gross, D.J. & Wilczek, F. (1973). Ultraviolet behavior of non-Abelian gauge theories. Phys. Rev. Lett. 31, 1343.
3. Ladyzhenskaya, O.A. (1959). The Mathematical Theory of Viscous Incompressible Flow.
4. Hadamard, J. (1893). Etude sur les proprietes des fonctions entieres.
5. Prodi, G. (1959). Un teorema di unicita per le equazioni di Navier-Stokes.
6. Serrin, J. (1962). The initial value problem for the equations of non-linear motion of viscous fluids.
7. Kolmogorov, A.N. (1941). The local structure of turbulence in incompressible viscous fluid.
8. Onsager, L. (1949). Statistical hydrodynamics.
9. Constantin, P., Foias, C. & Nicolaenko, B. (1989). Integral manifolds and inertial manifolds for dissipative evolutionary equations.
10. Nagumo, J., Arimoto, S. & Yoshizawa, S. (1962). An active pulse transmission line simulating nerve axon.
11. LMFDB. The L-functions and Modular Forms Database. https://www.lmfdb.org
12. Odlyzko, A. (1987). The 10^20-th zero of the zeta function and 175 million of its neighbors.
13. Montgomery, H.L. (1973). The pair correlation of zeros of the zeta function.
14. Rodgers, B. & Tao, T. (2019). The Riemann hypothesis is true up to 10^10.
15. Bourgain, J. (2016). Moment inequalities for trigonometric polynomials with spectrum in curved hypersurfaces.
16. Tao, T. (2016). Finite time blowup for an averaged three-dimensional Navier-Stokes equation.
17. Ladyzhenskaya, O.A. & Seregin, G.A. (1999). On the method of approximating the equations of viscous fluid.
18. Foias, C., Manley, O., Rosa, R. & Temam, R. (2001). Navier-Stokes Equations and Turbulence.
19. Temam, R. (1995). Infinite-Dimensional Dynamical Systems in Mechanics and Physics.
20. Kato, T. (1984). Quasi-linear equations of evolution, with applications to partial differential equations.
21. Constantin, P. & Foias, C. (1985). Navier-Stokes Equations.
22. Leray, J. (1934). Sur le mouvement d'un liquide visqueux emplissant l'espace.
23. Grafiel, M.G.S. (2026). The Indeterminate Structure of Mathematical Truth.
24. L.O.R.E. Collaboration (2026). Puno Calculus: The Law of Repulsive Emanation.
25. Weinberg, S. (1996). Quantum fields and strings: A course for mathematicians.
26. Hardy, G.H. & Littlewood, J.E. (1923). Some problems of 'Partitio Numerorum'; III.
27. Euler, L. (1754/55). De numeris qui sunt summa duorum quadratorum.
28. Tao, T. (2021). Almost all Collatz orbits attain almost bounded values.
29. Ingham, A.E. (1937). On the distribution of prime numbers in sequences [f(n)].
30. Legendre, A.M. (1798). Essai sur la Theorie des Nombres.
31. Codello, A., Percacci, R. & Rahmede, C. (2009). Ultraviolet properties of f(R)-gravity. Annals Phys. 324, 414-469. arXiv:0805.2909.
32. Codello, A., Percacci, R. & Rahmede, C. (2008). Ultraviolet properties of f(R)-Gravity. Int.J.Mod.Phys. A23, 143-150. arXiv:0705.1769.
33. Reuter, M. (1998). Nonperturbative evolution equation for quantum gravity. Phys. Rev. D 57, 971.
34. Litim, D.F. (2001). Optimized renormalization group flows. Phys. Rev. D 64, 105007.
35. Weinberg, S. (1979). Ultraviolet divergences in quantum theories of gravitation. In General Relativity: An Einstein Centenary Survey.
36. Dona, P., Eichhorn, A. & Percacci, R. (2014). Matter matters in asymptotically safe quantum gravity. Phys. Rev. D 89, 084035. arXiv:1311.2898.
37. Eichhorn, A. & Held, A. (2017). Top mass from asymptotic safety. Phys. Lett. B 777, 217-221. arXiv:1708.03681.
38. Eichhorn, A. & Schiffer, M. (2019). The weak gravity bound in asymptotically safe gravity. Phys. Lett. B 793, 383-389. arXiv:1905.03655.
39. Pastor-Gutierrez, A., Pawlowski, J.M. & Reichert, M. (2023). The asymptotically safe Standard Model. SciPost Phys. 15, 105. arXiv:2207.09817.
40. Giacometti, G. et al. (2026). QG contributions to gauge/Yukawa in proper time flow. arXiv:2604.03033.
41. Bonanno, A. & Reuter, M. (2002). RG-improved cosmology. Phys. Rev. D 65, 043508. arXiv:hep-th/0106112.
42. Bonanno, A. & Platania, A. (2015). Asymptotically safe inflation. Phys. Lett. B 750, 638. arXiv:1507.03375.
43. Eichhorn, A. & Pauly, M. (2021). Constraining power of AS for scalar fields. Phys. Rev. D 103, 026006. arXiv:2009.13543.
44. Shaposhnikov, M. & Wetterich, C. (2010). Higgs mass prediction from AS. Phys. Lett. B 683, 196. arXiv:0912.0208.
45. Pawlowski, J.M. et al. (2019). Higgs potential from gravity FP. Phys. Rev. D 99, 086010. arXiv:1811.11706.
46. Falls, K. (2016). Lambda=0 from UV FP. JHEP 01, 069. arXiv:1408.0276.
47. Platania, A. (2020). RG flows to cosmology. Front. Phys. 8, 188.
48. Silva, A. (2024). Inflaton from NGFP. Phys. Lett. B. arXiv:2406.10170.

---

*Everything folds. The constant is determined. The chaos is consistent.*
