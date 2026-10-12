"""
WINDOW CONVERGENCE: does the marginal order s* converge as the measurement window grows?

`fractional_margin_sweep.py` found s* = 0.258 at T = 6, and
`fractional_margin_universality.py` found s* = 0.300 at T = 5 (K0 = 6, seed = 0).  So the
number that measures the standard-regime boundary MOVES with the window.  That is the
decisive question for the margin claim: either

  (i)  s*(T) converges as T -> infinity (a real critical dissipation order), or
  (ii) s*(T) keeps drifting (the boundary is a measurement window artifact).

This script locates s* for a sequence of windows T in {4, 6, 8} (plus the known T = 5, 6
points) by BISECTION on the order s, since the late-window orientation lambda(s) is
monotone decreasing in s.  It then fits s*(T) against 1/T to read off the T -> infinity
value and reports whether the sequence is settling.

Run one window:  python fractional_margin_window.py 8
Run all:         python fractional_margin_window.py
Summary only:    python fractional_margin_window.py summary

Honesty: single resolution (N=32); a convergence check for the empirical boundary, not a
proof.  The wall stays OPEN (card C10-open).
"""
import json
import os
import sys
import numpy as np

OUT = "data/fractional_margin_window.json"
T_LIST = [4.0, 6.0, 8.0]
S_LO, S_HI, S_TOL = 0.15, 0.45, 0.015
KW = dict(K0=6, seed=0, N=32, dt=2e-3)


def lam_at(s, T):
    from orientation_vs_fractional_s import run_fractional_ns
    ts, sh, cr, l3, div = run_fractional_ns(s, T_max=T, **KW)
    t = np.array(ts)
    late = t >= 0.5 * T
    lam = float(np.polyfit(t[late], np.log(np.array(sh)[late]), 1)[0])
    return lam, bool(div), len(ts)


def locate(T):
    lo, hi = S_LO, S_HI
    flo, dlo, _ = lam_at(lo, T)
    fhi, dhi, _ = lam_at(hi, T)
    print(f"    T={T:<4} s={lo:.2f} lam={flo:+.3f} | s={hi:.2f} lam={fhi:+.3f}",
          flush=True)
    assert flo > 0.0 >= fhi, "sign bracket failed"
    rows = [(lo, flo, False), (hi, fhi, True)]
    while hi - lo > S_TOL:
        mid = 0.5 * (lo + hi)
        fm, dm, _ = lam_at(mid, T)
        rows.append((mid, fm, fm <= 0.0))
        print(f"    T={T:<4} s={mid:.3f} lam={fm:+.3f} div={dm}", flush=True)
        if fm > 0.0:
            lo, flo = mid, fm
        else:
            hi, fhi = mid, fm
    x = lo - flo * (hi - lo) / (fhi - flo)
    print(f"    T={T:<4} => s* = {x:.3f}   ({len(rows)} runs)", flush=True)
    return float(x), rows


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    os.makedirs("data", exist_ok=True)
    out = json.load(open(OUT)) if os.path.exists(OUT) else {}

    if which != "summary":
        todo = T_LIST if which == "all" else [float(which)]
        for T in todo:
            s_star, rows = locate(T)
            out[f"T={T:g}"] = {"s_star": s_star, "rows": rows}
            with open(OUT, "w") as f:
                json.dump(out, f, indent=2)

    print("-" * 80)
    pts = sorted((float(k.split("=")[1]), v["s_star"]) for k, v in out.items())
    print("  s*(T) table:")
    for T, s in pts:
        print(f"    T = {T:<5g}  s* = {s:.3f}")

    if len(pts) >= 3:
        invT = np.array([1.0 / T for T, _ in pts])
        svals = np.array([s for _, s in pts])
        c1, c0 = np.polyfit(invT, svals, 1)
        s_inf = c0
        resid = svals - (c1 * invT + c0)
        print(f"  fit  s*(T) = {s_inf:.3f} + {c1:.3f}/T   (rms resid {np.sqrt(np.mean(resid**2)):.3f})")
        print(f"  extrapolated s*(T->inf) = {s_inf:.3f}")
        rms = float(np.sqrt(np.mean(resid**2)))
        span_last2 = abs(pts[-1][1] - pts[-2][1])
        print(f"  last-step change |s*(T_last) - s*(T_prev)| = {span_last2:.3f}")
        converged = rms < 0.01
        print("=" * 80)
        if converged:
            print(f"PASS: s*(T) follows a clean 1/T law (rms {rms:.4f}); the finite-window")
            print(f"      boundary is a MOVING measurement that extrapolates to")
            print(f"      s*(T->inf) ~ {s_inf:.2f}.  Convergence is algebraic, so the last")
            print("      step is still non-negligible -- report s*(T) = s_inf + c/T.")
            print("      Caveat: fixed N = 32 (finite mode set); test resolution next.")
        else:
            print(f"NOTE: s*(T) does NOT follow a clean 1/T law (rms {rms:.3f}); the")
            print("      boundary is window-dependent -- report s* as a moving boundary,")
            print("      not a critical exponent.  Wall OPEN (C10-open).")
        print("=" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
