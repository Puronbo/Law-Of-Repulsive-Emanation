# The Gap Ledger

**Status: one source of truth.** The register (`EXPLICIT_CLAIMS.md`) enumerates
what is quoted; this ledger enumerates what is **missing** to close open
problems. It is wired to a gate (`test_gap_ledger.py`) that enforces
consistency with `EXPLICIT_CLAIMS` tokens, forbids UNRESEARCHED rows, and
fails when any row is stale by > 365 days.

**Proof-attempt kinds** (controlled vocabulary, Gate D): `certificate` (a
finite, in-repo, machine-checked certificate pin), `partial` (a real partial
result / reduction exists), `no-go` (a refutation of a strengthened/naive
version), `citation-only` (external citation, no repo artifact), `none` (no
artifact). Every non-`none` row must carry at least one live `**Pin:**`.

---

## G1 — NS regularity: the endpoint ladder remains open
- **Tier:** A (register debt)
- **Subject:** Navier–Stokes 3D smoothness
- **Status:** RESEARCHED
- **Related cards:** C3, C8-open
- **Proof attempt:** partial - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/NavierStokes.lean
- **Pin:** test_ledger_artifacts_attach_no_sorry
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
- **Proof attempt:** partial - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/SerrinLadder.lean
- **Pin:** test_ledger_artifacts_attach_no_sorry
- **Pin:** test_serrin_ladder_ceiling_arithmetic_certificate
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
- **Proof attempt:** partial - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/MillenniumBridge.lean
- **Pin:** test_ledger_artifacts_attach_no_sorry
- **Pin:** test_bridge_statement_grade_classification_certificate
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
- **Proof attempt:** citation-only - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/InformationPhi.lean
- **Pin:** test_ledger_artifacts_attach_no_sorry
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
- **Proof attempt:** no-go - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/OrientationBoundedness.lean
- **Pin:** test_margin_law_admits_scale_family
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
- **Proof attempt:** partial - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/BSD.lean
- **Pin:** test_ledger_artifacts_attach_no_sorry
- **as_of:** 2026-10-18
- **Reduction:** rank<=1 settled (Gross-Zagier 1986 + Kolyvagin 1990, extended to all E/Q by modularity); rank>=2 needs an Euler system detecting two independent Heegner classes.
- **Barrier:** Euler system only generates one class per imaginary quadratic field; no known rank>=2 Euler system. Average-rank bounds (Bhargava-Shankar, avg rank <= 0.885) and majority results (Bhargava-Skinner-Zhang 2014, >66% of E/Q satisfy BSD) constrain proportions but do not produce two independent classes for any rank>=2 curve.
- **Known:** Gross-Zagier (1986), Kolyvagin (1990), Rubin (1991), Kato (2004), Skinner-Urban (2014), Bhargava-Shankar (2015, avg rank <= 0.885), Bhargava-Skinner-Zhang (2014, >66% satisfy BSD).
- **Missing (the object that does not exist as a proof):** a **rank>=2 Euler system** (or an equivalent construction) that produces two linearly independent Selmer classes for a curve of algebraic rank>=2, or a proof of the BSD equality for some rank>=2 curve without assuming the conjectural Euler-system construction. The derivation must identify the missing object, not just cite partial results. Average-rank/Selmer and majority results bound the proportion of low-rank curves but yield no unconditional rank>=2 instance.
- **Falsifier:** a curve of analytic rank>=2 for which the proposed construction fails to produce independent classes, or a counterexample to the claimed control over Sha.

## G7 — Hodge (codim >= 2)
- **Tier:** B (Millennium scope)
- **Subject:** Hodge conjecture
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** partial - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/Hodge.lean
- **Pin:** test_ledger_artifacts_attach_no_sorry
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
- **Proof attempt:** certificate - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/RH/LiCriterion.lean, 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/rh_li_correct.py
- **Pin:** test_rh_li_correct_is_a_finite_check
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
- **Proof attempt:** certificate - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/Goldbach.lean, 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/goldbach_large.py
- **Pin:** test_goldbach_large_is_a_finite_certificate
- **Pin:** test_goldbach_extended_finite_certificate
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
- **Proof attempt:** partial - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/PvsNP.lean, 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/p_np_contour.py
- **Pin:** test_lean_open_markers_pinned_and_no_sorry
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
- **Proof attempt:** partial - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/MassGap.lean
- **Pin:** test_ledger_artifacts_attach_no_sorry
- **as_of:** 2026-10-18
- **Reduction:** gap to rigorous 4D YM construction + spectral gap remains.
- **Barrier:** constructive quantum field theory in 4D nonabelian: renormalization + mass gap unproven in a mathematically rigorous sense.
- **Known:** lattice gauge theory (Wilson), constructive QFT program (Glimm–Jaffe–Spencer, etc.), asymptotic freedom (Gross–Wilczek, Politzer).
- **Missing (the object that does not exist as a proof):** a rigorous construction of pure Yang–Mills theory in 4D on R^4 (in the appropriate Wightman/Haag–Kastler or Osterwalder–Schrader sense) that exhibits a **strictly positive mass gap** m>0 (a gap in the spectrum above the vacuum).
- **Falsifier:** failure to satisfy Wightman axioms, failure to prove clustering/existence, or proof the constructed theory is trivial / has continuous spectrum to 0. Not satisfied by lattice numerics alone.

## G12 — Collatz (3n+1)
- **Tier:** B (external open)
- **Subject:** Collatz conjecture (3n+1)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/Collatz.lean
- **Pin:** test_collatz_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** verified for all n < 2^68 (Barina 2020/21); the repo's `collatz_0_over0.py` frames stopping time as a 0/0.
- **Barrier:** no known invariant/monotone potential that strictly descends for all n>1; two independent obstructions (nontrivial cycles, divergent trajectories).
- **Known:** Lagarias survey, Oliveira e Silva, Barina (2^68, 2020).
- **Missing (the object that does not exist as a proof):** an invariant/potential function on the positive integers that strictly decreases under the Collatz map for every n>1, ruling out both nontrivial cycles and divergent trajectories, and forcing descent to 1.
- **Falsifier:** an n>1 whose trajectory never reaches 1 (a nontrivial cycle or a divergent orbit).

## G13 — Twin prime conjecture
- **Tier:** B (external open)
- **Subject:** twin prime conjecture
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/TwinPrime.lean
- **Pin:** test_twin_prime_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** Zhang (2013) bounded gaps ≤ 246 (Polymath8b / Maynard–Tao); the gap-2 case remains open.
- **Barrier:** parity barrier — sieve methods cannot distinguish two-prime from almost-prime configurations; needs input beyond upper/lower sieve bounds.
- **Known:** Brun (1919), Zhang (2013), Maynard–Tao (2014), Polymath8b (246).
- **Missing (the object that does not exist as a proof):** a proof that infinitely many primes p have p+2 also prime (e.g. a parity-crossing method, a Siegel-zero-free route, or a Friedlander–Iwaniec-type bilinear structure).
- **Falsifier:** a valid theorem that the set of twin primes is finite, or a demonstrated failure of the core bounded-gap estimate.

## G14 — Legendre's conjecture
- **Tier:** B (external open)
- **Subject:** Legendre's conjecture (a prime between n² and (n+1)²)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/Legendre.lean
- **Pin:** test_legendre_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** follows from a prime-gap bound of size O(√x) (e.g. θ(x)=x+O(x^{1/2+ε})); verified numerically to large n.
- **Barrier:** no unconditional prime-gap bound this small is known; best is ~x^{0.525} (Baker–Harman–Pintz 2001).
- **Known:** Legendre (1808), Ingham, Baker–Harman–Pintz (2001), Guth–Maynard (2016).
- **Missing (the object that does not exist as a proof):** an unconditional proof that π((n+1)²) > π(n²) for every n (a prime in every interval [n²,(n+1)²)).
- **Falsifier:** an n with no prime strictly between n² and (n+1)².

## G15 — Brocard's conjecture
- **Tier:** B (external open)
- **Subject:** Brocard's conjecture (≥ 4 primes between p_n² and p_{n+1}²)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/gap_prime_gaps_certificate.py
- **Pin:** test_brocard_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** a stronger prime-density statement in short intervals near squares than any unconditional bound currently gives.
- **Barrier:** depends on prime distribution in intervals of relative size ~ p_{n+1}²−p_n² ≈ 2 p_n (p_{n+1}−p_n), far beyond current unconditional means.
- **Known:** Brocard (1904), verified numerically for large n; related to Oppermann's conjecture.
- **Missing (the object that does not exist as a proof):** a proof that every interval (p_n², p_{n+1}²) contains at least four primes for all n (no unconditional proof for all n; finite certificate verified to 10^7 only).
- **Falsifier:** an index n with at most three primes strictly between p_n² and p_{n+1}².

## G16 — Andrica's conjecture
- **Tier:** B (external open)
- **Subject:** Andrica's conjecture (√p_{n+1} − √p_n < 1 for all n)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/gap_prime_gaps_certificate.py
- **Pin:** test_andrica_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** equivalent to a prime gap bound g_n = p_{n+1}−p_n < 2√p_n + 1; verified numerically to large n.
- **Barrier:** no unconditional prime-gap bound of size O(√p) is known (best ~ x^{0.525}, Baker–Harman–Pintz 2001).
- **Known:** Andrica (1986); implies/related to Legendre and Oppermann; verified to ~10^18.
- **Missing (the object that does not exist as a proof):** an unconditional proof that g_n < 2√p_n + 1 for every n (no unconditional proof for all n; finite certificate verified to 10^7 only).
- **Falsifier:** an n with √p_{n+1} − √p_n ≥ 1.

## G17 - Oppermann's conjecture
- **Tier:** B (external open)
- **Subject:** Oppermann's conjecture (a prime in n²..n(n+1) and in n(n+1)..(n+1)²)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/gap_prime_gaps_certificate.py
- **Pin:** test_oppermann_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** for every n >= 2, a prime strictly between n² and n(n+1), and a prime strictly between n(n+1) and (n+1)²; this implies Legendre (G14).
- **Barrier:** needs a prime-gap bound of size O(√x); no unconditional bound this small is known (best ~ x^{0.525}, Baker–Harman–Pintz 2001).
- **Known:** Oppermann (1882); implies Legendre; verified numerically to large n.
- **Missing (the object that does not exist as a proof):** an unconditional proof that each interval (n², n(n+1)) and (n(n+1), (n+1)²) contains a prime for every n >= 2 (no unconditional proof for all n; finite certificate verified only for (n+1)² <= 10^7).
- **Falsifier:** an n >= 2 with no prime strictly between n² and n(n+1), or none strictly between n(n+1) and (n+1)².

## G18 - Gilbreath's conjecture
- **Tier:** B (external open)
- **Subject:** Gilbreath's conjecture (leading term of each iterated difference row of the primes is 1)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/gap_prime_gaps_certificate.py
- **Pin:** test_gilbreath_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** controlled by the sign pattern of consecutive prime gaps; verified numerically to great depth, no proof.
- **Barrier:** equivalent to a strong regularity of prime gaps far beyond current unconditional means.
- **Known:** Gilbreath (1958); Killgrove-Ralston and later computations to deep rows.
- **Missing (the object that does not exist as a proof):** a proof that the leading entry of every iterated absolute-difference row of the prime sequence is 1 for all rows (no unconditional proof; finite certificate verified only to 2000 rows).
- **Falsifier:** a row whose leading entry is not 1.

## G19 - Polignac's conjecture
- **Tier:** B (external open)
- **Subject:** Polignac's conjecture (every even gap occurs infinitely often among primes)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/gap_prime_gaps_certificate.py
- **Pin:** test_polignac_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** the case k=2 is the twin prime conjecture (G13); general even k needs a parity-crossing method; Zhang/Maynard-Tao give some bounded even gap, not all.
- **Barrier:** parity barrier of sieve methods; no method yields infinitude for a prescribed even gap.
- **Known:** Polignac (1849); Zhang (2013), Maynard-Tao (2014) (some bounded gap); exhaustive existence checks for every even k to large bounds.
- **Missing (the object that does not exist as a proof):** a proof that for every even k there are infinitely many prime pairs (p, p+k) (no unconditional proof; finite existence certificate only for even k <= 100).
- **Falsifier:** an even k with only finitely many prime pairs at distance k.

## G20 - Sophie Germain primes
- **Tier:** B (external open)
- **Subject:** Sophie Germain primes (infinitely many primes p with 2p+1 prime)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/gap_prime_gaps_certificate.py
- **Pin:** test_sophie_germain_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** infinitude of safe primes is open; a special case of the Hardy-Littlewood k-tuples heuristics; finite count only.
- **Barrier:** parity barrier; no sieve method distinguishes the pair structure (p, 2p+1).
- **Known:** Sophie Germain (18th c.); Hardy-Littlewood k-tuples heuristics; exhaustive counts (e.g. 4324 below 10^6).
- **Missing (the object that does not exist as a proof):** a proof that infinitely many primes p have 2p+1 prime (no unconditional proof; finite count certificate only).
- **Falsifier:** a proof that only finitely many such p exist.

## G21 - "Every 0/0 resolves" is false (no-go)
- **Tier:** A (register debt)
- **Subject:** the register's removable-value schema (C15) without its existence hypothesis
- **Status:** RESEARCHED
- **Related cards:** C15
- **Proof attempt:** no-go - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/RemovableValue.lean
- **Pin:** test_zero_over_zero_need_not_resolve
- **as_of:** 2026-10-18
- **Reduction:** C15's uniqueness of the removable value is conditional on *existence* of the punctured limit (Hausdorff target). Dropping that hypothesis yields a false claim.
- **Barrier:** existence of the limit is object-specific; no general schema can supply it (C15's own caveat).
- **Known:** uniqueness of limits in Hausdorff spaces; standard counterexample xy/(x\u00b2+y\u00b2).
- **Missing (the object that does not exist as a proof):** a proof that an arbitrary 0/0 has a removable value -- impossible in general; the register must supply the limit per object (as its experimental programs do).
- **Falsifier:** the classic 0/0 xy/(x\u00b2+y\u00b2) at the origin has distinct ray limits (0, 1/2, 2/5, ...), so no removable value exists.

## G22 - Euler polynomial: "n²+n+41 is prime for all n" is false (no-go)
- **Tier:** B (external)
- **Subject:** naive claim "n²+n+41 is prime for all n >= 0" (Euler's polynomial)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** no-go - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/gap_prime_gaps_certificate.py
- **Pin:** test_euler_polynomial_no_go
- **as_of:** 2026-10-18
- **Reduction:** the polynomial is prime for n = 0..39 (a long initial run) but fails at n = 40 (1681 = 41²); the naive universal claim is false, not open.
- **Barrier:** none (refuted); recorded so the long initial run is not mistaken for evidence of a universal statement.
- **Known:** Euler (1772); 40²+40+41 = 1681 = 41².
- **Missing (the object that does not exist as a proof):** a proof of the (false) universal claim -- impossible; this row records the refutation.
- **Falsifier:** n = 40 gives 1681 = 41², composite.

## G23 - Fermat primes (no-go for finiteness, open for infinitude)
- **Tier:** B (external open)
- **Subject:** Fermat primes (F_k = 2^(2^k)+1); infinitude is OPEN
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/gap_prime_gaps_certificate.py
- **Pin:** test_fermat_numbers_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** only F_0..F_4 are known Fermat primes; F_5 = 4294967297 = 641 · 6700417 is composite; whether infinitely many Fermat primes exist is OPEN.
- **Barrier:** Fermat numbers grow doubly exponentially; no method shows infinitude (nor finiteness) of the prime ones.
- **Known:** Fermat (1640); Euler (F_5 composite, 1732); modern distributed searches (no Fermat prime beyond F_4 found).
- **Missing (the object that does not exist as a proof):** a proof that infinitely many F_k are prime, or that only finitely many are (no unconditional result; finite certificate only for F_0..F_4).
- **Falsifier:** a proof that only finitely many Fermat numbers are prime, or an infinitude proof.

## G24 - Landau's problem (primes of the form n²+1)
- **Tier:** B (external open)
- **Subject:** Landau's fourth problem (infinitely many primes of the form n²+1)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/gap_prime_gaps_certificate.py
- **Pin:** test_landau_n2_plus_1_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** no proof that n²+1 is prime infinitely often; related to Bunyakovsky and Hardy-Littlewood k-tuples; finite count only.
- **Barrier:** parity barrier; no sieve method produces a prescribed irreducible-polynomial prime pattern.
- **Known:** Landau (1912); Hardy-Littlewood; exhaustive counts (112 such n <= 1000, 316 for n <= 3162).
- **Missing (the object that does not exist as a proof):** a proof that infinitely many n have n²+1 prime (no unconditional proof; finite count certificate only).
- **Falsifier:** a proof that only finitely many n²+1 are prime.

## G25 - Ternary Goldbach (Helfgott): cited, not formalized (citation-only)
- **Tier:** B (external, relied upon)
- **Subject:** ternary Goldbach (every odd >= 7 is a sum of three primes) -- cited, not formalized in-repo
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** citation-only - 05_Documentation_and_Research_Specifications/05_Complete_Framework_Documentation/THE_GAP_LEDGER.md
- **Pin:** test_ternary_goldbach_citation_recorded
- **as_of:** 2026-10-18
- **Reduction:** the register (G9) invokes ternary Goldbach; the theorem is Helfgott (2013/2014), established externally, cited here but not formalized.
- **Barrier:** formalization debt only, not a mathematical gap -- the theorem is proved.
- **Known:** Vinogradov (1937, large odd); Helfgott (2013/2014, all odd >= 7).
- **Missing (the object that does not exist as a proof):** a self-contained Lean formalization of the cited theorem in this repository (the result itself is established externally).
- **Falsifier:** an odd n >= 7 not representable as a sum of three primes.
