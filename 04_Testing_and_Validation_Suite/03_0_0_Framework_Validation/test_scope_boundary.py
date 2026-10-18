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
4. a repo-wide census of unhedged settlement lines, walked recursively across
   all documentation trees, stays at or below the pinned baseline (a ratchet).
   A document is *excused* if
   it carries the scope banner -- a link to ``WHAT_THIS_DOES_NOT_PROVE.md`` --
   which is the legitimate, top-of-paper way to disclaim a narrative. A document
   without the banner may not contain an unhedged settlement claim;
5. **status-table consistency.** A *status cell* in any scanned document may not
   mark one of the seven problems DONE/PROVED/SOLVED/SETTLED. The census in (4)
   keys on phrases ("we prove", "is solved"), so a status table that simply says
   ``| Navier-Stokes | DONE |`` slipped through it. That is a factual
   contradiction of the boundary, not narrative flavour, so here the scope
   banner does **not** excuse it.

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

# Documentation trees walked (recursively) by the census.
SCAN_ROOTS = [
    os.path.join(ROOT, "05_Documentation_and_Research_Specifications"),
    os.path.join(ROOT, "07_Interdisciplinary_Connections_and_Frameworks"),
    os.path.join(ROOT, "03_Data_and_Observational_Resources"),
    os.path.join(ROOT, "02_Experimental_Implementations_and_Verification"),
]
# Directories never scanned (tooling, caches, vendored worktrees).
SKIP_DIRS = {".git", ".claude", "__pycache__", ".pytest_cache"}

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
    unscoped = 0
    for root in SCAN_ROOTS:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            if any(part in SKIP_DIRS for part in dirpath.split(os.sep)):
                continue
            for name in sorted(filenames):
                if not name.endswith(".md") or name in CENSUS_EXEMPT:
                    continue
                path = os.path.join(dirpath, name)
                text = _read(path)
                if BOUNDARY_LINK in text:
                    continue  # carries the scope banner; narrative disclaimed
                unscoped += 1
                hits = _unhedged_lines(text)
                if hits:
                    total += len(hits)
                    rel = os.path.relpath(path, ROOT)
                    offenders.append(f"  {len(hits):3d}  {rel}")
    report = "\n".join(offenders)
    print(
        f"\nscope census: {total} unhedged settlement lines in "
        f"{unscoped} docs lacking the scope banner "
        f"(baseline {BASELINE_UNHEDGED})\n{report}"
    )
    assert total <= BASELINE_UNHEDGED, (
        f"unhedged settlement lines grew to {total} "
        f"(baseline {BASELINE_UNHEDGED}); add the scope banner "
        "(`WHAT_THIS_DOES_NOT_PROVE.md` link) or hedge the claim:\n" + report
    )


# --------------------------------------------------------------------------
# 5. Millennium status tables may not contradict the boundary.
# --------------------------------------------------------------------------

# Distinctive tokens for the subject cell of a status row, mapped to a witness
# substring that must occur in the boundary's own problem table. Each pair is
# checked by the test below, so this list cannot drift away from the authority
# it is enforced against. `bsd` is an alias: the boundary spells it out.
SUBJECT_KEYS = {
    "navier": "navier",
    "yang": "yang",
    "riemann": "riemann",
    "poincar": "poincar",
    "hodge": "hodge",
    "np": "np",
    "bsd": "swinnerton",
}

# A status cell asserting the problem is done. Deliberately status-cell scoped:
# a sentence may still say "proved" as long as the *status* column does not.
SETTLED_CELL = re.compile(
    r"\b(DONE|SOLVED|RESOLVED|SETTLED|PROVED|PROOF|COMPLETE)\b", re.I
)

# Poincare really is settled -- by Perelman, in 2003 -- just never *by this
# project*, so a row may say so only if it names Perelman on the same line.
POINCARE_EXCEPTION = "perelman"


def _table_cells(line):
    """Cells of a markdown table row, or None when the line is not one."""
    s = line.strip()
    if not s.startswith("|"):
        return None
    return [c.strip() for c in s.strip("|").split("|")]


def _boundary_problems():
    """(subject, status) rows of the boundary document's own status table."""
    rows = []
    for line in _read(BOUNDARY).splitlines():
        cells = _table_cells(line)
        if not cells or len(cells) < 2:
            continue
        if cells[0].lower() == "problem" or set(cells[0]) <= set("-: "):
            continue
        rows.append((cells[0], cells[1]))
    return rows


def test_subject_keys_are_derived_from_the_boundary_table():
    """The name list may not drift from the authority it is checked against."""
    rows = _boundary_problems()
    assert len(rows) >= 7, (
        "WHAT_THIS_DOES_NOT_PROVE.md no longer exposes the seven-problem "
        f"status table (parsed {len(rows)} rows); Gate A cannot run"
    )
    blob = " ".join(subject for subject, _ in rows).lower()
    missing = [k for k, witness in SUBJECT_KEYS.items() if witness not in blob]
    assert not missing, (
        "SUBJECT_KEYS not witnessed by the boundary's own problem table: %s "
        "(update SUBJECT_KEYS or the boundary table so they agree)" % missing
    )


def test_no_status_cell_claims_a_millennium_problem_settled():
    offenders = []
    for root in SCAN_ROOTS:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            if any(part in SKIP_DIRS for part in dirpath.split(os.sep)):
                continue
            for name in sorted(filenames):
                if not name.endswith(".md") or name in CENSUS_EXEMPT:
                    continue
                path = os.path.join(dirpath, name)
                rel = os.path.relpath(path, ROOT)
                for n, line in enumerate(_read(path).splitlines(), 1):
                    cells = _table_cells(line)
                    if not cells or len(cells) < 2:
                        continue
                    subject, status = cells[0].lower(), cells[1]
                    if not any(k in subject for k in SUBJECT_KEYS):
                        continue
                    if not SETTLED_CELL.search(status):
                        continue
                    if "poincar" in subject and POINCARE_EXCEPTION in line.lower():
                        continue
                    # Hedge the *status* cell only. Scanning the whole row lets
                    # a problem excuse itself out of its own name -- the words
                    # "Hypothesis"/"Conjecture" are hedges, so
                    # `| Riemann Hypothesis | DONE |` would pass.
                    if HEDGE.search(status):
                        continue
                    offenders.append(f"  {rel}:{n}: | {cells[0]} | {status} |")
    report = "\n".join(offenders)
    assert not offenders, (
        "a status cell marks a Millennium problem settled, contradicting "
        "WHAT_THIS_DOES_NOT_PROVE.md (hedge it or set the status to OPEN):\n"
        + report
    )
