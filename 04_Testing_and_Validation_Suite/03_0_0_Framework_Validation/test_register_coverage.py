"""Register coverage: the honesty contract, machine-checked.

The register's central promise is that every claim card carries the halves it
advertises -- a Lean theorem half *and* (where it claims one) a reproducible
numeric half -- and that no card exists outside the traced set. This gate turns
that promise into an invariant:

1. **No orphan cards.** Every card token with a heading in ``EXPLICIT_CLAIMS.md``
   appears in ``ENTRIES`` (and vice versa); a card cannot exist in prose without a
   traced artifact, nor be traced without a heading.
2. **The numeric half actually runs.** Every ``*_certificates.py`` script named by
   a card is executed (stdlib-only, deterministic) and must exit ``0`` -- so a
   card's "empirical half" is verified by CI, not merely present on disk.
3. **The gap is declared, not hidden.** The cards with *no* experiment are pinned
   to a known allowlist: exactly the classical/open cards that carry no numeric
   claim. Adding an un-certified card fails the gate until it is declared here.

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_register_coverage.py -q
"""

import importlib.util
import os
import re
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOC_DIR = os.path.join(
    ROOT,
    "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
)
CLAIMS_MD = os.path.join(DOC_DIR, "EXPLICIT_CLAIMS.md")
EXP_DIR = os.path.join(
    ROOT,
    "02_Experimental_Implementations_and_Verification",
    "06_Miscellaneous_Experiments",
)

# Cards that carry no numeric half *by design*: C2 is cited-classical (its
# sufficiency is taken from the literature, not re-derived here) and C3 is the
# named OPEN brick. These are the register's declared gaps -- everything else
# must have a runnable certificate.
CERT_FREE_CARDS = {"C2", "C3"}

_CARD_RE = re.compile(r"(?m)^#{2,3}\s*(C\d+(?:/C\d+)?(?:-open)?)(?=\s|$)")


def _load_entries():
    """Load ``ENTRIES`` from the traceability test without duplicating the map."""
    path = os.path.join(HERE, "test_claim_traceability.py")
    spec = importlib.util.spec_from_file_location("_register_traceability", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ENTRIES


ENTRIES = _load_entries()


def _cards_in_claims_register():
    with open(CLAIMS_MD, encoding="utf-8") as fp:
        return set(_CARD_RE.findall(fp.read()))


def _traced_cards():
    return {token for token, _, _ in ENTRIES}


def _experiment_scripts(token):
    return [s for tok, _, scripts in ENTRIES if tok == token for s in scripts]


def test_no_card_exists_untraced_in_prose():
    orphan = sorted(_cards_in_claims_register() - _traced_cards())
    assert not orphan, f"cards with a heading but no ENTRIES trace: {orphan}"


def test_no_card_is_traced_without_a_heading():
    orphan = sorted(_traced_cards() - _cards_in_claims_register())
    assert not orphan, f"cards traced in ENTRIES but with no heading: {orphan}"


def test_certificate_scripts_are_declared_where_expected():
    scripts = sorted({s for _, _, ss in ENTRIES for s in ss
                      if s.endswith("_certificates.py")})
    assert scripts, "no certificate scripts found in the register"
    for name in scripts:
        assert os.path.isfile(os.path.join(EXP_DIR, name)), name


@pytest.mark.parametrize(
    "script",
    sorted({s for _, _, ss in ENTRIES for s in ss
            if s.endswith("_certificates.py")}),
)
def test_certificate_script_runs_green(script):
    """Every numeric half must reproduce and exit 0 (stdlib-only, deterministic)."""
    path = os.path.join(EXP_DIR, script)
    assert os.path.isfile(path), f"missing certificate script: {script}"
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, script],
        cwd=EXP_DIR,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    tail = (proc.stdout or "").strip().splitlines()[-4:]
    assert proc.returncode == 0, (
        f"{script} exited {proc.returncode}\n--- stdout tail ---\n"
        + "\n".join(tail)
        + f"\n--- stderr ---\n{(proc.stderr or '').strip()[-800:]}"
    )
    assert "PASS" in (proc.stdout or ""), f"{script} produced no PASS marker"


def test_only_the_declared_cards_lack_a_numeric_half():
    certified = {tok for tok, _, scripts in ENTRIES if scripts}
    bare = _traced_cards() - certified
    assert bare == CERT_FREE_CARDS, (
        "cards without a numeric half drift from the declared gap "
        f"(declared {sorted(CERT_FREE_CARDS)}, found {sorted(bare)}); update "
        "CERT_FREE_CARDS deliberately if this is intended"
    )
