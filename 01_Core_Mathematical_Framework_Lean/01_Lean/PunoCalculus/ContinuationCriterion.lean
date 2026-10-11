import Mathlib

/-!
# The continuation criterion: the logical shape of the wall

The open wall (`PunoCalculus.OnsagerCriterion`, `PunoCalculus.GreatAttractor`) is
BOUNDEDNESS of the scaling-critical invariant along the flow.  This file isolates
the *logical skeleton* every continuation criterion shares, independent of which
norm plays the role of the invariant.

Abstractly: a local existence theory is *extendable* while the invariant `N` stays
bounded.  So existence can only fail at a time `T` if `N` has escaped every bound
on `[0, T)`.  That contrapositive — **blowup <=> the invariant is unbounded** — is
the wall in its purest form: sufficiency (bounded => regular) is classical and is
what `OnsagerCriterion.weighted_sum_le` supplies a piece of; the missing brick is
the boundedness that this file shows is *exactly* what a blowup would require to
fail.

We formalise a discrete-time model: `exists_upto : ℕ → Prop` is "the solution
exists through step `t`", `N : ℕ → ℝ` is the invariant, and one continuation step
is available whenever `N` is bounded by `M`.  The result is non-vacuous and fully
kernel-checked; the analytic content it abstracts is the local existence theory.
-/

namespace PunoCalculus.ContinuationCriterion

/-- **Continuation sufficiency (discrete skeleton).**  If one can always advance
the solution by a step while the invariant `N` stays `<= M`, and the solution
starts at `0`, then it reaches every `t <= T` as long as `N <= M` on `[0, T]`.
So a bounded invariant rules out failure at `T`. -/
theorem exists_upto_of_bounded {exists_upto : ℕ → Prop} {N : ℕ → ℝ} {M : ℝ} {T : ℕ}
    (hstep : ∀ t < T, (∀ s ≤ t, N s ≤ M) → exists_upto t → exists_upto (t + 1))
    (h0 : exists_upto 0)
    (hbound : ∀ s ≤ T, N s ≤ M) :
    exists_upto T := by
  have h_all : ∀ t ≤ T, exists_upto t := by
    intro t
    induction t with
    | zero => intro _; exact h0
    | succ n ih =>
        intro hnT
        have hn : n ≤ T := Nat.le_of_succ_le hnT
        have hlt : n < T := Nat.lt_of_succ_le hnT
        exact hstep n hlt (fun s hs => hbound s (le_trans hs hn)) (ih hn)
  exact h_all T le_rfl

/-- **The wall (contrapositive).**  If the solution exists at `0` but FAILS at `T`
(`¬ exists_upto T`), then — no matter the bound `M` one proposes — the invariant
must exceed it somewhere in `[0, T]`.  Equivalently: a first failure of existence
forces the scaling-critical invariant to be unbounded.  This is the exact logical
face of the open wall: boundedness is not a technical convenience but the single
thing that stands between local existence and global regularity. -/
theorem unbounded_of_first_failure {exists_upto : ℕ → Prop} {N : ℕ → ℝ} {M : ℝ} {T : ℕ}
    (hstep : ∀ t < T, (∀ s ≤ t, N s ≤ M) → exists_upto t → exists_upto (t + 1))
    (h0 : exists_upto 0) (hfail : ¬ exists_upto T) :
    ¬ (∀ s ≤ T, N s ≤ M) :=
  fun hb => hfail (exists_upto_of_bounded hstep h0 hb)

/-- Formalised-facts register for `ContinuationCriterion.lean`. -/
def continuationFacts : List String :=
  [ "exists_upto_of_bounded", "unbounded_of_first_failure" ]

/-- The register has exactly two entries. -/
theorem continuationFacts_length : continuationFacts.length = 2 := by decide

end PunoCalculus.ContinuationCriterion
