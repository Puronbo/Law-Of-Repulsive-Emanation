import Mathlib

/-!
# PunoCalculus.SelfSimilarExponents

Formalisation of **Frontier 1** of the research note
`Linear Stability of Candidate Swirl Profiles.md`:

> The self-similar exponents are forced, and independent of the dimension
> parameter `n`.

**Setup (Hou's n = 3 classical system, arXiv:2405.10916).**  Writing the
self-similar ansatz

```
u1 = (T - t)^p U(ξ, η),  ω1 = (T - t)^q W(ξ, η),  ψ1 = (T - t)^s Ψ(ξ, η),
ξ = r/(T - t)^γ,          η = z/(T - t)^γ,
```

every term of the coupled system must enter at the same leading order for a
four-way dominant balance.  Under the substitution `ξ, η = x · τ^{-γ}` with
`τ = T - t`:

* time derivative `∂_t` contributes a factor `τ^{-1}` (the
  `(T-t)^{e-1}`-component; the similarity parts `-γ(ξ∂_ξ + η∂_η)` stay at the
  **same** power, so no balance condition changes),
* each `r`- or `z`-derivative contributes `τ^{-γ}`, so a second-order operator
  (any fixed `Δ_(r_n)`) contributes `τ^{-2γ}` **regardless of `n`**,
* each factor `u1·ψ1,z` contributes `τ^{p + s - γ}` (advection terms share this
  power, as do the stretching terms),
* the production term `(u1²),z` contributes `τ^{2p - γ}`.

The balance conditions reduce to a linear system in `(p, q, s, γ)` plus the
Poisson-consistency relation `Δ_(r_n) ψ1 ~ ω1`.  The module machine-checks:

1. **Existence**: `(p, q, s, γ) = (-1, -3/2, -1/2, 1/2)` satisfies all six
   balance equations and the Poisson relation (`forcedExponentsSatisfy`).
2. **Forced**: the six equations *alone* already force `γ = 1/2` and
   `s = -1/2`; the Poisson relation forces `q = -3/2`; the `ω1`-production
   balance then forces `p = -1` (`gammaForced`, `sForced`, `qForcedInPoisson`,
   `pForcedFromOmegaProduction`, and the combined `forcedExponentsUnique`).
3. **n-independent**: the balance system contains no reference to `n`, and
   the two places `n` does appear — the second-order operator prefactors and
   the coefficient `κ = n - 1` in `u^z = κ Ψ1 + r Ψ1,r` — only rescale
   prefactors, never τ-powers (`secondOrderPowerPrefactorIndependent`,
   `uzCoefficientPowerNIndependent`).  Hence the same exponents are forced for
   every real `n`, not just `n = 3`.

Honesty markers (same convention as `Hodge.quintic_codim2_open` /
`NavierStokes.nsGlobalRegularityOpen`):

* `selfSimilarProfileExistenceOpen : Bool := true` — whether a *bounded,
  admissible* profile realizing the forced exponents actually exists is an
  OPEN question.  Extension IV's two independent, corrected numerical searches
  failed to find one (the shape runs to the domain's outer corner), which is
  numerical evidence, not a theorem.
* `typeIINamingCertified : Bool := false` — the "Type II blow-up" naming
  attached to "exponents forced but no profile found" is an interpretive
  label, NOT a machine-checked theorem.
-/

namespace PunoCalculus.SelfSimilarExponents

noncomputable section

/-- The six dominant-balance equations in `(p, q, s, γ)` for the coupled
`(u1, ω1)` system, plus the Poisson consistency relation
`Δ_(r_n) ψ1 ~ ω1` (which ties `q` down given `s` and `γ`).  No equation
mentions `n`: the dimension-like parameter cancels in the power counting. -/
def BalanceSystem (p q s γ : ℝ) : Prop :=
  (p - 1 = p + s - γ) ∧          -- u1: time derivative ~ advection/stretching
  (p - 1 = p - 2 * γ) ∧          -- u1: time derivative ~ viscous diffusion
  (p + s - γ = p - 2 * γ) ∧      -- u1: stretching = diffusion
  (q - 1 = q + s - γ) ∧          -- ω1: time derivative ~ advection
  (q - 1 = 2 * p - γ) ∧          -- ω1: time derivative ~ production (u1²),z
  (q - 1 = q - 2 * γ) ∧          -- ω1: time derivative ~ viscous diffusion
  (q = s - 2 * γ)                -- Poisson consistency: Δ_(r_n) ψ1 ~ ω1

/-- The forced self-similar exponents of Frontier 1:
`γ = 1/2`, `p = -1`, `q = -3/2`, `s = -1/2`. -/
def forcedP : ℝ := -1
def forcedQ : ℝ := -3 / 2
def forcedS : ℝ := -1 / 2
def forcedGamma : ℝ := 1 / 2

/-- The forced quadruple satisfies all six balance equations and the Poisson
relation: the dominant-balance system is not empty. -/
theorem forcedExponentsSatisfy : BalanceSystem forcedP forcedQ forcedS forcedGamma := by
  unfold BalanceSystem forcedP forcedQ forcedS forcedGamma
  norm_num

/-- The u1 diffusion balance `p - 1 = p - 2γ` alone forces the spatial
rescale exponent: `γ = 1/2`. -/
theorem gammaForced (h : p - 1 = p - 2 * γ) : γ = (1 / 2 : ℝ) := by
  nlinarith

/-- The u1 time-vs-advection/stretching balance `p - 1 = p + s - γ`, given the
forced `γ`, forces the streamfunction exponent: `s = -1/2`. -/
theorem sForced (h : p - 1 = p + s - γ) (hg : γ = (1 / 2 : ℝ)) : s = -1 / 2 := by
  nlinarith

/-- The Poisson consistency relation forces the vorticity exponent:
`q = s - 2γ = -3/2` once `s` and `γ` are forced. -/
theorem qForcedInPoisson (h : q = s - 2 * γ) (hs : s = -1 / 2) (hg : γ = (1 / 2 : ℝ)) :
    q = -3 / 2 := by
  nlinarith

/-- The ω1 production balance `q - 1 = 2p - γ`, given the forced `q` and `γ`,
forces the swirl exponent: `p = -1`.  This is the last degree of freedom. -/
theorem pForcedFromOmegaProduction (h : q - 1 = 2 * p - γ) (hq : q = -3 / 2)
    (hg : γ = (1 / 2 : ℝ)) : p = -1 := by
  nlinarith

/-- **Frontier 1.**  The unique solution of the dominant-balance system is the
forced quadruple `(p, q, s, γ) = (-1, -3/2, -1/2, 1/2)`: no other exponents
admit a four-way dominant balance of the reduced axisymmetric system. -/
theorem forcedExponentsUnique (h : BalanceSystem p q s γ) :
    p = forcedP ∧ q = forcedQ ∧ s = forcedS ∧ γ = forcedGamma := by
  unfold BalanceSystem at h
  rcases h with ⟨hU1a, hU1d, hU1s, hW1a, hW1p, hW1d, hPois⟩
  have hGamma : γ = (1 / 2 : ℝ) := gammaForced hU1d
  have hS : s = -1 / 2 := sForced hU1a hGamma
  have hQ : q = -3 / 2 := qForcedInPoisson hPois hS hGamma
  have hP : p = -1 := pForcedFromOmegaProduction hW1p hQ hGamma
  unfold forcedP forcedQ forcedS forcedGamma
  exact And.intro hP (And.intro hQ (And.intro hS hGamma))

/-! ## n-independence

The dimension parameter `n` never enters the balance system (its type
signature contains no `n`), so unique forcedness holds unchanged for every
real `n`.  The two places `n` would appear concretely only rescale
prefactors:

1. the second-order operator `Δ_(r_n)` — its three terms are all
   second-order, contributing `basePower - 2γ` whatever the `n`-dependent
   coefficients are;
2. the coefficient `κ = n - 1` in `u^z = κ Ψ1 + r Ψ1,r` — a pure prefactor
   that multiplies the advection shape, never a τ-power.
-/

/-- The τ-power contributed by a second-order differential operator applied to
a `basePower`-term with an arbitrary prefactor. -/
def secondOrderPower (_c basePower γ : ℝ) : ℝ := basePower - 2 * γ

/-- A non-zero prefactor rescales the coefficient, never the τ-power:
`c₁ Δ` and `c₂ Δ` contribute the same power. -/
theorem secondOrderPowerPrefactorIndependent (_c₁ _c₂ basePower γ : ℝ) :
    secondOrderPower _c₁ basePower γ = secondOrderPower _c₂ basePower γ := rfl

/-- The τ-power of an advection term for a `basePower`-field with any
prefactor. -/
def advectionTermPower (_κ basePower γ : ℝ) : ℝ := basePower - γ

/-- The τ-power of an advection term does not depend on the coefficient
`κ = n - 1` arising in `u^z = κ Ψ1 + r Ψ1,r`. -/
theorem advectionTermPowerKappaIndependent (_κ₁ _κ₂ basePower γ : ℝ) :
    advectionTermPower _κ₁ basePower γ = advectionTermPower _κ₂ basePower γ := rfl

/-- Using the concrete coefficient `κ = n - 1` from the classical system:
the advection power is the same for every real `n` and `n'`. -/
theorem uzCoefficientPowerNIndependent (n n' basePower γ : ℝ) :
    advectionTermPower (n - 1) basePower γ =
      advectionTermPower (n' - 1) basePower γ := rfl

/-! ## Honesty markers (statement-layer convention)

* `selfSimilarProfileExistenceOpen` — whether a bounded, admissible profile
  realizing the forced exponents exists is OPEN.  The corrected numerical
  searches of Extension IV (explicit and semi-implicit) both found the shape
  running to the domain's outer corner instead of an interior profile; that is
  numerical evidence, not a proof of non-existence.
* `typeIINamingCertified` — the "Type II blow-up" reading of
  "exponents forced, no bounded profile found" is an interpretive label drawn
  from nonlinear blow-up theory, NOT a machine-checked theorem.
* The relation to Hou's published anomalous exponent `γ ≈ 0.5233` and dynamic
  effective dimension `≈ 3.188` is a commentary, not a formal statement.
-/

/-- Whether a bounded, admissible fixed-`n` profile realizing the forced
exponents exists: OPEN (numerical searches failed; no theorem either way). -/
def selfSimilarProfileExistenceOpen : Bool := true

/-- Whether the "Type II blow-up" interpretation is a machine-checked theorem:
it is not — it is an interpretive naming. -/
def typeIINamingCertified : Bool := false

/-- The certified inventory of this module. -/
def frontier1Facts : List String :=
  ["forced (p,q,s,γ) = (-1,-3/2,-1/2,1/2): unique four-way dominant balance (machine-checked)",
   "γ = 1/2 forced by u1 diffusion balance; s = -1/2 forced by u1 time/advection; q = -3/2 forced by Poisson; p = -1 forced by ω1 production (machine-checked)",
   "balance system is n-free; second-order and advection powers are prefactor-independent: exponents forced for EVERY real n, not just n = 3 (machine-checked)",
   "bounded profile at forced exponents EXISTS: OPEN (numerical searches fail; shape runs to domain corner)",
   "Type II blow-up naming: interpretive, NOT machine-checked",
   "connection to Hou γ ≈ 0.5233 / effective dimension ≈ 3.188: commentary only"]

/-- The inventory has exactly six entries. -/
theorem frontier1Facts_length : frontier1Facts.length = 6 := by
  native_decide

/-- The profile-existence question is open (boolean `true`, READ as
``is open''): no axiom attached. -/
theorem profile_existence_is_open : selfSimilarProfileExistenceOpen = true := rfl

/-- The Type II naming is not certified (boolean `false`). -/
theorem type_ii_naming_not_certified : typeIINamingCertified = false := rfl

end

end PunoCalculus.SelfSimilarExponents