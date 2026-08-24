"""
BOUNCING: minimal test. 2 configs only.
"""
import numpy as np, time as clock

N = 32; dt = 0.0003; STEPS = 1500; SAVE_EVERY = 10
ax = np.linspace(0, 2*np.pi, N, endpoint=False)
h = ax[1]-ax[0]; X,Y,Zg = np.meshgrid(ax,ax,ax,indexing="ij")
k1d = np.fft.fftfreq(N,d=h/(2*np.pi))
kx=k1d.reshape(N,1,1); ky=k1d.reshape(1,N,1); kz=k1d.reshape(1,1,N)
k2=kx**2+ky**2+kz**2
k2i=k2.copy(); k2i[0,0,0]=1; k_inv=1.0/k2i; k_inv[0,0,0]=0

def project(ux,uy,uz):
    ux_h,uy_h,uz_h=np.fft.fftn(ux),np.fft.fftn(uy),np.fft.fftn(uz)
    p_h=-k_inv*(1j*kx*ux_h+1j*ky*uy_h+1j*kz*uz_h)
    return(np.real(np.fft.ifftn(ux_h-1j*kx*p_h)),np.real(np.fft.ifftn(uy_h-1j*ky*p_h)),np.real(np.fft.ifftn(uz_h-1j*kz*p_h)))

def step(ux,uy,uz,nu):
    ux_h=np.fft.fftn(ux);uy_h=np.fft.fftn(uy);uz_h=np.fft.fftn(uz)
    ux_x=np.real(np.fft.ifftn(1j*kx*ux_h));ux_y=np.real(np.fft.ifftn(1j*ky*ux_h));ux_z=np.real(np.fft.ifftn(1j*kz*ux_h))
    uy_x=np.real(np.fft.ifftn(1j*kx*uy_h));uy_y=np.real(np.fft.ifftn(1j*ky*uy_h));uy_z=np.real(np.fft.ifftn(1j*kz*uy_h))
    uz_x=np.real(np.fft.ifftn(1j*kx*uz_h));uz_y=np.real(np.fft.ifftn(1j*ky*uz_h));uz_z=np.real(np.fft.ifftn(1j*kz*uz_h))
    nx_h=np.fft.fftn(-(ux*ux_x+uy*ux_y+uz*uz_z));ny_h=np.fft.fftn(-(ux*uy_x+uy*uy_y+uz*uy_z));nz_h=np.fft.fftn(-(ux*uz_x+uy*uz_y+uz*uz_z))
    p_h=-k_inv*(1j*kx*nx_h+1j*ky*ny_h+1j*kz*nz_h)
    return project(ux+dt*np.real(np.fft.ifftn(nx_h-1j*kx*p_h-nu*k2*ux_h)),
                   uy+dt*np.real(np.fft.ifftn(ny_h-1j*ky*p_h-nu*k2*uy_h)),
                   uz+dt*np.real(np.fft.ifftn(nz_h-1j*kz*p_h-nu*k2*uz_h)))

def gn14(ux,uy,uz):
    u2=ux**2+uy**2+uz**2; vol=(2*np.pi)**3; u_inf=float(np.max(np.sqrt(u2)))
    E=float(np.sum(u2)*h**3/(2*vol)); Z=sum(float(np.sum(k2*(np.fft.fftn(c).real**2+np.fft.fftn(c).imag**2)))*h**3/vol for c in [ux,uy,uz])
    L2=np.sqrt(2*max(E,1e-30));gL2=np.sqrt(max(Z,1e-30))
    return u_inf/(L2**0.5*gL2**0.5) if min(L2,gL2)>1e-30 else 0

# Config 1: poloidal R=0.5, nu=0.05 (weak viscosity = nonlinear has time to fight back)
cx=cy=cz=np.pi; R=0.5
r2=(X-cx)**2+(Y-cy)**2+(Zg-cz)**2
w=np.exp(-r2/(2*R**2)); w_hat=np.fft.fftn(w)
pux=np.real(np.fft.ifftn(-kx*kz*w_hat)); puy=np.real(np.fft.ifftn(-ky*kz*w_hat)); puz=np.real(np.fft.ifftn(-(kx**2+ky**2)*w_hat))
ux,uy,uz=project(pux,puy,puz)

print("Poloidal R=0.5, nu=0.05 (weak viscosity)")
g0=gn14(ux,uy,uz); print(f"  t=0.000: gn14={g0:.6f}")
prev_g = g0; ups=0; downs=0; peaks=[]; t0=clock.time()
for s in range(1,STEPS+1):
    ux,uy,uz=step(ux,uy,uz,0.05)
    if np.any(np.isnan(ux)): print("  DIVERGED"); break
    if s%SAVE_EVERY==0:
        g=gn14(ux,uy,uz); t=s*dt
        if g>prev_g: ups+=1
        else: downs+=1
        prev_g=g
        if s<=200 or s%200==0 or s>=STEPS-200:
            print(f"  t={t:.3f}: gn14={g:.6f}")
print(f"  [{clock.time()-t0:.1f}s] ups={ups} downs={downs}")

# Config 2: poloidal R=0.5, nu=0.01 (very weak viscosity)
ux2,uy2,uz2=project(pux.copy(),puy.copy(),puz.copy())
print()
print("Poloidal R=0.5, nu=0.01 (very weak viscosity)")
g0=gn14(ux2,uy2,uz2); print(f"  t=0.000: gn14={g0:.6f}")
prev_g=g0; ups=0; downs=0; t0=clock.time()
for s in range(1,STEPS+1):
    ux2,uy2,uz2=step(ux2,uy2,uz2,0.01)
    if np.any(np.isnan(ux2)): print("  DIVERGED"); break
    if s%SAVE_EVERY==0:
        g=gn14(ux2,uy2,uz2); t=s*dt
        if g>prev_g: ups+=1
        else: downs+=1
        prev_g=g
        if s<=200 or s%200==0 or s>=STEPS-200:
            print(f"  t={t:.3f}: gn14={g:.6f}")
print(f"  [{clock.time()-t0:.1f}s] ups={ups} downs={downs}")

# Config 3: TG at nu=0.05 (should be nearly flat)
ux3=np.sin(X)*np.cos(Y)*np.cos(Zg)
uy3=-np.cos(X)*np.sin(Y)*np.cos(Zg)
uz3=np.zeros_like(X)
ux3,uy3,uz3=project(ux3,uy3,uz3)
print()
print("Taylor-Green, nu=0.05")
g0=gn14(ux3,uy3,uz3); print(f"  t=0.000: gn14={g0:.6f}")
prev_g=g0; ups=0; downs=0; t0=clock.time()
for s in range(1,STEPS+1):
    ux3,uy3,uz3=step(ux3,uy3,uz3,0.05)
    if np.any(np.isnan(ux3)): print("  DIVERGED"); break
    if s%SAVE_EVERY==0:
        g=gn14(ux3,uy3,uz3); t=s*dt
        if g>prev_g: ups+=1
        else: downs+=1
        prev_g=g
        if s<=200 or s%200==0 or s>=STEPS-200:
            print(f"  t={t:.3f}: gn14={g:.6f}")
print(f"  [{clock.time()-t0:.1f}s] ups={ups} downs={downs}")
