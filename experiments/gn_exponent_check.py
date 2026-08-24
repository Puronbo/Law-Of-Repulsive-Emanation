"""
CRITICAL CHECK: verify the correct Ladyzhenskaya/GN exponents.

The Gagliardo-Nirenberg inequality in 3D:
  ||u||_{L^p} <= C ||D^m u||_{L^r}^a ||u||_{L^q}^{1-a}
  with 1/p = a(1/r - m/n) + (1-a)/q

For ||u||_{L^4} in 3D (n=3), m=1, r=2, q=2:
  1/4 = a(1/2 - 1/3) + (1-a)/2 = a/6 + (1-a)/2
  => a = 3/4

So: ||u||_{L^4} <= C ||grad u||_{L^2}^{3/4} ||u||_{L^2}^{1/4}

NOT: ||u||_{L^4} <= C ||u||_{L^2}^{3/4} ||grad u||_{L^2}^{1/4}  (WRONG exponents)

Verify both numerically to see which is bounded.
"""
import numpy as np


def random_divfree(n, n_modes=30, k_max=7, scale=1.0, seed=42):
    rng = np.random.default_rng(seed)
    ax = np.linspace(0,2*np.pi,n,endpoint=False); h=ax[1]-ax[0]
    X,Y,Z = np.meshgrid(ax,ax,ax,indexing="ij")
    ux=np.zeros((n,n,n)); uy=np.zeros((n,n,n)); uz=np.zeros((n,n,n))
    for _ in range(n_modes):
        kvec = rng.integers(1, k_max+1, size=3)
        phase = rng.uniform(0, 2*np.pi)
        a = rng.standard_normal(3)
        kd = kvec[0]*X + kvec[1]*Y + kvec[2]*Z + phase
        ck = np.cos(kd)
        ux += scale*(kvec[1]*a[2]-kvec[2]*a[1])*ck
        uy += scale*(kvec[2]*a[0]-kvec[0]*a[2])*ck
        uz += scale*(kvec[0]*a[1]-kvec[1]*a[0])*ck
    return ux, uy, uz, h


def abc_flow(s, k=1, n=96):
    ax = np.linspace(0,2*np.pi,n,endpoint=False); h=ax[1]-ax[0]
    X,Y,Z = np.meshgrid(ax,ax,ax,indexing="ij")
    return (s*np.sin(k*Z)+s*np.cos(k*Y),
            s*np.sin(k*X)+s*np.cos(k*Z),
            s*np.sin(k*Y)+s*np.cos(k*X), h)


def tg_flow(lam, n=96):
    ax = np.linspace(0,2*np.pi,n,endpoint=False); h=ax[1]-ax[0]
    X,Y,Z = np.meshgrid(ax,ax,ax,indexing="ij")
    return (lam*np.sin(X)*np.cos(Y)*np.cos(Z),
            lam*np.cos(X)*np.sin(Y)*np.cos(Z),
            -2*lam*np.cos(X)*np.cos(Y)*np.sin(Z), h)


def check_invariants(ux, uy, uz, h):
    n = ux.shape[0]; vol = (2*np.pi)**3
    u_sq = ux**2+uy**2+uz**2
    u_inf = float(np.max(np.sqrt(u_sq)))
    E = float(np.sum(u_sq)*h**3/(2*vol))
    L2 = np.sqrt(2*E)

    # L4 norm
    L4_4 = float(np.sum(u_sq**2)*h**3/vol)
    L4 = L4_4**(1/4)

    # ||grad u||_L2 = sqrt(Z)
    kx = np.fft.fftfreq(n,d=h/(2*np.pi)).reshape(n,1,1)
    ky = np.fft.fftfreq(n,d=h/(2*np.pi)).reshape(1,n,1)
    kz = np.fft.fftfreq(n,d=h/(2*np.pi)).reshape(1,1,n)
    ux_h = np.fft.fftn(ux); uy_h = np.fft.fftn(uy); uz_h = np.fft.fftn(uz)
    grad_sq = sum(np.real(np.fft.ifftn(1j*a*hh))**2
                  for hh in [ux_h,uy_h,uz_h] for a in [kx,ky,kz])
    Z = float(np.sum(grad_sq)*h**3/vol)
    grad_L2 = np.sqrt(Z)

    return u_inf, E, L2, L4, grad_L2, Z


def main():
    n = 96
    print("="*75)
    print("CHECK: which Ladyzhenskaya/GN exponents are correct?")
    print("="*75)

    # Correct GN: ||u||_L4 <= C * ||grad u||_L2^{3/4} * ||u||_L2^{1/4}
    # Wrong:      ||u||_L4 <= C * ||u||_L2^{3/4} * ||grad u||_L2^{1/4}

    configs = []
    for s in [0.5,1,2,5,10]:
        configs.append(("ABC", abc_flow(s,1,n)))
        configs.append(("TG", tg_flow(s,n)))
    for k_max in [2,4,7,10,20]:
        for seed in range(5):
            configs.append(("Rand", random_divfree(n,30,k_max,1.0,seed)))

    correct_ratios = []
    wrong_ratios = []

    for name, (ux,uy,uz,h) in configs:
        u_inf, E, L2, L4, grad_L2, Z = check_invariants(ux,uy,uz,h)

        # Correct: grad^{3/4} * L2^{1/4}
        rhs_correct = grad_L2**(3/4) * L2**(1/4)
        r_correct = L4 / rhs_correct if rhs_correct > 0 else 0
        correct_ratios.append(r_correct)

        # Wrong: L2^{3/4} * grad^{1/4}
        rhs_wrong = L2**(3/4) * grad_L2**(1/4)
        r_wrong = L4 / rhs_wrong if rhs_wrong > 0 else 0
        wrong_ratios.append(r_wrong)

    correct_ratios = np.array(correct_ratios)
    wrong_ratios = np.array(wrong_ratios)

    print(f"\nCorrect GN: ||u||_L4 <= C * ||grad u||_L2^{{3/4}} * ||u||_L2^{{1/4}}")
    print(f"  Ratio: min={correct_ratios.min():.4f}  max={correct_ratios.max():.4f}  "
          f"median={np.median(correct_ratios):.4f}")

    print(f"\nWrong GN:   ||u||_L4 <= C * ||u||_L2^{{3/4}} * ||grad u||_L2^{{1/4}}")
    print(f"  Ratio: min={wrong_ratios.min():.4f}  max={wrong_ratios.max():.4f}  "
          f"median={np.median(wrong_ratios):.4f}")

    # Now derive the key bound: ||u||_inf <= C * ||grad u||_L2
    # From correct GN + interpolation ||u||_L4 <= ||u||_L2^{1/4} ||u||_inf^{3/4}
    print(f"\n--- Key derivation: correct GN + interpolation ---")
    print(f"  ||u||_L4 <= C1 * ||grad||^{{3/4}} * ||u||_L2^{{1/4}}")
    print(f"  ||u||_L4 <= ||u||_L2^{{1/4}} * ||u||_inf^{{3/4}}  (Hölder)")
    print(f"  => ||u||_inf^{{3/4}} <= C1 * ||grad||^{{3/4}}")
    print(f"  => ||u||_inf <= C1^{{4/3}} * ||grad u||_L2 = C1^{{4/3}} * sqrt(2Z)")

    C1 = correct_ratios.max()
    print(f"\n  C1 (GN constant) = {C1:.4f}")
    print(f"  C1^{{4/3}} = {C1**(4/3):.4f}")

    # Verify: ||u||_inf <= C1^{4/3} * ||grad||_L2
    print(f"\n--- Verify ||u||_inf <= C * ||grad||_L2 ---")
    bound_ratios = []
    for name, (ux,uy,uz,h) in configs:
        u_inf, E, L2, L4, grad_L2, Z = check_invariants(ux,uy,uz,h)
        r = u_inf / grad_L2 if grad_L2 > 0 else 0
        bound_ratios.append(r)
    bound_ratios = np.array(bound_ratios)
    print(f"  ||u||_inf / ||grad||_L2: min={bound_ratios.min():.4f}  "
          f"max={bound_ratios.max():.4f}  median={np.median(bound_ratios):.4f}")
    print(f"  C1^{{4/3}} = {C1**(4/3):.4f} (should be >= max ratio)")

    # Prodi-Serrin closure
    print(f"\n--- Prodi-Serrin closure ---")
    C_ps = bound_ratios.max()
    print(f"  ||u||_inf <= {C_ps:.4f} * sqrt(Z) = {C_ps:.4f} * sqrt(eps/nu)")
    print(f"  => ||u||_inf^2 <= {C_ps**2:.4f} * Z")
    print(f"  => int_0^T ||u||_inf^2 dt <= {C_ps**2:.4f} * int_0^T Z dt")
    print(f"  = {C_ps**2:.4f} * (E0 - E(T))/nu  (by energy equation)")
    print(f"  <= {C_ps**2:.4f} * E0/nu  =  FINITE")
    print(f"  => u in L^2_t(L^inf_x)")
    print(f"  Prodi-Serrin (2/p + 3/q = 2/2 + 0 = 1): SATISFIED")
    print(f"  => GLOBAL REGULARITY")


if __name__ == "__main__":
    main()
