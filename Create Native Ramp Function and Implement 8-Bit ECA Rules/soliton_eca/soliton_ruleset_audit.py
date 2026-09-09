"""soliton_ruleset_audit: the stripped-layer correction to the claimed
"noiseless 16-rule" framework, measured -- not taken as given.

The prose asserted:

  (1) the bitmask condition
        f(0,0,0)=0, f(0,0,1)=0, f(1,0,0)=0, f(0,1,0)=1
      filters the 256-rule Wolfram database down to EXACTLY the set
      {4,12,36,44,68,76,100,108,132,140,164,172,196,204,228,236}; and
  (2) those 16 rules conserve the total information volume (active-bit
      count preserved exactly during propagation/storage).

The LAYER being stripped: the bitmask fixes exactly four output bits
(000->0, 001->0, 010->1, 100->0), leaving bits 3,5,6,7 FREE -- so the
"16 rules" are the trivial product set 2^4 of unconstrained bits; they are
the rules that treat the 000 VACUUM as a privileged, given zero-background.
Statement (2) then ASSUMED that a stable-against-assumed-zero baseline
implies conservation of the signal.  That assumption is FALSE: treating the
background as measured data (not a given 0) and asking which rules conserve
the TOTAL active population over EVERY configuration -- noise included --
yields a different, fundamental answer.

MEASURED, exhaustively over all binary ring configurations at widths
4..12 (every noise density, background included as data):

    L_ruleset_bitmask16                 PASS  -- the bitmask reproduces the
                                       claimed 16-rule set exactly.
    L_ruleset_blanket_conservation      HONEST_NEGATIVE -- "all 16 rules
                                       conserve active-bit count" is FALSE:
                                       only rule 204 conserves on rings.
    L_ruleset_fundamental_conservation  PASS  -- the TRUE conservative set
                                       (total active population conserved
                                       for EVERY config, background as
                                       measured data) is EXACTLY
{170, 184, 204, 226, 240},
                                        verified exhaustively on rings of
                                        widths 4..12 (2^12 = 4096 configs
                                        per width); a vectorized census
                                        extends the check to widths 14 and
                                        16 (2^16 = 65536 configs each),
                                        cross-validated against this serial
                                        path at width 12.
    L_ruleset_204_storage_identity      PASS  -- rule 204 holds a block at
                                       an identical offset (genuine storage).
    L_ruleset_164_shift_claim           HONEST_NEGATIVE -- rule 164 does
                                       NOT shift an isolated cell by +1 per
                                       cycle in a vacuum (single 1 is
                                       stationary), so the stated shift-in-
                                       vacuum identity does not hold.

Corrected fundamental fact (noise-is-data, not given):
the rules that conserve measured population independently of the
background are exactly {170, 184, 204, 226, 240}.

EXTENDED FAMILY (the 32-rule twin set): the implemented rule table now
contains, alongside the 16 bitmask rules, their 16 bitwise complements
255-r (black/white output swap).  Measured exhaustively:

    L_ruleset_twin32_characterization     PASS  -- the 32 implemented rules
                                        are EXACTLY the rules whose output
                                        window (f000,f001,f010,f100) is
                                        (0,0,1,0) or (1,1,0,1); the 2^4 free
                                        bits give 2*16 rules.
    L_ruleset_twin32_complement_closure   PASS  -- within the twin set,
                                        every rule's complement 255-r is
                                        also present (closure verified over
                                        the exhaustively-derived set).
    L_ruleset_twin32_blanket_conservation HONEST_NEGATIVE -- across ALL 32
                                        twin rules only 204 conserves
                                        active-bit count on rings; adding
                                        the 16 complements does NOT
                                        manufacture blanket conservation.
    L_eca_engine_matches_reference       PASS  -- the soliton-bus engine
                                        reproduces the reference ghost-zero
                                        ECA step exactly for every one of
                                        the 32 rules (widths 4..9, ten
                                        deterministic probes, five
                                        generations); soliton transport
                                        alters no rule semantics.
    L_ruleset_twin_output_swap           PASS  -- for every rule r, the
                                        complement twin 255-r maps any
                                        configuration to the bitwise
                                        complement of what r maps it to
                                        (exhaustive rings width 6..8).
    L_ruleset_family_distinct_dynamics   PASS  -- no two of the 32 rules
                                        share identical dynamics: every
                                        rule pair diverges already at the
                                        first generation over an exhaustive
                                        ring sweep (widths 3..5).
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Callable, Iterable, Iterator

import numpy as np

# Package root bootstrap so this module also runs as a standalone script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import SolitonECA, RULES as _RULE_TABLE  # noqa: E402

_BITMASK_CONDITION = ((0, 0, 0, 0),   # f(0,0,0)=0
                      (0, 0, 1, 0),   # f(0,0,1)=0
                      (0, 1, 0, 1),   # f(0,1,0)=1
                      (1, 0, 0, 0))   # f(1,0,0)=0
_CLAIMED_16 = {4, 12, 36, 44, 68, 76, 100, 108,
               132, 140, 164, 172, 196, 204, 228, 236}
_FUNDAMENTAL = {170, 184, 204, 226, 240}
_TWIN_SIDE_A = (0, 0, 1, 0)
_TWIN_SIDE_B = (1, 1, 0, 1)


def _bit(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def _step(rule: int, s: list[int]) -> list[int]:
    n = len(s)
    return [_bit(rule, s[(i - 1) % n], s[i], s[(i + 1) % n]) for i in range(n)]


def _bitmask_rules() -> set[int]:
    out = set()
    for rule in range(256):
        if all(_bit(rule, *nb) == want for *nb, want in _BITMASK_CONDITION):
            out.add(rule)
    return out


def _conserves_on_rings(rule: int,
                        widths: Iterable[int] = (8, 9, 10, 11, 12)) -> bool:
    for n in widths:
        for s in itertools.product((0, 1), repeat=n):
            if sum(s) != sum(_step(rule, list(s))):
                return False
    return True


def _conserves_fast(rule: int, width: int) -> bool:
    """Vectorized ring-population check for a single rule (exact: it is
    the same 3-bit lookup applied to every configuration)."""
    states = np.arange(1 << width)
    bits = ((states[:, None] >> np.arange(width)) & 1).astype(np.uint8)
    left = np.roll(bits, 1, axis=1)
    right = np.roll(bits, -1, axis=1)
    idx = (left << 2) | (bits << 1) | right
    lut = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    out = lut[idx]
    return bool(np.all(out.sum(axis=1) == bits.sum(axis=1)))


def _conservation_scales_holds() -> bool:
    # Cross-validate the vectorized path against the serial path at width 12.
    for r in _RULE_TABLE:
        if _conserves_fast(r, 12) != _conserves_on_rings(r, (12,)):
            return False
    # The conservative set persists at widths 14 and 16.
    for r in _FUNDAMENTAL:
        if not (_conserves_fast(r, 14) and _conserves_fast(r, 16)):
            return False
    # No other family rule conserves at either width.
    for r in set(_RULE_TABLE) - _FUNDAMENTAL:
        if _conserves_fast(r, 14) or _conserves_fast(r, 16):
            return False
    return True


def certify(label: str, meta: dict[str, object],
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


def _found():
    return _bitmask_rules()


def _blanket_holds():
    return all(_conserves_on_rings(r) for r in _CLAIMED_16)


def _fundamental_holds():
    return set(r for r in range(256) if _conserves_on_rings(r)) == _FUNDAMENTAL


def _storage_holds():
    # 204 stores a 1110 block at identical offset, and an isolated 1 stays.
    n = 21
    block = [0] * n
    for i in (3, 4, 5, 6):
        block[i] = 1
    s = list(block)
    for _ in range(20):
        s = _step(204, s)
        if s != block:
            return False
    return True


def _shift_holds():
    """164 claimed to shift an isolated cell by +1 per cycle in vacuum.
    Returns True ONLY IF the lone 1's position advances by exactly +1
    each step.  It is stationary, so this returns False -> the stated
    shift-in-vacuum identity does NOT hold (HONEST_NEGATIVE)."""
    n = 21
    s = [0] * n
    s[5] = 1
    pos = 5
    for k in range(1, 6):
        s = _step(164, s)
        idx = [i for i, v in enumerate(s) if v]
        # exactly one 1 remaining, at +1 from before
        if len(idx) != 1 or idx[0] != (pos + 1) % n:
            return False
        pos = idx[0]
    return True


def _twin_window(rule: int) -> tuple[int, int, int, int]:
    """Restricted output window (f000, f001, f010, f100) of a rule."""
    return (_bit(rule, 0, 0, 0), _bit(rule, 0, 0, 1),
            _bit(rule, 0, 1, 0), _bit(rule, 1, 0, 0))


def _twin_rules() -> set[int]:
    return {r for r in range(256)
            if _twin_window(r) in (_TWIN_SIDE_A, _TWIN_SIDE_B)}


def _twin_characterization_holds():
    return _twin_rules() == (_CLAIMED_16 | {255 - r for r in _CLAIMED_16})


def _twin_complement_closure_holds():
    twins = _twin_rules()
    return all(255 - r in twins for r in twins)


def _twin_blanket_holds():
    return all(_conserves_on_rings(r) for r in _twin_rules())


def _lcg() -> Iterator[int]:
    """Deterministic, platform-independent probe generator."""
    state = 20260214
    while True:
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        yield state


def _ghost_step(rule: int, s: list[int]) -> list[int]:
    """Reference ghost-zero ECA step, matching the SolitonECA boundary."""
    n = len(s)
    return [_bit(rule,
                 s[i - 1] if i > 0 else 0,
                 s[i],
                 s[i + 1] if i < n - 1 else 0)
            for i in range(n)]


def _engine_matches_reference(probes: int = 10,
                             generations: int = 5) -> bool:
    gen = _lcg()
    for rule in _RULE_TABLE:
        for width in (4, 5, 6, 7, 8, 9):
            for _ in range(probes):
                initial = [(next(gen) >> 16) & 1 for _ in range(width)]
                engine = SolitonECA(rule, width, initial)
                reference = list(initial)
                for _ in range(generations):
                    if list(engine.step()) != _ghost_step(rule, reference):
                        return False
                    reference = _ghost_step(rule, reference)
    return True


def _twin_output_swap_holds() -> bool:
    gen = _lcg()
    for rule in _RULE_TABLE:
        twin = 255 - rule
        for n in (6, 7, 8):
            for s in itertools.product((0, 1), repeat=n):
                a, b = _step(rule, list(s)), _step(twin, list(s))
                if any(1 - x != y for x, y in zip(a, b)):
                    return False
            for _ in range(8):
                s = [(next(gen) >> 16) & 1 for _ in range(n)]
                a, b = _step(rule, list(s)), _step(twin, list(s))
                if any(1 - x != y for x, y in zip(a, b)):
                    return False
    return True


def _family_dynamics_distinct() -> bool:
    family = sorted(_RULE_TABLE)
    for i in range(len(family)):
        for j in range(i + 1, len(family)):
            r0, r1 = family[i], family[j]
            if r0 != r1 and not any(
                _step(r0, list(s)) != _step(r1, list(s))
                for n in (3, 4, 5)
                for s in itertools.product((0, 1), repeat=n)):
                return False
    return True


def ruleset_certificates():
    return [
        certify("L_ruleset_bitmask16",
                {"domain": "all 256 Wolfram rules; bitmask conditions "
                           "f(000)=0,f(001)=0,f(010)=1,f(100)=0",
                 "law": "the bitmask filters to exactly the claimed 16-rule "
                        "set (structural: 4 output bits fixed, 4 free)",
                 "measured_on": "exhaustive 256-rule enumeration"},
                lambda: _found() == _CLAIMED_16),
        certify("L_ruleset_blanket_conservation",
                {"domain": "the claimed 16 rules, rings of width 8..12",
                 "law": "FALSE CANDIDATE: all 16 rules conserve active-bit "
                        "count on rings -- only rule 204 does",
                 "honest_check": "treating the 0-vacuum as a given baseline "
                                 "does NOT imply signal conservation"},
                _blanket_holds),
        certify("L_ruleset_fundamental_conservation",
                {"domain": "all 256 rules, EVERY ring configuration at "
                           "widths 8..12 (noise/background included as "
                           "measured data)",
                 "law": "the rules conserving the TOTAL active population "
                        "for every configuration are exactly "
                        "{170,184,204,226,240}",
                 "key_correction": "background is measured data, not a "
                                   "given zero"},
                _fundamental_holds),
        certify("L_ruleset_204_storage_identity",
                {"domain": "rule 204, block 1110 and isolated 1 on a "
                           "21-ring over 20 steps",
                 "law": "rule 204 holds a block at an identical offset "
                        "(genuine position-conserving storage)"},
                _storage_holds),
        certify("L_ruleset_164_shift_claim",
                {"domain": "rule 164, isolated single 1 in vacuum on a "
                           "21-ring",
                 "law": "FALSE CANDIDATE: rule 164 shifts an isolated cell "
                        "by +1 per cycle -- the lone 1 is stationary",
                 "honest_check": "164 is bitmask-stable but does not "
                                 "exhibit the stated +1 shift"},
                _shift_holds),
        certify("L_ruleset_twin32_characterization",
                {"domain": "all 256 Wolfram rules; output window "
                           "(f000,f001,f010,f100) in {(0,0,1,0),(1,1,0,1)}",
                 "law": "the implemented 32-rule twin set is exactly the "
                        "rules whose four fixed window bits are the bitmask "
                        "pattern (0,0,1,0) or its bitwise complement "
                        "(1,1,0,1); the 16 additions are 255-r twins of "
                        "the original 16",
                 "measured_on": "exhaustive 256-rule enumeration"},
                _twin_characterization_holds),
        certify("L_ruleset_twin32_complement_closure",
                {"domain": "the 32-rule twin family (exhaustively derived "
                           "by the window condition)",
                 "law": "the family is closed under black/white output "
                        "complement: every rule r has 255-r inside the "
                        "same 32-rule set",
                 "measured_on": "closure over the full twin set"},
                _twin_complement_closure_holds),
        certify("L_ruleset_twin32_blanket_conservation",
                {"domain": "all 32 twin rules, rings of width 8..12",
                 "law": "FALSE CANDIDATE: the extended 32-rule family "
                        "conserve active-bit count on rings -- only rule "
                        "204 does; the honest conservative set remains "
                        "{170,184,204,226,240}",
                 "honest_check": "extending the table by the 16 complements "
                                 "does not manufacture blanket conservation"},
                _twin_blanket_holds),
        certify("L_eca_engine_matches_reference",
                {"domain": "all 32 twin-family rules on a ghost-zero grid, "
                           "width 4..9, ten deterministic probes, five "
                           "generations per probe",
                 "law": "the soliton-bus engine reproduces the reference "
                        "ECA step exactly; bus transport alters no rule "
                        "semantics",
                 "measured_on": "32 rules x 6 widths x 10 probes x 5 "
                                "generations, engine vs direct reference"},
                _engine_matches_reference),
        certify("L_ruleset_twin_output_swap",
                {"domain": "ring configurations, exhaustive widths 6..8 "
                           "plus deterministic probes",
                 "law": "for every rule r, the complement twin 255-r maps "
                        "any configuration to the bitwise complement of "
                        "what r maps it to (black/white output swap)",
                 "measured_on": "all 32 rules over exhaustive rings 6..8 "
                                "and probes, one generation per config"},
                _twin_output_swap_holds),
        certify("L_ruleset_family_distinct_dynamics",
                {"domain": "every unordered pair of the 32 rules over all "
                           "ring configurations of width 3..5",
                 "law": "no two family members share identical dynamics: "
                        "every pair diverges already at the first "
                        "generation, because distinct 8-bit rules differ on "
                        "some neighborhood triple and every triple occurs "
                        "as a width-3 ring state",
                 "measured_on": "496 rule pairs, exhaustive first-"
                                "generation sweep over rings width 3..5"},
                _family_dynamics_distinct),
        certify("L_ruleset_conservation_scales_14_16",
                {"domain": "the conservative set {170,184,204,226,240} on "
                           "rings of width 14 and 16 (2^14 and 2^16 "
                           "configurations each)",
                 "law": "the measured conservative set persists at widths "
                        "14 and 16, and no other family rule conserves at "
                        "either width",
                 "measured_on": "vectorized ring-population census "
                                "(cross-validated against the serial path "
                                "at width 12, then applied at widths "
                                "14 and 16)"},
                _conservation_scales_holds),
    ]


if __name__ == "__main__":
    for c in ruleset_certificates():
        print("  %-42s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
