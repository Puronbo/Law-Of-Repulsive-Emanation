import Mathlib

/-!
# Attracting implies bounded: the sufficiency half for the general mechanism

The open wall is BOUNDEDNESS of the scaling-critical invariant.  Two shapes of
"boundedness for free" appear in the register:

* the *continuation* shape (`PunoCalculus.ContinuationCriterion`): while the
  invariant stays bounded one can extend existence, so blowup forces unboundedness;
* the *attracting* shape, formalised here: an orbit under an attracting
  (contracting) map is not merely bounded but convergent.

The on-flow bridge (`orientation_vs_invariant.py`) showed the sign of the measured
orientation equals the sign of the growth rate of the critical content, and that
the attracting regime is exactly the one where the critical content shrinks.  This
file makes the attracting side a theorem: a contracting self-map of a complete
space has a bounded (indeed convergent) orbit -- repulsion is the only way the
orbit can escape.  So "the great attractor does not yet repel" is, formally, a
boundedness statement.
-/

namespace PunoCalculus.StableBounded

open Filter
open scoped Topology

/-- **Attracting orbits are convergent (hence bounded).**  If `f` is a contraction
(`ContractingWith K f`, `K < 1`) on a complete space, then the orbit of any point
converges to the fixed point. -/
theorem attracting_orbit_converges
    {α : Type*} [MetricSpace α] [CompleteSpace α] [Nonempty α]
    {K : NNReal} (_hK : K < 1) {f : α → α} (hf : ContractingWith K f) (x : α) :
    Tendsto (fun n : ℕ => f^[n] x) atTop (𝓝 (hf.fixedPoint f)) :=
  hf.tendsto_iterate_fixedPoint x

/-- **Attracting orbits are bounded.**  The range of an attracting orbit is bounded —
the direct formal content of "it shrinks itself" (`GreatAttractor.fixedPoint_attracts`):
an attracting map cannot push the orbit past any bound. -/
theorem attracting_orbit_bounded
    {α : Type*} [MetricSpace α] [CompleteSpace α] [Nonempty α]
    {K : NNReal} (hK : K < 1) {f : α → α} (hf : ContractingWith K f) (x : α) :
    Bornology.IsBounded (Set.range fun n : ℕ => f^[n] x) :=
  Metric.isBounded_range_of_tendsto _ (attracting_orbit_converges hK hf x)

/-- **Monotone non-increasing is bounded by its initial value.**  The arithmetic
core of the Lyapunov/2D-enstrophy shape: if a nonnegative quantity never increases,
it stays below its start.  This is the "boundedness for free" available in 2D
(`Z` non-increasing) that is *not* available in 3D. -/
theorem monotone_bounded {N : ℕ → ℝ} (hN : Antitone N) (t : ℕ) : N t ≤ N 0 :=
  hN (Nat.zero_le t)

/-- Formalised-facts register for `StableBounded.lean`. -/
def stableBoundedFacts : List String :=
  [ "attracting_orbit_converges", "attracting_orbit_bounded", "monotone_bounded" ]

/-- The register has exactly three entries. -/
theorem stableBoundedFacts_length : stableBoundedFacts.length = 3 := by decide

end PunoCalculus.StableBounded
