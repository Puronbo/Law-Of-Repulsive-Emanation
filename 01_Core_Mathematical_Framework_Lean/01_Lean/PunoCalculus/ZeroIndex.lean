import Mathlib

/-!
# The **multiplicity index** (the Index mechanism)

The register's 0/0 atlas isolates an **Index** mechanism: 0/0 forms whose removable
value is an *integer* -- a winding number, a multiplicity, a topological invariant.
Its algebraic face is the **multiplicity of a root**: the integer `n` with which a
factor `(X - C a)` divides a polynomial.

* `Index a p`: the multiplicity of `a` as a root of `p` (`p.rootMultiplicity a`).
* `index_additive`: **the index adds under products** --
  `index (p·q) = index p + index q` (the integer is additive, as an index is).
* `index_pow`: `index (p^n) = n · index p`.
* `index_X_sub_C_self`: a simple root has index `1`.
* `index_pow_self`: `(X - a)^n` has index exactly `n`.
* `index_canonical`: `c · (X - a)^n` with `c ≠ 0` has index `n` -- the canonical
  integer removable value.
* `index_is_multiplicity`: the capstone bundling all of the above.

This is the algebraic face of the register's Index mechanism (the topological faces
-- winding numbers, Poincaré–Hopf -- are the same integer invariant in other
categories).  Scope as everywhere: a statement about polynomials over a domain, and
no Millennium problem is touched.
-/

noncomputable section

namespace PunoCalculus.ZeroIndex

open Polynomial

variable {R : Type*} [CommRing R] [IsDomain R] [DecidableEq R]

/-- The **index** of `p` at `a`: the order of `a` as a root of `p` (its root
multiplicity).  This is the Index mechanism's integer invariant. -/
def Index (a : R) (p : R[X]) : ℕ :=
  p.rootMultiplicity a

/-- The index of the constant `1` is `0`. -/
theorem index_one (a : R) : Index a (1 : R[X]) = 0 := by
  rw [Index, ← Polynomial.C_1, Polynomial.rootMultiplicity_C]

/-- **The index law: indices add under products.** -/
theorem index_additive {p q : R[X]} (h : p * q ≠ 0) (a : R) :
    Index a (p * q) = Index a p + Index a q := by
  simp only [Index]
  exact Polynomial.rootMultiplicity_mul h

/-- **Indices scale under powers.** -/
theorem index_pow {p : R[X]} (hp : p ≠ 0) (a : R) (n : ℕ) :
    Index a (p ^ n) = n * Index a p := by
  induction n with
  | zero => rw [pow_zero, zero_mul]; exact index_one a
  | succ n ih =>
      have hne : p ^ n * p ≠ 0 := mul_ne_zero (pow_ne_zero n hp) hp
      rw [pow_succ, index_additive hne, ih, Nat.succ_mul]

/-- **A simple root has index `1`.** -/
theorem index_X_sub_C_self (a : R) : Index a (X - C a) = 1 := by
  simp [Index, Polynomial.rootMultiplicity_X_sub_C]

/-- **`(X - a)^n` has index exactly `n`.** -/
theorem index_pow_self (a : R) (n : ℕ) : Index a ((X - C a) ^ n) = n := by
  have h := Polynomial.rootMultiplicity_mul_X_sub_C_pow (p := (1 : R[X])) (a := a) (n := n)
    one_ne_zero
  have h1 : Polynomial.rootMultiplicity a (1 : R[X]) = 0 := by
    simpa [Index] using index_one a
  simpa [Index, h1] using h

/-- **The canonical integer removable value.**  `c · (X - a)^n` with `c ≠ 0` has
index `n`. -/
theorem index_canonical (a : R) (c : R) (hc : c ≠ 0) (n : ℕ) :
    Index a (C c * (X - C a) ^ n) = n := by
  have hc' : (C c : R[X]) ≠ 0 := Polynomial.C_ne_zero.mpr hc
  have h := Polynomial.rootMultiplicity_mul_X_sub_C_pow (p := C c) (a := a) (n := n) hc'
  simpa [Index, Polynomial.rootMultiplicity_C] using h

/-- **The index is a multiplicity.**  The Index mechanism's invariant is additive
under products, scales under powers, is `1` at a simple root, `n` at `(X - a)^n`, and
`n` on the canonical integer removable value `c · (X - a)^n`. -/
theorem index_is_multiplicity :
    (∀ {p q : R[X]}, p * q ≠ 0 → ∀ a : R, Index a (p * q) = Index a p + Index a q) ∧
    (∀ {p : R[X]}, p ≠ 0 → ∀ a : R, ∀ n : ℕ, Index a (p ^ n) = n * Index a p) ∧
    (∀ a : R, Index a (X - C a) = 1) ∧
    (∀ a : R, ∀ n : ℕ, Index a ((X - C a) ^ n) = n) ∧
    (∀ a c : R, c ≠ 0 → ∀ n : ℕ, Index a (C c * (X - C a) ^ n) = n) :=
  ⟨fun h a => index_additive h a,
   fun hp a n => index_pow hp a n,
   index_X_sub_C_self,
   index_pow_self,
   fun a c hc n => index_canonical a c hc n⟩

/-- Formalised-facts register for `ZeroIndex.lean`. -/
def zeroIndexFacts : List String :=
  [ "Index", "index_one", "index_additive", "index_pow", "index_X_sub_C_self",
    "index_pow_self", "index_canonical", "index_is_multiplicity" ]

/-- The register has exactly eight entries. -/
theorem zeroIndexFacts_length : zeroIndexFacts.length = 8 := by decide

end PunoCalculus.ZeroIndex
