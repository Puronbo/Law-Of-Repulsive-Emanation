import Mathlib

/-!
# Zero as the point that defines its own position; the wall that shrinks itself

This file formalises the register reading of the honest wall
(`THE_LAW_OF_SINGULARITIES.md` §12.1) as a *removable 0/0* in the same
`Tendsto`-on-the-punctured-neighbourhood idiom as `PunoCalculus.Removable`:

* **"zero is the point that defines its own position."** At a fixed point
  `T x₀ = x₀` where `T` has derivative `L`, the change-of-position per
  change-of-position, `(T x - x)/(x - x₀)`, is the fixed-point 0/0 whose
  removable value is `L - 1` (`fixedPoint_selfSlope`).  This is the
  Banach/Brouwer 0/0 of Experiments #34/#35 of the Law of Singularities.  For
  the identity the point sits on itself and the shift is `0`
  (`identity_selfSlope`).

* **"it scales itself on how many zeros it has."** The removable value at a
  point of mutual vanishing is singled out exactly by the *order of vanishing*:
  dividing `(x - x₀)^k · h` by `(x - x₀)^j`
  * with `j = k` gives the finite value `h x₀`  (`zero_count_removable`);
  * with `j < k` gives `0`                        (`zero_count_under`);
  * with `j > k` the reciprocal gives `0`, i.e. the original blows up
    (`zero_count_over`).

  So the *number of zeros* `k` is the scale at which the wall shrinks itself
  to a finite value; fewer cancels leave nothing, more overshoot into a pole.
  This is Lemma 2.1 of the Law of Singularities made into three exact limits.

Scope is bounded as in `PunoCalculus.Removable`: every statement is a limit on
the punctured neighbourhood, never a value AT the singular point.
-/

noncomputable section

namespace PunoCalculus.ZeroFixedPoint

open Filter
open scoped Topology

/-- **The self-positioning 0/0.** At a fixed point `T x₀ = x₀` where `T` has
derivative `L`, the ratio of the change of position to the change of position
`(T x - x)/(x - x₀)` has removable value `L - 1`.  The point defines its own
position; the "self-shift" is the derivative minus the identity. -/
theorem fixedPoint_selfSlope {T : ℝ → ℝ} {L x₀ : ℝ}
    (hT : HasDerivAt T L x₀) (hfix : T x₀ = x₀) :
    Tendsto (fun x : ℝ => (T x - x) / (x - x₀)) (𝓝[≠] x₀) (𝓝 (L - 1)) := by
  have hslope : Tendsto (fun x : ℝ => slope T x₀ x) (𝓝[≠] x₀) (𝓝 L) :=
    hT.tendsto_slope
  have heq : (fun x : ℝ => (T x - x) / (x - x₀)) =ᶠ[𝓝[≠] x₀]
      (fun x : ℝ => slope T x₀ x - 1) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    have hx0 : x - x₀ ≠ 0 := sub_ne_zero.mpr hx
    rw [slope_def_field, hfix]
    field_simp [hx0]
    ring
  have hsub : Tendsto (fun x : ℝ => slope T x₀ x - 1) (𝓝[≠] x₀) (𝓝 (L - 1)) :=
    hslope.sub tendsto_const_nhds
  exact Tendsto.congr' heq.symm hsub

/-- **The point sits on itself.** For the identity map `T = id` the self-shift
is `L - 1 = 1 - 1 = 0`: zero is the point whose own position it defines, and the
shift is exactly nothing. -/
theorem identity_selfSlope (x₀ : ℝ) :
    Tendsto (fun x : ℝ => (x - x) / (x - x₀)) (𝓝[≠] x₀) (𝓝 0) := by
  simp

/-- **Dividing out exactly the number of zeros gives the finite value.** If
`h` is continuous at `x₀` and the numerator is `(x - x₀)^k · h x`, dividing by
`(x - x₀)^k` (the same number `k` of zeros) has removable value `h x₀`. -/
theorem zero_count_removable {h : ℝ → ℝ} {x₀ : ℝ} (hh : ContinuousAt h x₀)
    (k : ℕ) :
    Tendsto (fun x : ℝ => ((x - x₀) ^ k * h x) / (x - x₀) ^ k)
      (𝓝[≠] x₀) (𝓝 (h x₀)) := by
  have heq : (fun x : ℝ => ((x - x₀) ^ k * h x) / (x - x₀) ^ k) =ᶠ[𝓝[≠] x₀] h := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    have hx0 : (x - x₀) ^ k ≠ 0 := pow_ne_zero k (sub_ne_zero.mpr hx)
    field_simp [hx0]
  exact Tendsto.congr' heq.symm (hh.mono_left nhdsWithin_le_nhds)

/-- **Dividing out fewer zeros than the order leaves nothing.** With `j < k`
the ratio `(x - x₀)^k · h x / (x - x₀)^j` tends to `0`: an under-cancelled
0/0 collapses to zero. -/
theorem zero_count_under {h : ℝ → ℝ} {x₀ : ℝ} (hh : ContinuousAt h x₀)
    {k j : ℕ} (hjk : j < k) :
    Tendsto (fun x : ℝ => ((x - x₀) ^ k * h x) / (x - x₀) ^ j)
      (𝓝[≠] x₀) (𝓝 0) := by
  have heq : (fun x : ℝ => ((x - x₀) ^ k * h x) / (x - x₀) ^ j) =ᶠ[𝓝[≠] x₀]
      (fun x : ℝ => (x - x₀) ^ (k - j) * h x) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    have hx0 : x - x₀ ≠ 0 := sub_ne_zero.mpr hx
    have hpow : (x - x₀) ^ k = (x - x₀) ^ j * (x - x₀) ^ (k - j) := by
      rw [← pow_add, Nat.add_sub_of_le (le_of_lt hjk)]
    rw [hpow]
    field_simp [pow_ne_zero j hx0]
  have hx0t : Tendsto (fun x : ℝ => x - x₀) (𝓝[≠] x₀) (𝓝 0) := by
    have h : Tendsto (fun x : ℝ => x - x₀) (𝓝 x₀) (𝓝 0) := by
      simpa using (tendsto_id.sub_const x₀ :
        Tendsto (fun x : ℝ => x - x₀) (𝓝 x₀) (𝓝 (x₀ - x₀)))
    exact h.mono_left nhdsWithin_le_nhds
  have hh' : Tendsto h (𝓝[≠] x₀) (𝓝 (h x₀)) := hh.mono_left nhdsWithin_le_nhds
  have hm0 : k - j ≠ 0 := by omega
  have hz : (0 : ℝ) ^ (k - j) = 0 := zero_pow hm0
  have hlim : Tendsto (fun x : ℝ => (x - x₀) ^ (k - j) * h x) (𝓝[≠] x₀) (𝓝 0) := by
    have hp := hx0t.pow (k - j)
    rw [hz] at hp
    simpa using hp.mul hh'
  exact Tendsto.congr' heq.symm hlim

/-- **Dividing out more zeros than the order overshoots into a pole.** With
`k < j` and `h x₀ ≠ 0`, the reciprocal ratio
`(x - x₀)^j / ((x - x₀)^k · h x)` tends to `0`, i.e. the original ratio
diverges: an over-cancelled 0/0 has no finite removable value. -/
theorem zero_count_over {h : ℝ → ℝ} {x₀ : ℝ} (hh : ContinuousAt h x₀)
    (hh0 : h x₀ ≠ 0) {k j : ℕ} (hkj : k < j) :
    Tendsto (fun x : ℝ => (x - x₀) ^ j / ((x - x₀) ^ k * h x))
      (𝓝[≠] x₀) (𝓝 0) := by
  have hev : ∀ᶠ x : ℝ in 𝓝[≠] x₀, h x ≠ 0 :=
    (hh.tendsto.eventually (isOpen_ne.mem_nhds hh0)).filter_mono nhdsWithin_le_nhds
  have heq : (fun x : ℝ => (x - x₀) ^ j / ((x - x₀) ^ k * h x)) =ᶠ[𝓝[≠] x₀]
      (fun x : ℝ => (x - x₀) ^ (j - k) * (h x)⁻¹) := by
    filter_upwards [eventually_mem_nhdsWithin, hev] with x hx hhx
    have hx0 : x - x₀ ≠ 0 := sub_ne_zero.mpr hx
    have hpow : (x - x₀) ^ j = (x - x₀) ^ k * (x - x₀) ^ (j - k) := by
      rw [← pow_add, Nat.add_sub_of_le (le_of_lt hkj)]
    rw [hpow]
    have hkne : (x - x₀) ^ k ≠ 0 := pow_ne_zero k hx0
    field_simp [hkne, hhx]
  have hx0t : Tendsto (fun x : ℝ => x - x₀) (𝓝[≠] x₀) (𝓝 0) := by
    have h : Tendsto (fun x : ℝ => x - x₀) (𝓝 x₀) (𝓝 0) := by
      simpa using (tendsto_id.sub_const x₀ :
        Tendsto (fun x : ℝ => x - x₀) (𝓝 x₀) (𝓝 (x₀ - x₀)))
    exact h.mono_left nhdsWithin_le_nhds
  have hh' : Tendsto h (𝓝[≠] x₀) (𝓝 (h x₀)) := hh.mono_left nhdsWithin_le_nhds
  have hm0 : j - k ≠ 0 := by omega
  have hz : (0 : ℝ) ^ (j - k) = 0 := zero_pow hm0
  have hlim : Tendsto (fun x : ℝ => (x - x₀) ^ (j - k) * (h x)⁻¹)
      (𝓝[≠] x₀) (𝓝 0) := by
    have hp := hx0t.pow (j - k)
    rw [hz] at hp
    simpa using hp.mul (hh'.inv₀ hh0)
  exact Tendsto.congr' heq.symm hlim

/-- Formalised-facts register for `ZeroFixedPoint.lean`. -/
def zeroFixedPointFacts : List String :=
  [ "fixedPoint_selfSlope"
  , "identity_selfSlope"
  , "zero_count_removable"
  , "zero_count_under"
  , "zero_count_over" ]

/-- The register has exactly five entries. -/
theorem zeroFixedPointFacts_length : zeroFixedPointFacts.length = 5 := by decide

end PunoCalculus.ZeroFixedPoint
