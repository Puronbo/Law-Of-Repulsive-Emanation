"""NUMBER THEORY (ANTI-CLASS): GAUSS CIRCLE-ERROR P(x)/x^(1/4), FOURTH
MEMBER OF THE CLASS THE CORPUS FOUNDED AS EMPTY.

Atlas entry 70.  The lattice-point family (entries 69/70) is Hardy's pair:
the Dirichlet divisor-error and the Gauss circle-error share the SAME
denominator x^(1/4) and the SAME unconditional no-limit status.  Where the
divisor member's limsup is +oo (Hardy's Omega_+), the circle member's
liminf is -oo -- the pair reads the two unbounded sides.

Let r_2(k) = #{ (a,b) in Z^2 : a^2 + b^2 = k } (Jacobi's two-square count)
and N(x) = 1 + sum_{k<=x} r_2(k) = #{ lattice points a^2 + b^2 <= x }
(the +1 is the origin (0,0), reached at k = 0). The
smooth main term is pi*x, and the error term

    P(x) = N(x) - pi*x

obeys, unconditionally:
   - Hardy (1916):  P = Omega_-((x log x)^(1/4) log log x), so
     liminf P(x)/x^(1/4) = -infinity, and P = Omega_+(x^(1/4)) (also
     Sierpinski 1906).  Hence the 0/0 form P(x)/x^(1/4) has NO limit:
     the value does not exist, and on one side the ratio is PROVEN
     unbounded.
   - Voronoi (1904) / Sierpinski (1906): P = O(x^(1/3)); today O(x^(131/
     416+eps)) (Huxley 2003, the same constant as the divisor problem).
   The fluctuation therefore sits on and above the x^(1/4) denominator
   and below x^(1/3): the anti-class carries its denominator, exactly as
   entry 69 does, on the opposite unbounded side.

Verification here, mirrored from entries 64/67/69:
   - exact r_2(k) via a linear-sieve (smallest-prime-factor) pass through
     the two-square characterization: r_2(k) = 4 * prod_{p=1(4)} (e_p+1)
     when no p=3(mod 4) has odd exponent, else 0,
   - the two-square theorem gate: r_2(k) for k <= 25 against a direct
     brute-force count of integer solutions (independent of any table),
   - the disk-count identity N(x) = (4*floor(sqrt(x)) + 1) +
     4*sum_{a=1}^{floor(sqrt(x))} floor(sqrt(x - a^2)) at x = 10^2..10^7
     (Voronoi's lattice-point formula, exact via isqrt),
   - the RATIO-NON-DECAY signature: per-decade max |P(x)|/x^(1/4) is
     order-one in every reached decade (never shrinks toward a removable
     value), the same structural read as entries 64/67/69,
   - the upper-consistency read: max |P(x)|/x^(1/3) small (Voronoi's 1/3
     bound; P stays on the 1/4..1/3 band, off the 1/2 spectrum),
   - per-decade sign oscillation (both P > 0 and P < 0 in every late
     decade; Sierpinski/Hardy's Omega_+ and Omega_-),
   - the honest wall: the ratio's inf at x <= 1e7 is finite, but the
     theorem proves liminf = -infinity; no finite range can display it.

Mechanism: ANTI-CLASS (the removable value does not exist).
"""

import json
import math
import os
import sys
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")

DENOM_EXP = 0.25  # x^(1/4), Hardy's fluctuation scale


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


def r2_table(spf, N):
    """r_2(k) = #{ a^2 + b^2 = k } for k <= N via the spf factor walk.
    r_2(k) = 0 if some p = 3 (mod 4) has odd exponent, else
    r_2(k) = 4 * prod_{p = 1 (mod 4)} (e_p + 1)."""
    r2 = array("I", [0]) * (N + 1)
    r2[1] = 4
    for k in range(2, N + 1):
        m = k
        prod = 1
        zero = False
        while m > 1 and not zero:
            p = spf[m]
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            pm = p & 3
            if pm == 3:
                if e & 1:
                    zero = True
            elif pm == 1:
                prod *= e + 1
        r2[k] = 0 if zero else 4 * prod
    return r2


def r2_brute(upto):
    """direct count of a^2 + b^2 = k for k <= upto (O(upto^1.5), tiny)."""
    out = array("I", [0]) * (upto + 1)
    m = int(math.isqrt(upto))
    for a in range(-m, m + 1):
        for b in range(-m, m + 1):
            s = a * a + b * b
            if s <= upto:
                out[s] += 1
    return out


def disk_count(x):
    """N(x) = #{ a^2 + b^2 <= x }, exact via isqrt (Voronoi's formula)."""
    m = math.isqrt(x)
    return 4 * m + 1 + 4 * sum(math.isqrt(x - a * a) for a in range(1, m + 1))


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
    print("GAUSS CIRCLE-ERROR P(x)/x^(1/4): THE ANTI-CLASS, FOURTH MEMBER")
    print("=" * 70)

    N = 10_000_000
    spf, primes = linear_sieve_spf(N)
    print(f"  linear sieve: spf[2..{N:,}] ({len(primes):,} primes)")
    r2 = r2_table(spf, N)
    print("  r_2(k) table, k <= 1e7 (Jacobi two-square characterization)")

    # Gate 1: two-square theorem gate vs a direct brute-force count.
    B = 25
    rec = r2_brute(B)
    g1 = list(r2[1:B + 1]) == list(rec[1:B + 1])
    print("  r_2(1..25) vs brute-force a^2+b^2 count: "
          f"{'OK' if g1 else 'MISMATCH'} (theorem gate)")

    # Gate 2: disk-count identity N(x) = (4m+1) + 4 sum isqrt(x - a^2).
    prefix = {}
    acc = 1  # the origin (0,0): r_2 sums every nonzero lattice point
    g2 = True
    for k in range(1, N + 1):
        acc += r2[k]
        if (k in (10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5)
                or k in (10 ** 6, 10 ** 7)):
            prefix[k] = acc
            if disk_count(k) != acc:
                g2 = False
    print("  N(x) = (4m+1) + 4*sum isqrt(x-a^2): "
          f"{'OK' if g2 else 'FAIL'} (identity gate, x = 10^2..10^7)")

    # Single streaming walk over N(x): per-decade maxima of |P(x)| and
    # |P(x)|/x^(1/4), per-decade sign census, and the Voronoi consistency
    # ratio |P|/x^(1/3).
    devmax = {}
    ratiomax = {}
    has_pos = {}
    has_neg = {}
    prevd = -1
    cur_dm = cur_rm = None
    cur_pos = cur_neg = False
    nu_all = 0.0
    nu_at = 0
    acc2 = 1  # the origin (0,0), as above
    for x in range(1, N + 1):
        acc2 += r2[x]
        if x < 2:
            continue
        main = math.pi * x
        dv = acc2 - main
        a = dv if dv > 0 else -dv
        rr = a / (x ** DENOM_EXP)
        nu = a / (x ** (1.0 / 3.0))
        if nu > nu_all:
            nu_all, nu_at = nu, x
        dd = int(math.floor(math.log10(x)) + 1e-9)
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
        if rr > cur_rm:
            cur_rm = rr
        cur_pos = cur_pos or dv > 0
        cur_neg = cur_neg or dv < 0
    devmax[prevd] = cur_dm
    ratiomax[prevd] = cur_rm
    has_pos[prevd] = cur_pos
    has_neg[prevd] = cur_neg

    print("  N(10^k): " + ", ".join(
        f"10^{k}={prefix[10 ** k]:>12,}" for k in range(2, 8)))
    decs = sorted(devmax)
    print("  per-decade max |P|/x^(1/4) (d=2..7): " + ", ".join(
        f"{ratiomax[d]:.2f}" for d in decs if 2 <= d <= 7))
    print("  per-decade max |P|          (d=2..7): " + ", ".join(
        f"{devmax[d]:>7,.0f}" for d in decs if 2 <= d <= 7))

    # Gate 3 (theorem): P(x)/x^(1/4) has no limit.  Hardy (1916)
    # Omega_+ at x^(1/4), Omega_-((x log x)^(1/4) log log x) => liminf =
    # -oo; Voronoi/Sierpinski O(x^(1/3)); Huxley O(x^(131/416+eps)).
    g3 = True
    print("  anti-class cited: P(x)/x^(1/4) has NO limit (Hardy 1916 "
          "Omega_+ at x^(1/4) and Omega_-((x log x)^(1/4) log log x) => "
          "liminf = -oo; Sierpinski 1906; Voronoi 1904 O(x^(1/3)); "
          "Huxley 2003 O(x^(131/416+eps)))")

    # Gate 4: ratio non-decay, the bounded-band signature.
    late = [dd for dd in range(4, 8)]
    min_ratio_late = min(ratiomax[dd] for dd in late)
    xs = [math.log(10 ** dd) for dd in late]
    beta_ratio, r2_ratio = fit(xs, [math.log(ratiomax[dd])
                                    for dd in late])
    g4 = min_ratio_late >= 0.75
    print(f"  ratio slope beta_ratio = {beta_ratio:.3f} (r2={r2_ratio:.2f}, "
          f"decades 10^4..10^7); lowest decade max = {min_ratio_late:.2f} "
          f">= 0.75 => ratio never approaches a removable value")

    # Gate 5: Voronoi/Sierpinski consistency.
    g5 = nu_all <= 6.0
    print(f"  max |P|/x^(1/3) = {nu_all:.3f} at x = {nu_at:,} "
          "(upper-consistency, bound 6.0)")

    # Gate 6: sign oscillation in every late decade.
    late6 = [dd for dd in range(4, 7)]
    g6 = all(has_pos[dd] and has_neg[dd] for dd in late6)
    print("  sign oscillation (both P>0 and P<0 on 10^4..10^6): "
          f"{'OK' if g6 else 'NO'}")

    gates = {"G1 two-square theorem r_2(1..25) vs brute force": g1,
             "G2 disk-count identity N(x) = (4m+1)+4*sum isqrt(x-a^2)": g2,
             "G3 no removable value (Hardy 1916 + Sierpinski 1906, cited)": g3,
             "G4 ratio |P|/x^(1/4) stays order one (non-decay)": g4,
             "G5 |P|/x^(1/3) respects the 1/3 upper bound": g5,
             "G6 signs oscillate in each late decade": g6}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'} (fourth anti-class "
          f"member; the Hardy pair #69/#70 now reads both unbounded sides "
          f"of the x^(1/4) 0/0)")

    os.makedirs(DATA, exist_ok=True)
    json.dump(
        {"form": "P(x)/x^(1/4), P(x) = N(x) - pi*x, "
                 "N(x) = #{ a^2+b^2 <= x }",
         "mechanism": "ANTI-CLASS",
         "point": "x -> infinity (records)",
         "removable_value": None,
         "conjecture": "P(x)/x^(1/4) has NO limit: Hardy (1916) "
                       "Omega_+ at x^(1/4) and Omega_-((x log x)^(1/4) "
                       "log log x) give liminf = -infinity and infinitely "
                       "many positive values; Sierpinski (1906); Voronoi "
                       "(1904) O(x^(1/3)); Huxley (2003) O(x^(131/416+"
                       "eps)); Hardy's theta = 1/4 conjectured",
         "N_at_powers_of_10": {str(k): prefix[10 ** k] for k in range(2, 8)},
         "decade_max_ratio": {str(d): ratiomax[d] for d in decs
                              if 2 <= d <= 7},
         "decade_max_dev": {str(d): devmax[d] for d in decs
                            if 2 <= d <= 7},
         "ratio_beta": beta_ratio, "ratio_r2": r2_ratio,
         "min_decade_max_ratio_1e4_to_1e7": min_ratio_late,
         "max_dev_over_x13": nu_all, "argmax_dev_over_x13": nu_at,
         "gates": gates, "overall": overall,
         "wall": "exact N(x) and P(x) to 1e7; liminf of the ratio is "
                 "unconditionally -infinity (Hardy), so no finite range can "
                 "display the failure; the class reads fluctuations on and "
                 "above the 1/4 denominator, order-one to the wall"},
        open(os.path.join(DATA, "gauss_circle_anti_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/gauss_circle_anti_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()