"""Scope boundary: the front page may not *assert* that a Millennium problem is
settled.

The project ships honest machinery -- `PunoCalculus.MillenniumBridge` records all
seven Clay problems as ``NOT SETTLED BY THIS PROJECT`` -- but prose is free to
drift away from it. This test pins the drift:

1. ``WHAT_THIS_DOES_NOT_PROVE.md`` exists and is linked from ``README.md``;
2. ``README.md`` contains **no** unhedged settlement claim (a settlement phrase
   such as "we prove" / "rigorous proof" must be negated or hedged on the same
   line);
3. ``MillenniumBridge.lean`` still disclaims all seven problems;
4. a repo-wide census of unhedged settlement lines in the documentation folder
   stays at or below the pinned baseline (a ratchet). A document is *excused* if
   it carries the scope banner -- a link to ``WHAT_THIS_DOES_NOT_PROVE.md`` --
   which is the legitimate, top-of-paper way to disclaim a narrative. A document
   without the banner may not contain an unhedged settlement claim.

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_scope_boundary.py -q
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC_DIR = os.path.join(
    ROOT,
    "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
)
README = os.path.join(DOC_DIR, "README.md")
BOUNDARY = os.path.join(DOC_DIR, "WHAT_THIS_DOES_NOT_PROVE.md")
BRIDGE = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus",
    "MillenniumBridge.lean",
)

# Phrases that assert this project settled something. Matched case-insensitively.
BANNED = re.compile(
    r"rigorous proof|complete proof|complete elementary proof|"
    r"\bwe prove\b|\bwe proved\b|\bwe have proved\b|"
    r"\bis solved\b|\bare solved\b|\bsettles the\b|"
    r"unifies the (seven|7) millennium",
    re.I,
)

# A settlement phrase is neutralised when the same line negates or hedges it.
HEDGE = re.compile(
    r"\b(not|no|never|without|cannot|unproven|unsolved|unsettled|open|"
    r"gap|absence|conjectur\w*|hypothes\w*|analog\w*|interpret\w*|narrative|"
    r"reserve|candidate|propos\w*|aspir\w*|sketch|evidence|partial|caveat|"
    r"disclaim\w*|unverified|unsupported)\b",
    re.I,
)

# The boundary document is the reference that *defines* these phrases, so it is
# exempt from the census (it names them on purpose).
CENSUS_EXEMPT = {"WHAT_THIS_DOES_NOT_PROVE.md"}

# A document that contains this link carries the scope banner and is treated as
# honestly labelled narrative (all its settlement-sounding lines are disclaimed).
BOUNDARY_LINK = "WHAT_THIS_DOES_NOT_PROVE.md"

# Baseline measured on the current tree: unhedged settlement lines are
# grandfathered at this count, and the ratchet fails if the count grows. Lower
# this number as heroic prose is reconciled with the boundary.
BASELINE_UNHEDGED = 0


def _read(path):
    with open(path, encoding="utf-8", errors="replace") as fp:
        return fp.read()


def _unhedged_lines(text):
    """Line numbers whose settlement claim is neither negated nor hedged."""
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if BANNED.search(line) and not HEDGE.search(line):
            hits.append((i, line.strip()))
    return hits


def test_boundary_doc_exists_and_is_linked_from_readme():
    assert os.path.isfile(BOUNDARY), f"missing scope boundary doc: {BOUNDARY}"
    readme = _read(README)
    assert "WHAT_THIS_DOES_NOT_PROVE.md" in readme, (
        "README.md must link the scope boundary "
        "(WHAT_THIS_DOES_NOT_PROVE.md)"
    )


def test_front_page_has_no_unhedged_settlement_claims():
    hits = _unhedged_lines(_read(README))
    pretty = "\n".join(f"  README.md:{n}: {s}" for n, s in hits)
    assert not hits, (
        "README.md asserts a settlement without hedging it "
        f"(negate or hedge the claim):\n{pretty}"
    )


def test_millennium_bridge_disclaims_all_seven_problems():
    src = _read(os.path.join(
        ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean",
        "PunoCalculus", "MillenniumBridge.lean",
    ))
    assert "NOT SETTLED BY THIS PROJECT" in src, (
        "MillenniumBridge.lean lost its non-settlement status string"
    )
    assert re.search(r"statuses\.length\s*=\s*7", src), (
        "MillenniumBridge.lean no longer pins statuses.length = 7"
    )
    for ident in ("P_NNP", "HODGE", "POINCARE", "RH",
                  "YANG_MILLS", "NAVIER_STOKES", "BSD"):
        assert ident in src, f"MillenniumBridge.lean is missing {ident}"


def test_repo_wide_overclaim_census_within_baseline():
    total = 0
    offenders = []
    unscoped = []
    for name in sorted(os.listdir(DOC_DIR)):
        if not name.endswith(".md") or name in CENSUS_EXEMPT:
            continue
        text = _read(os.path.join(DOC_DIR, name))
        if BOUNDARY_LINK in text:
            continue  # doc carries the scope banner; its narrative is disclaimed
        unscoped.append(name)
        hits = _unhedged_lines(text)
        if hits:
            total += len(hits)
            offenders.append(f"  {len(hits):3d}  {name}")
    report = "\n".join(offenders)
    print(
        f"\nscope census: {total} unhedged settlement lines in "
        f"{len(unscoped)} docs lacking the scope banner "
        f"(baseline {BASELINE_UNHEDGED})\n{report}"
    )
    assert total <= BASELINE_UNHEDGED, (
        f"unhedged settlement lines grew to {total} "
        f"(baseline {BASELINE_UNHEDGED}); add the scope banner "
        "(`WHAT_THIS_DOES_NOT_PROVE.md` link) or hedge the claim:\n" + report
    )
