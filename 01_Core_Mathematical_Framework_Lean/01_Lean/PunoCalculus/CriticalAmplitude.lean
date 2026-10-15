import Mathlib

/-!
# The critical phenomenon: the amplitude is the removable value of a 0/0

The register's atlas names five 0/0 mechanisms.  Four are now machine-checked:
Probe (`ZeroProbe`, C19), Vanishing Rate (`ZeroValuation`, C18/C20), Index
(`ZeroIndex`, C21) and Conservation (cards C36/C37).  This file gives the fifth --
the **Critical Phenomenon** -- a formal core: at a phase transition two quantities
vanish together as powers of the reduced control parameter and their ratio is a
`0/0` whose removable value is a **critical amplitude**.

`orderParameter A β x = A * |x| ^ β` vanishes at the critical point `x = 0` for any
`β ≠ 0` (`orderParameter_at_critical`), and the probe ratio `amplitudeRatio A β x =
orderParameter A β x / |x| ^ β` -- a genuine `0/0`, numerator and denominator both
vanishing at `x = 0` -- has the exact removable value `A` off the critical point
(`amplitudeRatio_eq`).

The file also records the **critical scaling relations** as identities of the
exponent set forced by the Widom scaling form.  Reading the order parameter and the
isotherm as `m ~ t^β`, `h ~ m^δ`, the remaining exponents are determined,
`γ = β(δ-1)` (`gamma`) and `α = 2 - β(δ+1)` (`alpha`), and the classical scaling
relations hold identically: Widom `γ = β(δ-1)` (`widom_relation`), Rushbrooke
`α + 2β + γ = 2` (`rushbrooke_relation`), Josephson hyperscaling `ν d = 2 - α`
(`josephson_relation`) and Fisher `ν(2-η) = γ` (`fisher_relation`).

Scope, as everywhere: a statement about real powers and real algebra.  No
statistical-mechanics model is instantiated, no phase transition is proved
critical, and no Millennium problem is touched (see `WHAT_THIS_DOES_NOT_PROVE.md`).
The classical referent is Widom, *Equation of State near the Critical Point* (1965)
with the scaling-relation literature (Rushbrooke 1963, Fisher 1964, Josephson
1966); here it is the finite algebraic shadow.
-/

noncomputable section

namespace PunoCalculus.CriticalAmplitude

/-- The order parameter near a critical point: `m(x) = A * |x|^β`, with `A` the
critical amplitude and `β` the order-parameter exponent. -/
def orderParameter (A β x : ℝ) : ℝ := A * |x| ^ β

/-- The probe ratio `m(x) / |x|^β`: a `0/0` at the critical point, where numerator
and denominator both vanish. -/
def amplitudeRatio (A β x : ℝ) : ℝ := orderParameter A β x / |x| ^ β

/-- `|x|^β` is nonzero off the critical point, for every exponent `β`. -/
theorem abs_rpow_ne_zero (x β : ℝ) (hx : x ≠ 0) : |x| ^ β ≠ 0 := by
  rcases eq_or_ne β 0 with hβ | hβ
  · subst hβ
    rw [Real.rpow_zero]
    exact one_ne_zero
  · exact (Real.rpow_ne_zero (abs_nonneg x) hβ).mpr (abs_ne_zero.mpr hx)

/-- **The critical amplitude is the removable value of the 0/0.** Off the critical
point the probe ratio is exactly the amplitude `A`. -/
theorem amplitudeRatio_eq (A β x : ℝ) (hx : x ≠ 0) :
    amplitudeRatio A β x = A := by
  unfold amplitudeRatio orderParameter
  exact mul_div_cancel_right₀ A (abs_rpow_ne_zero x β hx)

/-- The order parameter genuinely vanishes at the critical point (for `β ≠ 0`). -/
theorem orderParameter_at_critical (A β : ℝ) (hβ : β ≠ 0) :
    orderParameter A β 0 = 0 := by
  unfold orderParameter
  rw [abs_zero, Real.zero_rpow hβ, mul_zero]

/-- Susceptibility exponent `γ = β(δ-1)` (Widom). -/
def gamma (β δ : ℝ) : ℝ := β * (δ - 1)

/-- Specific-heat exponent `α = 2 - β(δ+1)`, forced by the scaling relations. -/
def alpha (β δ : ℝ) : ℝ := 2 - β * (δ + 1)

/-- Correlation-length exponent `ν = (2-α)/d` (hyperscaling). -/
def nu (d β δ : ℝ) : ℝ := (2 - alpha β δ) / d

/-- Anomalous-dimension exponent `η = 2 - γ/ν`. -/
def eta (d β δ : ℝ) : ℝ := 2 - gamma β δ / nu d β δ

/-- **Widom relation** `γ = β(δ-1)`. -/
theorem widom_relation (β δ : ℝ) : gamma β δ = β * (δ - 1) := rfl

/-- **Rushbrooke relation** `α + 2β + γ = 2`. -/
theorem rushbrooke_relation (β δ : ℝ) :
    alpha β δ + 2 * β + gamma β δ = 2 := by
  unfold alpha gamma
  ring

/-- **Josephson hyperscaling** `ν d = 2 - α`. -/
theorem josephson_relation (d β δ : ℝ) (hd : d ≠ 0) :
    nu d β δ * d = 2 - alpha β δ := by
  unfold nu
  field_simp

/-- **Fisher relation** `ν(2-η) = γ`. -/
theorem fisher_relation (d β δ : ℝ) (h : nu d β δ ≠ 0) :
    nu d β δ * (2 - eta d β δ) = gamma β δ := by
  unfold eta
  field_simp
  ring

/-- Formalised-facts register for `CriticalAmplitude.lean`. -/
def criticalAmplitudeFacts : List String :=
  [ "orderParameter", "amplitudeRatio", "amplitudeRatio_eq",
    "orderParameter_at_critical", "gamma", "alpha", "nu", "eta",
    "widom_relation", "rushbrooke_relation", "josephson_relation",
    "fisher_relation" ]

/-- The register has exactly twelve entries. -/
theorem criticalAmplitudeFacts_length : criticalAmplitudeFacts.length = 12 := by
  decide

end PunoCalculus.CriticalAmplitude
