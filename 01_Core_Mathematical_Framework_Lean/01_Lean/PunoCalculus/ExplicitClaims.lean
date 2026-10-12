import Mathlib
import PunoCalculus.CriticalLadder

/-!
# Explicit claims: the arithmetic cores, machine-checked

Companion to `EXPLICIT_CLAIMS.md`.  The register's shared insight is written down as
claim cards; the parts of those cards that are pure arithmetic are proved here so
they leave the prose column and become facts.

* `morrey_threshold` -- **C7.**  `H^1` embeds in `L^inf` iff the effective dimension
  is below `2` (`0 < 1 - d / 2 ↔ d < 2`).  This is the dimensional wall.
* `physical_embedding_gap` -- **C7 corollary.**  At physical `d = 3` the energy
  method is exactly half a derivative short: `1 - 3/2 = -1/2`.
* `extra_power_strengthens_above_unit` -- **C4/C6.**  The next-order term `Z^{1+eps}`
  is strictly stronger than `Z` exactly where enstrophy exceeds unit level
  (`z <= z^(1+eps) ↔ 1 <= z`); so `int Z^{1+eps} dt < inf` breaks the marginality
  precisely in the intermittent regime `Z > 1`.  (Sign of the square-root self-map
  of `EmergentTime`.)
* `mean_le_dimMixture` -- **C8.**  The dimension of a mixture is a sup, not a mean:
  `(d + e)/2 <= max d e`.  Averaging can never lower the effective dimension.

No PDE content; the analytic claims (boundedness C5, empirical C9/C10) stay OPEN and
are cited, not proved, in `EXPLICIT_CLAIMS.md`.
-/

noncomputable section

namespace PunoCalculus.ExplicitClaims

open PunoCalculus.CriticalLadder (sCrit)

/-- **C7.**  The Morrey dimension threshold: a unit-`H^1` bump sits in `L^inf`
exactly when its effective dimension is below `2`. -/
theorem morrey_threshold (d : ℝ) : 0 < 1 - d / 2 ↔ d < 2 := by
  constructor <;> intro h <;> linarith

/-- **C7 corollary.**  At physical dimension `d = 3` the `H^1 -> L^inf` gain needed
is `1 - 3/2 = -1/2`: the energy method is half a derivative short. -/
theorem physical_embedding_gap : (1 : ℝ) - 3 / 2 = -(1 / 2) := by norm_num

/-- **C4/C6.**  One extra power of enstrophy is the exactly-critical next-order term:
`z^(1+eps)` dominates `z` exactly where `z` exceeds unit level.  Hence
`int Z^{1+eps} dt < inf` is a genuinely stronger requirement than `int Z dt < inf`,
and it bites exactly in the intermittent / high-dimension regime `Z > 1`. -/
theorem extra_power_strengthens_above_unit {z ε : ℝ} (hz : 0 < z) (hε : 0 < ε) :
    z ≤ z ^ (1 + ε) ↔ 1 ≤ z := by
  have hpow : 1 ≤ z ^ ε ↔ 1 ≤ z := by
    simpa using (Real.rpow_le_rpow_iff (show (0 : ℝ) ≤ 1 by norm_num) hz.le hε)
  have hcanon : z ≤ z * z ^ ε ↔ 1 ≤ z ^ ε := by
    constructor
    · intro h
      exact le_of_mul_le_mul_left (by simpa using h) hz
    · intro h
      simpa using mul_le_mul_of_nonneg_left h hz.le
  rw [Real.rpow_add hz, Real.rpow_one, hcanon]
  exact hpow

/-- **C8.**  Dimension of a mixture is a sup, not a mean: the average never goes
below the sup, so adding a lower-dimensional bulk cannot lower the effective
dimension of a high-dimensional spike. -/
def dimMixture (d e : ℝ) : ℝ := max d e

theorem mean_le_dimMixture (d e : ℝ) : (d + e) / 2 ≤ dimMixture d e := by
  unfold dimMixture
  have h1 := le_max_left d e
  have h2 := le_max_right d e
  linarith

/-- Formalised-facts register for the explicit-claims brick. -/
def explicitClaimsFacts : List String :=
  [ "morrey_threshold"
  , "physical_embedding_gap"
  , "extra_power_strengthens_above_unit"
  , "mean_le_dimMixture" ]

/-- The register has exactly four entries. -/
theorem explicitClaimsFacts_length : explicitClaimsFacts.length = 4 := by decide

end PunoCalculus.ExplicitClaims
