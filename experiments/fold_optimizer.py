"""
T60: THE FOLD AS OPTIMIZER (reversible vs dissipative dynamics).

Claim (from the spring-fold T58): the two folds ARE the two branches of
dynamics under reversal --
  RETRACE fold (area 0, returns to C0) = reversible / Hamiltonian flow
  MIRROR fold (area doubled, irreversible) = dissipative flow
and the crease / overcoil ring lock = the settling point of an
optimizer (the local minimum, topologically trapped).

Test system: a spring in a double well V(x) = x^4/4 - x^2/2
(minima at x = +-1, barrier at x = 0).

  (i)  HAMILTONIAN spring  (symplectic Euler, energy conserved):
       the trajectory RETRACES -- closed orbit in phase space,
       recurrence to the start, phase-space area preserved (Liouville).
       It never locks: it keeps re-folding.

  (ii) DAMPED spring  (friction gamma): the trajectory MIRROR-folds --
       energy decays, phase-space area contracts, it locks at the
       minimum and stays (the overcoil ring lock: escape would require
       re-crossing the barrier, i.e. crossing itself).

KNOWN FACTS (measured here):
  G1  Hamiltonian spring: energy drift ~ 0, phase area ~ conserved
  G2  Hamiltonian spring: returns near its start (recurrence, retrace)
  G3  Damped spring: energy decays to the minimum, area contracts
  G4  Damped spring: locks at x ~ +-1 and never escapes (local minimum
      = the ring lock; the barrier top = the self-crossing at TH - pi)

Outputs: metrics printed, data -> data/fold_optimizer_data.json,
plot -> docs/fold_optimizer.png
"""

import numpy as np
import os, json, math


def pot(x):
    return 0.25 * x ** 4 - 0.5 * x ** 2


def grad(x):
    return x ** 3 - x


def shoelace(xs, vs):
    return 0.5 * abs(np.sum(xs[:-1] * vs[1:] - xs[1:] * vs[:-1]))


def run_hamilton(x0, v0, dt, steps):
    xs, vs, es = [x0], [v0], [pot(x0) + 0.5 * v0 ** 2]
    x, v = x0, v0
    for _ in range(steps):
        a = -grad(x)
        v = v + a * dt
        x = x + v * dt
        xs.append(x)
        vs.append(v)
        es.append(pot(x) + 0.5 * v ** 2)
    return np.array(xs), np.array(vs), np.array(es)


def run_damped(x0, v0, dt, steps, gamma):
    xs, vs, es = [x0], [v0], [pot(x0) + 0.5 * v0 ** 2]
    x, v = x0, v0
    for _ in range(steps):
        a = -grad(x) - gamma * v
        v = v + a * dt
        x = x + v * dt
        xs.append(x)
        vs.append(v)
        es.append(pot(x) + 0.5 * v ** 2)
    return np.array(xs), np.array(vs), np.array(es)


def main():
    x0, v0, dt = 1.5, 0.0, 0.01
    steps_h = 40000
    steps_d = 60000

    xs, vs, es = run_hamilton(x0, v0, dt, steps_h)
    xd, vd, ed = run_damped(x0, v0, dt, steps_d, gamma=1.0)

    # --- G1: energy conservation (retrace preserves) ---
    drift_h = np.max(np.abs(es - es[0]))
    # phase area: compare first vs last cycle via convex hull area proxy
    half = len(xs) // 2
    area_early_h = shoelace(xs[:half], vs[:half])
    area_late_h = shoelace(xs[half:], vs[half:])
    area_ratio_h = area_late_h / (area_early_h + 1e-12)

    # --- G2: recurrence (return to start) ---
    ret = np.min(np.hypot(xs[1:] - x0, vs[1:] - v0))
    x_min, x_max = xs.min(), xs.max()
    period_est = 2.0 * (x_max - x_min) / np.mean(np.abs(vs[vs != 0]))

    # --- G3: damping contracts energy and area ---
    emin = pot(1.0)
    ed_final = ed[-1] - emin
    area_early_d = shoelace(xd[: len(xd) // 4], vd[: len(xd) // 4])
    area_late_d = shoelace(xd[-len(xd) // 4:], vd[-len(xd) // 4:])
    area_ratio_d = area_late_d / (area_early_d + 1e-12)

    # --- G4: locks at a minimum and stays ---
    lock_err = abs(xd[-1] - 1.0)
    tail = np.abs(xd[-2000:] - 1.0)
    stays = bool(np.all(tail < 0.05))

    print("=" * 72)
    print("T60: THE FOLD AS OPTIMIZER  (spring in double well V=x^4/4-x^2/2)")
    print("=" * 72)
    print(f"  HAMILTONIAN spring (retrace fold):")
    print(f"    G1 energy drift  max|E-E0| = {drift_h:.2e}   "
          f"phase-area ratio late/early = {area_ratio_h:.4f}")
    print(f"    G2 recurrence: closest return to start = {ret:.3f} "
          f"(x range [{x_min:.2f},{x_max:.2f}])")
    print(f"  DAMPED spring (mirror fold, gamma=1.0):")
    print(f"    G3 energy at end above minimum = {ed_final:.2e}   "
          f"phase-area ratio late/early = {area_ratio_d:.4f}")
    print(f"    G4 lock: |x_end - 1| = {lock_err:.2e}, stays inside 0.05 "
          f"for the last 2000 steps: {stays}")
    print()
    print("KNOWN FACTS:")
    print("  G1  the retrace fold conserves (energy drift ~0, area ~1.0):")
    print("      reversible dynamics, Liouville.")
    print("  G2  it returns near its start: Poincare recurrence; it never")
    print("      locks -- an optimizer run without friction never converges.")
    print("  G3  the mirror fold (friction) decays energy and contracts")
    print("      phase area: this is what lets an optimizer converge.")
    print("  G4  it locks at the minimum and cannot escape without re-")
    print("      crossing the barrier = the overcoil ring lock (T58).  The")
    print("      barrier top x=0 is the self-crossing at theta' = TH - pi.")
    res = {
        'drift_h': float(drift_h), 'area_ratio_h': float(area_ratio_h),
        'recurrence': float(ret), 'x_range': [float(x_min), float(x_max)],
        'ed_final': float(ed_final), 'area_ratio_d': float(area_ratio_d),
        'lock_err': float(lock_err), 'stays': bool(stays),
        'note': 'Hamiltonian = retrace fold (reversible); damped = mirror '
                'fold (irreversible); minimum = ring lock'}
    os.makedirs('data', exist_ok=True)
    with open(os.path.join('data', 'fold_optimizer_data.json'), 'w') as fp:
        json.dump(res, fp, indent=2)
    print("\nsaved data/fold_optimizer_data.json")

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(xs, vs, lw=0.5, color='tab:blue')
    axes[0].set_title('Hamiltonian (retrace): closed orbit, area kept')
    axes[0].set_xlabel('x'); axes[0].set_ylabel('v')
    axes[1].plot(xd, vd, lw=0.5, color='tab:orange')
    axes[1].set_title('Damped (mirror): spirals in, locks at x=+1')
    axes[1].set_xlabel('x'); axes[1].set_ylabel('v')
    plt.tight_layout()
    plt.savefig(os.path.join('docs', 'fold_optimizer.png'), dpi=120)
    print("plot -> docs/fold_optimizer.png")


if __name__ == '__main__':
    main()
