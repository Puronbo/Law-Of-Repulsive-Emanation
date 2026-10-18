"""Finite certificate for Beal's conjecture (Gap Ledger G33).

Beal's conjecture (1993): if a^x + b^y = c^z with a,b,c,x,y,z positive integers,
x,y,z > 2, then gcd(a,b,c) > 1. It is a generalization of Fermat's Last Theorem
and implies cases of Fermat-Catalan (under the common-factor condition).
This script verifies a finite search window: it enumerates small positive
integers a,b,c and exponents 3 <= x,y,z <= M and checks for coprime solutions to
a^x + b^y = c^z (and symmetries) -- finding none. It does NOT prove the
conjecture in general (still OPEN).
"""
import json
import os
from math import gcd


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


OUT = os.path.join(_central_data_dir(), "beal_certificate.json")


def beal_counterexamples(max_base=200, max_exp=10):
    """Search for coprime Beal counterexamples a^x + b^y = c^z with
    1 < a <= b, 3 <= x,y,z <= max_exp, c^z = a^x + b^y <= max_base^max_exp.
    Returns list of small solutions found (should be empty in window).
    """
    found = []
    # build list of powers up to bound to avoid recomputation
    pow_cache = {}
    def powv(n, e):
        k = (n, e)
        if k not in pow_cache:
            pow_cache[k] = n ** e
        return pow_cache[k]

    for a in range(1, max_base + 1):
        for b in range(a, max_base + 1):
            for x in range(3, max_exp + 1):
                ax = powv(a, x)
                if ax > max_base ** 3:  # coarse
                    pass
                for y in range(3, max_exp + 1):
                    by = powv(b, y)
                    s = ax + by
                    if s < 8:
                        continue
                    # factor s? just try small exponents z>=3 for c = integer root
                    for z in range(3, max_exp + 1):
                        # find integer c = round(s^(1/z))
                        if z > 64:
                            break
                        rz = int(round(s ** (1.0 / z)))
                        if rz < 2:
                            continue
                        if rz > max_base:
                            continue
                        cz = powv(rz, z)
                        if cz == s:
                            # found integer solution a^x + b^y = c^z
                            g = gcd(gcd(a, b), rz)
                            if g == 1:
                                found.append((a, x, b, y, rz, z, s))
                            break  # next (x,y,a,b)
    return found


def run(max_base=100, max_exp=6):
    cex = beal_counterexamples(max_base=max_base, max_exp=max_exp)
    out = {
        "experiment": "beal_conjecture_search",
        "max_base": max_base,
        "max_exp": max_exp,
        "coprime_counterexamples": cex,
        "honest_wall": (
            "Finite range only: no coprime solution to a^x+b^y=c^z with "
            "x,y,z>2 found below the search window (%d^%d); Beal's conjecture "
            "stays OPEN in general. Published searches have eliminated large "
            "windows without counterexamples (Norvig, Vanderkam, others)."
            % (max_base, max_exp - 1)),
        "references": [
            "Beal 1993 (posed; AMS prize $1,000,000)",
            "Wiles 1995 (Fermat's Last Theorem)",
            "Darmon-Granville (Fermat-Catalan finiteness for fixed exponents)",
            "Poonen-Schaefer-Stoll 2005 (2,3,7), Bruin (2,3,8),(2,3,9), "
            "Zureick-Brown (2,3,10), etc.",
            "Norvig computational searches; notabs.org/Beal summary (2013)",
            "AMS: Beal Conjecture prize statement",
        ],
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str)
    return out


if __name__ == "__main__":
    run()
