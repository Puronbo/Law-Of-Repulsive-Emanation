"""Tests for the puno lab application layer (puno_app).

NetworkApp is the application layer the UI drives; canned_ui wraps it in a
stdlib HTTP server.  These tests lock in both, plus the packaging detail
that the single-file UI ships next to the server module.
"""

import json
import threading
import urllib.request
from pathlib import Path

import numpy as np

from puno_app.app_state import NetworkApp

LAB_DIR = Path(__file__).resolve().parents[1] / "puno_app"


def _hits_order(d):
    ds = [h[1] for h in d["hits"]]
    return ds == sorted(ds)


def test_network_app_lifecycle():
    app = NetworkApp()
    snap = app.new_network(n=120, k=6, topology="scale-free", settle=5)
    assert snap["n"] == 120
    assert snap["topology"] == "scale-free"
    assert snap["ledger"]["verified"] is True
    assert snap["edges"] and snap["degree"]

    snap = app.spawn(3)
    assert snap["n"] == 123

    hits = app.search(0.0, 0.0, k=5)
    assert len(hits["hits"]) == 5 and _hits_order(hits)

    target = snap["positions"][10]
    r = app.route(0, *target)
    assert r["delivered"] is True and r["hops"] >= 1

    w = app.wiring()
    assert w["wired"] is True and w["stats"]["nodes"] == 123
    assert w["hubs"] and w["hubs"][0][1] >= w["hubs"][-1][1]

    snap = app.damage(10)
    assert snap["n"] == 113
    snap = app.heal(20)
    assert snap["n"] == 113
    assert np.isfinite(np.asarray(snap["positions"])).all()
    assert snap["ledger"]["verified"] is True

    v = app.verify()
    assert v["ok"] is True
    assert app.ledger()["verified"] is True


def test_network_app_autotick_respawns_into_holes():
    app = NetworkApp()
    app.new_network(n=120, k=6, topology="scale-free", settle=5)
    events = app.autotick(steps=1, respawn=1)
    assert events["n"] >= 120
    assert events["ledger"]["verified"] is True


def test_network_app_unwired_topology():
    app = NetworkApp()
    app.new_network(n=60, k=6, topology="plain", settle=3)
    assert app.wiring() == {"wired": False}
    assert app.snapshot()["edges"] is None


def test_network_app_errors_are_raised_not_swallowed():
    app = NetworkApp()
    try:
        app.step(steps=1)
        raise AssertionError("step with no engine should raise")
    except ValueError:
        pass


def _server():
    import sys
    sys.path.insert(0, str(LAB_DIR.parent))
    from puno_app.canned_ui import make_server
    srv = make_server("127.0.0.1", 0)
    return srv


def _http(srv, path, body=None, method=None):
    url = f"http://127.0.0.1:{srv.server_address[1]}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data,
                                 method=method or ("GET" if body is None
                                                   else "POST"))
    with urllib.request.urlopen(req, timeout=60) as r:
        ctype = r.headers.get("Content-Type", "")
        raw = r.read()
        return (json.loads(raw.decode("utf-8")) if "json" in ctype
                else raw.decode("utf-8"))


def test_canned_ui_serves_html_and_api():
    srv = _server()
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        html = _http(srv, "/")
        assert "<canvas" in html and "<script>" in html
        assert "ui.html" in (LAB_DIR / "canned_ui.py").read_text("utf-8")

        snap = _http(srv, "/api/snapshot", method="GET")
        assert snap["ok"] is True and snap["n"] == 0

        d = _http(srv, "/api/new", {"n": 80, "k": 6, "topology": "scale-free",
                                    "settle": 3})
        assert d["ok"] is True and d["n"] == 80 and d["edges"]

        d = _http(srv, "/api/spawn", {"count": 2})
        assert d["n"] == 82

        d = _http(srv, "/api/search", {"x": 0.0, "y": 0.0, "k": 4})
        assert len(d["hits"]) == 4

        tpos = _http(srv, "/api/snapshot", method="GET")["positions"][7]
        d = _http(srv, "/api/route", {"start": 0, "x": tpos[0], "y": tpos[1]})
        assert d["delivered"] is True

        d = _http(srv, "/api/topology", method="POST")
        assert d["wired"] is True and d["stats"]["gamma"] > 0

        d = _http(srv, "/api/ledger", method="POST")
        assert d["verified"] is True

        d = _http(srv, "/api/verify", method="POST")
        assert d["ok"] is True
    finally:
        srv.shutdown()
        t.join(timeout=5)


def test_canned_ui_rejects_unknown_paths():
    srv = _server()
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        import urllib.error
        try:
            _http(srv, "/nope")
            raise AssertionError("unknown path should 404")
        except urllib.error.HTTPError as e:
            assert e.code == 404
    finally:
        srv.shutdown()
        t.join(timeout=5)
