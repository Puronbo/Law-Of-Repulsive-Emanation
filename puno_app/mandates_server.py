"""Text-mandate dashboard: CLI + stdlib web UI for text-mandatable professions.

Which professions can be easily mandated through text? A profession is
text-mandatable when a complete written instruction set (the mandate) fully
determines the work - an agent handed only the text produces the output with
no tacit, embodied, or situational knowledge to supply. This module serves
that answer two ways from one shared report (professions.report.build_report):

    python -m puno_app.mandates_server report   # console table
    python -m puno_app.mandates_server serve    # http://127.0.0.1:8899

API (all JSON):
    GET /api/mandates   - the full report: professions with class, K/S,
                          mandate fraction/status, task decompositions, and
                          generated mandate text (or the skill residue)
"""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # noqa: E402

from professions.report import build_report  # noqa: E402

HTML_PATH = Path(__file__).resolve().parent / "mandates.html"


class Handler(BaseHTTPRequestHandler):
    server_version = "PunoMandates/0.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("puno_mandates: %s\n" % (fmt % args))

    def _send(self, code, body, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, payload):
        self._send(200, json.dumps(payload).encode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send(200, HTML_PATH.read_bytes(), "text/html; charset=utf-8")
        elif path == "/api/mandates":
            self._json(build_report())
        else:
            self._send(404, json.dumps({"ok": False, "error": path}).encode("utf-8"))


def make_server(host="127.0.0.1", port=8899):
    server = ThreadingHTTPServer((host, port), Handler)
    server.daemon_threads = True
    return server


def _print_report(report):
    print("=" * 72)
    print("text-mandatable professions (mandate = 1 - skill_fraction)")
    print("=" * 72)
    print("\n  status        mandate  class  profession")
    for r in report["professions"]:
        print("  %-13s  %6.1f%%   %s    %s"
              % (r["mandate_status"], r["mandate_fraction"] * 100, r["class"],
                 r["name"]))
    print("\n  status counts: %s" % ", ".join(
        "%s=%d" % kv for kv in sorted(report["status_counts"].items())))
    print("  class counts:  %s" % ", ".join(
        "%s=%d" % kv for kv in sorted(report["class_counts"].items())))
    print()
    print("verdict:", report["verdict"])


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="puno-mandates",
        description="text-mandatable professions: report or web dashboard")
    sub = ap.add_subparsers(dest="cmd", metavar="{report,serve}")
    sub.add_parser("report", help="print the mandate report table")
    serve = sub.add_parser("serve", help="run the web dashboard")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8899)
    args = ap.parse_args(argv)

    if args.cmd == "report":
        _print_report(build_report())
        return 0

    if args.cmd is None or args.cmd == "serve":
        if not HTML_PATH.exists():
            sys.exit(f"missing UI file: {HTML_PATH}")
        server = make_server(args.host, args.port)
        print(f"puno mandates dashboard: http://{args.host}:{args.port}  "
              f"(Ctrl-C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nbye")
        finally:
            server.server_close()
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
