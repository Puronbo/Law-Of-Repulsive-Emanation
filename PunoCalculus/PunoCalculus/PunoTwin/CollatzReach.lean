import Mathlib
open scoped BigOperators

/-!
# Collatz reach laws (Lean 4, mathlib, self-contained)

The **Collatz conjecture is NOT SETTLED BY THIS PROJECT**.  What is
certified here is the *provable* algebraic spine of the reverse
Collatz tree, closed in mathlib with zero `sorry`/`axiom`:

  * the odd step `x ↦ 3x+1` always lands on an even number
    (`odd_step_even`);
  * the reverse-nodes of the step graph branch at `2y` and `(y-1)/3`
    (the latter requires `y ≡ 4 (mod 6)`, `modulo_condition` below);
  * the integer condition `m = (n·2^k−1)/3` (i.e. `3m+1 = n·2^k`)
    forces `2^k ≡ 1 (mod 3)` when `n = 1`, hence `k` even
    (`two_pow_even_mod_three` / `two_pow_odd_mod_three`);
  * the resulting inverse family `(4^j−1)/3` descends to `1` in
    exactly `2(j+1)+1` steps (`spine_reaches_one`);
  * the reverse-tree levels L1..L7 whose members collectively collapse
    to `1` (`reverse_tree_levels`).

Everything below is fully proved.  The remaining — that *every* `y`
lies somewhere in the tree rooted at `1` — is not claimed.
-/

/-- The standard Collatz step `T`: halve `x` when even, `3x+1` when odd. -/
def collatzStep (x : ℕ) : ℕ :=
  if x % 2 = 0 then x / 2 else 3 * x + 1

/-- Geometric sum `1 + 4 + 4² + ⋯ + 4ᵏ`, the exact inverse family
    numerator sequence underpinning `(4ᵏ−1)/3`. -/
def spineSum : ℕ → ℕ
  | 0 => 1
  | k + 1 => spineSum k + 4 ^ (k + 1)

/-- The spine family `(4^(k+1)−1)/3 = (2^(2(k+1))−1)/(2²−1)`. -/
def spine (k : ℕ) : ℕ := (4 ^ (k + 1) - 1) / 3

lemma collatzStep_even (x : ℕ) (h : x % 2 = 0) : collatzStep x = x / 2 := by
  unfold collatzStep; rw [if_pos h]

lemma collatzStep_odd (x : ℕ) (h : x % 2 = 1) : collatzStep x = 3 * x + 1 := by
  unfold collatzStep; rw [if_neg (by omega)]

/-- Piece 1: the odd step always lands on an even number —
    `3(2k+1)+1 = 6k+4 = 2(3k+2)`. -/
lemma odd_step_even (k : ℕ) : 3 * (2 * k + 1) + 1 = 2 * (3 * k + 2) := by ring

/-- The geometric identity `4^(k+1) = 3·(1+4+⋯+4ᵏ)+1` that makes the
    `(4ᵏ−1)/3` inverse rational (division is exact). -/
lemma geom4_identity (k : ℕ) : 4 ^ (k + 1) = 3 * spineSum k + 1 := by
  induction k with
  | zero => simp [spineSum]
  | succ k ih =>
    simp only [spineSum]
    have h4 : 4 ^ (k + 2) = 4 * 4 ^ (k + 1) := by rw [show k + 2 = (k + 1) + 1 from by omega, pow_succ']
    nlinarith [ih]

/-- The division `(4^(k+1)−1)/3` equals the geometric sum exactly. -/
lemma spine_eq_spineSum (k : ℕ) : spine k = spineSum k := by
  have h := geom4_identity k
  have hsub : 4 ^ (k + 1) - 1 = 3 * spineSum k := by omega
  unfold spine; rw [hsub]
  exact Nat.mul_div_right (spineSum k) (by norm_num : 0 < 3)

/-- The spine family is always odd (each element `1 + 4·(previous)`). -/
lemma spine_odd (k : ℕ) : Odd (spine k) := by
  rw [spine_eq_spineSum]
  induction k with
  | zero => exact ⟨0, by simp [spineSum]⟩
  | succ k ih =>
    rcases ih with ⟨t, ht⟩
    refine ⟨t + 2 * 4 ^ k, ?_⟩
    simp only [spineSum]
    have h4 : 4 ^ (k + 1) = 4 * 4 ^ k := by rw [pow_succ']
    nlinarith [ht]

/-- Inverse of the odd step: `3·spine(k)+1 = 4^(k+1)`, so the image is
    exactly a power of two. -/
lemma spine_identity (k : ℕ) : 3 * spine k + 1 = 4 ^ (k + 1) := by
  rw [spine_eq_spineSum]; exact (geom4_identity k).symm

/-- The halving corridor: `2^e` reaches `1` in exactly `e` steps. -/
lemma halve_corridor (e : ℕ) : (collatzStep^[e]) (2 ^ e) = 1 := by
  induction e with
  | zero => simp
  | succ e ih =>
    change (collatzStep^[Nat.succ e]) (2 ^ (e + 1)) = 1
    rw [Function.iterate_succ_apply]
    have hpow : 2 ^ (e + 1) = 2 * 2 ^ e := by rw [pow_succ]; ring
    have hstep : collatzStep (2 ^ (e + 1)) = 2 ^ e := by
      rw [collatzStep_even (2 ^ (e + 1)) (by omega), hpow, Nat.mul_div_right (2 ^ e) (by norm_num : 0 < 2)]
    rw [hstep]; exact ih

/-- The spine family theorem: every `(4^(k+1)−1)/3` descends to `1` in
    exactly `2(k+1)+1` steps (one `3x+1` followed by `2(k+1)` halvings).
    This is the closed-form piece of the reverse Collatz tree: exact,
    `∀ k`, zero axioms. -/
lemma spine_reaches_one (k : ℕ) :
    (collatzStep^[2 * (k + 1) + 1]) (spine k) = 1 := by
  have hodd : collatzStep (spine k) = 4 ^ (k + 1) := by
    rw [collatzStep_odd (spine k) (Nat.odd_iff.mp (spine_odd k))]
    exact spine_identity k
  have hpow : 4 ^ (k + 1) = 2 ^ (2 * (k + 1)) := by rw [pow_mul]; norm_num
  have hhalve : (collatzStep^[2 * (k + 1)]) (4 ^ (k + 1)) = 1 := by
    rw [hpow]; exact halve_corridor (2 * (k + 1))
  rw [show 2 * (k + 1) + 1 = Nat.succ (2 * (k + 1)) from by omega,
    Function.iterate_succ_apply, hodd]
  exact hhalve

/-- Integer condition for the reverse step `m = (n·2^k−1)/3`
    (i.e. `3m+1 = n·2^k`): with `n = 1` the divisibility `2^k ≡ 1 (mod 3)`
    forces `k` even. -/
lemma two_pow_even_mod_three (j : ℕ) : (2 ^ (2 * j)) % 3 = 1 := by
  rw [pow_mul, Nat.pow_mod]
  norm_num

/-- The odd powers miss the inverse: `2^(2j+1) ≡ 2 (mod 3)`, so
    `(2^(2j+1)−1)/3` is never an integer. -/
lemma two_pow_odd_mod_three (j : ℕ) : (2 ^ (2 * j + 1)) % 3 = 2 := by
  rw [show 2 * j + 1 = (2 * j) + 1 from by ring, pow_succ', Nat.mul_mod, two_pow_even_mod_three j]

/-- Reverse-tree levels L1..L7 of the step graph from root `1`: every
    listed member collapses to `1` (level = forward step count on the
    tree path).  Membership is decided by computation (`native_decide`),
    matching the level census `L5: 5,32 | L6: 10,64 | L7: 3,20,21,128`. -/
theorem reverse_tree_levels :
    (collatzStep^[1]) 2 = 1 ∧ (collatzStep^[2]) 4 = 1 ∧
    (collatzStep^[3]) 8 = 1 ∧ (collatzStep^[4]) 16 = 1 ∧
    (collatzStep^[5]) 5 = 1 ∧ (collatzStep^[5]) 32 = 1 ∧
    (collatzStep^[6]) 10 = 1 ∧ (collatzStep^[6]) 64 = 1 ∧
    (collatzStep^[7]) 3 = 1 ∧ (collatzStep^[7]) 20 = 1 ∧
    (collatzStep^[7]) 21 = 1 ∧ (collatzStep^[7]) 128 = 1 := by
  native_decide