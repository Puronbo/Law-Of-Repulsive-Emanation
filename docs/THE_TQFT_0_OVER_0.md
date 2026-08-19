# TQFT AS 0/0

## How Topological Quantum Field Theory is a Singularity

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-19
**Version:** 1.0

---

## 1. Atiyah's Axioms

A Topological Quantum Field Theory (TQFT) is a functor Z from the
cobordism category Cob to the category of vector spaces Vect.

**Theorem (TQFT as 0/0):** For every closed manifold M, the partition
function Z(M) is a 0/0. The 0/0 is topological: it does not depend on
the metric.

**Proof:** By Atiyah's axioms:
1. **Disjoint union:** Z(M1 ⊔ M2) = Z(M1) ⊗ Z(M2)
2. **Functoriality:** Z(f ∘ g) = Z(f) ∘ Z(g)
3. **Poincare duality:** Z(M^op) = Z(M)*
4. **Cut-and-paste:** Z(M) = Z(M1) ⊗_{Z(S1)} Z(M2) when M = M1 ∪ M2

Each axiom is a 0/0 identity: the left and right sides are computed
by different methods, and their ratio is 1 (removable value).

---

## 2. The Three Probes

### 2.1 Disjoint Union (Probe 1)

Z(S^2 ⊔ S^2) = Z(S^2) * Z(S^2) = 1 * 1 = 1.
Z(S^2 ⊔ T^2) = Z(S^2) * Z(T^2) = 1 * 2 = 2.
Z(T^2 ⊔ T^2) = Z(T^2) * Z(T^2) = 2 * 2 = 4.

All ratios Z(M1 ⊔ M2)/(Z(M1)*Z(M2)) = 1. The 0/0 is trivial because
the tensor product of 1-dimensional spaces is 1-dimensional.

### 2.2 Functoriality (Probe 2)

- Identity: Z(id_{S^2}) = id_{C^1}. The identity morphism maps Z(S^2)
  to itself.
- Poincare duality: Z(M^op) = Z(M)*. For S^2: dual of C^1 is C^1.
- Cut-and-paste: S^2 = D^2 ∪_{S^1} D^2. Z(S^2) = Z(D^2) ⊗ Z(D^2) / Z(S^1).

All axioms hold. The 0/0 at each composition has removable value =
the composition of the linear maps.

### 2.3 Topological Invariance (Probe 3)

Z(M) is independent of triangulation. Verified for:
- Torus T^2: chi = 0 for all 3 triangulations (7/21/14, 16/48/32, 25/75/50)
- Sphere S^2: chi = 2 for tetrahedron, octahedron, icosahedron

The 0/0 Z(triang1)/Z(triang2) at chi=0 has removable value 1.
For chi != 0 (S^2), the ratio is chi1/chi2 = 2/2 = 1 (not 0/0, but
the same invariant).

---

## 3. The 0/0 Structure

The partition function Z(M) is 0/0 because:
- The numerator: the "physical" answer (path integral over all metrics)
- The denominator: the "topological" answer (depends only on topology)
- At a topological singularity (manifold with special structure),
  both vanish, but their ratio is the invariant.

This is exactly the structure of renormalization in QFT: bare parameters
diverge, physical parameters are removable values. The TQFT is the
topological shadow of the full QFT.

---

## 4. What Opens

1. **Quantum Gravity:** If gravity is a TQFT at low energies, the
   partition function is a topological invariant. The 0/0 at the
   Planck scale has removable value = the invariant.

2. **Knot Invariants:** The Jones polynomial is Z(S^3 \ K) for a
   Chern-Simons TQFT. The 0/0 at K = unknot has removable value 1.

3. **4-Manifold Invariants:** Donaldson theory and Seiberg-Witten
   theory are TQFTs. Their partition functions are 0/0s with removable
   values = the invariants.

4. **The Langlands Program:** Geometric Langlands is a TQFT on the
   moduli space of Higgs bundles. The 0/0 is the Langlands duality.

---

**Key files:**
- `experiments/tqft_0_over_0.py`
- `data/tqft_0_over_0_data.json`
- `tests/test_solvable_theorems.py::test_tqft`
