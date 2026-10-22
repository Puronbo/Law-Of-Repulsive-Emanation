import Mathlib

/-!
# Solar conversion bounds: Carnot, exergy accounting, and PV-T hybrids

A small module recording the *thermodynamic and accounting* ceilings on solar
energy harvesting.  These are the provable skeleton of "the most efficient way to
harvest solar energy":

- **Carnot**: any heat-to-work converter between a hot and cold reservoir has
  efficiency `1 - Tc/Th`; it rises with the source temperature, falls with the
  sink temperature, and is strictly below `1` whenever the sink is nonzero.
- **Exergy accounting (no free lunch)**: outputs split a *fixed* incoming budget.
  Electric and thermal output cannot both be maximal; using more electric strictly
  squeezes the thermal headroom.  A mixture *redistributes* the loss, it does not
  remove it.
- **PV-T hybrid**: combining a photovoltaic fraction `η` with a Carnot converter on
  the *waste heat* `(1-η)` never decreases total exergy -- which is why the most
  efficient harvesters are mixtures (PV+thermal, CSP+PV, tandem+concentration),
  judged by **total exergy**, not by one output alone.

The full Shockley-Queisser detailed-balance integral (a bandgap optimization over
the solar spectrum) is NOT formalized here: it requires the AM1.5 spectrum and
blackbody radiation laws as inputs, which are empirical, not kernel facts.  What
is proved is the accounting structure those ceilings obey.
-/

namespace PunoCalculus.SolarBounds

/-- Carnot efficiency of a heat engine between sink `tc` and source `th`. -/
noncomputable def carnot (tc th : ℝ) : ℝ := 1 - tc / th

/-- Total exergy of a PV-T hybrid: the PV fraction `η` in electricity, plus a
Carnot converter acting on the waste-heat fraction `1 - η`. -/
noncomputable def hybridExergy (pvEff wasteTc wasteTh budget : ℝ) : ℝ :=
  pvEff * budget + carnot wasteTc wasteTh * ((1 - pvEff) * budget)

/-- Carnot efficiency is monotone in the source temperature. -/
theorem carnot_mono_source {tc th1 th2 : ℝ}
    (h0 : 0 < tc) (h1 : 0 < th1) (_h2 : 0 < th2) (h : th1 ≤ th2) :
    carnot tc th1 ≤ carnot tc th2 := by
  unfold carnot
  have : tc / th2 ≤ tc / th1 := div_le_div_of_nonneg_left (le_of_lt h0) h1 h
  linarith

/-- A strictly hotter source is strictly better. -/
theorem carnot_strict_mono_source {tc th1 th2 : ℝ}
    (h0 : 0 < tc) (h1 : 0 < th1) (_h2 : 0 < th2) (h : th1 < th2) :
    carnot tc th1 < carnot tc th2 := by
  unfold carnot
  have : tc / th2 < tc / th1 := div_lt_div_of_pos_left h0 h1 h
  linarith

/-- Carnot efficiency is strictly below one for any nonzero sink temperature:
no heat engine is perfect. -/
theorem carnot_lt_one {tc th : ℝ} (h0 : 0 < tc) (h : 0 < th) : carnot tc th < 1 := by
  unfold carnot
  have : 0 < tc / th := div_pos h0 h
  linarith

/-- **No free lunch.**  With a fixed budget, electric and thermal output cannot
both be maximal: the thermal headroom is `B - e`. -/
theorem exergy_budget_squeeze {B e t : ℝ} (h : e + t ≤ B) : t ≤ B - e := by linarith

/-- Using strictly more electric output strictly reduces the thermal headroom. -/
theorem more_electric_less_thermal {B e1 e2 t : ℝ}
    (h : e2 + t ≤ B) (_he : e1 < e2) : t < B - e1 := by linarith

/-- **Mixtures never lose.**  A PV-T hybrid's total exergy is at least the pure-PV
electric output: capturing the waste heat cannot reduce the total.  This is the
provable reason the most efficient harvesters are mixtures, judged by total
exergy. -/
theorem hybrid_beats_pure_pv (pv tc th B : ℝ)
    (hB : 0 < B) (_hpv : 0 ≤ pv) (hpv1 : pv ≤ 1) (htc : 0 < tc) (hth : tc < th) :
    pv * B ≤ hybridExergy pv tc th B := by
  unfold hybridExergy carnot
  have hth0 : 0 < th := lt_trans htc hth
  have hc : 0 < 1 - tc / th := by rw [sub_pos, div_lt_one hth0]; exact hth
  have hw : 0 ≤ (1 - pv) * B := mul_nonneg (by linarith) (le_of_lt hB)
  nlinarith [mul_nonneg (le_of_lt hc) hw]

end PunoCalculus.SolarBounds
