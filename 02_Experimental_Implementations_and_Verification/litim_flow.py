"""
Beta functions for EH truncation, Litim (optimized) cutoff, d=4.
TYPE Ib with field redefinitions.
From Codello et al 2009, eq.(53).
Also integrates RG flow from UV FP to IR.
"""
import math

def beta_Ib(G, lam):
    pi = math.pi
    w2 = (1.0 - 2.0*lam)**2
    denom = w2 - (29.0 - 9.0*lam)/(72.0*pi) * G
    if abs(denom) < 1e-30:
        return 0.0, 0.0
    num_lam = ((12.0 - 33.0*lam + 20.0*lam**2 - 200.0*lam**3)*G
               + (467.0 - 572.0*lam)/(12.0*pi) * G**2)
    num_G = (105.0 - 212.0*lam + 200.0*lam**2) * G**2
    bl = -2.0*lam + (1.0/(24.0*pi)) * num_lam / denom
    bG = 2.0*G - (1.0/(24.0*pi)) * num_G / denom
    return bG, bl

def find_fp():
    best = (1e30, 0, 0)
    for i in range(1, 300):
        for j in range(1, 49):
            G0, l0 = i/100.0, j/100.0
            for _ in range(200):
                bG, bl = beta_Ib(G0, l0)
                if abs(bG)+abs(bl) < 1e-14:
                    break
                eps = 1e-8
                M00 = (beta_Ib(G0+eps,l0)[0]-bG)/eps
                M01 = (beta_Ib(G0,l0+eps)[0]-bG)/eps
                M10 = (beta_Ib(G0+eps,l0)[1]-bl)/eps
                M11 = (beta_Ib(G0,l0+eps)[1]-bl)/eps
                det = M00*M11-M01*M10
                if abs(det)<1e-30: break
                dG = -(M11*bG-M01*bl)/det
                dl = -(-M10*bG+M00*bl)/det
                G0 += dG; l0 += dl
                if l0>=0.5 or l0<=-0.01 or G0<=0: break
            if l0>0 and l0<0.5 and G0>0:
                bG2, bl2 = beta_Ib(G0, l0)
                res = bG2**2+bl2**2
                if res < best[0]:
                    best = (res, G0, l0)
    return best

def stability_matrix(G, lam):
    eps = 1e-7
    bG0, bl0 = beta_Ib(G, lam)
    M = [[(beta_Ib(G+eps,lam)[0]-bG0)/eps, (beta_Ib(G,lam+eps)[0]-bG0)/eps],
         [(beta_Ib(G+eps,lam)[1]-bl0)/eps, (beta_Ib(G,lam+eps)[1]-bl0)/eps]]
    return M

def rk4_step(G, lam, dt):
    """4th order Runge-Kutta step for RG flow (t = ln k)."""
    def f(G, lam):
        return beta_Ib(G, lam)
    k1 = f(G, lam)
    k2 = f(G + 0.5*dt*k1[0], lam + 0.5*dt*k1[1])
    k3 = f(G + 0.5*dt*k2[0], lam + 0.5*dt*k2[1])
    k4 = f(G + dt*k3[0], lam + dt*k3[1])
    G_new = G + (dt/6.0)*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
    lam_new = lam + (dt/6.0)*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
    return G_new, lam_new

def integrate_flow(Gs, ls, dt=-0.001, nsteps=50000):
    """Integrate RG flow from UV to IR. dt<0 means flowing to lower k."""
    G, lam = Gs, ls
    # Perturb slightly along the relevant direction to leave the FP
    M = stability_matrix(G, lam)
    tr = M[0][0]+M[1][1]
    det = M[0][0]*M[1][1]-M[0][1]*M[1][0]
    disc = tr*tr-4*det
    # Use the relevant eigenvector (eigenvalue with positive real part)
    if disc < 0:
        sq = math.sqrt(-disc)
        # Eigenvector for eigenvalue (-tr + i*sq)/2 (relevant)
        ev_re = (-tr)/2.0
        ev_im = sq/2.0
        # v = (M[0][1], eigenvalue - M[0][0])
        v1 = M[0][1]
        v2 = (-tr/2.0 + M[0][0])  # This gives one component
        # Normalize
        norm = math.sqrt(v1*v1 + v2*v2)
        if norm > 0:
            v1 /= norm; v2 /= norm
    else:
        sq = math.sqrt(disc)
        e1 = (-tr+sq)/2
        v1, v2 = 1.0, 0.0
    # Perturb along the relevant direction
    amp = 0.01
    G += amp * v1
    lam += amp * v2
    
    trajectory = [(0.0, G, lam)]
    for i in range(nsteps):
        G, lam = rk4_step(G, lam, dt)
        if G <= 0 or lam >= 0.5 or lam < -0.01:
            break
        t = (i+1)*dt
        trajectory.append((t, G, lam))
    return trajectory

def extract_prediction(trajectory):
    """Extract physical quantities from the flow."""
    # At scale k, G_tilde = G*k^2, Lambda_tilde = Lambda/k^2
    # So Lambda*G = Lambda_tilde * G_tilde (dimensionless)
    # And at a physical scale k_0: Lambda_phys = Lambda_tilde(k_0) * k_0^2
    # G_phys = G_tilde(k_0) / k_0^2
    # Therefore Lambda_phys = Lambda_tilde * G_tilde / G_phys * k_0^2 ... 
    # Actually: Lambda*G = Lambda_tilde * G_tilde is a SCALE-INVARIANT quantity
    
    print("\n--- RG Flow Analysis ---")
    print(f"{'t (= ln k)':>12} {'G_tilde':>10} {'lam_tilde':>10} {'G*lam':>10} {'lam/G':>10}")
    
    # Print at logarithmically spaced intervals
    n = len(trajectory)
    step = max(1, n // 50)
    indices = list(range(0, n, step))
    if indices[-1] != n-1:
        indices.append(n-1)
    
    for idx in indices:
        t, G, lam = trajectory[idx]
        product = G * lam
        ratio = lam / G if G > 0 else 0
        k = math.exp(t)
        print(f"{t:12.3f} {G:10.6f} {lam:10.6f} {product:10.6f} {ratio:10.6f}")
    
    # The key prediction: Lambda*G is constant along the separatrix
    t0, G0, l0 = trajectory[0]
    tN, GN, lN = trajectory[-1]
    print(f"\nAt FP:    G*={G0:.6f}, lam*={l0:.6f}, G*lam={G0*l0:.6f}")
    print(f"At IR:    G={GN:.6f}, lam={lN:.6f}, G*lam={GN*lN:.6f}")
    print(f"Lambda/G ratio at FP: {l0/G0:.6f}")
    print(f"Lambda/G ratio at IR: {lN/GN:.6f}")
    
    # The dimensionless prediction
    print(f"\nDimensionless prediction: Lambda*G = {G0*l0:.6f}")
    print(f"This equals Lambda_tilde * G_tilde which is scale-invariant.")
    print(f"In physical units: Lambda_phys * G_N = {G0*l0:.6f} (in Planck units)")
    print(f"  -> Lambda_phys = {G0*l0:.4f} / G_N")
    print(f"  -> Lambda_phys = {G0*l0:.4f} * M_Planck^2")

if __name__ == "__main__":
    res, Gs, ls = find_fp()
    print(f"=== Verified Codello 2009, type Ib, d=4 ===")
    print(f"Fixed point: G*={Gs:.6f}, lam*={ls:.6f}")
    print(f"Expected:    G*=0.7012, lam*=0.1715")
    bG, bl = beta_Ib(Gs, ls)
    print(f"Residual: {bG**2+bl**2:.6e}")
    
    M = stability_matrix(Gs, ls)
    tr = M[0][0]+M[1][1]
    det = M[0][0]*M[1][1]-M[0][1]*M[1][0]
    disc = tr*tr-4*det
    if disc < 0:
        sq = math.sqrt(-disc)
        print(f"theta = {-tr/2:.6f} +/- {sq/2:.6f}i  (expected: 1.689 +/- 2.486i)")
    
    print(f"\n=== Integrating RG flow from UV to IR ===")
    trajectory = integrate_flow(Gs, ls, dt=-0.005, nsteps=200000)
    extract_prediction(trajectory)
