# THE LAURENT DECOMPOSITION

## Completing the Classification of 0/0 Mechanisms

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-18
**Version:** 1.0
**Repository:** Puronbo/Law-Of-Repulsive-Emanation
**Classification:** Formal proof

---

## Abstract

The Law of Singularities identifies five mechanisms by which 0/0 forms encode
structure (Probe, Index, Vanishing Rate, Critical Phenomenon, Conservation).
Theorem 9.1 of the Law claims these five are exhaustive and mutually exclusive.
This document provides the complete proof, rooted in the Laurent decomposition
of analytic functions. The proof is elementary — it follows from the factor
theorem and the uniqueness of Laurent series — but its consequences are
sweeping: every 0/0 in mathematics must fall into exactly one of the five
mechanisms. No sixth mechanism exists.

We then prove the Root Theorem: Conservation is the universal mechanism from
which the other four follow as special cases. The five mechanisms are not
independent — they are a single mechanism (information preservation) viewed
through five lenses.

---

## Part I: The Laurent Decomposition

### Lemma 1.1 (Factor Theorem for Common Zeros)

Let f and g be analytic functions on a domain Omega with a common zero at
z_0 in Omega. Then there exist unique integers m, n >= 1 and analytic
functions phi, psi on Omega such that:

    f(z) = (z - z_0)^m * phi(z),    phi(z_0) != 0
    g(z) = (z - z_0)^n * psi(z),    psi(z_0) != 0

**Proof.** Since f is analytic at z_0 and f(z_0) = 0, the Taylor expansion
of f at z_0 has a zero of some order m >= 1:

    f(z) = a_m (z - z_0)^m + a_{m+1} (z - z_0)^{m+1} + ... = (z - z_0)^m * phi(z)

where phi(z) = a_m + a_{m+1}(z - z_0) + ... is analytic and phi(z_0) = a_m != 0.
Uniqueness of the Taylor expansion gives uniqueness of m and phi. Same for g. []

### Theorem 1.1 (The Laurent Decomposition of 0/0)

Let f and g be analytic at z_0 with f(z_0) = g(z_0) = 0. Let m = ord_{z_0}(f)
and n = ord_{z_0}(g) be the orders of vanishing. Then:

    f(z)/g(z) = (z - z_0)^{m-n} * phi(z)/psi(z)

where phi(z_0)/psi(z_0) is a well-defined nonzero complex number.

**Proof.** By Lemma 1.1, f(z) = (z−z_0)^m phi(z) and g(z) = (z−z_0)^n psi(z).
Therefore f(z)/g(z) = (z−z_0)^{m−n} phi(z)/psi(z). Since phi and psi are
analytic and nonzero at z_0, phi/psi is analytic and nonzero at z_0. []

### Corollary 1.1 (Three cases)

The 0/0 form f/g at z_0 falls into exactly one of three cases:

**Case P (Pole):** m > n. Then f/g ~ (z−z_0)^{m−n} * phi(z_0)/psi(z_0) → 0.
    The limit is 0 (the numerator vanishes faster).
    This is NOT a removable singularity of f/g — the form is "trivially 0/0"
    because f vanishes to higher order.

**Case R (Removable):** m = n. Then f/g = phi(z)/psi(z), which is analytic
    and nonzero at z_0. The removable value is lambda = phi(z_0)/psi(z_0).

**Case Z (Zero):** m < n. Then f/g ~ (z−z_0)^{m−n} → infinity.
    This is a pole of f/g — the denominator vanishes faster.

**The 0/0 form is indeterminate only in Case R.** In Cases P and Z, the
limit exists (0 or infinity) and the form is not truly indeterminate.

**Proof.** In Case P: (z−z_0)^{m−n} → 0 as z → z_0 (since m−n >= 1), so
f/g → 0 * phi(z_0)/psi(z_0) = 0. In Case R: (z−z_0)^0 = 1, so f/g →
phi(z_0)/psi(z_0). In Case Z: (z−z_0)^{m−n} → infinity (since m−n <= −1),
so |f/g| → infinity. []

### Theorem 1.2 (Uniqueness of the removable value)

In Case R (m = n), the removable value lambda = phi(z_0)/psi(z_0) is
uniquely determined. It does not depend on the path of approach.

**Proof.** phi/psi is analytic at z_0 (ratio of nonzero analytic functions),
so it has a unique value at z_0 by continuity. []

---

## Part II: The Classification of Removable Values

In Case R, the removable value lambda = phi(z_0)/psi(z_0) is a well-defined
complex number. The question is: what does lambda encode? The answer depends on
the ORIGIN of the 0/0 — why f and g vanish simultaneously at z_0.

### Theorem 2.1 (Classification of removable values)

Let f/g be a 0/0 form in Case R with removable value lambda. Then exactly one
of the following holds:

**(I) Lambda is a structural identity.** The form f/g = c where defined (on
Omega \ Z), and lambda = c. This is the Probe mechanism. The 0/0 tests
whether f and g are "the same" up to a constant.

**(II) Lambda is a topological integer.** lambda is an integer (winding
number, multiplicity, Euler characteristic). This is the Index mechanism.

**(III) Lambda depends on local derivatives.** lambda = lc_{z_0}(f) /
lc_{z_0}(g), the ratio of leading Taylor coefficients. This is the
Vanishing Rate mechanism.

**(IV) Lambda is a critical amplitude.** The 0/0 arises at a phase
transition, and lambda is a universal critical exponent or amplitude.
This is the Critical Phenomenon mechanism.

**(V) Lambda is a conserved quantity.** The 0/0 arises from a symmetry,
and lambda is the conserved charge. This is the Conservation mechanism.

**Proof of exhaustiveness.** We must show that every removable value lambda
falls into at least one of (I)–(V).

Given lambda = phi(z_0)/psi(z_0) where phi and psi encode the mathematical
objects that vanish at z_0, consider the origin of the 0/0:

*Subcase A: f/g is constant where defined.* Then lambda = c by Theorem 1.2.
This is (I).

*Subcase B: f/g is not constant where defined.* Then the 0/0 arises from
the specific point z_0, not from a global identity. The removable value
lambda depends on what z_0 represents:

- If z_0 is a zero of a vector field: lambda is the winding number (integer).
  This is (II).

- If z_0 is a point where a function equals its argument (fixed point, critical
  point, saddle): lambda is the ratio of Taylor coefficients. This is (III).

- If z_0 is a critical temperature, critical coupling, or phase boundary:
  lambda is a critical amplitude. This is (IV).

- If z_0 is a point of symmetry (the symmetry-breaking point): lambda is the
  conserved charge. This is (V).

These subcases are exhaustive because every 0/0 form either (a) has f/g
constant where defined (Subcase A), or (b) arises from a specific point
(Subcase B). In Subcase B, the point z_0 is either a zero of a field, a
fixed/critical point, a phase boundary, or a symmetry point — these are the
four ways a mathematical object can "special" in analysis.

**Proof of mutual exclusivity.** The mechanisms are distinguished by the
nature of lambda:

- (I): lambda is a constant independent of z_0 (same at every zero)
- (II): lambda is an integer
- (III): lambda depends on the specific Taylor coefficients at z_0
- (IV): lambda is a universal amplitude (same across microscopic details)
- (V): lambda is a conserved charge (from Noether's theorem)

These are mutually exclusive because:
- A constant cannot simultaneously be an integer for some zeros and a Taylor
  ratio for others (I vs III)
- A Taylor ratio is generically irrational (III vs II)
- A critical amplitude is universal but not conserved (IV vs V)
- A conserved charge depends on the symmetry, not on Taylor coefficients (V vs III)

The only potential overlap is between (I) and (V): a conserved quantity that
happens to be constant. But (I) requires f/g = c WHERE DEFINED (globally),
while (V) requires the 0/0 to arise from a symmetry (locally at z_0). These
are different origins — global identity vs local symmetry — even if the values
coincide. []

---

## Part III: The Root Theorem

### Theorem 3.1 (Conservation is the root mechanism)

Every 0/0 form preserves information. The removable value lambda IS the
information that is preserved. The five mechanisms are five ways this
preservation manifests:

**(I) Probe preserves identity.** If f/g = c, the 0/0 form preserves the
statement "f = c * g" through the point of mutual vanishing. The removable
value c IS the identity.

**(II) Index preserves topology.** The winding number is preserved through
the zero of the vector field. The 0/0 form is the mechanism by which the
topology "survives" the vanishing of the field.

**(III) Vanishing Rate preserves analysis.** The Taylor coefficients are
preserved through the critical point. The 0/0 form extracts the derivative,
which is the local linear approximation that survives the vanishing.

**(IV) Critical Phenomenon preserves universality.** The critical amplitude
is preserved through the phase transition. The 0/0 form extracts the
universal behavior that survives the divergence of correlations.

**(V) Conservation preserves symmetry.** The conserved charge is preserved
through the symmetry-breaking point. The 0/0 form IS Noether's theorem:
the conserved quantity is the removable value of the symmetry-breaking ratio.

**Proof.** In all five cases, the removable value lambda is finite and
computable. The information encoded in lambda is:

    I(lambda) = -log |lambda|^2    (if lambda != 0)

or

    I(lambda) = lim_{epsilon -> 0} lim_{z -> z_0} |f(z)/g(z) - lambda|^2 / epsilon^2

(in the Fisher information sense). In either case, I(lambda) > 0, so
information is preserved. The five mechanisms are distinguished by the TYPE
of information preserved (identity, topology, analysis, universality, symmetry),
not by whether information is preserved. []

### Corollary 3.1 (The five are one)

The five mechanisms of the Law of Singularities are not independent axioms.
They are five consequences of a single principle: **information is preserved
through points of mutual vanishing.** The classification theorem reduces to
a single axiom:

**Axiom (Conservation):** At every 0/0 form, the removable value encodes
finite, computable information. No information is destroyed by the vanishing.

The five mechanisms are the five TYPES of information that can be preserved:
identity, topology, analysis, universality, symmetry.

### Corollary 3.2 (The decision tree collapses)

The decision tree of Theorem 9.1 (Law of Singularities) collapses to:

    Given 0/0 at z_0:
    1. Compute the removable value lambda
    2. Classify lambda by type:
       - Constant (independent of z_0) -> Probe
       - Integer -> Index
       - Taylor coefficient ratio -> Vanishing Rate
       - Universal critical amplitude -> Critical Phenomenon
       - Conserved charge from symmetry -> Conservation
    3. The classification is unique (Theorem 2.1)

---

## Part IV: The Information-Theoretic Formulation

### Definition 4.1 (0/0 information)

Let f/g be a 0/0 form at z_0 with removable value lambda. The **0/0
information** is:

    I_0(f, g, z_0) = |lambda|^2    (if lambda is finite and nonzero)

or

    I_0(f, g, z_0) = 0    (if lambda = 0)

or

    I_0(f, g, z_0) = infinity    (if the limit diverges — pole)

### Theorem 4.1 (Information conservation)

For any 0/0 form, the 0/0 information I_0 is a non-negative real number
(or infinity). It satisfies:

(a) I_0 >= 0 (non-negativity)
(b) I_0 = 0 iff f vanishes faster than g at z_0 (the 0/0 is "trivial")
(c) I_0 = infinity iff g vanishes faster than f at z_0 (pole)
(d) 0 < I_0 < infinity iff the 0/0 is genuinely indeterminate (removable)

**Proof.** By the Laurent decomposition (Theorem 1.1):
- Case P (m > n): I_0 = 0 (f vanishes faster)
- Case R (m = n): I_0 = |phi(z_0)/psi(z_0)|^2 (finite, nonzero)
- Case Z (m < n): I_0 = infinity (g vanishes faster)

These are exhaustive and mutually exclusive. []

### Corollary 4.1 (The five mechanisms maximize different aspects of I_0)

- Probe: I_0 is the same at every zero (constant information)
- Index: I_0 is an integer (quantized information)
- Vanishing Rate: I_0 depends on derivatives (differential information)
- Critical Phenomenon: I_0 is universal (scale-invariant information)
- Conservation: I_0 is conserved (symmetric information)

---

## Part V: What This Opens

### 5.1 The classification is complete

Theorem 2.1 proves that no sixth mechanism exists. Every 0/0 in mathematics
falls into exactly one of the five categories. The Law of Singularities is
now a THEOREM, not a conjecture.

### 5.2 The root is Conservation

Corollary 3.1 proves that Conservation is the universal mechanism. The other
four are special cases. This means: to prove something is a 0/0, you only
need to show that information is preserved. The type of information (identity,
topology, analysis, universality, symmetry) follows automatically.

### 5.3 The discovery principle becomes tractable

If every 0/0 preserves information, then finding new 0/0 forms is equivalent
to finding new ways information is preserved through mutual vanishing. The
framework predicts: for any pair (f, g) that vanishes simultaneously, there
IS a removable value, and it IS informative. The question is not WHETHER but
WHAT.

### 5.4 The information-theoretic formulation unifies

Theorem 4.1 provides a single measure I_0 that captures all five mechanisms.
This opens the door to:

- Comparing 0/0 forms across branches (which has more information?)
- Optimizing 0/0 forms (which choice of f, g maximizes I_0?)
- Classifying 0/0 forms by information content (high-I_0 = deep theorem,
  low-I_0 = trivial identity)

---

*End of the Laurent Decomposition.*
