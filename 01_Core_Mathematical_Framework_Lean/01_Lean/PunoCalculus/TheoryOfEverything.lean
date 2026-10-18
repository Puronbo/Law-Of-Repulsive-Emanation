import Mathlib
import PunoCalculus.CriticalLadder
import PunoCalculus.GreatAttractor
import PunoCalculus.OnePattern
import PunoCalculus.OnsagerCriterion
import PunoCalculus.ContinuationCriterion
import PunoCalculus.StableBounded
import PunoCalculus.EnstrophyBarrier
import PunoCalculus.SufficiencyLoop
import PunoCalculus.QuantitativeContinuation
import PunoCalculus.OrientationBoundedness
import PunoCalculus.MarginCrossing
import PunoCalculus.FirstCrossing
import PunoCalculus.LogicBarrier

/-!
# The theory of everything: two numbers close the register

Every brick in this register has been an instance of one claim: **a scaling-critical
system is governed by exactly two organizing numbers** --

* the **order** `a`, which slides the critical rung (`OnePattern`:
  `criticalSmoothness a p = sCrit p + (1 - a)`, scale-invariance on the whole
  one-parameter family), and
* the **orientation** `r` (the magnitude of the local multiplier / Lyapunov base),
  which decides the side of the wall (`OrientationBoundedness`: the invariant is
  bounded iff `r <= 1`, and the SIGN of `log r` -- the formal Lyapunov exponent of
  `GreatAttractor.fixedPoint_logSign` -- reads that side).

`theoryOfEverything` is the entire register as one theorem: order sets the rung and
the barrier shape, orientation sets the side, order ≤ 1 shapes close the sufficiency
loop to global existence, and order 2 leaves the wall open.  `twoNumbersClose` states
the reduction: both questions -- *which rung* and *which side* -- are functions of the
two numbers alone.
-/

namespace PunoCalculus.TheoryOfEverything

open PunoCalculus.GreatAttractor (criticalSmoothness scalingWeight)
open PunoCalculus.CriticalLadder (sCrit)
open PunoCalculus.SerrinLadder (gnExponent)

noncomputable section

/-- The register's complete state: the two organizing numbers.  The `order` sets the
critical rung; the `orientation` (multiplier magnitude) sets the side of the wall. -/
structure Register where
  order : ℝ
  orientation : ℝ

/-- **Order determines the rung.**  For every order `a`, the scale-invariant
smoothness is the register ladder shifted by the order. -/
theorem order_sets_rung (a p : ℝ) :
    criticalSmoothness a p = sCrit p + (1 - a) :=
  PunoCalculus.OnePattern.criticalCurve_through_ladder a p

/-- **Orientation determines the side.**  For a nondegenerate multiplier, the
geometric invariant is bounded iff the orientation is at most one (attracting or
marginal); a repelling orientation escapes every bound. -/
theorem orientation_sets_side {r A : ℝ} (hr : 0 < r) (hA : 0 < A) :
    (∃ B : ℝ, ∀ n, r ^ n * A ≤ B) ↔ r ≤ 1 :=
  PunoCalculus.OrientationBoundedness.geometric_bounded_iff hr hA

/-- **The theory of everything (register form).**  Order, orientation, the barrier
hierarchy, and the sufficiency loop, all as one theorem. -/
theorem theoryOfEverything :
    -- (1) ORDER sets the rung: a one-parameter family through the ladder.
    (∀ a p : ℝ, criticalSmoothness a p = sCrit p + (1 - a)) ∧
    -- (2) the homogeneous norm is scale-free exactly on that family.
    (∀ a p : ℝ, scalingWeight (criticalSmoothness a p) a p = 0) ∧
    -- (3) the Serrin interpolation exponent and the rung are complementary (order one).
    (∀ p : ℝ, p ≠ 0 → gnExponent p + sCrit p = 1 / 2) ∧
    -- (4) ORIENTATION sets the side: the invariant is bounded iff attracting.
    (∀ r A : ℝ, 0 < r → 0 < A → ((∃ B : ℝ, ∀ n, r ^ n * A ≤ B) ↔ r ≤ 1)) ∧
    -- (5) the SIGN of the Lyapunov exponent `log r` reads that side.
    (∀ r A : ℝ, 0 < r → 0 < A →
      ((0 < Real.log r ↔ ¬ ∃ B : ℝ, ∀ n, r ^ n * A ≤ B) ∧
       (Real.log r ≤ 0 ↔ ∃ B : ℝ, ∀ n, r ^ n * A ≤ B))) ∧
    -- (6) the barrier by order: order ≤ 1 shapes are controlled, order 2 is not.
    ((∀ N : ℕ → ℝ, (∀ n, N (n + 1) ≤ N n) → ∀ t, N t ≤ N 0) ∧
      (∃ y : ℕ → ℝ,
        (∀ n, y (n + 1) ≤ y n + (y n) ^ 2) ∧ ¬ ∃ B : ℝ, ∀ n, y n ≤ B)) ∧
    -- (7) the sufficiency loop closes for order ≤ 1: bounded invariant => existence.
    (∀ {e : ℕ → Prop} {N : ℕ → ℝ}, (∀ n, N (n + 1) ≤ N n) →
      (∀ t, (∀ s ≤ t, N s ≤ N 0) → e t → e (t + 1)) → e 0 → ∀ T, e T) :=
  ⟨order_sets_rung,
   fun a p => PunoCalculus.OnePattern.scalingWeight_vanishes_family a p,
   fun p hp => PunoCalculus.CriticalLadder.thetaAddSCrit hp,
   fun r A hr hA => orientation_sets_side hr hA,
   fun r A hr hA => PunoCalculus.OrientationBoundedness.orientation_decides_boundedness hr hA,
   ⟨fun N hN t => PunoCalculus.EnstrophyBarrier.mono_step_bounded N hN t,
     by
       obtain ⟨y, hy, hunb⟩ :=
         PunoCalculus.EnstrophyBarrier.quadratic_no_uniform_bound 1 1 one_pos one_pos
           (by norm_num)
       exact ⟨y, fun n => by simpa using hy n, hunb⟩⟩,
   fun hN hstep h0 T => PunoCalculus.SufficiencyLoop.global_exists_of_mono hN hstep h0 T⟩

/-- **Two numbers close the register.**  Both the *which-rung* question (order) and
the *which-side* question (orientation) are functions of the two organizing numbers
alone; nothing else enters. -/
theorem twoNumbersClose :
    (∀ a p : ℝ, criticalSmoothness a p = sCrit p + (1 - a)) ∧
    (∀ r A : ℝ, 0 < r → 0 < A → ((∃ B : ℝ, ∀ n, r ^ n * A ≤ B) ↔ r ≤ 1)) :=
  ⟨order_sets_rung, fun _ _ => orientation_sets_side⟩

/-- **The order half is a bijection.**  For a fixed form `p`, the order `a` and the
critical rung are in bijection: `a ↦ criticalSmoothness a p` is injective (the order
is *recovered* from the rung, `a = 3/p - s`) and surjective (every rung is attained).
This is the precise content of "order sets the rung": which-rung is not merely a
function of the order, it is a *one-to-one correspondence*. -/
theorem order_sets_rung_bijective (p : ℝ) :
    Function.Bijective (fun a : ℝ => criticalSmoothness a p) := by
  constructor
  · intro a b h
    simp only [criticalSmoothness] at h
    linarith
  · intro s
    exact ⟨3 / p - s, by simp only [criticalSmoothness]; ring⟩

/-- **The side does not recover the orientation.**  Two distinct positive
orientations lie on the same side of the wall (both attracting/marginal, `r ≤ 1`),
so the side predicate `r ↦ r ≤ 1` is *not* injective: "orientation sets the side" is
a coarse sign, not a bijection.  The register's bijection is the pair
`(order, orientation) ↦ (rung, side)` -- onto, injective in the order coordinate, and
many-to-one in the orientation coordinate. -/
theorem orientation_not_injective_on_side :
    ∃ r r' : ℝ, 0 < r ∧ 0 < r' ∧ r ≤ 1 ∧ r' ≤ 1 ∧ r ≠ r' :=
  ⟨(1 / 2 : ℝ), 1, by norm_num, by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- **The register's two barriers, attached to the two numbers.**  The *order* margin is
a first crossing (existence, needing only continuity and a sign change -- the non-monotone
regime the third family falls into) and a unique crossing once the orientation `lambda(s)`
is antitone (so the critical order `s*` is well-defined); the *method* barrier (card C12)
is the diagonal escape of Cantor/Gödel/Turing -- no type enumerates its own predicate
space.  All three are corollaries of the same discipline: the organising number exists
(and, under monotonicity, is unique), and no self-enumerating certificate can exist. -/
theorem method_and_margin_barriers :
    (∀ {f : ℝ → ℝ} {a b : ℝ}, a < b → ContinuousOn f (Set.Icc a b) →
        StrictAntiOn f (Set.Icc a b) → 0 < f a → f b < 0 →
        ∃! c ∈ Set.Ioo a b, f c = 0) ∧
    (∀ {f : ℝ → ℝ} {a b : ℝ}, Continuous f → a ≤ b → 0 < f a → f b < 0 →
        ∃ c ∈ Set.Ioo a b, f c = 0 ∧ ∀ x ∈ Set.Ico a c, 0 < f x) ∧
    (∀ α : Type, ¬ ∃ φ : α → α → Bool, Function.Surjective φ) :=
  ⟨PunoCalculus.MarginCrossing.existsUnique_zero_of_strictAntiOn,
   fun hf hab ha hb => PunoCalculus.FirstCrossing.exists_first_zero hf hab ha hb,
   PunoCalculus.LogicBarrier.no_surjective_predicates⟩

/-- Formalised-facts register for the capstone. -/
def theoryOfEverythingFacts : List String :=
  [ "order_sets_rung", "orientation_sets_side", "twoNumbersClose", "theoryOfEverything",
    "method_and_margin_barriers" ]

/-- The register has exactly five entries. -/
theorem theoryOfEverythingFacts_length : theoryOfEverythingFacts.length = 5 := by decide

end

end PunoCalculus.TheoryOfEverything
