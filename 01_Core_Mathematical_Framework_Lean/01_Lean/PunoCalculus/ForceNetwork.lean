import Mathlib

/-!
# Change as interconnected force; each part held by inertia

Reading (L.O.R.E., `PAPER.md` §4-5): *change is everything interconnected in
force, each of which is a collection of points in space held by inertia.*  On a
spectral Navier-Stokes flow this is literal, and this file machine-checks its
arithmetic side:

* a collection of inertial parts coupled by any (nonnegative) interconnection
  weights has an aggregate "change value" **between the smallest and largest
  part** -- interconnection reweights, it can never mint a value outside its
  parts (`networkValueBetween`, generalising `MixtureGrowth.mixtureRatioBetween`
  from two parts to an arbitrary finite network);
* for a nonnegative force the induced change `force / inertia` is **antitone in
  the inertia** -- a part held by more inertia changes less
  (`inertiaDampsChange`).

The on-flow companion `ns_force_network.py` identifies the nodes (wavenumber
shells = collections of points in space), the inertia (shell energy), and the
interconnection force (nonlinear triad transfer), and measures that the network
is conservative and distributed and that heavier shells change less.  Nothing
here is a PDE claim; the wall stays OPEN.
-/

open scoped BigOperators

namespace PunoCalculus.ForceNetwork

noncomputable section

/-- If every part's change-value is at most `C`, then so is any inertia-weighted
average of the parts: interconnection (weighting) cannot concentrate a value
above the largest part. -/
theorem weightedValueLeMax {ι : Type*} (s : Finset ι) (w c : ι → ℝ) (C : ℝ)
    (hw : ∀ i ∈ s, 0 ≤ w i) (hsum : ∑ i ∈ s, w i = 1)
    (hc : ∀ i ∈ s, c i ≤ C) :
    ∑ i ∈ s, w i * c i ≤ C := by
  have h1 : ∑ i ∈ s, w i * C = C := by
    rw [← Finset.sum_mul, hsum, one_mul]
  rw [← h1]
  exact Finset.sum_le_sum (fun i hi => mul_le_mul_of_nonneg_left (hc i hi) (hw i hi))

/-- If every part's change-value is at least `c0`, then so is any inertia-weighted
average of the parts. -/
theorem leWeightedValueMin {ι : Type*} (s : Finset ι) (w c : ι → ℝ) (c0 : ℝ)
    (hw : ∀ i ∈ s, 0 ≤ w i) (hsum : ∑ i ∈ s, w i = 1)
    (hc : ∀ i ∈ s, c0 ≤ c i) :
    c0 ≤ ∑ i ∈ s, w i * c i := by
  have h1 : c0 = ∑ i ∈ s, w i * c0 := by
    rw [← Finset.sum_mul, hsum, one_mul]
  rw [h1]
  exact Finset.sum_le_sum (fun i hi => mul_le_mul_of_nonneg_left (hc i hi) (hw i hi))

/-- The network value of an interconnected (weighted) collection of inertial
parts lies between the smallest and largest part: a network reweights, it
cannot mint a value outside its parts. -/
theorem networkValueBetween {ι : Type*} (s : Finset ι) (w c : ι → ℝ) (c0 C : ℝ)
    (hw : ∀ i ∈ s, 0 ≤ w i) (hsum : ∑ i ∈ s, w i = 1)
    (hlo : ∀ i ∈ s, c0 ≤ c i) (hhi : ∀ i ∈ s, c i ≤ C) :
    c0 ≤ ∑ i ∈ s, w i * c i ∧ ∑ i ∈ s, w i * c i ≤ C :=
  ⟨leWeightedValueMin s w c c0 hw hsum hlo,
   weightedValueLeMax s w c C hw hsum hhi⟩

/-- Inertia damps change: for a nonnegative force, the induced change
`force / inertia` is antitone in the inertia -- a part held by more inertia
changes less. -/
theorem inertiaDampsChange {F I0 I : ℝ} (hF : 0 ≤ F) (hI0 : 0 < I0)
    (hI : I0 ≤ I) : F / I ≤ F / I0 := by
  have hIpos : 0 < I := lt_of_lt_of_le hI0 hI
  have h : 0 ≤ F / I0 - F / I := by
    field_simp
    nlinarith [hF, hI, hI0]
  linarith

/-- Statement-grade inventory of the force-network file. -/
def forceNetworkFacts : List String :=
  ["a weighted (interconnected) collection's value is at most the largest part: interconnection cannot concentrate (weightedValueLeMax)",
   "and at least the smallest part: the network value lies between min and max of the parts (networkValueBetween)",
   "inertia damps change: change = force/inertia is antitone in inertia -- a part held by more inertia changes less (inertiaDampsChange)",
   "reading: change is interconnection-mediated (force) but weighting only reweights -- it cannot mint a value outside the parts",
   "on-flow companion ns_force_network.py: the nonlinear interconnection is conservative (sum_m T_m ~ 0), distributed (high participation ratio), and heavier shells change less per unit inertia",
   "wall reading: concentration must come from a part already above the budget; the network cannot fabricate it"]

/-- The inventory has exactly six entries. -/
theorem forceNetworkFacts_length : forceNetworkFacts.length = 6 := by
  decide

end

end PunoCalculus.ForceNetwork
