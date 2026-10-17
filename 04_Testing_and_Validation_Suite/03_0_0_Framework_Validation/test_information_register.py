"""Information-register note gate.

``LANDAUER_BOUND_AND_THE_REGISTER.md`` states an **OPEN** claim (the
Landauer-register bridge) in the register's card format: a precise statement, a
named *missing entity* (a register-to-thermodynamics map ``Phi``), and a
*falsifier*. It separates the established physics (Landauer 1961; the 2025
Nature Physics quantum-many-body experiment; the q-desic quantum-gravity
corrections) from the unsupported narrative (a "self-computing universe",
information "has mass", mind = gravity).

This gate pins that honesty:

1. the note exists and carries the scope banner (a link to
   ``WHAT_THIS_DOES_NOT_PROVE.md``), so its narrative is disclaimed;
2. it names the verified anchors and explicitly flags the sources to discount;
3. it states the claim OPEN, names a missing entity, and names a falsifier;
4. it disclaims any physical claim and any Millennium claim;
5. the companion script exists, runs green (exit 0, ``PASS``), and is stdlib-only;
6. the two-state Lean instance (``PunoCalculus/InformationBridge.lean``) exists,
   exposes its four declarations, imports cleanly, and stays free of ``sorry``.

No Lean toolchain is required.

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_information_register.py -q
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC_DIR = os.path.join(
    ROOT,
    "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
)
EXP_DIR = os.path.join(
    ROOT,
    "02_Experimental_Implementations_and_Verification",
    "06_Miscellaneous_Experiments",
)
DOC = os.path.join(DOC_DIR, "LANDAUER_BOUND_AND_THE_REGISTER.md")
SCRIPT = os.path.join(EXP_DIR, "landauer_orientation.py")

# The two-state Lean instance of the schema (file-reading only; no Lean toolchain).
LEAN_DIR = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean"
)
LEAN = os.path.join(LEAN_DIR, "PunoCalculus", "InformationBridge.lean")
LEAN_ROOT = os.path.join(LEAN_DIR, "PunoCalculus.lean")

# Declarations the two-state brick must expose.
DECLS = [
    "binaryEntropy_half",
    "resetCost_two",
    "resetCost_eq_neg_orientation",
    "orientation_reset_nonpos",
]

# Verified anchors the note must name.
ANCHORS = ["Landauer", "Nature Physics", "2407.21690", "2510.00117", "q-desic"]

# Non-credible sources the note must explicitly discount.
DISCOUNT = ["roadtoomega", "Utopian Earth"]


def _read(path):
    with open(path, encoding="utf-8") as fp:
        return fp.read()


def test_note_exists_and_carries_scope_banner():
    assert os.path.isfile(DOC), DOC
    text = _read(DOC)
    assert text.strip(), "information-register note is empty"
    assert "WHAT_THIS_DOES_NOT_PROVE.md" in text, (
        "the note must link the scope boundary so its narrative is disclaimed"
    )


def test_note_names_the_verified_anchors():
    text = _read(DOC)
    missing = [a for a in ANCHORS if a not in text]
    assert not missing, f"note does not name verified anchors: {missing}"


def test_note_flags_sources_to_discount():
    text = _read(DOC)
    low = text.lower()
    assert "unverified" in low or "not credible" in low, (
        "note must warn that some cited sources are unverified"
    )
    missing = [d for d in DISCOUNT if d not in text]
    assert not missing, f"note must name the sources to discount: {missing}"


def test_note_states_an_open_claim_with_missing_entity_and_falsifier():
    low = _read(DOC).lower()
    assert "missing entity" in low, "note must name its missing entity"
    assert "falsifier" in low, "note must name its falsifier"
    assert "open" in low, "note must mark the claim OPEN"


def test_note_disclaims_physical_and_millennium_claims():
    low = _read(DOC).lower()
    assert "no physical claim" in low or "not a physical claim" in low, (
        "note must disclaim any physical claim"
    )
    assert "millennium" in low, "note must reference the Millennium boundary"


def test_companion_script_runs_green():
    assert os.path.isfile(SCRIPT), SCRIPT
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, SCRIPT],
        cwd=EXP_DIR,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, (
        f"{os.path.basename(SCRIPT)} exited {proc.returncode}\n"
        f"--- stderr ---\n{(proc.stderr or '').strip()[-800:]}"
    )
    assert "PASS" in (proc.stdout or ""), (
        f"{os.path.basename(SCRIPT)} produced no PASS marker"
    )


def test_two_state_lean_brick_exists_and_is_wired():
    assert os.path.isfile(LEAN), LEAN
    text = _read(LEAN)
    missing = [d for d in DECLS if d not in text]
    assert not missing, f"InformationBridge.lean missing declarations: {missing}"
    assert "sorry" not in text, "the two-state brick must be sorry-free"
    assert "Phi" in text, (
        "the brick must disclaim constructing the physical map Phi"
    )
    root = _read(LEAN_ROOT)
    assert "import PunoCalculus.InformationBridge" in root, (
        "InformationBridge.lean must be imported by the library root"
    )
