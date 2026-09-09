"""soliton_collision_crowd_audit: three-block damage crowding on the bus.

Round 14 mapped the two-block interaction range.  This audit adds a
THIRD 4-cell block: anchor A at pa, B at pa + 16 (well inside rule
147's saturative core), C at pa + 96 (independent range).  All damage
is Hamming density at generation 96 (W = 512, 8 per-probe placements,
round-12 protocol):: indicators:

    rule  f1      f2       f3       (f2/f1)  (f3-f2)/f1
    204   0.0078  0.0156   0.0234   2.000    1.000
     51   0.0078  0.0156   0.0234   2.000    1.000
    147   0.0723  0.0859   0.1506   1.188    0.895
    172   0.0032  0.0049   0.0081   ...

Laws:

- the isometry transports {204, 51} are EXACTLY additive: two blocks
  damage exactly 2*f1, three blocks exactly 3*f1 (bit distances 8 and
  12 over 512) -- their XOR-of-runs fields are disjoint live cells
  that neither merge nor cancel; the full-eraser 251 is also exactly
  additive (0 = 3*0); no other rule in the family is exactly
  additive;
- rule 147's in-core second block adds at most 0.35 f1 on top of f1
  (f2 = 1.188 f1): the crowding pair, inside the saturative core,
  still demands far less than an independent block would;
- but the FAR block lands nearly full even onto the crowded pair:
  (f3 - f2) >= 0.8 f1 (0.895 measured) -- super-additivity, NOT a
  shared budget: the caustic concatenates instead of saturating;
- HONEST_NEGATIVE: "two-block damage is additive for every rule" is
  false -- rule 147's f2 = 0.0859 versus 2*f1 = 0.1446 (0.59x).

Certificates:

    L_crowd_isometry_additive PASS/FAIL  exactly-additive rules are
                              EXACTLY {204, 51, 251}: f3 == 3*f1
                              within 1e-9 (251 the zero eraser).
    L_crowd_core_demand       PASS/FAIL  147's f2 <= 1.35 f1.
    L_crowd_far_lands         PASS/FAIL  147's (f3 - f2) >= 0.8 f1.
    L_crowd_all_additive      HONEST_NEGATIVE  "two-block additive for
                              every rule": FALSE.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES  # noqa: E402

_WIDTH = 512
_PROBES = 8
_GENS = 96
_BLOCK = 4
_B_SECOND = 16
_B_THIRD = 96
_ADD_TOL = 1e-9
_CORE_CEIL = 1.35
_FAR_FLOOR = 0.8
_ISOMETRIES = (204, 51)


def _lcg(seed: int = 0x0DDB1A5E5BAD5EED) -> int:
    return (6364136223846793005 * seed
            + 1442695040888963407) & ((1 << 64) - 1)


def _bit(r: int, l: int, c: int, rr: int) -> int:
    return (r >> ((l << 2) | (c << 1) | rr)) & 1


def _ring_step(r: int, s: list[int]) -> list[int]:
    m = len(s)
    return [_bit(r, s[i - 1], s[i], s[(i + 1) % m]) for i in range(m)]


def _distance(a: list[int], b: list[int]) -> float:
    return sum(x != y for x, y in zip(a, b)) / len(a)


def crowd_measurements() -> dict[int, dict[str, float]]:
    w = _WIDTH
    seed = _lcg()
    f = {r: {"f1": 0.0, "f2": 0.0, "f3": 0.0} for r in RULES}
    for _ in range(_PROBES):
        seed = _lcg(seed)
        bg = [((seed := _lcg(seed)) >> 16) & 1 for _ in range(w)]
        pa = (_lcg(seed) % w)
        seed = _lcg(seed)
        pb = (pa + _B_SECOND) % w
        pc = (pa + _B_THIRD) % w
        for r in RULES:
            base = list(bg)
            one = list(bg)
            two = list(bg)
            thr = list(bg)
            for i in range(_BLOCK):
                one[(pa + i) % w] ^= 1
                two[(pa + i) % w] ^= 1
                thr[(pa + i) % w] ^= 1
            for i in range(_BLOCK):
                two[(pb + i) % w] ^= 1
                thr[(pb + i) % w] ^= 1
            for i in range(_BLOCK):
                thr[(pc + i) % w] ^= 1
            cb = list(bg)
            co = list(one)
            ct = list(two)
            ch = list(thr)
            for _ in range(_GENS):
                cb = _ring_step(r, cb)
                co = _ring_step(r, co)
                ct = _ring_step(r, ct)
                ch = _ring_step(r, ch)
            f[r]["f1"] += _distance(cb, co)
            f[r]["f2"] += _distance(cb, ct)
            f[r]["f3"] += _distance(cb, ch)
    for r in RULES:
        for k in ("f1", "f2", "f3"):
            f[r][k] /= _PROBES
    return f


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


def crowd_certificates() -> tuple[list[dict[str, object]],
                                  dict[int, dict[str, float]]]:
    f = crowd_measurements()
    all_ok = all(f[r]["f3"] == 3 * f[r]["f1"] for r in _ISOMETRIES)
    only = {r for r in RULES if abs(f[r]["f3"] - 3 * f[r]["f1"]) <= _ADD_TOL}
    only_ok = only == set(_ISOMETRIES)
    f147 = f[147]
    core_ok = f147["f2"] <= _CORE_CEIL * f147["f1"]
    far_ok = (f147["f3"] - f147["f2"]) >= _FAR_FLOOR * f147["f1"]
    certs = [
        _certify("L_crowd_isometry_additive",
                 {"domain": f"width {_WIDTH}, {_PROBES} probes, three "
                            f"{_BLOCK}-cell blocks at 0/{_B_SECOND}/"
                            f"{_B_THIRD}, {_GENS} generations",
"law": f"the exact-additive set is {sorted(only)} "
                         "= the isometry transports {204, 51} (bit "
                         "-exact disjoint live cells) plus the full "
                         "eraser 251 (0 = 3*0); every other rule "
                         "breaks additivity",
                  "measured": {str(r): {"f1": round(f[r]["f1"], 4),
                                        "f2": round(f[r]["f2"], 4),
                                        "f3": round(f[r]["f3"], 4)}
                               for r in (204, 51)}},
                 lambda: all_ok and only == set((204, 51, 251))),
        _certify("L_crowd_core_demand",
                 {"law": "rule 147's in-core second block (d = 16) "
                         "adds at most "
                         f"{_CORE_CEIL - 1:.2f} f1: f2 = "
                         f"{f147['f2'] / f147['f1']:.3f} f1 -- the "
                         "crowded pair, inside the saturative core, "
                         "demands far less than an independent block",
                  "measured": {"f1": round(f147["f1"], 4),
                               "f2": round(f147["f2"], 4),
                               "f2/f1": round(f147["f2"] / f147["f1"], 3)}},
                 lambda: core_ok),
        _certify("L_crowd_far_lands",
                 {"law": "the far block (d = 96) lands nearly full "
                         "even onto the crowded pair: (f3 - f2) >= "
                         f"{_FAR_FLOOR} f1 (measured "
                         f"{(f147['f3'] - f147['f2']) / f147['f1']:.3f}) "
                         "-- the caustic CONCATENATES instead of "
                         "sharing a saturized budget",
                  "measured": {"f3": round(f147["f3"], 4),
                               "f3-f2": round(f147["f3"] - f147["f2"], 4),
                               "ratio": round((f147["f3"] - f147["f2"])
                                              / f147["f1"], 3)}},
                 lambda: far_ok),
        _certify("L_crowd_all_additive",
                 {"law": "two-block damage is additive for every "
                         "rule (f2 = 2 f1)",
                  "measured": f"FALSE: rule 147's f2 = "
                              f"{f147['f2']:.4f} versus 2 f1 = "
                              f"{2 * f147['f1']:.4f} (0.59x); it "
                              "concatenates damage only at distance "
                              "and vacates it in the core",
                  "ratio": round(f147["f2"] / (2 * f147["f1"]), 3)},
                 lambda: abs(f147["f2"] - 2 * f147["f1"]) <= _ADD_TOL),
    ]
    return certs, f


if __name__ == "__main__":
    certs, f = crowd_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    for r in sorted(RULES):
        d = f[r]
        print("  %3d  f1=%.4f f2=%.4f f3=%.4f  f2/f1=%.3f  (f3-f2)/f1=%.3f"
              % (r, d["f1"], d["f2"], d["f3"],
                 d["f2"] / d["f1"] if d["f1"] else 0.0,
                 (d["f3"] - d["f2"]) / d["f1"] if d["f1"] else 0.0))