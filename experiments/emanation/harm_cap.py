"""Harm-cap law: escape fraction is a ratio-law, and the g-axis has four
markers that harm steps across.

harm_as_depth.json measured 83.6% of harm trades past the elliptic cusp.
Theory: a fresh borrower (depth~0) escapes when d_eff>d*, i.e.
    (I*h/X)/(g0*gdepth) > d*
    h/X > g0*gdepth*d*/I  =: theta_star = 0.0633     <-- the true threshold
With h~U(0.02,0.2) and X~U(0.05,1.5) the predicted escape fraction is
computed by Monte Carlo (seed 42) and compared against the measured 0.8361.

CORRECTION (ledger audit): alpha_cusp = (g* - g0)/(I*g0*gdepth) = 1.0553 is
a DIMENSIONLESS coordinate of the g-axis ladder at the phase cusp g*
(= d*/I analytically), NOT an h/X threshold.  The h/X escape threshold is
theta_star = g0*gdepth*d*/I = 0.0633 = g0*gdepth*alpha_cusp.  Earlier
entries recorded "escape iff h/X > 1.0553", which is FALSE: the MC escape
rule below was and is correct (I*h/X > g0*gdepth*d*); only the name/label
was wrong.

Markers on the same g-axis (the engine's own scale constants):
    g0            base draw          - honest shallow floor
    g_gate=g_at(1) gate ceiling      - honest sigma floor (sigma>0)
    reward        contribution reward - sigma=0: turn neither pumps nor drains
    g*=2*sqrt(C)  phase cusp         - rotation dies (hyperbolic band)
alpha(g) = (g-g0)/(I*g0*gdepth) is the dimensionless ladder coordinate.
Harm moves g_eff = g + I*h/X across this ladder; crossing reward flips the
FT to negative action, crossing g* destroys the rotation.
"""

import json
import math
import os
import random

from credit_commons.sim import Params

random.seed(42)
P = Params()
C = P.g0 * P.gdepth * P.reward()             # 0.0078 (det per unit X)
G_STAR = 2.0 * math.sqrt(C)                  # 0.1766
D_STAR = (G_STAR / P.g0 - 1.0) / P.gdepth    # 2.11
REWARD = P.reward()                          # 0.13
G_D0 = P.g0
G_GATE = P.g_at(1.0)                         # 0.11
D_SIGMA0 = (REWARD / P.g0 - 1.0) / P.gdepth  # depth where g_at = reward

HARM_LO, HARM_HI = 0.02, 0.20
X_LO, X_HI = 0.05, 1.5
MC = 400000

# corrections: alpha_cusp is the g-ladder coordinate at g* (d*/I);
# theta_star is the h/X escape threshold (g0*gdepth*d*/I = 0.0633).
ALPHA_CUSP = (G_STAR - G_D0) / (P.I * P.g0 * P.gdepth)
THETA_STAR = P.g0 * P.gdepth * D_STAR / P.I


def main():
    n_esc = 0
    for _ in range(MC):
        h = random.uniform(HARM_LO, HARM_HI)
        x = random.uniform(X_LO, X_HI)
        if (P.I * h / x) / (P.g0 * P.gdepth) > D_STAR:
            n_esc += 1
    mc_esc = n_esc / MC

    def alpha_l(g):
        return (g - G_D0) / (P.I * P.g0 * P.gdepth)

    markers = [
        {"name": "g0 base draw", "g": G_D0,
         "sigma": math.log(REWARD / G_D0),
         "alpha_ladder": 0.0,
         "note": "honest shallow floor"},
        {"name": "g_gate g_at(1)", "g": G_GATE,
         "sigma": math.log(REWARD / G_GATE),
         "alpha_ladder": alpha_l(G_GATE),
         "note": "honest sigma floor 0.168"},
        {"name": "reward sigma=0", "g": REWARD, "sigma": 0.0,
         "alpha_ladder": alpha_l(REWARD),
         "note": "turn neither pumps nor drains; FT flips below"},
        {"name": "g* cusp", "g": G_STAR,
         "sigma": math.log(REWARD / G_STAR),
         "alpha_ladder": ALPHA_CUSP,
         "note": "disc=0: rotation dies, hyperbolic band"},
    ]
    out = {
        "seed": 42,
        "identity": "harm-cap law: fresh-borrower escape iff I*h/X > "
                    "g0*gdepth*d* (=0.1266) i.e. h/X > theta_star = %.5f.  "
                    "alpha_cusp=%.5f is the g-ladder dimensionless "
                    "coordinate of g* (=d*/I), NOT the h/X threshold; "
                    "theta_star = g0*gdepth*alpha_cusp.  MC prediction vs "
                    "the 0.8361 measured in harm_as_depth."
                    % (THETA_STAR, ALPHA_CUSP),
        "alpha_cusp_g_star_marker": ALPHA_CUSP,
        "escape_threshold_h_over_X": THETA_STAR,
        "d_star": D_STAR, "d_sigma0": D_SIGMA0, "I": P.I,
        "mc_escape_fraction": mc_esc,
        "measured_escape_fraction": 0.8361,
        "frac_residual": mc_esc - 0.8361,
        "markers": [{"name": m["name"], "g": m["g"], "sigma": m["sigma"],
                     "alpha_ladder_coordinate": m["alpha_ladder"],
                     "note": m["note"]}
                    for m in markers],
    }
    path = os.path.join("experiments", "emanation", "data", "harm_cap.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("escape threshold in h/X units = %.5f  (alpha_cusp marker at g* = "
          "%.5f is d*/I, NOT the threshold)" % (THETA_STAR, ALPHA_CUSP))
    print("MC escape fraction (fresh-borrower rule) = %.4f" % mc_esc)
    print("measured (harm_as_depth 8000 trades)     = 0.8361")
    print("residual = %+.4f" % (mc_esc - 0.8361))
    print()
    print("%-20s g=%.4f  sigma=%+.4f  alpha_ladder=%.4f  (%s)"
          % ("g0 base draw", G_D0, math.log(REWARD / G_D0), 0.0,
             "honest shallow floor"))
    print("%-20s g=%.4f  sigma=%+.4f  alpha_ladder=%.4f  (%s)"
          % ("g_gate g_at(1)", G_GATE, math.log(REWARD / G_GATE),
             alpha_l(G_GATE), "honest sigma floor 0.168"))
    print("%-20s g=%.4f  sigma=%+.4f  alpha_ladder=%.4f  (%s)"
          % ("reward sigma=0", REWARD, 0.0,
             alpha_l(REWARD), "FT flips below"))
    print("%-20s g=%.4f  sigma=%+.4f  alpha_ladder=%.4f  (%s)"
          % ("g* cusp", G_STAR, math.log(REWARD / G_STAR), ALPHA_CUSP,
             "rotation dies, hyperbolic"))
    print("WROTE data/harm_cap.json")


if __name__ == "__main__":
    main()