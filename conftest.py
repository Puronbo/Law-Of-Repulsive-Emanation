"""Repository-root pytest configuration.

Two jobs:

1. Put the project's importable packages on ``sys.path``. The numbered-directory
   reorganization moved ``puno_flow``/``puno_app``/``Universals`` under
   ``01_Core_Mathematical_Framework_Lean/01_Lean`` and ``regen_data.py`` under
   ``07_.../02_Mathematical_Physics_Connections``, so the old "everything sits
   next to the root conftest" assumption no longer holds and collection fails
   with ``ModuleNotFoundError`` before a single test runs.

2. Run the data-artifact preflight. Generated artifacts are not committed;
   a verification standard only persists if it is either tracked or
   regenerable from a named script. When an artifact is missing, ``load()`` in
   a test module raises a bare ``FileNotFoundError`` -- which is
   indistinguishable from a proof that failed. The preflight turns that into an
   explicit, actionable report.

The preflight is a *report*, not a gate: a clean checkout is expected to fail
here, and that failure is itself the finding. See ``PL-23`` in the prediction
ledger and ``regen_data.py`` for the recovery path.
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# Directories that hold importable project packages / tooling after the
# reorganization.
_PACKAGE_ROOTS = (
    ROOT,
    os.path.join(ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean"),
    # Holds the `packaging` package imported as `packaging.utilities`.
    os.path.join(
        ROOT,
        "06_Configuration_and_Metadata",
        "02_Data_Manifest_and_Processing",
    ),
    os.path.join(
        ROOT,
        "07_Interdisciplinary_Connections_and_Frameworks",
        "02_Mathematical_Physics_Connections",
    ),
)


def _topic_dirs():
    """Every per-topic subdirectory of the experiments tree.

    Test modules import experiment scripts by bare module name
    (``import rh_newman_flow_h1``), which used to work because all ~370 scripts
    shared one flat ``experiments/`` directory. They are now split across
    per-topic directories, so each has to be importable on its own.
    """
    base = os.path.join(ROOT, "02_Experimental_Implementations_and_Verification")
    if not os.path.isdir(base):
        return ()
    out = [base]
    for name in sorted(os.listdir(base)):
        path = os.path.join(base, name)
        if os.path.isdir(path) and name != "__pycache__":
            out.append(path)
    return tuple(out)


_PACKAGE_DIRS = _PACKAGE_ROOTS + _topic_dirs()

for _d in _PACKAGE_DIRS:
    if os.path.isdir(_d) and _d not in sys.path:
        sys.path.insert(0, _d)

# regen_data.py lives outside the root; expose it under its own name so the
# preflight below can import it.
try:
    import regen_data  # noqa: E402
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
        n
        for n in referenced
        if n not in tracked_set
        and n not in recreatable
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

    ``addopts = -q`` suppresses ``pytest_report_header``, so a header-only guard
    would be invisible in the default invocation -- which is exactly the
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
    _line(
        "Recovery: python regen_data.py --regen-all   (rebuilds every missing "
        "regenerable artifact)"
    )
    for name in MISSING:
        _line("  - %s" % name)
    _line("=" * 70)
