import Mathlib
import PunoCalculus.OrientationLaw

/-!
# Information bridge: the two-state (bit) instance of the Landauer–register schema

The note `LANDAUER_BOUND_AND_THE_REGISTER.md` states an **OPEN** claim: that
there is a map `Phi` from register states `(order a, orientation r, removable
value lambda)` to thermodynamic states carrying the Landauer cost.  This brick
does **not** construct `Phi`.  It formalises only the *arithmetic* of the
simplest instance -- the **two-state (bit) register** -- and ties it to the
register's own orientation sign:

* the fair bit carries `log 2` nats (`binaryEntropy_half`);
* resetting an `n`-state register costs `k_B T log n`, and for the bit
  `k_B T log 2` (`resetCost_two`);
* that cost is the **negative** orientation, scaled: `k_B T log n = -k_B T *
  orientation (1/n)` (`resetCost_eq_neg_orientation`), so a dissipative reset
  (`orientation (1/n) <= 0`, `orientation_reset_nonpos`) has non-negative cost.

The Landauer *bound* `k_B T log 2` is a physical input (Landauer, 1961; cited),
**not** derived here.  What is machine-checked is the exact arithmetic sharing the
constant `log 2` and the sign identity `cost = -k_B T * orientation`.  The
physical map `Phi` (a register-to-thermodynamics instantiation) remains the named
missing entity of the OPEN claim.  No Millennium problem is touched.
-/

noncomputable section

namespace PunoCalculus.InformationBridge

open PunoCalculus.OrientationLaw (orientation)

/-- Shannon entropy (nats) of a Bernoulli(`p`) bit. -/
def binaryEntropy (p : ℝ) : ℝ := -(p * Real.log p + (1 - p) * Real.log (1 - p))

/-- **A fair bit carries `log 2` nats.**  The binary entropy at `p = 1/2` is
`log 2`, the same constant as the Landauer cost of one bit. -/
theorem binaryEntropy_half : binaryEntropy (1 / 2) = Real.log 2 := by
  unfold binaryEntropy
  have hlog : Real.log ((1 : ℝ) / 2) = -Real.log 2 := by
    rw [one_div, Real.log_inv]
  rw [show (1 : ℝ) - 1 / 2 = 1 / 2 by norm_num, hlog]
  ring

/-- Minimum cost (work/heat) to reset an `n`-state register to a single state:
`k_B * T * log n` (Landauer's state-counting form). -/
def resetCost (kB T n : ℝ) : ℝ := kB * T * Real.log n

/-- **The bit case.**  Resetting a two-state register costs `k_B T log 2`. -/
theorem resetCost_two (kB T : ℝ) : resetCost kB T 2 = kB * T * Real.log 2 := by
  unfold resetCost
  rfl

/-- **Cost is minus the (scaled) orientation.**  The reset cost of an `n`-state
register is `-k_B T * orientation (1/n)`, since `orientation (1/n) = log (1/n) =
-log n`.  This is the algebraic link between the register's orientation sign and
the thermodynamic cost. -/
theorem resetCost_eq_neg_orientation (kB T n : ℝ) :
    resetCost kB T n = -kB * T * orientation (1 / n) := by
  unfold resetCost orientation
  rw [one_div, Real.log_inv]
  ring

/-- **A reset is dissipative in the register's sense.**  For any `n >= 1`, the
reset orientation `1/n` lies on the dissipative side: `log (1/n) <= 0`. -/
theorem orientation_reset_nonpos {n : ℕ} (hn : 1 ≤ n) :
    orientation (1 / (n : ℝ)) ≤ 0 := by
  have hnpos : (0 : ℝ) < (n : ℝ) := by
    have : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
    linarith
  have hpos : (0 : ℝ) < 1 / (n : ℝ) := by positivity
  have hle : (1 : ℝ) / (n : ℝ) ≤ 1 := by
    rw [div_le_iff₀ hnpos]
    simpa using (show (1 : ℝ) ≤ (n : ℝ) by exact_mod_cast hn)
  rw [orientation, ← Real.log_one]
  exact (Real.log_le_log_iff hpos (by norm_num)).mpr hle

/-- Formalised-facts register for `InformationBridge.lean`. -/
def informationBridgeFacts : List String :=
  [ "binaryEntropy_half", "resetCost_two", "resetCost_eq_neg_orientation",
    "orientation_reset_nonpos" ]

/-- The register has exactly four entries. -/
theorem informationBridgeFacts_length : informationBridgeFacts.length = 4 := by decide

end PunoCalculus.InformationBridge
