/-
  PunoCalculus.MarginCrossing

  The margin as a UNIQUE CROSSING.

  The register's order/orientation probe measures an orientation
  `lambda(s) = d/dt log(Z_high / Z_low)` as a function of the dissipation order `s`.
  Empirically `lambda` is ANTITONE in `s` (weak high-`k` dissipation repels, strong
  dissipation attracts), so the critical order `s*` -- the margin where the orientation
  flips sign -- is the UNIQUE zero of `lambda`.

  That empirical uniqueness is, at bottom, a theorem of real analysis: a continuous,
  strictly decreasing function on an interval that is positive at the left endpoint and
  negative at the right endpoint has exactly one zero there.  This brick proves it, so
  the register's margin is well-defined the moment antitonicity holds.  (The register's
  open content is not this arithmetic but the NS-specific ANTITONICITY of `lambda`.)

  Axioms: [propext, Classical.choice, Quot.sound]; the length certificate is
  axiom-free (`decide`).

  Author: Michael Grafiel S Puno
-/

import Mathlib

namespace PunoCalculus.MarginCrossing

/-- **The margin is a unique crossing.**  A function continuous on `[a,b]`, strictly
decreasing there, positive at `a` and negative at `b`, has exactly one zero in `(a,b)`.
This is the arithmetic core of the register's margin: `lambda` antitone in the
dissipation order `s` makes the critical order `s*` unique. -/
theorem existsUnique_zero_of_strictAntiOn {f : ℝ → ℝ} {a b : ℝ} (hab : a < b)
    (hf : ContinuousOn f (Set.Icc a b)) (hanti : StrictAntiOn f (Set.Icc a b))
    (ha : 0 < f a) (hb : f b < 0) :
    ∃! c ∈ Set.Ioo a b, f c = 0 := by
  have hmem : (0 : ℝ) ∈ Set.Icc (f b) (f a) := ⟨hb.le, ha.le⟩
  obtain ⟨c, hcIcc, hc0⟩ := (intermediate_value_Icc' hab.le hf) hmem
  have hc_ne_a : c ≠ a := by rintro rfl; exact ha.ne' hc0
  have hc_ne_b : c ≠ b := by rintro rfl; exact hb.ne hc0
  have hcIoo : c ∈ Set.Ioo a b :=
    ⟨lt_of_le_of_ne hcIcc.1 (Ne.symm hc_ne_a), lt_of_le_of_ne hcIcc.2 hc_ne_b⟩
  have hcmem : c ∈ Set.Icc a b := ⟨hcIoo.1.le, hcIoo.2.le⟩
  refine ⟨c, ⟨hcIoo, hc0⟩, ?_⟩
  intro d hd
  obtain ⟨hdIoo, hd0⟩ := hd
  have hdmem : d ∈ Set.Icc a b := ⟨hdIoo.1.le, hdIoo.2.le⟩
  rcases lt_trichotomy d c with hlt | heq | hgt
  · have hcon : f c < f d := hanti hdmem hcmem hlt
    rw [hc0, hd0] at hcon
    exact absurd hcon (lt_irrefl (0 : ℝ))
  · exact heq
  · have hcon : f d < f c := hanti hcmem hdmem hgt
    rw [hc0, hd0] at hcon
    exact absurd hcon (lt_irrefl (0 : ℝ))

/-- **Which side of the wall.**  The same hypotheses place every point left of the
unique crossing on the REPELLING side (`f > 0`) and every point right of it on the
attracting side (`f < 0`).  So the marginal order `s*` separates the two orientations. -/
theorem side_of_crossing {f : ℝ → ℝ} {a b c x : ℝ}
    (hanti : StrictAntiOn f (Set.Icc a b))
    (hc : c ∈ Set.Ioo a b) (hc0 : f c = 0) (hx : x ∈ Set.Icc a b) :
    (x < c → 0 < f x) ∧ (c < x → f x < 0) := by
  have hcmem : c ∈ Set.Icc a b := ⟨hc.1.le, hc.2.le⟩
  refine ⟨fun hlt => ?_, fun hgt => ?_⟩
  · have hcon : f c < f x := hanti hx hcmem hlt
    rwa [hc0] at hcon
  · have hcon : f x < f c := hanti hcmem hx hgt
    rwa [hc0] at hcon

/-- **Existence and uniqueness together.**  Under antitonicity with a strict sign change
on `[a,b]`, the marginal order exists and is unique.  This is the register's margin
statement, conditional only on `lambda` being antitone. -/
theorem margin_existsUnique {f : ℝ → ℝ} {a b : ℝ} (hab : a < b)
    (hf : ContinuousOn f (Set.Icc a b)) (hanti : StrictAntiOn f (Set.Icc a b))
    (ha : 0 < f a) (hb : f b < 0) :
    ∃! s : ℝ, s ∈ Set.Ioo a b ∧ f s = 0 ∧ (∀ x ∈ Set.Ioo a s, 0 < f x) ∧
      (∀ x ∈ Set.Ioo s b, f x < 0) := by
  obtain ⟨c, hc, huniq⟩ := existsUnique_zero_of_strictAntiOn hab hf hanti ha hb
  obtain ⟨hcIoo, hc0⟩ := hc
  refine ⟨c, ⟨hcIoo, hc0, ?_, ?_⟩, ?_⟩
  · intro x hx
    have hxb : x ∈ Set.Icc a b := ⟨hx.1.le, le_trans hx.2.le hcIoo.2.le⟩
    exact (side_of_crossing hanti hcIoo hc0 hxb).1 hx.2
  · intro x hx
    have hxb : x ∈ Set.Icc a b := ⟨le_trans hcIoo.1.le hx.1.le, hx.2.le⟩
    exact (side_of_crossing hanti hcIoo hc0 hxb).2 hx.1
  · intro d hd
    exact huniq d ⟨hd.1, hd.2.1⟩

/-- Formalised-facts register for `MarginCrossing.lean`. -/
def marginCrossingFacts : List String :=
  [ "existsUnique_zero_of_strictAntiOn", "side_of_crossing", "margin_existsUnique" ]

/-- The register has exactly three entries. -/
theorem marginCrossingFacts_length : marginCrossingFacts.length = 3 := by decide

end PunoCalculus.MarginCrossing
