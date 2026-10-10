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
| Fluid mechanics - Navier-Stokes | NS programs, `CascadeRatio.lean`, `NavierStokes.lean`, `SelfSimilarExponents.lean`, `MillenniumBridge.lean`, `experiments/stability_harness.py`, `fcc2 NavierStokes*` | **FORMALIZED (statement)** `PunoCalculus.NavierStokes`: Serrin scaling arithmetic as theorems (`serrinScaling 4 6 = 1`, `3 9 = 1`, admissible `(4,6)`/`(3,9)`, `q = 3` excluded), **OPEN WALL** markers (`fourierInfBound`, `prodiSerrinIntegralFiniteCertified = false`, `nsGlobalRegularityOpen = true`); **FORMALIZED (2026-10-10)** `PunoCalculus.SelfSimilarExponents`: four-way dominant balance of the reduced (u1, ω1) system forces `(p,q,s,γ) = (-1,-3/2,-1/2,1/2)` uniquely (Frontier 1 of `Linear Stability of Candidate Swirl Profiles.md`), n-independent (balance system is n-free; diffusion/advection prefactors never change τ-powers), with `selfSimilarProfileExistenceOpen = true` and `typeIINamingCertified = false` honesty markers; **CONCRETE (numeric / QA)** `stability_harness.py`: twin eigensolvers + numerical abscissa + domain scan verified against the closed-form FD spectrum (6 tests); global-regularity claim stays a non-formal proof-style document | `VERIFICATION_LEDGER` NS | None: Serrin arithmetic formalized (2026-10-09), Frontier-1 exponents formalized (2026-10-10); bounded-profile existence at the forced exponents remains OPEN (numeric searches only); Fourier bound and Prodi-Serrin integral remain unproved statements out of principle (the `1/|k|^2` sum diverges on `Z^3`) |
| Quantum gravity / asymptotic safety | `litim_flow.py`, `flow_pole_*`, `two_loop_cc`, `cusp_to_higgs`, winding instruments | **CONCRETE (numeric)** for the RG lane (reproductions of `arXiv:0705.1769`); framework-synthesis claims stay model-level | `VERIFICATION_LEDGER` QG | None obvious; instrument claims depend on numeric coefficient scans that are hard to make first-class Lean statements |
| Cosmology - observable lane | sound horizon, acoustic scale, birefringence, sigma8, DM cores, H0 | **PIPELINE / CONFRONTED / TENSION (EXT.)**; inputs primary-sourced | `VERIFICATION_LEDGER` refs | None; these are referee gates, not theorems |
| Particle physics - mass gaps | YM, Schwinger, Thirring-GN crossover, SU(2) 2+1D, universal mass gap | **CONCRETE (numeric)** formula reproductions; `MassGap.lean` now carries the crossover's removable-0/0 theorem; paper-level YM claims stay UNAUDITED | `VERIFICATION_LEDGER` mass-gap family | None: the crossover lemma is formalized (2026-10-09); the endpoint honesty rows (pole at `a -> 0`, CDM cusp special-case) are deliberately NOT machine-checked |
| Number theory - Goldbach / twin / Collatz | `Goldbach.lean`, `TwinPrime.lean`, `TwinRingLaws.lean`, `Collatz.lean` | **FORMALIZED (finite certificate)** `goldbach_even_4_to_100000` by `native_decide` + **CONCRETE (numeric)** for Goldbach <= 100K; conjecture **OPEN** (`goldbach_conjecture_open := true`); Collatz **OPEN**; twin-prime Lean files formalize laws, no primality claim found | `VERIFICATION_LEDGER` Goldbach; Collatz OPEN | None: certificate boundary done (item 6); do NOT advance a twin-prime claim |
| Riemann hypothesis / zeta | RH Lean module (`NewmanFlow`, `LiCriterion` etc.), `de_branges_extended.py`, `rh_li_correct.py`, `RH_PROOF_AUDIT.md` | **FORMALIZED (statement)** `liCriterionEquiv` + `finitePrefixNeverSettles` (no finite prefix settles the criterion) + **CONCRETE (numeric verification)**; "RH TRUE via Li" is a verification of `lambda_n > 0` up to n=30, NOT a formal proof; formal proof **OPEN** | `VERIFICATION_LEDGER` De Branges/RH; `RH_PROOF_AUDIT.md` | None: Li-criterion statement formalized (item 4); BOTH directions remain OPEN by design |
| Complexity - P vs NP | `PvsNP.lean`, `p_np_contour.py`, `p_np_flow.py` | Constructive part **OPEN (conceptual wall stated)**: identity exact, no polynomial compilation. **FORMALIZED (OPEN marker)** `noPolynomialCompilationKnown` + `compilationWall` (never a negation of P = NP) | `VERIFICATION_LEDGER` P vs NP | None: negative statement formalized as a status marker (item 5); P vs NP remains OPEN |
| Arithmetic geometry - BSD | `BSD.lean`, `bsd_extended.py` | **CONCRETE (numeric)** for 3 LMFDB curves; conjecture **OPEN** | `VERIFICATION_LEDGER` BSD | None; curve checks are numerical |
| 0/0 universal mathematics | `universal_impedance.py`, `circuit_*.py`, `mass_gap_calculator.py` | **FORMALIZED** (`PunoCalculus.Removable`: `removable_limit` + `quadratic_removable` + `impedance_crosszero`; N6 `A > 1` single-zero theorem; mass-gap crossover factor `a/sinh(a) -> 1` in `PunoCalculus.MassGap`) + **CONCRETE (numeric)** for the 7-system register (5 removable 0/0, 2 poles, 1 discontinuity) | `VERIFICATION_LEDGER` impedance/circuit | None at this level
| Applied 0/0 predictors | grokking, climate tipping, DM core, muon g-2 | **CONCRETE (numeric)** on their own data sets | `VERIFICATION_LEDGER` applied rows | None; data instruments |
| Dark Energy 0/0 framework | `02_Dark_Energy_0_0_Framework` (136 scripts) | **REGISTERED + PER-SCRIPT AUDITED** (`VERIFICATION_LEDGER` section, 2026-10-09): 127 scripts run to a PASS/completed verdict (write an artifact), 9 are UNREPRODUCIBLE (missing `../Universals` `manifold`/`litim_flow`, or `winding_phase_diagram` not on path), 1 (`ising_model`) times out >300 s; 3 carry numerical-overflow RuntimeWarnings; 2 report honest negatives/partials (`chi_rho_vacuity` vacuous, `polya_wall_1e8` G1 dependency); each subject theorem remains OPEN. 3 sizer import defects fixed earlier; `dark_unified.tex` is a paper, not a verified artifact | `VERIFICATION_LEDGER` Dark Energy section (per-script table) | Fix the 9 missing-dependency scripts if the `Universals` package is recovered; otherwise they stay disclosed-unreproducible |
| Speculative math documents | 33 `THE_*_0_OVER_0.md` (ABC, Arakelov, Langlands, Faltings, Sato-Tate, Selberg, ...) | **CLASSIFIED + per-document rows added** (P2 item 9 + 2026-10-09): 21 backed 1:1 (script + matching `test_*`; 19 under `02_Dark_Energy_0_0_Framework`, 2 under `06_Miscellaneous_Experiments`) now carry individual ledger rows; 12 reframing-essays with no computation cited | `VERIFICATION_LEDGER` legacy-provenance register (21-row table) | None: 21 backed rows done; the 12 reframing essays intentionally have no computation row |
| Application / essay papers | `papers/` 74 files (67 pdf + 7 tex) | **CLASSIFIED** (P2 item 9): 7 `.tex` audited + provenance addenda; 3 PDF peer the audited `.tex`; 57 PDF script-backed by name; 7 qualitative; PDF text-level claims NOT individually reproduced (open item, disclosed) | `VERIFICATION_LEDGER` paper-provenance register + non-concrete zone | Content-level verification of the 57 script-backed PDFs, deferred |
| Legacy Lean tree | `01_Lean/fcc2/Millennium-Prize-Problem-Lean-4-Proof/` (YangMills, RiemannHypothesis, PvsNP, NavierStokes, Hodge, BSD, ...) | **RESOLVED (P2 item 7): QUARANTINE as UNAUDITED-INDEPENDENT** - separate lake project (own name/`.lake`, namespaces `UniversalSingularity`/`PunoTwin`); its README disclaims solving the Millennium Problems; the one nontrivial theorem is `godForce_iff_Q_eq_one`; bridge modules carry explicit `sorry` gap markers; `BSD37a1.lean` is a fully-proved concrete analogue. Not reconciled (no conflict), not load-bearing: never import its modules from canonical code | this document | None: quarantined; provenance intact |

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
   `overdamped_unique_zero` (`âˆƒ! t` in `thetaGen`'s `w2 < 0` branch) in
   `AcousticZeroFlow.lean`. Axioms `[propext, Classical.choice, Quot.sound]`;
   the lemma `artanh = atanh` notation is the experiment's `atanh`.
3. **Removable-value lemma for the 0/0 family** - the single most replicated
   claim of the framework (`lim` equal to the physical value at the 0/0) as a
   theorem, not a script print. **[DONE]** `PunoCalculus.Removable` in
   `01_Lean/PunoCalculus/Removable.lean`: `removable_limit` (cancel-then-limit,
   `ð“[â‰ ]`-punctured, `g` continuous), `quadratic_removable` (`(xÂ²-aÂ²)/(x-a) -> 2a`
   â€” the `(Ï‰-Ï‰â‚€)`-type cancellation), `impedance_crosszero` (`m Ï‰â‚€ - k/Ï‰â‚€ = 0`,
   System 1 of `universal_impedance.py`). Axioms `[propext, Classical.choice,
   Quot.sound]`; module builds clean in `lake build PunoCalculus`.

P1 - statement-grade formalization:

4. Li-criterion equivalence for the RH verification program (proof stays OPEN).
   **[DONE]** `PunoCalculus.RH.LiCriterion` in
   `01_Lean/PunoCalculus/RH/LiCriterion.lean` (junction target
   `03_Riemann_Hypothesis_Module/RH`): `liCriterionEquiv` (the Li biconditional
   `RH â†” âˆ€ n â‰¥ 1, 0 â‰¤ Î» n` as a parameterized statement; neither direction
   proved), `liPrefixCond`, `liCoeffs30` (exact Float transcription of the 30
   committed coefficients of `rh_li_correct.json`, `n_max=30`, 800 zeros),
   `liPrefix30_positive : liCoeffs30.all (Float.le 0) = true` by `native_decide`,
   and the gap theorem `finitePrefixNeverSettles (k)` -- for EVERY finite bound
   some sequence passes the prefix and fails later (witness
   `fun n => if n = k+1 then -1 else 0`), with `finiteCheck30NotEnough` as the
   `k=30` corollary. `li_criterion_proof_open : Bool := true`; status string
   records the script's honesty clause. Both directions and RH stay OPEN.
5. PvsNP negative term ("no polynomial compilation known") formalized as an honest
   OPEN statement, never as a resolution.
   **[DONE]** `PunoCalculus.PvsNP`: `noPolynomialCompilationKnown : Bool := true`
   (genuinely open), `compilationWall` (verbatim `honest_wall` of
   `p_np_contour.py`), `compilation_wall_recorded` and
   `compilation_wall_is_open_status` by `native_decide`. Absence of knowledge is
   encoded as a status marker/theorem, never as a mathematical negation of
   P = NP. Interpretation strings softened to resolution-free form in
   `millennium_0_over_0.py` + `millennium_data.json`
   (`Q1_p_vs_np.p_vs_np.interpretation`, `Q3` meanings of NS/Hodge/BSD/YM) and
   `p_np_contour.py` + `p_np_contour.json` (`key_insight`); all six Q3
   resolution-flavoured `meaning` strings replaced; numbers unchanged.
6. Goldbach computational-certificate boundary for the extended checks.
   **[DONE]** `PunoCalculus.Goldbach`: Eratosthenes sieve (`markMultiples`,
   `sieveGo`/`sieve`, `isPrimeSieve` -- sieve stores *composite* marks), early-exit
   `goldbachWitness`, `goldbachCertificate limit` (sieve built once),
   `theorem goldbach_even_4_to_100000 : goldbachCertificate 100000 = true` by
   `native_decide`, `certificateBoundary = 100000` (matches
   `goldbach_large.py` MAX), `citedExternalRecord = 4e18` (citation only),
   `certificate_below_citation`, `goldbach_conjecture_open : Bool := true`.
   `goldbach_large.py` `/json` honesty sweep: `key_insight` no longer asserts
   the conjecture as fact, new `honest_wall`; artifact values byte-stable
   (verification/milestones/density unchanged).

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
  figure was a prose-match artifact â€” 17/18 run clean, and the 3 real import
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
- Log 0/0 micro-lemma (2026-10-08): new certified-Lean module
  `PunoCalculus.ZeroZero` -- `pÂ·log p` value/removability/zero-outcome, and
  `log (1+x)/x -> 1` real + complex, all `#print axioms` = the 3 standard;
  runtime gates `shannon_entropy_0_over_0.py` (SUPPORTED) and
  `log_limits_0_over_0.py` (all PASS) re-run clean.  Ledger rows added.  PNT
  mislabelling corrected: the Test 4 "0/0 at the pole" is an âˆž/âˆž ratio
  (both factors -> +âˆž); key renamed `pole_inf_over_inf` in script + central
  artifact, script re-run SUPPORTED; a Lean `(x-1)/log x` theorem is deferred
  as out of scope.  **[Path drift now FIXED 2026-10-09]** the 3 gates
  (`log_limits_0_over_0.py`, `shannon_entropy_0_over_0.py`,
  `prime_number_theorem_0_over_0.py`) plus `rh_li_correct.py`, `p_np_contour.py`,
  `goldbach_large.py` and `goldbach_0_over0.py` emitted `<cwd>/data/`; all seven
  now compute the emit path from `_central_data_dir()` (upward search), re-ran
  exit 0, and every numeric value is unchanged (`log_limits`/`shannon`
  value-identical; `prime_number_theorem` identical modulo JSON `\u221e`
  escaping, restored; `rh_li_correct` value-identical;
  `p_np_contour`/`goldbach_large`/`goldbach_0_over0` only the intended honesty
  strings changed).  Pinned by
  `test_open_status_pins.py::test_path_drift_gates_emit_centrally`.  The wider
  class (many `02_Dark_Energy_0_0_Framework`/`06_Miscellaneous_Experiments`
  scripts still literal `data/...`) remains disclosed and audited per-script,
  not bulk-rewritten.
- ZeroZero removable-0/0 family (2026-10-08): `PunoCalculus.ZeroZero` grows
  6 -> 17 theorems -- `KL` 0/0, `sin(x)/x`, `(1-cos(x))/x^2`, `(e^x-1)/x`,
  `tan(x)/x`, `log(x)/(x-1)`, `(x-1)/log(x)` (the previously-deferred inverse
  of the PNT âˆž/âˆž pair), `arcsin(x)/x`, `x^x`, `(1+x)^(1/x) -> e`, and complex
  `sin(z)/z` -- all `#print axioms` = the 3 standard; `lake build` green (8730
  jobs), zero warnings, temp axiom file deleted.  New gate
  `zero_zero_family_0_over_0.py` re-derives all 13 removable values and emits
  the central artifact via `_central_data_dir()` (regenerable and persisted).
  New `test_zero_zero_family_gate.py`: `summary.supported`, per-key `passed`,
  removable values pinned (`math.isclose`), `lean_module =
  PunoCalculus.ZeroZero` + theorem correspondence asserted; `regen_data`
  resolves the artifact to the script.  Full-suite gate green.
- AI-performable professions -- benchmark plumbing fixes (2026-10-08): the
  runner wrote its verdict artifact to a nonexistent local `../data/`; it now
  writes the committed central copy under `03_Data_and_Observational_Resources\
  02_Experimental_Data_Collections\`, and the JSON gained deterministic
  `schema` + `provenance` blocks.  Added schema-stable CSV export
  (`professions/export.py`, `puno-mandates export [--out] [--tasks]`, pinned
  by a round-trip test).  `puno_app/mandates_server.py` inserted the wrong dir
  on `sys.path` (the `01_Lean` app dir, not the professions package's parent);
  now resolves `PROF_SRC` from the repo root so `python -m puno_app.
  mandates_server report|export|serve` runs with no `PYTHONPATH`.  Frozen
  count assertions (`A==5/D==2/len==14`) replaced by dataset-derived internal
  consistency in `test_professions_mandate.py` and `test_solvable_theorems.py`
  (2 tests) -- counts legitimately track the stated [hypothesis]
   decompositions; current values unchanged (A=5, B=2, C=5, D=2).  Ledger rows
   added; affected tests green.
- P1 statement-grade formalization + honesty sweep (2026-10-09): roadmap items
   4/5/6 closed.  New `PunoCalculus.RH.LiCriterion` (statement + finite check +
   `finitePrefixNeverSettles` gap theorem), `PunoCalculus.PvsNP` OPEN marker
   (`noPolynomialCompilationKnown`, `compilationWall`), and a
   `native_decide` Goldbach certificate `<= 100000` in `PunoCalculus.Goldbach`.
   `lake build` green (8731 jobs, zero warnings).  Axioms: the non-`native_decide`
   theorems are exactly `[propext, Classical.choice, Quot.sound]`; the
   `native_decide` ones additionally carry the compiler-trust
   `native_decide.ax`, exactly as the shipped precedent
   `MillenniumBridge.seven_problems_declared_unsolved` (temp `#print axioms`
   file deleted).  Honesty sweep: `millennium_0_over_0.py`/`millennium_data.json`
   interpretations no longer claim P = NP / NS / Hodge / BSD / YM resolutions;
   `p_np_contour.py`/`json` `key_insight` no longer asserts an unproven `iff`;
   `goldbach_large.py`/`json` `key_insight` no longer asserts Goldbach as fact
   (new `honest_wall`).  New `test_open_status_pins.py` (6 tests) pins all of it
   plus central emit paths.  Six `<cwd>/data/` path-drift emissions unified to
   `_central_data_dir()` with zero numeric drift (see the log-0/0 item above).
- NavierStokes + MassGap statement layers (2026-10-09): new
   `PunoCalculus.NavierStokes` proves the Serrin scaling arithmetic (Serrin-line
   pairs `(4,6)` and `(3,9)`, admissibility, `q = 3` excluded for every finite
   `p`) and records the Fourier bound `||u||_inf^2 <= 4 E Z` + Prodi-Serrin
   integral finiteness as unproved statements with `nsGlobalRegularityOpen = true`
   (OPEN wall, `6`-row `nsFormalizedFacts`).  `PunoCalculus.MassGap` adds the
   removable-0/0 crossover lemma `sinh(a)/a -> 1` and `a/sinh(a) -> 1` on the
   punctured neighbourhood (from `Real.hasDerivAt_sinh`, sealed via
   `HasDerivAt.tendsto_slope`), with `crossoverCertifiedFacts` keeping the
   endpoint honesty rows (the `a -> 0` pole of `Lambda/sinh(a)` and the CDM
   `M = Lambda` special-case) machine-unchecked.  `lake build` green (8732 jobs);
   `#print axioms` = `[propext, Classical.choice, Quot.sound]` (or none); walls
   stay OPEN in the `MillenniumBridge` sense.
- Dark Energy per-script audit (2026-10-09): all 136 scripts in
   `02_Dark_Energy_0_0_Framework/` executed from the repo root; the field's
   previously "132 unregistered rows" gap is closed with a per-script table in
   `VERIFICATION_LEDGER.md`.  Result: 127 run to a PASS/completed verdict and
   write an artifact; **9 UNREPRODUCIBLE** (import `manifold`/`litim_flow` from
   an absent `../Universals` package -- `flow_active_learning`,
   `flow_hier_incremental`, `flow_hier_reg`, `flow_hier_reg_scaled`,
   `flow_hierarchical`, `flow_incremental`, `flow_regularized`,
   `flow_pole_scroll`; and `winding_transition_0_over_0` imports
   `winding_phase_diagram`, which lives in `06_Miscellaneous_Experiments/`);
   **1 timeout** (`ising_model_0_over_0.py` > 300 s).  Honest negatives retained
   (`chi_rho_vacuity` self-declares VACUOUS; `polya_wall_1e8` OVERALL FAIL on a
   missing detector dependency).  No tracked central artifact drift except JSON
   `\u221e` escaping (restored).  Each subject theorem stays OPEN -- the scripts
   compute a 0/0 interior value, never prove the surrounding theorem.
