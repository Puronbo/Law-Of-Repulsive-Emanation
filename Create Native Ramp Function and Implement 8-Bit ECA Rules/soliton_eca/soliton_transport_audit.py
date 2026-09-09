"""soliton_transport_audit: packet transport semantics of the 32-rule twin
family, measured -- not assumed, on both boundary policies.

A "packet" is a contiguous run of k active cells on a width-n wire.  Two
boundary policies are compared:

  ring   periodic (wraparound) boundaries -- the setting in which the
         exact state-space census found one-lap gliders {172, 228}
         (max cycle == width) and two-lap gliders {27, 59, 83, 115}
         (max cycle == 2*width);
  bus    ghost-zero (vacuum) boundaries -- the actual semantics of the
         soliton-bus engine SolitonECA.step().

Certificates:

    L_transport_rule204_bus_identity     PASS/FAIL  rule 204 (f = center)
                                         stores EVERY packet bit-exact on
                                         the vacuum bus at every generation:
                                         reconstitution error rate zero
                                         over the entire grid.
    L_transport_ring_lap_reconstitution  PASS/FAIL  on rings, every packet
                                         from the two-lap rules reappears
                                         at its exact starting state after
                                         2*width generations and from the
                                         one-lap rules after width
                                         generations.
    L_transport_bus_lap_reconstitution   PASS/FAIL  the same lap claim
                                         transferred to the vacuum bus.
    L_transport_rigid_conveyor           PASS/FAIL  FALSE CANDIDATE: some
                                         family rule other than the
                                         identity transports a packet as a
                                         rigid body with a constant
                                         nonzero displacement per
                                         generation (a conveyor belt).
    L_transport_storage_pair_exact       PASS/FAIL  the rules with zero
                                         reconstitution failures over the
                                         whole bus grid are exactly the
                                         pair {204, 236}.
    L_transport_rule236_block_storage    PASS/FAIL  rule 236 additionally
                                         stores EVERY contiguous block
                                         (any width 1..n) at every offset
                                         on the vacuum bus: exact storage
                                         beyond the narrow packet grid.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Callable, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES as _RULE_TABLE  # noqa: E402

_ONE_LAP = frozenset({172, 228})
_TWO_LAP = frozenset({27, 59, 83, 115})
_WIDTHS = (8, 10, 12)
_PACKET_WIDTHS = (1, 2, 3)


def _bit(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def step(rule: int, state: Sequence[int], boundary: str) -> tuple[int, ...]:
    n = len(state)
    out = []
    for i in range(n):
        left = state[(i - 1) % n] if boundary == "ring" else \
            (state[i - 1] if i > 0 else 0)
        right = state[(i + 1) % n] if boundary == "ring" else \
            (state[i + 1] if i < n - 1 else 0)
        out.append(_bit(rule, left, state[i], right))
    return tuple(out)


def _packet(width: int, k: int, start: int) -> tuple[int, ...]:
    return tuple(1 if start <= i < start + k else 0 for i in range(width))


def reconstitutes(rule: int, boundary: str, width: int, k: int,
                  start: int, gen: int) -> bool:
    s = _packet(width, k, start)
    for _ in range(gen):
        s = step(rule, s, boundary)
    return s == _packet(width, k, start)


def lap_reconstitutes(rule: int, boundary: str, width: int, k: int,
                      start: int) -> bool:
    gen = width if rule in _ONE_LAP else 2 * width
    return reconstitutes(rule, boundary, width, k, start, gen)


def rigid_shift(rule: int, width: int, k: int, start: int,
                horizon: int | None = None) -> set[int]:
    """All displacements delta such that the packet is rigidly shifted by
    delta per generation at every generation up to the horizon."""
    horizon = horizon or 2 * width
    s0 = _packet(width, k, start)
    deltas: set[int] = set(range(width))
    s = s0
    for g in range(1, horizon + 1):
        s = step(rule, s, "ring")
        keep = set()
        for d in list(deltas):
            if all((s[i] == s0[(i - g * d) % width])
                   for i in range(width)):
                keep.add(d)
        deltas = keep
        if not deltas:
            break
    return deltas


def bus_reconstitution_failures(rule: int) -> int:
    """Number of (width, k, start, gen) cells where the rule fails to
    reconstitute a packet on the vacuum bus over the whole grid."""
    fails = 0
    for width, k in itertools.product(_WIDTHS, _PACKET_WIDTHS):
        for start in range(width):
            for gen in range(1, 2 * width + 1):
                if not reconstitutes(rule, "bus", width, k, start, gen):
                    fails += 1
    return fails


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


def _rule204_bus_identity_holds() -> bool:
    return bus_reconstitution_failures(204) == 0


def _ring_lap_holds() -> bool:
    return all(lap_reconstitutes(rule, "ring", width, k, start)
               for rule in _ONE_LAP | _TWO_LAP
               for width in _WIDTHS
               for k in _PACKET_WIDTHS
               for start in range(width))


def _bus_lap_holds() -> bool:
    return all(lap_reconstitutes(rule, "bus", width, k, start)
               for rule in _ONE_LAP | _TWO_LAP
               for width in _WIDTHS
               for k in _PACKET_WIDTHS
               for start in range(width))


def _rigid_conveyor_holds() -> bool:
    """False candidate: a family rule other than the identity has a constant
    nonzero rigid displacement on the ring grid."""
    for rule in _RULE_TABLE:
        if rule == 204:
            continue
        for width in _WIDTHS:
            for k in _PACKET_WIDTHS:
                for start in range(width):
                    deltas = rigid_shift(rule, width, k, start)
                    if deltas and 0 not in deltas:
                        return True
    return False


def _unique_error_free_pair() -> set[int]:
    return {r for r in _RULE_TABLE if bus_reconstitution_failures(r) == 0}


def _storage_pair_holds() -> bool:
    return _unique_error_free_pair() == {204, 236}


def _block_storage_holds(rule: int = 236) -> bool:
    for width in _WIDTHS:
        for k in range(1, width + 1):
            for start in range(width - k + 1):
                s = _packet(width, k, start)
                target = _packet(width, k, start)
                for g in range(1, 2 * width + 1):
                    s = step(rule, s, "bus")
                    if s != target:
                        return False
    return True


def transport_certificates() -> list[dict[str, object]]:
    return [
        _certify("L_transport_rule204_bus_identity",
                 {"domain": "rule 204, vacuum-bus grid (widths 8/10/12, "
                            "packets 1..3 wide, every start offset, every "
                            "generation up to 2*width)",
                  "law": "rule 204 (f = center) stores every packet "
                         "bit-exact: zero reconstitution failures",
                  "measured_on": "full grid reconstitution sweep"},
                 _rule204_bus_identity_holds),
        _certify("L_transport_ring_lap_reconstitution",
                 {"domain": "one-lap {172,228} and two-lap {27,59,83,115} "
                            "rules on rings, full packet grid",
                  "law": "every packet reappears at its starting state "
                         "after width (resp. 2*width) ring generations",
                  "measured_on": "exact reconstitution at the lap "
                                 "generation, all offsets"},
                 _ring_lap_holds),
        _certify("L_transport_bus_lap_reconstitution",
                 {"domain": "the same lap claim transferred to the "
                            "ghost-zero bus",
                  "law": "the ring lap reconstitution holds unchanged on "
                         "the vacuum bus",
                  "measured_on": "exact reconstitution at the lap "
                                 "generation, all offsets"},
                 _bus_lap_holds),
        _certify("L_transport_rigid_conveyor",
                 {"domain": "all 32 family rules, ring packet grid",
                  "law": "FALSE CANDIDATE: a rule other than the identity "
                         "moves every packet as a rigid body with a "
                         "constant nonzero displacement per generation",
                  "honest_check": "period and lap structure measured in "
                                  "the state-space census does not imply "
                                  "per-generation rigid translation",
                  "measured_on": "per-generation shift set intersection "
                                 "over the full horizon"},
                 _rigid_conveyor_holds),
        _certify("L_transport_storage_pair_exact",
                 {"domain": "all 32 family rules, vacuum-bus grid",
                  "law": "the rules with zero reconstitution failures over "
                         "the whole bus grid are exactly {204, 236}",
                  "measured_on": "full bus-grid sweep of every rule"},
                 _storage_pair_holds),
        _certify("L_transport_rule236_block_storage",
                 {"domain": "rule 236 on the vacuum bus, widths 8/10/12, "
                            "every contiguous block width 1..n and every "
                            "interior offset, generations up to 2*width",
                  "law": "rule 236 stores every contiguous block exactly: "
                         "zero reconstitution failures even for arbitrary "
                         "block widths",
                  "measured_on": "full block grid sweep on the bus"},
                 _block_storage_holds),
    ]


def _render_failures() -> str:
    rows = ["  rule  bus failures"]
    for rule in sorted(_RULE_TABLE):
        rows.append("  %4d  %12d" % (rule, bus_reconstitution_failures(rule)))
    return "\n".join(rows)


if __name__ == "__main__":
    for c in transport_certificates():
        print("  %-44s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print(_render_failures())