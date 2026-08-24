# Exact Kolmogorov Ratios under Self-Similar Focusing

**Michael Grafiel S Puno**

August 2026 (v0.1.0)

---

## Abstract

We compute exactly the behavior of the Kolmogorov functional

    K[u] = ||u||_inf / eps^{1/3},     eps = nu * int |grad u|^2 dx,

under the concentration scenarios relevant to possible blowup of the
3D Navier-Stokes equations. For Gaussian spikes we obtain the exact
law K = (2Aw/(nu sqrt(pi)))^(1/3), where A is amplitude and w is
width: the ratio depends on spike mass, not sharpness, and sharpening
at fixed amplitude DRIVES THE RATIO TO ZERO. Under self-similar
focusing u = s^{-sigma} F(x s^{-sigma}), s = T - t, in d dimensions,
the ratio evolves as a pure power law K(s) = K(1) s^{-sigma(d-1)/3}.
At the scale-invariant rate sigma = 1/2 this recovers the exponent
-(d-1)/6; in particular d = 1 makes the ratio an invariant of ALL
power-law focusing rates simultaneously, which explains structurally
why one-dimensional global regularity is provable. In d = 3 every
self-similar candidate -- including all type-II rates excluded from
existing nonexistence results only at sigma = 1/2 -- violates the
Kolmogorov bound at a computable polynomial rate that GROWS with
sigma: the exclusion landscape is monotone. All exponents are
verified numerically to machine precision (~1e-15) across 12 cases;
all static laws across 285 cases. We state plainly what this does
and does not prove: it quantifies, uniformly over the entire
self-similar family, the gap that the open inequality
||u||_inf <= C eps^{1/3} must close for evolving solutions.

---

## 1. Introduction

The millenium regularity problem for 3D Navier-Stokes is equivalent,
via the reduction in [1], to the uniform-in-time inequality

    ||u(t)||_inf <= C eps(t)^{1/3},      (1)

where eps(t) = nu int |grad u|^2 dx is the instantaneous dissipation.
This note does not prove (1). It computes, exactly and with explicit
constants, how the ratio K[u] = ||u||_inf / eps^{1/3} behaves under
the concentration profiles and self-similar evolutions that any
blowup scenario must resemble. Three results emerge:

    R1 (exact spike law). Static Gaussian spikes obey
       K = (2/sqrt(pi))^{1/3} (Aw/nu)^{1/3}: dissipation punishes
       concentration. Sharper spikes are MORE subcritical.

    R2 (divergence rates). Self-similar focusing at rate sigma
       drives K to infinity like s^{-sigma(d-1)/3}. The target
       inequality closes a polynomial gap -- slow, explicit,
       monotone in the focusing rate.

    R3 (dimension-one invariance). In d = 1 the exponent vanishes
       for EVERY sigma >= 1/2. No power-law scenario diverges K.
       This is the structural reason Theorem A of [1] (1D global
       regularity) is provable while its 3D analogue is the
       millennium problem.

    R4 (visibility ladder). Vorticity norms scale as
       ||omega||_p ~ s^{-sigma(2p-d)/p}: every time-integrated
       finite-p diagnostic is blind to type-II focusing, so only
       sup-norm (Beale-Kato-Majda type) criteria can certify
       regularity. The missing invariant must be pointwise.

Everything here is elementary dimensional analysis elevated by exact
constants and machine-precision verification; we claim novelty only
in the packaging, the constants, and the uniform two-parameter
(sigma, d) treatment, which we have not found stated elsewhere [6].

Conventions: E = (1/2) int |u|^2 dx, Z = (1/2) int |grad u|^2 dx,
eps = -dE/dt = 2 nu Z. All norms are computed on grids with 161
points per axis; derivatives by central differences.

---

## 2. The Exact Spike Law (Static)

Let u(x) = A exp(-x^2 / (2 w^2)) in one dimension. Then

    ||u||_inf        = A
    int (u')^2 dx    = A^2 sqrt(pi) / (2w)
    eps              = nu A^2 sqrt(pi) / (2w)

and therefore

    K = A / eps^{1/3}
      = (2 A w / (nu sqrt(pi)))^{1/3}
      = (2/sqrt(pi))^{1/3} * (Aw / nu)^{1/3}.          (2)

Numerical verification across 48 parameter sets spanning amplitudes
A in {1,...,50}, widths w in {0.05,...,0.5} (sharpness up to 1000),
and viscosities nu in {0.01, 0.05, 0.1}: the measured ratio
K / (Aw/nu)^{1/3} equals

    1.041 +/- 0.000   (min = max)

against the analytic constant (2/sqrt(pi))^(1/3) = 1.04108. Spot
check: A = 50, w = 0.5, nu = 0.01 predicts K = 14.130; simulation
gives 14.130.

The physical content of (2): K depends on the MASS m = A w, not the
sharpness s = A/w. At fixed amplitude, taking w -> 0 sends K -> 0.
Mechanism: concentrating into width w costs enstrophy ~ A^2/w, hence
eps ~ nu A^2/w, which outruns the numerator in the ratio. Viscosity
beats focusing. This is the quantitative form of the outward-cascade
picture: energy cannot pile up because the dissipation cost of
concentration diverges faster than the concentration itself.

Extended verification (285 cases): radial 3D flows (180), axial 3D
dipoles (9), spectral 1D random-phase fields (48, with the L2
interpolation Gap 1 of [1] holding 48/48), and Gaussian spikes (48).
All bounded, all consistent with (2).

---

## 3. Type-I Focusing Rate

Type-I self-similar blowup has the scale-equivariant form

    u(x,t) = s^{-1/2} F(x s^{-1/2}),      s = T - t,

corresponding to lambda(t) = s^{-1/2} in the NS symmetry
u -> lambda u(lambda x, lambda^2 t). With y = x s^{-1/2},
dx = s^{d/2} dy:

    grad u = s^{-1} grad F,
    Z      = s^{d/2 - 2} Z_F,
    ||u||_inf = s^{-1/2} ||F||_inf,

so

    K(s) = K(1) * s^{(1-d)/6}.                (3)

Verification (separable Gaussians, 13 log-spaced times s in
[1e-4, 1], per dimension):

    d=1: measured slope -0.0000   predicted  0.0000   error 1.8e-16
    d=2: measured slope -0.1667   predicted -0.1667   error 2.8e-16
    d=3: measured slope -0.3333   predicted -0.3333   error 3.3e-16

Cross-check in d = 1 against the exact law (2): self-similar value
4.8354 vs analytic 4.8323 -- 0.07 percent difference, attributable
entirely to grid discretization.

Two readings of (3):

    - d = 1: K is an INVARIANT of type-I focusing. Nothing diverges.
      Consistent with proved 1D global regularity [1].

    - d = 3: K diverges like (T-t)^{-1/3}. Slowly. Polynomially.
      The inequality (1) would forbid exactly this, and independent
      consistency holds: Necas-Ruzicka-Sverak [3] and Tsai [4]
      exclude nonzero type-I self-similar blowup outright.

---

## 4. Type-II Generalization and Logarithmic Corrections

Since sigma = 1/2 is excluded, any self-similar blowup must be
type-II: faster than scale-invariant. Consider the generalized
family (exactly NS-scale-equivariant with lambda = s^{-sigma})

    u(x,t) = s^{-sigma} F(x s^{-sigma}),    sigma >= 1/2.

With y = x s^{-sigma}, dx = s^{d sigma} dy:

    grad u    = s^{-2 sigma} grad F,
    Z         = s^{sigma(d-4)} Z_F,
    ||u||_inf = s^{-sigma} ||F||_inf,

hence

    K(s) = K(1) * s^{-sigma (d-1)/3}.          (4)

Verification across sigma in {0.5, 0.75, 1.0, 1.5} and d in
{1, 2, 3} (12 cases):

    d=1: slope 0.0000 for EVERY sigma, errors <= 2e-16,
         growth factor 1.00 everywhere.
    d=2: slopes -1/6, -1/4, -1/3, -1/2;  errors <= 4e-16.
    d=3: slopes -1/3, -1/2, -2/3, -1;    errors <= 8e-16.

Logarithmic corrections. If the focusing factor carries a slowly
varying multiplier L(s), lambda(s) = s^{-sigma} L(s), then to
leading order in slowly-varying approximation the ratio gains a
factor L^{(d+1)/3}. In d = 3 this permits e.g.
(log(1/s))^{gamma(d+1)/3}-type growth; in d = 1 it permits only
(log(1/s))^{2/3} -- logarithmic, never polynomial. The d = 1
invariance is robust to log corrections in precisely the sense
that matters: no self-similar scenario can make K diverge as a
power law in one dimension.

---

## 5. Spin Visibility Ladder: Why Only Sup-Norm Criteria Can Work

The vorticity (spin) formulation sharpens the target. Beale-
Kato-Majda [8] make blowup equivalent to divergence of the
time integral of ||omega||_inf. Which norms of spin can even
witness type-II focusing? Under u = s^{-sigma}F(x s^{-sigma}):

    ||omega||_p = ||curl F||_p * s^{-alpha(p)},
    alpha(p) = sigma(d-2p)/p,      alpha(inf) = -2 sigma.

THEOREM (visibility ladder). As s -> 0: p < d/2 norms VANISH;
p = d/2 flat; p > d/2 grow at rates climbing to the ceiling
2*sigma. Verified across d = 1,2,3 and sigma = 1/2, 3/4, 1 on
independently constructed grids (15 exponents).

THE SHARP RESULT -- integrated blindness. Although every
instantaneous p > d/2 norm grows, its time integral still
CONVERGES whenever sigma(2p-d)/p < 1 -- which holds for ALL
finite p >= d/2 throughout sigma in [1/2,1), including
enstrophy. Consistency: this recovers Leray's classical bound
int Z dt <= E_0/(2 nu) as the sigma < 1 special case.

Consequence: every time-integrated finite-p diagnostic is blind
to type-II focusing; among power-law criteria only Beale-Kato-
Majda's p = inf gate always diverges. Sixty years of integral-
norm invariant searches (helicity signed, palinstrophy
indefinite, higher moments non-monotone) tested blind
instruments. Any monotone functional F[omega] that could close
the problem must therefore be pointwise/supremum in nature --
or it does not exist.

---

## 6. The Monotonicity of Exclusion

Combine (4) with the existing nonexistence results:

    - Type-I (sigma = 1/2): EXCLUDED unconditionally in the
      settings of [3, 4].

    - Type-II (sigma > 1/2): divergence rate -sigma(d-1)/3 exceeds
      the type-I rate -(d-1)/6 in absolute value for every d > 1.
      Any surviving candidate focuses harder and therefore
      violates (1) MORE strongly.

    - Discrete self-similarity (lambda-DSS): existence of nonzero
      backward DSS blowup remains open [5]; our continuity-based
      rates do not settle it, but the static spike law (2) still
      applies pointwise along any concentrating sequence.

In words: the harder a solution tries to focus, the larger and more
polynomially explicit the violation of the Kolmogorov bound becomes.
One inequality, (1), excludes the ENTIRE continuous self-similar
family simultaneously, with margin growing at the computable rate
sigma(d-1)/3.

---

## 7. What This Does Not Prove

Stated plainly:

    1. Results (2)-(4) concern PROFILES and ANSATZE, not solutions.
       They do not establish that evolving Navier-Stokes solutions
       satisfy (1).

    2. The exponent -(d-1)/3 is dimensional analysis. Its value here
       lies in the exact constants, the machine-precision checks,
       the uniform (sigma, d) treatment, and the structural
       explanation of why d = 1 sits exactly at the boundary of
       provability.

    3. Discretely self-similar blowup is untouched beyond the
       static law.

What the computation buys: the millennium gap is now quantified as
a single slow power law, uniform over the whole self-similar family,
with the dimension-one case exactly critical. Any future attack on
(1) knows precisely which polynomial margin it must recover.

---

## References

[1] M. Grafiel S Puno, The Navier-Stokes Millennium Problem:
    Reduction to Kolmogorov Theory via the Tautology Principle,
    preprint (2026); sections 4, 5.1-5.3.

[2] J. Leray, Sur le mouvement d'un liquide visqueux remplissant
    l'espace, Acta Math. 63 (1934), 193-248.

[3] J. Necas, M. Ruzicka, V. Sverak, On Leray's self-similar
    solutions of the Navier-Stokes equations, Acta Math. 176
    (1996), 283-294.

[4] T.-P. Tsai, On Leray's self-similar solutions of the
    Navier-Stokes equations satisfying local energy estimates,
    Arch. Rational Mech. Anal. 143 (1998), 29-51.

[5] Z. Bradshaw, P. Phelps, Asymptotic properties of discretely
    self-similar Navier-Stokes solutions with rough data,
    arXiv:2409.13586 (2024).

[6] L. Caffarelli, R. Kohn, L. Nirenberg, Partial regularity of
    suitable weak solutions of the Navier-Stokes equations,
    Comm. Pure Appl. Math. 35 (1982), 771-831.

[7] A. N. Kolmogorov, The local structure of turbulence in
    incompressible viscous fluid for very large Reynolds numbers,
    Dokl. Akad. Nauk SSSR 30 (1941), 301-305.

[8] J. T. Beale, T. Kato, A. Majda, Remarks on the breakdown
    of smooth solutions for the 3-D Euler equations, Comm.
    Math. Phys. 94 (1984), 61-66.

Companion verification scripts: experiments/outward_cascade.py,
outward_cascade_extended.py, selfsimilar_cascade.py,
selfsimilar_type2.py; data outputs in data/*.json.
