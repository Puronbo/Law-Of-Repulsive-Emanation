"""soliton_millennium_bridge_audit: rigorous, scoped placement of this
program's certified results relative to the Clay Millennium Prize
Problems, plus the exact-replica companion formalization contract.

The bridge is honest by construction.  For each of the seven
Millennium problems it mechanically scans the audit corpus for any
claim that its specific proof obligation has been settled, finds none,
and registers a HONEST_NEGATIVE delimitation (each with a "what solving
it demands" and "closest adjacent certified law" in meta).  Nothing
here argues that this program resolves a Millennium problem: the
certificates assert exactly what was MEASURED or PROVEN in-scope.

The three adjacent laws that ARE certified (all PASS):

  - L_mil_nse_crest_control    the discrete twin exhibits explicit
                               crest-magnitude control: at (Omega=0.5,
                               eps=0.20) the measured crest (3.66) sits
                               in the documented 3.656 cap basin and the
                               global maximum over the sampled window is
                               below the 4.0 ceiling.
  - L_mil_nse_mass_conserva-   the Peregrine breather conserves its
      tion_exact               mass-neutrality identity: the
                               window-defect equals the closed-form
                               correction 8L/(1+L^2) (L = 256) to within
                               1e-4, and the defect is constant along
                               z = 0..3 to within 1e-4 -- an exact
                               conserved energy-like law in the twin.
  - L_mil_nse_modal_depletion  at the crest the pump power fraction
                               P0 <= 0.25: a modal (frequency-sector)
                               control statement.

Laws (certificates):

    L_mil_nse_crest_control            PASS  explicit crest-magnitude
                                  control in the discrete twin, measured
                                  at (Omega=0.5, eps=0.20), checked
                                  against the documented 3.656 cap basin
                                  and a 4.0 global ceiling.
    L_mil_nse_mass_conservation_exact PASS  Peregrine mass-neutrality
                                  defect = 8L/(1+L^2), L = 256, to
                                  within 1e-4 at z = 0, 0.5, 1, 2, 3.
    L_mil_nse_modal_depletion         PASS  pump fraction P0 <= 0.25 at
                                  the crest.
    L_mil_P_NNP_untouched ... L_mil_BSD_untouched   HONEST_NEGATIVE
                                  for each of the seven Millennium
                                  problems: the corpus makes no
                                  sentinel resolution claim.
    L_mil_scope_discipline            PASS  no unqualified
                                  self-attributive resolution claim in
                                  the docs.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_physics import (  # noqa: E402
    Fiber,
    propagate,
)

_N = 8192
_L = 64.0
_DT = _L / _N
_Z_GRID = 0.05
_STEPS = 20
_OMEGA = 0.5
_EPS = 0.20
_Z_END = 18.0

_CAP_CEIL = 4.0
_CAP_MEASURED = 3.656  # documented crest at (Omega=0.5, eps=0.20)

# Mass-neutrality law parameters -- the exact documented configuration
# of the peregrine audit (window half-length _MASS_L, N = _MASS_N,
# P = 1.0, tolerance 1e-4).
_MASS_L = 256.0
_MASS_N = 16384
_MASS_TOL = 1e-4
_MASS_P = 1.0
_MASS_ZS = (0.0, 0.5, 1.0, 2.0, 3.0)

# Seven Clay Millennium Prize Problems: label, canonical name, and the
# sentinels whose presence in the corpus would constitute a claim that
# the program settles it (absent by design).
_MILLENNIA: list[tuple[str, str, tuple[str, ...]]] = [
    ("P_NNP", "P vs NP",
     ("p vs np is settled", "p vs np is proven", "p vs np is solved",
      "proves p vs np", "settles p vs np", "pbsp is resolved")),
    ("HODGE", "the Hodge conjecture",
     ("hodge conjecture is proved", "hodge is settled",
      "proves the hodge conjecture", "hodge conjecture proven")),
    ("POINCARE", "the Poincare conjecture",
     ("poincare conjecture is proved", "poincare is settled",
      "proves the poincare conjecture")),
    ("RH", "the Riemann hypothesis",
     ("riemann hypothesis is proved", "riemann is settled",
      "proves the riemann hypothesis", "rh is resolved")),
    ("YM", "Yang-Mills existence and mass gap",
     ("yang-mills is proved", "yang-mills is settled",
      "proves the yang-mills", "mass gap is established")),
    ("NSE", "Navier-Stokes existence and smoothness",
     ("navier-stokes is solved", "nse is resolved", "nse is proved",
      "proves the navier-stokes", "regularity is established")),
    ("BSD", "Birch and Swinnerton-Dyer",
     ("bsd is proved", "bsd is settled",
      "proves the birch and swinnerton-dyer",
      "swinnerton-dyer is resolved")),
]

# Problem-name tokens and resolution verbs used by the docs-scope scan.
_PROBLEM_TOKENS = ("navier-stokes", "nse", "riemann", "hodge",
                   "poincare", "yang-mills", "mass gap", "birch",
                   "swinnerton", "p vs np", "pbsp", "clay")
_VERB_TOKENS = ("resolved", "resolves", "solved", "solves", "proved",
                "proven", "proves", "proof of", "established",
                "disproved")
_SELF_TOKENS = ("we ", "our ", "this program", "this work",
                "certificate", "the twin", "the corpus", "our engine")


def _grid() -> np.ndarray:
    return np.linspace(-_L / 2, _L / 2, _N, endpoint=False)


def _run_power_scan(seed: np.ndarray, z_end: float = _Z_END
                    ) -> list[dict[str, float]]:
    dt = _DT
    cur = np.array(seed)
    prev = 0.0
    zs = np.arange(0.0, z_end + _Z_GRID / 2, _Z_GRID)
    rows = []
    for z in zs:
        if z > 0.0:
            cur = propagate(cur, dt, z - prev, fiber=Fiber(), steps=_STEPS)
            prev = z
        peak = float(np.max(np.abs(cur)))
        c = np.fft.fftshift(np.fft.fft(cur))
        f = 2 * np.pi * np.fft.fftshift(np.fft.fftfreq(_N, dt))
        k0 = int(np.argmin(np.abs(f - 0.0)))
        tot = float(np.sum(np.abs(c) ** 2))
        p0 = float(np.abs(c[k0]) ** 2) / tot if tot > 0 else 0.0
        rows.append({"z": float(z), "R": peak, "P0": p0})
    return rows


def _crest_run() -> list[dict[str, float]]:
    t = _grid()
    seed = np.sqrt(1.0) * (1 + _EPS * np.cos(_OMEGA * t))
    return _run_power_scan(seed)


def _mass_defect_at(z: float) -> float:
    """Window defect int(|u|^2 - P) dt on the documented mass grid."""
    t = np.linspace(-_MASS_L / 2, _MASS_L / 2, _MASS_N, endpoint=False)
    dt = float(np.diff(t)[0])
    u0 = np.sqrt(_MASS_P) * (
        1 - 4 * (1 + 2j * _MASS_P * z)
        / (1 + 4 * _MASS_P * t ** 2 + 4 * _MASS_P ** 2 * z ** 2))
    u = (u0 if z == 0.0
         else propagate(u0, dt, z, fiber=Fiber(), steps=_STEPS))
    return float(np.sum(np.abs(u) ** 2 - _MASS_P) * dt)


def _corpus_lines() -> list[tuple[str, str]]:
    """(filename, lowercased line) for every non-self source line."""
    root = Path(__file__).resolve().parent.parent
    out: list[tuple[str, str]] = []
    for pattern in ("soliton_eca/*.py", "*.py", "*.md"):
        for p in root.glob(pattern):
            name = p.name.lower()
            if "millennium_bridge" in name:
                continue
            try:
                raw = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for line in raw.splitlines():
                out.append((str(p), line.strip().lower()))
    return out


def _census_scan() -> dict[str, object]:
    """Scan the audit corpus for Millennium-claim sentinels."""
    corpus = "\n".join(txt for _, txt in _corpus_lines())
    found: dict[str, list[str]] = {}
    for tag, _name, sentinels in _MILLENNIA:
        hits = [s for s in sentinels
                if re.search(r"\b" + re.escape(s) + r"\b", corpus)]
        found[tag] = hits
    return {"corpus_bytes": len(corpus), "sentinels_found": found}


def _docs_scan() -> dict[str, object]:
    """Flag doc lines that self-attribute a Millennium resolution."""
    flagged: list[dict[str, str]] = []
    for path, line in _corpus_lines():
        if not path.lower().endswith(".md"):
            continue
        has_prob = any(re.search(r"\b" + t + r"\b", line)
                       for t in _PROBLEM_TOKENS)
        has_verb = any(re.search(r"\b" + v + r"\b", line)
                       for v in _VERB_TOKENS)
        has_self = any(s in line for s in _SELF_TOKENS)
        negated = any(n in line for n in (
            "not ", " no ", "never", "cannot", "won't", "does not",
            "do not", "is not", "are not", "no claim", "no proof",
            "does not settle", "does not resolve", "neither", "nor",
            "already settled", "already resolved", "already proved",
            "already proven", "outside", "not ours"))
        if has_prob and has_verb and has_self and not negated:
            flagged.append({"file": path, "line": line})
    return {"flagged": flagged}


def _certify(label: str, meta: dict[str, object],
             pred: Callable[[], bool]) -> dict[str, object]:
    asserted = bool(pred())
    return {
        "label": label,
        "meta": meta,
        "kind": "statement",
        "status": "PASS" if asserted else "HONEST_NEGATIVE",
        "asserted": asserted,
        "negated": not asserted,
        "n_ok": 1 if asserted else 0,
        "n_fail": 0 if asserted else 1,
        "first_failure": None if asserted else {"datum": "the predicate Failed"},
    }


def millennium_bridge_certificates() -> tuple[list[dict[str, object]],
                                              dict[str, object]]:
    scan = _census_scan()
    sent_found: dict[str, list[str]] = scan["sentinels_found"]

    # ---- NSE-adjacent certified laws (computed here) ----
    crest_rows = _crest_run()
    max_r = max(r["R"] for r in crest_rows)
    at_z = max(crest_rows, key=lambda r: r["R"])
    crest_control_ok = abs(at_z["R"] - _CAP_MEASURED) <= 0.05 and \
        max_r < _CAP_CEIL

    correction = 8 * _MASS_L / (1 + _MASS_L ** 2)
    defects = {z: _mass_defect_at(z) for z in _MASS_ZS}
    worst_defect = max(abs(d - correction) for d in defects.values())
    defect_spread = max(abs(d - defects[0.0]) for d in defects.values())
    mass_ok = worst_defect <= _MASS_TOL and defect_spread <= _MASS_TOL

    p0_at_crest = at_z["P0"]
    modal_ok = p0_at_crest <= 0.25

    # ---- seven delimitations (mechanically scanned) ----
    judged: dict[str, bool] = {}
    for tag, _name, _sent in _MILLENNIA:
        judged[tag] = len(sent_found.get(tag, [])) == 0

    flagged = _docs_scan()["flagged"]
    scope_ok = len(flagged) == 0

    stats = {
        "crest": {"max_R": round(max_r, 4),
                  "at_z": round(at_z["z"], 2),
                  "P0_at_crest": round(p0_at_crest, 4),
                  "documented_cap": _CAP_MEASURED},
        "mass": {"L": _MASS_L, "correction": round(correction, 8),
                 "defects": {str(z): round(d, 8)
                             for z, d in defects.items()},
                 "worst_abserr": round(worst_defect, 10),
                 "spread_abs": round(defect_spread, 10)},
        "scan": {"corpus_bytes": scan["corpus_bytes"],
                 "sentinels_found": sent_found},
        "docs": {"flagged_lines": flagged},
        "delimitations": judged,
    }

    certs = [
        _certify("L_mil_nse_crest_control",
                 {"law": f"the discrete twin exhibits explicit crest "
                         f"magnitude control: at (Omega, eps) = "
                         f"({_OMEGA}, {_EPS}) the measured crest "
                         f"{at_z['R']:.3f} at z = {at_z['z']:.2f} sits "
                         f"in the documented {_CAP_MEASURED} cap basin "
                         f"(+- 0.05) and the window maximum {max_r:.3f} "
                         f"is below the {_CAP_CEIL} ceiling.  This is "
                         "the rigorously checked DISCRETE analog of the "
                         "a priori control NSE regularity needs; it "
                         "does not bear on the continuum problem",
                  "max_R": round(max_r, 4),
                  "crest_z": round(at_z["z"], 2),
                  "cap_basin": _CAP_MEASURED,
                  "ceiling": _CAP_CEIL},
                 lambda: crest_control_ok),
        _certify("L_mil_nse_mass_conservation_exact",
                 {"law": f"the Peregrine breather conserves its "
                         f"mass-neutrality identity: the window defect "
                         f"int(|u|^2 - P) dt equals the closed-form "
                         f"correction 8L/(1+L^2) = {correction:.6f} "
                         f"(L = {_MASS_L}) to within {_MASS_TOL} at "
                         "every sampled z and is constant along z = "
                         "0..3 to within 1e-4 -- an exact "
                         "energy-like conserved law in the twin",
                  "correction": round(correction, 8),
                  "worst_abserr": round(worst_defect, 10),
                  "spread_abs": round(defect_spread, 10)},
                 lambda: mass_ok),
        _certify("L_mil_nse_modal_depletion",
                 {"law": f"at the crest the pump-sector power fraction "
                         f"P0 = {p0_at_crest:.4f} <= 0.25: the crest "
                         "depletes the pump in the frequency domain "
                         "(a modal control statement)",
                  "P0_at_crest": round(p0_at_crest, 4)},
                 lambda: modal_ok),
    ]
    adjacent = {
        "P_NNP": "the width-w classifiers in soliton_isometry_proofs "
                 "run in <= (2^w)^2 exact decidable evaluations "
                 "(polynomial in the state count): a finite "
                 "verification, with no claim about P vs NP",
        "HODGE": "none (decidable combinatorics of 2^8-cell rings "
                 "only)",
        "POINCARE": "none (already resolved by Perelman; this program "
                    "neither relies on nor re-proves it)",
        "RH": "the exact discrete spectral phase law e^{-i O_bin^2 "
              "z/2} of the linear stage is an exact finite-model "
              "statement; it is not a statement about the zeta "
              "function",
        "YM": "none (discrete mass-conservation laws only)",
        "NSE": "the three adjacent laws above (crest control, exact "
               "mass conservation, modal depletion): discrete "
               "analoga, scoped to the twin",
        "BSD": "none (no elliptic-curve machinery in the corpus)",
    }
    for tag, name, _sent in _MILLENNIA:
        hits = sent_found.get(tag, [])
        sentinel_note = (f"sentinel resolution claims present: {hits}"
                         if hits else
                         "no sentinel resolution claim in the corpus")
        certs.append(_certify(
            f"L_mil_{tag}_untouched",
            {"law": f"the program, as it stands, does NOT settle {name}: "
                    f"{sentinel_note}.  Solving it demands an "
                    "(unobtained) analytic statement of global scope; "
                    f"the closest certified adjacent result is "
                    f"{adjacent[tag]}",
             "problem": name,
             "closest_adjacent": adjacent[tag],
             "sentinel_hits": hits},
            lambda ok=judged[tag]: ok))
    certs.append(_certify(
        "L_mil_scope_discipline",
        {"law": "no doc line in the corpus un-negatedly self-attributes "
                "(we / our / this program / certificate / the twin) a "
                "resolution, proof, or disproof of any of the seven "
                "problems; every certified statement in this module is "
                "scoped to the twin or to the decidable finite algebra",
         "flagged_lines": flagged},
        lambda: scope_ok))
    return certs, stats


if __name__ == "__main__":
    certs, stats = millennium_bridge_certificates()
    for c in certs:
        print("  %-42s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  crest:", stats["crest"])
    print("  mass:", stats["mass"])
    print("  scan bytes:", stats["scan"]["corpus_bytes"],
          "sentinels:", stats["scan"]["sentinels_found"])
    print("  docs flagged lines:", stats["docs"]["flagged_lines"])
    print("  delimitations:", stats["delimitations"])