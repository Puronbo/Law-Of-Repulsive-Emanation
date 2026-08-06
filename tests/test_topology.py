"""Tests for the scale-free (Barabasi-Albert) topology and flow_over."""

import numpy as np
import pytest

from puno_flow import (
    FlowEngine,
    degree_sequence,
    hubs,
    power_law_exponent,
    preferential_attachment,
    topology_stats,
)


def test_preferential_attachment_shape_and_bounds():
    n, m = 500, 2
    edges = preferential_attachment(n, m, rng=np.random.RandomState(1))
    assert edges.ndim == 2 and edges.shape[1] == 2
    assert edges.min() >= 0 and edges.max() < n
    assert not np.any(edges[:, 0] == edges[:, 1])          # no self-loops


def test_ba_has_heavy_tail():
    edges = preferential_attachment(3000, 2, rng=np.random.RandomState(2))
    stats = topology_stats(edges, 3000)
    assert stats["max_degree"] > 3.0 * stats["mean_degree"]
    # a substantial share of nodes stay at the minimum degree (m = 2)
    deg = degree_sequence(edges, 3000)
    assert np.mean(deg == 2) > 0.1


def test_power_law_exponent_of_ba_is_around_three():
    edges = preferential_attachment(8000, 2, rng=np.random.RandomState(3))
    deg = degree_sequence(edges, 8000)
    gamma = power_law_exponent(deg, xmin=int(deg.min()))
    assert 2.0 <= gamma <= 3.6


def test_hubs_are_the_top_degree_nodes():
    edges = preferential_attachment(400, 3, rng=np.random.RandomState(4))
    deg = degree_sequence(edges, 400)
    h, d = hubs(edges, 400, k=5)
    assert h.shape == (5,)
    assert list(d) == sorted(deg.tolist(), reverse=True)[:5]


def test_power_law_exponent_needs_data():
    assert np.isnan(power_law_exponent(np.array([1])))


def test_flow_over_runs_finite_and_bounded():
    rng = np.random.RandomState(5)
    homes = rng.uniform(-0.5, 0.5, (300, 2))
    net = FlowEngine(dim=2, k=8).add_many(homes)
    edges = preferential_attachment(300, 2, rng=rng)
    net.flow_over(edges, steps=20)
    assert np.isfinite(net.q).all()
    assert np.linalg.norm(net.q, axis=-1).max() <= 0.9 + 1e-9


def test_flow_over_record_chains_every_step():
    rng = np.random.RandomState(6)
    homes = rng.uniform(-0.5, 0.5, (120, 2))
    net = FlowEngine(dim=2, k=8).add_many(homes)
    edges = preferential_attachment(120, 2, rng=rng)
    net.flow_over(edges, steps=10, record=True)
    assert net.verify_ledger() == (True, None, None)
    assert net.ledger_audit()["blocks"] == 120 * (1 + 10)  # genesis + steps


def test_flow_over_isolated_node_drifts_to_home():
    net = FlowEngine(dim=2, k=2).add_many(
        np.array([[0.0, 0.0], [0.0, 0.8], [0.1, 0.1]]))
    edges = np.array([[0, 1]])            # node 2 is isolated
    net.flow_over(edges, mu=0.0, steps=50)
    assert np.isfinite(net.q).all()
    # an isolated node feels only its home tether; it starts at home and
    # the tether is zero there, so it stays put (well inside the rim)
    assert np.linalg.norm(net.q[2] - net.h[2]) < 1e-9


def test_flow_over_accepts_out_of_range_edges_safely():
    net = FlowEngine(dim=2, k=2).add_many(
        np.array([[0.0, 0.0], [1.0, 0.0]]))
    net.flow_over(np.array([[0, 1], [5, 6]]), steps=5)
    assert np.isfinite(net.q).all()
