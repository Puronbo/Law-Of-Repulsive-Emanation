"""Tests for the Puno Net indefinite live-session service."""

import json
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import pytest

from puno_app.live_net import (
    METRIC_RING,
    LiveNetHandler,
    LiveNetService,
    _most_crowded_index,
    make_server,
)


def _post(port, path, body=None):
    url = f"http://127.0.0.1:{port}{path}"
    data = json.dumps(body or {}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def _get(port, path):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}",
                                timeout=10) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def _start_server(service):
    server = make_server(service, "127.0.0.1", 0)
    port = server.server_address[1]
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server, port


def _fast(**kw):
    cfg = dict(cap=10, arrival_every=10, flow_per_tick=1, heartbeat_every=50,
               damage_every=5000)
    save_path = kw.pop("save_path", None)
    cfg.update(kw)
    return LiveNetService(seed=42, save_path=save_path, **cfg)


# ---------------------------------------------------------------------- #
class TestDynamics:
    def test_ticks_advance_and_population_grows(self):
        svc = _fast()
        assert svc.tick == 0
        svc.step(100)
        assert svc.tick == 100
        assert svc.n > 0
        assert svc.born > 0
        assert svc._spacing() > 0
        assert 0.0 <= svc._mean_r() <= 1.0

    def test_cap_prunes_population(self):
        svc = _fast(cap=5, arrival_every=5)
        svc.step(400)
        assert svc.n <= 5
        assert svc.pruned > 0

    def test_damage_reduces_population(self):
        svc = _fast(cap=20, arrival_every=10)
        svc.step(300)
        before = svc.n
        svc.damage(3)
        assert svc.n == before - 3
        assert svc.killed == 3

    def test_pause_resume(self):
        svc = _fast()
        svc.step(50)
        paused = svc.pause()
        assert paused["paused"] is True
        svc.step(10)
        assert svc.tick == 50
        svc.resume()
        svc.step(10)
        assert svc.tick == 60

    def test_most_crowded_index_returns_valid_index(self):
        svc = _fast(cap=20, arrival_every=10)
        svc.step(300)
        j = _most_crowded_index(svc.engine)
        assert 0 <= j < svc.n


# ---------------------------------------------------------------------- #
class TestConfig:
    def test_lowering_cap_takes_effect_next_tick(self):
        svc = _fast(cap=30, arrival_every=10)
        svc.step(400)
        assert svc.n > 10
        svc.configure(cap=5)
        svc.step(1)
        assert svc.n <= 5

    def test_configure_returns_config_and_rejects_unknown(self):
        svc = _fast()
        out = svc.configure(home_r=0.5, arrival_every=7)
        assert out["config"]["home_r"] == 0.5
        assert out["config"]["arrival_every"] == 7
        with pytest.raises(ValueError):
            svc.configure(dim=3)


# ---------------------------------------------------------------------- #
class TestCheckpoint:
    def test_roundtrip_preserves_counters_and_rng_stream(self, tmp_path):
        svc = _fast(cap=8, arrival_every=10)
        svc.step(250)
        path = tmp_path / "live.pkl"
        svc.save(path)
        assert path.exists()

        a = LiveNetService.from_checkpoint(path)
        b = LiveNetService.from_checkpoint(path)
        assert a.tick == svc.tick == 250
        assert a.n == svc.n
        assert a.born == svc.born
        assert a.pruned == svc.pruned

        a.step(100)
        b.step(100)
        assert a.tick == b.tick
        assert a.n == b.n
        assert a.born == b.born
        assert a._spacing() == b._spacing()  # identical RNG stream

    def test_resumed_session_continues_ticks(self, tmp_path):
        svc = _fast(cap=8, arrival_every=10)
        svc.step(200)
        path = tmp_path / "live.pkl"
        svc.save(path)
        r = LiveNetService.from_checkpoint(path)
        r.step(50)
        assert r.tick == 250

    def test_autosave_rotation_bounded(self, tmp_path):
        svc = LiveNetService(seed=7, save_path=str(tmp_path / "live.pkl"),
                             autosave_every=50, keep_checkpoints=2,
                             cap=8, arrival_every=10, flow_per_tick=1,
                             heartbeat_every=50000)
        t = threading.Thread(target=svc.run_forever, kwargs=dict(max_ticks=300),
                             daemon=True)
        t.start()
        t.join(timeout=60)
        base = tmp_path / "live.pkl"
        assert base.exists()
        stamps = sorted(tmp_path.glob("live.[0-9]*.pkl"))
        assert len(stamps) <= 3  # keep_checkpoints + base


# ---------------------------------------------------------------------- #
class TestStateViews:
    def test_metrics_bounded(self):
        svc = _fast(cap=8, arrival_every=10, heartbeat_every=5)
        svc.step(500)
        assert 0 < len(svc.metrics) <= METRIC_RING
        series = svc.metrics_series(limit=10)
        assert len(series["tick"]) <= 10
        assert len(series["tick"]) == series["length"]

    def test_status_well_formed(self):
        svc = _fast()
        svc.step(60)
        s = svc.status()
        for key in ("tick", "n", "cap", "spacing", "mean_r", "probe",
                    "born", "pruned", "killed", "running", "paused",
                    "uptime", "alerts", "heartbeats", "config"):
            assert key in s
        assert s["tick"] == 60
        assert s["n"] == s["config"]["cap"] or s["n"] <= s["config"]["cap"]

    def test_positions_match_population(self):
        svc = _fast()
        svc.step(80)
        p = svc.positions()
        assert p["n"] == len(p["q"]) == svc.n


# ---------------------------------------------------------------------- #
class TestHttp:
    @pytest.fixture()
    def pair(self, tmp_path):
        svc = _fast(save_path=str(tmp_path / "live.pkl"))
        server, port = _start_server(svc)
        yield svc, port
        server.shutdown()

    def test_dashboard_served(self, pair):
        svc, port = pair
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/",
                                    timeout=10) as resp:
            assert resp.status == 200
            html = resp.read().decode("utf-8")
        assert "Puno" in html and "<script>" in html

    def test_get_endpoints(self, pair):
        svc, port = pair
        svc.step(80)
        code, status = _get(port, "/api/status")
        assert code == 200 and status["ok"] and status["tick"] == 80
        code, m = _get(port, "/api/metrics?limit=5")
        assert code == 200 and len(m["tick"]) <= 5
        code, p = _get(port, "/api/positions")
        assert code == 200 and p["n"] == svc.n
        code, h = _get(port, "/api/health")
        assert code == 200 and h["ok"] and h["tick"] == svc.tick
        code, a = _get(port, "/api/alerts")
        assert code == 200 and "alerts" in a

    def test_unknown_path_404(self, pair):
        svc, port = pair
        import urllib.error
        with pytest.raises(urllib.error.HTTPError) as exc:
            _get(port, "/api/nope")
        assert exc.value.code == 404

    def test_post_endpoints(self, pair):
        svc, port = pair
        code, body = _post(port, "/api/pause")
        assert code == 200 and body["paused"] is True
        code, body = _post(port, "/api/resume")
        assert code == 200 and body["paused"] is False
        svc.step(300)  # populate so damage has someone to kill
        before = svc.n
        code, body = _post(port, "/api/damage", {"count": 2})
        assert code == 200 and body["n"] == before - 2
        code, body = _post(port, "/api/step", {"count": 25})
        assert code == 200 and body["tick"] == svc.tick
        code, body = _post(port, "/api/config", {"cap": 7})
        assert code == 200 and body["config"]["cap"] == 7
        code, body = _post(port, "/api/checkpoint")
        assert code == 200

    def test_stop_endpoint_drains(self):
        svc = _fast()
        server, port = _start_server(svc)
        t = threading.Thread(target=svc.run_forever, daemon=True)
        t.start()
        time.sleep(0.2)
        assert svc._running
        code, body = _post(port, "/api/stop", {"save": False})
        assert code == 200 and body["stopping"] is True
        t.join(timeout=10)
        assert not svc._running
        assert svc._stop
        server.shutdown()

    def test_concurrent_status_during_ticks(self):
        svc = _fast(cap=6, arrival_every=10, flow_per_tick=1)
        server, port = _start_server(svc)
        t = threading.Thread(target=svc.run_forever, kwargs=dict(max_ticks=1500),
                             daemon=True)
        t.start()
        errors = []

        def reader(_):
            for _ in range(20):
                try:
                    _, s = _get(port, "/api/status")
                    assert s["ok"] and s["tick"] >= 0 and s["n"] >= 0
                except Exception as exc:  # pragma: no cover
                    errors.append(exc)

        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(reader, range(4)))
        t.join(timeout=60)
        assert not errors
        assert svc.tick >= 1500
        server.shutdown()


# ---------------------------------------------------------------------- #
class TestHandlerBinding:
    def test_servers_are_isolated(self):
        a = _fast()
        b = _fast()
        sa, pa = _start_server(a)
        sb, pb = _start_server(b)
        try:
            a.step(10)
            _, sa_status = _get(pa, "/api/status")
            _, sb_status = _get(pb, "/api/status")
            assert sa_status["tick"] == 10
            assert sb_status["tick"] == 0
            assert LiveNetHandler.service is not a  # class attr stays unbound
        finally:
            sa.shutdown()
            sb.shutdown()
