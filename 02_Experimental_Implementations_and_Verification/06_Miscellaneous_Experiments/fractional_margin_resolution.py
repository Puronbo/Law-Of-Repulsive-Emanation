"""
RESOLUTION SWEEP (v2): is the T = 16 collapse of s* physics or numerical damping?

At N = 32, `fractional_margin_window.py` found that by T = 16 the sign change of the
orientation vanishes: lambda < 0 for every order s >= 0.01, so s*(T) -> 0 and the
repelling regime looks like a finite-window transient.  But the "inviscid" floor at small
s is set by NUMERICAL damping (2/3 dealiasing + projected Heun RK2), which changes with N.
So the collapse could be numerical.

This script evaluates the late-window orientation lambda at fixed (N, T) by direct
evaluation (mode `lam`) or bisection (`mode locate`), with a disk cache keyed by
(N, T, s).  Comparing N = 32 vs N = 48 at T = 16 decides:

  - if lambda < 0 at BOTH resolutions for all small s -> the collapse is resolution
    independent (not numerical damping): s*(T) -> 0 is physical;
  - if N = 48 shows lambda > 0 where N = 32 did not -> the collapse is a numerical floor.

Run:  python fractional_margin_resolution.py lam 48 16 0.02
      python fractional_margin_resolution.py locate 48 16 0.02 0.18
      python fractional_margin_resolution.py summary
"""
import json
import os
import sys
import numpy as np

CACHE = "data/fractional_margin_resolution_cache.json"
OUT = "data/fractional_margin_resolution.json"


def _load():
    return json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def _save(c):
    os.makedirs("data", exist_ok=True)
    json.dump(c, open(CACHE, "w"), indent=2)


def lam(N, T, s):
    key = f"N={N} T={T:g} s={s:.3f}"
    c = _load()
    if key in c:
        return c[key][0], c[key][1]
    from orientation_vs_fractional_s import run_fractional_ns
    ts, sh, cr, l3, div = run_fractional_ns(s, N=N, dt=2e-3, T_max=T,
                                            save_every=25, K0=6, seed=0)
    t = np.array(ts)
    late = t >= 0.5 * T
    val = float(np.polyfit(t[late], np.log(np.array(sh)[late]), 1)[0])
    c[key] = [val, bool(div)]
    _save(c)
    print(f"    N={N} T={T:g} s={s:.3f}  lam={val:+.4f}  div={div}  n={len(ts)}", flush=True)
    return val, bool(div)


def locate(N, T, lo, hi, tol=0.012):
    flo, _ = lam(N, T, lo)
    fhi, _ = lam(N, T, hi)
    if not (flo > 0.0 >= fhi):
        print(f"    N={N} T={T:g} => NO crossing in [{lo},{hi}] "
              f"(lam={flo:+.3f},{fhi:+.3f})", flush=True)
        return None
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        fm, _ = lam(N, T, mid)
        if fm > 0.0:
            lo, flo = mid, fm
        else:
            hi, fhi = mid, fm
    x = lo - flo * (hi - lo) / (fhi - flo)
    print(f"    N={N} T={T:g} => s* = {x:.3f}   (bracket [{lo:.3f},{hi:.3f}])", flush=True)
    return float(x)


def summary():
    out = json.load(open(OUT)) if os.path.exists(OUT) else {}
    print("-" * 80)
    if not out:
        print("  (no located values yet)")
    for k, v in sorted(out.items()):
        print(f"    {k}:  s* = {'(none -- no crossing)' if v is None else f'{v:.3f}'}")
    print("-" * 80)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"
    os.makedirs("data", exist_ok=True)
    out = json.load(open(OUT)) if os.path.exists(OUT) else {}
    if cmd == "lam":
        lam(int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
    elif cmd == "locate":
        N, T = int(sys.argv[2]), float(sys.argv[3])
        lo, hi = float(sys.argv[4]), float(sys.argv[5])
        out[f"N={N} T={T:g}"] = locate(N, T, lo, hi)
        json.dump(out, open(OUT, "w"), indent=2)
    summary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
