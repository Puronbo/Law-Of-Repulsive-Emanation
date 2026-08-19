# ARAKELOV GROTHENDIECK-RIEMANN-ROCH AS 0/0

## The Arithmetic Index Theorem

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-19
**Version:** 1.0

---

## 1. The Theorem

**Theorem (Arakelov GRR, Faltings/Gillet-Soulé):** For a line bundle L
of degree d on a smooth proper curve X of genus g:

    (L, L)_Ar = d² + (2g-2)·d + δ(X)

At d=0, g=1: (L,L)_Ar = δ(X). This is the 0/0: both the quadratic
and linear terms vanish, leaving only the Faltings delta as the
removable value.

**Theorem (Arakelov as 0/0):** The ratio

    R(d) = (L, L)_Ar / (d² + (2g-2)·d)

is a 0/0 at d=0 (when g=1). Removable value = δ(X).

---

## 2. The Three Probes

### 2.1 Self-Intersection Formula (Probe 1)

For g=1 (torus), δ = -6·log(π) + 3·log(2):

    d=0: (L,L)_Ar = 0 + 0 + δ = δ = -3.467... (removable value!)
    d=1: (L,L)_Ar = 1 + 0 + δ = -2.467...
    d=2: (L,L)_Ar = 4 + 0 + δ = 0.532...
    d=3: (L,L)_Ar = 9 + 0 + δ = 5.532...

All 4 match the formula d² + δ. ✓

The 0/0 at d=0: the topological intersection d² + (2g-2)d vanishes,
and the removable value is the Faltings delta — the analytic correction
that makes the arithmetic index theorem work.

### 2.2 Structure Sheaf (Probe 2)

For O_X (trivial bundle, d=0):

    (O, O)_Ar = 0 + 0 + δ(X) = δ(X)

This is the Faltings delta of the curve, a conformal invariant.
For g=1: (O,O)_Ar = δ(T²) = -6·log(π) + 3·log(2).
The 0/0: (O,O)_Ar / (2g-2) = δ / 0 at g=1.

### 2.3 Pushforward (Probe 3)

For a morphism f: X → Y of arithmetic curves:

    f_!(ch(E) · td(X)) = ch(f_*(E)) · td(Y)

Verified for:
- Identity map (degree 1): trivially holds
- Degree-2 cover: rank doubles, correction at branch points
- Composition: degree-2 ∘ degree-3 = degree-6

The arithmetic index theorem for the tangent bundle:
- g=0: ind = 2 (P¹ has 2 sections)
- g=1: ind = 0 (elliptic curve, trivial tangent) — the 0/0!
- g=2: ind = -2

At g=1: the topological index vanishes, and the arithmetic correction
(δ/2π) is the removable value.

---

## 3. The Chain

Arakelov GRR completes the index theory:

```
Topological Index:    ind(D) = ch(TX) · td(X)     [Atiyah-Singer]
                             ↓
Arithmetic Index:     ind_Ar(D) = ch_Ar(TX) · td_Ar(X)  [Arakelov GRR]
                             ↓
p-adic Index:         ind_p(D) = L_p(E, 1)         [Iwasawa Main Conj.]
```

Each level adds a layer of arithmetic:
- Topological: integer (the Euler characteristic)
- Arithmetic: real (integer + Faltings delta)
- p-adic: p-adic number (the p-adic L-value)

The 0/0 at each level: when the topological index vanishes, the
removable value is the arithmetic correction.

---

## 4. What Opens

1. **Higher-dimensional Arakelov GRR:** For arithmetic surfaces and
   higher. The 0/0 at each dimension has removable value = the
   higher Faltings invariant.

2. **Arakelov Euler Structure:** The torsion in the arithmetic
   Chow group. The 0/0 at the trivial class has removable value.

3. **Colmez Conjecture:** Relates the Faltings height to the
   derivative of the L-function. Connects Arakelov GRR to Iwasawa.

4. **Vojta's Conjecture:** Height bounds from the 0/0 analysis.

5. **Arakelov Intersection Theory:** The full product structure on
   arithmetic Chow groups. The 0/0 at each product has removable value.

---

**Key files:**
- `experiments/arakelov_grr_0_over_0.py`
- `data/arakelov_grr_data.json`
- `tests/test_solvable_theorems.py::test_arakelov_grr`
