import Mathlib

/-!
# The section 9 / 16 Hankel criterion: the quadratic-form identity, and the
# sufficiency direction, formalised (Lean 4, Mathlib)

Machine-checked content behind two claims that `experiments/rh_widder_hankel_h3.py`
records only as numerical residuals and that `rh_widder_hankel_h2.py` uses as
the criterion's justification.

For a finite multiset of transformed zeros `q` and a real coefficient vector
`c = (c_0, ..., c_m)`, record section 9 builds the shifted moments

    M_k = Σ_j q_j^(k+1)

and the Hankel matrix `H = [M_{i+j}]_{i,j=0}^{m}`, so the quantity section 16
needs is the quadratic form `cᵀHc`.  Writing `P(u) = Σ_i c_i u^i` for the
polynomial with coefficients `c`, the content of H3c is the exact identity

    cᵀHc = Σ_j q_j P(q_j)^2,

verified there to `1e-40` on finite multisets.  Under RH every `q_j` is real
and non-negative, so each summand on the right is a real square times a
non-negative weight and the form is non-negative.  That is the *sufficiency*
half of record section 9's criterion: `RH ⟹ cᵀHc ≥ 0`.

## What is proved here, and what is not

Proved, all of it algebra over `R` and `C`:

1. `polyEval_sq`, `quadForm_eq`, `quadFormR_eq`: the identity
   `cᵀHc = Σ_j q_j P(q_j)^2`, for arbitrary complex atoms and arbitrary real
   `c`, and its real version.
2. `quadFormR_nonneg`: if every atom is a non-negative real then the form is
   non-negative.
3. `quadForm_ofReal` and `re_quadForm_of_real`: the complex form built from
   real atoms *equals* the real form, so (2) is a statement about the
   `C`-valued criterion the experiments build, not a weakened surrogate.

Not proved, and deliberately so:

* The **converse**, that `cᵀHc ≥ 0` for all `c`, all orders and all `x > 0`
  forces the atoms to be real.  That is the direction that would settle RH,
  and record section 27 identifies it as exactly the missing prime-side step.
  Nothing here assumes it.
* Positivity for the *actual* zeta spectrum.  `quadFormR_nonneg` is a theorem
  about an arbitrary finite multiset of non-negative reals; instantiating it
  at the zeta zeros requires RH, which is what is being sought.

So this file certifies that the criterion is *sound* -- a negative quadratic
form really would be a genuine obstruction -- and pins the algebra the
experiments measure.  It contributes nothing toward proving the form is
positive for zeta.  The gap above, not this file, is the state of the art.
-/

namespace PunoCalculus.RH

variable {n m : ℕ}

/-- The shifted moment sequence `M_k = Σ_j q_j^(k+1)` of record section 9. -/
noncomputable def M (qs : Fin n → ℂ) (k : ℕ) : ℂ :=
  ∑ j : Fin n, qs j ^ (k + 1)

/-- The polynomial `P(u) = Σ_i c_i u^i` whose coefficients are the vector `c`. -/
noncomputable def polyEval (c : Fin (m + 1) → ℝ) (u : ℂ) : ℂ :=
  ∑ i : Fin (m + 1), (c i : ℂ) * u ^ (i : ℕ)

/-- `cᵀHc` for `H = [M_{i+j}]_{i,j≤m}`, the object record section 27 needs. -/
noncomputable def quadForm (qs : Fin n → ℂ) (c : Fin (m + 1) → ℝ) : ℂ :=
  ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
    ((c i : ℂ) * (c j : ℂ)) * M qs ((i : ℕ) + (j : ℕ))

/-- Real version of `polyEval`. -/
noncomputable def polyEvalR (c : Fin (m + 1) → ℝ) (u : ℝ) : ℝ :=
  ∑ i : Fin (m + 1), c i * u ^ (i : ℕ)

/-- Real version of `M`. -/
noncomputable def MR (qs : Fin n → ℝ) (k : ℕ) : ℝ :=
  ∑ j : Fin n, qs j ^ (k + 1)

/-- Real version of `quadForm`. -/
noncomputable def quadFormR (qs : Fin n → ℝ) (c : Fin (m + 1) → ℝ) : ℝ :=
  ∑ i : Fin (m + 1), ∑ j : Fin (m + 1), c i * c j * MR qs ((i : ℕ) + (j : ℕ))

/-- Commuting three nested sums over `C`.  Proved separately so the users
below can apply it by `exact` instead of leaving `simp_rw` to guess rewrite
directions. -/
theorem three_sum_comm (f : Fin (m + 1) → Fin (m + 1) → Fin n → ℂ) :
    (∑ i : Fin (m + 1), ∑ j : Fin (m + 1), ∑ k : Fin n, f i j k) =
      ∑ k : Fin n, ∑ i : Fin (m + 1), ∑ j : Fin (m + 1), f i j k := by
  calc ∑ i : Fin (m + 1), ∑ j : Fin (m + 1), ∑ k : Fin n, f i j k
      = ∑ i : Fin (m + 1), ∑ k : Fin n, ∑ j : Fin (m + 1), f i j k := by
        congr 1
        funext i
        exact Finset.sum_comm
    _ = ∑ k : Fin n, ∑ i : Fin (m + 1), ∑ j : Fin (m + 1), f i j k := Finset.sum_comm

/-- Real version of `three_sum_comm`. -/
theorem three_sum_commR (f : Fin (m + 1) → Fin (m + 1) → Fin n → ℝ) :
    (∑ i : Fin (m + 1), ∑ j : Fin (m + 1), ∑ k : Fin n, f i j k) =
      ∑ k : Fin n, ∑ i : Fin (m + 1), ∑ j : Fin (m + 1), f i j k := by
  calc ∑ i : Fin (m + 1), ∑ j : Fin (m + 1), ∑ k : Fin n, f i j k
      = ∑ i : Fin (m + 1), ∑ k : Fin n, ∑ j : Fin (m + 1), f i j k := by
        congr 1
        funext i
        exact Finset.sum_comm
    _ = ∑ k : Fin n, ∑ i : Fin (m + 1), ∑ j : Fin (m + 1), f i j k := Finset.sum_comm

/-- `P(u)^2 = Σ_{i,j} c_i c_j u^(i+j)`: the square of the section 9 polynomial
expands into exactly the double sum that `cᵀHc` uses. -/
theorem polyEval_sq (c : Fin (m + 1) → ℝ) (u : ℂ) :
    (polyEval c u) ^ 2 =
      ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
        ((c i : ℂ) * (c j : ℂ)) * u ^ ((i : ℕ) + (j : ℕ)) := by
  have hsq : (∑ i : Fin (m + 1), (c i : ℂ) * u ^ (i : ℕ)) *
      (∑ j : Fin (m + 1), (c j : ℂ) * u ^ (j : ℕ)) =
      ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
        ((c i : ℂ) * (c j : ℂ)) * u ^ ((i : ℕ) + (j : ℕ)) := by
    calc (∑ i : Fin (m + 1), (c i : ℂ) * u ^ (i : ℕ)) *
        (∑ j : Fin (m + 1), (c j : ℂ) * u ^ (j : ℕ))
      = ∑ i : Fin (m + 1), ((c i : ℂ) * u ^ (i : ℕ)) *
          (∑ j : Fin (m + 1), (c j : ℂ) * u ^ (j : ℕ)) :=
        Finset.sum_mul Finset.univ _ _
      _ = ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
          ((c i : ℂ) * u ^ (i : ℕ)) * ((c j : ℂ) * u ^ (j : ℕ)) :=
        Finset.sum_congr rfl fun _i _ => Finset.mul_sum Finset.univ _ _
      _ = ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
          ((c i : ℂ) * (c j : ℂ)) * u ^ ((i : ℕ) + (j : ℕ)) := by
        refine Finset.sum_congr rfl fun i _ => ?_
        refine Finset.sum_congr rfl fun j _ => ?_
        ring
  unfold polyEval
  rw [pow_two]
  exact hsq

/-- Real version of `polyEval_sq`. -/
theorem polyEvalR_sq (c : Fin (m + 1) → ℝ) (u : ℝ) :
    (polyEvalR c u) ^ 2 =
      ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
        (c i * c j) * u ^ ((i : ℕ) + (j : ℕ)) := by
  have hsq : (∑ i : Fin (m + 1), c i * u ^ (i : ℕ)) *
      (∑ j : Fin (m + 1), c j * u ^ (j : ℕ)) =
      ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
        (c i * c j) * u ^ ((i : ℕ) + (j : ℕ)) := by
    calc (∑ i : Fin (m + 1), c i * u ^ (i : ℕ)) *
        (∑ j : Fin (m + 1), c j * u ^ (j : ℕ))
      = ∑ i : Fin (m + 1), (c i * u ^ (i : ℕ)) *
          (∑ j : Fin (m + 1), c j * u ^ (j : ℕ)) :=
        Finset.sum_mul Finset.univ _ _
      _ = ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
          (c i * u ^ (i : ℕ)) * (c j * u ^ (j : ℕ)) :=
        Finset.sum_congr rfl fun _i _ => Finset.mul_sum Finset.univ _ _
      _ = ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
          (c i * c j) * u ^ ((i : ℕ) + (j : ℕ)) := by
        refine Finset.sum_congr rfl fun i _ => ?_
        refine Finset.sum_congr rfl fun j _ => ?_
        ring
  unfold polyEvalR
  rw [pow_two]
  exact hsq

/-- Factoring one power of `u` out of the double sum.  This is the single place
the `+1` shift of the moments `M_{i+j+1}` is consumed, and it is where the
Hankel form turns into the squares `P(q)^2` of `quadForm_eq`. -/
private theorem double_sum_shift (u : ℂ) (a : Fin (m + 1) → ℂ) :
    (∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
        (a i * a j) * u ^ ((i : ℕ) + (j : ℕ) + 1)) =
      u * ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
        (a i * a j) * u ^ ((i : ℕ) + (j : ℕ)) := by
  have h : ∀ i j : Fin (m + 1),
      (a i * a j) * u ^ ((i : ℕ) + (j : ℕ) + 1) =
        u * ((a i * a j) * u ^ ((i : ℕ) + (j : ℕ))) := by
    intro i j
    rw [show (i : ℕ) + (j : ℕ) + 1 = ((i : ℕ) + (j : ℕ)) + 1 by omega, pow_succ]
    ring
  simp_rw [h]
  calc (∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
          u * ((a i * a j) * u ^ ((i : ℕ) + (j : ℕ))))
      = ∑ i : Fin (m + 1), u *
          ∑ j : Fin (m + 1), (a i * a j) * u ^ ((i : ℕ) + (j : ℕ)) :=
        Finset.sum_congr rfl fun _i _ => (Finset.mul_sum Finset.univ _ _).symm
    _ = u * ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
          (a i * a j) * u ^ ((i : ℕ) + (j : ℕ)) :=
        (Finset.mul_sum Finset.univ _ _).symm

/-- Real analogue of `double_sum_shift`. -/
private theorem double_sum_shiftR (u : ℝ) (a : Fin (m + 1) → ℝ) :
    (∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
        (a i * a j) * u ^ ((i : ℕ) + (j : ℕ) + 1)) =
      u * ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
        (a i * a j) * u ^ ((i : ℕ) + (j : ℕ)) := by
  have h : ∀ i j : Fin (m + 1),
      (a i * a j) * u ^ ((i : ℕ) + (j : ℕ) + 1) =
        u * ((a i * a j) * u ^ ((i : ℕ) + (j : ℕ))) := by
    intro i j
    rw [show (i : ℕ) + (j : ℕ) + 1 = ((i : ℕ) + (j : ℕ)) + 1 by omega, pow_succ]
    ring
  simp_rw [h]
  calc (∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
          u * ((a i * a j) * u ^ ((i : ℕ) + (j : ℕ))))
      = ∑ i : Fin (m + 1), u *
          ∑ j : Fin (m + 1), (a i * a j) * u ^ ((i : ℕ) + (j : ℕ)) :=
        Finset.sum_congr rfl fun _i _ => (Finset.mul_sum Finset.univ _ _).symm
    _ = u * ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
          (a i * a j) * u ^ ((i : ℕ) + (j : ℕ)) :=
        (Finset.mul_sum Finset.univ _ _).symm

/-- H3c, exactly: the section 16 quadratic form is the atom-weighted sum of
squares `cᵀHc = Σ_j q_j P(q_j)^2`.

No hypothesis on the atoms -- they may be arbitrary complex numbers, which is
what makes this an identity rather than an inequality.
`rh_widder_hankel_h3.py` verifies the same statement numerically to `1e-40`. -/
theorem quadForm_eq (qs : Fin n → ℂ) (c : Fin (m + 1) → ℝ) :
    quadForm qs c = ∑ k : Fin n, qs k * (polyEval c (qs k)) ^ 2 := by
  calc quadForm qs c
      = ∑ i : Fin (m + 1), ∑ j : Fin (m + 1), ∑ k : Fin n,
          ((c i : ℂ) * (c j : ℂ)) * qs k ^ ((i : ℕ) + (j : ℕ) + 1) := by
          unfold quadForm M
          refine Finset.sum_congr rfl fun i _ => ?_
          refine Finset.sum_congr rfl fun j _ => ?_
          exact Finset.mul_sum Finset.univ
            (fun k => qs k ^ (((i : ℕ) + (j : ℕ)) + 1)) _
    _ = ∑ k : Fin n, ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
          ((c i : ℂ) * (c j : ℂ)) * qs k ^ ((i : ℕ) + (j : ℕ) + 1) :=
      three_sum_comm fun i j k => ((c i : ℂ) * (c j : ℂ)) * qs k ^ ((i : ℕ) + (j : ℕ) + 1)
    _ = ∑ k : Fin n, qs k * (polyEval c (qs k)) ^ 2 := by
          refine Finset.sum_congr rfl fun k _ => ?_
          rw [double_sum_shift (qs k) fun i => (c i : ℂ), polyEval_sq]

/-- The real form satisfies the same identity as the complex one. -/
theorem quadFormR_eq (qs : Fin n → ℝ) (c : Fin (m + 1) → ℝ) :
    quadFormR qs c = ∑ k : Fin n, qs k * (polyEvalR c (qs k)) ^ 2 := by
  calc quadFormR qs c
      = ∑ i : Fin (m + 1), ∑ j : Fin (m + 1), ∑ k : Fin n,
          (c i * c j) * (qs k) ^ ((i : ℕ) + (j : ℕ) + 1) := by
          unfold quadFormR MR
          refine Finset.sum_congr rfl fun i _ => ?_
          refine Finset.sum_congr rfl fun j _ => ?_
          exact Finset.mul_sum Finset.univ
            (fun k => (qs k) ^ (((i : ℕ) + (j : ℕ)) + 1)) _
    _ = ∑ k : Fin n, ∑ i : Fin (m + 1), ∑ j : Fin (m + 1),
          (c i * c j) * (qs k) ^ ((i : ℕ) + (j : ℕ) + 1) :=
      three_sum_commR fun i j k => (c i * c j) * (qs k) ^ ((i : ℕ) + (j : ℕ) + 1)
    _ = ∑ k : Fin n, qs k * (polyEvalR c (qs k)) ^ 2 := by
          refine Finset.sum_congr rfl fun k _ => ?_
          rw [double_sum_shiftR (qs k) c, polyEvalR_sq]

/-- The sufficiency direction of record section 9's criterion: real non-negative
atoms force the quadratic form to be non-negative.

Each summand of `quadFormR_eq` is a non-negative weight `q_k` times a real
square.  Under RH the transformed zeros are exactly such atoms, so this is the
step that makes `cᵀHc ≥ 0` follow term by term rather than by sampling.

The hypothesis is `∀ k, 0 ≤ q_k` on an arbitrary finite multiset of reals.  It
is *not* discharged for the zeta spectrum: doing so would assume RH. -/
theorem quadFormR_nonneg (qs : Fin n → ℝ) (c : Fin (m + 1) → ℝ)
    (hq : ∀ k, 0 ≤ qs k) : 0 ≤ quadFormR qs c := by
  rw [quadFormR_eq]
  exact Finset.sum_nonneg fun k _ => mul_nonneg (hq k) (sq_nonneg _)

/-- The section 9 polynomial evaluated at a real point, in `C`.  Used only to
record that nothing is lost by running the criterion over `ℂ`. -/
theorem polyEval_ofReal (c : Fin (m + 1) → ℝ) (u : ℝ) :
    polyEval c (u : ℂ) = (polyEvalR c u : ℂ) := by
  unfold polyEval polyEvalR
  push_cast
  rfl

/-- The complex form built from real atoms *equals* the real form.  Stated as an
equality in `C` rather than as a statement about real parts, so that
`quadFormR_nonneg` transfers without needing a termwise `Complex.re` lemma. -/
theorem quadForm_ofReal (qs : Fin n → ℝ) (c : Fin (m + 1) → ℝ) :
    quadForm (fun k => (qs k : ℂ)) c = (quadFormR qs c : ℂ) := by
  have hmom : ∀ k : ℕ, M (fun j => (qs j : ℂ)) k = (MR qs k : ℂ) := by
    intro k
    unfold M MR
    push_cast
    rfl
  unfold quadForm quadFormR
  push_cast
  refine Finset.sum_congr rfl fun i _ => ?_
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [hmom, ← Complex.ofReal_mul, ← Complex.ofReal_mul]

/-- Hence the real part of the complex form is the real form, so
`quadFormR_nonneg` really is a statement about the `C`-valued object the
experiments build rather than about a weakened real surrogate. -/
theorem re_quadForm_of_real (qs : Fin n → ℝ) (c : Fin (m + 1) → ℝ) :
    (quadForm (fun k => (qs k : ℂ)) c).re = quadFormR qs c := by
  rw [quadForm_ofReal, Complex.ofReal_re]

/-- The criterion's soundness statement in one line: real non-negative atoms
give a non-negative quadratic form. -/
theorem quadForm_nonneg_of_real (qs : Fin n → ℝ) (c : Fin (m + 1) → ℝ)
    (hq : ∀ k, 0 ≤ qs k) : 0 ≤ (quadForm (fun k => (qs k : ℂ)) c).re :=
  (re_quadForm_of_real qs c).symm ▸ quadFormR_nonneg qs c hq

end PunoCalculus.RH
