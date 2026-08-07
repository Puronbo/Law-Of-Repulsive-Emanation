"""CalculusServer: stdlib HTTP layer over ``puno_app.calculus``.

The dashboard and the ``puno-calculus`` CLI share this one module.

HTTP endpoints (JSON):
    GET  /                  -> calculus.html (the dashboard)
    GET  /api/ping
    POST /api/derive        -> {expr}             d/dx
    POST /api/antideriv     -> {expr}             particular F (C = 0)
    POST /api/integrate     -> {expr, a, b}       definite integral constant
    POST /api/constant      -> {expr, q0, fq0}    C0 = fq0 - F(q0) (L.O.R.E.)
    POST /api/limit         -> {expr, x, side}    lim_{x->x0} f(x)
    POST /api/lore          -> {q0x, q0y, context, alpha}  C0 = V(q0) = H(q0,0)
    POST /api/points        -> {expr, a, b, n}    samples for the canvas
    POST /api/stop

CLI (``puno-calculus``):
    puno-calculus serve [--port 8091]
    puno-calculus derive EXPR
    puno-calculus antideriv EXPR
    puno-calculus integrate EXPR A B
    puno-calculus constant EXPR --q0 X --f0 Y
    puno-calculus lore [--q0x X --q0y Y --context "Tech Silicon"]
    puno-calculus constants            (same as ``puno-constants``)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from . import calculus

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "calculus.html")


class CalcHandler(BaseHTTPRequestHandler):
    server = None

    def log_message(self, fmt, *args):  # quiet by default
        pass

    # ------------------------------------------------------------------ #
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self._send_html()
        elif path == "/api/ping":
            self._json({"ok": True, "who": "puno-calculus",
                        "version": "1.0.0"})
        elif path == "/api/positions":
            try:
                self._json({"ok": True,
                            "positions": calculus.asset_positions()})
            except Exception as exc:  # noqa: BLE001
                self._json({"ok": False, "error": str(exc)}, 500)
        else:
            self._json({"ok": False, "error": "unknown endpoint"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        body = self._read_json()
        try:
            if path == "/api/derive":
                s, _ = calculus.differentiate(body["expr"])
                self._json({"ok": True, "expr": body["expr"],
                            "derivative": s})
            elif path == "/api/antideriv":
                s, exact = calculus.antiderivative(body["expr"])
                if not exact:
                    self._json({"ok": True, "expr": body["expr"],
                                "antiderivative": None, "exact": False,
                                "error": "outside the closed-form library "
                                         "(numeric only)"})
                else:
                    self._json({"ok": True, "expr": body["expr"],
                                "antiderivative": s, "exact": True})
            elif path == "/api/integrate":
                self._json({"ok": True,
                            **calculus.definite_integral(
                                body["expr"], float(body["a"]),
                                float(body["b"]))})
            elif path == "/api/constant":
                self._json(calculus.definitive_constant(
                    body["expr"], float(body["q0"]), float(body["f0"])))
            elif path == "/api/limit":
                self._json(calculus.limit(
                    body["expr"], body["x"], body.get("side", "both")))
            elif path == "/api/lore":
                try:
                    res = calculus.lore_measure(
                        (float(body.get("q0x", 0.0)),
                         float(body.get("q0y", 0.0))),
                        list(body.get("context") or ["Tech", "Silicon"]),
                        float(body["alpha"]) if body.get("alpha") else None)
                except Exception as exc:  # noqa: BLE001
                    res = {"ok": False,
                           "error": "%s: %s (asset present?)"
                                    % (type(exc).__name__, exc)}
                self._json(res)
            elif path == "/api/points":
                xs, ys = calculus.sample(
                    body["expr"], float(body["a"]), float(body["b"]),
                    int(body.get("n", 200)))
                self._json({"ok": True, "expr": body["expr"],
                            "a": float(body["a"]), "b": float(body["b"]),
                            "xs": xs, "ys": ys})
            elif path == "/api/stop":
                def _shutdown():
                    srv = CalcHandler.server
                    if srv is not None:
                        srv.shutdown()
                threading.Thread(target=_shutdown, daemon=True).start()
                self._json({"ok": True, "bye": True})
            else:
                self._json({"ok": False, "error": "unknown endpoint"}, 404)
        except (ValueError, KeyError) as exc:
            self._json({"ok": False, "error": str(exc)}, 400)
        except Exception as exc:  # noqa: BLE001
            self._json({"ok": False,
                        "error": "%s: %s" % (type(exc).__name__, exc)}, 500)

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


# --------------------------------------------------------------------------- #
# CLI subcommands
# --------------------------------------------------------------------------- #

def _cmd_serve(args):
    server = ThreadingHTTPServer((args.host, args.port), CalcHandler)
    CalcHandler.server = server
    url = "http://%s:%d" % (args.host, args.port)
    print("puno-calculus up: %s  (Ctrl-C to stop)" % url, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    print("bye")


def _emit(payload, args):
    if args.json:
        print(json.dumps(payload, indent=2))
    elif "error" in payload:
        print("error: %s" % payload["error"], file=sys.stderr)
        raise SystemExit(1)
    else:
        for key, value in payload.items():
            if isinstance(value, (dict, list)):
                print("%-22s %s" % (key + ":", json.dumps(value)))
            else:
                print("%-22s %s" % (key + ":", value))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="puno-calculus",
                                 description="The Puno Calculus engine, CLI "
                                             "and dashboard")
    sub = ap.add_subparsers(dest="cmd")

    p_serve = sub.add_parser("serve", help="browser dashboard")
    p_serve.add_argument("--port", type=int, default=8091)
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.set_defaults(handler=_cmd_serve)

    def _add_compute(name, help_text, ap_):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("expr")
        p.add_argument("--json", action="store_true")
        return p

    p_derive = _add_compute("derive", "d/dx of an expression", sub)
    p_derive.set_defaults(handler=lambda a: _emit(
        {"ok": True, "expr": a.expr,
         "derivative": calculus.differentiate(a.expr)[0]}, a))

    p_anti = _add_compute("antideriv", "particular antiderivative (C = 0)",
                          sub)
    p_anti.set_defaults(handler=lambda a: _emit(
        {"ok": True, "expr": a.expr,
         "antiderivative": calculus.antiderivative(a.expr)[0]}, a))

    p_int = _add_compute("integrate", "definite integral as a constant", sub)
    p_int.add_argument("a", type=float)
    p_int.add_argument("b", type=float)
    p_int.set_defaults(handler=lambda a: _emit(
        {"ok": True, **calculus.definite_integral(a.expr, a.a, a.b)}, a))

    p_con = _add_compute("constant",
                         "collapse C0 from initial condition (q0, F(q0))",
                         sub)
    p_con.add_argument("--q0", type=float, required=True)
    p_con.add_argument("--f0", type=float, required=True)
    p_con.set_defaults(handler=lambda a: _emit(
        calculus.definitive_constant(a.expr, a.q0, a.f0), a))

    p_lim = _add_compute("limit", "lim_{x->X} f(x); X = number or inf/-inf",
                         sub)
    p_lim.add_argument("x", help="point; use inf, -inf, or a number")
    p_lim.add_argument("--side", choices=["both", "left", "right"],
                       default="both")
    p_lim.set_defaults(handler=lambda a: _emit(
        calculus.limit(a.expr, a.x, a.side), a))

    p_lore = sub.add_parser("lore",
                            help="measure C0 = V(q0) = H(q0,0) from the asset")
    p_lore.add_argument("--q0x", type=float, default=0.0)
    p_lore.add_argument("--q0y", type=float, default=0.0)
    p_lore.add_argument("--context", default="Tech Silicon")
    p_lore.add_argument("--alpha", type=float, default=None)
    p_lore.add_argument("--json", action="store_true")
    p_lore.set_defaults(handler=lambda a: _emit(
        calculus.lore_measure((a.q0x, a.q0y), a.context.split(),
                              a.alpha), a))

    p_con2 = sub.add_parser(
        "constants", help="print the definitive constants (asset explorer)")
    p_con2.add_argument("--json", action="store_true")
    p_con2.set_defaults(handler=lambda a: _run_explorer(a))

    args = ap.parse_args(argv)
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 0
    args.handler(args)
    return 0


def _run_explorer(args):
    from . import constant_explorer
    constant_explorer.run(json_out=args.json)


if __name__ == "__main__":
    main()
