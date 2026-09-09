import Mathlib

/-!
# Twin ring laws (Lean 4, mathlib)

The general-width closure of the ring facts that the pure-core
`EcaIsometry` module certifies with `native_decide` on widths 4..16:
here the claims are proved for **every** ring width `w` by structural
induction, in mathlib, with self-contained definitions of the width-`w`
ring step (no floats, no axioms).

    rule 204 is the identity:  step 204 s w  =  s     whenever s < 2^w
    rule 51  is the complement:  step 51 s w =  2^w - 1 - s  whenever s < 2^w

The engine is the base-2 reading lemma: the width-`w` step output equals
`sumBits s w = (s % 2^w)`, proved from shift recurrences and the
mod-split identity `s % 2^(w+1) = (s % 2) + 2 * ((s/2) % 2^w)`.
-/

set_option linter.unreachableTactic false
set_option linter.unusedTactic false

namespace PunoTwin

/-- Bit `i` (0-indexed, least significant first) of `s`. -/
def bit (s i : Nat) : Nat := (s / (2 ^ i)) % 2

/-- Neighbourhood index of cell `i`: 4*left + 2*center + right. -/
def neighborIdx (s i w : Nat) : Nat :=
  (bit s ((i + w - 1) % w)) * 4
    + (bit s (i % w)) * 2
    + (bit s ((i + 1) % w))

/-- One step of rule `rule` on the width-`w` ring state `s`. -/
def step (rule s w : Nat) : Nat :=
  (List.range w).foldl
    (fun acc j => acc + (bit rule (neighborIdx s j w)) * (2 ^ j)) 0

/-- Sum `(bit s j) * 2^j` over `j < w` (the width-`w` reading of `s`). -/
def sumBits (s w : Nat) : Nat :=
  match w with
  | 0 => 0
  | w' + 1 => sumBits s w' + (bit s w') * (2 ^ w')

/-- Sum `(1 - bit s j) * 2^j` over `j < w` (the width-`w` complement). -/
def compBits (s w : Nat) : Nat :=
  match w with
  | 0 => 0
  | w' + 1 => compBits s w' + ((1 - bit s w') * (2 ^ w'))

lemma bit_lt_two (s i : Nat) : bit s i < 2 := by
  unfold bit
  exact Nat.mod_lt _ (by norm_num)

lemma bit_zero_one (s i : Nat) : bit s i = 0 ∨ bit s i = 1 := by
  have h := bit_lt_two s i
  omega

lemma nidx_lt_eight (s i w : Nat) : neighborIdx s i w < 8 := by
  have h1 := bit_lt_two s ((i + w - 1) % w)
  have h2 := bit_lt_two s (i % w)
  have h3 := bit_lt_two s ((i + 1) % w)
  unfold neighborIdx
  omega

lemma bit204 (k : Nat) (hk : k < 8) : bit 204 k = k / 2 % 2 := by
  interval_cases k <;> norm_num [bit]

lemma bit51 (k : Nat) (hk : k < 8) : bit 51 k = 1 - k / 2 % 2 := by
  interval_cases k <;> norm_num [bit]

/-- Rule 204 maps a neighbourhood to its centre cell. -/
lemma center_bit (s j w : Nat) : bit 204 (neighborIdx s j w) = bit s (j % w) := by
  rw [bit204 (neighborIdx s j w) (nidx_lt_eight s j w)]
  unfold neighborIdx
  rcases bit_zero_one s ((j + w - 1) % w) with hL | hL <;>
    rcases bit_zero_one s (j % w) with hC | hC <;>
      rcases bit_zero_one s ((j + 1) % w) with hR | hR <;>
        rw [hL, hC, hR] <;> norm_num

/-- Rule 51 maps a neighbourhood to the complement of its centre cell. -/
lemma center_comp_bit (s j w : Nat) : bit 51 (neighborIdx s j w) = 1 - bit s (j % w) := by
  rw [bit51 (neighborIdx s j w) (nidx_lt_eight s j w)]
  unfold neighborIdx
  rcases bit_zero_one s ((j + w - 1) % w) with hL | hL <;>
    rcases bit_zero_one s (j % w) with hC | hC <;>
      rcases bit_zero_one s ((j + 1) % w) with hR | hR <;>
        rw [hL, hC, hR] <;> norm_num

/-- Pointwise agreement on the first `n` indices implies foldl agreement. -/
lemma foldl_ext (n : Nat) {f g : Nat → Nat → Nat}
    (hf : ∀ acc j, j < n → f acc j = g acc j) :
    (List.range n).foldl f 0 = (List.range n).foldl g 0 := by
  induction n with
  | zero => rfl
  | succ n ih =>
      rw [List.range_succ, List.foldl_append, List.foldl_cons, List.foldl_nil]
      rw [List.foldl_append, List.foldl_cons, List.foldl_nil]
      rw [ih (fun acc j hj => hf acc j (by omega))]
      exact hf _ n (by omega)

/-- The step fold against the simple reading is `sumBits`. -/
lemma foldl_sumBits (s w : Nat) :
    (List.range w).foldl (fun acc j => acc + bit s (j % w) * 2 ^ j) 0 = sumBits s w := by
  induction w with
  | zero => rfl
  | succ w ih =>
      rw [List.range_succ, List.foldl_append, List.foldl_cons, List.foldl_nil]
      rw [foldl_ext w]
      · rw [ih, sumBits]
        have hmod : w % (w + 1) = w := Nat.mod_eq_of_lt (by omega)
        rw [hmod]
      · intro acc j hj
        have hjm : j % (w + 1) = j % w := by
          rw [Nat.mod_eq_of_lt (by omega)]
          rw [Nat.mod_eq_of_lt hj]
        rw [hjm]

/-- The step fold against the complement reading is `compBits`. -/
lemma foldl_compBits (s w : Nat) :
    (List.range w).foldl (fun acc j => acc + (1 - bit s (j % w)) * 2 ^ j) 0 =
      compBits s w := by
  induction w with
  | zero => rfl
  | succ w ih =>
      rw [List.range_succ, List.foldl_append, List.foldl_cons, List.foldl_nil]
      rw [foldl_ext w]
      · rw [ih, compBits]
        have hmod : w % (w + 1) = w := Nat.mod_eq_of_lt (by omega)
        rw [hmod]
      · intro acc j hj
        have hjm : j % (w + 1) = j % w := by
          rw [Nat.mod_eq_of_lt (by omega)]
          rw [Nat.mod_eq_of_lt hj]
        rw [hjm]

/-- `step (204) s w` is exactly the width-`w` reading of `s`. -/
theorem step204_eq (s w : Nat) : step 204 s w = sumBits s w := by
  unfold step
  have hfun : (fun acc j => acc + bit 204 (neighborIdx s j w) * 2 ^ j) =
      (fun acc j => acc + bit s (j % w) * 2 ^ j) := by
    funext acc j
    congr 1
    rw [center_bit s j w]
  rw [hfun]
  exact foldl_sumBits s w

/-- `step (51) s w` is exactly the width-`w` componentwise complement. -/
theorem step51_eq (s w : Nat) : step 51 s w = compBits s w := by
  unfold step
  have hfun : (fun acc j => acc + bit 51 (neighborIdx s j w) * 2 ^ j) =
      (fun acc j => acc + (1 - bit s (j % w)) * 2 ^ j) := by
    funext acc j
    congr 1
    rw [center_comp_bit s j w]
  rw [hfun]
  exact foldl_compBits s w

lemma bit_shift (s j : Nat) : bit s (j + 1) = bit (s / 2) j := by
  unfold bit
  rw [show 2 ^ (j + 1) = 2 * 2 ^ j by
    rw [show j + 1 = j.succ by omega]
    rw [Nat.pow_succ']]
  rw [show s / (2 * 2 ^ j) = (s / 2) / 2 ^ j by
    exact (Nat.div_div_eq_div_mul s 2 (2 ^ j)).symm]

lemma pow_two_succ_mul (w : Nat) : 2 ^ (w + 1) = 2 * 2 ^ w := by
  rw [show w + 1 = w.succ by omega]
  rw [Nat.pow_succ]
  rw [Nat.mul_comm]

lemma sumBits_unfold (s w : Nat) : sumBits s (w + 1) = sumBits s w + bit s w * 2 ^ w := by
  rfl

lemma compBits_unfold (s w : Nat) :
    compBits s (w + 1) = compBits s w + (1 - bit s w) * 2 ^ w := by
  rfl

lemma hb0 (s : Nat) : bit s 0 = s % 2 := by
  unfold bit
  norm_num [Nat.div_one]

/-- The shift recurrence for the reading: dropping the low bit shifts half. -/
lemma sumBits_shift (s w : Nat) : sumBits s (w + 1) = bit s 0 + 2 * sumBits (s / 2) w := by
  induction w with
  | zero => simp [sumBits]
  | succ w ih =>
      rw [sumBits_unfold s (w + 1)]
      rw [ih, bit_shift s w, pow_two_succ_mul]
      rw [sumBits_unfold (s / 2) w]
      ring

/-- The shift recurrence for the complement reading. -/
lemma compBits_shift (s w : Nat) :
    compBits s (w + 1) = (1 - bit s 0) + 2 * compBits (s / 2) w := by
  induction w with
  | zero => simp [compBits]
  | succ w ih =>
      rw [compBits_unfold s (w + 1)]
      rw [ih, bit_shift s w, pow_two_succ_mul]
      rw [compBits_unfold (s / 2) w]
      ring

/-- The mod-split identity: residues respect the base-2 shift. -/
lemma mod_split (s w : Nat) : s % 2 ^ (w + 1) = s % 2 + 2 * ((s / 2) % 2 ^ w) := by
  have hsplit : s = 2 * (s / 2) + s % 2 := by omega
  have hdiv : s / 2 = (s / 2) / 2 ^ w * 2 ^ w + (s / 2) % 2 ^ w := by
    rw [Nat.mul_comm]
    exact (Nat.div_add_mod (s / 2) (2 ^ w)).symm
  have hr : s % 2 < 2 := Nat.mod_lt s (by norm_num)
  have hbw : (s / 2) % 2 ^ w < 2 ^ w := Nat.mod_lt _ (by positivity)
  have h2 : 2 * ((s / 2) % 2 ^ w) + s % 2 < 2 * 2 ^ w := by
    nlinarith [hbw, hr]
  have hre : 2 * ((s / 2) / 2 ^ w * 2 ^ w + (s / 2) % 2 ^ w) + s % 2 =
      (2 * ((s / 2) % 2 ^ w) + s % 2) + ((s / 2) / 2 ^ w) * (2 * 2 ^ w) := by
    ring
  conv_lhs =>
    rw [pow_two_succ_mul, hsplit, hdiv, hre]
  conv_lhs =>
    rw [Nat.add_mul_mod_self_right]
  rw [Nat.mod_eq_of_lt h2]
  omega

/-- The width-`w` reading of `s` is its residue mod `2^w`. -/
theorem sumBits_eq (s w : Nat) : sumBits s w = s % 2 ^ w := by
  induction w generalizing s with
  | zero => simp [sumBits, Nat.mod_one]
  | succ w ih =>
      rw [sumBits_shift s w]
      rw [hb0 s]
      rw [ih (s / 2)]
      rw [mod_split]

/-- The width-`w` componentwise complement is `(2^w - 1) - (s mod 2^w)`. -/
theorem compBits_eq (s w : Nat) : compBits s w = 2 ^ w - 1 - s % 2 ^ w := by
  induction w generalizing s with
  | zero => simp [compBits, Nat.mod_one]
  | succ w ih =>
      rw [compBits_shift s w]
      rw [hb0 s]
      rw [ih (s / 2)]
      have hr0 : s % 2 = 0 ∨ s % 2 = 1 := by omega
      have hq : (s / 2) % 2 ^ w < 2 ^ w := Nat.mod_lt _ (by positivity)
      rcases hr0 with hr | hr
      · rw [hr]
        rw [mod_split]
        rw [hr, pow_two_succ_mul]
        omega
      · rw [hr]
        rw [mod_split]
        rw [hr, pow_two_succ_mul]
        omega

/-- Rule 204 is the identity on every width-`w` ring (all widths). -/
theorem rule204_identity_all (w s : Nat) (h : s < 2 ^ w) : step 204 s w = s := by
  rw [step204_eq, sumBits_eq]
  exact Nat.mod_eq_of_lt h

/-- Rule 51 is the width-`w` bitwise complement on every ring (all widths). -/
theorem rule51_complement_all (w s : Nat) (h : s < 2 ^ w) :
    step 51 s w = 2 ^ w - 1 - s := by
  rw [step51_eq, compBits_eq]
  rw [Nat.mod_eq_of_lt h]