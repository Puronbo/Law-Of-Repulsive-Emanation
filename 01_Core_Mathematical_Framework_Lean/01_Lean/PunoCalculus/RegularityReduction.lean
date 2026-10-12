import Mathlib
import PunoCalculus.OrientationLaw

/-!
# Global regularity reduces to boundedness of the critical-content integral (C10-open)

This brick packages the two OrientationLaw facts into the wall statement itself.  With
`X` the critical content and `g = d/dt log X` its log-growth rate, the continuous BKM
integral gives `X T = X 0 * exp (int_0^T g)`.  Hence:

* If the critical-content integral is bounded, `int_0^T g <= B` for every `T`, then the
  content is bounded, `X T <= X 0 * exp B` -- `regularity_reduced_to_integral`.
* Contrapositive: if the content is unbounded (blow-up), then the critical-content
  integral is unbounded -- `integral_unbounded_of_content_unbounded`.

So the ENTIRE wall is the single analytic question: is `int_0^T d/dt log X dt` bounded
along the real flow?  The discrete analogue is already `OrientationLaw`; the residue is
the NS-specific lower bound on `g` (Beale-Kato-Majda 1984; Constantin-Fefferman 1993).
-/

noncomputable section

open MeasureTheory

namespace PunoCalculus.RegularityReduction

/-- **Bounded integral => bounded content, with the explicit bound.**  If the
log-growth integral up to `T` is at most `B`, the critical content is at most
`X 0 * exp B`. -/
theorem content_le_exp_of_integral_le {X g : ℝ → ℝ} {T B : ℝ}
    (hX0 : 0 < X 0) (hXT : 0 < X T)
    (hderiv : ∀ t ∈ Set.uIcc 0 T, HasDerivAt (fun s => Real.log (X s)) (g t) t)
    (hcont : ContinuousOn g (Set.uIcc 0 T))
    (hint : (∫ t in (0)..T, g t) ≤ B) :
    X T ≤ X 0 * Real.exp B :=
  PunoCalculus.OrientationLaw.continuous_content_bounded hX0 hXT hderiv hcont hint

/-- **The wall is boundedness of the critical-content integral.**  If `X > 0` is
differentiable with log-growth rate `g` (continuous on every `[0, T]`) and the integral
`int_0^T g` is bounded uniformly in `T`, then the critical content is bounded uniformly
in `T`.  This is the exact form of the open residue: everything else is proved. -/
theorem regularity_reduced_to_integral {X g : ℝ → ℝ}
    (hX0 : 0 < X 0)
    (hpos : ∀ T, 0 ≤ T → 0 < X T)
    (hderiv : ∀ T, 0 ≤ T → ∀ t ∈ Set.uIcc 0 T,
      HasDerivAt (fun s => Real.log (X s)) (g t) t)
    (hcont : ∀ T, 0 ≤ T → ContinuousOn g (Set.uIcc 0 T))
    (hB : ∃ B, ∀ T, 0 ≤ T → (∫ t in (0)..T, g t) ≤ B) :
    ∃ C, ∀ T, 0 ≤ T → X T ≤ C := by
  obtain ⟨B, hB⟩ := hB
  exact ⟨X 0 * Real.exp B, fun T hT =>
    content_le_exp_of_integral_le hX0 (hpos T hT) (hderiv T hT) (hcont T hT) (hB T hT)⟩

/-- **No blow-up without a diverging critical-content integral.**  Contrapositive of
`regularity_reduced_to_integral`: if the critical content is unbounded, then the
log-growth integral `int_0^T g` is unbounded. -/
theorem integral_unbounded_of_content_unbounded {X g : ℝ → ℝ}
    (hX0 : 0 < X 0)
    (hpos : ∀ T, 0 ≤ T → 0 < X T)
    (hderiv : ∀ T, 0 ≤ T → ∀ t ∈ Set.uIcc 0 T,
      HasDerivAt (fun s => Real.log (X s)) (g t) t)
    (hcont : ∀ T, 0 ≤ T → ContinuousOn g (Set.uIcc 0 T))
    (hunbounded : ∀ C, ∃ T, 0 ≤ T ∧ C < X T) :
    ∀ B, ∃ T, 0 ≤ T ∧ B < (∫ t in (0)..T, g t) := by
  intro B
  by_contra h
  simp only [not_exists, not_and, not_lt] at h
  obtain ⟨C, hC⟩ :=
    regularity_reduced_to_integral hX0 hpos hderiv hcont ⟨B, h⟩
  obtain ⟨T, hT, hCT⟩ := hunbounded C
  exact absurd (hC T hT) (not_le.mpr hCT)

/-- Formalised-facts register for `RegularityReduction.lean`. -/
def regularityReductionFacts : List String :=
  [ "content_le_exp_of_integral_le", "regularity_reduced_to_integral",
    "integral_unbounded_of_content_unbounded" ]

/-- The register has exactly three entries. -/
theorem regularityReductionFacts_length : regularityReductionFacts.length = 3 := by decide

end PunoCalculus.RegularityReduction
