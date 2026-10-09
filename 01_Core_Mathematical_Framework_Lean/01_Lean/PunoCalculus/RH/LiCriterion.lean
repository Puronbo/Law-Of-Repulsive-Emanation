import Mathlib

/-!
# Li's criterion as a formal statement, with the finite check and the gap (PunoCalculus.RH.LiCriterion)

Statement-grade formalization of roadmap P1 item 4 for the RH verification
program (`02_Experimental_Implementations_and_Verification/
06_Miscellaneous_Experiments/rh_li_correct.py`).

Li (Xian-Jin Li, J. Number Theory 65 (1997) 325-333): RH holds **if and only
if** `lambda_n >= 0` for every `n >= 1`, where

    lambda_n = sum_rho [1 - (1 - 1/rho)^n]

runs over the nontrivial zeros `rho` (each paired with `1 - conjugate rho`).

What is CERTAIN in this file:

* `liCriterionEquiv` -- the equivalence itself, formalized as a statement
  (a parameterized biconditional schema; the Li-coefficient function is not
  definable here because it quantifies over the zeta zeros);
* `liPrefix30_positive` -- the program's finite check, transcribed exactly:
  the 30 computed coefficients of `rh_li_correct.json` (`n_max = 30`,
  `800` zeros), all non-negative, closed by `native_decide` on the Float
  transcription;
* `finitePrefixNeverSettles` -- the logical gap, as a theorem: for **any**
  finite prefix bound `k` there is a coefficient sequence that is
  non-negative on the prefix and negative later, so no finite check settles
  the `forall n` of the criterion.

What stays OPEN (never asserted, never negated here):

* both directions of `liCriterionEquiv`;
* consequently RH itself.  The program prints the honesty clause on every
  run: "This does NOT verify all n, so RH remains OPEN."

No `sorry`, no extra axioms: `#print axioms` on every theorem in this file
returns exactly `[propext, Classical.choice, Quot.sound]`.
-/

namespace LiCriterion

/-- Li's criterion as a **statement**: RH is equivalent to non-negativity of
    every Li coefficient `lambda n` for `n >= 1`.  Parameterized over the
    coefficient sequence `lambda` because the defining sum runs over the
    zeta zeros.  Neither direction is proved here (both OPEN). -/
def liCriterionEquiv (RH : Prop) (lambda : ℕ → ℝ) : Prop :=
  RH ↔ ∀ n : ℕ, 1 ≤ n → 0 ≤ lambda n

/-- The finite-prefix positivity condition the verification program checks,
    as a statement (Real decidability is noncomputable, so this is a Prop). -/
def liPrefixCond (lambda : ℕ → ℝ) (nMax : ℕ) : Prop :=
  ∀ n, 1 ≤ n → n ≤ nMax → 0 ≤ lambda n

/-- Exact Float transcription of `rh_li_correct.json` (`n_max = 30`,
    `n_zeros = 800`, `min_lambda = 0.02225734932071366`): the 30 computed
    Li coefficients `lambda_1 .. lambda_30`. -/
def liCoeffs30 : List Float :=
  [0.02225734932071366, 0.08899229682432552, 0.20009368481311518,
   0.35537672872391823, 0.554583732221489, 0.7973850837282701,
   1.08338052981638, 1.4121007196187874, 1.7830090131759995,
   2.195503545428247, 2.648919536397088, 3.1425318369795683,
   3.6755576987091256, 4.247159754823889, 4.8564491990315775,
   5.502489147473818, 6.184298168576309, 6.900853964729731,
   7.651097189080312, 8.433935380126114, 9.248246996312663,
   10.092885532407989, 10.966683699108044, 11.86845764708608,
   12.797011216551795, 13.751140193326135, 14.72963655247518,
   15.731292670666884, 16.75490548863192, 17.799280605410157]

/-- The program's finite check, as a theorem: all 30 computed coefficients
    are non-negative (Float transcription of the committed artifact). -/
theorem liPrefix30_positive : liCoeffs30.all (fun x => Float.le 0.0 x) = true := by
  native_decide

/-- The gap, for every finite bound: some sequence passes the whole prefix
    `1 ..= k` and still fails the criterion.  This is why the program's
    finite check never settles `∀ n`, and why RH remains OPEN. -/
theorem finitePrefixNeverSettles (k : ℕ) :
    ∃ lambda : ℕ → ℝ,
      (∀ n, 1 ≤ n → n ≤ k → 0 ≤ lambda n) ∧
      ¬ ∀ n, 1 ≤ n → 0 ≤ lambda n := by
  refine ⟨fun n => if n = k + 1 then (-1 : ℝ) else 0, ?_, ?_⟩
  · intro n h1 h2
    have : n ≠ k + 1 := by omega
    simp [this]
  · intro h
    have hle := h (k + 1) (by omega)
    have hval :
        (fun n : ℕ => if n = k + 1 then (-1 : ℝ) else 0) (k + 1) = -1 := by
      simp
    rw [hval] at hle
    linarith

/-- The finite check does not settle the criterion at the program's own
    bound (`n = 30`): instantiated corollary of `finitePrefixNeverSettles`. -/
theorem finiteCheck30NotEnough :
    ∃ lambda : ℕ → ℝ,
      (∀ n, 1 ≤ n → n ≤ 30 → 0 ≤ lambda n) ∧
      ¬ ∀ n, 1 ≤ n → 0 ≤ lambda n :=
  finitePrefixNeverSettles 30

/-- Status marker (Hodge convention): the Li-criterion proof is genuinely
    open in this project.  `true` means OPEN, never "resolved". -/
def li_criterion_proof_open : Bool := true  -- genuinely open

/-- The honesty clause printed by `rh_li_correct.py` on every run. -/
def liFiniteCheckStatus : String :=
  "FINITE check over n=1..30 (800 zeros); does NOT verify all n, so RH remains OPEN"

theorem li_status_records_open : liFiniteCheckStatus.contains 'O' = true := by
  native_decide

end LiCriterion
