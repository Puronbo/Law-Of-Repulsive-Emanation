import Mathlib
import PunoCalculus.RemovableValue

/-!
# C19 -- the **Probe** mechanism: the identity 0/0 resolves to `1`

`THE_0_OVER_0_ATLAS.md` classifies removable `0/0` forms into five mechanisms; the
first is the **Probe**: two functions that *vanish identically together* (`f =ᶠ g`)
so that their ratio is `1` wherever it is defined, and the `0/0` resolves to `1`.
(The register's largest removable-value class, "identity / `f = g`".)

This brick gives the Probe a formal face:

* `ProbeValue f g x₀ c`: the ratio `f/g` has punctured limit `c` at `x₀`.
* `probe_identity`: if `f =ᶠ g` off `x₀` and `g ≠ 0` off `x₀`, the ratio resolves
  to `1` -- the identity `0/0` has removable value `1`.
* `probe_self`: `f / f` resolves to `1` wherever `f` is nonzero off the point.
* `probe_value_unique`: the probe value, when it exists, is unique.
* `probe_is_removable`: the probe value is literally an `IsRemovableValue`.

Scope as everywhere: a `Tendsto` on the punctured neighbourhood, never a value AT
the point; a mathematical schema, not a claim about any Millennium problem.
-/

noncomputable section

namespace PunoCalculus.ZeroProbe

open Filter
open scoped Topology

/-- The **probe value** of the `0/0` `f/g` at `x₀`: the punctured limit of the
ratio `f/g`.  This is the Probe mechanism's invariant. -/
def ProbeValue (f g : ℝ → ℝ) (x₀ c : ℝ) : Prop :=
  Tendsto (fun x : ℝ => f x / g x) (𝓝[≠] x₀) (𝓝 c)

/-- **The probe resolves to `1`.**  If the two functions agree on the punctured
neighbourhood (`f =ᶠ g`) and the denominator is nonzero there, the `0/0` `f/g`
resolves to `1`.  This is the identity probe -- the register's "removable value
`1`" class (`f/g = 1` where defined). -/
theorem probe_identity {f g : ℝ → ℝ} {x₀ : ℝ}
    (h : f =ᶠ[𝓝[≠] x₀] g) (hg : ∀ᶠ x in 𝓝[≠] x₀, g x ≠ 0) :
    ProbeValue f g x₀ 1 := by
  have heq : (fun x : ℝ => f x / g x) =ᶠ[𝓝[≠] x₀] (fun _ => 1) := by
    filter_upwards [h, hg] with x hx hgx
    rw [hx, div_self hgx]
  exact Tendsto.congr' heq.symm tendsto_const_nhds

/-- **`f/f` probes to `1`.**  The canonical self-probe: wherever `f` is nonzero off
the point, the `0/0` `f/f` resolves to `1`. -/
theorem probe_self (f : ℝ → ℝ) {x₀ : ℝ} (hf : ∀ᶠ x in 𝓝[≠] x₀, f x ≠ 0) :
    ProbeValue f f x₀ 1 :=
  probe_identity (by filter_upwards with x; rfl) hf

/-- **The probe value is unique.**  A punctured limit, when it exists, is unique
(the target `ℝ` is Hausdorff).  This is the same uniqueness schema as
`RemovableValue.removable_value_unique`. -/
theorem probe_value_unique {f g : ℝ → ℝ} {x₀ c d : ℝ}
    (hc : ProbeValue f g x₀ c) (hd : ProbeValue f g x₀ d) : c = d :=
  tendsto_nhds_unique hc hd

/-- **The probe value is a removable value.**  The Probe mechanism's invariant is
literally the register's `IsRemovableValue` predicate applied to the ratio. -/
theorem probe_is_removable {f g : ℝ → ℝ} {x₀ : ℝ}
    (h : f =ᶠ[𝓝[≠] x₀] g) (hg : ∀ᶠ x in 𝓝[≠] x₀, g x ≠ 0) :
    RemovableValue.IsRemovableValue (fun x : ℝ => f x / g x) x₀ 1 :=
  probe_identity h hg

/-- Formalised-facts register for `ZeroProbe.lean`. -/
def zeroProbeFacts : List String :=
  [ "ProbeValue", "probe_identity", "probe_self", "probe_value_unique",
    "probe_is_removable" ]

/-- The register has exactly five entries. -/
theorem zeroProbeFacts_length : zeroProbeFacts.length = 5 := by decide

end PunoCalculus.ZeroProbe
