"""Finite certificate for Giuga's primality conjecture (Gap Ledger G30).

Giuga (1950): n > 1 is prime iff  sum_{k=1}^{n-1} k^{n-1} = -1 (mod n).
A composite n satisfying this is a "counterexample"; every such n is known to be
both a *Giuga number* and a *Carmichael number*.  This script verifies, by exact
integer arithmetic, that no counterexample exists below a finite bound: it lists
the Giuga numbers (composite n with  p | (n/p - 1)  for every prime p | n, i.e.
sum_{k=1}^{n-1} k^{phi(n)} = -1 (mod n)) up to the bound, then checks each against
Korselt's criterion for Carmichael numbers.  None qualifies, so Giuga's
conjecture holds to the bound -- it does NOT settle the conjecture.
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


OUT = os.path.join(_central_data_dir(), "giuga_certificate.json")


def spf_sieve(limit):
    """Smallest-prime-factor sieve up to ``limit`` inclusive."""
    spf = list(range(limit + 1))
    i = 2
    while i * i <= limit:
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    return spf


def factor(n, spf):
    """Distinct prime factors of ``n`` as a list of (prime, exponent)."""
    fac = []
    while n > 1:
        p = spf[n]
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        fac.append((p, e))
    return fac


def _squarefree(fac):
    return all(e == 1 for _, e in fac)


def is_giuga(n, fac):
    """Composite n with  p | (n/p - 1)  for every prime p | n."""
    if len(fac) < 2 or not _squarefree(fac):
        return False
    return all((n // p - 1) % p == 0 for p, _ in fac)


def is_carmichael(n, fac):
    """Korselt's criterion: squarefree and (p - 1) | (n - 1) for every p | n."""
    if len(fac) < 3 or not _squarefree(fac):
        return False
    return all((n - 1) % (p - 1) == 0 for p, _ in fac)


def giuga_numbers(limit):
    """All Giuga numbers <= ``limit`` (exact)."""
    spf = spf_sieve(limit)
    found = []
    for n in range(2, limit + 1):
        fac = factor(n, spf)
        if is_giuga(n, fac):
            found.append((n, [p for p, _ in fac],
                          is_carmichael(n, fac)))
    return found


def run(limit=10 ** 5):
    spf = spf_sieve(limit)
    nums = giuga_numbers(limit)
    out = {
        "experiment": "giuga_counterexample_search",
        "bound": limit,
        "giuga_numbers": [{"n": n, "prime_factors": pf, "is_carmichael": c}
                          for n, pf, c in nums],
        "giuga_numbers_value": [n for n, _, _ in nums],
        "counterexamples_found": [n for n, _, c in nums if c],
        "honest_wall": (
            "Finite range only: no counterexample to Giuga's conjecture below "
            "%d (the four known Giuga numbers up to %d are all non-Carmichael). "
            "Giuga's conjecture stays OPEN; a counterexample would need "
            ">= 19908 digits (Borwein-Maitland-Skerritt 2013), and whether "
            "there are infinitely many Giuga numbers is likewise open."
            % (limit, limit)),
        "known_giuga_numbers": [
            30, 858, 1722, 66198, 2214408306, 24423128562, 432749205173838,
            14737133470010574, 550843391309130318,
            244197000982499715087866346, 554079914617070801288578559178,
            1910667181420507984555759916338506],
        "references": [
            "Giuga 1950 (primality conjecture)",
            "Korselt 1899 (Carmichael criterion)",
            "Borwein, Borwein, Borwein, Girgensohn 1996 (bound 13800 digits)",
            "Borwein, Maitland, Skerritt, INTEGERS 13 (2013) (bound 19908 digits)",
            "Alford, Granville, Pomerance 1994 (infinitely many Carmichael numbers)",
            "OEIS A007850 (Giuga numbers)",
        ],
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str)
    return out


if __name__ == "__main__":
    run()
