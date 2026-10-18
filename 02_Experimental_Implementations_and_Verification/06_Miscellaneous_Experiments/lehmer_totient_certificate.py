"""Finite certificate for Lehmer's totient problem (Gap Ledger G31).

Lehmer (1932) asked whether any composite n satisfies phi(n) | (n - 1); none is
known.  Such an n must be odd, squarefree and Carmichael, and (Cohen-Hagis 1980,
Renze; Pinch) n > 10^26 with at least 15 distinct prime factors.  This script
verifies by exact integer arithmetic that no composite n below a finite bound has
phi(n) | (n - 1), and that the *2-Lehmer* relaxation (phi(n) | (n - 1)^2) is
strictly weaker: it already has solutions below 10^4, namely 561, 1105, 1729,
2465, 6601, 8481, where the first five are Carmichael numbers but 8481 is not.
It does NOT settle the conjecture.
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


OUT = os.path.join(_central_data_dir(), "lehmer_totient_certificate.json")


def totient_sieve(limit):
    """Euler phi for every n <= limit (exact)."""
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:  # p is prime
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi


def spf_sieve(limit):
    spf = list(range(limit + 1))
    i = 2
    while i * i <= limit:
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    return spf


def distinct_primes(n, spf):
    ps = []
    while n > 1:
        p = spf[n]
        ps.append(p)
        while n % p == 0:
            n //= p
    return ps


def lehmer_composites(limit):
    """Composite n <= limit with phi(n) | (n - 1) (expected: none)."""
    phi = totient_sieve(limit)
    found = []
    for n in range(2, limit + 1):
        if phi[n] == n - 1:
            continue  # n is prime
        if (n - 1) % phi[n] == 0:
            found.append(n)
    return found


def two_lehmer_numbers(limit):
    """Composite n <= limit with phi(n) | (n - 1)^2, with prime factors."""
    phi = totient_sieve(limit)
    spf = spf_sieve(limit)
    found = []
    for n in range(2, limit + 1):
        if phi[n] == n - 1:
            continue
        if ((n - 1) ** 2) % phi[n] == 0:
            found.append({"n": n, "prime_factors": distinct_primes(n, spf)})
    return found


def run(limit=10 ** 6):
    m = limit // 100  # keep the 2-Lehmer sweep cheap (10**4)
    out = {
        "experiment": "lehmer_totient_search",
        "bound": limit,
        "lehmer_composites": lehmer_composites(limit),
        "two_lehmer_bound": m,
        "two_lehmer_numbers": two_lehmer_numbers(m),
        "honest_wall": (
            "Finite range only: no composite n <= %d has phi(n) | (n - 1) (the "
            "conjecture stays OPEN beyond it), while the 2-Lehmer relaxation "
            "phi(n) | (n - 1)^2 already has solutions below 10^4 (and is thus "
            "strictly weaker). A Lehmer counterexample would be odd, "
            "squarefree and Carmichael, with >= 15 distinct prime factors and "
            "n > 10^26." % limit),
        "references": [
            "Lehmer 1932 (posed the problem; counterexample odd, squarefree, "
            ">= 7 prime factors)",
            "Cohen & Hagis 1980 (omega(n) >= 14, n > 10^20)",
            "Renze (omega(n) >= 15); Pinch (n > 10^26)",
            "Pomerance 1977, Pacific J. Math. (N(L,x) = O(x^{1/2} log^{3/4} x))",
            "Luca-Pomerance 2019 (N(L,x) <= x^{1/2} / log^{1/2+o(1)} x)",
            "Burcsi-Czirbusz-Farkas 2011 (3 | n => omega(n) >= 4e7, n > 10^3.6e8)",
            "Burek-Zmija 2019 (n <= 2^(2^r) - 2^(2^(r-1)) if 2 <= omega(n) <= r)",
            "Grau-Oller-Marcen (k-Lehmer numbers); OEIS A173703 (2-Lehmer)",
        ],
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str)
    return out


if __name__ == "__main__":
    run()
