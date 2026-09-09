"""run_all_audits.py: one-command certification of the whole suite.

Runs the unit test suite and every root validator, and prints a
PASS/FAIL register.  Exit code 0 iff everything passed.

The docs (README.md, Soliton-Bus Elementary Cellular Automata.md) pin
the count at "86 root validators" / "87-check suite".  The constant
PINCED_VALIDATORS below enforces that pin: if the on-disk validator
count ever drifts, this script prints an explicit FAIL line and exits
non-zero *even if every individual check passed*.

One-command contract:
    python run_all_audits.py
    # -> 87/87 registered checks passed  +  pinned: 86 validators … (OK)
"""
from __future__ import annotations

import glob
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PINCED_VALIDATORS = 86


def run(cmd: list[str]) -> bool:
    p = subprocess.run(cmd, cwd=str(ROOT),
                       capture_output=True, text=True)
    return p.returncode == 0


def main() -> int:
    validators = sorted(glob.glob(str(ROOT / "validate_*.py")))
    n_validators = len(validators)
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

    if n_validators != PINCED_VALIDATORS:
        print("  FAIL: expected %d validators, found %d"
              % (PINCED_VALIDATORS, n_validators))
        return 1
    print("  pinned: %d validators + 1 unit suite = %d registered checks (OK)"
          % (PINCED_VALIDATORS, PINCED_VALIDATORS + 1))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())