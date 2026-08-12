"""T74 human trial runner - session builder and scoring glue.

Turns the trial package (data/human_trial_package.json) into a concrete
interactive session for a human learner, and turns the learner's recorded
answers back into the engine's verdict flags via score_participant() - the
same code that grades the machine.

A session is a bounded, deterministic plan sampled from the package:
  - L1: n_l1 held-out probes per concept (recognition/transfer),
  - recheck: n_recheck held-out probes of the FIRST-TAUGHT concepts
    (Species A and B) after the whole curriculum - the single-session
    no-forgetting check,
  - creativity: n_creative prompts per level (trivial / mid / wild) per
    concept (the human places its own item on the disk).

build_answers() maps the human's inputs onto the answers schema that
score_participant() expects (probe_labels, sequential, creative_items).

Pure stdlib + numpy; the HTTP layer and the single-page app live in
puno_app/human_trial_ui.py and puno_app/human_trial.html.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "experiments"))
from human_trial_pilot import _taught, _prompt, score_participant, \
    CONCEPT_NAMES, C  # noqa: E402

LEVELS = ("trivial", "mid", "wild")
RECHECK_CONCEPTS = ("Species A", "Species B")   # the first-taught concepts


def build_session(seed=20260812, n_l1=8, n_recheck=4, n_creative=2):
    """Deterministic session plan from the T74 trial package (seed 42).

    Returns the plan as JSON-serializable dict the UI renders.  The probe
    subsets are sampled per concept on the session seed, so the same session
    can be reproduced (and scored) verbatim.
    """
    exemplars, probes = _taught(42)
    from human_trial_pilot import make_package
    pkg = make_package(42)
    rng = np.random.default_rng(seed)

    l1_idx = sorted(rng.choice(40, size=n_l1, replace=False).tolist())
    rk_idx = sorted(rng.choice(40, size=n_recheck, replace=False).tolist())

    def points(sets, idx):
        return {name: [[round(float(x), 3) for x in sets[c][i]]
                       for i in idx] for c, name in enumerate(CONCEPT_NAMES)}

    creativity = [{"level": level, "concept": name,
                   "prompt": _prompt(level, name)}
                  for level in LEVELS
                  for name in CONCEPT_NAMES
                  for _ in range(n_creative)]

    return {
        "meta": {"concepts": CONCEPT_NAMES,
                 "thresholds": pkg["meta"]["thresholds"],
                 "bars": pkg["meta"]["bars"],
                 "rule": pkg["meta"]["rule"]},
        "teaching": {name: [[round(float(x), 3) for x in ex[i]]
                            for i in range(len(ex))]
                     for name, ex in zip(CONCEPT_NAMES, exemplars)},
        "l1": {"probe_idx": l1_idx, "probes": points(probes, l1_idx)},
        "recheck": {"concepts": list(RECHECK_CONCEPTS),
                    "probe_idx": rk_idx,
                    "probes": {name: [[round(float(x), 3) for x in
                                        probes[c][i]] for i in rk_idx]
                               for c, name in enumerate(CONCEPT_NAMES)
                               if name in RECHECK_CONCEPTS}},
        "creativity": creativity,
    }


def build_answers(session, l1_labels, recheck_labels, creative_items):
    """Map the human's recorded inputs onto the score_participant schema.

    l1_labels      {concept_name: [label_idx, ...]}    one per L1 probe
    recheck_labels {concept_name: [label_idx, ...]}    one per recheck probe
    creative_items [{"level", "concept", "x", "y"}, ...]  placed items

    Returns the answers dict fed to score_participant().
    """
    probe_labels = {}
    for name in CONCEPT_NAMES:
        probe_labels[name] = [int(l) for l in l1_labels[name]]

    sequential = {}
    for stage in range(1, C + 1):
        sequential[str(stage)] = {}
        for c, name in enumerate(CONCEPT_NAMES):
            if name in RECHECK_CONCEPTS and c < stage:
                sequential[str(stage)][name] = \
                    [int(l) for l in recheck_labels[name]]
            else:
                sequential[str(stage)][name] = []

    creative = {lv: [] for lv in LEVELS}
    for it in creative_items:
        creative[it["level"]].append({"concept": it["concept"],
                                      "x": float(it["x"]),
                                      "y": float(it["y"])})

    return {"probe_labels": probe_labels, "sequential": sequential,
            "creative_items": creative}


def grade(session, answers):
    """Grade recorded answers on the same taught set the package uses."""
    exemplars, probes = _taught(42)
    return score_participant(answers, exemplars, probes)


def _perfect_reference(session):
    """Ground-truth answers: every probe routed to its true concept.

    Used by the test to pin the session schema, and by the UI to show what a
    perfect run looks like.  Not a human simulation - just the answer key.
    """
    l1_labels = {}
    for c, name in enumerate(CONCEPT_NAMES):
        l1_labels[name] = [c] * len(session["l1"]["probe_idx"])
    recheck = {}
    for name in RECHECK_CONCEPTS:
        recheck[name] = [CONCEPT_NAMES.index(name)] * \
            len(session["recheck"]["probe_idx"])
    return build_answers(session, l1_labels, recheck, [])
