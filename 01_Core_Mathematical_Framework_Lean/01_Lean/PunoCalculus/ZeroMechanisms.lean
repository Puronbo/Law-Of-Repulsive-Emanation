import Mathlib
import PunoCalculus.ZeroProbe
import PunoCalculus.ZeroValuation
import PunoCalculus.ZeroIndex

/-!
# The mechanism closure: the anti-class, and the five faces bundled

`THE_0_OVER_0_ATLAS.md` classifies a removable 0/0 into mechanisms -- Probe
(identity), Index (integer), Vanishing Rate (leading coefficient), Critical, and
Conservation -- and records the **amendment** that the strict completeness claim is
*false*: there are 0/0 forms whose ratio has **no limit at all** (the "anti-class":
Pólya `F(n)/√n`, Mertens, the divisor/circle errors, ...).  This brick makes that
amendment a theorem and closes the mechanism register:

* `abs_div_self_tendsto_right` / `abs_div_self_tendsto_left`: the sign function
  `|x|/x` tends to `1` from the right and `-1` from the left.
* `abs_div_self_no_limit`: **the anti-class is nonempty** -- the genuine 0/0
  `|x|/x` (both numerator and denominator vanish at `0`) has *no removable value*:
  its ratio has no punctured limit.  This refutes "every 0/0 is removable".
* `abs_vanish` / `id_vanish`: the numerator and denominator do both vanish at the
  point, so this really is a 0/0.
* `anti_class_nonempty`: the three facts above, bundled.
* `mechanisms_close`: the capstone -- the Probe, Vanishing-Rate, and Index faces
  (from `ZeroProbe`, `ZeroValuation`, `ZeroIndex`) together with the anti-class.

Scope as everywhere: `Tendsto` on the punctured neighbourhood, never a value AT the
point; a mathematical schema, not a claim about any Millennium problem.  The
Critical and Conservation mechanisms are named in the atlas but their formal
treatment is left to the dynamical-systems / symmetry rows elsewhere in the library.
-/

noncomputable section

namespace PunoCalculus.ZeroMechanisms

open Filter
open Polynomial
open scoped Topology

/-- **The sign function tends to `+1` from the right.** -/
theorem abs_div_self_tendsto_right :
    Tendsto (fun x : ℝ => |x| / x) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have h : (fun x : ℝ => |x| / x) =ᶠ[𝓝[>] (0 : ℝ)] (fun _ => 1) := by
    filter_upwards [self_mem_nhdsWithin] with x hx
    have hxpos : 0 < x := hx
    rw [abs_of_pos hxpos, div_self hxpos.ne']
  exact Tendsto.congr' h.symm tendsto_const_nhds

/-- **The sign function tends to `-1` from the left.** -/
theorem abs_div_self_tendsto_left :
    Tendsto (fun x : ℝ => |x| / x) (𝓝[<] (0 : ℝ)) (𝓝 (-1)) := by
  have h : (fun x : ℝ => |x| / x) =ᶠ[𝓝[<] (0 : ℝ)] (fun _ => -1) := by
    filter_upwards [self_mem_nhdsWithin] with x hx
    have hxneg : x < 0 := hx
    rw [abs_of_neg hxneg, neg_div, div_self (ne_of_lt hxneg)]
  exact Tendsto.congr' h.symm tendsto_const_nhds

/-- **The anti-class is nonempty.**  The 0/0 `|x|/x` has **no** removable value: its
ratio has no limit at `0`.  A limit would restrict to both one-sided limits, forcing
`1 = -1`. -/
theorem abs_div_self_no_limit :
    ¬ ∃ L : ℝ, Tendsto (fun x : ℝ => |x| / x) (𝓝[≠] (0 : ℝ)) (𝓝 L) := by
  rintro ⟨L, hL⟩
  have hright : Tendsto (fun x : ℝ => |x| / x) (𝓝[>] (0 : ℝ)) (𝓝 L) :=
    hL.mono_left (nhdsWithin_mono (0 : ℝ) (fun x hx => ne_of_gt (show 0 < x from hx)))
  have hleft : Tendsto (fun x : ℝ => |x| / x) (𝓝[<] (0 : ℝ)) (𝓝 L) :=
    hL.mono_left (nhdsWithin_mono (0 : ℝ) (fun x hx => ne_of_lt (show x < 0 from hx)))
  have h1 : L = 1 := tendsto_nhds_unique hright abs_div_self_tendsto_right
  have h2 : L = -1 := tendsto_nhds_unique hleft abs_div_self_tendsto_left
  exact absurd (h1.symm.trans h2) (by norm_num)

/-- The numerator `|·|` vanishes at `0`. -/
theorem abs_vanish : Tendsto (fun x : ℝ => |x|) (𝓝[≠] (0 : ℝ)) (𝓝 0) := by
  have hc : ContinuousAt (fun x : ℝ => |x|) 0 := continuous_abs.continuousAt
  simpa using hc.mono_left nhdsWithin_le_nhds

/-- The denominator `·` vanishes at `0`. -/
theorem id_vanish : Tendsto (fun x : ℝ => x) (𝓝[≠] (0 : ℝ)) (𝓝 0) := by
  have hc : ContinuousAt (fun x : ℝ => x) 0 := continuousAt_id
  simpa using hc.mono_left nhdsWithin_le_nhds

/-- **The anti-class is nonempty.**  A genuine 0/0 (both `|·|` and `·` vanish at
`0`) whose ratio `|x|/x` has no removable value.  This is the register's amendment:
the five-mechanism classification covers only the *removable* 0/0. -/
theorem anti_class_nonempty :
    Tendsto (fun x : ℝ => |x|) (𝓝[≠] (0 : ℝ)) (𝓝 0) ∧
    Tendsto (fun x : ℝ => x) (𝓝[≠] (0 : ℝ)) (𝓝 0) ∧
    (¬ ∃ L : ℝ, Tendsto (fun x : ℝ => |x| / x) (𝓝[≠] (0 : ℝ)) (𝓝 L)) :=
  ⟨abs_vanish, id_vanish, abs_div_self_no_limit⟩

variable {R : Type*} [CommRing R] [IsDomain R] [DecidableEq R]

/-- **The mechanism closure.**  The register's mechanism faces, bundled: the Probe
resolves a self-0/0 to `1` (`ZeroProbe`), the order of vanishing is additive
(`ZeroValuation`), the index is additive (`ZeroIndex`), and the anti-class is
nonempty -- a removable classification is *not* automatic. -/
theorem mechanisms_close :
    (∀ (f : ℝ → ℝ) (x₀ : ℝ), (∀ᶠ x in 𝓝[≠] x₀, f x ≠ 0) →
        ZeroProbe.ProbeValue f f x₀ 1) ∧
    (∀ (k l : ℕ) (f g : ℝ → ℝ) (x₀ : ℝ), ZeroValuation.HasOrder k f x₀ →
        ZeroValuation.HasOrder l g x₀ →
        ZeroValuation.HasOrder (k + l) (fun x => f x * g x) x₀) ∧
    (∀ {p q : R[X]}, p * q ≠ 0 → ∀ a : R,
        ZeroIndex.Index a (p * q) = ZeroIndex.Index a p + ZeroIndex.Index a q) ∧
    (¬ ∃ L : ℝ, Tendsto (fun x : ℝ => |x| / x) (𝓝[≠] (0 : ℝ)) (𝓝 L)) :=
  ⟨fun f x₀ hf => ZeroProbe.probe_self f hf,
   fun _k _l _f _g _x₀ hf hg => ZeroValuation.hasOrder_mul hf hg,
   fun h a => ZeroIndex.index_additive h a,
   abs_div_self_no_limit⟩

/-- Formalised-facts register for `ZeroMechanisms.lean`. -/
def zeroMechanismsFacts : List String :=
  [ "abs_div_self_tendsto_right", "abs_div_self_tendsto_left", "abs_div_self_no_limit",
    "abs_vanish", "id_vanish", "anti_class_nonempty", "mechanisms_close" ]

/-- The register has exactly seven entries. -/
theorem zeroMechanismsFacts_length : zeroMechanismsFacts.length = 7 := by decide

end PunoCalculus.ZeroMechanisms
