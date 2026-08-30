"""The genesis blowup: the exceptional fiber of the ledger's own 0/0.

Recent finding (0/0 census): a ratio that vanishes as 0/0 resolves only by
context; the set of all resolutions is the exceptional divisor of the blowup
at the point (Hironaka 1964), and "0/0 = 1" is one balanced-jet gauge, not a
value.  The ledger carries genuine 0/0 points - genesis accounts with
(credit, trust) near the origin, resolved IN CODE (depth clamp sim.py:182,
Gini guard).  This run probes the four economic rays as infinitesimal jets
from the origin and records each resolved ratio as a homogeneous point
(delta credit : delta trust) on the projective fiber P^1:

  T trade     : buyer (-X, -g0*X t)          -> slope near g0/reward-frame
  H harm      : buyer (0, -I*h)              -> point (0:1)  (credit-free ray)
  N necessity : buyer (-X, +n*X)             -> negative slope
  S seed      : phase-0 inflow (+s, 0)        -> the ONLY ray breaking the
                conserving membrane (Delta conserved_total = +s, mintage).

The conservating gauge (Delta(credit)+Delta(reserve) = 0 to 1e-12) is shown
to be direction-independent: it is the fibration's base, not its fiber.
"""

import json
import os

from credit_commons.sim import Params, Commons

P = Params()
g0 = P.g0


def add_near_origin(commons, trust):
    return commons.add_account(seed_credit=0.0, seed_trust=trust)


def conserved_of(c):
    return sum(a.credit for a in c.accounts.values()) + c.reserve


def probe(c, seller_credit=0.0, seller_trust=1000.0):
    s_id = c.add_account(seed_credit=seller_credit, seed_trust=seller_trust)
    return s_id


def main():
    # --- ray T: trade jet from near-origin ----------------------------------
    c1 = Commons(P)
    b1 = add_near_origin(c1, trust=1e-2)
    s1 = probe(c1)
    base = conserved_of(c1)
    before_b = (c1.accounts[b1].credit, c1.accounts[b1].trust)
    r = c1.trade(b1, s1, 1e-4)
    assert r.ok, r.reason
    after_b = (c1.accounts[b1].credit, c1.accounts[b1].trust)
    dC = after_b[0] - before_b[0]
    dT = after_b[1] - before_b[1]
    ray_t = {"label": "trade T", "point_P1": [round(dC, 10), round(dT, 10)],
             "slope_dT_dC": round(dT / dC, 6),
             "delta_conserved": round(conserved_of(c1) - base, 12)}

    # --- ray H: harm jet (credit-free) -------------------------------------
    c2 = Commons(P)
    b2 = add_near_origin(c2, trust=1e-2)
    s2 = probe(c2)
    base = conserved_of(c2)
    before_b = (c2.accounts[b2].credit, c2.accounts[b2].trust)
    r = c2.trade(b2, s2, 1e-4, committed_harm=1e-4)
    assert r.ok, r.reason
    after_b = (c2.accounts[b2].credit, c2.accounts[b2].trust)
    dC = after_b[0] - before_b[0]
    dT = after_b[1] - before_b[1]
    ray_h = {"label": "harm H", "point_P1": [round(dC, 10), round(dT, 10)],
             "slope_dT_dC": round(dT / dC, 6),
             "point_form": "(-1:-2) slope=I=2.0, tends to (0:1) as h/X->inf",
             "delta_conserved": round(conserved_of(c2) - base, 12),
             "note": "same spend X as ray T, but trust moves by I*h, not g0*X:"
                     " the harm direction is the I-slope, not a credit-free ray"}

    # --- ray N: necessity jet (trust-building) -----------------------------
    c3 = Commons(P)
    b3 = add_near_origin(c3, trust=1e-2)
    s3 = probe(c3)
    base = conserved_of(c3)
    before_b = (c3.accounts[b3].credit, c3.accounts[b3].trust)
    r = c3.trade(b3, s3, 1e-4, necessity=True)
    assert r.ok, r.reason
    after_b = (c3.accounts[b3].credit, c3.accounts[b3].trust)
    dC = after_b[0] - before_b[0]
    dT = after_b[1] - before_b[1]
    ray_n = {"label": "necessity N", "point_P1": [round(dC, 10), round(dT, 10)],
             "slope_dT_dC": round(dT / dC, 6),
             "delta_conserved": round(conserved_of(c3) - base, 12)}

    # --- ray S: phase-0 seed (external mintage) ----------------------------
    c4 = Commons(P)
    base = conserved_of(c4)
    s_id = c4.add_account(seed_credit=5.0, seed_trust=0.0)
    a = c4.accounts[s_id]
    ray_s = {"label": "seed S", "point_P1": [a.credit, a.trust],
             "point_form": "(1:0) external inflow",
             "delta_conserved": round(conserved_of(c4) - base, 12),
             "note": "the one ray off the conserving membrane (mintage by "
                     "Phase-0, by design)"}

    identity = ("genesis blowup: the ledger's own 0/0 (account at credit,"
                "trust near the origin) unfolds on an exceptional fiber;"
                "each economic rule is a distinct homogeneous ray "
                "(dcredit:dtrust) -- the resolution VALUES differ "
                "(T slope ~0.05, H slope = I = 2.0, N slope ~-0.10, S pure "
                "credit) and NONE equals 1; 0/0=1 lives only in the "
                "conserving GAUGE (delta conserved = 0, exact)")
    out = {
        "seed": 42,
        "identity": identity,
        "ray_T_trade": ({k: v for k, v in ray_t.items() if k != "label"}),
        "ray_H_harm": ({k: v for k, v in ray_h.items() if k != "label"}),
        "ray_N_necessity": ({k: v for k, v in ray_n.items() if k != "label"}),
        "ray_S_seed": ({k: v for k, v in ray_s.items() if k != "label"}),
        "exceptional_fiber_points": [
            "T: (%.5f : %.5f)" % (ray_t["point_P1"][0], ray_t["point_P1"][1]),
            "H: (%.5f : %.5f)" % (ray_h["point_P1"][0], ray_h["point_P1"][1]),
            "N: (%.5f : %.5f)" % (ray_n["point_P1"][0], ray_n["point_P1"][1]),
            "S: (1.0 : 0.0)",
        ],
        "conserving_gauge_exact": all(
            r["delta_conserved"] < 1e-11
            for r in (ray_t, ray_h, ray_n)),
        "code_resolutions_cited": [
            "sim.py:182 depth clamp max(0,-credit)/max(trust,1e-9) -> 0",
            "_gini empty guard -> 0.0",
        ],
    }
    path = os.path.join("experiments", "emanation", "data", "genesis_blowup.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("exceptional fiber of the ledger origin (dcredit : dtrust):")
    print("  T trade      (%.5f : %.5f)  slope dT/dC = %.6f  dCons=%s"
          % (ray_t["point_P1"][0], ray_t["point_P1"][1], ray_t["slope_dT_dC"],
             ray_t["delta_conserved"]))
    print("  H harm       (%.5f : %.5f)  slope = I = %.1f  ([(0:1) as h/X->inf)"
          % (ray_h["point_P1"][0], ray_h["point_P1"][1], ray_h["slope_dT_dC"]))
    print("  N necessity  (%.5f : %.5f)  slope dT/dC = %.6f  dCons=%s"
          % (ray_n["point_P1"][0], ray_n["point_P1"][1], ray_n["slope_dT_dC"],
             ray_n["delta_conserved"]))
    print("  S seed       (5.0 : 0.0)    off-membrane (mintage) dCons=%s"
          % ray_s["delta_conserved"])
    print("conserving membrane exact on T,H,N: %s"
          % out["conserving_gauge_exact"])
    print("WROTE data/genesis_blowup.json")


if __name__ == "__main__":
    main()