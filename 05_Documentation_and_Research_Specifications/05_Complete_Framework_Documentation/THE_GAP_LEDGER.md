# The Gap Ledger

**Status: one source of truth.** The register (`EXPLICIT_CLAIMS.md`) enumerates
what is quoted; this ledger enumerates what is **missing** to close open
problems. It is wired to a gate (`test_gap_ledger.py`) that enforces
consistency with `EXPLICIT_CLAIMS` tokens, forbids UNRESEARCHED rows, and
fails when any row is stale by > 365 days.

---

## G1 — NS regularity: the endpoint ladder remains open
- **Tier:** A (register debt)
- **Subject:** Navier–Stokes 3D smoothness
- **Status:** RESEARCHED
- **Related cards:** C3, C8-open
- **as_of:** 2026-10-18
- **Reduction:** `u ∈ L^∞_tL²_x ∩ L²_tḢ¹_x` (Leray–Hopf) → need unconditional scale-critical control (`L^p_tL^q_x`, `2/p+3/q<=1`; `L^∞_tL³_x` closed by ESS 2003, `BMO⁻¹` small-data only).
- **Known:** Leray (1934), LPS (1959/63/67), ESS (2003), Kato (1984), Koch–Tataru (2001), CKN (1982), Vasseur (2007), Gustafson–Kang–Tsai (2007).
- **Barrier:** energy bounds are supercritical under `u^λ=λu(λx,λ²t)`; no general proof of endpoint `B^{-1}_{∞,∞}` control for arbitrary Leray–Hopf solution. The hierarchy of regularity: weak (not unique, known to exist) ⊏ strong (unique, short-time) — the bridge is the missing unconditional scale-critical bound.
- **Missing (the object that does not exist as a proof):** an **unconditional** estimate placing an arbitrary Leray–Hopf solution into a scale-critical space on the `2/p+3/q=1` line for all `t<T_{max}` (with no additional regularity hypothesis). In particular, for the endpoint associated to `B^{-1}_{∞,∞}` (C3) there is no known proof that `‖u(·,t)‖_{B^{-1}_{∞,∞}}` is controlled a priori from the energy identity alone.
- **Falsifier:** exhibit a Leray–Hopf sequence or a rigorous counterexample logic showing the bound is false; or, conversely, a proof constructing such an a priori estimate. (Computational checks are not sufficient.)

## G2 — T3: λ(s) antitonicity
- **Tier:** A (register debt)
- **Subject:** Navier–Stokes/Burgers family
- **Status:** RESEARCHED
- **Related cards:** C3, C8-open
- **as_of:** 2026-10-18
- **Reduction:** the monotonicity of `λ(s)` (in the scaling order `s`) is assumed (T3 OPEN) to close the margin gap and to align the endpoint ladder.
- **Barrier:** equivalence of all `2/p+3/q=1` endpoint points does not by itself imply `λ(s)` antitone for the NS/Burgers family. The scaling map identifies norms only up to constants; monotonicity requires genuine endpoint embeddings for the concrete family, not just scale invariance.
- **Known:** Prodi–Serrin/Ladyzhenskaya hierarchy; endpoint `L^∞_tL³_x` (ESS); Koch–Tataru `BMO⁻¹` (small-data).
- **Missing (the object that does not exist as a proof):** a proof that for the actual NS/Burgers family, `s < t` (in the admissible scaling order used by the register) implies `λ(s) >= λ(t)` (antitone), under the admissible interpolation/embedding chain that enters `B^{-1}_{∞,∞}`. Alternatively, the dependency graph: which embeddings are needed (Besov/Morrey `B^{-1+3/p}_{p,∞}` ladder → `BMO⁻¹` → `B^{-1}_{∞,∞}`?) and why they hold unconditionally for Leray–Hopf.
- **Falsifier:** construct an explicit family within the Burgers/NS model class where `λ(s)` is not monotone on that chain, or show some required embedding fails unconditionally. Proof of monotonicity for the concrete family (with cited lemmas) closes T3.

## G3 — Bridge barrier (shared across mixture-of-dimensions readings)
- **Tier:** A (register debt)
- **Subject:** bridge across the four readings
- **Status:** RESEARCHED
- **Related cards:** C3, C8-open
- **as_of:** 2026-10-18
- **Reduction:** the single open content recurs identically across four readings (the "bridge barrier"). If it is the same obstruction, the gap should reduce to one constructive reading.
- **Barrier:** identifying equivalence does not force constructivity — the isomorphism is structural, not algorithmic for producing the missing a priori control.
- **Known:** four readings of "mixture of all dimensions"; identical open content shape.
- **Missing (the object that does not exist as a proof):** a proof that exactly one reading is **constructive** (yields an unconditional a priori bound for Leray–Hopf), or a proof the bridge is **irreducible** (all four equivalent and none constructive).
- **Falsifier:** find a counterexample in embedding/translation between readings that breaks equivalence of the open content, or produce the missing bound via one reading.

## G4 — Φ / InformationPhi (empirical, not formal)
- **Tier:** A (register debt)
- **Subject:** register's model
- **Status:** RESEARCHED
- **Related cards:** C17, C10
- **as_of:** 2026-10-18
- **Reduction:** `InformationPhi.lean` documents the register entropy production/orientation; the bound `k_B T log 2` is cited as input.
- **Barrier:** model is register-internal (not a measured result).
- **Missing:** empirical/operational link to a physical observable, not a PDE proof.

## G5 — Margin uniqueness (refuted by family)
- **Tier:** A (register debt)
- **Subject:** uniqueness of margin
- **Status:** RESEARCHED
- **Related cards:** C11, C12
- **as_of:** 2026-10-18
- **Reduction:** `boundedOrientation r = (1/2)tanh(c·log r)` satisfies the composition law for every real `c` — uniqueness is false.
- **Barrier:** the margin cannot be forced unique by the law alone; closeness/selection remains open.
- **Missing (the object that does not exist as a proof):** an **additional selection axiom** (with a physical/mathematical justification) that picks a canonical `c`, or a proof that all `c` are equivalent for all claims. The ledger requires either a canonical choice with justification, or a no-go proof.
- **Falsifier:** show no such selection is compatible with the register's claims, or derive contradiction from a proposed selection axiom.

## G6 — BSD (rank >= 2)
- **Tier:** B (Millennium scope)
- **Subject:** Birch–Swinnerton-Dyer
- **Status:** RESEARCHED
- **Related cards:** []
- **as_of:** 2026-10-18
- **Reduction:** rank<=1 Kolyvagin; rank>=2 needs Euler system detecting two independent Heegner classes.
- **Barrier:** Euler system only generates one per imaginary quadratic field; no known rank>=2 Euler system.
- **Missing:** construction of a rank>=2 Euler system (or equivalent to control Sha for product), not better computation.

## G7 — Hodge (codim >= 2)
- **Tier:** B (Millennium scope)
- **Subject:** Hodge conjecture
- **Status:** RESEARCHED
- **Related cards:** []
- **as_of:** 2026-10-18
- **Reduction:** (1,1) Lefschetz; codim>=2 open (quintic threefold canonical example).
- **Barrier:** no known geometric construction producing algebraic cycles representing general (2,1) Hodge classes.
- **Missing:** algebraic cycle construction for codim>=2 classes, not computation.

## G8 — Riemann Hypothesis
- **Tier:** B (Millennium scope)
- **Subject:** Riemann Hypothesis
- **Status:** RESEARCHED
- **Related cards:** []
- **as_of:** 2026-10-18
- **Reduction:** Li inequality verified n=1..30 (800 zeros); Turing/interval arithmetic only.
- **Barrier:** zero location proof still missing; known equivalences don't create the zero-free/critical-line proof.
- **Missing:** proof all nontrivial zeros on Re(s)=1/2 (technique gap), not more zeros.

## G9 — Goldbach
- **Tier:** B (Millennium scope)
- **Subject:** Goldbach conjecture
- **Status:** RESEARCHED
- **Related cards:** []
- **as_of:** 2026-10-18
- **Reduction:** circle method gives r(N)>0 for large N but N0 not effectively computable; Chen crosses to semiprime+prime (parity).
- **Barrier:** parity barrier of sieve methods.
- **Missing:** technique to cross parity barrier (or effective N0 + exhaustive small range closure by proof), not more verification.

## G10 — P vs NP
- **Tier:** B (Millennium scope)
- **Subject:** P vs NP
- **Status:** RESEARCHED
- **Related cards:** []
- **as_of:** 2026-10-18
- **Reduction:** natural proofs (Razborov–Rudich), algebraization (Aaronson–Wigderson), relativization (Baker–Gill–Solovay) rule out standard classes.
- **Barrier:** no known super-polynomial circuit lower bound for any explicit NP function.
- **Missing:** a non-relativizing, non-algebraizing, non-natural lower-bound method, not more algorithms.

## G11 — Yang–Mills mass gap
- **Tier:** B (Millennium scope)
- **Subject:** Yang–Mills existence & mass gap
- **Status:** RESEARCHED
- **Related cards:** []
- **as_of:** 2026-10-18
- **Reduction:** gap to rigorous 4D YM construction + spectral gap remains.
- **Barrier:** constructive quantum field theory in 4D nonabelian: renormalization + mass gap unproven in a mathematically rigorous sense.
- **Missing:** rigorous construction of pure YM in 4D with mass gap (technique/construction), not lattice numerics.