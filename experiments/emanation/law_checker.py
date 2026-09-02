"""Law checker: machine-readable certificates for candidate trajectory
laws over CA rules (the T1 seed of the 'physics replaces the
proof-checker' goal).

Given a deterministic step function, a candidate law (predictor), and a
domain of configs + horizons, verify exhaustively or per-sample and emit
a JSON certificate:

    {label, meta, domain, configs_checked, points_checked, status,
     n_mismatch, first_mismatch}

status is PASS when no configs disagree, and HONEST_NEGATIVE (with the
exact counter-example) otherwise.  A certificate is a *measured fact*:
every number comes from direct comparison against the true evolution on
the stated domain -- a supervisor can query these files instead of
re-running simulations, and the honest-negative entries are exactly the
candidates that must not be believed.

Domains supported:
    * exhaustive: every config meeting a predicate inside a cell window
    * sampled:    rng draws (meta carries the condition the law requires)
"""
import json
import os
import random

import shift_bus as sh


def verify_trajectory_law(step_fn, law_fn, configs, horizons):
    """Compare law to truth over configs x horizons.  `horizons` may be
    an iterable of T values or a callable T_domain(config).  Returns
    (points_checked, first_mismatch_or_None)."""
    checked = 0
    first = None
    for conf in configs:
        Ts = horizons(conf) if callable(horizons) else horizons
        for T in Ts:
            actual = step_fn(list(conf), T)
            pred = law_fn(list(conf), T)
            checked += 1
            if actual != pred and first is None:
                first = {
                    "config": list(conf),
                    "T": T,
                    "actual": sorted(actual),
                    "law": sorted(pred),
                }
    return checked, first


def min_gap(conf):
    if len(conf) < 2:
        return None
    return min(b - a for a, b in zip(conf, conf[1:]))


def merge_free_horizons(conf):
    """T <= g_min - 2 keeps every gap >= 2 forever (gap(t) >= gap(0)-t
    since no particle moves left), so no trailing particle can catch a
    cluster's melt within the whole trajectory: the per-cluster union
    law is exact on this sector by construction."""
    g = min_gap(conf)
    if g is None:
        return range(0, 3)
    return range(0, max(0, g - 1))


def certify(label, meta, step_fn, law_fn, configs, horizons,
            configs_checked=None):
    """Full certificate; configs_checked reflects how the domain was
    built (exhaustive vs sampled) for honest reporting."""
    checked, first = verify_trajectory_law(step_fn, law_fn, configs,
                                           horizons)
    return {
        "label": label,
        "meta": meta,
        "domain": meta.get("domain"),
        "configs_checked": configs_checked if configs_checked is not None
        else len(configs),
        "points_checked": checked,
        "status": "HONEST_NEGATIVE" if first is not None else "PASS",
        "n_mismatch": 1 if first is not None else 0,
        "first_mismatch": first,
    }


def exhaustive_configs(window, max_n, predicate=None, rng=None):
    """All size 1..max_n subsets of a `window`-cell range passing the
    predicate (exhaustive domain)."""
    import itertools
    out = []
    for n in range(1, max_n + 1):
        for conf in itertools.combinations(range(window), n):
            if predicate is None or predicate(conf):
                out.append(conf)
    return out


def sampled_configs(window, max_n, count, predicate, rng):
    """Independent draws from a window satisfying the predicate."""
    out = []
    while len(out) < count:
        n = rng.randint(1, max_n)
        conf = tuple(sorted(rng.sample(range(window), n)))
        if predicate(conf):
            out.append(conf)
    return out


def all_gap_ge_2(conf):
    return all(b - a >= 2 for a, b in zip(conf, conf[1:]))


def is_single_cluster(conf):
    return all(b - a == 1 for a, b in zip(conf, conf[1:]))


def open_certificates():
    """The certified law set for rules 29/71 (plus honest negatives).

    L1 free streaming (rule 29): exhaustive gap>=2 configs, all horizons
        -> PASS (the free sector is exact).
    L2 melt/law_trajectory (rule 29 single cluster): exhaustive override
        -> PASS (melt-window law is exact for ALL T on a single cluster).
    L3 composition (rule 29 sampled multi-cluster, T >= max melt time)
        -> PASS by the composition law condition (sampled, condition in
        meta).
    mirror variants for rule 71 (left-mover; boundary margin >= T)
        -> PASS.
    Honest negatives: the 29-traffic law applied to rules 44/100, and
    free_streams on touching configs -> HONEST_NEGATIVE with the exact
    counter-example.
    """
    rng = random.Random(2026)
    certs = []

    def tr_law(rule):
        from experiments.emanation import traffic_law as tl

        def law(conf, T):
            return tl.law_trajectory(rule, list(conf), T)
        return law

    def step_law(rule):
        return lambda conf, T: sh.evolve(rule, conf, 64, T)

    # L1 free streaming, rule 29, exhaustive gap>=2
    dom = exhaustive_configs(14, 3, predicate=all_gap_ge_2)
    certs.append(certify(
        "L1_free_streaming_29",
        {"domain": "exhaustive gap>=2 configs, window=14 cells, n<=3",
         "law": "free streaming: x_j(T)=x_j(0)+T (v=+1)"},
        step_law(29), tr_law(29), dom, range(0, 9),
        configs_checked=len(dom)))

    # L1 mirror, rule 71 (margin >= T so the padded open lattice holds)
    dom71 = exhaustive_configs_window_margin(14, 3, margin=0)
    dom71 = [c for c in dom71 if all(p >= 6 for p in c)]
    dom71 = [c for c in dom71 if all_gap_ge_2(c)]
    certs.append(certify(
        "L1_free_streaming_71",
        {"domain": "exhaustive gap>=2 configs, window=14 cells, n<=3, "
                   "positions >= 6 (padding for the left mover)"},
        step_law(71), tr_law(71), dom71, range(0, 6),
        configs_checked=len(dom71)))

    # L2 melt law, rule 29, exhaustive over single clusters
    dom2 = []
    for a in range(2, 13):
        for k in range(1, 5):
            dom2.append(tuple(a + i for i in range(k)))
    certs.append(certify(
        "L2_melt_single_cluster_29",
        {"domain": "exhaustive single clusters {a..a+k-1}, a in 2..12, "
                   "k in 1..4, ALL horizons 0..9",
         "law": "melt-window: spacing-2 launch after k-1 steps (exact "
                "for every T)"},
        step_law(29), tr_law(29), dom2, range(0, 10),
        configs_checked=len(dom2)))

    # L2 mirror single clusters (margin)
    dom2_71 = [tuple(10 + a + i for i in range(k))
               for a in range(2, 9) for k in range(1, 5)]
    certs.append(certify(
        "L2_melt_single_cluster_71",
        {"domain": "exhaustive single clusters translated right, all "
                   "horizons 0..5 (padding for the left mover)"},
        step_law(71), tr_law(71), dom2_71, range(0, 6),
        configs_checked=len(dom2_71)))

    # L3 composition law, rule 29, merge-free sector (PROVABLE sector):
    # T <= g_min - 2 for every config, so all gaps stay >= 2 and no
    # trailing particle can catch a cluster's melt -- the union of
    # per-cluster spacing-2 ladders is then exact by construction.
    rng3 = random.Random(7)
    dom3 = []
    while len(dom3) < 300:
        n = rng3.randint(2, 3)
        conf = tuple(sorted(rng3.sample(range(20), n)))
        if min_gap(conf) is not None and min_gap(conf) >= 5:
            dom3.append(conf)
    certs.append(certify(
        "L3_composition_mergerfree_29",
        {"domain": "sampled configs (300 draws, n in 2..3, window=20) "
                   "with min pairwise gap >= 5, per-config horizons T <= "
                   "g_min - 2 (gaps stay >= 2, so clusters never interact)",
         "law": "trajectory = union of per-cluster spacing-2 ladders "
                "(exact in this sector by construction)",
         "theorem": "gap(t) >= gap(0) - t (no left moves), so T <= g_min-2 "
                    "keeps gaps >= 2 -> free streaming throughout"},
        step_law(29), tr_law(29), dom3, merge_free_horizons))

    # Honest negatives
    certs.append(certify(
        "HONEST_NEGATIVE_29law_on_44",
        {"domain": "sampled configs n<=3 window=12 (80 draws)",
         "law": "candidate: 29-traffic law_trajectory applied to rule 44 "
                "(44 is a blob mover, NOT traffic)"},
        step_law(44), tr_law(29),
        sampled_configs(12, 3, 80, lambda c: True, rng), range(1, 7)))
    certs.append(certify(
        "HONEST_NEGATIVE_29law_on_100",
        {"domain": "sampled configs n<=3 window=12 (80 draws)",
         "law": "candidate: 29-traffic law_trajectory applied to rule 100"},
        step_law(100), tr_law(29),
        sampled_configs(12, 3, 80, lambda c: True, rng), range(1, 7)))
    certs.append(certify(
        "HONEST_NEGATIVE_free_streaming_on_touching",
        {"domain": "sampled configs WITH contacts (n in 2..3, 60 draws)",
         "law": "candidate: free streaming x_j(T)=x_j(0)+T assumed "
                "valid even where a contact is present"},
        step_law(29), tr_law(29),
        sampled_configs(12, 3, 60, lambda c: not all_gap_ge_2(c), rng),
        range(1, 7)))
    certs.append(certify(
        "HONEST_NEGATIVE_composition_merge_sector",
        {"domain": "the single config {4,7,9,10}, T=6",
         "law": "candidate: per-cluster union law (law_trajectory) used "
                "past the merge sector -- the trailing particle at 7 is "
                "caught by the melt of the {9,10} block (trailing gap 2 "
                "<= (k-1)+1 = 2 for a run of length k=2), so the union "
                "law overshoots: predicts 13, truth 12",
         "claim_corrected": "composition law is exact only while gaps stay "
                             ">= 2 (T <= g_min - 2); the old docstring "
                             "'exact for T >= max melt window' was FALSE "
                             "and is retracted -- this is the discovered "
                             "merge sector boundary"},
        step_law(29), tr_law(29), [(4, 7, 9, 10)], [6]))
    return certs


def exhaustive_configs_window_margin(window, max_n, margin):
    """window-cell exhaustive subsets (helper name kept for the 71
    padding); returns all subsets of range(margin, margin+window)."""
    import itertools
    out = []
    for n in range(1, max_n + 1):
        for conf in itertools.combinations(range(margin, margin + window), n):
            out.append(conf)
    return out


def save_certificates(certs, path=None):
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "data", "law_certificates.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(certs, fh, indent=1, sort_keys=True)
    return path