import Mathlib

/-!
# Section 8's lower-bound mechanism, formalised (Lean 4, Mathlib)

Machine-checked content behind `rh_widder_hankel_h8.py`'s H8d gate.

Writing `A(m) = sum_k rho_k^m` for the finite moment sums the ladder code
actually evaluates, and

    Q_m = A(m) + 2 cos(m theta)

for the quadratic form, three claims are proved:

1. `A(m)` is non-increasing in `m`, because every `rho_k` lies in `[0, 1]`.
2. `A(m) > 2` forces `Q_m > 0`, uniformly in the phase, because `cos >= -1`.
3. Chaining the two: positivity at a *finer* exponent `q` certifies positivity at
   every coarser `p <= q`, so one verified exponent yields an interval of the
   ladder.  The reverse transfer is invalid and is not claimed -- see
   `moment_antitone` and `moment_gt_two_at_coarser`.

Scope, stated honestly: the monotonicity is proved for `m` in the natural
numbers.  The Python ladder bisects over real `m`; this file covers the integer
ladder points and does not claim the real-exponent statement.  The `Q_m` results
hold for all real `m`.

Also recorded here is the limit of the argument: `cos >= -1` gives
`Q_m >= A(m) - 2` and nothing stronger.  Any claim that `Q_m` is bounded away
from zero without a moment lower bound would be false, and none is made.
-/

namespace PunoCalculus.RH

variable {ι : Type*}

/-- The `p`-th moment sum of the zero ordinates, matching the Python ladder's
`A(m) = sum_k rho_k^m` over a finite truncation of the spectrum. -/
def moment (rhos : ι → ℝ) (s : Finset ι) (p : ℕ) : ℝ :=
  Finset.sum s (fun k => rhos k ^ p)

/-- Raising a base in `[0, 1]` to a larger exponent can only shrink it. -/
theorem pow_antitone_of_le_one {rho : ℝ} (hx0 : 0 ≤ rho) (hx1 : rho ≤ 1) {p q : ℕ}
    (hp : p ≤ q) : rho ^ q ≤ rho ^ p := by
  have hdecomp : p + (q - p) = q := Nat.add_sub_of_le hp
  rw [← hdecomp, pow_add]
  calc rho ^ p * rho ^ (q - p) ≤ rho ^ p * 1 :=
        mul_le_mul_of_nonneg_left (pow_le_one₀ (n := q - p) hx0 hx1) (pow_nonneg hx0 p)
    _ = rho ^ p := mul_one _

/-- The finite moment sum is non-increasing in the exponent.  This is the step
that lets a bound proved at a coarser exponent survive at a finer one. -/
theorem moment_antitone {s : Finset ι} {rhos : ι → ℝ}
    (hrho : ∀ k ∈ s, 0 ≤ rhos k ∧ rhos k ≤ 1) {p q : ℕ} (hp : p ≤ q) :
    moment rhos s q ≤ moment rhos s p := by
  unfold moment
  refine Finset.sum_le_sum (N := ℝ) (s := s) (fun k hk => ?_)
  obtain ⟨h0, h1⟩ := hrho k hk
  exact pow_antitone_of_le_one h0 h1 hp

/-- The quadratic form `Q_m = A(m) + 2 cos(m theta)`. -/
noncomputable def qForm (A m theta : ℝ) : ℝ := A + 2 * Real.cos (m * theta)

/-- `cos >= -1`, so `Q_m >= A(m) - 2`.  This is the best bound obtainable from
`cos` alone and is recorded so the limit is explicit. -/
theorem qForm_sub_two_le (A m theta : ℝ) : A - 2 ≤ qForm A m theta := by
  have hcos : -1 ≤ Real.cos (m * theta) := Real.neg_one_le_cos _
  unfold qForm
  linarith

/-- And `Q_m <= A(m) + 2`. -/
theorem qForm_le_add_two (A m theta : ℝ) : qForm A m theta ≤ A + 2 := by
  have hcos : Real.cos (m * theta) ≤ 1 := Real.cos_le_one _
  unfold qForm
  linarith

/-- H8d's implication: a moment sum strictly above 2 forces the quadratic form
strictly positive, for every phase and every real exponent. -/
theorem qForm_pos_of_moment_gt_two {A m theta : ℝ} (hA : 2 < A) :
    0 < qForm A m theta := by
  have hcos : -1 ≤ Real.cos (m * theta) := Real.neg_one_le_cos _
  unfold qForm
  linarith

/-- The full lower-bound route, in the direction where monotonicity actually
helps.  If the moment sum at the *finer* exponent `q` exceeds 2, then it exceeds
2 at every coarser exponent `p <= q` as well.

Note the direction.  `moment_antitone` gives `A(q) <= A(p)` for `p <= q`, so a
bound proved at the coarse exponent does *not* descend to the fine one -- `A`
only decreases, and a bound on `A(p)` says nothing about `A(q)`.  What does
transfer is the reverse: one verified fine exponent certifies every coarser
exponent, hence a whole interval of the ladder rather than a single point. -/
theorem moment_gt_two_at_coarser {s : Finset ι} {rhos : ι → ℝ}
    (hrho : ∀ k ∈ s, 0 ≤ rhos k ∧ rhos k ≤ 1) {p q : ℕ} (hp : p ≤ q)
    (hA : 2 < moment rhos s q) : 2 < moment rhos s p :=
  lt_of_lt_of_le hA (moment_antitone hrho hp)

/-- Positivity of the form at a finer exponent certifies positivity at every
coarser one.  This is the statement H8d's ladder scan is really relying on: a
single verified `m` yields an interval, not an isolated point. -/
theorem qForm_pos_at_coarser {s : Finset ι} {rhos : ι → ℝ}
    (hrho : ∀ k ∈ s, 0 ≤ rhos k ∧ rhos k ≤ 1) {p q : ℕ} (hp : p ≤ q)
    (hA : 2 < moment rhos s q) (theta : ℝ) :
    0 < qForm (moment rhos s p) (p : ℝ) theta := by
  refine qForm_pos_of_moment_gt_two (A := moment rhos s p) (m := (p : ℝ))
    (theta := theta) ?_
  exact moment_gt_two_at_coarser hrho hp hA

end PunoCalculus.RH
