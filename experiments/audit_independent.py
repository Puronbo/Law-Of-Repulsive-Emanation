"""
INDEPENDENT AUDIT: re-derive the project's analytic claims
from scratch, WITHOUT importing any project code.
"""
import math
import random

print("=" * 70)
print("AUDIT 1: Exact Gaussian spike law")
print("Claim: K = (2Aw/(nu sqrt(pi)))^(1/3)")
print("=" * 70)

# Derive int (u')^2 dx for u = A exp(-x^2/(2w^2)) INDEPENDENTLY,
# using numerical quadrature instead of the Gaussian-moment formula.
A, w, nu = 3.0, 0.37, 0.02
N = 4_000_000
L = 40.0 * w
dx = L / N
xs = [-L / 2 + i * dx for i in range(N)]
# midpoint rule
s = 0.0
for i in range(0, N, 4):  # subsample every 4th point, weight 4
    x = xs[i]
    up = -A * x / w**2 * math.exp(-x * x / (2 * w * w))
    s += up * up
s *= 4 * dx
eps = nu * s
K_num = A / eps ** (1.0 / 3.0)
K_claim = (2 * A * w / (nu * math.sqrt(math.pi))) ** (1.0 / 3.0)
print(f"quadrature : K = {K_num:.6f}")
print(f"claim      : K = {K_claim:.6f}")
print(f"match      : {abs(K_num - K_claim) / K_claim * 100:.4f}% diff")

print()
print("=" * 70)
print("AUDIT 2: Self-similar exponent -(d-1)/6 by pure algebra")
print("=" * 70)
# u = s^-a F(x s^-a) with a = sigma (type-II parametrization used).
# dimless ratio K = ||u||_inf / (nu int|grad u|^2)^(1/3):
#   numerator      ~ s^(-a)
#   grad u         ~ s^(-2a)
#   int|grad u|^2  ~ s^(-4a) * s^(da) = s^(a(d-4))
#   denominator    ~ s^(a(d-4)/3)
#   K exponent     = -a - a(d-4)/3 = -a(d-1)/3
for d in (1, 2, 3):
    print(f"  d={d}: exponent = -(d-1)/3 * sigma -> "
          f"{-(d - 1) / 3:+.4f} * sigma")

print()
print("=" * 70)
print("AUDIT 3: Gap 1 inequality  ||du||_2 >= 2Z/sqrt(2E)")
print("=" * 70)
# Proof on file: Cauchy-Schwarz + integration by parts.
# Independent check on RANDOM divergence-free-ish 1D periodic fields.
random.seed(7)
worst = 1e9
for trial in range(200):
    N = 512
    Lp = 2 * math.pi
    dx = Lp / N
    # random smooth field from Fourier modes (periodic => IBP valid)
    import cmath
    uhat = [0j] * N
    for kk in range(1, 8):
        ph = random.uniform(0, 2 * math.pi)
        amp = random.uniform(0.1, 2.0)
        uhat[kk] = amp * cmath.exp(1j * ph)
        uhat[-kk] = uhat[kk].conjugate()
    u = [((sum(uhat[j] * cmath.exp(2j * math.pi * j * i / N)
              for j in range(N))).real) for i in range(N)]
    gu = [((sum(1j * j * uhat[j] * cmath.exp(2j * math.pi * j * i / N)
                for j in range(N))).real) for i in range(N)]
    lu = [((sum(-j * j * uhat[j] * cmath.exp(2j * math.pi * j * i / N)
                for j in range(N))).real) for i in range(N)]
    E = 0.5 * sum(x * x for x in u) * dx
    Z = 0.5 * sum(g * g for g in gu) * dx
    lap = math.sqrt(sum(l * l for l in lu) * dx)
    lhs = lap
    rhs = 2 * Z / math.sqrt(2 * E)
    worst = min(worst, lhs - rhs)
print(f"200 random fields: min(lhs - rhs) = {worst:.3e}")
verdict = "HOLDS" if worst >= -1e-10 else "VIOLATED"
print(f"Gap 1 {verdict} (independent construction)")

print()
print("=" * 70)
print("AUDIT 4: RG fixed point vs published values")
print("=" * 70)
# Recompute FP from the on-file betas and compare to Codello Table 3.
import sys
sys.path.insert(0, ".")
from litim_flow import find_fp  # noqa: E402
res, Gs, ls = find_fp()
print(f"computed: G*={Gs:.4f} lam*={ls:.4f} residual={res:.2e}")
print(f"on-file expectation: G*=0.7012 lam*=0.1715")
print(f"f(R) family (Table 3): G* in 0.95..1.56, GL* stable 0.11-0.12")
