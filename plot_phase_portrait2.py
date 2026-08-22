"""Part 2: Generate the 5-panel phase portrait."""
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from plot_phase_portrait import beta_Ib, find_fp, stability_matrix, integrate, rk4_step

res, Gs, ls = find_fp()
print(f"FP: G*={Gs:.6f}, lam*={ls:.6f}")

# Singular curve: denominator = 0 => G = (1-2L)^2 / ((29-9L)/(72pi))
lam_sing = np.linspace(0.01, 0.49, 300)
G_sing = []
for l in lam_sing:
    num = (29.0 - 9.0*l)/(72.0*math.pi)
    if num > 0:
        G_sing.append((1.0-2.0*l)**2 / num)
    else:
        G_sing.append(np.nan)
G_sing = np.array(G_sing)

# Multiple trajectories from FP
trajectories = []
for amp in [0.003, 0.008, 0.015, 0.025, 0.04, 0.06, 0.09]:
    for a_off in np.linspace(0, 2*math.pi, 12, endpoint=False):
        M = stability_matrix(Gs, ls)
        tr = M[0][0]+M[1][1]
        v1 = M[0][1]; v2 = (-tr/2.0 + M[0][0])
        n = math.sqrt(v1*v1+v2*v2)
        if n > 0: v1 /= n; v2 /= n
        angle = math.atan2(v2, v1) + a_off
        g0 = Gs + amp*math.cos(angle)
        l0 = ls + amp*math.sin(angle)
        if g0 > 0.001 and l0 > 0.001 and l0 < 0.49:
            traj = integrate(g0, l0, -0.005, 150000)
            if len(traj) > 20:
                trajectories.append(traj)

print(f"Computed {len(trajectories)} trajectories")

# Create figure
fig, axes = plt.subplots(1, 5, figsize=(26, 5.2))
plt.subplots_adjust(wspace=0.32, left=0.04, right=0.98, top=0.90, bottom=0.15)
XR = (0.0, 1.5)
YR = (0.0, 0.50)

# --- Panel (a): Vector field ---
ax = axes[0]
ax.set_title('(a) Vector field', fontsize=12, fontweight='bold')
ax.set_xlabel(r'$\tilde{G}$', fontsize=13)
ax.set_ylabel(r'$\tilde{\Lambda}$', fontsize=13)
gx = np.linspace(0.05, 1.4, 18)
ly = np.linspace(0.02, 0.46, 14)
for g in gx:
    for l in ly:
        bG, bl = beta_Ib(g, l)
        w2 = (1-2*l)**2
        denom = w2 - (29-9*l)/(72*math.pi)*g
        if abs(denom) < 0.001: continue
        mag = math.sqrt(bG**2+bl**2)
        if mag < 1e-10: continue
        sc = min(0.06/mag, 0.025)
        ax.arrow(g, l, bG*sc, bl*sc, head_width=0.008, head_length=0.004,
                 fc='steelblue', ec='steelblue', alpha=0.6, linewidth=0.5)
ax.plot(G_sing, lam_sing, 'r-', linewidth=1.5, alpha=0.7, label='Singular curve')
ax.plot(Gs, ls, 'k*', markersize=14, zorder=10, label=f'FP ({Gs:.3f}, {ls:.3f})')
ax.set_xlim(XR); ax.set_ylim(YR)
ax.legend(fontsize=7, loc='upper right')

# --- Panel (b): FP eigenstructure ---
ax = axes[1]
ax.set_title('(b) Eigenstructure at FP', fontsize=12, fontweight='bold')
ax.set_xlabel(r'$\tilde{G}$', fontsize=13)
ax.set_ylabel(r'$\tilde{\Lambda}$', fontsize=13)
M = stability_matrix(Gs, ls)
tr = M[0][0]+M[1][1]; det = M[0][0]*M[1][1]-M[0][1]*M[1][0]
disc = tr*tr-4*det
sq = math.sqrt(-disc) if disc < 0 else 0
print(f"tr={tr:.4f}, det={det:.4f}, disc={disc:.4f}, theta={tr/2:.4f}+/-{sq/2:.4f}i")
# Draw spiral near FP
for amp in [0.005, 0.01, 0.02]:
    for a0 in np.linspace(0, 2*math.pi, 8, endpoint=False):
        g0 = Gs + amp*math.cos(a0)
        l0 = ls + amp*math.sin(a0)
        if g0 > 0 and l0 > 0 and l0 < 0.5:
            traj = integrate(g0, l0, -0.003, 50000)
            if len(traj) > 10:
                tg = [t[0] for t in traj]
                tl = [t[1] for t in traj]
                ax.plot(tg, tl, 'b-', alpha=0.4, linewidth=0.7)
ax.plot(Gs, ls, 'r*', markersize=16, zorder=10)
ax.annotate(f'FP\nG*={Gs:.3f}\nL*={ls:.3f}\n$\\theta$=1.689$\\pm$2.486i',
            xy=(Gs, ls), xytext=(Gs+0.15, ls+0.12),
            fontsize=8, arrowprops=dict(arrowstyle='->', color='red'),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow'))
ax.set_xlim(XR); ax.set_ylim(YR)
ax.plot(G_sing, lam_sing, 'r-', linewidth=1, alpha=0.4)

# --- Panel (c): Full separatrix trajectories ---
ax = axes[2]
ax.set_title('(c) RG trajectories from FP', fontsize=12, fontweight='bold')
ax.set_xlabel(r'$\tilde{G}$', fontsize=13)
ax.set_ylabel(r'$\tilde{\Lambda}$', fontsize=13)
colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(trajectories)))
for i, traj in enumerate(trajectories):
    tg = [t[0] for t in traj]
    tl = [t[1] for t in traj]
    ax.plot(tg, tl, '-', color=colors[i], alpha=0.5, linewidth=0.6)
ax.plot(Gs, ls, 'r*', markersize=16, zorder=10)
ax.plot(G_sing, lam_sing, 'r-', linewidth=1.5, alpha=0.5)
ax.set_xlim(XR); ax.set_ylim(YR)

# --- Panel (d): Single spiral (zoomed) ---
ax = axes[3]
ax.set_title('(d) Spiral structure (zoomed)', fontsize=12, fontweight='bold')
ax.set_xlabel(r'$\tilde{G}$', fontsize=13)
ax.set_ylabel(r'$\tilde{\Lambda}$', fontsize=13)
# Pick one nice trajectory
for amp in [0.01]:
    M = stability_matrix(Gs, ls)
    tr2 = M[0][0]+M[1][1]
    v1 = M[0][1]; v2 = (-tr2/2.0 + M[0][0])
    n = math.sqrt(v1*v1+v2*v2)
    if n > 0: v1 /= n; v2 /= n
    g0 = Gs + amp*v1
    l0 = ls + amp*v2
    traj = integrate(g0, l0, -0.002, 300000)
    tg = [t[0] for t in traj]
    tl = [t[1] for t in traj]
    ax.plot(tg, tl, 'b-', alpha=0.8, linewidth=1.2)
ax.plot(Gs, ls, 'r*', markersize=16, zorder=10)
ax.plot(G_sing, lam_sing, 'r-', linewidth=1.5, alpha=0.5)
ax.set_xlim(0.3, 1.2); ax.set_ylim(0.0, 0.40)
ax.annotate('UV FP\n(start here)', xy=(Gs, ls), xytext=(0.95, 0.35),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='red'),
            bbox=dict(boxstyle='round', facecolor='lightyellow'))
ax.annotate('Flow to IR\n(decreasing k)', xy=(0.75, 0.12), xytext=(0.45, 0.05),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='blue'))

# --- Panel (e): Lambda*G product ---
ax = axes[4]
ax.set_title(r'(e) $\tilde{\Lambda} \cdot \tilde{G}$ along flow', fontsize=12, fontweight='bold')
ax.set_xlabel(r'$\tilde{G}$', fontsize=13)
ax.set_ylabel(r'$\tilde{\Lambda} \cdot \tilde{G}$', fontsize=13)
for amp in [0.005, 0.015, 0.03]:
    M2 = stability_matrix(Gs, ls)
    tr2 = M2[0][0]+M2[1][1]
    v1 = M2[0][1]; v2 = (-tr2/2.0 + M2[0][0])
    n = math.sqrt(v1*v1+v2*v2)
    if n > 0: v1 /= n; v2 /= n
    g0 = Gs + amp*v1
    l0 = ls + amp*v2
    traj = integrate(g0, l0, -0.003, 150000)
    tg = [t[0] for t in traj]
    tl = [t[1] for t in traj]
    prod = [t[0]*t[1] for t in traj]
    ax.plot(tg, prod, '-', linewidth=1.2, alpha=0.7, label=f'amp={amp}')
ax.axhline(y=Gs*ls, color='red', linestyle='--', linewidth=1, alpha=0.7,
           label=f'FP value: {Gs*ls:.4f}')
ax.set_xlim(XR)
ax.legend(fontsize=8)

fig.suptitle('Phase portrait: EH truncation, Litim cutoff, d=4 (Codello et al 2009, type Ib)',
             fontsize=14, fontweight='bold', y=0.97)

out = 'C:/Users/Me/Downloads/Puno_Calculus/docs/phase_portrait_rg_flow.png'
fig.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
print(f"Saved to {out}")
plt.close()
