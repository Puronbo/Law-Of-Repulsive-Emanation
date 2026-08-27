#!/usr/bin/env python3
"""
Random Matrix Theory: 0/0 of Universal Randomness
===================================================

Random matrices have UNIVERSAL eigenvalue statistics. The same
statistics appear in quantum chaos, zeta zeros, and finance.

1. WIGNER MATRICES:
   - Symmetric (GOE) or Hermitian (GUE) random matrices
   - Eigenvalues repel each other (level repulsion)
   - P(s=0) = 0 (0/0: eigenvalues never coincide!)

2. THREE ENSEMBLES:
   - GOE (beta=1): real symmetric, time-reversal invariant
   - GUE (beta=2): complex Hermitian, no time-reversal
   - GSE (beta=4): quaternion, spin-1/2 systems

3. NEIGHBOR-NEIGHBOR SPACING:
   - Poisson (uncorrelated): P(s) = exp(-s)  [no repulsion]
   - GOE: P(s) = (pi*s/2) * exp(-pi*s^2/4)
   - GUE: P(s) = (32/pi^2) * s^2 * exp(-4*s^2/pi)
   - Level repulsion: P(s->0) ~ s^beta

4. MONTEGOMERY-ODLYZKO LAW:
   - Pair correlation of zeta zeros = GUE!
   - This means the primes are "quantum chaotic"
   - Connects to Riemann hypothesis (Ch.25)

5. WIGNER SURMISE:
   - P(s) ~ s^beta * exp(-(beta+2)*s^2/4)
   - beta = 1 (GOE), 2 (GUE), 4 (GSE)
   - UNIVERSAL for all three ensembles

6. FINANCE:
   - Eigenvalue distribution of correlation matrices
   - Market noise: follows Marchenko-Pastur
   - Signal vs noise separation

7. CONNECTIONS:
   - Zeta zeros (Ch.25): Montgomery-Odlyzko = GUE
   - E8 (Ch.24): Lie algebras classify ensembles
   - Quantum chaos (Ch.43): quantum Feigenbaum
   - Finance (Ch.38): correlation matrices
   - Consciousness (Ch.34): neural connectivity

Author: Michael Grafiel S Puno
"""

import math
import json
import os
import time

import numpy as np
from numpy.linalg import eigvalsh

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_goe(n, n_matrices=1000):
    """Generate GOE (Gaussian Orthogonal Ensemble) eigenvalues."""
    all_eigenvalues = []
    for _ in range(n_matrices):
        A = np.random.randn(n, n)
        M = (A + A.T) / 2.0
        evals = eigvalsh(M)
        all_eigenvalues.extend(evals / np.sqrt(n))
    return np.array(all_eigenvalues)


def generate_gue(n, n_matrices=1000):
    """Generate GUE (Gaussian Unitary Ensemble) eigenvalues."""
    all_eigenvalues = []
    for _ in range(n_matrices):
        A = np.random.randn(n, n) + 1j * np.random.randn(n, n)
        M = (A + A.conj().T) / 2.0
        evals = eigvalsh(M)
        all_eigenvalues.extend(np.real(evals) / np.sqrt(n))
    return np.array(all_eigenvalues)


def nearest_neighbor_spacings(eigenvalues, n_matrices, matrix_size):
    """Compute nearest-neighbor spacing distribution."""
    spacings = []
    for i in range(n_matrices):
        start = i * matrix_size
        end = start + matrix_size
        evals = np.sort(eigenvalues[start:end])
        # Mean spacing
        mean_spacing = np.mean(np.diff(evals))
        if mean_spacing > 0:
            spacings.extend(np.diff(evals) / mean_spacing)
    return np.array(spacings)


def wigner_surmise_goE(s):
    """GOE Wigner surmise: P(s) = (pi*s/2) * exp(-pi*s^2/4)"""
    return (math.pi * s / 2.0) * math.exp(-math.pi * s**2 / 4.0)


def wigner_surmise_gue(s):
    """GUE Wigner surmise: P(s) = (32/pi^2) * s^2 * exp(-4*s^2/pi)"""
    return (32.0 / math.pi**2) * s**2 * math.exp(-4.0 * s**2 / math.pi)


def poisson(s):
    """Poisson distribution: P(s) = exp(-s) (no repulsion)"""
    return math.exp(-s)


def level_repulsion_test(spacings):
    """
    Test for level repulsion.

    P(s -> 0) ~ s^beta
    beta = 1: GOE (linear repulsion)
    beta = 2: GUE (quadratic repulsion)
    beta = 0: Poisson (no repulsion)
    """
    small_s = spacings[spacings < 0.5]
    if len(small_s) < 10:
        return None

    # Count how many spacings are near zero
    n_very_small = np.sum(small_s < 0.1)
    n_small = np.sum(small_s < 0.5)

    ratio = n_very_small / n_small if n_small > 0 else 0

    # For Poisson: ratio ~ 0.2 (uniform)
    # For GOE: ratio ~ 0.1 (linear repulsion)
    # For GUE: ratio ~ 0.05 (quadratic repulsion)
    if ratio > 0.15:
        return 0  # Poisson
    elif ratio > 0.08:
        return 1  # GOE
    else:
        return 2  # GUE


def marchenko_pastur(lambda_vals, q=1.0):
    """
    Marchenko-Pastur distribution.

    For random covariance matrices with ratio q = N/T.
    Eigenvalues follow MP distribution.
    Used in finance to separate signal from noise.
    """
    lambda_plus = (1 + np.sqrt(q))**2
    lambda_minus = (1 - np.sqrt(q))**2

    density = np.zeros_like(lambda_vals)
    mask = (lambda_vals >= lambda_minus) & (lambda_vals <= lambda_plus)
    density[mask] = np.sqrt((lambda_plus - lambda_vals[mask]) * (lambda_vals[mask] - lambda_minus)) / (2 * math.pi * q * lambda_vals[mask])
    return density


def generate_financial_correlation(n_assets=50, n_days=200):
    """
    Generate a financial correlation matrix.
    Eigenvalues follow Marchenko-Pastur (noise) + outliers (signal).
    """
    returns = np.random.randn(n_days, n_assets)
    corr = np.corrcoef(returns.T)
    evals = eigvalsh(corr)
    return evals


def zeta_zeros_mock(n_zeros=100):
    """
    Mock zeta zeros on the critical line.

    The actual zeros follow GUE statistics (Montgomery-Odlyzko).
    We generate synthetic zeros with GUE-like spacing.
    """
    # Generate GUE-like spacings
    spacings = np.random.exponential(1.0, n_zeros)
    # Adjust to have level repulsion
    for i in range(len(spacings)):
        if spacings[i] < 0.3:
            spacings[i] = 0.3 + np.random.exponential(0.5)
    zeros = np.cumsum(spacings)
    return zeros


def wigner_semicircle(n_points=1000):
    """
    Wigner semicircle law.

    Eigenvalue density: rho(E) = (2/(pi*R^2)) * sqrt(R^2 - E^2)
    for |E| < R, where R = 2*sqrt(N).
    """
    R = 2.0
    E = np.linspace(-R + 0.01, R - 0.01, n_points)
    rho = (2.0 / (math.pi * R**2)) * np.sqrt(R**2 - E**2)
    return E, rho


def main():
    print("=" * 70)
    print("RANDOM MATRIX THEORY: 0/0 OF UNIVERSAL RANDOMNESS")
    print("=" * 70)
    print()
    np.random.seed(42)

    # 1. Wigner Matrices
    print("1. WIGNER MATRICES")
    print("-" * 70)
    print()
    print("   GOE: real symmetric (beta=1)")
    print("   GUE: complex Hermitian (beta=2)")
    print("   GSE: quaternion (beta=4)")
    print()
    print("   Level repulsion: P(s=0) = 0 (0/0!)")
    print("   Eigenvalues NEVER coincide!")

    # 2. Eigenvalue Density
    print()
    print("2. WIGNER SEMICIRCLE LAW")
    print("-" * 70)
    print()
    E, rho = wigner_semicircle()
    print("   rho(E) = (2/(pi*R^2)) * sqrt(R^2 - E^2)")
    print()
    print("   E/rho(E)")
    print("   " + "-" * 25)
    for i in range(0, len(E), 100):
        print("   %-8.3f %.4f" % (E[i], rho[i]))

    # 3. GOE Spacings
    print()
    print("3. NEAREST-NEIGHBOR SPACINGS")
    print("-" * 70)
    print()
    n_mat = 500
    mat_size = 50
    print("   Generating %d GOE matrices (N=%d)..." % (n_mat, mat_size))
    goe_evals = generate_goe(mat_size, n_mat)
    goe_spacings = nearest_neighbor_spacings(goe_evals, n_mat, mat_size)
    print("   Total spacings: %d" % len(goe_spacings))
    print("   Mean spacing: %.4f (should be ~1)" % np.mean(goe_spacings))
    print("   Std spacing: %.4f" % np.std(goe_spacings))

    # Histogram
    hist, edges = np.histogram(goe_spacings, bins=20, range=(0, 4))
    mask = hist > 0
    centers = (edges[:-1] + edges[1:]) / 2
    print()
    print("   s_avg     Count    P(s)     Wigner")
    print("   " + "-" * 45)
    for c, n, w in zip(centers[mask], hist[mask], [wigner_surmise_goE(c) for c in centers[mask]]):
        p_emp = n / len(goe_spacings)
        print("   %-8.3f %-8d %.4f   %.4f" % (c, n, p_emp, w))

    # 4. Level Repulsion
    print()
    print("4. LEVEL REPULSION (0/0!)")
    print("-" * 70)
    print()
    beta = level_repulsion_test(goe_spacings)
    print("   P(s -> 0) ~ s^beta")
    print("   beta = 0: Poisson (no repulsion)")
    print("   beta = 1: GOE (linear repulsion)")
    print("   beta = 2: GUE (quadratic repulsion)")
    print()
    print("   Detected beta: %s" % ("GOE (beta=1)" if beta == 1 else ("GUE (beta=2)" if beta == 2 else "Poisson")))
    print()
    print("   Level repulsion: eigenvalues PUSH each other apart!")
    print("   P(s=0) = 0 exactly (0/0 removable singularity!)")

    # 5. GUE Comparison
    print()
    print("5. GUE: COMPLEX HERMITIAN")
    print("-" * 70)
    print()
    print("   Generating %d GUE matrices (N=%d)..." % (n_mat, mat_size))
    gue_evals = generate_gue(mat_size, n_mat)
    gue_spacings = nearest_neighbor_spacings(gue_evals, n_mat, mat_size)
    print("   Total spacings: %d" % len(gue_spacings))
    print("   Mean spacing: %.4f" % np.mean(gue_spacings))
    beta_gue = level_repulsion_test(gue_spacings)
    print("   Detected beta: %s" % ("GOE" if beta_gue == 1 else ("GUE" if beta_gue == 2 else "Poisson")))

    # 6. Wigner Surmise
    print()
    print("6. WIGNER SURMISE (UNIVERSAL!)")
    print("-" * 70)
    print()
    print("   P(s) ~ s^beta * exp(-(beta+2)*s^2/4)")
    print()
    print("   s     Poisson   GOE       GUE")
    print("   " + "-" * 45)
    for s_val in [0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]:
        p_pois = poisson(s_val)
        p_goe = wigner_surmise_goE(s_val)
        p_gue = wigner_surmise_gue(s_val)
        print("   %-5.1f %-9.4f %-9.4f %-9.4f" % (s_val, p_pois, p_goe, p_gue))
    print()
    print("   Poisson: P(0) = 1 (no repulsion)")
    print("   GOE: P(0) = 0 (linear repulsion)")
    print("   GUE: P(0) = 0 (quadratic repulsion)")
    print()
    print("   The 0/0 at s=0 is UNIVERSAL!")

    # 7. Zeta Zeros Connection
    print()
    print("7. MONTEGOMERY-ODLYZKO: ZETA ZEROS = GUE!")
    print("-" * 70)
    print()
    print("   The pair correlation of Riemann zeta zeros")
    print("   follows GUE statistics!")
    print()
    print("   This means: the primes are 'quantum chaotic'")
    print()
    zeros = zeta_zeros_mock(200)
    zero_spacings = np.diff(zeros)
    mean_sp = np.mean(zero_spacings)
    normalized = zero_spacings / mean_sp
    print("   Generated %d mock zeta zeros" % len(zeros))
    print("   Mean spacing: %.4f" % mean_sp)
    print("   Level repulsion detected: %s" % ("YES" if level_repulsion_test(normalized) in [1,2] else "NO"))
    print()
    print("   Montgomery (1973): pair correlation = sin(pi*x)/(pi*x)")
    print("   Odlyzko (1987): verified numerically for first 10^20 zeros")
    print()
    print("   The Riemann hypothesis is about QUANTUM CHAOS!")

    # 8. Finance
    print()
    print("8. FINANCE: CORRELATION MATRICES")
    print("-" * 70)
    print()
    print("   Eigenvalue distribution of stock correlation matrices")
    print("   follows Marchenko-Pastur (noise) + outliers (signal)")
    print()
    fin_evals = generate_financial_correlation(50, 200)
    print("   Assets: 50, Days: 200")
    print("   Eigenvalue range: [%.2f, %.2f]" % (np.min(fin_evals), np.max(fin_evals)))
    print("   Max eigenvalue: %.2f (market mode)" % np.max(fin_evals))
    print("   Min eigenvalue: %.2f (noise floor)" % np.min(fin_evals))
    print()
    print("   The Marchenko-Pastur law separates signal from noise!")
    print("   Connects to finance (Ch.38)")

    # 9. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO ALL PRIOR 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   RMT connects to EVERYTHING:")
    print()
    print("   Zeta zeros (Ch.25)  -> Montgomery-Odlyzko = GUE")
    print("   E8 (Ch.24)          -> Lie algebras classify ensembles")
    print("   Chaos (Ch.43)       -> Quantum chaos = RMT")
    print("   Finance (Ch.38)     -> Correlation matrices")
    print("   Consciousness (Ch.34)-> Neural connectivity")
    print("   Ising (Ch.36)       -> Density of states")
    print("   Quantum (Ch.39)     -> Quantum RMT")
    print()
    print("   The RMT 0/0 is the MOST UNIVERSAL!")
    print("   Level repulsion: P(s=0) = 0 everywhere!")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   RMT has 0/0 of universal randomness:")
    print()
    print("   1. LEVEL REPULSION:")
    print("      P(s=0) = 0 (eigenvalues never coincide)")
    print("      beta=1 (GOE), beta=2 (GUE), beta=4 (GSE)")
    print()
    print("   2. WIGNER SURMISE:")
    print("      P(s) ~ s^beta * exp(-(beta+2)*s^2/4)")
    print("      UNIVERSAL for all three ensembles")
    print()
    print("   3. MONTEGOMERY-ODLYZKO:")
    print("      Zeta zeros follow GUE!")
    print("      Primes are 'quantum chaotic'")
    print()
    print("   4. FINANCE:")
    print("      Correlation matrices follow Marchenko-Pastur")
    print("      Signal vs noise separation")
    print()
    print("   The RMT 0/0 is the MOST UNIVERSAL!")
    print("   Level repulsion: P(s=0) = 0 everywhere!")

    # Save
    results = {
        'rmt': {
            'name': 'Random Matrix Theory',
            'ensembles': {
                'GOE': {'beta': 1, 'symmetry': 'real symmetric'},
                'GUE': {'beta': 2, 'symmetry': 'complex Hermitian'},
                'GSE': {'beta': 4, 'symmetry': 'quaternion'},
            },
            'level_repulsion': 'P(s=0) = 0 (0/0)',
            'wigner_semicircle': True,
        },
        'wigner_surmise': {
            'formula': 'P(s) ~ s^beta * exp(-(beta+2)*s^2/4)',
            'universal': True,
        },
        'montgomery_odlyzko': {
            'pair_correlation': 'GUE',
            'implies': 'Primes are quantum chaotic',
            'connected_to_riemann': True,
        },
        'finance': {
            'distribution': 'Marchenko-Pastur',
            'signal_noise_separation': True,
        },
        'connections': {
            'connects_to': ['Zeta zeros', 'E8', 'Chaos', 'Finance', 'Consciousness', 'Ising'],
            'most_universal': True,
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'random_matrix_theory.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()
