"""NUMBER THEORY (REMOVABLE, VALUE 0): FIXED-CHARACTER PARTIAL SUMS
S(x)/x^(1/2), THE BOUNDED-BOX CONTROL MEMBER.

Atlas entry 72.  Entries 64/67/69/70 form the anti quartet: fluctuation ON
the denominator, per-decade ratio order-one, no limit.  Entry 72 is the
manufactured CONTROL on the opposite pole of the same instrument: a
summatory function whose RAW DEVIATION oscillates in a bounded box forever
(yet is provably 0/0 with removable value 0).

Let chi be the fixed primitive quadratic character mod 7 (Legendre symbol,
period 7, residues {1,2,4} -> +1, {3,5,6} -> -1, 7 | n -> 0) and

    S(x) = sum_{n<=x} chi(n).

Because chi is periodic with mean zero over each period, the partial sums
are BOUNDED: |S(x)| <= ~7 for ALL x (Poya-Vinogradov, trivially).  Hence

    S(x)/x^(1/2)  ->  0    (converges; value 0)

is REMOVABLE, and the per-decade max of |S|/sqrt(x) falls with log-log
slope exactly ~ -1/2 (bounded numerator, sqrt(x) denominator) -- the
criterion's decay sign reads removable unambiguously in a case where the
raw oscillation is MAXIMAL in the sense of never settling down.

Why this member matters (the epistemics):
   - The anti quartet hinges on the ratio's decade trend, NEVER on the
     size or wildness of the raw deviation.  Entry 72 is the control that
     proves it: the deviation here is as unruly as an anti member's (a
     signed random walk in a box), yet the ratio provably collapses, and
     the criterion reads it correctly (slope ~ -0.5) while anti members
     floor above zero (slope >= -0.15).
   - Chebyshev-bias-type denominators (pi(x;4,3) - pi(x;4,1) ~
     1.79 sqrt(x)/log x) are the INTERMEDIATE case: numerator grows, but
     a power below sqrt(x); this member with a BOUNDED numerator proves
     the read is not confused by the box itself.
   - Paley (1932) showed the oscillatory power of characters is a
     CROSS-modulus phenomenon (max_chi sums Omega_+(sqrt(q) log log q)),
     a different 0/0 in q-space that no finite x-range display -- cited
     here as the honest wall.

Verification here:
   - the character axioms: complete multiplicativity chi(ab) = chi(a)
     chi(b) and the zero period-sum (theorem gates, from the definition),
   - the removable read: per-decade max |S(x)|/sqrt(x) with log-log slope
     ~ -0.5 (r2 ~ 1.0) -- the bounded-box sign,
   - the BOX gate: max|S(x)| over [1,1e7] is essentially its one-period
     value (the fluctuation never grows; ratio of late-decade max to the
     early-decade max <= 2),
   - the honest wall: |S(10^7)|/sqrt(10^7) <= 0.01, and the true limit 0
     is proven by the Poya-Vinogradov bound, not by the wall.

Mechanism: Probe (tests the identity S(x) = o(sqrt(x))).
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")

Q = 7
CHI = {1: 1, 2: 1, 3: -1, 4: 1, 5: -1, 6: -1, 0: 0}  # Legendre symbol mod 7


def chi(n):
    return CHI[n % Q]


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
    print("FIXED-CHARACTER PARTIAL SUMS S(x)/sqrt(x) -> 0: THE BOUNDED-BOX "
          "CONTROL")
    print("=" * 70)

    N = 10_000_000

    # Gate 1: character axioms (complete multiplicativity, zero period sum).
    g1 = (sum(chi(n) for n in range(1, Q + 1)) == 0 and
          all(chi(a * b) == chi(a) * chi(b)
              for a in range(1, 150) for b in range(1, 150)))
    print("  character Axioms: period-7 sum = 0 and chi(ab) = chi(a)chi(b) "
          f"(a,b <= 150): {'OK' if g1 else 'FAIL'}")

    # Single streaming walk over S(x).
    pow10 = {10 ** k for k in range(2, 8)}
    spot = {}
    ratiomax = {}   # decade -> max |S(x)|/sqrt(x)
    absmax = {}     # decade -> max |S(x)|
    prevd = -1
    cur_rm = cur_am = None
    early_max = 0.0   # max |S(x)| over [1, 100] (the one-period box)
    s = 0
    rec = {}
    for x in range(1, N + 1):
        s += chi(x)
        if x in pow10:
            spot[x] = s
        a = s if s > 0 else -s
        rr = a / math.sqrt(x)
        dd = int(math.floor(math.log10(x)) + 1e-9)
        if dd != prevd:
            if prevd is not None:
                ratiomax[prevd] = cur_rm
                absmax[prevd] = cur_am
            prevd = dd
            cur_rm = cur_am = 0.0
        if rr > cur_rm:
            cur_rm = rr
        if a > cur_am:
            cur_am = a
        if x <= 100 and a > early_max:
            early_max = a
    ratiomax[prevd] = cur_rm
    absmax[prevd] = cur_am

    # Gate 2: removable theorem, cited (Poya-Vinogradov bound; value 0).
    g2 = True
    print("  removable cited: |S(x)| <= c (Poya-Vinogradov, trivial at "
          "mod 7: periodic mean-zero), so S(x)/sqrt(x) -> 0 (value 0); "
          "Paley 1932 cross-modulus oscillations are a different 0/0 in "
          "q-space, cited as the honest wall")

    decs = sorted(ratiomax)
    print("  S(10^k): " + ", ".join(
        f"10^{k}={spot[10 ** k]:>3}" for k in range(2, 8)))
    print("  per-decade max |S|/sqrt(x): " + ", ".join(
        f"{ratiomax[d]:.3e}" for d in decs if 2 <= d <= 7))
    print("  per-decade max |S| (box):   " + ", ".join(
        f"{absmax[d]:>5,}" for d in decs if 2 <= d <= 7))

    # Gate 3: decay sign.  Bounded numerator over sqrt(x) denominator
    # gives slope ~ -0.5; anti members floor above 0 (slope >= -0.15).
    late = [dd for dd in range(4, 8)]
    xs = [math.log(10 ** dd) for dd in late]
    beta_ratio, r2_ratio = fit(xs, [math.log(ratiomax[dd]) for dd in late])
    g3 = beta_ratio < -0.3 and r2_ratio > 0.9
    print(f"  ratio slope beta_ratio = {beta_ratio:.3f} (r2 = "
          f"{r2_ratio:.3f}, decades 10^4..10^7): bounded box / sqrt(x) "
          f"gives ~ -0.5 by construction")

    # Gate 4: the box does not grow.  Late-decade max |S| vs the
    # one-period value: ratio <= 2 (raw oscillation genuinely bounded).
    late_am = max(absmax[dd] for dd in range(4, 8))
    box_ratio = late_am / early_max if early_max else 0.0
    g4 = box_ratio <= 2.0
    print(f"  box gate: max|S| over 10^4..10^7 = {late_am} vs one-period "
          f"max {early_max:.0f} (ratio {box_ratio:.2f} <= 2: the deviation "
          f"never grows)")

    # Gate 5: the read at the wall (proven limit 0, not the wall's doing).
    g5 = abs(spot[10 ** 7]) / math.sqrt(10 ** 7) <= 0.01
    print(f"  |S(10^7)|/sqrt(10^7) = "
          f"{abs(spot[10 ** 7]) / math.sqrt(10 ** 7):.2e} <= 0.01 "
          "(the decay read at the wall)")

    gates = {"G1 character axioms (period sum, multiplicativity)": g1,
             "G2 removable 0 (Poya-Vinogradov, cited)": g2,
             "G3 decay sign (beta < -0.3, r2 > 0.9)": g3,
             "G4 bounded box (late/early max |S| <= 2)": g4,
             "G5 ratio below 0.01 at the wall": g5}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'} (the bounded-box "
          f"control: raw oscillation maximal in the never-settling sense, "
          f"ratio provably collapses -- the decay sign, and only the "
          f"decay sign, separates this from the anti quartet)")

    os.makedirs(DATA, exist_ok=True)
    json.dump(
        {"form": "S(x)/x^(1/2), S(x) = sum_{n<=x} chi(n), chi fixed "
                 "primitive quadratic mod 7",
         "mechanism": "Probe",
         "point": "x -> infinity",
         "removable_value": 0.0,
         "conjecture": "S(x)/sqrt(x) -> 0: partial sums of a periodic "
                       "mean-zero character are bounded (Poya-Vinogradov), "
                       "so the ratio provably vanishes at slope ~ -1/2; "
                       "the control member for 'raw oscillation is never "
                       "evidence; only the ratio's decade trend is'",
         "S_at_powers_of_10": {str(k): spot[10 ** k] for k in range(2, 8)},
         "decade_max_ratio": {str(d): ratiomax[d] for d in decs
                              if 2 <= d <= 7},
         "decade_max_abs": {str(d): absmax[d] for d in decs if 2 <= d <= 7},
         "ratio_beta": beta_ratio, "ratio_r2": r2_ratio,
         "box_ratio": box_ratio,
         "gates": gates, "overall": overall,
         "wall": "exact S(x) to 1e7; the truth of the limit rests on the "
                 "Poya-Vinogradov bound, not the wall; the cross-modulus "
                 "Paley oscillation (Omega_+(sqrt(q) log log q)) is a "
                 "separate 0/0 in q-space beyond any finite x-range"},
        open(os.path.join(DATA, "character_sums_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/character_sums_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()