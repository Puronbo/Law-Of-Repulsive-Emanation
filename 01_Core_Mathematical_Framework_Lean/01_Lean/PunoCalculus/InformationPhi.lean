import Mathlib
import PunoCalculus.InformationBridge
import PunoCalculus.RemovableValue
import PunoCalculus.OrientationLaw

/-!
# The map `Phi`: a concrete dynamical 0/0 system carrying the Landauer cost

The note `LANDAUER_BOUND_AND_THE_REGISTER.md` states an **OPEN** claim: a map
`Phi` from register states to thermodynamic states carrying the Landauer cost.
`InformationBridge.lean` formalises the two-state arithmetic.  This brick does the
two sharper things the note asks for:

1. **It exhibits a genuine dynamical 0/0 whose removable value is the register's
   `lambda` (card C17).**  The relaxation `x |-> r ^ x` has a content deficit per
   unit time `(1 - r^x)/x`, a `0/0` at `x = 0`; its removable value is
   `-log r = -orientation r` (`deficitRate_isRemovableValue`).  For the
   state-counting register `r = 1/n` that value is `log n` -- the register's
   content (`deficitRate_stateCounting`, `orientation_one_div`).
2. **It constructs `Phi` explicitly** on this system (`Phi`) and proves the three
   clauses of the claim for the bit: the removable value maps to the free-energy
   ratio (`Phi_freeRatio_eq_exp_neg_lambda`), the orientation is the
   entropy-production reading (`Phi_entropyProd_eq_orientation`,
   `register_entropy_rate`), and the one-bit erase cost is `k_B T log 2`
   (`Phi_bit_eraseCost`, `Phi_satisfies_claim`).

What is **not** done: the Landauer bound `k_B T log 2` is a cited physical input,
not derived, and `Phi` here is the *register's own model* of a thermodynamic
state -- the step of identifying it with a measured physical system is exactly the
missing entity of the OPEN claim.  No Millennium problem is touched.
-/

noncomputable section

namespace PunoCalculus.InformationPhi

open Filter
open scoped Topology

open PunoCalculus.OrientationLaw (orientation)
open PunoCalculus.RemovableValue (IsRemovableValue)
open PunoCalculus.InformationBridge (resetCost)

/-! ## 1. The dynamical 0/0 and its removable value (card C17) -/

/-- Content deficit per unit time of the relaxation `x |-> r ^ x`: the `0/0`
`(1 - r^x)/x` at `x = 0`. -/
def deficitRate (r x : ℝ) : ℝ := (1 - r ^ x) / x

/-- **The relaxation 0/0 resolves to `-orientation r` (C17).**  As the time step
`x -> 0`, the per-unit-time content deficit `(1 - r^x)/x` tends to `-log r`. -/
theorem deficitRate_isRemovableValue (r : ℝ) (hr : 0 < r) :
    IsRemovableValue (deficitRate r) 0 (-orientation r) := by
  have hpow : HasDerivAt (fun x : ℝ => r ^ x) (Real.log r) 0 := by
    simpa [Real.rpow_zero] using (Real.hasStrictDerivAt_const_rpow hr (0 : ℝ)).hasDerivAt
  have hneg : Tendsto (fun x : ℝ => -slope (fun y : ℝ => r ^ y) 0 x)
      (𝓝[≠] 0) (𝓝 (-Real.log r)) := hpow.tendsto_slope.neg
  have heq : deficitRate r =ᶠ[𝓝[≠] 0]
      (fun x : ℝ => -slope (fun y : ℝ => r ^ y) 0 x) := by
    filter_upwards [eventually_mem_nhdsWithin] with x _hx
    simp only [deficitRate, slope, Real.rpow_zero, sub_zero, vsub_eq_sub, smul_eq_mul]
    ring
  exact Tendsto.congr' heq.symm hneg

/-- The orientation of the reciprocal: `orientation (1/n) = -log n`. -/
theorem orientation_one_div (n : ℕ) :
    orientation (1 / (n : ℝ)) = -Real.log n := by
  unfold orientation
  rw [one_div, Real.log_inv]

/-- **`lambda` for the state-counting register (C17).**  For `r = 1/n` the
removable value of the relaxation 0/0 is `log n`, the register's content. -/
theorem deficitRate_stateCounting (n : ℕ) (hn : 0 < n) :
    IsRemovableValue (deficitRate (1 / (n : ℝ))) 0 (Real.log n) := by
  have hr : (0 : ℝ) < 1 / (n : ℝ) := by positivity
  have hval : -orientation (1 / (n : ℝ)) = Real.log n := by
    rw [orientation_one_div n]; ring
  rw [← hval]
  exact deficitRate_isRemovableValue (1 / (n : ℝ)) hr

/-! ## 2. The constructed map `Phi` -/

/-- A thermodynamic state as the register's model reads it. -/
structure ThermoState where
  /-- Equilibrium free-energy ratio of the modeled system. -/
  freeRatio : ℝ
  /-- Per-step entropy-production reading. -/
  entropyProd : ℝ
  /-- Minimum work (heat) to erase the register. -/
  eraseCost : ℝ

/-- The register's removable value `lambda` (C17) for an `n`-state register. -/
def lambda (n : ℕ) : ℝ := Real.log n

/-- **The candidate register-to-thermodynamics map `Phi`** of the OPEN claim, for
the `n`-state relaxation at temperature `T`.  It carries the removable value
`lambda` (C17) to the free-energy ratio `exp (-lambda)`, the orientation to the
entropy-production reading, and `k_B T * lambda` to the erase cost. -/
def Phi (kB T : ℝ) (n : ℕ) : ThermoState :=
  { freeRatio := 1 / (n : ℝ)
    entropyProd := orientation (1 / (n : ℝ))
    eraseCost := kB * T * Real.log n }

/-- **Claim clause (1): the removable value maps to the free-energy ratio.**
`Phi`'s free-energy ratio is `exp (-lambda)`; the free energy is `k_B T lambda`. -/
theorem Phi_freeRatio_eq_exp_neg_lambda (kB T : ℝ) (n : ℕ) (hn : 0 < n) :
    (Phi kB T n).freeRatio = Real.exp (-lambda n) := by
  unfold Phi lambda
  rw [Real.exp_neg, Real.exp_log (by exact_mod_cast hn), one_div]

/-- **Claim clause (2): the orientation is the entropy-production reading.** -/
theorem Phi_entropyProd_eq_orientation (kB T : ℝ) (n : ℕ) :
    (Phi kB T n).entropyProd = orientation (1 / (n : ℝ)) := rfl

/-- **The register entropy production is the orientation (C10).**  The per-unit-time
register entropy change of the relaxation is `orientation r`, for every `x != 0`. -/
theorem register_entropy_rate {r : ℝ} (hr : 0 < r) {x : ℝ} (hx : x ≠ 0) :
    Real.log (r ^ x) / x = orientation r := by
  rw [Real.log_rpow hr x]
  unfold orientation
  field_simp [hx]

/-- `Phi`'s erase cost is `InformationBridge`'s reset cost. -/
theorem Phi_eraseCost_eq_resetCost (kB T : ℝ) (n : ℕ) :
    (Phi kB T n).eraseCost = resetCost kB T n := by
  simp [Phi, resetCost]

/-- **Claim clause (3): the bit reset costs the Landauer quantum.** -/
theorem Phi_bit_eraseCost (kB T : ℝ) :
    (Phi kB T 2).eraseCost = kB * T * Real.log 2 := by
  unfold Phi
  rfl

/-- **`Phi` satisfies the three clauses of the OPEN claim for the bit.** -/
theorem Phi_satisfies_claim (kB T : ℝ) :
    (Phi kB T 2).freeRatio = Real.exp (-lambda 2) ∧
    (Phi kB T 2).entropyProd = orientation (1 / 2) ∧
    (Phi kB T 2).eraseCost = kB * T * Real.log 2 := by
  refine ⟨?_, ?_, ?_⟩
  · exact Phi_freeRatio_eq_exp_neg_lambda kB T 2 (by norm_num)
  · rfl
  · unfold Phi; rfl

/-- Formalised-facts register for `InformationPhi.lean`. -/
def informationPhiFacts : List String :=
  [ "deficitRate_isRemovableValue", "orientation_one_div",
    "deficitRate_stateCounting", "Phi_freeRatio_eq_exp_neg_lambda",
    "register_entropy_rate", "Phi_entropyProd_eq_orientation",
    "Phi_eraseCost_eq_resetCost", "Phi_bit_eraseCost", "Phi_satisfies_claim" ]

/-- The register has exactly nine entries. -/
theorem informationPhiFacts_length : informationPhiFacts.length = 9 := by decide

end PunoCalculus.InformationPhi
