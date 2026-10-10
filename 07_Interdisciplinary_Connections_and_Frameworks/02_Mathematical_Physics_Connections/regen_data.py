"""
regen_data.py - the persistence standard for data/ artifacts
============================================================

WHY THIS EXISTS
---------------
data/*.json artifacts are generated output and are not meant to be committed.
The repo no longer carries a root `.gitignore`; the manifest itself
(`DATA_MANIFEST.json`, this module) is the persistence record: an artifact
persists only if it is listed under ``tracked`` or regenerable from a script
listed under ``scripts``. ``tracked`` is derived from ``git ls-files``; after
the 2026-10 reorganization the committed copies live under legacy `data/` and
`experiments/data/` paths while the live central collection is the
`03_Data_and_Observational_Resources/02_Experimental_Data_Collections` root,
so untracked-but-regenerable and unreproducible are exactly the two buckets
that matter on a fresh clone.

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

HERE = os.path.dirname(os.path.abspath(__file__))
# This script lives two directories below the repository root
# (07_Interdisciplinary_Connections_and_Frameworks/02_Mathematical_Physics_Connections).
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(
    ROOT,
    "03_Data_and_Observational_Resources",
    "02_Experimental_Data_Collections",
)
MANIFEST = os.path.join(DATA, "DATA_MANIFEST.json")

SKIP_DIRS = re.compile(
       r"sigma_venv|site-packages|[Aa]rchive|\.git\\|node_modules|__pycache__"
       r"|\.lake\\|worktrees|Folding-Calculus|fcc2|sigma_venv|[Bb]uild\\|[Dd]ist\\"
   )
# Matches the artifact literal a script writes, e.g. OUT = "data/gate_data.json"
ARTIFACT_RE = re.compile(r"data/[A-Za-z0-9_\-]+\.json")

# Scripts that build their output path with `os.path.join(<dir>, "name.json")`
# rather than a literal `data/name.json` string. `ARTIFACT_RE` is deliberately
# narrow -- a looser pattern would also match artifacts a script merely READS,
# which would convert a genuine loss into a false "recreatable" claim -- so
# these are listed explicitly instead. Each entry is a script that WRITES the
# named artifact; a script that only reads one is not listed, because being able
# to read an artifact is not the same as being able to recreate it.
#
# `prebiotic_0over0.py` is here under the name it actually writes
# (`prebiotic_origin.json`), which is not derivable from the script's filename.
EXTRA_SOURCES = {
    "02_Experimental_Implementations_and_Verification/"
    "04_Acoustic_Zero_Flow_Experiments/acoustic_geometry.py": [
        "acoustic_geometry.json",
    ],
    "02_Experimental_Implementations_and_Verification/"
    "04_Acoustic_Zero_Flow_Experiments/sound_horizon_calculation.py": [
        "sound_horizon_calculation.json",
    ],
    "02_Experimental_Implementations_and_Verification/"
    "06_Miscellaneous_Experiments/big_bang_origin.py": [
        "big_bang_origin.json",
    ],
    "02_Experimental_Implementations_and_Verification/"
    "06_Miscellaneous_Experiments/first_cause.py": [
        "first_cause.json",
    ],
    "02_Experimental_Implementations_and_Verification/"
    "06_Miscellaneous_Experiments/prebiotic_0over0.py": [
        "prebiotic_origin.json",
    ],
    "02_Experimental_Implementations_and_Verification/"
    "06_Miscellaneous_Experiments/origin_matrix.py": [
        "origin_matrix.json",
    ],
    "02_Experimental_Implementations_and_Verification/"
    "experiments/stability_harness.py": [
        "stability_harness.json",
    ],
    # Toomre/spiral companions build their output path with
    # `os.path.join(OUTPUT_DIR, "<name>.json")`, so `ARTIFACT_RE` cannot see
    # them even though they regenerate their artifacts deterministically
    # (verified 2026-10-07: byte-identical reruns, timestamps excepted).
    "02_Experimental_Implementations_and_Verification/"
    "06_Miscellaneous_Experiments/toomre_critical.py": [
        "toomre_critical_corrected.json",
    ],
    "02_Experimental_Implementations_and_Verification/"
    "06_Miscellaneous_Experiments/toomre_universal.py": [
        "toomre_universal.json",
    ],
    "02_Experimental_Implementations_and_Verification/"
    "06_Miscellaneous_Experiments/spiral_mass_gap.py": [
        "spiral_mass_gap.json",
    ],
}


def _dark_energy_sources():
    """Artifacts emitted by `02_Dark_Energy_0_0_Framework` scripts.

    Each `*_0_over_0.py` finishes by writing ``<name>_data.json`` to a data
    directory resolved relative to the script's own path
    (``Path(__file__).resolve().parent.parent / 'data' / '<name>_data.json'``),
    so the emitted literal never contains ``data/<name>.json`` and
    `ARTIFACT_RE` cannot see it. An earlier gate required the text to contain
    ``_central_data_dir()``, which no current script uses -- the function
    silently mapped nothing and every one of these artifacts looked
    unreproducible. Detection now keys on the emit line: a quoted ``data``
    directory token and quoted ``*_data.json`` names on the same line.
    """
    out = {}
    d = os.path.join("02_Experimental_Implementations_and_Verification",
                     "02_Dark_Energy_0_0_Framework")
    _EMIT = re.compile(r"""['"]([\w-]+_data\.json)['"]""")
    try:
        entries = sorted(os.listdir(os.path.join(ROOT, d)))
    except OSError:
        return out
    for fn in entries:
        if not fn.endswith(".py"):
            continue
        try:
            with open(os.path.join(ROOT, d, fn), "r", encoding="utf-8",
                      errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        names = []
        for line in text.splitlines():
            if "'data'" not in line and '"data"' not in line:
                continue
            names.extend(_EMIT.findall(line))
        if not names and "_central_data_dir()" in text:
            m = re.search(r"""["']([a-z0-9_]+_data\.json)["']""", text)
            if m:
                names = [m.group(1)]
        key = (d + "/" + fn).replace("\\", "/")
        for name in dict.fromkeys(names):
            out.setdefault(name, []).append(key)
    return out


for _name, _scripts in _dark_energy_sources().items():
    for _script in _scripts:
        EXTRA_SOURCES.setdefault(_script, []).append(_name)


def _discover_data_roots():
    """Every `data` directory in the project, excluding vendored trees.

    The reorganization scattered the experiment scripts across the numbered
    top-level directories, so each one now emits its artifact next to itself
    rather than into a single shared `experiments/data`. Resolution has to look
    wherever a `data` directory actually is, or a test that reads an experiment
    artifact is reported as unsourced.
    """
    found = set()
    for dirpath, dirnames, _ in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not SKIP_DIRS.search(d + "\\")]
        if os.path.basename(dirpath).lower() == "data":
            found.add(dirpath)
    return tuple(sorted(found))


DATA_ROOTS = (DATA,) + tuple(r for r in _discover_data_roots() if r != DATA)


def _py_sources():
    """Every project .py file, excluding vendored trees.

    SKIP_DIRS is applied at EVERY depth, not just at the root. Pruning only
    when `rel == "."` let the walk descend into `.claude/worktrees/` and
    `02_Data_Manifest_and_Processing/build/`, so ~14200 of the 18585 "generating
    scripts" were stale agent worktrees, archive copies, and build output.
    That is unsound provenance rather than a rounding error: an artifact could
    be classed "recreatable" purely because a dead worktree copy of a script
    happened to mention its path.
    """
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not SKIP_DIRS.search(d + "\\")]
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
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        for match in ARTIFACT_RE.findall(text):
            out.setdefault(os.path.basename(match), set()).add(rel)
        for name in EXTRA_SOURCES.get(rel, ()):
            out.setdefault(name, set()).add(rel)
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
            ["git", "ls-files"],
            cwd=ROOT, capture_output=True, text=True, timeout=300,
        )
        if res.returncode == 0 and res.stdout.strip():
            rel_roots = {
                os.path.relpath(r, ROOT).replace("\\", "/") for r in DATA_ROOTS
            }
            names = set()
            for line in res.stdout.splitlines():
                line = line.strip()
                if line and os.path.dirname(line).replace("\\", "/") in rel_roots:
                    names.add(os.path.basename(line))
            if names:
                return names
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


def _iter_artifacts(root):
    """Yield every *.json under a data root, shallowest files first.

    Resolution has to DESCEND. Four artifacts live one level below a data
    root -- `human_trial_runs/HT-RUN-001.json` plus three in `school_data/` --
    and a top-level-only scan reported them as absent from the machine. That
    was a false loss: HT-RUN-001 was present and readable the whole time, and
    `tests/test_human_trial.py` reads it with the subdirectory included, so the
    suite passed while the audit reported the file missing.

    Breadth-first, so a top-level artifact still wins over a same-named one
    nested deeper -- that preserves the previous resolution order for the 500+
    files that were always visible.
    """
    if not os.path.isdir(root):
        return
    queue = [root]
    head = 0
    while head < len(queue):
        cur = queue[head]
        head += 1
        try:
            entries = sorted(os.listdir(cur))
        except OSError:
            continue
        subdirs = []
        for name in entries:
            full = os.path.join(cur, name)
            if os.path.isdir(full):
                if not SKIP_DIRS.search(os.path.basename(full)):
                    subdirs.append(full)
            elif name.endswith(".json"):
                yield full
        queue.extend(subdirs)


def find_data(name):
    """Absolute path of an artifact in any data root, or None.

    Matches on basename, which is the form `test_refs()` yields. Shallowest
    match wins; ties across data roots resolve in DATA_ROOTS order.
    """
    base = os.path.basename(name)
    for root in DATA_ROOTS:
        for path in _iter_artifacts(root):
            if os.path.basename(path) == base:
                return path
    return None


def classify(amap=None, tracked=None):
    """Partition on-disk artifacts into the three persistence buckets."""
    amap = build_map() if amap is None else amap
    tracked = tracked_files() if tracked is None else tracked
    names = set()
    for root in DATA_ROOTS:
        for path in _iter_artifacts(root):
            names.add(os.path.basename(path))
    buckets = {"tracked": [], "recreatable": [], "unreproducible": []}
    for name in sorted(names):
        if name in tracked:
            buckets["tracked"].append(name)
        elif amap.get(name):
            buckets["recreatable"].append(name)
        else:
            buckets["unreproducible"].append(name)
    return buckets


def ambiguous_names():
    """Basenames that exist at more than one path under the data roots.

    Buckets are keyed by basename, so two same-named artifacts in different
    data roots would be silently merged and whichever won `find_data()` would
    stand for both. Surfaced rather than hidden: it is a measurement of the
    layout, not an error to fix automatically.
    """
    seen = {}
    for root in DATA_ROOTS:
        for path in _iter_artifacts(root):
            seen.setdefault(os.path.basename(path), []).append(path)
    return {n: ps for n, ps in seen.items() if len(ps) > 1}


def nested_artifacts():
    """Artifacts that live BELOW a data root (one level in or deeper)."""
    out = []
    for root in DATA_ROOTS:
        base_depth = len(root.rstrip("\\/").split(os.sep))
        for path in _iter_artifacts(root):
            depth = len(os.path.abspath(path).split(os.sep))
            if depth > base_depth + 1:
                out.append(path)
    return sorted(out)


def report(buckets, refs=None, amap=None):
    total = sum(len(v) for v in buckets.values())
    print("=" * 72)
    print("DATA PERSISTENCE COVERAGE")
    print("=" * 72)
    print("  generated artifacts are not committed; an artifact persists ONLY")
    print("  if it is tracked OR regenerable from a script. Third bucket is a")
    print("  real loss.")
    print()
    print("  on disk                      : %d" % total)
    print("  TRACKED in git                : %d" % len(buckets["tracked"]))
    print("  UNTRACKED but recreatable     : %d" % len(buckets["recreatable"]))
    print("  UNREPRODUCIBLE (no script)    : %d" % len(buckets["unreproducible"]))
    nested = nested_artifacts()
    if nested:
        print()
        print("  NESTED below a data root     : %d  (in the totals above)"
              % len(nested))
        for p in nested:
            print("      %s" % os.path.relpath(p, ROOT).replace("\\", "/"))
    amb = ambiguous_names()
    if amb:
        print()
        print("  SAME-NAMED in >1 location    : %d" % len(amb))
        for n, ps in sorted(amb.items()):
            print("      %s" % n)
            for p in ps:
                print("          %s" % os.path.relpath(p, ROOT).replace("\\", "/"))
    print()
    if refs:
        refset = set(refs)
        ref_lost = [n for n in buckets["unreproducible"] if n in refset]
        ref_ok = [n for n in buckets["recreatable"] if n in refset]
        # Referenced by the tests but absent from THIS machine as well. An
        # earlier version missed these entirely, because classify() only
        # buckets files present on disk - so HT-RUN-001.json was invisible.
        ref_absent = [n for n in refset
                      if not find_data(n)]
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
    # Tests now live under 04_Testing_and_Validation_Suite/<topic>/, so scan
    # that tree rather than a single top-level tests/ directory.
    tests_dir = os.path.join(ROOT, "04_Testing_and_Validation_Suite")
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
        targets = [n for n in targets if not find_data(n)]
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
            "Generated artifacts are not committed; an artifact persists only "
            "if listed under 'tracked' or regenerable from 'scripts'. Anything "
            "under 'unreproducible' is a real loss and must be recovered by "
            "hand."
        ),
        "counts": {k: len(v) for k, v in buckets.items()},
        "unreproducible": buckets["unreproducible"],
        "recreatable": buckets["recreatable"],
        "tracked": buckets["tracked"],
        "scripts": amap,
    }
    # newline="\n" pins LF so the manifest is byte-identical on Windows and
    # POSIX; text mode would otherwise translate to CRLF on this platform.
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
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
