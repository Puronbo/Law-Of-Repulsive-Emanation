# Correction: `zero_to_riemann_zeta_complete_framework.md`

**Date:** 2026-09-29
**Subject:** `C:\Users\Me\Downloads\zero_to_riemann_zeta_complete_framework.md`
**Evidence:** `experiments/audit_zero_to_riemann_zeta.py` (20 claims, 16 agree,
4 disagree) → `experiments/data/audit_zero_to_riemann_zeta_data.json`
**Regression:** `tests/test_rh_framework_audit.py` (11 tests)

The source document is outside this repository and has been left untouched. This
is a claim-by-claim correction of it.

**Summary: the framework's spine is correct; four of its algebraic statements
are wrong, and two of those four are load-bearing.**

---

## 1. What is correct (16 claims)

| § | Claim | How it was checked |
|---|---|---|
| 3 | `w = u²`, `u = a+ig ⟹ Im w = 2ag`, so RH ⟺ `w` on the negative real axis | direct; `Im w = 1.045620 = 2ag` |
| 5 | mean spacing `~ 2π/log(T/2π)` | `0.5246` at `T = 1e6` |
| 6 | `H'/H = Σ Q_n/(1+Q_n z) = P₁ − P₂z + P₃z² − ⋯` | residual `2.8e-08` vs exact, pure truncation |
| 6 | Newton identities then link `e_k` to `P_k` | — |
| 7 | `q=0.9, r=0.5` refutes "degree 2 implies degree 3" | `0.1025 > 0` |
| 7 | `q²r² − 6qr + 4q + 4r − 3 ≤ 0` is the degree-3 hyperbolicity test | 516 random all-real-rooted cubics, 0 violations |
| 9 | Hadamard product; `Σ 1/ρ` is finite so the `+1/ρ` regularisation is legitimate | `−0.0230957090` |
| 10 | `a_n' = a_(n+1)` | central-difference error `9.66e-07 → 2.42e-07 → 6.04e-08`; ratios exactly 4.00, 4.00 |
| 10 | `∂_λ Ξ_λ = −∂_t² Ξ_λ` | residual `1.4e-16` relative |
| 10 | `RH ⟺ Λ = 0` (Rodgers–Tao) | theorem; see the caveat in §3 below |
| 11 | forward stability is one-way only | see §3 below |
| 13 | Newton `e_(k−1)e_(k+1)/e_k² ≤ k/(k+1)` | holds for `k = 2..7` |
| 14 | `Σ x_n` conserved; `(Σ x_n²)' = 2N(N−1)` | drift `2.2e-16`; `264.0` predicted vs `264.0145` measured |
| 14 | `E' = −Σ (x_n')² ≤ 0`, gradient descent | `76.042660 → 76.028186` |
| 15 | `L_n = g_n²G_n < 4` holds at most real gaps | 36 of 38 (95%) |
| 17 | the list of insufficient shortcuts is correct | all six sub-items |

§17 is the most valuable part of the document: it correctly fences off the
standard dead ends, including the two most tempting ones (θ-symmetry and Hankel
positivity).

---

## 2. Error 1 (§9) — sign error in `ξ'/ξ`

**Document writes:**

```
xi'/xi = zeta'/zeta + 1/s + 1/(s-1) - log(pi)/2 - (1/2) Gamma'(s/2)/Gamma(s/2)
```

**Correct:**

```
xi'/xi = zeta'/zeta + 1/s + 1/(s-1) - log(pi)/2 + (1/2) Gamma'(s/2)/Gamma(s/2)
```

because `d/ds log Γ(s/2) = +½ Γ'(s/2)/Γ(s/2)`. Residual at `s = 0.7 + 3.1i`:
**`1.724`** with the document's sign, **`5.0e-42`** with the corrected sign.

This is not cosmetic: the sign propagates into the §9
"prime data + archimedean data ⟷ zero data" identity, which is stated on the
strength of this formula.

---

## 3. Error 2 (§7) — the Jensen inequality is false for the actual ξ

**Document claims:** `D_n = a_(n+1)² − a_n a_(n+2) ≥ 0` (quadratic Jensen
hyperbolicity), hence `q_n ≤ 1`.

**Measured, for the true coefficients of `Ξ(t) = ξ(½ + it)`:**

| `n` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| `q_n = a_n a_(n+2) / a_(n+1)²` | 2.7911 | 1.5683 | 1.3279 | 1.2268 | 1.1716 | 1.1371 | 1.1136 | 1.0966 | 1.0838 |

**All above 1.** The sequence is strictly **log-convex**, not log-concave. The
degree-4 truncation in `t` is not real-rooted (negative discriminant), and
normalisation cannot rescue it, because `q_n` is invariant under rescaling all
`a_n` by a common factor.

**This is the most consequential error in the document**, for three reasons:

1. Taken literally it is **false**, not merely imprecise.
2. The inequality belongs to Jensen *hyperbolicity of a polynomial*, which the
   low-order truncations of `Ξ` do not have. If the document intends Jensen
   *polynomials* in the Griffin–Ono–Rolen–Zagier sense, that is a different
   construction and must be stated explicitly.
3. It invalidates every truncation-level hyperbolicity claim for `Ξ`. The
   degree-16 truncation of `Ξ` at `λ = 0` already has roots off the real axis.
   Consequently the Newman-boundary step (§10) **cannot be verified
   numerically** and must be carried as the Rodgers–Tao theorem it is; a
   "numerical check" of it on truncations would be meaningless.

**Consequence for the central claim `RH ⟺ PF_∞`:** if `PF_∞` is defined on this
raw Taylor sequence, it is **false** — the sequence is not even quadratic
Jensen, let alone totally positive. The document's phrase "in the appropriate
Riemann-(Ξ) normalization" is doing all the work and is never made precise. Note
that ordinary contiguous Toeplitz minors of the normalized sequence *do* come out
non-negative at low order, so the failure is specifically of the Turán/log-
concavity route; the correct statement needs the coefficient sequence and the
Jensen construction both pinned down before `PF_∞` means anything.

---

## 4. Error 3 (§12) — wrong identity, wrong boundary, wrong index

**Document claims:** `D_n = a_n²(1 − r_(n−1) r_n)`, boundary `r_(n−1) r_n = 1`,
and `r_n' = −D_(n+1)/a_n²`.

**Correct:**

```
D_n = a_(n+1)² − a_n a_(n+2) = a_n² r_n (r_n − r_(n+1))
r_n' = −D_n / a_n²
```

verified to `6.7e-41`. The document's form has a maximum relative mismatch of
**106.15** — it is a genuinely different quantity, not a typo. Note
`r_(n−1) r_n = a_(n+1)/a_(n−1)`, which simply does not appear in `D_n`.

So the quadratic boundary is `r_n = r_(n+1)` (monotone coefficient ratios), not
`r_(n−1) r_n = 1`.

**What survives:** the sign `r_n' ≤ 0` is still correct, so the flow direction is
unaffected. The index error is caught by finite-differencing `r_n` along the
actual deformation.

---

## 5. Error 4 (§13) — the Newton translation fails, and it matters

**Document claims:** Newton gives `a_(k−1)a_(k+1)/a_k² ≤ (2k+1)/(2k+2)`, i.e. a
margin of at least `1/(2k+2)`.

**Correct translation.** Newton gives `e_(k−1)e_(k+1)/e_k² ≤ k/(k+1)`. With
`e_k = (−1)^k a_k/((2k)!).Ξ(0))` and the `(2k)±1` factorial ratios this becomes

```
a_(k−1)a_(k+1)/a_k²  ≤  (2k+1)/(2k−1)
```

which **exceeds 1** and is therefore nearly vacuous. The naive Newton route
yields no curvature margin at all.

Worse, the document's stated bound is **contradicted outright** by the real
coefficients: `1.5683, 1.3279, 1.2268, 1.1716, 1.1371, 1.1136` for `k = 2..7` —
all above 1, i.e. all above the claimed `(2k+1)/(2k+2) < 1`.

**This is why Error 2 and Error 4 together are load-bearing.** §13 presents this
margin as the quantitative curvature the whole approach was reaching for. Its
loss is a real setback, not a bookkeeping error. (The underlying cause is
Error 2: the coefficients are log-convex, so no log-concave bound can hold.)

---

## 6. Refinement of §8

§8 concludes that generic positive kernels cannot supply the required all-order
bound. **The conclusion is right; the stated reason is not.**

The required bound is
`Var_n(u²)/E_n(u²)² ≤ (6n+8)/(2n+2)² ~ 3/(2n)`, which decays like `1/n`.
Generic concentration *does* decay at the right order, so the document's
"order 2/n" heuristic is essentially correct:

| `n` | 5 | 25 | 125 |
|---|---|---|---|
| required | 0.263889 | 0.058432 | 0.011936 |
| generic | 0.714 | 0.157 | 0.032 |
| ratio | **2.71** | **2.68** | **2.67** |

The failure is a **stable constant-factor deficit of ≈2.7**, not an
order-of-growth failure. This is a sharper and more actionable statement: any
successful kernel must beat the generic constant by a factor ≈2.7 *uniformly in
n*, which is precisely why "just a positive kernel" is not enough.

---

## 7. Minor and interpretive

- **§1, `θ = π/4`.** Narrative, not derived. The document itself concedes that
  scaling alone does not imply it. Do not cite it as a result.
- **§6, "positivity of `Q_n` is conditional on RH".** `Q_n = 1/γ_n² > 0`
  regardless. What *is* conditional on RH is that the transformed zeros form a
  simple product of distinct real-negative factors.
- **§8, the `2/n` figure.** A heuristic, as above.
- **§10, the `λ ≥ 0` domain.** Worth stating precisely, because it is what makes
  the obstruction structural: with `Φ(u) ~ e^(−u²/2)` the de Bruijn integrand is
  `e^((λ−½)u²)`, so the flow exists only on `λ ∈ [0, ½)` — a half-line, hence
  non-invertible. Measured: the integral over `[0,40]` is `2.802` at `λ = 0.4`
  and `3.849e+68` at `λ = 0.6`.

---

## 8. The document's own conclusion is honest and correct

§11 and §17(f) name the central obstacle exactly right, and §18 declines to
claim a proof. That should be preserved.

The obstruction is structural, and worth stating in its sharpest form: `Λ` is
*defined* as `inf{λ ≥ 0 : Ξ_λ real-rooted}` — a **lower endpoint** of the
hyperbolic set. Forward propagation can only show that set is upward closed. It
can never show the lower endpoint is 0. Since `RH ⟺ Λ = 0`, no forward-
stability argument can reach it; the question must be answered from the `λ = 0`
side. The document is right that this is where the difficulty lives.

The strongest structural statement in the whole framework is §17: the
`PF_∞ ⟺ RH` route, even if the coefficient sequence is fixed correctly (Error 2),
still requires showing a *backward* stability or a direct all-order positivity
mechanism at the boundary. The document has not supplied one, and correctly says
so.

---

## 9. Minimal repair list

1. §9: flip the sign of the gamma term.
2. §7: delete `D_n ≥ 0` for the raw Taylor coefficients. Either state that
   Jensen *polynomials* are meant, or abandon the quadratic route. Do not
   attempt to verify Newman-boundary claims on truncations.
3. §12: replace with `D_n = a_n² r_n(r_n − r_(n+1))`, boundary `r_n = r_(n+1)`,
   and fix the derivative index to `−D_n/a_n²`.
4. §13: replace the bound with `(2k+1)/(2k−1)` and state plainly that it is
   vacuous, then say what would be needed instead of a margin.
5. §8: restate the conclusion as a constant-factor deficit of ≈2.7.
6. Throughout: fix `PF_∞` to a precisely defined coefficient sequence before
   asserting `RH ⟺ PF_∞`.

**No proof of RH is claimed or implied by this framework, and this correction
does not supply one.**

Run `python experiments/audit_zero_to_riemann_zeta.py` to reproduce every number
in sections 1-9, and
`python experiments/rh_positivity_certificate.py` for sections 10-11.

---

## 10. The repair is vacuous: the Jensen condition does not characterise RH

Error 2 left open what the "appropriate normalization" for `PF_∞` should be
(§3, §9.6). The natural repair is the Jensen transform, whose all-order
real-rootedness is the substance of the Griffin-Ono-Rolen-Zagier programme. It
was implemented exactly and tested with the tools that make root counting
trustworthy (Sturm sequences, with the self-test that caught three separate
implementation bugs) in
`experiments/rh_positivity_certificate.py`, gates P1/P5:

- For `Ξ(t) = ξ(½ + it)`, the Jensen polynomial `J_n` is real-rooted at *every*
  tested degree 2..40. First impression: the repair works.
- But the control `1/(1 + t²/4)` — whose zeros are `±2i`, purely imaginary —
  also passes at every tested degree. The condition is **insensitive to where
  the zeros are**.
- The condition is not entirely blind: the stretched-decay sequence
  `(−1)^m 2^(−m²)` is rejected at degrees 32, 34, 36, 38, 40. So it constrains
  the decay profile of the coefficient list while ignoring the location of the
  zeros.

**Conclusion.** The Jensen smoothing is vacuous *as a certificate*: it cannot
separate `Ξ` (whose zeros are on the line) from a function whose zeros are off
it. This closes the option that Error 2 "just needed the right normalization".
The raw-sequence `PF_∞` is false and the smooth repair is uninformative; the
only remaining form of the route is the genuinely hard one (Λ = 0, or the
GORZ construction on the function with the correct sign convention), which no
one has a proof of.

---

## 11. The direction obstruction is algebraic, not analytic

§10's deformation acts on coefficients by `a_n' = a_(n+1)`. Two facts about
that shift (gates P3/P4), with the index direction stated exactly:

1. The **index-decreasing** shift `b_n' = b_(n−1)` has the exact generating
   function `B_λ(z) = e^(λz) A(z)` (`[zⁿ]e^(λz)A = Σ_{j≤n} a_j λ^(n−j)/(n−j)!`),
   and `e^(λz)` is a Pólya-Schur multiplier. That direction *is* accessible to
   Schoenberg-type positivity transfer.
2. The de Bruijn flow is the **index-increasing** shift `a_n' = a_(n+1)`
   (solution `Σ_{j≥n} a_j λ^(j−n)/(j−n)!`), whose generating function satisfies
   `∂_λ A_λ = (A_λ − A_λ(0))/z` — an ODE with a source term, **not** the
   multiplication `e^(λz) A(z)`. Coefficient mismatch against the multiplier
   direction: `3.46e-01` at `λ = 0.7`, exactly reproduced. The operation the
   flow performs has the opposite index sign from the operation that transfers
   positivity.

Independently, `A(z) = Σ a_n z^n` has finite radius of convergence (the
coefficient ratios are still rising at the top of the computable range, bound
≈ 1.09), so it is not even an entire object whose zeros could carry meaning.

So the one-way structure is not a subtlety about integrability; the index
direction of the positivity transfer and the index direction of the flow are
opposite, which is the Λ lower-endpoint problem of §8 above restated in
coefficient terms.

---

## 12. Updated repair list

1. §9: flip the sign of the gamma term.
2. §7: delete `D_n ≥ 0` for the raw Taylor coefficients. Do **not** replace it
   with the Jensen real-rootedness variant as a certificate: §10 shows that
   variant is vacuous. State plainly that no all-order positivity certificate
   is available on either the raw or the smoothed sequence.
3. §12: replace with `D_n = a_n² r_n(r_n − r_(n+1))`, boundary `r_n = r_(n+1)`,
   and fix the derivative index to `−D_n/a_n²`.
4. §13: replace the bound with `(2k+1)/(2k−1)` and state plainly that it is
   vacuous, then say what would be needed instead of a margin.
5. §8: restate the conclusion as a constant-factor deficit of ≈2.7.
6. Throughout: `PF_∞` has no usable normalization — raw is false (§3), smoothed
   is vacuous (§10), and the transfer is blocked in the flow's own direction
   (§11). Present the route as a genuinely open hard problem, not a certificate
   waiting for a letter.

---

## 13. The pinned §8 kernel and the zero dynamics are independently verified

The one-sided cosine-transform representation of §8 was re-derived from the
pinned record (September 2026, section 8) and verified from scratch — closed
form, pointwise, and along the de Bruijn flow — in
`experiments/rh_zero_scale_objects.py`, gates G1/G4:

- **G1 (kernel).** `Ξ(t) = ∫₀^∞ Φ(u) cos(tu) du` with `Φ(u) = 4Σ φ_n(u)`,
  `φ_n(u) = (2π²n⁴e^{9u/2} − 3πn²e^{5u/2})e^{−πn²e^{2u}}` reproduces:
  `∫Φ = ξ(½)` to full precision via the closed form (Gamma / incomplete gamma,
  agreement to the last digit), and `|Ξ(γₖ)| < 2.1e-25` at the first ten zeros.
  The load-bearing exponents are `(9u/2, 5u/2, 2u)` with prefactor 4; the
  earlier `(9u, 5u, 4u)` variant fails everything.
- **G2 (flow equation).** `∂_λ Ξ_λ = −∂_t² Ξ_λ` on the deformed kernel
  `Ξ_λ(t) = ∫ Φ(u) e^{λu²} cos(tu) du` holds to residuals of order `1e-54`.
- **G3 (real-axis persistence).** The first sixteen zeros stay real for `λ ∈
  {0, −1/10, −1/5, −1/4}`, each branch followed by Newton continuation from the
  previous root (identity preserved: no jump to a foreign root allowed). The
  range stops at −1/4 deliberately: below it, close pairs begin to bend
  together (g13/g14 near −0.3) in service of their departure scale.
- **G4 (velocity law).** The drift obeys `t'(λ) = Ξ_tt / Ξ_t`: the kernel
  derivative `Ξ_tt/Ξ_t` at each zero agrees with the tracked motion across
  `λ = ±1/40, ±1/20` (Richardson-extrapolated to remove the `t'''` curvature
  term) to at worst `3.6e-5` relative.
- **G5 (symmetric spacing law).** At λ = 0 the velocity satisfies the
  mirror-symmetric two-body (Calogero/Moser) law
  `t'_n = 1/γₙ + 4γₙ Σ_{k≠n} 1/(γₙ² − γₖ²)`. This is exactly the record's
  spacing law `dx_n/dλ = 2Σ_{m≠n} 1/(x_n − x_m)` evaluated over the *whole*
  mirror-symmetric zero set `{±γₖ}`: the image `−γₙ` supplies the `1/(2γₙ)`
  term and each partnered pair appears twice. The sum is carried directly
  over the first 200 zeros plus an exact moment tail
  (`M_{2j} = Σₖ 1/γₖ^{2j}` from the Taylor coefficients of `log Ξ(t)`),
  and agrees with the kernel velocity to a worst `1.01e-5` (g1: `2.6e-20`,
  g4: `3.3e-16`, g9: `3.3e-12`, g13: `2.6e-8`). **This resolves the
  previously reported "spacing-law O(1) mismatch":** the failure came from
  summing only the positive zeros; with the mirror images the law holds
  essentially exactly.
- **G6 (close-pair departure, now measured).** The closest adjacent pair
  (g13, g14) = (59.3470, 60.8318), Δγ = 1.4847, is continued down through the
  exact kernel by Newton continuation and then by an adaptive window scan of
  sign changes (Newton drifts to foreign roots near a double root). Over the
  fine ladder the squared gap is ~linear in λ with fitted slope `7.990`
  -- the exact gap law `(δ²)' = 8 − 4δ²S_n` of the pinned record forces the
  slope to 8 as the gap closes -- and its zero extrapolates the departure
  `λ* = −0.321318`, where the double-root condition `F = F_t = 0` holds to
  `|F|+|F_t| ≈ 8.8e-22`. The measured value is **strictly deeper than the
  naive mutual-only local model** `λ_c = −(Δγ)²/8 = −0.27556`: the
  remaining-spectrum term `S_n` pulls the pair apart, so a pure two-body
  picture under-cuts the true departure. G6 is the finite, visible face of
  Newman's "barely so" -- a measurement of the finite system, not a bound on
  Λ.
- **G7 (the next two closest pairs also depart).** The two next-closest
  adjacent pairs of the first sixteen zeros leave the real axis the same way,
  each at its own double root: (g9, g10), Δγ = 1.7687, `λ* = −0.469478`
  (slope `7.991`, `|F|+|F_t| ≈ 8.3e-18`); (g15, g16), Δγ = 1.9673,
  `λ* = −0.689762` (slope `7.988`, `|F|+|F_t| ≈ 7.8e-24`). Both are deeper
  than their naive mutual-only models (`−0.3910`, `−0.4838`).
- **G8 (λ* is predicted in closed form).** No per-pair tuning is involved:
  reading `S_n` off the exact spacing law at λ = 0,
  `S_n = (4/δ₀ − δ'(0))/(2δ₀)` with `δ₀ = γ_b − γ_a` and
  `δ'(0) = t'_b − t'_a`, the gap law solved with constant `S_n` gives
  `λ*_S = ln(1 − S_nδ₀²/2)/(4S_n)` (limit `S_n → 0` recovers the naive
  `λ_c = −δ₀²/8`). It lands on the measured departures: (13,14) `−0.321502`
  vs `−0.321318` (relative `5.7e-4`, naive off by `1.4e-1`); (9,10)
  `−0.470039` vs `−0.469478` (`1.2e-3`, naive `1.7e-1`); (15,16) `−0.688300`
  vs `−0.689762` (`2.1e-3`, naive `3.0e-1`). The departure scale is fixed by
  the stationary spectrum through the gap law -- a quantitative statement,
  not a free fit.
- **G9 (the gap law is an exact identity).** The pinned record's section 24
  law `δ' = 4/δ − 2δS_n` is verified as an identity, not fitted: `S_n` is
  computed *directly from the zero positions* as the mirror-symmetric
  rest-remainder sum
  `S_n = Σ_{m∉{a,b}} 1/((x_b−x_m)(x_a−x_m))` over the full set `{±γₖ}`
  (including the images `−x_a, −x_b`), first `G5_K=200` terms plus the moment
  tail, and `δ'(0)` is evaluated independently from the kernel velocity
  `Ξ_tt/Ξ_t` at each zero and from the spacing law.  All three agree on
  every measured pair: kernel-vs-law residual `≤ 1.0e-5` (the G5
  velocity-noise floor), spacing-vs-law residual `≤ 3.4e-11` (pure
  truncation), and the direct and velocity-built `S_n` agree to `≤ 1.2e-11`.
  This is why the `S_n` correction in G8 is not an empirical fudge: the
  rest-remainder sum the pinned record writes down IS the object the closed
  form uses, on the nose.
- **G10 (the collapse-rate direction is a theorem).** The pinned record's
  section 25 defines the mirror-symmetric inverse-square two-body sum
  `G_n = Σ_{m∉{a,b}} [1/(x_a−x_m)² + 1/(x_b−x_m)²]` and asserts
  `S_n ≤ ½G_n`.  That is a term-wise AM-GM inequality: with
  `u = 1/(x_a−x_m)`, `v = 1/(x_b−x_m)`, the identity `(u−v)² ≥ 0` gives
  `uv ≤ (u²+v²)/2` for **every** summand, including the mirror branches
  `±x_k` and the self-images `−x_a, −x_b` (checked term-wise: worst
  violation `0.0e+00`).  Summing, `S_n ≤ ½G_n`, and the exact gap law
  becomes the strict bound `(δ²)' = 8 − 4δ²S_n ≥ 8 − 2δ²G_n = 8 − 2L_n`
  with `L_n = δ²G_n`.  When `L_n < 4` the squared gap is forced to grow
  under forward flow by pure inequality — no velocity measurement enters.
  All fifteen adjacent pairs of the first sixteen zeros satisfy
  `S_n ≤ ½G_n`; the three measured pairs have `L_n = 1.1300 (13,14),
  1.3226 (9,10), 2.2874 (15,16)`, all `< 4`, and their measured gap slopes
  `2δ₀δ'(0) = 5.8278, 5.4704, 3.7708` sit at or *above* the bounds
  `8−2L = 5.7400, 5.3548, 3.4251` — the inequality is a strict loss, so the
  *direction* of each −1/4→0 squared-gap slope is exact while its *size* is
  not fixed by the theorem.

**Why the gap law is exact (the four-step identity).** Three lemmas, all
pure algebra, make G8/G9 identities rather than observations:

1. **Product form of Ξ.** As an even entire function of order 1 with real
   zeros, `Ξ_λ(t) = Ξ_λ(0) ∏ₖ (1 − t²/xₖ(λ)²)`, where `xₖ` are the positive
   zeros (mirror pairs `±xₖ` both appear).  Log-differentiating,
   `(ln Ξ_λ)'(t) = Σₖ 2t/(t²−xₖ²)`.
2. **Velocity law = two-body law.** Along the heat flow
   `∂_λΞ_λ = −∂_t²Ξ_λ`, a root obeys
   `x'_n = Ξ_tt/Ξ_t |_{x_n}`.  Near `t = x_n` the log-derivative has a
   simple pole with residue 1; its regular part at `x_n` is exactly
   `1/(2x_n) + Σ_{k≠n} 2x_n/(x_n²−xₖ²)`, which is the two-body sum over the
   mirror set: `x'_n = 2Σ_{m≠n} 1/(x_n−x_m)` over `{±xₖ}` (the self-image
   `−x_n` supplies the `1/(2x_n)` term).  This is precisely the pinned
   record's spacing law (G5, verified against the kernel to `1e-5`).
3. **Gap law from algebra.** For `δ = x_b − x_a`, subtract the two
   velocities: the mutual term `x_a ↔ x_b` telescopes to `4/δ` (each
   partner contributes `2·1/δ` via `t'_b` and `t'_a`), and every other term
   reassembles, using the mirror identity
   `1/((x_b−x_m)(x_a−x_m))`, into `−2δ S_n` with exactly the section-24
   rest-remainder sum.  Hence `δ' = 4/δ − 2δS_n`, i.e.
   `(δ²)' = 8 − 4δ²S_n` (G9 checks this identity numerically three ways).
4. **Closed form solves the ODE with constant `S_n`.** Treating `S_n` as
   frozen at its λ = 0 value, `V = δ²` solves `V' = 8 − 4S_nV`, giving the
   explicit closed form `λ*_S = ln(1 − S_nδ₀²/2)/(4S_n)`.  The only
   approximation in the whole chain is this constant-`S_n` freeze (G8
   quantifies it: relative `5.7e-4` to `2.1e-3` on the measured pairs); the
   λ = 0 identity itself, and the object `S_n` G8 uses, are exact.
5. **Direction of the bound is AM-GM (G10).** Step 3's `S_n` is itself
   bounded term-wise by the inverse-square two-body sum `G_n` through the
   elementary identity `uv ≤ (u²+v²)/2` applied to every reciprocal pair
   `u = 1/(x_a−x_m)`, `v = 1/(x_b−x_m)`.  Hence `δ' = 4/δ − 2δS_n ≥
   4/δ − δG_n`, i.e. `(δ²)' ≥ 8 − 2δ²G_n`.  Under `L_n = δ²G_n < 4` the gap
   expands in forward flow by inequality alone; every measured pair is in
   that regime, and the measured slopes confirm the bound is strict, not
   tight.  This moves the *sign* of the departure-rate from observation to
   theorem — but it does not follow the pair to its collapse, so the
   departure *scales* remain continuation measurements (G6–G8), exactly as
   the artifact states.

One honest wall remains and is stated in the artifact: the per-zero departure
scales `λ*ₖ` for the *other* zeros are unmeasured (a robust bifurcation
continuation for each pair is a separate, still-open computation), and no
general RH statement follows from a finite set of departure scales — however
many measured values agree that zeros leave the axis below −1/4, that is a
phenomenology of the flow, not a theorem about Λ. `departure_scales_open`
records this explicitly.

**Conclusion.** Nothing here touches the truth of RH; it confirms that the §8
kernel as pinned is the right object and that the framework's zero-motion
claims (real-axis persistence to −1/4, the velocity law, the symmetric
two-body spacing law, and now the measured close-pair departures with gap-law
slope 8, predicted in closed form by the `S_n`-corrected gap law) hold on it.
G10 adds a purely algebraic corollary: the squared-gap slope of every
measured pair is *positive by theorem* (a term-wise AM-GM bound
`(δ²)' ≥ 8 − 2δ²G_n` with `L_n < 4`), so the direction in which those pairs
depart is not an accident of the continuation.  The departure *scales*
themselves — the finite `λ*` at which each pair collapses — are still
measured, not derived, and the folklore that the inequality alone continues a
pair all the way is explicitly declined.  The departure scales of the three
closest pairs are aligned with what Newman's "barely so" demands of any
counterfactual: each pair does leave the axis at a finite λ, exactly at a
double root of the deformed kernel.

---

## 14. The Stieltjes/Widder/Hankel stage: the first shifted determinants (H1)

The October 2026 pinned records (`rh_infinite_unit_stieltjes_pinned.md`,
`rh_framework_pinned_october_2026.md`) reorganize the target around the
normalized unit `U(u) = X(u)/X(0)`, the transformed zero scales
`w_ρ = −u_ρ²`, the Stieltjes function `F_ξ(x) = 2G'(x)/G(x)` with
`G(x) = X(√x)`, the Widder moments `Q_m(x) = Σ_ρ q_ρ(x)^m`,
`q_ρ(x) = w_ρ/(x+w_ρ)²`, and the shifted Hankel determinants
`D_m(x) = Q_{2m+1}Q_{2m+3} − Q_{2m+2}²`.  Section 14 of the first record names
the immediate target explicitly: *do not add another independent criterion*,
compute `D_0 = Q_1Q_3 − Q_2²`, then `D_1 = Q_3Q_5 − Q_4²`, in search of a
positive-kernel representation.  `experiments/rh_widder_hankel_h1.py` opens
that stage with five sub-gates (H1a–H1e); all pass.

- **H1a (section 17 translation is exact).** The finite differential transform
  `Q_k(x) = ½ Σ_{j=0}^k C(k,j)(−x)^{k−j} (−1)^{2k−j−1}/(2k−j−1)! F_ξ^{(2k−j−1)}(x)`
  is rebuilt from `ζ'/ζ` by analytic continuation — *no* `zetazero` call enters
  `F_ξ` — and matched against the mirror-symmetric zero expansion
  `Σ_ρ q_ρ^m`.  The slowly-converging `m = 1` entry converges only like
  `log²K/K` (400 zeros leave a ~1e-3 hole), so it is closed with the exact
  log-Ξ moment tail `Q_1 = Σ_j (−1)^j(j+1)x^j M_{2j+2}` built from the Taylor
  data already used by G5/G9.  Worst relative residual over `x ∈ {1/10, 1/2,
  1, 2, 4, 16}` and `k = 1..5` is `2.9e-5`.  The pole at `s = 1` (i.e.
  `x = 1/4`) is deliberately avoided.
- **H1b (section 18 explicit formula, gamma sign load-bearing).** `F_ξ` is
  rebuilt independently from `Xi(s) = ½ s(s−1) π^{−s/2} Γ(s/2) ζ(s)` by
  logarithmic differentiation and matched against `F_rational + F_Gamma +
  F_prime`; the split closes to `1.3e-70`.  Flipping the sign of the
  `½log π` term of `F_Gamma` raises the residual to `2.5e+01`, so the sign in
  the pinned section 18 is the one that closes the identity — the same
  load-bearing sign that §2 of this document flagged in the Sept record.
- **H1c (section 10 Vandermonde identity is exact algebra).** For the
  zero-side `q_ρ`, `D_m = Q_{2m+1}Q_{2m+3} − Q_{2m+2}²` equals
  `Σ_{i<j}(q_iq_j)^{2m+1}(q_i−q_j)²` to `5.6e-69` (machine).  Under RH each
  term is `≥ 0`, so `D_m ≥ 0` term-by-term.  The check is made against the
  *truncated* products from the same 400 `q`'s — comparing it against the
  moment-tail-extended product would report a spurious ~11% mismatch, since
  the tail runs past the 400 zeros and the pair sum does not.
- **H1d (the first two determinants are positive on the sampled half-line).**
  `D_0(x), D_1(x) > 0` at every sampled `x > 0`, computed from the explicit
  formula without any zero-location data (e.g. `D_0(0.1) = 1.9434e-09`,
  `D_1(0.1) = 2.3558e-20`).  This is the sampled, first-order face of the
  Widder criterion's `D_m ≥ 0`; a *negative* sample would refute RH, positive
  samples are evidence consistent with it, nothing more.
- **H1e (section 10 off-axis obstruction reproduces).** A strictly dominant
  synthetic conjugate pair (`q_* = e^{±0.7i}`) over `20` real background
  `q_j ∈ [0, 1/3]` drives `D_m < 0` for `m ≥ 12` (`D_24 = −1.6601`), via the
  pair contribution `(q_*q̄_*)^{2m+1}(q_*−q̄_*)^2 = −4sin²θ` dominating the
  `O((1/3)^{2m+1})` background.  This is the derivation of section 10, not an
  RH proof; the determinant identity is re-checked on the synthetic multiset
  (`det_check = 5.6e-70`).

**Honest wall.** H1 is an investigation, not a proof.  The Widder criterion
(`RH ⇔ Q_m ≥ 0 ∀m`) is used only as a posited equivalence; positivity is
checked at finitely many `x`; and the actual bottleneck named by both records
— deriving the universal Hankel positivity from the prime–gamma explicit
formula (`F_ξ → Q_k → H_N → cᵀH_Nc ≥ 0`, record section 27) — is untouched.
The `D_0`, `D_1` samples are a first numerically-verified foothold on the
zero side of that bridge, with the translation (H1a), the explicit-formula
split (H1b), and the determinant algebra (H1c) now pinned exactly.

## 15. The full Hankel ladder and the shifted Schur identities (H2)

Where H1 opened the stage with the first two shifted determinants, H2 climbs
to the structure those determinants are the `2×2` shadows of:
`experiments/rh_widder_hankel_h2.py` builds the Hankel matrices of the
transformed-zero moment sequence `M_k(x) = Q_{k+1}(x)`,
`H_N(x) = [M_{i+j}(x)]_{i,j=0}^N`, and checks the two positivity conditions a
Stieltjes moment sequence must satisfy (records section 9 / section 16) —
the Hamburger Hankel `[Q_{i+j+1}]` and the Stieltjes Hankel `[Q_{i+j+2}]` —
together with the shifted Schur/Vandermonde determinant identity (section 10).
All four sub-gates (H2a, H2d, H2b/H2c, H2e) pass.

- **H2a (section 17 transform extends to `Q_1..Q_9`).** One Taylor expansion
  of `F_ξ` at each `x` supplies `Q_1..Q_9` through the same finite
  differential transform as H1a, and the result is cross-checked against the
  zero-side: the direct zero sum for `Q_3..Q_9` (fast convergence at 300
  zeros) and the exact log-Ξ moment series for `Q_1, Q_2`, whose `1/γ²`- and
  `1/γ⁴`-tails are not negligible.  Worst relative residual over
  `x ∈ {1/2, 1, 4}` is `1.3e-7`.  Again no `zetazero` call enters `F_ξ`.
- **H2d (section 10 shifted Schur/Vandermonde identity is exact algebra).**
  The shifted Hankel determinant factors as
  `det[Q_{i+j+1}]_{i,j≤N} = Σ_{0≤i_0<…<i_N} (∏_a q_{i_a}) ∏_{a<b}(q_{i_a}−q_{i_b})²`,
  so under RH (`q_ρ` real) every summand is `≥ 0` and `H_N ≥ 0` term by term;
  the `D_m` Vandermonde form is the `N = 1` case.  The identity is algebraic,
  hence holds for any finite multiset of `q`'s (real *or* complex) — the check
  runs on the first 8 zeros, where the brute-force sum over `C(8,4) = 70`
  quadruples is exact (enumerating `C(300,4) ≈ 3.3×10⁸` quadruples over all
  300 zeros is infeasible and unnecessary).  Identity residual `5.8e-67` for
  `N = 1, 2, 3` and `m = 0..3`.
- **H2b/H2c (ladder and both Hankel matrices are positive on the sampled
  half-line).** At every `x ∈ {1/2, 1, 4}` the ladder `D_0..D_3` and all
  leading principal determinants of the Hamburger Hankel `[Q_{i+j+1}]` and the
  Stieltjes Hankel `[Q_{i+j+2}]` are positive through order `N = 3`, computed
  from the explicit formula with no zero-location data.  At `x = 1`:
  `D = (1.891e-9, 2.219e-20, 1.730e-30)`,
  Hamburger `= (2.303e-2, 1.891e-9, 2.028e-22, 1.051e-41)`,
  Stieltjes `= (3.660e-5, 3.675e-15, 2.849e-31, 8.045e-54)`; the Stieltjes
  entries sit strictly below the Hamburger entries they shift, as they must.
  This is sampled evidence consistent with the Stieltjes/Widder positivity,
  not a proof; a negative sample would refute RH.
- **H2e (section 10 obstruction lifts to the full matrix).** A strictly
  dominant synthetic conjugate pair `q_* = e^{±0.7i}` over four real background
  `q_j ∈ [0.025, 0.1]` makes the full shifted Hankel determinant
  `det[Q_{i+j+1}]` negative for `N = 1, 2, 3` — the same off-axis mechanism as
  H1e, but now breaking Stieltjes positivity at the level of the whole matrix
  rather than a single `2×2` shifted minor.

**Honest wall.** H2 is an investigation, not a proof.  The Widder criterion is
posited, positivity is sampled at finitely many `x` and matrix orders
`N ≤ 3`, and the prime–gamma → Hankel bridge (record section 27:
`F_ξ → Q_k → H_N → cᵀH_Nc ≥ 0`) remains open.  What H2 adds is that the first
determinants of H1 are confirmed to be the leading edge of a coherent,
numerically positive Hankel structure, with the determinant algebra (H2d) and
the transform (H2a) pinned exactly.
