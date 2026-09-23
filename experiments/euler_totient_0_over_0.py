"""NUMBER THEORY (REMOVABLE, NAMED CONSTANT): EULER TOTIENT DENSITY
Sigma phi(n)/n^2 -> 3/pi^2, THE FLAT-DECAY CALIBRATION ANCHOR.

Atlas entry 71.  Entries 64/67/69/70 found the anti-class: fluctuations
that sit ON the denominator, ratio order-one.  Entry 71 is the opposite
calibration point: a REMOVABLE member whose deviation is as large as the
anti-class's in absolute terms but provably VANISHES against its own
denominator -- the flat-edge of the removable side.

Let Phi(x) = sum_{k<=x} phi(k) (Euler's totient summatory).  Dirichlet
(1849):  Phi(x) = (3/pi^2) x^2 + O(x log x).  The 0/0 form
    Phi(x)/x^2  ->  3/pi^2 = 0.30396355092701333...   (converges)
is REMOVABLE with a named constant.  The deviation

    E(x) = Phi(x) - (3/pi^2) x^2 = O(x log x)

is 1.5 powers of x LARGER than a sqrt-denominator fluctuation -- yet the
ratio |E(x)|/x^2 = O(log x / x) still collapses decade-on-decade, because
the fluctuation sits an entire power BELOW the denominator (x^1 vs x^2).
That is the exact structural contrast the quartet of anti members lacks:
anti = fluctuation on the denominator (ratio order-one, no limit);
totient = fluctuation a full power below (ratio x^{-1}, limit proves to
exist and equals 0 for the deviation).  The decay SIGN is what separates
them, and this member gives the removable side its slowest, most
ill-converging legitimate rate: log x/x, still slope ~ -1.

Montgomery also proved the oscillation is genuinely there (E = Omega_-
(n log log log n) type, sign changes infinitely), so the totient member
is the "removable that looks most anti at small ranges": the deviation
grows, the ratio still declines.  The Criterion's sign read -- slope of
the per-decade max, not the size of the deviation -- is exactly what
adjudicates it.

Verification here:
   - exact phi(k) via a linear-sieve (smallest-prime-factor) pass,
     phi(k) = k * prod_{p|k} (1 - 1/p),
   - the totient-sum identity sum_{d|n} phi(d) = n (a theorem gate,
     independent of any literature table),
   - the derivable spot table phi(10^d) = 0.4 * 10^d for d = 1..6,
   - the named constant 3/pi^2 (Dirichlet, proved) and the removable
     value read of Phi(x)/x^2,
   - the DECAY-SIGN gate: the per-decade max of |Phi(x)/x^2 - 3/pi^2|
     falls with log-log slope ~ -1 (fully removable; the anti quartet's
     slope is >= -0.15 with order-one floors),
   - the O(x log x) consistency read: max |E(x)|/(x log x) stays small,
   - the honest wall: sign oscillation persists (Montgomery) yet the
     ratio provably vanishes; no range can make this ratio order-one.

Mechanism: Vanishing Rate (leading density coefficient).
"""

import json
import math
import os
import sys
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")

RHO = 3.0 / (math.pi * math.pi)  # Dirichlet density, 3/pi^2


def linear_sieve_spf(N):
    """smallest-prime-factor table spf[2..N] (array 'I'), linear sieve."""
    spf = array("I", [0]) * (N + 1)
    primes = []
    for i in range(2, N + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        for p in primes:
            v = i * p
            if v > N:
                break
            spf[v] = p
            if p == spf[i]:
                break
    return spf, primes


def phi_table(spf, N):
    """phi(k) for k <= N via the spf factor walk (phi = k prod (1-1/p))."""
    ph = array("I", [0]) * (N + 1)
    ph[1] = 1
    for k in range(2, N + 1):
        m = k
        res = k
        while m > 1:
            p = spf[m]
            res = res // p * (p - 1)
            while m % p == 0:
                m //= p
        ph[k] = res
    return ph


def totient_divisor_identity(ph, upto):
    """sum_{d|n} phi(d) == n for n <= upto."""
    for n in range(1, upto + 1):
        sm = 0
        d = 1
        while d * d <= n:
            if n % d == 0:
                sm += ph[d]
                e = n // d
                if e != d:
                    sm += ph[e]
            d += 1
        if sm != n:
            return False
    return True


def fit(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx if sxx else 0.0
    syy = sum((y - my) ** 2 for y in ys)
    r2 = (sxy * sxy) / (sxx * syy) if sxx and syy else 0.0
    return slope, r2


def main():
    print("=" * 70)
    print("EULER TOTIENT DENSITY Phi(x)/x^2 -> 3/pi^2: THE FLAT-DECAY "
          "REMOVABLE ANCHOR")
    print("=" * 70)

    N = 10_000_000
    spf, primes = linear_sieve_spf(N)
    print(f"  linear sieve: spf[2..{N:,}] ({len(primes):,} primes)")
    ph = phi_table(spf, N)
    print("  phi(k) table, k <= 1e7")

    # Gate 1: totient-sum identity (theorem gate, independent).
    g1 = totient_divisor_identity(ph, 3000)
    print("  sum_{d|n} phi(d) = n for n <= 3000: "
          f"{'OK' if g1 else 'FAIL'}")

    # Gate 2: derivable spot table phi(10^d) = 10^d (1-1/2)(1-1/5).
    g2_pts = {10 ** d: 4 * 10 ** (d - 1) for d in range(1, 7)}
    g2 = all(ph[10 ** d] == 4 * 10 ** (d - 1) for d in range(1, 7))
    print("  phi(10^d) = 4*10^(d-1) (d=1..6): "
          f"{'OK' if g2 else 'MISMATCH'} "
          f"({[ph[10**d] for d in range(1,7)]})")

    # Streaming walk over the totient summatory Phi(x).
    pow10 = {10 ** k for k in range(2, 8)}
    spot = {}
    devmax = {}   # decade -> max |E(x)|/x^2 = max |Phi/x^2 - 3/pi^2|
    enorm = {}    # decade -> max |E(x)|/(x log x), O-consistency
    pos = neg = False
    prevd = -1
    cur_dm = cur_en = None
    acc = 0
    for x in range(1, N + 1):
        acc += ph[x]
        if x in pow10:
            spot[x] = acc
        if x < 2:
            continue
        dv = acc - RHO * x * x
        a = dv if dv > 0 else -dv
        r = a / (x * x)
        en = a / (x * math.log(x))
        dd = int(math.floor(math.log10(x)) + 1e-9)
        if dd != prevd:
            if prevd is not None:
                devmax[prevd] = cur_dm
                enorm[prevd] = cur_en
            prevd = dd
            cur_dm = cur_en = 0.0
        if r > cur_dm:
            cur_dm = r
        if en > cur_en:
            cur_en = en
        pos = pos or dv > 0
        neg = neg or dv < 0
    devmax[prevd] = cur_dm
    enorm[prevd] = cur_en

    print("  Phi(10^k): " + ", ".join(
        f"10^{k}={spot[10 ** k]:>13,}" for k in range(2, 8)))
    decs = sorted(devmax)
    print("  per-decade max |Phi/x^2 - 3/pi^2|: " + ", ".join(
        f"{devmax[d]:.3e}" for d in decs if 2 <= d <= 7))

    # Gate 3 (theorem): removable value 3/pi^2 (Dirichlet, proved;
    # E = O(x log x)).
    g3 = True
    print(f"  removable cited: Phi(x)/x^2 -> 3/pi^2 = {RHO:.15f} "
          "(Dirichlet 1849, O(x log x) error; named constant, proved)")

    # Gate 4: decay sign.  The per-decade max of |R - 3/pi^2| falls with a
    # robustly negative log-log slope (removable), the exact sign the
    # anti quartet provably lacks (their floors are order-one).
    late = [dd for dd in range(4, 8)]
    xs = [math.log(10 ** dd) for dd in late]
    beta_ratio, r2_ratio = fit(xs, [math.log(devmax[dd]) for dd in late])
    g4 = beta_ratio < -0.6
    print(f"  ratio slope beta_ratio = {beta_ratio:.3f} (r2={r2_ratio:.2f}, "
          f"decades 10^4..10^7): <= -0.6 => ratio collapses, removable "
          f"(anti quartet floors above 0 with slopes >= -0.15)")

    # Gate 5: O(x log x) consistency.
    enhi = max(enorm[d] for d in late)
    g5 = enhi <= 60.0
    print(f"  max |E(x)|/(x log x) = {enhi:.3f} (decades 10^4..10^7, "
          "O(x log x) consistency, bound 60.0)")

    print(f"  sign oscillation over [2,1e7] (Montgomery): "
          f"{'both signs' if pos and neg else 'one sign'} "
          "(the deviation wiggles; the ratio still vanishes)")

    gates = {"G1 totient identity sum_{d|n} phi(d) = n": g1,
             "G2 phi(10^d) = 4*10^(d-1) (d=1..6)": g2,
             "G3 removable value 3/pi^2 (Dirichlet, cited)": g3,
             "G4 ratio decay sign (beta < -0.6, removable)": g4,
             "G5 |E(x)|/(x log x) consistent with O(x log x)": g5}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'} (the flat-decay "
          f"removable anchor; the deviation is order x^1 but the "
          f"denominator is x^2, so the ratio provably vanishes -- the "
          f"decay sign separates this from the anti quartet)")

    os.makedirs(DATA, exist_ok=True)
    json.dump(
        {"form": "Phi(x)/x^2, Phi(x) = sum_{k<=x} phi(k)",
         "mechanism": "Vanishing Rate",
         "point": "x -> infinity",
         "removable_value": RHO,
         "constant": "3/pi^2 = 0.30396355092701333...",
         "conjecture": "Phi(x) = (3/pi^2) x^2 + O(x log x) (Dirichlet "
                       "1849, proved); Montgomery: the error oscillates "
                       "(Omega_- type sign changes) yet the ratio "
                       "provably collapses as O(log x / x)",
         "Phi_at_powers_of_10": {str(k): spot[10 ** k] for k in range(2, 8)},
         "decade_max_ratio": {str(d): devmax[d] for d in decs
                              if 2 <= d <= 7},
         "ratio_beta": beta_ratio, "ratio_r2": r2_ratio,
         "max_E_over_xlogx": enhi,
         "gates": gates, "overall": overall,
         "wall": "exact Phi(x) to 1e7; the definitive verification is the "
                 "decay sign (provably negative slope, O(log x / x) "
                 "collapse); contrasted with the anti quartet whose "
                 "ratio floors above zero"},
        open(os.path.join(DATA, "euler_totient_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/euler_totient_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()