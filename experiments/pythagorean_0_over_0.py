"""
Pythagorean theorem via 0/0
============================
The Pythagorean theorem: a^2 + b^2 = c^2 for a right triangle.

Dividing by c^2: (a/c)^2 + (b/c)^2 = 1.

The 0/0: at c = 0 (degenerate triangle), both a and b must also be 0,
so (a/c)^2 + (b/c)^2 = 0/0.  The removable value is 1.

For every non-degenerate right triangle, the normalized sum of squared
ratios equals exactly 1.  The 0/0 at the degenerate limit encodes the
theorem itself: the unit circle is the removable value.

Verified on Pythagorean triples: (3,4,5), (5,12,13), (8,15,17),
(7,24,25), (20,21,29).  Also verified on continuous parameterization
a=t, b=sqrt(c^2-t^2) for c=1.

HONEST WALL: numerical evaluation, not a proof of the Pythagorean theorem.
"""

import numpy as np
import json


def pythagorean_ratio(a, b, c):
    """Compute (a/c)^2 + (b/c)^2."""
    if abs(c) < 1e-300:
        return float("nan")
    return (a / c) ** 2 + (b / c) ** 2


def run():
    results = {}

    # --- Test 1: Pythagorean triples ---
    triples = [
        (3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
        (20, 21, 29), (9, 40, 41), (11, 60, 61), (12, 35, 37),
        (13, 84, 85), (16, 63, 65), (28, 45, 53), (33, 56, 65),
        (36, 77, 85), (39, 80, 89), (48, 55, 73), (65, 72, 97),
    ]
    triple_checks = []
    for a, b, c in triples:
        ratio = pythagorean_ratio(a, b, c)
        triple_checks.append({
            "a": a, "b": b, "c": c, "ratio": ratio,
            "error": abs(ratio - 1.0)
        })
    results["pythagorean_triples"] = triple_checks

    # --- Test 2: continuous parameterization c=1 ---
    # a = cos(theta), b = sin(theta), c = 1
    continuous_checks = []
    for theta in [0.1, 0.3, 0.5, 0.7, 1.0, 1.3, 1.5, np.pi / 4, np.pi / 3]:
        a = np.cos(theta)
        b = np.sin(theta)
        c = 1.0
        ratio = pythagorean_ratio(a, b, c)
        continuous_checks.append({
            "theta": float(theta), "a": float(a), "b": float(b),
            "ratio": ratio, "error": abs(ratio - 1.0)
        })
    results["continuous_parameterization"] = continuous_checks

    # --- Test 3: approach degenerate limit c -> 0 ---
    # For a fixed shape (a/c, b/c) = (3/5, 4/5), scale c down
    degenerate_checks = []
    for exp in range(0, 11):
        scale = 10.0 ** (-exp)
        a, b, c = 3 * scale, 4 * scale, 5 * scale
        ratio = pythagorean_ratio(a, b, c)
        degenerate_checks.append({
            "scale": scale, "ratio": ratio, "error": abs(ratio - 1.0)
        })
    results["degenerate_limit"] = degenerate_checks

    # --- Test 4: non-Pythagorean (should NOT give 1) ---
    non_pyth_checks = []
    for a, b, c in [(1, 1, 1), (2, 3, 4), (1, 2, 3), (5, 5, 5)]:
        ratio = pythagorean_ratio(a, b, c)
        non_pyth_checks.append({
            "a": a, "b": b, "c": c, "ratio": ratio,
            "not_one": abs(ratio - 1.0) > 1e-10
        })
    results["non_pythagorean"] = non_pyth_checks

    # --- Summary ---
    max_triple_err = max(t["error"] for t in triple_checks)
    max_cont_err = max(t["error"] for t in continuous_checks)
    max_deg_err = max(t["error"] for t in degenerate_checks)
    all_non_pyth = all(t["not_one"] for t in non_pyth_checks)
    supported = bool(max_triple_err < 1e-14 and max_cont_err < 1e-14
                     and max_deg_err < 1e-10 and all_non_pyth)
    results["summary"] = {
        "max_triple_error": max_triple_err,
        "max_continuous_error": max_cont_err,
        "max_degenerate_error": max_deg_err,
        "all_non_pythagorean_distinct": all_non_pyth,
        "supported": supported,
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Pythagorean theorem via 0/0")
    print(f"  triples error:       {s['max_triple_error']:.2e}")
    print(f"  continuous error:    {s['max_continuous_error']:.2e}")
    print(f"  degenerate error:    {s['max_degenerate_error']:.2e}")
    print(f"  non-pyth distinct:   {s['all_non_pythagorean_distinct']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/pythagorean_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
