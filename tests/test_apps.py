"""Tests for the autonomous applications (guard_mesh, search_service,
router)."""

import numpy as np
import pytest

from puno_flow.apps.guard_mesh import deploy, holes, run_simulation, tick
from puno_flow.apps.router import delivered_fraction, route
from puno_flow.apps.search_service import SearchService, dispatch


def test_holes_rank_most_isolated_first():
    rng = np.random.RandomState(0)
    X = rng.uniform(-0.5, 0.5, (120, 2))
    from puno_flow import FlowEngine
    engine = FlowEngine(dim=2, k=8).add_many(X)
    h = holes(engine)
    assert h.dtype.kind == "i"
    assert len(h) > 0
    # spacing of hole units >= spacing of the rest (ranked by isolation)
    _, d = engine.search(engine.q, k=8)
    mean_d = d[:, 1:].mean(axis=1)
    assert mean_d[h].min() >= np.quantile(mean_d, 0.9) - 1e-12


def test_mesh_respawns_and_recoers_from_damage():
    engine = deploy(150, seed=4)
    s_before = engine.spacing()
    drop = np.random.RandomState(9).choice(engine.n, size=40, replace=False)
    engine.remove(drop)
    s_after = engine.spacing()
    rng = np.random.RandomState(1)
    events = []
    for _ in range(3):
        events += tick(engine, target=s_before, rng=rng)
    s_recovered = engine.spacing()
    assert s_after > s_before
    assert any("respawned" in e for e in events)
    assert s_recovered < s_after


def test_mesh_simulation_timeline_and_ledger():
    engine = deploy(120, seed=6)
    log, engine = run_simulation(engine, ticks=8, damage_at=(3,))
    assert len(log) == 8
    assert log[3]["n"] < log[2]["n"]            # damage shrank the mesh
    assert log[-1]["n"] > log[3]["n"]           # respawn regrew it
    assert np.isfinite(engine.q).all()
    assert engine.verify_ledger() == (True, None, None)
    assert engine.ledger_audit()["chains"] >= engine.n


def test_search_service_insert_query_damage_heal():
    svc = SearchService()
    for i, (x, y) in enumerate([(0.1, 0.2), (0.4, 0.5), (0.9, 0.1)]):
        svc.insert(x, y, label=f"r{i}")
    hits = svc.query(0.1, 0.2, k=3)
    assert hits[0][0] == 0
    assert hits[0][1] == pytest.approx(0.0)
    assert hits[0][2] == "r0"
    # distances are ascending
    ds = [h[1] for h in hits]
    assert ds == sorted(ds)
    svc.damage(1)
    assert svc.engine.n == 2
    svc.heal(30)
    assert np.isfinite(svc.engine.q).all()
    assert svc.engine.verify_ledger() == (True, None, None)
    assert svc.ops()["verified"] is True


def test_search_service_dispatch_commands():
    svc = SearchService()
    svc.insert(0.0, 0.0, "origin")
    svc.insert(1.0, 0.0)
    out = dispatch("query 0 0 2", svc)
    assert out.startswith("  #0")
    assert "d=0.0000" in out
    assert "origin" in out
    assert "verified=True" in dispatch("stats", svc)
    assert dispatch("nonsense", svc).startswith("  unknown")


def test_router_delivers_between_units_after_settle():
    rng = np.random.RandomState(23)
    from puno_flow import FlowEngine
    engine = FlowEngine(dim=2, k=8, mu0=0.12).add_many(
        rng.uniform(-0.5, 0.5, (200, 2)))
    engine.settle(60)
    rng2 = np.random.RandomState(5)
    pairs = [(int(rng2.randint(0, 200)), engine.q[int(rng2.randint(0, 200))])
             for _ in range(20)]
    frac, med = delivered_fraction(engine, pairs)
    assert frac == 1.0
    assert med >= 1


def test_router_self_heals_after_damage():
    rng = np.random.RandomState(23)
    from puno_flow import FlowEngine
    engine = FlowEngine(dim=2, k=8, mu0=0.12).add_many(
        rng.uniform(-0.5, 0.5, (200, 2)))
    engine.settle(60)
    rng2 = np.random.RandomState(5)
    pairs = [(int(rng2.randint(0, 200)), engine.q[int(rng2.randint(0, 200))])
             for _ in range(20)]
    engine.remove(rng2.choice(200, size=60, replace=False))
    engine.heal(60)
    pairs = [(int(rng2.randint(0, engine.n)),
              engine.q[int(rng2.randint(0, engine.n))]) for _ in range(20)]
    frac, _ = delivered_fraction(engine, pairs)
    assert frac > 0.8
    assert engine.verify_ledger() == (True, None, None)


def test_router_route_reaches_exact_dest():
    rng = np.random.RandomState(1)
    from puno_flow import FlowEngine
    engine = FlowEngine(dim=2, k=8, mu0=0.12).add_many(
        rng.uniform(-0.5, 0.5, (100, 2)))
    engine.settle(30)
    path, delivered = route(engine, 0, engine.q[17])
    assert delivered
    assert path[-1] == 17
