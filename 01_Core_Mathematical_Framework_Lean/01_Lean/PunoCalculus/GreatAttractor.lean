import PunoCalculus.CriticalLadder
import PunoCalculus.ZeroFixedPoint

/-!
# The great attractor: orientation of a fixed point, and order meets the ladder

This extends the "zero as the self-defining point" brick
(`PunoCalculus.ZeroFixedPoint`) in two directions:

* **Orientation — "orient the great attractor where it repels the known
  universe from itself."** At a fixed point `T x₀ = x₀` with derivative `L`, the
  distance ratio `|T x - x₀| / |x - x₀|` tends to `|L|`
  (`fixedPoint_distanceRatio`).  Hence the point **repels** nearby points
  (`|T x - x₀| > |x - x₀|`) when `|L| > 1` (`fixedPoint_repels`) and **attracts**
  them (`|T x - x₀| < |x - x₀|`) when `|L| < 1` (`fixedPoint_attracts`).  The
  orientation of the single fixed point is exactly the classical trichotomy of
  `|L|` (`orientation_trichotomy`); "the great attractor that repels" is the
  `|L| > 1` branch.

* **Order meets the critical ladder — "it scales itself on how many zeros it
  has."** The order of vanishing `a` is the amplitude scaling weight.  Under the
  NS-type rescaling `u_λ(x) = λ^a u(λ x)` the homogeneous norm `Ḣ^s_p` carries
  factor `λ^{a + s - 3/p}` (`scalingWeight`), which is scale-invariant exactly on
  `s = criticalSmoothness a p = 3/p - a` (`scalingWeight_zero_iff`).  The
  register's critical ladder is the **order-one** rung:
  `criticalSmoothness 1 p = sCrit p` (`criticalSmoothness_one`); raising the
  order by one lowers the required smoothness by one
  (`criticalSmoothness_shift_order`).  So the single invariant
  (`CriticalLadder.lean`) is the one-zero form of the number-of-zeros family.

Scope is bounded as in `PunoCalculus.Removable`: the orientation statements are
eventual statements on the punctured neighbourhood, never values AT the point.
-/

noncomputable section

namespace PunoCalculus.GreatAttractor

open Filter
open scoped Topology
open PunoCalculus.CriticalLadder (sCrit)

/-! ## Orientation: repelling and attracting fixed points -/

/-- The distance ratio at a fixed point: `|T x - x₀| / |x - x₀| -> |L|`, where
`L` is the derivative of `T` at the fixed point `T x₀ = x₀`.  This is the
magnitude of the local linear expansion (or contraction) about the point. -/
theorem fixedPoint_distanceRatio {T : ℝ → ℝ} {L x₀ : ℝ}
    (hT : HasDerivAt T L x₀) (hfix : T x₀ = x₀) :
    Tendsto (fun x : ℝ => |T x - x₀| / |x - x₀|) (𝓝[≠] x₀) (𝓝 |L|) := by
  have hslope : Tendsto (fun x : ℝ => |slope T x₀ x|) (𝓝[≠] x₀) (𝓝 |L|) :=
    hT.tendsto_slope.abs
  have heq : (fun x : ℝ => |T x - x₀| / |x - x₀|) =ᶠ[𝓝[≠] x₀]
      (fun x : ℝ => |slope T x₀ x|) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    rw [slope_def_field, hfix, abs_div]
  exact Tendsto.congr' heq.symm hslope

/-- **The great attractor repels.**  At a fixed point with `|L| > 1`, points of
the "known universe" near `x₀` are pushed away from it: eventually
`|T x - x₀| > |x - x₀|`. -/
theorem fixedPoint_repels {T : ℝ → ℝ} {L x₀ : ℝ}
    (hT : HasDerivAt T L x₀) (hfix : T x₀ = x₀) (hL : 1 < |L|) :
    ∀ᶠ x in 𝓝[≠] x₀, |x - x₀| < |T x - x₀| := by
  have h := fixedPoint_distanceRatio hT hfix
  have hgt : ∀ᶠ x in 𝓝[≠] x₀, 1 < |T x - x₀| / |x - x₀| :=
    h.eventually (isOpen_Ioi.mem_nhds hL)
  filter_upwards [hgt, eventually_mem_nhdsWithin] with x hx1 hxne
  have hx0 : 0 < |x - x₀| := abs_pos.mpr (sub_ne_zero.mpr hxne)
  have hstep : 1 * |x - x₀| < (|T x - x₀| / |x - x₀|) * |x - x₀| :=
    mul_lt_mul_of_pos_right hx1 hx0
  rwa [one_mul, div_mul_cancel₀ _ hx0.ne'] at hstep

/-- **The great attractor attracts (it shrinks itself).**  At a fixed point with
`|L| < 1`, nearby points fall toward `x₀`: eventually `|T x - x₀| < |x - x₀|`. -/
theorem fixedPoint_attracts {T : ℝ → ℝ} {L x₀ : ℝ}
    (hT : HasDerivAt T L x₀) (hfix : T x₀ = x₀) (hL : |L| < 1) :
    ∀ᶠ x in 𝓝[≠] x₀, |T x - x₀| < |x - x₀| := by
  have h := fixedPoint_distanceRatio hT hfix
  have hlt : ∀ᶠ x in 𝓝[≠] x₀, |T x - x₀| / |x - x₀| < 1 :=
    h.eventually (isOpen_Iio.mem_nhds hL)
  filter_upwards [hlt, eventually_mem_nhdsWithin] with x hx1 hxne
  have hx0 : 0 < |x - x₀| := abs_pos.mpr (sub_ne_zero.mpr hxne)
  have hstep : (|T x - x₀| / |x - x₀|) * |x - x₀| < 1 * |x - x₀| :=
    mul_lt_mul_of_pos_right hx1 hx0
  rwa [div_mul_cancel₀ _ hx0.ne', one_mul] at hstep

/-- The orientation of the single fixed point is a trichotomy on `|L|`:
attracting (`< 1`), neutral (`= 1`), or repelling (`> 1`). -/
theorem orientation_trichotomy (L : ℝ) :
    |L| < 1 ∨ |L| = 1 ∨ 1 < |L| := by
  rcases lt_trichotomy |L| 1 with h | h | h
  · exact Or.inl h
  · exact Or.inr (Or.inl h)
  · exact Or.inr (Or.inr h)

/-- The **Lyapunov exponent** of the fixed point: the logarithm of the distance
ratio tends to `log |L|`.  This is the exact formal twin of the on-flow
repulsion rate `lambda` measured in `ns_zero_order.py`. -/
theorem fixedPoint_logRate {T : ℝ → ℝ} {L x₀ : ℝ}
    (hT : HasDerivAt T L x₀) (hfix : T x₀ = x₀) (hL : L ≠ 0) :
    Tendsto (fun x : ℝ => Real.log |T x - x₀| - Real.log |x - x₀|)
      (𝓝[≠] x₀) (𝓝 (Real.log |L|)) := by
  have h := fixedPoint_distanceRatio hT hfix
  have hpos : ∀ᶠ x in 𝓝[≠] x₀, 0 < |T x - x₀| / |x - x₀| :=
    h.eventually (isOpen_Ioi.mem_nhds (abs_pos.mpr hL))
  have hlog : Tendsto (fun x : ℝ => Real.log (|T x - x₀| / |x - x₀|))
      (𝓝[≠] x₀) (𝓝 (Real.log |L|)) :=
    (Real.continuousAt_log (abs_ne_zero.mpr hL)).tendsto.comp h
  refine hlog.congr' ?_
  filter_upwards [eventually_mem_nhdsWithin, hpos] with x hxne hxpos
  have hx0 : |x - x₀| ≠ 0 := abs_ne_zero.mpr (sub_ne_zero.mpr hxne)
  have hnum : |T x - x₀| ≠ 0 := by
    intro hz
    rw [hz, zero_div] at hxpos
    exact lt_irrefl 0 hxpos
  rw [Real.log_div hnum hx0]

/-- The Lyapunov exponent carries the orientation: `log |L| > 0` iff the fixed
point repels (`|L| > 1`), and `log |L| < 0` iff it attracts (`|L| < 1`).  So the
sign of the formal exponent is exactly the on-flow orientation. -/
theorem fixedPoint_logSign {L : ℝ} (hL : L ≠ 0) :
    (0 < Real.log |L| ↔ 1 < |L|) ∧ (Real.log |L| < 0 ↔ |L| < 1) := by
  have hx : 0 < |L| := abs_pos.mpr hL
  exact ⟨by rw [← Real.log_one, Real.log_lt_log_iff zero_lt_one hx],
         by rw [← Real.log_one, Real.log_lt_log_iff hx zero_lt_one]⟩

/-! ## Order meets the ladder: the number of zeros shifts the critical rung -/

/-- Critical smoothness for an object of amplitude scaling weight `a` measured
in `L^p`: the exponent that makes the scaled homogeneous norm invariant. -/
def criticalSmoothness (a p : ℝ) : ℝ := 3 / p - a

/-- The scaling weight of the homogeneous norm `Ḣ^s_p` under
`u_λ(x) = λ^a u(λ x)`: `a + s - 3 / p`. -/
def scalingWeight (s a p : ℝ) : ℝ := a + s - 3 / p

/-- The register's critical ladder is the **order-one** rung: with one zero of
amplitude weight (`a = 1`), `criticalSmoothness 1 p = sCrit p`. -/
theorem criticalSmoothness_one (p : ℝ) : criticalSmoothness 1 p = sCrit p := by
  unfold criticalSmoothness sCrit
  ring

/-- Raising the order by one lowers the required critical smoothness by one:
each extra zero buys one order of smoothness. -/
theorem criticalSmoothness_shift_order (a p : ℝ) :
    criticalSmoothness (a + 1) p = criticalSmoothness a p - 1 := by
  unfold criticalSmoothness
  ring

/-- More zeros (higher order) require less smoothness: `criticalSmoothness` is
antitone in the order `a`. -/
theorem criticalSmoothness_antitone_order {a b p : ℝ} (hab : a ≤ b) :
    criticalSmoothness b p ≤ criticalSmoothness a p := by
  unfold criticalSmoothness
  linarith

/-- The homogeneous norm is scale-invariant exactly on the critical rung: the
scaling weight vanishes iff `s = criticalSmoothness a p`. -/
theorem scalingWeight_zero_iff (s a p : ℝ) :
    scalingWeight s a p = 0 ↔ s = criticalSmoothness a p := by
  unfold scalingWeight criticalSmoothness
  constructor <;> intro h <;> linarith

/-- Formalised-facts register for `GreatAttractor.lean`. -/
def greatAttractorFacts : List String :=
  [ "fixedPoint_distanceRatio"
  , "fixedPoint_repels"
  , "fixedPoint_attracts"
  , "orientation_trichotomy"
  , "fixedPoint_logRate"
  , "fixedPoint_logSign"
  , "criticalSmoothness_one"
  , "criticalSmoothness_shift_order"
  , "criticalSmoothness_antitone_order"
  , "scalingWeight_zero_iff" ]

/-- The register has exactly ten entries. -/
theorem greatAttractorFacts_length : greatAttractorFacts.length = 10 := by
  decide
end PunoCalculus.GreatAttractor
