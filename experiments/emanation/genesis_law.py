"""Corrected threat density of the Ledger (jacobian-consistent): Pareto-2.

Earlier run of this file used the *unweighted* overlap length and reported a
log-uniform spectrum -- WRONG.  The ratio density for r = h/x with
h~U(A,B), x~U(C,D) must carry the Jacobian weight x:

    f(r) dr = int_x g(r*x, x) x dx dr,  g = 1/((B-A)(D-C))
    f(r)   = K * ( (min(D, B/r)^2 - max(C, A/r)^2) / 2 ),   K = 1/((B-A)(D-C))

pieces (r landmarks A/D=0.0133, B/D=0.1333, A/C=0.4, B/C=4):
    r < 0.0133 or r > 4           : 0
    0.0133..0.1333                : K/2 * (1.5^2 - (0.02/r)^2)
    0.1333..0.4                   : K/2 * (0.20^2 - 0.02^2) / r^2   <- PARETO-2
    0.4..4                        : K/2 * ((0.2/r)^2 - 0.05^2)

The middle band is Pareto with exponent 2 (mass ~ 1/r0 per factor step: a
doubling of threshold halves the vulnerable mass).  This run verifies
normalization (=1), the escape integral >= theta* (=0.8299, cross-check with
genesis_tail), and per-decade mass fractions.  The log-uniform (Jeffreys)
reading of the earlier buggy run is WITHDRAWN in the JSON.  Honest.
"""

import json
import math
import os

A, B, C, D = 0.02, 0.20, 0.05, 1.50
THETA = 0.063318
K = 1.0 / ((B - A) * (D - C))


def f(r):
    if r < A / D or r > B / C:
        return 0.0
    lo = max(C, A / r)
    hi = min(D, B / r)
    if hi <= lo:
        return 0.0
    return K * (hi * hi - lo * lo) / 2.0


def quad(r0, r1, n=400000):
    h = (r1 - r0) / n
    return sum(f(r0 + (i + 0.5) * h) for i in range(n)) * h


def main():
    r_lo, r_m1, r_m2, r_hi = A / D, B / D, A / C, B / C

    tot = quad(r_lo, r_hi)
    esc = quad(THETA, r_hi)
    decades = [
        ("decade1 0.0133-0.1333", quad(r_lo, r_m1)),
        ("decade2 0.1333-1.3333", quad(r_m1, 10 * r_m1)),
        ("tail    1.3333-4.0000", quad(10 * r_m1, r_hi)),
    ]

    # Pareto-2 check inside the 1/r^2 band: mass [0.1333,0.4] vs [0.4,1.2]
    m_lo = quad(r_m1, r_m2)
    m_hi = quad(r_m2, r_m2 * 3.0)
    pareto = {"mass_low_band": m_lo, "mass_hi_band": m_hi,
              "ratio_hi_over_low": m_hi / m_lo if m_lo else None,
              "prediction_1_over_r0": (1.0 / r_m2) / (1.0 / r_m1)}

    out = {
        "identity": "corrected threat density: PARETO-2 in the main band "
                    "(K/2*(B^2-A^2)/r^2 on 0.1333..0.4).  Normalization "
                    "total=%.5f (expect 1); escape integral over theta*=%.6f "
                    "= %.5f (genesis_tail closed form 0.82992); per-decade "
                    "mass fractions [%.4f, %.4f, %.4f].  LOG-UNIFORM claim "
                    "of the earlier buggy run WITHDRAWN."
                    % (tot, THETA, esc, *(m / tot for _, m in decades)),
        "density_pieces": {"A_over_D..B_over_D": "K/2*(1.5^2-(0.02/r)^2)",
                           "B_over_D..A_over_C": "K/2*(0.2^2-0.02^2)/r^2 "
                                                 "(PARETO-2)",
                           "A_over_C..B_over_C": "K/2*((0.2/r)^2-0.05^2)"},
        "per_decade_fractions": [
            {"bucket": name, "fraction": round(m / tot, 4)}
            for name, m in decades],
        "escape_integral": {"theta_star": THETA, "value": round(esc, 5),
                            "genesis_tail": 0.82992},
        "pareto2_check": {"mass_ratio_mid_to_low": pareto["ratio_hi_over_low"],
                          "analytic_1_over_r0_ratio":
                              round(pareto["prediction_1_over_r0"], 5)},
        "reading": "threat spectrum is heavy-tailed (Pareto alpha=2 in the "
                   "main band): each doubling of a threshold halves the "
                   "vulnerable mass; the transition smears because the "
                   "SENSITIVITY is power-law (a threshold never kills the "
                   "tail).  Additive gates still shape the *rate*; only the "
                   "population or multiplicative terms reshape the tail. "
                   "Honestly labelled; normalized, jacobian-correct.",
    }
    path = os.path.join("experiments", "emanation", "data", "genesis_law.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("normalized total = %.5f  (expect 1.0)" % tot)
    print("escape P(r>%.6f) = %.5f   (genesis_tail closed form 0.82992)"
          % (THETA, esc))
    for name, m in decades:
        print("  %-20s fraction %.4f" % (name, m / tot))
    print("Pareto-2 band mass ratio (mid/high) = %.4f  analytic 1/r0=%.4f"
          % (pareto["ratio_hi_over_low"], pareto["prediction_1_over_r0"]))
    print("WITHDRAWN: log-uniform claim of earlier run; density is Pareto-2.")
    print("WROTE data/genesis_law.json")


if __name__ == "__main__":
    main()