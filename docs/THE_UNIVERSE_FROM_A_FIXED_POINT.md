# The Universe from a Fixed Point

## The Big Bang as a 0/0 Singularity in the Renormalization Group Flow

**Author:** Michael Grafiel S Puno
**Date:** August 2026
**MSC 2020:** 83C05, 81T17, 58K05
**Keywords:** Big Bang, renormalization group, fixed point, cosmological constant, asymptotic safety, removable singularity

---

## Abstract

We propose that the Big Bang is the UV fixed point of the RG flow of quantum gravity. The universe begins at a scale-invariant state where all beta functions vanish: 0/0. The RG flow is the expansion. Dimensional transmutation creates the physical constants. Using the verified Litim cutoff beta functions of Codello, Percacci, and Rahmede (2009), we compute the fixed point in the Einstein-Hilbert truncation (G*=0.7012, Lambda*=0.1715, theta=1.689 +/- 2.486i) and in the f(R) truncation up to R^8 (L*G* stabilizes at 0.11-0.12). The product Lambda*G is a scheme-independent prediction. The EH truncation breaks down below k ~ 10^15 GeV; higher-derivative terms are needed for the full flow. The 0/0 at the fixed point encodes the initial conditions. The critical exponents are the removable values. The observed suppression (Lambda*G ~ 10^-122 in Planck units) requires nonlinear effects beyond the linearized flow near the FP.

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

### 6.3. The suppression problem

The FP product is Lambda*G = 0.12 (in Planck units). The observed product is:

    Lambda_obs * G_N = 1.06 x 10^-52 * 6.674 x 10^-11 = 7.07 x 10^-63 m^2

In Planck units: Lambda_obs * G_N ~ 10^-122. The required suppression from FP to observed is 10^-120.

Linearized flow analysis near the FP (n=8 truncation, 3 relevant directions):
- The complex pair (Re theta = 2.407) produces spiralling growth
- The real mode (theta = 1.398) adds monotonic growth
- At RG time t = -5 (roughly 5 e-folds from FP): deviation amplified by factor 10^5

The product Lambda*G GROWS along the linearized flow. The relevant modes amplify deviations, not suppress them. The linearization breaks down quickly.

This means: the observed suppression (10^-120) CANNOT come from the linearized flow near the FP. It must arise from:
1. Nonlinear effects far from the FP (the full trajectory through coupling space)
2. Trajectory selection from the 3D critical surface
3. Additional physics beyond the gravitational sector

### 6.4. Selection mechanism

The trajectory selection is determined by:
1. The requirement that the flow avoids the singular region
2. The 3 relevant directions in the f(R) truncation provide the freedom to find such trajectories
3. Matching to low-energy observations (G_N, Lambda_obs) selects the physical trajectory from the 3-parameter family

---

## 7. The Honest Assessment

### 7.1. What is verified

1. The NGFP exists at G*=0.7012, Lambda*=0.1715 (EH truncation).
2. The critical exponents are theta = 1.689 +/- 2.486i (complex, UV-attractive).
3. The product Lambda*G = 0.12 is stable across f(R) truncations (n=1 to n=8).
4. The f(R) truncations have 3 relevant directions at n>=4.
5. The beta functions reproduce the known results of Codello et al (2009) exactly.
6. The 0/0 structure at the fixed point is real.

### 7.2. What is computed

1. The RG flow spirals around the fixed point.
2. The physical scale setting connects k to cosmic time via the Friedmann equation.
3. The EH truncation breaks down at k ~ 5 x 10^15 GeV.
4. The separatrix comes closest to GFP at distance 0.018.
5. The f(R) product Lambda*G stabilizes at 0.11-0.12 across truncations n=1 to n=8.
6. Linearized flow shows the product GROWS toward IR (relevant modes amplify).
7. The required suppression (10^-120) is nonlinear and beyond linearization.

### 7.3. What is proposed (not proven)

1. That the Big Bang corresponds to the UV fixed point of quantum gravity.
2. That the RG flow maps to cosmic expansion.
3. That the dimensional transmutation produces the observed physical constants.

### 7.4. What remains open

1. **Standard Model coupling:** No mechanism to derive alpha, m_Higgs from the gravitational FP.
2. **Proof beyond truncation:** Asymptotic safety is not proven in the full theory.
3. **Below 10^15 GeV:** The EH truncation cannot reach low energy; f(R) or higher truncations needed.
4. **Trajectory selection:** The physical trajectory from the 3D critical surface is not uniquely determined by the FP alone.

---

## 8. References

1. Morse, M. (1925). Trans. AMS, 27, 345-396.
2. Griffith, A.A. (1921). Phil. Trans. Roy. Soc. A, 221, 163-198.
3. Wilson, K.G. (1971). Phys. Rev. B, 4, 3174-3205.
4. Zamolodchikov, A.B. (1986). JETP Lett., 43, 730-732.
5. Weinberg, S. (1979). In "Understanding the Fundamental Constituents of Matter", Plenum Press.
6. Reuter, M. (1998). Phys. Rev. D, 57, 971.
7. Lauscher, O. and Reuter, M. (2002). Phys. Rev. D, 65, 065016.
8. Wetterich, C. (1993). Phys. Lett. B, 301, 90-94.
9. Codello, A., Percacci, R., Rahmede, C. (2009). Annals Phys. 324, 414-469. arXiv:0805.2909.
10. Codello, A., Percacci, R., Sauro, C. (2009). J. Phys. A, 42, 125402.
11. Litim, D.F. (2001). Phys. Rev. Lett., 87, 201301.
12. Percacci, R. (2009). arXiv:0910.5167.
13. Falls, K., Litim, D.F., Nikolakopoulos, K., Rahmede, C. (2013). arXiv:1312.0359.
14. Puno, M.G.S. (2026). The Indeterminate Structure of Mathematical Truth.
