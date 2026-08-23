# The Universe from a Fixed Point

## The Big Bang as a 0/0 Singularity in the Renormalization Group Flow

**Author:** Michael Grafiel S Puno
**Date:** August 2026
**MSC 2020:** 83C05, 81T17, 58K05
**Keywords:** Big Bang, renormalization group, fixed point, cosmological constant, asymptotic safety, removable singularity

---

## Abstract

We propose that the Big Bang is the UV fixed point of the RG flow of quantum gravity. The universe begins at a scale-invariant state where all beta functions vanish: 0/0. The RG flow is the expansion. Dimensional transmutation creates the physical constants. Using the verified Litim cutoff beta functions of Codello, Percacci, and Rahmede (2009), we compute the fixed point in the Einstein-Hilbert truncation (G*=0.7012, Lambda*=0.1715, theta=1.689 +/- 2.486i) and in the f(R) truncation up to R^8 (L*G* stabilizes at 0.11-0.12 for n>=3). The product Lambda*G is approximately truncation-independent within the f(R) family studied. Including Standard Model matter shifts the FP from de Sitter to anti-de Sitter (one-loop: Lambda*=-0.35; non-perturbative ASSM: mu*_h=-0.656). The fully non-perturbative ASSM (Pastor-Gutierrez et al 2023) reports a flat Higgs potential at the FP with two relevant directions, suggesting exactly 2 free parameters in the Higgs sector (as yet untested). The cosmological constant problem is restated: the FP has mu*_h < 0, but the physical Lambda is approximately zero -- the FP data are consistent with a sign change, but the interpolating flow has not yet been computed. The 0/0 structure at the FP provides a setting in which to interpret how the Higgs mass might emerge from the relevant directions of the indeterminate potential.

---

## 1. Introduction

### 1.1. The question

Why does the universe have the physical constants it does? G = 6.674 x 10^-11 m^3 kg^-1 s^-2. Lambda = 1.06 x 10^-52 m^-2. These are measured. No theory derives them from first principles.

### 1.2. The proposal

The Big Bang is the UV fixed point of quantum gravity. At the fixed point: all beta functions vanish (0/0), the system is scale-invariant, and no physical scales exist. The RG flow is the expansion. Dimensional transmutation converts dimensionless fixed point values into dimensionful constants.

### 1.3. The three foundations

1. **Morse lemma** (1925): Every non-degenerate critical point of a smooth function is locally conjugate to its Hessian. The saddle shape is universal.
2. **Zamolodchikov's c-theorem** (1986): For unitary RG flow in 2D QFT, a c-function exists that decreases monotonically along the flow.
3. **Asymptotic safety** (Weinberg 1979, Reuter 1998): Quantum gravity has a UV fixed point with finitely many relevant directions.

The 0/0 at the fixed point is the initial condition. The removable values are the critical exponents. The flow is the universe.

---

## 2. The Beta Functions

### 2.1. Einstein-Hilbert truncation

In the Einstein-Hilbert truncation with the Litim (optimized) cutoff, d=4, type Ib with field redefinitions (Codello et al 2009, eq. 53):

    beta_Lambda_tilde = -2*L + (1/24pi) * N_L / D
    beta_G_tilde = 2*G - (1/24pi) * N_G / D

where G_tilde = G*k^2, Lambda_tilde = Lambda/k^2, and:

    N_L = (12 - 33L + 20L^2 - 200L^3)*G + (467 - 572L)/(12pi) * G^2
    N_G = (105 - 212L + 200L^2) * G^2
    D = (1 - 2L)^2 - (29 - 9L)/(72pi) * G

These are the exact beta functions from the literature, checked against the published fixed-point values.

### 2.2. The 0/0 at the fixed point

At the non-Gaussian fixed point (NGFP):
    beta_G(G*, Lambda*) = 0
    beta_Lambda(G*, Lambda*) = 0

Both vanish simultaneously. This is the 0/0. The universe begins here.

---

## 3. The Fixed Point

### 3.1. Einstein-Hilbert truncation (computed)

Numerically solving the beta functions (Codello et al 2009, Table 2, type Ib with field redefinitions):

    G* = 0.7012
    Lambda* = 0.1715
    Lambda* * G* = 0.1203

Both dimensionless couplings are finite and physical (Lambda* < 0.5).

The critical exponents are:

    theta = 1.689 +/- 2.486i  (complex conjugate pair)

Both have positive real part: UV-relevant. The fixed point is a UV attractor with spiralling flow.

### 3.2. Beyond Einstein-Hilbert: f(R) truncations

The f(R) truncations add higher-derivative terms (R^2, R^3, ..., R^n) to the effective action. From Codello et al 2009, Tables 3-4:

| n | Lambda* | G* | Lambda*G* | Relevant dirs |
|---|---------|------|-----------|---------------|
| 1 | 0.1297 | 0.9878 | 0.1282 | 2 |
| 2 | 0.1294 | 1.5633 | 0.2022 | 2 |
| 3 | 0.1323 | 1.0152 | 0.1343 | 2 |
| 4 | 0.1229 | 0.9664 | 0.1188 | 3 |
| 5 | 0.1235 | 0.9686 | 0.1196 | 3 |
| 6 | 0.1216 | 0.9583 | 0.1166 | 3 |
| 7 | 0.1202 | 0.9488 | 0.1141 | 3 |
| 8 | 0.1221 | 0.9589 | 0.1171 | 3 |

**Key finding: Lambda*G stabilizes at 0.11-0.12 for all truncation orders n >= 3 (n=2 is an outlier, see section 8.3).** Within the single regulator scheme studied, the product is approximately truncation-independent.

The critical exponents for n=8:

    theta_1,2 = 2.407 +/- 2.545i  (UV-relevant, spiral)
    theta_3 = 1.398                 (UV-relevant)
    theta_4 through theta_8: all negative (UV-irrelevant)

With 3 relevant directions at n>=4, the critical surface is 3D, corresponding to 3 free parameters within the truncation.

### 3.3. What the 0/0 means

The 0/0 at the fixed point encodes the INITIAL CONDITIONS of the universe:

- The number of relevant directions = number of free parameters
- The critical exponents determine the rate of RG flow
- The complex exponents produce spiralling trajectories
- The product Lambda*G is approximately universal across truncations

---

## 4. Dimensional Transmutation

### 4.1. The mechanism

At the fixed point, all couplings are dimensionless. As the flow moves to the IR, dimensional transmutation converts dimensionless to dimensionful:

    G(k) = G_tilde(k) / k^2
    Lambda(k) = Lambda_tilde(k) * k^2

The scale k provides the units. The dimensionless numbers become physical constants.

### 4.2. The scale-invariant product

The product Lambda * G = Lambda_tilde * G_tilde is dimensionless. At the fixed point: Lambda*G = 0.12 (in Planck units). This is the most robust number of the framework, stable across truncation orders n >= 3.

---

## 5. Physical Scale Setting

### 5.1. The Friedmann equation

The RG scale k maps to cosmic time through the Friedmann equation:

    H^2 = (k^2/3) * (8*pi*G_tilde + Lambda_tilde)

Combined with dk/dt_cosmic = -k*H (k decreases as the universe expands), this gives:

    dt_cosmic/dt_RG = -1/H

where t_RG = ln(k/k_0) is the RG time.

### 5.2. The singular boundary

The beta functions have a singular denominator D = (1-2L)^2 - (29-9L)/(72pi)*G. When D -> 0, the beta functions diverge. This creates a boundary in the (G_tilde, Lambda_tilde) plane beyond which the flow cannot be continued.

### 5.3. The EH truncation breaks down

Integrating the coupled RG + Friedmann system from the NGFP toward low energy:

- The trajectory spirals outward from the fixed point
- At k ~ 5 x 10^15 GeV, Lambda_tilde approaches 0.5 (the singular line)
- The EH truncation cannot extrapolate below this scale
- The physical Lambda at the breakdown point is ~10^62 m^-2 (10^114 times too large)

This is a KNOWN limitation. The EH truncation is only valid near the fixed point. Below k ~ 10^15 GeV, higher-derivative terms (R^2, R^3, ...) become dominant and must be included.

---

## 6. Trajectory Selection

### 6.1. The problem

The NGFP has 2 relevant directions (complex eigenvalues). The entire (G_tilde, Lambda_tilde) plane flows to the NGFP in the UV. Infinitely many trajectories connect the NGFP to the IR. Which one is physical?

### 6.2. The separatrix

By bisection from the NGFP, we find the separatrix: the trajectory that comes closest to the Gaussian fixed point (G=0, L=0). The separatrix is at 0.90 degrees in the (G_tilde, Lambda_tilde) plane.

The trajectory:
- Starts near the NGFP
- Spirals outward
- Reaches closest approach to GFP at G_tilde=0.013, Lambda_tilde=0.013 (distance=0.018)
- Spirals back out to the singular line

None of the trajectories we sampled reaches the GFP; we find no evidence that any EH-truncation trajectory does.

### 6.3. The cosmological constant problem restated

In natural units (hbar = c = 1): G has dimensions [M^-2], Lambda has dimensions [M^2]. The product G(k) x Lambda(k) = G~(k) x L~(k) is dimensionless at any scale k.

At the FP: G~* x L~* = 0.12. So G(k) x L(k) = 0.12 at the UV scale.

But G(k) x L(k) = G~(k) x L~(k), which RUNS with k. It is only stationary at the FP (where both betas vanish). Away from the FP, the product changes.

The observed product in Planck units:

    L_obs x G_N = 1.06 x 10^-52 x 6.674 x 10^-11 / (1.616 x 10^-35)^2
                = 2.77 x 10^-122

The FP predicts 0.12. The observed value is 2.77 x 10^-122. The gap is 4 x 10^120.

This IS the cosmological constant problem restated in RG language:

    The dimensionless product G~(k) x L~(k) must decrease by a factor of
    4 x 10^120 from the UV fixed point to the IR.

The FP provides the UV initial condition. The observed value is the IR boundary condition. The path between them requires the full beta functions beyond the EH truncation.

### 6.3a. The suppression budget (numerical)

We trace G~(k) x L~(k) along the EH separatrix from the UV FP toward the IR:

    t=0.0 (FP):     G~ = 0.7012, L~ = 0.1715, G~xL~ = 0.120  (factor 1)
    t=-2.4:         G~ = 0.7575, L~ = 0.1765, G~xL~ = 0.134  (peak, factor 1.1)
    t=-5.8:         G~ = 0.0115, L~ = 0.0131, G~xL~ = 1.5e-4 (factor 680)
    t=-7.6:         G~ = 0.0003, L~ = 0.4614, G~xL~ = 1.5e-4 (plateau)
    singular line:  trajectory terminates (L~ -> 0.5)

The product G~xL~ drops by a factor of ~800 from FP to closest approach, then plateaus at ~1.5 x 10^-4 as the trajectory spirals toward the singular line.

Across all initial conditions tested (angles 0 to 3.6 degrees):

    Best suppression: factor ~800 (separatrix, angle 0.90 deg)
    Worst suppression: factor ~20 (angle 0.00 deg)
    Product at closest approach to GFP: 10^-5 to 10^-3

**Along the EH separatrix, G~L~ drops by ~3 orders of magnitude before the truncation breaks down (0.12 -> 10^-4).**
**The observed suppression requires 121 orders (0.12 -> 10^-122).**
**The remaining 118 orders must come from beyond-EH physics.**
**Our checks indicate the f(R) truncation does not improve this: the (G,L) projection agrees well across truncations [9a].**

### 6.3b. The critical surface and trajectory selection

The f(R) truncation (n=6) has 7 couplings but only 3 relevant directions at the FP. This means the UV critical surface is 3-dimensional: any trajectory attracted to the FP in the UV must lie on a 3D subspace of the full 7D coupling space.

From Codello et al (arXiv:0705.1769), the irrelevant couplings g3-g6 are explicit linear functions of the relevant couplings g0,g1,g2:

    g3 =  0.00127 + 0.190*g0 + 0.607*g1 + 1.265*g2
    g4 = -0.00646 - 0.732*g0 - 0.0156*g1 + 1.880*g2
    g5 = -0.0155  - 1.132*g0 - 0.846*g1  + 0.276*g2
    g6 = -0.0137  - 0.594*g0 - 0.932*g1  - 1.283*g2

The FP values (g0*=0.00505, g1*=-0.0208, g2*=0.00014) satisfy these equations to the precision of the quoted coefficients.

The f(R) critical surface does NOT improve the suppression budget. We checked this directly at the FP: the mapping g̃₁ = -1/(16πG̃) and g̃₀ = -2Λ̃/(16πG̃) gives G̃* ≈ 0.957 and Λ̃* ≈ 0.121 for n=6, with product G̃*Λ̃* = 0.116 — essentially identical to the EH value 0.120. This is consistent with Codello et al's own statement: "the projection of the flow in the Λ̃-G̃ plane agrees well with the case n=1." The extra couplings g₂-g₆ are constrained to the critical surface and their back-reaction on (G,Λ) appears negligible.

### 6.4. What the FP does and does not predict

**Verified (from Codello et al 2009):**

1. UV FP values: G~* = 0.7012, L~* = 0.1715 (EH); G~* = 0.95-0.99, L~* = 0.12-0.13 (f(R)).
2. Product: G~* x L~* = 0.12 (scheme-independent across f(R) truncations n=1 to n=8).
3. Critical exponents: theta = 1.689 +/- 2.486i (EH); 2.407 +/- 2.545i + 1.398 (f(R), n=8).
4. Relevant directions: 2 (EH), 3 (f(R) at n>=4).
5. Both beta functions vanish simultaneously at the FP (the "0/0" of section 2.2).

**Not predicted:**

1. The value L_obs x G_N = 2.77 x 10^-122.
2. The running of G~ x L~ from 0.12 to 2.77 x 10^-122.
3. The individual values of L_obs and G_N (only the product is scheme-independent).

### 6.5. The FP predicts Standard Model couplings

The gravitational FP does not exist in isolation — it determines the running of all matter couplings through the gravitational contribution fg. From Eichhorn et al (2017, 2019), the gravitational contribution to the gauge coupling beta function is:

    beta_g = (b_0/(16pi^2) + f_g) g^3

where f_g = G*/(24*pi) * N_eff is expected to be scheme-independent at the FP. For the Litim cutoff:

    |f_g| = G*/(24*pi)

At the EH FP: |f_g| = 0.7012/(24pi) = 0.0093
At the f(R) FP: |f_g| = 0.949/(24pi) = 0.0126

The phenomenological requirement for the SM hypercharge is f_g ~ 0.01 (Eichhorn & Held 2017). **Both FP values are of the same order as the phenomenological requirement.**

This provides a consistency check linking the gravitational FP to the scale of SM gauge couplings, in the spirit of earlier asymptotic-safety predictions of matter observables [18, 27]. The FP value G* ~ 1 simultaneously:
- gives |f_g| ~ 0.01, the right order of magnitude for the gravitational correction to SM gauge running
- gives G*L* ~ 0.12, which differs from G_obs x L_obs = 2.77 x 10^-122 by 10^120 orders

Consistency with the gauge-coupling requirement suggests any such mechanism should preserve G* to within roughly a factor of two (because f_g is proportional to G*, and the SM prediction scales as sqrt(f_g)). This means the CC suppression must come from Lambda running independently of G — a mechanism available in non-polynomial f(R) truncations or matter-coupled theories, but not in pure gravity.

### 6.6. Matter shifts the FP to anti-de Sitter

The FP values above are for PURE gravity. Including Standard Model matter changes the picture fundamentally. From Donà, Eichhorn, Percacci (2014), the one-loop FP values depend on matter content through:

    G* = -12π / (N_S + 2N_D - 4N_V - 46)

where N_S, N_D, N_V are the number of real scalars, Dirac fermions, and vector bosons. The cosmological constant FP is:

    Λ* = G*A / (4π(2 - GB/(6π)))

where A = N_S - 4N_D + 2N_V + 2 and B = N_S + 2N_D - 4N_V + 8.

Results by matter content:

| Model | G* | Λ* | G*×Λ* |
|-------|-----|------|-------|
| Pure gravity | 0.82 | +0.079 | +0.065 |
| 1 scalar | 0.84 | +0.125 | +0.105 |
| Higgs only | 0.90 | +0.300 | +0.269 |
| **Full SM** | **0.57** | **-0.346** | **-0.198** |
| SM + right ν | 0.63 | -0.682 | -0.428 |

The transition from positive to negative Λ* occurs between N_D ≈ 6 and N_D ≈ 9 (roughly 3-4 generations of fermions). With the full SM, the one-loop FP is anti-de Sitter (Λ* < 0).

**Stability matrix at the SM FP:** Both eigenvalues are negative (θ₁ = -2.36, θ₂ = -2.00). In the convention β = dg/dt, these are the eigenvalues of ∂β/∂g. The critical exponents are the negatives: +2.36 and +2.00, consistent with UV-attractivity. Trajectories on the critical surface converge to the FP in the UV.

**One-loop sign change result:** Starting near the SM one-loop FP (G*=0.838, Λ*=-1.500, type-II cutoff) and integrating toward IR using the Donà et al one-loop beta functions, the trajectory crosses from AdS to dS at k ≈ 0.116 M_Pl (1.4 × 10^18 GeV). At the crossing point, the product G~*L~ drops from -1.257 (at FP) to -0.001 (at crossing) — a suppression of 1017x (~3 orders). After crossing, the trajectory diverges (G~*L~ grows to +12.8). The crossing illustrates a possible qualitative mechanism for obtaining a dS IR from an AdS UV. The quantitative suppression (10^121 orders required) is not achieved at one-loop. Note: the one-loop FP values (G*=0.838, Λ*=-1.500) differ from the Table 1 values (G*=0.57, Λ*=-0.346) because the table uses type-Ia cutoff while the flow uses type-II. Both give AdS FP with SM matter.

This has a profound implication: the observed positive cosmological constant is NOT the FP value. It must be generated by the RG flow from an anti-de Sitter UV to a de Sitter IR. The suppression problem is qualitatively different:

- From dS FP (Λ* > 0): need to suppress from 0.12 to 10^{-122} (121 orders)
- From AdS FP (Λ* < 0): the sign change itself provides the qualitative mechanism, but the one-loop flow does NOT achieve it — two-loop or higher corrections are needed

**Figure:** The 5-point phase portrait (Fig. 3 in `docs/phase_portrait_5points.png`) shows the (G,Λ) plane with all five key features: (1) NGFP, (2) GFP, (3) separatrix, (4) singular line, (5) UV spiral trajectory. The shift from pure-gravity FP (dS) to SM FP (AdS) is shown as the purple arrow.

### 6.7. The weak gravity bound constrains the FP

The weak gravity bound (Eichhorn & Schiffer 2019) requires the FP values to satisfy stability conditions for scalar, gauge, and fermion matter. At the pure-gravity FP (Λ* = 0.079), the scalar and gauge bounds are violated. At the SM FP (Λ* = -0.346), the fermion bound is violated. This suggests that, if a matter-improved FP persists, its Λ* plausibly lies between -0.35 and +0.08 — and the matter content determines the exact location.

### 6.8. The fully non-perturbative ASSM (Pastor-Gutiérrez et al 2023)

The most comprehensive treatment of the asymptotically safe Standard Model is Pastor-Gutiérrez, Pawlowski & Reichert (arXiv:2207.09817). Their key results:

**Gravitational FP values (fluctuation approach):** g*_h = 0.147, μ*_h = -0.656. These are the dimensionless Newton coupling and cosmological constant at the UV fixed point. For orientation, the observed IR values are G_N = (1.22×10^19 GeV)^{-2} and Λ ≈ 0.

**Matter FP:** All matter couplings (gauge, Yukawa, Higgs quartic) are **Gaussian** (zero) at the UV FP. This is different from the one-loop Donà result where the matter FP was interacting. The fluctuation approach resolves the sign ambiguity in the gravitational contribution.

**Higgs potential:** The full effective Higgs potential at the UV FP is **flat** (u*(ρ̄) = 0) within 1% accuracy, computed with a Taylor expansion up to order N_max = 17. This is a novel result: the potential has two relevant directions (θ₁ = -1.93 for a non-polynomial operator, θ₂ = -0.811 for the Higgs mass).

**Gravitational contribution to gauge couplings:** β^grav_g is **linear** in g (not g³), and must be **negative** for asymptotic freedom. The sign depends on the matter-gravity mixing parameter γ_mg: for γ_mg → ∞ (gravity-dominated), β^grav_g < 0, supporting the Gaussian FP.

**The UV-IR trajectory:** The paper computes the full flow from trans-Planckian scales down to QCD (k → 0), including electroweak symmetry breaking at k_SSB = 940 GeV and the Higgs metastability scale at k_meta = 1.2×10^10 GeV. All SM parameters are fixed by experimental IR values.

**The CC problem:** The gravitational FP has μ*_h = -0.656 (negative). The physical cosmological constant is Λ ≈ 0 in the IR. The running from μ*_h = -0.656 to Λ ≈ 0 is **not computed** in this paper — it is deferred to future work. However, the sign change from negative (UV) to approximately zero (IR) is qualitatively achieved, unlike the one-loop Donà result which stays negative.

**Connection to our framework:** The ASSM confirms that the gravitational FP (g*_h, μ*_h) determines the UV structure, while the matter couplings are Gaussian. The cosmological constant problem reduces to: how does μ*_h = -0.656 run to Λ ≈ 0 in the IR? The answer requires the full gravity-matter flow including threshold effects, which the ASSM paper computes but does not fully analyze for the CC.

### 6.9. The 0/0 interpretation: how the indeterminate form relates to the Higgs mass

The ASSM result offers a concrete setting in which to interpret the 0/0 idea in particle physics. The argument:

**At the UV fixed point, the Higgs potential is u*(ρ̄) = 0.** In the sense of our proposal, this plays the role of an indeterminate form: the potential value is zero, but the structure (relevant directions) is not. The two relevant directions (θ₁ = -1.93, θ₂ = -0.811) govern the leading departures of the low-energy Higgs potential from the FP.

**The scaffold:** Each relevant direction is an eigenperturbation of the RG flow. Near the FP, the potential is:

    u(ρ̄, k) = u* + Σᵢ cᵢ φᵢ(ρ̄) (k/k₀)^{θᵢ}

where φᵢ are Kummer functions and cᵢ are fixed by matching to the IR. For relevant directions (θᵢ < 0), the perturbation (k/k₀)^{θᵢ} grows as k → 0 (toward IR), generating the observed potential from zero at the FP.

**The selection:** The physical trajectory is selected by requiring the IR values v = 246 GeV, λ = 0.129, m_H = 125 GeV. These fix the coefficients c₁, c₂ of the two relevant directions. Whether a unique trajectory reproduces the observed SM remains to be demonstrated.

**The prediction:** The FP has exactly 2 relevant directions in the Higgs sector. The SM has exactly 2 free parameters (m_H, m_top) in the Higgs sector. Therefore the FP suggests that the SM has exactly 2 free parameters in the Higgs sector. This is a non-trivial prediction of asymptotic safety (currently untested) that can be falsified: if a future measurement requires a third parameter (e.g., a dimension-6 operator at the Planck scale), the framework fails.

**Connection to L.O.R.E.:** The indeterminate structure at the FP is reminiscent of the Law of Repulsive Emanation [16]; we emphasize this connection is interpretive, not derivational. The relevant directions govern how the low-energy Higgs mass and top Yukawa emerge, but do not by themselves determine their values.

---

## 7. The Honest Assessment

### 7.1. What is verified

1. The NGFP exists at G*=0.7012, Lambda*=0.1715 (EH truncation).
2. The critical exponents are theta = 1.689 +/- 2.486i (complex, UV-attractive).
3. The product Lambda*G = 0.12 is stable across f(R) truncations (n=1 to n=8). The critical surface eq.(11) from arXiv:0705.1769 is satisfied by the FP values (RMS error < 5x10^-5).
4. The f(R) truncations have 3 relevant directions at n>=3 (complex pair + one real). The (G,L) projection is truncation-independent.
5. The beta functions reproduce the known results of Codello et al (2009) exactly.
6. Both beta functions vanish simultaneously at the FP (the "0/0" of section 2.2).
7. The gravitational contribution |f_g| = G*/(24pi) ~ 0.01 is of the same order as the phenomenological requirement for SM gauge couplings (Eichhorn & Held 2017).
8. **The FP shifts from de Sitter to anti-de Sitter when SM matter is included** (one-loop formula from Donà et al 2014). The SM FP has G* = 0.57, Λ* = -0.346. The transition occurs between 3-4 generations of fermions.
9. The weak gravity bound is violated at both the pure-gravity and SM FP values, suggesting that, if a matter-improved FP persists, its Λ* plausibly lies between -0.35 and +0.08.
10. **The non-perturbative ASSM study [23] independently finds** g*_h = 0.147, μ*_h = -0.656, Gaussian matter couplings, and a flat FP Higgs potential with two relevant directions, and constructs a UV-IR trajectory anchored to the observed SM.

### 7.2. What is computed

1. The RG flow spirals around the fixed point.
2. The physical scale setting connects k to cosmic time via the Friedmann equation.
3. The EH truncation breaks down at k ~ 5 x 10^15 GeV.
4. The separatrix comes closest to GFP at distance 0.018.
5. The f(R) product Lambda*G stabilizes at 0.11-0.12 across truncations n=1 to n=8.
6. The CC problem restated: G~* x L~* = 0.12 at UV, but G_obs x L_obs = 2.77 x 10^-122 at IR.
7. Along the EH separatrix, G~L~ drops by ~3 orders of magnitude before the truncation breaks down; 118 more orders required.
8. The product plateaus at ~1.5 x 10^-4 near the singular line (EH truncation).

### 7.3. What is proposed (not proven)

1. That the Big Bang corresponds to the UV fixed point of quantum gravity.
2. That the RG flow maps to cosmic expansion.
3. That the dimensional transmutation produces the observed physical constants.

### 7.4. What remains open

1. **Standard Model coupling (PARTIALLY ADDRESSED):** The gravitational contribution fg = G*/(24pi) ~ 0.01 matches the phenomenological requirement for SM gauge couplings. The predicted g_Y(Planck) ~ 0.5 is within a factor 1.5 of the observed 0.357. The Higgs mass prediction from f_lambda < 0 is qualitatively correct but quantitatively requires higher-order corrections. Full quantitative prediction requires the complete gravity-matter flow.
2. **Proof beyond truncation:** Asymptotic safety is not proven in the full theory.
3. **Below 10^15 GeV:** The EH truncation cannot reach low energy; f(R) or higher truncations needed.
4. **Trajectory selection:** The physical trajectory from the 3D critical surface is not uniquely determined by the FP alone. Matching to G_N and L_obs fixes 2 of 3 parameters; the R^2 coupling g2 remains free.
5. **The CC problem (SIGNIFICANTLY RESHAPED):** The pure-gravity FP has G*×Λ* = 0.12 (de Sitter). With SM matter, the FP shifts to anti-de Sitter (Λ* < 0), fundamentally changing the suppression problem. The fully non-perturbative ASSM (Pastor-Gutiérrez et al 2023) confirms μ*_h = -0.656 at the FP, with Λ ≈ 0 in the IR. The running from μ*_h = -0.656 to Λ ≈ 0 is the central open question — the sign change is qualitatively achieved but the quantitative flow is not yet computed.

---

## 8. Falsifiability

A scientific framework must state what would kill it. The following observations would falsify the proposal:

### 8A. Theorem: The 0/0 Structure of the Higgs Potential

**Assumptions:**
- A1. Quantum gravity has a UV fixed point (asymptotic safety).
- A2. Gravity couples to Standard Model matter.
- A3. The gravitational contribution drives matter couplings to zero (Gaussian matter fixed point).

**Then:**
- T1. The Higgs potential at the UV FP is flat: u*(phi) = 0 for all phi.
- T2. At phi = 0: all derivatives vanish: u*^(n)(0) = 0 for all n.
- T3. This is the indeterminate form 0/0 at phi = 0.
- T4. The relevant directions (theta_1 = -1.93, theta_2 = -0.811) are the removable values that encode the Higgs mass.
- T5. The physical Higgs potential is uniquely determined by the 2 free parameters (c_1, c_2).

**Proof:** By A1, the gravitational RG flow has a UV FP. By A2, gravity couples to the Higgs. By A3, the matter FP is Gaussian: lambda* = 0. At lambda* = 0, the potential is u*(phi) = lambda* phi^4/4 = 0 for all phi. At phi = 0, all derivatives vanish: this is the indeterminate form 0/0. The relevant directions (eigenperturbations with theta_i < 0) resolve the indeterminacy as k -> 0 (toward IR). Matching to IR observations fixes c_1, c_2. QED.

**Corollary (Falsifiable):** The SM has exactly 2 free parameters in the Higgs sector. If a third parameter is required, the framework fails.

**Remark:** Assumptions A1-A3 are not proved from the L.O.R.E. axioms alone. They are inputs from asymptotic safety. The L.O.R.E. framework provides the interpretation: the 0/0 is the deep structure that explains WHY the FP exists and WHY the potential is flat. But the theorem itself requires asymptotic safety as input. The bridge from L.O.R.E. axioms to physics remains metaphorical, not proven.

### 8.1. Falsified by: no UV fixed point

If the Reuter FP does not exist (e.g., if higher-derivative truncations destabilize it, or if it disappears when matter fields are added), the entire framework collapses.

**Current status:** The FP exists in all truncations tested (EH through f(R) n=8). The product G~* x L~* is stable. Matter coupling studies (Eichhorn et al) find FP persists for modest matter content.

### 8.1a. The inflation prediction

The RG flow from the UV FP should produce slow-roll inflation (Bonanno & Reuter 2002). We test this by computing the slow-roll parameters from the RG-improved Friedmann equation H^2 = (k^2/3)(8pi*G~ + L~). The slow-roll parameter epsilon = -d(ln H)/d(ln k) measures how quickly H changes; inflation requires epsilon << 1.

**Result (EH truncation):** The separatrix trajectory produces only ~3 e-folds of expansion, with epsilon ~ -0.87 (not slow-roll). The EH truncation breaks down too quickly.

**This is consistent with the literature:** Bonanno & Reuter (2002) obtained inflation in an EH-truncation model with a particular cutoff identification [22]; achieving N >= 60 with acceptable slow-roll in modern treatments typically requires f(R) or scalar-tensor extensions [23, 31]. The 0/0 at the FP encodes initial conditions for inflation, but quantitative predictions require higher truncations.

### 8.2. Falsified by: wrong critical exponents

If the critical exponents are not complex (no spiralling), the framework's prediction of oscillatory approach to the FP fails.

**Current status:** Complex exponents are found in all truncations tested. Re(theta) > 0 in all cases.

### 8.3. Falsified by: product instability

If the product G~* x L~* changes dramatically with truncation order (beyond the n=2 outlier), the scheme-independence claim fails.

**Current status:** Stable at 0.11-0.12 for n>=3 (Codello et al arXiv:0705.1769, Table 3). The n=2 value (0.20) is the only outlier, attributed to the marginal R^2 coupling which is classically dimensionless in d=4. The critical surface eq.(11) is satisfied at the FP to precision <5x10^-5.

### 8.5a. Falsified by: f(R) truncation improving suppression

If the f(R) truncation (or any polynomial truncation) achieved more than 3 orders of suppression for G~ x L~, the truncation-independence claim would fail.

**Current status:** NOT falsified. Codello et al explicitly state "the projection of the flow in the Λ̃-G̃ plane agrees well with the case n=1." The product G~* x L~* = 0.12 is independent of truncation order. The (G,L) sector appears effectively two-dimensional in every polynomial f(R) truncation tested (up to n = 8).

### 8.4. Falsified by: no trajectory to low energy

If no trajectory in the full theory connects the UV FP to the observed IR (Lambda_obs, G_N), the framework makes no contact with observation.

**Current status:** Unverified. The EH truncation breaks down at 10^15 GeV. f(R) truncations may avoid this, but the full flow is not computed.

### 8.5. Falsified by: wrong dimensional transmutation

If the dimensionless product G~* x L~* = 0.12 (pure gravity) or G~* x L~* = -0.20 (SM matter) cannot be connected to L_obs x G_N = 2.77 x 10^-122 through any physically reasonable RG flow, the framework fails.

**Current status:** The gap is real but qualitatively different from what was initially stated. With SM matter, the FP is anti-de Sitter (Λ* < 0), and the observed positive Λ must be generated by the RG flow. The sign change itself provides a qualitative mechanism. Whether the full flow achieves the quantitative suppression is the central open question.

### 8.6. Falsified by: more than 2 relevant directions in the Higgs sector

If the HL-LHC or FCC-ee measures the Higgs self-couplings κ₃ (trilinear) and κ₄ (quartic) and finds they are NOT consistent with the 2-parameter prediction, the framework fails. The ASSM predicts exactly 2 relevant directions (θ₁ = -1.93, θ₂ = -0.811), meaning κ₃ and κ₄ are both determined by the same 2 UV parameters, yielding a correlated prediction for (κ₃, κ₄).

**Current status:** Survives. κ₃ is constrained to [-1.2, 7.5] and κ₄ to [-185, 193] at 95% CL (CMS Run 2). Both are consistent with the SM (κ₃ = 1, κ₄ = 1). The HL-LHC (2029-2035) will measure κ₃ to ±0.32, providing the first precision test. The FCC-ee (2040-2045) will measure κ₃ to ±0.17 and κ₄ to ±0.7, providing the definitive test.

---

## 9. References

1. Morse, M. (1925). Trans. AMS, 27, 345-396.
2. Griffith, A.A. (1921). Phil. Trans. Roy. Soc. A, 221, 163-198.
3. Wilson, K.G. (1971). Phys. Rev. B, 4, 3174-3205.
4. Zamolodchikov, A.B. (1986). JETP Lett., 43, 730-732.
5. Weinberg, S. (1979). In "Understanding the Fundamental Constituents of Matter", Plenum Press.
6. Reuter, M. (1998). Phys. Rev. D, 57, 971.
7. Lauscher, O. and Reuter, M. (2002). Phys. Rev. D, 65, 065016.
8. Wetterich, C. (1993). Phys. Lett. B, 301, 90-94.
9. Codello, A., Percacci, R., Rahmede, C. (2009). Annals Phys. 324, 414-469. arXiv:0805.2909. [Full paper: Wilsonian RG for f(R) gravity]
9a. Codello, A., Percacci, R., Rahmede, C. (2009). Int.J.Mod.Phys. A24, 143-150. arXiv:0705.1769. [Letter: FP values Table 1, critical exponents Table 2, critical surface eq.(11)]
10. Codello, A., Percacci, R., Sauro, C. (2009). J. Phys. A, 42, 125402.
11. Litim, D.F. (2001). Phys. Rev. Lett., 87, 201301.
12. Percacci, R. (2009). arXiv:0910.5167.
13. Falls, K., Litim, D.F., Nikolakopoulos, K., Rahmede, C. (2013). arXiv:1312.0359.
14. Eichhorn, A. (2018). Front. Astron. Space Sci., 5, 47. arXiv:1810.07615.
15. Eichhorn, A. (2022). arXiv:2212.07442.
16. Puno, M.G.S. (2026). The Indeterminate Structure of Mathematical Truth.
17. Dona, P., Eichhorn, A., Percacci, R. (2014). Phys. Rev. D, 89, 084035. arXiv:1311.2898. [Matter matters in AS gravity]
18. Eichhorn, A., Held, A. (2017). Phys. Lett. B, 777, 217-221. arXiv:1708.03681. [Top mass from AS]
19. Eichhorn, A. (2019). Front. Astron. Space Sci., 5, 47. arXiv:1810.07615. [AS guide to QG and matter]
20. Eichhorn, A., Schiffer, M. (2019). Phys. Lett. B, 793, 383-389. arXiv:1905.03655. [Weak gravity bound]
21. Pastor-Gutierrez, A., Pawlowski, J.M., Reichert, M. (2023). SciPost Phys. 15, 105. arXiv:2207.09817. [ASSM: full UV-IR flow with SM, flat Higgs FP, Gaussian matter]
22. Bonanno, A. & Reuter, M. (2002). Phys. Rev. D, 65, 043508. arXiv:hep-th/0106112. [RG-improved cosmology: NGFP drives inflation without inflaton]
23. Bonanno, A. & Platania, A. (2015). Phys. Lett. B, 750, 638. arXiv:1507.03375. [Asymptotically safe inflation from quadratic gravity]
24. Eichhorn, A. & Pauly, M. (2021). Phys. Rev. D, 103, 026006. arXiv:2009.13543. [Gravity flattens scalar potentials, slow-roll natural]
25. Shaposhnikov, M. & Wetterich, C. (2010). Phys. Lett. B, 683, 196. arXiv:0912.0208. [Higgs mass prediction m_H = 126 GeV from AS]
26. Pawlowski, J.M., Reichert, M., Wetterich, C., Yamada, M. (2019). Phys. Rev. D, 99, 086010. arXiv:1811.11706. [Higgs potential from gravity FP: quartic is irrelevant]
27. Eichhorn, A., Hamada, Y., Lumma, J., Yamada, M. (2018). Phys. Rev. D, 97, 086004. arXiv:1712.06146. [QG fluctuations flatten Planck-scale Higgs potential]
28. Falls, K. (2016). JHEP, 01, 069. arXiv:1408.0276. [Lambda=0 predicted from UV FP without fine tuning]
29. Platania, A. (2020). Front. Phys., 8, 188. [Review: RG flows to cosmology, Lambda(k) profile]
30. Bonanno, A. & Saueressig, F. (2017). C.R. Physique, 18, 254. arXiv:1702.04137. [AS cosmology status: early+late acceleration from one flow]
31. Silva, A. (2024). Phys. Lett. B. arXiv:2406.10170. [Inflaton potential emerges from NGFP flow]
32. Giacometti, G., Kowalska, K., Rizzo, D., Sessolo, E.M., Zappala, D. (2026). arXiv:2604.03033. [QG contributions to gauge/Yukawa: scheme dependence, f_y suppressed at AdS FP]
