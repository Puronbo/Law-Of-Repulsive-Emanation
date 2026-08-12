"""
complex_constant_test.py
========================
Extend the euler_number_test discipline (T57 null, T59/T61 clock test) to pi,
the imaginary unit, and Euler's identity e^(i*pi) = -1.

  PART 1  pi digit-prefix census (mirror the e-test; reversal + tau + digsum).
  PART 2  pi in the framework's own geometry: the golden angle 2*pi/phi^2 on
          the cusp (logarithmic) metric that hosts the golden-ratio closure.
  PART 3  i as the phase/rotation generator: |e^(i*theta)| = 1 is the
          re-encoding invariant (clock test); phase is gauge, magnitude is the
          conserved charge -- the repo's own "period invariant, phase gauge"
          (§3.19) stated for the circle.
  PART 4  e^(i*pi) + 1 = 0: a theorem, not a coincidence. Verified to machine
          precision; e^(i*2pi) = 1 is Poincare recurrence (the closed orbit /
          retrace); e^(i*pi) = -1 is the half-turn = the crease/fold of the
          circle (retrace_boundary doctrine).
  PART 5  The genuine pi-e-i bridge laws (theorems, not near-misses):
          Basel sum -> pi^2/6; Gaussian integral -> sqrt(pi)/2; Stirling ->
          e and pi together; prime number theorem pi(x) ~ x/ln x.
          Also records the repo's own refuted pi-touches (partition-function
          match flagged tautological; Selberg unification closed as Poisson).

Verdict artifact: ../data/complex_constant_test_data.json
"""

import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

PHI = (1 + math.sqrt(5)) / 2
PI_DIGITS = "3141592653589793238462643383279502884197169399375105820974944"
E = math.e


def factor(n):
    fs = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            fs[d] = fs.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        fs[n] = fs.get(n, 0) + 1
    return fs


def tau(fs):
    t = 1
    for p in fs.values():
        t *= p + 1
    return t


def digit_sum(n):
    return sum(int(c) for c in str(n))


def main():
    print("=" * 72)
    print("PART 1  digit-prefix census of pi (T57 mirror of the e-test)")
    print("=" * 72)
    rows = []
    for k in [2, 3, 4, 5, 6, 8, 10, 20]:
        pref = int(PI_DIGITS[:k])
        rev = int(PI_DIGITS[:k][::-1])
        rows.append({
            "k": k, "prefix": pref, "tau": tau(factor(pref)),
            "digit_sum": digit_sum(pref), "reverse_tau": tau(factor(rev)),
            "digit_sum_equal": digit_sum(pref) == digit_sum(rev),
        })
        print(f"  pi[{k:2d} digits] = {pref:20d}  tau={tau(factor(pref)):3d}  "
              f"digsum={digit_sum(pref):3d}  revtau={tau(factor(rev)):3d}")
    # 8-digit pi prefix: 31415926 -> 3,141,592,6... "31415926" -> 2*?*?
    p8 = int(PI_DIGITS[:8])
    print("  pi[8 digits] = 31415926 =", factor(p8), " tau =", tau(factor(p8)))

    print()
    print("=" * 72)
    print("PART 2  pi in the framework's geometry: the golden angle")
    print("=" * 72)
    golden_angle = 2 * math.pi / PHI ** 2
    print("  golden angle = 2*pi/phi^2 = %.4f rad = %.2f deg (fibonacci_spiral.py)"
          % (golden_angle, math.degrees(golden_angle)))
    print("  pi enters as the period of the circle on whose logarithmic (cusp)")
    print("  metric the golden angle and the golden-ratio closure are measured.")

    print()
    print("=" * 72)
    print("PART 3  i as the phase/rotation generator (clock test)")
    print("=" * 72)
    thetas = np.linspace(0, 8 * math.pi, 200001)
    mag = np.abs(np.exp(1j * thetas))
    max_dev = float(np.max(np.abs(mag - 1.0)))
    print("  |e^(i*theta)| over 200k samples: max deviation from 1 = %.2e"
          % max_dev)
    print("  -> magnitude is the invariant (the conserved charge / C0 of the")
    print("     circle); the phase is gauge -- the repo's own 'period is the")
    print("     invariant, phase is the gauge' (§3.19 circadian) in complex form.")

    print()
    print("=" * 72)
    print("PART 4  e^(i*pi) = -1: theorem, not coincidence")
    print("=" * 72)
    epi = complex(math.e ** (1j * math.pi))
    print("  e^(i*pi)      = %.17f %+.17fi" % (epi.real, epi.imag))
    print("  e^(i*pi)+1    = %.2e %+.2ei (machine zero)" % (abs(epi.real + 1), epi.imag))
    e2pi = complex(math.e ** (1j * 2 * math.pi))
    print("  e^(i*2*pi)    = %.17f %+.17fi (recurrence: closed orbit / retrace)"
          % (e2pi.real, e2pi.imag))
    print("  reading: the half-turn (crease) sends 1 -> -1; the full turn is")
    print("  Poincare recurrence; both are theorems -- re-encoding-invariant,")
    print("  unlike every digit coincidence tested in PART 1.")

    print()
    print("=" * 72)
    print("PART 5  the genuine pi-e-i bridge laws (theorems)")
    print("=" * 72)
    N = 100000
    basel = sum(1.0 / (n * n) for n in range(1, N + 1))
    print("  Basel:   sum 1/n^2 (n<=%d) = %.9f  vs  pi^2/6 = %.9f  (delta %.2e)"
          % (N, basel, math.pi ** 2 / 6, abs(basel - math.pi ** 2 / 6)))
    x = np.linspace(0, 12, 2000001)
    gauss = float(np.trapezoid(np.exp(-x * x), x))
    print("  Gauss:   int e^-x^2 [0,12] = %.9f  vs  sqrt(pi)/2 = %.9f  (delta %.2e)"
          % (gauss, math.sqrt(math.pi) / 2, abs(gauss - math.sqrt(math.pi) / 2)))
    for n in (10, 50, 100, 170):
        stirling = math.log(math.sqrt(2 * math.pi * n) * (n / E) ** n)
        exact = math.lgamma(n + 1)
        print("  Stirling: ln(%d!) ~ %.6f  vs  ln(sqrt(2*pi*n)(n/e)^n) = %.6f  (delta %.2e)"
              % (n, exact, stirling, abs(stirling - exact)))

    print()
    print("  Prime number theorem: pi(x) ~ x/ln(x)  (pi the function, e the base)")
    limit = 10 ** 7
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    pi_counts = {}
    for k in range(3, 8):
        m = 10 ** k
        pi_counts[m] = int(np.count_nonzero(sieve[:m + 1]))
    for m, pc in sorted(pi_counts.items()):
        pnt = m / math.log(m)
        print("  pi(10^%d) = %9d   x/ln x = %10.2f   ratio = %.4f"
              % (int(math.log10(m)), pc, pnt, pc / pnt))

    print()
    print("  Repo's own pi-touches already refuted or flagged:")
    print("   - partition-function match L(2)=40.14 vs C0*pi^2/6: tautology")
    print("     for ANY C0 (AUDIT 4); pi^2/6 itself is a real law (Basel).")
    print("   - Selberg unification (spectrum <-> Mersenne geodesics): closed")
    print("     2026-08-08 as Poisson, no zero-correspondence (AUDIT 4).")

    out = {
        "claim": "Connections of pi, i, and e^(i*pi) under the framework's own "
                 "null / clock-test / theorem discipline",
        "part1_pi_census": rows,
        "part2_golden_angle": {
            "golden_angle_deg": round(math.degrees(golden_angle), 4),
            "reading": "pi enters as the circle's period on the cusp "
                       "(logarithmic) metric hosting the golden angle.",
        },
        "part3_i_phase_gauge": {
            "max_magnitude_deviation": max_dev,
            "reading": "|e^(i*theta)| = 1 is the invariant; phase is gauge "
                       "(T59/T61, §3.19 in complex form).",
        },
        "part4_euler_identity": {
            "e_i_pi": [round(epi.real, 17), round(epi.imag, 17)],
            "residual_of_e_ipi_plus_1": [abs(epi.real + 1), abs(epi.imag)],
            "reading": "e^(i*pi) = -1 is a theorem (the half-turn / crease); "
                       "e^(i*2*pi) = 1 is recurrence; re-encoding-invariant, "
                       "unlike digit coincidences.",
        },
        "part5_bridge_laws": {
            "basel": [round(basel, 9), round(math.pi ** 2 / 6, 9)],
            "gaussian": [round(gauss, 9), round(math.sqrt(math.pi) / 2, 9)],
            "stirling_deltas": [
                abs(math.log(math.sqrt(2 * math.pi * n) * (n / E) ** n)
                    - math.lgamma(n + 1)) for n in (10, 50, 100, 170)
            ],
            "pnt": {str(m): [pc, round(pc / (m / math.log(m)), 4)]
                    for m, pc in sorted(pi_counts.items())},
            "repo_pi_touches": "partition-function match flagged tautological "
                               "for any C0; Selberg unification closed as "
                               "Poisson (AUDIT 4).",
        },
        "verdict": (
            "pi, i, and e^(i*pi) are not digit coincidences to null-test: they "
            "are the framework's own rotation geometry. pi is the circle's "
            "period (golden angle 2*pi/phi^2, Basel pi^2/6, Gaussian sqrt(pi), "
            "Stirling, and the prime-counting pi(x) ~ x/ln x that ties pi and "
            "e through primes). i is the phase generator -- the phase is gauge, "
            "the magnitude is the invariant conserved charge. e^(i*pi) = -1 is "
            "the half-turn crease and e^(i*2*pi) = 1 the recurrence: theorems "
            "that survive every re-encoding, the exact opposite of the "
            "digit-prefix 'laws' that the clock test kills. The framework's "
            "own pi-touches (partition function, Selberg) were already "
            "refuted/flagged; the pi-i-e bridge that survives is the theorem "
            "web, not the numerics."
        ),
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "complex_constant_test_data.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\nverdict:", out["verdict"])
    print("wrote data/complex_constant_test_data.json")


if __name__ == "__main__":
    main()
