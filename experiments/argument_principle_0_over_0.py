# argument_principle_0_over_0.py
# Argument principle via the 0/0 probe.
#
# The argument principle: (1/2pi i) oint_C f'(s)/f(s) ds = Z - P
# where Z = zeros inside C, P = poles inside C.
#
# The 0/0: at each zero rho, f(rho) = 0 in the denominator of f'/f.
# The residue (= multiplicity) is the removable value. The 0/0 is
# resolved not by evaluating the limit but by the residue theorem.
#
# We verify by integrating zeta'(s)/zeta(s) around rectangles in the
# critical strip and counting zeros inside. For rectangles that do NOT
# enclose the pole at s=1, the count is Z directly.

import json
import math
import os
import time

import mpmath

OUT = "data/argument_principle_0_over_0_data.json"
mpmath.mp.dps = 30


def zeta_prime_over_zeta(s):
    """Compute zeta'(s)/zeta(s) = d/ds log(zeta(s))."""
    z = mpmath.zeta(s)
    if abs(z) < 1e-50:
        return mpmath.mpc(0, 0)
    h = mpmath.mpf("1e-10")
    zp = (mpmath.zeta(s + h) - mpmath.zeta(s - h)) / (2 * h)
    return zp / z


def contour_integral_rectangle(re_min, re_max, im_min, im_max, n_side=2000):
    """Integrate zeta'/zeta around a rectangle, counter-clockwise.

    The four sides:
      bottom: re_min -> re_max at Im = im_min
      right:  im_min -> im_max at Re = re_max
      top:    re_max -> re_min at Im = im_max
      left:   im_max -> im_min at Re = re_min
    """
    integral = mpmath.mpc(0, 0)

    # Bottom (left to right)
    dr = mpmath.mpf(re_max - re_min) / n_side
    for i in range(n_side):
        t = re_min + i * dr
        integral += zeta_prime_over_zeta(mpmath.mpc(t, im_min)) * dr

    # Right (bottom to top)
    di = mpmath.mpf(im_max - im_min) / n_side
    for i in range(n_side):
        t = im_min + i * di
        integral += zeta_prime_over_zeta(mpmath.mpc(re_max, t)) * mpmath.mpc(0, 1) * di

    # Top (right to left)
    for i in range(n_side):
        t = re_max - i * dr
        integral += zeta_prime_over_zeta(mpmath.mpc(t, im_max)) * (-dr)

    # Left (top to bottom)
    for i in range(n_side):
        t = im_max - i * di
        integral += zeta_prime_over_zeta(mpmath.mpc(re_min, t)) * mpmath.mpc(0, -1) * di

    # argument principle: (1/2pi i) * integral = Z - P
    count = integral / (2 * mpmath.pi * mpmath.mpc(0, 1))
    return count


def run_experiment():
    t0 = time.time()
    results = {}

    # Known zeros (first 10)
    known_zeros = [float(mpmath.zetazero(k).imag) for k in range(1, 11)]

    # Test rectangles
    test_cases = [
        {"name": "first_zero_only",
         "re": (0.1, 0.9), "im": (13, 15),
         "expected": 1,
         "note": "should contain gamma_1 ~ 14.13, no pole (Re=1 not inside)"},
        {"name": "first_two_zeros",
         "re": (0.1, 0.9), "im": (13, 22),
         "expected": 2,
         "note": "gamma_1 ~ 14.13 and gamma_2 ~ 21.02"},
        {"name": "first_four_zeros",
         "re": (0.1, 0.9), "im": (13, 32),
         "expected": 4,
         "note": "first four zeros at 14.13, 21.02, 25.01, 30.42"},
        {"name": "no_zeros",
         "re": (0.1, 0.9), "im": (2, 5),
         "expected": 0,
         "note": "no non-trivial zeros in this range"},
        {"name": "wide_eight_zeros",
         "re": (0.1, 0.9), "im": (13, 48),
         "expected": 8,
         "note": "first eight zeros (last at ~45.33)"},
    ]

    for case in test_cases:
        re_min, re_max = case["re"]
        im_min, im_max = case["im"]
        expected = case["expected"]

        # Ensure we don't enclose the pole at s=1 (it's at Re=1, Im=0)
        # Our rectangles have Re_max < 1, so no pole inside
        count = contour_integral_rectangle(re_min, re_max, im_min, im_max, n_side=2000)
        computed = float(count.real)

        match = abs(computed - expected) < 0.5
        results[case["name"]] = {
            "re_range": case["re"],
            "im_range": case["im"],
            "expected_zeros": expected,
            "computed_count": round(computed, 2),
            "match": match,
            "note": case["note"],
        }
        print(f"  {case['name']}: computed={computed:.2f}, expected={expected}, "
              f"match={match}")

    all_match = all(r["match"] for r in results.values())

    summary = {
        "experiment": "argument_principle_0_over_0",
        "claim": "(1/2pi i) oint zeta'(s)/zeta(s) ds = Z inside rectangle; "
                 "at each zero rho, zeta(rho) = 0 in the denominator of zeta'/zeta "
                 "is the 0/0, the residue (= multiplicity) is the removable value",
        "n_known_zeros": len(known_zeros),
        "known_gamma": [round(g, 6) for g in known_zeros],
        "results": results,
        "verdict": "SUPPORTED" if all_match else "NOT SUPPORTED",
        "honest_wall": "The argument principle is a proven theorem (complex analysis). "
                       "This is a computational verification using numerical contour "
                       "integration of zeta'/zeta. The 0/0 framing: at each zero, "
                       "the denominator zeta(s) = 0 creates a 0/0 in zeta'/zeta, "
                       "resolved by the residue theorem (= multiplicity). The residue "
                       "is the removable value that extracts the zero count.",
        "time_total": round(time.time() - t0, 2),
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nVerdict: {summary['verdict']}")
    print(f"Saved to {OUT}")
    return summary


if __name__ == "__main__":
    run_experiment()
