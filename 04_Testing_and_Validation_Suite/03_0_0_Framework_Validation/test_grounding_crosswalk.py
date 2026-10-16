"""Known-studies grounding crosswalk: the framework anchored to the literature.

``KNOWN_STUDIES_GROUNDING.md`` links each of the framework's mechanisms (the 0/0
removable-value law, the five 0/0 mechanisms, folding, the ECA/twin/soliton
family, the scaling-critical ladder, discrete conservation, orientation, the
logic barrier) to named studies in the literature *and* to this repository's own
artifacts. This gate pins those links so the map cannot drift from the tree:

1. every Lean module the crosswalk names exists on disk;
2. every numeric script / validator it names exists on disk;
3. the named works (anchors) and mechanisms actually appear in the document;
4. the document states the honesty boundary (no Millennium problem settled).

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_grounding_crosswalk.py -q
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEAN_DIR = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean"
)
EXP_DIR = os.path.join(
    ROOT,
    "02_Experimental_Implementations_and_Verification",
    "06_Miscellaneous_Experiments",
)
ECA_DIR = os.path.join(
    ROOT,
    "07_Interdisciplinary_Connections_and_Frameworks",
    "02_Mathematical_Physics_Connections",
    "Create Native Ramp Function and Implement 8-Bit ECA Rules",
)
DOC = os.path.join(
    ROOT,
    "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
    "KNOWN_STUDIES_GROUNDING.md",
)

# Lean modules named by the crosswalk (relative to LEAN_DIR).
MODULES = [
    "PunoCalculus/RemovableValue.lean",
    "PunoCalculus/RemovableComplexBridge.lean",
    "PunoCalculus/LiouvilleBridge.lean",
    "PunoCalculus/LogicBarrier.lean",
    "PunoCalculus/ZeroProbe.lean",
    "PunoCalculus/VanishOrder.lean",
    "PunoCalculus/ZeroValuation.lean",
    "PunoCalculus/ZeroIndex.lean",
    "PunoCalculus/NoetherDiscrete.lean",
    "PunoCalculus/UniverseGrowth.lean",
    "PunoCalculus/CriticalAmplitude.lean",
    "PunoCalculus/ExplicitClaims.lean",
    "PunoCalculus/Curvature.lean",
    "PunoCalculus/CriticalLadder.lean",
    "PunoCalculus/SerrinLadder.lean",
    "PunoCalculus/OnsagerCriterion.lean",
    "PunoCalculus/ContinuationCriterion.lean",
    "PunoCalculus/SufficiencyLoop.lean",
    "PunoCalculus/EnstrophyBarrier.lean",
    "PunoCalculus/QuantitativeContinuation.lean",
    "PunoCalculus/GreatAttractor.lean",
    "PunoCalculus/OrientationBoundedness.lean",
    "PunoCalculus/OrientationLaw.lean",
    "PunoCalculus/DissipativeFlow.lean",
    "PunoCalculus/EcaIsometry.lean",
    "PunoTwin/TwinRingLaws.lean",
    "PunoTwin/TwinAnalyticLaws.lean",
    "PunoTwin/MPOperator.lean",
]

# Scripts named by the crosswalk, as (directory, filename).
SCRIPTS = [
    (EXP_DIR, "register_ladder_certificates.py"),
    (EXP_DIR, "register_criteria_certificates.py"),
    (EXP_DIR, "zero_mechanism_certificates.py"),
    (EXP_DIR, "arithmetic_shadow_certificates.py"),
    (EXP_DIR, "register_core_certificates.py"),
    (EXP_DIR, "dimension_threshold.py"),
    (EXP_DIR, "dimension_mixture.py"),
    (ECA_DIR, "run_all_audits.py"),
    (ECA_DIR, "validate_soliton_isometry_proofs.py"),
]

# Named works / results the crosswalk must cite (grounding anchors).
ANCHORS = [
    "Riemann", "Liouville", "L'Hôpital", "Mac Lane",
    "Noether", "Prodi", "Serrin", "Koch", "Onsager", "Beale", "Constantin",
    "Tao", "Widom", "Rushbrooke", "Josephson", "Fisher", "Wilson",
    "Demaine", "Robertson", "Kawasaki", "Keup", "Telgarsky", "Lewandowski",
    "Stewart", "Wolfram", "Cook", "Nagel", "Fermat", "Lawvere", "Cantor",
    "Morrey", "Adams", "Frisch",
]

# Mechanism tokens that must be present.
MECHANISMS = [
    "0/0", "removable value", "folding", "ECA", "TASEP", "Serrin", "Onsager",
    "Noether", "twin", "soliton",
]


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _stem(path):
    return os.path.splitext(os.path.basename(path))[0]


def test_crosswalk_doc_exists():
    assert os.path.isfile(DOC), DOC
    assert _read(DOC).strip(), "grounding crosswalk is empty"


def test_every_named_lean_module_exists_and_is_named_in_the_doc():
    doc = _read(DOC)
    problems = []
    for rel in MODULES:
        path = os.path.join(LEAN_DIR, rel.replace("/", os.sep))
        if not os.path.isfile(path):
            problems.append(f"missing Lean module on disk: {rel}")
        if _stem(rel) not in doc:
            problems.append(f"Lean module not named in the doc: {_stem(rel)}")
    assert not problems, "\n".join(problems)


def test_every_named_script_exists_and_is_named_in_the_doc():
    doc = _read(DOC)
    problems = []
    for directory, name in SCRIPTS:
        if not os.path.isfile(os.path.join(directory, name)):
            problems.append(f"missing script on disk: {name}")
        if name not in doc:
            problems.append(f"script not named in the doc: {name}")
    assert not problems, "\n".join(problems)


def test_known_study_anchors_are_present():
    doc = _read(DOC)
    missing = [a for a in ANCHORS if a not in doc]
    assert not missing, f"crosswalk is missing known-study anchors: {missing}"


def test_mechanisms_are_present():
    doc = _read(DOC).lower()
    missing = [m for m in MECHANISMS if m.lower() not in doc]
    assert not missing, f"crosswalk is missing mechanisms: {missing}"


def test_crosswalk_states_the_honesty_boundary():
    doc = _read(DOC)
    assert re.search(r"no\s+Millennium\s+problem", doc, re.I), (
        "crosswalk must state that no Millennium problem is settled"
    )
    assert "OPEN" in doc, "crosswalk must keep the wall marked OPEN"
