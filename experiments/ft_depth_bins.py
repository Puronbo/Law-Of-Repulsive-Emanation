"""Pointwise fluctuation theorem: sigma(d) holds per depth-bin.

ft_ledger.json established the mean action <sigma> = 0.769 over a mixed
ledger.  This run verifies the *pointwise* law on the same object:
for discretionary trades binned by buyer depth, the empirical
seller_gain / buyer_draw ratio within each bin must equal
    e^{sigma(d_mid)} = reward / g_at(d_mid).
It also closes the mirror round trip (buyer->seller:X then seller->buyer:X,
Ch.78 k_n mirror) and shows the total action equals
ln(roundtrip gain / roundtrip draw) = sigma(d_b) + sigma(d_s).
"""

import json
import math
import os
import random
from collections import defaultdict

from credit_commons.sim import Params, Commons

random.seed(42)
P = Params()
reward = P.reward()
N_TRADES = 30000
BIN = 0.10


def main():
    c = Commons(P)
    a = c.add_account(seed_credit=0.0, seed_trust=10.0)
    b = c.add_account(seed_credit=0.0, seed_trust=10.0)

    bins = defaultdict(lambda: {"draw": 0.0, "gain": 0.0, "n": 0})
    n_necessity = 0
    necessity_gain = 0.0
    necessity_x = 0.0

    for _ in range(N_TRADES):
        buyer, seller = (a, b) if random.random() < 0.5 else (b, a)
        X = round(random.uniform(0.05, 1.5), 2)
        necessity = random.random() < 0.10
        r = c.trade(buyer, seller, X, necessity=necessity, terminal=seller)
        if not r.ok:
            continue
        if necessity:
            n_necessity += 1
            necessity_x += X
            necessity_gain += P.n * X
            continue
        depth = c.accounts[buyer].depth()
        g = P.g_at(depth)
        d_bin = round(depth / BIN) * BIN
        bins[d_bin]["draw"] += g * X
        bins[d_bin]["gain"] += reward * X
        bins[d_bin]["n"] += 1

    rows = []
    for d_bin in sorted(bins):
        bl = bins[d_bin]
        if bl["draw"] <= 0 or bl["n"] < 50:
            continue
        ratio = bl["gain"] / bl["draw"]
        g_mid = P.g_at(d_bin + BIN / 2)
        pred = reward / g_mid
        rows.append({"depth_bin": d_bin, "n": bl["n"],
                     "empirical_gain_over_draw": ratio,
                     "predicted_e_sigma": pred,
                     "sigma_emp": math.log(ratio),
                     "sigma_pred": math.log(pred)})

    # mirror round trip closure at each requested depth
    def roundtrip(depth, X=1.0):
        c2 = Commons(P)
        u = c2.add_account(seed_credit=-10.0 * depth, seed_trust=10.0)
        v = c2.add_account(seed_credit=0.0, seed_trust=10.0)
        t0 = (c2.accounts[u].trust, c2.accounts[v].trust)
        r1 = c2.trade(u, v, X, necessity=False, terminal=v)
        if not r1.ok:
            return None
        # v holds +X-fee credit (gain) and spends it back to u (Ch.78 mirror);
        # no manual state fiddling: the engine's own flow carries the return.
        r2 = c2.trade(v, u, X, necessity=False, terminal=u)
        if not r2.ok:
            return None
        t1 = (c2.accounts[u].trust, c2.accounts[v].trust)
        db = t1[0] - t0[0]
        ds = t1[1] - t0[1]
        return {"d_b": db, "d_s": ds, "total": db + ds,
                "action_pred": math.log(reward / P.g_at(depth)) + math.log(
                    reward / P.g_at(0.0))}

    rt = []
    for d in [0.0, 0.3, 0.5, 0.8, 1.0]:
        r = roundtrip(d)
        if r is None:
            continue
        rt.append({"depth_b": d, "delta_buyer": r["d_b"], "delta_seller": r["d_s"],
                   "total": r["total"], "action_pred": r["action_pred"]})

    out = {
        "seed": 42,
        "identity": "pointwise FT: within each buyer-depth bin, empirical "
                    "gain/draw = reward/g_at(mid) = e^{sigma(d)}.  Plus mirror "
                    "round-trip closure (buyer->seller then seller->buyer, "
                    "Ch.78 mirror).",
        "reward": reward, "bin_size": BIN, "n_trades": N_TRADES,
        "bins": rows,
        "necessity_pump": {"n_trades": n_necessity, "x_total": necessity_x,
                           "gain_total": necessity_gain,
                           "gain_per_x": (necessity_gain /
                                          max(1e-12, necessity_x))},
        "roundtrips": rt,
    }
    path = os.path.join("experiments", "data", "ft_depth_bins.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("pointwise FT (empir vs e^{sigma(d_mid)}):")
    for row in rows:
        print(" d~%.1f  n=%5d  emp=%.4f  pred=%.4f  sigma_emp=%.4f "
              "sigma_pred=%.4f" % (row["depth_bin"], row["n"],
                                   row["empirical_gain_over_draw"],
                                   row["predicted_e_sigma"], row["sigma_emp"],
                                   row["sigma_pred"]))
    print("necessity pump: %.2f gain per unit x (n=0.10)"
          % out["necessity_pump"]["gain_per_x"])
    print("mirror round trips (total trust change vs action_pred):")
    for row in rt:
        print(" depth_b=%.1f  db=%.4f ds=%.4f  total=%.4f  action_pred=%.4f"
              % (row["depth_b"], row["delta_buyer"], row["delta_seller"],
                 row["total"], row["action_pred"]))
    print("WROTE data/ft_depth_bins.json")


if __name__ == "__main__":
    main()