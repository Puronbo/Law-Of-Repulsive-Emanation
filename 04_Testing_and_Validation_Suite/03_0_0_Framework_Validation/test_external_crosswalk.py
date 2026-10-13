"""External-corpora crosswalk: this project's modules vs. ``openai/math`` families.

`EXTERNAL_CORPORA_CROSSWALK.md` links this repository's certified artifacts to the
result families of the public ``openai/math`` manuscript collection. Nothing here
questions either side's mathematics; the test only pins the *links* so the human
map cannot drift from the tree.

Offline checks (no network at test time -- the external family numbers are pinned
against the documented snapshot):

1. the crosswalk file exists and cites the canonical repo URL and the announcement URL;
2. every module named under *Ours* exists under ``.../PunoCalculus/`` and is imported
   by the library root ``PunoCalculus.lean``;
3. every quoted ``openai/math`` family number appears in the crosswalk;
4. the "no counterpart" modules are named and exist.

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_external_crosswalk.py -q
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEAN_DIR = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus"
)
LEAN_ROOT = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus.lean"
)
CROSSWALK = os.path.join(
    ROOT,
    "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
    "EXTERNAL_CORPORA_CROSSWALK.md",
)

# Modules of ours that the crosswalk claims touch an openai/math family.
OURS = [
    "NavierStokes",
    "LogicBarrier",
    "BSD",
    "Hodge",
    "MassGap",
    "PvsNP",
    "ZeroFixedPoint",
    "MillenniumBridge",
    "Poincare",
]

# Topics with no counterpart in the snapshot -- still named and present in the tree.
NO_COUNTERPART = ["Collatz", "Goldbach", "TwinPrime", "Legendre"]

# Result-family numbers quoted in the crosswalk (pinned to the 2026-10-06 snapshot).
FAMILIES = [
    "376", "002", "006", "032", "215",
    "102", "105", "106", "274",
    "206", "242", "328", "314", "003",
]

REPO_URL = "https://github.com/openai/math"
ANNOUNCE_URL = "https://openai.com/index/sharing-ai-progress-in-mathematics/"


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def test_crosswalk_exists_and_cites_canonical_urls():
    assert os.path.isfile(CROSSWALK), CROSSWALK
    doc = _read(CROSSWALK)
    assert REPO_URL in doc, "crosswalk must cite the openai/math repo URL"
    assert ANNOUNCE_URL in doc, "crosswalk must cite the OpenAI announcement URL"


def test_every_named_module_exists():
    missing = [m for m in OURS + NO_COUNTERPART
               if not os.path.isfile(os.path.join(LEAN_DIR, m + ".lean"))]
    assert not missing, f"modules named by the crosswalk but missing: {missing}"


def test_every_named_module_is_imported_by_the_library_root():
    root_src = _read(LEAN_ROOT)
    not_imported = [
        m for m in OURS if f"import PunoCalculus.{m}" not in root_src
    ]
    assert not not_imported, (
        "modules named by the crosswalk but not imported by PunoCalculus.lean: "
        f"{not_imported}"
    )


def test_every_quoted_family_number_is_present():
    doc = _read(CROSSWALK)
    missing = [
        n for n in FAMILIES
        if not re.search(r"(?<!\d)" + n + r"(?!\d)", doc)
    ]
    assert not missing, f"crosswalk is missing quoted family numbers: {missing}"


def test_crosswalk_names_the_no_counterpart_modules():
    doc = _read(CROSSWALK)
    missing = [m for m in NO_COUNTERPART if m not in doc]
    assert not missing, f"crosswalk does not name modules {missing}"
