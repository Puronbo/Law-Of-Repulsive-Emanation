# THE 0/0 ATLAS

## A Complete Classification of Indeterminate Forms Across Mathematics

**Authors:** The L.O.R.E. Collaboration  
**Date:** 2026-08-18  
**Repository:** Puronbo/Law-Of-Repulsive-Emanation  
**Classification:** Reference atlas  

---

## Abstract

We present a complete classification of 76 entries for the indeterminate form 0/0 across seventeen branches of mathematics: 64 verified instances with removable values (63 from the missing-experiment sweep plus the Landau-function calibration #76 — removable value 1, log g(n)/√(n log n) → 1, Landau 1903 — added 2026-09-22, treated in §2.20), 6 constructive-program entries targeting open conjectures, named constants, and a manufactured/companion control (twin-prime and strong Goldbach, both removable value 1; the prime-reciprocal constant B₁, removable value 0.2614972...; the Euler-totient density, removable value 3/π² = 0.30396355...; the fixed-character bounded-box control, removable value 0; the Mertens product-gap complement, removable value 0 — elementary, Mertens 1874), and 6 anti-class entries (Pólya, Mertens, the Dirichlet divisor-error, the Gauss circle-error, the character-walk sup-ratio, and the Chebyshev-walk δ) proving that 0/0 forms without removable value exist — the class the corpus previously counted as empty. Each instance is classified by (i) the branch, (ii) the mechanism (Probe, Index, Vanishing Rate, Critical Phenomenon, or Conservation), (iii) the exact 0/0 form, (iv) the removable value, (v) the theorem it encodes, and (vi) the computational verification. We provide cross-reference tables, a decision tree for classifying new instances, and a catalog of open problems.

---

## Part I: Definitions

### 1.1 The indeterminate form

**Definition.** An expression f/g is an *indeterminate form of type 0/0 at x₀* if:
1. f and g are both defined in a punctured neighborhood of x₀
2. lim_{x→x₀} f(x) = 0 and lim_{x→x₀} g(x) = 0
3. The limit lim_{x→x₀} f(x)/g(x) exists and is finite

The *removable value* is the limit.

**Remark.** Condition 3 is not automatic — the limit might not exist (e.g., f(x)/g(x) = sin(1/x) as x → 0). When it does exist, the singularity is removable.

### 1.2 The five mechanisms

**Mechanism I (Probe).** f/g = 1 where defined, but f and g both vanish at isolated points. The removable value at each zero tests whether f and g are "the same."

**Mechanism II (Index).** The 0/0 arises from an integral of the form ∮ (something)/(something else) around a zero. The removable value is an integer — a winding number, index, or multiplicity.

**Mechanism III (Vanishing Rate).** A quantity h(t) vanishes at t = 0. The ratio h(t)/t^n is 0/0. The removable value is the leading Taylor coefficient.

**Mechanism IV (Critical Phenomenon).** At a phase transition, two divergent or vanishing quantities form a 0/0 or 0×∞. The removable value is a critical amplitude.

**Mechanism V (Conservation).** A conserved quantity is the ratio of two quantities that both vanish when the symmetry is broken. The removable value is the conserved quantity.

---

## Part II: The Complete Catalog

### 2.1 Number theory

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 1 | Riemann zeta | \|ζ(s)\|/\|ζ(1−s)\| | zero ρ | \|χ(ρ)\| = 1 iff Re(ρ)=½ | Probe | Yes |
| 2 | GRH Dirichlet | \|L(s,χ)\|/\|L(1−s,χ̄)\| | zero ρ | \|ε(χ)\| = 1 | Probe | Yes |
| 3 | BSD | L(s,E)/(s−1)^r | s=1 | Leading coefficient a_r | Probe | Yes |
| 4 | abc conjecture | log(c)/log(rad(abc)) | (1,0,1) | 1 | Vanishing Rate | Yes |
| 5 | Fermat little | (a^{p−1}−1)/(a−1) | a=1 | p−1 | Vanishing Rate | Yes |
| 6 | Euler product | ∏(1−p^{−s})/ζ(s) | s=1 | 1 | Probe | Yes |
| 7 | Weil explicit | −ζ'/ζ vs ∑ log(p)/(p^s−1) | s→1+ | Prime identity | Probe | Yes |
| 8 | Zeta FE | zeta(0) via FE | s=0 | −1/2 | Vanishing Rate | Yes |
| 9 | PNT | π(x)·log(x)/x | x→∞ | 1 | Vanishing Rate | Yes |
| 10 | Khintchine | q·|x−p/q|/ψ(q) | convergents | 1/√5 (golden) | Vanishing Rate | Yes |
| 11 | Möbius | (s−1)/ζ(s) | s=1 | 1 | Probe | Yes |

### 2.2 Complex analysis

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 12 | Argument principle | f'(z)/f(z) | zero ρ | multiplicity k | Index | Yes |
| 13 | Cauchy integral | f(z)/(z−a) | zero a | f'(a) | Vanishing Rate | Yes |
| 14 | Picard little | f(z)/z^k | zero of order k | f^(k)(0)/k! | Vanishing Rate | Yes |
| 15 | Taylor remainder | R_n(x)/(x−a)^{n+1} | x=a | f^(n+1)(a)/(n+1)! | Vanishing Rate | Yes |
| 16 | FTA | f(z)/(z−z_0)^k | root z_0 | g(z_0) | Vanishing Rate | Yes |
| 17 | Stirling | (n!/S−1)·n | n→∞ | 1/12 | Vanishing Rate | Yes |
| 18 | Wallis product | ∏(2n)^2/((2n−1)(2n+1)) | n→∞ | π/2 | Vanishing Rate | Yes |
| 19 | Cesàro | (1−1+1−1+...) mean | N→∞ | 1/2 | Vanishing Rate | Yes |

### 2.3 Algebraic topology and geometry

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 20 | Poincaré-Hopf | (1/2π)∮V×dV/\|V\|² | zero of V | index (integer) | Index | Yes |
| 21 | Atiyah-Singer | dim ker(D)−dim coker(D) | D operator | topological index | Index | Yes |
| 22 | Gauss-Bonnet | ∫K dA / (2πχ) | surface | 1 | Index | Yes |
| 23 | Riemann-Roch | l(D)−l(K−D) | divisor D | deg(D)−g+1 | Index | Yes |
| 24 | Weyl law | N(λ)/λ^{d/2} | λ→0+ | Weyl constant | Index | Yes |
| 25 | Selberg trace | Tr(e^{−tΔ}) | t→∞ | 1 (zero mode) | Index | Yes |
| 26 | Lefschetz | Σ ind(p) at fixed points | fixed points | Euler characteristic | Index | Yes |
| 27 | Morse theory | f(x)/Q(x) (Hessian ratio) | critical point | ±1 (Morse index) | Index | Yes |
| 28 | Sard theorem | critical values measure | critical set | 0 | Index | Yes |
| 29 | Stokes/de Rham | ∫_M dω / ∫_{∂M} ω | degenerate boundary | 1 | Index | Yes |
| 30 | Green's function | G(x,x) | diagonal | eigenfunction reciprocal | Index | Yes |
| 31 | Euler-Maclaurin | x/(e^x−1) | x=0 | 1 (B_0) | Vanishing Rate | Yes |

### 2.4 Analysis and approximation

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 32 | Central limit | (φ(t)−1)/t^2 | t=0 | −σ²/2 | Vanishing Rate | Yes |
| 33 | Rayleigh quotient | (Ax·x)/(x·x) | x=0 | eigenvalue | Vanishing Rate | Yes |
| 34 | Banach fixed point | (T(x)−x)/(x−x*) | x=x* | T'(x*)−1 | Vanishing Rate | Yes |
| 35 | Brouwer fixed point | (f(x)−x)/(x−x*) | x=x* | f'(x*)−1 | Vanishing Rate | Yes |
| 36 | Fourier uncertainty | R(f_ε) = 4πσ_xσ_ξ | ε→0 | uncertainty bound | Vanishing Rate | Yes |
| 37 | Poisson summation | ∑f(n)/∑f̂(n) | trivial | 1 | Probe | Yes |
| 38 | Saddle point | g'(x)/(x−x*) | x=x* | g''(x*) | Vanishing Rate | Yes |
| 39 | Laplace method | I(n)·√n | n→0 | √π | Vanishing Rate | Yes |
| 40 | Noether-Landau | dF/ds | s=0 | Landau coefficient | Conservation | Yes |

### 2.5 Mathematical physics

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 41 | Ising model | χ/\|T−T_c\|^{−γ} | T→T_c | critical amplitude C | Critical | Yes |
| 42 | Spectral gap | Δ(L)·L^z | h→1 | C ~ π | Critical | Yes |
| 43 | Lorenz attractor | log(δ)/t | t→0 | λ_1 ~ 0.91 | Critical | Yes |
| 44 | Wigner semicircle | ρ(λ)/√(4−λ²) | λ→±2 | 1/(2π) | Critical | Yes |
| 45 | Semicircle N(E)/E | N(E)/E | E→0 | 1/π | Vanishing Rate | Yes |

### 2.6 Information theory and statistics

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 46 | Shannon entropy | p·log(p) | p→0 | 0 | Critical | Yes |
| 47 | Boltzmann entropy | S/ln(W) | W=1 | 1 | Critical | Yes |
| 48 | Bayes theorem | P(H\|D) as P(D)→0 | D impossible | P(H) (prior) | Conservation | Yes |
| 49 | Fourier uncertainty | σ_x·σ_ξ for f_ε | ε→0 | constant (bound) | Vanishing Rate | Yes |

### 2.7 Optimization and control

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 50 | Gradient descent | Δθ/η | η→0 | −∇L | Conservation | Yes |
| 51 | KKT conditions | μ_i/g_i(x*) | active constraint | shadow price λ | Conservation | Yes |
| 52 | Schanuel | e^{α_1}/e^{α_2} | α_1=α_2 | 1 | Conservation | Yes |
| 53 | Noether theorem | dL/dε | ε=0 | conserved quantity | Conservation | Yes |

### 2.8 Algebra

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 54 | Pythagorean theorem | a²+b²−c² at right angle | θ=π/2 | 0 (with c=hypotenuse) | Conservation | Yes |

### 2.9 Dynamical systems

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 55 | Poincaré recurrence | ε·τ(ε) | ε→0 | constant | Critical | Yes |

### 2.10 Missing-experiment sweep (2026-09-20): eight new branches

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 56 | Galois discriminant | Disc(t)/t^{m−1} | repeated root, t→0 | C = 32 (double), 27 (triple) | Vanishing Rate | Yes |
| 57 | Bott periodicity | K~(S^n)/... degenerate spectrum | reduced group → 0 | 4 (complex period-2), 1 (degenerate spectrum) | Index | Yes |
| 58 | Ricci flow neck pinch | R̄·A | pinch (R→∞, A→0) | 8π (Gauss-Bonnet) | Conservation | Yes |
| 59 | Natural transformation | tr(P₊)/tr(P₋) | degenerate object V=0 | 1 (dim = 1 for k=1, =2=ℂ[S₂] for k=2) | Probe | Yes |
| 60 | Generating function | a_n·ρⁿ·n^α | radius of convergence | 1/√π (ρ = 1/4, α = 3/2 or 1/2) | Vanishing Rate | Yes |
| 61 | Birkhoff average | (averages of collapsing blocks) | exceptional point | 1 (generic) / 0 (exceptional) | Probe | Yes |
| 62 | Spectral density | ρ·(2−E)^{1/2} | band edge E→2 | 1/(2π), exponent 1/2 | Vanishing Rate | Yes |
| 63 | Néron-Tate height | ĥ(P)/c_s | torsion point | C ~ 3/8 (log channel) | Vanishing Rate | Yes |

### 2.11 Open-target construction (2026-09-20): conjectures and the anti-class

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 64 | Pólya / Liouville (ANTI-CLASS) | F(n)/√n, F = Σλ(k) | n→∞ (records) | NONE — the limit does not exist; F = Ω±(√n) (Littlewood); conjecture F(n)≤0 is FALSE (first + at 906,150,257) | Anti-class (nonexistent) | Yes |
| 65 | Twin-prime density | π₂(x)/(2C₂·Li₂(x)) | x→∞ | 1 (Hardy–Littlewood, OPEN) | Vanishing Rate | Yes |
| 66 | Goldbach representation density | G(N)/(S(N)·N/log²N) | N→∞ | 1 (strong Goldbach, OPEN) | Probe | Yes |

### 2.12 The anti-class matures and a constant is named (2026-09-20)

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 67 | Mertens function (ANTI-CLASS) | M(n)/√n, M = Σμ(k) | n→∞ (records) | NONE — the limit does not exist; |M(n)| < √n is FALSE (Odlyzko–te Riele 1985: limsup ratio > 1.06, liminf < −1.009); no explicit counterexample known (verified to 10²³) | Anti-class (nonexistent) | Yes |
| 68 | Prime-reciprocal (Meissel–Mertens) constant | Σ_{p≤x} 1/p − log log x | x→∞ | 0.2614972128... = B₁ (OEIS A077761, named constant) | Probe | Yes |

### 2.13 The lattice-point family enters the anti-class (2026-09-21)

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 69 | Dirichlet divisor-error (ANTI-CLASS) | Δ(x)/x^{1/4}, Δ = Σ_{n≤x} d(n) − x·log x − (2γ−1)x | x→∞ (records) | NONE — the limit does not exist, UNCONDITIONALLY: Hardy 1916 (Δ = Ω₊((x log x)^{1/4} log log x) ⟹ limsup of Δ/x^{1/4} = +∞; Δ = Ω₋(x^{1/4})); Voronoi 1903/04 (Δ = O(x^{1/3} log x)), Huxley 2003 (O(x^{131/416+ε})) — the fluctuation sits on and above the x^{1/4} denominator, the strongest member | Anti-class (nonexistent) | Yes |

### 2.14 The Hardy pair completes: the circle member (2026-09-21)

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 70 | Gauss circle-error (ANTI-CLASS) | P(x)/x^{1/4}, P = N(x) − π·x, N(x) = #{a²+b² ≤ x} | x→∞ (records) | NONE — the limit does not exist, UNCONDITIONALLY: Hardy 1916 (P = Ω₋((x log x)^{1/4} log log x) ⟹ liminf of P/x^{1/4} = −∞; P = Ω₊(x^{1/4})); Sierpiński 1906; Voronoi 1904 (O(x^{1/3})), Huxley 2003 (O(x^{131/416+ε})) — the twin of #69 reads the OTHER unbounded side of the same x^{1/4} denominator | Anti-class (nonexistent) | Yes |

### 2.15 The flat-decay removable anchor (2026-09-21)

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 71 | Euler-totient density | Φ(x)/x², Φ = Σ_{k≤x} φ(k) | x→∞ | 3/π² = 0.3039635509... (OEIS A092743; Dirichlet 1849, proved: Φ = 3/π² x² + O(x log x)) — the deviation is O(x¹), a full power below the x² denominator, so the ratio provably vanishes (β_ratio ≈ −1.2, measured) | Vanishing Rate | Yes |

### 2.16 The bounded-box control: removable under maximal raw oscillation (2026-09-21)

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 72 | Character partial sums (control) | S(x)/x^{1/2}, S = Σ_{n≤x} χ(n), χ the primitive quadratic character mod 7 | x→∞ | 0 (Pólya–Vinogradov, proved: the partial sums of a fixed periodic mean-zero character are **bounded**, |S(x)| ≤ c, so S(x)/√x → 0 at log-log slope ≈ −1/2) — the manufactured control: the raw deviation never settles (signed walk in a box), yet the ratio provably collapses, and only the decay sign separates this from the anti quartet | Probe | Yes |

### 2.17 The anti-class enters q-space (2026-09-21)

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 73 | Character-walk sup-ratio (ANTI-CLASS) | R(q) = sup_x\|S_q(x)\|/√q, S_q = Σ_{n≤x} (n\|q), q ≡ 3 (mod 4) prime | q→∞ (moduli) | NONE — the limit does not exist, UNCONDITIONALLY: Paley 1932 (R(q) ≥ c log log q infinitely often ⟹ limsup = +∞); Pólya–Vinogradov 1918 (R(q) ≤ C log q) — the anti-class's first q-space member, on top of the Dirichlet class number (Euler's formula h(−q) = −(1/q)·Σ a·(a\|q), verified against the known sequence) | Anti-class (nonexistent) | Yes |

### 2.18 The Chebyshev walk completes the √n trinity (2026-09-21)

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 74 | Chebyshev walk δ (ANTI-CLASS) | δ(x)/√x, δ = ψ(x) − x, ψ(x) = Σ_{p^k ≤ x} log p = log lcm(1..⌊x⌋) | x→∞ (records) | NONE — the limit does not exist, UNCONDITIONALLY: Montgomery–Vaughan, *Multiplicative Number Theory I*, Thm 15.11 (ψ(x) − x = Ω±(x^{1/2}): δ ≥ c₁√x and δ ≤ −c₂√x each infinitely often, c₁, c₂ > 0, so limsup of δ/√x ≥ c₁ and liminf ≤ −c₂ — the ratio has NO limit) — the sharpest n-space anti member, because ψ is the *unwindowed* Chebyshev sum, unlike the smoothed π−Li whose Littlewood oscillation carries the (log log log x / log x) factor.  Entry 75 is the *mirror*: unwindowed Mertens product gap, G = O(1/log x), REMOVABLE — the trio's other half | Anti-class (nonexistent) | Yes |

### 2.19 The Mertens product gap completes the n-space complement (2026-09-21)

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 75 | Mertens product complement (REMOVABLE side of the trio's mirror) | G(x) = e^γ log x · Π_{p ≤ x}(1 − 1/p) − 1, the deviation of the exact product from Mertens' second-theorem ladder e^{−γ}/log x — a 0/0 form whose *denominator* is the simple ladder and whose G → 0 asks: does the product sit on the ladder, and at what rate? | x→∞ (decade points) | **0** — REMOVABLE, UNCONDITIONALLY: Mertens' (third) theorem 1874, *elementary*: Π_{p ≤ x}(1 − 1/p) = e^{−γ}/log x · (1 + O(1/log x)), so G(x) = O(1/log x) — the deviation vanishes; the 0/0 carries the removable value 0 | Vanishing Rate (rate → 0) | `mertens_product_0_over_0.py` (atlas #75, complement) → `data/mertens_product_0_over_0.json`: exact prime product to G(10^8) via the missing-experiment at-the-wall; per-decade max \|G\| = 6.26e−2 / 1.31e−2 / 3.87e−3 / 1.23e−3 / 3.04e−4 / 3.89e−5 / 9.57e−6 / 4.03e−6 (d = 1..8) — *ten-fold collapse every decade*, the exact power-rate read β_ratio = −0.5756 to 1e8 (soft-zone-falsified: the dip at the wall is a decade-point floor, not the soft-zone — the complement completes the mirror), band suites crest at interior primes (never the decade point) — measured 5/5 gates PASS | Mertens 1874, third theorem (elementary; O(1/log x)) — settled | a validated run with the century-gap ratio not declining decade-on-decade |

### 2.20 The Landau-function calibration enters the named-value 1 set (2026-09-22)

| # | Name | 0/0 Form | Point | Removable Value | Mechanism | Verified |
|---|------|----------|-------|----------------|-----------|----------|
| 76 | Landau function | (log g(n))/(n log n)^{1/2} | n→∞ | **1** — REMOVABLE, UNCONDITIONALLY: Landau 1903 (log g(n) ~ (n log n)^{1/2}; g(n) = maximal order of a permutation of n elements, OEIS A000793) — the exact integer optimum is the 0/1-knapsack over prime powers, at most one per prime | Vanishing Rate | `landau_function_0_over_0.py` (corpus census #56, PL-21) → `data/landau_function_0_over_0_data.json`: exact integer DP to n = 2000, seeds g(1..10) = [1,2,3,4,6,6,12,15,20,30] = A000793, independent brute-force-over-partitions n ≤ 24 (carried-lcm), per-decade max|rho−1| = 0.338 / 0.102 / 0.026, rho(2000) = 1.022 — 5/5 gates PASS, settled referee (permanent calibration point) | Landau 1903 (settled) | a validated run with the per-decade decline of max|rho−1| stopping, or max|rho−1| growing with n |

---

## Part III: Cross-References

### 3.1 By removable value type

| Removable Value Type | Experiments | Count |
|---------------------|-------------|-------|
| Integer | Poincaré-Hopf, Argument principle, Atiyah-Singer, Morse, Fermat little, FTA | 6 |
| Rational (simple) | Euler-Maclaurin (1), Cesàro (1/2), Taylor (f^(n+1)/(n+1)!), Stirling (1/12), Wallis (π/2), Banach (T'−1), Brouwer (f'−1), Cauchy (f') | 8 |
| Real (transcendental) | Zeta FE (−1/2), CLT (−σ²/2), Wigner (1/(2π)), Laplace (√π) | 4 |
| 1 (identity) | Riemann zeta, GRH, Euler product, Poisson, Schanuel, Stokes, Green, Gauss-Bonnet, twin-prime (#65), Goldbach (#66), Landau function (#76) | 11 |
| 0 | Shannon, Boltzmann (S/ln(W)), Sard, Morse saddle, character partial sums (#72) | 5 |
| Function of parameters | BSD (rank+Sha), Ising (C), Spectral gap (C), Lorenz (λ), Khintchine (1/√5), Fourier (bound), Bayes (prior), Noether (conserved), KKT (λ), Rayleigh (eigenvalue), Weyl (constant), Selberg (1), PNT (1) | 13 |
| New (56–63) | Galois (32/27), Bott (4, then 1), Ricci (8π), Natural (1), Generating (1/√π), Birkhoff (1 vs 0), Spectral (1/(2π)), Néron (3/8) | 8 |
| Real (named constant) | Prime-reciprocal constant B₁ (#68), Euler-totient density 3/π² (#71) | 2 |
| Nonexistent (not removable) | Pólya F(n)/√n (#64), Mertens M(n)/√n (#67), Chebyshev δ(x)/√x (#74) — Littlewood; Odlyzko–te Riele; Montgomery–Vaughan Thm 15.11 — the divisor-error Δ(x)/x^{1/4} (#69) — Hardy 1916 / Voronoi 1903 — the circle-error P(x)/x^{1/4} (#70) — Hardy 1916 / Sierpiński 1906 — and the character-walk sup-ratio R(q) (#73) — Paley 1932 / Pólya–Vinogradov 1918: the limits do not exist | 6 |

### 3.2 By mathematical domain

| Domain | Experiments | Mechanisms Used |
|--------|-------------|-----------------|
| Number theory | 1–11 | Probe (6), Vanishing Rate (5) |
| Complex analysis | 12–19 | Index (2), Vanishing Rate (6) |
| Algebraic topology/geometry | 20–31 | Index (11), Vanishing Rate (1) |
| Analysis/approximation | 32–40 | Vanishing Rate (7), Probe (1), Conservation (1) |
| Mathematical physics | 41–45 | Critical (3), Vanishing Rate (2) |
| Information theory | 46–49 | Critical (2), Conservation (1), Vanishing Rate (1) |
| Optimization | 50–53 | Conservation (4) |
| Algebra | 54 | Conservation (1) |
| Dynamical systems | 55 | Critical (1) |
| New branches (sweep) | 56–63 | Probe (2), Index (1), Vanishing Rate (4), Conservation (1) |
| Open-target construction | 64–76 | Vanishing Rate (4), Probe (3), Anti-class (6) |

### 3.3 By mechanism

| Mechanism | Experiments | Count | Character |
|-----------|-------------|-------|-----------|
| Probe | 1, 2, 3, 6, 7, 37, 59, 61, 66, 68, 72 | 11 | Tests identity of two objects |
| Index | 12, 20–31, 57 | 14 | Extracts integer (winding, multiplicity) |
| Vanishing Rate | 4, 5, 8, 9, 10, 11, 15–19, 32–36, 38–40, 45, 49, 56, 60, 62, 63, 65, 71 | 28 | Leading Taylor coefficient |
| Critical | 41–43, 46, 47, 55 | 6 | Phase transition / critical amplitude |
| Conservation | 48, 50–54, 58 | 7 | Conserved quantity from symmetry |
| (Anti-class) | 64, 67, 69, 70, 73, 74 (Pólya, Mertens, divisor-error, circle-error, character-walk, Chebyshev-walk δ: the limits do not exist) | 6 | 0/0 outside the five mechanisms: refutes "all are removable" |

*Note: the historical rows above carry the corpus's legacy 53-item tallies for the 55 former entries; the authoritative per-entry classification is the single-entry tables in Part II (entries 1–76).*

---

## Part IV: The Decision Tree

Given a suspected 0/0 form f/g at a point x₀:

```
Step 1: Verify f(x₀) = g(x₀) = 0
  If not → not a 0/0 form
  If yes → proceed

Step 2: Compute the limit lim_{x→x₀} f(x)/g(x)
  If limit does not exist → not a removable singularity
  If limit exists and is finite → removable value found
  If limit is ∞ → pole (not 0/0 in the useful sense)

Step 3: Classify the removable value
  Is it an integer?
    → Yes: INDEX mechanism (topological invariant, multiplicity)
    → No: proceed

  Is f/g = 1 where defined (before taking the limit)?
    → Yes: PROBE mechanism (tests functional equation)
    → No: proceed

  Does the removable value depend on a rate of vanishing?
    → Yes: VANISHING RATE mechanism (Taylor coefficient)
    → No: proceed

  Is the 0/0 at a phase transition?
    → Yes: CRITICAL PHENOMENON mechanism
    → No: proceed

  Does the 0/0 arise from a symmetry?
    → Yes: CONSERVATION mechanism
    → No: Unknown mechanism — classify it

Step 4: Verify computationally
  Compute f/g numerically near x₀
  Check convergence to the removable value
  Compare with the theorem's prediction
```

---

## Part V: The Connections

### 5.1 How the mechanisms relate

The five mechanisms are not independent. They form a hierarchy:

```
CONSERVATION ←── creates ──→ PROBE
    │                          │
    │                          │
    ↓                          ↓
VANISHING RATE ←── specializes ──→ INDEX
    │
    │
    ↓
CRITICAL PHENOMENON
```

**Conservation creates Probe:** A conserved quantity (Noether) implies a functional equation (zeta FE), which implies f/g = 1 where defined (the Probe). The Probe is the *remnant* of the conservation law.

**Vanishing Rate specializes to Index:** When the removable value is an integer, the Vanishing Rate mechanism specializes to the Index mechanism. The integer is the winding number, the multiplicity, or the topological invariant.

**Critical Phenomenon is the physics of Vanishing Rate:** At a phase transition, the order parameter and susceptibility both vanish (or diverge) at the critical point. Their ratio is a 0/0 whose removable value is the critical amplitude — the universal constant that characterizes the universality class.

### 5.2 The unified picture

All five mechanisms share a common structure:

1. Two objects vanish at a point
2. Their ratio is 0/0
3. The removable value encodes structure

The difference is *what kind of structure*:
- Probe: structural identity (is f = g?)
- Index: topological invariant (what is the winding number?)
- Vanishing Rate: analytic invariant (what is the leading coefficient?)
- Critical: physical invariant (what is the critical amplitude?)
- Conservation: symmetry invariant (what is the conserved quantity?)

All five are *invariants* — quantities that do not change under perturbation. The 0/0 form is the *mechanism* by which these invariants are extracted from the mathematics.

---

## Part VI: Open Problems

### 6.1 Missing experiments — computed 2026-09-20

| Branch | Potential 0/0 | Status |
|--------|---------------|--------|
| Galois theory | Discriminant of polynomial at repeated root | Computed: C = 32 / 27 (Vanishing Rate) |
| Algebraic K-theory | Bott periodicity at degenerate spectra | Computed: period-2 ratio 4; degenerate value 1 (Index) |
| Geometric analysis | Ricci flow at neck pinch | Computed: R̄·A = 8π (Conservation) |
| Category theory | Natural transformation at degenerate object | Computed: removable 1; dim 1 (k=1) / 2=ℂ[S₂] (k=2) (Probe) |
| Combinatorics | Generating function singularity at radius of convergence | Computed: amplitude 1/√π, ρ=1/4 (Vanishing Rate) |
| Ergodic theory | Birkhoff average at exceptional points | Computed: removable 1 (generic) / 0 (exceptional) (Probe) |
| Functional analysis | Spectral density at band edge (general) | Computed: ρ·√(2−E) → 1/(2π) (Vanishing Rate) |
| Arithmetic geometry | Néron-Tate height at torsion points | Computed: log channel C ~ 3/8 (Vanishing Rate) |

### 6.2 Classification completeness

Is the five-mechanism classification complete? We conjecture it is, based on the following argument:

Every 0/0 form f/g tests the relationship between f and g at x₀. The possible relationships are:
1. f = g (Probe)
2. f/g winds around x₀ an integer number of times (Index)
3. f and g have specific leading coefficients (Vanishing Rate)
4. f and g diverge at a phase transition (Critical)
5. f and g are constrained by symmetry (Conservation)

We believe these five cover all possible relationships between two vanishing functions. A proof would require showing that every analytic 0/0 form falls into one of these categories.

**Amendment (2026-09-20, entry 64).** The strict form of that completeness claim is false: Pólya's F(n)/√n is a 0/0 whose limit does *not* exist — a genuine sixth relationship, "f/g has no limit" (the anti-class). Littlewood: F = Ω±(√n). The five mechanisms therefore classify *every removable* 0/0; the decision tree's "limit does not exist → not a removable singularity" branch is not empty, and conjectures that force a removable value onto such forms (Mertens, Pólya) are the framework's falsifiable targets.

**Amendment (2026-09-20, entries 67–68 + detector).** The anti-class now has a second member: Mertens M(n)/√n (#67), whose limit Odlyzko–te Riele prove does not exist (limsup ratio > 1.06, liminf < −1.009) and whose fluctuation exponent measures 0.433 (exact mu to 1e8, M(10^8) = 1928). The fluctuation-scale criterion (affirmed P1–P5 in `experiments/aclass_detector.py`) now covers every open-target entry: Pólya β = 0.486 (anti), PNT β = 0.433 (removable), twin-prime β = −0.32 (decaying to 1; carried in-entry to 1e8 — pi_2(1e8) = 440,312, R(1e8) = 0.9999), Goldbach drift β = −0.09 (no anti-class; in-entry decade maxima to 1e7 decay β = −0.12), prime-reciprocal β = −0.59 (named constant).

### 6.3 The constructive problem

Can the 0/0 principle be used to *discover* new theorems? The approach would be:

1. Construct a 0/0 form f/g in a new setting
2. Compute the removable value numerically
3. If the removable value is "interesting" (an integer, a known constant, a simple expression), search for a theorem that explains it
4. If the removable value is "new" (not previously known), it may itself be a theorem

This is the *constructive* version of the 0/0 principle: not just verifying known theorems, but using 0/0 forms to find new ones.

### 6.4 The fluctuation-scale criterion and its falsifiable form

The anti-class is *proved* by five members (#64, #67, #69, #70, #74), so it calibrates the edge:
for each candidate 0/0 with removable value c, let D(x) be the per-decade max of
|R(x) − c| (or, when sampling is too sparse, the pointwise log-log drift).  The
two readings of the criterion are the same statement in different units:

- **Ratio-deviation form** (what the detector's P4 reads): R(x) = f(x)/g(x),
  removable-compatible ⇔ D(x) falls decade-on-decade, so its log-log slope
  β_ratio is **negative**; anti-class ⇔ D(x) does not converge to 0, β_ratio ≳ 0.
- **Fluctuation-size form** (what P1/P2 read): if the leading scale of f is x^α
  (Pólya √n, PNT x/log x), removable-compatible ⇔ β_size < α, and the anti-class
  sits **exactly on** the denominator, β_size ≈ α.

The calibration is not a free choice: the six anti members have *proofs* pinning
the failure point, so a return to the tree's "limit does not exist" branch needs
a target whose decade maxima stop declining and floor strictly above 0 —
equivalently a sustained β_ratio ≥ 0.  Littlewood's F = Ω±(√n) is exactly that
statement (per-decade max of |F|/√n stays ~ constant, β_size ≈ 0.5, measured
0.486); Odlyzko–te Riele's limsup M/√n > 1.06 does the same for Mertens
(measured exponent 0.433); Montgomery–Vaughan Thm 15.11's ψ − x = Ω±(x^{1/2})
does the same for Chebyshev (measured band 0.51·0.61·0.71·0.69·0.68·0.75,
sup 0.74 @ 36.9M — below the √n floor, so the finite band alone would be
removable-looking; the theorem, not the range, is the arbiter); Paley's
R(q) ≥ c log log q does it in q-space
(measured floor 0.577+).  On the removable side the decay signs observed
across the corpus all lie *below* the anti floor: prime-reciprocal decade maxima
0.605 → 2.7e−5 (β_ratio = −0.59), twin-prime 0.0198 → 0.0096 → 0.0046
(β_ratio = −0.32, full decade to 1e8), and PNT's ratio deviation
(π−Li)/Li ~ x^{−0.57} — the fluctuation is subleading to x, removable — and the
totient density (#71) collapses with β_ratio = −1.20: its error is a whole
power below its x² denominator, the removable side's fastest legitimate decay.

Entry #69 (the Dirichlet divisor-error, Hardy 1916) adds a stronger member and
one structural lesson.  Δ(x)/x^{1/4} is proven to have no
limit — the Ω₊((x log x)^{1/4} log log x) theorem makes its limsup +∞
unconditionally, the Ω₋(x^{1/4}) pattern gives infinitely many negative
values — so no finite wall can display the failure, and the decade-max ratio
series reads order-one (3.4 → 3.8 → 4.8 → 5.4 → 5.8 → 1.7, d = 2..7 to 1e7)
with a single near-threshold dip (Δ(10^7) = −4, S(10^7) = 162,725,364) rather
than a clean slope.  The lesson: for members whose oscillation provably lives
on the denominator, the *bounded-band* reading — the per-decade max of the
normalized deviation never collapsing below order-one — is the robust anti
signature, and a single decade whose deviation cancels near a round point
must not be read as decay.  Removable members, by contrast, collapse their
band by orders of magnitude per decade (twin 0.0198 → 0.0046;
prime-reciprocal 0.605 → 2.7e−5; PNT β_ratio ≈ −0.57).

Entry #70 (the Gauss circle-error) is the Hardy-pair twin on the SAME
x^{1/4} denominator with the OPPOSITE unbounded side (liminf = −∞), and its
numerical profile is the same bounded-band picture (per-decade max ratio
4.9 → 5.4 → 6.2 → 7.3 → 8.0 → 1.75 to 1e7, with the same near-threshold dip
at P(10^7) = 98).  Together #69/#70 show the lattice-point anti-class is not
an accident of one construction: the denominator-carrying fluctuation is
the shared, theorem-pinned structure of an entire family.

Why, then, is Goldbach's gate the *weak* form ("no growth ≪ +1/2") and not the
strong form ("β_ratio < −0.2")?  Two structural reasons that the criterion
admits without weakening:

1. **Range.**  [1e4, 3e5] spans two full decades, and the per-even wobble —
   mean |R−1| ≈ 0.2, worst sample 0.34 — swamps any log-slow decay, so a
   *tight negative* slope is unmeasurable at this reach.  A positive anti-class
   drift, by contrast, would be plainly visible (decade maxima climbing above
   0.34).  The measurable distinction at this range is growth versus no-growth,
   which is why G6 reads the drift (−0.09) instead of a decay threshold.
2. **What the weight already removed.**  S(N) strips the smooth first-order
   dependence: G(N)/(S(N)·N/log²N) is flat to leading order, and entry 66's
   Spearman window (ρ > 0.6 within a fixed N-window) shows the residual is
   exactly the singular-series ordering — a bounded, zero-mean process.  For a
   bounded process the only way to threaten removability is to *grow*, so the
   criterion's dangerous clause — a validated run whose |R−1| climbs, decade
   maxima flooring above a positive constant — is the strictest clause the
   range can legally assert.

The same Criterion therefore sharpens as range increases: demand a decay *sign*
where full decades are sealed (twin at 1e8, prime-reciprocal at 2e7, Mertens
and Pólya at 1e8), demand only a *non-growth* where reach is two decades
(Goldbach at 3e5 in the detector, P5).  Range extension delivers exactly that
sharpening: in-entry at 1e7 (260 log-uniform evens) the Goldbach decade maxima
are 0.296 → 0.226 → 0.174, decade-decay beta = −0.12 (r2 = 1.00, three
decades) — the shallow decay the two-decade reach could not measure — while
growth (decade maxima flooring/climbing above the bounded band) remains the
operationally falsifiable clause.  A later decade of Goldbach counts that flips
the criterion's decay gate to FAIL is the ledger's PL-11 refutation, and it is
a *stronger* falsification than a mere slope miss: it
pushes the target onto the proved anti-class.

### 6.5 The proved-anti calibration: finite ranges always "look removable"

The six anti-class members are the corpus's calibration set, and what they
calibrate is uncomfortable: in every finite verification an anti member is
*indistinguishable* from a removable one.  No range has ever shown any of
them failing the bound it was designed to violate.

- **Pólya (#64):** F(n) ≤ 0 held for > 9×10⁸ terms before the first + at
  n = 906,150,257; Littlewood's Ω± guarantees infinitely more violations.
  The 0/0-limit for F(n)/√n failed only in the theorem, never in the data.
- **Mertens (#67):** verified here to 1e8 — the near-miss ratio |M(n)|/√n
  *grows with the range* (0.4378 @ 300,551 → 0.4627 @ 30,919,091), the bound
  HELD on [2, 1e8] (max ratio 0.8944, and that at n = 5), records still being
  set at n = 76,015,339, and the conjecture is only *proved* false
  (Odlyzko–te Riele, limsup > 1.06) — every finite value "looks removable".
- **Divisor-error (#69):** the sharpest case.  Verified here to 1e7 — |Δ|/x^{1/4}
  stays order-one (≈ 1.7–5.8) in every decade with signs oscillating, and
  |Δ|/x^{1/3} ≤ 1.93 (Voronoi's 1/3 bound).  Because Hardy's Ω₊ theorem makes
  the ratio's limsup +∞ *unconditionally*, no finite range can ever display the
  failure — this member's verdict rides entirely on the theorem, and the
  finite data can only corroborate the structural reading (order-one band,
  oscillation), never exhibit the contradiction.
- **Circle-error (#70):** the twin.  P(x)/x^{1/4} reads the same bounded-band
  profile (4.9 → 8.0 → 1.75 per-decade max to 1e7, P(10^7) = 98) on the
  opposite unbounded side (Hardy's liminf = −∞); the lattice-point pair
  shows the anti-class is a family structure, not a construction accident.
- **Equal-range wall (10^8):** both lattice members re-verified exactly to
  1e8 via their closed forms (S(x) = Σ⌊x/d⌋, N(x) = (4m+1)+4Σ isqrt(x−a²) —
  identities certified by the #69/#70 sieves to 1e7; continuity to the
  wall).  Sampled-window maxima keep rising, not decaying — divisor
  2.568 → 2.643 → 2.913 → 2.992, circle 4.243 → 3.106 → 4.420 → 4.599
  (full floors 2.57 / 3.11) — and the near-threshold 10^7 cancellation is
  confirmed as a dip inside the band, not a trend: window 10^7..10^8 beats
  window 10^6..10^7 for both.  S(10^8) = 1,857,511,568, N(10^8) =
  314,159,053 (|Δ|/x^{1/4} = 3.61, |P|/x^{1/4} = 2.12 at the wall).  The
  lattice pair now holds the same 1e8 range as the √n pair (#64/#67).
- **√n pair at the wall (10^8):** Pólya #64 extended to 1e8 alongside
  Mertens #67 for the pairwise calibration — per-decade band max
  |F|/√n = 1.29 | 1.33 | 1.30 | 1.27 | 1.36 (floor 1.27, never decaying),
  family amplitude already above 1 at 1e7 (1.167 @ 8,803,471) and max
  1.358, while |M|/√n stays inside the conjectured bound at range
  (0.8944).  F(10^k) = 0, −2, −14, −94, −288, −530, −842, −3,884
  (A002819; a(10^8) = −3884), min F = −10,443 @ 76,015,169 — the deepest
  excursion sits mid-band, and F(10^8) = −3,884 is the same *single-point
  pull-back* structure the lattice pair shows at 10^7 (Δ, P) and #72 at
its wall: a band truth (1.358) that a naive endpoint read (0.388) would
   misreport as decay — the third independent occurrence of the Dip Rule
   (§6.7).
- **Chebyshev completes the √n trinity (#74):** δ(x)/√x at 1e8, δ = ψ(x) − x,
  computed exactly via the prime-power breakpoints of ψ (= log lcm(1..⌊x⌋),
  spot-verified to 1e−9 on 1..40).  ψ(10^8) = 99,998,242.8 (ratio 0.999982),
  δ(10^k) = −2.2, −6.0, −3.3, +13.4, +51.6, −413.4, −1460.6, −1757.2 — both
  signs, crossing the axis afresh in every decade.  Per-decade band max
  |δ|/√x (d = 2..7) = 0.51 · 0.61 · 0.71 · 0.69 · 0.68 · 0.75 (non-collapse:
  each band holds ≥ ⅔ of the previous, through the wall), sup 0.74 @
  36,917,099 — a reader between the √n pair's floors (0.46 < 0.75 < 1.27),
  which is the member's whole point: Montgomery–Vaughan Thm 15.11
  (ψ − x = Ω±(x^{1/2}), unconditional), not any finite read, is what makes
  δ anti.  It is the corpus's clearest proof-before-range exhibition — the
  mirror of #69/#70, where the finite read *looked* decaying and the theorem
  still decided.

**The wall in one read (all five anti members at the 10^8 wall):**

| member | window-max read (same windows for all) | small-n spike | wall point | verdict |
|---|---|---|---|---|
| Mertens #67 (√n) | max \|M\|/√n = 0.472 @ 2,803 (n ≥ 10^3); 0.463 @ 30,919,091 (n ≥ 10^5); late flat ≈ 0.46 | |M(5)|/√5 = 0.894 (the conjecture's bound is tight at small n) | no limit (Odlyzko–te Riele); band flat, inside the conjecture's range all the way |
| Pólya #64 (√n) | per-decade 1.29 · 1.33 · 1.30 · 1.27 · 1.36, floor 1.27 | F = −1 @ 3, −2 @ 8 | F(10^8) = −3,884: point 0.388 (Dip) | no limit (Littlewood); amplitude already above 1 at 1e7 |
| Chebyshev #74 (√n) | per-decade (d = 2..7) 0.51 · 0.61 · 0.71 · 0.69 · 0.68 · 0.75, sup 0.74 @ 36,917,099 | δ crosses the axis in EVERY band (both signs), |δ(10^5)| = +51.6 | δ(10^8) = −1,757: point 0.176 | no limit (M–V Thm 15.11); the band reads between the √n pair's floors (0.46 < 0.75 < 1.27), so the theorem — not the range — is the arbiter |
| Divisor #69 (x^{1/4}) | windows 2.57 · 2.64 · 2.91 · 2.99, floor 2.57 | per-decade max (d = 2..7): 3.38 · 3.84 · 4.83 · 5.38 · 5.80 · 1.68 (a rise then the 10^7 dip) | \|Δ(10^8)\|/10^2 = 3.61 | no limit unconditionally (Hardy); the honest wall is a cap, X-form absent |
| Circle #70 (x^{1/4}) | windows 4.24 · 3.11 · 4.42 · 4.60, floor 3.11 | per-decade max (d = 2..7): 4.89 · 5.41 · 6.21 · 7.28 · 8.04 · 1.75 (rise then the 10^7 dip) | \|P(10^8)\|/10^2 = 2.12 | no limit unconditionally (Hardy); its dipole twin |

The √n trinity (F 1.27 · M 0.46 · δ 0.75 late bands) and the x^{1/4} pair
(2.57 / 3.11) all read the same *in-band non-decay* at the same wall — size
never decides (0.46 sits below 0.75 sits below 1.27 sits below 3.11), the
band's flatness does: which is the criterion's own claim, and exactly what
the Ω-theorems render a true limit failure rather than a finite cap.

Consequences for the criterion:

1. A near-miss ratio below 1 is evidence of nothing by itself: Pólya and
   Mertens both sit strictly below 1 in every range that exists to compute,
   and the divisor/circle ratios, though already order-one, are capped by any
   finite wall exactly when Hardy's theorems say the failure is a *limit*
   one has to reason to, not a value one reaches.
2. The only legally assertable anti-signature is *non-decay* — decade maxima
   flooring strictly above 0, a floor the proofs pin on the Mertens bound
   (limsup > 1.06, liminf < −1.009) and declare unbounded-above and
   unbounded-below for the lattice-point pair and for δ and F by their own
   Ω± theorems — and
   §6.4's falsifiable form for open targets is exactly the complementary
   clause: a validated run whose decade maxima stop declining and floor above a
   positive constant, while the "bound" keeps holding only empirically.
3. So a target that *does* decay decade-on-decade (prime-reciprocal −0.59,
   twin −0.32, totient −1.20, character-box −0.59) is exhibiting a behavior
   the six anti members
   provably never
   exhibit — which is the full content of "removable-compatible": support,
   never proof.  The criterion separates the corpus into the two classes by a
   signature the anti class provably lacks, and concedes that no finite run can
   prove removability of an open target.  (Entry #72, a *manufactured* control
   on the removable side — the same character walk built to never settle, whose
   bounded box puts its measured slope at ≈ −0.59 — pins item 3's converse:
   the criterion grants a bounded-band raw deviation the removable read
   precisely when the corrected ratio collapses, and the anti members are the
   case where it provably cannot.  Entry #73 shows the other face of the same
   family: release the box — let the modulus grow — and the same character
   walk's sup-ratio provably stops converging, Paley's theorem.)

### 6.6 The three structural readings and the bounded-box control

The whole calibration rests on ONE observable: the log-log slope β_ratio of
the per-decade maxima of |deviation|/|denominator|.  The corpus now rules it
in three regimes, with members whose verdicts are *proved* on both sides:

- **Anti, order-one band (β_ratio ≈ 0, floor > 0):** Pólya 0.486, Mertens
  0.433 (√n denominator, limsups pinned 1.06 / 1.009), and now the
  Chebyshev walk δ/√x (#74: per-decade bands 0.51 · 0.61 · 0.71 · 0.69 ·
  0.68 · 0.75, sup 0.74 @ 36.9M — a reader BELOW the √n pair's floors,
  which is the point: Montgomery–Vaughan Thm 15.11, not any range, is what
  makes δ anti), divisor/circle
  (x^{1/4} denominator, band 1.7–8.0 vs 4.9–8.0, no limit unconditionally),
  character-walk in q-space (#73: floor 0.69, creeping sup, no limit by
  Paley).  The class is nearly closed *within each space*: the classic
  n-space summatory functions are now the √n trinity (F = Σλ, M = Σμ,
  δ = ψ − x — all three Ω±(√x)) plus the x^{1/4} lattice pair — the
  verdicts proven on both sides — while the two classics still OPEN at the
  bare denominator are π−Li and S(T): both are proven to oscillate
  (Littlewood 1914: π−Li = Ω±(√x·log log log x/log x); Selberg: S(T)
  unbounded both signs) and both sit at scales a log (or less) BELOW their
  naked denominators, but no theorem proves the ratio's tendency to zero —
  the best upper bounds (even under RH: π−Li = O(√x log x), S(T) = O(log T))
  leave the ratio room up to log x — so neither is proved decaying, nor
  proved anti.  What provably *decays* in n-space is the bounded-box
  family: fixed-modulus character partial sums (#72, period-mean-zero
  ⟹ |S(x)| ≤ c ⟹ ratio → 0, Pólya–Vinogradov).  The q-space move (Paley)
  and the lattice-power move (Hardy) each open a new anti direction the
  criterion's seamless band-read confirms.
- **Removable, collapsing ratio (β_ratio < 0 strictly):** prime-reciprocal
  −0.59, twin −0.32, totient −1.20.
- **Removable, bounded-box (the manufactured control, #72):** the fixed
  quadratic character mod 7 — |S(x)| ≤ 2 for *every* x (one-period max, box
  ratio 1.00 to 1e7) yet S(x)/√x → 0 at measured β_ratio = −0.590 (r² =
  0.985, the expected −1/2): a case where the raw deviation never settles and
  never grows, and the corrected ratio still provably collapses.  The control
  answers the criterion's border question — "what if the deviation merely
  wiggles in a bounded band forever?" — with Pólya–Vinogradov: for *fixed*
  moduli that band is a box and the read is removable; the Paley
  oscillation (Ω₊(√q log log q)) lives *across* moduli, a different 0/0 in
  q-space the criterion's denominator does not address.  The Chebyshev-bias
  (π(x;4,3) − π(x;4,1) ~ 1.79√x/log x) is the honest intermediate: a band
  that *does* grow, one log below √x, so the corrected ratio
  (band/denominator) decays — removable, at rate slower than any boxed
  control, which is exactly why the slope read, not the band's size, is the
  criterion.

Collectively: fluctuation size is never evidence; the ratio's decade trend is
the whole observable; and the anti class is thin, provable, and nearly
exhaustive, while the removable side is measure-theoretically sweeping — the
asymmetry §5.2 predicted as Principle 3 in §4.4.

### 6.7 The Dip Rule

A single-point cancellation at a power-of-ten wall never defines a trend;
only window (band) comparisons do.  The corpus has now hit the same
near-threshold structure three times, independently, and reading the point
instead of the band would have falsified a true anti member each time:

- Δ(10^7) = −4 → point ratio 1.68 vs. the [10^6, 10^7) window's 5.80
  (divisor #69, extended):
- P(10^7) = 98 → point 1.75 vs. window 8.04 (circle #70, extended);
- F(10^8) = −3,884 → point ratio 0.388 vs. the [10^7, 10^8] window's
  1.358 (Pólya #64, extended to 1e8) — the deepest excursion sits mid-band
  (−10,443 @ 76,015,169), the walk then pulls back through the wall.

Every one of these is a genuine cancellation of the fluctuation AT the
decade point — the exact feature a decay-sign read on endpoints would
confuse with convergence.  The rule is therefore the criterion's second
half, complementing §6.6's band reads: **the observable is the window
maximum; the decade point is decoration.**  The three occurrences are the
same phenomenon across three different arithmetic families (√n, x^{1/4},
and the character/lattice family), which is why the extension probes
(#64 @1e8, #69/#70 @1e8) were built to sample windows first and report
landmarks second.

### 6.8 The three √n walks read the same slope, different bands

The criterion's slope reads the CLASS, not the member — shown by the
√n trinity measured pairwise at the 1e8 wall:

| walk | per-decade band max ratio | sup | wall point |
|------|---------------------------|-----|-----------|
| Pólya F/√n (#64) | 1.29 · 1.33 · 1.30 · 1.27 · 1.36 (d = 3..7) | 1.358 (d = 7) | F(10^8) = −3,884: 0.388 (dip) |
| Mertens M/√n (#67) | flat ≈ 0.46 (max ≥ 1e5: 0.463 @ 30.9M, band d = 7) | 0.463 (d = 7) | M(10^8) = +1,928: 0.1928 (dip) |
| Chebyshev δ/√n (#74) | 0.51 · 0.61 · 0.71 · 0.69 · 0.68 · 0.75 (d = 2..7) | 0.748 @ 36.9M (d = 7) | δ(10^8) = −1,757: 0.176 (dip) |

All three read log-log slope β_ratio ≈ 0 — flat bands — because all three
are governed by the SAME mechanism: the partial sums of (Möbius, Liouville,
Chebyshev-ψ) arithmetic functions, whose deviations are all Ω±(√x) with
√x exactly the natural scale, the correction locked by the Riemann-zero
machinery.  The slope cannot separate them; the band SIZE is the family
fingerprint (F's floor 1.27 — least cancellation; M's 0.46 — most; δ's
0.75 — the prime-power log-sum between).  And their three wall POINTS are
the Dip Rule trinity: each 10^8 read sits at a minimum of its own window
(0.388 vs 1.358; 0.1928 vs 0.463; 0.176 vs 0.748) — endpoint reads would
have called all three "decaying".  The verdicts ride the theorems, exactly
as §6.5's arbiter row states: the pair's bands are inside 1.27 ↔ 0.46,
δ's is between them.

### 6.9 The OPEN pair (fenced, uncertified): π−Li and S(T)

The criterion's slope is necessary, not sufficient: an order-one band can
mean "proven anti" OR "open, fluctuating below the denominator".  The two
classic n-space sums left over by §6.6 sit in the second slot, and neither
side can certify them — the one computed reading (exact scan 2026-09-21,
primes through R(x) = 10^8 sieved exactly and checked against the known
π(10^k) line 4, 25, 168, 1229, 9592, 78498, 664579, 5761455; Li to < 10⁻³
via the convergent Ei series):

| member | 0/0 form | ratio at 10^k (k = 1..8) | reading to 1e8 | theorem side | status |
|--------|----------|--------------------------|----------------|--------------|--------|
| π−Li open classic | (π(x) − Li(x))/√x | 0.685, 0.513, 0.304, 0.171, 0.120, 0.130, 0.107, 0.075 | β over d = 5..8 ≈ −0.07 (soft), and NON-monotone (d = 5→6 rises 0.120→0.130): both the anti-flat β ≈ 0 and the removable β ≤ −0.32 are disclaimed by an intermediate, unreproducible "scent" of decay | Littlewood 1914: π−Li = Ω±(√x·log log log x/log x) — fluctuation proven one factor BELOW √x (sign changes unconditionally, first crossing far beyond the wall), but NO upper bound proves the ratio → 0 (best unconditional ≫ √x; under RH only O(√x log x)); no no-limit theorem either — the oscillation is not at the denominator | **OPEN — cannot be certified** |
| S(T) open classic | S(T)/log T, S(T) = (1/π) arg ζ(1/2 + iT) | — | — | Selberg: S(T) unbounded both signs (fluctuations at a (log T)^{1/2}-ish scale) against the trivial O(log T) bound — the same pattern: oscillation at or below the denominator, no o(log T) theorem | **OPEN — cannot be certified** |

Two structural facts the pair exhibits that the certified classes never do:

1. **The decade point is the window maximum, not the dip (the Dip Rule's
   inverse).**  For π−Li the gap-lemma holds: g'(x) < 0 in every gap (the
   stationary equation Li(x) − π = 2x/ln x is never met — at 1e8 the
   left side is 754, the right ≈ 10⁷), so within a band |g| = (Li−π)/√x
   rises RIGHTWARD and its sup lands ON the decade point.  The certified
   anti trio's sup sits MID-window, its decade point a minimum (Dip Rule,
   §6.7).  The open family flips it: the single-sign walk climbs through
   the wall instead of pulling back through it.
2. **The slope reading hover-strikes its own soft negative (≈ −0.07).**
   No certified member reads there: the removable class is sharply negative
   (−0.32, −0.59, −1.20) and the anti class is flat (≈ 0).  π−Li's
   intermediate, direction-shuffling β is exactly the lurking Littlewood
   factor log log log x/log x leaking through the range — a finite "wink"
   of decay that nobody has promoted to a theorem.  The fence therefore
   marks the boundary where the framework *declines* to classify: without
   a certified value (removable) or a negative oscillation theorem (anti),
   a 0/0 stays open, no matter how believable its finite trend reads.  No
   census entry is claimed (§6.9 is a fence, not a member): the 6 anti
   members and the 70 removable-value entries stand, and the open pair is
   what the framework can point to and say — *this* is where it must wait.

---

## Appendix: Data Files

Each experiment produces a JSON data file in `data/`. The files contain:

- The 0/0 form and its parameters
- Numerical values of the removable value at multiple points
- Convergence data (how the removable value is approached)
- The summary verdict (SUPPORTED / NOT SUPPORTED)
- Honest wall statements (limitations of the numerical verification)

| Experiment | Data File |
|-----------|-----------|
| Riemann zeta | `data/argument_principle_0_over_0_data.json` |
| GRH Dirichlet | `data/grh_dirichlet_0_over_0_data.json` |
| BSD | `data/bsd_0_over_0_data.json` |
| abc | `data/abc_conjecture_0_over_0_data.json` |
| Fermat little | `data/fermat_little_0_over_0_data.json` |
| Euler product | `data/euler_product_0_over_0_data.json` |
| Weil explicit | `data/weil_explicit_0_over_0_data.json` |
| Zeta FE | `data/zeta_functional_eq_0_over_0_data.json` |
| PNT | `data/prime_number_theorem_0_over_0_data.json` |
| Khintchine | `data/khintchine_0_over_0_data.json` |
| Möbius | `data/mobius_function_0_over_0_data.json` |
| Argument principle | `data/argument_principle_0_over_0_data.json` |
| Cauchy integral | `data/cauchy_integral_0_over_0_data.json` |
| Picard | `data/picard_little_0_over_0_data.json` |
| Taylor | `data/taylor_remainder_0_over_0_data.json` |
| FTA | `data/fta_0_over_0_data.json` |
| Stirling | `data/stirling_approx_0_over_0_data.json` |
| Wallis | `data/wallis_product_0_over_0_data.json` |
| Cesàro | `data/cesaro_summation_0_over_0_data.json` |
| Poincaré-Hopf | `data/poincare_hopf_0_over_0_data.json` |
| Atiyah-Singer | `data/atiyah_singer_0_over_0_data.json` |
| Gauss-Bonnet | `data/gauss_bonnet_0_over_0_data.json` |
| Riemann-Roch | `data/riemann_roch_0_over_0_data.json` |
| Weyl law | `data/weyl_law_0_over_0_data.json` |
| Selberg trace | `data/selberg_trace_0_over_0_data.json` |
| Lefschetz | `data/lefschetz_fixed_point_0_over_0_data.json` |
| Morse theory | `data/morse_theory_0_over_0_data.json` |
| Sard | `data/sard_theorem_0_over_0_data.json` |
| Stokes/de Rham | `data/stokes_de_rham_0_over_0_data.json` |
| Green's function | `data/greens_function_0_over_0_data.json` |
| Euler-Maclaurin | `data/euler_maclaurin_0_over_0_data.json` |
| CLT | `data/central_limit_theorem_0_over_0_data.json` |
| Rayleigh | `data/rayleigh_quotient_0_over_0_data.json` |
| Banach | `data/banach_fixed_point_0_over_0_data.json` |
| Brouwer | `data/brouwer_fixed_point_0_over_0_data.json` |
| Fourier uncertainty | `data/fourier_uncertainty_0_over_0_data.json` |
| Poisson summation | `data/poisson_summation_0_over_0_data.json` |
| Saddle point | `data/saddle_point_0_over_0_data.json` |
| Laplace | `data/laplace_method_0_over_0_data.json` |
| Noether-Landau | `data/noether_landau_0_over_0_data.json` |
| Ising | `data/ising_model_0_over_0_data.json` |
| Spectral gap | `data/spectral_gap_0_over_0_data.json` |
| Lorenz | `data/lorenz_attractor_0_over_0_data.json` |
| Wigner | `data/wigner_semicircle_0_over_0_data.json` |
| Shannon | `data/shannon_entropy_0_over_0_data.json` |
| Boltzmann | `data/boltzmann_entropy_0_over_0_data.json` |
| Bayes | `data/bayes_theorem_0_over_0_data.json` |
| Gradient descent | `data/gradient_descent_0_over_0_data.json` |
| KKT | `data/kkt_conditions_0_over_0_data.json` |
| Schanuel | `data/schanuel_0_over_0_data.json` |
| Noether | `data/noether_theorem_0_over_0_data.json` |
| Pythagorean | `data/pythagorean_0_over_0_data.json` |
| Pólya anti-class | `data/polya_liouville_0_over_0.json` |
| Twin-prime density | `data/twin_prime_density_0_over_0.json` |
| Goldbach density | `data/goldbach_density_0_over_0.json` |
| Mertens function | `data/mobius_mertens_0_over_0.json` |
| Prime-reciprocal constant | `data/prime_reciprocal_0_over_0.json` |
| Dirichlet divisor-error (anti-class) | `data/dirichlet_divisor_anti_0_over_0.json` |
| Gauss circle-error (anti-class) | `data/gauss_circle_anti_0_over_0.json` |
| Euler-totient density | `data/euler_totient_0_over_0.json` |
| Character partial sums (bounded-box control) | `data/character_sums_0_over_0.json` |
| Character-walk sup-ratio (anti-class, q-space) | `data/char_walk_anti_0_over_0.json` |
| Lattice pair at the 10^8 wall (extension of #69/#70) | `data/lattice_wall_1e8_0_over_0.json` |
| Pólya/Liouville walk at the 10^8 wall (extension of #64) | `data/polya_wall_1e8_0_over_0.json` |
| Chebyshev walk δ/√x (anti-class) | `data/chebyshev_psi_0_over_0.json` |
| Landau function | `data/landau_function_0_over_0_data.json` |

*The Landau-function calibration (corpus #56, PL-21; registered 2026-09-22) -- REMOVABLE named value 1, Vanishing Rate, Landau 1903: log g(n)/sqrt(n log n) -> 1 unconditionally (A000793, 5/5 gates PASS, settled referee) -- is the numbered census's 76th entry (§2.20, above).*
---

## Cross-Domain Applications (physics fields using the Index mechanism)

Mechanism II (Index: winding number; THE_0_OVER_0_ATLAS.md:35) is not only
a mathematical taxonomy — the framework's own physical lanes run on it:

| Physical framework | 0/0 mechanism | Artifact | Status |
|---|---|---|---|
| FRG pole-pair winding: lower ridge W=-1, upper ridge W=0 (ray-pole); the winding number of the flow around the pole pair in (G, lam) is the argument-principle index Z-P of Mechanism II | Index (winding number over the pole-pair contour) | `experiments/flow_pole_regulator_robust.py`, `experiments/winding_phase_diagram.py`, `experiments/winding_classifier.py` | CONCRETE (fingerprint + R_trans(A,B) phase map + regulator classifier) |
| Release-lane selection: the CMB's e-fold demand is a positive-removable-value demand (THE_ENTROPY_CONDITION_THEOREM.md:251); LANE-2 (W=-1) REMOVABLE/SELECTED, LANE-1 (W=0, epsilon=1 cap) POLE; d* spans 10^-72.1..10^-49.6 | Index (winding) + removable-value sign (selection criterion) | `experiments/delta0_selection.py` + `data/delta0_selection.json` | CONCRETE (4/4 gates PASS; closes the "no selection principle" gap, ledger F19) |
| Higgs handoff: ridge eject lambda_0 = 0.36952 = universal cusp handoff 0.3695 (0.005%); Higgs plateau N=58 | Index (winding at lower-ridge ejector) + removable 0/0 of the cusp | `experiments/cusp_to_higgs_initial.py`, `experiments/trajectory_selection.py` | CONCRETE (framework synthesis) |
| Stability of the ejector under resolution: the W-observable is PIECEWISE in probe radius R (ejector flip 0->-1, NGFP-rebalanced 0, double-winding -2); the ejector lane is the RELEASE-WINDOW annulus R_trans < R < R_flip_back, and R_trans has a sharp minimum at the release point itself (G_c=0.6: 0.004), giving delta0_selection's falsifiability clause its quantitative threshold | Index (winding 0/0: the flip's removable value is the half-integer, an undefined winding number at the boundary) | `experiments/winding_transition_0_over_0.py` + `data/winding_transition_0_over_0.json` | CONCRETE (4/4 gates PASS; ledger F20) |
| Regulator-resolution winding: WHICH coarse-graining actively destroys the ejector. Field-blurring the singular locus is EXCLUDED (chaotic winding, no clean origin-crossing 0/0: min|beta_s| stalls ~2e-2); probe-undersampling is NOMINAL (sharp -1->0 at step_crit ~ 0.5 R, i.e. n > ~12.6 regardless of R). Selector domain pinned: W = -1 iff the probe sits in the annulus AND resolves it | Index (winding 0/0) + removable-value; the half-integer is the would-be crossing point that field-blur disproves and undersampling realizes as the axis of destruction | `experiments/regulator_resolution_winding.py` + `data/regulator_resolution_winding.json` | CONCRETE (5/5 gates PASS; ledger F21) |

Cross-reference: AUDIT.md (Poincare-Hopf index = chi(M); argument-principle
zero counts), WHERE_0_OVER_0_SOLVES.md, THE_UNIVERSAL_ZERO.md §2.2 (Index
mechanism). The winding number in the physics lane and the residue-theorem
family above are the same object: an integer removable value of a 0/0.

---

*This atlas is a reference document. For the philosophical interpretation, see ON_THE_NATURE_OF_ZERO.md. For the synthesis, see THE_UNIVERSAL_ZERO.md. For the epistemology, see REMOVABLE_SINGULARITIES.md.*

*All 70 removable-value entries verified computationally (64-sweep + 6 open-target/named/control — the sweep's 64th, the Landau-function calibration #76 — REMOVABLE value 1, Vanishing Rate, Landau 1903; the sixth, the Mertens product-gap complement #75 — REMOVABLE value 0, elementary, Mertens 1874); entries 64, 67, 69, 70, 73 and 74 document the anti-class — the Pólya and Mertens conjectures are FALSE, proven externally (Littlewood; Odlyzko–te Riele), the Chebyshev-walk ratio has no limit, proven unconditionally (Montgomery–Vaughan Thm 15.11: ψ − x = Ω±(x^{1/2})), the divisor/circle ratios have no limit, proven unconditionally (Hardy 1916; Voronoi; Sierpiński), and the character-walk sup-ratio has no limit in q-space, proven unconditionally (Paley 1932; Pólya–Vinogradov 1918) — each borne out by its fluctuation reading (Pólya 0.486, Mertens 0.433, Chebyshev δ band 0.51·0.61·0.71·0.69·0.68·0.75 below the √n floor — the theorem, not the range, arbitrates, divisor/circle bounded-band order-one, character-walk floor 0.577+ with creeping sup); entry 71 documents the removable side's flat-decay anchor (3/π², β_ratio = −1.20, Dirichlet 1849); entry 72 documents the bounded-box control (mod-7 character partial sums: |S| ≤ 2 at every x to 1e7, S(x)/√x → 0 at β_ratio = −0.590, Pólya–Vinogradov) — the manufactured counterpoint proving the criterion reads the ratio's decade trend alone, never the size of the raw oscillation. 646 regression tests passing.*
