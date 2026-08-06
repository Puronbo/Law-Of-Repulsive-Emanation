"""puno_flow regression suite: the exactness guarantee is asserted, not claimed.

Run:  python -m pytest tests/test_puno_flow.py -q
"""

import numpy as np
import pytest

from puno_flow import ExactIndex, FlowEngine, brute_knn, verify_exact


def _pts(n, dim, seed, lo=-0.5, hi=0.5):
    return np.random.RandomState(seed).uniform(lo, hi, (n, dim))


@pytest.mark.parametrize("dim", [1, 2, 3])
@pytest.mark.parametrize("seed", [1, 2, 3])
def test_grid_knn_equals_bruteforce(dim, seed):
    X = _pts(1000, dim, seed)
    ref = brute_knn(X, 12)
    got = ExactIndex(X, k=12, algorithm="grid").knn_all(12)
    assert all(np.array_equal(a, b) for a, b in zip(got, ref))


def test_kdtree_knn_equals_bruteforce():
    pytest.importorskip("scipy.spatial")
    X = _pts(500, 64, 7)
    ref = brute_knn(X, 12)
    got = ExactIndex(X, k=12, algorithm="kdtree").knn_all(12)
    assert all(np.array_equal(a, b) for a, b in zip(got, ref))


def test_indexed_flow_bit_identical_to_exact_2d():
    X = _pts(2000, 2, 7)
    exact = FlowEngine(dim=2, k=8, use_index=False,
                       index_min_n=2).add_many(X, X)
    indexed = FlowEngine(dim=2, k=8, use_index=True,
                         index_min_n=2).add_many(X, X)
    exact.settle(10)
    indexed.settle(10)
    assert np.array_equal(exact.q, indexed.q)


def test_indexed_flow_bit_identical_to_exact_64d():
    pytest.importorskip("scipy.spatial")
    X = _pts(500, 64, 7)
    exact = FlowEngine(dim=64, k=8, use_index=False,
                       index_min_n=2).add_many(X, X)
    indexed = FlowEngine(dim=64, k=8, use_index=True,
                         index_min_n=2).add_many(X, X)
    exact.settle(5)
    indexed.settle(5)
    assert np.array_equal(exact.q, indexed.q)
    assert exact.spacing() == indexed.spacing()


def test_verify_exact_returns_pass():
    X = _pts(1000, 2, 1)
    ok, report = verify_exact(X, k=12, steps=5)
    assert ok
    assert report["verdict"] == "PASS"


def test_predict_equals_nearest_centroid():
    X = _pts(800, 3, 3)
    net = FlowEngine(dim=3, k=8, use_index=True,
                     index_min_n=2).add_many(X, X)
    net.settle(5)
    Q = _pts(200, 3, 9)
    idx = ExactIndex(net.q, k=8, algorithm="grid")
    assert np.array_equal(net.predict(Q), idx.nearest(Q))


def test_flow_stays_finite_and_bounded():
    X = _pts(1500, 2, 5)
    net = FlowEngine(dim=2, k=8, max_r=0.9, use_index=True,
                     index_min_n=2).add_many(X, X)
    net.settle(8)
    assert np.isfinite(net.q).all()
    assert np.all(np.linalg.norm(net.q, axis=1) <= 0.9 + 1e-12)


def test_damage_and_heal_keep_units():
    X = _pts(600, 2, 11)
    net = FlowEngine(dim=2, k=8, use_index=True,
                     index_min_n=2).add_many(X, X)
    net.settle(5)
    net.remove(list(range(150)))
    assert net.n == 450
    net.heal(8)
    assert net.n == 450
    assert np.isfinite(net.q).all()
