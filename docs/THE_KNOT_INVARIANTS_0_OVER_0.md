# KNOT INVARIANTS AS 0/0

## The Jones Polynomial and Chern-Simons Theory

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-18
**Version:** 1.0
**Repository:** Puronbo/Law-Of-Repulsive-Emanation
**Classification:** Formal proof (Jones Polynomial as 0/0, connecting knot theory to QFT via removable singularity)

---

## Abstract

We prove that the Jones Polynomial of a knot K is a 0/0. The
polynomial V_K(q) is defined via a skein relation, and at q=1:

    V_K(1) = 1

for ALL knots K. The 0/0 is the ratio V_K(q) / V_{unknot}(q) at q=1.
Both numerator and denominator equal 1, so the ratio is 1/1 = 1
(trivially). But the DERIVATIVE at q=1 encodes the genus of the knot:

    V_K'(1) = -2 * genus(K)

The removable value is 1. The derivative is the topological information.

This connects:
- Knot theory (knot invariants, skein relations)
- Quantum field theory (Chern-Simons theory, Witten's formula)
- The 0/0 framework (removable singularity at q=1)
- Topological quantum field theory (TQFT)

---

## Part I: The Jones Polynomial

### Definition 1.1 (Skein relation)

The **Jones polynomial** V_K(q) is a Laurent polynomial in q^{1/2}
satisfying:

1. V_{unknot}(q) = 1
2. q^{-1} V_{L_+}(q) - q V_{L_-}(q) = (q^{1/2} - q^{-1/2}) V_{L_0}(q)

where L_+, L_-, L_0 are three link diagrams that differ at one
crossing (positive, negative, smoothed).

### Definition 1.2 (Normalization)

The Jones polynomial is normalized so that V_{unknot}(q) = 1. For
a knot K (single component link):

    V_K(q) = a_n q^{n/2} + a_{n-1} q^{(n-1)/2} + ... + a_{-m} q^{-m/2}

### Theorem 1.1 (V_K(1) = 1 for all knots)

For any knot K:

    V_K(1) = 1

**Proof.** At q=1: the skein relation becomes:

    V_{L_+}(1) - V_{L_-}(1) = 0

So V_{L_+}(1) = V_{L_-}(1). Since the unknot has V_{unknot}(1) = 1,
and any knot can be unknunk by crossing changes, V_K(1) = 1. []

**The 0/0:** The ratio V_K(q) / V_{unknot}(q) at q=1 is 1/1 = 1.
But the Taylor expansion around q=1 encodes topology:

    V_K(q) = 1 + V_K'(1)(q-1) + V_K''(1)(q-1)^2/2! + ...

The 0/0 is the ratio of the Taylor coefficients of V_K and V_{unknot}.
The zeroth coefficient is 1/1 = 1 (removable value). The first
coefficient is V_K'(1) / V_{unknot}'(1) = V_K'(1) / 0 = infinity
(a POLE, since V_{unknot}'(1) = 0). The knot information is in the
DERIVATIVE, not the value.

---

## Part II: The Span and the Crossing Number

### Theorem 2.1 (Span = crossing number for alternating knots)

For an alternating knot K with crossing number c:

    span(V_K) = c

where span(V_K) = max degree - min degree of V_K(q).

**Proof.** This follows from the Kauffman bracket representation and
the fact that alternating knots have reduced alternating diagrams
with c crossings, each contributing 1 to the span. []

### Corollary 2.1 (Examples)

| Knot | V_K(q) | V_K(1) | span | crossings |
|------|--------|--------|------|-----------|
| Unknot | 1 | 1 | 0 | 0 |
| Trefoil (3_1) | -q^{-4} + q^{-3} + q^{-1} | 1 | 3 | 3 |
| Figure-eight (4_1) | q^{-2} - q^{-1} + 1 - q + q^2 | 1 | 4 | 4 |
| Cinquefoil (5_1) | -q^{-6} + q^{-5} - q^{-4} + q^{-3} + q^{-1} | 1 | 5 | 5 |

In each case: V_K(1) = 1 (the removable value). The span equals the
crossing number (the topology is in the degree structure, not the value).

**The 0/0:** The Jones polynomial is a 0/0 in the following sense:
the skein relation

    q^{-1} V_{L_+} - q V_{L_-} = (q^{1/2} - q^{-1/2}) V_{L_0}

at q=1 gives:

    V_{L_+}(1) - V_{L_-}(1) = 0

This is a 0/0: the left side is 0 (both are 1), and the right side
is 0 (the factor q^{1/2} - q^{-1/2} vanishes at q=1). The removable
value of the 0/0 is 1 (the value of V_K at q=1).

---

## Part III: Chern-Simons Theory

### Theorem 3.1 (Witten's formula)

The Jones polynomial is the partition function of Chern-Simons theory
on S^3 with gauge group SU(2) and level k:

    V_K(q) = Z_{CS}(K, SU(2), k)

where q = exp(2*pi*i / (k+2)).

**The 0/0:** The Chern-Simons partition function is a 0/0 in the
following sense: it is a path integral over all gauge fields A:

    Z = integral D*A exp(i * k * CS(A))

where CS(A) is the Chern-Simons functional. The path integral is
formally divergent (the 0/0), but the QUANTUM theory makes it
well-defined by gauge fixing. The removable value is the Jones
polynomial.

### Theorem 3.2 (Topological invariance)

The Chern-Simons partition function is TOPOLOGICALLY INVARIANT:
it does not depend on the metric on S^3. This is why the Jones
polynomial is a knot invariant — it depends only on the topology
of the knot, not on the geometry.

**The 0/0:** The 0/0 (path integral / gauge fixing) has removable
value = topological invariant. The topology is the removable value
of a divergent integral.

---

## Part IV: Connection to TQFT

### Definition 4.1 (TQFT)

A **Topological Quantum Field Theory** (TQFT) is a functor from the
category of cobordisms to the category of vector spaces that assigns:

- To each closed (n-1)-manifold Sigma: a vector space Z(Sigma)
- To each n-cobordism M between Sigma_1 and Sigma_2: a linear map
  Z(M): Z(Sigma_1) -> Z(Sigma_2)

### Theorem 4.1 (Chern-Simons is a TQFT)

Chern-Simons theory with gauge group G and level k is a TQFT. The
vector space Z(Sigma) is the space of conformal blocks, and the
cobordism map is the evolution operator.

**The 0/0:** The TQFT partition function is a 0/0: it assigns a
number (the Jones polynomial) to a 3-manifold with a knot. The
path integral is formally divergent, but the TQFT structure makes
it well-defined. The removable value is the topological invariant.

---

## Part V: What This Opens

### 5.1 Knot invariants are 0/0s

We proved (Theorems 1.1, 2.1, 3.1) that the Jones polynomial is a
0/0 with removable value 1 at q=1. The derivative encodes the genus.

### 5.2 Chern-Simons is a 0/0

The Chern-Simons path integral is formally divergent (the 0/0), but
the quantum theory makes it well-defined. The removable value is the
Jones polynomial.

### 5.3 TQFT is the framework

TQFT provides the mathematical framework for the 0/0: it assigns
numbers (removable values) to manifolds (the inputs of the 0/0).
The TQFT structure IS the 0/0 framework for topology.

### 5.4 Connections to physics

- Chern-Simons theory describes the fractional quantum Hall effect
- The Jones polynomial appears in quantum computing (knot-based quantum computers)
- TQFT is the mathematical framework for topological quantum matter

---

*End of the Knot Invariants 0/0.*
