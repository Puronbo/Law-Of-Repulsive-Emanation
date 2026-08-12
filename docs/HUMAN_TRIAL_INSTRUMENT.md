# Human-Trial Instrument — running the T74 human protocol

`docs/LEARNING_CREATIVITY_TEST.md` Part 2 defines a human protocol that
reuses the engine's two axes, its joint novelty × validity rule, and its
pass bars.  This instrument makes that protocol *concrete and runnable*:

- a **trial package** (`data/human_trial_package.json`) — the materials a
  facilitator hands a learner: a labeled teaching set per concept, a
  held-out probe set, creativity prompts at three effort levels, and the
  pre-registered thresholds and bars;
- a **participant scorer** (`score_participant` in
  `experiments/human_trial_pilot.py`) — the *same* code that grades the
  machine in T74 grades a human's recorded answers;
- a **pilot** with simulated archetype participants showing the instrument
  works: the bars are attainable and they discriminate.

## How a real human trial runs

1. **Teach.**  Hand the learner the package's `teaching.exemplars` — 40
   labeled examples of each of the 8 concepts (Species A..H).  For the L1
   curve, teach a subset (e.g. 1, then 4, then 40 examples/concept) and probe
   after each stage; for L2, teach the concepts sequentially and re-probe the
   first-taught ones after every later concept.
2. **Probe.**  The learner routes each `probes.items` point (never shown) to
   a concept.  Record answers as `probe_labels`.
3. **Prompt for creativity.**  Three effort levels, 20 prompts per concept
   per level, drawn from `creativity_prompts`: *trivial* (tiny tweak of a
   shown example), *mid* (genuinely new but unmistakably the concept), *wild*
   (far outside any example).  The learner produces one item per prompt and
   claims its concept.  Record as `creative_items`.
4. **Grade.**  Run `score_participant(answers, exemplars, probes)`.  It
   applies the pre-registered spacing-derived thresholds
   (`meta.thresholds`) and the joint rule, and returns the same five verdict
   flags as the engine (L1 ceiling ≥0.90, L2 no-forgetting ≥0.85, C1 mid
   creative ≥0.15, C2 novel-min 0.90 / creative-max 0.05, C3 interior peak).

```python
import sys; sys.path.insert(0, 'experiments')
import json
from human_trial_pilot import score_participant, _taught, CONCEPT_NAMES

exemplars, probes = _taught(42)            # the package's shared set
answers = json.load(open("answers_001.json"))   # a real learner's answers
print(score_participant(answers, exemplars, probes))
```

The learner is graded on the *same* exemplars they were shown, and the
thresholds are pre-registered on those exemplars — "novel" and "valid" are
defined relative to the taught material before any item is judged, exactly
as the protocol requires.

## The pilot (what this module verifies)

Because no human is in the loop here, the module runs a pilot with
archetypal simulated participants on the same space.  This validates the
*instrument*, not human behavior:

- **P1 attainability** — a perfect participant (exact held-out routing,
  mid-effort variations) attains every engine bar: L1 ceiling 1.0, L2 1.0,
  C1 mid creative ≥0.15 (measured ~0.24–0.36), C2/C3 hold.
- **P2 discrimination** — a non-learner (uniform random routing, random
  generation) fails L1 (ceiling ≈ 1/C ≈ 0.13) and C1 (yield ≈ 0): the
  protocol is not passable by chance.
- **P3 the joint criterion binds on both sides** — within the perfect
  participant, trivial-effort items are valid-but-not-novel (valid ~0.9 >
  novel ~0.25), wild-effort items are novel-but-not-valid (novel ~1.0 > valid
  ~0.0), mid-effort is the only positive creative yield (interior-peaked like
  the engine's C3), and a pure copycat (exact memorized copies) scores 0.
- **P4 the C2 constraint holds** — random far items grade ~100% novel but
  ~0% creative under the pre-registered thresholds, so a facilitator using
  the rule cannot count novelty alone as creativity.

## Honest walls

- The pilot participants are **simulated archetypes**; the pilot proves the
  instrument's bars are attainable and discriminating and the rule is
  consistent, not that any human passes.  That is the precondition for a
  real trial: a human score against these bars is interpretable because the
  bars are neither impossible nor reachable by guessing.
- The creativity effort levels are simulated by the engine's own outward
  mutation moves at the three magnitudes; a real human will produce whatever
  they produce, and the pre-registered rule grades it.

## Where things live

| Piece | Location |
|---|---|
| Pilot + scorer + package generator | `experiments/human_trial_pilot.py` |
| Pilot verdict artifact | `data/human_trial_pilot_data.json` (gitignored, `git add -f`) |
| Trial package (the materials) | `data/human_trial_package.json` |
| Design doc (protocol) | `docs/LEARNING_CREATIVITY_TEST.md` |
| Pinned verdict test | `tests/test_solvable_theorems.py::test_human_trial_pilot_supported` |

## Commands

    python experiments/human_trial_pilot.py               # seed 42, print pilot verdict
    python experiments/human_trial_pilot.py --verdict     # write data/ JSON verdict + trial package
