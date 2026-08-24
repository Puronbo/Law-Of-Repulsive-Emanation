"""
RH: LI COEFFICIENT CONVERGENCE
================================

Track how lambda_1 converges as we add more zeros.
The exact value should be positive if RH is true.
"""

import json
import math
import os
import numpy as np
import mpmath

mpmath.mp.dps = 30
OUT = "data/rh_li_convergence.json"


def run():
    print("=" * 70)
    print("RH: LI COEFFICIENT CONVERGENCE")
    print("=" * 70)
    
    # Precompute zeros in batches
    all_zeros = []
    zero_counts = [50, 100, 200, 500, 800]
    
    # Compute 800 zeros
    print("Computing 800 zeros...")
    for k in range(1, 801):
        z = mpmath.zetazero(k)
        all_zeros.append(complex(mpmath.re(z), mpmath.im(z)))
    
    all_zeros = np.array(all_zeros)
    print(f"Done. First: {all_zeros[0]}, Last: {all_zeros[-1]}")
    
    # Track lambda_1, lambda_2, lambda_3 convergence
    print("\n--- Convergence of Li coefficients ---")
    print(f"{'N_zeros':>8s}  {'lambda_1':>14s}  {'lambda_2':>14s}  {'lambda_3':>14s}  {'lambda_5':>14s}")
    
    convergence = []
    for N in zero_counts:
        z = all_zeros[:N]
        
        lams = {}
        for n in [1, 2, 3, 5]:
            lam = 0.0
            for rho in z:
                partner = 1.0 - np.conj(rho)
                t1 = 1.0 - (1.0 + 2.0/rho)**n
                t2 = 1.0 - (1.0 + 2.0/partner)**n
                lam += np.real(t1) + np.real(t2)
            lams[n] = lam
        
        print(f"{N:>8d}  {lams[1]:+14.10f}  {lams[2]:+14.10f}  "
              f"{lams[3]:+14.10f}  {lams[5]:+14.10f}")
        
        convergence.append({
            "n_zeros": N,
            "lambda_1": float(lams[1]),
            "lambda_2": float(lams[2]),
            "lambda_3": float(lams[3]),
            "lambda_5": float(lams[5]),
        })
    
    # The tail correction: for zeros with gamma > T,
    # the contribution to lambda_n is approximately
    # -2n * sum_{gamma > T} 1/gamma^2 (for n=1)
    # = -2n * integral_T^infty N(t)/t^2 dt
    # where N(t) ~ t/(2pi) * log(t/(2pi*e)) + ... (Gram's law)
    
    print("\n--- Tail estimation ---")
    T_last = float(np.imag(all_zeros[-1]))
    N_zeros_total = len(all_zeros)
    
    # Approximate tail: integral from T to inf of N(t)/t^2 dt
    # N(t) ~ t/(2pi) * log(t/(2pi))
    # integral ~ log(T)/(2pi) (leading term)
    tail_lambda1 = -2 * math.log(T_last) / (2 * math.pi)
    
    print(f"  Last zero height: T = {T_last:.1f}")
    print(f"  Estimated tail contribution to lambda_1: {tail_lambda1:.6f}")
    print(f"  lambda_1 with 800 zeros: {convergence[-1]['lambda_1']:.6f}")
    print(f"  Estimated exact lambda_1: {convergence[-1]['lambda_1'] + tail_lambda1:.6f}")
    
    # For n >= 2, the tail is smaller
    tail_lambda2 = -4 * math.log(T_last) / (2 * math.pi)  # roughly
    print(f"  Estimated exact lambda_2: {convergence[-1]['lambda_2'] + tail_lambda2:.6f}")
    
    # Check if n >= 2 all positive
    all_n2_pos = all(c["lambda_2"] > 0 for c in convergence)
    print(f"\n  lambda_2 > 0 for all N: {all_n2_pos}")
    print(f"  lambda_n > 0 for n >= 2, N=800: {all(convergence[-1][f'lambda_{n}'] > 0 for n in [2,3,5])}")
    
    output = {
        "convergence": convergence,
        "all_n2_positive": bool(all_n2_pos),
        "tail_lambda1": float(tail_lambda1),
    }
    
    os.makedirs("data", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nOutput: {OUT}")
    return output


if __name__ == "__main__":
    run()
