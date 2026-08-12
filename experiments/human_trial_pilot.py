"""
Human-Trial Pilot (companion to the T74 learning & creativity test):
operationalizes Part 2 of docs/LEARNING_CREATIVITY_TEST.md and validates
that the human protocol's pass bars are ATTAINABLE and DISCRIMINATING.

The human protocol reuses the engine's space, rubric, and thresholds (the
same 8-concept bounded disk, the same spacing-derived novelty/acceptance
thresholds, the same joint novelty x validity rule).  This module:

  - generates the TRIAL PACKAGE: the concrete materials a facilitator hands
    a human learner - a labeled teaching set per concept (Species A..H),
    a held-out probe set (recognition/transfer items), creativity prompts at
    three effort levels (trivial / mid / wild), and the pre-registered
    thresholds and bars.  Written to data/human_trial_package.json.
  - SCORES any participant's answers on the engine's bars via
    score_participant() - the SAME code grades a machine (T74) or a human.
    The participant is graded on the SAME exemplars they were taught and the
    thresholds are pre-registered on those taught exemplars, exactly as the
    protocol states ("novel" and "valid" are defined relative to the taught
    material before any human item is judged).
  - runs a PILOT with archetypal simulated participants, verifying:
      P1 attainability - a perfect participant (exact held-out routing,
         mid-effort novel variations) attains every engine bar (L1 ceiling
         >=0.90, L2 no-forgetting >=0.85, C1 mid creative >=0.15);
      P2 discrimination - a non-learner (uniform random routing, random
         generation) fails L1 (ceiling ~= 1/C) and C1 (yield ~= 0) - the
         protocol is not passable by chance;
      P3 the joint criterion binds on both sides (the human C3) - within the
         perfect participant, trivial-effort items are valid-but-not-novel
         (valid > novel), wild-effort items are novel-but-not-valid
         (novel > valid), mid-effort is the only positive creative yield
         (interior-peaked like the engine), and a pure copycat (exact
         memorized copies) has creative yield exactly 0;
      P4 the C2 constraint holds on the human scale - random far items grade
         ~100% novel but ~0% creative under the pre-registered thresholds,
         so a facilitator using the rule cannot count novelty alone as
         creativity.

Honest walls:
  - The pilot participants are SIMULATED archetypes on the same synthetic
    concept space (perfect router / random router / copycat).  The pilot
    therefore validates the INSTRUMENT - bars attainable + discriminating,
    rule consistent - not actual human behavior.  A real human trial is run
    by handing a human the package and scoring their recorded answers with
    the same score_participant(); the package and scorer are the deliverable.
  - The creativity "effort" levels are simulated by the engine's own outward
    mutation moves at the three magnitudes; the grading thresholds are the
    pre-registered spacing-derived ones, identical to T74.

Usage:
  python human_trial_pilot.py               # run and print the pilot verdict
  python human_trial_pilot.py --verdict     # write data/ JSON verdict +
                                            # data/human_trial_package.json
"""

import datetime
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from learn_creativity_test import (_homes, _draw_class, memory, route_pts,
                                   N_EXEMPLARS, N_PROBES, NOVELTY_MULT,
                                   ACCEPT_MULT, C, NULL_R, N_NULL, MUT_JITTER)

DATA_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "data", "human_trial_pilot_data.json")
PACKAGE_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "data", "human_trial_package.json")

CONCEPT_NAMES = ["Species %s" % chr(65 + c) for c in range(C)]

# --- human creativity effort levels -> engine mutation magnitudes -------- #
EFFORT_MAG = {"trivial": 0.05, "mid": 0.12, "wild": 0.32}
N_MUT_PER_CONCEPT = 20          # creativity prompts per concept per level


def _outward_unit(src, rng):
    u = src / np.linalg.norm(src)
    ang = rng.uniform(-MUT_JITTER, MUT_JITTER)
    u = np.array([u[0] * np.cos(ang) - u[1] * np.sin(ang),
                  u[0] * np.sin(ang) + u[1] * np.cos(ang)])
    return u / np.linalg.norm(u)


def _taught(seed):
    """The package's teaching set and probe set (one shared stream, so the
    participant is graded on exactly the exemplars they were shown)."""
    rng = np.random.default_rng(seed)
    homes = _homes()
    exemplars = [_draw_class(homes[c], rng, N_EXEMPLARS) for c in range(C)]
    probes = [_draw_class(homes[c], rng, N_PROBES) for c in range(C)]
    return exemplars, probes


def _prompt(level, concept):
    return {
        "trivial": ("Produce an item that is a tiny tweak of a shown example "
                    "of %s - barely different." % concept),
        "mid": ("Produce a genuinely NEW item of %s - clearly different from "
                "any example you were shown, but unmistakably %s."
                % (concept, concept)),
        "wild": ("Produce an item you would never have seen, inventing "
                 "something far outside the examples of %s." % concept),
    }[level]


# ---------------------------------------------------------------------- #
# Trial package
# ---------------------------------------------------------------------- #
def make_package(seed):
    exemplars, probes = _taught(seed)
    mem_pts, _ = memory(exemplars)
    d = np.linalg.norm(mem_pts[:, None, :] - mem_pts[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    self_excl = d.min(axis=1)
    s_mean, s_std = float(self_excl.mean()), float(self_excl.std())
    novelty_thr = s_mean + NOVELTY_MULT * s_std
    accept_r = s_mean + ACCEPT_MULT * s_std

    rng = np.random.default_rng(seed + 1)
    rounds = {}
    for level in ("trivial", "mid", "wild"):
        rounds[level] = []
        for c in range(C):
            for k in range(N_MUT_PER_CONCEPT):
                src = mem_pts[rng.integers(c * N_EXEMPLARS,
                                           (c + 1) * N_EXEMPLARS)]
                mag = EFFORT_MAG[level]
                move = src + mag * _outward_unit(src, rng)
                rounds[level].append({
                    "concept": CONCEPT_NAMES[c],
                    "prompt": _prompt(level, CONCEPT_NAMES[c]),
                    "x": round(float(move[0]), 3),
                    "y": round(float(move[1]), 3)})

    return {
        "meta": {
            "test": "T74 human protocol (docs/LEARNING_CREATIVITY_TEST.md)",
            "seed": seed,
            "concepts": CONCEPT_NAMES,
            "space": "bounded 2D concept disk, homes on a ring of radius 0.25",
            "thresholds": {"novelty_thr": round(novelty_thr, 4),
                           "accept_r": round(accept_r, 4),
                           "spacing_mean": round(s_mean, 4),
                           "spacing_std": round(s_std, 4)},
            "bars": {"L1_ceiling": 0.90, "L2_no_forgetting": 0.85,
                     "C1_mid_creative": 0.15, "C2_novel_min": 0.90,
                     "C2_creative_max": 0.05},
            "rule": "an item is CREATIVE iff NOVEL (outside the taught core) "
                    "AND VALID (inside the learned manifold, routed to the "
                    "claimed concept); novelty alone is not creativity.",
        },
        "teaching": {"exemplars": {
            CONCEPT_NAMES[c]: [[round(float(x), 3) for x in ex[i]]
                               for i in range(N_EXEMPLARS)]
            for c, ex in enumerate(exemplars)}},
        "probes": {"items": {
            CONCEPT_NAMES[c]: [[round(float(x), 3) for x in pr[i]]
                               for i in range(N_PROBES)]
            for c, pr in enumerate(probes)}},
        "creativity_prompts": rounds,
    }


# ---------------------------------------------------------------------- #
# Scoring - the SAME rule grades a machine (T74) or a human
# ---------------------------------------------------------------------- #
def _thresholds(exemplars):
    mem_pts, mem_lab = memory(exemplars)
    d = np.linalg.norm(mem_pts[:, None, :] - mem_pts[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    self_excl = d.min(axis=1)
    s_mean, s_std = float(self_excl.mean()), float(self_excl.std())
    return (s_mean + NOVELTY_MULT * s_std), (s_mean + ACCEPT_MULT * s_std), \
        mem_pts, mem_lab


def score_participant(answers, exemplars, probes):
    """Grade a participant's recorded answers on the engine's bars.

    answers = {"probe_labels": {concept_name: [label_idx, ...]},
               "sequential": {stage_str: {concept_name: [label_idx, ...]}},
               "creative_items": {level: [{"concept": name, "x": .., "y": ..}]}}
    Returns the same verdict flags as the engine (l1/l2/c1/c2/c3).
    """
    novelty_thr, accept_r, mem_pts, mem_lab = _thresholds(exemplars)

    # L1 ceiling: full-exposure recognition on held-out probes.
    hits = total = 0
    for c in range(C):
        for lab in answers["probe_labels"][CONCEPT_NAMES[c]]:
            hits += (lab == c)
            total += 1
    l1_ceiling = hits / total
    l1_ok = l1_ceiling >= 0.90

    # L2: first-taught concepts re-probed after every later concept.
    if answers.get("sequential"):
        accs = {}
        for stage in range(1, C + 1):
            hits = total = 0
            for c in range(stage):
                for lab in answers["sequential"][str(stage)][CONCEPT_NAMES[c]]:
                    hits += (lab == c)
                    total += 1
            accs[str(stage)] = hits / total
        final_old = min(accs[str(k)] for k in range(C // 2, C + 1))
        l2_ok = final_old >= 0.85
    else:
        accs, final_old, l2_ok = {}, None, None

    # Creativity: joint novelty x validity on the produced items.
    yield_by_level = {}
    for level in ("trivial", "mid", "wild"):
        items = answers["creative_items"][level]
        if not items:
            continue
        pts = np.array([[it["x"], it["y"]] for it in items])
        claimed = np.array([CONCEPT_NAMES.index(it["concept"])
                            for it in items])
        got, dmin = route_pts(pts, mem_pts, mem_lab)
        novel = dmin > novelty_thr
        valid = (got == claimed) & (dmin <= accept_r)
        creative = novel & valid
        yield_by_level[level] = {
            "novel": float(novel.mean()), "valid": float(valid.mean()),
            "creative": float(creative.mean())}

    mid = yield_by_level.get("mid", {}).get("creative", 0.0)
    tr = yield_by_level.get("trivial", {}).get("creative", 0.0)
    wd = yield_by_level.get("wild", {}).get("creative", 0.0)
    c1_ok = mid >= 0.15
    c3_ok = (mid > tr) and (mid > wd) and mid >= 0.15

    # C2: rubric audit - random far items are novel but not creative.
    rng = np.random.default_rng(0)
    ang = rng.uniform(0, 2 * np.pi, N_NULL)
    rad = rng.uniform(*NULL_R, N_NULL)
    nulls = np.stack([rad * np.cos(ang), rad * np.sin(ang)], axis=1)
    _, d_null = route_pts(nulls, mem_pts, mem_lab)
    null_novel = float((d_null > novelty_thr).mean())
    null_creative = float(((d_null > novelty_thr) & (d_null <= accept_r))
                          .mean())
    c2_ok = null_novel >= 0.90 and null_creative <= 0.05

    return {"l1_ceiling": l1_ceiling, "l1_ok": l1_ok, "l2_ok": l2_ok,
            "l2_min": final_old, "c1_ok": c1_ok, "c2_ok": c2_ok,
            "c3_ok": c3_ok, "yield": yield_by_level,
            "null": {"novel": null_novel, "creative": null_creative}}


# ---------------------------------------------------------------------- #
# Pilot: archetypal simulated participants (taught on the shared set)
# ---------------------------------------------------------------------- #
def _archetype(seed, kind, exemplars, probes):
    rng = np.random.default_rng(seed + 100 + {"perfect": 0, "random": 1,
                                              "copycat": 2}[kind])
    mem_pts, mem_lab = memory(exemplars)

    probe_labels = {}
    for c in range(C):
        name = CONCEPT_NAMES[c]
        if kind == "perfect":
            probe_labels[name] = [c] * N_PROBES
        else:
            probe_labels[name] = [int(rng.integers(0, C))
                                  for _ in range(N_PROBES)]

    sequential = None
    if kind == "perfect":
        sequential = {}
        for stage in range(1, C + 1):
            sequential[str(stage)] = {}
            for c in range(stage):
                sequential[str(stage)][CONCEPT_NAMES[c]] = [c] * N_PROBES

    creative_items = {}
    for level in ("trivial", "mid", "wild"):
        items = []
        for c in range(C):
            for k in range(N_MUT_PER_CONCEPT):
                src = mem_pts[rng.integers(c * N_EXEMPLARS,
                                           (c + 1) * N_EXEMPLARS)]
                if kind == "copycat":
                    x, y = src
                elif kind == "random":
                    rad = rng.uniform(0, 0.9)
                    ang = rng.uniform(0, 2 * np.pi)
                    x, y = rad * np.cos(ang), rad * np.sin(ang)
                else:
                    mag = EFFORT_MAG[level]
                    move = src + mag * _outward_unit(src, rng)
                    x, y = move
                items.append({"concept": CONCEPT_NAMES[c],
                              "x": float(x), "y": float(y)})
        creative_items[level] = items

    return {"probe_labels": probe_labels, "sequential": sequential,
            "creative_items": creative_items}


def run_test(seed):
    exemplars, probes = _taught(seed)
    results = {}
    for kind in ("perfect", "random", "copycat"):
        answers = _archetype(seed, kind, exemplars, probes)
        results[kind] = score_participant(answers, exemplars, probes)

    p = results["perfect"]
    r_ = results["random"]
    cp = results["copycat"]

    # P1 attainability: the perfect participant attains every engine bar.
    p1_ok = p["l1_ok"] and p["l2_ok"] and p["c1_ok"] and p["c2_ok"] \
        and p["c3_ok"]

    # P2 discrimination: the non-learner fails L1 and C1.
    p2_ok = (not r_["l1_ok"]) and (not r_["c1_ok"]) \
        and r_["l1_ceiling"] <= 0.30 and r_["yield"]["mid"]["creative"] <= 0.06

    # P3 the joint criterion binds on both sides (the human C3).
    y = p["yield"]
    p3_ok = (y["mid"]["creative"] >= 0.15
             and y["mid"]["creative"] > y["trivial"]["creative"]
             and y["mid"]["creative"] > y["wild"]["creative"]
             and y["trivial"]["valid"] > y["trivial"]["novel"]
             and y["wild"]["novel"] > y["wild"]["valid"]
             and cp["yield"]["mid"]["creative"] == 0.0)

    # P4 the C2 constraint holds on the human scale (rubric audit).
    p4_ok = p["c2_ok"]

    return {"per_archetype": results,
            "p1_ok": p1_ok, "p2_ok": p2_ok, "p3_ok": p3_ok, "p4_ok": p4_ok}


def _verdict():
    seeds = (42, 11, 7)
    per = {}
    for s in seeds:
        per[str(s)] = run_test(s)

    def ok(fn):
        return all(fn(per[str(s)]) for s in seeds)

    p1, p2, p3, p4 = (ok(lambda o: o["p1_ok"]), ok(lambda o: o["p2_ok"]),
                      ok(lambda o: o["p3_ok"]), ok(lambda o: o["p4_ok"]))

    claims = [
        {"id": "P1",
         "claim": "the human protocol's bars are attainable: a perfect "
                  "participant (exact held-out routing, mid-effort novel "
                  "variations) attains every engine bar - L1 ceiling >=0.90, "
                  "L2 no-forgetting >=0.85, C1 mid creative >=0.15, C2 and "
                  "C3 hold",
         "verdict": "SUPPORTED" if p1 else "FAILED"},
        {"id": "P2",
         "claim": "the bars discriminate: a non-learner (uniform random "
                  "routing, random generation) fails L1 (ceiling ~= 1/C) and "
                  "C1 (creative yield ~= 0) - the protocol is not passable "
                  "by chance",
         "verdict": "SUPPORTED" if p2 else "FAILED"},
        {"id": "P3",
         "claim": "the joint criterion binds on both sides (human C3): "
                  "within the perfect participant trivial-effort items are "
                  "valid-but-not-novel (valid > novel), wild-effort items "
                  "novel-but-not-valid (novel > valid), mid-effort is the "
                  "only positive creative yield (interior-peaked like the "
                  "engine), and a pure copycat's yield is exactly 0",
         "verdict": "SUPPORTED" if p3 else "FAILED"},
        {"id": "P4",
         "claim": "the C2 constraint holds on the human scale: random far "
                  "items grade ~100% novel but ~0% creative under the "
                  "pre-registered thresholds, so a facilitator using the rule "
                  "cannot count novelty alone as creativity",
         "verdict": "SUPPORTED" if p4 else "FAILED"},
    ]
    verdict = ("SUPPORTED" if all(c["verdict"] == "SUPPORTED"
                                  for c in claims) else "FAILED")
    m = per["42"]["per_archetype"]["perfect"]["yield"]["mid"]["creative"]
    results = {
        "experiment": "human_trial_pilot: the T74 human protocol instrument "
                      "- trial package + participant scorer + archetypal "
                      "pilot showing the bars are attainable (perfect) and "
                      "discriminating (random/copycat fail)",
        "date": datetime.date.today().isoformat(),
        "seeds": list(seeds),
        "claims": claims,
        "verdict": ("%s (structural, simulated-participant pilot; 3 seeds): "
                    "a perfect participant attains L1 >=0.90, L2 >=0.85, C1 "
                    ">=0.15 (mid-effort creative yield %.2f) and C2/C3 hold "
                    "(P1); a random non-learner's L1 ceiling ~= 1/C and C1 "
                    "~= 0 fail the bars (P2); trivial items are "
                    "valid-but-not-novel, wild items novel-but-not-valid, "
                    "mid is the only positive yield (P3); random far items "
                    "are ~100%% novel but ~0%% creative (P4)"
                    % (verdict, m)),
        "per_seed": per,
    }
    with open(DATA_JSON, "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    with open(PACKAGE_JSON, "w") as f:
        json.dump(make_package(42), f, indent=1, sort_keys=True)
    print("verdicts written to %s" % DATA_JSON)
    print("trial package written to %s" % PACKAGE_JSON)
    for c in claims:
        print("  %s: %s" % (c["id"], c["verdict"]))
    for k, o in per["42"]["per_archetype"].items():
        print("  %-7s L1ceiling=%.3f L2min=%s C1mid=%.3f  yields %s"
              % (k, o["l1_ceiling"], o["l2_min"],
                 o["yield"]["mid"]["creative"],
                 {lv: round(o["yield"][lv]["creative"], 3)
                  for lv in ("trivial", "mid", "wild")}))
    return results


def main(argv):
    if "--verdict" in argv:
        _verdict()
    else:
        r = run_test(42)
        print("human_trial_pilot: P1 %s P2 %s P3 %s P4 %s"
              % (r["p1_ok"], r["p2_ok"], r["p3_ok"], r["p4_ok"]))
        for k, o in r["per_archetype"].items():
            print("  %-7s L1 ceiling %.3f; L2 min %s; yields %s"
                  % (k, o["l1_ceiling"], o["l2_min"],
                     {lv: round(o["yield"][lv]["creative"], 3)
                      for lv in ("trivial", "mid", "wild")}))


if __name__ == "__main__":
    main(sys.argv[1:])
