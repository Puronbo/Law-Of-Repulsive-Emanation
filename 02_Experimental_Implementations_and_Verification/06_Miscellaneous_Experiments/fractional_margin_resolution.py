"""
RESOLUTION SWEEP: is the marginal order s* resolution-dependent?

`fractional_margin_window.py` established that at fixed N = 32 the standard-regime
boundary is a moving measurement, s*(T) = 0.058 + 1.19/T (rms 0.001).  The remaining
ambiguity is whether that 1/T drift is a genuine continuum effect or an artifact of the
FINITE MODE SET (N = 32).  This script re-locates s* at fixed window T = 6 across the
resolution N in {32, 48} (K0 = 6, seed = 0), by bisection on the order s.

  - if s*(N=48) matches s*(N=32) = 0.259 to within the seed noise (~0.02), the boundary
    is resolution-stable at this window and the 1/T drift is not a finite-mode artifact;
  - if it moves, the finite-window boundary is resolution-dependent.

Caveat: `make_broadband_ic` is seed-based, so the realization is NOT bit-identical across
N (the seed study gives a ~0.02 noise floor); N = 48 is ~4.4x the cost of N = 32.

Run:  python fractional_margin_resolution.py locate 48 0.26 0.30
      python fractional_margin_resolution.py summary
"""
import json
import os
import sys
import numpy as np

CACHE = "data/fractional_margin_resolution_cache.json"
OUT = "data/fractional_margin_resolution.json"
KW = dict(dt=2e-3, T_max=6.0, save_every=25, K0=6, seed=0)


def _load():
    return json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def _save(c):
    os.makedirs("data", exist_ok=True)
    json.dump(c, open(CACHE, "w"), indent=2)


def lam(N, s):
    key = f"N={N} s={s:.3f}"
    c = _load()
    if key in c:
        return c[key][0], c[key][1]
    from orientation_vs_fractional_s import run_fractional_ns
    ts, sh, cr, l3, div = run_fractional_ns(s, N=N, **KW)
    t = np.array(ts)
    late = t >= 0.5 * KW["T_max"]
    val = float(np.polyfit(t[late], np.log(np.array(sh)[late]), 1)[0])
    c[key] = [val, bool(div)]
    _save(c)
    print(f"    N={N} s={s:.3f}  lam={val:+.4f}  div={div}  n={len(ts)}", flush=True)
    return val, bool(div)


def locate(N, lo, hi, tol=0.012):
    flo, _ = lam(N, lo)
    fhi, _ = lam(N, hi)
    assert flo > 0.0 >= fhi, f"N={N}: bracket [{lo},{hi}] failed (lam={flo},{fhi})"
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        fm, _ = lam(N, mid)
        if fm > 0.0:
            lo, flo = mid, fm
        else:
            hi, fhi = mid, fm
    x = lo - flo * (hi - lo) / (fhi - flo)
    print(f"    N={N} => s* = {x:.3f}   (bracket [{lo:.3f},{hi:.3f}])", flush=True)
    return float(x)


def summary():
    out = json.load(open(OUT)) if os.path.exists(OUT) else {}
    print("-" * 80)
    for k, v in sorted(out.items(), key=lambda kv: int(kv[0].split("=")[1])):
        print(f"    {k}:  s* = {v:.3f}")
    s32 = out.get("N=32")
    s48 = out.get("N=48")
    if s32 and s48:
        d = abs(s48 - s32)
        print("-" * 80)
        print(f"  |s*(N=48) - s*(N=32)| = {d:.3f}  (seed noise floor ~0.02)")
        print("=" * 80)
        if d < 0.03:
            print("PASS: s* is resolution-STABLE ~ the 1/T drift is not a finite-N")
            print("      artifact; the moving boundary is physical.  Wall OPEN (C10-open).")
        else:
            print("NOTE: s* shifts with resolution ~ the boundary is resolution-dependent;")
            print("      report s* as a resolution+window-dependent boundary.  Wall OPEN.")
        print("=" * 80)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"
    os.makedirs("data", exist_ok=True)
    out = json.load(open(OUT)) if os.path.exists(OUT) else {}
    if cmd == "locate":
        N = int(sys.argv[2]); lo = float(sys.argv[3]); hi = float(sys.argv[4])
        x = locate(N, lo, hi)
        out[f"N={N}"] = x
        json.dump(out, open(OUT, "w"), indent=2)
    summary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
