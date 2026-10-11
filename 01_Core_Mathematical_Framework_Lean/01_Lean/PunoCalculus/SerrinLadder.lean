import Mathlib

/-!
# Serrin ladder arithmetic (formal)

The `serrin_ladder.py` probe verifies numerically that the energy + enstrophy
method controls `L^p` exactly for `p <= 6`, with Gagliardo-Nirenberg
interpolation exponent `theta(p) = 3/2 - 3/p`, ceiling `theta(6) = 1`
(Sobolev `H^1 -> L^6`).  This file machine-checks the *arithmetic* of that
ladder, in the same claim ceiling as `NavierStokes.lean`'s `serrinScaling`
(no PDE content here):

* the interpolation exponent at the ceiling, `theta(6) = 1`;
* the intercept `theta(2) = 0` (energy control only, no interpolation gain);
* the Serrin companion `q(6) = 4` and the critical-power arithmetic of the
  `(p, q) = (6, 4)` route: the quantity integrated along the flow is
  `Z^{theta * q / 2}`, which is `Z^2` at `(6, 4)`;
* the energy identity supplies only `Z^1`, so the exactly critical next order
  is ONE extra power of enstrophy (`2 - 1 = 1`).

Nothing here proves Navier-Stokes regularity: the wall `int Z^2 dt < inf`
and the excluded `p = 3` endpoint (which needs `L^inf`, the dimensional wall
of `dimension_threshold.py`) stay OPEN, exactly as in `NavierStokes.lean`
(`prodiSerrinIntegralFiniteCertified = false`, `nsGlobalRegularityOpen = true`).
-/

namespace PunoCalculus.SerrinLadder

noncomputable section

/-- The Gagliardo-Nirenberg interpolation exponent `theta(p) = 3/2 - 3/p`. -/
def gnExponent (p : ℝ) : ℝ := 3 / 2 - 3 / p

/-- At the critical `p = 6` (Sobolev `H^1 -> L^6`) the exponent reaches 1. -/
theorem gnExponent_six : gnExponent 6 = 1 := by
  norm_num [gnExponent]

/-- At `p = 2` (energy) the exponent is 0: no interpolation gain. -/
theorem gnExponent_two : gnExponent 2 = 0 := by
  norm_num [gnExponent]

/-- At `p = 3` the exponent is `1/2`: the Serrin endpoint `p = 3` needs more
than E,Z control (in fact `L^inf`), recorded as arithmetic, not implication. -/
theorem gnExponent_three_half : gnExponent 3 = 1 / 2 := by
  norm_num [gnExponent]

/-- The ladder climb above the ceiling: `theta(3) = 1/2 < 1 = theta(6) <
`theta(8)`; the ceiling `p = 6` separates controlled from uncontrolled. -/
theorem gnExponent_ceiling_chain :
    gnExponent 3 = 1 / 2 ∧ gnExponent 6 = 1 ∧ gnExponent 8 = 9 / 8 := by
  norm_num [gnExponent]

/-- Serrin-line companion `q(p) = 2p/(p-3)` obtained from `2/q + 3/p = 1`. -/
def serrinQ (p : ℝ) : ℝ := 2 * p / (p - 3)

/-- On the Serrin line at `p = 6`, the time exponent is `q = 4`. -/
theorem serrinQ_six : serrinQ 6 = 4 := by
  norm_num [serrinQ]

/-- `q(p) = 2p/(p-3)` lies exactly on the Serrin line for every admissible
`p`: `2 / q(p) + 3 / p = 1` (with `p ≠ 0` and `p ≠ 3`). -/
theorem serrinQ_line (hp0 : p ≠ 0) (_hp3 : p ≠ 3) :
    2 / serrinQ p + 3 / p = 1 := by
  unfold serrinQ
  field_simp [hp0, _hp3]
  ring

/-- The energy method closes exactly for `p <= 6`: `theta(p) <= 1`
iff `p <= 6`, for every positive `p`.  At `p = 6` this is the Sobolev
`H^1 -> L^6` ceiling (`gnExponent_six`); above it no E,Z control exists. -/
theorem gnExponent_le_one_iff (hp : 0 < p) : gnExponent p ≤ 1 ↔ p ≤ 6 := by
  have key : gnExponent p ≤ 1 ↔ 1 / 2 ≤ 3 / p := by
    unfold gnExponent
    constructor <;> intro h <;> nlinarith
  rw [key]
  constructor
  · intro hh
    have hm : (1 / 2) * p ≤ 3 := (le_div_iff₀ hp).mp hh
    nlinarith
  · intro hle
    have hm : (1 / 2) * p ≤ 3 := by nlinarith
    exact (le_div_iff₀ hp).mpr hm

/-- The quantity integrated along the flow on the `(p, q)` route is
`Z^{theta * q / 2}`; at `(6, 4)` this is `Z^2`. -/
theorem criticalPower_six_four : gnExponent 6 * serrinQ 6 / 2 = 2 := by
  norm_num [gnExponent, serrinQ]

/-- The energy identity supplies only `Z^1`; the exactly critical next order is
ONE extra power of enstrophy. -/
theorem oneExtraPower : (gnExponent 6 * serrinQ 6 / 2) - 1 = 1 := by
  norm_num [gnExponent, serrinQ]

/-- Closed form of the critical power: on the `(p, q(p))` Serrin route the
quantity integrated along the flow is `Z^{3(p-2)/(2(p-3))}`; at `p = 6` this
is `Z^2` (`criticalPower_six_four`). -/
theorem criticalPowerIdentity (hp0 : p ≠ 0) (hp3 : p ≠ 3) :
    gnExponent p * serrinQ p / 2 = 3 * (p - 2) / (2 * (p - 3)) := by
  unfold gnExponent serrinQ
  field_simp [hp0, hp3]

/-- The offered power `1 + eps` closes the `(6, 4)` route exactly when
`eps >= 1`: the remaining gap is ONE more power of enstrophy (or its
Besov/Lorentz generalisation).  Whether any such power actually integrates
along the flow is a separate, OPEN question -- `extraEnstrophyPowerIntegralOpen`. -/
theorem powerClosesCriticalAtSix :
    (1 + eps ≥ gnExponent 6 * serrinQ 6 / 2 ↔ 1 ≤ eps) := by
  rw [criticalPower_six_four]
  constructor <;> intro h <;> nlinarith

/-- OPEN WALL MARKER (not a theorem): whether any `Z^{1+eps}` power with
`eps >= 0` actually integrates along the flow stays unproved, in the same
style as `NavierStokes.lean`'s `prodiSerrinIntegralFiniteCertified = false`. -/
def extraEnstrophyPowerIntegralOpen : Prop := True

/-- Statement-grade inventory of the ladder file. -/
def ladderFormalizedFacts : List String :=
  ["theta(p) <= 1 iff p <= 6 (p > 0): energy method closes exactly at the Sobolev ceiling (machine-checked)",
   "theta(6) = 1: Sobolev H^1 -> L^6 ceiling; theta(3) = 1/2, theta(2) = 0, theta(8) = 9/8 (machine-checked)",
   "Serrin companion q(p) = 2p/(p-3) lies on the Serrin line 2/q + 3/p = 1; q(6) = 4 (machine-checked)",
   "Serrin (p, q) = (6, 4): integrated quantity is Z^2 (machine-checked)",
   "energy identity gives only Z^1: ONE extra power of enstrophy",
   "critical power closed form: theta(p)*q(p)/2 = 3(p-2)/(2(p-3)); at p = 6 exactly Z^2 (machine-checked)",
   "gap conditional arithmetic: the offered power 1+eps closes the (6, 4) route iff eps >= 1; whether any such power integrates is OPEN (marker extraEnstrophyPowerIntegralOpen)",
   "wall stays OPEN: int Z^2 < infinity and the p = 3 endpoint (L^inf)"]

/-- The inventory has exactly eight entries. -/
theorem ladderFormalizedFacts_length : ladderFormalizedFacts.length = 8 := by
  decide

end

end PunoCalculus.SerrinLadder