"""Finite certificates for the prime-gap conjectures (Gap Ledger).

Three honest finite computations, each certifying a bounded range only:

* G16 Andrica: sqrt(p_{n+1}) - sqrt(p_n) < 1 for all consecutive prime pairs
  up to the sieve limit.
* G15 Brocard: at least four primes lie strictly between p_n^2 and p_{n+1}^2,
  verified for every n whose interval fits inside the sieve limit.
* G17 Oppermann: a prime strictly between n^2 and n(n+1), and one strictly
  between n(n+1) and (n+1)^2, for every n whose interval fits.

None certifies the conjecture for all n; all remain OPEN.
"""
import math
import json
import os
import time


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


OUT = os.path.join(_central_data_dir(), "gap_prime_gaps_certificate.json")


def sieve(limit):
    """Bytearray sieve: index i is 1 iff i is prime, for 0 <= i <= limit."""
    s = bytearray([1]) * (limit + 1)
    s[0] = s[1] = 0
    i = 2
    while i * i <= limit:
        if s[i]:
            s[i * i::i] = bytearray(len(range(i * i, limit + 1, i)))
        i += 1
    return s


def primes_upto(s, limit):
    return [i for i in range(2, limit + 1) if s[i]]


def andrica(s, limit, ps):
    max_slack = 0.0
    arg = (0, 0)
    for a, b in zip(ps, ps[1:]):
        d = math.sqrt(b) - math.sqrt(a)
        if d > max_slack:
            max_slack = d
            arg = (a, b)
    return {
        "limit": limit,
        "pairs": len(ps) - 1,
        "max_sqrt_gap": max_slack,
        "argmax_pair": list(arg),
        "all_below_one": max_slack < 1.0,
    }


def oppermann(s, limit, max_n):
    """Oppermann: for every n >= 2 there is a prime strictly between n^2 and
    n(n+1), and one strictly between n(n+1) and (n+1)^2."""
    n_done = 0
    worst = None
    for n in range(2, max_n + 1):
        a, b, c = n * n, n * (n + 1), (n + 1) * (n + 1)
        if c > limit:
            break
        left = any(s[m] for m in range(a + 1, b))
        right = any(s[m] for m in range(b + 1, c))
        n_done += 1
        if not (left and right):
            worst = n
            break
    return {
        "n_checked": n_done,
        "all_have_prime": worst is None,
        "first_failure": worst,
    }


def brocard(s, limit, ps, max_n):
    worst_n, worst_c = None, None
    n_done = 0
    for n in range(2, min(max_n, len(ps) - 1) + 1):
        a, b = ps[n - 1] ** 2, ps[n] ** 2
        if b > limit:
            break
        c = sum(s[m] for m in range(a + 1, b))
        n_done += 1
        if worst_c is None or c < worst_c:
            worst_n, worst_c = n, c
    return {
        "n_checked": n_done,
        "min_prime_count": worst_c,
        "min_prime_count_at_n": worst_n,
        "all_at_least_four": (worst_c is not None and worst_c >= 4),
    }


def run(limit=10 ** 7, brocard_max_n=100000):
    print("Sieve to %d..." % limit)
    t0 = time.time()
    s = sieve(limit)
    ps = primes_upto(s, limit)
    print("  %d primes in %.2fs" % (len(ps), time.time() - t0))

    a = andrica(s, limit, ps)
    print("Andrica: max sqrt-gap %.6f at %s (all<1: %s)"
          % (a["max_sqrt_gap"], a["argmax_pair"], a["all_below_one"]))

    b = brocard(s, limit, ps, brocard_max_n)
    print("Brocard: %d intervals, min count %s (all>=4: %s)"
          % (b["n_checked"], b["min_prime_count"], b["all_at_least_four"]))

    o = oppermann(s, limit, brocard_max_n)
    print("Oppermann: %d intervals, all have prime: %s"
          % (o["n_checked"], o["all_have_prime"]))

    out = {
        "experiment": "Prime-gap finite certificates (Gap Ledger G15/G16/G17)",
        "sieve_limit": limit,
        "andrica": a,
        "brocard": b,
        "oppermann": o,
        "honest_wall": (
            "Finite ranges only: Andrica verified up to the sieve limit, "
            "Brocard for intervals inside it, Oppermann for n with (n+1)^2 "
            "inside it. All three conjectures remain OPEN "
            "(no unconditional proof for all n)."
        ),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("Wrote %s" % OUT)
    return out


if __name__ == "__main__":
    run()
