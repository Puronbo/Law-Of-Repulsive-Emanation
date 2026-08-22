"""
Approach the separatrix from the NGFP side.
Since the NGFP has complex eigenvalues, all trajectories spiral outward.
We use bisection to find the specific angle that lands closest to GFP (G=0,L=0).
"""
import math, sys
sys.path.insert(0, 'C:/Users/Me/Downloads/Puno_Calculus')
from litim_flow import beta_Ib, find_fp

res, Gs, ls = find_fp()
print(f"NGFP: G*={Gs:.6f}, L*={ls:.6f}")

def flow_ir(G0, L0, dt=-0.005, nsteps=200000):
    G, L = G0, L0
    min_dist = math.sqrt(G**2 + L**2)
    min_point = (G, L)
    for i in range(nsteps):
        def f(g, l): return beta_Ib(g, l)
        k1 = f(G, L)
        k2 = f(G+0.5*dt*k1[0], L+0.5*dt*k1[1])
        k3 = f(G+0.5*dt*k2[0], L+0.5*dt*k2[1])
        k4 = f(G+dt*k3[0], L+dt*k3[1])
        G += (dt/6)*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        L += (dt/6)*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        if G<=0 or L>=0.5 or L<0 or G>10:
            return min_dist, min_point, i, False
        d = math.sqrt(G**2 + L**2)
        if d < min_dist:
            min_dist = d
            min_point = (G, L)
    return min_dist, min_point, nsteps, True

# Phase angle around the NGFP
# Start at G*+eps*cos(angle), L*+eps*sin(angle) for small eps
eps = 0.001
print(f"\nCoarse scan (eps={eps}), dt=-0.005:")
print(f"{'angle':>8} {'min_G':>10} {'min_L':>10} {'min_dist':>10} {'steps':>8} {'bounded':>8}")

best_angle = 0
best_d = 1e30
for i in range(360):
    angle = i * math.pi / 180
    G0 = Gs + eps * math.cos(angle)
    L0 = ls + eps * math.sin(angle)
    if G0 <= 0 or L0 <= 0 or L0 >= 0.5:
        continue
    d, pt, steps, ok = flow_ir(G0, L0, dt=-0.005, nsteps=100000)
    if i % 15 == 0:
        print(f"{angle*180/math.pi:8.1f} {pt[0]:10.6f} {pt[1]:10.6f} {d:10.6f} {steps:8d} {'yes' if ok else 'NO':>8}")
    if d < best_d:
        best_d = d
        best_angle = angle

print(f"\nBest angle: {best_angle*180/math.pi:.1f} deg, min dist to origin: {best_d:.6f}")

# Fine scan around best angle
print(f"\nFine scan around {best_angle*180/math.pi:.1f} deg:")
for i in range(-20, 21):
    angle = best_angle + i * math.pi / 3600  # 0.05 deg steps
    G0 = Gs + eps * math.cos(angle)
    L0 = ls + eps * math.sin(angle)
    if G0 <= 0 or L0 <= 0 or L0 >= 0.5:
        continue
    d, pt, steps, ok = flow_ir(G0, L0, dt=-0.003, nsteps=150000)
    marker = " <== BEST" if abs(angle - best_angle) < 0.001 else ""
    print(f"  {angle*180/math.pi:8.2f} deg -> min_G={pt[0]:.6f}, min_L={pt[1]:.6f}, min_dist={d:.6f}, bounded={'yes' if ok else 'NO'}{marker}")
