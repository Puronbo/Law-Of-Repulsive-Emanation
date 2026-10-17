import Mathlib
import PunoCalculus.InformationPhi
import PunoCalculus.EmergentTime
import PunoCalculus.OrientationLaw

/-!
# Information time: the orientation is a rate, the count is time

`InformationPhi.lean` constructs the register-to-thermodynamics map `Phi` on a
relaxation and proves the claim's three clauses for the bit.  Read the *other*
way -- the way `EmergentTime.lean` (card C13) reads it -- the same object is a
**time evolution**, not a thermometer.

* The register's time is the count `n` and nothing else
  (`EmergentTime.state_determined_by_count`): a change is a transfer, and elapsed
  time is the number of steps.
* The orientation `orientation r = log r` is the **per-step rate** (a Lyapunov
  exponent), i.e. an inverse time.  So the orientation trinity
  `{-1, 0, +1}` is only the *sign of a rate* -- the arrow of time: contraction =
  decay (`r < 1`), center = stationary (`r = 1`), expansion = growth (`r > 1`).
* `Phi`'s free-energy ratio is then the **one-step propagator** `e ^ (-rate)` of a
  relaxation of rate `lambda n = log n` (`Phi_freeRatio_eq_evolution`), and the
  orientation is minus the rate (`Phi_entropyProd_eq_neg_rate`).

The brick makes this precise and machine-checked:

* `evolution rate t = exp (-(rate * t))` is a genuine one-parameter time flow: it
  fixes the initial time (`evolution_zero`), is a semigroup (`evolution_add`), and
  its value at count `n` is the `n`-fold iterate of its one-step map
  (`evolution_pow_nat`) -- the register's "time is the count".
* `orientation_evolution_one` -- the orientation of the one-step retention is
  `-rate`, the negative rate; `retention_lt_one_iff` / `orientation_arrow` -- the
  decay / stationary / growth arrow is exactly the sign of `-rate`.
* `Phi_freeRatio_eq_evolution`, `Phi_entropyProd_eq_neg_rate` -- `Phi` is the
  one-step evolution and the rate of this flow.
* `orbit_eq_evolution` -- the register's geometric orbit at count `n`
  (`A * r ^ n`) is the time-`n` evolution with rate `-orientation r`, the
  multiplicative analogue of `EmergentTime.transfer_iterate`.

What this establishes is only the *shape* of `Phi` as a time/rate datum (already
determined by the register).  It does **not** identify a measured apparatus, and
the Landauer cost stays the cited physical input -- the falsifiable residue of the
OPEN claim (`LANDAUER_BOUND_AND_THE_REGISTER.md`).  No Millennium problem is
touched.
-/

noncomputable section

namespace PunoCalculus.InformationTime

open PunoCalculus.OrientationLaw (orientation)
open PunoCalculus.InformationPhi (Phi lambda)

/-- The one-parameter time flow: content relaxing at rate `rate` retains
`exp (-(rate * t))` at time `t`. -/
def evolution (rate t : ℝ) : ℝ := Real.exp (-(rate * t))

/-- The flow fixes the initial time: nothing has relaxed at `t = 0`. -/
theorem evolution_zero (rate : ℝ) : evolution rate 0 = 1 := by
  simp [evolution]

/-- The flow is a semigroup: evolving for `s + t` is evolving for `s`, then `t`. -/
theorem evolution_add (rate s t : ℝ) :
    evolution rate (s + t) = evolution rate s * evolution rate t := by
  unfold evolution
  have h : -(rate * (s + t)) = -(rate * s) + -(rate * t) := by ring
  rw [h, Real.exp_add]

/-- The one-step retention `exp (-rate)`. -/
theorem evolution_one (rate : ℝ) : evolution rate 1 = Real.exp (-rate) := by
  simp [evolution]

/-- **Orientation is minus the rate.**  The orientation of the one-step retention
`e ^ (-rate)` is exactly `-rate`. -/
theorem orientation_evolution_one (rate : ℝ) :
    orientation (evolution rate 1) = -rate := by
  unfold evolution orientation
  rw [mul_one, Real.log_exp]

/-- **The count is time.**  The value of the flow at count `n` is the `n`-fold
iterate of the one-step map -- the multiplicative analogue of
`EmergentTime.state_determined_by_count`. -/
theorem evolution_pow_nat (rate : ℝ) (n : ℕ) :
    (evolution rate 1) ^ n = evolution rate (n : ℝ) := by
  induction n with
  | zero => simp [evolution]
  | succ k ih =>
    rw [pow_succ, ih, ← evolution_add, Nat.cast_succ]

/-- **The arrow of time.**  A positive rate decays the content (`e ^ (-rate) < 1`);
a nonpositive rate does not. -/
theorem retention_lt_one_iff (rate : ℝ) :
    evolution rate 1 < 1 ↔ 0 < rate := by
  rw [evolution_one, Real.exp_lt_one_iff]
  constructor <;> intro h <;> linarith

/-- **The orientation trinity is the time arrow.**  The sign of the orientation is
the sign of `-rate`: negative = decay (`rate > 0`), zero = stationary
(`rate = 0`), positive = growth (`rate < 0`).  This is the `{-1, 0, +1}`
classification, read as a direction in time. -/
theorem orientation_arrow (rate : ℝ) :
    (orientation (evolution rate 1) < 0 ↔ 0 < rate) ∧
    (orientation (evolution rate 1) = 0 ↔ rate = 0) ∧
    (0 < orientation (evolution rate 1) ↔ rate < 0) := by
  rw [orientation_evolution_one]
  refine ⟨?_, ?_, ?_⟩ <;> constructor <;> intro h <;> linarith

/-- **The one-step retention is `r`.**  For rate `-orientation r`, the one-step
flow is exactly `r`. -/
theorem evolution_orientation_one (r : ℝ) (hr : 0 < r) :
    evolution (-orientation r) 1 = r := by
  unfold evolution orientation
  rw [mul_one, neg_neg, Real.exp_log hr]

/-- **`Phi`'s free-energy ratio is the one-step evolution.**  For the `n`-state
register this is the propagator `e ^ (-(lambda n))` of a relaxation of rate
`lambda n = log n`. -/
theorem Phi_freeRatio_eq_evolution (kB T : ℝ) (n : ℕ) (hn : 0 < n) :
    (Phi kB T n).freeRatio = evolution (lambda n) 1 := by
  rw [PunoCalculus.InformationPhi.Phi_freeRatio_eq_exp_neg_lambda kB T n hn]
  simp [evolution]

/-- **Orientation is minus the rate, for `Phi`.**  `Phi`'s entropy-production
reading is `-lambda n`, the negative of the register's rate. -/
theorem Phi_entropyProd_eq_neg_rate (kB T : ℝ) (n : ℕ) :
    (Phi kB T n).entropyProd = -lambda n := by
  simp only [PunoCalculus.InformationPhi.Phi_entropyProd_eq_orientation, lambda,
    PunoCalculus.InformationPhi.orientation_one_div]

/-- **The geometric orbit is the time flow.**  The register's orbit at count `n`
(`A * r ^ n`) equals the time-`n` evolution with rate `-orientation r` -- the
count *is* time. -/
theorem orbit_eq_evolution (A r : ℝ) (n : ℕ) (hr : 0 < r) :
    A * r ^ n = A * evolution (-orientation r) (n : ℝ) := by
  rw [← evolution_pow_nat, evolution_orientation_one r hr]

/-- Formalised-facts register for `InformationTime.lean`. -/
def informationTimeFacts : List String :=
  [ "evolution_zero", "evolution_add", "orientation_evolution_one",
    "evolution_pow_nat", "retention_lt_one_iff", "orientation_arrow",
    "Phi_freeRatio_eq_evolution", "Phi_entropyProd_eq_neg_rate",
    "orbit_eq_evolution" ]

/-- The register has exactly nine entries. -/
theorem informationTimeFacts_length : informationTimeFacts.length = 9 := by decide

end PunoCalculus.InformationTime
