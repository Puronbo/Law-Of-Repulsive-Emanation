import Mathlib
import PunoCalculus.ZeroZero

/-!
# The conic vertex as a removable 0/0

A parabola whose focus is the origin (the framework's "zero") and whose
vertex sits at radius `1/2` is the polar conic

  `r(θ) = l / (1 + e · cos θ)`,  with `l = 1`, `e = 1`,

i.e. `r(θ) = 1 / (1 + cos θ)`, `r(0) = 1/2`. The user's image — *zero as an
origin, a radius measured from it, a parabola dictating where the radius
changes, governed by its own parameters* — is exactly this object, and the
"point where the radius changes" is the **vertex**, where the radial excess
above the minimum is a removable 0/0:

  `(r(θ) − r(0)) / θ²  →  l·e / (2·(1+e)²)`  as `θ → 0`,

which for the vertex-at-`1/2` parabola is `1/8`.

This is the Vanishing-Rate mechanism in its purest form: a quantity that
vanishes quadratically, divided by `θ²`, yields a finite removable value that
is a curvature coefficient. Contrast the *escape to infinity* at `θ = π`,
where `1 + cos θ → 0` with a constant numerator — a genuine **pole**, not a
removable value (the Ising-heat-capacity situation, not the `sin x / x`
situation).

Every statement is a `Tendsto`, never an evaluation at the singular point,
matching the `PunoCalculus.ZeroZero` idiom.
-/

namespace PunoCalculus.ParabolaVertex

open Filter Topology
open scoped Topology

/-- The polar equation of a conic with one focus at the origin: the point at
distance `l / (1 + e * cos θ)` from the focus, `l` the semi-latus rectum and
`e` the eccentricity. `e = 1` is a parabola. -/
noncomputable def polar (l e θ : ℝ) : ℝ := l / (1 + e * Real.cos θ)

/-- The vertex radius: at `θ = 0` the radius is `l / (1 + e)`, the minimum of
`r` for `e ≥ 0`. For the vertex-at-`1/2` parabola (`l = e = 1`) this is `1/2`. -/
theorem polar_zero (l e : ℝ) : polar l e 0 = l / (1 + e) := by
  simp [polar, Real.cos_zero]

/-- The vertex-at-`1/2` parabola: `e = l = 1` gives `r(θ) = 1 / (1 + cos θ)`. -/
theorem polar_one_one (θ : ℝ) : polar 1 1 θ = 1 / (1 + Real.cos θ) := by
  simp [polar]

/-- Its vertex radius is exactly `1/2`. -/
theorem vertex_radius_one : polar 1 1 0 = 1 / 2 := by
  rw [polar_zero]; norm_num

/-- The radius function is **even**: `r(−θ) = r(θ)`. Hence the vertex is a
genuine two-sided extremum and the removable limit below is two-sided. -/
theorem polar_neg (l e θ : ℝ) : polar l e (-θ) = polar l e θ := by
  simp [polar, Real.cos_neg]

/-- Factoring the radial excess above the vertex, away from the polar
singularity: `r(θ) − r(0) = l·e·(1 − cos θ) / ((1 + e·cos θ)(1 + e))`. -/
theorem polar_sub_polar_zero (l e θ : ℝ) (hθ : 1 + e * Real.cos θ ≠ 0) (he : 1 + e ≠ 0) :
    polar l e θ - polar l e 0
      = l * e * (1 - Real.cos θ) / ((1 + e * Real.cos θ) * (1 + e)) := by
  rw [polar_zero]
  simp only [polar]
  field_simp
  ring

/-- **The vertex is a removable 0/0 with value `l·e / (2·(1+e)²)`.** The radial
excess above the vertex vanishes quadratically; divided by `θ²` it has the
finite removable value `l·e / (2·(1+e)²)` — a curvature coefficient governed by
the conic's own parameters `l` and `e`. -/
theorem vertex_removable (l e : ℝ) (he : 1 + e ≠ 0) :
    Tendsto (fun θ : ℝ => (polar l e θ - polar l e 0) / θ ^ 2)
      (𝓝[≠] 0) (𝓝 (l * e / (2 * (1 + e) ^ 2))) := by
  have hcont : Continuous (fun θ : ℝ => 1 + e * Real.cos θ) := by continuity
  have hev : ∀ᶠ θ in 𝓝[≠] 0, 1 + e * Real.cos θ ≠ 0 :=
    (hcont.continuousAt.eventually_ne (by simpa [Real.cos_zero] using he)).filter_mono
      nhdsWithin_le_nhds
  have hfact : Tendsto
      (fun θ : ℝ => (l * e / (1 + e)) * (((1 - Real.cos θ) / θ ^ 2)
        * (1 + e * Real.cos θ)⁻¹))
      (𝓝[≠] 0) (𝓝 ((l * e / (1 + e)) * ((1 / 2 : ℝ) * (1 + e)⁻¹))) := by
    have h1 : Tendsto (fun θ : ℝ => (1 - Real.cos θ) / θ ^ 2) (𝓝[≠] 0) (𝓝 (1 / 2 : ℝ)) :=
      PunoCalculus.ZeroZero.one_sub_cos_div_sq_tendsto_half
    have h2 : Tendsto (fun θ : ℝ => (1 + e * Real.cos θ)⁻¹) (𝓝[≠] 0)
        (𝓝 ((1 + e)⁻¹)) := by
      have hf : Tendsto (fun θ : ℝ => 1 + e * Real.cos θ) (𝓝 (0 : ℝ)) (𝓝 (1 + e)) := by
        simpa [Real.cos_zero] using hcont.tendsto 0
      exact (hf.inv₀ he).mono_left nhdsWithin_le_nhds
    exact tendsto_const_nhds.mul (h1.mul h2)
  have heq : (fun θ : ℝ => (polar l e θ - polar l e 0) / θ ^ 2) =ᶠ[𝓝[≠] 0]
      (fun θ : ℝ => (l * e / (1 + e)) * (((1 - Real.cos θ) / θ ^ 2)
        * (1 + e * Real.cos θ)⁻¹)) := by
    filter_upwards [hev, eventually_mem_nhdsWithin] with θ hθ hne
    rw [polar_sub_polar_zero l e θ hθ he]
    have hθ2 : θ ^ 2 ≠ 0 := pow_ne_zero 2 hne
    field_simp [hθ, he, hθ2, mul_ne_zero hθ he]
  have hval : (l * e / (1 + e)) * ((1 / 2 : ℝ) * (1 + e)⁻¹)
      = l * e / (2 * (1 + e) ^ 2) := by
    field_simp [he]
  rw [hval] at hfact
  exact Tendsto.congr' heq.symm hfact

/-- **The vertex-at-`1/2` parabola removes to `1/8`.** With `l = e = 1` the
removable value is `1·1 / (2·(1+1)²) = 1/8`. -/
theorem vertex_removable_one :
    Tendsto (fun θ : ℝ => (polar 1 1 θ - polar 1 1 0) / θ ^ 2)
      (𝓝[≠] 0) (𝓝 (1 / 8 : ℝ)) := by
  have h := vertex_removable 1 1 (by norm_num : (1 : ℝ) + 1 ≠ 0)
  have hval : (1 : ℝ) * 1 / (2 * (1 + 1) ^ 2) = 1 / 8 := by norm_num
  rwa [hval] at h

/-- Half-angle identity used for the pole sign analysis:
`1 + cos θ = 2·cos(θ/2)²`. -/
theorem one_add_cos_eq (θ : ℝ) : 1 + Real.cos θ = 2 * Real.cos (θ / 2) ^ 2 := by
  have h := Real.cos_two_mul' (θ / 2)
  have hs := Real.sin_sq_add_cos_sq (θ / 2)
  rw [show (2 : ℝ) * (θ / 2) = θ by ring] at h
  linarith

/-- Approaching the escape direction from below, `1 + cos θ → 0`. -/
theorem escape_denominator_tendsto_zero :
    Tendsto (fun θ : ℝ => 1 + Real.cos θ) (𝓝[<] Real.pi) (𝓝 0) := by
  have h : Tendsto (fun θ : ℝ => 1 + Real.cos θ) (𝓝 Real.pi) (𝓝 (0 : ℝ)) := by
    have hc : Continuous (fun θ : ℝ => 1 + Real.cos θ) := by continuity
    have h' := hc.tendsto Real.pi
    rw [Real.cos_pi] at h'
    norm_num at h'
    exact h'
  exact h.mono_left nhdsWithin_le_nhds

/-- Approaching the escape direction from below, `1 + cos θ → 0` **from the
right** (`0⁺`), since `1 + cos θ = 2·cos(θ/2)² > 0` for `θ` just below `π`. -/
theorem escape_denominator_tendsto_zero_pos :
    Tendsto (fun θ : ℝ => 1 + Real.cos θ) (𝓝[<] Real.pi) (𝓝[>] 0) := by
  rw [tendsto_nhdsWithin_iff]
  refine ⟨escape_denominator_tendsto_zero, ?_⟩
  have hIoi : Set.Ioi (Real.pi - 1) ∈ 𝓝[<] Real.pi :=
    mem_nhdsWithin_of_mem_nhds
      (isOpen_Ioi.mem_nhds (by rw [Set.mem_Ioi]; linarith [Real.pi_pos]))
  have hIio : Set.Iio Real.pi ∈ 𝓝[<] Real.pi := self_mem_nhdsWithin
  filter_upwards [hIoi, hIio] with θ hgt hlt
  have hgt' : Real.pi - 1 < θ := hgt
  have hlt' : θ < Real.pi := hlt
  rw [Set.mem_Ioi, one_add_cos_eq]
  have hhalf : Real.cos (θ / 2) > 0 := by
    apply Real.cos_pos_of_mem_Ioo
    constructor
    · linarith [hgt', Real.pi_gt_three]
    · linarith [hlt']
  have : 0 < Real.cos (θ / 2) ^ 2 := sq_pos_of_ne_zero (ne_of_gt hhalf)
  linarith [this]

/-- **The escape direction is a pole, not a removable value.** For the parabola
(`e = 1`) with `l > 0`, the radius `r(θ) = l / (1 + cos θ) → +∞` as `θ → π⁻`,
because the denominator tends to `0⁺`. This is the Ising-heat-capacity kind of
divergence, categorically different from the removable vertex 0/0. -/
theorem escape_pole (l : ℝ) (hl : 0 < l) :
    Tendsto (fun θ : ℝ => polar l 1 θ) (𝓝[<] Real.pi) atTop := by
  have hinv : Tendsto (fun θ : ℝ => (1 + Real.cos θ)⁻¹) (𝓝[<] Real.pi) atTop :=
    tendsto_inv_nhdsGT_zero.comp escape_denominator_tendsto_zero_pos
  have hcong : (fun θ : ℝ => polar l 1 θ) =ᶠ[𝓝[<] Real.pi]
      (fun θ : ℝ => l * (1 + Real.cos θ)⁻¹) := by
    filter_upwards with θ
    simp only [polar, one_mul, div_eq_mul_inv]
  exact Tendsto.congr' hcong.symm (hinv.const_mul_atTop hl)

/-- Register of rigorously established facts about the polar parabola. -/
def parabolaVertexFacts : List (String × String) :=
  [ ("vertex_radius", "r(0) = l / (1 + e); for l = e = 1 this is 1/2"),
    ("even", "r(-theta) = r(theta): the vertex is a genuine two-sided extremum"),
    ("vertex_removable", "re (r(theta) - r(0)) / theta^2 -> l*e / (2*(1+e)^2) as theta -> 0"),
    ("vertex_removable_one", "for l = e = 1 the removable value is 1/8"),
    ("escape_denominator", "1 + cos(theta) -> 0 as theta -> pi from below"),
    ("escape_pole", "r(theta) -> +infinity as theta -> pi^- for l > 0 (a pole, not 0/0)"),
    ("mirror", "the shadow x -> 1/x swaps the vertex radius 1/2 with 2 (see ShadowZeroZero)") ]

theorem parabolaVertexFacts_length : parabolaVertexFacts.length = 7 := by decide

end PunoCalculus.ParabolaVertex
