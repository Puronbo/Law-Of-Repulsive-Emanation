"""soliton_mi_destack_audit: de-stacking of the void harmonic stack.

Round 22 certified the carrier-void crest's 4-line harmonic stack
(P(+-Omega) + P(+-2-Omega) >= 0.60 at the first crest of Omega = 1.0,
all seed amplitudes).  Round 24 certified the ECA twin's TURNOVER: the
dominant pair's share peaks then collapses while concentration
continues.  This audit measures the NLSE side of the later
dynamics -- does the void stack SHED across the recurrence chain as
the carrier returns?

Measured (Omega = 1.0, seeds, same protocol as round 22; z <= 14)::

    stack (p1 + p2) at each crest:
        eps=.10  0.759   0.396
        eps=.20  0.738   0.531   0.271
        eps=.30  0.713   0.542   0.418   0.247
        eps=.45  0.662   0.487   0.516   0.454   0.349

Laws:

- the stack SHEDS more than 15% of its power within one full
  recurrence for every seed amplitude: second-crest stack <= 0.85x
  the first-crest stack (0.52x..0.76x) -- the harmonic stack is a
  first-crest structure with a fast first-cycle relaxation;
- the >= 0.60 dominance is a first-crest phenomenon: by the end of
  the sampled chain the stack is below 0.60 at every seed amplitude
  (max 0.396; down to 0.247) -- the carrier-free crest's harmonic
  purity is not sustained;
- the fundamental pair P(+-Omega) OUTLIVES the relaxation: p1 > p2 at
  every crest of every seed amplitude -- the NLSE mirror of the ECA
  turnover is a RELAXATION not an identity flip: the top pair never
  changes its identity, it only sheds share;
- HONEST_NEGATIVE: the stack share does NOT fall strictly at every
  crest -- eps = 0.45 bumps up at crest 3 (0.516 > 0.487); the
  relaxation is monotone for eps <= 0.30 but weakly non-monotone at
  the largest seed amplitude.

Certificates:

    L_dst_sheds            PASS/FAIL  second crest <= 0.85x first.
    L_dst_submajority      PASS/FAIL  final crest < 0.60 everywhere.
    L_dst_fund_persist     PASS/FAIL  p1 > p2 at every crest.
    L_dst_monotone_de        HONEST_NEGATIVE  "stack falls strictly at
                              every crest": FALSE (eps = 0.45 crest 3).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_mi_carrierfree_crest_audit import (  # noqa: E402
    carrierfree_data,
)

_SHED_FRAC = 0.85
_SUB = 0.60


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
        "first_failure": None if n_ok else {"datum": "predicate Failed"},
    }


def destack_certificates() -> tuple[list[dict[str, object]],
                                    dict[str, list[float]]]:
    data = carrierfree_data()
    stacks = {e: [c["p1"] + c["p2"] for c in data[e]] for e in data}
    sheds = max(stacks[e][1] / stacks[e][0] for e in stacks)
    finite = [e for e in stacks if stacks[e]]
    finals = max(stacks[e][-1] for e in finite)
    fund_ok = all(c["p1"] > c["p2"] for e in data for c in data[e])
    monotone = all(a >= b for e in stacks
                   for a, b in zip(stacks[e], stacks[e][1:]))
    certs = [
        _certify("L_dst_sheds",
                 {"domain": "Omega = 1.0, seeds {0.10, 0.20, 0.30, "
                            "0.45}, z <= 14, same protocol as "
                            "carrierfree (round 22)",
                  "law": "the void stack SHEDS > 15% of its power "
                         "within one full recurrence for every seed "
                         "amplitude: second-crest stack <= "
                         f"{_SHED_FRAC}x first-crest stack (max ratio "
                         f"{sheds:.2f}) -- the harmonic stack is a "
                         "first-crest structure with a fast "
                         "first-cycle relaxation",
                  "measured": {e: [round(v, 3) for v in stacks[e]]
                               for e in sorted(stacks)}},
                 lambda: sheds <= _SHED_FRAC),
        _certify("L_dst_submajority",
                 {"law": "the >= 0.60 distribution holds the power "
                         "(round 22) is a first-crest phenomenon: by "
                         "the end of the sampled chain the stack is "
                         f"below {_SUB} at every seed amplitude (max "
                         f"{finals:.3f}; down to "
                         f"{min(stacks[e][-1] for e in finite):.3f})",
                  "measured": {"final_stack": round(finals, 3)}},
                 lambda: finals < _SUB),
        _certify("L_dst_fund_persist",
                 {"law": "the fundamental pair P(+-Omega) OUTLIVES "
                         "the relaxation: p1 > p2 at every crest of "
                         "every seed amplitude -- the NLSE mirror of "
                         "the ECA turnover is a RELAXATION not an "
                         "identity flip: the top pair never changes "
                         "its identity, it only sheds share (contrast "
                         "round 24: the ECA top pair's identity turns "
                         "over as its share collapses)",
                  "measured": {e: {"p1": [round(c["p1"], 3)
                                          for c in data[e]],
                                   "p2": [round(c["p2"], 3)
                                          for c in data[e]]}
                               for e in sorted(data)}},
                 lambda: fund_ok),
        _certify("L_dst_monotone_de",
                 {"law": "the stack share falls strictly at every "
                         "crest of the chain",
                  "measured": f"FALSE: at eps = 0.45 crest 3 the stack "
                              f"bumps to {stacks['0.45'][2]:.3f} "
                              f"(crest 2: {stacks['0.45'][1]:.3f}); "
                              "the relaxation is monotone for "
                              "eps <= 0.30 but weakly non-monotone at "
                              "the largest seed amplitude",
                  "max_rebound": round(
                      max(max(b - a, 0.0) for e in stacks
                          for a, b in zip(stacks[e], stacks[e][1:])), 3)},
                 lambda: monotone),
    ]
    return certs, stacks


if __name__ == "__main__":
    certs, stacks = destack_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    for e in sorted(stacks):
        print("  eps=%s stack per crest: %s" % (
            e, " ".join("%.3f" % v for v in stacks[e])))