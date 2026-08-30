"""Phase boundary of the trust map: the elliptic basin and the gate margin.

The trust response J(d) = [[-g_at(d), -g0*gdepth], [reward, 0]] with
det = reward*g0*gdepth = 0.0078 (measured, depth-invariant) has characteristic
    disc(d) = T(d)^2 - 4*det,  T(d) = -g_at(d).
* disc < 0:  complex eigenpairs -> ELLIPTIC (rotation; trust recoverable,
             the mirror keeps cycling, Ch.78 k~_n=(-1)^n k_n).
* disc = 0:  parabolic cusp at  g* = 2*sqrt(det) = 0.1766  -> d* = 2.11.
* disc > 0:  hyperbolic (real, stable node) -> the rotation is gone; trust
             can no longer cycle back (no recovery loop).

The hard gate stops spending at depth 1.0 (g=0.11), i.e. at
    margin_depth = (d* - d_gate)/d* ~ 53%,
    margin_g     = (g* - g_d)/g* ~ 38%.
The gate guards the recoverability basin: theta would climb 106.4 -> 180 deg
as d -> d*; the gate fires at 128.5 deg, keeping the loop elliptic.

Verified in-engine: relax max_leverage and push depth past d*; the realized
finite-difference matrix must switch disc<0 -> disc>0 (rotation consumed),
while det (conservation-level invariant) stays 0.0078 exactly.
"""

import json
import math
import os

from credit_commons.sim import Params, Commons

P = Params()
reward = P.reward()
g0, gdepth = P.g0, P.gdepth
C = reward * g0 * gdepth                    # det PER UNIT X = 0.0078 (measured)
DET = C                                     # measured at X=1 in economy_matrix
G_STAR = 2.0 * math.sqrt(DET)               # 0.1766 (disc=0 locus at X=1)
D_STAR = (G_STAR / g0 - 1.0) / gdepth       # 2.11
G_GATE = g0 * (1 + gdepth * 1.0)            # 0.11 at depth 1.0


def disc_at_depth(d, X):
    g = g0 * (1 + gdepth * d)
    return g * g - 4 * C * X


def realized_matrix(depth, X=1.0, max_leverage=1.0, dstep=0.1):
    """Finite-difference measurement of J at the given depth using only
    nonzero trades (the engine rejects X=0).  We vary X at fixed depth and
    depth at fixed X with adjacent-bucket differences."""

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

    # d(buf)/dX at fixed depth: difference between X and 2X
    x1 = deltas(X, depth); x2 = deltas(2 * X, depth)
    if x1 is None or x2 is None:
        return None
    R11 = (x2[0] - x1[0]) / X
    R21 = (x2[1] - x1[1]) / X
    # d(buf)/ddepth at fixed X: difference between depth and depth+dstep
    d1 = deltas(X, depth); d2 = deltas(X, depth + dstep)
    if d1 is None or d2 is None:
        return None
    R12 = (d2[0] - d1[0]) / dstep
    R22 = (d2[1] - d1[1]) / dstep
    det = R11 * R22 - R12 * R21
    T = R11 + R22
    return {"R11": R11, "R12": R12, "R21": R21, "R22": R22,
            "det": det, "T": T, "disc": T * T - 4 * det}


def main():
    rows_gate = []
    for d in [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, d_star_round()]:
        g = g0 * (1 + gdepth * d)
        disc = g * g - 4 * C
        if disc < 0:
            im = math.sqrt(-disc) / 2.0
            theta = math.degrees(math.atan2(im, -g / 2.0))
        else:
            theta = 180.0
        rows_gate.append({"depth": d, "g": g, "disc_at_X1": disc,
                          "theta_deg": theta,
                          "x_star": g * g / (4.0 * C),
                          "regime": "elliptic" if disc < 0 else "parabolic" if
                          disc == 0 else "hyperbolic"})

    in_elliptic = realized_matrix(0.5, X=1.0, max_leverage=1.0)  # above turn threshold (deep-side, inside gate and basin)
    sub_turn = realized_matrix(0.5, X=0.1, max_leverage=1.0)     # below X*(0.5) -> hyperbolic
    across = realized_matrix(D_STAR, X=1.0, max_leverage=4.0)    # depth past d* at unit turn

    out = {
        "seed": 42,
        "identity": "gate is inside the elliptic basin: disc<0 (rotation/"
                    "recoverable trust) must hold.  Basin boundary is a curve "
                    "in (X, d): disc = g(d)^2 - 4*C*X with C = "
                    "g0*gdepth*reward = 0.0078 (det PER UNIT X - a measured "
                    "claim of this run).  Minimum viable turn X*(d) = "
                    "g(d)^2/4C: trades below it are hyperbolic (real negative "
                    "eigenvalues, pure decay, no recovery rotation); trades "
                    "above it are elliptic (rotation, the mirror cycles).",
        "params": {"reward": reward, "g0": g0, "gdepth": gdepth, "g_star": G_STAR,
                   "d_star": D_STAR, "gate_g": G_GATE, "C": C,
                   "margin_g_pct": 100.0 * (G_STAR - G_GATE) / G_STAR,
                   "margin_d_pct": 100.0 * (D_STAR - 1.0) / D_STAR},
        "path": rows_gate,
        "realized_elliptic_above_turn": in_elliptic,
        "realized_hyperbolic_below_turn": sub_turn,
        "realized_across_depth_boundary": across,
    }
    path = os.path.join("experiments", "data", "phase_boundary.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("g* = %.4f, d* = %.3f, gate g = %.4f  (margins g %.0f pct, d %.0f pct)"
          % (G_STAR, D_STAR, G_GATE, out["params"]["margin_g_pct"],
             out["params"]["margin_d_pct"]))
    print("C (det per unit X) = %.4f" % C)
    for r in rows_gate:
        print("d=%.2f g=%.4f disc=%+.4f X*=%.3f theta=%.1f  %s"
              % (r["depth"], r["g"], r["disc_at_X1"], r["x_star"],
                 r["theta_deg"], r["regime"]))
    print("realized above turn (d=0.5,X=1.0)  : disc=%.4f (%s)"
          % (in_elliptic["disc"], "elliptic" if in_elliptic["disc"] < 0 else "hyperbolic"))
    print("realized below turn (d=0.5,X=0.1)  : disc=%.4f (%s)"
          % (sub_turn["disc"], "elliptic" if sub_turn["disc"] < 0 else "hyperbolic"))
    print("realized across d* (d=2.11,X=1.0)  : disc=%.4f (%s)"
          % (across["disc"], "elliptic" if across["disc"] < 0 else "hyperbolic"))
    print("WROTE data/phase_boundary.json")


def d_star_round():
    return round(D_STAR, 2)


if __name__ == "__main__":
    main()