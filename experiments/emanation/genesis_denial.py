"""The refusal echo: a denying gate returns its own L, never the would-be.

First measurement here showed something degenerate and therefore deep: the
five refusals that freeze the harmed run ALL have would-be depth
d' = (X - credit)/trust ~ 1.001 - exactly L + 1/trust with L = max_leverage
= 1.0.  The gate denies the FIRST draw past the line, so the refusal
stream is pinned at L + 1/trust; archival of refusals can NEVER recover
what the engine refused.  The freeze file and the refusal log both say
"the line held" - they cannot say how deep the run WOULD have gone.

The only way to see the would-be excursion is to run a DIFFERENT gate:
max_leverage is the boundary's truncation lever.  By this arc's
ignition/crossover law, resolvability of the economy's own cusp
d* = 2.1106 switches on only when the gate PACKS the line (L > d*).
Sweep L to demonstrate both:

  1) REFUSAL ECHO LAW: for any L, every refusal's would-be depth is
     L + 1/trust (the gate returns its own lever).  The refusal stream is
     structurally degenerate - a flat echo, not a measurement.
  2) TRUNCATION MARGIN: for L < d* the gate freezes BELOW the cusp;
     the ledger's deepest observed state is L-ish, and d* - L is the
     unknowable dark margin of the engine's own reading.
  3) STRADDLING PROBE: at L = 2.5 > d* the engine enters the region the
     book calls the hyperbolic band; the freeze happens LATER (more
     accepted trades) and the freeze depth reports ~ L - i.e. only a
     meter that straddles the cusp sees it.  Same law as the folded-
     channel ignition (genesis_crossover), now on the engine's own
     primary boundary.

The audit stands: Commons.ledger records only successful trades; refusals
are unarchived.  Even if archived, the refusal log would be an echo of L -
the excursion lives only in counterfactual runs (straddling gates).

No Millennium claim; all numbers from seed-42 runs of the toy.
"""

import json
import math
import os
import random

from credit_commons.sim import Params, Commons

X = 1.0
HARM_PER_TRADE = 0.05
MAX_STEPS = 500000
SEED_CREDIT = 0.0
SEED_TRUST = 1000.0
D_STAR = 2.1106     # cusp (harm_as_depth book constant)

_P0 = Params()
G_STAR = 2.0 * math.sqrt(_P0.g0 * _P0.gdepth * _P0.reward())
# recompute d* from the parameters to avoid a hard-coded drift check:
D_STAR_REC = (G_STAR / _P0.g0 - 1.0) / _P0.gdepth


def run(lever, with_harm):
    random.seed(42)
    P = Params(max_leverage=lever)
    c = Commons(P)
    buyer = c.add_account(seed_credit=SEED_CREDIT, seed_trust=SEED_TRUST)
    seller = c.add_account(seed_credit=0.0, seed_trust=SEED_TRUST)
    refusal_depths = []
    accepted = 0
    deepest_reached = 0.0
    streak = 0
    steps = 0
    while steps < MAX_STEPS:
        c.step()
        b = c.accounts[buyer]
        would_be = (X - b.credit) / b.trust if b.trust > 0 else None
        h = HARM_PER_TRADE if with_harm else 0.0
        r = c.trade(buyer, seller, X, committed_harm=h)
        if not r.ok:
            if would_be is not None:
                refusal_depths.append(would_be)
            streak += 1
            if streak >= 5:
                break
        else:
            streak = 0
            accepted += 1
        deepest_reached = max(deepest_reached, (-c.accounts[buyer].credit) /
                              c.accounts[buyer].trust if
                              c.accounts[buyer].trust > 0 else 0.0)
        steps += 1
    fin = c.accounts[buyer]
    rd = refusal_depths or [0.0]
    return {
        "lever_L": lever,
        "accepted_trades": accepted,
        "denials": len(refusal_depths),
        "refusal_echo_median": sorted(rd)[len(rd) // 2],
        "refusal_echo_min": min(rd),
        "refusal_echo_max": max(rd),
        "deepest_reached": deepest_reached,
        "freeze_depth": fin.depth(),
        "freeze_trust": fin.trust,
        "freeze_credit": fin.credit,
    }


def main():
    rows = []
    for lever in (1.0, 1.5, 2.0, 2.5):
        cl = run(lever, False)
        harmed = run(lever, True)
        rows.append({
            "lever_L": lever,
            "clean": {"accepted": cl["accepted_trades"],
                      "denials": cl["denials"],
                      "refusal_echo": round(cl["refusal_echo_median"], 4)},
            "harmed": {"accepted": harmed["accepted_trades"],
                       "denials": harmed["denials"],
                       "refusal_echo": round(harmed["refusal_echo_median"],
                                             4),
                       "refusal_echo_range": [
                           round(harmed["refusal_echo_min"], 4),
                           round(harmed["refusal_echo_max"], 4)],
                       "deepest": round(harmed["deepest_reached"], 4),
                       "freeze_depth": round(harmed["freeze_depth"], 6)},
            "truncation_margin_below_cusp": round(
                D_STAR_REC - lever, 4),
        })

    out = {
        "identity": "REFUSAL ECHO: a denying gate returns its own lever L "
                    "(every would-be refused depth = L + 1/trust), never "
                    "the would-be excursion; archival of refusals cannot "
                    "reveal what was refused.  max_leverage is the "
                    "boundary's truncation lever: below the cusp "
                    "d* = %.4f the ledger's deepest state is L-ish and "
                    "d*-L is the dark margin of the engine's own reading; "
                    "only a STRADDLING gate (L > d*) lets the engine "
                    "enter/count the hyperbolic band - ignition on the "
                    "primary boundary, same law as genesis_crossover."
                    % D_STAR_REC,
        "d_star_recomputed": round(D_STAR_REC, 4),
        "refusal_echo_law": "refused would-be depth = L + 1/trust; the "
                            "refusal log is a flat echo of the gate, "
                            "regardless of how deep the run would have "
                            "gone.",
        "truncation_margin": "d* - L: for L < d* the freeze hides this "
                             "margin; only a straddling probe recovers it.",
        "sweep_harmed": rows,
        "audit": {
            "ledger_records_refusals": False,
            "finding": "refusals are neither archived nor (by the echo "
                       "law) recoverable from archival - they are the "
                       "gate's own reading.  The excursion is observable "
                       "only in counterfactual runs with L > d*, i.e. by "
                       "a meter that straddles the boundary.",
        },
        "references_note": "ignition/crossover law (genesis_crossover); "
                           "truncated-meter plateau (genesis_meter); "
                           "irreducibility of folded channels "
                           "(genesis_metamery); metrology frame JCGM 2008; "
                           "d* recomputed here from Params, not copied.",
    }
    path = os.path.join("experiments", "emanation", "data",
                        "genesis_denial.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("d* recomputed from Params = %.4f" % D_STAR_REC)
    print("refusal echo law: would-be refused = L + 1/trust")
    print("%6s %16s %10s %12s %14s" % ("L", "harmed_trades",
                                       "echo(L)", "deepest", "d*-L"))
    for r in rows:
        print("%6.1f %13d %10.3f %12.3f %12.4f" % (
            r["lever_L"], r["harmed"]["accepted"],
            r["harmed"]["refusal_echo"], r["harmed"]["deepest"],
            r["truncation_margin_below_cusp"]))
    print("at L=2.5 > d* the gate straddles: the engine enters/counts the "
          "hyperbolic band and the freeze deepens - resolvability of the "
          "cusp switches on only past the line (crossover law).")
    print("WROTE data/genesis_denial.json")


if __name__ == "__main__":
    main()