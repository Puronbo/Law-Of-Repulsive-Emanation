import Mathlib

/-!
# Section 8's dominance condition, formalised (Lean 4, Mathlib)

Machine-checked content behind `rh_widder_hankel_h8.py`'s H8a gate.

For an off-axis zero pair at height `gamma` displaced by `delta`, the zero's
square is

    w = gamma^2 - delta^2 - 2 i delta gamma,

the real zeros of zeta contribute the envelope

    q_real(x, g) = g^2 / (x + g^2)^2,

and the off-axis pair contributes `q_off(x, gamma, delta) = w / (x + w)^2`.

Claims proved here, all of them algebra:

1. `‖w‖ = gamma^2 + delta^2` exactly, independent of any phase.
2. `q_real(x, g) <= 1/(4x)` for `x > 0`, with equality exactly at `g^2 = x`.
   This is AM-GM applied to `x` and `g^2`.
3. Hence the envelope's maximum over `g` is `1/(4x)` and it is attained, so
   dominance at `x = ‖w‖` is an identity rather than a smallness condition
   on `delta`.

Nothing here is numerical.  The measured quantities in the Python artifact --
the largest admissible offset, the bracket `m_lower_bound`/`m_witness` -- are
experiments, not theorems, and are deliberately absent.  This file pins the
algebra the experiments measure; it does not replace them.
-/

namespace PunoCalculus.RH

/-- The square of an off-axis zero at height `gamma` displaced by `delta`.

Written as `Complex.mk` so that `re` and `im` are definitionally the two
coordinates; `wOf_eq` proves it is the polynomial the Python code uses. -/
noncomputable def wOf (gamma delta : ℝ) : ℂ :=
  Complex.mk (gamma ^ 2 - delta ^ 2) (-2 * delta * gamma)

@[simp] theorem re_wOf (gamma delta : ℝ) :
    (wOf gamma delta).re = gamma ^ 2 - delta ^ 2 := rfl

@[simp] theorem im_wOf (gamma delta : ℝ) :
    (wOf gamma delta).im = -2 * delta * gamma := rfl

/-- `wOf` is the polynomial `gamma^2 - delta^2 - 2 i delta gamma` appearing in
`rh_widder_hankel_h8.py`, so the Lean and Python statements are the same
statement and not two lookalikes. -/
theorem wOf_eq (gamma delta : ℝ) :
    wOf gamma delta = gamma ^ 2 - delta ^ 2 - 2 * Complex.I * delta * gamma := by
  apply Complex.ext <;>
    simp [wOf, ← Complex.ofReal_pow, Complex.ofReal_re, Complex.ofReal_im]

/-- The Pythagorean identity `|w|^2 = (gamma^2 + delta^2)^2`.  Pure algebra:
the cross terms cancel. -/
@[simp] theorem normSq_wOf (gamma delta : ℝ) :
    Complex.normSq (wOf gamma delta) = (gamma ^ 2 + delta ^ 2) ^ 2 := by
  rw [Complex.normSq_apply, re_wOf, im_wOf]
  ring

/-- From `a^2 = b^2` with `b >= 0`, conclude `a = |b|`.  Spelling out the factor
pairing explicitly rather than asking `nlinarith` to guess, since the sign
disjunction is exactly where automation tends to give up. -/
private theorem eq_of_sq_eq_sq_abs {a b : ℝ} (ha : 0 ≤ a) (h : a ^ 2 = b ^ 2) :
    a = |b| := by
  have habsq : a ^ 2 = (|b|) ^ 2 := by rw [sq_abs]; exact h
  have hprod : (a - |b|) * (a + |b|) = 0 := by nlinarith
  rcases mul_eq_zero.mp hprod with hc | hc
  · linarith
  · nlinarith [abs_nonneg b]

/-- H8a part 1: `|w| = gamma^2 + delta^2` exactly.

No sign hypotheses are needed: `gamma^2 + delta^2` is non-negative for all real
`gamma, delta`, so the identity holds on all of `R x R`.  The Python code only
ever evaluates it with `gamma, delta >= 0`, but the statement here is the
stronger one and costs nothing. -/
theorem norm_wOf (gamma delta : ℝ) :
    ‖wOf gamma delta‖ = gamma ^ 2 + delta ^ 2 := by
  have hsq : ‖wOf gamma delta‖ ^ 2 = (gamma ^ 2 + delta ^ 2) ^ 2 := by
    rw [Complex.sq_norm, normSq_wOf]
  have hnonneg : 0 ≤ gamma ^ 2 + delta ^ 2 := by positivity
  have := eq_of_sq_eq_sq_abs (norm_nonneg _) hsq
  rwa [abs_of_nonneg hnonneg] at this

/-- H8a part 1, without sign assumptions.  `gamma^2 + delta^2` is non-negative
for real `gamma, delta`, so the absolute value on the right is only a bridge
to the sign-free form. -/
theorem norm_wOf' (gamma delta : ℝ) :
    ‖wOf gamma delta‖ = |gamma ^ 2 + delta ^ 2| := by
  have hsq : ‖wOf gamma delta‖ ^ 2 = (gamma ^ 2 + delta ^ 2) ^ 2 := by
    rw [Complex.sq_norm, normSq_wOf]
  exact eq_of_sq_eq_sq_abs (norm_nonneg _) hsq

/-- The real envelope's contribution from a zero of height `g`. -/
noncomputable def qReal (x g : ℝ) : ℝ := g ^ 2 / (x + g ^ 2) ^ 2

/-- Clearing denominators turns the envelope bound into AM-GM on `x` and `g^2`. -/
theorem qReal_le_iff (hx : 0 < x) :
    qReal x g ≤ 1 / (4 * x) ↔ 4 * x * g ^ 2 ≤ (x + g ^ 2) ^ 2 := by
  have hden : 0 < (x + g ^ 2) ^ 2 := by positivity
  have h4 : (0 : ℝ) < 4 * x := by positivity
  rw [qReal, div_le_iff₀ hden, div_mul_eq_mul_div, le_div_iff₀ h4]
  constructor
  · intro h
    nlinarith [sq_nonneg (x - g ^ 2)]
  · intro h
    nlinarith [sq_nonneg (x - g ^ 2)]

/-- H8a part 2: the real envelope never exceeds `1/(4x)`. -/
theorem qReal_le (hx : 0 < x) :
    qReal x g ≤ 1 / (4 * x) := by
  refine (qReal_le_iff hx).mpr ?_
  nlinarith [sq_nonneg (x - g ^ 2)]

/-- The converse clearing, used to get strictness and the equality case. -/
theorem qReal_ge_iff (hx : 0 < x) :
    1 / (4 * x) ≤ qReal x g ↔ (x + g ^ 2) ^ 2 ≤ 4 * x * g ^ 2 := by
  have hden : 0 < (x + g ^ 2) ^ 2 := by positivity
  have h4 : (0 : ℝ) < 4 * x := by positivity
  rw [qReal, le_div_iff₀ hden, div_mul_eq_mul_div, one_mul, div_le_iff₀ h4]
  constructor
  · intro h
    nlinarith [sq_nonneg (x - g ^ 2)]
  · intro h
    nlinarith [sq_nonneg (x - g ^ 2)]

/-- H8a part 2, sharp: equality holds exactly at `g^2 = x`.  This is what makes
`1/(4x)` the envelope's maximum rather than a loose upper bound. -/
theorem qReal_eq_iff (hx : 0 < x) :
    qReal x g = 1 / (4 * x) ↔ g ^ 2 = x := by
  constructor
  · intro h
    have hkey : (x + g ^ 2) ^ 2 ≤ 4 * x * g ^ 2 :=
      (qReal_ge_iff (g := g) hx).mp (by rw [h])
    nlinarith [sq_nonneg (x - g ^ 2)]
  · intro h
    refine le_antisymm ?_ ?_
    · apply (qReal_le_iff (g := g) hx).mpr
      rw [← h]
      exact le_of_eq (by ring)
    · apply (qReal_ge_iff (g := g) hx).mpr
      rw [← h]
      exact le_of_eq (by ring)

/-- The envelope maximum `1/(4x)` is attained at `g^2 = x`, restated directly so
the "maximum" claim does not rest on reading `qReal_eq_iff` backwards. -/
theorem qReal_max_attained (x g : ℝ) (hx : 0 < x) (h : g ^ 2 = x) :
    qReal x g = 1 / (4 * x) := (qReal_eq_iff hx).mpr h

/-- And the attainment point is the only one: away from `g^2 = x` the envelope
is strictly below `1/(4x)`. -/
theorem qReal_lt_of_ne (hx : 0 < x) (h : g ^ 2 ≠ x) :
    qReal x g < 1 / (4 * x) := by
  refine lt_of_le_of_ne (qReal_le hx) ?_
  intro hc
  exact h ((qReal_eq_iff hx).mp hc)

/-- Summarised the way H8a reports it: for `x > 0` the real envelope never
exceeds `1/(4x)`, hits it exactly at `g^2 = x`, and is strictly below it
elsewhere. -/
theorem qReal_envelope (hx : 0 < x) :
    qReal x g ≤ 1 / (4 * x) ∧ (qReal x g = 1 / (4 * x) ↔ g ^ 2 = x) :=
  ⟨qReal_le hx, qReal_eq_iff hx⟩

end PunoCalculus.RH
