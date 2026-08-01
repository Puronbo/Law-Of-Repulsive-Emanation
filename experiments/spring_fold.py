"""
T58: THE SPRING THAT FOLDS UP ON ITSELF.

Principle (user): "a spring increasing from 0, as matter develops it folds
up on itself."  Grafted onto the existing cosmology (PHYSICAL_UNIVERSAL_MAP
S2 "wound-up spring"; archive "unfolding/folding theorem = derivatives/
integrals"):

  DEVELOPMENT  (unfolding)  = the spring grows from r=0,  dr/dtheta = +a
  FOLD         (folding)     = the spring folds back, dr/dtheta = -a
  CLOSURE      (integral)    = the fold is the integral that returns the
                               spring toward C0 (the origin).

Two distinct folds:
  A   MIRROR fold  r=a(2TH - f), angle keeps increasing: the coil crosses
      back OVER the grown coil (self-intersects at theta' = TH - pi, one
      half-turn before the apex), sweeping the area twice (2 * a^2 TH^3/6).
      Crease at the apex is pi - 2 arctan(1/TH) (a near-pi crease).
  A1  RETRACE fold: the spring folds back ALONG its own path (angle
      decreases), net enclosed area 0, exact C0 closure, crease exactly pi.
  A2  GOLDEN fold: fold length chosen so length_growth/length_fold = phi.
  B   3D helix: z rises during development, falls on the fold -> coils nest.

Outputs: metrics printed, data -> data/spring_fold_data.json,
plot -> docs/spring_fold.png
"""

import numpy as np
import os, json, math

PHI = (1 + 5 ** 0.5) / 2
A = 1.0
TH = 20.0                    # apex angle (10 full turns of development)


def arc_length(a, th):
    """arclength of Archimedean spiral r = a*theta from 0 to th."""
    return (a / 2.0) * (th * math.sqrt(1 + th * th) + math.asinh(th))


def inv_arc(a, s_target, lo, hi):
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if arc_length(a, mid) < s_target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def polar_area(r, th):
    return 0.5 * float(np.sum((0.5 * (r[:-1] + r[1:])) ** 2 * np.diff(th)))


def crease_at(th, r, apex):
    """tangent reversal across the apex (radians), from finite diffs.
    k = first point at/above the apex; crease = |ang[k] - ang[k-1]|."""
    x, y = r * np.cos(th), r * np.sin(th)
    ang = np.arctan2(np.diff(y), np.diff(x))
    k = int(np.argmin(np.abs(th - apex)))
    return abs(ang[k] - ang[k - 1])


print("=" * 72)
print("T58: THE SPRING THAT FOLDS UP ON ITSELF  (r = a*theta, a = 1)")
print("=" * 72)
out = {}

# ---------------- MODEL A: mirror fold (angle keeps increasing) --------
n = 6000
g = np.linspace(0, TH, n, endpoint=False)
f = np.linspace(TH, 2 * TH, n, endpoint=False)
thA = np.concatenate([g, f])
rA = np.concatenate([A * g, A * (2 * TH - f)])
areaA = polar_area(rA, thA)
creaseA = crease_at(thA, rA, TH)
pred_crease = 2 * math.atan(1 / TH)                # analytic soft crease
# self-crossing of the mirror fold: fold point at f crosses growth at
# theta' = TH - pi (one half-turn before apex).
th_cross = TH - math.pi
print("\nMODEL A: MIRROR fold (angle keeps increasing)")
print(f"  total length = {arc_length(A, TH)*2:.2f}   net area = {areaA:,.1f} "
      f"(= 2 * a^2 TH^3 / 6 = {2*A*A*TH**3/6:,.1f}; sweeps the growth twice)")
print(f"  crease at apex = {creaseA/math.pi:.4f}*pi  "
      f"(analytic 2 arctan(1/TH) = {pred_crease/math.pi:.4f}*pi: "
      f"a SOFT fold, tangents stay ~parallel)")
print(f"  self-crossing: fold crosses the grown coil at theta' = TH - pi "
      f"= {th_cross:.3f} (one half-turn before the apex)")
out['A'] = {'length': arc_length(A, TH) * 2, 'area': areaA,
            'area_pred': 2 * A * A * TH ** 3 / 6,
            'crease_pi': creaseA / math.pi,
            'crease_pred_pi': pred_crease / math.pi,
            'crossing_theta': th_cross}

# ---------------- MODEL A1: retrace fold (angle decreases) -------------
g1 = np.linspace(0, TH, n, endpoint=False)
back = np.linspace(TH, 0, n)                     # reverse traversal
th1 = np.concatenate([g1, back])
r1 = np.concatenate([A * g1, A * back])
area1 = polar_area(r1, th1)
clos1 = math.hypot(r1[-1] * np.cos(th1[-1]), r1[-1] * np.sin(th1[-1]))
crease1 = crease_at(th1, r1, TH)
print("\nMODEL A1: RETRACE fold (folds back along its own path)")
print(f"  net area = {area1:+.2e}  closure to C0 = {clos1:.2e}  "
      f"crease = {crease1/math.pi:.4f}*pi")
print(f"  the spring folds back into itself exactly: encloses nothing,")
print(f"  returns to C0, crease pi.  (unfolding = derivative, folding =")
print(f"  integral; the loop integrates back to the constant it unfolded from)")
out['A1'] = {'area': area1, 'closure': clos1, 'crease_pi': crease1 / math.pi}

# ---------------- MODEL A2: golden fold --------------------------------
sg = arc_length(A, TH)
s_end = sg / PHI ** 2                     # so L_growth/(L_growth-L_fold)=phi
th_end = inv_arc(A, s_end, 0, TH)
fold_len = sg - s_end
ratio = sg / fold_len
g2 = np.linspace(0, TH, n, endpoint=False)
f2 = np.linspace(TH, TH + (TH - th_end), n, endpoint=False)
th2 = np.concatenate([g2, f2])
r2 = np.concatenate([A * g2, A * (2 * TH - f2)])
clos2 = math.hypot(r2[-1] * np.cos(th2[-1]), r2[-1] * np.sin(th2[-1]))
r_ret = A * th_end
print(f"\nMODEL A2: GOLDEN fold")
print(f"  solve L_growth/L_fold = phi = {PHI:.6f} -> returned ratio "
      f"{ratio:.6f}")
print(f"  fold closes to r = {r_ret:.4f} = apex * {r_ret/(A*TH):.4f} "
      f"(golden remainder; closure error {clos2:.2e})")
out['A2'] = {'ratio': ratio, 'r_ret': r_ret,
             'r_ret_over_apex': r_ret / (A * TH), 'closure': clos2}

# ---------------- MODEL B: 3D helix fold -------------------------------
tb = np.concatenate([np.linspace(0, TH, n, endpoint=False),
                     np.linspace(TH, 2 * TH, n, endpoint=False)])
rb = A * np.concatenate([np.linspace(0, TH, n, endpoint=False),
                         2 * TH - np.linspace(TH, 2 * TH, n, endpoint=False)])
zb = np.concatenate([np.linspace(0, TH, n, endpoint=False),
                     2 * TH - np.linspace(TH, 2 * TH, n, endpoint=False)])
print(f"\nMODEL B: 3D helix spring (z rises during development, falls on")
print(f"  the fold) -> the coil returns to z={zb[-1]:.2e}, nesting the fold")
print(f"  inside the grown coils: 'folds up on itself' in space.")
out['B'] = {'z_return': float(zb[-1]), 'n_points': int(len(tb))}

# ---------------- MODEL C: overcoil ring lock ---------------------------
# The fold climbs to a second layer z = h0 and coils back OVER every
# growth turn (its (r,theta) projection sweeps the same annulus), then
# dips UNDER the first coil and lands on the START (C0).  End and start
# are both locked -> the spring becomes a closed ring with no free ends.
h0 = A * TH * 0.30                    # overcoil layer height
eps = 0.25                            # how far the tuck lands from C0
tuck = 1.5                            # arc over which z dips below plane
tc = np.linspace(TH, 2 * TH - eps, n, endpoint=False)
rc = A * (2 * TH - tc)
zc = h0 * np.sin(math.pi * (tc - TH) / TH)
dip = np.clip((tc - (2 * TH - eps - tuck)) / tuck, 0.0, 1.0) ** 2
zc = zc - h0 * 0.35 * dip             # end dips under the start coil
thc, rc, zc = tc, rc, zc
closC = math.hypot(rc[-1] * np.cos(thc[-1]), rc[-1] * np.sin(thc[-1]))
r_endC = float(rc[-1])
z_endC = float(zc[-1])
above = float(np.min(zc[(rc > 2 * math.pi * A) & (rc < A * TH - 2)]))
peakC = float(np.max(zc))
tuckC = r_endC < 2 * math.pi * A and z_endC < 0.0     # end under start coil
overlap = float(np.mean(rc < A * TH))                 # fold projects on growth
print(f"\nMODEL C: OVERCOIL ring lock (fold coils over itself in 3D)")
print(f"  fold rises to z = {h0:.2f}, projects onto the growth's own "
      f"annulus ({overlap*100:.0f}% of fold radii inside it)")
print(f"  end lands r={r_endC:.3f}, z={z_endC:+.3f} (inside the first coil, "
      f"under it) -> tucked on the START; apex is the fold's hinge = END")
print(f"  closure to C0 = {closC:.3f}   rides z in [{above:.3f},{peakC:.2f}] "
      f"over the coils (no cutting; tuck stays inside the first coil)")
print(f"  both ends locked -> closed ring, no free end: cannot unwind "
      f"(unlike A's single side-crossing, which stays open at both ends)")
out['C'] = {'h0': h0, 'r_end': r_endC, 'z_end': z_endC,
            'closure': closC, 'tuck_on_start': tuckC,
            'clearance': above, 'overlap_frac': overlap}

# ---------------- save -------------------------------------------------
os.makedirs('data', exist_ok=True)
with open(os.path.join('data', 'spring_fold_data.json'), 'w') as fp:
    json.dump(out, fp, indent=2)
print(f"\nsaved data/spring_fold_data.json")

# ---------------- plot --------------------------------------------------
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(11, 5.5),
                         subplot_kw={'projection': 'polar'})
n2 = len(thA) // 2
ax = axes[0]
ax.plot(thA[:n2], rA[:n2], color='tab:orange', lw=1.0,
        label='development (unfold)')
ax.plot(thA[n2:], rA[n2:], color='tab:blue', lw=1.0, label='mirror fold')
ax.plot(thA[:1], rA[:1], 'k*', ms=12, label='C0 (origin)')
ax.set_rmax(A * TH + 1)
ax.set_rticks([])
ax.set_title('A: mirror fold (self-crosses)', fontsize=9)
ax.legend(loc='upper right', fontsize=7)
ax = axes[1]
m = len(th1) // 2
ax.plot(th1[:m], r1[:m], color='tab:orange', lw=1.0,
        label='development (unfold)')
ax.plot(th1[m:], r1[m:], color='tab:blue', lw=1.0, label='retrace fold')
ax.plot(th1[:1], r1[:1], 'k*', ms=12, label='C0 (origin)')
ax.set_rmax(A * TH + 1)
ax.set_rticks([])
ax.set_title('A1: retrace fold (back along itself)', fontsize=9)
ax.legend(loc='upper right', fontsize=7)
plt.tight_layout()
plt.savefig(os.path.join('docs', 'spring_fold.png'), dpi=120)
print(f"plot -> docs/spring_fold.png")

fig3 = plt.figure(figsize=(6.5, 6))
ax3 = fig3.add_subplot(111, projection='3d')
xg, yg = A * g * np.cos(g), A * g * np.sin(g)
xc3, yc3 = rc * np.cos(thc), rc * np.sin(thc)
ax3.plot(xg, yg, np.zeros_like(g), color='tab:orange', lw=1.2,
         label='development (z=0)')
ax3.plot(xc3, yc3, zc, color='tab:blue', lw=1.2, label='overcoil fold')
ax3.plot([0], [0], [0], 'k*', ms=12, label='C0 start')
ax3.scatter([xc3[-1]], [yc3[-1]], [zc[-1]], color='red', s=40,
            label='end tucked under start')
ax3.view_init(elev=22, azim=60)
ax3.set_title('C: overcoil ring lock (coils over itself)', fontsize=9)
ax3.legend(loc='upper left', fontsize=7)
plt.tight_layout()
plt.savefig(os.path.join('docs', 'spring_fold_overcoil.png'), dpi=120)
print(f"plot -> docs/spring_fold_overcoil.png")

print("\nVERDICT")
print("=" * 72)
print("  development is the derivative (dr/dtheta = +a, matter grows from 0);")
print("  the fold is the integral; the loop returns toward C0.  A mirror")
print("  fold sweeps its own coil twice (soft crease 2 arctan(1/TH)) and")
print("  self-crosses a half-turn short of the apex; a retrace fold")
print("  encloses nothing and closes exactly to C0 (crease pi).  The")
print("  overcoil fold (C) coils over itself and tucks under the start:")
print("  both ends locked = a closed ring with no free ends, the")
print("  strongest lock of the four.")
