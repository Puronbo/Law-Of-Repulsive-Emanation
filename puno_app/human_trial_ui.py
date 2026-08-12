"""T74 human trial runner - stdlib HTTP server + single-file browser app.

Serves the interactive learning & creativity trial built from the T74 trial
package (docs/HUMAN_TRAIL_INSTRUMENT.md, docs/LEARNING_CREATIVITY_TEST.md):

    python -m puno_app.human_trial_ui [--host 127.0.0.1] [--port 8790]

Endpoints:
    GET  /             - the single-page trial app
    GET  /api/session  - the deterministic session plan (probes, prompts)
    POST /api/score    - grade recorded answers with score_participant()
                         (the SAME code that grades the machine)

Run the trial in a browser, download the answers JSON, and score it - either
here (POST /api/score) or with experiments/human_trial_pilot.py.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # noqa

from puno_app.human_trial import build_answers, build_session, grade  # noqa

HERE = Path(__file__).resolve().parent
HTML = (HERE / "human_trial.html").read_text(encoding="utf-8")


def make_server(host="127.0.0.1", port=8790, session_seed=20260812):
    session = build_session(seed=session_seed)

    class Handler(BaseHTTPRequestHandler):
        server_version = "HumanTrial/1.0"

        def log_message(self, fmt, *args):
            sys.stderr.write("human_trial: %s\n" % (fmt % args))

        def _send(self, code, body, ctype="application/json"):
            if isinstance(body, (dict, list)):
                body = json.dumps(body).encode("utf-8")
            elif isinstance(body, str):
                body = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/" or self.path == "/index.html":
                self._send(200, HTML, "text/html; charset=utf-8")
            elif self.path == "/api/session":
                self._send(200, session)
            else:
                self._send(404, {"ok": False, "error": "not found"})

        def do_POST(self):
            if self.path != "/api/score":
                self._send(404, {"ok": False, "error": "not found"})
                return
            length = int(self.headers.get("Content-Length", 0))
            try:
                answers = json.loads(self.rfile.read(length).decode("utf-8"))
                result = grade(session, answers)
            except Exception as exc:  # noqa: BLE001 - surface to the client
                self._send(400, {"ok": False, "error": str(exc)})
                return
            result["ok"] = True
            self._send(200, result)

    return ThreadingHTTPServer((host, port), Handler)


def main(argv=None):
    ap = argparse.ArgumentParser(description="T74 human trial runner")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8790)
    ap.add_argument("--session-seed", type=int, default=20260812)
    args = ap.parse_args(argv)
    srv = make_server(args.host, args.port, args.session_seed)
    url = "http://%s:%d/" % (args.host, srv.server_address[1])
    print("T74 human trial: open %s in a browser" % url)
    print("  learn the 8 species, route held-out probes, place creative items")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
