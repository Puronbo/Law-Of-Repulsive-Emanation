# Experiments — Full Detail

Every number below was re-verified by rerun or direct read of the persisted data file. Full claim-by-claim declaration: `docs/NOVELTY_AND_CREATION.md`.

Looking for a topic? `KEYWORDS.md` maps search terms to files, including topics that don't appear in any file name.

## Verified Findings

| Finding | Result |
|---|---|
| Math-validation suite | **192 passed / 0 failed** (`Universals/math_validation.py`) |
| Regression suite | **169/169 passed** (`tests/test_solvable_theorems.py`) |
| L.O.R.E. | C0 = V(q0) = H(q0,0), 109 tests; T-symmetry error 0.003 |
| Fold theorem (T63/T64) | crease = **unique viscosity solution of \|r'\| = a**; retrace = cut locus; eikonal err 3.3e-13; measured crease 0.0350pi vs derived 0.0318pi; area 2666.6665 vs 2666.6666... |
| Clock-test canon (T59/T61) | law-ness 1.000 -> 0.417 under calendar re-index -> 1.000 under rotation; rotation overlap/sim 1.000 |
| Prime count (T62) | **pi(943,901,200,001) = 35,575,526,191** from scratch (Lucy-Hedgehog + segmented sieve); 943,901,200,001 is prime |
| Googol census (C7) | 186 primes 2^n-k < 10^100 across 15 k-families (k=3: 21, k=1: 12, k=5: 19); n_max = 332 |
| Bridge beyond 2^n-k | **RESOLVED 2026-08-08**: extends trivially (every prime p = 2^n-k uniquely); near-integer resonance 2.44% over 5.76M primes vs 2.26% matched random-integer bridge (z=19.5) and 2% uniform null |
| T67 O(1) spatial search | indexed flow **bit-identical** to all-pairs; 2D exponent 1.106 vs exact 1.925; n=100k flows at 10.35 s/step (all-pairs D = 160 GB); 10k x 128-D real domains 4.12 s/step (D = 102 GB) |
| T72 whole-internet flow | 1,914,915 sites flowed: **~449 s/step** (448,659 ms), all-pairs D = 58,670 GB; 20% kill (382,983) then heal +7.8% spacing recovery |
| T55i internet net | 1,000,000 real top-1M sites bulk-loaded, routed by nearest-centroid over real geometry, 20% outage with no repair unit, 1000-site slice flows at ~862 ms/step with spacing recovery |
| T55j internet union | two top-1M lists deduped to **1,914,915 unique widely-used sites**; holding ~2 KB/site (3.92 GB); routed; outage-survived; checkpoint reloads bit-identical |
| T55g name-space anomaly | geometry as anomaly detector vs legit population: DGA-shape novelty 90% below legit p5, near-miss impersonation 18% above legit median, blocklist overlap = necessary-but-not-sufficient |
| Decentral Bank (T68-T71) | double-entry ledger conserved exactly over 3000 txs; nonce replay rejected; quorum = majority honesty (not BFT); Ed25519 sigs verified; WAL bit-identical; 14/14 commit over real TCP sockets; mutual TLS |
| Ground states | quantum E0 = 5.843778304934855; classical conservative 24.4328733; dissipative 10.0036703 (30 eigenvalues) |
| Continuum-limit drift | **measured PASS** -- first-order convergence to zero (order 0.925-1.040) |
| Golden-ratio closure (T58) | **derived** -- r_ret/apex = 0.6137690167 = theta*/Theta solving s(theta*)/s(Theta)=1/phi^2 (delta 0.0) |
| Golden fold as chain law (C2) | **NOT SUPPORTED** -- retrace chain has 1/4 adjacent rungs within 1% of phi, phi^2; the phi^2 rung is an isolated coincidence-scale hit |
| Spectral C1/C3/C4 (100 modes) | C1 partial; C3b supported (12.2416 vs lambda(31)=12.261); C4 -> Poisson mean-r 0.372 |
| Zeta zero spectral match | **the 22,491 located zeros are GUE** -- KS 0.037, level repulsion beta = 1.64, number variance tracking GUE ensemble |
| S-function census (Littlewood) | **S(t) as quiet as the classical theory allows** -- max\|S(g_j)\| = 1 at all 653 Gram points; max\|S\|/log T = 0.164 |
| Body fold symmetry | fold is EXACT, breaking is measured, tree mirror fails by factor of 2 |
| Riemann-Siegel certifier | **648 zeros certified on Re(s)=1/2** via interval arithmetic + Turing method; NOT a proof of RH |
| de Bruijn-Newman condensation | **finite probe** -- closest certified pair merger time t_c = -0.0482; NOT a bound on Lambda |

## 0/0 Experiments (Batches 1-15)

| Experiment | Result |
|---|---|
| GRH Dirichlet L-functions | g_chi(s) = \|L(s,chi)\|/\|L(1-s,chi_bar)\| = 1 on critical line for 8 Legendre symbols |
| abc conjecture | record quality 1.630; unit triple (1,1,1) is 0/0 with removable value 1 |
| Poincare-Hopf | index = removable value of V/\|V\| at zeros; S^2 Euler characteristic = 2 |
| Riemann-Roch | l(D)-l(K-D)=0 at deg(D)=g-1 for genera 1-5 |
| BSD | L(1+eps,E) shrinks to 0 for rank 1, stabilizes for rank 0 |
| Argument principle | (1/2pi*i) integral zeta'/zeta ds = Z inside 5 rectangles; 0/0 resolved by residue |
| Atiyah-Singer | ind(D) = b0-b1+b2 = chi(M) for S^2 and T^2 |
| Gradient descent | Hessian resolves saddle 0/0; Newton escapes in 1 step; 10D saddle confirmed |
| Heat kernel trace | Tr(e^{-tLap}) -> 1 as t -> inf; removable value = 1 |
| Lefschetz fixed-point | L(id) = chi(M); 0/0 at trace of f_* on H1 |
| Gauss-Bonnet | integral K dA = 2 pi chi(M); 0/0 at zero-curvature points |
| Weyl's law | N(lambda)/lambda^{d/2} -> C_weyl; 0/0 at lambda=0 |
| Central limit theorem | phi(t) -> e^{-t^2/2}; 0/0 at (phi(t)-1)/t^2 = -1/2 |
| Banach fixed-point | contraction -> unique fixed point; 0/0 at (T(x)-x)/(x-x*) = T'(x*)-1 |
| Poisson summation | theta functional eq verified; 0/0 at s=0, removable = 0.5 |
| Rayleigh quotient | R(x) = (x^T A x)/(x^T x); 0/0 at x=0; removable = eigenvalue |
| Cauchy integral | f(z)/(z-a) at z=a is 0/0; removable = f'(a); max error 8.89e-05 |
| Noether/Landau | M = tanh(M/T); 0/0 at T_c; removable = sqrt(3) |
| Euler-Maclaurin | B(x) = x/(e^x-1); 0/0 at x=0; removable = 1 |
| Laplace method | I(n)*sqrt(n) = sqrt(pi); 0/0 at n=0; removable = sqrt(pi) |
| Wallis product | prod (2n)^2/((2n-1)(2n+1)) -> pi/2; error 3.93e-08 at N=10^7 |
| Cesaro summation | Grandi 1-1+1-1... Cesaro -> 1/2; geometric 0/0 at r=1 |
| Fermat's little theorem | (a^{p-1}-1)/(a-1) at a=1: 0/0, removable=p-1 for primes 2..47 |
| Fundamental theorem of algebra | f(z)/(z-z0)^k at z0: 0/0, removable=g(z0); max error 6e-12 |
| Pythagorean theorem | (a/c)^2+(b/c)^2 at c=0: 0/0, removable=1; 16 triples verified |
| Taylor's theorem | R_n(x)/(x-a)^{n+1} at x=a: 0/0, removable=f^{(n+1)}(a)/(n+1)!; max error 2e-13 |
| Fourier uncertainty | sigma_x . sigma_xi / (1/4pi) at f=0: 0/0, removable=1 (Gaussian bound) |
| Morse theory | f/Q at critical point: 0/0, removable for min/max, not for saddle |
| Brouwer fixed-point | (f(x)-x)/(x-x*) at x*: 0/0, removable=Df(x*)-I |
| Stokes/de Rham | boundary/surface ratio at empty boundary: 0/0, removable=1 |
| Sard's theorem | image/domain ratio at critical point: 0/0, removable=0 |
| KKT conditions | mu/g at active constraint: 0/0, removable=shadow price |
| Euler product | (1-p^{-s})^{-1}/(1-q^{-s})^{-1} at s=0: 0/0, removable=ln(q)/ln(p) |
| Picard's little theorem | entire functions omitting values: e^z omits 0 only; sin(z)/z -> 1 at 0 |
| Weil explicit formula | -zeta'/zeta = sum_p log(p)/(p^s-1): zeros count the primes |
| Poincare recurrence | eps*tau(eps) -> constant for irrational rotations; recurrence rate 0/0 |
| Prime number theorem | pi(x)*log(x)/x -> 1; pole 1/log(x) / 1/(x-1) -> 1 as x -> 1+ |
| Ising model | phase transition at T_c = 2/log(1+sqrt(2)); magnetization drops, energy = -2*sqrt(2) |
| Khintchine | Dirichlet bound holds for all convergents; golden ratio q^2*error -> 1/sqrt(5) |
| Schanuel | e^a * e^b = e^{a+b} at a=-b (0/0 removable=1); Lindemann-Weierstrass verified |
| Shannon entropy | 0*log(0) = 0/0 removable value = 0; uniform max H=ln(n); MI 0/0 at perfect/deterministic |
| Bayes theorem | posterior -> prior as P(D)->0 (0/0 removable = prior) |
| Lorenz attractor | Lyapunov exponent ~0.91 (log(1)/0 = 0/0); sum = -(sigma+1+beta) |
| Boltzmann entropy | S/ln(W)=1 (0/0 at W=1 removable=1); 0*ln(0)=0 |
| Zeta functional equation | zeta(0) = -1/2 via FE (0*inf = 0/0 removable = -1/2); trivial zeros via sin(pi*s/2)=0 |
| Wigner semicircle | GUE/GOE eigenvalue density = semicircle; edge 0/0, removable = 1/(2*pi) |
| Noether's theorem | Conserved quantities from symmetry; dL/deps = 0/0 at eps=0 removable=0 |
| Spectral gap | Gap closes at TFIM critical point h=1; Delta*L -> C (0*inf = 0/0) |
| Green's function | 1D/2D Green's functions; eigenfunction expansion converges; free-space G = -(1/(2*pi))*log(r) |
| Mobius function | mu(n) values correct; sum_{d\|n} mu(d) = [n==1]; Dirichlet series 1/zeta(s) at s=1 |
| Saddle point | Gaussian saddle converges; Stirling via Laplace; g'(x)/(x-x*) -> g''(x*) (0/0 removable) |
| Stirling's approximation | n!/Stirling -> 1; correction 1/(12n); [ratio-1]*n -> 1/12 (0*inf = 0/0) |
| Logarithmic limits 0/0 | 6 sub-exps: log(1+x)/x->1, log product->1, Stirling log->0, H_n-ln(n)->gamma, Binet F_n/phi^n->1/sqrt(5), Euler reflection z*Gamma(z)*Gamma(1-z)->1 |
| Combinatorics 0/0 | 6 sub-exps: S(n,k)/k^n->1/k!, Catalan n^(3/2)/4^n->1/sqrt(pi), binom(n,k)/n^k->1/k!, Motzkin->const, log(p(n))/sqrt(n)->pi*sqrt(2/3), derangement 1/e |
| Probability ergodic 0/0 | 6 sub-exps: Weak LLN->mu, Martingale diff=0, Birkhoff ergodic int f dmu, conditional E[X|Y]=E[X], Shannon-McMillan H(X), Kolmogorov 0-1 |
| Number theory sums 0/0 | 6 sub-exps: von Mangoldt psi(x)/x->1, totient sum->6/pi^2, Mertens->1/e^gamma, Chebyshev bias, Liouville bounded, totient sum->3/pi^2 |
| Convex variational 0/0 | 6 sub-exps: Legendre transform f*(p), Fenchel-Moreau f**=f, Poincare, Brachistochrone, Isoperimetric->1, Euler-Lagrange=0 |
| Random matrix 0/0 | 5 sub-exps: Circular law disk, Tracy-Widom TW_1, Wigner semicircle, Marchenko-Pastur, sample covariance mean=1 |

## Mertens/Prime Census

| Experiment | Result |
|---|---|
| Mertens-psi census | M(10^k) reproduced exactly; max\|M(x)\|/sqrt(x) = 0.4722 at x=2803; explicit formula verified |
| Mertens sublinear census | M(10^11..10^14) computed exactly, completing the published table; first \|M\|/sqrt(x) > 0.5 excursion at height |
| Mertens explicit formula at height | 22491 located zeros carry ~98% of M(10^14); residuals non-monotone in T |
| Chebyshev psi at height | psi truncation measurably WORSE than M's at every height; conditional convergence bites |
| S-function census | S(t) = o(log t) test uncompletable by any finite computation |

## C0 / Geodesics / Fold

| Experiment | Result |
|---|---|
| Continuum limit | drift -> 0 at first order (0.925-1.040) |
| Metric comparison | REFUTED at settings (numerical blowup) |
| C0 crossing T-sym | CAVEAT: small errors but no trajectory crossed the origin |
| C0 cusp geodesic | REFUTED at settings (same blowup as metric comparison) |
| T39 cusp isometry | **SUPPORTED (exact)**: cusp metric isometric to Euclidean; energy CV 3.06e-15 |

## Routing Flow / Balance

| Experiment | Result |
|---|---|
| Balance survey T49 | 50/50 balance best shock absorber but NOT layout optimum |
| Balance scaling T54 | scaling is a real confound but NOT the problem; shell geometry is dimension-independent |
| Balance continual T50 | adaptive mu=0.5 absorb -> mu=0 settle wins both axes every seed |
| Phi-jump scheduler T53 | FIB batching most robust on disk; scheduling NOT needed on real embeddings |
| Flow-regularized training | C0 flow regularizer at lambda=0.007 lifts routing +0.030 with test acc 0.905 |
| Hierarchical + incremental | old-class routing preserved across all growth stages; hier beats flat |

## Polysphere / DecentralNet

| Experiment | Result |
|---|---|
| Polysphere extensions | NOT SUPPORTED: learned truths don't reproduce routing |
| Polysphere routing | SUPPORTED: batch routing exact -- 180/180 identity confusion matrix |
| Polysphere on real MNIST | SUPPORTED: routing 0.890 vs chance 0.100; anomaly gap 0.663 |
| DecentralNet local net T55c | SUPPORTED: fully local net ~free or better on old-routing |
| DecentralNet on real MNIST T55d | SUPPORTED: no-dependency module routes real embeddings at 0.810 |
| DecentralNet class-incremental T55e | NOT SUPPORTED: local reflow LOSES to raw centroids |
| Flow ceiling T55h | SUPPORTED: all-pairs kNN ceiling ~2x10^4; RAM is binding wall |
| O(1) spatial search T67 | SUPPORTED: bit-identical to all-pairs; n=100k at 10.35 s/step |

## Bazaar / Web / Bank

| Experiment | Result |
|---|---|
| Bazaar hybrid | SUPPORTED (structural): 4chan anonymity + reddit memory verified as 6 structural claims |
| DecentralNet live daemon | SUPPORTED (bounded run): population never exceeds CAP; self-healing + checkpoint reload |
| Bazaar network | SUPPORTED (structural over real TCP): 4 nodes replicate, mesh feed works, standing-gated removal |
| Decentral Web T73 | SUPPORTED: content-addressed P2P web with replication, addressing, name resolution |
| Learning & Creativity T74 | SUPPORTED: acquisition curve, no-forgetting, novel-but-valid yield |
| Learning-Curve Scaling T75 | SUPPORTED: curve is a density effect; capacity saturation at C*~8 |
| Human-Trial Instrument | SUPPORTED (simulated pilot): instrument works on archetypal participants |

## Detailed Sections

### Internet-Scale Flow (T67, T72)

The DecentralNet engine's per-neuron flow is O(n^2) all-pairs. **T67** replaced it with a proven-exact spatial index (numpy grid for dim <= 3, cKDTree for dim >= 4): results are **bit-identical** to all-pairs, only the expected work is O(1). Measured: 2D exponent 1.02 vs exact 1.88; n=100k 2D at ~5 s/step where all-pairs needs a 160 GB distance matrix; 10,000 real top-1M domain embeddings at 128-D in ~2 s/step (102 GB all-pairs).

**T72** then flowed the *entire* real internet net (1,914,915 sites): **~449 s/step** where all-pairs D would be 58,670 GB; consensus spacing rises across the population; a 20% kill (382,983 sites) recovers **+7.8%** spacing after heal(1) across 1.53M survivors.

### Decentral Bank (T68-T71, T16-T20)

A value-carrying fragment bank where **routing is ownership**: hashed double-entry ledgers, nonce double-spend rejection, witness quorum, and an amount-outlier anomaly layer.

- T1-T6: deterministic routing; integrity conserved exactly (64,000 = 64,000 over 3000 txs); nonce replay rejected; quorum catches every faulty send below 40% corruption but collapses at >= 50% -- **majority honesty, not BFT**
- T7/T8: Ed25519 signatures verified at append; WAL save/load bit-identical
- T12-T18: PROPOSE->VOTE->COMMIT->NOTIFY over real TCP sockets -- 14/14 commit, bit-identical replicas
- T19/T20: mutual TLS, then over this machine's real LAN NIC -- 14/14 commit

### Decentral Web (T73)

A working content-addressed P2P "web": pages publish once and replicate to a single verifying archive shared by every node; a node can die and its pages are still served by survivors; a stateless restart resyncs bit-identical; and a near-miss name resolves to the intended page. W1-W4 all SUPPORTED over real TCP processes.

### Learning & Creativity Test (T74)

A test ascertaining two things: **LEARNED** (did it acquire the curriculum, does it persist?) and **CREATIVITY** (can it generate new-but-right content?). One rubric, two axes. L1 the acquisition curve (near-chance 0.125 -> >= 0.90), L2 no forgetting (first-taught >= 0.92), C1 novel-but-valid yield (>= 0.24), C2 novelty != creativity, C3 interior-peaked creativity landscape. All SUPPORTED.

### Learning-Curve Scaling (T75)

T74's acquisition curve is a **density effect**, not an artifact: sparse floor tracks 1/C (chance), full-exposure ceiling >= 0.90, capacity saturation at C* ~ pi * HOME_R / (2 * SIGMA) ~ 8.

### Human-Trial Instrument

The T74 human protocol made concrete and runnable: a trial package (`data/human_trial_package.json`) plus `score_participant()`, the same code that grades the machine, grading a human's recorded answers. First real human run (HT-RUN-001, 2026-08-12) archived in `data/human_trial_runs/`.

### The Universal Calendar

All known civilizations on one exact, continuous, untruncated day axis anchored at epoch_0d (2000-10-26 10:26:20.00). C0 = 24.434792 is the calendar's own unit. 14 layers; 27 tests.

### AI-Performable Professions & Text-Mandates

The 14-profession verdict: 5 Class A with zero skill-based knowledge, 2 fully-gated, 5 partial, 2 not. 21 tests.

### Packaging-Line Systems

PLC IEC 61131-3 utilities, servo control, facility air sizing, rainwater collection, standby efficiency, servo regenerative energy. Consolidated in `docs/AUTO_PACKAGING_SYSTEM.md`.
