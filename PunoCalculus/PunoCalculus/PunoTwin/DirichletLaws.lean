import Mathlib.NumberTheory.LSeries.DirichletContinuation
import Mathlib.NumberTheory.LSeries.HurwitzZetaValues
import Mathlib.NumberTheory.EulerProduct.DirichletLSeries
import Mathlib.NumberTheory.LSeries.Nonvanishing
import Mathlib.NumberTheory.Bernoulli
import Mathlib.Data.Nat.Prime.Defs
import Mathlib.NumberTheory.LegendreSymbol.ZModChar
import Mathlib.NumberTheory.SumTwoSquares

open DirichletCharacter HurwitzZeta
open scoped Real BigOperators
open Nat

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
    (`chi4_rootNumber`), closing the conductor-4 character register.

Everything below is fully proved.  The remaining — exact transcendental
identities such as `L(2, χ₋₄) = Catalans' G`, or any claim that the
aperiodic lattice of the *discrete* twin reproduces these laws beyond
the verified instances — is not claimed here.
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

lemma apply_three : χ₈ℂ 3 = -1 := by norm_num [χ₈ℂ]
lemma apply_five : χ₈ℂ 5 = -1 := by norm_num [χ₈ℂ]
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

lemma apply_five : χ₈'ℂ 5 = -1 := by norm_num [χ₈'ℂ]
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

end PunoTwin.Dirichlet