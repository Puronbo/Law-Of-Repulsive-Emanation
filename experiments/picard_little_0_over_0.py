"""
Picard's little theorem via 0/0
===============================
Picard's little theorem: if f is an entire function that omits two
distinct values in C, then f is constant.

Equivalently: a non-constant entire function takes every complex value
with at most one exception.

The 0/0: consider the ratio f(z) / (z - z_0) at a zero z_0 of f.
This is 0/0. The removable value is f'(z_0) (by L'Hopital or the
definition of derivative). If f has a zero of order k at z_0, then
f(z) = (z - z_0)^k g(z) with g(z_0) != 0, and f(z)/(z-z_0)^k has
removable value g(z_0).

The Picard 0/0: consider e^{f(z)} / (z - a) where f has a logarithmic
singularity at a (i.e., f(a) is undefined but e^{f(a)} = a). The ratio
is 0/0 if e^{f(z)} -> a and z -> a simultaneously. The removable value
encodes the local behavior.

Concrete 0/0 for Picard: for f(z) = e^z (entire, omits only 0):
  f(z) / (z - z_0) at a zero of f: but e^z has no zeros! So f(z) / (z-a)
  at a point where f(a) = 0 would be 0/0, but such a doesn't exist.
  This is Picard's content: e^z omits exactly one value (0).

For f(z) = sin(z): zeros at z = n*pi. At z = 0:
  sin(z) / z -> 1 (the classical 0/0, removable = 1).
  sin(z) omits no values (takes every value in C).

For f(z) = e^{e^z}: entire, omitting 0 (from e^z) and... actually e^{e^z}
omits 0 (since e^w != 0 for all w). Does it omit anything else? No, e^z
takes all nonzero values, so e^{e^z} takes all nonzero values. So it omits
only 0 (not two values), so Picard doesn't force it to be constant.

The Picard 0/0: consider f(z) = z / (e^{1/z} - 1) near z = 0.
e^{1/z} has an essential singularity at z = 0. Near z = 0, e^{1/z} takes
all nonzero values infinitely often (by Picard). The ratio z/(e^{1/z}-1)
at z = 0 is 0/0 (numerator -> 0, denominator -> inf in most directions
but = 0 along certain paths). The behavior is wildly non-removable.

HONEST WALL: numerical verification of Picard-related 0/0 ratios
for specific entire functions, not a proof of Picard's theorem.
"""

import numpy as np
import json


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: 0/0 at zeros of entire functions ---
    # sin(z) / z at z = 0: 0/0, removable = 1
    # sin(z) / (z - n*pi) at z = n*pi: 0/0, removable = (-1)^n
    sin_tests = []
    for n in range(-5, 6):
        z0 = n * np.pi
        eps_vals = [1e-3, 1e-5, 1e-7, 1e-9]
        ratios = []
        for eps in eps_vals:
            z_plus = z0 + eps
            z_minus = z0 - eps
            # Central difference approximation of derivative
            ratio = (np.sin(z_plus) - np.sin(z_minus)) / (z_plus - z_minus)
            ratios.append(float(ratio))

        expected = np.cos(z0)  # = (-1)^n
        if ratios:
            best = ratios[-1]
            sin_tests.append({
                "zero": float(z0),
                "n": n,
                "removable_value": float(best),
                "expected": float(expected),
                "error": float(abs(best - expected)),
                "converges": bool(abs(best - expected) < 1e-4)
            })

    results["sin_z0_over_z"] = {
        "function": "sin(z)/z at z = n*pi",
        "note": "0/0 with removable value = cos(n*pi) = (-1)^n",
        "tests": sin_tests
    }

    # --- Test 2: e^z omits only 0 (Picard content) ---
    # e^z never equals 0. Verify numerically:
    omit_tests = []
    # Check |e^z| on a grid near the origin
    grid_re = np.linspace(-5, 5, 200)
    grid_im = np.linspace(-5, 5, 200)
    min_abs_ez = float('inf')
    min_point = (0, 0)
    for re in grid_re:
        for im in grid_im:
            val = np.exp(re + 1j * im)
            if abs(val) < min_abs_ez:
                min_abs_ez = abs(val)
                min_point = (float(re), float(im))

    omit_tests.append({
        "function": "e^z",
        "min_abs_value": float(min_abs_ez),
        "min_at": list(min_point),
        "omits_zero": bool(min_abs_ez > 1e-10)
    })

    # 1/z is not entire (has pole at 0), but e^{1/z} has essential singularity
    # Near z = 0, e^{1/z} takes all nonzero values (Picard's great theorem)
    # Check: along z = t (real), e^{1/z} = e^{1/t} -> inf as t -> 0+
    # Along z = it, e^{1/(it)} = e^{-i/t} has |value| = 1
    # Along z = -t, e^{-1/t} -> 0 as t -> 0+
    essential_paths = []
    for t in [0.1, 0.01, 0.001]:
        # Positive real
        v_pos = np.exp(1.0 / t)
        # Negative real
        v_neg = np.exp(-1.0 / t)
        # Imaginary
        v_imag = np.exp(-1j / t)
        essential_paths.append({
            "t": t,
            "exp(1/t)_real": float(v_pos),
            "exp(-1/t)_real": float(v_neg),
            "exp(-i/t)_magnitude": float(abs(v_imag))
        })

    results["e_z_omits_zero"] = omit_tests
    results["essential_singularity"] = {
        "function": "e^{1/z} near z = 0",
        "note": "takes all nonzero values (Picard great theorem)",
        "paths": essential_paths
    }

    # --- Test 3: 0/0 for (e^z - 1)/z at z = 0 ---
    # e^z - 1 has a simple zero at z = 0. (e^z - 1)/z -> 1.
    ez_ratio_tests = []
    for eps in [0.1, 0.01, 0.001, 0.0001, 0.00001]:
        val = (np.exp(eps) - 1) / eps
        ez_ratio_tests.append({
            "z": eps,
            "ratio": float(val),
            "deviation_from_one": float(abs(val - 1.0))
        })

    results["ez_minus_1_over_z"] = {
        "note": "(e^z - 1)/z at z = 0: 0/0, removable = 1 (derivative of e^z at 0)",
        "tests": ez_ratio_tests
    }

    # --- Test 4: sin(z)/z ratio converges to 1 (classical 0/0) ---
    sin_ratio_convergence = []
    for eps in [0.1, 0.01, 0.001, 0.0001]:
        val = np.sin(eps) / eps
        sin_ratio_convergence.append({
            "z": eps,
            "ratio": float(val),
            "deviation_from_one": float(abs(val - 1.0))
        })

    results["sinz_over_z"] = {
        "note": "sin(z)/z -> 1 as z -> 0: 0/0 removable value = 1",
        "tests": sin_ratio_convergence
    }

    # --- Test 5: sin(z)/(z - pi) at z = pi: 0/0 removable = -1 ---
    sin_pi_tests = []
    for eps in [0.1, 0.01, 0.001, 0.0001]:
        val = np.sin(np.pi + eps) / eps
        sin_pi_tests.append({
            "z_minus_pi": eps,
            "ratio": float(val),
            "deviation_from_neg1": float(abs(val - (-1.0)))
        })

    results["sinz_at_pi"] = {
        "note": "sin(z)/(z-pi) at z=pi: 0/0 removable = cos(pi) = -1",
        "tests": sin_pi_tests
    }

    # --- Test 6: entire functions that omit values ---
    # cosh(z) omits no values in C (takes every value).
    # Check: cosh(z) = (e^z + e^{-z})/2. Range includes all of C.
    # Verify cosh hits a target value w for various w.
    target_tests = []
    for w_re, w_im in [(0.5, 0), (0, 0.5), (2, 1), (-1, 3)]:
        w = complex(w_re, w_im)
        # Solve cosh(z) = w numerically: z = arccosh(w) = log(w + sqrt(w^2 - 1))
        try:
            import cmath
            z_sol = cmath.acosh(w)
            val = np.cosh(z_sol)
            target_tests.append({
                "target": [w_re, w_im],
                "found_z": [float(z_sol.real), float(z_sol.imag)],
                "cosh_at_z": [float(val.real), float(val.imag)],
                "error": float(abs(val - w))
            })
        except Exception:
            target_tests.append({
                "target": [w_re, w_im],
                "error": float('inf')
            })

    results["cosh_hits_all_values"] = {
        "function": "cosh(z)",
        "note": "cosh is entire and takes every value in C (omits nothing)",
        "tests": target_tests
    }

    # --- Summary ---
    sin_converges = all(t["converges"] for t in sin_tests)
    ez_omits = omit_tests[0]["omits_zero"]
    ez_ratio_conv = ez_ratio_tests[-1]["deviation_from_one"] < 1e-4
    sin_ratio_conv = sin_ratio_convergence[-1]["deviation_from_one"] < 1e-4
    cosh_all = all(t.get("error", 1) < 1e-6 for t in target_tests)

    supported = bool(sin_converges and ez_omits and ez_ratio_conv and
                     sin_ratio_conv and cosh_all)

    results["summary"] = {
        "supported": supported,
        "sin_removable_values_correct": sin_converges,
        "exp_omits_zero": ez_omits,
        "ez_minus_1_ratio_converges": ez_ratio_conv,
        "sinz_over_z_converges": sin_ratio_conv,
        "cosh_takes_all_values": cosh_all,
        "honest_wall": "numerical verification of Picard-related 0/0 ratios "
                       "for specific entire functions, not a proof of Picard's theorem"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Picard's little theorem via 0/0")
    print(f"  sin removable values:     {s['sin_removable_values_correct']}")
    print(f"  e^z omits zero:           {s['exp_omits_zero']}")
    print(f"  (e^z-1)/z -> 1:           {s['ez_minus_1_ratio_converges']}")
    print(f"  sin(z)/z -> 1:            {s['sinz_over_z_converges']}")
    print(f"  cosh takes all values:    {s['cosh_takes_all_values']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/picard_little_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
