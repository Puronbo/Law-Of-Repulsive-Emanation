# Field-by-field audit and formalization roadmap

Register of every research field present in this repository, its current
concreteness tier, and the next machine-checkable step for each. This document
is the map; `VERIFICATION_LEDGER.md` is the single source of truth for claim
status. Nothing here adds a claim: every row below is a restatement of a ledger
row, a directory scan, or an explicit `OPEN / UNAUDITED` label.

Method: a claim is `FORMALIZED` only if it is a theorem in a compiling Lean
module; `CONCRETE (numeric)` only if it has an executable artifact and an
independent check; everything else is `PIPELINE`, `CONFRONTED`, `MODEL-LEVEL`,
`TENSION (EXT.)`, `OPEN`, or `UNAUDITED`. Tiers are the ledger's own.

## Register

| Field | Areas in repo | Status tier | Where recorded | Next formalization candidate |
|---|---|---|---|---|
| Cosmology - N7 origin window | `OriginWindow.lean`, `origin_consistency_window_n7.py`, 71 tests | **FORMALIZED** (18 theorems; affine law, divergence, three-origins capstone) + CONCRETE numeric | `VERIFICATION_LEDGER` / N7 | Exact law `eps = 1/(D a^(-1-3w) - sigma)` at the level of `SOf` (currently numeric-only row) |
| Acoustics - N6 zero flow | `AcousticZeroFlow.lean`, `acoustic_zero_flow_n6.py` | **CONCRETE (numeric)** + partial Lean; A>1 single-zero branch FORMALIZATION **OPEN** | `VERIFICATION_LEDGER` row / N6 | `A > 1`: one zero iff `abs(b) > abs(a) omega`, at `atanh(-a omega/b)/omega` |
| Fluid mechanics - Navier-Stokes | NS programs, `CascadeRatio.lean`, `MillenniumBridge.lean`, `fcc2 NavierStokes*` | **CONCRETE (numeric)** for cascade ratios and the finite-action-step bounds; global-regularity claim is a proof-style document, not a formal object | `VERIFICATION_LEDGER` NS | Formalize the Fourier bound `\|\|u\|\|_inf^2 <= 4EZ` and the Prodi-Serrin integral finiteness as statements (today numeric + hand proof) |
| Quantum gravity / asymptotic safety | `litim_flow.py`, `flow_pole_*`, `two_loop_cc`, `cusp_to_higgs`, winding instruments | **CONCRETE (numeric)** for the RG lane (reproductions of `arXiv:0705.1769`); framework-synthesis claims stay model-level | `VERIFICATION_LEDGER` QG | None obvious; instrument claims depend on numeric coefficient scans that are hard to make first-class Lean statements |
| Cosmology - observable lane | sound horizon, acoustic scale, birefringence, sigma8, DM cores, H0 | **PIPELINE / CONFRONTED / TENSION (EXT.)**; inputs primary-sourced | `VERIFICATION_LEDGER` refs | None; these are referee gates, not theorems |
| Particle physics - mass gaps | YM, Schwinger, Thirring-GN crossover, SU(2) 2+1D, universal mass gap | **CONCRETE (numeric)** formula reproductions; `MassGap.lean` exists but paper-level YM claims are UNAUDITED | `VERIFICATION_LEDGER` mass-gap family | Removable-value lemma for the universal `M = Lambda/sinh(2 pi/(g_eff^2(N-1)))` crossover at the circuit/0/0 level |
| Number theory - Goldbach / twin / Collatz | `Goldbach.lean`, `TwinPrime.lean`, `TwinRingLaws.lean`, `Collatz.lean` | **CONCRETE (numeric)** for Goldbach <= 100K; Collatz **OPEN**; twin-prime Lean files formalize laws, no primality claim found | `VERIFICATION_LEDGER` Goldbach; Collatz OPEN | Goldbach computational bound as a certificate statement; do NOT advance a twin-prime claim |
| Riemann hypothesis / zeta | RH Lean module (`NewmanFlow` etc.), `de_branges_extended.py`, `rh_li_correct.py`, `RH_PROOF_AUDIT.md` | **CONCRETE (numeric verification)**; "RH TRUE via Li" is a verification of `lambda_n > 0` up to n=30, NOT a formal proof; formal proof **OPEN** | `VERIFICATION_LEDGER` De Branges/RH; `RH_PROOF_AUDIT.md` | The Li-criterion equivalence itself as a formal statement, separated from the finite verification |
| Complexity - P vs NP | `PvsNP.lean`, `p_np_contour.py`, `p_np_flow.py` | Constructive part **OPEN (conceptual wall stated)**: identity exact, no polynomial compilation | `VERIFICATION_LEDGER` P vs NP | Formalize the negative statement "no merging theorem for general formulas known" + the exact-for-N statements |
| Arithmetic geometry - BSD | `BSD.lean`, `bsd_extended.py` | **CONCRETE (numeric)** for 3 LMFDB curves; conjecture **OPEN** | `VERIFICATION_LEDGER` BSD | None; curve checks are numerical |
| 0/0 universal mathematics | `universal_impedance.py`, `circuit_*.py`, `mass_gap_calculator.py` | **CONCRETE (numeric)** for the 7-system register (5 removable 0/0, 2 poles, 1 discontinuity) | `VERIFICATION_LEDGER` impedance/circuit | The removable-value theorem: `lim_{x->x0} f(x) = value` for the rational families (highest-replication claim in repo) |
| Applied 0/0 predictors | grokking, climate tipping, DM core, muon g-2 | **CONCRETE (numeric)** on their own data sets | `VERIFICATION_LEDGER` applied rows | None; data instruments |
| Dark Energy 0/0 framework | `02_Dark_Energy_0_0_Framework` (135 scripts) | **AUDIT GAP** - no ledger section; 18 scripts reference `../data` paths (soft fail); `dark_unified.tex` is a paper, not a verified artifact | this document | Audit gap; first fix paths, then register |
| Speculative math documents | 33 `THE_*_0_OVER_0.md` (ABC, Arakelov, Langlands, Faltings, Sato-Tate, Selberg, ...) | **UNAUDITED** - no ledger rows | this document | Classification per document before anything else |
| Application / essay papers | `papers/` 74 files (67 pdf + 7 tex) | **UNAUDITED** - ledger's known-non-concrete zone (count was 28; actual is 74) | this document + `VERIFICATION_LEDGER` non-concrete zone | The 7 `.tex` are the only load-bearing ones; audit those first |
| Legacy Lean tree | `01_Lean/fcc2/Millennium-Prize-Problem-Lean-4-Proof/` (YangMills, RiemannHypothesis, PvsNP, NavierStokes, Hodge, BSD, ...) | **UNAUDITED / status unknown** - a second Lean tree duplicates the canonical `PunoCalculus` modules; two trees claiming coverage conflicts | this document | Resolve: legacy snapshot or live module; then either reconcile or quarantine |

## Roadmap

P0 - machine-check next (bounded, provable cores, matching the N7 standard):

1. **N7 exact law at the `SOf` level** - close the one numeric-only row in the
   flagship node.
2. **N6 `A > 1` single-zero branch** - the same discipline applied to the
   acoustic node.
3. **Removable-value lemma for the 0/0 family** - the single most replicated
   claim of the framework (`lim` equal to the physical value at the 0/0) as a
   theorem, not a script print.

P1 - statement-grade formalization:

4. Li-criterion equivalence for the RH verification program (proof stays OPEN).
5. PvsNP negative term ("no polynomial compilation known") formalized as an honest
   OPEN statement, never as a resolution.
6. Goldbach computational-certificate boundary for the extended checks.

P2 - adjudication before expansion:

7. Resolve `fcc2` legacy Lean tree vs canonical `PunoCalculus`.
8. Repair 18 stale `../data` scripts and register the Dark Energy field in the
   ledger.
9. Audit the 7 `.tex` essays (the only load-bearing papers), then classify the
   33 `THE_*_0_OVER_0.md` documents and the remaining PDFs by provenance.

## Audit findings shipped with this pass

- `docs/papers/` holds 74 files (67 PDF, 7 TEX), not 28. Ledger non-concrete
  zone corrected.
- Dark Energy 0/0 framework: 135 scripts, 18 with stale `../data` references,
  and no ledger section. Largest unregistered field in the repo.
- `fcc2/` is a second, unaudited Lean tree replicating the canonical modules.
- The RH ledger rows are numeric verifications; any proof-grade reading stays
  OPEN (`RH_PROOF_AUDIT.md` is explicit about this).