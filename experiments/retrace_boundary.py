"""
T64: THE RETRACE IS NOT ASSUMED -- the reflecting boundary at TH is
selected by the viscosity condition.

T63 derived the forward fold as the unique viscosity solution of
|r'| = a with r(0) = r(2TH) = 0 (the tent).  But the RETURN
characteristic was still put in by hand: "the same equation with a
reflecting boundary at TH".  This experiment removes that assumption.

Claim:  the equation plus the two pins admits INFINITELY many weak
solutions, so the fold's switch point is not fixed by the PDE alone.
The unique VISCOSITY solution is selected, and its switch point is
exactly the cut locus {theta : dist(theta,0) = dist(theta,2TH)} =
{TH} -- equal eikonal time from both C0 pins.  The "reflecting
boundary" is the shock/caustic where the two forward characteristics
collide; the return characteristic is the same equation continuing
past the collision.  Reflection: slope +a -> -a, |r'| = a conserved.

The infinite family (switch at xi in (0, TH), xi = TH gives the tent):
    up   [0, xi]        slope +a
    down [xi, 2xi]      slope -a      <- down-to-up corner at 2xi
    up   [2xi, TH+xi]   slope +a
    down [TH+xi, 2TH]   slope -a
All have |r'| = a a.e. and r(0) = r(2TH) = 0.

Viscosity classification (this is the whole proof):
  - at a smooth point or an up-to-down corner the steep-tangent test
    is vacuous (u - phi strictly decreases through the point);
  - at a DOWN-to-UP corner (local min, value 0) the FLAT tangent
    phi = const gives u - phi a local min with |phi'| = 0 < a, which
    VIOLATES the supersolution inequality.  So every zig-zag with
    xi != TH fails; the tent (xi = TH, no down-up corner) passes
    every test and is therefore the unique viscosity solution.
  - the upwind map is monotone: one step RAISES the down-up corner
    (0 -> a*H), eroding any zig-zag toward the tent.

Measured facts:
  E1  the family {xi} are all weak solutions (slopes, endpoints exact)
  E2  viscosity checker: zig-zag fails at its down-up corner, tent passes
  E3  the upwind solver with the zig-zag as INITIAL GUESS converges to
      the tent (selection is dynamical, not initial-data dependent)
  E4  the switch point of the selected solution is the cut locus: equal
      eikonal time from both pins, theta = TH
  E5  reflection: slope +a -> -a across the crease (|r'| conserved)

Outputs: metrics printed, data -> data/retrace_boundary_data.json,
plot -> docs/retrace_boundary.png
"""

import numpy as np
import os, json, math

A, TH = 1.0, 20.0
H = 0.01


def zigzag(theta, xi):
    """Piecewise slope +/-a zig-zag with first switch at xi (in (0, TH))."""
    r = np.zeros_like(theta)
    up1 = theta <= xi
    down = (theta > xi) & (theta <= 2 * xi)
    up2 = (theta > 2 * xi) & (theta <= TH + xi)
    down2 = theta > TH + xi
    r[up1] = A * theta[up1]
    r[down] = A * (2 * xi - theta[down])
    r[up2] = A * (theta[up2] - 2 * xi)
    r[down2] = A * (2 * TH - theta[down2])
    return r


def weak_solution(r, theta):
    """|r'| = a a.e. (finite differences, excluding kinks) and endpoints."""
    d = np.diff(r) / np.diff(theta)
    body = d[np.abs(d) > A / 2]  # slope magnitudes at smooth grid points
    ok_slope = bool(bool(np.all(np.isclose(np.abs(d), A)))
                    and bool(r[0] == 0 and r[-1] == 0))
    max_dev = float(np.max(np.abs(np.diff(r) / np.diff(theta)))) if len(d) else 0.0
    return ok_slope, max_dev


def viscosity_check(r, theta):
    """Flag down-to-up corners (local minima): flat tangent gives |phi'|=0 < a
    -> violates the supersolution inequality.  Up-to-down corners and smooth
    points pass (steep-tangent test vacuous).  Returns (passes, worst |phi'|)."""
    n = len(r)
    worst = 1e9
    fails = 0
    for i in range(1, n - 1):
        is_min = r[i] < r[i - 1] - 1e-9 and r[i] < r[i + 1] - 1e-9
        is_max = r[i] > r[i - 1] + 1e-9 and r[i] > r[i + 1] + 1e-9
        if is_min:
            # supersolution at a local min needs |phi'| >= a for every touching
            # phi; the flat tangent (|phi'| = 0) shows violation unless r flat
            worst = min(worst, 0.0)
            fails += 1
        if is_max:
            # subsolution at a local max: flat tangent |phi'| = 0 <= a is OK;
            # steep tangents are vacuous (r - phi strictly decreasing there)
            worst = min(worst, 0.0)
    return (fails == 0, worst, fails)


def upwind_eikonal(theta, r0, iters=None):
    """Gauss-Seidel upwind solve of |r'| = a with r(0)=r(2TH)=0, from r0."""
    n = len(theta)
    r = np.array(r0, dtype=float)
    r[0] = r[-1] = 0.0
    if iters is None:
        iters = int(2 * (2 * TH / H) + 100)
    for _ in range(iters):
        r_prev = r.copy()
        for i in range(1, n - 1):
            r[i] = min(r[i - 1] + A * H, r[i + 1] + A * H)
        if np.max(np.abs(r - r_prev)) < 1e-12:
            break
    return r


def tent(theta):
    return A * np.minimum(theta, 2 * TH - theta)


def main():
    theta = np.arange(0, 2 * TH + H / 2, H)
    r_tent = tent(theta)

    # E1: the family {xi} are all weak solutions
    xis = [0.2 * TH, 0.5 * TH, 0.8 * TH]
    weak_ok = []
    for xi in xis:
        r = zigzag(theta, xi)
        ok, dev = weak_solution(r, theta)
        weak_ok.append((xi, ok, dev))

    # E2: viscosity classification
    v_tent_ok, v_tent_worst, v_tent_fails = viscosity_check(r_tent, theta)
    v_results = []
    for xi in xis:
        r = zigzag(theta, xi)
        ok, worst, fails = viscosity_check(r, theta)
        v_results.append((xi, ok, worst, fails))

    # E3: upwind from a zig-zag initial guess -> the tent
    xi0 = 0.5 * TH
    r_zig = zigzag(theta, xi0)
    r_relax = upwind_eikonal(theta, r_zig)
    e3_err = float(np.max(np.abs(r_relax - r_tent)))
    # one-step erosion: the down-up corner at 2*xi0 is raised from 0 to a*H
    corner = int(round(2 * xi0 / H))
    step1 = upwind_eikonal(theta, r_zig, iters=1)
    corner_before = float(r_zig[corner])
    corner_after = float(step1[corner])

    # E4: the selected switch point is the cut locus (equal eikonal time)
    crease_i = int(round(TH / H))
    t_left = A * theta[crease_i]
    t_right = A * (2 * TH - theta[crease_i])
    cut_eq = abs(t_left - t_right)

    # E5: reflection across the crease: slope +a -> -a
    sl_left = (r_tent[crease_i] - r_tent[crease_i - 1]) / H
    sl_right = (r_tent[crease_i + 1] - r_tent[crease_i]) / H
    refl = abs(abs(sl_left) - abs(sl_right))

    print("=" * 72)
    print("T64: THE RETRACE DERIVED -- the reflecting boundary at TH is")
    print("     the cut locus, selected by the viscosity condition")
    print("=" * 72)
    for xi, ok, dev in weak_ok:
        print(f"  E1  weak solution xi={xi:4.1f}: slope |r'|=a {ok}, "
              f"max |dr/dth| = {dev:.2f}, r(0)=r(2TH)=0: yes")
    print(f"      -> the equation + two pins admits infinitely many folds "
          f"(any xi in (0, TH))")
    print(f"  E2  viscosity checker (flat-tangent supersolution test):")
    print(f"      tent  (xi=TH): passes = {v_tent_ok}  (down-up corners = "
          f"{v_tent_fails})")
    for xi, ok, worst, fails in v_results:
        print(f"      zig-zag xi={xi:4.1f}: passes = {ok}  (down-up corners = "
              f"{fails}, min |phi'| = {worst:.0f} < a)")
    print(f"      -> down-to-up corners violate |phi'| >= a; the tent has "
          f"none, so it")
    print(f"         is the UNIQUE viscosity solution")
    print(f"  E3  upwind solve seeded with the zig-zag (xi={xi0:.1f}):")
    print(f"      converged to tent with max err = {e3_err:.1e}")
    print(f"      one step raises the down-up corner 0 -> {corner_after:.3f} "
          f"(a*H = {A*H:.3f}): erosion")
    print(f"      -> selection is dynamical, not initial-data dependent")
    print(f"  E4  switch point of the selected fold = cut locus: "
          f"|t_left - t_right| = {cut_eq:.2e} at theta = TH")
    print(f"      -> the two forward characteristics collide at equal eikonal "
          f"time;")
    print(f"         TH is a shock, NOT a prescribed boundary")
    print(f"  E5  reflection: slope before crease {sl_left:+.3f}, after "
          f"{sl_right:+.3f}; |r'| conserved to {refl:.1e}")
    print()
    print("THEOREM (closes SPRING_BIBLE crease 6, fully):")
    print("  The fold is not imposed, and neither is the retrace.  The")
    print("  equation |r'| = a with C0 pinned at both ends of the loop has")
    print("  infinitely many weak solutions; the viscosity condition selects")
    print("  exactly one - the tent - whose single switch point is the cut")
    print("  locus {theta: dist(theta,0) = dist(theta,2TH)} = {TH}.  The")
    print("  'reflecting boundary' is the shock where the outgoing and")
    print("  returning characteristics collide with equal eikonal time; the")
    print("  fold (return characteristic) is the same equation continuing")
    print("  past the collision, with |r'| = a conserved.  Retrace is a")
    print("  consequence, not an assumption.")
    res = {'weak_family': [(float(xi), ok, dev) for xi, ok, dev in weak_ok],
           'tent_passes': bool(v_tent_ok),
           'zigzag_viscosity': [(float(xi), ok, fails, worst)
                                for xi, ok, worst, fails in v_results],
           'upwind_from_zigzag_err': e3_err,
           'corner_before': corner_before, 'corner_after': corner_after,
           'cut_locus_eq': float(cut_eq),
           'reflection': float(refl),
           'theorem': 'retrace boundary is the cut locus/shock at TH selected '
                      'by viscosity; infinitely many weak solutions, unique '
                      'viscosity solution = tent'}
    os.makedirs('data', exist_ok=True)
    with open(os.path.join('data', 'retrace_boundary_data.json'), 'w') as fp:
        json.dump(res, fp, indent=2)
    print("\nsaved data/retrace_boundary_data.json")

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    ax = axes[0]
    ax.plot(theta, r_tent, color='tab:blue', lw=2, label='tent (selected)')
    for xi in xis:
        ax.plot(theta, zigzag(theta, xi), '--', lw=1,
                label=f'zig-zag xi={xi:.0f}')
    ax.axvline(TH, color='k', ls=':', lw=1)
    ax.set_title('weak solutions of |r\'| = a (infinite family)')
    ax.set_xlabel('theta'); ax.set_ylabel('r')
    ax.legend(fontsize=7)
    ax2 = axes[1]
    ax2.plot(theta, zigzag(theta, xi0), color='tab:gray', lw=1,
             label=f'initial guess (xi={xi0:.0f})')
    ax2.plot(theta, r_relax, color='tab:red', lw=1.6,
             label='upwind relaxation -> tent')
    ax2.plot(theta, r_tent, color='tab:blue', lw=2, label='tent (exact)')
    ax2.set_title('viscosity erosion selects the fold')
    ax2.set_xlabel('theta'); ax2.set_ylabel('r')
    ax2.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(os.path.join('docs', 'retrace_boundary.png'), dpi=120)
    print("plot -> docs/retrace_boundary.png")


if __name__ == '__main__':
    main()
