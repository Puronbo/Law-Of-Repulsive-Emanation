# Explicit Claims Register

**Status: mixed.** Each card below is one *falsifiable sentence* distilled from the
register's shared insight, tagged by type:

- **Theorem** — established in the literature (source given; treat as factual).
- **Formal** — machine-checked in this repository (Lean file given; axiom-clean).
- **Empirical** — supported by the repo's numerical experiments (script + tolerance).
- **Conjecture / Open** — explicit but unresolved (the *missing entity* is named).

The purpose is to move the insight out of prose: a claim is "explicit and factual"
only when it has (i) a precise statement, (ii) a falsifier, and (iii) a source for
the entity it is missing. This register supplies those three for every card.

Every card is also indexed -- card → Lean artifact (module + declarations) →
numerical experiment -> citation -- in **`CLAIM_TRACEABILITY.md`**, and every link in
that map is machine-checked by
`04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_claim_traceability.py`
(module exists and is imported by `PunoCalculus.lean`; identifier is really declared;
experiment exists; the map references every card, module and script).

## Schema

| field | meaning |
|---|---|
| **ID** | stable name |
| **statement** | one falsifiable sentence |
| **type** | Theorem / Formal / Empirical / Conjecture |
| **evidence** | file, experiment, or citation establishing it *now* |
| **falsifier** | the observation/derivation that would refute it |
| **missing entity** | the object not yet constructed (for open cards) |
| **source** | literature anchor for the missing entity / the theorem |

## Claim cards

### C1 — The scaling-critical invariant is one object in many forms · Theorem
- **statement.** Every scale-critical function space for 3D Navier–Stokes is a
  form of `s_crit(p) = 3/p - 1`; the chain is `L^3 ⊂ Ḃ^{-1+3/p}_{p,∞} ⊂ BMO^{-1} ⊂ Ḃ^{-1}_{∞,∞}`.
- **evidence**: `CriticalLadder.lean` (invariance `scalingInvariant_iff`, anchors
  `sCrit(3)=0`, `sCrit(2)=1/2`).
- **falsifier**: a critical hypothesis space whose scaling index is not `3/p - 1`.
- **source:** Prodi (1959); Serrin (1962); Koch–Tataru (2001, *Adv. Math.*, `BMO^{-1}`);
  Cheskidov–Shvydkoy (2010, arXiv:0708.3067, largest critical space).

## C2 — Sufficiency is classical; positive margin implies regularity

**Type:** Theorem. **Statement.** Any `L^p_t L^q_x` with `2/q + 3/p <= 1`
(`p < inf`) or `L^\inf_t L^3_x` solution is smooth. **Evidence:** Prodi–Serrin;
Escauriaza–Seregin–Sverak (2003). **Falsifier:** a singular solution satisfying the
margin. **Missing entity:** none (established).

## C3 — Boundedness along the flow is the open brick

**Type:** Conjecture/Open. **Statement.** `||u(t)||_{B^{-1}_{\inf,\inf}}` stays
bounded along the Leray–Hopf flow. **Evidence:** none — this is the open problem.
**Falsifier:** an unbounded-norm Leray solution (would prove non-uniqueness/blowup).
**Missing entity:** a proof; nearest partial: Cheskidov–Shvydkoy (2010,
arXiv:0708.3067); Ri (arXiv:2307.11312, 2023 — **single-author, unrefereed, treat
as unverified**). **Source:** Bourgain–Pavlovic (2008, JAMS) for the ill-posedness
scale.

## C4/C6 — The missing control is exactly one extra power of enstrophy

**Type:** Formal (arithmetic core) + Theorem (analytic frame). **Statement.** The
exactly critical quantity is `int Z^{1+eps} dt`; the energy identity gives only
`int Z dt < inf`, and `Z^{1+eps}` is strictly stronger exactly where `Z > 1`.
**Evidence:** `ExplicitClaims.extra_power_strengthens_above_unit`
(`z <= z^(1+eps) ↔ 1 <= z`, machine-checked); register `EnstrophyBarrier`,
`QuantitativeContinuation`. **Falsifier:** a proof that `int Z dt < inf` already
closes all critical norms. **Missing entity:** a sub-critical Besov/Lorentz
estimate (the "one extra power"); source: Tao (2016, 2021 quantitative continuation
bounds); Feng–He–Wang (2025, Lorentz); arXiv:2411.06483 (Besov); Grujic (2024, JMFM,
"Asymptotic Criticality").

## C4/C6 — Dimension threshold and the half-derivative gap

**Type:** Formals. **Statement.** `H^1` embeds in `L^\inf` iff `d < 2`; at physical
`d = 3` the gap is exactly `1/2` derivative. **Evidence:**
`ExplicitClaims.morrey_threshold` (`0 < 1 - d/2 ↔ d < 2`),
`ExplicitClaims.physical_embedding_gap` (`1 - 3/2 = -1/2`). **Falsifier:** an
`H^1 -> L^\inf` embedding in `d = 3`. **Missing entity:** none (arithmetic).

## C8 — Dimension of a mixture is a sup, not a mean

**Type:** Formal. **Statement.** `(d + e)/2 <= max d e`; averaging cannot lower the
effective dimension. **Evidence:** `ExplicitClaims.mean_le_dimMixture`;
`dimension_mixture.py` (measured: sup governed by `max_i d_i`). **Falsifier:** a
mixing rule whose effective dimension is an average. **Missing entity:** an
equation-preserving reweighting keeping high-dimension energy under the `O(eps)`
budget; sources: Adams–Hedberg (1996, Riesz potentials / fractal measures); Tao
(dimensional regularisation).

## C9 — Intermittency budget theta_max = O(eps)

**Type:** Empirical. **Statement.** The admissible high-dimension `H^1` fraction
vanishes linearly with scale: `theta_max = O(eps)` (measured `3.33e-3` at
`eps = 1e-3` vs leading-order `3.29e-3`). **Evidence:** `dimension_mixture.py`.
**Falsifier:** a mixture attaining `theta_max = O(1)` with `d_eff < 2`. **Missing
entity:** a rigorous multifractal measure bridge; sources: Constantin (1994,
intermittency); Frisch, *Turbulence* (1995).

## C10 — Orientation sign equals the sign of the critical-content derivative

**Type:** Empirical + Formal (model core). **Statement.** `sign(lambda) = sign(mu)`
across systems (n = 6, balanced 3 repelling / 3 attracting), where `lambda` is the
orbit Lyapunov base and `mu = d/dt log(critical content)`: 3D NS `-3.11 / -0.41`;
2D NS `-9.27 / -0.53`; 3D Euler `+1.72 / +0.16`; 1D Burgers `+16.24 / +2.39`;
CLM `+34.75 / +2.82`; linear heat `-66.74 / -0.13`. **Evidence:**
`orientation_vs_invariant.py` (6 systems, all match); resolution-converged at
`T = 8` (`N = 32/48/64`, `|dk|/k = 0.027`,
`|dlambda|/|lambda| = 0.019`). **Formal model core:** `OrientationLaw.lean` proves
`mu == lambda` on the geometric orbit (`logGrowth_geometric`), hence `sign_match`
and `orientation_reads_wall` (`mu > 0` iff the invariant escapes every bound). More
generally, with no geometric assumption, `logGrowth_of_ratio_eq` gives
`mu = log(relative increment)` for any positive sequence and
`exists_pos_logGrowth_of_unbounded` gives: unbounded content ⇒ some strictly positive
growth rate (`bounded_of_nonpos_logGrowth` as contrapositive).
growth rate (`bounded_of_nonpos_logGrowth` as contrapositive).
**One-parameter family (dissipation order):** `orientation_vs_fractional_s.py` extends
the empirical half to `u_t + u·∇u = -nu (-Δ)^s u`. The critical index is s-dependent
(`H^sigma` critical at `sigma = 5/2 - 2s`); over that `s`-correct critical content the
match holds at `s = 1.0 / 0.75 / 0.5` (`lambda = -3.15 / -1.29 / -0.30`, `mu = -0.63
/ -0.67 / -0.56`), all attracting, with `|lambda|` shrinking toward the inviscid regime.
**Provable energy face:** `DissipativeFlow.lean` proves `logGrowth_deriv` (log-growth
`= m / X t`), `logGrowth_nonpos_of_dissipative` (`m <= 0` => `d/dt log X <= 0`) and
`content_le_initial_of_dissipative` (a dissipative flow never lets its content grow,
      `X T <= X 0`).
**Margin (empirical):** `fractional_margin_sweep.py` locates the boundary of the
standard regime: the late-window orientation crosses zero at the marginal order
`s* = 0.258` (scaling gap `|lambda| ~ |s - s*|^beta`, `beta = 1.19`) and, at fixed
`s = 0.40`, at viscosity `nu* = 0.049` (`gamma = 1.03`) -- both gaps linear. The
critical content is still decaying where the orientation has flipped (s = 0.20:
`lambda = +0.05`, `mu = -0.20`), so the orientation LEADS the wall.
**Robustness (empirical):** `fractional_margin_universality.py` re-locates `s*` across
the band split `K0 in {4, 6, 8}` and a different seed -- `s* = 0.28 .. 0.32` (spread
`0.037`, `T = 5`), so the margin is NOT an artifact of the `K0` split. But
`fractional_margin_window.py` shows `s*` is a MOVING, SHRINKING boundary: over
`T = 4, 6, 8, 10, 12` it follows `s*(T) = 0.055 + 1.21/T` (rms `0.002`), and by `T = 16`
it has fallen to `O(0.01)`. At `N = 32`, `T = 16` the crossing VANISHES (`lambda < 0`
for all `s >= 0.01`), but `fractional_margin_resolution.py` shows this vanish is PARTLY
a numerical floor: at `N = 48`, `T = 16` the crossing PERSISTS at `s* ~= 0.012`
(`lambda(0.01) = +0.001`, `lambda(0.02) = -0.013`). Hence `s*` is a finite-window
TRANSIENT of the high-k pile-up that collapses steeply toward a small value -- NOT a
well-resolved critical order (whether the limit is exactly `0` is resolution-limited at
small `s`). A resolution check at fixed `T = 6` gives `s* = 0.259 (N = 32)` vs
`0.265 (N = 48)` -- agreement to `0.006`, within the ~`0.02` seed noise -- so the
intermediate-`T` values are resolution-stable.
**Margin is a unique crossing (formal core):** `MarginCrossing.lean` proves that a
continuous, strictly decreasing `lambda(s)` positive at the left endpoint and negative at
the right has exactly ONE zero (`existsUnique_zero_of_strictAntiOn`), that this zero
separates a repelling (`lambda > 0`) side from an attracting (`lambda < 0`) side
(`side_of_crossing`), and packages both as `margin_existsUnique`. So the register's
marginal order `s*` is well-defined the moment `lambda` is antitone in `s`; the open
content is that antitonicity, not the arithmetic.
**Margin as a first crossing (no monotonicity needed):** `FirstCrossing.lean` drops the
antitone hypothesis entirely -- the third family (fractional CLM) is NOT monotone in `s`.
For any `Continuous f` with `0 < f a` and `f b < 0` on `a ≤ b` it proves the set `{x ∈
[a,b] : f x ≤ 0}` (closed, bounded below) has a least element `c` that is an interior zero,
with `f > 0` strictly on `[a,c)` (`exists_first_zero`), and that `c` is the FIRST zero --
no earlier one (`margin_exists_firstCrossing`). So a margin EXISTS under the weakest
hypothesis (continuity + one sign change); uniqueness is the extra content the NS/Burgers
family carries.
**Falsifier:** a grid-converged system with `sign(lambda) != sign(mu)`. **Missing
entity:** the analytic claim that the identification `mu = lambda` survives the real
flow; sources: Beale–Kato–Majda (1984); Constantin–Fefferman (1993); Deng–Hou–Yu (2015).

## C10-open — The analytic residue: `mu = lambda` for the real flow

**Type:** Conjecture/Open. **Statement.** Let `u` be a Leray–Hopf solution of 3D NS on
`[0,T*)` and `X(t) = ‖u(t)‖_{Ḃ^{-1}_{∞,∞}}` its largest critical content. Define the
orientation `lambda := limsup_{n} (1/n) log(X(n)/X(0))` and the growth rate
`mu(n) = logGrowth X n`. Then `sign(lambda) = sign(mu)` asymptotically, and in
particular `lambda > 0` iff `X` is unbounded (the content escapes the wall), `lambda
<= 0` iff `X` is bounded. **Evidence (partial):** the discrete form is fully proved
(`OrientationLaw.lean`: `logGrowth_geometric`, `log_eq_sum_logGrowth`,
`bounded_of_bounded_sum_logGrowth`, `unbounded_sum_of_unbounded`); the sign match is
empirical across 6 systems (`orientation_vs_invariant.py`). **Continuous part proved:**
`OrientationLaw.contLogGrowth_integral` (`int_0^T g = log X T - log X 0`) and
`continuous_content_bounded` (bounded `int_0^T g` => `X T <= X 0 * exp B`) are
machine-checked, so the residue is exactly the NS-specific bound on `g`.
**Wall isolated:** `RegularityReduction.lean` proves the reduction BOTH ways and packages
it as an equivalence -- `regularity_iff_integral_bounded`: the content is bounded uniformly
in `T` iff the critical-content integral `int_0^T g` is bounded uniformly in `T`
(`regularity_reduced_to_integral` and its converse `integral_le_of_content_le`, plus the
contrapositive `integral_unbounded_of_content_unbounded`) -- so the residue is *exactly*
the boundedness of the critical-content integral. **Sufficiency proved too:**
`SerrinSufficiency.lean` supplies the classical Prodi-Serrin direction in the same
`(X, g)` abstraction -- `content_le_of_growth_le_weight` (if the log-growth rate is
dominated by a weight of finite action, `X T <= X 0 * exp (R M)`) and
`bounded_on_of_serrinAction` (such a finite supercritical control forbids finite-time
blow-up) -- alongside the Serrin-margin arithmetic `serrinMargin p q = 1 - (2/q + 3/p)`
(positive = strictly supercritical; `serrinMargin_eq_neg_ladder` shows a positive margin
is exactly "above the critical rung"). So the register now has BOTH halves: a bounded
control (sufficient) and the equivalence; only the NS-specific existence of that control
on the real flow stays open. values are resolution-stable. Whether the collapsing limit is exactly `0` is
resolution-limited at small `s`.
**Cross-PDE recurrence (empirical):** `fractional_burgers_margin.py` runs the identical
order/orientation probe on fractional Burgers `u_t + u u_x = -nu (-∂_xx)^s u`
(1D, spectral, seed-averaged over 4 ICs). Burgers is shock-forming, yet it carries the
SAME order/orientation margin -- a critical dissipation order separating repelling
(weak dissipation) from attracting (strong) -- and it SHRINKS as the window grows:
`s* = 1.51 / 0.35 / 0.27 / 0.22` at `T = 3 / 5 / 8 / 12` on `N = 256`, fit `s*(T) = 0.134 +
1.072/T` (`T >= 5`), comparable to the NS `0.055 + 1.206/T`. (Burgers is noisier: seed
spread up to `~0.5` near the crossing at `N = 256`; only the seed-averaged trend is
quoted.) A grid/timestep check (`res` mode) shows the crossing is resolution-stable once
the grid is fine enough: at `T = 8`, `s* = 0.288 (N = 256)` vs `0.212 (N = 512)` vs `0.213
(N = 768)` -- N=512 and N=768 agree to `0.001` (N=256 is biased `~0.08` high). The
converged `window512` mode re-runs the whole table at `N = 512, dt = 2.5e-4`:
`s* = 1.457 / 0.299 / 0.228 / 0.213` at `T = 3 / 5 / 8 / 12`, fit `s*(T) = 0.143 + 0.764/T`
(`T >= 5`). So the shrinking law survives grid refinement, and its extrapolated limit
`s*(inf) ~ 0.14` is grid-stable (same intercept as N=256, smaller slope). So the margin is
a property of the class of fractionally-dissipated systems, not of Navier-Stokes alone --
the recursion (order/orientation boundary) recurs across a second, qualitatively different
family.
**Third family (empirical, honest negative):** `fractional_clm_margin.py` runs the same
probe on fractional CLM `d_t w = w H(w) - nu (-∂_xx)^s w` -- a PROVEN-blowup family
(Constantin-Lax-Majda 1985). It HAS a critical dissipation order separating repelling
(small `s`, the CLM blowup regime) from attracting (large `s`): at `T = 3`,
`lambda = 34` at `s = 0.1`, `+2.2` at `s = 2.5`, `-0.05` at `s = 3.0`, and the crossing
near `s* ~ 2.7-3.0` is resolution-stable (`N = 256` vs `N = 512` agree; a third grid
`N = 1024` gives `lambda(2.0) = +3.95`, `lambda(3.0) = -0.02`, so the sign flip between
`2.0` and `3.0` is grid-robust). But its window
dependence is NOT the clean shrinking transient: `s* ~ 2.66 / 2.70 / 2.71` at `T = 2 / 3 /
4` (a stable threshold), and beyond `s ~ 2.5` the orientation hovers inside the noise floor
(`|lambda| <~ 0.05`) over a broad band `s ~ 2.5..5.5`, so at `T = 6` the first sign change
jumps out to `~5.4`. So the existence of a margin recurs across three families, but the
shrinking law is specific to the NS/Burgers family, not universal.
**Falsifier:** a
Leray–Hopf solution with unbounded `‖u‖_{B^{-1}_{∞,∞}}` but `lambda <= 0`, or a global
solution with `lambda > 0`. **Missing entity:** the bridge from the discrete
telescoping identity to the *real* flow -- i.e. an analytic lower bound on
`mu(t) = d/dt log ‖u(t)‖` (equivalently the BKM/Constantin–Fefferman critical-content
integral). **Sources:** Beale–Kato–Majda (1984); Constantin–Fefferman (1993);
Deng–Hou–Yu (2015); Cheskidov–Shvydkoy (2010).

## C11 — Orientation decides the wall

**Type:** Formal. **Statement.** For the geometric orbit, bounded `↔ r <= 1`, and
`0 < log r` iff unbounded. **Evidence:** `OrientationBoundedness.lean`
(`geometric_bounded_iff`, `orientation_decides_boundedness`,
`repelling_iff_unbounded`). **Falsifier:** a model bounded with `r > 1`.

## C12 — Two numbers close the register

**Type:** Formal. **Statement.** Both *which-rung* (order) and *which-side*
(orientation) are functions of the two numbers alone.
**Evidence:** `TheoryOfEverything.lean` (`theoryOfEverything`, `twoNumbersClose`).
**Falsifier:** a register brick not expressible via `(order, orientation)`.

## C13 — Time is emergent, not primitive

**Type:** Formal (structural; **not** a physical claim). **Statement.** Change is
transfer (energy moved, total conserved); the state is a function of the transfer
count alone, so time is the count, not a variable. **Evidence:**
`EmergentTime.lean` (`transfer_conserves_total`, `state_determined_by_count`).
**Falsifier:** a conservative change that depends on something other than its index
in the model.

## C14 — Heterogeneous barrier types across the Millennium list

**Type:** Formal (the abstract barrier is machine-checked) / Interpretive (the card's
"all walls are one type" reading stays a map, not a theorem).
**Statement.** The recurring obstruction is (method-barrier / existence-barrier /
bridge-barrier), and the cleanest of these -- the method barrier -- is a *diagonal,
self-referential* construction. **Evidence (machine-checked):** `LogicBarrier.lean`
proves Lawvere's fixed-point theorem -- if `α` surjects onto its own function space
`α → β`, then *every* `f : β → β` has a fixed point (`lawvere_fixedpoint`); hence a
fixed-point-free `f` forbids any such enumeration (`no_surjective_of_no_fixedpoint`), so
no type enumerates its own predicates (`no_surjective_predicates`, Cantor's theorem in
diagonal form) and the diagonal predicate escapes every enumeration
(`diagonal_not_mem_range`). This one skeleton is shared by Cantor (1891), Gödel's
diagonal lemma (1931), and Turing's halting problem (1936); no model of computation or of
arithmetic is formalised, and no Millennium problem is touched. **Sources:** P vs NP:
Baker–Gill–Solovay (1975), Razborov–Rudich (1997), Aaronson–Wigderson (2008); the
diagonal engine: Cantor (1891), Gödel (1931), Turing (1936), Lawvere (1969); Yang–Mills:
Osterwalder–Schrader (1973), Jaffe–Witten (2000); NS/BSD/RH as in the register.

## C15 — Nothing is the origin: zero links all forms

**Type:** Formal (structural). **Statement.** The empty type `Empty` (cardinality
`0`) is the *initial object* of `Type`: into **every** type `α` there is an arrow
`Empty → α`, and it is **unique**; dually `PUnit` (cardinality `1`) is *terminal*.
Under the sum of types (`+`) `Empty` is the **identity** and under the product
(`×`) it is **absorbing** — `0 + a = a`, `0 * a = 0`, rebuilt with sets.
**Evidence:** `ZeroLink.lean` (`empty_unique_arrow`, `empty_isInitial`,
`unit_isTerminal`, `empty_classified_initial`, `unit_classified_terminal`,
`zero_links_all`; axioms `⊆ {propext, Classical.choice, Quot.sound}`).
**Falsifier:** a type with two distinct arrows `Empty → α`, or a type that is both
initial and terminal in `Type`. **Missing entity:** none for the structural
statement; the *categorical zero object* (initial ∧ terminal), which requires an
Ab-enriched category such as modules, is **card C16** (now claimed there for
`ModuleCat R`), not claimed here. **Source:** Awodey, *Category Theory* (2010);
Mac Lane, *Categories for the
Working Mathematician* (1998) — the empty set is the initial object of `Set`. This
is the structural face of the register's own 0/0 doctrine (`Removable`,
`ZeroZero`, `ZeroFixedPoint`): an initial arrow *exists* and is *unique*, exactly
as a removable 0/0 has an existing, definite value.

## C16 — The zero object: one object is origin and target

**Type:** Formal (structural / categorical). **Statement.** In a category with a
*zero object*, a single object `Z` is simultaneously **initial** (a unique arrow
`Z → Y` into every `Y`) and **terminal** (a unique arrow `Y → Z` from every `Y`) --
the two directions that `Type` splits between `Empty` and `PUnit`. For a ring `R`,
`ModuleCat R` has such an object (`ModuleCat.instHasZeroObject`), and any two zero
objects are isomorphic. **Evidence:** `ZeroObject.lean` (`initial_link`,
`terminal_link`, `zero_isInitial`, `zero_isTerminal`, `zero_links_both_ways`,
`zero_unique_up_to_iso`, `modules_haveZeroObject`, `modules_exists_zeroObject`,
`modules_zero_links`). **Falsifier:** a claimed zero object with two distinct arrows
to or from some object. **Missing entity:** none for the module categories; `Type`
itself has no zero object (initial `Empty` and terminal `PUnit` differ) -- recorded,
not claimed. **Source:** Awodey, *Category Theory* (2010); Mac Lane (1998). This
*completes* C15: zero links all forms **within a single object** exactly when the
category has a zero object.

## C17 — The 0/0 / initial-arrow bridge: removability is existence + uniqueness

**Type:** Formal (analytic ↔ categorical schema). **Statement.** A *removable
value* of `f` at a puncture `a` is a value `L` with `Tendsto f (𝓝[≠] a) (𝓝 L)`;
when it exists it is **unique** (the target `ℝ` is Hausdorff), so the removable
value is a genuine "exactly one" -- the *same* `∃!` schema that characterizes the
initial arrow in `ZeroLink`. Concretely, the canonical 0/0
`(x - a)·g(x)/(x - a)` with `g` continuous at `a` has the unique removable value
`g a` (`Removable.removable_limit` for existence, `removable_value_unique` for
uniqueness), and any continuous extension of a punctured map is unique
(`extension_unique`). **Evidence:** `RemovableValue.lean` (`IsRemovableValue`,
`removable_value_unique`, `existsUnique_iff_exists_and_unique`, `extension_unique`,
`removable_exists_unique`, `removable_value_bridge`, `initial_arrow_schema`).
**Falsifier:** two distinct values both being punctured limits of the same map at
the same point, or two distinct continuous extensions agreeing off the point.
**Missing entity:** none at the schema level; whether a *given physical* 0/0 has a
limit is the object-specific content of the experimental programs (card-specific),
not claimed here. **Source:** standard topology (uniqueness of limits in Hausdorff
spaces) applied to the register's own `Removable` and `ZeroLink` -- the analytic and
categorical faces of one schema.

## C18 — Order of vanishing as a graded index

`PunoCalculus.ZeroFixedPoint` counts the zeros of a 0/0: dividing `(x - x₀)^k · h` by
`(x - x₀)^j` gives `h x₀` at `j = k`, `0` at `j < k`, and diverges at `j > k`.  This
card makes that "number of zeros" a **graded index** -- a level in a decreasing
`ℕ`-filtration of punctured neighbourhoods.  Level `k` is `VanishesToOrder k f x₀`:
`f` factors as `(· - x₀)^k · g` with `g` continuous at `x₀`.  The filtration is
**decreasing** (`vanishes_succ_imp`, `vanishes_antitone`: `k ≤ m` gives `F m ⊆ F k`),
and -- the grade itself -- dividing out one zero lowers the level by exactly one:
`vanishes_shift` gives `F (k+1) f ↔ F k (divideOut x₀ f)` with
`divideOut x₀ f = f / (· - x₀)`.  Exact order `k` (`HasGrade k f x₀`) is membership in
`F k` but not `F (k+1)`; the canonical `(· - x₀)^k · h` with `h x₀ ≠ 0` has exact grade
`k` (`hasGrade_canonical`), the exact grade shifts by one under `divideOut`
(`hasGrade_shift`), and it is well-defined (`grade_unique`: `HasGrade k → HasGrade m →
k = m`).  **Evidence:** `VanishOrder.lean` (`VanishesToOrder`, `divideOut`,
`vanishes_zero`, `vanishes_succ_imp`, `vanishes_shift`, `HasGrade`, `hasGrade_canonical`,
`hasGrade_shift`, `vanishes_antitone`, `grade_unique`, `order_is_graded`).
**Falsifier:** a map with two distinct exact orders at a point, or a level-`(k+1)`
member that is not a level-`k` member.  **Missing entity:** none for the filtration
itself; identifying the graded degree with a *physical* scaling exponent stays
object-specific (cards C1/C10).  **Source:** order-of-vanishing / valuation theory (the
local ring of germs at `x₀` filtered by `(x - x₀)^k`), applied to the register's own
`ZeroFixedPoint` `zero_count_*` results and completing the scaling story of
`GreatAttractor`.

## C19 — The Probe mechanism: an identity 0/0 resolves to `1`

**Type:** Formal (analytic mechanism). **Statement.** `THE_0_OVER_0_ATLAS.md`
classifies a removable 0/0 into five mechanisms; the first is the **Probe**.  If two
functions agree on the punctured neighbourhood of `x₀` (`f =ᶠ[𝓝[≠] x₀] g`) and the
denominator is nonzero there, then the ratio `f/g` resolves to `1`: the identity 0/0
has removable value `1` (`probe_identity`).  In particular `f/f` probes to `1` where
`f ≠ 0` (`probe_self`); the probe value, when it exists, is unique
(`probe_value_unique`); and it is literally an `IsRemovableValue`
(`probe_is_removable`).  **Evidence:** `ZeroProbe.lean` (`ProbeValue`, `probe_identity`,
`probe_self`, `probe_value_unique`, `probe_is_removable`).  **Falsifier:** two
functions agreeing off the point whose ratio fails to tend to `1` where the denominator
is nonzero.  **Missing entity:** none -- the probe value is the value at the point of
the forced continuous extension.  **Source:** the register's own atlas (Probe
mechanism, the "removable value `1`" class: functional-equation / identity entries).

## C20 — The Vanishing-Rate mechanism: the order of vanishing is a valuation

**Type:** Formal (analytic mechanism). **Statement.** `ZeroFixedPoint`/`VanishOrder`
grade a 0/0 by a *filtration* -- and that grading is provably **not** additive under
products (`|·|` and `|·|` both lie at grade `0`, their product `(·)^2` at grade `2`).
The atlas's **Vanishing-Rate** mechanism ("leading Taylor coefficient") instead needs
the genuine order of vanishing, defined by a residue limit:
`HasOrder k f x₀` iff some nonzero `c` has `f / (· - x₀)^k → c` at the puncture.  This
order **is** a valuation: it **adds under products** (`hasOrder_mul`, the law
`order(f·g) = order f + order g`), **scales under powers** (`hasOrder_pow`,
`order(f^n) = n·order f`), is `0` exactly on nonzero punctured limits
(`hasOrder_zero_iff`), is realised by the canonical `(·-x₀)^n·h` with `h x₀ ≠ 0`
(`hasOrder_canonical`), and is well-defined (`hasOrder_unique`, via
`hasOrder_lt_imp_not`).  **Evidence:** `ZeroValuation.lean` (`HasOrder`, `hasOrder_one`,
`hasOrder_zero_iff`, `hasOrder_mul`, `hasOrder_pow`, `hasOrder_canonical`,
`hasOrder_lt_imp_not`, `hasOrder_unique`, `order_is_valuation`).  **Falsifier:** a
nonzero residue giving a strictly smaller and a strictly larger order simultaneously.
**Missing entity:** none for the valuation law; the equality of this order with a
*physical* scaling exponent stays object-specific (C1/C10).  **Source:** order-of-
vanishing / valuation theory (the `(x - x₀)`-adic valuation of germs at `x₀`), applied
to the register's `ZeroFixedPoint` and complementing C18's filtration.

## C21 — The Index mechanism: the root multiplicity is an additive integer

**Type:** Formal (algebraic mechanism). **Statement.** The atlas's **Index**
mechanism turns a 0/0 into an **integer** (winding number, multiplicity).  Its
algebraic face is the root multiplicity: `Index a p := p.rootMultiplicity a`.  It is
**additive under products** (`index_additive`, `Index a (p·q) = Index a p + Index a q`
for `p·q ≠ 0`), **scales under powers** (`index_pow`), is `1` at a simple root
(`index_X_sub_C_self`), is exactly `n` on `(X - a)^n` (`index_pow_self`) and on the
canonical integer removable value `c·(X - a)^n` with `c ≠ 0` (`index_canonical`).
**Evidence:** `ZeroIndex.lean` (`Index`, `index_one`, `index_additive`, `index_pow`,
`index_X_sub_C_self`, `index_pow_self`, `index_canonical`, `index_is_multiplicity`).
**Falsifier:** a product whose multiplicity differs from the sum of its factors'.
**Missing entity:** none for the algebraic face; the topological faces (winding
numbers, Poincaré–Hopf) are the same integer invariant in other categories -- recorded,
not claimed here.  **Source:** polynomial algebra (multiplicity in a UFD / the local
ring `R[X]_{(X-a)}`), the algebraic face of the register's Index mechanism.

## C22 — The mechanism closure: the anti-class, and the five faces bundled

**Type:** Formal (analytic mechanism / closure). **Statement.** The atlas's
**amendment** records that the strict completeness claim is *false*: there are 0/0
forms whose ratio has **no limit at all** (the "anti-class": Pólya `F(n)/√n`, Mertens,
the divisor/circle errors, ...).  This card makes that a theorem and closes the
mechanism register.  The genuine 0/0 `|x|/x` at `0` (both `|·|` and `·` vanish:
`abs_vanish`, `id_vanish`) has **no** removable value: `|x|/x` tends to `1` from the
right (`abs_div_self_tendsto_right`) and to `-1` from the left
(`abs_div_self_tendsto_left`), so a punctured limit would force `1 = -1` --
`abs_div_self_no_limit`, i.e. **the anti-class is nonempty** (`anti_class_nonempty`).
The capstone `mechanisms_close` bundles the register's mechanism faces: Probe resolves
a self-0/0 to `1`, the order of vanishing is additive, the index is additive, and the
anti-class is nonempty -- a removable value is *not* automatic.  **Evidence:**
`ZeroMechanisms.lean` (`abs_div_self_tendsto_right`, `abs_div_self_tendsto_left`,
`abs_div_self_no_limit`, `abs_vanish`, `id_vanish`, `anti_class_nonempty`,
`mechanisms_close`).  **Falsifier:** a limit of `|x|/x` at `0`, which would force the
one-sided limits `1` and `-1` to agree.  **Missing entity:** none -- the anti-class
member is explicit.  **Source:** the register's own atlas (amendment, entries 64/67/69
/70/73/74), and standard one-sided-limit theory; the Critical and Conservation
mechanisms remain object-specific (cards C1/C10).

## C23 — Riemann's removable singularity, in the register's 0/0 schema

**Type:** Formal (analytic bridge / named theorem). **Statement.** Card C17 states
the register's 0/0 schema over `ℝ` (`RemovableValue`): a punctured limit, when it
exists, is unique, and the canonical `(x-a)·g(x)/(x-a)` has a removable value --
but it proves the *schema*, not that any given 0/0 actually has a limit.  This card
anchors the schema to a genuine theorem.  Mathlib proves **Riemann's removable
singularity theorem**
(`Complex.tendsto_limUnder_of_differentiable_on_punctured_nhds_of_bounded_under`):
a function complex-differentiable and bounded on a punctured neighbourhood of `c`
has a punctured limit.  Read through the register's predicate
(`IsRemovableValueAt f c L := Tendsto f (𝓝[≠] c) (𝓝 L)`), it gives **existence**
(`removable_value_exists`: the value is `limUnder (𝓝[≠] c) f`) and, with `ℂ`
Hausdorff, **uniqueness** (`removable_value_unique`) -- a genuine `∃!`
(`exists_unique_removable_value`), the identical shape of C17's
`removable_exists_unique`, now over `ℂ`.  The **coincidence**
(`limUnder_eq_of_isRemovableValue`) is that mathlib's `limUnder` *is* the removable
value: it equals any punctured limit; and `canonical_zero_over_zero` re-proves the
concrete 0/0 `(z-c)·g(z)/(z-c) ↦ g c` on `ℂ`.  **Evidence:**
`RemovableComplexBridge.lean` (`IsRemovableValueAt`, `removable_value_exists`,
`removable_value_unique`, `exists_unique_removable_value`,
`limUnder_eq_of_isRemovableValue`, `canonical_zero_over_zero`), over
`Mathlib.Analysis.Complex.RemovableSingularity`.  **Falsifier:** a bounded
holomorphic 0/0 with two distinct removable values, or a canonical
`(z-c)·g(z)/(z-c)` that fails to tend to `g c`.  **Missing entity:** none -- the
theorem is mathlib's; the bridge is the new content.  **Source:** Riemann's
removable singularity theorem (Mathlib, Y. Kudryashov); the register's own 0/0
doctrine (`Removable`, `RemovableValue`).

## C24 — Liouville's theorem: global boundedness collapses the entire 0/0

**Type:** Formal (analytic bridge / named theorem). **Statement.** Card C23 records that
*local* boundedness at a puncture lets a 0/0 resolve to a finite value (Riemann's
removable singularity theorem).  This card is the *global* dual: on the whole plane,
boundedness is coercive.  Mathlib proves **Liouville's theorem** -- a function
complex-differentiable on all of `ℂ` whose range is bounded is a constant -- formalised
here in register form: `bounded_entire_const` (`∃ c, f = Function.const ℂ c`),
`bounded_entire_apply_eq` (a bounded entire `f` takes the same value at any two points),
`bounded_entire_value_unique` (it takes at most one value).  The register's statement is
`eq_zero_of_bounded_of_eq_zero`: a bounded entire function that **vanishes at the origin**
is *identically zero* -- global boundedness forces the register's 0/0 to `0`; no nonzero
bounded entire function can carry a zero.  The bounded-at-infinity form
`bounded_at_infinity_const` says an entire function tending to a finite value `c` at
infinity (along `cocompact ℂ`) is the constant `c`.  **Evidence:** `LiouvilleBridge.lean`
(`bounded_entire_const`, `bounded_entire_apply_eq`, `bounded_entire_value_unique`,
`eq_zero_of_bounded_of_eq_zero`, `bounded_at_infinity_const`), over
`Mathlib.Analysis.Complex.Liouville`.  **Falsifier:** a bounded entire function taking two
distinct values, or a bounded entire function vanishing at the origin that is not zero.
**Missing entity:** none -- the theorem is mathlib's; the register reading is the new
content.  **Source:** Liouville's theorem (Mathlib, Y. Kudryashov); the register's own 0/0
doctrine (`Removable`, `RemovableValue`, `RemovableComplexBridge`).

## C25 — The Serrin ladder: one extra power of enstrophy is the wall

**Type:** Formal (arithmetic core) + Theorem (analytic frame). **Statement.** The energy+enstrophy route reaches the Serrin line `2/q + 3/p = 1` only up to `p = 6`: the Gagliardo–Nirenberg exponent `theta(p) = 3/2 - 3/p` satisfies `theta(p) <= 1` **iff** `p <= 6` (`gnExponent_le_one_iff`), the Sobolev ceiling `H^1 -> L^6` is the only reachable critical endpoint, and the exactly-critical quantity integrated along the flow is `Z^{theta(p)*q(p)/2} = Z^2` at `(6,4)` (`criticalPowerIdentity`) while the energy identity supplies only `Z^1` (`oneExtraPower`, `powerClosesCriticalAtSix`: `1 + eps` closes the `(6,4)` route iff `eps >= 1`). So the missing control is exactly one extra power of enstrophy. **Evidence:** `SerrinLadder.lean` (`gnExponent`, `gnExponent_six`, `gnExponent_two`, `gnExponent_three_half`, `gnExponent_ceiling_chain`, `serrinQ`, `serrinQ_six`, `serrinQ_line`, `gnExponent_le_one_iff`, `criticalPower_six_four`, `oneExtraPower`, `criticalPowerIdentity`, `powerClosesCriticalAtSix`). **Falsifier:** a `theta(p) <= 1` interpolation ladder reaching a critical pair beyond `p = 6`, or a proof that `int Z dt < inf` already closes every critical norm. **Missing entity:** whether any `int Z^{1+eps} dt` is finite along the real flow (marker `extraEnstrophyPowerIntegralOpen`). **Source:** Prodi (1959); Serrin (1962); Sobolev `H^1 -> L^6`; Tao (2016, 2021 quantitative continuation).

## C26 — The great attractor: orientation of a fixed point, and the order that shifts the rung

**Type:** Formal (analytic). **Statement.** At a fixed point `T x₀ = x₀` with derivative `L`, the distance ratio `|T x - x₀| / |x - x₀| -> |L|` (`fixedPoint_distanceRatio`), so nearby points are pushed OUT exactly when `|L| > 1` (`fixedPoint_repels`) and fall IN when `|L| < 1` (`fixedPoint_attracts`); the orientation is a trichotomy (`orientation_trichotomy`) and the Lyapunov exponent `log |L|` is its sign (`fixedPoint_logRate`, `fixedPoint_logSign`). The same object scales on how many zeros it has: an `L^p` object of amplitude weight `a` has scaling weight `a + s - 3/p`, vanishing exactly on `s = criticalSmoothness a p = 3/p - a` (`scalingWeight_zero_iff`), which slides the critical rung by the order. **Evidence:** `GreatAttractor.lean` (`fixedPoint_distanceRatio`, `fixedPoint_repels`, `fixedPoint_attracts`, `orientation_trichotomy`, `fixedPoint_logRate`, `fixedPoint_logSign`, `orientationDiscriminator`, `criticalSmoothness`, `scalingWeight`, `criticalSmoothness_one`, `criticalSmoothness_shift_order`, `criticalSmoothness_antitone_order`, `scalingWeight_zero_iff`). **Falsifier:** a fixed point with `|L| > 1` whose neighbours fall inward, or a scaling weight that vanishes off `s = 3/p - a`. **Missing entity:** none for the arithmetic; the on-flow identification of `L` with the real multiplier is object-specific (C10/C10-open). **Source:** the register's own `THE_LAW_OF_SINGULARITIES.md` §12.1; `HasDerivAt.tendsto_slope`; `CriticalLadder`.

## C27 — Change as an interconnected force held by inertia

**Type:** Formal (arithmetic). **Statement.** Change is interconnection-mediated (force) and held by inertia: a finite collection of inertial parts coupled by any nonnegative weights has an aggregate value between the smallest and largest part (`networkValueBetween`; `weightedValueLeMax`, `leWeightedValueMin`), so interconnection reweights but cannot mint a value outside its parts; and for a nonnegative force the induced change `force / inertia` is antitone in inertia (`inertiaDampsChange`): more inertia, less change. **Evidence:** `ForceNetwork.lean` (`weightedValueLeMax`, `leWeightedValueMin`, `networkValueBetween`, `inertiaDampsChange`). **Falsifier:** a network with nonnegative weights whose aggregate lies outside the range of its parts, or a change that grows with inertia. **Missing entity:** none — pure arithmetic (generalises `MixtureGrowth` from two parts to any finite network). **Source:** the register's own reading, `PAPER.md` §4–5; on-flow companion `ns_force_network.py`.

## C28 — Addition of parts cannot fabricate concentration

**Type:** Formal (arithmetic). **Statement.** A mixture's norm is at most the sum of the parts (`normMixtureLeSum`): adding parts transmits concentration, never creates it. A two-part mixture's ratio — and its energy-weighted square — is bracketed by the parts' ratios, `min <= mixture <= max` (`mixtureRatioBetween`, `weightedSqBetween`), so no averaging can fabricate a ratio above the largest part (`spikeCannotLowerRatio`). **Evidence:** `MixtureGrowth.lean` (`normMixtureLeSum`, `mixtureRatioBetween`, `weightedSqBetween`, `spikeCannotLowerRatio`). **Falsifier:** a mixture whose effective ratio exceeds the maximum part ratio. **Missing entity:** none — machine-checks `dimension_mixture.py`'s “max, not mean”. **Source:** the register's `dimension_mixture.py`; `norm_add_le`.

## C29 — The Onsager sufficiency skeleton: a bounded invariant frees the excess

**Type:** Formal (analytic skeleton). **Statement.** If the enstrophy `Z` is uniformly bounded by `M` on a sample set, then for every excess order `n` the supercritical moment is controlled, `sum Z^{n+1} <= M^n * sum Z` (`weighted_sum_le`): a positive Onsager excess is *free* once the invariant moment is bounded. The contrapositive is the wall itself (`spike_of_excess`): if the supercritical moment exceeds `M^n * sum Z`, then `Z` exceeds `M` somewhere, so an Onsager-violating cascade cannot hide beneath a bounded invariant. An excess weight `w >= 1` makes the supercritical sum dominate the critical one (`excess_majorizes`). **Evidence:** `OnsagerCriterion.lean` (`weighted_sum_le`, `spike_of_excess`, `excess_majorizes`). **Falsifier:** a bounded `Z` whose supercritical moment exceeds `M^n * sum Z`. **Missing entity:** the boundedness of the invariant moment itself (marker `criticalInvariantBoundedOpen`). **Source:** Onsager (1949); the register's `CriticalLadder`.

## C30 — The continuation criterion: the logical shape of the wall

**Type:** Formal (logical skeleton). **Statement.** The logical skeleton every continuation criterion shares, independent of which norm plays the invariant: if a local-existence step is always available while the invariant `N <= M` on `[0,T]` and the flow starts at `0`, then the flow reaches `T` (`exists_upto_of_bounded`); equivalently, if the flow exists at `0` but FAILS at `T`, then no bound `M` holds and the scaling-critical invariant must escape every bound (`unbounded_of_first_failure`). Boundedness is not a technical convenience but exactly what stands between local existence and global regularity. **Evidence:** `ContinuationCriterion.lean` (`exists_upto_of_bounded`, `unbounded_of_first_failure`). **Falsifier:** a flow that stays bounded yet fails to extend, or one that blows up with a bounded invariant. **Missing entity:** which norm is the invariant on the real flow (the object-specific content of C1/C3). **Source:** Beale–Kato–Majda (1984) continuation criterion; the register's `OnsagerCriterion`, `GreatAttractor`.

## C31 — Attracting implies bounded: the sufficiency half of the general mechanism

**Type:** Formal (analytic). **Statement.** Two shapes of “boundedness for free”. (1) *Attracting*: a contraction `f` on a complete nonempty metric space (`ContractingWith K f`, `K < 1`) has its orbit converge to the fixed point (`attracting_orbit_converges`, from Mathlib `tendsto_iterate_fixedPoint`), hence a BOUNDED range (`attracting_orbit_bounded`): “the great attractor does not yet repel” is formally a boundedness statement, so repulsion is the only escape route. (2) *Monotone*: a non-increasing quantity stays below its start (`monotone_bounded`), the arithmetic core of the 2D enstrophy Lyapunov shape that is not available in 3D. **Evidence:** `StableBounded.lean` (`attracting_orbit_converges`, `attracting_orbit_bounded`, `monotone_bounded`). **Falsifier:** a contraction whose orbit is unbounded, or a non-increasing quantity exceeding its initial value. **Missing entity:** none for the arithmetic; the on-flow multiplier is object-specific. **Source:** Mathlib metrization (`tendsto_iterate_fixedPoint`); the register's `orientation_vs_invariant.py` bridge.

## C32 — The sufficiency loop: 2D closes, 3D does not

**Type:** Formal (synthesis). **Statement.** Plugs the register pieces together. If the invariant `N` is non-increasing (the 2D enstrophy shape, `EnstrophyBarrier.mono_step_bounded`) then feeding `M = N 0` to the continuation criterion closes the loop: existence holds at every time (`global_exists_of_mono`). But a per-step increment bounded by `C * (value)^2` (`C > 0`, the 3D shape) admits an invariant that escapes EVERY bound (`quadratic_criterion_unavailable`, from `EnstrophyBarrier.quadratic_step_unbounded`), so the hypothesis the continuation criterion needs holds for no `M`: the sufficiency engine cannot be started from a quadratic increment. **Evidence:** `SufficiencyLoop.lean` (`global_exists_of_mono`, `quadratic_criterion_unavailable`). **Falsifier:** a quadratic-increment invariant that nevertheless admits a uniform bound. **Missing entity:** whether the real 3D enstrophy increment can be controlled below quadratic. **Source:** the register's `EnstrophyBarrier` + `ContinuationCriterion`.

## C33 — Self-similar exponents are forced, and dimension-independent

**Type:** Formal (from `Linear Stability of Candidate Swirl Profiles.md` Frontier 1). **Statement.** The four-way dominant balance of the reduced `(u₁, omega₁)` system forces `(p, q, s, gamma) = (-1, -3/2, -1/2, 1/2)` uniquely and dimension-independently (`forcedExponentsSatisfy`, `forcedExponentsUnique`, `gammaForced`, `sForced`, `qForcedInPoisson`, `pForcedFromOmegaProduction`); the balance system is `n`-free, since the second-order diffusion power and the `kappa = n - 1` advection prefactor rescale coefficients, never powers (`secondOrderPowerPrefactorIndependent`, `advectionTermPowerKappaIndependent`, `uzCoefficientPowerNIndependent`), and the stiffening parameter is monotone in the effective dimension (`kappaMonotone`, `dynamicalNMonotoneStiffening_powersForced`): dimensions add stiffness, never powers. **Evidence:** `SelfSimilarExponents.lean` (`BalanceSystem`, `forcedP`, `forcedQ`, `forcedS`, `forcedGamma`, `forcedExponentsSatisfy`, `gammaForced`, `sForced`, `qForcedInPoisson`, `pForcedFromOmegaProduction`, `forcedExponentsUnique`, `secondOrderPower`, `secondOrderPowerPrefactorIndependent`, `advectionTermPower`, `advectionTermPowerKappaIndependent`, `uzCoefficientPowerNIndependent`, `kappaMonotone`, `dynamicalNMonotoneStiffening_powersForced`, `profile_existence_is_open`, `type_ii_naming_not_certified`). **Falsifier:** a balance solution with exponents other than `(-1, -3/2, -1/2, 1/2)`, or one whose `tau`-powers depend on `n`. **Missing entity:** bounded-profile existence at the forced exponents stays OPEN (`profile_existence_is_open`; marker `selfSimilarProfileExistenceOpen`). **Source:** Hou, arXiv:2405.10916; `Linear Stability of Candidate Swirl Profiles.md` Frontier 1.

## C34 — Zero defines its own position; the wall shrinks itself

**Type:** Formal (removable-value arithmetic). **Statement.** The register's honest wall as a removable 0/0 in the `Removable` idiom (a `Tendsto` on the punctured neighbourhood, never a value AT the point). (1) “zero is the point that defines its own position”: at a fixed point `T x₀ = x₀` with derivative `L`, the change-of-position per change-of-position `(T x - x)/(x - x₀)` has removable value `L - 1` (`fixedPoint_selfSlope`); for the identity the self-shift is `0` (`identity_selfSlope`). (2) “it scales itself on how many zeros it has”: at a point of mutual vanishing the removable value is singled out exactly by the order of vanishing `k` — dividing `(x - x₀)^k * h` by `(x - x₀)^j` gives `h x₀` when `j = k` (`zero_count_removable`), `0` when `j < k` (`zero_count_under`), and blows up when `j > k` (`zero_count_over`). **Evidence:** `ZeroFixedPoint.lean` (`fixedPoint_selfSlope`, `identity_selfSlope`, `zero_count_removable`, `zero_count_under`, `zero_count_over`). **Falsifier:** a removable value at a mutual-vanishing point not singled out by the order of vanishing. **Missing entity:** none for the arithmetic; the wall's on-flow finiteness is diagnostic (`ns_zero_order.py`). **Source:** the register's `THE_LAW_OF_SINGULARITIES.md` §12.1; `Removable`.

## C35 — The one pattern: every critical exponent is the ladder shifted by the order

**Type:** Formal (synthesis). **Statement.** The synthesis brick: every guise of the scaling-critical object is the register ladder `sCrit` shifted by the order. `criticalCurve_through_ladder : criticalSmoothness a p = sCrit p + (1 - a)` — a one-parameter family (parameter = order `a`) passing through the ladder at `a = 1` (`ladder_is_order_one`). The recurrence identity generalises `CriticalLadder.thetaAddSCrit`: `gnExponent p + criticalSmoothness a p = 1/2` at `a = 1`-shift (`theta_add_criticalCurve`, `theta_add_criticalCurve_one`), and the scaling weight vanishes along the whole family (`scalingWeight_vanishes_family`). With orientation — `GreatAttractor` — the whole register is two numbers: an order selecting the rung and a multiplier selecting the side. **Evidence:** `OnePattern.lean` (`criticalCurve_through_ladder`, `ladder_is_order_one`, `theta_add_criticalCurve`, `theta_add_criticalCurve_one`, `scalingWeight_vanishes_family`). **Falsifier:** a critical exponent not lying on the one-parameter order-shifted ladder. **Missing entity:** none — synthesis of already-checked bricks. **Source:** the register capstone; `CriticalLadder`, `GreatAttractor`.

**Missing entity:** none — synthesis of already-checked bricks. **Source:** the register capstone; `CriticalLadder`, `GreatAttractor`.

## C36 — The discrete Noether theorem: the Conservation mechanism

**Type:** Formal (arithmetic). **Statement.** The register names five 0/0 mechanisms, of which only three were Lean-formalised (Probe C19, Vanishing Rate C18/C20, Index C21); the Conservation mechanism — “the conserved quantity is the ratio of two quantities that both vanish when the symmetry is broken” — had only prose. This card gives it a formal core over a finite site set: a configuration is a velocity field `v : ι → ℝ`, its momentum is the sum `Σᵢ vᵢ` (`momentum`), and the charge carried by `q` against `qm` is the total displacement `Σᵢ (qᵢ − qmᵢ)` (`charge`). The charge **is** a difference of two momenta (`charge_eq_momentum_sub`), vanishes with no displacement (`charge_self`), is invariant under a simultaneous translation of both configurations (**the symmetry**; `charge_translation_invariant`), and equals the removable value of the momentum rate `(Σᵢ vᵢ·dt)/dt` (`momentum_from_rate`, the Probe face). **The discrete Noether theorem:** for a balanced force field (`∀ q, Σᵢ Fᵢ(q) = 0`, the infinitesimal form of translation invariance) the time-symmetric update `q_{k+1} = 2 q_k - q_{k-1} + F(q_k)` conserves the charge (`momentum_conserved`); along any such trajectory the momentum equals its initial value at every step (`momentumAt_eq_initial`), and `conservationLaw` bundles the symmetry, the balance law and the constancy. **Evidence:** `NoetherDiscrete.lean` (`charge_eq_momentum_sub`, `charge_self`, `charge_translation_invariant`, `momentum_from_rate`, `momentum_conserved`, `momentumAt_conserved`, `momentumAt_eq_initial`, `conservationLaw`). **Falsifier:** a balanced force whose discrete-Newton step changes the charge, or a "symmetry" translation that changes it. **Missing entity:** none for the finite arithmetic; the continuum limit / field-theoretic Noether theorem is not taken here. **Source:** Noether, *Invariante Variationsprobleme* (1918); the register's `ZeroMechanisms.lean` Conservation mechanism.

## Sources for the missing entities (summary)

| missing entity | closest existing work |
|---|---|
| boundedness of `||u||_{B^{-1}_{\inf,\inf}}` | Cheskidov–Shvydkoy 2010 (arXiv:0708.3067); Ri 2023 (arXiv:2307.11312, unrefereed) |
| quantitative continuation / next-order term | Tao 2016, 2021; Feng–He–Wang 2025; arXiv:2411.06483 |
| Lyapunov/orientation exponent identification | Beale–Kato–Majda 1984; Constantin–Fefferman 1993; Deng–Hou–Yu 2015 |
| `mu = lambda` for the real flow (C10-open) | discrete form proved in `OrientationLaw.lean`; continuous bridge: BKM 1984; Constantin–Fefferman 1993; Deng–Hou–Yu 2015 |
| intermittency / multifractal bridge | Constantin 1994; Frisch 1995; Sreenivasan |
| dimension threshold / Riesz potentials | Adams–Hedberg 1996; Tao (dim. regularisation) |
| method barriers (P vs NP) | Baker–Gill–Solovay 1975; Razborov–Rudich 1997; Aaronson–Wigderson 2008 |

## What is machine-checked here

`ExplicitClaims.lean` (axioms exactly `[propext, Classical.choice, Quot.sound]`):
`morrey_threshold`, `physical_embedding_gap`, `extra_power_strengthens_above_unit`,
`mean_le_dimMixture`. `OrientationLaw.lean` (same axiom set): `logGrowth_geometric`,
`sign_match`, `orientation_reads_wall` (card C10's model core), the generalization
`logGrowth_of_ratio_eq` / `logGrowth_pos_iff` / `bounded_of_nonpos_logGrowth` /
`exists_pos_logGrowth_of_unbounded`, the discrete BKM integral
`log_eq_sum_logGrowth`, `bounded_of_bounded_sum_logGrowth`, `unbounded_sum_of_unbounded`,
and the CONTINUOUS BKM integral `contLogGrowth_integral`, `continuous_content_bounded`
(13 formalised facts). `DissipativeFlow.lean` (same axiom set): `logGrowth_deriv`,
`logGrowth_nonpos_of_dissipative`, `content_le_initial_of_dissipative` -- the
dissipative (L^2-energy) face of card C10, `X T <= X 0` under non-positive log-growth.
`RegularityReduction.lean` (same axiom set): `content_le_exp_of_integral_le`,
`regularity_reduced_to_integral`, `integral_unbounded_of_content_unbounded`,
`integral_le_of_content_le`, `regularity_iff_integral_bounded` -- the wall reduced to a
single inequality and stated as an EQUIVALENCE (content bounded iff `int_0^T g` bounded;
5 formalised facts).
`SerrinSufficiency.lean` (same axiom set): `serrinMargin_pos_iff`, `serrinMargin_line`,
`serrinMargin_eq_neg_ladder` (supercritical-margin arithmetic), `content_le_of_growth_le_weight`,
`bounded_on_of_serrinAction` -- the classical Prodi-Serrin SUFFICIENCY direction
(finite supercritical control bounds the content; 5 formalised facts).
`MarginCrossing.lean` (same axiom set): `existsUnique_zero_of_strictAntiOn` (an antitone
`lambda` has a unique zero -- the margin `s*` is well-defined), `side_of_crossing` (the
zero separates the repelling from the attracting side), `margin_existsUnique` (3 facts).
`FirstCrossing.lean` (same axiom set): `exists_first_zero` (a continuous sign change has an
interior FIRST zero, with `f > 0` to its left -- no monotonicity assumed) and
`margin_exists_firstCrossing` (that first zero is exact: no earlier zero; 2 facts).
`LogicBarrier.lean` (axiom-FREE): `lawvere_fixedpoint` (Lawvere's diagonal fixed-point
theorem), `no_surjective_of_no_fixedpoint`, `no_surjective_predicates` (Cantor), and
`diagonal_not_mem_range` -- the shared skeleton of Cantor/Gödel/Turing, card C14's formal
core (4 facts). `ZeroLink.lean` (axioms `⊆ [Quot.sound]`): `empty_unique_arrow`,
`empty_isInitial`, `unit_isTerminal`, `empty_classified_initial`,
`unit_classified_terminal`, `zero_links_all` -- card C15's structural core: the empty
type is initial, `PUnit` terminal, `0` the identity of `+` and annihilator of `×`
(11 facts). `ZeroObject.lean` (same axiom set): `initial_link`, `terminal_link`,
`zero_isInitial`, `zero_isTerminal`, `zero_links_both_ways`, `zero_unique_up_to_iso`,
`modules_haveZeroObject`, `modules_exists_zeroObject`, `modules_zero_links` -- card
C16: a category with a zero object has ONE object that is at once origin and target,
and `ModuleCat R` is such a category (9 facts). `RemovableValue.lean` (same axiom
set): `IsRemovableValue`, `removable_value_unique`, `existsUnique_iff_exists_and_unique`,
`extension_unique`, `removable_exists_unique`, `removable_value_bridge`,
`initial_arrow_schema` -- card C17: the removable value of a 0/0 is a genuine `∃!`,
the same schema as the initial arrow, so removability is existence + uniqueness
(7 facts). `VanishOrder.lean` (same axiom set): `VanishesToOrder`, `divideOut`,
`vanishes_zero`, `vanishes_succ_imp`, `vanishes_shift`, `HasGrade`, `hasGrade_canonical`,
`hasGrade_shift`, `vanishes_antitone`, `grade_unique`, `order_is_graded` -- the order of
vanishing as a decreasing `ℕ`-filtration whose grade shifts by one when a zero is
divided out vanishing as a decreasing `ℕ`-filtration whose grade shifts by one when a zero is
divided out (11 formalised facts). `ZeroProbe.lean` (same axiom set): `ProbeValue`,
`probe_identity`, `probe_self`, `probe_value_unique`, `probe_is_removable` -- card C19:
the Probe mechanism, an identity 0/0 resolving to `1` (5 facts). `ZeroValuation.lean`
(same axiom set): `HasOrder`, `hasOrder_one`, `hasOrder_zero_iff`, `hasOrder_mul`,
`hasOrder_pow`, `hasOrder_canonical`, `hasOrder_lt_imp_not`, `hasOrder_unique`,
`order_is_valuation` -- card C20: the order of vanishing as a valuation that is
additive under products (9 facts). `ZeroIndex.lean` (same axiom set): `Index`,
`index_one`, `index_additive`, `index_pow`, `index_X_sub_C_self`, `index_pow_self`,
`index_canonical`, `index_is_multiplicity` -- card C21: the root multiplicity as an
additive integer (the algebraic face of the Index mechanism; 8 facts).
`ZeroMechanisms.lean` (same axiom set): `abs_div_self_tendsto_right`,
`abs_div_self_tendsto_left`, `abs_div_self_no_limit`, `abs_vanish`, `id_vanish`,
`anti_class_nonempty`, `mechanisms_close` -- card C22: the anti-class is nonempty (a
genuine 0/0, `|x|/x`, with no removable value) and the mechanism faces bundled
(7 facts). `RemovableComplexBridge.lean` (same axiom set): `IsRemovableValueAt`,
`removable_value_exists`, `removable_value_unique`, `exists_unique_removable_value`,
`limUnder_eq_of_isRemovableValue`, `canonical_zero_over_zero` -- card C23: Riemann's
removable singularity theorem (Mathlib) read through the register's 0/0 schema over
`ℂ`; the bounded holomorphic 0/0 has an *existing, unique* removable value, the
`ℂ` twin of C17 (6 facts). `LiouvilleBridge.lean` (same axiom set): `bounded_entire_const`,
`bounded_entire_apply_eq`, `bounded_entire_value_unique`, `eq_zero_of_bounded_of_eq_zero`,
`bounded_at_infinity_const` -- card C24: Liouville's theorem (Mathlib) in register form,
the *global* dual of C23 -- a bounded entire function is constant, so a bounded entire 0/0
vanishes identically (5 facts). The capstone
`TheoryOfEverything.method_and_margin_barriers` bundles the
order margin (existence always, uniqueness under antitonicity) and the method barrier
alongside `twoNumbersClose`.
The **Navier–Stokes wall bricks** (cards C25 … C35, same axiom set
`⊆ {propext, Classical.choice, Quot.sound}`) are the arithmetic core of the open wall,
each kernel-checked and now card-linked: `SerrinLadder.lean` (C25, 13 facts — the
interpolation ladder `theta(p) = 3/2 - 3/p`, ceiling `p = 6`, and the one-extra-power
gap); `GreatAttractor.lean` (C26, 13 facts — fixed-point orientation `|L| ⋚ 1` and the
order-shifted critical rung); `ForceNetwork.lean` (C27, 4 facts — interconnection
reweights, inertia damps change); `MixtureGrowth.lean` (C28, 4 facts — addition of parts
cannot fabricate concentration); `OnsagerCriterion.lean` (C29, 3 facts — bounded
invariant frees the excess, its contrapositive is the wall); `ContinuationCriterion.lean`
(C30, 2 facts — bounded invariant ⟺ no blow-up); `StableBounded.lean` (C31, 3 facts —
attracting ⇒ bounded); `SufficiencyLoop.lean` (C32, 2 facts — 2D closes, 3D does not);
`SelfSimilarExponents.lean` (C33, 20 facts — forced, dimension-independent self-similar
exponents; two honest open-marker restatements); `ZeroFixedPoint.lean` (C34, 5 facts —
zero defines its own position, the wall shrinks itself); `OnePattern.lean` (C35, 5 facts
— every critical exponent is the ladder shifted by the order). Each card names its
missing entity (the open wall) explicitly; none is a Millennium result.

The **Conservation-mechanism brick** (card C36, same axiom set
`⊆ {propext, Classical.choice, Quot.sound}`) closes the last unformalised 0/0
mechanism: `NoetherDiscrete.lean` (C36, 8 quoted facts — the discrete Noether
theorem: a balanced force conserves the charge under the time-symmetric update, so
momentum is a constant of the motion).

The remaining cards are cited (Theorem) or left OPEN with a
named missing entity (Conjecture; see C10-open). No card here is a Millennium result.
