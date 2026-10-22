import Mathlib

/-!
# Number parity: the even numbers as the fixed point of accumulation

A small, self-contained number-theory module recording the elementary structure of
the even numbers: evenness is divisibility by `2`; the evens are closed under
addition and multiplication; they are exactly the image of doubling; and the
partial sums of the evens pile up as a product `n(n+1)` that is itself even.

The last fact is the precise content of "the evens pile up and never escape":
the accumulation operation is closed on the evens, so every partial sum of evens
is even.  Nothing here is open -- it is elementary and kernel-checked.
-/

namespace PunoCalculus.NumberParity

/-- Evenness is exactly divisibility by two. -/
theorem even_iff_dvd (n : ℕ) : Even n ↔ 2 ∣ n := even_iff_two_dvd

/-- The even numbers are closed under addition. -/
theorem evens_closed_add {a b : ℕ} (ha : Even a) (hb : Even b) : Even (a + b) :=
  ha.add hb

/-- The even numbers are closed under multiplication by any natural. -/
theorem evens_closed_mul {a b : ℕ} (ha : Even a) : Even (a * b) := ha.mul_right b

/-- Doubling is injective: distinct naturals have distinct doubles. -/
theorem doubling_injective : Function.Injective (fun n : ℕ => 2 * n) :=
  fun a b h => Nat.eq_of_mul_eq_mul_left (by norm_num) h

/-- The even numbers are **exactly** the image of doubling. -/
theorem even_range_is_doubling :
    Set.range (fun n : ℕ => 2 * n) = {m | Even m} := by
  ext m; constructor
  · rintro ⟨k, rfl⟩; exact ⟨k, by ring⟩
  · rintro ⟨k, rfl⟩; exact ⟨k, by ring⟩

/-- **The pile-up.**  The sum of the first `n` even numbers (`0 + 2 + 4 + … + 2n`)
is the product `n(n+1)` -- twice a triangular number. -/
theorem sum_evens (n : ℕ) :
    (Finset.range (n + 1)).sum (fun k => 2 * k) = n * (n + 1) := by
  induction n with
  | zero => simp
  | succ n ih => rw [Finset.sum_range_succ, ih]; ring

/-- The product of two consecutive naturals is always even. -/
theorem product_consecutive_even (n : ℕ) : Even (n * (n + 1)) :=
  Nat.even_mul_succ_self n

/-- **The pile-up never escapes.**  Every partial sum of the even numbers is even:
accumulation is closed on the evens. -/
theorem sum_evens_even (n : ℕ) :
    Even ((Finset.range (n + 1)).sum (fun k => 2 * k)) := by
  rw [sum_evens n]; exact product_consecutive_even n

/-- The number `2` is the unique even prime. -/
theorem two_unique_even_prime {p : ℕ} (hp : p.Prime) (he : Even p) : p = 2 := by
  have hdvd : 2 ∣ p := even_iff_two_dvd.mp he
  rcases hp.eq_one_or_self_of_dvd 2 hdvd with h | h
  · omega
  · exact h.symm

end PunoCalculus.NumberParity
