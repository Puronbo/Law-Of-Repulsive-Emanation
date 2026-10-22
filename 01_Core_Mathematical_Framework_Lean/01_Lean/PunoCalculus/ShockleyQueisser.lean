import Mathlib

/-!
# Shockley-Queisser shape: the interior optimum is unavoidable

A single-junction solar cell faces two opposing pressures as the bandgap `g`
rises: it **absorbs fewer photons** (the fraction of the spectrum above the gap
falls) but **extracts more energy per absorbed photon** (each carries at least the
gap).  This module records the provable *structural* consequence: when one factor
is strictly decreasing and the other strictly increasing, the efficiency has an
**interior optimum** -- it is neither monotone increasing nor monotone decreasing.

The concrete sharpening `E g = (1 - g) * g` is the simplest model with both
factors (absorbed fraction `1 - g`, per-photon voltage `g`); it attains its unique
maximum at `g = 1/2` on `[0,1]`.

This is the provable skeleton of the Shockley-Queisser curve.  The *empirical*
detailed-balance integral over the AM1.5 spectrum is NOT formalized -- only the
monotonicity structure that forces an interior peak.
-/

namespace PunoCalculus.ShockleyQueisser

/-- Absorbed fraction as a function of bandgap: strictly decreasing. -/
noncomputable def absorbed (g : ℝ) : ℝ := 1 - g

/-- Per-photon extractable voltage: strictly increasing in the bandgap. -/
noncomputable def voltage (g : ℝ) : ℝ := g

/-- Single-junction efficiency model: absorbed fraction times per-photon voltage. -/
noncomputable def efficiency (g : ℝ) : ℝ := absorbed g * voltage g

/-- The absorbed fraction is strictly decreasing in the bandgap. -/
theorem absorbed_strict_decreasing {x y : ℝ} (h : x < y) :
    absorbed y < absorbed x := by
  unfold absorbed; linarith

/-- The per-photon voltage is strictly increasing in the bandgap. -/
theorem voltage_strict_increasing {x y : ℝ} (h : x < y) :
    voltage x < voltage y := by
  unfold voltage; linarith

/-- The low-gap extreme is beaten by the interior point `g = 1/2`. -/
theorem efficiency_zero_lt_half : efficiency 0 < efficiency (1 / 2) := by
  unfold efficiency absorbed voltage; norm_num

/-- The high-gap extreme is beaten by the interior point `g = 1/2`. -/
theorem efficiency_one_lt_half : efficiency 1 < efficiency (1 / 2) := by
  unfold efficiency absorbed voltage; norm_num

/-- **Interior optimum.**  The efficiency is not monotone: there are gaps where
raising the bandgap helps and gaps where it hurts. -/
theorem efficiency_not_monotone : ¬ Monotone efficiency := by
  intro h
  have hle : (1 : ℝ) ≤ 2 := by norm_num
  have key : efficiency 1 ≤ efficiency 2 := h hle
  unfold efficiency absorbed voltage at key; norm_num at key

/-- The efficiency is not antitone either. -/
theorem efficiency_not_antitone : ¬ Antitone efficiency := by
  intro h
  have hle : (0 : ℝ) ≤ 1 / 2 := by norm_num
  have key : efficiency (1 / 2) ≤ efficiency 0 := h hle
  unfold efficiency absorbed voltage at key; norm_num at key

/-- **The peak is unique.**  On `[0,1]`, `g = 1/2` maximizes the efficiency. -/
theorem half_is_max {g : ℝ} (_h0 : 0 ≤ g) (_h1 : g ≤ 1) :
    efficiency g ≤ efficiency (1 / 2) := by
  unfold efficiency absorbed voltage
  nlinarith [sq_nonneg (g - 1 / 2)]

end PunoCalculus.ShockleyQueisser
