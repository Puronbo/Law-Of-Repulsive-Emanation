import Mathlib
import PunoCalculus.RegularityReduction
import PunoCalculus.CriticalLadder
import PunoCalculus.SerrinLadder

/-!
# Prodi-Serrin sufficiency: a finite supercritical control bounds the content

`RegularityReduction.lean` reduces the wall to *boundedness of the critical-content
integral* `int_0^T g` (card C10-open).  This brick supplies the classical **sufficiency
direction** in the register's own `(X, g)` abstraction, and the Serrin-margin arithmetic
that names "supercritical".

* `serrinMargin p q = 1 - (2/q + 3/p)`: the slack over the Serrin line `2/q + 3/p = 1`.
  Positive = strictly supercritical (the assumed `L^p_t L^q_x` control is stronger than
  the scaling-critical route).  It vanishes exactly on the companion `q = q(p)`
  (`serrinMargin_line`) and equals `-(sCrit p + 2/q)` (`serrinMargin_eq_neg_ladder`):
  a positive margin is exactly "above the critical rung".
* `content_le_of_growth_le_weight`: if the log-growth rate is dominated by a weight whose
  *action* `int_0^T w` is finite, then the content is bounded, `X T <= X 0 * exp (R M)`.
  This is the logical kernel of Prodi-Serrin sufficiency -- the PDE supplies the
  pointwise bound `g <= R w` (from the equation) and the finite action `M` (from
  `||u||_{L^p_t L^q_x} < inf`); the register supplies the arithmetic.
* `bounded_on_of_serrinAction`: applied on every `[0, T]`, a finite supercritical control
  forbids finite-time blow-up of the critical content -- the abstract conclusion.

What stays open (card C10-open) is the NS-specific *existence* of that control on the
real flow: this brick proves sufficiency, not the a priori bound.
-/

noncomputable section

open MeasureTheory

namespace PunoCalculus.SerrinSufficiency

/-- The **Serrin margin** `m(p, q) = 1 - (2/q + 3/p)`: the slack over the Serrin line
`2/q + 3/p = 1`.  Positive iff the assumed `L^p_t L^q_x` control is strictly
supercritical. -/
def serrinMargin (p q : ℝ) : ℝ := 1 - (2 / q + 3 / p)

/-- A positive margin is exactly strict supercriticality `2/q + 3/p < 1` (the
arithmetic identity; positivity of `p, q` is what makes it the supercritical regime). -/
theorem serrinMargin_pos_iff {p q : ℝ} :
    0 < serrinMargin p q ↔ 2 / q + 3 / p < 1 := by
  unfold serrinMargin
  constructor <;> intro h <;> linarith

/-- The margin vanishes exactly on the Serrin line: on the companion `q = q(p)` it is
`0`.  So `serrinQ` is the critical (margin-free) route. -/
theorem serrinMargin_line {p : ℝ} (hp0 : p ≠ 0) (hp3 : p ≠ 3) :
    serrinMargin p (PunoCalculus.SerrinLadder.serrinQ p) = 0 := by
  unfold serrinMargin
  rw [PunoCalculus.SerrinLadder.serrinQ_line hp0 hp3]
  ring

/-- The margin is the negative of the critical-ladder sum `sCrit p + 2/q`: `m > 0`
means the assumed control sits strictly above the critical rung. -/
theorem serrinMargin_eq_neg_ladder {p q : ℝ} :
    serrinMargin p q = -(PunoCalculus.CriticalLadder.sCrit p + 2 / q) := by
  unfold serrinMargin PunoCalculus.CriticalLadder.sCrit
  ring

/-- **Prodi-Serrin sufficiency (kernel).**  If the log-growth rate `g` of the critical
content is dominated by a nonnegative weight `w` (`g <= R * w`, `R >= 0`) whose action
over `[0, T]` is finite (`int_0^T w <= M`), then the content is bounded,
`X T <= X 0 * exp (R * M)`.  A finite supercritical control bounds the content -- the
sufficiency direction of the wall, with the PDE supplying `w` and the finite `M`. -/
theorem content_le_of_growth_le_weight {X g w : ℝ → ℝ} {T R M : ℝ}
    (hT : 0 ≤ T) (hX0 : 0 < X 0) (hXT : 0 < X T)
    (hderiv : ∀ t ∈ Set.uIcc 0 T, HasDerivAt (fun s => Real.log (X s)) (g t) t)
    (hcontg : ContinuousOn g (Set.uIcc 0 T))
    (hcontw : ContinuousOn w (Set.uIcc 0 T))
    (hR : 0 ≤ R)
    (hle : ∀ t ∈ Set.uIcc 0 T, g t ≤ R * w t)
    (hint : (∫ t in (0)..T, w t) ≤ M) :
    X T ≤ X 0 * Real.exp (R * M) := by
  apply PunoCalculus.RegularityReduction.content_le_exp_of_integral_le
    hX0 hXT hderiv hcontg
  have hgi : IntervalIntegrable g volume 0 T := hcontg.intervalIntegrable
  have hwi : IntervalIntegrable (fun t => R * w t) volume 0 T :=
    (continuousOn_const.mul hcontw).intervalIntegrable
  have hmono : (∫ t in (0)..T, g t) ≤ ∫ t in (0)..T, R * w t :=
    intervalIntegral.integral_mono_on hT hgi hwi
      (fun x hx => hle x (Set.Icc_subset_uIcc hx))
  have hlin : (∫ t in (0)..T, R * w t) = R * ∫ t in (0)..T, w t :=
    intervalIntegral.integral_const_mul R w
  calc (∫ t in (0)..T, g t) ≤ ∫ t in (0)..T, R * w t := hmono
    _ = R * ∫ t in (0)..T, w t := hlin
    _ ≤ R * M := mul_le_mul_of_nonneg_left hint hR

/-- **No finite-time blow-up under a finite supercritical control.**  If the log-growth
rate is dominated by a nonnegative weight (`g <= R w`, `R >= 0`) whose action is finite
on every `[0, T]`, then the critical content is bounded on every `[0, T]`.  This is the
abstract Prodi-Serrin conclusion; the NS-specific availability of the control stays open
(card C10-open). -/
theorem bounded_on_of_serrinAction {X g w : ℝ → ℝ} {R : ℝ}
    (hR : 0 ≤ R)
    (hX0 : 0 < X 0)
    (hpos : ∀ T, 0 ≤ T → 0 < X T)
    (hderiv : ∀ T, 0 ≤ T → ∀ t ∈ Set.uIcc 0 T,
      HasDerivAt (fun s => Real.log (X s)) (g t) t)
    (hcontg : ∀ T, 0 ≤ T → ContinuousOn g (Set.uIcc 0 T))
    (hcontw : ∀ T, 0 ≤ T → ContinuousOn w (Set.uIcc 0 T))
    (hle : ∀ T, 0 ≤ T → ∀ t ∈ Set.uIcc 0 T, g t ≤ R * w t)
    (haction : ∀ T, 0 ≤ T → ∃ M, (∫ t in (0)..T, w t) ≤ M) :
    ∀ T, 0 ≤ T → ∃ C, X T ≤ C := by
  intro T hT
  obtain ⟨M, hM⟩ := haction T hT
  exact ⟨X 0 * Real.exp (R * M),
    content_le_of_growth_le_weight hT hX0 (hpos T hT) (hderiv T hT)
      (hcontg T hT) (hcontw T hT) hR (hle T hT) hM⟩

/-- Formalised-facts register for `SerrinSufficiency.lean`. -/
def serrinSufficiencyFacts : List String :=
  [ "serrinMargin_pos_iff", "serrinMargin_line", "serrinMargin_eq_neg_ladder",
    "content_le_of_growth_le_weight", "bounded_on_of_serrinAction" ]

/-- The register has exactly five entries. -/
theorem serrinSufficiencyFacts_length : serrinSufficiencyFacts.length = 5 := by decide

end PunoCalculus.SerrinSufficiency
