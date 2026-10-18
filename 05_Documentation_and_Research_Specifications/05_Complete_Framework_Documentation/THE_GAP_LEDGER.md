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
- **Barrier:** model is register-internal (not a measured result); operational definition of the observable is missing.
- **Known:** orientation–growth link (C10), removable value schema (C17), information/entropy markers in the register.
- **Missing (the object that does not exist as a proof):** an **operational, reproducible experiment** (or a derivation from first principles linking to a measured quantity) that connects `Φ`/`InformationPhi` to a physical observable with defined units, protocol, and error bounds. The ledger requires an empirical anchor (not a PDE proof).
- **Falsifier:** failing to reproduce the reported relation under stated conditions, or a measurement that contradicts the bound with stated uncertainty. Also, if no operational definition exists, the claim remains untestable.

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
- **Known:** Gross–Zagier (1986), Kolyvagin (1990), Rubin (1991), Kato (1993).
- **Missing (the object that does not exist as a proof):** a **rank>=2 Euler system** (or an equivalent construction) that produces two linearly independent Selmer classes for a curve of algebraic rank>=2, or a proof of the BSD equality for some rank>=2 curve without assuming the conjectural Euler-system construction. The derivation must identify the missing object, not just cite partial results.
- **Falsifier:** a curve of analytic rank>=2 for which the proposed construction fails to produce independent classes, or a counterexample to the claimed control over Sha.

## G7 — Hodge (codim >= 2)
- **Tier:** B (Millennium scope)
- **Subject:** Hodge conjecture
- **Status:** RESEARCHED
- **Related cards:** []
- **as_of:** 2026-10-18
- **Reduction:** (1,1) Lefschetz; codim>=2 open (quintic threefold canonical example).
- **Barrier:** no known geometric construction producing algebraic cycles representing general (2,1) Hodge classes.
- **Known:** Lefschetz (1924), Murty (1979), Clemens (1984), Griffiths (1984).
- **Missing (the object that does not exist as a proof):** a geometric construction that produces, for the relevant (2,1) Hodge classes on a smooth projective variety (e.g. quintic threefold), explicit algebraic cycles with nonzero projection onto those components, or a theorem showing the obstruction is unavoidable in a given class. Must specify the target variety/class.
- **Falsifier:** the constructed cycle has zero Hodge-theoretic pairing with the claimed (2,1) forms, or the proposed construction fails on the standard example.

## G8 — Riemann Hypothesis
- **Tier:** B (Millennium scope)
- **Subject:** Riemann Hypothesis
- **Status:** RESEARCHED
- **Related cards:** []
- **as_of:** 2026-10-18
- **Reduction:** Li inequality verified n=1..30 (800 zeros); Turing/interval arithmetic only.
- **Barrier:** zero location proof still missing; known equivalences don't create the zero-free/critical-line proof.
- **Known:** Hardy–Littlewood, Montgomery, Odlyzko, Conrey, de Branges framework context, Li criterion.
- **Missing (the object that does not exist as a proof):** a proof that for all nontrivial zeros ρ of ζ(s), Re(ρ)=1/2 (or a direct equivalence chain closed without the numerical step as proof of the universal claim). The ledger rejects "more zeros verified" as closure.
- **Falsifier:** any nontrivial zero found off the critical line under sufficient precision, or a logical gap in the equivalence chain used.

## G9 — Goldbach (strong)
- **Tier:** B (Millennium scope)
- **Subject:** Goldbach conjecture (strong/binary)
- **Status:** RESEARCHED
- **Related cards:** []
- **as_of:** 2026-10-18
- **Reduction:** ternary (every odd >= 7 sum of three primes) was proved by Helfgott (2013/2014) (unconditional). Strong (binary): every even >= 4 sum of two primes remains open.
- **Barrier:** parity barrier of sieve methods; effective minor-arc bounds + Siegel zeros complicate explicit N0.
- **Known:** Vinogradov (1937), Chen (1973), Helfgott (ternary), Oliveira e Silva (2013) exhaustive checks.
- **Missing (the object that does not exist as a proof):** a technique to cross the parity barrier (or an effective N0 and a proof covering all N <= N0 + the large-N tail by a non-sieve method), yielding an unconditional proof for all even n>=4.
- **Falsifier:** an even integer n>=4 with no representation as sum of two primes, or a logical gap in the large-N tail bound.

## G10 — P vs NP
- **Tier:** B (Millennium scope)
- **Subject:** P vs NP
- **Status:** RESEARCHED
- **Related cards:** []
- **as_of:** 2026-10-18
- **Reduction:** natural proofs (Razborov–Rudich), algebraization (Aaronson–Wigderson), relativization (Baker–Gill–Solovay) rule out standard classes.
- **Barrier:** no known super-polynomial circuit lower bound for any explicit NP function.
- **Known:** Razborov–Rudich (1997), Aaronson–Wigderson (2003), Baker–Gill–Solovay (1975).
- **Missing (the object that does not exist as a proof):** a non-relativizing, non-algebraizing, non-natural lower-bound method that yields a super-polynomial (or exponential) circuit lower bound for some explicit function in NP, or a constructive proof P=NP.
- **Falsifier:** a relativized world where the claimed method fails, or the claimed lower-bound proof collapsing under algebraization/natural-proofs tests, or an explicit polynomial circuit for an NP-complete function.

## G11 — Yang–Mills mass gap
- **Tier:** B (Millennium scope)
- **Subject:** Yang–Mills existence & mass gap
- **Status:** RESEARCHED
- **Related cards:** []
- **as_of:** 2026-10-18
- **Reduction:** gap to rigorous 4D YM construction + spectral gap remains.
- **Barrier:** constructive quantum field theory in 4D nonabelian: renormalization + mass gap unproven in a mathematically rigorous sense.
- **Known:** lattice gauge theory (Wilson), constructive QFT program (Glimm–Jaffe–Spencer, etc.), asymptotic freedom (Gross–Wilczek, Politzer).
- **Missing (the object that does not exist as a proof):** a rigorous construction of pure Yang–Mills theory in 4D on R^4 (in the appropriate Wightman/Haag–Kastler or Osterwalder–Schrader sense) that exhibits a **strictly positive mass gap** m>0 (a gap in the spectrum above the vacuum).
- **Falsifier:** failure to satisfy Wightman axioms, failure to prove clustering/existence, or proof the constructed theory is trivial / has continuous spectrum to 0. Not satisfied by lattice numerics alone.