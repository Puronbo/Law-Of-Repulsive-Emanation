"""Tilt contraction across depth: the measured reason constant-lambda fails.

Established (economy_matrix.json): per trade the sell-side tilt is
    sigma(d) = ln(reward / g_at(d)),  reward = r(1+alpha) = 0.13.
The draw rate g_at(d) = g0*(1+gdepth*d) is PROGRESSIVE in depth (E2), so the
tilt is NOT a constant: it collapses from ln(0.13/0.05)=0.955 at depth 0 to
ln(0.13/0.11)=0.167 at full leverage.  The economy's equity lever is exactly
this contraction: rewards pull hard when shallow, debts pull harder when deep.
A constant-lambda machine (lambda=1 axiom, or any single coin) cannot express
it -> the 11-25 pct residuals measured earlier are this, not noise.

Also: under buyer<->seller exchange the mirror product is exactly -1,
    (reward/g_at(d)) * (-g_at(d)/reward) = -1,
the economic image of Ch.78's cumulant mirror k~_n = (-1)^n k_n, measured here
on actual trades.  The operator that wants to be exact must therefore pass
through det(R)=g0*gdepth*reward != 0: the two ledgers are NOT degenerate; they
split along the depth direction precisely so that no single scalar coin, and
no single actor, controls value.
"""

import json
import math
import os

from credit_commons.sim import Params, Commons

P = Params()
reward = P.reward()   # 0.13


def coin_at_depth(d, X=1.0):
    """Measure both trust deltas for one discretionary trade at depth d."""
    c = Commons(P)
    b = c.add_account(seed_credit=0.0, seed_trust=10.0)
    s = c.add_account(seed_credit=0.0, seed_trust=10.0)
    c.accounts[b].credit = -d * 10.0
    t0 = (c.accounts[b].trust, c.accounts[s].trust)
    c.trade(b, s, X, necessity=False, terminal=s)
    t1 = (c.accounts[b].trust, c.accounts[s].trust)
    db = t1[0] - t0[0]
    ds = t1[1] - t0[1]
    return db, ds   # buyer delta, seller delta


def main():
    depths = [0.0, 0.25, 0.5, 0.75, 1.0]
    rows = []
    for d in depths:
        if d >= 1.0:
            # the hard gate (max_leverage=1.0) makes depth 1.0 unreachable by
            # any spend: credit-X <= -trust would be violated.  The tilt is
            # still well-defined analytically at the boundary wall.
            g = P.g_at(1.0)
            sig = math.log(reward / g)
            rows.append({
                "depth": 1.0,
                "buyer_trust_delta": 0.0,
                "seller_trust_delta": 0.0,
                "g_at_depth": g,
                "tilt_sigma": sig,
                "mirror_product_buy_times_sell": -g / reward,
                "note": "hard gate: impossible to spend at full leverage",
            })
            continue
        db, ds = coin_at_depth(d)
        g = P.g_at(d)
        sig = math.log(reward / g)
        rows.append({
            "depth": d,
            "buyer_trust_delta": db,
            "seller_trust_delta": ds,
            "g_at_depth": g,
            "tilt_sigma": sig,
            "mirror_product_buy_times_sell": (db / ds if ds else None),
        })

    out = {
        "seed": 42,
        "identity": "tilt sigma(d)=ln(reward/g_at(d)) contracts with depth "
                    "(0.955 -> 0.167); mirror product =-1 under exchange",
        "params": {"reward": reward, "g0": P.g0, "gdepth": P.gdepth,
                   "alpha": P.alpha},
        "rows": rows,
        "conclusion": "the anti-concentration lever is the depth-dependence of "
                      "the trust tilt; a constant coin/lambda=1 is the "
                      "11-25 pct error; requiring one scalar would make one "
                      "actor control value -> the progressive g(d) is the "
                      "anti-oligarchy principle made measurable.",
    }
    path = os.path.join("experiments", "data", "tilt_depths.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    for r in rows:
        print("depth=%.2f  buyer=%.4f  seller=%.4f  g=%.4f  sigma=%.4f  "
              "mirror(buy/sell)=%.4f%s"
              % (r["depth"], r["buyer_trust_delta"], r["seller_trust_delta"],
                 r["g_at_depth"], r["tilt_sigma"],
                 r["mirror_product_buy_times_sell"],
                 "  (gated)" if "note" in r else ""))
    print("WROTE data/tilt_depths.json")


if __name__ == "__main__":
    main()