import Mathlib

/-!
# Beal at exponent three: a *proven* modular obstruction

Beal's conjecture (1993) asks whether `a^x + b^y = c^z` with `x, y, z > 2` has any
answer in coprime positive integers.  It is open.  A computational certificate can
only ever test a finite window (see `beal_certificate.py`, Gap Ledger G33); the point
of this module is to record the one *exact* theorem that a window scan can lean on:
a rigorous reduction that eliminates an entire residue class regardless of size.

The reduction is the classical mod-9 obstruction to Fermat's equation at exponent 3.
An integer coprime to `3` has cube `±1 (mod 9)` (a unit of `ZMod 9` has cubic residue
`±1`), and no sum of two such residues is again `±1`.  Hence

* **`three_dvd_of_cubes`** — if `A³ + B³ = C³` then `3` divides one of `A, B, C`;
  equivalently, there is **no** solution with all three bases coprime to `3`.

This is a genuine (if partial) proof-shaped fact: the Beal search for exponent `3`
may skip every triple whose three bases are units modulo `3`, and any candidate
coprime solution `a^3 + b^3 = c^3` with `3 ∤ a, b` provably has `3 ∣ c`.

The finite residue check is discharged by `decide` over the nine-element ring
`ZMod 9` (axiom-free); the lift to `ℕ` is exact.  The general Beal conjecture
remains OPEN and is not claimed here.
-/

namespace PunoCalculus.Beal

/-- A unit of `ZMod 9` has cubic residue `±1`. -/
theorem unit_cube (a : ZMod 9) (ha : IsUnit a) : a ^ 3 = 1 ∨ a ^ 3 = 8 := by
  revert a; decide

/-- **No solution modulo 9 with all three terms units.**  If `a, b, c` are all
units of `ZMod 9` then `a³ + b³ ≠ c³`: the cubes are `±1` and no such sum is `±1`. -/
theorem no_unit_cubes_solution (a b c : ZMod 9) (ha : IsUnit a) (hb : IsUnit b)
    (hc : IsUnit c) : a ^ 3 + b ^ 3 ≠ c ^ 3 := by
  revert a b c; decide

/-- An integer not divisible by `3` is a unit in `ZMod 9` (since `9 = 3²`). -/
theorem unit_of_not_dvd (n : ℕ) (h : ¬ 3 ∣ n) : IsUnit (n : ZMod 9) := by
  rw [ZMod.isUnit_iff_coprime, show (9 : ℕ) = 3 ^ 2 by norm_num,
    Nat.coprime_pow_right_iff (by norm_num)]
  exact ((Nat.Prime.coprime_iff_not_dvd (show Nat.Prime 3 by norm_num)).mpr h).symm

/-- The cubic residue criterion: a base coprime to `3` has cube `±1 (mod 9)`. -/
theorem cube_mod9 (n : ℕ) (h : ¬ 3 ∣ n) : (n : ZMod 9) ^ 3 = 1 ∨ (n : ZMod 9) ^ 3 = 8 :=
  unit_cube _ (unit_of_not_dvd n h)

/-- **The exponent-3 Beal/FLT obstruction.**  If `A³ + B³ = C³` then at least one of
`A, B, C` is divisible by `3`; equivalently there is no solution with all three bases
coprime to `3`.  This is the reduction a finite window scan rests on. -/
theorem three_dvd_of_cubes (A B C : ℕ) (h : A ^ 3 + B ^ 3 = C ^ 3) :
    3 ∣ A ∨ 3 ∣ B ∨ 3 ∣ C := by
  by_contra hc
  rw [not_or, not_or] at hc
  obtain ⟨hA, hB, hC⟩ := hc
  have hz : (A : ZMod 9) ^ 3 + (B : ZMod 9) ^ 3 = (C : ZMod 9) ^ 3 := by
    have := congrArg (fun x : ℕ => (x : ZMod 9)) h
    push_cast at this
    simpa using this
  exact no_unit_cubes_solution _ _ _ (unit_of_not_dvd A hA) (unit_of_not_dvd B hB)
    (unit_of_not_dvd C hC) hz

/-- **Corollary for coprime witnesses.**  If `3 ∤ A` and `3 ∤ B` but `A³ + B³ = C³`,
then `3 ∣ C`.  (So a Beal search may restrict `c` to multiples of `3` whenever the
two addends are coprime to `3`.) -/
theorem three_dvd_of_cubes_of_not_dvd (A B C : ℕ) (h : A ^ 3 + B ^ 3 = C ^ 3)
    (hA : ¬ 3 ∣ A) (hB : ¬ 3 ∣ B) : 3 ∣ C := by
  rcases three_dvd_of_cubes A B C h with h3 | h3 | h3
  · exact absurd h3 hA
  · exact absurd h3 hB
  · exact h3

/-- Formalised-facts register for `Beal.lean`. -/
def bealFacts : List (String × String) :=
  [ ("unit_cube", "a unit of ZMod 9 has cube 1 or 8"),
    ("no_unit_cubes_solution", "no a^3 + b^3 = c^3 in ZMod 9 with a,b,c all units"),
    ("unit_of_not_dvd", "n not divisible by 3 is a unit of ZMod 9"),
    ("cube_mod9", "a base coprime to 3 has cube +/-1 (mod 9)"),
    ("three_dvd_of_cubes", "A^3 + B^3 = C^3 (over N) forces 3 | A or 3 | B or 3 | C"),
    ("three_dvd_of_cubes_of_not_dvd", "if 3 does not divide A or B then 3 | C for A^3+B^3=C^3") ]

/-- The register has exactly six entries. -/
theorem bealFacts_length : bealFacts.length = 6 := by decide

end PunoCalculus.Beal
