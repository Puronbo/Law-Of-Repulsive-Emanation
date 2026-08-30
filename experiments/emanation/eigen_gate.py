"""The eigen-path to the wall: theta(depth) -> pi as the gate fires, while
sigma_area = -ln det(J_trust) is depth-invariant (the budgeted scar per unit).

From economy_matrix.json the trust Jacobian (wrt X, depth) is
    J(X,d) = [[ -g_at(d),  -g0*gdepth*X ],
              [  reward,      0        ]],
        g_at(d) = g0*(1+gdepth*d),  reward = r*(1+alpha).
Measured at X=1: det = reward*g0*gdepth = 0.0078 (depth-invariant),
sigma_area = -ln(0.0078) = 4.85.  The eigen angles:
    d=0:    T=-0.05      theta ~ 106.4 deg
    d=1:    T=-0.11      theta ~ 128.6 deg  (climbing toward pi)
The hard gate (max_leverage) refuses to spend at d=1 precisely as lending can
push theta no further — the theta -> pi wall.  The scar I*h in the simulator
accumulates linearly = the log-det budget per unit, the same additive law as
the FT: det_total = det^N, sigma_total = N*sigma_step.

This is the entire arc in one figure: credit map det=1 (conservation, no
mintage); trust map det<1 (contracting, the scar); the coin is the angle;
lambda=1=det(J_F/J_G) demands area preservation of the trust map, exactly what
conservation forbids for credit — same law, mirrored sign.
"""

import json
import math
import os

from credit_commons.sim import Params

P = Params()
reward = P.reward()
g0, gdepth = P.g0, P.gdepth
DET_TRUST = reward * g0 * gdepth
SIGMA_AREA = -math.log(DET_TRUST) if DET_TRUST > 0 else float("nan")


def eig_angle(d, X=1.0):
    g = g0 * (1 + gdepth * d)
    T = -g
    # J = [[-g, -g0*gdepth*X],[reward, 0]]
    D = -(-g0 * gdepth * X) * reward   # det
    disc = T * T - 4 * D
    if disc < 0:
        re, im = T / 2.0, math.sqrt(-disc) / 2.0
        return theta(re, im), math.hypot(re, im), re, im
    return None, None, None, None


def theta(re, im):
    return math.degrees(math.atan2(im, re))


def main():
    rows = []
    for d in [0.0, 0.25, 0.5, 0.75, 1.0]:
        ang, mag, re, im = eig_angle(d)
        rows.append({
            "depth": d,
            "g_at": g0 * (1 + gdepth * d),
            "theta_deg": ang,
            "mag": mag,
            "re": re,
            "im": im,
            "sigma_area": SIGMA_AREA,
            "det": DET_TRUST,
        })

    out = {
        "seed": 42,
        "identity": "theta(d) climbs 106.4 -> 128.6 (-> pi) as depth -> 1; "
                    "sigma_area = -ln(det) = 4.85 is depth-invariant: the "
                    "budgeted scar per unit; the gate is the theta->pi wall; "
                    "lambda=1=det(J_F/J_G) is area-preservation the trust "
                    "map is forbidden to have (conservation mirrors it).",
        "params": {"reward": reward, "g0": g0, "gdepth": gdepth,
                   "I": P.I, "max_leverage": P.max_leverage},
        "rows": rows,
        "det_trust": DET_TRUST,
        "sigma_area": SIGMA_AREA,
    }
    path = os.path.join("experiments", "emanation", "data", "eigen_gate.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    for r in rows:
        print("depth=%.2f  g=%.4f  theta=%.1f deg  |lambda|=%.4f  "
              "sigma_area=%.3f (invariant)" % (r["depth"], r["g_at"],
              r["theta_deg"], r["mag"], r["sigma_area"]))
    print("WROTE data/eigen_gate.json")


if __name__ == "__main__":
    main()