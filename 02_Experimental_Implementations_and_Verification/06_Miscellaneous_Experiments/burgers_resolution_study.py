"""
RESOLUTION CONTROL FOR THE CROSS-SYSTEM PROBE.

The cross-system conclusion (Burgers repels, Navier-Stokes attracts) is only as
trustworthy as the convergence of the order/orientation probe on the Burgers side.
This reruns the identical probe at increasing grid sizes N = 256 / 512 / 1024 for a
fixed small viscosity and reports whether the order `k` and orientation `lambda`
settle.  If they converge, the Burgers reading is not a grid artefact and the
cross-system contrast is apples-to-apples.

Data -> data/burgers_resolution_study_nu{nu}.json
"""
import json
import os
import argparse
import numpy as np
from burgers_zero_order import run_case


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nu", type=float, default=0.02)
    ap.add_argument("--Ns", type=str, default="256,512,1024")
    args = ap.parse_args()

    Ns = [int(x) for x in args.Ns.split(",")]
    nu = args.nu
    print("=" * 78)
    print(f"BURGERS RESOLUTION STUDY: nu = {nu}, N in {Ns}")
    print("=" * 78)

    cases = {}
    rows = []
    for N in Ns:
        res = run_case(nu, N=N)
        cases[str(N)] = res
        rows.append((N, res))
        print(f"  N={N:5d}:  k = {res['order_of_vanishing_k']:+.4f}   "
              f"lambda = {res['repulsion_rate_lambda']:+.4f}   [{res['walltime_s']:.1f}s]")

    with open(f"data/burgers_resolution_study_nu{nu}.json", "w") as f:
        json.dump({"nu": nu, "cases": cases}, f, indent=2)

    ks = [r[1]["order_of_vanishing_k"] for r in rows]
    ls = [r[1]["repulsion_rate_lambda"] for r in rows]
    dk = abs(ks[-1] - ks[-2]) / max(abs(ks[-1]), 1e-12)
    dl = abs(ls[-1] - ls[-2]) / max(abs(ls[-1]), 1e-12)
    print("-" * 78)
    print(f"  convergence (N={Ns[-2]} -> {Ns[-1]}):  |dk|/k = {dk:.4f}   |dlambda|/|lambda| = {dl:.4f}")
    assert all(v > 0 for v in ls), "Burgers should be repelling at every resolution"
    tol = 0.10
    conv = dk < tol and dl < tol
    print(f"  {'CONVERGED' if conv else 'NOT converged'} (tol {tol}).  "
          f"Orientation repelling at every N: {all(v > 0 for v in ls)}.")
    print("=" * 78)
    assert conv, "Burgers order/orientation did not converge -- comparison not rigorous"
    print(f"PASS: Burgers reading is grid-converged (k -> {ks[-1]:.3f}, lambda -> {ls[-1]:+.3f}); "
          f"the cross-system contrast with Navier-Stokes is rigorous.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
