"""Tests for the plug-and-play UI: registry, catalog, and HTTP endpoints.

The registry must serve "any function" - a decorated plugin in plugins/ or an
auto-discovered experiment in experiments/ - with zero per-function code, and
the HTTP server must turn that catalog into runnable forms.
"""

import json
import threading
import urllib.error
import urllib.request

import pytest

from puno_flow.plugin import (
    registry, run, run_async, jsonable, discover_plugins, experiments_catalog,
)
from puno_app.plugin_ui import make_server

# ---------------------------------------------------------------------- #
# Registry (no HTTP needed)
# ---------------------------------------------------------------------- #
class TestRegistry:
    def test_plugins_are_registered(self):
        discover_plugins()
        for name in ("add", "greet", "collatz", "word_freq"):
            p = registry.get(name)
            assert p is not None and p.kind == "function"
            assert p.title and p.params

    def test_add_explicit_params(self):
        out = run("add", {"a": 2.5, "b": 3.5})
        assert out["sum"] == 6.0
        assert out["text"] == "2.5 + 3.5 = 6.0"

    def test_introspected_params_types(self):
        p = registry.get("greet")
        types = {q["name"]: q["type"] for q in p.spec()["params"]}
        assert types == {"name": "str", "excited": "bool", "times": "int"}
        out = run("greet", {"name": "world", "excited": False, "times": 2})
        assert out["greeting"] == "hello, world! hello, world! "

    def test_introspected_default_type_from_value(self):
        p = registry.get("collatz")
        types = {q["name"]: q["type"] for q in p.spec()["params"]}
        assert types == {"n": "int"}
        assert run("collatz", {"n": 27})["steps"] == 111

    def test_jsonable_normalizes_sets_tuples(self):
        out = run("word_freq", {})
        assert out["unique_count"] > 0
        assert isinstance(out["frequencies"], dict)
        assert isinstance(out["first_three"], list)  # tuple -> list

    def test_run_async_returns_normalized_result(self):
        future = run_async("add", {"a": 1, "b": 2})
        assert future.result(timeout=10)["sum"] == 3

    def test_missing_plugin_raises(self):
        with pytest.raises(KeyError):
            run("definitely_not_a_plugin", {})

    def test_experiments_are_catalogued(self):
        experiments_catalog()
        for name in ("rotation_test", "decentral_web", "bazaar_net"):
            p = registry.get(name)
            assert p is not None and p.kind == "experiment"
            assert p.script
        # verdict-capable modules expose the --verdict flag on the script
        for name in ("decentral_web", "bazaar_net"):
            assert registry.get(name).script[-1] == "--verdict"

    def test_unified_catalog_has_both_kinds(self):
        cat = registry.catalog(with_source=True)
        kinds = {c["kind"] for c in cat}
        assert {"function", "experiment"} <= kinds


# ---------------------------------------------------------------------- #
# HTTP endpoints
# ---------------------------------------------------------------------- #
def _post(port, path, body=None):
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}",
        data=json.dumps(body or {}).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def _get(port, path):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}",
                                timeout=30) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


@pytest.fixture(scope="module")
def server():
    srv = make_server("127.0.0.1", 0)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield port
    srv.shutdown()


class TestHttp:
    def test_dashboard_served(self, server):
        with urllib.request.urlopen(f"http://127.0.0.1:{server}/",
                                    timeout=30) as resp:
            html = resp.read().decode("utf-8")
        assert resp.status == 200
        assert "<script>" in html and "catalog" in html

    def test_catalog_has_functions_and_experiments(self, server):
        code, body = _get(server, "/api/catalog")
        assert code == 200 and body["ok"] and body["count"] > 50
        kinds = {c["kind"] for c in body["catalog"]}
        assert {"function", "experiment"} <= kinds
        by_name = {c["name"]: c for c in body["catalog"]}
        assert by_name["add"]["params"][0]["type"] == "float"

    def test_plugin_spec(self, server):
        code, body = _get(server, "/api/plugin/greet")
        assert code == 200 and body["ok"]
        assert body["title"] == "Greet a name"
        assert {p["name"]: p["type"] for p in body["params"]} == \
            {"name": "str", "excited": "bool", "times": "int"}

    def test_run_function_endpoint(self, server):
        code, body = _post(server, "/api/run/add",
                           {"values": {"a": 2, "b": 3}})
        assert code == 200 and body["ok"]
        assert body["result"]["sum"] == 5.0
        assert body["elapsed_ms"] >= 0

    def test_run_missing_plugin_404(self, server):
        with pytest.raises(urllib.error.HTTPError) as exc:
            _post(server, "/api/run/nope", {})
        assert exc.value.code == 404

    def test_run_experiment_on_function_is_400(self, server):
        with pytest.raises(urllib.error.HTTPError) as exc:
            _post(server, "/api/experiment/add")
        assert exc.value.code == 400

    def test_verdict_endpoint(self, server):
        code, body = _get(server, "/api/verdict/decentral_web")
        assert code == 200 and body["ok"]
        v = body["verdict"]
        assert v is not None and v["verdict"].startswith("SUPPORTED")
        assert {c["id"] for c in v["claims"]} == {"W1", "W2", "W3", "W4"}

    def test_verdict_missing_is_null(self, server):
        code, body = _get(server, "/api/verdict/not_an_experiment")
        assert code == 200 and body["ok"] and body["verdict"] is None

    def test_unknown_path_404(self, server):
        with pytest.raises(urllib.error.HTTPError) as exc:
            _get(server, "/api/nope")
        assert exc.value.code == 404


class TestHttpExperimentSubprocess:
    def test_run_fast_experiment_verdict(self, server):
        """The subprocess path: rotation_test is ~1s, deterministic, and its
        pinned verdict JSON is bit-unchanged by the rerun."""
        import hashlib
        from pathlib import Path
        data = Path(__file__).resolve().parents[1] / "data"
        path = data / "rotation_test_data.json"
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        code, body = _post(server, "/api/experiment/rotation_test")
        assert code == 200 and body["ok"]
        assert body["exit_code"] == 0
        assert body["output"]
        assert body["verdict"] is not None
        assert body["verdict"]["verdict"].startswith("SUPPORTED")
        after = hashlib.sha256(path.read_bytes()).hexdigest()
        assert after == before
