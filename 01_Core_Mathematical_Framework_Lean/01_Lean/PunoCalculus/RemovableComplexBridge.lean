import Mathlib
import PunoCalculus.RemovableValue

/-!
# Riemann's removable singularity, read through the register's 0/0 schema

`PunoCalculus.RemovableValue` states the register's 0/0 doctrine for real functions:
a punctured limit, when it exists, is unique (`removable_value_unique`), and the
canonical quotient `(x-a)*g(x)/(x-a)` has a removable value
(`removable_exists_unique`).  That brick is deliberately *object-specific*: it
proves the `∃!` schema, not that any given 0/0 actually has a limit.

This brick anchors that schema to a genuine theorem.  Mathlib proves **Riemann's
removable singularity theorem**
(`Complex.tendsto_limUnder_of_differentiable_on_punctured_nhds_of_bounded_under`):
a function complex-differentiable and bounded on a punctured neighbourhood of `c`
has a punctured limit.  Reading that theorem through the register's predicate
recovers the full `∃!` schema over `ℂ`:

* `IsRemovableValueAt f c L` -- the complex removable-value predicate
  `Tendsto f (𝓝[≠] c) (𝓝 L)`, the `ℂ` twin of `RemovableValue.IsRemovableValue`;
* `removable_value_exists` -- **existence**, in register form: a bounded holomorphic
  0/0 has a removable value, namely `limUnder (𝓝[≠] c) f`;
* `removable_value_unique` -- **uniqueness** (the target `ℂ` is Hausdorff);
* `exists_unique_removable_value` -- the register's `∃!` schema over `ℂ`, exactly the
  shape of `RemovableValue.removable_exists_unique`;
* `limUnder_eq_of_isRemovableValue` -- the **coincidence**: mathlib's `limUnder` is
  *the* removable value -- it equals every punctured limit;
* `canonical_zero_over_zero` -- the concrete 0/0 `(z-c)*g(z)/(z-c)` has removable
  value `g c`, the `ℂ` twin of `RemovableValue.removable_exists_unique`.

Scope bounded as everywhere: existence is a `Tendsto` on the punctured neighbourhood
(never a value AT the point), and this is a mathematical bridge between the
register's schema and a named theorem, not a claim about any Millennium problem.
-/

noncomputable section

namespace PunoCalculus.RemovableComplexBridge

open Filter
open scoped Topology

/-- `L` is the **complex removable value** of `f` at the puncture `c`: the `0/0`
resolves to `L`, i.e. `f` has the punctured limit `L`.  The `ℂ` twin of
`RemovableValue.IsRemovableValue`. -/
def IsRemovableValueAt (f : ℂ → ℂ) (c L : ℂ) : Prop :=
  Tendsto f (𝓝[≠] c) (𝓝 L)

/-- **Existence (Riemann's removable singularity theorem, in register form).** A
function complex-differentiable on a punctured neighbourhood of `c` and bounded
there has a removable value, namely `limUnder (𝓝[≠] c) f`. -/
theorem removable_value_exists (f : ℂ → ℂ) (c : ℂ)
    (hd : ∀ᶠ z in 𝓝[≠] c, DifferentiableAt ℂ f z)
    (hb : IsBoundedUnder (· ≤ ·) (𝓝[≠] c) fun z => ‖f z - f c‖) :
    IsRemovableValueAt f c (limUnder (𝓝[≠] c) f) :=
  Complex.tendsto_limUnder_of_differentiable_on_punctured_nhds_of_bounded_under hd hb

/-- **Uniqueness half.** A punctured limit, when it exists, is unique -- the `ℂ`
twin of `RemovableValue.removable_value_unique`. -/
theorem removable_value_unique {f : ℂ → ℂ} {c L₁ L₂ : ℂ}
    (h₁ : IsRemovableValueAt f c L₁) (h₂ : IsRemovableValueAt f c L₂) : L₁ = L₂ :=
  tendsto_nhds_unique h₁ h₂

/-- **The register's `∃!` schema over `ℂ`.** A bounded holomorphic 0/0 has *exactly
one* removable value -- existence plus uniqueness, the identical shape of
`RemovableValue.removable_exists_unique`. -/
theorem exists_unique_removable_value (f : ℂ → ℂ) (c : ℂ)
    (hd : ∀ᶠ z in 𝓝[≠] c, DifferentiableAt ℂ f z)
    (hb : IsBoundedUnder (· ≤ ·) (𝓝[≠] c) fun z => ‖f z - f c‖) :
    ∃! L, IsRemovableValueAt f c L :=
  ⟨limUnder (𝓝[≠] c) f, removable_value_exists f c hd hb,
    fun _L hL => removable_value_unique hL (removable_value_exists f c hd hb)⟩

/-- **Coincidence.** Mathlib's removable value is *the* removable value: the
`limUnder` produced by Riemann's theorem equals any punctured limit `L`. -/
theorem limUnder_eq_of_isRemovableValue {f : ℂ → ℂ} {c L : ℂ}
    (hd : ∀ᶠ z in 𝓝[≠] c, DifferentiableAt ℂ f z)
    (hb : IsBoundedUnder (· ≤ ·) (𝓝[≠] c) fun z => ‖f z - f c‖)
    (hL : IsRemovableValueAt f c L) : limUnder (𝓝[≠] c) f = L :=
  removable_value_unique (removable_value_exists f c hd hb) hL

/-- **The canonical 0/0 resolves to `g c`.** The concrete quotient
`(z-c)*g(z)/(z-c)` with `g` continuous at `c` has the removable value `g c` -- the
`ℂ` twin of `RemovableValue.removable_exists_unique`. -/
theorem canonical_zero_over_zero (g : ℂ → ℂ) (c : ℂ) (hg : ContinuousAt g c) :
    IsRemovableValueAt (fun z : ℂ => (z - c) * g z / (z - c)) c (g c) := by
  have h_eq : (fun z : ℂ => (z - c) * g z / (z - c)) =ᶠ[𝓝[≠] c] g := by
    filter_upwards [self_mem_nhdsWithin] with z hz
    exact mul_div_cancel_left₀ (g z) (sub_ne_zero.mpr hz)
  exact (tendsto_congr' h_eq).mpr (hg.mono_left nhdsWithin_le_nhds)

/-- Formalised-facts register for `RemovableComplexBridge.lean`. -/
def removableComplexBridgeFacts : List String :=
  [ "IsRemovableValueAt", "removable_value_exists", "removable_value_unique",
    "exists_unique_removable_value", "limUnder_eq_of_isRemovableValue",
    "canonical_zero_over_zero" ]

/-- The register has exactly six entries. -/
theorem removableComplexBridgeFacts_length : removableComplexBridgeFacts.length = 6 := by
  decide

end PunoCalculus.RemovableComplexBridge
