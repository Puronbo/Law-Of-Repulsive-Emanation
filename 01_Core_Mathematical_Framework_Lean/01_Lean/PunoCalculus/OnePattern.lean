import PunoCalculus.GreatAttractor

/-!
# The one pattern: every critical exponent is the ladder, shifted by the order

This is the synthesis brick.  Every brick in this register has been a special
case of a single object: a **removable `0/0` of finite order, oriented by one
responsive number.**  Two knobs organize every wall:

* **order** `a` (how many zeros) — it slides the critical rung; and
* **orientation** `L` (the local multiplier) — its magnitude decides whether the
  point repels (`|L| > 1`) or attracts (`|L| < 1`).

Here we make the *order* half of that statement one line: the critical
smoothness `criticalSmoothness a p = 3/p - a` is a **one-parameter family
through the register ladder**,

    criticalSmoothness a p = sCrit p + (1 - a),

so every guise of the critical object is the order-one rung `sCrit` shifted by
the order.  The recurrence identity `theta + criticalSmoothness a = 1/2 + (1 - a)`
generalises `CriticalLadder.thetaAddSCrit` and collapses to it at order one.  The
homogeneous norm is scale-free exactly on this family.  The *orientation* half is
`GreatAttractor.fixedPoint_logSign` (`sign log|L| = orientation`).  Two numbers,
one pattern.
-/

noncomputable section

namespace PunoCalculus.OnePattern

open PunoCalculus.GreatAttractor (criticalSmoothness scalingWeight)
open PunoCalculus.CriticalLadder (sCrit)
open PunoCalculus.SerrinLadder (gnExponent)

/-- **One pattern, one line.**  The critical smoothness of an object of order `a`
in `L^p` is exactly the register ladder `sCrit p` shifted by `1 - a`: every form
of the scaling-critical object is the order-one rung translated by the order. -/
theorem criticalCurve_through_ladder (a p : ℝ) :
    criticalSmoothness a p = sCrit p + (1 - a) := by
  unfold criticalSmoothness sCrit
  ring

/-- The register's scaling-critical ladder is the **order-one** member of the
family. -/
theorem ladder_is_order_one (p : ℝ) : criticalSmoothness 1 p = sCrit p := by
  rw [criticalCurve_through_ladder]
  ring

/-- **One-pattern recurrence identity.**  The Serrin interpolation exponent plus
the order-`a` critical smoothness is the order-independent constant
`1/2 + (1 - a)`: the same identity recurs at every order. -/
theorem theta_add_criticalCurve (hp : p ≠ 0) (a : ℝ) :
    gnExponent p + criticalSmoothness a p = 1 / 2 + (1 - a) := by
  rw [criticalCurve_through_ladder]
  have h := PunoCalculus.CriticalLadder.thetaAddSCrit (p := p) hp
  linarith

/-- At order one the recurrence identity is exactly `thetaAddSCrit`. -/
theorem theta_add_criticalCurve_one (hp : p ≠ 0) :
    gnExponent p + criticalSmoothness 1 p = 1 / 2 := by
  rw [theta_add_criticalCurve hp 1]
  ring

/-- The homogeneous norm is scale-free exactly on the family: the scaling weight
`a + s - 3/p` vanishes at `s = criticalSmoothness a p`, for every order `a`. -/
theorem scalingWeight_vanishes_family (a p : ℝ) :
    scalingWeight (criticalSmoothness a p) a p = 0 := by
  unfold scalingWeight criticalSmoothness
  ring

/-- The formalised facts of this synthesis brick. -/
def onePatternFacts : List String :=
  [ "criticalCurve_through_ladder"
  , "ladder_is_order_one"
  , "theta_add_criticalCurve"
  , "theta_add_criticalCurve_one"
  , "scalingWeight_vanishes_family" ]

/-- The register has exactly five entries. -/
theorem onePatternFacts_length : onePatternFacts.length = 5 := by decide

end PunoCalculus.OnePattern
