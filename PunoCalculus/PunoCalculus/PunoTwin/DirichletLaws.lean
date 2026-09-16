import Mathlib.NumberTheory.LSeries.DirichletContinuation
import Mathlib.NumberTheory.LSeries.HurwitzZetaValues
import Mathlib.NumberTheory.LSeries.PrimesInAP
import Mathlib.NumberTheory.EulerProduct.DirichletLSeries
import Mathlib.NumberTheory.LSeries.Nonvanishing
import Mathlib.NumberTheory.Bernoulli
import Mathlib.Data.Nat.Prime.Defs
import Mathlib.NumberTheory.LegendreSymbol.ZModChar
import Mathlib.NumberTheory.SumTwoSquares
import Mathlib.Analysis.Real.Pi.Leibniz
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.Order.Interval.Set.UnorderedInterval
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Arctan

open DirichletCharacter HurwitzZeta Filter
open scoped Real BigOperators Topology
open Nat
open intervalIntegral

/-!
# Dirichlet L-function laws (Lean 4, mathlib)

The **L-function half-plane universality claims of Project Puno are NOT
SETTLED BY THIS PROJECT**.  What is certified here is the *provable*
spine of the L-function laws that underpin the twin's scaling motif
(the R57-60 denominator laws `1+4a²` / Fermat-prime spikes, the
spectral-midpoint bracket at `s = 1/2`, and the trivial-zero parity
laws), closed in mathlib with zero `sorry`/`axiom`:

  * **functional equation at `s = 1/2`**: for every primitive
    `χ`, `Λ(χ, 1/2) = rootNumber χ · Λ(χ⁻¹, 1/2)`
    (`center_symmetry`, from mathlib's
    `IsPrimitive.completedLFunction_one_sub`);
  * **Euler product**: the Dirichlet series of `χ` splits into the
    `∏ₚ (1 − χ(p) p^{−s})⁻¹` over primes (`eulerProduct_tprod`);
  * **special values at negative integers**: `ζ(−k) = (−1)ᵏ Bₖ₊₁/(k+1)`
    (`zeta_neg_nat`, incl. `ζ(−4) = B₅/5` and `ζ(2) = π²/6`);
  * **the concrete primitive quadratic characters** `χ₄`, `χ₈`, `χ₈'`
    (lifted to `ℂ`), with `conductor = 4` resp. `8`, hence
    **`IsPrimitive`**, and the functional-equation example at `1/2`;
  * **parity (trivial-zero) law**: `L(χ₄, negative odd) = 0`,
    `L(χ₈, negative even) = 0`, `L(χ₈', negative odd) = 0`
    (`χ₄ℂ_odd`, `χ₈ℂ_even`, `χ₈'ℂ_odd` + examples);
  * **nonvanishing at `s = 1`**: `L(1, χ₄) ≠ 0`, `L(1, χ₈) ≠ 0`,
    `L(1, χ₈') ≠ 0` and `L(χ, s) ≠ 0` on `Re s ≥ 1` (the Dirichlet
    prime-theorem engine, `LFunction_apply_one_ne_zero` /
    `LFunction_ne_zero_of_one_le_re` in mathlib), plus the Riemann
    boundary law `ζ(s) ≠ 0` on `Re s ≥ 1`;
  * **exact special value at `s = 1` for `χ₃`**: the classical
    `L(1, χ₃) = π/(3√3)` certified as a *Dirichlet-series* limit — the
    ordered partial sums `Σₙ χ₃(n)/n` tend to `π/(3√3)`
    (`chi3_series_real_pi_div_three_sqrt_three`,
    `chi3_series_pi_div_three_sqrt_three`), through the reindex-by-3
    (`chi3Partial_split`) and the integral
    `∫₀¹ 1/(1+x+x²) dx = π/(3√3)` (`integral_cubic_value`);  the `χ₄`
    instance `L(1, χ₄) = π/4` is certified in the Leibniz section below;
  * **von Staudt–Clausen**: `B₁₆ + ∑_{p−1 | 16} 1/p` is an integer,
    and the Fermat-spike lattice `p = 2^(2^j)+1 ↔ 2^(2^j−1) | k`
    with instances `5 ↔ 2|k`, `17 ↔ 8|k`, `257 ↔ 128|k`, `65537 ↔ 2^15|k`
    (`vonStaudt_B16`, `spike_law`, `spike_*`, `spike_*_iff`);  the
    `fermat_bridge`
    closes the loop to the MPOperator window denominator: at
    `a = 2^(2^k−1)`, `1 + 4a² = 2^(2^(k+1)) + 1` (so `a = 128` → `65537`);
  * **conductor-denominator law**: every prime divisor of the window
    denominator `1 + 4·a²` is `2` or `≡ 1 mod 4`, i.e. lies in the
    splitting rule `χ₄(p) = 1` of the conductor-4 character, and the
    converse — every prime `p ≡ 1 mod 4` divides some `1 + 4·a²` — so
    the odd primes dividing the window denominators are *exactly* the
    `p ≡ 1 mod 4` primes (`prime_divisor_of_denominator_family`,
    `denominator_exists_of_four_mod_one`, `prime_divides_denominator_iff`,
    `chi4_splits_of_denominator`, via the two-squares law
    `ZMod.exists_sq_eq_neg_one_iff`);  stated in the character register,
    `∃ a, p | 1 + 4·a² ⟺ χ₄(p) = 1` (`chi4_apply_eq_one_iff`,
    `chi4_splits_iff_denominator`) — a prime divides a window denominator
    iff smooth von Staudt–Clausen revision leaves the Fermat prime
    `χ₄`-split, tying the smooth-lattice spike and the conductor-4 law;
  * **Gauss sum and root number**: the `χ₄` Gauss sum evaluates to `2i`
    (`chi4_gaussSum`), and the epsilon factor is `rootNumber χ₄ = 1`
    (`chi4_rootNumber`), closing the conductor-4 character register;
  * **self-duality and the completed functional equation**: `χ₄` is
    quadratic and self-dual (`chi4_isQuadratic`, `chi4_self_conjugate`,
    `chi4_sq_eq_one`), `χ₄(−1) = −1` (`chi4_neg_one`), the Gauss-square
    identity `gaussSum(χ₄, stdAddChar)² = χ₄(−1)·4 = −4`
    (`chi4_gaussSum_sq`, `chi4_gaussSum_sq_value`), and the
    **self-dual completed functional equation**
    `Λ(χ₄, 1−s) = 4^{s−1/2} · Λ(χ₄, s)` (`chi4_completedL_one_sub`),
    combining the level `4`, root number `1` and self-duality;
  * **Gauss sums and root numbers of `χ₈`, `χ₈'`**: the eighth-root
    Gauss sums evaluate to `2·√2` resp. `2√2·i`
    (`chi8_gaussSum`, `chi8'_gaussSum`), the epsilon factors are
    `rootNumber χ₈ = 1` resp. `rootNumber χ₈' = 1` (`chi8_rootNumber`,
    `chi8'_rootNumber`), `e^{πi/4} = (√2/2)(1+i)` (`exp_pi_div_four_mul_I`),
    both characters are quadratic and **self-dual**
    (`chi8_isQuadratic`, `chi8'_isQuadratic`), the Gauss-square identities
    `gaussSum(χ₈, stdAddChar)² = 8` and `χ₈(−1)·8 = 8` resp.
    `χ₈'(−1)·8 = −8` (`chi8_gaussSum_sq_value`, `chi8'_gaussSum_sq_value`),
    and the **self-dual completed functional equations**
    `Λ(χ₈, 1−s) = 8^{s−1/2} · Λ(χ₈, s)` and
    `Λ(χ₈', 1−s) = 8^{s−1/2} · Λ(χ₈', s)`
    (`chi8_completedL_one_sub`, `chi8'_completedL_one_sub`),
    closing the level-8 character register;
  * **Gauss sum and root number of `χ₃`**: the third-root Gauss sum
    evaluates to `i·√3` (`chi3_gaussSum`), the epsilon factor is
    `rootNumber χ₃ = 1` (`chi3_rootNumber`), the primitive cube roots are
    `e^{2πi/3} = −1/2 + i·(√3/2)` and `e^{4πi/3} = −1/2 − i·(√3/2)`
    (`exp_two_pi_div_three_mul_I`, `exp_four_pi_div_three_mul_I`), the
    odd quadratic character `χ₃` is **self-dual** (`chi3_isQuadratic`,
    `chi3_self_conjugate`), and the **self-dual completed functional
    equation** `Λ(χ₃, 1−s) = 3^{s−1/2} · Λ(χ₃, s)` (`chi3_completedL_one_sub`)
    closes the level-3 odd-parity register.
  * **General quadratic-character lemma layer**: the character-independent
    laws behind all four registers — a quadratic character is **self-dual**
    (`self_conjugate_of_quadratic`), the **quadratic resolvent identity**
    `gaussSum(χ, stdAddChar)² = χ(−1)·p` for prime conductors `p`
    (`gaussSum_sq_of_quadratic`, via mathlib's `GaussSum.gaussSum_sq` over
    `𝔽ₚ`), the epsilon-square law `rootNumber χ ∈ {±1}`
    (`rootNumber_sq_of_quadratic`), and the **self-dual functional equation**
    for every primitive quadratic character
    `Λ(χ, 1−s) = N^{s−1/2} · rootNumber χ · Λ(χ, s)`
    (`completedL_one_sub_of_quadratic`).  The sign of the root number (in
    fact `+1` for `χ₄`, `χ₈`, `χ₈'`, `χ₃`) is pinned by the explicit
    Gauss-sum evaluations; the composite moduli `4` and `8` are covered by
    the direct computations above.
  * **L-function trivial zeros**: vanishing at negative integers for
    each register — `L(χ₄, −(2n+1)) = 0`, `L(χ₈, −2(n+1)) = 0`,
    `L(χ₈', −(2n+1)) = 0`, `L(χ₃, −(2n+1)) = 0` — following from
    the parity of the functional equation (Γ((s+1)/2) for odd χ,
    Γ(s/2) for even χ).
  * **Dirichlet's theorem for the supported levels**: instantiating
    mathlib's full theorem (`DirichletsTheorem`) — whose engine is the
    nonvanishing of `L(1, χ)` above — every residue class coprime to
    `3`, `4`, or `8` contains infinitely many primes
    (`infinitelyManyPrimes_mod_three`, `infinitelyManyPrimes_mod_four`,
    `infinitelyManyPrimes_mod_eight` and the per-residue coverage
    examples);
  * **exact special value at `s = 1` for `χ₄`**: the Dirichlet series
    `Σₙ χ₄(n)/n` converges (conditionally, in the ordered-partial-sum
    sense) to `π/4` — the classical `L(1, χ₄) = π/4` value
    (`chi4_series_real_pi_div_four`, `chi4_series_pi_div_four`).
    mathlib's bridge from the *analytic* `LFunction` to the Dirichlet
    series (`LFunction_eq_LSeries`) requires `1 < s.re`, so no bridge
    exists at `s = 1`; the value is therefore certified here as the
    limit of the ordered partial sums (via the Leibniz `π/4` series and
    the reindex `n = 2i + 1`).

Everything below is fully proved.  The remaining — the exact
transcendental identities `L(2, χ₋₄) = Catalan's G` and the
`s = 1` special values `L(1, χ₃) = π/(3√3)`, `L(1, χ₈) = ln(1+√2)/√2`,
`L(1, χ₈') = π/(4√2)` stated in the code as future-work goals, or any
claim that the aperiodic lattice of the *discrete* twin reproduces these
laws beyond the verified instances — is not claimed here.
-/

namespace PunoTwin.Dirichlet

variable {N : ℕ} [NeZero N]

/-- **Functional equation at the spectral midpoint `s = 1/2`** (primitive
character): `Λ(χ, 1/2) = rootNumber χ · Λ(χ⁻¹, 1/2)`. -/
lemma center_symmetry (χ : DirichletCharacter ℂ N) (hχ : χ.IsPrimitive) :
    completedLFunction χ (1 / 2) = rootNumber χ * completedLFunction χ⁻¹ (1 / 2) := by
  have h := hχ.completedLFunction_one_sub (1 / 2)
  calc
    completedLFunction χ (1 / 2) = completedLFunction χ (1 - 1 / 2) := by norm_num
    _ = N ^ (1 / 2 - 1 / 2) * rootNumber χ * completedLFunction χ⁻¹ (1 / 2) := h
    _ = rootNumber χ * completedLFunction χ⁻¹ (1 / 2) := by simp

omit [NeZero N] in
/-- **Euler product for a Dirichlet `L`-series** (convergent half-plane):
`L(s, χ) = ∏ₚ (1 − χ(p) p^{−s})⁻¹`. -/
lemma eulerProduct_tprod (χ : DirichletCharacter ℂ N) {s : ℂ} (hs : 1 < s.re) :
    ∏' p : Primes, (1 - χ p * (p : ℂ) ^ (-s))⁻¹ = LSeries (fun n : ℕ ↦ χ n) s := by
  simpa using (DirichletCharacter.LSeries_eulerProduct_tprod χ hs)

/-- **Special value at negative integers**: `ζ(−k) = (−1)ᵏ Bₖ₊₁/(k+1)`. -/
lemma zeta_neg_nat (k : ℕ) : riemannZeta (-k) = (-1 : ℂ) ^ k * bernoulli (k + 1) / (k + 1) :=
  riemannZeta_neg_nat_eq_bernoulli k

/-- Example of the law at `k = 4`: `ζ(−4) = B₅/5` (and `B₅ = 0`). -/
example : riemannZeta (-(4 : ℂ)) = (bernoulli 5 : ℂ) / 5 := by
  have h := zeta_neg_nat 4
  norm_num at h
  simpa using h

/-- Example of the law at `s = 2` (positive side): `ζ(2) = π²/6`. -/
example : riemannZeta 2 = (π : ℂ) ^ 2 / 6 := riemannZeta_two

/-! ### Concrete primitive quadratic characters `χ₄`, `χ₈`, `χ₈'` lifted to `ℂ` -/

/-- `χ₄` (the nontrivial mod-4 character) lifted to `ℂ`. -/
def χ₄ℂ : DirichletCharacter ℂ 4 := ZMod.χ₄.ringHomComp (algebraMap ℤ ℂ)

/-- `χ₈` (ℚ(√2)/ℚ) lifted to `ℂ`. -/
def χ₈ℂ : DirichletCharacter ℂ 8 := ZMod.χ₈.ringHomComp (algebraMap ℤ ℂ)

/-- `χ₈'` (ℚ(√−2)/ℚ) lifted to `ℂ`. -/
def χ₈'ℂ : DirichletCharacter ℂ 8 := ZMod.χ₈'.ringHomComp (algebraMap ℤ ℂ)

namespace χ₄ℂ

lemma apply_one : χ₄ℂ 1 = 1 := by norm_num [χ₄ℂ]
lemma apply_three : χ₄ℂ 3 = -1 := by norm_num [χ₄ℂ]

lemma apply_zero : χ₄ℂ 0 = 0 := by norm_num [χ₄ℂ]
lemma apply_two : χ₄ℂ 2 = 0 := by norm_num [χ₄ℂ]

lemma ne_char_one : χ₄ℂ ≠ 1 := by
  intro h
  have this := congrArg (fun ψ : DirichletCharacter ℂ 4 ↦ ψ (3 : ZMod 4)) h
  change χ₄ℂ 3 = (1 : DirichletCharacter ℂ 4) 3 at this
  have h1 : (1 : DirichletCharacter ℂ 4) 3 = (1 : ℂ) := by
    have h3u : IsUnit (3 : ZMod 4) := by
      exact (ZMod.isUnit_iff_coprime 3 4).mpr (by norm_num)
    exact MulChar.one_apply h3u
  rw [apply_three, h1] at this
  norm_num at this

lemma not_factorsThrough_two : ¬ χ₄ℂ.FactorsThrough 2 := by
  intro hf
  rcases hf with ⟨hd, χ₀, hχ⟩
  have h3 := congrArg (fun ψ : DirichletCharacter ℂ 4 ↦ ψ (3 : ZMod 4)) hχ
  have hcast : (changeLevel hd χ₀) (3 : ZMod 4) = χ₀ (3 : ZMod 2) := by
    simpa using (changeLevel_eq_cast_of_dvd' (R := ℂ) (χ := χ₀) hd
      (by decide : IsCoprime (3 : ℤ) 4))
  rw [hcast] at h3
  have h31 : (3 : ZMod 2) = 1 := by decide
  rw [h31] at h3
  norm_num [apply_three, χ₄ℂ, map_one] at h3

/-- The conductor of `χ₄` is `4`. -/
lemma conductor_eq_four : χ₄ℂ.conductor = 4 := by
  apply le_antisymm
  · have hd := χ₄ℂ.conductor_dvd_level
    exact le_of_dvd (by norm_num) hd
  · by_contra h
    have hle : χ₄ℂ.conductor < 4 := lt_of_not_ge h
    interval_cases hc : χ₄ℂ.conductor
    · exfalso
      exact χ₄ℂ.conductor_ne_zero hc
    · have hχ : χ₄ℂ = 1 := (DirichletCharacter.eq_one_iff_conductor_eq_one).mpr hc
      exact ne_char_one hχ
    · exact not_factorsThrough_two <|
        (DirichletCharacter.mem_conductorSet_iff χ₄ℂ).1 <| by simpa [hc] using conductor_mem_conductorSet χ₄ℂ
    · have : 3 ∣ 4 := by simpa [hc] using χ₄ℂ.conductor_dvd_level
      omega

/-- `χ₄` is a **primitive** character (level equals conductor). -/
lemma isPrimitive : χ₄ℂ.IsPrimitive := by
  rw [DirichletCharacter.IsPrimitive]
  exact conductor_eq_four

end χ₄ℂ

/-- Functional-equation example at `s = 1/2` for `χ₄`. -/
example : completedLFunction χ₄ℂ (1 / 2) = rootNumber χ₄ℂ * completedLFunction χ₄ℂ⁻¹ (1 / 2) :=
  center_symmetry χ₄ℂ χ₄ℂ.isPrimitive

namespace χ₈ℂ

lemma apply_zero : χ₈ℂ (0 : ZMod 8) = 0 := by norm_num [χ₈ℂ]
lemma apply_one : χ₈ℂ (1 : ZMod 8) = 1 := by norm_num [χ₈ℂ]
lemma apply_two : χ₈ℂ (2 : ZMod 8) = 0 := by norm_num [χ₈ℂ]
lemma apply_three : χ₈ℂ 3 = -1 := by norm_num [χ₈ℂ]
lemma apply_four : χ₈ℂ (4 : ZMod 8) = 0 := by norm_num [χ₈ℂ]
lemma apply_five : χ₈ℂ 5 = -1 := by norm_num [χ₈ℂ]
lemma apply_six : χ₈ℂ (6 : ZMod 8) = 0 := by norm_num [χ₈ℂ]
lemma apply_seven : χ₈ℂ 7 = 1 := by norm_num [χ₈ℂ]

lemma ne_char_one : χ₈ℂ ≠ 1 := by
  intro h
  have this := congrArg (fun ψ : DirichletCharacter ℂ 8 ↦ ψ (3 : ZMod 8)) h
  change χ₈ℂ 3 = (1 : DirichletCharacter ℂ 8) 3 at this
  have h1 : (1 : DirichletCharacter ℂ 8) 3 = (1 : ℂ) := by
    have h3u : IsUnit (3 : ZMod 8) := by
      exact (ZMod.isUnit_iff_coprime 3 8).mpr (by norm_num)
    exact MulChar.one_apply h3u
  rw [apply_three, h1] at this
  norm_num at this

lemma not_factorsThrough_four : ¬ χ₈ℂ.FactorsThrough 4 := by
  intro hf
  rcases hf with ⟨hd, χ₀, hχ⟩
  have h5 := congrArg (fun ψ : DirichletCharacter ℂ 8 ↦ ψ (5 : ZMod 8)) hχ
  have hcast : (changeLevel hd χ₀) (5 : ZMod 8) = χ₀ (5 : ZMod 4) := by
    simpa using (changeLevel_eq_cast_of_dvd' (R := ℂ) (χ := χ₀) hd
      (by decide : IsCoprime (5 : ℤ) 8))
  rw [hcast] at h5
  have h51 : (5 : ZMod 4) = 1 := by decide
  rw [h51] at h5
  norm_num [apply_five, χ₈ℂ, map_one] at h5

lemma not_factorsThrough_two : ¬ χ₈ℂ.FactorsThrough 2 := by
  intro hf
  rcases hf with ⟨hd, χ₀, hχ⟩
  have h3 := congrArg (fun ψ : DirichletCharacter ℂ 8 ↦ ψ (3 : ZMod 8)) hχ
  have hcast : (changeLevel hd χ₀) (3 : ZMod 8) = χ₀ (3 : ZMod 2) := by
    simpa using (changeLevel_eq_cast_of_dvd' (R := ℂ) (χ := χ₀) hd
      (by decide : IsCoprime (3 : ℤ) 8))
  rw [hcast] at h3
  have h31 : (3 : ZMod 2) = 1 := by decide
  rw [h31] at h3
  norm_num [apply_three, χ₈ℂ, map_one] at h3

/-- The conductor of `χ₈` is `8`. -/
lemma conductor_eq_eight : χ₈ℂ.conductor = 8 := by
  apply le_antisymm
  · have hd := χ₈ℂ.conductor_dvd_level
    exact le_of_dvd (by norm_num) hd
  · by_contra h
    have hle : χ₈ℂ.conductor < 8 := lt_of_not_ge h
    have hd := χ₈ℂ.conductor_dvd_level
    interval_cases hc : χ₈ℂ.conductor <;> norm_num at hd
    · have hχ : χ₈ℂ = 1 := (DirichletCharacter.eq_one_iff_conductor_eq_one).mpr hc
      exact ne_char_one hχ
    · exact not_factorsThrough_two <|
        (DirichletCharacter.mem_conductorSet_iff χ₈ℂ).1 <| by simpa [hc] using conductor_mem_conductorSet χ₈ℂ
    · exact not_factorsThrough_four <|
        (DirichletCharacter.mem_conductorSet_iff χ₈ℂ).1 <| by simpa [hc] using conductor_mem_conductorSet χ₈ℂ

/-- `χ₈` is a **primitive** character. -/
lemma isPrimitive : χ₈ℂ.IsPrimitive := by
  rw [DirichletCharacter.IsPrimitive]
  exact conductor_eq_eight

end χ₈ℂ

/-- Functional-equation example at `s = 1/2` for `χ₈`. -/
example : completedLFunction χ₈ℂ (1 / 2) = rootNumber χ₈ℂ * completedLFunction χ₈ℂ⁻¹ (1 / 2) :=
  center_symmetry χ₈ℂ χ₈ℂ.isPrimitive

namespace χ₈'ℂ

lemma apply_zero : χ₈'ℂ (0 : ZMod 8) = 0 := by norm_num [χ₈'ℂ]
lemma apply_one : χ₈'ℂ (1 : ZMod 8) = 1 := by norm_num [χ₈'ℂ]
lemma apply_two : χ₈'ℂ (2 : ZMod 8) = 0 := by norm_num [χ₈'ℂ]
lemma apply_three : χ₈'ℂ (3 : ZMod 8) = 1 := by norm_num [χ₈'ℂ]
lemma apply_four : χ₈'ℂ (4 : ZMod 8) = 0 := by norm_num [χ₈'ℂ]
lemma apply_five : χ₈'ℂ 5 = -1 := by norm_num [χ₈'ℂ]
lemma apply_six : χ₈'ℂ (6 : ZMod 8) = 0 := by norm_num [χ₈'ℂ]
lemma apply_seven : χ₈'ℂ 7 = -1 := by norm_num [χ₈'ℂ]

lemma ne_char_one : χ₈'ℂ ≠ 1 := by
  intro h
  have this := congrArg (fun ψ : DirichletCharacter ℂ 8 ↦ ψ (5 : ZMod 8)) h
  change χ₈'ℂ 5 = (1 : DirichletCharacter ℂ 8) 5 at this
  have h1 : (1 : DirichletCharacter ℂ 8) 5 = (1 : ℂ) := by
    have h5u : IsUnit (5 : ZMod 8) := by
      exact (ZMod.isUnit_iff_coprime 5 8).mpr (by norm_num)
    exact MulChar.one_apply h5u
  rw [apply_five, h1] at this
  norm_num at this

lemma not_factorsThrough_four : ¬ χ₈'ℂ.FactorsThrough 4 := by
  intro hf
  rcases hf with ⟨hd, χ₀, hχ⟩
  have h5 := congrArg (fun ψ : DirichletCharacter ℂ 8 ↦ ψ (5 : ZMod 8)) hχ
  have hcast : (changeLevel hd χ₀) (5 : ZMod 8) = χ₀ (5 : ZMod 4) := by
    simpa using (changeLevel_eq_cast_of_dvd' (R := ℂ) (χ := χ₀) hd
      (by decide : IsCoprime (5 : ℤ) 8))
  rw [hcast] at h5
  have h51 : (5 : ZMod 4) = 1 := by decide
  rw [h51] at h5
  norm_num [apply_five, χ₈'ℂ, map_one] at h5

lemma not_factorsThrough_two : ¬ χ₈'ℂ.FactorsThrough 2 := by
  intro hf
  rcases hf with ⟨hd, χ₀, hχ⟩
  have h5 := congrArg (fun ψ : DirichletCharacter ℂ 8 ↦ ψ (5 : ZMod 8)) hχ
  have hcast : (changeLevel hd χ₀) (5 : ZMod 8) = χ₀ (5 : ZMod 2) := by
    simpa using (changeLevel_eq_cast_of_dvd' (R := ℂ) (χ := χ₀) hd
      (by decide : IsCoprime (5 : ℤ) 8))
  rw [hcast] at h5
  have h51 : (5 : ZMod 2) = 1 := by decide
  rw [h51] at h5
  norm_num [apply_five, χ₈'ℂ, map_one] at h5

/-- The conductor of `χ₈'` is `8`. -/
lemma conductor_eq_eight : χ₈'ℂ.conductor = 8 := by
  apply le_antisymm
  · have hd := χ₈'ℂ.conductor_dvd_level
    exact le_of_dvd (by norm_num) hd
  · by_contra h
    have hle : χ₈'ℂ.conductor < 8 := lt_of_not_ge h
    have hd := χ₈'ℂ.conductor_dvd_level
    interval_cases hc : χ₈'ℂ.conductor <;> norm_num at hd
    · have hχ : χ₈'ℂ = 1 := (DirichletCharacter.eq_one_iff_conductor_eq_one).mpr hc
      exact ne_char_one hχ
    · exact not_factorsThrough_two <|
        (DirichletCharacter.mem_conductorSet_iff χ₈'ℂ).1 <| by simpa [hc] using conductor_mem_conductorSet χ₈'ℂ
    · exact not_factorsThrough_four <|
        (DirichletCharacter.mem_conductorSet_iff χ₈'ℂ).1 <| by simpa [hc] using conductor_mem_conductorSet χ₈'ℂ

/-- `χ₈'` is a **primitive** character. -/
lemma isPrimitive : χ₈'ℂ.IsPrimitive := by
  rw [DirichletCharacter.IsPrimitive]
  exact conductor_eq_eight

end χ₈'ℂ

/-- Functional-equation example at `s = 1/2` for `χ₈'`. -/
example : completedLFunction χ₈'ℂ (1 / 2) = rootNumber χ₈'ℂ * completedLFunction χ₈'ℂ⁻¹ (1 / 2) :=
  center_symmetry χ₈'ℂ χ₈'ℂ.isPrimitive

/-! ### Fermat-spike law for Bernoulli denominators (R57-60 motif) -/

/-- **von Staudt–Clausen for `B₁₆`**: `B₁₆ + ∑_{p−1 | 16} 1/p` is an
integer. -/
lemma vonStaudt_B16 :
    bernoulli 16 + ∑ p ∈ Finset.range 18 with p.Prime ∧ (p - 1) ∣ 16,
      (1 : ℚ) / (p : ℚ) ∈ Set.range Int.cast := by
  simpa using (Bernoulli.vonStaudt_clausen 8)

/-- **Fermat-spike lattice**: `p = 2^(2^j) + 1` spikes in the denominator
of `B_{2k}` exactly when `p - 1 = 2^(2^j)` divides `2k`, i.e.
`2^(2^j - 1) | k` (`spike_lattice`: the "at exactly the multiples"
converse).

Concrete instances (R57-60 motif): `5 ↔ 2 | k`, `17 ↔ 8 | k`,
`257 ↔ 128 | k`, `65537 ↔ 2^15 | k`. -/
lemma spike_5_prime : Nat.Prime 5 := by decide
lemma spike_5_cond : (5 - 1) ∣ 2 * 2 := by norm_num
lemma spike_17_prime : Nat.Prime 17 := by decide
lemma spike_17_cond : (17 - 1) ∣ 2 * 8 := by norm_num
lemma spike_257_prime : Nat.Prime 257 := by native_decide
lemma spike_257_cond : (257 - 1) ∣ 2 * 128 := by norm_num

/-- The lattice law for every `j`: `2^(2^j) | 2·2^(2^j−1)`, i.e. the spike
of `F_j = 2^(2^j)+1` occurs at every `k` multiple of `2^(2^j−1)`. -/
lemma spike_law (j : ℕ) : (2 ^ (2 ^ j) + 1 - 1 : ℕ) ∣ 2 * 2 ^ (2 ^ j - 1) := by
  rw [Nat.add_sub_cancel]
  have hpos : 0 < 2 ^ j := pow_pos (by norm_num) j
  have hsucc : (2 ^ j - 1) + 1 = 2 ^ j := Nat.succ_pred_eq_of_pos hpos
  rw [← hsucc, pow_succ, mul_comm]
  exact dvd_rfl

/-- **Bridge to the MPOperator Fermat denominators** (R57–60 window motif):
at `a = 2^(2^k−1)` the window denominator `1 + 4·a²` is exactly the
`(k+1)`-th Fermat number `2^(2^(k+1)) + 1`.  Instances: `a = 2` → `17`,
`a = 8` → `257`, `a = 128` → `65537`. -/
lemma fermat_bridge (k : ℕ) :
    1 + 4 * (2 ^ (2 ^ k - 1)) ^ 2 = 2 ^ (2 ^ (k + 1)) + 1 := by
  rw [show (4 : ℕ) = 2 ^ 2 by norm_num]
  rw [← pow_mul]
  rw [← pow_add]
  have hsum : 2 + (2 ^ k - 1) * 2 = 2 ^ (k + 1) := by
    rw [pow_succ]
    have hpos : 0 < 2 ^ k := pow_pos (by norm_num) k
    omega
  rw [hsum]
  omega

/-- The `k=3` instance: `a = 128` gives the window denominator `65537`. -/
lemma fermat_bridge_window :
    1 + 4 * (2 ^ (2 ^ 3 - 1)) ^ 2 = 2 ^ (2 ^ 4) + 1 :=
  fermat_bridge 3

/-- `65537 = 2^16 + 1` is prime (the `a = 128` window denominator). -/
lemma spike_65537_prime : Nat.Prime (2 ^ 16 + 1) := by
  native_decide

/-- The 65537 spike condition: `65537 − 1 = 2^16` divides `2·2^15`. -/
lemma spike_65537_cond : (2 ^ 16 + 1 - 1) ∣ 2 * 2 ^ 15 := by
  norm_num

/-- **Spike-lattice iff** (the "at exactly the multiples" converse): for
the Fermat form `F_j = 2^(2^j) + 1`, the spike condition
`F_j − 1 = 2^(2^j) | 2k` holds *exactly* when `2^(2^j − 1) | k` — so
`B_{2k}` revisits `F_j`-spikes precisely at the lattice of multiples of
`2^(2^j−1)`, never between them (purely arithmetic; the von Staudt–
Clausen membership above is the Bernoulli-side half). -/
lemma spike_lattice (j k : ℕ) :
    (2 ^ (2 ^ j) ∣ 2 * k ↔ 2 ^ (2 ^ j - 1) ∣ k) := by
  have hpos : 0 < 2 ^ j := pow_pos (by norm_num) j
  have hpow : 2 ^ j = (2 ^ j - 1) + 1 := by omega
  have h2 : 2 * 2 ^ (2 ^ j - 1) = 2 ^ (2 ^ j) := by
    nth_rewrite 2 [hpow]
    rw [pow_add, pow_one, mul_comm]
  rw [← h2]
  exact Nat.mul_dvd_mul_iff_left (by norm_num : 0 < (2 : ℕ))

/-- The spike condition with the `+ 1 − 1` cancelled: `(F_j − 1) | 2k`
reduces exactly to the lattice law. -/
lemma spike_iff (j k : ℕ) :
    (2 ^ (2 ^ j) + 1 - 1) ∣ 2 * k ↔ 2 ^ (2 ^ j - 1) ∣ k := by
  rw [Nat.add_sub_cancel]
  exact spike_lattice j k

/-- `5 ↔ 2 | k`: `4 = 2² | 2k` iff `k` even — *exactly*, matching
`spike_5_cond` at `k = 2`. -/
lemma spike_5_iff (k : ℕ) : (5 - 1) ∣ 2 * k ↔ 2 ∣ k := by
  convert spike_iff 1 k using 1 <;> norm_num

/-- `17 ↔ 8 | k`: `16 = 2⁴ | 2k` iff `8 | k` — *exactly*, matching
`spike_17_cond` at `k = 8`. -/
lemma spike_17_iff (k : ℕ) : (17 - 1) ∣ 2 * k ↔ 8 ∣ k := by
  convert spike_iff 2 k using 1 <;> norm_num

/-- `257 ↔ 128 | k`: `256 = 2⁸ | 2k` iff `128 | k` — *exactly*, matching
`spike_257_cond` at `k = 128`. -/
lemma spike_257_iff (k : ℕ) : (257 - 1) ∣ 2 * k ↔ 128 ∣ k := by
  convert spike_iff 3 k using 1 <;> norm_num

/-- `65537 = 2^16 + 1 ↔ 2^15 | k`: `2^16 | 2k` iff `2^15 | k` —
*exactly*, matching `spike_65537_cond` at `k = 2^15`. -/
lemma spike_65537_iff (k : ℕ) : (2 ^ 16 + 1 - 1) ∣ 2 * k ↔ 2 ^ 15 ∣ k := by
  convert spike_iff 4 k using 1 <;> norm_num

/-! ### Conductor-denominator law (the `1+4a²` window and conductor `4`) -/

set_option linter.style.haveILetI false in
/-- **Conductor-denominator law** (forward): every prime divisor of the
window-denominator family `1 + 4·a²` is either `2` or `≡ 1 mod 4` —
i.e. sits in the conductor-4 splitting rule of the character.  From
`p | 1 + 4a²` one gets `(2a)² ≡ −1 (mod p)`, so `−1` is a square in
`ZMod p`, and by the two-squares law (`ZMod.exists_sq_eq_neg_one_iff`)
`p % 4 ≠ 3`, which forces `p = 2 ∨ p % 4 = 1`. -/
lemma prime_divisor_of_denominator_family (p a : ℕ) (hp : p.Prime) (hd : p ∣ 1 + 4 * a ^ 2) :
    p = 2 ∨ p % 4 = 1 := by
  haveI : Fact p.Prime := ⟨hp⟩
  -- -1 is a square mod p, since (2a)^2 = -1 mod p
  have hsq : IsSquare (-1 : ZMod p) := by
    refine ⟨((2 * a : ℕ) : ZMod p), ?_⟩
    have hc0 : ((1 + 4 * a ^ 2 : ℕ) : ZMod p) = 0 := (ZMod.natCast_eq_zero_iff _ _).mpr hd
    have hb : ((4 * a ^ 2 : ℕ) : ZMod p) = -1 := by
      apply eq_neg_of_add_eq_zero_left
      simpa [Nat.cast_add, add_comm] using hc0
    rw [← hb]
    norm_cast
    ring_nf
  -- two-squares / Euler: -1 is a square mod p iff p % 4 != 3
  have h13 : p % 4 ≠ 3 := (ZMod.exists_sq_eq_neg_one_iff (p := p)).mp hsq
  -- interval-cases the residue
  have hlt : p % 4 < 4 := Nat.mod_lt p (by norm_num)
  have hp_eq_two_of_two_dvd : 2 ∣ p → p = 2 := by
    intro h2dvd
    exact (Nat.Prime.dvd_iff_eq hp (by norm_num : (2 : ℕ) ≠ 1)).mp h2dvd
  interval_cases hq : p % 4
  · left
    exact hp_eq_two_of_two_dvd <| Nat.dvd_trans (by norm_num : (2 : ℕ) ∣ 4)
      ((Nat.dvd_iff_mod_eq_zero).mpr hq)
  · right
    rfl
  · left
    exact hp_eq_two_of_two_dvd ((Nat.dvd_iff_mod_eq_zero).mpr (by omega))
  · exact (h13 rfl).elim

/-- **Conductor-denominator law, χ₄ form**: for an odd prime divisor `p`
of a window denominator `1 + 4·a²`, the character takes the splitting
value `χ₄(p) = 1`. -/
lemma chi4_splits_of_denominator (p a : ℕ) (hp : p.Prime) (hp2 : p ≠ 2)
    (hd : p ∣ 1 + 4 * a ^ 2) : χ₄ℂ (p : ZMod 4) = 1 := by
  rcases prime_divisor_of_denominator_family p a hp hd with rfl | hm
  · exfalso
    exact hp2 rfl
  · have hcast : (p : ZMod 4) = (1 : ZMod 4) := by
      have htmp : p % 4 = 1 % 4 := by
        rw [hm]
      exact (ZMod.natCast_eq_natCast_iff' p 1 4).mpr htmp
    rw [hcast]
    norm_num [χ₄ℂ]

/-- Example: the Fermat prime `5` divides the window denominator at
`a = 1` and satisfies `χ₄(5) = 1`. -/
example : χ₄ℂ (5 : ZMod 4) = 1 := by
  exact chi4_splits_of_denominator 5 1 (by decide) (by norm_num) (by norm_num)

/-- Example: the `a = 2` window denominator `17` is `≡ 1 mod 4` and is
`χ₄`-split. -/
example : χ₄ℂ (17 : ZMod 4) = 1 := by
  exact chi4_splits_of_denominator 17 2 (by decide) (by norm_num) (by norm_num)

set_option linter.style.haveILetI false in
/-- **Conductor-denominator law** (converse): every prime `p ≡ 1 mod 4`
divides some window denominator `1 + 4·a²` — since `−1` is a square in
`ZMod p`, take `a` to be the root divided by `2`. -/
lemma denominator_exists_of_four_mod_one (p : ℕ) (hp : p.Prime) (hp1 : p % 4 = 1) :
    ∃ a : ℕ, p ∣ 1 + 4 * a ^ 2 := by
  haveI : Fact p.Prime := ⟨hp⟩
  have hp2 : p ≠ 2 := by omega
  have h2ne : (2 : ZMod p) ≠ 0 := by
    intro hz
    have hd : p ∣ 2 := (ZMod.natCast_eq_zero_iff 2 p).mp hz
    have heq : p = 2 := (Nat.prime_dvd_prime_iff_eq hp Nat.prime_two).mp hd
    exact hp2 heq
  have h13 : p % 4 ≠ 3 := by
    rw [hp1]
    norm_num
  have hsq : IsSquare (-1 : ZMod p) := (ZMod.exists_sq_eq_neg_one_iff (p := p)).mpr h13
  rcases hsq with ⟨y, hy⟩
  let a : ℕ := (y * (2 : ZMod p)⁻¹).val
  refine ⟨a, ?_⟩
  have hcast : (a : ZMod p) = y * (2 : ZMod p)⁻¹ := by
    dsimp [a]
    exact ZMod.natCast_zmod_val (y * (2 : ZMod p)⁻¹)
  have h2a : (2 : ZMod p) * (a : ZMod p) = y := by
    rw [hcast]
    calc
      (2 : ZMod p) * (y * (2 : ZMod p)⁻¹) = y * ((2 : ZMod p) * (2 : ZMod p)⁻¹) := by ring
      _ = y := by rw [mul_inv_cancel₀ h2ne, mul_one]
  have hsq2 : (2 * (a : ZMod p)) ^ 2 = -1 := by
    rw [h2a]
    simpa [pow_two] using hy.symm
  have hconn : ((4 * a ^ 2 : ℕ) : ZMod p) = (2 * (a : ZMod p)) ^ 2 := by
    simp [show 4 * a ^ 2 = (2 * a) ^ 2 by ring]
  have hsq2_aln : ((4 * a ^ 2 : ℕ) : ZMod p) = -1 := by
    rw [hconn]
    exact hsq2
  have hzmod : ((1 + 4 * a ^ 2 : ℕ) : ZMod p) = 0 := by
    rw [Nat.cast_add]
    rw [hsq2_aln]
    norm_num
  exact (ZMod.natCast_eq_zero_iff (1 + 4 * a ^ 2) p).mp hzmod

/-- **Conductor-denominator law** (full iff): an odd prime divides a window
denominator `1 + 4·a²` iff `p ≡ 1 mod 4`. -/
lemma prime_divides_denominator_iff (p : ℕ) (hp : p.Prime) (hp2 : p ≠ 2) :
    (∃ a : ℕ, p ∣ 1 + 4 * a ^ 2) ↔ p % 4 = 1 := by
  constructor
  · rintro ⟨a, hd⟩
    rcases prime_divisor_of_denominator_family p a hp hd with hp2' | hm
    · exfalso
      exact hp2 hp2'
    · exact hm
  · intro hm
    exact denominator_exists_of_four_mod_one p hp hm

/-- Example: `13 ≡ 1 mod 4`, and indeed `13` divides the window denominator
at `a = 4` since `13 | 65 = 1 + 4·4²`. -/
example : 13 ∣ 1 + 4 * 4 ^ 2 := by
  norm_num

/-- The value of the lifted character `χ₄ℂ` on `p : ℤ/4` is `1` iff
`p ≡ 1 mod 4` — the conductor-4 splitting rule at the residue level
(mathlib evaluates `ZMod.χ₄ (p : ZMod 4)` by `p % 4`). -/
lemma chi4_apply_eq_one_iff (p : ℕ) : χ₄ℂ (p : ZMod 4) = 1 ↔ p % 4 = 1 := by
  have help : ZMod.χ₄ (p : ZMod 4) = (1 : ℤ) ↔ p % 4 = 1 := by
    rw [ZMod.χ₄_nat_eq_if_mod_four]
    constructor
    · intro h
      by_cases h2 : p % 2 = 0
      · norm_num [h2] at h
      · simp [h2] at h
        by_cases h1 : p % 4 = 1
        · exact h1
        · norm_num [h1] at h
    · intro h1
      have h2 : p % 2 = 1 := Nat.odd_of_mod_four_eq_one h1
      simp [h1, h2]
  change (↑(ZMod.χ₄ (p : ZMod 4)) : ℂ) = (1 : ℂ) ↔ p % 4 = 1
  rw [show ((1 : ℂ) = (↑(1 : ℤ) : ℂ)) by norm_num]
  exact_mod_cast help

/-- **Conductor-denominator law, full χ₄ form**: for an odd prime `p`,
some window denominator `1 + 4·a²` is divisible by `p` iff the
conductor-4 character takes the splitting value `χ₄(p) = 1`.  This is
`prime_divides_denominator_iff` re-expressed through the character, so
the `MPOperator` denominator family and the conductor-4 splitting rule
pin the same lattice. -/
lemma chi4_splits_iff_denominator (p : ℕ) (hp : p.Prime) (hp2 : p ≠ 2) :
    (∃ a : ℕ, p ∣ 1 + 4 * a ^ 2) ↔ χ₄ℂ (p : ZMod 4) = 1 := by
  rw [prime_divides_denominator_iff p hp hp2]
  exact (chi4_apply_eq_one_iff p).symm

/-! ### Parity (trivial-zero) law for `χ₄`, `χ₈`, `χ₈'` -/

/-- `χ₄` is **odd**: `χ₄(−1) = −1`. -/
lemma χ₄ℂ_odd : χ₄ℂ.Odd := by
  rw [DirichletCharacter.Odd]
  rw [show (-1 : ZMod 4) = 3 by decide, χ₄ℂ.apply_three]

/-- `χ₈` is **even**: `χ₈(−1) = 1`. -/
lemma χ₈ℂ_even : χ₈ℂ.Even := by
  rw [DirichletCharacter.Even]
  rw [show (-1 : ZMod 8) = 7 by decide]
  norm_num [χ₈ℂ]

/-- `χ₈'` is **odd**: `χ₈'(−1) = −1`. -/
lemma χ₈'ℂ_odd : χ₈'ℂ.Odd := by
  rw [DirichletCharacter.Odd]
  rw [show (-1 : ZMod 8) = 7 by decide]
  norm_num [χ₈'ℂ]

/-- **Trivial zeros** of `L(χ₄, s)` at all negative odd integers. -/
example (n : ℕ) : LFunction χ₄ℂ (-(2 * n) - 1) = 0 :=
  χ₄ℂ_odd.LFunction_neg_two_mul_nat_sub_one n

/-- **Trivial zeros** of `L(χ₈, s)` at all negative even integers. -/
example (n : ℕ) [NeZero n] : LFunction χ₈ℂ (-(2 * n)) = 0 :=
  χ₈ℂ_even.LFunction_neg_two_mul_nat n

/-- **Trivial zeros** of `L(χ₈', s)` at all negative odd integers. -/
example (n : ℕ) : LFunction χ₈'ℂ (-(2 * n) - 1) = 0 :=
  χ₈'ℂ_odd.LFunction_neg_two_mul_nat_sub_one n

/-! ### Gauss sum and root number of `χ₄` -/

@[simp] lemma chi4_stdAddChar_zero : ZMod.stdAddChar (0 : ZMod 4) = 1 := by
  change ZMod.stdAddChar ((0 : ℤ) : ZMod 4) = 1
  rw [ZMod.stdAddChar_coe (0 : ℤ)]
  norm_num [Complex.exp_zero]

@[simp] lemma chi4_stdAddChar_one : ZMod.stdAddChar (1 : ZMod 4) = Complex.I := by
  change ZMod.stdAddChar ((1 : ℤ) : ZMod 4) = Complex.I
  rw [ZMod.stdAddChar_coe (1 : ℤ)]
  have h₁ : (2 * π * Complex.I * (1 : ℤ) / ((4 : ℕ) : ℂ) : ℂ) = π / 2 * Complex.I := by ring_nf
  rw [h₁, Complex.exp_pi_div_two_mul_I]

@[simp] lemma chi4_stdAddChar_two : ZMod.stdAddChar (2 : ZMod 4) = -1 := by
  change ZMod.stdAddChar ((2 : ℤ) : ZMod 4) = -1
  rw [ZMod.stdAddChar_coe (2 : ℤ)]
  have h₂ : (2 * π * Complex.I * (2 : ℤ) / ((4 : ℕ) : ℂ) : ℂ) = π * Complex.I := by ring_nf
  rw [h₂, Complex.exp_pi_mul_I]

@[simp] lemma chi4_stdAddChar_three : ZMod.stdAddChar (3 : ZMod 4) = -Complex.I := by
  change ZMod.stdAddChar ((3 : ℤ) : ZMod 4) = -Complex.I
  rw [ZMod.stdAddChar_coe (3 : ℤ)]
  have h₃ : (2 * π * Complex.I * (3 : ℤ) / ((4 : ℕ) : ℂ) : ℂ) = -π / 2 * Complex.I + 2 * π * Complex.I := by ring_nf
  rw [h₃, Complex.exp_add, Complex.exp_neg_pi_div_two_mul_I, Complex.exp_two_pi_mul_I]
  norm_num

lemma zmod4_sum_fin (f : Fin 4 → ℂ) : (∑ i : Fin 4, f i) = f 0 + f 1 + f 2 + f 3 := by
  simp [Fin.sum_univ_four]

lemma sigma_zmod4 (f : ZMod 4 → ℂ) : (∑ k : ZMod 4, f k) = f 0 + f 1 + f 2 + f 3 := by
  calc
    (∑ k : ZMod 4, f k) = (∑ i : Fin 4, f i) := by rfl
    _ = f 0 + f 1 + f 2 + f 3 := by
      rw [zmod4_sum_fin (fun i : Fin 4 => f i)]
      rfl

/-- The `χ₄` **Gauss sum**: `∑ₐ χ₄(a) e^{2πia/4} = 2i`. -/
lemma chi4_gaussSum : gaussSum χ₄ℂ ZMod.stdAddChar = 2 * Complex.I := by
  calc
    gaussSum χ₄ℂ ZMod.stdAddChar = (∑ k : ZMod 4, χ₄ℂ k * ZMod.stdAddChar k) := by rfl
    _ = (χ₄ℂ 0 * ZMod.stdAddChar 0 + χ₄ℂ 1 * ZMod.stdAddChar 1 +
          χ₄ℂ 2 * ZMod.stdAddChar 2 + χ₄ℂ 3 * ZMod.stdAddChar 3) := by
      exact sigma_zmod4 (fun k : ZMod 4 => χ₄ℂ k * ZMod.stdAddChar k)
    _ = 2 * Complex.I := by
      rw [χ₄ℂ.apply_zero, chi4_stdAddChar_zero, χ₄ℂ.apply_one, chi4_stdAddChar_one,
        χ₄ℂ.apply_two, chi4_stdAddChar_two, χ₄ℂ.apply_three, chi4_stdAddChar_three]
      ring

set_option linter.style.haveILetI false in
/-- **`4 ^ (1/2) = 2`** — the principal complex square root appearing in
the root-number factor. -/
lemma chi4_sqrt : ((4 : ℕ) : ℂ) ^ (1 / 2 : ℂ) = 2 := by
  rw [Complex.cpow_def]
  have h40 : ((4 : ℕ) : ℂ) ≠ 0 := by norm_num
  rw [if_neg h40]
  rw [show ((4 : ℕ) : ℂ) = ((4 : ℝ) : ℂ) by norm_num]
  rw [(Complex.ofReal_log (by norm_num : (0 : ℝ) ≤ 4)).symm]
  have hrlog : Real.log 4 = 2 * Real.log 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num]
    rw [Real.log_pow]
    norm_num
  rw [hrlog]
  have hc : (↑(2 * Real.log 2 : ℝ) : ℂ) * (1 / 2 : ℂ) = (Real.log 2 : ℂ) := by
    push_cast
    ring
  rw [hc]
  have hlog2 : Complex.exp (↑(Real.log 2) : ℂ) = 2 := by
    rw [← Complex.ofReal_exp, Real.exp_log (by norm_num : (0 : ℝ) < 2)]
    norm_num
  rw [hlog2]

/-- **Root number of `χ₄`**: `rootNumber χ₄ = 1`. -/
lemma chi4_rootNumber : rootNumber χ₄ℂ = 1 := by
  rw [DirichletCharacter.rootNumber]
  rw [chi4_gaussSum]
  rw [if_neg]
  · rw [chi4_sqrt]
    norm_num [pow_one]
  · exact χ₄ℂ_odd.not_even

/-! ### Self-duality and the completed functional equation for `χ₄` -/

/-- `χ₄` is a **quadratic character**: its values lie in `{0, ±1}`. -/
lemma chi4_isQuadratic : χ₄ℂ.IsQuadratic := by
  exact (ZMod.isQuadratic_χ₄).comp (algebraMap ℤ ℂ)

/-- `χ₄` is **self-dual**: `χ₄⁻¹ = χ₄`. -/
lemma chi4_self_conjugate : χ₄ℂ⁻¹ = χ₄ℂ := by
  exact chi4_isQuadratic.inv

/-- `χ₄² = 1` (trivial character). -/
lemma chi4_sq_eq_one : χ₄ℂ ^ 2 = 1 := by
  exact chi4_isQuadratic.sq_eq_one

/-- Value at `−1`: `χ₄(−1) = −1`. -/
lemma chi4_neg_one : χ₄ℂ (-1) = (-1 : ℂ) := by
  rw [show (-1 : ZMod 4) = 3 by decide, χ₄ℂ.apply_three]

/-- Square of the Gauss sum: from `chi4_gaussSum` = `2i`, we get
`gaussSum(χ₄, stdAddChar)² = −4`. -/
lemma chi4_gaussSum_sq : (gaussSum χ₄ℂ ZMod.stdAddChar) ^ 2 = -(4 : ℂ) := by
  rw [chi4_gaussSum]
  have hi_sq : Complex.I ^ 2 = (-1 : ℂ) := Complex.I_sq
  rw [show (2 * Complex.I) ^ 2 = (2 : ℂ) ^ 2 * Complex.I ^ 2 from by ring]
  rw [hi_sq]
  norm_num

/-- The quadratic-character Gauss-sum identity `χ₄(−1)·4 = −4`,
consistent with `chi4_gaussSum`. -/
lemma chi4_gaussSum_sq_value : χ₄ℂ (-1) * (4 : ℂ) = -(4 : ℂ) := by
  rw [chi4_neg_one]
  norm_num

/-- The **self-dual functional equation** for `χ₄` (level `4`, root number
`1`): `Λ(χ₄, 1−s) = 4^(s−1/2) · Λ(χ₄, s)`. -/
lemma chi4_completedL_one_sub (s : ℂ) :
    DirichletCharacter.completedLFunction χ₄ℂ (1 - s) =
      (4 : ℂ) ^ (s - 1 / 2) * DirichletCharacter.completedLFunction χ₄ℂ s := by
  have h := χ₄ℂ.isPrimitive.completedLFunction_one_sub s
  rw [h, chi4_rootNumber, chi4_self_conjugate]
  simp

/-! ### Gauss sum and root number of `χ₈`, `χ₈'` -/

/-- `e^{πi/4} = (√2/2)·(1+i)`: the primitive eighth root of unity as a
complex number. -/
lemma exp_pi_div_four_mul_I : Complex.exp ((↑(Real.pi / 4 : ℝ)) * Complex.I) =
    (↑(Real.sqrt 2 / (2 : ℝ))) * (1 + Complex.I) := by
  rw [← Complex.cos_add_sin_I]
  rw [← Complex.ofReal_cos (Real.pi / 4), ← Complex.ofReal_sin (Real.pi / 4)]
  rw [show (Real.cos (Real.pi / 4) : ℝ) = Real.sqrt 2 / (2 : ℝ) by rw [Real.cos_pi_div_four]]
  rw [show (Real.sin (Real.pi / 4) : ℝ) = Real.sqrt 2 / (2 : ℝ) by rw [Real.sin_pi_div_four]]
  ring

@[simp] lemma chi8_stdAddChar_zero : ZMod.stdAddChar (0 : ZMod 8) = 1 := by
  change ZMod.stdAddChar ((0 : ℤ) : ZMod 8) = 1
  rw [ZMod.stdAddChar_coe (0 : ℤ)]
  norm_num [Complex.exp_zero]

@[simp] lemma chi8_stdAddChar_one : ZMod.stdAddChar (1 : ZMod 8) =
    (↑(Real.sqrt 2 / (2 : ℝ))) * (1 + Complex.I) := by
  change ZMod.stdAddChar ((1 : ℤ) : ZMod 8) =
    (↑(Real.sqrt 2 / (2 : ℝ))) * (1 + Complex.I)
  rw [ZMod.stdAddChar_coe (1 : ℤ)]
  have h₁ : (2 * π * Complex.I * (1 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
      (↑(Real.pi / 4 : ℝ)) * Complex.I := by
    have h₁' : (2 * π * Complex.I * (1 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
        (Real.pi : ℂ) / (4 : ℂ) * Complex.I := by ring_nf
    calc
      (2 * π * Complex.I * (1 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
          (Real.pi : ℂ) / (4 : ℂ) * Complex.I := h₁'
      _ = (↑(Real.pi / 4 : ℝ)) * Complex.I := by
        exact congrArg (fun t : ℂ => t * Complex.I)
          (Complex.ofReal_div Real.pi (4 : ℝ)).symm
  rw [h₁, exp_pi_div_four_mul_I]

set_option linter.style.haveILetI false in
@[simp] lemma chi8_stdAddChar_three : ZMod.stdAddChar (3 : ZMod 8) =
    (↑(Real.sqrt 2 / (2 : ℝ))) * (-1 + Complex.I) := by
  change ZMod.stdAddChar ((3 : ℤ) : ZMod 8) =
    (↑(Real.sqrt 2 / (2 : ℝ))) * (-1 + Complex.I)
  rw [ZMod.stdAddChar_coe (3 : ℤ)]
  have h₃ : (2 * π * Complex.I * (3 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
      (↑(Real.pi / 4 : ℝ)) * Complex.I + π / 2 * Complex.I := by
    have h₃' : (2 * π * Complex.I * (3 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
        (Real.pi : ℂ) / (4 : ℂ) * Complex.I + π / 2 * Complex.I := by ring_nf
    calc
      (2 * π * Complex.I * (3 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
          (Real.pi : ℂ) / (4 : ℂ) * Complex.I + π / 2 * Complex.I := h₃'
      _ = (↑(Real.pi / 4 : ℝ)) * Complex.I + π / 2 * Complex.I := by
        exact congrArg (fun t : ℂ => t + π / 2 * Complex.I) (
          congrArg (fun t : ℂ => t * Complex.I)
            (Complex.ofReal_div Real.pi (4 : ℝ)).symm)
  rw [h₃, Complex.exp_add, Complex.exp_pi_div_two_mul_I, exp_pi_div_four_mul_I]
  ring_nf
  rw [Complex.I_sq]
  ring

@[simp] lemma chi8_stdAddChar_five : ZMod.stdAddChar (5 : ZMod 8) =
    (↑(Real.sqrt 2 / (2 : ℝ))) * (-1 - Complex.I) := by
  change ZMod.stdAddChar ((5 : ℤ) : ZMod 8) =
    (↑(Real.sqrt 2 / (2 : ℝ))) * (-1 - Complex.I)
  rw [ZMod.stdAddChar_coe (5 : ℤ)]
  have h₅ : (2 * π * Complex.I * (5 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
      (↑(Real.pi / 4 : ℝ)) * Complex.I + π * Complex.I := by
    have h₅' : (2 * π * Complex.I * (5 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
        (Real.pi : ℂ) / (4 : ℂ) * Complex.I + π * Complex.I := by ring_nf
    calc
      (2 * π * Complex.I * (5 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
          (Real.pi : ℂ) / (4 : ℂ) * Complex.I + π * Complex.I := h₅'
      _ = (↑(Real.pi / 4 : ℝ)) * Complex.I + π * Complex.I := by
        exact congrArg (fun t : ℂ => t + π * Complex.I) (
          congrArg (fun t : ℂ => t * Complex.I)
            (Complex.ofReal_div Real.pi (4 : ℝ)).symm)
  rw [h₅, Complex.exp_add, Complex.exp_pi_mul_I, exp_pi_div_four_mul_I]
  ring

set_option linter.style.haveILetI false in
@[simp] lemma chi8_stdAddChar_seven : ZMod.stdAddChar (7 : ZMod 8) =
    (↑(Real.sqrt 2 / (2 : ℝ))) * (1 - Complex.I) := by
  change ZMod.stdAddChar ((7 : ℤ) : ZMod 8) =
    (↑(Real.sqrt 2 / (2 : ℝ))) * (1 - Complex.I)
  rw [ZMod.stdAddChar_coe (7 : ℤ)]
  have h₇ : (2 * π * Complex.I * (7 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
      (↑(Real.pi / 4 : ℝ)) * Complex.I +
        (-π / 2 * Complex.I + 2 * π * Complex.I) := by
    have h₇' : (2 * π * Complex.I * (7 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
        (Real.pi : ℂ) / (4 : ℂ) * Complex.I +
          (-π / 2 * Complex.I + 2 * π * Complex.I) := by ring_nf
    calc
      (2 * π * Complex.I * (7 : ℤ) / ((8 : ℕ) : ℂ) : ℂ) =
          (Real.pi : ℂ) / (4 : ℂ) * Complex.I +
            (-π / 2 * Complex.I + 2 * π * Complex.I) := h₇'
      _ = (↑(Real.pi / 4 : ℝ)) * Complex.I +
            (-π / 2 * Complex.I + 2 * π * Complex.I) := by
        exact congrArg (fun t : ℂ => t + (-π / 2 * Complex.I + 2 * π * Complex.I)) (
          congrArg (fun t : ℂ => t * Complex.I)
            (Complex.ofReal_div Real.pi (4 : ℝ)).symm)
  rw [h₇, Complex.exp_add, Complex.exp_add, Complex.exp_neg_pi_div_two_mul_I,
    Complex.exp_two_pi_mul_I, exp_pi_div_four_mul_I]
  ring_nf
  rw [Complex.I_sq]
  ring

lemma zmod8_sum_fin (f : Fin 8 → ℂ) :
    (∑ i : Fin 8, f i) = f 0 + (f 1 + (f 2 + (f 3 + (f 4 + (f 5 + (f 6 + f 7)))))) := by
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  simp

lemma sigma_zmod8 (f : ZMod 8 → ℂ) :
    (∑ k : ZMod 8, f k) = f 0 + (f 1 + (f 2 + (f 3 + (f 4 + (f 5 + (f 6 + f 7)))))) := by
  calc
    (∑ k : ZMod 8, f k) = (∑ i : Fin 8, f i) := by rfl
    _ = f 0 + (f 1 + (f 2 + (f 3 + (f 4 + (f 5 + (f 6 + f 7)))))) := by
      rw [zmod8_sum_fin (fun i : Fin 8 => f i)]
      rfl

set_option linter.style.haveILetI false in
/-- The `χ₈` **Gauss sum**: `∑ₐ χ₈(a) e^{2πia/8} = 2·√2`. -/
lemma chi8_gaussSum : gaussSum χ₈ℂ ZMod.stdAddChar = 2 * (Real.sqrt 2 : ℂ) := by
  calc
    gaussSum χ₈ℂ ZMod.stdAddChar = (∑ k : ZMod 8, χ₈ℂ k * ZMod.stdAddChar k) := by rfl
    _ = (χ₈ℂ 0 * ZMod.stdAddChar 0 + (χ₈ℂ 1 * ZMod.stdAddChar 1 +
          (χ₈ℂ 2 * ZMod.stdAddChar 2 + (χ₈ℂ 3 * ZMod.stdAddChar 3 +
          (χ₈ℂ 4 * ZMod.stdAddChar 4 + (χ₈ℂ 5 * ZMod.stdAddChar 5 +
          (χ₈ℂ 6 * ZMod.stdAddChar 6 + χ₈ℂ 7 * ZMod.stdAddChar 7))))))) := by
      exact sigma_zmod8 (fun k : ZMod 8 => χ₈ℂ k * ZMod.stdAddChar k)
    _ = 2 * (Real.sqrt 2 : ℂ) := by
      rw [χ₈ℂ.apply_zero, χ₈ℂ.apply_one, χ₈ℂ.apply_two, χ₈ℂ.apply_three,
        χ₈ℂ.apply_four, χ₈ℂ.apply_five, χ₈ℂ.apply_six, χ₈ℂ.apply_seven,
        chi8_stdAddChar_zero, chi8_stdAddChar_one, chi8_stdAddChar_three,
        chi8_stdAddChar_five, chi8_stdAddChar_seven]
      rw [Complex.ofReal_div]
      norm_num
      ring

set_option linter.style.haveILetI false in
/-- The `χ₈'` **Gauss sum**: `∑ₐ χ₈'(a) e^{2πia/8} = 2√2·i`. -/
lemma chi8'_gaussSum : gaussSum χ₈'ℂ ZMod.stdAddChar = 2 * (Real.sqrt 2 : ℂ) * Complex.I := by
  calc
    gaussSum χ₈'ℂ ZMod.stdAddChar = (∑ k : ZMod 8, χ₈'ℂ k * ZMod.stdAddChar k) := by rfl
    _ = (χ₈'ℂ 0 * ZMod.stdAddChar 0 + (χ₈'ℂ 1 * ZMod.stdAddChar 1 +
          (χ₈'ℂ 2 * ZMod.stdAddChar 2 + (χ₈'ℂ 3 * ZMod.stdAddChar 3 +
          (χ₈'ℂ 4 * ZMod.stdAddChar 4 + (χ₈'ℂ 5 * ZMod.stdAddChar 5 +
          (χ₈'ℂ 6 * ZMod.stdAddChar 6 + χ₈'ℂ 7 * ZMod.stdAddChar 7))))))) := by
      exact sigma_zmod8 (fun k : ZMod 8 => χ₈'ℂ k * ZMod.stdAddChar k)
    _ = 2 * (Real.sqrt 2 : ℂ) * Complex.I := by
      rw [χ₈'ℂ.apply_zero, χ₈'ℂ.apply_one, χ₈'ℂ.apply_two, χ₈'ℂ.apply_three,
        χ₈'ℂ.apply_four, χ₈'ℂ.apply_five, χ₈'ℂ.apply_six, χ₈'ℂ.apply_seven,
        chi8_stdAddChar_zero, chi8_stdAddChar_one, chi8_stdAddChar_three,
        chi8_stdAddChar_five, chi8_stdAddChar_seven]
      rw [Complex.ofReal_div]
      norm_num
      ring

set_option linter.style.haveILetI false in
/-- **`8 ^ (1/2) = 2·√2`** — the principal complex square root appearing in
the root-number factor. -/
lemma chi8_sqrt : ((8 : ℕ) : ℂ) ^ (1 / 2 : ℂ) = 2 * (Real.sqrt 2 : ℂ) := by
  rw [show ((8 : ℕ) : ℂ) = ((8 : ℝ) : ℂ) by norm_num]
  rw [show (1 / 2 : ℂ) = ((1 / 2 : ℝ) : ℂ) by norm_num]
  rw [← Complex.ofReal_cpow (by norm_num : (0 : ℝ) ≤ 8) (1 / 2 : ℝ)]
  rw [← Real.sqrt_eq_rpow (8 : ℝ)]
  have hr : Real.sqrt (8 : ℝ) = 2 * Real.sqrt 2 := by
    rw [show (8 : ℝ) = 4 * 2 by norm_num]
    rw [Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 4) (2 : ℝ)]
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num]
    rw [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ 2)]
  rw [hr]
  rw [Complex.ofReal_mul]
  norm_num

/-- **Root number of `χ₈`**: `rootNumber χ₈ = 1`. -/
lemma chi8_rootNumber : rootNumber χ₈ℂ = 1 := by
  rw [DirichletCharacter.rootNumber]
  rw [chi8_gaussSum]
  rw [if_pos χ₈ℂ_even]
  rw [chi8_sqrt]
  norm_num [pow_zero]

/-- **Root number of `χ₈'`**: `rootNumber χ₈' = 1`. -/
lemma chi8'_rootNumber : rootNumber χ₈'ℂ = 1 := by
  rw [DirichletCharacter.rootNumber]
  rw [chi8'_gaussSum]
  rw [if_neg]
  · rw [chi8_sqrt]
    norm_num [pow_one]
  · exact χ₈'ℂ_odd.not_even

/-! ### Self-duality and the completed functional equations for `χ₈`, `χ₈'` -/

/-- `χ₈` is a **quadratic character**: its values lie in `{0, ±1}`. -/
lemma chi8_isQuadratic : χ₈ℂ.IsQuadratic := by
  exact (ZMod.isQuadratic_χ₈).comp (algebraMap ℤ ℂ)

/-- `χ₈` is **self-dual**: `χ₈⁻¹ = χ₈`. -/
lemma chi8_self_conjugate : χ₈ℂ⁻¹ = χ₈ℂ := by
  exact chi8_isQuadratic.inv

/-- `χ₈² = 1` (trivial character). -/
lemma chi8_sq_eq_one : χ₈ℂ ^ 2 = 1 := by
  exact chi8_isQuadratic.sq_eq_one

/-- `χ₈'` is a **quadratic character**: its values lie in `{0, ±1}`. -/
lemma chi8'_isQuadratic : χ₈'ℂ.IsQuadratic := by
  exact (ZMod.isQuadratic_χ₈').comp (algebraMap ℤ ℂ)

/-- `χ₈'` is **self-dual**: `χ₈'⁻¹ = χ₈'`. -/
lemma chi8'_self_conjugate : χ₈'ℂ⁻¹ = χ₈'ℂ := by
  exact chi8'_isQuadratic.inv

/-- `χ₈'² = 1` (trivial character). -/
lemma chi8'_sq_eq_one : χ₈'ℂ ^ 2 = 1 := by
  exact chi8'_isQuadratic.sq_eq_one

/-- Value at `−1`: `χ₈(−1) = 1` (`χ₈` even). -/
lemma chi8_neg_one : χ₈ℂ (-1) = (1 : ℂ) := by
  rw [show (-1 : ZMod 8) = 7 by decide, χ₈ℂ.apply_seven]

/-- Value at `−1`: `χ₈'(−1) = −1` (`χ₈'` odd). -/
lemma chi8'_neg_one : χ₈'ℂ (-1) = (-1 : ℂ) := by
  rw [show (-1 : ZMod 8) = 7 by decide, χ₈'ℂ.apply_seven]

set_option linter.style.haveILetI false in
/-- Square of the Gauss sum: from `chi8_gaussSum` = `2√2`, we get
`gaussSum(χ₈, stdAddChar)² = 8`. -/
lemma chi8_gaussSum_sq : (gaussSum χ₈ℂ ZMod.stdAddChar) ^ 2 = (8 : ℂ) := by
  rw [chi8_gaussSum]
  have hs : (Real.sqrt 2 : ℂ) ^ 2 = (2 : ℂ) := by
    rw [← Complex.ofReal_pow]
    rw [show (Real.sqrt 2 ^ 2 : ℝ) = 2 by
      rw [pow_two, Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 2)]]
    rfl
  rw [show (2 * (Real.sqrt 2 : ℂ)) ^ 2 = (2 : ℂ) ^ 2 * (Real.sqrt 2 : ℂ) ^ 2 from by ring]
  rw [hs]
  norm_num

/-- The quadratic-character Gauss-sum identity `χ₈(−1)·8 = 8`,
consistent with `chi8_gaussSum`. -/
lemma chi8_gaussSum_sq_value : χ₈ℂ (-1) * (8 : ℂ) = (8 : ℂ) := by
  rw [chi8_neg_one]
  norm_num

/-- The quadratic-character Gauss-sum identity `χ₈'(−1)·8 = −8`,
consistent with `chi8'_gaussSum`. -/
lemma chi8'_gaussSum_sq_value : χ₈'ℂ (-1) * (8 : ℂ) = -(8 : ℂ) := by
  rw [chi8'_neg_one]
  norm_num

/-- The **self-dual functional equation** for `χ₈` (level `8`, root number
`1`): `Λ(χ₈, 1−s) = 8^(s−1/2) · Λ(χ₈, s)`. -/
lemma chi8_completedL_one_sub (s : ℂ) :
    DirichletCharacter.completedLFunction χ₈ℂ (1 - s) =
      (8 : ℂ) ^ (s - 1 / 2) * DirichletCharacter.completedLFunction χ₈ℂ s := by
  have h := χ₈ℂ.isPrimitive.completedLFunction_one_sub s
  rw [h, chi8_rootNumber, chi8_self_conjugate]
  simp

/-- The **self-dual functional equation** for `χ₈'` (level `8`, root number
`1`): `Λ(χ₈', 1−s) = 8^(s−1/2) · Λ(χ₈', s)`. -/
lemma chi8'_completedL_one_sub (s : ℂ) :
    DirichletCharacter.completedLFunction χ₈'ℂ (1 - s) =
      (8 : ℂ) ^ (s - 1 / 2) * DirichletCharacter.completedLFunction χ₈'ℂ s := by
  have h := χ₈'ℂ.isPrimitive.completedLFunction_one_sub s
  rw [h, chi8'_rootNumber, chi8'_self_conjugate]
  simp

namespace ZMod

/-- The nontrivial quadratic character on `ZMod 3` — `χ₃` (values in `ℤ`,
mirroring mathlib's `χ₄`). -/
@[simps]
def χ₃ : MulChar (ZMod 3) ℤ where
  toFun a :=
    match a with
    | 0 => 0
    | 1 => 1
    | 2 => -1
  map_one' := rfl
  map_mul' := by decide
  map_nonunit' := by decide

/-- `χ₃` takes values in `{0, 1, -1}` -/
theorem isQuadratic_χ₃ : χ₃.IsQuadratic := by
  unfold MulChar.IsQuadratic
  decide

end ZMod

/-- `χ₃` (the mod-3 quadratic character) lifted to `ℂ`. -/
def χ₃ℂ : DirichletCharacter ℂ 3 := ZMod.χ₃.ringHomComp (algebraMap ℤ ℂ)

namespace χ₃ℂ

lemma apply_zero : χ₃ℂ (0 : ZMod 3) = 0 := by norm_num [χ₃ℂ]
lemma apply_one : χ₃ℂ (1 : ZMod 3) = 1 := by norm_num [χ₃ℂ]
lemma apply_two : χ₃ℂ (2 : ZMod 3) = -1 := by norm_num [χ₃ℂ]

lemma ne_char_one : χ₃ℂ ≠ 1 := by
  intro h
  have this := congrArg (fun ψ : DirichletCharacter ℂ 3 ↦ ψ (2 : ZMod 3)) h
  change χ₃ℂ 2 = (1 : DirichletCharacter ℂ 3) 2 at this
  have h2 : (1 : DirichletCharacter ℂ 3) 2 = (1 : ℂ) := by
    have h2u : IsUnit (2 : ZMod 3) := by
      exact (ZMod.isUnit_iff_coprime 2 3).mpr (by norm_num)
    exact MulChar.one_apply h2u
  rw [apply_two, h2] at this
  norm_num at this

/-- The conductor of `χ₃` is `3`. -/
lemma conductor_eq_three : χ₃ℂ.conductor = 3 := by
  apply le_antisymm
  · have hd := χ₃ℂ.conductor_dvd_level
    exact Nat.le_of_dvd (by norm_num) hd
  · by_contra h
    have hle : χ₃ℂ.conductor < 3 := lt_of_not_ge h
    interval_cases hc : χ₃ℂ.conductor
    · exfalso
      exact χ₃ℂ.conductor_ne_zero hc
    · have hχ : χ₃ℂ = 1 := (DirichletCharacter.eq_one_iff_conductor_eq_one).mpr hc
      exact ne_char_one hχ
    · have : (2 : ℕ) ∣ 3 := by simpa [hc] using χ₃ℂ.conductor_dvd_level
      norm_num at this

/-- `χ₃` is a **primitive** character (level equals conductor). -/
lemma isPrimitive : χ₃ℂ.IsPrimitive := by
  rw [DirichletCharacter.IsPrimitive]
  exact conductor_eq_three

end χ₃ℂ

/-- `χ₃` is **odd**: `χ₃(−1) = −1`. -/
lemma χ₃ℂ_odd : χ₃ℂ.Odd := by
  rw [DirichletCharacter.Odd]
  rw [show (-1 : ZMod 3) = 2 by decide]
  norm_num [χ₃ℂ]

/-! ### Gauss sum and root number of `χ₃` -/

/-- `e^{2πi/3} = −1/2 + i·(√3/2)`: the primitive cube root of unity. -/
lemma exp_two_pi_div_three_mul_I : Complex.exp ((↑(2 * Real.pi / 3 : ℝ)) * Complex.I) =
    (↑(Real.sqrt 3 / (2 : ℝ))) * Complex.I - (1 / 2 : ℂ) := by
  rw [← Complex.cos_add_sin_I]
  rw [← Complex.ofReal_cos (2 * Real.pi / 3), ← Complex.ofReal_sin (2 * Real.pi / 3)]
  rw [show (Real.cos (2 * Real.pi / 3) : ℝ) = -(1 / 2) by
    rw [show 2 * Real.pi / 3 = Real.pi - Real.pi / 3 by ring]
    rw [Real.cos_pi_sub, Real.cos_pi_div_three]]
  rw [show (Real.sin (2 * Real.pi / 3) : ℝ) = Real.sqrt 3 / (2 : ℝ) by
    rw [show 2 * Real.pi / 3 = Real.pi - Real.pi / 3 by ring]
    rw [Real.sin_pi_sub, Real.sin_pi_div_three]]
  norm_num
  ring

/-- `e^{4πi/3} = −1/2 − i·(√3/2)`: the square of the primitive cube root. -/
lemma exp_four_pi_div_three_mul_I : Complex.exp ((↑(4 * Real.pi / 3 : ℝ)) * Complex.I) =
    (↑(Real.sqrt 3 / (2 : ℝ))) * (-Complex.I) - (1 / 2 : ℂ) := by
  rw [← Complex.cos_add_sin_I]
  rw [← Complex.ofReal_cos (4 * Real.pi / 3), ← Complex.ofReal_sin (4 * Real.pi / 3)]
  rw [show (Real.cos (4 * Real.pi / 3) : ℝ) = -(1 / 2) by
    rw [show 4 * Real.pi / 3 = Real.pi / 3 + Real.pi by ring]
    rw [Real.cos_add_pi, Real.cos_pi_div_three]]
  rw [show (Real.sin (4 * Real.pi / 3) : ℝ) = -(Real.sqrt 3 / (2 : ℝ)) by
    rw [show 4 * Real.pi / 3 = Real.pi / 3 + Real.pi by ring]
    rw [Real.sin_add_pi, Real.sin_pi_div_three]]
  norm_num
  ring

/-- Coefficient bridge: `2·(π/3) = 2π/3` as complex cast. -/
lemma hen2 : (2 : ℂ) * (↑(Real.pi / (3 : ℝ)) : ℂ) = (↑(2 * Real.pi / (3 : ℝ)) : ℂ) := by
  calc
    (2 : ℂ) * (↑(Real.pi / (3 : ℝ)) : ℂ)
        = (↑(2 : ℝ) : ℂ) * (↑(Real.pi / (3 : ℝ)) : ℂ) := by norm_num
    _ = (↑((2 : ℝ) * (Real.pi / (3 : ℝ))) : ℂ) := by rw [Complex.ofReal_mul]
    _ = (↑(2 * Real.pi / (3 : ℝ)) : ℂ) := by
      exact congrArg (algebraMap ℝ ℂ)
        (show (2 : ℝ) * (Real.pi / (3 : ℝ)) = 2 * Real.pi / (3 : ℝ) by ring)

/-- Coefficient bridge: `4·(π/3) = 4π/3` as complex cast. -/
lemma hen4 : (4 : ℂ) * (↑(Real.pi / (3 : ℝ)) : ℂ) = (↑(4 * Real.pi / (3 : ℝ)) : ℂ) := by
  calc
    (4 : ℂ) * (↑(Real.pi / (3 : ℝ)) : ℂ)
        = (↑(4 : ℝ) : ℂ) * (↑(Real.pi / (3 : ℝ)) : ℂ) := by norm_num
    _ = (↑((4 : ℝ) * (Real.pi / (3 : ℝ))) : ℂ) := by rw [Complex.ofReal_mul]
    _ = (↑(4 * Real.pi / (3 : ℝ)) : ℂ) := by
      exact congrArg (algebraMap ℝ ℂ)
        (show (4 : ℝ) * (Real.pi / (3 : ℝ)) = 4 * Real.pi / (3 : ℝ) by ring)

@[simp] lemma chi3_stdAddChar_zero : ZMod.stdAddChar (0 : ZMod 3) = 1 := by
  change ZMod.stdAddChar ((0 : ℤ) : ZMod 3) = 1
  rw [ZMod.stdAddChar_coe (0 : ℤ)]
  norm_num [Complex.exp_zero]

@[simp] lemma chi3_stdAddChar_one : ZMod.stdAddChar (1 : ZMod 3) =
    (↑(Real.sqrt 3 / (2 : ℝ))) * Complex.I - (1 / 2 : ℂ) := by
  change ZMod.stdAddChar ((1 : ℤ) : ZMod 3) =
    (↑(Real.sqrt 3 / (2 : ℝ))) * Complex.I - (1 / 2 : ℂ)
  rw [ZMod.stdAddChar_coe (1 : ℤ)]
  have h₁ : (2 * π * Complex.I * (1 : ℤ) / ((3 : ℕ) : ℂ) : ℂ) =
      (↑(2 * Real.pi / (3 : ℝ))) * Complex.I := by
    have h₁' : (2 * π * Complex.I * (1 : ℤ) / ((3 : ℕ) : ℂ) : ℂ) =
        (Real.pi : ℂ) / (3 : ℂ) * (2 : ℂ) * Complex.I := by ring_nf
    calc
      (2 * π * Complex.I * (1 : ℤ) / ((3 : ℕ) : ℂ) : ℂ) =
          (Real.pi : ℂ) / (3 : ℂ) * (2 : ℂ) * Complex.I := h₁'
      _ = (↑(Real.pi / (3 : ℝ)) : ℂ) * (2 : ℂ) * Complex.I := by
        exact congrArg (fun t : ℂ => t * (2 : ℂ) * Complex.I)
          (Complex.ofReal_div Real.pi (3 : ℝ)).symm
      _ = (2 : ℂ) * (↑(Real.pi / (3 : ℝ)) : ℂ) * Complex.I := by ring
      _ = (↑(2 * Real.pi / (3 : ℝ))) * Complex.I := by
        rw [hen2]
  rw [h₁, exp_two_pi_div_three_mul_I]

@[simp] lemma chi3_stdAddChar_two : ZMod.stdAddChar (2 : ZMod 3) =
    (↑(Real.sqrt 3 / (2 : ℝ))) * (-Complex.I) - (1 / 2 : ℂ) := by
  change ZMod.stdAddChar ((2 : ℤ) : ZMod 3) =
    (↑(Real.sqrt 3 / (2 : ℝ))) * (-Complex.I) - (1 / 2 : ℂ)
  rw [ZMod.stdAddChar_coe (2 : ℤ)]
  have h₂ : (2 * π * Complex.I * (2 : ℤ) / ((3 : ℕ) : ℂ) : ℂ) =
      (↑(4 * Real.pi / (3 : ℝ))) * Complex.I := by
    have h₂' : (2 * π * Complex.I * (2 : ℤ) / ((3 : ℕ) : ℂ) : ℂ) =
        (Real.pi : ℂ) / (3 : ℂ) * (4 : ℂ) * Complex.I := by ring_nf
    calc
      (2 * π * Complex.I * (2 : ℤ) / ((3 : ℕ) : ℂ) : ℂ) =
          (Real.pi : ℂ) / (3 : ℂ) * (4 : ℂ) * Complex.I := h₂'
      _ = (↑(Real.pi / (3 : ℝ)) : ℂ) * (4 : ℂ) * Complex.I := by
        exact congrArg (fun t : ℂ => t * (4 : ℂ) * Complex.I)
          (Complex.ofReal_div Real.pi (3 : ℝ)).symm
      _ = (4 : ℂ) * (↑(Real.pi / (3 : ℝ)) : ℂ) * Complex.I := by ring
      _ = (↑(4 * Real.pi / (3 : ℝ))) * Complex.I := by
        rw [hen4]
  rw [h₂, exp_four_pi_div_three_mul_I]

lemma zmod3_sum_fin (f : Fin 3 → ℂ) :
    (∑ i : Fin 3, f i) = f 0 + (f 1 + f 2) := by
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  rw [Fin.sum_univ_succ]
  simp

lemma sigma_zmod3 (f : ZMod 3 → ℂ) :
    (∑ k : ZMod 3, f k) = f 0 + (f 1 + f 2) := by
  calc
    (∑ k : ZMod 3, f k) = (∑ i : Fin 3, f i) := by rfl
    _ = f 0 + (f 1 + f 2) := by
      rw [zmod3_sum_fin (fun i : Fin 3 => f i)]
      rfl

/-- The `χ₃` **Gauss sum**: `∑ₐ χ₃(a) e^{2πia/3} = i·√3`. -/
lemma chi3_gaussSum : gaussSum χ₃ℂ ZMod.stdAddChar = (Real.sqrt 3 : ℂ) * Complex.I := by
  calc
    gaussSum χ₃ℂ ZMod.stdAddChar = (∑ k : ZMod 3, χ₃ℂ k * ZMod.stdAddChar k) := by rfl
    _ = (χ₃ℂ 0 * ZMod.stdAddChar 0 + (χ₃ℂ 1 * ZMod.stdAddChar 1 +
          χ₃ℂ 2 * ZMod.stdAddChar 2)) := by
      exact sigma_zmod3 (fun k : ZMod 3 => χ₃ℂ k * ZMod.stdAddChar k)
    _ = (Real.sqrt 3 : ℂ) * Complex.I := by
      rw [χ₃ℂ.apply_zero, chi3_stdAddChar_zero, χ₃ℂ.apply_one, chi3_stdAddChar_one,
        χ₃ℂ.apply_two, chi3_stdAddChar_two]
      rw [Complex.ofReal_div]
      norm_num
      ring

/-- **`3 ^ (1/2) = √3`** — the principal complex square root in the
root-number factor. -/
lemma chi3_sqrt : ((3 : ℕ) : ℂ) ^ (1 / 2 : ℂ) = (Real.sqrt 3 : ℂ) := by
  rw [show ((3 : ℕ) : ℂ) = ((3 : ℝ) : ℂ) by norm_num]
  rw [show (1 / 2 : ℂ) = ((1 / 2 : ℝ) : ℂ) by norm_num]
  rw [← Complex.ofReal_cpow (by norm_num : (0 : ℝ) ≤ 3) (1 / 2 : ℝ)]
  rw [← Real.sqrt_eq_rpow (3 : ℝ)]

/-- **Root number of `χ₃`**: `rootNumber χ₃ = 1`. -/
lemma chi3_rootNumber : rootNumber χ₃ℂ = 1 := by
  rw [DirichletCharacter.rootNumber]
  rw [chi3_gaussSum]
  rw [if_neg]
  · rw [chi3_sqrt]
    norm_num [pow_one]
  · exact χ₃ℂ_odd.not_even

/-! ### Self-duality and the completed functional equation for `χ₃` -/

/-- `χ₃` is a **quadratic character**: its values lie in `{0, ±1}`. -/
lemma chi3_isQuadratic : χ₃ℂ.IsQuadratic := by
  exact (ZMod.isQuadratic_χ₃).comp (algebraMap ℤ ℂ)

/-- `χ₃` is **self-dual**: `χ₃⁻¹ = χ₃`. -/
lemma chi3_self_conjugate : χ₃ℂ⁻¹ = χ₃ℂ := by
  exact chi3_isQuadratic.inv

/-- `χ₃² = 1` (trivial character). -/
lemma chi3_sq_eq_one : χ₃ℂ ^ 2 = 1 := by
  exact chi3_isQuadratic.sq_eq_one

/-- Value at `−1`: `χ₃(−1) = −1` (`χ₃` odd). -/
lemma chi3_neg_one : χ₃ℂ (-1) = (-1 : ℂ) := by
  rw [show (-1 : ZMod 3) = 2 by decide, χ₃ℂ.apply_two]

/-- The quadratic-character Gauss-sum identity `χ₃(−1)·3 = −3`,
consistent with `chi3_gaussSum`. -/
lemma chi3_gaussSum_sq_value : χ₃ℂ (-1) * (3 : ℂ) = -(3 : ℂ) := by
  rw [chi3_neg_one]
  norm_num

/-- Square of the Gauss sum: from `chi3_gaussSum` = `i·√3`, we get
`gaussSum(χ₃, stdAddChar)² = −3`. -/
lemma chi3_gaussSum_sq : (gaussSum χ₃ℂ ZMod.stdAddChar) ^ 2 = -(3 : ℂ) := by
  rw [chi3_gaussSum]
  ring_nf
  rw [Complex.I_sq]
  rw [← Complex.ofReal_pow]
  norm_num [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)]

/-- The **self-dual functional equation** for `χ₃` (level `3`, root number
`1`): `Λ(χ₃, 1−s) = 3^(s−1/2) · Λ(χ₃, s)`. -/
lemma chi3_completedL_one_sub (s : ℂ) :
    DirichletCharacter.completedLFunction χ₃ℂ (1 - s) =
      (3 : ℂ) ^ (s - 1 / 2) * DirichletCharacter.completedLFunction χ₃ℂ s := by
  have h := χ₃ℂ.isPrimitive.completedLFunction_one_sub s
  rw [h, chi3_rootNumber, chi3_self_conjugate]
  simp

/-! ### General quadratic-character lemma layer -/

/-- A quadratic character is **self-dual**: `χ⁻¹ = χ`. -/
lemma self_conjugate_of_quadratic (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N)
    (hχ₂ : χ.IsQuadratic) : χ⁻¹ = χ :=
  hχ₂.inv

/-- `(N ^ (1/2))² = N` in `ℂ`, for a nonzero integer modulus `N`. -/
lemma cpow_half_sq (N : ℕ) [NeZero N] : ((N : ℂ) ^ (1 / 2 : ℂ)) ^ 2 = (N : ℂ) := by
  have h12 : (1 / 2 : ℂ) = (2 : ℂ)⁻¹ := by norm_num
  rw [h12]
  exact Complex.cpow_nat_inv_pow (x := (N : ℂ)) (n := 2) (by decide)

/-- The **quadratic resolvent identity over `𝔽ₚ`**: for a nontrivial
quadratic character `χ` of prime conductor `p`,
`gaussSum(χ, stdAddChar)² = χ(−1)·p`.  This is mathlib's `GaussSum.gaussSum_sq`
instantiated at `R = ZMod p`, `ψ = stdAddChar` — the one law that makes
every prime-conductor quadratic register automatic, up to the explicit
evaluation of the Gauss sum. -/
lemma gaussSum_sq_of_quadratic (p : ℕ) [Fact p.Prime] [NeZero p]
    (χ : DirichletCharacter ℂ p) (hχ₁ : χ ≠ 1) (hχ₂ : χ.IsQuadratic) :
    gaussSum χ ZMod.stdAddChar ^ 2 = χ (-1) * (p : ℂ) := by
  have hψ : (ZMod.stdAddChar (N := p)).IsPrimitive := ZMod.isPrimitive_stdAddChar p
  have hcard : (Fintype.card (ZMod p) : ℂ) = (p : ℂ) := by
    exact_mod_cast ZMod.card p
  simpa [hcard] using
    (gaussSum_sq (R := ZMod p) (R' := ℂ) (χ := χ) (ψ := ZMod.stdAddChar) hχ₁ hχ₂ hψ)

set_option maxHeartbeats 800000 in
/-- The **root number of a nontrivial quadratic character has square `1`**:
`rootNumber χ ∈ {±1}`.  The sign — for the quadratic registers `χ₄`, `χ₈`,
`χ₈'`, `χ₃` it is `+1` — is pinned by the explicit Gauss-sum evaluations
above. -/
lemma rootNumber_sq_of_quadratic (p : ℕ) [Fact p.Prime] [NeZero p]
    (χ : DirichletCharacter ℂ p) (hχ₁ : χ ≠ 1) (hχ₂ : χ.IsQuadratic) :
    rootNumber χ ^ 2 = 1 := by
  classical
  rw [DirichletCharacter.rootNumber]
  have hG := gaussSum_sq_of_quadratic p χ hχ₁ hχ₂
  have hS : ((p : ℂ) ^ (1 / 2 : ℂ)) ^ 2 = (p : ℂ) := cpow_half_sq p
  have hψ : (ZMod.stdAddChar (N := p)).IsPrimitive := ZMod.isPrimitive_stdAddChar p
  have hS0 : (p : ℂ) ^ (1 / 2 : ℂ) ≠ 0 := by
    intro hs
    have hs2 : (p : ℂ) = 0 := by
      calc
        (p : ℂ) = ((p : ℂ) ^ (1 / 2 : ℂ)) ^ 2 := hS.symm
        _ = 0 := by
          rw [hs]
          norm_num
    exact (NeZero.ne p) (Nat.cast_eq_zero.mp hs2)
  have hG0 : gaussSum χ ZMod.stdAddChar ≠ 0 :=
    gaussSum_ne_zero_of_nontrivial (h := by
      change (Fintype.card (ZMod p) : ℂ) ≠ 0
      rw [ZMod.card]
      exact_mod_cast (NeZero.ne p)) hχ₁ hψ
  by_cases hE : χ.Even
  · have hneg : χ (-1) = (1 : ℂ) := by simpa [DirichletCharacter.Even] using hE
    have hSq : gaussSum χ ZMod.stdAddChar ^ 2 =
        (Complex.I ^ (if χ.Even then 0 else 1)) ^ 2 * ((p : ℂ) ^ (1 / 2 : ℂ)) ^ 2 := by
      calc
        gaussSum χ ZMod.stdAddChar ^ 2 = (p : ℂ) := by rw [hG, hneg]; norm_num
        _ = (1 : ℂ) * ((p : ℂ) ^ (1 / 2 : ℂ)) ^ 2 := by rw [hS]; norm_num
        _ = (Complex.I ^ 0) ^ 2 * ((p : ℂ) ^ (1 / 2 : ℂ)) ^ 2 := by norm_num
        _ = (Complex.I ^ (if χ.Even then 0 else 1)) ^ 2 * ((p : ℂ) ^ (1 / 2 : ℂ)) ^ 2 := by
          rw [if_pos hE]
    rw [div_div, div_pow, mul_pow, ← hSq]
    exact div_self (pow_ne_zero 2 hG0)
  · have hO : χ.Odd := χ.even_or_odd.resolve_left hE
    have hneg : χ (-1) = (-1 : ℂ) := by simpa [DirichletCharacter.Odd] using hO
    have hSq : gaussSum χ ZMod.stdAddChar ^ 2 =
        (Complex.I ^ (if χ.Even then 0 else 1)) ^ 2 * ((p : ℂ) ^ (1 / 2 : ℂ)) ^ 2 := by
      calc
        gaussSum χ ZMod.stdAddChar ^ 2 = -((p : ℂ)) := by rw [hG, hneg]; norm_num
        _ = (Complex.I ^ 1) ^ 2 * ((p : ℂ) ^ (1 / 2 : ℂ)) ^ 2 := by
          rw [hS]
          rw [pow_one]
          rw [Complex.I_sq]
          norm_num
        _ = (Complex.I ^ (if χ.Even then 0 else 1)) ^ 2 * ((p : ℂ) ^ (1 / 2 : ℂ)) ^ 2 := by
          rw [if_neg hE]
    rw [div_div, div_pow, mul_pow, ← hSq]
    exact div_self (pow_ne_zero 2 hG0)

/-- The **self-dual functional equation** for a primitive quadratic
character: `Λ(χ, 1−s) = N^(s−1/2) · rootNumber χ · Λ(χ, s)` — the one
statement that, together with the root number, specializes to each
quadratic register. -/
lemma completedL_one_sub_of_quadratic (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N)
    (hprim : χ.IsPrimitive) (hquad : χ.IsQuadratic) (s : ℂ) :
    completedLFunction χ (1 - s) = (N : ℂ) ^ (s - 1 / 2) * rootNumber χ * completedLFunction χ s := by
  rw [hprim.completedLFunction_one_sub s]
  rw [hquad.inv]

/-- Coverage of the general layer over the `χ₃` prime register: the
resolvent identity, the epsilon-square law, self-duality, and the
self-dual functional equation. -/
example : gaussSum χ₃ℂ ZMod.stdAddChar ^ 2 = χ₃ℂ (-1) * (3 : ℂ) :=
  gaussSum_sq_of_quadratic 3 χ₃ℂ χ₃ℂ.ne_char_one chi3_isQuadratic

example : rootNumber χ₃ℂ ^ 2 = 1 :=
  rootNumber_sq_of_quadratic 3 χ₃ℂ χ₃ℂ.ne_char_one chi3_isQuadratic

example : χ₃ℂ⁻¹ = χ₃ℂ :=
  self_conjugate_of_quadratic 3 χ₃ℂ chi3_isQuadratic

example (s : ℂ) :
    completedLFunction χ₃ℂ (1 - s) = (3 : ℂ) ^ (s - 1 / 2) * rootNumber χ₃ℂ * completedLFunction χ₃ℂ s :=
  completedL_one_sub_of_quadratic 3 χ₃ℂ χ₃ℂ.isPrimitive chi3_isQuadratic s

/-- Coverage on the composite-modulus registers: self-duality of `χ₄`,
`χ₈`, `χ₈'` is a case of the layer (`χ² = 1`, hence `χ⁻¹ = χ`); their
Gauss sums are evaluated directly above. -/
example : χ₄ℂ⁻¹ = χ₄ℂ := self_conjugate_of_quadratic 4 χ₄ℂ chi4_isQuadratic

example : χ₈ℂ⁻¹ = χ₈ℂ := self_conjugate_of_quadratic 8 χ₈ℂ chi8_isQuadratic

example : χ₈'ℂ⁻¹ = χ₈'ℂ := self_conjugate_of_quadratic 8 χ₈'ℂ chi8'_isQuadratic

/-! ### Nonvanishing at `s = 1` (Dirichlet prime-theorem engine) -/

/-- **`L(1, χ₄) ≠ 0`** — the nonvanishing law that underlies Dirichlet's
theorem on primes in arithmetic progressions, specialized to `χ₄`
(`LFunction_apply_one_ne_zero`, mathlib). -/
lemma χ₄𝕃_ne_zero_one : LFunction χ₄ℂ 1 ≠ 0 :=
  LFunction_apply_one_ne_zero χ₄ℂ.ne_char_one

/-- **`L(1, χ₈) ≠ 0`** — nonvanishing for `χ₈`. -/
lemma χ₈𝕃_ne_zero_one : LFunction χ₈ℂ 1 ≠ 0 :=
  LFunction_apply_one_ne_zero χ₈ℂ.ne_char_one

/-- **`L(1, χ₈') ≠ 0`** — nonvanishing for `χ₈'`. -/
lemma χ₈'𝕃_ne_zero_one : LFunction χ₈'ℂ 1 ≠ 0 :=
  LFunction_apply_one_ne_zero χ₈'ℂ.ne_char_one

/-- **`L(1, χ₃) ≠ 0`** — nonvanishing for `χ₃`. -/
lemma χ₃𝕃_ne_zero_one : LFunction χ₃ℂ 1 ≠ 0 :=
  LFunction_apply_one_ne_zero χ₃ℂ.ne_char_one

/-- **Nonvanishing on the critical-strip boundary**: for every character,
`L(χ, s) ≠ 0` whenever `Re s ≥ 1` and `χ ≠ 1` (or `s ≠ 1`) — the
`LFunction_ne_zero_of_one_le_re` law of mathlib, stated here for the
concrete `χ₄`, `χ₈`, `χ₈'`. -/
example {s : ℂ} (hs : 1 ≤ s.re) : LFunction χ₄ℂ s ≠ 0 :=
  LFunction_ne_zero_of_one_le_re (χ := χ₄ℂ) (by
    left
    exact χ₄ℂ.ne_char_one) hs

example {s : ℂ} (hs : 1 ≤ s.re) : LFunction χ₈ℂ s ≠ 0 :=
  LFunction_ne_zero_of_one_le_re (χ := χ₈ℂ) (by
    left
    exact χ₈ℂ.ne_char_one) hs

example {s : ℂ} (hs : 1 ≤ s.re) : LFunction χ₈'ℂ s ≠ 0 :=
  LFunction_ne_zero_of_one_le_re (χ := χ₈'ℂ) (by
    left
    exact χ₈'ℂ.ne_char_one) hs

/-- **Riemann ζ has no zeros on `Re s ≥ 1`** (mathlib
`riemannZeta_ne_zero_of_one_le_re`), the boundary of the prime-number
theorem. -/
lemma riemann_no_zeros_on_boundary (s : ℂ) (hs : 1 ≤ s.re) : riemannZeta s ≠ 0 :=
  riemannZeta_ne_zero_of_one_le_re hs

/-! ### L-function trivial zeros at negative integers

The completed functional equation has a Γ-factor whose poles force
`L(χ, s) = 0` at negative integers whose parity disagrees with the
character's parity:
- **odd** χ: Γ((s+1)/2) has poles at `s = −1, −3, −5, …` →
  `L(χ, −(2n+1)) = 0`
- **even** χ: Γ(s/2) has poles at `s = −2, −4, −6, …` →
  `L(χ, −2(n+1)) = 0`

These are the Dirichlet-L-series analogues of `zeta_neg_nat`. -/

/-- `L(χ₄, −(2n+1)) = 0` — trivial zeros at every odd negative integer
(odd character: Γ((s+1)/2) poles). -/
lemma chi4_LFunction_neg_odd (n : ℕ) :
    LFunction χ₄ℂ (-(2 * n) - 1) = 0 :=
  DirichletCharacter.Odd.LFunction_neg_two_mul_nat_sub_one χ₄ℂ_odd n

/-- `L(χ₈, −2(n+1)) = 0` — trivial zeros at every strictly negative
even integer (even character: Γ(s/2) poles). -/
lemma chi8_LFunction_neg_even (n : ℕ) :
    LFunction χ₈ℂ (-(2 * (n + 1))) = 0 :=
  DirichletCharacter.Even.LFunction_neg_two_mul_nat_add_one χ₈ℂ_even n

/-- `L(χ₈', −(2n+1)) = 0` — trivial zeros at odd negative integers. -/
lemma chi8'_LFunction_neg_odd (n : ℕ) :
    LFunction χ₈'ℂ (-(2 * n) - 1) = 0 :=
  DirichletCharacter.Odd.LFunction_neg_two_mul_nat_sub_one χ₈'ℂ_odd n

/-- `L(χ₃, −(2n+1)) = 0` — trivial zeros at odd negative integers. -/
lemma chi3_LFunction_neg_odd (n : ℕ) :
    LFunction χ₃ℂ (-(2 * n) - 1) = 0 :=
  DirichletCharacter.Odd.LFunction_neg_two_mul_nat_sub_one χ₃ℂ_odd n

/-! ### Dirichlet's theorem on primes in arithmetic progressions

The analytic engine above — in particular the nonvanishing of
`L(1, χ) ≠ 0` for every nontrivial character — activates mathlib's full
Dirichlet theorem (`DirichletsTheorem`).  The generic law below covers
**every** coprime modulus/residue pair; the lemma family that follows
instantiates it for the three supported levels (`3`, `4`, `8`), with
per-residue coverage examples. -/

/-- **Dirichlet's theorem** (generic): for any `q ≠ 0` and residue `a`
coprime to `q`, there are infinitely many primes `p ≡ a [MOD q]`. -/
lemma dirichlet_prime_infinitely_many (q a : ℕ) (hq : q ≠ 0) (ha : a.Coprime q) :
    {p : ℕ | p.Prime ∧ p ≡ a [MOD q]}.Infinite :=
  infinite_setOfPred_prime_and_modEq hq ha

/-- **Dirichlet's theorem** (generic, order form): for any `q ≠ 0`,
residue `a` coprime to `q`, and bound `n`, there is a prime `p > n`
with `p ≡ a [MOD q]` — so each coprime residue class contains unboundedly
many primes. -/
lemma dirichlet_prime_gt (q a : ℕ) (hq : q ≠ 0) (ha : a.Coprime q) (n : ℕ) :
    ∃ p : ℕ, p > n ∧ p.Prime ∧ p ≡ a [MOD q] :=
  forall_exists_prime_gt_and_modEq n hq ha

/-- **Dirichlet's theorem for the level `3`**: for any residue `a` coprime
to `3` (i.e. `a = 1, 2`), there are infinitely many primes
`p ≡ a [MOD 3]`. -/
lemma infinitelyManyPrimes_mod_three (a : ℕ) (ha : a.Coprime 3) :
    {p : ℕ | p.Prime ∧ p ≡ a [MOD 3]}.Infinite :=
  dirichlet_prime_infinitely_many 3 a (by decide) ha

/-- **Dirichlet's theorem for the level `4`**: for any residue `a` coprime
to `4` (i.e. `a = 1, 3`), there are infinitely many primes
`p ≡ a [MOD 4]`. -/
lemma infinitelyManyPrimes_mod_four (a : ℕ) (ha : a.Coprime 4) :
    {p : ℕ | p.Prime ∧ p ≡ a [MOD 4]}.Infinite :=
  dirichlet_prime_infinitely_many 4 a (by decide) ha

/-- **Dirichlet's theorem for the level `8`**: for any residue `a` coprime
to `8` (i.e. `a = 1, 3, 5, 7` — the odd residues), there are infinitely
many primes `p ≡ a [MOD 8]`. -/
lemma infinitelyManyPrimes_mod_eight (a : ℕ) (ha : a.Coprime 8) :
    {p : ℕ | p.Prime ∧ p ≡ a [MOD 8]}.Infinite :=
  dirichlet_prime_infinitely_many 8 a (by decide) ha

/-- Coverage of the level-3 register: both coprime residue classes. -/
example : {p : ℕ | p.Prime ∧ p ≡ 1 [MOD 3]}.Infinite :=
  infinitelyManyPrimes_mod_three 1 (by decide)

example : {p : ℕ | p.Prime ∧ p ≡ 2 [MOD 3]}.Infinite :=
  infinitelyManyPrimes_mod_three 2 (by decide)

/-- Coverage of the level-4 register: both coprime residue classes. -/
example : {p : ℕ | p.Prime ∧ p ≡ 1 [MOD 4]}.Infinite :=
  infinitelyManyPrimes_mod_four 1 (by decide)

example : {p : ℕ | p.Prime ∧ p ≡ 3 [MOD 4]}.Infinite :=
  infinitelyManyPrimes_mod_four 3 (by decide)

/-- Coverage of the level-8 register: all four odd residue classes. -/
example : {p : ℕ | p.Prime ∧ p ≡ 1 [MOD 8]}.Infinite :=
  infinitelyManyPrimes_mod_eight 1 (by decide)

example : {p : ℕ | p.Prime ∧ p ≡ 3 [MOD 8]}.Infinite :=
  infinitelyManyPrimes_mod_eight 3 (by decide)

example : {p : ℕ | p.Prime ∧ p ≡ 5 [MOD 8]}.Infinite :=
  infinitelyManyPrimes_mod_eight 5 (by decide)

example : {p : ℕ | p.Prime ∧ p ≡ 7 [MOD 8]}.Infinite :=
  infinitelyManyPrimes_mod_eight 7 (by decide)

/-- The generic law covers moduli beyond the registers: any coprime pair. -/
example : {p : ℕ | p.Prime ∧ p ≡ 4 [MOD 5]}.Infinite :=
  dirichlet_prime_infinitely_many 5 4 (by decide) (by decide)

example : {p : ℕ | p.Prime ∧ p ≡ 9 [MOD 10]}.Infinite :=
  dirichlet_prime_infinitely_many 10 9 (by decide) (by decide)

/-- The order form: beyond every bound there is a prime in the class. -/
example (n : ℕ) : ∃ p > n, p.Prime ∧ p ≡ 2 [MOD 5] :=
  dirichlet_prime_gt 5 2 (by decide) (by decide) n

/-!
# Exact special value at `s = 1`: `L(1, χ₄) = π/4` (Leibniz)

Certified here as a *Dirichlet-series* convergence identity: the ordered
partial sums of `Σₙ χ₄(n)/n` tend to `π/4`.  Rationale for this form:
mathlib's bridge from the analytic `LFunction` to the Dirichlet series
(`LFunction_eq_LSeries`) requires `1 < s.re`, so no bridge exists at
`s = 1`; the classical value is therefore stated as the ordered-partial-sum
(conditionally convergent) limit, reached through the Leibniz reindex
`n = 2i + 1`.

**Future work (NOT proved here):** the corresponding exact special values
`Σₙ χ₈(n)/n → ln(1+√2)/√2`, `Σₙ χ₈'(n)/n → π/(4√2)` follow the same
reindex method and need further open-`mathlib` machinery (the `ln(1+√2)`
series for `χ₈`).  They are left OPEN by design — no `sorry`, no unproved
claims.

The `χ₃` instance `Σₙ χ₃(n)/n → π/(3√3) = L(1, χ₃)` **is** closed, in the
next section, by a different route: the grouped series telescopes to the
geometric integral `∫₀¹ 1/(1+x+x²) dx = π/(3√3)` under dominated
convergence.
-/

lemma chi4_even_zero_real {n : ℕ} (hn : n % 2 = 0) : ((ZMod.χ₄ n : ℤ) : ℝ) = 0 := by
  have hz : ZMod.χ₄ n = 0 := by
    rw [ZMod.χ₄_nat_eq_if_mod_four]
    simp [hn]
  simp [hz]

lemma ZMod.chi4_two_mul_add_one_real (i : ℕ) :
    ((ZMod.χ₄ ((2 * i + 1 : ℕ) : ZMod 4) : ℤ) : ℝ) = (-1 : ℝ) ^ i := by
  have hodd : (2 * i + 1) % 2 = 1 := by omega
  have hhalf : (2 * i + 1) / 2 = i := by omega
  have h := ZMod.χ₄_eq_neg_one_pow (n := 2 * i + 1) hodd
  rw [hhalf] at h
  rw [h]
  norm_num

/-- The `χ₄` Dirichlet series at `s = 1` (`Σ χ₄(n)/n`): its partial sums coincide with the
Leibniz partial sums (limit `π/4`) after the reindex `n = 2i + 1`. -/
lemma chi4_series_partial_real (N : ℕ) :
    (∑ n ∈ Finset.range N, ((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ)) =
      ∑ i ∈ Finset.range (N / 2), (-1 : ℝ) ^ i / (2 * i + 1) := by
  calc
    (∑ n ∈ Finset.range N, ((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ))
        = ∑ n ∈ Finset.range N,
            (if n % 2 = 1 then ((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ) else 0) := by
          refine Finset.sum_congr rfl ?_
          intro n hn
          by_cases h : n % 2 = 1
          · simp [h]
          · have h0 : ((ZMod.χ₄ n : ℤ) : ℝ) = 0 :=
              chi4_even_zero_real (Nat.mod_two_eq_zero_or_one n |>.resolve_right h)
            rw [h0]
            simp [h]
    _    = ∑ n ∈ (Finset.range N).filter (fun n : ℕ => n % 2 = 1),
            ((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ) := by
          exact (Finset.sum_filter (s := Finset.range N)
            (p := fun n : ℕ => n % 2 = 1)
            (f := fun n : ℕ => ((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ))).symm
    _    = ∑ i ∈ Finset.range (N / 2), (-1 : ℝ) ^ i / (2 * i + 1) := by
          symm
          refine Finset.sum_bij (fun i _ => 2 * i + 1) ?_ ?_ ?_ ?_
          · intro i hi
            rw [Finset.mem_filter]
            constructor
            · rw [Finset.mem_range]
              have hi' : i < N / 2 := by
                rw [Finset.mem_range] at hi
                exact hi
              have hle : i + 1 ≤ N / 2 := Nat.succ_le_iff.mpr hi'
              have hm : 2 * (i + 1) ≤ 2 * (N / 2) := Nat.mul_le_mul_left 2 hle
              have hdiv : 2 * (N / 2) ≤ N := Nat.mul_div_le N 2
              omega
            · rw [show (2 * i + 1) % 2 = 1 by omega]
          · intro i₁ h₁ a₂ h₂ h
            omega
          · intro n hn
            rw [Finset.mem_filter, Finset.mem_range] at hn
            rcases hn with ⟨hnN, hnodd⟩
            refine ⟨n / 2, ⟨?_, ?_⟩⟩
            · rw [Finset.mem_range]
              omega
            · omega
          · intro i hi
            rw [ZMod.chi4_two_mul_add_one_real i]
            rw [show ((2 * i + 1 : ℕ) : ℝ) = 2 * (i : ℝ) + 1 by norm_num]

lemma chi4_series_real_pi_div_four :
    Tendsto (fun N : ℕ => ∑ n ∈ Finset.range N, ((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ)) atTop
      (𝓝 (Real.pi / 4 : ℝ)) := by
  have hdiv : Tendsto (fun N : ℕ => N / 2) atTop atTop := by
    rw [tendsto_atTop_atTop]
    intro b
    refine ⟨2 * b, ?_⟩
    intro m hm
    rw [Nat.le_div_iff_mul_le (by norm_num : 0 < 2)]
    omega
  have hmain : Tendsto (fun N : ℕ => ∑ i ∈ Finset.range (N / 2), (-1 : ℝ) ^ i / (2 * i + 1)) atTop
      (𝓝 (Real.pi / 4 : ℝ)) := Real.tendsto_sum_pi_div_four.comp hdiv
  convert hmain using 1
  funext N
  rw [chi4_series_partial_real]

lemma chi4ℂ_term_eq (n : ℕ) :
    (algebraMap ℝ ℂ) (((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ)) = (χ₄ℂ n) / (n : ℂ) := by
  have hnum : (algebraMap ℝ ℂ) (((ZMod.χ₄ n : ℤ) : ℝ)) = ((ZMod.χ₄ n : ℤ) : ℂ) := by norm_num
  have hnum2 : ((ZMod.χ₄ n : ℤ) : ℂ) = (χ₄ℂ n) := by simp [χ₄ℂ]
  have hden : (algebraMap ℝ ℂ) (n : ℝ) = (n : ℂ) := by rfl
  rw [map_div₀, hnum, hnum2, hden]

lemma chi4_series_eq_real (N : ℕ) :
    (algebraMap ℝ ℂ) (∑ n ∈ Finset.range N, (((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ)))
      = ∑ n ∈ Finset.range N, (χ₄ℂ n) / (n : ℂ) := by
  calc
    (algebraMap ℝ ℂ) (∑ n ∈ Finset.range N, (((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ)))
        = ∑ n ∈ Finset.range N, (algebraMap ℝ ℂ) (((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ)) :=
          map_sum (algebraMap ℝ ℂ) (fun n : ℕ => ((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ)) (Finset.range N)
    _ = ∑ n ∈ Finset.range N, (χ₄ℂ n) / (n : ℂ) :=
          Finset.sum_congr rfl (by intro n hn; exact chi4ℂ_term_eq n)

/-- The `L(1, χ₄) = π/4` special value as a Dirichlet-series limit: the ordered partial
sums `Σ_{n<N} χ₄(n)/n` (in `ℂ`) tend to `π/4`. -/
lemma chi4_series_pi_div_four :
    Tendsto (fun N : ℕ => ∑ n ∈ Finset.range N, (χ₄ℂ n) / (n : ℂ)) atTop (𝓝 (Real.pi / 4 : ℂ)) := by
  have hc : Tendsto (RCLike.ofReal ∘ (fun N : ℕ => ∑ n ∈ Finset.range N, ((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ))) atTop
      (𝓝 (RCLike.ofReal (K := ℂ) (Real.pi / 4 : ℝ))) :=
    RCLike.continuous_ofReal.continuousAt.tendsto.comp chi4_series_real_pi_div_four
  have hpi : 𝓝 (RCLike.ofReal (K := ℂ) (Real.pi / 4 : ℝ)) = 𝓝 (Real.pi / 4 : ℂ) := by
    congr 1
    change (algebraMap ℝ ℂ) (Real.pi / 4) = (Real.pi : ℂ) / 4
    exact map_div₀ (algebraMap ℝ ℂ) Real.pi 4
  have hobs : ∀ᶠ N in atTop,
      (RCLike.ofReal ∘ (fun N : ℕ => ∑ n ∈ Finset.range N, ((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ))) N =
        ∑ n ∈ Finset.range N, (χ₄ℂ n) / (n : ℂ) := by
    apply Filter.Eventually.of_forall
    intro N
    change (algebraMap ℝ ℂ) (∑ n ∈ Finset.range N, (((ZMod.χ₄ n : ℤ) : ℝ) / (n : ℝ))) =
      ∑ n ∈ Finset.range N, (χ₄ℂ n) / (n : ℂ)
    exact chi4_series_eq_real N
  simpa [hpi] using hc.congr' hobs

/-!
# Exact special value at `s = 1`: `L(1, χ₃) = π/(3√3)`

Certified here as a *Dirichlet-series* convergence identity: the ordered
partial sums of `Σₙ χ₃(n)/n` tend to `π/(3√3)`.  As with `χ₄`, mathlib's
bridge from the analytic `LFunction` to the Dirichlet series
(`LFunction_eq_LSeries`) requires `1 < s.re`, so no bridge exists at
`s = 1`; the classical value is stated as the ordered-partial-sum
(conditionally convergent) limit.

The step function route differs from the `χ₄ = π/4` reindex: the grouped
sums `Σₖ (1/(3k+1) − 1/(3k+2))` are realized on `(0,1]` by the step
functions `χ₃StepF N x = Σ_{k<N} (x^(3k) − x^(3k+1))`, whose partial
integrals coincide with the (real) grouped sums, whose limit is the
(interval) integral `∫₀¹ 1/(1+x+x²) dx = π/(3√3)` (dominated
convergence), and the ordered partial sums reduce to the grouped sums up
to a vanishing correction (`χ₃TurnTail`).  All certified with zero
`sorry`/`axiom`.
-/

set_option maxHeartbeats 400000

-- `χ₃` pattern on `ℕ`, as real values
noncomputable def chi3Z (n : ℕ) : ℝ :=
  if n % 3 = 1 then 1 else if n % 3 = 2 then -1 else 0

lemma chi3Z_three_mul (k : ℕ) : chi3Z (3 * k) = 0 := by
  have h : (3 * k) % 3 = 0 := by omega
  simp [chi3Z, h]
lemma chi3Z_three_mul_add_one (k : ℕ) : chi3Z (3 * k + 1) = 1 := by
  have h : (3 * k + 1) % 3 = 1 := by omega
  simp [chi3Z, h]
lemma chi3Z_three_mul_add_two (k : ℕ) : chi3Z (3 * k + 2) = -1 := by
  have h : (3 * k + 2) % 3 = 2 := by omega
  simp [chi3Z, h]

/-- The mod-3 pattern `chi3Z` is exactly the real values of the character
`ZMod.χ₃`: `χ₃(n) = 0, 1, -1` for `n ≡ 0, 1, 2 mod 3`. -/
lemma chi3Z_eq_χ₃ (n : ℕ) : ((ZMod.χ₃ n : ℤ) : ℝ) = chi3Z n := by
  have hmod : n % 3 = 0 ∨ n % 3 = 1 ∨ n % 3 = 2 := by omega
  rcases hmod with h0 | h1 | h2
  · have hn : (n : ZMod 3) = ((0 : ℕ) : ZMod 3) := by
      rw [ZMod.natCast_eq_natCast_iff]
      change n % 3 = 0 % 3
      simp [h0]
    have hz : ZMod.χ₃ (0 : ZMod 3) = 0 := by decide
    simp [hn, hz, chi3Z, h0]
  · have hn : (n : ZMod 3) = ((1 : ℕ) : ZMod 3) := by
      rw [ZMod.natCast_eq_natCast_iff]
      change n % 3 = 1 % 3
      simp [h1]
    have hz : ZMod.χ₃ (1 : ZMod 3) = 1 := by decide
    simp [hn, hz, chi3Z, h1]
  · have hn : (n : ZMod 3) = ((2 : ℕ) : ZMod 3) := by
      rw [ZMod.natCast_eq_natCast_iff]
      change n % 3 = 2 % 3
      simp [h2]
    have hz : ZMod.χ₃ (2 : ZMod 3) = -1 := by decide
    simp [hn, hz, chi3Z, h2]

-- the grouped series term, in `ℝ`
noncomputable def chi3GroupTerm (k : ℕ) : ℝ :=
  (1 : ℝ) / (3 * (k : ℝ) + 1) - (1 : ℝ) / (3 * (k : ℝ) + 2)

noncomputable def chi3Group (M : ℕ) : ℝ :=
  ∑ k ∈ Finset.range M, chi3GroupTerm k

-- ordered partial sums of `χ₃ n / n`
noncomputable def chi3Partial (N : ℕ) : ℝ :=
  ∑ n ∈ Finset.range N, chi3Z n / (n : ℝ)

-- the limit function on `[0,1]`: value is `1/(1+x+x^2)` for `x<1`, else 0
noncomputable def chi3LimitF (x : ℝ) : ℝ :=
  if x < 1 then 1 / (1 + x + x ^ 2) else 0

noncomputable def thetaF (x : ℝ) : ℝ :=
  (2 / Real.sqrt 3) * Real.arctan ((2 * x + 1) / Real.sqrt 3)

lemma hasDerivAt_thetaF (x : ℝ) :
    HasDerivAt thetaF (1 / (1 + x + x ^ 2)) x := by
  have hlin : HasDerivAt (fun y : ℝ => (2 * y + 1) / Real.sqrt 3) (2 / Real.sqrt 3) x := by
    have hA : HasDerivAt (fun y : ℝ => 2 * y + 1) 2 x := by
      simpa using ((hasDerivAt_id x).const_mul 2 |>.add_const 1)
    exact hA.div_const (Real.sqrt 3)
  have hcomp : HasDerivAt (fun y : ℝ => Real.arctan ((2 * y + 1) / Real.sqrt 3))
      ((1 / (1 + (((2 * x + 1) / Real.sqrt 3) ^ 2))) * (2 / Real.sqrt 3)) x := by
    exact HasDerivAt.comp (x := x) (h₂ := Real.arctan)
      (h₂' := (1 / (1 + (((2 * x + 1) / Real.sqrt 3) ^ 2)))) (h := fun y : ℝ => (2 * y + 1) / Real.sqrt 3)
      (h' := (2 / Real.sqrt 3)) (Real.hasDerivAt_arctan ((2 * x + 1) / Real.sqrt 3)) hlin
  have htot := hcomp.const_mul (2 / Real.sqrt 3)
  have hfix : (2 / Real.sqrt 3) * ((1 / (1 + (((2 * x + 1) / Real.sqrt 3) ^ 2))) *
      (2 / Real.sqrt 3)) = 1 / (1 + x + x ^ 2) := by
    have hdz : 1 + x + x ^ 2 ≠ 0 := by
      have hpos : 0 < 1 + x + x ^ 2 := by nlinarith [sq_nonneg (x + 1 / 2)]
      exact ne_of_gt hpos
    have hs2 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
    field_simp [hs2, hdz]
    ring_nf
    rw [hs2]
    ring
  convert htot using 1
  · rfl
  · rfl
  · rfl
  · exact hfix.symm

lemma integral_cubic_value :
    ∫ x in (0 : ℝ)..1, 1 / (1 + x + x ^ 2) = Real.pi / (3 * Real.sqrt 3) := by
  have hcont : ContinuousOn thetaF (Set.Icc 0 1) := by
    unfold thetaF
    fun_prop
  have hderiv : ∀ x ∈ Set.Ioo (0 : ℝ) 1, HasDerivAt thetaF (1 / (1 + x + x ^ 2)) x := by
    intro x hx
    exact hasDerivAt_thetaF x
  have hint : IntervalIntegrable (fun x : ℝ => 1 / (1 + x + x ^ 2)) MeasureTheory.volume 0 1 := by
    have hden : ∀ x : ℝ, 1 + x + x ^ 2 ≠ 0 := by
      intro x
      have hpos : 0 < 1 + x + x ^ 2 := by nlinarith [sq_nonneg (x + 1 / 2)]
      exact ne_of_gt hpos
    have hdencont : Continuous (fun x : ℝ => 1 + x + x ^ 2) := by fun_prop
    have hc : Continuous (fun x : ℝ => 1 / (1 + x + x ^ 2)) := by
      simpa using (hdencont.inv₀ hden).const_mul 1
    exact hc.intervalIntegrable 0 1
  have hftc := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le (a := (0 : ℝ)) (b := 1)
    (by norm_num) hcont hderiv hint
  have hval : thetaF 1 - thetaF 0 = Real.pi / (3 * Real.sqrt 3) := by
    unfold thetaF
    have hs2 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
    have h3 : (3 : ℝ) / Real.sqrt 3 = Real.sqrt 3 := by
      field_simp [hs2]; rw [hs2]
    have h1 : (1 : ℝ) / Real.sqrt 3 = (Real.sqrt 3)⁻¹ := by
      rw [one_div]
    rw [show (2 * 1 + 1 : ℝ) / Real.sqrt 3 = Real.sqrt 3 by
        rw [show (2 * 1 + 1 : ℝ) = 3 by norm_num]; exact h3,
      show (2 * 0 + 1 : ℝ) / Real.sqrt 3 = (Real.sqrt 3)⁻¹ by
        rw [show (2 * 0 + 1 : ℝ) = 1 by norm_num]; exact h1]
    rw [Real.arctan_sqrt_three, Real.arctan_inv_sqrt_three]
    field_simp
    norm_num
  rwa [hval] at hftc

lemma integral_pow_aux (m : ℕ) :
    ∫ x in (0 : ℝ)..1, x ^ m = (1 : ℝ) / (m + 1) := by
  have hF (x : ℝ) : HasDerivAt (fun y : ℝ => y ^ (m + 1) / (m + 1 : ℝ)) (x ^ m) x := by
    have hd := (hasDerivAt_id x).pow (m + 1)
    have hd' := hd.div_const (m + 1 : ℝ)
    convert hd' using 1
    · rfl
    · rfl
    · funext y
      simp [id]
    · have hc : (m + 1 : ℝ) ≠ 0 := by exact_mod_cast (Nat.succ_ne_zero m)
      simp [id]
      field_simp [hc]
  have hint : IntervalIntegrable (fun x : ℝ => x ^ m) MeasureTheory.volume 0 1 := by
    have hc : Continuous (fun x : ℝ => x ^ m) := by fun_prop
    exact hc.intervalIntegrable 0 1
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt (f := fun y : ℝ => y ^ (m + 1) / (m + 1 : ℝ))
      (f' := fun x : ℝ => x ^ m) (fun x _ => hF x) hint]
  simp

-- the grouped step functions
noncomputable def chi3StepF (N : ℕ) (x : ℝ) : ℝ :=
  ∑ k ∈ Finset.range N, (x ^ (3 * k) - x ^ (3 * k + 1))

lemma chi3StepF_closed (N : ℕ) (x : ℝ) :
    chi3StepF N x = (1 - x ^ (3 * N)) / (1 + x + x ^ 2) := by
  by_cases hx : x = 1
  · subst hx
    simp [chi3StepF]
  · have hdz : 1 + x + x ^ 2 ≠ 0 := by
      have hpos : 0 < 1 + x + x ^ 2 := by nlinarith [sq_nonneg x]
      exact ne_of_gt hpos
    have hx3ne : x ^ 3 ≠ 1 := by
      intro h
      have hfac : (x - 1) * (x ^ 2 + x + 1) = x ^ 3 - 1 := by ring
      have hm : (x - 1) * (x ^ 2 + x + 1) = 0 := by
        rw [hfac, h]; ring
      have hq : x ^ 2 + x + 1 ≠ 0 := by
        have hpos : 0 < x ^ 2 + x + 1 := by nlinarith [sq_nonneg x]
        exact ne_of_gt hpos
      have hz := mul_eq_zero.mp hm
      rcases hz with hx1 | hq0
      · exact hx (sub_eq_zero.mp hx1)
      · exact (hq hq0).elim
    have hsum : (∑ k ∈ Finset.range N, (x ^ 3) ^ k) = ((x ^ 3) ^ N - 1) / (x ^ 3 - 1) :=
      geom_sum_eq hx3ne N
    have hterm : ∀ k, x ^ (3 * k) - x ^ (3 * k + 1) = (1 - x) * (x ^ 3) ^ k := by
      intro k
      have h1 : x ^ (3 * k) = (x ^ 3) ^ k := by rw [pow_mul]
      have h2 : x ^ (3 * k + 1) = x * (x ^ 3) ^ k := by
        rw [← h1, pow_add, pow_one]
        ring
      calc
        x ^ (3 * k) - x ^ (3 * k + 1) = (x ^ 3) ^ k - x * (x ^ 3) ^ k := by rw [h1, h2]
        _ = (1 - x) * (x ^ 3) ^ k := by ring
    calc
      chi3StepF N x = ∑ k ∈ Finset.range N, (1 - x) * (x ^ 3) ^ k := by
        unfold chi3StepF
        refine Finset.sum_congr rfl ?_
        intro k hk
        exact hterm k
      _ = (1 - x) * ∑ k ∈ Finset.range N, (x ^ 3) ^ k := by rw [Finset.mul_sum]
      _ = (1 - x) * ((x ^ 3) ^ N - 1) / (x ^ 3 - 1) := by
        rw [hsum]
        ring
      _ = (1 - x ^ (3 * N)) / (1 + x + x ^ 2) := by
        have hpx : 1 - x ≠ 0 := sub_ne_zero.mpr (Ne.symm hx)
        have h13 : (x ^ 3) ^ N = x ^ (3 * N) := by rw [pow_mul]
        rw [h13]
        field_simp [hpx, hdz, hx3ne]
        ring_nf

lemma chi3StepF_norm_le {N : ℕ} {x : ℝ} (hx : x ∈ Set.Ioc (0 : ℝ) 1) :
    ‖chi3StepF N x‖ ≤ (1 : ℝ) := by
  rcases hx with ⟨h0, hxle⟩
  have hnum0 : 0 ≤ 1 - x ^ (3 * N) := by
    have hpl : x ^ (3 * N) ≤ 1 := pow_le_one₀ (n := 3 * N) h0.le hxle
    nlinarith
  have hnum1 : 1 - x ^ (3 * N) ≤ 1 := by
    nlinarith [pow_nonneg h0.le (3 * N)]
  have hd : 0 < 1 + x + x ^ 2 := by nlinarith [sq_nonneg x]
  have hden1 : 1 ≤ 1 + x + x ^ 2 := by nlinarith [sq_nonneg x]
  have hge : 0 ≤ (1 - x ^ (3 * N)) / (1 + x + x ^ 2) := div_nonneg hnum0 hd.le
  have hle : (1 - x ^ (3 * N)) / (1 + x + x ^ 2) ≤ 1 := by
    exact (div_le_one hd).2 (by nlinarith [pow_nonneg h0.le (3 * N), hden1])
  rw [chi3StepF_closed N x, Real.norm_eq_abs, abs_of_nonneg hge]
  exact hle

lemma chi3StepF_tendsto_limit {x : ℝ} (hx : x ∈ Set.Ioc (0 : ℝ) 1) :
    Tendsto (fun N : ℕ => chi3StepF N x) atTop (𝓝 (chi3LimitF x)) := by
  rcases hx with ⟨h0, hxle⟩
  by_cases hx1 : x = 1
  · subst hx1
    simp [chi3StepF, chi3LimitF]
  · have hlt : x < 1 := lt_of_le_of_ne hxle hx1
    have hlim : chi3LimitF x = 1 / (1 + x + x ^ 2) := by
      simp [chi3LimitF, hlt]
    rw [hlim]
    have hdz : 1 + x + x ^ 2 ≠ 0 := by
      have hpos : 0 < 1 + x + x ^ 2 := by nlinarith [sq_nonneg x]
      exact ne_of_gt hpos
    have hx2 : x ^ 2 < 1 := by
      have hlt2 : x ^ 2 < x := by
        simpa [pow_two] using (mul_lt_mul_of_pos_left hlt h0)
      exact lt_trans hlt2 hlt
    have hx3 : x ^ 3 < 1 := by
      have hle : x ^ 2 * x ≤ x ^ 2 := by
        have hc := mul_le_mul_of_nonneg_left hlt.le (pow_nonneg h0.le 2)
        simpa using hc
      have hlt2 := lt_of_le_of_lt hle hx2
      simpa [show x ^ 3 = x ^ 2 * x by ring] using hlt2
    have hx3n : ‖x ^ 3‖ < (1 : ℝ) := by
      rw [Real.norm_eq_abs, abs_of_pos (pow_pos h0 3)]
      exact hx3
    have ht0 : Tendsto (fun N : ℕ => (x ^ 3) ^ N) atTop (𝓝 (0 : ℝ)) :=
      tendsto_pow_atTop_nhds_zero_of_norm_lt_one hx3n
    have ht : Tendsto (fun N : ℕ => x ^ (3 * N)) atTop (𝓝 (0 : ℝ)) := by
      simpa [pow_mul] using ht0
    have hsub : Tendsto (fun N : ℕ => (1 : ℝ) - x ^ (3 * N)) atTop (𝓝 (1 : ℝ)) := by
      simpa using (tendsto_const_nhds (x := (1 : ℝ))).sub ht
    have ht1 : Tendsto (fun N : ℕ => (1 - x ^ (3 * N)) / (1 + x + x ^ 2)) atTop
        (𝓝 (1 / (1 + x + x ^ 2))) :=
      hsub.div tendsto_const_nhds hdz
    convert ht1 using 1
    · funext N
      exact chi3StepF_closed N x

lemma integral_chi3StepF (N : ℕ) :
    ∫ x in (0 : ℝ)..1, chi3StepF N x = chi3Group N := by
  unfold chi3StepF chi3Group
  have hI1 (k : ℕ) : IntervalIntegrable (fun x : ℝ => x ^ (3 * k)) MeasureTheory.volume 0 1 := by
    have hc : Continuous (fun x : ℝ => x ^ (3 * k)) := by fun_prop
    exact hc.intervalIntegrable 0 1
  have hI2 (k : ℕ) : IntervalIntegrable (fun x : ℝ => x ^ (3 * k + 1)) MeasureTheory.volume 0 1 := by
    have hc : Continuous (fun x : ℝ => x ^ (3 * k + 1)) := by fun_prop
    exact hc.intervalIntegrable 0 1
  rw [intervalIntegral.integral_finsetSum (fun k hk => (hI1 k).sub (hI2 k))]
  apply Finset.sum_congr rfl
  intro k hk
  rw [chi3GroupTerm]
  rw [intervalIntegral.integral_sub (hI1 k) (hI2 k)]
  rw [integral_pow_aux (3 * k), integral_pow_aux (3 * k + 1)]
  norm_num [Nat.cast_add, Nat.cast_mul]
  ring_nf

lemma tendsto_integral_chi3StepF :
    Tendsto (fun N : ℕ => ∫ x in (0 : ℝ)..1, chi3StepF N x) atTop
      (𝓝 (∫ x in (0 : ℝ)..1, chi3LimitF x)) := by
  refine intervalIntegral.tendsto_integral_filter_of_dominated_convergence
      (μ := MeasureTheory.volume) (l := atTop) (F := fun N x => chi3StepF N x)
      (bound := fun _ : ℝ => 1) (f := chi3LimitF) ?_ ?_ ?_ ?_
  · refine Eventually.of_forall ?_
    intro N
    have hc : Continuous (chi3StepF N) := by
      unfold chi3StepF
      fun_prop
    exact hc.aestronglyMeasurable
  · refine Eventually.of_forall ?_
    intro N
    exact MeasureTheory.ae_of_all MeasureTheory.volume
      (fun x => fun hx =>
        chi3StepF_norm_le (N := N) (by
          simpa [Set.uIoc_of_le (show (0 : ℝ) ≤ 1 by norm_num)] using hx))
  · have hc : Continuous (fun _ : ℝ => (1 : ℝ)) := continuous_const
    exact hc.intervalIntegrable 0 1
  · exact MeasureTheory.ae_of_all MeasureTheory.volume
      (fun x => fun hx =>
        chi3StepF_tendsto_limit (by
          simpa [Set.uIoc_of_le (show (0 : ℝ) ≤ 1 by norm_num)] using hx))

lemma chi3_group_tendsto :
    Tendsto chi3Group atTop (𝓝 (Real.pi / (3 * Real.sqrt 3))) := by
  have h1 := tendsto_integral_chi3StepF
  have hval : (∫ x in (0 : ℝ)..1, chi3LimitF x) = Real.pi / (3 * Real.sqrt 3) := by
    have hcongr : ∫ x in (0 : ℝ)..1, chi3LimitF x = ∫ x in (0 : ℝ)..1, 1 / (1 + x + x ^ 2) := by
      exact intervalIntegral.integral_congr_Ioo_of_le (show (0 : ℝ) ≤ 1 by norm_num)
        (fun x hx => by simp [chi3LimitF, hx.2])
    rw [hcongr]
    exact integral_cubic_value
  have h1' : Tendsto (fun N : ℕ => ∫ x in (0 : ℝ)..1, chi3StepF N x) atTop
      (𝓝 (Real.pi / (3 * Real.sqrt 3))) := by
    simpa [hval] using h1
  exact h1'.congr' (Eventually.of_forall (fun N => integral_chi3StepF N))

-- ordered partial sums reduce to the grouped series, plus a lim-vanishing correction

lemma chi3Partial_three_mul (M : ℕ) : chi3Partial (3 * M) = chi3Group M := by
  induction M with
  | zero => simp [chi3Partial, chi3Group]
  | succ M ih =>
      rw [show 3 * (M + 1) = 3 * M + 3 by omega]
      unfold chi3Partial
      rw [Finset.sum_range_succ]
      rw [Finset.sum_range_succ]
      rw [Finset.sum_range_succ]
      have h0 : chi3Z (3 * M) / ((3 * M : ℕ) : ℝ) = 0 := by
        rw [chi3Z_three_mul M]; simp
      have h1 : chi3Z (3 * M + 1) / ((3 * M + 1 : ℕ) : ℝ) = 1 / (3 * (M : ℝ) + 1) := by
        have hc1 : (((3 * M + 1 : ℕ) : ℝ)) = 3 * (M : ℝ) + 1 := by
          norm_num [Nat.cast_add, Nat.cast_mul]
        rw [chi3Z_three_mul_add_one M, hc1]
      have h2 : chi3Z (3 * M + 2) / ((3 * M + 2 : ℕ) : ℝ) = -(1 / (3 * (M : ℝ) + 2)) := by
        have hc2 : (((3 * M + 2 : ℕ) : ℝ)) = 3 * (M : ℝ) + 2 := by
          norm_num [Nat.cast_add, Nat.cast_mul]
        rw [chi3Z_three_mul_add_two M, hc2, neg_div]
      rw [h0, h1, h2]
      unfold chi3Group
      rw [Finset.sum_range_succ]
      change chi3Partial (3 * M) + (0 : ℝ) + (1 / (3 * (M : ℝ) + 1)) +
          (-(1 / (3 * (M : ℝ) + 2))) = chi3Group M + chi3GroupTerm M
      rw [ih]
      unfold chi3GroupTerm
      ring

noncomputable def chi3TurnTail (N : ℕ) : ℝ :=
  ∑ j ∈ Finset.range (N % 3), chi3Z (3 * (N / 3) + j) / ((3 * (N / 3) + j : ℕ) : ℝ)

lemma chi3TurnTail_eq_zero {N : ℕ} (hr : N % 3 = 0) : chi3TurnTail N = 0 := by
  unfold chi3TurnTail
  rw [hr]
  simp

lemma chi3TurnTail_eq_zero' {N : ℕ} (hr : N % 3 = 1) : chi3TurnTail N = 0 := by
  unfold chi3TurnTail
  rw [hr]
  rw [Finset.sum_range_succ]
  simp [chi3Z_three_mul]

lemma chi3TurnTail_eq_inv {N : ℕ} (hr : N % 3 = 2) :
    chi3TurnTail N = (1 : ℝ) / ((3 * (N / 3) + 1 : ℕ) : ℝ) := by
  unfold chi3TurnTail
  rw [hr]
  rw [Finset.sum_range_succ, Finset.sum_range_succ]
  simp [chi3Z_three_mul, chi3Z_three_mul_add_one]

lemma chi3Partial_split (N : ℕ) :
    chi3Partial N = chi3Partial (3 * (N / 3)) + chi3TurnTail N := by
  unfold chi3Partial chi3TurnTail
  conv_lhs => rw [← show (3 * (N / 3) + N % 3) = N by omega]
  rw [Finset.sum_range_add]

lemma chi3TurnTail_bound {N : ℕ} :
    ‖chi3TurnTail N‖ ≤ (1 : ℝ) / ((3 * (N / 3) + 1 : ℕ) : ℝ) := by
  have hmod : N % 3 = 0 ∨ N % 3 = 1 ∨ N % 3 = 2 := by omega
  rcases hmod with h0 | h1 | h2
  · rw [chi3TurnTail_eq_zero h0]
    simp
    have hk : (0 : ℕ) < 3 * (N / 3) + 1 := by omega
    have hd : (0 : ℝ) < ((3 * (N / 3) + 1 : ℕ) : ℝ) := by exact_mod_cast hk
    simpa using hd.le
  · rw [chi3TurnTail_eq_zero' h1]
    simp
    have hk : (0 : ℕ) < 3 * (N / 3) + 1 := by omega
    have hd : (0 : ℝ) < ((3 * (N / 3) + 1 : ℕ) : ℝ) := by exact_mod_cast hk
    simpa using hd.le
  · rw [chi3TurnTail_eq_inv h2]
    have hk : (0 : ℕ) < 3 * (N / 3) + 1 := by omega
    have hd1 : (0 : ℝ) < ((3 * (N / 3) + 1 : ℕ) : ℝ) := by exact_mod_cast hk
    have hpos : (0 : ℝ) < 1 / ((3 * (N / 3) + 1 : ℕ) : ℝ) := div_pos (by norm_num) hd1
    rw [Real.norm_eq_abs, abs_of_pos hpos]

lemma chi3TurnTail_tendsto : Tendsto chi3TurnTail atTop (𝓝 (0 : ℝ)) := by
  have hmd : Tendsto (fun N : ℕ => (3 * (N / 3) + 1 : ℕ)) atTop atTop := by
    rw [tendsto_atTop_atTop]
    intro b
    refine ⟨3 * b + 3, ?_⟩
    intro N hN
    omega
  have hcast : Tendsto (fun N : ℕ => (((3 * (N / 3) + 1 : ℕ) : ℝ))) atTop atTop :=
    tendsto_natCast_atTop_atTop.comp hmd
  have hinv : Tendsto (fun N : ℕ => (((3 * (N / 3) + 1 : ℕ) : ℝ)⁻¹)) atTop (𝓝 (0 : ℝ)) :=
    tendsto_inv_atTop_zero.comp hcast
  have hb : Tendsto (fun N : ℕ => (1 : ℝ) / ((3 * (N / 3) + 1 : ℕ) : ℝ)) atTop (𝓝 (0 : ℝ)) := by
    exact hinv.congr' (Eventually.of_forall (fun N => by rw [← one_div]))
  have hneg : Tendsto (fun N : ℕ => -((1 : ℝ) / ((3 * (N / 3) + 1 : ℕ) : ℝ))) atTop (𝓝 (0 : ℝ)) := by
    simpa using hb.neg
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le hneg hb ?_ ?_
  · intro N
    have hbN : |chi3TurnTail N| ≤ (1 : ℝ) / ((3 * (N / 3) + 1 : ℕ) : ℝ) := by
      simpa [Real.norm_eq_abs] using chi3TurnTail_bound (N := N)
    exact (abs_le.mp hbN).1
  · intro N
    have hbN : |chi3TurnTail N| ≤ (1 : ℝ) / ((3 * (N / 3) + 1 : ℕ) : ℝ) := by
      simpa [Real.norm_eq_abs] using chi3TurnTail_bound (N := N)
    exact (abs_le.mp hbN).2

lemma chi3Partial_tendsto :
    Tendsto chi3Partial atTop (𝓝 (Real.pi / (3 * Real.sqrt 3))) := by
  have hg : Tendsto (fun M : ℕ => chi3Partial (3 * M)) atTop (𝓝 (Real.pi / (3 * Real.sqrt 3))) :=
    chi3_group_tendsto.congr' (Eventually.of_forall (fun M => (chi3Partial_three_mul M).symm))
  have hq : Tendsto (fun N : ℕ => N / 3) atTop atTop := by
    rw [tendsto_atTop_atTop]
    intro b
    refine ⟨3 * (b + 1), ?_⟩
    intro N hN
    omega
  have hmain : Tendsto (fun N : ℕ => chi3Partial (3 * (N / 3))) atTop
      (𝓝 (Real.pi / (3 * Real.sqrt 3))) :=
    hg.comp hq
  have htail : Tendsto (fun N : ℕ => chi3Partial N - chi3Partial (3 * (N / 3))) atTop (𝓝 (0 : ℝ)) :=
    chi3TurnTail_tendsto.congr' (Eventually.of_forall (fun N => by
      change chi3TurnTail N = chi3Partial N - chi3Partial (3 * (N / 3))
      rw [chi3Partial_split]
      ring))
  have hsum := hmain.add htail
  convert hsum using 1
  · funext N
    ring
  · simp

/-- The `χ₃` Dirichlet series at `s = 1` (`Σ χ₃(n)/n`): its ordered partial sums in `ℝ`
coincide with the ordered partial sums of the mod-3 pattern `chi3Z n / n`. -/
lemma chi3_series_partial_real (N : ℕ) :
    (∑ n ∈ Finset.range N, ((ZMod.χ₃ n : ℤ) : ℝ) / (n : ℝ)) = chi3Partial N := by
  unfold chi3Partial
  refine Finset.sum_congr rfl ?_
  intro n hn
  rw [chi3Z_eq_χ₃ n]

/-- `L(1, χ₃) = π/(3√3)` as a Dirichlet-series limit (in `ℝ`): the ordered partial sums
`Σ_{n<N} χ₃(n)/n` tend to `π/(3√3)`. -/
lemma chi3_series_real_pi_div_three_sqrt_three :
    Tendsto (fun N : ℕ => ∑ n ∈ Finset.range N, ((ZMod.χ₃ n : ℤ) : ℝ) / (n : ℝ)) atTop
      (𝓝 (Real.pi / (3 * Real.sqrt 3) : ℝ)) := by
  convert chi3Partial_tendsto using 1
  funext N
  rw [chi3_series_partial_real]

lemma chi3ℂ_term_eq (n : ℕ) :
    (algebraMap ℝ ℂ) (((ZMod.χ₃ n : ℤ) : ℝ) / (n : ℝ)) = (χ₃ℂ n) / (n : ℂ) := by
  have hnum : (algebraMap ℝ ℂ) (((ZMod.χ₃ n : ℤ) : ℝ)) = ((ZMod.χ₃ n : ℤ) : ℂ) := by norm_num
  have hnum2 : ((ZMod.χ₃ n : ℤ) : ℂ) = (χ₃ℂ n) := by simp [χ₃ℂ]
  have hden : (algebraMap ℝ ℂ) (n : ℝ) = (n : ℂ) := by rfl
  rw [map_div₀, hnum, hnum2, hden]

lemma chi3_series_eq_real (N : ℕ) :
    (algebraMap ℝ ℂ) (∑ n ∈ Finset.range N, (((ZMod.χ₃ n : ℤ) : ℝ) / (n : ℝ)))
      = ∑ n ∈ Finset.range N, (χ₃ℂ n) / (n : ℂ) := by
  calc
    (algebraMap ℝ ℂ) (∑ n ∈ Finset.range N, (((ZMod.χ₃ n : ℤ) : ℝ) / (n : ℝ)))
        = ∑ n ∈ Finset.range N, (algebraMap ℝ ℂ) (((ZMod.χ₃ n : ℤ) : ℝ) / (n : ℝ)) :=
          map_sum (algebraMap ℝ ℂ) (fun n : ℕ => ((ZMod.χ₃ n : ℤ) : ℝ) / (n : ℝ)) (Finset.range N)
    _ = ∑ n ∈ Finset.range N, (χ₃ℂ n) / (n : ℂ) :=
          Finset.sum_congr rfl (by intro n hn; exact chi3ℂ_term_eq n)

/-- The `L(1, χ₃) = π/(3√3)` special value as a Dirichlet-series limit: the ordered partial
sums `Σ_{n<N} χ₃(n)/n` (in `ℂ`) tend to `π/(3√3)`. -/
lemma chi3_series_pi_div_three_sqrt_three :
    Tendsto (fun N : ℕ => ∑ n ∈ Finset.range N, (χ₃ℂ n) / (n : ℂ)) atTop
      (𝓝 (Real.pi / (3 * Real.sqrt 3) : ℂ)) := by
  have hc : Tendsto (RCLike.ofReal ∘ (fun N : ℕ => ∑ n ∈ Finset.range N, ((ZMod.χ₃ n : ℤ) : ℝ) / (n : ℝ))) atTop
      (𝓝 (RCLike.ofReal (K := ℂ) (Real.pi / (3 * Real.sqrt 3) : ℝ))) :=
    RCLike.continuous_ofReal.continuousAt.tendsto.comp chi3_series_real_pi_div_three_sqrt_three
  have hpi : 𝓝 (RCLike.ofReal (K := ℂ) (Real.pi / (3 * Real.sqrt 3) : ℝ)) =
      𝓝 (Real.pi / (3 * Real.sqrt 3) : ℂ) := by
    congr 1
    change (algebraMap ℝ ℂ) (Real.pi / (3 * Real.sqrt 3)) =
      (Real.pi : ℂ) / ((3 : ℂ) * (Real.sqrt 3 : ℂ))
    rw [map_div₀, map_mul]
    simp
  have hobs : ∀ᶠ N in atTop,
      (RCLike.ofReal ∘ (fun N : ℕ => ∑ n ∈ Finset.range N, ((ZMod.χ₃ n : ℤ) : ℝ) / (n : ℝ))) N =
        ∑ n ∈ Finset.range N, (χ₃ℂ n) / (n : ℂ) := by
    apply Filter.Eventually.of_forall
    intro N
    change (algebraMap ℝ ℂ) (∑ n ∈ Finset.range N, (((ZMod.χ₃ n : ℤ) : ℝ) / (n : ℝ))) =
      ∑ n ∈ Finset.range N, (χ₃ℂ n) / (n : ℂ)
    exact chi3_series_eq_real N
  simpa [hpi] using hc.congr' hobs


noncomputable def chi8PrimeZ (n : ℕ) : ℝ :=
  if n % 8 = 1 then 1 else if n % 8 = 3 then 1 else if n % 8 = 5 then -1 else
    if n % 8 = 7 then -1 else 0

lemma chi8PrimeZ_eight_mul (k : ℕ) : chi8PrimeZ (8 * k) = 0 := by
  simp [chi8PrimeZ]
lemma chi8PrimeZ_eight_mul_add_zero (k : ℕ) : chi8PrimeZ (8 * k + 0) = 0 := by
  simp [chi8PrimeZ]
lemma chi8PrimeZ_eight_mul_add_one (k : ℕ) : chi8PrimeZ (8 * k + 1) = 1 := by
  simp [chi8PrimeZ]
lemma chi8PrimeZ_eight_mul_add_two (k : ℕ) : chi8PrimeZ (8 * k + 2) = 0 := by
  simp [chi8PrimeZ]
lemma chi8PrimeZ_eight_mul_add_three (k : ℕ) : chi8PrimeZ (8 * k + 3) = 1 := by
  simp [chi8PrimeZ]
lemma chi8PrimeZ_eight_mul_add_four (k : ℕ) : chi8PrimeZ (8 * k + 4) = 0 := by
  simp [chi8PrimeZ]
lemma chi8PrimeZ_eight_mul_add_five (k : ℕ) : chi8PrimeZ (8 * k + 5) = -1 := by
  simp [chi8PrimeZ]
lemma chi8PrimeZ_eight_mul_add_six (k : ℕ) : chi8PrimeZ (8 * k + 6) = 0 := by
  simp [chi8PrimeZ]
lemma chi8PrimeZ_eight_mul_add_seven (k : ℕ) : chi8PrimeZ (8 * k + 7) = -1 := by
  simp [chi8PrimeZ]

/-- The mod-8 pattern `chi8PrimeZ` is exactly the real values of the character
`ZMod.χ₈'`: `χ₈'(n) = 0, 1, 1, -1, -1` on `n ≡ 0, 1, 3, 5, 7 mod 8`. -/
lemma chi8PrimeZ_eq_χ₈' (n : ℕ) : ((ZMod.χ₈' n : ℤ) : ℝ) = chi8PrimeZ n := by
  have hmod : n % 8 = 0 ∨ n % 8 = 1 ∨ n % 8 = 2 ∨ n % 8 = 3 ∨ n % 8 = 4 ∨ n % 8 = 5 ∨
      n % 8 = 6 ∨ n % 8 = 7 := by omega
  rcases hmod with h0 | h1 | h2 | h3 | h4 | h5 | h6 | h7
  · have hn : (n : ZMod 8) = ((0 : ℕ) : ZMod 8) := by
      rw [ZMod.natCast_eq_natCast_iff]
      change n % 8 = 0 % 8
      simp [h0]
    have hz : ZMod.χ₈' (0 : ZMod 8) = 0 := by decide
    simp [hn, hz, chi8PrimeZ, h0]
  · have hn : (n : ZMod 8) = ((1 : ℕ) : ZMod 8) := by
      rw [ZMod.natCast_eq_natCast_iff]
      change n % 8 = 1 % 8
      simp [h1]
    have hz : ZMod.χ₈' (1 : ZMod 8) = 1 := by decide
    simp [hn, hz, chi8PrimeZ, h1]
  · have hn : (n : ZMod 8) = ((2 : ℕ) : ZMod 8) := by
      rw [ZMod.natCast_eq_natCast_iff]
      change n % 8 = 2 % 8
      simp [h2]
    have hz : ZMod.χ₈' (2 : ZMod 8) = 0 := by decide
    simp [hn, hz, chi8PrimeZ, h2]
  · have hn : (n : ZMod 8) = ((3 : ℕ) : ZMod 8) := by
      rw [ZMod.natCast_eq_natCast_iff]
      change n % 8 = 3 % 8
      simp [h3]
    have hz : ZMod.χ₈' (3 : ZMod 8) = 1 := by decide
    simp [hn, hz, chi8PrimeZ, h3]
  · have hn : (n : ZMod 8) = ((4 : ℕ) : ZMod 8) := by
      rw [ZMod.natCast_eq_natCast_iff]
      change n % 8 = 4 % 8
      simp [h4]
    have hz : ZMod.χ₈' (4 : ZMod 8) = 0 := by decide
    simp [hn, hz, chi8PrimeZ, h4]
  · have hn : (n : ZMod 8) = ((5 : ℕ) : ZMod 8) := by
      rw [ZMod.natCast_eq_natCast_iff]
      change n % 8 = 5 % 8
      simp [h5]
    have hz : ZMod.χ₈' (5 : ZMod 8) = -1 := by decide
    simp [hn, hz, chi8PrimeZ, h5]
  · have hn : (n : ZMod 8) = ((6 : ℕ) : ZMod 8) := by
      rw [ZMod.natCast_eq_natCast_iff]
      change n % 8 = 6 % 8
      simp [h6]
    have hz : ZMod.χ₈' (6 : ZMod 8) = 0 := by decide
    simp [hn, hz, chi8PrimeZ, h6]
  · have hn : (n : ZMod 8) = ((7 : ℕ) : ZMod 8) := by
      rw [ZMod.natCast_eq_natCast_iff]
      change n % 8 = 7 % 8
      simp [h7]
    have hz : ZMod.χ₈' (7 : ZMod 8) = -1 := by decide
    simp [hn, hz, chi8PrimeZ, h7]

-- the grouped series term, in `ℝ`
noncomputable def chi8PrimeGroupTerm (k : ℕ) : ℝ :=
  (1 : ℝ) / (8 * (k : ℝ) + 1) + (1 : ℝ) / (8 * (k : ℝ) + 3)
    - (1 : ℝ) / (8 * (k : ℝ) + 5) - (1 : ℝ) / (8 * (k : ℝ) + 7)

noncomputable def chi8PrimeGroup (M : ℕ) : ℝ :=
  ∑ k ∈ Finset.range M, chi8PrimeGroupTerm k

-- ordered partial sums of `χ₈' n / n`
noncomputable def chi8PrimePartial (N : ℕ) : ℝ :=
  ∑ n ∈ Finset.range N, chi8PrimeZ n / (n : ℝ)

-- the limit function on `[0,1]`: value is `(1+x^2)/(1+x^4)` for `x<1`, else 0
noncomputable def chi8PrimeLimitF (x : ℝ) : ℝ :=
  if x < 1 then (1 + x ^ 2) / (1 + x ^ 4) else 0

noncomputable def chi8ThetaF (x : ℝ) : ℝ :=
  (1 / Real.sqrt 2) * Real.arctan (Real.sqrt 2 * x - 1) +
    (1 / Real.sqrt 2) * Real.arctan (Real.sqrt 2 * x + 1)

lemma hasDerivAt_chi8PhiF (x : ℝ) :
    HasDerivAt (fun y : ℝ => (1 / Real.sqrt 2) * Real.arctan (Real.sqrt 2 * y - 1))
      (1 / (x ^ 2 - Real.sqrt 2 * x + 1) / 2) x := by
  have hlin : HasDerivAt (fun y : ℝ => Real.sqrt 2 * y - 1) (Real.sqrt 2) x := by
    simpa using ((hasDerivAt_id x).const_mul (Real.sqrt 2)).add_const (-1)
  have harc : HasDerivAt (fun y : ℝ => Real.arctan (Real.sqrt 2 * y - 1))
      ((1 / (1 + (Real.sqrt 2 * x - 1) ^ 2)) * Real.sqrt 2) x := by
    exact HasDerivAt.comp (x := x) (h₂ := Real.arctan)
      (h₂' := (1 / (1 + ((Real.sqrt 2 * x - 1) ^ 2))))
      (h := fun y : ℝ => Real.sqrt 2 * y - 1)
      (h' := Real.sqrt 2) (Real.hasDerivAt_arctan (Real.sqrt 2 * x - 1)) hlin
  have htot := harc.const_mul (1 / Real.sqrt 2)
  have hfix : (1 / Real.sqrt 2) * ((1 / (1 + (Real.sqrt 2 * x - 1) ^ 2)) * Real.sqrt 2)
      = (1 / (x ^ 2 - Real.sqrt 2 * x + 1)) / 2 := by
    have hsqrt : Real.sqrt 2 ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr (by norm_num : (0 : ℝ) < 2))
    have hdz : x ^ 2 - Real.sqrt 2 * x + 1 ≠ 0 := by
      have hctx : (x - Real.sqrt 2 / 2) ^ 2 + 1 / 2 = x ^ 2 - Real.sqrt 2 * x + 1 := by
        have hs2' : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
        field_simp [hs2']
        ring_nf
        rw [hs2']
        ring
      have hpos : 0 < x ^ 2 - Real.sqrt 2 * x + 1 := by
        nlinarith [sq_nonneg (x - Real.sqrt 2 / 2), hctx]
      exact ne_of_gt hpos
    have hden_eq : 1 + (Real.sqrt 2 * x - 1) ^ 2 = 2 * (x ^ 2 - Real.sqrt 2 * x + 1) := by
      have hs2 : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
      rw [show (Real.sqrt 2 * x - 1) ^ 2 = (Real.sqrt 2) ^ 2 * x ^ 2 - 2 * Real.sqrt 2 * x + 1 by ring]
      rw [hs2]
      ring
    calc
      (1 / Real.sqrt 2) * ((1 / (1 + (Real.sqrt 2 * x - 1) ^ 2)) * Real.sqrt 2)
          = (1 / Real.sqrt 2) * ((1 / (2 * (x ^ 2 - Real.sqrt 2 * x + 1))) * Real.sqrt 2) := by
            rw [hden_eq]
      _ = ((1 / Real.sqrt 2) * Real.sqrt 2) * (1 / (2 * (x ^ 2 - Real.sqrt 2 * x + 1))) := by
            ring
      _ = (1 / (2 * (x ^ 2 - Real.sqrt 2 * x + 1))) := by
            have hprod : (1 / Real.sqrt 2) * Real.sqrt 2 = 1 := by
              field_simp [hsqrt]
            rw [hprod]
            ring
      _ = (1 / (x ^ 2 - Real.sqrt 2 * x + 1)) / 2 := by
            field_simp [hdz, (by norm_num : (2 : ℝ) ≠ 0)]
  rw [hfix] at htot
  exact htot

lemma hasDerivAt_chi8PsiF (x : ℝ) :
    HasDerivAt (fun y : ℝ => (1 / Real.sqrt 2) * Real.arctan (Real.sqrt 2 * y + 1))
      (1 / (x ^ 2 + Real.sqrt 2 * x + 1) / 2) x := by
  have hlin : HasDerivAt (fun y : ℝ => Real.sqrt 2 * y + 1) (Real.sqrt 2) x := by
    simpa using ((hasDerivAt_id x).const_mul (Real.sqrt 2)).add_const 1
  have harc : HasDerivAt (fun y : ℝ => Real.arctan (Real.sqrt 2 * y + 1))
      ((1 / (1 + (Real.sqrt 2 * x + 1) ^ 2)) * Real.sqrt 2) x := by
    exact HasDerivAt.comp (x := x) (h₂ := Real.arctan)
      (h₂' := (1 / (1 + ((Real.sqrt 2 * x + 1) ^ 2))))
      (h := fun y : ℝ => Real.sqrt 2 * y + 1)
      (h' := Real.sqrt 2) (Real.hasDerivAt_arctan (Real.sqrt 2 * x + 1)) hlin
  have htot := harc.const_mul (1 / Real.sqrt 2)
  have hfix : (1 / Real.sqrt 2) * ((1 / (1 + (Real.sqrt 2 * x + 1) ^ 2)) * Real.sqrt 2)
      = (1 / (x ^ 2 + Real.sqrt 2 * x + 1)) / 2 := by
    have hsqrt : Real.sqrt 2 ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr (by norm_num : (0 : ℝ) < 2))
    have hdz : x ^ 2 + Real.sqrt 2 * x + 1 ≠ 0 := by
      have hctx : (x + Real.sqrt 2 / 2) ^ 2 + 1 / 2 = x ^ 2 + Real.sqrt 2 * x + 1 := by
        have hs2' : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
        field_simp [hs2']
        ring_nf
        rw [hs2']
        ring
      have hpos : 0 < x ^ 2 + Real.sqrt 2 * x + 1 := by
        nlinarith [sq_nonneg (x + Real.sqrt 2 / 2), hctx]
      exact ne_of_gt hpos
    have hden_eq : 1 + (Real.sqrt 2 * x + 1) ^ 2 = 2 * (x ^ 2 + Real.sqrt 2 * x + 1) := by
      have hs2 : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
      rw [show (Real.sqrt 2 * x + 1) ^ 2 = (Real.sqrt 2) ^ 2 * x ^ 2 + 2 * Real.sqrt 2 * x + 1 by ring]
      rw [hs2]
      ring
    calc
      (1 / Real.sqrt 2) * ((1 / (1 + (Real.sqrt 2 * x + 1) ^ 2)) * Real.sqrt 2)
          = (1 / Real.sqrt 2) * ((1 / (2 * (x ^ 2 + Real.sqrt 2 * x + 1))) * Real.sqrt 2) := by
            rw [hden_eq]
      _ = ((1 / Real.sqrt 2) * Real.sqrt 2) * (1 / (2 * (x ^ 2 + Real.sqrt 2 * x + 1))) := by
            ring
      _ = (1 / (2 * (x ^ 2 + Real.sqrt 2 * x + 1))) := by
            have hprod : (1 / Real.sqrt 2) * Real.sqrt 2 = 1 := by
              field_simp [hsqrt]
            rw [hprod]
            ring
      _ = (1 / (x ^ 2 + Real.sqrt 2 * x + 1)) / 2 := by
            field_simp [hdz, (by norm_num : (2 : ℝ) ≠ 0)]
  rw [hfix] at htot
  exact htot

lemma hasDerivAt_chi8ThetaF (x : ℝ) :
    HasDerivAt chi8ThetaF ((1 + x ^ 2) / (1 + x ^ 4)) x := by
  have hsum := (hasDerivAt_chi8PhiF x).add (hasDerivAt_chi8PsiF x)
  have hfix : (1 / (x ^ 2 - Real.sqrt 2 * x + 1)) / 2 +
        (1 / (x ^ 2 + Real.sqrt 2 * x + 1)) / 2 = (1 + x ^ 2) / (1 + x ^ 4) := by
    have hs2 : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
    have hdp : x ^ 2 - Real.sqrt 2 * x + 1 ≠ 0 := by
      have hctx : (x - Real.sqrt 2 / 2) ^ 2 + 1 / 2 = x ^ 2 - Real.sqrt 2 * x + 1 := by
        have hs2' : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
        field_simp [hs2']
        ring_nf
        rw [hs2']
        ring
      have hpos : 0 < x ^ 2 - Real.sqrt 2 * x + 1 := by
        nlinarith [sq_nonneg (x - Real.sqrt 2 / 2), hctx]
      exact ne_of_gt hpos
    have hdq : x ^ 2 + Real.sqrt 2 * x + 1 ≠ 0 := by
      have hctx : (x + Real.sqrt 2 / 2) ^ 2 + 1 / 2 = x ^ 2 + Real.sqrt 2 * x + 1 := by
        have hs2' : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
        field_simp [hs2']
        ring_nf
        rw [hs2']
        ring
      have hpos : 0 < x ^ 2 + Real.sqrt 2 * x + 1 := by
        nlinarith [sq_nonneg (x + Real.sqrt 2 / 2), hctx]
      exact ne_of_gt hpos
    have hdn : 1 + x ^ 4 ≠ 0 := by
      have hpos : 0 < 1 + x ^ 4 := by nlinarith [sq_nonneg (x ^ 2)]
      exact ne_of_gt hpos
    have hAB : (x ^ 2 - Real.sqrt 2 * x + 1) * (x ^ 2 + Real.sqrt 2 * x + 1) = x ^ 4 + 1 := by
      calc
        (x ^ 2 - Real.sqrt 2 * x + 1) * (x ^ 2 + Real.sqrt 2 * x + 1)
            = (x ^ 2 + 1) ^ 2 - (Real.sqrt 2 * x) ^ 2 := by ring
        _ = (x ^ 2 + 1) ^ 2 - (Real.sqrt 2) ^ 2 * x ^ 2 := by
              rw [show (Real.sqrt 2 * x) ^ 2 = (Real.sqrt 2) ^ 2 * x ^ 2 by ring]
        _ = (x ^ 2 + 1) ^ 2 - 2 * x ^ 2 := by rw [hs2]
        _ = x ^ 4 + 1 := by ring
    have hsumden : (1 / (x ^ 2 - Real.sqrt 2 * x + 1)) + (1 / (x ^ 2 + Real.sqrt 2 * x + 1))
        = (2 * (x ^ 2 + 1)) / (x ^ 4 + 1) := by
      have hstep := div_add_div (a := (1 : ℝ)) (c := (1 : ℝ)) hdp hdq
      rw [hstep]
      rw [hAB]
      congr 1
      ring
    calc
      (1 / (x ^ 2 - Real.sqrt 2 * x + 1)) / 2 + (1 / (x ^ 2 + Real.sqrt 2 * x + 1)) / 2
          = ((1 / (x ^ 2 - Real.sqrt 2 * x + 1)) + (1 / (x ^ 2 + Real.sqrt 2 * x + 1))) / 2 := by
            ring
      _ = ((2 * (x ^ 2 + 1)) / (x ^ 4 + 1)) / 2 := by rw [hsumden]
      _ = (1 + x ^ 2) / (1 + x ^ 4) := by
            field_simp [hdn]
            ring
  rw [hfix] at hsum
  exact hsum

lemma integral_chi8Prime_value :
    ∫ x in (0 : ℝ)..1, (1 + x ^ 2) / (1 + x ^ 4) = Real.pi / (2 * Real.sqrt 2) := by
  have hcont : ContinuousOn chi8ThetaF (Set.Icc 0 1) := by
    unfold chi8ThetaF
    fun_prop
  have hderiv : ∀ x ∈ Set.Ioo (0 : ℝ) 1, HasDerivAt chi8ThetaF ((1 + x ^ 2) / (1 + x ^ 4)) x := by
    intro x hx
    exact hasDerivAt_chi8ThetaF x
  have hint : IntervalIntegrable (fun x : ℝ => (1 + x ^ 2) / (1 + x ^ 4)) MeasureTheory.volume 0 1 := by
    have hden : ∀ x : ℝ, 1 + x ^ 4 ≠ 0 := by
      intro x
      have hpos : 0 < 1 + x ^ 4 := by nlinarith [sq_nonneg (x ^ 2)]
      exact ne_of_gt hpos
    have hc1 : Continuous (fun x : ℝ => 1 + x ^ 4) := by fun_prop
    have hc2 : Continuous (fun x : ℝ => 1 + x ^ 2) := by fun_prop
    have hc : Continuous (fun x : ℝ => (1 + x ^ 2) / (1 + x ^ 4)) := by
      have hcm : Continuous (fun x : ℝ => (1 + x ^ 2) * (1 + x ^ 4)⁻¹) := hc2.mul (hc1.inv₀ hden)
      refine hcm.congr ?_
      intro x
      rw [← div_eq_mul_inv]
    exact hc.intervalIntegrable 0 1
  have hftc := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le (a := (0 : ℝ)) (b := 1)
    (by norm_num) hcont hderiv hint
  have hval : chi8ThetaF 1 - chi8ThetaF 0 = Real.pi / (2 * Real.sqrt 2) := by
    unfold chi8ThetaF
    have hls : (1 : ℝ) < Real.sqrt 2 := by
      have h := Real.sqrt_lt_sqrt (by norm_num : (0 : ℝ) ≤ 1) (by norm_num : (1 : ℝ) < 2)
      simpa [Real.sqrt_one] using h
    have hp : 0 < Real.sqrt 2 - 1 := by linarith
    have hsum : Real.arctan (Real.sqrt 2 - 1) + Real.arctan (Real.sqrt 2 + 1) = Real.pi / 2 := by
      have hA := Real.arctan_inv_of_pos hp
      rw [Real.inv_sqrt_two_sub_one] at hA
      linarith
    have hs0 : Real.arctan (Real.sqrt 2 * 0 - 1) + Real.arctan (Real.sqrt 2 * 0 + 1) = 0 := by
      simp [Real.arctan_neg, Real.arctan_one]
    rw [← mul_add, ← mul_add, hs0]
    simp
    rw [hsum]
    have hsqrt : Real.sqrt 2 ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr (by norm_num : (0 : ℝ) < 2))
    field_simp [hsqrt, (by norm_num : (2 : ℝ) ≠ 0)]
  rwa [hval] at hftc

lemma integral_pow_aux8 (m : ℕ) :
    ∫ x in (0 : ℝ)..1, x ^ m = (1 : ℝ) / (m + 1) := by
  exact integral_pow_aux m

-- the grouped step functions
noncomputable def chi8PrimeStepF (N : ℕ) (x : ℝ) : ℝ :=
  ∑ k ∈ Finset.range N, (x ^ (8 * k) + x ^ (8 * k + 2) - x ^ (8 * k + 4) - x ^ (8 * k + 6))

lemma chi8PrimeStepF_closed {N : ℕ} {x : ℝ} (hx : x ∈ Set.Ioc (0 : ℝ) 1) :
    chi8PrimeStepF N x = (1 + x ^ 2 - x ^ 4 - x ^ 6) * (1 - x ^ (8 * N)) / (1 - x ^ 8) := by
  rcases hx with ⟨h0, hxle⟩
  by_cases hx1 : x = 1
  · subst hx1
    have hstep : chi8PrimeStepF N 1 = 0 := by
      unfold chi8PrimeStepF
      apply Finset.sum_eq_zero
      intro k hk
      have h1 : (1 : ℝ) ^ (8 * k) = 1 := by simp
      have h2 : (1 : ℝ) ^ (8 * k + 2) = 1 := by simp
      have h4 : (1 : ℝ) ^ (8 * k + 4) = 1 := by simp
      have h6 : (1 : ℝ) ^ (8 * k + 6) = 1 := by simp
      rw [h1, h2, h4, h6]
      norm_num
    have h8N : (1 : ℝ) ^ (8 * N) = 1 := by simp
    rw [hstep, h8N]
    norm_num
  · have hlt : x < 1 := lt_of_le_of_ne hxle hx1
    have hx8ne : x ^ 8 ≠ 1 := by
      have hp : x ^ 8 < 1 := pow_lt_one₀ h0.le hlt (by norm_num : (8 : ℕ) ≠ 0)
      exact ne_of_lt hp
    have hsum : (∑ k ∈ Finset.range N, (x ^ 8) ^ k) = ((x ^ 8) ^ N - 1) / (x ^ 8 - 1) :=
      geom_sum_eq hx8ne N
    have hterm : ∀ k, x ^ (8 * k) + x ^ (8 * k + 2) - x ^ (8 * k + 4) - x ^ (8 * k + 6)
        = (1 + x ^ 2 - x ^ 4 - x ^ 6) * (x ^ 8) ^ k := by
      intro k
      have h1 : x ^ (8 * k) = (x ^ 8) ^ k := by rw [pow_mul]
      have h2 : x ^ (8 * k + 2) = x ^ 2 * (x ^ 8) ^ k := by
        calc x ^ (8 * k + 2) = x ^ (8 * k) * x ^ 2 := by rw [pow_add]
             _ = (x ^ 8) ^ k * x ^ 2 := by rw [h1]
             _ = x ^ 2 * (x ^ 8) ^ k := by ring
      have h4 : x ^ (8 * k + 4) = x ^ 4 * (x ^ 8) ^ k := by
        calc x ^ (8 * k + 4) = x ^ (8 * k) * x ^ 4 := by rw [pow_add]
             _ = (x ^ 8) ^ k * x ^ 4 := by rw [h1]
             _ = x ^ 4 * (x ^ 8) ^ k := by ring
      have h6 : x ^ (8 * k + 6) = x ^ 6 * (x ^ 8) ^ k := by
        calc x ^ (8 * k + 6) = x ^ (8 * k) * x ^ 6 := by rw [pow_add]
             _ = (x ^ 8) ^ k * x ^ 6 := by rw [h1]
             _ = x ^ 6 * (x ^ 8) ^ k := by ring
      rw [h1, h2, h4, h6]
      ring
    calc
      chi8PrimeStepF N x = ∑ k ∈ Finset.range N, (1 + x ^ 2 - x ^ 4 - x ^ 6) * (x ^ 8) ^ k := by
        unfold chi8PrimeStepF
        refine Finset.sum_congr rfl ?_
        intro k hk
        exact hterm k
      _ = (1 + x ^ 2 - x ^ 4 - x ^ 6) * ∑ k ∈ Finset.range N, (x ^ 8) ^ k := by
        rw [Finset.mul_sum]
      _ = (1 + x ^ 2 - x ^ 4 - x ^ 6) * ((x ^ 8) ^ N - 1) / (x ^ 8 - 1) := by
        rw [hsum]
        ring
      _ = (1 + x ^ 2 - x ^ 4 - x ^ 6) * (1 - x ^ (8 * N)) / (1 - x ^ 8) := by
        have hpow : (x ^ 8) ^ N = x ^ (8 * N) := by rw [pow_mul]
        have hneg : (x ^ 8) ^ N - 1 = -(1 - x ^ (8 * N)) := by
          rw [hpow]
          ring
        have hneg2 : x ^ 8 - 1 = -(1 - x ^ 8) := by ring
        have hd8 : (1 : ℝ) - x ^ 8 ≠ 0 := sub_ne_zero.mpr hx8ne.symm
        rw [hneg, hneg2]
        field_simp [hd8]

lemma chi8PrimeStepF_norm_le {N : ℕ} {x : ℝ} (hx : x ∈ Set.Ioc (0 : ℝ) 1) :
    ‖chi8PrimeStepF N x‖ ≤ (2 : ℝ) := by
  rcases hx with ⟨h0, hxle⟩
  by_cases hx1 : x = 1
  · subst hx1
    have hstep : chi8PrimeStepF N 1 = 0 := by
      unfold chi8PrimeStepF
      apply Finset.sum_eq_zero
      intro k hk
      have h1 : (1 : ℝ) ^ (8 * k) = 1 := by simp
      have h2 : (1 : ℝ) ^ (8 * k + 2) = 1 := by simp
      have h4 : (1 : ℝ) ^ (8 * k + 4) = 1 := by simp
      have h6 : (1 : ℝ) ^ (8 * k + 6) = 1 := by simp
      rw [h1, h2, h4, h6]
      norm_num
    rw [hstep]
    norm_num
  · have hlt : x < 1 := lt_of_le_of_ne hxle hx1
    rw [chi8PrimeStepF_closed (N := N) (x := x) ⟨h0, hxle⟩]
    have hfac : 1 + x ^ 2 - x ^ 4 - x ^ 6 = (1 - x ^ 2) * (1 + x ^ 2) ^ 2 := by ring
    have hfac2 : 1 - x ^ 8 = (1 - x ^ 2) * (1 + x ^ 2) * (1 + x ^ 4) := by ring
    have hge1 : 0 ≤ 1 - x ^ 2 := by
      have hp := pow_le_one₀ (n := 2) h0.le hxle
      nlinarith
    have hgeX : 0 ≤ 1 + x ^ 2 := by nlinarith [sq_nonneg x]
    have hge8 : 0 ≤ 1 - x ^ (8 * N) := by
      have hp := pow_le_one₀ (n := 8 * N) h0.le hxle
      nlinarith
    have hdenpos : 0 < 1 - x ^ 8 := by
      have hp : x ^ 8 < 1 := pow_lt_one₀ h0.le hlt (by norm_num : (8 : ℕ) ≠ 0)
      nlinarith
    have hx2le1 : (1 + x ^ 2) ≤ 2 := by
      have h2' : x ^ 2 ≤ 1 := by nlinarith [sq_nonneg x, hxle]
      nlinarith
    have h4 : 0 ≤ x ^ 4 := pow_nonneg h0.le 4
    have hmain : (1 + x ^ 2) * (1 - x ^ (8 * N)) ≤ 2 * (1 + x ^ 4) := by
      have hb1 : (1 + x ^ 2) * (1 - x ^ (8 * N)) ≤ (1 + x ^ 2) * 1 :=
        mul_le_mul_of_nonneg_left (by
          have hx8 : 0 ≤ x ^ (8 * N) := pow_nonneg h0.le (8 * N)
          nlinarith) hgeX
      have hb3 : (1 + x ^ 2) ≤ 2 * (1 + x ^ 4) := by
        have h0' : (2 : ℝ) ≤ 2 * (1 + x ^ 4) := by nlinarith [h4]
        exact le_trans hx2le1 h0'
      calc
        (1 + x ^ 2) * (1 - x ^ (8 * N)) ≤ (1 + x ^ 2) * 1 := hb1
        _ = 1 + x ^ 2 := by ring
        _ ≤ 2 * (1 + x ^ 4) := hb3
    have hinter : (1 + x ^ 2) ^ 2 * (1 - x ^ (8 * N)) ≤ (1 + x ^ 2) * (2 * (1 + x ^ 4)) := by
      have hh := mul_le_mul_of_nonneg_left hmain hgeX
      calc
        (1 + x ^ 2) ^ 2 * (1 - x ^ (8 * N)) = (1 + x ^ 2) * ((1 + x ^ 2) * (1 - x ^ (8 * N))) := by ring
        _ ≤ (1 + x ^ 2) * (2 * (1 + x ^ 4)) := hh
    have hnum0 : 0 ≤ (1 + x ^ 2 - x ^ 4 - x ^ 6) * (1 - x ^ (8 * N)) := by
      have hA : 0 ≤ 1 + x ^ 2 - x ^ 4 - x ^ 6 := by
        rw [hfac]
        exact mul_nonneg hge1 (sq_nonneg (1 + x ^ 2))
      exact mul_nonneg hA hge8
    have htop : (1 + x ^ 2 - x ^ 4 - x ^ 6) * (1 - x ^ (8 * N)) ≤ 2 * (1 - x ^ 8) := by
      have hh := mul_le_mul_of_nonneg_left hinter hge1
      calc
        (1 + x ^ 2 - x ^ 4 - x ^ 6) * (1 - x ^ (8 * N))
            = (1 - x ^ 2) * ((1 + x ^ 2) ^ 2 * (1 - x ^ (8 * N))) := by
              rw [hfac]
              ring
        _ ≤ (1 - x ^ 2) * ((1 + x ^ 2) * (2 * (1 + x ^ 4))) := hh
        _ = 2 * (1 - x ^ 8) := by rw [hfac2]; ring
    have hge : 0 ≤ (1 + x ^ 2 - x ^ 4 - x ^ 6) * (1 - x ^ (8 * N)) / (1 - x ^ 8) :=
      div_nonneg hnum0 hdenpos.le
    have hle' : (1 + x ^ 2 - x ^ 4 - x ^ 6) * (1 - x ^ (8 * N)) / (1 - x ^ 8) ≤ 2 := by
      rw [div_le_iff₀ hdenpos]
      exact htop
    rw [Real.norm_eq_abs, abs_of_nonneg hge]
    exact hle'

lemma chi8PrimeStepF_tendsto_limit {x : ℝ} (hx : x ∈ Set.Ioc (0 : ℝ) 1) :
    Tendsto (fun N : ℕ => chi8PrimeStepF N x) atTop (𝓝 (chi8PrimeLimitF x)) := by
  rcases hx with ⟨h0, hxle⟩
  by_cases hx1 : x = 1
  · subst hx1
    have hz : ∀ N : ℕ, chi8PrimeStepF N 1 = 0 := by
      intro N
      unfold chi8PrimeStepF
      apply Finset.sum_eq_zero
      intro k hk
      have h1 : (1 : ℝ) ^ (8 * k) = 1 := by simp
      have h2 : (1 : ℝ) ^ (8 * k + 2) = 1 := by simp
      have h4 : (1 : ℝ) ^ (8 * k + 4) = 1 := by simp
      have h6 : (1 : ℝ) ^ (8 * k + 6) = 1 := by simp
      rw [h1, h2, h4, h6]
      norm_num
    have hlf : chi8PrimeLimitF 1 = 0 := by simp [chi8PrimeLimitF]
    simp [hz, hlf]
  · have hlt : x < 1 := lt_of_le_of_ne hxle hx1
    have hlim : chi8PrimeLimitF x = (1 + x ^ 2) / (1 + x ^ 4) := by
      simp [chi8PrimeLimitF, hlt]
    have hx8lt : ‖x ^ 8‖ < (1 : ℝ) := by
      rw [Real.norm_eq_abs, abs_of_pos (pow_pos h0 8)]
      exact pow_lt_one₀ h0.le hlt (by norm_num : (8 : ℕ) ≠ 0)
    have ht0 : Tendsto (fun N : ℕ => (x ^ 8) ^ N) atTop (𝓝 (0 : ℝ)) :=
      tendsto_pow_atTop_nhds_zero_of_norm_lt_one hx8lt
    have ht8 : Tendsto (fun N : ℕ => x ^ (8 * N)) atTop (𝓝 (0 : ℝ)) := by
      simpa [pow_mul] using ht0
    have hsub : Tendsto (fun N : ℕ => (1 : ℝ) - x ^ (8 * N)) atTop (𝓝 (1 : ℝ)) := by
      simpa using (tendsto_const_nhds (x := (1 : ℝ))).sub ht8
    have hconst : Tendsto (fun _ : ℕ => (1 + x ^ 2 - x ^ 4 - x ^ 6 : ℝ)) atTop
        (𝓝 (1 + x ^ 2 - x ^ 4 - x ^ 6)) := tendsto_const_nhds
    have hnum : Tendsto (fun N : ℕ => (1 + x ^ 2 - x ^ 4 - x ^ 6) * (1 - x ^ (8 * N))) atTop
        (𝓝 (1 + x ^ 2 - x ^ 4 - x ^ 6)) := by
      have hm := hconst.mul hsub
      simpa using hm
    have hden : Tendsto (fun _ : ℕ => (1 - x ^ 8 : ℝ)) atTop (𝓝 (1 - x ^ 8)) := tendsto_const_nhds
    have hd8 : (1 : ℝ) - x ^ 8 ≠ 0 := by
      have hp : x ^ 8 < 1 := pow_lt_one₀ h0.le hlt (by norm_num : (8 : ℕ) ≠ 0)
      nlinarith
    have hq : Tendsto (fun N : ℕ => ((1 + x ^ 2 - x ^ 4 - x ^ 6) * (1 - x ^ (8 * N))) / (1 - x ^ 8))
        atTop (𝓝 ((1 + x ^ 2 - x ^ 4 - x ^ 6) / (1 - x ^ 8))) :=
      hnum.div hden hd8
    have hv : (1 + x ^ 2 - x ^ 4 - x ^ 6) / (1 - x ^ 8) = (1 + x ^ 2) / (1 + x ^ 4) := by
      have hd4p : 0 < 1 - x ^ 4 := by
        have hp : x ^ 4 < 1 := pow_lt_one₀ h0.le hlt (by norm_num : (4 : ℕ) ≠ 0)
        nlinarith
      have hden4 : 1 + x ^ 4 ≠ 0 := by
        have hpos : 0 < 1 + x ^ 4 := by nlinarith [sq_nonneg (x ^ 2)]
        exact ne_of_gt hpos
      have hfac : 1 + x ^ 2 - x ^ 4 - x ^ 6 = (1 + x ^ 2) * (1 - x ^ 4) := by ring
      have hfac8 : 1 - x ^ 8 = (1 - x ^ 4) * (1 + x ^ 4) := by ring
      calc
        (1 + x ^ 2 - x ^ 4 - x ^ 6) / (1 - x ^ 8)
            = ((1 + x ^ 2) * (1 - x ^ 4)) / ((1 - x ^ 4) * (1 + x ^ 4)) := by
              rw [hfac, hfac8]
        _ = (1 + x ^ 2) / (1 + x ^ 4) := by
          field_simp [ne_of_gt hd4p, hden4]
    have hq' : Tendsto (fun N : ℕ => chi8PrimeStepF N x) atTop
        (𝓝 ((1 + x ^ 2) / (1 + x ^ 4))) := by
      simpa [hv] using hq.congr' (Eventually.of_forall (fun N => by
        exact (chi8PrimeStepF_closed (N := N) (x := x) ⟨h0, hxle⟩).symm))
    convert hq' using 1
    · rw [hlim]

lemma integral_chi8PrimeStepF (N : ℕ) :
    ∫ x in (0 : ℝ)..1, chi8PrimeStepF N x = chi8PrimeGroup N := by
  unfold chi8PrimeStepF chi8PrimeGroup
  have hI0 (k : ℕ) : IntervalIntegrable (fun x : ℝ => x ^ (8 * k)) MeasureTheory.volume 0 1 := by
    have hc : Continuous (fun x : ℝ => x ^ (8 * k)) := by fun_prop
    exact hc.intervalIntegrable 0 1
  have hI2 (k : ℕ) : IntervalIntegrable (fun x : ℝ => x ^ (8 * k + 2)) MeasureTheory.volume 0 1 := by
    have hc : Continuous (fun x : ℝ => x ^ (8 * k + 2)) := by fun_prop
    exact hc.intervalIntegrable 0 1
  have hI4 (k : ℕ) : IntervalIntegrable (fun x : ℝ => x ^ (8 * k + 4)) MeasureTheory.volume 0 1 := by
    have hc : Continuous (fun x : ℝ => x ^ (8 * k + 4)) := by fun_prop
    exact hc.intervalIntegrable 0 1
  have hI6 (k : ℕ) : IntervalIntegrable (fun x : ℝ => x ^ (8 * k + 6)) MeasureTheory.volume 0 1 := by
    have hc : Continuous (fun x : ℝ => x ^ (8 * k + 6)) := by fun_prop
    exact hc.intervalIntegrable 0 1
  rw [intervalIntegral.integral_finsetSum
    (fun k hk => (((hI0 k).add (hI2 k)).sub (hI4 k)).sub (hI6 k))]
  apply Finset.sum_congr rfl
  intro k hk
  unfold chi8PrimeGroupTerm
  rw [intervalIntegral.integral_sub (((hI0 k).add (hI2 k)).sub (hI4 k)) (hI6 k)]
  rw [intervalIntegral.integral_sub ((hI0 k).add (hI2 k)) (hI4 k)]
  rw [intervalIntegral.integral_add (hI0 k) (hI2 k)]
  rw [integral_pow_aux (8 * k), integral_pow_aux (8 * k + 2), integral_pow_aux (8 * k + 4),
    integral_pow_aux (8 * k + 6)]
  norm_num [Nat.cast_add, Nat.cast_mul]
  ring

lemma tendsto_integral_chi8PrimeStepF :
    Tendsto (fun N : ℕ => ∫ x in (0 : ℝ)..1, chi8PrimeStepF N x) atTop
      (𝓝 (∫ x in (0 : ℝ)..1, chi8PrimeLimitF x)) := by
  refine intervalIntegral.tendsto_integral_filter_of_dominated_convergence
      (μ := MeasureTheory.volume) (l := atTop) (F := fun N x => chi8PrimeStepF N x)
      (bound := fun _ : ℝ => 2) (f := chi8PrimeLimitF) ?_ ?_ ?_ ?_
  · refine Eventually.of_forall ?_
    intro N
    have hc : Continuous (chi8PrimeStepF N) := by
      unfold chi8PrimeStepF
      fun_prop
    exact hc.aestronglyMeasurable
  · refine Eventually.of_forall ?_
    intro N
    exact MeasureTheory.ae_of_all MeasureTheory.volume
      (fun x => fun hx =>
        chi8PrimeStepF_norm_le (N := N) (by
          simpa [Set.uIoc_of_le (show (0 : ℝ) ≤ 1 by norm_num)] using hx))
  · have hc : Continuous (fun _ : ℝ => (2 : ℝ)) := continuous_const
    exact hc.intervalIntegrable 0 1
  · exact MeasureTheory.ae_of_all MeasureTheory.volume
      (fun x => fun hx =>
        chi8PrimeStepF_tendsto_limit (by
          simpa [Set.uIoc_of_le (show (0 : ℝ) ≤ 1 by norm_num)] using hx))

lemma chi8PrimeGroup_tendsto :
    Tendsto chi8PrimeGroup atTop (𝓝 (Real.pi / (2 * Real.sqrt 2))) := by
  have h1 := tendsto_integral_chi8PrimeStepF
  have hval : (∫ x in (0 : ℝ)..1, chi8PrimeLimitF x) = Real.pi / (2 * Real.sqrt 2) := by
    have hcongr : ∫ x in (0 : ℝ)..1, chi8PrimeLimitF x = ∫ x in (0 : ℝ)..1, (1 + x ^ 2) / (1 + x ^ 4) := by
      exact intervalIntegral.integral_congr_Ioo_of_le (show (0 : ℝ) ≤ 1 by norm_num)
        (fun x hx => by simp [chi8PrimeLimitF, hx.2])
    rw [hcongr]
    exact integral_chi8Prime_value
  have h1' : Tendsto (fun N : ℕ => ∫ x in (0 : ℝ)..1, chi8PrimeStepF N x) atTop
      (𝓝 (Real.pi / (2 * Real.sqrt 2))) := by
    simpa [hval] using h1
  exact h1'.congr' (Eventually.of_forall (fun N => integral_chi8PrimeStepF N))

-- ordered partial sums reduce to the grouped series, plus a lim-vanishing correction
lemma chi8PrimePartial_eight_mul (M : ℕ) : chi8PrimePartial (8 * M) = chi8PrimeGroup M := by
  induction M with
  | zero => simp [chi8PrimePartial, chi8PrimeGroup]
  | succ M ih =>
      rw [show 8 * (M + 1) = 8 * M + 8 by omega]
      unfold chi8PrimePartial
      rw [Finset.sum_range_add]
      have hb1 : chi8PrimeZ (8 * M + 1) / ((8 * M + 1 : ℕ) : ℝ) = 1 / (8 * (M : ℝ) + 1) := by
        have hc : ((8 * M + 1 : ℕ) : ℝ) = 8 * (M : ℝ) + 1 := by norm_num [Nat.cast_add, Nat.cast_mul]
        rw [chi8PrimeZ_eight_mul_add_one M, hc]
      have hb3 : chi8PrimeZ (8 * M + 3) / ((8 * M + 3 : ℕ) : ℝ) = 1 / (8 * (M : ℝ) + 3) := by
        have hc : ((8 * M + 3 : ℕ) : ℝ) = 8 * (M : ℝ) + 3 := by norm_num [Nat.cast_add, Nat.cast_mul]
        rw [chi8PrimeZ_eight_mul_add_three M, hc]
      have hb5 : chi8PrimeZ (8 * M + 5) / ((8 * M + 5 : ℕ) : ℝ) = -(1 / (8 * (M : ℝ) + 5)) := by
        have hc : ((8 * M + 5 : ℕ) : ℝ) = 8 * (M : ℝ) + 5 := by norm_num [Nat.cast_add, Nat.cast_mul]
        rw [chi8PrimeZ_eight_mul_add_five M, hc, neg_div]
      have hb7 : chi8PrimeZ (8 * M + 7) / ((8 * M + 7 : ℕ) : ℝ) = -(1 / (8 * (M : ℝ) + 7)) := by
        have hc : ((8 * M + 7 : ℕ) : ℝ) = 8 * (M : ℝ) + 7 := by norm_num [Nat.cast_add, Nat.cast_mul]
        rw [chi8PrimeZ_eight_mul_add_seven M, hc, neg_div]
      have hb0 : chi8PrimeZ (8 * M + 0) / ((8 * M + 0 : ℕ) : ℝ) = 0 := by
        rw [chi8PrimeZ_eight_mul_add_zero M]
        simp
      have hb2 : chi8PrimeZ (8 * M + 2) / ((8 * M + 2 : ℕ) : ℝ) = 0 := by
        rw [chi8PrimeZ_eight_mul_add_two M]
        simp
      have hb4 : chi8PrimeZ (8 * M + 4) / ((8 * M + 4 : ℕ) : ℝ) = 0 := by
        rw [chi8PrimeZ_eight_mul_add_four M]
        simp
      have hb6 : chi8PrimeZ (8 * M + 6) / ((8 * M + 6 : ℕ) : ℝ) = 0 := by
        rw [chi8PrimeZ_eight_mul_add_six M]
        simp
      have hblock : (∑ j ∈ Finset.range 8, chi8PrimeZ (8 * M + j) / ((8 * M + j : ℕ) : ℝ))
          = chi8PrimeGroupTerm M := by
        unfold chi8PrimeGroupTerm
        rw [Finset.sum_range_succ, Finset.sum_range_succ, Finset.sum_range_succ,
          Finset.sum_range_succ, Finset.sum_range_succ, Finset.sum_range_succ,
          Finset.sum_range_succ, Finset.sum_range_succ]
        rw [hb7, hb6, hb5, hb4, hb3, hb2, hb1, hb0]
        ring
      rw [hblock]
      have hg : chi8PrimeGroup (M + 1) = chi8PrimeGroup M + chi8PrimeGroupTerm M := by
        unfold chi8PrimeGroup
        rw [Finset.sum_range_succ]
      rw [hg]
      rw [← ih]
      rfl

noncomputable def chi8PrimeTurnTail (N : ℕ) : ℝ :=
  ∑ j ∈ Finset.range (N % 8), chi8PrimeZ (8 * (N / 8) + j) / ((8 * (N / 8) + j : ℕ) : ℝ)

lemma chi8PrimePartial_split (N : ℕ) :
    chi8PrimePartial N = chi8PrimePartial (8 * (N / 8)) + chi8PrimeTurnTail N := by
  unfold chi8PrimePartial chi8PrimeTurnTail
  conv_lhs => rw [← show (8 * (N / 8) + N % 8) = N by omega]
  rw [Finset.sum_range_add]

lemma chi8PrimeTurnTail_bound {N : ℕ} :
    ‖chi8PrimeTurnTail N‖ ≤ (8 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ) := by
  unfold chi8PrimeTurnTail
  have hkpos : (0 : ℕ) < 8 * (N / 8) + 1 := by omega
  have hdpos : (0 : ℝ) < ((8 * (N / 8) + 1 : ℕ) : ℝ) := by exact_mod_cast hkpos
  have hc : 0 ≤ (1 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ) := div_nonneg (by norm_num) hdpos.le
  have hb : ∑ j ∈ Finset.range (N % 8),
        ‖chi8PrimeZ (8 * (N / 8) + j) / ((8 * (N / 8) + j : ℕ) : ℝ)‖
      ≤ ∑ j ∈ Finset.range (N % 8), (1 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ) := by
    refine Finset.sum_le_sum ?_
    intro j hjin
    have hj8 : j < 8 := lt_of_lt_of_le (Finset.mem_range.mp hjin) (le_of_lt (Nat.mod_lt N (by norm_num : 0 < 8)))
    have hjr : j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 ∨ j = 5 ∨ j = 6 ∨ j = 7 := by omega
    rcases hjr with h0 | h1 | h2 | h3 | h4 | h5 | h6 | h7
    · subst h0
      have hz : chi8PrimeZ (8 * (N / 8) + 0) = 0 := chi8PrimeZ_eight_mul_add_zero (N / 8)
      rw [hz, zero_div]
      simpa using hc
    · subst h1
      have hz : chi8PrimeZ (8 * (N / 8) + 1) = 1 := chi8PrimeZ_eight_mul_add_one (N / 8)
      rw [hz]
      have hnorm : ‖(1 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ)‖ = (1 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ) := by
        rw [Real.norm_eq_abs, abs_of_pos (div_pos (by norm_num) hdpos)]
      rw [hnorm]
    · subst h2
      have hz : chi8PrimeZ (8 * (N / 8) + 2) = 0 := chi8PrimeZ_eight_mul_add_two (N / 8)
      rw [hz, zero_div]
      simpa using hc
    · subst h3
      have hk3 : (0 : ℕ) < 8 * (N / 8) + 3 := by omega
      have hd3 : (0 : ℝ) < ((8 * (N / 8) + 3 : ℕ) : ℝ) := by exact_mod_cast hk3
      have hz : chi8PrimeZ (8 * (N / 8) + 3) = 1 := chi8PrimeZ_eight_mul_add_three (N / 8)
      rw [hz]
      have hnorm : ‖(1 : ℝ) / ((8 * (N / 8) + 3 : ℕ) : ℝ)‖ = (1 : ℝ) / ((8 * (N / 8) + 3 : ℕ) : ℝ) := by
        rw [Real.norm_eq_abs, abs_of_pos (div_pos (by norm_num) hd3)]
      rw [hnorm]
      have hleD : ((8 * (N / 8) + 1 : ℕ) : ℝ) ≤ ((8 * (N / 8) + 3 : ℕ) : ℝ) := by
        exact_mod_cast (by omega : (8 * (N / 8) + 1 : ℕ) ≤ 8 * (N / 8) + 3)
      have hide : ((8 * (N / 8) + 3 : ℕ) : ℝ)⁻¹ ≤ ((8 * (N / 8) + 1 : ℕ) : ℝ)⁻¹ := by
        rw [inv_le_inv₀ hd3 hdpos]
        exact hleD
      simpa [one_div] using hide
    · subst h4
      have hz : chi8PrimeZ (8 * (N / 8) + 4) = 0 := chi8PrimeZ_eight_mul_add_four (N / 8)
      rw [hz, zero_div]
      simpa using hc
    · subst h5
      have hk5 : (0 : ℕ) < 8 * (N / 8) + 5 := by omega
      have hd5 : (0 : ℝ) < ((8 * (N / 8) + 5 : ℕ) : ℝ) := by exact_mod_cast hk5
      have hz : chi8PrimeZ (8 * (N / 8) + 5) = -1 := chi8PrimeZ_eight_mul_add_five (N / 8)
      rw [hz]
      have hnorm : ‖(-(1 : ℝ)) / ((8 * (N / 8) + 5 : ℕ) : ℝ)‖ = (1 : ℝ) / ((8 * (N / 8) + 5 : ℕ) : ℝ) := by
        rw [neg_div]
        rw [Real.norm_eq_abs, abs_neg, abs_of_pos (div_pos (by norm_num) hd5)]
      rw [hnorm]
      have hleD : ((8 * (N / 8) + 1 : ℕ) : ℝ) ≤ ((8 * (N / 8) + 5 : ℕ) : ℝ) := by
        exact_mod_cast (by omega : (8 * (N / 8) + 1 : ℕ) ≤ 8 * (N / 8) + 5)
      have hide : ((8 * (N / 8) + 5 : ℕ) : ℝ)⁻¹ ≤ ((8 * (N / 8) + 1 : ℕ) : ℝ)⁻¹ := by
        rw [inv_le_inv₀ hd5 hdpos]
        exact hleD
      simpa [one_div] using hide
    · subst h6
      have hz : chi8PrimeZ (8 * (N / 8) + 6) = 0 := chi8PrimeZ_eight_mul_add_six (N / 8)
      rw [hz, zero_div]
      simpa using hc
    · subst h7
      have hk7 : (0 : ℕ) < 8 * (N / 8) + 7 := by omega
      have hd7 : (0 : ℝ) < ((8 * (N / 8) + 7 : ℕ) : ℝ) := by exact_mod_cast hk7
      have hz : chi8PrimeZ (8 * (N / 8) + 7) = -1 := chi8PrimeZ_eight_mul_add_seven (N / 8)
      rw [hz]
      have hnorm : ‖(-(1 : ℝ)) / ((8 * (N / 8) + 7 : ℕ) : ℝ)‖ = (1 : ℝ) / ((8 * (N / 8) + 7 : ℕ) : ℝ) := by
        rw [neg_div]
        rw [Real.norm_eq_abs, abs_neg, abs_of_pos (div_pos (by norm_num) hd7)]
      rw [hnorm]
      have hleD : ((8 * (N / 8) + 1 : ℕ) : ℝ) ≤ ((8 * (N / 8) + 7 : ℕ) : ℝ) := by
        exact_mod_cast (by omega : (8 * (N / 8) + 1 : ℕ) ≤ 8 * (N / 8) + 7)
      have hide : ((8 * (N / 8) + 7 : ℕ) : ℝ)⁻¹ ≤ ((8 * (N / 8) + 1 : ℕ) : ℝ)⁻¹ := by
        rw [inv_le_inv₀ hd7 hdpos]
        exact hleD
      simpa [one_div] using hide
  have hwell : ‖chi8PrimeTurnTail N‖
      ≤ ∑ j ∈ Finset.range (N % 8), (1 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ) := by
    calc
      ‖chi8PrimeTurnTail N‖
          = ‖∑ j ∈ Finset.range (N % 8), chi8PrimeZ (8 * (N / 8) + j) / ((8 * (N / 8) + j : ℕ) : ℝ)‖ := rfl
      _ ≤ ∑ j ∈ Finset.range (N % 8), ‖chi8PrimeZ (8 * (N / 8) + j) / ((8 * (N / 8) + j : ℕ) : ℝ)‖ :=
          norm_sum_le (Finset.range (N % 8))
            (fun j : ℕ => chi8PrimeZ (8 * (N / 8) + j) / ((8 * (N / 8) + j : ℕ) : ℝ))
      _ ≤ ∑ j ∈ Finset.range (N % 8), (1 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ) := hb
  have hconst : ∑ j ∈ Finset.range (N % 8), (1 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ)
      ≤ (8 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ) := by
    have hcard : (N % 8 : ℕ) ≤ 8 := le_of_lt (Nat.mod_lt N (by norm_num : 0 < 8))
    calc
      (∑ j ∈ Finset.range (N % 8), (1 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ))
          = ((N % 8 : ℕ) : ℝ) * ((1 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ)) := by
            rw [Finset.sum_const, nsmul_eq_mul, Finset.card_range]
      _ ≤ (8 : ℝ) * ((1 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ)) := by
            exact mul_le_mul_of_nonneg_right (by exact_mod_cast hcard) hc
      _ = (8 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ) := by
            rw [mul_one_div]
  exact le_trans hwell hconst

lemma chi8PrimeTurnTail_tendsto : Tendsto chi8PrimeTurnTail atTop (𝓝 (0 : ℝ)) := by
  have hmd : Tendsto (fun N : ℕ => (8 * (N / 8) + 1 : ℕ)) atTop atTop := by
    rw [tendsto_atTop_atTop]
    intro b
    refine ⟨8 * (b + 1), ?_⟩
    intro N hN
    omega
  have hcast : Tendsto (fun N : ℕ => (((8 * (N / 8) + 1 : ℕ) : ℝ))) atTop atTop :=
    tendsto_natCast_atTop_atTop.comp hmd
  have hinv : Tendsto (fun N : ℕ => (((8 * (N / 8) + 1 : ℕ) : ℝ)⁻¹)) atTop (𝓝 (0 : ℝ)) :=
    tendsto_inv_atTop_zero.comp hcast
  have hb : Tendsto (fun N : ℕ => (1 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ)) atTop (𝓝 (0 : ℝ)) := by
    exact hinv.congr' (Eventually.of_forall (fun N => by rw [← one_div]))
  have hb8 : Tendsto (fun N : ℕ => (8 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ)) atTop (𝓝 (0 : ℝ)) := by
    have hb8m : Tendsto (fun N : ℕ => (8 : ℝ) * (1 / ((8 * (N / 8) + 1 : ℕ) : ℝ))) atTop (𝓝 (0 : ℝ)) := by
      simpa using hb.const_mul (8 : ℝ)
    exact hb8m.congr' (Eventually.of_forall (fun N => by rw [mul_one_div]))
  have hneg : Tendsto (fun N : ℕ => -((8 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ))) atTop (𝓝 (0 : ℝ)) := by
    simpa using hb8.neg
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le hneg hb8 ?_ ?_
  · intro N
    have hbN : |chi8PrimeTurnTail N| ≤ (8 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ) := by
      simpa [Real.norm_eq_abs] using chi8PrimeTurnTail_bound (N := N)
    exact (abs_le.mp hbN).1
  · intro N
    have hbN : |chi8PrimeTurnTail N| ≤ (8 : ℝ) / ((8 * (N / 8) + 1 : ℕ) : ℝ) := by
      simpa [Real.norm_eq_abs] using chi8PrimeTurnTail_bound (N := N)
    exact (abs_le.mp hbN).2

lemma chi8PrimePartial_tendsto :
    Tendsto chi8PrimePartial atTop (𝓝 (Real.pi / (2 * Real.sqrt 2))) := by
  have hg : Tendsto (fun M : ℕ => chi8PrimePartial (8 * M)) atTop (𝓝 (Real.pi / (2 * Real.sqrt 2))) :=
    chi8PrimeGroup_tendsto.congr' (Eventually.of_forall (fun M => (chi8PrimePartial_eight_mul M).symm))
  have hq : Tendsto (fun N : ℕ => N / 8) atTop atTop := by
    rw [tendsto_atTop_atTop]
    intro b
    refine ⟨8 * (b + 1), ?_⟩
    intro N hN
    omega
  have hmain : Tendsto (fun N : ℕ => chi8PrimePartial (8 * (N / 8))) atTop
      (𝓝 (Real.pi / (2 * Real.sqrt 2))) :=
    hg.comp hq
  have htail : Tendsto (fun N : ℕ => chi8PrimePartial N - chi8PrimePartial (8 * (N / 8))) atTop (𝓝 (0 : ℝ)) :=
    chi8PrimeTurnTail_tendsto.congr' (Eventually.of_forall (fun N => by
      change chi8PrimeTurnTail N = chi8PrimePartial N - chi8PrimePartial (8 * (N / 8))
      rw [chi8PrimePartial_split]
      ring))
  have hsum := hmain.add htail
  convert hsum using 1
  · funext N
    ring
  · simp

/-- The `χ₈'` Dirichlet series at `s = 1` (`Σ χ₈'(n)/n`): its ordered partial sums in `ℝ`
coincide with the ordered partial sums of the mod-8 pattern `chi8PrimeZ n / n`. -/
lemma chi8Prime_series_partial_real (N : ℕ) :
    (∑ n ∈ Finset.range N, ((ZMod.χ₈' n : ℤ) : ℝ) / (n : ℝ)) = chi8PrimePartial N := by
  unfold chi8PrimePartial
  refine Finset.sum_congr rfl ?_
  intro n hn
  rw [chi8PrimeZ_eq_χ₈' n]

/-- `L(1, χ₈') = π/(2√2)` as a Dirichlet-series limit (in `ℝ`): the ordered partial sums
`Σ_{n<N} χ₈'(n)/n` tend to `π/(2√2)`. -/
lemma chi8Prime_series_real_pi_div_two_sqrt_two :
    Tendsto (fun N : ℕ => ∑ n ∈ Finset.range N, ((ZMod.χ₈' n : ℤ) : ℝ) / (n : ℝ)) atTop
      (𝓝 (Real.pi / (2 * Real.sqrt 2) : ℝ)) := by
  convert chi8PrimePartial_tendsto using 1
  funext N
  rw [chi8Prime_series_partial_real]

lemma chi8Primeℂ_term_eq (n : ℕ) :
    (algebraMap ℝ ℂ) (((ZMod.χ₈' n : ℤ) : ℝ) / (n : ℝ)) = (χ₈'ℂ n) / (n : ℂ) := by
  have hnum : (algebraMap ℝ ℂ) (((ZMod.χ₈' n : ℤ) : ℝ)) = ((ZMod.χ₈' n : ℤ) : ℂ) := by norm_num
  have hnum2 : ((ZMod.χ₈' n : ℤ) : ℂ) = (χ₈'ℂ n) := by simp [χ₈'ℂ]
  have hden : (algebraMap ℝ ℂ) (n : ℝ) = (n : ℂ) := by rfl
  rw [map_div₀, hnum, hnum2, hden]

lemma chi8Prime_series_eq_real (N : ℕ) :
    (algebraMap ℝ ℂ) (∑ n ∈ Finset.range N, (((ZMod.χ₈' n : ℤ) : ℝ) / (n : ℝ)))
      = ∑ n ∈ Finset.range N, (χ₈'ℂ n) / (n : ℂ) := by
  calc
    (algebraMap ℝ ℂ) (∑ n ∈ Finset.range N, (((ZMod.χ₈' n : ℤ) : ℝ) / (n : ℝ)))
        = ∑ n ∈ Finset.range N, (algebraMap ℝ ℂ) (((ZMod.χ₈' n : ℤ) : ℝ) / (n : ℝ)) :=
          map_sum (algebraMap ℝ ℂ) (fun n : ℕ => ((ZMod.χ₈' n : ℤ) : ℝ) / (n : ℝ)) (Finset.range N)
    _ = ∑ n ∈ Finset.range N, (χ₈'ℂ n) / (n : ℂ) :=
          Finset.sum_congr rfl (by intro n hn; exact chi8Primeℂ_term_eq n)

/-- The `L(1, χ₈') = π/(2√2)` special value as a Dirichlet-series limit: the ordered partial
sums `Σ_{n<N} χ₈'(n)/n` (in `ℂ`) tend to `π/(2√2)`. -/
lemma chi8Prime_series_pi_div_two_sqrt_two :
    Tendsto (fun N : ℕ => ∑ n ∈ Finset.range N, (χ₈'ℂ n) / (n : ℂ)) atTop
      (𝓝 (Real.pi / (2 * Real.sqrt 2) : ℂ)) := by
  have hc : Tendsto (RCLike.ofReal ∘ (fun N : ℕ => ∑ n ∈ Finset.range N, ((ZMod.χ₈' n : ℤ) : ℝ) / (n : ℝ))) atTop
      (𝓝 (RCLike.ofReal (K := ℂ) (Real.pi / (2 * Real.sqrt 2) : ℝ))) :=
    RCLike.continuous_ofReal.continuousAt.tendsto.comp chi8Prime_series_real_pi_div_two_sqrt_two
  have hpi : 𝓝 (RCLike.ofReal (K := ℂ) (Real.pi / (2 * Real.sqrt 2) : ℝ)) =
      𝓝 (Real.pi / (2 * Real.sqrt 2) : ℂ) := by
    congr 1
    change (algebraMap ℝ ℂ) (Real.pi / (2 * Real.sqrt 2)) =
      (Real.pi : ℂ) / ((2 : ℂ) * (Real.sqrt 2 : ℂ))
    rw [map_div₀, map_mul]
    simp
  have hobs : ∀ᶠ N in atTop,
      (RCLike.ofReal ∘ (fun N : ℕ => ∑ n ∈ Finset.range N, ((ZMod.χ₈' n : ℤ) : ℝ) / (n : ℝ))) N =
        ∑ n ∈ Finset.range N, (χ₈'ℂ n) / (n : ℂ) := by
    apply Filter.Eventually.of_forall
    intro N
    change (algebraMap ℝ ℂ) (∑ n ∈ Finset.range N, (((ZMod.χ₈' n : ℤ) : ℝ) / (n : ℝ))) =
      ∑ n ∈ Finset.range N, (χ₈'ℂ n) / (n : ℂ)
    exact chi8Prime_series_eq_real N
  simpa [hpi] using hc.congr' hobs

end PunoTwin.Dirichlet