# Puno Calculus

The Law of Repulsive Emanation (L.O.R.E.): *C0 is measured, not chosen.*

A hyperbolic novelty engine, Hamiltonian flow on the Poincare disk, and a formal proof that the constant of integration is uniquely determined by the initial condition.

## The Core Idea

The antiderivative ∫f(x)dx = F(x) + C has an arbitrary constant only when the initial condition is unknown. When the initial condition IS known — when you know where the system starts — the constant collapses to a specific value C0, uniquely determined by the geometry:

    C0 = V(q0) = H(q0, 0)

This is **L.O.R.E.** — the Law of Repulsive Emanation. The constant emanates from the origin. It is measured, not chosen.

## What the Engine Does

The Poincare disk engine:

1. Embeds text probes into a 2D hyperbolic space
2. Evolves them via Hamiltonian mechanics with the correct Riemannian metric
3. Detects novelty/anomaly by radial distance from the origin
4. Simulates cosmological cycles (Big Bang -> expansion -> heat death -> recurrence)
5. Closes closed timelike curves via self-consistent iteration
6. Measures crease density in neural network decision boundaries

## Quick Start

```bash
cd Universals
python engine.py
```

This runs all 7 phases of the engine and exports JSON data to the Universals directory.

For individual experiments:
```bash
python exp1_crease_subgradient.py
python exp2_crease_density.py
python exp3_early_stop.py
python demo_ood.py
python exp_pruning.py
python fold_visual.py
```

## Validation

```bash
python math_validation.py
```

Runs 67 cross-validation tests covering geodesic distance, conformal factor, Hamilton's equations, Kawasaki constraint, Bekenstein bound, Wheeler-DeWitt constraint, soft crease metrics, exp/log maps, Mobius addition, and crease density.

## The Paper

`Universals/PAPER.md` contains the complete proof of L.O.R.E. and the theoretical framework.

## Dashboard

Open `Universals/index.html` in a browser for a 17-panel live dashboard.

## Architecture

```
Puno_Calculus/
├── Universals/
│   ├── engine.py              # Main engine (7 phases)
│   ├── hamiltonian_flow.py    # Hamiltonian mechanics
│   ├── crease_metrics.py      # Crease diagnostics
│   ├── puno_utils.py          # Shared utilities
│   ├── manifold/
│   │   └── poincare.py        # Poincare disk geometry
│   ├── exp*.py                # 7 Book of Puno experiments
│   ├── math_validation.py     # 67-test validation suite
│   ├── prove_c0.py            # L.O.R.E. proofs
│   ├── index.html             # Dashboard
│   ├── PAPER.md               # Research paper
│   └── *.json                 # Engine output data
├── extracted_text/            # Original source text
├── pyproject.toml
├── README.md
└── LICENSE
```

## The Law of Repulsive Emanation

**Theorem.** The constant of integration C0 is uniquely determined by the initial condition and system parameters.

**Proof.** At t=0: H(0) = K(0) + V(q0). Since p(0)=0, K(0)=0, so H(0)=V(q0). V(q0) = sum_i max(0, alpha - d(q0, xi))^2 where every input is fixed. Therefore V(q0) is a specific number. Call it C0. Verified across 32 parameter variations. Every case: C0 = H(q0, 0). Always determined. Never arbitrary.

## Key Finding: The λ⁴ Bug

The original velocity formula computed p/lam_sq where lam_sq = (1-||q||²)²/4 = 1/λ², giving velocity = p·λ². The correct Hamilton's equation requires dq/dt = (1/λ²)·p. The factor λ⁴ error causes energy blowup near the boundary. Corrected to p·lam_sq.

## Experiments

| Experiment | Result |
|------------|--------|
| Subgradient Selection | All strategies reach 99.7% accuracy |
| Crease vs Boundary | r(crease, complexity) = -0.77 |
| Early Stopping | 71-80% epoch savings via crease stabilization |
| OOD Detection | Crease AUROC 0.88 (center-noise) |
| Pruning | Crease beats magnitude at every ratio (+1.4% at 25%) |
| Fold Visualization | 90° crease as elementary fold |

## References

1. Newton, I. (1668). Fundamental Theorem of Calculus.
2. Puno, M. G. S. (2026). The Book of Puno (2nd ed.).

---

*Everything folds. The constant is determined.*
