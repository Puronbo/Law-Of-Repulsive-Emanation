"""Finite certificate for the odd-perfect-number problem (Gap Ledger G27) and
Mersenne primes / even perfect numbers (Gap Ledger G29).

Honest finite computation only:

* Even perfect numbers correspond to Mersenne primes (Euclid-Euler), so the
  even list is completely classified.
* Odd perfect numbers: none is known, and none exists below the recorded search
  limit (a divisor-sum sieve).  Euler's necessary form (n = q^a m^2 with
  q = a = 1 mod 4, q prime) is recorded as a structural constraint.

The open claim -- that no odd perfect number exists -- is NOT resolved here;
only a bounded search is certified.
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


OUT = os.path.join(_central_data_dir(), "perfect_numbers_certificate.json")


def sigma_sieve(limit):
    """sigma[n] = sum of positive divisors of n, for 0 <= n <= limit."""
    sig = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for m in range(d, limit + 1, d):
            sig[m] += d
    return sig


def perfect_search(sig, limit):
    """Perfect numbers n <= limit (sigma(n) == 2n), split into even/odd."""
    even = [n for n in range(2, limit + 1, 2) if sig[n] == 2 * n]
    odd = [n for n in range(3, limit + 1, 2) if sig[n] == 2 * n]
    return {"limit": limit, "even": even, "odd": odd,
            "odd_found": len(odd) > 0,
            "assertion": "unknown"}


def euler_form_note():
    """Euler's necessary condition on an odd perfect number n = q^a m^2 with
    q prime, q = a = 1 (mod 4).  None is known; the search below is finite."""
    return {
        "form": "n = q^a * m^2, q prime, q = a = 1 (mod 4), m odd",
        "none_known": True,
        "known_lower_bound_citation": "> 10^1500 (Ochem-Rao 2012)",
    }


def _is_prime_small(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def mersenne_primes(pmax):
    """Exact Lucas-Lehmer certificate: for each prime exponent p <= pmax,
    M_p = 2^p - 1 is prime iff the LL iteration s = s^2 - 2 (mod M_p),
    s_0 = 4, terminates at 0 after p - 2 steps.  Returns the exponents found;
    infinitude of Mersenne primes is OPEN (Euclid-Euler links them to the even
    perfect numbers)."""
    exps = [2] if pmax >= 2 else []
    for p in range(3, pmax + 1, 2):
        if not _is_prime_small(p):
            continue
        m = (1 << p) - 1
        s = 4
        for _ in range(p - 2):
            s = (s * s - 2) % m
        if s == 0:
            exps.append(p)
    return {"pmax": pmax, "exponents": exps, "count": len(exps),
            "known_total_citation": 52,
            "largest_known_citation": "2^136279841 - 1 (GIMPS, Oct 2024)"}


def run(limit=10 ** 6, pmax=5000):
    sig = sigma_sieve(limit)
    found = perfect_search(sig, limit)
    print("Even perfect numbers <= %d: %s" % (limit, found["even"]))
    print("Odd perfect numbers <= %d: %s" % (limit, found["odd"]))
    mp = mersenne_primes(pmax)
    print("Mersenne prime exponents <= %d: %s" % (pmax, mp["exponents"]))
    out = {
        "experiment": "Perfect numbers / Mersenne primes (Gap Ledger G27, G29)",
        "search_limit": limit,
        "even_perfect": found["even"],
        "odd_perfect": found["odd"],
        "euler_form": euler_form_note(),
        "mersenne_primes": mp,
        "honest_wall": (
            "Finite search only: no odd perfect number exists up to the search "
            "limit; the even perfect numbers are exactly those built from "
            "Mersenne primes (Euclid-Euler). The Mersenne list is exact (Lucas-"
            "Lehmer) only for exponents <= pmax. Whether any odd perfect number "
            "exists (best known bound > 10^1500) and whether infinitely many "
            "Mersenne primes exist both remain OPEN."
        ),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("Wrote %s" % OUT)
    return out


if __name__ == "__main__":
    run()
