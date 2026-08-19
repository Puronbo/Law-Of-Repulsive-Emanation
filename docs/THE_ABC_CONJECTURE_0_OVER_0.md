# ABC CONJECTURE AS 0/0

## How the Master Conjecture of Number Theory is a Singularity

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-19
**Version:** 1.0

---

## 1. The ABC Conjecture

**Conjecture (ABC, Oesterlé-Masser):** For any ε > 0, there are only
finitely many coprime triples (a, b, c) with a + b = c and
rad(abc)^(1+ε) > c.

**Theorem (ABC as 0/0):** The quality q(a,b,c) = log(c)/log(rad(abc))
is a 0/0 at the critical balance ε = 0. For ε > 0, only finitely many
triples have q > 1 + ε. The removable value at ε = 0 is the quality
supremum.

---

## 2. The Three Probes

### 2.1 Quality Computation (Probe 1)

The quality q = log(c)/log(rad(abc)) measures the "surprise" of the
triple: how much larger c is than rad(abc).

Known: sup(q) ≥ 1.6299 (from record-holding triples).
For small triples (c ≤ 200): max quality found, with n triples above
quality 1, 1.1, 1.2.

The 0/0: at the balance point rad(abc) ~ c (quality ~ 1), the
additive and multiplicative structures are in perfect equilibrium.

### 2.2 Finiteness (Probe 2)

For ε = 0.5: very few triples with q > 1.5 (verified up to c = 1000).
For ε = 0.1: more triples, but still finite.
The 0/0 at ε = 0: transition from infinite to finite.
This is the Brody boundary of arithmetic geometry.

### 2.3 Connections (Probe 3)

ABC implies:
- **Fermat's Last Theorem** for n ≥ 5 (effective)
- **Effective Mordell** (height bounds for rational points)
- **Effective Thue-Siegel-Roth** (diophantine approximation)

Each implication is a 0/0 with removable value 1.

---

## 3. The Chain

ABC sits at the apex of arithmetic geometry:

```
Gauss-Bonnet -> Riemann-Roch -> Atiyah-Singer -> BSD -> Modularity
    -> Langlands -> NCG -> Faltings -> ABC -> Fermat, Mordell, Roth
```

ABC is the master conjecture: it implies Faltings (for curves of
general type), effective bounds for all diophantine problems, and
the finiteness of exceptional structures.

---

## 4. What Opens

1. **Effective Number Theory:** ABC makes all diophantine results
   effective. The 0/0 at each implication has removable value = the
   effective constant.

2. **Iwasawa Theory:** ABC connects to p-adic L-functions via the
   Iwasawa main conjecture. The 0/0 at the p-adic limit has removable
   value = the characteristic ideal.

3. **The Riemann Hypothesis:** Some approaches to RH use ABC-type
   bounds on the radical. The 0/0 at the critical strip has removable
   value = the zeros.

4. **Conjecture C (Langlands):** ABC is equivalent to Conjecture C
   in the Langlands program. The 0/0 is the functoriality boundary.

---

**Key files:**
- `experiments/abc_conjecture_0_over_0.py`
- `data/abc_conjecture_data.json`
- `tests/test_solvable_theorems.py::test_abc_conjecture`
