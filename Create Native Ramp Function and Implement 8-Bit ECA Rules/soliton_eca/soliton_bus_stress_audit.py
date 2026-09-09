"""soliton_bus_stress_audit: the soliton-bus engine under load, measured --
not assumed.

The engine is exercised at large widths: bit-exact agreement with the
ghost-zero reference step at widths 512..2048 across all 32 family rules,
approximately-linear per-step cost at widths up to 8192, bit-exact
determinism of repeated runs, and long-range marker-impulse fidelity (a
single active pulse on a background of zeros survives intact at width
4096 under rule 204, the bus identity).

Certificates:

    L_stress_reference_large_widths   PASS/FAIL  at widths {512, 1024,
                                    2048}, every family rule matches the
                                    ghost-zero reference for every
                                    generation of every LCG probe.
    L_stress_linearity                PASS/FAIL  per-step wall time scales
                                    approximately linearly: the 2x-width
                                    step-time ratio stays below 2.6 at
                                    widths {2048, 4096, 8192}.
    L_stress_deterministic            PASS/FAIL  two identical runs
                                    (rule 219, width 977, 50 generations)
                                    produce bit-identical outputs.
    L_stress_marker_impulse_fidelity PASS/FAIL  a lone impulse injected on
                                    a zero background at width 4096 under
                                    rule 204 survives every generation
                                    unchanged (the bus neither leaks nor
                                    ghosts at scale).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import SolitonECA, RULES as _RULE_TABLE  # noqa: E402

_WIDE = (512, 1024, 2048)
_LINEAR = (2048, 4096, 8192)
_LINEAR_RATIO = 2.6
_DETERMINISTIC_RULE = 219
_DETERMINISTIC_WIDTH = 977
_MARKER_WIDTH = 4096


def _lcg(seed: int = 0x9E3779B97F4A7C15) -> int:
    state = seed
    while True:
        state = (6364136223846793005 * state + 1442695040888963407) & (
            (1 << 64) - 1)
        yield state


def _ghost_step(rule: int, s: list[int]) -> list[int]:
    """Ghost-zero reference step, matching the SolitonECA boundary."""
    n = len(s)
    out = []
    for i in range(n):
        left = s[i - 1] if i > 0 else 0
        right = s[i + 1] if i < n - 1 else 0
        neighborhood = (left << 2) | (s[i] << 1) | right
        out.append((rule >> neighborhood) & 1)
    return out


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


def _reference_large_widths_holds() -> bool:
    gen = _lcg()
    for rule in _RULE_TABLE:
        for width in _WIDE:
            for _ in range(3):
                initial = [(next(gen) >> 16) & 1 for _ in range(width)]
                engine = SolitonECA(rule, width, initial)
                reference = list(initial)
                for _ in range(6):
                    if list(engine.step()) != _ghost_step(rule, reference):
                        return False
                    reference = _ghost_step(rule, reference)
    return True


def _step_seconds(rule: int, width: int, generations: int) -> float:
    engine = SolitonECA(rule, width)
    t0 = time.perf_counter()
    for _ in range(generations):
        list(engine.step())
    return (time.perf_counter() - t0) / generations


def _linearity_holds() -> bool:
    times = {}
    for width in _LINEAR:
        _step_seconds(204, width, 2)  # warm-up
        times[width] = _step_seconds(204, width, 8)
    return all(times[2 * w] / times[w] <= _LINEAR_RATIO
               for w in _LINEAR[:-1])


def _deterministic_holds() -> bool:
    gen = _lcg()
    initial = [(next(gen) >> 16) & 1 for _ in range(_DETERMINISTIC_WIDTH)]
    runs = []
    for _ in range(2):
        engine = SolitonECA(_DETERMINISTIC_RULE, _DETERMINISTIC_WIDTH,
                            list(initial))
        runs.append(bytes(v for _ in range(50) for v in engine.step()))
    return runs[0] == runs[1]


def _marker_fidelity_holds() -> bool:
    initial = [0] * _MARKER_WIDTH
    initial[_MARKER_WIDTH // 2] = 1
    engine = SolitonECA(204, _MARKER_WIDTH, initial)
    for _ in range(30):
        if list(engine.step()) != initial:
            return False
    return True


def stress_certificates() -> list[dict[str, object]]:
    return [
        _certify("L_stress_reference_large_widths",
                 {"domain": f"all 32 rules x widths {_WIDE} x 3 LCG "
                            "probes x 6 generations",
                  "law": "the engine state equals the ghost-zero reference "
                         "at every generation of every probe",
                  "measured_on": "bit-exact engine-vs-reference "
                                 "comparison at scale"},
                 _reference_large_widths_holds),
        _certify("L_stress_linearity",
                 {"domain": f"rule 204, widths {_LINEAR}, 8 timed "
                            "generations after warm-up",
                  "law": f"step-time ratio for doubling the width < "
                         f"{_LINEAR_RATIO} (approximately linear per-step "
                         "cost)",
                  "measured_on": "per-step wall time per width"},
                 _linearity_holds),
        _certify("L_stress_deterministic",
                 {"domain": f"rule {_DETERMINISTIC_RULE}, width "
                            f"{_DETERMINISTIC_WIDTH}, 50 generations",
                  "law": "two identical runs produce bit-identical "
                         "outputs",
                  "measured_on": "byte comparison of repeated runs"},
                 _deterministic_holds),
        _certify("L_stress_marker_impulse_fidelity",
                 {"domain": f"rule 204, width {_MARKER_WIDTH}, single "
                            "impulse on zero background",
                  "law": "the lone impulse survives every generation "
                         "unchanged (no bus leakage, no ghost cells)",
                  "measured_on": "bit-exact state at 30 generations"},
                 _marker_fidelity_holds),
    ]


def _render_table() -> str:
    rows = ["  width   us/step       rel"]
    prev = None
    first = None
    for width in _LINEAR:
        _step_seconds(204, width, 1)  # warm-up
        secs = _step_seconds(204, width, 8)
        us = secs * 1e6
        rel = 1.0 if prev is None else us / first
        rows.append("  %5d  %8.1f  %7.2f" % (width, us, rel))
        if first is None:
            first = us
        prev = us
    return "\n".join(rows)


if __name__ == "__main__":
    for c in stress_certificates():
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print(_render_table())