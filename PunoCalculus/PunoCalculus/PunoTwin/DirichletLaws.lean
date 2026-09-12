import Mathlib.NumberTheory.LSeries.DirichletContinuation
import Mathlib.NumberTheory.LSeries.HurwitzZetaValues
import Mathlib.NumberTheory.EulerProduct.DirichletLSeries
import Mathlib.NumberTheory.Bernoulli
import Mathlib.Data.Nat.Prime.Defs
import Mathlib.NumberTheory.LegendreSymbol.ZModChar

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
  * **von Staudt–Clausen**: `B₁₆ + ∑_{p−1 | 16} 1/p` is an integer,
    and the Fermat-spike lattice `p = 2^(2^j)+1 ↔ 2^(2^j−1) | k`
    with instances `5 ↔ 2|k`, `17 ↔ 8|k`, `257 ↔ 128|k`, `65537 ↔ 2^15|k`
    (`vonStaudt_B16`, `spike_law`, `spike_*`);  the `fermat_bridge`
    closes the loop to the MPOperator window denominator: at
    `a = 2^(2^k−1)`, `1 + 4a² = 2^(2^(k+1)) + 1` (so `a = 128` → `65537`).

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
`2^(2^j - 1) | k`.

Concrete instances (R57-60 motif): `5 ↔ 2 | k`, `17 ↔ 8 | k`,
`257 ↔ 128 | k`. -/
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

end PunoTwin.Dirichlet