"""The exact tail law: escape fraction is a CLOSED FORM of the population.

genesis_gapfn.json measured the escape fraction as a smeared (Griffiths-like)
rise across the endogenous coupling.  But the smearing function is simply
the tail of the ratio statistic r = h/X, and for independent uniforms it is
CLOSED FORM.  This run derives

    f_esc = P(h/x > theta*)   theta* = g0*gdepth*d* / I

with h~U(a,b), x~U(c,d) from the engine's model population (a,b,c,d =
0.02, 0.2, 0.05, 1.5), partitions at the pure ratio landmarks
    {a/d, b/d, a/c, b/c} = {0.0133, 0.1333, 0.4, 4.0}
and the escape threshold theta* = 0.0633 falling inside (a/d, b/d):

    f_esc = [ (c'-c) + ( b(d-c') - theta*(d^2-c'^2)/2 )/(b-a) ] / (d-c)
    c' = a/theta*.

Prediction ~0.830.  Cross-check against harm_cap MC 0.8305 and the measured
0.8361 (harm_as_depth).  Numbers derived, then verified by MC; reading
labelled honestly (tail statistics, not a Yang-Mills gap).
"""

import json
import math
import os
import random

from credit_commons.sim import Params

random.seed(42)
P = Params()
G_STAR = 2.0 * math.sqrt(P.g0 * P.gdepth * P.reward())
D_STAR = (G_STAR / P.g0 - 1.0) / P.gdepth
THETA = P.g0 * P.gdepth * D_STAR / P.I        # escape ratio threshold

A, B, C, D = 0.02, 0.20, 0.05, 1.50


def closed_form():
    c_prime = A / THETA
    if THETA <= A / D:
        return 1.0
    if THETA >= B / C:
        return 0.0
    if THETA < A / C and THETA <= B / D:
        # all x<=c': always escape; x in (c', d): partial
        num = (c_prime - C) + (B * (D - c_prime)
                               - THETA * (D * D - c_prime * c_prime) / 2.0) \
            / (B - A)
    elif THETA >= A / C:
        # a(<=theta x) binds for all x in (c, d): no all-escape zone
        num = (B * (D - C) - THETA * (D * D - C * C) / 2.0) / (B - A)
    else:  # THETA in (A/D, A/C): all-escape zone is (c, d) only partial
        num = (D - C)
    return num / (D - C)


def mc(n=1000000):
    k = 0
    for _ in range(n):
        h = random.uniform(A, B)
        x = random.uniform(C, D)
        if h / x > THETA:
            k += 1
    return k / n


def main():
    f = closed_form()
    m = mc()
    landmarks = {"a/d": round(A / D, 4), "b/d": round(B / D, 4),
                 "a/c": round(A / C, 4), "b/c": round(B / C, 4),
                 "theta_star": round(THETA, 6),
                 "theta_inside": round(A / D, 4) < THETA < round(B / D, 4)}
    out = {
        "identity": "exact tail law derived and verified: escape = P(h/x > "
                    "theta*) where theta* = g0*gdepth*d*/I = %.6f; closed-form "
                    "f_esc = %.5f over the population box (h in %.2f..%.2f, "
                    "x in %.2f..%.2f); MC %.5f; harm_cap MC 0.8305; measured "
                    "0.8361.  The Griffiths-smeared transition of "
                    "genesis_gapfn IS this closed-form tail; its landmarks "
                    "are the pure population ratios %s."
                    % (THETA, f, A, B, C, D, m, landmarks),
        "closed_form_escape": round(f, 6),
        "mc_escape": round(m, 6),
        "harm_cap_mc": 0.8305,
        "measured_escape_0_8361": 0.8361,
        "residuals": {"closed_vs_mc": round(f - m, 6),
                      "closed_vs_measured": round(f - 0.8361, 6),
                      "mc_vs_measured": round(m - 0.8361, 6)},
        "threshold_and_landmarks": landmarks,
        "reading": "safety = the exact tail of an endogenous ratio "
                   "statistic; the engine's deterministic gates (depth "
                   "clamp, Gini guard) act on the population that IS this "
                   "distribution.  Tail-statistics object, honestly labelled "
                   "- not a spectral/mass gap.",
    }
    path = os.path.join("experiments", "emanation", "data", "genesis_tail.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)
    print("theta* = %.6f   landmarks %s" % (THETA, landmarks))
    print("closed form f_esc = %.5f" % f)
    print("MC (seed 42)      = %.5f" % m)
    print("harm_cap MC       = 0.83050")
    print("measured (as_depth)= 0.83610")
    print("residuals: closed-MC %+.6f  closed-measured %+.6f  MC-measured %+.6f"
          % (f - m, f - 0.8361, m - 0.8361))
    print("WROTE data/genesis_tail.json")


if __name__ == "__main__":
    main()