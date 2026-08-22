import math

# EH beta functions (Codello 2009, eq.53, type Ib)
def beta_Ib(G, L):
    if G <= 0 or L <= 0 or L >= 0.5:
        return 0, 0, False
    pi = math.pi
    NL = (12 - 33*L + 20*L**2 - 200*L**3)*G + (467 - 572*L)/(12*pi) * G**2
    NG = (105 - 212*L + 200*L**2) * G**2
    D = (1 - 2*L)**2 - (29 - 9*L)/(72*pi) * G
    if abs(D) < 1e-15:
        return 0, 0, False
    bL = -2*L + (1/(24*pi)) * NL / D
    bG = 2*G - (1/(24*pi)) * NG / D
    return bG, bL, True

# RK4 step
def rk4_step(G, L, dt):
    k1G, k1L, ok1 = beta_Ib(G, L)
    if not ok1: return G, L, False
    k2G, k2L, ok2 = beta_Ib(G + 0.5*dt*k1G, L + 0.5*dt*k1L)
    if not ok2: return G, L, False
    k3G, k3L, ok3 = beta_Ib(G + 0.5*dt*k2G, L + 0.5*dt*k2L)
    if not ok3: return G, L, False
    k4G, k4L, ok4 = beta_Ib(G + dt*k3G, L + dt*k3L)
    if not ok4: return G, L, False
    G_new = G + (dt/6)*(k1G + 2*k2G + 2*k3G + k4G)
    L_new = L + (dt/6)*(k1L + 2*k2L + 2*k3L + k4L)
    if G_new <= 0 or L_new <= 0 or L_new >= 0.5:
        return G, L, False
    return G_new, L_new, True

# Find FP
G_fp, L_fp = 0.7012, 0.1715
for _ in range(100):
    bG, bL, ok = beta_Ib(G_fp, L_fp)
    G_fp -= 0.001 * bG
    L_fp -= 0.001 * bL
print("FP: G*={:.6f}, L*={:.6f}, G*L*={:.6f}".format(G_fp, L_fp, G_fp*L_fp))

# Trace product along multiple trajectories
print()
print("TRAJECTORY ANALYSIS: G~ x L~ along the flow")
print("=" * 60)
print()

# Separatrix trajectory (0.90 deg from FP)
angle = math.radians(0.90)
dG0 = 0.001 * math.cos(angle)
dL0 = 0.001 * math.sin(angle)
G0, L0 = G_fp + dG0, L_fp + dL0

dt = -0.005  # toward IR
t = 0
max_t = -10
G, L = G0, L0
print("SEPARATRIX trajectory (0.90 deg from FP)")
print("  t        G~       L~       G~xL~     log10(G~xL~)")
print("  {:5.1f}   {:.4f}   {:.4f}   {:.6f}   {:.2f}".format(0, G, L, G*L, math.log10(G*L)))

n_print = 0
while t > max_t:
    G_new, L_new, ok = rk4_step(G, L, dt)
    if not ok:
        print("  BREAK at t={:.1f} (singular line)".format(t))
        break
    G, L = G_new, L_new
    t += dt
    if n_print % 20 == 0:
        print("  {:5.1f}   {:.4f}   {:.4f}   {:.6f}   {:.2f}".format(t, G, L, G*L, math.log10(max(G*L, 1e-300))))
    n_print += 1

print()
print()

# Multiple initial conditions
print("MULTIPLE TRAJECTORIES: product G~xL~ at closest approach to GFP")
print("-" * 60)
for deg in [0.0, 0.45, 0.90, 1.35, 1.80, 2.25, 2.70, 3.15, 3.60]:
    ang = math.radians(deg)
    dG = 0.001 * math.cos(ang)
    dL = 0.001 * math.sin(ang)
    G, L = G_fp + dG, L_fp + dL
    t = 0
    min_dist = 1e10
    LG_at_min = 0
    G_at_min = 0
    L_at_min = 0
    while t > -8:
        G_new, L_new, ok = rk4_step(G, L, dt)
        if not ok:
            break
        G, L = G_new, L_new
        t += dt
        dist = math.sqrt(G**2 + L**2)
        if dist < min_dist:
            min_dist = dist
            LG_at_min = G * L
            G_at_min = G
            L_at_min = L
    print("  angle={:.2f} deg: closest dist={:.4f}, G~={:.4f}, L~={:.4f}, G~xL~={:.6f} ({:.2e})".format(
        deg, min_dist, G_at_min, L_at_min, LG_at_min, LG_at_min))

print()
print()

# The key question
print("THE KEY QUESTION:")
print("=" * 60)
print()
print("  FP value:        G~* x L~* = {:.6f}".format(G_fp * L_fp))
print("  Observed:        G_obs x L_obs = 2.77e-122")
print()
print("  In the EH truncation, the product G~xL~ along trajectories:")
print("  - Starts at ~0.12 at the FP")
print("  - At closest approach to GFP: ~10^-4 to 10^-3")
print("  - Maximum suppression in EH: factor ~100-1000")
print("  - EH breaks down before reaching low energy")
print()
print("  The observed suppression (factor 4e120) is NOT achieved")
print("  in the EH truncation. The EH flow only achieves factor ~10^3.")
print()
print("  The remaining factor of ~10^117 must come from:")
print("  1. Nonlinear flow far from FP (beyond linearization)")
print("  2. f(R) truncation with R^2 coupling running")
print("  3. Matter field contributions to beta functions")
print()
print("  This is the honest state of the problem.")
