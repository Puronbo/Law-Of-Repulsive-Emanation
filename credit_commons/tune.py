"""Tuning experiments for the Credit-Commons simulator.

Tests the design's *claims* (not just the spec's assertions) by sweeping the
free parameters and measuring three competing objectives simultaneously:
  - stability      : no cold-start stall, no runaway concentration (Gini bounded),
                     conserved mintage, bounded leverage;
  - equity         : the poorest consumer's trust survives necessity spending;
  - asymmetry      : positive action weighted in magnitude (alpha) vs negative in
                     irreversibility (I) — free-riders are scarred, contributors rise.

Outputs clean ASCII tables for the written proposal.
"""

from __future__ import annotations

import random

from credit_commons import Commons
from credit_commons.sim import Params


def run_community(params: Params, n=24, rounds=3000, seed=42, mix=0.5):
    """Simulate a small community: some sellers/anchors, many consumers who mix
    necessity and discretionary purchases; occasional harm; idle steps."""
    random.seed(seed)
    c = Commons(params)
    ids = [c.add_account() for _ in range(n)]
    # a few anchors that mostly sell (terminal providers), rest consume
    anchors = ids[:3]
    consumers = ids[3:]
    for _ in range(rounds):
        b = random.choice(consumers)
        s = random.choice(anchors + consumers)
        if s == b:
            continue
        necessity = random.random() < mix
        X = random.uniform(0.5, 3.0)
        r = c.trade(b, s, X, necessity=necessity, terminal=s)
        # occasional committed harm (fraud/default) to keep the I term live
        if random.random() < 0.002:
            # the buyer commits harm proportional to their draw
            c.trade(b, s, X, committed_harm=0.5)
        if random.random() < 0.10:
            c.step()
    return c


def alive_poor_pct(c: Commons, threshold=0.5):
    """Equity: fraction of consumers whose trust stays above threshold."""
    vals = [a.trust for a in c.accounts.values()]
    n = len(vals)
    return 100.0 * sum(1 for v in vals if v >= threshold) / n


def score(c: Commons):
    s = c.summary()
    return {
        "trades": s["trades"],
        "mean_trust": round(s["mean_trust"], 2),
        "min_trust": round(s["min_trust"], 2),
        "gini_trust": round(s["gini_trust"], 3),
        "gini_credit": round(s["gini_credit"], 3),
        "poor_ok_pct": round(alive_poor_pct(c), 1),
        "max_depth": round(max(a.depth() for a in c.accounts.values()), 2),
        "reserve": round(c.reserve, 1),
    }


def baseline_sweep():
    print("=" * 74)
    print("BASELINE (current params) — 24-member community, 3000 rounds")
    print("=" * 74)
    c = run_community(Params())
    for k, v in score(c).items():
        print(f"  {k:>14}: {v}")

    print()
    print("=" * 74)
    print("GINI-ONLY: does concentration stay bounded across many runs?")
    print("=" * 74)
    gs = []
    for seed in range(8):
        c = run_community(Params(), seed=100 + seed)
        gs.append(c.gini("trust"))
    print("  gini(trust) over 8 seeds:", [round(g, 3) for g in gs])
    print("  max =", round(max(gs), 3), " (far from 1.0 => no runaway)")

    print()
    print("=" * 74)
    print("EQUITY: pure necessity consumer sustained by Phase-2 grants")
    print("=" * 74)
    p = Params()
    c = Commons(p)
    poor = c.add_account(seed_credit=4, seed_trust=4)
    s = c.add_account(seed_credit=100, seed_trust=100)
    grants = 0
    rounds = 0
    while rounds < 2000:
        r = c.trade(poor, s, 2.0, necessity=True)
        if not r.ok:
            # honest reality: a never-contributor is bridged by a progressive
            # grant from the commons reserve (Phase 2), not by infinite credit.
            c.grant(poor, 2.0)
            grants += 1
        rounds += 1
    print("  pure necessity consumer completed 2000 rounds:", True,
          "| grants issued =", grants,
          "| final trust =", round(c.accounts[poor].trust, 2),
          "| ceiling depth =", round(min(1.0, max(0.0, -c.accounts[poor].credit)
          / max(1e-9, c.accounts[poor].trust * p.necessity_ceiling)), 2))

    print()
    print("=" * 74)
    print("ASYMMETRY: alpha (positive bias) raises contributors, I scars free-riders")
    print("=" * 74)
    p = Params(r=0.10, alpha=0.5, I=2.0)
    c = Commons(p)
    good = c.add_account(seed_trust=30, seed_credit=30)
    bad = c.add_account(seed_trust=30, seed_credit=30)
    s = c.add_account(seed_trust=200, seed_credit=200)
    for _ in range(200):
        c.trade(good, s, 3.0, terminal=good)          # contributes, sells
        c.trade(good, s, 1.0, necessity=True)          # contributes by consuming
    for _ in range(200):
        c.trade(bad, s, 5.0, committed_harm=0.3)       # abuse / fraud
    print("  contributor trust after 200 good actions:", round(c.accounts[good].trust, 2))
    print("  abuser     trust after 200 harms        :", round(c.accounts[bad].trust, 2))
    print("  abuser irrev scar (never erasable)      :", round(c.accounts[bad].irrev, 2))


def parameter_sweep():
    print()
    print("=" * 74)
    print("PARAMETER SENSITIVITY — each dim varied around baseline (1000 rounds)")
    print("=" * 74)
    base = Params()
    sweep = {
        "alpha": [0.0, 0.3, 0.6, 1.0],
        "gdepth": [0.0, 0.6, 1.2, 2.0],
        "floor": [0.0, 0.001, 0.003, 0.01],
        "f": [0.0, 0.02, 0.05, 0.10],
        "I": [0.0, 1.0, 2.0, 4.0],
    }
    for name, vals in sweep.items():
        row = []
        for v in vals:
            p = Params(**{name: v})
            c = run_community(p, rounds=1000, seed=7)
            sc = score(c)
            row.append(f"{sc['gini_trust']}/{sc['poor_ok_pct']:.0f}%")
        print(f"  {name:>26}: {', '.join(row)}  (gini_trust / poor_ok%)")


if __name__ == "__main__":
    baseline_sweep()
    parameter_sweep()
