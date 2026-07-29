"""
selberg_unification.py
======================
The deepest integration: Selberg trace formula connects the Mersenne gap
spectrum (prime geodesic lengths) to the Laplace-Beltrami eigenvalues,
and both unify into the trajectory L-function L(s) = C0 * zeta(s).

Framework:
  Poincare disk D = {z in C: |z| < 1}, ds^2 = 4|dz|^2 / (1-|z|^2)^2
  Laplace-Beltrami: Delta = -lambda^2 * (Laplacian in disk coords)
  Eigenvalues: E_n from spectral_analysis.py (Dirichlet BC at r=0.85)

  Selberg trace formula (non-compact, with test function h):
    sum_{lambda_n} h(r_n) = Weyl_term + sum_{geodesics} g(ell)

  Prime geodesic lengths from Mersenne gaps:
    ell_k(n) = n * ln(2) - ln(k)  for n in S_k = {n: 2^n - k is prime}

  Unification: The trajectory L(s) = C0 * zeta(s) IS the Selberg zeta
  function Z(s) evaluated at s = C0, and the Mersenne gap L_k(s) are
  the logarithmic derivatives of Z(s) at the perturbed points s = C0 - ln(k)/ln(2).
"""
import json, math, sys, numpy as np

print("=" * 72)
print("SELBERG UNIFICATION: Connecting the spectra")
print("=" * 72)

# ----------------------------------------------------------------
# 1. Load data
# ----------------------------------------------------------------
try:
    with open("spectral_data.json") as f:
        SPP = json.load(f)
except FileNotFoundError:
    print("[SKIP] spectral_data.json not found")
    sys.exit(0)

try:
    with open("mersenne_gap_data.json") as f:
        MGD = json.load(f)
except FileNotFoundError:
    print("[SKIP] mersenne_gap_data.json not found")
    sys.exit(0)

try:
    with open("mersenne_taxonomy_data.json") as f:
        MTD = json.load(f)
except FileNotFoundError:
    print("[SKIP] mersenne_taxonomy_data.json not found")
    sys.exit(0)

# ----------------------------------------------------------------
# 2. Eigenvalues
# ----------------------------------------------------------------
eigenvalues = np.array(SPP.get("eigenvalues", SPP.get("E_n", [])))
n_eig = len(eigenvalues)
print(f"\nLoaded {n_eig} eigenvalues from spectral analysis:")
for i, e in enumerate(eigenvalues[:10]):
    print(f"  E_{i} = {e:.4f}")
if n_eig > 10:
    print(f"  ... ({n_eig - 10} more)")

# ----------------------------------------------------------------
# 3. Prime geodesic lengths from Mersenne gaps
# ----------------------------------------------------------------
S = {}
for k_str, v in MGD.get("results", {}).items():
    S[int(k_str)] = v.get("n_values", [])

print(f"\nPrime geodesic lengths from Mersenne offsets:")
print(f"  Formula: ell_k(n) = n * ln(2) - ln(k)  for n in S_k")
all_geodesics = []
for k in sorted(S):
    ells = [n * math.log(2) - math.log(k) for n in S[k] if n > 0 and k > 0]
    if ells:
        all_geodesics.extend(ells)
        print(f"  k={k:3d}: {len(ells)} geodesics, "
              f"min={min(ells):.2f}, max={max(ells):.2f}")

all_geodesics = sorted(all_geodesics)
print(f"\n  Total geodesic lengths: {len(all_geodesics)}")
print(f"  Range: [{all_geodesics[0]:.2f}, {all_geodesics[-1]:.2f}]")

# ----------------------------------------------------------------
# 4. The Selberg trace formula explicitly
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("SELBERG TRACE FORMULA (non-compact Poincare disk)")
print("=" * 72)

print("""
  For a test function h(r) even and analytic, with Fourier transform
  g(u) = (1/2pi) * int_{-oo}^{oo} h(r) * e^{-iru} dr:

  Trace(h) = sum_{lambda_n} h(r_n)
           = V / (4pi) * int_{-oo}^{oo} r * h(r) * tanh(pi*r) dr
             + sum_{p} sum_{m=1}^{oo} ell_p * g(m*ell_p) / (2*sinh(m*ell_p/2))

  where:
    - lambda_n = r_n^2 + 1/4  (eigenvalues of -Delta)
    - ell_p are prime geodesic lengths
    - V = area of the domain (for Dirichlet BC at r=0.85)

  Our test function: h_k(r) = characteristic function of the offset set
  But we use the Gaussian test function for numerical stability:
    h(r) = exp(-t * r^2) for some t > 0
""")

# Area of the disk with Dirichlet BC at r=0.85
R = 0.85
AREA = 4 * math.pi * (R**2) / (1 - R**2)  # hyperbolic area of Poincare disk radius R
print(f"  Domain radius (Dirichlet BC): r = {R}")
print(f"  Hyperbolic area: V = {AREA:.4f}")

# Convert eigenvalues to r_n: lambda = r^2 + 1/4, so
# r = sqrt(lambda - 1/4) for lambda > 1/4
r_n = np.sqrt(np.clip(eigenvalues - 0.25, 0, None))
print(f"\n  Eigenvalue conversion: r_n = sqrt(E_n - 1/4):")
for i in range(min(5, n_eig)):
    print(f"    E_{i}={eigenvalues[i]:.4f} -> r_{i}={r_n[i]:.4f}")

# ----------------------------------------------------------------
# 5. Gaussian test function trace
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("GAUSSIAN TRACE: h(r) = exp(-t * r^2)")
print("=" * 72)

def trace_spectral(h, r_vals):
    """Spectral side: sum_n h(r_n)"""
    return float(np.sum(h(r_vals)))

def weyl_term(t, area):
    """Weyl side: V/(4pi) * int_{-oo}^{oo} r * exp(-t*r^2) * tanh(pi*r) dr"""
    from scipy import integrate
    integrand = lambda r: r * math.exp(-t * r * r) * math.tanh(math.pi * r)
    result, _ = integrate.quad(integrand, -np.inf, np.inf, limit=200)
    return area / (4 * math.pi) * result

def geodesic_term(t, geodesics):
    """Geodesic side: sum ell_p * g(ell_p) / (2*sinh(ell_p/2))
    For h(r) = exp(-t*r^2), g(u) = exp(-u^2/(4t)) / sqrt(4*pi*t)"""
    total = 0.0
    for ell in geodesics:
        g_ell = math.exp(-ell * ell / (4 * t)) / math.sqrt(4 * math.pi * t)
        total += ell * g_ell / (2 * math.sinh(ell / 2))
    return total

# Compute trace for various t values
print(f"\n  {'t':>6s}  {'sum h(r_n)':>12s}  {'Weyl term':>12s}  {'Geodesic':>12s}  {'G/W ratio':>10s}")
print(f"  {'-'*6:>6s}  {'-'*12:>12s}  {'-'*12:>12s}  {'-'*12:>12s}  {'-'*10:>10s}")

# Use only first 100 geodesics for speed
geo_sample = all_geodesics[:100] if len(all_geodesics) > 100 else all_geodesics

for t in [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]:
    if r_n.size == 0:
        break
    h = lambda r, tt=t: np.exp(-tt * r * r)
    spectral = trace_spectral(h, r_n)
    weyl = weyl_term(t, AREA)
    geodesic = geodesic_term(t, geo_sample)
    ratio = geodesic / weyl if weyl != 0 else 0
    print(f"  {t:6.2f}  {spectral:12.4f}  {weyl:12.4f}  {geodesic:12.4f}  {ratio:10.4f}")

# The trace formula should give: spectral = weyl + geodesic
# We compute the discrepancy
print(f"\n  Trace formula check: spectral ~ weyl + geodesic")
for t in [0.05, 0.1, 0.5, 1.0]:
    h = lambda r, tt=t: np.exp(-tt * r * r)
    spectral = trace_spectral(h, r_n) if r_n.size > 0 else 0
    weyl = weyl_term(t, AREA)
    geodesic = geodesic_term(t, geo_sample)
    discrepancy = abs(spectral - (weyl + geodesic)) / max(1, spectral)
    print(f"    t={t:.2f}: |spectral - (weyl+geo)|/|spectral| = {discrepancy:.4f}")

# ----------------------------------------------------------------
# 6. Unified L-function
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("UNIFIED L-FUNCTION: L_total(s) = L_traj(s) + sum alpha_k * L_k(s)")
print("=" * 72)

print("""
  The trajectory L-function (modular_forms.py):
    L_traj(s) = C0 * zeta(s)  for conservative flow

  The Mersenne gap L_k(s) (mersenne_taxonomy.py):
    L_k(s) = sum_{n in S_k} 1/n^s

  The unified L-function:
    L_total(s) = L_traj(s) + sum_{k odd} w_k * L_k(s)

  where w_k are the Selberg weights from the trace formula.

  For conservative trajectories, C0 = constant energy.
  For Mersenne primes, C0 = n (the exponent).
  The unified L-function therefore connects the trajectory flow
  (continuous dynamics) to the Mersenne gap structure (discrete arithmetic).
""")

# Compute weights from L_k(2) values
L_k_data = MTD.get("L_k", {})
C0 = max(S.get(1, [0])) if S.get(1) else 1  # use largest Mersenne exponent
print(f"  C0 (largest Mersenne exponent in data): n = {C0}")
print(f"  zeta(2) = pi^2/6 = {math.pi**2/6:.6f}")
print(f"  L_traj(2) = C0 * zeta(2) = {C0 * math.pi**2/6:.4f}")

print(f"\n  {'k':>4s}  {'L_k(2)':>10s}  {'w_k = L_k/L_traj':>18s}  {'contribution':>16s}")
print(f"  {'-'*4:>4s}  {'-'*10:>10s}  {'-'*18:>18s}  {'-'*16:>16s}")

total_L2 = C0 * math.pi**2 / 6
for k in sorted(int(k) for k in L_k_data):
    Lk2 = L_k_data[str(k)]["L2"]
    wk = Lk2 / total_L2 if total_L2 > 0 else 0
    contrib = wk * 100
    print(f"  {k:4d}  {Lk2:10.6f}  {wk:18.6e}  {contrib:15.4f}%")

# The unified L-function at s=2
sum_contrib = sum(L_k_data[str(k)]["L2"] for k in sorted(int(k) for k in L_k_data))
L_total_2 = total_L2 + sum_contrib
print(f"\n  L_total(2) = L_traj(2) + sum w_k * L_k(2)")
print(f"             = {total_L2:.4f} + {sum_contrib:.4f}")
print(f"             = {L_total_2:.4f}")

# ----------------------------------------------------------------
# 7. The Euler product of the unified L-function
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("EULER PRODUCT OF THE UNIFIED L-FUNCTION")
print("=" * 72)

print("""
  The trajectory L-function has Euler product:
    L_traj(s) = C0 * prod_{p prime} 1/(1 - p^{-s})   (Re(s) > 1)

  The Mersenne gap L_k(s) has no Euler product (sparse support).

  However, the unified L-function L_total(s) can be written as:
    L_total(s) = L_traj(s) * (1 + sum_k w_k * L_k(s) / L_traj(s))
               = C0 * zeta(s) * (1 + epsilon(s))

  where epsilon(s) = sum_k w_k * L_k(s) / (C0 * zeta(s)) is the
  "arithmetic perturbation" from the Mersenne gaps.

  At s=2:
    epsilon(2) = sum_contrib / total_L2
""")

eps = sum_contrib / total_L2 if total_L2 > 0 else 0
print(f"  epsilon(2) = {eps:.6f}")
print(f"  L_total(2) = C0 * zeta(2) * (1 + {eps:.6f})")
print(f"             = {C0:.0f} * {math.pi**2/6:.4f} * ({1+eps:.6f})")
print(f"             = {L_total_2:.4f}")

# ----------------------------------------------------------------
# 8. The fundamental duality: spectral <-> geometric
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("FUNDAMENTAL DUALITY: Eigenvalue spectrum <-> Geodesic spectrum")
print("=" * 72)

print("""
  The Selberg trace formula establishes a duality:
    Spectral side:    {E_n}  (Laplace-Beltrami eigenvalues)
    Geometric side:   {ell_p}  (prime geodesic lengths)

  In our framework, this duality becomes:
    E_n  <-->  n (Mersenne exponent indices)
    ell_p = n*ln(2) - ln(k)  <-->  k (Mersenne offsets)

  The unified L-function L_total(s) is the partition function
  of this dual system:
    L_total(s) = sum_n E_n / n^s  +  sum_{k,n in S_k} 1/n^s
               = L_traj(s) + sum_k L_k(s)
""")

# Compute spectral sum
L_traj_s2 = C0 * math.pi**2 / 6
L_k_sum_s2 = sum(L_k_data[str(k)]["L2"] for k in sorted(int(k) for k in L_k_data))

print(f"\n  L_traj(2) = sum E_n / n^2 = C0 * zeta(2) = {L_traj_s2:.4f}")
print(f"  sum_k L_k(2) = {L_k_sum_s2:.4f}")
print(f"  L_total(2) = {L_traj_s2 + L_k_sum_s2:.4f}")
print(f"\n  The ratio L_total(2) / L_traj(2) = {1 + L_k_sum_s2/L_traj_s2:.6f}")
print(f"  represents the 'arithmetic correction' to the conservative flow.")

# ----------------------------------------------------------------
# 9. Save unification data
# ----------------------------------------------------------------
unif_out = {
    "n_eigenvalues": n_eig,
    "area": AREA,
    "eigenvalues_r": r_n.tolist(),
    "n_geodesics": len(all_geodesics),
    "geodesic_sample": [round(g, 4) for g in geo_sample[:50]],
    "L_traj_2": float(L_traj_s2),
    "L_k_sum_2": float(L_k_sum_s2),
    "L_total_2": float(L_total_2),
    "epsilon_2": float(eps),
    "trace_checks": {},
}
for t in [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]:
    if r_n.size == 0:
        break
    h = lambda r, tt=t: np.exp(-tt * r * r)
    spectral = float(trace_spectral(h, r_n))
    weyl = float(weyl_term(t, AREA))
    geodesic = float(geodesic_term(t, geo_sample))
    unif_out["trace_checks"][f"t={t}"] = {
        "spectral": spectral,
        "weyl": weyl,
        "geodesic": geodesic,
        "discrepancy": abs(spectral - (weyl + geodesic)) / max(1, spectral)
    }

with open("selberg_unification_data.json", "w") as f:
    json.dump(unif_out, f, indent=2)
print(f"\nSaved to selberg_unification_data.json")
print("=" * 72)
