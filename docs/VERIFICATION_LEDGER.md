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
