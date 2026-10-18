"""
UNIVERSALITY CHECK: is the marginal order s* physical, or an artifact of the split?

`fractional_margin_sweep.py` located the boundary of the standard regime at `s* = 0.258`
using the orientation `lambda = d/dt log(Z_high/Z_low)` with the high/low split `K0 = 6`.
Two ways that number could be an ARTIFACT rather than a property of the flow:

  (a) it could track `K0` (the arbitrary band split), and
  (b) it could depend on the initial condition (band centre `k0`, width `sigma`, seed).

This script re-locates `s*` across `K0 in {4, 6, 8}` (same IC) and across a different
initial condition (seed=1).  For each configuration it scans the order grid in increasing
`s` (stopping as soon as the crossing is bracketed) and interpolates the first sign
change of the late-window orientation.  If `s*` is stable across these, the margin is a
property of the equation, not of the measurement.

Run one config:   python fractional_margin_universality.py "K0=8"
Run them all:     python fractional_margin_universality.py

Honesty: single resolution (N=32), single window (T=5); a robustness check for the
empirical margin, not a proof.  The wall stays OPEN (card C8-open).
"""
import json
import os
import sys
import numpy as np

OUT = "data/fractional_margin_universality.json"
T_MAX = 5.0
S_GRID = (0.20, 0.23, 0.26, 0.29, 0.32)


def late_orientation(s, **kw):
    from orientation_vs_fractional_s import run_fractional_ns
    ts, sh, cr, l3, div = run_fractional_ns(s, **kw)
    t = np.array(ts)
    late = t >= 0.5 * kw["T_max"]
    lam = float(np.polyfit(t[late], np.log(np.array(sh)[late]), 1)[0])
    return lam, bool(div), len(ts)


def locate_s_star(label, s_grid=S_GRID, **kw):
    rows = []
    prev = None
    for s in s_grid:
        lam, div, n = late_orientation(s, **kw)
        rows.append({"s": s, "lambda_late": lam, "diverged": div, "n": n})
        print(f"    {label:<12} s={s:.2f}  lambda_late={lam:+.3f}  div={div}  n={n}",
              flush=True)
        if prev is not None and prev[1] > 0.0 >= lam:
            (sp, lp), (sc, lc) = prev, (s, lam)
            x = sp - lp * (sc - sp) / (lc - lp)
            print(f"    {label:<12} => s* = {x:.3f}", flush=True)
            return float(x), rows
        prev = (s, lam)
    print(f"    {label:<12} => no crossing in grid", flush=True)
    return None, rows


CONFIGS = [
    ("K0=4", dict(K0=4, seed=0, T_max=T_MAX)),
    ("K0=6", dict(K0=6, seed=0, T_max=T_MAX)),
    ("K0=8", dict(K0=8, seed=0, T_max=T_MAX)),
    ("seed=1", dict(K0=6, seed=1, T_max=T_MAX)),
]


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    configs = [] if which == "summary" else [c for c in CONFIGS if which in ("all", c[0])]
    print("=" * 80)
    print(f"UNIVERSALITY: s* across band split K0 and initial condition  (T={T_MAX})")
    print(f"  running: {[c[0] for c in configs]}")
    print("=" * 80)
    os.makedirs("data", exist_ok=True)
    out = {}
    if os.path.exists(OUT):
        try:
            out = json.load(open(OUT))
        except Exception:
            out = {}
    for name, kw in configs:
        s_star, rows = locate_s_star(name, **kw)
        out[name] = {"s_star": s_star, "T_max": T_MAX, "rows": rows}
        with open(OUT, "w") as f:
            json.dump(out, f, indent=2)
    print("-" * 80)
    print("  located:", {k: (round(v["s_star"], 3) if v["s_star"] else None)
                        for k, v in out.items()}, flush=True)
    if which in ("all", "summary"):
        vals = [v["s_star"] for v in out.values() if v["s_star"] is not None]
        if len(vals) >= 2:
            spread = max(vals) - min(vals)
            print(f"  overall spread of s* = {spread:.3f}  (s* in "
                  f"{min(vals):.3f} .. {max(vals):.3f})")
            stable = spread < 0.06 and len(vals) >= 4
            print("=" * 80)
            if stable:
                print("PASS: s* is stable across K0 and the initial condition -- the")
                print("      margin is a property of the equation.  Wall OPEN (C8-open).")
            else:
                print("NOTE: s* varies with the measurement/IC -- report as such.")
            print("=" * 80)
            assert stable, "s* not stable across configurations"
    print("=" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
