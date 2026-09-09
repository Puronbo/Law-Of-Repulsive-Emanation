import Mathlib

open Filter
open scoped Interval Topology MeasureTheory

/-!
# Twin analytic laws (Lean 4, mathlib)

Machine-checked closed forms behind the discrete twin's NLSE laws.
The Peregrine crest profile is real-valued:

    u(t) = sqrt(P) * (1 - 4 / (1 + 4 P t^2))

and its mass defect density rho(t) = |u(t)|^2 - P simplifies to

    rho(t) = 8 P (1 - 4 P t^2) / (1 + 4 P t^2)^2.

Since d/dt [ t/(1+4Pt^2) ] = (1 - 4 P t^2)/(1 + 4 P t^2)^2, the window
integral is exactly the boundary term (no transcendentals):

    int_(-a)^(a) rho = 8 P [ G(a) - G(-a) ] = 16 P a/(1 + 4 P a^2).

At a = L/2 this is 8 P L/(1 + P L^2), the documented closed form
8 L/(1 + L^2) at P = 1.  As a -> infinity the RHS tends to 0, which
is the breather's mass neutrality on the full line.
-/

namespace PunoTwin

/-- Peregrine crest profile (real seed of the twin). -/
noncomputable def peregrine (P t : ℝ) : ℝ :=
  Real.sqrt P * (1 - 4 / (1 + 4 * P * t ^ 2))

/-- Mass defect density |u|^2 - P, expressed without sqrt. -/
noncomputable def peregrineRho (P t : ℝ) : ℝ :=
  P * (16 / (1 + 4 * P * t ^ 2) ^ 2 - 8 / (1 + 4 * P * t ^ 2))

/-- Simplified form of the density: rho = 8P(1-4Pt^2)/(1+4Pt^2)^2. -/
theorem rho_eq_structure (hP : 0 < P) :
    (fun t : ℝ => peregrineRho P t) =
      fun t : ℝ => 8 * P * ((1 - 4 * P * t ^ 2) / (1 + 4 * P * t ^ 2) ^ 2) := by
  funext t
  have hden : 0 < 1 + 4 * P * t ^ 2 := by positivity
  dsimp [peregrineRho]
  field_simp [hden.ne']
  ring_nf

/-- The density is literally |u|^2 - P for the real profile. -/
theorem rho_eq_abs_profile (hP : 0 < P) :
    (fun t : ℝ => peregrineRho P t) = fun t : ℝ => (peregrine P t) ^ 2 - P := by
  funext t
  have hsqrt : (Real.sqrt P) ^ 2 = P := Real.sq_sqrt hP.le
  dsimp [peregrineRho, peregrine]
  field_simp [hP.ne']
  ring_nf
  rw [hsqrt]
  ring_nf

private lemma deriv_id_lam (x : ℝ) : deriv (fun s : ℝ => s) x = 1 := by
  exact deriv_id x

private lemma deriv_poly_1_quad (P t : ℝ) :
    deriv (fun s : ℝ => 1 + 4 * P * s ^ 2) t = 8 * P * t := by
  have hd1 : DifferentiableAt ℝ (fun s : ℝ => (1 : ℝ)) t := by fun_prop
  have hd2 : DifferentiableAt ℝ (fun s : ℝ => 4 * P * s ^ 2) t := by fun_prop
  have hsq : DifferentiableAt ℝ (fun s : ℝ => s) t := by fun_prop
  have hsq_d : DifferentiableAt ℝ (fun s : ℝ => s ^ 2) t := by fun_prop
  have hdersq : deriv (fun s : ℝ => s ^ 2) t = 2 * t := by
    rw [show (fun s : ℝ => s ^ 2) = fun s : ℝ => s * s by funext s; ring]
    rw [show (fun s : ℝ => s * s) = (fun s : ℝ => s) * (fun s : ℝ => s) by rfl]
    rw [deriv_mul hsq hsq, deriv_id_lam t]
    ring_nf
  rw [show (fun s : ℝ => 1 + 4 * P * s ^ 2) = (fun s : ℝ => (1 : ℝ)) + (fun s : ℝ => 4 * P * s ^ 2) by rfl]
  rw [deriv_add hd1 hd2, deriv_const, deriv_const_mul (4 * P) hsq_d, hdersq]
  ring

private lemma deriv_density (hP : 0 < P) (t : ℝ) :
    deriv (fun s : ℝ => s / (1 + 4 * P * s ^ 2)) t =
      (1 - 4 * P * t ^ 2) / (1 + 4 * P * t ^ 2) ^ 2 := by
  have hd_id : DifferentiableAt ℝ (fun s : ℝ => s) t := by fun_prop
  have hd_poly : DifferentiableAt ℝ (fun s : ℝ => 1 + 4 * P * s ^ 2) t := by fun_prop
  have hden : 1 + 4 * P * t ^ 2 ≠ 0 := by positivity
  rw [show (fun s : ℝ => s / (1 + 4 * P * s ^ 2)) =
      (fun s : ℝ => s) / (fun s : ℝ => 1 + 4 * P * s ^ 2) by rfl]
  rw [deriv_div hd_id hd_poly hden]
  rw [deriv_id_lam t, deriv_poly_1_quad P t]
  field_simp [hden]
  ring_nf

/-- Exact derivative of the antiderivative part. -/
theorem antiderivative_deriv (hP : 0 < P) (t : ℝ) :
    deriv (fun s : ℝ => s / (1 + 4 * P * s ^ 2)) t =
      (1 - 4 * P * t ^ 2) / (1 + 4 * P * t ^ 2) ^ 2 :=
  deriv_density hP t

/-- Pointwise HasDerivAt form. -/
theorem antiderivative_hasDerivAt (hP : 0 < P) (t : ℝ) :
    HasDerivAt (fun s : ℝ => s / (1 + 4 * P * s ^ 2))
      ((1 - 4 * P * t ^ 2) / (1 + 4 * P * t ^ 2) ^ 2) t := by
  rw [← antiderivative_deriv hP t]
  have hden : 1 + 4 * P * t ^ 2 ≠ 0 := by positivity
  have hd : DifferentiableAt ℝ (fun s : ℝ => s / (1 + 4 * P * s ^ 2)) t := by fun_prop
  exact hd.hasDerivAt

/-- The exact window defect: int_(-a)^(a) rho = 16 P a / (1 + 4 P a^2). -/
theorem window_defect_exact (hP : 0 < P) (ha : 0 < a) :
    (∫ t in -a..a, peregrineRho P t) = 16 * P * a / (1 + 4 * P * a ^ 2) := by
  rw [rho_eq_structure hP]
  have hG : (fun t : ℝ => 8 * P * ((1 - 4 * P * t ^ 2) / (1 + 4 * P * t ^ 2) ^ 2)) =
      fun t : ℝ => 8 * P * deriv (fun s : ℝ => s / (1 + 4 * P * s ^ 2)) t := by
    funext t
    rw [antiderivative_deriv hP t]
  rw [hG]
  rw [intervalIntegral.integral_const_mul]
  have hhderiv : ∀ x ∈ Set.uIcc (-a) a,
      DifferentiableAt ℝ (fun s : ℝ => s / (1 + 4 * P * s ^ 2)) x := by
    intro x hx
    exact (antiderivative_hasDerivAt hP x).differentiableAt
  have hcont_dens : ContinuousOn
      (fun t : ℝ => (1 - 4 * P * t ^ 2) / (1 + 4 * P * t ^ 2) ^ 2) (Set.uIcc (-a) a) := by
    refine Continuous.continuousOn ?_
    have hnum : Continuous (fun t : ℝ => 1 - 4 * P * t ^ 2) := by fun_prop
    have hden : Continuous (fun t : ℝ => (1 + 4 * P * t ^ 2) ^ 2) := by fun_prop
    have hden_ne : ∀ t : ℝ, (1 + 4 * P * t ^ 2) ^ 2 ≠ 0 := by
      intro t
      positivity
    exact hnum.div hden hden_ne
  have hderiv_eq : (fun t : ℝ => deriv (fun s : ℝ => s / (1 + 4 * P * s ^ 2)) t) =
      fun t : ℝ => (1 - 4 * P * t ^ 2) / (1 + 4 * P * t ^ 2) ^ 2 := by
    funext t
    rw [antiderivative_deriv hP t]
  have hint : IntervalIntegrable (fun t : ℝ =>
      deriv (fun s : ℝ => s / (1 + 4 * P * s ^ 2)) t) MeasureTheory.volume (-a) a := by
    rw [hderiv_eq]
    exact (hcont_dens.intervalIntegrable : IntervalIntegrable
      (fun t : ℝ => (1 - 4 * P * t ^ 2) / (1 + 4 * P * t ^ 2) ^ 2) MeasureTheory.volume (-a) a)
  have hft := intervalIntegral.integral_deriv_eq_sub hhderiv hint
  have hvalue : (fun s : ℝ => s / (1 + 4 * P * s ^ 2)) a -
      (fun s : ℝ => s / (1 + 4 * P * s ^ 2)) (-a) = 2 * a / (1 + 4 * P * a ^ 2) := by
    have hden : 0 < 1 + 4 * P * a ^ 2 := by positivity
    field_simp [hden.ne']
    ring_nf
  rw [hft]
  rw [hvalue]
  field_simp [hP.ne', ha.ne']
  ring_nf

/-- At a = L/2 the defect is exactly the documented closed form 8 P L/(1 + P L^2). -/
theorem defect_at_L (hP : 0 < P) (L : ℝ) :
    16 * P * (L / 2) / (1 + 4 * P * (L / 2) ^ 2) = 8 * P * L / (1 + P * L ^ 2) := by
  have hden : 0 < 1 + P * L ^ 2 := by positivity
  field_simp [hden.ne']
  ring_nf

/-- Full-line mass neutrality for the Peregrine breather: as the half
    window a grows, the measured defect 16 P a/(1 + 4 P a^2) tends to 0. -/
theorem defect_tendsto_zero (hP : 0 < P) :
    Tendsto (fun b : ℝ => 16 * P * b / (1 + 4 * P * b ^ 2)) atTop (𝓝 0) := by
  set r : ℝ → ℝ := fun b => 16 * P * b / (1 + 4 * P * b ^ 2)
  have ht4 : Tendsto (fun b : ℝ => 4 / b) atTop (𝓝 0) := by
    simpa [div_eq_mul_inv] using
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => (4 : ℝ)) atTop (𝓝 4)).mul
        (tendsto_inv_atTop_zero : Tendsto (fun b : ℝ => b ⁻¹) atTop (𝓝 0))
  have hbgt : ∀ᶠ b : ℝ in atTop, 1 ≤ b := by
    rw [Filter.eventually_atTop]
    exact ⟨1, fun _ h => h⟩
  have hbdd : ∀ᶠ b : ℝ in atTop, |r b| ≤ 4 / b := by
    filter_upwards [hbgt] with b hb1
    have hPpos : 0 < 16 * P * b := by positivity
    have hdenpos : 0 < 1 + 4 * P * b ^ 2 := by positivity
    have habs : |r b| = 16 * P * b / (1 + 4 * P * b ^ 2) := by
      unfold r
      rw [abs_of_nonneg]
      exact div_nonneg hPpos.le hdenpos.le
    rw [habs]
    rw [div_le_iff₀ hdenpos]
    have hb0 : b ≠ 0 := by linarith
    field_simp [hb0]
    linarith
  have hsqz : Tendsto (fun b : ℝ => |r b|) atTop (𝓝 0) :=
    tendsto_of_tendsto_of_tendsto_of_le_of_le'
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => (0 : ℝ)) atTop (𝓝 0))
      ht4
      (by filter_upwards with b; positivity)
      hbdd
  change Tendsto r atTop (𝓝 0)
  rw [tendsto_zero_iff_norm_tendsto_zero]
  simpa [Real.norm_eq_abs] using hsqz

/-- Exact rational window defect at P = 1, a = 128 (half-window length):
     D = 16·1·128/(1 + 4·128^2) = 2048/65537. -/
theorem defect_window_closed_form :
    (16 : ℚ) * 1 * 128 / (1 + 4 * 1 * 128 ^ 2) = (2048 : ℚ) / 65537 := by
  norm_num

/-- The outer-tail remainder at P = 1, b = 4096 is 65536/67108865 and lies
     strictly below the window defect D = 2048/65537, so mass leaks beyond. -/
theorem defect_at_L_tail_lt_window :
    (16 : ℚ) * 1 * 4096 / (1 + 4 * 1 * 4096 ^ 2) < (2048 : ℚ) / 65537 := by
  norm_num

end PunoTwin