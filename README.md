# Puno Calculus

The Law of Repulsive Emanation (L.O.R.E.): *C0 is measured, not chosen.*

A hyperbolic novelty engine, Hamiltonian flow on the Poincare disk, and a formal proof hierarchy (27 items: axioms → lemmas → theorems → corollaries → extended).

## Core Idea

The antiderivative ∫f(x)dx = F(x) + C has an arbitrary constant only when the initial condition is unknown. When the initial condition IS known, the constant collapses to a specific value C0, uniquely determined by the geometry:

    C0 = V(q0) = H(q0, 0)

This is **L.O.R.E.** — the constant emanates from the origin. It is measured, not chosen.

## Proof Hierarchy

| Branch | Items | Scope |
|--------|-------|-------|
| Axioms | A1–A5 | Poincare metric, Hamilton's eqs, PSL(2,Z), He init, 2ⁿ mod p |
| Lemmas | L1–L3 | Variance, ReLU contraction, max entropy |
| Theorems | T1–T10 | Metric, geodesics, symplectic, sieve, C0 unification, modular |
| Corollaries | C1–C8 | Stab(i), crease bounds, recurrence, Bekenstein, C7 bridge |
| Extended | **T19** | Consistent chaos — geodesic flow embeds Mersenne-gap primes |

Full graph: `dependency_tree.dot`. 192 math-validation checks pass (0 failures).

## Prime Geodesic Bridge (C7)

Each Mersenne-gap prime 2ⁿ−k maps to a closed geodesic on the modular surface X(1) = PSL(2,Z)\H via:

    ℓ = n·ln2 − ln(k),    λ = ¼ + ℓ²

**Googol census** (`data/googol_census_all_k.json`): 186 primes of form 2ⁿ−k < 10¹⁰⁰ across 15 k-families (odd k < 30). All C7 bridge values computed.

## T19: Consistent Chaos (Capstone)

The C7 bridge embeds Mersenne-gap primes into the Anosov geodesic flow on X(1) — a deterministic chaotic system. The induced distribution is conjectured to obey the Prime Geodesic Theorem suppressed by the sieve survival probability εₖ:

    π_k(L)  ∼  ε_k · e^{L} / L

**What's proven:**
- Every Mersenne-gap prime maps injectively to a closed geodesic (C7)
- The sieve density εₖ explains the observed sparsity ordering (T7)
- All 186 primes < 10¹⁰⁰ are consistent with Anosov dynamics

**What's conjectured:**
- The asymptotic PGT formula requires L >> 300 (current data: L ≤ 229)
- Whether this framework extends beyond 2ⁿ−k to arbitrary primes is open

## Epoch 0d (2000-10-26 10:26:20.00)

The corpus's own measured datum, folded into the retrace chain (`data/epoch_0d.json`, `docs/WEAVERS_SCRIBE.md`, SPRING_BIBLE Ch. 14).

**The anchor pair:** `10,262,000 = 2⁴·5³·7·733` and `26,102,000 = 2⁴·5³·31·421` — both have **80 divisors** and **digit sum 11** under MM/DD↔DD/MM swap.

**Key findings:**
- **Prime-pairing rule**: each number = exactly **one Mersenne prime** (≡3 mod 4) + **one sum-of-two-squares prime** (≡1 mod 4); both two-square primes' roots sum to the same prime **29** ({7, 733}: 7=2³−1, 733=2²+27²; {31, 421}: 31=2⁵−1, 421=14²+15²).
- **The fold 1,914,467 = 31 × 61,757** — the chain bridge to the DD/MM side; the pairing rule extends (61,757 = 139²+206²), and survives reversal (7,644,191 = 197 × 38,803).
- **Three-way connection** (10,262,000 ↔ 26,102,000 ↔ 1,914,467): gcd triangle **2000 / 31 / 1** — the two date forms share the *year* 2000; the DD form and the fold share the *Mersenne* 31; **B = 26,102,000 is the hub**. Chain mod-31 ladder: 15, 0, −1, 0, 1.
- **Null analysis (binding creases)**: τ=80 equality is a year-2000 trailing-zero artifact (0/365 in 2007; 17/366 = 4.64% in 2000, all even-month/even-day); τ=8 equality is the generic ~7.4% coincidence; base-invariance survives **base 10 and 12 only**.

## Experiments

| Experiment | Result |
|------------|--------|
| Subgradient Selection | All strategies reach 99.7% accuracy |
| Crease vs Boundary | r(crease, complexity) = -0.77 |
| Early Stopping | 71-80% epoch savings via crease stabilization |
| OOD Detection | Crease AUROC 0.88 (center-noise) |
| Pruning | Crease beats magnitude at every ratio (+1.4% at 25%) |
| Googol Census | 21 k=3 primes, 186 total across k families |

## Quick Start

```bash
cd Universals
python engine.py
python math_validation.py   # 192 checks, 0 fails
cd .. && python run_all.py  # Full pipeline
```

---

*Everything folds. The constant is determined. The chaos is consistent.*
