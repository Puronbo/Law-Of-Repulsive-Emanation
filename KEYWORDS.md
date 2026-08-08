# Keywords / Search Index

Find where a topic lives in this repo, even when the term does not appear in a
file name. Grep for a term here first, then jump to the listed file(s).

Usage: `grep -i "basketball" KEYWORDS.md` or just search this file.

---

## A–Z

- **ADC / analog-to-digital / quantization noise / oversampling / SNR** — `docs/papers/adc_quantization_invariance.tex` (+ `.pdf`)
- **Archimedean spiral / arc length / golden-ratio closure / 0.6138** — `experiments/fold_golden_closure.py`, `data/fold_golden_closure_data.json`, `docs/SPRING_BIBLE.md`
- **Active learning** — `experiments/flow_active_learning.py`
- **Anomaly detection / novelty / impersonation** — `docs/AUDIT.md`, `docs/THE_BOOK.md`, `experiments/decentral_net_anomaly.py`, `Universals/engine.py`
- **Audio clipping / harmonic distortion / diode rectifier** — `docs/papers/relu_analog_digital_systems.tex` (+ `.pdf`)
- **Automorphic forms / modular forms / L-functions / SL(2,Z)** — `docs/PAPER.md`, `Universals/modular_forms.py`, `Universals/mersenne_taxonomy.py`
- **Balance / self-balancing dynamics** — `puno_flow/engine.py`, `experiments/balance_auto.py`, `balance_continual.py`, `balance_scale.py`, `balance_survey.py`, `self_balancing.py`
- **Basketball / streaks / hot-hand fallacy** — `docs/papers/hot_hand_fallacy_reversal.pdf`
- **Bekenstein bound / holographic entropy / saturation** — `docs/PAPER.md`, `data/bekenstein_shift_data.json` (claim withdrawn; see `docs/AUDIT.md`), `experiments/bekenstein_rerun.py`, `data/bekenstein_rerun_data.json` (n=100: raw shift significant but positional — index-matched control erases it)
- **Black-Scholes / options / finance / stock splits** — `docs/papers/info_theory_compression_finance_invariance.tex` (+ `.pdf`)
- **Brownian motion / random walks / diffusive scaling** — `docs/papers/physics_applied_math_invariance.tex` (+ `.pdf`)
- **Buckingham Pi theorem / dimensional analysis / units** — `docs/papers/physics_applied_math_invariance.tex` (+ `.pdf`)
- **Byzantine / consensus / quorum / majority honesty (not BFT)** — `docs/papers/decentralized_protocol_proofs.tex` (+ `.pdf`), `docs/AUDIT.md`, `data/decentral_bank_data.json`
- **C0 / L.O.R.E. / constant of integration / antiderivative** — `README.md`, `docs/PAPER.md`, `Universals/c0_law_data.json`, `Universals/inverse_solver.py`
- **Chaos / consistent chaos / C(f) index / T19** — `docs/PAPER.md`, `Universals/chaos_order_benchmark.py`, `flow_chaos.py`, `divisor_chaos.py`
- **Chemical equilibrium / pH / titration** — `docs/papers/critical_points_damping_phase_ph.tex` (+ `.pdf`)
- **Clock test / calendar re-indexing / law-ness** — `docs/THE_BOOK.md`, `experiments/clock_test.py`, `rotation_test.py`, `data/clock_test_data.json`
- **Compression / rate-distortion / Shannon entropy / data-processing inequality** — `docs/papers/info_theory_compression_finance_invariance.tex` (+ `.pdf`)
- **Conformal time / cosmic expansion / light cone / FRW metric / big bang** — `docs/papers/conformal_time_light_cone_invariance.tex` (+ `.pdf`), `docs/papers/division_by_zero_bounce.tex` (+ `.pdf`)
- **Continuum limit / drift / first-order convergence / dt → 0** — `experiments/continuum_limit.py`, `data/continuum_limit_drift.json`
- **Consensus / ledger / double-entry / double-spend / nonce / WAL** — `docs/AUDIT.md`, `puno_flow/ledger.py`, `experiments/decentral_bank*.py`, `data/decentral_bank*.json`, `patents/PUNO-PPA-003_fragment_bank.md`
- **Content addressing / hashing / collision resistance / Kademlia / XOR routing / DHT** — `docs/papers/decentralized_protocol_proofs.tex` (+ `.pdf`)
- **Cosine similarity / embeddings / search / nearest-centroid** — `docs/papers/ml_quantization_embedding_proofs.tex` (+ `.pdf`), `docs/DECENTRAL_NET.md`
- **Crease / fold / ReLU / softplus / GELU / decision boundary** — `docs/THE_BOOK.md`, `docs/AUDIT.md`, `Universals/crease_metrics.py`, `fold_visual.py`, `data/crease_data.json`, `patents/PUNO-PPA-002_crease_diagnostics.md`
- **Crease pruning / pruning / subgradient selection** — `Universals/exp_pruning.py`, `exp1*.py`, `data/exp_pruning_results.json`
- **Critical damping / oscillation boundary / second-order systems** — `docs/papers/critical_points_damping_phase_ph.tex` (+ `.pdf`)
- **Critical phenomena / phase transitions / magnetization / mean field / Tc** — `docs/papers/critical_points_damping_phase_ph.tex` (+ `.pdf`)
- **Cronbach alpha / IRT / item response theory / psychometrics / reliability** — `docs/papers/psychometrics_invariance.tex` (+ `.pdf`)
- **Cut locus / viscosity solution / eikonal equation / retrace** — `docs/PAPER.md`, `experiments/eikonal_fold.py`, `retrace_boundary.py`, `data/eikonal_fold_data.json`, `data/retrace_boundary_data.json`
- **Dashboard / serve** — `Universals/serve_dashboard.py`, `docs/index.html`
- **Decentral Bank / value-carrying fragments / ownership routing** — `experiments/decentral_bank*.py`, `patents/PUNO-PPA-003_fragment_bank.md`, `data/decentral_bank*.json`
- **DecentralNet / self-healing mesh / guard mesh / router / search service** — `docs/DECENTRAL_NET.md`, `Universals/manifold/decentral_net.py`, `puno_flow/apps/`, `data/decentral_net*.json`
- **Division by zero / Riemann sphere / quantum cosmology bounce / loop quantum cosmology** — `docs/papers/division_by_zero_bounce.tex` (+ `.pdf`)
- **Divisor function / highly composite numbers / divisor chaos** — `Universals/divisor_chaos.py`, `divisor_deep.py`, `data/epoch_0d.json`
- **Econometrics / OLS / Wald test / Dagenais–Dufour / unit invariance** — `docs/papers/econometrics_invariance.tex` (+ `.pdf`)
- **Ed25519 / signatures / TLS / mutual TLS / TCP sockets** — `docs/AUDIT.md`, `experiments/decentral_bank_net.py`
- **Eikonal / fold equation / T63 / T64** — `docs/PAPER.md`, `experiments/eikonal_fold.py`, `spring_fold.py`, `data/spring_fold_data.json`
- **Embeddings / ML quantization / weight quantization / fixed-point** — `docs/papers/ml_quantization_embedding_proofs.tex` (+ `.pdf`)
- **Entropy / thermodynamics / partition function / heat capacity / second law** — `docs/PAPER.md`, `Universals/thermodynamics.py`, `data/entropy_data.json`, `data/thermo_data.json`
- **Epoch 0d / 2000-10-26 / date corpus / anchor pair** — `README.md`, `data/epoch_0d.json`, `data/epoch_0d_datescan.json`, `docs/WEAVERS_SCRIBE.md`, `docs/SPRING_BIBLE.md`
- **Evaluation heuristic / ternary scoring / pass-fail / rescaling** — `docs/papers/corrected_paper.tex` (+ `.pdf`), `corrected_paper_detailed.tex` (+ `.pdf`)
- **Fibonacci / golden ratio / golden spiral / phi** — `experiments/fibonacci_spiral.py`, `fibonacci_squares.py`, `phi_scheduler.py`, `golden_survey.py`, `fold_golden_closure.py`, `fold_ladder_phi.py`, `data/fold_ladder_phi_data.json` (C2: retrace chain is 1/4 golden rungs — NOT a chain law), `data/epoch_0d.json`
- **Finance / options / Black-Scholes / homogeneity** — `docs/papers/info_theory_compression_finance_invariance.tex` (+ `.pdf`)
- **Flat foldability / fold vertex / ReLU vertex / codimension-1** — `experiments/kawasaki_null.py`, `data/kawasaki_null_data.json`, `Universals/crease_metrics.py`
- **Fold / folding / spring fold / mirror area / origami / Kawasaki** — `docs/PAPER.md`, `docs/SPRING_BIBLE.md`, `experiments/spring_fold.py`, `fold_optimizer.py`, `fold_golden_closure.py`, `data/fold_optimizer_data.json`, `patents/PUNO-PPA-002_crease_diagnostics.md`
- **Genesis / cosmology / narrative cosmology / Physical Universal Map / PUM** — `docs/GENESIS.md`, `docs/PHYSICAL_UNIVERSAL_MAP.md`, `docs/THE_BOOK.md`
- **Googol census / 2^n−k primes / k-families** — `README.md`, `data/googol_census*.json`, `data/googol_census*.md`, `scripts/googol_census.py`
- **Ground state / quantum / eigenvalues / Laplace–Beltrami / Weyl law** — `docs/PAPER.md`, `Universals/spectral_analysis.py`, `thermodynamics.py`, `spectral_extended.py`, `data/spectral_data.json`, `data/spectral_extended_data.json`
- **Hamiltonian flow / symplectic / leapfrog / Poincare disk** — `docs/PAPER.md`, `Universals/hamiltonian_flow.py`, `Universals/manifold/poincare.py`, `data/hamiltonian_data.json`
- **Hierarchical flow / hierarchy / clustering** — `experiments/flow_hierarchical.py`, `flow_hier_incremental.py`, `flow_hier_reg*.py`
- **Hot hand / basketball / streaks** — `docs/papers/hot_hand_fallacy_reversal.pdf`
- **Hyperbolic geometry / Poincare disk / upper half-plane / geodesics** — `Universals/manifold/poincare.py`, `docs/PAPER.md`, `docs/MIGRATION*.md`
- **Impersonation / attack / adversarial** — `docs/AUDIT.md`, `experiments/decentral_net_anomaly.py`
- **Incremental / continual learning / no-forgetting** — `experiments/flow_incremental.py`, `balance_continual.py`, `decentral_net_continual.py`
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
- **Polysphere / sphere / higher-dim / routing** — `Universals/manifold/polysphere.py`, `experiments/polysphere_*.py`
- **Prime count / pi(x) / sieve / Lucy-Hedgehog / segmented sieve / PNT / Li(x)** — `README.md`, `experiments/prime_count_from_scratch.py`, `Universals/segmented_sieve_benchmark.py`, `scripts/`, `data/prime_engine_data.json`
- **Prime gaps / prime geodesics / geodesic bridge / C7 / prime geodesic theorem / PGT / finite-L / bridge extension** — `docs/PAPER.md`, `experiments/prime_gap_bridge.py`, `reverse_pair_gaps.py`, `pgt_finite_l.py`, `bridge_extension.py`, `data/googol_census_all_k_c7.*`, `data/pgt_finite_l_data.json`, `data/bridge_extension_data.json` (2ⁿ−k → arbitrary primes: trivial extension, no 2ⁿ−k-special resonance)
- **Prime-indexed time steps / prime geodesic spectrum / PAPER §8.4 / recurrence-time factorization** — `experiments/prime_time.py`, `data/prime_time_data.json` (C0-at-primes = uniform conservation; spectrum = short-transient artifact; recurrence claim unmeasurable — flow escapes disk)
- **Psychometrics / Cronbach / IRT / measurement invariance / DIF** — `docs/papers/psychometrics_invariance.tex` (+ `.pdf`)
- **Quantum thermodynamics / ground state / partition function** — `Universals/thermodynamics.py`, `data/thermo_data.json`
- **Quantization / resolution loss / bit depth / range–resolution** — `docs/papers/adc_quantization_invariance.tex` (+ `.pdf`), `ml_quantization_embedding_proofs.tex` (+ `.pdf`)
- **Rectifier / diode / audio clipping / ReLU analog** — `docs/papers/relu_analog_digital_systems.tex` (+ `.pdf`)
- **ReLU / dying ReLU / positive homogeneity / layer-rescaling symmetry** — `docs/papers/relu_invariance_dying_relu.tex` (+ `.pdf`)
- **Regularization / flow regularization / self-balancing** — `experiments/flow_regularized.py`, `flow_hier_reg*.py`
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
- **Spring fold / T63 / T64 / eikonal / fold-as-unitary** — `experiments/spring_fold.py`, `data/spring_fold_data.json`, `docs/SPRING_BIBLE.md`, `experiments/fold_unitary.py`, `data/fold_unitary_data.json` (mirror fold NOT a unitary gate: non-injective, arc length not preserved)
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
- Solvable-theorem verdicts (2026-08-08) → `data/continuum_limit_drift.json`, `data/spectral_extended_data.json`, `data/kawasaki_null_data.json`, `data/pgt_finite_l_data.json`, `data/fold_golden_closure_data.json`, `data/prime_time_data.json`, `data/time_reversal_convergence_data.json`, `data/bekenstein_rerun_data.json`, `data/wheeler_dewitt_selection_data.json`, `data/fold_unitary_data.json`, `data/kawasaki_ctc_data.json`, `data/bridge_extension_data.json`, `data/selberg_paradigm_data.json`, `data/fold_ladder_phi_data.json`
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
- Solvable-theorem experiments → `experiments/continuum_limit.py`, `experiments/spectral_extended.py`, `experiments/kawasaki_null.py`, `experiments/pgt_finite_l.py`, `experiments/fold_golden_closure.py`, `experiments/prime_time.py`, `experiments/time_reversal_convergence.py`, `experiments/bekenstein_rerun.py`, `experiments/wheeler_dewitt_selection.py`, `experiments/fold_unitary.py`, `experiments/kawasaki_ctc.py`, `experiments/bridge_extension.py`, `experiments/selberg_paradigm.py`, `experiments/fold_ladder_phi.py`
- Proofs / validation → `Universals/proofs.py`, `math_validation.py`
- Patents → `patents/PUNO-PPA-001_spatial_indexed_flow.md` (+ 002, 003)
