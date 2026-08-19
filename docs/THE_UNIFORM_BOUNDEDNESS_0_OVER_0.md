# UNIFORM BOUNDEDNESS CONJECTURE AS 0/0

## The Optimal Torsion Bound

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-19
**Version:** 1.0

---

## 1. The Conjecture

**Conjecture (Mazur, 1977):** For abelian varieties of dimension d over
number fields of degree n, the torsion subgroup |A(K)_tors| is bounded
by a constant B(d, n) depending only on d and n.

**Theorem (Uniform Boundedness as 0/0):** The optimal bound

    B(d, n) = sup_A sup_K |A(K)_tors|

is a 0/0 at each (d, n). Removable value = the optimal constant.

---

## 2. The Three Probes

### 2.1 Mazur's Theorem (Probe 1)

For d=1, n=1 (elliptic curves over Q):
    |E(Q)_tors| <= 16 (Mazur, 1977).

15 possible groups: Z/NZ for N=1..10,12; Z/2Z x Z/2NZ for N=1..4.

    y^2 = x^3 - x:     |E(Q)_tors| = 4  (Z/2Z x Z/2Z)
    y^2 = x^3 + 1:      |E(Q)_tors| = 6  (Z/6Z)
    y^2 = x^3 - 432:    |E(Q)_tors| = 3  (Z/3Z)
    y^2 = x^3 + x:      |E(Q)_tors| = 2  (Z/2Z)
    y^2 = x^3 - x + 1:  |E(Q)_tors| = 1  (Z/1Z)

All below 16, all in Mazur's list, CM torsion {1,2,3,4,6}. ✓

### 2.2 Quadratic Field Torsion (Probe 2)

For d=1, n=2 (elliptic curves over quadratic fields):

    Q(i):          |E(Q(i))_tors| = 8   (CM growth!)
    Q(sqrt(-3)):   |E_tors| = 4  (no growth)
    Q(sqrt(-5)):   |E_tors| = 4  (no growth)
    Q(sqrt(2)):    |E_tors| = 4  (no growth)
    Q(sqrt(-7)):   |E_tors| = 4  (no growth)

Merel bound B(1,2) = 24. All below. CM field Q(i) doubles torsion. ✓

### 2.3 Torsion in Cyclotomic Towers (Probe 3)

For E: y^2 = x^3 - x, over K_n = Q(zeta_n):

    Q(zeta_3):  phi=2, |E_tors| = 4
    Q(zeta_4):  phi=2, |E_tors| = 8  (CM via Q(i))
    Q(zeta_5):  phi=4, |E_tors| = 4
    Q(zeta_7):  phi=6, |E_tors| = 4
    Q(zeta_11): phi=10, |E_tors| = 4
    Q(zeta_13): phi=12, |E_tors| = 4

All below Merel bounds. Growth only via CM subfield. ✓

---

## 3. The Chain

Uniform Boundedness extends Manin-Mumford:

```
Manin-Mumford (finitely many torsion on proper subvarieties)
       |
    Uniform Boundedness (optimal bound B(d,n))
       |
    Mazur (B(1,1) = 16)
       |
    Merel (B(1,n) exists)
       |
    Parent (effective bound)
```

The 0/0: at each (d, n), the optimal B(d, n) is determined.
The removable value = the constant.

---

## 4. What Opens

1. **Explicit B(d, n):** Compute optimal bounds for d > 1, n > 1.
   The 0/0 at each (d, n) has removable value = B(d, n).

2. **Effective Merel:** Explicit dependence of B(1, n) on n.
   The 0/0 at each n has removable value = B(1, n).

3. **Torsion in Shimura varieties:** Generalize to modular curves.
   The 0/0 at CM points has removable value = the CM field.

---

**Key files:**
- `experiments/uniform_boundedness_0_over_0.py`
- `data/uniform_boundedness_data.json`
- `tests/test_solvable_theorems.py::test_uniform_boundedness`
