# Puno Calculus

**The Law of Repulsive Emanation (L.O.R.E.)** -- *C0 is measured, not chosen.*

55 experiments showing that the deep structure of mathematics is the indeterminate form 0/0: a singularity whose removable value encodes the structural information of the system it sits in. The capstone theory document, **The Law of Singularities**, formalizes this as axioms, five mechanisms, and a classification theorem.

## The Thesis

The antiderivative integral f(x)dx = F(x) + C has an arbitrary constant only when the initial condition is unknown. When it IS known, the constant collapses to a specific value C0, uniquely determined by the geometry: C0 = V(q0) = H(q0, 0). This is L.O.R.E. -- the constant emanates from the origin.

The entire framework turns out to be a 0/0 structure. C0 = V(q0)/(N - |context|) is 0/0 at full context (both numerator and denominator vanish). The same form appears everywhere: g(s) = |zeta(s)|/|zeta(1-s)| is 0/0 at every zeta zero, with removable value |chi(rho)| that equals 1 if and only if Re(rho) = 1/2 -- making the Riemann Hypothesis equivalent to proving the singularity is removable.

**The Law of Singularities** ([`THE_LAW_OF_SINGULARITIES.md`](docs/THE_LAW_OF_SINGULARITIES.md)) formalizes this: five mechanisms by which 0/0 arises (Probe, Index, Vanishing Rate, Critical Phenomenon, Conservation), a classification theorem for removable vs essential singularities, and an extraction theorem showing how to recover the structural information. 55 experiments across 14 batches verify the pattern across number theory, topology, analysis, physics, statistics, information theory, and geometry.

## Papers

### The Law of Singularities (Capstone)

| Paper | Description |
|---|---|
| [`THE_LAW_OF_SINGULARITIES.md`](docs/THE_LAW_OF_SINGULARITIES.md) | **The formal theory:** axioms, 5 mechanisms, classification theorem, extraction theorem, universality theorem, 20 chapters, 55 experiment applications |

### The 0/0 Paper Suite

| Paper | Description |
|---|---|
| [`THE_UNIVERSAL_ZERO.md`](docs/THE_UNIVERSAL_ZERO.md) | Main synthesis: 55 experiments, five mechanisms, complete taxonomy |
| [`ON_THE_NATURE_OF_ZERO.md`](docs/ON_THE_NATURE_OF_ZERO.md) | Philosophical treatise: what zero actually is, the three zeros, 20 chapters |
| [`THE_0_OVER_0_ATLAS.md`](docs/THE_0_OVER_0_ATLAS.md) | Reference atlas: complete catalog, cross-reference tables, decision tree |
| [`REMOVABLE_SINGULARITIES.md`](docs/REMOVABLE_SINGULARITIES.md) | Epistemology: what the 0/0 form tells us about knowledge |

### Companion Papers

| Paper | What it proves |
|---|---|
| [`RH_REDUCTION_PAPER.pdf`](docs/RH_REDUCTION_PAPER.pdf) | g(s) = \|zeta(s)\|/\|zeta(1-s)\| is identically 1 iff RH; combined with Rodgers-Tao, RH <=> Lambda = 0 |
| [`WHAT_ZERO_IS.pdf`](docs/WHAT_ZERO_IS.pdf) | Zero has three identities; c/0 is a pole, 0/0 is indeterminate |
| [`WHERE_0_OVER_0_SOLVES.pdf`](docs/WHERE_0_OVER_0_SOLVES.pdf) | 0/0 as structural probe in 10 open problems |
| [`IF_C0_IS_0_OVER_0.pdf`](docs/IF_C0_IS_0_OVER_0.pdf) | C0 = 0/0; viscosity solution = unique removable value |

Source generators: `generate_companion_papers.py`, `generate_rh_paper.py`.

## Key Results

| Result | Headline Number |
|---|---|
| RH reduction | g(s) = 1 on critical line, 0/0 at zeros, removable value = \|chi(rho)\|, equals 1 iff Re(rho)=1/2 |
| C0 = 0/0 | V(q0)/(N - \|context\|) is 0/0 at full context; removable value = average energy per non-context node |
| Fold theorem (T63/T64) | Crease = unique viscosity solution of \|r'\| = a; eikonal error 3.3e-13 |
| Internet-scale flow (T72) | 1,914,915 sites flowed at ~449 s/step; 20% kill heals +7.8% |
| O(1) spatial search (T67) | Bit-identical to all-pairs; n=100k at 10.35 s/step |
| Prime count (T62) | pi(943,901,200,001) = 35,575,526,191 from scratch |
| Mertens census | M(10^11..10^14) computed exactly, completing the published table |
| Certified zeros | 648 zeros on Re(s)=1/2 via interval arithmetic (not a proof of RH) |
| GUE statistics | 22,491 zeros fit GUE: KS 0.037, beta = 1.64, Montgomery-Odlyzko law |
| Math validation | 192/192 checks pass; 149/149 regression tests pass |

Full experiment details: [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md)

## Experiments (55 total, 14 batches)

Each experiment is a Python script in `experiments/` that writes a verdict JSON to `data/`. All 149 regression tests pass from persisted data.

**Number Theory (10):** GRH Dirichlet, abc conjecture, BSD, Euler product, Weil explicit, PNT, Mertens census, Mertens explicit height, Chebyshev psi, Mobius function

**Topology (8):** Poincare-Hopf, Riemann-Roch, Atiyah-Singer, Gauss-Bonnet, Lefschetz fixed-point, Morse theory, Brouwer fixed-point, Stokes/de Rham

**Analysis (12):** Argument principle, Heat kernel trace, Weyl's law, Euler-Maclaurin, Laplace method, Wallis product, Cesaro summation, Cauchy integral, Rayleigh quotient, Poisson summation, Saddle point, Taylor remainder

**Algebra/Number Theory (5):** Fermat's little theorem, FTA, Pythagorean theorem, Banach fixed-point, Noether/Landau

**Physics (4):** Ising model, Spectral gap, Green's function, Lorenz attractor

**Statistics/Info Theory (4):** Central limit theorem, Shannon entropy, Bayes theorem, Boltzmann entropy

**Geometry/Combinatorics (6):** Fourier uncertainty, KKT conditions, Sard's theorem, Picard's little theorem, Khintchine, Schanuel

**Original L.O.R.E. (6):** Spring fold, Eikonal fold, Retrace boundary, Fold optimizer, Prime count, Googol census

See [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) for full results and honest walls.

## Bazaar -- P2P Social Platform

Reddit + 4chan in the browser. No server stores your data.

- WebRTC DataChannels for peer-to-peer mesh
- Content-addressed via SHA-256; ECDSA P-256 identity
- 0/0 quality scoring (posts start at 0/0, converge to a removable value as peers vote)
- Anonymous or identified
- Optional WebSocket signaling relay (`server.js`) or fully manual SDP exchange (no server needed)

```
bazaar/index.html     # self-contained web app (no build step)
bazaar/server.js      # optional WebSocket signaling relay (~70 lines Node.js)
bazaar/README.md      # usage instructions
```

## Repository Map

```
Universals/           # L.O.R.E. core: engine, proofs, math validation, Hamiltonian flow, manifold
puno_flow/            # Exact balance-flow SDK: modular-add arithmetic, ledger, consensus, plugins
experiments/          # 55 experiment scripts (batches 1-14 complete)
data/                 # Regenerable verdict JSONs (gitignored)
tests/                # 149 regression tests (all passing)
docs/                 # Papers, theory, instrument manuals, audit, weavers
  THE_LAW_OF_SINGULARITIES.md    # Capstone theory document
  THE_UNIVERSAL_ZERO.md          # Main 0/0 synthesis
  ON_THE_NATURE_OF_ZERO.md       # Philosophical treatise
  THE_0_OVER_0_ATLAS.md          # Reference atlas
  REMOVABLE_SINGULARITIES.md     # Epistemology
  RH_REDUCTION_PAPER.md/.pdf     # RH proof reduction
  WHAT_ZERO_IS.md/.pdf           # Classification of zero
  WHERE_0_OVER_0_SOLVES.md/.pdf  # 10 open problems
  IF_C0_IS_0_OVER_0.md/.pdf     # C0 as 0/0
  EXPERIMENTS.md                 # Full experiment details (this file's companion)
  AUDIT.md                       # Claim-by-claim audit (82 sequels)
  WEAVERS_SCRIBE.md              # Narrative chapters (5.48)
  KEYWORDS.md                    # Keyword index
bazaar/               # P2P social platform (index.html, server.js)
calendars/            # Universal calendar (14 civilizations, exact rational arithmetic)
professions/          # AI-performable professions (14-profession verdict)
packaging/            # Packaging-line systems (PLC, servo, air, water)
patents/              # Provisional patent drafts
puno_app/             # Browser lab, web dashboards, Bazaar UI
plugins/              # Auto-discovered plugin registry
scripts/              # Net nodes, pipeline, operational scaffolding
tools/                # Net service installers
```

## Proof Hierarchy

| Branch | Items | Scope |
|--------|-------|-------|
| Axioms | A1-A5 | Poincare metric, Hamilton's eqs, PSL(2,Z), He init, 2^n mod p |
| Lemmas | L1-L3 | Variance, ReLU contraction, max entropy |
| Theorems | T1-T10 | Metric, geodesics, symplectic, sieve, C0 unification, modular |
| Corollaries | C1-C8 | Stab(i), crease bounds, recurrence, generalization gap, C7 bridge |
| Extended | **T19** | Consistent chaos -- geodesic flow embeds Mersenne-gap primes |

Full graph: `dependency_tree.dot`. 192 math-validation checks pass (0 failures).

## Core Idea

The antiderivative integral f(x)dx = F(x) + C has an arbitrary constant only when the initial condition is unknown. When the initial condition IS known, the constant collapses to a specific value C0:

    C0 = V(q0) = H(q0, 0)

This is **L.O.R.E.** -- the constant emanates from the origin. It is measured, not chosen.

## Quick Start

```bash
# install (numpy + stdlib only)
pip install -e .

# run the core
cd Universals && python engine.py && python math_validation.py   # 192 checks, 0 fails

# run the regression suite (149 tests, all passing)
pytest tests/test_solvable_theorems.py

# run a few key experiments
python experiments/prime_count_from_scratch.py       # pi(943901200001) = 35575526191
python experiments/eikonal_fold.py                    # fold theorem (viscosity solution)
python experiments/decentral_net_t67.py               # O(1) spatial search on 100k points
python experiments/grh_dirichlet_0_over_0.py          # GRH probe for 8 Dirichlet L-functions

# run all 0/0 experiments (batches 1-14)
python experiments/central_limit_theorem_0_over_0.py  # CLT 0/0
python experiments/ising_model_0_over_0.py            # Ising phase transition
python experiments/zeta_functional_eq_0_over_0.py     # zeta functional equation

# the browser lab
puno-lab [--host 127.0.0.1] [--port 8765]

# the universal calendar
puno-calendar today

# professions mandate report
puno mandates

# Bazaar P2P social platform
node bazaar/server.js     # optional signaling relay
# open bazaar/index.html in browser

# plug-and-play UI (auto-discovers all functions and experiments)
puno-plug [--host 127.0.0.1] [--port 8767]
```

## Honest Walls

- RH remains **open**; the 0/0 experiments are complete reductions (g = 1 IS Re(rho) = 1/2), not unconditional proofs
- The Mertens conjecture is proven false but no explicit counterexample is known; |M(x)| < sqrt(x) holds for all x <= 10^14
- pi(x) > Li(x) is proven to occur but pi(x) < Li(x) at every computable height
- The Bekenstein shift result is **withdrawn** (positional, not primality)
- Selberg unification and partition-function match are **tautologies** by construction
- The PUM cosmological mapping is not citable as verified physics

Full audit: [`docs/AUDIT.md`](docs/AUDIT.md) (82 sequels, claim-by-claim)

---

*Everything folds. The constant is determined. The chaos is consistent.*
