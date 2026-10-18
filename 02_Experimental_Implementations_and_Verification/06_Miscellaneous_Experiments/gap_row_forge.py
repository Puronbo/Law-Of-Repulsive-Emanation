"""Gap Ledger row forge: draft a Gate-D-valid ledger row for a new problem.

The forge proves nothing.  It is register *tooling*: given a subject and the
kind of proof attempt that exists, it

  * assigns the next free ``G<n>`` number from the live ledger,
  * emits a row skeleton carrying every field Gate D requires
    (``**Proof attempt:** <kind> - <artifact>`` plus at least one live pin),
  * refuses an illegal proof-attempt kind,
  * refuses to name an artifact path that does not exist under the repo root,
  * refuses a pin that is not a real test function,
  * never emits a resolved/``DONE`` status.

The mathematical content (Reduction/Barrier/Known/Missing/Falsifier) is left as
``TODO`` for the author; the forge only enforces that the *shape* is honest and
machine-checkable.  This is the reusable "row generator" for the solver
pipeline: it turns a claimed proof attempt into a ledger entry that Gate D will
accept or reject.

Usage::

    python gap_row_forge.py --subject "Mersenne primes" --kind certificate \
        --artifact path/to/artifact.py --pin test_some_pin
"""
import argparse
import datetime
import os
import re

PROOF_KINDS = ("certificate", "partial", "no-go", "citation-only", "none")
LEDGER_REL = os.path.join(
    "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
    "THE_GAP_LEDGER.md",
)
TESTS_DIR_REL = os.path.join(
    "04_Testing_and_Validation_Suite", "03_0_0_Framework_Validation"
)


def _repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.exists(os.path.join(here, LEDGER_REL)):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            raise RuntimeError("repository root not found from " + __file__)
        here = parent


def next_token(ledger_text):
    """Next free G number, e.g. ``'G28'``, from the live ledger text."""
    nums = [int(n) for n in re.findall(r"(?m)^##\s+G(\d+)", ledger_text)]
    return "G%d" % (max(nums) + 1 if nums else 1)


def pin_exists(pin, root=None):
    """True iff ``pin`` is defined as a test function under the tests dir."""
    root = root or _repo_root()
    tests_dir = os.path.join(root, TESTS_DIR_REL)
    if not os.path.isdir(tests_dir):
        return False
    pat = re.compile(r"(?m)^\s*def\s+" + re.escape(pin) + r"\s*\(")
    for name in os.listdir(tests_dir):
        if not name.endswith(".py"):
            continue
        with open(os.path.join(tests_dir, name), encoding="utf-8",
                  errors="replace") as fp:
            if pat.search(fp.read()):
                return True
    return False


def _render(token, subject, kind, artifact, pin, tier, cards, date):
    cards_field = "[" + ", ".join(cards) + "]" if cards else "[]"
    lines = [
        "## %s - %s" % (token, subject),
        "- **Tier:** %s" % tier,
        "- **Subject:** %s" % subject,
        "- **Status:** RESEARCHED",
        "- **Related cards:** %s" % cards_field,
        "- **Proof attempt:** %s - %s" % (kind, artifact),
        "- **Pin:** %s" % pin,
        "- **as_of:** %s" % date,
        "- **Reduction:** TODO",
        "- **Barrier:** TODO",
        "- **Known:** TODO",
        "- **Missing (the object that does not exist as a proof):** TODO",
        "- **Falsifier:** TODO",
    ]
    return "\n".join(lines)


def forge_row(subject, kind, artifact, pin, tier="B", cards=None,
              date=None, root=None, token="G0"):
    """Return a Gate-D-shaped ledger row for ``subject`` (token placeholder
    unless the caller supplies one from :func:`next_token``).

    Raises ``ValueError`` on an illegal kind, a missing artifact, or a pin that
    is not a real test function -- so the forge cannot emit a row Gate D would
    reject.
    """
    if kind not in PROOF_KINDS:
        raise ValueError(
            "illegal proof-attempt kind %r (allowed: %s)"
            % (kind, ", ".join(PROOF_KINDS)))
    if not subject.strip():
        raise ValueError("subject must be non-empty")
    if kind != "none":
        if not pin or pin == "n/a":
            raise ValueError("non-none kind needs a live pin name")
        if not pin_exists(pin, root=root):
            raise ValueError("pin %r is not a real test function" % pin)
        if artifact and artifact != "n/a":
            root = root or _repo_root()
            for path in [x.strip() for x in artifact.split(",") if x.strip()]:
                if not os.path.exists(os.path.join(root, path)):
                    raise ValueError("artifact path does not exist: %s" % path)
    if date is None:
        date = datetime.date.today().isoformat()
    return _render(token, subject, kind, artifact, pin, tier, cards, date)


def validate_row(row):
    """Return a list of Gate-D-style problems with ``row`` (empty == OK)."""
    problems = []
    if not re.search(r"(?m)^##\s+G\d+\b", row):
        problems.append("row has no '## G<n>' heading")
    m = re.search(r"(?m)^-\s*\*\*Proof attempt:\*\*\s*(.+)$", row)
    if not m:
        problems.append("row has no **Proof attempt:** line")
    else:
        parts = re.split(r"\s+[-\u2014\u2013]\s+", m.group(1).strip(),
                         maxsplit=1)
        kind = parts[0].strip()
        if kind not in PROOF_KINDS:
            problems.append("illegal proof-attempt kind: %r" % kind)
        if kind != "none" and (len(parts) < 2 or not parts[1].strip()):
            problems.append("no artifact path for non-none kind")
    if not re.search(r"(?m)^-\s*\*\*Pin:\*\*\s*\S+", row):
        problems.append("row has no **Pin:** line")
    if re.search(r"(?i)\bDONE\b|\bresolved\b", row):
        problems.append("row claims resolution (DONE/resolved)")
    for field in ("Tier", "Subject", "Status", "Reduction", "Barrier",
                  "Known", "Falsifier"):
        if not re.search(r"(?m)^-\s*\*\*" + field + r":", row):
            problems.append("row missing **%s:** field" % field)
    if "**Missing (the object that does not exist as a proof):**" not in row:
        problems.append("row missing **Missing (...)** field")
    return problems


ARTIFACT_TEMPLATE = '''"""TODO: {title}

Finite certificate scaffold for Gap Ledger row {token} ({kind}).  This skeleton
proves nothing: fill the computation and record the honest wall (bounded range
only) before attaching it to the row.
"""
import json
import os


def _central_data_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        cand = os.path.join(here, "03_Data_and_Observational_Resources",
                            "02_Experimental_Data_Collections")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(here)
        if parent == here:
            raise RuntimeError("repository root not found from " + __file__)
        here = parent


OUT = os.path.join(_central_data_dir(), "{slug}.json")


def run():
    out = {{"experiment": {title!r},
           "honest_wall": "TODO: finite range only; the conjecture stays OPEN"}}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str)
    return out


if __name__ == "__main__":
    run()
'''

PIN_TEMPLATE = '''

def {pin}():
    """TODO: {subject} -- replace this scaffold with a real finite certificate.
    It deliberately raises until filled, so no gate can pass on an empty pin."""
    raise NotImplementedError("TODO: fill in the {subject} certificate")
'''


def scaffold_artifact(path, subject, token="G?", kind="certificate", slug=None):
    """Write a runnable artifact skeleton to ``path``; refuse to overwrite."""
    if os.path.exists(path):
        raise ValueError("artifact already exists: %s" % path)
    slug = slug or os.path.splitext(os.path.basename(path))[0]
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(ARTIFACT_TEMPLATE.format(title=subject, token=token,
                                          kind=kind, slug=slug))
    return True


def scaffold_pin(tests_file, pin, subject):
    """Append a *failing* pin scaffold to ``tests_file``; refuse duplicates."""
    if not os.path.exists(tests_file):
        raise ValueError("tests file does not exist: %s" % tests_file)
    with open(tests_file, encoding="utf-8", errors="replace") as fp:
        text = fp.read()
    if re.search(r"(?m)^\s*def\s+" + re.escape(pin) + r"\s*\(", text):
        raise ValueError("pin %r already defined in %s" % (pin, tests_file))
    with open(tests_file, "a", encoding="utf-8", newline="\n") as fp:
        fp.write(PIN_TEMPLATE.format(pin=pin, subject=subject))
    return True


def append_row(ledger_text, row):
    """Return ``ledger_text`` with ``row`` appended as a new section (pure)."""
    return ledger_text.rstrip("\n") + "\n\n" + row.strip("\n") + "\n"


def apply(subject, kind, artifact_rel, pin, tier="B", tests_file_rel=None,
          root=None, date=None, write=False):
    """End-to-end: scaffold the artifact + pin (if absent), render the row with
    the next G-number, and append it to the ledger.  Returns a report; only
    writes the ledger when ``write`` is true."""
    root = root or _repo_root()
    ledger_path = os.path.join(root, LEDGER_REL)
    with open(ledger_path, encoding="utf-8") as fp:
        ledger = fp.read()
    token = next_token(ledger)

    created_artifact = False
    if artifact_rel not in (None, "n/a", "") and kind != "none":
        art_path = os.path.join(root, artifact_rel)
        if not os.path.exists(art_path):
            scaffold_artifact(art_path, subject, token, kind)
            created_artifact = True

    created_pin = False
    if kind != "none" and not pin_exists(pin, root=root):
        if not tests_file_rel:
            raise ValueError("pin %r missing and no tests_file to scaffold it"
                             % pin)
        scaffold_pin(os.path.join(root, tests_file_rel), pin, subject)
        created_pin = True

    row = forge_row(subject, kind, artifact_rel, pin, tier=tier, date=date,
                    root=root, token=token)
    new_ledger = append_row(ledger, row)
    if write:
        with open(ledger_path, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(new_ledger)
    return {"token": token, "row": row, "created_artifact": created_artifact,
            "created_pin": created_pin, "ledger": new_ledger}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gap Ledger row forge")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--kind", required=True, choices=PROOF_KINDS)
    ap.add_argument("--artifact", default="n/a")
    ap.add_argument("--pin", default="n/a")
    ap.add_argument("--tier", default="B")
    ap.add_argument("--tests-file", default=None,
                    help="test file (relative to repo root) to scaffold the pin"
                         " into when --apply is used")
    ap.add_argument("--apply", action="store_true",
                    help="scaffold artifact + pin and append the row to the "
                         "live ledger")
    args = ap.parse_args(argv)

    root = _repo_root()
    if args.apply:
        report = apply(args.subject, args.kind, args.artifact, args.pin,
                       tier=args.tier, tests_file_rel=args.tests_file,
                       root=root, write=True)
        print(report["token"] + " appended; artifact scaffolded=%s, pin "
              "scaffolded=%s"
              % (report["created_artifact"], report["created_pin"]))
        return 0

    with open(os.path.join(root, LEDGER_REL), encoding="utf-8") as fp:
        token = next_token(fp.read())
    print(_render(token, args.subject, args.kind, args.artifact, args.pin,
                  args.tier, None, datetime.date.today().isoformat()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
