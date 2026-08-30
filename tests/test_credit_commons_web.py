"""Automated end-to-end test of the Credit-Commons web pilot via Flask's test
client (no live server needed). Exercises the full HTTP surface and asserts the
conservation invariant (gate 6) holds across the wire.
"""

import math
import os
import tempfile

import pytest

from credit_commons.web import app as appmod
from credit_commons.web.ledger import Ledger


@pytest.fixture()
def client(tmp_path):
    db = str(tmp_path / "pilot.db")
    appmod.ledger = Ledger(db)
    appmod.app.config["TESTING"] = True
    c = appmod.app.test_client()
    yield c
    appmod.ledger.close()


def post(client, path, body, sess=None):
    return client.post(path, json=body)


def test_full_flow_conservation(client):
    b = client.post("/api/accounts", json={"handle": "bob", "pin": "1234", "tier": "individual"})
    assert b.get_json()["ok"]
    s = client.post("/api/accounts", json={"handle": "grocery", "pin": "9999", "tier": "business"})
    assert s.get_json()["ok"]

    st0 = client.get("/api/status").get_json()
    before = st0["conserved_total"]

    # sign in as bob
    login = client.post("/api/session", json={"handle": "bob", "pin": "1234"})
    assert login.get_json()["ok"]

    # trade bob -> grocery, necessity
    tr = client.post("/api/trade", json={"seller": "grocery", "x": 5, "necessity": True, "terminal": "grocery"})
    assert tr.get_json()["ok"]

    # conservation holds (no mintage, nothing lost)
    st = client.get("/api/status").get_json()
    assert st["conserved_total"] == pytest.approx(before, abs=1e-6)


def test_harm_gauge_conserved_and_cited(client):
    """The '-1 conserved charge' (gate 14): a committed harm I*h shows in
    irrev_total, stays conserved (residual 0), and the physics gauges carry
    the measured markers from experiments/harm_cap.json."""
    b = client.post("/api/accounts", json={"handle": "bob", "pin": "1234"})
    assert b.get_json()["ok"]
    s = client.post("/api/accounts", json={"handle": "grocery", "pin": "9999", "tier": "business"})
    assert s.get_json()["ok"]
    st0 = client.get("/api/status").get_json()
    assert st0["irrev_total"] == 0.0
    assert st0["harm_events"] == 0
    # physics gauges match the measured ladder (harm_cap.json)
    pg = st0["physics"]
    I = appmod.ledger.p.I
    assert pg["sigma_floor"] == pytest.approx(
        math.log(0.13 / 0.11), abs=1e-4)  # ln(reward/g_at(1)) = 0.167
    assert pg["alpha_zero"] == pytest.approx(
        (0.13 - 0.05) / (I * 0.05 * 1.20), abs=1e-4)  # 0.667
    assert pg["alpha_cusp"] == pytest.approx(
        (2 * (0.05 * 1.20 * 0.13) ** 0.5 - 0.05) / (I * 0.05 * 1.20), abs=1e-4)

    bob = appmod.ledger.conn.execute(
        "SELECT id FROM accounts WHERE handle='bob'").fetchone()["id"]
    shop = appmod.ledger.conn.execute(
        "SELECT id FROM accounts WHERE handle='grocery'").fetchone()["id"]
    before = client.get("/api/status").get_json()["conserved_total"]
    appmod.ledger.trade(bob, shop, 1.0, committed_harm=0.07)
    st = client.get("/api/status").get_json()
    # irrev_total = I * h = 2 * 0.07
    assert st["irrev_total"] == pytest.approx(2.0 * 0.07, abs=1e-6)
    assert st["harm_events"] == 1
    # credit conservation untouched by the harm charge
    assert st["conserved_total"] == pytest.approx(before, abs=1e-6)


def test_bad_pin_rejected(client):
    client.post("/api/accounts", json={"handle": "bob", "pin": "1234"})
    r = client.post("/api/session", json={"handle": "bob", "pin": "0000"})
    assert r.status_code == 401
    assert r.get_json()["ok"] is False


def test_unauth_trade_rejected(client):
    client.post("/api/accounts", json={"handle": "alice", "pin": "1111"})
    client.post("/api/accounts", json={"handle": "shop", "pin": "2222", "tier": "business"})
    r = client.post("/api/trade", json={"seller": "shop", "x": 2})
    assert r.status_code == 401


def test_ledger_and_needs_signing_guard(client):
    client.post("/api/accounts", json={"handle": "a", "pin": "1a2b3c"})
    client.post("/api/accounts", json={"handle": "b", "pin": "1111", "tier": "business"})
    client.post("/api/session", json={"handle": "a", "pin": "1a2b3c"})
    client.post("/api/trade", json={"seller": "b", "x": 3, "terminal": "b"})
    ld = client.get("/api/ledger").get_json()
    assert ld["ok"] and len(ld["ledger"]) == 1
    assert ld["ledger"][0]["kind"] == "trade"


def test_pwa_static_routes_serve(client):
    for path, ctype in [
        ("/", "text/html"),
        ("/manifest.webmanifest", "manifest"),
        ("/sw.js", "javascript"),
        ("/icon.svg", "svg"),
    ]:
        r = client.get(path)
        assert r.status_code == 200, path
        assert ctype in r.content_type, path
