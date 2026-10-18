"""
Open-status pins for the P1 statement-grade formalizations (roadmap items 4-6)
plus the closed path-drift defect (P2).

These tests pin the HONEST side of each artifact: the finite computations are
recorded, and every claim of resolution is asserted absent.  They are
deliberately string/status pins, not value pins -- the value pins live in
test_solvable_theorems.py.

Run:  python -m pytest test_open_status_pins.py -q
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(
    ROOT, "03_Data_and_Observational_Resources", "02_Experimental_Data_Collections"
)
LEAN_DIR = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus"
)
EXPERIMENTS_DIR = os.path.join(
    ROOT, "02_Experimental_Implementations_and_Verification"
)


def load(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as fp:
        return json.load(fp)


def _lean(rel):
    with open(os.path.join(LEAN_DIR, rel), encoding="utf-8") as fp:
        return fp.read()


def _script(rel):
    with open(os.path.join(EXPERIMENTS_DIR, rel), encoding="utf-8") as fp:
        return fp.read()


def test_p_np_contour_honest_wall_pinned():
    d = load("p_np_contour.json")
    assert (
        "No polynomial-size compilation theorem known for general formulas"
        in d["honest_wall"]
    )
    assert "remains OPEN" in d["key_insight"]
    assert " iff " not in d["key_insight"]


def test_millennium_interpretation_never_claims_resolution():
    d = load("millennium_data.json")
    pnp = d["Q1_p_vs_np"]["p_vs_np"]
    assert pnp["removable_value"] == 0
    assert "remains OPEN" in pnp["interpretation"]
    assert pnp["interpretation"].startswith("consistent with P != NP")

    meanings = {p["name"]: p["meaning"] for p in d["Q3_all_six"]["problems"]}
    for name in (
        "P vs NP",
        "Yang-Mills",
        "Navier-Stokes",
        "Hodge Conjecture",
        "Birch-Swinnerton-Dyer",
    ):
        assert "OPEN" in meanings[name], (name, meanings[name])

    joined = " ".join(meanings.values())
    assert "Smooth solutions exist" not in joined
    assert "Every Hodge class is algebraic" not in joined
    assert "Algebraic rank = analytic rank" not in joined


def test_goldbach_large_is_a_finite_certificate():
    d = load("goldbach_large.json")
    assert d["verification"]["max_n"] == 100000
    assert d["verification"]["even_numbers_tested"] == 49999
    assert d["verification"]["failures"] == 0
    assert "remains OPEN" in d["key_insight"]
    assert "OPEN" in d["honest_wall"]
    last = d["milestones"][-1]
    assert last["n"] == 100000 and last["representations"] == 810


def test_rh_li_correct_is_a_finite_check():
    d = load("rh_li_correct.json")
    assert d["n_max"] == 30 and d["n_zeros"] == 800
    assert d["all_positive"] is True
    assert abs(d["min_lambda"] - 0.02225734932071366) < 1e-15
    script = _script("06_Miscellaneous_Experiments/rh_li_correct.py")
    assert "so RH remains OPEN" in script


def test_lean_open_markers_pinned_and_no_sorry():
    li = _lean("RH/LiCriterion.lean")
    pnp = _lean("PvsNP.lean")
    gb = _lean("Goldbach.lean")

    assert "li_criterion_proof_open : Bool := true" in li
    assert "def liCriterionEquiv" in li
    assert "theorem finitePrefixNeverSettles" in li

    assert "noPolynomialCompilationKnown : Bool := true" in pnp
    assert "theorem compilation_wall_recorded" in pnp

    assert "goldbach_conjecture_open : Bool := true" in gb
    assert "theorem goldbach_even_4_to_100000" in gb

    for src in (li, pnp, gb):
        assert "sorry" not in re.sub(r"`sorry`", "", src)


def test_ledger_artifacts_attach_no_sorry():
    """Gate-D live pin (general): every ``.lean`` artifact named by a ledger
    ``Proof attempt:`` line is real and attaches no ``sorry`` in code.  The only
    permitted occurrence is the literal `` `sorry` `` inside prose/comments."""
    ledger = os.path.join(
        ROOT,
        "05_Documentation_and_Research_Specifications",
        "05_Complete_Framework_Documentation",
        "THE_GAP_LEDGER.md",
    )
    with open(ledger, encoding="utf-8") as fp:
        text = fp.read()
    attempts = [ln for ln in text.splitlines() if "**Proof attempt:**" in ln]
    assert attempts, "no Proof attempt lines in ledger"
    lean = set()
    for ln in attempts:
        lean.update(re.findall(r"[\w./]+\.lean", ln))
    assert len(lean) >= 10, sorted(lean)
    for rel in sorted(lean):
        sub = os.path.relpath(
            rel, "01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus")
        src = _lean(sub.replace("\\", "/"))
        assert "sorry" not in re.sub(r"`sorry`", "", src), rel


def test_path_drift_gates_emit_centrally():
    for rel in (
        "02_Dark_Energy_0_0_Framework/log_limits_0_over_0.py",
        "02_Dark_Energy_0_0_Framework/shannon_entropy_0_over_0.py",
        "02_Dark_Energy_0_0_Framework/prime_number_theorem_0_over_0.py",
        "06_Miscellaneous_Experiments/rh_li_correct.py",
        "06_Miscellaneous_Experiments/p_np_contour.py",
        "06_Miscellaneous_Experiments/goldbach_large.py",
        "06_Miscellaneous_Experiments/goldbach_0_over0.py",
        "06_Miscellaneous_Experiments/gap_prime_gaps_certificate.py",
    ):
        src = _script(rel)
        assert "_central_data_dir()" in src, rel
        assert '"data/' not in src, rel


# --- Gate-D live pins: self-contained finite certificates (Gap Ledger) -------
# These recompute a small, honest finite certificate in-process so the Gap
# Ledger's `certificate`-kind rows are exercised, not merely declared.  Each
# certifies a finite range only; the corresponding conjecture stays OPEN.

def _sieve(limit):
    """Bytearray sieve: index i is 1 iff i is prime, for 0 <= i <= limit."""
    s = bytearray([1]) * (limit + 1)
    s[0] = s[1] = 0
    i = 2
    while i * i <= limit:
        if s[i]:
            s[i * i::i] = bytearray(len(range(i * i, limit + 1, i)))
        i += 1
    return s


def test_collatz_is_a_finite_certificate():
    """Collatz: every n in [2, 10000] reaches 1 (finite range only)."""
    def reaches_one(n):
        while n != 1:
            n = n // 2 if n % 2 == 0 else 3 * n + 1
        return True
    assert all(reaches_one(n) for n in range(2, 10001))


def test_legendre_is_a_finite_certificate():
    """Legendre: a prime lies strictly between n^2 and (n+1)^2, n in [1, 1000]."""
    N = 1000
    s = _sieve((N + 1) * (N + 1))
    for n in range(1, N + 1):
        assert sum(s[m] for m in range(n * n + 1, (n + 1) * (n + 1))) > 0, n


def test_twin_prime_is_a_finite_certificate():
    """Twin primes: the number of pairs (p, p+2) with p <= 10^6 is 8169."""
    X = 10 ** 6
    s = _sieve(X + 2)
    assert sum(1 for p in range(2, X + 1) if s[p] and s[p + 2]) == 8169


def test_goldbach_extended_finite_certificate():
    """Goldbach (extended): every even n in [4, 10^7] has a prime pair.
    This raises the pinned boundary of ``goldbach_large.py`` (10^5) by 100x;
    the strong Goldbach conjecture remains OPEN."""
    X = 10 ** 7
    s = _sieve(X)
    for n in range(4, X + 1, 2):
        for p in range(2, n // 2 + 1):
            if s[p] and s[n - p]:
                break
        else:
            raise AssertionError("no prime pair for %d" % n)


def test_serrin_ladder_ceiling_arithmetic_certificate():
    """G2 pin (arithmetic sub-result): re-check, in CI without Lean, the
    Serrin-ladder arithmetic proved in ``SerrinLadder.lean`` -- the
    Gagliardo-Nirenberg exponent ``theta(p) = 3/2 - 3/p`` satisfies
    ``theta(p) <= 1  iff  p <= 6``, and the closed form
    ``theta(p)*q(p)/2 = 3(p-2)/(2(p-3))`` with ``q(p) = 2p/(p-3)``.  This is
    only the *arithmetic*; the PDE a priori bound (G1/G2) stays OPEN."""
    def theta(p):
        return 1.5 - 3.0 / p
    def serrin_q(p):
        return 2.0 * p / (p - 3.0)
    for p in (1.5, 2.0, 3.0, 4.0, 5.0, 5.999, 6.0):
        assert theta(p) <= 1.0 + 1e-12, p
    for p in (6.001, 7.0, 8.0, 10.0, 100.0):
        assert theta(p) > 1.0, p
    assert abs(theta(6.0) - 1.0) < 1e-12
    for p in (4.0, 5.0, 6.0, 10.0):
        assert abs(theta(p) * serrin_q(p) / 2 - 3 * (p - 2) / (2 * (p - 3))) < 1e-12, p
    assert abs(theta(6.0) * serrin_q(6.0) / 2 - 2.0) < 1e-12


def test_margin_law_admits_scale_family():
    """Gate-D pin for G5 (no-go): the register's margin composition law
    ``f(r*s) = (x+y)/(1+4xy)`` is satisfied by the whole one-parameter family
    ``f = (1/2) tanh(c * log r)`` -- for every real c.  So the law alone does
    NOT single out a unique margin; uniqueness is false (G5)."""
    import math
    def scale(c, r):
        return 0.5 * math.tanh(c * math.log(r))
    r, s = 2.0, 3.0
    for c in (0.1, 0.5, 1.0, 2.0, -0.7):
        x = scale(c, r)
        y = scale(c, s)
        assert abs(scale(c, r * s) - (x + y) / (1 + 4 * x * y)) < 1e-12, c


def test_andrica_is_a_finite_certificate():
    """Andrica: max (sqrt(p_{n+1}) - sqrt(p_n)) < 1 over prime pairs <= 10^7."""
    import math
    limit = 10 ** 7
    s = _sieve(limit)
    ps = [i for i in range(2, limit + 1) if s[i]]
    assert max(math.sqrt(b) - math.sqrt(a) for a, b in zip(ps, ps[1:])) < 1.0


def test_brocard_is_a_finite_certificate():
    """Brocard: >= 4 primes strictly between p_n^2 and p_{n+1}^2, for every n
    whose interval fits in the sieve (n >= 2, limit 10^7)."""
    limit = 10 ** 7
    s = _sieve(limit)
    ps = [i for i in range(2, limit + 1) if s[i]]
    n_done = 0
    for n in range(2, len(ps)):
        a, b = ps[n - 1] ** 2, ps[n] ** 2
        if b > limit:
            break
        assert sum(s[m] for m in range(a + 1, b)) >= 4, n
        n_done += 1
    assert n_done >= 400



