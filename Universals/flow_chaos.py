"""Compute C for the Hamiltonian geodesic flow on the Poincare disk."""
import numpy as np

def gap_D(vals):
    gaps = [abs(vals[i+1] - vals[i]) for i in range(len(vals)-1)]
    mg, vg = float(np.mean(gaps)), float(np.var(gaps))
    return vg / mg if mg > 0 else 0

def factorise(n):
    if n == 1: return {}
    d, pf, p = n, {}, 2
    while p * p <= d:
        while d % p == 0: pf[p] = pf.get(p, 0) + 1; d //= p
        p += 1 if p == 2 else 2
    if d > 1: pf[d] = pf.get(d, 0) + 1
    return pf

def d(n, cnt=1):
    for a in factorise(n).values(): cnt *= a + 1
    return cnt

N = 100
D_d = gap_D([d(n) for n in range(1, N+1)])
print(f"D_d = {D_d:.4f}")

# Pure numpy Hamiltonian flow on Poincare disk
def inv_metric(q):
    r2 = np.dot(q, q)
    return (1 - r2)**2 / 4 if r2 < 1 else 1e-4

def repulsion_grad(q, alpha=1.0):
    r2 = np.dot(q, q)
    if r2 >= 1:
        return np.zeros(2)
    return 2 * alpha * q / (1 - r2)

def christoffel(q, p):
    r2 = np.dot(q, q)
    if r2 >= 1 or r2 == 0:
        return np.zeros(2)
    p2 = np.dot(p, p)
    factor = 4 * r2 * p2 / (1 - r2)**3
    return factor * q

# Conservative flow (no friction)
q = np.array([0.1, 0.0])
p = np.array([0.0, 0.0])
dt = 0.01
steps = 2000

radii = []
for i in range(steps):
    lam_sq = max(inv_metric(q), 1e-4)
    grad_v = repulsion_grad(q)
    christ = christoffel(q, p)
    force = -grad_v + christ

    pHalf = p + 0.5 * dt * force
    qNew = q + dt * pHalf * lam_sq
    r = np.linalg.norm(qNew)
    if r >= 0.99:
        qNew = qNew * (0.99 / r)

    lam_sqN = max(inv_metric(qNew), 1e-4)
    grad_vN = repulsion_grad(qNew)
    christN = christoffel(qNew, pHalf)
    forceN = -grad_vN + christN
    pNew = pHalf + 0.5 * dt * forceN

    q, p = qNew, pNew
    radii.append(np.linalg.norm(q))

# Divisor baseline
D_geo = gap_D(radii)
C_geo = D_geo / D_d

print(f"Steps: {len(radii)}")
print(f"Mean radius: {np.mean(radii):.4f}")
print(f"Radius range: [{min(radii):.4f}, {max(radii):.4f}]")
print(f"D(geodesic radii) = {D_geo:.4f}")
print(f"C(geodesic flow) = {C_geo:.4f}")

# Also try dissipative flow (with friction, approaches attractor)
q = np.array([0.1, 0.0])
p = np.array([0.0, 0.0])
gamma = 0.5
radii_d = []
for i in range(steps):
    lam_sq = max(inv_metric(q), 1e-4)
    grad_v = repulsion_grad(q)
    christ = christoffel(q, p)
    force = -grad_v + christ

    pHalf = p + 0.5 * dt * (force - gamma * p)
    qNew = q + dt * pHalf * lam_sq
    r = np.linalg.norm(qNew)
    if r >= 0.99:
        qNew = qNew * (0.99 / r)

    lam_sqN = max(inv_metric(qNew), 1e-4)
    grad_vN = repulsion_grad(qNew)
    christN = christoffel(qNew, pHalf)
    forceN = -grad_vN + christN
    pNew = pHalf + 0.5 * dt * (forceN - gamma * pHalf)

    q, p = qNew, pNew
    radii_d.append(np.linalg.norm(q))

D_diss = gap_D(radii_d)
C_diss = D_diss / D_d
print(f"\nDissipative (gamma={gamma}):")
print(f"  D(radii) = {D_diss:.4f}")
print(f"  C(radii) = {C_diss:.4f}")
