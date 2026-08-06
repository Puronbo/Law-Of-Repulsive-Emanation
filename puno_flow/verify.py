"""Bit-exactness verification: the indexed path must equal brute force.

This is the testable guarantee the package is sold on: ExactIndex returns the
same k-NN sets as the all-pairs reference for any point set, and indexed flow
produces bit-identical trajectories to the exact path.
"""

import numpy as np

from .engine import FlowEngine
from .index import ExactIndex, brute_knn

__all__ = ["verify_exact"]


def verify_exact(pts, k=12, steps=5):
    """Prove indexed results equal brute force for the given points.

    Returns (ok, report) where report records each equality check:
      - grid k-NN == brute force (all points, sorted sets)
      - k-d tree k-NN == brute force (dim >= 4, when scipy is present)
      - indexed flow positions == exact all-pairs flow positions (bitwise)
    """
    X = np.asarray(pts, dtype=float)
    report = {}
    ok = True

    ref = brute_knn(X, k)
    grid = ExactIndex(X, k=k, algorithm="grid")
    g_eq = all(np.array_equal(a, b)
               for a, b in zip(grid.knn_all(k), ref))
    report["grid_knn_equals_bruteforce"] = bool(g_eq)
    ok = ok and g_eq

    t_eq = None
    if X.shape[1] >= 4:
        try:
            tree = ExactIndex(X, k=k, algorithm="kdtree")
            t_eq = all(np.array_equal(a, b)
                       for a, b in zip(tree.knn_all(k), ref))
        except ImportError:
            t_eq = None
        report["kdtree_knn_equals_bruteforce"] = t_eq
        if t_eq is not None:
            ok = ok and t_eq

    exact = FlowEngine(dim=X.shape[1], k=8, use_index=False,
                       index_min_n=2).add_many(X, X)
    indexed = FlowEngine(dim=X.shape[1], k=8, use_index=True,
                         index_min_n=2).add_many(X, X)
    exact.settle(steps)
    indexed.settle(steps)
    flow_eq = np.array_equal(exact.q, indexed.q)
    report["indexed_flow_bit_identical_to_exact"] = bool(flow_eq)
    ok = ok and flow_eq

    report["verdict"] = "PASS" if ok else "FAIL"
    return ok, report
