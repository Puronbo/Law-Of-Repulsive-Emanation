"""Puno lab - canned UI (stdlib HTTP server + single-file browser app).

This is the "I'll create the lab UI myself" module: a stdlib-only
ThreadingHTTPServer with a JSON API over one NetworkApp instance, and a
single self-contained HTML/JS page served at GET /.  No framework, no
bundler, no live server - run it with:

    python -m puno_app.canned_ui [--host 127.0.0.1] [--port 8765]

API (all JSON):
    GET  /api/snapshot          - full state (positions, edges, stats, log)
    POST /api/new               - {n, k, mu0, topology, m, seed, settle}
    POST /api/step              - {steps, mode: settle|absorb|over, mu}
    POST /api/create            - {x, y}
    POST /api/spawn             - {count}
    POST /api/damage            - {count}
    POST /api/heal              - {steps}
    POST /api/rewire            - {m}
    POST /api/autotick          - {steps, respawn}
    POST /api/search            - {x, y, k}
    POST /api/route             - {start, x, y}
    POST /api/record            - {on}
    POST /api/verify            - all-pairs bit-exactness check
    POST /api/ledger            - chain audit
    POST /api/topology          - wiring stats + hubs
"""

import argparse
import json
import sys
from pathlib import Path
from threading import Thread
from urllib.parse import parse_qs, urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from puno_app.app_state import NetworkApp

HTML_PATH = Path(__file__).resolve().parent / "ui.html"


def _json_default(obj):
    """Fallback encoder for numpy scalars/arrays that slip past _clean."""
    import numpy as np
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    return str(obj)


class _App:
    """Global app instance so handlers stay stateless."""

    app = NetworkApp()


class Handler(BaseHTTPRequestHandler):
    server_version = "PunoLab/0.1"

    # ------------------------------------------------------------------ #
    def log_message(self, fmt, *args):
        sys.stderr.write("puno_ui: %s\n" % (fmt % args))

    def _send(self, code, payload, ctype="application/json"):
        body = json.dumps(payload, default=_json_default).encode("utf-8")
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
        elif path == "/api/snapshot":
            with _App.app.lock:
                self._ok(_App.app.snapshot())
        else:
            self._error(f"unknown path {path}", 404)

    def do_POST(self):
        path = urlparse(self.path).path
        app = _App.app
        body = self._post_json()
        try:
            with app.lock:
                if path == "/api/new":
                    self._ok(app.new_network(**body))
                elif path == "/api/step":
                    self._ok(app.step(**body))
                elif path == "/api/create":
                    self._ok(app.create(body.get("x", 0.0),
                                        body.get("y", 0.0)))
                elif path == "/api/spawn":
                    self._ok(app.spawn(body.get("count", 3)))
                elif path == "/api/damage":
                    self._ok(app.damage(body.get("count", 10)))
                elif path == "/api/heal":
                    self._ok(app.heal(body.get("steps", 50)))
                elif path == "/api/rewire":
                    self._ok(app.rewire(body.get("m", 2),
                                        body.get("seed")))
                elif path == "/api/autotick":
                    self._ok(app.autotick(body.get("steps", 3),
                                          body.get("respawn", 3)))
                elif path == "/api/search":
                    self._ok(app.search(body.get("x", 0.0),
                                        body.get("y", 0.0),
                                        body.get("k", 5)))
                elif path == "/api/route":
                    self._ok(app.route(body.get("start", 0),
                                       body.get("x", 0.0),
                                       body.get("y", 0.0)))
                elif path == "/api/record":
                    self._ok(app.set_record(bool(body.get("on", True))))
                elif path == "/api/verify":
                    self._ok(app.verify())
                elif path == "/api/ledger":
                    self._ok(app.ledger())
                elif path == "/api/topology":
                    self._ok(app.wiring())
                else:
                    self._error(f"unknown path {path}", 404)
        except Exception as exc:  # surface engine errors as JSON
            self._error(str(exc))

    # ------------------------------------------------------------------ #
    def _serve_html(self):
        html = HTML_PATH.read_text(encoding="utf-8")
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def make_server(host="127.0.0.1", port=8765):
    server = ThreadingHTTPServer((host, port), Handler)
    server.daemon_threads = True
    return server


def main(argv=None):
    ap = argparse.ArgumentParser(description="Puno lab canned UI")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args(argv)

    if not HTML_PATH.exists():
        sys.exit(f"missing UI file: {HTML_PATH}")

    server = make_server(args.host, args.port)
    Thread(target=server.serve_forever, daemon=True).start()
    print(f"puno lab UI: http://{args.host}:{args.port}  "
          f"(n={_App.app.engine.n if _App.app.engine else 0})")
    try:
        while True:
            with _App.app.lock:
                if _App.app.engine is not None:
                    _App.app.autotick(steps=1, respawn=1)
            server.handle_request()
    except KeyboardInterrupt:
        print("\nbye")
        server.shutdown()


if __name__ == "__main__":
    main()
