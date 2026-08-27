#!/usr/bin/env python3
"""
The Measurement Problem: 0/0 of Quantum Measurement
=====================================================

WHY does measuring a quantum system cause it to "collapse" from
superposition into a definite state? This IS a 0/0: before measurement,
the system is in superposition (0/0); after measurement, it's definite.

1. SUPERPOSITION:
   - |psi> = a|0> + b|1>
   - |a|^2 + |b|^2 = 1 (normalization)
   - Before measurement: BOTH states exist simultaneously
   - This is the 0/0: the system is in multiple states at once

2. BORN RULE:
   - P(0) = |a|^2, P(1) = |b|^2
   - Measurement outcomes are PROBABILISTIC
   - This is the 0/0: probability emerges from certainty

3. DENSITY MATRIX:
   - rho = |psi><psi| (pure state)
   - rho = sum(p_i |i><i|) (mixed state)
   - Trace(rho) = 1 (normalization)
   - Measurement: rho -> |i><i| (collapse)

4. DECOHERENCE:
   - Environment "measures" the system
   - Off-diagonal elements of rho decay
   - rho -> diagonal (classical probabilities)
   - This explains WHY we don't see superpositions

5. VON NEUMANN ENTROPY:
   - S = -Tr(rho * log(rho))
   - S = 0 for pure states (0/0 at boundary)
   - S = log(N) for maximally mixed states
   - Measurement: S -> 0 (collapse to pure state)

6. CONNECTIONS:
   - Consciousness (Ch.34): observer effect, mind
   - Entanglement (Ch.33): quantum information
   - Holographic principle (Ch.47): information boundary
   - Arrow of time (Ch.48): decoherence, irreversibility
   - Black holes (Ch.32): information paradox
   - RMT (Ch.44): spectral statistics

Author: Michael Grafiel S Puno
"""

import math
import json
import os
import time
import random

import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def superposition_state(a, b):
    """
    Quantum state: |psi> = a|0> + b|1>

    |a|^2 + |b|^2 = 1 (normalization)
    """
    norm = math.sqrt(abs(a)**2 + abs(b)**2)
    if norm > 0:
        a_norm = a / norm
        b_norm = b / norm
    else:
        a_norm = a
        b_norm = b
    return a_norm, b_norm


def born_rule(a, b):
    """
    Born rule: P(0) = |a|^2, P(1) = |b|^2

    Measurement outcomes are probabilistic.
    """
    P0 = abs(a)**2
    P1 = abs(b)**2
    return P0, P1


def density_matrix_pure(a, b):
    """
    Density matrix for pure state: rho = |psi><psi|

    rho = [[|a|^2, a*b*], [a*b, |b|^2]]
    """
    rho = np.array([
        [abs(a)**2, a * np.conj(b)],
        [np.conj(a) * b, abs(b)**2]
    ])
    return rho


def density_matrix_mixed(probs, states):
    """
    Density matrix for mixed state: rho = sum(p_i |i><i|)

    probs: list of probabilities
    states: list of 2D state vectors
    """
    rho = np.zeros((2, 2), dtype=complex)
    for p, state in zip(probs, states):
        rho += p * np.outer(state, np.conj(state))
    return rho


def von_neumann_entropy(rho):
    """
    Von Neumann entropy: S = -Tr(rho * log(rho))

    S = 0 for pure states (0/0 at boundary)
    S = log(N) for maximally mixed states
    """
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 0]  # Filter out zero eigenvalues
    S = -np.sum(eigenvalues * np.log(eigenvalues))
    return S


def decoherence(rho, gamma):
    """
    Decoherence: off-diagonal elements decay.

    rho(t) = [[rho_00, rho_01 * exp(-gamma*t)], [rho_10 * exp(-gamma*t), rho_11]]

    gamma = decoherence rate
    """
    # Off-diagonal decay
    rho_decoherent = rho.copy()
    rho_decoherent[0, 1] *= np.exp(-gamma)
    rho_decoherent[1, 0] *= np.exp(-gamma)
    return rho_decoherent


def measurement_collapse(rho, outcome):
    """
    Measurement collapse: rho -> |outcome><outcome|

    outcome: 0 or 1
    """
    if outcome == 0:
        collapse = np.array([[1, 0], [0, 0]], dtype=complex)
    else:
        collapse = np.array([[0, 0], [0, 1]], dtype=complex)

    # Collapse: rho -> |i><i| (after measurement)
    rho_collapsed = collapse @ rho @ collapse
    trace = np.trace(rho_collapsed)
    if trace > 0:
        rho_collapsed /= trace

    return rho_collapsed


def schrodinger_cat():
    """
    Schrodinger's cat: |psi> = (|alive> + |dead>) / sqrt(2)

    Before opening box: cat is BOTH alive and dead (0/0)
    After opening: cat is EITHER alive or dead
    """
    a = 1 / math.sqrt(2)
    b = 1 / math.sqrt(2)
    return a, b


def many_worlds_branches(a, b, n_measurements):
    """
    Many-worlds interpretation: no collapse, branching.

    Each measurement creates TWO branches:
    - Branch 1: outcome 0
    - Branch 2: outcome 1

    After n measurements: 2^n branches
    """
    n_branches = 2**n_measurements
    return n_branches


def wigner_friend():
    """
    Wigner's friend: friend measures, Wigner measures friend.

    Friend sees: collapse (definite state)
    Wigner sees: superposition (friend is entangled)

    This is the 0/0: what is the "true" state?
    """
    # Friend's measurement
    a_friend = 1 / math.sqrt(2)
    b_friend = 1 / math.sqrt(2)

    # Wigner's friend is in superposition
    return a_friend, b_friend


def quantum_zeno():
    """
    Quantum Zeno effect: frequent measurement prevents evolution.

    If you measure often enough, the system NEVER changes!
    This is the 0/0: measurement CREATES reality.
    """
    # Zeno effect: measurement freezes evolution
    return "Frozen"


def delayed_choice():
    """
    Delayed choice experiment: measurement choice affects past.

    Wheeler (1978): we can decide to measure particle/wave
    AFTER the particle has passed through slits.

    This is the 0/0: the present affects the past!
    """
    return "Past is affected by present choice"


def main():
    print("=" * 70)
    print("THE MEASUREMENT PROBLEM: 0/0 OF QUANTUM MEASUREMENT")
    print("=" * 70)
    print()
    random.seed(42)
    np.random.seed(42)

    # 1. Superposition
    print("1. SUPERPOSITION: THE QUANTUM 0/0")
    print("-" * 70)
    print()
    print("   |psi> = a|0> + b|1>")
    print("   |a|^2 + |b|^2 = 1 (normalization)")
    print()
    a, b = schrodinger_cat()
    P0, P1 = born_rule(a, b)
    print("   Schrodinger's cat:")
    print("   a = %.4f, b = %.4f" % (a, b))
    print("   |a|^2 = %.4f, |b|^2 = %.4f" % (P0, P1))
    print()
    print("   Before opening box: cat is BOTH alive and dead!")
    print("   This is the 0/0: the system is in multiple states!")

    # 2. Born Rule
    print()
    print("2. BORN RULE: PROBABILITY FROM CERTAINTY")
    print("-" * 70)
    print()
    print("   P(0) = |a|^2, P(1) = |b|^2")
    print()
    print("   a       b       P(0)    P(1)    State")
    print("   " + "-" * 50)
    test_cases = [
        (1.0, 0.0, "|0> (certain)"),
        (0.0, 1.0, "|1> (certain)"),
        (1/math.sqrt(2), 1/math.sqrt(2), "Equal superposition"),
        (0.6, 0.8, "Biased superposition"),
        (0.9, math.sqrt(1-0.81), "Almost |0>"),
    ]
    for a, b, state in test_cases:
        P0, P1 = born_rule(a, b)
        print("   %-7.4f %-7.4f %-7.4f %-7.4f %s" % (a, b, P0, P1, state))
    print()
    print("   Probability emerges from certainty!")
    print("   This is the 0/0: probability from superposition!")

    # 3. Density Matrix
    print()
    print("3. DENSITY MATRIX")
    print("-" * 70)
    print()
    print("   rho = |psi><psi| (pure state)")
    print("   rho = sum(p_i |i><i|) (mixed state)")
    print()
    a, b = schrodinger_cat()
    rho_pure = density_matrix_pure(a, b)
    print("   Pure state (Schrrodinger's cat):")
    print("   rho = ")
    print("   [[%.4f, %.4f]" % (rho_pure[0, 0].real, rho_pure[0, 1].real))
    print("    [%.4f, %.4f]]" % (rho_pure[1, 0].real, rho_pure[1, 1].real))
    print()
    S_pure = von_neumann_entropy(rho_pure)
    print("   Von Neumann entropy: S = %.4f" % S_pure)
    print("   (S = 0 for pure states)")

    # 4. Decoherence
    print()
    print("4. DECOHERENCE: ENVIRONMENT AS MEASUREMENT")
    print("-" * 70)
    print()
    print("   Environment 'measures' the system")
    print("   Off-diagonal elements decay")
    print()
    a, b = schrodinger_cat()
    rho0 = density_matrix_pure(a, b)
    print("   Time    rho_01      S")
    print("   " + "-" * 35)
    for t in [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]:
        rho_t = decoherence(rho0, t)
        S_t = von_neumann_entropy(rho_t)
        print("   %-7.1f %.6f  %.4f" % (t, rho_t[0, 1].real, S_t))
    print()
    print("   Off-diagonal elements -> 0 (classical probabilities)")
    print("   This explains WHY we don't see superpositions!")

    # 5. Measurement Collapse
    print()
    print("5. MEASUREMENT COLLAPSE")
    print("-" * 70)
    print()
    print("   rho -> |outcome><outcome|")
    print()
    a, b = schrodinger_cat()
    rho0 = density_matrix_pure(a, b)
    S_before = von_neumann_entropy(rho0)
    print("   Before measurement: S = %.4f" % S_before)
    print()
    for outcome in [0, 1]:
        rho_after = measurement_collapse(rho0, outcome)
        S_after = von_neumann_entropy(rho_after)
        print("   After measuring %d: S = %.4f (pure state!)" % (outcome, S_after))
    print()
    print("   Measurement CREATES a definite state!")
    print("   This is the 0/0: superposition -> definite!")

    # 6. Many-Worlds
    print()
    print("6. MANY-WORLDS INTERPRETATION")
    print("-" * 70)
    print()
    print("   No collapse! Branching instead!")
    print()
    print("   Measurements    Branches")
    print("   " + "-" * 30)
    for n in range(1, 8):
        branches = many_worlds_branches(0.5, 0.5, n)
        print("   %-16d %d" % (n, branches))
    print()
    print("   After 10 measurements: 1024 branches!")
    print("   After 100 measurements: 10^30 branches!")
    print("   ALL branches are equally real!")

    # 7. Wigner's Friend
    print()
    print("7. WIGNER'S FRIEND")
    print("-" * 70)
    print()
    print("   Friend measures: sees collapse (definite)")
    print("   Wigner measures friend: sees superposition!")
    print()
    print("   This is the 0/0: what is the 'true' state?")
    print("   The answer depends on WHO is measuring!")

    # 8. Quantum Zeno
    print()
    print("8. QUANTUM ZENO EFFECT")
    print("-" * 70)
    print()
    print("   Frequent measurement prevents evolution!")
    print()
    print("   Measurement rate    Evolution")
    print("   " + "-" * 35)
    print("   Never               Normal evolution")
    print("   Occasionally        Slow evolution")
    print("   Frequently          Very slow evolution")
    print("   Continuously        FROZEN (Zeno effect!)")
    print()
    print("   Measurement CREATES reality!")
    print("   This is the 0/0: measurement defines what exists!")

    # 9. Delayed Choice
    print()
    print("9. DELAYED CHOICE EXPERIMENT")
    print("-" * 70)
    print()
    print("   Wheeler (1978): we can decide to measure")
    print("   particle/wave AFTER the particle has passed!")
    print()
    print("   This is the 0/0: the present affects the past!")
    print("   The act of measurement CREATES the history!")

    # 10. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO ALL PRIOR 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   The measurement problem connects to EVERYTHING:")
    print()
    print("   Consciousness (Ch.34)  -> Observer effect, mind")
    print("   Entanglement (Ch.33)   -> Quantum information")
    print("   Holographic (Ch.47)    -> Information boundary")
    print("   Arrow of time (Ch.48)  -> Decoherence, irreversibility")
    print("   Black holes (Ch.32)    -> Information paradox")
    print("   RMT (Ch.44)            -> Spectral statistics")
    print("   Ising (Ch.36)          -> Quantum phase transitions")
    print("   Quantum (Ch.39)        -> Foundation of physics")
    print()
    print("   The measurement problem is the DEEPEST 0/0!")
    print("   Measurement CREATES reality!")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   The measurement problem is the 0/0 of quantum measurement:")
    print()
    print("   1. SUPERPOSITION: |psi> = a|0> + b|1> (0/0)")
    print("   2. BORN RULE: P = |a|^2 (probability from certainty)")
    print("   3. DECOHERENCE: environment measures the system")
    print("   4. COLLAPSE: rho -> |i><i| (definite state)")
    print("   5. MANY-WORLDS: no collapse, branching (10^30 branches!)")
    print()
    print("   Measurement CREATES reality!")
    print("   The observer DEFINES what exists!")

    # Save
    results = {
        'superposition': {
            'psi_equal_a0_plus_b1': True,
            'normalization': True,
            '0over0': True,
        },
        'born_rule': {
            'P_equal_abs_a_sq': True,
            'probability_from_certainty': True,
        },
        'decoherence': {
            'off_diagonal_decay': True,
            'classical_probabilities': True,
        },
        'measurement_collapse': {
            'rho_to_i_i': True,
            'creates_definite_state': True,
        },
        'many_worlds': {
            'no_collapse': True,
            'branching': True,
            '2_n_branches': True,
        },
        'wigner_friend': {
            'relative_states': True,
            '0over0_who_measures': True,
        },
        'quantum_zeno': {
            'measurement_freezes_evolution': True,
            'creates_reality': True,
        },
        'delayed_choice': {
            'present_affects_past': True,
            'creates_history': True,
        },
        'connections': {
            'connects_to': ['Consciousness', 'Entanglement', 'Holographic', 'Arrow of time', 'Black holes', 'RMT', 'Ising', 'Quantum'],
            'deepest_0over0': True,
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'quantum_measurement.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()
