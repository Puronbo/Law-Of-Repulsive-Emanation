import Mathlib
import PunoCalculus.ZeroZero

/-!
# The shadow mechanism: the reciprocal mirror `x ↦ 1/x`

The framework calls one mechanism the *shadow* of another
(`THE_WEB_OF_PROOFS.md`: "Critical Phenomenon is the physical shadow of Vanishing
Rate") and reads a concrete instance as the *finite image* a mechanism casts on a
computable domain ("the integer shadow of √2"; "`log 0` is the numeric shadow of
the divergence").  This file gives the one shadow that is a genuine *algebraic
involution*: the reciprocal mirror `σ x = x⁻¹`.

Two facts are formalised, and they are deliberately **different**, which is exactly
the point `ZeroZero.lean` makes when it refuses to conflate `∞/∞` with `0/0`:

* **Relocation (value-preserving).**  Composing a removable-`0/0` ratio with `σ`
  moves the singular point `0 → ∞` and keeps the removable value: if `r → L` on the
  right of `0`, then `r ∘ σ → L` at `+∞` (`shadow_preserves_value`), and `σ` is an
  involution (`shadow_involution`).  The removable value is a *mirror invariant*.

* **Inversion (the `0/0 ↔ ∞/∞` mirror).**  The term-reciprocal of the shadow,
  `(r ∘ σ)⁻¹`, is the shape in which numerator and denominator diverge when `r`'s
  do not; its removable value is `L⁻¹` (`shadow_inverts_value`).  So the two
  operations -- *relocate the point* versus *invert the terms* -- must not be
  identified: only the second changes the form `0/0 → ∞/∞`, and it inverts the
  value while the first preserves it.

This mirrors the register's own "shadow" bookkeeping: every claim has a
`Falsifier`, and every mechanism its reverse; here the reverse of the variable
mirror is proved exact (`σ` is an involution), whereas the register records that
other, dynamical reverses fail (`WEAVERS_SCRIBE.md`: T-symmetry refuted, the
integer tree mirror fails).

Scope, as everywhere: a statement about limits on a punctured neighbourhood and
real field algebra.  No value is created -- the mirror only relocates or inverts a
removable value that is already there, and it never evaluates a quotient *at* a
singular point.
-/

noncomputable section

namespace PunoCalculus.ShadowZeroZero

open Filter
open scoped Topology

/-- The shadow map: the reciprocal mirror `σ x = x⁻¹`.  On the right of `0` it
sends the punctured neighbourhood out to `+∞`. -/
def shadow (r : ℝ → ℝ) : ℝ → ℝ := fun t => r t⁻¹

/-- `σ` is an involution: `σ (σ r) = r`.  The variable mirror is its own reverse. -/
theorem shadow_involution (r : ℝ → ℝ) : shadow (shadow r) = r := by
  funext t
  simp [shadow, inv_inv]

/-- `t ↦ t⁻¹` maps `+∞` to the right punctured neighbourhood `𝓝[>] 0`. -/
theorem tendsto_inv_atTop_nhdsGT_zero_R :
    Tendsto (fun t : ℝ => t⁻¹) atTop (𝓝[>] (0 : ℝ)) :=
  tendsto_inv_atTop_nhdsGT_zero

/-- **Value-preserving relocation.**  A removable value on the right of `0` is the
removable value of the shadow at `+∞`: the mirror moves the singularity, not the
value. -/
theorem shadow_preserves_value (f g : ℝ → ℝ) {L : ℝ}
    (h : Tendsto (fun x : ℝ => f x / g x) (𝓝[>] (0 : ℝ)) (𝓝 L)) :
    Tendsto (fun t : ℝ => f t⁻¹ / g t⁻¹) atTop (𝓝 L) :=
  h.comp tendsto_inv_atTop_nhdsGT_zero_R

/-- Two-sided form: a removable `0/0` at `0` has the same removable value at `+∞`
after the mirror (the two-sided limit restricts to the right one). -/
theorem shadow_preserves_value_of_ne (f g : ℝ → ℝ) {L : ℝ}
    (h : Tendsto (fun x : ℝ => f x / g x) (𝓝[≠] (0 : ℝ)) (𝓝 L)) :
    Tendsto (fun t : ℝ => f t⁻¹ / g t⁻¹) atTop (𝓝 L) :=
  shadow_preserves_value f g
    (h.mono_left (nhdsWithin_mono 0 (fun _ hx => ne_of_gt hx)))

/-- **The `0/0 ↔ ∞/∞` inversion.**  Reciprocal of the shadow: when the shadow's
removable value is `L ≠ 0`, its term-reciprocal has removable value `L⁻¹`.  This is
the shape in which both numerator and denominator diverge -- the `∞/∞` mirror of
`0/0` -- and it inverts the value, unlike the relocation above. -/
theorem shadow_inverts_value (r : ℝ → ℝ) {L : ℝ}
    (h : Tendsto r (𝓝[>] (0 : ℝ)) (𝓝 L)) (hL : L ≠ 0) :
    Tendsto (fun t : ℝ => (r t⁻¹)⁻¹) atTop (𝓝 L⁻¹) :=
  (h.comp tendsto_inv_atTop_nhdsGT_zero_R).inv₀ hL

/-- The concrete instance: `sin x / x → 1` at `0⁺`, so its shadow
`sin (1/t) / (1/t) → 1` at `+∞`.  The `0/0` at the origin and the `0/0` at infinity
carry the same removable value `1`, read through the mirror. -/
theorem shadow_sin_over_x :
    Tendsto (fun t : ℝ => Real.sin t⁻¹ / t⁻¹) atTop (𝓝 1) :=
  shadow_preserves_value_of_ne Real.sin (fun x : ℝ => x)
    PunoCalculus.ZeroZero.sin_x_div_tendsto_one

/-- Formalised-facts register for `ShadowZeroZero.lean`. -/
def shadowZeroZeroFacts : List String :=
  [ "shadow", "shadow_involution", "tendsto_inv_atTop_nhdsGT_zero_R",
    "shadow_preserves_value", "shadow_preserves_value_of_ne",
    "shadow_inverts_value", "shadow_sin_over_x" ]

/-- The register has exactly seven entries. -/
theorem shadowZeroZeroFacts_length : shadowZeroZeroFacts.length = 7 := by
  decide

end PunoCalculus.ShadowZeroZero
