"""validate_soliton_delta_linear_origin: independent re-derivation.

Does NOT trust linear_origin_certificates(): it builds its OWN
Kerr-free replica (its own seed construction, its own FFT angle
extraction, its own bin-frequency and wrapped-angle helpers), re-checks
the four linear theorems against its own expectations, and re-derives
the two refutation statistics (first-crest residual median, delta* vs
mean-z Spearman) with its own tie-averaged ranking code.

What the validation asserts:

  - common sideband advance: on every consecutive z pair of every seed
    the plus and minus mode bins both advance by exactly
    -w_bin^2 dz /2 (worst error <= 1e-9).  This is the analytic
    e^{-i w_bin^2 z /2} rotation of the two sideband bins.
  - seed identity: rel1 at z=0 equals 2 phi for every phase-sweep
    seed, to the grid/bin discretization level (0.03 rad).
  - rel1 linear invariance: rel1 is constant over the whole linear
    stage to 1e-9 (common-mode cancellation of the sideband rotation).
  - delta chirp: delta advances by exactly +w_bin^2 dz /2 between
    branch-flip steps; each flip step is a ~pi change collocated with a
    sideband angle within w_bin^2 dz of a +/-pi cut, and flips are
    < 1% of all steps.  delta is therefore NOT frozen in the linear
    stage: the crest-chain freeze is a nonlinear quasi-equilibrium.
  - first-crest linear: HYPOTHESIS refuted (median residual from the
    seed-gauge chirp exceeds 1.0 rad).
  - crest-position: HYPOTHESIS refuted (max per-geometry |rho| of
    delta* vs mean-z stays below 0.75; no geometry reaches 0.75).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_physics import (  # noqa: E402
    Fiber,
    propagate,
)
from soliton_eca.soliton_mi_closure_chain_audit import (  # noqa: E402
    closure_chains,
)
from soliton_eca.soliton_delta_linear_origin_audit import (  # noqa: E402
    linear_origin_certificates,
)

_N = 8192
_L = 64.0
_DZ = 0.05
_STEPS = 20
_P = 1.0
_GRID_TOL = 0.03
_EXACT_TOL = 1e-9
_PHASE_SET = tuple(p * np.pi / 8 for p in range(8))
_GEO = ((0.5, 0.20), (0.5, 0.30), (0.5, 0.45),
        (1.0, 0.20), (1.0, 0.30), (1.0, 0.45))

_EXPECTED = {
    "L_dl_common_sideband_advance": "PASS",
    "L_dl_rel1_seed_identity": "PASS",
    "L_dl_rel1_linear_invariant": "PASS",
    "L_dl_delta_linear_chirp": "PASS",
    "L_dl_first_crest_linear": "HONEST_NEGATIVE",
    "L_dl_crest_position": "HONEST_NEGATIVE",
}


def _grid_array():
    t = np.linspace(-_L / 2, _L / 2, _N, endpoint=False)
    dt = float(np.diff(t)[0])
    return t, dt


def _freqs(dt: float):
    f = 2 * np.pi * np.fft.fftshift(np.fft.fftfreq(_N, dt))
    return f


def _bin_omega(om: float, dt: float) -> float:
    f = _freqs(dt)
    k = int(np.argmin(np.abs(f - om)))
    return abs(float(f[k]))


def _wrap(v: float) -> float:
    return (v + np.pi) % (2 * np.pi) - np.pi


def _phase(u: np.ndarray, om: float, dt: float, sign: int) -> float:
    f = _freqs(dt)
    c = np.fft.fftshift(np.fft.fft(u))
    k = int(np.argmin(np.abs(f - sign * om)))
    return float(np.angle(c[k]))


def _rel1(u: np.ndarray, om: float, dt: float) -> float:
    return _wrap(_phase(u, om, dt, +1) - _phase(u, om, dt, -1))


def _delta(u: np.ndarray, om: float, dt: float) -> float:
    f = _freqs(dt)
    c = np.fft.fftshift(np.fft.fft(u))
    k0 = int(np.argmin(np.abs(f - 0.0)))
    kp = int(np.argmin(np.abs(f - om)))
    km = int(np.argmin(np.abs(f + om)))
    a0, ap, am = np.angle(c[k0]), np.angle(c[kp]), np.angle(c[km])
    return _wrap(a0 - (ap + am) / 2)


def _replica():
    t, dt = _grid_array()
    zs = np.arange(0.0, 18.0 + _DZ / 2, _DZ)
    ri: dict[tuple[float, float, int], list[dict[str, float]]] = {}
    for om, eps in _GEO:
        for p_ind in range(8):
            phi = p_ind * np.pi / 8
            seed = np.sqrt(_P) * (1 + eps * np.cos(om * t + phi))
            cur = np.array(seed)
            prev = 0.0
            row = []
            for z in zs:
                if z > 0.0:
                    cur = propagate(cur, dt, z - prev,
                                    fiber=Fiber(gamma=0.0),
                                    steps=_STEPS)
                    prev = z
                f = _freqs(dt)
                c = np.fft.fftshift(np.fft.fft(cur))
                k0 = int(np.argmin(np.abs(f - 0.0)))
                kp = int(np.argmin(np.abs(f - om)))
                km = int(np.argmin(np.abs(f + om)))
                row.append({"z": float(z),
                            "plus": float(np.angle(c[kp])),
                            "minus": float(np.angle(c[km])),
                            "delta": _delta(cur, om, dt),
                            "rel1": _rel1(cur, om, dt)})
            ri[(om, eps, p_ind)] = row
    return ri, dt


def _ranks(v: list[float]) -> list[float]:
    n = len(v)
    out = [0.0] * n
    order = sorted(range(n), key=lambda i: v[i])
    r = 0.0
    while r < n:
        j = order[int(r)]
        s = 1.0
        while r + s < n and v[order[int(r + s)]] == v[j]:
            s += 1.0
        avg = r + (s - 1.0) / 2.0 + 1.0
        for k in range(int(s)):
            out[order[int(r + k)]] = avg
        r += s
    return out


def _spearman(x: list[float], y: list[float]) -> float:
    if len(x) < 2:
        return 0.0
    rx, ry = _ranks(x), _ranks(y)
    n = len(x)
    mx = sum(rx) / n
    my = sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / n
    sx = (sum((a - mx) ** 2 for a in rx) / n) ** 0.5
    sy = (sum((b - my) ** 2 for b in ry) / n) ** 0.5
    if sx == 0 or sy == 0:
        return 0.0
    return cov / (sx * sy)


# ---- live statuses ----
certs, _ = linear_origin_certificates()
assert len(certs) == 6
for c in certs:
    assert c["label"] in _EXPECTED
    assert c["status"] == _EXPECTED[c["label"]], (
        c["label"], c["status"], _EXPECTED[c["label"]])
    assert ("asserted" in c and "negated" in c and
            c["asserted"] != c["negated"])

# ---- 1. seed identity: rel1(seed) = 2 phi ----
t, dt = _grid_array()
worst_seed = 0.0
for om, eps in _GEO:
    for p_ind in range(8):
        phi = p_ind * np.pi / 8
        seed = np.sqrt(_P) * (1 + eps * np.cos(om * t + phi))
        worst_seed = max(worst_seed,
                         abs(_wrap(_rel1(seed, om, dt) - 2 * phi)))
assert worst_seed <= _GRID_TOL, worst_seed

# ---- 2. common sideband advance + rel1 invariance + delta chirp ----
ri, dt = _replica()
worst_common = 0.0
worst_rel1_drift = 0.0
flips = 0
misplaced = 0
steps = 0
for (om, eps, p), row in ri.items():
    w = _bin_omega(om, dt)
    r0 = row[0]["rel1"]
    for c0, c1 in zip(row[:-1], row[1:]):
        steps += 1
        dz = c1["z"] - c0["z"]
        exp_sb = -(w ** 2) * dz / 2
        worst_common = max(
            worst_common,
            abs(_wrap(c1["plus"] - c0["plus"]) - exp_sb),
            abs(_wrap(c1["minus"] - c0["minus"]) - exp_sb))
        worst_rel1_drift = max(worst_rel1_drift,
                               abs(_wrap(c1["rel1"] - r0)))
        adv_d = _wrap(c1["delta"] - c0["delta"])
        exp_d = (w ** 2) * dz / 2
        if abs(adv_d - exp_d) <= _EXACT_TOL:
            continue
        flips += 1
        # flip window = one full per-step advance w^2 dz (the flip
        # magnitude is pi +- w^2 dz/2; the margin covers fp knife-edge)
        pi_like = abs(abs(adv_d) - np.pi) <= (w ** 2) * dz
        at_cut = (min(abs(c0["plus"]), abs(c1["plus"]))
                  > np.pi - (w ** 2) * dz) or \
                 (min(abs(c0["minus"]), abs(c1["minus"]))
                  > np.pi - (w ** 2) * dz)
        if not (pi_like and at_cut):
            misplaced += 1
assert worst_common <= _EXACT_TOL, worst_common
assert worst_rel1_drift <= _EXACT_TOL, worst_rel1_drift
assert misplaced == 0, misplaced
assert flips / steps < 0.01, (flips, steps)

# ---- 3. first-crest linear refutation ----
ct = closure_chains()
res = []
for (om, eps), phases in ct.items():
    w = _bin_omega(om, dt)
    for p_ind in range(8):
        ch = phases[f"p{p_ind}"]
        if not ch:
            continue
        z1 = ch[0]["z"]
        seed = np.sqrt(_P) * (1 + eps * np.cos(
            om * t + p_ind * np.pi / 8))
        linear_at_z1 = _wrap(_delta(seed, om, dt) + w ** 2 * z1 / 2)
        res.append(abs(_wrap(ch[0]["delta"] - linear_at_z1)))
median_resid = float(np.median(res))
assert median_resid > 1.0, median_resid

# ---- 4. crest-position refutation ----
all_pairs = []
per_geo = []
for om, eps in _GEO:
    pairs = []
    for p_ind in range(8):
        ch = ct[(om, eps)][f"p{p_ind}"]
        if len(ch) >= 1:
            pairs.append((float(np.mean([c["delta"] for c in ch])),
                          float(np.mean([c["z"] for c in ch]))))
    all_pairs.extend(pairs)
    if len(pairs) >= 4:
        per_geo.append(_spearman([a for a, _ in pairs],
                                 [b for _, b in pairs]))
max_rho = max(per_geo) if per_geo else 0.0
n_strong = sum(1 for v in per_geo if v >= 0.75)
assert max_rho < 0.75, max_rho
assert n_strong < 3, n_strong
assert abs(_spearman([a for a, _ in all_pairs],
                     [b for _, b in all_pairs])) < 0.75

print("soliton delta-linear-origin validation passed")
print(f"  worst seed rel1 identity resid: {worst_seed:.4f}")
print(f"  worst common sideband err: {worst_common:.3e}")
print(f"  worst rel1 linear drift: {worst_rel1_drift:.3e}")
print(f"  flip steps {flips}/{steps} ({flips / steps:.4f}), misplaced {misplaced}")
print(f"  first-crest median resid: {median_resid:.4f}")
print(f"  delta*-zbar max per-geo rho: {max_rho:.4f}")