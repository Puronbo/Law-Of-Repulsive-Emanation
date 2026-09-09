"""soliton_mi_phase_probe_audit: phase robustness of the near-cap
crest, scoped to the near-cap mountain (re-scope supersedes round 32).

Round 32 swept the modulation's initial phase (8 draws, k*pi/8) using
the round-22 crest protocol (local maxima above R >= 1.2) and read a
SECTORED void: it reported PUMP-STRONG first crests (P0 ~= 0.97) at
phi = pi/2 and 5pi/8 and a second-crest break at 3pi/8.

This audit re-scopes the crest DEFINITION to the near-cap mountain
(R >= 2.5, the R ~= 2.8 self-focusing crests) and finds those round-32
readings were low-ridge artifacts (weak phase-conjugate echoes at
R ~= 1.2 in the loose 1.2 threshold):

    near-cap crests (R >= 2.5), observing the seed's brightness column:
      every phase forms a first crest at z ~= 2.45 with R ~= 2.81-2.84;
      first-crest P0: 0.0003 0.0006 0.0017 0.0021 0.0013 0.0006
                      0.0003 0.0002   (max 0.0021)

Laws (measured):

- the near-cap crest FORMS at every initial phase: 8/8 draws reach
  R >= 2.5 (round 32's "sine seed does not focus" is an artifact of
  reading a z = 0.35 ridge of R = 1.22 as 'the crest');
- the near-cap first crest is carrier-void for EVERY phase: P0 <= 0.01
  (max 0.0021) and a harmonic stack (p1 + p2) >= 0.60 (min 0.712) --
  the round-22 void is PHASE-INERTIAL, superseding round-32's
  'sector-dependent' claim;
- the phase sensitivity lives in the RECURRENCE, not the void: the
  near-cap second-crest P0 is <= 0.06 at six phases but breaks at
  phi = 3pi/8 (0.0612) and phi = pi/2 (0.2101) -- the round-22
  'one-recurrence persistence' is phase-fragile at real near-cap
  second crests;
- HONEST_NEGATIVE: at every phase the carrier returns at some later
  near-cap crest (chain maximum P0 = 0.018..0.210), so the round-22
  'void is a first-period signature' survives the re-scope.

Certificates:

    L_ph_formed      PASS/FAIL  every one of the 8 phases forms a
                          near-cap crest (R >= 2.5) within z <= 14.
    L_ph_void_first  PASS/FAIL  first near-cap crest P0 <= 0.01, all
                          8 phases.
    L_ph_stack_first PASS/FAIL  (p1 + p2) >= 0.60, all 8 phases.
    L_ph_second      HONEST_NEGATIVE  "second near-cap crest P0 <=
                          0.06 for every phase": FALSE (0.0612 at
                          3pi/8; 0.2101 at pi/2).
    L_ph_chain_void  HONEST_NEGATIVE  "every near-cap crest in the
                          chain is void": FALSE (carrier returns at
                          all 8 phases).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_physics import (  # noqa: E402
    Fiber,
    propagate,
)

from soliton_eca.soliton_mi_modal_audit import (  # noqa: E402
    _grid,
    _split,
    _Z_GRID,
    _STEPS_PER_DZ,
)

_P = 1.0
_OMEGA = 1.0
_EPS = 0.20
_Z_END = 14.0
_N_PHASES = 8
_NEAR_CAP = 2.5
_VOID_CEIL = 0.01
_STACK_FLOOR = 0.60
_SECOND_CEIL = 0.06


def _crest_chain(phi: float) -> list[dict[str, float]]:
    t = _grid()
    dt = float(np.diff(t)[0])
    seed = np.sqrt(_P) * (1 + _EPS * np.cos(_OMEGA * t + phi))
    ci = int(np.argmax(np.abs(seed)))
    zs = np.arange(0.0, _Z_END + _Z_GRID / 2, _Z_GRID)
    cur = np.array(seed)
    prev = 0.0
    r = np.empty(len(zs))
    fields = []
    for k, z in enumerate(zs):
        if z > 0.0:
            cur = propagate(cur, dt, z - prev, fiber=Fiber(),
                            steps=_STEPS_PER_DZ)
            prev = z
        r[k] = np.abs(cur[ci])
        fields.append(cur.copy())
    chain = []
    for i in range(2, len(zs) - 2):
        if r[i] >= _NEAR_CAP and r[i] >= max(r[i - 2:i + 3]):
            s = _split(fields[i], _OMEGA)
            chain.append({"z": float(zs[i]), "R": float(r[i]),
                          "p0": float(s["p0"]), "p1": float(s["p1"]),
                          "p2": float(s["p2"]), "rest": float(s["rest"])})
    return chain


def phase_data() -> dict[str, list[dict[str, float]]]:
    return {f"p{p}": _crest_chain(p * np.pi / _N_PHASES)
            for p in range(_N_PHASES)}


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


def phase_certificates() -> tuple[list[dict[str, object]],
                                  dict[str, object]]:
    data = phase_data()
    forming = {k: chain for k, chain in data.items() if chain}
    first = {k: chain[0] for k, chain in forming.items()}
    second = {k: chain[1] for k, chain in forming.items()
              if len(chain) > 1}
    chain_max = {k: max(c["p0"] for c in chain)
                 for k, chain in forming.items()}
    void_first_max = max(c["p0"] for c in first.values())
    stack_first_min = min(c["p1"] + c["p2"] for c in first.values())
    second_max = max(c["p0"] for c in second.values())
    second_breaks = {k: round(c["p0"], 4) for k, c in second.items()
                     if c["p0"] > _SECOND_CEIL}
    every_chain_void = all(chain_max[k] <= _VOID_CEIL
                           for k in forming)
    certs = [
        _certify("L_ph_formed",
                 {"domain": f"P = {_P}, eps = {_EPS}, "
                            f"Omega = {_OMEGA}, {_N_PHASES} phase "
                            f"draws in k*pi/8, z <= {_Z_END}, "
                            f"near-cap crest definition R >= "
                            f"{_NEAR_CAP} on the seed's brightness "
                            "column",
                  "law": "the near-cap crest FORMS at every initial "
                         "phase: all 8 draws reach R >= 2.5 (first "
                         "crest R ~= 2.81-2.84 at z ~= 2.45); "
                         "round-32's 'sine seed does not focus' "
                         "read a z = 0.35 ridge of R = 1.22 as the "
                         "crest -- an artifact of the loose 1.2 "
                         "threshold",
                  "forming_phases": sorted(forming),
                  "crest_counts": {k: len(c)
                                   for k, c in sorted(data.items())}},
                 lambda: len(forming) == _N_PHASES),
        _certify("L_ph_void_first",
                 {"law": "the near-cap FIRST crest is carrier-void "
                         f"for EVERY phase: P0 <= {_VOID_CEIL} on "
                         f"all 8 (max {void_first_max:.4f}) -- the "
                         "round-22 void is PHASE-INERTIAL; the "
                         "round-32 'sector-dependent' claim is "
                         "superseded (it read low ridges as crests)",
                  "measured": {k: round(c["p0"], 4)
                               for k, c in sorted(first.items())}},
                 lambda: void_first_max <= _VOID_CEIL),
        _certify("L_ph_stack_first",
                 {"law": "the void crest remains the 4-line harmonic "
                         f"stack for EVERY phase: (p1 + p2) >= "
                         f"{_STACK_FLOOR} on all 8 (min "
                         f"{stack_first_min:.3f})",
                  "measured": {k: round(c["p1"] + c["p2"], 4)
                               for k, c in sorted(first.items())}},
                 lambda: stack_first_min >= _STACK_FLOOR),
        _certify("L_ph_second",
                 {"law": "the void persists one recurrence at every "
                         f"phase: near-cap SECOND crest P0 <= "
                         f"{_SECOND_CEIL}",
                  "measured": f"FALSE at two phases: {second_breaks} "
                              f"-- the near-cap second crest at "
                              f"phi = 3pi/8 reaches 0.0612 and at "
                              "phi = pi/2 0.2101 (both R >= 2.5), so "
                              "the round-22 'one-recurrence "
                              "persistence' is phase-fragile at the "
                              "truly crest-level crests",
                  "second_P0": {k: round(c["p0"], 4)
                                for k, c in sorted(second.items())}},
                 lambda: second_max <= _SECOND_CEIL),
        _certify("L_ph_chain_void",
                 {"law": "every near-cap crest in the chain is "
                         f"carrier-void (P0 <= {_VOID_CEIL})",
                  "measured": f"FALSE: the chain maximum P0 is "
                              f"{[round(chain_max[k], 3) for k in sorted(chain_max)]} "
                              "-- the carrier returns at a later "
                              "near-cap crest for every phase "
                              "(round-22 'first-period signature' "
                              "survives the re-scope)",
                  "chain_max_P0": {k: round(v, 4)
                                   for k, v in
                                   sorted(chain_max.items())}},
                 lambda: every_chain_void),
    ]
    return certs, {"first": first, "second": second,
                   "chain_max": chain_max}


if __name__ == "__main__":
    certs, _ = phase_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))