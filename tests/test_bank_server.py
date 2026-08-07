"""Tests for the Decentral Bank dashboard stack (puno_app.bank_*).

BankService is the headless driver around the multi-process Decentral Bank
network; bank_server wraps it in a stdlib HTTP server (mirroring canned_ui).
These tests lock in both layers plus the packaging detail that bank.html
ships next to the server module.
"""

import json
import threading
import urllib.request
from pathlib import Path

from puno_app.bank_service import BankService

APP_DIR = Path(__file__).resolve().parents[1] / "puno_app"


def _http(port, path, body=None, method=None):
    url = f"http://127.0.0.1:{port}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data,
                                 method=method or ("GET" if body is None
                                                   else "POST"))
    with urllib.request.urlopen(req, timeout=90) as r:
        ctype = r.headers.get("Content-Type", "")
        raw = r.read()
        return (json.loads(raw.decode("utf-8")) if "json" in ctype
                else raw.decode("utf-8"))


def _wait_status(port, pred, timeout=20):
    import time
    deadline = time.time() + timeout
    while time.time() < deadline:
        s = _http(port, "/api/status", method="GET")
        if pred(s):
            return s
        time.sleep(0.3)
    raise AssertionError("status condition not met: %s" % pred)


def test_bank_service_lifecycle():
    svc = BankService(n_frag=6, k=3, vote_timeout=0.5, n_accounts=12,
                      min_balance=100)
    import time
    try:
        time.sleep(3)
        s = svc.status()
        assert s["alive_count"] == 6
        assert s["conserved"] is True

        cid, tx = svc.submit(0, 1, 10)
        assert cid.startswith("t")
        time.sleep(2)
        s = svc.status()
        assert s["committed"] == 1
        assert s["total_blocks"] >= 1
        assert s["conserved"] is True

        v = svc.validate_all()
        assert v is not None and v["chains_valid"] is True
        assert v["conserved"] is True

        svc.kill(3)
        time.sleep(0.5)
        assert svc.status()["alive_count"] == 5

        svc.restart(3)
        time.sleep(2)
        assert svc.status()["alive_count"] == 6

        svc.partition([[0, 1, 2], [3, 4, 5]])
        svc.full_network()
        svc.resync()
        assert svc.status()["alive_count"] == 6
    finally:
        svc.stop()


def test_bank_service_rebuild_changes_params():
    svc = BankService(n_frag=4, k=2, vote_timeout=0.5, n_accounts=8,
                      min_balance=50)
    import time
    try:
        time.sleep(2)
        assert svc.status()["n_frag"] == 4
        svc.rebuild(n_frag=8, k=3, n_accounts=16, min_balance=25)
        time.sleep(2)
        s = svc.status()
        assert s["n_frag"] == 8
        assert s["n_accounts"] == 16
        assert s["min_balance"] == 25
        assert s["conserved"] is True
    finally:
        svc.stop()


def test_bank_server_serves_html_and_api():
    import sys
    sys.path.insert(0, str(APP_DIR.parent))
    from http.server import ThreadingHTTPServer

    from puno_app.bank_server import BankHandler
    from puno_app.bank_service import BankService
    service = BankService(n_frag=5, k=2, vote_timeout=0.5, n_accounts=10,
                          min_balance=60)
    BankHandler.service = service
    srv = ThreadingHTTPServer(("127.0.0.1", 0), BankHandler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    port = srv.server_address[1]
    import time
    try:
        time.sleep(2)

        html = _http(port, "/", method="GET")
        assert "<canvas" in html and "<script>" in html
        assert "bank.html" in (APP_DIR / "bank_server.py").read_text("utf-8")

        s = _http(port, "/api/status", method="GET")
        assert s["ok"] is True and s["alive_count"] == 5

        d = _http(port, "/api/submit", {"from": 0, "to": 1, "amount": 7})
        assert d["ok"] is True and d["cid"].startswith("t")

        _wait_status(port, lambda s: s["committed"] >= 1 and s["conserved"])

        ac = _http(port, "/api/accounts", method="GET")
        assert len(ac["accounts"]) == 10
        assert ac["accounts"][0]["balance"] == 60 - 7

        d = _http(port, "/api/kill", {"node": 4})
        assert d["ok"] is True
        _wait_status(port, lambda s: s["alive_count"] == 4)

        d = _http(port, "/api/restart", {"node": 4})
        assert d["ok"] is True
        _wait_status(port, lambda s: s["alive_count"] == 5)

        d = _http(port, "/api/partition",
                  {"groups": [[0, 1], [2, 3, 4]]})
        assert d["ok"] is True
        d = _http(port, "/api/full-network", {})
        assert d["ok"] is True

        v = _http(port, "/api/validate", method="GET")
        assert v["ok"] is True and v["chains_valid"] is True
    finally:
        srv.shutdown()
        t.join(timeout=5)
        service.stop()
