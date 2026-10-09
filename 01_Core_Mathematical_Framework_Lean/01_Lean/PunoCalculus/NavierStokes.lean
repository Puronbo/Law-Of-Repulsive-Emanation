import Mathlib

/-!
# Navier-Stokes statement layers

Statement-grade formalisation of the two pieces the audit marks as "today
numeric + hand proof" (see the Fluid mechanics row of
`FIELD_AUDIT_AND_FORMALIZATION_ROADMAP.md`):

1. **The Serrin scaling arithmetic** is REAL theorem content.  For the 3D
   Navier-Stokes equations the Prodi-Serrin regularity criterion (Prodi 1959,
   Serrin 1962, Ladyzhenskaya 1967) says: a suitable weak solution on a
   critical pair `(p, q)` with `2/p + 3/q = 1`, `q > 3`, is smooth.  This file
   machine-checks the *scaling* facts: `(p, q) = (4, 6)` and `(p, q) = (3, 9)`
   lie on the Serrin line and in the admissible region, and `q = 3` is excluded
   for every finite `p` (the endpoint criterion needs `q > 3`).

2. **The Fourier / Prodi-Serrin bound and the criterion** are recorded as
   unproved statements, matching the CODE, not the paper:
   - `fourierInfBound`   - the claimed torus bound `‖u‖_∞^2 ≤ 4 E Z`
     (`r3_extension.py`: "On T^3: ||u||_inf^2 <= 4EZ").  The reported route
     `sum 1/|k|^2 ≤ sum 1/|k|`... is the documented T^3 vs R^3 gap: the real
     sum `Σ_{k ∈ Z³, k≠0} 1/|k|²` diverges, so the constant-`4` form is NOT
     machine-checked here.
   - `prodiSerrinIntegralFiniteCertified` - the final step
     `∫ ‖u‖_∞^2 dt < ∞` (`ns_r3_proof.py`, `r3_extension.py`) is numerically
     suggested, NOT a proof.
   - `nsGlobalRegularityOpen` - the implication from the certified scaling
     facts to smoothness in finite time remains the Navier-Stokes existence
     and smoothness problem: OPEN, not discharged.  (`MillenniumBridge.lean`
     already records "NAVIER_STOKES :: NOT SETTLED BY THIS PROJECT".)
-/

namespace PunoCalculus.NavierStokes

noncomputable section

/-- The Serrin scaling exponent `2/p + 3/q` of `L^p_t L^q_x` (3 dimensions). -/
def serrinScaling (p q : ℝ) : ℝ := 2 / p + 3 / q

/-- Prodi-Serrin admissibility: the integrability pair `(p, q)` with `q > 3`
and scaling `2/p + 3/q ≤ 1`.  For critical pairs equality holds. -/
def prodiSerrinAdmissible (p q : ℝ) : Prop := 3 < q ∧ serrinScaling p q ≤ 1

/-- `(p, q) = (4, 6)` is on the Serrin line: `2/4 + 3/6 = 1`. -/
theorem serrinScaling_line_4_6 : serrinScaling 4 6 = 1 := by
  norm_num [serrinScaling]

/-- `(p, q) = (4, 6)` is admissible: `q = 6 > 3` and the scaling is `1 ≤ 1`. -/
theorem prodiSerrin_admissible_4_6 : prodiSerrinAdmissible 4 6 := by
  norm_num [prodiSerrinAdmissible, serrinScaling]

/-- `(p, q) = (3, 9)` is on the Serrin line: `2/3 + 3/9 = 1`. -/
theorem serrinScaling_line_3_9 : serrinScaling 3 9 = 1 := by
  norm_num [serrinScaling]

/-- `(p, q) = (3, 9)` is admissible: `q = 9 > 3` and the scaling is `1 ≤ 1`. -/
theorem prodiSerrin_admissible_3_9 : prodiSerrinAdmissible 3 9 := by
  norm_num [prodiSerrinAdmissible, serrinScaling]

/-- `q = 3` is never admissible, for ANY finite `p`: the criterion demands
`q > 3` strictly, so the endpoint `(p, 3)` is excluded. -/
theorem serrin_endpoint_q3_excluded (p : ℝ) : ¬ prodiSerrinAdmissible p 3 := by
  intro h
  exact (lt_irrefl 3) (h.1)

/-- The claimed torus Fourier bound `‖u‖_∞^2 ≤ 4 E Z` (`r3_extension.py`).
Recorded as an unproved statement: the constant-`4` form depends on the
T^3-mode counting documented there and is not machine-checked. -/
def fourierInfBound (uInf2 E Z : ℝ) : Prop := uInf2 ≤ 4 * E * Z

/-- The Prodi-Serrin integral-finiteness final step
`∫ ‖u‖_∞^2 dt < ∞`: numerically suggested by `ns_r3_proof.py` and
`r3_extension.py`, NOT formally proved. -/
def prodiSerrinIntegralFiniteCertified : Bool := false

/-- The Navier-Stokes existence-and-smoothness wall: whether the implication
from certified scaling/admissibility to global regularity has been discharged.
It has not: this is the exact Millennium problem, and the wall stays OPEN. -/
def nsGlobalRegularityOpen : Bool := true

/-- The statement-grade inventory of this module: two certified rows of Serrin
scaling arithmetic, one certified exclusion, and the two OPEN/unproved
statement layers beyond them. -/
def nsFormalizedFacts : List String :=
  ["serrinScaling 4 6 = 1 and (4,6) admissible (machine-checked)",
   "serrinScaling 3 9 = 1 and (3,9) admissible (machine-checked)",
   "q = 3 excluded for every finite p (machine-checked)",
   "fourierInfBound ||u||_inf^2 <= 4 E Z: statement only, NOT machine-checked",
   "Prodi-Serrin integral finiteness: numerically suggested, NOT a proof",
   "3D Navier-Stokes global regularity: OPEN, NOT discharged"]

/-- The inventory has exactly six entries. -/
theorem nsFormalizedFacts_length : nsFormalizedFacts.length = 6 := by
  native_decide

/-- The integral-finiteness step is recorded as unproved (boolean `false`). -/
theorem prodiSerrinIntegral_is_open : prodiSerrinIntegralFiniteCertified = false := rfl

/-- The global-regularity wall is explicitly open (boolean `true`, READ as
``is open'').  No axiom and no `sorry` is attached: this is a marker value,
the same convention as `Hodge.quintic_codim2_open` and
`PvsNP.noPolynomialCompilationKnown`. -/
theorem ns_global_regularity_wall_open : nsGlobalRegularityOpen = true := rfl

end

end PunoCalculus.NavierStokes