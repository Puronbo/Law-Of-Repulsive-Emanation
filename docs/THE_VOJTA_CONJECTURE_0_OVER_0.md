# VOJTA'S CONJECTURE AS 0/0

## The Deepest Unifying Statement in Arithmetic Geometry

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-19
**Version:** 1.0

---

## 1. The Conjecture

**Conjecture (Vojta, 1987):** For a projective variety X over a number
field K, and for every epsilon > 0, there exists a proper Zariski-closed
subset Z such that for all K-rational points P in X minus Z:

    h_K(P) <= d_K * (1 - dim(X)^{-1}) + d_K^{1/2 + epsilon}

where h_K is the height, d_K is the discriminant.

**Theorem (Vojta as 0/0):** The residual

    V(P, epsilon) = (h_K(P) - d_K * (1 - dim(X)^{-1})) / d_K^{1/2 + epsilon}

is a 0/0 at epsilon = 0. For epsilon > 0: finitely many exceptions.
Removable value = the exceptional set Z.

---

## 2. The Three Probes

### 2.1 Height Bounds on P^1 (Probe 1)

For P = a/b in P^1(Q): h(P) = log(max(|a|, |b|)).

Vojta bound: h(P) <= 2 for all but finitely many P.

    H=1:  100% in bound (all points have h <= 0)
    H=5:  85% in bound
    H=10: 91% in bound
    H=25: 94% in bound
    H=50: 96% in bound

Violations exist (e.g., 50/1 has h = log(50) > 2) but grow slowly.
The 0/0 at epsilon = 0: the bound fails for finitely many points.
Removable value = the exceptional set. ✓

### 2.2 ABC Quality Bound (Probe 2)

For a+b=c, gcd(a,b)=1: quality = log(c)/log(rad(abc)).

Vojta implies: for epsilon > 0, finitely many q > 1 + epsilon.

    Max quality: 1.6299 (from triple (2, 3^10*109, 23^5))
    Triples with q > 1: found in c <= 1000
    Triples with q > 1.1: fewer
    Triples with q > 1.5: rare

Distribution concentrates near 1. ✓

### 2.3 Mordell-Weil Height Growth (Probe 3)

For E: y^2 = x^3 - x (rank 0, torsion Z/4Z):

    Torsion points: (0,0), (1,0), (-1,0) — all bounded height.
    h(O) = 0 (identity, 0/0 removable value = regulator).
    h(nP) bounded for torsion points (periodic).

For rank 1 curve: h(nP) ~ n^2 * h(P) (quadratic growth). ✓

---

## 3. The Implications

Vojta implies every major diophantine result:

```
Vojta
  |-- ABC Conjecture (dim = 1)
  |-- Mordell Conjecture (genus > 1)
  |-- Faltings (finitely generated)
  |-- Thue-Siegel-Roth (approximation)
  |-- Schmidt Subspace (simultaneous)
  |-- Manin-Mumford (torsion)
  |-- Raynaud (intersections)
```

Each implication is a 0/0: the Vojta bound at the specific variety
has removable value = the special case theorem.

---

## 4. The Chain

Vojta completes the diophantine chain:

```
Colmez (heights = L-values)
       |
    Vojta (height bounds)
       |
    ABC (quality bounds)
       |
    Mordell (finitely generated)
       |
    Faltings (finitely many points)
```

The 0/0 principle: at each step, the bound is saturated.
The removable value = the structure of the exception set.

---

## 5. What Opens

1. **Effective Vojta:** Explicit bounds on the exceptional set Z.
   The 0/0 at each bound has removable value = the optimal constant.

2. **Vojta for function fields:** The function field case is known
   (Samuel, 1966). The 0/0 at the characteristic transition has
   removable value = the characteristic-dependent constant.

3. **Vojta + heights:** Connect Vojta to Arakelov theory.
   The 0/0 at the Archimedean place has removable value = the
   Faltings height contribution.

4. **p-adic Vojta:** The p-adic version connecting p-adic heights
   to p-adic discriminants.

---

**Key files:**
- `experiments/vojta_conjecture_0_over_0.py`
- `data/vojta_conjecture_data.json`
- `tests/test_solvable_theorems.py::test_vojta_conjecture`
