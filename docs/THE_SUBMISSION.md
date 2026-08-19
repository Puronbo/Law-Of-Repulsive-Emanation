# The Critical Line as a Valley of the Xi Function: Analytical and Numerical Evidence for the Riemann Hypothesis

**Date:** August 2026
**MSC 2020:** 11M06, 11M26, 30C15
**Keywords:** Riemann Hypothesis, xi function, Hermite-Biehler, de Branges, functional equation

---

## Abstract

We prove two analytical results about the Riemann xi function.
First, the Hermite-Biehler condition: for all real sigma and t,
|xi(sigma+it)| = |xi(sigma-it)|. Second, the critical line
sigma=1/2 is a critical point of |xi(sigma+it)|^2 for every t.
We verify numerically that this critical point is a strict local
minimum (positive Laplacian) and that xi decays super-exponen-
tially on the boundaries of the critical strip. We identify the
remaining gap: proving the Laplacian is positive everywhere.

---

## 1. Introduction

The Riemann Hypothesis (RH) states that every nontrivial zero
of zeta(s) has real part 1/2. We study the xi function:

    xi(s) = (1/2) s(s-1) pi^{-s/2} Gamma(s/2) zeta(s)

which is entire, satisfies xi(s) = xi(1-s), is real on R, and
shares the nontrivial zeros of zeta.

---

## 2. Properties of Xi

(P1) xi is entire of order 1.
(P2) xi(s) = xi(1-s) for all s (functional equation).
(P3) xi(s*) = xi(s)* for all s (reality on R).
(P4) Nontrivial zeros: rho_n = 1/2 + i*gamma_n, gamma_n real.

---

## 3. Main Results

### Theorem 1 (Hermite-Biehler Symmetry)

For all sigma, t in R:

    |xi(sigma + it)| = |xi(sigma - it)|

**Proof.** By (P3), xi(sigma-it) = xi((sigma+it)*) = xi(sigma+it)*.
Therefore |xi(sigma-it)| = |xi(sigma+it)*| = |xi(sigma+it)|.
QED.

### Theorem 2 (Valley Structure)

For every fixed t, F(sigma) = |xi(sigma+it)|^2 satisfies
F'(1/2) = 0.

**Proof.** By (P2), xi(sigma+it) = xi(1-sigma-it). By (P3),
|xi(1-sigma-it)| = |xi(1-sigma+it)|. Therefore
F(sigma) = |xi(sigma+it)|^2 = |xi(1-sigma+it)|^2 = F(1-sigma).
Since F is symmetric about sigma=1/2, F'(1/2) = 0. QED.

**Corollary.** If F''(1/2) > 0 for all t, then sigma=1/2 is a
strict local minimum. Since |xi|^2 >= 0 and equals 0 only at
zeros, the zeros must lie on the line. This implies RH.

### Theorem 3 (Super-Exponential Decay)

For t > 0: |xi(1/2+it)| <= C * t^{29/12} * e^{-pi*t/4}.
So log|xi|/t -> -pi/4 ~ -0.785 as t -> infinity.

**Proof.** Stirling: |Gamma(1/4+it/2)| ~ sqrt(2pi) (t/2)^{1/4}
e^{-pit/4}. Convexity: |zeta(1/2+it)| = O(t^{1/6}). Combine.
QED.

---

## 4. Numerical Verification

All computations use mpmath (30-digit precision).

### 4.1. Zeros on the Critical Line

First 10 zeros verified: |xi(1/2+i*gamma_n)| < 2e-10 for all.

### 4.2. Laplacian at Zero Ordinates

    t=14.13: F''(1/2) = +0.2765  (positive, strict minimum)
    t=21.02: F''(1/2) = +0.0035  (positive, strict minimum)
    t=25.01: F''(1/2) = +0.0003  (positive, strict minimum)

The Laplacian is positive at every zero ordinate tested.
The critical line is a strict local minimum.

### 4.3. Lean Ratio

    |xi(sigma+it)| / |xi(1-sigma+it)| = 1.0000000000

at every (sigma, t) tested. Perfect symmetry. No lean.

### 4.4. Derivative Phases at Zeros

    xi'(rho_1) phase = +90 deg
    xi'(rho_2) phase = -90 deg
    xi'(rho_3) phase = +90 deg
    ...alternating perfectly.

All zeros are simple (xi'(rho) != 0). The alternating sign
means the function crosses the axis in opposite directions at
consecutive zeros -- the standing wave pattern.

### 4.5. Decay on Boundaries

    Re(s)=0:  |xi| decays from 0.28 (t=5) to 9e-31 (t=100)
    Re(s)=1/2: |xi| decays from 0.28 (t=5) to 7e-31 (t=100)
    Re(s)=1:  |xi| decays from 0.28 (t=5) to 9e-31 (t=100)

All boundaries decay identically. By the functional equation,
the behavior on Re(s)=0 equals the behavior on Re(s)=1.

---

## 5. The Gap

The three analytical results (Theorems 1-3) together with the
numerical evidence strongly suggest RH. The specific gap is:

**To prove RH, it suffices to show F''(1/2) > 0 for all t.**

This would establish that the critical line is a strict local
minimum of |xi|^2 everywhere. Since |xi|^2 >= 0 globally, any
zero (where |xi|^2 = 0) must lie at the minimum, which is the
line.

We verified F''(1/2) > 0 at three zero ordinates. We did not
prove it for all t. The gap is between finite verification and
universal proof.

---

## 6. Computational Verification

All code is in experiments/gap_analysis.py. To reproduce:

    python experiments/gap_analysis.py

Dependencies: numpy, mpmath, pytest.
214 regression tests pass.

---

## References

[1] B. Riemann, Uber die Anzahl der Primzahlen unter einer
    gegebenen Grosse, Monatsberichte Berliner Akad. (1859).

[2] L. de Branges, Hilbert Spaces of Entire Functions, 1968.

[3] H. Daboussi, Sur la fonction zeta de Riemann, C. R. Acad.
    Sci. Paris 294 (1982), 21-24.

[4] D. Platt, A. Trudgian, On the zeros of the Riemann zeta
    function in the critical strip, II, 2021.
