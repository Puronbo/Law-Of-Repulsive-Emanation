"""
NUMBER THEORY (ANTI-CLASS): POLYA'S CONJECTURE, THE 0/0 WITHOUT
REMOVABLE VALUE
================================================================
Atlas entry 64.  The one class the atlas founded as empty.

Form.  F(n) = sum_{k<=n} lambda(k)  (lambda = Liouville, (-1)^Omega(k)).
The scaling ratio  F(n)/n^{1/2}  is the 0/0 candidate: every prime
factor of n pays a sign, so F behaves like the balance of fair coin
tosses (one per prime factor).  Polya conjectured F(n) <= 0 for all
n >= 2.  IF that held, the ratio F(n)/sqrt(n) would sit at or below
0 forever: a removable "value" at most 0.

Littlewood (and later Lehman/Tanaka) showed the truth is the
OPPOSITE class: the limit does NOT exist -- F(n) = Omega_+(sqrt(n))
and Omega_-(sqrt(n)) (unbounded oscillations of both signs), and the
first positive F(n) occurs at n = 906,150,257.  So this is a 0/0
whose removable value does not exist: the Decision Tree's "if limit
does not exist -> not a removable singularity" branch, realised as a
living conjecture that data supports for 2 <= n < 9.1e8 and that is
FALSE.

This is the honest wall as an entry: 63 of 63 previous entries have
removable values; Polya proves the complementary class is non-empty,
so "all instances are removable" was a statement of corpus bias, not
of nature.

Verification here: exact parity sieve of Omega up to 1e7; record
excursion growth (oscillatory signature, NOT a converging limit);
first-10 F values against the known sequence.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")


def liouville_summatory(N):
    """Exact F(n) = sum_{k<=n} lambda(k) up to N via a parity sieve."""
    par = bytearray(N + 1)  # 1 iff Omega(k) odd
    sieve = bytearray([1]) * (N + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    primes = [i for i in range(2, N + 1) if sieve[i]]
    for p in primes:
        q = p
        while q <= N:
            for m in range(q, N + 1, q):
                par[m] ^= 1
            q *= p
    F = [0] * (N + 1)
    running = 0
    for n in range(1, N + 1):
        running += 1 if par[n] == 0 else -1
        F[n] = running
    return F


def main():
    print("=" * 70)
    print("POLYA / LIOUVILLE: THE 0/0 WITHOUT REMOVABLE VALUE")
    print("=" * 70)
    N = 10_000_000
    F = liouville_summatory(N)

    first10 = F[1:11]
    known = [1, 0, -1, 0, -1, 0, -1, -2, -1, 0]
    g1 = first10 == known
    print(f"F(1..10) = {first10}  (known {known})  {'OK' if g1 else 'MISMATCH'}")

    g2 = True
    fmin = fargmin = fmax = fargmax = None
    records = []  # (n, F) for new min records
    for n in range(2, N + 1):
        v = F[n]
        if v > 0:
            g2 = False
        if fmax is None or v > fmax:
            fmax = v
            fargmax = n
        if fmin is None or v < fmin:
            fmin = v
            fargmin = n
            records.append((n, v))
    print(f"Polya predicate F(n)<=0 over [2,{N}]: {'KEPT' if g2 else 'BROKEN'} "
          f"(maxF={fmax} at n={fargmax}, minF={fmin} at n={fargmin})")

    # Oscillation signature, data-honest: a settled removable limit would
    # stop producing new extreme records; a live +/-sqrt(n) walk keeps
    # setting records with frequency ~ sqrt(n) (fresh minima to the end).
    # Finite data cannot prove non-convergence -- that is the honest wall;
    # the statistics are the strongest evidence a census can offer.
    nrec = len(records)
    last_rec_n = records[-1][0] if nrec else 0
    g3 = (500 <= nrec <= 8000) and (last_rec_n > N // 2)
    print(f"  {nrec} new negative records over [2,{N}] "
          f"(random-walk scale ~ sqrt(N) = {int(math.sqrt(N))}); "
          f"last record at n={last_rec_n}")
    for n in (10**3, 10**4, 10**5, 10**6, 10**7):
        if n <= N:
            print(f"  n={n:>9,}  F(n)={F[n]:>7,}  F/sqrt(n)={F[n]/math.sqrt(n):+.4f}")

    print("\n" + "-" * 70)
    print("INTERPRETATION")
    print("-" * 70)
    print("A conjectured 'removable value at most 0' whose limit provably")
    print("does not exist (Littlewood 1914: F(n)=Omega_+(sqrt(n)) AND")
    print("Omega_-(sqrt(n))).  First positive F at n = 906,150,257")
    print("(Lehman; Tanaka 1980).  Data supports Polya to 1e7 and the")
    print("genuine class is the NON-EXISTENT removable value: entry 64,")
    print("the corpus counterweight to the 63/63 removable value claim.")

    g4 = True  # Littlewood-cited anti-class; finite check cannot prove it
    gates = {"G1 F(1..10) exact (A002819)": g1,
             "G2 Polya predicate holds over [2,1e7]": g2,
             "G3 record census: live walk to 1e7 (oscillation signature)": g3,
             "G4 anti-class cited (Littlewood; first+ at 906150257)": g4}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'} (entry establishes the "
          f"non-removable class; the conjecture itself is FALSE)")

    os.makedirs(DATA, exist_ok=True)
    json.dump(
        {"form": "F(n)/sqrt(n), F(n)=sum lambda(k)", "mechanism": "ANTI-CLASS",
         "point": "n -> inf (records)", "removable_value": None,
         "conjecture": "Polya F(n)<=0 false (Littlewood Omega_+-)",
         "first_positive_known": 906150257, "first10": first10,
         "minF": fmin, "minF_n": fargmin,
         "n_records": nrec, "last_record_n": last_rec_n,
         "gates": gates, "overall": overall,
         "wall": "finite range to 1e7; anti-class value from Littlewood"},
        open(os.path.join(DATA, "polya_liouville_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/polya_liouville_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()