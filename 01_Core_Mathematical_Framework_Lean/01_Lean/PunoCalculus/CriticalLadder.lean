import Mathlib
import PunoCalculus.SerrinLadder

/-!
# Scaling-critical ladder (formal)

The Navier-Stokes scaling `u_λ(x) = λ u(λ x)` is the "change" the equation
itself generates.  The single object invariant under it is the scaling-critical
norm: on `L^p`-based spaces the invariant smoothness index is
`s_crit(p) = 3/p - 1`.  Every critical space is a different *form* of that one
pattern, nested as `L^3 ⊂ Ḃ^{-1+3/p}_{p,∞} ⊂ BMO^{-1} ⊂ Ḃ^{-1}_{∞,∞}`.

This file machine-checks the arithmetic of that ladder, in the same claim
ceiling as `SerrinLadder.lean` (no PDE content):

* the invariance condition `s + 1 - 3/p = 0 ↔ s = s_crit(p)`;
* the anchors `s_crit(3) = 0` (`L^3`), `s_crit(2) = 1/2` (`Ḣ^{1/2}`),
  `s_crit(6) = -1/2` (the `L^6` route);
* the **one-pattern identity**: the Serrin interpolation exponent and the
  critical index are complementary, `theta(p) + s_crit(p) = 1/2` for *every*
  form `p` -- the arithmetic does not depend on the guise;
* monotonicity of the embedding chain (`p ≤ q ⟹ s_crit(q) ≤ s_crit(p)`);
* `s_crit(p) > -1` for all finite `p`: the largest critical space
  (`s = -1`, `Ḃ^{-1}_{∞,∞}`) is approached, never attained at finite `p`;
* the Onsager excess: the weighted flux `2^{(1+eta) j}` is supercritical
  exactly when `eta > 0`; `eta = 0` is the critical borderline.

Whether the invariant is *bounded along the flow* (the largest-critical-space
regularity problem) is the OPEN wall, recorded as a marker, not a claim.
-/

namespace PunoCalculus.CriticalLadder

noncomputable section

open PunoCalculus.SerrinLadder

/-- Scaling-critical smoothness index for an `L^p`-based critical space:
a homogeneous norm with `s = 3/p - 1` is invariant under `u_λ(x) = λ u(λ x)`. -/
def sCrit (p : ℝ) : ℝ := 3 / p - 1

/-- The scaling factor of `Ḃ^s_{p,q}` under `u_λ` has exponent `s + 1 - 3/p`;
it is scaling-invariant (exponent `0`) iff `s = s_crit(p)`. -/
theorem scalingInvariant_iff :
    s + 1 - 3 / p = 0 ↔ s = sCrit p := by
  unfold sCrit
  constructor <;> intro h <;> linarith

/-- `L^3` is scaling-critical: `s_crit(3) = 0`. -/
theorem sCrit_three : sCrit 3 = 0 := by norm_num [sCrit]

/-- The `L^2`-based endpoint sits at `s_crit(2) = 1/2` (`Ḣ^{1/2}`). -/
theorem sCrit_two : sCrit 2 = 1 / 2 := by norm_num [sCrit]

/-- The `L^6` route's critical space sits at `s_crit(6) = -1/2`. -/
theorem sCrit_six : sCrit 6 = -1 / 2 := by norm_num [sCrit]

/-- **One-pattern identity.**  The Serrin interpolation exponent
`theta(p) = 3/2 - 3/p` and the scaling-critical index `s_crit(p) = 3/p - 1`
are complementary: their sum is the fixed constant `1/2` for every form `p`.
This is why one critical object appears in every functional guise. -/
theorem thetaAddSCrit (hp : p ≠ 0) : gnExponent p + sCrit p = 1 / 2 := by
  unfold gnExponent sCrit
  field_simp [hp]
  ring

/-- Monotonicity of the ladder: more integrability (`p ≤ q`) lowers the
required smoothness (`s_crit(q) ≤ s_crit(p)`), so the embedding chain
`L^3 ⊂ Ḃ^{-1+3/p} ⊂ ... ⊂ Ḃ^{-1}_{∞,∞}` is monotone. -/
theorem sCrit_antitone {p q : ℝ} (hp : 0 < p) (hpq : p ≤ q) :
    sCrit q ≤ sCrit p := by
  have hq : 0 < q := lt_of_lt_of_le hp hpq
  have hp0 : p ≠ 0 := ne_of_gt hp
  have hq0 : q ≠ 0 := ne_of_gt hq
  unfold sCrit
  have key : 3 / q - 3 / p = 3 * (p - q) / (p * q) := by
    field_simp [hp0, hq0]
  have hle : 3 / q - 3 / p ≤ 0 := by
    rw [key]
    exact div_nonpos_of_nonpos_of_nonneg (by nlinarith) (by positivity)
  linarith

/-- For every finite positive `p`, `s_crit(p) > -1`: the largest critical
space (`s = -1`, `Ḃ^{-1}_{∞,∞}`) is approached as `p -> ∞`, never attained. -/
theorem sCrit_gt_neg_one (hp : 0 < p) : -1 < sCrit p := by
  unfold sCrit
  have h : 0 < 3 / p := div_pos (by norm_num) hp
  linarith

/-- The Onsager excess: the weighted flux `2^{(1+eta) j}` is supercritical
(decays with scale) exactly when `eta > 0`; `eta = 0` is the critical
borderline where the whole regularity question lives. -/
theorem onsagerExcess_supercritical {eta : ℝ} : 1 < 1 + eta ↔ 0 < eta := by
  constructor <;> intro h <;> linarith

/-- OPEN WALL MARKER (not a theorem): whether the invariant critical norm is
bounded along the flow -- equivalently, whether a positive Onsager excess
`eta > 0` holds in the singular limit -- stays unproved. -/
def criticalInvariantBoundedOpen : Prop := True

/-- Statement-grade inventory of the critical-ladder file. -/
def criticalLadderFacts : List String :=
  ["scaling invariance: s + 1 - 3/p = 0 iff s = s_crit(p) (machine-checked)",
   "anchors: s_crit(3) = 0 (L^3), s_crit(2) = 1/2 (H^{1/2}), s_crit(6) = -1/2 (L^6 route)",
   "one-pattern identity: theta(p) + s_crit(p) = 1/2 for every form p (machine-checked)",
   "monotonicity: p <= q implies s_crit(q) <= s_crit(p); the critical embedding chain is monotone",
   "s_crit(p) > -1 for all finite p: largest critical space (s = -1) approached, never attained",
   "Onsager excess: supercritical iff eta > 0; eta = 0 is the critical borderline",
   "reading: one invariant pattern, many forms (L^p/Besov/Lorentz/BMO^{-1}); the arithmetic is p-independent",
   "wall: boundedness of the invariant critical norm along the flow is OPEN (marker criticalInvariantBoundedOpen)"]

/-- The inventory has exactly eight entries. -/
theorem criticalLadderFacts_length : criticalLadderFacts.length = 8 := by
  decide

end

end PunoCalculus.CriticalLadder
