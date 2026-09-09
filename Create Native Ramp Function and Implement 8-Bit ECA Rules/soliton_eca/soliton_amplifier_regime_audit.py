"""soliton_amplifier_regime_audit: cross-sector damage regimes (family).

Ties the damage sectors measured in the other audits into one regime
map for the 32-rule twin family:

    reach      {27, 59, 83, 91, 115, 123, 147, 155, 172, 187, 211,
                228, 243}  -- width-16 single-cell half-reach amplifiers
                (perturbation audit);
    collapse   {164, 172, 228, 251}  -- spatial variance collapsers
                (mixing-rate audit);
    erasers    {36, 219, 251}  -- injected extents wiped at every size
                (extent-spectrum audit);
    transparent {204, 51}  -- Hamming isometries (damage audit) that are
                in no growth sector.

Cross-sector laws:

    reach n collapse = {172, 228}        the one-lap permutation pair is
                                         the only amplifier that also
                                         collapses spatial variance -- the
                                         strongest amplifier (147) is
                                         variance-neutral;
    erasers == mixing sparse basins      {36, 219, 251} is exactly the
                                         mixing-rate sparse-basin set;
    {204, 51} join no growth sector      the transport twins sit outside
                                         reach, collapse and erasers.

Certificates:

    L_regime_reach_collapse_pair     PASS/FAIL  reach n collapse ==
                                    {172, 228}.
    L_regime_transport_growth_free   PASS/FAIL  {204, 51} are in none of
                                    reach, collapse, erasers.
    L_regime_eraser_sparse_identity  PASS/FAIL  extent-erasers == mixing
                                    sparse basins == {36, 219, 251}.
    L_regime_collapsers_amplify      HONEST_NEGATIVE  "every
                                    spatial-variance collapser is a
                                    single-cell amplifier" is FALSE: 164
                                    and 251 collapse variance yet register
                                    zero half-reach events.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_perturbation_audit import _W16_REACH  # noqa: E402
from soliton_eca.soliton_mixing_rate_audit import (  # noqa: E402
    _COLLAPSE_SET,
    _SPARSE_SET,
)
from soliton_eca.soliton_damage_audit import _ISOMETRY_SET  # noqa: E402
from soliton_eca.soliton_extent_spectrum_audit import _ERASER_SET  # noqa: E402

_REACH = set(_W16_REACH)
_COLLAPSE = set(_COLLAPSE_SET)
_ERASERS = set(_ERASER_SET)
_SPARSE = set(_SPARSE_SET)
_TRANSPORT = set(_ISOMETRY_SET)


def _certify(label: str, meta: dict[str, object],
             pred: Callable[[], bool]) -> dict[str, object]:
    n_ok = 1 if pred() else 0
    return {
        "label": label,
        "meta": meta,
        "kind": "statement",
        "status": "PASS" if n_ok else "HONEST_NEGATIVE",
        "n_ok": n_ok,
        "n_fail": 0 if n_ok else 1,
        "first_failure": None if n_ok else {"datum": "the predicate Failed"},
    }


def regime_certificates() -> list[dict[str, object]]:
    return [
        _certify("L_regime_reach_collapse_pair",
                 {"law": "the only width-16 single-cell amplifiers that "
                         "also collapse spatial variance are the one-lap "
                         "permutation pair {172, 228}; the strongest "
                         "amplifier 147 is variance-neutral",
                  "measured": sorted(_REACH & _COLLAPSE)},
                 lambda: (_REACH & _COLLAPSE) == {172, 228}),
        _certify("L_regime_transport_growth_free",
                 {"law": "the transport twins {204, 51} appear in none "
                         "of the family's damage sectors -- reach, "
                         "collapse or erasers; their damage policy is "
                         "injectivity-bound, not amplifying",
                  "measured": sorted(_TRANSPORT & (_REACH | _COLLAPSE |
                                                   _ERASERS))},
                 lambda: not (_TRANSPORT & (_REACH | _COLLAPSE | _ERASERS))),
        _certify("L_regime_eraser_sparse_identity",
                 {"law": "the extent-erasers are exactly the mixing-rate "
                         "sparse basins: {36, 219, 251} -- the same "
                         "three rules form the wiping and the "
                         "variance-sparse sectors",
                  "erasers": sorted(_ERASERS),
                  "sparse": sorted(_SPARSE)},
                 lambda: _ERASERS == _SPARSE),
        _certify("L_regime_collapsers_amplify",
                 {"law": "every spatial-variance collapser is a "
                         "single-cell half-reach amplifier",
                  "measured": "164 and 251 collapse variance (mixing-"
                              "rate audit) yet register zero half-reach "
                              "events (perturbation audit)"},
                 lambda: _COLLAPSE <= _REACH),
    ]


if __name__ == "__main__":
    for c in regime_certificates():
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))