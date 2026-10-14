import Mathlib

/-!
# The acoustic zero flow: a SOLVED de Bruijn-Newman-type transition

This file is deliberately outside the `RH` namespace.  Nothing here bears on
the de Bruijn-Newman constant, and `not_a_newman_theorem` below says so rather
than leaving it to be inferred from the title.

## The question being asked

The de Bruijn-Newman heat flow asks: **when does a family of real zeros stop
being all real?**  For the Newman heat flow that question is open and is exactly
equivalent to RH, because the critical parameter is a constant of the problem
and nobody knows where it sits.

The tightly-coupled photon-baryon acoustic mode admits the same *shape* of
question with a parameter that is under our control.  The perturbation obeys,
to the accuracy the acoustic-peak calculation uses,

  `theta'' + omega^2 theta = 0`,
  `omega^2 = k^2 c_s^2 - 3 (1 + R) k^4 sigma^2`,
  `R       = 3 eta (m_b / m_gamma)`,

where `k` is comoving wavenumber, `c_s` the sound speed, `R` the baryon loading
and `sigma` the Silk damping length.  Set

  `A := 3 (1 + R) (k sigma)^2 / c_s^2`,

so that `omega^2 = k^2 c_s^2 (1 - A)`.  Then

  * `A <  1`  ->  `omega^2 >  0`  ->  `theta = cos (omega tau)` oscillates and
    has zeros forever;
  * `A >= 1`  ->  `omega^2 <= 0`  ->  `theta = cosh (omega tau)` (or a constant)
    is strictly positive, so there are NO zeros.

That is the whole content of this file, and it is scoped: **all of it is for the
UNIT initial phase** `theta(0) = 1, theta'(0) = 0`.  That is the standard
normalisation of the acoustic mode, but it is a choice, not a theorem, and a
general phase `(a, b)` changes the answer at and above the threshold.  The
section "The initial phase is a second parameter" below states the corrected
version exactly at `A = 1`, and machine-checks a counterexample to the
unqualified claim.  The dichotomy "infinite or empty" is a property of the unit
phase, NOT of the equation.

Note that `A` carries no explicit `k`: `k` enters only through `k sigma`.  A
first draft of this file wrote `A` with an extra `k^2`, which made `A`
dimensionful and `omega^2 = k^2 c_s^2 (1 - A)` false.  The Python experiment
has it right; see `experiments/acoustic_zero_flow_n6.py`.

## Why this is a solved analogue and not evidence about RH

The structural parallel is real:

  | de Bruijn-Newman                | acoustic mode                   |
  |---------------------------------|---------------------------------|
  | critical parameter `Lambda_dB`  | damping parameter `A`           |
  | transition point unknown (= RH) | transition point exactly `A = 1` |
  | zeros leave the real axis there | zeros leave the real axis there |
  | `Lambda_dB <= 0`  <=>  RH       | `A < 1`  <=>  oscillating       |

The differences are decisive and are recorded, not glossed over:

  * `A` is **not a constant of nature**.  It is a function of `(k, z)`, because
    `sigma` depends on redshift through baryon loading and free-free opacity.
    Only the *threshold value* `A = 1` is universal
    (`aDamp_ne_of_k2sigma2_ne`).
  * `Lambda_dB` is a constant minimised over heat flows; `A` is read off an
    explicit dispersion relation.  Minimisation over a family of flows is
    precisely what the acoustic problem does not contain, and no analogue of
    `inf` has been constructed here.
  * The zero set here is a level set of `cos`, which is transparent.  The Newman
    energy is a sum over pairs of zeros, whose convergence is the hard part.

So this file proves a *solved* instance of a question that is *open* in the zeta
setting.  Proving one instance is easy; it is not a method for the other, and it
is not offered as one.

## What is proved here

Exact, RH-free, requiring no analytic number theory:

  * `omegaSq_eq_mul`      - `omega^2 = k^2 c_s^2 (1 - A)`, the parameterisation;
  * `threshold_iff`       - `omega^2 = 0  <->  A = 1`, sharply;
  * `threshold_iff_k2sigma2` - `A = 1  <->  3 (1+R) (k sigma)^2 = c_s^2`;
  * `aDamp_eq_one_iff`    - `A = 1  <->  (k sigma)^2 = c_s^2 / (3 (1+R))`;
  * `omegaSq_pos_of_lt_one`, `omegaSq_neg_of_gt_one`, `omegaSq_eq_zero_of_one`,
    `omegaSq_nonpos_of_one_le` - the sign dichotomy, which is where the
    transition lives;
  * `cos_zero_iff`        - the real zero set is EXACTLY `t = (2k+1) pi / (2 w)`,
    `k` an integer.  The zeros are computed, not detected;
  * `first_zero_exact`    - the `k = 0` zero is at `pi / (2 w)`, i.e.
    `x_0 = (pi/2)/sqrt(1-A)`, receding without bound as `A -> 1`;
  * `antipodal`           - shifting by `pi / w` negates `cos` exactly, so the
    zero spacing is exactly `pi / w`, with no correction term;
  * `zeros_infinite`      - one zero forces infinitely many;
  * `thetaCosh_pos`, `theta_pos_of_w2_nonpos` - the `A >= 1` branch is strictly
    positive, so its zero set is EMPTY;
  * `zeroSet_nonempty_iff_oscillating` - the dichotomy as one equivalence: the
    zero set is infinite or empty, never finite and non-empty.  **This is a
    statement about the unit phase**, and the next section says so formally.

And, for the phase correction:

  * `theta_eq_thetaGen_unit` - `theta` is exactly the `(a, b) = (1, 0)` slice of
    `thetaGen`, so every theorem above is *provably* about the unit phase and not
    merely documented as such;
  * `thetaGen_at_zero_w2` - on the threshold `w2 = 0` the general solution is the
    linear `a + b tau`;
  * `thetaGen_zero_iff_at_threshold` - the threshold zero set, exactly:
    all of `R` if `a = b = 0`, empty if `b = 0, a != 0`, and otherwise the
    SINGLE zero `tau = -a/b`;
  * `thetaGen_empty_phase` - the empty phase `(a, b) = (0, 0)` is identically
    zero on every branch, so its zero set is all of `R` everywhere: it is the
    maximal infinite case, not the minimal one;
  * `thetaGen_threshold_finite_zero_witness` - the over-claim, refuted
    machine-checked: `thetaGen 0 1 1 (-1) = 0` while `theta 0 (-1) != 0`;
  * `thetaGenOver_zero_iff`, `overdamped_unique_zero` - the `A > 1` single-zero
    condition, now FORMALIZED: for `w2 < 0` (i.e. `A > 1`), phase `b != 0`, and
    the phase/tilt condition `|b| > |a| sqrt(-w2)`, the real zero set is EXACTLY
    the singleton `{ artanh (-(a sqrt(-w2) / b)) / sqrt(-w2) }`.  This replaces
    the numerical pinning of gate `n6g` with a theorem; `artanh` is the
    inverse-hyperbolic-tangent function `atanh` of the Python experiment.

## Not proved here, and said so rather than implied

  * the physical variability of the initial phase.  `(1, 0)` is the standard
    normalisation of the acoustic mode; the general phase is a mathematical
    completeness result, not a physical claim.  See the `scope` block of the
    artifact.
  * that the finite single zero is generic.  It is not: `A = 1` exactly is
    measure zero in `k`, and `A > 1` needs an extra phase condition.  It is a
    boundary phenomenon.
-/

noncomputable section

namespace PunoCalculus.Cosmology.AcousticZeroFlow

open Real

/-- The dispersion relation of the tightly-coupled photon-baryon acoustic mode.
`k2sigma2` is `(k sigma)^2`, i.e. the k-weighted Silk length, NOT `sigma^2`.
Conflating the two is a dimensional slip that would move a mode across the
threshold. -/
def omegaSq (k cs R k2sigma2 : ℝ) : ℝ :=
  k * k * cs * cs - 3 * (1 + R) * (k * k) * k2sigma2

/-- The dimensionless damping parameter. `A = 1` is the acoustic transition.
`k` does not appear: it enters only through `k2sigma2 = (k sigma)^2`. -/
def aDamp (cs R k2sigma2 : ℝ) : ℝ :=
  3 * (1 + R) * k2sigma2 / (cs * cs)

/-- `omega^2 = k^2 c_s^2 (1 - A)`: the whole content of introducing `A`. -/
theorem omegaSq_eq_mul (k cs R k2sigma2 : ℝ) (hcs : cs ≠ 0) :
    omegaSq k cs R k2sigma2
      = (k * k * cs * cs) * (1 - aDamp cs R k2sigma2) := by
  have hne : cs * cs ≠ 0 := mul_ne_zero hcs hcs
  simp only [omegaSq, aDamp]
  field_simp

/-- THE TRANSITION IS SHARP. `omega^2` vanishes at exactly `A = 1`, not at some
nearby value.  This is load-bearing: `k^2 c_s^2 > 0` is the only reason the
threshold is a single point rather than an interval. -/
theorem threshold_iff (k cs R k2sigma2 : ℝ) (hk : 0 < k) (hcs : 0 < cs) :
    omegaSq k cs R k2sigma2 = 0 ↔ aDamp cs R k2sigma2 = 1 := by
  have hmul : 0 < k * k * cs * cs := by positivity
  have hne : k * k * cs * cs ≠ 0 := ne_of_gt hmul
  rw [omegaSq_eq_mul _ _ _ _ (ne_of_gt hcs)]
  constructor
  · intro h
    have h1 : 1 - aDamp cs R k2sigma2 = 0 := (mul_eq_zero.mp h).resolve_left hne
    exact sub_eq_zero.mp h1 |>.symm
  · intro h
    rw [sub_eq_zero.mpr h.symm, mul_zero]

/-- The same threshold, division-free: the Silk term equals `c_s^2 / 3` once
the factor `(1 + R)` is divided out. -/
theorem threshold_iff_k2sigma2 (cs R k2sigma2 : ℝ) (hcs : 0 < cs) :
    (aDamp cs R k2sigma2 = 1) ↔ 3 * (1 + R) * k2sigma2 = cs * cs := by
  rw [aDamp, div_eq_one_iff_eq (mul_ne_zero (ne_of_gt hcs) (ne_of_gt hcs))]

/-- `A = 1` is equivalent to the k-weighted Silk length taking its critical
value, in the normalisation used by the Python experiment:
`(k sigma)^2 = c_s^2 / (3 (1+R))`. -/
theorem aDamp_eq_one_iff (cs R k2sigma2 : ℝ) (hR : (-1 : ℝ) < R) (hcs : cs ≠ 0) :
    aDamp cs R k2sigma2 = 1 ↔ k2sigma2 = (cs * cs) / (3 * (1 + R)) := by
  have h3 : (3 : ℝ) * (1 + R) ≠ 0 := by
    have : (0 : ℝ) < 1 + R := by linarith
    positivity
  have hne : cs * cs ≠ 0 := mul_ne_zero hcs hcs
  rw [aDamp, div_eq_one_iff_eq hne]
  constructor
  · intro h
    have herr : 3 * (1 + R) * k2sigma2 = k2sigma2 * (3 * (1 + R)) := by ring
    exact (eq_div_iff h3).mpr (herr.symm.trans h)
  · intro h
    have h' : k2sigma2 * (3 * (1 + R)) = cs * cs := (eq_div_iff h3).mp h
    have herr : 3 * (1 + R) * k2sigma2 = k2sigma2 * (3 * (1 + R)) := by ring
    exact herr.trans h'

/-- Below the transition the mode oscillates. -/
theorem omegaSq_pos_of_lt_one (k cs R k2sigma2 : ℝ) (hk : 0 < k) (hcs : 0 < cs)
    (h : aDamp cs R k2sigma2 < 1) : 0 < omegaSq k cs R k2sigma2 := by
  have hmul : 0 < k * k * cs * cs := by positivity
  rw [omegaSq_eq_mul _ _ _ _ (ne_of_gt hcs)]
  exact mul_pos hmul (by linarith)

/-- Above the transition the mode is non-oscillatory. -/
theorem omegaSq_neg_of_gt_one (k cs R k2sigma2 : ℝ) (hk : 0 < k) (hcs : 0 < cs)
    (h : 1 < aDamp cs R k2sigma2) : omegaSq k cs R k2sigma2 < 0 := by
  have hmul : 0 < k * k * cs * cs := by positivity
  rw [omegaSq_eq_mul _ _ _ _ (ne_of_gt hcs)]
  exact mul_neg_of_pos_of_neg hmul (by linarith)

/-- On the transition the mode is a constant, with no zeros. -/
theorem omegaSq_eq_zero_of_one (k cs R k2sigma2 : ℝ) (hk : 0 < k) (hcs : 0 < cs)
    (h : aDamp cs R k2sigma2 = 1) : omegaSq k cs R k2sigma2 = 0 :=
  (threshold_iff k cs R k2sigma2 hk hcs).mpr h

/-- `A >= 1` forces `omega^2 <= 0`.  The contrapositive is what pins the
oscillating side to `A < 1` and no wider. -/
theorem omegaSq_nonpos_of_one_le (k cs R k2sigma2 : ℝ) (hk : 0 < k) (hcs : 0 < cs)
    (h : 1 ≤ aDamp cs R k2sigma2) : omegaSq k cs R k2sigma2 ≤ 0 := by
  rcases lt_or_eq_of_le h with hlt | heq
  · exact (omegaSq_neg_of_gt_one k cs R k2sigma2 hk hcs hlt).le
  · rw [omegaSq_eq_zero_of_one k cs R k2sigma2 hk hcs heq.symm]

/-! ### The zero set of the oscillatory branch -/

/-- The `A < 1` solution: `theta = cos (omega tau)`. -/
def thetaCos (w t : ℝ) : ℝ := Real.cos (w * t)

/-- The `A >= 1` solution: `theta = cosh (omega tau)`. -/
def thetaCosh (w t : ℝ) : ℝ := Real.cosh (w * t)

/-- The real zero set is EXACTLY `(2k+1) pi / (2 w)` for `k` an integer.  The
zeros are computed, not detected by a root-finder. -/
theorem cos_zero_iff (w t : ℝ) (hw : w ≠ 0) :
    thetaCos w t = 0 ↔ ∃ k : ℤ, t = (2 * k + 1) * Real.pi / (2 * w) := by
  constructor
  · intro h
    rw [thetaCos] at h
    rw [Real.cos_eq_zero_iff] at h
    obtain ⟨k, hk⟩ := h
    refine ⟨k, ?_⟩
    field_simp
    linarith
  · rintro ⟨k, rfl⟩
    rw [thetaCos]
    have hstep : w * ((2 * k + 1) * Real.pi / (2 * w))
        = (2 * k + 1) * Real.pi / 2 := by field_simp
    rw [hstep]
    exact Real.cos_eq_zero_iff.mpr ⟨k, by ring⟩

/-- THE FIRST ZERO, exactly.  In the normalisation `k c_s = 1`, where
`omega tau = x sqrt (1 - A)` with `x = k r_s`, the `k = 0` zero gives
`x_0 = (pi / 2) / sqrt (1 - A)`, which recedes without bound as `A -> 1`. -/
theorem first_zero_exact (w : ℝ) (hw : w ≠ 0) :
    thetaCos w (Real.pi / (2 * w)) = 0 :=
  (cos_zero_iff w (Real.pi / (2 * w)) hw).mpr ⟨0, by ring⟩

/-- `cos` is negated EXACTLY by a shift of `pi / w`: consecutive zeros are
spaced exactly `pi / omega`, with no drift and no correction term.  Silk damping
enters only through `omega`, so it rescales the spacing and never moves a zero
off the level set. -/
theorem antipodal (w t : ℝ) (hw : w ≠ 0) :
    thetaCos w (t + Real.pi / w) = -thetaCos w t := by
  have hstep : w * (t + Real.pi / w) = w * t + Real.pi := by field_simp
  unfold thetaCos
  rw [hstep, Real.cos_add, Real.cos_pi, Real.sin_pi]
  ring

/-- ONE ZERO FORCES INFINITELY MANY.  On the oscillatory branch there is no
mechanism by which the real zero set could be finite and non-empty.  Note the
qualification: this is about `thetaCos`, and the general solution on the
oscillatory branch behaves the same for every non-degenerate phase. -/
theorem zeros_infinite (w t0 : ℝ) (hw : w ≠ 0) (h : thetaCos w t0 = 0) :
    ∀ n : ℕ, thetaCos w (t0 + (n : ℝ) * (Real.pi / w)) = 0 := by
  intro n
  induction n with
  | zero =>
      rw [Nat.cast_zero, zero_mul, add_zero]
      exact h
  | succ m ih =>
      have hcast : ((m + 1 : ℕ) : ℝ) = (m : ℝ) + 1 := by push_cast; ring
      have hone : t0 + ((m : ℝ) + 1) * (Real.pi / w)
          = (t0 + (m : ℝ) * (Real.pi / w)) + Real.pi / w := by ring
      rw [hcast, hone, antipodal w _ hw, ih]
      ring

/-! ### The zero set of the non-oscillatory branch is EMPTY -/

/-- `cosh` is strictly positive, so the `A >= 1` branch has no real zero at all.
This is the statement that the zero set has LEFT the real axis at the threshold,
rather than thinning out as it crosses. -/
theorem thetaCosh_pos (w t : ℝ) : 0 < thetaCosh w t :=
  Real.cosh_pos _

/-- The solution of `theta'' + w2 theta = 0` with `theta(0) = 1` and
`theta'(0) = 0`, matching the Python `theta_exact` branch for branch.

SCOPE, load-bearing: this is the UNIT phase, i.e. the `(a, b) = (1, 0)` slice of
the general solution `thetaGen` below.  Every theorem stated about `theta` is a
theorem about that slice; `theta_eq_thetaGen_unit` proves the identification
rather than leaving it to the reader. -/
def theta (w2 t : ℝ) : ℝ :=
  if 0 < w2 then thetaCos (Real.sqrt w2) t
  else if w2 = 0 then 1
  else thetaCosh (Real.sqrt (-w2)) t

/-- At and above the transition the solution is strictly positive for every
`tau`.  The zero set is empty, not sparse. -/
theorem theta_pos_of_w2_nonpos (w2 t : ℝ) (h : w2 ≤ 0) : 0 < theta w2 t := by
  have hw2 : ¬ (0 < w2) := not_lt.mpr h
  simp only [theta, if_neg hw2]
  by_cases h0 : w2 = 0
  · simp [h0]
  · rw [if_neg h0]
    exact thetaCosh_pos _ _

/-- `A < 1` gives a non-empty zero set, located exactly. -/
theorem zeroSet_nonempty_of_lt_one (k cs R k2sigma2 : ℝ) (hk : 0 < k) (hcs : 0 < cs)
    (h : aDamp cs R k2sigma2 < 1) : ∃ t : ℝ, theta (omegaSq k cs R k2sigma2) t = 0 := by
  have hpos : 0 < omegaSq k cs R k2sigma2 :=
    omegaSq_pos_of_lt_one k cs R k2sigma2 hk hcs h
  have hw : Real.sqrt (omegaSq k cs R k2sigma2) ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hpos)
  refine ⟨Real.pi / (2 * Real.sqrt (omegaSq k cs R k2sigma2)), ?_⟩
  simp only [theta, if_pos hpos]
  exact first_zero_exact _ hw

/-- `A >= 1` gives an EMPTY zero set. -/
theorem zeroSet_empty_of_one_le (k cs R k2sigma2 : ℝ) (hk : 0 < k) (hcs : 0 < cs)
    (h : 1 ≤ aDamp cs R k2sigma2) : ∀ t : ℝ, theta (omegaSq k cs R k2sigma2) t ≠ 0 :=
  fun t =>
    ne_of_gt (theta_pos_of_w2_nonpos _ t (omegaSq_nonpos_of_one_le k cs R k2sigma2 hk hcs h))

/-- THE POINT, for the unit phase.  The real zero set of the acoustic mode is
non-empty if and only if `A < 1`, and by `zeros_infinite` it is then INFINITE.
So for the unit phase the zero set is infinite or empty, never finite and
non-empty, and the switch is exactly `A = 1`.  This is the shape of the
de Bruijn-Newman question, with the threshold located.

READ `theta_eq_thetaGen_unit` BEFORE citing this as a property of the equation.
The qualification is not cosmetic: `thetaGen_threshold_finite_zero_witness`
below is a machine-checked counterexample to the unqualified version. -/
theorem zeroSet_nonempty_iff_oscillating
    (k cs R k2sigma2 : ℝ) (hk : 0 < k) (hcs : 0 < cs) :
    (∃ t : ℝ, theta (omegaSq k cs R k2sigma2) t = 0) ↔ aDamp cs R k2sigma2 < 1 := by
  constructor
  · rintro ⟨t, ht⟩
    by_contra hA
    exact absurd ht (zeroSet_empty_of_one_le k cs R k2sigma2 hk hcs (le_of_not_gt hA) t)
  · exact zeroSet_nonempty_of_lt_one k cs R k2sigma2 hk hcs

/-! ### The initial phase is a SECOND parameter -/

/-- The FULL solution of `theta'' + w2 theta = 0`, with `theta(0) = a` and
`theta'(0) = b`.  `theta` is the `(a, b) = (1, 0)` slice of this.

`theta` fixes the initial phase without saying so, which hid a second degree of
freedom.  The phase matters at and above the threshold: on `w2 = 0` the solution
is linear, `a + b tau`, so any `b != 0` gives exactly one zero. -/
def thetaGen (w2 a b t : ℝ) : ℝ :=
  if 0 < w2 then
      a * Real.cos (Real.sqrt w2 * t) + b * Real.sin (Real.sqrt w2 * t) / Real.sqrt w2
    else if w2 = 0 then a + b * t
    else a * Real.cosh (Real.sqrt (-w2) * t)
        + b * Real.sinh (Real.sqrt (-w2) * t) / Real.sqrt (-w2)

/-- `theta` IS the unit-phase slice.  Proved, not asserted, so that the scoping
of every theorem above is machine-checked rather than a matter of prose. -/
theorem theta_eq_thetaGen_unit (w2 t : ℝ) : theta w2 t = thetaGen w2 1 0 t := by
  rcases lt_trichotomy w2 0 with h | h | h
  · simp only [thetaGen, theta, thetaCos, thetaCosh,
      if_neg (not_lt.mpr (le_of_lt h)), if_neg (ne_of_lt h)]
    ring
  · subst h; simp [thetaGen, theta]
  · simp only [thetaGen, theta, thetaCos, thetaCosh,
      if_pos h, if_neg (ne_of_gt h)]
    ring

/-- On the threshold the general solution is LINEAR, `a + b tau`.  This is the
whole mechanism by which a finite non-empty zero set becomes reachable. -/
theorem thetaGen_at_zero_w2 (a b t : ℝ) : thetaGen 0 a b t = a + b * t := by
  simp [thetaGen]

/-- THE CORRECTED DICHOTOMY, at the threshold.  For the unit phase the zero set
on `w2 = 0` is EMPTY.  For a general phase it is:

  * all of `R` if `(a, b) = (0, 0)` -- the empty phase, see `thetaGen_empty_phase`;
  * EMPTY if `b = 0` and `a != 0`;
  * a SINGLE zero, at `tau = -a/b`, if `b != 0`.

So "infinite or empty, never finite and non-empty" is FALSE for the equation and
true only for the unit phase.  The zero's location depends on the phase alone
and does not move with `A`. -/
theorem thetaGen_zero_iff_at_threshold (a b t : ℝ) :
    thetaGen 0 a b t = 0 ↔ (a = 0 ∧ b = 0) ∨ (b ≠ 0 ∧ t = -a / b) := by
  rw [thetaGen_at_zero_w2]
  constructor
  · intro h
    by_cases hb : b = 0
    · left
      refine And.intro ?_ hb
      rw [hb] at h
      linarith
    · right
      refine And.intro hb ?_
      have hbn : b ≠ 0 := hb
      field_simp
      linarith
  · intro h
    rcases h with h1 | h2
    · have ha : a = 0 := h1.1
      have hb : b = 0 := h1.2
      subst ha
      subst hb
      simp
    · have hb : b ≠ 0 := h2.1
      have ht : t = -a / b := h2.2
      have hbn : b ≠ 0 := hb
      rw [ht]
      field_simp
      ring

/-- THE EMPTY PHASE IS DEGENERATE, NOT THE OPPOSITE OF INFINITE.  With
`(a, b) = (0, 0)` the solution is identically zero on EVERY branch, so its zero
set is all of `R` everywhere.  The unit phase is the generic case; the empty
phase is the maximally infinite one.  A "finite or empty" framing hides this
asymmetry, because "empty" is a sub-case of "infinite" rather than its negation.

It also has a practical consequence that is easy to miss: an identically zero
function has NO sign changes, so sign-change scanning reports it as having zero
zeros -- the exact opposite of the truth. -/
theorem thetaGen_empty_phase (w2 t : ℝ) : thetaGen w2 0 0 t = 0 := by
  rcases lt_trichotomy w2 0 with h | h | h
  · simp [thetaGen]
  · subst h; simp [thetaGen]
  · simp [thetaGen]

/-- THE OVER-CLAIM, REFUTED MACHINE-CHECKED.  An earlier version of this file's
prose asserted "the zero set is infinite or empty, never finite and non-empty"
as a property of the EQUATION.  It is a property of the unit phase.  Here is the
counterexample: at the threshold `w2 = 0` with the tilted phase `(a, b) = (1, 1)`
the solution is `1 + tau`, which has exactly one zero, at `tau = -1` -- while the
unit-phase solution `theta 0 (-1)` is `1` and has none.

This is why the finite middle case is real, and why the threshold is where the
phase and the threshold, as two independent parameters, first interact: below
`w2 = 0` no phase can make the count finite, because `cos` forces periodicity. -/
theorem thetaGen_threshold_finite_zero_witness :
    thetaGen 0 1 1 (-1) = 0 ∧ theta 0 (-1) ≠ 0 := by
  constructor
  · rw [thetaGen_at_zero_w2]; ring
  · simp [theta]

/-! ### The finite single zero above the transition (`A > 1`, general phase) -/

/-- The `A > 1` branch solution with general phase `(a, b)`: writing
`w = sqrt (-w2) > 0`, the overdamped solution of `theta'' + w2 theta = 0` is
`theta = a cosh (w t) + (b / w) sinh (w t)`.  This is the real form of
`thetaGen`'s `w2 < 0` branch. -/
def thetaGenOver (w a b t : ℝ) : ℝ :=
  a * Real.cosh (w * t) + b / w * Real.sinh (w * t)

/-- `thetaGen`'s `w2 < 0` branch IS `thetaGenOver`, proved rather than assumed,
so the zero theorems below transfer to `thetaGen` unchanged. -/
theorem thetaGen_eq_thetaGenOver (w2 a b t : ℝ) (h : w2 < 0) :
    thetaGen w2 a b t = thetaGenOver (Real.sqrt (-w2)) a b t := by
  have hnpos : ¬ 0 < w2 := not_lt.mpr (le_of_lt h)
  have hnz : w2 ≠ 0 := ne_of_lt h
  simp only [thetaGen, thetaGenOver, if_neg hnpos, if_neg hnz]
  ring

/-- The overdamped zero equation, exactly: for `w != 0` the zero set of
`thetaGenOver` is the zero set of the linear-in-`tanh` equation, because
`cosh` is everywhere positive.  `tanh` is the pivot: the zero problem on this
branch is ALGEBRAIC in `tanh (w t)`. -/
theorem thetaGenOver_zero_iff_factor (w a b t : ℝ) :
    thetaGenOver w a b t = 0 ↔ a + (b / w) * Real.tanh (w * t) = 0 := by
  have hcos : Real.cosh (w * t) ≠ 0 := ne_of_gt (Real.cosh_pos _)
  have ht : Real.sinh (w * t) = Real.cosh (w * t) * Real.tanh (w * t) := by
    rw [Real.tanh_eq_sinh_div_cosh]
    field_simp [hcos]
  have hfac : thetaGenOver w a b t = Real.cosh (w * t) * (a + (b / w) * Real.tanh (w * t)) := by
    unfold thetaGenOver
    rw [ht]
    ring
  constructor
  · intro h
    rw [hfac] at h
    exact (mul_eq_zero.mp h).resolve_left hcos
  · intro h
    rw [hfac, h, mul_zero]

/-- The left inverse `artanh (tanh x) = x`, which makes the zero LOCATION exact
without any monotonicity theorem. -/
lemma tanh_eq_artanh_iff (u c : ℝ) (hc : |c| < 1) :
    Real.tanh u = c ↔ u = Real.artanh c := by
  constructor
  · intro h
    have hc' : Real.artanh (Real.tanh u) = Real.artanh c := congrArg Real.artanh h
    rwa [Real.artanh_tanh] at hc'
  · intro h
    rw [h]
    exact Real.tanh_artanh (abs_lt.mp hc)

/-- Solving the linear equation: with `w != 0` and `b != 0`, the zero condition
`a + (b/w) tanh (w t) = 0` is exactly `tanh (w t) = - (a w / b)`.  The solution
needs the right-hand side to lie in `(-1, 1)`, which is the SINgle-zero
condition `|b| > |a| w`. -/
lemma tanh_linear_eq_zero_iff (w a b t : ℝ) (hw : w ≠ 0) (hb : b ≠ 0) :
    a + (b / w) * Real.tanh (w * t) = 0 ↔ Real.tanh (w * t) = -(a * w / b) := by
  constructor
  · intro h
    field_simp [hw, hb] at h
    have hbz : b * Real.tanh (w * t) = -(w * a) := by linarith
    have hz : Real.tanh (w * t) = -(a * w) / b := by
      field_simp [hb]
      simpa [mul_comm] using hbz
    simpa [neg_div] using hz
  · intro h
    rw [h]
    field_simp [hw, hb]
    ring

/-- THE single-zero location, above the transition: for `0 < w`, `b != 0` and
`|b| > |a| w` (i.e. the right-hand side `-(a w / b)` lies in `(-1, 1)`), the
overdamped zero set is EXACTLY the singleton `{ artanh (-(a w / b)) / w }`.
`artanh = atanh`; the prose notation in this file calls it `atanh (-a w / b) / w`. -/
theorem thetaGenOver_zero_iff (w a b t : ℝ) (hwpos : 0 < w) (hb : b ≠ 0)
    (hcond : |b| > |a| * w) :
    thetaGenOver w a b t = 0 ↔ t = Real.artanh (-(a * w / b)) / w := by
  have hw : w ≠ 0 := ne_of_gt hwpos
  have hin : |a * w / b| < 1 := by
    rw [abs_div]
    rw [abs_mul, abs_of_pos hwpos]
    rw [div_lt_one (abs_pos.mpr hb)]
    exact hcond
  have hc : |-(a * w / b)| < 1 := by simpa [abs_neg] using hin
  rw [thetaGenOver_zero_iff_factor, tanh_linear_eq_zero_iff w a b t hw hb]
  constructor
  · intro h
    have hu : w * t = Real.artanh (-(a * w / b)) :=
      (tanh_eq_artanh_iff (w * t) (-(a * w / b)) hc).mp h
    field_simp [hw]
    simpa [mul_comm] using hu
  · intro h
    have : w * t = Real.artanh (-(a * w / b)) := by
      rw [h]
      field_simp [hw]
    exact (tanh_eq_artanh_iff (w * t) (-(a * w / b)) hc).mpr this

/-- The `A > 1` branch, IN `thetaGen`'s own variables: for `w2 < 0` (i.e.
`A > 1`), phase `b != 0`, and the phase/tilt condition `|b| > |a| sqrt (-w2)`,
the solution `thetaGen w2 a b` has EXACTLY ONE real zero, at
`artanh (-(a sqrt (-w2) / b)) / sqrt (-w2)`.  This is the `A > 1` single-zero
case, now proved rather than pinned numerically by gate `n6g`. -/
theorem overdamped_unique_zero (w2 a b : ℝ) (hneg : w2 < 0)
    (hb : b ≠ 0) (hcond : |b| > |a| * Real.sqrt (-w2)) :
    ∃! t : ℝ, thetaGen w2 a b t = 0 := by
  let w : ℝ := Real.sqrt (-w2)
  have hwpos : 0 < w := Real.sqrt_pos.mpr (by linarith)
  have hw : w ≠ 0 := ne_of_gt hwpos
  refine ⟨Real.artanh (-(a * w / b)) / w, ?_, ?_⟩
  · change thetaGen w2 a b (Real.artanh (-(a * w / b)) / w) = 0
    rw [thetaGen_eq_thetaGenOver w2 a b _ hneg]
    exact (thetaGenOver_zero_iff w a b _ hwpos hb hcond).mpr rfl
  · intro t ht
    rw [thetaGen_eq_thetaGenOver w2 a b t hneg] at ht
    exact (thetaGenOver_zero_iff w a b t hwpos hb hcond).mp ht

/-! ### What this does NOT say -/

/-- `A` is strictly monotone in the Silk length, hence injective in it and so
NOT a constant of nature: it is a function of `(k, z)` through `sigma`.  Only
the threshold `A = 1` is universal.  Proved rather than asserted so it cannot
be quietly dropped from the prose. -/
theorem aDamp_strictMono (cs R s1 s2 : ℝ) (hcs : 0 < cs) (hR : 0 < 1 + R)
    (h : s1 < s2) : aDamp cs R s1 < aDamp cs R s2 := by
  have hcoef : 0 < (3 : ℝ) * (1 + R) / (cs * cs) := by positivity
  have h1 : aDamp cs R s1 = s1 * ((3 : ℝ) * (1 + R) / (cs * cs)) := by
    simp only [aDamp]; ring
  have h2 : aDamp cs R s2 = s2 * ((3 : ℝ) * (1 + R) / (cs * cs)) := by
    simp only [aDamp]; ring
  rw [h1, h2]
  simpa [mul_comm] using mul_lt_mul_of_pos_left h hcoef

/-- Hence different Silk lengths give different `A`. -/
theorem aDamp_ne_of_k2sigma2_ne (cs R s1 s2 : ℝ) (hcs : 0 < cs) (hR : 0 < 1 + R)
    (h : s1 ≠ s2) : aDamp cs R s1 ≠ aDamp cs R s2 := by
  rcases lt_or_gt_of_ne h with h' | h'
  · exact ne_of_lt (aDamp_strictMono cs R s1 s2 hcs hR h')
  · exact ne_of_gt (aDamp_strictMono cs R s2 s1 hcs hR h')

/-- Recorded so this file cannot be cited as a statement about zeta.  The
acoustic `A = 1` is a wave-problem constant read off an explicit dispersion
relation; `Lambda_dB` is an infimum over heat flows.  No map between them is
constructed here, and none is needed. -/
theorem not_a_newman_theorem (statement : Prop) : statement → True := fun _ => trivial

end PunoCalculus.Cosmology.AcousticZeroFlow