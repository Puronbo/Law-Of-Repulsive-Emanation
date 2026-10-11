"""
RESOLUTION CONVERGENCE of the order / orientation probe (`ns_zero_order.py`).

Every diagnostic so far carries the caveat "under-resolved at N=32".  This script
runs the SAME order-of-vanishing / repulsion probe on the SAME initial condition
(same physical spectrum, more grid points) at increasing N and reports whether the
two measured numbers are grid-converged:

    k(N)      = order of vanishing of the high-shell enstrophy (Z_high ~ Z^k)
    lambda(N) = repulsion rate d/dt log(Z_high / Z_low)

If k(N) and lambda(N) settle (relative change N/2 -> N small) the trend is physical;
if they keep drifting with N the reading is a grid artefact and must stay OPEN.

Run:
    python ns_resolution_study.py --nu 0.1
    python ns_resolution_study.py --nu 0.05
"""
import argparse
import json
import os

from ns_zero_order import run_case

OUT = "data/ns_resolution_study.json"
CONV_TOL = 0.10  # 10% relative change between the two finest grids

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nu", type=float, default=0.1)
    ap.add_argument("--Ns", type=str, default="32,48,64")
    ap.add_argument("--Tmax", type=float, default=8.0)
    args = ap.parse_args()
    Ns = [int(x) for x in args.Ns.split(",")]
    nu = args.nu

    os.makedirs("data", exist_ok=True)
    print("=" * 78)
    print(f"RESOLUTION STUDY  nu={nu}  N in {Ns}  T_max={args.Tmax}  (same IC, finer grid)")
    print("=" * 78)
    print(f"{'N':>5} {'k':>11} {'lambda':>13} {'share_end':>13} {'wall_s':>8}")
    rows = []
    for N in Ns:
        res = run_case(nu, N=N, T_max=args.Tmax)
        if res.get("diverged"):
            print(f"{N:>5}   DIVERGED at t={res['t']:.2f}")
            rows.append({"N": N, "diverged": True})
            continue
        row = {"N": N, "k": res["order_of_vanishing_k"],
               "lambda": res["repulsion_rate_lambda"],
               "share_end": res["share_end"], "wall_s": res["walltime_s"]}
        rows.append(row)
        print(f"{N:>5} {row['k']:>11.4f} {row['lambda']:>13.5f} "
              f"{row['share_end']:>13.3e} {row['wall_s']:>8.0f}")

    ok = [r for r in rows if not r.get("diverged", False)]
    result = {"nu": nu, "Ns": Ns, "T_max": args.Tmax, "rows": rows}
    if len(ok) >= 2:
        dk = abs(ok[-1]["k"] - ok[-2]["k"]) / abs(ok[-1]["k"])
        dl = abs(ok[-1]["lambda"] - ok[-2]["lambda"]) / abs(ok[-1]["lambda"])
        conv = dk < CONV_TOL and dl < CONV_TOL
        result["dk_rel"] = dk
        result["dlambda_rel"] = dl
        result["converged"] = conv
        print(f"\n  convergence {ok[-2]['N']}->{ok[-1]['N']}:  "
              f"|dk|/k = {dk:.3f}   |dlambda|/|lambda| = {dl:.3f}   (tol {CONV_TOL})")
        print(f"  VERDICT: {'CONVERGED (trend is physical)' if conv else 'NOT converged (still grid-dependent)'}")
        trend_k = ok[-1]["k"] - ok[0]["k"]
        trend_l = ok[-1]["lambda"] - ok[0]["lambda"]
        print(f"  trend over N:  k {ok[0]['k']:.3f} -> {ok[-1]['k']:.3f} ({trend_k:+.3f});  "
              f"lambda {ok[0]['lambda']:+.3f} -> {ok[-1]['lambda']:+.3f} ({trend_l:+.3f})")
        if ok[-1]["lambda"] < 0:
            print("  orientation remains ATTRACTING at the finest grid: the great attractor")
            print("  still does not repel in the resolved range." if conv else
                  "  (but the reading is not grid-converged, so this is not yet a physical claim).")
    out = f"data/ns_resolution_study_nu{nu}.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=2)

    assert len(ok) >= 2, "resolution study needs at least two non-diverged resolutions"
    print(f"\nPASS: resolution study at nu={nu} recorded to {out}.  "
          f"converged={result.get('converged')}.  Diagnostic only.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
