"""BankServer: stdlib HTTP layer over BankService, mirroring canned_ui.py.

Endpoints (JSON):
    GET  /                  -> bank.html (the dashboard)
    GET  /api/status        -> live network view
    GET  /api/accounts      -> account table
    GET  /api/ledgers       -> per-fragment chains as seen by a node
    GET  /api/validate      -> chain validity + conservation replay
    POST /api/submit        -> {from, to, amount}
    POST /api/kill          -> {node}
    POST /api/restart       -> {node}
    POST /api/kill-all
    POST /api/restart-all
    POST /api/partition     -> {groups: [[...],[...]]}
    POST /api/full-network
    POST /api/resync        -> {node?}
    POST /api/new           -> {n_frag?, k?, vote_timeout?, n_accounts?,
                                min_balance?, tls?}
    POST /api/stop

The service (and its child processes) is created only inside ``main()`` so a
Windows ``spawn`` child of the network re-importing this module never builds
a network at import time.
"""

import argparse
import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from .bank_service import BankService

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "bank.html")


class BankHandler(BaseHTTPRequestHandler):
    service = None
    server = None

    def log_message(self, fmt, *args):
        pass

    # ------------------------------------------------------------------ #
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self._send_html()
        elif path == "/api/status":
            self._json(self.service.status())
        elif path == "/api/accounts":
            self._json({"ok": True, "accounts": self.service.accounts()})
        elif path == "/api/ledgers":
            self._json({"ok": True,
                        "ledgers": self.service.ledgers()})
        elif path == "/api/validate":
            v = self.service.validate_all()
            if v is None:
                self._json({"ok": False, "error": "snapshot not ready"})
            else:
                self._json({"ok": True, **v})
        else:
            self._json({"ok": False, "error": "unknown endpoint"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        body = self._read_json()
        try:
            if path == "/api/submit":
                cid, tx = self.service.submit(
                    int(body["from"]), int(body["to"]), int(body["amount"]))
                self._json({"ok": True, "cid": cid,
                            "amount": tx["amount"],
                            "from": tx["from"], "to": tx["to"]})
            elif path == "/api/kill":
                self.service.kill(int(body["node"]))
                self._json({"ok": True})
            elif path == "/api/restart":
                self.service.restart(int(body["node"]))
                self._json({"ok": True})
            elif path == "/api/kill-all":
                self.service.kill_all()
                self._json({"ok": True})
            elif path == "/api/restart-all":
                self.service.restart_all()
                self._json({"ok": True})
            elif path == "/api/partition":
                self.service.partition(body.get("groups") or [])
                self._json({"ok": True})
            elif path == "/api/full-network":
                self.service.full_network()
                self._json({"ok": True})
            elif path == "/api/resync":
                node = body.get("node")
                self.service.resync(int(node) if node is not None else None)
                self._json({"ok": True})
            elif path == "/api/new":
                self.service.rebuild(
                    n_frag=body.get("n_frag"),
                    k=body.get("k"),
                    vote_timeout=body.get("vote_timeout"),
                    n_accounts=body.get("n_accounts"),
                    min_balance=body.get("min_balance"),
                    tls=body.get("tls"))
                self._json({"ok": True})
            elif path == "/api/stop":
                def _shutdown():
                    self.service.stop()
                    srv = BankHandler.server
                    if srv is not None:
                        srv.shutdown()
                threading.Thread(target=_shutdown, daemon=True).start()
                self._json({"ok": True, "bye": True})
            else:
                self._json({"ok": False, "error": "unknown endpoint"}, 404)
        except (ValueError, KeyError) as exc:
            self._json({"ok": False, "error": str(exc)}, 400)
        except Exception as exc:  # noqa: BLE001 - surface to the UI
            self._json({"ok": False, "error": "%s: %s"
                        % (type(exc).__name__, exc)}, 500)

    # ------------------------------------------------------------------ #
    def _read_json(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = 0
        if n <= 0:
            return {}
        return json.loads(self.rfile.read(n) or b"{}")

    def _send_html(self):
        with open(HTML_PATH, "rb") as fh:
            body = fh.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, payload, code=200):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="puno-bank",
                                 description="Decentral Bank live dashboard")
    ap.add_argument("--port", type=int, default=8090)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--n-frag", type=int, default=6)
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--vote-timeout", type=float, default=0.8)
    ap.add_argument("--n-accounts", type=int, default=24)
    ap.add_argument("--min-balance", type=int, default=100)
    ap.add_argument("--tls", action="store_true")
    args = ap.parse_args(argv)

    service = BankService(n_frag=args.n_frag, k=args.k,
                          vote_timeout=args.vote_timeout,
                          n_accounts=args.n_accounts,
                          min_balance=args.min_balance,
                          tls=args.tls, host=args.host)
    BankHandler.service = service

    server = ThreadingHTTPServer((args.host, args.port), BankHandler)
    BankHandler.server = server
    url = "http://%s:%d" % (args.host, args.port)
    print("puno-bank up: n=%d k=%d  %s  (Ctrl-C to stop)" %
          (args.n_frag, args.k, url), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        service.stop()
    print("bye")


if __name__ == "__main__":
    main()
