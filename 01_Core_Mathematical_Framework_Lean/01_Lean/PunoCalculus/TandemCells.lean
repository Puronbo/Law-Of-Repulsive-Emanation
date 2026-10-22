import Mathlib

/-!
# Tandem cells: monotone but diminishing returns

Adding junctions to a multijunction solar cell raises the detailed-balance ceiling
but with **diminishing returns**.  This module records the provable structure with
the standard geometric model `C(n) = L - L·rⁿ` for `0 ≤ r ≤ 1`, `L ≥ 0`, where
`L` is the asymptotic ceiling and `r` the fraction of the remaining loss each new
junction fails to capture:

- **Monotone:** the ceiling never decreases as junctions are added.
- **Bounded:** it never exceeds the limit `L` (no mixture creates work).
- **Diminishing increments:** `C(n+2) − C(n+1) ≤ C(n+1) − C(n)` -- the gain per
  added junction shrinks geometrically, which is why a 4th or 5th junction buys
  little: the sub-bandgap and thermalization losses are already squeezed out.

Everything here is elementary real analysis, kernel-checked; nothing is open.
-/

namespace PunoCalculus.TandemCells

/-- The `n`-junction ceiling with asymptotic limit `L` and per-junction gap
fraction `r` (the fraction of the remaining loss not captured). -/
noncomputable def ceiling (L r : ℝ) (n : ℕ) : ℝ := L - L * r ^ n

/-- **More junctions never hurt.**  The ceiling is monotone in the junction count. -/
theorem ceiling_monotone {L r : ℝ} (hL : 0 ≤ L) (hr0 : 0 ≤ r) (hr1 : r ≤ 1) :
    Monotone (ceiling L r) := by
  intro m n hmn
  unfold ceiling
  have : r ^ n ≤ r ^ m := pow_le_pow_of_le_one hr0 hr1 hmn
  nlinarith

/-- **No free lunch.**  The ceiling never exceeds the asymptotic limit `L`. -/
theorem ceiling_le_limit {L r : ℝ} (hL : 0 ≤ L) (hr0 : 0 ≤ r) (n : ℕ) :
    ceiling L r n ≤ L := by
  unfold ceiling
  have : 0 ≤ L * r ^ n := mul_nonneg hL (pow_nonneg hr0 n)
  linarith

/-- The gain from one added junction is `L·rⁿ·(1-r)`. -/
theorem ceiling_increment (L r : ℝ) (n : ℕ) :
    ceiling L r (n + 1) - ceiling L r n = L * r ^ n * (1 - r) := by
  unfold ceiling
  rw [pow_succ]; ring

/-- **Diminishing returns.**  The increment from the `(n+1)`-th junction is at most
the increment from the `n`-th: each added junction buys less than the last. -/
theorem ceiling_increments_shrink {L r : ℝ} (hL : 0 ≤ L) (hr0 : 0 ≤ r) (hr1 : r ≤ 1)
    (n : ℕ) :
    ceiling L r (n + 2) - ceiling L r (n + 1) ≤ ceiling L r (n + 1) - ceiling L r n := by
  rw [ceiling_increment, ceiling_increment]
  have h1rn : 0 ≤ r ^ n := pow_nonneg hr0 n
  have hfac : 0 ≤ 1 - r := by linarith
  have hbase : 0 ≤ L * (1 - r) := mul_nonneg hL hfac
  have hstep : r ^ (n + 1) ≤ r ^ n := pow_le_pow_of_le_one hr0 hr1 (Nat.le_succ n)
  calc L * r ^ (n + 1) * (1 - r)
      = (L * (1 - r)) * r ^ (n + 1) := by ring
    _ ≤ (L * (1 - r)) * r ^ n := mul_le_mul_of_nonneg_left hstep hbase
    _ = L * r ^ n * (1 - r) := by ring

end PunoCalculus.TandemCells
