# KNOWN-STUDIES GROUNDING CROSSWALK

*Status: map / linkage. No external result is claimed as ours; no Millennium
problem is settled here. See `WHAT_THIS_DOES_NOT_PROVE.md` and
`EXPLICIT_CLAIMS.md`.*

*Every citation below was checked against a publisher page, an arXiv abstract,
or a lecture-note PDF (last enrichment pass: 2026-10-16). ArXiv IDs and DOIs are
given so a reader can re-verify each link.*

---

## Purpose

The register (`EXPLICIT_CLAIMS.md`, cards C1–C38; `VERIFICATION_LEDGER.md`) is
self-contained: each card pairs a Lean theorem half with a numeric certificate
half. This document is the **outward** half of the same honesty contract. It
anchors each of the framework's mechanisms to **named, checkable studies** in the
literature *and* to **our own certified artifacts** at the same time, so a reader
can move in either direction:

* from a classical result to the repository object that is a form of it, or
* from a repository object to the classical result it echoes.

Every *Known studies* cell is a **link**, never an import; every *Ours* cell is
**something the repository actually proves or runs**. The gate
`test_grounding_crosswalk.py` pins these links (files exist, modules exist,
anchors present) so the map cannot drift from the tree.

### How to read a block

* **Ours** — the repository artifacts (docs, Lean modules, numeric certificates).
* **Known studies** — named results/works the mechanism is a form of.
* **Shared content** — the exact statement the two sides actually share.
* **Honest boundary** — what the link does **not** carry.
* **Sources** — the concrete reference(s) with an identifier (arXiv ID, DOI,
  journal, or URL) for the citations introduced or sharpened in that block.

---

## M1. The 0/0 removable-value law

* **Ours** — `THE_LAW_OF_SINGULARITIES.md`; `REMOVABLE_SINGULARITIES.md`; Lean
  `PunoCalculus/RemovableValue.lean` (`IsRemovableValue`,
  `removable_value_unique`, `existsUnique_iff_exists_and_unique`),
  `PunoCalculus/RemovableComplexBridge.lean` (the Riemann schema).
* **Known studies** — the removable-singularity theorem of **Riemann** (1851);
  the bounded-entire collapse of **Liouville** (`PunoCalculus/LiouvilleBridge.lean`);
  the classical indeterminate-form
  limits and **L'Hôpital**'s rule; the categorical initial/terminal/zero object of
  **Mac Lane**.
* **Shared content** — an indeterminate `0/0` whose surrounding structure forces
  a *unique* finite value: exactly "a removable singularity has a unique
  extension value". Riemann's theorem is a four-way equivalence — boundedness
  near the point, continuous extendability, holomorphic extendability, and
  `lim (z-a)f(z) = 0` — with the extension unique by the identity theorem; the
  canonical example is `sinc(z) = sin(z)/z` filled in by `sinc(0) := 1`, i.e. a
  literal `0/0` whose value the structure forces.
* **Honest boundary** — this is the *general form*; the analytic hypotheses
  (continuity, holomorphy) that make a specific `0/0` removable are the classical
  theorems, cited, not re-proved.
* **Sources** — Riemann's theorem on removable singularities, standard statement
  and proof (e.g. lecture notes, Univ. of Toronto MAT334H1; Saracco, *Holomorphic
  functions in one complex variable*, SNS Pisa, Thm. 2.4);
  en.wikipedia.org/wiki/Removable_singularity (TFAE list and the `sinc` example).

---

## M2. The five 0/0 mechanisms

* **Ours** — `PunoCalculus/ZeroProbe.lean` (C19), `VanishOrder.lean` /
  `ZeroValuation.lean` (C18/C20), `ZeroIndex.lean` (C21),
  `NoetherDiscrete.lean` / `UniverseGrowth.lean` (C36/C37),
  `CriticalAmplitude.lean` (C38); numeric halves
  `zero_mechanism_certificates.py`, `arithmetic_shadow_certificates.py`.
* **Known studies** — root **index** / multiplicity; algebraic **valuations**
  (order of vanishing, `v(xy)=v(x)+v(y)`); discrete conservation laws
  (**Noether**, 1918); critical scaling relations of statistical mechanics —
  **Widom** (1965), **Rushbrooke** (1963), **Josephson** (1967), **Fisher**
  (1968), **Wilson** renormalization (1971).
* **Shared content** — each mechanism is the arithmetic skeleton of a classical
  construction: Probe ⇒ removable value; Vanishing-Rate ⇒ valuation; Index ⇒
  additive multiplicity; Conservation ⇒ momentum/charge balance; Critical
  Phenomenon ⇒ Widom/Rushbrooke/Josephson/Fisher exponent identities. The scaling
  hypothesis of Widom/Kadanoff/Fisher makes the exponent identities
  consequences of one homogeneity assumption, and Wilson's renormalization group
  explains *why* they hold: the critical point is a fixed point of a
  scale transformation.
* **Honest boundary** — each is instantiated on finite models / finite
  enumeration; no phase transition is proved critical, no field theory is
  constructed.
* **Sources** — H. E. **Stanley**, *Scaling, universality, and renormalization:
  Three pillars of modern critical phenomena*, Rev. Mod. Phys. 71, S358 (1999)
  (cps-www.bu.edu/hes/articles/s99a.pdf); A. **Pelissetto** & E. **Vicari**,
  *Critical Phenomena and Renormalization-Group Theory*, Phys. Rept. 368 (2002)
  549–727, arXiv:cond-mat/0012164, DOI 10.1016/S0370-1573(02)00219-3;
  B. **Simons**, Cambridge TCM scaling lecture notes
  (tcm.phy.cam.ac.uk/~bds10/phase/scaling.pdf) for the named identities
  (Rushbrooke `α+2β+γ=2`, Widom `δ−1=γ/β`, Josephson `2−α=dν`,
  Fisher `γ=(2−η)ν`).

---

## M3. The folding mechanism

* **Ours** — `THE_BOOK_OF_PUNO.md` and `Folding_Calculus_Paper.md` (fold =
  differentiation, unfold = the antiderivative; **crease density** as a
  diagnostic); `PunoCalculus/Curvature.lean`.
* **Known studies** — the **fold-and-cut** theorem (**Demaine**, Demaine & Lubiw,
  1998); isometric folding of Riemannian manifolds (**Robertson**, 1977);
  **Kawasaki**'s flat-foldability condition; ReLU networks as folded
  piecewise-linear maps (**Keup** & Helias, 2022; **Telgarsky**, 2016); the
  space-folding measure (**Lewandowski** et al., TMLR 2025 / AAAI 2026);
  FoldAndCutNetworks (**Stewart**, Layton, Bennett & Driggs, 2025).
* **Shared content** — a piecewise-smooth object is the *unfolding* of its
  creases; differentiation folds, and the crease set is the singular locus; a
  ReLU network is a layered fold. Two of the machine-learning links are explicit
  in the literature, not just analogies: Keup & Helias argue that the universal
  approximation property of ReLU nets is *linked to the fold-and-cut theorem*,
  with separability manufactured by progressive folding in unused higher
  dimensions; Lewandowski et al. give the first **quantitative** folding measure
  (range-metric based), prove equivalence of convexity notions between input and
  activation spaces, and validate on CantorNet and MNIST.
* **Honest boundary** — "ReLU layer = fold" is a modelling frame with numerical
  support (crease density vs depth / accuracy), not a theorem; the NP-power of
  fold-and-cut does **not** transfer.
* **Sources** — C. **Keup** & M. **Helias**, *Origami in N dimensions: How
  feed-forward networks manufacture linear separability*, arXiv:2203.11355
  (2022); M. **Lewandowski**, H. Eghbalzadeh, B. Heinzl, R. Pisoni & B. A. Moser,
  *On Space Folds of ReLU Neural Networks*, arXiv:2502.09954, TMLR 2025.

---

## M4. The ECA / elementary-cellular-automata family

* **Ours** — `PunoCalculus/EcaIsometry.lean` (affine/isometry classifications;
  the rule-204 / rule-51 identity–complement pair at every ring width 4..16);
  `PunoTwin/TwinRingLaws.lean` (`rule204_identity_all`, `rule51_complement_all`,
  **every** width); `PunoTwin/TwinAnalyticLaws.lean` (NLSE twin mass law);
  `ELASTIC_SOLITON_SCATTERING.md` (shift_bus **rule 29 == ECA 184**,
  **rule 71 == ECA 226**; the five density-conserving rules 15/29/51/71/85; the
  soliton family {12,44,68,100}); certified suite `Create Native Ramp Function
  and Implement 8-Bit ECA Rules/` (`run_all_audits.py`,
  `validate_soliton_isometry_proofs.py`).
* **Known studies** — **Wolfram**'s classification of elementary cellular
  automata into four classes (1983; 2002 *A New Kind of Science*, pp. 231, 693);
  **Cook**'s proof that rule 110 is universal (2004); rule 184 as the
  deterministic traffic / **TASEP** model (**Nagel**–Schreckenberg, 1992; exact
  flow derived by **Fuks**, 1999); the Fermat number `F4 = 65537 = 2^16+1` in
  the Fermat denominator window of `MPOperator`.
* **Shared content** — ECA rules form exhaustively enumerable families; identity
  (204) and complement (51) are the "perfect" members, closed under ring width.
  The density-conserving set is exactly `{15, 29, 51, 71, 85}`, and it
  decomposes the way the traffic literature predicts: the TASEP pair
  `29 ≡ 184` / `71 ≡ 226`, the transparent movers `15/85`, and the static
  identity `51` — indeed rule 184 is noted in the literature as one of only two
  symmetric non-trivial elementary rules that conserve the number of active
  sites, with 15/85 the transparent (hop-to-empty) cases and 51 the trivial
  static case.
* **Honest boundary** — rule-110 universality is Cook's theorem, not ours; our
  content is the exact classification / closure for the specific families at each
  width and the exact TASEP identification, not an autonomy result.
* **Sources** — S. **Wolfram**, *A New Kind of Science* (Wolfram Media, 2002),
  wolframscience.com; M. **Cook**, *Universality in Elementary Cellular
  Automata*, Complex Systems 15(1) (2004) 1–40,
  DOI 10.25088/complexsystems.15.1.1; K. **Nagel** & M. **Schreckenberg**,
  *A cellular automaton model for freeway traffic*, J. Phys. I France 2 (1992)
  2221; H. **Fuks**, *Exact results for deterministic cellular automata traffic
  models*, Phys. Rev. E 60 (1999) 197–202, arXiv:comp-gas/9902001,
  DOI 10.1103/PhysRevE.60.197; the rule-184 classification (Nagel 1996 PRE
  53:4655; Biham–Middleton–Levine; Maerivoet & De Moor 2005 survey;
  Chowdhury–Santen–Schadschneider, Phys. Rep. 329 (2000)) as collected at
  en.wikipedia.org/wiki/Rule_184.

---

## M5. The scaling-critical ladder (the Navier–Stokes wall)

* **Ours** — `CriticalLadder.lean` (C1), `SerrinLadder.lean` (C25),
  `OnsagerCriterion.lean` (C29), `ContinuationCriterion.lean` (C30),
  `SufficiencyLoop.lean` (C32), `EnstrophyBarrier.lean`,
  `QuantitativeContinuation.lean`; numeric halves
  `register_core_certificates.py`, `register_ladder_certificates.py`,
  `register_criteria_certificates.py`.
* **Known studies** — the **Prodi** (1959) / **Serrin** (1962) regularity
  criterion; its critical-space extension in `B^{-1}_{\infty,\infty}`
  (**Cheskidov**–Shvydkoy, 2007) and the `L^3` case of **Escauriaza**–Seregin–
  Šverák (2003); the full critical-Besov family
  `Ḃ^{-1+3/p}_{p,q}(R^3)` (**Gallagher**–**Koch**–**Planchon**, 2016);
  **Onsager** (1949) anomalous dissipation and its sharp exponent —
  conservation above 1/3, dissipation at or below (**Isett**, 2018, Hölder
  case; **Novack**–**Vicol**, 2023, intermittent `L^3`-based case; statistical
  and general-law variants of **Fjordholm**–Wiedemann and **Bardos** et al.);
  **Beale**–Kato–Majda (1984) and **Constantin**–Fefferman (1993) continuation
  criteria; **Tao** (2016, 2021) quantitative continuation; recent partial
  results (Feng–He–Wang, 2025; Grujic, 2024; **Albritton**, 2020, critical
  `BMO^{-1}`/`VMO^{-1}` criteria).
* **Shared content** — the one scaling-invariant index `s_crit(p) = 3/p - 1`
  is **literally** the critical Besov index of the Gallagher–Koch–Planchon
  family (`Ḃ^{-1+3/p}_{p,q}`), whose blow-up alternative generalizes the
  Escauriaza–Seregin–Šverák `L^3` theorem and specializes to the
  Cheskidov–Shvydkoy `B^{-1}_{\infty,\infty}` case at `p = ∞`; the
  complementary exponent `theta(p) + s_crit(p) = 1/2` is the Prodi–Serrin
  complementarity; and the Onsager-excess borderline `eta = 0` is exactly the
  sharp Onsager exponent (the conjecture is now a theorem in both directions on
  the Hölder and intermittent-Besov sides).
* **Honest boundary** — boundedness of the critical norm along the flow is
  **OPEN**; the whole register records it as a marker, never a settlement. The
  Onsager conjecture being settled is *their* theorem, not ours: it is the
  model for what a sharp borderline statement looks like.
* **Sources** — A. **Cheskidov** & R. **Shvydkoy**, arXiv:0708.3067 (2007);
  L. **Escauriaza**, G. Seregin & Š. Šverák, Uspekhi Mat. Nauk 58(2(350))
  (2003) 3–44; I. **Gallagher**, G. S. Koch & F. **Planchon**, *Blow-up of
  critical Besov norms at a potential Navier–Stokes singularity*, Comm. Math.
  Phys. 343 (2016) 39–82, arXiv:1407.4156, DOI 10.1007/s00220-016-2593-z;
  P. **Isett**, *A proof of Onsager's conjecture*, Ann. of Math. 188 (2018)
  871; M. **Novack** & V. **Vicol**, *An intermittent Onsager theorem*,
  arXiv:2203.13115, Invent. Math. (2023), DOI 10.1007/s00222-023-01185-6;
  U. S. **Fjordholm** & E. **Wiedemann**, *Statistical solutions and Onsager's
  conjecture*, arXiv:1706.04113, Physica D (2017),
  DOI 10.1016/j.physd.2017.10.009; C. **Bardos**, P. Gwiazda,
  A. Świerczewska-Gwiazda, E. S. **Titi** & E. **Wiedemann**, *On the Extension
  of Onsager's Conjecture for General Conservation Laws*, arXiv:1806.02483,
  J. Nonlinear Sci. (2018).

---

## M6. Discrete conservation (Noether)

* **Ours** — `NoetherDiscrete.lean` (`momentum_conserved`),
  `UniverseGrowth.lean` (`universeGrowth_conserves`); numeric half
  `arithmetic_shadow_certificates.py`.
* **Known studies** — **Noether** (1918) symmetry ⇒ conservation; its discrete,
  structure-preserving counterpart: the **discrete Noether theorem** of
  **Marsden** & **West** — an invariant *discrete* Lagrangian conserves the
  discrete momentum map, and Verlet/SHAKE/RATTLE are the resulting
  symplectic-momentum variational integrators.
* **Shared content** — translation invariance ⇒ a conserved momentum; growth
  that enters with zero displacement is neutral. Both sides are the same
  mechanism at different levels of discreteness: ours is the finite-sum shadow,
  theirs the geometric integrator.
* **Honest boundary** — finite sums of reals; no continuum limit, no field
  theory, no symplectic structure is constructed.
* **Sources** — W. W. **Marsden** & M. West, *Discrete mechanics and
  variational integrators*, Acta Numerica 10 (2001) 357–514 (Thm. 1.3.3,
  discrete Noether's theorem); W. **Kane**, J. E. Marsden & M. Ortiz,
  *Symplectic-Energy-Momentum Preserving Variational Integrators* (1999),
  cds.caltech.edu.

---

## M7. Orientation and boundedness (the great attractor)

* **Ours** — `GreatAttractor.lean` (C26), `OrientationBoundedness.lean` (C11),
  `OrientationLaw.lean` / `DissipativeFlow.lean` (C10); numeric half
  `register_ladder_certificates.py`.
* **Known studies** — Lyapunov stability and the sign of log-growth; fixed-point
  stability by linearization (`|f'|`); the attractive / neutral / repelling
  trichotomy.
* **Shared content** — the orientation (`|L| ⋚ 1`, sign of `log r`) decides
  boundedness; the log-growth integral is the discriminator, and orientation
  alone sets the wall's side.
* **Honest boundary** — numerical and finite-arithmetic; the analytic wall
  remains that of M5. *Gap note:* unlike M1–M6 and M8–M9, this block has no
  single named external theorem it is a form of — it is the classical
  linearization trichotomy applied to the ladder's own data, and we keep it
  listed as such rather than manufacturing a citation.

---

## M8. The logic barrier

* **Ours** — `PunoCalculus/LogicBarrier.lean` (C14: `lawvere_fixedpoint`,
  `no_surjective_of_no_fixedpoint`, `no_surjective_predicates`,
  `diagonal_not_mem_range`; axiom-free).
* **Known studies** — the **Lawvere** fixed-point theorem (1969); **Cantor**'s
  diagonal argument (1891).
* **Shared content** — a surjection onto predicates forces a fixed point, and the
  absence of that fixed point forbids the surjection — the abstract diagonal
  barrier. Lawvere's own framing is that Cantor, Russell, Gödel and Tarski are
  all special cases of the single fixed-point theorem (Cantor's theorem is the
  case `Y = 2`); our Lean module is the constructive shadow of exactly that
  statement.
* **Honest boundary** — the barrier is formal/constructive; it constrains proof
  *strategies*, not the truth of the underlying conjectures.
* **Sources** — F. W. **Lawvere**, *Diagonal arguments and cartesian closed
  categories*, Lecture Notes in Mathematics 92 (Springer, 1969); TAC reprint
  tac.mta.ca/tac/reprints/articles/15/tr15.pdf;
  en.wikipedia.org/wiki/Lawvere%27s_fixed-point_theorem.

---

## M9. The dimensional wall and mixtures

* **Ours** — `PunoCalculus/ExplicitClaims.lean` (`morrey_threshold`,
  `physical_embedding_gap`, `mean_le_dimMixture`); numeric halves
  `dimension_threshold.py`, `dimension_mixture.py`.
* **Known studies** — **Morrey**'s inequality and the Sobolev embedding
  `H^1 ⊂ L^∞` below dimension 2 (**Adams**–Hedberg, 1996); intermittency and
  dimension regularization in turbulence (**Frisch**, 1995; Constantin, 1994);
  the upper-critical-dimension wall of statistical mechanics: hyperscaling
  (`2 − α = dν`) holds below `d = 4` and breaks above, where mean-field
  exponents take over (**Pelissetto**–Vicari).
* **Shared content** — the `H^1 → L^∞` gain is `1 - d/2`, so the energy method is
  exactly half a derivative short at physical `d = 3`; the dimension of a mixture
  is a sup, not a mean, so averaging never lowers the effective dimension. The
  statistical-mechanics wall is the same shape of fact: a dimension threshold
  above which the classical (mean-field) description silently regains validity.
* **Honest boundary** — finite arithmetic on the embedding index; the analytic
  embedding theorems are cited, and the regularity wall stays open.
* **Sources** — see M2 for the Pelissetto–Vicari reference (hyperscaling and its
  breakdown above the upper critical dimension).

---

## What this crosswalk does not do

* It does not import any external result as a proof of ours, and does not export
  ours as a proof of theirs.
* It does not settle any Millennium problem; the register's marker stays
  **OPEN**.
* It is a map of *shared statements*, and `test_grounding_crosswalk.py` pins the
  links so the map cannot drift from the tree.

---

*Everything folds. Everything unfolds. The crease is where the action is.*
