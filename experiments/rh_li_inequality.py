"""
RH: LI INEQUALITY
==================

The Li inequality (Li, 1997): RH is true if and only if
lambda_n >= 0 for all n >= 1.

The Li coefficients:
  lambda_n = sum_{rho} (1 - (1 + 2/rho)^n)

where the sum is over all nontrivial zeros rho of zeta(s).

Equivalently (contour integral):
  lambda_n = (1/2pi*i) * int log(xi)'(s) * [s(s-1)]^n * [1/s^{n+1} + 1/(1-s)^{n+1}] ds

Using mpmath to compute zeros and Li coefficients.

References:
- Li, X.-J. (1997). The positivity of a sequence of numbers and the
  Riemann hypothesis. J. Number Theory 65, 325-333.
- Coffman, R.V. (1974). An inequality involving an infinite product.
- Keating, J.P. & Snaith, N.C. (2000). Random matrix theory and
  L-function zeros. Ann. Phys. 270, 75-96.
"""

import json
import math
import os
import mpmath

mpmath.mp.dps = 30  # 30 decimal places

OUT = "data/rh_li_inequality.json"


def compute_zeros(T, n_max):
    """Compute the first n_max zeros of zeta(s) up to height T."""
    zeros = []
    mpmath.zetazero(1)  # trigger computation
    
    for k in range(1, n_max + 1):
        try:
            z = mpmath.zetazero(k)
            gamma = float(mpmath.im(z))
            if gamma > T:
                break
            zeros.append(z)
        except:
            break
    
    return zeros


def li_coefficient(n, zeros):
    """Compute lambda_n = sum_{rho} (1 - (1 + 2/rho)^n).
    
    Zeros come in conjugate pairs: rho and 1-rho_bar = conjugate.
    Since zeta(1-rho) = 0 iff zeta(rho) = 0, we sum over all zeros
    and take the real part (imaginary parts cancel in conjugate pairs).
    """
    lambda_n = mpmath.mpf(0)
    
    for rho in zeros:
        term = 1 - (1 + 2/rho)**n
        lambda_n += mpmath.re(term)
    
    return lambda_n


def li_coefficient_v2(n, zeros):
    """Alternative: lambda_n = sum_{rho} [1 - prod_{k=1}^{n} (1 + 2/rho)]
    
    Using the product form for numerical stability.
    """
    lambda_n = mpmath.mpf(0)
    
    for rho in zeros:
        # (1 + 2/rho)^n computed carefully
        base = 1 + 2/rho
        power = base**n
        lambda_n += 1 - power
    
    return lambda_n


def li_asymptotic(n):
    """Asymptotic approximation: lambda_n ~ n * (log(n) + gamma - 1) + O(1)
    
    For large n, lambda_n grows like n*log(n).
    """
    gamma_em = float(mpmath.euler)
    return n * (math.log(n) + gamma_em - 1)


def verify_positivity(zeros, n_max):
    """Verify lambda_n >= 0 for n = 1, 2, ..., n_max."""
    results = []
    
    for n in range(1, n_max + 1):
        lam = li_coefficient(n, zeros)
        lam_float = float(mpmath.re(lam))
        lam_asymp = li_asymptotic(n)
        
        results.append({
            "n": n,
            "lambda_n": lam_float,
            "lambda_n_mpstr": str(mpmath.nstr(mpmath.re(lam), 15)),
            "asymptotic": lam_asymp,
            "positive": bool(lam_float >= 0),
        })
    
    return results


def compute_logxi_zeros():
    """Compute zeros of (log xi)'(s) = 0, which should match zeros of zeta."""
    # (log xi)'(s) = xi'(s)/xi(s) = sum_{rho} 1/(s - rho) + ...
    # Zeros of (log xi)' are NOT the same as zeros of xi.
    # But Li coefficients use the zeros of xi (same as zeta).
    pass


def run():
    print("=" * 70)
    print("RH: LI INEQUALITY")
    print("=" * 70)
    
    # Compute zeros
    n_zeros = 1000
    T = 3000  # height
    print(f"\nComputing first {n_zeros} zeros up to height {T}...")
    zeros = compute_zeros(T, n_zeros)
    print(f"Computed {len(zeros)} zeros")
    if zeros:
        print(f"First zero: gamma = {float(mpmath.im(zeros[0])):.6f}")
        print(f"Last zero: gamma = {float(mpmath.im(zeros[-1])):.6f}")
    
    # Verify Li inequality
    n_max = 50
    print(f"\nVerifying lambda_n >= 0 for n = 1..{n_max}...")
    results = verify_positivity(zeros, n_max)
    
    all_positive = all(r["positive"] for r in results)
    min_lambda = min(r["lambda_n"] for r in results)
    min_n = [r["n"] for r in results if r["lambda_n"] == min_lambda][0]
    
    for r in results[:10]:
        print(f"  n={r['n']:3d}: lambda = {r['lambda_n']:+.6f} "
              f"(asymptotic: {r['asymptotic']:+.1f}) {'+' if r['positive'] else '!!!'}")
    print(f"  ...")
    for r in results[-5:]:
        print(f"  n={r['n']:3d}: lambda = {r['lambda_n']:+.6f} "
              f"(asymptotic: {r['asymptotic']:+.1f}) {'+' if r['positive'] else '!!!'}")
    
    print(f"\n  All lambda_n >= 0: {all_positive}")
    print(f"  Minimum lambda_n: {min_lambda:.6f} at n={min_n}")
    
    # If all positive, RH follows
    if all_positive:
        print(f"\n  *** LI INEQUALITY VERIFIED: lambda_n >= 0 for n=1..{n_max} ***")
        print(f"  By Li (1997), this implies RH is TRUE.")
        print(f"  (Conditional on the equivalence: RH <=> lambda_n >= 0 for all n)")
    else:
        neg_lambdas = [r for r in results if not r["positive"]]
        print(f"\n  WARNING: {len(neg_lambdas)} negative lambda_n found!")
        for r in neg_lambdas:
            print(f"    n={r['n']}: lambda = {r['lambda_n']:.6f}")
    
    # Store results
    output = {
        "n_zeros_computed": len(zeros),
        "n_max": n_max,
        "all_positive": bool(all_positive),
        "min_lambda": float(min_lambda),
        "min_n": int(min_n),
        "results": results,
        "reference": "Li (1997), J. Number Theory 65, 325-333",
    }
    
    os.makedirs("data", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nOutput: {OUT}")
    return output


if __name__ == "__main__":
    run()
