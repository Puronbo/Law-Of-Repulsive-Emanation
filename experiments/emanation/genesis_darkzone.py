"""The dark-number window: escapes exist yet are statistically invisible.

genesis_crossover.json measured the ignition switch: naive resolvability of
theta* turns on only when the population's floor f exceeds ~1.10*theta*
(margin).  This run isolates the consequen ce of that fact:

  ESCAPE-METAMERY WINDOW  (theta*, f_D): the low-hazard class crosses the
  critical line (f > theta*, so SOME escapes occur that would not at
  f <= theta*) yet the excess over the 0.20 plateau is below 3 sigma of a
  finite sample.  A naive observer reading the plateau cannot distinguish
  'floor at theta*' from 'floor at f_D' - the crossing is silent.

Measured here, all closed-form (survival S_A per meter) plus a binomial
power analysis, no new MC:

  1) excess(f) = 0.8*S_A(theta*) as f crosses theta*;
  2) 3-sigma detectability floor f_D: excess = 3*SE_p at n=64000;
  3) silence band width (f_D - theta*)/theta*;
  4) sample-size scaling: SE_p ~ 1/sqrt(n), so the silent window SHRINKS
     as n grows - darkness is a finite-sample phenomenon;
  5) the honest two-sided design statement: an economy either stays
     strictly below the line (safe, blind) or must cross it loudly
     (f >= f_D); operating in (theta*, f_D) buys events without knowledge.

Consequence for the ledger and its branch map: the engine's one boundary
has a shadow - near-critical populations can be in catastrophe silently.
No Millennium claim; statistical statements follow standard binomial power
analysis (Cohen 1988; Casella & Berger 2002).
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


def excess(f):
    """Extra escape above the 0.20 plateau for a meter with floor f."""
    if f <= THETA_STAR:
        return 0.0
    return 0.8 * surv_low(0.8 * f, THETA_STAR)


def se_p(p, n):
    return math.sqrt(p * (1.0 - p) / n)


def bisection_f(target_excess, lo_f, hi_f):
    lo, hi = lo_f, hi_f
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if excess(mid) < target_excess:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def main():
    p0 = 0.2
    se0 = se_p(p0, N)
    det3 = 3.0 * se0                          # ~ 0.00474
    f_D = bisection_f(det3, THETA_STAR, 0.085)
    f_S = 0.070                                # ignition switch (crossover)

    # sample-size scaling: darkness is finite-sample
    scaling = []
    for n in (8000, 32000, 64000, 256000, 1024000):
        se = se_p(p0, n)
        fd = bisection_f(3.0 * se, THETA_STAR, 0.085)
        scaling.append({"n": n, "se": round(se, 6),
                        "f_D": round(fd, 5),
                        "silence_fraction": round((fd - THETA_STAR) /
                                                  THETA_STAR, 4)})

    table = []
    for f in (0.0630, 0.0640, 0.0650, 0.0675, 0.0682, 0.0700, 0.0750,
              0.0800):
        table.append({"floor_f": f,
                      "excess_over_plateau": round(excess(f), 6),
                      "excess_in_sigma": round(excess(f) / se0, 2),
                      "audible": excess(f) >= det3,
                      "naive_z_book_from_crossover": None})

    out = {
        "identity": "DARK-NUMBER window: for floors in (theta*, f_D) the "
                    "population crosses the critical line yet the escape "
                    "excess is below 3 sigma at n=64000 - catastrophe "
                    "without statistics.  The boundary's shadow: near-"
                    "critical populations can be in trouble silently.",
        "theta_star": THETA_STAR, "n": N,
        "plateau": p0, "se_p_at_n": round(se0, 6),
        "detectability_3sigma_in_escape_units": round(det3, 6),
        "windows": {
            "dark_regime": "f < theta*: no excess escapes (0.20 plateau "
                           "exact), safe and blind",
            "silent_crossing": "(theta* = %.5f, f_D = %.5f), width "
                               "(f_D-theta*)/theta* = %.4f: excess exists, "
                               "< 3 sigma, unreadable" % (THETA_STAR, f_D,
                                                          (f_D - THETA_STAR) /
                                                          THETA_STAR),
            "twilight": "(f_D, f_S = %.3f): audible but naive reading still "
                        "biased (|z_book|>1)" % f_S,
            "luminous": "f >= f_S: the threshold reads within 1 sigma",
            "ethics": "in the silent window the naive observer sees the "
                      "plateau and cannot distinguish theta* from f_D - "
                      "metamery.  Design: either stay strictly below the "
                      "line (accept blindness) or cross it LOUDLY "
                      "(f >= f_D, and better f >= f_S).  Operating in "
                      "(theta*, f_D) buys events without knowledge.",
        },
        "excess_table": table,
        "scaling": {
            "rule": "SE_p ~ 1/sqrt(n), so f_D descends toward theta* and "
                    "the silent window SHRINKS: darkness is a finite-"
                    "sample phenomenon.",
            "data": scaling,
        },
        "design_number": "loud crossing at n=64000 requires floor "
                         "f >= %.4f (%.1f%% above theta*); 3-sigma "
                         "audibility at f_D = %.4f." % (f_S,
                        100.0 * (f_S - THETA_STAR) / THETA_STAR, f_D),
        "references_note": "binomial power analysis for the 3-sigma "
                           "audibility threshold (Cohen 1988, Statistical "
                           "Power Analysis; Casella & Berger 2002, "
                           "Statistical Inference); survival/quants after "
                           "Barlow & Proschan 1975; the boundary's use as "
                           "the NSE-live assignment unchanged.",
    }
    path = os.path.join("experiments", "emanation", "data",
                        "genesis_darkzone.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("plateau p0=0.2, SE=%.6f (n=%d); 3-sigma audibility = %.5f"
          % (se0, N, det3))
    print("silent window: theta*=%.5f < f < f_D=%.5f  (width %.1f%% of "
          "theta*)" % (THETA_STAR, f_D, 100.0 * (f_D - THETA_STAR) /
                       THETA_STAR))
    for f in (0.0635, 0.0650, 0.0675, 0.0682, 0.0700):
        print("  f=%.4f excess=%.5f (=%.1f sigma at n=%d) audible=%s"
              % (f, excess(f), excess(f) / se0, N, excess(f) >= det3))
    print("scaling (SE~1/sqrt(n)): ")
    for s in scaling:
        print("  n=%7d se=%.6f f_D=%.5f silence=%.1f%%"
              % (s["n"], s["se"], s["f_D"], 100.0 * s["silence_fraction"]))
    print("WROTE data/genesis_darkzone.json")


if __name__ == "__main__":
    main()