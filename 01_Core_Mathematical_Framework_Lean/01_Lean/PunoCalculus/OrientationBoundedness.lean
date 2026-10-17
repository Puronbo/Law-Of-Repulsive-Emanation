import Mathlib
import PunoCalculus.GreatAttractor

/-!
# Orientation decides boundedness: the two organizing numbers meet

The register has two organizing numbers: the ORDER of the invariant's increment
(`EnstrophyBarrier`, `QuantitativeContinuation`) and the ORIENTATION -- the sign of
the Lyapunov exponent `log |L|` at the fixed point (`GreatAttractor.fixedPoint_logSign`).
This brick joins them.

For the geometric model `N n = r ^ n * A` (the exact orbit of a fixed point with
multiplier `r`), boundedness is decided *entirely* by the orientation:

* `r <= 1` (attracting or marginal): `N` is bounded by its start (`geometric_bounded_of_le_one`);
* `r > 1` (repelling): `N` escapes every bound (`geometric_unbounded_of_one_lt`).

So `∃ B, ∀ n, N n ≤ B  ↔  r <= 1` (`geometric_bounded_iff`), and -- the bridge to
`GreatAttractor` -- the sign of `log r` reads the wall: `0 < log r` iff unbounded,
`log r <= 0` iff bounded (`orientation_decides_boundedness`).  With `r = |L|` this is
exactly the orientation `Repelling`/`Attracting` (`repelling_iff_unbounded`): the
multiplier sign is the direction, and the direction is whether the invariant is
bounded.  That is the on-flow wall (`orientation_vs_invariant.py`) as a theorem.

## The bounded orientation: a floor, a midpoint, and a ceiling

`log r` is unbounded on `(0, ∞)`; the Möbius rescaling
`boundedOrientation r = (r - 1) / (2 * (r + 1))` folds it into the open window
`(-1/2, 1/2)` -- a **floor** `-1/2`, a **midpoint** `0` at `r = 1`, and a
**ceiling** `1/2`, neither end attained.  The map is antisymmetric
(`boundedOrientation (1/r) = -boundedOrientation r`), strictly increasing, and
carries the orientation's sign (`sign (boundedOrientation r) = sign (log r)`), so
the bounded coordinate reads the wall exactly as `log r` does
(`boundedOrientation_reads_the_wall`).

## Linkages: the unbounded orientation, composition, and the window

The bounded orientation is exactly the folded orientation
`boundedOrientation r = (1/2) * tanh ((log r) / 2)` (`boundedOrientation_eq_tanh`),
so it is a bijection of the positive multipliers onto the open window
(`boundedOrientation_bijOn`, `boundedOrientation_image`), with the explicit inverse
`boundedOrientationInv y = (1 + 2y) / (1 - 2y)`.  It is additive under the
register's count (`boundedOrientation_pow`) and carries a velocity-addition
composition law `boundedOrientation (r * s) = (x + y) / (1 + 4xy)` for
`x = boundedOrientation r`, `y = boundedOrientation s` (`boundedOrientation_mul`),
the half-angle addition of `tanh` (`tanh_add`).
-/

namespace PunoCalculus.OrientationBoundedness

open Filter
open scoped Topology

/-- **Attracting / marginal ⇒ bounded.**  A geometric orbit with `0 ≤ r ≤ 1` stays
below its start (for `0 ≤ A`). -/
theorem geometric_bounded_of_le_one {r A : ℝ} (hr : 0 ≤ r) (hr1 : r ≤ 1) (hA : 0 ≤ A) :
    ∀ n, r ^ n * A ≤ A := by
  intro n
  calc r ^ n * A ≤ 1 * A := mul_le_mul_of_nonneg_right (pow_le_one₀ hr hr1) hA
    _ = A := one_mul A

/-- **Repelling ⇒ unbounded.**  A geometric orbit with `r > 1` (and `A > 0`) escapes
every bound. -/
theorem geometric_unbounded_of_one_lt {r A : ℝ} (hr : 1 < r) (hA : 0 < A) :
    ∀ M : ℝ, ∃ n, M < r ^ n * A := by
  intro M
  have hpow : Tendsto (fun n : ℕ => r ^ n) atTop atTop :=
    tendsto_pow_atTop_atTop_of_one_lt hr
  have hcm : Tendsto (fun n : ℕ => r ^ n * A) atTop atTop := by
    simpa only [mul_comm] using hpow.const_mul_atTop hA
  exact (hcm.eventually (eventually_gt_atTop M)).exists

/-- **The geometric dichotomy.**  For a nondegenerate orbit (`r > 0`, `A > 0`):
bounded iff `r <= 1`. -/
theorem geometric_bounded_iff {r A : ℝ} (hr : 0 < r) (hA : 0 < A) :
    (∃ B : ℝ, ∀ n, r ^ n * A ≤ B) ↔ r ≤ 1 := by
  constructor
  · intro ⟨B, hB⟩
    rcases le_or_gt r 1 with hr1 | hr1
    · exact hr1
    · obtain ⟨n, hn⟩ := geometric_unbounded_of_one_lt hr1 hA B
      exact absurd (hB n) (not_le.mpr hn)
  · intro hr1
    exact ⟨A, geometric_bounded_of_le_one (le_of_lt hr) hr1 (le_of_lt hA)⟩

/-- **The orientation decides boundedness.**  The sign of `log r` reads the wall:
positive (`1 < r`, repelling) iff the invariant is unbounded; nonpositive
(`r ≤ 1`, attracting/marginal) iff it is bounded.  The formal twin of
`GreatAttractor.fixedPoint_logSign` and of the on-flow
`orientation_vs_invariant.py` bridge. -/
theorem orientation_decides_boundedness {r A : ℝ} (hr : 0 < r) (hA : 0 < A) :
    (0 < Real.log r ↔ ¬ ∃ B : ℝ, ∀ n, r ^ n * A ≤ B) ∧
    (Real.log r ≤ 0 ↔ ∃ B : ℝ, ∀ n, r ^ n * A ≤ B) := by
  have hiff : (∃ B : ℝ, ∀ n, r ^ n * A ≤ B) ↔ r ≤ 1 := geometric_bounded_iff hr hA
  have hle : Real.log r ≤ 0 ↔ r ≤ 1 := by
    rw [← Real.log_one, Real.log_le_log_iff hr zero_lt_one]
  exact ⟨by rw [Real.log_pos_iff (le_of_lt hr), ← not_le, ← hiff],
         by rw [hle, ← hiff]⟩

/-- **Repelling iff unbounded (the orientation bridge).**  With `r = |L|` this is the
`GreatAttractor` orientation: a repelling fixed point (`1 < |L|`) has an unbounded
geometric invariant, an attracting one (`|L| < 1`) a bounded invariant. -/
theorem repelling_iff_unbounded {L A : ℝ} (hL : L ≠ 0) (hA : 0 < A) :
    (0 < Real.log |L| ↔ ¬ ∃ B : ℝ, ∀ n, |L| ^ n * A ≤ B) ∧
    (Real.log |L| ≤ 0 ↔ ∃ B : ℝ, ∀ n, |L| ^ n * A ≤ B) :=
  orientation_decides_boundedness (abs_pos.mpr hL) hA

/-- The bounded orientation: the Möbius map of the multiplier into the open window
`(-1/2, 1/2)`.  Same sign as `log r`, but folded into a bounded coordinate. -/
noncomputable def boundedOrientation (r : ℝ) : ℝ := (r - 1) / (2 * (r + 1))

/-- **The floor form.**  On the attractive side the bounded orientation is
`-1/2` plus a positive term (`r/(r+1)`), so it never reaches `-1/2`. -/
theorem boundedOrientation_eq_floor_form {r : ℝ} (hr : 0 < r) :
    boundedOrientation r = -(1 / 2) + r / (r + 1) := by
  unfold boundedOrientation
  field_simp
  ring

/-- **The ceiling form.**  It is also `1/2` minus a positive term (`1/(r+1)`), so it
never reaches `1/2`. -/
theorem boundedOrientation_eq_ceiling_form {r : ℝ} (hr : 0 < r) :
    boundedOrientation r = 1 / 2 - 1 / (r + 1) := by
  unfold boundedOrientation
  field_simp
  ring

/-- **The floor.**  `boundedOrientation r > -1/2` for every positive multiplier:
`-1/2` is a strict lower bound, approached but never attained. -/
theorem boundedOrientation_floor {r : ℝ} (hr : 0 < r) :
    -(1 / 2) < boundedOrientation r := by
  have hden : 0 < r + 1 := by linarith
  rw [boundedOrientation_eq_floor_form hr]
  have : 0 < r / (r + 1) := div_pos hr hden
  linarith

/-- **The ceiling.**  `boundedOrientation r < 1/2` for every positive multiplier:
`1/2` is a strict upper bound, approached but never attained. -/
theorem boundedOrientation_ceiling {r : ℝ} (hr : 0 < r) :
    boundedOrientation r < 1 / 2 := by
  have hden : 0 < r + 1 := by linarith
  rw [boundedOrientation_eq_ceiling_form hr]
  have : 0 < 1 / (r + 1) := one_div_pos.mpr hden
  linarith

/-- **The midpoint.**  The neutral multiplier `r = 1` maps to `0`: the centre of the
window, the register's stationary point. -/
theorem boundedOrientation_midpoint : boundedOrientation 1 = 0 := by
  unfold boundedOrientation
  norm_num

/-- **The three distinguished values.**  A floor (`-1/2`, strict lower bound), a
midpoint (`0`, attained at `r = 1`), and a ceiling (`1/2`, strict upper bound):
the bounded orientation lives in the open window straddling its midpoint, with the
floor and ceiling never attained. -/
theorem boundedOrientation_floor_midpoint_ceiling :
    (∀ r : ℝ, 0 < r → -(1 / 2) < boundedOrientation r) ∧
    boundedOrientation 1 = 0 ∧
    (∀ r : ℝ, 0 < r → boundedOrientation r < 1 / 2) :=
  ⟨fun _ hr => boundedOrientation_floor hr, boundedOrientation_midpoint,
   fun _ hr => boundedOrientation_ceiling hr⟩

/-- **Antisymmetry (the Möbius involution).**  Inverting the multiplier negates the
bounded orientation: `boundedOrientation (1/r) = -boundedOrientation r`.  The floor
and ceiling are exchanged, which is why the window is symmetric about `0`. -/
theorem boundedOrientation_antisymm {r : ℝ} (hr : 0 < r) :
    boundedOrientation r⁻¹ = -boundedOrientation r := by
  have hr0 : r ≠ 0 := ne_of_gt hr
  have hr1 : r + 1 ≠ 0 := ne_of_gt (by linarith : (0 : ℝ) < r + 1)
  unfold boundedOrientation
  rw [inv_eq_one_div]
  field_simp
  ring

/-- **Strict monotonicity.**  The bounded orientation is strictly increasing on the
positive multipliers: it preserves the order that the orientation reads. -/
theorem boundedOrientation_lt {r s : ℝ} (hr : 0 < r) (hrs : r < s) :
    boundedOrientation r < boundedOrientation s := by
  have hs : 0 < s := lt_trans hr hrs
  have hr1 : 0 < r + 1 := by linarith
  have hs1 : 0 < s + 1 := by linarith
  rw [boundedOrientation_eq_ceiling_form hr, boundedOrientation_eq_ceiling_form hs]
  have hlt : 1 / (s + 1) < 1 / (r + 1) := one_div_lt_one_div_of_lt hr1 (by linarith)
  linarith

/-- Strict monotonicity, bundled on `(0, ∞)`. -/
theorem boundedOrientation_strictMonoOn :
    StrictMonoOn boundedOrientation (Set.Ioi 0) :=
  fun _ hr _ _ hrs => boundedOrientation_lt hr hrs

/-- **Positive side.**  A repelling multiplier (`1 < r`) gives a positive bounded
orientation. -/
theorem boundedOrientation_pos {r : ℝ} (hr : 1 < r) : 0 < boundedOrientation r := by
  have hr0 : 0 < r := lt_trans zero_lt_one hr
  unfold boundedOrientation
  exact div_pos (by linarith) (by positivity)

/-- **Negative side.**  An attracting multiplier (`r < 1`) gives a negative bounded
orientation. -/
theorem boundedOrientation_neg {r : ℝ} (hr : 0 < r) (hr1 : r < 1) :
    boundedOrientation r < 0 := by
  unfold boundedOrientation
  exact div_neg_of_neg_of_pos (by linarith) (by positivity)

/-- **The sign is the side.**  The bounded orientation is positive iff the multiplier
is repelling (`1 < r`).  Its sign is the orientation's sign. -/
theorem boundedOrientation_pos_iff {r : ℝ} (hr : 0 < r) :
    0 < boundedOrientation r ↔ 1 < r := by
  constructor
  · intro h
    by_contra hc
    rw [not_lt] at hc
    rcases lt_or_eq_of_le hc with h1 | h1
    · exact absurd h (not_lt.mpr (le_of_lt (boundedOrientation_neg hr h1)))
    · subst h1
      rw [boundedOrientation_midpoint] at h
      exact lt_irrefl 0 h
  · intro h
    exact boundedOrientation_pos h

/-- **Zero at the midpoint.**  `boundedOrientation r = 0` iff `r = 1`. -/
theorem boundedOrientation_eq_zero {r : ℝ} (hr : 0 < r) :
    boundedOrientation r = 0 ↔ r = 1 := by
  have hden : 2 * (r + 1) ≠ 0 :=
    ne_of_gt (by positivity : (0 : ℝ) < 2 * (r + 1))
  unfold boundedOrientation
  rw [div_eq_zero_iff]
  constructor
  · rintro (h | h)
    · linarith
    · exact absurd h hden
  · intro h
    left; linarith

/-- **Negative side iff.**  `boundedOrientation r < 0` iff `r < 1`. -/
theorem boundedOrientation_neg_iff {r : ℝ} (hr : 0 < r) :
    boundedOrientation r < 0 ↔ r < 1 := by
  constructor
  · intro h
    by_contra hc
    rw [not_lt] at hc
    rcases lt_or_eq_of_le hc with h1 | h1
    · exact absurd h (not_lt.mpr (le_of_lt (boundedOrientation_pos h1)))
    · subst h1
      rw [boundedOrientation_midpoint] at h
      exact lt_irrefl 0 h
  · intro h
    exact boundedOrientation_neg hr h

/-- **Sign preservation.**  The bounded orientation has exactly the sign of the
orientation `log r`: positive, zero and negative agree (`sign (boundedOrientation r)
= sign (log r)`). -/
theorem boundedOrientation_sign {r : ℝ} (hr : 0 < r) :
    (0 < boundedOrientation r ↔ 0 < Real.log r) ∧
    (boundedOrientation r = 0 ↔ Real.log r = 0) ∧
    (boundedOrientation r < 0 ↔ Real.log r < 0) := by
  have hlogpos : (0 < Real.log r) ↔ 1 < r := Real.log_pos_iff (le_of_lt hr)
  have hlogneg : Real.log r < 0 ↔ r < 1 := by
    rw [← Real.log_one, Real.log_lt_log_iff hr zero_lt_one]
  have hlogzero : Real.log r = 0 ↔ r = 1 := by
    constructor
    · intro h
      have h' : Real.exp (Real.log r) = Real.exp 0 := by rw [h, Real.exp_zero]
      rwa [Real.exp_log hr, Real.exp_zero] at h'
    · intro h
      rw [h, Real.log_one]
  exact ⟨by rw [boundedOrientation_pos_iff hr, hlogpos],
         by rw [boundedOrientation_eq_zero hr, hlogzero],
         by rw [boundedOrientation_neg_iff hr, hlogneg]⟩

/-- **The bounded orientation reads the wall.**  `0 < boundedOrientation r` iff the
invariant is unbounded, `boundedOrientation r ≤ 0` iff it is bounded -- the same
reading as `orientation_decides_boundedness`, in the bounded coordinate. -/
theorem boundedOrientation_reads_the_wall {r A : ℝ} (hr : 0 < r) (hA : 0 < A) :
    (0 < boundedOrientation r ↔ ¬ ∃ B : ℝ, ∀ n, r ^ n * A ≤ B) ∧
    (boundedOrientation r ≤ 0 ↔ ∃ B : ℝ, ∀ n, r ^ n * A ≤ B) := by
  have h := orientation_decides_boundedness hr hA
  have hpos : (0 < boundedOrientation r) ↔ (0 < Real.log r) :=
    (boundedOrientation_sign hr).1
  have hnonpos : (boundedOrientation r ≤ 0) ↔ (Real.log r ≤ 0) := by
    have hlt := (boundedOrientation_sign hr).2.2
    have heq := (boundedOrientation_sign hr).2.1
    constructor
    · intro hle
      rcases lt_or_eq_of_le hle with h1 | h1
      · exact le_of_lt (hlt.mp h1)
      · exact le_of_eq (heq.mp h1)
    · intro hle
      rcases lt_or_eq_of_le hle with h1 | h1
      · exact le_of_lt (hlt.mpr h1)
      · exact le_of_eq (heq.mpr h1)
  exact ⟨hpos.trans h.1, hnonpos.trans h.2⟩

/-- Formalised-facts register for `OrientationBoundedness.lean`. -/
def orientationBoundednessFacts : List String :=
  [ "geometric_bounded_of_le_one", "geometric_unbounded_of_one_lt",
    "geometric_bounded_iff", "orientation_decides_boundedness", "repelling_iff_unbounded" ]

/-- The register has exactly five entries. -/
theorem orientationBoundednessFacts_length : orientationBoundednessFacts.length = 5 := by
  decide

/-- Formalised-facts register for the bounded-orientation brick. -/
def boundedOrientationFacts : List String :=
  [ "boundedOrientation_floor", "boundedOrientation_midpoint",
    "boundedOrientation_ceiling", "boundedOrientation_floor_midpoint_ceiling",
    "boundedOrientation_antisymm", "boundedOrientation_lt",
    "boundedOrientation_strictMonoOn", "boundedOrientation_pos_iff",
    "boundedOrientation_sign", "boundedOrientation_reads_the_wall" ]

/-- The bounded-orientation register has exactly ten entries. -/
theorem boundedOrientationFacts_length : boundedOrientationFacts.length = 10 := by
  decide

/-! ## Linkages: the unbounded orientation, composition, and the window -/

/-- **The hyperbolic form.**  The bounded orientation is half the hyperbolic tangent
of half the orientation: `boundedOrientation r = (1/2) * tanh ((log r) / 2)`.  This
is the exact link between the bounded coordinate and the unbounded orientation
`Real.log`. -/
theorem boundedOrientation_eq_tanh {r : ℝ} (hr : 0 < r) :
    boundedOrientation r = 1 / 2 * Real.tanh (Real.log r / 2) := by
  have h2y : (2 * boundedOrientation r) ∈ Set.Ioo (-1 : ℝ) 1 := by
    refine ⟨?_, ?_⟩
    · have := boundedOrientation_floor hr; linarith
    · have := boundedOrientation_ceiling hr; linarith
  have hratio :
      (1 + 2 * boundedOrientation r) / (1 - 2 * boundedOrientation r) = r := by
    unfold boundedOrientation
    have hr1 : r + 1 ≠ 0 := ne_of_gt (by linarith : (0 : ℝ) < r + 1)
    field_simp
    ring
  have ha : Real.artanh (2 * boundedOrientation r) = Real.log r / 2 := by
    rw [Real.artanh_eq_half_log (Set.mem_Icc.mpr ⟨le_of_lt h2y.1, le_of_lt h2y.2⟩),
      hratio]
    ring
  have h := Real.tanh_artanh h2y
  rw [ha] at h
  linarith [h]

/-- **The count form.**  The bounded orientation of `r ^ n` is half the hyperbolic
tangent of `n` times half the orientation: iterating the orbit adds the (halved)
orientation, so the bounded coordinate is additive along the register's count. -/
theorem boundedOrientation_pow {r : ℝ} (hr : 0 < r) (n : ℕ) :
    boundedOrientation (r ^ n) = 1 / 2 * Real.tanh ((n : ℝ) * Real.log r / 2) := by
  rw [boundedOrientation_eq_tanh (pow_pos hr n), Real.log_pow]

/-- **The hyperbolic addition law.**  `tanh (a + b) = (tanh a + tanh b) /
(1 + tanh a * tanh b)`.  The composition rule that makes `boundedOrientation` a
group-like coordinate. -/
theorem tanh_add (a b : ℝ) :
    Real.tanh (a + b) = (Real.tanh a + Real.tanh b) / (1 + Real.tanh a * Real.tanh b) := by
  have hden : 1 + Real.tanh a * Real.tanh b ≠ 0 := by
    have hval : 1 + Real.tanh a * Real.tanh b
        = Real.cosh (a + b) / (Real.cosh a * Real.cosh b) := by
      rw [Real.tanh_eq_sinh_div_cosh a, Real.tanh_eq_sinh_div_cosh b, Real.cosh_add]
      field_simp
    rw [hval]
    exact ne_of_gt (div_pos (Real.cosh_pos _) (mul_pos (Real.cosh_pos a) (Real.cosh_pos b)))
  rw [Real.tanh_eq_sinh_div_cosh (a + b), Real.sinh_add, Real.cosh_add,
    Real.tanh_eq_sinh_div_cosh a, Real.tanh_eq_sinh_div_cosh b]
  field_simp

/-- **Composition (velocity-addition law).**  Multiplying multipliers adds their
bounded orientations by the hyperbolic addition law:
`boundedOrientation (r * s) = (x + y) / (1 + 4 x y)` with `x = boundedOrientation r`
and `y = boundedOrientation s`.  The bounded coordinate is a group-like (relativistic
velocity) coordinate on the positive multipliers. -/
theorem boundedOrientation_mul {r s : ℝ} (hr : 0 < r) (hs : 0 < s) :
    boundedOrientation (r * s)
      = (boundedOrientation r + boundedOrientation s)
        / (1 + 4 * boundedOrientation r * boundedOrientation s) := by
  rw [boundedOrientation_eq_tanh (mul_pos hr hs),
    Real.log_mul (ne_of_gt hr) (ne_of_gt hs),
    boundedOrientation_eq_tanh hr, boundedOrientation_eq_tanh hs]
  have harg : (Real.log r + Real.log s) / 2 = Real.log r / 2 + Real.log s / 2 := by ring
  rw [harg, tanh_add]
  ring

/-- The inverse of the bounded orientation on the open window:
`boundedOrientationInv y = (1 + 2y) / (1 - 2y)`. -/
noncomputable def boundedOrientationInv (y : ℝ) : ℝ := (1 + 2 * y) / (1 - 2 * y)

/-- The inverse stays positive on the window. -/
theorem boundedOrientationInv_pos {y : ℝ} (hy : y ∈ Set.Ioo (-(1 / 2)) (1 / 2)) :
    0 < boundedOrientationInv y := by
  unfold boundedOrientationInv
  apply div_pos <;> linarith [hy.1, hy.2]

/-- **Right inverse.**  `boundedOrientation` undoes `boundedOrientationInv` on the
window: every window value is attained. -/
theorem boundedOrientation_right_inv {y : ℝ} (hy : y ∈ Set.Ioo (-(1 / 2)) (1 / 2)) :
    boundedOrientation (boundedOrientationInv y) = y := by
  have h1 : (1 : ℝ) - 2 * y ≠ 0 := by linarith [hy.2]
  unfold boundedOrientation boundedOrientationInv
  field_simp
  ring

/-- **Left inverse.**  `boundedOrientationInv` undoes `boundedOrientation` on the
positive multipliers. -/
theorem boundedOrientation_left_inv {r : ℝ} (hr : 0 < r) :
    boundedOrientationInv (boundedOrientation r) = r := by
  have hr1 : r + 1 ≠ 0 := ne_of_gt (by linarith : (0 : ℝ) < r + 1)
  unfold boundedOrientationInv boundedOrientation
  field_simp
  ring

/-- **The window is the range.**  `boundedOrientation` maps the positive multipliers
exactly onto the open window `(-1/2, 1/2)`. -/
theorem boundedOrientation_image :
    boundedOrientation '' Set.Ioi (0 : ℝ) = Set.Ioo (-(1 / 2)) (1 / 2) := by
  ext y
  constructor
  · rintro ⟨r, hr, rfl⟩
    exact ⟨boundedOrientation_floor hr, boundedOrientation_ceiling hr⟩
  · intro hy
    exact ⟨boundedOrientationInv y, boundedOrientationInv_pos hy,
      boundedOrientation_right_inv hy⟩

/-- **Surjectivity onto the window.** -/
theorem boundedOrientation_surjOn :
    Set.SurjOn boundedOrientation (Set.Ioi (0 : ℝ)) (Set.Ioo (-(1 / 2)) (1 / 2)) :=
  fun y hy => ⟨boundedOrientationInv y, boundedOrientationInv_pos hy,
    boundedOrientation_right_inv hy⟩

/-- **Order isomorphism.**  `boundedOrientation` is a bijection from the positive
multipliers onto the open window: strictly increasing, onto, window-valued. -/
theorem boundedOrientation_bijOn :
    Set.BijOn boundedOrientation (Set.Ioi (0 : ℝ)) (Set.Ioo (-(1 / 2)) (1 / 2)) :=
  ⟨fun _ hr => ⟨boundedOrientation_floor hr, boundedOrientation_ceiling hr⟩,
   boundedOrientation_strictMonoOn.injOn, boundedOrientation_surjOn⟩

/-- Formalised-facts register for the bounded-orientation linkages. -/
def boundedOrientationLinkFacts : List String :=
  [ "boundedOrientation_eq_tanh", "boundedOrientation_pow", "tanh_add",
    "boundedOrientation_mul", "boundedOrientationInv_pos",
    "boundedOrientation_right_inv", "boundedOrientation_left_inv",
    "boundedOrientation_image", "boundedOrientation_surjOn",
    "boundedOrientation_bijOn" ]

/-- The linkage register has exactly ten entries. -/
theorem boundedOrientationLinkFacts_length : boundedOrientationLinkFacts.length = 10 := by
  decide

end PunoCalculus.OrientationBoundedness
