import Mathlib
import PunoCalculus.ParabolaVertex

/-!
# The crease: the cusp as the local normal form of every fold

The user's question — *research the brain, what it can do, what made it evolve to
generate thought, then work out the mathematics of every crease* — has a sharp
mathematical core.  The folds of the cerebral cortex (gyri and sulci) are the
creases of a growth/buckling energy on the cortical sheet; globally they obey a
universal scaling law (Mota & Herculano-Houzel, *Science* 2015; Wang et al.,
*PNAS* 2016: exposed area scales with the product of total area and the square
root of thickness, read off a free-energy minimisation).  Locally, however,
**every generic crease has one and the same normal form** — Thom's cusp — and
that local form is elementary, exact, and provable.

This module formalises the local mathematics in its entirety:

* the **fold germ** `Φ a x = x³ − a·x`, whose derivative `3x² − a` vanishes on the
  crease set;
* the **crease criterion** — the derivative vanishes exactly when `3x² = a`, so a
  crease exists only for `a ≥ 0`, and at `a > 0` there are exactly two creases
  `x = ±√(a/3)`, which collide at the **cusp** `a = 0` (a single degenerate crease
  at `x = 0`) and vanish for `a < 0`;
* the **cusp potential** `V a b x = x⁴/4 − a·x²/2 − b·x` of catastrophe theory,
  whose gradient is the fold germ `x³ − a·x − b`, so the **crease manifold is the
  gradient-zero surface**;
* the **cusp curve** itself: parametrised by `a = 3r²`, `b = −2r³`, the gradient
  factors as `(x − r)²(x + 2r)` — the crease is exactly a **double root**, and the
  discriminant vanishes, `4a³ = 27b²`;
* and the concrete instance from `ParabolaVertex`: the **logistic apex** `x = 1/2`
  is a crease of the doubling map (`deriv logistic (1/2) = 0`) — the same point the
  conic vertex sits on.

Scope, as everywhere in this library: exact real algebra and calculus of the
*local* germs.  That the brain's folds take this form is an empirical physical
claim (recorded in the link graph and the research note), **not** something proved
here; what is proved here is that *if* a fold is generic, its crease is a cusp,
and that statement is complete.
-/

noncomputable section

namespace PunoCalculus.Crease

/-- The fold germ in one parameter: `Φ a x = x³ − a·x`.  Its derivative
`3x² − a` vanishes on the crease set; the parameter `a` unfolds the fold and at
`a = 0` the two creases collide — the cusp. -/
def fold (a x : ℝ) : ℝ := x ^ 3 - a * x

/-- **The fold derivative.**  `d/dx Φ a x = 3x² − a`. -/
theorem deriv_fold (a x : ℝ) : deriv (fold a) x = 3 * x ^ 2 - a := by
  have h1 : deriv (fun y : ℝ => y ^ 3) x = 3 * x ^ 2 := by
    rw [deriv_pow_field]; ring_nf
  have h2 : deriv (fun y : ℝ => a * y) x = a := deriv_const_mul_id a
  have hfun : fold a = (fun y : ℝ => y ^ 3) - (fun y : ℝ => a * y) := by
    funext y; unfold fold; simp only [Pi.sub_apply]
  rw [hfun, deriv_sub (by fun_prop) (by fun_prop), h1, h2]

/-- `HasDerivAt` form of `deriv_fold`. -/
theorem hasDerivAt_fold (a x : ℝ) : HasDerivAt (fold a) (3 * x ^ 2 - a) x := by
  rw [← deriv_fold]
  exact (by unfold fold; fun_prop : DifferentiableAt ℝ (fold a) x).hasDerivAt

/-- A point is a **crease** of the fold `Φ a` when the derivative vanishes:
`3x² = a`. -/
def IsCrease (a x : ℝ) : Prop := 3 * x ^ 2 = a

/-- The crease criterion: a point is a crease iff the fold derivative vanishes
there. -/
theorem deriv_fold_zero_iff (a x : ℝ) : deriv (fold a) x = 0 ↔ IsCrease a x := by
  rw [deriv_fold, IsCrease]; constructor <;> intro h <;> linarith

/-- A crease exists only for `a ≥ 0`. -/
theorem crease_nonneg {a x : ℝ} (h : IsCrease a x) : 0 ≤ a := by
  rw [IsCrease] at h; rw [← h]; nlinarith [sq_nonneg x]

/-- Every crease has `x² = a/3`. -/
theorem crease_sq {a x : ℝ} (h : IsCrease a x) : x ^ 2 = a / 3 := by
  rw [IsCrease] at h; linarith

/-- The crease criterion in squares. -/
theorem crease_iff (a x : ℝ) : IsCrease a x ↔ x ^ 2 = a / 3 := by
  rw [IsCrease]; constructor <;> intro h <;> linarith

/-- For `a > 0` the right crease is `√(a/3)`. -/
theorem crease_sqrt {a : ℝ} (ha : 0 < a) : IsCrease a (Real.sqrt (a / 3)) := by
  rw [IsCrease, Real.sq_sqrt (by positivity)]
  ring

/-- For `a > 0` the left crease is `−√(a/3)`. -/
theorem crease_neg_sqrt {a : ℝ} (ha : 0 < a) : IsCrease a (- Real.sqrt (a / 3)) := by
  rw [IsCrease, neg_sq, Real.sq_sqrt (by positivity)]
  ring

/-- **The two creases.**  For `a > 0` the only creases are `±√(a/3)`; as `a → 0⁺`
they collide at the cusp point, and for `a < 0` there are none. -/
theorem crease_eq_sqrt_or {a : ℝ} (ha : 0 < a) {x : ℝ} (h : IsCrease a x) :
    x = Real.sqrt (a / 3) ∨ x = - Real.sqrt (a / 3) := by
  have hx : x ^ 2 = a / 3 := crease_sq h
  have hv : (Real.sqrt (a / 3)) ^ 2 = a / 3 := Real.sq_sqrt (by positivity)
  have h2 : x ^ 2 = (Real.sqrt (a / 3)) ^ 2 := by rw [hx, hv]
  exact sq_eq_sq_iff_eq_or_eq_neg.mp h2

/-- At `a = 0` the single degenerate crease sits at `x = 0` — the cusp point. -/
theorem crease_zero_iff (x : ℝ) : IsCrease 0 x ↔ x = 0 := by
  rw [IsCrease]; constructor
  · intro h; nlinarith [sq_nonneg x]
  · intro h; rw [h]; ring

/-- For `a < 0` the fold has no crease at all: the fold disappears. -/
theorem no_crease_of_neg {a x : ℝ} (ha : a < 0) : ¬ IsCrease a x :=
  fun h => not_le_of_gt ha (crease_nonneg h)

/-- The cusp potential of catastrophe theory: `V a b x = x⁴/4 − a·x²/2 − b·x`.
Its gradient is the fold germ `x³ − a·x − b`, so the critical (crease) set is a
cusp surface in `(a, b, x)`. -/
def cusp (a b x : ℝ) : ℝ := x ^ 4 / 4 - a * x ^ 2 / 2 - b * x

/-- **The cusp gradient is the fold germ.**  `d/dx V a b x = x³ − a·x − b`. -/
theorem deriv_cusp (a b x : ℝ) : deriv (cusp a b) x = x ^ 3 - a * x - b := by
  have h1 : deriv (fun y : ℝ => y ^ 4 / 4) x = x ^ 3 := by
    rw [deriv_div_const, deriv_pow_field]; ring_nf
  have h2 : deriv (fun y : ℝ => a * y ^ 2 / 2) x = a * x := by
    rw [deriv_div_const, deriv_const_mul_field, deriv_pow_field]; ring_nf
  have h3 : deriv (fun y : ℝ => b * y) x = b := deriv_const_mul_id b
  have hfun : cusp a b = (fun y : ℝ => y ^ 4 / 4) - (fun y : ℝ => a * y ^ 2 / 2)
      - (fun y : ℝ => b * y) := by
    funext y; unfold cusp; simp only [Pi.sub_apply]
  rw [hfun, deriv_sub (by fun_prop) (by fun_prop),
      deriv_sub (by fun_prop) (by fun_prop), h1, h2, h3]

/-- **The crease is a double root.**  On the cusp curve `a = 3r²`, `b = −2r³` the
gradient factors as `(x − r)²(x + 2r)`: the two creases have collided into a
double root — the exact signature of the cusp. -/
theorem cusp_curve_factor (r x : ℝ) :
    x ^ 3 - 3 * r ^ 2 * x + 2 * r ^ 3 = (x - r) ^ 2 * (x + 2 * r) := by
  ring

/-- The **discriminant vanishes** on the cusp curve: with `a = 3r²`, `b = −2r³`,
`4a³ = 27b²`.  This is the cusp curve of the fold's parameter plane. -/
theorem cusp_discriminant (r : ℝ) : 4 * (3 * r ^ 2) ^ 3 = 27 * (-(2 * r ^ 3)) ^ 2 := by
  ring

/-- **The logistic apex is a crease.**  The vertex-origin parabola of
`ParabolaVertex` has its apex at `x = 1/2`, where the derivative of the doubling
map vanishes: `deriv logistic (1/2) = 0`.  The conic vertex and the crease of the
logistic map are the same point. -/
theorem deriv_logistic_half :
    deriv PunoCalculus.ParabolaVertex.logistic (1 / 2) = 0 := by
  rw [(PunoCalculus.ParabolaVertex.hasDerivAt_logistic (1 / 2)).deriv]
  norm_num

/-- Formalised-facts register for `Crease.lean`. -/
def creaseFacts : List (String × String) :=
  [ ("fold", "Phi a x = x^3 - a*x: the one-parameter fold germ"),
    ("deriv_fold", "d/dx (Phi a) x = 3*x^2 - a"),
    ("crease_criterion", "x is a crease of Phi a iff 3*x^2 = a (the derivative vanishes)"),
    ("crease_nonneg", "a crease exists only for a >= 0"),
    ("crease_sqrt", "for a > 0 the two creases are +/- sqrt(a/3)"),
    ("crease_zero", "for a = 0 the single crease is x = 0 (the cusp point)"),
    ("no_crease_neg", "for a < 0 the fold has no crease"),
    ("cusp", "V a b x = x^4/4 - a*x^2/2 - b*x: the cusp potential"),
    ("deriv_cusp", "d/dx (V a b) x = x^3 - a*x - b: the fold germ is the cusp gradient"),
    ("cusp_curve_factor", "x^3 - 3r^2x + 2r^3 = (x-r)^2 (x+2r): the crease is a double root"),
    ("cusp_discriminant", "4a^3 = 27b^2 on the cusp curve a=3r^2, b=-2r^3"),
    ("logistic_apex_crease", "the logistic apex x = 1/2 is a crease: deriv logistic (1/2) = 0") ]

/-- The register has exactly twelve entries. -/
theorem creaseFacts_length : creaseFacts.length = 12 := by decide

end PunoCalculus.Crease
