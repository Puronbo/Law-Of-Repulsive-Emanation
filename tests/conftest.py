"""Data-artifact preflight.

This repository gitignores ``data/*.json``, so a verification standard only
persists if it is either tracked or regenerable from a named script. When an
artifact is missing, ``load()`` in the test modules raises a bare
``FileNotFoundError`` -- which is indistinguishable from a proof that failed.

This preflight turns that into an explicit, actionable report:

  * ``puno_data_preflight`` -- reports coverage and the exact set of
    test-referenced artifacts that are neither tracked nor regenerable.
  * A session-level header printing the same summary.

The preflight is a *report*, not a gate: a clean checkout is expected to fail
here, and that failure is itself the finding. See ``PL-23`` in
``docs/PREDICTION_LEDGER.md`` and ``regen_data.py`` for the recovery path.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
MANIFEST = os.path.join(DATA, "DATA_MANIFEST.json")

sys.path.insert(0, ROOT)

try:
    import regen_data
except Exception:  # pragma: no cover - preflight must never break collection
    regen_data = None


def _collect():
    """Return (summary_dict, missing_list). Never raises."""
    if regen_data is None:
        return {"error": "regen_data.py not importable"}, []

    try:
        amap = regen_data.build_map()
        tracked = regen_data.tracked_files()
        buckets = regen_data.classify(amap=amap, tracked=tracked)
        refs = regen_data.test_refs()
    except Exception as exc:  # pragma: no cover
        return {"error": f"{type(exc).__name__}: {exc}"}, []

    recreatable = set(buckets.get("recreatable", []))
    tracked_set = set(tracked)

    referenced = set(refs or [])

    missing = sorted(
        n for n in referenced
        if n not in tracked_set and n not in recreatable
        and regen_data.find_data(n) is None
    )

    summary = {
        "tracked": len(tracked_set),
        "recreatable": len(recreatable),
        "unreproducible": len(buckets.get("unreproducible", [])),
        "referenced": len(referenced),
        "missing_load_bearing": len(missing),
    }
    return summary, missing


SUMMARY, MISSING = _collect()


def _line(text):
    print(text)


def pytest_report_header(config):
    if "error" in SUMMARY:
        return "data preflight: UNAVAILABLE (%s)" % SUMMARY["error"]
    return (
        "data preflight: {tracked} tracked / {recreatable} recreatable / "
        "{unreproducible} unreproducible; {referenced} test-referenced, "
        "{missing_load_bearing} with no tracked-or-regenerable source"
    ).format(**SUMMARY)


def pytest_sessionstart(session):
    """Announce the preflight unconditionally.

    ``addopts = -q`` suppresses ``pytest_report_header``, so a header-only
    guard would be invisible in the default invocation -- which is exactly the
    silent-no-op failure this module exists to prevent.
    """
    if "error" in SUMMARY:
        _line("data preflight: UNAVAILABLE (%s)" % SUMMARY["error"])
        return
    _line(
        "data preflight: %d tracked / %d recreatable / %d unreproducible; "
        "%d test-referenced, %d with no tracked-or-regenerable source"
        % (
            SUMMARY["tracked"],
            SUMMARY["recreatable"],
            SUMMARY["unreproducible"],
            SUMMARY["referenced"],
            SUMMARY["missing_load_bearing"],
        )
    )


def pytest_sessionfinish(session, exitstatus):
    if "error" in SUMMARY:
        _line("\ndata preflight unavailable: %s" % SUMMARY["error"])
        return
    if not MISSING:
        return
    _line("\n" + "=" * 70)
    _line(
        "DATA PREFLIGHT: %d test-referenced artifact(s) are absent and have no "
        "tracked or regenerable source." % len(MISSING)
    )
    _line(
        "A test reading one of these fails with FileNotFoundError. That is a "
        "PERSISTENCE failure, not a verdict failure."
    )
    _line("Recovery: python regen_data.py --regen-all   (rebuilds every missing regenerable artifact)")
    _line("         see PL-23 in docs/PREDICTION_LEDGER.md for the unrecovered remainder")
    for name in MISSING:
        _line("  - %s" % name)
    _line("=" * 70)


# NOTE: assertions live in tests/test_data_persistence.py, not here. pytest does
# not collect test functions from conftest.py during a normal `pytest tests/`
# run, so a test placed in this file would never execute.
