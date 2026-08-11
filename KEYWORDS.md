# Keywords / Search Index

Find where a topic lives in this repo, even when the term does not appear in a
file name. Grep for a term here first, then jump to the listed file(s).

Usage: `grep -i "basketball" KEYWORDS.md` or just search this file.

---

## A–Z

- **ADC / analog-to-digital / quantization noise / oversampling / SNR** — `docs/papers/adc_quantization_invariance.tex` (+ `.pdf`)
- **Archimedean spiral / arc length / golden-ratio closure / 0.6138** — `experiments/fold_golden_closure.py`, `data/fold_golden_closure_data.json`, `docs/SPRING_BIBLE.md`
- **Active learning** — `experiments/flow_active_learning.py`, `data/flow_active_learning_data.json` (margin-AL reaches 0.80/0.82 with 75/90 labels vs random 120/165; raw force-cancellation score is not the winner)
- **Anomaly detection / novelty / impersonation** — `docs/AUDIT.md`, `docs/THE_BOOK.md`, `experiments/decentral_net_anomaly.py`, `Universals/engine.py`
- **Audio clipping / harmonic distortion / diode rectifier** — `docs/papers/relu_analog_digital_systems.tex` (+ `.pdf`)
- **Automorphic forms / modular forms / L-functions / SL(2,Z)** — `docs/PAPER.md`, `Universals/modular_forms.py`, `Universals/mersenne_taxonomy.py`
- **Balance / self-balancing dynamics** — `puno_flow/engine.py`, `experiments/balance_auto.py`, `balance_continual.py`, `balance_scale.py`, `balance_survey.py`, `self_balancing.py`, `data/balance_survey_data.json` (T49: 50/50 is best shock absorber but NOT the layout optimum — PARTIAL), `data/balance_scale_data.json` (T54: scaling is a real confound A*~n^1.086 but NOT the problem; dimension-independent shell), `data/balance_continual_data.json` (T50: adaptive mu=0.5→0 schedule wins both axes; fixed balanced P5 harmful)
- **Basketball / streaks / hot-hand fallacy** — `docs/papers/hot_hand_fallacy_reversal.pdf`
- **Bekenstein bound / holographic entropy / saturation** — `docs/PAPER.md`, `data/bekenstein_shift_data.json` (claim withdrawn; see `docs/AUDIT.md`), `experiments/bekenstein_rerun.py`, `data/bekenstein_rerun_data.json` (n=100: raw shift significant but positional — index-matched control erases it)
- **Black-Scholes / options / finance / stock splits** — `docs/papers/info_theory_compression_finance_invariance.tex` (+ `.pdf`)
- **Brownian motion / random walks / diffusive scaling** — `docs/papers/physics_applied_math_invariance.tex` (+ `.pdf`)
- **Buckingham Pi theorem / dimensional analysis / units** — `docs/papers/physics_applied_math_invariance.tex` (+ `.pdf`)
- **Byzantine / consensus / quorum / majority honesty (not BFT)** — `docs/papers/decentralized_protocol_proofs.tex` (+ `.pdf`), `docs/AUDIT.md`, `data/decentral_bank_data.json`
- **C0 / L.O.R.E. / constant of integration / antiderivative** — `README.md`, `docs/PAPER.md`, `Universals/c0_law_data.json`, `Universals/inverse_solver.py`
- **Chaos / consistent chaos / C(f) index / T19** — `docs/PAPER.md`, `Universals/chaos_order_benchmark.py`, `flow_chaos.py`, `divisor_chaos.py`
- **Chemical equilibrium / pH / titration** — `docs/papers/critical_points_damping_phase_ph.tex` (+ `.pdf`)
- **Clock test / calendar re-indexing / law-ness** — `docs/THE_BOOK.md`, `experiments/clock_test.py`, `rotation_test.py`, `data/clock_test_data.json` (T59 SUPPORTED: calendar features nail the law at e0 = 1.0000 but break at e0+15 = 0.4167 — below chance, anti-correlated alignment; intrinsic mod-2/3/5/7 features survive both epochs)
- **Compression / rate-distortion / Shannon entropy / data-processing inequality** — `docs/papers/info_theory_compression_finance_invariance.tex` (+ `.pdf`)
- **Conformal time / cosmic expansion / light cone / FRW metric / big bang** — `docs/papers/conformal_time_light_cone_invariance.tex` (+ `.pdf`), `docs/papers/division_by_zero_bounce.tex` (+ `.pdf`)
- **Continuum limit / drift / first-order convergence / dt → 0** — `experiments/continuum_limit.py`, `data/continuum_limit_drift.json`
- **Consensus / ledger / double-entry / double-spend / nonce / WAL** — `docs/AUDIT.md`, `puno_flow/ledger.py`, `experiments/decentral_bank*.py`, `data/decentral_bank*.json`, `patents/PUNO-PPA-003_fragment_bank.md`
- **Content addressing / hashing / collision resistance / Kademlia / XOR routing / DHT** — `docs/papers/decentralized_protocol_proofs.tex` (+ `.pdf`)
- **Cosine similarity / embeddings / search / nearest-centroid** — `docs/papers/ml_quantization_embedding_proofs.tex` (+ `.pdf`), `docs/DECENTRAL_NET.md`; `experiments/rotation_test.py`, `data/rotation_test_data.json` (T61: rotation preserves top-8 neighbor structure exactly — overlap 1.0, sim corr 1.0, coords change 0.745; abs() relabeling drops to 0.426, 6.5x chance — 'collapse to chance' overstated)
- **Crease / fold / ReLU / softplus / GELU / decision boundary** — `docs/THE_BOOK.md`, `docs/AUDIT.md`, `Universals/crease_metrics.py`, `fold_visual.py`, `data/crease_data.json`, `patents/PUNO-PPA-002_crease_diagnostics.md`
- **Crease pruning / pruning / subgradient selection** — `Universals/exp_pruning.py`, `exp1*.py`, `data/exp_pruning_results.json`
- **Critical damping / oscillation boundary / second-order systems** — `docs/papers/critical_points_damping_phase_ph.tex` (+ `.pdf`)
- **Critical phenomena / phase transitions / magnetization / mean field / Tc** — `docs/papers/critical_points_damping_phase_ph.tex` (+ `.pdf`)
- **Cronbach alpha / IRT / item response theory / psychometrics / reliability** — `docs/papers/psychometrics_invariance.tex` (+ `.pdf`)
- **Cut locus / viscosity solution / eikonal equation / retrace** — `docs/PAPER.md`, `experiments/eikonal_fold.py`, `retrace_boundary.py`, `data/eikonal_fold_data.json` (T63 SUPPORTED, derived: mirror fold = unique viscosity solution of |r′|=a, cut locus EXACT), `data/retrace_boundary_data.json` (T64 SUPPORTED: retrace NOT assumed — infinite weak solutions, viscosity uniquely selects the tent, upwind from a zig-zag seed converges, switch point = cut locus EXACT)
- **Dashboard / serve** — `Universals/serve_dashboard.py`, `docs/index.html`
- **Decentral Bank / value-carrying fragments / ownership routing** — `experiments/decentral_bank*.py`, `patents/PUNO-PPA-003_fragment_bank.md`, `data/decentral_bank*.json`
- **DecentralNet / self-healing mesh / guard mesh / router / search service** — `docs/DECENTRAL_NET.md`, `Universals/manifold/decentral_net.py`, `puno_flow/apps/`, `data/decentral_net*.json`, `data/decentral_net_data.json`, `data/decentral_net_mnist_data.json`, `data/decentral_net_continual_data.json`, `data/decentral_net_ceiling_data.json` (T55c SUPPORTED: local-only balance ~free or better on old-routing — banner ABS-SC final_old 0.913 vs centralized 0.870, final_all 0.843 vs 0.853; shell EMERGES from local rules but needs the private home tether — without it collapses to rim 0.57→0.85 at mu0=0.12; self-heals with no repair unit — 50% loss spacing spread 0.16→0.11, regrown 0.917 vs 0.877; MNIST no collapse, ABS-SC 0.813 > FIB 0.647; spacing gate never fired on clean stream), `data/decentral_net_mnist_data.json` (T55d real 64D MNIST SUPPORTED: local-settle 0.810 vs nearest-centroid 0.817; kill 3/10 keeps 0.834, heal spacing 0.562→0.854 routing 0.822; regrow full net 0.767), `data/decentral_net_continual_data.json` (T55e continual local reflow NOT SUPPORTED for routing: ADD old 0.805 vs CONTROL 0.863, all 0.647 vs 0.671 — homes ARE the centroids; MIX collapses old 0.061/all 0.305 — never mix frames; tether NOT dimension-independent — mu0=0.12 over-drifts in 64D 0.49, no mu0 beats CONTROL), `data/decentral_net_ceiling_data.json` (T55h flow ceiling SUPPORTED measured: ms/step n^1.76 → exponent ~2.06 past 5k, 66/1230/25422 ms/step at 1k/5k/20k; peak WS 22.6 GB at n=20k vs D=3.2 GB; ceiling ~2×10^4 on 31.7 GB — beyond needs O(1) spatial search, T67)
- **Division by zero / Riemann sphere / quantum cosmology bounce / loop quantum cosmology** — `docs/papers/division_by_zero_bounce.tex` (+ `.pdf`)
- **Divisor function / highly composite numbers / divisor chaos** — `Universals/divisor_chaos.py`, `divisor_deep.py`, `data/epoch_0d.json`
- **Econometrics / OLS / Wald test / Dagenais–Dufour / unit invariance** — `docs/papers/econometrics_invariance.tex` (+ `.pdf`)
- **Ed25519 / signatures / TLS / mutual TLS / TCP sockets** — `docs/AUDIT.md`, `experiments/decentral_bank_net.py`
- **Eikonal / fold equation / T63 / T64** — `docs/PAPER.md`, `experiments/eikonal_fold.py`, `spring_fold.py`, `data/eikonal_fold_data.json` (T63 SUPPORTED, derived: unique viscosity solution of |r′|=a with C0 at both ends converges to the exact tent — mirror fold derived, cut locus EXACT, mirror area 2a²TH³/6 EXACT), `data/spring_fold_data.json`
- **Embeddings / ML quantization / weight quantization / fixed-point** — `docs/papers/ml_quantization_embedding_proofs.tex` (+ `.pdf`)
- **Entropy / thermodynamics / partition function / heat capacity / second law** — `docs/PAPER.md`, `Universals/thermodynamics.py`, `data/entropy_data.json`, `data/thermo_data.json`
- **Epoch 0d / 2000-10-26 / date corpus / anchor pair** — `README.md`, `data/epoch_0d.json`, `data/epoch_0d_datescan.json`, `docs/WEAVERS_SCRIBE.md`, `docs/SPRING_BIBLE.md`
- **Evaluation heuristic / ternary scoring / pass-fail / rescaling** — `docs/papers/corrected_paper.tex` (+ `.pdf`), `corrected_paper_detailed.tex` (+ `.pdf`)
- **Fibonacci / golden ratio / golden spiral / phi** — `experiments/fibonacci_spiral.py`, `fibonacci_squares.py`, `phi_scheduler.py`, `fib_stream.py`, `golden_survey.py`, `fold_golden_closure.py`, `fold_ladder_phi.py`, `van_iterson.py`, `data/fold_ladder_phi_data.json` (C2: retrace chain is 1/4 golden rungs — NOT a chain law), `data/golden_survey_data.json` (phi EXACT in cusp metric; static C0 packing has no golden structure; gap-filling does NOT lock onto golden angle), `data/fib_stream_data.json` (T52: Fibonacci-sized stream is steady; AD_phi beats P0 on both axes in all 3 seeds; golden insertion washes out; ring-packing min_d law, no golden signature), `data/van_iterson_data.json` (T48a: NO golden locking in any continuous C0 rule — divergence 170–200°, r~n^0.4–0.5; locking needs the insertion/contact constraint), `data/fibonacci_spiral_data.json` (REFUTED: fib-on-disk turns 42.1°/29.2° vs golden 137.5°, pseudo-energy drift 1.00/11.81), `data/fibonacci_squares_data.json` (REFUTED frictionless claim: 90° turning is construction artifact, drift 0.96, escapes disk r 1.117, T-sym 0.99), `data/phi_scheduler_data.json` (T53 SUPPORTED w/ caveat: FIB batching most robust on disk layouts — stream-old 0.912, final-old 0.910, ~2.25 buffer; FIB+ABS buys final_all at old-routing cost; P5 fixed mu=0.5 never usable; on MNIST scheduling NOT needed — NAIVE 0.953 > FIB 0.907 > FIB+ABS 0.887, geometry-regime tool), `data/epoch_0d.json`
- **Finance / options / Black-Scholes / homogeneity** — `docs/papers/info_theory_compression_finance_invariance.tex` (+ `.pdf`)
- **Flat foldability / fold vertex / ReLU vertex / codimension-1** — `experiments/kawasaki_null.py`, `data/kawasaki_null_data.json`, `Universals/crease_metrics.py`
- **Fold / folding / spring fold / mirror area / origami / Kawasaki** — `docs/PAPER.md`, `docs/SPRING_BIBLE.md`, `experiments/spring_fold.py`, `fold_optimizer.py`, `fold_golden_closure.py`, `data/fold_optimizer_data.json` (T60 SUPPORTED: Hamiltonian = retrace fold conserves and recurs but never locks; damped = mirror fold collapses and locks at the minimum — the ring lock; drift 3.9e-3 bounded, area 0.9921 vs ~0), `patents/PUNO-PPA-002_crease_diagnostics.md`
- **Genesis / cosmology / narrative cosmology / Physical Universal Map / PUM** — `docs/GENESIS.md`, `docs/PHYSICAL_UNIVERSAL_MAP.md`, `docs/THE_BOOK.md`; T65 §10.1 four-pack tested in `experiments/t65_fourpack.py`, `data/t65_fourpack_results.json` (MIXED, mostly REFUTED: P1 τ = 1.4272 identical across all curiosity_drive — corr NaN, knob inert; P2 ascent err 1.79–1.82, T-symmetry fails; P3 MI 0.034 vs null 0.009 clears chance but single coord already = 1.0, not holographic; P4 converged fraction 0.0, no fixed point)
- **Googol census / 2^n−k primes / k-families** — `README.md`, `data/googol_census*.json`, `data/googol_census*.md`, `scripts/googol_census.py`
- **Ground state / quantum / eigenvalues / Laplace–Beltrami / Weyl law** — `docs/PAPER.md`, `Universals/spectral_analysis.py`, `thermodynamics.py`, `spectral_extended.py`, `data/spectral_data.json`, `data/spectral_extended_data.json`
- **Hamiltonian flow / symplectic / leapfrog / Poincare disk** — `docs/PAPER.md`, `Universals/hamiltonian_flow.py`, `Universals/manifold/poincare.py`, `experiments/hamiltonian_routing.py`, `data/hamiltonian_data.json`, `data/hamiltonian_routing_data.json` (C0 flow separates centroid anchors for routing: mean pair dist 0.180→1.143, routing 0.420→0.765, nearest-centroid reaches the oracle 0.909; min pair dist barely moves, flow is not the ceiling; C0 geodesic Poincare-vs-cusp comparison in `experiments/metric_comparison.py`, `data/metric_comparison_data.json` is REFUTED — both blow up numerically from a "stable" start, Poincare goes NaN, cusp escapes to ~2e13; `experiments/c0_crossing_tsym.py`, `data/c0_crossing_tsym_data.json` is a CAVEAT — T-sym holds (err 0.066-0.226) but no run actually crossed the C0 origin; `experiments/c0_cusp_flow.py`, `data/c0_cusp_flow_data.json` is REFUTED — cusp C0 geodesic blows up at dt=0.005/5000 steps, Poincare NaN, cusp escapes to ~2.7e23)
- **Hierarchical flow / hierarchy / clustering** — `experiments/flow_hierarchical.py`, `flow_hier_incremental.py`, `flow_hier_reg*.py`, `data/flow_hierarchical_data.json` (SUPPORTED: 2-level C0 flow matches flat 30-anchor routing with 6 comparisons/level instead of 30)
- **Hot hand / basketball / streaks** — `docs/papers/hot_hand_fallacy_reversal.pdf`
- **Hyperbolic geometry / Poincare disk / upper half-plane / geodesics** — `Universals/manifold/poincare.py`, `docs/PAPER.md`, `docs/MIGRATION*.md`; cusp metric isometry w=log(q) verified exactly in `experiments/t39_cusp_flow.py`, `data/t39_cusp_flow_data.json` (SUPPORTED: energy CV 3e-15, step ratio = phi exactly, w-plane R² = 1.0, T-sym err 0)
- **Impersonation / attack / adversarial** — `docs/AUDIT.md`, `experiments/decentral_net_anomaly.py`
- **Incremental / continual learning / no-forgetting** — `experiments/flow_incremental.py`, `flow_hier_incremental.py`, `balance_continual.py`, `decentral_net_continual.py`, `data/flow_incremental_data.json` (reflow buys separation min_d 0.49–0.80 vs 0.25–0.54 but NOT routing; random-add matches/beats — MIXED), `data/flow_hier_incremental_data.json` (hier + incremental growth preserves old-class routing 0.892 vs 0.840, no forgetting; hier beats flat; coarse reflow = pure translation — SUPPORTED), `data/balance_continual_data.json` (T50: adaptive mu=0.5→0 wins)
- **Information theory / entropy / compression** — `docs/papers/info_theory_compression_finance_invariance.tex` (+ `.pdf`)
- **Internet / whole-internet flow / Cisco Umbrella / Majestic / T72** — `README.md`, `experiments/decentral_net_internet.py`, `decentral_net_t72.py`, `data/decentral_net_t72_data.json`
- **Kawasaki / flat foldability / crease / point-cloud artifact / CTC constraint** — `docs/PAPER.md`, `Universals/crease_metrics.py`, `experiments/kawasaki_null.py`, `data/kawasaki_null_data.json`, `experiments/kawasaki_ctc.py`, `data/kawasaki_ctc_data.json` (not a CTC/Novikov constraint)
- **k-NN / nearest neighbor / exact index / grid / Chebyshev ring / cKDTree / T67** — `puno_flow/index.py`, `verify.py`, `patents/PUNO-PPA-001_spatial_indexed_flow.md`, `docs/AUDIT.md`, `data/decentral_net_t67_data.json`
- **L-function / zeta / Dirichlet series / theta function / Euler product** — `docs/PAPER.md`, `Universals/modular_forms.py`, `mersenne_taxonomy.py`, `data/modular_data.json`
- **Ledger / blockchain-inspired / hash chain** — `puno_flow/ledger.py`, `experiments/decentral_bank*.py`
- **Mersenne primes / 2^n−1 / 2^n−k / M52 / 5630** — `Universals/mersenne_gaps.py`, `mersenne_congruence.py`, `mersenne_taxonomy.py`, `data/mersenne_*.json`
- **MNIST / digits** — `experiments/decentral_net_mnist.py`, `polysphere_mnist.py`
- **Modular group / PSL(2,Z) / Cayley transform / elliptic point** — `docs/PAPER.md`, `Universals/modular_forms.py`
- **Morse theory / energy landscape / potential V(q) / fixed points** — `Universals/energy_landscape.py`, `data/landscape_data.json`
- **Noether / conserved charge / time-translation symmetry** — `docs/PAPER.md`, `Universals/noether_analysis.py`, `data/noether_data.json`
- **Novelty / creation metrics / novelty engine** — `docs/NOVELTY_AND_CREATION.md`, `docs/AUDIT.md`, `Universals/engine.py`
- **OOD / out-of-distribution / detection / MSP baseline** — `Universals/demo_ood.py`, `data/exp_ood_results.json`
- **Oversampling / OSR / ADC** — `docs/papers/adc_quantization_invariance.tex` (+ `.pdf`)
- **Patent / PPA / provisional application / prior art / expired patents** — `patents/PUNO-PPA-001_spatial_indexed_flow.md`, `PUNO-PPA-002_crease_diagnostics.md`, `PUNO-PPA-003_fragment_bank.md`, `EXPIRED_PATENTS.md`, `docs/US7284987B2_ANALYSIS.md`
- **Pentagonal numbers / Pascal triangle / numerological corpus** — `docs/WEAVERS_SCRIBE.md`, `data/epoch_0d.json`
- **Photon / rubber ball / photon dynamics** — `experiments/photon_rubber_ball.py`, `data/photon_rubber_ball_data.json`
- **Polysphere / sphere / higher-dim / routing** — `Universals/manifold/polysphere.py`, `experiments/polysphere_*.py`, `data/polysphere_extensions_data.json` (NOT SUPPORTED: learned truths don't reproduce routing 0.483 vs 1.000; S^2 repulsion collapses separation 16.76x → 1.21x; batch routing/anomaly gap at scale DO hold), `data/polysphere_use_cases_data.json` (classifier/anomaly/generator/continual hold at batch level — batch acc 1.000, anomaly gap 0.728; per-point weak 0.653; separation score not bit-reproducible)
- **Prime count / pi(x) / sieve / Lucy-Hedgehog / segmented sieve / PNT / Li(x)** — `README.md`, `experiments/prime_count_from_scratch.py`, `Universals/segmented_sieve_benchmark.py`, `scripts/`, `data/prime_engine_data.json` (T62 SUPPORTED: pi exact at every chain point, pi(943901200001)=35575526191, endpoint prime, next gap 8; corrections — true gap below is 24 not 1, window max gap 176 exceeds its own 40–100 note)
- **Prime gaps / prime geodesics / geodesic bridge / C7 / prime geodesic theorem / PGT / finite-L / bridge extension** — `docs/PAPER.md`, `experiments/prime_gap_bridge.py`, `reverse_pair_gaps.py`, `pgt_finite_l.py`, `bridge_extension.py`, `data/googol_census_all_k_c7.*`, `data/pgt_finite_l_data.json`, `data/bridge_extension_data.json` (2ⁿ−k → arbitrary primes: trivial extension, no 2ⁿ−k-special resonance), `data/reverse_pair_gaps_data.json` (T57: 10262↔26102 NOT a reversal pair — reverse(10262)=26201; 80-multiple + 11-sums hold but are plain arithmetic)
- **Prime-indexed time steps / prime geodesic spectrum / PAPER §8.4 / recurrence-time factorization** — `experiments/prime_time.py`, `data/prime_time_data.json` (C0-at-primes = uniform conservation; spectrum = short-transient artifact; recurrence claim unmeasurable — flow escapes disk)
- **Psychometrics / Cronbach / IRT / measurement invariance / DIF** — `docs/papers/psychometrics_invariance.tex` (+ `.pdf`)
- **Quantum thermodynamics / ground state / partition function** — `Universals/thermodynamics.py`, `data/thermo_data.json`
- **Quantization / resolution loss / bit depth / range–resolution** — `docs/papers/adc_quantization_invariance.tex` (+ `.pdf`), `ml_quantization_embedding_proofs.tex` (+ `.pdf`)
- **Rectifier / diode / audio clipping / ReLU analog** — `docs/papers/relu_analog_digital_systems.tex` (+ `.pdf`)
- **ReLU / dying ReLU / positive homogeneity / layer-rescaling symmetry** — `docs/papers/relu_invariance_dying_relu.tex` (+ `.pdf`)
- **Regularization / flow regularization / self-balancing** — `experiments/flow_regularized.py`, `flow_hier_reg*.py`, `data/flow_regularized_data.json` (SUPPORTED w/ narrow-window caveat: λ=0.007 lifts routing 0.900→0.930 with acc 0.905 and sep 1.59x kept, but sweep is non-monotonic 0.003:+0.01/0.005:−0.02/0.007:+0.03/0.01:−0.07/0.015:+0.00, larger λ clearly hurts), `data/flow_hier_reg_data.json` (T48b NOT SUPPORTED for stability: flow-REG drift 6.616 rel 0.686 vs baseline 6.549 rel 0.647, flat routing worse all 0.805 vs 0.885 / old 0.873 vs 0.973; only hier routing better 0.790 vs 0.765), `data/flow_hier_reg_scaled_data.json` (T55b n-scaling via T54 A* law NOT SUPPORTED materially: drift 6.5048 rel 0.644 → NSCAL 6.4636 rel 0.640 / LIN 6.4573 rel 0.640, ≤0.7% gain; all other metrics identical to 3 dp), `data/balance_auto_data.json` (T51 autonomous regime switch NOT SUPPORTED: burst detector fires only on explosive events but AD ≈ P0 on routing — MNIST old 0.990 vs 1.000 / all 0.975 vs 0.985, disp 1.816 vs 1.828; P5 constant-mu decisively worse; on real MNIST the reflow policy is nearly irrelevant, all routes ≥ 0.94), `data/self_balancing_data.json` (T55a self-balancing router SUPPORTED in the geometry regime: coherence gate fires in a trapped core — COH skips absorb, lands exactly on P0 old 0.900/all 0.860, disp 0.513; all-routing gain survives on clean stream COH final_all 0.850 vs P0 0.770 but seed-42 old 0.810 < ABS-SC 0.930; MNIST part4 COH 0.873 < FIB 0.940; coherence = shell-thickness signal not general crowding), `data/polysphere_mnist_data.json` (real MNIST SUPPORTED: batch routing 0.890 vs chance 0.100; anomaly gap 0.663 (in 0.877 vs OOD 0.214); hierarchical end-to-end 0.753 vs chance ~0.111; active learning flags unknowns 60%, final 10/10 = 1.000), `data/polysphere_nnflow_viz_data.json` (NN-truths / S²-flow / viz PARTIAL: learnable truths 0.880 vs chance 0.100 SUPPORTED; S² Hamiltonian flow NOT SUPPORTED — silhouette ~0.0, 3–4/6 self-route at low conf, repulsion destroys centroid structure (run-to-run variance, unseeded draw, verdict robust); viz distribution tracks true fractions within ~1–3 pts)
- **Rescaling invariance / scale invariance / unit invariance / homogeneity** — `docs/papers/physics_applied_math_invariance.tex` (+ `.pdf`), plus the whole `*_invariance` family of papers in `docs/papers/`
- **Riemann zeta / zeta function / special values / zeta regularization** — `docs/PAPER.md`, `Universals/modular_forms.py`, `puno_flow/topology.py`
- **Rotation test / T61** — `experiments/rotation_test.py`, `data/rotation_test_data.json`
- **Scale-free networks / power law / Barabasi–Albert / log-log fit / Broido–Clauset** — `docs/papers/scale_free_network_controversy.tex`, `docs/papers/scale_free_update_correction.pdf`, `puno_flow/topology.py`, `tests/test_topology.py`
- **Selberg / trace formula / unification / spectral geometry / paradigm** — `docs/PAPER.md`, `Universals/selberg_unification.py`, `data/selberg_unification_data.json`, `experiments/selberg_paradigm.py`, `data/selberg_paradigm_data.json` (100 modes: Poisson not GOE; no zero correspondence; no trace-formula peaks — not a concrete Selberg instance)
- **Self-balancing / gossip / mesh** — `puno_flow/apps/`, `experiments/self_balancing.py`
- **Shannon entropy / information** — `docs/papers/info_theory_compression_finance_invariance.tex` (+ `.pdf`)
- **Spatial index / spatial search / O(1) search / grid index** — `puno_flow/index.py`, `patents/PUNO-PPA-001_spatial_indexed_flow.md`, `docs/AUDIT.md`, `experiments/decentral_net_t67.py`
- **Spectral geometry / spectrum / eigenvalues / Erdos-Kac / multiplicative chaos** — `Universals/spectrum_analysis.py`, `spectrum_extended.py`, `spectral_analysis.py`, `continuous_spectrum.py`, `data/spectral_data.json`
- **Spectrum statistics / level spacing / Poisson / GOE / C1 / C3 / C4** — `experiments/spectral_extended.py`, `data/spectral_extended_data.json`, `Universals/spectral_analysis.py`
- **Spring fold / T63 / T64 / eikonal / fold-as-unitary** — `experiments/spring_fold.py`, `data/spring_fold_data.json`, `docs/SPRING_BIBLE.md`, `experiments/fold_unitary.py`, `data/fold_unitary_data.json` (mirror fold NOT a unitary gate: non-injective, arc length not preserved) `data/spring_fold_data.json` (T58 SUPPORTED by construction: mirror-fold area = 2a²TH³/6 EXACT, self-crosses at TH−π; retrace fold closes EXACTLY to C0 with crease π; golden fold ratio = φ EXACT but does NOT close to C0 — error 12.3, closes to golden remainder 0.614·apex; overcoil fold tucks end under start into a closed ring)
- **T-series / theorems / T1–T72** — `docs/THE_BOOK.md`, `docs/AUDIT.md`, `docs/NOVELTY_AND_CREATION.md`, `Universals/proofs.py`
- **T-symmetry / time reversal / energy conservation** — `experiments/c0_crossing_tsym.py`, `c0_cusp_flow.py`, `t39_cusp_flow.py`, `experiments/time_reversal_convergence.py` (PAPER's 0.003 = dt-dependent integrator bound, superconverges O(dt^6.9)), `data/time_reversal_convergence_data.json`
- **Ternary evaluation / scoring heuristic** — `docs/papers/corrected_paper.tex` (+ `.pdf`)
- **Thermodynamics / entropy / partition function** — `Universals/thermodynamics.py`, `data/thermo_data.json`
- **Toy network / live network / browser UI** — `puno_app/`, `puno_flow/examples/`
- **Wald test / econometrics / non-invariance** — `docs/papers/econometrics_invariance.tex` (+ `.pdf`)
- **Weyl law / eigenvalue density** — `docs/PAPER.md`, `Universals/thermodynamics.py`
- **Wheeler–DeWitt / quantum cosmology / singularity / bounce** — `docs/papers/division_by_zero_bounce.tex` (+ `.pdf`), `experiments/wheeler_dewitt_selection.py`, `data/wheeler_dewitt_selection_data.json` (constraint selects nothing: unshifted empty on conservative flow, shifted = C₀ law relabeled)

---

## Papers quick map

| Topic | Paper |
|---|---|
| ADC / quantization / oversampling | `docs/papers/adc_quantization_invariance.tex` |
| Conformal time / light cone / expansion | `docs/papers/conformal_time_light_cone_invariance.tex` |
| Ternary heuristic rescaling (corrected) | `docs/papers/corrected_paper.tex`, `corrected_paper_detailed.tex` |
| Damping / phase transitions / pH | `docs/papers/critical_points_damping_phase_ph.tex` |
| Consensus / hashing / routing / thresholds | `docs/papers/decentralized_protocol_proofs.tex` |
| Division by zero / Riemann sphere / bounce | `docs/papers/division_by_zero_bounce.tex` |
| Econometrics / OLS / Wald | `docs/papers/econometrics_invariance.tex` |
| Info theory / compression / finance | `docs/papers/info_theory_compression_finance_invariance.tex` |
| ML quantization / embeddings | `docs/papers/ml_quantization_embedding_proofs.tex` |
| Physics / dimensional analysis / power laws | `docs/papers/physics_applied_math_invariance.tex` |
| Psychometrics / IRT / reliability | `docs/papers/psychometrics_invariance.tex` |
| ReLU as rectifier / audio | `docs/papers/relu_analog_digital_systems.tex` |
| ReLU invariance / dying ReLU | `docs/papers/relu_invariance_dying_relu.tex` |
| Scale-free controversy (tex) | `docs/papers/scale_free_network_controversy.tex` |
| Scale-free update correction (PDF only) | `docs/papers/scale_free_update_correction.pdf` |
| Hot-hand fallacy reversal (PDF only) | `docs/papers/hot_hand_fallacy_reversal.pdf` |

## PDF-only papers (no .tex source)

- `docs/papers/hot_hand_fallacy_reversal.pdf` — hot-hand / basketball streaks
- `docs/papers/scale_free_update_correction.pdf` — scale-free network update

## Data map (persisted results)

- Prime counting / googol census → `data/googol_census*.json`, `data/prime_engine_data.json`
- Mersenne analysis → `data/mersenne_*.json`
- Epoch 0d corpus → `data/epoch_0d.json`, `data/epoch_0d_datescan.json`
- Clock / rotation tests → `data/clock_test_data.json`, `data/rotation_test_data.json`
- Spring fold / eikonal / retrace → `data/spring_fold_data.json`, `data/eikonal_fold_data.json`, `data/retrace_boundary_data.json`
- Solvable-theorem verdicts (2026-08-08) → `data/continuum_limit_drift.json`, `data/spectral_extended_data.json`, `data/kawasaki_null_data.json`, `data/pgt_finite_l_data.json`, `data/fold_golden_closure_data.json`, `data/prime_time_data.json`, `data/time_reversal_convergence_data.json`, `data/bekenstein_rerun_data.json`, `data/wheeler_dewitt_selection_data.json`, `data/fold_unitary_data.json`, `data/kawasaki_ctc_data.json`, `data/bridge_extension_data.json`, `data/selberg_paradigm_data.json`, `data/fold_ladder_phi_data.json`, `data/flow_hierarchical_data.json`, `data/flow_active_learning_data.json`, `data/balance_survey_data.json`, `data/balance_scale_data.json`, `data/balance_continual_data.json`, `data/polysphere_extensions_data.json`, `data/flow_incremental_data.json`, `data/flow_hier_incremental_data.json`, `data/polysphere_use_cases_data.json`, `data/polysphere_routing_data.json`, `data/golden_survey_data.json`, `data/fib_stream_data.json`, `data/hamiltonian_routing_data.json`, `data/metric_comparison_data.json`, `data/c0_crossing_tsym_data.json`, `data/c0_cusp_flow_data.json`, `data/t39_cusp_flow_data.json`, `data/van_iterson_data.json`, `data/reverse_pair_gaps_data.json`, `data/fibonacci_spiral_data.json`, `data/prime_engine_data.json`, `data/fibonacci_squares_data.json`, `data/rotation_test_data.json`, `data/clock_test_data.json`, `data/spring_fold_data.json`, `data/eikonal_fold_data.json`, `data/retrace_boundary_data.json`, `data/fold_optimizer_data.json`, `data/t65_fourpack_results.json`, `data/phi_scheduler_data.json`, `data/flow_regularized_data.json`, `data/flow_hier_reg_data.json`, `data/flow_hier_reg_scaled_data.json`, `data/balance_auto_data.json`, `data/self_balancing_data.json`, `data/polysphere_mnist_data.json`, `data/polysphere_nnflow_viz_data.json`
- Spectral / Hamiltonian / thermo → `data/spectral_data.json`, `data/hamiltonian_data.json`, `data/thermo_data.json`
- Experiments (exp1/2/3, OOD, pruning) → `data/exp*_results.json`, `data/exp_ood_results.json`
- DecentralNet / Decentral Bank → `data/decentral_net*.json`, `data/decentral_bank*.json`
- Bekenstein (withdrawn, then settled) → `data/bekenstein_shift_data.json`, `data/bekenstein_rerun_data.json`

## Code map

- Flow dynamics / PPA-001 → `puno_flow/engine.py`
- Exact index / k-NN / T67 → `puno_flow/index.py`, `verify.py`
- Ledger / hash chains → `puno_flow/ledger.py`
- Scale-free topology → `puno_flow/topology.py`
- Hyperbolic manifold → `Universals/manifold/`
- Solvable-theorem experiments → `experiments/continuum_limit.py`, `experiments/spectral_extended.py`, `experiments/kawasaki_null.py`, `experiments/pgt_finite_l.py`, `experiments/fold_golden_closure.py`, `experiments/prime_time.py`, `experiments/time_reversal_convergence.py`, `experiments/bekenstein_rerun.py`, `experiments/wheeler_dewitt_selection.py`, `experiments/fold_unitary.py`, `experiments/kawasaki_ctc.py`, `experiments/bridge_extension.py`, `experiments/selberg_paradigm.py`, `experiments/fold_ladder_phi.py`, `experiments/flow_hierarchical.py`, `experiments/flow_active_learning.py`, `experiments/balance_survey.py`, `experiments/balance_scale.py`, `experiments/balance_continual.py`, `experiments/polysphere_extensions.py`, `experiments/flow_incremental.py`, `experiments/flow_hier_incremental.py`, `experiments/polysphere_use_cases.py`, `experiments/polysphere_routing.py`, `experiments/golden_survey.py`, `experiments/fib_stream.py`, `experiments/hamiltonian_routing.py`, `experiments/metric_comparison.py`, `experiments/c0_crossing_tsym.py`, `experiments/c0_cusp_flow.py`, `experiments/t39_cusp_flow.py`, `experiments/van_iterson.py`, `experiments/reverse_pair_gaps.py`, `experiments/fibonacci_spiral.py`, `experiments/prime_count_from_scratch.py`, `experiments/fibonacci_squares.py`, `experiments/rotation_test.py`, `experiments/clock_test.py`, `experiments/spring_fold.py`, `experiments/eikonal_fold.py`, `experiments/retrace_boundary.py`, `experiments/fold_optimizer.py`, `experiments/t65_fourpack.py`, `experiments/phi_scheduler.py`, `experiments/flow_regularized.py`, `experiments/flow_hier_reg.py`, `experiments/flow_hier_reg_scaled.py`, `experiments/balance_auto.py`, `experiments/self_balancing.py`, `experiments/polysphere_mnist.py`, `experiments/polysphere_nnflow_viz.py`, `experiments/decentral_net.py`, `experiments/decentral_net_mnist.py`, `experiments/decentral_net_continual.py`, `experiments/decentral_net_ceiling.py`
- Proofs / validation → `Universals/proofs.py`, `math_validation.py`
- Patents → `patents/PUNO-PPA-001_spatial_indexed_flow.md` (+ 002, 003)
