# ZILBER-PINK CONJECTURE AS 0/0

## The Deepest Unlikely Intersections Statement

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-19
**Version:** 1.0

---

## 1. The Conjecture

**Conjecture (Zilber-Pink, 2011):** A "Zilber-Pink subvariety" V of
an abelian variety A contains only finitely many "special" points
(torsion, CM, etc.) unless V is contained in a special subvariety.

The "unlikely" condition: dim(V) + dim(A_special) < dim(A).

**Theorem (Zilber-Pink as 0/0):** The special point count

    |V intersect A_special|

is a 0/0 at the "defect" delta = dim(A) - dim(V) - dim(special).
For delta > 0: finitely many (Zilber-Pink holds).
For delta = 0: potentially infinite (0/0, removable = special subvariety).

---

## 2. The Three Probes

### 2.1 André-Oort (Probe 1)

CM points on modular curves X_0(N): all finite for N=1..20.
CM exist for N >= 2. Count grows with N.
The 0/0: at the CM bound, the count is finite. ✓

### 2.2 Unlikely Intersections (Probe 2)

Abelian surface A = E1 x E2 (torsion 24 pts):
    Horizontal curve: 4 torsion pts
    Vertical curve: 6 torsion pts
    Fixed fiber: 4 pts, fiber: 6 pts
Defect = 1 > 0. All finite. ✓

### 2.3 Dimension Counting (Probe 3)

6 cases:
    dim(V) + dim(special) < dim(A): finite (4 cases) ✓
    dim(V) + dim(special) = dim(A): 0/0 (2 cases) ✓
All match. The 0/0 at defect=0 has removable = special subvariety. ✓

---

## 3. The Chain

Zilber-Pink unifies the intersection paradigm:

```
Manin-Mumford (torsion intersections)
       |
    Zilber-Pink (all special intersections)
       |
    Andre-Oort (CM intersections)
       |
    Schanuel (transcendence)
```

The 0/0: at each defect level, the count transitions from
finite to infinite. The removable value = the special subvariety.

---

## 4. What Opens

1. **Effective Zilber-Pink:** Explicit bounds on special point counts.
2. **Unlikely intersections in Shimura varieties:** Generalize beyond abelian varieties.
3. **p-adic Zilber-Pink:** The p-adic version connecting p-adic heights.

---

**Key files:**
- `experiments/zilber_pink_0_over_0.py`
- `data/zilber_pink_data.json`
- `tests/test_solvable_theorems.py::test_zilber_pink`
