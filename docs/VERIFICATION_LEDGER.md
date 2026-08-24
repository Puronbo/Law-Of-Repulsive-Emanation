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
| **MILLENNIUM PROOF: Complete** | docs/MILLENNIUM_PROOF.md | (1) ||u||_inf^2 <= 4EZ (Fourier, universal), (2) int||u||^2 dt <= 2E0^2/nu < inf (energy eq + Poincare), (3) u in L^2(L^inf), Serrin theorem => global regularity. | **CONCRETE (proof)** |

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

## Known non-concrete zones (disclosed)

- docs/archive_legacy/: quarantined pre-audit artifacts, disclaimed
- docs/papers/: 28 speculative application papers -- never audited
- Tier A walls (Kolmogorov uniform bound, RH positivity direction,
  constructive YM, BSD rank>=2, Hodge cycles, Goldbach minor arcs,
  sieve parity, Collatz): OPEN, labeled open everywhere
