/-
  Finite exact scanning primitives -- the kernel-side core of the register's
  finite-certificate machinery (Gap Ledger G28, and the shared base of
  `PrimeGaps`, `PerfectNumbers`, `ErdosMoser`, `Giuga`, `Lehmer`).

  The Python certificates under
  `02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/`
  sieve windows of 10^6-10^7 and record the answers in JSON.  They are honest
  and reproducible, but they are *not* proofs: no kernel ever checked them.
  This module supplies the same scans in a form the Lean kernel reduces, so
  every window below is a theorem, not a measurement.

  Design constraints discovered while building it (recorded so the next module
  does not rediscover them):

  * `decide (Nat.Prime n)` *does* reduce in the kernel -- but only up to a
    raised `maxRecDepth`.  Every scan below therefore carries
    `set_option maxRecDepth 100000 in` at its use site.
  * `Nat.sqrt` does **not** reduce in the kernel (`decide` gets stuck on it),
    so no sqrt-based predicate may appear in a scanned Boolean.  Andrica's
    `sqrt q - sqrt p < 1` is instead carried in its exact square form
    `(q - p - 1)^2 < 4p`, proved equivalent in `PunoCalculus.PrimeGaps`.
  * Every scan is a `Bool` built from `List.range`/`filter`/`any`/`all`, so a
    single `decide` discharges a whole window at once.

  Nothing here decides an infinitude claim.  Each predicate is decidable on a
  finite window and that is the entire reach of the method.
-/
import Mathlib

namespace PunoCalculus.FiniteScan

/-- Kernel-reducible primality test: the `Bool` reflection of `Nat.Prime`.
`decide (Nat.Prime n)` reduces in the kernel for the sizes used by the register. -/
def isPrimeB (n : ℕ) : Bool := decide (Nat.Prime n)

/-- The Boolean test reflects `Nat.Prime` exactly, in both directions. -/
theorem isPrimeB_eq_iff (n : ℕ) : isPrimeB n = true ↔ Nat.Prime n :=
  ⟨of_decide_eq_true, decide_eq_true⟩

/-- Every prime `<= N`, in increasing order. -/
def primesUpTo (N : ℕ) : List ℕ := (List.range (N + 1)).filter isPrimeB

@[simp] theorem primesUpTo_eq (N : ℕ) :
    primesUpTo N = (List.range (N + 1)).filter isPrimeB := rfl

/-- Every element of `primesUpTo N` really is prime, and every prime `<= N`
appears.  The two half-statements together make the scan *complete*, which is
what turns a window into a certificate about all primes in it. -/
theorem mem_primesUpTo {N p : ℕ} :
    p ∈ primesUpTo N ↔ Nat.Prime p ∧ p ≤ N := by
  rw [primesUpTo_eq, List.mem_filter, List.mem_range]
  constructor
  · rintro ⟨hlt, hp⟩
    exact ⟨(isPrimeB_eq_iff p).mp hp, Nat.lt_succ_iff.mp hlt⟩
  · rintro ⟨hp, hle⟩
    exact ⟨Nat.lt_succ_of_le hle, (isPrimeB_eq_iff p).mpr hp⟩

/-- The first `n` primes, `primesUpTo` on a bound that is known to contain them. -/
def firstPrimes (n : ℕ) : List ℕ := (primesUpTo (n * n + 10)).take n

/-- Absolute difference of two naturals -- deliberately *not* `a - b`, because
Gilbreath's table is built from absolute differences and its rows are not
monotone (`1, 2, 2, 4, 2` already has a descent, where plain `b - a`
underflows to `0`). -/
def natAbsDiff (a b : ℕ) : ℕ := if a ≤ b then b - a else a - b

/-- One absolute-difference row of Gilbreath's construction: the row that
follows `a :: b :: t` is `|b - a| :: ...`, and a singleton or the empty list
produces the empty row. -/
def absDiff : List ℕ → List ℕ
  | [] => []
  | [_] => []
  | a :: b :: t => natAbsDiff a b :: absDiff (b :: t)

/-- The difference row of a list with at least two elements is strictly shorter
than that list, so the Gilbreath iteration strictly descends (the fuel in
`gilbreathAux` is therefore always sufficient). -/
theorem length_absDiff : ∀ {a b : ℕ} {t : List ℕ},
    (absDiff (a :: b :: t)).length < (a :: b :: t).length
  | a, b, t => by
    induction t generalizing a b with
    | nil => simp [absDiff]
    | cons c t ih =>
      have h := ih (a := b) (b := c)
      simp only [absDiff, List.length_cons] at h ⊢
      omega

/-- Gilbreath's construction, driven by explicit fuel so that the kernel can
reduce it: is every iterated absolute-difference row of `row` headed by `1`? -/
def gilbreathAux : ℕ → List ℕ → Bool
  | 0, _ => true
  | _ + 1, [] => true
  | _ + 1, [_] => true
  | fuel + 1, row => (row.headD 0 = 1) && gilbreathAux fuel (absDiff row)

/-- Gilbreath's check on a list: is every *iterated absolute-difference* row
headed by `1`?  The initial prime row is not itself a difference row (its head
is the first prime, `2`), so the check starts at the first difference row.
Fuel is the length of the original list, which is more than enough by
`length_absDiff`. -/
def gilbreathHolds (row : List ℕ) : Bool := gilbreathAux row.length (absDiff row)

/-- Is there a prime strictly between `lo` and `hi`?  The scan covers exactly
`lo + 1, ..., hi`, so the window is `lo < m <= hi`. -/
def anyPrime (lo hi : ℕ) : Bool :=
  (List.range (hi - lo)).any fun i => isPrimeB (lo + 1 + i)

/-- `anyPrime` is complete on its window: it is true exactly when some prime
lies in `(lo, hi]`.  This is what makes Oppermann's interval scan a certificate. -/
theorem anyPrime_eq_iff (lo hi : ℕ) :
    anyPrime lo hi = true ↔ ∃ m, lo < m ∧ m ≤ hi ∧ Nat.Prime m := by
  rw [anyPrime, List.any_eq_true]
  constructor
  · rintro ⟨i, hrange, hp⟩
    have hi1 : i < hi - lo := List.mem_range.mp hrange
    exact ⟨lo + 1 + i, by omega, by omega,
      (isPrimeB_eq_iff (lo + 1 + i)).mp hp⟩
  · rintro ⟨m, hlo, hhi, hp⟩
    have hle : lo + 1 ≤ m := by omega
    refine ⟨m - (lo + 1), ?_, ?_⟩
    · exact List.mem_range.mpr (by omega)
    · rw [Nat.add_sub_cancel' hle]
      exact (isPrimeB_eq_iff m).mpr hp

/-- Scan a list of primes for a Boolean property of consecutive pairs
`f p q`.  Used for Andrica and Brocard. -/
def allConsecutive (ps : List ℕ) (f : ℕ → ℕ → Bool) : Bool :=
  (ps.zip ps.tail).all fun pq => f pq.1 pq.2

/-- Count the primes in `ps` satisfying a Boolean property. -/
def countIf (ps : List ℕ) (f : ℕ → Bool) : ℕ :=
  (ps.filter f).length

/-- The smallest prime in `ps` satisfying a Boolean property, or `none`. -/
def firstWhere (ps : List ℕ) (f : ℕ → Bool) : Option ℕ :=
  ps.find? f

/-- Admissible constellation test: `p` starts the pattern `pat`. -/
def startsPattern (pat : List ℕ) (p : ℕ) : Bool :=
  pat.all fun d => isPrimeB (p + d)

/-- The smallest start of the constellation `pat` among the primes `<= limit`. -/
def firstConstellation (limit : ℕ) (pat : List ℕ) : Option ℕ :=
  (primesUpTo limit).find? fun p => startsPattern pat p

end PunoCalculus.FiniteScan
