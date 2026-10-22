import Mathlib
import PunoCalculus.EssentialIdentity

/-!
# Uncovering the static: what CH 3's flicker actually is

`PunoCalculus.EssentialIdentity` proves `sin (1/x)` has **no** punctured limit at
`0`.  That result says the picture on channel `sin (1/x)` never locks -- but it
does **not** say what the "static" *is*.  This module uncovers it: the static is
not noise, it is a precise structure.

Two families of **turning points**:

* `xₙ = 1 / (π/2 + 2πn)`, which tends to `0`, and where `sin (1/xₙ) = 1`
  (`turnPos_value`, `turnPos_lt`, `turnPos_pos`).
* `zₙ = 1 / (3π/2 + 2πn)`, which tends to `0`, and where `sin (1/zₙ) = -1`
  (`turnNeg_value`, `turnNeg_lt`, `turnNeg_pos`).

Consequences, all kernel-checked:

* `plus_one_arbitrarily_near` : the value `+1` is attained arbitrarily close to
  `0` (on the right).
* `minus_one_arbitrarily_near` : the value `-1` is attained arbitrarily close to
  `0` (on the right).
* `static_has_both_extremes` : in **every** right-neighbourhood of `0`, both `+1`
  and `-1` occur.  This is the static, uncovered: not randomness, but the two
  extremes recurring at every scale -- which is *why* no limit exists.

The picture "fills up" because the turning points accumulate at `0`: infinitely
many oscillations pile into every interval about `0`.  The static is that
accumulation.  (The stronger statement -- that `sin (1/x)` attains *every* value
in `[-1,1]` in every neighbourhood, by the intermediate value theorem between
consecutive turning points -- is the natural extension and is not needed here.)

Nothing is open; every lemma is elementary and kernel-checked.
-/

noncomputable section

namespace PunoCalculus.StaticUncovered

open Filter Topology
open scoped Topology

/-! ## The turning-point families -/

/-- The positive turning point `xₙ = 1 / (π/2 + 2πn)`. -/
def turnPos (n : ℕ) : ℝ := 1 / (Real.pi / 2 + 2 * Real.pi * n)

/-- The negative turning point `zₙ = 1 / (3π/2 + 2πn)`. -/
def turnNeg (n : ℕ) : ℝ := 1 / (3 * Real.pi / 2 + 2 * Real.pi * n)

/-- **+1 turning points are real turning points.**  `sin (1 / turnPos n) = 1`. -/
theorem turnPos_value (n : ℕ) : Real.sin (1 / turnPos n) = 1 := by
  unfold turnPos
  rw [one_div_one_div, add_comm,
    show 2 * Real.pi * n + Real.pi / 2 = Real.pi / 2 + (n : ℤ) * (2 * Real.pi) by
      push_cast; ring,
    Real.sin_add_int_mul_two_pi, Real.sin_pi_div_two]

/-- **-1 turning points are real turning points.**  `sin (1 / turnNeg n) = -1`. -/
theorem turnNeg_value (n : ℕ) : Real.sin (1 / turnNeg n) = -1 := by
  unfold turnNeg
  rw [one_div_one_div, add_comm,
    show 2 * Real.pi * n + 3 * Real.pi / 2 =
      3 * Real.pi / 2 + (n : ℤ) * (2 * Real.pi) by push_cast; ring,
    Real.sin_add_int_mul_two_pi]
  have h : (3 : ℝ) * Real.pi / 2 = Real.pi / 2 + Real.pi := by ring
  rw [h, Real.sin_add_pi, Real.sin_pi_div_two]

/-- `1/(π/2 + 2πn) < ε` for `ε > 0` and `n` large enough (denominators `→ ∞`). -/
private lemma one_div_denom_lt (k : ℝ) (hk : 0 < k) {ε : ℝ} (hε : 0 < ε) :
    ∃ n : ℕ, (1 : ℝ) / (k + 2 * Real.pi * n) < ε := by
  obtain ⟨n, hn⟩ := exists_nat_gt (1 / ε / (2 * Real.pi))
  refine ⟨n, ?_⟩
  have hp : (0 : ℝ) < Real.pi := Real.pi_pos
  rw [div_lt_iff₀ (by positivity)]
  have hn' : 1 / ε / (2 * Real.pi) < (n : ℝ) := hn
  rw [div_lt_iff₀ (by positivity)] at hn'
  rw [div_lt_iff₀ hε] at hn'
  nlinarith [hn', hp]

/-- Nonnegativity of every turning point. -/
theorem turnPos_pos (n : ℕ) : 0 < turnPos n := by
  unfold turnPos; positivity

/-- Positivity of the negative turning point (it is still a positive `x`). -/
theorem turnNeg_pos (n : ℕ) : 0 < turnNeg n := by
  unfold turnNeg; positivity

/-- **Turning points head to the puncture.**  For every `ε > 0` there is a
positive turning point below `ε`. -/
theorem turnPos_lt {ε : ℝ} (hε : 0 < ε) : ∃ n : ℕ, turnPos n < ε := by
  unfold turnPos
  simpa using one_div_denom_lt (Real.pi / 2) (by positivity) hε

/-- Same for the negative turning points. -/
theorem turnNeg_lt {ε : ℝ} (hε : 0 < ε) : ∃ n : ℕ, turnNeg n < ε := by
  unfold turnNeg
  simpa only [add_comm] using one_div_denom_lt (3 * Real.pi / 2) (by positivity) hε

/-! ## The static, uncovered -/

/-- **`+1` is attained arbitrarily close to `0`** (from the right). -/
theorem plus_one_arbitrarily_near :
    ∀ ε > 0, ∃ x, 0 < x ∧ x < ε ∧ Real.sin (1 / x) = 1 := by
  intro ε hε
  obtain ⟨n, hn⟩ := turnPos_lt hε
  exact ⟨turnPos n, turnPos_pos n, hn, turnPos_value n⟩

/-- **`-1` is attained arbitrarily close to `0`** (from the right). -/
theorem minus_one_arbitrarily_near :
    ∀ ε > 0, ∃ x, 0 < x ∧ x < ε ∧ Real.sin (1 / x) = -1 := by
  intro ε hε
  obtain ⟨n, hn⟩ := turnNeg_lt hε
  exact ⟨turnNeg n, turnNeg_pos n, hn, turnNeg_value n⟩

/-- **The static uncovered.**  In every right-neighbourhood of `0` both extremes
`+1` and `-1` occur.  The flicker is not noise: it is the two extremes recurring
at every scale, which is exactly why no limit exists. -/
theorem static_has_both_extremes :
    ∀ ε > 0, (∃ x, 0 < x ∧ x < ε ∧ Real.sin (1 / x) = 1) ∧
             (∃ x, 0 < x ∧ x < ε ∧ Real.sin (1 / x) = -1) := by
  intro ε hε
  exact ⟨plus_one_arbitrarily_near ε hε, minus_one_arbitrarily_near ε hε⟩

end PunoCalculus.StaticUncovered
