"""Reproduce the puno_flow benchmark card: the testable exactness story.

Prints the bit-exactness verdicts and the headline scaling number (indexed 2D
flow at n=100k where the all-pairs distance matrix would need tens of GB).

Usage:  python puno_flow/examples/benchmark_card.py
"""

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from puno_flow import FlowEngine, verify_exact


def main():
    rng = np.random.RandomState(1)

    X = rng.uniform(-0.5, 0.5, (2000, 2))
    ok, report = verify_exact(X, k=12, steps=5)
    print("bit-exactness (grid vs brute force, indexed flow vs exact flow):")
    for key, val in report.items():
        print(f"  {key}: {val}")
    print(f"  verdict: {report['verdict']}")

    n = 100_000
    X = rng.uniform(-1.0, 1.0, (n, 2))
    net = FlowEngine(dim=2, k=8, use_index=True,
                     index_min_n=2).add_many(X, X)
    t0 = time.time()
    net.settle(2)
    ms = (time.time() - t0) * 1000.0 / 2
    d_gb = n * n * 2 * 8 / 1e9
    print(f"\nindexed 2D flow  n={n:,}:  {ms:.1f} ms/step "
          f"(all-pairs distance matrix would need {d_gb:,.0f} GB)")
    print(f"spacing {net.spacing():.4f}   finite {np.isfinite(net.q).all()}")


if __name__ == "__main__":
    main()
