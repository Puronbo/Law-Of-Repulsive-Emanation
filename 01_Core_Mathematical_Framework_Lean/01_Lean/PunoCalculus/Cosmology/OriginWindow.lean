import Mathlib

/-!
# The origin consistency window: ONE number, TWO problems, ONE inequality

Flatness and horizon are usually presented as two independent initial-value
problems of early-universe cosmology.  They are not.  Both are controlled by the
single stiffness integral

  `S := int (1 + 3w) dln a`,

which is additive over eras, hence path-independent, and is the only
history-dependent quantity either question needs.

## The question being asked

A cosmology is not a set of laws; it is a history -- a scale factor `a(t)`
carrying an equation of state `p = w rho`.  Given such a history:

  * `rho(a) = rho_i a^(-3(1+w))` from the continuity equation;
  * `H^2 = (8 pi G / 3) rho - k / a^2` from Friedmann;
  * `eps = |Omega - 1| = |k| / (a^2 H^2)`, the curvature parameter;
  * `r = 1/(aH)`, the comoving Hubble radius.

Differentiating gives, for constant `w` per era and in fact in general:

  `dln eps / dln a = 1 + 3w`      and      `dln r / dln a = (1 + 3w)/2`

so both are exponentials of the SAME integral `S`:

  `eps` is multiplied by `e^S`,   `r` is multiplied by `e^(S/2)`.

## The two admissibility conditions, both sign tests on `S`

  (F) FLATNESS  `eps_f < eps_obs`  <=>  `S < S_req`,  `S_req = log (eps_obs/eps_i)`
  (H) HORIZON   `r_f < r_i`        <=>  `S < 0`

The horizon direction is the easy thing to get backwards, so it is stated
carefully.  The horizon problem asks that today's observable region fit INSIDE
the Hubble patch that existed earlier.  Today's region has comoving size
`r_f = 1/(a_f H_f)`, the earlier patch has `r_i = 1/(a_i H_i)`, so the
requirement is `r_f < r_i`, i.e. `e^(S/2) < 1`, i.e. `S < 0`.  The comoving
Hubble radius must SHRINK.  Hence a decelerating era (`w > -1/3`) makes the
horizon problem worse, not better -- and the matter era we live through
contributes `+80` to `S` all by itself.

## The linking statement, and what it is not

Since `eps_obs < eps_i`, `S_req = log (eps_obs/eps_i) < 0` strictly, and so

  `S < S_req  ==>  S < 0`,

i.e. **flatness admissibility implies horizon admissibility**.  One inequality
does both jobs and flatness is the binding one.  The two "separate"
initial-value problems are one problem.

`not_a_beginning_theorem` is the load-bearing scope statement.  Everything above
is a CONSISTENCY FILTER on an assumed history.  `eps_i` is an INPUT here and
`filter_leaves_eps_i_free` records that no value of it is excluded.  A filter
that leaves `eps_i` free cannot have derived it, so it cannot claim to explain
the beginning, and there is deliberately no theorem here of that shape to
borrow.  This is the cosmological counterpart of `not_a_newman_theorem` in
`AcousticZeroFlow.lean`.

## What is proved here

  * `S_append`, `S_reverse`, `S_split_era`, `S_split_thirds` - `S` is additive
    and order-independent, so it is a function of the history rather than of the
    bookkeeping used to write it down;
  * `stiffness_zero_iff`, `stiffness_neg_of_lt`, `stiffness_pos_of_gt`,
    `stiffness_matter` - the sign test is sharp at `w = -1/3`, and the matter
    era contributes `+n`;
  * `epsFinal_lt_epsObs_iff` - (F) is EXACTLY `S < S_req`, not an inequality in
    a proxy variable;
  * `radiusRatio_lt_one_iff` - (H) is EXACTLY `S < 0`;
  * `sRequired_neg` - `S_req < 0` whenever `eps_obs < eps_i`, which is what
    orders the two thresholds;
  * `flatness_implies_horizon` - THE LINKING THEOREM, as a machine-checked
    implication and not a sentence of prose;
  * `boundary_inadmissible`, `horizon_only_band_exists`,
    `admissible_iff_flat_of_neg` - the conditions are open, and STRICTLY
    nested rather than identical;
  * `the_three_origins_share_one_axis` - the capstone of the zero thread: the
    window has exactly three decisive values (the unique stiffness zero
    `w = -1/3`, the horizon origin `S = 0`, the flatness origin
    `S = sRequired < 0`), all on one axis, each a strict boundary and never a
    solution;
  * `nInflNeeded_lt_iff_flat`, `deSitter_threshold_iff` - the required
    inflation length, in the form actually used, so that "42.2549 e-folds" is a
    theorem about a formula rather than a number in a Python string.  Note that
    division by the negative inflationary stiffness REVERSES the inequality:
    that is what turns the threshold into a lower bound on the required length,
    and it is the one place where an algebra slip would silently invert the
    physics;
  * `sRequired_mono`, `nInflNeeded_mono_epsI` - the threshold has a floor and no
    ceiling;
  * `nInflNeeded_affine`, `nInflNeeded_anti_mono_epsObs` - THE AFFINE LAW: the
    required length depends on the curvature bound only through `log eps_obs`,
    and a looser bound demands weakly less.  This is what makes "each decade of
    precision buys half an e-fold" a theorem rather than a slogan, and it holds
    for EVERY positive `eps_obs` with no observational input whatsoever;
  * `nInflNeeded_epsObsNeededFor`, `epsObsNeededFor_nInflNeeded` - the two are
    MUTUAL INVERSES, so "60 e-folds need 4.2e-18" and "4.2e-18 certifies 60
    e-folds" cannot drift apart;
  * `deSitter_decade_gain` - the de Sitter increment exactly: a factor of ten in
    the bound moves the requirement by exactly `log 10 / (-2)` from any
    starting point;
  * `deSitter_decade_gain_neg`, `deSitter_tighter_bound_demands_more` - that
    increment is NEGATIVE, so tightening the bound strictly increases the
    requirement.  The strictness is what rules out any finite length certifying
    a finite bound, and hence `~60` e-folds for any achievable precision;
  * `saturated_length_is_not_admissible` - the saturating length `nInflNeeded`
    sits EXACTLY on the boundary, so `boundary_inadmissible` holds in the length
    formulation too: no length can exceed a condition already met exactly;
  * `nInflNeeded_unbounded_above`, `nInflNeeded_above_persists` - THE DIVERGENCE
    AS A THEOREM.  For every finite target length `N` there is an `eps_obs > 0`
    whose requirement exceeds it, and once such a precision is passed every
    tighter measurement still demands strictly more.  The requirement is an
    unbounded function of the measured precision, so the ceiling at `~60` is a
    theorem about the exact law `eps = 1/(D*a^(-1-3w) - sigma)`, not a number
    borrowed from experiment.  No observational input is used;
  * `curvatureVerdict`, `curvatureVerdict_iff_falsified`, `curvatureVerdict_neg`,
    `curvatureVerdict_at_bound`, `curvatureVerdict_mono_bound` - the model filter
    as a DECIDABLE PREDICATE rather than a string in a Python dict.  Sign
    symmetry is pinned, so the `omega_k < -1e-4` (closed) case that would
    separate slow-roll from false-vacuum eternal inflation is provably OUT of
    reach of this function;
  * `curvatureVerdict_excludes_something` - the rule is not vacuous AS A RULE;
    what N7 lacks is a prediction to feed it, which `filter_leaves_eps_i_free`
    states separately;
  * `curvatureVerdict_bridge_open` - the verdict is NOT a second criterion: it is
    the flatness test (F) evaluated at the `S` that produces that curvature;
  * `curvatureVerdict_boundary_disagrees` - **a discrepancy found by
    formalisation.**  At `|omega_k| = eps_obs` exactly, `curvatureVerdict` calls
    the model admissible while `flatnessAdmissible` calls it inadmissible.  Both
    conventions are defensible alone, but they are not the same predicate, so the
    Python wrapper must not be described as a restatement of (F) without this
    caveat;
  * `filter_leaves_eps_i_free` - the tripwire: `eps_i` is unconstrained.
   * `epsExact_*` - the exact curvature law at the `SOf` level.  The closed
     form `eps = 1/(D a^(-1-3w) - sigma)` is written without a variable
     exponent as `eps = 1/(D e^(-S) - sigma)`, where `S = stiffness w * n =
     (1+3w) ln a`, so that `e^(-S) = a^(-(1+3w))`.  `epsExact_SOf_factor`
     factors the aggregate two-era law over eras, `epsExact_sigma_zero` shows
     the `- sigma` shift is the WHOLE difference from the leading power law,
     and `epsExact_leading_ratio` / `epsExact_radius_ratio_sq` reproduce the
     `n7b`/`n7c` ratio laws (`1/(1 - sigma/X)` and `1 - sigma/X`, with
     `X = D e^(-S)`) exactly, not to 1e-12;

## Not proved here, and said so rather than implied

  * the direct `a^r` form `eps = 1/(D a^(-1-3w) - sigma)` is NOT formalised
    here: it needs a variable exponent on a base of uncontrolled sign.  What IS
    formalised (below) is the equivalent `exp(-S)` form, which carries the same
    physics without raising a base to a variable exponent.  The numeric closed
    form is verified against direct Friedmann integration in
    `02_Experimental_Implementations_and_Verification/01_Poincare_Universe_and_Cosmological_Models/origin_consistency_window_n7.py`
    (gates `n7a`-`n7c`, to `3e-16`);
  * that GR is the correct theory of the very early universe.  This file is
    conditional on FLRW + GR throughout and says nothing at the `t < 1e-43 s`
    regime where that is conjectural;
  * that the observed `eps_obs ~ 0.011` is anything other than a measurement.
    It enters as an input, and every theorem above is an identity or an order
    statement VALID FOR ALL POSITIVE `eps_obs`, so none of them depends on this
    number or on any other observational quantity.  The provenance of `0.011`
    itself is NOT established in this file and is not established by the
    framework; it is a pre-existing figure that has not been audited against a
    primary source here, and it should not be described as verified until it is;
  * that the two boundary conventions of `curvatureVerdict_boundary_disagrees`
    should be reconciled.  Which convention the model filter SHOULD use is a
    modelling decision, not a theorem, so the disagreement is recorded rather
    than closed.
-/

noncomputable section

namespace PunoCalculus.Cosmology.OriginWindow

open Real

/-! ### The stiffness integral `S` -/

/-- One era of constant equation of state `w` lasting `n` e-folds. -/
structure Era where
  /-- Equation-of-state parameter, `p = w rho`. -/
  w : ℝ
  /-- E-folds, i.e. `dln a` accumulated during the era. -/
  n : ℝ
  deriving DecidableEq

/-- The density of `S` in `dln a`.  Vanishes exactly at `w = -1/3`; that single
value is the boundary of the whole story, and `stiffness_zero_iff` says so
rather than leaving it to be noticed. -/
def stiffness (w : ℝ) : ℝ := 1 + 3 * w

/-- THE single history-dependent quantity: `S := int (1 + 3w) dln a`. -/
def S (eras : List Era) : ℝ :=
  (eras.map (fun e => stiffness e.w * e.n)).sum

/-- `S` for the common two-era history: inflation, then a later era. -/
def SOf (w₁ n₁ w₂ n₂ : ℝ) : ℝ := stiffness w₁ * n₁ + stiffness w₂ * n₂

/-- What the curvature parameter does over the history: multiplied by `e^S`. -/
def epsFinal (epsI s : ℝ) : ℝ := epsI * Real.exp s

/-- `r_f / r_i = e^(S/2)`: the comoving Hubble radius is multiplied by this. -/
def radiusRatio (s : ℝ) : ℝ := Real.exp (s / 2)

/-- The flatness threshold on `S`.  Negative exactly when `eps_obs < eps_i`. -/
def sRequired (epsObs epsI : ℝ) : ℝ := Real.log (epsObs / epsI)

/-- (F) FLATNESS admissibility. -/
def flatnessAdmissible (s epsObs epsI : ℝ) : Prop := s < sRequired epsObs epsI

/-- (H) HORIZON admissibility.  `S < 0`, i.e. the comoving Hubble radius must
shrink; see the header for why the sign is what it is. -/
def horizonAdmissible (s : ℝ) : Prop := s < 0

/-- A history is admissible iff both sign tests pass. -/
def admissible (s epsObs epsI : ℝ) : Prop :=
  flatnessAdmissible s epsObs epsI ∧ horizonAdmissible s

/-- The inflation length that saturates flatness, given a post-inflationary era
of `nMatter` e-folds at `w = 0`.  Only meaningful when the inflationary era has
negative stiffness, which `nInflNeeded_lt_iff_flat` records as a hypothesis
rather than leaving as a division-by-a-nonpositive-number footnote. -/
def nInflNeeded (epsObs epsI nMatter wInfl : ℝ) : ℝ :=
  (sRequired epsObs epsI - stiffness 0 * nMatter) / stiffness wInfl

/-! ### Additivity and path independence -/

/-- `S` is additive over concatenated eras.  This is the reason `S` -- and not
some other functional -- is the right quantity to compare histories with. -/
theorem S_append (as bs : List Era) : S (as ++ bs) = S as + S bs := by
  simp [S]

/-- `S` is order-independent, hence a function of the history rather than of the
bookkeeping used to write it down. -/
theorem S_reverse (eras : List Era) : S eras.reverse = S eras := by
  simp only [S, List.map_reverse, List.sum_reverse]

/-- Splitting one era into three of the same `w` changes nothing.  The local
form of the same statement as `S_append`. -/
theorem S_split_era (eras : List Era) (e : Era) :
    S (eras ++ [e]) = S eras + stiffness e.w * e.n := by
  simp [S]

/-- Three eras of the same `w` and the same total length as one era. -/
theorem S_split_thirds (w n : ℝ) :
    S [{ w := w, n := n / 3 }, { w := w, n := n / 3 }, { w := w, n := n / 3 }] = stiffness w * n := by
  simp [S]
  ring

/-! ### The sign test is sharp at `w = -1/3` -/

/-- The stiffness vanishes at exactly one value of `w`, namely `w = -1/3`.  This
is a boundary of the scaling laws, and emphatically NOT a solution: with zero
stiffness `S` gets no help from that era, and the matter era still follows. -/
theorem stiffness_zero_iff (w : ℝ) : stiffness w = 0 ↔ w = -1 / 3 := by
  simp only [stiffness]
  constructor
  · intro h
    have h3 : (3 : ℝ) * w = -1 := by linarith
    linarith
  · intro h
    norm_num [h]

/-- Only `w < -1/3` helps. -/
theorem stiffness_neg_of_lt (w : ℝ) (h : w < -1 / 3) : stiffness w < 0 := by
  simp only [stiffness]
  linarith

/-- Only `w > -1/3` hurts. -/
theorem stiffness_pos_of_gt (w : ℝ) (h : -1 / 3 < w) : 0 < stiffness w := by
  simp only [stiffness]
  linarith

/-- The matter era is not free: `w = 0` gives stiffness `+1`, so `n` e-folds of
matter contribute exactly `+n` to `S` and make the horizon problem worse. -/
theorem stiffness_matter (n : ℝ) : stiffness 0 * n = n := by
  simp [stiffness]

/-- de Sitter has stiffness `-2` per e-fold. -/
theorem stiffness_deSitter : stiffness (-1) = (-2 : ℝ) := by
  norm_num [stiffness]

/-! ### Both conditions are EXACTLY sign tests on `S` -/

/-- (F) in the sharp form: `eps_f < eps_obs` is equivalent to `S < S_req`.  No
approximation, and no proxy variable. -/
theorem epsFinal_lt_epsObs_iff (epsObs epsI s : ℝ) (hI : 0 < epsI) (hO : 0 < epsObs) :
    epsFinal epsI s < epsObs ↔ s < sRequired epsObs epsI := by
  have hpos : 0 < epsObs / epsI := div_pos hO hI
  constructor
  · intro h
    rw [epsFinal, ← mul_comm (Real.exp s) epsI] at h
    have h' : Real.exp s < epsObs / epsI := (lt_div_iff₀ hI).mpr h
    have hexp : Real.exp s < Real.exp (Real.log (epsObs / epsI)) := by
      rw [Real.exp_log hpos]
      exact h'
    exact (Real.exp_lt_exp).mp hexp
  · intro h
    have hexp : Real.exp s < Real.exp (Real.log (epsObs / epsI)) := Real.exp_lt_exp.mpr h
    rw [Real.exp_log hpos] at hexp
    rw [epsFinal, ← mul_comm (Real.exp s) epsI]
    exact (lt_div_iff₀ hI).mp hexp

/-- (H) in the sharp form: the comoving Hubble radius shrinks, `r_f < r_i`, if
and only if `S < 0`.  This is where the sign is pinned down; note that `S = 0`
is NOT admissible, which `boundary_inadmissible` also records. -/
theorem radiusRatio_lt_one_iff (s : ℝ) :
    radiusRatio s < 1 ↔ s < 0 := by
  rw [radiusRatio, Real.exp_lt_one_iff]
  constructor <;> intro h <;> linarith

/-- The flatness condition IS the stated `S`-test. -/
theorem flatness_iff_eps (epsObs epsI s : ℝ) (hI : 0 < epsI) (hO : 0 < epsObs) :
    flatnessAdmissible s epsObs epsI ↔ epsFinal epsI s < epsObs :=
  (epsFinal_lt_epsObs_iff epsObs epsI s hI hO).symm

/-- The horizon condition IS the stated `S`-test. -/
theorem horizon_iff_radius (s : ℝ) :
    horizonAdmissible s ↔ radiusRatio s < 1 :=
  (radiusRatio_lt_one_iff s).symm

/-! ### THE LINKING STATEMENT -/

/-- `S_req < 0` whenever the observed curvature is smaller than the assumed
initial curvature.  This is the whole reason flatness can imply horizon: the
two thresholds are ordered, and the ordering is what makes one bind. -/
theorem sRequired_neg (epsObs epsI : ℝ) (hI : 0 < epsI) (hO : 0 < epsObs)
    (hlt : epsObs < epsI) : sRequired epsObs epsI < 0 := by
  have h1 : 0 < epsObs / epsI := div_pos hO hI
  have h2 : epsObs / epsI < 1 := (div_lt_iff₀ hI).mpr (by linarith)
  have h3 := Real.strictMonoOn_log h1 (show (0 : ℝ) < 1 by norm_num) h2
  rwa [Real.log_one] at h3

/-- **THE LINKING THEOREM.**  Flatness admissibility implies horizon
admissibility.  Proved as an implication, so that "one inequality does both
jobs" cannot be quietly upgraded to "they are the same condition" -- see
`horizon_only_band_exists`, which shows they are strictly nested. -/
theorem flatness_implies_horizon (epsObs epsI s : ℝ) (hI : 0 < epsI) (hO : 0 < epsObs)
    (hlt : epsObs < epsI) (hflat : flatnessAdmissible s epsObs epsI) :
    horizonAdmissible s := by
  have hn := sRequired_neg epsObs epsI hI hO hlt
  unfold flatnessAdmissible at hflat
  unfold horizonAdmissible
  linarith

/-- BOTH BOUNDARIES ARE EXCLUDED.  `S = S_req` fails flatness by reflexivity and
`S = 0` fails flatness because `S_req < 0 < S` there, so both conditions are
open.  Worth recording because a proof that accidentally admitted a boundary
would still pass the implication above. -/
theorem boundary_inadmissible (epsObs epsI : ℝ) (hI : 0 < epsI) (hO : 0 < epsObs)
    (hlt : epsObs < epsI) :
    ¬ admissible (sRequired epsObs epsI) epsObs epsI ∧ ¬ admissible 0 epsObs epsI := by
  have hn := sRequired_neg epsObs epsI hI hO hlt
  constructor
  · intro h
    exact lt_irrefl _ h.1
  · intro h
    exact (not_lt_of_ge (le_of_lt hn)) h.1

/-- BOTH ADMISSIBLE means ONE inequality.  Since `S_req < 0`, the conjunction of
the two conditions collapses to the flatness condition alone: the horizon test
is redundant, not an independent requirement.  This is the formal content of
"one inequality does both jobs". -/
theorem admissible_iff_flat_of_neg (epsObs epsI s : ℝ) (hI : 0 < epsI) (hO : 0 < epsObs)
    (hlt : epsObs < epsI) :
    admissible s epsObs epsI ↔ flatnessAdmissible s epsObs epsI := by
  have hn := sRequired_neg epsObs epsI hI hO hlt
  unfold admissible flatnessAdmissible horizonAdmissible
  constructor
  · rintro ⟨h1, _⟩
    exact h1
  · intro h
    exact ⟨h, lt_trans h hn⟩

/-- ...and the nesting is STRICT, not vacuous: the horizon condition holds on a
non-empty band where flatness fails, so flatness is genuinely the binding one
and the horizon test is not merely redundant in every case. -/
theorem horizon_only_band_exists (epsObs epsI : ℝ) (hI : 0 < epsI) (hO : 0 < epsObs)
    (hlt : epsObs < epsI) :
    ∃ s : ℝ, horizonAdmissible s ∧ ¬ flatnessAdmissible s epsObs epsI := by
  have hn := sRequired_neg epsObs epsI hI hO hlt
  refine ⟨(sRequired epsObs epsI) / 2, ?_⟩
  unfold horizonAdmissible flatnessAdmissible
  constructor <;> linarith

/-- **THE THREE ORIGINS SHARE ONE AXIS** - the capstone of the zero thread.  The
window has exactly three decisive values, and they sit on ONE real line, in
strict order, with no perpendicular sub-systems:

1. *the parameter origin* - `w = -1/3` is the UNIQUE zero of the stiffness, the
   single place where both the `eps` and `r` exponents stop evolving;
2. *the horizon origin* - `S = 0`, admissible only strictly below it;
3. *the flatness origin* - `S = sRequired = ln(eps_obs/eps_i) < 0`, strictly
   below the horizon origin, which is exactly why the flatness test is the
   binding one (`flatness_implies_horizon` + `horizon_only_band_exists`).

The illustrative model `w = -1` sits strictly below the parameter origin, on the
helping side, which is the content of `stiffness_deSitter < 0`.  Anything like
"perpendicular zero systems" has no instance here: three distinct values, one
axis, and each is a strict boundary, never a solution. -/
theorem the_three_origins_share_one_axis (epsObs epsI : ℝ) (hI : 0 < epsI)
    (hO : 0 < epsObs) (hlt : epsObs < epsI) :
    (∃! w : ℝ, stiffness w = 0) ∧ sRequired epsObs epsI < 0 ∧ stiffness (-1) < 0 := by
  constructor
  · refine ⟨(-1 / 3), ?_, ?_⟩
    · exact (stiffness_zero_iff (-1 / 3)).2 rfl
    · intro y hy
      exact (stiffness_zero_iff y).1 hy
  · constructor
    · exact sRequired_neg epsObs epsI hI hO hlt
    · rw [stiffness_deSitter]
      norm_num

/-! ### The required inflation length -/

/-- The threshold, in the form actually used.  Inflation length strictly above
`(target - post-inflation contribution) / stiffness` makes the history flat.
Proved in both directions, so the numeric threshold is a theorem about this
formula rather than a constant in a Python string.

The sign flip is the whole point: `stiff < 0`, so dividing reverses the
inequality and the threshold becomes a LOWER bound on the required length.
`div_lt_iff_of_neg` is doing the load-bearing work here. -/
theorem nInflNeeded_lt_iff_flat {stiff target nMatter N : ℝ} (hs : stiff < 0) :
    N > (target - nMatter) / stiff ↔ stiff * N + nMatter < target := by
  have h1 : (target - nMatter) / stiff < N ↔ N * stiff < target - nMatter :=
    div_lt_iff_of_neg hs
  rw [gt_iff_lt, h1]
  constructor <;> intro h <;> linarith

/-- The de Sitter case in the shape of the Python experiment: 80 e-folds of
matter contribute `+80` to `S` and cannot be wished away, so exceeding
`nInflNeeded epsObs epsI 80 (-1)` is EXACTLY what flatness demands. -/
theorem deSitter_threshold_iff (epsObs epsI N : ℝ) :
    N > nInflNeeded epsObs epsI 80 (-1)
      ↔ flatnessAdmissible (SOf (-1) N 0 80) epsObs epsI := by
  have hcore : (sRequired epsObs epsI - stiffness 0 * 80) / stiffness (-1) < N
      ↔ stiffness (-1) * N + stiffness 0 * 80 < sRequired epsObs epsI :=
    nInflNeeded_lt_iff_flat (stiff := stiffness (-1)) (target := sRequired epsObs epsI)
      (nMatter := stiffness 0 * 80) (N := N) (by rw [stiffness_deSitter]; norm_num)
  unfold nInflNeeded flatnessAdmissible
  rw [SOf]
  exact hcore

/-- ...and the same length also delivers the horizon condition, so ONE length
satisfies both.  The threshold is shared, which is the whole claim. -/
theorem deSitter_threshold_admissible (epsObs epsI N : ℝ) (hI : 0 < epsI)
    (hO : 0 < epsObs) (hlt : epsObs < epsI) (hN : N > nInflNeeded epsObs epsI 80 (-1)) :
    admissible (SOf (-1) N 0 80) epsObs epsI := by
  have hflat : flatnessAdmissible (SOf (-1) N 0 80) epsObs epsI :=
    (deSitter_threshold_iff epsObs epsI N).mp hN
  exact ⟨hflat,
    flatness_implies_horizon epsObs epsI (SOf (-1) N 0 80) hI hO hlt hflat⟩

/-- `sRequired` DECREASES as `eps_i` grows: a larger assumed initial curvature
makes the ratio `eps_obs / eps_i` smaller, and `log` is increasing. -/
theorem sRequired_mono (epsObs epsI1 epsI2 : ℝ) (hO : 0 < epsObs) (hI1 : 0 < epsI1)
    (hI2 : 0 < epsI2) (h : epsI1 ≤ epsI2) :
    sRequired epsObs epsI2 ≤ sRequired epsObs epsI1 := by
  have hden : (0 : ℝ) < epsI1 * epsI2 := mul_pos hI1 hI2
  have hsub : (0 : ℝ) ≤ epsObs * (epsI2 - epsI1) :=
    mul_nonneg hO.le (sub_nonneg.mpr h)
  have hid : epsObs / epsI1 - epsObs / epsI2
      = epsObs * (epsI2 - epsI1) / (epsI1 * epsI2) := by
    field_simp
  have hq : (0 : ℝ) ≤ epsObs / epsI1 - epsObs / epsI2 := by
    rw [hid]
    exact div_nonneg hsub hden.le
  have hdiff : epsObs / epsI2 ≤ epsObs / epsI1 := sub_nonneg.mp hq
  exact Real.log_le_log (div_pos hO hI2) hdiff

/-- ...and so the required length GROWS with `eps_i`, weakly: a larger assumed
initial curvature demands more inflation, never less.  The threshold therefore
has a floor set by the smallest `eps_i` and no ceiling. -/
theorem nInflNeeded_mono_epsI (epsObs epsI1 epsI2 : ℝ) (hO : 0 < epsObs) (hI1 : 0 < epsI1)
    (hI2 : 0 < epsI2) (h : epsI1 ≤ epsI2) :
    nInflNeeded epsObs epsI1 80 (-1) ≤ nInflNeeded epsObs epsI2 80 (-1) := by
  have hsr := sRequired_mono epsObs epsI1 epsI2 hO hI1 hI2 h
  have h1 : nInflNeeded epsObs epsI1 80 (-1) = (sRequired epsObs epsI1 - 80) / (-2) := by
    norm_num [nInflNeeded, stiffness]
  have h2 : nInflNeeded epsObs epsI2 80 (-1) = (sRequired epsObs epsI2 - 80) / (-2) := by
    norm_num [nInflNeeded, stiffness]
  rw [h1, h2]
  exact div_le_div_of_nonpos_of_le (by norm_num) (by linarith)

/-! ### The affine law: required length versus measured precision -/

/-- The observational precision a given required length would demand: the exact
INVERSE of `nInflNeeded` in `eps_obs`.  Written as an exponential so that the
round-trip is provable without a case split on the sign of `eps_obs`.

Nothing here is observational.  `nInflNeeded` is affine in `log eps_obs`, so
the two are mutual inverses by algebra alone, for ANY positive `eps_obs`. -/
def epsObsNeededFor (n epsI nMatter wInfl : ℝ) : ℝ :=
  Real.exp (stiffness wInfl * n + stiffness 0 * nMatter) * epsI

/-- **THE AFFINE LAW.**  For fixed `eps_i`, matter era and inflationary `w`, the
required length depends on the measured curvature only through `log eps_obs`:

    `n(eps_2) - n(eps_1) = log(eps_2 / eps_1) / stiffness wInfl`

This is what "each decade of precision buys half an e-fold" means: the increment
is a *constant* set by the slope `1 / (1 + 3w)`, independent of where you are.
No observational number enters, and none is needed. -/
theorem nInflNeeded_affine (eps₁ eps₂ epsI nMatter wInfl : ℝ) (hI : 0 < epsI)
    (hO₁ : 0 < eps₁) (hO₂ : 0 < eps₂) (hs : stiffness wInfl < 0) :
    nInflNeeded eps₂ epsI nMatter wInfl - nInflNeeded eps₁ epsI nMatter wInfl
      = Real.log (eps₂ / eps₁) / stiffness wInfl := by
  have hstiff : stiffness wInfl ≠ 0 := ne_of_lt hs
  have hr : epsI ≠ 0 := ne_of_gt hI
  have h₁ : Real.log (eps₂ / epsI) = Real.log eps₂ - Real.log epsI :=
    Real.log_div hO₂.ne' hr
  have h₂ : Real.log (eps₁ / epsI) = Real.log eps₁ - Real.log epsI :=
    Real.log_div hO₁.ne' hr
  have h₃ : Real.log (eps₂ / eps₁) = Real.log eps₂ - Real.log eps₁ :=
    Real.log_div hO₂.ne' hO₁.ne'
  unfold nInflNeeded sRequired
  rw [h₁, h₂, h₃]
  field_simp
  ring

/-- A LOOSER curvature bound demands weakly LESS inflation.  Equivalently: a
tighter bound demands more, and there is no free lunch in the other direction.

This is the monotonicity that makes `n7k` a statement about precision rather
than about a number: without it, "saturates" would be a slogan. -/
theorem nInflNeeded_anti_mono_epsObs (eps₁ eps₂ epsI nMatter wInfl : ℝ) (hI : 0 < epsI)
    (hO₁ : 0 < eps₁) (hO₂ : 0 < eps₂) (hs : stiffness wInfl < 0) (h : eps₁ ≤ eps₂) :
    nInflNeeded eps₂ epsI nMatter wInfl ≤ nInflNeeded eps₁ epsI nMatter wInfl := by
  have haff := nInflNeeded_affine eps₁ eps₂ epsI nMatter wInfl hI hO₁ hO₂ hs
  have hratio : (1 : ℝ) ≤ eps₂ / eps₁ := (le_div_iff₀ hO₁).mpr (by linarith)
  have hlog : (0 : ℝ) ≤ Real.log (eps₂ / eps₁) := by
    simpa using (Real.log_le_log (by norm_num) hratio)
  have hdiv : Real.log (eps₂ / eps₁) / stiffness wInfl ≤ 0 :=
    div_nonpos_of_nonneg_of_nonpos hlog (le_of_lt hs)
  linarith

/-- Round trip, left to right: measuring at exactly the precision the required
length demands returns that length.  Holds for EVERY real `n`, including
negative ones -- there is no positivity assumption on the length, because none
is needed once the inversion is written exponentially. -/
theorem nInflNeeded_epsObsNeededFor (n epsI nMatter wInfl : ℝ) (hI : 0 < epsI)
    (hs : stiffness wInfl < 0) :
    nInflNeeded (epsObsNeededFor n epsI nMatter wInfl) epsI nMatter wInfl = n := by
  have hr : epsI ≠ 0 := ne_of_gt hI
  have hstiff : stiffness wInfl ≠ 0 := ne_of_lt hs
  unfold epsObsNeededFor nInflNeeded sRequired
  rw [Real.log_div (mul_ne_zero (Real.exp_ne_zero _) hr) hr, Real.log_mul (Real.exp_ne_zero _) hr,
    Real.log_exp]
  field_simp
  ring

/-- Round trip, right to left.  Together with the previous theorem this makes the
two functions genuine mutual inverses, so `n7k` may state a requirement either as
"a length this long needs precision this good" or as "precision this good
certifies a length this long" without the two wordings drifting apart. -/
theorem epsObsNeededFor_nInflNeeded (epsObs epsI nMatter wInfl : ℝ) (hI : 0 < epsI)
    (hO : 0 < epsObs) (hs : stiffness wInfl < 0) :
    epsObsNeededFor (nInflNeeded epsObs epsI nMatter wInfl) epsI nMatter wInfl = epsObs := by
  have hr : epsI ≠ 0 := ne_of_gt hI
  have hstiff : stiffness wInfl ≠ 0 := ne_of_lt hs
  have hkey : stiffness wInfl
        * ((Real.log (epsObs / epsI) - stiffness 0 * nMatter) / stiffness wInfl)
      = Real.log (epsObs / epsI) - stiffness 0 * nMatter := by
    field_simp
  unfold epsObsNeededFor nInflNeeded sRequired
  rw [hkey]
  have hexp : Real.exp (Real.log (epsObs / epsI) - stiffness 0 * nMatter
      + stiffness 0 * nMatter) = epsObs / epsI := by
    have hre : Real.log (epsObs / epsI) - stiffness 0 * nMatter
        + stiffness 0 * nMatter = Real.log (epsObs / epsI) := by ring
    rw [hre, Real.exp_log (div_pos hO hI)]
  rw [hexp]
  field_simp

/-- The de Sitter increment, made exact: a factor of ten in the curvature bound
moves the required length by exactly `log 10 / (-2)`, whatever the starting
point.  The Python quotes "half an e-fold per decade"; `log 10 / 2 = 1.1513` is
what that sentence actually denotes, and here it is a theorem. -/
theorem deSitter_decade_gain (epsObs epsI nMatter : ℝ) (hI : 0 < epsI) (hO : 0 < epsObs) :
    nInflNeeded (10 * epsObs) epsI nMatter (-1) - nInflNeeded epsObs epsI nMatter (-1)
      = Real.log 10 / (-2) := by
  have hs : stiffness (-1) < 0 := by rw [stiffness_deSitter]; norm_num
  have haff := nInflNeeded_affine epsObs (10 * epsObs) epsI nMatter (-1) hI hO
    (mul_pos (by norm_num) hO) hs
  have hid : 10 * epsObs / epsObs = 10 := by field_simp
  rw [hid] at haff
  simpa [stiffness_deSitter] using haff

/-- ...and the sign of that increment is NEGATIVE: a looser bound demands less
inflation.  Equivalently, tightening by a decade demands strictly more, so the
curve has a genuine ceiling rather than running to infinity in practice. -/
theorem deSitter_decade_gain_neg : Real.log 10 / (-2) < 0 :=
  div_neg_of_pos_of_neg (Real.log_pos (by norm_num)) (by norm_num)

/-- Tightening the curvature bound by a decade demands STRICTLY more inflation.
The strictness is the content: it is what rules out a finite length certifying
`~60` e-folds, since any finite target can be met only by a bound that is finite. -/
theorem deSitter_tighter_bound_demands_more (epsObs epsI nMatter : ℝ) (hI : 0 < epsI)
    (hO : 0 < epsObs) :
    nInflNeeded epsObs epsI nMatter (-1) < nInflNeeded (epsObs / 10) epsI nMatter (-1) := by
  have hs : stiffness (-1) < 0 := by rw [stiffness_deSitter]; norm_num
  have haff := nInflNeeded_affine (epsObs / 10) epsObs epsI nMatter (-1) hI
    (div_pos hO (by norm_num)) hO hs
  have hid : epsObs / (epsObs / 10) = 10 := by field_simp
  rw [hid, stiffness_deSitter] at haff
  linarith [deSitter_decade_gain_neg]

/-- The saturating length is EXACTLY the boundary, and so is inadmissible.  This
is `boundary_inadmissible` restated in the length formulation: the single
threshold `nInflNeeded` is a real number, and no choice of history length can
exceed a condition that is already met exactly. -/
theorem saturated_length_is_not_admissible (epsObs epsI nMatter wInfl : ℝ)
    (hs : stiffness wInfl < 0) :
    ¬ flatnessAdmissible (SOf wInfl (nInflNeeded epsObs epsI nMatter wInfl) 0 nMatter) epsObs epsI := by
  have hstiff : stiffness wInfl ≠ 0 := ne_of_lt hs
  have hkey : stiffness wInfl
        * ((Real.log (epsObs / epsI) - stiffness 0 * nMatter) / stiffness wInfl)
      = Real.log (epsObs / epsI) - stiffness 0 * nMatter := by
    field_simp
  intro h
  unfold flatnessAdmissible at h
  unfold nInflNeeded sRequired at h
  rw [SOf, hkey] at h
  linarith

/-- **THE DIVERGENCE AS A THEOREM.**  For ANY finite target length `N` there is a
positive precision `eps_obs` whose requirement already exceeds it.  Together
with `nInflNeeded_anti_mono_epsObs` this turns "the criterion tops out" from a
statement about noise floors into a theorem about the function itself: the
required length is unbounded as the measured curvature tightens.  No
observational number enters; the result is pure algebra from the definitions,
conditional only on `stiffness wInfl < 0` and `eps_i > 0`. -/
theorem nInflNeeded_unbounded_above (epsI nMatter wInfl : ℝ) (hI : 0 < epsI)
    (hs : stiffness wInfl < 0) :
    ∀ N : ℝ, ∃ epsObs, 0 < epsObs ∧ N < nInflNeeded epsObs epsI nMatter wInfl := by
  intro N
  let s : ℝ := nMatter + N * stiffness wInfl - 1
  have hstiff : stiffness wInfl ≠ 0 := ne_of_lt hs
  refine ⟨epsI * Real.exp s, ?pos, ?big⟩
  · exact mul_pos hI (Real.exp_pos s)
  · have hfrac : epsI * Real.exp s / epsI = Real.exp s := by
      field_simp [ne_of_gt hI]
    have hlog : Real.log (epsI * Real.exp s / epsI) = s := by
      rw [hfrac, Real.log_exp]
    unfold nInflNeeded sRequired
    rw [hlog]
    have hsib : s - stiffness 0 * nMatter = N * stiffness wInfl - 1 := by
      dsimp [s]
      rw [stiffness_matter]
      ring
    rw [hsib]
    have hcalc : (N * stiffness wInfl - 1) / stiffness wInfl = N - 1 / stiffness wInfl := by
      field_simp [hstiff]
    rw [hcalc]
    have hinv : (1 / stiffness wInfl : ℝ) < 0 :=
      div_neg_of_pos_of_neg (by norm_num) hs
    linarith

/-- What you actually use: there is a precision `eps_obs` such that EVERY tighter
measurement certifies strictly more than `N`, so the divergeence cannot be
out-run by improving the experiment into a regime where the requirement backs
down.  This is `nInflNeeded_unbounded_above` plus the monotonicity
`nInflNeeded_anti_mono_epsObs`, packaged as the statement that costs nothing to
quote. -/
theorem nInflNeeded_above_persists (epsI nMatter wInfl N : ℝ) (hI : 0 < epsI)
    (hs : stiffness wInfl < 0) :
    ∃ epsObs, 0 < epsObs
      ∧ ∀ eps', 0 < eps' → eps' ≤ epsObs → N < nInflNeeded eps' epsI nMatter wInfl := by
  rcases nInflNeeded_unbounded_above epsI nMatter wInfl hI hs N with ⟨eps0, hpos, hbig⟩
  refine ⟨eps0, hpos, ?_⟩
  intro eps' heps' hle
  have hm := nInflNeeded_anti_mono_epsObs eps' eps0 epsI nMatter wInfl hI heps' hpos hs hle
  exact lt_of_lt_of_le hbig hm

/-! ### The model filter: a verdict rule, not a discovery -/

/-- The mechanical verdict on a model that predicts its own final curvature:
`|omega_k| > eps_obs` falsifies it.

The rule is SIGN-BLIND BY DESIGN.  The statement that actually separates
slow-roll from false-vacuum eternal inflation is a claim about the SIGN of
`omega_k`, i.e. about a model-specific probability distribution, and
`curvatureVerdict_neg` pins that this function cannot express it. -/
def curvatureVerdict (omegaK epsObs : ℝ) : Bool := decide (abs omegaK ≤ epsObs)

/-- The rule is exactly "falsified iff the predicted curvature exceeds the
measured bound".  Stated as an `iff` so that the Python string `"FALSIFIED"`
cannot be a free-floating label. -/
theorem curvatureVerdict_iff_falsified (omegaK epsObs : ℝ) :
    curvatureVerdict omegaK epsObs = false ↔ abs omegaK > epsObs := by
  simp [curvatureVerdict]

/-- **SIGN SYMMETRY, PINNED.**  The verdict ignores which side of flat the model
falls on.  Deliberate: `omega_k < -1e-4` (closed) is the case that would exclude
false-vacuum eternal inflation, and this function does not see it.  Recorded so
the omission cannot later be mistaken for coverage. -/
theorem curvatureVerdict_neg (omegaK epsObs : ℝ) :
    curvatureVerdict (-omegaK) epsObs = curvatureVerdict omegaK epsObs := by
  simp [curvatureVerdict, abs_neg]

/-- The boundary is INCLUSIVE: a model predicting exactly `eps_obs` is not an
excess, so it is admissible.  Note that this DISAGREES with `flatnessAdmissible`,
which is strict; see `curvatureVerdict_boundary_disagrees`, which states the
discrepancy rather than leaving it implicit. -/
theorem curvatureVerdict_at_bound (epsObs : ℝ) (hO : 0 ≤ epsObs) :
    curvatureVerdict epsObs epsObs = true := by
  simp [curvatureVerdict, abs_of_nonneg hO]

/-- TIGHTENING THE BOUND CAN ONLY EXCLUDE MORE.  The comparison is
antisymmetric, so the two directions of the Python's "excluded today" /
"excluded at the threshold" are not independent claims. -/
theorem curvatureVerdict_mono_bound (omegaK epsObs₁ epsObs₂ : ℝ) (h : epsObs₁ ≤ epsObs₂)
    (hf : curvatureVerdict omegaK epsObs₂ = false) :
    curvatureVerdict omegaK epsObs₁ = false := by
  rw [curvatureVerdict_iff_falsified] at hf ⊢
  exact lt_of_le_of_lt h hf

/-- The rule is NOT vacuous as a rule: for every positive bound there EXISTS a
prediction it excludes.  What N7 does not supply is such a prediction -- `eps_i`
is free -- which is the separate, load-bearing limitation recorded by
`filter_leaves_eps_i_free` and by `not_a_beginning_theorem`.  Separating "the
rule works" from "we have nothing to feed it" is the point. -/
theorem curvatureVerdict_excludes_something (epsObs : ℝ) (hO : 0 < epsObs) :
    ∃ omegaK : ℝ, curvatureVerdict omegaK epsObs = false :=
  ⟨epsObs + 1, by
    rw [curvatureVerdict_iff_falsified, abs_of_pos (by linarith : (0 : ℝ) < epsObs + 1)]
    linarith⟩

/-- THE BRIDGE, in the open case.  A model's curvature verdict is not a separate
criterion: it is the FLATNESS test of this file, evaluated at the `S` that
produces that curvature.  Formally, with `s = log(|omega_k| / eps_i)` so that
`epsFinal epsI s = |omega_k|`. -/
theorem curvatureVerdict_bridge_open (omegaK epsObs epsI : ℝ) (hI : 0 < epsI)
    (hO : 0 < epsObs) (hK : omegaK ≠ 0) :
    (abs omegaK < epsObs) ↔ flatnessAdmissible (Real.log (abs omegaK / epsI)) epsObs epsI := by
  have hK' : 0 < abs omegaK := abs_pos.mpr hK
  unfold flatnessAdmissible sRequired
  rw [Real.log_lt_log_iff (div_pos hK' hI) (div_pos hO hI),
    div_lt_div_iff_of_pos_right hI]

/-- **THE BOUNDARY MISMATCH, FOUND AND STATED.**  At exactly
`|omega_k| = eps_obs` the two criteria DISAGREE: `curvatureVerdict` calls it
admissible (no excess) while `flatnessAdmissible` calls it inadmissible (the
strict bound is not met).  Both are defensible in isolation -- a measured
curvature equal to the bound is not an excess, and a saturated history is not a
flat one -- but they are not the same predicate, so `n7l` must not be described
as a restatement of (F) without this caveat.  Machine-checked rather than
asserted, because a boundary convention is exactly the sort of thing that gets
quietly assumed. -/
theorem curvatureVerdict_boundary_disagrees (epsObs epsI : ℝ) (hO : 0 < epsObs) :
    curvatureVerdict epsObs epsObs = true
      ∧ ¬ flatnessAdmissible (Real.log (epsObs / epsI)) epsObs epsI := by
  constructor
  · exact curvatureVerdict_at_bound epsObs hO.le
  · intro h
    unfold flatnessAdmissible at h
    unfold sRequired at h
    exact lt_irrefl _ h

/-! ### The exact curvature law at the `SOf` level -/

/-- The closed-form curvature law with `S` as the exponent:
`eps = 1/(D e^(-S) - sigma)`.  In one era `S = stiffness w * n = (1+3w) ln a`,
so `e^(-S) = a^(-(1+3w))`: this is the experiment's closed form
`eps = 1/(D a^(-1-3w) - sigma)` written without raising a base to a variable
exponent.  `D` is the matching constant fixed by the initial condition,
`sigma` is the curvature shift from `-k = -sigma |k|`. -/
def epsExact (D sigma S : ℝ) : ℝ := 1 / (D * Real.exp (-S) - sigma)

/-- With `sigma = 0` the exact law IS the leading power law.  The `- sigma`
term is therefore the entire difference between the two laws: formal half of
the ``leading laws are ASYMPTOTIC, not identities'' gate (which is a statement
about `sigma != 0`). -/
theorem epsExact_sigma_zero (D S : ℝ) :
    epsExact D 0 S = 1 / (D * Real.exp (-S)) := by
  unfold epsExact
  simp

/-- **THE SOf-LEVEL EXACT LAW.**  The aggregate two-era closed form factors
over eras at the `SOf` level: `e^(-SOf w₁ n₁ w₂ n₂)` is the product of the two
per-era powers, so `eps = 1/(D e^(-SOf) - sigma)` is the same number written
from the factored history.  This is the formal counterpart of ```S`` additive
over eras'' applied to the exact law itself (gate `n7a`'s exponent splitting),
and it is exactly the identity the two-era numeric `SOf` exercises. -/
theorem epsExact_SOf_factor (D sigma w₁ n₁ w₂ n₂ : ℝ) :
    epsExact D sigma (SOf w₁ n₁ w₂ n₂)
      = 1 / (D * (Real.exp (-(stiffness w₁ * n₁)) * Real.exp (-(stiffness w₂ * n₂))) - sigma) := by
  unfold epsExact SOf
  have h : -(stiffness w₁ * n₁ + stiffness w₂ * n₂)
      = -(stiffness w₁ * n₁) + -(stiffness w₂ * n₂) := by ring
  rw [h, Real.exp_add]

/-- `n7b` EXACT: with `X = D e^(-S)` the ratio
`eps_exact / eps_leading = 1/(1 - sigma/X)` is a real-number identity, not a
close approximation (the experiment quotes it to 1e-12). -/
theorem epsExact_leading_ratio (D sigma S : ℝ) (hX : D * Real.exp (-S) ≠ 0)
    (hden : D * Real.exp (-S) - sigma ≠ 0) :
    epsExact D sigma S / (1 / (D * Real.exp (-S)))
      = 1 / (1 - sigma / (D * Real.exp (-S))) := by
  unfold epsExact
  let X : ℝ := D * Real.exp (-S)
  have hX' : X ≠ 0 := by simpa [X] using hX
  have hden' : X - sigma ≠ 0 := by simpa [X] using hden
  change (1 / (X - sigma)) / (1 / X) = 1 / (1 - sigma / X)
  rw [div_div]
  have hprod : (X - sigma) * (1 / X) = 1 - sigma / X := by
    field_simp [hX']
  rw [hprod]

/-- `n7c` EXACT in squared form.  Since `r ∝ eps^(1/2)` (both are multiplied by
`e^(S/2)` per era; see the header), `(r_exact / r_leading)^2 =
eps_exact / eps_leading`, so with `X = D e^(-S)` this identity
`eps_leading / eps_exact = 1 - sigma/X` is the exact content of
`r_exact / r_leading = (1 - sigma/X)^(-1/2)` (square-rooting both sides is
what the experiment does numerically). -/
theorem epsExact_radius_ratio_sq (D sigma S : ℝ) (hX : D * Real.exp (-S) ≠ 0)
    (hden : D * Real.exp (-S) - sigma ≠ 0) :
    1 / (D * Real.exp (-S)) / epsExact D sigma S
      = 1 - sigma / (D * Real.exp (-S)) := by
  unfold epsExact
  let X : ℝ := D * Real.exp (-S)
  have hX' : X ≠ 0 := by simpa [X] using hX
  have hden' : X - sigma ≠ 0 := by simpa [X] using hden
  change (1 / X) / (1 / (X - sigma)) = 1 - sigma / X
  field_simp [hX', hden']

/-! ### The scope tripwire -/

/-- THE TRIPWIRE, part 1.  No value of `eps_i` is excluded by the window: for
every positive `eps_obs, eps_i` there EXISTS an inflation length making the
history admissible.  The filter only sets a required LENGTH.  So `eps_i` cannot
have been derived here, and this file must not be cited as doing so.

The case split is load-bearing rather than cosmetic: when `eps_obs < eps_i` the
flatness threshold is negative and dominates; when `eps_obs >= eps_i` the
threshold is non-negative and the horizon condition dominates instead.  One
condition is always the binding one, never neither. -/
theorem filter_leaves_eps_i_free (epsObs epsI : ℝ) (hO : 0 < epsObs) (hI : 0 < epsI) :
    ∃ N : ℝ, admissible (SOf (-1) N 0 80) epsObs epsI := by
  have hs : stiffness (-1) = (-2 : ℝ) := stiffness_deSitter
  have h0 : stiffness 0 = (1 : ℝ) := by norm_num [stiffness]
  by_cases hlt : epsObs < epsI
  · -- binding condition is flatness: S_req < 0
    refine ⟨80 - sRequired epsObs epsI + 1, ?_⟩
    have hn := sRequired_neg epsObs epsI hI hO hlt
    unfold admissible flatnessAdmissible horizonAdmissible
    rw [SOf, hs, h0]
    constructor <;> linarith
  · -- binding condition is horizon: S_req >= 0
    have hsr : 0 ≤ sRequired epsObs epsI := by
      unfold sRequired
      exact Real.log_nonneg ((le_div_iff₀ hI).mpr (by linarith))
    refine ⟨41, ?_⟩
    unfold admissible flatnessAdmissible horizonAdmissible
    rw [SOf, hs, h0]
    constructor <;> linarith

/-- THE TRIPWIRE, part 2.  There is no theorem here deriving initial conditions.
Recorded explicitly so that no later reader can cite this file as a derivation
of `eps_i`, of a cause, or of a beginning: it is a filter on an assumed
history.  The cosmological counterpart of `not_a_newman_theorem` in
`AcousticZeroFlow.lean`. -/
theorem not_a_beginning_theorem (statement : Prop) : statement → True := fun _ => trivial

end PunoCalculus.Cosmology.OriginWindow