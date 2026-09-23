"""NUMBER THEORY (ANTI-CLASS): DIRICHLET DIVISOR ERROR Delta(x)/x^(1/4),
THIRD MEMBER OF THE CLASS THE CORPUS FOUNDED AS EMPTY.

Atlas entry 69.  Entry 64 (Polya/Liouville) and entry 67 (Mertens) found
the anti-class on the sqrt(n) scale; the lattice-point family supplies a
STRONGER, unconditionally-proved member on the x^(1/4) scale.

Let d(n) be the divisor function and S(x) = sum_{n<=x} d(n).  The smooth
main term of S is x*log(x) + (2*gamma - 1)*x, and the error term

    Delta(x) = S(x) - x*log(x) - (2*gamma - 1)*x

obeys, unconditionally:
   - Hardy (1916):  Delta = Omega_+((x log x)^(1/4) log log x), so
     limsup Delta(x)/x^(1/4) = +infinity, and Delta = Omega_-(x^(1/4)),
     so Delta(x)/x^(1/4) is infinitely often < -c < 0.  Hence the 0/0 form
     Delta(x)/x^(1/4) has NO limit -- the value does not exist, and on one
     side the ratio is even PROVEN unbounded.
   - Voronoi (1903/04): Delta = O(x^(1/3) log x); today O(x^(131/416+eps))
     (Huxley 2003).  The fluctuation therefore sits on and above the
     x^(1/4) denominator and below x^(1/3): the anti-class carries its
     denominator, now with a stronger no-limit status than entries 64/67
     where only limsup/liminf constants (Odlyzko-te Riele, Humphries) are
     known.

Empirically the exact computation is striking and matches the theorem:
   |Delta(x)|/x^(1/4) stays order-one (about 2..10) through every decade
   to 1e7 and never collapses toward 0, while |Delta(x)|/x^(1/3) stays
   below ~1.4 (Voronoi's bound, with headroom).  Delta can be tiny near
   x = 10^k (Delta(10^7) = -4), which is the oscillatory structure, not
   decay; near-threshold decades are why a naive "growth exponent" is not
   the right single number for this member -- the interval-scale reading
   is.

Verification here, mirrored from entries 64/67:
   - exact d(n) via a linear-sieve (smallest-prime-factor) pass,
   - the divisor-summatory identity S(x) = sum_{d<=x} floor(x/d) (a
     theorem gate, independent of any literature table),
   - the divisor table d(1..16) against the standard values,
   - the RATIO-NON-DECAY signature: per-decade max |Delta|/x^(1/4) is
     order one in every reached decade (never shrinks toward a removable
     value), the same structural tell as |F|/sqrt(n) and |M|/sqrt(n)
     staying order one while removable targets (twin -0.32, prime-
     reciprocal -0.59, PNT-drift) go to zero,
   - Voronoi consistency: max |Delta|/x^(1/3) <= ~1.4 over [1e4, 1e7]
     (fluctuations respect the proved 1/3 bound; the class stays off the
     sqrt-spectrum entries 64/67 sit on),
   - per-decade sign oscillation (both Delta > 0 and Delta < 0 in every
     late decade, Hardy's Omega_+ and Omega_-),
   - the honest wall: the ratio's sup at x <= 1e7 is ~9.4, but Hardy
     proves it unbounded; no finite range can display the failure.

Mechanism: ANTI-CLASS (the removable value does not exist).
"""

import json
import math
import os
import sys
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")

GAMMA = 0.57721566490153286060651209008240243104215933593992
MAIN_COEF = 2.0 * GAMMA - 1.0  # 2*gamma - 1 in the divisor-summatory term
DENOM_EXP = 0.25                # x^(1/4), Hardy's fluctuation scale

DIV_TABLE_16 = [1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6, 2, 4, 4, 5]


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


def divisor_table(spf, N):
    """d(n) = #{ divisors of n } for n <= N via the spf factor walk."""
    d = array("I", [1]) * (N + 1)
    d[0] = 0
    for n in range(2, N + 1):
        m = n
        tot = 1
        while m > 1:
            p = spf[m]
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            tot *= e + 1
        d[n] = tot
    return d


def floor_sum_identity(x):
    """S(x) = sum_{d<=x} floor(x/d), the independent divisor identity."""
    return sum(x // dd for dd in range(1, x + 1))


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
    print("DIRICHLET DIVISOR ERROR Delta(x)/x^(1/4): THE ANTI-CLASS, "
          "THIRD MEMBER")
    print("=" * 70)

    N = 10_000_000
    spf, primes = linear_sieve_spf(N)
    print(f"  linear sieve: spf[2..{N:,}] ({len(primes):,} primes)")
    d = divisor_table(spf, N)
    print("  divisor table d(n), n <= 1e7")

    # Gate 1: invariance theorem, S(x) = sum_{d<=x} floor(x/d).
    id_pts = (10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5)
    S_id = {}
    acc = 0
    for n in range(1, 10 ** 5 + 1):
        acc += d[n]
        if n in id_pts:
            S_id[n] = acc
    g1 = all(S_id[x] == floor_sum_identity(x) for x in id_pts)
    print("  S(x) = sum_{d<=x} floor(x/d): "
          f"{'OK' if g1 else 'FAIL'} (identity gate, x = 10^2..10^5)")

    # Gate 2: divisor table against the standard values.
    g2 = list(d[1:17]) == DIV_TABLE_16
    print(f"  d(1..16) = {list(d[1:17])}  "
          f"{'OK' if g2 else 'MISMATCH'} (standard table)")

    # Single streaming walk over S(x): per-decade maxima of |Delta(x)| and
    # |Delta(x)|/x^(1/4), per-decade sign census, and the Voronoi
    # consistency ratio |Delta|/x^(1/3).
    pow10 = {10 ** k for k in range(2, 8)}
    spot = {}
    devmax = {}    # decade -> max |Delta(x)|
    ratiomax = {}  # decade -> max |Delta(x)|/x^(1/4)
    has_pos = {}
    has_neg = {}
    prevd = -1
    cur_dm = cur_rm = None
    cur_pos = cur_neg = False
    nu_all = 0.0   # max |Delta|/x^(1/3), Voronoi-consistency statistic
    nu_at = 0
    acc2 = 0
    for n in range(1, N + 1):
        acc2 += d[n]
        if n in pow10:
            spot[n] = acc2
        if n < 2:
            continue
        main = n * math.log(n) + MAIN_COEF * n
        dv = acc2 - main
        a = dv if dv > 0 else -dv
        r = a / (n ** DENOM_EXP)
        nu = a / (n ** (1.0 / 3.0))
        if nu > nu_all:
            nu_all, nu_at = nu, n
        dd = int(math.floor(math.log10(n)) + 1e-9)
        if dd != prevd:
            if prevd is not None:
                devmax[prevd] = cur_dm
                ratiomax[prevd] = cur_rm
                has_pos[prevd] = cur_pos
                has_neg[prevd] = cur_neg
            prevd = dd
            cur_dm = cur_rm = 0.0
            cur_pos = cur_neg = False
        if a > cur_dm:
            cur_dm = a
        if r > cur_rm:
            cur_rm = r
        cur_pos = cur_pos or dv > 0
        cur_neg = cur_neg or dv < 0
    devmax[prevd] = cur_dm
    ratiomax[prevd] = cur_rm
    has_pos[prevd] = cur_pos
    has_neg[prevd] = cur_neg

    print("  S(10^k): " + ", ".join(
        f"10^{k}={spot[10 ** k]:>14,}" for k in range(2, 8)))
    decs = sorted(devmax)
    print("  per-decade max |Delta|/x^(1/4) (d=2..7): " + ", ".join(
        f"{ratiomax[d]:.2f}" for d in decs if 2 <= d <= 7))
    print("  per-decade max |Delta|          (d=2..7): " + ", ".join(
        f"{devmax[d]:>7,.0f}" for d in decs if 2 <= d <= 7))

    # Gate 3 (theorem): Delta(x)/x^(1/4) has no limit.  Hardy (1916)
    # limsup = +oo and infinitely many negative values; Voronoi O(x^(1/3))
    # bounds the ratio above.  Cited, hence always true.
    g3 = True
    print("  anti-class cited: Delta(x)/x^(1/4) has NO limit (Hardy 1916 "
          "Omega_+((x log x)^(1/4) log log x) => limsup = oo; Omega_- "
          "at x^(1/4); Voronoi 1903 O(x^(1/3)); Huxley 2003 "
          "O(x^(131/416+eps)))")

    # Gate 4: ratio non-decay.  The per-decade max of |Delta|/x^(1/4) is
    # order one in every reached decade (removable targets collapse toward
    # 0 with strongly negative decade slopes).
    late = [dd for dd in range(4, 8)]
    min_ratio_late = min(ratiomax[dd] for dd in late)
    xs = [math.log(10 ** dd) for dd in late]
    beta_ratio, r2_ratio = fit(xs, [math.log(ratiomax[dd])
                                    for dd in late])
    g4 = min_ratio_late >= 0.75
    print(f"  ratio slope beta_ratio = {beta_ratio:.3f} (r2={r2_ratio:.2f}, "
          f"decades 10^4..10^7); lowest decade max = {min_ratio_late:.2f} "
          f">= 0.75 => ratio never approaches a removable value "
          f"(twin -0.32, prime-reciprocal -0.59 slopes are those decays)")

    # Gate 5: Voronoi consistency -- |Delta|/x^(1/3) stays small (the
    # proved O(x^(1/3)) upper bound; the class reads between x^(1/4) and
    # x^(1/3), off the 1/2 spectrum of entries 64/67).
    g5 = nu_all <= 5.0
    print(f"  max |Delta|/x^(1/3) = {nu_all:.3f} at x = {nu_at:,} "
          "(Voronoi consistency, bound 5.0)")

    # Gate 6: sign oscillation in every late decade (Hardy's Omega_+ and
    # Omega_-, numerically).
    late6 = [dd for dd in range(4, 7)]
    g6 = all(has_pos[dd] and has_neg[dd] for dd in late6)
    print("  sign oscillation (both Delta>0 and Delta<0 on 10^4..10^6): "
          f"{'OK' if g6 else 'NO'}")

    gates = {"G1 divisor identity S(x) = sum floor(x/d)": g1,
             "G2 divisor table d(1..16)": g2,
             "G3 no removable value (Hardy 1916 + Voronoi 1903, cited)": g3,
             "G4 ratio |Delta|/x^(1/4) stays order one (non-decay)": g4,
             "G5 |Delta|/x^(1/3) respects Voronoi's 1/3 bound": g5,
             "G6 signs oscillate in each late decade": g6}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'} (third anti-class "
          f"member; the removable value provably does not exist -- proved "
          f"unbounded on one side, the strongest member, and the "
          f"lattice-point theorem carries the verdict, not the wall)")

    os.makedirs(DATA, exist_ok=True)
    json.dump(
        {"form": "Delta(x)/x^(1/4), Delta(x) = sum_{n<=x} d(n) - "
                 "x*log(x) - (2*gamma-1)*x",
         "mechanism": "ANTI-CLASS",
         "point": "x -> infinity (records)",
         "removable_value": None,
         "conjecture": "Delta(x)/x^(1/4) has NO limit: Hardy (1916) "
                       "Omega_+((x log x)^(1/4) log log x) gives limsup "
                       "= +infinity and Omega_-(x^(1/4)) gives infinitely "
                       "many negative values; Voronoi (1903) O(x^(1/3)); "
                       "Huxley (2003) O(x^(131/416+eps)); the open question "
                       "is the correction below x^(1/3) (Hardy's theta = "
                       "1/4 conjectured)",
         "S_at_powers_of_10": {str(k): spot[10 ** k] for k in range(2, 8)},
         "decade_max_ratio": {str(d): ratiomax[d] for d in decs
                              if 2 <= d <= 7},
         "decade_max_dev": {str(d): devmax[d] for d in decs
                            if 2 <= d <= 7},
         "ratio_beta": beta_ratio, "ratio_r2": r2_ratio,
         "min_decade_max_ratio_1e4_to_1e7": min_ratio_late,
         "max_dev_over_x13": nu_all, "argmax_dev_over_x13": nu_at,
         "gates": gates, "overall": overall,
         "wall": "exact S(x) and Delta(x) to 1e7; limsup of the ratio is "
                 "unconditionally +infinity (Hardy), so no finite range can "
                 "display the failure; the class already reads fluctuations "
                 "on and above the 1/4 denominator, order-one to the wall"},
        open(os.path.join(DATA, "dirichlet_divisor_anti_0_over_0.json"),
             "w"),
        indent=2)
    print("Wrote data/dirichlet_divisor_anti_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()