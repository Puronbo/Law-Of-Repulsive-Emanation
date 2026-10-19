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
- **Pin:** test_ns_wall_markers_pinned
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
- **Pin:** test_information_phi_markers_pinned
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
- **Known:** `OrientationBoundedness.lean` (`boundedOrientation`, `boundedOrientationScale`); the one-parameter scale family `boundedOrientationScale c` satisfies the composition law for every real `c`, so uniqueness is refuted; register cards C11/C12 record the margin.
- **Missing (the object that does not exist as a proof):** an **additional selection axiom** (with a physical/mathematical justification) that picks a canonical `c`, or a proof that all `c` are equivalent for all claims. The ledger requires either a canonical choice with justification, or a no-go proof.
- **Falsifier:** show no such selection is compatible with the register's claims, or derive contradiction from a proposed selection axiom.

## G6 — BSD (rank >= 2)
- **Tier:** B (Millennium scope)
- **Subject:** Birch–Swinnerton-Dyer
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** partial - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/BSD.lean
- **Pin:** test_ledger_artifacts_attach_no_sorry
- **Pin:** test_bsd_rank_records_pinned
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
- **Pin:** test_hodge_quintic_open_marker_pinned
- **as_of:** 2026-10-18
- **Reduction:** codim 1 is the Lefschetz (1,1) theorem (proved: Hodge classes are divisor classes). Codim >= 2 open in general; the degree-m middle cohomology of a 2m-fold is the only nontrivial part of a hypersurface. Canonical hard case: Hdg^2(quintic threefold). Rational Hodge conjecture now known for very general abelian four- and fivefolds (Markman, arXiv 2024/2025); the integral Hodge conjecture provably fails for very general principally polarized abelian varieties of dim >= 4 (Engel-de Gaay Fortman-Schreieder, arXiv:2507.15704, 2025), so the rational and integral statements diverge.
- **Barrier:** no general geometric construction produces algebraic cycles representing arbitrary (2,1) Hodge classes; only special classes are reachable (Lefschetz divisors, generated-in-degree-one abelian varieties, cubic fourfolds). Mumford (1969) shows Hdg^2 need not be generated by divisor products, so degree-one generation is unavailable in general.
- **Known:** Lefschetz (1,1) (1924); Clemens-Griffiths (1972, cubic threefold not rational); Zucker (1977, Hodge conjecture for cubic fourfolds); Murty (1979); Moonen-Zarhin (dim < 5: degree-one generation or CM by an imaginary quadratic field); Markman (2024/2025, abelian four- and fivefolds); Engel-de Gaay Fortman-Schreieder (2025, integral Hodge conjecture false for ppav dim >= 4).
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
- **Reduction:** RH is equivalent to Lambda <= 0 for the de Bruijn-Newman constant; the complementary bound Lambda >= 0 was proved by Rodgers-Tao (2018/2020), so RH is now exactly the statement Lambda = 0, with the best rigorous bracket 0 <= Lambda <= 0.2. Also equivalent to Li's criterion and to Weil positivity (Connes-Consani). RH verified for the first 10^13 nontrivial zeros (Gourdon-Demichel 2004); the function-field analogue is proved (Weil 1948).
- **Barrier:** no unconditional proof that Re(rho)=1/2 for all zeros; the equivalences (Li, Weil positivity, de Bruijn-Newman) restate RH without supplying the needed positivity/zero-free region, and the de Bruijn-Newman route leaves only the interval 0 <= Lambda <= 0.2.
- **Known:** Riemann (1859); Hardy (1914, infinitely many zeros on the line); Weil (1948, function fields); Montgomery (1973, pair correlation); Odlyzko; Conrey (1989, >2/5, refined to >41.7% by Pratt-Robles-Zaharescu–Zeindler 2020); Gourdon-Demichel (2004, first 10^13 zeros); Rodgers–Tao (2018/2020, Newman's conjecture Lambda >= 0); Polymath15 (2019, Lambda <= 0.22); Platt-Trudgian (2021, Lambda <= 0.2); Connes-Consani (Weil positivity).
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
- **Reduction:** non-uniform route: P != NP would follow from any NP language lacking polynomial-size circuits. Three barriers block the standard techniques: relativization (Baker-Gill-Solovay 1975), natural proofs (Razborov-Rudich 1997), algebrization (Aaronson-Wigderson 2008). Williams (2011) broke relativization/natural-proofs with an algorithmic method (NEXP not in ACC^0). Meta-complexity (MCSP) is now the main program: hardness of MCSP is equivalent-in-spirit to circuit lower bounds (Kabanets-Cai; Hirahara 2022).
- **Barrier:** no super-polynomial (indeed no fixed-polynomial) circuit lower bound is known for any explicit NP function; not even NE vs formulas (NEXP vs NC_1) is settled. Magnification and localization barriers further constrain current methods.
- **Known:** Baker-Gill-Solovay (1975); Razborov-Rudich (1997); Aaronson-Wigderson (2008); Williams (2011, NEXP not in ACC^0; Godel Prize 2024); Murray-Williams (2017, MCSP not NP-hard under local reductions); Hirahara (2022, NP-hardness of meta-complexity via information-theoretic cryptography).
- **Missing (the object that does not exist as a proof):** a non-relativizing, non-algebraizing, non-natural lower-bound method that yields a super-polynomial (or exponential) circuit lower bound for some explicit function in NP, or a constructive proof P=NP.
- **Falsifier:** a relativized world where the claimed method fails, or the claimed lower-bound proof collapsing under algebraization/natural-proofs tests, or an explicit polynomial circuit for an NP-complete function.

## G11 — Yang–Mills mass gap
- **Tier:** B (Millennium scope)
- **Subject:** Yang–Mills existence & mass gap
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** partial - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/MassGap.lean
- **Pin:** test_ledger_artifacts_attach_no_sorry
- **Pin:** test_massgap_crossover_pinned
- **as_of:** 2026-10-18
- **Reduction:** existence is rigorously established only in low dimension / finite volume: 2D Yang-Mills measure on compact surfaces (Driver, Sengupta, Levy); 3D finite-volume via stochastic quantization (Chandra-Chevyrev-Hairer-Shen, 2022); finite-volume 4D with infrared cutoff (Magnen-Rivasseau-Seneor 1993; Balaban's RG program). The 4D mass gap is proved only in the strong-coupling lattice regime, not in the continuum. General spectral-gap decidability is itself undecidable (Cubitt-Perez-Garcia-Wolf, 2015), so only theory-specific structure can close it.
- **Barrier:** no rigorous 4D continuum limit of nonabelian lattice gauge theory satisfying the Osterwalder-Schrader axioms, together with a uniform positive lower bound on the mass gap along the continuum/renormalization trajectory; the Clay problem is explicitly open (Jaffe-Witten 2000). Numerous 2024-2025 preprints claim full proofs (e.g. arXiv:2506.00284; Agawa; Nye; Lim) but none is peer-reviewed or accepted, so none counts here.
- **Known:** Wilson lattice gauge theory (1974); Balaban renormalization-group program; Magnen-Rivasseau-Seneor (1993); Glimm-Jaffe constructive QFT; asymptotic freedom (Gross-Wilczek, Politzer 1973); Chandra-Chevyrev-Hairer-Shen (3D existence, 2022); strong-coupling finite-lattice mass gap.
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

## G26 - Prime k-tuples (Dickson-type constellations)
- **Tier:** B (external open)
- **Subject:** prime k-tuples / Dickson's conjecture (every admissible pattern occurs infinitely often)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/gap_prime_gaps_certificate.py
- **Pin:** test_prime_constellations_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** a single admissible pattern (twin, triplet, quadruplet, quintuplet, sextuplet) is realized finitely often; the infinitude claim is Dickson's conjecture, subsuming the twin prime (G13), Polignac k=2 (G19) and Sophie Germain (G20) cases.
- **Barrier:** parity barrier of sieve methods; no method yields infinitude for a prescribed admissible pattern (Zhang/Maynard-Tao give only some bounded gap).
- **Known:** Dickson (1904); Hardy-Littlewood k-tuples heuristics; Maynard-Tao (2014) bounded gaps; smallest constellations (twin 3,5; quadruplet 5,7,11,13; quintuplet 5,7,11,13,17; sextuplet 7,11,13,17,19,23).
- **Missing (the object that does not exist as a proof):** a proof that every admissible k-tuple pattern is realized by infinitely many prime translates (no unconditional proof; finite existence certificate gives one occurrence per pattern only).
- **Falsifier:** an admissible pattern occurring only finitely often.

## G27 - Odd perfect numbers (none known)
- **Tier:** B (external open)
- **Subject:** odd perfect numbers (does any odd n with sigma(n) = 2n exist?)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/perfect_numbers_certificate.py
- **Pin:** test_odd_perfect_numbers_no_small_certificate
- **as_of:** 2026-10-18
- **Reduction:** even perfect numbers are exactly 2^(p-1)(2^p-1) with 2^p-1 prime (Euclid-Euler); the odd case is open. Euler's necessary form: an odd perfect number is q^a m^2 with q prime, q = a = 1 (mod 4).
- **Barrier:** no method shows existence or non-existence of an odd perfect number; only necessary conditions and lower bounds are known.
- **Known:** Euclid-Euler (even case); Euler (odd form, 18th c.); Ochem-Rao (2012, lower bound > 10^1500); Nielsen (2015, at least 101 prime factors counted with multiplicity).
- **Missing (the object that does not exist as a proof):** a proof that no odd n satisfies sigma(n) = 2n (or an explicit example) -- no unconditional result; finite certificate only that none exists up to the search limit.
- **Falsifier:** an odd n with sigma(n) = 2n, or a proof that only even perfect numbers exist.

## G28 - Gap Ledger row forge (register tooling)
- **Tier:** A (register debt)
- **Subject:** the register's own row-forge tooling (drafting and validating ledger entries)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/gap_row_forge.py
- **Pin:** test_gap_row_forge_emits_gate_valid_rows
- **Pin:** test_gap_row_forge_applies_end_to_end
- **as_of:** 2026-10-18
- **Reduction:** drafting a row is decidable: assign the next G-number, require a legal proof-attempt kind, a git-tracked artifact path, and a live pin, then reject anything Gate D would reject; `apply` additionally scaffolds the artifact and a deliberately-failing pin and appends the row.
- **Barrier:** none for the shape (decidable); the forge cannot supply the mathematical content (Reduction/Barrier/Known/Missing/Falsifier) nor prove any subject.
- **Known:** the live ledger (every G-row in this file); Gate D in test_gap_ledger.py; the forge's own self-test.
- **Missing (the object that does not exist as a proof):** an automatic prover that fills a row's mathematical fields and closes the gap; the forge only guarantees the shape is honest and machine-checkable.
- **Falsifier:** a forge output that Gate D accepts but which claims resolution, or a legal-looking row emitted with an illegal kind, a missing artifact, or a fake pin.

## G29 - Mersenne primes
- **Tier:** B (external open)
- **Subject:** Mersenne primes (infinitely many primes of the form 2^p - 1?)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/perfect_numbers_certificate.py
- **Pin:** test_mersenne_primes_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** 2^p - 1 can be prime only if p is prime; for prime p the exact Lucas-Lehmer test decides M_p. Mersenne primes correspond bijectively to even perfect numbers (Euclid-Euler), so this row underwrites the even side of G27.
- **Barrier:** no proof of infinitude (or finiteness); Lenstra-Pomerance-Wagstaff heuristics suggest infinitely many, but no unconditional method yields it.
- **Known:** Euclid-Euler (even perfect numbers); Lucas (1876) / Lehmer (1930s) test; 52 Mersenne primes known as of 2025; largest 2^136279841 - 1 (GIMPS / Luke Durant, Oct 2024); all exponents below 136,279,841 tested at least once (2025).
- **Missing (the object that does not exist as a proof):** a proof that infinitely many (or only finitely many) M_p are prime -- no unconditional result; finite Lucas-Lehmer certificate only for exponents up to pmax.
- **Falsifier:** a proof that only finitely many M_p are prime, or an infinitude proof.

## G30 - Giuga's conjecture (Giuga-and-Carmichael criterion)
- **Tier:** B
- **Subject:** Giuga's conjecture (Giuga-and-Carmichael criterion)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/giuga_certificate.py
- **Pin:** test_giuga_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** drafting the certificate is decidable: enumerate the Giuga numbers (composite n with p | (n/p - 1) for every prime p | n, i.e. sum_{k=1}^{n-1} k^{phi(n)} = -1 (mod n)) below a bound, then test each with Korselt's criterion; a Giuga number that is also Carmichael is exactly a counterexample to Giuga's conjecture, and none occurs below the bound.
- **Barrier:** the search is finite while the conjecture is universal; no known structure rules out a counterexample, which would have to be simultaneously squarefree, Korselt-compliant (Carmichael) and satisfy the far stronger p^2(p-1) | (n - p) condition for every prime p | n.
- **Known:** Giuga numbers 30, 858, 1722, 66198, 2214408306, ... (twelve known explicitly, the list complete through the 12th term; a 13th enormous candidate is listed but not certified, OEIS A007850); all known Giuga numbers are even and it is unknown whether infinitely many exist or whether any odd one exists; every counterexample to Giuga's conjecture must have at least 19908 decimal digits (Borwein-Maitland-Skerritt, INTEGERS 13 (2013)); Alford-Granville-Pomerance (1994) proved there are infinitely many Carmichael numbers, and Luca-Pomerance-Shparlinski bound the Giuga count by O(X^{1/2} (log X)^2).
- **Missing (the object that does not exist as a proof):** an unconditional proof that no composite n is both a Giuga number and a Carmichael number (equivalently that sum_{k=1}^{n-1} k^{n-1} != -1 (mod n) for every composite n); also nothing settles the infinitude of Giuga numbers or the existence of an odd Giuga number.
- **Falsifier:** a single composite n with p^2 (p-1) | (n - p) for every prime p | n (i.e. both Giuga and Carmichael) would refute Giuga's conjecture; a Giuga number <= 10^5 that is also Carmichael would refute the finite certificate's claim.

## G31 - Lehmer's totient problem (phi(n) divides n-1)
- **Tier:** B
- **Subject:** Lehmer's totient problem (phi(n) divides n-1)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/lehmer_totient_certificate.py
- **Pin:** test_lehmer_totient_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** reading the conjecture is decidable on a finite range: compute phi(n) by sieve and test (n - 1) mod phi(n) = 0 for every composite n <= bound; no n passes. The relaxation phi(n) | (n - 1)^2 (2-Lehmer numbers) is checked the same way and does have solutions, confirming the two conditions are genuinely different.
- **Barrier:** the test is finite while the conjecture quantifies over all composites; a counterexample must be simultaneously odd, squarefree and Carmichael, so it is invisible to any search below the known lower bound n > 10^26 with >= 15 distinct prime factors.
- **Known:** no composite n with phi(n) | (n - 1) is known; any such n is odd, squarefree and Carmichael (Lehmer 1932); omega(n) >= 14 (Cohen-Hagis 1980), improved to omega(n) >= 15, n > 10^26 (Renze; Pinch reports n > 10^30); if 3 | n then omega(n) >= 4x10^7 and n > 10^(3.6x10^8) (Burcsi-Czirbusz-Farkas 2011); counting bounds N(L,x) = O(x^{1/2} log^{3/4} x) (Pomerance 1977) and <= x^{1/2} / log^{1/2+o(1)} x (Luca-Pomerance 2019); the 2-Lehmer relaxation phi(n) | (n - 1)^2 does have solutions, e.g. 561, 1105, 1729, 2465, 6601, 8481 below 10^4 (OEIS A173703) -- the first five are Carmichael but 8481 = 3.11.257 is not, so 2-Lehmer is strictly weaker than the Lehmer condition.
- **Missing (the object that does not exist as a proof):** an unconditional proof that no composite n satisfies phi(n) | (n - 1); equivalently a proof that the Lehmer set L is empty, or a single explicit member.
- **Falsifier:** one composite n with phi(n) | (n - 1) (necessarily odd, squarefree, Carmichael, > 10^26) refutes the conjecture; a composite n <= 10^6 with phi(n) | (n - 1) would refute this finite certificate.

## G32 - Wieferich primes (2^(p-1) = 1 mod p^2)
- **Tier:** B
- **Subject:** Wieferich primes (2^(p-1) = 1 mod p^2)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/wieferich_certificate.py, 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/Wieferich.lean
- **Pin:** test_wieferich_primes_is_a_finite_certificate
- **Pin:** test_wieferich_primes_are_machine_checked
- **as_of:** 2026-10-19
- **Reduction:** membership is decidable per prime: sieve the primes and test pow(2, p - 1, p^2) == 1, recording the Fermat quotient; this decides the finite set of Wieferich primes below any bound and exhibits their Fermat quotients. The two known instances are additionally *machine-checked*: `Wieferich.lean` proves `IsWieferich 1093` and `IsWieferich 3511` by kernel `decide` (axiom-free), and proves the structural restatements `Wieferich p ↔ p^2 | 2^(p-1) - 1 ↔ p | (2^(p-1) - 1)/p` (the Fermat quotient's second-order zero). Reduction is finite (the range) plus exact (the instances).
- **Barrier:** deciding which primes are Wieferich below a bound says nothing about how many there are; the heuristic (Crandall-Dilcher-Pomerance) that A(p) = (2^(p-1) - 1)/p mod p behaves randomly predicts ~ log log x Wieferich primes up to x, i.e. infinitely many, with an infinite expected gap to the next one, so no finite search can evidence infinitude. Machine-checking the two instances only certifies them, not the count.
- **Known:** only 1093 (Meissner 1913) and 3511 (Beeger 1922) are known; no others below 6.7x10^15 (Dorais-Klyve 2011), since extended beyond 1.45x10^17 (OEIS A001220); Wieferich 1909 linked them to the first case of Fermat's Last Theorem; Silverman 1988 proved finitely many follow from the abc conjecture; base-3 (Mirimanoff) primes are 11 and 1006003. In `Wieferich.lean`: `prime_1093`, `prime_3511`, `wieferich_1093`, `wieferich_3511`, `fermat_dvd`, `isWieferich_iff_sq_dvd`, `isWieferich_iff_quotient_dvd`, `quotient_1093_dvd`, `quotient_3511_dvd` (register `wieferichFacts`, ten entries).
- **Missing (the object that does not exist as a proof):** an unconditional proof that infinitely many Wieferich primes exist (equivalently a proof that the random-Fermat-quotient heuristic holds without the abc conjecture); also no proof that infinitely many non-Wieferich primes exist. The instances can be certified but the arithmetic crease's *frequency* cannot be counted.
- **Falsifier:** infinitely many primes p with 2^(p-1) not = 1 (mod p^2) beyond a point would refute infinitude of Wieferich primes; a Wieferich prime below 10^6 other than 1093 or 3511 would refute the finite certificate; a Lean-accepted `IsWieferich p` whose `p` failed the modular identity would refute `Wieferich.lean`.

## G33 - Beal's conjecture (a^x+b^y=c^z with x,y,z>2, gcd=1 => none?)
- **Tier:** B
- **Subject:** Beal's conjecture (a^x+b^y=c^z with x,y,z>2, gcd=1 => none?)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/beal_certificate.py
- **Pin:** test_beal_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** for each triple (a^x, b^y, c^z) with x,y,z > 2, test equality and check gcd(a,b,c); the search is exact up to the chosen bound. Absence in a window is finite evidence only.
- **Barrier:** no known proof method extends a finite window to all positive integers (Beal is open); the Darmon-Granville theorem gives finiteness for fixed exponents satisfying 1/x+1/y+1/z < 1 but Beal allows all x,y,z > 2 and no fixed sum constraint except the equation.
- **Known:** Beal (1993), AMS $1,000,000 prize; Wiles (FLT); Darmon-Granville (finiteness for fixed exponents); Poonen-Schaefer-Stoll, Bruin, Zureick-Brown resolved specific (x,y,z) families; large computational searches (Norvig, Vanderkam, Beal team) found no coprime counterexamples in wide windows.
- **Missing (the object that does not exist as a proof):** a proof that there are no positive integers a,b,c,x,y,z>2 with gcd(a,b,c)=1 and a^x+b^y=c^z, or a single explicit counterexample meeting those conditions.
- **Falsifier:** any coprime (a,b,c,x,y,z>2) with a^x+b^y=c^z refutes Beal's conjecture; such a triple in the window searched would refute this certificate.

## G34 - Erd\u0151s-Moser equation (power sum = square of triangular number)
- **Tier:** B
- **Subject:** Erd\u0151s-Moser equation (power sum = square of triangular number)
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** certificate - 02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/erdos_moser_certificate.py
- **Pin:** test_erdos_moser_is_a_finite_certificate
- **as_of:** 2026-10-18
- **Reduction:** for each (m,k) with 1 < m <= max_m, 1 <= k <= max_k, test sum_{j < m} j^k == m^k; the only known solution is (3,1). Absence in a finite window is not a proof of the conjecture.
- **Barrier:** any further solution requires k even, satisfies strong p-adic/divisibility conditions, and is known to have m > 10^10^6 (bounds have improved further), so no feasible finite search can exclude all solutions (the conjecture is open).
- **Known:** Erdős (conjectured no other solutions); Moser (1953) gave necessary conditions and m > 10^10^6; Gallot-Moree-Zudilin (2010) improved to m > 10^10^9; Kellner/Moree gave further conditions.
- **Missing (the object that does not exist as a proof):** a proof that sum_{j < m} j^k = m^k has no integer solutions with (m,k) != (3,1), or an explicit counterexample.
- **Falsifier:** a pair (m,k) with (m,k) != (3,1) and sum_{j < m} j^k == m^k would refute Erdős–Moser; such a pair in the window would refute this certificate.

## G35 - The crease: the cusp normal form of every fold (brain folds)
- **Tier:** A (formal core)
- **Subject:** the local normal form of every generic crease (the cusp) and its reading as a brain/cortical fold
- **Status:** RESEARCHED
- **Related cards:** []
- **Proof attempt:** partial - 01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/Crease.lean
- **Pin:** test_crease_module_is_a_partial_formalization
- **as_of:** 2026-10-19
- **Reduction:** the local mathematics of a fold is decidable in exact real algebra and is machine-checked in `Crease.lean`: a crease is a zero of the fold derivative `3x^2 - a` (`deriv_fold_zero_iff`), the crease count follows from `x^2 = a/3` -- none for `a < 0` (`no_crease_of_neg`), a single degenerate crease `x = 0` at `a = 0` (`crease_zero_iff`) and exactly two `+/- sqrt(a/3)` for `a > 0` (`crease_sqrt`, `crease_neg_sqrt`, `crease_eq_sqrt_or`) -- and the cusp potential `V a b x = x^4/4 - a x^2/2 - b x` has that fold germ as gradient (`deriv_cusp`), its crease a double root `(x-r)^2 (x+2r)` on the cusp curve with vanishing discriminant `4a^3 = 27b^2` (`cusp_curve_factor`, `cusp_discriminant`); the logistic apex `x = 1/2` is a crease (`deriv_logistic_half`). The brain reading (cortical gyri/sulci as these creases, with universal scaling) is empirical and recorded in BRAIN_CREASE.md.
- **Barrier:** the reduction is strictly local: it proves that *if* a fold is generic its crease is a cusp, but it does not derive any particular crease pattern (a cortex, a crumpled sheet, a trained network's decision boundary) from a stated physical energy, and it does not fix the folding exponent; the global scaling law (Mota-Herculano-Houzel, predicted exponent 1.25, observed ~1.305) is an empirical/modelling result, not a theorem of this repository.
- **Known:** Thom's catastrophe-theory normal forms (the fold `x^2` and cusp `x^3` as the local models of generic creases); Richman-Stewart (1988) differential-growth buckling model of cortical convolution; Mota-Herculano-Houzel (Science 2015) universal cortical-folding scaling and Wang et al. (PNAS 2016) human universality across >1000 MRIs (invariant to sex, shifted by age, perturbed in Alzheimer's); the neuron-level adaptations associated with human cortical expansion (Galakhova et al. 2022; Namba-Huttner 2024); formalised facts in `Crease.lean` (`creaseFacts`, twelve entries).
- **Missing (the object that does not exist as a proof):** a derivation of any specific crease pattern (cortical gyri/sulci, a crumpled sheet, a neural-network decision boundary) from a stated physical energy, with its exponent proved, and any bridge from this local cusp algebra to the open global folding law -- the object that does not exist as a proof is that energy-minimisation theorem.
- **Falsifier:** a generic fold whose crease is not locally a cusp (a crease with no double-root collision, i.e. the local model fails), or a physical crease pattern whose measured folding exponent provably contradicts its stated energy model.
