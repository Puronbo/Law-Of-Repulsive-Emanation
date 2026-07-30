"""Map arithmetic functions to effective t in the d_t family."""
import numpy as np
from scipy.interpolate import interp1d

def factorise(n):
    if n == 1: return {}
    d, pf, p = n, {}, 2
    while p * p <= d:
        while d % p == 0: pf[p] = pf.get(p, 0) + 1; d //= p
        p += 1 if p == 2 else 2
    if d > 1: pf[d] = pf.get(d, 0) + 1
    return pf

def gap_D(vals):
    gaps = [abs(vals[i+1] - vals[i]) for i in range(len(vals)-1)]
    mg, vg = float(np.mean(gaps)), float(np.var(gaps))
    return vg / mg if mg > 0 else 0

def d_t(n, t):
    cnt = 1.0
    for a in factorise(n).values(): cnt *= (a + 1) ** t
    return cnt

N = 100
D_d = gap_D([d_t(n, 1.0) for n in range(1, N+1)])
ts = np.linspace(0, 3, 31)
C_vals = [gap_D([d_t(n, t) for n in range(1, N+1)]) / D_d for t in ts]

ts_ge1 = ts[ts >= 1.0]
Cs_ge1 = np.array(C_vals)[ts >= 1.0]
C_to_t = interp1d(Cs_ge1, ts_ge1, kind='cubic')

funcs = {
    'mu(n)': 0.2172,
    'omega(n)': 0.2541,
    'Omega(n)': 0.3713,
    'lambda(n)': 0.4704,
    'd(n)': 1.0,
    'phi(n)': 5.83,
    'Mersenne': 11.42,
    'rad(n)': 11.71,
    'sigma(n)': 15.11,
    'd(n)^2': 18.03,
}

print(f"{'Function':>20} {'C':>8} {'t_eff':>8}")
print("-" * 38)
for name, c in sorted(funcs.items(), key=lambda x: x[1]):
    if c >= 1.0:
        t_eff = float(C_to_t(c))
        print(f"{name:>20} {c:>8.4f} {t_eff:>8.4f}")
    else:
        print(f"{name:>20} {c:>8.4f} {'<1':>8}")
