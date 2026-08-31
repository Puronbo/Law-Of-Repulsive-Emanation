"""The three fences of depth: interior protection, denial, cusp, asymptote.

genesis_denial established the REFUSAL ECHO on the leverage gate
(sim.py:177): every denied would-be depth equals the gate's own lever L
plus one draw, so a denying gate reads only itself.  Here the same law is
applied to the engine's SECOND denial gate - the necessity-protection
ceiling (sim.py:172-175), a reserved fraction of trust immune to the hard
gate and held INSIDE the danger zone (0.6 << d* = 2.11).  Measurements:

  1) NECESSITY ECHO: a necessity-only buyer is denied when cumulative
     spend passes 0.6*trust; the refused would-be depth should read
     0.6 + 1/trust - the echo law with lever 0.6.
  2) UNCAPED NECESSITY ASYMPTOTE: necessity draws never deepen (draw = 0,
     trust regenerates at n*X + floor per step; n = 0.10 necessity
     rebuild, floor = 0.001 baseline), so with the ceiling removed the
     depth converges -credit/trust -> t/(1000 + 0.101 t) -> 1/0.101 =
     9.90.  FINITE - but 4.7x ABOVE the catapult cusp d* = 2.1106.  The
     fence at 0.6 therefore keeps the poor's paper-depth below the
     (theoretical) catapult entry even though the uncapped would-be lives
     far above it.  Necessity cannot catapult (no scar, no drawdown), so
     the excess is benign - the fence protects the ledger's credit
     aesthetics, not crisis.
  3) THE THREE FENCES of the depth axis: 0.6 (interior protection),
     1.0 (denial, default max_leverage), 2.1106 (catastrophe cusp from
     Params).  Two are refusal echoes of their own gate; the third is
     the theory constant; the gaps (0.4 and 1.11) are, by the echo law,
     NOT readable from inside the economy - only a straddling probe
     crosses them.
"""

import json
import math
import os
import random

from credit_commons.sim import Params, Commons

X = 1.0
MAX_STEPS = 400000
SEED_CREDIT = 0.0
SEED_TRUST = 1000.0

_P = Params()
G_STAR = 2.0 * math.sqrt(_P.g0 * _P.gdepth * _P.reward())
D_STAR = (G_STAR / _P.g0 - 1.0) / _P.gdepth          # 2.1106
N_FLOOR = _P.n + _P.floor                            # 0.10 + 0.001
PRED_ASYMPTOTE = 1.0 / N_FLOOR                        # 9.9010


def run(ceiling, with_harm=False):
    random.seed(42)
    P = Params(necessity_ceiling=ceiling)
    c = Commons(P)
    buyer = c.add_account(seed_credit=SEED_CREDIT, seed_trust=SEED_TRUST)
    seller = c.add_account(seed_credit=0.0, seed_trust=SEED_TRUST)
    refused = []
    streak = 0
    steps = 0
    max_depth = 0.0
    try_n = 0
    while steps < MAX_STEPS:
        c.step()
        b = c.accounts[buyer]
        if b.trust > 0:
            would_be = (X - b.credit) / b.trust
            max_depth = max(max_depth, would_be)
        h = HARM if with_harm else 0.0
        r = c.trade(buyer, seller, X, necessity=True, committed_harm=h)
        try_n += 1
        if not r.ok:
            if b.trust > 0:
                refused.append((X - b.credit) / b.trust)
            streak += 1
            if streak >= 5:
                break
        else:
            streak = 0
        steps += 1
    fin = c.accounts[buyer]
    rd = sorted(refused) or [0.0]
    return {
        "trades_accepted": try_n - len(refused),
        "denials": len(refused),
        "echo_median": rd[len(rd) // 2],
        "echo_range": (rd[0], rd[-1]),
        "max_would_be_depth": max_depth,
        "final_depth": fin.depth(),
        "final_trust": fin.trust,
    }


HARM = 0.0   # necessity path: no scar applied in this census


def main():
    bounded = run(Params().necessity_ceiling)          # 0.6
    uncapped = run(1e6)                                 # effectively no fence

    fences = {
        "interior_protection_L": Params().necessity_ceiling,
        "denial_L": Params().max_leverage,
        "cusp_d_star": round(D_STAR, 4),
        "uncapped_asymptote_1/(n+floor)": round(PRED_ASYMPTOTE, 4),
    }

    out = {
        "identity": "THE THREE FENCES of depth: 0.6 (interior "
                    "protection, necessity ceiling), 1.0 (denial, "
                    "max_leverage), 2.1106 (catastrophe cusp from "
                    "Params), plus the uncapped necessity asymptote "
                    "1/(n+floor).  The interior fence ECHOES the same "
                    "refusal law (refused would-be = L + 1/trust) with "
                    "lever 0.6; the interior gaps (0.4, 1.11) are not "
                    "readable from inside, by the echo law.",
        "necessity_echo": {
            "lever": Params().necessity_ceiling,
            "bounded_run": {
                "trades": bounded["trades_accepted"],
                "denials": bounded["denials"],
                "refused_would_be_median": round(bounded["echo_median"], 4),
                "predicted": round(Params().necessity_ceiling +
                                   1.0 / bounded["final_trust"], 4),
                "echo_ok": round(bounded["echo_median"] -
                                 (Params().necessity_ceiling +
                                  1.0 / bounded["final_trust"]), 4),
            },
            "uncapped_run": {
                "max_depth_reached": round(uncapped["max_would_be_depth"],
                                           4),
                "asymptote_1_div_(n+floor)": round(PRED_ASYMPTOTE, 4),
                "final_depth": round(uncapped["final_depth"], 4),
                "above_cusp": round(uncapped["max_would_be_depth"] /
                                    D_STAR, 3),
            },
            "interpretation": "necessity draws never deepen (draw=0, "
                              "trust regenerates at n*X+floor = 0.101 per "
                              "step), so the uncapped paper-depth "
                              "converges FINITE ~9.90 - 4.7x ABOVE the "
                              "catapult cusp; but necessity cannot "
                              "catapult (no scar, no drawdown), so the "
                              "fence is protection of the credit ledger's "
                              "aesthetics; at 0.6 it sits far below both "
                              "denial and cusp."
        },
        "fences": fences,
        "gaps_not_readable_inside": {
            "0.6_to_1.0": round(Params().max_leverage -
                                Params().necessity_ceiling, 4),
            "1.0_to_cusp": round(D_STAR - Params().max_leverage, 4),
            "note": "per the refusal echo, each fence's reading is its "
                    "own lever; the gap between fences is recoverable "
                    "only by straddling probes (genesis_crossover law).",
        },
        "references_note": "echo law and ignition (genesis_denial, "
                           "genesis_crossover, genesis_metamery); d* "
                           "recomputed from Params; necessity mechanics "
                           "E1 in sim.py:172-200.",
    }
    path = os.path.join("experiments", "emanation", "data",
                        "genesis_fences.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("d* = %.4f ; 1/(n+floor) = %.4f" % (D_STAR, PRED_ASYMPTOTE))
    print("necessity echo (L=0.6):")
    print("  bounded:  trades=%d denials=%d refused_would_be=%.4f"
          % (bounded["trades_accepted"], bounded["denials"],
             bounded["echo_median"]))
    print("  predicted %.4f (0.6 + 1/trust@freeze)" %
          (Params().necessity_ceiling + 1.0 / bounded["final_trust"]))
    print("  uncapped: max depth=%.4f (asymptote 1/(n+floor)=%.4f, "
          "%.3f x cusp)"
          % (uncapped["max_would_be_depth"], PRED_ASYMPTOTE,
             uncapped["max_would_be_depth"] / D_STAR))
    print("fences: 0.6 (protection)  1.0 (denial)  %.4f (cusp)  %.4f"
          % (D_STAR, PRED_ASYMPTOTE))
    print("gaps 0.6->1.0=%.4f ; 1.0->cusp=%.4f (not readable from inside)"
          % (Params().max_leverage - Params().necessity_ceiling,
             D_STAR - Params().max_leverage))
    print("WROTE data/genesis_fences.json")


if __name__ == "__main__":
    main()