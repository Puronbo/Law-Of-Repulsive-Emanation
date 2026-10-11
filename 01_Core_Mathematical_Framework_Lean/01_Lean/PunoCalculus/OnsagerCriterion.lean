import Mathlib

/-!
# The Onsager excess criterion: sufficiency skeleton and its contrapositive

The open wall is BOUNDEDNESS of the scaling-critical invariant along the flow.
Classically, *if* that invariant moment is bounded, a positive Onsager excess is
free: the supercritical moment `sum Z^{n+1}` is controlled by `M^n · sum Z`.  This
file formalises exactly that sufficiency skeleton (the inequality the missing
brick must be fed into), together with its contrapositive — the *wall*: an
Onsager-violating cascade forces the invariant moment `Z` to exceed its presumed
bound `M` somewhere.

The excess order `n` is one more instance of the register's one pattern: a
nonnegative "order" that shifts which moment is controlled, exactly as the order
of vanishing shifts the critical rung (`PunoCalculus.OnePattern`).
-/

namespace PunoCalculus.OnsagerCriterion

open Finset

/-- **Excess criterion (sufficiency skeleton).**  If the enstrophy `Z` is
uniformly bounded by `M` on the sample set `s`, then for every excess order `n`
the supercritical moment `sum Z^{n+1}` is controlled by `M^n · sum Z`.  A positive
Onsager excess is thus *free* once the invariant moment is bounded — which is
exactly the boundedness the wall fails to supply. -/
theorem weighted_sum_le {ι : Type*} (Z : ι → ℝ) (s : Finset ι) (n : ℕ) (M : ℝ)
    (hZ : ∀ t ∈ s, 0 ≤ Z t) (hM : ∀ t ∈ s, Z t ≤ M) :
    (∑ t ∈ s, Z t ^ (n + 1)) ≤ M ^ n * ∑ t ∈ s, Z t := by
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro t ht
  rw [pow_succ]
  exact mul_le_mul_of_nonneg_right (pow_le_pow_left₀ (hZ t ht) (hM t ht) n) (hZ t ht)

/-- **The wall, contrapositive.**  If the supercritical moment exceeds the
invariant bound `M^n · sum Z`, then the enstrophy must exceed `M` somewhere on
`s`: an excess-spike cascade cannot live beneath a bounded invariant.  This is the
precise shape of what stays OPEN — producing that spike (or ruling it out in the
singular limit) is the missing brick. -/
theorem spike_of_excess {ι : Type*} (Z : ι → ℝ) (s : Finset ι) (n : ℕ) (M : ℝ)
    (hZ : ∀ t ∈ s, 0 ≤ Z t)
    (h : M ^ n * (∑ t ∈ s, Z t) < ∑ t ∈ s, Z t ^ (n + 1)) :
    ∃ t ∈ s, M < Z t := by
  by_contra hc
  simp only [not_exists, not_and, not_lt] at hc
  exact (lt_irrefl _) (h.trans_le (weighted_sum_le Z s n M hZ hc))

/-- The open brick: the uniform bound `M` on the invariant moment.  Stated as an
open marker in the register idiom — the criterion above is sufficient, this
boundedness is what is missing. -/
def criticalInvariantBoundedOpen : Prop := True

/-- The formalised facts of this criterion brick. -/
def onsagerCriterionFacts : List String :=
  [ "weighted_sum_le", "spike_of_excess" ]

/-- The register has exactly two entries. -/
theorem onsagerCriterionFacts_length : onsagerCriterionFacts.length = 2 := by decide

end PunoCalculus.OnsagerCriterion
