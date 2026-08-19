# SATO-TATE CONJECTURE AS 0/0

## The Semicircle Law for Elliptic Curves

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-19
**Version:** 1.0

---

## 1. The Theorem

**Theorem (Sato-Tate, proved 2011):** For a non-CM elliptic curve E
over Q, the normalized Frobenius traces x_p = a_p / (2*sqrt(p))
follow the semicircle distribution on [-1,1]:

    mu_ST(dx) = (1/pi) * sqrt(1 - x^2) dx

**Theorem (as 0/0):** The difference between the empirical distribution
of x_p and the semicircle law converges to 0.
At CM curves: the distribution DEGENERATES. The 0/0 at CM has
removable value = the CM-specific atomic measure.

---

## 2. The Three Probes

### 2.1 Semicircle Law (Probe 1)

E: y^2=x^3-x+1 (non-CM), 470 good primes:
    KS statistic: 0.069 (semicircle not rejected) ✓
    Hasse bound: all |x_p| <= 1 ✓
    Moments: E[x^2]=0.248 (exp 0.25), E[x^4]=0.128 (exp 0.125),
             E[x^6]=0.081 (exp 0.078) ✓

### 2.2 CM Degeneration (Probe 2)

E: y^2=x^3-x (CM by Z[i]):
    KS vs semicircle: 0.336 (REJECTED) ✓
    CM primes (p=3 mod 4): all x_p = 0 ✓
    Fraction near 0: 50.2% (half are exactly 0)
    Split primes: non-zero x_p ✓

### 2.3 Moment Convergence (Probe 3)

Two non-CM curves, moments match Catalan numbers:
    E[x^2] ~ 1/4, E[x^4] ~ 1/8, E[x^6] ~ 5/64
    All within 20% of expected. ✓

---

## 3. The Chain

Sato-Tate extends Shimura-Taniyama:

```
Shimura-Taniyama (L(E,s) = L(f,s))
       |
    Sato-Tate (distribution of a_p)
       |
    Langlands (automorphic representations)
```

The 0/0: at CM curves, the semicircle degenerates.
Removable value = the CM-specific measure.

---

## 4. What Opens

1. **Higher-dimensional Sato-Tate:** For abelian varieties of
   dimension g > 1. The distribution is on Sp(2g).
2. **Sato-Tate for Galois representations:** Generalize beyond
   elliptic curves to higher-dimensional representations.
3. **Effective Sato-Tate:** Explicit convergence rates.

---

**Key files:**
- `experiments/sato_tate_0_over_0.py`
- `data/sato_tate_data.json`
- `tests/test_solvable_theorems.py::test_sato_tate`
