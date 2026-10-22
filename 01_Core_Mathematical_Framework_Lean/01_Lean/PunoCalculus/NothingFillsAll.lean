import Mathlib
import PunoCalculus.NullAbundance

/-!
# Nothing and something filling everything

The register's `0/0` arc was about a *value* that fails to exist at a point.  This module is
about the complementary phenomenon: a point where **nothing exists everywhere** and the
whole is nonetheless **something**.

The precise, provable shape of that sentence is:

* Every point of `ℝ` is *nothing* — a null singleton.
* The whole line is the union of all of them.  **Nothing fills everything.**
* The whole line is *not* nothing — it has infinite measure.  **Something remains.**
* No **countable** family of null sets can cover even one interval.  So the filling that
  does occur is an *uncountable* phenomenon, and uncountability is exactly the hinge.
* Every **finite** stage of the pile-up is nothing, and the **infinite** stage is
  everything.  The accumulation does not converge; it *jumps*.

That last line is the one that matters for the register, because it is the same shape as
the essential singularity:

| family of nothings | the accumulation | the register's word |
|---|---|---|
| a countable family of null sets | its union is still null — the limit **exists** | **removable** |
| all the points of `ℝ` | the union is everything — the limit **does not exist** | **essential** |

A countable pile of nullities resolves to nullity; the pile of *all* nullities resolves to
everything.  The supremum of the stages is the same in both cases (nothing), yet the
outcomes differ, so the stages do not determine the outcome.  This is the measure-theoretic
counterpart of `x / x = 1` on one channel and `2 * x / x = 2` on another: the same form,
the same origin, and the answer depends on which family you accumulate.

Nothing here is open.  It is elementary measure theory, kernel-checked.
-/

namespace PunoCalculus.NothingFillsAll

open MeasureTheory Set

/-! ## Nothing fills everything -/

/-- **Nothing fills everything.**  The whole line is literally nothing piled up: every piece
of it is a null singleton, and there are enough of them to cover the whole. -/
theorem nothing_fills_everything :
    (Set.univ : Set ℝ) = ⋃ x : ℝ, ({x} : Set ℝ) := by
  ext x; simp

/-- **And something remains.**  The pile-up is everything: the whole line has infinite
measure.  Nothing was ever added — the measure was always there, in the cardinality. -/
theorem something_remains : volume (Set.univ : Set ℝ) = ⊤ := by
  simp

/-- The whole is not nothing.  This is the sentence that the union above makes
non-paradoxical: the pieces are all null, the whole is not. -/
theorem the_whole_is_not_nothing : volume (Set.univ : Set ℝ) ≠ 0 := by
  rw [something_remains]; simp

/-! ## But countably many nothings stay nothing -/

/-- **Countably many nothings stay nothing.**  The measure of a countable union of null sets
is null — no measurability hypothesis needed, and no exception for infinite families.  The
index is any countable type, not just `ℕ`. -/
theorem countable_nothings_stay_nothing {ι : Type*} [Countable ι] (f : ι → Set ℝ)
    (h : ∀ i, volume (f i) = 0) : volume (⋃ i, f i) = 0 :=
  (measure_iUnion_null_iff).2 h

/-- **The switch, negative side.**  The whole line cannot be covered by a countable family
of null sets.  So the filling above is an uncountable phenomenon, and countability is the
exact hinge between "a pile of nothing" and "everything". -/
theorem no_countable_filling {ι : Type*} [Countable ι] :
    ¬ ∃ f : ι → Set ℝ, (∀ i, volume (f i) = 0) ∧ (Set.univ : Set ℝ) = ⋃ i, f i := by
  rintro ⟨f, hf, hunion⟩
  have hz : volume (⋃ i, f i) = 0 := countable_nothings_stay_nothing f hf
  rw [← hunion] at hz
  exact the_whole_is_not_nothing hz

/-- **Nowhere near covering.**  A countable pile of nothing cannot cover even one closed
interval of positive length.  Countable nothing can be *everywhere* (dense) but never
*covering* — the two senses of "everywhere" come apart. -/
theorem countable_nothings_cover_no_interval (f : ℕ → Set ℝ) (h : ∀ n, volume (f n) = 0)
    (a b : ℝ) (hab : a < b) : ¬ (Set.Icc a b : Set ℝ) ⊆ (⋃ (n : ℕ), f n) := by
  intro hsub
  have hz : volume (⋃ (n : ℕ), f n) = 0 := countable_nothings_stay_nothing f h
  have hz' : volume (Set.Icc a b : Set ℝ) = 0 := measure_mono_null hsub hz
  rw [Real.volume_Icc] at hz'
  have hpos : (0 : ℝ) < b - a := by linarith
  exact ENNReal.ofReal_ne_zero_iff.mpr hpos hz'

/-- **The something is the cardinality.**  The filling that does occur cannot be a countable
one; the reals are not countable to begin with. -/
theorem the_filling_is_uncountable : ¬ (Set.univ : Set ℝ).Countable :=
  Cardinal.not_countable_real

/-! ## The essential jump: nothing at every finite stage, everything at the end -/

/-- Every **finite** stage of the pile-up is nothing: finitely many null singletons are
null. -/
theorem every_finite_stage_is_nothing (F : Finset ℝ) :
    volume (⋃ x ∈ F, ({x} : Set ℝ)) = 0 :=
  (measure_biUnion_null_iff F.countable_toSet).2 fun _ _ => measure_singleton _

/-- No finite stage reaches the whole.  The jump is real, not an artefact of the index. -/
theorem finite_stages_never_reach_the_whole (F : Finset ℝ) :
    volume (⋃ x ∈ F, ({x} : Set ℝ)) ≠ volume (Set.univ : Set ℝ) := by
  rw [something_remains]
  intro h
  have : volume (⋃ x ∈ F, ({x} : Set ℝ)) = ⊤ := h
  rw [every_finite_stage_is_nothing F] at this
  simp at this

/-- **The essential accumulation.**  At every finite stage the pile-up is nothing; at the
infinite stage it is everything.  There is no value in between, and no limit to speak of:
this is the measure-theoretic image of an essential singularity, where the accumulation of
infinitely many nullities is *not* removable. -/
theorem nothing_at_finite_stages_everything_at_the_end :
    (∀ F : Finset ℝ, volume (⋃ x ∈ F, ({x} : Set ℝ)) = 0) ∧
      volume (Set.univ : Set ℝ) = ⊤ :=
  ⟨every_finite_stage_is_nothing, something_remains⟩

/-- **The switch, stated as one theorem.**  A countable accumulation of nothing *resolves* —
its value is nothing.  The accumulation of *all* nothing does not resolve — it jumps from
nothing to everything.  The stages are the same in both cases; only the cardinality of the
family differs.  Countability is the hinge, and it is the hinge the register cares about:
an infinite accumulation of nullities is not a removable singularity. -/
theorem accumulation_resolves_countably_but_not_uncountably :
    (∀ f : ℕ → Set ℝ, (∀ n, volume (f n) = 0) → volume (⋃ (n : ℕ), f n) = 0) ∧
      ((∀ F : Finset ℝ, volume (⋃ x ∈ F, ({x} : Set ℝ)) = 0) ∧
        volume (Set.univ : Set ℝ) = ⊤) :=
  ⟨countable_nothings_stay_nothing, nothing_at_finite_stages_everything_at_the_end⟩

/-- **Nowhere without covering.**  Countable nothing may be dense — the rationals sit
everywhere and measure nothing — but it can never *cover* an interval.  Covering is what
requires uncountability.  So "everywhere" and "filling" are genuinely two different
things, and the register's "nothing and something" is exactly the case where both hold at
once. -/
theorem nowhere_without_covering :
    Dense (Set.range ((↑) : ℚ → ℝ)) ∧
      volume (Set.range ((↑) : ℚ → ℝ)) = 0 ∧
      (∀ (f : ℕ → Set ℝ), (∀ n, volume (f n) = 0) →
        ∀ a b : ℝ, a < b → ¬ (Set.Icc a b : Set ℝ) ⊆ (⋃ (n : ℕ), f n)) :=
  ⟨NullAbundance.rationals_dense, NullAbundance.rationals_null_and_dense.1,
    countable_nothings_cover_no_interval⟩

end PunoCalculus.NothingFillsAll
