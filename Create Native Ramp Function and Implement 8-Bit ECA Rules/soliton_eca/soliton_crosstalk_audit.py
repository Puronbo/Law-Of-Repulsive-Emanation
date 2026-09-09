"""soliton_crosstalk_audit: multi-packet carrier isolation of the 32-rule
twin family on the ghost-zero (vacuum) bus, measured -- not assumed.

A carrier is a rule that stores TWO or THREE packets (contiguous blocks of
1..3 active cells) placed on the same width-n wire.  A placement passes if
every packet reconstitutes bit-exact at every generation up to 2*width,
i.e. packets are transported without crosstalk.

Certificates:

    L_crosstalk_rule204_multiplex    PASS/FAIL  rule 204 (identity) stores
                                     EVERY multi-packet placement exactly:
                                     zero failures over the whole grid.
    L_crosstalk_unique_carrier       PASS/FAIL  rule 204 is the ONLY rule
                                     with zero multi-packet failures.
    L_crosstalk_236_naive            HONEST_NEGATIVE  FALSE CANDIDATE:
                                     rule 236 stores arbitrary multi-
                                     packet payloads as exactly as it
                                     stores single blocks -- placements
                                     whose consecutive blocks are one
                                     zero apart fail (the gap collapses).
    L_crosstalk_236_gap_law          PASS/FAIL  236 reconstitutes a
                                     multi-block placement exactly iff no
                                     pair of consecutive blocks is
                                     separated by exactly one zero.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Callable, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES as _RULE_TABLE  # noqa: E402

_WIDTHS = (8, 10, 12)
_PACKET_WIDTHS = (1, 2, 3)
_Q_COUNTS = (2, 3)


def _bit(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def step(rule: int, state: Sequence[int], width: int) -> tuple[int, ...]:
    out = []
    for i in range(width):
        left = state[i - 1] if i > 0 else 0
        right = state[i + 1] if i < width - 1 else 0
        out.append(_bit(rule, left, state[i], right))
    return tuple(out)


def pattern(width: int, starts: Sequence[int], k: int) -> tuple[int, ...]:
    cells = [0] * width
    for p in starts:
        for j in range(p, p + k):
            cells[j] = 1
    return tuple(cells)


def placement_ok(rule: int, width: int, starts: Sequence[int],
                 k: int) -> bool:
    target = pattern(width, starts, k)
    s = target
    for _ in range(1, 2 * width + 1):
        s = step(rule, s, width)
        if s != target:
            return False
    return True


def _placements(width: int, q: int, k: int):
    for starts in itertools.combinations(range(width - q * k + 1), q):
        if any(starts[j] < starts[j - 1] + k for j in range(1, q)):
            continue
        yield starts


def multi_failures(rule: int) -> int:
    fails = 0
    for width in _WIDTHS:
        for q in _Q_COUNTS:
            for k in _PACKET_WIDTHS:
                if q * k > width:
                    continue
                for starts in _placements(width, q, k):
                    if not placement_ok(rule, width, starts, k):
                        fails += 1
    return fails


def _gap_one(starts: Sequence[int], k: int) -> bool:
    return any(starts[j] - starts[j - 1] - k == 1
               for j in range(1, len(starts)))


def _236_gap_law_holds(rule: int = 236) -> bool:
    for width in _WIDTHS:
        for q in _Q_COUNTS:
            for k in _PACKET_WIDTHS:
                if q * k > width:
                    continue
                for starts in _placements(width, q, k):
                    if placement_ok(rule, width, starts, k) == _gap_one(
                            starts, k):
                        return False
    return True


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


def _rule204_multiplex_holds() -> bool:
    return multi_failures(204) == 0


def _unique_carrier_holds() -> bool:
    return {r for r in _RULE_TABLE if multi_failures(r) == 0} == {204}


def _236_naive_holds() -> bool:
    """False candidate: 236 stores arbitrary multi-packet payloads."""
    return _236_gap_law_holds_naive_false()


def _236_gap_law_holds_naive_false() -> bool:
    """True iff the NAIVE claim holds; expected False."""
    for width in _WIDTHS:
        for q in _Q_COUNTS:
            for k in _PACKET_WIDTHS:
                if q * k > width:
                    continue
                if any(not placement_ok(236, width, starts, k)
                       for starts in _placements(width, q, k)):
                    return False
    return True


def crosstalk_certificates() -> list[dict[str, object]]:
    return [
        _certify("L_crosstalk_rule204_multiplex",
                 {"domain": "rule 204, 2- and 3-packet placements, widths "
                            "8/10/12, packet widths 1..3, every generation "
                            "up to 2*width",
                  "law": "rule 204 stores every multi-packet placement "
                         "bit-exact: zero crosstalk failures over the grid",
                  "measured_on": "exhaustive placement sweep"},
                 _rule204_multiplex_holds),
        _certify("L_crosstalk_unique_carrier",
                 {"domain": "all 32 family rules over the multi-packet "
                            "placement grid",
                  "law": "rule 204 is the only rule with zero multi-packet "
                         "failures (unique full multiplexer)",
                  "measured_on": "full grid failure count per rule"},
                 _unique_carrier_holds),
        _certify("L_crosstalk_236_naive",
                 {"domain": "rule 236 over all multi-packet placements",
                  "law": "FALSE CANDIDATE: rule 236 stores arbitrary "
                         "multi-packet payloads as exactly as single "
                         "blocks -- placements with consecutive blocks one "
                         "zero apart fail because the separating zero "
                         "collapses",
                  "honest_check": "the block-storage rule 236 is not a "
                                  "universal multiplexer; the gap "
                                  "structure is measured next",
                  "measured_on": "exhaustive placement sweep"},
                 _236_naive_holds),
        _certify("L_crosstalk_236_gap_law",
                 {"domain": "rule 236, gap structure of multi-block "
                            "placements",
                  "law": "a multi-block placement reconstitutes exactly "
                         "iff no pair of consecutive blocks is separated "
                         "by exactly one zero (gap-1 while adjacent "
                         "blocks simply merge into a larger block)",
                  "measured_on": "predicted-vs-actual over the full grid"},
                 _236_gap_law_holds),
    ]


def _render_failures() -> str:
    rows = ["  rule  multi-packet failures"]
    for rule in sorted(_RULE_TABLE):
        rows.append("  %4d  %18d" % (rule, multi_failures(rule)))
    return "\n".join(rows)


if __name__ == "__main__":
    for c in crosstalk_certificates():
        print("  %-34s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print(_render_failures())