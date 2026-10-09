import Mathlib

/-
  PunoCalculus.MassGap

  NOTE: This module uses a rational approximation m = mu/(1+x)
  instead of the actual one-loop formula m = mu*exp(-x) where
  x = 8*pi^2/(b0*g^2). A rational model was chosen for simplicity;
  Float.exp is available in Lean 4 stdlib.

  Both formulas give m > 0 for all g > 0, so the positivity
  conclusion is the same. But the numerical values differ:
    Actual:   m(g=1) ~ exp(-7.18) ~ 0.00076 GeV
    This file: m(g=1) ~ 1/(1+7.18) ~ 0.122

  The actual proof (Theorem 16) uses asymptotic freedom
  (Gross-Wilczek 1973) to establish m > 0 analytically.
  This module verifies positivity on a simplified model.

  The Python experiment yang_mills_gap_proof.py uses the
  correct exponential formula via mpmath.

  CROSSOVER SECTION (bottom): the universal formula
  M = Lambda / sinh(2*pi / (g_eff^2 * (N-1))) of the Thirring-GN
  crossover / dark-matter core line (`dark_matter_core.py`,
  `thirring_gn_crossover.py`, `dark_unified.py`) has, at the circuit/0/0
  level, the removable factor `sinh(a)/a -> 1` as `a -> 0`.  That is
  formalised below as a real theorem (`sinh_div_self_tendsto_one`,
  `massGapCrossoverRemovable`).  Endpoint honesty: as `a -> 0` the mass
  `M = Lambda/sinh(a)` itself diverges like `Lambda/a` (a POLE, not a
  removable 0/0), and as `g_eff^2 -> 0` the pure formula gives `M -> 0`
  while `dark_matter_core.py` special-cases the cuspy profile `M = Lambda`
  below `sigma_m < 1e-20` - so the "smooth cross-over to the cusp" is a
  numerically-supported statement, NOT a limit of the formula.
-/

def b0 (Nc : Float) : Float := 11.0 * Nc / 3.0

def massGapVal (mu expVal : Float) : Float :=
  if expVal <= 0.0 then mu
  else mu / (1.0 + expVal)

def verifyMassGapPositive : Bool :=
  massGapVal 1.0 (8.0 * 3.14159265358979 * 3.14159265358979 / (b0 3.0 * 0.3 * 0.3)) > 0.0 &&
  massGapVal 1.0 (8.0 * 3.14159265358979 * 3.14159265358979 / (b0 3.0 * 0.5 * 0.5)) > 0.0 &&
  massGapVal 1.0 (8.0 * 3.14159265358979 * 3.14159265358979 / (b0 3.0 * 1.0 * 1.0)) > 0.0 &&
  massGapVal 1.0 (8.0 * 3.14159265358979 * 3.14159265358979 / (b0 3.0 * 1.5 * 1.5)) > 0.0 &&
  massGapVal 1.0 (8.0 * 3.14159265358979 * 3.14159265358979 / (b0 3.0 * 2.0 * 2.0)) > 0.0 &&
  massGapVal 1.0 (8.0 * 3.14159265358979 * 3.14159265358979 / (b0 3.0 * 3.0 * 3.0)) > 0.0 &&
  massGapVal 1.0 (8.0 * 3.14159265358979 * 3.14159265358979 / (b0 3.0 * 4.0 * 4.0)) > 0.0 &&
  massGapVal 1.0 (8.0 * 3.14159265358979 * 3.14159265358979 / (b0 3.0 * 5.0 * 5.0)) > 0.0

#eval verifyMassGapPositive

/-!
# The mass-gap crossover lemma (line 1)

The universal cross-over formula `M = Lambda / sinh(a)` with
`a = 2*pi / (g_eff^2 * (N-1))` (`dark_matter_core.py`, `dark_unified.py`)
contains, at the circuit/0/0 level, the factor `sinh(a)/a` whose value at
`a = 0` is `1`: the numerator and denominator both vanish there, and the
quotient has a removable value.  These are genuine (and machine-checked)
analysis facts:
  * `sinh_div_self_tendsto_one` : `sinh(a)/a -> 1` on the punctured
    neighbourhood of `0`;
  * `massGapCrossoverRemovable` : `a/sinh(a) -> 1`, the reciprocal factor.
The endpoint honesty row is carried in `crossoverCertifiedFacts`.
-/

namespace PunoCalculus.MassGap

open Filter
open scoped Topology

noncomputable section

/-- `sinh(a)/a -> 1` as `a -> 0` on the punctured neighbourhood: the removable
0/0 at the heart of the mass-gap crossover formula.  Proved from the derivative
of `sinh` at `0` (`Real.hasDerivAt_sinh`), so no numerical constant is guessed. -/
theorem sinh_div_self_tendsto_one :
    Tendsto (fun x : ℝ => Real.sinh x / x) (𝓝[≠] 0) (𝓝 1) := by
  have h := (Real.hasDerivAt_sinh 0).tendsto_slope
  have heq : (fun x : ℝ => Real.sinh x / x) =ᶠ[𝓝[≠] 0] slope Real.sinh 0 := by
    filter_upwards with x
    simp [slope]
    rw [div_eq_mul_inv, mul_comm]
  exact Tendsto.congr' heq.symm (by simpa using h)

/-- `a/sinh(a) -> 1` as `a -> 0` on the punctured neighbourhood: the reciprocal
of `sinh(a)/a` (finite and nonzero near `0`), i.e. the crossover factor itself. -/
theorem massGapCrossoverRemovable :
    Tendsto (fun x : ℝ => x / Real.sinh x) (𝓝[≠] 0) (𝓝 1) := by
  have h1 : Tendsto (fun x : ℝ => Real.sinh x / x) (𝓝[≠] 0) (𝓝 1) :=
    sinh_div_self_tendsto_one
  have h2 : Tendsto (fun x : ℝ => (Real.sinh x / x)⁻¹) (𝓝[≠] 0) (𝓝 (1⁻¹ : ℝ)) :=
    Tendsto.inv₀ h1 (by norm_num)
  have heq : (fun x : ℝ => x / Real.sinh x) =ᶠ[𝓝[≠] 0]
      (fun x : ℝ => (Real.sinh x / x)⁻¹) := by
    filter_upwards [eventually_mem_nhdsWithin] with x hx
    have hx0 : x ≠ 0 := hx
    have hs : Real.sinh x ≠ 0 := (Real.sinh_ne_zero).mpr hx0
    field_simp [hx0, hs]
  have h2' : Tendsto (fun x : ℝ => (Real.sinh x / x)⁻¹) (𝓝[≠] 0) (𝓝 1) := by
    simpa using h2
  exact Tendsto.congr' heq.symm h2'

/-- Which pieces of the crossover the module actually certifies, and which it
explicitly does NOT: the removable 0/0 factor is machine-checked; the pole of
`M` at `a = 0`, the `a -> infinity` limit, and the CDM cusp special-case are
NOT (recorded for honesty). -/
def crossoverCertifiedFacts : List String :=
  ["sinh(a)/a -> 1 as a -> 0: REMOVABLE 0/0 factor, machine-checked",
   "a/sinh(a) -> 1 as a -> 0: crossover factor, machine-checked",
   "M = Lambda/sinh(a) as a -> 0: grows like Lambda/a (POLE, not removable 0/0): NOT machine-checked",
   "M = Lambda/sinh(a) as a -> infinity (g_eff^2 small): tends to 0 - pure formula contradicts the CDM special-case M = Lambda (sigma_m < 1e-20): NOT machine-checked"]

/-- The honesty inventory has exactly four entries. -/
theorem crossoverCertifiedFacts_length : crossoverCertifiedFacts.length = 4 := by
  native_decide

end

end PunoCalculus.MassGap
