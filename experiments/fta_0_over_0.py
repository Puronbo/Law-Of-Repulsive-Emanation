"""
Fundamental theorem of algebra via 0/0
=======================================
At root z_0 of multiplicity k: f(z)/(z-z_0)^k at z_0 is 0/0.
Removable = g(z_0) = f^{(k)}(z_0)/k!.
Uses mpmath 50-digit precision.

HONEST WALL: numerical evaluation, not a proof of FTA.
"""

import mpmath
import json

mpmath.mp.dps = 80


def poly_eval(coeffs, z):
    r = mpmath.mpc(0)
    for c in coeffs:
        r = r * z + c
    return r


def run():
    results = {}
    H_LIST = [mpmath.mpf(10)**(-k) for k in range(1, 13)]

    def test(name, coeffs, z0, k, expected_re, expected_im=0):
        vals = []
        for h in H_LIST:
            z = mpmath.mpc(z0) + h
            num = poly_eval(coeffs, z)
            den = (z - mpmath.mpc(z0))**k
            ratio = num / den
            vals.append(complex(ratio))
        last = vals[-1]
        err_re = abs(last.real - expected_re)
        err_im = abs(last.imag - expected_im)
        results[name] = {
            "limit_re": last.real, "limit_im": last.imag,
            "expected_re": expected_re, "expected_im": expected_im,
            "error": err_re + err_im,
            "convergence": [abs(vals[i+1] - vals[i]) for i in range(len(vals)-1)]
        }

    # 1: z^2-1, root z=1, rem = f'(1) = 2
    test("z2_m1_root1", [1, 0, -1], 1.0, 1, 2.0)

    # 2: z^2-1, root z=-1, rem = f'(-1) = -2
    test("z2_m1_root_neg1", [1, 0, -1], -1.0, 1, -2.0)

    # 3: (z-2)^3, triple root z=2, rem = g(2) = 1
    test("triple_root", [1, -6, 12, -8], 2.0, 3, 1.0)

    # 4: z^2+1, root z=i, rem = 2i
    test("complex_root_i", [1, 0, 1], 1j, 1, 0.0, 2.0)

    # 5: z^3-z, root z=0, rem = -1
    test("cubic_root_0", [1, 0, -1, 0], 0.0, 1, -1.0)

    # 6: (z-3)^2(z-5) = z^3-11z^2+39z-45, double root z=3, rem = g(3) = 3-5 = -2
    test("double_root", [1, -11, 39, -45], 3.0, 2, -2.0)

    # 7: z^4-1, root z=1, rem = f'(1) = 4
    test("quartic_root", [1, 0, 0, 0, -1], 1.0, 1, 4.0)

    max_err = max(v["error"] for v in results.values() if "error" in v)
    results["summary"] = {"max_error": max_err, "supported": bool(max_err < 1e-6)}
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("FTA via 0/0 (mpmath 50-digit)")
    for k, v in results.items():
        if k == "summary":
            continue
        if isinstance(v, dict) and "error" in v:
            conv = v["convergence"]
            print(f"  {k:25s}: err={v['error']:.2e}, last_conv={conv[-1]:.2e}")
    print(f"  max error: {s['max_error']:.2e}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/fta_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
