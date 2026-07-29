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
    ("Formal Proofs (26 results: 5 axioms + 3 lemmas + 10 theorems + 8 corollaries)", "python", "Universals/proofs.py"),
    ("Validation (121 tests)", "python", "Universals/math_validation.py"),
    ("Dual Attestation (12 dualities)", "python", "Universals/duality.py"),
    ("Engine (7 phases)", "python", "Universals/engine.py"),
    ("Experiment 1: Subgradient", "python", "Universals/exp1_crease_subgradient.py"),
    ("Experiment 1b: Narrower threshold", "python", "Universals/exp1b_crease_subgradient.py"),
    ("Experiment 2: Crease vs Boundary", "python", "Universals/exp2_crease_density.py"),
    ("Experiment 3: Early Stopping", "python", "Universals/exp3_early_stop.py"),
    ("Experiment: OOD Detection", "python", "Universals/demo_ood.py"),
    ("Experiment: Pruning", "python", "Universals/exp_pruning.py"),
    ("Prime Geodesics Analysis", "python", "Universals/prime_analysis.py"),
    ("Noether Charge = C0 (same as C0 law)", "python", "Universals/noether_analysis.py"),
    ("Energy Landscape Critical Points", "python", "Universals/energy_landscape.py"),
    ("Spectral + Bekenstein (matched-pairs)", "python", "Universals/spectral_analysis.py"),
    ("Modular Forms + L-Functions (tautological)", "python", "Universals/modular_forms.py"),
    ("Quantum Thermodynamics", "python", "Universals/thermodynamics.py"),
    ("Mersenne Gap Analysis", "python", "Universals/mersenne_gaps.py", ["--verified"]),
    ("Mersenne Taxonomy: L_k(s)", "python", "Universals/mersenne_taxonomy.py"),
    ("Mersenne Congruence: Sieve Analysis", "python", "Universals/mersenne_congruence.py"),
    ("Selberg Unification (algebraic identity only)", "python", "Universals/selberg_unification.py"),
    ("C0 Law Dashboard Data", "python", "generate_c0_data.py"),
    ("Quickstart Example", "python", "example.py"),
]

start = time.time()
passed = 0
failed = 0

print("=" * 60)
print("PUNO CALCULUS - COMPLETE RUN")
print("=" * 60)

for item in steps:
    label = item[0]
    script = item[2]
    args = item[3] if len(item) > 3 else []
    print(f"\n--- {label} ---")
    cmd = [sys.executable, script] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start
    if result.returncode == 0:
        print(f"  PASS ({elapsed:.1f}s)")
        passed += 1
    else:
        print(f"  FAIL (exit {result.returncode})")
        if result.stderr:
            print(result.stderr[:500])
        if result.stdout:
            print(result.stdout[-500:])
        failed += 1

elapsed = time.time() - start
print(f"\n{'=' * 60}")
print(f"COMPLETE: {passed} passed, {failed} failed in {elapsed:.0f}s")
print(f"{'=' * 60}")

sys.exit(0 if failed == 0 else 1)
