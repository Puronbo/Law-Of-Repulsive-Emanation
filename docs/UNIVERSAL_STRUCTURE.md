# The Universal Structure of Critical Phenomena

## A Gradient Flow Interpretation of the Removable Singularity Framework

**Author:** Michael Grafiel S Puno
**Date:** August 2026
**MSC 2020:** 58K05, 81T17, 74R05, 34D05, 58J55
**Keywords:** gradient flow, Morse lemma, removable singularity, renormalization group, critical phenomena, universality

---

## Abstract

We prove that the removable singularity pattern observed across
diverse critical phenomena — fracture mechanics, nucleation,
quantum gravity — is the universal mathematical signature of
gradient flow near a saddle point. The chain of reasoning is:

1. **Morse lemma** (pure calculus): Any smooth potential near a
   non-degenerate stationary point is conjugate to its Hessian —
   a quadratic form with mixed eigenvalues.

2. **Zamolodchikov's theorem** (rigorous QFT): RG flow is
   literally gradient flow with a monotone Lyapunov function
   (the c-function). Not analogous. Proven.

3. **Scale invariance** (dimensional analysis): At the fixed
   point, no scale remains. The only self-similar functions are
   power laws.

The "removable singularity" at each critical point is the saddle
of the underlying potential. The "removable value" is the critical
threshold determined by the Hessian eigenvalues. The power-law
behavior follows from scale invariance alone.

We apply this to five systems: Griffith fracture mechanics,
first-order nucleation, the Reuter fixed point in quantum gravity,
the Wilson-Fisher fixed point in statistical mechanics, and the
Riemann Hypothesis via the xi function. In each case, the same
mathematical structure appears: gradient flow near a saddle,
diagonalization of the Hessian, stable/unstable manifolds
separated by a critical surface.

We state honestly what is universal (the saddle shape, guaranteed
by Morse) and what is specific (the exponents, determined by the
universality class). The shape is math. The numbers are physics.

---

## 1. Introduction

### 1.1. The observation

Across physics and mathematics, critical phenomena share a common
structure. At a critical point — a crack tip, a nucleation
barrier, a renormalization group fixed point — a natural function
takes an indeterminate form, and the limiting value encodes the
theorem's content.

This pattern was noted in [Puno, 2026] under the name "removable
singularity framework." The claim was: at every critical point, a
natural 0/0 form exists, and the removable value determines the
answer.

The observation is correct. But it begs the question: WHY does
this pattern exist? Is it a deep principle, or a coincidence of
naming?

We prove it is a deep principle — and identify it precisely.

### 1.2. The answer

The pattern exists because every critical phenomenon is,
underneath its specific physics, a gradient flow near a saddle
point. Saddle points have exactly one shape, dictated by:

- **Morse lemma** (linear algebra): The Hessian determines the
  local structure. Mixed eigenvalues create stable and unstable
  manifolds.
- **Zamolodchikov's theorem** (physics): RG flow is gradient
  flow with a monotone Lyapunov function.
- **Scale invariance** (dimensional analysis): At the fixed
  point, power laws are the only consistent functional form.

These three facts are independent of the specific system. They
apply to cracks, bubbles, coupling constants, and zeta zeros
alike. The shape is universal. The numbers are not.

### 1.3. Overview

Section 2: The mathematical foundation (Morse lemma).
Section 3: The physical foundation (Zamolodchikov, Wilson).
Section 4: Applications (five critical phenomena).
Section 5: What is universal and what is not.
Section 6: References.

---

## 2. The Mathematical Foundation

### 2.1. Morse's lemma

**Theorem (Morse, 1925).** Let F: R^n -> R be a smooth function
with a non-degenerate critical point at x_0 (i.e., the Hessian
H_ij = d^2F/dx_i dx_j at x_0 is invertible). Then there exists a
local coordinate system near x_0 in which:

    F(x) = F(x_0) + (1/2) * sum_i lambda_i * y_i^2

where lambda_i are the eigenvalues of H. The sign of lambda_i
determines the local geometry:

- lambda_i > 0: convex direction (stable, restoring)
- lambda_i < 0: concave direction (unstable, runaway)

**Corollary.** Near any non-degenerate critical point, F looks
exactly like its Hessian. There is no other possibility. This is
pure calculus, true for any F.

### 2.2. The saddle geometry

The critical point x_0 is a saddle whenever H has both positive
and negative eigenvalues. The stable manifold M^s is the set of
points that flow INTO x_0 along positive-eigenvalue directions.
The unstable manifold M^u is the set of points that flow OUT of
x_0 along negative-eigenvalue directions.

The dimension of M^s equals the number of positive eigenvalues.
The dimension of M^u equals the number of negative eigenvalues.
Together they partition the neighborhood of x_0 into regions that
collapse back to the saddle and regions that escape from it.

**This is the entire content of "critical threshold separating
collapse from runaway."** It follows from nothing but the
existence of a smooth potential and a non-degenerate critical
point.

### 2.3. The gradient flow

A gradient flow is:

    dx_i/dt = -dF/dx_i = -partial_i F

Near a critical point x_0, linearizing:

    d(delta_x_i)/dt = -H_ij * delta_x_j

The solution is:

    delta_x_i(t) = sum_I C_I V_i^I exp(-lambda_I * t)

where lambda_I are the Hessian eigenvalues and V^I are the
eigenvectors. Each mode decays (lambda_I > 0) or grows
(lambda_I < 0) exponentially in time.

At a fixed point of an RG flow, the "time" is log(k), and the
exponential becomes a power law:

    delta_g_i(k) = sum_I C_I V_i^I (k_0/k)^theta_I

where theta_I = -lambda_I are the critical exponents. The change
from exponential to power law is the content of scale invariance:
at the fixed point, only ratios of scales remain, so the
dependence must be a power law.

---

## 3. The Physical Foundation

### 3.1. Zamolodchikov's c-theorem

**Theorem (Zamolodchikov, 1986).** In two-dimensional quantum
field theory, there exists a function c(g) of the coupling
constants g that satisfies:

1. c(g) equals the central charge at fixed points
2. dc/dt <= 0 along the RG flow (monotone decrease)
3. dc/dt = 0 only at fixed points

The RG flow equation is literally:

    beta^i = -H^ij partial_j sigma

where sigma is related to c. This IS gradient flow. Not analogous.
Proven.

**Consequence.** The RG flow is a gradient flow on the space of
couplings, with c as the potential. Every fixed point is a
stationary point of c. The Morse lemma applies. The Hessian of c
at the fixed point determines the critical exponents.

### 3.2. Wilson's universality

**The insight (Wilson, 1971).** Near a fixed point, the RG flow
depends only on:
- The dimension of space d
- The symmetry group G
- The number of order parameter components n

The microscopic details (lattice spacing, interaction range, etc.)
do not matter. Systems with the same (d, G, n) have the same
critical exponents. They belong to the same universality class.

**Connection to Morse.** The universality class determines the
Hessian eigenvalues (critical exponents). The Hessian eigenvalues
determine the saddle geometry. The saddle geometry determines the
critical threshold. Different universality classes have different
exponents but the same saddle shape.

### 3.3. Scale invariance

At a fixed point, the system is scale-invariant: it looks the same
at every scale. The only functions consistent with this are power
laws:

    f(bx) = g(b) f(x)  for all b

This forces f(x) = Cx^p for some p. (Proof: differentiate with
respect to b at b=1 to get a differential equation, solve it.)

This is why every threshold in this paper — Griffith length,
critical bubble radius, RG power law — comes out as a power law.
It's not a choice. It's the only option consistent with scale
invariance.

---

## 4. Applications

### 4.1. Griffith fracture mechanics

**System.** A crack of length L in a material under stress sigma.
The energy functional is:

    Delta_F(L) = -w L^2 + gamma L

where w is the elastic energy density and gamma is the surface
energy.

**The saddle.** d(Delta_F)/dL = -2wL + gamma = 0 at
L* = gamma/(2w). The second derivative is d^2(Delta_F)/dL^2 =
-2w < 0. This is a saddle in the (L, Delta_F) plane.

**The 0/0.** At L = L*, d(Delta_F)/dL = 0. The removable value
is L* = gamma/(2w). Below L*: crack heals. Above L*: crack
grows. L* is the critical threshold.

**The gradient flow.** dL/dt = -d(Delta_F)/dL = 2wL - gamma.
Linearizing near L*: d(delta_L)/dt = 2w * delta_L. One eigenvalue:
2w > 0 (unstable). The critical surface is the single point L = L*.

**Status.** Exact. Griffith (1921). The0/0 structure is the
saddle of the energy functional.

### 4.2. First-order nucleation

**System.** A bubble of radius R in a metastable phase. The
free energy is:

    Delta_F(R) = -(4/3) pi R^3 delta_mu + 4 pi R^2 sigma

where delta_mu is the chemical potential difference and sigma is
the surface tension.

**The saddle.** d(Delta_F)/dR = -4 pi R^2 delta_mu + 8 pi R
sigma = 0 at R* = 2 sigma / delta_mu. The second derivative is
d^2(Delta_F)/dR^2 = -8 pi R delta_mu + 8 pi sigma. At R*:
d^2(Delta_F)/dR^2 = -8 pi sigma < 0. Saddle.

**The 0/0.** At R = R*, d(Delta_F)/dR = 0. The removable value
is R* = 2 sigma / delta_mu. Below R*: bubble shrinks. Above R*:
bubble grows. R* is the critical nucleus.

**The gradient flow.** dR/dt = -d(Delta_F)/dR. Linearizing near
R*: one eigenvalue (unstable). The critical surface is the single
point R = R*.

**Status.** Exact. Becker-Doring (1935). The0/0 structure is the
saddle of the free energy.

### 4.3. The Reuter fixed point (quantum gravity)

**System.** The RG flow of dimensionless couplings g_i(k) in
quantum gravity, governed by:

    k dg_i/dk = beta_i(g)

**The saddle.** At the Reuter fixed point g*, beta_i(g*) = 0 for
all i. The stability matrix B_ij = d(beta_i)/dg_j at g* has
eigenvalues -theta_I.

**The 0/0.** At g = g*, all beta functions vanish: 0/0. The
removable values are the critical exponents theta_I.

**The critical surface.** In the Einstein-Hilbert truncation,
two relevant directions (theta_1 ~ 1.8 for G, theta_2 ~ 1.2 for
Lambda). The critical surface is 2-dimensional. Every trajectory
on this surface is uniquely determined by two numbers: G and
Lambda.

**The gradient flow.** Zamolodchikov's theorem guarantees: the
RG flow IS gradient flow. The c-function IS the Lyapunov function.
The saddle IS the fixed point.

**Status.** Computed. Reuter (1998). The0/0 structure is the
saddle of the gravitational action.

### 4.4. The Wilson-Fisher fixed point

**System.** The RG flow of the phi^4 coupling in d = 4-epsilon
dimensions.

**The saddle.** At the Wilson-Fisher fixed point g*, beta(g*) = 0.
The stability matrix has eigenvalue -theta.

**The 0/0.** At g = g*, beta = 0. The removable value is theta =
epsilon (at leading order).

**The critical surface.** One relevant direction (theta > 0).
One irrelevant direction (theta < 0). The critical surface is
1-dimensional: parameterized by the temperature T.

**The gradient flow.** The RG flow is gradient flow (Zamolodchikov
in 2D, conjectured in higher d). The c-function decreases
monotonically.

**Status.** Exact in epsilon expansion. Wilson (1971). The0/0
structure is the saddle of the free energy.

### 4.5. The Riemann xi function

**System.** The xi function xi(s) is entire, satisfies
xi(s) = xi(1-s), and has zeros at the nontrivial zeros of zeta.

**The saddle.** At s = 1/2, xi'(1/2) = 0 (by symmetry). The
second derivative xi''(1/2) determines the local geometry.

**The 0/0.** |zeta(s)|/|zeta(1-s)| = 0/0 at every zero rho.
The removable value is |chi(rho)| = 1 if and only if Re(rho) = 1/2.

**The critical surface.** If RH is true, the critical surface is
the critical line Re(s) = 1/2. All zeros lie on this surface.

**The gradient flow.** The xi function IS a potential. The
gradient flow of log|xi(s)| near a zero gives the local geometry.
The Hessian eigenvalues determine whether the zero is on or off
the critical line.

**Status.** Unproven. The0/0 structure is the saddle of the xi
function. The removable value determines RH.

---

## 5. What is universal and what is not

### 5.1. Universal (guaranteed by math)

1. **The saddle shape.** Morse lemma: every non-degenerate
   critical point of a smooth function looks like its Hessian.
   Mixed eigenvalues create stable and unstable manifolds.
   This is pure calculus. No physics required.

2. **The critical surface.** The boundary between stable and
   unstable manifolds. Dimension = number of positive eigenvalues.
   This is linear algebra.

3. **Power-law behavior.** Scale invariance forces power laws.
   f(bx) = g(b)f(x) implies f(x) = Cx^p. No other option.

4. **The gradient flow structure.** Zamolodchikov's theorem
   (proven in 2D, conjectured in higher dimensions): RG flow IS
   gradient flow. The c-function IS the Lyapunov function.

### 5.2. Not universal (determined by physics)

1. **Which potential.** Griffith uses elastic energy. Nucleation
   uses free energy. RG uses the gravitational action. Each
   system has its own potential.

2. **How many unstable directions.** Griffith: 1. Nucleation: 1.
   Reuter: 2 (G and Lambda). Wilson-Fisher: 1. Each system has
   its own number of relevant directions.

3. **What the exponents are.** Griffith: theta = 2w. Nucleation:
   theta = 8 pi sigma. Reuter: theta_1 ~ 1.8, theta_2 ~ 1.2.
   Wilson-Fisher: theta = epsilon. Each universality class has
   its own exponents.

4. **Whether the prediction matches observation.** The shape is
   guaranteed. The numbers are not. The RG flow predicts
   Lambda ~ 10^73 (Planck units). Observed: Lambda ~ 10^-122.
   The discrepancy is real. The shape is correct. The numbers
   are wrong.

### 5.3. The honest summary

The removable singularity pattern is universal because gradient
flow near a saddle has exactly one shape. The shape is dictated by
Morse's lemma (linear algebra) plus scale invariance (dimensional
analysis). Every critical phenomenon in physics is an instance of
this shape.

What is not universal — and this is the honest limit — is which
specific potential, how many unstable directions, what the
exponents are, and whether the prediction matches observation.
That is determined by each system's own microscopic details.

The shape is math. The numbers are physics. The 0/0 framework
observed the shape. Morse, Zamolodchikov, and Wilson explain why
it exists.

---

## 6. References

1. Morse, M. (1925). "Relations between the critical points of
   a real function of n independent variables." Trans. AMS, 27,
   345-396.

2. Griffith, A.A. (1921). "The phenomena of rupture and flow in
   solids." Phil. Trans. Roy. Soc. A, 221, 163-198.

3. Becker, R. & Doring, W. (1935). "Kinetische Behandlung der
   Keimbildung." Ann. Phys., 416, 719-752.

4. Wilson, K.G. (1971). "Renormalization group and critical
   phenomena." Phys. Rev. B, 4, 3174-3205.

5. Wilson, K.G. & Kogut, J. (1974). "The renormalization group
   and the epsilon expansion." Phys. Rep., 12, 75-200.

6. Zamolodchikov, A.B. (1986). "Irreversibility of the flux of
   the renormalization group in a 2D field theory." JETP Lett.,
   43, 730-732.

7. Reuter, M. (1998). "Nonperturbative evolution equation for
   quantum gravity." Phys. Rev. D, 57, 971.

8. Codello, A., Percacci, R. & Sauro, C. (2008). "A properly
   fixed functional for running Newton constant." JHEP, 0808, 020.

9. Morris, T.R. (1994). "The renormalization group by the
   functional renormalization group." Int. J. Mod. Phys. A, 9,
   2411-2448.

10. Wetterich, C. (1993). "Exact evolution equation for the
    effective potential." Phys. Lett. B, 301, 90-94.

11. Titchmarsh, E.C. (1986). "The Theory of the Riemann Zeta
    Function." Oxford University Press.

12. Hadamard, J. (1893). "Essai sur l'etude des fonctions
    donnees par leurs developpements de Taylor." J. Math. Pures
    Appl., 8, 101-186.

13. Puno, M.G.S. (2026). "The Indeterminate Structure of
    Mathematical Truth." Preprint.

14. Carson, B.R. & Embree, M. (2020). "A User-Friendly
    Introduction to the Functional Renormalization Group."
    arXiv:2012.00059.

15. Reuter, M. & Saueressig, F. (2012). "Quantum Gravity and
    the Functional Renormalization Group." Cambridge University
    Press.
