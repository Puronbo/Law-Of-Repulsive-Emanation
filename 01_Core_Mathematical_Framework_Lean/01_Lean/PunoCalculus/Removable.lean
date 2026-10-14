import Mathlib

/-!
# The removable-value mechanism (the field-agnostic "0/0 = physical value")

The framework's most replicated claim is that a "0/0 at a special point" is
removable and its value is the physical value there.  This file formalises the
*mechanism* behind that claim as a plain continuity statement:

* `removable_limit`   - if `g` is continuous at `x₀`, then
    `(x - x₀) * g x / (x - x₀)` tends to `g x₀` near `x₀` (on the punctured
    neighbourhood, where the denominator is genuinely nonzero).
* `quadratic_removable` - the canonical instance `(x² - a²)/(x - a) -> 2a`.
    This is exactly the `(omega - omega₀)`-style cancellation used for the
    impedance/resonance systems of `universal_impedance.py`.
* `impedance_crosszero` - the mechanical oscillator resonance identity
    `m omega₀ - k / omega₀ = 0` for `omega₀ = sqrt (k / m)`, i.e. the real
    part of the impedance stays `c` while the imaginary part crosses zero
    (System 1, `q1`, `removable_is_c`).

Scope is scrupulously bounded: `removable_limit` is a theorem about a *limit on
the punctured neighbourhood*, so it never claims the quotient has a value AT the
point.  The framework's own distinction between a removable 0/0 and a genuine
pole (e.g. the Ising specific-heat divergence, which is a pole, NOT a 0/0;
see `universal_impedance.py` System 3 `key_difference`) is therefore preserved:
removal is a statement about `Tendsto`, not about evaluation at a point.
-/

noncomputable section

namespace PunoCalculus.Removable

open Filter
open scoped Topology

/-- On the punctured neighbourhood the quotient `(x - x₀) * g x / (x - x₀)`
equals `g x`: this is the cancellation that makes the singularity removable. -/
lemma quotient_eq_of_ne (g : ℝ → ℝ) (x x₀ : ℝ) (h : x ≠ x₀) :
    (x - x₀) * g x / (x - x₀) = g x := by
  have hx : x - x₀ ≠ 0 := sub_ne_zero.mpr h
  field_simp [hx]

/-- `removable_limit`: a "0/0" whose denominator shares a linear factor with the
numerator has, on the punctured neighbourhood, the limit `g x₀` of the residue.
This is the machine-checked content of the framework's removable-value claim. -/
theorem removable_limit (g : ℝ → ℝ) (x₀ : ℝ) (hg : ContinuousAt g x₀) :
    Tendsto (fun x : ℝ => (x - x₀) * g x / (x - x₀)) (𝓝[≠] x₀) (𝓝 (g x₀)) := by
  have heq : (fun x : ℝ => (x - x₀) * g x / (x - x₀)) =ᶠ[𝓝[≠] x₀] g := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    exact quotient_eq_of_ne g x x₀ hx
  have hg' : Tendsto g (𝓝[≠] x₀) (𝓝 (g x₀)) :=
    hg.mono_left nhdsWithin_le_nhds
  exact Tendsto.congr' heq.symm hg'

/-- The canonical removable singularity: `(x² - a²)/(x - a) -> 2 a`.
This is the `(omega - omega₀)`-style cancellation `(omega² - omega₀²) = (omega - omega₀)(omega + omega₀)` used across the impedance systems. -/
theorem quadratic_removable (a : ℝ) :
    Tendsto (fun x : ℝ => (x ^ 2 - a ^ 2) / (x - a)) (𝓝[≠] a) (𝓝 (2 * a)) := by
  have hfac : (fun x : ℝ => (x - a) * (x + a) / (x - a)) =
      fun x : ℝ => (x ^ 2 - a ^ 2) / (x - a) := by
    funext x
    ring
  rw [← hfac]
  have hg : ContinuousAt (fun x : ℝ => x + a) a :=
    (continuous_id.add continuous_const).continuousAt
  simpa [two_mul] using removable_limit (fun x : ℝ => x + a) a hg

/-- For the mechanical oscillator `Z(omega) = c + i (m omega - k/omega)` at
resonance `omega₀ = sqrt (k/m)` (with `k, m > 0`), the imaginary part crosses
zero: `m omega₀ - k / omega₀ = 0`.  This is `universal_impedance.py` System 1,
where `im m * omega - k / omega` vanishes at `w0 = sqrt(k/m)` and the real part
remains the removable value `c`. -/
theorem impedance_crosszero (k m : ℝ) (hk : 0 < k) (hm : 0 < m)
    (w0 : ℝ) (hw0 : w0 = Real.sqrt (k / m)) :
    m * w0 - k / w0 = 0 := by
  rw [hw0]
  let r : ℝ := Real.sqrt (k / m)
  have hr : r ≠ 0 := (Real.sqrt_pos.mpr (div_pos hk hm)).ne'
  have hsq : r ^ 2 = k / m := Real.sq_sqrt (le_of_lt (div_pos hk hm))
  have hmul : m * r ^ 2 = k := by
    rw [hsq]
    field_simp [hm.ne']
  have hkr : k / r = m * r := by
    rw [← hmul]
    field_simp [hr]
  calc
    m * r - k / r = m * r - m * r := by rw [hkr]
    _ = 0 := by ring

end PunoCalculus.Removable