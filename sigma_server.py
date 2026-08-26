"""
Sigma Standalone Server
========================

Serves the Sigma web application with zero dependencies.
Pure Python 3 stdlib. No pip install needed.

Usage:
    python sigma_server.py
    # Open http://localhost:8000 in any browser

Options:
    --port PORT    Port to serve on (default: 8000)
    --host HOST    Host to bind to (default: 0.0.0.0)
    --open         Open browser automatically

Author: Michael Grafiel S Puno
Repository: https://github.com/Puronbo/Law-Of-Repulsive-Emanation
"""

import http.server
import socketserver
import os
import sys
import webbrowser
import threading
import argparse


class SigmaHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler that serves the Sigma webapp."""
    
    def __init__(self, *args, **kwargs):
        # Serve from the webapp directory
        webapp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webapp')
        super().__init__(*args, directory=webapp_dir, **kwargs)
    
    def do_GET(self):
        # Serve sigma.html for root
        if self.path == '/' or self.path == '':
            self.path = '/sigma.html'
        super().do_GET()
    
    def log_message(self, format, *args):
        # Colorful logging
        if '200' in str(args):
            sys.stdout.write("\033[32m[OK]\033[0m ")
        elif '404' in str(args):
            sys.stdout.write("\033[31m[404]\033[0m ")
        else:
            sys.stdout.write("[--] ")
        sys.stdout.write(format % args + "\n")
        sys.stdout.flush()


def open_browser(port):
    """Open browser after a short delay."""
    import time
    time.sleep(1)
    webbrowser.open('http://localhost:%d' % port)


def main():
    parser = argparse.ArgumentParser(description='Sigma Standalone Server')
    parser.add_argument('--port', type=int, default=8000, help='Port (default: 8000)')
    parser.add_argument('--host', default='0.0.0.0', help='Host (default: 0.0.0.0)')
    parser.add_argument('--open', action='store_true', help='Open browser automatically')
    args = parser.parse_args()
    
    webapp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webapp')
    if not os.path.exists(os.path.join(webapp_dir, 'sigma.html')):
        print("ERROR: webapp/sigma.html not found.")
        print("Run: python _gen_webapp.py")
        sys.exit(1)
    
    with socketserver.TCPServer((args.host, args.port), SigmaHandler) as httpd:
        print("=" * 60)
        print("SIGMA: The Removable Singularity Chassis")
        print("=" * 60)
        print()
        print("  Serving: %s" % webapp_dir)
        print("  URL:     http://localhost:%d" % args.port)
        print("  Host:    %s" % args.host)
        print()
        print("  No API keys. No dependencies. Self-contained.")
        print()
        print("  Press Ctrl+C to stop.")
        print()
        
        if args.open:
            t = threading.Thread(target=open_browser, args=(args.port,))
            t.daemon = True
            t.start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
