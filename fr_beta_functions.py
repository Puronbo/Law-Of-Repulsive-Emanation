"""
f(R) beta functions from Codello et al 2009, eq.(117)+(119).
The PDE for dGamma_k/dt is given explicitly. We evaluate it numerically
for a polynomial ansatz f(R) = sum g_n R^n, then extract beta functions
via eq.(119): dg_i/dt = (1/i!) d^i/dR^i [dGamma_k/dt / V]|_{R=0}
using finite differences.

Gauge: rho=0, alpha=0, beta->inf (section VII.4).
Cutoff: optimized (Litim) type Ib.
d=4.
"""
import math

def flow_rhs(R, g, nmax, dgdt=None):
    """
    Evaluate the right-hand side of eq.(117) at dimensionless curvature R=R/k^2.
    
    g = [g_0, g_1, ..., g_nmax] dimensionless couplings (thousands, as in Table 3).
    dgdt = [dg_0/dt, ..., dg_nmax/dt] if provided, used for the dot terms.
    
    Returns dGamma_k/dt evaluated at this R value (dimensionful RHS of eq 117).
    The beta functions are extracted from the Taylor expansion in R.
    """
    pi = math.pi
    R2 = R * R
    R3 = R2 * R
    R4 = R3 * R
    R5 = R4 * R
    R6 = R5 * R

    def poly_eval(c, r):
        """Evaluate polynomial sum c[i] * r^i."""
        s = 0.0
        for i in range(len(c)):
            s += c[i] * r**i
        return s

    def poly_deriv(c, r, order=1):
        """Evaluate d^order/dr^order of polynomial sum c[i] * r^i."""
        s = 0.0
        for i in range(order, len(c)):
            coeff = c[i]
            for j in range(order):
                coeff *= (i - j)
            s += coeff * r**(i - order)
        return s

    def poly_dot(c, dc, r):
        """Evaluate sum dc[i] * r^i (the scale derivative of the polynomial)."""
        s = 0.0
        for i in range(len(dc)):
            s += dc[i] * r**i
        return s

    def poly_dot_deriv(c, dc, r, order=1):
        """Evaluate d^order/dr^order of sum dc[i] * r^i."""
        s = 0.0
        for i in range(order, len(dc)):
            coeff = dc[i]
            for j in range(order):
                coeff *= (i - j)
            s += coeff * r**(i - order)
        return s

    # f and derivatives
    f = poly_eval(g, R)
    fp = poly_deriv(g, R, 1)
    fpp = poly_deriv(g, R, 2)
    fppp = poly_deriv(g, R, 3)

    # dot derivatives (if provided)
    if dgdt is not None:
        f_dot = poly_dot(g, dgdt, R)
        fp_dot = poly_dot_deriv(g, dgdt, R, 1)
        fpp_dot = poly_dot_deriv(g, dgdt, R, 2)
    else:
        f_dot = 0.0
        fp_dot = 0.0
        fpp_dot = 0.0

    # Prefactor: 384*pi^2 / (30240 * R^2) --- but we multiply by R^2 to cancel
    prefactor = 384.0 * pi**2 / 30240.0

    # ===================================================================
    # TERM 1 (eq 117 first big bracket): from transverse-traceless tensor
    # -1008*(511*R^2 - 360*R - 1080)/(R-3)
    # ===================================================================
    def safe_div(num, den):
        if abs(den) < 1e-30:
            return 0.0
        return num / den

    # --- First bracket: -1008*(511*R^2 - 360*R - 1080)/(R-3) ---
    T1a = -1008.0 * (511.0*R2 - 360.0*R - 1080.0) / (R - 3.0)

    # --- Second bracket: -2016*(607*R^2 - 360*R - 2160)/(R-4) ---
    T1b = -2016.0 * (607.0*R2 - 360.0*R - 2160.0) / (R - 4.0)

    # --- Third bracket (tensor propagator numerator terms):
    # 20*(311*R^3 - 126*R^2 - 22680*R + 45360)*(fp_dot + 2*fp - 2*R*fpp)
    #   - 252*(R^2 + 360*R - 1080)*fp
    # all divided by (3*f - (R-3)*fp)
    num_T1c = (20.0 * (311.0*R3 - 126.0*R2 - 22680.0*R + 45360.0)
               * (fp_dot + 2.0*fp - 2.0*R*fpp)
               - 252.0 * (R2 + 360.0*R - 1080.0) * fp)
    den_T1c = 3.0*f - (R - 3.0)*fp
    T1c = safe_div(num_T1c, den_T1c)

    # --- Fourth bracket (from scalar h-sigma mixing):
    # [1008*(29*R^2 + 360*R + 1080)*fp
    #  + 4*(185*R^3 + 3654*R^2 + 22680*R + 45360)*(fp_dot + 2*fp - 2*R*fpp)
    #  - 2016*(29*R^3 + 273*R^2 - 3240)*fpp
    #  - 9*(181*R^4 + 3248*R^3 + 15288*R^2 - 90720)*(fpp_dot - 2*R*fppp)]
    # / (fpp*(R-3)^2 + 2*f + (3-2*R)*fp)
    Rm3sq = (R - 3.0)**2
    num_T1d = (1008.0*(29.0*R2 + 360.0*R + 1080.0)*fp
               + 4.0*(185.0*R3 + 3654.0*R2 + 22680.0*R + 45360.0)
               * (fp_dot + 2.0*fp - 2.0*R*fpp)
               - 2016.0*(29.0*R3 + 273.0*R2 - 3240.0)*fpp
               - 9.0*(181.0*R4 + 3248.0*R3 + 15288.0*R2 - 90720.0)
               * (fpp_dot - 2.0*R*fppp))
    den_T1d = fpp*Rm3sq + 2.0*f + (3.0 - 2.0*R)*fp
    T1d = safe_div(num_T1d, den_T1d)

    bracket1 = T1a + T1b + T1c + T1d

    # ===================================================================
    # SIGMA (isolated modes, eq 118, beta-gauge):
    # Sigma = -10*(R^2 - 20*R + 54)*R^2 / (R^2 - 7*R + 12)
    # ===================================================================
    den_sig = R2 - 7.0*R + 12.0
    Sigma = safe_div(-10.0 * (R2 - 20.0*R + 54.0) * R2, den_sig)

    # ===================================================================
    # Total: prefactor * R^2 * (bracket1 + Sigma) / R^2
    # Actually eq 117 has prefactor * (1/R^2) * {bracket + Sigma}
    # But Sigma already contains R^2 in numerator, so:
    # dGamma/dt = prefactor * (bracket1 + Sigma)
    # ===================================================================
    result = prefactor * (bracket1 + Sigma)

    return result


def extract_beta_functions(g, nmax, step=0.001, method='vandermonde'):
    """
    Extract beta functions dg_i/dt from the PDE eq.(117)+(119).
    
    Method: evaluate flow_rhs at nmax+1 points R=0, step, 2*step, ...
    and extract Taylor coefficients via finite differences.
    
    g = [g_0, ..., g_nmax] (thousands, as in Table 3)
    Returns [dg_0/dt, ..., dg_nmax/dt]
    """
    if method == 'vandermonde':
        # Evaluate at n+1 points
        n = nmax + 1
        R_vals = [i * step for i in range(n)]
        # Use first derivative approximation: solve for fp_dot at each point
        # At R=0, the PDE simplifies most.

        # Build system: at each R_j, the PDE gives an equation
        # involving fp_dot(R_j) = sum_i i * dg_i/dt * R_j^(i-1)
        # We solve for the coefficients of fp_dot's Taylor expansion.

        # Actually, the simplest approach: the PDE gives
        # dGamma/dt = RHS(R, g, g', g'', g''', fp_dot, fpp_dot)
        # We need to find fp_dot(R) = sum_i beta_i * i * R^(i-1)
        # such that the PDE is satisfied at each evaluation point.

        # Since the PDE is nonlinear in fp_dot, we use iterative approach.
        # But for the linearized flow near FP, fp_dot is small, so we
        # can treat it as a perturbation.

        # Better: use the fact that the PDE is already given in the paper
        # as the RHS. We just need to Taylor-expand it.
        # 
        # Key insight from eq.(119): beta_i = (1/i!) * d^i/dR^i [RHS]|_{R=0}
        # So we compute the RHS with fp_dot=0 (zeroth iteration), get a function
        # of R, then extract its Taylor coefficients.

        # First pass: compute RHS ignoring fp_dot terms (they are higher order)
        rhs_vals = []
        for R_j in R_vals:
            rhs_vals.append(flow_rhs(R_j, g, nmax, dgdt=None))

        # Now extract Taylor coefficients of RHS about R=0 using finite differences
        # For equally spaced points, use the standard FD formula
        # Actually, let's use a simpler method: solve the linear system

        # rhs(R) = sum_k c_k * R^k  (Taylor expansion of RHS)
        # We know rhs_vals at R_j = j*step
        # Solve for c_k:
        A = [[R_j**k for k in range(n)] for R_j in R_vals]
        c = solve_linear(A, rhs_vals)

        # Now the PDE says: sum_k c_k R^k + (terms from fp_dot) = dGamma/dt
        # The "terms from fp_dot" in eq 117 are already included in the RHS
        # because we passed dgdt=None. The actual dGamma/dt expansion gives:
        # beta_0 = c_0  (the constant term)
        # But wait, we need to account for the fp_dot contributions.

        # Let me use the DIRECT approach instead:
        # eq.(119): dg_i/dt = (1/i!) * d^i/dR^i [dGamma_k/dt / V]|_{R=0}
        # The RHS of eq.(117) IS dGamma_k/dt / V (up to the prefactor).
        # So beta_i is just the i-th Taylor coefficient of the RHS.

        # But the RHS depends on fp_dot which IS the beta functions.
        # So this is self-referential. We need to solve self-consistently.

        # APPROACH: iterate.
        # Start with dgdt = [0, 0, ..., 0]
        # Compute RHS, extract Taylor coefficients -> new dgdt
        # Repeat until convergence

        dgdt = [0.0] * (nmax + 1)

        for iteration in range(50):
            rhs_vals = []
            for R_j in R_vals:
                rhs_vals.append(flow_rhs(R_j, g, nmax, dgdt=dgdt))

            # Extract Taylor coefficients
            A = [[R_j**k for k in range(n)] for R_j in R_vals]
            c = solve_linear(A, rhs_vals)

            # beta_i = c_i (Taylor coefficient of RHS at R=0)
            new_dgdt = list(c)

            # Check convergence
            max_diff = max(abs(new_dgdt[i] - dgdt[i]) for i in range(n))
            if max_diff < 1e-20:
                break
            dgdt = new_dgdt

        return dgdt

    elif method == 'direct_fd':
        # Direct finite difference of RHS at R=0
        # Compute RHS at R=0 with fp_dot=0, then the Taylor expansion
        # gives beta functions. But this ignores the fp_dot feedback.
        # 
        # For a first approximation, this is fine.
        n = nmax + 1
        hs = step

        # Compute RHS at multiple points near R=0
        # Use central differences for Taylor coefficients
        rhs0 = flow_rhs(0.0, g, nmax, dgdt=None)

        # For higher coefficients, use finite differences
        betas = [0.0] * (nmax + 1)
        betas[0] = rhs0  # beta_0 = RHS(0)

        # For beta_1, beta_2, etc., we need the derivatives of RHS at R=0
        # Use the fact that beta_i = (1/i!) * d^i(RHS)/dR^i|_{R=0}
        # Compute via finite differences on RHS

        # Actually, let's use the Vandermonde approach properly.
        R_vals = [i * hs for i in range(n)]
        rhs_vals = [flow_rhs(R_vals[i], g, nmax, dgdt=None) for i in range(n)]

        A = [[R_vals[i]**k for k in range(n)] for i in range(n)]
        c = solve_linear(A, rhs_vals)
        return c

    else:
        raise ValueError(f"Unknown method: {method}")


def solve_linear(A, b):
    """Solve Ax = b for x using Gaussian elimination with partial pivoting."""
    n = len(b)
    # Augmented matrix
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    for col in range(n):
        # Partial pivoting
        max_val = abs(M[col][col])
        max_row = col
        for row in range(col + 1, n):
            if abs(M[row][col]) > max_val:
                max_val = abs(M[row][col])
                max_row = row
        M[col], M[max_row] = M[max_row], M[col]

        pivot = M[col][col]
        if abs(pivot) < 1e-30:
            continue

        # Eliminate below
        for row in range(col + 1, n):
            factor = M[row][col] / pivot
            for j in range(col, n + 1):
                M[row][j] -= factor * M[col][j]

    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for j in range(i + 1, n):
            s -= M[i][j] * x[j]
        if abs(M[i][i]) > 1e-30:
            x[i] = s / M[i][i]
    return x


def verify_fp(g_fp, nmax):
    """
    Verify that g_fp is a fixed point: all beta functions should vanish.
    """
    betas = extract_beta_functions(g_fp, nmax, step=0.001)
    print("Fixed point verification (beta functions should be ~0):")
    for i, b in enumerate(betas):
        print(f"  beta_{i} = {b:.6e}")
    return betas


def stability_matrix(g_fp, nmax, eps=1e-6):
    """
    Compute the stability matrix M_{ij} = d(beta_i)/d(g_j) at the fixed point.
    """
    n = nmax + 1
    M = [[0.0] * n for _ in range(n)]

    betas0 = extract_beta_functions(g_fp, nmax, step=0.001)

    for j in range(n):
        g_plus = g_fp[:]
        g_plus[j] += eps
        g_minus = g_fp[:]
        g_minus[j] -= eps

        betas_plus = extract_beta_functions(g_plus, nmax, step=0.001)
        betas_minus = extract_beta_functions(g_minus, nmax, step=0.001)

        for i in range(n):
            M[i][j] = (betas_plus[i] - betas_minus[i]) / (2.0 * eps)

    return M


def critical_exponents(M):
    """
    Compute critical exponents from the stability matrix.
    Convention: sum_j M_{ij} V_j = -theta * V_i
    So theta = -eigenvalue of M.
    """
    n = len(M)
    # Compute eigenvalues using QR iteration (simplified)
    # For small n, use the characteristic polynomial
    if n == 2:
        tr = M[0][0] + M[1][1]
        det = M[0][0]*M[1][1] - M[0][1]*M[1][0]
        disc = tr**2 - 4*det
        if disc >= 0:
            sq = math.sqrt(disc)
            e1 = (tr + sq) / 2
            e2 = (tr - sq) / 2
            return [-e1, -e2]
        else:
            sq = math.sqrt(-disc)
            return [complex(-tr/2, sq/2), complex(-tr/2, -sq/2)]
    else:
        # For higher dimensions, use QR algorithm
        return eigenvalues_qr(M)


def eigenvalues_qr(M, max_iter=1000, tol=1e-10):
    """Compute eigenvalues via QR iteration."""
    n = len(M)
    A = [row[:] for row in M]

    for _ in range(max_iter):
        # QR decomposition (Gram-Schmidt)
        Q = [[0.0]*n for _ in range(n)]
        R = [[0.0]*n for _ in range(n)]

        for j in range(n):
            v = [A[i][j] for i in range(n)]
            for i in range(j):
                dot = sum(A[k][j] * Q[k][i] for k in range(n))
                R[i][j] = dot
                for k in range(n):
                    v[k] -= dot * Q[k][i]
            norm = math.sqrt(sum(x**2 for x in v))
            R[j][j] = norm
            if norm > 1e-30:
                for k in range(n):
                    Q[k][j] = v[k] / norm

        # A = Q * R, so new A = R * Q
        A_new = [[0.0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                s = 0.0
                for k in range(n):
                    s += R[i][k] * Q[j][k]  # Note: Q^T here
                A_new[i][j] = s
        A = A_new

    # Eigenvalues are on the diagonal
    evals = []
    i = 0
    while i < n:
        if i + 1 < n and abs(A[i+1][i]) > tol:
            # Complex eigenvalue pair
            tr = A[i][i] + A[i+1][i+1]
            det = A[i][i]*A[i+1][i+1] - A[i][i+1]*A[i+1][i]
            disc = tr**2 - 4*det
            if disc >= 0:
                sq = math.sqrt(disc)
                evals.append(complex((tr+sq)/2, 0))
                evals.append(complex((tr-sq)/2, 0))
            else:
                sq = math.sqrt(-disc)
                evals.append(complex(tr/2, sq/2))
                evals.append(complex(tr/2, -sq/2))
            i += 2
        else:
            evals.append(complex(A[i][i], 0))
            i += 1

    # Critical exponents: theta = -eigenvalue
    return [-e for e in evals]


# ===================================================================
# MAIN: Test with known data from Codello 2009
# ===================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("f(R) BETA FUNCTIONS - DIRECT FROM EQ.(117)")
    print("=" * 70)
    print()

    # Test n=1 (EH truncation)
    # From Table 3: g0* = 5.226e-3, g1* = -20.140e-3
    # (values multiplied by 1000 in the table)
    print("--- n=1 truncation (EH) ---")
    g1_fp = [5.226e-3, -20.140e-3]
    print(f"FP values: g0*={g1_fp[0]:.6f}, g1*={g1_fp[1]:.6f}")
    betas = verify_fp(g1_fp, 1)
    print()

    # Test n=2 truncation
    print("--- n=2 truncation ---")
    g2_fp = [3.292e-3, -12.726e-3, 1.514e-3]
    print(f"FP values: {[f'{x:.6f}' for x in g2_fp]}")
    betas = verify_fp(g2_fp, 2)
    print()

    # Test n=3 truncation
    print("--- n=3 truncation ---")
    g3_fp = [5.184e-3, -19.596e-3, 0.702e-3, -9.682e-3]
    print(f"FP values: {[f'{x:.6f}' for x in g3_fp]}")
    betas = verify_fp(g3_fp, 3)
    print()

    # Test n=4 truncation
    print("--- n=4 truncation ---")
    g4_fp = [5.059e-3, -20.585e-3, 0.270e-3, -10.967e-3, -8.646e-3]
    print(f"FP values: {[f'{x:.6f}' for x in g4_fp]}")
    betas = verify_fp(g4_fp, 4)
    print()

    # If FP values don't verify, try Newton refinement
    print("=" * 70)
    print("NEWTON REFINEMENT OF FP (n=4)")
    print("=" * 70)
    g = g4_fp[:]
    nmax = 4
    for iteration in range(30):
        betas = extract_beta_functions(g, nmax, step=0.0005)
        res = math.sqrt(sum(b**2 for b in betas))
        if res < 1e-12:
            print(f"Converged after {iteration} iterations, residual={res:.2e}")
            break

        M = stability_matrix(g, nmax, eps=1e-6)
        dg = solve_linear(M, [-b for b in betas])

        # Damped Newton step
        alpha = 1.0
        g_new = [g[i] + alpha * dg[i] for i in range(nmax + 1)]

        # Check if residual improved
        betas_new = extract_beta_functions(g_new, nmax, step=0.0005)
        res_new = math.sqrt(sum(b**2 for b in betas_new))

        if res_new < res:
            g = g_new
            if iteration % 5 == 0:
                print(f"  iter {iteration}: residual={res:.2e}, g={[f'{x:.6f}' for x in g]}")
        else:
            alpha *= 0.5
            if alpha < 1e-10:
                print(f"  Stuck at iteration {iteration}, residual={res:.2e}")
                break

    print(f"\nRefined FP: {[f'{x:.6f}' for x in g]}")
    betas = extract_beta_functions(g, nmax, step=0.0005)
    print(f"Residual: {math.sqrt(sum(b**2 for b in betas)):.2e}")
    print(f"Table 3 n=4: g0*=5.059e-3, g1*=-20.585e-3, g2*=0.270e-3, g3*=-10.967e-3, g4*=-8.646e-3")

    # Now compute stability matrix and critical exponents
    print()
    print("=" * 70)
    print("STABILITY MATRIX AND CRITICAL EXPONENTS (n=4)")
    print("=" * 70)
    M = stability_matrix(g, nmax, eps=1e-6)
    print("Stability matrix M:")
    for i in range(nmax + 1):
        print(f"  [{', '.join(f'{M[i][j]:12.4e}' for j in range(nmax + 1))}]")

    evals = critical_exponents(M)
    print(f"\nEigenvalues of M: {evals}")
    thetas = [-e for e in evals]
    print(f"Critical exponents (theta = -eigenvalue): {thetas}")

    # Expected from Table 4 n=4: theta = 2.864 +/- 2.446i, 1.546, -3.911, -5.216
    print(f"\nExpected (Table 4, n=4):")
    print(f"  Complex pair: 2.864 +/- 2.446i")
    print(f"  Real: 1.546, -3.911, -5.216")
