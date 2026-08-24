"""
Fast NS evolution: does viscous damping crush concentration?
Uses N=32, forward Euler, small R values only.
Just need qualitative answer: does gn14 go up or down under NS?
"""
import numpy as np
import time as clock

N = 32
nu = 1.0
dt = 0.00005
STEPS = 2000
SAVE_EVERY = 100

ax = np.linspace(0, 2*np.pi, N, endpoint=False)
h = ax[1] - ax[0]
X, Y, Zg = np.meshgrid(ax, ax, ax, indexing="ij")
cx = cy = cz = np.pi

k1d = np.fft.fftfreq(N, d=h/(2*np.pi))
kx = k1d.reshape(N,1,1)
ky = k1d.reshape(1,N,1)
kz = k1d.reshape(1,1,N)
k2 = kx**2 + ky**2 + kz**2
k2i = k2.copy(); k2i[0,0,0] = 1.0; k_inv = 1.0/k2i; k_inv[0,0,0] = 0.0

def make_poloidal(R):
    r2 = (X-cx)**2 + (Y-cy)**2 + (Zg-cz)**2
    w = np.exp(-r2 / (2*R**2))
    w_hat = np.fft.fftn(w)
    ux = np.real(np.fft.ifftn(-kx*kz*w_hat))
    uy = np.real(np.fft.ifftn(-ky*kz*w_hat))
    uz = np.real(np.fft.ifftn(-(kx**2+ky**2)*w_hat))
    return ux, uy, uz

def project(ux, uy, uz):
    ux_h,uy_h,uz_h = np.fft.fftn(ux), np.fft.fftn(uy), np.fft.fftn(uz)
    div_h = 1j*kx*ux_h + 1j*ky*uy_h + 1j*kz*uz_h
    p_h = -k_inv * div_h
    return (np.real(np.fft.ifftn(ux_h - 1j*kx*p_h)),
            np.real(np.fft.ifftn(uy_h - 1j*ky*p_h)),
            np.real(np.fft.ifftn(uz_h - 1j*kz*p_h)))

def step(ux, uy, uz):
    ux_h = np.fft.fftn(ux); uy_h = np.fft.fftn(uy); uz_h = np.fft.fftn(uz)
    ux_x = np.real(np.fft.ifftn(1j*kx*ux_h)); ux_y = np.real(np.fft.ifftn(1j*ky*ux_h)); ux_z = np.real(np.fft.ifftn(1j*kz*ux_h))
    uy_x = np.real(np.fft.ifftn(1j*kx*uy_h)); uy_y = np.real(np.fft.ifftn(1j*ky*uy_h)); uy_z = np.real(np.fft.ifftn(1j*kz*uy_h))
    uz_x = np.real(np.fft.ifftn(1j*kx*uz_h)); uz_y = np.real(np.fft.ifftn(1j*ky*uz_h)); uz_z = np.real(np.fft.ifftn(1j*kz*uz_h))

    nx_h = np.fft.fftn(-(ux*ux_x + uy*ux_y + uz*ux_z))
    ny_h = np.fft.fftn(-(ux*uy_x + uy*uy_y + uz*uy_z))
    nz_h = np.fft.fftn(-(ux*uz_x + uy*uz_y + uz*uz_z))

    div_h = 1j*kx*nx_h + 1j*ky*ny_h + 1j*kz*nz_h
    p_h = -k_inv * div_h

    ux_new = ux + dt*(np.real(np.fft.ifftn(nx_h - 1j*kx*p_h - nu*k2*ux_h)))
    uy_new = uy + dt*(np.real(np.fft.ifftn(ny_h - 1j*ky*p_h - nu*k2*uy_h)))
    uz_new = uz + dt*(np.real(np.fft.ifftn(nz_h - 1j*kz*p_h - nu*k2*uz_h)))
    return project(ux_new, uy_new, uz_new)

def metrics(ux, uy, uz):
    u2 = ux**2 + uy**2 + uz**2
    vol = (2*np.pi)**3
    u_inf = float(np.max(np.sqrt(u2)))
    E = float(np.sum(u2)*h**3 / (2*vol))
    Z = sum(float(np.sum(k2*(np.fft.fftn(c).real**2+np.fft.fftn(c).imag**2)))*h**3/vol for c in [ux,uy,uz])
    r2 = (X-cx)**2+(Y-cy)**2+(Zg-cz)**2
    r_eff = float(np.sqrt(np.sum(r2*u2)/max(np.sum(u2),1e-30)))
    L2 = np.sqrt(2*max(E,1e-30)); gL2 = np.sqrt(max(Z,1e-30))
    gn14 = u_inf/(L2**0.5*gL2**0.5) if min(L2,gL2)>1e-30 else 0
    return E, Z, u_inf, r_eff, gn14

print(f"N={N} nu={nu} dt={dt} steps={STEPS} T_max={STEPS*dt:.3f}")
print()

for R in [2.0, 1.0, 0.5]:
    print(f"--- R_init = {R} ---")
    ux, uy, uz = make_poloidal(R)
    ux, uy, uz = project(ux, uy, uz)
    m = metrics(ux, uy, uz)
    print(f"  t=0.000: E={m[0]:.6f} Z={m[1]:.4f} r_eff={m[3]:.4f} u_inf={m[2]:.4f} gn14={m[4]:.4f}")

    t0 = clock.time()
    diverged = False
    for s in range(1, STEPS+1):
        ux, uy, uz = step(ux, uy, uz)
        if np.any(np.isnan(ux)):
            print(f"  DIVERGED at step {s} t={s*dt:.4f}")
            diverged = True
            break
        if s % SAVE_EVERY == 0:
            m = metrics(ux, uy, uz)
            print(f"  t={s*dt:.4f}: E={m[0]:.6f} Z={m[1]:.4f} r_eff={m[3]:.4f} u_inf={m[2]:.4f} gn14={m[4]:.4f}")

    if not diverged:
        m = metrics(ux, uy, uz)
        print(f"  FINAL: gn14 = {m[4]:.4f}")
    print(f"  [{clock.time()-t0:.1f}s]")
    print()
