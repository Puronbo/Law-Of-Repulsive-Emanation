"""The denial rate as a first-passage law.

genesis_overshoot found the g0 mechanism is a denial-RATE flood: doubling
g0 (0.05->0.10) raised denials ~6.5x (1668 -> 10818) at quasi-stable
~0.8 depth.  That rate is an uncharacterized law and the connection to
classical first-passage/hitting time is the natural-philosopher move to
make while the rig is warm.  This run sweeps the mechanistic knobs and
reads the steady-state DENIAL RATE (denials per draw-attempt), testing
for a closed-form power law in the per-trade net drift.

Per-trade net drift toward the gate (gross): each accepted draw X moves
-gross credit toward the gate by X (credit -X) and moves the gate
+trust*L up by g(d)*X*L (trust -g(d)X, times L), so the NET approach rate
per unit X is (1 - g(d)*L) in gate units; regeneration +floor*L per step
pulls away by floor*L.  Hence a candidate rate law:

    rate_denial ~  (draw_drive)^(theta) * (floor_resist)^{-phi}

with the drift balance most parsimoniously (1 - g(d)*L) vs floor*L.
Measure rate vs g0 (={0.025,0.05,0.10,0.20}) and vs floor (={0,0.001,
0.01,0.1}) and fit a power in (1-g(d)L) and in floor*L.  If the rate
obeys a clean power the refusal/flood arc closes as a first-passage
statistics of the toy; if not, the honest claim is the rate is walk-path
specific and the arc's invariant is only the identity/excess/echo laws.

No Millennium claim.
"""

import json
import math
import os
import random

from credit_commons.sim import Params, Commons

SEED = 7
N_ACCOUNTS = 40
STEPS = 2500


def denial_rate(g0, floor, seed=SEED, distress_frac=1.0 / 3.0):
    random.seed(seed)
    P = Params(g0=g0, floor=floor, grant_bias=0.5)
    c = Commons(P)
    ids = [c.add_account(seed_credit=0.0,
                         seed_trust=random.uniform(20, 200)) for _ in
           range(N_ACCOUNTS)]
    split = N_ACCOUNTS // 3
    distress = set(ids[:split])
    nec_stress = set(ids[split:2 * split])
    denials = 0
    attempts = 0
    for s in range(STEPS):
        c.step()
        for i in range(N_ACCOUNTS):
            a = ids[i]
            b = c.accounts[a]
            if b.trust <= 0:
                continue
            if a in distress:
                X = random.uniform(0.5, 2.0)
                r = c.trade(a, ids[(i + 1) % N_ACCOUNTS], X,
                            necessity=False)
            elif a in nec_stress:
                X = random.uniform(0.9, 3.0)
                r = c.trade(a, ids[(i + 1) % N_ACCOUNTS], X,
                            necessity=True)
            else:
                X = random.uniform(0.5, 1.5)
                r = c.trade(a, ids[(i + 1) % N_ACCOUNTS], X,
                            necessity=(random.random() < 0.4))
            attempts += 1
            if not r.ok:
                denials += 1
    return denials, attempts


def main():
    g0_rows = []
    g0_base = Params().g0
    for g0 in (0.025, 0.05, 0.10, 0.20):
        d, a = denial_rate(g0, 0.001)
        rate = d / max(1, a)
        gd_at_pw = Params().g0 * (1 + Params().gdepth)  # depth~1 proxy
        g0_rows.append({
            "g0": g0, "denials": d, "attempts": a,
            "rate": round(rate, 5),
            "g0_over_base": round(g0 / g0_base, 2),
            "rate_ratio_vs_base": round(rate / (denial_rate(g0_base,
                                                             0.001)[0] /
                                                max(1, denial_rate(g0_base,
                                                                    0.001)[1])),
                                        3),
        })

    floor_rows = []
    for fl in (0.0, 0.001, 0.01, 0.1):
        d, a = denial_rate(0.05, fl)
        floor_rows.append({"floor": fl, "denials": d, "attempts": a,
                           "rate": round(d / max(1, a), 5)})

    out = {
        "identity": "DENIAL RATE AS FIRST-PASSAGE LAW - CORRECTED: the "
                    "denial rate is NOT a stationary single number.  "
                    "Per-window (500-step) rate at LOW g0 ramps "
                    "monotonically without settling across 3000 steps "
                    "(g0=0.06: 0.0046,0.0176,0.0225,0.0286,0.0302,0.0407 "
                    "- a slow penetration, not burn-in); at HIGH g0 it "
                    "saturates to a plateau after an initial transient "
                    "(g0=0.15: 0.018,0.169,0.176,0.122,0.128,0.137 ~0.13). "
                    "Forced power laws (g0-doubling) are HORIZON DEPENDENT "
                    "and are not claimed.",
        "g0_sweep_rate": g0_rows,
        "floor_sweep_rate": floor_rows,
        "time_structure": {
            "window_steps": 500,
            "low_g0_006_windows": [0.0046, 0.0176, 0.0225, 0.0286,
                                   0.0302, 0.0407],
            "low_g0_read": "monotonic ramp, never settles - slow "
                           "first-passage penetration, not burn-in",
            "high_g0_015_windows": [0.0180, 0.1687, 0.1756, 0.1216,
                                    0.1280, 0.1373],
            "high_g0_read": "initial transient then plateau ~0.13 - a "
                            "held rate at strong drawdown",
            "no_single_steady_state_at_low_g0": True,
        },
        "conclusion": ("the denial/flood rate has NO single steady state "
                       "at marginal drawdown: it ramps with observation "
                       "time (slow penetration).  At strong drawdown it "
                       "plateaus.  The '6.5x per g0 doubling, power 2.7' "
                       "number from the coarse sweep is a HORIZON ARTIFACT "
                       "and is WITHDRAWN; only the identity/excess/echo "
                       "laws and the depth~0.8 quasi-stable gate are "
                       "claimed as invariant."),
        "references_note": "flood observation genesis_overshoot "
                           "(1668->10818, now shown horizon-dependent); "
                           "first-passage vocabulary is a liaison, not a "
                           "solved measure; gates sim.py:174,177; "
                           "mechanics sim.py:135-144.  No external refs.",
    }

    # time structure of the denial rate (per-window), reproducible in-run
    def window_rates(g0, steps=3000, win=500):
        random.seed(SEED)
        N = N_ACCOUNTS
        P = Params(g0=g0, floor=0.001, grant_bias=0.5)
        c = Commons(P)
        ids = [c.add_account(seed_credit=0.0,
                             seed_trust=random.uniform(20, 200)) for _ in
               range(N)]
        split = N // 3
        dist = set(ids[:split])
        nec = set(ids[split:2 * split])
        wins = {}
        for s in range(steps):
            c.step()
            for i in range(N):
                a = ids[i]
                b = c.accounts[a]
                if b.trust <= 0:
                    continue
                if a in dist:
                    X = random.uniform(0.5, 2.0)
                    r = c.trade(a, ids[(i + 1) % N], X, necessity=False)
                elif a in nec:
                    X = random.uniform(0.9, 3.0)
                    r = c.trade(a, ids[(i + 1) % N], X, necessity=True)
                else:
                    X = random.uniform(0.5, 1.5)
                    r = c.trade(a, ids[(i + 1) % N], X,
                                necessity=(random.random() < 0.4))
                w = s // win
                wd, wa = wins.get(w, (0, 0))
                wa += 1
                if not r.ok:
                    wd += 1
                wins[w] = (wd, wa)
        outl = []
        for w in sorted(wins):
            d, a = wins[w]
            outl.append(round(d / max(1, a), 4))
        return outl

    low_win = window_rates(0.06)
    high_win = window_rates(0.15)
    out["time_structure"]["low_g0_006_windows"] = low_win
    out["time_structure"]["high_g0_015_windows"] = high_win
    # ramp test: is the low-g0 last window much larger than the first?
    out["time_structure"]["low_g0_last_over_first"] = round(
        low_win[-1] / max(1e-6, low_win[0]), 2)
    out["time_structure"]["n_windows"] = len(low_win)

    # the g0-doubling power from the coarse sweep is now read as
    # HORIZON-DEPENDENT and is intentionally NOT emitted as a claimed law.
    path = os.path.join("experiments", "emanation", "data",
                        "genesis_denial_rate.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("g0 sweep (denial rate per attempt, STEPS=%d):" % STEPS)
    for r in g0_rows:
        print("  g0=%.3f denials=%6d attempts=%7d rate=%.5f ratio=%.2f"
              % (r["g0"], r["denials"], r["attempts"], r["rate"],
                 r["rate_ratio_vs_base"]))
    print("floor sweep:")
    for r in floor_rows:
        print("  floor=%4s denials=%6d attempts=%7d rate=%.5f"
              % (str(r["floor"]), r["denials"], r["attempts"], r["rate"]))
    print("per-window rate (500-step), g0=0.06 (LOW, ramps):")
    print("  ", ["%.4f" % r for r in low_win])
    print("per-window rate (500-step), g0=0.15 (HIGH, plateaus):")
    print("  ", ["%.4f" % r for r in high_win])
    print("rate is NON-STATIONARY at low g0 (last/first=%.2f); "
          "no single steady state; power-law flood claim WITHDRAWN"
          % out["time_structure"]["low_g0_last_over_first"])
    print("WROTE data/genesis_denial_rate.json")


if __name__ == "__main__":
    main()