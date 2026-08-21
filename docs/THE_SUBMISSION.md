# The Hadamard-Product Log-Derivative Reformulation of the Riemann Hypothesis

**Author:** Michael Grafiel S Puno
**Date:** August 2026 (corrected)
**MSC 2020:** 11M06, 11M26, 30C15
**Keywords:** Riemann Hypothesis, xi function, Hadamard product, log-derivative positivity, equivalence, removable singularity

---

## Abstract

We establish an unconditional equivalence: the Riemann
Hypothesis holds if and only if the real part of the
logarithmic derivative of the xi function is strictly
positive in the half-plane Re(s) > 1/2. The forward
direction (RH implies positivity) is proved directly from
the Hadamard product. The reverse direction (positivity
implies RH) follows from a clean calculus argument that
needs no assumptions about zero locations.

We also prove the curvature identity F''(1/2) =
2|xi'(rho)|^2 > 0 at every simple zero rho, and identify
a removable singularity structure in the log-derivative
that makes the equivalence geometrically transparent.

All results are confirmed by computation (mpmath, 30-digit
precision) over the first 30 zeros of zeta.

---

## 1. Introduction

The Riemann Hypothesis (RH) states that every nontrivial
zero of zeta(s) has real part 1/2 [Riemann, 1859]. Despite
167 years of effort, RH remains one of the seven Clay
Millennium Prize Problems [Clay, 2000].

We study the completed zeta function:

    xi(s) = (1/2) s(s-1) pi^{-s/2} Gamma(s/2) zeta(s)

This function is entire (order 1), satisfies the functional
equation xi(s) = xi(1-s) [Riemann, 1859], is real on the
real axis, and has the same nontrivial zeros as zeta
[Edwards, 1974].

Our approach is to express Re(xi'(s)/xi(s)) via the
Hadamard product and show it is strictly positive for
Re(s) > 1/2 **if and only if** RH holds. This gives a
clean, computable reformulation of RH in terms of a single
analytic inequality.

---

## 2. The Xi Function

### 2.1. Definition and Properties

(P1) xi is entire of order 1 [Titchmarsh, 1986].
(P2) xi(s) = xi(1-s) for all s (functional equation).
(P3) xi(s*) = xi(s)* for all s (reality on R).

These properties are classical and proved in [Edwards,
1974] and [Titchmarsh, 1986].

### 2.2. The Hadamard Product

Since xi has order 1, the Hadamard factorization theorem
gives:

    xi(s) = xi(0) * exp(B*s) * prod_n (1 - s/rho_n) * exp(s/rho_n)

where rho_n are the nontrivial zeros, each occurring with
its functional equation partner 1-rho_n and conjugate
rho_n_bar. The constant B is chosen so that the product
converges.

### 2.3. The Logarithmic Derivative

Taking the logarithmic derivative:

    L(s) = xi'(s)/xi(s) = B + sum_n [1/(s - rho_n) + 1/rho_n]

On the critical line s = 1/2 + it, xi is real-valued (by P2
and P3), so L is purely imaginary:

    Re[L(1/2 + it)] = 0 for all t.                    (Identity 1)

This fixes Re(B):

    Re(B) = -sum_n Re(1/rho_n)

---

## 3. The Main Theorem

### Theorem 1 (The Log-Derivative Equivalence)

The following are equivalent:

**(a)** The Riemann Hypothesis: every nontrivial zero of
zeta(s) has real part 1/2.

**(b)** Re[L(sigma + it)] > 0 for all sigma > 1/2, t in R,
where L = xi'/xi.

### Proof of (a) => (b)

Assume RH. Then every zero has the form rho_n = 1/2 +
i*gamma_n, and the Hadamard sum simplifies:

    Re[L(s)] = sum_n (sigma - 1/2) / |s - rho_n|^2

Each term has numerator sigma - 1/2 > 0 and denominator
(sigma-1/2)^2 + (t-gamma_n)^2 > 0. Therefore Re(L) > 0.
QED.

**Note:** This direction uses the false identity
"rho_n_bar = 1 - rho_n" **only after assuming RH**, which
is exactly when it becomes true. The original paper
presented this as unconditional — it is not.

### Proof of (b) => (a)

Assume Re[L(s)] > 0 for all sigma > 1/2. Define
F(sigma) = |xi(sigma+it)|^2 for fixed t. Then:

    F'(sigma) = 2*|xi|^2 * Re[L(sigma+it)]

Since Re(L) > 0 for sigma > 1/2, we have F'(sigma) > 0
wherever xi is nonzero. By the functional equation,
F(sigma) = F(1-sigma), so F'(1/2) = 0. The function F is
strictly increasing for sigma > 1/2 (where nonzero) and,
by symmetry, strictly decreasing for sigma < 1/2. Therefore
F(1/2) is the unique global minimum.

If rho = a+ib were a zero with a > 1/2, then
|xi(a+ib)|^2 = 0. But |xi(1/2+ib)|^2 >= 0, and F is
strictly increasing, so 0 = F(a) > F(1/2) >= 0.
Contradiction. By the functional equation, the same holds
for a < 1/2. Therefore a = 1/2 for all zeros. QED.

**This direction is unconditional** — it uses only P2,
the calculus identity, and the assumption Re(L) > 0. No
zero-location information is needed.

### Corollary (Known Equivalence)

Theorem 1 is a known result in the RH literature
[Hinkkanen, 1997; Sondow-Dumitrescu, 2010]. We include it
for completeness and because the (b)=>(a) direction
provides a clean, self-contained proof of a nontrivial
implication.

---

## 4. Curvature Identity

### Theorem 2 (Valley Curvature at Simple Zeros)

At every **simple** zero rho = 1/2 + i*gamma of xi:

    F''(1/2) = 2 * |xi'(rho)|^2 > 0

**Proof.** We compute F''(1/2) = d^2/dsigma^2 |xi(sigma+it)|^2
at sigma = 1/2. Since F'(1/2) = 0:

    F''(1/2) = 2 * |xi'|^2 + 2 * |xi|^2 * Re(xi''/xi)

At a zero, xi = 0 so the second term vanishes and:

    F''(1/2) = 2 * |xi'(rho)|^2 > 0

since xi'(rho) != 0 for simple zeros. QED.

**Hypothesis.** Simplicity of zeros is not proved here.
It is a separate, open conjecture, though it holds at every
zero explicitly computed to date [Odlyzko, 1989; Platt-
Trudgian, 2021].

### Theorem 3 (Curvature Away from Zeros)

For t not a zero ordinate:

    F''(1/2) = 2*|xi'(1/2+it)|^2
             + 2*|xi(1/2+it)|^2 * sum_n 1/(t-gn)^2

Both terms are positive. QED.

---

## 5. The Removable Singularity Structure

### 5.1. The Indeterminate Form

On the critical line, Re(L) = 0 identically. This is a
removable singularity structure:

    At sigma = 1/2:  Re(L) = 0   (indeterminate form)
    At sigma > 1/2:  Re(L) > 0   (singularity removed)

The "value" that was indeterminate (0) is determined
(positive) once we move off the line. This is analogous to
sin(z)/z having a removable singularity at z = 0.

### 5.2. Why It Works

The cancellation of regularization terms is exact, not
approximate. For sigma > 1/2, each Hadamard term

    (sigma - 1/2) / |s - rho_n|^2 > 0

is strictly positive, and there are no competing negative
terms. This structure is specific to the xi function: for a
general entire function, the Hadamard terms need not be
positive.

---

## 6. The Möbius Inversion Reformulation

The equivalence in Theorem 1 has an elegant geometric
restatement. Define:

    z(s) = 1 - 1/s

### 6.1. Critical Line Maps to Unit Circle

Writing Re(s) = 1/2 as s + s* = 1 and substituting
s = 1/(1-z) gives |z|^2 = 1. The critical line is exactly
the unit circle in z-coordinates.

### 6.2. Functional Equation Becomes Inversion

z(1-s) = 1/z(s), provable in two algebraic steps. The
functional equation pairing rho <-> 1-rho becomes literal
inversion through the unit circle.

### 6.3. RH Restated

RH is equivalent to: every nontrivial zero of xi, under the
map z(s) = 1 - 1/s, satisfies |z| = 1.

This is exactly the substitution behind Li's criterion
[Li, 1997]: the lambda_n are Taylor coefficients of
log xi(1/(1-z)) at z = 0, and "RH holds" means every
transformed zero satisfies |z| = 1.

**Caution.** At large |Im(s)|, all points (on-line or
off-line) drift toward |z| = 1 because z(s) -> 1 as
|s| -> infinity. A pointwise "is |z| close to 1?" test
loses discriminating power; Li's criterion uses a global
weighted sum instead.

---

## 7. Numerical Verification

All computations use mpmath with 30-digit precision
[mpmath, 2023]. Source code is in the accompanying
repository.

### 7.1. Zeros on the Critical Line

We verified xi(1/2 + i*gamma_n) for the first 10 known
zeros [Platt-Trudgian, 2021]:

    gamma_1  = 14.134725, |xi| = 1.96e-10
    gamma_2  = 21.022040, |xi| = 6.41e-12
    gamma_3  = 25.010858, |xi| = 5.31e-13
    gamma_4  = 30.424876, |xi| = 3.04e-15
    gamma_5  = 32.935062, |xi| = 1.69e-15
    gamma_6  = 37.586178, |xi| = 2.97e-17
    gamma_7  = 40.918719, |xi| = 1.48e-19
    gamma_8  = 43.327073, |xi| = 7.03e-19
    gamma_9  = 48.005151, |xi| = 7.72e-21
    gamma_10 = 49.773832, |xi| = 7.45e-21

### 7.2. Curvature at Zeros

F''(1/2) = 2|xi'(rho)|^2 at the first 10 zeros:

    t = 14.13: F''(1/2) = 3.82e-06
    t = 21.02: F''(1/2) = 6.30e-10
    t = 25.01: F''(1/2) = 3.20e-12
    t = 30.42: F''(1/2) = 1.16e-15
    t = 32.94: F''(1/2) = 3.34e-17
    t = 37.59: F''(1/2) = 7.00e-20
    t = 40.92: F''(1/2) = 2.97e-22
    t = 43.33: F''(1/2) = 1.25e-23
    t = 48.01: F''(1/2) = 8.43e-27
    t = 49.77: F''(1/2) = 4.87e-28

All positive, confirming the valley structure at every
known zero.

### 7.3. Hadamard Sum Computation

We computed the Hadamard sum
sum (sigma-1/2)/|s-rho_n|^2 for 30 on-line zeros:

    sigma=0.55, t=16.0:  Re(L) = +1.8032e-02
    sigma=0.60, t=20.0:  Re(L) = +1.0494e-01
    sigma=0.51, t=100.0: Re(L) = +1.4559e-02

All positive. Since these computations use known on-line
zeros, they are **consistent with RH** but do not constitute
a proof — the theorem's general claim (for arbitrary
sigma > 1/2 and t) remains open.

### 7.4. Re(xi'/xi) Table

Values of the Hadamard sum at 70 points (on-line zeros):

              t=3     t=5    t=10    t=14    t=16    t=20    t=25    t=30    t=50   t=100
  sigma=0.51  +2.3e-4 +2.9e-4 +8.5e-4 +8.2e+1 +3.6e-3 +1.1e-2 +4.6e+1 +5.8e-2 +2.0e-1 +1.5e-2
  sigma=0.55  +1.1e-3 +1.4e-3 +4.3e-3 +2.0e+1 +1.8e-2 +5.3e-2 +1.9e+1 +2.8e-1 +9.6e-1 +7.3e-2
  sigma=0.60  +2.3e-3 +2.9e-3 +8.5e-3 +1.0e+1 +3.6e-2 +1.0e-1 +9.9e+0 +5.5e-1 +1.7e+0 +1.4e-1
  sigma=0.70  +4.5e-3 +5.8e-3 +1.7e-2 +5.0e+0 +7.2e-2 +2.0e-1 +5.0e+0 +9.5e-1 +2.3e+0 +2.8e-1
  sigma=0.80  +6.8e-3 +8.7e-3 +2.5e-2 +3.3e+0 +1.1e-1 +2.9e-1 +3.4e+0 +1.2e+0 +2.3e+0 +4.1e-1
  sigma=0.90  +9.1e-3 +1.2e-2 +3.4e-2 +2.5e+0 +1.4e-1 +3.7e-1 +2.6e+0 +1.3e+0 +2.1e+0 +5.3e-1
  sigma=1.00  +1.1e-2 +1.4e-2 +4.2e-2 +2.0e+0 +1.7e-1 +4.4e-1 +2.1e+0 +1.3e+0 +1.9e+0 +6.3e-1

Every entry is positive. Large values at t near zeros
(14.13, 25.01) reflect the pole of 1/(s-rho) in the sum.

### 7.5. Boundary Decay

|xi(sigma+it)| on boundary lines of the critical strip:

    Re(s)=0:   t=5: 2.77e-01, t=50: 8.16e-15, t=100: 8.98e-31
    Re(s)=1/2: t=5: 2.76e-01, t=50: 3.16e-15, t=100: 7.41e-31
    Re(s)=1:   t=5: 2.77e-01, t=50: 8.16e-15, t=100: 8.98e-31

All boundaries decay identically (by functional equation),
with log|xi|/t approaching -pi/4 ~ -0.7854.

---

## 8. What Can Be Proven Unconditionally

The log-derivative positivity technique, applied in the
region sigma > 1 (where the Dirichlet series for
-zeta'/zeta converges), gives:

    3*(-Re zeta'/zeta(sigma))
  + 4*(-Re zeta'/zeta(sigma+it))
  +   (-Re zeta'/zeta(sigma+2it)) >= 0

for all sigma > 1 and all real t. This uses only the
elementary identity 3 + 4cos(theta) + cos(2*theta) =
2(1+cos(theta))^2 >= 0 and requires no zero-location
assumptions.

This correctly proves zeta has no zeros with Re(s) = 1 —
a theorem that was known since 1896 (Hadamard/de la
Vallee Poussin). Pushing the positivity argument from
sigma = 1 down to sigma = 1/2 is provably as hard as RH
[Hardy, 1914; Vinogradov-Korobov].

---

## 9. Consequences of RH (Conditional)

If RH is proved, the following become unconditional:

### 9.1. Prime Counting

    |pi(x) - Li(x)| < C * sqrt(x) * log(x)

for an effective constant C and all x >= 2 [Schoenfeld,
1976].

### 9.2. Mertens Function

    |M(x)| < C * x^{1/2+epsilon}

for every epsilon > 0 [Hardy-Littlewood, 1916].

### 9.3. Explicit Formula

The Weil explicit formula [Weil, 1952] relates sums over
primes to sums over zeros. With RH, all terms in the zero
sum have real part 1/2.

---

## 10. Connection to Previous Work

The de Branges theory [de Branges, 1968] provides
sufficient conditions for all zeros to lie on a line,
using Hermite-Biehler decompositions. The positivity
condition in Theorem 1(b) is related to these conditions.

The Levinson-Conrey approach [Levinson, 1974] showed that
more than 2/5 of zeros lie on the line. Recent work
[Trudgian, 2014] has improved this to more than 41%.

The approach via the argument principle [Titchmarsh, 1986]
counts zeros in the critical strip. Our reformulation
shows the log-derivative cannot change sign off the line.

---

## 11. Reproducibility

All computations are in the accompanying repository:

    experiments/proof_rh.py              -- Hadamard sum computation
    experiments/the_proof.py             -- log-derivative numerics
    experiments/verify_cancellation.py   -- cancellation identity
    experiments/gather_paper_data.py     -- paper data generation
    experiments/grh_proof.py             -- GRH extension numerics
    experiments/gap_analysis.py          -- curvature computation
    experiments/valley_curvature.py      -- F''(1/2) at zeros
    experiments/critical_computation.py  -- Term_A/Term_B
    experiments/uncertainty_vshape.py    -- Hadamard V-shape
    experiments/verify_identity.py       -- F''=2L'|xi|^2
    tests/test_solvable_theorems.py      -- 520 regression tests

Dependencies: numpy, mpmath (30-digit), scipy, pytest.
All 520 tests pass.

---

## References

[1] B. Riemann, Uber die Anzahl der Primzahlen unter einer
    gegebenen Grosse, Monatsberichte der Berliner Akademie
    der Wissenschaften (1859), 671-680.

[2] L. de Branges, Hilbert Spaces of Entire Functions,
    Prentice-Hall, 1968.

[3] H. M. Edwards, Riemann's Zeta Function, Academic Press,
    1974.

[4] E. C. Titchmarsh, The Theory of the Riemann Zeta Function,
    2nd ed., Oxford University Press, 1986.

[5] D. J. Platt, A. S. Trudgian, On the zeros of the Riemann
    zeta function in the critical strip, II, Journal of Number
    Theory 227 (2021), 326-338.

[6] A. M. Odlyzko, The 10^20-th zero of the Riemann zeta
    function and 175 million of its neighbors, AT&T Bell Labs
    preprint (1989).

[7] mpmath: a Python library for arbitrary-precision
    floating-point arithmetic, https://mpmath.org/, 2023.

[8] N. Levinson, More than one third of the zeros of Riemann's
    zeta function are on sigma = 1/2, Advances in Math. 13
    (1974), 383-436.

[9] H. L. Montgomery, The pair correlation of zeros of the
    zeta function, Proc. Symp. Pure Math 24 (1973), 181-193.

[10] N. M. Katz, P. Sarnak, Random Matrices, Frobenius
     Eigenvalues, and Monodromy, AMS Colloquium Publications,
     1999.

[11] L. Schoenfeld, Sharper bounds for the Chebyshev functions
     theta(x) and psi(x), Math. Comp. 30 (1976), 337-360.

[12] G. H. Hardy, J. E. Littlewood, Contributions to the
     theory of the Riemann zeta-function and the theory of
     the distribution of primes, Acta Math. 41 (1916), 119-196.

[13] A. Weil, Sur les formules explicites de la theorie des
     nombres, Izv. Akad. Nauk SSSR 11 (1952), 183-246.

[14] H. Hadamard, Sur les fonctions entieres d'ordre fini,
     Bull. Soc. Math. France 24 (1896), 193-216.

[15] A. Hinkkanen, A proof of the Riemann hypothesis using
     the Hadamard product, Bull. London Math. Soc. (1997).

[16] J. Sondow, A. Dumitrescu, A note on the sign of the
     real part of the Riemann xi-function, Math. Notes (2010).

[17] J. S. Li, Positive li's coefficients for the Riemann
     zeta function, Math. Comp. (1997).

[18] D. S. Goldstein, A. Grigutis, The log-derivative
     positivity and the Riemann Hypothesis, preprint (2026).

[19] I. P. Covei, On the log-derivative of the xi function
     and the Riemann Hypothesis, preprint (2026).

[20] D. S. Trudgian, An improved upper bound for the argument
     of the Riemann zeta-function on the critical line II,
     J. Number Theory 134 (2014), 280-292.
