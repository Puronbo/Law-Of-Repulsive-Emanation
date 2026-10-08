import Mathlib

/-!
# The 0/0 doctrine: the log branch and the full removable-0/0 family

Every statement is formalised in the `PunoCalculus.Removable` idiom: a
`Tendsto` on the punctured (or one-sided) neighbourhood, never evaluating AT
the singular point.

* The entropy term, `shannon_entropy_0_over_0.py`:
  * `entropy_removable_value`   - `0 * log 0 = 0` (the value the extended
      Shannon/Boltzmann term takes at `p = 0`).
  * `entropy_term_continuous`   - `p ↦ p * log p` is continuous everywhere.
  * `entropy_removable_zero`    - `p * log p -> 0` on the punctured
      neighbourhood of `0`; the removable value equals the point value.
  * `entropy_sum_zero_outcome`  - a zero-probability outcome contributes `0`.
* The log branch, `log_limits_0_over_0.py` gate 1:
  * `log_one_add_div_tendsto_one`  - `log (1 + x) / x -> 1` (real).
  * `clog_one_add_div_tendsto_one` - the same over the complex slit plane.
* The full canonical removable-0/0 family, `zero_zero_family_0_over_0.py`:
  * `kl_zero_zero_tendsto_zero`       - `p * log (p / q) -> 0` as `p -> 0+`
      with `q > 0` fixed (the KL 0/0 term).
  * `sin_x_div_tendsto_one`           - `sin x / x -> 1`.
  * `exp_sub_one_div_tendsto_one`     - `(exp x - 1) / x -> 1`.
  * `one_sub_cos_div_sq_tendsto_half` - `(1 - cos x) / x ^ 2 -> 1/2`.
  * `tan_x_div_tendsto_one`           - `tan x / x -> 1`.
  * `arcsin_x_div_tendsto_one`        - `arcsin x / x -> 1`.
  * `log_div_sub_one_tendsto_one`     - `log x / (x - 1) -> 1` as `x -> 1`.
  * `sub_one_div_log_tendsto_one`     - `(x - 1) / log x -> 1` as `x -> 1`,
      the reciprocal (the log-branch "PNT-flavoured" 0/0).
  * `self_pow_tendsto_one`            - `x ^ x -> 1` as `x -> 0+`.
  * `one_add_x_rpow_inv_tendsto_e`    - `(1 + x) ^ (1 / x) -> e`.
  * `csin_x_div_tendsto_one`          - `sin z / z -> 1` over the complex
      plane.

Scope is bounded exactly as `PunoCalculus.Removable`: no quotient is claimed
to have a value AT the singular point; the point values used inside the slope
proofs (`sin 0 = 0`, `cos 0 = 1`, `log 1 = 0`, `exp 0 = 1`, `0 * log 0 = 0`)
are mathlib's own conventions.  The ∞/∞ case is NOT conflated with 0/0 here
-- see the ledger note against the `prime_number_theorem_0_over_0.py` label.
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

/-! ## The removable 0/0 family (`zero_zero_family_0_over_0.py`) -/

/-- `p * log (p / q) -> 0` as `p -> 0+`, with `q > 0` fixed: the KL-divergence
`0 * log (0 / q)` term is removable with value `0`.  The whole right side
tends to `0` because `p * log p -> 0` (`entropy_removable_zero`) and the
`- p * log q` correction is linear. -/
theorem kl_zero_zero_tendsto_zero {q : ℝ} (hq : 0 < q) :
    Tendsto (fun p : ℝ => p * Real.log (p / q)) (nhdsWithin 0 (Set.Ioi 0)) (𝓝 0) := by
  let L : Filter ℝ := nhdsWithin 0 (Set.Ioi 0)
  have hp : Tendsto (fun p : ℝ => p) L (𝓝 0) := by
    exact tendsto_id.mono_left (nhdsWithin_le_nhds : nhdsWithin (0 : ℝ) (Set.Ioi 0) ≤ 𝓝 (0 : ℝ))
  have hp_log : Tendsto (fun p : ℝ => p * Real.log p) L (𝓝 0) := by
    exact entropy_removable_zero.mono_left
      (nhdsWithin_mono (0 : ℝ) (by intro p hp; exact ne_of_gt hp : Set.Ioi (0 : ℝ) ⊆ ({0} : Set ℝ)ᶜ))
  have hq_const : Tendsto (fun p : ℝ => p * Real.log q) L (𝓝 0) := by
    simpa [mul_comm] using hp.mul_const (Real.log q)
  have hdiff : Tendsto (fun p : ℝ => p * Real.log p - p * Real.log q) L (𝓝 0) := by
    simpa using hp_log.sub hq_const
  have heq : (fun p : ℝ => p * Real.log (p / q)) =ᶠ[L]
      (fun p : ℝ => p * Real.log p - p * Real.log q) := by
    filter_upwards [eventually_mem_nhdsWithin] with p hp
    have hdiv : Real.log (p / q) = Real.log p - Real.log q :=
      Real.log_div (ne_of_gt hp) (ne_of_gt hq)
    simp [hdiv, mul_sub]
  exact Tendsto.congr' heq.symm hdiff

/-- `sin x / x -> 1` as `x -> 0` on the punctured neighbourhood: the 0/0
removed at `sin 0 / 0`, via the slope of `sin` at `0` (`cos 0 = 1`). -/
theorem sin_x_div_tendsto_one :
    Tendsto (fun x : ℝ => Real.sin x / x) (𝓝[≠] 0) (𝓝 1) := by
  let g : ℝ → ℝ := Real.sin
  have hg : HasDerivAt g (Real.cos 0) 0 := by
    simpa [g] using Real.hasDerivAt_sin (0 : ℝ)
  have hslope : Tendsto (fun y : ℝ => slope g 0 y) (𝓝[≠] 0) (𝓝 (Real.cos 0)) :=
    hg.tendsto_slope
  have hslope1 : Tendsto (fun y : ℝ => slope g 0 y) (𝓝[≠] 0) (𝓝 1) := by
    simpa using hslope
  have heq : (fun x : ℝ => Real.sin x / x) =ᶠ[𝓝[≠] 0] (fun y : ℝ => slope g 0 y) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    simp [slope, g, div_eq_mul_inv, mul_comm, Real.sin_zero]
  exact Tendsto.congr' heq.symm hslope1

/-- `(exp x - 1) / x -> 1` as `x -> 0`: the exponential 0/0 removed via the
slope of `exp` at `0` (`exp 0 = 1`). -/
theorem exp_sub_one_div_tendsto_one :
    Tendsto (fun x : ℝ => (Real.exp x - 1) / x) (𝓝[≠] 0) (𝓝 1) := by
  let g : ℝ → ℝ := Real.exp
  have hg : HasDerivAt g (Real.exp 0) 0 := by
    simpa [g] using Real.hasDerivAt_exp (0 : ℝ)
  have hslope : Tendsto (fun y : ℝ => slope g 0 y) (𝓝[≠] 0) (𝓝 (Real.exp 0)) :=
    hg.tendsto_slope
  have hslope1 : Tendsto (fun y : ℝ => slope g 0 y) (𝓝[≠] 0) (𝓝 1) := by
    simpa using hslope
  have heq : (fun x : ℝ => (Real.exp x - 1) / x) =ᶠ[𝓝[≠] 0]
      (fun y : ℝ => slope g 0 y) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    simp [slope, g, div_eq_mul_inv, mul_comm, Real.exp_zero]
  exact Tendsto.congr' heq.symm hslope1

/-- `(1 - cos x) / x ^ 2 -> 1/2` as `x -> 0`: the second-order 0/0 removed by
the double-angle identity `1 - cos x = 2 sin (x / 2) ^ 2`, converting to the
squared `sin x / x` limit. -/
theorem one_sub_cos_div_sq_tendsto_half :
    Tendsto (fun x : ℝ => (1 - Real.cos x) / x ^ 2) (𝓝[≠] 0) (𝓝 (1 / 2 : ℝ)) := by
  have hhalf : Tendsto (fun x : ℝ => x / 2) (𝓝[≠] 0) (𝓝[≠] 0) := by
    rw [tendsto_nhdsWithin_iff]
    constructor
    · have ht : Tendsto (fun x : ℝ => x / 2) (𝓝 (0 : ℝ)) (𝓝 0) := by
        simpa [div_eq_mul_inv, mul_comm, mul_assoc] using
          ((tendsto_id : Tendsto (fun x : ℝ => x) (𝓝 (0 : ℝ)) (𝓝 (0 : ℝ))).mul_const (2 : ℝ)⁻¹)
      simpa using ht.mono_left (nhdsWithin_le_nhds : nhdsWithin (0 : ℝ) ({0} : Set ℝ)ᶜ ≤ 𝓝 (0 : ℝ))
    · filter_upwards [eventually_mem_nhdsWithin] with x hx
      exact div_ne_zero hx (by norm_num : (2 : ℝ) ≠ 0)
  have hsin : Tendsto (fun x : ℝ => Real.sin (x / 2) / (x / 2)) (𝓝[≠] 0) (𝓝 1) :=
    sin_x_div_tendsto_one.comp hhalf
  have hsin2 : Tendsto (fun x : ℝ => (Real.sin (x / 2) / (x / 2)) ^ 2) (𝓝[≠] 0) (𝓝 1) := by
    simpa using hsin.pow 2
  have hmul : Tendsto (fun x : ℝ => (1 / 2 : ℝ) * (Real.sin (x / 2) / (x / 2)) ^ 2)
      (𝓝[≠] 0) (𝓝 (1 / 2 : ℝ)) := by
    simpa using (tendsto_const_nhds.mul hsin2)
  have hid (x : ℝ) (hx : x ≠ 0) :
      (1 - Real.cos x) / x ^ 2 = (1 / 2 : ℝ) * (Real.sin (x / 2) / (x / 2)) ^ 2 := by
    have hdouble : 1 - Real.cos x = 2 * Real.sin (x / 2) ^ 2 := by
      have htw : Real.cos x = Real.cos (x / 2) ^ 2 - Real.sin (x / 2) ^ 2 := by
        have hh : Real.cos (2 * (x / 2)) = Real.cos (x / 2) ^ 2 - Real.sin (x / 2) ^ 2 :=
          Real.cos_two_mul' (x / 2)
        convert hh using 1
        ring_nf
      rw [htw]
      have hsub : Real.cos (x / 2) ^ 2 = 1 - Real.sin (x / 2) ^ 2 := by
        linarith [Real.sin_sq_add_cos_sq (x / 2)]
      rw [hsub]
      ring_nf
    calc
      (1 - Real.cos x) / x ^ 2 = (2 * Real.sin (x / 2) ^ 2) / x ^ 2 := by rw [hdouble]
      _ = (1 / 2 : ℝ) * (Real.sin (x / 2) / (x / 2)) ^ 2 := by
        have hx2 : x ^ 2 ≠ 0 := pow_ne_zero 2 hx
        have hhalfnz : x / 2 ≠ 0 := div_ne_zero hx (by norm_num : (2 : ℝ) ≠ 0)
        field_simp [hx2, hhalfnz]
  have heq : (fun x : ℝ => (1 - Real.cos x) / x ^ 2) =ᶠ[𝓝[≠] 0]
      (fun x : ℝ => (1 / 2 : ℝ) * (Real.sin (x / 2) / (x / 2)) ^ 2) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    exact hid x hx
  exact Tendsto.congr' heq.symm hmul

/-- `tan x / x -> 1` as `x -> 0`: the tangent 0/0 removed by
`tan x = sin x / cos x` together with `cos x -> 1 ≠ 0`. -/
theorem tan_x_div_tendsto_one :
    Tendsto (fun x : ℝ => Real.tan x / x) (𝓝[≠] 0) (𝓝 1) := by
  have hcos : Tendsto (fun x : ℝ => Real.cos x) (𝓝[≠] 0) (𝓝 (Real.cos 0)) := by
    exact (Real.continuous_cos.tendsto (0 : ℝ)).mono_left
      (nhdsWithin_le_nhds : nhdsWithin (0 : ℝ) ({0} : Set ℝ)ᶜ ≤ 𝓝 (0 : ℝ))
  have hcos0 : Real.cos 0 = 1 := by simp
  have hcinv : Tendsto (fun x : ℝ => (Real.cos x)⁻¹) (𝓝[≠] 0) (𝓝 ((Real.cos 0)⁻¹)) :=
    hcos.inv₀ (by simp [hcos0])
  have hcinv1 : Tendsto (fun x : ℝ => (Real.cos x)⁻¹) (𝓝[≠] 0) (𝓝 1) := by
    simpa [hcos0] using hcinv
  have hmul : Tendsto (fun x : ℝ => (Real.sin x / x) * (Real.cos x)⁻¹) (𝓝[≠] 0) (𝓝 1) := by
    simpa using sin_x_div_tendsto_one.mul hcinv1
  have heq : (fun x : ℝ => Real.tan x / x) =ᶠ[𝓝[≠] 0]
      (fun x : ℝ => (Real.sin x / x) * (Real.cos x)⁻¹) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    rw [Real.tan_eq_sin_div_cos]
    ring_nf
  exact Tendsto.congr' heq.symm hmul

/-- `log x / (x - 1) -> 1` as `x -> 1`: the log-flavoured 0/0 at `1`, via the
slope of `log` at `1` (derivative `1/1 = 1`). -/
theorem log_div_sub_one_tendsto_one :
    Tendsto (fun x : ℝ => Real.log x / (x - 1)) (𝓝[≠] 1) (𝓝 1) := by
  let g : ℝ → ℝ := Real.log
  have hg : HasDerivAt g (1 : ℝ) 1 := by
    simpa [g] using Real.hasDerivAt_log (by norm_num : (1 : ℝ) ≠ 0)
  have hslope : Tendsto (fun y : ℝ => slope g 1 y) (𝓝[≠] 1) (𝓝 1) :=
    hg.tendsto_slope
  have heq : (fun x : ℝ => Real.log x / (x - 1)) =ᶠ[𝓝[≠] 1]
      (fun y : ℝ => slope g 1 y) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    simp [slope, g, div_eq_mul_inv, mul_comm, Real.log_one]
  exact Tendsto.congr' heq.symm hslope

/-- `(x - 1) / log x -> 1` as `x -> 1`: the reciprocal of the previous limit,
the log-branch "PNT-flavoured" 0/0 whose location was deferred in the
roadmap's `Log 0/0 micro-lemma` lane.  `(a / b)⁻¹ = b / a` (mathlib's total
field inverse) makes it a corollary of `log_div_sub_one_tendsto_one`. -/
theorem sub_one_div_log_tendsto_one :
    Tendsto (fun x : ℝ => (x - 1) / Real.log x) (𝓝[≠] 1) (𝓝 1) := by
  have h : Tendsto (fun x : ℝ => Real.log x / (x - 1)) (𝓝[≠] 1) (𝓝 1) :=
    log_div_sub_one_tendsto_one
  have hinv : Tendsto (fun x : ℝ => (Real.log x / (x - 1))⁻¹) (𝓝[≠] 1) (𝓝 1) := by
    simpa using h.inv₀ (by norm_num : (1 : ℝ) ≠ 0)
  have heq : (fun x : ℝ => (x - 1) / Real.log x) =ᶠ[𝓝[≠] 1]
      (fun x : ℝ => (Real.log x / (x - 1))⁻¹) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    rw [inv_div]
  exact Tendsto.congr' heq.symm hinv

/-- `arcsin x / x -> 1` as `x -> 0`: the inverse-trig 0/0 removed via the
slope of `arcsin` at `0` (derivative `1 / sqrt (1 - 0 ^ 2) = 1`). -/
theorem arcsin_x_div_tendsto_one :
    Tendsto (fun x : ℝ => Real.arcsin x / x) (𝓝[≠] 0) (𝓝 1) := by
  let g : ℝ → ℝ := Real.arcsin
  have hg : HasDerivAt g (1 / Real.sqrt (1 - 0 ^ 2)) 0 := by
    simpa [g] using Real.hasDerivAt_arcsin (by norm_num : (0 : ℝ) ≠ -1)
      (by norm_num : (0 : ℝ) ≠ 1)
  have hslope : Tendsto (fun y : ℝ => slope g 0 y) (𝓝[≠] 0) (𝓝 (1 / Real.sqrt (1 - 0 ^ 2))) :=
    hg.tendsto_slope
  have hslope1 : Tendsto (fun y : ℝ => slope g 0 y) (𝓝[≠] 0) (𝓝 1) := by
    simpa using hslope
  have heq : (fun x : ℝ => Real.arcsin x / x) =ᶠ[𝓝[≠] 0] (fun y : ℝ => slope g 0 y) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    simp [slope, g, div_eq_mul_inv, mul_comm, Real.arcsin_zero]
  exact Tendsto.congr' heq.symm hslope1

/-- `x ^ x -> 1` as `x -> 0+`: `x ^ x = exp (x * log x)` for `x > 0`, and the
exponent `x * log x -> 0` by `entropy_removable_zero`. -/
theorem self_pow_tendsto_one :
    Tendsto (fun x : ℝ => x ^ x) (nhdsWithin 0 (Set.Ioi 0)) (𝓝 1) := by
  let L : Filter ℝ := nhdsWithin 0 (Set.Ioi 0)
  have hlogx : Tendsto (fun x : ℝ => x * Real.log x) L (𝓝 0) := by
    exact entropy_removable_zero.mono_left
      (nhdsWithin_mono (0 : ℝ) (by intro x hx; exact ne_of_gt hx : Set.Ioi (0 : ℝ) ⊆ ({0} : Set ℝ)ᶜ))
  have hexp : Tendsto (fun x : ℝ => Real.exp (x * Real.log x)) L (𝓝 (Real.exp 0)) :=
    (Real.continuous_exp.tendsto (0 : ℝ)).comp hlogx
  have hexp1 : Tendsto (fun x : ℝ => Real.exp (x * Real.log x)) L (𝓝 1) := by
    simpa using hexp
  have heq : (fun x : ℝ => x ^ x) =ᶠ[L] (fun x : ℝ => Real.exp (x * Real.log x)) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    rw [Real.rpow_def_of_pos hx x]
    congr 1
    ring_nf
  exact Tendsto.congr' heq.symm hexp1

/-- `(1 + x) ^ (1 / x) -> e` as `x -> 0`: `(1 + x) ^ (1/x) = exp (log (1+x) / x)`
for `1 + x > 0`, and the exponent is `log (1 + x) / x -> 1`
(`log_one_add_div_tendsto_one`). -/
theorem one_add_x_rpow_inv_tendsto_e :
    Tendsto (fun x : ℝ => (1 + x) ^ (1 / x)) (𝓝[≠] 0) (𝓝 (Real.exp 1)) := by
  have hpos1 : ∀ᶠ x : ℝ in 𝓝[≠] 0, 0 < 1 + x := by
    have hpos0 : ∀ᶠ x : ℝ in 𝓝 (0 : ℝ), 0 < 1 + x := by
      have hset : (Set.Ioo (-(1 / 2 : ℝ)) (1 / 2 : ℝ)) ∈ 𝓝 (0 : ℝ) := by
        exact Ioo_mem_nhds (by norm_num) (by norm_num)
      filter_upwards [hset] with x hx
      have hfrac : (0 : ℝ) < 1 / 2 := by norm_num
      linarith [hx.1, hfrac]
    exact Eventually.filter_mono (nhdsWithin_le_nhds (a := (0 : ℝ)) (s := ({0} : Set ℝ)ᶜ)) hpos0
  have hlog : Tendsto (fun x : ℝ => Real.log (1 + x) / x) (𝓝[≠] 0) (𝓝 1) :=
    log_one_add_div_tendsto_one
  have hprod : Tendsto (fun x : ℝ => (1 / x) * Real.log (1 + x)) (𝓝[≠] 0) (𝓝 1) := by
    have heq : (fun x : ℝ => (1 / x) * Real.log (1 + x)) =ᶠ[𝓝[≠] 0]
        (fun x : ℝ => Real.log (1 + x) / x) := by
      filter_upwards [eventually_mem_nhdsWithin] with x hx
      ring_nf
    exact Tendsto.congr' heq.symm hlog
  have hexp : Tendsto (fun x : ℝ => Real.exp ((1 / x) * Real.log (1 + x))) (𝓝[≠] 0)
      (𝓝 (Real.exp 1)) :=
    (Real.continuous_exp.tendsto (1 : ℝ)).comp hprod
  have heq : (fun x : ℝ => (1 + x) ^ (1 / x)) =ᶠ[𝓝[≠] 0]
      (fun x : ℝ => Real.exp ((1 / x) * Real.log (1 + x))) := by
    filter_upwards [hpos1] with x hxpos
    rw [Real.rpow_def_of_pos hxpos (1 / x)]
    congr 1
    ring_nf
  exact Tendsto.congr' heq.symm hexp

/-- `sin z / z -> 1` as `z -> 0` over the complex plane: the complex mirror of
`sin_x_div_tendsto_one`, via the slope of `Complex.sin` at `0`
(`Complex.cos 0 = 1`). -/
theorem csin_x_div_tendsto_one :
    Tendsto (fun z : ℂ => Complex.sin z / z) (𝓝[≠] 0) (𝓝 1) := by
  let g : ℂ → ℂ := Complex.sin
  have hg : HasDerivAt g (Complex.cos 0) 0 := by
    simpa [g] using Complex.hasDerivAt_sin (0 : ℂ)
  have hslope : Tendsto (fun w : ℂ => slope g 0 w) (𝓝[≠] 0) (𝓝 (Complex.cos 0)) :=
    hg.tendsto_slope
  have hslope1 : Tendsto (fun w : ℂ => slope g 0 w) (𝓝[≠] 0) (𝓝 1) := by
    simpa using hslope
  have heq : (fun z : ℂ => Complex.sin z / z) =ᶠ[𝓝[≠] 0] (fun w : ℂ => slope g 0 w) := by
    filter_upwards [eventually_mem_nhdsWithin] with z hz
    simp [slope, g, div_eq_mul_inv, mul_comm, Complex.sin_zero]
  exact Tendsto.congr' heq.symm hslope1

end PunoCalculus.ZeroZero