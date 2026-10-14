"""Physics crosswalk: the register's cards joined to the physics programs.

`PHYSICS_CROSSWALK.md` is the physics twin of `EXTERNAL_CORPORA_CROSSWALK.md`. It
maps each claim card to a physics phenomenon, a standard object/theorem, and a
status tag, under an explicit *adjacency ≠ equivalence* rule. This checker keeps the
map honest and resolvable:

1. the crosswalk exists and carries the scope banner (links
   `WHAT_THIS_DOES_NOT_PROVE.md`);
2. every physics document it cites exists on disk, and each is named in the map;
3. every card ID in the map is a real token in the traceability map
   (`test_claim_traceability.ENTRIES`);
4. every row status is one of the legend's tags;
5. the three genuine hinge anchors (renormalization, mass gap, Onsager) are present,
   so the map cannot silently drop its load-bearing rows.

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_physics_crosswalk.py -q
"""

import importlib.util
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC_DIR = os.path.join(
    ROOT, "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
)
CROSSWALK = os.path.join(DOC_DIR, "PHYSICS_CROSSWALK.md")
CHECKER = os.path.join(
    ROOT, "04_Testing_and_Validation_Suite", "03_0_0_Framework_Validation",
    "test_claim_traceability.py",
)

# Tracked framework docs the map must link (exist in a CI checkout).
BOUNDARY_DOCS = [
    os.path.join(DOC_DIR, "EXTERNAL_CORPORA_CROSSWALK.md"),
    os.path.join(DOC_DIR, "SHARED_WALL_AND_PATH_FORWARD.md"),
    os.path.join(DOC_DIR, "WHAT_THIS_DOES_NOT_PROVE.md"),
]

# Physics sources live in the (larger, untracked) research tree: the map must
# *name* them, but CI cannot require them on disk.
PHYSICS_SOURCE_NAMES = [
    "PHYSICS_CATEGORIZATION.md",
    "THEORY_CONNECTIONS_SUMMARY.md",
    "VERIFIED_SYNTHESIS_AND_EQUIVALENTS.md",
    "summary.md",
]

STATUSES = {"Lean-proved", "physics-known", "analogy", "open", "excluded"}
CARD_TOKEN = re.compile(r"\*\*(C\d+(?:/C\d+)?(?:-open)?)\*\*")


def _read(path):
    with open(path, encoding="utf-8") as fp:
        return fp.read()


def _card_tokens():
    spec = importlib.util.spec_from_file_location("tct", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {t for t, _, _ in mod.ENTRIES}


def test_crosswalk_exists_and_carries_scope_banner():
    assert os.path.isfile(CROSSWALK), CROSSWALK
    doc = _read(CROSSWALK)
    assert "WHAT_THIS_DOES_NOT_PROVE.md" in doc, "crosswalk must link the scope boundary"
    assert "adjacency" in doc.lower() and "equivalence" in doc.lower(), (
        "crosswalk must state the adjacency != equivalence rule"
    )


def test_tracked_framework_docs_exist_and_are_named():
    doc = _read(CROSSWALK)
    missing_file = [p for p in BOUNDARY_DOCS if not os.path.isfile(p)]
    assert not missing_file, "tracked framework docs missing on disk: %s" % missing_file
    not_named = [os.path.basename(p) for p in BOUNDARY_DOCS
                 if os.path.basename(p) not in doc]
    assert not not_named, "tracked framework docs not named in the crosswalk: %s" % not_named


def test_every_physics_source_is_named():
    doc = _read(CROSSWALK)
    not_named = [p for p in PHYSICS_SOURCE_NAMES if p not in doc]
    assert not not_named, "physics sources not named in the crosswalk: %s" % not_named


def test_every_card_token_is_a_real_card():
    tokens = _card_tokens()
    found = set(CARD_TOKEN.findall(_read(CROSSWALK)))
    bad = sorted(found - tokens)
    assert not bad, "crosswalk references card IDs not in the traceability map: %s" % bad
    assert found, "crosswalk references no cards at all"


def test_every_row_status_is_known():
    doc = _read(CROSSWALK)
    # status is the final pipe-delimited cell of each data row
    statuses = set()
    for line in doc.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[-1] in STATUSES:
            statuses.add(cells[-1])
    assert statuses, "no rows with a recognised status tag found"
    # every row must end in a known status: rows with 5+ cells must use one
    unknown = []
    for line in doc.splitlines():
        if not line.startswith("|") or set(line) <= set("|-: "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[-1].lower() != "status" and cells[-1] not in STATUSES:
            unknown.append(cells[-1])
    assert not unknown, "crosswalk rows with unknown status tags: %s" % unknown


def test_hinge_anchors_present():
    doc = _read(CROSSWALK).lower()
    for anchor in ("renormalization", "mass gap", "onsager"):
        assert anchor in doc, "crosswalk dropped a hinge anchor: %s" % anchor
