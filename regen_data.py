"""
regen_data.py - the persistence standard for data/ artifacts
============================================================

WHY THIS EXISTS
---------------
.data/*.json is gitignored (.gitignore:15, "Generated data artifacts"). That
is a sound design - generated data should not be stored - but it silently
assumed every artifact was REPRODUCIBLE. It was not, and nothing in the repo
recorded the mapping from artifact to generating script.

Consequences as of 2026-09-28, before this file:
  - 88 of 388 data/*.json files existed only on one machine and would vanish
  - 35 of those 88 are load-bearing: tests/test_solvable_theorems.py and
    friends read 250 distinct verdict JSONs, so 35 tests hard-fail on a fresh
    clone. "693 passed" was a property of the machine, not of the repository.
  - 17 of those 35 had NO discoverable generating script and were simply lost

This module makes "the standards do not persist" recoverable:
  1. builds the artifact -> script map by scanning sources for the
     `data/<name>.json` literal
  2. reports the three buckets: TRACKED / UNTRACKED-BUT-RECREATABLE /
     UNREPRODUCIBLE
  3. regenerates any named subset on demand

USAGE
-----
  python regen_data.py                      # coverage report
  python regen_data.py --unreproducible     # the lost ones, with no script
  python regen_data.py --regen chi_rho      # regenerate matching artifacts
  python regen_data.py --manifest           # write data/DATA_MANIFEST.json

NOTE ON SCALE (2026-09-28)
-------------------------
The gap is not random. The 17 unreproducible artifacts are the ones pinned to
absolute values rather than scale-free structure: information_conservation,
millennium, poincare, selberg_trace, riemann_roch, qft_0_over_0, and the
rest. The scale-free families - the 0/0 instances, the GUE/self-similar
probes - regenerate from their scripts. Everything here scales; chi and rho
do not, and neither, apparently, do the artifacts that depend on them.
"""

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
MANIFEST = os.path.join(DATA, "DATA_MANIFEST.json")

SKIP_DIRS = re.compile(
    r"sigma_venv|site-packages|archive|\.git\\|node_modules|__pycache__|\\data\\"
)
# Matches the artifact literal a script writes, e.g. OUT = "data/foo.json"
ARTIFACT_RE = re.compile(r"data/[A-Za-z0-9_\-]+\.json")


def _py_sources():
    """Every project .py file, excluding vendored trees."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        if rel == ".":
            dirnames[:] = [
                d for d in dirnames if not SKIP_DIRS.search(d + "\\")
            ]
        for fn in filenames:
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def build_map():
    """artifact filename -> sorted list of scripts that mention it."""
    out = {}
    for path in _py_sources():
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        for match in ARTIFACT_RE.findall(text):
            name = os.path.basename(match)
            out.setdefault(name, set()).add(
                os.path.relpath(path, ROOT).replace("\\", "/")
            )
    return {k: sorted(v) for k, v in out.items()}


def tracked_files():
    """Names of artifacts currently under git version control.

    Falls back to the committed manifest's ``tracked`` list when git is
    unavailable -- e.g. running from a ``git archive``/zip extraction, where
    ``git ls-files`` returns nothing and every artifact would otherwise look
    untracked. The manifest is the portable record of what is supposed to
    persist.
    """
    try:
        res = subprocess.run(
            ["git", "ls-files", "data"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        if res.returncode == 0 and res.stdout.strip():
            return {os.path.basename(l) for l in res.stdout.splitlines() if l.strip()}
    except (OSError, subprocess.SubprocessError):
        pass
    return manifest_tracked()


def manifest_tracked():
    """Tracked-artifact list recorded in the committed manifest, if readable."""
    if not os.path.exists(MANIFEST):
        return set()
    try:
        with open(MANIFEST, encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, ValueError):
        return set()
    return set(payload.get("tracked") or [])


def classify(amap=None, tracked=None):
    """Partition on-disk artifacts into the three persistence buckets."""
    amap = build_map() if amap is None else amap
    tracked = tracked_files() if tracked is None else tracked
    on_disk = sorted(
        f for f in os.listdir(DATA) if f.endswith(".json")
    ) if os.path.isdir(DATA) else []
    buckets = {"tracked": [], "recreatable": [], "unreproducible": []}
    for name in on_disk:
        if name in tracked:
            buckets["tracked"].append(name)
        elif amap.get(name):
            buckets["recreatable"].append(name)
        else:
            buckets["unreproducible"].append(name)
    return buckets


def report(buckets, refs=None, amap=None):
    total = sum(len(v) for v in buckets.values())
    print("=" * 72)
    print("DATA PERSISTENCE COVERAGE")
    print("=" * 72)
    print("  data/*.json is gitignored, so an artifact persists ONLY if it is")
    print("  tracked OR regenerable from a script. Third bucket is a real loss.")
    print()
    print("  on disk                      : %d" % total)
    print("  TRACKED in git                : %d" % len(buckets["tracked"]))
    print("  UNTRACKED but recreatable     : %d" % len(buckets["recreatable"]))
    print("  UNREPRODUCIBLE (no script)    : %d" % len(buckets["unreproducible"]))
    print()
    if refs:
        refset = set(refs)
        ref_lost = [n for n in buckets["unreproducible"] if n in refset]
        ref_ok = [n for n in buckets["recreatable"] if n in refset]
        # Referenced by the tests but absent from THIS machine as well. An
        # earlier version missed these entirely, because classify() only
        # buckets files present on disk - so HT-RUN-001.json was invisible.
        ref_absent = [n for n in refset
                      if not os.path.exists(os.path.join(DATA, n))]
        ref_absent_lost = [n for n in ref_absent if not amap.get(n)]
        print("  load-bearing for the test suite (referenced by tests/*.py):")
        print("    total referenced              : %d" % len(refset))
        print("    recreatable on a fresh clone : %d" % len(ref_ok))
        print("    UNREPRODUCIBLE (on disk)      : %d" % len(ref_lost))
        print("    UNREPRODUCIBLE (not on disk)  : %d  <- absent here too"
              % len(ref_absent_lost))
        if ref_absent:
            print("    referenced but missing locally:")
            for n in ref_absent:
                print("      %-46s %s" % (n, "LOST" if not amap.get(n)
                                         else "(rebuildable)"))
        print()
    if buckets["unreproducible"]:
        print("  LOST - no generating script found:")
        for n in buckets["unreproducible"]:
            mark = " [test depends on this]" if refs and n in set(refs) else ""
            print("    %s%s" % (n, mark))
        print()
    return total


def test_refs():
    """Data files the test suite loads, i.e. what a fresh clone would miss.

    Scans tests/ AND root-level test_*.py. An earlier version walked tests/
    only and undercounted the losses by one: HT-RUN-001.json is loaded by a
    root-level test file, so the tool reported 17 unreproducible when the true
    count against a fresh clone is 18. Verified by extracting HEAD and
    diffing the referenced set against the extracted data/ directory.
    """
    found = set()
    targets = []
    tests_dir = os.path.join(ROOT, "tests")
    if os.path.isdir(tests_dir):
        for dirpath, dirnames, filenames in os.walk(tests_dir):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            targets += [os.path.join(dirpath, f) for f in filenames
                        if f.endswith(".py")]
    try:
        targets += [os.path.join(ROOT, f) for f in os.listdir(ROOT)
                    if f.startswith("test_") and f.endswith(".py")]
    except OSError:
        pass
    for path in targets:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                found.update(re.findall(r"['\"]([A-Za-z0-9_\-]+\.json)['\"]",
                                       fh.read()))
        except OSError:
            continue
    return sorted(found)


def regenerate(pattern, amap, missing_only=False, only=None):
    """Re-run the generating script(s) for artifacts matching `pattern`.

    With ``missing_only`` (used by ``--regen-all``) the target set is narrowed
    to artifacts that are regenerable but NOT currently on disk, so a fresh
    clone rebuilds exactly what it lacks instead of re-running all 300+ scripts.
    ``only`` further restricts to an explicit set of names (the test-referenced
    load-bearing set), which is what a clone actually needs to make its suite
    meaningful.
    """
    import fnmatch
    targets = [n for n in amap if fnmatch.fnmatch(n, "*%s*" % pattern)]
    if only is not None:
        targets = [n for n in targets if n in only]
    if missing_only:
        targets = [n for n in targets if not os.path.exists(os.path.join(DATA, n))]
    if not targets:
        print("no artifact matches %r" % pattern)
        return 1
    print("%d artifact(s) to regenerate" % len(targets))
    failures = 0
    for name in targets:
        for script in amap[name]:
            print("-" * 72)
            print("regenerating %s  <-  %s" % (name, script))
            try:
                res = subprocess.run(
                    [sys.executable, script], cwd=ROOT, timeout=1800,
                )
            except subprocess.TimeoutExpired:
                print("  TIMEOUT")
                failures += 1
                continue
            if res.returncode != 0:
                print("  FAILED (exit %d)" % res.returncode)
                failures += 1
            else:
                print("  ok")
    print("-" * 72)
    print("%d script run(s), %d failure(s)" % (len(targets), failures))
    return failures


def write_manifest(amap, buckets):
    os.makedirs(DATA, exist_ok=True)
    payload = {
        "generated_by": "regen_data.py --manifest",
        "note": (
            "Machine-readable artifact -> script map so that a fresh clone can "
            "recreate its verification standards. See regen_data.py."
        ),
        "persistence_rule": (
            "data/*.json is gitignored; an artifact persists only if listed "
            "under 'tracked' or regenerable from 'scripts'. Anything under "
            "'unreproducible' is a real loss and must be recovered by hand."
        ),
        "counts": {k: len(v) for k, v in buckets.items()},
        "unreproducible": buckets["unreproducible"],
        "recreatable": buckets["recreatable"],
        "tracked": buckets["tracked"],
        "scripts": amap,
    }
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("wrote %s (%d scripts mapped)" % (
        os.path.relpath(MANIFEST, ROOT), len(amap)))
    return MANIFEST


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Report or repair data/ persistence for this repo.")
    ap.add_argument("--regen", metavar="PATTERN",
                    help="regenerate artifacts matching PATTERN")
    ap.add_argument("--regen-all", action="store_true",
                    help="regenerate every MISSING regenerable artifact "
                         "(one-command recovery for a fresh clone)")
    ap.add_argument("--unreproducible", action="store_true",
                    help="list only the artifacts that cannot be recreated")
    ap.add_argument("--manifest", action="store_true",
                    help="write data/DATA_MANIFEST.json")
    ap.add_argument("--no-test-refs", action="store_true",
                    help="skip the test-dependency cross-check")
    args = ap.parse_args(argv)

    amap = build_map()
    buckets = classify(amap)

    if args.unreproducible:
        for n in buckets["unreproducible"]:
            print(n)
        return 0
    if args.regen:
        return regenerate(args.regen, amap)
    if args.regen_all:
        # Only the test-referenced set: those are what the suite reads, so
        # those are what a clone needs to make its verdict meaningful.
        return regenerate("", amap, missing_only=True, only=set(test_refs()))

    refs = None if args.no_test_refs else test_refs()
    report(buckets, refs, amap)
    if args.manifest:
        write_manifest(amap, buckets)
    return 0


if __name__ == "__main__":
    sys.exit(main())
