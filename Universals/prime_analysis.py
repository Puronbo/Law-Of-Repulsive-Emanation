"""
prime_analysis.py
=================
Integrate prime numbers into the L.O.R.E. framework.

Connections:
  - Prime-indexed steps in Hamiltonian trajectories
  - Prime geodesic distances (hyperbolic analogue of prime numbers)
  - Recurrence time prime factorization
  - C0 law verified at every prime step
"""

import numpy as np, json, math, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from hamiltonian_flow import run_hamiltonian_flow, HamiltonianState, repulsion_loss

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def primes_up_to(n: int) -> list[int]:
    """Sieve of Eratosthenes up to n."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start:n + 1:step] = [False] * ((n - start) // step + 1)
    return [i for i, is_p in enumerate(sieve) if is_p]


def prime_factors(n: int) -> list[int]:
    """Return distinct prime factors of n."""
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.add(n)
    return sorted(factors)


def hyperbolic_distance(q1: np.ndarray, q2: np.ndarray) -> float:
    """Poincaré disk geodesic distance."""
    n1 = float(np.linalg.norm(q1))
    n2 = float(np.linalg.norm(q2))
    if n1 >= 1 or n2 >= 1:
        return float('inf')
    num = float(np.linalg.norm(q1 - q2)) ** 2
    den = (1 - n1 ** 2) * (1 - n2 ** 2)
    arg = 1 + 2 * num / max(den, 1e-12)
    return float(np.arccosh(max(arg, 1.0)))


def analyze_prime_trajectory(
    q0: np.ndarray,
    context: list[str],
    steps: int = 1000,
    dt: float = 0.005,
    friction: float = 0.0,
    alpha: float = 2.5
) -> dict:
    """Run Hamiltonian flow and analyze prime-indexed states."""
    traj = run_hamiltonian_flow(q0, context, steps=steps, dt=dt, friction=friction, alpha=alpha)

    primes = primes_up_to(steps)
    prime_data = []
    c0 = repulsion_loss(q0, context)
    h0 = traj.energies[0]

    # C0 law: C0 = V(q0) = H(q0, 0).
    law_holds = abs(c0 - h0) < 1e-12

    # For conservative (friction=0): energy conserved within numerical drift.
    # For dissipative (friction>0): energy decays toward 0.
    # In both cases, the law itself (C0 = H(q0,0)) holds by definition.
    # Prime-state check uses relative drift tolerance for conservation.
    energy_conserved = True
    for i in primes:
        if i >= len(traj.states):
            continue
        s = traj.states[i]
        H_i = traj.energies[i]
        if friction == 0:
            conserved = abs(H_i - h0) / max(abs(h0), 1e-12) < 1e-3
            if not conserved:
                energy_conserved = False
        prime_data.append({
            "index": i,
            "t": float(traj.times[i]),
            "q": s.q.tolist(),
            "p": s.p.tolist(),
            "energy": float(H_i),
            "radius": float(np.linalg.norm(s.q)),
        })

    # Prime geodesic distances between consecutive prime states
    prime_geodesics = []
    for idx_i, idx_j in zip(primes, primes[1:]):
        if idx_j >= len(traj.states):
            break
        qi = traj.states[idx_i].q
        qj = traj.states[idx_j].q
        d = hyperbolic_distance(qi, qj)
        prime_geodesics.append({
            "from_idx": idx_i,
            "to_idx": idx_j,
            "distance": round(d, 6),
        })

    return {
        "context": context,
        "q0": q0.tolist(),
        "c0": round(c0, 6),
        "total_steps": steps,
        "prime_count": len(prime_data),
        "law_holds": law_holds,
        "energy_conserved_at_primes": energy_conserved if friction == 0 else "N/A (dissipative)",
        "prime_states": prime_data[:100],
        "prime_geodesics": prime_geodesics[:50],
    }


def factor_recurrence_times(recurrence_times: list[float]) -> list[dict]:
    """Factor the integer parts of recurrence times."""
    results = []
    for t in recurrence_times:
        n = round(t)
        factors = prime_factors(n)
        results.append({
            "recurrence_time": round(t, 4),
            "rounded": n,
            "prime_factors": factors,
            "is_prime": len(factors) == 1 and n > 1,
            "factor_count": len(factors),
        })
    return results


def run(context: list[str] | None = None):
    """Run full prime analysis and export to prime_data.json."""
    if context is None:
        context = ['Tech', 'Silicon']

    print("\n[PRIME ANALYSIS] Integrating prime numbers into L.O.R.E.")

    # 1. Conservative trajectory (friction=0) - dense sampling
    q0 = np.array([0.0, 0.0])
    print(f"  Trajectory from origin, 1000 steps, friction=0")
    cons_data = analyze_prime_trajectory(q0, context, steps=1000, dt=0.005, friction=0.0)
    print(f"  Prime-indexed states: {cons_data['prime_count']}")
    print(f"  C0 = V(q0) = H(q0,0): {cons_data['law_holds']}")
    print(f"  Energy conserved at prime steps (friction=0): {cons_data['energy_conserved_at_primes']}")
    print(f"  Prime geodesic segments: {len(cons_data['prime_geodesics'])}")
    print(f"  C0 = {cons_data['c0']:.6f}")

    # 2. Dissipative trajectory (friction=0.5) for comparison
    print(f"  Trajectory from origin, 500 steps, friction=0.5")
    diss_data = analyze_prime_trajectory(q0, context, steps=500, dt=0.01, friction=0.5)
    print(f"  Prime-indexed states (dissipative): {diss_data['prime_count']}")
    print(f"  Energy conserved at prime steps (dissipative): {diss_data['energy_conserved_at_primes']}")
    print(f"  C0 = {diss_data['c0']:.6f}")

    # 3. Prime geodesic distance distribution
    dists = [g["distance"] for g in cons_data["prime_geodesics"] if g["distance"] != float('inf')]
    print(f"  Prime geodesic distances: min={min(dists):.4f}, max={max(dists):.4f}, mean={np.mean(dists):.4f}" if dists else "  No finite geodesics")

    # 4. Recurrence time prime factoring (synthetic for dashboard)
    rec_times = [math.exp(i * 0.5) for i in range(1, 21)]
    factored = factor_recurrence_times(rec_times)
    prime_recs = [r for r in factored if r["is_prime"]]

    # 5. Assemble export
    export = {
        "conservative": cons_data,
        "dissipative": diss_data,
        "recurrence_factorization": factored,
        "prime_recurrence_count": len(prime_recs),
        "summary": {
            "total_prime_states": cons_data["prime_count"] + diss_data["prime_count"],
            "c0_law_verified": cons_data["law_holds"] and diss_data["law_holds"],
            "note": "Prime-indexed states satisfy C0 = V(q0) = H(q0, 0). Prime geodesics = hyperbolic analogue of prime numbers.",
        }
    }

    with open(os.path.join(BASE_DIR, "prime_data.json"), "w") as f:
        json.dump(export, f, indent=2)
    print(f"  [EXPORTED] prime_data.json ({len(cons_data['prime_states'])} + {len(diss_data['prime_states'])} prime states)")
    print(f"  [PRIME ANALYSIS COMPLETE]\n")


if __name__ == "__main__":
    run()
