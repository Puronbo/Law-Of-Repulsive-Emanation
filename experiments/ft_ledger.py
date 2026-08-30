"""Live fluctuation theorem in the Credit-Commons ledger.

The engine's trust flow per discretionary trade is
    buyer  -g_at(depth)*X   (draw)
    seller +reward()*X      (gain),   ratio reward/g_at(depth).
Fluctuation theorem (Evans-Searles 1994, Crooks 1999): over a long ledger
    P(total gain)/P(total loss) ~ e^{sigma_total},
where the per-trade action is  sigma_k = ln( reward / g_at(depth_k) ).
This is the temporal twin of the response-matrix invariants (det=0.0078,
tilt_depths sigma=0.9555 at depth 0): the exchange does not mint; it
fluctuates with a fixed log-ratio per unit of turnover.

Measured: a long random ledger (both directions, mixed necessity), the
aggregate positive vs negative community-trust changes, the empirically
accumulated action, and the ratio against the predicted exponential.
"""

import json
import math
import os
import random

from credit_commons.sim import Params, Commons

random.seed(42)

P = Params()
reward = P.reward()          # 0.13
N_TRADES = 20000


def main():
    c = Commons(P)
    a = c.add_account(seed_credit=0.0, seed_trust=10.0)
    bb = c.add_account(seed_credit=0.0, seed_trust=10.0)

    s_pos = 0.0          # sum of gains (community trust up)
    s_neg = 0.0          # sum of losses (community trust down)
    n_pos = 0
    n_neg = 0
    sum_action = 0.0     # sum ln(reward/g_at(depth))
    draw_total = 0.0     # total buyer-side draw (sum g(depth)*X)
    gain_total = 0.0     # total seller-side gain (sum reward*X)
    n_ok = 0
    denied = 0

    for _ in range(N_TRADES):
        buyer, seller = (a, bb) if random.random() < 0.5 else (bb, a)
        X = round(random.uniform(0.05, 1.5), 2)
        necessity = random.random() < 0.05
        t0 = c.accounts[buyer].trust + c.accounts[seller].trust
        r = c.trade(buyer, seller, X, necessity=necessity, terminal=seller)
        if not r.ok:
            denied += 1
            continue
        t1 = c.accounts[buyer].trust + c.accounts[seller].trust
        d_trust = t1 - t0
        if necessity:
            continue  # E1 rebuild is the pump; FT applies to the draw side
        depth = c.accounts[buyer].depth()
        g = P.g_at(depth)
        sigma_k = math.log(reward / max(1e-9, g))
        sum_action += sigma_k
        draw_total += g * X
        gain_total += reward * X
        if d_trust >= 0:
            n_pos += 1
            s_pos += d_trust
        else:
            n_neg += 1
            s_neg -= d_trust
        n_ok += 1

    ratio = s_pos / max(1e-12, s_neg)
    ln_ratio = math.log(ratio) if ratio > 0 else None
    # mirror statistics across the two sides of every trade (Ch.78 k_n mirror):
    ln_gain_draw = math.log(gain_total / max(1e-12, draw_total))
    out = {
        "seed": 42,
        "identity": "live FT in log form: ln(sum_gains/sum_losses) = "
                    "sum ln(reward/g_at(depth)) along the ledger",
        "n_trades": N_TRADES, "n_ok": n_ok, "denied": denied,
        "reward": reward,
        "sum_action": sum_action,
        "sum_gains": s_pos, "sum_losses": s_neg,
        "gain_loss_ratio": ratio,
        "ln_gain_loss_ratio": ln_ratio,
        "action": sum_action,
        "residual": (ln_ratio - sum_action) if ln_ratio is not None else None,
        "draw_total": draw_total, "gain_total": gain_total,
        "mirror_ln_gain_over_draw": ln_gain_draw,
        "mean_action_per_trade": sum_action / max(1, n_ok),
        "n_pos": n_pos, "n_neg": n_neg,
    }
    path = os.path.join("experiments", "data", "ft_ledger.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("trades ok=%d denied=%d" % (n_ok, denied))
    print("sum ln(reward/g) = %.4f  (action sum-sigma)" % sum_action)
    print("sum gains=%.6f  sum losses=%.6f  ln(ratio)=%.4f"
          % (s_pos, s_neg, ln_ratio))
    print("residual = ln(ratio) - sum-sigma = %.6f" % (ln_ratio - sum_action))
    print("mirror: total gain=%.4f  total draw=%.4f  ln(gain/draw)=%.4f"
          % (gain_total, draw_total, ln_gain_draw))
    print("mean action/trade = %.6f   (tilt_depths sigma0 = 0.9555)"
          % out["mean_action_per_trade"])
    print("WROTE data/ft_ledger.json")


if __name__ == "__main__":
    main()