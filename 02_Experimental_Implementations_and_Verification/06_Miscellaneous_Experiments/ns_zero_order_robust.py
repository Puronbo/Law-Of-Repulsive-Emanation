"""
SECOND-INITIAL-CONDITION ROBUSTNESS of the order / orientation probe.

The order-of-vanishing `k` and the repulsion rate `lambda` were read on one
broadband initial condition.  Here the SAME probe is run on several different
initial conditions (different random seeds and different spectral bands) at a
fixed resolution, to test whether the two readings are an artefact of that one IC.

If every IC gives a finite order `k > 1` and an ATTRACTING rate `lambda < 0`,
the reading is IC-independent (a property of the decaying flow, not the seed).

Run:
    python ns_zero_order_robust.py --nu 0.1
    python ns_zero_order_robust.py --nu 0.05
"""
import argparse
import json
import os

from ns_zero_order import run_case

# (seed, k0, sigma) -- two seeds on the baseline band, plus a broader and a narrow band
CONFIGS = [(7, 4.0, 1.5), (13, 4.0, 1.5), (7, 3.0, 1.0), (7, 5.0, 2.0)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nu", type=float, default=0.1)
    ap.add_argument("--N", type=int, default=32)
    ap.add_argument("--Tmax", type=float, default=8.0)
    args = ap.parse_args()
    nu, N, Tmax = args.nu, args.N, args.Tmax

    os.makedirs("data", exist_ok=True)
    print("=" * 78)
    print(f"IC ROBUSTNESS  nu={nu}  N={N}  T_max={Tmax}  configs={len(CONFIGS)}")
    print("=" * 78)
    print(f"{'seed':>5} {'k0':>5} {'sigma':>6} {'k':>10} {'lambda':>12} {'share_end':>12}")
    rows = []
    for seed, k0, sigma in CONFIGS:
        res = run_case(nu, N=N, T_max=Tmax, seed=seed, k0=k0, sigma=sigma)
        if res.get("diverged"):
            print(f"{seed:>5} {k0:>5.1f} {sigma:>6.1f}   DIVERGED at t={res['t']:.2f}")
            rows.append({"seed": seed, "k0": k0, "sigma": sigma, "diverged": True})
            continue
        row = {"seed": seed, "k0": k0, "sigma": sigma,
               "k": res["order_of_vanishing_k"],
               "lambda": res["repulsion_rate_lambda"],
               "share_end": res["share_end"]}
        rows.append(row)
        print(f"{seed:>5} {k0:>5.1f} {sigma:>6.1f} {row['k']:>10.4f} "
              f"{row['lambda']:>12.5f} {row['share_end']:>12.3e}")

    ok = [r for r in rows if not r.get("diverged", False)]
    out = f"data/ns_zero_order_robust_nu{nu}.json"
    result = {"nu": nu, "N": N, "T_max": Tmax, "rows": rows}
    if ok:
        ks = [r["k"] for r in ok]
        ls = [r["lambda"] for r in ok]
        result["k_min"], result["k_max"] = min(ks), max(ks)
        result["lambda_min"], result["lambda_max"] = min(ls), max(ls)
        result["all_finite_order"] = all(k > 1.0 for k in ks)
        result["all_attracting"] = all(l < 0.0 for l in ls)
        print(f"\n  k range [{min(ks):.3f}, {max(ks):.3f}]   "
              f"lambda range [{min(ls):+.3f}, {max(ls):+.3f}]   (N_ok={len(ok)})")
        print(f"  VERDICT: finite order on all ICs = {result['all_finite_order']};  "
              f"attracting on all ICs = {result['all_attracting']}")
    with open(out, "w") as f:
        json.dump(result, f, indent=2)

    assert len(ok) >= 3, "need at least three non-diverged ICs"
    assert all(k > 1.0 for k in [r["k"] for r in ok]), "some IC gave order <= 1"
    assert all(l < 0.0 for l in [r["lambda"] for r in ok]), "some IC appeared repelling"
    print(f"\nPASS: order/orientation reading is IC-independent at nu={nu} "
          f"(recorded to {out}).  Diagnostic only.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
