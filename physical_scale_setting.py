"""
Physical scale setting: derive k <-> cosmic time from Friedmann equation.

Key identities:
  G_tilde = G(k) * k^2     (dimensionless Newton constant)
  Lambda_tilde = Lambda(k) / k^2  (dimensionless cosmological constant)

Friedmann equation in terms of dimensionless couplings:
  H^2 = (k^2 / 3) * (8*pi*G_tilde + Lambda_tilde)

RG time t_RG = ln(k/k_0), so dk/dt_RG = k.
Cosmic time: dk/dt_cosmic = -k*H  (k decreases as universe expands)

Combined: dt_cosmic/dt_RG = -k/(dk/dt_RG) * dk/dt_cosmic ... wrong.

Actually: dk/dt_cosmic = -k*H  =>  dk/d(ln k) * d(ln k)/dt_cosmic = -k*H
  =>  k * d(ln k)/dt_cosmic = -k*H
  =>  d(ln k)/dt_cosmic = -H
  =>  dt_cosmic = -d(ln k)/H = -dt_RG * k / (k*H) = -dt_RG / H

Wait, that gives dt_cosmic = -dt_RG / H. But H is dimensionful.
Let me redo carefully.

In natural units (hbar = c = 1):
  t_RG = ln(k / k_0)  (dimensionless)
  t_cosmic has dimensions of [energy]^{-1}

  dk/dt_cosmic = -k * H    ... (1)
  dk/dt_RG = k             ... (2)

From (2): dk = k * dt_RG
Sub into (1): k * dt_RG / dt_cosmic = -k * H
  => dt_cosmic/dt_RG = -1/H

H has dimensions of [energy] (since H = (da/dt)/a, and both a and t have 
dimensions, but in natural units H ~ [energy]).

H^2 = (k^2 / 3) * (8*pi*G_tilde + Lambda_tilde)

So H = k * sqrt((8*pi*G_tilde + Lambda_tilde) / 3)

Therefore: dt_cosmic/dt_RG = -1 / (k * sqrt((8*pi*G_tilde + Lambda_tilde)/3))

And the scale factor: da/dt_cosmic = H*a => d(ln a)/dt_cosmic = H
  => d(ln a)/dt_RG = H * dt_cosmic/dt_RG = -1

So ln(a) = -t_RG + const = -ln(k/k_0) + const = ln(k_0/k) + const
  => a ~ k_0/k  (scale factor inversely proportional to RG scale)

This is the standard result: k ~ 1/a (comoving energy scale).

The physical cosmological constant at cosmic time t:
  Lambda_phys(t) = Lambda_tilde(k(t)) * k(t)^2

And physical Newton constant:
  G_phys(t) = G_tilde(k(t)) / k(t)^2

We integrate the coupled system:
  dG_tilde/dt_RG = beta_G(G_tilde, Lambda_tilde)
  dLambda_tilde/dt_RG = beta_Lambda(G_tilde, Lambda_tilde)
  dt_cosmic/dt_RG = -1 / (k_0 * exp(t_RG) * sqrt((8*pi*G_tilde + Lambda_tilde)/3))

Starting from near the FP (t_RG large) and flowing to IR (t_RG decreasing).
"""
import math
import sys
sys.path.insert(0, 'C:/Users/Me/Downloads/Puno_Calculus')
from litim_flow import beta_Ib, find_fp, stability_matrix, rk4_step

# Constants
M_Planck_GeV = 1.2209e19   # Planck mass in GeV
G_N_SI = 6.674e-11         # Newton constant in SI
M_Planck_kg = 2.176e-8     # Planck mass in kg
c = 2.998e8                # speed of light m/s
hbar = 1.055e-34           # Planck constant J*s
G_eV = 6.709e-39           # Newton constant in GeV^{-2}

def hubble(G_tilde, L_tilde, k):
    """Hubble parameter H = k * sqrt((8*pi*G_tilde + L_tilde)/3)."""
    val = 8.0*math.pi*G_tilde + L_tilde
    if val < 0:
        return 0.0
    return k * math.sqrt(val / 3.0)

def coupled_flow(t_RG, G_t, L_t, k):
    """Combined RG + cosmic flow. Returns (dG/dt_RG, dL/dt_RG, dt_cosmic/dt_RG)."""
    bG, bL = beta_Ib(G_t, L_t)
    H = hubble(G_t, L_t, k)
    if H < 1e-30:
        dt_cosmic = 0.0
    else:
        dt_cosmic = -1.0 / H
    return bG, bL, dt_cosmic

def integrate_with_cosmic_time(k_start_GeV, G_t0, L_t0, dt_RG=-0.01, nsteps=200000):
    """
    Integrate from high k to low k.
    k_start_GeV: starting RG scale in GeV
    G_t0, L_t0: starting values of dimensionless couplings
    """
    pi = math.pi
    k = k_start_GeV
    G_t, L_t = G_t0, L_t0
    t_RG = 0.0
    t_cosmic = 0.0
    
    # Storage
    results = []
    
    for i in range(nsteps):
        k = k_start_GeV * math.exp(t_RG)
        
        # Store
        H = hubble(G_t, L_t, k)
        G_phys = G_t / k**2 if k > 0 else 0
        L_phys = L_t * k**2 if k > 0 else 0
        results.append({
            't_RG': t_RG,
            'k_GeV': k,
            'G_tilde': G_t,
            'L_tilde': L_t,
            'G_phys_GeV2': G_phys,
            'L_phys_GeV2': L_phys,
            'H_GeV': H,
            't_cosmic_s': t_cosmic,
            'a_over_a0': k_start_GeV / k if k > 0 else 0,
        })
        
        # RK4 step for RG flow
        G_new, L_new = rk4_step(G_t, L_t, dt_RG)
        
        if G_new <= 0 or L_new >= 0.5 or L_new < -0.5:
            break
        
        # Cosmic time step
        H_mid = hubble(G_new, L_new, k_start_GeV * math.exp(t_RG + 0.5*dt_RG))
        if H_mid > 1e-30:
            dt_cosmic_step = -dt_RG / H_mid  # dt_cosmic/dt_RG = -1/H
            t_cosmic += dt_cosmic_step
        
        G_t, L_t = G_new, L_new
        t_RG += dt_RG
        
        # Stop if k is too small
        if k < 1e-2:
            break
    
    return results

def geV_to_seconds(GeV):
    """Convert energy in GeV to time in seconds via natural units."""
    # hbar = 6.582e-25 GeV*s
    return 6.582e-25 / GeV if GeV > 0 else float('inf')

def geV2_to_m2(GeV2):
    """Convert GeV^2 to m^{-2} (for Lambda)."""
    # 1 GeV = 5.068e15 m^{-1}, so 1 GeV^2 = 2.568e31 m^{-2}
    return GeV2 * 2.568e31

if __name__ == "__main__":
    res, Gs, ls = find_fp()
    print(f"=== Physical Scale Setting ===")
    print(f"FP: G*={Gs:.6f}, L*={ls:.6f}, G*L*={Gs*ls:.6f}")
    
    # Start near FP at high k, flow to low k
    # Perturb slightly from FP along relevant direction
    M = stability_matrix(Gs, ls)
    tr = M[0][0]+M[1][1]
    v1 = M[0][1]; v2 = (-tr/2.0 + M[0][0])
    norm = math.sqrt(v1*v1 + v2*v2)
    if norm > 0: v1 /= norm; v2 /= norm
    amp = 0.005
    G0 = Gs + amp*v1
    L0 = ls + amp*v2
    
    # Start at k = 10^19 GeV (near Planck scale)
    k_start = 1e19
    results = integrate_with_cosmic_time(k_start, G0, L0, dt_RG=-0.01, nsteps=500000)
    
    print(f"\nIntegrated {len(results)} steps")
    print(f"\n{'k (GeV)':>12} {'G_tilde':>10} {'L_tilde':>10} {'G*L':>10} {'G_phys (GeV-2)':>16} {'L_phys (GeV2)':>16} {'L_phys (m-2)':>16} {'t_cosmic (s)':>14}")
    print("-" * 120)
    
    # Print at logarithmically spaced points
    n = len(results)
    for p in [0, 0.001, 0.01, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.95, 1.0]:
        idx = min(int(n * p), n-1)
        r = results[idx]
        k = r['k_GeV']
        t_s = geV_to_seconds(k)
        L_m2 = geV2_to_m2(r['L_phys_GeV2'])
        print(f"{k:12.2e} {r['G_tilde']:10.6f} {r['L_tilde']:10.6f} {r['G_tilde']*r['L_tilde']:10.6f} "
              f"{r['G_phys_GeV2']:16.6e} {r['L_phys_GeV2']:16.6e} {L_m2:16.6e} {r['t_cosmic_s']:14.6e}")
    
    # Final values
    r = results[-1]
    print(f"\n=== Final values ===")
    print(f"k_final = {r['k_GeV']:.2e} GeV")
    print(f"G_tilde = {r['G_tilde']:.6f}")
    print(f"L_tilde = {r['L_tilde']:.6f}")
    print(f"G_phys = {r['G_phys_GeV2']:.6e} GeV^-2")
    print(f"L_phys = {r['L_phys_GeV2']:.6e} GeV^2 = {geV2_to_m2(r['L_phys_GeV2']):.6e} m^-2")
    print(f"Observed L = 1.06e-52 m^-2")
    
    if r['L_phys_GeV2'] != 0:
        ratio = abs(geV2_to_m2(r['L_phys_GeV2'])) / 1.06e-52
        print(f"|Predicted| / Observed = {ratio:.2e}")
    
    print(f"\nCosmic time elapsed: {r['t_cosmic_s']:.6e} seconds")
    print(f"Scale factor ratio a/a_0 = {r['a_over_a0']:.6e}")
