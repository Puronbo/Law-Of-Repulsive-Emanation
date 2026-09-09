"""run_all_audits.py: one-command certification of the whole suite.

Runs the unit test suite and every root validator, and prints a
PASS/FAIL register.  Exit code 0 iff everything passed.
"""
from __future__ import annotations

import glob
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(cmd: list[str]) -> bool:
    p = subprocess.run(cmd, cwd=str(ROOT),
                       capture_output=True, text=True)
    return p.returncode == 0


def main() -> int:
    validators = sorted(glob.glob(str(ROOT / "validate_*.py")))
    suite = [("pytest (unit)", ["python", "-m", "pytest",
                                "soliton_eca", "-q"])]
    suite += [(Path(v).stem, ["python", str(v)]) for v in validators]

    fails = 0
    print("\n=== soliton-eca certification register ===")
    for name, cmd in suite:
        ok = run(cmd)
        if not ok:
            fails += 1
        print("  %-42s %s" % (name, "PASS" if ok else "FAIL"))
    print("  %d/%d registered checks passed"
          % (len(suite) - fails, len(suite)))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())