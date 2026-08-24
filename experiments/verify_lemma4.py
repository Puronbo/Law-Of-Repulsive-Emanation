"""
INDEPENDENT VERIFICATION of Lemma 4 (dilation exactness)
=========================================================
Different from experiments/log_corridor.py in every load-bearing way:
  - profile: compact-support cosine bump (NOT Gaussian; no closed form),
    so any agreement is structural, not fitted-to-formula
  - norms via Riemann sums of analytic derivative expressions where
    possible, else central differences at TWO resolutions
  - lambda set includes irrational/arbitrary values

Identity under test:  K[u] = K[F] * lambda^((d-1)/3)
Hand re-derivation (third route): grad u = lam^2 gradF(lam x);
int|grad u|^2 = lam^4 * lam^{-d} int|gradF|^2 = lam^{4-d} Z_F;
K = lam||F||inf / (nu lam^{4-d} Z_F)^{1/3} = lam^{(d-1)/3} K[F].  OK.
"""
import numpy as np

def make_F(d, n):
    """Compact cosine bump on [-1,1]^d."""
    ax = np.linspace(-1, 1, n)
    grids = np.meshgrid(*([ax]*d), indexing="ij")
    r = np.sqrt(sum(c**2 for c in grids))
    inside = r < 1.0
    F = np.where(inside, np.cos(np.pi * r / 2) ** 4, 0.0)
    return F, ax[1]-ax[0]

def K_at(d, lam, n):
    ws = 1.0/lam
    ax = np.linspace(-ws, ws, n)
    h = ax[1]-ax[0]
    g = np.meshgrid(*([ax]*d), indexing="ij")
    rr = np.sqrt(sum(c**2 for c in g))
    U = np.where(rr < ws, lam*np.cos(np.pi*rr/(2*ws))**4, 0.0)
    g2 = np.zeros_like(U)
    for k in range(d):
        g2 += np.gradient(U, h, axis=k)**2
    eps = float(np.sum(g2)*h**d)
    return float(np.max(np.abs(U))) / eps**(1/3)

print("Lemma 4 verification, cosine-bump profile (no closed form):")
print(f"{'d':>2} {'lam':>10} {'n':>5} {'measured ratio':>16} {'predicted':>12}")
all_err = []
for d in (1,2,3):
    for n in (401, 1601) if d==1 else ([201,801] if d==2 else [81,161]):
        K1 = K_at(d, 1.0, n)          # reference, same resolution
        for lam in (0.3, 1/np.pi, 1.0, np.e, 4.7):
            meas = K_at(d, lam, n)/K1
            pred = lam**((d-1)/3)
            err = abs(meas-pred)/pred
            all_err.append(err)
            print(f"{d:>2} {lam:>10.4f} {n:>5} {meas:>16.8f} {pred:>12.8f}  err={err:.1e}")
print(f"\nmax relative error across {len(all_err)} checks: {max(all_err):.2e}")
print("VERDICT:", "IDENTITY HOLDS" if max(all_err) < 2e-3 else "INVESTIGATE")
