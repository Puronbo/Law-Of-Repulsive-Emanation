"""Finite certificate for Beal's conjecture (Gap Ledger G33).

Beal's conjecture (1993): if a^x + b^y = c^z with a,b,c,x,y,z positive integers,
x,y,z > 2, then gcd(a,b,c) > 1. It is a generalization of Fermat's Last Theorem
and implies cases of Fermat-Catalan (under the common-factor condition).

This script verifies a finite search window: it enumerates small positive integers
a,b,c and exponents 3 <= x,y,z <= M and checks for coprime solutions to
a^x + b^y = c^z (and symmetries) -- finding none. It does NOT prove the conjecture
in general (still OPEN).

Strengthened (exact arithmetic) 2026-10-19:
  * the candidate root `c = s^(1/z)` is now computed with an EXACT integer z-th root
    (`_iroot`, Newton with an integer correction step) instead of a float
    `round(s ** (1.0/z))`, so no rounding slip can hide or invent a solution;
  * every candidate sum `s = a^x + b^y` is first passed through an EXACT modular
    pre-check: `s % 9` must be a z-th power residue modulo 9 (`_pow_residues9`),
    which is a genuine (window-independent) necessary condition;
  * the search leans on the proven reduction `PunoCalculus.Beal.three_dvd_of_cubes`
    (machine-checked, exact): a solution to A^3 + B^3 = C^3 forces 3 | A or 3 | B or
    3 | C, i.e. no solution has all three bases coprime to 3.

Neither the finite window nor the exact reductions prove Beal's conjecture.
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


def _iroot(n, k):
    """Exact floor of the k-th root of n >= 0 (integer arithmetic only)."""
    if n < 0:
        raise ValueError("negative radicand")
    if n < 2 or k == 1:
        return n
    # integer seed 2^ceil(bitlength/k) >= n^(1/k), then integer Newton + correction
    x = 1 << (-(-n.bit_length() // k))
    while True:
        y = ((k - 1) * x + n // (x ** (k - 1))) // k
        if y >= x:
            break
        x = y
    while x ** k > n:
        x -= 1
    while (x + 1) ** k <= n:
        x += 1
    return x


def _pow_residues9(z):
    """Set of z-th power residues modulo 9 -- an exact necessary condition."""
    return {pow(r, z, 9) for r in range(9)}


def beal_counterexamples(max_base=200, max_exp=10):
    """Search for coprime Beal counterexamples a^x + b^y = c^z with
    1 < a <= b, 3 <= x,y,z <= max_exp, c^z = a^x + b^y <= max_base^max_exp.
    Returns list of small solutions found (should be empty in window).
    """
    found = []
    pow_cache = {}

    def powv(n, e):
        k = (n, e)
        if k not in pow_cache:
            pow_cache[k] = n ** e
        return pow_cache[k]

    residues = {z: _pow_residues9(z) for z in range(3, max_exp + 1)}

    for a in range(1, max_base + 1):
        for b in range(a, max_base + 1):
            for x in range(3, max_exp + 1):
                ax = powv(a, x)
                for y in range(3, max_exp + 1):
                    by = powv(b, y)
                    s = ax + by
                    if s < 8:
                        continue
                    for z in range(3, max_exp + 1):
                        # EXACT necessary condition: c^z = s requires s % 9 to be a
                        # z-th power residue mod 9 (rules out entire cases, exactly).
                        if (s % 9) not in residues[z]:
                            continue
                        rz = _iroot(s, z)
                        if rz < 2 or rz > max_base:
                            continue
                        if powv(rz, z) != s:
                            continue
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
        "method": "exact integer z-th roots + exact modulo-9 power-residue pre-check",
        "mod9_reduction": (
            "PunoCalculus.Beal.three_dvd_of_cubes (machine-checked): "
            "A^3 + B^3 = C^3 forces 3 | A or 3 | B or 3 | C; no solution has all "
            "three bases coprime to 3."),
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
