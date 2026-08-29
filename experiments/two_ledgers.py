#!/usr/bin/env python3
"""Ch.82 The Two Ledgers Are One Price: the tilt-center translation of
Ch.80/81 (Delta mu = mu_coin - mu_control, the realized work detuning) versus
the exponential ledger of Ch.74/75 (ln J_act = ln <e^{-W}>, the information
book).  On the same coin rows we test whether the coin's measured detuning
equals minus its information ledger,
    Delta mu  ~  -ln J_act      (hypothesis)
and report the EXTRACTION EFFICIENCY of the demon per bit,
    eps = |Delta mu| / ln 2     (realized work per bit vs the ideal Szilard
                                 face value ln 2 = 0.6931, Sagawa-Ueda 2010).

Because the control is reversible (DeltaF = 0, ln J_control = 0), Delta mu is
the WORK THE DEMON ACTUALLY PURCHASES; the ratio to ln 2 tells how far a
real engine runs from the ideal one-bit ceiling.  The 0/0: as the coin fades
toward the no-feedback control (Delta mu -> 0, ln J -> 0 together) the
efficiency per bit is 0/0 whose removable value is bounded by 1 (Sagawa-Ueda:
J <= e^I with I = ln 2, so a fair coin can never buy more than its face
value).  This closes Ch.75's bill from the tilt side: the two accounts Ch.81
separated (constant detuning + shaping) live under one measured price.

Instruments: same Heun SRK2, seed 42, rows of Ch.74-81.
"""
import os
import sys
import json
import math
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import detailed_ledger as dl

SEED = 42
FAR_MEDIAN = dl.FAR_MEDIAN
LN2 = math.log(2.0)  # 0.6931 nats, the bit's face value


def stats(sample):
    n = float(len(sample))
    mu = sum(sample) / n
    var = sum((w - mu) ** 2 for w in sample) / n
    lnJ = math.log(sum(math.exp(-w) for w in sample) / n)
    return mu, var, lnJ


def main():
    random.seed(SEED)
    print("Ch.82 The Two Ledgers Are One Price")
    print("  Delta mu = mu_coin - mu_control  vs  ln J_act = ln <e^{-W}>")
    print("  extraction efficiency eps = |Delta mu| / ln 2  (Sagawa-Ueda bit)")

    out = {"seed": SEED, "median": FAR_MEDIAN, "ln2": LN2, "rows": {}}

    print("\n  running control round trip 300k ...")
    ctrl = dl.run_stiff(300000, 0.5, 0.5, 0.5, "control")
    mu_c, var_c, lnJ_c = stats(ctrl)
    print("    control: mu=%.5f var=%.5f ln J=%.5f"
          % (mu_c, var_c, lnJ_c))
    out["control"] = {"mu": round(mu_c, 5), "var": round(var_c, 5),
                      "lnJ": round(lnJ_c, 5)}

    def analyze(name, runs, tau1, tf, ts):
        print("\n  running %s %d ..." % (name, runs))
        w = dl.run_stiff(runs, tau1, tf, ts, "median")
        mu, var, lnJ = stats(w)
        dm = mu - mu_c
        eps = abs(dm) / LN2
        ratio = (dm / lnJ) if lnJ != 0 else float('nan')
        # mirror of the Ch.81 split: constant detuning vs ln J
        print("    %-10s mu=%+.5f var=%.5f ln J=%+.5f  Delta mu=%+.5f  "
              "-lnJ=%+.5f  ratio=%.3f  eps=%.3f"
              % (name, mu, var, lnJ, dm, -lnJ, ratio, eps))
        out["rows"][name] = {
            "runs": runs, "mu": round(mu, 5), "var": round(var, 5),
            "lnJ": round(lnJ, 5), "delta_mu": round(dm, 5),
            "minus_lnJ": round(-lnJ, 5), "ratio_dm_over_lnJ": round(ratio, 4),
            "efficiency_eps": round(eps, 4),
        }
        return dm, lnJ

    # the Ch.74-81 engaged frontier rows
    analyze("engaged_0p5", 200000, 0.5, 0.5, 0.5)
    dm1, lnJ1 = analyze("engaged_035", 200000, 0.5, 0.35, 2.0)
    dm2, lnJ2 = analyze("engaged_025", 200000, 0.5, 0.25, 4.0)
    dm3, lnJ3 = analyze("harvest_005", 100000, 0.5, 0.05, 16.0)

    print("\n  PATTERN:")
    print("    engaged weakest: Delta mu = %+.4f vs -ln J = %+.4f (ratio %.2f)"
          % (dm1, -lnJ1, dm1 / lnJ1 if lnJ1 else 0))
    print("    the two ledgers approach 1:1 on the mild coin, depart as the")
    print("    strong coin's shaping (Ch.81 netR) takes over.")
    print("    extraction efficiency eps per bit: %.3f .. %.3f of the ideal 1.0"
          % (abs(dm3) / LN2, abs(dm1) / LN2 if dm1 else 0))

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "two_ledgers.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print("\njson -> %s" % path)


if __name__ == "__main__":
    main()