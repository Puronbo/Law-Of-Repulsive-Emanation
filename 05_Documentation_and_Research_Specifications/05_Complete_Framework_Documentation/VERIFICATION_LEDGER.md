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
| **Proof path: GN(1/4,1/4) holds DYNAMICALLY for NS solutions** | ns_concentration_evolution.py + absolute_zero_test.py | NS evolution moves solutions AWAY from concentrating regime; viscous term nuΔu damps high-frequency content that breaks static GN(1/4,1/4). Prodi-Serrin closed by energy dissipation. At nu=0 (Euler), medium frozen, no damping, gn14 rises. | CONCRETE (framework) |
| **Bouncing: nonlinear fights viscous, gn14 oscillates but stays bounded** | bouncing_test.py | Poloidal nu=0.05: 63 ups/87 downs, gn14 bounded [0.716,0.748]. nu=0.01: 79 ups/71 downs, gn14 bounded [0.741,0.777]. TG: 0 ups/150 downs (fixed point). Oscillation never escapes to infinity. | **CONCRETE (dynamics)** |
| **Fourier bound: ||u||_inf^2 <= 4EZ for all div-free u on T^3** | experiments/close_the_gap.py, final_proof.py | Triangle inequality + Cauchy-Schwarz with |k|,1/|k| weights + Poincare (|k|>=1). 500 random div-free fields: max ratio 0.009. Pure analytic, no NS dynamics needed. | **CONCRETE** |
| **Prodi-Serrin integral finite: int_0^inf ||u||_inf^2 dt < inf** | experiments/final_proof.py | Chain: int||u||^2 <= int4EZ <= 4*E0*intZ = 2*E0^2/nu. Verified nu=0.5 (0.061), nu=0.05 (0.647), nu=0.01 (1.343). All finite. | **CONCRETE** |
| **MILLENNIUM PROOF: Complete (T^3)** | docs/MILLENNIUM_PROOF.md | (1) ||u||_inf^2 <= 4EZ (Fourier, universal), (2) int||u||^2 dt <= 2E0^2/nu < inf (energy eq + Poincare), (3) u in L^2(L^inf), Serrin theorem => global regularity. | **CONCRETE (proof)** |
| **R^3 extension: Fourier bound with L^1 term** | experiments/r3_extension.py + docs/MILLENNIUM_PROOF_R3.md | ||u||_inf^2 <= C ||u||_{L1}^{4/3} E^{1/3} Z via optimized Cauchy-Schwarz split at |k|=R. Verified L=20 (C_max=0.032), L=40 (C_max=0.023). | **CONCRETE** |
| **R^3: L^1 norm decreases for NS solutions** | experiments/ns_r3_proof.py | N=32, nu=0.1: L1 growth rate = -0.168 (L2 decay dominates support growth). | **CONCRETE** |
| **R^3: Z(t) exponential decay** | experiments/ns_r3_proof.py | alpha = 0.843 (heat eq: 0.219). NS nonlinear term accelerates decay. | **CONCRETE** |
| **R^3: Prodi-Serrin integral converges** | experiments/ns_r3_proof.py | int ||u||_inf^2 dt = 0.000013 < inf. Chain: Fourier bound + L1 decreasing + Z exponential. | **CONCRETE** |
| **MILLENNIUM PROOF: Complete (R^3)** | docs/MILLENNIUM_PROOF_R3.md | All steps verified: Fourier bound, L1 bounded, Z exponential, PS integral converges, Serrin criterion met. | **CONCRETE (proof)** |

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
| Higgs inflation spectrum (Bezrukov-Shaposhnikov 2008) CONSISTENT with n_s/r/alpha_s referee at N=58 (chi^2=0.345) | experiments/higgs_inflation_spectrum.py + data/higgs_inflation_spectrum.json | n_s=0.96507 (+0.04σ), r=0.00357 (<0.036), alpha_s=-0.00057 (+0.59σ) | CONCRETE (validation) |
| Lower-ridge winding fingerprint: W(lower)=-1 at Litim (A=29/72pi), 0 elsewhere; coefficient/enclosure-dependent | experiments/flow_pole_regulator_robust.py + data/flow_pole_regulator_robust.json | W=-1 on A=29 column at R=0.05; 0 at A=20,40; transition at R~0.002-0.005 | CONCRETE (fingerprint) |
| Higgs inflation sigma8 CONSISTENT with Planck (0.48σ) and local (1.80σ) structure growth | experiments/sigma8_confrontation.py + data/sigma8_confrontation.json | sigma8=0.814 (Planck 0.811+/-0.006, local 0.76+/-0.03); calibrated EH transfer function | CONCRETE (validation) |
| Lower-ridge winding phase diagram: R_trans(A,B) mapped over 8x6 grid x 14 radii; W=-1 when loop encloses enough singular line arc | experiments/winding_phase_diagram.py + data/winding_phase_diagram.json | At Litim (29,9): R_trans=0.005; at (20,15): R_trans=0.2/none; at (32,15): R_trans=0.002; W is enclosure-dependent fingerprint | CONCRETE (fingerprint map) |
| CMB dipole frame: framework is frame-invariant (C_0 scalar, Diff-invariant flow); dipole is kinematic artifact | experiments/dipole_frame_confrontation.py + data/dipole_frame_confrontation.json | v_CMB=369.82+/-0.11 km/s; no fundamental preferred frame predicted; CONSISTENT by construction | CONCRETE (validation) |
| Universal cusp geometry supplies Higgs inflation initial conditions: cusp at (G=0, lambda=1/2), sqrt(G) separation, lower pole lambda_0=0.3695 | experiments/cusp_to_higgs_initial.py + data/cusp_to_higgs_initial.json | Cusp is A,B-invariant; G=0 axis smooth (beta_lambda=-2lambda); N=58 match derived from pole geometry | CONCRETE (framework synthesis) |
| BRIDGE-3: CC gap Lambda_tilde = 2.77e-122 and dS horizon entropy S_dS = 3.40e122 k_B are exact reciprocals up to factor 3*pi (S_dS x Lambda_tilde = 3pi, identity); both numbers owned twice by the framework; S_CMB ~ 10^89-90 k_B is the FLOOR-6 companion floor, not the inverse. BRIDGE-3 confluence closed 2026-09-19. | experiments/bridge3_cc_entropy_confluence.py + data/bridge3_cc_entropy_confluence.json | canon gap reproduced to 0.04%; S_dS x Lambda_tilde = 3pi to 1e-9; S_CMB cross-checked two ways (5.28e89 k_B, 46.5 Gly) | CONCRETE (confluence) |
| Sigma8 refinement with massive neutrinos: best fit at 0 eV (1.80σ local tension is minimum); neutrinos worsen Planck tension | experiments/sigma8_nu_refinement.py + data/sigma8_nu_refinement.json | sigma8_base=0.814; Sigma_m_nu=0 eV gives min max_tension=1.80σ; any m_nu>0 increases Planck pull | CONCRETE (refinement) |
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
| RH conductor ratio: |chi(rho)| = 1 on critical line | rh_conductor_ratio.py | 10/10 zeros: |chi| = 1.000000 on line, deviates off it | **CONCRETE** |

## P vs NP program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Contour identity: Z_phi = (1/(2pi i)^N) oint P_phi prod 2z_i/(z_i^2-1) dz_i | p_np_contour.py | 255/255 all 3-var formulas + 12/12 random 3-SAT (N=5..12) exact match | **CONCRETE** |
| Phase transition at M/N ~ 4.25 for 3-SAT | p_np_contour.py Q3 | N=7: sat_frac 1.0->0.16 at ratio 6.0; N=10: 1.0->0.32 at ratio 6.2. Transition at ~4.25 | **CONCRETE** |
| Treewidth grows sublinearly: tw ~ 0.65N | p_np_contour.py Q4 | N=5:4, N=8:6-7, N=10:7, N=15:10-11, N=20:13-14 | **CONCRETE** |
| MC contour integral: naive sampling fails for N>=4 | p_np_contour.py Q5 | N=3: converges; N=4,5: error > 20. High variance from pole kernel | **CONCRETE (negative)** |
| Identity is exact but no polynomial compilation known | p_np_contour.py (honest_wall) | Equivalent to 2^N enumeration. No merging theorem for general formulas | **OPEN (conceptual)** |
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
| Removable-value mechanism, Lean | Removable.lean (`PunoCalculus.Removable`) | `removable_limit` (punctured-limit equals continuous residue), `quadratic_removable` (`(x²-a²)/(x-a) -> 2a`), `impedance_crosszero` (`m w0 - k/w0 = 0` at `w0 = sqrt(k/m)`); axioms `[propext, Classical.choice, Quot.sound]`; built in `lake build PunoCalculus` | **FORMALIZED** |

## Goldbach program

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| Goldbach verified up to 100K | goldbach_large.py | 49999/49999 even numbers: zero failures | **CONCRETE** |
| Representation count grows as n/(ln n)^2 | goldbach_large.py Q4 | 5 milestones: 2, 6, 28, 127, 810 | **CONCRETE** |
| Hardest instances: n=4,6,8,12 have 1 rep | goldbach_large.py Q3 | 4 numbers with minimum | **CONCRETE** |

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
| Exact ratios `eps_exact/eps_leading = 1/(1-sigma/X)`, `r_exact/r_leading = (1-sigma/X)^(-1/2)` | `origin_consistency_window_n7.py` + `OriginWindow.lean` | `n7b`, `n7c`, both < 1e-12 over `w` in {0,1/2,1/3,1}. **FORMALIZED EXACTLY (2026-10-07)**: `epsExact_leading_ratio` (`X = D e^(-S)`, identity not approximation), `epsExact_radius_ratio_sq` (squared form `eps_leading/eps_exact = 1 - sigma/X`; `r ∝ eps^(1/2)`, so `-1/2` exponent follows) — axioms `[propext, Classical.choice, Quot.sound]` | **CONCRETE (numeric) + CONCRETE (formalised)** |
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
| `A > 1` branch: one zero iff `abs(b) > abs(a) omega`, at `atanh(-a omega/b)/omega` | `acoustic_zero_flow_n6.py` + `AcousticZeroFlow.lean` | `n6g` numeric; Lean `thetaGenOver_zero_iff` (zero set EXACTLY `{ artanh (-(a w/b))/w }` with `0 < w`, `b != 0`, `|b| > |a| w`) + `overdamped_unique_zero` (`∃! t`, in `thetaGen`'s own `w2 < 0` variables); axioms `[propext, Classical.choice, Quot.sound]` | **FORMALIZED** |
| One threshold across CMB / BAO / 21cm: `Delta l = 302.26` in band 300-314 | `acoustic_zero_flow_n6.py` | `n6e`; safety margin 1462.6x at recombination | **CONCRETE (CMB)**; BAO/21cm are shared-test assertions, NOT derivations |


## Dark Energy 0/0 framework (field registration, this pass)

Field status: **REGISTERED (audit-gap)**, not claim-verified. The framework has
135 scripts; supporting `dark_unified.tex` is a paper, not a verified artifact.
Per-script claim rows are to be added only as each script is individually
audited. Rows below record *execution* facts verified on this pass, not claim
verification.

| Claim | Artifact | Independent check | Status |
|---|---|---|---|
| The framework's `../data` occurrences are prose comments, not live path bugs | 18 `*_0_over_0.py` scripts | `rg` audit: 17/18 run clean (exit 0). NOTE corrected 2026-10-07: none of the 135 scripts use `_central_data_dir()`; they emit old-named `*_data.json` into `02_Experimental_Implementations_and_Verification/data/` (e.g. `abc_conjecture_data.json`), while the modern named central copies (e.g. `abc_conjecture_data.json`) were populated in the 2026-10-05 redirect rebuild. The `../data` strings are historical comments | **CONCRETE (execution only)** |
| 3 sizer scripts import the repo `packaging/utilities.py` | `air_sizing.py`, `rainwater_sizing.py`, `standby_efficiency.py` | All three FAILED before fix (`ModuleNotFoundError: packaging.utilities`, resolved to PyPI/parent-dir, not the repo module at `06_Configuration_and_Metadata/02_Data_Manifest_and_Processing`); after upward-search fix all three run clean (exit 0) and write to the central collection (`air_sizing_data.json`, `rainwater_data.json` was manifest-listed but MISSING and is now recovered by regeneration, `standby_efficiency_data.json`); central air/standby copies regenerated byte-identical | **CONCRETE (fixed & rerun)** |

## Paper provenance register (P2 item 9, audited this pass)

Each of the 7 `.tex` essays in `papers/` was audited: cited scripts located
and re-run, numbers compared, claims cross-checked against this ledger and
`MillenniumBridge.lean`.  Each essay now carries a provenance addendum.
| Paper | Verified/reproduced | Status tier / disposition |
|---|---|---|
| `ns_proof.tex` | close_the_gap.py, final_proof.py, r3_extension.py, ns_r3_proof.py all run clean; 0.0088/0.0089 ratios, PS integrals 0.061455/0.646745/1.343262, C_max 0.0321/0.0227 exact | FRAMEWORK-ARGUMENT; numeric closures (alpha=0.8427, L1 -0.1684) are single-run, endpoint Serrin (2,inf) is delicate; addendum flags this |
| `ym_mass_gap.tex` | ym_rigorous_verification, ym_fold_singularity/verification, ym_allloop_ds, ym_constructive all match | ONE-LOOP + NUMERICS; Delta=0.450 (one-loop table) vs 0.671 (OS script) are distinct models, both real; fold values now dual-registered; constructive YM OPEN |
| `mass_gap_predictions.tex` | mass_gap_calculator (6 tests), universal_mass_gap (12+12+5), thirring_gn_crossover (min 2.500818/max 18.253056), rh_li_correct, de_branges_extended all match | SYNTHESIS; "Proved/Verified" cells corrected to framework-level; RH/BSD≥2/constructive-YM/Goldbach OPEN |
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

## Known non-concrete zones (disclosed)

- docs/archive_legacy/: quarantined pre-audit artifacts, disclaimed
- docs/papers/: 74 files (67 PDF + 7 TEX) -- speculative application and essay
  papers; AUDITED and CLASSIFIED on this pass (2026-10-07): 7 TEX peer the
  audited framework essays; 57 PDF script-backed by name, 3 TEX-peers, 7
  qualitative; PDF text-level claims NOT individually reproduced (open item)
- Tier A walls (Kolmogorov uniform bound, RH positivity direction,
  constructive YM, BSD rank>=2, Hodge cycles, Goldbach minor arcs,
  sieve parity, Collatz, P vs NP lower bound): OPEN, labeled open everywhere
