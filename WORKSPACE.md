# Puno_Calculus — Workspace Index

This directory contains **three independent git repositories**. They share an
author and a set of ideas, but they are separate projects with separate
histories, remotes, and workflows. Do not merge them; do not run one repo's
entrypoint from inside another.

| Directory | Project | Remote | HEAD | Tracked files |
|---|---|---|---|---|
| `.` (root) | **Law of Repulsive Emanation** (LORE) | `Puronbo/Law-Of-Repulsive-Emanation` | `breakthrough-register` | 1766 |
| `j/` | **Photon Rubber Ball Research** | `Puronbo/Photon-Rubber-Ball-Research` | `main` @ `d957108` | 134 |
| `Folding-Calculus/` | **Folding Calculus** | `Puronbo/Folding-Calculus` | `main` @ `518dede` | 154 |

`j/` also carries `folding` and `lore` as extra remotes (provenance only — those
are now standalone sibling clones, so use the sibling directory, not `j/`).

---

## 1. Folding Calculus — `Folding-Calculus/`

**"The 90-Degree Complex Manifold — The Universe as a Whole"**, formerly
titled *"Crease Density — Folding, Unfolding, and the Geometry of Everything."*
By Michael Grafiel Sayson Puno. Licensed CC BY 4.0; v1.0.0 is archived
(Zenodo DOI `10.5281/zenodo.21217457`).

**Core idea.** A 90° fold of tangent vectors is the complex structure
`J² = −I`. Where the Nijenhuis tensor fails to vanish,

```
N_J(X, Y) = [X, Y] + J[JX, Y] + J[X, JY] − [JX, JY]
```

is a **crease**, and the local normal form of a generic crease is the cusp
catastrophe `V(x; a, b) = ¼x⁴ − ½ax² − bx`. Physical domains are treated as
sheaves; phenomena are stalk multiplicity colliding at the crease.

**Layout** — layers intended as a journey, enterable at any level:

| Layer | Content | Status |
|---|---|---|
| `0-ROOTS/` | Crease density in ReLU networks | empirically verified (synthetic 2D only) |
| `1-GEOMETRY/` | `FOUNDATIONS.md`, spacetime theorem + self-critique | formal mathematics |
| `2-CREASE-AS-GENERATOR/` | Sheaves collide | theoretical |
| `3-IMAGINARY-SPREAD/` | Wick rotation as `J` | theoretical |
| `4-PHASE-AS-CREASE/` | Phase boundaries | theoretical |
| `5-ENGINE/` | Continuous crease dynamics, simulations, videos | empirically verified |
| `7-EVERYWHERE/` | Cross-domain: biology, economics, music, cognition… | theoretical |
| `8-PAPERS/` | Preprint, proof sketch, abstract | theoretical |
| `9-TOWARDS/` | Unified Crease Principle, roadmap | theoretical |

Note the numbering gap: **there is no stage 6.** Either it was removed or never
existed. Worth resolving before publishing a "layers 0–9" claim.

**Workflow** (run from the `Folding-Calculus/` directory):

```bash
pip install -r 0-ROOTS/requirements.txt   # numpy, matplotlib, scipy (torch optional)

# Layer 0 — empirical root
python 0-ROOTS/src/exp2_crease_density.py

# Layer 5 — continuous engine
python 5-ENGINE/tests.py
python 5-ENGINE/experiments.py
python 5-ENGINE/produce_videos.py --all
```

There is **no single runner**. Verification is per-script, and unlike the other
two repos there is no consolidated pass/fail gate.

**Verified state, 2026-09-28** (fresh clone at `518dede`):

- `5-ENGINE/tests.py` — 10/10 PASS, exit 0.
- `0-ROOTS/src/exp2_crease_density.py` — exit 0, wrote `exp2_results.png`.

**Caveat on the headline claim.** The root README says crease density "is the
experimental shadow of the Nijenhuis tensor norm." The underlying
`0-ROOTS/results/crease_density_note.md` is more careful and should be treated
as authoritative: across five architectures crease density correlates
**r = −0.77** with decision-boundary complexity while **layer depth correlates
r = +0.97**, so the note itself calls crease density "a secondary signal here,
not a replacement for depth." All Layer-0 results are on small synthetic 2D
datasets with 2–5-layer MLPs ≤128 units — no real datasets, no standard
benchmarks. The `−0.77` in particular does not support the README's phrasing.

---

## 2. Law of Repulsive Emanation — root `.`

The main Puno/Calculus corpus: `sigma/`, `sigma_venv/`, `experiments/`,
`data/`, `docs/`, `tests/`.

**Workflow** (run from the root):

```bash
python run_all.py          # 21 steps: data preflight + 20 experiment/proof steps
python -m pytest tests/    # 693 tests
```

**Data persistence (fixed 2026-09-28).** `data/*.json` is gitignored, so an
artifact persists only if tracked or regenerable. This was not true: 88 of 388
artifacts existed on one machine only, and **36 were load-bearing for the test
suite** — meaning "693 passed" was a property of the machine, not the repo.
Three changes close the loop:

1. `regen_data.py` (`report` / `--regen-all` / `--manifest`) maps every artifact
   to its generating script. It is now **step 1 of `run_all.py`**, so the
   pipeline reports its own data coverage before claiming any results. A fresh
   clone repairs itself with one command:

   ```bash
   python regen_data.py --regen-all    # rebuild every MISSING regenerable artifact
   ```
2. `data/DATA_MANIFEST.json` records the mapping (currently 305 tracked,
   47 recreatable, 42 unreproducible).
3. `tests/conftest.py` runs a **data preflight** on every pytest session. A
   missing artifact previously produced a bare `FileNotFoundError` —
   indistinguishable from a proof that failed. It now prints an explicit
   `data preflight: ... N with no tracked-or-regenerable source` line and, in a
   fresh clone, names each absent artifact and points at the recovery path.

Against a clean `git archive HEAD` the preflight reports **36**
load-bearing absences. One command closes 18 of them
(`python regen_data.py --regen-all`); the remaining **18 have no discoverable
source** and are recorded in `PL-23` in `docs/PREDICTION_LEDGER.md`. The suite
carries ratchets on both numbers so neither can grow silently.

---

## 3. Photon Rubber Ball Research — `j/`

Crease-like physics for photon–rubber-ball systems: recoil, adhesion, thermal
trapping, contraction.

**Workflow** (run from `j/`), per `ACTION_PLAN.md`:

```bash
python results_of_record.py     # 58 checks, exit 0
python ladder_instrument.py     # 27 checks
ruff check --select F           # must be clean
```

**Known gap, already logged as X55:** there is no runner, and no
`-W error::RuntimeWarning` wiring, so this repo cannot make a blanket "all green"
claim. See `CORRIGENDUM.md` for tracked retractions.

**Linked worktrees — 6, all restored (2026-09-28).** The repo was moved from
`C:\Users\Me\Desktop\j` to here, which broke all six linked-worktree links.
Each worktree directory had moved with the repo, but its `.git` marker still
pointed at the dead `Desktop\j\.git/worktrees/...` path, so git could no longer
see them. They were re-registered at their original branch tips:

| Worktree | Branch | Tip | Untracked work preserved |
|---|---|---|---|
| `connections-map` | `worktree-connections-map` | `738644a` | 1 file |
| `dark-energy-analysis` | `worktree-dark-energy-analysis` | `738644a` | 1 file |
| `density-analysis` | `worktree-density-analysis` | `738644a` | 1 file |
| `folding-analysis` | `worktree-folding-analysis` | `738644a` | 1 file |
| `mighty-sparking-bachman` | `worktree-mighty-sparking-bachman` | `61c2d12` | 3 files |
| `universe-sim-worktree` | `worktree-universe-sim-worktree` | `544b8e1` | 64 files |

All six sit under `j/.claude/worktrees/` (gitignored, so no repo pollution).
Verified: each is a functioning git worktree, `fsck` clean, and all 71
previously-untracked files restored. All six branches are **0 ahead of `main`**
and 7–53 behind it, so none of them carries unmerged commits — they are older
snapshots, not divergent work.

To enter one:

```bash
cd j/.claude/worktrees/universe-sim-worktree
```

**Path fix needed:** `PROJECT_INDEX.md`, `HANDOFF.md`, `NEXT_STEPS.md` and
`ACTION_PLAN.md` still reference the old location
`C:\Users\Me\Desktop\j\...`. The directory is now
`C:\Users\Me\Downloads\Puno_Calculus\j`.

---

## House rules

1. **Run each repo's entrypoint from its own root.** They have independent
   dependencies and independent verdicts.
2. **A result is "verified" only if a named script reproduces it.** Prose,
   notebooks, and generated narrative are not evidence.
3. **Keep verified and speculative separated**, as Folding Calculus does with
   its layer table.
4. **Fix the README when it outruns its own experiment.** Both the LORE χ(ρ)
   work (`PL-22`) and Folding Calculus' crease-density claim were cases where
   the prose asserted more than the instrument produced.
