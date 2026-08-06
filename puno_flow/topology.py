"""Scale-free networks for the toy network.

A scale-free network has a power-law degree distribution: a few hubs carry
most of the links while most nodes are sparsely connected.  The canonical
generator is Barabasi-Albert preferential attachment (a new node attaches to
m existing nodes chosen with probability proportional to their current
degree), which yields P(k) ~ k^-3 in the large-n limit.

Everything here is numpy + stdlib.  The generated edge list can be wired into
FlowEngine.flow_over so the local-only balance dynamics run over hubs and
spokes instead of uniform k-NN neighbourhoods.
"""

import numpy as np

__all__ = [
    "preferential_attachment",
    "degree_sequence",
    "power_law_exponent",
    "hubs",
    "topology_stats",
]


def preferential_attachment(n, m=2, rng=None):
    """Barabasi-Albert preferential attachment.

    Builds an undirected network of n nodes; each new node attaches to m
    existing nodes with probability proportional to their current degree.
    Returns an (E, 2) int array of edges (both orientations implied).
    """
    rng = np.random.RandomState(7) if rng is None else rng
    if n < 2 or m < 1:
        raise ValueError("need n >= 2 and m >= 1")
    if m >= n:
        raise ValueError("m must be < n")
    base = m + 1
    edges = []
    for i in range(base):
        for j in range(i + 1, base):
            edges.append((i, j))
    pool = list(range(base)) * m
    for new in range(base, n):
        targets = set()
        while len(targets) < m:
            targets.add(pool[rng.randint(len(pool))])
        for t in targets:
            edges.append((new, t))
            pool.append(new)
            pool.append(t)
    return np.asarray(edges, dtype=int)


def degree_sequence(edges, n):
    """Per-node degree from an (E, 2) undirected edge list."""
    edges = np.asarray(edges, dtype=int)
    return np.bincount(edges.ravel(), minlength=n)


def _hurwitz_zeta(s, a, kmax=2000):
    """zeta(s, a) = sum_{k>=0} (k+a)^{-s} via Euler-Maclaurin (integral tail
    + half-term).  Accurate to ~1e-9 relative for s >= 1.5, good enough for
    exponent fitting."""
    total = 0.0
    for k in range(kmax):
        total += (k + a) ** (-s)
    u = kmax + a
    total += u ** (1.0 - s) / (s - 1.0) + 0.5 * u ** (-s)
    return total


def _zeta_logsum(s, a, kmax=2000):
    """sum_{k>=0} (k+a)^{-s} * ln(k+a) = -zeta'(s, a), Euler-Maclaurin."""
    total = 0.0
    for k in range(kmax):
        u = k + a
        total += u ** (-s) * np.log(u)
    u = kmax + a
    total += (u ** (1.0 - s) * (np.log(u) / (s - 1.0) + 1.0 / (s - 1.0) ** 2)
              + 0.5 * u ** (-s) * np.log(u))
    return total


def power_law_exponent(degrees, xmin=1):
    """Discrete maximum-likelihood exponent gamma for P(k) ~ k^-gamma
    (Clauset-Shalizi-Newman discrete estimator, solved by bisection).
    NaN if there is not enough data above xmin."""
    deg = np.asarray(degrees, dtype=float)
    deg = deg[deg >= xmin]
    if len(deg) < 2:
        return float("nan")
    xmin = float(xmin)
    lmean = float(np.mean(np.log(deg)))

    def f(gamma):
        z = _hurwitz_zeta(gamma, xmin)
        return -_zeta_logsum(gamma, xmin) / z + lmean

    lo, hi = 1.1, 20.0
    if f(lo) > 0.0:
        return float("nan")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def hubs(edges, n, k=10):
    """The k highest-degree nodes: (indices, degrees), descending."""
    deg = degree_sequence(edges, n)
    order = np.argsort(deg)[::-1][:k]
    return order, deg[order]


def topology_stats(edges, n):
    """Summary: size, mean/max degree, fitted exponent, heavy-tail check."""
    deg = degree_sequence(edges, n)
    mean = float(deg.mean())
    mx = int(deg.max())
    return {
        "nodes": n,
        "edges": len(np.asarray(edges)),
        "mean_degree": mean,
        "max_degree": mx,
        "gamma": power_law_exponent(deg, xmin=max(1, int(deg.min()))),
        "heavy_tail": mx > 3.0 * mean,
    }
