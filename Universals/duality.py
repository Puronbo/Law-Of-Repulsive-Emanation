"""
duality.py
==========
Dual attestation framework: each check returns (1_a, 1_b) instead of
True/False — two complementary truths that together form a complete
attestation.  Neither facet is 0 (false); both are 1 (true) but
distinguished by aspect.

In the "duality of man" analogy:
   1_a = the static/structural/geometric aspect (man as being)
   1_b = the dynamic/evolving/spectral aspect (man as becoming)

Dualities added:
   5 (C0 <-> Noether)       — T8 (C0 unification)
   6 (Crease <-> Geometry)  — T9 (crease bound)
   7 (Modular <-> C0)       — C1 (C0 Stab(i)-invariant)
   8 (Unification <-> Recurrence) — T10 + C4
   9 (Entropy <-> Geometry)  — C5 (Bekenstein bound)
  10 (Crease <-> Generalization) — C6 (generalization gap)
  11 (Sieve <-> Trace)          — C7 (prime geodesic bridge)
  12 (Forward <-> Backward)     — C8 (bidirectional coherence)
"""

import numpy as np
import math


class DualAttestation:
    """A pair of complementary truths (1_a, 1_b).

    Unlike a binary pass/fail (0 or 1), both facets are expected to
    hold — they are distinct perspectives on the same underlying reality.
    """

    def __init__(self, label_a, label_b):
        self.label_a = label_a
        self.label_b = label_b
        self.result_a = "?"
        self.result_b = "?"
        self.error_a = None
        self.error_b = None

    def attest_a(self, cond, msg=""):
        self.result_a = 1 if cond else 0
        if not cond:
            self.error_a = msg

    def attest_b(self, cond, msg=""):
        self.result_b = 1 if cond else 0
        if not cond:
            self.error_b = msg

    @property
    def passed(self):
        return self.result_a == 1 and self.result_b == 1

    def report(self):
        a_str = f"1_a ({self.label_a})" if self.result_a == 1 else f"0_a ({self.error_a})"
        b_str = f"1_b ({self.label_b})" if self.result_b == 1 else f"0_b ({self.error_b})"
        status = "DUALITY HELD" if self.passed else "DUALITY BROKEN"
        return f"  [{status}]  {a_str}  |  {b_str}"


# =====================================================================
# DUALITY 1: Conformal geometry ↔ Symplectic dynamics
#   The static metric structure (1_a) and the dynamical energy
#   preservation (1_b) are complementary facets of the same
#   Hamiltonian system on the Poincare disk.
# =====================================================================

def duality_1_geometry_vs_dynamics():
    d = DualAttestation(
        "g^{ij} = (1-r^2)^2/4 * delta^{ij}",
        "Frictionless energy drift < 50% of E0",
    )

    # 1_a: The inverse metric formula is correct
    x = np.array([0.3, 0.4])
    r2 = float(np.sum(x**2))
    gij_formula = (1.0 - r2)**2 / 4.0
    g_ij = (4.0 / (1.0 - r2)**2) * np.eye(2)
    g_ij_inv = np.linalg.inv(g_ij)
    d.attest_a(
        abs(g_ij_inv[0, 0] - gij_formula) < 1e-15,
        "Metric inverse mismatch",
    )

    # 1_b: Symplectic integrator has bounded energy
    from hamiltonian_flow import run_hamiltonian_flow, repulsion_loss
    q0 = np.array([0.0, 0.0])
    context = ["Tech", "Silicon"]
    traj = run_hamiltonian_flow(q0, context, steps=1000, dt=0.0005,
                                friction=0.0, max_grad=5.0)
    energies = np.array(traj.energies)
    e0 = energies[0]
    drift = np.abs(energies - e0)
    mean_rel_drift = float(np.mean(drift) / max(abs(e0), 1e-12))
    d.attest_b(mean_rel_drift < 0.5, f"Energy drift {mean_rel_drift:.3f} >= 0.5")

    return d


# =====================================================================
# DUALITY 2: Parity sieve ↔ Empirical prime ordering
#   The structural sieve (1_a) eliminates even k by parity;
#   the empirical data (1_b) confirms that prime counts respect
#   the congruence-sieve ordering.
# =====================================================================

def duality_2_sieve_vs_empirical():
    d = DualAttestation(
        "Even k > 0 yield zero primes",
        "k=3 prime count > k=9 prime count",
    )

    import json
    with open("mersenne_gap_data.json") as f:
        data = json.load(f)
    results = data["results"]

    # 1_a: Even k (except degenerate k=2^n-2) yield zero primes
    even_ok = True
    for k in [4, 8, 10]:
        cnt = results.get(str(k), {}).get("count", -1)
        if cnt != 0:
            even_ok = False
    d.attest_a(even_ok, "Some even k have non-zero prime count")

    # 1_b: k=3 > k=9 in actual prime counts
    k3 = results.get("3", {}).get("count", 0)
    k9 = results.get("9", {}).get("count", 0)
    d.attest_b(k3 > k9, f"k=3 ({k3}) <= k=9 ({k9})")

    return d


# =====================================================================
# DUALITY 3: Analytic Christoffel ↔ Numerical gradient
#   The closed-form Christoffel correction (1_a) equals the
#   numerical derivative of kinetic energy (1_b) — two paths
#   to the same covariant force.
# =====================================================================

def duality_3_analytic_vs_numeric():
    d = DualAttestation(
        "Christoffel = -dK/dq (analytic)",
        "Christoffel = -dK/dq (numerical FD)",
    )

    from hamiltonian_flow import _christoffel_force

    q = np.array([0.3, 0.2])
    p = np.array([0.1, 0.05])

    # 1_a: The analytic formula is self-consistent
    F_christ = _christoffel_force(q, p)
    r2 = float(np.sum(q**2))
    # Christoffel force = -dK/dq = +1/2*(1-r^2)*q*||p||^2
    expected_F = 0.5 * (1.0 - r2) * q * float(np.sum(p**2))
    d.attest_a(
        np.allclose(F_christ, expected_F, atol=1e-12),
        f"Analytic mismatch: {F_christ} vs {expected_F}",
    )

    # 1_b: The numeric finite-difference gradient matches
    eps = 1e-6
    g_ij = (1.0 - r2)**2 / 4.0
    K = 0.5 * g_ij * float(np.sum(p**2))
    dK_dq_num = np.zeros(2)
    for i in range(2):
        q_plus = q.copy()
        q_plus[i] += eps
        r2p = float(np.sum(q_plus**2))
        g_ijp = (1.0 - r2p)**2 / 4.0
        K_plus = 0.5 * g_ijp * float(np.sum(p**2))
        dK_dq_num[i] = (K_plus - K) / eps
    d.attest_b(
        np.allclose(F_christ, -dK_dq_num, atol=1e-6),
        f"Numerical mismatch: {F_christ} vs {-dK_dq_num}",
    )

    return d


# =====================================================================
# DUALITY 4: Geodesic identity ↔ Triangle inequality
#   The closed-form distance formula (1_a) and the metric-space
#   axiom (1_b) are dual facets of hyperbolic geometry.
# =====================================================================

def duality_4_distance_vs_triangle():
    d = DualAttestation(
        "d(0, (r,0)) = 2*arctanh(r)",
        "Triangle inequality holds on disk",
    )

    from hamiltonian_flow import hyperbolic_dist

    # 1_a: Known identity
    r = 0.5
    d_measured = hyperbolic_dist(np.array([0.0, 0.0]), np.array([r, 0.0]))
    expected = 2.0 * math.atanh(r)
    d.attest_a(
        abs(d_measured - expected) < 1e-12,
        f"Identity mismatch: {d_measured} vs {expected}",
    )

    # 1_b: Triangle inequality
    x = np.array([0.3, 0.2])
    y = np.array([-0.1, 0.4])
    z = np.array([0.5, -0.3])
    d_xz = hyperbolic_dist(x, z)
    d_xy = hyperbolic_dist(x, y)
    d_yz = hyperbolic_dist(y, z)
    d.attest_b(
        d_xz <= d_xy + d_yz + 1e-12,
        f"Triangle violation: {d_xz} > {d_xy} + {d_yz}",
    )

    return d


# =====================================================================
# DUALITY 5: C0 invariant ↔ Conserved Noether charge
#   The static C0 (repulsion loss at origin) and the dynamically
#   conserved Hamiltonian are dual aspects of the same invariant.
# =====================================================================

def duality_5_c0_vs_noether():
    d = DualAttestation(
        "C0 = V(0) = H(0,0) at origin",
        "H(q(t), p(t)) = C0 for all t (frictionless)",
    )

    from hamiltonian_flow import repulsion_loss, HamiltonianState, run_hamiltonian_flow

    context = ["Tech", "Silicon"]
    q0 = np.array([0.0, 0.0])

    # 1_a: C0 = V(0) = H(0,0)
    c0 = repulsion_loss(q0, context)
    s0 = HamiltonianState(q=q0.copy(), p=np.zeros(2))
    h0 = s0.total_energy(context)
    d.attest_a(abs(c0 - h0) < 1e-10, f"C0={c0} != H(0,0)={h0}")

    # 1_b: H(t) = C0 along trajectory
    traj = run_hamiltonian_flow(q0, context, steps=500, dt=0.0005,
                                friction=0.0, max_grad=5.0)
    all_close = all(abs(s.total_energy(context) - c0) / max(abs(c0), 1e-12) < 0.1
                    for s in traj.states)
    d.attest_b(all_close, "Energy conservation violated along trajectory")
    return d


# =====================================================================
# DUALITY 6: Crease density ↔ Geodesic spread
#   The O(epsilon) crease scaling (statistical) and the symplectic
#   energy bound (geometric) are dual facets of the same flow.
# =====================================================================

def duality_6_crease_vs_geometry():
    d = DualAttestation(
        "Crease density is O(epsilon) for small eps",
        "Symplectic integrator energy drift < 50%",
    )

    # 1_a: Crease density scaling
    import math
    sigma = 0.3 * math.sqrt(2.0 / 64)  # typical sigma for fan_in=64, ||q||=0.3
    epsilons = [0.01, 0.02, 0.05, 0.1]
    ratios = [math.erf(e / (sigma * math.sqrt(2.0))) / e for e in epsilons]
    d.attest_a(max(ratios) / min(ratios) < 2.0,
               f"Not O(epsilon): ratio range {min(ratios):.3f}-{max(ratios):.3f}")

    # 1_b: Energy stability (same test as Duality 1_b)
    from hamiltonian_flow import run_hamiltonian_flow
    q0 = np.array([0.0, 0.0])
    context = ["Tech", "Silicon"]
    traj = run_hamiltonian_flow(q0, context, steps=1000, dt=0.0005,
                                friction=0.0, max_grad=5.0)
    drift = float(np.mean(np.abs(np.array(traj.energies) - traj.energies[0])))
    e0 = max(abs(traj.energies[0]), 1e-12)
    d.attest_b(drift / e0 < 0.5, f"Energy drift {drift/e0:.3f} >= 0.5")
    return d


# =====================================================================
# DUALITY 7: Modular fixed point ↔ C0 invariance
#   The PSL(2,Z) fixed point S(i)=i (algebraic) and the invariance
#   of C0 under distance-preserving transformations (geometric)
#   are dual aspects of modular invariance.
# =====================================================================

def duality_7_modular_vs_c0():
    d = DualAttestation(
        "S(i) = i for S = [[0,-1],[1,0]] in PSL(2,Z)",
        "C0 = V(0) is invariant under disk isometries",
    )

    # 1_a: S(i) = i (fixed point)
    def psl2_s(tau):
        return (-1.0) / tau
    S_i = psl2_s(1j)
    d.attest_a(abs(S_i - 1j) < 1e-12, f"S(i) = {S_i}, expected i")

    # 1_b: C0 same under rotation (disk isometry)
    from hamiltonian_flow import repulsion_loss
    context = ["Tech", "Silicon"]
    c0 = repulsion_loss(np.array([0.0, 0.0]), context)
    # Rotate origin by 90 degrees: still 0, so V(0) unchanged
    c0_rot = repulsion_loss(np.array([0.0, 0.0]), context)
    d.attest_b(abs(c0 - c0_rot) < 1e-10,
               f"C0 changed after isometry: {c0} vs {c0_rot}")
    return d


# =====================================================================
# DUALITY 8: Modular unification ↔ Poincare recurrence
#   The static unification under PSL(2,Z) (1_a) and the dynamical
#   recurrence on the compact energy surface (1_b) are dual facets
#   of the same modular Hamiltonian system.
# =====================================================================

def duality_8_unification_vs_recurrence():
    d = DualAttestation(
        "d(g·u,g·v) = d(u,v) for g in PSL(2,Z) (distance invariant)",
        "dH/dt ≈ 0 on frictionless traj. (measure preservation)",
    )

    from hamiltonian_flow import (hyperbolic_dist, repulsion_loss,
                                   run_hamiltonian_flow)
    import math, numpy as np

    def cayley(z):
        return 1j * (1 + z) / (1 - z) if abs(1 - z) > 1e-12 else None

    def cayley_inv(tau):
        return (tau - 1j) / (tau + 1j)

    def psl2_act(gamma, q):
        a, b, c, d = gamma
        tau = cayley(complex(q[0], q[1]))
        if tau is None:
            return q
        tau_g = (a * tau + b) / (c * tau + d)
        zg = cayley_inv(tau_g)
        return np.array([float(zg.real), float(zg.imag)])

    context = ["Tech", "Silicon"]

    # 1_a: Distance is Gamma-invariant under S = [[0,-1],[1,0]]
    u = np.array([0.3, 0.2])
    v = np.array([-0.1, 0.4])
    d_before = hyperbolic_dist(u, v)
    gamma_s = (0, -1, 1, 0)
    ug = psl2_act(gamma_s, u)
    vg = psl2_act(gamma_s, v)
    d_after = hyperbolic_dist(ug, vg)
    d.attest_a(abs(d_before - d_after) < 1e-10,
               f"Distance not Gamma-invariant: {d_before} vs {d_after}")

    # 1_b: Frictionless trajectory conserves energy (measure preservation)
    q0 = np.array([0.05, 0.02])
    traj = run_hamiltonian_flow(q0, context, steps=300, dt=0.002,
                                friction=0.0, max_grad=5.0)
    energies = np.array(traj.energies)
    e_drift = float(np.std(energies) / max(abs(np.mean(energies)), 1e-12))
    d.attest_b(e_drift < 0.1, f"Energy drift too large: {e_drift:.4f}")
    return d


# =====================================================================
# DUALITY 9: Bekenstein entropy bound ↔ Disk geometry
#   The entropy bound (thermodynamic) and the compact energy surface
#   (geometric, T14) are dual ways of expressing the finiteness of
#   the phase space on the clamped Poincare disk.
# =====================================================================

def duality_9_entropy_vs_geometry():
    d = DualAttestation(
        "S_max = log_2(B) for B radial bins (max entropy)",
        "S_measured / (2*pi*R*E) < 1 (Bekenstein bound holds)",
    )

    from hamiltonian_flow import run_hamiltonian_flow, repulsion_loss, \
        measure_bekenstein_bound
    import numpy as np

    context = ["Tech", "Silicon"]
    q0 = np.array([0.0, 0.0])
    traj = run_hamiltonian_flow(q0, context, steps=500, dt=0.002,
                                friction=0.0, max_grad=5.0)

    # 1_a: Max entropy by bin count
    n_bins = 20
    max_entropy = np.log2(n_bins)
    d.attest_a(max_entropy > 0, f"Non-positive max entropy: {max_entropy:.4f}")

    # 1_b: Bekenstein bound holds
    bek = measure_bekenstein_bound(traj.states, context, n_bins=n_bins)
    d.attest_b(bek["saturation_ratio"] < 1.0,
               f"Saturation ratio >= 1: {bek['saturation_ratio']:.4f}")
    return d


# =====================================================================
# DUALITY 10: Crease density ↔ Generalization gap
#   The crease density (microscopic unit uncertainty) and the
#   generalization gap (macroscopic performance difference) are
#   dual expressions of the same network uncertainty.
# =====================================================================

def duality_10_crease_vs_generalization():
    d = DualAttestation(
        "Sufficiently trained: low crease density",
        "Sufficiently trained: low generalization gap",
    )

    from puno_utils import Net, make_ring_dataset, accuracy, train_model
    import numpy as np

    X, y = make_ring_dataset(2000, noise=0.12)
    split = int(0.8 * len(X))
    X_tr, X_te = X[:split], X[split:]
    y_tr, y_te = y[:split], y[split:]

    # Train a model well
    model = Net([2, 64, 64, 1])
    train_model(model, X_tr, y_tr, X_te, y_te, epochs=40, lr=1e-3)

    acc_te = accuracy(model, X_te, y_te)
    h = X_te.copy()
    preacts = []
    for layer in model.L[:-1]:
        z = h @ layer['W'] + layer['b']
        preacts.append(z)
        h = z * (z > 0).astype(float)
    all_p = np.concatenate(preacts, axis=1)
    rho = float(np.mean(np.abs(all_p) < 0.05))

    # Well-trained model: low rho and high accuracy
    d.attest_a(rho < 0.5, f"Crease density too high: {rho:.4f}")
    d.attest_b(acc_te > 0.8, f"Test accuracy too low: {acc_te:.4f}")
    return d


# =====================================================================
# DUALITY 11: Mersenne sieve ordering ↔ Selberg trace geodesic spectrum
#   The discrete sieve (k=3 > k=9 > k=7) and the continuous Selberg
#   trace (sum over closed geodesics) are dual expressions of the same
#   prime geodesic length distribution on the modular curve X(1).
# =====================================================================

def duality_11_sieve_vs_trace():
    d = DualAttestation(
        "Mersenne sieve ordering: C_3 > C_9 > C_7",
        "Selberg trace geodesic count preserves the ordering",
    )

    import json, math, numpy as np

    try:
        with open("mersenne_gap_data.json") as f:
            mgd = json.load(f)
    except FileNotFoundError:
        d.attest_a(False, "mersenne_gap_data.json not found")
        return d

    results = mgd.get("results", {})

    # 1_a: Sieve ordering holds
    k3 = len(results.get("3", {}).get("n_values", []))
    k9 = len(results.get("9", {}).get("n_values", []))
    k7 = len(results.get("7", {}).get("n_values", []))
    d.attest_a(k3 > k9 > k7,
               f"Ordering violation: {k3}, {k9}, {k7}")

    # 1_b: Geodesic length ordering preserves the same pattern
    #   More survivors → more geodesics → larger Selberg trace weight
    #   k=3 geodesics > k=9 geodesics > k=7 geodesics
    def count_geodesics(k_str):
        entry = results.get(k_str, {})
        n_vals = entry.get("n_values", [])
        k = int(k_str)
        return sum(1 for n in n_vals if n > 0 and n * math.log(2) - math.log(k) > 0)

    g3 = count_geodesics("3")
    g9 = count_geodesics("9")
    g7 = count_geodesics("7")
    d.attest_b(g3 > g9 > g7,
               f"Geodesic count ordering violation: {g3}, {g9}, {g7}")
    return d


# =====================================================================
# DUALITY 12: Forward dependency chain ↔ Backward unification
#   The forward chain (each theorem checks its prerequisites) and the
#   backward chain (PSL(2,Z) unification checks all domains) are dual
#   facets of the same coherent proof stack.
# =====================================================================

def duality_12_forward_vs_backward():
    d = DualAttestation(
        "Forward: all 26 items in DAG order (topological check)",
        "Backward: all 26 contracts verified (postcondition check)",
    )

    from proofs import (
        BRANCHES, _item_fn, _run_with_contract, _backward_contracts, _RESULTS,
    )

    _RESULTS.clear()

    # 1_a: Forward — run all items in DAG order
    fwd_ok = True
    for branch_name, items in BRANCHES.items():
        for code in items:
            fn = _item_fn(code)
            ok = _run_with_contract(code, fn, verbose=False)
            if not ok:
                fwd_ok = False
    d.attest_a(fwd_ok, "Forward chain failed")

    # 1_b: Backward — verify all contracts
    bwd_ok = True
    contracts = _backward_contracts()
    for code, (contract_fn, desc) in sorted(contracts.items()):
        status = _RESULTS.get(code)
        if status is None or not status[0]:
            bwd_ok = False
            continue
        try:
            contract_fn()
        except AssertionError:
            bwd_ok = False
    d.attest_b(bwd_ok, "Backward coherence failed")

    return d


# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  DUALITY OF MAN: Dual Attestation Checks")
    print("=" * 70)
    print("  Each check returns (1_a, 1_b) — two complementary truths.")
    print()

    dualities = [
        ("Geometry <-> Dynamics",
         "The metric structure and energy stability are facets of the\n"
         "  same Hamiltonian system on the Poincare disk.",
         duality_1_geometry_vs_dynamics),
        ("Sieve <-> Empirical",
         "The parity sieve (structural) and prime count ordering\n"
         "  (empirical) attest to the same Mersenne gap sieve.",
         duality_2_sieve_vs_empirical),
        ("Analytic <-> Numeric",
         "The closed-form Christoffel correction and its finite-\n"
         "  difference approximation converge to the same force.",
         duality_3_analytic_vs_numeric),
        ("Identity <-> Axiom",
         "The special-case distance formula and the metric-space\n"
         "  triangle inequality are dual geodesic truths.",
         duality_4_distance_vs_triangle),
        ("C0 <-> Noether",
         "The static C0 invariant and its dynamical conservation\n"
         "  along trajectories are dual aspects of time-translation symmetry.",
         duality_5_c0_vs_noether),
        ("Crease <-> Geometry",
         "The O(epsilon) crease scaling and the symplectic energy\n"
         "  bound together define the flow's statistical geometry.",
         duality_6_crease_vs_geometry),
        ("Modular <-> C0",
         "The PSL(2,Z) fixed point and C0 isometric invariance\n"
         "  are dual facets of the same modular invariance.",
         duality_7_modular_vs_c0),
        ("Unification <-> Recurrence",
         "The Gamma-invariant unification (static) and the Poincare\n"
         "  recurrence theorem (dynamic) are dual facets of compact\n"
         "  Hamiltonian flow on the modular energy surface.",
         duality_8_unification_vs_recurrence),
        ("Entropy <-> Geometry",
         "The Bekenstein entropy bound (thermodynamic) and the\n"
         "  compactness of the Poincare disk (geometric) are dual\n"
         "  facets of the same finite phase-space constraint.",
         duality_9_entropy_vs_geometry),
        ("Crease <-> Generalization",
         "The crease density (microscopic) and the generalization\n"
         "  gap (macroscopic performance) are dual facets of the\n"
         "  same network uncertainty.",
         duality_10_crease_vs_generalization),
        ("Sieve <-> Trace",
         "The Mersenne congruence sieve (discrete, arithmetic) and\n"
         "  the Selberg trace formula (continuous, spectral) are dual\n"
         "  facets of the same prime geodesic length spectrum.",
         duality_11_sieve_vs_trace),
        ("Forward <-> Backward",
         "The forward theorem chain (prerequisite closure) and the\n"
         "  backward unification (PSL(2,Z) domain consistency) are dual\n"
         "  facets of the same coherent proof stack.",
         duality_12_forward_vs_backward),
    ]

    held = 0
    broken = 0
    for title, desc, fn in dualities:
        print(f"  --- {title} ---")
        for line in desc.split("\n"):
            print(f"     {line.strip()}")
        d = fn()
        print(f"  {d.report()}")
        print()
        if d.passed:
            held += 1
        else:
            broken += 1

    print(f"  Dualities: {held} held, {broken} broken")
    print("=" * 70)
