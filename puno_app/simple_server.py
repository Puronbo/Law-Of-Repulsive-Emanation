"""Puno lab - alias entry point for the canned UI server.

Runs the same stdlib HTTP server as puno_app.canned_ui with a friendlier
name.  Use:

    python -m puno_app.simple_server [--host 127.0.0.1] [--port 8765]
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from puno_app.canned_ui import main  # noqa: E402

if __name__ == "__main__":
    main()
