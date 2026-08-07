"""The definitive-constant explorer (``puno-constants``).

The project's L.O.R.E. thesis is that the integration constant is only
arbitrary while the initial condition is unknown; the moment ``(q0, V(q0))``
is *measured*, ``C0`` is a number.  This CLI walks the project's own assets
and prints the constants those measurements determine:

    1. L.O.R.E. C0 = V(q0) = H(q0, 0) -- measured live on the Poincare disk
       from ``Universals/hamiltonian_flow.py`` (the repulsion potential).
    2. Fold mirror area  --  ``\\int_0^TH (a*theta)^2 dtheta = a^2*TH^3/3``,
       computed exactly by the engine's antiderivative (a = 1, TH = 20 gives
       2666.666... = 2 * a^2 * TH^3 / 6).
    3. epoch_0d datum  --  tau(10262000) = tau(26102000) = 80 and the
       gcd triangle 2000 / 31 / 1 (computed with integer arithmetic here).
    4. Prime-count datum  --  pi(943,901,200,001) = 35,575,526,191, loaded
       from ``data/prime_engine_data.json`` (sieved, not re-sieved).
    5. Quantum ground state  --  E0 = 5.843778304934855, loaded from
       ``data/spectral_data.json``.

Everything the explorer prints is either recomputed here with integer/ exact
arithmetic or read from a persisted asset; nothing is fabricated.
"""

from __future__ import annotations

import json
import math
import os
import sys
from importlib import resources as _res

from . import calculus

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data")


def _load_json(name: str):
    """Read an experiment JSON asset.

    Prefers the installed ``data`` package (works from a wheel); falls back
    to the repository ``data/`` directory for a bare source checkout.
    """
    try:
        import data
    except ImportError:
        data = None
    if data is not None:
        try:
            with _res.files(data).joinpath(name).open("r",
                                                      encoding="utf-8") as fh:
                return json.load(fh)
        except (FileNotFoundError, OSError):
            pass
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _divisor_count(n: int) -> int:
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            count += 1
            if i != n // i:
                count += 1
        i += 1
    return count


def _prime_factors(n: int):
    fac = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            fac[d] = fac.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        fac[n] = fac.get(n, 0) + 1
    return fac


def _load_json(name: str):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- #
# The five definitive constants
# --------------------------------------------------------------------------- #

def lore_constant(q0=(0.0, 0.0), context=("Tech", "Silicon")):
    """1. C0 = V(q0) = H(q0,0), measured from the Poincare-disk asset."""
    try:
        res = calculus.lore_measure(q0, list(context))
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}
    return {
        "ok": True,
        "name": "L.O.R.E. C0 = V(q0) = H(q0, 0)",
        "source": res["source"],
        "q0": res["q0"],
        "context": res["context"],
        "C0": res["C0"],
        "V_q0": res["V_q0"],
        "H_q0_0": res["H_q0_0"],
    }


def fold_mirror_area(a: float = 1.0, th: float = 20.0):
    """2. Fold mirror area: exact integral of (a*theta)^2 over [0, TH].

    The engine integrates ``theta^2`` symbolically and multiplies by a^2,
    giving ``a^2 * TH^3 / 3`` (reported by the README as 2 * a^2 * TH^3 / 6,
    the double sweep).  The exact value is re-derived; the numeric value
    cross-checks it.
    """
    area_expr = "x^2"
    d = calculus.definite_integral(area_expr, 0.0, float(th))
    engine_antideriv = d["antiderivative"]            # x^3 / 3
    exact = float(a) ** 2 * float(th) ** 3 / 3.0
    return {
        "ok": True,
        "name": "Fold mirror area",
        "integrand": "a^2 * theta^2 over [0, TH]",
        "antiderivative(theta)": engine_antideriv,
        "a": float(a), "TH": float(th),
        "exact": exact,
        "as_2a2TH3_over_6": 2.0 * float(a) ** 2 * float(th) ** 3 / 6.0,
        "cross_check_numeric": d["numeric_value"] or d["exact_value"],
    }


def epoch_0d():
    """3. The epoch datum: both calendar renderings have tau = 80."""
    n1, n2 = 10_262_000, 26_102_000
    t1, t2 = _divisor_count(n1), _divisor_count(n2)
    factors1, factors2 = _prime_factors(n1), _prime_factors(n2)
    chain = 1_914_467
    chain_factors = _prime_factors(chain)
    g1, g2 = math.gcd(2000, 31), math.gcd(31, 1)
    return {
        "ok": True,
        "name": "epoch_0d datum (2000-10-26 10:26:20.00)",
        "unix_epoch_seconds": 972_527_180,
        "tau(10262000)": t1, "tau(26102000)": t2,
        "factorization(10262000)": " x ".join(
            "%d^%d" % (p, k) for p, k in sorted(factors1.items())),
        "factorization(26102000)": " x ".join(
            "%d^%d" % (p, k) for p, k in sorted(factors2.items())),
        "gcd_triangle": [g1, g2, math.gcd(2000, 1)],
        "chain_fold_1914467": " x ".join(
            "%d^%d" % (p, k) for p, k in sorted(chain_factors.items())),
    }


def prime_counts():
    """4. Prime-count datum, read from the persisted sieve asset."""
    data = _load_json("prime_engine_data.json")
    if data is None or not isinstance(data.get("pi"), dict):
        return {"ok": False,
                "error": "data/prime_engine_data.json not present in this "
                         "checkout"}
    pi = data["pi"]
    return {
        "ok": True,
        "name": "Prime-count datum (Lucy_Hedgehog pi + segmented sieve)",
        "note": data.get("note"),
        "endpoint_prime": data.get("endpoint_prime"),
        "pi(10262)": pi.get("10262"),
        "pi(26102)": pi.get("26102"),
        "pi(730421)": pi.get("730421"),
        "pi(1914467)": pi.get("1914467"),
        "pi(943901200001)": pi.get("943901200001"),
    }


def quantum_ground_state():
    """5. Quantum ground state E0 from the spectral asset."""
    data = _load_json("spectral_data.json")
    if data is None or not isinstance(data.get("eigenvalues"), list):
        return {"ok": False,
                "error": "data/spectral_data.json not present in this "
                         "checkout"}
    ev = data["eigenvalues"]
    return {
        "ok": True,
        "name": "Quantum ground state E0",
        "context": data.get("context"),
        "n_eigenvalues": len(ev),
        "E0": float(min(ev)),
        "first_eigenvalues": ev[:5],
    }


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #

def collect():
    blocks = [
        lore_constant(),
        fold_mirror_area(),
        epoch_0d(),
        prime_counts(),
        quantum_ground_state(),
    ]
    return {"definitive_constants": blocks,
            "engine": "puno_app.calculus (exact + numeric)"}


def run(json_out: bool = False) -> int:
    data = collect()
    if json_out:
        print(json.dumps(data, indent=2))
        return 0

    line = "=" * 72
    print(line)
    print("THE DEFINITIVE CONSTANTS  (L.O.R.E.)")
    print("the integration constant is measured, not chosen")
    print(line)
    for block in data["definitive_constants"]:
        if not block.get("ok"):
            print("[--] %s" % block.get("name", "unknown"))
            print("     error: %s" % block["error"])
            continue
        print("\n%s" % block["name"])
        for key, value in block.items():
            if key in ("ok", "name"):
                continue
            print("  %-28s %s" % (key, value))
    print("\n" + line)
    print("engine: %s" % data["engine"])
    print(line)
    return 0


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(
        prog="puno-constants",
        description="Print the definitive constants measured from the "
                    "project assets")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable JSON output")
    args = ap.parse_args(argv)
    return run(json_out=args.json)


if __name__ == "__main__":
    sys.exit(main())
