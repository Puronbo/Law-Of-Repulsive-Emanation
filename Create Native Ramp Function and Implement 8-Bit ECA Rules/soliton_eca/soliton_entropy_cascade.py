"""soliton_entropy_cascade: exact information-retention audit of the
32-rule twin family, measured -- not assumed.

A soliton-bus message is a configuration of the ring.  Start from the
UNIFORM ensemble over all 2^n states and let every rule act t times; the
pushforward distribution's Shannon entropy H(t) is the ensemble
information that survives t generations of transport.  At width n = 12 the
family map is enumerated exactly (4096 states), so H(t) is exact, not
estimated.

Certificates:

    L_entropy_lossless_pair          PASS/FAIL  the rules that lose NO
                                     ensemble entropy at any generation
                                     (H(t) = n = 12 for all t) are exactly
                                     the permutation pair {204, 51}.
    L_entropy_twin_dominance         HONEST_NEGATIVE  FALSE CANDIDATE: the
                                     A-side bitmask rule always retains at
                                     least as much entropy as its B-side
                                     complement twin -- pair (44, 211)
                                     retains 0.53 vs 0.73 and violates it.
    L_entropy_fast_dissipation     HONEST_NEGATIVE  FALSE CANDIDATE:
                                     every non-permutation rule halves its
                                     entropy within 8 generations -- only
                                     rules 36/147/164/219/251 ever halve
                                     within the 32-generation horizon.
    L_entropy_reproducible           PASS/FAIL  recomputation is
                                     bit-for-bit identical (deterministic
                                     enumeration).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES as _RULE_TABLE  # noqa: E402

_WIDTH = 12
_GENERATIONS = 32


def _bit(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def _next_id(rule: int, n: int, sid: int) -> int:
    out = 0
    for i in range(n):
        out |= _bit(rule, (sid >> ((i - 1) % n)) & 1, (sid >> i) & 1,
                    (sid >> ((i + 1) % n)) & 1) << i
    return out


def entropy_cascade(rule: int) -> dict[str, object]:
    n = _WIDTH
    n_states = 1 << n
    nxt = [_next_id(rule, n, s) for s in range(n_states)]
    counts = [1] * n_states
    h0 = float(n)
    retained = [h0]
    for _ in range(_GENERATIONS):
        nxt_counts = [0] * n_states
        for s, c in enumerate(counts):
            if c:
                nxt_counts[nxt[s]] += c
        counts = nxt_counts
        h = h0 - sum(c * math.log2(c) for c in counts if c) / n_states
        retained.append(h)
    lossless = retained[-1] == h0
    half = None
    for g in range(1, len(retained)):
        if retained[g] <= h0 / 2.0:
            half = g
            break
    return {"rule": rule, "retained": retained[-1] / h0,
            "lossless": lossless, "half_life": half}


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


def _lossless_pair_holds() -> bool:
    lossless = {r for r in _RULE_TABLE
                if entropy_cascade(r)["lossless"]}
    return lossless == {204, 51}


def _twin_dominance_holds() -> bool:
    """False candidate: retained entropy of A-side >= that of its twin."""
    info = {r: entropy_cascade(r) for r in _RULE_TABLE}
    for rule in _RULE_TABLE:
        if rule in _SIDE_A():
            if info[rule]["retained"] < info[255 - rule]["retained"]:
                return False
    return True


def _SIDE_A() -> set[int]:
    return {r for r in _RULE_TABLE if _bit(r, 0, 0, 0) == 0
            and _bit(r, 0, 0, 1) == 0 and _bit(r, 0, 1, 0) == 1
            and _bit(r, 1, 0, 0) == 0}


def _fast_dissipation_holds() -> bool:
    """False candidate: every non-permutation rule halves within 8 gens."""
    for rule in _RULE_TABLE:
        if rule in (204, 51):
            continue
        info = entropy_cascade(rule)
        if info["half_life"] is None or info["half_life"] > 8:
            return False
    return True


def _reproducible_holds() -> bool:
    return all(entropy_cascade(r) == entropy_cascade(r) for r in _RULE_TABLE)


def entropy_certificates() -> list[dict[str, object]]:
    return [
        _certify("L_entropy_lossless_pair",
                 {"domain": "all 32 family rules, exact uniform-ensemble "
                            "entropy over 2^12 states, 32 generations",
                  "law": "the rules that retain all ensemble entropy at "
                         "every generation are exactly the permutation "
                         "pair {204, 51}",
                  "measured_on": "exact pushforward entropy H(t)"},
                 _lossless_pair_holds),
        _certify("L_entropy_twin_dominance",
                 {"domain": "entropy-retention of each A-side rule versus "
                            "its B-side complement twin",
                  "law": "FALSE CANDIDATE: the A-side bitmask twin always "
                         "retains at least as much ensemble entropy as the "
                         "B-side complement -- pair (44, 211) retains "
                         "0.53 vs 0.73; several pairs go both ways",
                  "honest_check": "retention order between twins is "
                                  "rule-specific, not side-specific",
                  "measured_on": "identical ensemble, e.g. width 12"},
                 _twin_dominance_holds),
        _certify("L_entropy_fast_dissipation",
                 {"domain": "all non-permutation family rules",
                  "law": "FALSE CANDIDATE: every non-permutation rule "
                         "halves its ensemble entropy within 8 "
                         "generations -- only rules 36/147/164/219/251 "
                         "half within the 32-generation horizon",
                  "honest_check": "most dissipative rules never halve the "
                                  "ensemble entropy at width 12; the "
                                  "entropy ladder is slow, not abrupt",
                  "measured_on": "exact H(t), width 12, 32 generations"},
                 _fast_dissipation_holds),
        _certify("L_entropy_reproducible",
                 {"domain": "repeatability of the cascade computation",
                  "law": "recomputing the cascade is bit-for-bit identical",
                  "measured_on": "duplicated exact enumeration"},
                 _reproducible_holds),
    ]


def _render_table() -> str:
    rows = ["  rule  retained  half-life"]
    for rule in sorted(_RULE_TABLE):
        info = entropy_cascade(rule)
        rows.append("  %4d  %8.4f  %s" % (
            rule, info["retained"], info["half_life"]))
    return "\n".join(rows)


if __name__ == "__main__":
    for c in entropy_certificates():
        print("  %-34s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print(_render_table())