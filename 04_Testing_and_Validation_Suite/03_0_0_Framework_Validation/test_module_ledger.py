"""Module ledger: every Lean module is classified exactly once and actually built.

`CLAIM_TRACEABILITY.md` links the *carded* modules, but a module could silently
exist outside that map, never imported by the library root and never built. This
checker closes that hole. `MODULE_LEDGER.md` classifies every module under
``.../01_Lean/PunoCalculus/`` (recursively) by category and, for card modules, by
the claim card(s) it carries. The checker asserts:

1. every module on disk appears in the ledger, and every ledger entry exists on
   disk (no phantoms, no gaps);
2. every category is one of the legend's;
3. a module the traceability checker maps to a card is tagged ``card`` in the
   ledger, with exactly the card IDs the traceability map assigns it, and every
   such ID is a real token in that map;
4. every module is imported by the library root ``PunoCalculus.lean`` (so
   ``lake build PunoCalculus`` compiles all of it).

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_module_ledger.py -q
"""

import importlib.util
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEAN_DIR = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus"
)
LEAN_ROOT = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus.lean"
)
LEDGER = os.path.join(
    ROOT, "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation", "MODULE_LEDGER.md",
)
CHECKER = os.path.join(
    ROOT, "04_Testing_and_Validation_Suite", "03_0_0_Framework_Validation",
    "test_claim_traceability.py",
)

CATEGORIES = {
    "card", "millennium-cert", "rh-research", "number-theory-cert",
    "fluid-diagnostic", "numerical-cert", "cosmology", "core-scaffold",
}


def _read(path):
    with open(path, encoding="utf-8") as fp:
        return fp.read()


def _entries():
    spec = importlib.util.spec_from_file_location("tct", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ENTRIES


def _disk_modules():
    mods = set()
    for dirpath, _, filenames in os.walk(LEAN_DIR):
        for name in filenames:
            if name.endswith(".lean"):
                rel = os.path.relpath(os.path.join(dirpath, name), LEAN_DIR)[:-5]
                mods.add(rel.replace(os.sep, "."))
    return mods


ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([a-z\-]+)\s*\|\s*([^|]*)\|", re.M)


def _ledger_rows():
    rows = {}
    for mt in ROW.finditer(_read(LEDGER)):
        name, cat, cards = mt.group(1), mt.group(2), mt.group(3).strip()
        rows[name] = (cat, cards)
    return rows


def test_ledger_exists():
    assert os.path.isfile(LEDGER), LEDGER


def test_every_module_on_disk_is_in_the_ledger():
    disk = _disk_modules()
    missing = sorted(disk - set(_ledger_rows()))
    assert not missing, "modules on disk but absent from MODULE_LEDGER.md: %s" % missing


def test_no_phantom_ledger_entries():
    disk = _disk_modules()
    phantom = sorted(set(_ledger_rows()) - disk)
    assert not phantom, "ledger entries with no module on disk: %s" % phantom


def test_every_category_is_known():
    bad = sorted({c for c, _ in _ledger_rows().values() if c not in CATEGORIES})
    assert not bad, "ledger categories outside the legend: %s" % bad


def test_card_modules_are_tagged_card_with_the_right_ids():
    entries = _entries()
    card_of = {}
    for token, mods, _ in entries:
        for mod in mods:
            card_of.setdefault(mod, set()).add(token)
    tokens = {t for t, _, _ in entries}
    rows = _ledger_rows()
    problems = []
    for mod, cards in card_of.items():
        if mod not in rows:
            problems.append("card module %s missing from ledger" % mod)
            continue
        cat, listed = rows[mod]
        if cat != "card":
            problems.append("%s mapped to cards %s but ledger category is %r"
                            % (mod, sorted(cards), cat))
        listed_ids = {c.strip() for c in listed.replace("\u2014", "").split(",") if c.strip()}
        if listed_ids != cards:
            problems.append("%s ledger cards %s != traceability cards %s"
                            % (mod, sorted(listed_ids), sorted(cards)))
    assert not problems, "\n".join(problems)


def test_every_ledger_card_id_is_a_real_card():
    tokens = {t for t, _, _ in _entries()}
    bad = set()
    for _, (_, cards) in _ledger_rows().items():
        for c in cards.replace("\u2014", "").split(","):
            c = c.strip()
            if c and c not in tokens:
                bad.add(c)
    assert not bad, "ledger references card IDs not in the traceability map: %s" % sorted(bad)


def test_every_module_is_imported_by_the_library_root():
    root_src = _read(LEAN_ROOT)
    not_imported = sorted(
        m for m in _disk_modules()
        if not re.search(r"(?m)^import PunoCalculus\.%s\s*$" % re.escape(m), root_src)
    )
    assert not not_imported, (
        "modules never built (not imported by PunoCalculus.lean): %s" % not_imported
    )
