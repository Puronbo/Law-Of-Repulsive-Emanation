"""Tests for the Puno Calculus: the engine, the dashboard HTTP layer, the
CLI subcommands, and the definitive-constant explorer.

The whole point of the L.O.R.E. thesis is that an integration constant is
only arbitrary while the initial condition is unknown; the explorer and the
engine both collapse it from measured values.  These tests pin that down with
exact identities and asset-backed measurements.
"""

import json
import math
import subprocess
import sys
import threading
import urllib.request
from pathlib import Path

import pytest

from puno_app import calculus

APP_DIR = Path(__file__).resolve().parents[1] / "puno_app"


# --------------------------------------------------------------------------- #
# Engine: parser / evaluation
# --------------------------------------------------------------------------- #

def test_parse_and_eval():
    e = calculus.parse("3*x^2 + sin(x)")
    assert calculus.eval_expr(e, 1.0) == pytest.approx(3 + math.sin(1))
    assert calculus.eval_expr(calculus.parse("2^3"), 0) == pytest.approx(8)
    assert calculus.eval_expr(calculus.parse("-x^2"), 3) == pytest.approx(-9)
    assert calculus.eval_expr(calculus.parse("x^-1"), 2) == pytest.approx(0.5)
    assert calculus.eval_expr(calculus.parse("e"), 0) == pytest.approx(math.e)
    assert calculus.eval_expr(calculus.parse("pi"), 0) == pytest.approx(math.pi)


def test_parse_errors():
    with pytest.raises(ValueError):
        calculus.parse("3 +* 2")
    with pytest.raises(ValueError):
        calculus.parse("")


# --------------------------------------------------------------------------- #
# Engine: symbolic differentiation
# --------------------------------------------------------------------------- #

def test_derive_polynomial():
    s, _ = calculus.differentiate("x^3")
    assert s.replace(" ", "") == "3*x^2"
    s, _ = calculus.differentiate("3*x^2 + sin(x)")
    assert "cos" in s and s.count("cos") == 1


def test_derive_trig_and_product():
    s, _ = calculus.differentiate("sin(x)")
    assert s.replace(" ", "") == "cos(x)"
    s, _ = calculus.differentiate("x*exp(x)")
    # d(x e^x) = e^x + x e^x
    d = calculus.parse(s)
    assert calculus.eval_expr(d, 1.0) == pytest.approx(2 * math.e)


def test_derive_numeric_agreement():
    cases = ["x^2", "sin(x)", "exp(x)", "log(x)", "x*cos(x)", "3*x^2 + sin(x)"]
    for expr in cases:
        e = calculus.parse(expr)
        d = calculus.differentiate(expr)[1]
        f = lambda x: calculus.eval_expr(e, x)
        for x in (0.5, 1.3, 2.7):
            assert calculus.numeric_differentiate(f, x) == pytest.approx(
                calculus.eval_expr(d, x), abs=1e-6), expr


# --------------------------------------------------------------------------- #
# Engine: symbolic antiderivative
# --------------------------------------------------------------------------- #

def test_antiderivative_identities():
    cases = {
        "x^2": "x^3/3",
        "1/x": "log(x)",
        "exp(x)": "exp(x)",
        "sin(x)": "-cos(x)",
        "cos(x)": "sin(x)",
        "exp(2*x)": "exp(2*x)/2",
        "x*exp(x)": "(x - 1)*exp(x)",
    }
    for expr, expected in cases.items():
        s, exact = calculus.antiderivative(expr)
        assert exact is True, expr
        assert s.replace(" ", "") == expected.replace(" ", ""), expr


def test_antiderivative_roundtrip():
    # d/dx (F) == f for a battery of closed-form cases
    cases = ["x^3", "3*x^2 + sin(x)", "exp(3*x)", "x*exp(x)", "x*sin(x)",
             "x*cos(x)", "1/x", "sqrt(x)", "1/sqrt(x)", "1/(1 + x^2)",
             "sin(x)^2", "cos(x)^2", "log(x)", "tan(x)", "2^x"]
    for expr in cases:
        s, exact = calculus.antiderivative(expr)
        assert exact is True, expr
        d, _ = calculus.differentiate(s)
        for x in (0.4, 1.1, 2.2):
            if expr in ("log(x)",):
                x = 1.7  # avoid branch cuts near 0
            assert calculus.eval_expr(calculus.parse(d), x) == pytest.approx(
                calculus.eval_expr(calculus.parse(expr), x), rel=1e-6), expr


def test_antiderivative_outside_library():
    s, exact = calculus.antiderivative("sin(x)/x")
    assert exact is False and s is None


# --------------------------------------------------------------------------- #
# Engine: definite integrals as constants
# --------------------------------------------------------------------------- #

def test_definite_integral_exact():
    d = calculus.definite_integral("x^2", 0, 3)
    assert d["exact"] is True
    assert d["exact_value"] == pytest.approx(9)
    assert d["antiderivative"].replace(" ", "") == "x^3/3"


def test_fold_mirror_area_constant():
    # the README signature constant: 2 * a^2 * TH^3 / 6 with a = 1, TH = 20
    a, th = 1.0, 20.0
    d = calculus.definite_integral("x^2", 0, th)
    assert d["exact_value"] == pytest.approx(2 * a * a * th ** 3 / 6, rel=1e-12)
    assert d["exact_value"] == pytest.approx(2666.6666666666665, rel=1e-9)


def test_definite_integral_numeric_fallback():
    d = calculus.definite_integral("sin(x)/x", 1e-9, 1)
    assert d["exact"] is False
    assert d["numeric_value"] == pytest.approx(0.946083070367, rel=1e-4)


def test_integrate_numeric_sinc():
    v = calculus.integrate_numeric(lambda x: math.sin(x) / x if x else 1.0,
                                   1e-9, math.pi)
    assert v == pytest.approx(1.851937051982466, rel=1e-6)


# --------------------------------------------------------------------------- #
# Engine: the definitive constant (L.O.R.E.)
# --------------------------------------------------------------------------- #

def test_definitive_constant_collapses():
    res = calculus.definitive_constant("2*x", q0=1.0, fq0=5.0)
    assert res["ok"] is True
    assert res["particular"].replace(" ", "") == "x^2"
    assert res["particular_at_q0"] == pytest.approx(1)
    assert res["C0"] == pytest.approx(4)
    assert res["definitive"] == "x^2 + 4"
    # derivative of the definitive antiderivative is still f
    d, _ = calculus.differentiate(res["definitive"])
    assert calculus.eval_expr(calculus.parse(d), 2.0) == pytest.approx(4)


def test_definitive_constant_conserved_across_origins():
    # C0 depends on the measured point; the family {F + C} is invariant:
    # choosing a different measured (q0, F(q0)) shifts C0 by exactly the
    # difference in F(q0), so F(q) + C0 stays the same function.
    base = calculus.definitive_constant("2*x", 1.0, 5.0)
    other = calculus.definitive_constant("2*x", 2.0, 8.0)
    d_base = calculus.parse(base["definitive"])
    d_other = calculus.parse(other["definitive"])
    for x in (0.0, 0.5, 1.0, 3.0):
        assert calculus.eval_expr(d_base, x) == pytest.approx(
            calculus.eval_expr(d_other, x), rel=1e-12)


# --------------------------------------------------------------------------- #
# Engine: asset-backed measure C0 = V(q0) = H(q0, 0)
# --------------------------------------------------------------------------- #

def test_lore_measure_uses_asset():
    res = calculus.lore_measure(q0=(0.0, 0.0), context=["Tech", "Silicon"])
    assert res["ok"] is True
    assert "hamiltonian_flow" in res["source"]
    assert res["V_q0"] == res["H_q0_0"]
    assert res["C0"] == res["V_q0"]
    assert res["kinetic_energy"] == 0.0
    assert "Origin" in res["positions"]


def test_lore_measure_matches_positions_asset():
    res = calculus.lore_measure(q0=(0.0, 0.0), context=["Tech", "Silicon"])
    pos = calculus.asset_positions()
    assert pos["Origin"] == [0.0, 0.0]
    assert res["positions"]["Silicon"] == pos["Silicon"]


def test_sample():
    xs, ys = calculus.sample("x^2", 0, 2, n=10)
    assert len(xs) == 11 and len(ys) == 11
    assert ys[5] == pytest.approx(1.0)
    xs2, ys2 = calculus.sample("1/x", 0, 1, n=5)
    assert ys2[0] is None  # pole at 0 must not crash


# --------------------------------------------------------------------------- #
# Limits
# --------------------------------------------------------------------------- #

def test_limit_exact_identities():
    cases = {
        "sin(x)/x": (0, 1.0),
        "tan(x)/x": (0, 1.0),
        "(1 - cos(x))/x^2": (0, 0.5),
        "(exp(x) - 1)/x": (0, 1.0),
        "log(1 + x)/x": (0, 1.0),
        "(1 + x)^(1/x)": (0, math.e),
        "(1 + 1/x)^x": ("inf", math.e),
        "(1 + 2/x)^x": ("inf", math.e ** 2),
        "1/x": ("inf", 0.0),
        "x^2": (2, 4.0),
        "3*x + 1": (1, 4.0),
    }
    for expr, (x0, expected) in cases.items():
        r = calculus.limit(expr, x0, "both")
        assert r["ok"] is True and r["exists"] is True, expr
        assert r["value"] == pytest.approx(expected, rel=1e-6), expr
        # exact flag set for standard forms and continuous substitution
        assert r["exact"] is True, expr


def test_limit_numeric_fallbacks():
    r = calculus.limit("sin(x)/x", "inf", "both")
    assert r["exists"] is True and r["value"] == pytest.approx(0.0, abs=1e-6)
    assert r["exact"] is False


def test_limit_divergence_and_two_sided_split():
    r = calculus.limit("1/x", 0, "both")
    assert r["exists"] is False and r["value"] is None
    assert "left:-inf" in r["diverges"] and "right:+inf" in r["diverges"]

    r = calculus.limit("log(x)", 0, "right")
    assert r["exists"] is False and r["diverges"] == "-inf"

    r = calculus.limit("exp(x)", "inf", "both")
    assert r["exists"] is False and r["diverges"] == "+inf"


def test_limit_one_sided():
    assert calculus.limit("1/x", 0, "left")["value"] is None
    r = calculus.limit("1/x", 0, "right")
    assert r["exists"] is False and r["diverges"] == "+inf"
    r = calculus.limit("x^2", 2, "right")
    assert r["exists"] is True and r["value"] == pytest.approx(4)


# --------------------------------------------------------------------------- #
# Regression: adding limits must not change any established finding
# --------------------------------------------------------------------------- #

def test_findings_unchanged_by_limit_feature():
    # 1. fold mirror area
    d = calculus.definite_integral("x^2", 0, 20)
    assert d["exact_value"] == pytest.approx(2666.6666666666665)

    # 2. the C0 battery measured earlier
    battery = [("2*x", 1.0, 5.0, 4.0), ("x^2", 1.0, 5.0, 14 / 3),
               ("sin(x)", 0.0, 0.0, 1.0), ("exp(x)", 0.0, 0.0, -1.0),
               ("1/x", 1.0, 5.0, 5.0), ("x*exp(x)", 0.0, 0.0, 1.0)]
    for expr, q0, f0, c0 in battery:
        r = calculus.definitive_constant(expr, q0, f0)
        assert r["ok"] is True and r["C0"] == pytest.approx(c0), expr

    # 3. the L.O.R.E. asset measure
    m = calculus.lore_measure(q0=(0.0, 0.0), context=["Tech", "Silicon"])
    assert m["ok"] is True and m["C0"] == pytest.approx(24.434791603891032)

    # 4. the explorer blocks still resolve to the same numbers
    from puno_app import constant_explorer
    blocks = constant_explorer.collect()
    assert all(b["ok"] for b in blocks["definitive_constants"])
    fa = blocks["definitive_constants"][1]
    assert fa["exact"] == pytest.approx(2666.6666666666665)
    pc = blocks["definitive_constants"][3]
    assert pc["pi(943901200001)"] == 35_575_526_191


# --------------------------------------------------------------------------- #
# Server: HTTP + CLI
# --------------------------------------------------------------------------- #

def _http(port, path, body=None):
    url = f"http://127.0.0.1:{port}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data,
        method="POST" if body is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            ctype = r.headers.get("Content-Type", "")
            raw = r.read()
            return (json.loads(raw.decode("utf-8")) if "json" in ctype
                    else raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:  # 400/500 still carry a JSON body
        return json.loads(exc.read().decode("utf-8"))


def test_calculus_server_http():
    from http.server import ThreadingHTTPServer
    from puno_app.calculus_server import CalcHandler

    srv = ThreadingHTTPServer(("127.0.0.1", 0), CalcHandler)
    CalcHandler.server = srv
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    port = srv.server_address[1]
    try:
        html = _http(port, "/")
        assert "<canvas" in html and "<script>" in html
        assert "Puno Calculus" in html
        assert "calculus.html" in (APP_DIR / "calculus_server.py").read_text("utf-8")

        ping = _http(port, "/api/ping")
        assert ping["ok"] is True

        d = _http(port, "/api/derive", {"expr": "x^3"})
        assert d["ok"] is True and d["derivative"].replace(" ", "") == "3*x^2"

        a = _http(port, "/api/antideriv", {"expr": "x^2"})
        assert a["ok"] is True and a["exact"] is True
        assert a["antiderivative"].replace(" ", "") == "x^3/3"

        i = _http(port, "/api/integrate", {"expr": "x^2", "a": 0, "b": 3})
        assert i["ok"] is True and i["exact_value"] == pytest.approx(9)

        c = _http(port, "/api/constant",
                  {"expr": "2*x", "q0": 1, "f0": 5})
        assert c["ok"] is True and c["C0"] == pytest.approx(4)

        lm = _http(port, "/api/limit",
                   {"expr": "sin(x)/x", "x": "0", "side": "both"})
        assert lm["ok"] is True and lm["exists"] is True
        assert lm["value"] == pytest.approx(1)

        lr = _http(port, "/api/lore",
                   {"q0x": 0, "q0y": 0, "context": ["Tech", "Silicon"]})
        assert lr["ok"] is True and lr["C0"] == lr["V_q0"]

        p = _http(port, "/api/points",
                  {"expr": "x^2", "a": 0, "b": 2, "n": 4})
        assert p["ok"] is True and len(p["xs"]) == 5

        pos = _http(port, "/api/positions")
        assert pos["ok"] is True and "Origin" in pos["positions"]

        bad = _http(port, "/api/derive", {"expr": "3 +* 2"})
        assert bad["ok"] is False and "error" in bad
    finally:
        _http(port, "/api/stop", {})  # graceful shutdown
        t.join(timeout=5)


def test_calculus_cli_derive():
    out = subprocess.run(
        [sys.executable, "-m", "puno_app.calculus_server", "derive", "x^2"],
        capture_output=True, text=True, cwd=APP_DIR.parent)
    assert out.returncode == 0, out.stderr
    lines = {l.split(":")[0].strip(): l.split(":", 1)[1].strip()
             for l in out.stdout.strip().splitlines() if ":" in l}
    assert lines["derivative"] == "2*x"


def test_calculus_cli_integrate_json():
    out = subprocess.run(
        [sys.executable, "-m", "puno_app.calculus_server", "integrate",
         "--json", "x^2", "0", "3"],
        capture_output=True, text=True, cwd=APP_DIR.parent)
    assert out.returncode == 0, out.stderr
    data = json.loads(out.stdout)
    assert data["exact_value"] == pytest.approx(9)


# --------------------------------------------------------------------------- #
# Explorer: the definitive constants from the assets
# --------------------------------------------------------------------------- #

def test_explorer_fold_mirror_area():
    from puno_app import constant_explorer
    res = constant_explorer.fold_mirror_area()
    assert res["ok"] is True
    assert res["exact"] == pytest.approx(2666.6666666666665)
    assert res["as_2a2TH3_over_6"] == res["exact"]
    assert res["antiderivative(theta)"] == "x^3/3"


def test_explorer_epoch_0d():
    from puno_app import constant_explorer
    res = constant_explorer.epoch_0d()
    assert res["tau(10262000)"] == 80
    assert res["tau(26102000)"] == 80
    assert res["gcd_triangle"] == [1, 1, 1]
    assert res["chain_fold_1914467"].replace(" ", "") == "31^1x61757^1"


def test_explorer_prime_counts_from_asset():
    from puno_app import constant_explorer
    res = constant_explorer.prime_counts()
    assert res["ok"] is True
    assert res["pi(943901200001)"] == 35_575_526_191


def test_explorer_quantum_ground_state():
    from puno_app import constant_explorer
    res = constant_explorer.quantum_ground_state()
    assert res["ok"] is True
    assert res["E0"] == pytest.approx(5.843778304934855)


def test_explorer_collect_and_run():
    from puno_app import constant_explorer
    data = constant_explorer.collect()
    assert len(data["definitive_constants"]) == 5
    assert all(b["ok"] for b in data["definitive_constants"])
    assert data["engine"] == "puno_app.calculus (exact + numeric)"
