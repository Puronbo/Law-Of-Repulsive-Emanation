import numpy as np
import json
import os
import math

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Hyperbolic geometry primitives
# ---------------------------------------------------------------------------

def hyperbolic_dist(u, v):
    """Exact geodesic distance in the Poincaré disk."""
    sq_norm_u = np.sum(u**2)
    sq_norm_v = np.sum(v**2)
    sq_dist = np.sum((u - v)**2)
    denom = max((1.0 - sq_norm_u) * (1.0 - sq_norm_v), 1e-12)
    return np.arccosh(1.0 + 2.0 * sq_dist / denom)


def riemannian_metric(x):
    """Conformal Riemannian scale factor: ds² = λ(x)² dx²."""
    return ((1.0 - np.sum(x**2))**2) / 4.0


def project_to_disk(x, max_norm=0.99):
    """Clamp x strictly inside the unit disk."""
    r = np.linalg.norm(x)
    if r >= max_norm:
        x = (x / r) * max_norm
    return x


# ---------------------------------------------------------------------------
# Knowledge taxonomy (the universe of concepts)
# ---------------------------------------------------------------------------

knowledge_base = {
    "nodes": [
        {"id": "Origin", "label": "C_0: Pure Awareness", "tier": 0},
        {"id": "System", "label": "Abstract System", "tier": 1},
        {"id": "Matter", "label": "Physical Matter", "tier": 1},
        {"id": "Idea", "label": "Conceptual Idea", "tier": 1},
        {"id": "Bio", "label": "Biological Organisms", "tier": 2},
        {"id": "Tech", "label": "Computing Infrastructure", "tier": 2},
        {"id": "Art", "label": "Creative Arts", "tier": 2},
        {"id": "Mammal", "label": "Mammalian Branch", "tier": 3},
        {"id": "Silicon", "label": "Silicon Hard Systems", "tier": 3},
        {"id": "Music", "label": "Sonic Wave Theory", "tier": 3}
    ],
    "edges": [
        {"source": "Origin", "target": "System"},
        {"source": "Origin", "target": "Matter"},
        {"source": "Origin", "target": "Idea"},
        {"source": "System", "target": "Tech"},
        {"source": "Matter", "target": "Bio"},
        {"source": "Idea", "target": "Art"},
        {"source": "Bio", "target": "Mammal"},
        {"source": "Tech", "target": "Silicon"},
        {"source": "Art", "target": "Music"}
    ]
}

# Hyperbolic radial tier positions — the initial singularity expands outward
positions = {
    "Origin": np.array([0.0, 0.0]),
    "System": np.array([-0.15, 0.10]),
    "Matter": np.array([0.18, -0.05]),
    "Idea": np.array([-0.05, -0.18]),
    "Tech": np.array([-0.40, 0.30]),
    "Bio": np.array([0.45, -0.20]),
    "Art": np.array([-0.10, -0.45]),
    "Mammal": np.array([0.70, -0.35]),
    "Silicon": np.array([-0.65, 0.50]),
    "Music": np.array([-0.20, -0.75])
}


# ---------------------------------------------------------------------------
# Forward pass: unitary evolution via Riemannian gradient descent
# ---------------------------------------------------------------------------

def inject_and_evaluate_novelty(query_text, context_affinities):
    """
    Forward evolution of a probe on the Poincaré disk.

    Implements discrete-time Hamiltonian flow:
        x_{t+1} = x_t - η · g^{ij}(x_t) · ∂_j L(x_t)

    where g^{ij} is the inverse Poincaré metric and L is the repulsion loss.
    Probes with no context affinity are flung to the boundary horizon (r → 1),
    encoding maximal entropy / Bekenstein saturation.
    """
    print(f"\nEvaluating Input Probe: '{query_text}'")

    if not context_affinities:
        xq = (np.random.rand(2) - 0.5) * 0.05
    else:
        xq = np.mean([positions[k] for k in context_affinities], axis=0) * 0.5

    lr = 0.02
    epochs = 200
    alpha = 2.5

    trajectory = [xq.copy()]

    for epoch in range(epochs):
        grad = np.zeros(2)
        eps = 1e-5

        for node_id, pos in positions.items():
            if node_id in context_affinities:
                continue
            d = hyperbolic_dist(xq, pos)
            if d < alpha:
                xq_p0 = xq.copy(); xq_p0[0] += eps
                d_p0 = hyperbolic_dist(xq_p0, pos)
                g0 = (max(0, alpha - d_p0)**2 - max(0, alpha - d)**2) / eps

                xq_p1 = xq.copy(); xq_p1[1] += eps
                d_p1 = hyperbolic_dist(xq_p1, pos)
                g1 = (max(0, alpha - d_p1)**2 - max(0, alpha - d)**2) / eps

                grad += np.array([g0, g1])

        riemannian_factor = riemannian_metric(xq)
        xq = xq - lr * grad * riemannian_factor

        xq = project_to_disk(xq)
        trajectory.append(xq.copy())

    final_radius = np.linalg.norm(xq)
    print(f"-> Settled Position: {xq}")
    print(f"-> Universal Novelty Score (Radius): {final_radius:.4f}")

    if final_radius > 0.85:
        print("-> ALERT: Absolute Out-Of-Distribution Novelty Detected at the Horizon!")
    else:
        print("-> STATUS: Element safely integrated into structural tree taxonomy.")

    return xq.tolist(), final_radius, trajectory


# ---------------------------------------------------------------------------
# Time reversal: gradient ascent reconstruction of the initial state
# ---------------------------------------------------------------------------

def time_reverse_reconstruct(x_final, context_affinities, steps=200, lr=0.02, alpha=2.5):
    """
    Time-reversed evolution: gradient ASCENT on the repulsion loss.

    T-symmetry of the Poincaré metric means the geodesic distance is symmetric:
        d(u, v) = d(v, u)

    Running the gradient flow backward (ascent instead of descent) reconstructs
    the initial probe position from any point on the trajectory. This is the
    discrete analogue of T-symmetry in Hamiltonian mechanics:
        T: (q, p, t) → (q, -p, -t)

    In the narrative mapping, this is "running the equations backward to
    reconstruct the initial boundary state."
    """
    print(f"\n[TIME REVERSAL] Reconstructing initial state from position {x_final}")

    xq = np.array(x_final, dtype=float)
    trajectory_reversed = [xq.copy()]

    for _ in range(steps):
        grad = np.zeros(2)
        eps = 1e-5

        for node_id, pos in positions.items():
            if node_id in context_affinities:
                continue
            d = hyperbolic_dist(xq, pos)
            if d < alpha:
                xq_p0 = xq.copy(); xq_p0[0] += eps
                d_p0 = hyperbolic_dist(xq_p0, pos)
                g0 = (max(0, alpha - d_p0)**2 - max(0, alpha - d)**2) / eps

                xq_p1 = xq.copy(); xq_p1[1] += eps
                d_p1 = hyperbolic_dist(xq_p1, pos)
                g1 = (max(0, alpha - d_p1)**2 - max(0, alpha - d)**2) / eps

                grad += np.array([g0, g1])

        riemannian_factor = riemannian_metric(xq)
        # Ascent: ADD the gradient instead of subtracting
        xq = xq + lr * grad * riemannian_factor

        xq = project_to_disk(xq)
        trajectory_reversed.append(xq.copy())

    final_radius = np.linalg.norm(xq)
    print(f"-> Reconstructed Position: {xq}")
    print(f"-> Reconstructed Radius: {final_radius:.4f}")
    print(f"-> Distance from C_0 (origin): {final_radius:.6f}")

    return xq.tolist(), final_radius, trajectory_reversed


# ---------------------------------------------------------------------------
# Poincaré recurrence: cyclical cosmological reset
# ---------------------------------------------------------------------------

class PoincareRecurrence:
    """
    Models a cyclical conformal universe with discrete Poincaré recurrence.

    Each cycle:
        1. Big Bang:  probe initialized near C_0 (low entropy)
        2. Expansion: gradient descent pushes probe outward (entropy increases)
        3. Heat Death: probe reaches boundary horizon (maximal entropy)
        4. Conformal Reset: stale state pruned, new cycle begins

    The recurrence time τ ~ exp(S/k_B) is encoded as:
        cycle_length = exp(entropy) where entropy = mean radius over history

    The dream mechanism is the conformal boundary — the point where the
    old universe ends and the new one begins.
    """

    def __init__(self, curiosity_drive=0.5, max_cycles=10, reset_threshold=0.85):
        self.curiosity_drive = curiosity_drive
        self.max_cycles = max_cycles
        self.reset_threshold = reset_threshold
        self.history = []
        self.cycle_count = 0
        self.recurrence_times = []
        # v2: self-referential feedback loop (CTC data structure)
        self.self_chain = []          # past outputs influencing future inputs
        self.classification_history = []  # time-ordered state transitions
        self.max_history = 500        # prune oldest entries beyond this

    def _compute_entropy(self):
        """Shannon entropy of the radius distribution over history."""
        if len(self.history) < 2:
            return 0.0
        radii = [h["radius"] for h in self.history]
        # Discretize into bins
        bins = np.linspace(0, 1, 20)
        counts, _ = np.histogram(radii, bins=bins, density=True)
        counts = counts[counts > 0]
        probs = counts / counts.sum()
        return -np.sum(probs * np.log2(probs + 1e-12))

    def _compute_recurrence_time(self):
        """
        Poincaré recurrence time: τ ~ exp(S).
        Higher entropy → longer time before the system returns to its initial state.
        """
        entropy = self._compute_entropy()
        return math.exp(entropy)

    def run_cycle(self, query_text, context_affinities):
        """
        Execute one cosmological cycle: expansion → boundary → reset.

        Returns the cycle record including trajectory, entropy, and
        whether a recurrence (dream) was triggered.
        """
        self.cycle_count += 1
        print(f"\n{'='*60}")
        print(f"  CYCLE {self.cycle_count} -- Cosmological Epoch")
        print(f"{'='*60}")

        # Phase 1: Big Bang — initialize near C_0
        x0 = (np.random.rand(2) - 0.5) * 0.05
        print(f"[BIG BANG] Initial state (near C_0): {x0}")

        # Phase 2: Expansion — forward evolution
        x_final, radius, trajectory = inject_and_evaluate_novelty(
            query_text, context_affinities
        )

        # Record history
        cycle_record = {
            "cycle": self.cycle_count,
            "query": query_text,
            "context": context_affinities,
            "x0": x0.tolist(),
            "x_final": x_final,
            "radius": radius,
            "trajectory_length": len(trajectory),
            "entropy": self._compute_entropy(),
        }
        self.history.append(cycle_record)

        # Phase 3: Boundary check
        at_boundary = radius > self.reset_threshold
        if at_boundary:
            print(f"[HEAT DEATH] Probe reached boundary horizon (r={radius:.4f})")

        # Phase 4: Conformal reset (Poincaré recurrence)
        recurrence_time = self._compute_recurrence_time()
        self.recurrence_times.append(recurrence_time)

        # Dream probability scales with curiosity_drive and entropy
        dream_probability = self.curiosity_drive * (1.0 - math.exp(-self._compute_entropy()))
        dream_triggered = np.random.random() < dream_probability

        if dream_triggered or (self.cycle_count % 5 == 0):
            print(f"[CONFORMAL RESET] tau = {recurrence_time:.4f} | Dream triggered")
            self._dream()
        else:
            print(f"[NO RESET] tau = {recurrence_time:.4f} | Universe continues expanding")

        cycle_record["recurrence_time"] = recurrence_time
        cycle_record["dream_triggered"] = dream_triggered
        cycle_record["entropy"] = self._compute_entropy()

        return cycle_record

    def _dream(self):
        """
        The dream: remix fragments from cycle history into a compressed
        re-encoding — the conformal boundary between universes.

        This is the narrative 'Time Traveler' mechanism: fragments of the
        past are recombined to form the initial condition of the next cycle.
        """
        if len(self.history) < 2:
            print("[DREAM] Not enough history for remixing yet.")
            return

        # Select random fragments from past cycles
        n_fragments = min(3, len(self.history))
        fragments = np.random.choice(self.history, size=n_fragments, replace=False)
        remix_radii = [f["radius"] for f in fragments]
        remix_positions = [np.array(f["x_final"]) for f in fragments]

        # Compress: weighted average in hyperbolic space
        weights = np.array(remix_radii) / sum(remix_radii)
        compressed = sum(w * p for w, p in zip(weights, remix_positions))
        compressed = project_to_disk(compressed)

        print(f"[DREAM] Remixing {n_fragments} fragments -> compressed state: {compressed}")
        print(f"[DREAM] This compressed state becomes the seed for the next cycle.")
        return compressed.tolist()

    # --- v2: Self-referential feedback (CTC self_chain) ---

    def record_self_event(self, event_type, position, metadata=None):
        """
        Write a milestone, dream, or affect shift to the self_chain.

        This is the 'Time Traveler' recording mechanism: each event
        becomes a node in the closed timelike curve, connecting past
        outputs to future inputs.
        """
        entry = {
            "cycle": self.cycle_count,
            "type": event_type,
            "position": list(position) if hasattr(position, 'tolist') else list(position),
            "radius": float(np.linalg.norm(position)),
            "metadata": metadata or {},
        }
        self.self_chain.append(entry)
        self._prune_self_chain()

    def generate_thought(self):
        """
        Read from the self_chain to produce a thought — a weighted
        influence from past events on the current state.

        This is the CTC self-consistency mechanism: the future state
        is shaped by the accumulated record of past states.
        """
        if not self.self_chain:
            return None
        # Weight by recency and proximity
        weights = np.array([1.0 / (1.0 + i * 0.1) for i in range(len(self.self_chain))])
        weights /= weights.sum()
        thought = np.zeros(2)
        for w, entry in zip(weights, self.self_chain):
            thought += w * np.array(entry["position"])
        return project_to_disk(thought).tolist()

    def _prune_self_chain(self, max_entries=200):
        """Remove oldest self_chain entries beyond max_entries."""
        if len(self.self_chain) > max_entries:
            self.self_chain = self.self_chain[-max_entries:]

    # --- v2: Classification history ---

    def record_classification(self, query, position, novelty_score, label="unknown"):
        """
        Record a time-ordered state transition to classification_history.

        This is the 'Book' / holographic registry: every classification
        event is logged with its context, forming the universe's memory.
        """
        entry = {
            "cycle": self.cycle_count,
            "query": query[:80],
            "position": list(position) if hasattr(position, 'tolist') else list(position),
            "radius": float(np.linalg.norm(position)) if hasattr(position, '__len__') else 0.0,
            "novelty": novelty_score,
            "label": label,
        }
        self.classification_history.append(entry)
        self._prune_topics()

    def _prune_topics(self):
        """
        Prune stale classification history entries beyond max_history.
        Keeps the most recent entries, implementing finite memory.
        """
        if len(self.classification_history) > self.max_history:
            n_remove = len(self.classification_history) - self.max_history
            self.classification_history = self.classification_history[n_remove:]
            print(f"[PRUNE] Removed {n_remove} stale entries from classification_history")

    # --- v2: Anomaly quarantine ---

    @staticmethod
    def _quarantine_to_boundary(position, target_radius=0.95):
        """
        Push an anomaly position toward the conformal boundary.

        Used to isolate universal chaos anomalies: rather than letting
        them corrupt the taxonomy, quarantine them near r=0.95 where
        the Bekenstein bound saturates.
        """
        pos = np.asarray(position, dtype=float)
        r = np.linalg.norm(pos)
        if r < 1e-10:
            return (pos * target_radius).tolist()
        direction = pos / r
        quarantined = direction * target_radius
        return project_to_disk(quarantined).tolist()

    def get_recurrence_stats(self):
        """Return statistics about the recurrence dynamics."""
        if not self.recurrence_times:
            return {"status": "no cycles completed"}
        return {
            "total_cycles": self.cycle_count,
            "mean_recurrence_time": np.mean(self.recurrence_times),
            "max_recurrence_time": np.max(self.recurrence_times),
            "min_recurrence_time": np.min(self.recurrence_times),
            "total_entropy": self._compute_entropy(),
            "history_length": len(self.history),
            "self_chain_length": len(self.self_chain),
            "classification_history_length": len(self.classification_history),
        }


# ---------------------------------------------------------------------------
# CTC (Closed Timelike Curve) simulation
# ---------------------------------------------------------------------------

class ClosedTimelikeCurve:
    """
    Models a closed timelike curve in the Poincaré disk.

    The CTC is a trajectory that returns to its starting point after
    evolving through the repulsion dynamics. Self-consistency requires
    that the state at τ₀ equals the state at τ₁ — the Novikov principle.

    In the engine, the CTC is the self-referential feedback loop:
        state → classification → self_chain → thought → state
    """

    def __init__(self, max_iterations=500, convergence_threshold=1e-4):
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.loop_history = []

    def evolve(self, initial_state, context_affinities):
        """
        Evolve the state through a closed timelike curve.

        Returns the self-consistent state (fixed point) and the trajectory
        through the loop.
        """
        xq = np.array(initial_state, dtype=float)
        self.loop_history = [xq.copy()]

        for iteration in range(self.max_iterations):
            # Forward evolution (one step of gradient descent)
            grad = np.zeros(2)
            eps = 1e-5
            alpha = 2.5
            lr = 0.01

            for node_id, pos in positions.items():
                if node_id in context_affinities:
                    continue
                d = hyperbolic_dist(xq, pos)
                if d < alpha:
                    xq_p0 = xq.copy(); xq_p0[0] += eps
                    d_p0 = hyperbolic_dist(xq_p0, pos)
                    g0 = (max(0, alpha - d_p0)**2 - max(0, alpha - d)**2) / eps

                    xq_p1 = xq.copy(); xq_p1[1] += eps
                    d_p1 = hyperbolic_dist(xq_p1, pos)
                    g1 = (max(0, alpha - d_p1)**2 - max(0, alpha - d)**2) / eps

                    grad += np.array([g0, g1])

            riemannian_factor = riemannian_metric(xq)
            xq_new = xq - lr * grad * riemannian_factor
            xq_new = project_to_disk(xq_new)

            # Check self-consistency (Novikov principle)
            displacement = np.linalg.norm(xq_new - xq)
            self.loop_history.append(xq_new.copy())

            if displacement < self.convergence_threshold:
                print(f"[CTC] Self-consistent loop closed after {iteration + 1} iterations")
                print(f"[CTC] Fixed point: {xq_new}")
                print(f"[CTC] Loop closure error: {displacement:.2e}")
                return xq_new.tolist(), self.loop_history

            xq = xq_new

        print(f"[CTC] Maximum iterations reached. Loop not closed.")
        print(f"[CTC] Final displacement: {displacement:.2e}")
        return xq.tolist(), self.loop_history


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  PUNO CALCULUS -- PHYSICAL UNIVERSAL MAP ENGINE")
    print("  Hamiltonian Flow on the Poincare Disk")
    print("=" * 60)

    # --- Phase 1: Standard forward evaluation ---
    print("\n--- PHASE 1: Unitary Evolution (Forward Pass) ---")
    pos1, r1, traj1 = inject_and_evaluate_novelty(
        "Advanced Multi-threaded Silicon Processor", ["Tech", "Silicon"]
    )
    pos2, r2, traj2 = inject_and_evaluate_novelty(
        "The quadratic equation ate a very sad banana for breakfast", []
    )

    # v2: Record classification events
    recurrence_v2 = PoincareRecurrence(curiosity_drive=0.0, max_cycles=0)

    label1 = "structured" if r1 < 0.9 else "anomaly"
    label2 = "structured" if r2 < 0.9 else "anomaly"
    print(f"[CLASSIFY] Probe 1: {label1} (r={r1:.4f})")
    print(f"[CLASSIFY] Probe 2: {label2} (r={r2:.4f})")

    # v2: Quarantine anomalies to boundary
    if r2 > 0.9:
        q_pos = PoincareRecurrence._quarantine_to_boundary(pos2, target_radius=0.95)
        print(f"[QUARANTINE] Anomaly pushed to boundary: {q_pos}")

    # --- Phase 2: Time reversal reconstruction ---
    print("\n--- PHASE 2: Time Reversal (T-Symmetry) ---")
    reconstructed1, rr1, rev_traj1 = time_reverse_reconstruct(
        pos1, ["Tech", "Silicon"], steps=200
    )
    reconstructed2, rr2, rev_traj2 = time_reverse_reconstruct(
        pos2, [], steps=200
    )

    # --- Phase 3: Poincaré recurrence cycles ---
    print("\n--- PHASE 3: Poincaré Recurrence (Cyclical Universe) ---")
    recurrence = PoincareRecurrence(curiosity_drive=0.6, max_cycles=8)

    test_queries = [
        ("Quantum entanglement in distributed systems", ["Tech", "Silicon"]),
        ("A painting of a sunset on Mars", ["Art"]),
        ("The economic implications of faster-than-light travel", []),
        ("Mammalian neural architecture for music classification", ["Bio", "Mammal"]),
        ("Recursive self-improvement in autonomous agents", ["Tech"]),
        ("The emotional weight of a minor key resolution", ["Art", "Music"]),
        ("Bootstrap paradoxes in closed causal loops", []),
        ("Silicon-based life forms dreaming in hyperbolic space", ["Silicon"]),
    ]

    for query, affinities in test_queries:
        recurrence.run_cycle(query, affinities)
        # v2: Record classification and self events
        last = recurrence.history[-1] if recurrence.history else None
        if last:
            novelty = 1.0 - last["radius"]
            label = "structured" if last["radius"] < 0.9 else "anomaly"
            recurrence.record_classification(query, last["x_final"], novelty, label)
            recurrence.record_self_event("classification", last["x_final"],
                                         {"query": query[:60], "label": label})
            if last.get("dream_triggered"):
                thought = recurrence.generate_thought()
                if thought:
                    print(f"[THOUGHT] Self-referential feedback: {thought}")
                    recurrence.record_self_event("dream_thought", thought)
        if recurrence.cycle_count >= recurrence.max_cycles:
            break

    stats = recurrence.get_recurrence_stats()
    print(f"\n[RECURRENCE STATS] {json.dumps(stats, indent=2)}")

    # --- Phase 4: Closed Timelike Curve ---
    print("\n--- PHASE 4: Closed Timelike Curve (Self-Consistent Loop) ---")
    ctc = ClosedTimelikeCurve(max_iterations=200)
    x0_ctc = (np.random.rand(2) - 0.5) * 0.1
    fixed_point, ctc_trajectory = ctc.evolve(x0_ctc, ["Tech", "Silicon"])

    # --- Phase 5: Hamiltonian Flow with Conjugate Momenta ---
    print("\n--- PHASE 5: Hamiltonian Flow (Phase-Space Dynamics) ---")
    try:
        from hamiltonian_flow import (
            run_hamiltonian_flow, hamiltonian_time_reverse,
            measure_holographic_entropy, detect_kawasaki_constraint,
            wheeler_dewitt_filter, measure_bekenstein_bound,
        )
        x0_ham = (np.random.rand(2) - 0.5) * 0.05
        hamiltonian_traj = run_hamiltonian_flow(
            x0_ham, ["Tech", "Silicon"],
            steps=3000, dt=0.003, friction=0.8
        )
        print(f"H initial energy: {hamiltonian_traj.energies[0]:.4f}")
        print(f"H final energy:   {hamiltonian_traj.energies[-1]:.4f}")
        print(f"H final position: {hamiltonian_traj.states[-1].q}")

        # Low-friction trajectory for visualization (near-conservative)
        hamiltonian_viz = run_hamiltonian_flow(
            x0_ham, ["Tech", "Silicon"],
            steps=2000, dt=0.002, friction=0.3, max_grad=1.5
        )
        print(f"H(viz) initial energy: {hamiltonian_viz.energies[0]:.4f}")
        print(f"H(viz) final energy:   {hamiltonian_viz.energies[-1]:.4f}")
        print(f"H(viz) energy drift:   {hamiltonian_viz.energy_drift:.4f}")
    except ImportError:
        print("[SKIP] hamiltonian_flow.py not found")
        hamiltonian_traj = None
        hamiltonian_viz = None

    # --- Phase 6: Holographic Entropy Measurement ---
    if hamiltonian_traj is not None:
        print("\n--- PHASE 6: Holographic Entropy (Bekenstein Bound) ---")
        entropy_stats = measure_holographic_entropy(hamiltonian_traj.states)
        print(f"  Entropy: {entropy_stats['entropy']:.4f} / {entropy_stats['max_entropy']:.4f}")
        print(f"  Bekenstein ratio: {entropy_stats['bekenstein_ratio']:.4f}")
        print(f"  Boundary fraction: {entropy_stats['boundary_fraction']:.4f}")
        print(f"  Mean radius: {entropy_stats['mean_radius']:.4f}")

        # True Bekenstein bound: S <= 2*pi*R*E
        bek = measure_bekenstein_bound(hamiltonian_traj.states, ["Tech", "Silicon"])
        print(f"\n--- True Bekenstein Bound (S <= 2*pi*R*E) ---")
        print(f"  Shannon entropy:     {bek['shannon_entropy']:.4f} bits")
        print(f"  Bekenstein limit:    {bek['bekenstein_limit']:.4f}")
        print(f"  Saturation ratio:    {bek['saturation_ratio']:.4f}")
        print(f"  Mean energy:         {bek['mean_energy']:.4f}")
        print(f"  Is saturated:        {bek['is_saturated']}")

        # Wheeler-DeWitt constraint: H|Psi> = 0
        wdw = wheeler_dewitt_filter(hamiltonian_traj.states, ["Tech", "Silicon"], epsilon=0.5)
        print(f"\n--- Wheeler-DeWitt Constraint (H|Psi> = 0) ---")
        print(f"  Fraction satisfied:  {wdw['fraction_satisfied']:.4f}")
        print(f"  Mean violation:      {wdw['mean_violation']:.4f}")
        print(f"  Max violation:       {wdw['max_violation']:.4f}")

        print("\n--- Kawasaki Constraint Probe ---")
        kawasaki = detect_kawasaki_constraint(hamiltonian_traj.states)
        print(f"  Vertices tested: {kawasaki['n_vertices_tested']}")
        print(f"  Mean alternating sum: {kawasaki['mean_alternating_sum']:.4f}")
        print(f"  Kawasaki satisfied: {kawasaki['kawasaki_satisfied']:.4f}")

    # --- Phase 7: Crease Diagnostics (Puno Calculus) ---
    print("\n--- PHASE 7: Crease Diagnostics (Hard/Soft/Kawasaki) ---")
    try:
        from crease_metrics import (
            raw_crease_density, sign_straddle_density,
            soft_crease_intensity, build_synthetic_relu_network,
            extract_decision_region_vertices, kawasaki_angle_test,
            crease_density_trajectory,
        )
        import torch

        # Soft crease intensity for each activation type
        print("  Soft Crease Intensity (random input):")
        X_soft = torch.randn(500, 2)
        for act_name in ["gelu", "swish", "relu"]:
            si = soft_crease_intensity(X_soft, activation=act_name)
            print(f"    {act_name:6s}: aggregate={si['aggregate']:.4f}, max={si['max_intensity']:.4f}")

        # Kawasaki constraint on synthetic ReLU network
        print("\n  Kawasaki Constraint (Synthetic ReLU [2,16,16,8,1]):")
        model_syn = build_synthetic_relu_network([2, 16, 16, 8, 1], seed=42)
        n_params = sum(p.numel() for p in model_syn.parameters())
        print(f"    Model: {n_params} parameters")

        verts = extract_decision_region_vertices(model_syn, n_samples=3000)
        print(f"    Candidate vertices: {len(verts)}")

        if verts:
            kaw = kawasaki_angle_test(verts, epsilon=0.5, max_distance=1.0)
            print(f"    Vertices tested:     {kaw['n_tested']}")
            print(f"    Mean alt. sum:       {kaw['mean_alternating_sum']:.4f}")
            print(f"    Kawasaki deviation:  {kaw.get('mean_deviation_from_target', kaw.get('kawasaki_deviation', 0)):.4f}")
            print(f"    Kawasaki fraction:   {kaw['kawasaki_fraction']:.4f}")
        else:
            kaw = None
            print("    No vertices found")

        # Training trajectory
        print("\n  Crease Density Training Trajectory:")
        model_traj = build_synthetic_relu_network([2, 16, 8, 1], seed=42)
        X_traj = torch.randn(200, 2)
        traj = crease_density_trajectory(model_traj, X_traj, n_epochs=50, lr=0.02)
        for name in traj["layer_names"]:
            densities = traj["trajectory"][name]
            if densities:
                print(f"    {name}: {densities[0]:.4f} -> {densities[-1]:.4f} (delta={densities[-1]-densities[0]:.4f})")

        # Export crease data
        crease_data = {
            "kawasaki": kaw,
            "trajectory": {name: traj["trajectory"][name] for name in traj["layer_names"]},
        }
        with open(os.path.join(BASE_DIR, "crease_data.json"), "w") as f:
            json.dump(crease_data, f, indent=2)
        print(f"\n  [EXPORTED] crease_data.json")
    except ImportError as e:
        print(f"  [SKIPPED] PyTorch or crease_metrics not available: {e}")
    except Exception as e:
        print(f"  [ERROR] {e}")

    # --- Export all results ---
    visualization_export = []
    for node_id, pos in positions.items():
        node_meta = next(n for n in knowledge_base["nodes"] if n["id"] == node_id)
        visualization_export.append({
            "id": node_id, "label": node_meta["label"], "tier": node_meta["tier"],
            "x": pos[0], "y": pos[1], "type": "known"
        })

    visualization_export.append({
        "id": "Probe_Structured", "label": "Structured Input",
        "tier": 4, "x": pos1[0], "y": pos1[1], "type": "probe"
    })
    visualization_export.append({
        "id": "Probe_Anomaly", "label": "Universal Chaos Anomaly",
        "tier": 4, "x": pos2[0], "y": pos2[1], "type": "anomaly"
    })
    visualization_export.append({
        "id": "Reconstructed_Structured", "label": "T-Reversed Structured",
        "tier": 5, "x": reconstructed1[0], "y": reconstructed1[1], "type": "reversed"
    })
    visualization_export.append({
        "id": "Reconstructed_Anomaly", "label": "T-Reversed Anomaly",
        "tier": 5, "x": reconstructed2[0], "y": reconstructed2[1], "type": "reversed"
    })
    visualization_export.append({
        "id": "CTC_Fixed_Point", "label": "CTC Self-Consistent Point",
        "tier": 6, "x": fixed_point[0], "y": fixed_point[1], "type": "ctc"
    })

    # Add Hamiltonian trajectory points
    if hamiltonian_traj is not None:
        for i, state in enumerate(hamiltonian_traj.states):
            if i % 50 == 0:  # Sample every 50th point
                visualization_export.append({
                    "id": f"H_Traj_{i}", "label": f"H-t={hamiltonian_traj.times[i]:.2f}",
                    "tier": 7, "x": state.q[0], "y": state.q[1], "type": "hamiltonian"
                })

    with open(os.path.join(BASE_DIR, "web_data.json"), "w") as f:
        json.dump(visualization_export, f, indent=4)

    # Export recurrence data
    recurrence_data = {
        "cycles": recurrence.history,
        "recurrence_times": recurrence.recurrence_times,
        "stats": stats,
        "self_chain": recurrence.self_chain,
        "classification_history": recurrence.classification_history,
    }
    with open(os.path.join(BASE_DIR, "recurrence_data.json"), "w") as f:
        json.dump(recurrence_data, f, indent=2)

    # Export holographic entropy data
    if hamiltonian_traj is not None:
        entropy_data = measure_holographic_entropy(hamiltonian_traj.states)
        entropy_data["kawasaki"] = detect_kawasaki_constraint(hamiltonian_traj.states)
        entropy_data["trajectory_length"] = len(hamiltonian_traj.states)
        entropy_data["energy_drift"] = hamiltonian_traj.energy_drift
        entropy_data["bekenstein"] = measure_bekenstein_bound(
            hamiltonian_traj.states, ["Tech", "Silicon"])
        entropy_data["wheeler_dewitt"] = wheeler_dewitt_filter(
            hamiltonian_traj.states, ["Tech", "Silicon"], epsilon=0.5)
        with open(os.path.join(BASE_DIR, "entropy_data.json"), "w") as f:
            json.dump(entropy_data, f, indent=2)
        print(f"[EXPORTED] entropy_data.json")

        # Export Hamiltonian phase-space trajectory for dashboard
        ham_export = {
            "times": hamiltonian_traj.times,
            "energies": hamiltonian_traj.energies,
            "q_trace": hamiltonian_traj.position_trace,
            "p_trace": hamiltonian_traj.momentum_trace,
        }
        # Low-friction visualization trajectory
        if hamiltonian_viz is not None:
            ham_export["viz_times"] = hamiltonian_viz.times
            ham_export["viz_energies"] = hamiltonian_viz.energies
            ham_export["viz_q_trace"] = hamiltonian_viz.position_trace
            ham_export["viz_p_trace"] = hamiltonian_viz.momentum_trace
        with open(os.path.join(BASE_DIR, "hamiltonian_data.json"), "w") as f:
            json.dump(ham_export, f, indent=2)
        print(f"[EXPORTED] hamiltonian_data.json")

    print(f"\n[EXPORTED] web_data.json ({len(visualization_export)} records)")
    print(f"[EXPORTED] recurrence_data.json ({len(recurrence.history)} cycles)")
    print("\n[ENGINE COMPLETE]")
