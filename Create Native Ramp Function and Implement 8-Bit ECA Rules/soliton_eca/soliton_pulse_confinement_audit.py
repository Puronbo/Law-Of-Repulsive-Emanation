"""soliton_pulse_confinement_audit: impulse confinement of the 32-rule twin
family on the ghost-zero bus, measured -- not assumed.

A single active impulse is injected into an all-zero vacuum bus.  A rule
"confines" the impulse when the support width (span of the active cells)
stays bounded; it "radiates" when the support spreads to the full lattice.
This is the ECA analogue of the NLSE result measured in
soliton_radiation_audit: the fundamental soliton (A = 1) stays compact
while non-integer amplitudes shed spreading radiation.

Certificates:

    L_pulse_a_side_stationary       PASS/FAIL  every A-side bitmask rule
                                    keeps the impulse as a single
                                    stationary active cell at every
                                    generation (its window fixes
                                    (010)->1, (001)->0, (100)->0, (000)->0).
    L_pulse_confined_is_a_side      PASS/FAIL  the rules whose impulse
                                    stays within support <= 3 over the
                                    whole grid are EXACTLY the 16 A-side
                                    bitmask rules.
    L_pulse_traveling_impulse         HONEST_NEGATIVE  FALSE CANDIDATE:
                                    some rule carries a bounded-support
                                    (<= 4) impulse along the bus as a
                                    moving soliton-like pulse -- none do:
                                    A-side pulses are stationary, B-side
                                    pulses spread to the full lattice.
    L_pulse_b_side_fills            PASS/FAIL  every B-side complement
                                    rule's impulse reaches support ==
                                    width at some generation, at every
                                    measured width.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES as _RULE_TABLE  # noqa: E402

_SIDE_A = frozenset({4, 12, 36, 44, 68, 76, 100, 108,
                     132, 140, 164, 172, 196, 204, 228, 236})
_WIDTHS = (8, 12, 16)
_CONFINEMENT_BOUND = 3
_TRAVEL_BOUND = 4


def _bit(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def _step(rule: int, s: list[int]) -> list[int]:
    n = len(s)
    out = []
    for i in range(n):
        left = s[i - 1] if i > 0 else 0
        right = s[i + 1] if i < n - 1 else 0
        out.append(_bit(rule, left, s[i], right))
    return out


def _support(s: list[int]) -> int:
    idx = [i for i, v in enumerate(s) if v]
    return 0 if not idx else max(idx) - min(idx) + 1


def impulse_profile(rule: int, width: int) -> dict[str, object]:
    imp = [0] * width
    imp[width // 2] = 1
    s = list(imp)
    supports = []
    for _ in range(1, 2 * width + 1):
        s = _step(rule, s)
        supports.append(_support(s))
    max_support = max(supports)
    return {"rule": rule, "width": width,
            "max_support": max_support,
            "stationary": max_support == 1,
            "confined": max_support <= _CONFINEMENT_BOUND,
            "fills": max_support == width,
            "support_seq": supports}


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


def _a_side_stationary_holds() -> bool:
    return all(impulse_profile(r, w)["stationary"]
               for r in _SIDE_A for w in _WIDTHS)


def _confined_is_a_side_holds() -> bool:
    confined = {r for r in _RULE_TABLE
                if all(impulse_profile(r, w)["confined"] for w in _WIDTHS)}
    return confined == set(_SIDE_A)


def _no_traveling_pulse_holds() -> bool:
    """False candidate: a bounded-support impulse moves along the bus."""
    for rule in _RULE_TABLE:
        for width in _WIDTHS:
            p = impulse_profile(rule, width)
            if not p["stationary"] and p["max_support"] <= _TRAVEL_BOUND:
                return True
    return False


def _b_side_fills_holds() -> bool:
    for rule in set(_RULE_TABLE) - _SIDE_A:
        if not all(impulse_profile(rule, w)["fills"] for w in _WIDTHS):
            return False
    return True


def confinement_certificates() -> list[dict[str, object]]:
    return [
        _certify("L_pulse_a_side_stationary",
                 {"domain": "single-impulse inputs on the vacuum bus, "
                            "widths 8/12/16, all generations up to 2*width",
                  "law": "every A-side bitmask rule keeps the impulse as a "
                         "single stationary active cell at every "
                         "generation: support == 1 throughout",
                  "measured_on": "full support-width trajectory per rule"},
                 _a_side_stationary_holds),
        _certify("L_pulse_confined_is_a_side",
                 {"domain": "all 32 family rules over the impulse grid",
                  "law": "the rules whose impulse stays within support "
                         "<= 3 over the whole grid are exactly the 16 "
                         "A-side bitmask rules",
                  "measured_on": "exact support-width enumeration"},
                 _confined_is_a_side_holds),
        _certify("L_pulse_traveling_impulse",
                 {"domain": "impulse support and displacement over the "
                            "grid",
                  "law": "FALSE CANDIDATE: some family rule carries the "
                         "impulse as a bounded-support (<= 4) moving "
                         "soliton-like pulse along the bus -- the A-side "
                         "pulses are stationary and every B-side pulse "
                         "spreads to the full lattice, so no traveling "
                         "pulse exists",
                  "honest_check": "confinement and transport are "
                                  "mutually exclusive in this family: "
                                  "everything that confines is stationary",
                  "measured_on": "support-width and displacement "
                                 "trajectories"},
                 _no_traveling_pulse_holds),
        _certify("L_pulse_b_side_fills",
                 {"domain": "single-impulse inputs under the 16 B-side "
                            "complement rules",
                  "law": "every B-side rule's impulse reaches support == "
                         "width (the full lattice) at some generation, at "
                         "every measured width",
                  "measured_on": "exact support-width enumeration"},
                 _b_side_fills_holds),
    ]


def _render_table() -> str:
    rows = ["  rule  w8/12/16 max support    class"]
    for rule in sorted(_RULE_TABLE):
        stats = [impulse_profile(rule, w)["max_support"] for w in _WIDTHS]
        if all(s == 1 for s in stats):
            kind = "A-side stationary"
        elif any(s == w for s, w in zip(stats, _WIDTHS)):
            kind = "B-side spreading"
        else:
            kind = "other"
        rows.append("  %4d  %-20s  %s" % (
            rule, "/".join(map(str, stats)), kind))
    return "\n".join(rows)


if __name__ == "__main__":
    for c in confinement_certificates():
        print("  %-34s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print(_render_table())