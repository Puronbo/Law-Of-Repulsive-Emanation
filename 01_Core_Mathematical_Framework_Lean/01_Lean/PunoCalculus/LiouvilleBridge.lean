import Mathlib
import PunoCalculus.RemovableComplexBridge

noncomputable section

namespace PunoCalculus.LiouvilleBridge

open Filter Function
open scoped Topology

/-- **Liouville's theorem** (register form): a function complex-differentiable on all of `C`
whose range is bounded is a constant -- the *global* dual of card C23's *local* resolution.
There local boundedness lets a `0/0` resolve to a finite value; here global boundedness is
coercive. -/
theorem bounded_entire_const (f : ℂ → ℂ) (hf : Differentiable ℂ f)
    (hb : Bornology.IsBounded (Set.range f)) : ∃ c, f = Function.const ℂ c :=
  hf.exists_eq_const_of_bounded hb

/-- A bounded entire function takes the same value at any two points. -/
theorem bounded_entire_apply_eq (f : ℂ → ℂ) (hf : Differentiable ℂ f)
    (hb : Bornology.IsBounded (Set.range f)) (z w : ℂ) : f z = f w :=
  hf.apply_eq_apply_of_bounded hb z w

/-- A bounded entire function takes at most one value: no two points differ. -/
theorem bounded_entire_value_unique (f : ℂ → ℂ) (hf : Differentiable ℂ f)
    (hb : Bornology.IsBounded (Set.range f)) : ¬ ∃ z w, f z ≠ f w := by
  rintro ⟨z, w, hzw⟩
  exact hzw (bounded_entire_apply_eq f hf hb z w)

/-- **The global `0/0` collapses.** A bounded entire function that vanishes at the origin is
identically zero -- global boundedness forces the register's `0/0` to `0`. -/
theorem eq_zero_of_bounded_of_eq_zero (f : ℂ → ℂ) (hf : Differentiable ℂ f)
    (hb : Bornology.IsBounded (Set.range f)) (h0 : f 0 = 0) : f = 0 := by
  obtain ⟨c, hc⟩ := bounded_entire_const f hf hb
  have hc0 : c = 0 := by simpa [hc] using h0
  rw [hc, hc0]
  funext z
  rfl

/-- **Bounded at infinity implies constant.** An entire function that tends to a finite value
`c` at infinity (i.e. along `cocompact C`) is the constant `c`. -/
theorem bounded_at_infinity_const (f : ℂ → ℂ) (hf : Differentiable ℂ f) {c : ℂ}
    (hb : Tendsto f (cocompact ℂ) (𝓝 c)) : f = Function.const ℂ c :=
  hf.eq_const_of_tendsto_cocompact hb

/-- Formalised-facts register for `LiouvilleBridge.lean`. -/
def liouvilleBridgeFacts : List String :=
  [ "bounded_entire_const", "bounded_entire_apply_eq", "bounded_entire_value_unique",
    "eq_zero_of_bounded_of_eq_zero", "bounded_at_infinity_const" ]

/-- The register has exactly five entries. -/
theorem liouvilleBridgeFacts_length : liouvilleBridgeFacts.length = 5 := by
  decide

end PunoCalculus.LiouvilleBridge