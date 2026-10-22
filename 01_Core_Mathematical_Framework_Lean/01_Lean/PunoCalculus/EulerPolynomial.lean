import Mathlib

/-!
# Euler polynomial: why `n² + n + 41` cannot be prime for all `n` (G22)

The polynomial `n² + n + 41` is prime for a famously long initial run
(`n = 0 … 39`) but fails at `n = 40`, where it equals `41²`.  This module records
the refutation of the naive universal claim *and* the **structural reason** it
must fail: for **any** `p > 1`, the shifted polynomial `n² + n + p` is composite at
`n = p - 1`, because there it equals the perfect square `p²`.

So the long initial run is a coincidence of small `n`, not evidence of a universal
statement.  Everything here is elementary and kernel-checked; nothing is open.
-/

namespace PunoCalculus.EulerPolynomial

/-- The Euler reading of the polynomial at `n`. -/
def euler (n : ℕ) : ℕ := n ^ 2 + n + 41

/-- The value at the failure point is a perfect square. -/
theorem euler_forty_eq_square : euler 40 = 41 * 41 := by
  unfold euler; norm_num

/-- `n² + n + 41` is **not** prime at `n = 40` (the naive universal claim is false). -/
theorem euler_forty_not_prime : ¬ Nat.Prime (euler 40) := by
  unfold euler; norm_num

/-- The long initial run is real: the value at `n = 0` is prime. -/
theorem euler_zero_prime : Nat.Prime (euler 0) := by
  unfold euler; norm_num

/-- The long initial run is real: the value at `n = 39` is prime. -/
theorem euler_thirtynine_prime : Nat.Prime (euler 39) := by
  unfold euler; norm_num

/-- **Structural reason.**  For any `p ≥ 1`, `(p-1)² + (p-1) + p = p²`. -/
theorem shifted_at_pred_eq_square (p : ℕ) (hp : 1 ≤ p) :
    (p - 1) ^ 2 + (p - 1) + p = p ^ 2 := by
  zify [hp]; ring

/-- **The general obstruction.**  For **any** `p > 1`, the polynomial `n² + n + p`
is composite at `n = p - 1` (it equals `p²`).  Hence no such polynomial is prime
for all `n`; the universal claim is refuted for every choice of `p > 1`. -/
theorem shifted_not_prime_at_pred (p : ℕ) (hp : 1 < p) :
    ¬ Nat.Prime ((p - 1) ^ 2 + (p - 1) + p) := by
  have hp1 : 1 ≤ p := le_of_lt hp
  rw [shifted_at_pred_eq_square p hp1]
  intro h
  have hd : p ∣ p ^ 2 := ⟨p, by ring⟩
  have hlt : p < p ^ 2 := by nlinarith
  rcases h.eq_one_or_self_of_dvd p hd with h1 | h2 <;> omega

end PunoCalculus.EulerPolynomial
