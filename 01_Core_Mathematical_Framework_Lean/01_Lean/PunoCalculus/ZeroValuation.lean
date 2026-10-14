import Mathlib
import PunoCalculus.VanishOrder

/-!
# Order of vanishing as a **valuation** (the Vanishing-Rate mechanism)

`PunoCalculus.VanishOrder` grades a 0/0 by the *filtration* level at which it
vanishes (`VanishesToOrder` / `HasGrade`).  That grading is a **filtration**, not a
valuation: it is *not* additive under products -- `|·|` and `|·|` both sit at grade
`0` at `x₀ = 0`, yet `|·|·|·| = (·)^2` sits at grade `2`.  The register's
*Vanishing-Rate* mechanism ("leading Taylor coefficient") needs the genuine
**order of vanishing**, defined by a residue *limit*:

* `HasOrder k f x₀`: some nonzero `c` with `f / (· - x₀)^k → c` at the puncture.
  This is the order of vanishing of `f` at `x₀` (`|·|` has order `1`, not `0`).
* `hasOrder_zero_iff`: order `0` is exactly "has a nonzero punctured limit".
* `hasOrder_mul`: **the valuation law** -- orders add under products,
  `order (f·g) = order f + order g`.
* `hasOrder_pow`: orders scale under powers, `order (f^n) = n · order f`.
* `hasOrder_canonical`: the canonical `(· - x₀)^n · h` with `h x₀ ≠ 0` has order `n`.
* `hasOrder_lt_imp_not` / `hasOrder_unique`: the order is well-defined; a strictly
  smaller order excludes a larger one.
* `order_is_valuation`: the capstone bundling additivity, scaling, and uniqueness.

The non-additivity of `HasGrade` (`VanishOrder`) versus the additivity of `HasOrder`
here is the exact reason the register's Vanishing-Rate mechanism is a *valuation*
while its zero-count is only a *filtration*.

Scope as everywhere: a `Tendsto` on the punctured neighbourhood, never a value AT
the point, and no Millennium problem is touched.
-/

noncomputable section

namespace PunoCalculus.ZeroValuation

open Filter
open scoped Topology

/-- **The order of vanishing** of `f` at `x₀` is `k` when `f / (· - x₀)^k` has a
nonzero punctured limit.  This is the Vanishing-Rate mechanism's invariant, and is
additive under products (unlike the filtration `VanishOrder.HasGrade`). -/
def HasOrder (k : ℕ) (f : ℝ → ℝ) (x₀ : ℝ) : Prop :=
  ∃ c : ℝ, c ≠ 0 ∧ Tendsto (fun x : ℝ => f x / (x - x₀) ^ k) (𝓝[≠] x₀) (𝓝 c)

/-- The constant `1` has order `0`. -/
theorem hasOrder_one (x₀ : ℝ) : HasOrder 0 (fun _ : ℝ => (1 : ℝ)) x₀ := by
  refine ⟨1, one_ne_zero, ?_⟩
  simp

/-- **Order `0` is "a nonzero punctured limit".** -/
theorem hasOrder_zero_iff {f : ℝ → ℝ} {x₀ : ℝ} :
    HasOrder 0 f x₀ ↔ ∃ c : ℝ, c ≠ 0 ∧ Tendsto f (𝓝[≠] x₀) (𝓝 c) := by
  simp [HasOrder]

/-- **The valuation law: orders add under products.**  `order (f·g) = order f +
order g`. -/
theorem hasOrder_mul {k l : ℕ} {f g : ℝ → ℝ} {x₀ : ℝ}
    (hf : HasOrder k f x₀) (hg : HasOrder l g x₀) :
    HasOrder (k + l) (fun x : ℝ => f x * g x) x₀ := by
  obtain ⟨c, hc, hfp⟩ := hf
  obtain ⟨d, hd, hgp⟩ := hg
  refine ⟨c * d, mul_ne_zero hc hd, ?_⟩
  have hprod : Tendsto (fun x : ℝ => (f x / (x - x₀) ^ k) * (g x / (x - x₀) ^ l))
      (𝓝[≠] x₀) (𝓝 (c * d)) := hfp.mul hgp
  have heq : (fun x : ℝ => (f x / (x - x₀) ^ k) * (g x / (x - x₀) ^ l))
      =ᶠ[𝓝[≠] x₀] fun x : ℝ => f x * g x / (x - x₀) ^ (k + l) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    have hx0 : x - x₀ ≠ 0 := sub_ne_zero.mpr hx
    rw [pow_add]
    field_simp [pow_ne_zero k hx0, pow_ne_zero l hx0]
  exact Tendsto.congr' heq hprod

/-- **Orders scale under powers.**  `order (f^n) = n · order f`. -/
theorem hasOrder_pow {k : ℕ} {f : ℝ → ℝ} {x₀ : ℝ} (hf : HasOrder k f x₀) (n : ℕ) :
    HasOrder (k * n) (fun x : ℝ => f x ^ n) x₀ := by
  induction n with
  | zero => simpa using hasOrder_one x₀
  | succ n ih => simpa [pow_succ, Nat.mul_succ] using hasOrder_mul ih hf

/-- **The canonical vanishing has order `n`.**  `(· - x₀)^n · h` with `h` continuous
at `x₀` and `h x₀ ≠ 0` has order of vanishing exactly `n`. -/
theorem hasOrder_canonical {h : ℝ → ℝ} {x₀ : ℝ} (hh : ContinuousAt h x₀)
    (hh0 : h x₀ ≠ 0) (n : ℕ) :
    HasOrder n (fun x : ℝ => (x - x₀) ^ n * h x) x₀ := by
  refine ⟨h x₀, hh0, ?_⟩
  have heq : (fun x : ℝ => ((x - x₀) ^ n * h x) / (x - x₀) ^ n) =ᶠ[𝓝[≠] x₀] h := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    have hx0 : x - x₀ ≠ 0 := sub_ne_zero.mpr hx
    have hA : (x - x₀) ^ n ≠ 0 := pow_ne_zero n hx0
    field_simp [hA]
  have ht : Tendsto h (𝓝[≠] x₀) (𝓝 (h x₀)) := hh.mono_left nhdsWithin_le_nhds
  exact Tendsto.congr' heq.symm ht

/-- **A strictly smaller order excludes a larger one.**  If `f` has order `k` and
`k < m`, then `f` cannot also have order `m`. -/
theorem hasOrder_lt_imp_not {k m : ℕ} (hkm : k < m) {f : ℝ → ℝ} {x₀ : ℝ}
    (hk : HasOrder k f x₀) : ¬ HasOrder m f x₀ := by
  intro hm
  obtain ⟨c, hc, h1⟩ := hk
  obtain ⟨d, _hd, h2⟩ := hm
  have heq : (fun x : ℝ => f x / (x - x₀) ^ k) =ᶠ[𝓝[≠] x₀]
      fun x : ℝ => (x - x₀) ^ (m - k) * (f x / (x - x₀) ^ m) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    have hx0 : x - x₀ ≠ 0 := sub_ne_zero.mpr hx
    have hp : (x - x₀) ^ m = (x - x₀) ^ k * (x - x₀) ^ (m - k) := by
      rw [← pow_add, Nat.add_sub_of_le hkm.le]
    rw [hp]
    field_simp [pow_ne_zero k hx0, pow_ne_zero (m - k) hx0]
  have hlim : Tendsto (fun x : ℝ => (x - x₀) ^ (m - k) * (f x / (x - x₀) ^ m))
      (𝓝[≠] x₀) (𝓝 0) := by
    have hxm : Tendsto (fun x : ℝ => (x - x₀)) (𝓝[≠] x₀) (𝓝 0) := by
      have hc' : ContinuousAt (fun x : ℝ => x - x₀) x₀ :=
        continuousAt_id.sub continuousAt_const
      simpa using hc'.mono_left nhdsWithin_le_nhds
    have hmk : m - k ≠ 0 := by omega
    have hp : Tendsto (fun x : ℝ => (x - x₀) ^ (m - k)) (𝓝[≠] x₀) (𝓝 0) := by
      have := hxm.pow (m - k)
      rw [zero_pow hmk] at this
      simpa using this
    have := hp.mul h2
    simpa using this
  have h1' : Tendsto (fun x : ℝ => f x / (x - x₀) ^ k) (𝓝[≠] x₀) (𝓝 0) :=
    Tendsto.congr' heq.symm hlim
  exact hc (tendsto_nhds_unique h1 h1')

/-- **The order of vanishing is well-defined.** -/
theorem hasOrder_unique {k m : ℕ} {f : ℝ → ℝ} {x₀ : ℝ}
    (hk : HasOrder k f x₀) (hm : HasOrder m f x₀) : k = m := by
  rcases lt_trichotomy k m with h | h | h
  · exact absurd hm (hasOrder_lt_imp_not h hk)
  · exact h
  · exact absurd hk (hasOrder_lt_imp_not h hm)

/-- **The Vanishing-Rate mechanism is a valuation.**  The order of vanishing is
additive under products, scales under powers, is well-defined, and is realized by the
canonical `(· - x₀)^n · h`. -/
theorem order_is_valuation :
    (∀ (k l : ℕ) (f g : ℝ → ℝ) (x₀ : ℝ),
        HasOrder k f x₀ → HasOrder l g x₀ → HasOrder (k + l) (fun x => f x * g x) x₀) ∧
    (∀ (k : ℕ) (f : ℝ → ℝ) (x₀ : ℝ), HasOrder k f x₀ →
        ∀ n : ℕ, HasOrder (k * n) (fun x => f x ^ n) x₀) ∧
    (∀ (k m : ℕ) (f : ℝ → ℝ) (x₀ : ℝ),
        HasOrder k f x₀ → HasOrder m f x₀ → k = m) ∧
    (∀ (n : ℕ) (h : ℝ → ℝ) (x₀ : ℝ), ContinuousAt h x₀ → h x₀ ≠ 0 →
        HasOrder n (fun x : ℝ => (x - x₀) ^ n * h x) x₀) :=
  ⟨fun _k _l _f _g _x₀ hf hg => hasOrder_mul hf hg,
   fun _k _f _x₀ hf n => hasOrder_pow hf n,
   fun _k _m _f _x₀ hk hm => hasOrder_unique hk hm,
   fun n _h _x₀ hh hh0 => hasOrder_canonical hh hh0 n⟩

/-- Formalised-facts register for `ZeroValuation.lean`. -/
def zeroValuationFacts : List String :=
  [ "HasOrder", "hasOrder_one", "hasOrder_zero_iff", "hasOrder_mul", "hasOrder_pow",
    "hasOrder_canonical", "hasOrder_lt_imp_not", "hasOrder_unique", "order_is_valuation" ]

/-- The register has exactly nine entries. -/
theorem zeroValuationFacts_length : zeroValuationFacts.length = 9 := by decide

end PunoCalculus.ZeroValuation
