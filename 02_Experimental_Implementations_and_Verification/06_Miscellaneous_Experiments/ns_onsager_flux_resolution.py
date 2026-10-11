"""
RESOLUTION CONVERGENCE of the Onsager flux exponent (`ns_onsager_flux.py`).

The standing caveat on the flux probe was: at nu = 0.05 the dissipative range is
under-resolved at N = 32, so the apparent crossing of the Onsager line a = 1 might
be grid pile-up rather than physics.  This script re-runs the SAME flux probe on
the SAME initial condition at increasing N and reports whether a(N) settles.

Run:
    python ns_onsager_flux_resolution.py --nu 0.05
    python ns_onsager_flux_resolution.py --nu 0.1
"""
import argparse
import json
import os

from ns_onsager_flux import run_case

CONV_TOL = 0.10  # 10% relative change between the two finest grids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nu", type=float, default=0.05)
    ap.add_argument("--Ns", type=str, default="32,48,64")
    args = ap.parse_args()
    Ns = [int(x) for x in args.Ns.split(",")]
    nu = args.nu

    os.makedirs("data", exist_ok=True)
    print("=" * 78)
    print(f"ONSAGER FLUX RESOLUTION STUDY  nu={nu}  N in {Ns}  (same IC, finer grid)")
    print("=" * 78)
    print(f"{'N':>5} {'a':>10} {'eta_max':>10} {'T_run':>8} {'wall_s':>8}")
    rows = []
    for N in Ns:
        res = run_case(nu, N=N)
        if res.get("diverged"):
            print(f"{N:>5}   DIVERGED at t={res['t']:.2f}")
            rows.append({"N": N, "diverged": True})
            continue
        row = {"N": N, "a": res["flux_exponent_a"],
               "eta_max": res["onsager_excess_eta_max"],
               "T_run": res["T_run"], "wall_s": res["walltime_s"]}
        rows.append(row)
        print(f"{N:>5} {row['a']:>10.4f} {row['eta_max']:>10.4f} "
              f"{row['T_run']:>8.1f} {row['wall_s']:>8.0f}")

    ok = [r for r in rows if not r.get("diverged", False)]
    result = {"nu": nu, "Ns": Ns, "rows": rows}
    if len(ok) >= 2:
        da = abs(ok[-1]["a"] - ok[-2]["a"]) / abs(ok[-1]["a"])
        result["da_rel"] = da
        result["converged"] = da < CONV_TOL
        print(f"\n  convergence {ok[-2]['N']}->{ok[-1]['N']}:  |da|/a = {da:.3f}   (tol {CONV_TOL})")
        print(f"  VERDICT: {'CONVERGED' if result['converged'] else 'NOT converged (still grid-dependent)'}")
        print("  a vs the Onsager line a = 1: " + ", ".join(
            f"N{r['N']}: a={r['a']:.3f} ({'above' if r['a'] > 1 else 'below'})" for r in ok))

    out = f"data/ns_onsager_flux_res_nu{nu}.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=2)

    assert len(ok) >= 2, "need at least two non-diverged resolutions"
    print(f"\nPASS: Onsager flux resolution study at nu={nu} recorded to {out}.  Diagnostic only.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
