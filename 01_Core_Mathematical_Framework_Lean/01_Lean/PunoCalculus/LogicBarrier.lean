/-
  PunoCalculus.LogicBarrier

  THE METHOD BARRIER, in its abstract form (card C12).

  The register's C12 observes that the Millennium walls are METHOD barriers, not merely
  missing computations.  The cleanest such barrier is one theorem of Lawvere: a
  diagonal, self-referential construction.  In a cartesian closed setting, if a type `α`
  can SURJECT onto its own function space `α → β` (`φ` an enumeration of all predicates),
  then EVERY endomap `f : β → β` has a fixed point.  Contrapositive: an endomap with NO
  fixed point (for `β = Bool`, negation `!`) forbids any such enumeration.

  This single fact is the abstract engine of three famous walls:

    * Cantor -- `α` cannot enumerate its own predicates (`no_surjective_predicates`);
    * Turing -- the halting problem (the diagonal "does program `a` halt on `a`?" escapes
      every total decider, exactly as the diagonal predicate escapes `φ`'s range);
    * Gödel -- the diagonal lemma (a fixed point of "this sentence is unprovable"), whose
      fixed-point-free instance is the same escape.

  We prove the abstract theorem and its Corollaries.  We do NOT formalise a model of
  computation or of arithmetic, and we make NO claim about any Millennium problem:
  this is the shared SKELETON of the barriers, machine-checked.  Sources: Cantor (1891);
  Gödel (1931); Turing (1936); Lawvere, "Diagonal arguments and cartesian closed
  categories" (1969).

  Axioms: [propext, Classical.choice, Quot.sound]; the length certificate is axiom-free.

  Author: Michael Grafiel S Puno
-/

import Mathlib

namespace PunoCalculus.LogicBarrier

/-- **Lawvere's fixed-point theorem (the diagonal engine).**  If `φ : α → α → β` is
surjective -- i.e. `α` enumerates every predicate `α → β` -- then every `f : β → β` has a
fixed point.  Proof: the diagonal `g a = f (φ a a)` is some row `φ a₀` of the
enumeration, and evaluating there gives `φ a₀ a₀ = f (φ a₀ a₀)`. -/
theorem lawvere_fixedpoint {α β : Type*} (f : β → β) (φ : α → α → β)
    (hφ : Function.Surjective φ) : ∃ b : β, f b = b := by
  obtain ⟨a, ha⟩ := hφ (fun x => f (φ x x))
  exact ⟨φ a a, (congrFun ha a).symm⟩

/-- **A fixed-point-free map forbids an enumeration.**  Contrapositive of
`lawvere_fixedpoint`: if `f` has no fixed point, no surjection `α → (α → β)` exists. -/
theorem no_surjective_of_no_fixedpoint {α β : Type*} (f : β → β)
    (hf : ∀ b, f b ≠ b) (φ : α → α → β) : ¬ Function.Surjective φ :=
  fun hφ => by
    obtain ⟨b, hb⟩ := lawvere_fixedpoint f φ hφ
    exact hf b hb

/-- **Cantor's theorem, diagonal form.**  No type enumerates its own predicate space
`α → Bool`: negation has no fixed point.  (This is precisely the halting / diagonal
obstruction, made type-generic.) -/
theorem no_surjective_predicates (α : Type) :
    ¬ ∃ φ : α → α → Bool, Function.Surjective φ := by
  rintro ⟨φ, hφ⟩
  obtain ⟨b, hb⟩ := lawvere_fixedpoint (fun b : Bool => !b) φ hφ
  have hne : ∀ b : Bool, (!b) ≠ b := by decide
  exact hne b hb

/-- The diagonal predicate of an enumeration `φ`: `diag φ a = !(φ a a)`. -/
def diagonal {α : Type*} (φ : α → α → Bool) : α → Bool := fun a => !(φ a a)

/-- **The diagonal escapes every enumeration** (Cantor/Gödel/Turing, concretely).  For
any `φ`, the predicate `diag φ` is not one of `φ`'s rows. -/
theorem diagonal_not_mem_range {α : Type*} (φ : α → α → Bool) :
    diagonal φ ∉ Set.range φ := by
  rintro ⟨a, ha⟩
  have h : φ a a = diagonal φ a := congrFun ha a
  have hne : ∀ x : Bool, (!x) ≠ x := by decide
  exact hne (φ a a) h.symm

/-- Formalised-facts register for `LogicBarrier.lean`. -/
def logicBarrierFacts : List String :=
  [ "lawvere_fixedpoint", "no_surjective_of_no_fixedpoint", "no_surjective_predicates",
    "diagonal_not_mem_range" ]

/-- The register has exactly four entries. -/
theorem logicBarrierFacts_length : logicBarrierFacts.length = 4 := by decide

end PunoCalculus.LogicBarrier
