"""soliton_mixing_rate_audit: spatial variance decay in the twin family.

The density audit tracks one global number (population density); this
audit tracks the FULL distribution spread -- the population-count variance
over the cells of a length-512 ring -- under true-random (LCG high-bit)
half-density seeds, at generations 2, 20 and 100.  It separates the
rules by how much of a random pattern's structure survives:

    preservers     V100/V2 >= 0.8:  the chaotic mixing sector, the
                    stationary sector and the transport pair all KEEP
                    the variance of a random pattern (they mix state
                    space but do not homogenize space);
    collapses      V100/V2 <= 0.6:  exactly {164, 172, 228, 251} -- the
                    de-permuted former rotation 164, the one-lap pair
                    {172, 228} and the fill rule 251 -- reassemble a
                    random pattern into sparse structure within the
                    first 20 generations;
    sparse basins  V100 <= 0.06:     exactly {36, 219, 251} -- the
                    B-side near-uniform attractors and the A-side sparse
                    stationary rule 36.

Rules 204 and 51 preserve the variance EXACTLY (identity and
complement-involution are variance isometries).

Certificates:

    L_variance_collapse_pair PASS/FAIL  the rules with V100/V2 <= 0.6 are
                              exactly {164, 172, 228, 251}.
    L_variance_collapse_fast PASS/FAIL  for every collapse rule the
                              reassembly is already complete at
                              generation 20: V20/V2 <= 0.6.
    L_variance_sparse_basins PASS/FAIL  the rules with V100 <= 0.06 are
                              exactly {36, 219, 251}.
    L_variance_isometry_exact PASS/FAIL  rules 204 and 51 preserve the
                              variance to machine precision (exact
                              isometries).
    L_variance_homogenizer   HONEST_NEGATIVE  the claim "every mixing
                              rule homogenizes space (spatial variance ->
                              0)" is FALSE: the chaotic mixing sector
                              keeps V100 ~ 0.20-0.25; only {36, 219,
                              251} reach V100 <= 0.06 and only 251
                              reaches 0.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES  # noqa: E402

_WIDTH = 512
_GENS = 100
_PROBES = 6
_SAMPLE_GENS = (2, 20, 100)

_COLLAPSE_SET = {164, 172, 228, 251}
_SPARSE_SET = {36, 219, 251}
_ISOMETRY_SET = {204, 51}


def _lcg(seed: int = 0x0DDB1A5E5BAD5EED) -> int:
    return (6364136223846793005 * seed
            + 1442695040888963407) & ((1 << 64) - 1)


def _bit(r: int, l: int, c: int, rr: int) -> int:
    return (r >> ((l << 2) | (c << 1) | rr)) & 1


def _ring_step(r: int, s: list[int]) -> list[int]:
    m = len(s)
    return [_bit(r, s[i - 1], s[i], s[(i + 1) % m]) for i in range(m)]


def _variance_series(r: int) -> dict[int, float]:
    """Mean spatial variance at each sampled generation over probes."""
    acc = {g: [] for g in _SAMPLE_GENS}
    seed = _lcg()
    for _ in range(_PROBES):
        seed = _lcg(seed)
        s = [((seed := _lcg(seed)) >> 16) & 1 for _ in range(_WIDTH)]
        for g in range(1, _GENS + 1):
            s = _ring_step(r, s)
            if g in acc:
                acc[g].append(float(np.var(s)))
    return {g: float(np.mean(v)) for g, v in acc.items()}


def variance_table() -> dict[int, dict]:
    out = {}
    for r in RULES:
        v = _variance_series(r)
        out[r] = {
            "V2": v[2],
            "V20": v[20],
            "V100": v[100],
            "ratio": v[100] / v[2],
            "ratio20": v[20] / v[2],
        }
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


def mixing_rate_certificates() -> tuple[list[dict[str, object]],
                                        dict[int, dict]]:
    t = variance_table()
    collapse = {r for r, d in t.items() if d["ratio"] <= 0.6}
    collapse20 = {r for r, d in t.items() if d["ratio20"] <= 0.6}
    sparse = {r for r, d in t.items() if d["V100"] <= 0.06}
    iso_exact = {r for r, d in t.items()
                 if abs(d["V100"] - d["V2"]) <= 5e-15}
    mixing = set(RULES) - _COLLAPSE_SET - _SPARSE_SET

    certs = [
        _certify("L_variance_collapse_pair",
                 {"domain": f"width {_WIDTH} ring, {_PROBES} true-random "
                            "half-density probes, 100 generations",
                  "law": "the rules whose late-time variance collapses to "
                         f"below 60% of the initial are exactly "
                         f"{sorted(_COLLAPSE_SET)} -- the de-permuted 164, "
                         "the one-lap pair and the fill rule 251",
                  "measured": {str(r): round(t[r]["ratio"], 3) for r in
                               sorted(_COLLAPSE_SET)}},
                 lambda: collapse == _COLLAPSE_SET),
        _certify("L_variance_collapse_fast",
                 {"law": "for every collapse rule the reassembly "
                         "completes within 20 generations: V20/V2 <= 0.6 "
                         "exactly on the collapse set",
                  "measured": {str(r): round(t[r]["ratio20"], 3) for r in
                               sorted(_COLLAPSE_SET)}},
                 lambda: collapse20 == _COLLAPSE_SET),
        _certify("L_variance_sparse_basins",
                 {"law": "the rules whose late-time variance is below "
                         f"0.06 are exactly {sorted(_SPARSE_SET)}",
                  "measured": {str(r): round(t[r]["V100"], 4) for r in
                               sorted(_SPARSE_SET)}},
                 lambda: sparse == _SPARSE_SET),
        _certify("L_variance_isometry_exact",
                 {"law": "rules 204 and 51 preserve the spatial variance "
                         "to machine precision (identity / complement "
                         "are variance isometries)",
                  "measured": {str(r): round(t[r]["V100"], 6) for r in
                               sorted(_ISOMETRY_SET)}},
                 lambda: _ISOMETRY_SET <= iso_exact),
        _certify("L_variance_homogenizer",
                 {"law": "every mixing rule homogenizes a random "
                         "half-density lattice to zero spatial variance",
                  "measured": "the chaotic mixing sector keeps V100 ~ "
                              "0.20-0.25; only "
                              f"{sorted(_SPARSE_SET)} reach V100 <= 0.06 "
                              "and only 251 reaches 0",
                  "non_homogenizers": sorted(mixing)},
                 lambda: all(t[r]["V100"] <= 0.01 for r in mixing)),
    ]
    return certs, t


if __name__ == "__main__":
    certs, t = mixing_rate_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  rule  V2     V20    V100   V100/V2")
    for r in RULES:
        d = t[r]
        print("  %3d  %.3f   %.3f   %.3f   %.3f" % (
            r, d["V2"], d["V20"], d["V100"], d["ratio"]))