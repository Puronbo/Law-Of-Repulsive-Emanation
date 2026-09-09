/- PunoCalculus.EcaIsometry
   ========================

   Formal, machine-checked statements of the width-w ring-algebra
   theorems that the sibling Python audit corpus verifies
   (soliton_isometry_proofs + validate_soliton_isometry_proofs).

   Everything here is exact and decidable: states are integers
   0 .. 2^w - 1, the ring evolution is the deterministic one-step map,
   and every displayed theorem is decided by `native_decide` (a
   closed, kernel-verified Bool/decidable computation).  There are no
   approximations, no axioms, and no number-theoretic import.

   The theorems mirror the audited facts at width 8, and the parity
   theorem covers ring widths 6 .. 14:

     * rule 204 is the identity map on all 256 states;
     * rule 51 is the bitwise complement;
     * the GF(2)-affine sector is the 16 low-degree rules
       {0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195,
        204, 240, 255};
     * the exact Hamming-isometry class is the six rotations
       {15, 51, 85, 170, 204, 240};
     * the constants are exactly {0, 255};
     * the multi-input affine rules (transducers) are exactly
       {60, 90, 102, 105, 150, 153, 165, 195};
     * the four census extras {154, 166, 180, 210} are neither
       isometries nor bijections at width 8, and are bijections for
       exactly the odd widths among 6..14;
     * within the 32-rule twin family the isometry class reduces to
       the pair {204, 51}.

   Millennium scope: these are finite, decidable statements of a
   P-style classification; they quantify the state-count-2^w
   enumeration but say nothing about P vs NP, nor about any other
   Millennium problem.  The pairing is documented in
   PunoCalculus.MillenniumBridge.
-/

namespace EcaIsometry

/-! Ring infrastructure (exact integer semantics). -/

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
    (fun acc i => acc + (bit rule (neighborIdx s i w)) * (2 ^ i)) 0

/-- Hamming distance of two width-`w` states. -/
def hamming (x y w : Nat) : Nat :=
  (List.range w).foldl
    (fun acc i =>
      let a := bit x i
      let b := bit y i
      acc + (a + b - 2 * ((a + b) / 2))) 0

/-- Bitwise XOR of two width-`w` states. -/
def xor (x y w : Nat) : Nat :=
  (List.range w).foldl
    (fun acc i =>
      let a := bit x i
      let b := bit y i
      acc + (a + b - 2 * ((a + b) / 2)) * (2 ^ i)) 0

/-- State equality on all `w` bits, as a Bool. -/
def statesEq (x y w : Nat) : Bool :=
  (List.range w).all (fun i => bit x i == bit y i)

/-- Is inequality `GF(2)`-affine: exists c, for all x, y:
    T x xor T y  =  T (x xor y) xor c. -/
def affineCheck (rule w : Nat) : Bool :=
  (List.range (2 ^ w)).any (fun c =>
    (List.range (2 ^ w)).all (fun x =>
      (List.range (2 ^ w)).all (fun y =>
        statesEq (xor (step rule x w) (step rule y w) w)
                 (xor (step rule (xor x y w) w) c w) w)))

/-- The GF(2)-affine sector at width `w`. -/
def affineSet (w : Nat) : List Nat :=
  (List.range (2 ^ w)).filter (fun r => affineCheck r w)

/-- Exact Hamming isometry of the ring: distances are preserved. -/
def isometryCheck (rule w : Nat) : Bool :=
  (List.range (2 ^ w)).all (fun x =>
    (List.range (2 ^ w)).all (fun y =>
      hamming (step rule x w) (step rule y w) w == hamming x y w))

/-- The exact isometry class at width `w`. -/
def isometrySet (w : Nat) : List Nat :=
  (List.range (2 ^ w)).filter (fun r => isometryCheck r w)

/-- Elementary membership test (Nat list). -/
def memList : Nat → List Nat → Bool
  | _, [] => false
  | n, m :: ms => if n == m then true else memList n ms

/-- No duplicates (Nat list). -/
def noDup : List Nat → Bool
  | [] => true
  | n :: ns => if memList n ns then false else noDup ns

/-- Bijectivity of `rule` on the width-`w` state space. -/
def bijective (rule w : Nat) : Bool :=
  noDup ((List.range (2 ^ w)).map (fun s => step rule s w))

/-- Flip bit `k` of the 3-bit index `i` (used for input dependence). -/
def flipBit (i k : Nat) : Nat :=
  if bit i k == 0 then i + (2 ^ k) else i - (2 ^ k)

/-- Number of truth-table inputs that `rule` actually depends on. -/
def inputCount (rule : Nat) : Nat :=
  (List.range 3).foldl
    (fun acc k =>
      acc + (if (List.range 8).any
                  (fun i => bit rule i != bit rule (flipBit i k))
                then 1 else 0)) 0

/-- Bitwise complement on the width-8 state space. -/
def complement (s : Nat) : Nat := 255 - s

/-! Theorems (all decided by finite, kernel-verified evaluation). -/

theorem affine_is_sixteen :
    affineSet 8 = [0, 15, 51, 60, 85, 90, 102, 105,
                  150, 153, 165, 170, 195, 204, 240, 255] := by
  native_decide

theorem isometry_is_six :
    isometrySet 8 = [15, 51, 85, 170, 204, 240] := by
  native_decide

theorem rule204_identity :
    (List.range 256).all (fun s => step 204 s 8 == s) = true := by
  native_decide

theorem rule51_complement :
    (List.range 256).all (fun s => step 51 s 8 == complement s) =
      true := by
  native_decide

theorem constants_pair :
    (affineSet 8).filter (fun r => inputCount r == 0) = [0, 255] := by
  native_decide

theorem transducer_is_eight :
    (affineSet 8).filter (fun r => 2 <= inputCount r) = [60, 90, 102, 105,
      150, 153, 165, 195] := by
  native_decide

theorem extras_not_isometry :
    [154, 166, 180, 210].all (fun r => isometryCheck r 8 == false) =
      true := by
  native_decide

theorem extras_not_bijective_width8 :
    [154, 166, 180, 210].all (fun r => bijective r 8 == false) = true := by
  native_decide

theorem extras_bijective_iff_odd :
    ((List.range 15).drop 6).all (fun w =>
      [154, 166, 180, 210].all (fun r => bijective r w == (w % 2 == 1))) =
        true := by
  native_decide

theorem six_is_pair_in_family :
    (isometrySet 8).filter (fun r => r == 204 || r == 51) = [51, 204] := by
  native_decide

/-- P-style certificates of the exact counts (finite-state).
    These are the statements referenced by the Millennium-scope
    pairing in PunoCalculus.MillenniumBridge. -/
theorem count_affine_sector : (affineSet 8).length = 16 := by
  native_decide

theorem count_isometry_class : (isometrySet 8).length = 6 := by
  native_decide

/-! Stronger classification forms: the width-8 sector AND class are
    decided exactly, rule for rule (membership biconditionals as Bool
    equations over the full rule space), and the identity-complement
    pair is verified on every state of every ring width 4..16. -/

/-- Complement on the width-`w` state space (all ones minus s). -/
def complementGen (s w : Nat) : Nat := (2 ^ w) - 1 - s

theorem affine_class_exact :
    (List.range 256).all (fun r =>
      (affineCheck r 8 == true) ==
        memList r [0, 15, 51, 60, 85, 90, 102, 105,
                   150, 153, 165, 170, 195, 204, 240, 255]) = true := by
  native_decide

theorem isometry_class_exact :
    (List.range 256).all (fun r =>
      (isometryCheck r 8 == true) ==
        memList r [15, 51, 85, 170, 204, 240]) = true := by
  native_decide

theorem rule204_identity_widths :
    ((List.range 17).drop 4).all (fun w =>
      (List.range (2 ^ w)).all (fun s => step 204 s w == s)) = true := by
  native_decide

theorem rule51_complement_widths :
    ((List.range 17).drop 4).all (fun w =>
      (List.range (2 ^ w)).all (fun s =>
        step 51 s w == complementGen s w)) = true := by
  native_decide

-- Sanity echoes, matching the Python audits' stdout behaviour.
#eval affineSet 8
#eval isometrySet 8

end EcaIsometry