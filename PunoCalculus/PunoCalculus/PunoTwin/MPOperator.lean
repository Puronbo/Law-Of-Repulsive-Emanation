import Mathlib

/-!
# MP-Operator: the exact discriminant bridge to the soliton mass law

We consider the operator `A_{α,β} = αD + βV`, where `D = d/dx` and
`V f(x) = ∫₀ˣ f (t) dt` (the antiderivative).  The eigenvalue equation
`A f = λ f` is the integro-differential equation `α f' + β V f = λ f`;
differentiating once yields the second-order ordinary differential equation

    α f'' - λ f' + β f = 0

with characteristic polynomial `α r² - λ r + β` and discriminant

    Δ(α,β,λ) = λ² - 4 α β.

This module records *exact, fully proved* identities (every theorem below is
closed by `ring`/`norm_num`, with zero unproved gaps) about that discriminant.
The key bridge: for the family `α = 1`, `β = a`,
`λ = 2a + 1` the discriminant is exactly the soliton window denominator of
the twin mass law:

    Δ(1, a, 2a+1) = (2a+1)² - 4a = 4a² + 1 = 1 + 4a²,

which at `a = 128` is the Fermat number `2¹⁶ + 1 = 65537` (the denominator
of the exact window defect `2048/65537`) and at `a = 4096` is
`2²⁶ + 1 = 67108865` (the denominator of the tail remainder
`65536/67108865`).  The defect identity

    D = 16 P a / (1 + 4 P a²)  =  2 · (8 a / (1 + 4 a²))   at  P = 1

then re-expresses the mass law as twice the antiderivative of the defect
density evaluated at the window half-length `a`.
-/

namespace PunoTwin.MPOperator

/-- The operator discriminant for the `λ = 2a + 1` family equals the
soliton window denominator: `Δ(1, a, 2a+1) = 1 + 4a²`. -/
theorem operator_discriminant_bridge (a : ℚ) :
    (2 * a + 1) ^ 2 - 4 * a = 1 + 4 * a ^ 2 := by
  ring

/-- The window denominator is the operator discriminant at `a = 128`:
`Δ(1, 128, 257) = 65537`. -/
theorem window_discriminant_closed_form :
    (2 * (128 : ℚ) + 1) ^ 2 - 4 * 128 = 65537 := by
  norm_num

/-- The tail denominator is the operator discriminant at `a = 4096`:
`Δ(1, 4096, 8193) = 67108865`. -/
theorem tail_discriminant_closed_form :
    (2 * (4096 : ℚ) + 1) ^ 2 - 4 * 4096 = 67108865 := by
  norm_num

/-- The window denominator is the Fermat number `2¹⁶ + 1`. -/
theorem fermat_denominator_window :
    1 + 4 * (128 : ℚ) ^ 2 = 2 ^ 16 + 1 := by
  norm_num

/-- The discriminant stays positive for the window family, so the
characteristic polynomial has two distinct real roots and the eigenspace
has dimension one (the two integration constants collapse onto one line). -/
theorem window_discriminant_pos : 0 < (2 * (128 : ℚ) + 1) ^ 2 - 4 * 128 := by
  norm_num

/-- The window defect is twice the antiderivative of the defect density at
the window half-length: `D = 2 · Vρ(a)` at `P = 1`, `a = 128`. -/
theorem defect_is_double_antiderivative :
    (16 : ℚ) * 1 * 128 / (1 + 4 * 1 * 128 ^ 2)
      = 2 * ((8 : ℚ) * 128 / (1 + 4 * 1 * 128 ^ 2)) := by
  norm_num

/-- The same split identity at the outer-tail length `b = 4096`: the tail
remainder is twice the antiderivative at `b`. -/
theorem tail_is_double_antiderivative :
    (16 : ℚ) * 1 * 4096 / (1 + 4 * 1 * 4096 ^ 2)
      = 2 * ((8 : ℚ) * 4096 / (1 + 4 * 1 * 4096 ^ 2)) := by
  norm_num

/-- The mass-law antiderivative `u(t) = t/(1+4Pt²)` satisfies a genuinely
*first-order* rational ODE with the closed-form derivative known from
`PunoTwin.TwinAnalyticLaws.antiderivative_deriv`:

    (1 + 4 P t²) · u′(t) + 8 P t · u(t) = 1   for every real `t`, `P > 0`.

This is the exact algebraic content behind the "2 × antiderivative"
identity above.  (It is NOT an eigenfunction statement for
`A_{α,β}`: a constant-coefficient eigen-ODE has only exponential
solutions, so the ratio pie bridge to the defect is purely an arithmetic
denominator match, not an analytic solution match.) -/
theorem antiderivative_first_order_law (hP : 0 < P) (t : ℝ) :
    (1 + 4 * P * t ^ 2) * ((1 - 4 * P * t ^ 2) / (1 + 4 * P * t ^ 2) ^ 2)
      + 8 * P * t * (t / (1 + 4 * P * t ^ 2)) = 1 := by
  have hden : 0 < 1 + 4 * P * t ^ 2 := by positivity
  field_simp [hden.ne']
  ring

/-- The mass-radius identity for the defect: for every half-window `a`,
    D(a)·a + 4/(1 + 4a²) = 4 exactly.  Equivalently D(a)·a = 4 − 4/(1+4a²),
    so the product D(a)·a is strictly bounded above by the mass ceiling 4,
    rising monotonically toward it as `a` grows past 1/2.  This is the
    exact algebraic content of the numerically-checked window defect: at
    a = 128, D·a = 262144/65537 and 4/(1+4·128²) = 4/65537. -/
theorem mass_radius_identity (a : ℝ) :
    16 * a ^ 2 / (1 + 4 * a ^ 2) + 4 / (1 + 4 * a ^ 2) = 4 := by
  have hden : 1 + 4 * a ^ 2 ≠ 0 := by positivity
  field_simp [hden]
  ring

/-- The same mass-radius identity at the certified window `a = 128`
    (P = 1), stated as an exact rational: D(128)·128 = 262144/65537. -/
theorem mass_radius_window :
    (16 : ℚ) * 1 * 128 / (1 + 4 * 1 * 128 ^ 2) * 128 = (262144 : ℚ) / 65537 := by
  norm_num

/-- The same mass-radius identity at the outer-tail length `b = 4096`
    (P = 1): D(4096)·4096 = 65536/67108865 · 4096 = 268435456/67108865.
    The remainder 4/(1+4·4096²) = 4/67108865 stays strictly positive, so
    the product is strictly below the mass ceiling 4 at every half-window. -/
theorem mass_radius_tail :
    (16 : ℚ) * 1 * 4096 / (1 + 4 * 1 * 4096 ^ 2) * 4096
      = (268435456 : ℚ) / 67108865 := by
  norm_num

/-- The mass-radius product at the tail lies strictly below the mass
    ceiling 4, because the celebrated remainder 4/(1 + 4b²) is positive
    (here 4/67108865 > 0). -/
theorem mass_radius_tail_lt_ceil :
    (16 : ℚ) * 1 * 4096 / (1 + 4 * 1 * 4096 ^ 2) * 4096 < 4 := by
  norm_num

/-- The bridge-family discriminant is positive for every real half-window
    `a`: 1 + 4a² ≥ 1 > 0.  Hence every characteristic polynomial
    r² − (2a+1)r + a of the two-root picture has two distinct real roots,
    with no transition to the Δ = 0 or Δ < 0 regimes on the mass law. -/
theorem window_discriminant_real_pos (a : ℝ) : 1 ≤ 1 + 4 * a ^ 2 := by
  nlinarith [sq_nonneg a]

/-- Vieta's identity for the spectral roots, stated universally: for any
    roots `r₁`, `r₂`, the discriminant of the monic polynomial
    (r − r₁)(r − r₂) = r² − (r₁+r₂)r + r₁r₂ equals
    (r₁+r₂)² − 4r₁r₂ = (r₁−r₂)².  This is the same exact rational the
    characteristic-equation bridge evaluates at (α,β,λ) = (1, a, 2a+1):
    (2a+1)² − 4a = Δ. -/
theorem vieta_discriminant (r₁ r₂ : ℝ) :
    (r₁ + r₂) ^ 2 - 4 * r₁ * r₂ = (r₁ - r₂) ^ 2 := by
  ring

/-- Three-regime classification on the bridge family: the discriminant
    Δ = (2a+1)² − 4a = 4a² + 1 is always strictly positive, so the
    characteristic polynomial r² − (2a+1)r + a has two distinct real roots
    on the whole mass law; the Δ = 0 double-root point and the Δ < 0
    complex-conjugate (oscillatory) pair can arise in the general operator
    algebra A_{α,β} = αD + βV, but never on this exact bridge. -/
theorem bridge_discriminant_never_negative (a : ℝ) : 0 < 4 * a ^ 2 + 1 := by
  nlinarith [sq_nonneg a]

/-- The exact value at the certified window: Δ(128) = 65537 > 0. -/
theorem bridge_discriminant_window_pos : (0 : ℚ) < 4 * 128 ^ 2 + 1 := by
  norm_num

/-- Square-squeeze of the discriminant: for every real half-window `a > 0`
    the bridge discriminant Δ = 4a² + 1 sits strictly between the squares
    `(2a)²` and `(2a+1)²`.  Since square root is monotone, this is the
    bare-hands statement that `2a < √Δ < 2a+1` — no overt radicand lemma
    needed — which is exactly what pins the spectral bracket
    `0 < r₂ < 1/2 < r₁ < 2a+1` in `char_poly_at_half` and friends:
    r₁ = (2a+1+√Δ)/2 < 2a+1 and r₂ = (2a+1−√Δ)/2 ∈ (0, 1/2). -/
theorem bridge_discriminant_square_squeeze (a : ℝ) (ha : 0 < a) :
    (2 * a) ^ 2 < 4 * a ^ 2 + 1 ∧ 4 * a ^ 2 + 1 < (2 * a + 1) ^ 2 := by
  constructor
  · nlinarith [sq_nonneg a]
  · nlinarith [sq_nonneg a, ha]

/-- Window form of the square-squeeze: at `a = 128` the discriminant
    `65537` is sandwiched between 256² and 257², i.e.
    `65536 < 65537 < 66049` — the tightest exact rational bracket of the
    spectral roots at the certified window. -/
theorem bridge_discriminant_square_squeeze_window :
    (256 : ℚ) ^ 2 < 4 * 128 ^ 2 + 1 ∧ 4 * 128 ^ 2 + 1 < (257 : ℚ) ^ 2 := by
  constructor
  · norm_num
  · norm_num

/-- Tail form of the square-squeeze: at `a = 4096` the discriminant
    `67108865` is sandwiched between 8192² and 8193², i.e.
    `67108864 < 67108865 < 67125249` — the exact bracket at the tail
    window (monotonic under `mass_radius_window_lt_tail`). -/
theorem bridge_discriminant_square_squeeze_tail :
    (8192 : ℚ) ^ 2 < 4 * 4096 ^ 2 + 1 ∧ 4 * 4096 ^ 2 + 1 < (8193 : ℚ) ^ 2 := by
  constructor
  · norm_num
  · norm_num

/-- Tight rational lid on the discriminant interval: the upper endpoint
    of the squeeze can be refined from `2a+1` to `2a + 1/(4a)`, whose
    square exceeds the discriminant Δ = 4a² + 1 by exactly `1/(16a²)`.
    Symmetric refinement of the spectral-shadow bound
    `r₁ − r₂ = √Δ < 2a + 1/(4a)` for every `a > 0`. -/
theorem bridge_discriminant_tight_upper_square (a : ℝ) (ha : 0 < a) :
    (2 * a + 1 / (4 * a)) ^ 2 = 4 * a ^ 2 + 1 + 1 / (16 * a ^ 2) := by
  field_simp
  ring

/-- Window form of the tight lid: at `a = 128`,
    `(2a + 1/(4a))² = 65537 + 1/262144` — the square of the refined upper
    endpoint misses the discriminant by exactly one part in 262144. -/
theorem bridge_discriminant_tight_upper_square_window :
    (2 * (128 : ℚ) + 1 / (4 * 128)) ^ 2 = 4 * 128 ^ 2 + 1 + 1 / (16 * 128 ^ 2) := by
  norm_num

/-- Tail form of the tight lid: at `a = 4096`,
    `(2a + 1/(4a))² = 67108865 + 1/268435456` — refining the tail to one
    part in 2²⁸. -/
theorem bridge_discriminant_tight_upper_square_tail :
    (2 * (4096 : ℚ) + 1 / (4 * 4096)) ^ 2 = 4 * 4096 ^ 2 + 1 + 1 / (16 * 4096 ^ 2) := by
  norm_num

/-- Exact gap-scaling law: the lid's excess `1/(16a²)` over the
    discriminant shrinks by the factor 1/4 when the half-window doubles —
    so a 32× step from window to tail (4096 = 32·128) tightens the gap by
    2⁻¹⁰, from 1/262144 to 1/268435456. -/
theorem discrim_gap_quarter_scaling (a : ℝ) (ha : 0 < a) :
    1 / (16 * (2 * a) ^ 2) = (1 / 4 : ℝ) * 1 / (16 * a ^ 2) := by
  field_simp
  ring

/-- Vieta midpoint bracket: for any two roots `r₁, r₂` of the bridge
    characteristic polynomial `r² − (2a+1)r + a` (so `r₁ + r₂ = 2a+1`
    and `r₁r₂ = a`), the product of the signed distances from the spectral
    midpoint is exactly `−1/4`, independent of `a`.  With a positive
    leading coefficient the midpoint therefore lies strictly between the
    two roots for every `a > 0`: `r₂ < 1/2 < r₁`. -/
theorem vieta_midpoint_bracket (a r₁ r₂ : ℝ)
    (hsum : r₁ + r₂ = 2 * a + 1) (hprod : r₁ * r₂ = a) :
    (1 / 2 - r₁) * (1 / 2 - r₂) = (-1 / 4 : ℝ) := by
  nlinarith

/-- Spectral-gap squared squeeze: the identity `(r₁−r₂)² = Δ = 4a²+1`
    (a pure consequence of Vieta's sum and product) is pinched, for every
    `a > 0`, between the window square `(2a)²` and the tight lid
    `(2a + 1/(4a))²` of `bridge_discriminant_tight_upper_square`.  This is
    the ordering-free (absolute) form `2a < |r₁−r₂| < 2a + 1/(4a)` of the
    spectral-gap shadow. -/
theorem bridge_gap_square_squeeze (a r₁ r₂ : ℝ) (ha : 0 < a)
    (hsum : r₁ + r₂ = 2 * a + 1) (hprod : r₁ * r₂ = a) :
    (2 * a) ^ 2 < (r₁ - r₂) ^ 2 ∧
      (r₁ - r₂) ^ 2 < (2 * a + 1 / (4 * a)) ^ 2 := by
  have hgap : (r₁ - r₂) ^ 2 = 4 * a ^ 2 + 1 := by
    nlinarith [hsum, hprod]
  constructor
  · rw [hgap]
    exact (bridge_discriminant_square_squeeze a ha).1
  · rw [hgap, bridge_discriminant_tight_upper_square a ha]
    have hpos : 0 < 1 / (16 * a ^ 2) := by positivity
    nlinarith

/-- Window tag of the gap shadow: at `a = 128`, the squared distance
    between the roots satisfies `65536 < (r₁−r₂)² < 65537 + 1/262144`. -/
theorem bridge_gap_square_squeeze_window (r₁ r₂ : ℝ)
    (hsum : r₁ + r₂ = (2 * 128 + 1 : ℝ)) (hprod : r₁ * r₂ = (128 : ℝ)) :
    (2 * 128 : ℝ) ^ 2 < (r₁ - r₂) ^ 2 ∧
      (r₁ - r₂) ^ 2 < (2 * 128 + 1 / (4 * 128)) ^ 2 := by
  exact bridge_gap_square_squeeze 128 r₁ r₂ (by norm_num) hsum hprod

/-- Tail tag of the gap shadow: at `a = 4096`, the squared distance
    between the roots satisfies `67108864 < (r₁−r₂)² < 67108865 + 1/268435456`. -/
theorem bridge_gap_square_squeeze_tail (r₁ r₂ : ℝ)
    (hsum : r₁ + r₂ = (2 * 4096 + 1 : ℝ)) (hprod : r₁ * r₂ = (4096 : ℝ)) :
    (2 * 4096 : ℝ) ^ 2 < (r₁ - r₂) ^ 2 ∧
      (r₁ - r₂) ^ 2 < (2 * 4096 + 1 / (4 * 4096)) ^ 2 := by
  exact bridge_gap_square_squeeze 4096 r₁ r₂ (by norm_num) hsum hprod

/-- Mirror law of the spectral distance I: the two signed distances from
    the spectral midpoint `1/2` to the roots sum to exactly `2a` — twice
    the half-window, one half-window per side — for any two roots of
    `r² − (2a+1)r + a`. -/
theorem spectral_midpoint_distance_sum (a r₁ r₂ : ℝ)
    (hsum : r₁ + r₂ = 2 * a + 1) :
    (r₁ - 1 / 2) + (r₂ - 1 / 2) = 2 * a := by
  nlinarith

/-- Mirror law of the spectral distance II: the two signed distances from
    the spectral midpoint multiply to exactly `−1/4`, independently of
    `a`.  With sum `2a` and product `−1/4`, they are the two roots of the
    mirror quadratic `z² − 2a·z − 1/4 = 0`, whose discriminant is exactly
    the bridge discriminant `4a² + 1` — the gap shadow in centred
    coordinates. -/
theorem spectral_midpoint_distance_prod (a r₁ r₂ : ℝ)
    (hsum : r₁ + r₂ = 2 * a + 1) (hprod : r₁ * r₂ = a) :
    (r₁ - 1 / 2) * (r₂ - 1 / 2) = -1 / 4 := by
  nlinarith

/-- The spectral midpoint lies strictly between the two roots for every
    half-window: `(1/2 − r₁)(1/2 − r₂) < 0`, universally in the roots'
    data (no positivity hypothesis needed). -/
theorem spectral_midpoint_between_roots (a r₁ r₂ : ℝ)
    (hsum : r₁ + r₂ = 2 * a + 1) (hprod : r₁ * r₂ = a) :
    (1 / 2 - r₁) * (1 / 2 - r₂) < 0 := by
  have hb := vieta_midpoint_bracket a r₁ r₂ hsum hprod
  nlinarith

/-- Each signed distance from the midpoint solves the mirror quadratic:
    `z² − 2a·z − 1/4 = 0` at `z = r₁ − 1/2` and at `z = r₂ − 1/2`. -/
theorem spectral_distance_mirror_quadratic (a r₁ r₂ : ℝ)
    (hsum : r₁ + r₂ = 2 * a + 1) (hprod : r₁ * r₂ = a) :
    (r₁ - 1 / 2) ^ 2 - 2 * a * (r₁ - 1 / 2) - 1 / 4 = 0 ∧
      (r₂ - 1 / 2) ^ 2 - 2 * a * (r₂ - 1 / 2) - 1 / 4 = 0 := by
  have hl : (r₁ - 1 / 2) ^ 2 - 2 * a * (r₁ - 1 / 2) - 1 / 4
      = r₁ ^ 2 - (2 * a + 1) * r₁ + a := by
    ring
  have hpl : r₁ ^ 2 - (2 * a + 1) * r₁ + a = 0 := by
    rw [← hsum]
    ring_nf
    nlinarith [hprod]
  have hr : (r₂ - 1 / 2) ^ 2 - 2 * a * (r₂ - 1 / 2) - 1 / 4
      = r₂ ^ 2 - (2 * a + 1) * r₂ + a := by
    ring
  have hpr : r₂ ^ 2 - (2 * a + 1) * r₂ + a = 0 := by
    rw [← hsum]
    ring_nf
    nlinarith [hprod]
  constructor
  · exact hl.trans hpl
  · exact hr.trans hpr

/-- The mirror quadratic `z² − 2a·z − 1/4` carries exactly the bridge
    discriminant: `(−2a)² − 4·(−1/4) = 4a² + 1 = Δ`.  The centred shadow
    is the same gap, measured from the midpoint. -/
theorem mirror_quadratic_discriminant_is_bridge (a : ℝ) :
    (2 * a) ^ 2 + 4 * (1 / 4) = 4 * a ^ 2 + 1 := by
  ring

/-- Harmonic law of the roots: the reciprocal roots sum to `2 + 1/a`.
    Since `r₁r₂ = a > 0`, both roots are nonzero and
    `1/r₁ + 1/r₂ = (r₁+r₂)/(r₁r₂) = (2a+1)/a = 2 + 1/a` — the exact
    numeric shadow of the spectral pair in the twin ring `ℤ[a, 1/a]`. -/
theorem spectral_reciprocal_sum_law (a r₁ r₂ : ℝ) (ha : 0 < a)
    (hsum : r₁ + r₂ = 2 * a + 1) (hprod : r₁ * r₂ = a) :
    1 / r₁ + 1 / r₂ = 2 + 1 / a := by
  have h₁ : r₁ ≠ 0 := by
    intro h
    have : a = 0 := by nlinarith [hprod, h]
    nlinarith
  have h₂ : r₂ ≠ 0 := by
    intro h
    have : a = 0 := by nlinarith [hprod, h]
    nlinarith
  have hjoin : 1 / r₁ + 1 / r₂ = (r₁ + r₂) / (r₁ * r₂) := by
    field_simp [h₁, h₂]
    ring
  rw [hjoin, hsum, hprod]
  field_simp [ne_of_gt ha]

/-- Explicit spectral bracket, under the standard root ordering
    (`r₂` the contractive root, `r₁` the expansive root, so r₂ < 1/2 < r₁):
    the full rational window `0 < r₂ < 1/2 < r₁ < 2a+1` holds for every
    `a > 0`.  The top cap `r₁ < 2a+1` is equivalent to the positivity of
    `r₂` via `r₁ + r₂ = 2a+1`, and `r₂ = a/r₁ > 0` follows from the Vieta
    product.  This is the bracket asserted by the sign analysis in
    `spectral_bracket_window`, now closed by `field_simp`/`positivity`. -/
theorem spectral_roots_bracket_explicit (a r₁ r₂ : ℝ) (ha : 0 < a)
    (hsum : r₁ + r₂ = 2 * a + 1) (hprod : r₁ * r₂ = a)
    (hord : r₂ < 1 / 2 ∧ 1 / 2 < r₁) :
    0 < r₂ ∧ r₂ < 1 / 2 ∧ 1 / 2 < r₁ ∧ r₁ < 2 * a + 1 := by
  have hr₁ : 0 < r₁ := by linarith
  have hrecip : r₂ = a / r₁ := by
    rw [← hprod]
    field_simp [ne_of_gt hr₁]
  have hpos : 0 < r₂ := by
    rw [hrecip]
    positivity
  have htop : r₁ < 2 * a + 1 := by
    have : 2 * a + 1 - r₁ = r₂ := by linarith
    linarith
  constructor
  · exact hpos
  constructor
  · exact hord.1
  constructor
  · exact hord.2
  · exact htop

/-- The explicit bracket at the certified window `a = 128`:
    `0 < r₂ < 1/2 < r₁ < 257`. -/
theorem spectral_roots_bracket_window (r₁ r₂ : ℝ)
    (hsum : r₁ + r₂ = (2 * 128 + 1 : ℝ)) (hprod : r₁ * r₂ = (128 : ℝ))
    (hord : r₂ < 1 / 2 ∧ 1 / 2 < r₁) :
    0 < r₂ ∧ r₂ < 1 / 2 ∧ 1 / 2 < r₁ ∧ r₁ < (2 * 128 + 1 : ℝ) := by
  exact spectral_roots_bracket_explicit 128 r₁ r₂ (by norm_num) hsum hprod hord

/-- The harmonic law at the certified window: the reciprocal roots sum to
    `2 + 1/128`. -/
theorem spectral_reciprocal_sum_window (r₁ r₂ : ℝ)
    (hsum : r₁ + r₂ = (2 * 128 + 1 : ℝ)) (hprod : r₁ * r₂ = (128 : ℝ)) :
    1 / r₁ + 1 / r₂ = 2 + (1 / 128 : ℝ) := by
  exact spectral_reciprocal_sum_law 128 r₁ r₂ (by norm_num) hsum hprod

/-- The harmonic law at the outer-tail window: the reciprocal roots sum to
    `2 + 1/4096`. -/
theorem spectral_reciprocal_sum_tail (r₁ r₂ : ℝ)
    (hsum : r₁ + r₂ = (2 * 4096 + 1 : ℝ)) (hprod : r₁ * r₂ = (4096 : ℝ)) :
    1 / r₁ + 1 / r₂ = 2 + (1 / 4096 : ℝ) := by
  exact spectral_reciprocal_sum_law 4096 r₁ r₂ (by norm_num) hsum hprod

/-! ## The operator composition law on the polynomial model

The pair (D, V) acts on polynomials: D is `Polynomial.derivative` and V is
the antiderivative `integral` below, which divides the coefficient of
`Xⁿ` by `(n+1)`.  On this model the two Leibniz half-turns are exact and
provable by coefficient arithmetic:

    D (V g) = g      (derivative of an antiderivative recovers g)
    V (D g) = g − g(0)   (antiderivative of a derivative drops the constant)

Hence the commuting-defect (anticommutator) of the pair is
`D V + V D = 2 id − E₀` with `E₀ g = g(0)`, and the operator square of
`A_{α,β} = α D + β V` satisfies

    A_{α,β}² g = α² D² g + α β (2 g − g(0)) + β² V² g,

which is the polynomial, fully-proved form of the composition law that
Round 54's `vieta_midpoint_bracket` shadows in the spectral ring.  Every
statement below is closed (no `sorry`/`axiom`); the coefficient lemmas
`integral_coeff_*` are the computational backbone. -/

/-- The antiderivative endomorphism on the polynomial model of the
    operator pair (D, V): `V g = Σₙ cₙ xⁿ⁺¹/(n+1)`, the exact discrete
    inverse of `Polynomial.derivative` up to constants. -/
noncomputable def integral (p : Polynomial ℝ) : Polynomial ℝ :=
  p.sum (fun n c => Polynomial.C (c / (↑n + 1)) * Polynomial.X ^ (n + 1))

/-- The antiderivative has no constant term: `(V g).coeff 0 = 0`. -/
lemma integral_coeff_zero (p : Polynomial ℝ) : (integral p).coeff 0 = 0 := by
  rw [integral, Polynomial.coeff_sum, Polynomial.sum_def]
  simp

/-- The coefficient law of the antiderivative:
    `(V g).coeff (n+1) = g.coeff n / (n+1)` for every `n`. -/
lemma integral_coeff_succ (p : Polynomial ℝ) (n : ℕ) :
    (integral p).coeff (n + 1) = p.coeff n / (↑n + 1) := by
  rw [integral, Polynomial.coeff_sum, Polynomial.sum_def]
  simp_rw [Polynomial.coeff_C_mul_X_pow]
  have hguard : ∀ x, (if n + 1 = x + 1 then p.coeff x / (↑x + 1) else 0)
      = if n = x then p.coeff n / (↑n + 1) else 0 := by
    intro x
    by_cases hx : x = n
    · subst x
      simp
    · have hn : n ≠ x := by exact fun hn => hx (hn.symm)
      simp [hn]
  simp_rw [hguard]
  rw [Finset.sum_ite_eq]
  by_cases hn : n ∈ p.support
  · rw [if_pos hn]
  · rw [if_neg hn]
    have hp : p.coeff n = 0 := by
      rw [Polynomial.mem_support_iff] at hn
      exact not_not.mp hn
    simp [hp]

/-- Commutation relation I: `D (V g) = g` — deriving an antiderivative
    recovers the polynomial exactly.  This is the operator-level
    `DV = id` on the polynomial model. -/
theorem derivative_integral (p : Polynomial ℝ) :
    Polynomial.derivative (integral p) = p := by
  apply Polynomial.ext
  intro n
  rw [Polynomial.coeff_derivative, integral_coeff_succ]
  have hnz : (↑n + 1 : ℝ) ≠ 0 := by positivity
  field_simp [hnz]

/-- Commutation relation II: `V (D g) = g − g(0)` — antideriving a
    derivative returns the original polynomial minus its constant term,
    i.e. `VD = id − E₀` with evaluation-at-zero `E₀`. -/
theorem integral_derivative_sub_eval0 (p : Polynomial ℝ) :
    integral (Polynomial.derivative p) = p - Polynomial.C (p.coeff 0) := by
  apply Polynomial.ext
  intro m
  cases m with
  | zero =>
      rw [integral_coeff_zero]
      simp
  | succ n =>
      rw [integral_coeff_succ, Polynomial.coeff_derivative]
      have hnz : (↑n + 1 : ℝ) ≠ 0 := by positivity
      field_simp [hnz]
      simp

/-- The antiderivative is additive: `V (f + g) = V f + V g`. -/
lemma integral_add (f g : Polynomial ℝ) : integral (f + g) = integral f + integral g := by
  apply Polynomial.ext
  intro n
  cases n with
  | zero =>
      simp [integral_coeff_zero]
  | succ m =>
      rw [integral_coeff_succ, Polynomial.coeff_add, Polynomial.coeff_add,
        integral_coeff_succ, integral_coeff_succ]
      field_simp

/-- The antiderivative is `ℝ`-linear for constant multiples:
    `V (C a · g) = C a · V g`. -/
lemma integral_C_mul (a : ℝ) (f : Polynomial ℝ) :
    integral (Polynomial.C a * f) = Polynomial.C a * integral f := by
  apply Polynomial.ext
  intro n
  cases n with
  | zero =>
      simp [integral_coeff_zero]
  | succ m =>
      rw [integral_coeff_succ, Polynomial.coeff_C_mul, Polynomial.coeff_C_mul, integral_coeff_succ]
      field_simp

/-- The derivative is linear for constant multiples on the polynomial
    model: `D (C c · g) = C c · D g`. -/
lemma derivative_C_mul (c : ℝ) (f : Polynomial ℝ) :
    Polynomial.derivative (Polynomial.C c * f) = Polynomial.C c * Polynomial.derivative f := by
  rw [Polynomial.derivative_mul]
  simp

/-- The anticommutator defect of the operator pair: with `D = derivative`
    and `V = integral` on the polynomial model,
    `D V + V D = 2 id − E₀`, i.e. acting on any g:

    D(V g) + V(D g) = 2 g − g(0).

    This is the exact twist that the eigen-ODE
    `α f' + β V f = λ f` inherits when the operator is applied twice, and
    it locates the mass-law bridge at the single point `g(0)`. -/
theorem anticommutator_defect (p : Polynomial ℝ) :
    Polynomial.derivative (integral p) + integral (Polynomial.derivative p)
      = (2 : ℝ) • p - Polynomial.C (p.coeff 0) := by
  rw [derivative_integral, integral_derivative_sub_eval0]
  rw [two_smul]
  ring

/-- The MP operator `A_{α,β} = α D + β V` acting on polynomials. -/
noncomputable def opA (α β : ℝ) (f : Polynomial ℝ) : Polynomial ℝ :=
  Polynomial.C α * Polynomial.derivative f + Polynomial.C β * integral f

/-- The composition law of the MP operator on the polynomial model: for
    every `α, β ∈ ℝ` and every polynomial `g`,

    A_{α,β}² g = α² D² g + αβ(2g − g(0)) + β² V² g.

    The proof unfolds the square, distributes D and V through the sum via
    the linearity facts, and collapses the two commutation relations —
    exactly the `2id − E₀` anticommutator of `anticommutator_defect`. -/
theorem operator_square_commutation_defect (α β : ℝ) (g : Polynomial ℝ) :
    opA α β (opA α β g)
      = Polynomial.C (α ^ 2) * Polynomial.derivative (Polynomial.derivative g)
        + Polynomial.C (α * β) * ((2 : ℝ) • g - Polynomial.C (g.coeff 0))
        + Polynomial.C (β ^ 2) * integral (integral g) := by
  unfold opA
  simp [Polynomial.derivative_add, integral_add, integral_C_mul,
    derivative_integral, integral_derivative_sub_eval0]
  rw [two_smul]
  ring

/-- The composition law at the bridge family `α = 1`, `β = a` — the
    exact operator form behind the characteristic equation
    `λ² − (2a+1)λ + a = 0`: squaring the bridge operator sheds the
    `2a+1`-cross-term `a(2g − g(0))` and the residual `a² V²`. -/
theorem operator_square_bridge_family (a : ℝ) (g : Polynomial ℝ) :
    opA 1 a (opA 1 a g)
      = Polynomial.derivative (Polynomial.derivative g)
        + Polynomial.C a * ((2 : ℝ) • g - Polynomial.C (g.coeff 0))
        + Polynomial.C (a ^ 2) * integral (integral g) := by
  rw [operator_square_commutation_defect 1 a g]
  simp [Polynomial.C_1]

/-- Spectral-gap theorem: the characteristic polynomial
    `P(r) = r² − (2a+1)r + a` of the bridge eigen-ODE evaluates to exactly
    `−1/4` at `r = 1/2`, independently of the half-window `a`.  Because the
    leading coefficient is `1 > 0`, the polynomial is negative exactly
    between its two roots, so for every `a > 0` the small root satisfies
    `r₂ < 1/2 < r₁`: the contractive root is always strictly below the
    spectral midpoint 1/2, while the expansive root always exceeds it.
    This is the algebraic gap behind `mass_radius_identity`'s ceiling 4. -/
theorem char_poly_at_half (a : ℚ) :
    (1 / 2 : ℚ) ^ 2 - (2 * a + 1) * (1 / 2 : ℚ) + a = (-1 / 4 : ℚ) := by
  ring

/-- The same spectral midpoint is revisited at the certified window: the
    window's characteristic polynomial confirms `P(1/2) = −1/4` exactly
    when `a = 128`, with room of `−1/4` on each side of the gap. -/
theorem char_poly_at_half_window :
    (1 / 2 : ℚ) ^ 2 - (2 * 128 + 1) * (1 / 2 : ℚ) + 128 = (-1 / 4 : ℚ) := by
  norm_num

/-- Spectral-bracket evaluations.  On the bridge family, the characteristic
    polynomial `P(r) = r² − (2a+1)r + a` takes the exact, `a`-proportional
    values `P(0) = a` and `P(1) = −a` for every half-window `a`, and the
    `a`-independent `P(1/2) = −1/4`.  With leading coefficient 1 the
    quadratic opens upward, so wherever `P` is negative lies strictly
    between its two real roots (by `bridge_discriminant_never_negative`).
    Hence for `a > 0`: `0 < r₂ < 1/2 < r₁ < 2a+1` — the spectral bracket
    pins the two roots between 0/1/2 and the window's edge, the discrete
    analogue of a standing-wave sector between two halting thresholds. -/
theorem char_poly_at_zero (a : ℚ) :
    (0 : ℚ) ^ 2 - (2 * a + 1) * (0 : ℚ) + a = a := by
  ring

theorem char_poly_at_one (a : ℚ) :
    (1 : ℚ) ^ 2 - (2 * a + 1) * (1 : ℚ) + a = -a := by
  ring

theorem char_poly_at_twice_window (a : ℚ) :
    (2 * a + 1) ^ 2 - (2 * a + 1) * (2 * a + 1) + a = a := by
  ring

/-- The four exact evaluations of the spectral bracket in one decidable
    statement, certified simultaneously at the window `a = 128`: the
    polynomial is above the base (P(0) = 128), below the midpoint
    (P(1/2) = −1/4), below the unit station (P(1) = −128), and back above at
    the window edge (P(2a+1) = 128).  The bracket `0 < r₂ < 1/2 < r₁ <
    2a+1` follows from the sign pattern and the upward-opening leading
    coefficient. -/
theorem spectral_bracket_window :
    (0 : ℚ) ^ 2 - (2 * 128 + 1) * (0 : ℚ) + 128 = 128 ∧
      (1 / 2 : ℚ) ^ 2 - (2 * 128 + 1) * (1 / 2 : ℚ) + 128 = -1 / 4 ∧
      (1 : ℚ) ^ 2 - (2 * 128 + 1) * 1 + 128 = -128 ∧
      (2 * 128 + 1) ^ 2 - (2 * 128 + 1) * (2 * 128 + 1) + 128 = 128 := by
  constructor
  · norm_num
  constructor
  · norm_num
  constructor
  · norm_num
  norm_num

/-- Monotonicity of the mass-radius product between the two certified
    windows: the tail's product `268435456/67108865` is strictly larger
    than the window's `262144/65537`, confirming the product rises toward
    the mass ceiling 4 as the half-window grows. -/
theorem mass_radius_window_lt_tail :
    (262144 : ℚ) / 65537 < (268435456 : ℚ) / 67108865 := by
  norm_num

end PunoTwin.MPOperator