# MANIN-MUMFORD CONJECTURE AS 0/0

## Torsion Intersections on Abelian Varieties

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-19
**Version:** 1.0

---

## 1. The Conjecture

**Conjecture (Manin-Mumford, 1961; proved by Raynaud, 1983):**
A closed subvariety V of an abelian variety A contains a dense set of
torsion points if and only if V is a translation of an abelian subvariety.

**Theorem (Manin-Mumford as 0/0):** The torsion count

    |V intersect A_tors|

is a 0/0 at the "bound" where V is a proper subvariety.
Removable value = 0 (finitely many torsion points on proper subvarieties).

---

## 2. The Three Probes

### 2.1 Torsion Subgroups (Probe 1)

For elliptic curves over Q, Mazur's theorem: |E(Q)_tors| <= 16.

    y^2 = x^3 - x:     |E(Q)_tors| = 4 (Z/4Z)
    y^2 = x^3 + 1:      |E(Q)_tors| = 6 (Z/6Z)
    y^2 = x^3 - 432:    |E(Q)_tors| = 3 (Z/3Z)
    y^2 = x^3 + x:      |E(Q)_tors| = 2 (Z/2Z)
    y^2 = x^3 - x + 1:  |E(Q)_tors| = 1 (trivial)

All finite, all below Mazur bound. CM torsion: 1,2,3,4,6 only. ✓

### 2.2 Height of Torsion (Probe 2)

Torsion points: h_NT(P) = 0 (Neron-Tate height).
Identity: h(O) = 0 (0/0 removable value = regulator).
All rank 0 curves: all rational points are torsion. ✓

### 2.3 Raynaud's Theorem (Probe 3)

Abelian surface A = E1 x E2 (product of CM elliptic curves):
    A_tors = E1_tors x E2_tors = 4 x 6 = 24 points.

Horizontal curve C = E1 x {O}: |C intersect A_tors| = 4.
Vertical curve C = {O} x E2: |C intersect A_tors| = 6.
All finite, all < 24 (total product torsion). ✓

---

## 3. The Chain

Manin-Mumford completes the torsion chain:

```
Vojta (height bounds)
       |
    Manin-Mumford (torsion intersections)
       |
    Raynaud (proof via Faltings)
       |
    Faltings (finitely many points)
       |
    Mordell (finitely generated)
```

The 0/0: at the "bound" where V = A (the whole abelian variety),
the torsion intersection is A_tors (infinite for A over Q-bar).
For proper V: finite (removable = 0).

---

## 4. What Opens

1. **Uniform Boundedness Conjecture:** |E(K)_tors| bounded by a
   function of [K:Q] only. The 0/0 at the bound has removable
   value = the optimal constant.

2. **Zilber-Pink Conjecture:** unlikely intersections (not Manin-Mumford
   or André-Oort) are Zariski-closed. The 0/0 at each unlikely
   intersection has removable value.

3. **Oort's Conjecture:** special subvarieties of Shimura varieties
   are determined by their torsion. The 0/0 at CM points has
   removable value = the CM field.

---

**Key files:**
- `experiments/manin_mumford_0_over_0.py`
- `data/manin_mumford_data.json`
- `tests/test_solvable_theorems.py::test_manin_mumford`
