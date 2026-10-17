import Mathlib
import PunoCalculus.InformationBridge

/-!
# Information mixture: the "mixture of two or more" decomposition

The note `LANDAUER_BOUND_AND_THE_REGISTER.md` states an **OPEN** claim: that a
register to thermodynamic map `Phi` carries the Landauer cost.  Its named missing
entity is a *measured physical system*.  Every candidate that has been measured so
far is, in fact, a **mixture**: the total entropy production splits into a weighted
"thermodynamic" part plus an **information** part.

* Aimet et al. (2025): `Sigma = Delta I + Delta D` (information + environment
  athermality), equivalently `beta dE + dS`.
* Yan et al., *PRL* 121, 190601 (2018): `ΔQ/k_BT = Delta S + I(S' : R') + D` --
  a three-channel mixture (thermodynamic + mutual information + relative entropy).
* Xue et al. (2024): `Sigma = Sigma_pop + Sigma_coh` (classical population +
  quantum coherence).

This brick formalises only the *algebra of the mixture itself* -- the
Shannon-entropy identity that all these decompositions share:

* `entropy_mixture`: the entropy of a two-block mixture is the weighted entropy
  of the parts **plus** the mixing entropy `binaryEntropy t`;
* `binaryEntropy_nonneg`: that mixing term is non-negative, so mixing adds
  information (`entropy_mixture_ge`);
* `entropy_mixture_half`: a fair mixture (`t = 1/2`) of two channels carries
  exactly `log 2` of extra entropy -- the same constant as one Landauer quantum.

What is **not** done: no measured apparatus is identified here, and no
thermodynamic quantity is derived.  This is the classical mixture algebra that a
concrete measured realisation (the named missing entity of the OPEN claim) would
have to instantiate.  See `PHYSICAL_REALIZATION_OF_PHI.md`.  No Millennium
problem is touched.
-/

noncomputable section

namespace PunoCalculus.InformationMixture

open PunoCalculus.InformationBridge (binaryEntropy)

/-- Shannon entropy (nats) of a finite probability vector. -/
def shannonEntropy {α : Type} [Fintype α] (p : α → ℝ) : ℝ := -∑ i, p i * Real.log (p i)

/-- The mixture of a distribution `a` on `α` and `b` on `β` with weight `t`:
`t` of channel `a` and `1 - t` of channel `b`. -/
def mixture {α β : Type} (t : ℝ) (a : α → ℝ) (b : β → ℝ) : α ⊕ β → ℝ
  | Sum.inl i => t * a i
  | Sum.inr j => (1 - t) * b j

/-- First component of `mixture`, by definition. -/
theorem mixture_inl {α β : Type} (t : ℝ) (a : α → ℝ) (b : β → ℝ) (i : α) :
    mixture t a b (Sum.inl i) = t * a i := rfl

/-- Second component of `mixture`, by definition. -/
theorem mixture_inr {α β : Type} (t : ℝ) (a : α → ℝ) (b : β → ℝ) (j : β) :
    mixture t a b (Sum.inr j) = (1 - t) * b j := rfl

/-- **The mixture decomposition.**  For a genuine mixture (`0 < t < 1`) of two
positive, normalised probability vectors, the entropy of the mixture is the
weighted sum of the parts **plus** the mixing entropy `binaryEntropy t`.  This is
the classical "information term" that the measured bipartite and multichannel
entropy-production splits isolate. -/
theorem entropy_mixture {α β : Type} [Fintype α] [Fintype β]
    (t : ℝ) (a : α → ℝ) (b : β → ℝ)
    (ht : 0 < t) (ht1 : 0 < 1 - t)
    (ha : ∀ i, 0 < a i) (hb : ∀ j, 0 < b j)
    (ha1 : ∑ i, a i = 1) (hb1 : ∑ j, b j = 1) :
    shannonEntropy (mixture t a b)
      = t * shannonEntropy a + (1 - t) * shannonEntropy b + binaryEntropy t := by
  have hinl :
      ∑ i, (t * a i) * Real.log (t * a i)
        = t * Real.log t - t * shannonEntropy a := by
    have hterm : ∀ i, (t * a i) * Real.log (t * a i)
        = (t * Real.log t) * a i + t * (a i * Real.log (a i)) := by
      intro i
      rw [Real.log_mul (ne_of_gt ht) (ne_of_gt (ha i))]
      ring
    calc ∑ i, (t * a i) * Real.log (t * a i)
        = ∑ i, ((t * Real.log t) * a i + t * (a i * Real.log (a i))) :=
          Finset.sum_congr rfl (fun i _ => hterm i)
      _ = (t * Real.log t) * ∑ i, a i + t * ∑ i, a i * Real.log (a i) := by
          rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum]
      _ = t * Real.log t - t * shannonEntropy a := by
          rw [ha1, mul_one]
          unfold shannonEntropy
          ring
  have hinr :
      ∑ j, ((1 - t) * b j) * Real.log ((1 - t) * b j)
        = (1 - t) * Real.log (1 - t) - (1 - t) * shannonEntropy b := by
    have hterm : ∀ j, ((1 - t) * b j) * Real.log ((1 - t) * b j)
        = ((1 - t) * Real.log (1 - t)) * b j
          + (1 - t) * (b j * Real.log (b j)) := by
      intro j
      rw [Real.log_mul (ne_of_gt ht1) (ne_of_gt (hb j))]
      ring
    calc ∑ j, ((1 - t) * b j) * Real.log ((1 - t) * b j)
        = ∑ j, (((1 - t) * Real.log (1 - t)) * b j
            + (1 - t) * (b j * Real.log (b j))) :=
          Finset.sum_congr rfl (fun j _ => hterm j)
      _ = ((1 - t) * Real.log (1 - t)) * ∑ j, b j
            + (1 - t) * ∑ j, b j * Real.log (b j) := by
          rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum]
      _ = (1 - t) * Real.log (1 - t) - (1 - t) * shannonEntropy b := by
          rw [hb1, mul_one]
          unfold shannonEntropy
          ring
  conv_lhs => unfold shannonEntropy
  rw [Fintype.sum_sum_type]
  simp only [mixture_inl, mixture_inr]
  rw [hinl, hinr]
  unfold binaryEntropy
  ring

/-- **The mixing term is non-negative.**  For `0 <= t <= 1`, the binary entropy
`binaryEntropy t >= 0`: splitting a register into a mixture never loses
information. -/
theorem binaryEntropy_nonneg {t : ℝ} (h0 : 0 ≤ t) (h1 : t ≤ 1) :
    0 ≤ binaryEntropy t := by
  unfold binaryEntropy
  have ht : t * Real.log t ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos h0 (Real.log_nonpos h0 h1)
  have h1t : 0 ≤ 1 - t := by linarith
  have h1t1 : 1 - t ≤ 1 := by linarith
  have h1' : (1 - t) * Real.log (1 - t) ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos h1t (Real.log_nonpos h1t h1t1)
  have hsum : t * Real.log t + (1 - t) * Real.log (1 - t) ≤ 0 := add_nonpos ht h1'
  linarith

/-- **Mixtures add information.**  The entropy of a mixture is at least the
weighted entropy of its parts; the excess is the non-negative mixing term. -/
theorem entropy_mixture_ge {α β : Type} [Fintype α] [Fintype β]
    (t : ℝ) (a : α → ℝ) (b : β → ℝ)
    (ht : 0 < t) (ht1 : 0 < 1 - t)
    (ha : ∀ i, 0 < a i) (hb : ∀ j, 0 < b j)
    (ha1 : ∑ i, a i = 1) (hb1 : ∑ j, b j = 1) :
    t * shannonEntropy a + (1 - t) * shannonEntropy b
      ≤ shannonEntropy (mixture t a b) := by
  rw [entropy_mixture t a b ht ht1 ha hb ha1 hb1]
  have := binaryEntropy_nonneg (le_of_lt ht) (by linarith)
  linarith

/-- **A fair mixture carries exactly one Landauer quantum of extra entropy.**
For `t = 1/2` the mixing term is `log 2` -- the same constant as the one-bit
erase cost of `InformationBridge` (`resetCost_two`). -/
theorem entropy_mixture_half {α β : Type} [Fintype α] [Fintype β]
    (a : α → ℝ) (b : β → ℝ)
    (ha : ∀ i, 0 < a i) (hb : ∀ j, 0 < b j)
    (ha1 : ∑ i, a i = 1) (hb1 : ∑ j, b j = 1) :
    shannonEntropy (mixture (1 / 2) a b)
      = (1 / 2) * shannonEntropy a + (1 / 2) * shannonEntropy b + Real.log 2 := by
  rw [entropy_mixture (1 / 2) a b (by norm_num) (by norm_num) ha hb ha1 hb1,
      PunoCalculus.InformationBridge.binaryEntropy_half]
  ring

/-- Formalised-facts register for `InformationMixture.lean`. -/
def informationMixtureFacts : List String :=
  [ "entropy_mixture", "binaryEntropy_nonneg", "entropy_mixture_ge",
    "entropy_mixture_half" ]

/-- The register has exactly four entries. -/
theorem informationMixtureFacts_length : informationMixtureFacts.length = 4 := by decide

end PunoCalculus.InformationMixture
