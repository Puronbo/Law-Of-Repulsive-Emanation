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
* `orientation_sign_iff`, `orientation_arrow_is_causal` -- the sign of the
  orientation is the register's *cause-and-effect* datum: the trinity classifies the
  base (`r < 1`, `r = 1`, `1 < r`), and increasing the count by one moves the orbit
  in the direction that sign fixes (contraction = decrease, center = stationary,
  expansion = increase).

What this establishes is only the *shape* of `Phi` as a time/rate datum (already
determined by the register).  It does **not** identify a measured apparatus, and
the Landauer cost stays the cited physical input -- the falsifiable residue of the
OPEN claim (`LANDAUER_BOUND_AND_THE_REGISTER.md`).  No Millennium problem is
touched.
-/

noncomputable section

namespace PunoCalculus.InformationTime

open PunoCalculus.OrientationLaw (orientation geometricOrbit)
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

/-- **The orientation trinity, in terms of the base `r`.**  For a positive base the
sign of the orientation `log r` classifies the orbit directly: negative =
contraction (`r < 1`), zero = center (`r = 1`), positive = expansion (`1 < r`). -/
theorem orientation_sign_iff (r : ℝ) (hr : 0 < r) :
    (orientation r < 0 ↔ r < 1) ∧
    (orientation r = 0 ↔ r = 1) ∧
    (0 < orientation r ↔ 1 < r) := by
  refine ⟨?_, ?_, ?_⟩
  · constructor
    · intro h
      have h' : Real.log r < Real.log 1 := by rw [Real.log_one]; exact h
      exact (Real.log_lt_log_iff hr zero_lt_one).mp h'
    · intro h
      have h' : Real.log r < Real.log 1 := (Real.log_lt_log_iff hr zero_lt_one).mpr h
      rwa [Real.log_one] at h'
  · constructor
    · intro h
      have h' : Real.exp (orientation r) = Real.exp 0 := by rw [h, Real.exp_zero]
      rwa [orientation, Real.exp_log hr, Real.exp_zero] at h'
    · intro h
      rw [h, orientation, Real.log_one]
  · constructor
    · intro h
      have h' : Real.log 1 < Real.log r := by rw [Real.log_one]; exact h
      exact (Real.log_lt_log_iff zero_lt_one hr).mp h'
    · intro h
      have h' : Real.log 1 < Real.log r := (Real.log_lt_log_iff zero_lt_one hr).mpr h
      rwa [Real.log_one] at h'

/-- **The orientation sign is the causal arrow (cause -> effect).**  Stepping the
count from `n` to `n + 1` -- a cause and its immediate effect -- moves the orbit in
the direction fixed by `sign (orientation r)`: contraction (`orientation r < 0`) is
monotone decrease, center (`= 0`) is stationary, expansion (`> 0`) is monotone
increase.  Hence `sign (orientation r)` is the register's ordered *before -> after*
datum, i.e. its causal arrow. -/
theorem orientation_arrow_is_causal {r A : ℝ} (hr : 0 < r) (hA : 0 < A) :
    (0 < orientation r → ∀ n, geometricOrbit r A n < geometricOrbit r A (n + 1)) ∧
    (orientation r = 0 → ∀ n, geometricOrbit r A (n + 1) = geometricOrbit r A n) ∧
    (orientation r < 0 → ∀ n, geometricOrbit r A (n + 1) < geometricOrbit r A n) := by
  obtain ⟨hlt, heq, hgt⟩ := orientation_sign_iff r hr
  have hpow : ∀ n : ℕ, 0 < r ^ n := fun n => pow_pos hr n
  refine ⟨?_, ?_, ?_⟩
  · intro hpos n
    have hr1 : 1 < r := hgt.mp hpos
    have : r ^ n < r ^ n * r := by nlinarith [hpow n, hr1]
    calc geometricOrbit r A n = r ^ n * A := by rw [geometricOrbit]
      _ < (r ^ n * r) * A := mul_lt_mul_of_pos_right this hA
      _ = geometricOrbit r A (n + 1) := by rw [geometricOrbit, pow_succ]
  · intro hzero n
    have hr1 : r = 1 := heq.mp hzero
    rw [geometricOrbit, geometricOrbit, hr1, one_pow, one_pow]
  · intro hneg n
    have hr1 : r < 1 := hlt.mp hneg
    have : r ^ n * r < r ^ n := by nlinarith [hpow n, hr1]
    calc geometricOrbit r A (n + 1) = r ^ n * r * A := by rw [geometricOrbit, pow_succ]
      _ < r ^ n * A := mul_lt_mul_of_pos_right this hA
      _ = geometricOrbit r A n := by rw [geometricOrbit]

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
    "orientation_sign_iff", "orientation_arrow_is_causal",
    "Phi_freeRatio_eq_evolution", "Phi_entropyProd_eq_neg_rate",
    "orbit_eq_evolution" ]

/-- The register has exactly eleven entries. -/
theorem informationTimeFacts_length : informationTimeFacts.length = 11 := by decide

end PunoCalculus.InformationTime
