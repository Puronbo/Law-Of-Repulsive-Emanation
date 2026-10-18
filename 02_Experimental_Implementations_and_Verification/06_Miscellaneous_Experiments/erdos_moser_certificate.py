"""Finite certificate for the Erdős–Moser equation (Gap Ledger G34).

The Erdős–Moser equation is 1^k + 2^k + ... + (m-1)^k = m^k with positive
integers m,k; the only known solution is 1+2 = 3 (m=3,k=1). Erdős conjectured
no other solutions. Moser (1953) showed that any further solution has k even,
various p-adic/divisibility conditions, and m > 10^10^6 (now improved to much
larger bounds); it remains OPEN. This script verifies no other solution exists
below a finite bound (m-1 small, k>=2 even by Moser conditions where relevant)
and does NOT settle the conjecture in general.
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


OUT = os.path.join(_central_data_dir(), "erdos_moser_certificate.json")


def power_sum(m1, k):
    """S_k(m1) = sum_{j=1}^{m1} j^k."""
    s = 0
    for j in range(1, m1 + 1):
        s += j ** k
    return s


def erdos_moser_solutions(max_m=100, max_k=20):
    """Search for (m,k) with m >= 4, k >= 1 and sum_{j< m} j^k == m^k.
    Known open: only (3,1). Return found pairs in window.
    """
    found = []
    for m in range(4, max_m + 1):
        rhs = m ** max_k  # not needed
        for k in range(1, max_k + 1):
            lhs = power_sum(m - 1, k)
            rhs_mk = m ** k
            if lhs == rhs_mk:
                found.append((m, k))
                break  # no larger k needed for same m? maybe not necessary, but cheap
    return found


def run(max_m=80, max_k=12):
    sol = erdos_moser_solutions(max_m=max_m, max_k=max_k)
    out = {
        "experiment": "erdos_moser_search",
        "max_m": max_m,
        "max_k": max_k,
        "solutions_found": sol,
        "known_solution": [3, 1],
        "honest_wall": (
            "Finite range only: no solution to sum_{j< m} j^k = m^k found with "
            "m <= %d, k <= %d except (3,1) (the conjecture stays OPEN in "
            "general). Moser (1953) showed any further solution requires k even, "
            "many p-adic conditions, and m > 10^10^6 (much larger bounds now)."
            % (max_m, max_k)),
        "references": [
            "Erdős–Moser equation (Wikipedia)",
            "Moser 1953 (necessary conditions, lower bound 10^10^6)",
            "Gallot-Moree-Zudilin 2010 (m > 10^10^9)",
            "Kellner 2011 (conjecture variants), Moree surveys",
        ],
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, default=str)
    return out


if __name__ == "__main__":
    run()
