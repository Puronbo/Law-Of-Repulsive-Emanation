"""Axiom audit: the generated footprint table must track the traceability checker.

`AXIOM_AUDIT.md` records the axiom footprint of every Lean declaration quoted by a
card in `test_claim_traceability.ENTRIES`. The probe that fills in the *footprints* is
transient (it needs a Lean toolchain), but the *declaration list* it reports is fully
determined by `ENTRIES` — so a toolchain-free CI checkout can still verify the two have
not drifted. This closes the hole that let `AXIOM_AUDIT.md` silently fall behind the
`ENTRIES` table (cards, modules and quoted declarations added without regenerating it):

1. every card token in `ENTRIES` has a `### <token>` section in `AXIOM_AUDIT.md`
   (and there are no sections for unknown cards);
2. the declarations listed under each card are exactly `module.name` for that card's
   `ENTRIES` Lean modules (so adding, removing or renaming a quoted declaration without
   regenerating the audit fails here);
3. the stated "Declarations audited" count equals the distinct declarations quoted;
4. the stated axiom-free count equals the number of `none (axiom-free)` rows.

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_axiom_audit.py -q
"""

import importlib.util
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC_DIR = os.path.join(
    ROOT, "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
)
AUDIT = os.path.join(DOC_DIR, "AXIOM_AUDIT.md")
CHECKER = os.path.join(
    ROOT, "04_Testing_and_Validation_Suite", "03_0_0_Framework_Validation",
    "test_claim_traceability.py",
)

SECTION = re.compile(r"^###\s+(\S+)\s*$", re.MULTILINE)
ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|", re.MULTILINE)
DECL_COUNT = re.compile(r"\*\*Declarations audited:\*\*\s*(\d+)")
AXIOM_FREE = re.compile(r"\*\*Axiom-free declarations:\*\*\s*(\d+)")
AXIOM_FREE_CELL = "none (axiom-free)"


def _read(path):
    with open(path, encoding="utf-8") as fp:
        return fp.read()


def _entries():
    spec = importlib.util.spec_from_file_location("tct", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ENTRIES


def _expected_by_token():
    """token -> set of `module.name` quoted by the card (union over repeat entries)."""
    out = {}
    for token, lean, _scripts in _entries():
        decls = out.setdefault(token, set())
        for module, names in lean.items():
            for name in names:
                decls.add("%s.%s" % (module, name))
    return out


def _documented_by_token():
    """token -> set of declarations listed under its `### token` section(s)."""
    doc = _read(AUDIT)
    sections = list(SECTION.finditer(doc))
    out = {}
    for i, m in enumerate(sections):
        end = sections[i + 1].start() if i + 1 < len(sections) else len(doc)
        out.setdefault(m.group(1), set()).update(ROW.findall(doc[m.end():end]))
    return out


def test_every_card_has_a_section_and_no_extra_sections():
    expected = set(_expected_by_token())
    documented = set(_documented_by_token())
    missing = sorted(expected - documented)
    extra = sorted(documented - expected)
    assert not missing, "cards with no section in AXIOM_AUDIT.md: %s" % missing
    assert not extra, "AXIOM_AUDIT.md sections for unknown cards: %s" % extra


def test_declarations_match_the_entries_table():
    expected = _expected_by_token()
    documented = _documented_by_token()
    problems = []
    for token in sorted(expected):
        missing = sorted(expected[token] - documented.get(token, set()))
        extra = sorted(documented.get(token, set()) - expected[token])
        if missing:
            problems.append("%s: audit is missing %s" % (token, missing))
        if extra:
            problems.append("%s: audit lists extra %s" % (token, extra))
    assert not problems, (
        "AXIOM_AUDIT.md drifted from the ENTRIES table:\n  " + "\n  ".join(problems)
    )


def test_stated_declaration_count_matches():
    distinct = set()
    for decls in _expected_by_token().values():
        distinct |= decls
    m = DECL_COUNT.search(_read(AUDIT))
    assert m, "AXIOM_AUDIT.md must state 'Declarations audited: <n>'"
    assert int(m.group(1)) == len(distinct), (
        "AXIOM_AUDIT.md states %s declarations, ENTRIES quotes %d distinct"
        % (m.group(1), len(distinct))
    )


def test_stated_axiom_free_count_matches_rows():
    doc = _read(AUDIT)
    rows = doc.count(AXIOM_FREE_CELL)
    m = AXIOM_FREE.search(doc)
    assert m, "AXIOM_AUDIT.md must state 'Axiom-free declarations: <n>'"
    assert int(m.group(1)) == rows, (
        "AXIOM_AUDIT.md states %s axiom-free, table has %d 'none (axiom-free)' rows"
        % (m.group(1), rows)
    )
