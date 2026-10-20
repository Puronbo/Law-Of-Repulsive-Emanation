/-
  Perfect numbers and Mersenne primes, kernel-checked (Gap Ledger G27, G29).

  `02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/
  perfect_numbers_certificate.py` certifies these by a divisor-sum sieve to
  10^6 and a Lucas-Lehmer run to exponent 5000.  This module re-certifies the
  same statements in the Lean kernel on its own (smaller) windows, plus the
  exact arithmetic facts that need no window at all.

  What is a theorem here and what is not:

  * **Theorem (exact).**  `Nat.Perfect` holds for 6, 28, 496, 8128 (Mathlib's
    own `Perfect`, i.e. its Finset sum of divisors), and `euclidForm p` for
    p = 2,3,5,7 equals exactly those four numbers.
  * **Theorem (window).**  No even perfect number other than 6, 28, 496 lies
    below 2000, and no odd perfect number lies below 2000, each computed by
    *direct divisor summation* -- an independent sigma from Mathlib's.
  * **Theorem (exact, primality).**  For every prime exponent p <= 31 the
    primality of `M_p = 2^p - 1` is decided in-kernel: prime for
    p = 2,3,5,7,13,17,19,31, composite for p = 11,23,29.  (`decide` on
    `Nat.Prime` for numbers past ~10^5 recurses past the kernel depth limit,
    so the large cases go through `norm_num`.)
  * **Theorem (algorithm).**  The Lucas-Lehmer iteration returns 0 exactly for
    p = 2,3,5,7,13,17,19,31 among prime exponents <= 31.  Its equivalence to
    primality is the classical Lucas-Lehmer theorem, cited here, not proved.
  * **Not a theorem.**  That no odd perfect number exists (best bound
    > 10^1500, Ochem-Rao), that infinitely many Mersenne primes exist, and
    Euler's *necessity* of the form below.  All stay OPEN.
-/
import Mathlib
import PunoCalculus.FiniteScan

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

namespace PunoCalculus.PerfectNumbers

open PunoCalculus.FiniteScan

/-! ### Divisor sum and perfection (G27) -/

/-- `sigma(n)` by direct summation: every `i` in `0..n` that divides `n` is
added.  Plain lists rather than a `Finset`, so the kernel can scan a window
without building Finsets -- and the result is sigma by construction. -/
def divisorSum (n : ℕ) : ℕ :=
  (List.range (n + 1)).foldl (fun acc i => if i ∣ n then acc + i else acc) 0

/-- `n` is perfect when `sigma(n) = 2n`. -/
def isPerfectB (n : ℕ) : Bool := divisorSum n = 2 * n

/-- Mathlib's `Nat.Perfect` (sum of *proper* divisors equals `n`) agrees with
the `sigma(n) = 2n` formulation, on each of the four numbers certified here. -/
theorem perfect_6 : Nat.Perfect 6 := by
  exact (Nat.perfect_iff_sum_divisors_eq_two_mul (by norm_num)).mpr (by decide)

theorem perfect_28 : Nat.Perfect 28 := by
  exact (Nat.perfect_iff_sum_divisors_eq_two_mul (by norm_num)).mpr (by decide)

theorem perfect_496 : Nat.Perfect 496 := by
  exact (Nat.perfect_iff_sum_divisors_eq_two_mul (by norm_num)).mpr (by decide)

theorem perfect_8128 : Nat.Perfect 8128 := by
  exact (Nat.perfect_iff_sum_divisors_eq_two_mul (by norm_num)).mpr (by decide)

/-- The direct-sum sigma agrees with `2n` at 8128 as well -- so the two
independent sigma computations certify the same number. -/
theorem isPerfect_8128 : isPerfectB 8128 = true := by decide

/-- No even perfect number in `2 <= n < 2000` other than 6, 28, 496.
(A window; the Python certificate scans to 10^6.) -/
theorem even_perfect_window :
    ((List.range 2000).filter (fun n => 2 ≤ n && n % 2 = 0 && isPerfectB n))
      = [6, 28, 496] := by decide

/-- No odd perfect number in `2 <= n < 2000`.  (A window; none is known at
all, and the Python certificate scans to 10^6 -- the conjecture is OPEN.) -/
theorem odd_perfect_window :
    ((List.range 2000).filter (fun n => 2 ≤ n && n % 2 = 1 && isPerfectB n))
      = [] := by decide

/-! ### Euler's necessary form (structural, conditional) -/

/-- Euler's shape for an odd perfect number: `n = q^a * m^2`. -/
def eulerOddForm (q a m : ℕ) : ℕ := q ^ a * m ^ 2

/-- Conditional on Euler's classical necessary form for an odd perfect number
with `q = 1 mod 4` (cited, not proved here), such a number is `1 mod 4`.
This is a *conditional* structural fact, not a proof that no odd perfect
number exists. -/
theorem eulerOddForm_mod4 (q a m : ℕ) (hq : q % 4 = 1) (hm : m % 2 = 1) :
    eulerOddForm q a m % 4 = 1 := by
  have hqa : q ^ a % 4 = 1 := by rw [Nat.pow_mod, hq]; simp
  obtain h1 | h3 : m % 4 = 1 ∨ m % 4 = 3 := by omega
  · have hm2 : m ^ 2 % 4 = 1 := by rw [Nat.pow_mod, h1]
    rw [eulerOddForm, Nat.mul_mod, hqa, hm2]
  · have hm2 : m ^ 2 % 4 = 1 := by rw [Nat.pow_mod, h3]
    rw [eulerOddForm, Nat.mul_mod, hqa, hm2]

/-! ### Euclid-Euler form of the even perfect numbers (G29) -/

/-- Euclid-Euler: the even perfect number built from the exponent `p`. -/
def euclidForm (p : ℕ) : ℕ := 2 ^ (p - 1) * (2 ^ p - 1)

theorem euclidForm_2 : euclidForm 2 = 6 := by norm_num [euclidForm]

theorem euclidForm_3 : euclidForm 3 = 28 := by norm_num [euclidForm]

theorem euclidForm_5 : euclidForm 5 = 496 := by norm_num [euclidForm]

theorem euclidForm_7 : euclidForm 7 = 8128 := by norm_num [euclidForm]

/-! ### Lucas-Lehmer (G29) -/

/-- The Lucas-Lehmer iteration `s <- s^2 - 2 mod M_p`, `p-2` steps, `s0 = 4`. -/
def llAux (m : ℕ) : ℕ → ℕ → ℕ
  | 0, s => s
  | fuel + 1, s => llAux m fuel ((s * s - 2) % m)

/-- Lucas-Lehmer for the exponent `p`: `M_p` passes iff the iteration ends at
0 (with `p = 2` handled separately, `M_2 = 3`).  The equivalence with
primality is the classical Lucas-Lehmer theorem -- cited, not proved. -/
def lucasLehmerB (p : ℕ) : Bool :=
  if p = 2 then decide (2 ^ 2 - 1 = 3)
  else llAux (2 ^ p - 1) (p - 2) 4 = 0

/-- Lucas-Lehmer accepts exactly the exponents `2,3,5,7,13,17,19,31` among the
prime exponents `<= 31`. -/
theorem mersenne_window_ll :
    (primesUpTo 31).filter (fun p => lucasLehmerB p)
      = [2, 3, 5, 7, 13, 17, 19, 31] := by decide

/-! ### Mersenne primality, decided in-kernel (no reliance on Lucas-Lehmer) -/

/-- Primality of `M_p` decided by `decide` for prime exponents up to 13 --
the range where `Nat.Prime`'s decidability stays inside the kernel depth. -/
theorem mersenne_primality_window :
    (primesUpTo 13).filter (fun p => isPrimeB (2 ^ p - 1))
      = [2, 3, 5, 7, 13] := by decide

theorem mersenne_17 : Nat.Prime (2 ^ 17 - 1) := by norm_num

theorem mersenne_19 : Nat.Prime (2 ^ 19 - 1) := by norm_num

theorem mersenne_31 : Nat.Prime (2 ^ 31 - 1) := by norm_num

theorem not_mersenne_11 : ¬ Nat.Prime (2 ^ 11 - 1) := by norm_num

theorem not_mersenne_23 : ¬ Nat.Prime (2 ^ 23 - 1) := by norm_num

theorem not_mersenne_29 : ¬ Nat.Prime (2 ^ 29 - 1) := by norm_num

/-- Register of rigorously established facts about perfect numbers and
Mersenne primes. -/
def perfectNumberFacts : List (String × String) :=
  [ ("perfect_exact", "Nat.Perfect holds for 6, 28, 496 and 8128 (kernel-checked)"),
    ("perfect_even_window", "no other even perfect number below 2000 (direct divisor summation)"),
    ("odd_perfect_window", "no odd perfect number below 2000 (direct divisor summation)"),
    ("euler_form", "n = q^a m^2 with q = 1 mod 4 and m odd forces n = 1 mod 4 (conditional)"),
    ("euclid_euler", "euclidForm p = 2^(p-1) (2^p - 1) equals 6, 28, 496, 8128 for p = 2,3,5,7"),
    ("lucas_lehmer", "LL accepts exactly 2,3,5,7,13,17,19,31 among prime exponents <= 31"),
    ("mersenne_primality", "M_p prime iff p in {2,3,5,7,13,17,19,31}, for every prime p <= 31"),
    ("open", "no odd perfect number exists / Mersenne primes infinite: both remain OPEN") ]

theorem perfectNumberFacts_length : perfectNumberFacts.length = 8 := by decide

end PunoCalculus.PerfectNumbers
