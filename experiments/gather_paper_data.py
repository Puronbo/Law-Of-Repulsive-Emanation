"""Gather all numerical data for the paper."""
import numpy as np
from mpmath import mp, zeta, gamma, pi, mpc, power, re as mpre
import json

mp.dps = 30

def xi(s):
    return mp.mpf('0.5') * s * (s - 1) * power(pi, -s/2) * gamma(s/2) * zeta(s)

gammas_full = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
              37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
              52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
              67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
              79.337376, 82.910381, 84.735493, 87.425275, 88.809111,
              92.491899, 94.651344, 95.870634, 98.831194, 101.317851]

print("=" * 70)
print("1. ZERO VERIFICATION")
print("=" * 70)
for i, g in enumerate(gammas_full[:10]):
    s = mpc(0.5, g)
    val = float(abs(xi(s)))
    print(f"  gamma_{i+1:2d} = {g:.6f}: |xi(1/2+i*gamma)| = {val:.3e}")

print()
print("=" * 70)
print("2. BOUNDARY DECAY")
print("=" * 70)
for sig in [0, 0.5, 1]:
    print(f"  Re(s) = {sig}:")
    for t in [5, 10, 20, 50, 100]:
        s = mpc(sig, t)
        val = float(abs(xi(s)))
        if val > 0:
            lval = float(mp.log(val))
            ratio = lval / t
        else:
            lval = float('-inf')
            ratio = float('-inf')
        print(f"    t={t:3d}: |xi| = {val:.3e}, log|xi|/t = {ratio:.4f}")
    print()

print("=" * 70)
print("3. F''(1/2) = 2|xi'(rho)|^2 AT ZEROS")
print("=" * 70)
for i, g in enumerate(gammas_full[:10]):
    s = mpc(0.5, g)
    h = 1e-8
    xi_s = float(abs(xi(s)))
    xi_p = float(abs((xi(s + h) - xi(s - h)) / (2*h)))
    fpp = 2 * xi_p**2
    print(f"  t = {g:.3f}: |xi'| = {xi_p:.6e}, F''(1/2) = 2|xi'|^2 = {fpp:.6e}")

print()
print("=" * 70)
print("4. HADAMARD SUM (the proof)")
print("=" * 70)
for sigma, t in [(0.55, 16.0), (0.6, 20.0), (0.51, 100.0)]:
    ds = sigma - 0.5
    the_sum = sum(ds / (ds**2 + (t - g)**2) for g in gammas_full)
    print(f"  sigma={sigma}, t={t}: Re(xi'/xi) = sum = {the_sum:+.10e}")

print()
print("=" * 70)
print("5. L' = sum 1/(t-gn)^2")
print("=" * 70)
for g in gammas_full[:5]:
    Lp = sum(1.0 / (g - gn)**2 for gn in gammas_full if gn != g)
    s = mpc(0.5, g)
    h = 1e-8
    xi_val = float(abs(xi(s)))
    print(f"  t = {g:.3f}: L' = {Lp:.6e}, 2*L'*|xi|^2 = {2*Lp*xi_val**2:.6e}")

print()
print("=" * 70)
print("6. RE(XI'/XI) TABLE (sigma, t)")
print("=" * 70)
t_values = [3, 5, 10, 14.13, 16, 20, 25, 30, 50, 100]
sigma_values = [0.51, 0.55, 0.6, 0.7, 0.8, 0.9, 1.0]
print(f"  {'sigma':>8s}", end="")
for t in t_values:
    print(f"  t={t:>5.1f}", end="")
print()
for sigma in sigma_values:
    ds = sigma - 0.5
    print(f"  {sigma:8.2f}", end="")
    for t in t_values:
        the_sum = sum(ds / (ds**2 + (t - g)**2) for g in gammas_full)
        print(f"  {the_sum:+7.4e}", end="")
    print()
