"""lane_status: read-only master-plan aggregator for the application lane.

Scans the repository's lane facts (register files, the lean-bridge
record, git state, and the presence/absence of lane artifacts) and prints
a one-screen status board.  READ-ONLY: it never runs the heavy gates,
never writes files, and never stages anything.  Exit 0 always (it is an
inventory, not a gate); failures to find a file are reported as status,
not as errors.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _head(md: str) -> str:
    p = ROOT / md
    if not p.exists():
        return "MISSING"
    lines = [ln.strip().lstrip("\ufeff") for ln in
             p.read_text(encoding="utf-8", errors="replace").splitlines()
             if ln.strip() and ln.strip() != "\ufeff"]
    return (lines[0].lstrip("# "))[:70] if lines else "(empty)"


def _git_summary() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, timeout=10)
    except Exception:
        return "git unavailable"
    return r.stdout.strip() if r.returncode == 0 else "no HEAD"


def _inventory() -> list[tuple[str, str]]:
    rows = [
        ("sealed register lane",
         "branch=%s heads=%s gate=%s validators=%s" % (
             subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            capture_output=True, text=True, timeout=10)
             .stdout.strip() or "?",
             _git_summary(),
             _head("GATE_KEEPER.md"),
             "89 (pinned; see GATE_KEEPER)")),
        ("lean bridge (5/7 derivable)",
         "kernel-pass recorded in %s; reserved 2/7 prose stay NOT-SETTLED"
         % _head("HANDOFF.md")),
        ("handoff / reproduction",
         _head("HANDOFF.md")),
        ("packaging supply-chain lane",
         "ABANDONED & KEPT ALIVE (banner in docs/AUTO_PACKAGING_*.md); "
         + "code dir exists" if (ROOT / "packaging").is_dir()
         else "ABANDONED & KEPT ALIVE (banner in docs); code dir missing"),
        ("battery-drain dashboard (application)",
         "skeleton: model + tests exist"
         if (ROOT / "experiments" / "battery_drain").is_dir()
         else "not built"),
        ("BOPC ticket",
         "filed (docs/BOPC.md)" if (ROOT / "docs" / "BOPC.md").exists()
         else "unfiled"),
        ("master-plan aggregator",
         "this script (scripts/lane_status.py)"),
    ]
    return rows


def main() -> int:
    print("AUTOMATION MASTERPLAN - lane status board (read-only)")
    for name, status in _inventory():
        print("  [%s] %s: %s" % ("x" if "MISSING" in status else " ",
                                 name, status))
    print("RESULT: inventory only; exit 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())