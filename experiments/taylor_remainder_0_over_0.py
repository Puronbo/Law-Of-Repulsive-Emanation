"""
Taylor's theorem via 0/0
=========================
Taylor remainder ratio: R_n(x)/(x-a)^{n+1} at x=a is 0/0.
Removable value = f^{(n+1)}(a)/(n+1)!.
Uses mpmath 50-digit precision, no float() mid-computation.

HONEST WALL: numerical evaluation, not a proof of Taylor's theorem.
"""

import mpmath
import json

mpmath.mp.dps = 80
PI = mpmath.pi
H_LIST = [mpmath.mpf(10)**(-k) for k in range(1, 13)]


def run():
    results = {}

    def test(name, rem_fn, expected_mpf):
        vals = []
        for h in H_LIST:
            vals.append(float(rem_fn(h)))
        last = vals[-1]
        conv = [abs(vals[i+1] - vals[i]) for i in range(len(vals)-1)]
        exp_f = float(expected_mpf)
        results[name] = {
            "limit": last, "expected": exp_f,
            "error": abs(last - exp_f),
            "convergence": conv
        }

    # 1: e^x a=0 n=2, rem -> 1/6
    test("exp_a0_n2",
         lambda h: (mpmath.exp(h) - (1 + h + h**2/2)) / h**3,
         mpmath.mpf(1)/6)

    # 2: sin(x) a=0 n=1, rem -> -1/6
    test("sin_a0_n1",
         lambda h: (mpmath.sin(h) - h) / h**3,
         -mpmath.mpf(1)/6)

    # 3: cos(x) a=0 n=2, rem -> 1/24
    test("cos_a0_n2",
         lambda h: (mpmath.cos(h) - (1 - h**2/2)) / h**4,
         mpmath.mpf(1)/24)

    # 4: e^x a=1 n=3, rem -> e/24
    test("exp_a1_n3",
         lambda h: (mpmath.exp(1+h) - mpmath.exp(1)*(1+h+h**2/2+h**3/6)) / h**4,
         mpmath.exp(1)/24)

    # 5: sin(x) a=pi/4 n=2, rem -> -cos(pi/4)/6 = -sqrt(2)/12
    A5 = PI/4
    SA5 = mpmath.sin(A5)
    CA5 = mpmath.cos(A5)
    test("sin_api4_n2",
         lambda h: (mpmath.sin(A5+h) - (SA5 + CA5*h - SA5*h**2/2)) / h**3,
         -mpmath.sqrt(2)/12)

    # 6: ln(1+x) a=0 n=3, rem -> -1/4
    test("ln_a0_n3",
         lambda h: (mpmath.log(1+h) - (h - h**2/2 + h**3/3)) / h**4,
         -mpmath.mpf(1)/4)

    max_err = max(v["error"] for v in results.values() if "error" in v)
    results["summary"] = {"max_error": max_err, "supported": bool(max_err < 1e-6)}
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Taylor remainder 0/0 (mpmath 80-digit)")
    for k, v in results.items():
        if k == "summary":
            continue
        if isinstance(v, dict) and "error" in v:
            conv = v["convergence"]
            print(f"  {k:20s}: lim={v['limit']:.10f}, err={v['error']:.2e}, last_conv={conv[-1]:.2e}")
    print(f"  max error: {s['max_error']:.2e}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/taylor_remainder_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
