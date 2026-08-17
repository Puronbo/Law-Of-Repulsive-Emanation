"""
Cauchy integral formula via 0/0
================================
The Cauchy integral formula: f(a) = (1/2pi i) oint f(z)/(z-a) dz

At z = a, the integrand f(z)/(z-a) is 0/0 when f(a) = 0. By L'Hopital:

  lim_{z->a} f(z)/(z-a) = f'(a)

The removable value is f'(a), the derivative at the zero.

Examples:
  sin(z)/z at z=0: 0/0, removable = cos(0) = 1
  cos(z)/(z-pi/2) at z=pi/2: 0/0, removable = -sin(pi/2) = -1
  (z-1)^3/(z-1) at z=1: 0/0, removable = 0 (higher-order zero)

The 0/0 encodes the derivative: the residue of the removable singularity
equals the first derivative, which equals the contour integral coefficient.

HONEST WALL: numerical limit computation, not a proof of Cauchy's formula.
"""

import numpy as np
import json


def removable_limit(f, a, h_vals):
    """Compute f(z)/(z-a) for z = a + h, showing the 0/0 -> f'(a) limit."""
    results = []
    for h in h_vals:
        z = a + h
        ratio = float((f(z) / (z - a)).real)
        results.append({"h": float(h), "ratio": ratio})
    return results


def run():
    results = {}

    # --- Test 1: sin(z)/z at z=0 ---
    f1 = lambda z: np.sin(z)
    a1 = 0.0
    deriv1 = 1.0
    h_vals = [10.0 ** (-k) for k in range(1, 13)]
    lim1 = removable_limit(f1, a1, h_vals)
    err1 = abs(lim1[-1]["ratio"] - deriv1)
    results["sin_z_over_z"] = {
        "removable_limit": lim1,
        "expected_removable": deriv1,
        "limit_error": err1,
    }

    # --- Test 2: cos(z)/(z-pi/2) at z=pi/2 ---
    f2 = lambda z: np.cos(z)
    a2 = np.pi / 2
    deriv2 = -1.0
    h_vals2 = [10.0 ** (-k) for k in range(1, 13)]
    lim2 = removable_limit(f2, a2, h_vals2)
    err2 = abs(lim2[-1]["ratio"] - deriv2)
    results["cos_z_over_z_minus_pi2"] = {
        "removable_limit": lim2,
        "expected_removable": deriv2,
        "limit_error": err2,
    }

    # --- Test 3: (z-1)^2/(z-1) at z=1 ---
    f3 = lambda z: (z - 1) ** 2
    a3 = 1.0
    deriv3 = 0.0
    h_vals3 = [10.0 ** (-k) for k in range(1, 13)]
    lim3 = removable_limit(f3, a3, h_vals3)
    err3 = abs(lim3[-1]["ratio"] - deriv3)
    results["z_minus_1_squared"] = {
        "removable_limit": lim3,
        "expected_removable": deriv3,
        "limit_error": err3,
    }

    # --- Test 4: (e^z - 1)/z at z=0 ---
    f4 = lambda z: np.exp(z) - 1.0
    a4 = 0.0
    deriv4 = 1.0  # d/dz(e^z-1) at 0 = e^0 = 1
    h_vals4 = [10.0 ** (-k) for k in range(1, 13)]
    lim4 = removable_limit(f4, a4, h_vals4)
    err4 = abs(lim4[-1]["ratio"] - deriv4)
    results["exp_z_minus_1_over_z"] = {
        "removable_limit": lim4,
        "expected_removable": deriv4,
        "limit_error": err4,
    }

    # --- Test 5: (1 - cos(z))/z^2 at z=0 (0/0, removable = 1/2) ---
    f5 = lambda z: 1.0 - np.cos(z)
    a5 = 0.0
    removable5 = 0.5  # (1-cos z)/z^2 -> 1/2 by L'Hopital
    h_vals5 = [10.0 ** (-k) for k in range(2, 8)]
    lim5_results = []
    for h in h_vals5:
        z = a5 + h
        ratio = float((2.0 * np.sin(z / 2.0) ** 2) / (z ** 2)).real
        lim5_results.append({"h": float(h), "ratio": ratio})
    err5 = abs(lim5_results[-1]["ratio"] - removable5)
    results["one_minus_cos_over_z2"] = {
        "removable_limit": lim5_results,
        "expected_removable": removable5,
        "limit_error": err5,
    }

    # --- Summary ---
    max_err = max(err1, err2, err3, err4, err5)
    supported = bool(max_err < 1e-4)
    results["summary"] = {
        "max_limit_error": max_err,
        "supported": supported,
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Cauchy integral formula via 0/0")
    print(f"  sin(z)/z rem error:          {results['sin_z_over_z']['limit_error']:.2e}")
    print(f"  cos(z)/(z-pi/2) rem error:   {results['cos_z_over_z_minus_pi2']['limit_error']:.2e}")
    print(f"  (z-1)^2/(z-1) rem error:     {results['z_minus_1_squared']['limit_error']:.2e}")
    print(f"  (e^z-1)/z rem error:          {results['exp_z_minus_1_over_z']['limit_error']:.2e}")
    print(f"  (1-cos z)/z^2 rem error:      {results['one_minus_cos_over_z2']['limit_error']:.2e}")
    print(f"  max error: {s['max_limit_error']:.2e}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/cauchy_integral_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
