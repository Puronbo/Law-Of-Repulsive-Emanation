"""Flask web app for the Credit-Commons pilot.

Serves the PWA (browser + add-to-home-screen) and a small JSON API over the
persistent SQLite ledger in `ledger.py`. Implements the security posture of
docs/CREDIT_COMMONS.md §6: memorable PIN + recallable account number, but
NEVER offline cash — everything is online, sessions are short-lived and
revocable, logins are rate-limited per handle.

Run (from repo root):
    $env:PYTHONPATH="C:\\Users\\Me\\Downloads\\Puno_Calculus"
    python credit_commons/web/app.py
Then open http://127.0.0.1:5000 in a browser.
"""

from __future__ import annotations

import math
import os
import secrets
import time

from flask import Flask, jsonify, request, send_from_directory, session as fsess

from credit_commons.sim import Params
from credit_commons.web.ledger import Ledger

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static")
DB_PATH = os.environ.get("CC_DB", os.path.join(BASE, "pilot.db"))

app = Flask(__name__, static_folder=STATIC, static_url_path="")
app.secret_key = os.environ.get("CC_SECRET", secrets.token_hex(16))

ledger = Ledger(DB_PATH)

# §6: rate-limit login attempts per handle (simple in-memory, pilot scale)
_login_attempts: dict[str, list[float]] = {}
LOGIN_WINDOW = 60.0
LOGIN_MAX = 5


def _rate_limit(handle: str) -> bool:
    now = time.time()
    ts = _login_attempts.get(handle, [])
    ts = [t for t in ts if now - t < LOGIN_WINDOW]
    _login_attempts[handle] = ts
    if len(ts) >= LOGIN_MAX:
        return False
    ts.append(now)
    return True


def public_account(a):
    return {
        "id": a["id"],
        "handle": a["handle"],
        "tier": a["tier"],
        "credit": round(a["credit"], 4),
        "trust": round(a["trust"], 4),
        "irrev": round(a["irrev"], 4),
        "necess": round(a["necess"], 4),
    }


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------
@app.post("/api/accounts")
def create_account():
    data = request.get_json(force=True) or {}
    handle = str(data.get("handle", "")).strip()
    pin = str(data.get("pin", ""))
    if not handle or not (4 <= len(pin) <= 8):
        return jsonify({"ok": False, "reason": "handle + PIN (4-8) required"}), 400
    tier = str(data.get("tier", "individual"))
    aid, ok, msg = ledger.create_account(handle, pin, tier=tier)
    if not ok:
        return jsonify({"ok": False, "reason": msg}), 409
    row = ledger.conn.execute(
        "SELECT * FROM accounts WHERE id=?", (aid,)).fetchone()
    return jsonify({"ok": True, "account": public_account(row)})


@app.post("/api/session")
def login():
    data = request.get_json(force=True) or {}
    handle = str(data.get("handle", "")).strip()
    pin = str(data.get("pin", ""))
    if not handle:
        return jsonify({"ok": False, "reason": "handle required"}), 400
    if not _rate_limit(handle):
        return jsonify({"ok": False, "reason": "too many attempts, wait"}), 429
    aid = ledger.verify_pin(handle, pin)
    if aid is None:
        return jsonify({"ok": False, "reason": "bad credentials"}), 401
    # §6 short-lived, revocable session token (single-comons pilot)
    token = secrets.token_hex(16)
    fsess["cc_uid"] = aid
    fsess["cc_token"] = token
    fsess["cc_exp"] = time.time() + 3600  # 1 hour
    fsess.permanent = False
    row = ledger.conn.execute("SELECT * FROM accounts WHERE id=?", (aid,)).fetchone()
    return jsonify({"ok": True, "token": token, "account": public_account(row)})


def _authed():
    if fsess.get("cc_exp", 0) < time.time():
        return None
    return fsess.get("cc_uid")


@app.get("/api/me")
def me():
    uid = _authed()
    if uid is None:
        return jsonify({"ok": False, "reason": "not signed in"}), 401
    row = ledger.conn.execute("SELECT * FROM accounts WHERE id=?", (uid,)).fetchone()
    return jsonify({"ok": True, "account": public_account(row)})


@app.post("/api/trade")
def trade():
    uid = _authed()
    if uid is None:
        return jsonify({"ok": False, "reason": "not signed in"}), 401
    data = request.get_json(force=True) or {}
    seller_handle = str(data.get("seller", "")).strip()
    x = float(data.get("x", 0))
    necessity = bool(data.get("necessity", False))
    terminal = str(data.get("terminal", "")).strip()
    seller = ledger.conn.execute(
        "SELECT id FROM accounts WHERE handle=?", (seller_handle,)).fetchone()
    if seller is None:
        return jsonify({"ok": False, "reason": "unknown seller"}), 400
    term_id = None
    if terminal:
        tr = ledger.conn.execute(
            "SELECT id FROM accounts WHERE handle=?", (terminal,)).fetchone()
        term_id = tr["id"] if tr else None
    ok, info = ledger.trade(uid, seller["id"], x, necessity=necessity,
                            terminal=term_id)
    if not ok:
        return jsonify({"ok": False, "reason": info.get("reason", "trade rejected")}), 400
    return jsonify({"ok": True, "fee": info["fee"]})


@app.post("/api/grant")
def grant():
    uid = _authed()
    if uid is None:
        return jsonify({"ok": False, "reason": "not signed in"}), 401
    data = request.get_json(force=True) or {}
    recipient = str(data.get("recipient", "")).strip()
    amount = float(data.get("amount", 0))
    row = ledger.conn.execute(
        "SELECT id FROM accounts WHERE handle=?", (recipient,)).fetchone()
    if row is None:
        return jsonify({"ok": False, "reason": "unknown recipient"}), 400
    ok, info = ledger.grant(row["id"], amount, sponsor_id=uid)
    if not ok:
        return jsonify({"ok": False, "reason": info}), 400
    return jsonify({"ok": True, "granted": round(info, 4) if isinstance(info, float) else info})


_P = Params()


def _physics_gauges():
    """The measured invariants as live gauges (experiments/harm_cap.json):
    sigma_floor = ln(reward/g_at(1)) is the honest minimum positive action;
    the alpha ladder = h/X thresholds a harm must clear to step g_eff past
    the gate, reward (sigma=0, FT flips), and the phase cusp g*=2*sqrt(C)."""
    reward = _P.reward()
    g_star = 2.0 * (_P.g0 * _P.gdepth * reward) ** 0.5
    sigma_floor = math.log(reward / _P.g_at(1.0))
    return {
        "sigma_floor": round(sigma_floor, 4),
        "alpha_gate": round((_P.g_at(1.0) - _P.g0) / (_P.I * _P.g0 * _P.gdepth), 4),
        "alpha_zero": round((reward - _P.g0) / (_P.I * _P.g0 * _P.gdepth), 4),
        "alpha_cusp": round((g_star - _P.g0) / (_P.I * _P.g0 * _P.gdepth), 4),
    }


@app.get("/api/status")
def status():
    s = ledger.conn.execute(
        "SELECT COUNT(*) AS n, COALESCE(SUM(credit),0) AS credit FROM accounts").fetchone()
    # Gini of trust (unsigned best-equity metric)
    trusts = [r["trust"] for r in ledger.conn.execute(
        "SELECT trust FROM accounts").fetchall()]
    gini = _gini(trusts)
    irr = ledger.conn.execute(
        "SELECT COALESCE(SUM(irrev),0) AS v FROM accounts").fetchone()["v"]
    harm_events = ledger.conn.execute(
        "SELECT COUNT(*) n FROM ledger WHERE kind='trade' AND note LIKE 'harm=%'"
    ).fetchone()["n"]
    return jsonify({
        "ok": True,
        "members": s["n"],
        "circulation": round(s["credit"], 4),
        "reserve": round(ledger.reserve, 4),
        "conserved_total": round(ledger.conserved_total(), 4),
        "gini_trust": round(gini, 4),
        "trades": ledger.conn.execute(
            "SELECT COUNT(*) n FROM ledger WHERE kind='trade'").fetchone()["n"],
        "irrev_total": round(irr, 4),
        "harm_events": harm_events,
        "physics": _physics_gauges(),
        "genesis": ledger.genesis,
    })


@app.get("/api/ledger")
def ledger_view():
    rows = ledger.ledger_rows(limit=max(1, min(500, request.args.get("n", 100, type=int))))
    out = []
    for r in rows:
        bh = ledger.conn.execute("SELECT handle FROM accounts WHERE id=?",
                                 (r["buyer"],)).fetchone()
        sh = ledger.conn.execute("SELECT handle FROM accounts WHERE id=?",
                                 (r["seller"],)).fetchone()
        if r["kind"] == "trade":
            out.append({
                "kind": "trade",
                "buyer": bh["handle"] if bh else None,
                "seller": sh["handle"] if sh else None,
                "x": round(r["x"], 4), "fee": round(r["fee"], 4),
                "necessity": bool(r["necessity"]),
            })
        else:
            out.append({"kind": "grant", "recipient": sh["handle"] if sh else None,
                        "amount": round(r["x"], 4)})
    return jsonify({"ok": True, "ledger": out})


@app.post("/api/logout")
def logout():
    fsess.clear()
    return jsonify({"ok": True})


# ---------------------------------------------------------------------------
# PWA static serving + installability
# ---------------------------------------------------------------------------
@app.get("/")
def index():
    return send_from_directory(STATIC, "index.html")


@app.get("/manifest.webmanifest")
def manifest():
    return send_from_directory(STATIC, "manifest.webmanifest", mimetype="application/manifest+json")


@app.get("/sw.js")
def sw():
    return send_from_directory(STATIC, "sw.js", mimetype="application/javascript")


def _gini(vals):
    vals = sorted(vals)
    n = len(vals)
    if n == 0 or sum(vals) == 0:
        return 0.0
    cum = sum((2 * i - n - 1) * v for i, v in enumerate(vals, start=1))
    return min(1.0, cum / (n * sum(vals)))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Credit-Commons pilot on http://127.0.0.1:{port}  (db: {DB_PATH})")
    app.run(host="127.0.0.1", port=port, debug=False)
