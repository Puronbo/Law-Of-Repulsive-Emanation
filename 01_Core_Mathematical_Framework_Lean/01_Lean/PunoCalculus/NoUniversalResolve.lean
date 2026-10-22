import Mathlib
import PunoCalculus.RemovableValue

/-!
# G21 no-go: "every 0/0 resolves" is **false**

`PunoCalculus.RemovableValue` proves the *positive* half of the 0/0 doctrine: a
`0/0` with a shared linear factor has a punctured limit, and that limit is unique
when it exists.  This module records the **no-go** half that G21 demands: it is
*not* the case that every `0/0` resolves.  Not every punctured limit exists.

- `sign_step` : the two-sided sign function `x ↦ +1 (x>0) / −1 (x<0)`, a canonical
  `0/0` at `0` (both one-sided limits are nonzero and disagree).
- `sign_step_has_no_limit` : the punctured limit at `0` **does not exist** -- the
  left limit is `-1`, the right limit is `+1`, and a Hausdorff limit would have to
  equal both.  Hence "every 0/0 resolves" is refuted.
- `id_over_id_resolves` : the contrast -- the genuine removable `0/0` `x/x`
  *does* resolve to `1` on the punctured neighbourhood.  So removability is a
  condition, not a universal.

Everything here is elementary topology, kernel-checked; nothing is open.
-/

noncomputable section

namespace PunoCalculus.NoUniversalResolve

open Filter Topology
open scoped Topology

/-- The two-sided sign step: `+1` for positive `x`, `-1` otherwise.  Read as a
`0/0` at the origin, its two one-sided limits disagree. -/
def signStep (x : ℝ) : ℝ := if 0 < x then 1 else -1

/-- **G21 no-go.**  The punctured limit of `signStep` at `0` does not exist, so not
every `0/0` resolves. -/
theorem signStep_has_no_limit : ¬ ∃ L, Tendsto signStep (𝓝[≠] 0) (𝓝 L) := by
  rintro ⟨L, hL⟩
  have hsubR : Set.Ioi (0 : ℝ) ⊆ ({0}ᶜ : Set ℝ) := by
    intro x hx; simp; exact ne_of_gt hx
  have hp : Tendsto signStep (𝓝[>] (0 : ℝ)) (𝓝 L) :=
    hL.mono_left (nhdsWithin_mono 0 hsubR)
  have hpos : Tendsto signStep (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    apply tendsto_const_nhds.congr'
    filter_upwards [self_mem_nhdsWithin] with x hx
    exact (if_pos hx).symm
  have e1 : L = 1 := tendsto_nhds_unique hp hpos
  have hsubL : Set.Iio (0 : ℝ) ⊆ ({0}ᶜ : Set ℝ) := by
    intro x hx; simp; exact ne_of_lt hx
  have hn : Tendsto signStep (𝓝[<] (0 : ℝ)) (𝓝 L) :=
    hL.mono_left (nhdsWithin_mono 0 hsubL)
  have hneg : Tendsto signStep (𝓝[<] (0 : ℝ)) (𝓝 (-1)) := by
    apply tendsto_const_nhds.congr'
    filter_upwards [self_mem_nhdsWithin] with x hx
    exact (if_neg (not_lt.mpr hx.le)).symm
  have e2 : L = -1 := tendsto_nhds_unique hn hneg
  linarith

/-- **The contrast.**  The genuine removable `0/0` `x/x` resolves to `1` on the
punctured neighbourhood.  Removability is a condition, not a universal. -/
theorem id_over_id_resolves :
    Tendsto (fun x : ℝ => x / x) (𝓝[≠] 0) (𝓝 1) := by
  apply tendsto_const_nhds.congr'
  filter_upwards [self_mem_nhdsWithin] with x hx
  rw [div_self]; exact_mod_cast hx

end PunoCalculus.NoUniversalResolve
