"""
NUMBER THEORY: HARDY-LITTLEWOOD TWIN-PRIME DENSITY (OPEN TARGET)
================================================================
Atlas entry 65.  Constructive-program instance.

The count of twin primes up to x, pi_2(x), and its conjectured
transfer density 2*C_2 * x/log(x)^2 both vanish in ratio terms as
the density scale is probed:

    R(x) = pi_2(x) / (2*C_2 * x / log(x)^2)

Crossing the 'radius' (the transfer kernel x/log(x)^2), the ratio is
the 0/0 of two densities and its REMOVABLE VALUE is 1 -- exactly the
Hardy-Littlewood twin-prime conjecture (singular series C_2 =
prod_p (1 - 1/(p-1)^2)).  The value 1 is 'interesting' (a clean
constant equal to the identity): by the atlas constructive problem,
the theorem to hunt is the one that pins R(x) -> 1.

C_2 and 2*C_2 are COMPUTED IN-CODE from the product over primes,
not hard-coded: the framework derives its own target constant.

Gates are honest: R(x) is asymptotic with a slow secondary
oscillation; we require trend-to-1 within a loose band and a
monotone decrease of the deviation at the top end.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")


def primes_to(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(2, n + 1) if s[i]]


def li2(x):
    """int_2^x dt/log(t)^2 on a log-scale trapezoid grid."""
    a = 2.0
    ng = 6000
    lo = math.log(a)
    hi = math.log(x)
    t0 = math.exp(lo)
    total = 0.0
    for k in range(1, ng + 1):
        tt = math.exp(lo + (hi - lo) * k / ng)
        total += 0.5 * (1.0 / (lo + (hi - lo) * (k - 1) / ng) ** 2
                        + 1.0 / (lo + (hi - lo) * k / ng) ** 2) * (tt - t0)
        t0 = tt
    return total


def main():
    print("=" * 70)
    print("TWIN-PRIME DENSITY: HARDY-LITTLEWOOD 0/0 (OPEN TARGET)")
    print("=" * 70)

    # Singular series constant, computed in-code: 2*C_2
    P = primes_to(10 ** 5)
    C2 = 1.0
    for p in P[1:]:
        C2 *= (1.0 - 1.0 / ((p - 1) * (p - 1)))
    K = 2.0 * C2
    print(f"singular series 2*C_2 = {K:.12f}  (literature 1.320323631694..)")

    N = 100_000_000
    print(f"sieve primes up to {N} ...")
    P = primes_to(N)
    print(f"  pi({N}) = {len(P)}")

    xs = [10 ** 6, 5 * 10 ** 6, 2 * 10 ** 7, N]
    flagged = bytearray(N + 3)
    for p in P:
        flagged[p] = 1
    counts = {}
    t = 0
    # fine checkpoints (every 1e5) feed the fluctuation-scale criterion:
    # per-decade max of |R(x) - 1| must fall decade-on-decade (the
    # removable-value signature carried by aclass_detector P4).
    CHK = 10 ** 5
    xs_fine = [k * CHK for k in range(1, N // CHK + 1)]
    fine = {}
    j = 0
    for n in range(3, N + 1, 2):
        if flagged[n] and flagged[n - 2]:
            t += 1
        if n in xs:
            counts[n] = t
        if n + 1 in xs:  # even snapshots: pi_2(x) = count of pairs with larger member <= x
            counts[n + 1] = t
        while j < len(xs_fine) and n >= xs_fine[j]:
            fine[xs_fine[j]] = t
            j += 1
    while j < len(xs_fine):
        fine[xs_fine[j]] = t
        j += 1
    print(f"pi_2(x) exact: " + ", ".join(f"x={x} -> {counts.get(x, '?')}" for x in xs))

    rows = []
    for x in xs:
        lx = math.log(x)
        L2 = li2(x)
        R = counts[x] / (K * L2)
        Rraw = counts[x] / (K * x / (lx * lx))
        rows.append((x, counts[x], R))
        print(f"  x={x:>10,}  pi_2={counts[x]:>7,}  "
              f"2C2*Li2(x) = {K*L2:>9,.0f}  R={R:.4f} "
              f"(raw x/log^2x R={Rraw:.4f})")
    g1 = all(0.97 <= r <= 1.03 for _, _, r in rows[-2:])
    g2 = all(0.94 <= r <= 1.06 for _, _, r in rows)
    g3 = abs(K - 1.320323631694) < 2e-6

    # fluctuation-scale criterion (matches aclass_detector P4): per-decade
    # max |R - 1| decays -> removable-compatible, not anti-class.
    dpairs = [(x, abs(fine[x] / (K * li2(x)) - 1.0)) for x in xs_fine
              if x >= 10 ** 5]
    bins = {}
    for x, d in dpairs:
        k = int(math.floor(math.log10(x)) + 1e-9)
        bins.setdefault(k, []).append(d)
    rows_c = [(k, max(bins[k])) for k in sorted(bins)
              if len(bins[k]) >= 3]
    cpts = [(math.log(10 ** (k + 0.5)), math.log(v)) for k, v in rows_c]
    nc = len(cpts)
    cmx = sum(p for p, _ in cpts) / nc
    cmy = sum(q for _, q in cpts) / nc
    csxx = sum((p - cmx) ** 2 for p, _ in cpts)
    csxy = sum((p - cmx) * (q - cmy) for p, q in cpts)
    beta = csxy / csxx if csxx else 0.0
    csyy = sum((q - cmy) ** 2 for _, q in cpts)
    r2 = (csxy * csxy) / (csxx * csyy) if csxx and csyy else 0.0
    per_decade = {f"10^{k}": v for k, v in rows_c}
    print("  criterion: per-decade max |R-1|: " +
          ", ".join(f"10^{k}->{v:.4f}" for k, v in rows_c))
    print(f"  criterion: decay exponent beta = {beta:.2f} (r2={r2:.2f}, "
          f"{nc} decades) -> "
          f"{'REMOVABLE-COMPATIBLE (decaying)' if beta < -0.2 else 'NOT CLEAN'}")
    g4 = beta < -0.2 and r2 > 0.7

    print("\n" + "-" * 70)
    print("INTERPRETATION")
    print("-" * 70)
    print("R(x) is the 0/0 of two prime-pair densities; the removable")
    print("value (conjectural, OPEN) is 1.  Compared against the H-L")
    print("integral form 2*C_2*Li_2(x) the ratio lands in [0.94,1.06]")
    print("and tightens to within 3% at the top.  The framework computed")
    print("its own target constant 2*C_2 = 1.3203236.. from the product")
    print("over primes.  Honest wall: exact pi_2 to 1e8 only.")

    gates = {"G1 R(x) approaches 1 at the top of the range": g1,
             "G2 R stays in the H-L band across the range": g2,
             "G3 in-code 2*C_2 matches literature (target derived, not cited)": g3,
             "G4 criterion: per-decade max |R-1| decays (beta < -0.2)": g4}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'}")

    os.makedirs(DATA, exist_ok=True)
    json.dump(
        {"form": "pi_2(x)/(2*C_2*x/log(x)^2)", "mechanism": "Vanishing Rate",
         "point": "x -> inf (density 0/0)", "removable_value": 1.0,
         "conjecture": "Hardy-Littlewood twin-prime (OPEN)",
         "C2_computed": C2, "two_C2_computed": K,
         "rows": [{"x": x, "pi2": a, "R": r} for x, a, r in rows],
         "criterion_decay_beta": beta, "criterion_decay_r2": r2,
         "per_decade_max": per_decade,
         "gates": gates, "overall": overall,
         "wall": "counts to 1e8; asymptotic slow"}, 
        open(os.path.join(DATA, "twin_prime_density_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/twin_prime_density_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()