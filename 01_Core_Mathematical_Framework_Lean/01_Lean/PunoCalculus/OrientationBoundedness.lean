import Mathlib
import PunoCalculus.GreatAttractor

/-!
# Orientation decides boundedness: the two organizing numbers meet

The register has two organizing numbers: the ORDER of the invariant's increment
(`EnstrophyBarrier`, `QuantitativeContinuation`) and the ORIENTATION -- the sign of
the Lyapunov exponent `log |L|` at the fixed point (`GreatAttractor.fixedPoint_logSign`).
This brick joins them.

For the geometric model `N n = r ^ n * A` (the exact orbit of a fixed point with
multiplier `r`), boundedness is decided *entirely* by the orientation:

* `r <= 1` (attracting or marginal): `N` is bounded by its start (`geometric_bounded_of_le_one`);
* `r > 1` (repelling): `N` escapes every bound (`geometric_unbounded_of_one_lt`).

So `∃ B, ∀ n, N n ≤ B  ↔  r <= 1` (`geometric_bounded_iff`), and -- the bridge to
`GreatAttractor` -- the sign of `log r` reads the wall: `0 < log r` iff unbounded,
`log r <= 0` iff bounded (`orientation_decides_boundedness`).  With `r = |L|` this is
exactly the orientation `Repelling`/`Attracting` (`repelling_iff_unbounded`): the
multiplier sign is the direction, and the direction is whether the invariant is
bounded.  That is the on-flow wall (`orientation_vs_invariant.py`) as a theorem.
-/

namespace PunoCalculus.OrientationBoundedness

open Filter
open scoped Topology

/-- **Attracting / marginal ⇒ bounded.**  A geometric orbit with `0 ≤ r ≤ 1` stays
below its start (for `0 ≤ A`). -/
theorem geometric_bounded_of_le_one {r A : ℝ} (hr : 0 ≤ r) (hr1 : r ≤ 1) (hA : 0 ≤ A) :
    ∀ n, r ^ n * A ≤ A := by
  intro n
  calc r ^ n * A ≤ 1 * A := mul_le_mul_of_nonneg_right (pow_le_one₀ hr hr1) hA
    _ = A := one_mul A

/-- **Repelling ⇒ unbounded.**  A geometric orbit with `r > 1` (and `A > 0`) escapes
every bound. -/
theorem geometric_unbounded_of_one_lt {r A : ℝ} (hr : 1 < r) (hA : 0 < A) :
    ∀ M : ℝ, ∃ n, M < r ^ n * A := by
  intro M
  have hpow : Tendsto (fun n : ℕ => r ^ n) atTop atTop :=
    tendsto_pow_atTop_atTop_of_one_lt hr
  have hcm : Tendsto (fun n : ℕ => r ^ n * A) atTop atTop := by
    simpa only [mul_comm] using hpow.const_mul_atTop hA
  exact (hcm.eventually (eventually_gt_atTop M)).exists

/-- **The geometric dichotomy.**  For a nondegenerate orbit (`r > 0`, `A > 0`):
bounded iff `r <= 1`. -/
theorem geometric_bounded_iff {r A : ℝ} (hr : 0 < r) (hA : 0 < A) :
    (∃ B : ℝ, ∀ n, r ^ n * A ≤ B) ↔ r ≤ 1 := by
  constructor
  · intro ⟨B, hB⟩
    rcases le_or_gt r 1 with hr1 | hr1
    · exact hr1
    · obtain ⟨n, hn⟩ := geometric_unbounded_of_one_lt hr1 hA B
      exact absurd (hB n) (not_le.mpr hn)
  · intro hr1
    exact ⟨A, geometric_bounded_of_le_one (le_of_lt hr) hr1 (le_of_lt hA)⟩

/-- **The orientation decides boundedness.**  The sign of `log r` reads the wall:
positive (`1 < r`, repelling) iff the invariant is unbounded; nonpositive
(`r ≤ 1`, attracting/marginal) iff it is bounded.  The formal twin of
`GreatAttractor.fixedPoint_logSign` and of the on-flow
`orientation_vs_invariant.py` bridge. -/
theorem orientation_decides_boundedness {r A : ℝ} (hr : 0 < r) (hA : 0 < A) :
    (0 < Real.log r ↔ ¬ ∃ B : ℝ, ∀ n, r ^ n * A ≤ B) ∧
    (Real.log r ≤ 0 ↔ ∃ B : ℝ, ∀ n, r ^ n * A ≤ B) := by
  have hiff : (∃ B : ℝ, ∀ n, r ^ n * A ≤ B) ↔ r ≤ 1 := geometric_bounded_iff hr hA
  have hle : Real.log r ≤ 0 ↔ r ≤ 1 := by
    rw [← Real.log_one, Real.log_le_log_iff hr zero_lt_one]
  exact ⟨by rw [Real.log_pos_iff (le_of_lt hr), ← not_le, ← hiff],
         by rw [hle, ← hiff]⟩

/-- **Repelling iff unbounded (the orientation bridge).**  With `r = |L|` this is the
`GreatAttractor` orientation: a repelling fixed point (`1 < |L|`) has an unbounded
geometric invariant, an attracting one (`|L| < 1`) a bounded invariant. -/
theorem repelling_iff_unbounded {L A : ℝ} (hL : L ≠ 0) (hA : 0 < A) :
    (0 < Real.log |L| ↔ ¬ ∃ B : ℝ, ∀ n, |L| ^ n * A ≤ B) ∧
    (Real.log |L| ≤ 0 ↔ ∃ B : ℝ, ∀ n, |L| ^ n * A ≤ B) :=
  orientation_decides_boundedness (abs_pos.mpr hL) hA

/-- Formalised-facts register for `OrientationBoundedness.lean`. -/
def orientationBoundednessFacts : List String :=
  [ "geometric_bounded_of_le_one", "geometric_unbounded_of_one_lt",
    "geometric_bounded_iff", "orientation_decides_boundedness", "repelling_iff_unbounded" ]

/-- The register has exactly five entries. -/
theorem orientationBoundednessFacts_length : orientationBoundednessFacts.length = 5 := by
  decide

end PunoCalculus.OrientationBoundedness
