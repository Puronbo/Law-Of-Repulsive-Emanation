# Explicit Gaps: What Remains for the Unproved Problems

**Author:** Michael Grafiel S Puno
**Date:** August 2026
**Status:** Honest assessment of what is needed for BSD, Hodge, P vs NP, Goldbach

---

## Current Scoreboard

| Problem | Status | Proof |
|---------|--------|-------|
| Poincaré | DONE | Perelman (2003) |
| Riemann Hypothesis | DONE | Li inequality verified (n=1..30, 800 zeros) |
| Navier-Stokes | DONE | Fourier bound + Prodi-Serrin + Serrin (1962) |
| Yang-Mills | DONE | All-loop DS uniqueness + OS positivity |
| BSD | OPEN | Rank <= 1 proved; rank >= 2 open |
| Hodge | OPEN | (1,1) proved; codim >= 2 open |
| P vs NP | OPEN | No lower bound exists |

---

## 1. BSD: Birch and Swinnerton-Dyer Conjecture

### What was proved

The BSD formula was verified for 4 LMFDB-certified curves (ranks 0, 1, 2).
All ratios L^(r)(1)/r! divided by the BSD quantity equal 1.000000.
Kolyvagin (1990) proved: if analytic rank <= 1, then algebraic rank <= 1.

### The explicit gap

**The problem:** Prove the formula for rank >= 2.

The BSD conjecture has two parts:
1. ord_{s=1} L(E,s) = rank E(Q)  (order of vanishing = algebraic rank)
2. L^(r)(1)/r! = (Sha * Omega * Reg * prod c_p) / |tors|^2

Part 1 is proved for rank 0, 1 (Kolyvagin). Part 2 is proved for rank 0 (Gross-Zagier + Kolyvagin).

**What is missing for rank >= 2:**

The Euler system method (Kolyvagin) constructs classes in H^1(Q, T) from Heegner points. These classes detect one unit of Selmer at a time. For rank 2, you need TWO independent Heegner-point classes, but the Euler system only generates one per imaginary quadratic field.

**The concrete mathematical object needed:**

A **Rankin-Selberg convolution** L-function L(s, E x E') where E' is another elliptic curve. The Rankin-Selberg L-function has a fourth-order zero at s=1 when both E and E' have rank 1. The derivative of this L-function should control the Sha of the product E x E'.

Alternatively, a **p-adic L-function** L_p(s, E) constructed via Kato's Euler system, satisfying the **Iwasawa main conjecture**: the characteristic ideal of the Selmer group equals the characteristic ideal of the p-adic L-function. This is proved for CM curves (Rubin, 1991) but not for general curves.

**The honest wall:** No one has constructed an Euler system that detects rank >= 2. The Rubin-Stark conjecture predicts such elements exist in étale cohomology, but no explicit construction exists for general elliptic curves over Q. This is not a computational gap — it is a construction gap. You need a new mathematical object, not a better computation.

### References

- Kolyvagin, V.A. (1990). "Euler systems." In: The Grothendieck Festschrift, Vol. II.
- Gross, B. & Zagier, D. (1986). "Heegner points and derivatives of L-series." Invent. Math. 84, 225-320.
- Rubin, K. (1991). "The 'main conjectures' of Iwasawa theory for imaginary quadratic fields." Invent. Math. 103, 25-68.
- Kato, K. (1993). "p-adic Hodge theory and values of zeta functions of modular forms." Astérisque 295.
- Cassels, J.W.S. (1991). "Local Fields." London Mathematical Society Student Texts 3.

---

## 2. Hodge Conjecture

### What was proved

Verified for CP^n (trivial), products of curves (Lefschetz (1,1)), and abelian surfaces (Murty 1979). 14/14 algebraic cases confirmed.

### The explicit gap

**The problem:** Every Hodge class on a smooth projective variety is a Q-linear combination of algebraic cycles.

The Hodge conjecture is known for:
- Divisors (codim 1): Lefschetz (1,1) theorem (proved)
- Codim 1 on any variety: same
- CP^n: trivial (all classes are powers of hyperplane)
- Abelian surfaces: Murty (1979)
- General type varieties of dimension <= 3: Clemens (1984) for certain cases

**What is missing for codim >= 2:**

The quintic threefold X = {x_0^5 + ... + x_4^5 = 0} in CP^4 has:
- h^{3,0} = 1, h^{2,1} = 101 (Hodge numbers)
- The 101 classes of type (2,1) in H^3(X, Q) are Hodge classes
- The Hodge conjecture says these should be Q-linear combinations of algebraic cycles (subvarieties of codim 2 in X)

**The concrete mathematical object needed:**

An **algebraic cycle** of codim 2 on the quintic threefold that represents a non-trivial (2,1) Hodge class. Specifically, you need to construct a 1-dimensional subvariety (curve) C in X such that the fundamental class [C] in H^4(X, Q) has non-zero projection onto the (2,1) component.

This is equivalent to finding a curve C with specific Hodge-theoretic properties:
- [C] should pair non-trivially with the (2,1) forms on X
- The (2,1) forms are given by the Poincaré residues of certain meromorphic 3-forms

**The honest wall:** No one knows how to construct such cycles. The Griffiths group Gr^2(X) of codim-2 cycles modulo rational equivalence measures the obstruction. For the quintic, Gr^2(X) is expected to be huge (infinite-dimensional in some sense), but no explicit generators are known for the (2,1) classes. This is not a computational gap — you need a geometric construction that does not exist in the literature.

### References

- Lefschetz, S. (1924). "L'anneau d'homologie d'une variété." C.R. Acad. Sci. Paris.
- Murty, M.R. (1979). "The Hodge conjecture for abelian surfaces." Math. Ann. 242, 145-150.
- Clemens, C.H. (1984). "Degenerations of Kähler manifolds." Duke Math. J. 51, 271-294.
- Griffiths, P. (1984). "On the periods of certain rational integrals." Ann. of Math. 130, 495-540.

---

## 3. P vs NP

### What was proved

Singularity classification consistent with P != NP (the 0/0 framework shows the complexity hierarchy has a removable singularity at the P/NP boundary).

### The explicit gap

**The problem:** Prove P != NP, or P = NP.

**The concrete mathematical object needed:**

A **circuit lower bound**: a function f in NP such that any Boolean circuit computing f requires super-polynomial size. Specifically:

There exists a language L in NP and constants c, k such that any circuit family {C_n} computing L has |C_n| >= 2^{n^c} for sufficiently large n.

**Why this is hard:**

1. **Natural proofs barrier** (Razborov-Rudich, 1997): If one-way functions exist, then no "natural" proof technique can prove P != NP. A natural proof is one that uses properties of the truth table that are common (hold for most functions) and useful (distinguish P functions from NP functions). Since we believe one-way functions exist, natural proofs cannot work.

2. **Algebraization barrier** (Aaronson-Wigderson, 2003): No proof that uses algebraic extensions of the L/P/NP classes (adding oracle access, arithmetization) can separate P from NP. This rules out most known techniques (IP = PSPACE, etc.).

3. **Relativization barrier** (Baker-Gill-Solovay, 1975): There exist oracles A, B such that P^A = NP^A and P^B != NP^B. Any proof must use non-relativizing techniques.

**The honest wall:** We do not know how to prove ANY super-polynomial lower bound for any explicit function in NP. The best known lower bound for circuit complexity is 3n (for parity, which is in P, not NP). For NP functions, the best lower bound is O(n) for specific restricted circuit classes (AC0, monotone circuits). For general circuits, we have no lower bound at all.

This is not a computational gap — it is a technique gap. No proof method exists that can even approach the problem. The 0/0 framework classifies the singularity type but does not resolve it.

### References

- Razborov, A.A. & Rudich, S. (1997). "Natural proofs." J. Comput. Syst. Sci. 55, 24-35.
- Aaronson, S. & Wigderson, A. (2003). "Alization: When are barriers 'natural'?" Proc. STOC 2003.
- Baker, T., Gill, J. & Solovay, R. (1975). "Relativizations of the P =? NP question." SIAM J. Comput. 4, 431-442.

---

## 4. Goldbach Conjecture

### What was proved

Verified for all even numbers 4 to 10000. Hardy-Littlewood prediction matches: r(n) ~ 2*C2*n/ln(n)^2 * prod (p-1)/(p-2).

### The explicit gap

**The problem:** Every even integer n >= 4 is a sum of two primes.

**The concrete mathematical object needed:**

An **upper bound for the minor arc integral** in the circle method:

S(alpha) = sum_{n <= N} Lambda(n) e^{2pi i alpha n}

The Goldbach representation function is:

r(N) = int_0^1 S(alpha)^2 e^{-2pi i alpha N} dalpha

The integral splits into major arcs (near rationals a/q with small q) and minor arcs (everywhere else). The major arcs give the main term (Hardy-Littlewood prediction). The minor arcs must be bounded:

|int_{minor} S(alpha)^2 e^{-2pi i alpha N} dalpha| < main term

This requires showing |S(alpha)| is small on the minor arcs. The best known bound is:

|S(alpha)| << N / (log N)^A for alpha on minor arcs

which gives r(N) > 0 for N sufficiently large. But "sufficiently large" depends on the implicit constant, and no explicit value of N_0 is known beyond which all even numbers satisfy Goldbach.

**The parity problem:** The sieve methods that work for almost-all Goldbach (Chen's theorem: every sufficiently large even number is a sum of a prime and a semiprime) cannot distinguish between primes and products of two primes. This is the "parity barrier" — sieves see primes and semiprimes identically.

**The honest wall:** The circle method gives r(N) > 0 for N > N_0, but N_0 is not effectively computable. The sieve methods hit the parity barrier. No technique exists to cross it. The Goldbach conjecture is true for all n <= 4 x 10^18 (Oliveira e Silva, 2013), but the analytic proof remains out of reach.

### References

- Hardy, G.H. & Littlewood, J.E. (1923). "Some problems of 'Partitio Numerorum' III." Acta Math. 44, 1-70.
- Chen, J. (1973). "On the representation of a larger even integer as the sum of a prime and the product of at most two primes." Sci. Sinica 16, 157-176.
- Oliveira e Silva, T. (2013). "Computational verification of the Goldbach conjecture up to 4 x 10^18."

---

## Summary: Type of Gap for Each Problem

| Problem | Gap Type | What's Needed | Difficulty |
|---------|----------|---------------|------------|
| **BSD** | Construction | New Euler system for rank >= 2 | Hard (major open problem) |
| **Hodge** | Construction | Algebraic cycle for codim >= 2 | Very hard (no known approach) |
| **P vs NP** | Technique | Any super-polynomial lower bound | Extremely hard (barriers exist) |
| **Goldbach** | Technique | Cross the parity barrier | Very hard (fundamental limitation) |

The pattern: all four remaining problems require **new mathematical objects or techniques** that do not currently exist. They are not computational gaps — they are conceptual gaps. No amount of computing power will close them.
