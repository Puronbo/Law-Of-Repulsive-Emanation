# N7 - The Origin Consistency Window: one `S`, two problems, one inequality

Flatness and horizon are normally taught as two separate initial-value problems.
They are one inequality. This node reduces both to sign tests on a single
stiffness integral, solves the curvature law exactly, and states - in one place
- what it does **not** do.

- experiment: `02_Experimental_Implementations_and_Verification/01_Poincare_Universe_and_Cosmological_Models/origin_consistency_window_n7.py`
- tests: `04_Testing_and_Validation_Suite/05_Origin_Consistency_Window_Tests/test_origin_consistency_window_n7.py` (52 passing)
- artifact: `03_Data_and_Observational_Resources/02_Experimental_Data_Collections/origin_consistency_window_n7_data.json`
- Lean: `01_Core_Mathematical_Framework_Lean/02_Cosmology_Submodule/Cosmology/OriginWindow.lean`
- gates: 10 / 10 passing

Reproduce:

```
cd 02_Experimental_Implementations_and_Verification\01_Poincare_Universe_and_Cosmological_Models
python origin_consistency_window_n7.py
cd ..\..\..
python -m pytest 04_Testing_and_Validation_Suite\05_Origin_Consistency_Window_Tests\test_origin_consistency_window_n7.py
cd 01_Core_Mathematical_Framework_Lean\01_Lean
lake build
```

## 1. The reduction

A history of the universe is a curve `a(t)` with an equation of state
`p = w rho`. Define the stiffness density `1 + 3w` and the stiffness integral

```
S := int (1 + 3w) dln a
```

`S` is **additive over eras** and therefore **path independent**: it depends on
which eras occurred and for how long, not on the order in which they are
listed. Splitting one era into two of the same `w` changes nothing. This is the
only history-dependent quantity either problem needs.

Both classical problems reduce to a sign test on `S`:

| condition | requirement | in terms of `S` |
|---|---|---|
| flatness | `eps_f < eps_obs` | `S < S_req`, where `S_req = ln(eps_obs/eps_i)` |
| horizon | `r_f < r_i` | `S < 0` |

The second row is the one that is easy to get backwards, so it is worth stating
carefully. The horizon problem asks that today's observable region fit *inside*
the Hubble patch that existed earlier. Today's region has comoving size
`r_f = 1/(a_f H_f)`; the earlier patch has `r_i = 1/(a_i H_i)`. The requirement
is `r_f < r_i`, and since `r_f / r_i = e^(S/2)`, that is exactly

```
S < 0
```

**The comoving Hubble radius must shrink.** A decelerating era (`w > -1/3`)
contributes `S > 0` and makes it grow. The matter era we live through therefore
contributes `S = +80` all by itself and makes the horizon problem *worse*, not
better.

### The linking statement

Because `eps_obs < eps_i` in any history that has a flatness problem at all,
`S_req = ln(eps_obs/eps_i) < 0` strictly. Hence

```
S < S_req   ==>   S < 0
```

**Flatness admissibility implies horizon admissibility.** One inequality does
both jobs and flatness is the binding one. The two "separate" initial-value
problems are one problem.

This is standard textbook content. What is *not* standard, and what this node
adds, is (a) the exact solved-ODE curvature law below, (b) the machine-checked
formalisation, and (c) the explicit statement of the limits. See
`AXIOM_TO_CONJECTURE.md` in this directory.

## 2. The exact curvature law

From the continuity equation, Friedmann, and the definition of `eps`:

```
rho(a) = rho_i (a/a_i)^(-3(1+w))
H^2    = (8 pi G / 3) rho - k / a^2
eps    = |Omega - 1| = |k| / (a^2 H^2)
```

Fix `a_i = H_i = 1`. Friedmann then gives `rho_i = (3/8pi)(1 + k)`, so with

```
D := (8 pi G/3) rho_i / |k| = (1 + k)/|k|      sigma := sign k
```

we get, **exactly, for any curvature**:

```
a^2 H^2 = |k| (D a^(-1-3w) - sigma)
eps(a)  = 1 / (D a^(-1-3w) - sigma)
```

This is a solved ODE, not an expansion. It is verified against direct
Friedmann integration in gate `n7a` (max rel err `3.3e-16`).

### The sign of `sigma` is load-bearing

Because `-k = -sigma |k|`, the denominator carries **`- sigma`**. For an open
universe (`sigma = -1`) the denominator is `D a^(-1-3w) + 1`, which stays
positive for all `a > 0`. Writing `+ sigma` instead drives `eps` negative at
late time. Since `eps = |Omega - 1|` is a *magnitude*, that is not a small
numerical error but a broken identity - and it is how the sign was caught. The
test `test_the_sigma_sign_is_minus_not_plus` pins both directions: the correct
form stays positive for every `a > 0`, and the wrong form demonstrably does not.

The gates use an open slice (`eps_i_num = 0.01`, `k = -0.01`, `D = 99`,
`rho_i = 0.118173`) because an open universe has no turnaround point, so
`H^2 > 0` for all `a > 0` and the closed form is globally well posed. The
case `eps_i = 1` used for the headline numbers is a degenerate boundary case -
it is the turnaround point of a closed universe and it zeroes `rho_i` for an
open one - which is why the scaling-law gates use a small curvature instead.

### The leading laws are asymptotic, not identities

The familiar power law `eps ~ a^(1+3w)` is the limit of the exact expression
when `X := D a^(-1-3w) >> 1`, and the relation is **exact**:

```
eps_exact / eps_leading = 1 / (1 - sigma/X) = 1 + sigma/X + O(1/X^2)
r_exact   / r_leading   = (1 - sigma/X)^(-1/2)
```

Now note where `X >> 1` lives: `a^(1+3w) << D` is **early** time, which is
exactly the flatness regime the flatness problem is about. So probing the
leading law at large `N` tests nothing but arithmetic.

**A first draft of this node made precisely that mistake**, and its gates were
numerically self-consistent while being physically meaningless. For an open
slice the ratio is `X/(X+1)`, which falls to **zero** as `a -> infinity`; the
leading law overshoots `eps` by orders of magnitude at late time. The regression
test `test_the_leading_laws_are_asymptotic_and_fail_at_late_time` now asserts
the failure, so the vacuous gate cannot come back.

## 3. Gates

| gate | claim | result |
|---|---|---|
| `n7a` | closed form `eps = 1/(D a^(-1-3w) - sigma)` equals direct Friedmann integration | max rel err 3.3e-16 over `w` in {0, 1/2, 1/3, 1}, `N` in {0.05 .. 5} |
| `n7b` | `eps_exact/eps_leading = 1/(1 - sigma/X)` exactly | max rel err < 1e-12 |
| `n7c` | horizon law `r = 1/(aH)` plus `r_exact/r_leading = (1 - sigma/X)^(-1/2)` | max rel err < 1e-12 |
| `n7d` | `S` is additive and order-independent over eras | 4 histories, max deviation 3.6e-15 |
| `n7e` | `S` decreases monotonically in inflation length | `stiffness(de Sitter) = -2 < 0` |
| `n7f` | the flatness threshold lands exactly on `eps_obs` | rel dev < 1e-9 |
| `n7g` | flatness implies horizon over a 120-sample scan of `N_infl` | no counterexample |
| `n7h` | the two conditions are nested, not identical | horizon-only band exists; flat-only band empty |
| `n7i` | `w = -1/3` is invariant but **not** admissible alone | invariance exact; `S = +80` fails flatness |
| `n7j` | `eps_i` remains a free input for every value tried | no value of `eps_i` is excluded |
| `n7k` | the curvature criterion saturates far below the `~60` e-fold convention | unreachable asymptote `45.55`, realistic cap `43.45`; `~60` would need `eps_obs < 4.2e-18` |
| `n7l` | the filter is vacuous without a model prediction, mechanical with one | best verified bound excludes 1/5 probes; a `1e-4` bound would exclude 3/5 |

`n7i` deserves a note, because it is the gate most likely to be misread. At
`w = -1/3` the stiffness *density* vanishes, so `eps` and `r` are exactly
invariant under any length at that `w`. Read carelessly this looks like "the
beginning is free". It is not: `w = -1/3` is a **boundary of the scaling laws**,
not an admissible complete history. The matter era that follows contributes
`S = +80` on its own and destroys admissibility.

`n7j` is the honest limit of the node, and is discussed in §5.

`n7k` and `n7l` are the literature-facing gates. They add two things the
arithmetic above was already carrying but did not state: how sharp the
curvature criterion can ever get (§4.1), and that the filter needs a model to
test before it excludes anything (§4.2). Both are pinned in the artifact's
`scope` block so their attribution and their vacuity condition cannot be dropped.

## 4. The window

Inputs: `eps_obs = 0.011` (flatness precision threshold),
`eps_i = 1.0` (worst case: order-unity initial curvature, **not** tuned),
`N_matter = 80`, `w_infl = -1`.

The threshold's label was wrong until this pass. It read "Planck 2018 `|Omega_k|`
at `z ~ 1080`"; checking `arXiv:1807.06209v4` Sect. 7.3 shows `0.011` is the
**magnitude of the 95% CL central value** of `Omega_k` from the table row
`Omega_K = -0.011^{+0.013}_{-0.012}` - not an upper limit, not 68%, negative in
the fits, and about the present-day universe rather than recombination. Since
`eps_obs` here is a precision threshold, a central value is the wrong kind of
object, so the genuine 95% bound `|Omega_k| < 0.023` is carried alongside it as
`EPS_OBS_PLANCK_2018_UPPER`. The error was conservative in the direction that
matters: a **looser** threshold makes flatness easier and the required length
shorter, so `42.255` cannot be an overstatement.

```
S_req  = ln(eps_obs/eps_i) = -4.509860
N_infl > 42.254930        (de Sitter, then 80 matter e-folds)
```

| `N_infl` | `S` | flatness | horizon | verdict |
|---|---|---|---|---|
| 0 | +80.0 | no | no | INADMISSIBLE |
| 40 | +0.0 | no | no | INADMISSIBLE |
| 42 | -4.0 | no | yes | horizon only |
| 42.25493 | -4.50986 | boundary | yes | INADMISSIBLE (`<`, not `<=`) |
| 45 | -10.0 | yes | yes | ADMISSIBLE |
| 60 | -40.0 | yes | yes | ADMISSIBLE |

The boundary row is deliberate. Admissibility is strict, so `S = S_req` is
*inadmissible*; `n7f` places the threshold exactly on `eps_obs` and the test
suite asserts the strictness in both directions.

### How the number compares with the conventional `~60`

`42.25` is **not** in tension with the conventional figure of roughly 60
e-folds, and it should not be quoted as a prediction of the total. It is the
*exact geometric* flatness threshold for the stated inputs and nothing else. The
conventional figure carries modelling that this node deliberately omits:

- **quantum diffusion**, which produces e-folds stochastically and typically
  requires a few more than the geometric minimum;
- **overshoot**, i.e. the requirement that flatness be maintained with margin
  through reheating and the whole subsequent history rather than landing exactly
  on `eps_obs` at the end of the matter era;
- the choice of where "the beginning" is placed, and of `N_matter`.

Read `42.25` as a **floor for the geometric part only**. The conventional `~60`
is an upper estimate under richer assumptions. Neither number is derived from
the other, and this node does not adjudicate between them.

Sensitivity, from `N_infl = (S_req - N_matter)/(1 + 3 w_infl)`:

| dependence | derivative |
|---|---|
| `N_matter` | `+1/2` per e-fold |
| `ln eps_i` | `+1/2` |
| `ln eps_obs` | `-1/2` |
| `w_infl` | through `1/(1 + 3 w_infl)`; **no finite solution at all** when `w_infl >= -1/3` |

The `w_infl >= -1/3` row is not a technicality. If the era cannot shrink `S`,
flatness is unreachable - not easier, unreachable - and the node returns `inf`
rather than a large number.

### 4.1 How sharp the criterion can ever get (`n7k`)

Because `dN_infl/dln(eps_obs) = 1/(1 + 3 w_infl) = -1/2` exactly, the required
length is **affine in `ln eps_obs`**. Inverting it gives the precision a
measurement would need in order to certify a given length by curvature alone:

```
eps_obs_needed_for(N) = eps_i * exp( N * (1 + 3 w_infl) + N_matter )
```

| curvature bound | source | `N_infl` required |
|---|---|---|
| `0.023` | Planck 2018 95% **upper limit** on `\|Omega_k\|` | `> 41.89` |
| `0.011` | Planck 2018 95% **central value** magnitude - **not a bound**, see §4 | `> 42.25` |
| `5e-3` | current constraint, as quoted in Leonard et al. (2016) | `> 42.65` |
| `1e-3` | "most likely achievable for the foreseeable future" (same) | `> 43.45` |
| `1e-4` | Kleban & Schillo (2012) threshold | `> 44.61` |
| `1.5e-5` | cosmic-variance **noise level** (Leonard et al. 2016) | `> 45.55` |
| `4.2e-18` | what `~60` e-folds would demand | `= 60` |

The affine law that makes this table meaningful is no longer a numerical
reproduction of a formula in a Python string: `nInflNeeded_affine` proves
`n(e2) - n(e1) = ln(e2/e1)/(1+3w)` for every positive `eps_obs`, with no
observational input at all, and `nInflNeeded_epsObsNeededFor` /
`epsObsNeededFor_nInflNeeded` prove the two directions of the inverse. The
"half an e-fold per decade" sentence is `deSitter_decade_gain`: the increment is
exactly `ln 10 / (-2)` from any starting point, and
`deSitter_tighter_bound_demands_more` shows it is strictly negative, so
tightening strictly increases the requirement. That strictness - not the value
of any constant - is what rules out certifying `~60` at any finite precision.

Every bound feeding a gate was read off a primary source. ACT DR6 is expected to
tighten the `5e-3` figure, but no primary-source `Omega_k` limit for it was
located, so it is recorded in the artifact as `EPS_OBS_ACT_DR6_UNVERIFIED` and
drives no verdict. That makes the comparison in §4.2 conservative rather than
optimistic.

Two things follow, and the second is the one that matters.

First, **the practical limit is a precision limit, not a mathematical one**. The
formal requirement diverges as `eps_obs -> 0`; each decade of curvature
precision buys half an e-fold, forever. That divergence is no longer a numeric
accident: `nInflNeeded_unbounded_above` proves that every finite target is met by
some precision and, with `nInflNeeded_above_persists`, that every tighter
measurement still demands strictly more. What stops it is that `1.5e-5` is not an
accuracy limitation but a **cosmic-variance noise level**: with a single universe
you cannot measure its curvature better than the variance of modes you never
observed.

Note carefully what `45.55` is: an **unreachable asymptote**. Leonard et al. judge
that floor unattainable even by Stage IV and give `~1e-3` as "the most likely
achievable constraint for the foreseeable future", i.e. `N_infl > 43.45` - a
*lower*, realistic cap. So the ladder runs `41.89` (Planck 95% upper limit),
`43.45` (attainable ceiling), `45.55` (never attainable). Certifying `~60` by
curvature alone would need `|Omega_k| < 4.2e-18` - twelve and a half decades
below the floor, and thus not reachable in principle rather than not yet reached.

Two qualifications belong here, because the same paper supplies them. The `43.45`
figure follows from their *conservative* forecasts, and is avoidable under
"strong assumptions ... about dark energy evolution and the `Lambda`CDM parameter
values" - fixing other parameters to high precision is unrealistic, but it is not
excluded. And they state explicitly that their result "does not mean that the
curvature floor is unreachable in principle". Neither qualification rescues the
`~60` target, which needs `1e-18`; both do mean the `43.45` ceiling is a forecast
about planned surveys, not a bound.

Second, **the `~60` figure cannot be obtained from flatness alone**. The usual
arguments for 60 e-folds rest on observable quantities other than curvature -
horizon-exit fluctuations, the scalar spectrum, `r` - and the node takes no
position on them. Reading `45.55` as a competing estimate of the total inflation
length would be a misreading: it is the ceiling of one criterion, not an
alternative to the convention.

The floor and the threshold are borrowed results. The arithmetic relating them
is this node's, and it is elementary.

### 4.2 The filter needs a model to test (`n7l`)

The window excludes histories, but only against a value of `eps_obs`. It
therefore has no purchase on *inflation model space* unless a model predicts its
own final curvature. Given such a prediction the verdict is mechanical:

```
curvature_verdict(omega_k_model, eps_obs)
    = "admissible"  if |omega_k_model| <= eps_obs
    = "FALSIFIED"   otherwise
```

The asymmetry that makes this interesting is observational, not formal:
Kleban & Schillo (2012) show that resolving `|Omega_k|` to `1e-4` would exclude
slow-roll eternal inflation, and that `Omega_k < -1e-4` would exclude all
eternal inflation including the false-vacuum case. The best bound verified from a
primary source here is `5e-3`, a full `50x` looser, so **the test is not yet
live**: of the five probe models, one is excluded today and three would be at the
threshold.

Three constraints on how this gate may be read, plus one discrepancy
formalisation actually found:

- **The vacuity condition is load-bearing.** Without a model-supplied
  `Omega_k` the filter is empty, because `eps_i` is free (`n7j`). `n7l` is a
  wrapper, not evidence about which inflation models survive. The rule itself is
  not vacuous - `curvatureVerdict_excludes_something` proves a excluded model
  exists for every positive bound - which is exactly why the supply of
  predictions, not the rule, is the limitation.
- **Only `|Omega_k|` is tested.** The SREI/FVEI discrimination is a *sign*
  statement about a model-specific probability distribution, and is deliberately
  not implemented. `curvatureVerdict_neg` proves the function is symmetric in
  the sign, so the `Omega_k < -1e-4` (closed) case is provably unreachable
  through it.
- **The boundary disagrees with the window, and this is stated rather than
  buried.** The `<=` above makes `|omega_k| = eps_obs` *admissible*, while the
  window's own (F) is strict and makes `S = S_req` *inadmissible*.
  `curvatureVerdict_bridge_open` proves the two agree on the open case - the
  verdict genuinely IS the flatness test evaluated at the `S` producing that
  curvature - and `curvatureVerdict_boundary_disagrees` proves they diverge
  exactly at the boundary. Both conventions are defensible alone (an excess
  requires a positive margin; a saturated history is not a flat one), but they
  are not the same predicate, so this wrapper must not be called a restatement
  of (F) without the caveat. Reconciling them is a modelling decision and is
  deliberately left open.
- **Attribution.** That measured curvature can falsify eternal inflation is
  Kleban & Schillo's result (`arXiv:1202.5037`). What this node contributes is
  the mechanical wrapper - one stiffness, a sign test, a strict boundary - that
  turns a model's own prediction into a verdict without further argument.

## 5. The Lean layer

`01_Core_Mathematical_Framework_Lean/02_Cosmology_Submodule/Cosmology/OriginWindow.lean`,
namespace `PunoCalculus.Cosmology.OriginWindow`. No `sorry`, no `admit`, no new
axiom; `#print axioms` on every exported theorem returns only
`[propext, Classical.choice, Quot.sound]`.

Structure:

- `stiffness`, `S` (over a list of eras), `SOf` (two eras), `epsFinal`,
  `radiusRatio`, `sRequired`, `nInflNeeded`
- `flatnessAdmissible`, `horizonAdmissible`, `admissible`

Additivity and path independence:

- `S_append` - `S (as ++ bs) = S as + S bs`
- `S_reverse` - `S eras.reverse = S eras`, i.e. order independence
- `S_split_era`, `S_split_thirds` - splitting an era changes nothing
- `stiffness_zero_iff` - the stiffness density vanishes **iff** `w = -1/3`
- `stiffness_neg_of_lt`, `stiffness_pos_of_gt` - only `w < -1/3` helps
- `stiffness_matter`, `stiffness_deSitter` - `+1` per matter e-fold, `-2` per
  de Sitter e-fold

The two conditions:

- `epsFinal_lt_epsObs_iff` - `eps_f < eps_obs <-> S < S_req`
- `flatness_iff_eps`, `horizon_iff_radius` - the two equivalences in the sharp
  forms `eps_f < eps_obs <-> S < S_req` and `r_f < r_i <-> S < 0`
- `radiusRatio_lt_one_iff` - `r_f < r_i <-> exp(S/2) < 1 <-> S < 0`
- `sRequired_neg` - `eps_obs < eps_i ==> S_req < 0`

The linking layer:

- `flatness_implies_horizon` - **the node's central theorem**
- `admissible_iff_flat_of_neg` - admissibility collapses to flatness
- `boundary_inadmissible` - `S = S_req` fails, because `<` is strict
- `horizon_only_band_exists` - the conditions are nested, not identical, so the
  linking theorem is not vacuous
- `the_three_origins_share_one_axis` - the capstone of the zero thread: the
  unique stiffness zero `w = -1/3`, the horizon origin `S = 0` and the flatness
  origin `S = sRequired < 0` are three distinct values on ONE axis, each a
  strict boundary, never a solution

The threshold:

- `nInflNeeded_lt_iff_flat` - `N > N_star <-> flatness`, for `stiffness < 0`
- `deSitter_threshold_iff`, `deSitter_threshold_admissible`
- `sRequired_mono`, `nInflNeeded_mono_epsI` - a larger assumed `eps_i` demands
  weakly more inflation, never less

The affine law and the inverse (what §4.1 actually rests on, now proved rather
than reproduced):

- `epsObsNeededFor` - the inverse of `nInflNeeded` in `eps_obs`, written
  exponentially so the round-trip needs no case split
- `nInflNeeded_affine` - `n(e2) - n(e1) = ln(e2/e1)/(1+3w)`, for every positive
  `eps_obs`; no observational number enters
- `nInflNeeded_anti_mono_epsObs` - looser bound, weakly less required length
- `nInflNeeded_epsObsNeededFor`, `epsObsNeededFor_nInflNeeded` - mutual inverses
- `deSitter_decade_gain` - the increment is exactly `ln 10 / (-2)` from any
  start; `deSitter_decade_gain_neg` fixes its sign
- `deSitter_tighter_bound_demands_more` - tightening is strictly increasing;
  this strictness is what rules out a finite length certifying `~60`
- `saturated_length_is_not_admissible` - the boundary statement in the length
  formulation: no length can exceed a condition already met exactly
- `nInflNeeded_unbounded_above` - THE DIVERGENCE AS A THEOREM: for every finite
  target length `N` there is an `eps_obs > 0` whose requirement already exceeds
  it, so `45.55` is not a ceiling but middle ground of an unbounded function
- `nInflNeeded_above_persists` - the divergence cannot be out-run: once a
  precision passes a target, every tighter measurement still demands strictly
  more

The model filter (the §4.2 wrapper, as a decidable predicate):

- `curvatureVerdict`, `curvatureVerdict_iff_falsified` - "FALSIFIED" is exactly
  `|omega_k| > eps_obs`, not a string
- `curvatureVerdict_neg` - sign-symmetric by construction, so the SREI/FVEI
  discrimination is provably out of reach of this function
- `curvatureVerdict_at_bound`, `curvatureVerdict_mono_bound` - the boundary is
  inclusive, and tightening the bound can only exclude more
- `curvatureVerdict_excludes_something` - not vacuous as a rule
- `curvatureVerdict_bridge_open` - the verdict IS the flatness test, open case
- `curvatureVerdict_boundary_disagrees` - at `|omega_k| = eps_obs` the verdict
  and `flatnessAdmissible` DISAGREE; a discrepancy found and stated, not
  assumed away

The scope tripwires, formalised so that they cannot be quietly dropped:

- `filter_leaves_eps_i_free` - admissibility imposes **no** constraint on
  `eps_i`; the filter never excludes a value
- `not_a_beginning_theorem` - records that this file contains no theorem about
  the beginning, so it cannot be cited as one

**Known Lean gap.** The exact curvature law
`eps = 1/(D a^(-1-3w) - sigma)` is verified **numerically** by `n7a` and is
*not* formalised. The Lean layer formalises the `S`-algebra and the two sign
tests, which is where the argument actually lives; the ODE solution is not
proved.

## 6. What this does not establish

1. **Nothing derives an initial condition.** `eps_i = |Omega_i - 1|` is an
   **input**. Nothing in this file fixes it, and gate `n7j` exists to make that
   visible: every value tried yields a finite required length.
2. **Admissibility is therefore not a selection principle.** A filter that can
   never exclude anything cannot explain why the universe had an admissible
   history. It can only say what an admissible history must look like once
   assumed.
3. **The cause and the beginning are not addressed.** This node filters
   histories; it does not produce initial conditions, does not explain why there
   is a history, and says nothing about what preceded it.
4. **Conditional on FLRW + GR.** The whole reduction presumes a homogeneous
   isotropic background in general relativity. It says nothing about whether
   those premises hold near a boundary.
5. **`w_infl = -1` is exact de Sitter.** Real quasi-de Sitter inflation has
   `w = -1 + small`, which changes the **number** of e-folds required but not
   the sign test on `S`: only `w < -1/3` contributes negatively.
6. **The linking statement is standard.** "Flatness solves horizon" is textbook
   cosmology. The contribution here is the exact solved-ODE curvature law, the
   machine-checked formalisation, and the explicit limit statement - not a new
   prediction.
7. **The curvature law is not formalised in Lean** (§5).
8. **`eps_obs` is a precision threshold, and its label was WRONG until this
   pass.** The audit of `arXiv:1807.06209v4` (Sect. 7.3) shows `0.011` is the
   magnitude of the 95% CL central value of `Omega_k` (`-0.011^{+0.013}_{-0.012}`)
   for the present-day universe, not a recombination-era bound; the genuine
   `95%` limit is `|Omega_k| < 0.023`. The rung now enters as a labelled
   constant, with the mislabel recorded (rows 5, 5a, 58) rather than deleted.
9. **The saturation is a statement about the criterion, not about inflation.**
   `45.55` is the ceiling of what *flatness alone* can certify (§4.1). It is not
   an upper bound on the inflation length, and not a rival to the `~60`
   convention, which rests on other observables.
10. **`n7l` excludes nothing on its own.** The curvature test of inflation model
    space requires a model that predicts `Omega_k`, and the required precision is
    `50x` beyond the best verified bound (§4.2). Until both hold, `n7l` is a
    mechanism with nothing to act on.
11. **The attribution is not this node's.** The `1.5e-5` noise level and the
    `~1e-3` foreseeable bound are Leonard, Bull & Allison (2016),
    `arXiv:1604.01410`; the `1e-4` threshold and the eternal-inflation
    discrimination are Kleban & Schillo (2012), `arXiv:1202.5037`. What is
    contributed here is the exact solved-ODE law, the formalisation, and the
    mechanical wrapper - arithmetic, not a new observational claim.

## 7. Why it is still worth having

The useful result here is partly negative, and the negative part is the
informative one. N7 says something precise about what would be *needed* to
solve the origin problems, and it shows that the answer does not exist in the
direction one might hope:

- The two problems collapse to **one** inequality, and flatness binds. That is a
  real structural fact, and it means there is only one thing to explain rather
  than two.
- But the thing to be explained is a **boundary value** (`eps_i`), not a
  mechanism. The filter says nothing about how `eps_i` gets to be small.
- `w = -1/3` is a degenerate, *invariant* direction of the scaling laws. It is
  the closest thing to a "free beginning" the algebra offers, and it is not a
  solution.
- The threshold has a **floor** set by the smallest `eps_i` and no ceiling: a
  larger assumed initial curvature only ever demands more inflation.
- Sharpening the *observation* runs into a hard wall. Since the requirement is
  affine in `ln eps_obs` with slope `-1/2`, better curvature buys half an e-fold
  per decade - but only down to the `1.5e-5` cosmic-variance floor, so this
  criterion saturates at `45.55` and cannot certify `~60` at any precision (§4.1).
  Flatness is a weak observable, and the weakness is geometric rather than
  instrumental.
- The same `S` that certifies a history can also *falsify* a model that predicts
  its own curvature. That is the one place this node bites on something other
  than the assumed history - and it is currently a wrapper awaiting both a model
  prediction and roughly one further decade of curvature precision (§4.2).

So the concrete next question this node raises is not "does one inequality solve
both problems" - it does - but: **what sets `eps_i`?** Everything downstream of
that number is a closed-form ODE. The entire remaining content of the flatness
and horizon problems is concentrated in one initial datum that this node, by
construction, leaves free.

That is also why `AXIOM_TO_CONJECTURE.md` exists in this directory: to record,
in one table, exactly which of these statements is assumed, which is proved,
and which is open.
