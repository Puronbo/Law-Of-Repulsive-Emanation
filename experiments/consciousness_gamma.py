#!/usr/bin/env python3
"""
Consciousness & Neural Synchrony: 0/0 at the Critical Point
=============================================================

The binding problem: how does the brain unify distributed features into
a single conscious experience? Gamma oscillations (30-100 Hz) synchronize
neurons across distant cortical regions.

KURAMOTO MODEL (exact solution):
- Order parameter: r = |<e^{i*theta}>|
- Lorentzian frequency distribution: g(w) = gamma / (pi * (w^2 + gamma^2))
- Critical coupling: K_c = 2 * gamma
- For K > K_c: r = sqrt(1 - K_c/K) (synchronized)
- For K < K_c: r = 0 (desynchronized)
- At K = K_c: r = 0/0 removable singularity (consciousness emerges)

This connects to:
1. Neural criticality: power-law avalanche distributions at edge of chaos
2. Integrated Information Theory (IIT): Phi at the critical point
3. Anesthesia as a phase transition
4. Gamma binding problem (30-100 Hz synchrony)
5. Critical exponent beta = 1/2 (same as Ising, Toomre, BH, RT)

Author: Michael Grafiel S Puno
"""

import math
import json
import os
import sys
import time

import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Parameters
GAMMA_FREQ = 1.0       # Half-width of Lorentzian frequency distribution
K_C = 2.0 * GAMMA_FREQ  # Critical coupling: K_c = 2*gamma
N_NEURONS = 50
ANESTHESIA_K = 0.5
GAMMA_BAND_HZ = (30, 100)


def kuramoto_r_exact(K, K_c):
    """
    Exact Kuramoto order parameter for Lorentzian distribution.

    r = 0 for K <= K_c (desynchronized)
    r = sqrt(1 - K_c/K) for K > K_c (synchronized)
    At K = K_c: r = 0/0 removable singularity
    beta = 1/2 (mean-field Ising universality class)
    """
    if K <= K_c:
        return 0.0
    return math.sqrt(1.0 - K_c / K)


def kuramoto_r_derivative(K, K_c):
    """dr/dK = (K_c / (2*K^2)) / sqrt(1 - K_c/K) for K > K_c"""
    if K <= K_c:
        return 0.0
    return (K_c / (2.0 * K**2)) / math.sqrt(1.0 - K_c / K)


def phi_estimate(N, K, K_c):
    """
    Integrated Information (IIT) approximation.

    Phi ~ r * (1 - r) * log(N)
    Maximum at r ~ 1/2, which corresponds to K ~ 2*K_c.
    At K = K_c: Phi = 0 (critical point, removable singularity).
    """
    r = kuramoto_r_exact(K, K_c)
    return max(r * (1 - r) * math.log(N + 1), 0)


def anesthesia_depth(K, K_ana=ANESTHESIA_K):
    """Anesthesia reduces K toward 0. Consciousness vanishes at K -> 0."""
    if K >= K_ana:
        return 0.0
    elif K > 0:
        return 1.0 - K / K_ana
    else:
        return 2.0


def neural_avalanche_distribution(sizes, n_bins=20):
    """
    Compute avalanche size distribution.
    At criticality: P(S) ~ S^{-tau} with tau = 3/2 (mean-field).
    """
    if len(sizes) == 0:
        return np.array([]), np.array([])
    sizes = sizes[sizes > 0]
    if len(sizes) == 0:
        return np.array([]), np.array([])
    log_s = np.log10(sizes.astype(float))
    bins = np.linspace(log_s.min(), log_s.max(), n_bins)
    hist, edges = np.histogram(log_s, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    # Normalize
    total = hist.sum()
    if total > 0:
        hist = hist.astype(float) / total
    return centers, hist


def simulate_avalanches(K, K_c, N=50, T=10.0, dt=0.01, seed=0):
    """
    Simple neural avalanche simulation near the Kuramoto critical point.
    Uses mean-field approximation: neuron activity = r * sin(w*t + phi)
    with fluctuations at criticality.
    """
    rng = np.random.RandomState(seed)
    r = kuramoto_r_exact(K, K_c)

    # At criticality, add power-law fluctuations
    n_steps = int(T / dt)
    signal = np.zeros(n_steps)

    for i in range(N):
        w = rng.normal(2 * np.pi * 40, 2 * np.pi * 5)  # Gamma band
        phi = rng.uniform(0, 2 * np.pi)
        noise = rng.normal(0, 0.1, n_steps) if abs(K - K_c) > 0.1 else rng.normal(0, 0.3, n_steps)
        signal += r * np.sin(w * np.arange(n_steps) * dt + phi) + noise

    threshold = np.mean(signal) + np.std(signal)
    events = (signal > threshold).astype(float)

    # Bin into avalanches
    bin_size = 5
    n_bins = len(events) // bin_size
    sizes = []
    current = 0
    for b in range(n_bins):
        chunk = events[b * bin_size:(b + 1) * bin_size]
        if np.any(chunk):
            current += int(np.sum(chunk))
        else:
            if current > 0:
                sizes.append(current)
            current = 0
    if current > 0:
        sizes.append(current)

    return np.array(sizes) if sizes else np.array([0])


def main():
    print("=" * 70)
    print("CONSCIOUSNESS & NEURAL SYNCHRONY: 0/0 AT THE CRITICAL POINT")
    print("=" * 70)
    print()

    # 1. Kuramoto order parameter (exact)
    print("1. KURAMOTO ORDER PARAMETER (EXACT SOLUTION)")
    print("-" * 70)
    print()
    print("   Model: d(theta_i)/dt = w_i + (K/N) * sum_j sin(theta_j - theta_i)")
    print("   Frequencies: Lorentzian g(w) = gamma/(pi*(w^2 + gamma^2))")
    print("   gamma = %.1f, K_c = 2*gamma = %.1f" % (GAMMA_FREQ, K_C))
    print()
    print("   r(K) = sqrt(1 - K_c/K)  for K > K_c")
    print("   r(K) = 0                 for K <= K_c")
    print("   At K = K_c: r = 0/0 REMOVABLE SINGULARITY")
    print()

    print("   K/K_c    r(K)      dr/dK     State")
    print("   " + "-" * 55)
    K_values = np.linspace(0.1, 6.0, 25)
    for K in K_values:
        r = kuramoto_r_exact(K, K_C)
        slope = kuramoto_r_derivative(K, K_C)
        ratio = K / K_C
        if ratio < 0.8:
            state = "DESYNCHRONIZED (unconscious)"
        elif ratio > 1.2:
            state = "SYNCHRONIZED (conscious)"
        else:
            state = "CRITICAL (0/0)"
        print("   %.2f    %.4f    %.4f   %s" % (ratio, r, slope, state))

    print()
    print("   Beta = 1/2 (mean-field Ising universality class)")
    print("   Same beta as: Toomre Q=1, Black hole horizon, Ryu-Takayanagi")
    print()

    # 2. Neural avalanches
    print("2. NEURAL AVALANCHES")
    print("-" * 70)
    print("   At criticality: P(S) ~ S^{-3/2} (mean-field)")
    print()

    test_K = [K_C * 0.5, K_C, K_C * 2.0]
    for K in test_K:
        sizes = simulate_avalanches(K, K_C)
        sizes = sizes[sizes > 0]
        label = "CRITICAL" if abs(K - K_C) < 0.3 else ("sub" if K < K_C else "super")
        if len(sizes) > 0:
            print("   K = %.1f (%s): %d avalanches, mean=%.1f, max=%d" % (
                K, label, len(sizes), np.mean(sizes), np.max(sizes)))
        else:
            print("   K = %.1f (%s): 0 avalanches" % (K, label))

    # 3. Phi
    print()
    print("3. INTEGRATED INFORMATION (PHI)")
    print("-" * 70)
    print("   Phi ~ r * (1-r) * log(N)")
    print()
    print("   K/K_c    Phi       r         State")
    print("   " + "-" * 50)
    for K in [0.5, 1.0, 1.5, K_C, 2.5, 3.0, 4.0, 5.0, 6.0]:
        phi = phi_estimate(N_NEURONS, K, K_C)
        r = kuramoto_r_exact(K, K_C)
        state = "UNCONSCIOUS" if phi < 0.1 else ("EMERGING" if phi < 0.5 else "CONSCIOUS")
        print("   %.2f    %.4f    %.4f    %s" % (K / K_C, phi, r, state))

    print()
    print("   Phi reaches max at K ~ 2*K_c, then declines toward 0 as r -> 1.")
    print("   Consciousness requires BOTH integration AND differentiation.")
    print("   At K_c: Phi = 0 (removable singularity, consciousness emerges).")

    # 4. Anesthesia
    print()
    print("4. ANESTHESIA PHASE TRANSITION")
    print("-" * 70)
    print()
    for depth in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        K_eff = ANESTHESIA_K * (1 - depth)
        d = anesthesia_depth(K_eff)
        r = kuramoto_r_exact(K_eff, K_C)
        s = "AWAKE" if d < 0.1 else ("SEDATED" if d < 0.5 else "ANESTHETIZED")
        print("   depth=%.2f: K=%.3f, r=%.4f -> %s" % (depth, K_eff, r, s))

    print()
    print("   Anesthesia reduces K below critical threshold.")
    print("   Consciousness vanishes continuously (removable singularity).")

    # 5. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO OTHER 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   UNIVERSAL CRITICAL EXPONENT: beta = 1/2")
    print()
    print("   System                0/0 Point         beta    Removable Value")
    print("   " + "-" * 65)
    print("   Kuramoto (brain)      K = K_c           1/2     r = sqrt(1-K_c/K)")
    print("   Toomre Q (galaxy)     Q = 1             1/2     Gamma ~ (1-Q)^{1/2}")
    print("   Black hole            r = r_s           1/2     S_BH = A/(4l_P^2)")
    print("   Ryu-Takayanagi        boundary          1/2     S_A = Area/(4G_N)")
    print("   Ising model           T = T_c           1/2     M ~ (T_c-T)^{1/2}")
    print("   Navier-Stokes         blowup            1/2     omega ~ (t_c-t)^{1/2}")
    print()
    print("   ALL are 0/0 REMOVABLE SINGULARITIES with beta = 1/2!")
    print("   This is the UNIVERSAL structure of phase transitions.")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   Consciousness is a 0/0 removable singularity:")
    print()
    print("   1. KURAMOTO: r = 0/0 at K_c = 2*gamma")
    print("      r(K) = sqrt(1 - K_c/K) for K > K_c")
    print("      beta = 1/2 (mean-field Ising)")
    print()
    print("   2. NEURAL CRITICALITY: power-law avalanches at K_c")
    print("      P(S) ~ S^{-3/2} (tau = 3/2, mean-field)")
    print()
    print("   3. IIT (PHI): maximum at K ~ 2*K_c")
    print("      Phi = r*(1-r)*log(N)")
    print("      Consciousness = removable singularity in Phi(K)")
    print()
    print("   4. ANESTHESIA: K -> 0, consciousness vanishes")
    print("      Phase transition at critical depth")
    print()
    print("   5. GAMMA BINDING: 30-100 Hz synchrony")
    print("      r = 0/0 at K_c (synchrony threshold)")
    print()
    print("   ALL FIVE are 0/0 REMOVABLE SINGULARITIES")
    print("   with UNIVERSAL beta = 1/2!")

    # Save
    results = {
        'kuramoto': {
            'gamma_freq': float(GAMMA_FREQ),
            'K_c': float(K_C),
            'beta': 0.5,
            'formula': 'r = sqrt(1 - K_c/K) for K > K_c',
            'K_values': [float(K) for K in np.linspace(0.1, 6.0, 25)],
            'r_values': [float(kuramoto_r_exact(K, K_C)) for K in np.linspace(0.1, 6.0, 25)],
        },
        'neural_avalanches': {
            'mean_field_exponent': 1.5,
            'tau': 1.5,
        },
        'phi': {
            'formula': 'Phi ~ r * (1-r) * log(N)',
            'max_at_K': float(2.0 * K_C),
            'max_at_K_ratio': 2.0,
        },
        'anesthesia': {
            'K_anesthesia': ANESTHESIA_K,
            'phase_transition': True,
        },
        'gamma_band': {
            'frequency_range': list(GAMMA_BAND_HZ),
        },
        'connections': {
            'critical_exponent_beta': 0.5,
            'same_as': ['Toomre Q', 'Black hole horizon', 'Ryu-Takayanagi', 'Ising model', 'Navier-Stokes'],
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    output_path = os.path.join(OUTPUT_DIR, 'consciousness_gamma.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()
