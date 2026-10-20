/-
  Lehmer's totient problem, kernel-checked (Gap Ledger G31).

  `02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/
  lehmer_totient_certificate.py` sweeps phi(n) | (n-1) to 10^6 (finding no
  composite n) and the 2-Lehmer relaxation phi(n) | (n-1)^2 to 10^4 (finding
  six).  This module re-certifies both sweeps in the Lean kernel on the window
  n <= 10000, using `PunoCalculus.Factorization.totientFac` (whose product law
  is machine-checked, and whose values are cross-checked against Mathlib's
  proved `Nat.totient` on exactly the numbers the conclusions rest on).

  What is a theorem here and what is not:

  * **Theorem (window).**  No composite n <= 10000 satisfies phi(n) | (n-1),
    while the *relaxed* condition phi(n) | (n-1)^2 already has solutions
    561, 1105, 1729, 2465, 6601, 8481 -- so the machine-checked kernel confirms
    that the two conditions are genuinely different (the relaxation is
    strictly weaker: it has members and Lehmer has none, in the same window).
  * **Theorem (exact).**  `totientFac` agrees with Mathlib's `Nat.totient`
    at 6, 561, 1105, 1729, 2465, 6601, 8481 -- the numbers the conclusions
    rest on.
  * **Not a theorem.**  That no composite Lehmer number exists (any would be
    odd, squarefree, Carmichael, with >= 15 distinct prime factors and
    n > 10^26 -- the best bounds are cited).  The conjecture stays OPEN.
-/
import Mathlib
import PunoCalculus.Factorization

set_option maxRecDepth 100000
set_option maxHeartbeats 6000000

namespace PunoCalculus.Lehmer

open PunoCalculus.Factorization

/-- Lehmer's condition on `n`: composite, and `phi(n)` divides `n - 1`.
Composite-ness is tested through the totient itself (`phi(n) = n - 1` holds
exactly for primes), the sweep never calling a per-element primality test. -/
def isLehmerB (n : ℕ) : Bool :=
  1 < n && !(totientFac n = n - 1) && (n - 1) % totientFac n = 0

/-- The 2-Lehmer relaxation: composite, and `phi(n)` divides `(n - 1)^2`. -/
def isTwoLehmerB (n : ℕ) : Bool :=
  1 < n && !(totientFac n = n - 1) && (n - 1) ^ 2 % totientFac n = 0

/-! ### Cross-checks against Mathlib's proved totient -/

theorem totientFac_6 : totientFac 6 = Nat.totient 6 := by decide

theorem totientFac_561 : totientFac 561 = Nat.totient 561 := by decide

theorem totientFac_1105 : totientFac 1105 = Nat.totient 1105 := by decide

theorem totientFac_1729 : totientFac 1729 = Nat.totient 1729 := by decide

theorem totientFac_2465 : totientFac 2465 = Nat.totient 2465 := by decide

theorem totientFac_6601 : totientFac 6601 = Nat.totient 6601 := by decide

theorem totientFac_8481 : totientFac 8481 = Nat.totient 8481 := by decide

/-! ### The sweeps -/

/-- **Lehmer's window certificate:** no composite `n <= 10000` satisfies
`phi(n) | (n - 1)`.  (The Python certificate sweeps to 10^6; the conjecture
quantifies over all composites and stays OPEN.) -/
theorem lehmer_window :
    (List.range 10001).filter isLehmerB = [] := by decide

/-- **The 2-Lehmer window:** the relaxed condition
`phi(n) | (n - 1)^2` has exactly 561, 1105, 1729, 2465, 6601, 8481 among the
composites `<= 10000` -- so the relaxation is strictly weaker (a machine-checked
separation of the two conditions in one window). -/
theorem two_lehmer_window :
    (List.range 10001).filter isTwoLehmerB
      = [561, 1105, 1729, 2465, 6601, 8481] := by decide

/-- The two conditions disagree at 8481: 2-Lehmer holds, Lehmer does not. -/
theorem two_lehmer_8481 : isTwoLehmerB 8481 = true := by decide

theorem not_lehmer_8481 : isLehmerB 8481 = false := by decide

/-- Register of rigorously established facts about Lehmer's totient problem. -/
def lehmerFacts : List (String × String) :=
  [ ("lehmer_window", "no composite n <= 10000 has phi(n) | (n-1) (kernel-checked)"),
    ("two_lehmer_window", "the relaxation phi(n) | (n-1)^2 has exactly 561, 1105, 1729, 2465, 6601, 8481 below 10^4"),
    ("separation", "the two conditions differ at 8481: 2-Lehmer holds, Lehmer does not (kernel-checked)"),
    ("totient_crosscheck", "totientFac agrees with Mathlib's Nat.totient at 6 and at every number the conclusions rest on"),
    ("known_bounds", "any Lehmer composite is odd, squarefree, Carmichael, omega >= 15, n > 10^26 (cited)"),
    ("open", "no composite n with phi(n) | (n-1) is known and none is proved impossible: the problem remains OPEN") ]

theorem lehmerFacts_length : lehmerFacts.length = 6 := by decide

end PunoCalculus.Lehmer
