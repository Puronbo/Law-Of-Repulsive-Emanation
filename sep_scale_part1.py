"""Physical scale setting along the separatrix. Part 1: integration."""
import math, sys
sys.path.insert(0, 'C:/Users/Me/Downloads/Puno_Calculus')
from litim_flow import beta_Ib, find_fp

res, Gs, ls = find_fp()
pi = math.pi
sep_angle = 0.90 * pi / 180
eps = 0.001
G0 = Gs + eps * math.cos(sep_angle)
L0 = ls + eps * math.sin(sep_angle)

def rk4_step(G, L, dt):
    def f(g, l): return beta_Ib(g, l)
    k1 = f(G, L)
    k2 = f(G+0.5*dt*k1[0], L+0.5*dt*k1[1])
    k3 = f(G+0.5*dt*k2[0], L+0.5*dt*k2[1])
    k4 = f(G+dt*k3[0], L+dt*k3[1])
    return (G+(dt/6)*(k1[0]+2*k2[0]+2*k3[0]+k4[0]),
            L+(dt/6)*(k1[1]+2*k2[1]+2*k3[1]+k4[1]))

k_start = 1e19
dt_RG = -0.005
G_t, L_t = G0, L0
t_RG = 0.0
t_cosmic = 0.0
results = []

for step in range(500000):
    k = k_start * math.exp(t_RG)
    val = max(0, (8*pi*G_t + L_t)/3)
    H = k * math.sqrt(val) if val > 0 else 0
    G_phys = G_t / k**2 if k > 0 else 0
    L_phys = L_t * k**2 if k > 0 else 0
    results.append((t_RG, k, G_t, L_t, G_phys, L_phys, H, t_cosmic))
    G_new, L_new = rk4_step(G_t, L_t, dt_RG)
    if G_new <= 0 or L_new >= 0.5 or L_new < 0 or G_new > 10:
        break
    k2 = k_start * math.exp(t_RG + dt_RG)
    val2 = max(0, (8*pi*G_new + L_new)/3)
    H_new = k2 * math.sqrt(val2) if val2 > 0 else 0
    H_avg = (H + H_new) / 2 if H + H_new > 0 else 1e-30
    t_cosmic += (-dt_RG) / H_avg
    G_t, L_t = G_new, L_new
    t_RG += dt_RG
    if k < 1e-2:
        break

import pickle
with open('sep_results.pkl', 'wb') as f:
    pickle.dump(results, f)
print(f"Done: {len(results)} steps, final k={results[-1][1]:.2e} GeV")
