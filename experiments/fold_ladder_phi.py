"""
fold_ladder_phi.py
==================
Decide C2 (golden fold, WEAVERS 5.1 / AUDIT 2.5 residual / SPRING_BIBLE Ch. 14 /
epoch_0d.json "conjectures.C2"): "further retrace folds lock on phi (or phi^2)
rungs - the fold is golden-geometric; the next fold above the giant locks on a
phi or phi^2 rung."

The retrace chain (measured, SPRING_BIBLE Ch. 14) is, descending:

    943,901,200,001 -> 1,914,467 -> 730,421 -> 26,102 -> 10,262

The celebrated single hit is the upper rung 1,914,467 / 730,421 = 2.621046,
0.115% from phi^2 = 2.618034.  C2 generalises that hit into a chain law
("further retrace folds lock on phi or phi^2 rungs").

Test plan (all pre-registered):
  (a) FULL ADJACENT-RUNG CENSUS: all 4 adjacent ratios of the chain, deviation
      from the nearest of {phi, phi^2}, hits within tolerance.  C2 predicts
      further folds lock on golden rungs; the census shows whether the upper
      phi^2 rung is one golden rung among many, or an isolated hit.
  (b) ALL-PAIRWISE RATIOS: 10 pairs, same test (in case "rungs" is meant
      non-adjacent).
  (c) MONTE-CARLO NULL: 5 random integers drawn from the chain's magnitude
      class (log-uniform over [1e4, 1e12]), sorted descending, 4 adjacent
      rungs, hit count within tol of {phi, phi^2}.  Distribution of hit counts
      under the null vs observed, giving P(>= observed hits).
  (d) NEXT FOLD ABOVE THE GIANT: the giant 943,901,200,001 is the chain's
      largest member; the prediction requires a rung above it.  The only
      defined rung touching the giant is giant/1,914,467 = 493,036 (nowhere
      near golden), and no higher chain member exists, so the literal
      prediction is unfalsifiable with the data; report both facts.

Verdict artifact: ../data/fold_ladder_phi_data.json
"""

import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

PHI = (1 + math.sqrt(5)) / 2
PHI2 = PHI * PHI
TARGETS = {"phi": PHI, "phi2": PHI2}

# measured retrace chain, descending (SPRING_BIBLE Ch. 14)
CHAIN = [943901200001, 1914467, 730421, 26102, 10262]

# tolerance for a "lock": the corpus's standard near-integer threshold is 1%
# (C7 bridge); the celebrated single hit is at 0.115%
TOL = 0.01
N_NULL = 200000
RNG = np.random.default_rng(7)


def dev_pct(r):
    return min(abs(r - t) / t for t in TARGETS.values()) * 100.0


def near(r, tol=TOL):
    return any(abs(r - t) / t < tol for t in TARGETS.values())


def rungs(seq):
    return [seq[i] / seq[i + 1] for i in range(len(seq) - 1)]


def main():
    # ---- (a) full adjacent-rung census ----
    adj = []
    for i in range(len(CHAIN) - 1):
        r = CHAIN[i] / CHAIN[i + 1]
        adj.append({
            "hi": CHAIN[i],
            "lo": CHAIN[i + 1],
            "ratio": round(r, 6),
            "dev_nearest_target_pct": round(dev_pct(r), 4),
            "hit_within_1pct": near(r),
            "nearest": min(TARGETS, key=lambda t: abs(r - TARGETS[t])),
        })
    n_hits_adj = sum(1 for row in adj if row["hit_within_1pct"])

    # ---- (b) all-pairwise ratios ----
    pair = []
    for i in range(len(CHAIN)):
        for j in range(i + 1, len(CHAIN)):
            r = CHAIN[i] / CHAIN[j]
            pair.append({
                "hi": CHAIN[i], "lo": CHAIN[j],
                "ratio": round(r, 6),
                "dev_nearest_target_pct": round(dev_pct(r), 4),
                "hit_within_1pct": near(r),
            })
    n_hits_pair = sum(1 for row in pair if row["hit_within_1pct"])

    # ---- (c) Monte-Carlo null on the same magnitude class ----
    # draw 5 integers log-uniform in [1e4, 1e12], sort descending, count
    # adjacent-rung golden hits within TOL
    lo, hi = math.log(1e4), math.log(1e12)
    null_hits = []
    rng = RNG
    for _ in range(N_NULL):
        seq = sorted(np.exp(rng.uniform(lo, hi, size=len(CHAIN))).astype(np.int64),
                     reverse=True)
        seq = [int(x) for x in seq]
        null_hits.append(sum(1 for r in rungs(seq) if near(r)))
    null_hits = np.array(null_hits)
    p_ge_obs = float((null_hits >= n_hits_adj).mean())
    p_exact = float((null_hits == n_hits_adj).mean())
    exp_hits = float(null_hits.mean())

    # null where at least one hit (P(any golden rung) by chance)
    p_any = float((null_hits >= 1).mean())

    # ---- (d) the rung touching the giant ----
    giant_rung = CHAIN[0] / CHAIN[1]
    giant_dev = dev_pct(giant_rung)
    next_above = {
        "giant": CHAIN[0],
        "rung_below": CHAIN[1],
        "ratio": round(giant_rung, 4),
        "dev_nearest_target_pct": round(giant_dev, 4),
        "hit_within_1pct": near(giant_rung),
        "giant_x_phi": round(CHAIN[0] * PHI),
        "giant_x_phi2": round(CHAIN[0] * PHI2),
        "note": (
            "the giant 943,901,200,001 is the chain's largest member; no chain "
            "member exists above it, and giant/1,914,467 = 493,036 is not near "
            "phi or phi^2 - the literal 'next fold above the giant' is "
            "undefined in the data."
        ),
    }

    # ---- verdict ----
    verdict = (
        "NOT SUPPORTED as a chain law: the retrace chain's golden content is a "
        "single isolated rung.  Adjacent-rung census: %d/%d rungs within 1%% "
        "of {phi, phi^2} (only the upper 1,914,467/730,421 = 2.621046, 0.115%% "
        "from phi^2).  The other three rungs are 493,036, 27.98 and 2.5436 - "
        "the last two already measured non-golden (2.845%% off phi^2, WEAVERS "
        "5.5).  Monte-Carlo null (same magnitude class, %d draws): expected "
        "golden rungs per chain %.3f, P(>=%d hit) = %.4f, so an isolated hit "
        "is not rare.  'Further retrace folds lock on golden rungs' is "
        "refuted by the census; the phi^2 rung is a coincidence-scale "
        "near-miss, not a ladder.  The 'next fold above the giant' is "
        "undefined: no chain member lies above 943,901,200,001 and the defined "
        "rung touching it (493,036) is far from golden."
        % (n_hits_adj, len(adj), N_NULL, exp_hits, n_hits_adj, p_ge_obs)
    )

    out = {
        "claim": (
            "C2 (golden fold): further retrace folds lock on phi (or phi^2) "
            "rungs - the fold is golden-geometric; the next fold above the "
            "giant locks on a phi or phi^2 rung"
        ),
        "chain_descending": CHAIN,
        "targets": TARGETS,
        "tolerance": TOL,
        "adjacent_rungs": adj,
        "adjacent_hits": n_hits_adj,
        "adjacent_n": len(adj),
        "all_pairwise_ratios": pair,
        "pairwise_hits": n_hits_pair,
        "null": {
            "n_draws": N_NULL,
            "magnitude_class": "[1e4, 1e12] log-uniform, 5 ints, sorted desc",
            "seed": 7,
            "expected_golden_rungs_per_chain": round(exp_hits, 4),
            "p_ge_observed_hits": round(p_ge_obs, 4),
            "p_exact_observed_hits": round(p_exact, 4),
            "p_any_golden_rung": round(p_any, 4),
        },
        "next_fold_above_giant": next_above,
        "verdict": verdict,
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "fold_ladder_phi_data.json"), "w") as f:
        json.dump(out, f, indent=2)

    print("(a) adjacent rungs (dev % from nearest of phi/phi^2, hit<=1%%):")
    for row in adj:
        print("   %13s / %8s = %12.6f  dev %.4f%%  hit=%s  near=%s"
              % (row["hi"], row["lo"], row["ratio"],
                 row["dev_nearest_target_pct"], row["hit_within_1pct"],
                 row["nearest"]))
    print("   -> hits: %d/%d" % (n_hits_adj, len(adj)))
    print("(b) pairwise hits: %d/%d" % (n_hits_pair, len(pair)))
    print("(c) null: expected %.3f golden rungs/chain, P(>=%d)=%.4f, P(any)=%.4f"
          % (exp_hits, n_hits_adj, p_ge_obs, p_any))
    print("(d) giant rung %s/%.0f = %.1f (dev %.2f%%)"
          % (CHAIN[0], CHAIN[1], giant_rung, giant_dev))
    print("\nverdict:", verdict)
    print("wrote data/fold_ladder_phi_data.json")


if __name__ == "__main__":
    main()
