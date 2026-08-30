"""Echo boundary of the trust oscillator: Q=1 at X = 4*X*(d).

The exchange J(d,X) is a damped discrete rotation with
    zeta = sqrt(X*(d)/X) = |cos theta|,   Q = 1/(2*zeta).
At zeta = 1/2 (i.e. Q = 1, X = 4*X*) the response crosses from
* underdamped regime (Q > 1): a unit shock over-shoots; the trust spring
  rings - the reinvestment echo (a sale provokes reply back past balance);
* overdamped regime  (Q < 1): monotone creep to the fixed point, no echo.
For unit turns (X = 1) the crossing depth solves g(d)^2/4C = 1/4, i.e.
g(d)^2 = C -> d_echo = (sqrt(C)/g0 - 1)/gdepth ~ 0.64.

Measured here: realized J at several depths for X=1, reporting zeta, Q,
per-full-cycle amplitude ratio |lambda|^(2*pi/theta), and the Q=1 crossing.
"""

import json
import math
import os

from credit_commons.sim import Params, Commons

P = Params()
reward = P.reward()
g0, gdepth = P.g0, P.gdepth
C = reward * g0 * gdepth                      # 0.0078 (det per unit X)
D_ECHO = (math.sqrt(C) / g0 - 1.0) / gdepth   # ~0.64 for X=1


def realized(depth, X=1.0, max_leverage=1.0, dstep=0.05):
    def deltas(Xv, D):
        c = Commons(P)
        c.p.max_leverage = max_leverage
        b = c.add_account(seed_credit=0.0, seed_trust=10.0)
        s = c.add_account(seed_credit=0.0, seed_trust=10.0)
        c.accounts[b].credit = -D * 10.0
        t0 = (c.accounts[b].trust, c.accounts[s].trust)
        r = c.trade(b, s, Xv, necessity=False, terminal=s)
        if not r.ok:
            return None
        t1 = (c.accounts[b].trust, c.accounts[s].trust)
        return (t1[0] - t0[0], t1[1] - t0[1])

    x1 = deltas(X, depth); x2 = deltas(2 * X, depth)
    if x1 is None or x2 is None:
        return None
    R11 = (x2[0] - x1[0]) / X
    R21 = (x2[1] - x1[1]) / X
    d1 = deltas(X, depth); d2 = deltas(X, depth + dstep)
    if d1 is None or d2 is None:
        return None
    R12 = (d2[0] - d1[0]) / dstep
    R22 = (d2[1] - d1[1]) / dstep
    det = R11 * R22 - R12 * R21
    T = R11 + R22
    disc = T * T - 4 * det
    w = 0.5 * math.sqrt(-disc) if disc < 0 else 0.0
    theta = math.degrees(math.atan2(w, T / 2.0)) if disc < 0 else 180.0
    lam = math.sqrt(max(0.0, det))
    per_step_angle = math.radians(theta) if disc < 0 else math.pi
    full_cycles_steps = 2 * math.pi / max(1e-9, per_step_angle)
    per_cycle = lam ** full_cycles_steps if lam > 0 else 0.0
    return {"R11": R11, "R12": R12, "R21": R21, "R22": R22,
            "det": det, "T": T, "disc": disc, "omega": w, "theta_deg": theta,
            "lam": lam, "per_cycle_ratio": per_cycle}


def main():
    rows = []
    for d in [0.0, 0.3, 0.5, d_echo_round(), 0.8, 0.9, 1.0]:
        g = g0 * (1 + gdepth * d)
        x_star = g * g / (4.0 * C)
        zeta = math.sqrt(x_star / 1.0)        # X = 1
        Q = 1.0 / (2.0 * zeta)
        r = realized(d, X=1.0)
        if r is None:
            continue
        rows.append({"depth": d, "g": g, "x_star": x_star, "zeta": zeta,
                     "Q": Q, "regime": "echo (underdamped)" if Q > 1
                     else "creep (overdamped)",
                     "theta_deg": r["theta_deg"], "omega": r["omega"],
                     "per_cycle_ratio": r["per_cycle_ratio"]})

    out = {
        "seed": 42,
        "identity": "trust exchange at unit turn crosses Q=1 (zeta=1/2) at "
                    "d_echo ~ 0.64: shallower depths are underdamped - a "
                    "sale provokes a reply past balance (reinvestment echo); "
                    "deeper depths are overdamped - monotone creep to the "
                    "mirror, no echo.  Q = 1/(2*zeta), zeta = sqrt(X*/X).",
        "d_echo_for_X1": D_ECHO, "C": C, "X": 1.0,
        "rows": rows,
    }
    path = os.path.join("experiments", "data", "echo_boundary.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("X=1: Q=1 crossing at d_echo = %.3f  (g^2 = C)" % D_ECHO)
    for r in rows:
        print("d=%.2f g=%.4f X*=%.4f zeta=%.4f Q=%.2f theta=%.1f "
              "per_cycle=%.2e  %s"
              % (r["depth"], r["g"], r["x_star"], r["zeta"], r["Q"],
                 r["theta_deg"], r["per_cycle_ratio"], r["regime"]))
    print("WROTE data/echo_boundary.json")


def d_echo_round():
    return round(D_ECHO, 2)


if __name__ == "__main__":
    main()