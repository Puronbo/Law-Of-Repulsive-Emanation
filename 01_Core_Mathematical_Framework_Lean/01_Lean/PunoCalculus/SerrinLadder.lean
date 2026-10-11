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

/-- The quantity integrated along the flow on the `(p, q)` route is
`Z^{theta * q / 2}`; at `(6, 4)` this is `Z^2`. -/
theorem criticalPower_six_four : gnExponent 6 * serrinQ 6 / 2 = 2 := by
  norm_num [gnExponent, serrinQ]

/-- The energy identity supplies only `Z^1`; the exactly critical next order is
ONE extra power of enstrophy. -/
theorem oneExtraPower : (gnExponent 6 * serrinQ 6 / 2) - 1 = 1 := by
  norm_num [gnExponent, serrinQ]

/-- Statement-grade inventory of the ladder file. -/
def ladderFormalizedFacts : List String :=
  ["theta(6) = 1: Sobolev H^1 -> L^6 ceiling (machine-checked)",
   "theta(3) = 1/2, theta(2) = 0, theta(8) = 9/8 (machine-checked)",
   "Serrin (p, q) = (6, 4): integrated quantity is Z^2 (machine-checked)",
   "energy identity gives only Z^1: ONE extra power of enstrophy",
   "wall stays OPEN: int Z^2 < infinity and the p = 3 endpoint (L^inf)"]

/-- The inventory has exactly five entries. -/
theorem ladderFormalizedFacts_length : ladderFormalizedFacts.length = 5 := by
  native_decide

end

end PunoCalculus.SerrinLadder