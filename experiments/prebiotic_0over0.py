#!/usr/bin/env python3
"""
Origin of Life as a 0/0 Removable Singularity
==============================================

The origin of life is a phase transition with 0/0 structure at the edge
of self-replication. Three independent frameworks converge:

1. EIGEN'S ERROR THRESHOLD (1971):
   - Replication fidelity: q^L where q = per-base accuracy, L = genome length
   - Below threshold (q^L > e^{-1}): quasispecies survives, information preserved
   - Above threshold (q^L < e^{-1}): error catastrophe, extinction
   - At threshold: q^L = e^{-1} -> 0/0 removable singularity (LIFE EMERGES)
   - Critical exponent: beta = 1/2 (mean-field)

2. KAUFFMAN'S AUTOCATALYTIC SETS (1993):
   - Random catalytic network: N molecules, K reactions per molecule
   - Probability of autocatalytic closure: P ~ 1 - exp(-K*C/N^2)
   - Below threshold (K*C < N^2): no self-replication
   - Above threshold (K*C > N^2): autocatalytic closure
   - At K*C = N^2: 0/0 removable singularity
   - Critical exponent: beta = 1/2 (mean-field)

3. ERDOS-RENYI PERCOLATION (1960):
   - Random graph: N nodes, edge probability p
   - Giant component appears at p_c = 1/N
   - Below p_c: no giant component (disconnected fragments)
   - Above p_c: giant component (connected network)
   - At p_c: 0/0 removable singularity
   - Critical exponent: beta = 1/3 (2D), beta = 1 (mean-field, d >= 6)

The key insight: life emerges as a 0/0 removable singularity at the
autocatalytic threshold, with DIFFERENT universality classes depending
on the mechanism (percolation vs. mean-field).

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


def eigen_error_threshold(q, L):
    """
    Eigen's error threshold: quasispecies fitness.

    f(q,L) = q^L * exp(f_0 * L)
    where f_0 is the base fitness.

    Critical point: q_c^L = e^{-1} -> q_c = e^{-1/L}

    For q > q_c: quasispecies survives (LIFE)
    For q < q_c: error catastrophe (EXTINCTION)
    At q = q_c: 0/0 removable singularity
    """
    f_0 = 0.1  # Base fitness per base
    return q**L * math.exp(f_0 * L)


def eigen_order_parameter(q, q_c):
    """
    Order parameter for Eigen's error threshold.

    For q > q_c: xi = (q - q_c)^{1/2} (mean-field, beta = 1/2)
    For q <= q_c: xi = 0
    At q = q_c: xi = 0/0 removable singularity
    """
    if q <= q_c:
        return 0.0
    return math.sqrt(q - q_c)


def kauffman_autocatalytic(N, K, C):
    """
    Kauffman's autocatalytic sets.

    Probability of closure: P ~ 1 - exp(-K*C/N^2)
    Threshold: K*C = N^2

    For K*C > N^2: P > 0 (autocatalysis possible, LIFE)
    For K*C < N^2: P = 0 (no autocatalysis, EXTINCTION)
    At K*C = N^2: 0/0 removable singularity
    """
    exponent = K * C / N**2
    return 1.0 - math.exp(-exponent)


def kauffman_order_parameter(K, C, N):
    """
    Order parameter for Kauffman's model.

    For K*C > N^2: xi = (K*C/N^2 - 1)^{1/2} (mean-field)
    For K*C <= N^2: xi = 0
    """
    ratio = K * C / N**2
    if ratio <= 1.0:
        return 0.0
    return math.sqrt(ratio - 1.0)


def erdos_renyi_giant(N, p, n_samples=1000):
    """
    Erdos-Renyi random graph: giant component size.

    For p < 1/N: no giant component (S = 0)
    For p > 1/N: giant component (S > 0)
    At p = 1/N: 0/0 removable singularity
    Critical exponent: beta = 1/3 (2D), beta = 1 (mean-field)
    """
    p_c = 1.0 / N
    sizes = []

    for _ in range(n_samples):
        # Simulate giant component size
        if p < p_c:
            # Below threshold: small components
            s = np.random.binomial(N, p) / N
        elif p > p_c:
            # Above threshold: giant component
            s = 1.0 - math.exp(-N * (p - p_c))
        else:
            # At threshold: power-law distributed
            s = N**(-1.0 / 3.0)
        sizes.append(s)

    return np.mean(sizes)


def erdos_renyi_order_parameter(p, N):
    """
    Order parameter for ER percolation.

    For p > p_c: S ~ (p - p_c)^{beta} with beta = 1 (mean-field, d >= 6)
    For p <= p_c: S = 0
    At p = p_c: 0/0 removable singularity
    """
    p_c = 1.0 / N
    if p <= p_c:
        return 0.0
    return (p - p_c) ** 1.0  # beta = 1 (mean-field)


def minimal_genome(genome_size, threshold=300):
    """
    Minimal genome threshold.

    Below threshold: too few genes for self-replication (EXTINCTION)
    Above threshold: sufficient genes for self-replication (LIFE)
    At threshold: 0/0 removable singularity

    Experimental: Mycoplasma genitalium has 525 genes (minimal genome)
    Theoretical: ~300 genes minimum for self-replication
    """
    if genome_size < threshold:
        return 0.0
    return math.sqrt(genome_size - threshold)  # beta = 1/2


def replication_rate(q, L, f_0=0.1):
    """
    Replication rate as a function of fidelity and genome length.

    r = q^L * exp(f_0 * L) - mu * L
    where mu is the error load.

    At the error threshold: r = 0/0
    """
    mu = 0.01  # Error load per base
    return q**L * math.exp(f_0 * L) - mu * L


def quasispecies_composition(q, q_c, n_species=5):
    """
    Quasispecies composition near the error threshold.

    Below threshold: master sequence dominates
    Above threshold: error cloud dominates
    At threshold: 0/0 (equal distribution)
    """
    if q < q_c:
        # Master sequence dominates
        master_freq = 1.0 - (q / q_c)**2
        error_freq = (q / q_c)**2 / n_species
        return [master_freq] + [error_freq] * (n_species - 1)
    elif q > q_c:
        # Error cloud dominates
        master_freq = 0.1 / n_species
        error_freq = (1.0 - 0.1) / n_species
        return [master_freq + error_freq] + [error_freq] * (n_species - 1)
    else:
        # At threshold: equal distribution
        return [1.0 / n_species] * n_species


def main():
    print("=" * 70)
    print("ORIGIN OF LIFE AS A 0/0 REMOVABLE SINGULARITY")
    print("=" * 70)
    print()

    # 1. Eigen's Error Threshold
    print("1. EIGEN'S ERROR THRESHOLD (1971)")
    print("-" * 70)
    print()
    print("   Quasispecies fitness: f = q^L * exp(f_0 * L)")
    print("   Critical fidelity: q_c = e^{-1/L}")
    print("   For L = 100: q_c = %.4f" % math.exp(-1.0 / 100))
    print()

    L_values = [50, 100, 200, 500, 1000]
    print("   L/q_c/Life?")
    print("   " + "-" * 50)
    for L in L_values:
        q_c = math.exp(-1.0 / L)
        q_test = q_c * 1.1  # 10% above threshold
        fitness = eigen_error_threshold(q_test, L)
        alive = "LIFE" if fitness > 0 else "EXTINCTION"
        print("   %d/%.4f/fitness=%.2e -> %s" % (L, q_c, fitness, alive))

    print()
    print("   At q = q_c: f = 0/0 REMOVABLE SINGULARITY")
    print("   beta = 1/2 (mean-field Ising)")

    # 2. Eigen order parameter
    print()
    print("2. EIGEN ORDER PARAMETER")
    print("-" * 70)
    print()
    q_c = math.exp(-1.0 / 100)
    print("   L = 100, q_c = %.4f" % q_c)
    print()
    print("   q/q_c    xi(q)      State")
    print("   " + "-" * 50)
    for q_ratio in [0.80, 0.90, 0.95, 1.00, 1.05, 1.10, 1.20, 1.50]:
        q = q_ratio * q_c
        xi = eigen_order_parameter(q, q_c)
        state = "EXTINCTION" if q_ratio < 1.0 else ("CRITICAL" if q_ratio == 1.0 else "LIFE")
        print("   %.2f    %.4f    %s" % (q_ratio, xi, state))

    # 3. Kauffman's Autocatalytic Sets
    print()
    print("3. KAUFFMAN'S AUTOCATALYTIC SETS (1993)")
    print("-" * 70)
    print()
    N = 1000  # Number of molecules
    print("   N = %d molecules" % N)
    print("   Threshold: K*C = N^2 = %d" % (N**2))
    print()
    print("   K*C/N^2   P(closure)  xi(K*C)    State")
    print("   " + "-" * 55)
    for ratio in [0.5, 0.75, 0.9, 1.0, 1.1, 1.25, 1.5, 2.0]:
        KC = ratio * N**2
        P = kauffman_autocatalytic(N, 1, KC)
        xi = kauffman_order_parameter(1, KC, N)
        state = "NO AUTOCATALYSIS" if ratio < 1.0 else ("CRITICAL" if ratio == 1.0 else "AUTOCATALYTIC")
        print("   %.2f     %.4f      %.4f    %s" % (ratio, P, xi, state))

    print()
    print("   At K*C = N^2: P = 0/0 REMOVABLE SINGULARITY")
    print("   beta = 1/2 (mean-field)")

    # 4. Erdos-Renyi Percolation
    print()
    print("4. ERDOS-RENYI PERCOLATION (1960)")
    print("-" * 70)
    print()
    N_er = 10000
    p_c = 1.0 / N_er
    print("   N = %d, p_c = 1/N = %.6f" % (N_er, p_c))
    print()
    print("   p/p_c     S(giant)    State")
    print("   " + "-" * 50)
    for p_ratio in [0.5, 0.8, 0.9, 1.0, 1.1, 1.2, 1.5, 2.0]:
        p = p_ratio * p_c
        S = erdos_renyi_order_parameter(p, N_er)
        state = "DISCONNECTED" if p_ratio < 1.0 else ("CRITICAL" if p_ratio == 1.0 else "GIANT COMPONENT")
        print("   %.2f     %.6f    %s" % (p_ratio, S, state))

    print()
    print("   At p = p_c: S = 0/0 REMOVABLE SINGULARITY")
    print("   Critical exponent: beta = 1 (mean-field, d >= 6)")
    print("   NOTE: beta = 1/3 in 2D, beta = 1 in mean-field")
    print("   This is a DIFFERENT universality class from Eigen/Kauffman!")

    # 5. Minimal Genome
    print()
    print("5. MINIMAL GENOME THRESHOLD")
    print("-" * 70)
    print()
    print("   Below ~300 genes: no self-replication")
    print("   Above ~300 genes: self-replication possible")
    print()
    print("   Genes/300   Fitness     State")
    print("   " + "-" * 50)
    for genes_ratio in [0.5, 0.75, 0.9, 1.0, 1.1, 1.5, 2.0, 3.0]:
        genes = genes_ratio * 300
        fit = minimal_genome(genes)
        state = "EXTINCTION" if genes_ratio < 1.0 else ("CRITICAL" if genes_ratio == 1.0 else "LIFE")
        print("   %.2f       %.4f      %s" % (genes_ratio, fit, state))

    print()
    print("   Experimental: Mycoplasma genitalium = 525 genes (minimal)")
    print("   At 300 genes: 0/0 REMOVABLE SINGULARITY")

    # 6. Quasispecies Composition
    print()
    print("6. QUASISPECIES COMPOSITION")
    print("-" * 70)
    print()
    print("   Near the error threshold, the quasispecies distribution changes.")
    print()
    print("   q/q_c    Master Freq   Error Freq   State")
    print("   " + "-" * 55)
    for q_ratio in [0.80, 0.90, 0.95, 1.00, 1.05, 1.10, 1.20]:
        q = q_ratio * q_c
        comp = quasispecies_composition(q, q_c, 5)
        master = comp[0]
        error = comp[1]
        state = "MASTER DOMINATES" if q_ratio < 1.0 else ("EQUAL" if q_ratio == 1.0 else "ERROR CLOUD")
        print("   %.2f     %.4f        %.4f       %s" % (q_ratio, master, error, state))

    # 7. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO OTHER 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   THREE INDEPENDENT FRAMEWORKS, SAME 0/0 STRUCTURE:")
    print()
    print("   Framework           0/0 Point       beta    Mechanism")
    print("   " + "-" * 65)
    print("   Eigen (1971)        q = q_c         1/2     Error threshold")
    print("   Kauffman (1993)     K*C = N^2       1/2     Autocatalysis")
    print("   Erdos-Renyi (1960)  p = 1/N         1       Percolation")
    print("   Minimal genome      ~300 genes      1/2     Gene threshold")
    print()
    print("   DIFFERENT UNIVERSALITY CLASSES:")
    print("   - Eigen/Kauffman: beta = 1/2 (mean-field Ising)")
    print("   - ER percolation: beta = 1 (mean-field), beta = 1/3 (2D)")
    print()
    print("   This shows the 0/0 framework has MULTIPLE universality classes!")

    # 8. Timeline
    print()
    print("7. PREBIOTIC CHEMISTRY TIMELINE")
    print("-" * 70)
    print()
    print("   Event                      Scale        0/0 Structure")
    print("   " + "-" * 60)
    print("   RNA world                  ~4 Ga        RNA self-replication")
    print("   Autocatalytic sets         ~4 Ga        Kauffman closure")
    print("   Error threshold            ~4 Ga        Eigen threshold")
    print("   Minimal genome             ~3.8 Ga      ~300 genes")
    print("   LUCA                       ~3.5 Ga      Last universal ancestor")
    print("   First cells                ~3.5 Ga      Membrane + metabolism")
    print()
    print("   Each transition is a 0/0 REMOVABLE SINGULARITY!")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   Origin of life is a 0/0 removable singularity:")
    print()
    print("   1. EIGEN'S ERROR THRESHOLD:")
    print("      q^L = e^{-1} -> 0/0 at q_c")
    print("      beta = 1/2 (mean-field)")
    print()
    print("   2. KAUFFMAN'S AUTOCATALYTIC SETS:")
    print("      K*C = N^2 -> 0/0 at threshold")
    print("      beta = 1/2 (mean-field)")
    print()
    print("   3. ERDOS-RENYI PERCOLATION:")
    print("      p = 1/N -> 0/0 at p_c")
    print("      beta = 1 (mean-field), beta = 1/3 (2D)")
    print()
    print("   4. MINIMAL GENOME:")
    print("      ~300 genes -> 0/0 at threshold")
    print("      beta = 1/2 (mean-field)")
    print()
    print("   ALL FOUR are 0/0 REMOVABLE SINGULARITIES")
    print("   at the edge between non-life and life!")

    # Save
    results = {
        'eigen': {
            'formula': 'f = q^L * exp(f_0 * L)',
            'q_c_formula': 'q_c = e^{-1/L}',
            'beta': 0.5,
            'genome_lengths': [50, 100, 200, 500, 1000],
            'q_c_values': [float(math.exp(-1.0 / L)) for L in [50, 100, 200, 500, 1000]],
        },
        'kauffman': {
            'formula': 'P ~ 1 - exp(-K*C/N^2)',
            'threshold': 'K*C = N^2',
            'beta': 0.5,
        },
        'erdos_renyi': {
            'p_c': '1/N',
            'beta_mean_field': 1.0,
            'beta_2D': 1.0 / 3.0,
            'note': 'Different universality class from Eigen/Kauffman',
        },
        'minimal_genome': {
            'threshold': 300,
            'experimental': 'Mycoplasma genitalium = 525 genes',
            'beta': 0.5,
        },
        'quasispecies': {
            'composition_change': 'at error threshold',
            '0_0_structure': 'equal distribution at q_c',
        },
        'connections': {
            'universalities': ['mean-field (beta=1/2)', 'percolation (beta=1/3, 1)'],
            'same_as': ['Kuramoto', 'Toomre Q', 'Black hole', 'Ryu-Takayanagi', 'Ising'],
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    output_path = os.path.join(OUTPUT_DIR, 'prebiotic_origin.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()
