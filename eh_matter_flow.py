"""
Einstein-Hilbert gravity + minimally coupled matter (real scalars, Dirac
fermions, abelian vectors), optimized (Litim type II) cutoff.

Sources (exact equations, transcribed verbatim):
  Dona-Eichhorn-Percacci, arXiv:1311.2898 (PRD 89, 084035):
    beta functions        eq.(21),(22)      [any d]
    anomalous dimensions  eq.(23)-(34)      [coupled LINEAR system, eq.(48)]
    perturbative limit    eq.(35)-(38)      [d=4, etas neglected]
    type Ia variant       eq.(46),(47)
  Standard Model counting: N_S = 4 real scalars (Higgs doublet),
    N_D = 45/2 Dirac (= 45 Weyl), N_V = 12 gauge bosons.

Conventions: Gamma_k = (1/16 pi G) int sqrt(g) (-R + 2 Lambda);
dimensionless g_tilde = G k^(d-2), lambda_tilde = Lambda/k^2; t = ln k.

NOTE: there are NO two-loop corrections to beta_G, beta_Lambda anywhere:
in MS scheme the one-loop divergence is Gauss-Bonnet and the two-loop
divergence is Goroff-Sagnotti C^3, which does not feed back on (g, lambda).
The Wetterich equation used here is one-loop exact by construction.
"""
import math

# Standard Model matter content (Dona et al counting)
SM = {"NS": 4.0, "ND": 22.5, "NV": 12.0}
PURE = {"NS": 0.0, "ND": 0.0, "NV": 0.0}


# ----------------------------------------------------------------------
# Perturbative closed system, d=4 (eq. 35,36; type Ia variant eq. 46,47)
# ----------------------------------------------------------------------
def betas_pert(lam, G, N=SM, cutoff="II"):
    NS, ND, NV = N["NS"], N["ND"], N["NV"]
    X = NS + 2.0 * ND - 4.0 * NV
    Y = NS - 4.0 * ND + 2.0 * NV
    grav = 46.0 if cutoff == "II" else 22.0     # graviton+ghost contribution
    cross = -16.0 if cutoff == "II" else 8.0
    bG = 2.0 * G + G * G / (6.0 * math.pi) * (X - grav)
    bl = (-2.0 * lam + G / (4.0 * math.pi) * (Y + 2.0)
          + G * lam / (6.0 * math.pi) * (X + cross))
    return bG, bl


def fp_pert_analytic(N=SM, cutoff="II"):
    """Fixed points eq.(37),(38); type Ia: 46->22 and 31->7."""
    NS, ND, NV = N["NS"], N["ND"], N["NV"]
    X = NS + 2.0 * ND - 4.0 * NV
    Y = NS - 4.0 * ND + 2.0 * NV
    gstar = -12.0 * math.pi / (X - (46.0 if cutoff == "II" else 22.0))
    lstar = -0.75 * (Y + 2.0) / (X - (31.0 if cutoff == "II" else 7.0))
    return lstar, gstar


# ----------------------------------------------------------------------
# Anomalous dimensions, eq.(23)-(34), as the linear system eta = v + M eta
# ----------------------------------------------------------------------
def _eta_affine(lam, G, N, d):
    """Return (v, M) with eta_vec = v + M @ eta_vec, eta=(h,c,S,D,V)."""
    NS, ND, NV = N["NS"], N["ND"], N["NV"]
    pi = math.pi
    nd2 = 2.0 ** (d // 2)                       # 2^floor(d/2), =4 at d=4
    gam = math.gamma(d / 2.0)
    pre = (4.0 * pi) ** (d / 2.0) * gam
    K32 = 32.0 * pi * G / pre                   # common 32-pi prefactor
    K16 = 16.0 * pi * G / pre                   # fermion-loop prefactor in (27)
    w = 1.0 - 2.0 * lam                         # threshold denominator
    v = [0.0] * 5
    M = [[0.0] * 5 for _ in range(5)]

    # --- eta_h = [a + c eta_h + e eta_c] G  + matter loops   (23),(27)
    dm2 = d - 2.0
    a0 = -4.0 * pi * dm2 * (-896 + 264 * d + 1076 * d**2 - 434 * d**3
                            + 21 * d**4 + d**5)
    a1 = 16.0 * pi * dm2 * (-2048 + 2552 * d - 318 * d**2 - 125 * d**3
                            + 2 * d**4 + d**5)
    a2 = -16.0 * pi * (12544 - 25760 * d + 16968 * d**2 - 4228 * d**3
                       + 354 * d**4 - 17 * d**5 + d**6)
    a3 = 4096.0 * pi * dm2 * (-32 + 50 * d - 19 * d**2 + 2 * d**3)
    a4 = -2048.0 * pi * dm2 * (-32 + 50 * d - 19 * d**2 + 2 * d**3)
    anum = a0 + a1 * lam + a2 * lam**2 + a3 * lam**3 + a4 * lam**4
    aden = pre * d**2 * (d**2 - 4) * (3 * d - 2) * w**4
    cnum = (8.0 * pi * (d - 1) * (128 + 720 * d - 350 * d**2 + 29 * d**3
            + 32 * (d - 2) * (d + 4) * lam))
    cden = pre * d**2 * (d + 2) * (d + 4) * (3 * d - 2) * w**3
    enum = -128.0 * pi * (32 - 50 * d + 23 * d**2)
    eden = pre * d**2 * (d + 2) * (d + 4) * (3 * d - 2)
    v[0] += G * anum / aden
    M[0][0] += G * cnum / cden
    M[0][1] += G * enum / eden
    hs = (d - 2) ** 3
    hS = 2.0 * (8 - 10 * d + d**2) / (d + 4)
    hd = 2.0
    hD = (d - 2) / (d + 1)
    hv = d**2 - 12 * d + 8
    hV = -2.0 * (16 - d) / (d + 4)
    fS = 1.0 / (d**2 * (d + 2) * (3 * d - 2))
    fD = (d - 1) * (d - 2) / (d**3 * (3 * d - 2))
    fV = (d - 1) * (d - 2) / (d**2 * (d + 2) * (3 * d - 2))
    v[0] += -NS * K32 * fS * hs + ND * nd2 * K16 * fD * hd \
        - NV * K32 * fV * hv
    M[0][2] += -NS * K32 * fS * hS
    M[0][3] += ND * nd2 * K16 * fD * hD
    M[0][4] += -NV * K32 * fV * hV

    # --- eta_c = [b + dd eta_h + ff eta_c] G                    (28)-(31)
    bnum = 64.0 * pi * (-8 + 4 * d + 18 * d**2 - 7 * d**3
                        + 2 * (4 - 9 * d**2 + 3 * d**3) * lam)
    dnum = -64.0 * pi * (4 - 4 * d - 9 * d**2 + 4 * d**3)
    fnum = -64.0 * pi * (4 - 9 * d**2 + 3 * d**3)
    den = pre * d**2 * (d**2 - 4) * (d + 4) * w**2
    v[1] += G * bnum / den
    M[1][0] += G * dnum / den
    M[1][1] += G * fnum / den

    # --- eta_S                                                  (32)
    s1 = (2.0 / (d + 2)) / w**2
    s2 = (2.0 / (d + 2)) / w
    s3 = (d + 1) * (d - 4) / (2.0 * d * w**2)
    v[2] += -K32 * (s1 + s2 + s3)
    M[2][0] += K32 * (2.0 / ((d + 2) * (d + 4) * w**2)
                      + (d + 1) * (d - 4) / (2.0 * d * (d + 2) * w**2))
    M[2][2] += K32 * 2.0 / ((d + 2) * (d + 4) * w)

    # --- eta_D                                                  (33)
    q1 = (d - 1) * (d**2 + 9 * d - 8) / (8.0 * d * (d - 2) * (d + 1) * w**2)
    q2 = (d - 1) ** 2 / (2.0 * d * (d + 1) * (d - 2) * w)
    q3 = -(d - 1) * (2 * d**2 - 3 * d - 4) / (4.0 * d * (d - 2) * w**2)
    v[3] += K32 * (q1 + q2 + q3)
    M[3][0] += K32 * (-q1 / (d + 3) - q3 / (d + 2))
    M[3][3] += -K32 * (d - 1) ** 2 / (2.0 * d * (d + 1) * (d - 2) * (d + 2) * w)

    # --- eta_V                                                  (34)
    r1 = (d - 1) * (16 + 10 * d - 9 * d**2 + d**3) / (2.0 * d**2 * (d - 2) * w**2)
    r2 = 4.0 * (d - 1) * (2 * d - 5) / (d * (d**2 - 4) * w)
    r3 = 4.0 * (d - 1) * (2 * d - 5) / (d * (d**2 - 4) * w**2)
    v[4] += -K32 * (r1 + r2 + r3)
    M[4][0] += K32 * (r1 / (d + 2) + r3 / (d + 4))
    M[4][4] += K32 * 4.0 * (d - 1) * (2 * d - 5) / (d * (d**2 - 4) * (d + 4) * w)
    return v, M


def _solve_linear(A, b):
    n = len(b)
    aug = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        p = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[p] = aug[p], aug[col]
        pv = aug[col][col]
        if abs(pv) < 1e-300:
            raise ValueError("singular eta system")
        for j in range(col, n + 1):
            aug[col][j] /= pv
        for r in range(n):
            if r != col and aug[r][col] != 0.0:
                fac = aug[r][col]
                for j in range(col, n + 1):
                    aug[r][j] -= fac * aug[col][j]
    return [aug[i][n] for i in range(n)]


def solve_etas(lam, G, N=SM, d=4, improved=True):
    v, M = _eta_affine(lam, G, N, d)
    if not improved:
        return v
    lhs = [[(1.0 if i == j else 0.0) - M[i][j] for j in range(5)] for i in range(5)]
    return _solve_linear(lhs, v)


# ----------------------------------------------------------------------
# Full beta functions, eq.(21),(22)
# ----------------------------------------------------------------------
def betas_full(lam, G, N=SM, d=4, improved=True):
    if G <= 0.0 or 1.0 - 2.0 * lam <= 1e-12:
        return None
    NS, ND, NV = N["NS"], N["ND"], N["NV"]
    pi = math.pi
    nd2 = 2.0 ** (d // 2)
    gam = math.gamma(d / 2.0)
    pre = (4.0 * pi) ** (d / 2.0) * gam
    w = 1.0 - 2.0 * lam
    eh, ec, eS, eD, eV = solve_etas(lam, G, N, d, improved)

    A1 = (d * (d + 1) * (d + 2 - eh) / w - 4.0 * d * (d + 2 - ec)
          + 2 * NS * (2 + d - eS) - 2 * ND * nd2 * (2 + d - eD)
          + 2 * NV * (d * d - 4 - d * eV))
    B = (d * (5 * d - 7) * (d - eh) / w + 4 * (d + 6) * (d - ec)
         - 2 * NS * (d - eS) - ND * nd2 * (d - eD)
         + 2 * NV * (d * (8 - d) - (6 - d) * eV))

    p1 = 8.0 * pi * G / (pre * d * (d + 2))
    p2 = 4.0 * pi * G * lam / (3.0 * d * pre)
    p3 = 4.0 * pi * G * G / (3.0 * d * pre)
    bl = -2.0 * lam + p1 * A1 - p2 * B
    bG = (d - 2) * G - p3 * B
    return bG, bl


# ----------------------------------------------------------------------
# Fixed points, stability, flow
# ----------------------------------------------------------------------
def _newton(lam, G, N, d, improved, iters=200, tol=1e-12):
    """Damped Newton with backtracking; returns (lam, G, residual)."""
    res = betas_full(lam, G, N, d, improved)
    if res is None:
        return lam, G, 1e30
    f = res[0] ** 2 + res[1] ** 2
    for _ in range(iters):
        bG, bl = betas_full(lam, G, N, d, improved)
        if bG * bG + bl * bl < tol:
            break
        eps = 1e-8
        r0 = betas_full(lam + eps, G, N, d, improved)
        r1 = betas_full(lam, G + eps, N, d, improved)
        if r0 is None or r1 is None:
            break
        J = [[(r0[1] - bl) / eps, (r1[1] - bl) / eps],
             [(r0[0] - bG) / eps, (r1[0] - bG) / eps]]
        det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
        if abs(det) < 1e-300:
            break
        dl = -(J[1][1] * bl - J[0][1] * bG) / det
        dG = -(-J[1][0] * bl + J[0][0] * bG) / det
        step = 1.0
        ok = False
        for _ in range(30):
            l2, g2 = lam + step * dl, G + step * dG
            r2 = betas_full(l2, g2, N, d, improved)
            if r2 is not None and g2 > 0 and l2 < 0.49:
                f2 = r2[0] ** 2 + r2[1] ** 2
                if f2 < f:
                    lam, G, f = l2, g2, f2
                    ok = True
                    break
            step *= 0.5
        if not ok:
            break
    res = betas_full(lam, G, N, d, improved)
    fr = 1e30 if res is None else math.hypot(*res)
    return lam, G, fr


def find_fp_full(N=SM, d=4, improved=True):
    lp, gp = fp_pert_analytic(N)
    seeds = [(lp, gp)] if gp > 0 and -1.0 < lp < 0.45 else []
    li = -0.5
    while li < 0.46:
        gj = 0.05
        while gj < 4.0:
            seeds.append((li, gj))
            gj *= 1.25
        li += 0.05
    best = (1e30, None)
    for lam, G in seeds:
        if not (G > 0 and lam < 0.49):
            continue
        try:
            lam2, G2, fr = _newton(lam, G, N, d, improved)
        except (ValueError, OverflowError, ZeroDivisionError):
            continue
        if fr < best[0]:
            best = (fr, (lam2, G2))
        if best[0] < 1e-12:
            break
    return None if best[0] >= 1e-6 else best[1]


def critical_exponents(lam, G, N=SM, d=4, improved=True):
    eps = 1e-7
    bG, bl = betas_full(lam, G, N, d, improved)
    r0 = betas_full(lam + eps, G, N, d, improved)
    r1 = betas_full(lam, G + eps, N, d, improved)
    J = [[(r0[1] - bl) / eps, (r1[1] - bl) / eps],
         [(r0[0] - bG) / eps, (r1[0] - bG) / eps]]
    tr = J[0][0] + J[1][1]
    det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
    disc = tr * tr - 4.0 * det
    if disc >= 0:
        sq = math.sqrt(disc)
        eig = [(-(tr + sq) / 2.0), (-(tr - sq) / 2.0)]   # theta = -eigenvalue
    else:
        sq = math.sqrt(-disc)
        eig = [complex(-tr / 2.0, sq / 2.0), complex(-tr / 2.0, -sq / 2.0)]
    return eig


def relevant_direction(lam, G, N=SM, d=4, improved=True):
    """Eigenvector pair of the stability matrix; returns (v, theta) for the
    most UV-relevant direction (largest Re theta)."""
    eps = 1e-7
    bG, bl = betas_full(lam, G, N, d, improved)
    r0 = betas_full(lam + eps, G, N, d, improved)
    r1 = betas_full(lam, G + eps, N, d, improved)
    J = [[(r0[1] - bl) / eps, (r1[1] - bl) / eps],
         [(r0[0] - bG) / eps, (r1[0] - bG) / eps]]
    tr = J[0][0] + J[1][1]
    det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
    disc = tr * tr - 4.0 * det
    if disc >= 0:
        sq = math.sqrt(disc)
        eigs = [(tr + sq) / 2.0, (tr - sq) / 2.0]
        vecs = []
        for ev in eigs:
            w1, w2 = J[0][1], ev - J[0][0]
            n = math.hypot(w1, w2) or 1.0
            vecs.append((w1 / n, w2 / n))
        order = sorted(range(2), key=lambda i: -eigs[i])
        return vecs[order[0]], -eigs[order[0]]
    sq = math.sqrt(-disc)
    re, im = tr / 2.0, sq / 2.0
    w1, w2 = J[0][1], re - J[0][0]
    n = math.sqrt(w1 * w1 + w2 * w2) or 1.0
    return (w1 / n, w2 / n), complex(-re, -im)


def integrate_to_ir(lam0, G0, N=SM, d=4, improved=True,
                    dt=-0.01, nsteps=20000, lam_stop=0.49):
    """RK4 flow toward IR (t = ln k decreasing). Returns list of (t,lam,G)."""
    traj = [(0.0, lam0, G0)]

    def f(lam, G):
        r = betas_full(lam, G, N, d, improved)
        return (0.0, 0.0) if r is None else (r[1], r[0])

    lam, G = lam0, G0
    for i in range(nsteps):
        k1 = f(lam, G)
        k2 = f(lam + 0.5 * dt * k1[0], G + 0.5 * dt * k1[1])
        k3 = f(lam + 0.5 * dt * k2[0], G + 0.5 * dt * k2[1])
        k4 = f(lam + dt * k3[0], G + dt * k3[1])
        lam += dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
        G += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
        if G <= 0 or lam >= lam_stop or not (abs(lam) < 1e6 and abs(G) < 1e12):
            break
        traj.append(((i + 1) * dt, lam, G))
    return traj


# ----------------------------------------------------------------------
def main():
    for label, N in (("pure gravity", PURE), ("Standard Model", SM)):
        print("=" * 64)
        print(f"{label}:  N_S={N['NS']}  N_D={N['ND']}  N_V={N['NV']}")
        lp, gp = fp_pert_analytic(N)
        print(f"perturbative FP (eq.37,38): lambda*={lp:.6f}  G*={gp:.6f}")
        fp = find_fp_full(N)
        if fp is None:
            print("full system: no fixed point found")
            continue
        lam, G = fp
        bG, bl = betas_full(lam, G, N)
        th = critical_exponents(lam, G, N)
        print(f"full-system FP: lambda*={lam:.6f}  G*={G:.6f}  "
              f"(residual {math.hypot(bG, bl):.2e})")
        print("critical exponents theta:", ", ".join(
            (f"{t.real:.3f}{t.imag:+.3f}i" if isinstance(t, complex)
             else f"{t:.3f}") for t in th))
        vec, theta = relevant_direction(lam, G, N)
        amp = 1e-3
        traj = integrate_to_ir(lam + amp * vec[0], G + amp * vec[1], N)
        t0, l0, g0 = traj[0]
        tn, ln, gn = traj[-1]
        print(f"UV->IR flow along theta={theta:.3f}: {len(traj)} steps, "
              f"ends at t={tn:.2f}, lambda={ln:.4g}, G_tilde={gn:.4g}")
        for tt in (traj[0], traj[len(traj) // 4], traj[len(traj) // 2],
                   traj[3 * len(traj) // 4], traj[-1]):
            t, l, g = tt
            k_over_mp = math.exp(t)
            print(f"  t={t:+8.2f}  k/M_Pl={k_over_mp:.3e}  "
                  f"Lambda(k)/k^2={l:+9.4f}  G(k)*k^2={g:.5f}  "
                  f"L*G={l * g:+.5f}")


if __name__ == "__main__":
    main()
