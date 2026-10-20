/-
  Giuga's conjecture, kernel-checked (Gap Ledger G30).

  `02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/
  giuga_certificate.py` enumerates Giuga numbers to 10^5 and tests each against
  Korselt's criterion, finding no number that is both Giuga and Carmichael.
  This module re-certifies the same statements in the Lean kernel on the window
  n < 10000, standing on `PunoCalculus.Factorization` (whose product law is
  machine-checked on exactly this window).

  What is a theorem here and what is not:

  * **Theorem (window).**  The Giuga numbers below 10^4 are exactly
    30, 858, 1722; the Carmichael numbers below 10^4 are exactly
    561, 1105, 1729, 2465, 2821, 6601, 8911 (Korselt's criterion as a
    predicate); and no n below 10^4 is both -- i.e. **no counterexample to
    Giuga's conjecture exists in the window**, kernel-checked.
  * **Theorem (exact).**  66198 (the fourth known Giuga number, outside the
    window) is Giuga; 30, 858, 1722 are Giuga; 1729 is Carmichael but *not*
    Giuga, so the two families are visibly independent.
  * **Reviewed, not proved.**  `primeFacGo`'s output elements being prime
    (see `Factorization.lean`); the equivalence of the factor-based Giuga
    predicate with the sum `sum_{k=1}^{n-1} k^{n-1} = -1 (mod n)` form.
  * **Not a theorem.**  That no counterexample exists at all (Borwein-
    Maitland-Skerritt: any counterexample needs >= 19908 digits), the
    infinitude of Giuga numbers, or the existence of an odd Giuga number.
    All stay OPEN.
-/
import Mathlib
import PunoCalculus.Factorization

set_option maxRecDepth 100000
set_option maxHeartbeats 6000000

namespace PunoCalculus.Giuga

open PunoCalculus.Factorization

/-- A Giuga number: composite `n` with at least two distinct prime factors,
squarefree, and `p | (n/p - 1)` for every prime `p | n`.  (The two-factor
condition plus squarefree *is* the composite condition: a prime has one
factor.) -/
def isGiugaB (n : ℕ) : Bool :=
  let ps := primeFacGo n n 2
  1 < n && (2 ≤ ps.length) && (ps.length = ps.eraseDups.length)
    && (ps.all fun p => (n / p - 1) % p = 0)

/-- A Carmichael number: squarefree, at least three prime factors, and
`(p - 1) | (n - 1)` for every prime `p | n` -- Korselt's criterion, exactly. -/
def isCarmichaelB (n : ℕ) : Bool :=
  let ps := primeFacGo n n 2
  1 < n && (3 ≤ ps.length) && (ps.length = ps.eraseDups.length)
    && (ps.all fun p => (n - 1) % (p - 1) = 0)

/-! ### Exact instances -/

theorem giuga_30 : isGiugaB 30 = true := by decide

theorem giuga_858 : isGiugaB 858 = true := by decide

theorem giuga_1722 : isGiugaB 1722 = true := by decide

/-- The fourth known Giuga number, 2 * 3 * 11 * 17 * 59 -- beyond the window,
certified as an exact instance. -/
theorem giuga_66198 : isGiugaB 66198 = true := by decide

theorem carmichael_561 : isCarmichaelB 561 = true := by decide

/-- 1729 = 7 * 13 * 19 satisfies Korselt (6, 12, 18 all divide 1728) -- and
NOT the Giuga condition, so the two families are visibly independent. -/
theorem carmichael_1729 : isCarmichaelB 1729 = true := by decide

theorem not_giuga_1729 : isGiugaB 1729 = false := by decide

theorem not_carmichael_30 : isCarmichaelB 30 = false := by decide

/-! ### The window -/

/-- The Giuga numbers below 10000 are exactly 30, 858, 1722 (the Python
certificate sweeps to 10^5). -/
theorem giuga_window :
    (List.range 10000).filter isGiugaB = [30, 858, 1722] := by decide

/-- The Carmichael numbers below 10000 are exactly
561, 1105, 1729, 2465, 2821, 6601, 8911 (Korselt's criterion, evaluated). -/
theorem carmichael_window :
    (List.range 10000).filter isCarmichaelB
      = [561, 1105, 1729, 2465, 2821, 6601, 8911] := by decide

/-- **The certificate's core claim:** no `n < 10000` is both a Giuga number and
a Carmichael number, so Giuga's conjecture has no counterexample in the
window.  The conjecture itself stays OPEN. -/
theorem no_giuga_carmichael_window :
    (List.range 10000).filter (fun n => isGiugaB n && isCarmichaelB n) = [] := by
  decide

/-- Register of rigorously established facts about Giuga's conjecture. -/
def giugaFacts : List (String × String) :=
  [ ("criterion", "Giuga: composite, squarefree, p | n/p - 1 for every prime p | n; Korselt: squarefree, (p-1) | (n-1)"),
    ("giuga_window", "Giuga numbers below 10^4 are exactly 30, 858, 1722 (kernel-checked)"),
    ("giuga_66198", "66198 is Giuga (kernel-checked, outside the window)"),
    ("carmichael_window", "Carmichael numbers below 10^4 are exactly 561, 1105, 1729, 2465, 2821, 6601, 8911"),
    ("counterexample_window", "no n below 10^4 is both Giuga and Carmichael (kernel-checked)"),
    ("factorization", "factor lists product-reproduce every n below 10^4 (Factorization.lean window)"),
    ("open", "Giuga's conjecture (no composite is both Giuga and Carmichael) remains OPEN; a counterexample needs >= 19908 digits") ]

theorem giugaFacts_length : giugaFacts.length = 7 := by decide

end PunoCalculus.Giuga
