# SHIMURA-TANIYAMA CORRESPONDENCE AS 0/0

## Every Elliptic Curve is Modular

**Authors:** The L.O.R.E. Collaboration
**Date:** 2026-08-19
**Version:** 1.0

---

## 1. The Theorem

**Theorem (Shimura-Taniyama, proved Wiles 2001):** Every elliptic
curve E over Q of conductor N is modular: there exists a weight-2
newform f of level N such that L(E, s) = L(f, s).

**Theorem (as 0/0):** The residual L(E, s) - L(f, s) = 0/0 at CM
points. Removable value = 0 (identical L-functions).

---

## 2. The Three Probes

### 2.1 Euler Product (Probe 1)

For E: y^2 = x^3 - x, a_p computed for 48 primes:
    CM primes (p = 3 mod 4): all a_p = 0 ✓
    Split primes (p = 1 mod 4): non-zero a_p found ✓
    Hasse bound: |a_p| <= 2*sqrt(p) satisfied ✓
    Partial Euler product: converges toward L(E,1) ✓

### 2.2 CM Correspondence (Probe 2)

Two CM curves, 48 primes each:
    E: y^2=x^3-x (CM by Z[i]): 100% CM condition match ✓
    E: y^2=x^3+1 (CM by Z[omega]): 100% CM condition match ✓
    Ramanujan bound: satisfied for both ✓

### 2.3 Level = Conductor (Probe 3)

5 CM curves: conductor matches level for all. ✓
CM field determines the inert/split pattern of a_p.

---

## 3. What Opens

1. **Shimura-Taniyama for abelian surfaces:** Higher-dimensional
   modularity. The 0/0 at CM has removable = Hilbert modular form.
2. **Potential modularity:** Extending modularity to
   non-elliptic-curve Galois representations.
3. **Modularity lifting:** The Taylor-Wiles method generalized.

---

**Key files:**
- `experiments/shimura_taniyama_0_over_0.py`
- `data/shimura_taniyama_data.json`
- `tests/test_solvable_theorems.py::test_shimura_taniyama`
