import Mathlib

/-!
# The 0/0 doctrine, at the log branch: `p * log p` and `log (1 + x) / x`

The framework's log-flavoured 0/0 claims, formalised in the
`PunoCalculus.Removable` idiom (limit on the punctured neighbourhood; never
evaluating AT the point):

* `entropy_removable_value`   - `0 * log 0 = 0` (the value the extended
    Shannon/Boltzmann entropy term takes at `p = 0`, matching
    `shannon_entropy_0_over_0.py` gate 1).
* `entropy_removable_zero`    - `p * log p -> 0` on the punctured
    neighbourhood of `0`: the "0/0 is removable" statement for the entropy
    term.  The whole function `p ↦ p * log p` is actually continuous
    (`entropy_term_continuous`), so the removed value equals the point value.
* `entropy_sum_zero_outcome`  - a zero-probability outcome contributes `0`
    to the finite Shannon sum, exactly the convention the Python gates use
    (`shannon_entropy_0_over_0.py: for p = 0 the term is 0`).
* `log_one_add_div_tendsto_one`    - `log (1 + x) / x -> 1` at `x = 0`
    (real): `log_limits_0_over_0.py` gate 1, "0/0, removable = 1".
* `clog_one_add_div_tendsto_one`   - the same limit over the complex slit
    plane (`Complex.log (1 + z) / z -> 1`), where `z ↦ 1 + z` never leaves
    `slitPlane` near `z = 0` since `1 ∈ slitPlane`.

Scope is bounded exactly as `PunoCalculus.Removable`: every statement is a
`Tendsto` on the punctured neighbourhood, so no quotient is claimed to have a
value AT the singular point; the point value `log 1 = 0` / `0 * log 0 = 0`
used in the slopes is mathlib's own convention.  The ∞/∞ case is NOT
conflated with 0/0 here -- see the ledger note against the
`prime_number_theorem_0_over_0.py` label.
-/

noncomputable section

namespace PunoCalculus.ZeroZero

open Filter
open scoped Topology

/-- The value of the entropy term at `p = 0` under mathlib's `log 0 = 0`
convention: `0 * log 0 = 0`.  This is the "removed value" the extended
Shannon term takes, per `shannon_entropy_0_over_0.py`. -/
theorem entropy_removable_value : (fun t : ℝ => t * Real.log t) 0 = 0 := by
  simp [Real.log_zero]

/-- The entropy term `p * log p` is continuous everywhere (value 0 at 0):
the 0/0 at `p = 0` is removable, and the removal does not change the value. -/
theorem entropy_term_continuous : Continuous (fun t : ℝ => t * Real.log t) :=
  Real.continuous_mul_log

/-- `p * log p -> 0` on the punctured neighbourhood of `0`: the framework's
"0/0 at p = 0, removable value 0" claim, kept in `The Universal Zero` and
`The Law of Singularities` and exercised by `shannon_entropy_0_over_0.py`. -/
theorem entropy_removable_zero :
    Tendsto (fun t : ℝ => t * Real.log t) (𝓝[≠] 0) (𝓝 0) := by
  have hc := entropy_term_continuous
  have h0 : Tendsto (fun t : ℝ => t * Real.log t) (𝓝[≠] 0) (𝓝 (0 * Real.log 0)) := by
    exact hc.continuousAt.mono_left nhdsWithin_le_nhds
  exact h0.mono_right (le_of_eq (by simp [Real.log_zero]))

/-- A zero-probability outcome contributes exactly `0` to the finite Shannon
sum: the extended-entropy convention used by the Python gates. -/
theorem entropy_sum_zero_outcome {ι : Type*} (p : ι → ℝ) (j : ι)
    (hpj : p j = 0) : p j * Real.log (p j) = 0 := by
  simp [hpj]

/-- `log (1 + x) / x -> 1` at `x = 0`: the "0/0, removable = 1" gate of
`log_limits_0_over_0.py`, following `log (1 + x)` being differentiable at `0`
with derivative `1`. -/
theorem log_one_add_div_tendsto_one :
    Tendsto (fun x : ℝ => Real.log (1 + x) / x) (𝓝[≠] 0) (𝓝 1) := by
  let g : ℝ → ℝ := fun y => Real.log (1 + y)
  have hg : HasDerivAt g (1 : ℝ) 0 := by
    have hlog : HasDerivAt (fun y : ℝ => Real.log (1 + y)) 1 0 := by
      have hlin : HasDerivAt (fun y : ℝ => 1 + y) 1 0 := by
        simpa using (hasDerivAt_id (0 : ℝ)).const_add (1 : ℝ)
      simpa using hlin.log (by norm_num : (1 + (0 : ℝ)) ≠ 0)
    simpa [g] using hlog
  have hslope : Tendsto (fun x : ℝ => slope g 0 x) (𝓝[≠] 0) (𝓝 1) := by
    simpa [g] using hg.tendsto_slope
  have heq : (fun x : ℝ => Real.log (1 + x) / x) =ᶠ[𝓝[≠] 0]
      (fun x : ℝ => slope g 0 x) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    simp [slope, g, sub_zero, Real.log_one, div_eq_mul_inv, mul_comm]
  exact Tendsto.congr' heq.symm hslope

/-- `Complex.log (1 + z) / z -> 1` at `z = 0` on `slitPlane`: the same 0/0
gate of `log_limits_0_over_0.py` over the complex branch, where `z ↦ 1 + z`
stays inside the branch near the point of interest (`1 ∈ slitPlane`). -/
theorem clog_one_add_div_tendsto_one :
    Tendsto (fun z : ℂ => Complex.log (1 + z) / z) (𝓝[≠] 0) (𝓝 1) := by
  let g : ℂ → ℂ := fun w => Complex.log (1 + w)
  have hg : HasDerivAt g (1 : ℂ) 0 := by
    have hlog : HasDerivAt (fun w : ℂ => Complex.log (1 + w)) 1 0 := by
      have hlin : HasDerivAt (fun w : ℂ => 1 + w) 1 0 :=
        (hasDerivAt_id (0 : ℂ)).const_add (1 : ℂ)
      have h₂ : (1 + (0 : ℂ)) ∈ Complex.slitPlane := by
        simp [Complex.slitPlane]
      simpa using hlin.clog h₂
    simpa [g] using hlog
  have hslope : Tendsto (fun z : ℂ => slope g 0 z) (𝓝[≠] 0) (𝓝 1) := by
    simpa [g] using hg.tendsto_slope
  have heq : (fun z : ℂ => Complex.log (1 + z) / z) =ᶠ[𝓝[≠] 0]
      (fun z : ℂ => slope g 0 z) := by
    filter_upwards [eventually_mem_nhdsWithin] with z hz
    simp [slope, g, sub_zero, Complex.log_one, div_eq_mul_inv, mul_comm]
  exact Tendsto.congr' heq.symm hslope

end PunoCalculus.ZeroZero