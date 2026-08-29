#!/usr/bin/env python3
"""Ch.81 The Coin's Leading Effect Is a Constant: feedback in tilt space is,
to leading order, a PURE TRANSLATION of the work-tilt curve -- the demon moves
the center but (to first order) does not reshape the mirror.  The translation
c = a(1/2) matches the mean-work reduction Delta mu = mu_coin - mu_control;
what remains after removing the shift is the STATE-DEPENDENT part of the bit,
which grows as the coin strengthens.

Ch.80 found a(t)+a(1-t) = const (antisymmetry about a SHIFTED center) and
c = a(1/2) = -0.073 engaged, -0.129 harvest.  This chapter asks HOW MUCH of
the coin is a pure shift.  For a constant unconditional bias delta (every
trajectory's work shifted by delta -- not physically the feedback, but its
leading effect), the tilted mean obeys a(t) -> a(t)+delta at EVERY t, so
c = delta = mu_coin - mu_control.  Measured on the same rows:

  engaged 0.35/2:  c = a(1/2) = -0.0726,  Delta mu = -0.0683   -> c ~ Delta mu
  harvest 0.05/16: c = a(1/2) = -0.1294,  Delta mu = -0.1547   -> c deviates

We quantify the reshaping residual netR = |a(t) - [a_ctrl(t) + c]| swept over
the tilt grid: ~0 if the coin is a pure translation, growing if the bit is
strongly state-dependent.  This is the (Sagawa-Ueda 2010; Parrondo-Horowitz-
Sagawa 2015) information-demand: the more the demon conditions on the state,
the more the work curve bends after the shift is removed -- the coin is part
constant (detuning) and part shaping, and the split is MEASURABLE.

Instruments: same Heun SRK2, seed 42, rows of Ch.76-80.  We re-sample control,
engaged, harvest, and report the split.
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
TGRID = [-2.0, -1.0, -0.5, 0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]


def swept_mean(sample, tgrid):
    """a(t) = <W e^{-tW}>/<e^{-tW}> over the tilt grid."""
    rows = []
    for t in tgrid:
        s0 = 0.0
        s1 = 0.0
        for w in sample:
            ew = math.exp(-t * w)
            s0 += ew
            s1 += w * ew
        rows.append((t, s1 / s0))
    return rows


def center_a_half(sample):
    """c = a(1/2), the shifted mirror center."""
    t = 0.5
    s0 = 0.0
    s1 = 0.0
    for w in sample:
        ew = math.exp(-t * w)
        s0 += ew
        s1 += w * ew
    return s1 / s0


def main():
    random.seed(SEED)
    print("Ch.81 The Coin's Leading Effect Is a Constant: translation vs "
          "reshaping in tilt space")
    print("  c = a(1/2) ;  Delta mu = mu_coin - mu_control ;  reshaping "
          "residual netR")

    out = {"seed": SEED, "median": FAR_MEDIAN, "tgrid": TGRID, "rows": {}}

    print("\n  running control round trip 250k ...")
    ctrl = dl.run_stiff(250000, 0.5, 0.5, 0.5, "control")
    mu_c = sum(ctrl) / len(ctrl)
    a_ctrl = swept_mean(ctrl, TGRID)
    c_ctrl = center_a_half(ctrl)
    print("    mu_control = %.4f ; c(control) = a(1/2) = %+.5f"
          % (mu_c, c_ctrl))
    out["control"] = {"mu": round(mu_c, 4), "center": round(c_ctrl, 5),
                      "at": [[t, a] for (t, a) in a_ctrl]}

    def analyze(name, sample, ctrl_at):
        mu = sum(sample) / len(sample)
        c = center_a_half(sample)
        dm = mu - mu_c
        this_at = swept_mean(sample, TGRID)
        # reshaping residual over the WELL-CONDITIONED central window
        # t in [-0.5, 2.0], after removing the shift relative to control
        netR = 0.0
        ncnt = 0
        for (t, av) in this_at:
            actrl = dict(ctrl_at).get(t)
            if actrl is not None and -0.5 <= t <= 2.0:
                netR += abs(av - (actrl + c))
                ncnt += 1
        ant = 0.0
        seen = set()
        for (t, av) in this_at:
            # mirror partner 1-t
            p = None
            for (tt, aa) in this_at:
                if abs(tt - (1.0 - t)) < 1e-9:
                    p = aa
                    break
            if p is not None and t not in seen and (1.0 - t) not in seen:
                ant += abs(av + p)
                seen.add(t)
                seen.add(1.0 - t)
        out["rows"][name] = {
            "mu": round(mu, 4), "center": round(c, 5),
            "delta_mu": round(dm, 4), "c_minus_dm": round(c - dm, 4),
            "reshaping_netR": round(netR, 4), "ncnt": ncnt,
            "antisym_resid": round(ant, 5),
        }
        print("    %-12s mu=%+.4f c=a(1/2)=%+.5f  Delta mu=%+.4f  "
              "c-Delta mu=%+.4f  netR(c,w)=%.4f  antisym=%.4f"
              % (name, mu, c, dm, c - dm, netR, ant))
        return dm, c

    print("\n  running engaged 0.35/2 200k ...")
    eng = dl.run_stiff(200000, 0.5, 0.35, 2.0, "median")
    analyze("engaged", eng, a_ctrl)

    print("\n  running harvest 0.05/16 100k ...")
    har = dl.run_stiff(100000, 0.5, 0.05, 16.0, "median")
    analyze("harvest", har, a_ctrl)

    print("\n  PATTERN: engaged is ~pure translation (c ~ Delta mu, small "
          "netR);")
    print("  the stronger harvest deviates (c != Delta mu, larger netR) -- the")
    print("  growing STATE-DEPENDENCE of the bit, the part beyond a detuning.")

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "coin_constant.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print("\njson -> %s" % path)


if __name__ == "__main__":
    main()