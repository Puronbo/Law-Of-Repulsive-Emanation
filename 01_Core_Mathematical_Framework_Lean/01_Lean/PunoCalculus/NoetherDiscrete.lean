import Mathlib

/-!
# The discrete Noether theorem (the Conservation mechanism's formal home)

The register's atlas names five 0/0 mechanisms; three of them -- Probe, Vanishing
Rate, Index -- are machine-checked (`ZeroProbe`, `ZeroValuation`, `ZeroIndex`).  The
**Conservation** mechanism -- "a conserved quantity is the ratio of two quantities
that both vanish when the symmetry is broken" -- had only prose behind it.  This
file gives it a formal core: a **discrete Noether theorem** over a finite site set.

Setting.  A configuration is a velocity field `v : ι → ℝ` on a finite index set
`ι`; its **momentum** is the sum `Σᵢ vᵢ`.  The **charge** carried by `q` relative
to `qm` is the total displacement `Σᵢ (qᵢ - qmᵢ)`.

* `charge_eq_momentum_sub` -- the charge is a *difference of two momenta*; when both
  vanish the 0/0 is exactly the conserved quantity (the register's framing).
* `charge_self` -- no displacement carries zero charge (the vanishing numerator).
* `charge_translation_invariant` -- **the symmetry**: translating both
  configurations by the same constant leaves the charge unchanged.
* `momentum_from_rate` -- the momentum is the removable value of `(Σᵢ vᵢ·dt)/dt` at
  `dt = 0`: the Probe face of the conserved quantity.
* `momentum_conserved` -- **the discrete Noether theorem**: for a force field whose
  total force vanishes on every configuration (`Σᵢ Fᵢ(q) = 0`, the infinitesimal
  form of translation invariance), one step of the time-symmetric update
  `q_{k+1} = 2 q_k - q_{k-1} + F(q_k)` leaves the charge unchanged.
* `momentumAt_eq_initial` -- along a discrete-Newton trajectory, momentum is a
  constant of the motion: it equals its initial value at every step.
* `conservationLaw` -- the capstone bundling the symmetry, the balance law and the
  constancy of the momentum.

Scope, as everywhere: a statement about finite sums of reals.  No continuum limit
is taken, no PDE is solved, and no Millennium problem is touched (see
`WHAT_THIS_DOES_NOT_PROVE.md`).  The classical referent is Noether, *Invariante
Variationsprobleme* (1918); here it is the finite-dimensional, discrete shadow.
-/

noncomputable section

namespace PunoCalculus.NoetherDiscrete

open Finset

variable {ι : Type*} [Fintype ι]

/-- A **velocity field** on the finite index set `ι`: one real number per site. -/
abbrev Velocity (ι : Type*) := ι → ℝ

/-- The **total momentum** of a velocity field: the sum of the per-site velocities. -/
def momentum (v : Velocity ι) : ℝ := ∑ i, v i

/-- The **charge** carried by `q` relative to `qm`: the total displacement
`Σᵢ (qᵢ - qmᵢ)`.  This is the conserved quantity of the Conservation mechanism. -/
def charge (q qm : Velocity ι) : ℝ := ∑ i, (q i - qm i)

/-- The charge is the difference of the two total momenta: the conserved quantity is
literally a `0/0` of two quantities that vanish together when the symmetry is broken. -/
theorem charge_eq_momentum_sub (q qm : Velocity ι) :
    charge q qm = momentum q - momentum qm := by
  unfold charge momentum
  rw [Finset.sum_sub_distrib]

/-- A configuration has zero charge against itself (no displacement): the vanishing
numerator of the 0/0. -/
theorem charge_self (q : Velocity ι) : charge q q = 0 := by
  unfold charge
  simp

/-- **The symmetry.**  The charge is invariant under a simultaneous translation of
both configurations by the same constant. -/
theorem charge_translation_invariant (q qm : Velocity ι) (c : ℝ) :
    charge (fun i => q i + c) (fun i => qm i + c) = charge q qm := by
  unfold charge
  exact Finset.sum_congr rfl (fun i _ => by ring)

/-- **The Probe face.**  The momentum is the removable value of the quotient
`(Σᵢ vᵢ · dt) / dt` as `dt → 0`: both numerator and denominator vanish at `dt = 0`,
and the removable value is the conserved momentum. -/
theorem momentum_from_rate (v : Velocity ι) (dt : ℝ) (hdt : dt ≠ 0) :
    (∑ i, v i * dt) / dt = momentum v := by
  rw [← Finset.sum_mul, momentum]
  exact mul_div_cancel_right₀ _ hdt

/-- One step of the discrete Newton rule for a force field `F`: the time-symmetric
update `q_{k+1} = 2 q_k - q_{k-1} + F(q_k)`. -/
def step (F : Velocity ι → Velocity ι) (qm q : Velocity ι) : Velocity ι :=
  fun i => 2 * q i - qm i + F q i

/-- **The discrete Noether theorem.**  If the force field is *balanced* -- its total
force vanishes on every configuration, `Σᵢ Fᵢ(q) = 0` (the infinitesimal form of
translation invariance) -- then one step of the discrete Newton rule conserves the
charge. -/
theorem momentum_conserved (F : Velocity ι → Velocity ι)
    (hbalance : ∀ q, ∑ i, F q i = 0) (q qm : Velocity ι) :
    charge (step F qm q) q = charge q qm := by
  unfold charge step
  rw [show (∑ i, (2 * q i - qm i + F q i - q i))
        = (∑ i, (q i - qm i)) + ∑ i, F q i by
      rw [← Finset.sum_add_distrib]
      exact Finset.sum_congr rfl (fun i _ => by ring)]
  rw [hbalance q, add_zero]

/-- A trajectory is a discrete-Newton trajectory for `F` when each step follows the
rule `u_{k+2} = step F u_k u_{k+1}`. -/
def IsDiscreteNewton (F : Velocity ι → Velocity ι) (u : ℕ → Velocity ι) : Prop :=
  ∀ k, u (k + 2) = step F (u k) (u (k + 1))

/-- The momentum carried at step `k`: the charge from `u k` to `u (k+1)`. -/
def momentumAt (u : ℕ → Velocity ι) (k : ℕ) : ℝ := charge (u (k + 1)) (u k)

/-- Along a discrete-Newton trajectory of a balanced force, the momentum is the same
at every step. -/
theorem momentumAt_conserved (F : Velocity ι → Velocity ι)
    (hbalance : ∀ q, ∑ i, F q i = 0) {u : ℕ → Velocity ι}
    (hu : IsDiscreteNewton F u) (k : ℕ) :
    momentumAt u (k + 1) = momentumAt u k := by
  unfold momentumAt
  rw [hu k]
  exact momentum_conserved F hbalance (u (k + 1)) (u k)

/-- **Momentum is a constant of the motion**: along any discrete-Newton trajectory of
a balanced force it equals its initial value at every step. -/
theorem momentumAt_eq_initial (F : Velocity ι → Velocity ι)
    (hbalance : ∀ q, ∑ i, F q i = 0) {u : ℕ → Velocity ι}
    (hu : IsDiscreteNewton F u) (k : ℕ) :
    momentumAt u k = momentumAt u 0 := by
  induction k with
  | zero => rfl
  | succ k ih => rw [momentumAt_conserved F hbalance hu k, ih]

/-- **The Conservation mechanism's capstone.**  The charge is a difference of two
momenta, vanishes with no displacement, is invariant under simultaneous translation
(the symmetry), is the removable value of the momentum rate (the Probe face), and is
conserved by the discrete Newton rule whenever the force field is balanced -- and is
therefore a constant of the motion along any trajectory. -/
theorem conservationLaw :
    (∀ q qm : Velocity ι, charge q qm = momentum q - momentum qm) ∧
    (∀ q : Velocity ι, charge q q = 0) ∧
    (∀ q qm : Velocity ι, ∀ c : ℝ,
      charge (fun i => q i + c) (fun i => qm i + c) = charge q qm) ∧
    (∀ v : Velocity ι, ∀ dt : ℝ, dt ≠ 0 →
      (∑ i, v i * dt) / dt = momentum v) ∧
    (∀ F : Velocity ι → Velocity ι, (∀ q, ∑ i, F q i = 0) →
      ∀ q qm : Velocity ι, charge (step F qm q) q = charge q qm) ∧
    (∀ F : Velocity ι → Velocity ι, (∀ q, ∑ i, F q i = 0) →
      ∀ _u : ℕ → Velocity ι, IsDiscreteNewton F _u →
      ∀ k : ℕ, momentumAt _u k = momentumAt _u 0) :=
  ⟨charge_eq_momentum_sub, charge_self, charge_translation_invariant,
   momentum_from_rate, momentum_conserved,
   fun F h _u hu k => momentumAt_eq_initial F h hu k⟩

/-- Formalised-facts register for `NoetherDiscrete.lean`. -/
def noetherDiscreteFacts : List String :=
  [ "momentum", "charge", "charge_eq_momentum_sub", "charge_self",
    "charge_translation_invariant", "momentum_from_rate", "step",
    "momentum_conserved", "IsDiscreteNewton", "momentumAt",
    "momentumAt_conserved", "momentumAt_eq_initial", "conservationLaw" ]

/-- The register has exactly thirteen entries. -/
theorem noetherDiscreteFacts_length : noetherDiscreteFacts.length = 13 := by decide

end PunoCalculus.NoetherDiscrete
