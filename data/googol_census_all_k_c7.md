# C7 Prime Geodesic Bridge — All k-Families (odd k < 30)

**Scope:** 2ⁿ − k primes < 10¹⁰⁰ (n ≤ 332)
**Total:** 186 primes across 15 k-families

---

## 1. Sparsity Ranking

| Rank | k | Count | Avg gap | Max gap | 2ⁿ mod 3 constraint |
|------|---|-------|---------|---------|---------------------|
| 1 | 7 | **1** | 332.0 | 332 | n odd (k ≡ 1) |
| 2 | 29 | **4** | 69.0 | 108 | n even (k ≡ 2) |
| 3 | 13 | **8** | 19.0 | 48 | n odd (k ≡ 1) |
| 4 | 11 | **10** | 35.3 | 132 | n even (k ≡ 2) |
| 5 | 23 | **10** | 35.3 | 112 | n even (k ≡ 2) |
| 6 | 1 | **12** | 11.4 | 30 | n odd (k ≡ 1) |
| 7 | 9 | **13** | 26.4 | 102 | no restriction (k ≡ 0) |
| 8 | 15 | **13** | 19.2 | 58 | no restriction (k ≡ 0) |
| 9 | 21 | **13** | 8.8 | 43 | no restriction (k ≡ 0) |
| 10 | 25 | **13** | 15.3 | 36 | n odd (k ≡ 1) |
| 11 | 19 | **16** | 19.1 | 72 | n odd (k ≡ 1) |
| 12 | 27 | **16** | 15.0 | 90 | no restriction (k ≡ 0) |
| 13 | 17 | **17** | 12.0 | 52 | n even (k ≡ 2) |
| 14 | 5 | **19** | 12.4 | 52 | n even (k ≡ 2) |
| 15 | 3 | **21** | 13.2 | 65 | no restriction (k ≡ 0) |

**Pattern:** k ≡ 0 mod 3 (no mod-3 constraint) averages **15.8** primes. k ≡ 2 mod 3 averages **12.0**. k ≡ 1 mod 3 averages **10.2** — but k=7 drags this down dramatically at only 1.

---

## 2. The k=7 Anomaly

Only **n = 39** yields a prime for 2ⁿ − 7 < 10¹⁰⁰.

**Connection to Ramanujan–Nagell:** The equation 2ⁿ − 7 = x² has exactly 5 solutions (n = 3, 4, 5, 7, 15). None coincide with 2ⁿ − 7 being prime — but the same covering congruence structure that limits square values also limits primality.

**Covering system for k=7:**

| p | order | n ≡ ? mod order → p divides 2ⁿ−7 |
|---|-------|----------------------------------|
| 3 | 2 | n ≡ 0 → covers all **even** n |
| 5 | 4 | n ≡ 1 → covers n ≡ 1, 5, 9, ... |
| 11 | 10 | n ≡ 7 → covers n ≡ 7, 17, 27, ... |
| 13 | 12 | n ≡ 11 → covers n ≡ 11, 23, ... |
| 19 | 18 | n ≡ 6 → covers n ≡ 6, 24, 42, ... |
| 29 | 28 | n ≡ 12 → covers n ≡ 12, 40, ... |

Combined density: only ~12% of n survive trial division by primes ≤ 31. Of those, only n=39 survives full primality testing under 10¹⁰⁰.

---

## 3. Mod 12 Patterns

The constraint 2ⁿ mod 3 forces parity selection:

| k mod 3 | Parity | k values | Surviving n mod 12 |
|---------|--------|----------|-------------------|
| 0 | unrestricted | 3, 9, 15, 21, 27 | all residues |
| 1 | n **odd** | 1, 7, 13, 19, 25 | 1, 3, 5, 7, 9, 11 |
| 2 | n **even** | 5, 11, 17, 23, 29 | 0, 2, 4, 6, 8, 10 |

Within this parity, k further restricts:

| k | Dominant n mod 12 | Count fraction |
|---|-------------------|----------------|
| 3 | 2, 5, 6, 10 (4 each) | 4/21 |
| 9 | 9 (6/13) | 6/13 |
| 11 | 6 (5/10) | 5/10 |
| 17 | 8 (6/17) | 6/17 |
| 25 | 9 (7/13) | 7/13 |
| 27 | 8, 10 (4 each) | 4/16 |

---

## 4. C7 Bridge — Near-Integer Eigenvalues

The Selberg eigenvalue λ = ¼ + ℓ² where ℓ = n·ln2 − ln(k). Six primes have λ within 0.01 of an integer:

| k | n | Digits | λ | frac(λ) | |λ − round(λ)| |
|---|---|--------|---|---------|--------------|
| 17 | 6 | 2 | 2.007400 | 0.0074 | **0.0074** |
| 11 | 114 | 35 | 5871.009759 | 0.0098 | **0.0098** |
| 21 | 46 | 14 | 832.009897 | 0.0099 | **0.0099** |
| 9 | 21 | 7 | 152.991574 | 0.9916 | 0.0084 |
| 29 | 8 | 3 | 4.993168 | 0.9932 | 0.0068 |
| 27 | 6 | 2 | 0.994849 | 0.9948 | 0.0052 |

These "spectral resonances" may indicate geodesics whose lengths align with the arithmetic tail of the Selberg zeta function.

---

## 5. Cross-Family Coincidences

39 values of n produce primes for multiple k. The most prolific:

| n | # of k | k values |
|---|--------|----------|
| 5 | **10** | 1, 3, 9, 13, 15, 19, 21, 25, 27, 29 |
| 4 | **5** | 3, 5, 9, 11, 13 |
| 6 | **7** | 3, 5, 11, 17, 21, 23, 27 |
| 8 | **6** | 5, 15, 17, 23, 27, 29 |
| 10 | **5** | 3, 5, 11, 15, 27 |

All are small n (small numbers → higher primality probability).

---

## 6. Summary

1. **k=7 is uniquely sparse** — the covering congruence overlap from p=3 (even n) and p=5 (n≡1 mod 4) eliminates ~90% of candidates, and only n=39 is prime under 10¹⁰⁰.
2. **k ≡ 0 mod 3 families are densest** because 2ⁿ mod 3 imposes no parity filter.
3. **6 spectral resonances** (λ ≈ integer) found across families — potentially testable against the Selberg trace formula.
4. **C7 bridge extended** to all 186 primes — full data in `googol_census_all_k_c7.json`.

Files:
- `data/googol_census_all_k.json` — raw prime exponents by k
- `data/googol_census_all_k_c7.json` — C7 bridge values for every prime
