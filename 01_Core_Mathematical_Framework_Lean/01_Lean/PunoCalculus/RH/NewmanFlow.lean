import Mathlib
import PunoCalculus.RH.Hankel

/-!
# The de Bruijn–Newman flow: the unconditional positivity layer

`PunoCalculus.RH.Hankel` proves the record section 9/16 criterion exactly:

  `cᵀHc = ∑_j q_j P(q_j)²`

together with its sufficiency direction (`quadFormR_nonneg`).  That algebra is
correct, and it is also **vacuous as a criterion**, because its nonnegativity
requires `q_j ≥ 0` for every atom, and that is RH itself.  `quadForm_nonneg_of_real`
in `Hankel.lean` therefore has `hq : ∀ j, 0 ≤ qs j` as a *hypothesis*.  A
criterion whose proof of nonnegativity assumes the conclusion cannot decide
anything.

Record section 28 asks for an operator `T` with an invariant whose fixed points
force the axis.  The operator that already does this is the de Bruijn–Newman
flow (de Bruijn 1950, Newman 1976, Rodgers–Tao 2018):

  `Φ(u)   = ∑_n (2π²n⁴e^{9u} − 3πn²e^{5u}) exp(−πn²e^{4u})`
  `H_t(z) = ∫₀^∞ e^{tu²} Φ(u) cos(zu) du`,  `H_0(z) = ⅛ ξ(½ + iz/2)`
  `∂_t H_t = −∂_{zz} H_t`

whose zeros `x_j(t)` satisfy `dx_j/dt = −2 ∑_{k≠j} 1/(x_k − x_j)`, and whose
energy is

  `E(t) = ∑_{j≠k} 1/|x_j − x_k|²`.

`E` is a sum of squares whose nonnegativity is **unconditional**: it holds for
every configuration of real points, with no hypothesis on the zeros.  That is
the structural difference from the Hankel form, and this file records it.

## What is proved here

Only the RH-free finite algebra, which needs no analytic number theory:

  * `energy_nonneg` — unconditional, for any real configuration;
  * `energyPair_pos` — strictly positive once the two points differ;
  * `odeRhs_eq_neg` — the zero ODE's right-hand side, shown to be a repulsion,
    i.e. `−2/(x_k − x_j) = 2/(x_j − x_k)`.  This is the sign that does real work;
  * `odeSum_pair`, `odeSum_two` — the two-sided symmetry `1/(a−b) + 1/(b−a) = 0`,
    i.e. why a *two-sided* progression is an equilibrium;
  * `oneSided_defect_ne_zero` — and the negative control that a *one-sided*
    finite window is **not** an equilibrium.  This is not a technicality: it is
    why `E` and `H` diverge in the infinite-zero limit and need truncation plus
    renormalisation;
  * `hankel_criterion_needs_atom_nonneg` — the contrast, on the two-point
    configuration `q = (−1, 1)`, in one statement.

## What is NOT proved here

Nothing about `Φ`, `H_t`, the zeta zeros, or `Λ`.  Those are analytic and are
handled numerically in `experiments/rh_newman_flow_h1.py`.  In particular this
file does **not** prove `Λ ≤ 0`, which is equivalent to RH; Rodgers–Tao proved
`Λ ≥ 0` and the opposite inequality is open.  A sign correction is recorded in
the experiment: the exact two-zero flow gives `∂_t E < 0` and `∂_t² E > 0`, so
`E` is decreasing and convex, and the manifestly non-negative sum of squares is
`−∂_t E` rather than `∂_t E`.

## Note on Lean style

Numerals inside `if … else …` terms are written `(0 : ℝ)` / `(1 : ℝ)` /
`(2 : ℝ)` rather than bare `0`.  With a bare numeral and no expected type
propagating through a binder, `ite` elaboration degrades the expected type to
`Sort ?u`, which then cascades into `AddCommMonoid Prop` and
`OfNat (Sort ?u) 0`.  This is an elaboration-order artefact, not a mathematical
obstacle.
-/

namespace PunoCalculus.RH.NewmanFlow

open PunoCalculus.RH

variable {n : ℕ}

/-- The de Bruijn–Newman energy of a finite zero configuration,
`E = ∑_{j≠k} 1/|x_j − x_k|²`, summed over ordered pairs. -/
noncomputable def energy (x : Fin n → ℝ) : ℝ :=
  ∑ j : Fin n,
    ∑ k : Fin n, if j ≠ k then (1 : ℝ) / (x j - x k) ^ 2 else (0 : ℝ)

/-- **Unconditional.**  The energy is non-negative for *every* configuration of
real points — no assumption about the `x_j`, in particular none about positivity
or about the critical line.  This is the property the Hankel form lacks. -/
theorem energy_nonneg (x : Fin n → ℝ) : 0 ≤ energy x := by
  refine Finset.sum_nonneg fun j _ => ?_
  refine Finset.sum_nonneg fun k _ => ?_
  by_cases h : j ≠ k
  · simp only [if_pos h]
    exact div_nonneg (by norm_num) (sq_nonneg _)
  · simp [h]

/-- The two-point energy, `2/(a−b)²`, as it appears when `n = 2`. -/
noncomputable def energyPair (a b : ℝ) : ℝ := 2 / (a - b) ^ 2

/-- Strict positivity once the two points are distinct. -/
theorem energyPair_pos {a b : ℝ} (h : a ≠ b) : 0 < energyPair a b := by
  unfold energyPair
  have h2 : (0 : ℝ) < (a - b) ^ 2 := by
    rw [sq]
    exact mul_self_pos.mpr (sub_ne_zero.mpr h)
  exact div_pos (by norm_num) h2

/-- The right-hand side of the de Bruijn–Newman zero ODE,
`dx_j/dt = −2 ∑_{k≠j} 1/(x_k − x_j)`.  The `−2` sits inside the summand so no
distributivity lemma is needed downstream. -/
noncomputable def odeRhs (x : Fin n → ℝ) (j : Fin n) : ℝ :=
  ∑ k : Fin n, if j ≠ k then (-2 : ℝ) / (x k - x j) else (0 : ℝ)

/-- The sign, established without hypotheses: the ODE is a *repulsion*.
`2/(x_j − x_k) = −2/(x_k − x_j)` holds in `ℝ` because
`−a/b = a/(−b)`, with no distinctness needed (`1/0 = 0` on both sides). -/
theorem odeRhs_eq_neg (x : Fin n → ℝ) (j : Fin n) :
    odeRhs x j = ∑ k : Fin n, if j ≠ k then (2 : ℝ) / (x j - x k) else (0 : ℝ) := by
  refine Finset.sum_congr rfl fun k _ => ?_
  by_cases h : j ≠ k
  · simp only [if_pos h]
    calc (-2 : ℝ) / (x k - x j)
        = -(2 / (x k - x j)) := by rw [neg_div]
      _ = -(2 / -(x j - x k)) := by rw [show x k - x j = -(x j - x k) from by ring]
      _ = -(-(2 / (x j - x k))) := by rw [div_neg]
      _ = 2 / (x j - x k) := by rw [neg_neg]
  · simp [h]

/-- Two-sided symmetry: the two-point window cancels exactly, so a two-sided
progression is an equilibrium of the ODE. -/
theorem odeSum_pair (a b : ℝ) : 1 / (b - a) + 1 / (a - b) = 0 := by
  have h : 1 / (b - a) = -(1 / (a - b)) := by
    rw [show b - a = -(a - b) from by ring, div_neg]
  rw [h]
  ring

/-- The same statement aggregated over `Fin 2`, i.e. the full ODE sum vanishes. -/
theorem odeSum_two (x : Fin 2 → ℝ) :
    (∑ j : Fin 2, ∑ k : Fin 2,
      if j ≠ k then (1 : ℝ) / (x k - x j) else (0 : ℝ)) = 0 := by
  have h0 : (∑ k : Fin 2, if (0 : Fin 2) ≠ k then (1 : ℝ) / (x k - x 0) else (0 : ℝ))
      = 1 / (x 1 - x 0) := by simp
  have h1 : (∑ k : Fin 2, if (1 : Fin 2) ≠ k then (1 : ℝ) / (x k - x 1) else (0 : ℝ))
      = 1 / (x 0 - x 1) := by simp
  have hsplit :
      (∑ j : Fin 2, ∑ k : Fin 2,
        if j ≠ k then (1 : ℝ) / (x k - x j) else (0 : ℝ))
        = (∑ k : Fin 2, if (0 : Fin 2) ≠ k then (1 : ℝ) / (x k - x 0) else (0 : ℝ))
          + (∑ k : Fin 2, if (1 : Fin 2) ≠ k then (1 : ℝ) / (x k - x 1) else (0 : ℝ)) := by
    simp
  rw [hsplit, h0, h1, odeSum_pair]

/-- **Negative control.**  A *one-sided* finite window is **not** an
equilibrium: with `x = (0, 1, 2)` the ODE sum at `j = 0` is `H_2 = 3/2`, not
`0`.  This is why `E` and `H` are divergent as the zero count grows and why
Rodgers–Tao must truncate and renormalise; the equilibrium statement is only
true for a two-sided window in principal-value sense. -/
theorem oneSided_defect_ne_zero
    (x : Fin 3 → ℝ) (h0 : x 0 = 0) (h1 : x 1 = 1) (h2 : x 2 = 2) :
    (∑ k : Fin 3, if (0 : Fin 3) ≠ k then (1 : ℝ) / (x k - x 0) else (0 : ℝ)) = 3 / 2 := by
  have hsplit :
      (∑ k : Fin 3, if (0 : Fin 3) ≠ k then (1 : ℝ) / (x k - x 0) else (0 : ℝ))
        = 1 / (x 1 - x 0) + 1 / (x 2 - x 0) := by
    simp [Fin.sum_univ_succ]
  rw [hsplit, h1, h0, h2]
  norm_num

/-- The contrast, in one statement: on the two-point configuration
`q = (−1, 1)` the record section 9/16 quadratic form takes **both** signs.

`MR q 0 = −1 + 1 = 0`, `MR q 1 = 1 + 1 = 2`, `MR q 2 = −1 + 1 = 0`, so the
`2 × 2` block is `[[0, 2], [2, 0]]` with eigenvalues `±2`.  Hence
`quadFormR` is indefinite here, and no positivity statement about it can be
made without the hypothesis `0 ≤ q`, which is precisely RH.

The *same two points* as an energy configuration give `energyPair (−1, 1) = 1/2 > 0`
unconditionally (`hankel_contrast_energy`). -/
theorem hankel_criterion_needs_atom_nonneg :
    quadFormR (![(-1 : ℝ), 1]) (![1, -1]) = -4 ∧
      quadFormR (![(-1 : ℝ), 1]) (![1, 1]) = 4 := by
  constructor <;> simp [quadFormR, MR] <;> norm_num

/-- The unconditional counterpart: the same configuration has positive energy. -/
theorem hankel_contrast_energy : 0 < energyPair (-1) 1 :=
  energyPair_pos (by norm_num)

/-! ### The general-`n` closed form for `∂_t E`

Everything above is finite algebra at `n = 2, 3`.  What the infinite-order step
actually needs is the *identity* behind gate `n2a` of
`experiments/rh_newman_flow_h2.py`:

    ∂_t E = −4 ∑_{j≠k} (S_j − S_k) / (x_j − x_k)³,   S_j = ∑_{k≠j} 1/(x_j − x_k)

with no differentiation and no renormalisation.  It holds because the ODE gives
`d/dt (x_j − x_k) = 2(S_j − S_k)`, and each summand of `E` is `(x_j − x_k)⁻²`.

Note that the summand is `−2·(ẋ_j − ẋ_k)/(x_j − x_k)³`, an *unsimplified*
chain rule: it is what one gets by differentiating one ordered pair and is
correct without any distinctness hypothesis (`1/0 = 0` throughout).  Substituting
the ODE is the whole content of the next theorem. -/

/-- The slope sum `S_j = ∑_{k≠j} 1/(x_j − x_k)`. -/
noncomputable def slopeSum (x : Fin n → ℝ) (j : Fin n) : ℝ :=
  ∑ k : Fin n, if j ≠ k then (1 : ℝ) / (x j - x k) else (0 : ℝ)

/-- The ODE right-hand side is `2 S_j`: the repulsion of `odeRhs_eq_neg`,
written with the sum collected. -/
theorem odeRhs_eq_two_slopeSum (x : Fin n → ℝ) (j : Fin n) :
    odeRhs x j = 2 * slopeSum x j := by
  rw [odeRhs_eq_neg]
  unfold slopeSum
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun k _ => ?_
  by_cases h : j ≠ k
  · simp only [if_pos h]
    ring
  · simp [h]

/-- The time derivative of `E`, as the unsimplified chain rule on one ordered
pair: `−2(ẋ_j − ẋ_k)/(x_j − x_k)³`. -/
noncomputable def energyDeriv (x v : Fin n → ℝ) : ℝ :=
  ∑ j : Fin n,
    ∑ k : Fin n, if j ≠ k then (-2 : ℝ) * (v j - v k) / (x j - x k) ^ 3 else (0 : ℝ)

/-- The closed form of the same quantity, with the ODE substituted in. -/
noncomputable def energyDerivClosed (x : Fin n → ℝ) : ℝ :=
  ∑ j : Fin n,
    ∑ k : Fin n,
      if j ≠ k then (-4 : ℝ) * (slopeSum x j - slopeSum x k) / (x j - x k) ^ 3
      else (0 : ℝ)

/-- **The general-`n` identity.**  If the configuration moves with velocity
`ẋ_j = 2 S_j` — which is exactly the de Bruijn–Newman zero ODE — then the
derivative of the energy is the closed form, for *every* `n` and with no
renormalisation term.

This is gate `n2a`, which the experiment checks numerically at `n = 2..8` by
differentiating the ODE term by term.  The statement is proved here for all `n`,
and it is unconditional: no injectivity or distinctness hypothesis is needed
because both sides are `0` whenever `x_j = x_k`. -/
theorem energyDeriv_eq_closed (x v : Fin n → ℝ) (h : ∀ j, v j = 2 * slopeSum x j) :
    energyDeriv x v = energyDerivClosed x := by
  unfold energyDeriv energyDerivClosed
  refine Finset.sum_congr rfl fun j _ => ?_
  refine Finset.sum_congr rfl fun k _ => ?_
  by_cases hjk : j ≠ k
  · simp only [if_pos hjk]
    have hv : v j - v k = 2 * (slopeSum x j - slopeSum x k) := by
      rw [h j, h k]
      ring
    rw [hv]
    congr 1
    ring
  · simp [hjk]

/-- The exact two-zero value: `S_0 − S_1 = 2/(x_0 − x_1)`, and the two ordered
pairs contribute equally, giving `∂_t E = −16/(x_0 − x_1)⁴`. -/
theorem energyDerivClosed_two (x : Fin 2 → ℝ) (h : x 0 - x 1 ≠ 0) :
    energyDerivClosed x = -16 / (x 0 - x 1) ^ 4 := by
  have hs0 : slopeSum x 0 = 1 / (x 0 - x 1) := by simp [slopeSum]
  have hs1 : slopeSum x 1 = 1 / (x 1 - x 0) := by simp [slopeSum]
  have hsplit :
      (∑ j : Fin 2, ∑ k : Fin 2,
        if j ≠ k then (-4 : ℝ) * (slopeSum x j - slopeSum x k) / (x j - x k) ^ 3
        else (0 : ℝ))
        = (-4 * (slopeSum x 0 - slopeSum x 1) / (x 0 - x 1) ^ 3)
          + (-4 * (slopeSum x 1 - slopeSum x 0) / (x 1 - x 0) ^ 3) := by
    simp
  have h' : x 1 - x 0 ≠ 0 := by
    intro hc
    apply h
    linarith
  rw [energyDerivClosed, hsplit, hs0, hs1]
  field_simp
  ring

/-- …and it is **negative**, which is gate `n2b` at `n = 2`: the energy strictly
decreases for two distinct zeros.  For `n = 2` the sign comes from a genuine
fourth power, not from an inequality that is merely believed. -/
theorem energyDerivClosed_two_neg (x : Fin 2 → ℝ) (h : x 0 - x 1 ≠ 0) :
    energyDerivClosed x < 0 := by
  rw [energyDerivClosed_two x h]
  have h4 : (0 : ℝ) < (x 0 - x 1) ^ 4 := by positivity
  have : (-16 : ℝ) / (x 0 - x 1) ^ 4 < 0 := div_neg_of_neg_of_pos (by norm_num) h4
  simpa using this

/-! ### What this does *not* give

`energyDeriv_eq_closed` is an identity, not an inequality.  For `n ≥ 3` the sign
of `∂_t E` is the sign of `−4 ∑_{j≠k} (S_j − S_k)/(x_j − x_k)³`, which balances
positive pair terms against negative triple terms and is **not** a termwise
non-negative sum.  The experiment checks `∂_t E ≤ 0` over tens of thousands of
configurations, but no proof and no sum-of-squares certificate is given here or
there.  So `energyDerivClosed_two_neg` above is the *only* sign result in this
file, and generalising it to `n ≥ 3` is precisely the open part. -/

/-- **The energy cannot see an absolute position.**  `E` depends only on the
differences `x_j − x_k`, so translating *every* zero by the same constant leaves it
exactly unchanged.

What this licenses is narrow and should not be overstated.  It proves that the
*value* of `energy` carries no information about the common offset of the zeros.
It does **not** by itself prove that no energy argument can ever bear on `Λ`:
`Λ` is a threshold for a statement that is itself translation-covariant (shifting
all zeros by a real constant preserves whether they are all real), and the
threshold could in principle still be read off from how `E` *evolves* or from the
boundary data, where absolute position enters through the ODE even though the
energy value does not.  So the honest conclusion is: a purely pointwise energy
inequality evaluated on one configuration is blind to offset, and any route from
energy to `Λ` has to supply the offset information some other way.

What does decide it is spacing: Rodgers–Tao obtain `Λ ≥ 0` by showing that
`Λ < 0` would force the zeros of `H_0` to be locally close to equally spaced,
which contradicts Montgomery pair correlation.  The relevant object is therefore
the *equidistant* configuration.

A caution, since it is easy to overstate what `odeSum_pair` and `odeSum_two`
give.  They establish `∑_j ẋ_j = 0`: the **centroid** is conserved exactly.  They
do **not** make a two-sided arithmetic progression a fixed point of the ODE — for
an equidistant configuration the individual velocities are `ẋ_j = 2∑_{k≠j}1/(x_j−x_k)`,
which is nonzero (outward drift, of order `log n` at the endpoints).  Equidistance
and being a configuration fixed point are different properties; only the former is
what the spacing argument uses. -/
theorem energy_translationInvariant (x : Fin n → ℝ) (c : ℝ) :
    energy (fun j => x j + c) = energy x := by
  unfold energy
  refine Finset.sum_congr rfl fun j _ => ?_
  refine Finset.sum_congr rfl fun k _ => ?_
  by_cases h : j ≠ k
  · simp only [if_pos h]
    have hd : (x j + c) - (x k + c) = x j - x k := by ring
    rw [hd]
  · simp [h]

/-! ### `i²` and an exact reformulation of `Λ ≤ 0`

There is a clean way to state "all zeros of `H_0` are real" that puts `i² = −1`
at the centre rather than treating it as bookkeeping.  Write the offset of a
zero from the critical line as `ρ − ½ = a + bi`, so `a = β − ½` and `b = γ`.
Expanding with `i² = −1`,

    `(ρ − ½)² = (a² − b²) + 2abi`,

so the imaginary part of the square is exactly `2ab`.  Since
`ρ² − ρ + ¼ = (ρ − ½)²`, it follows that

    RH  ⟺  for every zero `ρ`,  `ρ² − ρ + ¼` is real and negative  ⟺  `Λ ≤ 0`.

The negativity is not decoration.  On the critical line the square is `−γ² < 0`
for a nontrivial zero, whereas a *real* zero of `ζ` — so `b = 0` — gives `a² ≥ 0`.
The condition is therefore strictly stronger than "no real zeros", which is a
different and much easier statement: `ζ` has the trivial real zeros `−2,−4,…`.

The structural fact behind it is `sq_im_eq_zero_iff`: a square is real exactly
when the number lies on one of the two axes.  `i² = −1` is what makes those two
axes interchangeable, since the very same relation sends `i` to the real
direction `−1`.  This is why `i²` is not an accident of notation here.

Note the genuine limitation: this reformulation is an *equivalence*, so it
relocates the difficulty into "every zero has real square" and settles nothing on
its own.  What it does supply is the exact algebraic predicate that an off-line
zero must violate, which is the `2ab` computed in `sq_im` below. -/

/-- **A square is real exactly when the number is real or purely imaginary.**
This is where `i² = −1` does the work: for `z = a + bi` one has
`z² = (a² − b²) + 2abi`, so `z²` is real iff `2ab = 0`, i.e. iff `a = 0` or
`b = 0`.  In Newman terms `a = 0` means the zero lies on the critical line and
`b = 0` means it is real. -/
theorem sq_im (a b : ℝ) :
    Complex.im (((a : ℂ) + Complex.I * b) ^ 2) = 2 * a * b := by
  simp only [pow_two, Complex.add_im, Complex.mul_im, Complex.I_im, Complex.I_re,
    Complex.ofReal_im, Complex.ofReal_re, Complex.add_re, Complex.mul_re]
  ring

/-- The square `(ρ − ½)²` is real exactly on the union of the two axes. -/
theorem sq_im_eq_zero_iff (a b : ℝ) :
    Complex.im (((a : ℂ) + Complex.I * b) ^ 2) = 0 ↔ a = 0 ∨ b = 0 := by
  rw [sq_im a b]
  constructor
  · intro h
    have h0 : (2 : ℝ) * a * b = 0 := by linarith
    rcases mul_eq_zero.mp h0 with h1 | h2
    · exact Or.inl (by nlinarith)
    · exact Or.inr h2
  · intro h
    rcases h with rfl | rfl <;> ring

/-- On the critical line, the quadratic invariant collapses to a negative real:
for `ρ = ½ + iγ`, `(ρ − ½)² = −γ²`.  This is the `i² = −1` step: the `iγ`
squared is `−γ²`, which is real and non-positive. -/
theorem crit_line_sq (g : ℝ) :
    (((1 / 2 : ℂ) + Complex.I * g - (1 / 2 : ℂ)) ^ 2) = -(g ^ 2 : ℂ) := by
  have h1 : (1 / 2 : ℂ) + Complex.I * g - (1 / 2 : ℂ) = Complex.I * g := by ring
  have hI : (Complex.I : ℂ) ^ 2 = -1 := by
    calc Complex.I ^ 2 = Complex.I * Complex.I := by ring
      _ = -1 := Complex.I_mul_I
  rw [h1, mul_pow, hI]
  ring

/-- …and off the critical line it is not real: with `β ≠ ½` and `γ ≠ 0` the
imaginary part `2ab = 2γ(β − ½)` survives.  So "real square" detects the critical
line, which is what the `RH ⟺ Λ ≤ 0` reformulation rests on. -/
theorem crit_line_sq_of_real (a b : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) :
    Complex.im (((a : ℂ) + Complex.I * b) ^ 2) ≠ 0 :=
  fun h => by
    rcases (sq_im_eq_zero_iff a b).mp h with h | h
    · exact ha h
    · exact hb h

/-- **The sharp form, which is exactly RH.**  For a *nontrivial* zero the
imaginary part `b = γ` is nonzero, so the `b = 0` branch of `sq_im_eq_zero_iff`
is excluded and only `a = 0` remains.  Writing the offset from the critical line
as `w = ρ − ½ = a + bi`:

    `w² real  ⟺  a = 0  ⟺  ρ = ½ + iγ  ⟺  z = −2iw = 2γ is real  ⟺  RH`.

The last step uses `z = (2ρ − 1)/i = −2i·w`, so `z` is real exactly when `w` is
purely imaginary.  Note the asymmetry that makes this non-trivial: without
`b ≠ 0` the equivalence fails, because `b = 0` is a *real* zero of `ζ`, which is
a different thing entirely from a zero on the critical line. -/
theorem nontrivial_sq_real_iff_on_crit_line (a b : ℝ) (hb : b ≠ 0) :
    Complex.im (((a : ℂ) + Complex.I * b) ^ 2) = 0 ↔ a = 0 := by
  constructor
  · intro h
    rcases (sq_im_eq_zero_iff a b).mp h with ha | hb'
    · exact ha
    · exact absurd hb' hb
  · intro ha
    subst ha
    exact (sq_im_eq_zero_iff 0 b).mpr (Or.inl rfl)

/-! ### N5: the convergent Hadamard detector

Sections N1-N4 built *energy* sums, and every one of them diverges: the
de Bruijn-Newman energy `Σ_{j≠k} 1/|x_j - x_k|²` is infinite for an infinite
zero set, the `n`-particle truncations have no uniform bound, and the `i²`
experiment showed the squared-energy variant is even *negative* for the complex
configuration `z = ±ib`.  Energy was the wrong object.

Hadamard's product gives a sum that **converges**.  For a nontrivial zero `ρ`,

  `Σρ 2/(ρ(1-ρ)) = 2 + γ_E - log(4π)`   (both members of each pair `{ρ, 1-ρ}`)

and since `ρ(1-ρ) = 1/4 - (ρ - 1/2)²`, the denominator is precisely the
quadratic that `sq_im_eq_zero_iff` uses to detect the critical line.  The `i²`
criterion and the convergent series share one quadratic; that is the structural
bridge proved below in `rho_one_minus_rho`.

Taking the imaginary part turns the series into an off-line **signature**

  `Φ = Im[1/(ρ(1-ρ))] = 2ab/(u² + 4a²b²)`,   `u = 1/4 - a² + b²`,

with `ρ = 1/2 + a + bi`.  `Φ` vanishes exactly on the two axes, is odd in `a`,
and for large `b` equals `2a/b³` to leading order: linear in the displacement
from the critical line, with a gain that *grows* like `1/b³`.

`Φ` is a refutation device, not a proof.  `ΣΦ ≠ 0` would refute RH; `ΣΦ = 0` is
consistent with RH and with symmetric off-line pairs, and proves nothing.  This
file therefore proves the algebra exactly and claims nothing about the zero sum. -/

/-- Real part of `u + iv`. -/
theorem re_add_I_mul (u v : ℝ) : ((u : ℂ) + Complex.I * v).re = u := by
  simp only [Complex.add_re, Complex.ofReal_re, Complex.ofReal_im, Complex.mul_re,
    Complex.I_re]
  ring

/-- Imaginary part of `u + iv`. -/
theorem im_add_I_mul (u v : ℝ) : ((u : ℂ) + Complex.I * v).im = v := by
  simp only [Complex.add_im, Complex.ofReal_im, Complex.ofReal_re, Complex.mul_im,
    Complex.I_im]
  ring

/-- `normSq (u + iv) = u² + v²`: the denominator that makes the reciprocal real
up to one division. -/
theorem normSq_add_I_mul (u v : ℝ) :
    Complex.normSq ((u : ℂ) + Complex.I * v) = u ^ 2 + v ^ 2 := by
  rw [Complex.normSq_apply, re_add_I_mul, im_add_I_mul]
  ring

/-- **The reciprocal rule.**  `1/(u + iv) = (u - iv)/(u² + v²)`, so its imaginary
part is `-v/(u² + v²)`.  This is the whole source of the signature below: the
`i²` quadratic appears in the *denominator*, and `Im` extracts it. -/
theorem im_one_div_add_I_mul (u v : ℝ) (h : u ^ 2 + v ^ 2 ≠ 0) :
    Complex.im (1 / ((u : ℂ) + Complex.I * v)) = -v / (u ^ 2 + v ^ 2) := by
  rw [Complex.div_im]
  simp only [Complex.one_re, Complex.one_im, re_add_I_mul, im_add_I_mul,
    normSq_add_I_mul]
  field_simp
  ring

/-- **The structural bridge from `i²` to the Hadamard denominator.**  For a zero
`ρ = 1/2 + (a + bi)`,

  `ρ(1 - ρ) = 1/4 - (ρ - 1/2)²`.

The very quadratic that `sq_im_eq_zero_iff` uses to *detect* the critical line
is the quadratic that appears in the denominator of the convergent Hadamard
series.  `i²` supplies the criterion; the Hadamard product supplies convergence. -/
theorem rho_one_minus_rho (a b : ℝ) :
    ((1 / 2 : ℂ) + (a + Complex.I * b)) * ((1 / 2 : ℂ) - (a + Complex.I * b))
      = (1 / 4 : ℂ) - ((a : ℂ) + Complex.I * b) ^ 2 := by
  have hI : (Complex.I : ℂ) ^ 2 = -1 := by
    calc Complex.I ^ 2 = Complex.I * Complex.I := by ring
      _ = -1 := Complex.I_mul_I
  calc _ = (((a + 1 / 2 : ℝ) : ℂ) + Complex.I * b) * (((1 / 2 - a : ℝ) : ℂ) - Complex.I * b) := by
        push_cast
        ring
    _ = _ := by
      ring_nf
      rw [hI]
      push_cast
      ring

/-- The same quadratic expanded into real and imaginary parts:
`1/4 - (a + bi)² = (1/4 - a² + b²) + i(-2ab)`. -/
theorem offset_sq_expand (a b : ℝ) :
    (1 / 4 : ℂ) - ((a : ℂ) + Complex.I * b) ^ 2
      = ((1 / 4 - a ^ 2 + b ^ 2 : ℝ) : ℂ) + Complex.I * ((-2 * a * b : ℝ) : ℂ) := by
  have hI : (Complex.I : ℂ) ^ 2 = -1 := by
    calc Complex.I ^ 2 = Complex.I * Complex.I := by ring
      _ = -1 := Complex.I_mul_I
  have h2 : (1 / 4 : ℂ) - ((a : ℂ) + Complex.I * b) ^ 2
      = ((1 / 4 - a ^ 2 + b ^ 2 : ℝ) : ℂ) + Complex.I * (-2 * (a : ℝ) * b) := by
    calc _ = (1 / 4 : ℂ) - (((a : ℂ) + Complex.I * b) * ((a : ℂ) + Complex.I * b)) := by
          ring
      _ = _ := by
        ring_nf
        rw [hI]
        push_cast
        ring
  rw [h2]
  push_cast
  ring

/-- **The N5 signature, exactly.**  For the offset `w = ρ - 1/2 = a + bi` the
denominator is `ρ(1-ρ) = 1/4 - w² = u + i(-2ab)` with `u = 1/4 - a² + b²`, so

  `Φ = Im[1/(ρ(1-ρ))] = 2ab/(u² + 4a²b²)`.

This is the whole detector in one formula: it vanishes exactly on the two axes,
it is odd in `a`, and for large `b` it is `2a/b³`, i.e. linear in the off-line
displacement with a gain that grows like `1/b³`.  Note what is *not* claimed:
this is one zero's contribution.  The series `ΣΦ` is not evaluated here, and its
vanishing would refute nothing. -/
theorem phi_signature (a b : ℝ)
    (h : (1 / 4 - a ^ 2 + b ^ 2) ^ 2 + 4 * a ^ 2 * b ^ 2 ≠ 0) :
    Complex.im
        (1 / (((1 / 2 : ℂ) + (a + Complex.I * b)) * ((1 / 2 : ℂ) - (a + Complex.I * b))))
      = 2 * a * b / ((1 / 4 - a ^ 2 + b ^ 2) ^ 2 + 4 * a ^ 2 * b ^ 2) := by
  have hsq : (-2 * a * b) ^ 2 = 4 * a ^ 2 * b ^ 2 := by ring
  have h' : (1 / 4 - a ^ 2 + b ^ 2) ^ 2 + (-2 * a * b) ^ 2 ≠ 0 := by
    rw [hsq]
    exact h
  rw [rho_one_minus_rho a b, offset_sq_expand a b]
  have e := im_one_div_add_I_mul (1 / 4 - a ^ 2 + b ^ 2) (-2 * a * b) h'
  rw [hsq] at e
  convert e using 1
  all_goals ring_nf

end PunoCalculus.RH.NewmanFlow
