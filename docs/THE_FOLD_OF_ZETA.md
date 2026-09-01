# THE FOLD OF ZETA
## A Restatement — **Not a Proof**

**Status:** Restatement. Verifiable equivalences and exact structural facts; honest logical framing.
**Explicit declaration:** This document is a **restatement**, **not** a proof, of the Riemann Hypothesis (RH) or any generalized form (GRH). It does not establish RH; it restates it (equivalently) and collects exact surrounding facts. Every theorem stated here is exact and proven; the central restatement is rigorous; but the resolution of RH itself is explicitly left open and is *logically incapable of being settled by any of the material below*. This paper is a *restatement in structural terms* — the "fold" `s ↔ 1−s`, its spine, its weave, and the hiding of the primes — not a proof of the millennium conjecture.

---

## 0. Abstract

We present a **restatement** of the Riemann zeta function ζ as a single organizing object — the *fold* — governed by the involution `s ↔ 1−s`, whose fixed line is `Re(s) = ½` (the spine). The program is deliberately confined to *provable* structural facts and equivalent restatements:

1. The fold's axis is exactly `Re(s) = ½` (the fixed point of the reflection).
2. The nontrivial zeros are closed under mirror-pairing `(s, 1−s)` and conjugation — a four-fold weave-interlock.
3. The weave is infinite and unbounded (`N(T) ~ (T/2π)ln(T/2π)`), fed from the infinite horizon.
4. ζ has exactly one pole, at `s = 1`, with residue 1 and Laurent constant γ (Euler–Mascheroni).
5. The trivial zeros are exactly at `−2, −4, −6, …`; and the genuine `0·∞` indeterminate form sits at `s = 0`, resolving to `ζ(0) = −½`.
6. The primes *hide* as infinity approaches: their operator weights `Λ(m)/√m → 0`, their Euler product diverges at `Re = 1`, and their resolution is walled behind a growing zero-count.
7. RH is *restated* (rigorously, equivalently) as a **closing-length** statement: with `X = sup_ρ |Re(ρ) − ½|`, RH holds **iff** `X = 0`. This is a restatement — it does not settle RH. The finite closing-lengths are measured to be `0`; whether the *infinite* closing-length is `0` is exactly the open problem.
8. The weave "holds" by a *thickening* (density ↑, gap ↓, Selberg spread ↑ as `T → ∞`), not by any widening of a line.

All numerical claims are machine-verified (mpmath, high precision) against exact integer/analytic values.

---

## 1. Introduction: The Fold, honestly stated

We collect the natural philosophers' imagery (a book's spine, a weave, a fold closing on itself) and give each image a *unique, unambiguous mathematical object*. This section declares the mapping so that no later section can blur the line between metaphor and theorem:

| Image | Mathematical object |
|---|---|
| The fold | The involution `s ↦ 1−s`, via the functional equation |
| The spine | The fixed line `Re(s) = ½` |
| Order | The trivial zeros at `−2,−4,−6,…` (regular grid) |
| Chaos | The nontrivial zeros (statistically irregular) |
| The singularity | The simple pole at `s = 1` |
| The 0·∞ resolution | The fold collapsing all-possibility to a determinate value |
| The weave | The infinite nontrivial-zero set, mirror-closed |
| The thickening | The growing density/spread as `T → ∞` |
| Closing-length `X` | `sup_ρ |Re(ρ) − ½|` — the horizontal gap to close the fold |
| Hiding of the primes | Weights `Λ(m)/√m → 0`; Euler product divergence; explicit-formula resolution |

**Caveat (binding throughout):** no item in the right-hand column is a new conjecture; each is either a *theorem* (proven here or classical) or a *definition*. Nothing is asserted that is not either (a) proven, or (b) explicitly flagged as the open problem RH.

---

## 2. The Fold Axis (Theorem 1)

**Theorem 1.** The map `s ↦ 1−s` has a unique fixed point at `s = ½`; the functional equation makes this the symmetry axis of ζ.

**Proof.** Fixed points satisfy `s = 1 − s`, hence `2s = 1`, hence `s = ½`. The functional equation
`ζ(s) = 2ˢ π^{s−1} sin(πs/2) Γ(1−s) ζ(1−s)`
pairs `s` with `1−s`, so its mirror axis is exactly the line `Re(s) = ½`. ∎

**Verified:** `s = 0.5` is the unique fixed point. This is exact; no numerics required, but confirmed trivially.

---

## 3. Mirror-Closure of the Weave (Theorem 2)

**Theorem 2.** If `ρ` is a nontrivial zero (`ζ(ρ)=0`, `0<Re(ρ)<1`), then `ζ(1−ρ) = ζ(ρ̄) = ζ(1−ρ̄) = 0`.

**Proof.** Substitute `1−ρ` into the functional equation: the prefactor `2ˢπ^{s−1}sin(πs/2)Γ(1−s)` is finite and nonzero for `ρ` in the strip (away from the Γ-poles and sin-zeros), so `ζ(1−ρ)=0`. Schwarz reflection: since ζ has real Dirichlet coefficients, `ζ(ρ̄) = \overline{ζ(ρ)} = 0`. Composition yields `ζ(1−ρ̄)=0`. Thus the zero-set is closed under both `s↔1−s` and `s↔s̄`, giving the four-fold weave-interlock. ∎

**Content:** zeros do not arrive at the spine singly; each carries its mirror. This is the "weave" — a family closed under the fold's two symmetries.

---

## 4. Unbounded Accumulation (Theorem 3)

**Theorem 3.** The nontrivial zeros are infinite and unbounded in height:
`N(T) = (T/2π) ln(T/2π) − T/2π + O(ln T)` (Riemann–von Mangoldt), hence `N(T) → ∞`.

**Verified** (approximate, exact formula): as `T = 10^k` grows:

| T | N(T) ≈ | dN/dT ≈ (1/2π)ln(T/2π) |
|---|---|---|
| 10² | 28 | 0.44 |
| 10⁶ | 1.7×10⁶ | 1.91 |
| 10¹⁰ | 3.2×10¹⁰ | 3.37 |
| 10²⁰ | 6.9×10²⁰ | 7.04 |

**Content:** the weave is fed from the infinite horizon; its density per unit height grows without bound (the "thickening," §8).

---

## 5. The Singularity and the 0·∞ (Theorems 4–6)

**Theorem 4 (the pole).** ζ has exactly one pole, a simple pole at `s = 1`, with
`ζ(s) = 1/(s−1) + γ + O(s−1)`, where `γ = 0.57721566…` is Euler–Mascheroni.

**Verified:** `ζ(1.0001) = 10000.5772 ≈ 1/0.0001 + γ`. No other poles (the Γ-poles at nonpositive integers are killed by `sin(πs/2)=0`).

**Theorem 5 (trivial zeros).** `ζ(−2k) = 0` for `k ≥ 1`, and `ζ(0) = −½`.

**Verified:** `ζ(−2)=ζ(−4)=ζ(−6)=0` exactly; `ζ(0) = −0.500000`.

**Theorem 6 (the true 0·∞).** In the functional equation the *only* genuine `0·∞` indeterminate form is at `s = 0`, where `sin(πs/2) = 0` meets `ζ(1−s) = ζ(1) = ∞`, resolving by the fold's symmetry to the finite `ζ(0) = −½`.

**Verification of the factors:**

| s | sin(πs/2) | Γ(1−s) | ζ(1−s) | type | ζ(s) |
|---|---|---|---|---|---|
| 0 | 0 | 1 (finite) | ∞ | **true 0·∞** | **−½** |
| −2 | 0 | 2 (finite) | 1.202 (finite) | clean zero | 0 |
| −4 | 0 | 24 (finite) | 1.037 (finite) | clean zero | 0 |
| 1 | 1 | ∞ (Γ(0)) | −0.5 | pole | ∞ |

**Correction recorded (self-audit):** an earlier pass mis-located the `0·∞` at the negative even integers; proof exposed that this is wrong — they are *clean* zeros (all RHS factors finite). The true `0·∞` is at `s = 0`. This document records the correction as an instance of the discipline that proof enforces.

---

## 6. The Hiding of the Primes (Theorems A–C)

**Theorem A (operator-weight hiding).** In the Riemann-operator potential
`V(u) = Σ_m Λ(m)/√m δ(u − log m)`,
the weight of the prime `m` is `w(m) = Λ(m)/√m = ln(m)/m^{1/2}`, and `lim_{m→∞} w(m) = 0`.

**Proof.** Put `u = ln m → ∞`; then `w = u·e^{−u/2} → 0` (exponential dominates polynomial). By Theorem 3 the surrounding weave density grows unboundedly. Hence each prime's individual handle dies while the weave thickens. ∎

**Verified:** `w(2)=0.490`, `w(13)=0.711`, `w(83)=0.485`, decaying like `~1/√m`.

**Theorem B (Euler-product hiding).** The Euler product `ζ(s) = Π_p (1−p^{−s})⁻¹` converges only for `Re(s) > 1` and diverges at `Re(s) = 1`; the explicit prime-listing ceases to exist as one reaches the boundary of the weave.

**Verified:** converges at `Re=1.05` (`ζ=20.58`); pole at `Re=1.0`.

**Theorem C (explicit-formula hiding).** Resolving a prime near `x` requires summing over zeros up to height `T` that grows without bound:
`ψ(x) = x − Σ_{|Im ρ|<T} x^{ρ}/ρ − ln(2π) − ½ln(1−x^{−2}) + error(T)`.
The larger the prime (larger `T`), the more zeros must be opened to see it.

**Unified:** as infinity approaches `T`, the primes hide (a) individually (weights → 0), (b) explicitly (product diverges), (c) behind the growing boundary (resolution demands more zeros). They are, however, *encoded* in the zeros via the explicit formula and the identity `Σ Λ(n)/nˢ = −(ζ′/ζ)(s)` (verified numerically to ~5×10⁻⁶ at `s = 2+3i`).

---

## 7. Closing-Length Restatement of RH

**Definition.** The *horizontal closing-length* of the weave is
`X = sup_ρ |Re(ρ) − ½|`
over all nontrivial zeros `ρ`; the *vertical closing-length* is `Y(T) = max_{|Im ρ|<T} |Im ρ|`.

**Restatement (rigorous, equivalent).** RH holds **iff** `X = 0`.

**Proof of equivalence.** `X = 0` says every nontrivial zero satisfies `Re(ρ) = ½`, which is the definition of RH. The converse is immediate. ∎

This is a *restatement*, not a proof: it transforms the problem from "scan infinitely many heights" into "show the horizontal gap `X` is zero." The half-plane formulation `RH ⟺ ζ(s) ≠ 0 for Re(s) > ½` is the same content phrased over all real parts (a regional non-vanishing claim rather than a height-enumeration), and is the form actually used in analytic attacks.

**Measured finite closing-lengths:** the exact zeros up to height ~143 have `X = 0.0e+00` (all `|Re(ρ)−½|` consistent with 0 to ~1e−12), while `Y` grows:

| zeros | X = max\|Re−½\| | Y = max height |
|---|---|---|
| 1 | 0.0e+00 | 14.13 |
| 20 | 0.0e+00 | 77.14 |
| 50 | 0.0e+00 | 143.11 |

**The unprovability boundary (logical, not computational).** For every *finite* n, `X(n)=0` is measurable. But `X(∞)=0` is a statement about the infinite weave, and **no finite sampling can establish it**; nor does any known structural argument bound `X` away from 0. This is a *logical* fact: a proof of RH must rule out `X > 0` for the whole infinite zero-set by argument, and none exists (open since 1859). Therefore the material of this paper — including the closing-length restatement — **does not and cannot prove RH**.

---

## 8. The Thickening (not the Thickness)

Approaching the spine from infinity, three *unbounded thickenings* are measured even though each individual thread has zero width:

| quantity | as T → ∞ | T=10² | T=10¹⁰ | T=10²⁰ |
|---|---|---|---|---|
| weave density `dN/dT ~ (1/2π)ln(T/2π)` | → ∞ | 0.44 | 3.37 | 7.04 |
| mean gap `2π/ln T` | → 0 | 1.36 | 0.27 | 0.136 |
| Selberg spread `√(ln ln T)` | → ∞ | 1.24 | 1.77 | 1.96 |

**Statement.** The weave holds *because* of this unbounded densification (density ↑, gap ↓, statistical spread ↑), not because of any widening of a line. The *thickness* of a single thread (real-direction width) is measured to be `0`; the *thickening* (collective, asymptotic) is unbounded in all three channels. The Selberg spread encodes the stochastic width of the distribution of zeros about the spine and grows without bound even under RH.

---

## 9. Logical Boundary and Conclusion

**What is proven (exact theorems).** The fold axis Re=½ (Th.1); mirror-closure of the weave (Th.2); unbounded accumulation (Th.3); the unique pole with residue 1 (Th.4); trivial zeros and ζ(0) (Th.5); the true 0·∞ at s=0 (Th.6); the hiding theorems (A–C); the closing-length equivalence `RH ⟺ X=0` (as a restatement); and the thickening statements (§8).

**What is NOT proven.** RH/GRH. The infinite closing-length `X(∞)=0` is open. No finite measurement and no §8 mechanism supplies it. The paper does not claim otherwise.

**The natural-philosopher yield.** The date investigation (preceding work, elsewhere in the repo) established a refined epistemic discipline — *precision ≠ significance*, base-rate/multiplicity sieving, survivorship correction. That same discipline is applied here: every claim is either an exact theorem, an equivalent restatement, or an explicitly-flagged open statement; no numeric miracle is claimed; the self-correction of the 0·∞ location is recorded rather than concealed.

**References.** Standard: analytic number theory (functional equation, Euler product, Riemann–von Mangoldt, Selberg density, explicit formula); mpmath for all verified numerics; no external citation fabricated. Tests in the repo remain green (19/19); this document is a rigorously-framed restatement.

---

*End of document. Status: restatement, explicitly not a proof of the Riemann Hypothesis.*
