import Mathlib
import PunoCalculus.ContinuationCriterion
import PunoCalculus.EnstrophyBarrier

/-!
# The sufficiency loop: 2D closes, 3D does not

This brick plugs the three register pieces together.

* `PunoCalculus.EnstrophyBarrier.mono_step_bounded`: a non-increasing invariant is
  bounded by its start (the 2D enstrophy shape).
* `PunoCalculus.ContinuationCriterion.exists_upto_of_bounded`: a bounded invariant
  plus an extendable local-existence step gives global existence.

Composed, they say: **in the 2D shape the loop closes** -- non-increasing enstrophy
is bounded for free, and boundedness propagates to existence at every time.  In the
3D shape the same loop *cannot be switched on*: the quadratic increment admits no
uniform bound (`EnstrophyBarrier.quadratic_step_unbounded`), so the hypothesis the
continuation criterion needs holds for no `M`.  That is the wall restated as a
statement about which shape of increment the sufficiency engine accepts.
-/

namespace PunoCalculus.SufficiencyLoop

/-- **The 2D sufficiency loop closes.**  If the invariant `N` is non-increasing
(the 2D enstrophy shape) and the local-existence step is available while `N ≤ N 0`,
then existence holds at every time.  This is `mono_step_bounded` feeding
`exists_upto_of_bounded` with the free bound `M = N 0`. -/
theorem global_exists_of_mono
    {exists_upto : ℕ → Prop} {N : ℕ → ℝ} (hy : ∀ n, N (n + 1) ≤ N n)
    (hstep : ∀ t, (∀ s ≤ t, N s ≤ N 0) → exists_upto t → exists_upto (t + 1))
    (h0 : exists_upto 0) : ∀ T, exists_upto T := by
  intro T
  exact ContinuationCriterion.exists_upto_of_bounded
    (M := N 0) (fun t _ hb ht => hstep t hb ht) h0
    (fun s _ => EnstrophyBarrier.mono_step_bounded N hy s)

/-- **The 3D shape disables the loop.**  A per-step increment bounded by
`C * (value)^2` (`C > 0`) admits an invariant that escapes EVERY bound: for every
`M` some iterate exceeds it.  So the hypothesis `∀ s ≤ T, N s ≤ M` the continuation
criterion needs is satisfiable for no `M` -- the sufficiency engine cannot be
started from a quadratic increment. -/
theorem quadratic_criterion_unavailable (C A : ℝ) (hC : 0 < C) (hA : 0 < A)
    (hCA : 1 ≤ C * A) :
    ∃ y : ℕ → ℝ,
      (∀ n, y (n + 1) ≤ y n + C * (y n) ^ 2) ∧ (∀ M : ℝ, ∃ s, M < y s) := by
  obtain ⟨y, hy, hunb⟩ := EnstrophyBarrier.quadratic_step_unbounded C A hC hA hCA
  exact ⟨y, hy, hunb⟩

/-- Formalised-facts register for `SufficiencyLoop.lean`. -/
def sufficiencyLoopFacts : List String :=
  [ "global_exists_of_mono", "quadratic_criterion_unavailable" ]

/-- The register has exactly two entries. -/
theorem sufficiencyLoopFacts_length : sufficiencyLoopFacts.length = 2 := by decide

end PunoCalculus.SufficiencyLoop
