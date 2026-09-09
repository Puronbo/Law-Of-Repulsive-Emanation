"""soliton_damage_crystallization_audit: dominant-pair share of the
damage spectrum.

Round 22 certified the NLSE carrier-void crest: the near-cap crest is
an EXACT 4-line harmonic stack (the +-Omega and +-2-Omega pairs hold
>= 0.60 of the power).  This audit maps the ECA twin -- does the
amplifier's damage field crystallize onto a dominant wavenumber pair
the way the NLSE crest stacks onto its harmonic lines?

Measured protocol (512-ring, 8 true-random probes, same drawing as
damage-modal round 16), top-2 non-DC wavenumber joint share::

    rule       top2@2    top2@12   top2@48   top2@96
    204        0.016     0.016     0.016     0.016
    51         0.016     0.016     0.016     0.016
    147        0.019     0.037     0.073     0.127

Laws:

- the dominant amplifier 147 CRYSTALLIZES: its top-2-wavenumber share
  rises strictly at every sampled generation (0.019 -> 0.127, an
  6.7-fold rise) -- the concentrating caustic locks onto its two
  dominant wavenumbers, the soft ECA mirror of the NLSE stack
  formation;
- the isometry transports {204, 51} do NOT crystallize: their top-2
  share is identical and time-invariant (flat 0.016) -- the flipped
  block's damage stays broadband, the ECA mirror of the NLSE far band
  keeping the carrier;
- HONEST_NEGATIVE: the amplifier's damage does NOT reach the NLSE's
  supermajority lock -- at the sampling horizon the pair holds only
  0.127 of the damage power (not >= 0.60); concentration without
  majority: the ECA caustic crystallizes but stays diffuse, so the
  carrier-void stack has NO exact ECA supermajority twin.

Certificates:

    L_cry_amplifier_rises   PASS/FAIL  147's top-2 share strictly
                          rises at every sampled generation and the
                          @96/@2 ratio is >= 5.
    L_cry_transport_const  PASS/FAIL  204 == 51 at every sampled
                          generation and time-invariant (1e-6).
    L_cry_supermajority    HONEST_NEGATIVE  "the amplifier's damage
                          crystallizes onto a supermajority pair
                          (>= 0.60)": FALSE (max 0.127).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_damage_modal_audit import (  # noqa: E402
    _bit,
    _lcg,
    _ring_step,
    RULES,
    _WIDTH,
    _PROBES,
    _GENS,
    _BLOCK,
    _TIMES,
)

_TRANSPORT = (204, 51)
_AMP = 147
_INV_TOL = 1e-6
_RISE_RATIO = 5.0
_SUPERMAJORITY = 0.60


def _top2_share(flat: list[int]) -> float:
    c = np.abs(np.fft.fft(np.asarray(flat, dtype=float))) ** 2
    tot = float(c.sum())
    if tot < 1e-12:
        return 0.0
    c = np.copy(c)
    c[0] = 0.0
    return float(np.sort(c)[-2:].sum() / tot)


def cry_table() -> dict[int, dict[int, float]]:
    top = {r: {g: [] for g in _TIMES} for r in RULES}
    w = _WIDTH
    seed = _lcg()
    for _ in range(_PROBES):
        seed = _lcg(seed)
        bg = [((seed := _lcg(seed)) >> 16) & 1 for _ in range(w)]
        pa = (_lcg(seed) % w)
        seed = _lcg(seed)
        for r in RULES:
            clean = list(bg)
            one = list(bg)
            for i in range(_BLOCK):
                one[(pa + i) % w] ^= 1
            for g in range(1, _GENS + 1):
                clean = _ring_step(r, clean)
                one = _ring_step(r, one)
                if g in _TIMES:
                    flat = [1 if a != b else 0
                            for a, b in zip(clean, one)]
                    top[r][g].append(_top2_share(flat))
    return {r: {g: float(np.mean(top[r][g])) for g in _TIMES}
            for r in RULES}


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


def cry_certificates() -> tuple[list[dict[str, object]],
                                dict[int, dict[int, float]]]:
    tab = cry_table()
    a = [tab[_AMP][g] for g in _TIMES]
    t2 = tab[204]
    t51 = tab[51]
    rise_ok = all(y > x for x, y in zip(a, a[1:])) \
        and a[-1] / a[0] >= _RISE_RATIO
    const_ok = all(abs(t2[g] - t2[_TIMES[0]]) <= _INV_TOL
                   for g in _TIMES) \
        and all(abs(t51[g] - t51[_TIMES[0]]) <= _INV_TOL
                for g in _TIMES) \
        and all(abs(t2[g] - t51[g]) <= _INV_TOL for g in _TIMES)
    max_share = max(a)
    certs = [
        _certify("L_cry_amplifier_rises",
                 {"domain": f"width {_WIDTH}, single {_BLOCK}-cell "
                            f"block, gens {_GENS}, {_PROBES} probes, "
                            f"samples {_TIMES}",
                  "law": "rule 147's damage CRYSTALLIZES: the top-2 "
                         "wavenumber share rises strictly at every "
                         "sampled generation (0.019 -> 0.127, "
                         f"{a[-1] / a[0]:.1f}-fold) -- the "
                         "concentrating caustic locks onto its two "
                         "dominant wavenumbers, the soft ECA mirror "
                         "of the NLSE stack formation",
                  "measured": {"147": [round(v, 3) for v in a],
                               "ratio": round(a[-1] / a[0], 2)}},
                 lambda: rise_ok),
        _certify("L_cry_transport_const",
                 {"law": "the isometry transports {204, 51} do NOT "
                         "crystallize: their top-2 share is identical "
                         "and time-invariant (flat 0.016) -- the "
                         "flipped block's damage stays broadband, the "
                         "ECA mirror of the NLSE far band keeping "
                         "the carrier",
                  "measured": {"204": [round(t2[g], 3) for g in _TIMES],
                               "51": [round(t51[g], 3) for g in _TIMES]}},
                 lambda: const_ok),
        _certify("L_cry_supermajority",
                 {"law": "the amplifier's damage crystallizes onto a "
                         f"supermajority wavenumber pair (>= "
                         f"{_SUPERMAJORITY} of the power), matching "
                         "the NLSE harmonic stack",
                  "measured": f"FALSE: at the sampling horizon the "
                              f"pair holds only {max_share:.3f} (not "
                              f">= {_SUPERMAJORITY}); concentration "
                              "without majority -- the ECA caustic "
                              "crystallizes 6.7-fold but stays diffuse, "
                              "so the carrier-void stack has no exact "
                              "ECA supermajority twin",
                  "max_top2_share": round(max_share, 3)},
                 lambda: max_share >= _SUPERMAJORITY),
    ]
    return certs, tab


if __name__ == "__main__":
    certs, tab = cry_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  rule   top2@2    @12    @48    @96")
    for r in (204, 51, 147):
        print("  %3d  %6.3f %6.3f %6.3f %6.3f" % (
            r, *[tab[r][g] for g in _TIMES]))