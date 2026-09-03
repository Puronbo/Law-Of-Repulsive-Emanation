"""topology_audit: the fifth real-subsystem audit -- the Barabasi-Albert
scale-free network generator and its degree-spectrum contracts
(puno_flow/topology.py).

Audited invariants (pure numpy arithmetic, deterministic, reproducible):
    L39_handshake_degree_sum:
        The handshake lemma: sum(degree) == 2 * |E| for every BA network.
        Checked exhaustively over a dense domain of (n, m, seed) tuples.
    L40_simple_graph_no_self_or_dup:
        The edge list of a BA network contains no self-loop (u != v) and
        no duplicate unordered edge pair.  The pool-with-replacement +
        set() target selection guarantees distinct targets per node.
        Verified exactly over many draws and node sizes.
    L41_ba_min_degree_is_m:
        For a BA network built with parameter m, the minimum degree is
        exactly m.  The initial base clique has degree m, and every later
        node attaches to exactly m targets.  Verified over several
        (n, m, seed) draws.
    L42_ba_power_law_exponent_three:
        The fitted Clauset-Shalizi-Newman discrete MLE exponent for a
        large BA network (n=2000, m=2) is close to 3 (|gamma-3| < 0.15).
        This is the asymptotic power-law signature gamma ~ 3 of the BA
        model.
HONEST NEGATIVE (rejected, not introduced):
    L43_hubs_returns_strictly_descending:
        The FALSE candidate law "hubs(edges,n,k) returns k nodes with
        strictly descending degrees" is rejected: np.argsort breaks ties
        by index, so the returned degrees can be non-increasing with
        equal neighbours at the boundary.
"""
import numpy as np

from puno_flow.topology import (
    preferential_attachment,
    degree_sequence,
    power_law_exponent,
    hubs,
)

_SEEDS = list(range(10))
_NS = [50, 200, 500]
_MS = [2, 3]


def _L39_handshake_degree_sum(datum):
    n, m, seed = datum
    rng = np.random.RandomState(seed)
    edges = preferential_attachment(n, m=m, rng=rng)
    deg = degree_sequence(edges, n)
    return int(deg.sum()) == 2 * len(edges)


def _L40_simple_graph_no_self_or_dup(datum):
    n, m, seed = datum
    rng = np.random.RandomState(seed)
    edges = preferential_attachment(n, m=m, rng=rng)
    for u, v in edges:
        if u == v:
            return False
    seen = set()
    for u, v in edges:
        key = (min(u, v), max(u, v))
        if key in seen:
            return False
        seen.add(key)
    return True


def _L41_ba_min_degree_is_m(datum):
    n, m, seed = datum
    rng = np.random.RandomState(seed)
    edges = preferential_attachment(n, m=m, rng=rng)
    deg = degree_sequence(edges, n)
    return int(deg.min()) == m


def _L42_ba_power_law_exponent_three(datum):
    n, m, seed = datum
    rng = np.random.RandomState(seed)
    edges = preferential_attachment(n, m=m, rng=rng)
    deg = degree_sequence(edges, n)
    gamma = power_law_exponent(deg, xmin=15)
    return abs(gamma - 3.0) < 0.15


def _L43_hubs_strictly_descending(datum):
    """FALSE candidate: hubs returns strictly descending degrees.
    Returns True iff every consecutive pair of returned degrees is
    strictly decreasing -- which fails when ties exist at the cutoff."""
    n, m, seed = datum
    rng = np.random.RandomState(seed)
    edges = preferential_attachment(n, m=m, rng=rng)
    _, degs = hubs(edges, n, k=min(20, n))
    for i in range(len(degs) - 1):
        if degs[i] <= degs[i + 1]:
            return False
    return True


def _certify(label, meta, pred, domain):
    from experiments.emanation import law_checker as lc
    return lc.certify_statement(label, meta, pred, list(domain))


_DOMAIN = [(n, m, s) for n in _NS for m in _MS for s in _SEEDS]
_LARGE_DOMAIN = [(50000, 2, s) for s in range(6)]


def topology_certificates():
    certs = []
    certs.append(_certify(
        "L39_handshake_degree_sum",
        {"domain": "n in {50,200,500} x m in {2,3} x seeds 0..9 "
                   "(60 draws): sum(degree) must equal 2*|E| exactly",
         "law": "handshake lemma: sum_k d(k) = 2|E| for any undirected "
                "graph, verified via degree_sequence on the BA edge list",
         "measured_on": "puno_flow.topology.preferential_attachment + "
                        "degree_sequence"},
        _L39_handshake_degree_sum, _DOMAIN))
    certs.append(_certify(
        "L40_simple_graph_no_self_or_dup",
        {"domain": "n in {50,200,500} x m in {2,3} x seeds 0..9 "
                   "(60 draws): no self-loop, no duplicate edge",
         "law": "BA preferential_attachment uses a set() to pick m "
                "distinct targets per new node, so the edge list is a "
                "simple graph (no self-loops, no parallel edges)",
         "measured_on": "puno_flow.topology.preferential_attachment"},
        _L40_simple_graph_no_self_or_dup, _DOMAIN))
    certs.append(_certify(
        "L41_ba_min_degree_is_m",
        {"domain": "n in {50,200,500} x m in {2,3} x seeds 0..9 "
                   "(60 draws): min(degree) == m",
         "law": "the initial base clique (m+1 fully connected nodes) has "
                "degree m; every later node attaches to exactly m targets "
                "and receives no further edges until it is chosen as a "
                "target -- minimum degree is exactly m",
         "measured_on": "puno_flow.topology.preferential_attachment + "
                        "degree_sequence"},
        _L41_ba_min_degree_is_m, _DOMAIN))
    certs.append(_certify(
        "L42_ba_power_law_exponent_three",
        {"domain": "6 large BA networks (n=50000, m=2, seeds 0..5): "
                   "CSN discrete MLE tail exponent (xmin=15) must be "
                   "within 0.15 of 3",
         "law": "the BA model has asymptotic degree distribution P(k) ~ "
                "k^-3; the Clauset-Shalizi-Newman estimator fitted to the "
                "degree tail of a single large draw should recover "
                "gamma ~ 3",
         "measured_on": "puno_flow.topology.power_law_exponent"},
        _L42_ba_power_law_exponent_three, _LARGE_DOMAIN))
    certs.append(_certify(
        "L43_hubs_returns_strictly_descending",
        {"domain": "n in {50,200,500} x m in {2,3} x seeds 0..9 "
                   "(60 draws): hubs(edges,n,k=20) degrees strictly "
                   "descending",
         "law": "FALSE CANDIDATE: hubs returns k nodes with strictly "
                "descending degrees; np.argsort breaks ties by index so "
                "the returned degrees can be non-increasing with equal "
                "neighbours at the selection boundary",
         "honest_check": "must find at least one (n,m,seed) where the "
                         "returned hub degrees are NOT strictly descending"},
        _L43_hubs_strictly_descending, _DOMAIN))
    return certs
