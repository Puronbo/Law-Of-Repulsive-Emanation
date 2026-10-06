# N7 - Axiom to conjecture: what is assumed, proved, and open

A single table for the Origin Consistency Window. The purpose is that no claim
in this node can be upgraded by re-reading it: every line says which of the
three categories it belongs to, and the categories are not negotiable at
read time.

Companion to `ORIGIN_CONSISTENCY_WINDOW.md` in this directory.

## Status vocabulary

- **ASSUMED** - taken as input. Not established here, not argued for, not
  derived. If the assumption fails, every result below it fails.
- **PROVED (Lean)** - machine-checked in
  `01_Core_Mathematical_Framework_Lean/02_Cosmology_Submodule/Cosmology/OriginWindow.lean`.
  No `sorry`, no `admit`, no new axiom; `#print axioms` yields only
  `[propext, Classical.choice, Quot.sound]`.
- **PROVED (numeric)** - closed form or identity verified against an independent
  computation to the quoted tolerance. Not a proof; a check with teeth.
- **PROVED (textbook)** - standard published result, cited not re-derived. The
  node is not the source.
- **OPEN** - genuinely unresolved, and left unresolved on purpose.
- **NOT ADDRESSED** - outside the node's scope by construction. Not a gap to be
  quietly filled later.

## The table

| # | Statement | Status | Where |
|---|---|---|---|
| 1 | The universe is well described by a homogeneous isotropic background (FLRW) | **ASSUMED** | premise of the whole reduction |
| 2 | Gravity is general relativity | **ASSUMED** | Friedmann and acceleration equations |
| 3 | The equation of state is `p = w rho` with `w` piecewise constant over eras | **ASSUMED** | `s_of_path`, era model |
| 4 | `eps = \|Omega - 1\| = \|k\| / (a^2 H^2)` | **ASSUMED** | definition |
| 5 | `eps_obs = 0.011` - the flatness precision threshold | **ASSUMED** | modelling choice, and a number whose label was WRONG until this pass. `0.011` is the magnitude of the 95% CL *central value* of `Omega_k` from Planck 2018 VI (`arXiv:1807.06209v4`, Sect. 7.3, table row `Omega_K = -0.011^{+0.013}_{-0.012}`), **not** an upper limit, not 68%, and negative in the fits. Since `eps_obs` here is a precision threshold, a central value is the wrong kind of object; the genuine 95% bound `|Omega_k| < 0.023` is carried as `EPS_OBS_PLANCK_2018_UPPER`. The mislabel is recorded in `VERIFICATION_LEDGER` rather than deleted. See rows 48-59. |
| 5a | The `0.011` mislabel could not have inflated any result | **PROVED (numeric)** | `n7k`: a LOOSER threshold makes flatness *easier* and the required length *shorter*, so `42.255` is an underestimate of the requirement under a looser bound, never an overstatement. |
| 6 | `eps_i = 1.0` - order-unity initial curvature | **ASSUMED** | worst case, deliberately *not* tuned |
| 7 | `N_matter = 80` post-inflation matter e-folds | **ASSUMED** | modelling choice |
| 8 | `w_infl = -1`, exact de Sitter | **ASSUMED** | exact and single-parameter |
| 9 | `S := int (1 + 3w) dln a` is additive over eras, hence path independent | **PROVED (Lean)** | `S_append`, `S_reverse`, `S_split_era`, `S_split_thirds` |
| 10 | The stiffness density vanishes iff `w = -1/3` | **PROVED (Lean)** | `stiffness_zero_iff` |
| 11 | Only `w < -1/3` contributes negatively to `S` | **PROVED (Lean)** | `stiffness_neg_of_lt`, `stiffness_pos_of_gt` |
| 12 | `eps_f < eps_obs <-> S < ln(eps_obs/eps_i)` | **PROVED (Lean)** | `epsFinal_lt_epsObs_iff`, `flatness_iff_eps` |
| 13 | `r_f < r_i <-> S < 0` (comoving Hubble radius must shrink) | **PROVED (Lean)** | `horizon_iff_radius`, `radiusRatio_lt_one_iff` |
| 14 | `eps_obs < eps_i ==> S_req < 0` | **PROVED (Lean)** | `sRequired_neg` |
| 15 | **Flatness admissibility implies horizon admissibility** | **PROVED (Lean)** | `flatness_implies_horizon` |
| 16 | Admissibility collapses to flatness alone when `S_req < 0` | **PROVED (Lean)** | `admissible_iff_flat_of_neg` |
| 17 | The conditions are nested, not identical - a horizon-only band exists | **PROVED (Lean)** | `horizon_only_band_exists`; numeric `n7h` |
| 18 | Strictness: `S = S_req` is inadmissible | **PROVED (Lean)** | `boundary_inadmissible` |
| 19 | `N_infl > N_star <-> flatness`, for `stiffness < 0` | **PROVED (Lean)** | `nInflNeeded_lt_iff_flat` |
| 20 | Larger `eps_i` demands weakly more inflation, never less | **PROVED (Lean)** | `sRequired_mono`, `nInflNeeded_mono_epsI` |
| 21 | No finite inflation length exists when `w_infl >= -1/3` | **PROVED (Lean)** | `nInflNeeded` returns `inf`; numeric gate |
| 22 | `eps = 1/(D a^(-1-3w) - sigma)` exactly, for any curvature | **PROVED (numeric)** | `n7a`, max rel err 3.3e-16 |
| 23 | `eps_exact/eps_leading = 1/(1 - sigma/X)` exactly | **PROVED (numeric)** | `n7b`, < 1e-12 |
| 24 | `r_exact/r_leading = (1 - sigma/X)^(-1/2)` exactly | **PROVED (numeric)** | `n7c`, < 1e-12 |
| 25 | The leading laws hold only for `X = D a^(-1-3w) >> 1`, i.e. early time | **PROVED (numeric)** | ratio falls to 0 as `a -> inf`; regression test |
| 26 | `N_infl > 42.25493` for the stated inputs | **PROVED (numeric)** | `n7f`, rel dev < 1e-9 |
| 27 | `w = -1/3` leaves `eps` and `r` exactly invariant at any length | **PROVED (numeric)** | `n7i` |
| 28 | "Flatness resolves the horizon problem" | **PROVED (textbook)** | not this node's contribution |
| 29 | **`eps_i` is an INPUT; nothing here fixes it** | **PROVED (Lean), and this is the main limit** | `filter_leaves_eps_i_free`; gate `n7j` |
| 30 | Admissibility excludes **no** value of `eps_i`, so it is not a selection principle | **PROVED (Lean)** | `filter_leaves_eps_i_free` |
| 31 | **What sets `eps_i`** | **OPEN** | the entire remaining content of the problem |
| 32 | Whether FLRW + GR remain valid at the boundary where this matters | **OPEN** | premise 1 and 2 are untested at that regime |
| 33 | The exact curvature law as a Lean proof | **OPEN** | numeric gate only; no formalisation |
| 34 | `dN_infl/dln(eps_obs) = 1/(1 + 3 w_infl) = -1/2`, i.e. the required length is affine in `ln eps_obs` | **PROVED (numeric)** | `n7k`; exact inversion `eps_obs_needed_for` |
| 35 | The curvature criterion reaches an **unreachable asymptote** at `N_infl > 45.5536` on the `1.5e-5` cosmic-variance noise level | **PROVED (numeric), ATTRIBUTED level** | `n7k`; noise level is Leonard, Bull & Allison 2016 (`arXiv:1604.01410`), not this node's |
| 36 | Certifying `~60` by flatness alone would need `\|Omega_k\| < 4.2e-18` | **PROVED (numeric)** | `n7k`; 12.5 decades below the floor, so unreachable in principle |
| 37 | A model predicting its own curvature is falsified iff `\|omega_k\| > eps_obs` | **PROVED (numeric)** | `n7l`; `curvature_verdict`, boundary inclusive |
| 38 | The saturation is a PRECISION limit, not a mathematical ceiling | **PROVED (Lean - see row 60)** | now `nInflNeeded_unbounded_above`; the divergence is a theorem, and `log(0)` raising `ValueError` is its numeric shadow |
| 39 | `curvature_verdict` is symmetric in sign; the SREI/FVEI sign test | **OPEN / DELIBERATELY OMITTED** | sign statement about a model-specific distribution, not implemented |
| 40 | Any inflation model's own `Omega_k` prediction | **OPEN** | without one, `n7l` excludes nothing; the filter is vacuous |
| 41 | Whether `\|Omega_k\|` can be resolved to `1e-4`, which would make the eternal-inflation sign test live | **OPEN (observational)** | best verified bound `5e-3` is `50x` looser; Kleban & Schillo 2012 (`arXiv:1202.5037`) |
| 42 | Quantum diffusion, overshoot, reheating history | **NOT ADDRESSED** | omitted by construction |
| 43 | The cause of the history, and what preceded it | **NOT ADDRESSED** | `not_a_beginning_theorem` records this formally |
| 44 | Initial conditions of any kind | **NOT ADDRESSED** | `not_a_beginning_theorem` |
| 45 | The foreseeable cap is `N_infl > 43.45` at `eps_obs ~ 1e-3`, below the `45.55` asymptote | **PROVED (numeric), ATTRIBUTED forecast** | `n7k`; Leonard et al. call `1e-3` "the most likely achievable constraint ... for the foreseeable future" — a *conservative forecast*, avoidable under strong ΛCDM/dark-energy assumptions, and **not** unreachable in principle by their own statement |
| 46 | A tighter ACT DR6 curvature limit | **UNVERIFIED - EXCLUDED FROM GATES** | recorded as `EPS_OBS_ACT_DR6_UNVERIFIED`; drives no verdict, so §4.2 is conservative |
| 47 | Whether every gated observational input traces to a primary source | **VERIFIED (numeric)** | `test_every_gated_observational_input_has_a_verified_source` pins each constant to its arXiv id; an earlier pass carried three unsourced numbers, now corrected |
| 48 | `N_infl` is affine in `ln eps_obs`: `n(e2) - n(e1) = ln(e2/e1)/(1+3w)` | **PROVED (Lean)** | `nInflNeeded_affine`; holds for every positive `eps_obs`, no observational input needed |
| 49 | `n_infl_needed` and `eps_obs_needed_for` are mutual inverses | **PROVED (Lean)** | `nInflNeeded_epsObsNeededFor`, `epsObsNeededFor_nInflNeeded` |
| 50 | A decade in the bound moves the requirement by exactly `ln 10 / (-2)` | **PROVED (Lean)** | `deSitter_decade_gain`, `deSitter_decade_gain_neg` - the "half an e-fold per decade" sentence, with `ln 10 / 2 = 1.1513` identified as the constant |
| 51 | Tightening the bound demands STRICTLY more inflation | **PROVED (Lean)** | `deSitter_tighter_bound_demands_more`; the strictness is what rules out any finite length certifying `~60` |
| 52 | The saturating length sits exactly on the boundary and is inadmissible | **PROVED (Lean)** | `saturated_length_is_not_admissible` - `boundary_inadmissible` restated in the length formulation |
| 53 | The model filter is a decidable predicate, and is SIGN-BLIND by design | **PROVED (Lean)** | `curvatureVerdict`, `curvatureVerdict_iff_falsified`, `curvatureVerdict_neg` - sign symmetry pinned, so the `Omega_k < -1e-4` case separating SREI from FVEI is provably unreachable through this function |
| 54 | The filter is not vacuous *as a rule*; only as a supply of predictions | **PROVED (Lean)** | `curvatureVerdict_excludes_something` shows a excluded model exists for every positive bound; what N7 lacks is one to feed it (rows 40, 29-30) |
| 55 | The curvature verdict *is* the flatness test (F), in the open case | **PROVED (Lean)** | `curvatureVerdict_bridge_open` |
| 56 | **At `|Omega_k| = eps_obs` the two criteria DISAGREE** | **PROVED (Lean) - a discrepancy formalisation found** | `curvatureVerdict_boundary_disagrees`: `curvatureVerdict` calls it admissible (no excess), `flatnessAdmissible` calls it inadmissible (strict bound unmet). Both conventions are defensible alone; they are not the same predicate |
| 57 | Which boundary convention the model filter *should* use | **OPEN - modelling decision, not a theorem** | deliberately not closed; the disagreement is recorded so it cannot be quietly assumed |
| 58 | `0.011` was mislabelled "`\|Omega_k\|` at recombination (Planck 2018)" | **CORRECTED - source retrieved** | `arXiv:1807.06209v4` Sect. 7.3: it is the magnitude of the 95% CL *central value* (`Omega_K = -0.011^{+0.013}_{-0.012}`), not a bound; genuine 95% limit `\|Omega_k\| < 0.023` now carried as `EPS_OBS_PLANCK_2018_UPPER`. See rows 5, 5a |
| 59 | All new N7 theorems rest only on the three standard axioms | **VERIFIED (Lean)** | `#print axioms` on all 18 N7 additions returns `[propext, Classical.choice, Quot.sound]` |
| 60 | **The requirement DIVERGES as `eps_obs -> 0`** | **PROVED (Lean) - promoted from numeric** | `nInflNeeded_unbounded_above`: for every finite target `N` there is an `eps_obs > 0` whose requirement already exceeds it. Row 38 moves from `PROVED (numeric)` (a `log(0)` `ValueError`) to a theorem about the function itself; no observational value is used |
| 61 | Once a precision exceeds a target, EVERY tighter measurement does too | **PROVED (Lean)** | `nInflNeeded_above_persists` - `nInflNeeded_unbounded_above` + `nInflNeeded_anti_mono_epsObs`, so the divergence cannot be out-run by improving the experiment |
| 62 | **The three origins share one axis** | **PROVED (Lean)** | `the_three_origins_share_one_axis`: the unique stiffness zero `w = -1/3`, the horizon origin `S = 0`, and the flatness origin `S = sRequired < 0` are three distinct values, strictly ordered on one line; each is a strict boundary, never a solution. "Perpendicular zero systems" has no instance here |

## The three claims that are easy to misquote

**"N7 explains the beginning."** No. Rows 29-30 and 35-36. The node is a
consistency filter on an assumed history. `not_a_beginning_theorem` is formalised
precisely so this file cannot be cited as a beginning result.

**"N7 predicts 42.25 e-folds."** No, and not `~60` either. Row 26 is the exact
*geometric flatness* threshold for the stated inputs and nothing more. The
conventional figure carries quantum diffusion, overshoot, and reheating history,
all listed as NOT ADDRESSED in row 42. The two numbers are not in tension
because they are not the same quantity; neither is derived from the other.

**"N7 says inflation lasts at most 45.55 e-folds."** No, and this is the easiest
new misreading. Rows 35-36 say that the *flatness criterion* tops out at
`45.5536` once the `1.5e-5` cosmic-variance floor is respected, and that
certifying `~60` on curvature alone would need `|Omega_k| < 4.2e-18`. That is a
statement about one observable, not an upper bound on the inflation length and
not a rival to the `~60` convention, which rests on horizon-exit fluctuations,
the scalar spectrum and `r` (rows 26, 42). It is also a *precision* limit, not a
mathematical one: the formal requirement diverges as `eps_obs -> 0`, now as a
theorem (`nInflNeeded_unbounded_above`, row 60) rather than a numeric accident.

**"N7 excludes some inflation models."** Not yet. Row 37 shows the verdict is
mechanical *given* a model that predicts its own curvature, but N7 supplies no
such prediction and derives none, so the filter is vacuous as it stands (row 40,
and rows 29-30). Independently, the sign test needs `|Omega_k|` resolved to
`1e-4` where the best verified bound is `50x` looser (row 41). The only thing
falsified here so far is an order-unity curvature.

**"Flatness and horizon are independent problems."** No, within FLRW + GR. Row
15. This is the one place where the node genuinely collapses two problems to
one, and it is standard textbook content (row 28), not a new prediction.

## What a mechanism would have to do

Row 31 is the whole remaining problem, and it is worth writing in the form a
future node would have to satisfy. A mechanism for the origin problems must
produce `eps_i < eps_obs` **dynamically**, from a law rather than from an input.
Concretely, it must:

1. produce a history with `S < 0` without `S` being assumed small at the outset;
2. do so for a *range* of initial conditions, since `eps_i` is currently free
   and a mechanism that only works at one point has merely relocated the
   fine-tuning (row 30);
3. remain valid in the regime where FLRW + GR are themselves in question
   (row 32).

N7 supplies none of these and is not trying to. What it supplies is the
bookkeeping that makes the target precise: once `eps_i` is fixed by something,
everything downstream is a closed-form ODE.

## Cross-references

- specification: `ORIGIN_CONSISTENCY_WINDOW.md` (this directory)
- experiment: `02_Experimental_Implementations_and_Verification/01_Poincare_Universe_and_Cosmological_Models/origin_consistency_window_n7.py`
- tests: `04_Testing_and_Validation_Suite/05_Origin_Consistency_Window_Tests/test_origin_consistency_window_n7.py` (52 passing; the scope rows above are asserted as tests, not only as prose)
- artifact: `03_Data_and_Observational_Resources/02_Experimental_Data_Collections/origin_consistency_window_n7_data.json` (scope block mirrors rows 29-36)
- Lean: `01_Core_Mathematical_Framework_Lean/02_Cosmology_Submodule/Cosmology/OriginWindow.lean`
