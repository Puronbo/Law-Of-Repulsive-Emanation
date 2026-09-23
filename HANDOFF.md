# HANDOFF — byte-steering guide to the sealed register

Purpose: a domain reviewer can independently reproduce every registered
gate from the byte facts below. No proof claims are made here; this file
only *steers*: names, paths, hashes, and the exact commands whose exit
codes the register counts. Anything below claimed as "passed" is a real
run result already recorded on branch `breakthrough-register`.

## Repo facts (the thing being handed off)

- Repo root: `C:\Users\Me\Downloads\Puno_Calculus` (branch
  `breakthrough-register`, remote `github.com/Puronbo/Law-Of-Repulsive-Emanation`).
- Register state at HEAD `75b75b7` (Eighteenth layer):
  - meta-audit `validate_soliton_millennium_meta_audit.py` = **10/10, exit 0**
  - on-disk root validators = **89** (pinned: `run_all_audits.py`
    `PINCED_VALIDATORS = 89`; meta-audit check #9 compares == 89; docs
    pin "89 root validators")
  - `tests/` = 645 passed; emanation suite = 252 passed;
    `soliton_eca` package = 33 passed
  - certificate gate = **125 certificates** (105 PASS, 20
    HONEST_NEGATIVE), **83 claims all believed** — reproduced with
    `python scripts/certify_repo.py --gate` from the repo root

## The seven vendored twins

The register's 7-twin closure, byte-pinned by
`SUITE_CLOSURE_SHA` (recompute recipe below):

| # | twin | path under repo | status | verified content anchors (grep) |
|---|------|-----------------|--------|---------------------------------|
| 1 | EcaIsometry | `PunoCalculus/PunoCalculus/EcaIsometry.lean` | 2/7 **reserved prose** (exact decidable, `native_decide`; no Mathlib) | `affine_class_exact`, `isometry_class_exact`, `rule204_identity_widths`, `rule51_complement_widths`, `complement_is_involution`, `isometry_class_three_pairs`, `complementGen` |
| 2 | MillenniumBridge | `PunoCalculus/PunoCalculus/MillenniumBridge.lean` | 2/7 **reserved prose** (explicit NON-resolution; no Mathlib) | `statuses`, `NOT SETTLED BY THIS PROJECT`, `seven_problems_declared_unsolved` |
| 3 | TwinAnalyticLaws | `PunoCalculus/PunoCalculus/PunoTwin/TwinAnalyticLaws.lean` | 5/7 **derivable** (imports Mathlib) | `rho_eq_structure`, `rho_eq_abs_profile`, `antiderivative_deriv`, `antiderivative_hasDerivAt`, `window_defect_exact`, `defect_at_L`, `defect_tendsto_zero`, `defect_window_closed_form`, `defect_at_L_tail_lt_window` |
| 4 | TwinRingLaws | `PunoCalculus/PunoCalculus/PunoTwin/TwinRingLaws.lean` | 5/7 **derivable** (imports Mathlib) | `step204_eq`, `step51_eq`, `sumBits_eq`, `compBits_eq`, `rule204_identity_all`, `rule51_complement_all` |
| 5 | MPOperator | `PunoCalculus/PunoCalculus/PunoTwin/MPOperator.lean` | 5/7 **derivable** (imports Mathlib) | — |
| 6 | CollatzReach | `PunoCalculus/PunoCalculus/PunoTwin/CollatzReach.lean` | 5/7 **derivable** (imports Mathlib) | `odd_step_even`, `spine_identity`, `spine_reaches_one`, `two_pow_even_mod_three`, `two_pow_odd_mod_three`, `reverse_tree_levels` |
| 7 | DirichletLaws | `PunoCalculus/PunoCalculus/PunoTwin/DirichletLaws.lean` | 5/7 **derivable** (imports Mathlib) | `center_symmetry` (+ L-function laws, primitive chi's, parity law, spike lattice) |

Grep expectations are the exact (byte) anchors the meta-audit's checks
#1–#6 verify.

## The pin and the recompute recipe

- `SUITE_CLOSURE_SHA` (registers the seven vendored twins):
  `9fff39883f799f96bca6d283d225f053a4f5232b067f73798c2e12d54d57d0c5d302612de5b3e5e4a5b3f46252811e4d71a281e586f95001cf9cf599c88b7794`
- The vendor tree's own origin: `github.com/Puronbo/Millennium-Prize-Problem-Lean-4-Proof`,
  pinned twin-origin commit `a975c74` (`TWIN_ORIGIN_SHA`).
- Recipe: take the file-NAME-sorted list of the seven files above; for
  each file in that sorted order update a SHA-512 aggregator with
  `name.encode("utf-8") + b"\x00"` then the file's raw bytes; the final
  hex digest must equal `SUITE_CLOSURE_SHA` exactly. This is check #10
  inside `validate_soliton_millennium_meta_audit.py` (function
  `_twin_byte_closure_missing`); any rename/drop/byte change breaks it.

## Reproduce every gate (commands, from the repo root)

    python "Create Native Ramp Function and Implement 8-Bit ECA Rules\validate_soliton_millennium_meta_audit.py"   # 10/10 exit 0
    python "Create Native Ramp Function and Implement 8-Bit ECA Rules\run_all_audits.py"                            # 90/90 + pinned 89 validators, exit 0
    python scripts\certify_repo.py --gate                                                                            # 125 certs / 83 claims
    python -m pytest tests -q                                                                                        # 645 passed
    cd experiments\emanation; $env:PYTHONPATH="<repo root>"; python -m pytest -q                                    # 252 passed
    python "Create Native Ramp Function and Implement 8-Bit ECA Rules\validate_soliton_metrics.py"                  # runtime-over-wire validator
    python "Create Native Ramp Function and Implement 8-Bit ECA Rules\validate_soliton_nn.py"                       # SNN validator
    python "Create Native Ramp Function and Implement 8-Bit ECA Rules\validate_soliton_drift.py"                    # drift validator

Byte-normalization audit (planner-only, read-only):
    python scripts\twin_byte_check.py                                                                               # closure == pin, per-file SHA-512, origin-mirror diffs

## The origin lane (now genuinely built — recompute recipe)

The register's former "genuine build NOT completed" bullet is closed. The
origin repository `github.com/Puronbo/Millennium-Prize-Problem-Lean-4-Proof`
is mirrored on disk at `fcc2\Millennium-Prize-Problem-Lean-4-Proof` (this
mirror is gitignored; `scripts/twin_byte_check.py` reports it as an
informational byte-mirror). Live state and exact recompute:

- mirror checkout: upstream master HEAD `cb8608e…`
  (`git -C fcc2\Millennium-Prize-Problem-Lean-4-Proof rev-parse HEAD`)
- real toolchain: `leanprover/lean4:v4.33.1` (origin's own `lean-toolchain`),
  Mathlib v4.33.1 rev `0df444a3…` (origin's committed `lake-manifest.json`)
- warm package cache: `fcc2\...\.lake\packages` was populated from the mirror
  lane's already-built cache (all nine package revs matched the origin
  manifest byte-for-byte before copying), so no mathlib rebuild was needed.
- build #1 (all modules): delete `.lake\build\lib\lean\*` oleans and run

      $env:PATH = "$env:USERPROFILE\.elan\bin;$env:PATH"
      lake build MillenniumPrizeProblem PunoTwin          # exit 0, 8737 jobs

  at `fcc2\Millennium-Prize-Problem-Lean-4-Proof`. `Build completed
  successfully (8737 jobs)`, TRUE exit 0.
- build #2 (fresh no-cache on the project's own modules): DELETE the
  project oleans (Main, Solution, Challenge, UniversalSingularity/*,
  PunoTwin/*) and run the same command — exit 0 again, 8737 jobs, every
  project module recompiled from source (e.g. PunoTwin.DirichletLaws 24 s,
  TwinAnalyticLaws 26 s, TwinRingLaws 26 s, MPOperator 27 s). The pass is
  provably NOT cache reuse of the project modules; only the vendored
  dependency oleans (mathlib and aux packages) are reused, as in any lake
  project.
- scope facts (recorded, not hidden): the origin's `lean_lib PunoTwin`
  declares roots TwinAnalyticLaws/TwinRingLaws/MPOperator/DirichletLaws —
  `CollatzReach.lean` is present but NOT a declared origin root (its
  byte-identical vendored copy compiles in the mirror lane's PunoTwin
  target, 21-23 s); the origin's non-twin `UniversalSingularity` modules
  compile with exit-0 `sorry` warnings (e.g. HilbertPolya; `declaration
  uses sorry`); the origin raises NO 7/7 claim by itself.
- byte-mirror facts after the build: TwinAnalyticLaws, TwinRingLaws,
  MPOperator and CollatzReach remain byte-identical to the sealed vendored
  closure; DirichletLaws.lean has SINCE grown upstream (Round-70 special
  values L(1,χ3), L(1,χ8), L(1,χ8')) so its live origin bytes now differ
  from the sealed closure on that single file. `SUITE_CLOSURE_SHA` is
  untouched (check #10 still recomputes it over the sealed vendored tree).
  The provenance pin `a975c74` predates the current upstream history and no
  longer resolves in a fresh clone; the vendored closure remains pinned to
  its recorded digest.

## Honest boundaries (do not let these be over-read)

- The 5/7 derivable twins have a REAL kernel pass: `lake build` of
  `PunoTwin.{TwinAnalyticLaws,TwinRingLaws,MPOperator,CollatzReach,DirichletLaws}`
  exits 0 under Lean/Lake toolchain `leanprover/lean4:v4.33.1` with
  Mathlib v4.33.1 (rev `0df444a3…`) and its prebuilt olean cache
  (8706 jobs, `Build completed successfully`). The build was run in a
  temp lane whose `PunoTwin/*.lean` bytes are verified byte-identical
  to the vendored closure (see `scripts/twin_byte_check.py`).
  Reproduce: `lake update && lake build PunoTwin.{...}` in the temp
  project `C:\Users\Me\AppData\Local\Temp\opencode\twin_build`.
  Fresh no-cache re-run confirmed: delete the five twin oleans, rebuild
  the same targets, exit 0 again (8710 jobs) - NOT cache reuse.
- The 2/7 reserved files contain NO resolution claims and are NOT part
  of the kernel pass: `MillenniumBridge` declares the seven problems
  NOT SETTLED by this project; `EcaIsometry` is exact-decidable prose
  (`native_decide`), intentionally outside Mathlib. The register stands
  at 5/7 kernel-pass + 2/7 reserved prose, and NO 7/7 is claimed
  anywhere.
- The origin lane genuinely builds (see recipe above) but that does NOT
  certify the 2/7 reserve: those two names do not exist in the origin
  repository at all, so nothing upstream can be over-read as their
  derivation.
- Working-tree drift is real and visible (`git status --porcelain`);
  `experiments/emanation/data/supervision_verdict.json` carries a
  regenerate-time timestamp diff; the protected file
  `experiments/emanation/data/shift_bus_verdict.json` is never staged.