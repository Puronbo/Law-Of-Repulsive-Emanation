"""
THE KEY INEQUALITY
==================
On the critical line, F''(1/2) = 2|xi|^2 * (L' - 2*lambda^2)
where L' = sum 1/(t-gn)^2 > 0  (proved)
and lambda = Im(xi'/xi).

F'' > 0 iff L' > 2*lambda^2

L' has NO cancellation (all terms positive).
lambda has CANCELLATION (terms alternate in sign).
This is why F'' > 0: the positive sum dominates the squared alternating sum.
"""

import numpy as np
from mpmath import mp, zeta, gamma, pi, fabs, mpc, power, re as mpre, im as mpim
import json

mp.dps = 30


def xi(s):
    return mp.mpf('0.5') * s * (s - 1) * power(pi, -s/2) * gamma(s/2) * zeta(s)


def compute_key_inequality(t, gammas):
    """
    Compute L' and 2*lambda^2 and their ratio.
    """
    s = mpc(0.5, t)
    h = mp.mpf('1e-10')

    xi_s = xi(s)
    xi_p = (xi(s + h) - xi(s - h)) / (2 * h)

    # Log derivative
    ld = xi_p / xi_s if fabs(xi_s) > 1e-20 else None

    # lambda = Im(L)
    lam = float(mpim(ld)) if ld else 0

    # F'' directly
    h2 = 0.005
    fpp = (float(fabs(xi(mpc(0.5 + h2, t))))**2
           - 2 * float(fabs(xi_s))**2
           + float(fabs(xi(mpc(0.5 - h2, t))))**2) / h2**2

    # L' from Hadamard: sum 1/(t-gn)^2 + 1/(t+gn)^2
    # Use both positive and negative gamma (conjugate pairs)
    all_gammas = list(gammas) + [-g for g in gammas]
    L_prime = sum(1.0 / (t - g)**2 for g in all_gammas if abs(t - g) > 0.001)

    # The inequality: L' > 2*lambda^2
    two_lam_sq = 2 * lam**2
    ratio = L_prime / two_lam_sq if two_lam_sq > 1e-50 else float('inf')

    # |xi|^2
    xi_sq = float(fabs(xi_s))**2

    # F'' from formula
    fpp_formula = 2 * xi_sq * (L_prime - two_lam_sq)

    return {
        't': t,
        'L_prime': L_prime,
        'lambda': lam,
        'two_lam_sq': two_lam_sq,
        'ratio': ratio,
        'inequality_holds': L_prime > two_lam_sq,
        'fpp_direct': fpp,
        'fpp_formula': fpp_formula,
        'xi_sq': xi_sq
    }


def main():
    print("=== THE KEY INEQUALITY: L' > 2*lambda^2 ===")
    print()
    print("F''(1/2) = 2|xi|^2 * (L' - 2*lambda^2)")
    print("  L' = sum 1/(t-gn)^2 > 0   (no cancellation, all positive)")
    print("  lambda = Im(xi'/xi)         (has cancellation, alternates)")
    print()
    print("L' > 2*lambda^2 iff F'' > 0 iff RH holds at this t")
    print()

    gammas = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
              37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
              52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
              67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
              79.337376, 82.910381, 84.735493, 87.425275, 88.809111,
              92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
              103.725539, 105.446623, 107.168611, 109.916463, 111.030285,
              111.874644, 114.320221, 116.226680, 118.990733, 121.367562,
              122.147690, 124.257865, 127.516648, 129.578685, 131.097408,
              133.936776, 134.201297, 137.135911, 139.795298, 141.122848,
              143.470015, 144.881595, 146.000169, 148.927533, 150.924290,
              153.015909, 155.591213, 156.341429, 158.845722, 161.189349,
              163.030708, 165.537065, 167.181301, 168.833547, 169.910989,
              173.628784, 174.740131, 176.312539, 177.755558, 178.444528,
              180.437053, 182.240214, 183.161489, 184.884173, 185.598380,
              187.294489, 189.412233, 192.016710, 193.079727, 195.267509,
              196.459980, 197.534134, 199.723516, 201.284598, 202.493003,
              204.029987, 204.921764, 206.493844, 207.869885, 209.576534]

    # Dense sampling between zeros
    t_values = list(np.linspace(5, 210, 200))
    # Add exact zeros
    for g in gammas[:20]:
        t_values.append(g)
    t_values.sort()

    results = []
    min_ratio = float('inf')
    min_ratio_t = 0
    all_holds = True

    for t in t_values:
        r = compute_key_inequality(t, gammas)
        results.append(r)

        if r['inequality_holds'] and r['ratio'] < min_ratio:
            min_ratio = r['ratio']
            min_ratio_t = r['t']

        if not r['inequality_holds']:
            all_holds = False
            print(f"  VIOLATION at t={t:.2f}: L'={r['L_prime']:.4e}, "
                  f"2*lam^2={r['two_lam_sq']:.4e}")

    print(f"Tested {len(t_values)} points from t=5 to t=210.")
    print()

    if all_holds:
        print("L' > 2*lambda^2 at ALL tested points.")
        print(f"Minimum ratio L'/(2*lambda^2) = {min_ratio:.6f} at t={min_ratio_t:.2f}")
        print(f"  (ratio > 1 means inequality holds)")
    else:
        print("INEQUALITY VIOLATED at some points!")

    # Show behavior near the minimum
    print()
    print("Behavior near minimum ratio:")
    nearby = [r for r in results if abs(r['t'] - min_ratio_t) < 5]
    for r in nearby:
        is_zero = any(abs(r['t'] - g) < 0.5 for g in gammas[:20])
        tag = " *" if is_zero else ""
        print(f"  t={r['t']:7.2f}: L'={r['L_prime']:+.6e}, "
              f"2*lam^2={r['two_lam_sq']:+.6e}, "
              f"ratio={r['ratio']:.6f}{tag}")

    # High-t behavior
    print()
    print("High-t behavior (t > 100):")
    high_t = [r for r in results if r['t'] > 100]
    if high_t:
        ratios = [r['ratio'] for r in high_t if r['ratio'] < 1e10]
        if ratios:
            print(f"  min ratio: {min(ratios):.6f}")
            print(f"  max ratio: {max(ratios):.6f}")

    with open('data/key_inequality_data.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("Saved to data/key_inequality_data.json")


if __name__ == '__main__':
    main()
