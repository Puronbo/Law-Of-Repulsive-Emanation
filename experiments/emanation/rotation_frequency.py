"""Rotation frequency vs turnover: the critical onset at X*(d).

From phase_boundary.py: the trust response J = [[-g(d), -g0*gdepth*X],
[reward, 0]] has det = C*X with C = g0*gdepth*reward (0.0078) and
    disc = g^2 - 4*C*X,   X*(d) = g(d)^2/(4*C).
The eigenpairs are complex (elliptic, rotation: theta in (90,180)) only when
disc<0, and the rotation frequency is
    omega = Im(lambda) = sqrt(-disc)/2 = sqrt(C*(X - X*)).
So the exchange rotation is an order-parameter onset: omega ~ sqrt(X - X*),
the mean-field critical exponent 1/2 in the distance above the minimum
viable turn.

Measured here: finite-difference J at fixed depth d=0.5 for several X past
the threshold, comparing the realized rotation frequency against the
analytic sqrt law.
"""

import json
import math
import os

from credit_commons.sim import Params, Commons

P = Params()
reward = P.reward()
g0, gdepth = P.g0, P.gdepth
C = reward * g0 * gdepth          # 0.0078 (det per unit X)
G_AT = g0 * (1 + gdepth * 0.5)    # 0.08 at depth 0.5
X_STAR = G_AT * G_AT / (4 * C)    # 0.205
CHI = 0.0
N = 0


def realized(depth, X, max_leverage=1.0, dstep=0.1):
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
    if disc < 0:
        omega = 0.5 * math.sqrt(-disc)
        theta = math.degrees(math.atan2(omega, T / 2.0))
    else:
        omega = 0.0
        theta = 180.0
    return {"R11": R11, "R12": R12, "R21": R21, "R22": R22,
            "det": det, "T": T, "disc": disc, "omega": omega, "theta": theta}


def main():
    global CHI, N
    rows = []
    for X in [0.22, 0.3, 0.5, 1.0, 2.0]:
        w_analytic = math.sqrt(max(0.0, C * (X - X_STAR)))
        r = realized(0.5, X)
        if r is None:
            continue
        zeta = math.sqrt(X_STAR / X)          # damping ratio = g/(2 sqrt(C X))
        Q = 1.0 / (2.0 * zeta)                # quality factor = 1/(2 zeta)
        rows.append({"X": X, "x_star": X_STAR, "drive": X - X_STAR,
                     "omega_analytic": w_analytic, "omega_realized": r["omega"],
                     "theta_deg": r["theta"], "disc": r["disc"],
                     "zeta": zeta, "Q": Q,
                     "cos_theta_sq": math.cos(math.radians(r["theta"])) ** 2,
                     "zeta_sq": zeta * zeta})
        if w_analytic > 0:
            N += 1
            CHI += (r["omega"] - w_analytic) ** 2

    out = {
        "seed": 42,
        "identity": "rotation of the trust exchange is a critical onset: "
                    "omega = sqrt(C*(X-X*)), mean-field exponent 1/2.  The "
                    "minimum viable turn X*(0.5)=g(0.5)^2/4C separates pure "
                    "decay (hyperbolic, omega=0) from rotation (elliptic, "
                    "omega>0).  MSE of the realized frequencies against the "
                    "sqrt law recorded as chi_sq/N.",
        "depth": 0.5, "g_at": G_AT, "C": C, "x_star": X_STAR,
        "law": "omega = sqrt(C*(X - X*))",
        "reduction": "J is a damped harmonic oscillator: stiffness C, "
                     "damping g(d).  Damping ratio zeta = g/(2*sqrt(C*X)) = "
                     "sqrt(X*/X) = |cos theta|; quality factor Q = "
                     "1/(2*zeta) = 1/(2*|cos theta|).  At X=X*: zeta=1, "
                     "critical damping, theta=180 deg, det=0, rank-1 mirror "
                     "(Ch.78) - no rotation, pure decay.",
        "rows": rows,
        "chi_sq_per_point": CHI / max(1, N),
    }
    path = os.path.join("experiments", "emanation", "data", "rotation_frequency.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("d=0.5, X* = %.4f, C = %.4f" % (X_STAR, C))
    for r in rows:
        print("X=%.2f drive=%+.3f  omega=%.4f  zeta=%.4f  Q=%.2f  "
              "theta=%.1f  cos^2=%.4f zeta^2=%.4f"
              % (r["X"], r["drive"], r["omega_realized"], r["zeta"], r["Q"],
                 r["theta_deg"], r["cos_theta_sq"], r["zeta_sq"]))
    print("chi_sq/pt = %.2e" % out["chi_sq_per_point"])
    print("WROTE data/rotation_frequency.json")


if __name__ == "__main__":
    main()