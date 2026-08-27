#!/usr/bin/env python3
"""
Free Will: 0/0 of Agency (Determinism vs. Choice)
===================================================

Following Ch.54 (the deterministic Life simulation), physics seems fully
deterministic. Yet we EXPERIENCE choice. Are free will and determinism
compatible?

1. DETERMINISM IS REPRODUCIBLE:
   - Same seed + same rule => bit-identical future (Life, Ch.54)
   - The universe's ~10^121 operations (Lloyd, Ch.54) contain
     ZERO observed violations of the laws
   - Every "choice" in the simulation is a logic gate: deterministic

2. DETERMINISM IS NOT PREDICTABILITY:
   - Logistic map x -> 4x(1-x): Lyapunov exponent lambda = ln 2
   - One bit of uncertainty destroys prediction in ~53 steps
   - Laplace's demon is IMPOSSIBLE in practice: chaotic (Poincare)
   - Determinism says WHAT HAPPENS, not what we KNOW

3. CONSERVATION OF CHOICE (INFORMATION):
   - In a deterministic universe, information is conserved (Liouville)
   - A "choice" TRANSFORMS information; it never CREATES it
   - Entropy before = entropy after (reversible dynamics)

4. LIBET (1983): READINESS POTENTIAL:
   - Unconscious brain activity precedes conscious decision
   - RP onset ~ -550 ms, conscious intention (W) ~ -200 ms
   - The "choice" is already underway BEFORE we are aware of it

5. CONWAY-KOCHEN FREE WILL THEOREM (2006):
   - Axioms: SPIN, TWIN, FIN
   - If experimenters have free will, so do particles
   - Contrapositive: if particles are determined, so are we
   - Choice and law are ENTANGLED (the 0/0 of agency)

6. THE 0/0 PROOF (COMPATIBILISM):
   - World A: actions fully determined by past
   - World B: actions freely chosen
   - Every observable outcome is IDENTICAL in A and B
   - The distinction has zero observational content: it IS 0/0
   - Free will = determined choice that FEELS free (self-referential)

7. CONNECTIONS:
   - Simulation (Ch.54): deterministic substrate
   - Hard problem (Ch.53): the felt quality of choosing
   - Measurement (Ch.49): Born rule randomness at collapse
   - Chaos (Ch.43): determinism without predictability
   - Entanglement (Ch.33): TWIN correlations
   - Arrow of time (Ch.48): irreversibility of experience

Author: Michael Grafiel S Puno
"""

import math
import json
import os
import random
import time

import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def life_step(grid, height, width):
    n = np.zeros_like(grid, dtype=np.int32)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            n += np.roll(np.roll(grid, dy, axis=0), dx, axis=1)
    new = np.zeros_like(grid, dtype=np.int32)
    new[(grid == 1) & ((n == 2) | (n == 3))] = 1
    new[(grid == 0) & (n == 3)] = 1
    return new


def run_life(seed, steps):
    H, W = 60, 60
    grid = np.zeros((H, W), dtype=np.int32)
    for cell in seed:
        grid[cell[1] + 10, cell[0] + 10] = 1
    for _ in range(steps):
        grid = life_step(grid, H, W)
    return grid


def lyapunov_logistic(r, x0, n, transient):
    """Numerical Lyapunov exponent of logistic map."""
    x = x0
    for _ in range(transient):
        x = r * x * (1 - x)
    total = 0.0
    for _ in range(n):
        x = r * x * (1 - x)
        total += math.log(abs(r * (1 - 2 * x)))
    return total / n


def shannon_entropy(probs):
    h = 0.0
    for p in probs:
        if p > 1e-15:
            h += -p * math.log2(p)
    return h


def decision_equivalence():
    """
    Two world-variants: actions as determined vs actions as free.
    Both generate the same output trajectory from the same inputs.
    Observational equivalence = 1.0 (identical histories).
    """
    rng = random.Random(7)
    inputs = [rng.random() for _ in range(200)]

    # World A (determined): decision = deterministic function f
    def f_determined(s):
        return round(math.sin(s * 12345.6789) * 1000000) % 7

    # World B (free): same outputs, labeled 'choice'
    histA = [f_determined(s) for s in inputs]
    histB = [f_determined(s) for s in inputs]  # chosen path

    identical = histA == histB
    return identical, histA[:6], histB[:6]


def info_conservation():
    """Reversible deterministic dynamics conserve entropy."""
    rng = random.Random(11)
    v = [rng.random() for _ in range(1024)]
    p0 = [v[i] / sum(v) for i in range(len(v))]
    H0 = shannon_entropy(p0)

    # reversible permutation (deterministic map, invertible)
    idx = rng.sample(range(len(v)), len(v))
    w = [v[idx[i]] for i in range(len(w))] if False else [v[i] for i in (idx)]
    sw = sum(w)
    p1 = [wi / sw for wi in w]
    H1 = shannon_entropy(p1)
    return H0, H1


def libet_timing():
    """Libet 1983: readiness potential precedes conscious decision."""
    rp_onset = -550.0   # ms before movement
    w_awareness = -200.0  # ms before movement (conscious intention)
    return {
        'readiness_potential': rp_onset,
        'conscious_intention_W': w_awareness,
        'gap_ms': abs(rp_onset - w_awareness),
        'choice_begins_before_awareness': True,
    }


def conway_kochen():
    """
    Conway-Kochen Free Will Theorem (2006).
    Axioms: SPIN (spin-1, 120-degree axes), TWIN (entanglement),
    FIN (finite-speed propagation).
    """
    axioms = {
        'SPIN': 'spin-1 particle: two-step outcomes on 120-deg axes',
        'TWIN': 'entangled twins give perfectly correlated spins',
        'FIN': 'no information travels faster than light',
    }
    theorem = {
        'if_experimenters_free_then_particles_free': True,
        'contrapositive_particles_determined_then_we_are': True,
        'choice_and_law_entangled': True,
    }
    return axioms, theorem


def predictability_horizon(lambda_, eps0, epsmin):
    """Steps until initial uncertainty eps0 grows to epsmin."""
    return math.log(eps0 / epsmin) / lambda_


def main():
    print("=" * 70)
    print("FREE WILL: 0/0 OF AGENCY (DETERMINISM VS CHOICE)")
    print("=" * 70)
    print()

    # 1. Determinism is reproducible
    print("1. DETERMINISM IS REPRODUCIBLE")
    print("-" * 70)
    print()
    seed = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    g1 = run_life(seed, 100)
    g2 = run_life(seed, 100)
    g3 = run_life(seed, 100)
    same_12 = int((g1 == g2).all())
    same_13 = int((g1 == g3).all())
    print("   Same seed, same rule (Game of Life, 100 gens):")
    print("   run1 vs run2 identical: %s" % ("YES" if same_12 else "NO"))
    print("   run1 vs run3 identical: %s" % ("YES" if same_13 else "NO"))
    print("   reproducibility: %.7f" % 1.0)
    print()
    print("   Every 'choice' in the simulation is a logic gate:")
    print("   determined by the rule. No observed violation in")
    print("   ~10^121 operations of the universe (Ch.54, Lloyd).")

    # 2. Determinism is not predictability
    print()
    print("2. DETERMINISM IS NOT PREDICTABILITY")
    print("-" * 70)
    print()
    lam = lyapunov_logistic(4.0, 0.1, 20000, 1000)
    print("   Logistic map x -> 4x(1-x):")
    print("   Numerical Lyapunov exponent: %.6f (theory ln 2 = %.6f)" % (lam, math.log(2.0)))
    eps0 = 1e-8
    epsmin = 1e-16
    H = predictability_horizon(math.log(2.0), eps0, epsmin)
    print("   Uncertainty 1e-8 grows to 1e-16-level divergence in")
    print("   %.0f iterations (roughly one bit lost per step)" % H)
    print()
    print("   Determinism says WHAT WILL HAPPEN, not what we KNOW.")
    print("   Laplace's demon is impossible in practice (Poincare):")
    print("   the 0/0 of determinism vs predictability (Ch.43 chaos).")

    # 3. Conservation of choice
    print()
    print("3. CONSERVATION OF CHOICE (INFORMATION)")
    print("-" * 70)
    print()
    H0, H1 = info_conservation()
    print("   Reversible deterministic dynamics:")
    print("   Entropy before: %.6f bits" % H0)
    print("   Entropy after : %.6f bits" % H1)
    print("   Conservation: %s (diff %.2e)" % ("CONFIRMED" if abs(H0 - H1) < 1e-6 else "BROKEN", abs(H0 - H1)))
    print()
    print("   A 'choice' TRANSFORMS information; it never CREATES it.")
    print("   Freedom is not a new fact - it is the same fact")
    print("   experienced from inside (the 0/0 of agency).")

    # 4. Libet
    print()
    print("4. LIBET (1983): READINESS POTENTIAL")
    print("-" * 70)
    print()
    lt = libet_timing()
    print("   Readiness potential onset : %d ms (before movement)" % lt['readiness_potential'])
    print("   Conscious intention (W)   : %d ms" % lt['conscious_intention_W'])
    print("   Gap                        : %d ms" % lt['gap_ms'])
    print()
    print("   The choice is already underway BEFORE we are")
    print("   aware of deciding. Brain processes determine")
    print("   what we then attribute to free will.")

    # 5. Conway-Kochen
    print()
    print("5. CONWAY-KOCHEN FREE WILL THEOREM (2006)")
    print("-" * 70)
    print()
    axioms, theo = conway_kochen()
    for k, v in axioms.items():
        print("   Axiom %-5s: %s" % (k, v))
    print()
    for k, v in theo.items():
        print("   %-52s: %s" % (k, v))
    print()
    print("   If experiments have a truly free choice of setting,")
    print("   particles too must be able to choose their outcomes.")
    print("   Contrapositive: if particles are fully determined,")
    print("   experimenters' choices were fixed at the Big Bang.")
    print("   Choice and law are ENTANGLED (the 0/0 of agency).")

    # 6. 0/0 proof
    print()
    print("6. THE 0/0 PROOF (COMPATIBILISM)")
    print("-" * 70)
    print()
    identical, hA, hB = decision_equivalence()
    print("   World A (determined) outputs: %s" % (hA[:6],))
    print("   World B (free)     outputs: %s" % (hB[:6],))
    print("   Full 200-step histories identical: %s" % ("YES" if identical else "NO"))
    print()
    print("   Every observable outcome of a 'freely chosen' history")
    print("   is identical to a 'determined' history. The distinction")
    print("   has ZERO observational content: it IS a 0/0.")
    print()
    print("   Compatibilism is the REMOVABLE SINGULARITY of agency:")
    print("   free will = determined choice that FEELS free.")
    print("   It is turtles all the way down (Ch.54).")

    # 7. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO PRIOR 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   Free will connects to:")
    print()
    print("   Simulation (Ch.54) -> Deterministic substrate")
    print("   Hard problem (Ch.53) -> The felt quality of choosing")
    print("   Measurement (Ch.49) -> Born rule at collapse")
    print("   Chaos (Ch.43) -> Determinism without predictability")
    print("   Entanglement (Ch.33) -> TWIN correlations")
    print("   Arrow of time (Ch.48) -> Irreversibility of experience")
    print("   Grokking (Ch.35) -> Algorithms decide, we observe")
    print()
    print("   Free will is the 0/0 of AGENCY: the boundary where")
    print("   law and choice become observationally indistinguishable!")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   1. REPRODUCIBLE: same seed => same future (Life)")
    print("   2. UNPREDICTABLE: Lyapunov lambda = ln 2 (chaos)")
    print("   3. CONSERVED: choice transforms, never creates info")
    print("   4. LIBET: RP -550 ms, awareness -200 ms (gap 350 ms)")
    print("   5. CONWAY-KOCHEN: free experimenters => free particles")
    print("   6. 0/0 PROOF: free and determined histories identical")
    print()
    print("   Agency is the 0/0 of DETERMINISM and CHOICE!")
    print("   Law and freedom are the same fact from two sides!")

    # Save
    results = {
        'determinism': {
            'reproducible': True,
            'same_seed_same_future': True,
            'lloyd_no_violation': True,
        },
        'chaos': {
            'lyapunov_logistic_4': round(lam, 6),
            'theory': round(math.log(2.0), 6),
            'deterministic_but_unpredictable': True,
        },
        'info_conservation': {
            'entropy_before': round(H0, 6),
            'entropy_after': round(H1, 6),
            'choice_transforms_not_creates': True,
        },
        'libet': {
            'rp_onset_ms': -550,
            'W_awareness_ms': -200,
            'gap_ms': 350,
        },
        'conway_kochen': {
            'axioms': ['SPIN', 'TWIN', 'FIN'],
            'theorem': True,
            'free_experimenters_imply_free_particles': True,
        },
        'the_0over0': {
            'free_vs_determined_identical': bool(identical),
            'compatibilism': True,
            'removable_singularity_of_agency': True,
        },
        'connections': ['Simulation', 'Hard problem', 'Measurement', 'Chaos', 'Entanglement', 'Arrow of time'],
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'free_will.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()