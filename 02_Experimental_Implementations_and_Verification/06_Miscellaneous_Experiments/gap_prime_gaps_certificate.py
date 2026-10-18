"""Finite certificates for the prime conjectures (Gap Ledger G15-G20).

Honest finite computations, each certifying a bounded range only:

* G16 Andrica: sqrt(p_{n+1}) - sqrt(p_n) < 1 for all consecutive prime pairs
  up to the sieve limit.
* G15 Brocard: at least four primes lie strictly between p_n^2 and p_{n+1}^2,
  verified for every n whose interval fits inside the sieve limit.
* G17 Oppermann: a prime strictly between n^2 and n(n+1), and one strictly
  between n(n+1) and (n+1)^2, for every n whose interval fits.
* G18 Gilbreath: leading term of every absolute-difference row of the primes
  is 1 (verified to the first few thousand primes; O(m^2)).
* G19 Polignac: for every even k <= 100 there is a prime pair differing by k
  (existence only; infinitude is the open claim).
* G20 Sophie Germain: finite count of primes p with 2p+1 prime (infinitude OPEN).

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


def gilbreath(ps, m=2000):
    """Gilbreath: with the primes as row 0, take absolute differences row by
    row; the leading entry of every row is 1.  Checked on the first ``m`` primes
    (the full check is O(m^2))."""
    row = list(ps[:m])
    rows = 0
    ok = True
    while len(row) > 1:
        row = [abs(row[i + 1] - row[i]) for i in range(len(row) - 1)]
        rows += 1
        if row[0] != 1:
            ok = False
            break
    return {"primes_used": min(len(ps), m), "rows": rows,
            "leading_always_one": ok}


def polignac(s, limit, kmax):
    """Polignac: for each even gap k, some prime pair differs by k.  For each
    even k <= kmax we record the smallest starting prime (existence, not the
    open infinitude claim)."""
    smallest = {}
    for k in range(2, kmax + 1, 2):
        found = None
        for p in range(2, limit - k + 1):
            if s[p] and s[p + k]:
                found = p
                break
        smallest[k] = found
    return {
        "kmax": kmax,
        "all_found": all(v is not None for v in smallest.values()),
        "smallest": {str(k): v for k, v in smallest.items()},
    }


def sophie_germain(s, limit):
    """Sophie Germain primes: primes p with 2p+1 also prime.  Records the finite
    count up to the sieve limit (infinitude is OPEN)."""
    cnt = 0
    for p in range(2, limit + 1):
        if s[p] and 2 * p + 1 <= limit and s[2 * p + 1]:
            cnt += 1
    return {"limit": limit, "count": cnt}


def fermat_numbers():
    """Fermat numbers F_k = 2^(2^k)+1.  F_0..F_4 are prime (finite primality
    certificate); F_5 is composite (641 | F_5).  Whether infinitely many Fermat
    primes exist is OPEN."""
    def isprime(n):
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True
    facts = []
    for k in range(0, 6):
        v = (1 << (1 << k)) + 1
        if k <= 4:
            facts.append({"k": k, "value": v, "prime": isprime(v)})
        else:
            facts.append({"k": k, "value": v, "prime": False,
                          "factor": 641, "divides": v % 641 == 0})
    return {
        "known_fermat_primes": [f["k"] for f in facts if f["prime"]],
        "facts": facts,
    }


def landau_n2_plus_1(s, limit, nmax=None):
    """Landau: infinitely many primes of the form n^2 + 1 (OPEN).  Finite
    certificate: count of such primes for n with n^2+1 <= limit."""
    if nmax is None:
        nmax = int((limit - 1) ** 0.5)
    cnt = 0
    first_n = []
    for n in range(0, nmax + 1):
        v = n * n + 1
        if v <= limit and s[v]:
            cnt += 1
            if len(first_n) < 5:
                first_n.append(n)
    return {"nmax": nmax, "count": cnt, "first_n": first_n}


def euler_polynomial(nmax=40):
    """No-go: the naive claim 'n^2+n+41 is prime for all n>=0' is FALSE.  It is
    prime for n=0..39 but composite at n=40 (1681 = 41^2)."""
    def isprime(n):
        if n < 2:
            return False
        i = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i += 1
        return True
    prime = {n: isprime(n * n + n + 41) for n in range(0, nmax + 1)}
    first_composite = next((n for n in range(0, nmax + 1) if not prime[n]), None)
    return {
        "nmax": nmax,
        "first_composite_n": first_composite,
        "prime_for_all_below_first_composite": (
            first_composite is not None
            and all(prime[n] for n in range(0, first_composite))
        ),
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

    g = gilbreath(ps)
    print("Gilbreath: %d rows, leading always 1: %s"
          % (g["rows"], g["leading_always_one"]))

    po = polignac(s, limit, 100)
    print("Polignac: even k<=100 all found: %s" % po["all_found"])

    sg = sophie_germain(s, limit)
    print("Sophie Germain primes <= %d: %d" % (limit, sg["count"]))

    fe = fermat_numbers()
    print("Fermat: known prime indices %s (F_5 composite)"
          % fe["known_fermat_primes"])

    la = landau_n2_plus_1(s, limit)
    print("Landau n^2+1 primes (n<=%d): %d" % (la["nmax"], la["count"]))

    eu = euler_polynomial()
    print("Euler n^2+n+41 first composite at n=%s" % eu["first_composite_n"])

    out = {
        "experiment": "Prime finite certificates (Gap Ledger G15-G25)",
        "sieve_limit": limit,
        "andrica": a,
        "brocard": b,
        "oppermann": o,
        "gilbreath": g,
        "polignac": po,
        "sophie_germain": sg,
        "fermat": fe,
        "landau_n2_plus_1": la,
        "euler_polynomial": eu,
        "honest_wall": (
            "Finite ranges only: Andrica verified up to the sieve limit, "
            "Brocard/Oppermann for intervals inside it, Gilbreath to the first "
            "few thousand primes, Polignac existence for even k <= 100, Sophie "
            "Germain and n^2+1 prime counts to the sieve limit, Fermat primality "
            "for F_0..F_4 only. All corresponding conjectures remain OPEN "
            "(no unconditional proof for all n)."
        ),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("Wrote %s" % OUT)
    return out


if __name__ == "__main__":
    run()
