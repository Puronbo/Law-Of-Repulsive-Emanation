# AUDIT — What is missing, conjectured, open, and claimed

Comprehensive findings from a full-corpus sweep (docs, experiments, library,
data, git history).  Verified items are marked **[verified]**, references the
audit did not re-run are marked **[claimed]** (the original source line is
given so it can be re-run).

---

## 1. WHAT IS MISSING

### 1.1 The declared next build (explicit, repeated)
* **O(1)-per-neuron spatial search.**  `decentral_net_ceiling.py` (T55h):
  "Scaling beyond ~2×10⁴ needs O(1)-per-neuron spatial search, not all-pairs."
  `decentral_net_union.py` (T55i) and `reverse_pair_gaps.py` (T57) repeat it.
  THE_BOOK Ch. 14: "the declared next build."  This is THE single most
  explicit unbuilt capability.  **[verified: repeated in 4 sources]**

### 1.2 The declared-required capability
* **The multivariate observation bank** (ASN, TLS age, WHOIS, content).  THE_BOOK
  Ch. 2 defines it canonically; Ch. 10 says the anomaly doctrine *requires* it:
  "names alone are necessary but not sufficient" (measured, T55j).  No
  implementation exists — the net stores only name embeddings (`q == h` in both
  pkls **[verified]**).  This is the biggest *scientific* gap: it is the stated
  path from "novelty works" to "anomalies distinguishable."

### 1.3 T-series gaps
* **T40–T47 (8 labels) have no experiment files.**  T46 and T47 are referenced
  as prior results (`balance_continual.py`: "T46 no-forgetting mechanism";
  `fib_stream.py`: "T47's optimal incremental rotation") but no file exists here.
* **T8 referenced** by `c0_cusp_flow.py` ("the Poincaré metric (T8)") — no file.
* **T48/T55 exist only as sublabels** (T48a/b, T55a–j); the pre-T39 history lives
  in `Universals/` modules and `docs/PAPER.md`, not as experiments.

### 1.4 The migration that was never applied
* `docs/MIGRATION.md` and `MIGRATION_1.md` are **byte-identical** and describe a
  v2 rewrite (`NoveltyDetectionEngine`, `Packet`, `evaluate_batch`,
  `export_manifest`, `tests/test_engine.py` expecting "7 passed",
  `requirements.txt`).  Those symbols exist **only in `archive\`** (the old
  "hyperbolic-ai" project), never in the live repo.  The live engine is the v1
  numpy `Universals/engine.py` (which *does* contain `dream`, `self_chain`,
  `record_self_event`, `classification_history`, `_quarantine_to_boundary`,
  `inject_and_evaluate_novelty` **[verified]**).  Treat the MIGRATION docs as
  historical intent — or execute them.  **[verified]**

### 1.5 Test coverage
* `tests/` holds only the T58–T64 spring suite (10 tests).  No test for the
  T-series, the manifold library, or the engine.  The T55-series experiments
  are self-verifying prints, not regression tests.

### 1.6 Orphaned/hygiene gaps
* `scripts/` is gitignored NodeDefense code from another project.  Its
  `config.yaml` has a real TODO: `novelty_threshold: null # TODO: Set via
  empirical fit from golden_set.npy` — and **`golden_set.npy` does not exist**.
* **`scripts/start.ps1` contains live credentials** (Bluesky + Groq API key).
  Currently gitignored, but it must be scrubbed before the repo is ever shared.
* `web_data.json` exists twice with identical MD5: `Universals/` (served by the
  dashboard) and `data/` (dead copy).
* No CI, no lockfile.  `pyproject.toml` + `puno` CLI exist (recent).
* README quickstart implies `math_validation.py` at root; it lives in
  `Universals/`.  The "142/147 validations pass" count is unverified here —
  `dependency_tree.dot` has 86 edges, `Universals/math_validation.py` has 37
  test functions.  **[claimed; count via `run_all.py`]**

### 1.7 Documented inconsistencies (fixable) — **RESOLVED 2026-08-01**
| Item | Value A | Value B | Resolution |
|---|---|---|---|
| PAPER.md test count | 88 (abstract) | 109 (conclusion) | Unified on **109**; abstract now cites §9 and notes unification. `run_all.py` was found to have a path bug (relative path doubled under `cwd` — all 20 steps failed before starting) and is **now fixed**; a full re-count is pending a fresh run. |
| PAPER.md ground state | E₀ = 5.84 | E₀ = 5.58 | **5.84 is correct** (`spectral_data.json` eig[0] = `thermo_data.json` ground_state = 5.843778304934855; r = 2.365 → λ = ¼ + r²). PAPER edited to 5.84. |
| `internet_net.pkl` size | 3.02 GB (THE_BOOK) | 3.17 GB (DECENTRAL_NET) | Actual 3,172,999,165 B = **3.17 GB**. THE_BOOK corrected. |
| README validation count | 142/147 | actual | Reran `math_validation.py`: **192 PASS, 0 FAIL**. README updated. Also fixed the script's UnicodeEncodeError on Windows consoles (stdout reconfigured to UTF-8). |

---

## 2. CONJECTURES (explicit)

1. **Prime geodesic theorem with sieve suppression** (README): π_k(L) ∼ ε_k·e^L/L
   — "conjectured to obey."  Data limit L ≤ 229 vs required L ≫ 300.  Whether the
   framework extends beyond 2ⁿ−k to arbitrary primes is declared open.
2. **Selberg paradigm** (PAPER): the finite-disk spectrum (30 eigenvalues)
   "suggests" a concrete instance of Selberg's framework; the eigenvalues ↔
   Riemann-zero correspondence is "conjectured" — and explicitly undecidable at
   30 eigenvalues (GUE/Poisson discrimination impossible).  **[claimed]**
3. **BOOK V pedagogy** (THE_BOOK): misconception = weak solution; creases =
   threshold concepts; C₀ = prior knowledge.  Preface says plainly: "the
   pedagogy has not been validated on learners."  **[verified: self-declared]**
4. **Four testable predictions, never executed** (PHYSICAL_UNIVERSAL_MAP §10.1):
   (i) recurrence time scales with entropy; (ii) T-symmetry of the loss
   landscape; (iii) holographic compression ratio (1,536 → 2); (iv) CTC/self-chain
   fixed point at 10⁶ iterations.  None has a dedicated experiment.
5. **Golden-ratio closure mechanism** (SPRING_BIBLE/T58): the fold "closes to
   r = apex·0.6138" — measured, but the *reason* the closing radius is set by
   the crease is asserted, not derived.
6. **"Golden metric" hypothesis** (`fibonacci_squares.py`): a metric where the
   log-spiral is geodesic — later confirmed *exactly* for the cusp metric by
   T39/golden_survey, so this one is effectively resolved.

---

## 3. OPEN THEORETICAL QUESTIONS

* **Wheeler–DeWitt on the disk** (PUM §10.5.1): can an analogue of the
  Hamiltonian constraint select "physical" knowledge configurations?
* **Fold-and-cut as discrete unitary evolution** (PUM §10.5.2): "remains open."
* **Kawasaki constraint** (PUM §10.2): mean deviation **0.49** from target 0 —
  a measured *failure*, called "genuine open problem."
* **Retrace boundary condition** — **RESOLVED by T64** (viscosity-selected cut
  locus).  **Fold theorem** — **RESOLVED by T63** (eikonal/viscosity).  Both
  should be treated as closed, not open.  **[verified]**
* **Prime-metric framework beyond 2ⁿ−k** (README).
* **Continuum limit**: PAPER's "residual drift is numerical and converges to
  zero as dt→0" is anticipated, not measured at arbitrary precision.

---

## 4. THEORIES STANDING (the framework's claims, with strength)

| Theory | Claim | Strength |
|---|---|---|
| **L.O.R.E.** (C₀ determined, not chosen) | C₀ = H(q₀,0), never arbitrary | PAPER: 109 tests, T-symmetry error 3e-3. |
| **Noether charge Q = H(t) ≈ C₀** | <1% drift over 1000 steps, converges as dt→0 | Measured on 6 trajectories; limit anticipated |
| **Eikonal fold cosmology** (T63/T64) | fold = unique viscosity solution of |r′|=a; retrace = cut locus | **Derived + 10-test regression suite** — the strongest theory in the repo |
| **Clock-test canon** (T59/T61) | laws live in invariants, not conventions | Measured 1.000→0.417→1.000 |
| **Anomaly doctrine** (T55j) | novelty works; impersonation partial; observation bank required | Measured, incomplete by its own verdict |
| **Arithmetic Bekenstein shift** (PAPER) | η_prime=0.1336 vs η_random=0.1285, Δη +3.9%, p=0.002 | 60 trajectories **[claimed]**; small-signal — re-verify |
| **Selberg unification** (PAPER) | 30 eigenvalues ↔ 196 Mersenne geodesics, ε(2)=0.000265 | **[claimed]**; eigenvalue sample too small to discriminate GUE |
| **Partition function match** (PAPER) | L(2)=40.14 vs C₀·π²/6=40.19 (<0.2%) | **[claimed]** |
| **Thermodynamics/entropy** | ln-thinning ↔ entropy; second law as folding | Analogical, not falsifiable as stated |
| **PUM §10.1 four-pack (T65)** | P1 τ~entropy; P2 T-symmetry; P3 holographic MI; P4 CTC fixed point | **0.5/4 confirmed.** P1 = tautology (τ := exp(entropy) in source); P2 refuted (recon err ≈ 1.8); P4 refuted (converged fraction 0.0); P3 weakly positive (MI 0.034 vs null 0.009) but synthetic. See `data/t65_fourpack_results.json` |

---

## 5. RECOMMENDED NEXT MOVES (ranked effort→value)

1. **Fix the five verified inconsistencies** (PAPER 88/109 + E₀, pkl size, README
   paths) — minutes, removes noise from every future reading.
2. **Execute the four PUM testable predictions** as a T65 four-pack (quick,
   local, closes §2.4) — the cheapest way to convert "conjectures" into
   measured facts, matching the project's own doctrine. **DONE 2026-08-02 —
   0.5/4 confirmed; P2 and P4 refuted, P1 tautological, P3 synthetic. See Ch.
   5.9 of WEAVERS_SCRIBE + `data/t65_fourpack_results.json`.**
3. **Scrub `scripts/` credentials** (and either delete or quarantine the orphan)
   before the repo is shared.
4. **Observation bank (T66)** — the declared-required capability; the one gap
   with genuine new science.  Needs an external data source (ASN/TLS/WHOIS) —
   network-bound.
5. **O(1)-per-neuron spatial search (T67)** — the declared next build; the one
   that unlocks flowing 1.9M sites.  Significant engineering.
6. **Either execute or retire MIGRATION** — currently a dead-but-authoritative
   doc; mark superseded to stop future confusion.
7. **Regression coverage for the T55 series + library** — the experiments print
   results but nothing pins them.

---

## 6. BOTTOM LINE

Nothing in the *claimed physics* is contradicted by the code — the strongest
results (fold derivation, clock test, anomaly doctrine, scaling law) are all
reproducible and internally consistent.  The gaps are: **(1)** the two declared
builds (observation bank, O(1) search) are absent; **(2)** four explicit
predictions and several conjectures (Selberg, PGT, pedagogy) are untested;
**(3)** the PAPER.md numbers contain two hard inconsistencies; **(4)** hygiene
items (orphaned `scripts/` with live credentials, dead doc copies, MIGRATION
superseded-but-present).
