/-
  The Erdos-Moser equation, kernel-checked (Gap Ledger G34).

  `02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/
  erdos_moser_certificate.py` searches for solutions of

      1^k + 2^k + ... + (m-1)^k = m^k      (m >= 2, k >= 1)

  in a finite window and finds none beyond the known one, (m, k) = (3, 1).
  This module re-certifies that window in the Lean kernel and pins the known
  solution as an exact instance.

  What is a theorem here and what is not:

  * **Theorem (exact).**  (3, 1) *is* a solution: 1 + 2 = 3.
  * **Theorem (window).**  No pair with `4 <= m <= 80` and `1 <= k <= 12` is a
    solution (the same window the Python certificate searches).
  * **Not a theorem.**  That (3, 1) is the *only* solution.  Moser (1953)
    showed any further solution requires k even and m > 10^(10^6) (since
    improved far beyond), so no feasible search excludes all solutions -- the
    conjecture stays OPEN.
-/
import Mathlib

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

namespace PunoCalculus.ErdosMoser

/-- `powerSum m k = 1^k + 2^k + ... + m^k`, accumulated by a fold -- for
`k >= 1` the leading `0^k` in `List.range m` adds nothing, so this is the
left-hand side of the Erdos-Moser equation on `m` candidates. -/
def powerSum (m k : ℕ) : ℕ := (List.range m).foldl (fun acc j => acc + j ^ k) 0

/-- The Erdos-Moser equation on a candidate pair: does the power sum equal the
single `m^k`? -/
def isEmSol (m k : ℕ) : Bool := powerSum m k = m ^ k

/-- The same sum as Mathlib's `Finset` sum, on a concrete instance -- tying the
fold-based computation used by the scan to the library's canonical sum. -/
theorem powerSum_10_2_eq : powerSum 10 2 = ∑ j ∈ Finset.range 10, j ^ 2 := by
  decide

/-! ### The known solution -/

/-- The only known solution: `1 + 2 = 3`. -/
theorem em_solution_3_1 : isEmSol 3 1 = true := by decide

/-- A negative control: `1^2 + 2^2 + 3^2 = 14` is not `4^2 = 16`. -/
theorem not_em_4_2 : isEmSol 4 2 = false := by decide

/-! ### The window -/

/-- **The window certificate:** no solution with `4 <= m <= 80`,
`1 <= k <= 12` (the Python certificate's window).  (3, 1) is outside the
window by construction -- it is pinned above.  The conjecture that (3, 1) is
the *only* solution stays OPEN. -/
theorem em_window :
    ((List.range' 4 77).flatMap fun m =>
      (List.range' 1 12).filterMap fun k =>
        if isEmSol m k then some (m, k) else none) = [] := by decide

/-- Register of rigorously established facts about the Erdos-Moser equation. -/
def erdosMoserFacts : List (String × String) :=
  [ ("known_solution", "(3, 1) is a solution: 1 + 2 = 3 (kernel-checked)"),
    ("window", "no solution with 4 <= m <= 80 and 1 <= k <= 12 (kernel-checked)"),
    ("sum_bridge", "powerSum equals Mathlib's Finset sum on the checked instance"),
    ("moser_conditions", "any further solution has k even and m > 10^(10^6) (Moser 1953, cited)"),
    ("open", "whether (3, 1) is the only solution remains OPEN") ]

theorem erdosMoserFacts_length : erdosMoserFacts.length = 5 := by decide

end PunoCalculus.ErdosMoser
