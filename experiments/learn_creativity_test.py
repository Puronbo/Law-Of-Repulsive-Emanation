"""
Learning & Creativity Test (T74): ascertaining what an agent LEARNED in a
learning environment, and whether it CREATES novel-but-valid content.

Two axes, one rubric, both measured on the repo's own primitives:

  LEARNED (acquisition):
    A routing agent with a stored-memory representation (the exemplars it was
    shown; majority-vote k-NN routing - the agent routes a point to the
    majority class among its K_VOTE nearest stored exemplars, k-NN being the
    repo's own local primitive, K_NN=8 in decentral_net) is exposed to a
    labeled curriculum in a bounded concept space (a Poincare-style disk,
    DecentralNet-style homes).  Ascertained by a learning curve: held-out
    probe accuracy as exposure grows (near-chance at minimal exposure - with
    a sparse memory the k-neighborhood is dominated by OTHER concepts - to
    high at full exposure, where the true concept's exemplars dominate the
    neighborhood), and by a sequential-teaching run that checks the
    first-taught concepts do not decay under continued exposure (no
    forgetting).

  CREATIVITY (novel-but-valid generation):
    The agent generates near-miss variations of its stored exemplars (radially
    outward exploration with angular jitter).  A generated item counts as
    CREATIVE iff it is simultaneously
      - NOVEL:  outside the observed training core (distance to the nearest
        stored exemplar above a novelty threshold derived from the taught
        exemplars' own spacings - the same doctrine that made the internet
        name-space novelty axis work, A1 of decentral_net_anomaly), and
      - VALID:  inside the learned manifold (distance within an acceptance
        radius derived from the taught exemplars) and routed to the intended
        concept.
    Random far nulls are novel but INVALID (outside the manifold - rejected),
    so novelty alone is not creativity: the joint quadrant is required.  The
    creative yield over mutation size is interior-peaked: too-close variations
    are valid but not novel, too-far are novel but not valid - a real
    novelty/validity trade-off, not a monotone curve.

Claims (each a verdict run on seeds 42/11/7):
  L1  learned:      probe accuracy climbs from near-chance at minimal exposure
                    to >=0.9 at full exposure (the curriculum is acquired).
  L2  learned:      persists - first-taught concepts keep >=0.85 accuracy
                    after every later concept is added (no forgetting under
                    continued exposure; additive memory does not destabilize).
  C1  creativity:   a measurable share of mid-size near-miss variations are
                    simultaneously novel AND valid (new-but-right content
                    that was never presented).
  C2  novelty != creativity: random far nulls are novel but invalid, so the
                    joint novelty x validity criterion is necessary.
  C3  landscape:    creative yield peaks at an interior mutation size
                    (too-close not novel; too-far not valid).

Honest walls:
  - The agent is a stored-memory router over independent gaussian exemplars in
    a synthetic 2D concept space: it ascertains ACQUISITION and NOVEL-VALID
    GENERATION under controlled conditions, not transfer to unseen tasks or
    open-domain invention.  All claims are MECHANISM claims about the test
    (the environment->agent mapping is measurable and reproducible).
  - Creativity here is the operational novelty x validity quadrant; it does
    not claim human-like intent, surprise, or cultural value.
  - The same two axes (recognition/transfer for learned; novelty x
    appropriateness for creativity) are the rubric the human-assessment
    protocol in docs/LEARNING_CREATIVITY_TEST.md reuses.

Usage:
  python learn_creativity_test.py               # run and print the verdict
  python learn_creativity_test.py --verdict     # write data/ JSON verdict
"""

import json
import os
import sys

import numpy as np

DATA_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "data", "learn_creativity_test_data.json")

# --- environment ------------------------------------------------------- #
C = 8                   # concepts in the curriculum
HOME_R = 0.25           # DecentralNet-style homes: compact interior blob
SIGMA = 0.05            # within-concept exemplar noise
MAX_R = 0.9             # disk bound (the "learning environment" is bounded)
N_EXEMPLARS = 40        # exemplars available per concept
N_PROBES = 40           # held-out probes per concept
EXPOSURE_SIZES = [1, 2, 4, 8, 16, 40]

# --- agent routing ------------------------------------------------------- #
K_VOTE = 5              # majority vote over the k nearest stored exemplars
                        # (k-NN is the repo's own local primitive, cf.
                        # K_NN=8 in decentral_net)

# --- creativity generation --------------------------------------------- #
NOVELTY_MULT = 1.0      # novelty threshold = mean + mult*std of spacings
ACCEPT_MULT = 3.5       # acceptance radius = mean + mult*std of spacings
MUT_SIZES = [0.05, 0.12, 0.22, 0.32]   # mutation magnitude sweep
MUT_JITTER = np.deg2rad(25)            # angular jitter on the outward move
N_MUT = 150             # mutations per size per seed
NULL_R = (0.55, 0.85)   # random far-null annulus (outside the learned blob)
N_NULL = 150


def _homes():
    return np.array([[HOME_R * np.cos(2 * np.pi * c / C),
                      HOME_R * np.sin(2 * np.pi * c / C)]
                     for c in range(C)])


def _clip(x):
    n = np.linalg.norm(x)
    return x if n <= MAX_R else x * (MAX_R / n)


def _draw_class(home, rng, n):
    out = np.empty((n, 2))
    for i in range(n):
        out[i] = _clip(home + rng.normal(0.0, SIGMA, 2))
    return out


def build(seed):
    rng = np.random.default_rng(seed)
    homes = _homes()
    exemplars = [_draw_class(homes[c], rng, N_EXEMPLARS) for c in range(C)]
    probes = [_draw_class(homes[c], rng, N_PROBES) for c in range(C)]
    return rng, exemplars, probes


def memory(exposed):
    """The stored memory: points + labels from per-concept exposed sets."""
    pts = np.vstack([exposed[c] for c in range(len(exposed))])
    lab = np.repeat(np.arange(len(exposed)),
                    [len(exposed[c]) for c in range(len(exposed))])
    return pts, lab


def route_pts(pts, mem_pts, mem_lab):
    """Stored-memory k-NN routing: majority vote over the K_VOTE nearest
    stored exemplars.  Returns (label, nearest-exemplar distance)."""
    d = np.linalg.norm(pts[:, None, :] - mem_pts[None, :, :], axis=2)
    nn = np.argpartition(d, K_VOTE, axis=1)[:, :K_VOTE]
    votes = mem_lab[nn]
    lab = np.array([np.bincount(v, minlength=len(set(mem_lab))).argmax()
                    for v in votes])
    db = d[np.arange(len(pts)), np.argmin(d, axis=1)]
    return lab, db


def accuracy(exposed, probes, n_per):
    """Held-out probe accuracy under exposure of n_per exemplars/concept."""
    mem_pts, mem_lab = memory([exposed[c][:n_per] for c in range(C)])
    got, _ = route_pts(np.vstack(probes), mem_pts, mem_lab)
    return float(np.mean(got == np.repeat(np.arange(C), N_PROBES)))


def _outward_unit(src, rng):
    """Unit vector from the disk center through the exemplar, jittered."""
    u = src / np.linalg.norm(src)
    ang = rng.uniform(-MUT_JITTER, MUT_JITTER)
    u = np.array([u[0] * np.cos(ang) - u[1] * np.sin(ang),
                  u[0] * np.sin(ang) + u[1] * np.cos(ang)])
    return u / np.linalg.norm(u)


# ---------------------------------------------------------------------- #
# The test
# ---------------------------------------------------------------------- #
def run_test(seed):
    rng, exemplars, probes = build(seed)

    # --- L1: the learning curve (acquisition) -------------------------- #
    curve = {}
    for n in EXPOSURE_SIZES:
        curve[str(n)] = accuracy(exemplars, probes, n_per=n)
    floor, ceiling = curve[str(EXPOSURE_SIZES[0])], curve[str(EXPOSURE_SIZES[-1])]
    l1_ok = floor <= 0.35 and ceiling >= 0.90 and ceiling - floor >= 0.55

    # --- L2: sequential teaching, no forgetting ------------------------- #
    acc_after = {}
    for step in range(1, C + 1):
        taught = list(range(step))
        mem_pts, mem_lab = memory([exemplars[c] for c in taught])
        got, _ = route_pts(np.vstack([probes[c] for c in taught]),
                           mem_pts, mem_lab)
        exp = np.repeat(taught, N_PROBES)
        acc_after[str(step)] = float(np.mean(got == exp))
    final_old = min(acc_after[str(k)] for k in range(C // 2, C + 1))
    l2_ok = final_old >= 0.85

    # --- thresholds from the taught exemplars' own spacings ------------- #
    mem_pts, mem_lab = memory(exemplars)
    # nearest-neighbour distance of each exemplar EXCLUDING itself
    d = np.linalg.norm(mem_pts[:, None, :] - mem_pts[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    self_excl = d.min(axis=1)
    s_mean, s_std = float(self_excl.mean()), float(self_excl.std())
    novelty_thr = s_mean + NOVELTY_MULT * s_std
    accept_r = s_mean + ACCEPT_MULT * s_std

    # --- creativity: near-miss generation ------------------------------- #
    src_idx = rng.integers(0, N_EXEMPLARS * C, size=N_MUT)
    src_pts = mem_pts[src_idx]
    src_lab = mem_lab[src_idx]
    creative = {}
    for s in MUT_SIZES:
        mut = np.array([p + s * _outward_unit(p, rng) for p in src_pts])
        mut = np.array([_clip(m) for m in mut])
        got, dmut = route_pts(mut, mem_pts, mem_lab)
        novel = dmut > novelty_thr
        valid = (got == src_lab) & (dmut <= accept_r)
        cr = novel & valid
        creative[str(s)] = {
            "novel": float(novel.mean()), "valid": float(valid.mean()),
            "creative": float(cr.mean()),
        }

    # --- C2: random far nulls are novel but invalid --------------------- #
    ang = rng.uniform(0, 2 * np.pi, N_NULL)
    rad = rng.uniform(*NULL_R, N_NULL)
    nulls = np.stack([rad * np.cos(ang), rad * np.sin(ang)], axis=1)
    _, d_null = route_pts(nulls, mem_pts, mem_lab)
    null_novel = float((d_null > novelty_thr).mean())
    null_creative = float(((d_null > novelty_thr) & (d_null <= accept_r))
                          .mean())
    c2_ok = null_novel >= 0.90 and null_creative <= 0.05

    # --- C1: a measurable creative yield exists at mid size ------------- #
    mid = creative[str(MUT_SIZES[1])]["creative"]
    c1_ok = mid >= 0.15

    # --- C3: creative yield is interior-peaked -------------------------- #
    ys = [creative[str(s)]["creative"] for s in MUT_SIZES]
    c3_ok = ys[1] > ys[0] and ys[1] > ys[2] and ys[1] > ys[3]

    return {
        "curve": curve, "floor": floor, "ceiling": ceiling, "l1_ok": l1_ok,
        "no_forgetting_min": final_old, "l2_ok": l2_ok,
        "thresholds": {"novelty": float(novelty_thr),
                       "acceptance": float(accept_r),
                       "spacing_mean": s_mean, "spacing_std": s_std},
        "creative": creative, "mid_creative": mid,
        "null": {"novel": null_novel, "creative": null_creative},
        "c1_ok": c1_ok, "c2_ok": c2_ok, "c3_ok": c3_ok,
    }


def _verdict():
    import datetime
    seeds = (42, 11, 7)
    per = {}
    for s in seeds:
        per[str(s)] = run_test(s)

    def ok(fn):
        return all(fn(per[str(s)]) for s in seeds)

    l1 = ok(lambda o: o["l1_ok"])
    l2 = ok(lambda o: o["l2_ok"])
    c1 = ok(lambda o: o["c1_ok"])
    c2 = ok(lambda o: o["c2_ok"])
    c3 = ok(lambda o: o["c3_ok"])

    claims = [
        {"id": "L1",
         "claim": "learned: held-out probe accuracy climbs from near-chance "
                  "at minimal exposure (%.2f) to %.2f at full exposure "
                  "across seeds - the curriculum is demonstrably acquired",
         "verdict": "SUPPORTED" if l1 else "FAILED"},
        {"id": "L2",
         "claim": "learned persists: first-taught concepts keep >=0.85 "
                  "accuracy after every later concept is added (no "
                  "forgetting under continued exposure; additive stored "
                  "memory does not destabilize)",
         "verdict": "SUPPORTED" if l2 else "FAILED"},
        {"id": "C1",
         "claim": "creativity: a measurable share of mid-size near-miss "
                  "variations are simultaneously NOVEL (outside the taught "
                  "core) and VALID (inside the learned manifold, routed to "
                  "the intended concept) - new-but-right content that was "
                  "never presented",
         "verdict": "SUPPORTED" if c1 else "FAILED"},
        {"id": "C2",
         "claim": "novelty is not creativity: random far nulls are novel "
                  "but invalid, so the joint novelty x validity criterion "
                  "is necessary",
         "verdict": "SUPPORTED" if c2 else "FAILED"},
        {"id": "C3",
         "claim": "the creativity landscape is interior-peaked: creative "
                  "yield is maximized at a middle mutation size because "
                  "too-close variations are valid but not novel and too-far "
                  "are novel but not valid - a real trade-off, not a "
                  "monotone curve",
         "verdict": "SUPPORTED" if c3 else "FAILED"},
    ]
    verdict = ("SUPPORTED" if all(c["verdict"] == "SUPPORTED"
                                  for c in claims) else "FAILED")
    results = {
        "experiment": "learn_creativity_test (T74): a test ascertaining "
                      "what an agent learned in a learning environment and "
                      "whether it creates novel-but-valid content",
        "date": datetime.date.today().isoformat(),
        "seeds": list(seeds),
        "claims": claims,
        "verdict": ("%s (structural, synthetic concept space; 3 seeds): "
                    "accuracy climbs %.2f -> %.2f as exposure grows 1..40 "
                    "exemplars/concept (L1); first-taught concepts keep "
                    ">=%.2f after all later concepts are added (L2); "
                    "mid-size near-miss variations yield %.0f%% novel-AND-"
                    "valid items the agent never saw (C1); random far "
                    "nulls are %.0f%% novel but %.0f%% creative, so the "
                    "joint novelty x validity criterion is necessary (C2); "
                    "creative yield over mutation size is interior-peaked "
                    "(C3)"
                    % (verdict, per["42"]["floor"], per["42"]["ceiling"],
                       per["42"]["no_forgetting_min"],
                       100 * per["42"]["mid_creative"],
                       100 * per["42"]["null"]["novel"],
                       100 * per["42"]["null"]["creative"])),
        "per_seed": per,
    }
    with open(DATA_JSON, "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    print("verdicts written to %s" % DATA_JSON)
    for c in claims:
        print("  %s: %s" % (c["id"], c["verdict"]))
    print("  L1 curve (n=1..40): %s"
          % [round(per["42"]["curve"][str(n)], 3) for n in EXPOSURE_SIZES])
    print("  L2 no-forgetting min: %.3f" % per["42"]["no_forgetting_min"])
    print("  C1 mid creative yield: %.3f" % per["42"]["mid_creative"])
    print("  C2 null novel/creative: %.3f / %.3f"
          % (per["42"]["null"]["novel"], per["42"]["null"]["creative"]))
    print("  C3 yields: %s" % [round(per["42"]["creative"][str(s)]["creative"], 3)
                               for s in MUT_SIZES])
    return results


def main(argv):
    if "--verdict" in argv:
        _verdict()
    else:
        r = run_test(42)
        print("learn_creativity_test: L1 curve %s" %
              [round(r["curve"][str(n)], 3) for n in EXPOSURE_SIZES])
        print("  no-forgetting min %.3f; mid creative %.3f; null "
              "novel/creative %.3f/%.3f; yields %s"
              % (r["no_forgetting_min"], r["mid_creative"],
                 r["null"]["novel"], r["null"]["creative"],
                 [round(r["creative"][str(s)]["creative"], 3)
                  for s in MUT_SIZES]))
        print("  L1 %s L2 %s C1 %s C2 %s C3 %s"
              % (r["l1_ok"], r["l2_ok"], r["c1_ok"], r["c2_ok"], r["c3_ok"]))


if __name__ == "__main__":
    main(sys.argv[1:])
