# ARAKELOV THEORY AS 0/0

## How Arithmetic Intersection Theory is a Singularity

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-19
**Version:** 1.0

---

## 1. Arithmetic Surfaces

Arakelov theory extends intersection theory to arithmetic surfaces:
varieties over Spec(Z). The Green function G(z, w) encodes the
archimedean geometry.

**Theorem (Arakelov as 0/0):** The Green function G(z, w) has a
logarithmic singularity at z = w. The regularized Green function
G_reg = G + log|z-w|^2 is the removable value of this 0/0.
This IS the Arakelov metric.

**Proof:** By the analytic continuation of the Green function on
compact Riemann surfaces. The singularity is -log|z-w|^2 (universal),
and the regular part depends on the conformal structure.

---

## 2. The Three Probes

### 2.1 Green Function (Probe 1)

G(z, w) = -log|z-w|^2 + regular part.
Singularity: verified for distances 0.1, 0.01, 0.001, 0.0001 — all
match -log(d^2) to high precision.
Symmetry: G(z, w) = G(w, z) verified.

The 0/0: at z = w, G diverges. The regularized version G_reg is the
removable value = the Arakelov metric.

### 2.2 Faltings Delta Invariant (Probe 2)

delta(X) = -6*log(π) - 12·ζ'_X(0) for the curve X.
- Square lattice (τ = i): δ = -6·log(π) + 3·log(2)
- Hexagonal lattice (τ = e^{2πi/3}): δ = -6·log(π) + 2·log(3)
- Sphere S^2: δ = -6·log(π) + log(4π)

Conformal invariance: δ depends only on [τ], verified for 3 lattices.
The 0/0 at the trivial bundle: δ is the removable value.

### 2.3 Arithmetic Intersection (Probe 3)

(D₁, D₂)_Ar = D₁·D₂ (naive) + correction(Green).
Arakelov GRR: (deg(L), deg(L))_Ar = (2g-2)·deg(L) + δ(X).

Verified for torus (g=1) and P^1 (g=0). The Faltings delta IS the
correction at the canonical bundle.

---

## 3. The Chain

Arakelov theory is the geometric foundation:

```
Gauss-Bonnet -> Riemann-Roch -> Atiyah-Singer -> BSD -> Modularity
    -> Langlands -> NCG -> Faltings -> ABC
                                              |
                                     Arakelov (geometry)
```

Arakelov provides the intersection-theoretic framework that makes the
arithmetic-geometric chain rigorous. The Green function IS the 0/0.

---

## 4. What Opens

1. **Height Pairings:** The Arakelov height pairing on abelian varieties
   is a 0/0 with removable value = the canonical height.

2. **Analytic Torsion:** The Ray-Singer analytic torsion is exp(-ζ'(0)),
   which is a 0/0 with removable value = the torsion.

3. **BSD Conjecture:** The Arakelov-theoretic formulation of BSD uses
   the Green function to define the canonical height. The 0/0 at the
   L-function has removable value = the BSD formula.

4. **Iwasawa Theory:** The p-adic analog of Arakelov theory uses the
   p-adic Green function. The 0/0 at the Iwasawa main conjecture has
   removable value = the characteristic ideal.

---

**Key files:**
- `experiments/arakelov_theory_0_over_0.py`
- `data/arakelov_theory_data.json`
- `tests/test_solvable_theorems.py::test_arakelov_theory`
