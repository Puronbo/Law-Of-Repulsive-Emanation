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
empirical across 6 systems (`orientation_vs_invariant.py`). **Falsifier:** a
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

**Type:** Interpretive (the one non-falsifiable card; kept to record the map).
**Statement.** The recurring obstruction is (method-barrier / existence-barrier /
bridge-barrier), not one theorem. **Sources:** P vs NP: Baker–Gill–Solovay (1975),
Razborov–Rudich (1997), Aaronson–Wigderson (2008); Yang–Mills: Osterwalder–Schrader
(1973), Jaffe–Witten (2000); NS/BSD/RH as in the register.

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
`exists_pos_logGrowth_of_unbounded`, and the discrete BKM integral
`log_eq_sum_logGrowth`, `bounded_of_bounded_sum_logGrowth`, `unbounded_sum_of_unbounded`
(11 formalised facts). The remaining cards are cited (Theorem) or left OPEN with a
named missing entity (Conjecture; see C10-open). No card here is a Millennium result.
