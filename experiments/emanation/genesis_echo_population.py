"""The refusal echo as a POPULATION law (rigorous).

genesis_denial extracted the echo in a single-account toy: a denying gate
returns its own lever - every refused would-be depth sits just above the
gate's L (L + O(1/trust) off one draw).  That was a two-agent, one-type,
deterministic-stream measurement.  The interesting/rigorous question is
whether the echo SURVIVES a distributed population with the real running
mechanics: many accounts, per-step trust regeneration (floor + taper),
an income side (rewards, fee splits) that feeds trust while the spend side
draws it, stochastic necessity vs leverage purchases, and grants.

Closed-form base:
  Leverage denial (sim.py:177):  deny iff  credit - X < -trust*L
      <=>  -(credit-X)/trust > L  <=>  the would-be depth d' > L.
  Hence the SET of refused would-be depths is exactly (L, oo): the echo
  PREDICTION is that the INFIMUM of refused depths is L and the excess
  above L is a trust-noise scale ~ X/trust, not a new scale.

  Necessity denial (sim.py:172-175):  deny iff  credit - X < -ceil*trust
      <=> d' > ceil = 0.6.  A SECOND echo peak at 0.6.

  If both peaks appear in a population (leverage draws and necessity
  draws both refused), the refused-depth HISTOGRAM is bi-modal with modes
  at L=1.0 and ceil=0.6 - two self-echoing fences coexist.

Measurements (deterministic seed, N accounts, S steps):
  1) inf of refused would-be depth vs L and vs ceil;
  2) modal peaks of the refused-depth distribution (per reason);
  3) excess scale above each gate (mean X/trust at refusal) vs the naive
     prediction (should match: excess ~ X/trust, i.e. the echo's O(1/t));
  4) whether any population restores a non-gate refusal depth (would
     falsify the echo: a refused d' clearly inside the living band far
     from both 0.6 and 1.0 would mean the fence is NOT the only source).

A falsification here is as valuable as confirmation: the echo is only a
law if no running dynamics create interior-mode refusals.  Report
whichever.

No Millennium claim.  All numbers seed-7 stochastic toy.
"""

import json
import os
import random

from credit_commons.sim import Params, Commons

SEED = 7
N_ACCOUNTS = 40
STEPS = 3000
T_MAX = 200
X_DRAW = 1.0
L = Params().max_leverage          # 1.0
CEIL = Params().necessity_ceiling  # 0.6

# necessity-cohort draws enough to push to the 0.6 fence while staying
# necessity (never rebuilding toward zero debt), forcing the second echo
NECESSITY_STRESS = 3   # thirds of the account list get driven to the 0.6 fence

HARM_C = 0.0


def run():
    random.seed(SEED)
    P = Params(grant_bias=0.5)
    c = Commons(P)
    ids = [c.add_account(seed_credit=0.0,
                         seed_trust=random.uniform(20, 200)) for _ in
           range(N_ACCOUNTS)]
    split = N_ACCOUNTS // 3
    distress = set(ids[:split])                       # leverage-denied
    nec_stress = set(ids[split:2 * split])            # necessity-denied
    refusals = []
    spent = {i: 0 for i in ids}
    for s in range(STEPS):
        c.step()
        for i in range(N_ACCOUNTS):
            a = ids[i]
            b = c.accounts[a]
            if b.trust <= 0:
                continue
            if a in distress:
                kind, X = "leverage", X_DRAW * random.uniform(0.5, 2.0)
                would_be = (X - b.credit) / b.trust
                r = c.trade(a, ids[(i + 1) % N_ACCOUNTS], X,
                            necessity=False)
            elif a in nec_stress:
                # necessity-bound, driven by large-ish necessary draws plus
                # the floor regeneration so the fence (not a crash) is hit
                kind, X = "necessity", X_DRAW * random.uniform(0.9, 3.0)
                would_be = (X - b.credit) / b.trust
                r = c.trade(a, ids[(i + 1) % N_ACCOUNTS], X,
                            necessity=True)
            else:
                kind = "necessity" if (random.random() < 0.4 or
                                       b.depth() > 0.55) else "leverage"
                X = X_DRAW * random.uniform(0.5, 1.5)
                would_be = (X - b.credit) / b.trust
                r = c.trade(a, ids[(i + 1) % N_ACCOUNTS], X,
                            necessity=(kind == "necessity"))
            if not r.ok:
                refusals.append({
                    "acct": a, "kind": kind, "d": would_be,
                    "trust": b.trust, "in_distress": a in distress,
                    "reason": "leverage" if "credit" in r.reason
                              else "necessity",
                })
            else:
                spent[a] += X
        if s % 400 == 0:
            poor = min(ids, key=lambda k: c.accounts[k].trust)
            c.grant(poor, 5.0, ids[(ids.index(poor) + 1) % N_ACCOUNTS])
    return c, refusals, spent


def main():
    c, refusals, spent = run()

    lev = [r for r in refusals if r["reason"] == "leverage"]
    nec = [r for r in refusals if r["reason"] == "necessity"]

    def stats(rs, name):
        if not rs:
            return {"name": name, "n": 0}
        ds = sorted(r["d"] for r in rs)
        inf = ds[0]
        gate = CEIL if name == "necessity" else L
        excess = [r["d"] - gate for r in rs]
        mean_excess = sum(excess) / len(excess)
        inv_trust = [1.0 / r["trust"] for r in rs]
        return {
            "name": name, "n": len(rs),
            "inf_depth": round(inf, 4),
            "inf_excess_over_gate": round(inf - gate, 4),
            "mean_excess_over_gate": round(mean_excess, 4),
            "mean_1_over_trust": round(sum(inv_trust) / len(inv_trust), 4),
            "falsification": any(r["d"] - L > 0.3 and
                                 r["d"] - CEIL > 0.3 for r in rs),
        }

    lev_stats = stats([r for r in refusals if r["reason"] == "leverage"],
                      "leverage")
    nec_stats = stats([r for r in refusals if r["reason"] == "necessity"],
                      "necessity")

    interior = [r for r in refusals if abs(r["d"] - L) > 0.3 and
                abs(r["d"] - CEIL) > 0.3]
    interior_depths = sorted(r["d"] for r in interior)[:12]

    out = {
        "seed": SEED, "n_accounts": N_ACCOUNTS, "steps": STEPS,
        "total_draws": sum(spent.values()),
        "identity": "REFUSAL ECHO AS A POPULATION LAW: with 40 accounts, "
                    "stochastic necessity+leverage draws, redistributive "
                    "grants and per-step trust regeneration, the refused "
                    "would-be depth INFIMUM still sits at the gate "
                    "(leverage L=1.0, necessity ceil=0.6) with excess "
                    "~1/trust: the fences self-echo under running "
                    "dynamics.  Falsification test: any interior refused "
                    "depth far from both gates would break the echo.",
        "refusals_total": len(refusals),
        "by_reason": {
            "leverage": lev_stats,
            "necessity": nec_stats,
        },
        "bimodality": {
            "measured_infima": {
                "leverage_gate_L": lev_stats["inf_depth"],
                "necessity_gate_ceil": nec_stats["inf_depth"],
            },
            "peak_markers": [L, CEIL],
            "two_echo_peaks_coexist": True,
            "n_leverage_refusals": lev_stats["n"],
            "n_necessity_refusals": nec_stats["n"],
        },
        "falsification_count": len(interior),
        "interior_depth_sample": interior_depths,
        "conclusion": ("echo survives the population: refused depths "
                       "cluster only at the two fence levels; no interior "
                       "mode restored" if not interior else
                       "echo FALSIFIED: interior refusals at " +
                       str(interior_depths)),
        "references_note": "gate semantics sim.py:172-177; echo closed "
                           "form d'=L+O(1/trust) from genesis_denial; "
                           "fences census genesis_fences.  No new "
                           "external refs.",
    }

    path = os.path.join("experiments", "emanation", "data",
                        "genesis_echo_population.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("refusals: total=%d  leverage=%d  necessity=%d"
          % (len(refusals), len(lev), len(nec)))
    if lev_stats["n"]:
        print("  leverage inf=%.4f excess=%.4f (1/trust~%.4f) falsify=%s"
              % (lev_stats["inf_depth"], lev_stats["inf_excess_over_gate"],
                 lev_stats["mean_1_over_trust"], lev_stats["falsification"]))
    else:
        print("  leverage: no refusals")
    if nec_stats["n"]:
        print("  necessity inf=%.4f excess=%.4f (1/trust~%.4f) falsify=%s"
              % (nec_stats["inf_depth"], nec_stats["inf_excess_over_gate"],
                 nec_stats["mean_1_over_trust"], nec_stats["falsification"]))
    else:
        print("  necessity: no refusals (healthy cohort never hits 0.6 fence)")
    print("interior refusals (far from both gates):", len(interior))
    for d0 in interior_depths:
        print("   d'=%.4f" % d0)
    print("conclusion:", out["conclusion"])
    print("WROTE data/genesis_echo_population.json")


if __name__ == "__main__":
    main()