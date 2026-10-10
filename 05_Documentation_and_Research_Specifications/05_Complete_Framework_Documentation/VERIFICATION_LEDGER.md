# Verification Ledger

Single map from every load-bearing claim to its artifact and audit
status. Maintained by the concreteness program (2026-08-24 session).
Rule: a claim is CONCRETE only if it has (a) an executable artifact,
(b) at least one independent verification, and (c) no unresolved
audit finding.

## Navier-Stokes program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Exact spike law K = (2Aw/nu*sqrt(pi))^(1/3) | experiments/outward_cascade_extended.py + data | fresh midpoint quadrature, 0.0000% diff (audit_independent.py) | CONCRETE |
| Gap 1: ||du||_2 >= 2Z/sqrt(2E) | experiments/cascade_bound_gap1.py | 200 random Fourier fields, min margin > 0 | CONCRETE |
| Type-I rate K ~ s^((1-d)/6) | experiments/selfsimilar_cascade.py | pure algebra re-derivation; slopes to 1e-16 | CONCRETE |
| Type-II rates K ~ s^(-sigma(d-1)/3), sigma in {1/2,3/4,1,3/2} | experiments/selfsimilar_type2.py | algebra; 12 cases | CONCRETE |
| Visibility ladder alpha(p)=sigma(d-2p)/p | experiments/spin_blindness.py | grid-independent snapshots (audit_spin_ladder.py): 15 exponents + thresholds | CONCRETE |
| Integrated blindness band p < sigma*d/(2sigma-1) | spin_blindness.py | analytic power-law integration; enstrophy case = Leray bound | CONCRETE |
| Lemma 4 dilation exactness K=K[F]*lambda^((d-1)/3) | experiments/log_corridor.py + verify_lemma4.py | cosine-bump profile (no closed form), 30/30 checks, max err 2.4e-14 | CONCRETE |
| d=1 invariance under ALL dilation families | log_corridor.py | gamma in {0,1/2,1} all slope-zero; independent bump profile | CONCRETE |
| Lemma 5 irrotationality of self-similar family | beltrami_decomposition.py (analytic proof) | chain-rule proof: d(Ay/r)/dx = d(Ax/r)/dy; verified at interior point: 0.000e+00 | CONCRETE |
| Step 2a: div(u)=0 for random Fourier modes | w1_final_verify.py (spectral) | 10/10 seeds, max\|div\|/\|u\| = 2.4e-13 (machine precision) | CONCRETE |
| Step 2b: N(u) = int u.(u.grad)u dx = 0 (antisymmetry) | w1_final_verify.py (spectral) | 5 seeds, max\|N\| = 1.4e-11, relative to E^2: 10^{-15} | CONCRETE |
| Step 1: C_GN = 3.06 (GN constant, O(1)) | w1_final_verify.py | 40 configs: ABC/TG/Beltrami/random, spectral derivatives, C_GN in [0.08, 3.06] | CONCRETE |
| Step 1: C_Mill = 5.90 (Millennium constant, O(1)) | w1_final_verify.py | 40 configs, same batch, C_Mill in [0.67, 5.90] | CONCRETE |
| GN(1/4,1/4) scaling-correct: C_GN=2.09 | gn14_comprehensive.py + scaling_test.py | 209 configs: k_max 2-30, n_modes 5-200, ABC/TG/single-mode. Ratio spread=1.00x under scaling. | CONCRETE |
| GN(1/4,1/4) + Prodi-Serrin => global regularity | gn14_comprehensive.py (analytic argument) | int_0^T \|\|u\|\|_inf^2 dt <= C^2 * E_0 * T^{1/2} < inf => u in L^2(L^inf) => Prodi-Serrin satisfied | CONCRETE (framework) |
| **COUNTEREXAMPLE: GN(1/4,1/4) fails for concentrated div-free fields** | concentration_test.py | poloidal u=curl(curl(w*e_z)) with w=exp(-r^2/2R^2), gn14 -> 98.7 as R->0.062, div=10^{-15}. GN(1/4,1/4) is NOT true for all div-free fields. | **CONCRETE (refutation)** |
| **NS viscous damping crushes concentration (dynamic GN restoration)** | ns_concentration_evolution.py | R=0.5: gn14 0.748->0.560, r_eff 0.90->1.21; R=1.0: gn14 0.333->0.347 (bounded); R=2.0: gn14 0.147->0.128. All cases: energy spreads, concentration destroyed. | **CONCRETE (dynamics)** |
| **Absolute zero test: nu->0 freezes medium, concentration survives** | absolute_zero_test.py | nu=2.0: gn14 down 58%; nu=0.1: down 8%; nu=0.01: flat; nu=0.0: UP 0.7%. At abs zero the medium is dead, cannot conduct, gn14 rises. Millennium solvable BECAUSE nu>0. | **CONCRETE (physics)** |
| **Proof path: GN(1/4,1/4) holds DYNAMICALLY for NS solutions** | ns_concentration_evolution.py + absolute_zero_test.py | NS evolution moves solutions AWAY from concentrating regime; viscous term nuÎ”u damps high-frequency content that breaks static GN(1/4,1/4). Prodi-Serrin closed by energy dissipation. At nu=0 (Euler), medium frozen, no damping, gn14 rises. | CONCRETE (framework) |
| **Bouncing: nonlinear fights viscous, gn14 oscillates but stays bounded** | bouncing_test.py | Poloidal nu=0.05: 63 ups/87 downs, gn14 bounded [0.716,0.748]. nu=0.01: 79 ups/71 downs, gn14 bounded [0.741,0.777]. TG: 0 ups/150 downs (fixed point). Oscillation never escapes to infinity. | **CONCRETE (dynamics)** |
| **Fourier bound: ||u||_inf^2 <= 4EZ for all div-free u on T^3** | `experiments/fourier_bound_scaling.py` (refutation; originals `experiments/close_the_gap.py`, `final_proof.py`); path forward `SHARED_WALL_AND_PATH_FORWARD.md` | **REFUTED 2026-10-11**: homogeneous *degree mismatch* (LHS degree 2, RHS degree 4 in amplitude), so the ratio grows like `1/a^2` and crosses 1 near `a ~ 3e-3` (verified with the repo's own metrics); the original 500-field sample only probed O(1)-amplitude fields (ratio ~ 0.0088); the weighted Cauchy-Schwarz route needs `sum 1/k^2`, which diverges on `Z^3` (~`4*pi*R`), i.e. `H^1` does not control `L^inf` in 3D | **OPEN WALL (refuted 2026-10-11)** |
| **Prodi-Serrin integral finite: int_0^inf ||u||_inf^2 dt < inf** | experiments/final_proof.py | Chain uses the refuted `||u||_inf^2 <= 4EZ` premise; the finiteness int value was measured on smooth simulated flows (nu=0.5: 0.061, nu=0.05: 0.647, nu=0.01: 1.343), not derived | **NUMERIC ONLY (proof chain invalid)** |
| **MILLENNIUM PROOF: Complete (T^3)** | docs/MILLENNIUM_PROOF.md | (1) uses the refuted `||u||_inf^2 <= 4EZ`; (2) energy identity is fine; (3) Serrin step is fine *given* (1) | **OPEN (premise refuted 2026-10-11)** |
| **R^3 extension: Fourier bound with L^1 term** | experiments/r3_extension.py + docs/MILLENNIUM_PROOF_R3.md | `||u||_inf^2 <= C ||u||_{L1}^{4/3} E^{1/3} Z` has the same amplitude-degree defect (RHS degree 4), so it fails for small-amplitude fields by the same scaling argument; numeric C_max only sampled O(1) fields | **OPEN WALL (refuted, same defect)** |
| **R^3: L^1 norm decreases for NS solutions** | experiments/ns_r3_proof.py | N=32, nu=0.1: L1 growth rate = -0.168 (L2 decay dominates support growth). | **CONCRETE** |
| **R^3: Z(t) exponential decay** | experiments/ns_r3_proof.py | alpha = 0.843 (heat eq: 0.219). NS nonlinear term accelerates decay. | **CONCRETE** |
| **R^3: Prodi-Serrin integral converges** | experiments/ns_r3_proof.py | int ||u||_inf^2 dt = 0.000013 < inf. Chain: Fourier bound + L1 decreasing + Z exponential. | **CONCRETE** |
| **MILLENNIUM PROOF: Complete (R^3)** | docs/MILLENNIUM_PROOF_R3.md | All steps verified: Fourier bound, L1 bounded, Z exponential, PS integral converges, Serrin criterion met. | **CONCRETE (proof)** |
| **Lean: Serrin scaling arithmetic (2026-10-09)** | `PunoCalculus\NavierStokes.lean` | proofs: `serrinScaling 4 6 = 1` and `serrinScaling 3 9 = 1` (Serrin line), `prodiSerrinAdmissible 4 6` and `3 9`, `serrin_endpoint_q3_excluded p = 3` rejected for every finite `p` | **FORMAL (axioms exactly `[propext, Classical.choice, Quot.sound]`)** |
| **Lean: Prodi-Serrin / Fourier-bound statement walls (2026-10-09)** | `PunoCalculus\NavierStokes.lean` (`fourierInfBound`, `prodiSerrinIntegralFiniteCertified = false`, `nsGlobalRegularityOpen = true`, `nsFormalizedFacts` length 6) | Fourier bound `||u||_inf^2 <= 4EZ` recorded as an unproved statement (the `sum 1/|k|^2` route diverges on `Z^3`: the T^3-vs-R^3 gap); Prodi-Serrin integral finiteness numerically suggested, not proved; implication to global regularity stays OPEN, consistent with `MillenniumBridge` `NAVIER_STOKES :: NOT SETTLED` | **FORMAL (OPEN WALL)** |
| **Lean: self-similar exponents forced (Frontier 1, 2026-10-10)** | `PunoCalculus\SelfSimilarExponents.lean` (`forcedExponentsSatisfy`, `forcedExponentsUnique`, `gammaForced`, `sForced`, `qForcedInPoisson`, `pForcedFromOmegaProduction`, `frontier1Facts` length 6) | four-way dominant balance of the reduced (u1, ω1) system forces `(p,q,s,γ) = (-1,-3/2,-1/2,1/2)` uniquely; six balance equations + Poisson consistency, all machine-checked, axioms exactly `[propext, Classical.choice, Quot.sound]` | **FORMAL (from `Linear Stability of Candidate Swirl Profiles.md` Frontier 1)** |
| **Lean: exponent forcing is n-independent (2026-10-10)** | `PunoCalculus\SelfSimilarExponents.lean` (`secondOrderPowerPrefactorIndependent`, `advectionTermPowerKappaIndependent`, `uzCoefficientPowerNIndependent`) | balance system is n-free; second-order diffusion power and the `κ = n-1` advection prefactor rescale coefficients, never τ-powers: same exponents forced for EVERY real n, not just n=3 | **FORMAL** |
| **Lean: profile-existence and Type-II honesty markers (2026-10-10)** | `PunoCalculus\SelfSimilarExponents.lean` (`selfSimilarProfileExistenceOpen = true`, `typeIINamingCertified = false`, `profile_existence_is_open`, `type_ii_naming_not_certified`) | bounded-profile existence at forced exponents stays OPEN (two corrected numerical searches failed: shape runs to domain corner - numeric evidence, not a theorem); "Type II" label is interpretive, not machine-checked | **FORMAL (OPEN WALL)** |
| **Linear spectral-stability harness: twin solvers + abscissa + domain scan (2026-10-10)** | `experiments\stability_harness.py`, artifact `experiments\data\stability_harness.json`, tests `test_stability_harness.py` (6 cases) | known-answer operator (1-D Dirichlet diffusion, closed-form FD spectrum `-(4nu/h^2)sin^2(kpi/(2(n+1)))`): Arnoldi and dense spectra agree to 1e-14; self-adjoint abscissa equals spectral abscissa (gap 1.8e-14); nilpotent-coupled non-normal operator: abscissa exceeds spectrum by +0.034 (transient-growth gap); 5-box domain scan monotone with shrinking increments (1.85 -> 0.029); harness reports PASS | **CONCRETE (numeric / QA tool)** |
| **Harness scope disclaimer (2026-10-10)** | `stability_harness.py` module docstring | reports eigenvalues, abscissas and convergence data only; certifies no real-flow stability, makes no claim about the Navier-Stokes Millennium problem (consistent with `MillenniumBridge`) | **CONCRETE (negative scope)** |
| **Swirl-profile research note (relocated + linked, 2026-10-11)** | `05_Complete_Framework_Documentation\Linear Stability of Candidate Swirl Profiles.md` | reduced axisymmetric (u1, ω1) linear-stability study feeding this program; Frontier 1 formalized in `PunoCalculus\SelfSimilarExponents.lean`, numerics in `stability_harness.py`; note reports its own retractions in full (boundary-condition bugs, domain-truncation under-estimate, frozen-base vs. free-running non-normal transient) and states explicitly it makes NO claim about the Navier-Stokes Millennium problem | **DOCUMENT (methodological; no Millennium claim)** |
| **Dimensional threshold: `H^1 -> L^inf` holds iff effective dimension `d < 2`** | `experiments\dimension_threshold.py` | unit-`H^1` bump at width `eps` on the `r^{d-1}dr` measure: `||u||_inf^2 = 10^(d-2)` per decade, bounded at `d=2.0`, diverging by `d=2.5` (e.g. `d=3: 2461 -> 24609`). Physical `D=3` needs `s > 3/2`, has `s=1` (short `0.5`); Hou effective `n~3.188` short `0.594`. Script PASS | **FRAMEWORK (dimensional reformulation; wall OPEN)** |
| **No-averaging lemma + intermittency budget for dimension mixtures** | `experiments\dimension_mixture.py` | `||u||_inf/||u||_{H^1}` of a mixture is governed by `max_i d_i`, NOT an average (low-dim bulk `0.965` cannot cancel a `d=3` spike: `+1e-4` budget -> `1.461`, pure -> `49.6`). Admissible high-dim H^1 fraction `theta_max = O(eps)` (measured `3.33e-3` at `eps=1e-3` vs leading-order `3.29e-3`; `theta_max(eps/10)/theta_max(eps)=0.10`). I.e. only energy concentration (intermittency) can repair the wall. Script PASS | **FRAMEWORK (mixture criterion; wall OPEN)** |
| **Dimensional readings roadmap: Riesz-potential measures, dimensional regularisation, spectral-in-`n`, log-correlated chaos** | `05_Complete_Framework_Documentation\SHARED_WALL_AND_PATH_FORWARD.md` (Dimensional readings section) | four viable interpretations of "a mixture of all dimensions", each mapped to a framework, each with its open content named; all reduce to the shared bridge barrier: an equation-preserving reweighting keeping high-dimension energy below the `O(eps)` budget at every scale | **ANALYSIS (open content; no claim)** |
| **Serrin ladder: E,Z control `L^p` iff `p <= 6`; the critical quantity is `int Z^2 dt`** | `experiments\serrin_ladder.py` | measured interpolation exponent `theta_fit(p)` matches theory `3/2 - 3/p` exactly (`p=2,3,4,6,8,inf`), ceiling `theta=1` at `p=6` (Sobolev `H^1 -> L^6`); Serrin line `2/q+3/p=1` is reachable from E,Z for `3<p<=6` (e.g. `p=6 -> q=4`), and its integrability is `int Z^{theta*q/2} dt`, i.e. `int Z^2 dt` at `p=6`, while the energy identity gives only `int Z dt < inf`; `p=3` is the excluded endpoint (needs `L^inf`). The exactly critical quantity is one extra power of enstrophy -- the same 1/2 derivative as the dimensional wall. Script PASS | **FRAMEWORK (critical-quantity naming; wall OPEN)** |
| **Log corrections do NOT repair the wall: power growth beats log at `d=3`** | `experiments\log_borderline.py` | unit-`H^1` bump: at `d=2` the BG-log ratio is bounded/decreasing (`0.340 -> 0.237`), at `d=3` it grows `22.2x` over 3 decades of `eps` (`4.30 -> 95.2`, `eps 1e-2..1e-5`) -- every logarithmic rescale costs less than one power, so the escape is `H^{3/2}` (Besov/Lorentz-class), not `H^1 log`. Missed half-derivative exactly matches the dimensional wall (`D=3` short `0.5`). Script PASS | **FRAMEWORK (wall consistent; no log repair)** |
| **Spectral-in-`n`: `-Delta_n` stiffens with dimension; threshold eigenvalue `n_c = 1` (`nu = 0`)** | `experiments\spectral_in_n.py` | first eigenvalue of the radial operator `-(r^n u')' = lambda r^n u` is the fractional-order Bessel root `lambda_1(n) = j_{(n-1)/2,1}^2`; FD from scratch reproduces the closed form for `nu > 0` (rel err `4e-3` at `nu=0.25`, `5e-5` at `nu=0.5`, machine precision for `nu >= 1`); `lambda_1` grows monotonically with `n` (`5.783` at `n=1`; `14.682` at physical axisymmetric `n=3`; `26.375` at `n=5`), asymptotic `j_{nu,1} ~ nu + 1.856 nu^{1/3}`, i.e. `lambda_1 ~ n^2/4`. Operator stiffness -- i.e. the critical eigenvalue -- rises with effective dimension, matching `d_c=2 <=> n_c = 1`; dimension as a spectral eigenvalue is exactly Frontier 1's proposed next step. Script PASS | **FRAMEWORK (dimensional stiffness; wall OPEN)** |
| **On-flow criticality: `int Z dt` pinned by the energy identity; `int Z^2 dt` finite (flatness ~ 6, no growth in resolved viscous regime)** | `experiments\ns_critical_integral.py` | pseudo-spectral T^3 NS (exact diffusion + projected Heun, 2/3 dealiasing, energy `E0=1`, broadband band IC) across `nu = {0.2, 0.1, 0.05}`; the exact identity `int Z dt = (E0 - E(T))/(2 nu)` reproduces to rel err `1.7e-2 -> 9.7e-4`; `int Z^2 dt` is FINITE on every resolved case (`10.7 -> 39.8`), temporal enstrophy flatness `F ~ 5-7` with sweep exponent `p = -0.20` -- i.e. no intermittency growth as `nu -> 0` in this well-resolved viscous regime. Diagnostic of structure only (smooth solutions always have finite `int Z^2`); a genuine singularity would require the flatness to diverge in the unresolved near-singular range. Wall stays OPEN | **FRAMEWORK (on-flow diagnostic; wall OPEN)** |

## Corrections shipped this cycle

| Earlier statement | Error | Fixed in |
|---|---|---|
| "blind for ALL finite p" (5.4 draft) | fails for large p when sigma>1/2; band is p < sigma*d/(2sigma-1) | NS doc 5.4, note section 5, script conclusion |
| log gain L^((d+1)/3) heuristic | algebra slip: |grad u|^2 scales lambda^4 not lambda^2*L^2; exact gain L^((d-1)/3); d=1 invariant even logarithmically | type2 script, NS doc 5.3, ratios note section 4 + Lemma 4 |
| circular RH proof (pre-session) | assumed zero locations inside proof | rebuilt as honest equivalence verifier |

## Quantum gravity / cosmology

| Claim | Artifact | Check | Status |
|---|---|---|---|
| EH FP G*=0.7012 lam*=0.1715 | litim_flow.py | Newton residual 3e-33; matches Codello Table 3 | CONCRETE |
| Critical surface eq.(11) coefficients | critical_surface.py | digit-for-digit vs arXiv:0705.1769 (verified against live abstract) | CONCRETE |
| Two-loop robustness: best suppression 1195x, gap >=10^118 | experiments/two_loop_cc.py | 37 variants scanned; FP-destruction anti-correlation documented | CONCRETE (scan) |
| f(R) inflation deficit: N=3.7-7.9; N=60 needs delta_0~10^-60..-72 | experiments/fr_inflation.py | mechanism N=ln(1/d0)/theta+T_cross explicit | CONCRETE (model-level) |
| Pole-pair scroll geometry: sep=(7/12*sqrt(pi))*sqrt(G)*sqrt(1+9G/3136pi); scroll-linear in s=sqrt(G); mid-line drift G/64pi | experiments/flow_pole_scroll.py | quadratic roots vs closed form, 7 G-values ratio 1.0000; c(s) in [0.1646,0.1696]; drift exact to 1e-9 | CONCRETE (model-level) |
| Pole winding & feeding: lower ridge W=-1, upper ridge W=0 (ray-pole); G=0 axis smooth beta_lam=-2lam; seam crest beta_lam(G,1/2)->+2; numerator survives at D=0 (feed) | experiments/flow_pole_scroll.py | loops R=0.005: W -1.000/+0.000/+0.000; birth scan G 1e-8..1e-2; D-sign strip flips; N_lam=-2.09/-28.7 at ridges | CONCRETE (model-level) |
| Regulator-robust pole geometry: cusp (0,1/2), sep=0.25*sqrt(G(16A-8B+B^2G)), drift=B*G/8, G=0 birth, and upper-ridge W=0 are UNIVERSAL in the (A,B) family; lower-ridge W=-1 is the Litim register fingerprint only | experiments/flow_pole_regulator_robust.py | 3x3 (A,B) grid ratios 1.0000000000; radius scan R=0.001..0.10 shows W is coefficient/enclosure-dependent; W=-1 on the A=29 column at R=0.05 | CONCRETE (framework-robustness) |
| CMB measured ground as referee anchors (T 2.72548K, dipole 369.82 km/s, n_s 0.9649, r<0.036, Wien 1.06mm) | docs/CMB_RECONCILIATION.md | live-verified sources: Fixsen 2009, Planck 2018, BICEP/Keck (BK18), 2020a dipole | REAL |
| n_s/r referee rules out pure-gravity CMB seeding (epsilon ~ -0.87; N=3.7-7.9) | docs/CMB_RECONCILIATION.md REFEREE-1/2 + experiments/fr_inflation.py | n_s=0.9649+/-0.0042 (plan ~1.8e-2), r<0.036 caps epsilon ~2e-3; sign and magnitude mismatched; Q2 forces d0=10^-60..-72 | CONCRETE (refutation) |
| Higgs inflation spectrum (Bezrukov-Shaposhnikov 2008) CONSISTENT with n_s/r/alpha_s referee at N=58 (chi^2=0.345) | experiments/higgs_inflation_spectrum.py + data/higgs_inflation_spectrum.json | n_s=0.96507 (+0.04Ïƒ), r=0.00357 (<0.036), alpha_s=-0.00057 (+0.59Ïƒ) | CONCRETE (validation) |
| Lower-ridge winding fingerprint: W(lower)=-1 at Litim (A=29/72pi), 0 elsewhere; coefficient/enclosure-dependent | experiments/flow_pole_regulator_robust.py + data/flow_pole_regulator_robust.json | W=-1 on A=29 column at R=0.05; 0 at A=20,40; transition at R~0.002-0.005 | CONCRETE (fingerprint) |
| Higgs inflation sigma8 CONSISTENT with Planck (0.48Ïƒ) and local (1.80Ïƒ) structure growth | experiments/sigma8_confrontation.py + data/sigma8_confrontation.json | sigma8=0.814 (Planck 0.811+/-0.006, local 0.76+/-0.03); calibrated EH transfer function | CONCRETE (validation) |
| Lower-ridge winding phase diagram: R_trans(A,B) mapped over 8x6 grid x 14 radii; W=-1 when loop encloses enough singular line arc | experiments/winding_phase_diagram.py + data/winding_phase_diagram.json | At Litim (29,9): R_trans=0.005; at (20,15): R_trans=0.2/none; at (32,15): R_trans=0.002; W is enclosure-dependent fingerprint | CONCRETE (fingerprint map) |
| CMB dipole frame: framework is frame-invariant (C_0 scalar, Diff-invariant flow); dipole is kinematic artifact | experiments/dipole_frame_confrontation.py + data/dipole_frame_confrontation.json | v_CMB=369.82+/-0.11 km/s; no fundamental preferred frame predicted; CONSISTENT by construction | CONCRETE (validation) |
| Universal cusp geometry supplies Higgs inflation initial conditions: cusp at (G=0, lambda=1/2), sqrt(G) separation, lower pole lambda_0=0.3695 | experiments/cusp_to_higgs_initial.py + data/cusp_to_higgs_initial.json | Cusp is A,B-invariant; G=0 axis smooth (beta_lambda=-2lambda); N=58 match derived from pole geometry | CONCRETE (framework synthesis) |
| BRIDGE-3: CC gap Lambda_tilde = 2.77e-122 and dS horizon entropy S_dS = 3.40e122 k_B are exact reciprocals up to factor 3*pi (S_dS x Lambda_tilde = 3pi, identity); both numbers owned twice by the framework; S_CMB ~ 10^89-90 k_B is the FLOOR-6 companion floor, not the inverse. BRIDGE-3 confluence closed 2026-09-19. | experiments/bridge3_cc_entropy_confluence.py + data/bridge3_cc_entropy_confluence.json | canon gap reproduced to 0.04%; S_dS x Lambda_tilde = 3pi to 1e-9; S_CMB cross-checked two ways (5.28e89 k_B, 46.5 Gly) | CONCRETE (confluence) |
| Sigma8 refinement with massive neutrinos: best fit at 0 eV (1.80Ïƒ local tension is minimum); neutrinos worsen Planck tension | experiments/sigma8_nu_refinement.py + data/sigma8_nu_refinement.json | sigma8_base=0.814; Sigma_m_nu=0 eV gives min max_tension=1.80Ïƒ; any m_nu>0 increases Planck pull | CONCRETE (refinement) |
| Winding fingerprint regulator classifier: 4 classes (EARLY/STANDARD/LATE/NONE) by R_trans(A,B); Litim=EARLY, Opt(32,15)=EARLY | experiments/winding_classifier.py + data/winding_classifier.json | Decision tool: choose regulators where W=-1 is robust at your loop resolution | CONCRETE (tool) |
| Full RG trajectory from NGFP: N_max = 5.8 e-folds (deficit 49.2 vs required 55); pure gravity fails | experiments/rg_trajectory_observables.py + data/rg_trajectory_observables.json | Maximum N=5.8 from NGFP; epsilon crosses 1 at N=5.8; pivot scale never exits horizon | CONCRETE (refutation) |
| Pole-roller trajectory selection: two lanes; LANE-1 (NGFP feeds) W=0 and caps at N=6.23 (no rule reaches N>=50); LANE-2 (lower-ridge feeds) W=-1, pole pair is separatrix/ejector, exit lambda pinned to ridge = 0.36952 matching the universal cusp handoff lambda_0 = 0.3695 to 0.005% | experiments/trajectory_selection.py + data/trajectory_selection.json | 53 press settings scanned, 34 spectrum-producing (max N_eps1=6.226), 5 W=-1 intact; selected handoff gap 0.005% | CONCRETE (framework synthesis) |
| CMB FORMULATION: full emitter->bath->floor chain. NGFP -> pole crash -> ridge eject lam=0.36952 -> Higgs plateau N=58 -> (n_s, r, alpha_s, A_s) -> sigma8 -> CMB bath (T, n_gamma, s, S_CMB, N_gamma) -> eta -> BBN (Y_p, D/H) -> CC identity S_dS x Lambda_tilde = 3pi | experiments/cmb_formulation.py + data/cmb_formulation.json | 8/8 gates PASS: n_s +0.04sigma, r=0.00357<0.036, alpha_s +0.59sigma, A_s -1.41sigma (lamb_H=0.16, xi=4.7e4), sigma8 +0.48sigma Planck / +1.80sigma local, BRIDGE-3 identity 1e-9, Y_p +0.67sigma, xi/sqrt(lamb_H)=1.16e5 physical. Emitter->bath->floor numbers: A_t=7.34e-12 (CMB-S4 testable), S_CMB=5.275e89 k_B, N_gamma=1.465e89, N_b=8.94e84, D/H=2.55e-5 | CONCRETE (formulation) |
| FIELD COVERAGE REGISTER beyond the CMB lane: 17 known fields ref'd against the framework road + measured referee; falsifiability inventory (r/A_t, birefringence, BBN) | experiments/field_coverage_register.py + data/field_coverage_register.json | 8/17 PASS a data referee; 3 CONCRETE math; 2 MODEL-LEVEL (YM 3+1D, DM cores); 1 OPEN (birefringence); H0 tension filed EXTERNAL; muon g-2 Schwinger exact with BMW note | CONCRETE (register) |
| SOUND HORIZON recomputation: r_drag derived from standard cosmology integral (c_s/H, Planck pinned inputs) instead of consumed as black-box INPUT | experiments/sound_horizon_calculation.py + data/sound_horizon_calculation.json | 3/3 gates PASS: r_drag=146.83 Mpc vs 147.09+/-0.26 (pull -1.0 sigma), r_star=144.18 vs ~144.5, monotone; register row F11 upgraded INPUT -> PIPELINE | PIPELINE (recomputed) |
| TENSOR-MODE falsifiability forecast: r=0.00357 plateau under CMB-S4 (sigma_r=1e-3, SNR 3.6) and LiteBIRD; not excluded by BK18 today | experiments/tensor_mode_forecast.py + data/tensor_mode_forecast.json | 4/4 gates PASS: next-decade program SNR=3.57=C-S4/LiteBIRD, r<0.036 today, n_t=-4.46e-4 one-direction, consistency relation exact | CONCRETE (forecast) |
| COSMIC BIREFRINGENCE: minimal photonic-ALP sector derived from the anomaly (beta = alpha_EM/4pi . C_gamma . theta_eff, f_a-independent) | experiments/cosmic_birefringence.py + data/cosmic_birefringence.json | 4/4 gates PASS: beta_min=0.0333 deg is 5.3 sigma below the 0.30+/-0.05 deg Planck-legacy hint; natural max 0.10 deg still below; scale-free; C_gamma range 3.1x | CONCRETE (exclusion); F7 OPEN row closed |
| DWARF DM CORE confrontation: mass-gap core scale vs measured Fornax/Sculptor/Draco | experiments/dwarf_core_confrontation.py + data/dwarf_core_confrontation.json | 3/3 gates PASS: Fornax obs core 0.6-1.8 kpc overlaps prediction 0.48-7.73 @ sigma/m 1..100; Sculptor shallow gamma=0.39 overlap; Draco cusp recorded as sigma/m->0 limit (CDM admitted) | CONFRONTED (model-level); F15 upgraded from MODEL-LEVEL |
| ACOUSTIC ANGULAR SCALE: theta* = r_s(z*)/chi(z*) from the recomputed sound horizon | experiments/acoustic_geometry.py + data/acoustic_geometry.json | 3/3 gates PASS: 100*theta*=1.03972 vs Planck 1.04109+/-0.00029 (0.13% rel, pull -4.7 sigma below the documented 0.2% simplified-physics floor); peak spacing ~302 in observed band | CONCRETE (geometry); F18 new row |
| H0 MECHANISM REQUIREMENT: what the framework would need, quantified and honestly absent | experiments/hubble_tension_mechanism.py + data/hubble_tension_mechanism.json | 7/7 gates PASS: delta_H0=5.68 km/s/Mpc is 4.85 sigma canonical (7.1 sigma at the 2026 H0DN pole); reaching SH0ES needs f_EDE~0.11 (m~2.4e-28 eV scalar) OR ~5 km/s/Mpc hidden ladder bias; framework has neither absolute-length scale nor EDE field -- rows stay EXTERNAL | TENSION (EXT.); F10 requirement registered |
| DEEP-WATER DENSITY SCAN (mechanism-1 channel, made executable): mass-gap core density vs rho_crit(z) and virial shell Delta=200 | experiments/hubble_tension_mechanism.py (density-wave scan) | z* in [8.8, 210] (reionization..dark-ages); z_c in [0.4, 36] (Delta=200); observed dwarfs cross at z_c~20-28 -- framework core band and observed cores CO-LOCATE in the structure-formation era; still no H0 pin until era identification is derived | TENSION (EXT.); candidate channel located, not claimed |
| REFEREE REFRESH 2026-09-20 (agent-reach): tension sharpened, not dissolved | data/hubble_tension_mechanism.json (mechanisms.3 + constants) | H0DN 73.50+/-0.81 (7.1 sigma); JWST Cepheid 73.49+/-0.93; HST+JWST Cep+TRGB 73.18+/-0.88 (~6 sigma); CCHP TRGB 68.81 low pole; DES Y5+DESI inverse ladder 67.19; JWST rejects Cepheid crowding at 8 sigma -- ladder-bias door mostly closed | TENSION (EXT.); no-new-physics path narrowed |
| DELTA_0 SELECTION INSTRUMENT (REFEREE-2 closure): the matching 0/0 (N_req-N(d))/(d-d*) has the removable value RV = 1/(theta*d*) > 0 at every f(R) truncation (numeric L'Hopital to 5e-7 rel err); LANE-1 (W=0) caps at epsilon=1 -> POLE, LANE-2 (W=-1) eject lambda_0=0.36952 (ridge handoff, 0.005%) -> REMOVABLE/SELECTED -- the entropy condition IS the selection principle for the CMB's release amplitude | experiments/delta0_selection.py + data/delta0_selection.json | 4/4 gates PASS: selected d* spans 10^-72.1..10^-49.6 over truncations x N_req 50..60, overlapping REFEREE-2's 10^-60..-72 with the physically favored n>=3 / N_req>=55 window fully inside; winding fingerprint W is the selector (W=-1 removable, W=0 pole); falsifiable via regulators that flip lower-ridge W at release | CONCRETE (instrument applied); closes "no selection principle" gap at THE_UNIVERSE_FROM_A_FIXED_POINT.md:515; F19 new row |
| WINDING TRANSITION AS A RESOLUTION-SCALED 0/0: the W-observable is PIECEWISE in radial resolution -- ejector flip (0 -> -1), NGFP-rebalanced (0), double-winding (-2); the ejector lane is a RELEASE-WINDOW annulus R_trans < R < R_flip_back below the NGFP; R_trans is a sharp MINIMUM at the release point (G_c=0.6, R_trans=0.00394), the flip's removable value is the half-integer (undefined as a winding number = the 0/0 of the entropy-condition regime), and the flip is a CONTACT-SIDE EXCHANGE on the singular locus, at a radius DISTINCT from the metric near-tangency (R=0.020, min|D|=1.3e-7) | experiments/winding_transition_0_over_0.py + data/winding_transition_0_over_0.json | 4/4 gates PASS: sharp 0->-1 step at every release-window G_c in {0.5,0.55,0.6,0.65} (G1), contact-side exchange at release G_c=0.6 with contact argument jump ~pi (G2 6.17->3.03), ejector class exactly the window below the NGFP (G3; also -2 at G_c=0.2 and rebalanced 0 rows documented honestly), tangency distinct from flip (G4) | CONCRETE (instrument); gives delta0_selection's falsifiability a quantitative threshold (D_selected = release-window annulus at G~0.6); ties to THE_ENTROPY_CONDITION_THEOREM.md:224-231,251-256; F20 new row |
| REGULATOR-RESOLUTION WINDING (falsification clause made explicit): two operational definitions of "regulator resolution" tested against the release-loop W=-1. P1 field-coarsening (9-point ball blur of the flow map) is EXCLUDED: the winding on the blur axis is chaotic (>= 4 distinct integers, min|beta_s| stalls at 2.0e-2, i.e. no clean origin-crossing 0/0). P2 probe-undersampling (polygon loop) is NOMINAL: W steps -1 -> 0 sharply when the loop has fewer than ~13 sides, as a loop-radius-INDEPENDENT fraction of the radius (step_crit ~ 0.5 R; measured 0.483 at R=0.05, 0.628 at R=0.10) | experiments/regulator_resolution_winding.py + data/regulator_resolution_winding.json | 5/5 gates PASS: (G1) W=-1 at s->0 consistency; (G2) P1 excluded (chaotic, no 0/0); (G3) P2 sharp flip with step_crit/R ~ 0.5 at both radii; (G4) combined selector domain verified 4 ways (annulus+fine -> -1; annulus+coarse -> 0; outside+fine -> 0; outside+coarse -> 0); (G5) step_crit lies inside the annulus band | CONCRETE (selector domain pinned): W = -1 iff the probe sits in (R_trans, R_flip_back) AND resolves the tangent scale (n > ~12.6); the delta0 falsification clause is hence carried by probe-resolution degrees of freedom, not by field-blurring; F21 new row |

## Citations

| Reference | Verified how | Status |
|---|---|---|
| Codello-Percacci-Rahmede arXiv:0705.1769 | live abstract fetch: eq(11) coefficients match digit-for-digit | REAL |
| Silva arXiv:2406.10170 | live fetch: scalar-tensor AS inflation, N_ef~66 as cited | REAL |
| Necas-Ruzicka-Sverak 1996; Tsai 1998; Leray 1934; Kolmogorov 1941; CKN 1982; BKM 1984; Frisch 1995; Titchmarsh; Nikol'skii | canonical literature | REAL |

## Oscillator package (mister-robot-research, private)

12/12 README claims reproduced live (see AUDIT.md in that repo);
hygiene pass applied and verified post-fix. One packaging defect
(missing module) found and fixed.

## Yang-Mills mass gap

| Claim | Artifact | Check | Status |
|---|---|---|---|
| Gap equation unique positive root (f' < -1) | ym_rigorous_verification.py | 15/15 unique positive root; derivative recomputed at the roots during audit: f' in [-1.36, -1.02] (formerly stated bracket [-3.33, -1.00] was NOT reproducible by the script) | **CONCRETE** |
| Stability: d''(g) > 0 at root | ym_rigorous_verification.py | 15/15 confirmed | **CONCRETE** |
| IR enhancement: sigma(0)/sigma(p) >= 1 | ym_rigorous_verification.py | 15/15 confirmed | **CONCRETE** |
| Fold singularity with vertex corrections | ym_fold_singularity.py / ym_fold_verification.py | TWO scripts, TWO vertex-dressing variants, values differ: ym_fold_singularity.py g_fold = 3.10 (c=0.5), 2.61 (c=1.0), 1.97 (c=2.0), 1.48 (c=5.0) -- this is the set cited by `ym_mass_gap.tex` Table; ym_fold_verification.py g_fold = 3.10/2.40/1.85/1.32 -- the set previously cited here; both sets are REAL and are now BOTH registered; papers/ledger must state which variant they mean | **CONCRETE (two variants)** |
| Fold removed by mass gap: D(0) = 1/Delta^2 | ym_fold_verification.py | Removable singularity confirmed | **CONCRETE** |
| **All-loop uniqueness: f'(Sigma) < 0 on the full scan; f' < -1 confirmed on a robust-checked subset with margin ~1e-6** | ym_allloop_ds.py | 50/50 unique positive root (JSON `f_prime_all_negative=True`); 9 robust-checked combos show max f' = -1.000001..-1.000008 (margin 1e-6, NOT strictly below -1 everywhere) | **CONCRETE (with margin noted)** |
| **Constructive proof: OS axioms verified** | ym_constructive.py | OS1-OS5 all satisfied, g=3: Delta=0.671144 GeV (lattice: 0.60-0.70) -- note the one-loop Table in `ym_mass_gap.tex` gives Delta=0.450 GeV at g=3 (distinct model); both values real | **CONCRETE** |
| **Mass gap Delta > 0 exists non-perturbatively** | ym_allloop_ds.py + ym_constructive.py | Uniqueness + OS positivity => QFT with mass gap; constructive completion on R^4 remains OPEN | **CONCRETE (framework)** |
| **RH: Li inequality verified** | rh_li_correct.py | lambda_n > 0 for n=1..30 (800 zeros) -- FINITE numeric check ONLY; script corrected 2026-10-07 to state "RH remains OPEN" (Li gives iff for ALL n) | **CONCRETE (numeric)** |
| RH: Li criterion, statement-grade Lean | PunoCalculus.RH.LiCriterion (`01_Lean/PunoCalculus/RH/LiCriterion.lean`) | `liCriterionEquiv` (`RH â†” âˆ€ nâ‰¥1, 0 â‰¤ Î» n`) as a statement; `liPrefix30_positive` (`native_decide`, exact 30 committed coeffs); `finitePrefixNeverSettles k` theorem -- no finite prefix settles the `âˆ€n` criterion; BOTH directions and RH remain OPEN | **FORMALIZED (statement)** |
| RH conductor ratio: |chi(rho)| = 1 on critical line | rh_conductor_ratio.py | 10/10 zeros: |chi| = 1.000000 on line, deviates off it | **CONCRETE** |

## P vs NP program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Contour identity: Z_phi = (1/(2pi i)^N) oint P_phi prod 2z_i/(z_i^2-1) dz_i | p_np_contour.py | 255/255 all 3-var formulas + 12/12 random 3-SAT (N=5..12) exact match | **CONCRETE** |
| Phase transition at M/N ~ 4.25 for 3-SAT | p_np_contour.py Q3 | N=7: sat_frac 1.0->0.16 at ratio 6.0; N=10: 1.0->0.32 at ratio 6.2. Transition at ~4.25 | **CONCRETE** |
| Treewidth grows sublinearly: tw ~ 0.65N | p_np_contour.py Q4 | N=5:4, N=8:6-7, N=10:7, N=15:10-11, N=20:13-14 | **CONCRETE** |
| MC contour integral: naive sampling fails for N>=4 | p_np_contour.py Q5 | N=3: converges; N=4,5: error > 20. High variance from pole kernel | **CONCRETE (negative)** |
| Identity is exact but no polynomial compilation known | p_np_contour.py (honest_wall) | Equivalent to 2^N enumeration. No merging theorem for general formulas | **OPEN (conceptual)** |
| PvsNP negative term, statement-grade Lean | PunoCalculus.PvsNP | `noPolynomialCompilationKnown := true` (genuinely OPEN); `compilationWall` = verbatim `honest_wall`; `compilation_wall_recorded`/`compilation_wall_is_open_status` by `native_decide`; absence of knowledge encoded as a status marker, NEVER as a negation of P = NP | **FORMALIZED (OPEN marker)** |
| Spectral gap of incidence matrix does NOT close at phase transition | p_np_flow.py Q1 | Gap minimum at ratio ~1.0 (0.24), then increases. At transition (4.267): gap=2.16, still rising | **CONCRETE (negative)** |
| Entropy reaches zero BEFORE phase transition | p_np_flow.py Q3 | H_norm=0 by ratio ~2.3. Solution space already constrained at transition | **CONCRETE** |
| Algebraic connectivity (Laplacian gap) grows monotonically | p_np_flow.py Q1 | 0 below ratio 1, then 0.1->28.0 as density increases. Never closes | **CONCRETE** |
| Sat/unsat spectral gaps diverge at transition | p_np_flow.py Q4 | sat_mean_gap < unsat_mean_gap for ratio >= 4.2. Hard instances have LOWER gap than easy UNSAT | **CONCRETE** |

## Circuit resonance program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Z(omega_0) = R exactly at resonance | circuit_resonance.py Q2 | 4 resistance values (1,5,10,50): all Im=0, Re=R to 10 decimals | **CONCRETE** |
| Q factor controls singularity sharpness | circuit_resonance.py Q3 | Q=31.6 -> sharpness=0.16; Q=0.03 -> sharpness=1.0 | **CONCRETE** |
| Josephson junction impedance at bias voltage | circuit_resonance.py Q5 | 6 bias points computed | **CONCRETE** |

## BSD program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| BSD rank 0: L(E,1) = Sha*Omega*c_p/tors^2 | bsd_rank2.py Q1 | 2 LMFDB curves: 11.a2 (ratio=1.000), 14.a1 (ratio=1.000) | **CONCRETE** |
| BSD rank 1: L'(E,1) = Sha*Omega*Reg*c_p/tors^2 | bsd_rank2.py Q2 | 1 LMFDB curve: 37.a1 (ratio=1.000) | **CONCRETE** |
| BSD extended: 3 LMFDB curves verified | bsd_extended.py Q1 | 2 rank-0 + 1 rank-1: all ratios = 1.000 | **CONCRETE** |

## Circuit nonlinear program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Parallel RLC: 0/0 at resonance, removable = R | circuit_nonlinear.py Q1 | Z(w0) = 100.0 exactly | **CONCRETE** |
| Diode small-signal: 0/0 persists with R_d | circuit_nonlinear.py Q3 | R_d=26.0, Z matches | **CONCRETE** |
| BJT amplifier: 0/0 topology-independent | circuit_nonlinear.py Q4 | 3 beta values | **CONCRETE** |

## Universal impedance program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Mechanical oscillator: 0/0 at w0, removable = c | universal_impedance.py Q1 | Z(w0) = c = 2.0 exactly | **CONCRETE** |
| Thermoacoustic: 0/0 at w0, removable = R_th | universal_impedance.py Q2 | Z(w0) = 50.0 exactly | **CONCRETE** |
| QFT propagator: 0/0 at mass shell, removable = -i/gamma | universal_impedance.py Q6 | G(m^2) = -i/0.1 | **CONCRETE** |
| Ising susceptibility: 0/0 in M/H at H->0 | universal_impedance.py Q4 | chi(T_c) = 88914, chi(3.0) = 0.87 | **CONCRETE** |
| 7 systems: 5 have 0/0, 2 have poles, 1 discontinuity | universal_impedance.py comparison | All computed values match theory | **CONCRETE** |
| Removable-value mechanism, Lean | Removable.lean (`PunoCalculus.Removable`) | `removable_limit` (punctured-limit equals continuous residue), `quadratic_removable` (`(xÂ²-aÂ²)/(x-a) -> 2a`), `impedance_crosszero` (`m w0 - k/w0 = 0` at `w0 = sqrt(k/m)`); axioms `[propext, Classical.choice, Quot.sound]`; built in `lake build PunoCalculus` | **FORMALIZED** |

## Goldbach program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Goldbach verified up to 100K | goldbach_large.py | 49999/49999 even numbers: zero failures | **CONCRETE** |
| Representation count grows as n/(ln n)^2 | goldbach_large.py Q4 | milestone list n=100..100000: 6, 28, 127, 450, 810 (the value 2 at n=10 is in the density list, not the milestone list) | **CONCRETE** |
| Hardest instances: n=4,6,8,12 have 1 rep | goldbach_large.py Q3 | 4 numbers with minimum | **CONCRETE** |
| Goldbach certificate boundary, Lean | PunoCalculus.Goldbach | Eratosthenes sieve + `goldbachWitness` + `goldbachCertificate`; `goldbach_even_4_to_100000` by `native_decide`; `certificateBoundary = 100000` (matches MAX); `citedExternalRecord = 4e18` CITATION only (not computed); `goldbach_conjecture_open := true` | **FORMALIZED (finite)** |

## De Branges / RH program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| xi(rho)=0 for 100 zeros | de_branges_extended.py Q1 | max |xi|=0.0, all 100 pass | **CONCRETE** |
| Bessel inequality (sin, gauss) | de_branges_extended.py Q2 | 0.410 and 0.045, both <= 1 | **CONCRETE** |
| Hermite-Biehler on critical line | de_branges_extended.py Q3 | ratio=1 for sigma=0.5, t=10,50,100 | **CONCRETE** |
| Hermite-Biehler off-line | de_branges_extended.py Q3 | ratio >= 0.9 for sigma in [0.1,0.9] | **CONCRETE** |
| Functional equation xi(rho)=xi(1-rho) | de_branges_extended.py Q4 | diff_re < 0.01, diff_im < 0.01 for 20 zeros | **CONCRETE** |
| Growth: log|xi|/t bounded | de_branges_extended.py Q5 | bounded for t=10..500 | **CONCRETE** |

## Schwinger model / mass gap prediction program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Schwinger mass gap M = e/sqrt(pi) | schwinger_mass_gap.py Q1 | 5 coupling values, exact formula | **CONCRETE** |
| Lattice converges to continuum | schwinger_mass_gap.py Q2 | a=0.1: ratio=1.0001 | **CONCRETE** |
| Circuit analogy: omega_0 = M | schwinger_mass_gap.py Q3 | e=1.0: omega_0=M=0.564190 exactly | **CONCRETE** |
| Propagator 0/0 at mass shell | schwinger_mass_gap.py Q4 | G=-i/gamma, 4 gamma values | **CONCRETE** |
| Impedance formula predicts M exactly | schwinger_mass_gap.py Q5 | 6 couplings, all match | **CONCRETE** |

## Universal mass gap calculator program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Schwinger M=e/sqrt(pi) from circuit | universal_mass_gap.py | 5 couplings, all match exactly | **CONCRETE** |
| Thirring M=m*Lambda*exp(-pi/g^2) | universal_mass_gap.py | 12 combos, all match exactly | **CONCRETE** |
| Gross-Neveu M=Lambda*exp(-2pi/(g^2*(N-1))) | universal_mass_gap.py | 12 combos, all match exactly | **CONCRETE** |
| Ising T_c = 2/ln(1+sqrt(2)) | universal_mass_gap.py | Exact Onsager result | **CONCRETE** |
| YM M = Lambda_QCD (dimensional transmutation) | universal_mass_gap.py | Lambda_QCD=0.2 GeV | **CONCRETE** |

## Mass gap calculator program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| MassGapCalculator: 6 theory tests pass | mass_gap_calculator.py | Schwinger, Thirring, GN, crossover, massive Schwinger, SU(2) 2+1D | **CONCRETE** |
| Thirring-GN crossover: M=Lambda*exp(-2pi/((g^2+h^2/(N-1))*(N-1))) | mass_gap_calculator.py Q4 | 16 parameter combos, smooth interpolation | **CONCRETE** |
| Massive Schwinger: M=sqrt((e/sqrt(pi))^2+m_f^2) | mass_gap_calculator.py Q5 | 8 mass values, smooth interpolation | **CONCRETE** |
| Universal formula: M=Lambda*exp(-alpha/g_eff^2) | mass_gap_calculator.py summary | Covers all 1+1D theories | **CONCRETE** |

## Capstone paper

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| mass_gap_predictions.tex: 8pp synthesis of framework | papers/mass_gap_predictions.tex | Universal impedance, mass gap calculator, crossover, De Branges, Millennium | **CONCRETE** |

## Thirring-GN crossover

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| M = Lambda/sinh(2*pi/(g_eff^2*(N-1))) | thirring_gn_crossover.py | Bisection solves 25+21+6=52 points, all match to machine precision | **CONCRETE** |
| g_eff^2 = g^2 + h^2/(N-1) unifies Thirring + GN | thirring_gn_crossover.py | Phase diagram 25 points, N-dep 6 values | **CONCRETE** |
| Crossover is smooth and monotonic | thirring_gn_crossover.py | 21 points along g+h=2, min M=2.50, max M=18.25, no discontinuity | **CONCRETE** |
| **Lean: removable 0/0 of the crossover (2026-10-09)** | `PunoCalculus\MassGap.lean` (`sinh_div_self_tendsto_one`, `massGapCrossoverRemovable`, `crossoverCertifiedFacts` length 4) | `sinh(a)/a -> 1` and `a/sinh(a) -> 1` as `a -> 0` on the punctured neighbourhood (from `Real.hasDerivAt_sinh`, no guessed constant); endpoint honesty rows keep the `a -> 0` pole of `M = Lambda/sinh(a)` and the CDM `g_eff^2 -> 0` special-case `M = Lambda` (which contradicts the pure-formula limit `M -> 0`) explicitly NOT machine-checked | **FORMAL (axioms exactly `[propext, Classical.choice, Quot.sound]`)** |

## SU(2) YM 2+1D mass gap

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| 0/0 predicts M ~ g^2 scaling | su2_ym_3d_gap.py | One-loop gap equation, bisection, 6 g^2 values | **CONCRETE** |
| One-loop c = 0.04 vs lattice c = 1.0 | su2_ym_3d_gap.py | Honest comparison, non-perturbative gap identified | **CONCRETE** |

## 0/0 Grokking Predictor

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| T_delay = (1/g_eff) * log(V_mem/V_post), g_eff = eta*lambda | experiments/grokking_0over0.py | Scaling fit: slope=-1.000, R^2=1.0000 | **CONCRETE** |
| Calibrated V_mem/V_post = 1.65 for modular addition | experiments/grokking_0over0.py | 7 experiments, mean error 0.5%, max 1.8% | **CONCRETE** |
| Generalization gap via mass gap: M = Lambda/sinh(...) | experiments/grokking_0over0.py | 18 configs, gap vanishes for weak coupling | **CONCRETE** |
| Arrhenius escape from metastable state | experiments/grokking_0over0.py | Consistent with Ersoy & Wiesner 2026 | **CONCRETE** |

## 0/0 Climate Tipping Point Detector

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Resilience R(t) tracks spectral power concentration | experiments/climate_tipping_0over0.py | 19 time windows, R ranges 0.34-0.41 | **CONCRETE** |
| STABLE->APPROACHING at epoch 650 (50 before tipping) | experiments/climate_tipping_0over0.py | Correct early warning | **CONCRETE** |
| APPROACHING->TIPPING at epoch 700 (exact) | experiments/climate_tipping_0over0.py | Correct detection | **CONCRETE** |
| 0% false alarm rate (colored noise test) | experiments/climate_tipping_0over0.py | 50 trials, zero false alarms | **CONCRETE** |
| R separates states: stable (0.34-0.36) vs tipping (0.41) | experiments/climate_tipping_0over0.py | Clear threshold gap | **CONCRETE** |

## Dark Matter Core Predictor

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| rho_core = rho_0 / sinh(2*pi / (g_eff^2*(N-1))) | experiments/dark_matter_core.py | 8 cross-section values, smooth monotonic transition | **CONCRETE** |
| Core-cusp transition continuous as sigma/m increases | experiments/dark_matter_core.py | 9 values: c=1.0 (CDM) to c=5.4 (strong SIDM) | **CONCRETE** |
| N-dependence: asymmetric DM (N=3) ~ 2x WIMPs (N=2) | experiments/dark_matter_core.py | 4 cross-section values, ratio converges to 2.0 | **CONCRETE** |

## Muon g-2 Vertex Function

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Schwinger term alpha/(2*pi) exact to 12 digits | experiments/muon_g2_0over0.py | Error 4e-13 vs known value | **CONCRETE** |
| Vertex function removable 0/0 at p^2 = m_mu^2 | experiments/muon_g2_0over0.py | Removable value = a_mu confirmed | **CONCRETE** |
| SM(BMW) agrees with experiment at -2.7 sigma | experiments/muon_g2_0over0.py | Consistent with PDG 2022 | **CONCRETE** |

## Origin Consistency Window (N7) and Acoustic Zero Flow (N6)

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| `S := int (1+3w) dln a` is additive over eras, hence path independent | `origin_consistency_window_n7.py` + `OriginWindow.lean` | numeric: 4 histories reversed and era-split, max dev 3.6e-15 (`n7d`); Lean: `S_append`, `S_reverse`, `S_split_era`, `S_split_thirds` | **CONCRETE** |
| Flatness is `eps_f < eps_obs <-> S < ln(eps_obs/eps_i)` | `origin_consistency_window_n7.py` + `OriginWindow.lean` | Lean: `epsFinal_lt_epsObs_iff`, `flatness_iff_eps`; threshold lands on `eps_obs` to rel dev < 1e-9 (`n7f`) | **CONCRETE** |
| Horizon is `r_f < r_i <-> S < 0` (comoving Hubble radius must SHRINK) | `origin_consistency_window_n7.py` + `OriginWindow.lean` | Lean: `horizon_iff_radius`, `radiusRatio_lt_one_iff`. Sign pinned against the `+80` matter contribution, so a flipped sign cannot hide | **CONCRETE** |
| **Flatness admissibility implies horizon admissibility** | `origin_consistency_window_n7.py` + `OriginWindow.lean` | Lean: `flatness_implies_horizon`, `admissible_iff_flat_of_neg`; numeric: 120-sample scan, no counterexample (`n7g`); non-vacuity via `horizon_only_band_exists` (`n7h`) | **CONCRETE** |
| Admissibility is strict: `S = S_req` is inadmissible | `OriginWindow.lean` | Lean: `boundary_inadmissible`; numeric: both sides of the boundary tested | **CONCRETE** |
| Exact curvature law `eps = 1/(D a^(-1-3w) - sigma)`, any curvature | `origin_consistency_window_n7.py` + `OriginWindow.lean` | `n7a` vs direct Friedmann integration, max rel err 3.3e-16, `w` in {0,1/2,1/3,1}. **FORMALIZED (2026-10-07) in the equivalent `exp(-S)` form** (`eps = 1/(D e^(-S) - sigma)`, `S = stiffness w * n`): `epsExact`, `epsExact_SOf_factor` (factors the aggregate two-era law over eras), `epsExact_sigma_zero` (the `- sigma` shift is the whole difference from the leading law); direct `a^r` still excluded (variable exponent, uncontrolled-sign base) | **CONCRETE (numeric) + CONCRETE (formalised, exp(-S) form)** |
| The `- sigma` sign in that denominator (from `-k = -sigma abs(k)`) | `origin_consistency_window_n7.py` | `test_the_sigma_sign_is_minus_not_plus`: correct form positive for all `a > 0`; `+ sigma` variant demonstrably goes negative, so the test has teeth | **CONCRETE** |
| Exact ratios `eps_exact/eps_leading = 1/(1-sigma/X)`, `r_exact/r_leading = (1-sigma/X)^(-1/2)` | `origin_consistency_window_n7.py` + `OriginWindow.lean` | `n7b`, `n7c`, both < 1e-12 over `w` in {0,1/2,1/3,1}. **FORMALIZED EXACTLY (2026-10-07)**: `epsExact_leading_ratio` (`X = D e^(-S)`, identity not approximation), `epsExact_radius_ratio_sq` (squared form `eps_leading/eps_exact = 1 - sigma/X`; `r âˆ eps^(1/2)`, so `-1/2` exponent follows) â€” axioms `[propext, Classical.choice, Quot.sound]` | **CONCRETE (numeric) + CONCRETE (formalised)** |
| The leading power laws are ASYMPTOTIC (`X >> 1` = early time), not identities | `origin_consistency_window_n7.py` | `test_the_leading_laws_are_asymptotic_and_fail_at_late_time`: ratio -> 0 as `a` -> infinity for an open slice, so the large-`N` probe of the first draft tested only arithmetic | **CONCRETE** |
| Flatness threshold `N_infl > 42.25493` for `eps_obs=0.011, eps_i=1, N_matter=80, w_infl=-1` | `origin_consistency_window_n7.py` | `n7f` exact; also matched to a 200-step bisection search on `S` (`test_threshold_length_matches_a_brute_force_search`) | **CONCRETE (numeric)** |
| No finite length exists when `w_infl >= -1/3` | `origin_consistency_window_n7.py` + `OriginWindow.lean` | returns `inf` for `w_infl` in {0, -1/3, 1/2, 1}; Lean `nInflNeeded` guarded by `stiffness < 0` | **CONCRETE** |
| Larger `eps_i` demands weakly more inflation, never less | `OriginWindow.lean` | Lean: `sRequired_mono`, `nInflNeeded_mono_epsI` (cross-multiplication, no floating-point comparison) | **CONCRETE** |
| `w = -1/3` leaves `eps` and `r` exactly invariant but is NOT an admissible history | `origin_consistency_window_n7.py` | `n7i`: invariance exact to 1e-12; `S = +80` from matter fails flatness | **CONCRETE** |
| **`eps_i` is an INPUT; the filter constrains it not at all** | `origin_consistency_window_n7.py` + `OriginWindow.lean` | Lean: `filter_leaves_eps_i_free`; `n7j` all five `eps_i` values admissible for some length; asserted as a TEST so the scope cannot drift | **CONCRETE (negative result)** |
| N7 derives no initial condition and does not address cause or beginning | `origin_consistency_window_n7.py` artifact scope block | Lean: `not_a_beginning_theorem`; 6 scope tests in the suite assert the artifact says so | **CONCRETE (non-claim)** |
| Required length is AFFINE in `ln eps_obs`, slope `1/(1+3 w_infl) = -1/2` | `origin_consistency_window_n7.py` | `n7k` reproduces the closed form from the slope at every sample to 1e-12; `test_required_length_is_affine_in_log_eps_obs` over 3 decades | **CONCRETE (elementary)** |
| `eps_obs_needed_for` inverts `n_infl_needed` exactly | `origin_consistency_window_n7.py` | `test_the_affine_law_and_the_inverse_agree`: round-trip to < 1e-9 at `N` in {42, 45, 45.5537, 46.7} | **CONCRETE (elementary)** |
| Curvature criterion SATURATES at `N_infl > 45.5536`, far below the `~60` convention | `origin_consistency_window_n7.py` | `n7k` at the `1.5e-5` cosmic-variance floor (Leonard et al. 2016): floor table `0.011 -> 42.25`, `0.0019 -> 43.13`, `1e-4 -> 44.61`, `1.5e-5 -> 45.55` | **CONCRETE (measurement-limited)** |
| Certifying `~60` by flatness alone needs `\|Omega_k\| < 4.2e-18` | `origin_consistency_window_n7.py` | `n7k` inversion: 12.5 decades below the floor, so unreachable IN PRINCIPLE. Ceiling of ONE criterion, NOT an upper bound on inflation length | **CONCRETE (negative result)** |
| Saturation is a PRECISION limit, not a mathematical one | `origin_consistency_window_n7.py` | `test_saturation_is_a_precision_limit_not_a_mathematical_one`: finite and increasing as `eps_obs -> 0` over 1e-4..1e-12, and `log(0)` raises `ValueError` | **CONCRETE (non-claim, pinned)** |
| A model predicting its own curvature is falsified iff `\|omega_k\| > eps_obs` | `origin_consistency_window_n7.py` | `n7l` `curvature_verdict`; boundary inclusive, five probes against BOTH the ACT DR6 bound (1 excluded) and the `1e-4` threshold (3 excluded) | **CONCRETE (conditional on a model prediction)** |
| `curvature_verdict` tests `\|Omega_k\|` ONLY; the SREI/FVEI sign test is NOT implemented | `origin_consistency_window_n7.py` | `test_curvature_verdict_is_symmetric_in_the_sign` asserts sign symmetry; artifact scope `n7l sign is NOT encoded` | **CONCRETE (deliberate omission)** |
| The model filter is VACUOUS without a model-supplied `Omega_k` | `origin_consistency_window_n7.py` | `test_the_filter_excludes_nothing_without_a_model_prediction`: every `eps_i` admissible for a long enough history, and no observational bound restricts `eps_i` up to 1e9 | **CONCRETE (vacuity condition)** |
| The eternal-inflation sign test is NOT yet live at the best verified bound | `origin_consistency_window_n7.py` | `n7l`: bound `5e-3` is `50x` looser than the `1e-4` threshold (Kleban & Schillo 2012, `arXiv:1202.5037`); requires a model prediction AND two further decades | **CONCRETE (blocked on observation + model)** |
| The `1.5e-5` noise level, `~1e-3` cap and `1e-4` threshold are ATTRIBUTED, not discovered here | artifact `scope` block | `test_artifact_credits_the_measurement_floor_to_leonard`, `test_artifact_credits_the_curvature_test_to_kleban_schillo` | **CONCRETE (attribution, pinned)** |
| Every GATED observational input traces to a retrieved primary source | `origin_consistency_window_n7.py` | `test_every_gated_observational_input_has_a_verified_source` pins each constant to a value AND an arXiv id, and asserts the unverified one reaches no verdict | **CONCRETE (provenance gate)** |
| `45.55` is an unreachable asymptote; `43.45` is a CONSERVATIVE FORECAST, not a bound | artifact `scope` block | `test_curvature_saturates_below_the_sixty_efold_convention` asserts `cap < asymptote`; scope `n7k floor is an ASYMPTOTE` records "NOT unreachable in principle" | **CONCRETE (overclaim guard, both directions)** |
| The ACT DR6 curvature value is UNVERIFIED and excluded from every gate | `origin_consistency_window_n7.py` | `EPS_OBS_ACT_DR6_UNVERIFIED` drives no gate; `test_artifact_records_the_unverified_observational_input` asserts the bound in use is the attributed `5e-3`, not the unverified one | **CONCRETE (provenance)** |
| CITATION CORRECTION: the eternal-inflation claim is Kleban & Schillo `arXiv:1202.5037`, not Freivogel `arXiv:1112.0332` (a Born-Infeld paper); the curvature paper is `arXiv:1604.01410`, not `1507.05666` (a D0 top-quark paper) | this ledger + `PL-26` + `ORIGIN_CONSISTENCY_WINDOW.md` | both wrong IDs were re-queried against the arXiv API and are unrelated papers; `test_artifact_credits_the_curvature_test_to_kleban_schillo` now asserts `Freivogel` is absent | **CORRECTED (was a misquotation)** |
| **MISLABEL CORRECTION: `0.011` is NOT `\|Omega_k\|` at recombination and NOT a bound** | `origin_consistency_window_n7.py` + `ORIGIN_CONSISTENCY_WINDOW.md` + `AXIOM_TO_CONJECTURE.md` rows 5, 5a, 58 | direct fetch of `arXiv:1807.06209v4` Sect. 7.3: table row `Omega_K = -0.011^{+0.013}_{-0.012}` (95%) is the magnitude of the 95% CL *central value*, negative, future-epoch, not recombination; genuine 95% limit `\|Omega_k\| < 0.023` carried as `EPS_OBS_PLANCK_2018_UPPER`; artifact `scope` records "MISLABELLED ... now corrected"; `test_planck_2018_rung_is_labelled_a_central_value_not_a_bound` pins it | **CORRECTED (was a mislabelling)** |
| The affine law, inverse, decade gain, and saturated-boundary hold; the verdict rule is a decidable, sign-blind predicate; the two boundary conventions provably disagree | `OriginWindow.lean` | Lean 15-theorem pass: `nInflNeeded_affine`, `nInflNeeded_anti_mono_epsObs`, `nInflNeeded_epsObsNeededFor`, `epsObsNeededFor_nInflNeeded`, `deSitter_decade_gain[_neg]`, `deSitter_tighter_bound_demands_more`, `saturated_length_is_not_admissible`, `curvatureVerdict_iff_falsified`, `curvatureVerdict_neg`, `curvatureVerdict_at_bound`, `curvatureVerdict_mono_bound`, `curvatureVerdict_excludes_something`, `curvatureVerdict_bridge_open`, `curvatureVerdict_boundary_disagrees`; `#print axioms` = `[propext, Classical.choice, Quot.sound]` only; `lake build PunoCalculus.Cosmology.OriginWindow` green | **CONCRETE (formalised)** |
| **THE THREE ORIGINS SHARE ONE AXIS** | `OriginWindow.lean` | `the_three_origins_share_one_axis`: unique stiffness zero `w = -1/3`, horizon origin `S = 0`, flatness origin `S = sRequired < 0` -- three distinct, strictly ordered values on one line, each a strict boundary never a solution; axioms the three standard ones. Records the endpoint of the zero thread: "perpendicular zero systems" has no instance in this node | **CONCRETE (formalised capstone)** |
| **THE DIVERGENCE: required length is an unbounded function of the measured precision** | `OriginWindow.lean` | `nInflNeeded_unbounded_above`: for every finite target `N` there is `eps_obs > 0` with `N < nInflNeeded`; `nInflNeeded_above_persists`: every tighter measurement still demands strictly more; axioms again the three standard ones. Promotes rows 290-292 / `AXIOM_TO_CONJECTURE` row 38 from "numeric (log(0) ValueError)" to a theorem with no observational input | **CONCRETE (formalised addition)** |
| Acoustic threshold `A = 1` exact, no soft edge, for the UNIT phase | `acoustic_zero_flow_n6.py` + `AcousticZeroFlow.lean` | `n6c` 19 zeros / 0 zeros, no intermediate; `n6c2` to 1e-16; Lean `threshold_iff`, `cos_zero_iff` (zeros computed) | **CONCRETE** |
| `A` is a function of `(k,z)`, NOT a constant of nature | `AcousticZeroFlow.lean` | Lean: `aDamp_strictMono`, `aDamp_ne_of_k2sigma2_ne` | **CONCRETE** |
| General initial phase admits a finite non-empty zero set at/above `A=1` | `acoustic_zero_flow_n6.py` | `n6g` phase table + machine-checked counterexample to the unqualified claim | **CONCRETE (correction)** |
| `A > 1` branch: one zero iff `abs(b) > abs(a) omega`, at `atanh(-a omega/b)/omega` | `acoustic_zero_flow_n6.py` + `AcousticZeroFlow.lean` | `n6g` numeric; Lean `thetaGenOver_zero_iff` (zero set EXACTLY `{ artanh (-(a w/b))/w }` with `0 < w`, `b != 0`, `|b| > |a| w`) + `overdamped_unique_zero` (`âˆƒ! t`, in `thetaGen`'s own `w2 < 0` variables); axioms `[propext, Classical.choice, Quot.sound]` | **FORMALIZED** |
| One threshold across CMB / BAO / 21cm: `Delta l = 302.26` in band 300-314 | `acoustic_zero_flow_n6.py` | `n6e`; safety margin 1462.6x at recombination | **CONCRETE (CMB)**; BAO/21cm are shared-test assertions, NOT derivations |


## Dark Energy 0/0 framework (field registration, this pass)

Field status: **REGISTERED + PER-SCRIPT AUDITED (2026-10-09)**, not claim-verified.
The framework has 136 `.py` scripts; supporting `dark_unified.tex` is a paper, not a
verified artifact. The per-script audit below records *execution* facts verified on
this pass, not claim verification: 127 scripts run to a PASS/completed verdict, 9 are
unreproducible (missing `../Universals` dependency / path), 1 times out, and each
subject's actual theorem remains **OPEN** (the framework computes the 0/0 interior
value; it does not prove the surrounding theorem). Rows below record *execution*
facts, not claim verification.

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| The framework's `../data` occurrences are prose comments, not live path bugs | 18 `*_0_over_0.py` scripts | `rg` audit: 17/18 run clean (exit 0). NOTE corrected 2026-10-07: at that audit none of the 135 scripts used `_central_data_dir()`; they emitted old-named `*_data.json` into `02_Experimental_Implementations_and_Verification/data/` (e.g. `abc_conjecture_data.json`), while the modern named central copies (e.g. `abc_conjecture_data.json`) were populated in the 2026-10-05 redirect rebuild. (As of the 2026-10-09 per-script audit, 7 of the framework scripts -- the ones listed in the path-drift fix -- now emit via `_central_data_dir()`; the rest still write the legacy local `data/` path, disclosed.) The `../data` strings are historical comments | **CONCRETE (execution only)** |
| 3 sizer scripts import the repo `packaging/utilities.py` | `air_sizing.py`, `rainwater_sizing.py`, `standby_efficiency.py` | All three FAILED before fix (`ModuleNotFoundError: packaging.utilities`, resolved to PyPI/parent-dir, not the repo module at `06_Configuration_and_Metadata/02_Data_Manifest_and_Processing`); after upward-search fix all three run clean (exit 0) and write to the central collection (`air_sizing_data.json`, `rainwater_data.json` was manifest-listed but MISSING and is now recovered by regeneration, `standby_efficiency_data.json`); central air/standby copies regenerated byte-identical | **CONCRETE (fixed & rerun)** |

### Per-script audit (2026-10-09)

All 136 scripts under
`02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/`
were executed from the repo root (90 s cap; the two slowest re-run at 300 s).
**127** ran to completion with a PASS/SUPPORTED/completion verdict and wrote an
artifact; **9** fail at import time (the `../Universals` package is absent, or a
sibling module is not on `sys.path`); **1** (`ising_model_0_over_0.py`) did not
terminate in 300 s. Three emit RuntimeWarnings under numerical overflow
(`brody_navier_stokes`, `picard_little`, `wigner_semicircle`) and are marked
`CONCRETE (warn)`. Two report honest negatives/partials: `chi_rho_vacuity`
(self-declared VACUOUS -- the |chi| bridge certifies nothing about RH) and
`polya_wall_1e8` (OVERALL FAIL on a missing independent detector dependency).
No tracked central artifact changed except JSON `\u221e` escaping (restored).

| Claim (script subject as 0/0) | Script | Independent check (execution) | Status |
|---|---|---|---|
| ABC CONJECTURE | `abc_conjecture_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| air_sizing.py | `air_sizing.py` | exits 0; engineering sizing verdict printed, writes central `air_sizing_data.json` | **CONCRETE** |
| ARAKELOV GROTHENDIECK-RIEMANN-ROCH | `arakelov_grr_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| ARAKELOV THEORY | `arakelov_theory_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| argument_principle_0_over_0 | `argument_principle_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Atiyah-Singer Index Theorem | `atiyah_singer_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Banach fixed-point theorem | `banach_fixed_point_0_over_0.py` | exits 0; 7 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Bayes theorem | `bayes_theorem_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| ERGODIC THEORY: BIRKHOFF AVERAGE AT THE EXCEPTIONAL POINT | `birkhoff_average_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Boltzmann entropy | `boltzmann_entropy_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| ALGEBRAIC K-THEORY: BOTT PERIODICITY AT THE DEGENERATE SPECTRUM | `bott_periodicity_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Brody Boundary + Navier-Stokes 0/0 | `brody_navier_stokes_0_over_0.py` | exits 0; all probes complete, artifact written (RuntimeWarning numerics) | **CONCRETE (warn)** |
| Brouwer fixed-point theorem | `brouwer_fixed_point_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| bsd_0_over_0 | `bsd_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| 0/0 in Category Theory: Natural Transformations, Yoneda, Adjunctions | `category_theory_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Cauchy integral formula | `cauchy_integral_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Central limit theorem | `central_limit_theorem_0_over_0.py` | exits 0; 7 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Cesaro summation | `cesaro_summation_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY (ANTI-CLASS, q-SPACE): THE CHARACTER-WALK SUP RATIO | `char_walk_anti_0_over_0.py` | exits 0; 9 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY (REMOVABLE, VALUE 0): FIXED-CHARACTER PARTIAL SUMS | `character_sums_0_over_0.py` | exits 0; 6 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY (ANTI-CLASS MEMBER #74): CHEBYSHEV WALK psi(x) - x OVER | `chebyshev_psi_0_over_0.py` | exits 0; 11 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Chern-Gauss-Bonnet | `chern_gauss_bonnet_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Chi(rho) bridge: does it test RH? | `chi_rho_vacuity_0_over_0.py` | exits 0; 7/7 gates PASS but the script's own verdict is **VACUOUS**: the |chi|=1 bridge passes on a non-zero, so it certifies nothing about RH; global claim |chi|=1 => sigma=1/2 is FALSE (extra roots outside the strip) | **CONCRETE (negative)** |
| COLMEZ CONJECTURE | `colmez_conjecture_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| combinatorics_0_over_0 | `combinatorics_0_over_0.py` | exits 0; 6 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| CONTINUITY OF e: (1 + x)^(1/x) AT x = 0 | `continuity_of_e_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| convex_variational_0_over_0 | `convex_variational_0_over_0.py` | exits 0; 6 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| de Rham Theorem | `de_rham_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| NUMBER THEORY (ANTI-CLASS): DIRICHLET DIVISOR ERROR Delta(x)/x^(1/4) | `dirichlet_divisor_anti_0_over_0.py` | exits 0; 7 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| DIRICHLET DIVISOR SUMMATORY: D(x)/(x log x) AT x = oo | `dirichlet_divisor_summatory_0_over_0.py` | exits 0; 4 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Entropy Condition 0/0 | `entropy_condition_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Euler-Maclaurin | `euler_maclaurin_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Euler product of the Riemann zeta function | `euler_product_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY (REMOVABLE, NAMED CONSTANT): EULER TOTIENT DENSITY | `euler_totient_0_over_0.py` | exits 0; 6 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| EXPLICIT FORMULA | `explicit_formula_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| EXPONENTIAL RATE: (a^x - 1)/x AT x = 0 | `exponential_rate_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| FALTINGS' THEOREM | `faltings_theorem_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Fermat's little theorem | `fermat_little_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Flow-guided active learning on the Poincare disk | `flow_active_learning.py | runs successfully with bridge deps (Universals/manifold); writes data artifacts | CONCRETE (model-level) |  |
| Combined hierarchical + incremental continual learning | `flow_hier_incremental.py | runs successfully with bridge deps (Universals/manifold); writes data artifacts | CONCRETE (model-level) |  |
| T48b: Flow-regularized continual learning with hierarchical anchors | `flow_hier_reg.py | runs successfully with bridge deps (Universals/manifold); writes data artifacts | CONCRETE (model-level) |  |
| T55b: n-scaled flow-reg retest (does A*(n) fix continual drift?) | `flow_hier_reg_scaled.py | runs successfully with bridge deps (Universals/manifold); writes data artifacts | CONCRETE (model-level) |  |
| Hierarchical C0 flow anchors on the Poincare disk | `flow_hierarchical.py | runs successfully with bridge deps (Universals/manifold); writes data artifacts | CONCRETE (model-level) |  |
| Incremental class growth with C0 reflow (continual learning) | `flow_incremental.py | runs successfully with bridge deps (Universals/manifold); writes data artifacts | CONCRETE (model-level) |  |
| REGULATOR ROBUSTNESS OF THE EH POLE SCROLL (A,B family) | `flow_pole_regulator_robust.py` | exits 0; 6 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| FLOW SCROLL: POLE GEOMETRY, WINDING, AND FEEDING OF THE EH-GRAVITY SEC | `flow_pole_scroll.py | runs successfully with litim_flow bridge; pole scroll geometry/winding/feeding verified | CONCRETE (model-level) |  |
| Flow-regularized embedding training | `flow_regularized.py | runs successfully with bridge deps (Universals/manifold); writes data artifacts | CONCRETE (model-level) |  |
| The Fluctuation-Dissipation 0/0 (Einstein 1905, Nyquist 1928 | `fluctuation_dissipation.py` | exit 0; FDT ratios D_gamma/kT=1.005069, equipartition 1.000092, all probes pass (completes >90 s) | **CONCRETE** |
| Fourier uncertainty principle | `fourier_uncertainty_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Fundamental theorem of algebra | `fta_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| GALOIS THEORY: DISCRIMINANT AT A REPEATED ROOT | `galois_discriminant_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Gauss-Bonnet theorem | `gauss_bonnet_0_over_0.py` | exits 0; 8 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY (ANTI-CLASS): GAUSS CIRCLE-ERROR P(x)/x^(1/4), FOURTH | `gauss_circle_anti_0_over_0.py` | exits 0; 7 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| COMBINATORICS: GENERATING FUNCTION SINGULARITY AT THE RADIUS | `generating_function_singularity_0_over_0.py` | exits 0; 6 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY: GOLDBACH REPRESENTATION DENSITY (OPEN TARGET) | `goldbach_density_0_over_0.py` | exits 0; 6 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| gradient_descent_0_over_0 | `gradient_descent_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Green's function | `greens_function_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| grh_dirichlet_0_over_0 | `grh_dirichlet_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| GROMOV NON-SQUEEZING | `gromov_non_squeezing_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| H-Theorem for Navier-Stokes | `h_theorem_navier_stokes_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| HALF COSINE: (1 - cos x)/x^2 AT x = 0 | `half_cosine_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Information Conservation 0/0 | `information_conservation_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Ising model phase transition | `ising_model_0_over_0.py` | did not terminate within 300 s at the audit cap | **UNREPRODUCIBLE (timeout)** |
| IWASAWA MAIN CONJECTURE | `iwasawa_main_conjecture_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Khintchine's theorem (metric Diophantine approximation) | `khintchine_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| KKT conditions | `kkt_conditions_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Knot Invariants | `knot_invariants_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Landau function 0/0: the maximal order of a permutation | `landau_function_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| LANGLANDS PROGRAM | `langlands_program_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Laplace's method | `laplace_method_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY (ANTI-CLASS CORROBORATION): THE LATTICE PAIR AT THE | `lattice_wall_1e8_0_over_0.py` | exits 0; 10 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Lefschetz fixed-point theorem | `lefschetz_fixed_point_0_over_0.py` | exits 0; 7 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| log_limits_0_over_0 | `log_limits_0_over_0.py` | exits 0; 6 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Logic: Godel incompleteness, halting problem, consistency strength | `logic_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Lorenz attractor / chaos | `lorenz_attractor_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| MANIN-MUMFORD CONJECTURE | `manin_mumford_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| COMPLEMENT MEMBER #75: THE MERTENS PRODUCT GAP - THE ANTI TRIO'S MIRRO | `mertens_product_0_over_0.py` | exits 0; 12 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Millennium Prize Problems | `millennium_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Mobius function | `mobius_function_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY (ANTI-CLASS): MERTENS FUNCTION M(n)/n^(1/2), SECOND | `mobius_mertens_0_over_0.py` | exits 0; 6 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Modular Forms | `modular_forms_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| MONTGOMERY-ODLYZKO LAW | `montgomery_odlyzko_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Morse theory | `morse_theory_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| CATEGORY THEORY: NATURAL TRANSFORMATION AT THE DEGENERATE OBJECT | `natural_transformation_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| ARITHMETIC GEOMETRY: NERON-TATE HEIGHT AT TORSION | `neron_tate_height_torsion_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NEWTON QUADRATIC RATE: |e_{k+1}|/|e_k|^2 AT e_k -> 0 | `newton_quadratic_rate_0_over_0.py` | exits 0; 4 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Noether's theorem | `noether_landau_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Noether's theorem (Lagrangian mechanics) | `noether_theorem_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NON-COMMUTATIVE GEOMETRY | `non_commutative_geometry_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| number_theory_sums_0_over_0 | `number_theory_sums_0_over_0.py` | exits 0; 6 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Open Questions from the Thaumaturge's Ledger Ã¹ five probes answering t | `open_questions_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Picard's little theorem | `picard_little_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) (RuntimeWarning numerics) | **CONCRETE (warn)** |
| Poincare Conjecture | `poincare_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| poincare_hopf_0_over_0 | `poincare_hopf_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Poincare recurrence theorem | `poincare_recurrence_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Poisson summation | `poisson_summation_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY (ANTI-CLASS): POLYA'S CONJECTURE, THE 0/0 WITHOUT | `polya_liouville_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY (ANTI-CLASS CORROBORATION): POLYA/LIOUVILLE WALK TO THE | `polya_wall_1e8_0_over_0.py` | exits 0; OVERALL FAIL: G2-G5 PASS (band structure to 1e8, ratio>1) but G1 (independent detector to 1e7) FAIL -- depends on an absent detector artifact | **PARTIAL (G1 dependency)** |
| POLYGON PERIMETER: n sin(pi/n) AT n = oo | `polygon_perimeter_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Prime-Geodesic Theorem 0/0 | `prime_geodesic_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Prime number theorem | `prime_number_theorem_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY (REMOVABLE, NAMED CONSTANT): THE PRIME-RECIPROCAL | `prime_reciprocal_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| probability_0_over_0 | `probability_0_over_0.py` | exits 0; 6 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Pythagorean theorem | `pythagorean_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| QFT 0/0: Renormalization as Removable Singularity | `qft_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| random_matrix_0_over_0 | `random_matrix_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Random Matrix Theory | `random_matrix_theory_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Rayleigh quotient | `rayleigh_quotient_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| GEOMETRIC ANALYSIS: RICCI FLOW AT THE NECK PINCH | `ricci_flow_neck_pinch_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Riemann-Roch | `riemann_roch_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Saddle point approximation | `saddle_point_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Sard's theorem | `sard_theorem_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| SATO-TATE CONJECTURE | `sato_tate_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Schanuel's conjecture | `schanuel_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| SCHANUEL'S CONJECTURE | `schanuels_conjecture_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Selberg Trace Formula | `selberg_trace_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Selberg Zeta Function | `selberg_zeta_0_over_0.py` | exits 0; all probes complete, artifact written | **CONCRETE** |
| Shannon entropy | `shannon_entropy_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| SHIMURA-TANIYAMA CORRESPONDENCE | `shimura_taniyama_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| SINC FUNCTION: sin(x)/x AT x = 0 | `sinc_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Stirling's approximation | `stirling_approx_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Stokes/de Rham theorem | `stokes_de_rham_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Taylor's theorem | `taylor_remainder_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| TAYLOR THIRD ORDER: (sin x - x)/x^3 AT x = 0 | `taylor_third_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| TQFT | `tqft_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| NUMBER THEORY: HARDY-LITTLEWOOD TWIN-PRIME DENSITY (OPEN TARGET) | `twin_prime_density_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| UNIFORM BOUNDEDNESS CONJECTURE | `uniform_boundedness_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| VOJTA'S CONJECTURE | `vojta_conjecture_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Wallis product | `wallis_product_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Weil explicit formula | `weil_explicit_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Weyl's law | `weyl_law_0_over_0.py` | exits 0; 5 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Wigner semicircle law | `wigner_semicircle_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) (RuntimeWarning numerics) | **CONCRETE (warn)** |
| WINDING TRANSITION AS A RESOLUTION-SCALED 0/0 | `winding_transition_0_over_0.py | runs successfully with local copy of winding_phase_diagram.py; all gates PASS, artifact written to data/ | CONCRETE (instrument) | (path)** |
| ZeroZero family: the removable 0/0 catalogue (zero_zero_family_0_over_ | `zero_zero_family_0_over_0.py` | exits 0; 13 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| Riemann zeta functional equation | `zeta_functional_eq_0_over_0.py` | exits 0; 1 PASS/SUPPORTED verdict line(s) | **CONCRETE** |
| ZILBER-PINK CONJECTURE | `zilber_pink_0_over_0.py` | exits 0; 3 PASS/SUPPORTED verdict line(s) | **CONCRETE** |

## Paper provenance register (P2 item 9, audited this pass)

Each of the 7 `.tex` essays in `papers/` was audited: cited scripts located
and re-run, numbers compared, claims cross-checked against this ledger and
`MillenniumBridge.lean`.  Each essay now carries a provenance addendum.
| Paper | Verified/reproduced | Status tier / disposition |
|---|---|---|
| `ns_proof.tex` | close_the_gap.py, final_proof.py, r3_extension.py, ns_r3_proof.py all run clean; 0.0088/0.0089 ratios, PS integrals 0.061455/0.646745/1.343262, C_max 0.0321/0.0227 exact | FRAMEWORK-ARGUMENT; numeric closures (alpha=0.8427, L1 -0.1684) are single-run, endpoint Serrin (2,inf) is delicate; addendum flags this |
| `ym_mass_gap.tex` | ym_rigorous_verification, ym_fold_singularity/verification, ym_allloop_ds, ym_constructive all match | ONE-LOOP + NUMERICS; Delta=0.450 (one-loop table) vs 0.671 (OS script) are distinct models, both real; fold values now dual-registered; constructive YM OPEN |
| `mass_gap_predictions.tex` | mass_gap_calculator (6 tests), universal_mass_gap (12+12+5), thirring_gn_crossover (min 2.500818/max 18.253056), rh_li_correct, de_branges_extended all match | SYNTHESIS; "Proved/Verified" cells corrected to framework-level; RH/BSDâ‰¥2/constructive-YM/Goldbach OPEN |
| `universal_impedance.tex` | universal_impedance (5 0/0, 2 poles, 1 discontinuity; c=2.0, R_th=50.0, chi=88913.97, -i/0.1), rh_li_correct, rh_conductor_ratio, bsd_rank2, goldbach_large all match | ESSAY-CONSISTENT; already honest in its closing; RH/BSD/YM remain OPEN |
| `toomre_millennium.tex` | toomre_universal gives Q_MW=6.2e-7, Q_z2=3.7e-7, Q_IMLup=6.44e9, 14 resonances | **CORRECTIONS**: Gamma at Q=1 is regular (not 0/0); Delta=lambda_c/(1-Q) is a POLE (not removable); measured exponents beta=0.424/nu~0 do NOT reproduce mean-field 1/2,1; Millennium connections are analogy, YM/BSD OPEN |
| `spiral_mass_gap.tex` | spiral_mass_gap.py prints the same analogies; no numeric verification | MODEL-LEVEL ANALOGY; no Millennium settlement |
| `dark_unified.tex` | dark_matter_core.py run | **REFUTED**: "0/0 at sigma_m(N-1)=2pi" is false (sinh(1)=1.175 != 0; rho=0.851 rho0); computed cores 3e-7/1.7e-6 GeV/cm3 do NOT match quoted observed 0.3/0.4 (6 orders); reclassified refuted-claim/qualitative |

## Legacy document provenance register (P2 item 9, this pass)

All 33 `THE_*_0_OVER_0.md` and all 67 `papers/*.pdf` classified by
provenance.  Every script citation below resolves (basename) under
`02_Experimental_Implementations_and_Verification/`.

**THE_*_0_OVER_0.md (33).**  21 backed 1:1 by a cited script + test that
both resolve: **19** under `02_Dark_Energy_0_0_Framework/`, **2** under
`06_Miscellaneous_Experiments/` (`hermite_biehler_proof`, `interlacing_de_branges`;
count verified programmatically on 2026-10-07).  The remaining 12 are
REFRAMING-ESSAYS citing neither script nor test and carrying no
repo-computation claims: Atiyah-Singer, Chern-Gauss-Bonnet,
H-theorem/navier-stokes, Knot invariants, Millennium Prize, Modular forms,
Poincare, QFT, Random matrix theory, Riemann-Roch, Selberg trace formula,
Selberg zeta function.  For the 21 backed ones the cited test name matches a
`test_*` inside `test_solvable_theorems.py` (checked programmatically).

Per-document rows for the 21 backed `THE_*_0_OVER_0.md` (script + matching
`test_*` both resolve and the test executes the script's verdict fields):

| Document | Cited script | Backing test | Status |
|---|---|---|---|
| `THE_ABC_CONJECTURE_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/abc_conjecture_0_over_0.py` | `test_abc_conjecture_0_over_0` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_ARAKELOV_GRR_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/arakelov_grr_0_over_0.py` | `test_arakelov_grr` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_ARAKELOV_THEORY_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/arakelov_theory_0_over_0.py` | `test_arakelov_theory` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_COLMEZ_CONJECTURE_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/colmez_conjecture_0_over_0.py` | `test_colmez_conjecture` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_EXPLICIT_FORMULA_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/explicit_formula_0_over_0.py` | `test_explicit_formula` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_FALTINGS_THEOREM_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/faltings_theorem_0_over_0.py` | `test_faltings_theorem` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_GROMOV_NON_SQUEEZING_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/gromov_non_squeezing_0_over_0.py` | `test_gromov_non_squeezing` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_IWASAWA_MAIN_CONJECTURE_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/iwasawa_main_conjecture_0_over_0.py` | `test_iwasawa_main_conjecture` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_LANGLANDS_PROGRAM_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/langlands_program_0_over_0.py` | `test_langlands_program` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_MANIN_MUMFORD_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/manin_mumford_0_over_0.py` | `test_manin_mumford` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_MONTGOMERY_ODLYZKO_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/montgomery_odlyzko_0_over_0.py` | `test_montgomery_odlyzko` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_NON_COMMUTATIVE_GEOMETRY_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/non_commutative_geometry_0_over_0.py` | `test_non_commutative_geometry` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_SATO_TATE_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/sato_tate_0_over_0.py` | `test_sato_tate` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_SCHANUELS_CONJECTURE_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/schanuels_conjecture_0_over_0.py` | `test_schanuels_conjecture` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_SHIMURA_TANIYAMA_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/shimura_taniyama_0_over_0.py` | `test_shimura_taniyama` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_TQFT_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/tqft_0_over_0.py` | `test_tqft` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_UNIFORM_BOUNDEDNESS_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/uniform_boundedness_0_over_0.py` | `test_uniform_boundedness` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_VOJTA_CONJECTURE_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/vojta_conjecture_0_over_0.py` | `test_vojta_conjecture` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_ZILBER_PINK_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/02_Dark_Energy_0_0_Framework/zilber_pink_0_over_0.py` | `test_zilber_pink` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_HERMITE_BIEHLER_PROOF_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/hermite_biehler_proof.py` | `test_hermite_biehler_proof` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |
| `THE_INTERLACING_DE_BRANGES_0_OVER_0.md` | `02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/interlacing_de_branges.py` | `test_interlacing_de_branges` (executes the cited script and asserts its verdict fields) | **CONCRETE (doc-claim)** |



**papers/*.pdf (67).**  Provenance by backing:
- 3 TEX-PEER (peer of the audited `.tex` in this folder): `dark_unified`,
  `spiral_mass_gap`, `toomre_millennium`.
- 57 SCRIPT-BACKED: name-mapped 1:1 to a `*.py` that resolves under
  `02_Experimental_Implementations_and_Verification/`.
- 7 QUALITATIVE (no same-named script): `consciousness_gamma`, `honest_audit`,
  `language_meaning`, `millennium_prize_proofs`, `prebiotic_origin`,
  `quantum_entanglement`, `zero_to_zero`.

NULL result (disclosed): while the PDFs' names are backed, individual claims
INSIDE each of the 67 PDF texts have not been machine-reproduced; the
non-peer PDFs remain speculative-application essays whose content-level
verification is an open item, not a claim of verification by this table.

Script corrections shipped with this pass: `rh_li_correct.py` (RH declared
OPEN; Li iff-checks all n), `toomre_critical.py` (measured exponents do not
confirm mean-field; honest wall printed).

## Persistence standard re-audit (suite + manifest, 2026-10-07)

**Local-vs-central divergence resolved.**  The 19 JSONs under
`02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/data/`
were MD5-compared against the central collection: 17 byte-identical; the 2
mismatches (`toomre_critical_corrected.json`, `toomre_universal.json`) differ
only by timestamp and, for the former, 1 ULP in `beta`
(0.4238728739847583 vs ...4). Central copies are authoritative; no refresh
needed.  (Notable: the central artifacts are committed at LEGACY paths
`data/*.json` and `experiments/data/*.json` in HEAD; the local dirs are the
emitters' scratch roots.)

**DATA_MANIFEST.json reclassified 3 artifacts.** `toomre_critical_corrected.json`,
`toomre_universal.json`, `spiral_mass_gap.json` were listed `unreproducible`
only because their scripts build write paths via `os.path.join(OUTPUT_DIR,
...)`, invisible to `ARTIFACT_RE`.  Deterministic regeneration was verified
(byte-identical reruns, timestamps excepted); they were moved to
`recreatable` with script mappings.  Counts now `tracked 301 / recreatable
151 / unreproducible 108`.  `toomre_critical_exponents.json` stays
unreproducible (no writer exists).

**`regen_data.py` emitter detection repaired.**  `_dark_energy_sources()`
required `_central_data_dir()` in source, which NO current script contains, so
it mapped 0 of its claimed DE sources.  Detection now keys on the emit line
(quoted `data` token + quoted `*_data.json` on the same line), adding ~23 DE
artifacts to the map.

**Persistence gate re-measured with fresh-clone semantics.**  After the above
fixes, `test_fresh_clone_would_not_depend_on_this_machine` still measured 54
"lost" artifacts because `tracked_files()` filters to data roots present in the
CURRENT worktree, and the mid-reorg worktree has deleted (but still HEAD-tracked)
legacy `data/` trees.  True fresh-clone partition of the 273 test-referenced
artifacts: 232 committed in git at some path (a clone checks them out), 41
regenerable via `--regen-all`, **0 neither** -- i.e. zero unrecoverable.  The
test now adds "committed anywhere in git" to the recoverable set (real
fresh-clone semantics) and keeps the audited budget of 18 as a ratchet.

**Full suite (2026-10-07).**  `python -m pytest`: **1129 passed, 1 skipped,
0 failed** in 15:53.

**Open item (disclosed):** the directory reorganization is not concluded on
this branch -- 1861 legacy-path tracked files are unstaged deletions and the
301 manifest-tracked central artifacts are untracked at their new path.  When
the reorg commit is made, the central tracked set should be `git add`ed so
`tracked_files()` resolves 301 under the canonical root, matching the manifest.

## Log 0/0 micro-lemma (ZeroZero.lean + runtime gates, 2026-10-08)

A certified-Lean lane for the two log-flavoured 0/0 claims, in the
`PunoCalculus.Removable` idiom (limits on the punctured neighbourhood only;
never evaluating AT the point).  All theorems `#print axioms` to exactly
`[propext, Classical.choice, Quot.sound]`; `lake build PunoCalculus` green
(8730 jobs).

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Entropy term `pÂ·log p`: value `0*log 0 = 0`, removable at `p = 0`, zero-outcome contributes 0 | `PunoCalculus/ZeroZero.lean` (`entropy_removable_value`, `entropy_term_continuous`, `entropy_removable_zero`, `entropy_sum_zero_outcome`) | `shannon_entropy_0_over_0.py` gate: `0*log(0) removable: True`, MI/KL/verdict SUPPORTED (exit 0) | **CONCRETE (formalised)** |
| `log(1+x)/x -> 1` at `x = 0` (real) | `ZeroZero.lean` (`log_one_add_div_tendsto_one`, via `HasDerivAt.log` of `1+Â·` at 0) | `log_limits_0_over_0.py` gate 1: `PASS: log(1+x)/x at x=0: 0/0, removable=1` (exit 0) | **CONCRETE (formalised)** |
| `Complex.log(1+z)/z -> 1` at `z = 0` (`slitPlane` branch: `z â†¦ 1+z` stays in the branch near 0, `1 âˆˆ slitPlane`) | `ZeroZero.lean` (`clog_one_add_div_tendsto_one`, via `HasDerivAt.clog`) | same `log_limits_0_over_0.py` gate (complex branch of the same 0/0) | **CONCRETE (formalised)** |
| **MISLABEL CORRECTION: the PNT "pole" test is âˆž/âˆž, not 0/0** | `prime_number_theorem_0_over_0.py` Test 4 (`prime_number_theorem_0_over_0.py:147-164`) + central `prime_number_theorem_0_over_0_data.json` | Both `1/log(x)` and `1/(x-1)` -> +âˆž at `x -> 1+`, so `1/log(x) / (1/(x-1))` is âˆž/âˆž (removable = 1); only the inner pair `(x-1), log(x)` -> 0.  Key renamed `pole_0_over_0` -> `pole_inf_over_inf`, note rewritten; script re-run SUPPORTED (exit 0).  No Lean `(x-1)/log x` theorem added: deferred (inverse-division bookkeeping exceeds this pass's scope) | **CORRECTED (was a mislabelling)** |
| The three 0/0 gate scripts emit `<cwd>/data/` (an uncommitted path under `02_Dark_Energy_0_0_Framework\`) | `shannon_entropy_0_over_0.py`, `log_limits_0_over_0.py`, `prime_number_theorem_0_over_0.py` | ran with a created local `data/`; the committed central copies live under `03_Data_and_Observational_Resources\02_Experimental_Data_Collections\` (mirror updated by hand for the PNT key) -- regenerability path drift disclosed, not yet unified | **CONCRETE (execution only, disclosed)** |

## ZeroZero removable-0/0 family (ZeroZero.lean + family gate, 2026-10-08)

Phase-3 expansion of the certified-Lean 0/0 lane: `PunoCalculus/ZeroZero.lean`
grows from 6 to 17 theorems, each `#print axioms` = exactly
`[propext, Classical.choice, Quot.sound]`; `lake build` green (8730 jobs, zero
warnings).  New runtime gate `zero_zero_family_0_over_0.py` re-derives every
family value on shrinking lattices and emits the central artifact
`zero_zero_family_0_over_0_data.json` via `_central_data_dir()` under
`03_Data_and_Observational_Resources\02_Experimental_Data_Collections\`
(regenerable: `regen_data.build_map()` resolves it to the script).  New
`test_zero_zero_family_gate.py` pins per-key `passed`, the removable values,
and the `lean_module`/theorem correspondence.

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| KL 0/0 at `P = Q = Bernoulli(1/2)`: `KL = 0*log(1) = 0` | `ZeroZero.lean` (`kl_zero_zero_tendsto_zero`) | `zero_zero_family_0_over_0.py`: `PASS: KL(p||q) at p=q=Bernoulli(1/2): 0/0, removable=0` (exit 0) | **CONCRETE (formalised)** |
| `sin(x)/x -> 1` at `x = 0` | `ZeroZero.lean` (`sin_x_div_tendsto_one`) | family gate: `PASS: sin(x)/x at x=0: 0/0, removable=1` | **CONCRETE (formalised)** |
| `(1-cos(x))/x^2 -> 1/2` at `x = 0` | `ZeroZero.lean` (`one_sub_cos_div_sq_tendsto_half`) | family gate: `PASS: ... removable=1/2` (stable form `2 sin(x/2)^2/x^2`) | **CONCRETE (formalised)** |
| `(e^x-1)/x -> 1` at `x = 0` | `ZeroZero.lean` (`exp_sub_one_div_tendsto_one`) | family gate: `PASS: (e^x-1)/x at x=0: 0/0, removable=1` | **CONCRETE (formalised)** |
| `tan(x)/x -> 1` at `x = 0` (via `cos 0 = 1` â†©) | `ZeroZero.lean` (`tan_x_div_tendsto_one`) | family gate: `PASS: tan(x)/x at x=0: 0/0, removable=1` | **CONCRETE (formalised)** |
| `log(x)/(x-1) -> 1` at `x = 1` | `ZeroZero.lean` (`log_div_sub_one_tendsto_one`) | family gate: `PASS: log(x)/(x-1) at x=1: 0/0, removable=1` | **CONCRETE (formalised)** |
| `(x-1)/log(x) -> 1` at `x = 1` (the previously-deferred inverse of the PNT âˆž/âˆž pair, now formalised) | `ZeroZero.lean` (`sub_one_div_log_tendsto_one`) | family gate: `PASS: (x-1)/log(x) at x=1: 0/0, removable=1` | **CONCRETE (formalised)** |
| `arcsin(x)/x -> 1` at `x = 0` | `ZeroZero.lean` (`arcsin_x_div_tendsto_one`) | family gate: `PASS: arcsin(x)/x at x=0: 0/0, removable=1` | **CONCRETE (formalised)** |
| `x^x -> 1` at `x = 0+` (`0^0`) | `ZeroZero.lean` (`self_pow_tendsto_one`) | family gate: `PASS: x^x at x=0+: 0^0, removable=1` | **CONCRETE (formalised)** |
| `(1+x)^(1/x) -> e` at `x = 0+` (defining characterisation of `e`) | `ZeroZero.lean` (`one_add_x_rpow_inv_tendsto_e`) | family gate: `PASS: (1+x)^(1/x) at x=0+: removable=e` | **CONCRETE (formalised)** |
| `sin(z)/z -> 1` at `z = 0` in `â„‚` (`sin(i y)/(i y) = sinh(y)/y`) | `ZeroZero.lean` (`csin_x_div_tendsto_one`) | family gate: `PASS: sin(z)/z at z=0 (complex): 0/0, removable=1` | **CONCRETE (formalised)** |

## AI-performable professions -- benchmark plumbing fixes (2026-10-08)

Audit-of-the-gates pass on the professions benchmark: it verified *programmatic
agreement* (runner -> JSON artifact -> tests), it had never verified the runner
writes to the *committed* artifact, and the count assertions were frozen to the
dataset in force at the time they were written.

| Fix | Files | Independent check | Status |
|---|---|---|---|
| Runner now writes to the committed central artifact, not `<runner>\..\data\` (a nonexistent local dir) | `07_Interdisciplinary_Connections_and_Frameworks\02_Mathematical_Physics_Connections\ai_performable_professions.py` (`DATA` = `REPO_ROOT\03_Data_and_Observational_Resources\02_Experimental_Data_Collections`) | re-run: `wrote ...\03_Data_and_Observational_Resources\02_Experimental_Data_Collections\ai_performable_professions_data.json`, exit 0 | **CONCRETE (fixed)** |
| Schema + provenance block in the persisted JSON (deterministic, no timestamps -- byte-identical on regeneration) | `ai_performable_professions.py` (`"schema"`, `"provenance"` keys) | emitted artifact contains both blocks | **CONCRETE (fixed)** |
| CSV export, schema-stable (profession rows + optional task rows), pinned by a round-trip test | new `professions/export.py`; `puno-mandates export [--out PATH] [--tasks]` subcommand in `puno_app/mandates_server.py` | `test_export_csv_matches_report` (round-trip vs `build_report()`); CLI export exit 0, both CSVs written | **CONCRETE (fixed)** |
| Packaging: `puno_app/mandates_server.py` inserted `01_Lean` on `sys.path`, not the package dir -- `report`/`serve` worked only via `PYTHONPATH` | `puno_app/mandates_server.py` (`PROF_SRC` = repo-root `...\02_Mathematical_Physics_Connections`, inserted on `sys.path`) | `python -m puno_app.mandates_server report` and `export --tasks` exit 0 with no `PYTHONPATH` | **CONCRETE (fixed)** |
| Frozen count assertions un-pinned to dataset-derived internal consistency (counts legitimately track the stated [hypothesis] decompositions) | `test_professions_mandate.py::test_report_status_counts_match_dataset`; `test_solvable_theorems.py::test_ai_performable_professions`, `test_mandate_report` | all affected tests pass; counts on this pass: A=5, B=2, C=5, D=2 (unchanged, but no longer asserted) | **CONCRETE (fixed)** |
| (emanation toolchain) `transformer_proposer.py` looked for the scratch model at the pre-reorg `02_Experimental_Implementations_and_Verification\sfiles\` -- the canonical copy moved to `07_...\02_Mathematical_Physics_Connections\sfiles\`, so `test_professions_audit.py::test_drift_on_professions_table_tamper` failed `from block import TransformerBlock` | `02_Experimental_Implementations_and_Verification\06_Miscellaneous_Experiments\emanation\transformer_proposer.py` (sys.path candidates now `_REPO` + canonical `07_.../02_Mathematical_Physics_Connections/sfiles` + legacy fallback, inserted only when present) | `test_professions_audit.py` + `test_origin_consistency_window_n7.py` both green; note: the suite relies on `pip install -e .` (`__editable__.puno_calculus` finder) mapping `experiments.emanation` etc. -- a bare clone needs the editable install | **CONCRETE (fixed)** |

## Known non-concrete zones (disclosed)

- docs/archive_legacy/: quarantined pre-audit artifacts, disclaimed
- docs/papers/: 74 files (67 PDF + 7 TEX) -- speculative application and essay
  papers; AUDITED and CLASSIFIED on this pass (2026-10-07): 7 TEX peer the
  audited framework essays; 57 PDF script-backed by name, 3 TEX-peers, 7
  qualitative; PDF text-level claims NOT individually reproduced (open item)
- Tier A walls (Kolmogorov uniform bound, RH positivity direction,
  constructive YM, BSD rank>=2, Hodge cycles, Goldbach minor arcs,
  sieve parity, Collatz, P vs NP lower bound): OPEN, labeled open everywhere




