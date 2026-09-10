"""validate_soliton_millennium_meta_audit: T4, bridge meta pointing at proofs.

The certificates live on three artifacts built in three different ways,
and the meta-audit refuses to let any of them drift out of the doc
record: it greps the actual sources for the closed theorems and pins
the register wording to the suite count.

    kind   artifact                     gate
    ----   ------------------------------------------------------------
    Lean   PunoCalculus.EcaIsometry     affine_class_exact,
           (v4.33.0, pure core,         isometry_class_exact,
            native_decide)              rule204_identity_widths,
                                        rule51_complement_widths,
                                        complementGen
Lean   PunoCalculus.MillenniumBridge  statuses :: NOT SETTLED BY
           (decidable strings)            THIS PROJECT, statuses.length=7
            (seven_problems_declared_unsolved)
    Lean   PunoTwin.TwinAnalyticLaws    rho_eq_structure,
           (mathlib v4.33.1)            rho_eq_abs_profile,
                                         antiderivative_deriv,
                                         antiderivative_hasDerivAt,
                                         window_defect_exact,
                                         defect_at_L,
                                         defect_tendsto_zero,
                                         defect_window_closed_form,
                                         defect_at_L_tail_lt_window
    Lean   PunoTwin.TwinRingLaws        step204_eq, step51_eq,
           (mathlib v4.33.1)            sumBits_eq, compBits_eq,
                                         rule204_identity_all,
                                         rule51_complement_all
    py     validate_..._closed_forms    exact rational 2048/65537,
                                         65536/67108865
    md     Soliton-Bus ... .md          "86 root validators", the
                                         theorem names, the exact
                                         rationals, seven delimitations

Provenance: the PunoTwin twin files mirror the mathlib v4.33.1 origin
repository github.com/Puronbo/Millennium-Prize-Problem-Lean-4-Proof at
commit 6acb7f9c2e0803714f8fc894ddf8fe8a5017bb72.  The vendored copies in
PunoCalculus/PunoCalculus/PunoTwin and the origin tree must stay
byte-identical (hash-audited); bumping the mathlib rev in either place
invalidates the other.

The honest constraint is re-pinned here as well: none of the three
artifact kinds may assert that a Millennium problem is settled.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
PW = WORKSPACE / "PunoCalculus" / "PunoCalculus"
TWIN_ORIGIN_SHA = "6acb7f9c2e0803714f8fc894ddf8fe8a5017bb72"
TWIN_ORIGIN_URL = "github.com/Puronbo/Millennium-Prize-Problem-Lean-4-Proof"


def _puno_twin() -> Path:
    env = os.environ.get("PUNO_TWIN_PATH")
    cand = [Path(env)] if env else []
    cand += [
        PW / "PunoTwin",
        Path(r"C:\Users\Me\Desktop\Mamamogobyerno\fcc2\Millennium-Prize-Problem-Lean-4-Proof\PunoTwin"),
        Path.home() / "Desktop" / "Mamamogobyerno" / "fcc2"
        / "Millennium-Prize-Problem-Lean-4-Proof" / "PunoTwin",
    ]
    for p in cand:
        if p.is_dir():
            return p
    raise FileNotFoundError(
        "PunoTwin not found; set PUNO_TWIN_PATH to its directory")


MW = _puno_twin()
DOC = ROOT / "Soliton-Bus Elementary Cellular Automata.md"

ECHO = [
    "affine_class_exact", "isometry_class_exact",
    "rule204_identity_widths", "rule51_complement_widths",
    "complementGen",
]
MBR = [
    "statuses", "NOT SETTLED BY THIS PROJECT",
    "seven_problems_declared_unsolved",
]
TWIN = [
    "rho_eq_structure", "rho_eq_abs_profile",
    "antiderivative_deriv", "antiderivative_hasDerivAt",
    "window_defect_exact", "defect_at_L", "defect_tendsto_zero",
    "defect_window_closed_form",
    "defect_window_closed_form :",
    "(16 : ℚ) * 1 * 128 / (1 + 4 * 1 * 128 ^ 2) = (2048 : ℚ) / 65537",
    "defect_at_L_tail_lt_window",
    "defect_at_L_tail_lt_window :",
    "(16 : ℚ) * 1 * 4096 / (1 + 4 * 1 * 4096 ^ 2) < (2048 : ℚ) / 65537",
]
RING = [
    "step204_eq", "step51_eq",
    "sumBits_eq", "compBits_eq",
    "rule204_identity_all", "rule51_complement_all",
]
DOCPINS = [
    "86 root validators",
    "2048/65537",
    "65536/67108865",
    "TwinAnalyticLaws",
    "TwinRingLaws",
    "rule204_identity_all",
    "rule51_complement_all",
    "NOT SETTLED BY THIS",
    "declared NOT SETTLED explicitly",
    "PunoTwin",
    TWIN_ORIGIN_SHA,
    TWIN_ORIGIN_URL,
]


def _grep(path: Path, needles: list[str]) -> list[str]:
    text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8",
                                              errors="ignore"))
    return [n for n in needles if n not in text]


def _check(label: str, missing: list[str]) -> None:
    ok = not missing
    print(f"  [{'PASS ' if ok else 'FAIL '}] {label}"
          + ("" if ok else f" missing: {missing}"))
    assert not missing, (label, missing)


def _root_validator_count() -> int:
    return len(list(ROOT.glob("validate_*.py")))


print("soliton millennium meta audit (bridge meta -> proofs)")
_check("EcaIsometry carries the five closure theorems",
       _grep(PW / "EcaIsometry.lean", ECHO))
_check("MillenniumBridge carries the seven NOT-SETTLED declarations",
       _grep(PW / "MillenniumBridge.lean", MBR))
_check("TwinAnalyticLaws carries the seven mass-law theorems",
       _grep(MW / "TwinAnalyticLaws.lean", TWIN))
_check("TwinRingLaws carries the general-width ring closure",
       _grep(MW / "TwinRingLaws.lean", RING))
_check("the docs pin the suite count and the certified rationals",
       _grep(DOC, DOCPINS))
_check("on-disk validator count matches the prose-pinned count",
       [] if _root_validator_count() == 86
       else [f"on-disk {_root_validator_count()} != pinned 86"])

# honest constraint across artifacts: no settlement assertion may appear
# in any of the sources carrying these names.
for name, path in [("EcaIsometry.lean", PW / "EcaIsometry.lean"),
                   ("MillenniumBridge.lean", PW / "MillenniumBridge.lean"),
                   ("TwinAnalyticLaws.lean", MW / "TwinAnalyticLaws.lean"),
                   ("TwinRingLaws.lean", MW / "TwinRingLaws.lean")]:
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    hits = [s for s in ("is solved", "is settled", "proves ", "proved:",
                        "are settled") if re.search(r"\b" + re.escape(s),
                                                    text)]
    assert not hits, (name, hits)
print("soliton millennium meta audit passed: Lean T1/T2 + T3/T4 sources,"
      " docs, and seven delimitations are all pinned in one register")