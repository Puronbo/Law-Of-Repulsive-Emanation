import Mathlib

/-!
# The Widder-Hankel tail density, formalised (Lean 4, Mathlib)

Machine-checked content behind `rh_widder_hankel_h9.py`'s tail correction.

Rescaling the local zeta density to a half-plane of modulus `T` leaves a tail
integral on the real axis,

    tail(m, T) = ∫_T^∞  log(t / 2π) / (2π) · t^(-2m) dt,

which is what makes the rescaled density a Mellin transform.  The condition
`m > 1/2` is the convergence threshold: `∫_T^∞ t^(-2m) dt` converges iff
`2m > 1`, and that is why the framework evaluates at `m >= 1`.

Proved here:

- `rpow_antitone_m`: on `T >= 1` the power factor `T^(-2m)` is decreasing in
  `m`, for real `m`.  This is the qualitative reason a heavier `m` costs less
  tail, and it is exactly the monotonicity the Python ladder relies on when it
  bisects over real `m`.  Unlike the natural-exponent version in
  `PunoCalculus.RH.Monotonicity`, this one covers the real exponents the code
  actually evaluates.

By hand, with `a = 2m - 1`, the antiderivative of the integrand is

    -t^(1-2m) · ( log(t/2π)/(2m-1) + 1/(2m-1)^2 ) / (2π)     for 2m ≠ 1

and its derivative is `log(t/2π) · t^(-2m) / (2π)`.

Not yet formalised, and deliberately not claimed:

- that antiderivative as a `HasDerivAt` theorem, and hence the closed form
  `tail(m, T) = T^(1-2m) · (1 + (2m-1)·log(T/2π)) / (2π·(2m-1)^2)`;
- the improper limit `lim_{B→∞}` of that antiderivative;
- continuity of the integrand on `Ioi 0`, and local integrability on compact
  subintervals (`IntervalIntegrable`).  These are routine but were not
  discharged here; note that local integrability holds for *every* `m`, so it
  is not where `m > 1/2` bites -- only the behaviour at infinity is;
- that `m > 1/2` is the *iff* condition for convergence of the improper
  integral, as opposed to the numerical check that motivates it;
- the local-finiteness claim `dμ = 2∑δ_{γ²}`, which needs measure theory.

The Python artifact remains the evidence for all of the above.  Nothing in this
file is a proof of RH.
-/

namespace PunoCalculus.RH

/-- The tail density at height `T`: the rescaled density's contribution from
`[T, ∞)`.  Its justification is the Mellin-transform identity above. -/
noncomputable def tailDensity (m T : ℝ) : ℝ :=
  Real.log (T / (2 * Real.pi)) / (2 * Real.pi) * T ^ (-2 * m)

/-- The tail integrand as a function of the integration variable, so that
monotonicity statements can be made about the power factor. -/
noncomputable def tailIntegrand (m : ℝ) : ℝ → ℝ :=
  fun t => Real.log (t / (2 * Real.pi)) / (2 * Real.pi) * t ^ (-2 * m)

/-- On `T >= 1` the power factor `T^(-2m)` decreases as `m` increases, for real
`m`.  This is the monotonicity the real-exponent ladder scan relies on: a
heavier `m` multiplies the tail by a smaller factor.

The direction is the one that makes the argument work.  Raising `m` lowers the
exponent `-2m`, and lowering the exponent of a base `>= 1` lowers the value. -/
theorem rpow_antitone_m {m m' T : ℝ} (hT : 1 ≤ T) (hm : m' ≤ m) :
    T ^ (-2 * m) ≤ T ^ (-2 * m') := by
  refine Real.rpow_le_rpow_of_exponent_le hT ?_
  linarith

end PunoCalculus.RH
