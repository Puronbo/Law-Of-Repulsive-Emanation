import Mathlib
import PunoCalculus.CriticalLadder

/-!
# Emergent time: change is transfer, time is the count

This brick formalises three structural claims of the register's ontology.

1. **Time is not a primitive variable.**  A "change" is a *transfer* (removal from
   one reservoir, addition to another); there is no clock.  Iterating the transfer
   map `n` times is what we call "elapsed time", and the state is a function of the
   COUNT `n` alone (`state_determined_by_count`).  Because a transfer only moves
   energy, the total is invariant (`transfer_conserves_total`): decay is removal,
   growth is transfer, and neither needs a time axis.

2. **The squaring relation is the order-2 self-similar fixed ratio.**  `sqrt b = a`
   forces `b / a = a`: the value equals its own ratio -- the self-consistency of a
   doubling step (`EnstrophyBarrier.doubling`).  `sqrt_self_consistency` proves it.

3. **Change costs energy in proportion to the dimension count.**  A `d`-dimensional
   object's scale-free change exponent is the dimension-`d` critical rung
   `sCritN d p = d / p - 1` (`sCritN_three` recovers the register ladder at `d = 3`).
   It is scale-free exactly on `s = d / p - a` (`scaleFreeN_iff`), and more
   dimensions cost more (`sCritN_mono`): the energy needed to change an object
   grows with its number of dimensions.

This is a structural reframing (a toy reservoir model plus dimension-parameter
arithmetic), not a PDE claim; the boundedness wall stays OPEN.
-/

noncomputable section

namespace PunoCalculus.EmergentTime

open PunoCalculus.CriticalLadder (sCrit)

/-! ### 1. Change is transfer; time is the step count -/

/-- A two-reservoir state: energy in `hot` may be removed and transferred to `cold`.
No time coordinate appears. -/
structure Reservoir where
  hot : ℝ
  cold : ℝ

theorem Reservoir.ext {r s : Reservoir} (h1 : r.hot = s.hot) (h2 : r.cold = s.cold) :
    r = s := by
  cases r; cases s; simp_all

/-- Total energy across the two reservoirs. -/
def Reservoir.total (r : Reservoir) : ℝ := r.hot + r.cold

/-- One change: remove `δ` from `hot` and transfer it to `cold`. -/
def transfer (δ : ℝ) (r : Reservoir) : Reservoir := ⟨r.hot - δ, r.cold + δ⟩

@[simp] theorem transfer_hot (δ : ℝ) (r : Reservoir) :
    (transfer δ r).hot = r.hot - δ := rfl

@[simp] theorem transfer_cold (δ : ℝ) (r : Reservoir) :
    (transfer δ r).cold = r.cold + δ := rfl

/-- A change is a transfer: it moves energy, it does not create or destroy it.
Decay (removal) and growth (transfer) are two readings of the same move. -/
theorem transfer_conserves_total (δ : ℝ) (r : Reservoir) :
    (transfer δ r).total = r.total := by
  simp only [transfer, Reservoir.total, transfer_hot, transfer_cold]
  ring

/-- After `n` transfers the reservoirs have moved `n * δ`; there is no other clock. -/
theorem transfer_iterate (δ : ℝ) (r : Reservoir) (n : ℕ) :
    ((transfer δ)^[n] r).hot = r.hot - n * δ ∧
    ((transfer δ)^[n] r).cold = r.cold + n * δ := by
  induction n with
  | zero => simp
  | succ k ih =>
    rw [Function.iterate_succ_apply']
    constructor
    · rw [transfer_hot, ih.1]; push_cast; ring
    · rw [transfer_cold, ih.2]; push_cast; ring

/-- **Time is the count.**  The state is a function of the number of transfers
alone: no separate time variable exists. -/
theorem state_determined_by_count (δ : ℝ) (r : Reservoir) (n : ℕ) :
    (transfer δ)^[n] r = ⟨r.hot - n * δ, r.cold + n * δ⟩ :=
  Reservoir.ext (transfer_iterate δ r n).1 (transfer_iterate δ r n).2

/-! ### 2. The squaring relation is the order-2 self-similar fixed ratio -/

/-- **`sqrt b = a => b / a = a`.**  The squaring relation is self-consistent: the
value `a` equals its own ratio `b / a`.  This is the fixed ratio of the order-2
(doubling) step. -/
theorem sqrt_self_consistency {a b : ℝ} (ha : 0 < a) (h : Real.sqrt b = a) :
    b / a = a := by
  have hs : b = a * a := ((Real.sqrt_eq_iff_mul_self_eq_of_pos ha).mp h).symm
  rw [hs, div_eq_iff (ne_of_gt ha)]

/-! ### 3. Change cost grows with the dimension count -/

/-- The scale-free change exponent of a `d`-dimensional object in `L^p`: the
dimension-`d` critical rung `d / p - 1`. -/
def sCritN (d p : ℝ) : ℝ := d / p - 1

/-- At `d = 3` this is exactly the register ladder `sCrit`. -/
theorem sCritN_three (p : ℝ) : sCritN 3 p = sCrit p := by
  unfold sCritN sCrit
  ring

/-- The homogeneous norm of a `d`-dimensional object of order `a` has scaling
weight `a + s - d / p`. -/
def scalingWeightN (s a d p : ℝ) : ℝ := a + s - d / p

/-- Scale-freeness picks the change exponent: the weight vanishes exactly when
`s = d / p - a`. -/
theorem scaleFreeN_iff {s a d p : ℝ} :
    scalingWeightN s a d p = 0 ↔ s = d / p - a := by
  unfold scalingWeightN
  constructor <;> intro h <;> linarith

/-- **More dimensions cost more.**  For fixed `p > 0`, the change exponent is
monotone in the dimension count: a higher-dimensional object needs more energy
(more smoothness) to be changed in a scale-free way. -/
theorem sCritN_mono {d e p : ℝ} (hp : 0 < p) (hde : d ≤ e) :
    sCritN d p ≤ sCritN e p := by
  unfold sCritN
  have h : d / p ≤ e / p := div_le_div_of_nonneg_right hde (le_of_lt hp)
  linarith

/-- Formalised-facts register for this brick. -/
def emergentTimeFacts : List String :=
  [ "transfer_conserves_total"
  , "transfer_iterate"
  , "state_determined_by_count"
  , "sqrt_self_consistency"
  , "sCritN_three"
  , "scaleFreeN_iff"
  , "sCritN_mono" ]

/-- The register has exactly seven entries. -/
theorem emergentTimeFacts_length : emergentTimeFacts.length = 7 := by decide

end PunoCalculus.EmergentTime
