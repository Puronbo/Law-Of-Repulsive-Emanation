/-
  PunoCalculus.FirstCrossing

  The margin as a FIRST CROSSING -- no monotonicity needed.

  `MarginCrossing.lean` locates the register's margin `s*` as the UNIQUE zero of the
  orientation `lambda(s)`, which requires `lambda` to be strictly decreasing.  The
  third-family probe (`fractional_clm_margin.py`, fractional CLM) shows that hypothesis
  can FAIL: there the orientation is repelling at small `s`, crosses near a stable
  threshold, then hovers inside the noise floor over a broad band before crossing again --
  so the zero set need not be a single point.

  This brick replaces uniqueness by the WEAKEST hypothesis that still yields a margin:
  continuity plus a single sign change.  It proves the set of points where `f ≤ 0` has a
  least element `c` (closed and bounded below), that `c` is an interior zero, that `f > 0`
  strictly to the left of `c`, and hence that `c` is the FIRST zero -- no earlier one
  exists.  So a margin exists as a first crossing for ANY continuous orientation with a
  sign change; uniqueness is the extra (NS/Burgers-specific) content.

  -/

import Mathlib

namespace PunoCalculus.FirstCrossing

/-- **The first crossing exists without monotonicity.**  A continuous `f` on `[a,b]` with
`f a > 0 > f b` has a first zero `c` in the open interval `(a,b)`: the point where `f`
stops being positive is an interior zero, and `f > 0` strictly on `[a,c)`.  No monotonicity
is assumed, so the zero set may be larger than `{c}`. -/
theorem exists_first_zero {f : ℝ → ℝ} (hf : Continuous f) {a b : ℝ} (hab : a ≤ b)
    (ha : 0 < f a) (hb : f b < 0) :
    ∃ c ∈ Set.Ioo a b, f c = 0 ∧ ∀ x ∈ Set.Ico a c, 0 < f x := by
  have hmem : (0 : ℝ) ∈ Set.Icc (f b) (f a) := ⟨hb.le, ha.le⟩
  obtain ⟨z, hzIcc, hz0⟩ := (intermediate_value_Icc' hab hf.continuousOn) hmem
  have hzb : z ≠ b := by rintro rfl; exact hb.ne hz0
  set T : Set ℝ := Set.Icc a b ∩ f ⁻¹' Set.Iic 0 with hT
  have hzT : z ∈ T := ⟨hzIcc, le_of_eq hz0⟩
  have hTne : T.Nonempty := ⟨z, hzT⟩
  have hTclosed : IsClosed T := isClosed_Icc.inter (IsClosed.preimage hf isClosed_Iic)
  have hTbdd : BddBelow T := ⟨a, fun x hx => hx.1.1⟩
  set c : ℝ := sInf T with hc
  have hcmem : c ∈ T := hTclosed.csInf_mem hTne hTbdd
  have hcIcc : c ∈ Set.Icc a b := hcmem.1
  have hcnonpos : f c ≤ 0 := hcmem.2
  have hPa : a ∉ T := by
    intro hx
    have h2 : f a ≤ 0 := hx.2
    linarith [ha, h2]
  have hac : c ≠ a := by
    intro h
    rw [h] at hcmem
    exact hPa hcmem
  have hle : a ≤ c := le_csInf hTne (fun x hx => hx.1.1)
  have ha_lt_c : a < c := lt_of_le_of_ne hle (Ne.symm hac)
  have hc_le_z : c ≤ z := csInf_le hTbdd hzT
  have hc_lt_b : c < b := lt_of_le_of_lt hc_le_z (lt_of_le_of_ne hzIcc.2 hzb)
  have hpos : ∀ x ∈ Set.Ico a c, 0 < f x := by
    intro x hx
    have hxmem : x ∈ Set.Icc a b := ⟨hx.1, le_of_lt (lt_of_lt_of_le hx.2 hcIcc.2)⟩
    have hxnotT : x ∉ T := by
      intro hxT
      have hle' : c ≤ x := csInf_le hTbdd hxT
      linarith [hx.2]
    have : ¬ f x ≤ 0 := fun hle0 => hxnotT ⟨hxmem, hle0⟩
    exact not_le.mp this
  refine ⟨c, ⟨ha_lt_c, hc_lt_b⟩, ?_, hpos⟩
  obtain ⟨w, hwIcc, hw0⟩ := (intermediate_value_Icc' hle hf.continuousOn)
    (show (0 : ℝ) ∈ Set.Icc (f c) (f a) from ⟨hcnonpos, ha.le⟩)
  rcases lt_or_eq_of_le hwIcc.2 with hwlt | hweq
  · have hwpos : 0 < f w := hpos w ⟨hwIcc.1, hwlt⟩
    linarith
  · rw [← hweq]; exact hw0

/-- **The margin exists as a first crossing.**  The same hypotheses give an interior zero
`c` with `f > 0` strictly to its left and NO earlier zero anywhere in `(a, c)`.  This is
the existence half of the register's margin statement, freed of the antitone hypothesis
that `MarginCrossing.margin_existsUnique` requires. -/
theorem margin_exists_firstCrossing {f : ℝ → ℝ} (hf : Continuous f) {a b : ℝ} (hab : a ≤ b)
    (ha : 0 < f a) (hb : f b < 0) :
    ∃ c, c ∈ Set.Ioo a b ∧ f c = 0 ∧ (∀ x ∈ Set.Ico a c, 0 < f x) ∧
      (∀ d ∈ Set.Ioo a c, f d ≠ 0) := by
  obtain ⟨c, hcIoo, hc0, hpos⟩ := exists_first_zero hf hab ha hb
  exact ⟨c, hcIoo, hc0, hpos, fun d hd => ne_of_gt (hpos d ⟨hd.1.le, hd.2⟩)⟩

/-- The three facts of this brick. -/
def firstCrossingFacts : List String :=
  ["exists_first_zero", "margin_exists_firstCrossing"]

theorem firstCrossingFacts_length : firstCrossingFacts.length = 2 := rfl

end PunoCalculus.FirstCrossing
