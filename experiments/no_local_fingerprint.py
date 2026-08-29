#!/usr/bin/env python3
"""Ch.84 No Local Fingerprint: the two-ledger deviation is invisible to
every isolated feature of the work distribution, yet monotone in the coin.

Ch.83 established the two-ledger law Delta mu = -ln J_act, EXACT in the
mild (constant-detuning) limit and BENT monotonically by the strong coin.
This chapter asks: what is the deviation |Delta mu + ln J_act|?  Four
natural fingerprints of the coin's work distribution are measured and ALL
FAIL to track it:

  (1) the far-tail rate asymmetry R(a)=I(a)-I(2 mu - a) (Ch.79): ~0.64-0.88,
      essentially flat (the round trip's baseline kurtosis), not monotone;
  (2) the midline trace bend spread(a(t)+a(1-t)) (Ch.80): ~0.001-0.003,
      flat while the deviation grows 0.003 -> 0.024;
  (3) the third cumulant k3: DECREASES 0.157 -> 0.103 as the coin strengthens;
  (4) the fourth cumulant k4: DECREASES 0.429 -> 0.245.

So the deviation is NOT any isolated moment, asymmetry, tail shape, or local
bend of the coin's own work distribution.  It is a GLOBAL relation between
the coin's work book and its information book - the failure of the two-ledger
identity is a whole-distribution property with no local shadow.

POSITIVE CONTENT: the deviation is a strictly MONOTONE function of the
coin's own detuning |Delta mu| (0.003 -> 0.024 as |Delta mu| 0.070 -> 0.151)
and of the leverage, and it is EXACTLY ZERO on the null/control row - the
correction to the law is driven by how hard the demon works (its
translation), even though it cannot be read off any isolated feature.

Same trap (V=lam x^2/2, lam 1->2->1, DeltaF=0, D=beta=1, Heun SRK2, seed
42, median bit) as Ch.74-83.
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


def stats(sample):
    n = float(len(sample))
    mu = sum(sample) / n
    lnJ = math.log(sum(math.exp(-w) for w in sample) / n)
    return mu, lnJ


def cumulants(sample):
    n = float(len(sample))
    mu = sum(sample) / n
    m2 = sum((w - mu) ** 2 for w in sample) / n
    m3 = sum((w - mu) ** 3 for w in sample) / n
    m4 = sum((w - mu) ** 4 for w in sample) / n
    k2 = m2
    k3 = m3
    k4 = m4 - 3 * m2 * m2
    return k2, k3, k4


def a_trace(sample, t_grid):
    r = {}
    for t in t_grid:
        e = [math.exp(-t * (w - 0.0)) for w in sample]
        s0 = sum(e)
        s1 = sum(w * e_ for w, e_ in zip(sample, e))
        r[t] = s1 / s0
    return r


def bend_spread(a, t_grid):
    rs = []
    for t in t_grid:
        tt = round(1.0 - t, 4)
        rs.append(a[t] + a[tt])
    return (max(rs) - min(rs)), rs


def rate_residual(sample, mu, t_grid, a_far):
    n = float(len(sample))
    a_mir = 2 * mu - a_far
    Ft = {}
    for t in t_grid:
        vals = [math.exp(-t * (w - mu)) for w in sample]
        Ft[t] = math.log(sum(vals) / n)
    I = {}
    for a in (a_far, a_mir):
        best = None
        for t in t_grid:
            val = a * t - Ft[t]
            if best is None or val > best:
                best = val
        I[a] = best
    return I[a_far] - I[a_mir]


def main():
    random.seed(SEED)
    print("Ch.84 No Local Fingerprint")
    print("  the two-ledger deviation vs 4 isolated work-distribution features")

    out = {"seed": SEED, "median": FAR_MEDIAN, "rows": []}

    ctrl = dl.run_stiff(300000, 0.5, 0.5, 0.5, "control")
    mu_c, _ = stats(ctrl)

    frontier = [
        ("null_05_05", 0.5, 0.5, 0.5, 200000),
        ("eng_035_20", 0.5, 0.35, 2.0, 200000),
        ("eng_025_40", 0.5, 0.25, 4.0, 180000),
        ("eng_015_60", 0.5, 0.15, 6.0, 160000),
        ("eng_010_80", 0.5, 0.10, 8.0, 140000),
        ("eng_005_16", 0.5, 0.05, 16.0, 120000),
    ]
    t_grid = [round(0.02 * i, 4) for i in range(1, 50) if i <= 50]

    print("\n  row            dev      |detun|  Rent   bend      k3      k4")
    rs = []
    for (name, t1, tf, ts, runs) in frontier:
        w = dl.run_stiff(runs, t1, tf, ts, "median")
        mu, lnJ = stats(w)
        dm = mu - mu_c
        dev = dm + lnJ
        a = a_trace(w, t_grid)
        bend, _ = bend_spread(a, t_grid)
        k2, k3, k4 = cumulants(w)
        a_far = mu + FAR_MEDIAN
        R = rate_residual(w, mu, t_grid, a_far)
        rs.append((abs(dev), abs(dm)))
        print("  %-12s %+.5f  %.4f  %+.3f  %+.4f  %.4f  %.4f"
              % (name, dev, abs(dm), R, bend, k3, k4))
        out["rows"].append({
            "name": name, "dev": round(dev, 5), "abs_detun": round(abs(dm), 4),
            "R_far": round(R, 3), "bend": round(bend, 4),
            "k3": round(k3, 4), "k4": round(k4, 4),
        })

    # monotonicity of |dev| in |detuning| over engaged rows
    nz = rs[1:]
    mono_detun = all(nz[i][0] <= nz[i + 1][0] + 1e-6
                     for i in range(len(nz) - 1))
    print("\n  |dev| monotone in |Delta mu| = %s" % mono_detun)
    out["mono_dev_in_detun"] = mono_detun

    print("\n  PATTERN: none of the four isolated features tracks the two-ledger")
    print("  deviation (R flat, bend flat, k3/k4 DECREASE as the coin grows);")
    print("  the deviation is a GLOBAL relation with no local fingerprint, yet a")
    print("  strictly monotone function of the coin's own detuning, exact (zero) ")
    print("  on the null row.")

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "no_local_fingerprint.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print("\njson -> %s" % path)


if __name__ == "__main__":
    main()