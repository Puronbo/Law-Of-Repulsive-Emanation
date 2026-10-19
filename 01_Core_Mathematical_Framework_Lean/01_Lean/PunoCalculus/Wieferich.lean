/-
  Wieferich primes, base 2 (Gap Ledger G32), promoted from a Python finite
  certificate to a machine-checked theorem.

  A Wieferich prime (base 2) is a prime `p` with `2^(p-1) = 1 (mod p^2)`.  Only
  `p = 1093` and `p = 3511` are known; whether infinitely many exist is OPEN (a
  Crandall-Dilcher-Pomerance heuristic predicts ~ log log x of them up to x; the
  abc conjecture would give finitely many).

  This module *proves in Lean* that 1093 and 3511 are Wieferich primes, upgrading
  the finite Python search
  (`02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/wieferich_certificate.py`)
  to a kernel-checked statement about the two known instances.  The Python script
  scans a range (decidable membership); this module certifies the positive
  instances and the structural facts exactly.

  The 0/0 / crease reading.  Fermat's little theorem says `p | 2^(p-1) - 1` for a
  prime `p != 2`, so the Fermat quotient `q_p = (2^(p-1) - 1) / p` is an integer:
  a *resolvable* 0/0 (`fermat_dvd`).  A Wieferich prime is exactly where `q_p`
  again vanishes mod `p`, i.e. `p^2 | 2^(p-1) - 1` -- the resolvent acquires a
  *second-order* zero (`isWieferich_iff_sq_dvd`, `isWieferich_iff_quotient_dvd`).
  This is the arithmetic analogue of a crease in `PunoCalculus.Crease`: the point
  where a first-order vanishing (Fermat's `p | ...`) is upgraded to a genuine
  degeneracy (the square `p^2 | ...`).  The register's 0/0 theme thus has a
  number-theoretic instance whose degeneracy is *exactly* what makes Wieferich
  primes rare.

  Scope.  Proves: the two known instances and their primality; the order-2
  divisibility restatement; Fermat's divisibility; the quotient restatement; the
  two quotient instances; and the *no-go* that records why a first-order
  certificate cannot work at all (see `first_order_not_iff_isWieferich`).
  Infinitude stays OPEN.

  The no-go.  `fermat_dvd` makes the first-order resolvent `2^(p-1) - 1` vanish
  mod `p` for *every* odd prime, so the first-order predicate is identically true
  on that domain and separates nothing.  `not_wieferich_3` gives a prime that
  passes that test and is still not Wieferich, so the two predicates are not
  pointwise equivalent (`first_order_not_iff_isWieferich`).  Any certificate whose
  only content is the first-order vanishing therefore accepts every odd prime and
  cannot detect the crease: the discriminating information lives entirely in the
  second order.  This barrier is *proved*, not asserted.
-/
import Mathlib

namespace PunoCalculus.Wieferich

/-- A Wieferich prime, base 2: a prime `p` with `2^(p-1) = 1 (mod p^2)`. -/
def IsWieferich (p : ℕ) : Prop := Nat.Prime p ∧ 2 ^ (p - 1) % p ^ 2 = 1

theorem prime_1093 : Nat.Prime 1093 := by norm_num

theorem prime_3511 : Nat.Prime 3511 := by norm_num

set_option maxRecDepth 100000 in
set_option exponentiation.threshold 5000 in
/-- 1093 is a Wieferich prime: `2^1092 = 1 (mod 1093^2)`. -/
theorem wieferich_1093 : IsWieferich 1093 := ⟨prime_1093, by decide⟩

set_option maxRecDepth 100000 in
set_option exponentiation.threshold 5000 in
/-- 3511 is a Wieferich prime: `2^3510 = 1 (mod 3511^2)`. -/
theorem wieferich_3511 : IsWieferich 3511 := ⟨prime_3511, by decide⟩

/-- The order-2 divisibility restatement: a prime `p` is Wieferich iff the Fermat
difference `2^(p-1) - 1` is divisible by the *square* `p^2` (the second-order
zero of the resolvent). -/
theorem isWieferich_iff_sq_dvd (p : ℕ) (hp : Nat.Prime p) :
    IsWieferich p ↔ p ^ 2 ∣ 2 ^ (p - 1) - 1 := by
  have h1 : 1 ≤ 2 ^ (p - 1) := Nat.one_le_two_pow
  have hp2 : 1 < p ^ 2 := by nlinarith [hp.two_le]
  have hiff : (2 ^ (p - 1) % p ^ 2 = 1) ↔ (p ^ 2 ∣ 2 ^ (p - 1) - 1) := by
    rw [← Nat.modEq_iff_dvd' h1, Nat.ModEq, Nat.mod_eq_of_lt hp2]
    exact eq_comm
  exact ⟨fun h => hiff.mp h.2, fun h => ⟨hp, hiff.mpr h⟩⟩

/-- The Fermat quotient, base 2: `(2^(p-1) - 1) / p`.  An integer for every prime
`p != 2` by Fermat's little theorem (the resolvable 0/0). -/
def fermatQuotient2 (p : ℕ) : ℕ := (2 ^ (p - 1) - 1) / p

/-- Fermat's little theorem, divisibility form: for a prime `p != 2`, `p` divides
`2^(p-1) - 1`.  Hence the Fermat quotient is an integer -- the first-order zero of
`2^(p-1) - 1` at the prime. -/
theorem fermat_dvd (p : ℕ) (hp : Nat.Prime p) (h2 : p ≠ 2) :
    p ∣ 2 ^ (p - 1) - 1 := by
  have hcop : Nat.Coprime 2 p := Nat.coprime_two_left.mpr (hp.odd_of_ne_two h2)
  have h := Nat.ModEq.pow_card_sub_one_eq_one hp hcop
  have h' : 1 ≡ 2 ^ (p - 1) [MOD p] := h.symm
  exact (Nat.modEq_iff_dvd' (Nat.one_le_two_pow : 1 ≤ 2 ^ (p - 1))).mp h'

/-- The crease of the Fermat resolvent: for a prime `p != 2`, `p` is Wieferich iff
the Fermat quotient `q_p` is *itself* divisible by `p` -- the second-order zero.
A first-order vanishing (Fermat) is upgraded to a genuine degeneracy. -/
theorem isWieferich_iff_quotient_dvd (p : ℕ) (hp : Nat.Prime p) (h2 : p ≠ 2) :
    IsWieferich p ↔ p ∣ fermatQuotient2 p := by
  have hsq := isWieferich_iff_sq_dvd p hp
  have hfd : p ∣ 2 ^ (p - 1) - 1 := fermat_dvd p hp h2
  rw [hsq, fermatQuotient2]
  constructor
  · intro h
    obtain ⟨k, hk⟩ := h
    exact ⟨k, by rw [hk, pow_two, mul_assoc, Nat.mul_div_cancel_left _ hp.pos]⟩
  · intro h
    obtain ⟨k, hk⟩ := h
    exact ⟨k, by rw [pow_two, mul_assoc, ← hk, Nat.mul_div_cancel' hfd]⟩

/-- `1093` divides its Fermat quotient: the second-order zero at 1093. -/
theorem quotient_1093_dvd : 1093 ∣ fermatQuotient2 1093 :=
  (isWieferich_iff_quotient_dvd 1093 prime_1093 (by norm_num)).mp wieferich_1093

/-- `3511` divides its Fermat quotient: the second-order zero at 3511. -/
theorem quotient_3511_dvd : 3511 ∣ fermatQuotient2 3511 :=
  (isWieferich_iff_quotient_dvd 3511 prime_3511 (by norm_num)).mp wieferich_3511

theorem prime_3 : Nat.Prime 3 := by norm_num

/-- The witness prime for the no-go: `3` is not a Wieferich prime, since
`2^(3-1) % 3^2 = 4`, not `1`. -/
theorem not_wieferich_3 : ¬ IsWieferich 3 := by
  intro h
  have := h.2
  norm_num at this

/-- The discriminating witness: `p = 3` satisfies the *first-order* Fermat
vanishing `3 | 2^2 - 1` and yet is not Wieferich.  Passing the first-order test
therefore does not imply the crease. -/
theorem first_order_holds_but_not_wieferich_3 :
    3 ∣ 2 ^ (3 - 1) - 1 ∧ ¬ IsWieferich 3 :=
  ⟨by norm_num, not_wieferich_3⟩

/-- **No-go for first-order certificates.**  There is no pointwise equivalence
between the first-order Fermat vanishing `p | 2^(p-1) - 1` and the Wieferich
condition: the first holds for *every* odd prime (`fermat_dvd`), yet it fails to
imply the second already at `p = 3`.  Hence a certificate whose only content is
the first-order vanishing accepts every odd prime and cannot detect the crease --
the discriminating information is entirely second-order.  The barrier is proved
here rather than asserted; it does *not* say Wieferich primes are finite. -/
theorem first_order_not_iff_isWieferich :
    ¬ ∀ p, (p ∣ 2 ^ (p - 1) - 1) ↔ IsWieferich p := by
  intro h
  exact not_wieferich_3 ((h 3).mp (by norm_num))

/-- Register of rigorously established facts about Wieferich primes (base 2). -/
def wieferichFacts : List (String × String) :=
  [ ("definition", "p is Wieferich iff p is prime and 2^(p-1) = 1 (mod p^2)"),
    ("instance_1093", "1093 is a Wieferich prime (kernel-checked by decide)"),
    ("instance_3511", "3511 is a Wieferich prime (kernel-checked by decide)"),
    ("order2", "Wieferich iff p^2 divides 2^(p-1) - 1: the resolvent's second-order zero"),
    ("fermat", "for prime p != 2, p divides 2^(p-1) - 1 (Fermat: the resolvent is an integer)"),
    ("quotient", "Wieferich iff p divides the Fermat quotient (2^(p-1) - 1)/p"),
    ("quotient_1093", "1093 divides (2^1092 - 1)/1093"),
    ("quotient_3511", "3511 divides (2^3510 - 1)/3511"),
    ("crease_analogy", "a Wieferich prime is the arithmetic crease of the Fermat resolvent (cf. Crease)"),
    ("open", "infinitude of Wieferich primes is OPEN (heuristic ~ log log x; abc implies finitely many)") ]

theorem wieferichFacts_length : wieferichFacts.length = 10 := by decide

end PunoCalculus.Wieferich
