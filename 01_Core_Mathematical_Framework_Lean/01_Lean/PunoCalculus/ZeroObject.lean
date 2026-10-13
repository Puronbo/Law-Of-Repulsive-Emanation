import Mathlib

/-!
# The zero object: the one object that is both origin and target

`PunoCalculus.ZeroLink` shows that in `Type` the origin of the category (`Empty`,
initial) and its target (`PUnit`, terminal) are **two different** objects -- every
type receives a unique arrow from `Empty` and sends a unique arrow to `PUnit`, but
no single type does both.  This brick is the honest completion of that sentence:
in a category with a genuine **zero object** one object *is* both at once, and it
is exactly then that "zero completes the link between all forms".

Concretely, for a ring `R` the category `ModuleCat R` of `R`-modules has a zero
object (`ModuleCat.instHasZeroObject`): the zero module.  Relative to it *every*
module receives a unique arrow from the origin and sends a unique arrow to the
target -- the same object, both directions.  The general theorems here are stated
for an arbitrary category `C`; the module instantiation shows the link is not
vacuous.

* `initial_link` / `terminal_link`: a (co)initial object links every object by a
  **unique** arrow -- the categorical form of the removable value existing and
  being definite (`PunoCalculus.Removable`, `PunoCalculus.ZeroLink`).
* `zero_isInitial` / `zero_isTerminal`: a zero object is both at once.
* `zero_links_both_ways`: the capstone -- **one** `Z` links every `Y` in both
  directions, the statement `Type` cannot make.
* `zero_unique_up_to_iso`: the link is unique up to isomorphism.
* `modules_haveZeroObject` / `modules_exists_zeroObject` / `modules_zero_links`:
  the instantiation in `ModuleCat R`, where the zero object really exists.

Scope bounded as everywhere: this is a structural machine-checked brick over
Mathlib's own category theory, not a claim about any Millennium problem, and not a
claim that `Type` itself has a zero object (it does not -- see `ZeroLink`).
-/

namespace PunoCalculus.ZeroObject

open CategoryTheory CategoryTheory.Limits

section Abstract

variable {C : Type u} [Category.{v} C]

/-- **An initial object links every object from the source by a unique arrow.** -/
theorem initial_link {X Y : C} (h : IsInitial X) : ∃! _f : X ⟶ Y, True :=
  ⟨h.to Y, trivial, fun g _ => h.hom_ext g (h.to Y)⟩

/-- **A terminal object links every object to the target by a unique arrow.** -/
theorem terminal_link {X Y : C} (h : IsTerminal X) : ∃! _f : Y ⟶ X, True :=
  ⟨h.from Y, trivial, fun g _ => h.hom_ext g (h.from Y)⟩

/-- A **zero object** is initial. -/
noncomputable def zero_isInitial {Z : C} (h : IsZero Z) : IsInitial Z := IsZero.isInitial h

/-- A **zero object** is terminal. -/
noncomputable def zero_isTerminal {Z : C} (h : IsZero Z) : IsTerminal Z := IsZero.isTerminal h

/-- **The zero object links both ways.**  A single `Z` is the source of a unique
arrow into *every* `Y` **and** the target of a unique arrow from *every* `Y` -- the
two directions that `Type` splits between `Empty` and `PUnit`, here joined in one
object. -/
theorem zero_links_both_ways {Z : C} (h : IsZero Z) (Y : C) :
    (∃! _f : Z ⟶ Y, True) ∧ (∃! _f : Y ⟶ Z, True) :=
  ⟨initial_link (IsZero.isInitial h), terminal_link (IsZero.isTerminal h)⟩

/-- Any two zero objects are isomorphic: the link is unique up to isomorphism. -/
noncomputable def zero_unique_up_to_iso {X Y : C} (hX : IsZero X) (hY : IsZero Y) : X ≅ Y :=
  IsZero.iso hX hY

end Abstract

section Modules

variable (R : Type u) [Ring R]

/-- **`ModuleCat R` has a zero object** -- Mathlib's `ModuleCat.instHasZeroObject`. -/
theorem modules_haveZeroObject : HasZeroObject (ModuleCat R) :=
  ModuleCat.instHasZeroObject

/-- Concretely, there is an object of the module category that is at once initial
and terminal. -/
theorem modules_exists_zeroObject : ∃ Z : ModuleCat R, IsZero Z := HasZeroObject.zero

/-- **The module zero object links every module both ways.** -/
theorem modules_zero_links (Z : ModuleCat R) (h : IsZero Z) (M : ModuleCat R) :
    (∃! _f : Z ⟶ M, True) ∧ (∃! _f : M ⟶ Z, True) :=
  zero_links_both_ways h M

end Modules

/-- Formalised-facts register for `ZeroObject.lean`. -/
def zeroObjectFacts : List String :=
  [ "initial_link", "terminal_link", "zero_isInitial", "zero_isTerminal",
    "zero_links_both_ways", "zero_unique_up_to_iso",
    "modules_haveZeroObject", "modules_exists_zeroObject", "modules_zero_links" ]

/-- The register has exactly nine entries. -/
theorem zeroObjectFacts_length : zeroObjectFacts.length = 9 := by decide

end PunoCalculus.ZeroObject
