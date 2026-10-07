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
| Cosmology - N7 origin window | `OriginWindow.lean`, `origin_consistency_window_n7.py`, 71 tests | **FORMALIZED** (18+18 theorems; affine law, divergence, three-origins capstone, exact curvature law at `SOf` level) + CONCRETE numeric | `VERIFICATION_LEDGER` / N7 | None: the exact-law row is now formalised in `exp(-S)` form; remaining N7 extension candidates (SREI/FVEI sign test) are observation-blocked by design |
| Acoustics - N6 zero flow | `AcousticZeroFlow.lean`, `acoustic_zero_flow_n6.py` | **FORMALIZED** (`thetaGenOver_zero_iff`, `overdamped_unique_zero`: `A > 1` zero set is EXACTLY `{ artanh (-(a w/b))/w }`; `artanh = atanh` of the experiment) + **CONCRETE (numeric)** | `VERIFICATION_LEDGER` N6 | None (the shared `SOf`-level exact law is formalised on the N7 side, item 1) |
| Fluid mechanics - Navier-Stokes | NS programs, `CascadeRatio.lean`, `MillenniumBridge.lean`, `fcc2 NavierStokes*` | **CONCRETE (numeric)** for cascade ratios and the finite-action-step bounds; global-regularity claim is a proof-style document, not a formal object | `VERIFICATION_LEDGER` NS | Formalize the Fourier bound `\|\|u\|\|_inf^2 <= 4EZ` and the Prodi-Serrin integral finiteness as statements (today numeric + hand proof) |
| Quantum gravity / asymptotic safety | `litim_flow.py`, `flow_pole_*`, `two_loop_cc`, `cusp_to_higgs`, winding instruments | **CONCRETE (numeric)** for the RG lane (reproductions of `arXiv:0705.1769`); framework-synthesis claims stay model-level | `VERIFICATION_LEDGER` QG | None obvious; instrument claims depend on numeric coefficient scans that are hard to make first-class Lean statements |
| Cosmology - observable lane | sound horizon, acoustic scale, birefringence, sigma8, DM cores, H0 | **PIPELINE / CONFRONTED / TENSION (EXT.)**; inputs primary-sourced | `VERIFICATION_LEDGER` refs | None; these are referee gates, not theorems |
| Particle physics - mass gaps | YM, Schwinger, Thirring-GN crossover, SU(2) 2+1D, universal mass gap | **CONCRETE (numeric)** formula reproductions; `MassGap.lean` exists but paper-level YM claims are UNAUDITED | `VERIFICATION_LEDGER` mass-gap family | Removable-value lemma for the universal `M = Lambda/sinh(2 pi/(g_eff^2(N-1)))` crossover at the circuit/0/0 level |
| Number theory - Goldbach / twin / Collatz | `Goldbach.lean`, `TwinPrime.lean`, `TwinRingLaws.lean`, `Collatz.lean` | **CONCRETE (numeric)** for Goldbach <= 100K; Collatz **OPEN**; twin-prime Lean files formalize laws, no primality claim found | `VERIFICATION_LEDGER` Goldbach; Collatz OPEN | Goldbach computational bound as a certificate statement; do NOT advance a twin-prime claim |
| Riemann hypothesis / zeta | RH Lean module (`NewmanFlow` etc.), `de_branges_extended.py`, `rh_li_correct.py`, `RH_PROOF_AUDIT.md` | **CONCRETE (numeric verification)**; "RH TRUE via Li" is a verification of `lambda_n > 0` up to n=30, NOT a formal proof; formal proof **OPEN** | `VERIFICATION_LEDGER` De Branges/RH; `RH_PROOF_AUDIT.md` | The Li-criterion equivalence itself as a formal statement, separated from the finite verification |
| Complexity - P vs NP | `PvsNP.lean`, `p_np_contour.py`, `p_np_flow.py` | Constructive part **OPEN (conceptual wall stated)**: identity exact, no polynomial compilation | `VERIFICATION_LEDGER` P vs NP | Formalize the negative statement "no merging theorem for general formulas known" + the exact-for-N statements |
| Arithmetic geometry - BSD | `BSD.lean`, `bsd_extended.py` | **CONCRETE (numeric)** for 3 LMFDB curves; conjecture **OPEN** | `VERIFICATION_LEDGER` BSD | None; curve checks are numerical |
| 0/0 universal mathematics | `universal_impedance.py`, `circuit_*.py`, `mass_gap_calculator.py` | **FORMALIZED** (`PunoCalculus.Removable`: `removable_limit` + `quadratic_removable` + `impedance_crosszero`) + **CONCRETE (numeric)** for the 7-system register (5 removable 0/0, 2 poles, 1 discontinuity) | `VERIFICATION_LEDGER` impedance/circuit | N6 `A > 1` single-zero theorem; mass-gap crossover formula at the circuit/0/0 level |
| Applied 0/0 predictors | grokking, climate tipping, DM core, muon g-2 | **CONCRETE (numeric)** on their own data sets | `VERIFICATION_LEDGER` applied rows | None; data instruments |
| Dark Energy 0/0 framework | `02_Dark_Energy_0_0_Framework` (135 scripts) | **REGISTERED** (`VERIFICATION_LEDGER` section added): 17/18 `*_0_over_0.py` run clean and write to the central collection; 3 sizer scripts (`air_sizing`, `rainwater_sizing`, `standby_efficiency`) had a broken `packaging.utilities` import, all FIXED and verified; 132 scripts still have no per-script ledger rows; `dark_unified.tex` is a paper, not a verified artifact | `VERIFICATION_LEDGER` Dark Energy section | Per-script ledger rows; N7 methodology applied field-wide |
| Speculative math documents | 33 `THE_*_0_OVER_0.md` (ABC, Arakelov, Langlands, Faltings, Sato-Tate, Selberg, ...) | **CLASSIFIED** (P2 item 9): 21 backed 1:1 (script + `test_*` both resolve; 17 under `02_Dark_Energy_0_0_Framework`, 4 under `06_Miscellaneous_Experiments`); 12 reframing-essays with no computation cited (see ledger register) | `VERIFICATION_LEDGER` legacy-provenance register | Add per-document ledger rows for the 21 backed ones only |
| Application / essay papers | `papers/` 74 files (67 pdf + 7 tex) | **CLASSIFIED** (P2 item 9): 7 `.tex` audited + provenance addenda; 3 PDF peer the audited `.tex`; 57 PDF script-backed by name; 7 qualitative; PDF text-level claims NOT individually reproduced (open item, disclosed) | `VERIFICATION_LEDGER` paper-provenance register + non-concrete zone | Content-level verification of the 57 script-backed PDFs, deferred |
| Legacy Lean tree | `01_Lean/fcc2/Millennium-Prize-Problem-Lean-4-Proof/` (YangMills, RiemannHypothesis, PvsNP, NavierStokes, Hodge, BSD, ...) | **UNAUDITED / status unknown** - a second Lean tree duplicates the canonical `PunoCalculus` modules; two trees claiming coverage conflicts | this document | Resolve: legacy snapshot or live module; then either reconcile or quarantine |

## Roadmap

P0 - machine-check next (bounded, provable cores, matching the N7 standard):

1. **N7 exact law at the `SOf` level** - close the one numeric-only row in the
   flagship node.
   **[DONE]** `OriginWindow.lean` now carries `epsExact` plus four theorems at
   the `SOf` level (`epsExact_SOf_factor` factors the aggregate two-era law over
   eras; `epsExact_sigma_zero` pins the `- sigma` shift as the whole difference
   from the leading law; `epsExact_leading_ratio` and `epsExact_radius_ratio_sq`
   make the `n7b`/`n7c` ratio laws exact identities).  The closed form is
   formalised in the equivalent `exp(-S)` form (`eps = 1/(D e^(-S) - sigma)`,
   `S = stiffness w * n`, so `e^(-S) = a^(-(1+3w))`) precisely to avoid the
   variable-exponent-on-uncontrolled-sign-base obstruction the file had
   documented; the direct `a^r` form remains numeric-only.  Axioms
   `[propext, Classical.choice, Quot.sound]` only (`#print axioms` checked);
   `lake build PunoCalculus.Cosmology.OriginWindow` green.
2. **N6 `A > 1` single-zero branch** - the same discipline applied to the
   acoustic node. **[DONE]** `thetaGenOver_zero_iff` (zero set exactly
   `{ artanh (-(a w/b))/w }` under `0 < w`, `b != 0`, `|b| > |a| w`) and
   `overdamped_unique_zero` (`∃! t` in `thetaGen`'s `w2 < 0` branch) in
   `AcousticZeroFlow.lean`. Axioms `[propext, Classical.choice, Quot.sound]`;
   the lemma `artanh = atanh` notation is the experiment's `atanh`.
3. **Removable-value lemma for the 0/0 family** - the single most replicated
   claim of the framework (`lim` equal to the physical value at the 0/0) as a
   theorem, not a script print. **[DONE]** `PunoCalculus.Removable` in
   `01_Lean/PunoCalculus/Removable.lean`: `removable_limit` (cancel-then-limit,
   `𝓝[≠]`-punctured, `g` continuous), `quadratic_removable` (`(x²-a²)/(x-a) -> 2a`
   — the `(ω-ω₀)`-type cancellation), `impedance_crosszero` (`m ω₀ - k/ω₀ = 0`,
   System 1 of `universal_impedance.py`). Axioms `[propext, Classical.choice,
   Quot.sound]`; module builds clean in `lake build PunoCalculus`.

P1 - statement-grade formalization:

4. Li-criterion equivalence for the RH verification program (proof stays OPEN).
5. PvsNP negative term ("no polynomial compilation known") formalized as an honest
   OPEN statement, never as a resolution.
6. Goldbach computational-certificate boundary for the extended checks.

P2 - adjudication before expansion:

7. Resolve `fcc2` legacy Lean tree vs canonical `PunoCalculus`.
   **[DONE]** Verdict - **independent pedagogical/analogy project, quarantine,
   do not reconcile**:
   * it is a SEPARATE lake project (`lakefile.toml` name
     `millennium-prize-problem-lean-4-proof`, own `.lake`), namespaces
     `UniversalSingularity` / `PunoTwin`, none of which appear in `PunoCalculus`;
     the canonical `lake build PunoCalculus` never compiles it;
   * its own README declares "This project does NOT solve the Millennium Prize
     Problems": modules are `Q`-model vocabulary assignments; the one nontrivial
     theorem is `godForce_iff_Q_eq_one`; `Main/Solution/Challenge` are entry
     points with disclaimers; bridge modules carry explicit `sorry` gap markers
     (`RiemannHypothesisReal`, `PvsNPReal`, `YangMillsReal`, `NavierStokesReal`,
     `HodgeConjectureReal`, `PoincareConjectureReal`, `BSDReal`, `HilbertPolya`,
     ...); `BSD37a1.lean` is the only fully-proved concrete analogue (rank-one
     `37a1` arithmetic, no actual `sorry`; one prose mention);
   * this is CONSISTENT with canonical `MillenniumBridge.lean` ("NOT SETTLED BY
     THIS PROJECT"); no claim conflict exists, so nothing to merge.  Caution is
     recorded: never import `UniversalSingularity`/`PunoTwin` modules from
     canonical code, and keep the nested project out of aggregate claim sets.
     Register as **UNAUDITED-INDEPENDENT** (self-described, `sorry`-flagged,
     provenance intact, not load-bearing for `PunoCalculus`).
8. Repair 18 stale `../data` scripts and register the Dark Energy field in the
   ledger.
   **[DONE - with a correction to the premise]** The "18 stale `../data`
   scripts (soft fail)" finding was WRONG in its detail: `rg` matched prose.
   Verified facts:
   * 17 of the 18 `*_0_over_0.py` scripts RUN CLEAN (exit 0) and write their
     artifacts to the central collection
     (`03_Data_Observational.../02_Experimental_Data_Collections`); their
     `../data` occurrences are HISTORICAL COMMENTS explaining a pre-reorg
     `../data` sibling that no longer exists, beside the `_central_data_dir()`
     upward-search fix already in the code (sample: `entropy_condition_0_over_0.py`);
   * the one real defect in the set was `air_sizing.py` import resolution:
     `from packaging.utilities import ...` resolved to PyPI `packaging` (or
     nothing) because the repo module lives at
     `06_Configuration_and_Metadata/02_Data_Manifest_and_Processing`.
     The same defect was found in `rainwater_sizing.py` and
     `standby_efficiency.py`.  All THREE are fixed with an upward search for the
     repo's `packaging/utilities.py` and now run clean, writing to the central
     collection (`air_sizing_data.json`, `rainwater_data.json`,
     `standby_efficiency_data.json` there).  The central `rainwater_data.json`
     was MISSING before this pass (manifest-listed but absent, so the loader
     test could not resolve it) and is now RECOVERED by regeneration; the
     existing central `air_sizing`/`standby` copies regenerate byte-identical;
   * the Dark Energy field is now REGISTERED in `VERIFICATION_LEDGER.md` with a
     section header + status; per-script claim rows are to be added only as each
     script is individually audited (no manufactured rows).
9. Audit the 7 `.tex` essays (the only load-bearing papers), then classify the
   33 `THE_*_0_OVER_0.md` documents and the remaining PDFs by provenance.
   **[DONE]** All 7 `.tex` audited (18 cited scripts located and re-run; all
   match within rounding); provenance addenda appended to every `.tex`; ledger
   YM rows 106/109/111 corrected; `rh_li_correct.py` (RH declared OPEN, Li
   iff-check is finite) and `toomre_critical.py` (measured exponents do NOT
   confirm mean-field; honest wall printed) patched.  Key dispositions:
   * `dark_unified.tex` **REFUTED** -- "0/0 at `sigma_m(N-1)=2pi`" is false
     (`sinh(1)=1.175 != 0`, `rho_core = 0.851 rho_0`, smooth monotone); its
     own "numerical verification" shows computed cores 3e-7/1.7e-6 GeV/cm^3
     that do NOT match the quoted observed 0.3/0.4 (six orders of magnitude).
   * `toomre_millennium.tex` -- corrections: `Gamma(Q)=kappa*sqrt(1-Q^2)/2` is
     REGULAR at Q=1 (Gamma(1)=0, no 0/0); `Delta=lambda_c/(1-Q)` is a genuine
     POLE, not a removable 0/0; measured exponents beta=0.424 / nu~0 do NOT
     reproduce the claimed mean-field 1/2, 1 (systems numbers DO reproduce:
     Q_MW=6.2e-7, Q_z2=3.7e-7, Q_IMLup=6.44e9, 14 resonances).
   * `mass_gap_predictions.tex` -- Millennium table "Proved/Verified" cells
     reconciled to framework-level (constructive YM OPEN, RH OPEN, BSD>=2 OPEN,
     Goldbach OPEN); `ym_mass_gap.tex` fold values dual-registered and the
     `Delta=0.671` (OS script) vs `0.450` (one-loop table) models separated;
     `ns_proof.tex` flagged as framework-argument with single-run numeric
     closures at the endpoint Serrin step; `universal_impedance.tex`,
     `spiral_mass_gap.tex` confirmed honest/model-level.
   * Register rows 31 and 32 below are updated from UNAUDITED to CLASSIFIED.

## Audit findings shipped with this pass

- `docs/papers/` holds 74 files (67 PDF, 7 TEX), not 28. Ledger non-concrete
  zone corrected.
- Dark Energy 0/0 framework: 135 scripts, no ledger section (largest
  unregistered field in the repo); the earlier "18 stale `../data` scripts"
  figure was a prose-match artifact — 17/18 run clean, and the 3 real import
  defects (`packaging.utilities`) are fixed as item 8.
- `fcc2/` is a second, unaudited Lean tree replicating the canonical modules.
- The RH ledger rows are numeric verifications; any proof-grade reading stays
  OPEN (`RH_PROOF_AUDIT.md` is explicit about this).
- Paper audit (P2 item 9, this pass): `dark_unified.tex` refuted
  (`sinh(1)=1.175 != 0`, computed cores 3e-7/1.7e-6 do NOT match quoted observed
  0.3/0.4 GeV/cm^3); `toomre_millennium.tex` fixed (Gamma(1)=0 regular, mass-gap
  pole not removable 0/0, measured exponents beta=0.424/nu~0 refute mean-field);
  `rh_li_correct.py` and `toomre_critical.py` patched (honest walls); all 7 TEX
  now carry provenance addenda; 33 THE docs and 67 PDFs classified in the ledger
  register (21 backed / 12 reframing; 3 tex-peers / 57 script-backed / 7
  qualitative, PDF text-level claims still open).
- N7 exact law (P0 item 1, this pass): the numeric-only curvature row is now
  formalized at the `SOf` level in `exp(-S)` form (4 new theorems, 3 standard
  axioms), closing the flagged numeric-only row.
- Persistence standard re-audit (continuation pass, 2026-10-07): local data dirs
  byte-match central (17/19; the 2 diffs are timestamp/1-ULP only); 3 toomre/
  spiral artifacts moved `unreproducible` -> `recreatable` in DATA_MANIFEST.json
  with script mappings (regeneration verified deterministic);
  `regen_data.py._dark_energy_sources()` repaired (had required a
  `_central_data_dir()` no script uses, so it mapped 0 DE artifacts; now keys on
  the emit line, ~23 added); the persistence gate measured 54 phantom losses
  that were a worktree-mid-reorg artifact - true fresh-clone partition of 273
  referenced artifacts = 232 committed-in-git + 41 regenerable + 0 neither, so
  the test now counts git-committed-anywhere and keeps budget 18. Full suite:
  1129 passed / 1 skipped / 0 failed (15:53).