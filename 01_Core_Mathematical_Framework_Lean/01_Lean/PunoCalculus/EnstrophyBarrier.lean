import Mathlib

/-!
# The enstrophy barrier: linear (2D) is bounded, quadratic (3D) is blow-up-capable

The register's wall is BOUNDEDNESS of the scaling-critical invariant.  The one
structural difference between the 2D and 3D enstrophy budgets is the *order of the
right-hand side*:

* 2D (`Z_t <= 0`, enstrophy non-increasing): the increment is *linear* with slope
  `<= 0`, so the quantity is bounded by its start -- boundedness for free;
* 3D (`dZ/dt <= C Z^2`): the increment is quadratic, and this inequality admits
  UNBOUNDED solutions -- boundedness is no longer implied.

This file makes the contrast a theorem.  `mono_step_bounded` is the 2D shape
(a non-increasing sequence is bounded by its initial value).  `quadratic_step_unbounded`
exhibits an explicit sequence (`A * 2^n`) with quadratic per-step increment that is
unbounded -- so the 3D shape carries no free bound.  The two together are the
arithmetic reason the extra order in 3D is exactly the difference between a
Lyapunov bound and a possible finite-time blow-up.
-/

namespace PunoCalculus.EnstrophyBarrier

open Filter
open scoped Topology

/-- **2D shape: a non-increasing sequence is bounded by its start.**  The arithmetic
core of the enstrophy Lyapunov control `dZ/dt ≤ 0` available in two dimensions. -/
theorem mono_step_bounded (y : ℕ → ℝ) (hy : ∀ n, y (n + 1) ≤ y n) :
    ∀ n, y n ≤ y 0 := by
  intro n
  induction n with
  | zero => exact le_refl _
  | succ k ih => exact le_trans (hy k) ih

/-- The explicit doubling schedule `y n = A * 2^n`: it doubles every step. -/
def doubling (A : ℝ) (n : ℕ) : ℝ := A * 2 ^ n

theorem doubling_succ (A : ℝ) (n : ℕ) : doubling A (n + 1) = 2 * doubling A n := by
  simp only [doubling, pow_succ]
  ring

/-- **3D shape: the quadratic increment admits unbounded solutions.**  Whenever the
per-step increment is bounded by `C * (value)^2` (`C > 0`), it does NOT force a bound:
the explicit schedule `y n = A * 2^n` (with `A > 0`, `C * A ≥ 1`) satisfies the
inequality and is unbounded.  Contrast with `mono_step_bounded`. -/
theorem quadratic_step_unbounded (C A : ℝ) (hC : 0 < C) (hA : 0 < A) (hCA : 1 ≤ C * A) :
    ∃ y : ℕ → ℝ,
      (∀ n, y (n + 1) ≤ y n + C * (y n) ^ 2) ∧
      (∀ K : ℝ, ∃ n, K < y n) := by
  refine ⟨doubling A, ?_, ?_⟩
  · intro n
    rw [doubling_succ]
    have hpos : 0 < doubling A n := by
      unfold doubling; positivity
    have h2n : (1 : ℝ) ≤ 2 ^ n := one_le_pow₀ (by norm_num)
    have hA_le : A ≤ doubling A n := by
      unfold doubling
      calc A = A * 1 := (mul_one A).symm
        _ ≤ A * 2 ^ n := mul_le_mul_of_nonneg_left h2n (le_of_lt hA)
    have hyC : 1 ≤ C * doubling A n :=
      calc (1 : ℝ) ≤ C * A := hCA
        _ ≤ C * doubling A n := mul_le_mul_of_nonneg_left hA_le (le_of_lt hC)
    have hquad : doubling A n ≤ C * (doubling A n) ^ 2 := by
      calc doubling A n = doubling A n * 1 := (mul_one _).symm
        _ ≤ doubling A n * (C * doubling A n) :=
              mul_le_mul_of_nonneg_left hyC (le_of_lt hpos)
        _ = C * (doubling A n) ^ 2 := by ring
    linarith
  · intro K
    have hT : Tendsto (fun n : ℕ => (2 : ℝ) ^ n) atTop atTop :=
      tendsto_pow_atTop_atTop_of_one_lt (by norm_num)
    have hT' : Tendsto (fun n : ℕ => doubling A n) atTop atTop := by
      simpa only [doubling] using hT.const_mul_atTop hA
    exact (hT'.eventually (eventually_gt_atTop K)).exists

/-- **The contrast.**  A non-increasing quantity is uniformly bounded (2D enstrophy
shape); a quadratically-incrementing quantity is not (3D enstrophy shape). -/
theorem quadratic_no_uniform_bound (C A : ℝ) (hC : 0 < C) (hA : 0 < A) (hCA : 1 ≤ C * A) :
    (∃ y : ℕ → ℝ,
        (∀ n, y (n + 1) ≤ y n + C * (y n) ^ 2) ∧
        ¬ (∃ B : ℝ, ∀ n, y n ≤ B)) := by
  obtain ⟨y, hy, hunb⟩ := quadratic_step_unbounded C A hC hA hCA
  exact ⟨y, hy, fun ⟨B, hB⟩ => by
    obtain ⟨n, hn⟩ := hunb B
    exact not_lt_of_ge (hB n) hn⟩

/-- Formalised-facts register for `EnstrophyBarrier.lean`. -/
def enstrophyBarrierFacts : List String :=
  [ "mono_step_bounded", "doubling_succ", "quadratic_step_unbounded",
    "quadratic_no_uniform_bound" ]

/-- The register has exactly four entries. -/
theorem enstrophyBarrierFacts_length : enstrophyBarrierFacts.length = 4 := by decide

end PunoCalculus.EnstrophyBarrier
