import Mathlib
import PunoCalculus.Removable
import PunoCalculus.ZeroLink

/-!
# The 0/0 / initial-arrow bridge: removability is existence + uniqueness

`PunoCalculus.Removable` proves the *existence* half of the register's 0/0
doctrine: a `0/0` with a shared linear factor has a punctured limit.  `ZeroLink`
proves the *structural* half: an initial object has, into every type, an arrow that
exists and is unique (`∃!`).  This brick shows the two are the **same schema** --
"there is exactly one" -- applied to a value in the analytic case and to an arrow
in the categorical case.

* `IsRemovableValue f a L`: the predicate "`L` is the removable value of `f` at the
  puncture `a`", i.e. `Tendsto f (𝓝[≠] a) (𝓝 L)` -- the 0/0 resolves to `L`.
* `removable_value_unique`: the **uniqueness** half -- a punctured limit, when it
  exists, is unique (the target `ℝ` is Hausdorff).  This is the analytic twin of
  `ZeroLink.empty_unique_arrow`'s uniqueness.
* `existsUnique_iff_exists_and_unique`: the **shared schema** -- `∃!` is exactly
  existence plus uniqueness, for any predicate.
* `removable_exists_unique`: the removable value of the canonical 0/0 exists AND
  is unique -- a genuine `∃!`, the same shape as the initial arrow.
* `extension_unique`: a continuous extension of a punctured map is unique -- the
  categorical "at most one arrow" in analytic form.
* `removable_value_bridge` / `initial_arrow_schema`: the same `∃!` schema applied
  to the removable value and to the initial arrow, side by side.

Scope bounded as everywhere: existence is a `Tendsto` on the punctured
neighbourhood (never a value AT the point), and this is a mathematical schema, not
a claim about any Millennium problem.
-/

noncomputable section

namespace PunoCalculus.RemovableValue

open Filter
open scoped Topology

/-- `L` is the **removable value** of `f` at the puncture `a`: the `0/0` resolves
to `L`, i.e. `f` has the punctured limit `L`. -/
def IsRemovableValue (f : ℝ → ℝ) (a L : ℝ) : Prop :=
  Tendsto f (𝓝[≠] a) (𝓝 L)

/-- **Uniqueness half.** A punctured limit, when it exists, is unique. -/
theorem removable_value_unique {f : ℝ → ℝ} {a L₁ L₂ : ℝ}
    (h₁ : IsRemovableValue f a L₁) (h₂ : IsRemovableValue f a L₂) : L₁ = L₂ :=
  tendsto_nhds_unique h₁ h₂

/-- **The shared schema.** "There is exactly one" is precisely existence plus
uniqueness, for any predicate.  This is the shape used by both the initial arrow
(`ZeroLink`) and the removable value. -/
theorem existsUnique_iff_exists_and_unique {β : Type*} (R : β → Prop) :
    (∃! b, R b) ↔ ∃ b, R b ∧ ∀ b', R b' → b' = b :=
  ⟨fun ⟨b, hb, hu⟩ => ⟨b, hb, hu⟩, fun ⟨b, hb, hu⟩ => ⟨b, hb, hu⟩⟩

/-- **A continuous extension of a punctured map is unique.** If two functions agree
on the punctured neighbourhood of `a` and are both continuous at `a`, they agree AT
`a`: there is at most one continuous extension.  This is the analytic form of
"at most one arrow" out of the initial object (`ZeroObject.initial_link`). -/
theorem extension_unique {f g : ℝ → ℝ} {a : ℝ}
    (hf : ContinuousAt f a) (hg : ContinuousAt g a) (h : f =ᶠ[𝓝[≠] a] g) :
    f a = g a :=
  tendsto_nhds_unique_of_eventuallyEq (hf.mono_left nhdsWithin_le_nhds)
    (hg.mono_left nhdsWithin_le_nhds) h

/-- **The removable 0/0 has a unique value.** The canonical quotient
`(x - a) * g x / (x - a)` with `g` continuous at `a` has a removable value, and it
is unique: a genuine `∃!`, the same shape as the initial arrow. -/
theorem removable_exists_unique (g : ℝ → ℝ) (a : ℝ) (hg : ContinuousAt g a) :
    ∃! L, IsRemovableValue (fun x : ℝ => (x - a) * g x / (x - a)) a L := by
  refine ⟨g a, Removable.removable_limit g a hg, ?_⟩
  intro L hL
  exact removable_value_unique hL (Removable.removable_limit g a hg)

/-- **The bridge.** The removable value is characterized by the shared schema:
existence plus uniqueness of a single value. -/
theorem removable_value_bridge (g : ℝ → ℝ) (a : ℝ) (hg : ContinuousAt g a) :
    ∃ L, IsRemovableValue (fun x : ℝ => (x - a) * g x / (x - a)) a L ∧
      ∀ L', IsRemovableValue (fun x : ℝ => (x - a) * g x / (x - a)) a L' → L' = L :=
  (existsUnique_iff_exists_and_unique _).mp (removable_exists_unique g a hg)

/-- **The initial arrow has the same schema.** `ZeroLink`'s initial arrow
`Empty → α` is a `∃!`; unfolding it with the shared schema gives existence plus
uniqueness, the identical shape as `removable_value_bridge`. -/
theorem initial_arrow_schema (α : Type) :
    ∃ _f : Empty → α, True ∧ ∀ _g : Empty → α, True → _g = _f :=
  (existsUnique_iff_exists_and_unique (fun _ : Empty → α => True)).mp
    (ZeroLink.empty_unique_arrow α)

/-- Formalised-facts register for `RemovableValue.lean`. -/
def removableValueFacts : List String :=
  [ "IsRemovableValue", "removable_value_unique", "existsUnique_iff_exists_and_unique",
    "extension_unique", "removable_exists_unique", "removable_value_bridge",
    "initial_arrow_schema" ]

/-- The register has exactly seven entries. -/
theorem removableValueFacts_length : removableValueFacts.length = 7 := by decide

end PunoCalculus.RemovableValue
