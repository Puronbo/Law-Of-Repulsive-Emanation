import Mathlib
import PunoCalculus.ContinuationCriterion
import PunoCalculus.EnstrophyBarrier

/-!
# Quantitative continuation: the barrier hierarchy by order

The continuation criterion (`PunoCalculus.ContinuationCriterion`) says a bounded
invariant gives global existence.  *Quantitative* continuation asks how much growth
the invariant may have and still be controlled on a finite window.  The answer is
set by the ORDER of the increment:

* order 0 (`N_{n+1} <= N_n + C`): LINEAR growth, `N_t <= N_0 + C t`;
* order 1 (`N_{n+1} <= (1+C) N_n`): GEOMETRIC growth, `N_t <= (1+C)^t N_0` -- still
  a computable bound on every finite window;
* order 2 (`N_{n+1} <= N_n + C N_n^2`): NO uniform bound (the 3D shape), so the
  continuation engine cannot be started.

`barrier_hierarchy` is the one statement with all three orders.  `exists_upto_of_geometric`
shows the quantitative payoff: an order-one increment yields the explicit window
bound `(1+C)^T N_0`, which feeds the continuation criterion to give existence up to
`T`.  This is the discrete shadow of the classical double-log continuation bounds:
control the invariant at a computable rate and existence follows to any finite time.
-/

namespace PunoCalculus.QuantitativeContinuation

/-- **Order 0: a constant increment grows linearly.** -/
theorem linear_bound {N : ℕ → ℝ} {C : ℝ} (h : ∀ n, N (n + 1) ≤ N n + C) :
    ∀ t, N t ≤ N 0 + C * t := by
  intro t
  induction t with
  | zero => simp
  | succ k ih =>
      have hk : (↑(k + 1) : ℝ) = ↑k + 1 := by push_cast; ring
      rw [hk]
      linarith [h k, ih]

/-- **Order 1: a multiplicative increment grows geometrically**, with the explicit
window bound `(1+C)^t N_0`. -/
theorem geometric_bound {N : ℕ → ℝ} {C : ℝ} (hC : 0 ≤ C)
    (h : ∀ n, N (n + 1) ≤ (1 + C) * N n) :
    ∀ t, N t ≤ (1 + C) ^ t * N 0 := by
  intro t
  induction t with
  | zero => simp
  | succ k ih =>
      calc N (k + 1) ≤ (1 + C) * N k := h k
        _ ≤ (1 + C) * ((1 + C) ^ k * N 0) :=
              mul_le_mul_of_nonneg_left ih (by linarith)
        _ = (1 + C) ^ (k + 1) * N 0 := by rw [pow_succ]; ring

/-- **The barrier hierarchy.**  One statement, three orders: order 0 is linear, order
1 is geometric (both finite on every window), order 2 admits no uniform bound. -/
theorem barrier_hierarchy (C A : ℝ) (hC : 0 < C) (hA : 0 < A) (hCA : 1 ≤ C * A) :
    (∀ N : ℕ → ℝ, (∀ n, N (n + 1) ≤ N n + C) → ∀ t, N t ≤ N 0 + C * t) ∧
    (∀ N : ℕ → ℝ, (∀ n, N (n + 1) ≤ (1 + C) * N n) →
      ∀ t, N t ≤ (1 + C) ^ t * N 0) ∧
    (∃ y : ℕ → ℝ,
      (∀ n, y (n + 1) ≤ y n + C * (y n) ^ 2) ∧ ¬ ∃ B : ℝ, ∀ n, y n ≤ B) :=
  ⟨fun _ h => linear_bound h, fun _ h => geometric_bound (le_of_lt hC) h,
   EnstrophyBarrier.quadratic_no_uniform_bound C A hC hA hCA⟩

/-- **Quantitative continuation (order one).**  With a geometric increment and a
nonnegative start, the invariant is bounded on `[0, T]` by the computable value
`(1+C)^T * N_0`; feeding that bound to the continuation criterion gives existence up
to `T`.  So a controlled growth rate -- not boundedness outright -- already buys any
finite continuation window. -/
theorem exists_upto_of_geometric
    {exists_upto : ℕ → Prop} {N : ℕ → ℝ} {C : ℝ} {T : ℕ}
    (hC : 0 < C) (hN0 : 0 ≤ N 0)
    (h : ∀ n, N (n + 1) ≤ (1 + C) * N n)
    (hstep : ∀ t < T, (∀ s ≤ t, N s ≤ (1 + C) ^ T * N 0) →
      exists_upto t → exists_upto (t + 1))
    (h0 : exists_upto 0) : exists_upto T :=
  ContinuationCriterion.exists_upto_of_bounded hstep h0 (fun s hs => by
    have hb : N s ≤ (1 + C) ^ s * N 0 := geometric_bound (le_of_lt hC) h s
    have hpow : (1 + C) ^ s ≤ (1 + C) ^ T :=
      pow_le_pow_right₀ (by linarith) hs
    exact le_trans hb (mul_le_mul_of_nonneg_right hpow hN0))

/-- Formalised-facts register for `QuantitativeContinuation.lean`. -/
def quantitativeContinuationFacts : List String :=
  [ "linear_bound", "geometric_bound", "barrier_hierarchy", "exists_upto_of_geometric" ]

/-- The register has exactly four entries. -/
theorem quantitativeContinuationFacts_length : quantitativeContinuationFacts.length = 4 := by
  decide

end PunoCalculus.QuantitativeContinuation
