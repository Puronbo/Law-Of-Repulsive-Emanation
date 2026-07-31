"""
Golden-ratio survey: three "parts" of one structure.

  Part 1 — Fibonacci spiral (exact geodesic of the cusp metric):
      q_n = phi^n * exp(i n pi/2)      -> step ratio = phi exactly.

  Part 2 — C0-flow ring packing (static): N repelling points on the disk.
      Measure angular gaps (uniform rings?) and radius-vs-index exponent
      (r ~ n^p; Fermat phyllotaxis would give r ~ sqrt(n)).

  Part 3 — C0-flow center injection (growth dynamics): points emerge one
      at a time at the disk center and repel all others (overdamped).
      Measure the angular advance of consecutive emergences:
          golden angle  = 2*pi/phi^2 = 137.5 deg
      This is the Douady-Couder mechanism: repulsion + radial growth.
      The missing parameter is the outward drift per emergence
      (relaxation between injections).

Each part reports its measured ratios against the theoretical
phi / phi^2 / golden-angle values.  The "terms" differ: the golden
ratio appears as a growth ratio in Part 1, as a spacing angle in
Part 3, and (if present) as a packing law in Part 2.
"""

import numpy as np
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Universals'))
from manifold.c0_flow import c0_flow, to_disk, pair_stats

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
rng = np.random.RandomState(seed)

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi / PHI**2          # 137.5077 deg
GOLDEN_ANGLE_DEG = math.degrees(GOLDEN_ANGLE)
max_r = 0.9

def ang(q):
    return math.atan2(q[1], q[0])

def angular_gap_hist(points):
    """Sort by angle, report gap statistics (uniform = 2*pi/N spacing)."""
    n = len(points)
    th = np.array([ang(q) for q in points])
    th = np.sort(th)
    gaps = np.diff(np.hstack([th, th[:1] + 2*math.pi]))
    mean_gap = np.mean(gaps)
    cv = np.std(gaps) / max(mean_gap, 1e-12)
    return mean_gap, cv, gaps

# ===================================================================
print("=" * 70)
print("GOLDEN-RATIO SURVEY: three parts of one structure")
print("=" * 70)

# ===================================================================
# PART 1: Fibonacci spiral exact geodesic (cusp metric)
# ===================================================================
print("\n" + "-" * 70)
print("PART 1: Fibonacci spiral q_n = phi^n exp(i n pi/2)")
print("-" * 70)
N1 = 200
qs1 = np.array([[PHI**n * math.cos(n * math.pi / 2),
                 PHI**n * math.sin(n * math.pi / 2)] for n in range(N1 + 1)])
steps = np.array([np.linalg.norm(qs1[i+1] - qs1[i]) for i in range(N1)])
sr = steps[1:] / steps[:-1]
sr_asym = sr[-50:].mean()
print(f"  Step ratio (asymptotic) : {sr_asym:.6f}   phi = {PHI:.6f}   "
      f"diff = {sr_asym-PHI:+.2e}")
print(f"  Radius ratio per 90 deg : {np.linalg.norm(qs1[-1])/np.linalg.norm(qs1[-2]):.6f}")
print(f"  Radius ratio per full turn (360 deg): "
      f"{np.linalg.norm(qs1[-1])/np.linalg.norm(qs1[-5]):.6f}   phi^4 = {PHI**4:.6f}")

# ===================================================================
# PART 2: Static C0-flow ring packing
# ===================================================================
print("\n" + "-" * 70)
print("PART 2: Static C0-flow packing (repulsion only, no growth)")
print("-" * 70)
print(f"  {'N':<5}{'min_d':<9}{'gap mean':<10}{'gap CV':<9}{'r~n^p':<9}{'comment'}")
print("  " + "-"*56)
for N in [13, 21, 34, 55]:
    init = to_disk(rng.randn(N, 2) * 0.05, max_r=0.1)
    pts = c0_flow(init, n_steps=1200, dt=0.02, friction=0.04, max_r=max_r)
    d_min, d_mean = pair_stats(pts)
    mean_gap, cv, gaps = angular_gap_hist(pts)
    # radius exponent: sort by radius, fit log r vs log rank
    r = np.sort(np.array([np.linalg.norm(q) for q in pts]))
    # exclude tiny radii near 0
    r = r[r > 1e-3]
    p = float(np.polyfit(np.log(np.arange(1, len(r)+1)), np.log(r), 1)[0])
    uniform = cv < 0.15
    comment = "uniform ring" if uniform else ("spiral-ish" if p > 0.45 and p < 0.55 else "packing")
    print(f"  {N:<5}{d_min:<9.4f}{math.degrees(mean_gap):<10.2f}{cv:<9.3f}{p:<9.3f}{comment}")

# ===================================================================
# PART 3: Center injection (growth dynamics) — the missing parameter
# ===================================================================
print("\n" + "-" * 70)
print("PART 3: Emergence with radial growth (Douady-Couder mechanism)")
print("-" * 70)
print(f"  Golden angle = {GOLDEN_ANGLE_DEG:.3f} deg = 2*pi/phi^2")

# --- 3a. Constant rotation optimality: delta = golden angle maximizes ---
# ---     the minimum angular separation (best packing on a circle).  ---
print("\n  3a. Constant rotation theta_n = n*delta: min angular gap vs delta")
th_golden = np.array([(n * GOLDEN_ANGLE) % (2*math.pi) for n in range(1, 101)])
th_golden.sort()
gaps_g = np.diff(np.hstack([th_golden, th_golden[:1] + 2*math.pi]))
min_gap_golden = gaps_g.min()
# compare to a dyadic and to uniform irrational rotations
def min_gap_rot(delta, N=100):
    th = np.sort(np.array([(n * delta) % (2*math.pi) for n in range(1, N+1)]))
    gaps = np.diff(np.hstack([th, th[:1] + 2*math.pi]))
    return gaps.min()
min_gap_uniform = min_gap_rot(2*math.pi / PHI)      # 222.5 deg rotation
min_gap_dyadic = min_gap_rot(2*math.pi / 3)         # 120 deg rotation
print(f"     golden 2pi/phi^2 = {math.degrees(min_gap_golden):7.3f} deg")
print(f"     complement 2pi/phi= {math.degrees(min_gap_uniform):7.3f} deg")
print(f"     rational 2pi/3    = {math.degrees(min_gap_dyadic):7.3f} deg")
best = max(min_gap_golden, min_gap_uniform, min_gap_dyadic)
print(f"     -> golden rotation maximizes the minimum gap"
      f" {'YES' if min_gap_golden == best else 'no'}")

# --- 3b. Emergence + radial growth: divergence angle vs growth g ---
print("\n  3b. Hard-core arc model (van Iterson / Douady-Couder).")
print("      Primordia transport radially outward at speed v; each subtends")
print("      an angular arc core/r; a new primordium appears at radius r0 in")
print("      the largest free angular arc. Divergence angle self-organizes.")
print(f"      {'v (growth)':<12}{'divergence':<12}{'|d-golden|':<12}{'within 5deg'}")
print("      " + "-"*44)
def arc_model(n_pts, v, r0=0.15, core=0.06, dt=0.02, plast_steps=10):
    """Primordia = (r, theta); additive radial transport; largest free arc."""
    pts = [(r0, rng.uniform(0, 2*math.pi))]
    divergence = []
    last_theta = pts[0][1]
    for _ in range(n_pts - 1):
        # transport outward for one plastochron
        for _ in range(plast_steps):
            pts = [(r + v*dt, th) for (r, th) in pts]
        # arcs excluded by each primordium at the emergence radius r0
        excl = []
        for (r, th) in pts:
            half = core / max(r, 1e-9)   # angular half-width
            if half < math.pi:
                excl.append((th - half, th + half))
        # merge intervals on the circle, find the largest free arc
        if not excl:
            new_theta = rng.uniform(0, 2*math.pi)
        else:
            ivs = sorted([(a % (2*math.pi), b % (2*math.pi)) for (a, b) in excl])
            # circular merge
            free = []
            prev_end = ivs[0][0]
            for (a, b) in ivs + [(ivs[0][0] + 2*math.pi, ivs[0][1] + 2*math.pi)]:
                if a > prev_end + 1e-12:
                    free.append((prev_end, a))
                prev_end = max(prev_end, b)
            if not free:
                new_theta = rng.uniform(0, 2*math.pi)
            else:
                best = max(free, key=lambda iv: iv[1] - iv[0])
                new_theta = ((best[0] + best[1]) / 2.0) % (2*math.pi)
        div = (new_theta - last_theta) % (2*math.pi)
        divergence.append(div)
        last_theta = new_theta
        pts.append((r0, new_theta))
    return np.array(divergence)

for v in [0.02, 0.04, 0.06, 0.08, 0.10, 0.15]:
    div = arc_model(80, v)
    div_deg = np.degrees(div[-60:])          # asymptotic regime
    d = np.abs(div_deg - GOLDEN_ANGLE_DEG)
    d = np.minimum(d, 360 - d)
    print(f"      {v:<12.2f}{np.mean(div_deg):<12.2f}{np.mean(d):<12.2f}{np.mean(d < 5):.2f}")

print(f"\n      Result: gap-filling emergence does NOT lock onto the golden angle.")
print(f"      Divergence stays near 360 - (small arc): each new primordium")
print(f"      bisects the leftover of the previous one.  The golden angle is")
print(f"      a SPECIFIC fixed point of the continuous contact dynamics")
print(f"      (Van Iterson/Douady-Couder), not a generic emergent property.")

# ===================================================================
# PART 4: the SAME Fibonacci spiral measured in different metrics
# ===================================================================
print("\n" + "-" * 70)
print("PART 4: one pattern, many metrics — 'a ratio different in terms'")
print("-" * 70)

def hyp_dist(z, w):
    d = np.linalg.norm(np.array(z) - np.array(w))
    denom = np.abs(1 - np.conj(complex(*z)) * complex(*w))
    return 2 * math.atanh(min(d / denom, 0.999999))

# 4a. Cusp spiral (unbounded): q_n = phi^n e^{i n pi/2} — t39 exact geodesic
N4 = 200
qs_cusp = np.array([[PHI**n*math.cos(n*math.pi/2), PHI**n*math.sin(n*math.pi/2)]
                    for n in range(1, N4+1)])
st_cusp = np.array([np.linalg.norm(qs_cusp[i+1]-qs_cusp[i]) for i in range(N4-1)])

# 4b. Exact Fibonacci square corners q_n = F_n e^{i n pi/2} (as fib_squares)
F = [0, 1]
for _ in range(N4):
    F.append(F[-1] + F[-2])
qs_fib = np.array([[F[n]*math.cos(n*math.pi/2), F[n]*math.sin(n*math.pi/2)]
                   for n in range(1, N4+1)])
st_fib = np.array([np.linalg.norm(qs_fib[i+1]-qs_fib[i]) for i in range(N4-1)])

# 4c. Same Fibonacci radii embedded on the disk r = tanh(n ln phi)
qs_disk = np.array([[math.tanh(n*math.log(PHI))*math.cos(n*math.pi/2),
                     math.tanh(n*math.log(PHI))*math.sin(n*math.pi/2)]
                    for n in range(1, N4+1)])
st_eucl = np.array([np.linalg.norm(qs_disk[i+1]-qs_disk[i]) for i in range(N4-1)])
st_hypo = np.array([hyp_dist(qs_disk[i], qs_disk[i+1]) for i in range(N4-1)])
def tail_ratio(x):
    r = x[1:]/x[:-1]
    return float(np.mean(r[-80:]))
def finite_mean(x):
    r = x[1:]/x[:-1]
    return float(np.mean(r[:29]))   # 30 squares, matching fibonacci_squares

print(f"  {'metric':<28}{'ratio':<12}{'regime'}")
print("  " + "-"*50)
print(f"  {'Cusp (log coords)':<28}{tail_ratio(st_cusp):<12.6f}  phi EXACT")
print(f"  {'Euclidean, first 30':<28}{finite_mean(st_fib):<12.6f}  finite mean ~ phi")
print(f"  {'Euclidean, asymptotic':<28}{tail_ratio(st_eucl):<12.6f}  -> 1 (tanh saturation)")
print(f"  {'Poincare hyperbolic':<28}{tail_ratio(st_hypo):<12.6f}  -> 1 (boundary saturation)")
print(f"\n  The same spiral measured in different 'terms' (metrics/regimes):")
print(f"  phi (cusp, exact) | ~phi finite (1.6287 like fib_squares) | 1 (disk).")
print(f"  The missing parameter is the METRIC + the growth regime (bounded vs unbounded).")

# ===================================================================
print("\n" + "=" * 70)
print("TERMS TABLE — where the golden ratio shows up in each part")
print("=" * 70)
print(f"  {'part':<28}{'measured':<14}{'theoretical':<14}{'match'}")
print("  " + "-"*58)
print(f"  {'Fib spiral step ratio':<28}{sr_asym:<14.6f}{'phi':<14}{'EXACT' if abs(sr_asym-PHI)<1e-5 else 'close'}")
print(f"  {'Fib radius/full turn':<28}{np.linalg.norm(qs1[-1])/np.linalg.norm(qs1[-5]):<14.4f}{'phi^4':<14}")
print(f"  {'Golden angle':<28}{GOLDEN_ANGLE_DEG:<14.3f}{'2pi/phi^2':<14}{'definition'}")
print(f"  {'phi - 1 = 1/phi':<28}{PHI-1:<14.6f}{'1/phi':<14}{'EXACT identity'}")
print(f"  {'phi^2 = phi + 1':<28}{PHI**2:<14.6f}{'phi+1':<14}{'EXACT identity'}")
print(f"  {'Euclidean ratio (sqs)':<28}{finite_mean(st_fib):<14.6f}{'~phi':<14}{'finite 30'}")
print(f"  {'Poincare ratio (disk)':<28}{tail_ratio(st_hypo):<14.6f}{'-> 1':<14}{'boundary'}")
print(f"  {'Cusp ratio (log coords)':<28}{tail_ratio(st_cusp):<14.6f}{'-> phi':<14}{'EXACT'}")
print(f"\n  Conclusion: the golden ratio is EXACT in the cusp metric")
print(f"  (logarithmic coordinates) — the Fibonacci spiral is its geodesic.")
print(f"  In the static C0 flow on the disk (Part 2) there is no golden")
print(f"  structure: repulsion alone gives uniform rings (2*pi/n spacing),")
print(f"  the same spacing our hierarchical / incremental / AL layouts use.")
print(f"  Emergent golden-angle locking (Part 3) needs the continuous")
print(f"  contact dynamics, not gap-filling.  The missing parameters are")
print(f"  the METRIC and the EMERGENCE DYNAMICS, both absent from the")
print(f"  static repulsion layouts.")
print(f"\nDone.")
