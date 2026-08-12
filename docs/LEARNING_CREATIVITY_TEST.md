# Learning & Creativity Test — ascertaining learned and creativity in a learning environment

A test that asks two questions of a learner (an agent or a human) in a learning
environment:

1. **LEARNED** — did the learner actually acquire the curriculum (vs. pattern
   matching the session), and does what was learned persist?
2. **CREATIVITY** — can the learner generate *new-but-right* content: items it
   was never shown that are simultaneously **novel** and **valid**?

One rubric, two axes, re-used by the engine experiment and by the human
protocol.  The engine experiment (`experiments/learn_creativity_test.py`)
operationalizes the rubric on the repo's own machinery, so the human protocol
below is *scored on the same axes and thresholds the engine verifies*, not on
an arbitrary set of made-up criteria.

## The rubric (used for both agents and humans)

| Axis | Ascertained by | Operational test |
|---|---|---|
| **LEARNED — recognition/transfer** | held-out probe accuracy | can the learner route/recognize items it was never shown?  A learning curve over exposure: near-chance at minimal exposure → high at full exposure.  Plus **retention**: first-learned content stays accurate as more is learned (no forgetting). |
| **LEARNED — persistence** | retention under continued exposure | see above: the sequential-teaching run (L2). |
| **CREATIVITY — novelty** | distance from the taught core | a generated item is *novel* when it lies outside the taught core (beyond a threshold derived from the taught exemplars' own spacings — the same doctrine that made the internet name-space novelty axis work, T55i/A1). |
| **CREATIVITY — appropriateness** | validity under the learned manifold | a generated item is *valid* when it is inside the learned manifold (within an acceptance radius derived from the taught exemplars) and routes to the intended concept. |
| **CREATIVITY — joint** | novel × valid | a generated item is *creative* iff it is novel AND valid.  Novelty alone is not creativity: random far items are novel but invalid (rejected). |

The engine fixes concrete thresholds for both axes on a bounded synthetic
concept space.  The human protocol reuses the *same* qualitative rubric and
the same quantitative decision rule (novel × appropriate), with the space and
the graders' role stated up front.

## Where things live

| Piece | Location |
|---|---|
| Engine experiment + verdict | `experiments/learn_creativity_test.py` |
| Verdict artifact | `data/learn_creativity_test_data.json` (gitignored, `git add -f`) |
| Design doc (this file) | `docs/LEARNING_CREATIVITY_TEST.md` |
| Pinned verdict test | `tests/test_solvable_theorems.py::test_learn_creativity_supported` |

```python
import sys; sys.path.insert(0, 'experiments')
from learn_creativity_test import run_test
r = run_test(42)
assert all(r[k] for k in ("l1_ok", "l2_ok", "c1_ok", "c2_ok", "c3_ok"))
```

## Part 1 — the engine experiment (the repo's own machinery)

A routing agent with a stored-memory representation (the exemplars it was
shown) lives in a bounded 2D concept space (a Poincaré-style disk,
DecentralNet-style homes).  It routes a point to the majority class among its
`K_VOTE=5` nearest stored exemplars — k-NN being the repo's own local
primitive (`K_NN=8` in `decentral_net`).  The curriculum: 8 concepts on a
compact interior blob, 40 exemplars each, 40 held-out probes each.

### Claims (each a verdict run on seeds 42/11/7)

- **L1 learned — the acquisition curve.**  Held-out probe accuracy climbs from
  near-chance (0.125 ≈ 1/C) at 1 exemplar/concept to ≥0.90 at full exposure.
  Mechanism: with a sparse memory the 5-neighborhood is dominated by *other*
  concepts; as the memory fills, the true concept's exemplars dominate the
  neighborhood.  (Measured: 0.12 → 0.94.)
- **L2 learned persists — no forgetting.**  Concepts are taught sequentially;
  the first-taught concepts keep ≥0.85 accuracy after every later concept is
  added.  Additive stored memory does not destabilize what was learned.
  (Measured: ≥0.92.)
- **C1 creativity — novel-but-valid yield.**  A measurable share of mid-size
  near-miss variations of stored exemplars are simultaneously NOVEL (outside
  the taught core) and VALID (inside the learned manifold, routed to the
  intended concept) — new-but-right content that was never presented.
  (Measured: mid-size yield ≥0.24 across seeds.)
- **C2 novelty ≠ creativity.**  Random far nulls (outside the learned blob)
  are ~100% novel but ~0% creative: the joint novelty × validity criterion is
  necessary.  (Measured: 1.00 / 0.00.)
- **C3 the creativity landscape is interior-peaked.**  Creative yield peaks at
  a middle mutation size — too-close variations are valid but not novel,
  too-far are novel but not valid — a real trade-off, not a monotone curve.
  (Measured: yields [≈0.2, ≈0.3, ≈0.05, 0.0] at sizes 0.05/0.12/0.22/0.32.)

### Honest walls (engine)

- The agent is a stored-memory k-NN router over independent gaussian exemplars
  in a synthetic 2D space: the claims ascertain ACQUISITION and NOVEL-VALID
  GENERATION under controlled conditions, not transfer to unseen tasks or
  open-domain invention.  They are **mechanism claims** about the test (the
  environment → agent mapping is measurable and reproducible).
- "Creativity" here is the operational novelty × validity quadrant; it does
  not claim human-like intent, surprise, or cultural value.

## Part 2 — the human protocol (reuses the same rubric and scores)

The same two axes, the same decision rule, run with a human learner in a
human-scale concept space.  The engine's thresholds are the *reference
operating points*: "novel" and "valid" are defined relative to the taught
material before any human item is judged.

### Setup (mirrors the engine, one-to-one)

- A human learns **8 concepts** (e.g. 8 species, 8 knots, 8 dialects, 8
  functions — anything with a bounded, gradable similarity space), taught as a
  labeled curriculum of examples.
- The grader prepares, per concept, a held-out set of recognition items
  (probes) that were never shown.

### Axis 1 — LEARNED (recognition/transfer + persistence)

- **L1 recognition/transfer:** after each exposure stage (few examples →
  many), the learner is probed on *held-out* items and must route them to the
  right concept.  The curve (near-chance at minimal exposure → high at full)
  is the acquisition evidence.  Pass bar: the same as the engine — accuracy
  climbs from ≈1/C to ≥0.90.
- **L2 persistence:** concepts are taught sequentially; the first-taught
  concepts are re-probed after every later concept is added.  Pass bar: the
  first-taught concepts keep ≥0.85 (the engine's no-forgetting bar).

### Axis 2 — CREATIVITY (novel × appropriate)

- **Novelty:** before grading, the taught material fixes the "core".  A
  generated item is *novel* when it is meaningfully outside that core — the
  human analogue of the engine's spacing-derived threshold.  The simplest
  operational rule: an item no grader can attribute to memorization of a shown
  example, i.e. it is not a copy or a trivial re-arrangement of any taught
  item.
- **Appropriateness/validity:** the item must be *right* for the concept it
  claims — a specialist grades it as valid for the intended concept, the
  human analogue of "inside the learned manifold and routed to the intended
  concept".
- **Creative iff novel AND appropriate:** an item is counted creative only in
  the joint quadrant.  Random/absurd far items (novel but not appropriate) and
  close paraphrases of taught items (appropriate but not novel) do not count —
  exactly the engine's C2/C3 structure.
- **Pass bars:** reuse the engine's — a measurable share (≥0.15) of the
  learner's mid-effort novel productions are also appropriate (C1); novelty
  alone fails (C2); and the yield is interior-peaked over effort/intensity
  (C3: trivial variations and wild inventions both underperform the middle).

### Why the engine score governs the human protocol

The human bars are not invented: each is the engine's verified operating
point, re-expressed in human terms.  A protocol that passes the human run and
an agent that passes the engine run are being graded by the *same* two-axis,
joint-quadrant rubric — so "learned and creativity" means the same thing in
both cases, and the two can be compared on one scale.

## Interactive demo

    python experiments/learn_creativity_test.py          # run seed 42, print the verdict
    python experiments/learn_creativity_test.py --verdict  # write data/ JSON verdict
