# The brain and the mathematics of every crease

**Status: research synthesis + pointer, not a proof.** This note records what is
known about the human brain — what it does, why it evolved to generate thought —
and then isolates the one part of the picture that is *exactly* mathematics: the
local normal form of every fold. The local mathematics is machine-checked in
`01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/Crease.lean`; the brain
facts below are empirical literature, cited, and are **not** claimed as proved by
this repository. Where a statement is a theory (not settled science) it is marked.

---

## 1. What the brain can do

- **Scale.** The adult human brain has on the order of **8.6 × 10¹⁰ neurons**
  (Azevedo et al. 2009); the cerebral cortex alone holds roughly 1.6 × 10¹⁰, with
  the remainder in cerebellum and subcortical structures. Cortical neurons make on
  the order of **10¹⁴–10¹⁵ synaptic connections** (reviewed in Galakhova et al.
  2022). The connectome is a directed weighted graph of astronomical degree.
- **It computes over representations.** Sensory areas encode the world, downstream
  areas decode — a distributed succession of encode/decode steps that build
  internal models used to select actions (Mathis et al. 2024). "Activation" is the
  weak statement; the strong one is that a region's population activity *carries*
  decodable content that other regions read.
- **It composes.** Human thought is combinatorial: an unbounded set of novel
  concepts can be generated and understood (Frankland & Greene 2020). Evidence
  points to map-like representations (default-mode subregions) combined with
  sentence-like relational representations (temporal and prefrontal cortex),
  echoing Fodor's "language of thought" as a mechanism, not a metaphor.
- **It predicts.** The free-energy principle (Friston 2010, and many later works)
  frames perception, action, and learning as the minimisation of a variational
  free energy — the brain as a prediction machine that continuously updates a
  generative model against sensory evidence. This is the leading "why" of cortical
  computation; it is a *theory*.

## 2. What made the human brain evolve, and generate thought

- **Expansion is not just "more neurons."** Cortical expansion in humans is driven
  as much by *neuron properties and connectivity* as by cell number (Galakhova et
  al. 2022; Namba & Huttner 2024). Human supragranular (upper) cortical layers are
  disproportionately enlarged, their pyramidal neurons have larger, more complex
  dendrites — a single human neuron can perform computations comparable to a
  multi-layer network — and their synapses are strong, reliable, and fast-recovering.
- **Human-specific genes and progenitors.** Molecular work points to human-specific
  genes that alter the behaviour of cortical stem and progenitor cells, expanding
  the neocortex (Namba & Huttner 2024). The same broadly conserved cell types are
  shared across species but develop on different temporal trajectories and acquire
  distinct molecular and functional properties (Nehme et al. 2024).
- **The threshold account.** At some scale of neurons, connectivity, and recurrence,
  a system becomes also a *subject* — a thing to which events appear. The two
  leading computational theories are **global workspace theory** (Baars; Dehaene —
  broadcast of selected information to many regions) and **integrated information
  theory** (Tononi — a measure Φ of how irreducible the system's causal structure
  is). Neither is settled. The **hard problem** (Chalmers 1995) — why any of this
  processing is *experienced* rather than merely performed — is open; no physical
  account of the processes has closed it.

## 3. The mathematics of every crease

This is the part that is exact. Two layers — a global empirical scaling, and a
local theorem.

### 3.1 The folds are creases (global, empirical)

The folds of the cerebral cortex (gyri and sulci) are **creases** of a
growth/buckling energy acting on the cortical sheet:

- **Mechanical origin.** Richman & Stewart (1988) modelled the developing cortex as
  a layered elastic sheet in which an outer stratum grows faster than the core,
  producing compressive stress and, past a critical stress, elastic **buckling** —
  the gyri and sulci. The same differential-growth/buckling class of model underlies
  microgyria and lissencephaly.
- **Universal scaling.** Mota & Herculano-Houzel (*Science* 2015) showed that the
  degree of folding scales **uniformly** across lissencephalic and gyrencephalic
  species, across individuals, and within a single cortex, as a function of the
  product of total cortical surface area `A` and the square root of cortical
  thickness `√t`. The relation is *derived* by minimising an effective free energy
  of cortical shape, and it also reproduces the folding index of crumpled paper
  balls. Wang et al. (*PNAS* 2016) confirmed it across >1000 human MRIs — invariant
  to sex, shifted by age, and perturbed (lower offset / exponent) in Alzheimer's —
  a mechanistic link read as changes in the mechanical forces on the cortex.
- **Honesty.** This section is a citation of *empirical and modelling* results. The
  exponent (predicted 1.25, observed ≈1.305) is a physical-law claim, not a theorem
  of this repository.

### 3.2 Every crease is a cusp (local, exact)

Globally the folds are a scaling phenomenon; **locally, every generic crease has a
single normal form** — Thom's cusp — and that form is elementary and completely
provable. `PunoCalculus.Crease` formalises it:

- **Fold germ.** `Φ a x = x³ − a·x`, with derivative `3x² − a` (`deriv_fold`).
- **Crease criterion.** A point is a crease iff the derivative vanishes:
  `deriv (Φ a) x = 0 ↔ 3x² = a` (`deriv_fold_zero_iff`). Hence a crease exists only
  for `a ≥ 0` (`crease_nonneg`), and for `a > 0` there are exactly **two**,
  `x = ±√(a/3)` (`crease_sqrt`, `crease_neg_sqrt`, `crease_eq_sqrt_or`).
- **The cusp.** At `a = 0` the two creases collide at a single degenerate crease
  `x = 0` (`crease_zero_iff`); for `a < 0` the fold has no crease
  (`no_crease_of_neg`). This is the cusp bifurcation: creation/destruction of a pair
  of creases as the parameter crosses zero.
- **Cusp potential.** `V a b x = x⁴/4 − a·x²/2 − b·x`, whose gradient is the fold
  germ `x³ − a·x − b` (`deriv_cusp`) — the crease manifold is the gradient-zero
  surface, a cusp surface in `(a, b, x)`.
- **Double root.** On the cusp curve `a = 3r²`, `b = −2r³`, the gradient factors as
  `(x − r)²(x + 2r)` (`cusp_curve_factor`): the crease is a **double root**, and the
  discriminant vanishes, `4a³ = 27b²` (`cusp_discriminant`).
- **The shared instance.** The logistic apex `x = 1/2` of `ParabolaVertex` is a
  crease of the doubling map: `deriv logistic (1/2) = 0` (`deriv_logistic_half`).

So "the mathematics of every crease," taken at the level where it is *certain*, is
the cusp normal form and its unfolding. What remains genuinely open is the *global*
statement — that a given physical crease pattern (a cortex, a crumpled sheet, a
trained network's decision boundary) is minimising a specific energy with a specific
exponent — which is where the empirical claims of §3.1 live.

---

## What is and is not claimed here

- **Proved (machine-checked):** the local fold/cusp algebra in
  `PunoCalculus.Crease` — crease criterion, crease counts, cusp potential gradient,
  double-root factorisation, discriminant, and the logistic-apex crease.
- **Cited, not proved:** brain scale and composition; the human-specific expansion
  mechanisms; the free-energy, global-workspace and integrated-information theories;
  the cortical buckling model and the universal folding scaling law.
- **Open:** the hard problem of consciousness; the rigorous derivation of folding
  from first-principles physics; and the identification of any crease pattern with a
  specific energy exponent in the framework's own terms.

## References

- Azevedo, F. A. C. et al. (2009). Equal numbers of neuronal and nonneuronal cells
  make the human brain an isometrically scaled-up primate brain. *J. Comp. Neurol.*
- Chalmers, D. J. (1995). Facing up to the problem of consciousness. *JCS* 2(3).
- Frankland, S. M., & Greene, J. D. (2020). Concepts and compositionality: in search
  of the brain's language of thought. *Annu. Rev. Psychol.* 71.
- Friston, K. (2010). The free-energy principle: a unified brain theory?
  *Nat. Rev. Neurosci.* 11.
- Galakhova, A. A. et al. (2022). Evolution of cortical neurons supporting human
  cognition. *Trends Cogn. Sci.*
- Mathis, M. W. et al. (2024). Decoding the brain: from neural representations to
  mechanistic models. *Cell*.
- Mota, B., & Herculano-Houzel, S. (2015). Cortical folding scales universally with
  surface area and thickness, not number of neurons. *Science* 349(6243).
- Namba, T., & Huttner, W. B. (2024). What makes us human: insights from the
  evolution and development of the human neocortex. *Annu. Rev. Cell Dev. Biol.*
- Nehme, R., Pietiläinen, O., & Barrett, L. E. (2024). Genomic, molecular, and
  cellular divergence of the human brain. *Trends Neurosci.*
- Richman, D. P., & Stewart, R. M. (1988). Mechanical model of brain convolutional
  development. *Science* 240.
- Tononi, G. (2008). Consciousness as integrated information: a provisional
  manifesto. *Biol. Bull.* 215.
- Wang, Y., Necus, J., Kaiser, M., & Mota, B. (2016). Universality in human cortical
  folding in health and disease. *PNAS* 113(45).
