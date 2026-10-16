"""Theory-of-everything (C12 capstone) program gate.

``THEORY_OF_EVERYTHING.md`` fixes what "theory of everything" means *inside this
repository*: the register's structural unification as card **C12** -- a
scaling-critical system is governed by exactly two organizing numbers (order and
orientation), formalized in ``PunoCalculus/TheoryOfEverything.lean``. This gate
pins that program so it cannot drift from the tree:

1. the capstone module exists and exposes the six quoted declarations;
2. every ``PunoCalculus`` module the capstone imports exists on disk and is named
   in the program document (the brick map stays complete);
3. the facts register ``theoryOfEverythingFacts`` has exactly five entries;
4. the document states the honesty boundary (no Millennium problem settled) and
   names card C12, keeping the wall marked OPEN.

No Lean toolchain is required: this is a file-reading gate, exactly like the
other verification gates that run in CI.

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_theory_of_everything.py -q
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEAN_DIR = os.path.join(ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean")
CAPSTONE = os.path.join(LEAN_DIR, "PunoCalculus", "TheoryOfEverything.lean")
DOC = os.path.join(
    ROOT,
    "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
    "THEORY_OF_EVERYTHING.md",
)

# Declarations the capstone must expose.
DECLS = [
    "order_sets_rung",
    "orientation_sets_side",
    "twoNumbersClose",
    "order_sets_rung_bijective",
    "orientation_not_injective_on_side",
    "theoryOfEverything",
    "method_and_margin_barriers",
    "theoryOfEverythingFacts",
]

# The facts register has exactly this many entries.
FACT_COUNT = 5


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _capstone_imports(src):
    """Return the imported ``PunoCalculus.*`` module names (attributes kept)."""
    mods = []
    for name in re.findall(r"^\s*import\s+([\w.]+)\s*$", src, re.M):
        if name.startswith("PunoCalculus."):
            mods.append(name)
    return mods


def test_program_doc_exists():
    assert os.path.isfile(DOC), DOC
    assert _read(DOC).strip(), "theory-of-everything program doc is empty"


def test_capstone_module_exists_and_exposes_the_quoted_declarations():
    assert os.path.isfile(CAPSTONE), CAPSTONE
    src = _read(CAPSTONE)
    missing = [d for d in DECLS if d not in src]
    assert not missing, f"capstone does not expose: {missing}"


def test_every_capstone_import_exists_and_is_named_in_the_doc():
    src = _read(CAPSTONE)
    doc = _read(DOC)
    problems = []
    for mod in _capstone_imports(src):
        rel = mod.replace(".", os.sep, 1)  # PunoCalculus.X -> PunoCalculus\X
        path = os.path.join(LEAN_DIR, rel + ".lean")
        if not os.path.isfile(path):
            problems.append(f"missing Lean module on disk: {mod}")
        stem = mod.split(".")[-1]
        if stem not in doc:
            problems.append(f"capstone import not named in the doc: {stem}")
    assert not problems, "\n".join(problems)


def test_capstone_is_named_in_the_doc():
    doc = _read(DOC)
    assert "TheoryOfEverything" in doc, "doc must name the capstone module"
    assert "C12" in doc, "doc must name card C12"


def test_facts_register_has_exactly_five_entries():
    src = _read(CAPSTONE)
    m = re.search(
        r"theoryOfEverythingFacts\s*:\s*List String\s*:=\s*\[(.*?)\]", src, re.S
    )
    assert m, "could not locate the theoryOfEverythingFacts list"
    entries = re.findall(r'"[^"]*"', m.group(1))
    assert len(entries) == FACT_COUNT, (
        f"facts register has {len(entries)} entries, expected {FACT_COUNT}"
    )
    assert re.search(
        r"theoryOfEverythingFacts_length\s*:.*=\s*5\b", src
    ), "capstone must certify the facts-register length as 5"


def test_doc_states_the_honesty_boundary():
    doc = _read(DOC)
    assert re.search(r"no\s+Millennium\s+problem", doc, re.I), (
        "program doc must state that no Millennium problem is settled"
    )
    assert "OPEN" in doc, "program doc must keep the wall marked OPEN"
