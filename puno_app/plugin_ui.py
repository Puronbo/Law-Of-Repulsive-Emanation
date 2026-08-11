"""Puno Plug: a plug-and-play UI for any function in the repo.

One HTTP server, zero per-function code.  Every decorated plugin in
``plugins/`` and every experiment in ``experiments/`` is auto-discovered and
gets a form generated from its declared (or introspected) parameters.  Run a
function in-process; run an experiment as its subprocess verdict; either way
the result renders as JSON in the browser.

    python -m puno_app.plugin_ui [--host 127.0.0.1] [--port 8767]
    puno-plug                                     # installed entry point

API (all JSON except GET /):
    GET  /                        - the plug-and-play UI page
    GET  /api/catalog             - full catalog (functions + experiments)
    GET  /api/plugin/<name>       - one plugin's spec (params, source)
    POST /api/run/<name>          - run a function plugin   {values: {...}}
    POST /api/experiment/<name>   - run an experiment verdict (subprocess)
    GET  /api/verdict/<name>      - the linked data/<name>_data.json (if any)

A function plugin returns anything (dicts, numpy arrays, sets, ...); the
registry normalizes it to JSON before the response is written.  Experiment
runs stream their stdout into the response's ``output`` field and attach the
freshly written verdict JSON when the module declares one.
"""

import argparse
import json
import os
import subprocess
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from puno_flow.plugin import (  # noqa: E402
    jsonable, registry, experiments_catalog, discover_plugins,
    repo_root)

HTML_PATH = Path(__file__).resolve().parent / "plugin_ui.html"
DATA_DIR = repo_root() / "data"

PLUGIN_CACHE_LOCK = threading.Lock()


def _refresh_catalog():
    """Idempotently build the unified catalog (plugins + experiments)."""
    with PLUGIN_CACHE_LOCK:
        discover_plugins()
        experiments_catalog()
        return registry


class _Catalog:
    """Global registry reference so handlers stay stateless."""

    registry = _refresh_catalog()


def _load_verdict(name):
    """Read data/<name>_data.json if present; return None otherwise."""
    path = DATA_DIR / (name + "_data.json")
    if not path.is_file():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


class Handler(BaseHTTPRequestHandler):
    server_version = "PunoPlug/0.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("puno_plug: %s\n" % (fmt % args))

    # ------------------------------------------------------------------ #
    def _send(self, code, payload, ctype="application/json"):
        body = json.dumps(payload, default=jsonable).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _error(self, msg, code=400):
        self._send(code, {"ok": False, "error": str(msg)})

    def _ok(self, payload):
        self._send(200, {"ok": True, **payload})

    def _post_json(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        return json.loads(raw) if raw else {}

    # ------------------------------------------------------------------ #
    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._serve_html()
            return
        if path == "/api/catalog":
            catalog = _Catalog.registry.catalog(with_source=True)
            self._ok({"count": len(catalog), "catalog": catalog})
            return
        if path.startswith("/api/verdict/"):
            name = path.rsplit("/", 1)[1]
            verdict = _load_verdict(name)
            if verdict is None:
                self._ok({"verdict": None})
            else:
                self._ok({"verdict": jsonable(verdict)})
            return
        if path.startswith("/api/plugin/"):
            name = path.rsplit("/", 1)[1]
            p = _Catalog.registry.get(name)
            if p is None:
                self._error(f"no plugin named {name!r}", 404)
                return
            self._ok(p.spec(with_source=True))
            return
        self._error(f"unknown path {path}", 404)

    def do_POST(self):
        path = urlparse(self.path).path
        body = self._post_json()
        if path.startswith("/api/run/"):
            self._run_function(path.rsplit("/", 1)[1], body)
            return
        if path.startswith("/api/experiment/"):
            self._run_experiment(path.rsplit("/", 1)[1])
            return
        self._error(f"unknown path {path}", 404)

    # ------------------------------------------------------------------ #
    def _run_function(self, name, body):
        p = _Catalog.registry.get(name)
        if p is None:
            self._error(f"no plugin named {name!r}", 404)
            return
        if p.fn is None:
            self._error(f"{name} is an experiment - use POST "
                        f"/api/experiment/{name}", 400)
            return
        t0 = time.time()
        try:
            result = p.run(body.get("values", {}))
        except Exception as exc:
            self._error("%s: %s" % (type(exc).__name__, exc))
            return
        self._ok({"result": jsonable(result),
                  "elapsed_ms": round((time.time() - t0) * 1000, 1)})

    def _run_experiment(self, name):
        p = _Catalog.registry.get(name)
        if p is None:
            self._error(f"no plugin named {name!r}", 404)
            return
        if p.script is None:
            self._error(f"{name} has no run command", 400)
            return
        t0 = time.time()
        try:
            proc = subprocess.run(
                p.script, capture_output=True, text=True, timeout=3600,
                cwd=str(REPO_ROOT))
        except subprocess.TimeoutExpired:
            self._error("experiment timed out after 3600s", 504)
            return
        except OSError as exc:
            self._error("could not start experiment: %s" % exc)
            return
        out = proc.stdout[-20000:]
        err = proc.stderr[-20000:]
        verdict = _load_verdict(name) if proc.returncode == 0 else None
        self._ok({
            "exit_code": proc.returncode,
            "output": out,
            "stderr": err,
            "elapsed_s": round(time.time() - t0, 2),
            "verdict": jsonable(verdict) if verdict is not None else None,
        })

    def _serve_html(self):
        if not HTML_PATH.exists():
            self._error("missing UI file: %s" % HTML_PATH, 500)
            return
        html = HTML_PATH.read_text(encoding="utf-8")
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def make_server(host="127.0.0.1", port=8767):
    server = ThreadingHTTPServer((host, port), Handler)
    server.daemon_threads = True
    return server


def main(argv=None):
    ap = argparse.ArgumentParser(description="Puno Plug - plug-and-play UI")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8767)
    args = ap.parse_args(argv)

    if not HTML_PATH.exists():
        sys.exit("missing UI file: %s" % HTML_PATH)

    n = len(_Catalog.registry.catalog())
    server = make_server(args.host, args.port)
    print(f"puno plug: http://{args.host}:{args.port}  "
          f"({n} functions + experiments in the catalog)")
    print("  press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
