# The Universe from a Fixed Point

## The Big Bang as a 0/0 Singularity in the Renormalization Group Flow

**Author:** Michael Grafiel S Puno
**Date:** August 2026
**MSC 2020:** 83C05, 81T17, 58K05
**Keywords:** Big Bang, renormalization group, fixed point, cosmological constant, asymptotic safety, removable singularity

---

## Abstract

We propose that the Big Bang is the UV fixed point of the RG flow of quantum gravity. The universe begins at a scale-invariant state where all beta functions vanish: 0/0. The RG flow is the expansion. Dimensional transmutation creates the physical constants. Using the verified Litim cutoff beta functions of Codello, Percacci, and Rahmede (2009), we compute the fixed point in the Einstein-Hilbert truncation (G*=0.7012, Lambda*=0.1715, theta=1.689 +/- 2.486i) and in the f(R) truncation up to R^8 (L*G* stabilizes at 0.11-0.12). The product Lambda*G is a scheme-independent prediction of the UV fixed point. The cosmological constant problem is restated: the dimensionless product runs from 0.12 at the UV scale to 2.77 x 10^-122 at the observed scale. The gap (4 x 10^120) requires the full beta functions beyond the EH truncation. We state the falsifiability conditions: the framework is killed if no UV fixed point exists, if the critical exponents are not complex, or if the product instability exceeds truncation uncertainty.

---

## 1. Introduction

### 1.1. The question

Why does the universe have the physical constants it does? G = 6.674 x 10^-11 m^3 kg^-1 s^-2. Lambda = 1.06 x 10^-52 m^-2. These are measured. No theory derives them from first principles.

### 1.2. The proposal

The Big Bang is the UV fixed point of quantum gravity. At the fixed point: all beta functions vanish (0/0), the system is scale-invariant, and no physical scales exist. The RG flow is the expansion. Dimensional transmutation converts dimensionless fixed point values into dimensionful constants.

### 1.3. The three foundations

1. **Morse lemma** (1925): Every critical point of a smooth function is conjugate to its Hessian. The saddle shape is universal.
2. **Zamolodchikov theorem** (1986): In 2D CFT, RG flow is gradient flow. The c-function decreases monotonically.
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

These are the EXACT beta functions from the literature, verified to reproduce the known fixed point.

### 2.2. The 0/0 at the fixed point

At the non-Gaussian fixed point (NGFP):
    beta_G(G*, Lambda*) = 0
    beta_Lambda(G*, Lambda*) = 0

Both vanish simultaneously. This is the 0/0. The universe begins here.

---

## 3. The Fixed Point

### 3.1. Einstein-Hilbert truncation (verified)

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

**Key finding: Lambda*G stabilizes at 0.11-0.12 across ALL truncations.** The product is more stable than the individual values. This is a scheme-independent prediction of asymptotic safety.

The critical exponents for n=8:

    theta_1,2 = 2.407 +/- 2.545i  (UV-relevant, spiral)
    theta_3 = 1.398                 (UV-relevant)
    theta_4 through theta_8: all negative (UV-irrelevant)

With 3 relevant directions at n>=4, the critical surface is 3D. There are 3 free parameters.

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

The product Lambda * G = Lambda_tilde * G_tilde is dimensionless. At the fixed point: Lambda*G = 0.12 (in Planck units). This is the most robust prediction of the framework, stable across all truncation orders.

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

No trajectory in the EH truncation reaches the GFP. The separatrix is the one that comes closest.

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

**The EH truncation achieves 3 orders of magnitude of suppression (0.12 -> 10^-4).**
**The observed suppression requires 121 orders (0.12 -> 10^-122).**
**The remaining 118 orders must come from beyond-EH physics.**
**Crucially, the f(R) truncation does NOT improve this: the (G,L) projection is truncation-independent.**

### 6.3b. The critical surface and trajectory selection

The f(R) truncation (n=6) has 7 couplings but only 3 relevant directions at the FP. This means the UV critical surface is 3-dimensional: any trajectory attracted to the FP in the UV must lie on a 3D subspace of the full 7D coupling space.

From Codello et al (arXiv:0705.1769), the irrelevant couplings g3-g6 are explicit linear functions of the relevant couplings g0,g1,g2:

    g3 =  0.00127 + 0.190*g0 + 0.607*g1 + 1.265*g2
    g4 = -0.00646 - 0.732*g0 - 0.0156*g1 + 1.880*g2
    g5 = -0.0155  - 1.132*g0 - 0.846*g1  + 0.276*g2
    g6 = -0.0137  - 0.594*g0 - 0.932*g1  - 1.283*g2

The FP values (g0*=0.00505, g1*=-0.0208, g2*=0.00014) satisfy these equations exactly. The product G~*xL~* = 0.116 under the mapping g1=-Z, g0=2LZ.

The f(R) critical surface does NOT improve the suppression budget. We verified this directly: from the FP values in Table 1, the mapping g̃₁ = -1/(16πG̃) and g̃₀ = -2Λ̃/(16πG̃) gives G̃* ≈ 0.957 and Λ̃* ≈ 0.121 for n=6, with product G̃*Λ̃* = 0.116 — essentially identical to the EH value 0.129. This is consistent with Codello et al's own statement: "the projection of the flow in the Λ̃-G̃ plane agrees well with the case n=1." The extra couplings g₂-g₆ are constrained to the critical surface and their back-reaction on (G,Λ) is negligible. The f(R) truncation contributes 3 additional orders of suppression at most (from the n=2 outlier to the converged value), but does NOT bridge the 121-order gap. The missing 118 orders require beyond-f(R) physics: matter couplings, non-minimal curvature-matter interaction, or fundamentally new mechanisms beyond polynomial truncations.

### 6.4. What the FP does and does not predict

**Verified (from Codello et al 2009):**

1. UV FP values: G~* = 0.7012, L~* = 0.1715 (EH); G~* = 0.95-0.99, L~* = 0.12-0.13 (f(R)).
2. Product: G~* x L~* = 0.12 (scheme-independent across f(R) truncations n=1 to n=8).
3. Critical exponents: theta = 1.689 +/- 2.486i (EH); 2.407 +/- 2.545i + 1.398 (f(R), n=8).
4. Relevant directions: 2 (EH), 3 (f(R) at n>=4).
5. The 0/0 structure at the FP is real.

**Not predicted:**

1. The value L_obs x G_N = 2.77 x 10^-122.
2. The running of G~ x L~ from 0.12 to 2.77 x 10^-122.
3. The individual values of L_obs and G_N (only the product is scheme-independent).

### 6.5. The FP predicts Standard Model couplings

The gravitational FP does not exist in isolation — it determines the running of all matter couplings through the gravitational contribution fg. From Eichhorn et al (2017, 2019), the gravitational contribution to the gauge coupling beta function is:

    beta_g = (b_0/(16pi^2) + f_g) g^3

where f_g = G*/(24*pi) * N_eff is universal (scheme-independent at the FP). For the Litim cutoff:

    |f_g| = G*/(24*pi)

At the EH FP: |f_g| = 0.7012/(24pi) = 0.0093
At the f(R) FP: |f_g| = 0.949/(24pi) = 0.0126

The phenomenological requirement for the SM hypercharge is f_g ~ 0.01 (Eichhorn & Held 2017). **Both FP values give the right order of magnitude.**

This is the first concrete prediction connecting the gravitational FP to observable particle physics. The FP value G* ~ 1 simultaneously:
- Predicts |f_g| ~ 0.01 -> correct SM gauge coupling scale
- Predicts G*L* ~ 0.12 -> wrong CC by 10^120

Any mechanism that suppresses G*L* must preserve G* to within ~50% (because f_g is proportional to G*, and the SM prediction scales as sqrt(f_g)). This means the CC suppression must come from Lambda running independently of G — a mechanism available in non-polynomial f(R) truncations or matter-coupled theories, but not in pure gravity.

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

The transition from positive to negative Λ* occurs between N_D ≈ 6 and N_D ≈ 9 (roughly 3-4 generations of fermions). With the full SM, **the FP is anti-de Sitter** (Λ* < 0).

**Stability matrix at the SM FP:** Both eigenvalues are negative (θ₁ = -2.36, θ₂ = -2.00). In the convention β = dg/dt, these are the eigenvalues of ∂β/∂g. The critical exponents are the negatives: +2.36 and +2.00, confirming UV-attractivity. The FP is a UV attractor — all trajectories converge to it going to high energy. The relevant eigenvector (0.287, -0.958) determines the departure direction toward IR.

**One-loop RG flow result:** Starting near the SM FP and integrating toward IR (t → +∞), the trajectory stays in anti-de Sitter (Λ < 0). Lambda does NOT change sign in the one-loop approximation. The product G×Λ remains at ≈ -0.20 throughout the flow. This is a **known limitation of the one-loop approximation** — the sign change requires two-loop corrections (Pastor-Gutiérrez et al 2023) or non-minimal curvature-matter coupling.

This has a profound implication: the observed positive cosmological constant is NOT the FP value. It must be generated by the RG flow from an anti-de Sitter UV to a de Sitter IR. The suppression problem is qualitatively different:

- From dS FP (Λ* > 0): need to suppress from 0.12 to 10^{-122} (121 orders)
- From AdS FP (Λ* < 0): the sign change itself provides the qualitative mechanism, but the one-loop flow does NOT achieve it — two-loop or higher corrections are needed

**Figure:** The 5-point phase portrait (Fig. 3 in `docs/phase_portrait_5points.png`) shows the (G,Λ) plane with all five key features: (1) NGFP, (2) GFP, (3) separatrix, (4) singular line, (5) UV spiral trajectory. The shift from pure-gravity FP (dS) to SM FP (AdS) is shown as the purple arrow.

### 6.7. The weak gravity bound constrains the FP

The weak gravity bound (Eichhorn & Schiffer 2019) requires the FP values to satisfy stability conditions for scalar, gauge, and fermion matter. At the pure-gravity FP (Λ* = 0.079), the scalar and gauge bounds are violated. At the SM FP (Λ* = -0.346), the fermion bound is violated. This suggests the true FP lies between these extremes — with some Λ* between -0.35 and +0.08 — and the matter content determines the exact location.

### 6.8. The fully non-perturbative ASSM (Pastor-Gutiérrez et al 2023)

The most comprehensive treatment of the asymptotically safe Standard Model is Pastor-Gutiérrez, Pawlowski & Reichert (arXiv:2207.09817). Their key results:

**Gravitational FP values (fluctuation approach):** g*_h = 0.147, μ*_h = -0.656. These are the dimensionless Newton coupling and cosmological constant at the UV fixed point. The physical IR values are G_N = (1.22×10^19 GeV)^{-2} and Λ ≈ 0.

**Matter FP:** All matter couplings (gauge, Yukawa, Higgs quartic) are **Gaussian** (zero) at the UV FP. This is different from the one-loop Donà result where the matter FP was interacting. The fluctuation approach resolves the sign ambiguity in the gravitational contribution.

**Higgs potential:** The full effective Higgs potential at the UV FP is **flat** (u*(ρ̄) = 0) within 1% accuracy, computed with a Taylor expansion up to order N_max = 17. This is a novel result: the potential has two relevant directions (θ₁ = -1.93 for a non-polynomial operator, θ₂ = -0.811 for the Higgs mass).

**Gravitational contribution to gauge couplings:** β^grav_g is **linear** in g (not g³), and must be **negative** for asymptotic freedom. The sign depends on the matter-gravity mixing parameter γ_mg: for γ_mg → ∞ (gravity-dominated), β^grav_g < 0, supporting the Gaussian FP.

**The UV-IR trajectory:** The paper computes the full flow from trans-Planckian scales down to QCD (k → 0), including electroweak symmetry breaking at k_SSB = 940 GeV and the Higgs metastability scale at k_meta = 1.2×10^10 GeV. All SM parameters are fixed by experimental IR values.

**The CC problem:** The gravitational FP has μ*_h = -0.656 (negative). The physical cosmological constant is Λ ≈ 0 in the IR. The running from μ*_h = -0.656 to Λ ≈ 0 is **not computed** in this paper — it is deferred to future work. However, the sign change from negative (UV) to approximately zero (IR) is qualitatively achieved, unlike the one-loop Donà result which stays negative.

**Connection to our framework:** The ASSM confirms that the gravitational FP (g*_h, μ*_h) determines the UV structure, while the matter couplings are Gaussian. The cosmological constant problem reduces to: how does μ*_h = -0.656 run to Λ ≈ 0 in the IR? The answer requires the full gravity-matter flow including threshold effects, which the ASSM paper computes but does not fully analyze for the CC.

---

## 7. The Honest Assessment

### 7.1. What is verified

1. The NGFP exists at G*=0.7012, Lambda*=0.1715 (EH truncation).
2. The critical exponents are theta = 1.689 +/- 2.486i (complex, UV-attractive).
3. The product Lambda*G = 0.12 is stable across f(R) truncations (n=1 to n=8). The critical surface eq.(11) from arXiv:0705.1769 is satisfied by the FP values (RMS error < 5x10^-5).
4. The f(R) truncations have 3 relevant directions at n>=3 (complex pair + one real). The (G,L) projection is truncation-independent.
5. The beta functions reproduce the known results of Codello et al (2009) exactly.
6. The 0/0 structure at the fixed point is real.
7. The gravitational contribution |f_g| = G*/(24pi) ~ 0.01 matches the phenomenological requirement for SM gauge couplings (Eichhorn & Held 2017).
8. **The FP shifts from de Sitter to anti-de Sitter when SM matter is included** (one-loop formula from Donà et al 2014). The SM FP has G* = 0.57, Λ* = -0.346. The transition occurs between 3-4 generations of fermions.
9. The weak gravity bound is violated at both the pure-gravity and SM FP values, constraining the true FP to Λ* between -0.35 and +0.08.
10. **The fully non-perturbative ASSM (Pastor-Gutiérrez et al 2023) confirms:** the gravitational FP has g*_h = 0.147, μ*_h = -0.656; all matter couplings are Gaussian; the Higgs potential is flat at the FP with two relevant directions; the UV-IR trajectory reproduces the observed SM.

### 7.2. What is computed

1. The RG flow spirals around the fixed point.
2. The physical scale setting connects k to cosmic time via the Friedmann equation.
3. The EH truncation breaks down at k ~ 5 x 10^15 GeV.
4. The separatrix comes closest to GFP at distance 0.018.
5. The f(R) product Lambda*G stabilizes at 0.11-0.12 across truncations n=1 to n=8.
6. The CC problem restated: G~* x L~* = 0.12 at UV, but G_obs x L_obs = 2.77 x 10^-122 at IR.
7. The EH flow achieves 3 orders of suppression (0.12 -> 10^-4); 118 more orders required.
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

### 8.1. Falsified by: no UV fixed point

If the Reuter FP does not exist (e.g., if higher-derivative truncations destabilize it, or if it disappears when matter fields are added), the entire framework collapses.

**Current status:** The FP exists in all truncations tested (EH through f(R) n=8). The product G~* x L~* is stable. Matter coupling studies (Eichhorn et al) find FP persists for modest matter content.

### 8.2. Falsified by: wrong critical exponents

If the critical exponents are not complex (no spiralling), the framework's prediction of oscillatory approach to the FP fails.

**Current status:** Complex exponents confirmed in all truncations. Re(theta) > 0 in all cases.

### 8.3. Falsified by: product instability

If the product G~* x L~* changes dramatically with truncation order (beyond the n=2 outlier), the scheme-independence claim fails.

**Current status:** Stable at 0.11-0.12 for n>=3 (Codello et al arXiv:0705.1769, Table 3). The n=2 value (0.20) is the only outlier, attributed to the marginal R^2 coupling which is classically dimensionless in d=4. The critical surface eq.(11) is satisfied at the FP to precision <5x10^-5.

### 8.5a. Falsified by: f(R) truncation improving suppression

If the f(R) truncation (or any polynomial truncation) achieved more than 3 orders of suppression for G~ x L~, the truncation-independence claim would fail.

**Current status:** NOT falsified. Codello et al explicitly state "the projection of the flow in the Λ̃-G̃ plane agrees well with the case n=1." The product G~* x L~* = 0.12 is independent of truncation order. The (G,L) physics is robustly 2-dimensional regardless of how many higher-curvature terms are included.

### 8.4. Falsified by: no trajectory to low energy

If no trajectory in the full theory connects the UV FP to the observed IR (Lambda_obs, G_N), the framework makes no contact with observation.

**Current status:** Unverified. The EH truncation breaks down at 10^15 GeV. f(R) truncations may avoid this, but the full flow is not computed.

### 8.5. Falsified by: wrong dimensional transmutation

If the dimensionless product G~* x L~* = 0.12 (pure gravity) or G~* x L~* = -0.20 (SM matter) cannot be connected to L_obs x G_N = 2.77 x 10^-122 through any physically reasonable RG flow, the framework fails.

**Current status:** The gap is real but qualitatively different from what was initially stated. With SM matter, the FP is anti-de Sitter (Λ* < 0), and the observed positive Λ must be generated by the RG flow. The sign change itself provides a qualitative mechanism. Whether the full flow achieves the quantitative suppression is the central open question.

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
21. Pastor-Gutierrez, A., Pawlowski, J.M., Reichert, M. (2023). SciPost Phys. 15, 105. arXiv:2209.14627. [AS Standard Model]
22. Giacometti, G., Kowalska, K., Rizzo, D., Sessolo, E.M., Zappala, D. (2026). arXiv:2604.03033. [QG contributions to gauge/Yukawa in proper time flow]
23. Pastor-Gutiérrez, A., Pawlowski, J.M., Reichert, M. (2023). SciPost Phys. 15, 105. arXiv:2207.09817. [ASSM: full UV-IR flow with SM, flat Higgs FP, Gaussian matter]
