import PunoCalculus.NoetherDiscrete

/-!
# The increasing point universe: growth is momentum-neutral

`NoetherDiscrete.lean` proved the Conservation mechanism on a *fixed*, finite site
set.  This file takes the next step the register asks for: the universe of points
itself **increases**.  A universe is a monotone family of finite active sets
`U : ℕ → Finset ι` (`U k ⊆ U (k+1)`); a configuration is a velocity field `v`.

The observable is the **total momentum over the current universe**,
`momentumOn (U k) v = Σ_{x ∈ U k} v x`.  The question is what universe growth does
to a conserved quantity.  The answer is exact and elementary:

* `momentumOn_grow` -- the momentum splits as `momentumOn t v = momentumOn s v +
  momentumOn (t \ s) v` whenever `s ⊆ t`: the total over the grown universe is the
  old total plus the momentum of the *new* sites.
* `influx U v k` -- that new-sites term: the momentum carried in when the universe
  goes from `U k` to `U (k+1)`.
* `universeGrowth_decomp` -- `momentumOn (U (k+1)) v = momentumOn (U k) v +
  influx U v k`: growth is a continuity equation, the influx being the "creation
  current" at the growing boundary.
* `universeGrowth_conserves` -- **the growth theorem**: if every newly created point
  enters with zero velocity (carries nothing), the total momentum is a constant of
  the growing universe, equal to its value on `U 0`.
* `chargeOn_universeGrowth_conserves` -- the same for the register's charge
  `Σ_{x ∈ U k} (q x - qm x)`, so the C36 conserved quantity survives an expanding
  universe.
* `momentumOn_univ` -- on a saturated universe (`Finset.univ`) this is exactly
  `NoetherDiscrete.momentum`.

Scope, as everywhere: finite sums of reals, no continuum limit, no PDE, no
Millennium problem (see `WHAT_THIS_DOES_NOT_PROVE.md`).  An increasing universe here
means an increasing **index set**; it is not a cosmological model.
-/

noncomputable section

namespace PunoCalculus.UniverseGrowth

open Finset

variable {ι : Type*} [DecidableEq ι]

/-- The **momentum over a universe** `s`: the sum of the field on the active sites. -/
def momentumOn (s : Finset ι) (v : ι → ℝ) : ℝ := ∑ x ∈ s, v x

/-- The **charge over a universe** `s` carried by `q` relative to `qm`: the total
displacement on the active sites. -/
def chargeOn (s : Finset ι) (q qm : ι → ℝ) : ℝ := ∑ x ∈ s, (q x - qm x)

/-- The charge over a universe is the difference of the two total momenta. -/
theorem chargeOn_eq_momentumOn_sub (s : Finset ι) (q qm : ι → ℝ) :
    chargeOn s q qm = momentumOn s q - momentumOn s qm := by
  unfold chargeOn momentumOn
  rw [Finset.sum_sub_distrib]

/-- **Growth splits the momentum.**  When `s ⊆ t`, the total over the grown universe
is the old total plus the momentum of the sites that were added, `t \ s`. -/
theorem momentumOn_grow {s t : Finset ι} (h : s ⊆ t) (v : ι → ℝ) :
    momentumOn t v = momentumOn s v + momentumOn (t \ s) v := by
  unfold momentumOn
  rw [← Finset.sum_union (Finset.disjoint_sdiff), Finset.union_sdiff_of_subset h]

/-- **Growth is momentum-neutral when the new points carry nothing.**  If every site
added between `s` and `t` has zero velocity, the total momentum is unchanged. -/
theorem momentumOn_grow_eq {s t : Finset ι} (h : s ⊆ t) (v : ι → ℝ)
    (hv : ∀ x ∈ t, x ∉ s → v x = 0) :
    momentumOn t v = momentumOn s v := by
  unfold momentumOn
  exact (Finset.sum_subset h hv).symm

/-- The same neutrality for the register's charge: sites added with zero displacement
do not change the total charge. -/
theorem chargeOn_grow_eq {s t : Finset ι} (h : s ⊆ t) (q qm : ι → ℝ)
    (hq : ∀ x ∈ t, x ∉ s → q x - qm x = 0) :
    chargeOn t q qm = chargeOn s q qm := by
  unfold chargeOn
  exact (Finset.sum_subset h hq).symm

/-- A **growing (increasing) point universe**: a monotone family of finite active
sets, `U k ⊆ U (k+1)`. -/
def IsGrowingUniverse (U : ℕ → Finset ι) : Prop := Monotone U

/-- The **creation current**: the momentum carried by the points added when the
universe grows from `U k` to `U (k+1)`. -/
def influx (U : ℕ → Finset ι) (v : ι → ℝ) (k : ℕ) : ℝ :=
  momentumOn (U (k + 1) \ U k) v

/-- **The growth continuity equation.**  The momentum over the universe after one
growth step is the momentum before it plus the creation current. -/
theorem universeGrowth_decomp (U : ℕ → Finset ι) (v : ι → ℝ)
    (hU : IsGrowingUniverse U) (k : ℕ) :
    momentumOn (U (k + 1)) v = momentumOn (U k) v + influx U v k := by
  unfold influx
  exact momentumOn_grow (hU (Nat.le_succ k)) v

/-- **The growth theorem.**  Along an increasing point universe, if every newly
created point enters with zero velocity, the total momentum is a constant of the
universe: it equals its value on `U 0` at every stage. -/
theorem universeGrowth_conserves (U : ℕ → Finset ι) (v : ι → ℝ)
    (hU : IsGrowingUniverse U)
    (hnew : ∀ k, ∀ x ∈ U (k + 1) \ U k, v x = 0) :
    ∀ k, momentumOn (U k) v = momentumOn (U 0) v := by
  intro k
  induction k with
  | zero => rfl
  | succ k ih =>
    have hstep : momentumOn (U (k + 1)) v = momentumOn (U k) v :=
      momentumOn_grow_eq (hU (Nat.le_succ k)) v
        (fun x hx hxs => hnew k x (Finset.mem_sdiff.mpr ⟨hx, hxs⟩))
    rw [hstep, ih]

/-- **The register's conserved charge survives an expanding universe.**  The same
constant-of-the-motion statement for `Σ (q x - qm x)` when new sites enter with zero
displacement. -/
theorem chargeOn_universeGrowth_conserves (U : ℕ → Finset ι) (q qm : ι → ℝ)
    (hU : IsGrowingUniverse U)
    (hnew : ∀ k, ∀ x ∈ U (k + 1) \ U k, q x - qm x = 0) :
    ∀ k, chargeOn (U k) q qm = chargeOn (U 0) q qm := by
  intro k
  induction k with
  | zero => rfl
  | succ k ih =>
    have hstep : chargeOn (U (k + 1)) q qm = chargeOn (U k) q qm :=
      chargeOn_grow_eq (hU (Nat.le_succ k)) q qm
        (fun x hx hxs => hnew k x (Finset.mem_sdiff.mpr ⟨hx, hxs⟩))
    rw [hstep, ih]

/-- On a saturated universe the growth observable is exactly the C36 momentum. -/
theorem momentumOn_univ [Fintype ι] (v : ι → ℝ) :
    momentumOn Finset.univ v = NoetherDiscrete.momentum v := by
  unfold momentumOn NoetherDiscrete.momentum
  simp

/-- Formalised-facts register for `UniverseGrowth.lean`. -/
def universeGrowthFacts : List String :=
  [ "momentumOn", "chargeOn", "chargeOn_eq_momentumOn_sub", "momentumOn_grow",
    "momentumOn_grow_eq", "chargeOn_grow_eq", "IsGrowingUniverse", "influx",
    "universeGrowth_decomp", "universeGrowth_conserves",
    "chargeOn_universeGrowth_conserves", "momentumOn_univ" ]

/-- The register has exactly twelve entries. -/
theorem universeGrowthFacts_length : universeGrowthFacts.length = 12 := by decide

end PunoCalculus.UniverseGrowth
