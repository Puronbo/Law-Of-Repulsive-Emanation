"""The anti-FT channel: committed harm I*h is the engine's only generator
of negative community action.

ft_ledger.json showed community trust NEVER falls over 19k honest trades
(losses=0): the pump is strictly positive.  The one designed exception is
committed_harm (sim.py:187-194): buyer trust -= I*h (=2*h), no paired +sigma.
This run tests the exact identities with identical RNG streams:
  * control (no harm): community loss events = 0;
  * mixed (harm fraction): community_total_mixed == community_total_control
    - I*sum(h) to ~0 residual  (the harm shifts the pump by exactly -I*h);
  * I*sum(h) scar is exactly conserved into the accounts' irrev column
    (gate 14 conservation, like credit conservation under gate 6).
"""

import json
import math
import os
import random

from credit_commons.sim import Params, Commons

random.seed(42)
P = Params()
N_TRADES = 8000
HARM_LO, HARM_HI = 0.02, 0.20


def run(harm_style, seed=42):
    random.seed(seed)
    c = Commons(P)
    a = c.add_account(seed_credit=0.0, seed_trust=1000.0)
    b = c.add_account(seed_credit=0.0, seed_trust=1000.0)

    comm_total = 0.0
    neg_events = 0
    neg_total = 0.0
    harm_committed = 0.0
    irrev_total = 0.0
    last = None
    neg_first_descr = None

    for _ in range(N_TRADES):
        buyer, seller = (a, b) if random.random() < 0.5 else (b, a)
        X = round(random.uniform(0.05, 1.5), 2)
        h = round(random.uniform(HARM_LO, HARM_HI), 4)
        committed = h if harm_style == "mixed" else 0.0
        t0 = c.accounts[buyer].trust + c.accounts[seller].trust
        r = c.trade(buyer, seller, X, necessity=False, terminal=seller,
                    committed_harm=committed)
        if not r.ok:
            continue
        t1 = c.accounts[buyer].trust + c.accounts[seller].trust
        d = t1 - t0
        comm_total += d
        if committed > 0:
            harm_committed += committed
        if d < 0:
            neg_events += 1
            neg_total -= d
            if neg_first_descr is None:
                g = P.g_at(c.accounts[buyer].depth())
                neg_first_descr = {"x": X, "h": h, "g": g, "d": d}
        last = c

    irrev_total = c.accounts[a].irrev + c.accounts[b].irrev
    expected_delta = -P.I * harm_committed
    return {"harm_style": harm_style, "comm_total": comm_total,
            "neg_events": neg_events, "neg_total": neg_total,
            "harm_committed": harm_committed, "I": P.I,
            "expected_harm_shift": expected_delta,
            "irrev_total": irrev_total,
            "residual": comm_total - (comm_total - expected_delta) - (
                expected_delta - expected_delta),
            "neg_first": neg_first_descr}


def main():
    ctrl = run("control")
    mix = run("mixed")
    # identical streams, so the ONLY difference is the -I*h shift plus any
    # feedback through depth (trust drops -> depth up -> g up -> draw up).
    shift = mix["comm_total"] - ctrl["comm_total"]
    expected = mix["expected_harm_shift"]            # -I*sum(h) < 0
    irrev_expected = -expected                       # +I*sum(h)
    irrev_check = mix["irrev_total"] - irrev_expected
    feedback = shift - expected                      # amplification via depth
    amp = shift / expected if expected else 0.0      # >1 means harm amplifies
    out = {
        "seed": 42,
        "identity": "committed harm is the anti-FT channel: with identical "
                    "RNG streams the mixed economy's cumulative community "
                    "trust equals the control minus I*sum(h) PLUS a depth-"
                    "feedback amplification (harm-depleted trust raises "
                    "depth -> g -> draw).  I*sum(h) is exactly conserved "
                    "into account irrev (gate 14).",
        "n_trades": N_TRADES, "harm_range": [HARM_LO, HARM_HI], "I": P.I,
        "control": ctrl, "mixed": mix,
        "comparison": {
            "direct_shift_expected": expected,
            "measured_shift": shift,
            "depth_feedback_term": feedback,
            "amplification_factor": amp,
            "irrev_conserved": mix["irrev_total"],
            "irrev_expected": irrev_expected,
            "irrev_residual": irrev_check,
        },
    }
    path = os.path.join("experiments", "emanation", "data", "harm_ft_break.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("control: comm_total=%.4f  neg_events=%d" % (ctrl["comm_total"],
                                                       ctrl["neg_events"]))
    print("mixed  : comm_total=%.4f  neg_events=%d  neg_total=%.4f"
          % (mix["comm_total"], mix["neg_events"], mix["neg_total"]))
    print("first negative event: X=%.2f h=%.4f g=%.4f d=%.6f  (I*h=%.4f "
          "vs (reward-g)*X=%.4f)"
          % (mix["neg_first"]["x"], mix["neg_first"]["h"], mix["neg_first"]["g"],
             mix["neg_first"]["d"], P.I * mix["neg_first"]["h"],
             (P.reward() - mix["neg_first"]["g"]) * mix["neg_first"]["x"]))
    print("direct shift (-I*sum h) = %.4f  measured = %.4f"
          % (expected, shift))
    print("depth-feedback term = %.4f  (amplification x%.6f)"
          % (feedback, amp))
    print("irrev conserved: total=%.4f expected=%.4f residual=%.6f"
          % (mix["irrev_total"], irrev_expected, irrev_check))
    print("WROTE data/harm_ft_break.json")


if __name__ == "__main__":
    main()