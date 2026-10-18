import Mathlib
import PunoCalculus.OrientationLaw

/-!
# Dissipative flows are attracting: the energy face of the orientation law (C8)

Card **C8** identifies the orientation `lambda` with the growth rate `mu` of the
critical content.  For a *dissipative* flow -- one whose content has non-positive time
derivative, the prototypical case being the Navier-Stokes energy identity
`dE/dt = -nu ||grad u||^2 <= 0` -- the growth rate of `log(content)` is non-positive.
Combined with `OrientationLaw.continuous_content_bounded`, a flow whose log-growth rate
`g` is `<= 0` on `[0, T]` satisfies `X T <= X 0`: dissipation never lets the content
grow.  This is the *attracting* side of the on-flow probe (`orientation_vs_invariant.py`,
3D/2D Navier-Stokes, `lambda < 0` and `mu < 0`) as a theorem.

Honesty: this is the energy (L^2-type) face.  For the scaling-critical content
`||u||_{B^{-1}_{inf,inf}}` there is no such energy identity, so `g` need not be
non-positive; proving `int_0^T g < inf` for the critical content is exactly the open
wall (card C8-open).  This brick closes the dissipative half, not the wall.
-/

noncomputable section

open MeasureTheory

namespace PunoCalculus.DissipativeFlow

/-- **Log-growth is the relative rate of change.**  If the content `X` has time
derivative `m` at `t` and `X t != 0`, then `log (X .)` has derivative `m / X t`. -/
theorem logGrowth_deriv {X : ℝ → ℝ} {m t : ℝ} (hX : X t ≠ 0) (hderiv : HasDerivAt X m t) :
    HasDerivAt (fun s => Real.log (X s)) (m / X t) t := by
  simpa [div_eq_inv_mul] using hderiv.log hX

/-- **Dissipative flow => non-positive log-growth.**  If the content is positive at `t`
and its time derivative is non-positive (dissipation dominates), the log-growth rate is
non-positive. -/
theorem logGrowth_nonpos_of_dissipative {X : ℝ → ℝ} {m t : ℝ}
    (hX : 0 < X t) (hderiv : HasDerivAt X m t) (hm : m ≤ 0) :
    deriv (fun s => Real.log (X s)) t ≤ 0 := by
  rw [(logGrowth_deriv (ne_of_gt hX) hderiv).deriv]
  exact div_nonpos_of_nonpos_of_nonneg hm (le_of_lt hX)

/-- **A dissipative flow never lets its content grow.**  If on `[0, T]` the log-content
has continuous growth rate `g <= 0`, then `X T <= X 0`.  The Navier-Stokes energy
estimate (`g = d/dt log ||u||_{L^2} <= 0`) is the motivating case. -/
theorem content_le_initial_of_dissipative {X g : ℝ → ℝ} {T : ℝ}
    (h0 : 0 ≤ T) (hX0 : 0 < X 0) (hXT : 0 < X T)
    (hderiv : ∀ t ∈ Set.uIcc 0 T, HasDerivAt (fun s => Real.log (X s)) (g t) t)
    (hcont : ContinuousOn g (Set.uIcc 0 T))
    (hnonpos : ∀ t ∈ Set.uIcc 0 T, g t ≤ 0) :
    X T ≤ X 0 := by
  have hIntg : IntervalIntegrable g volume 0 T := hcont.intervalIntegrable
  have hInt0 : IntervalIntegrable (fun _ : ℝ => (0 : ℝ)) volume 0 T := intervalIntegrable_const
  have hle : (∫ t in (0)..T, g t) ≤ ∫ t in (0)..T, (0 : ℝ) :=
    intervalIntegral.integral_mono_on h0 hIntg hInt0
      (fun t ht => hnonpos t (by rw [Set.uIcc_of_le h0]; exact ht))
  have hb := PunoCalculus.OrientationLaw.continuous_content_bounded
    (B := 0) hX0 hXT hderiv hcont (by simpa using hle)
  simpa using hb

/-- Formalised-facts register for `DissipativeFlow.lean`. -/
def dissipativeFlowFacts : List String :=
  [ "logGrowth_deriv", "logGrowth_nonpos_of_dissipative", "content_le_initial_of_dissipative" ]

/-- The register has exactly three entries. -/
theorem dissipativeFlowFacts_length : dissipativeFlowFacts.length = 3 := by decide

end PunoCalculus.DissipativeFlow
