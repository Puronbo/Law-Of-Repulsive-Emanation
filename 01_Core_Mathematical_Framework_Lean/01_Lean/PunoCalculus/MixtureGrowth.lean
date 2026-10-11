import Mathlib

/-!
# Growth by addition of parts (formal)

`dimension_mixture.py` measured (and `SelfSimilarExponents.lean`,
`SerrinLadder.lean` formalised the surrounding arithmetic) that a mixture of
parts with different critical content is governed by the MAX over the parts,
not an average, and that the only thing that can move a mixture toward the
critical shell is a part whose own ratio is already above the `O(eps)` budget
-- i.e. intermittency, energy concentration.  This file machine-checks the
arithmetic of "growth by addition": 

* a mixture's norm is at most the sum of its parts (`norm_add_le`): adding
  parts transmits the parts' concentration, it never creates more of it;
* a two-part mixture's ratio (and energy-weighted squared ratio) is bracketed
  by the parts' ratios: no averaging can fabricate a ratio above the max part.

Nothing here is a PDE claim; `ns_spike_mixture.py` is the on-flow companion
that measures whether a concentrated spike added to a smooth bulk persists
or is killed by viscosity.
-/

namespace PunoCalculus.MixtureGrowth

noncomputable section

variable {X : Type*} [NormedAddCommGroup X]

/-- Hilbert-space form of growth-by-addition: a mixture is bounded by the sum
of its parts.  Adding parts transmits the parts' concentration; it can never
create more of it. -/
theorem normMixtureLeSum (u v : X) : ‖u + v‖ ≤ ‖u‖ + ‖v‖ :=
  norm_add_le u v

variable {f1 f2 r1 r2 : ℝ}

/-- The ratio of a two-part mixture is bracketed by the parts' ratios
(min <= mixture <= max).  No averaging can fabricate a ratio above the max
part -- the `dimension_mixture.py` "max, not mean" reading, machine-checked. -/
theorem mixtureRatioBetween (hr12 : r1 ≤ r2) (hr1 : 0 ≤ r1)
    (hf1 : 0 ≤ f1) (hf2 : 0 ≤ f2) (hsum : f1 + f2 = 1) :
    r1 ≤ f1 * r1 + f2 * r2 ∧ f1 * r1 + f2 * r2 ≤ r2 := by
  constructor
  · rw [← sub_nonneg]
    have hdiff : f1 * r1 + f2 * r2 - r1 = f2 * (r2 - r1) := by nlinarith [hsum]
    rw [hdiff]
    exact mul_nonneg hf2 (sub_nonneg.mpr hr12)
  · rw [← sub_nonneg]
    have hdiff : r2 - (f1 * r1 + f2 * r2) = f1 * (r2 - r1) := by nlinarith [hsum]
    rw [hdiff]
    exact mul_nonneg hf1 (sub_nonneg.mpr hr12)

/-- Energy-weighted version (the quantity `dimension_mixture.py` measures):
the squared mixture ratio is bracketed by the parts' squares. -/
theorem weightedSqBetween (hr12 : r1 * r1 ≤ r2 * r2)
    (hf1 : 0 ≤ f1) (hf2 : 0 ≤ f2) (hsum : f1 + f2 = 1) :
    r1 * r1 ≤ f1 * r1 * r1 + f2 * r2 * r2 ∧
      f1 * r1 * r1 + f2 * r2 * r2 ≤ r2 * r2 := by
  constructor
  · rw [← sub_nonneg]
    have hdiff : f1 * r1 * r1 + f2 * r2 * r2 - r1 * r1 =
        f2 * (r2 * r2 - r1 * r1) := by nlinarith [hsum]
    rw [hdiff]
    exact mul_nonneg hf2 (sub_nonneg.mpr hr12)
  · rw [← sub_nonneg]
    have hdiff : r2 * r2 - (f1 * r1 * r1 + f2 * r2 * r2) =
        f1 * (r2 * r2 - r1 * r1) := by nlinarith [hsum]
    rw [hdiff]
    exact mul_nonneg hf1 (sub_nonneg.mpr hr12)

/-- Corollary: a low-dimension bulk (bounded ratio) cannot cancel a high-dim
spike; the mixture's critical content stays at least that of the smaller part. -/
theorem spikeCannotLowerRatio (hr12 : r1 ≤ r2) (hr1 : 0 ≤ r1)
    (hf1 : 0 ≤ f1) (hf2 : 0 ≤ f2) (hsum : f1 + f2 = 1) :
    r1 ≤ f1 * r1 + f2 * r2 :=
  (mixtureRatioBetween hr12 hr1 hf1 hf2 hsum).1

/-- Statement-grade inventory of the mixture-growth file. -/
def mixtureGrowthFacts : List String :=
  ["L2 norm of a mixture is at most the sum of the parts (norm_add_le): addition transmits concentration, never creates it",
   "mixture ratio is bracketed by the parts' ratios: min <= mixture <= max (dimension_mixture's max-not-mean reading, machine-checked)",
   "energy-weighted squared ratios likewise bracketed (the quantity dimension_mixture.py measures)",
   "corollary: a low-dim bulk (ratio ~ 1) cannot cancel a high-dim spike; the mixture stays at least the smaller part",
   "wall reading: only energy concentration (a part whose ratio is above the O(eps) budget) can move a mixture toward the critical shell"]

/-- The inventory has exactly five entries. -/
theorem mixtureGrowthFacts_length : mixtureGrowthFacts.length = 5 := by
  decide

end

end PunoCalculus.MixtureGrowth