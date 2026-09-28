"""Data-artifact persistence gate.

Lives in a real test module, not ``conftest.py``: pytest does not collect test
functions from ``conftest.py`` during a normal ``pytest tests/`` run, so a test
placed there is a silent no-op. ``conftest.py`` holds only the session hooks
that *report* coverage; the assertions live here.

See ``PL-23`` in ``docs/PREDICTION_LEDGER.md`` and ``regen_data.py``.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import regen_data  # noqa: E402

# Audited ceilings, from PL-23. These are ratchets, not aspirations: each one
# fails only if the situation gets WORSE than the recorded state. They exist so
# that silent data loss is caught by the suite instead of by whoever clones
# next. Tighten them when the underlying set actually shrinks.
AUDITED_UNRECOVERABLE_LOAD_BEARING = 18
AUDITED_TRACKED_WITHOUT_GENERATOR = 66


def test_manifest_exists_and_is_loadable():
    """The manifest is the persistence contract; it must be readable."""
    path = os.path.join(DATA, "DATA_MANIFEST.json")
    assert os.path.exists(path), (
        "data/DATA_MANIFEST.json is missing. It must be committed -- it is the "
        "record of which artifacts are tracked and which are regenerable."
    )
    with open(path, encoding="utf-8") as fh:
        manifest = json.load(fh)
    assert manifest.get("scripts"), "manifest has no artifact -> script mapping"
    assert "counts" in manifest, "manifest has no counts block"


def test_test_ref_scanner_is_working():
    """Guard the guard: a broken scanner would under-report every loss below."""
    referenced = regen_data.test_refs()
    assert len(referenced) >= 200, (
        "test_refs() found only %d artifacts; the scanner is probably broken, "
        "which would make every other number in this file meaningless."
        % len(referenced)
    )


def test_load_bearing_artifact_loss_does_not_regress():
    """PL-23's central claim: a suite result must not depend on the machine.

    A test-referenced artifact must be tracked, or regenerable from a named
    script, or present. This is a ratchet on the documented losses -- it fires
    only if the count climbs above the audited ceiling.

    Note the ``os.path.exists`` escape hatch. On the machine that recorded the
    losses the 18 files are still on disk, so they do not count here; in a
    clean clone they do. The assertion therefore binds in the clone, which is
    where it matters, and reports 0 on a repaired checkout.
    """
    amap = regen_data.build_map()
    tracked = set(regen_data.tracked_files())
    referenced = set(regen_data.test_refs())

    unrecoverable = sorted(
        name
        for name in referenced
        if name not in tracked
        and not amap.get(name)
        and not os.path.exists(os.path.join(DATA, name))
    )

    assert len(unrecoverable) <= AUDITED_UNRECOVERABLE_LOAD_BEARING, (
        "data persistence REGRESSED: %d test-referenced artifacts have no "
        "tracked or regenerable source, above the audited ceiling of %d (PL-23). "
        "Offenders: %s"
        % (
            len(unrecoverable),
            AUDITED_UNRECOVERABLE_LOAD_BEARING,
            unrecoverable,
        )
    )


def test_fresh_clone_would_not_depend_on_this_machine():
    """The machine-independence claim, stated as a checkable partition.

    Simulates a clean clone and asks the only question that matters: after a
    one-command recovery (``python regen_data.py --regen-all``), what would a
    fresh clone STILL be missing?

    The answer must be the artifacts with no generating script at all. The
    regenerable ones do not count -- they are one command away, which is the
    whole point of shipping regen_data.py and the manifest. Budget: the 18
    audited losses in PL-23.
    """
    amap = regen_data.build_map()
    tracked = set(regen_data.tracked_files())
    referenced = set(regen_data.test_refs())

    # Not present on disk AND not regenerable == unrecoverable in a clone.
    unrecoverable = sorted(
        name for name in referenced
        if name not in tracked and not amap.get(name)
    )

    assert len(unrecoverable) <= AUDITED_UNRECOVERABLE_LOAD_BEARING, (
        "after a full --regen-all recovery a fresh clone would still be missing "
        "%d test-referenced artifacts (budget %d, PL-23): %s"
        % (len(unrecoverable), AUDITED_UNRECOVERABLE_LOAD_BEARING, unrecoverable)
    )
    # A broken amap would make 'unrecoverable' equal the whole referenced set
    # and trip the budget for the wrong reason, so require the tool to explain
    # the bulk of the set.
    explained = sum(1 for n in referenced if n in tracked or amap.get(n))
    assert explained > 0.5 * len(referenced), (
        "regen_data.build_map() + git explained only %d of %d referenced "
        "artifacts; the ratchet above would be meaningless"
        % (explained, len(referenced))
    )


def test_tracked_artifacts_without_a_generator_do_not_regress():
    """66 tracked artifacts have no discoverable generating script.

    They are safe -- git holds them -- but if they were ever lost they could
    not be rebuilt. Recorded here so the number cannot quietly climb. Drop the
    constant as generators are recovered.
    """
    amap = regen_data.build_map()
    tracked = set(regen_data.tracked_files())
    unexplained = sorted(n for n in tracked if not amap.get(n))
    assert len(unexplained) <= AUDITED_TRACKED_WITHOUT_GENERATOR, (
        "tracked artifacts without a generating script rose to %d, above the "
        "audited %d: %s"
        % (
            len(unexplained),
            AUDITED_TRACKED_WITHOUT_GENERATOR,
            unexplained,
        )
    )
