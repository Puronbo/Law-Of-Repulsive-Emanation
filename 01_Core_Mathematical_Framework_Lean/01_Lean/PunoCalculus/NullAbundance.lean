import Mathlib

/-!
# Null abundance: "nothing" as the countable substrate

A small, self-contained measure-theory module recording the precise sense in which
"nothing" is the most abundant thing: **infinite count does not buy positive
measure**.  A single point is null; any countable set is null; the rationals are
countable *and* dense, so they are everywhere and yet measure nothing; the even
naturals, though they pile up without end, are null.

The asymmetry is the honest content: uncountable sets need not be null (`[0,1]`
has measure `1`).  So "abundance" and "substance" are *different roles* -- one is
count (cardinality / density), the other is magnitude (measure).  What is proved
here is the measure statement; the claim that the *pile-up* of infinitesimals
"equals nothing" is the indeterminate form `0/0` and is **not** asserted.

Nothing here is open -- it is elementary measure theory, kernel-checked.
-/

namespace PunoCalculus.NullAbundance

open MeasureTheory

/-- One point is nothing: a singleton has measure zero. -/
theorem singleton_null (x : ℝ) : volume ({x} : Set ℝ) = 0 := measure_singleton x

/-- Infinitely many nothings are still nothing: any countable set is null. -/
theorem countable_null (s : Set ℝ) (h : s.Countable) : volume s = 0 :=
  h.measure_zero volume

/-- The rationals, embedded in `ℝ`, are countable. -/
theorem rationals_countable : (Set.range ((↑) : ℚ → ℝ)).Countable :=
  Set.countable_range _

/-- The rationals are **dense** in `ℝ`: every real is a limit of rationals. -/
theorem rationals_dense : Dense (Set.range ((↑) : ℚ → ℝ)) := Rat.denseRange_cast

/-- **Null abundance.**  The rationals are dense (everywhere) yet null (nowhere):
presence without magnitude. -/
theorem rationals_null_and_dense :
    volume (Set.range ((↑) : ℚ → ℝ)) = 0 ∧ Dense (Set.range ((↑) : ℚ → ℝ)) :=
  ⟨(Set.countable_range _).measure_zero volume, Rat.denseRange_cast⟩

/-- The even naturals, viewed in `ℝ`, are countable. -/
theorem evens_countable :
    (Set.range (fun n : ℕ => ((2 * n : ℕ) : ℝ))).Countable :=
  Set.countable_range _

/-- The evens pile up without end, and the pile still measures nothing. -/
theorem evens_pile_is_null :
    volume (Set.range (fun n : ℕ => ((2 * n : ℕ) : ℝ))) = 0 :=
  (Set.countable_range _).measure_zero volume

/-- The asymmetry that keeps the claim honest: uncountable sets need not be null. -/
theorem unit_interval_not_null : volume (Set.Icc (0 : ℝ) 1) = 1 := by simp

end PunoCalculus.NullAbundance
