#!/usr/bin/env python3
"""
serve_dashboard.py
==================
Start a local HTTP server for the L.O.R.E. dashboard.
Opens http://localhost:8080/docs/ in your default browser.

Serving layout:
  /             -> 302 redirect to /docs/ (the dashboard)
  /docs/        -> docs/index.html (the dashboard UI)
  /docs/*       -> static files from docs/
  /Universals/* -> JSON data + modules the dashboard fetches via ../Universals/

Usage:  python serve_dashboard.py  [port]
"""

import http.server
import webbrowser
import sys
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path in ("/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/docs/")
            self.end_headers()
            return
        if path == "/docs":
            self.send_response(302)
            self.send_header("Location", "/docs/")
            self.end_headers()
            return
        super().do_GET()

    def log_message(self, fmt, *args):
        sys.stderr.write("[dashboard] %s\n" % (fmt % args))


if __name__ == "__main__":
    url = f"http://localhost:{PORT}/docs/"
    print(f"\n  L.O.R.E. Dashboard: {url}")
    print(f"  Serving files from: {ROOT}")
    print("  Press Ctrl+C to stop.\n")
    webbrowser.open(url)
    http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
