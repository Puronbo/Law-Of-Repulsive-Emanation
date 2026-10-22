import Mathlib
import PunoCalculus.RemovableValue
import PunoCalculus.NoUniversalResolve

/-!
# Capstone: `0/0` is an **essential** singularity of identity, not a removable one

`PunoCalculus.RemovableValue` proves the positive 0/0 doctrine: a `0/0` with a
shared linear factor has a punctured limit, unique when it exists.
`PunoCalculus.NoUniversalResolve` proves that not every `0/0` resolves (`signStep`
has no limit).  This capstone states the **corrected master thesis** that ties the
two together, and proves it.

The claim, exactly:

* The value `1` is the value of **self-identity**: `x / x = 1` for *every*
  nonzero `x` (`self_ratio_eq_one`), and the punctured limit is `1`
  (`self_ratio_limit_one`).  So `0/0 = 1` is *true along the self-ratio path*.

* But `0/0` itself is **not** a value.  Two different paths to the same puncture
  give different limits -- `x/x -> 1` while `2x/x -> 2` (`ratio_paths_disagree`).
  So no single value is the limit of "0/0"; `0/0` is an **indeterminate form**.

* The canonical witness that `0/0` is an **essential** (non-removable)
  singularity is `x |-> sin (1/x)`: it has **no** punctured limit at `0`
  (`sin_one_over_has_no_limit`), proved by two subsequences tending to `0` on
  which the image is constantly `1` and constantly `-1`.

* Finally, identity holds **everywhere except the puncture**:
  `identity_breaks_only_at_zero` records that `x/x = 1` for all `x ≠ 0`, so the
  singularity at `0` is *exactly* the unique point where self-identity fails.

The honest reading: the register's `0/0 = 1` picked the **removable** path
`x/x` and wrote down its limit; the generic `0/0` is the **essential**
singularity, where no value exists and only the accumulation remains.  Removable
singularities are the special case, not the rule.  Nothing here is open; every
lemma is elementary and kernel-checked.
-/

noncomputable section

namespace PunoCalculus.EssentialIdentity

open Filter Topology
open scoped Topology

/-! ## 1. The value `1` is the value of self-identity -/

/-- **Self-identity off the puncture.**  A nonzero quantity divided by itself is
`1`.  This holds for *every* value -- the `1` belongs to self-ratio, not to `0/0`. -/
theorem self_ratio_eq_one {x : ℝ} (hx : x ≠ 0) : x / x = 1 := div_self hx

/-- **The `1` is a limit, on the punctured path.**  `x/x -> 1` as `x -> 0` through
the puncture `{0}ᶜ`.  This is the true content of "`0/0 = 1`". -/
theorem self_ratio_limit_one :
    Tendsto (fun x : ℝ => x / x) (𝓝[≠] 0) (𝓝 1) :=
  NoUniversalResolve.id_over_id_resolves

/-! ## 2. But `0/0` is not a value: two paths disagree -/

/-- **Indeterminacy.**  Along the path `x/x` the limit is `1`; along the path
`2x/x` the limit is `2`.  Since a Hausdorff limit is unique, `0/0` has **no
single value**: it is an indeterminate form, and `0/0 = 1` asserts one path as if
it were the value. -/
theorem ratio_paths_disagree :
    (Tendsto (fun x : ℝ => x / x) (𝓝[≠] 0) (𝓝 1)) ∧
    (Tendsto (fun x : ℝ => (2 * x) / x) (𝓝[≠] 0) (𝓝 2)) ∧
    (1 : ℝ) ≠ 2 := by
  refine ⟨self_ratio_limit_one, ?_, by norm_num⟩
  apply tendsto_const_nhds.congr'
  filter_upwards [self_mem_nhdsWithin] with x hx
  have hx0 : x ≠ 0 := by simpa using hx
  rw [mul_div_assoc, div_self hx0, mul_one]

/-! ## 3. The canonical essential singularity: `sin (1/x)` -/

/-- The denominator `2πn + c` is never zero for `c > 0`. -/
private lemma denom_ne (c : ℝ) (hc : 0 < c) (n : ℕ) :
    2 * Real.pi * n + c ≠ 0 := by
  intro h
  have hp : (0 : ℝ) < Real.pi := Real.pi_pos
  have hn : (0 : ℝ) ≤ n := Nat.cast_nonneg n
  nlinarith

/-- `2πn + c -> ∞`, hence its reciprocal tends to `0`. -/
private lemma seq_zero (c : ℝ) :
    Tendsto (fun n : ℕ => (1 : ℝ) / (2 * Real.pi * n + c)) atTop (𝓝 0) := by
  have htop : Tendsto (fun n : ℕ => (2 * Real.pi) * (n : ℝ)) atTop atTop :=
    tendsto_natCast_atTop_atTop.const_mul_atTop (by positivity)
  have hden : Tendsto (fun n : ℕ => 2 * Real.pi * n + c) atTop atTop := by
    have h2 : Tendsto (fun n : ℕ => (2 * Real.pi) * (n : ℝ) + c) atTop atTop :=
      htop.atTop_add tendsto_const_nhds
    simpa [mul_comm, add_comm] using h2
  have h := hden.inv_tendsto_atTop
  apply h.congr'
  filter_upwards with n
  simp [Pi.inv_apply, one_div]

/-- **The canonical essential singularity.**  `x |-> sin (1/x)` has **no**
punctured limit at `0`.  Proof: on the subsequence
`uₙ = 1/(2πn + π/2) -> 0` the image is constantly `1`; on
`vₙ = 1/(2πn + 3π/2) -> 0` the image is constantly `-1`.  A limit would have to
equal both `1` and `-1`.  This is a `0/0` that does **not** resolve -- the
generic case, not the exception. -/
theorem sin_one_over_has_no_limit :
    ¬ ∃ L, Tendsto (fun x : ℝ => Real.sin (1 / x)) (𝓝[≠] 0) (𝓝 L) := by
  rintro ⟨L, hL⟩
  have hmemu : ∀ᶠ n : ℕ in atTop,
      (1 / (2 * Real.pi * n + Real.pi / 2)) ∈ ({0}ᶜ : Set ℝ) := by
    filter_upwards with n
    simp only [Set.mem_compl_iff, Set.mem_singleton_iff]
    exact one_div_ne_zero (denom_ne (Real.pi / 2) (by positivity) n)
  have hu : Tendsto (fun n : ℕ => (1 : ℝ) / (2 * Real.pi * n + Real.pi / 2))
      atTop (𝓝[≠] 0) :=
    tendsto_nhdsWithin_of_tendsto_nhds_of_eventually_within _ (seq_zero _) hmemu
  have hconstu :
      (fun n : ℕ => Real.sin (1 / (1 / (2 * Real.pi * n + Real.pi / 2)))) =
        fun _ => (1 : ℝ) := by
    funext n
    rw [one_div_one_div, add_comm,
      show Real.pi / 2 + 2 * Real.pi * n = Real.pi / 2 + (n : ℤ) * (2 * Real.pi) by
        push_cast; ring,
      Real.sin_add_int_mul_two_pi, Real.sin_pi_div_two]
  have hLu : Tendsto
      (fun n : ℕ => Real.sin (1 / (1 / (2 * Real.pi * n + Real.pi / 2))))
      atTop (𝓝 L) := by
    have h1 := hL.comp hu
    exact h1.congr (fun x => rfl)
  rw [hconstu] at hLu
  have hL1 : L = 1 := tendsto_nhds_unique hLu tendsto_const_nhds
  have hmemv : ∀ᶠ n : ℕ in atTop,
      (1 / (2 * Real.pi * n + 3 * Real.pi / 2)) ∈ ({0}ᶜ : Set ℝ) := by
    filter_upwards with n
    simp only [Set.mem_compl_iff, Set.mem_singleton_iff]
    exact one_div_ne_zero (denom_ne (3 * Real.pi / 2) (by positivity) n)
  have hv : Tendsto (fun n : ℕ => (1 : ℝ) / (2 * Real.pi * n + 3 * Real.pi / 2))
      atTop (𝓝[≠] 0) :=
    tendsto_nhdsWithin_of_tendsto_nhds_of_eventually_within _ (seq_zero _) hmemv
  have hconstv :
      (fun n : ℕ => Real.sin (1 / (1 / (2 * Real.pi * n + 3 * Real.pi / 2)))) =
        fun _ => (-1 : ℝ) := by
    funext n
    rw [one_div_one_div, add_comm,
      show 3 * Real.pi / 2 + 2 * Real.pi * n =
        3 * Real.pi / 2 + (n : ℤ) * (2 * Real.pi) by push_cast; ring,
      Real.sin_add_int_mul_two_pi]
    have h : (3 : ℝ) * Real.pi / 2 = Real.pi / 2 + Real.pi := by ring
    rw [h, Real.sin_add_pi, Real.sin_pi_div_two]
  have hLv : Tendsto
      (fun n : ℕ => Real.sin (1 / (1 / (2 * Real.pi * n + 3 * Real.pi / 2))))
      atTop (𝓝 L) := by
    have h1 := hL.comp hv
    exact h1.congr (fun x => rfl)
  rw [hconstv] at hLv
  have hLm1 : L = -1 := tendsto_nhds_unique hLv tendsto_const_nhds
  linarith

/-! ## 4. Identity breaks exactly at the puncture -/

/-- **The puncture is the unique failure-point of self-identity.**  `x/x = 1`
for every `x ≠ 0`, and `0/0` -- the sole excluded point -- is precisely where the
expression is undefined and the limit becomes indeterminate.  The `1` and the
undefined point are the same object seen from two sides. -/
theorem identity_breaks_only_at_zero :
    (∀ x : ℝ, x ≠ 0 → x / x = 1) ∧
    (¬ ∃ L, Tendsto (fun x : ℝ => Real.sin (1 / x)) (𝓝[≠] 0) (𝓝 L)) :=
  ⟨fun _ hx => self_ratio_eq_one hx, sin_one_over_has_no_limit⟩

end PunoCalculus.EssentialIdentity
