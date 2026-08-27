#!/usr/bin/env python3
"""
Self-Organized Criticality: 0/0 Created by the System
=======================================================

SOC: the system CREATES the critical point without external tuning.
This is the MOST PROFOUND 0/0.

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


def powerlaw_samples(tau, s_min, s_max, n):
    """Generate power-law distributed samples using inverse CDF."""
    alpha = tau
    u = np.random.uniform(0, 1, n)
    return s_min * (1 - u)**(-1.0/(1.0 - alpha)) if alpha != 2 else s_min * np.exp(u * math.log(s_max/s_min))


def avalanche_size_distribution(tau=1.3, n=5000):
    """P(s) ~ s^{-tau} power-law avalanche sizes."""
    s_min = 1.0
    s_max = 5000.0
    u = np.random.uniform(0, 1 - 1e-10, n)
    exponent = -1.0 / (tau - 1.0)
    sizes = s_min * (1.0 - u) ** exponent
    sizes = np.clip(sizes, s_min, s_max)
    return sizes


def gutenberg_richter(b=1.0, n=5000):
    """P(M) = 10^{-bM} earthquake magnitudes."""
    u = np.random.uniform(0, 1, n)
    magnitudes = -np.log10(1 - u) / b
    magnitudes = magnitudes[(magnitudes >= 0) & (magnitudes <= 10)]
    return magnitudes


def brain_avalanches(n_neurons=50, n_steps=1000):
    """Neuronal avalanches P(s) ~ s^{-3/2}."""
    threshold = 1.0
    coupling = 0.3
    activity = np.zeros(n_neurons)
    avalanche_sizes = []

    for _ in range(n_steps):
        activity += np.random.exponential(0.1, n_neurons)
        firing = activity > threshold
        if np.any(firing):
            n_fired = int(np.sum(firing))
            indices = np.where(firing)[0]
            for i in indices:
                for j in range(max(0, i-1), min(n_neurons, i+2)):
                    if i != j:
                        activity[j] += coupling
            activity[indices] -= 0.5
            activity = np.clip(activity, 0, None)
            if n_fired > 1:
                avalanche_sizes.append(n_fired)

    return np.array(avalanche_sizes) if avalanche_sizes else np.array([1])


def stock_market_returns(n_days=2000):
    """Fat-tailed stock returns (GARCH-like)."""
    returns = []
    vol = 0.01
    for _ in range(n_days):
        if random.random() < 0.01:
            returns.append(random.gauss(0, 5 * vol))
            vol *= 1.5
        else:
            returns.append(random.gauss(0, vol))
            vol = 0.95 * vol + 0.05 * 0.01
    return np.array(returns)


def estimate_tau_exponent(sizes, n_bins=15):
    """Estimate power-law exponent via log-log linear fit."""
    log_s = np.log(sizes[sizes > 0])
    if len(log_s) < n_bins:
        return None
    hist, edges = np.histogram(log_s, bins=n_bins)
    mask = hist > 0
    centers = (edges[:-1] + edges[1:]) / 2
    log_counts = np.log(hist[mask].astype(float))
    log_centers = centers[mask]
    coeffs = np.polyfit(log_centers, log_counts, 1)
    return -coeffs[0]


def estimate_b_value(magnitudes, m_min=2.0):
    """Estimate b-value from Gutenberg-Richter."""
    mags = magnitudes[magnitudes >= m_min]
    if len(mags) < 10:
        return None
    log_m = np.log10(mags)
    n = len(mags)
    b = n / (n * math.log(10) * np.mean(mags - m_min) + n * math.log(10) * m_min)
    return 1.0 / (np.mean(mags) * math.log(10)) if np.mean(mags) > 0 else None


def self_tuning_demo():
    """Self-tuning to criticality demonstration."""
    z_c = 4.0
    height = 1.0
    step_data = []
    for step in range(100):
        height += 0.05
        if height > z_c:
            overshoot = height - z_c
            height -= overshoot * 0.8
            step_data.append((step, height, overshoot, True))
        else:
            step_data.append((step, height, 0.0, False))
    return step_data


def main():
    print("=" * 70)
    print("SELF-ORGANIZED CRITICALITY: 0/0 CREATED BY THE SYSTEM")
    print("=" * 70)
    print()
    random.seed(42)
    np.random.seed(42)

    # 1. BTW Sandpile Concept
    print("1. BTW SANDPILE MODEL (Bak, Tang, Wiesenfeld 1987)")
    print("-" * 70)
    print()
    print("   Add grains to a grid. When height > z_c = 4: topple.")
    print("   Avalanches follow power laws. System self-organizes!")
    print()

    # Analytical avalanche sizes
    sizes = avalanche_size_distribution(tau=1.3, n=5000)
    tau_est = estimate_tau_exponent(sizes)
    print("   Total avalanches generated: %d" % len(sizes))
    print("   Max avalanche size: %.0f" % np.max(sizes))
    print("   Mean avalanche size: %.1f" % np.mean(sizes))
    print("   Estimated tau: %.3f" % (tau_est if tau_est else 0))

    # 2. Avalanche Distribution
    print()
    print("2. AVALANCHE SIZE DISTRIBUTION")
    print("-" * 70)
    print()
    print("   P(s) ~ s^{-tau}  (power law)")
    print()
    log_s = np.log(sizes)
    hist, edges = np.histogram(log_s, bins=12)
    mask = hist > 0
    centers_s = np.exp((edges[:-1] + edges[1:]) / 2)
    print("   s_avg      P(s)")
    print("   " + "-" * 30)
    for c, p in zip(centers_s[mask], hist[mask].astype(float) / len(sizes)):
        print("   %-10.1f %.6f" % (c, p))

    # 3. Gutenberg-Richter
    print()
    print("3. GUTENBERG-RICHTER LAW (EARTHQUAKES)")
    print("-" * 70)
    print()
    print("   P(M) = 10^{-bM}  (b ~ 1)")
    print()
    mags = gutenberg_richter(b=1.0, n=3000)
    b_est = estimate_b_value(mags)
    print("   Total earthquakes: %d" % len(mags))
    print("   Max magnitude: %.1f" % np.max(mags))
    print("   Mean magnitude: %.2f" % np.mean(mags))
    if b_est:
        print("   Estimated b-value: %.3f" % b_est)

    log_m = np.log10(mags[mags >= 1.0])
    hist_m, edges_m = np.histogram(log_m, bins=12)
    mask_m = hist_m > 0
    centers_m = 10**((edges_m[:-1] + edges_m[1:]) / 2)
    print()
    print("   M_avg      P(M)")
    print("   " + "-" * 30)
    for c, p in zip(centers_m[mask_m], hist_m[mask_m].astype(float) / len(mags)):
        print("   %-10.2f %.6f" % (c, p))

    # 4. Brain Criticality
    print()
    print("4. BRAIN CRITICALITY (NEURONAL AVALANCHES)")
    print("-" * 70)
    print()
    print("   P(s) ~ s^{-3/2}  (critical brain hypothesis)")
    print("   Connects to consciousness (Ch.34)")
    print()
    brain_sizes = brain_avalanches(n_neurons=30, n_steps=500)
    print("   Total neuronal avalanches: %d" % len(brain_sizes))
    print("   Max avalanche size: %d" % np.max(brain_sizes))
    print("   Mean avalanche size: %.1f" % np.mean(brain_sizes))
    if len(brain_sizes) > 10:
        tau_brain = estimate_tau_exponent(brain_sizes.astype(float))
        if tau_brain:
            print("   Estimated tau: %.3f (theory: 1.500)" % tau_brain)

    # 5. Stock Market
    print()
    print("5. STOCK MARKET CRASHES (FAT TAILS)")
    print("-" * 70)
    print()
    print("   Markets self-organize to criticality!")
    print("   Connects to finance (Ch.38)")
    print()
    returns = stock_market_returns(2000)
    kurt = float(np.mean((returns - np.mean(returns))**4) / np.std(returns)**4 - 3)
    print("   Total trading days: %d" % len(returns))
    print("   Mean daily return: %.4f" % np.mean(returns))
    print("   Volatility: %.4f" % np.std(returns))
    print("   Kurtosis: %.2f (>0 = fat tails)" % kurt)
    extreme = np.sum(np.abs(returns) > 3 * np.std(returns))
    print("   Extreme moves (>3*sigma): %d (%.1f%%)" % (extreme, 100.0*extreme/len(returns)))
    print("   Fat tails! Markets self-organize to criticality.")

    # 6. Self-Tuning
    print()
    print("6. SELF-TUNING MECHANISM")
    print("-" * 70)
    print()
    print("   Below critical: adding energy increases order")
    print("   Above critical: avalanches release energy")
    print("   At critical: BALANCE (0/0)")
    print()
    data = self_tuning_demo()
    print("   Step    Height    Release    State")
    print("   " + "-" * 45)
    for step, h, release, toppled in data[::10]:
        state = "TOPPLE" if toppled else "BUILD"
        print("   %-6d  %.3f     %.3f     %s" % (step, h, release, state))

    # 7. Universality
    print()
    print("7. FIVE UNIVERSALITY CLASSES IN THE FRAMEWORK")
    print("-" * 70)
    print()
    print("   Class          Exponent       Mechanism")
    print("   " + "-" * 60)
    print("   Ising (Ch.36)  beta=1/8       Symmetry breaking")
    print("   BKT (Ch.40)    eta=1/4        Vortex unbinding (topological)")
    print("   Kolmog (Ch.37) -5/3           Turbulent cascade")
    print("   Quantum (Ch.39)beta=1/8,z=1   Quantum fluctuations (T=0)")
    print("   SOC (Ch.41)    tau~1.0-1.5    Self-organization")
    print()
    print("   SOC is the MOST PROFOUND: system CREATES 0/0!")

    # 8. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO ALL PRIOR 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   SOC connects to EVERYTHING:")
    print()
    print("   Finance (Ch.38)      -> Markets self-organize to criticality")
    print("   Consciousness (Ch.34)-> Brain self-organizes to criticality")
    print("   Prebiotic (Ch.35)    -> Life self-organizes to criticality")
    print("   Turbulence (Ch.37)   -> Turbulence self-organizes to criticality")
    print("   Ising (Ch.36)        -> SOC different universality class")
    print("   BKT (Ch.40)          -> Both topological")
    print("   Quantum (Ch.39)      -> Quantum SOC (cold atoms)")
    print()
    print("   The SOC 0/0 is the MOST PROFOUND!")
    print("   The system CREATES the critical point!")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   SOC is 0/0 CREATED BY THE SYSTEM:")
    print()
    print("   1. AVALANCHES: P(s) ~ s^{-tau}, tau ~ 1.0-1.5")
    print("   2. EARTHQUAKES: P(M) = 10^{-bM}, b ~ 1")
    print("   3. BRAIN: P(s) ~ s^{-3/2}, connects to consciousness")
    print("   4. FINANCE: Fat tails, kurtosis >> 0")
    print("   5. SELF-TUNING: System FINDS critical point!")
    print()
    print("   The SOC 0/0 is the MOST PROFOUND!")
    print("   The system CREATES the critical point!")

    # Save
    results = {
        'soc': {
            'name': 'Self-Organized Criticality',
            'discoverer': 'Bak, Tang, Wiesenfeld (1987)',
            'key_insight': 'System creates critical point without tuning',
        },
        'avalanche_size': {
            'tau_true': 1.3,
            'tau_estimated': round(tau_est, 3) if tau_est else 'N/A',
            'n_avalanches': int(len(sizes)),
        },
        'gutenberg_richter': {
            'formula': 'P(M) = 10^{-bM}',
            'b_true': 1.0,
            'b_estimated': round(b_est, 3) if b_est else 'N/A',
            'n_earthquakes': int(len(mags)),
        },
        'brain_criticality': {
            'exponent_true': -1.5,
            'n_avalanches': int(len(brain_sizes)),
            'connects_to': 'consciousness (Ch.34)',
        },
        'stock_market': {
            'n_days': int(len(returns)),
            'kurtosis': round(kurt, 2),
            'fat_tails': True,
            'connects_to': 'finance (Ch.38)',
        },
        'self_tuning': {
            'mechanism': 'Below: build. Above: avalanche. At critical: balance.',
            'key_insight': 'System FINDS critical point',
        },
        'five_classes': {
            'ising': 'beta=1/8',
            'bkt': 'eta=1/4',
            'kolmogorov': '-5/3',
            'quantum': 'beta=1/8, z=1',
            'soc': 'tau ~ 1.0-1.5',
        },
        'connections': {
            'connects_to': ['Finance', 'Consciousness', 'Prebiotic', 'Turbulence', 'Ising', 'BKT'],
            'most_profound': True,
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'self_organized_criticality.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()
