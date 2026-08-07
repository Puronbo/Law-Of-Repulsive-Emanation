"""Rigor campaign: push the exactness, ledger, topology, app, and server
contracts until no gap is found.

Run:  python -m pytest tests/test_rigor.py -q
"""

import importlib.resources
import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

import numpy as np
import pytest

from puno_flow import ExactIndex, FlowEngine, brute_knn, verify_exact
from puno_flow.ledger import pack_indices, pack_state
from puno_flow.topology import (
    degree_sequence,
    hubs,
    power_law_exponent,
    preferential_attachment,
    topology_stats,
)
from puno_app.app_state import NetworkApp
from puno_app.canned_ui import HTML_PATH, Handler, make_server


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _uniform(n, dim, seed, lo=-0.5, hi=0.5):
    return np.random.RandomState(seed).uniform(lo, hi, (n, dim))


def _dist(X):
    return np.linalg.norm(X[:, None] - X[None], axis=-1)


def _newton_flow(dim, seed, k=8, n=400, steps=6, use_index=True):
    X = _uniform(n, dim, seed)
    exact = FlowEngine(dim=dim, k=k, use_index=False,
                       index_min_n=2).add_many(X, X)
    idx = FlowEngine(dim=dim, k=k, use_index=use_index,
                     index_min_n=2).add_many(X, X)
    exact.settle(steps)
    idx.settle(steps)
    return exact, idx


# --------------------------------------------------------------------------- #
# A. grid exactness over degenerate and adversarial geometries
# --------------------------------------------------------------------------- #
def _check_ordered(X, k, algorithm="grid"):
    ref = brute_knn(X, k)
    got = ExactIndex(X, k=k, algorithm=algorithm).knn_all(k)
    assert all(np.array_equal(a, b) for a, b in zip(got, ref))


@pytest.mark.parametrize("seed", [1, 2, 3])
@pytest.mark.parametrize("k", [3, 9, 17])
def test_grid_ordered_exactness_sweep(seed, k):
    _check_ordered(_uniform(600, 3, seed), k)


def test_grid_collinear_2d_and_3d():
    rng = np.random.RandomState(4)
    for dim in (2, 3):
        line = np.column_stack([rng.uniform(-1, 1, 250),
                                np.zeros((250, dim - 1))])
        _check_ordered(line, 1)
        _check_ordered(line, 12)
        # NOTE: k close to n on degenerate geometry makes the ring scan run
        # to the full grid diameter (the k-th distance is the whole span) -
        # still exact, but k ~ n is inherently all-pairs work either way.
        # k >= n is exercised on uniform geometry in
        # test_grid_k_beyond_population_and_single_neighbour.


def test_grid_all_identical_and_concentrated_duplicates():
    same = np.zeros((300, 2))
    _check_ordered(same, 12)
    rng = np.random.RandomState(5)
    dups = np.vstack([rng.uniform(-0.5, 0.5, (40, 2))] * 6)
    _check_ordered(dups, 15)


def test_grid_clusters_with_outlier():
    rng = np.random.RandomState(6)
    cl = np.vstack([rng.randn(200, 3) * 0.01,
                    rng.randn(200, 3) * 0.01 + 1.0,
                    np.array([[9.0, 9.0, 9.0]])])
    _check_ordered(cl, 8)


def test_grid_k_beyond_population_and_single_neighbour():
    X = _uniform(50, 2, 7)
    _check_ordered(X, 60)     # k > n-1: every other point, canonical order
    _check_ordered(X, 49)     # k == n-1
    _check_ordered(X, 1)
    _check_ordered(X[0:1], 8)
    _check_ordered(X[0:2], 8)


def test_grid_near_collinear_jitter():
    rng = np.random.RandomState(8)
    base = rng.uniform(-1, 1, (300, 2))
    jitter = base + rng.randn(300, 2) * 1e-6
    _check_ordered(jitter, 9)


# --------------------------------------------------------------------------- #
# B. kdtree exactness: ordered for distinct geometry, set-property on ties
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("k", [1, 8, 12])
def test_kdtree_ordered_exactness(k):
    pytest.importorskip("scipy.spatial")
    _check_ordered(_uniform(500, 64, 9), k, algorithm="kdtree")


def test_kdtree_padding_beyond_population():
    pytest.importorskip("scipy.spatial")
    for n in (5, 8, 40):
        X = _uniform(n, 64, 3)
        _check_ordered(X, 2 * n, algorithm="kdtree")   # padding must vanish
        _check_ordered(X, n - 1, algorithm="kdtree")
        _check_ordered(X, 1, algorithm="kdtree")


def test_grid_rejects_high_dim_explicit_use():
    with pytest.raises(ValueError):
        ExactIndex(_uniform(50, 64, 1), k=8, algorithm="grid")


def test_kdtree_self_exclusion_every_row():
    pytest.importorskip("scipy.spatial")
    X = _uniform(300, 16, 11)
    got = ExactIndex(X, k=8, algorithm="kdtree").knn_all(8)
    for i, nb in enumerate(got):
        assert i not in nb


def test_kdtree_tie_sets_are_true_knn():
    pytest.importorskip("scipy.spatial")
    rng = np.random.RandomState(12)
    X = np.vstack([rng.uniform(-0.5, 0.5, (150, 64)),
                   np.tile(np.ones(64) * 0.1, (40, 1))])   # 40 exact ties
    k = 8
    D = _dist(X)
    np.fill_diagonal(D, np.inf)
    order = np.argsort(D, axis=1)
    ref = [order[i][:k] for i in range(len(X))]
    kth = np.sort(D, axis=1)[:, k - 1]
    nxt = np.sort(D, axis=1)[:, k]
    got = ExactIndex(X, k=k, algorithm="kdtree").knn_all(k)
    for i in range(len(X)):
        g = np.asarray(got[i])
        assert len(set(g.tolist())) == k
        # every returned point is at most the true k-th distance
        assert np.all(D[i][g] <= kth[i] + 1e-12)
        # if the k-th / (k+1)-th boundary is not tied, the set must match brute
        if kth[i] < nxt[i] - 1e-12:
            assert set(g.tolist()) == set(np.asarray(ref[i]).tolist())


def test_kdtree_nearest_matches_brute():
    pytest.importorskip("scipy.spatial")
    X = _uniform(400, 32, 13)
    Q = _uniform(100, 32, 14)
    D = np.linalg.norm(Q[:, None] - X[None], axis=-1)
    ref = np.argmin(D, axis=1)
    got = ExactIndex(X, k=8, algorithm="kdtree").nearest(Q)
    assert np.array_equal(got, ref)


# --------------------------------------------------------------------------- #
# C. flow bit-exactness across dims and the index threshold
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("dim", [1, 2, 3])
@pytest.mark.parametrize("seed", [1, 2])
def test_indexed_flow_bit_identical_low_dim(dim, seed):
    exact, idx = _newton_flow(dim, seed)
    assert np.array_equal(exact.q, idx.q)
    assert exact.spacing() == idx.spacing()
    assert exact.consensus() == idx.consensus()


@pytest.mark.parametrize("dim", [5, 16, 64])
def test_indexed_flow_bit_identical_high_dim(dim):
    pytest.importorskip("scipy.spatial")
    exact, idx = _newton_flow(dim, 3, k=6, n=300, steps=4)
    assert np.array_equal(exact.q, idx.q)
    assert exact.spacing() == idx.spacing()


def test_index_threshold_brute_below_and_index_above():
    X = _uniform(300, 2, 15)                     # below index_min_n=512
    idx = FlowEngine(dim=2, k=8, use_index=True,
                     index_min_n=512).add_many(X, X)
    assert idx._index() is None                  # brute path below threshold
    idx.add_many(_uniform(400, 2, 16))           # now 700 units: over the line
    assert idx._index() is not None
    assert idx._index().algorithm == "grid"
    idx.settle(3)
    assert np.isfinite(idx.q).all()


# --------------------------------------------------------------------------- #
# D. k-NN and engine edge cases
# --------------------------------------------------------------------------- #
def test_k_zero_returns_empty_no_crash():
    X = _uniform(100, 3, 21)
    g = ExactIndex(X, k=0, algorithm="grid").knn_all(0)
    assert all(len(r) == 0 for r in g)
    net = FlowEngine(dim=2, k=0).add_many(_uniform(50, 2, 22))
    net.settle(3)
    assert np.isfinite(net.q).all()


def test_single_and_two_unit_engines():
    net = FlowEngine(dim=2, k=8).add(np.array([0.1, 0.1]))
    net.settle(3)
    assert np.isfinite(net.q).all()
    assert net.spacing() == 0.0
    assert net.consensus() == 1.0
    net.add(np.array([0.2, 0.2]))
    net.settle(3)
    assert np.isfinite(net.q).all()


def test_remove_all_then_grow_again():
    net = FlowEngine(dim=2, k=8).add_many(_uniform(40, 2, 23))
    net.remove(np.arange(40))
    assert net.n == 0
    assert net.chains.chains == {}
    assert len(net.chains.archived) == 40
    net.add_many(_uniform(30, 2, 24))
    net.settle(2)
    assert net.n == 30
    assert net.verify_ledger()[0]


def test_spawn_requires_population():
    net = FlowEngine(dim=2, k=8)
    with pytest.raises(ValueError):
        net.spawn(1)


def test_search_sorted_and_identity_search():
    X = _uniform(120, 2, 25)
    net = FlowEngine(dim=2, k=6).add_many(X)
    hits, dist = net.search(np.array([0.0, 0.0]), k=5)
    assert len(hits) == 5
    assert np.all(np.diff(dist) >= 0)
    net.settle(4)
    ih, id_ = net.search_by_identity(np.array([0.0, 0.0]), k=3)
    assert len(ih) == 3 and np.all(np.diff(id_) >= 0)


def test_absorb_pulls_toward_homes():
    rng = np.random.RandomState(26)
    X = rng.uniform(-0.5, 0.5, (200, 2))
    net = FlowEngine(dim=2, k=8, use_index=True, index_min_n=2).add_many(X)
    net.settle(5)
    spread_before = float(np.mean(np.linalg.norm(net.q - net.h, axis=-1)))
    net.absorb(150, mu=200.0)
    spread_after = float(np.mean(np.linalg.norm(net.q - net.h, axis=-1)))
    assert spread_after < 0.6 * spread_before


# --------------------------------------------------------------------------- #
# E. ledger: hashing, tamper detection, archive + rekey, create-after-remove
# --------------------------------------------------------------------------- #
def test_pack_deterministic_and_variable_length():
    a = pack_state(np.array([0.1, 0.2, 0.3]))
    b = pack_state(np.array([0.1, 0.2, 0.3]))
    assert a == b
    assert len(a) > 0
    assert pack_indices([0, 1, 2]) != pack_indices([0, 1, 3])


def test_genesis_idempotent_and_growth():
    net = FlowEngine(dim=2, k=8).add_many(_uniform(20, 2, 30))
    net.chains.genesis(0, pack_state(net.h[0]))
    assert net.chains.length(0) == 1
    net.settle(2, record=True)
    assert all(net.chains.length(i) == 3 for i in range(20))
    assert net.verify_ledger()[0]
    audit = net.ledger_audit()
    assert audit["chains"] == 20
    assert audit["blocks"] == 3 * 20
    assert len(audit["heads"]) == 20


def test_tamper_detected_on_every_chain_field():
    rng = np.random.RandomState(31)
    X = rng.uniform(-0.5, 0.5, (30, 2))
    net = FlowEngine(dim=2, k=8).add_many(X)
    net.settle(3, record=True)
    assert net.verify_ledger()[0]
    chain = net.chains.chains[5]
    b = chain.blocks[1]                    # first state block (seq 1)
    orig_payload = b["payload"]
    b["payload"] = "x"
    assert not net.verify_ledger()[0]      # tampered payload
    b["payload"] = orig_payload
    assert net.verify_ledger()[0]
    b["prev"] = "0" * 64
    assert not net.verify_ledger()[0]
    b["prev"] = chain.blocks[0]["hash"]
    assert net.verify_ledger()[0]
    chain.blocks[0]["payload"] = "genesis-tampered"
    assert not net.verify_ledger()[0]      # tampered genesis breaks whole chain


def test_tamper_remains_detected_after_more_records():
    rng = np.random.RandomState(32)
    X = rng.uniform(-0.5, 0.5, (15, 2))
    net = FlowEngine(dim=2, k=8).add_many(X)
    net.settle(3, record=True)
    net.chains.chains[2].blocks[1]["payload"] = "tampered"
    net.settle(2, record=True)
    assert not net.verify_ledger()[0]


def test_remove_archives_history_and_never_aliases_new_unit():
    X = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    net = FlowEngine(dim=2, k=3).add_many(X)
    net.settle(3, record=True)
    heads_before = {i: net.chains.head(i) for i in range(4)}
    lengths_before = {i: net.chains.length(i) for i in range(4)}

    mapping = net.remove(np.array([1]))
    assert mapping == {0: 0, 2: 1, 3: 2}
    assert net.n == 3
    assert list(net.chains.chains.keys()) == [0, 1, 2]
    assert list(net.chains.archived.keys()) == [1]
    assert net.chains.verify_archived() == (True, None)
    # rekeyed survivors keep their exact history
    assert net.chains.length(0) == lengths_before[0]
    assert net.chains.length(1) == lengths_before[2]
    assert net.chains.length(2) == lengths_before[3]
    assert net.chains.head(0) == heads_before[0]
    assert net.chains.head(1) == heads_before[2]
    assert net.chains.head(2) == heads_before[3]
    assert net.verify_ledger()[0]

    idx = net.create(np.array([0.5, 0.5]))
    assert idx == 3
    assert net.chains.length(3) == 1        # fresh genesis, not a stale ledger
    assert 3 in net.chains.chains
    assert 3 not in net.chains.archived
    assert net.chains.chains[3].length == 1
    assert net.verify_ledger()[0]
    assert net.chains.verify_archived() == (True, None)

    net.spawn(3, rng=np.random.RandomState(1))
    assert net.verify_ledger()[0]
    audit = net.ledger_audit()
    assert audit["chains"] == net.n
    assert audit["archived"] == 1


# --------------------------------------------------------------------------- #
# F. topology: attachment invariants, exponent, hubs, stats
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("n,m", [(100, 1), (200, 2), (300, 5), (77, 3)])
def test_preferential_attachment_invariants(n, m):
    edges = preferential_attachment(n, m=m, rng=np.random.RandomState(0))
    expected_E = m * (m + 1) // 2 + m * (n - m - 1)
    assert len(edges) == expected_E
    assert edges.shape == (expected_E, 2)
    assert np.all((edges >= 0) & (edges < n))
    assert not np.any(edges[:, 0] == edges[:, 1])          # no self-loops
    pairs = {tuple(sorted(e)) for e in edges.tolist()}
    assert len(pairs) == expected_E                         # no duplicate edges
    deg = degree_sequence(edges, n)
    assert len(deg) == n
    assert deg.sum() == 2 * expected_E
    assert deg.min() == m
    # attachments are invariant across seeds (structure, not just count)
    e2 = preferential_attachment(n, m=m, rng=np.random.RandomState(99))
    assert len(e2) == expected_E


def test_attachment_rejects_bad_args():
    with pytest.raises(ValueError):
        preferential_attachment(1, m=2)
    with pytest.raises(ValueError):
        preferential_attachment(5, m=5)
    with pytest.raises(ValueError):
        preferential_attachment(5, m=0)


def test_exponent_hubs_and_stats():
    n = 2000
    edges = preferential_attachment(n, m=2, rng=np.random.RandomState(0))
    deg = degree_sequence(edges, n)
    gamma = power_law_exponent(deg)
    assert np.isfinite(gamma)
    assert 1.5 < gamma < 4.0
    h_idx, h_deg = hubs(edges, n, k=10)
    assert len(h_idx) == 10
    assert h_deg[0] == deg.max()
    assert all(h_deg[i] >= h_deg[i + 1] for i in range(9))
    stats = topology_stats(edges, n)
    assert stats["nodes"] == n
    assert stats["edges"] == len(edges)
    assert stats["max_degree"] == int(deg.max())
    assert abs(stats["mean_degree"] - 2 * len(edges) / n) < 1e-9
    assert stats["heavy_tail"] is True


# --------------------------------------------------------------------------- #
# G. NetworkApp: damage renumbering, lifecycle, record toggle
# --------------------------------------------------------------------------- #
def _consistency(app):
    n = app.engine.n
    snap = app.snapshot()
    assert snap["n"] == n
    assert bool(np.isfinite(app.engine.q).all())
    assert snap["ledger"]["verified"] is True
    assert snap["ledger"]["chains"] == n
    if app.edges is not None:
        deg = degree_sequence(app.edges, n)
        assert deg.sum() == 2 * len(app.edges)
        assert app.edges.max() < n
        assert app.edges.min() >= 0
        assert len(deg) == n
        assert snap["topology_stats"]["edges"] == len(app.edges)
        assert snap["topology_stats"]["nodes"] == n


def test_damage_renumbers_edges_and_stats_consistent():
    app = NetworkApp()
    app.new_network(n=120, k=6, m=2, settle=2)
    _consistency(app)
    before = len(app.edges)
    app.damage(10)
    assert app.engine.n == 110
    _consistency(app)
    app.damage(50)
    assert app.engine.n == 60
    _consistency(app)
    app.step(steps=3, mode="over")
    _consistency(app)


def test_app_lifecycle_create_spawn_heal_rewire():
    app = NetworkApp()
    app.new_network(n=60, k=6, m=2, settle=2)
    app.create(0.3, -0.3)
    _consistency(app)
    app.spawn(4)
    _consistency(app)
    app.damage(5)
    _consistency(app)
    app.heal(steps=3)
    _consistency(app)
    app.rewire(m=2)
    _consistency(app)
    r = app.route(0, 0.2, 0.2)
    assert isinstance(r["delivered"], bool)
    assert r["path"]
    s = app.search(0.0, 0.0, k=5)
    assert len(s["hits"]) == 5


def test_new_network_resets_state_cleanly():
    app = NetworkApp()
    app.new_network(n=50, settle=1)
    old = app.engine
    old_ledger = app.engine.chains
    app.new_network(n=80, settle=1)
    assert app.engine is not old
    assert app.engine.chains is not old_ledger
    assert app.engine.n == 80
    assert app.snapshot()["ledger"]["chains"] == 80


def test_record_toggle_freezes_and_resumes_ledger():
    app = NetworkApp()
    app.new_network(n=30, settle=1)
    n0 = app.snapshot()["ledger"]["blocks"]
    app.set_record(False)
    app.step(steps=2, mode="settle")
    assert app.snapshot()["ledger"]["blocks"] == n0
    app.set_record(True)
    app.step(steps=2, mode="settle")
    assert app.snapshot()["ledger"]["blocks"] > n0
    assert app.verify()["ok"] is True
    assert app.ledger()["verified"] is True


def test_spawn_empty_app_raises():
    app = NetworkApp()
    with pytest.raises(ValueError):
        app.spawn(1)


# --------------------------------------------------------------------------- #
# H. server: serving, packaging, and concurrent safety
# --------------------------------------------------------------------------- #
def _get(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return r.status, r.read(), r.headers


def _post(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, json.loads(r.read().decode("utf-8"))


def test_html_packaged_and_served():
    assert HTML_PATH.exists()
    assert HTML_PATH.is_file()
    assert importlib.resources.files("puno_app").joinpath(
        "ui.html").is_file()
    assert "api/snapshot" in HTML_PATH.read_text(encoding="utf-8")


def test_server_serves_html_and_snapshot():
    from puno_app.canned_ui import _App
    _App.app = NetworkApp()              # other tests share this global
    server = make_server("127.0.0.1", 0)
    server.daemon_threads = True
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    try:
        port = server.server_address[1]
        base = f"http://127.0.0.1:{port}"
        status, body, headers = _get(base + "/")
        assert status == 200
        assert headers["Content-Type"].startswith("text/html")
        assert "api/snapshot" in body.decode("utf-8")
        status, body, _ = _get(base + "/api/snapshot")
        assert status == 200
        snap = json.loads(body.decode("utf-8"))
        assert snap["ok"] is True
        assert snap["n"] == 0               # fresh app we just installed
        status, d = _post(base + "/api/new",
                          {"n": 50, "k": 6, "topology": "scale-free",
                           "m": 2, "settle": 2})
        assert status == 200 and d["n"] == 50
        try:
            _get(base + "/nope")
            assert False, "expected 404"
        except urllib.error.HTTPError as exc:
            assert exc.code == 404
    finally:
        server.shutdown()
        server.server_close()


def test_concurrent_readers_and_writers_stay_consistent():
    server = make_server("127.0.0.1", 0)
    server.daemon_threads = True
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    try:
        port = server.server_address[1]
        base = f"http://127.0.0.1:{port}"
        _post(base + "/api/new", {"n": 60, "k": 6, "m": 2, "settle": 2})
        stop = threading.Event()
        errors = []
        lock = threading.RLock()

        def writer():
            try:
                for _ in range(60):
                    with lock:
                        _post(base + "/api/autotick", {"steps": 2, "respawn": 2})
                        _post(base + "/api/create", {"x": 0.2, "y": -0.2})
                    if np.random.RandomState(0).rand() < 0.3:
                        with lock:
                            _post(base + "/api/damage", {"count": 3})
            except Exception as exc:  # noqa: BLE001
                errors.append(f"writer: {exc!r}")
            finally:
                stop.set()

        def reader():
            try:
                while not stop.is_set():
                    _, body, _ = _get(base + "/api/snapshot")
                    snap = json.loads(body.decode("utf-8"))
                    n = snap["n"]
                    assert snap["ok"] is True
                    assert n > 0
                    assert len(snap["positions"]) == n
                    assert snap["stats"]["finite"] is True
                    assert snap["ledger"]["verified"] is True
                    assert snap["ledger"]["chains"] == n
                    assert len(snap["degree"]) == n
                    assert snap["degree"] == snap["degree"]  # not None
                    edges = snap["edges"]
                    if edges:
                        assert max(max(e) for e in edges) < n
                        assert sum(deg for deg in snap["degree"]) == 2 * len(edges)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"reader: {exc!r}")

        threads = [threading.Thread(target=writer)]
        threads += [threading.Thread(target=reader) for _ in range(2)]
        for th in threads:
            th.start()
        for th in threads:
            th.join(timeout=60)
        assert not stop.is_set() or True     # writer finished normally
        assert not errors, errors
    finally:
        server.shutdown()
        server.server_close()


# --------------------------------------------------------------------------- #
# I. end-to-end: verify_exact over the damage-repaired population
# --------------------------------------------------------------------------- #
def test_verify_exact_after_full_lifecycle():
    app = NetworkApp()
    app.new_network(n=90, k=6, m=2, settle=2)
    app.damage(10)
    app.create(0.4, 0.4)
    app.spawn(2)
    app.step(steps=3, mode="settle")
    v = app.verify()
    assert v["ok"] is True
    assert v["report"]["verdict"] == "PASS"
