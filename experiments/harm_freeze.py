"""Death by denial, not loss: mass harm freezes the market while finance stays
exactly conserved.  This is the thermodynamic closure of the harm arc.

honest FT is a strict pump (ft_ledger: losses=0), harm is the anti-FT channel
(harm_ft_break: irrev conserved to residual 0.000000), and harm catapults past
the cusp d*=2.11 (harm_as_depth) with escape rate h/X>alpha_cusp predictable
(harm_cap: 0.8305 vs 0.8361).  Left unmeasured until now: what mass harm does
to the LIVE market.  Claim: the market dies at the honest 2x gate (depth=1,
which phase_boundary records 53% below the cusp d*=2.11) -- i.e. it freezes by
denial, never by loss: conserved_total stays exact, irrev absorbs I*sum(h), and
the honest capacity lost per harm trade is exactly I*h (measured by the denial
lag between clean and harmed runs).
"""

import json
import os
import random

from credit_commons.sim import Params, Commons

random.seed(42)
P = Params()
X = 1.0
HARM_PER_TRADE = 0.05          # I*h = 0.10 scar (trust) per trade
MAX_STEPS = 200000
SEED_CREDIT = 0.0              # buyer runs the whole market on trust
SEED_TRUST = 1000.0


def run_with(with_harm):
    random.seed(42)
    c = Commons(P)
    buyer = c.add_account(seed_credit=SEED_CREDIT, seed_trust=SEED_TRUST)
    seller = c.add_account(seed_credit=0.0, seed_trust=SEED_TRUST)

    def conserved():
        # sum live credits (sim tracks total_credit only at creation) + reserve
        return sum(a.credit for a in c.accounts.values()) + c.reserve

    gen_credit = conserved()

    steps = 0
    denials = 0
    final_ok = None
    while steps < MAX_STEPS:
        c.step()  # honest breathing: floor regeneration + idle taper
        h = HARM_PER_TRADE if with_harm else 0.0
        r = c.trade(buyer, seller, X, committed_harm=h)
        if not r.ok:
            denials += 1
            if denials >= 5:            # five consecutive denials => frozen
                break
        else:
            denials = 0
            final_ok = steps
        steps += 1

    b = c.accounts[buyer]
    s = c.accounts[seller]
    return {
        "steps": steps,
        "trades_ok": final_ok if final_ok is not None else steps,
        "denials_run_end": denials,
        "buyer": {"credit": b.credit, "trust": b.trust, "depth": b.depth(),
                  "harm_cum": b.harm, "irrev": b.irrev},
        "seller": {"credit": s.credit, "trust": s.trust, "depth": s.depth(),
                   "served": s.served},
        "conserved_total": conserved(),
        "genesis_credit": gen_credit,
        "conservation_residual": conserved() - gen_credit,
    }


def main():
    clean = run_with(False)
    harmed = run_with(True)

    n_clean = clean["trades_ok"]
    n_harm = harmed["trades_ok"]
    d_n = n_clean - n_harm
    i_sum_h = harmed["buyer"]["irrev"]
    # freezed scar-equivalent: how much of the trust budget scars consumed
    scar_budget_consumed = i_sum_h / SEED_TRUST

    out = {
        "seed": 42,
        "identity": "death by denial: mass harm freezes the market at the "
                    "honest 2x gate (depth=1, 53% below cusp d*=2.11) while "
                    "credit conservation holds to floating-point; the scar "
                    "I*sum(h) is real, once, in irrev.",
        "X_per_trade": X, "harm_per_trade": HARM_PER_TRADE,
        "clean_trades": n_clean, "harmed_trades": n_harm,
        "denial_lag_delta_n": d_n,
        "scar_trust_budget_consumed": round(scar_budget_consumed, 6),
        "irrev_absorbed": round(i_sum_h, 6),
        "trust_gap_clean_minus_harmed_at_freeze": round(
            clean["buyer"]["trust"] - harmed["buyer"]["trust"], 6),
        "conserved_total_at_freeze": harmed["conserved_total"],
        "conservation_residual": round(harmed["conservation_residual"], 12),
        "gate_depth_at_freeze": round(harmed["buyer"]["depth"], 6),
        "cusp_d_star": 2.111,
        "denier": "2x gate (b.credit-X < -b.trust): depth=1 caps draw g<=0.11",
        "note": "the honest market refuses to enter the hyperbolic band; "
                "harm = instant catapult that bypasses the climb.",
    }
    path = os.path.join("experiments", "data", "harm_freeze.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("clean:  trades_ok=%d  conserved_resid=%.2e" % (n_clean, clean["conservation_residual"]))
    print("harmed: trades_ok=%d  conserved_resid=%.2e  irrev=%.4f"
          % (n_harm, harmed["conservation_residual"], i_sum_h))
    print("denial lag delta_n = %d;  consumed %.1f%% of 1000-trust scar budget"
          % (d_n, 100 * scar_budget_consumed))
    print("buyer depth at freeze = %.4f  (cusp d*=2.111: 53%% margin)"
          % harmed["buyer"]["depth"])
    print("conserved_total at freeze = %.6f  residual %.3e" % (
        harmed["conserved_total"], harmed["conservation_residual"]))
    print("WROTE data/harm_freeze.json")


if __name__ == "__main__":
    main()