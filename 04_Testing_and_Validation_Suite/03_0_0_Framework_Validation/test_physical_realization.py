"""Physical-realization note gate.

``PHYSICAL_REALIZATION_OF_PHI.md`` is the candidate list for the missing entity
of the Landauer-register OPEN claim: which *measured* systems realise the
register's two-state content, and whether any of them is a **mixture of two or
more** channels. It is narrative and makes no physical claim.

This gate pins that honesty:

1. the note exists and carries the scope banner (a link to
   ``WHAT_THIS_DOES_NOT_PROVE.md``);
2. it names measured two-state systems (colloidal bead, single-electron box,
   qubit+cavity, flux logic, levitated nanosphere, trapped ion);
3. it names the mixture decompositions (information vs thermodynamic; population
   vs coherence; three-channel);
4. it states the candidate identification OPEN, names the missing entity, the
   falsifier, and disclaims any physical and any Millennium claim;
5. the mixture brick (``PunoCalculus/InformationMixture.lean``) exists, exposes
   its four declarations, is free of ``sorry``, and is imported by the library
   root ``PunoCalculus.lean``.

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_physical_realization.py -q
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC_DIR = os.path.join(
    ROOT,
    "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
)
DOC = os.path.join(DOC_DIR, "PHYSICAL_REALIZATION_OF_PHI.md")

LEAN_ROOT = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus.lean"
)
LEAN = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus",
    "InformationMixture.lean",
)
LEAN_TIME = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus",
    "InformationTime.lean",
)

# Measured two-state systems the note must name.
SYSTEMS = [
    "Bérut", "Koski", "Cottet", "Saira", "Ciampini", "Yan",
    "trapped ion", "levitated",
]

# Measured decompositions the note must name.
MIXTURES = [
    "mixture", "information", "thermodynamic", "population", "coherence",
    "Aimet", "2407.21690",
]

# Causal-arrow (cause-and-effect) reading the note must name.
CAUSATION = ["Rovelli", "10.31389/pop.46", "cause and effect", "entropy gradient"]

# Declarations the mixture brick must expose.
DECLS = [
    "entropy_mixture", "binaryEntropy_nonneg", "entropy_mixture_ge",
    "entropy_mixture_half",
]

# Declarations the time brick must expose.
TIME_DECLS = [
    "evolution_add", "orientation_evolution_one", "evolution_pow_nat",
    "orientation_arrow", "orientation_sign_iff", "orientation_arrow_is_causal",
    "Phi_freeRatio_eq_evolution",
    "Phi_entropyProd_eq_neg_rate", "orbit_eq_evolution",
]


def _read(path):
    with open(path, encoding="utf-8", errors="replace") as fp:
        return fp.read()


def test_note_exists_and_carries_scope_banner():
    assert os.path.isfile(DOC), DOC
    text = _read(DOC)
    assert text.strip(), "physical-realization note is empty"
    assert "WHAT_THIS_DOES_NOT_PROVE.md" in text, (
        "the note must link the scope boundary so its narrative is disclaimed"
    )


def test_note_names_measured_systems():
    text = _read(DOC)
    low = text.lower()
    missing = [s for s in SYSTEMS if s.lower() not in low]
    assert not missing, f"note does not name measured systems: {missing}"


def test_note_names_the_mixture_decompositions():
    text = _read(DOC)
    low = text.lower()
    missing = [m for m in MIXTURES if m.lower() not in low]
    assert not missing, f"note does not name the mixture decompositions: {missing}"


def test_note_names_the_causal_arrow_reading():
    low = _read(DOC).lower()
    missing = [c for c in CAUSATION if c.lower() not in low]
    assert not missing, f"note does not name the causal-arrow reading: {missing}"


def test_note_states_open_with_missing_entity_and_falsifier():
    low = _read(DOC).lower()
    assert "missing entity" in low, "note must name its missing entity"
    assert "falsifier" in low, "note must name its falsifier"
    assert "open" in low, "note must mark the identification OPEN"


def test_note_disclaims_physical_and_millennium_claims():
    low = _read(DOC).lower()
    assert "no physical claim" in low or "not a physical claim" in low, (
        "note must disclaim any physical claim"
    )
    assert "millennium" in low, "note must reference the Millennium boundary"


def test_mixture_brick_exists_and_is_wired():
    assert os.path.isfile(LEAN), LEAN
    text = _read(LEAN)
    missing = [d for d in DECLS if d not in text]
    assert not missing, f"InformationMixture.lean missing declarations: {missing}"
    assert "sorry" not in text, "the mixture brick must be sorry-free"
    root = _read(LEAN_ROOT)
    assert "import PunoCalculus.InformationMixture" in root, (
        "InformationMixture.lean must be imported by the library root"
    )


def test_time_brick_exists_and_is_wired():
    lean_time = os.path.join(
        ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus",
        "InformationTime.lean",
    )
    assert os.path.isfile(lean_time), lean_time
    text = _read(lean_time)
    missing = [d for d in TIME_DECLS if d not in text]
    assert not missing, f"InformationTime.lean missing declarations: {missing}"
    assert "sorry" not in text, "the time brick must be sorry-free"
    assert "EmergentTime" in text, (
        "the time brick must link the C11 time module"
    )
    root = _read(LEAN_ROOT)
    assert "import PunoCalculus.InformationTime" in root, (
        "InformationTime.lean must be imported by the library root"
    )
