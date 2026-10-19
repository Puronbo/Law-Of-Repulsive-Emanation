/-
  Wilson primes (Gap Ledger G36), promoted from a Python finite scan to a
  machine-checked theorem.

  A Wilson prime is a prime `p` with `p^2 | (p-1)! + 1`.  Only `p = 5, 13, 563`
  are known (Wilson 1770; OEIS A007540); whether infinitely many exist is OPEN.

  This module *proves in Lean* that 5, 13 and 563 are Wilson primes.  The instances
  5 and 13 close by `norm_num`; 563 does not, because `562!` has 1304 digits, so it
  is computed as an exact modular factorial in the kernel: `factMod 562 563^2`
  reduces mod `563^2` at every one of the 562 multiplication steps and stays a
  machine word, `decide` certifies `factMod_562`, and `factMod_eq` bridges that to
  `562! % 563^2`.  No floating point, no external search, no approximation.

  The 0/0 / crease reading.  Wilson's theorem says `p | (p-1)! + 1` for every prime
  `p` (`wilson_dvd`) -- a first-order zero of the Wilson resolvent that holds
  *universally*, and so cannot discriminate one prime from another.  A Wilson prime
  is exactly where that resolvent acquires a *second-order* zero, `p^2 | (p-1)!+1`,
  equivalently `p` divides the Wilson quotient `w_p = ((p-1)! + 1)/p`
  (`isWilsonPrime_iff_quotient_dvd`) -- the same first-order -> second-order upgrade
  that defines a Wieferich prime (`PunoCalculus.Wieferich`) and the same degeneracy
  as the fold crease in `PunoCalculus.Crease`.  `first_order_tests_are_universal`
  records that *both* arithmetic first-order tests (Fermat's and Wilson's) hold for
  every odd prime, so neither can tell a crease from a non-crease: only the square
  condition can.

  Scope.  Proves: the three known instances and their primality; the modular
  factorial bridge; Wilson's theorem in divisibility form; the order-2 restatement;
  the quotient restatement and its three instances; and the universality of the two
  first-order tests.  Infinitude stays OPEN -- this is an exact arithmetic
  certificate for the known instances, not a proof about the family's size.
-/
import Mathlib
import PunoCalculus.Wieferich

namespace PunoCalculus.Wilson

/-- A Wilson prime: a prime `p` with `p^2 | (p-1)! + 1`. -/
def IsWilsonPrime (p : ℕ) : Prop := Nat.Prime p ∧ p ^ 2 ∣ Nat.factorial (p - 1) + 1

/-- Exact modular factorial: `factMod n m` is `n!` reduced modulo `m` after every
multiplication step, so the intermediate values stay below `m` even when `n!` is
astronomically large. -/
def factMod : ℕ → ℕ → ℕ
  | 0, m => 1 % m
  | k + 1, m => ((k + 1) * factMod k m) % m

/-- `factMod` computes a representative of `n!` modulo `m`. -/
theorem factMod_modEq (n m : ℕ) : factMod n m ≡ Nat.factorial n [MOD m] := by
  induction n with
  | zero => rw [factMod, Nat.factorial_zero]; exact Nat.mod_modEq 1 m
  | succ k ih =>
    rw [factMod, Nat.factorial_succ]
    exact (Nat.mod_modEq _ _).trans ((Nat.ModEq.refl (k + 1)).mul ih)

/-- Every modular factorial stays strictly below the modulus. -/
theorem factMod_lt {m : ℕ} (hm : 0 < m) (n : ℕ) : factMod n m < m := by
  induction n with
  | zero => exact Nat.mod_lt 1 hm
  | succ k _ => exact Nat.mod_lt _ hm

/-- The bridge: the stepwise-reduced factorial really is `n! % m`. -/
theorem factMod_eq {m : ℕ} (hm : 0 < m) (n : ℕ) :
    factMod n m = Nat.factorial n % m := by
  have h := factMod_modEq n m
  have hlt := factMod_lt hm n
  rw [← Nat.mod_eq_of_lt hlt]
  exact h

set_option maxRecDepth 100000 in
/-- `562! = -1 (mod 563^2)`, certified exactly in the kernel by `decide` over the
562-step modular factorial (no float, no external search). -/
theorem factMod_562 : factMod 562 (563 ^ 2) = 563 ^ 2 - 1 := by decide

theorem prime_five : Nat.Prime 5 := by norm_num

theorem prime_thirteen : Nat.Prime 13 := by norm_num

theorem prime_563 : Nat.Prime 563 := by norm_num

/-- **Wilson's theorem**, divisibility form: every prime `p` divides `(p-1)! + 1`.
This is the *first-order* zero of the Wilson resolvent, and it holds for every
prime -- hence it cannot discriminate. -/
theorem wilson_dvd (p : ℕ) [Fact (Nat.Prime p)] : p ∣ Nat.factorial (p - 1) + 1 := by
  rw [← ZMod.natCast_eq_zero_iff]
  rw [Nat.cast_add, Nat.cast_one]
  rw [ZMod.wilsons_lemma]
  exact neg_add_cancel 1

/-- `5` is a Wilson prime: `5^2 | 4! + 1`. -/
theorem wilson_five : IsWilsonPrime 5 := ⟨prime_five, by norm_num⟩

/-- `13` is a Wilson prime: `13^2 | 12! + 1`. -/
theorem wilson_thirteen : IsWilsonPrime 13 := ⟨prime_thirteen, by norm_num⟩

/-- The divisibility needed for `563`, computed from the kernel-checked modular
factorial `factMod_562`. -/
theorem wilson_563_sq : (563 ^ 2 : ℕ) ∣ Nat.factorial 562 + 1 := by
  have hm : 0 < 563 ^ 2 := by norm_num
  rw [Nat.dvd_iff_mod_eq_zero, Nat.add_mod]
  have h := factMod_562
  rw [factMod_eq hm 562] at h
  rw [h]
  norm_num

/-- `563` is a Wilson prime -- the instance that required the modular factorial. -/
theorem wilson_563 : IsWilsonPrime 563 := ⟨prime_563, wilson_563_sq⟩

/-- `b^2 | a` if and only if `b | a/b`, whenever `b | a`: the order-2 condition is
exactly divisibility of the quotient. -/
theorem sq_dvd_iff_dvd_div {b a : ℕ} (hb : 0 < b) (hdvd : b ∣ a) :
    b ^ 2 ∣ a ↔ b ∣ a / b := by
  rw [Nat.pow_two]
  constructor
  · intro h
    have h2 : b * (a / b) = a := Nat.mul_div_cancel' hdvd
    rw [← h2] at h
    exact Nat.dvd_of_mul_dvd_mul_left hb h
  · intro hd
    have h1 : b * (a / b / b) = a / b := Nat.mul_div_cancel' hd
    have h2 : b * (a / b) = a := Nat.mul_div_cancel' hdvd
    rw [← h2, ← h1, ← Nat.mul_assoc]
    exact Nat.dvd_mul_right _ _

/-- The Wilson quotient `w_p = ((p-1)! + 1)/p`.  An integer for every prime `p` by
Wilson's theorem -- the resolvable 0/0. -/
def wilsonQuotient (p : ℕ) : ℕ := (Nat.factorial (p - 1) + 1) / p

/-- The crease of the Wilson resolvent: a prime `p` is a Wilson prime if and only if
`p` divides the Wilson quotient `w_p` -- the second-order zero. -/
theorem isWilsonPrime_iff_quotient_dvd (p : ℕ) (hp : Nat.Prime p) :
    IsWilsonPrime p ↔ p ∣ wilsonQuotient p := by
  have : Fact (Nat.Prime p) := Fact.mk hp
  have hdvd := wilson_dvd p
  have hsq : p ^ 2 ∣ Nat.factorial (p - 1) + 1 ↔ p ∣ (Nat.factorial (p - 1) + 1) / p :=
    sq_dvd_iff_dvd_div hp.pos hdvd
  show IsWilsonPrime p ↔ p ∣ (Nat.factorial (p - 1) + 1) / p
  exact ⟨fun h => hsq.mp h.2, fun h => ⟨hp, hsq.mpr h⟩⟩

/-- `5` divides its Wilson quotient: the second-order zero at 5. -/
theorem quotient_five_dvd : 5 ∣ wilsonQuotient 5 :=
  (isWilsonPrime_iff_quotient_dvd 5 prime_five).mp wilson_five

/-- `13` divides its Wilson quotient: the second-order zero at 13. -/
theorem quotient_thirteen_dvd : 13 ∣ wilsonQuotient 13 :=
  (isWilsonPrime_iff_quotient_dvd 13 prime_thirteen).mp wilson_thirteen

/-- `563` divides its Wilson quotient: the second-order zero at 563. -/
theorem quotient_563_dvd : 563 ∣ wilsonQuotient 563 :=
  (isWilsonPrime_iff_quotient_dvd 563 prime_563).mp wilson_563

/-- **Both** arithmetic first-order tests are universal on their domains: Fermat's
`p | 2^(p-1) - 1` for an odd prime, and Wilson's `p | (p-1)! + 1` for any prime.
Neither first-order test can therefore discriminate a crease from a non-crease;
only the second-order (square) condition can. -/
theorem first_order_tests_are_universal (p : ℕ) (hp : Nat.Prime p) (h2 : p ≠ 2) :
    p ∣ 2 ^ (p - 1) - 1 ∧ p ∣ Nat.factorial (p - 1) + 1 := by
  have : Fact (Nat.Prime p) := Fact.mk hp
  exact ⟨PunoCalculus.Wieferich.fermat_dvd p hp h2, wilson_dvd p⟩

/-- Register of rigorously established facts about Wilson primes. -/
def wilsonFacts : List (String × String) :=
  [ ("definition", "p is a Wilson prime iff p is prime and p^2 divides (p-1)! + 1"),
    ("instance_5", "5 is a Wilson prime (kernel-checked)"),
    ("instance_13", "13 is a Wilson prime (kernel-checked)"),
    ("instance_563", "563 is a Wilson prime (exact modular factorial, kernel-checked)"),
    ("modular_factorial", "factMod n m = n! % m, so 562! mod 563^2 is certified without 1304-digit intermediates"),
    ("wilson", "Wilson's theorem: every prime p divides (p-1)! + 1 -- the universal first-order zero"),
    ("order2", "Wilson prime iff p^2 divides (p-1)! + 1: the resolvent's second-order zero"),
    ("quotient", "Wilson prime iff p divides the Wilson quotient ((p-1)! + 1)/p"),
    ("quotient_instances", "5, 13 and 563 each divide their own Wilson quotient"),
    ("first_order_universal", "Fermat and Wilson first-order tests hold for every odd prime, so neither discriminates"),
    ("open", "infinitude of Wilson primes is OPEN (only 5, 13, 563 known)") ]

theorem wilsonFacts_length : wilsonFacts.length = 11 := by decide

end PunoCalculus.Wilson
