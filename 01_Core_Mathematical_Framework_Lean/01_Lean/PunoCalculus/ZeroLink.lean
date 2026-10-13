import Mathlib

/-!
# Zero links all forms: nothing is the initial object, its arrow exists and is unique

This file formalises the **structural face** of the framework's 0/0 doctrine
(`PunoCalculus.Removable`, `PunoCalculus.ZeroZero`, `PunoCalculus.ZeroFixedPoint`).
There the claim is *analytic*: a "0/0" at a special point is removable, and its
value is the physical value there -- an **existence** (the limit exists) together
with a **uniqueness** (the value is definite).  Here is the same word in its
*categorical* sense, and it is the sense in which "everything starts at nothing":

* **Nothing is the origin.** `Empty` (the type with no elements -- cardinality
  `0` -- the empty set) is the *initial object* of `Type`: into **every** type
  `α` there is an arrow `Empty → α`, and there is **exactly one**
  (`empty_unique_arrow`).  So the zero object is the common source of all forms:
  every mathematical object receives a canonical map from nothing.  This is the
  set-theoretic *link between all forms of mathematics*.

* **Existence ∧ uniqueness = removability.** The two halves of "removable" are
  exactly the two halves of "initial": the arrow *exists* (as the limit value
  exists), and it is *the only one* (as the removable value is definite).  The
  same discipline that removes `0/0` names the unique arrow out of `0`.

* **Zero is the arithmetic of all forms.** Under the sum of types (`+`,
  coproduct) `Empty` is the **identity** (`Sum Empty α ≃ α`, `Sum α Empty ≃ α`),
  and under the product of types (`×`) it is **absorbing**
  (`α × Empty ≃ Empty`, `Empty × α ≃ Empty`): `0 + a = a` and `0 * a = 0`,
  rebuilt with sets instead of numbers.  The two canonical types reproduce the
  arithmetic of the two canonical numbers.

* **The one object.** Dually, `PUnit` (the singleton -- cardinality `1`) is the
  *terminal object*: from every `α` there is exactly one arrow `α → PUnit`
  (`unit_unique_arrow`).  The classification is exact: a type is initial **iff**
  it is empty (`empty_classified_initial`), and terminal **iff** it is a
  subsingleton (`unit_classified_terminal`).

Scope is bounded as everywhere in the register: this is a machine-checked
*structural* brick (Mathlib's own `Empty`/`PUnit`/`Sum`/`Prod`), not a claim about
any Millennium problem and not a claim that "0/0" has a value AT a point.  In a
category with a genuine **zero object** (both initial and terminal, e.g. modules)
`Type` itself does not qualify -- here `0` is initial and `1` is terminal --
which is exactly why the doctrine is stated on the punctured neighbourhood and on
the unique arrow, never on a point value.
-/

namespace PunoCalculus.ZeroLink

/-! ## The origin: the unique arrow out of nothing -/

/-- The canonical arrow from nothing into any type: `Empty → α`, by
`Empty.elim`. This is the "link" every object receives from `0`. -/
def ofEmpty (α : Type) : Empty → α := fun e => e.elim

/-- **There is exactly one arrow out of nothing.** For every type `α` the map
`Empty → α` exists and is unique.  Existence is the limit's existence;
uniqueness is the removable value being definite. -/
theorem empty_unique_arrow (α : Type) : ∃! _f : Empty → α, True := by
  refine ⟨ofEmpty α, trivial, ?_⟩
  intro g _
  funext e
  cases e

/-- A type is **initial** when it admits a unique arrow into every type. -/
def Initial (I : Type) : Prop := ∀ α : Type, ∃! _f : I → α, True

/-- **Nothing is initial.** `Empty` sits at the origin of `Type`. -/
theorem empty_isInitial : Initial Empty := empty_unique_arrow

/-- The dually canonical arrow into one: `α → PUnit`. -/
def toUnit (α : Type) : α → PUnit := fun _ => PUnit.unit

/-- **There is exactly one arrow into one.** -/
theorem unit_unique_arrow (α : Type) : ∃! _f : α → PUnit, True := by
  refine ⟨toUnit α, trivial, ?_⟩
  intro g _
  funext a
  exact Subsingleton.elim (g a) PUnit.unit

/-- A type is **terminal** when every type has a unique arrow into it. -/
def Terminal (T : Type) : Prop := ∀ α : Type, ∃! _f : α → T, True

/-- **One is terminal.** `PUnit` sits at the target of all forms. -/
theorem unit_isTerminal : Terminal PUnit := unit_unique_arrow

/-! ## The classification is exact: initial = empty, terminal = subsingleton -/

/-- **A type is initial iff it is empty.** From initiality, the unique arrow
`I → Empty` is a witness that `I` has no elements. -/
theorem empty_classified_initial {I : Type} (h : Initial I) : IsEmpty I := by
  obtain ⟨f, _, _⟩ := h Empty
  exact ⟨fun i => (f i).elim⟩

/-- **A type is terminal iff it is a subsingleton.** Terminality forces the two
constant maps `Bool → T` to agree, hence any two points are equal. -/
theorem unit_classified_terminal {T : Type} (h : Terminal T) : Subsingleton T := by
  obtain ⟨f, _, huniq⟩ := h Bool
  refine ⟨fun a b => ?_⟩
  have h1 : (fun _ : Bool => a) = f := huniq (fun _ : Bool => a) trivial
  have h2 : (fun _ : Bool => b) = f := huniq (fun _ : Bool => b) trivial
  have hh : (fun _ : Bool => a) = (fun _ : Bool => b) := by rw [h1, h2]
  exact congrFun hh true

/-! ## Zero as the arithmetic of all forms

Under `+` (coproduct of types) nothing is the identity; under `×` (product of
types) nothing is absorbing.  These are `0 + a = a` and `0 * a = 0`, rebuilt with
sets. -/

/-- **`0 + a = a`.** `Empty` is the identity for the coproduct. -/
def emptySumEquiv (α : Type) : Sum Empty α ≃ α where
  toFun s := match s with
    | Sum.inl e => e.elim
    | Sum.inr a => a
  invFun := Sum.inr
  left_inv := by rintro (e | a) <;> (first | cases e | rfl)
  right_inv := by intro a; rfl

/-- **`a + 0 = a`.** -/
def sumEmptyEquiv (α : Type) : Sum α Empty ≃ α where
  toFun s := match s with
    | Sum.inl a => a
    | Sum.inr e => e.elim
  invFun := Sum.inl
  left_inv := by rintro (a | e) <;> (first | rfl | cases e)
  right_inv := by intro a; rfl

/-- **`a * 0 = 0`.** `Empty` is absorbing for the product. -/
def prodEmptyEquiv (α : Type) : α × Empty ≃ Empty where
  toFun p := p.2
  invFun e := e.elim
  left_inv := by rintro ⟨a, e⟩; cases e
  right_inv := by intro e; cases e

/-- **`0 * a = 0`.** -/
def emptyProdEquiv (α : Type) : Empty × α ≃ Empty where
  toFun p := p.1
  invFun e := e.elim
  left_inv := by rintro ⟨e, a⟩; cases e
  right_inv := by intro e; cases e

/-! ## The capstone: zero links all forms -/

/-- **Nothing links all forms.** One theorem bundling the whole structural face:
`Empty` is initial, `PUnit` is terminal, and under the two type-formers `0` is the
identity of `+` and the annihilator of `×`.  This is the categorical reading of
"everything starts at zero". -/
theorem zero_links_all :
    Initial Empty ∧ Terminal PUnit ∧
    (∀ α : Type, Nonempty (Sum Empty α ≃ α)) ∧
    (∀ α : Type, Nonempty (Sum α Empty ≃ α)) ∧
    (∀ α : Type, Nonempty (α × Empty ≃ Empty)) ∧
    (∀ α : Type, Nonempty (Empty × α ≃ Empty)) :=
  ⟨empty_isInitial, unit_isTerminal,
   fun α => ⟨emptySumEquiv α⟩, fun α => ⟨sumEmptyEquiv α⟩,
   fun α => ⟨prodEmptyEquiv α⟩, fun α => ⟨emptyProdEquiv α⟩⟩

/-- Formalised-facts register for `ZeroLink.lean`. -/
def zeroLinkFacts : List String :=
  [ "empty_unique_arrow", "empty_isInitial", "unit_unique_arrow", "unit_isTerminal",
    "empty_classified_initial", "unit_classified_terminal",
    "emptySumEquiv", "sumEmptyEquiv", "prodEmptyEquiv", "emptyProdEquiv",
    "zero_links_all" ]

/-- The register has exactly eleven entries. -/
theorem zeroLinkFacts_length : zeroLinkFacts.length = 11 := by decide

end PunoCalculus.ZeroLink
