"""Tests for the toy-network extras: ledgers (blockchain), creation,
search-engine API, and local agreement (consensus)."""

import numpy as np
import pytest

from puno_flow import (
    ChainStore,
    FlowEngine,
    LedgerChain,
    brute_knn,
    pack_indices,
    pack_state,
    sha256,
)


def test_block_hash_is_content_addressed():
    assert sha256(b"a") != sha256(b"b")
    c = LedgerChain()
    h1 = c.append(b"first")
    h2 = c.append(b"second")
    assert h1 != h2
    assert c.head == h2
    assert c.length == 2
    assert c.verify() == (True, None)


def test_ledger_tamper_detected():
    c = LedgerChain(b"genesis")
    c.append(b"one")
    c.append(b"two")
    assert c.verify() == (True, None)
    c.blocks[1]["payload"] = b"ONE"
    ok, bad = c.verify()
    assert ok is False
    assert bad == 1


def test_chain_store_verify_all():
    store = ChainStore()
    store.genesis(0, pack_state([0.0, 0.0]))
    store.record(0, pack_state([0.1, 0.1]) + pack_indices([1, 2]))
    store.genesis(1, pack_state([1.0, 1.0]))
    assert store.verify_all() == (True, None, None)
    assert store.length(0) == 2
    store.chains[0].blocks[0]["payload"] = pack_state([9.0, 9.0])
    assert store.verify_all()[0] is False


def test_create_adds_unit_with_genesis():
    net = FlowEngine(dim=2, k=2)
    idx = net.create(np.array([0.1, 0.2]))
    assert idx == 0
    assert net.n == 1
    assert net.chain_head(0) is not None
    assert net.verify_ledger() == (True, None, None)
    assert net.ledger_audit()["chains"] == 1
    assert net.ledger_audit()["blocks"] == 1


def test_create_with_parent_chain_provenance():
    net = FlowEngine(dim=2, k=2)
    net.create(np.array([0.0, 0.0]))
    idx = net.create(np.array([0.3, 0.3]), parent=0)
    assert idx == 1
    assert net.verify_ledger() == (True, None, None)


def test_spawn_creates_units_around_homes():
    net = FlowEngine(dim=2, k=3).add_many(np.array([[0.0, 0.0]]))
    created = net.spawn(5, spread=0.01, rng=np.random.RandomState(3))
    assert len(created) == 5
    assert net.n == 6
    assert net.verify_ledger() == (True, None, None)
    assert net.ledger_audit()["chains"] == 6


def test_search_returns_ranked_hits():
    net = FlowEngine(dim=2, k=4).add_many(
        np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [2.0, 2.0]]))
    hits, dist = net.search(np.array([0.0, 0.0]))
    assert hits[0] == 0
    assert dist[0] == pytest.approx(0.0)
    assert len(hits) == 4
    assert all(np.diff(dist) >= 0)


def test_search_batch():
    net = FlowEngine(dim=2, k=2).add_many(
        np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]))
    q = np.array([[0.0, 0.0], [1.1, 1.0]])
    hits, dist = net.search(q)
    assert hits.shape == (2, 2)
    assert hits[0, 0] == 0
    assert hits[1, 0] == 1


def test_search_by_identity():
    homes = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    net = FlowEngine(dim=2, k=2).add_many(homes)
    hits, dist = net.search_by_identity(np.array([1.05, 0.0]))
    assert hits[0] == 1
    assert dist[0] == pytest.approx(0.05)


def test_consensus_perfect_reciprocity():
    net = FlowEngine(dim=2, k=1).add_many(
        np.array([[0.0, 0.0], [1.0, 0.0]]))
    assert net.consensus() == pytest.approx(1.0)


def test_consensus_reflects_mutuality():
    rng = np.random.RandomState(5)
    X = rng.uniform(-1.0, 1.0, (100, 2))
    net = FlowEngine(dim=2, k=8).add_many(X)
    c = net.consensus()
    assert 0.0 < c <= 1.0
    nb = brute_knn(net.q, 8)
    manual = 0
    total = 0
    for i in range(100):
        for j in nb[i]:
            total += 1
            if i in nb[j]:
                manual += 1
    assert c == pytest.approx(manual / total)


def test_flow_record_builds_chains_without_changing_trajectory():
    rng = np.random.RandomState(2)
    X = rng.uniform(-0.5, 0.5, (200, 2))
    a = FlowEngine(dim=2, k=8).add_many(X)
    b = FlowEngine(dim=2, k=8).add_many(X)
    a.settle(3)
    b.settle(3, record=True)
    assert np.array_equal(a.q, b.q)
    assert b.ledger_audit()["chains"] == 200
    assert b.ledger_audit()["blocks"] == 200 * 4  # genesis + 3 recorded steps
    assert b.verify_ledger() == (True, None, None)
    assert a.ledger_audit()["chains"] == 200      # genesis only
    assert a.ledger_audit()["blocks"] == 200


def test_flow_record_heads_advance_per_step():
    rng = np.random.RandomState(2)
    X = rng.uniform(-0.5, 0.5, (50, 2))
    net = FlowEngine(dim=2, k=8).add_many(X)
    head0 = net.chain_head(0)
    net.settle(1, record=True)
    head1 = net.chain_head(0)
    net.settle(1, record=True)
    head2 = net.chain_head(0)
    assert head0 is not None               # genesis block at birth
    assert len({head0, head1, head2}) == 3
    assert net.verify_ledger() == (True, None, None)


def test_status_snapshot():
    net = FlowEngine(dim=2, k=4).add_many(
        np.array([[0.0, 0.0], [1.0, 0.0]]))
    s = net.status()
    assert s["n"] == 2
    assert s["dim"] == 2
    assert s["consensus"] == pytest.approx(1.0)
    assert s["ledger_chains"] == 2
    assert s["ledger_blocks"] == 2
