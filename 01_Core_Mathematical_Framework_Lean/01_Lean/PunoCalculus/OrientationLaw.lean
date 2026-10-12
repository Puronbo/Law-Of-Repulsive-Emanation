import Mathlib
import PunoCalculus.OrientationBoundedness

/-!
# Orientation law: the growth rate equals the orientation (C10, model core)

Card **C10** of `EXPLICIT_CLAIMS.md` claims `sign(lambda) = sign(mu)`, where `lambda`
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
identification survives the real flow (card C10 proper) stays empirical/OPEN.
-/

noncomputable section

namespace PunoCalculus.OrientationLaw

/-- The geometric orbit `N n = r ^ n * A` (same model as `OrientationBoundedness`). -/
def geometricOrbit (r A : ℝ) (n : ℕ) : ℝ := r ^ n * A

/-- The orientation `lambda = log r` (Lyapunov base of the orbit). -/
def orientation (r : ℝ) : ℝ := Real.log r

/-- Discrete log-growth rate `mu(n) = log(N(n+1)) - log(N n)` of a positive sequence:
the finite-difference reading of `d/dt log(content)`. -/
def logGrowth (N : ℕ → ℝ) (n : ℕ) : ℝ := Real.log (N (n + 1)) - Real.log (N n)

/-- **General growth law.**  For any positive sequence whose *relative increment* is
the constant `r` (`N (n+1) = r * N n`), the growth rate is `log r`.  The geometric
orbit is the special case `A * r^n`; this is the honest model form of C10 -- the
growth rate of the content is the log of its relative increment. -/
theorem logGrowth_of_ratio_eq {N : ℕ → ℝ} (hN : ∀ k, 0 < N k) {r : ℝ} (hr : 0 < r)
    (h : ∀ n, N (n + 1) = r * N n) (n : ℕ) : logGrowth N n = Real.log r := by
  unfold logGrowth
  rw [h n, Real.log_mul (ne_of_gt hr) (ne_of_gt (hN n))]
  ring

/-- **C10 model core: `mu == lambda`.**  On the geometric orbit the growth rate is
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

/-- **C10, sign form.**  The growth of the critical content has the same sign as the
orientation. -/
theorem sign_match {r A : ℝ} (hr : 0 < r) (hA : 0 < A) (n : ℕ) :
    (0 < logGrowth (geometricOrbit r A) n) ↔ (0 < orientation r) := by
  rw [logGrowth_geometric hr hA n]

/-- **C10 + C11, model form.**  The (common) sign of the growth rate and the
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

/-- **Continuous content bound (provable part of C10-open).**  If the critical-content
integral `∫_0^T g` is bounded by `B`, then `X T ≤ X 0 * exp B`.  The continuous
analogue of `bounded_of_bounded_sum_logGrowth`: bounded content-integral ⇒ bounded
content.  Only the NS-specific bound on the growth rate `g` stays open (card C10-open). -/
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

/-- Formalised-facts register for `OrientationLaw.lean`. -/
def orientationLawFacts : List String :=
  [ "logGrowth_of_ratio_eq", "logGrowth_geometric", "sign_match", "logGrowth_pos_iff",
    "logGrowth_nonpos_iff", "bounded_of_nonpos_logGrowth",
    "exists_pos_logGrowth_of_unbounded", "log_eq_sum_logGrowth",
    "bounded_of_bounded_sum_logGrowth", "unbounded_sum_of_unbounded",
    "contLogGrowth_integral", "continuous_content_bounded", "orientation_reads_wall" ]

/-- The register has exactly thirteen entries. -/
theorem orientationLawFacts_length : orientationLawFacts.length = 13 := by decide

end PunoCalculus.OrientationLaw
