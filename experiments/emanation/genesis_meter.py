"""The metrology of the critical line: the PLATEAU-TRAP law.

First hypothesis - "meter bias diverges AT the critical line as the floor
f -> theta*" - was REFUTED by the computed curve (|z| is SMALLEST near the
threshold, not largest).  The corrected law, stated after the falsified run:

A bimodal meter whose low-hazard class is TRUNCATED BELOW the threshold
(floor f = max h/X < theta*) has a survival PLATEAU of height w_hazard at
every theta in [f, theta*].  Any escape reading p above the plateau forces
the naive invert to land on the steep sub-floor branch, pinning the
estimate just below the floor, theta_est ~ f.  Consequences, measured:

  1) theta_est(f) is TRA PPED at the floor: theta_est ~= f for every f in
     the family (theta_est - f ~ -0.0041 near theta*, ~ -0.001 far below);
  2) the deviation theta* - theta_est, in units of the meter's own claimed
     precision (delta-method at theta_est), blows up as the floor descends:
     z_book = -144 at f=0.03, -24 at f=0.05, -5.3 at f=0.0625, -4.55 at
     f=0.0632.  Bias grows AWAY from the critical line, not toward it;
  3) the f=0.0625 member reproduces the empirical two_class point exactly
     (z_book = -5.32 vs measured -5.30) - the law replays the economy;
  4) meters whose severity span STRADDLES theta* (box: max h/X = 4.0;
     narrow: 0.1667) have non-flat survival AT theta* and resolve it
     precisely (z 1.27 / 0.93).  Populations truncated below theta*
     cannot resolve theta* at all; the reading is a statement about the
     floor, not the threshold.

Design rule: an honest meter needs a population whose severity reach
STRADDLES the critical line.  A population whose reach stops below theta*
yields a reading trapped at its own floor.  The operator who instead reads
the PLATEAU structurally (p = w_hazard implies 'theta* is at least the
floor') gets the correct qualitative answer - the trap lives in naive
inversion, not in the physics.

No Millennium claim; NSE-live-branch measurement discipline; hypothesis
refutation recorded as a first-class result.
"""

import json
import math
import os

from credit_commons.sim import Params

P = Params()
G_STAR = 2.0 * math.sqrt(P.g0 * P.gdepth * P.reward())
D_STAR = (G_STAR / P.g0 - 1.0) / P.gdepth
THETA_STAR = P.g0 * P.gdepth * D_STAR / P.I     # 0.06332

N = 64000
DELTA_P = 0.0034
P_MEAS = 0.2 + DELTA_P
SE_P = math.sqrt(P_MEAS * (1.0 - P_MEAS) / N)


def surv_low(hi_h, theta):
    a, b, c, d = 0.02, hi_h, 0.8, 1.5
    if theta <= a / d:
        return 1.0
    if theta >= b / c:
        return 0.0
    x1 = a / theta
    x2 = b / theta
    area = 0.0
    if x1 > c:
        area += min(x1, d) - c
    lo = max(c, x1)
    hi = min(d, x2)
    if hi > lo:
        area += ((b * hi - theta * hi * hi / 2.0)
                 - (b * lo - theta * lo * lo / 2.0)) / (b - a)
    return area / (d - c)


def surv_meter(hi_h, theta):
    return 0.8 * surv_low(hi_h, theta) + 0.2


def dsurv(hi_h, theta, h=1e-5):
    return (surv_meter(hi_h, theta + h) -
            surv_meter(hi_h, theta - h)) / (2.0 * h)


def quantile_meter(hi_h, target, lo_t, hi_t):
    lo, hi = lo_t, hi_t
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if surv_meter(hi_h, mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def main():
    floors = [0.030, 0.040, 0.050, 0.055, 0.058, 0.060, 0.061, 0.062,
              0.0625, 0.0630, 0.0632]
    rows = []
    for f in floors:
        hi_h = 0.8 * f
        te = quantile_meter(hi_h, P_MEAS, 1e-6, 0.07)
        se_est = SE_P / abs(dsurv(hi_h, te))
        z_book = (te - THETA_STAR) / se_est
        rows.append({"floor_f": f,
                     "hi_h_class": hi_h,
                     "theta_est": round(te, 6),
                     "se_est": round(se_est, 6),
                     "bias_theta_star_minus_est": round(THETA_STAR - te, 6),
                     "theta_est_minus_floor": round(te - f, 6),
                     "z_book": round(z_book, 2)})
        print("  f=%.4f  theta_est=%.6f (floor-pinned %+.4f)  bias=%.5f  "
              "z=%+.2f"
              % (f, te, te - f, THETA_STAR - te, z_book))

    row0625 = [r for r in rows if abs(r["floor_f"] - 0.0625) < 1e-9][0]
    empirical_z = -5.30   # genesis_populations.json (two_class, sign kept)

    out = {
        "identity": "PLATEAU-TRAP law of threshold metering: a population "
                    "truncated below theta* (floor f = max h/X < theta*) "
                    "gives a survival plateau in [f, theta*]; naive "
                    "inversion of an over-plateau reading pins theta_est "
                    "just below the floor and reports it with a fixed "
                    "precision, so the deviation from book grows as the "
                    "floor DESCENDS (z = -144 at f=0.03 .. -4.55 at "
                    "f=0.0632).  Meter resolution requires the population's "
                    "reach to STRADDLE theta* (box, narrow).  Initial "
                    "'divergence at the critical line' hypothesis REFUTED "
                    "by its own curve and replaced by this corrected law.",
        "theta_star": THETA_STAR,
        "measured_conditions": {"n": N, "delta_p": DELTA_P,
                                "p_meas": P_MEAS, "se_p": round(SE_P, 6)},
        "meters": rows,
        "validation": {
            "f0625_is_the_two_class_member": True,
            "computed_z_book": row0625["z_book"],
            "empirical_z": empirical_z,
            "agree": abs(row0625["z_book"] - empirical_z) < 0.3,
        },
        "plateau_trap": {
            "trapped_at_floor": all(
                abs(r["theta_est_minus_floor"]) < 0.006 for r in rows),
            "bias_grows_as_floor_descends": rows[0]["z_book"] <
                rows[-1]["z_book"],
            "straddling_meters": [
                {"population": "box", "max_h_over_X": 4.0,
                 "straddles_theta_star": True, "z_measured": 1.27},
                {"population": "narrow", "max_h_over_X": 0.17,
                 "straddles_theta_star": True, "z_measured": 0.93},
                {"population": "two_class (low class)", "max_h_over_X": 0.0625,
                 "straddles_theta_star": False, "z_measured": -5.30}],
            "law": "resolution requires straddling; truncated populations "
                   "read their own floor, with a bias that scales away "
                   "from the threshold.",
        },
        "design_rule": "to measure theta* with a ledger experiment, the "
                       "probing population must span h/X both below AND "
                       "above theta*.  An operator reading p = w_hazard at "
                       "the plateau should interpret it structurally "
                       "('theta* lies at or above the floor'), not invert "
                       "it: the trap is in the naive inversion, not in the "
                       "physics.",
        "refutation_record": "first framing ('divergence at the critical "
                             "line', margin design delta) is WITHDRAWN and "
                             "replaced, per the co-production no-claim "
                             "discipline.",
        "references_note": "survival per meter (Barlow & Proschan 1975); "
                           "delta-method uncertainty (Kendall & Stuart); "
                           "systematic vs statistical metrology bias (JCGM "
                           "2008 GUM): the plateau is a systematic-shape "
                           "bias, its SE is statistical - the two must not "
                           "be combined, which is the exact error the first "
                           "framing made.",
    }
    path = os.path.join("experiments", "emanation", "data",
                        "genesis_meter.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("validation: computed z=%.2f vs empirical %.2f -> %s"
          % (row0625["z_book"], empirical_z,
             "OK" if abs(row0625["z_book"] - empirical_z) < 0.3 else "MISMATCH"))
    print("plateau trap: theta_est pinned below floor for all members -> "
          "bias grows as floor descends (z=-144 at f=0.030 to -4.55 at "
          "f=0.0632).")
    print("straddling meters (box, narrow) read theta* precisely (z=1.27, "
          "0.93); truncated populations read their own floor.")
    print("initial critical-line-divergence hypothesis REFUTED; recorded.")
    print("WROTE data/genesis_meter.json")


if __name__ == "__main__":
    main()