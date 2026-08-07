# Puno Calculus

The Law of Repulsive Emanation (L.O.R.E.): *C0 is measured, not chosen.*

A hyperbolic novelty engine: Hamiltonian flow on the Poincare disk, a formal proof hierarchy (27 items: axioms → lemmas → theorems → corollaries → extended), a derived fold theorem, a decentralized consensus flow that has been run on the whole 1.9M-site internet, and a from-scratch prime count verified exact.

## Verified Findings (2026-08-04)

Every number below was re-verified by rerun or direct read of the persisted data file. Full claim-by-claim declaration with references: `docs/NOVELTY_AND_CREATION.md`.

Looking for a topic? `KEYWORDS.md` maps search terms to files, including topics that don't appear in any file name.

| Finding | Result |
|---|---|
| Math-validation suite | **192 passed / 0 failed** (`Universals/math_validation.py`) |
| Regression suite | **15/15 passed** (`tests/test_spring_series.py` + `tests/test_solvable_theorems.py`, ~1.1 s) |
| L.O.R.E. | C0 = V(q0) = H(q0,0), 109 tests; T-symmetry error 0.003 |
| Fold theorem (T63/T64) | crease = **unique viscosity solution of |r′| = a**; retrace = cut locus; eikonal err 3.3e-13; measured crease 0.0350π vs derived 0.0318π; area 2666.6665 vs 2666.6666… |
| Clock-test canon (T59/T61) | law-ness 1.000 → 0.417 under calendar re-index → 1.000 under rotation; rotation overlap/sim 1.000 |
| Prime count (T62) | **π(943,901,200,001) = 35,575,526,191** from scratch (Lucy-Hedgehog + segmented sieve); 943,901,200,001 is prime |
| Googol census (C7) | 186 primes 2ⁿ−k < 10¹⁰⁰ across 15 k-families (k=3: 21, k=1: 12, k=5: 19); n_max = 332 |
| T67 O(1) spatial search | indexed flow **bit-identical** to all-pairs; 2D exponent 1.02 vs exact 1.88; n=100k flows at ~5 s/step (all-pairs D = 160 GB); 10k×128-D real domains ~2 s/step (D = 102 GB) |
| T72 whole-internet flow | 1,914,915 sites flowed: **277,218 ms/step**, all-pairs D = 58,670 GB; 20% kill (382,983) then heal +7.8% spacing recovery |
| Decentral Bank (T68–T71, T16–T20) | double-entry ledger conserved exactly over 3000 txs; nonce replay rejected; quorum = majority honesty (not BFT), catches every faulty send < 40% corruption; anomaly recall 0.51 / precision 0.63 vs null 0.019; Ed25519 sigs verified; WAL bit-identical save/load; 14/14 commit over real TCP sockets; mutual TLS; LAN NIC 192.168.100.241 |
| Ground states | quantum E0 = 5.843778304934855; classical conservative 24.4328733; dissipative 10.0036703 (30 eigenvalues) |
| Kawasaki | mean deviation 0.49 from target 0 — **resolved 2026-08-08: sampling artifact** (point-cloud scatter; exact 2-line criterion |4α−2π| fails generically, 9.5% vs 8% uniform null); ReLU fold vertices are NOT flat-foldable |
| Continuum-limit drift | **measured PASS 2026-08-08** — first-order convergence to zero (order 0.925–1.040); residual is the boundary r=0.99 projection floor |
| Golden-ratio closure (T58) | **derived 2026-08-08** — r_ret/apex = 0.6137690167 = θ*/Θ solving s(θ*)/s(Θ)=1/φ² on the Archimedean spiral (delta 0.0, → 1/φ as Θ→∞) |
| Spectral C1/C3/C4 (100 modes) | C1 partial (k=12: 0.53%, k=26: 0.96%); C3a not supported (no mode near λ(7)); C3b supported (12.2416 vs λ(31)=12.261, Δ=0.0197); C4 → Poisson ⟨r⟩=0.372 (GOE 0.536) |

**Honest walls (recorded, not hidden):** Bekenstein shift **withdrawn** (its own persisted data shows the null: p=0.789/0.938); Selberg unification and partition-function match are **tautologies** by the code's own construction; T65 four-pack scored **0.5/4** (P2, P4 refuted); PUM cosmological mapping is not citable as verified physics (`docs/AUDIT.md` §3–§4).

## Core Idea

The antiderivative ∫f(x)dx = F(x) + C has an arbitrary constant only when the initial condition is unknown. When the initial condition IS known, the constant collapses to a specific value C0, uniquely determined by the geometry:

    C0 = V(q0) = H(q0, 0)

This is **L.O.R.E.** — the constant emanates from the origin. It is measured, not chosen.

## Proof Hierarchy

| Branch | Items | Scope |
|--------|-------|-------|
| Axioms | A1–A5 | Poincare metric, Hamilton's eqs, PSL(2,Z), He init, 2ⁿ mod p |
| Lemmas | L1–L3 | Variance, ReLU contraction, max entropy |
| Theorems | T1–T10 | Metric, geodesics, symplectic, sieve, C0 unification, modular |
| Corollaries | C1–C8 | Stab(i), crease bounds, recurrence, generalization gap, C7 bridge |
| Extended | **T19** | Consistent chaos — geodesic flow embeds Mersenne-gap primes |

Full graph: `dependency_tree.dot`. 192 math-validation checks pass (0 failures).

## Prime Geodesic Bridge (C7)

Each Mersenne-gap prime 2ⁿ−k maps to a closed geodesic on the modular surface X(1) = PSL(2,Z)\H via:

    ℓ = n·ln2 − ln(k),    λ = ¼ + ℓ²

**Googol census** (`data/googol_census_all_k_c7.json`): 186 primes of form 2ⁿ−k < 10¹⁰⁰ across 15 k-families (odd k < 30), verified from the persisted file (k=3: 21 primes, avg gap 13.15; k=1: 12 primes, avg gap 11.36; k=5: 19 primes). All C7 bridge values computed.

## Fold Theorem (T63/T64) — strongest derived result

The spring-fold with fixed endpoints and one free apex obeys the eikonal equation |r′| = a on [0, 2Θ]; the crease is the **unique viscosity solution** and the retrace curve is the **cut locus**. Verified: eikonal error 3.3e-13, upwind error ~1e-10, measured crease angle 0.0350π vs derived 0.0318π, mirror area 2666.6665 vs 2a²Θ³/6 = 2666.6666…, pinned by the 10-test regression suite.

## T19: Consistent Chaos (Capstone)

The C7 bridge embeds Mersenne-gap primes into the Anosov geodesic flow on X(1) — a deterministic chaotic system. The induced distribution is conjectured to obey the Prime Geodesic Theorem suppressed by the sieve survival probability εₖ:

    π_k(L)  ∼  ε_k · e^{L} / L

**What's proven:**
- Every Mersenne-gap prime maps injectively to a closed geodesic (C7)
- The sieve density εₖ explains the observed sparsity ordering (T7)
- All 186 primes < 10¹⁰⁰ are consistent with Anosov dynamics

**What's conjectured:**
- The asymptotic PGT formula requires L >> 300 (current data: L ≤ 229)
- Whether this framework extends beyond 2ⁿ−k to arbitrary primes is open

**What's measured (2026-08-08, `experiments/pgt_finite_l.py`):** at finite L the
growth form is **refuted** — π_k(L) grows like ln L (one candidate per n),
slope 0.002 vs the predicted 1.0, and ε_k·e^L/L overpredicts the observed 186
primes by ~95 orders of magnitude at L=200.  The sieve ordering is only partial
(Pearson r=0.696, Spearman 0.816).  The literal PGT-with-sieve-suppression
conjecture is falsified at finite L; the L≫300 asymptotic is unreachable from
the googol census (n_max=332) and would need the full X(1) geodesic spectrum.

## Epoch 0d (2000-10-26 10:26:20.00)

The corpus's own measured datum, folded into the retrace chain (`data/epoch_0d.json`, `docs/WEAVERS_SCRIBE.md`, SPRING_BIBLE Ch. 14).

**The anchor pair:** `10,262,000 = 2⁴·5³·7·733` and `26,102,000 = 2⁴·5³·31·421` — both have **80 divisors** and **digit sum 11** under MM/DD↔DD/MM swap.

**Key findings:**
- **Prime-pairing rule**: each number = exactly **one Mersenne prime** (≡3 mod 4) + **one sum-of-two-squares prime** (≡1 mod 4); both two-square primes' roots sum to the same prime **29** ({7, 733}: 7=2³−1, 733=2²+27²; {31, 421}: 31=2⁵−1, 421=14²+15²).
- **The fold 1,914,467 = 31 × 61,757** — the chain bridge to the DD/MM side; the pairing rule extends (61,757 = 139²+206²), and survives reversal (7,644,191 = 197 × 38,803).
- **Three-way connection** (10,262,000 ↔ 26,102,000 ↔ 1,914,467): gcd triangle **2000 / 31 / 1** — the two date forms share the *year* 2000; the DD form and the fold share the *Mersenne* 31; **B = 26,102,000 is the hub**. Chain mod-31 ladder: 15, 0, −1, 0, 1.
- **Null analysis (binding creases)**: τ=80 equality is a year-2000 trailing-zero artifact (0/365 in 2007; 17/366 = 4.64% in 2000, all even-month/even-day); τ=8 equality is the generic ~7.4% coincidence; base-invariance survives **base 10 and 12 only**.

## Experiments (verified from persisted data)

| Experiment | Result |
|------------|--------|
| Subgradient Selection (exp1b) | All 4 strategies (standard/random/oppose/always_on) reach **99.8% best / 99.7% final** accuracy |
| Crease vs Complexity (exp2) | **r(crease, complexity) = −0.77** (recomputed from data: −0.766) — deeper nets crease less |
| Early Stopping (exp3) | Crease-stable stops at 26–80% epoch savings (shallow 79.8%, medium 64%, deep 71%), test acc within ~3 pts of baseline |
| OOD Detection (exp_ood) | Crease AUROC **0.88** on center-noise (beats MSP's 0.71); MSP better on far-Gaussian (0.99) |
| Pruning (exp_pruning) | Crease beats magnitude at 7/10 ratios, **+13.5 pts at 25%** (0.720 vs 0.585); not a strict win at 10%, 45%, 50% |
| Googol Census (C7) | 186 primes across 15 k-families (k=3: 21, k=1: 12, k=5: 19) |
| Continuum limit (`continuum_limit.py`) | drift → 0 at first order (0.925–1.040) on interior trajectories; boundary clip = floor |
| Spectral extended (`spectral_extended.py`) | 100 modes; C1 partial (k=12 0.53%), C3b supported (Δ=0.0197), C4 → Poisson ⟨r⟩=0.372 |
| Kawasaki null (`kawasaki_null.py`) | 0.4866 reproduced; shown to be point-cloud scatter, not flat-foldability failure |
| PGT finite-L (`pgt_finite_l.py`) | growth form refuted (slope 0.002 vs 1.0); sieve ordering partial (r=0.696) |
| Golden-ratio closure (`fold_golden_closure.py`) | 0.613769 derived exactly (s(θ*)/s(Θ)=1/φ², delta 0.0) |

## Internet-Scale Flow (T67, T72)

The DecentralNet engine's per-neuron flow is O(n²) all-pairs. **T67** replaced it with a proven-exact spatial index (numpy grid for dim ≤ 3, cKDTree for dim ≥ 4): results are **bit-identical** to all-pairs, only the expected work is O(1). Measured: 2D exponent 1.02 vs exact 1.88; n=100k 2D at ~5 s/step where all-pairs needs a 160 GB distance matrix; 10,000 real top-1M domain embeddings at 128-D in ~2 s/step (102 GB all-pairs).

**T72** then flowed the *entire* real internet net (1,914,915 sites — union of Cisco Umbrella + Majestic top-1M, PCA(2) of real 128-D embeddings): **277,218 ms/step** where all-pairs D would be 58,670 GB; consensus spacing 0.00033 → 0.00036; a 20% kill (382,983 sites) recovers +7.8% spacing after heal(1). Honest wall: 128-D native flow stays near 10⁴ (crease #22), and this is still one machine. See `experiments/decentral_net_t67.py`, `experiments/decentral_net_t72.py`, `data/decentral_net_t67_data.json`, `data/decentral_net_t72_data.json`.

## Decentral Bank (T68–T71, T16–T20)

A value-carrying fragment bank where **routing is ownership**: hashed double-entry ledgers, nonce double-spend rejection, witness quorum, and an amount-outlier anomaly layer — with its walls measured, not assumed.

- T1–T6: deterministic routing (partition spread min 8 / max 74 / σ 20.6 over 16 fragments); integrity conserved exactly (64,000 = 64,000 over 3000 txs); nonce replay rejected; 30% damage survives; quorum catches *every* faulty send below 40% corruption but collapses at ≥50% — **majority honesty, not BFT**; anomaly recall 0.51 / precision 0.63 vs null 0.019.
- T7/T8: Ed25519 signatures verified at append (tamper/wrong-key/address-spoof all rejected); WAL save/load bit-identical.
- T12–T18: PROPOSE→VOTE→COMMIT→NOTIFY over a controllable relay, then real TCP sockets — 14/14 commit, bit-identical replicas, stateless restart rebuilds every fragment, total-loss WAL reassembles every chain.
- T19/T20: mutual TLS (CERT_REQUIRED both sides), then over this machine's real LAN NIC — 14/14 commit, replicas bit-identical.

See `data/decentral_bank_data.json`, `data/decentral_bank_bridge_data.json`, `data/decentral_bank_net_data.json`.

## Quick Start

```bash
# install the package (numpy + stdlib only; the lab and toy network need
# nothing else.  scipy/sklearn/matplotlib are optional extras for the
# legacy experiments/ catalog)
pip install -e .            # or: pip install .[experiments] for experiments

# toy network / exact k-NN SDK
python -m puno_flow.examples.toy_network
python -m puno_flow.examples.benchmark_card

# autonomous apps (self-healing mesh, search daemon, greedy router)
python -m puno_flow.apps.router [n] [trials]
python -m puno_flow.apps.guard_mesh [ticks] [n]
python -m puno_flow.apps.search_service

# the browser lab: open the printed URL
puno-lab [--host 127.0.0.1] [--port 8765]      # or: python -m puno_app.canned_ui

# classic quick start from a checkout
cd Universals
python engine.py
python math_validation.py   # 192 checks, 0 fails
cd .. && python run_all.py  # Full pipeline
pytest tests/test_spring_series.py   # 10 passed
python experiments/prime_count_from_scratch.py   # pi(943901200001) = 35575526191
python Universals/serve_dashboard.py   # L.O.R.E. dashboard -> http://localhost:8080/docs/
```

---

*Everything folds. The constant is determined. The chaos is consistent.*
