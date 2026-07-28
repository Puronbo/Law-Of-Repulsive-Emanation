#!/usr/bin/env python3
"""
run_all.py
==========
One command to run everything: validation, engine, experiments, proofs.
Usage:  python run_all.py
"""

import subprocess, sys, time, os

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

steps = [
    ("Validation (88 tests)", "python", "Universals/math_validation.py"),
    ("Engine (7 phases)", "python", "Universals/engine.py"),
    ("Experiment 1: Subgradient", "python", "Universals/exp1_crease_subgradient.py"),
    ("Experiment 1b: Wider threshold", "python", "Universals/exp1b_crease_subgradient.py"),
    ("Experiment 2: Crease vs Boundary", "python", "Universals/exp2_crease_density.py"),
    ("Experiment 3: Early Stopping", "python", "Universals/exp3_early_stop.py"),
    ("Experiment: OOD Detection", "python", "Universals/demo_ood.py"),
    ("Experiment: Pruning", "python", "Universals/exp_pruning.py"),
    ("C0 Law Dashboard Data", "python", "generate_c0_data.py"),
    ("Quickstart Example", "python", "example.py"),
]

start = time.time()
passed = 0
failed = 0

print("=" * 60)
print("PUNO CALCULUS — COMPLETE RUN")
print("=" * 60)

for label, cmd, script in steps:
    print(f"\n--- {label} ---")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    elapsed = time.time() - start
    if result.returncode == 0:
        print(f"  PASS ({elapsed:.1f}s)")
        passed += 1
    else:
        print(f"  FAIL (exit {result.returncode})")
        print(result.stderr[:500])
        failed += 1

elapsed = time.time() - start
print(f"\n{'=' * 60}")
print(f"COMPLETE: {passed} passed, {failed} failed in {elapsed:.0f}s")
print(f"{'=' * 60}")

sys.exit(0 if failed == 0 else 1)
