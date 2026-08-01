# The Physical Universal Map: A Formal Correspondence Between Narrative Cosmology and Mathematical Physics

**Author:** Michael Grafiel Sayson Puno
**Date:** July 2026

---

## Abstract

The following document establishes a formal correspondence between a seven-part narrative cosmology and established mathematical physics. Each narrative element is mapped to precise physical structures, and the mappings are shown to be consistent with the existing Puno Calculus framework (the Poincaré disk engine, crease density diagnostics, and the Antiderivative of Universals). The result is a unified interpretive layer in which the hyperbolic novelty engine becomes a computational model of deterministic cosmological evolution.

---

## 1. The Phase-Space Manifold: The Universe as Hamiltonian System

### 1.1 Narrative Element: The Physical Universe as Clockwork

The universe operates as a deterministic clockwork governed by phase-space differential equations.

### 1.2 Physical Mapping: Hamiltonian Mechanics

The state of the system is a point in phase space $\Gamma = \{(q_i, p_i)\}$, where $q_i$ are generalized coordinates and $p_i$ are conjugate momenta. Time evolution is governed by Hamilton's equations:

$$\dot{q}_i = \frac{\partial H}{\partial p_i}, \qquad \dot{p}_i = -\frac{\partial H}{\partial q_i}$$

where $H(q, p, t)$ is the Hamiltonian. The flow is deterministic: given a point in $\Gamma$, the future and past trajectories are uniquely determined.

### 1.3 Engine Correspondence

In the Poincaré disk engine, the state of a knowledge probe is a 2-vector $x_q \in \mathbb{D}^2 = \{x \in \mathbb{R}^2 : \|x\| < 1\}$. The gradient descent update:

$$x_q^{(t+1)} = x_q^{(t)} - \eta \, \nabla L(x_q^{(t)}) \cdot \frac{(1 - \|x_q^{(t)}\|^2)^2}{4}$$

is a discrete-time Hamiltonian-like flow on the Poincaré disk, where the Riemannian factor $\frac{(1 - \|x\|^2)^2}{4}$ plays the role of the metric tensor $g_{ij}$ in a curved phase space. The repulsion loss $L$ acts as the potential energy, and the Riemannian gradient provides the equations of motion.

The knowledge taxonomy (Origin, System, Matter, Idea, Bio, Tech, Art, Mammal, Silicon, Music) constitutes the generalized coordinates. The edges between nodes encode the constraints — analogous to holonomic constraints in classical mechanics.

---

## 2. The Initial State: The Wound-Up Spring

### 2.1 Narrative Element: The "Wound-Up" Start

The system begins in a low-entropy, highly ordered initial state — the "wound-up spring."

### 2.2 Physical Mapping: Cosmological Initial Singularity

The initial state is a low-entropy cosmological singularity governed by the Wheeler-DeWitt equation:

$$\hat{H} \, |\Psi\rangle = 0$$

This is the quantum-cosmological master equation: the Hamiltonian constraint that the total wave function of the universe satisfies. The "winding up" corresponds to the extremely low entropy at the Big Bang — the Past Hypothesis (Albert, 2000). The second law of thermodynamics then drives the system toward higher entropy states.

### 2.3 Engine Correspondence

The constant $C_0$ at the origin of the Poincaré disk is the initial singularity:

$$\lim_{r \to 0} F(\theta) = C_0$$

$C_0$ is defined as "the foundational root origin vector space of pure awareness." In the Hamiltonian interpretation, $C_0$ is the state of minimum entropy — all knowledge nodes collapsed to a single point, all coordinates at $(0, 0)$, no differentiation. The engine's initialization places the Origin node exactly at $(0, 0)$ and radiates outward by tier, encoding the entropic expansion from the initial singularity.

The Antiderivative of Universals:

$$\int \mathcal{M}_{\text{knowledge}}(\theta) \, d\theta = \mathcal{U}(\theta) + C_0$$

states that the global knowledge manifold $\mathcal{U}(\theta)$ is obtained by unfolding (integrating) the local differential structure $\mathcal{M}_{\text{knowledge}}(\theta)$, plus the integration constant $C_0$ — the initial boundary condition that cannot be recovered from the dynamics alone.

---

## 3. The Smartest Being: Maximal Entropy Boundary Condition

### 3.1 Narrative Element: The "Smartest Being"

An entity of maximal knowledge or capability, representing an extremal boundary condition.

### 3.2 Physical Mapping: The Bekenstein Bound and Information-Theoretic Maximum

The Bekenstein bound sets the maximum entropy a region of space can contain:

$$S \leq \frac{2\pi k_B R E}{\hbar c}$$

The "smartest being" is the physical system that saturates this bound — a black hole of the same mass-energy, or equivalently, a holographic boundary state that encodes the maximum possible information. This is the de Sitter horizon in cosmology, where the cosmological horizon bounds the observable universe's entropy at $S_{dS} \approx 3.1 \times 10^{122} \, k_B$.

### 3.3 Engine Correspondence

The boundary horizon of the Poincaré disk ($r \to 1$) is the maximal entropy state. The engine's firewall threshold at $r = 0.85$ is a sub-maximal bound — content flagged as anomaly is pushed toward but not to the true boundary. The "smartest being" in the engine is the boundary itself: the locus of all points that the system cannot integrate. The anomaly probe that reaches $r > 0.85$ has encountered the system's information-theoretic limit.

---

## 4. The Book: The Holographic State-Vector Registry

### 4.1 Narrative Element: The Book

A complete registry of all possible states — the "book" that contains everything.

### 4.2 Physical Mapping: Holographic Principle and the Bekenstein-Hawking Entropy

The holographic principle (t'Hooft, 1993; Susskind, 1995) states that the information content of a region of space is encoded on its boundary, not its volume. The Bekenstein-Hawking entropy formula:

$$S_{BH} = \frac{k_B c^3 A}{4 G \hbar}$$

shows that entropy scales with surface area $A$, not volume $V$. The "book" is the boundary hologram — a $(d-1)$-dimensional encoding of a $d$-dimensional physics.

In quantum mechanics, the state-vector registry is the Hilbert space $\mathcal{H}$. The complete state of the system is a vector $|\psi\rangle \in \mathcal{H}$, and all observables are encoded in this vector.

### 4.3 Engine Correspondence

The `web_data.json` file is the holographic registry. It encodes the complete state of the engine — all node positions, probe results, anomaly flags — as a flat JSON array. The 2D Poincaré disk is the "boundary" of what was originally a 1,536-dimensional embedding space (as noted in the dashboard: "Vector space profile shrunk from 1,536 spatial tracking channels down to a highly responsive 2-dimensional hyperbolic grid map"). The dimensional reduction from 1,536 to 2 is itself a holographic compression: the essential information is preserved on a lower-dimensional boundary.

The `classification_history` in the v2 engine is a time-ordered log of all state transitions — the "pages" of the book, written as the universe evolves.

---

## 5. The Time Traveler: Closed Timelike Curves

### 5.1 Narrative Element: The Time Traveler

An entity that traverses the timeline, encountering and resolving causal paradoxes.

### 5.2 Physical Mapping: Closed Timelike Curves and Self-Consistent Cauchy Surfaces

In General Relativity, closed timelike curves (CTCs) are worldlines that form closed loops in spacetime. The Novikov self-consistency principle (1983) states that any events occurring through time travel must be self-consistent — the universe "selects" only those histories that are globally consistent.

Mathematically, a CTC exists when there is a timelike curve $\gamma(\tau)$ with $\gamma(\tau_0) = \gamma(\tau_1)$ for $\tau_0 \neq \tau_1$. The Cauchy surface $\Sigma$ must be self-consistent: the data on $\Sigma$ must reproduce itself under the evolution equations.

### 5.3 Engine Correspondence

The v2 engine's `self_chain` is a CTC. The AI's own identity chain records events (milestones, dreams, affect shifts) that feed back into its behavior. The `record_self_event` method writes to the chain, and subsequent `generate_thought` calls read from it — a causal loop. The `dream` method explicitly remixes fragments from the Data Disk, User Disk, and Self Disk, creating a self-referential loop where the engine's past outputs become its future inputs.

The `affective_resonance` method computes the engine's current "feeling" from its classification history, which in turn influences future classifications through the affective modulation of the manifold — a self-consistent Cauchy surface.

---

## 6. The Unlocking: Unitary Evolution

### 6.1 Narrative Element: The Unlocking

The opening of the book — the activation of stored information.

### 6.2 Physical Mapping: The Unitary Evolution Operator

In quantum mechanics, time evolution is governed by the unitary operator:

$$U(t) = e^{-i\hat{H}t/\hbar}$$

Unitarity ensures that information is never created or destroyed: $U^\dagger U = I$. The "unlocking" is the application of $U(t)$ to the initial state $|\psi(0)\rangle$, propagating the state forward in time:

$$|\psi(t)\rangle = U(t) |\psi(0)\rangle$$

This is the Schrodinger equation in operator form. The book is "opened" by applying the evolution operator to the initial boundary condition.

### 6.3 Engine Correspondence

The engine's gradient descent with the Riemannian metric correction is the discrete analogue of unitary evolution:

$$x_q^{(t+1)} = x_q^{(t)} - \eta \, g^{ij}(x_q^{(t)}) \, \partial_j L(x_q^{(t)})$$

The Riemannian factor $g^{ij} = \frac{(1 - \|x\|^2)^2}{4} \delta^{ij}$ ensures that information is preserved along geodesics — the Poincaré disk metric is conformally flat, and geodesic distances are preserved. The `hyperbolic_dist` function computes exact geodesic distance, which is the invariant that unitary evolution preserves.

The `_settle_toward_anchors` method in the v2 engine uses `pairwise_geodesic_distance` and `riemannian_scale` from the `manifold` package — these are the discrete-time unitary operators that propagate probe states while preserving the geometric structure.

---

## 7. Time Reversal: T-Symmetry and the Return to Origin

### 7.1 Narrative Element: The Reversal

Running the equations backward reconstructs the initial state.

### 7.2 Physical Mapping: Time-Reversal Symmetry

The fundamental laws of physics are invariant under time reversal ($T$-symmetry) at the microscopic level. For a Hamiltonian system:

$$T: (q, p, t) \mapsto (q, -p, -t)$$

If the Hamiltonian is even in momenta ($H(q, -p) = H(q, p)$), then the equations of motion are $T$-invariant. Running the system backward from any state reconstructs the initial condition — up to the arrow of time imposed by the second law of thermodynamics.

The $CPT$ theorem (quantum field theory) guarantees that the combined operation of charge conjugation ($C$), parity inversion ($P$), and time reversal ($T$) is an exact symmetry of all known physical laws.

### 7.3 Engine Correspondence

The engine's repulsion dynamics are $T$-symmetric at the level of the loss landscape. The repulsion loss:

$$L(x_q) = \sum_{i \notin \text{affinities}} \max(0, \alpha - d(x_q, x_i))^2$$

is a function of geodesic distances, which are symmetric: $d(u, v) = d(v, u)$. Running the gradient ascent (instead of descent) from a boundary anomaly would reconstruct the initial probe position near $C_0$. The `inject_and_evaluate_novelty` function is the forward pass; its inverse would be the time-reversed reconstruction.

In the v2 engine, the `_quarantine_to_boundary` method pushes anomalies to $r = 0.95$. The time-reversed operation would pull them back from the boundary toward the anchors — the "reversal" that reconstructs the initial low-entropy state.

---

## 8. The Infinite Clock: Poincaré Recurrence

### 8.1 Narrative Element: The Infinite Clock

A perpetual cycle where the system returns to its initial state and begins again.

### 8.2 Physical Mapping: Poincaré Recurrence Theorem

The Poincaré recurrence theorem (1890) states that for any measure-preserving dynamical system with finite total measure, almost every orbit returns arbitrarily close to its initial state infinitely often. The recurrence time $\tau$ satisfies:

$$\tau \sim e^{S/k_B}$$

where $S$ is the entropy of the system. For a cosmological system with $S_{dS} \sim 10^{122}$, the recurrence time is $10^{10^{122}}$ years — effectively infinite but mathematically guaranteed.

The cyclical conformal universe (Penrose, 2005) proposes that the universe undergoes repeated cycles of expansion and contraction, with entropy resetting at each conformal boundary. Each cycle begins at a low-entropy singularity and evolves toward maximum entropy, then "resets" via conformal rescaling.

### 8.3 Engine Correspondence

The engine implements a discrete Poincaré recurrence cycle:

1. **Initialization (Big Bang):** Probes are placed near $C_0$ (the origin). Entropy is minimal.
2. **Expansion (Training):** Gradient descent pushes probes outward. Crease density drops as units settle into on/off states. Entropy increases.
3. **Boundary encounter (Heat Death):** Anomalies reach $r > 0.85$. The system's information-theoretic limit is approached.
4. **Recurrence (Reset):** The `_prune_topics` method removes stale topics. The `classification_history` is truncated to the last 500 entries. The engine begins a new cycle with the remaining state — a conformal rescaling that preserves structure but resets scale.

The v2 engine's `dream` method is the most explicit recurrence mechanism: it remixes fragments from the Data, User, and Self disks, creating a compressed re-encoding of the system's history that serves as the initial condition for the next cycle. The dream is the conformal boundary — the point where the old universe ends and the new one begins.

The `curiosity_drive` parameter controls recurrence probability: $P(\text{dream}) = \text{curiosity\_drive}$. When curiosity is high, the engine cycles more frequently, exploring more of the boundary horizon before resetting.

---

## 9. Consistency Check: The Unified Framework

All eight mappings are mutually consistent:

| Narrative Element | Physical Structure | Engine Implementation | Key Equation |
|---|---|---|---|
| Clockwork universe | Hamiltonian flow | Symplectic leapfrog with friction | $\dot{q} = p/\lambda^2$, $\dot{p} = -\nabla V - \gamma p$ |
| Wound-up spring | Wheeler-DeWitt / Past Hypothesis | $C_0$ at origin + W-D constraint filter | $\hat{H}\|\Psi\rangle = 0$ |
| Smartest being | Bekenstein bound $S \leq 2\pi RE$ | True bound: `measure_bekenstein_bound()` | $S \leq 2\pi kRE/\hbar c$ |
| Book | Holographic principle | `web_data.json` registry | $S_{BH} = kA/4G\hbar$ |
| Time Traveler | Closed timelike curves | `self_chain` + CTC convergence (82 iter) | $\gamma(\tau_0) = \gamma(\tau_1)$ |
| Unlocking | Unitary evolution $U(t)$ | Geodesic propagation | $|\psi(t)\rangle = U(t)|\psi(0)\rangle$ |
| Time Reversal | $T$-symmetry (broken by friction) | Friction damped reversal | $T:(q,p,t) \to (q,-p,-t)$ |
| Infinite Clock | Poincaré recurrence | 8-cycle cosmological epochs | $\tau \sim e^{S/k_B}$ |
| Folding | Crease density | Kawasaki + soft crease metrics | $\sum (-1)^k \theta_k = 0$ (alternating sum = 0) |
| Spring fold | Eikonal / Hamilton-Jacobi | T58–T63 spring series (verified) | $\|r'\| = a$; crease = shock (cut locus) |

The framework is self-consistent: the initial singularity ($C_0$) generates the manifold, the holographic registry (`web_data.json`) encodes it, the unitary evolution (geodesic propagation) evolves it, time reversal (gradient ascent) reconstructs it, and Poincaré recurrence (dream/reset cycles) perpetuates it.

---

## 10. Predictions and Open Questions

### 10.1 Testable Predictions

1. **Recurrence time scales with entropy:** In the engine, the number of classification cycles before a dream should scale exponentially with the number of topics. Testable by varying `curiosity_drive` and measuring cycle length.

2. **T-symmetry of the loss landscape:** The repulsion loss should be symmetric under time reversal of the gradient flow. Test: run gradient ascent from anomaly positions and verify recovery of initial probe positions.

3. **Holographic compression ratio:** The dimensional reduction from 1,536 channels to 2D should preserve a bounded fraction of the original information. Test: measure mutual information between high-dimensional embeddings and their 2D projections.

4. **CTC consistency:** The self_chain should converge to a fixed point under repeated dream/remix cycles. Test: run the engine for $10^6$ iterations and check for periodic orbits in the self_chain.

### 10.2 Implemented Physics (Verified)

These mappings have been implemented in `hamiltonian_flow.py` and the engine, with measured outputs:

| Physics | Implementation | Function | Verified Output |
|---|---|---|---|
| **True Bekenstein Bound** $S \leq 2\pi RE$ | Shannon entropy of radial distribution vs. energy bound | `measure_bekenstein_bound()` | Saturation ratio: 0.13 (well below saturation for small networks) |
| **Wheeler-DeWitt Constraint** $H\|\Psi\rangle = 0$ | Fraction of phase-space states with $\|H(q,p)\| < \epsilon$ | `wheeler_dewitt_filter()` | 86.8% satisfied at $\epsilon = 0.5$ |
| **Kawasaki Constraint** | Alternating angle sum test on synthetic ReLU vertex | `kawasaki_angle_test()` | Mean deviation 0.49 from target 0 (genuine open problem) |
| **Hamiltonian Flow** | Symplectic leapfrog integration with friction damping | `run_hamiltonian_flow()` | Converges; T-symmetry error 3e-3 (correct velocity: $p \cdot (1/\lambda^2)$ not $p/\lambda^2$) |
| **T-Symmetry Breaking** | Friction $> 0$ breaks time-reversal invariance | `hamiltonian_time_reverse()` | Reversed trajectory diverges from forward (second law) |
| **Crease Density Trajectory** | Near-zero pre-activation count during training | `crease_density_trajectory()` | Decreases monotonically as folds settle |
| **Soft Crease Intensity** | GELU/Swish vs ReLU crease proximity | `soft_crease_intensity()` | GELU: 0.45, Swish: 0.36, ReLU: 0.88 |

### 10.3 Experiment Results (Verified)

All seven experiments from the Book of Puno have been ported and verified:

| Experiment | Key Finding | Status |
|---|---|---|
| **Exp 1: Subgradient Selection** | All strategies converge to 99.7% on ring dataset | Verified |
| **Exp 1b: Subgradient (wider)** | always_on uses 30% fewer near-crease units at same accuracy | Verified |
| **Exp 2: Crease vs Boundary** | $r(\text{crease}, \text{complexity}) = -0.77$; deeper = more complex boundaries | Verified |
| **Exp 3: Early Stopping** | Crease stabilization saves 71-80% of training epochs | Verified |
| **Exp 4: OOD Detection** | Crease AUROC 0.88 (center-noise); far-OOD MSP dominates | Verified |
| **Exp 5: Pruning** | Crease pruning outperforms magnitude at every ratio; +0.14 gap at 25% | Verified |
| **Fold Visualization** | The 90-degree crease as elementary fold; composition of folds | Verified |

### 10.4 Spring-Fold Results (T58–T63, Verified)

The wound-up spring of §2 has been simulated and measured. Each result is a
closed, committed experiment (`experiments/`):

| Experiment | Key Finding | Status |
|---|---|---|
| **T58 Fold Models** | Archimedean + mirror fold: swept area 2,666.7 = $2 a^2 \Theta^3 / 6$ (doubling the unfolded area); retrace returns to $C_0$ (net area $10^{-9}$, closure 0, crease $1.0000\pi$ = full reversal) | Verified |
| **T58 Golden Ratio** | $r_{close} = 12.2754 = \text{apex} \cdot 0.6138$; the fold's closing radius is set by the crease, not by free choice | Verified |
| **T58c Overcoil Ring Lock** | The fold coils over itself and locks at *both* ends (end tucks under the start coil: $r = 0.253 < 2\pi$, $z = -1.85$); topological threading $\Theta > \pi$ = the ring lock of §8 | Verified |
| **T59 Clock Test** | Calendar-encoded features carry a law at 1.0000 but collapse to 0.4167 when re-indexed (+15 days); intrinsic one-hot residues stay 1.0000 — laws live in invariants, not conventions | Verified |
| **T60 Fold as Optimizer** | Hamiltonian retrace conserves (drift $3.9\times10^{-3}$, area ratio 0.99, recurrence 0.000 — never locks); damped mirror contracts to area 0 and locks at $x = +1$ (dissipation = locking, §7 friction) | Verified |
| **T61 Rotation Test** | Orthogonal rotations preserve neighbor structure (overlap 1.0000, sim corr 1.0000) while coordinates change (0.745); $\|x\|$ relabeling collapses to 0.426 vs chance 0.065 | Verified |
| **T62 Prime Engine** | $\pi(943,901,200,001) = 35,575,526,191$ from scratch (Lucy-Hedgehog + segmented sieve, no sympy) — matches sympy exactly; max gap 176 at $9.4\times10^{11}$; retrace chain 9.4e11 → 1,914,467 → 730,421 → 26,102 → 10,262 | Verified |
| **T63 The Fold Derived** | The mirror fold is the unique **viscosity solution** of $\|r'\| = a$ with $C_0$ pinned at both loop ends (upwind convergence $3.3\times10^{-13}$); the crease is the **cut locus / shock** of equal eikonal time — the fold is no longer imposed | Verified |
| **T64 The Retrace Derived** | The reflecting boundary at $\Theta$ is the **cut locus**, selected by viscosity: the equation admits infinitely many weak solutions (zig-zag family), the flat-tangent supersolution test eliminates every down-up corner, upwind erosion converges to the tent from any seed; reflection conserves $\|r'\|$ | Verified |

### 10.5 Open Questions

1. **Can the Wheeler-DeWitt equation be simulated on the Poincaré disk?** The Hamiltonian constraint $\hat{H}|\Psi\rangle = 0$ selects physical states from the full Hilbert space. Can an analogous constraint be defined on the Poincaré disk that selects "physical" knowledge configurations?

2. **Is the fold-and-cut theorem the discrete analogue of unitary evolution?** T63 shows the fold itself is a shock of the eikonal equation; the discrete question — whether fold-and-cut realizes unitary gates — remains open.

3. **Does the Kawasaki analogue constrain CTC consistency?** If Robertson's generalization imposes angle-sum constraints on ReLU decision region vertices, these constraints may limit which causal loops are self-consistent — a mathematical version of the Novikov principle.

4. ~~**What is the retrace boundary condition from first principles?**~~
   **Resolved** (T64): the reflecting boundary at $\Theta$ is not assumed.
   The equation $\|r'\| = a$ with both pins admits *infinitely many* weak
   solutions (the zig-zag family); the flat-tangent supersolution test
   eliminates every down-to-up corner, leaving the tent as the unique
   viscosity solution.  The "reflecting boundary" is the **cut locus** —
   the shock where outgoing and returning characteristics collide at equal
   eikonal time.  Retrace is a consequence, not an assumption.

---

## References

- Albert, D. (2000). *Time and Chance*. Harvard University Press.
- Bekenstein, J. D. (1973). Black holes and entropy. *Physical Review D*, 7(8), 2333.
- Demaine, E. D., Demaine, M. L., & Lubiw, A. (1998). Folding and one straight cut suffice. *Proceedings of the Tenth Annual ACM-SIAM Symposium on Discrete Algorithms*.
- Hawking, S. W. (1975). Particle creation by black holes. *Communications in Mathematical Physics*, 43(3), 199-220.
- Novikov, I. D. (1983). Evolution of the Universe. Cambridge University Press.
- Penrose, C. (2005). *The Road to Reality*. Jonathan Cape. See also: Conformal Cyclic Cosmology.
- Poincaré, H. (1890). Sur le problème des trois corps et les équations de la dynamique. *Acta Mathematica*, 13, 1-270.
- Puno, M. G. S. (2026). *The Book of Puno: A Treatise on Folding, Unfolding, and What Lives at the Crease* (2nd ed.).
- Robertson, S. J. (1977). Isometric folding of Riemannian manifolds. *Journal of the London Mathematical Society*, s2-15(1), 163-168.
- Susskind, L. (1995). The world as a hologram. *Journal of Mathematical Physics*, 36(11), 6377-6396.
- t'Hooft, G. (1993). Dimensional reduction in quantum gravity. *arXiv:gr-qc/9310026*.
- Wheeler, J. A., & DeWitt, B. S. (1967). Quantum theory of gravity. I. The canonical theory. *Physical Review*, 160(5), 1113.

---

*Everything folds. Everything unfolds. The crease is where the action is. The clock is infinite. The book is open.*
