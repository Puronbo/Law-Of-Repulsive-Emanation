# Learning-Curve Scaling (T75) — the acquisition curve is a density effect

T74's learning curve was measured at a single operating point
(C=8 concepts, SIGMA=0.05 exemplar noise).  This theorem asks whether the
curve is an *artifact of that one setting* or the general signature of
density-based stored-memory acquisition.  It sweeps the curriculum size C
over the same space and the same router.

The router is identical to T74: a stored-memory k-NN agent (majority vote
over the `K_VOTE` nearest stored exemplars; k-NN is the repo's own local
primitive, `K_NN=8` in `decentral_net`) in a bounded 2D concept space (a
Poincaré-style disk, homes on a ring of radius `HOME_R=0.25`).

## Claims (each a verdict run on seeds 42/11/7)

- **S1 — the sparse floor is chance.**  With one exemplar per concept the
  router sits at chance `1/C`, and the floor strictly *decreases* with C over
  the well-separated regime C ∈ {2,4,8,16}: more competing concepts = a
  denser confusion field, so a probe's k-neighborhood is dominated by *other*
  concepts' exemplars.  Measured floor: 0.50 → 0.25 → 0.125 → ~0.07,
  tracking 1/C exactly.  (K_VOTE is clipped to `min(5, C)` at small C — a
  majority vote cannot draw more neighbours than there are classes; at
  C=2/4 ties resolve to the lower-index class, still exactly chance.)
- **S2 — the acquisition curve exists at every scale.**  The full-exposure
  ceiling holds ≥0.90 for every C ∈ {2,4,8}, so the curve's dynamic range
  (ceiling − floor) *grows* with C (0.50 at C=2 → 0.82 at C=8): a bigger
  curriculum is harder to start from but is still fully acquired.
- **S3 — capacity saturation.**  Beyond the well-separated regime the memory
  saturates the space and the full-exposure ceiling collapses.  Once the
  adjacent-home separation `2·HOME_R·sin(π/C)` falls to a few exemplar-sigma,
  the concepts' gaussian clouds overlap and even a full memory cannot
  separate them.  Measured ceiling: 0.94 (C=8) → 0.61 (C=16) → 0.42 (C=24)
  → 0.30 (C=32), strictly decreasing.  The predicted critical scale
  `C* ≈ π·HOME_R/(2·SIGMA) ≈ 8` is exactly where T74's operating point sits.
  Concordance check (diagnostic, not a pinned claim): with SIGMA=0.03 the
  ceiling still holds 0.89 at C=16; with SIGMA=0.10 it collapses to 0.59
  already at C=8 — the collapse tracks separation/σ, not a magic C.

## Honest walls

- Synthetic 2D concept space, stored-memory k-NN router, gaussian exemplars:
  **mechanism claims** about the learning environment, not about natural
  curricula or real learners.  The point of T75 is that T74's learning curve
  is the general signature of density-based stored-memory acquisition,
  bounded by an explicit, measurable capacity scale.
- The saturation prediction is structural: it says *where* the well-separated
  regime ends, given the space's geometry (HOME_R) and the exemplar scale
  (SIGMA).

## Where things live

| Piece | Location |
|---|---|
| Experiment + verdict | `experiments/learn_curve_scale.py` |
| Verdict artifact | `data/learn_curve_scale_data.json` (gitignored, `git add -f`) |
| Pinned verdict test | `tests/test_solvable_theorems.py::test_learn_curve_scale_supported` |

```python
import sys; sys.path.insert(0, 'experiments')
from learn_curve_scale import run_test
r = run_test(42)
assert all(r[k] for k in ("s1_ok", "s2_ok", "s3_ok"))
```

## Commands

    python experiments/learn_curve_scale.py               # seed 42, print verdict
    python experiments/learn_curve_scale.py --verdict     # write data/ JSON verdict
