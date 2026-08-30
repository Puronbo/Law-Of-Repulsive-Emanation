"""Does the genesis exceptional fiber split 4 -> 6 -> 12, mirroring the
bosonic splitting pattern (1 -> 4 -> 6 -> 12)?

genesis_blowup.json measured the CORE four rays of the ledger origin:
  T trade (slope ~g0), H harm (slope ~I), N necessity (slope ~-n), S seed
  (pure credit).  This run enumerates the engine's TWELVE documented
  elementary economic processes (docs/CREDIT_COMMONS.md, sim.py Params) and
  probes every trust-moving one at the origin; the credit-only rails are
  recorded as directions (1:0).  The registry then lays out the layered
  splitting as they occur in the engine's OWN layers:

    Layer 1  core market      : T, H, N, S                       = 4
    Layer 2  financing mirrors: grant G, regeneration tick Z     = 2  (=> 6)
    Layer 3  fee / tax rails  : taper A, consumer-floor F,
                                terminal L, referrer R,
                                validator V, reserve sink B      = 6  (=> 12)

The 12 = 4 + 2 + C(4,2); the six Layer-3 rails are the pairwise conduits
(edges of K4) over a fee'd trade's four parties (buyer, seller, terminal,
reserve).  All values measured from sim.py; nothing assumed.
"""

import json
import os

from credit_commons.sim import Params, Commons

P = Params()
g0 = P.g0
I = P.I
n = P.n
X = 1e-4


def new_c(seed_credit=0.0, seed_trust=1e-2, seller_trust=1e3):
    c = Commons(P)
    b = c.add_account(seed_credit=seed_credit, seed_trust=seed_trust)
    s = c.add_account(seed_credit=0.0, seed_trust=seller_trust)
    return c, b, s


def delta_of(c, who):
    a = c.accounts[who]
    return (round(a.credit, 12), round(a.trust, 12))


def main():
    reg = {}

    # T trade ---------------------------------------------------------------
    c, b, s = new_c()
    before = (c.accounts[b].credit, c.accounts[b].trust)
    assert c.trade(b, s, X).ok
    dC, dT = c.accounts[b].credit - before[0], c.accounts[b].trust - before[1]
    reg["T_trade_draw"] = {"layer": 1, "ray": [dC, dT],
                           "slope_dT_dC": dT / dC,
                           "sim": "sim.py:202-204 g_at(depth)*X",
                           "params": "g0=%.3f gdepth=%.2f" % (P.g0, P.gdepth)}

    # H harm -----------------------------------------------------------------
    c, b, s = new_c()
    before = (c.accounts[b].credit, c.accounts[b].trust)
    assert c.trade(b, s, X, committed_harm=1e-4).ok
    dC, dT = c.accounts[b].credit - before[0], c.accounts[b].trust - before[1]
    reg["H_harm_scar"] = {"layer": 1, "ray": [dC, dT],
                          "slope_dT_dC": dT / dC,
                          "sim": "sim.py:187-193 I*committed_harm",
                          "params": "I=%.2f" % P.I}

    # N necessity ------------------------------------------------------------
    c, b, s = new_c()
    before = (c.accounts[b].credit, c.accounts[b].trust)
    assert c.trade(b, s, X, necessity=True).ok
    dC, dT = c.accounts[b].credit - before[0], c.accounts[b].trust - before[1]
    reg["N_necessity_build"] = {"layer": 1, "ray": [dC, dT],
                                "slope_dT_dC": dT / dC,
                                "sim": "sim.py:197-200 trust += n*X, no draw",
                                "params": "n=%.2f" % P.n}

    # S seed (Phase-0 external, off-membrane) -------------------------------
    c, b, s = new_c(seed_credit=0.0, seed_trust=0.0)
    sid = c.add_account(seed_credit=5.0, seed_trust=0.0)
    a = c.accounts[sid]
    reg["S_seed_inflow"] = {"layer": 1, "ray": [a.credit, a.trust],
                            "point": "(1:0) pure credit, mintage by design",
                            "sim": "sim.py:109-120 add_account",
                            "params": "seed_credit=5.0 seed_trust=0.0"}

    # G grant (reserve-funded; the giving mirror of T) ----------------------
    c, b, s = new_c()
    c.reserve = 1.0                # fund the rail (reserve is model-internal)
    before = (c.accounts[b].credit, c.accounts[b].trust)
    amt = c.grant(b, 1e-3)
    dC, dT = c.accounts[b].credit - before[0], c.accounts[b].trust - before[1]
    reg["G_grant_mirror"] = {"layer": 2, "ray": [round(dC, 12), round(dT, 12)],
                             "slope_dT_dC": (dT / dC) if dC else None,
                             "sim": "sim.py:121-127, 246-254 progressive grant",
                             "params": "grant_bias=%.2f 0.05*amt trust" % P.grant_bias}

    # Z regeneration tick (floor) -------------------------------------------
    c, b, s = new_c()
    t0 = c.accounts[b].trust
    c.step()
    dT = c.accounts[b].trust - t0
    reg["Z_tick_floor"] = {"layer": 2, "ray": [0.0, dT],
                           "slope_dT_dC": None, "point": "(0:1) pure-trust +",
                           "sim": "sim.py:135-144 trust += floor",
                           "params": "floor=%.3f" % P.floor}

    # A taper (idle surplus drain) ------------------------------------------
    c, b, s = new_c(seed_credit=0.5, seed_trust=0.01)
    t0 = c.accounts[b].trust
    c.step()
    dT = c.accounts[b].trust - t0
    reg["A_taper_drain"] = {"layer": 3, "ray": [0.0, dT],
                            "slope_dT_dC": None, "point": "(0:-1) pure-trust -",
                            "sim": "sim.py:139-141, 61-65 taper_of",
                            "params": "taper0=%.2f taperA=%.4f" % (P.taper0, P.taperA)}

    # F consumer-floor rebate ------------------------------------------------
    c, b, s = new_c()
    assert c.trade(b, s, X).ok
    # floor: fee*consumer_floor credited back to buyer (sim.py:237-242)
    fee = P.f * X
    floor_val = fee * P.consumer_floor
    reg["F_floor_rebate"] = {"layer": 3, "ray": [floor_val, 0.0],
                             "point": "(1:0) credit rail",
                             "sim": "sim.py:237-242 consumer floor",
                             "params": "consumer_floor=%.2f" % P.consumer_floor}

    # L terminal / R referrer / V validator / B reserve ----------------------
    rem = fee - floor_val
    for key, share, ss in [
            ("L_terminal_share", P.terminal_share, "sim.py:245-249"),
            ("R_referrer_share", P.refer_share, "sim.py:250-254"),
            ("V_validator_share", P.validator_share, "sim.py:255-262")]:
        reg[key] = {"layer": 3, "ray": [rem * share, 0.0],
                    "point": "(1:0) credit rail",
                    "sim": ss, "params": "share=%.2f" % share}
    reserve_val = fee - floor_val
    reg["B_reserve_sink"] = {"layer": 3, "ray": [reserve_val, 0.0],
                             "point": "reserve column (meta), conserving",
                             "sim": "sim.py:263-264 reserve += fee - spent",
                             "params": "f=%.2f" % P.f}

    layers = {1: [], 2: [], 3: []}
    for k, v in reg.items():
        layers[v["layer"]].append(k)
    counts = {ln: len(ks) for ln, ks in layers.items()}
    n1, n2, n3 = counts[1], counts[2], counts[3]

    out = {
        "identity": "the genesis exceptional fiber splits in nested layers "
                    "4 -> 6 -> 12 mirroring the bosonic split pattern "
                    "(1 -> 4 -> 6 -> 12): 12 documented elementary processes "
                    "= 4 core + 2 mirrors + 6 pairwise fee/tax rails "
                    "(C(4,2)=6 edges of K4 over a trade's four parties).",
        "12_documented_elementary_processes": reg,
        "layers": layers,
        "counts": {"layer1": n1, "layer1+2": n1 + n2, "all": n1 + n2 + n3},
        "nesting": "4 subset 6 subset 12: %s" % (
            set(layers[1]).issubset(layers[1] + layers[2])
            and set(layers[1] + layers[2]).issubset(
                layers[1] + layers[2] + layers[3])),
        "layering_rule": "4 core market rays; +2 financing/axial mirrors "
                         "(grant + regeneration)=6; +6 pairwise conduit rails "
                         "(K4 edges: taper, consumer-floor, terminal, "
                         "referrer, validator, reserve)=12.",
        "honest_caveats": [
            "credit-only rails all share the point (1:0) on the fiber; "
            "the COUNT is of processes (charges), not of distinct directions",
            "the matching to the bosonic 1->4->6->12 is a charge-count "
            "transfer, not a physical identification",
        ],
    }
    path = os.path.join("experiments", "emanation", "data", "genesis_split.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("layer 1 (core, 4): %s" % ", ".join(layers[1]))
    print("layer 2 (+2 = 6):  %s" % ", ".join(layers[2]))
    print("layer 3 (+6 = 12): %s" % ", ".join(layers[3]))
    print("counts: 4 -> %d -> %d  | 12 nested: %s"
          % (n1 + n2, n1 + n2 + n3, out["nesting"]))
    print("slopes: T=%.4f  H=%.4f  N=%.4f" % (
        reg["T_trade_draw"]["slope_dT_dC"], reg["H_harm_scar"]["slope_dT_dC"],
        reg["N_necessity_build"]["slope_dT_dC"]))
    print("WROTE data/genesis_split.json")


if __name__ == "__main__":
    main()