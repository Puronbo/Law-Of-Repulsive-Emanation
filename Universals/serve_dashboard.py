#!/usr/bin/env python3
"""
serve_dashboard.py
==================
Start a local HTTP server for the L.O.R.E. dashboard.
Opens http://localhost:8080 in your default browser.

Usage:  python serve_dashboard.py  [port]
"""

import http.server
import webbrowser
import sys
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
DIR = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)


if __name__ == "__main__":
    url = f"http://localhost:{PORT}"
    print(f"\n  L.O.R.E. Dashboard: {url}")
    print(f"  Serving files from: {DIR}")
    print("  Press Ctrl+C to stop.\n")
    webbrowser.open(url)
    http.server.HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
