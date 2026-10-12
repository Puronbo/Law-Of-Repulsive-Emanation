import Mathlib
import PunoCalculus.OrientationBoundedness

/-!
# Orientation law: the growth rate equals the orientation (C10, model core)

Card **C10** of `EXPLICIT_CLAIMS.md` claims `sign(lambda) = sign(mu)`, where `lambda`
is the orbit's Lyapunov base (the *orientation*) and `mu = d/dt log(critical content)`
is the growth rate.  Empirically it holds in four systems (`orientation_vs_invariant.py`).
Its *model core* is a theorem, and that is what this brick proves.

On the geometric orbit `N n = r ^ n * A` (the exact model of `OrientationBoundedness`),
the discrete growth rate

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

/-- **C10 model core: `mu == lambda`.**  On the geometric orbit the growth rate is
constant and equals the orientation `log r`. -/
theorem logGrowth_geometric {r A : ℝ} (hr : 0 < r) (hA : 0 < A) (n : ℕ) :
    logGrowth (geometricOrbit r A) n = orientation r := by
  have hpos : 0 < r ^ n * A := mul_pos (pow_pos hr n) hA
  unfold logGrowth orientation geometricOrbit
  have hrec : r ^ (n + 1) * A = r * (r ^ n * A) := by rw [pow_succ]; ring
  rw [hrec, Real.log_mul (ne_of_gt hr) (ne_of_gt hpos)]
  ring

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

/-- Formalised-facts register for `OrientationLaw.lean`. -/
def orientationLawFacts : List String :=
  [ "logGrowth_geometric", "sign_match", "orientation_reads_wall" ]

/-- The register has exactly three entries. -/
theorem orientationLawFacts_length : orientationLawFacts.length = 3 := by decide

end PunoCalculus.OrientationLaw
