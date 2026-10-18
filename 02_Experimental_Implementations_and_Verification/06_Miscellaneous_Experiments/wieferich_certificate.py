"""Finite certificate for Wieferich primes, base 2 (Gap Ledger G32).

A Wieferich prime is a prime p with 2^(p-1) = 1 (mod p^2); only p = 1093 and
p = 3511 are known.  Whether infinitely many exist is open (a heuristic based on
Crandall-Dilcher-Pomerance predicts ~log log x of them up to x, i.e. infinitely
many, but no proof is known; the abc conjecture would give finitely many).  This
script verifies by exact modular arithmetic that 1093 and 3511 are the only
Wieferich primes below a finite bound.  It does NOT settle infinitude.
"""
import json
import os


def _central_data_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        cand = os.path.join(here, "03_Data_and_Observational_Resources",
                            "02_Experimental_Data_Collections")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(here)
        if parent == here:
            raise RuntimeError("repository root not found from " + __file__)
        here = parent


OUT = os.path.join(_central_data_dir(), "wieferich_certificate.json")


def primes_below(limit):
    """All primes < ``limit`` (simple sieve)."""
    sieve = bytearray([1]) * limit
    sieve[0:2] = b"\x00\x00"
    i = 2
    while i * i < limit:
        if sieve[i]:
            sieve[i * i:limit:i] = b"\x00" * (((limit - 1 - i * i) // i) + 1)
        i += 1
    return [n for n in range(limit) if sieve[n]]


def is_wieferich(p):
    """2^(p-1) = 1 (mod p^2), for prime p (exact)."""
    return pow(2, p - 1, p * p) == 1


def wieferich_primes(limit):
    """Wieferich primes base 2 below ``limit`` (exact)."""
    return [p for p in primes_below(limit) if is_wieferich(p)]


def run(limit=10 ** 6):
    found = wieferich_primes(limit)
    out = {
        "experiment": "wieferich_prime_search_base2",
        "bound": limit,
        "wieferich_primes": found,
        "fermat_quotients": {str(p): (pow(2, p - 1, p * p) - 1) // p
                             for p in found},
        "honest_wall": (
            "Finite range only: 1093 and 3511 are the only Wieferich primes "
            "below %d; whether infinitely many exist stays OPEN. No others are "
            "known below 6.7x10^15 (Dorais-Klyve 2011, since extended past "
            "1.45x10^17, OEIS A001220)." % limit),
        "references": [
            "Wieferich 1909 (link to Fermat's Last Theorem, first case)",
            "Meissner 1913 (1093), Beeger 1922 (3511)",
            "Knauer-Richstein 2005 (no others < 1.25x10^15)",
            "Dorais-Klyve 2011, JIS 14 (no others < 6.7x10^15)",
            "Crandall, Dilcher, Pomerance 1997 (heuristic ~log log x)",
            "Silverman 1988 (abc conjecture implies finitely many)",
            "OEIS A001220",
        ],
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str)
    return out


if __name__ == "__main__":
    run()
