import Mathlib
import PunoCalculus.OrientationBoundedness

/-!
# Orientation law: the growth rate equals the orientation (C8, model core)

Card **C8** of `EXPLICIT_CLAIMS.md` claims `sign(lambda) = sign(mu)`, where `lambda`
is the orbit's Lyapunov base (the *orientation*) and `mu = d/dt log(critical content)`
is the growth rate.  Empirically it holds in six systems (`orientation_vs_invariant.py`), three attracting
and three repelling.  Its *model core* is a theorem, and that is what this brick proves.

The core is first stated for a *general* positive sequence: the growth rate is the log
of its relative increment (`logGrowth_of_ratio_eq`), so sign-of-growth is exactly
strict increase (`logGrowth_pos_iff`) and non-positive growth forces boundedness
(`bounded_of_nonpos_logGrowth`, hence `exists_pos_logGrowth_of_unbounded`) -- with no
geometric assumption.  The exact model is then the constant-relative-increment orbit:
on `N n = r^n * A`, the growth rate

    mu(n) = log N(n+1) - log(N n)

is constant and equal to the orientation `lambda = log r` (`logGrowth_geometric`).
Hence `sign(mu) = sign(lambda)` (`sign_match`), and by
`OrientationBoundedness.orientation_decides_boundedness` that shared sign *reads the
wall*: `mu > 0` iff the invariant escapes every bound (`orientation_reads_wall`).
So on the model, "the growth rate of the critical content" and "the orientation" are
the same number, and it is the wall's own reading -- the analytic claim that this
identification survives the real flow (card C8 proper) stays empirical/OPEN.
-/

noncomputable section

namespace PunoCalculus.OrientationLaw

open PunoCalculus.OrientationBoundedness

/-- The geometric orbit `N n = r ^ n * A` (same model as `OrientationBoundedness`). -/
def geometricOrbit (r A : ℝ) (n : ℕ) : ℝ := r ^ n * A

/-- The orientation `lambda = log r` (Lyapunov base of the orbit). -/
def orientation (r : ℝ) : ℝ := Real.log r

/-- Discrete log-growth rate `mu(n) = log(N(n+1)) - log(N n)` of a positive sequence:
the finite-difference reading of `d/dt log(content)`. -/
def logGrowth (N : ℕ → ℝ) (n : ℕ) : ℝ := Real.log (N (n + 1)) - Real.log (N n)

/-- **General growth law.**  For any positive sequence whose *relative increment* is
the constant `r` (`N (n+1) = r * N n`), the growth rate is `log r`.  The geometric
orbit is the special case `A * r^n`; this is the honest model form of C8 -- the
growth rate of the content is the log of its relative increment. -/
theorem logGrowth_of_ratio_eq {N : ℕ → ℝ} (hN : ∀ k, 0 < N k) {r : ℝ} (hr : 0 < r)
    (h : ∀ n, N (n + 1) = r * N n) (n : ℕ) : logGrowth N n = Real.log r := by
  unfold logGrowth
  rw [h n, Real.log_mul (ne_of_gt hr) (ne_of_gt (hN n))]
  ring

/-- **C8 model core: `mu == lambda`.**  On the geometric orbit the growth rate is
constant and equals the orientation `log r`.  Now a corollary of the general growth
law `logGrowth_of_ratio_eq` (the geometric orbit has constant relative increment). -/
theorem logGrowth_geometric {r A : ℝ} (hr : 0 < r) (hA : 0 < A) (n : ℕ) :
    logGrowth (geometricOrbit r A) n = orientation r := by
  have hN : ∀ k, 0 < geometricOrbit r A k := fun k => mul_pos (pow_pos hr k) hA
  have hrec : ∀ k, geometricOrbit r A (k + 1) = r * geometricOrbit r A k := by
    intro k; unfold geometricOrbit; rw [pow_succ]; ring
  show logGrowth (geometricOrbit r A) n = Real.log r
  exact logGrowth_of_ratio_eq hN hr hrec n

/-- **Sign of the growth rate is the direction of motion** (no geometry).  The growth
rate is positive exactly when the critical content strictly increased. -/
theorem logGrowth_pos_iff {N : ℕ → ℝ} (hN : ∀ k, 0 < N k) (n : ℕ) :
    (0 < logGrowth N n) ↔ N n < N (n + 1) := by
  unfold logGrowth
  rw [sub_pos, Real.log_lt_log_iff (hN n) (hN (n + 1))]

/-- **Non-positive growth means non-increase** (no geometry). -/
theorem logGrowth_nonpos_iff {N : ℕ → ℝ} (hN : ∀ k, 0 < N k) (n : ℕ) :
    logGrowth N n ≤ 0 ↔ N (n + 1) ≤ N n := by
  unfold logGrowth
  rw [sub_nonpos, Real.log_le_log_iff (hN (n + 1)) (hN n)]

/-- **Boundedness from a non-positive growth rate** (no geometry).  If every step has
non-positive growth, the content is non-increasing, hence bounded.  So a repelling
(unbounded) invariant *must* show a strictly positive growth rate at some step. -/
theorem bounded_of_nonpos_logGrowth {N : ℕ → ℝ} (hN : ∀ k, 0 < N k)
    (h : ∀ n, logGrowth N n ≤ 0) : ∃ B, ∀ k, N k ≤ B :=
  ⟨N 0, fun k => by
    induction k with
    | zero => exact le_refl _
    | succ k ih => exact le_trans ((logGrowth_nonpos_iff hN k).mp (h k)) ih⟩

/-- **Unbounded content forces a strictly positive growth rate somewhere** (no
geometry).  Contrapositive of `bounded_of_nonpos_logGrowth`: the wall's repelling
side is read by the sign of the growth rate alone. -/
theorem exists_pos_logGrowth_of_unbounded {N : ℕ → ℝ} (hN : ∀ k, 0 < N k)
    (h : ¬ ∃ B, ∀ k, N k ≤ B) : ∃ n, 0 < logGrowth N n := by
  by_contra hc
  push Not at hc
  exact h (bounded_of_nonpos_logGrowth hN hc)

open Finset in
/-- **Telescoping (discrete BKM integral).**  The log of the content at step `n` is the
starting log plus the running sum of the growth rates.  This is the discrete analogue
of `log(content) = log(content_0) + int d/dt log(content) dt`. -/
theorem log_eq_sum_logGrowth {N : ℕ → ℝ} (n : ℕ) :
    Real.log (N n) = Real.log (N 0) + ∑ k ∈ range n, logGrowth N k := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [sum_range_succ, ← add_assoc, ← ih]
      unfold logGrowth
      ring

open Finset in
/-- **Bounded content ⟺ bounded running growth sum.**  If the running sum of the
growth rates is bounded above then the content is bounded (`exp` of a bounded quantity).
The discrete reading of the wall: no blow-up of the content without a blow-up of the
associated critical-content integral. -/
theorem bounded_of_bounded_sum_logGrowth {N : ℕ → ℝ} (hN : ∀ k, 0 < N k)
    (h : ∃ B, ∀ n, ∑ k ∈ range n, logGrowth N k ≤ B) :
    ∃ B', ∀ n, N n ≤ B' := by
  obtain ⟨B, hB⟩ := h
  refine ⟨Real.exp (Real.log (N 0) + B), fun n => ?_⟩
  have hlog : Real.log (N n) ≤ Real.log (N 0) + B := by
    have := hB n; linarith [log_eq_sum_logGrowth (N := N) n]
  calc N n = Real.exp (Real.log (N n)) := (Real.exp_log (hN n)).symm
    _ ≤ Real.exp (Real.log (N 0) + B) := Real.exp_le_exp.mpr hlog

open Finset in
/-- **Wall contrapositive.**  Unbounded content forces the running growth sum to be
unbounded (a diverging critical-content integral).  The repelling side of the wall is
exactly a non-summable growth rate. -/
theorem unbounded_sum_of_unbounded {N : ℕ → ℝ} (hN : ∀ k, 0 < N k)
    (h : ¬ ∃ B', ∀ n, N n ≤ B') :
    ¬ ∃ B, ∀ n, ∑ k ∈ range n, logGrowth N k ≤ B :=
  fun hB => h (bounded_of_bounded_sum_logGrowth hN hB)

/-- **C8, sign form.**  The growth of the critical content has the same sign as the
orientation. -/
theorem sign_match {r A : ℝ} (hr : 0 < r) (hA : 0 < A) (n : ℕ) :
    (0 < logGrowth (geometricOrbit r A) n) ↔ (0 < orientation r) := by
  rw [logGrowth_geometric hr hA n]

/-- **C8 + C9, model form.**  The (common) sign of the growth rate and the
orientation is exactly the wall: positive iff the invariant escapes every bound,
non-positive iff it is bounded.  This is `orientation_vs_invariant.py` as a theorem
on the model. -/
theorem orientation_reads_wall {r A : ℝ} (hr : 0 < r) (hA : 0 < A) (n : ℕ) :
    (0 < logGrowth (geometricOrbit r A) n ↔
        ¬ ∃ B : ℝ, ∀ k, geometricOrbit r A k ≤ B) ∧
    (logGrowth (geometricOrbit r A) n ≤ 0 ↔
        ∃ B : ℝ, ∀ k, geometricOrbit r A k ≤ B) := by
  simp only [logGrowth_geometric hr hA n, orientation, geometricOrbit]
  exact PunoCalculus.OrientationBoundedness.orientation_decides_boundedness hr hA

/-- **Continuous telescoping (continuous BKM integral).**  If `g` is the log-derivative
of the critical content `X` (`HasDerivAt (fun s => log (X s)) (g t) t`), then the
integral of the growth rate over `[0, T]` is the log of the content ratio.  The
continuous counterpart of `log_eq_sum_logGrowth`. -/
theorem contLogGrowth_integral {X g : ℝ → ℝ} {T : ℝ}
    (hderiv : ∀ t ∈ Set.uIcc 0 T, HasDerivAt (fun s => Real.log (X s)) (g t) t)
    (hcont : ContinuousOn g (Set.uIcc 0 T)) :
    ∫ t in (0)..T, g t = Real.log (X T) - Real.log (X 0) :=
  intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hcont.intervalIntegrable

/-- **Continuous content bound (provable part of C8-open).**  If the critical-content
integral `∫_0^T g` is bounded by `B`, then `X T ≤ X 0 * exp B`.  The continuous
analogue of `bounded_of_bounded_sum_logGrowth`: bounded content-integral ⇒ bounded
content.  Only the NS-specific bound on the growth rate `g` stays open (card C8-open). -/
theorem continuous_content_bounded {X g : ℝ → ℝ} {T B : ℝ}
    (hX0 : 0 < X 0) (hXT : 0 < X T)
    (hderiv : ∀ t ∈ Set.uIcc 0 T, HasDerivAt (fun s => Real.log (X s)) (g t) t)
    (hcont : ContinuousOn g (Set.uIcc 0 T))
    (hint : ∫ t in (0)..T, g t ≤ B) :
    X T ≤ X 0 * Real.exp B := by
  have hftc := contLogGrowth_integral hderiv hcont
  have hlog : Real.log (X T) ≤ Real.log (X 0) + B := by
    rw [hftc] at hint; linarith
  calc X T = Real.exp (Real.log (X T)) := (Real.exp_log hXT).symm
    _ ≤ Real.exp (Real.log (X 0) + B) := Real.exp_le_exp.mpr hlog
    _ = X 0 * Real.exp B := by rw [Real.exp_add, Real.exp_log hX0]

/-! ## The bounded orientation face

`boundedOrientation r = (r - 1) / (2 (r + 1))` (card C9) is a *bounded* reading of the
orientation.  It was a leaf; here it earns its keep as a consumer of the orientation law.
It carries the same sign as the named orientation `orientation r` -- closing the gap where
the bounded form and the register symbol were never explicitly linked -- it reads the sign
of the growth rate of a *general* positive sequence through its relative increment, and
along the geometric orbit it is a *bounded* coordinate that moves strictly with the orbit:
increasing when repelling, decreasing when attracting, pinned at the centre `r = 1`.  A
bounded monotone coordinate is exactly a Lyapunov function -- the reason a bounded
orientation is worth having at all (it can only ever read a fixed window `(-1/2, 1/2)` yet
still tracks the wall's side). -/

/-- **The bounded orientation carries the orientation's sign.**  `boundedOrientation` and
the register's named orientation `orientation r = log r` agree on positivity, at the
midpoint, and on negativity.  Explicit bridge between card C9's bounded window and card
C8's Lyapunov base. -/
theorem boundedOrientation_orientation_sign {r : ℝ} (hr : 0 < r) :
    (0 < boundedOrientation r ↔ 0 < orientation r) ∧
    (boundedOrientation r = 0 ↔ orientation r = 0) ∧
    (boundedOrientation r < 0 ↔ orientation r < 0) := by
  simpa only [orientation] using boundedOrientation_sign hr

/-- **The bounded orientation reads the growth rate of a general sequence.**  For any
positive `N`, the bounded orientation of its relative increment `N(n+1)/N n` has the same
sign as the growth rate `logGrowth N n`; no geometric assumption. -/
theorem boundedOrientation_ratio_sign {N : ℕ → ℝ} (hN : ∀ k, 0 < N k) (n : ℕ) :
    (0 < boundedOrientation (N (n + 1) / N n) ↔ 0 < logGrowth N n) ∧
    (boundedOrientation (N (n + 1) / N n) = 0 ↔ logGrowth N n = 0) ∧
    (boundedOrientation (N (n + 1) / N n) < 0 ↔ logGrowth N n < 0) := by
  have hpos : 0 < N (n + 1) / N n := div_pos (hN (n + 1)) (hN n)
  have hlog : Real.log (N (n + 1) / N n) = logGrowth N n := by
    unfold logGrowth
    rw [Real.log_div (ne_of_gt (hN (n + 1))) (ne_of_gt (hN n))]
  have h := boundedOrientation_sign hpos
  rw [hlog] at h
  exact h

/-- **The bounded orientation of the orbit is confined to the open window.**  Along
`N n = r^n` it always lies in `(-1/2, 1/2)`, for every positive `r`. -/
theorem boundedOrientation_geometricOrbit_mem {r : ℝ} (hr : 0 < r) (n : ℕ) :
    boundedOrientation (r ^ n) ∈ Set.Ioo (-(1 / 2)) (1 / 2) :=
  ⟨boundedOrientation_floor (pow_pos hr n), boundedOrientation_ceiling (pow_pos hr n)⟩

/-- **Repelling orbit: the bounded orientation strictly increases.**  For `1 < r` the
bounded coordinate of `r^n` is strictly increasing in `n` (a Lyapunov function climbing
toward the ceiling). -/
theorem boundedOrientation_geometricOrbit_strictMono {r : ℝ} (hr : 1 < r) :
    StrictMono (fun n : ℕ => boundedOrientation (r ^ n)) := by
  intro m n hmn
  exact boundedOrientation_strictMonoOn (pow_pos (lt_trans zero_lt_one hr) m)
    (pow_pos (lt_trans zero_lt_one hr) n) (pow_lt_pow_right₀ hr hmn)

/-- **Attracting orbit: the bounded orientation strictly decreases.**  For `0 < r < 1` it
strictly decreases in `n`. -/
theorem boundedOrientation_geometricOrbit_strictAnti {r : ℝ} (hr : 0 < r) (hr1 : r < 1) :
    StrictAnti (fun n : ℕ => boundedOrientation (r ^ n)) := by
  intro m n hmn
  exact boundedOrientation_strictMonoOn (pow_pos hr n) (pow_pos hr m)
    (pow_lt_pow_right_of_lt_one₀ hr hr1 hmn)

/-- **Centre: the bounded orientation is pinned.**  At `r = 1` the orbit is frozen and the
bounded orientation is identically `0`. -/
theorem boundedOrientation_geometricOrbit_center {r : ℝ} (hr : r = 1) (n : ℕ) :
    boundedOrientation (r ^ n) = 0 := by
  subst hr
  rw [one_pow, boundedOrientation_midpoint]

/-! ## Counterexample: naive uniqueness is false

The naive claim that center + antisymmetry + strict monotonicity + bounded in the window
forces a scalar multiple of `boundedOrientation` is false.  The following example satisfies
all four properties but is not a scalar multiple at `r=2,3`. -/

noncomputable def squareOrientation (r : ℝ) : ℝ := (r ^ 2 - 1) / (2 * (r ^ 2 + 1))

/-- `squareOrientation` is centered at `r=1`. -/
theorem squareOrientation_center : squareOrientation 1 = 0 := by
  norm_num [squareOrientation]

/-- `squareOrientation` maps positive reals into the open window. -/
theorem squareOrientation_mem {r : ℝ} (hr : 0 < r) :
    squareOrientation r ∈ Set.Ioo (-(1 / 2)) (1 / 2) := by
  have hpos : 0 < 2 * (r ^ 2 + 1) := by positivity
  refine ⟨?_, ?_⟩
  · rw [squareOrientation, lt_div_iff₀ hpos]
    nlinarith [sq_nonneg r]
  · rw [squareOrientation, div_lt_iff₀ hpos]
    nlinarith [sq_nonneg r]

/-- `squareOrientation` is strictly monotone on `(0, ∞)`. -/
theorem squareOrientation_strictMonoOn : StrictMonoOn squareOrientation (Set.Ioi (0 : ℝ)) := by
  intro r hr s hs hrs
  have hposr : 0 < 2 * (r ^ 2 + 1) := by positivity
  have hposs : 0 < 2 * (s ^ 2 + 1) := by positivity
  have hrs2 : r ^ 2 < s ^ 2 := pow_lt_pow_left₀ hrs (le_of_lt hr) (by norm_num)
  rw [squareOrientation, squareOrientation, div_lt_div_iff₀ hposr hposs]
  nlinarith [hrs2]

/-- `squareOrientation` satisfies the antisymmetry law `f(r⁻¹) = -f(r)`. -/
theorem squareOrientation_antisym {r : ℝ} (hr : 0 < r) :
    squareOrientation r⁻¹ = -squareOrientation r := by
  unfold squareOrientation
  field_simp
  ring

/-- The counterexample: no real `c` makes `squareOrientation` a scalar multiple of
`boundedOrientation` on all positive reals. -/
theorem squareOrientation_not_scalar_multiple_of_boundedOrientation :
    ¬ ∃ c : ℝ, ∀ r : ℝ, 0 < r → squareOrientation r = c * boundedOrientation r := by
  rintro ⟨c, hc⟩
  have h2 := hc 2 (by norm_num)
  have h3 := hc 3 (by norm_num)
  norm_num [squareOrientation, boundedOrientation] at h2 h3
  linarith

/-- Formalised-facts register for `OrientationLaw.lean`. -/
def orientationLawFacts : List String :=
  [ "logGrowth_of_ratio_eq", "logGrowth_geometric", "sign_match", "logGrowth_pos_iff",
    "logGrowth_nonpos_iff", "bounded_of_nonpos_logGrowth",
    "exists_pos_logGrowth_of_unbounded", "log_eq_sum_logGrowth",
    "bounded_of_bounded_sum_logGrowth", "unbounded_sum_of_unbounded",
    "contLogGrowth_integral", "continuous_content_bounded", "orientation_reads_wall",
    "boundedOrientation_orientation_sign", "boundedOrientation_ratio_sign",
    "boundedOrientation_geometricOrbit_mem", "boundedOrientation_geometricOrbit_strictMono",
    "boundedOrientation_geometricOrbit_strictAnti", "boundedOrientation_geometricOrbit_center" ]

/-- The register has exactly nineteen entries. -/
theorem orientationLawFacts_length : orientationLawFacts.length = 19 := by decide

end PunoCalculus.OrientationLaw
