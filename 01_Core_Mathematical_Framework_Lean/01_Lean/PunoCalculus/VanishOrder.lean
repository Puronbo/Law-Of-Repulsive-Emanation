import Mathlib

/-!
# Order of vanishing as a graded index

`PunoCalculus.ZeroFixedPoint` measures the "number of zeros" `k` of a 0/0: dividing
`(x - x₀)^k · h` by `(x - x₀)^j` gives `h x₀` when `j = k`, `0` when `j < k`, and
diverges when `j > k`.  This brick makes the *number of zeros* a **graded index** --
a level in a decreasing filtration -- so that "it scales itself on how many zeros it
has" becomes a statement about one `ℕ`-grading.

* `VanishesToOrder k f x₀`: the level-`k` member of the vanishing filtration -- `f`
  factors as `(· - x₀)^k · g` with `g` continuous at `x₀`.  Higher `k` = "more
  zeros" = more restrictive.
* `divideOut x₀ f`: divide out one zero, `x ↦ f x / (x - x₀)`.
* `vanishes_zero`: level `0` is "the residue is continuous" (no zero).
* `vanishes_succ_imp` / `vanishes_antitone`: the filtration is **decreasing** --
  vanishing to order `k+1` implies order `k`, and `k ≤ m` brings `F m ⊆ F k`.
* `vanishes_shift`: **the grade.**  `F (k+1) f ↔ F k (divideOut x₀ f)` -- dividing
  out one zero lowers the level by exactly one.  This is "how many zeros" as the
  graded degree.
* `HasGrade k f x₀`: exact order `k` -- in `F k` but not in `F (k+1)`.
* `hasGrade_canonical`: the canonical `(· - x₀)^k · h` with `h x₀ ≠ 0` has exact
  grade `k`.
* `hasGrade_shift`: the exact grade shifts by one under `divideOut`.
* `grade_unique`: the grade is well-defined (`HasGrade k → HasGrade m → k = m`).
* `order_is_graded`: the capstone bundling all of the above.

Scope bounded as in `Removable`/`ZeroFixedPoint`: everything is a statement about
the punctured neighbourhood and the filtration, never a value AT the point, and no
Millennium problem is touched.
-/

noncomputable section

namespace PunoCalculus.VanishOrder

open Filter
open scoped Topology

/-- **The level-`k` member of the vanishing filtration:** `f` vanishes to order at
least `k` at `x₀` when it factors as `(· - x₀)^k · g` with `g` continuous at `x₀`. -/
def VanishesToOrder (k : ℕ) (f : ℝ → ℝ) (x₀ : ℝ) : Prop :=
  ∃ g : ℝ → ℝ, ContinuousAt g x₀ ∧ f =ᶠ[𝓝[≠] x₀] fun x => (x - x₀) ^ k * g x

/-- Divide out one zero at `x₀`. -/
def divideOut (x₀ : ℝ) (f : ℝ → ℝ) : ℝ → ℝ := fun x => f x / (x - x₀)

/-- **Level `0` is "the residue is continuous".**  Vanishing to order `0` means `f`
agrees with a function continuous at `x₀` on the punctured neighbourhood. -/
theorem vanishes_zero (f : ℝ → ℝ) (x₀ : ℝ) :
    VanishesToOrder 0 f x₀ ↔ ∃ g : ℝ → ℝ, ContinuousAt g x₀ ∧ f =ᶠ[𝓝[≠] x₀] g := by
  constructor
  · rintro ⟨g, hg, hfg⟩
    exact ⟨g, hg, by simpa using hfg⟩
  · rintro ⟨g, hg, hfg⟩
    exact ⟨g, hg, by simpa using hfg⟩

/-- **The filtration is decreasing.**  Vanishing to order `k+1` implies vanishing to
order `k`: one more zero is strictly more restrictive. -/
theorem vanishes_succ_imp {k : ℕ} {f : ℝ → ℝ} {x₀ : ℝ}
    (h : VanishesToOrder (k + 1) f x₀) : VanishesToOrder k f x₀ := by
  obtain ⟨g, hg, hfg⟩ := h
  refine ⟨fun x => (x - x₀) * g x, (continuousAt_id.sub continuousAt_const).mul hg, ?_⟩
  refine hfg.trans ?_
  filter_upwards with x
  rw [pow_succ]
  ring

/-- **The grade: dividing out one zero lowers the level by one.**
`F (k+1) f ↔ F k (divideOut x₀ f)`.  So "how many zeros" is the graded degree. -/
theorem vanishes_shift (k : ℕ) (f : ℝ → ℝ) (x₀ : ℝ) :
    VanishesToOrder (k + 1) f x₀ ↔ VanishesToOrder k (divideOut x₀ f) x₀ := by
  constructor
  · rintro ⟨g, hg, hfg⟩
    refine ⟨g, hg, ?_⟩
    filter_upwards [hfg, eventually_mem_nhdsWithin] with x hfx hx
    have hx0 : x - x₀ ≠ 0 := sub_ne_zero.mpr hx
    show f x / (x - x₀) = (x - x₀) ^ k * g x
    rw [hfx, pow_succ]
    field_simp [hx0]
  · rintro ⟨g, hg, hfg⟩
    refine ⟨g, hg, ?_⟩
    filter_upwards [hfg, eventually_mem_nhdsWithin] with x hfx hx
    have hx0 : x - x₀ ≠ 0 := sub_ne_zero.mpr hx
    have hdiv : f x / (x - x₀) = (x - x₀) ^ k * g x := by
      simpa [divideOut] using hfx
    show f x = (x - x₀) ^ (k + 1) * g x
    rw [show (x - x₀) ^ (k + 1) * g x = (x - x₀) * ((x - x₀) ^ k * g x) by
      rw [pow_succ]; ring]
    rw [← hdiv]
    field_simp [hx0]

/-- **Vanishing to order at least `k` is antitone in `k`.** -/
theorem vanishes_antitone {k m : ℕ} (hkm : k ≤ m) {f : ℝ → ℝ} {x₀ : ℝ}
    (h : VanishesToOrder m f x₀) : VanishesToOrder k f x₀ := by
  revert h
  induction hkm with
  | refl => exact fun h => h
  | step _ ih => exact fun h => ih (vanishes_succ_imp h)

/-- **Exact order `k`:** in the level-`k` filtration but not the level-`k+1` one. -/
def HasGrade (k : ℕ) (f : ℝ → ℝ) (x₀ : ℝ) : Prop :=
  VanishesToOrder k f x₀ ∧ ¬ VanishesToOrder (k + 1) f x₀

/-- **The canonical 0/0 has exact grade `k`.**  `(· - x₀)^k · h` with `h` continuous
at `x₀` and `h x₀ ≠ 0` lies in `F k` but not `F (k+1)`: the number of zeros is
exactly `k`. -/
theorem hasGrade_canonical {h : ℝ → ℝ} {x₀ : ℝ} (hh : ContinuousAt h x₀)
    (hh0 : h x₀ ≠ 0) (k : ℕ) :
    HasGrade k (fun x : ℝ => (x - x₀) ^ k * h x) x₀ := by
  refine ⟨⟨h, hh, ?_⟩, ?_⟩
  · filter_upwards with x; rfl
  · rintro ⟨g, hg, hfg⟩
    have hev : ∀ᶠ x in 𝓝[≠] x₀, h x = (x - x₀) * g x := by
      filter_upwards [hfg, eventually_mem_nhdsWithin] with x hfx hx
      have hx0 : x - x₀ ≠ 0 := sub_ne_zero.mpr hx
      have hk : (x - x₀) ^ k ≠ 0 := pow_ne_zero k hx0
      have hx' : (x - x₀) ^ k * h x = (x - x₀) ^ k * ((x - x₀) * g x) := by
        rw [hfx, pow_succ]
        ring
      exact mul_left_cancel₀ hk hx'
    have hcont : Tendsto (fun x : ℝ => (x - x₀) * g x) (𝓝[≠] x₀) (𝓝 0) := by
      have h1 : Tendsto (fun x : ℝ => x - x₀) (𝓝[≠] x₀) (𝓝 0) := by
        have hc : ContinuousAt (fun x : ℝ => x - x₀) x₀ :=
          continuousAt_id.sub continuousAt_const
        simpa using hc.mono_left nhdsWithin_le_nhds
      have h2 : Tendsto g (𝓝[≠] x₀) (𝓝 (g x₀)) := hg.mono_left nhdsWithin_le_nhds
      simpa using h1.mul h2
    have hht : Tendsto h (𝓝[≠] x₀) (𝓝 (h x₀)) := hh.mono_left nhdsWithin_le_nhds
    exact hh0 (tendsto_nhds_unique_of_eventuallyEq hht hcont hev)

/-- **The exact grade shifts by one under `divideOut`.** -/
theorem hasGrade_shift (k : ℕ) (f : ℝ → ℝ) (x₀ : ℝ) :
    HasGrade (k + 1) f x₀ ↔ HasGrade k (divideOut x₀ f) x₀ := by
  unfold HasGrade
  rw [vanishes_shift k f x₀, vanishes_shift (k + 1) f x₀]

/-- **The grade is well-defined.**  A function has at most one exact order of
vanishing at a point. -/
theorem grade_unique {k m : ℕ} {f : ℝ → ℝ} {x₀ : ℝ}
    (hk : HasGrade k f x₀) (hm : HasGrade m f x₀) : k = m := by
  rcases le_total k m with hkm | hmk
  · by_contra hne
    have hlt : k + 1 ≤ m := Nat.succ_le_iff.mpr (lt_of_le_of_ne hkm hne)
    exact hk.2 (vanishes_antitone hlt hm.1)
  · by_contra hne
    have hlt : m + 1 ≤ k := Nat.succ_le_iff.mpr (lt_of_le_of_ne hmk (Ne.symm hne))
    exact hm.2 (vanishes_antitone hlt hk.1)

/-- **The capstone: order of vanishing is a graded index.**  The vanishing sets form
a decreasing `ℕ`-filtration (`vanishes_succ_imp`), dividing out one zero shifts the
exact grade by one (`hasGrade_shift`), the grade is well-defined (`grade_unique`), and
the canonical `(· - x₀)^k · h` sits at exact grade `k` (`hasGrade_canonical`). -/
theorem order_is_graded :
    (∀ (k : ℕ) (f : ℝ → ℝ) (x₀ : ℝ),
        VanishesToOrder (k + 1) f x₀ → VanishesToOrder k f x₀) ∧
    (∀ (k : ℕ) (f : ℝ → ℝ) (x₀ : ℝ),
        HasGrade (k + 1) f x₀ ↔ HasGrade k (divideOut x₀ f) x₀) ∧
    (∀ (k m : ℕ) (f : ℝ → ℝ) (x₀ : ℝ), HasGrade k f x₀ → HasGrade m f x₀ → k = m) ∧
    (∀ (k : ℕ) (h : ℝ → ℝ) (x₀ : ℝ),
        ContinuousAt h x₀ → h x₀ ≠ 0 →
          HasGrade k (fun x : ℝ => (x - x₀) ^ k * h x) x₀) :=
  ⟨fun _ _ _ => vanishes_succ_imp,
   fun k f x₀ => hasGrade_shift k f x₀,
   fun _ _ _ _ => grade_unique,
   fun k _ _ hh hh0 => hasGrade_canonical hh hh0 k⟩

/-- Formalised-facts register for `VanishOrder.lean`. -/
def vanishOrderFacts : List String :=
  [ "VanishesToOrder", "divideOut", "vanishes_zero", "vanishes_succ_imp",
    "vanishes_shift", "HasGrade", "hasGrade_canonical", "hasGrade_shift",
    "vanishes_antitone", "grade_unique", "order_is_graded" ]

/-- The register has exactly eleven entries. -/
theorem vanishOrderFacts_length : vanishOrderFacts.length = 11 := by decide

end PunoCalculus.VanishOrder
