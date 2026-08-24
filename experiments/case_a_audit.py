"""
CASE A AUDIT (fast): does F blow up when Z -> 0?
N=16, RK2, no python-loop nonlinear (vectorized).
"""
import numpy as np
import time as clock

N = 16
dt = 0.001
STEPS = 1500
SAVE_EVERY = 50

ax = np.linspace(0, 2*np.pi, N, endpoint=False)
h = ax[1] - ax[0]
X,Y,Zg = np.meshgrid(ax, ax, ax, indexing="ij")
k1d = np.fft.fftfreq(N, d=h/(2*np.pi))
kx = k1d.reshape(N,1,1); ky = k1d.reshape(1,N,1); kz = k1d.reshape(1,1,N)
k2 = kx**2 + ky**2 + kz**2
k2i = k2.copy(); k2i[0,0,0] = 1; k_inv = 1.0/k2i; k_inv[0,0,0] = 0.0

def project(ux_h, uy_h, uz_h):
    p_h = -k_inv*(1j*kx*ux_h + 1j*ky*uy_h + 1j*kz*uz_h)
    return ux_h-1j*kx*p_h, uy_h-1j*ky*p_h, uz_h-1j*kz*p_h

def nonlinear_h(ux,uy,uz):
    ux_h,uy_h,uz_h = np.fft.fftn(ux),np.fft.fftn(uy),np.fft.fftn(uz)
    ux_x=np.fft.ifftn(1j*kx*ux_h);ux_y=np.fft.ifftn(1j*ky*ux_h);ux_z=np.fft.ifftn(1j*kz*ux_h)
    uy_x=np.fft.ifftn(1j*kx*uy_h);uy_y=np.fft.ifftn(1j*ky*uy_h);uz_z=np.fft.ifftn(1j*kz*uz_h)
    uz_x=np.fft.ifftn(1j*kx*uz_h);uz_y=np.fft.ifftn(1j*ky*uz_h);uy_z=np.fft.ifftn(1j*kz*uy_h)
    ux_z2=ux_z; ux_y2=ux_y; ux_x2=ux_x  # already computed
    fx_h=np.fft.fftn(-(ux*ux_x+uy*ux_y+uz*ux_z))
    fy_h=np.fft.fftn(-(ux*uy_x+uy*uy_y+uz*uy_z))
    fz_h=np.fft.fftn(-(ux*uz_x+uy*uz_y+uz*uz_z))
    px_h=-k_inv*(1j*kx*fx_h+1j*ky*fy_h+1j*kz*fz_h)
    return np.fft.fftn(np.real(np.fft.ifftn(fx_h-1j*kx*px_h))), \
           np.fft.fftn(np.real(np.fft.ifftn(fy_h-1j*ky*px_h))), \
           np.fft.fftn(np.real(np.fft.ifftn(fz_h-1j*kz*px_h)))

def step(ux,uy,uz,nu):
    fx_h,fy_h,fz_h = nonlinear_h(ux,uy,uz)
    ux_h=np.fft.fftn(ux);uy_h=np.fft.fftn(uy);uz_h=np.fft.fftn(uz)
    dx_h = fx_h - nu*k2*ux_h
    dy_h = fy_h - nu*k2*uy_h
    dz_h = fz_h - nu*k2*uz_h
    dx_h[0,0,0]=0;dy_h[0,0,0]=0;dz_h[0,0,0]=0
    ux1,uy1,uz1 = project(ux_h+dt*dx_h, uy_h+dt*dy_h, uz_h+dt*dz_h)
    ux1=np.real(np.fft.ifftn(ux1));uy1=np.real(np.fft.ifftn(uy1));uz1=np.real(np.fft.ifftn(uz1))
    fx1_h,fy1_h,fz1_h = nonlinear_h(ux1,uy1,uz1)
    ux1_h=np.fft.fftn(ux1);uy1_h=np.fft.fftn(uy1);uz1_h=np.fft.fftn(uz1)
    dx1_h = fx1_h - nu*k2*ux1_h
    dy1_h = fy1_h - nu*k2*uy1_h
    dz1_h = fz1_h - nu*k2*uz1_h
    dx1_h[0,0,0]=0;dy1_h[0,0,0]=0;dz1_h[0,0,0]=0
    ux2,uy2,uz2 = project(ux_h+0.5*dt*(dx_h+dx1_h), uy_h+0.5*dt*(dy_h+dy1_h), uz_h+0.5*dt*(dz_h+dz1_h))
    return np.real(np.fft.ifftn(ux2)),np.real(np.fft.ifftn(uy2)),np.real(np.fft.ifftn(uz2))

def metrics(ux,uy,uz):
    u2=ux**2+uy**2+uz**2; vol=(2*np.pi)**3
    u_inf=float(np.max(np.sqrt(u2)))
    E=float(np.sum(u2)*h**3/(2*vol))
    Z=sum(float(np.sum(k2*abs(np.fft.fftn(c))**2))*h**3/vol for c in [ux,uy,uz])
    L2=np.sqrt(2*max(E,1e-30));gZ=np.sqrt(max(Z,1e-30))
    F=u_inf/(L2**0.5*gZ**0.5) if min(L2,gZ)>1e-30 else 0
    return E, Z, u_inf, F

# Poloidal IC
cx=cy=cz=np.pi; R=0.5
r2=(X-cx)**2+(Y-cy)**2+(Zg-cz)**2
w=np.exp(-r2/(2*R**2)); wh=np.fft.fftn(w)
pux=np.real(np.fft.ifftn(-kx*kz*wh))
puy=np.real(np.fft.ifftn(-ky*kz*wh))
puz=np.real(np.fft.ifftn(-(kx**2+ky**2)*wh))

E0,Z0,_,_ = metrics(pux,puy,puz)
print("CASE A AUDIT: F vs Z as solution decays")
print(f"IC: E0={E0:.6f} Z0={Z0:.2f}")
print("="*75)

for nu in [0.5, 0.05, 0.0]:
    ux,uy,uz=pux.copy(),puy.copy(),puz.copy()
    tag = f"nu={nu}" + (" EULER" if nu==0 else "")
    print(f"\n--- {tag} ---")
    F_max=0; t0=clock.time()
    traj = []
    dead=False

    for s in range(1, STEPS+1):
        ux,uy,uz=step(ux,uy,uz,nu)
        if np.any(np.isnan(ux)) or np.max(np.abs(ux))>1e4:
            print(f"  DIVERGED at t={s*dt:.2f}"); dead=True; break
        if s % SAVE_EVERY == 0:
            E,Z,u_inf,F = metrics(ux,uy,uz)
            traj.append((s*dt, E, Z, u_inf, F))
            if F > F_max: F_max = F

    if not dead and traj:
        print(f"  [{clock.time()-t0:.1f}s]")
        print(f"  {'t':>5} {'E':>10} {'Z':>10} {'u_inf':>7} {'F':>6} {'F/E^0.25/Z^0.25':>16}")
        for row in traj[:3]:
            print(f"  {row[0]:5.2f} {row[1]:10.6f} {row[2]:10.4f} {row[3]:7.4f} {row[4]:6.4f} {row[4]:16.4f}")
        print(f"  {'...':>5}")
        for row in traj[-5:]:
            print(f"  {row[0]:5.2f} {row[1]:10.6f} {row[2]:10.4f} {row[3]:7.4f} {row[4]:6.4f} {row[4]:16.4f}")
        print(f"  F_max={F_max:.4f}")
        if nu==0:
            E_ratio = traj[-1][1]/traj[0][1]
            print(f"  Energy: {traj[0][1]:.6f} -> {traj[-1][1]:.6f} (ratio={E_ratio:.4f})")
        print(f"  => {'F BOUNDED (proof gap non-issue)' if F_max<1.0 else 'F EXCEEDS 1'}")

print("\n" + "="*75)
print("If F blows up at nu=0 but bounded at nu>0:")
print("  => temperature difference IS the mechanism")
print("  => Case A gap closes because viscous term damps u_inf faster than Z decays")
