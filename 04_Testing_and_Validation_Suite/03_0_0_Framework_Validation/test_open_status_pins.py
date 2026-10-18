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


def test_gilbreath_is_a_finite_certificate():
    """Gilbreath: the leading term of every row of absolute differences of the
    primes is 1 (checked for the first 2000 primes)."""
    s = _sieve(20000)
    ps = [i for i in range(2, 20001) if s[i]][:2000]
    assert len(ps) == 2000
    row = ps
    rows = 0
    while len(row) > 1:
        row = [abs(row[i + 1] - row[i]) for i in range(len(row) - 1)]
        assert row[0] == 1
        rows += 1
    assert rows == 1999


def test_polignac_is_a_finite_certificate():
    """Polignac: for every even k <= 100 there is a prime pair with gap k
    (existence only, limit 10^6)."""
    limit = 10 ** 6
    s = _sieve(limit)
    for k in range(2, 101, 2):
        assert any(s[p] and s[p + k] for p in range(2, limit - k + 1)), k


def test_sophie_germain_is_a_finite_certificate():
    """Sophie Germain primes (p with 2p+1 prime): count up to 10^6 is 4324."""
    limit = 10 ** 6
    s = _sieve(limit)
    cnt = sum(1 for p in range(2, limit + 1)
              if s[p] and 2 * p + 1 <= limit and s[2 * p + 1])
    assert cnt == 4324


def test_zero_over_zero_need_not_resolve():
    """G21 no-go: the register's C15 uniqueness of the removable value is
    *conditional on existence* of the punctured limit.  The classic 0/0
    ``f(x,y) = xy/(x^2+y^2)`` has no limit at the origin -- along distinct rays
    it tends to distinct values -- so no removable value exists.  Uniqueness
    cannot be strengthened to unconditional existence."""
    def f(x, y):
        return x * y / (x * x + y * y)
    vals = {m: f(1.0, m) for m in (0.0, 0.5, 1.0, 2.0, -1.0)}
    assert abs(vals[0.0] - 0.0) < 1e-12
    assert abs(vals[1.0] - 0.5) < 1e-12
    assert abs(vals[2.0] - 0.4) < 1e-12
    assert len({round(v, 12) for v in vals.values()}) >= 4


def test_fermat_numbers_is_a_finite_certificate():
    """Fermat numbers: F_0..F_4 = 3, 5, 17, 257, 65537 are prime; F_5 is
    composite (641 | F_5).  Infinitude of Fermat primes stays OPEN."""
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
    for k in (0, 1, 2, 3, 4):
        assert isprime((1 << (1 << k)) + 1), k
    f5 = (1 << (1 << 5)) + 1
    assert f5 == 4294967297 and f5 % 641 == 0


def test_landau_n2_plus_1_is_a_finite_certificate():
    """Landau: primes of the form n^2+1; exactly 112 for n <= 1000."""
    s = _sieve(10 ** 6 + 1)
    cnt = sum(1 for n in range(0, 1001) if s[n * n + 1])
    assert cnt == 112


def test_euler_polynomial_no_go():
    """No-go: 'n^2+n+41 is prime for all n>=0' is false.  Prime for n=0..39,
    composite at n=40 (1681 = 41^2)."""
    def isprime(n):
        if n < 2:
            return False
        i = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i += 1
        return True
    assert all(isprime(n * n + n + 41) for n in range(0, 40))
    v = 40 * 40 + 40 + 41
    assert v == 1681 and v == 41 * 41 and not isprime(v)


def test_bridge_statement_grade_classification_certificate():
    """G3 sub-result: MillenniumBridge.lean machine-checks the *statement-grade*
    classification (seven problems declared unsolved; adjacent classifications),
    not the missing constructivity."""
    src = _lean("MillenniumBridge.lean")
    for name in ("seven_problems_declared_unsolved",
                 "pnnp_adjacent_classification",
                 "pnnp_adjacent_isometry_count",
                 "rh_adjacent_finite_sector"):
        assert ("theorem " + name) in src, name


def test_ternary_goldbach_citation_recorded():
    """G25: the register relies on Helfgott's ternary Goldbach theorem, cited
    but not formalized in-repo; the citation must be recorded."""
    ledger = os.path.join(
        ROOT, "05_Documentation_and_Research_Specifications",
        "05_Complete_Framework_Documentation", "THE_GAP_LEDGER.md")
    with open(ledger, encoding="utf-8") as fp:
        assert "Helfgott" in fp.read()


def test_ns_wall_markers_pinned():
    """G1 sub-result pin: NavierStokes.lean carries the open-wall markers
    (global regularity OPEN; Prodi-Serrin integral NOT certified) plus the
    Fourier bound -- the register does not claim to have closed NS."""
    src = _lean("NavierStokes.lean")
    assert "nsGlobalRegularityOpen : Bool := true" in src
    assert "prodiSerrinIntegralFiniteCertified : Bool := false" in src
    assert "theorem ns_global_regularity_wall_open" in src
    assert "def fourierInfBound" in src


def test_bsd_rank_records_pinned():
    """G6 sub-result pin: BSD.lean records the rank ladder [0,0,1,2] and the
    matching conductors, without claiming a general rank>=2 theorem."""
    src = _lean("BSD.lean")
    assert "def curve_rank : List Nat := [0, 0, 1, 2]" in src
    assert "def curve_conductor : List Nat := [11, 14, 37, 389]" in src
    assert "def verifyAll : Bool" in src


def test_hodge_quintic_open_marker_pinned():
    """G7 sub-result pin: Hodge.lean marks the quintic (2,1) codimension-2
    classes as genuinely open."""
    src = _lean("Hodge.lean")
    assert "def quintic_codim2_open : Bool := true" in src


def test_massgap_crossover_pinned():
    """G11 sub-result pin: MassGap.lean carries the crossover fact
    (a/sinh a -> 1) and the positivity check, without claiming a 4D proof."""
    src = _lean("MassGap.lean")
    assert "def verifyMassGapPositive : Bool" in src
    assert "theorem massGapCrossoverRemovable" in src
    assert "theorem sinh_div_self_tendsto_one" in src


def test_information_phi_markers_pinned():
    """G4 content pin: InformationPhi.lean formalizes the register's Phi model
    (free-ratio, entropy-production, erase-cost, Landauer bit) -- the missing
    object is the *empirical operational* anchor, not the formal side."""
    src = _lean("InformationPhi.lean")
    assert "def Phi (kB T :" in src
    assert "theorem Phi_freeRatio_eq_exp_neg_lambda" in src
    assert "theorem Phi_bit_eraseCost" in src
    assert "theorem Phi_satisfies_claim" in src
    assert "def informationPhiFacts : List String" in src
    assert "theorem informationPhiFacts_length : informationPhiFacts.length = 9" in src


def test_oppermann_is_a_finite_certificate():
    """Oppermann: for every n >= 2 with (n+1)^2 inside the sieve, a prime lies
    strictly between n^2 and n(n+1), and one between n(n+1) and (n+1)^2."""
    limit = 10 ** 7
    s = _sieve(limit)
    n_done = 0
    for n in range(2, 4000):
        a, b, c = n * n, n * (n + 1), (n + 1) * (n + 1)
        if c > limit:
            break
        assert any(s[m] for m in range(a + 1, b)), n
        assert any(s[m] for m in range(b + 1, c)), n
        n_done += 1
    assert n_done >= 3000


def test_prime_constellations_is_a_finite_certificate():
    """Prime k-tuples (Dickson-type): each admissible constellation has a
    smallest start whose shifted values are all prime -- twin (3,5), triplet
    (5,7,11), quadruplet (5,7,11,13), quintuplet (5..17), sextuplet (7..23).
    Existence only; infinitude (Dickson) stays OPEN."""
    limit = 10 ** 6
    s = _sieve(limit)

    def smallest(pat):
        for p in range(2, limit - pat[-1] + 1):
            if all(s[p + d] for d in pat):
                return p
        return None

    assert smallest((0, 2)) == 3
    assert smallest((0, 2, 6)) == 5
    assert smallest((0, 2, 6, 8)) == 5
    assert smallest((0, 2, 6, 8, 12)) == 5
    assert smallest((0, 4, 6, 10, 12, 16)) == 7


def test_odd_perfect_numbers_no_small_certificate():
    """Odd perfect numbers: even perfect numbers <= 10^6 are exactly
    {6, 28, 496, 8128} (Euclid-Euler); no odd perfect number exists <= 10^6.
    Existence/non-existence in general stays OPEN."""
    limit = 10 ** 6
    sig = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for m in range(d, limit + 1, d):
            sig[m] += d
    even = [n for n in range(2, limit + 1, 2) if sig[n] == 2 * n]
    odd = [n for n in range(3, limit + 1, 2) if sig[n] == 2 * n]
    assert even == [6, 28, 496, 8128]
    assert odd == []


def test_mersenne_primes_is_a_finite_certificate():
    """G29: exact Lucas-Lehmer certificate -- prime exponents p <= 2000 with
    2^p - 1 prime are exactly [2,3,5,7,13,17,19,31,61,89,107,127,521,607,1279].
    Infinitude of Mersenne primes stays OPEN."""
    def isp(n):
        if n < 2:
            return False
        i = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i += 1
        return True
    found = []
    for p in range(2, 2001):
        if not isp(p):
            continue
        if p == 2:
            found.append(p)
            continue
        m = (1 << p) - 1
        s = 4
        for _ in range(p - 2):
            s = (s * s - 2) % m
        if s == 0:
            found.append(p)
    assert found == [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127,
                     521, 607, 1279]


def _load_gap_row_forge():
    import importlib.util
    path = os.path.join(
        ROOT, "02_Experimental_Implementations_and_Verification",
        "06_Miscellaneous_Experiments", "gap_row_forge.py")
    spec = importlib.util.spec_from_file_location("_gap_row_forge", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_gap_row_forge_emits_gate_valid_rows():
    """G28: the row forge turns a claimed proof attempt into a Gate-D-valid row
    and refuses illegal kinds, missing artifacts, and fake pins; it never emits
    a resolved/DONE status."""
    import pytest
    forge = _load_gap_row_forge()
    row = forge.forge_row(
        subject="Synthetic self-test gap",
        kind="certificate",
        artifact="02_Experimental_Implementations_and_Verification/"
                 "06_Miscellaneous_Experiments/gap_row_forge.py",
        pin="test_gap_row_forge_emits_gate_valid_rows")
    assert forge.validate_row(row) == []
    assert "TODO" in row and "DONE" not in row
    assert forge.next_token("## G1 - a\n## G2 - b\n") == "G3"

    with pytest.raises(ValueError):
        forge.forge_row(subject="x", kind="proved", artifact="n/a", pin="n/a")
    with pytest.raises(ValueError):
        forge.forge_row(subject="x", kind="certificate",
                        artifact="does/not/exist.py",
                        pin="test_gap_row_forge_emits_gate_valid_rows")
    with pytest.raises(ValueError):
        forge.forge_row(subject="x", kind="certificate",
                        artifact="01_Core_Mathematical_Framework_Lean/"
                                 "01_Lean/PunoCalculus/Hodge.lean",
                        pin="test_no_such_pin_exists_anywhere")


def test_gap_row_forge_applies_end_to_end(tmp_path):
    """G28: the forge closes the loop -- scaffold artifact + pin, then append a
    Gate-D-valid row carrying the next G-number (all in a throwaway root)."""
    forge = _load_gap_row_forge()
    root = str(tmp_path)
    ledger_path = tmp_path / forge.LEDGER_REL
    os.makedirs(os.path.dirname(str(ledger_path)), exist_ok=True)
    ledger_path.write_text("## G1 - seed\n- **Proof attempt:** no-go - n/a\n",
                           encoding="utf-8")
    tests_dir = tmp_path / forge.TESTS_DIR_REL
    os.makedirs(str(tests_dir), exist_ok=True)
    (tests_dir / "test_demo.py").write_text(
        "def test_seed():\n    assert True\n", encoding="utf-8")

    report = forge.apply(
        subject="Demo certificate",
        kind="certificate",
        artifact_rel="exp/demo_cert.py",
        pin="test_demo_certificate",
        tests_file_rel=forge.TESTS_DIR_REL + "/test_demo.py",
        root=root)
    assert report["token"] == "G2"
    assert report["created_artifact"] and report["created_pin"]
    assert os.path.exists(os.path.join(root, "exp", "demo_cert.py"))
    assert "## G2 - Demo certificate" in report["ledger"]
    assert forge.validate_row(report["row"]) == []





def test_giuga_is_a_finite_certificate():
    """G30: an exact search finds no counterexample to Giuga's conjecture below
    10**5 -- the four Giuga numbers there (30, 858, 1722, 66198) are each
    non-Carmichael, so Giuga's conjecture (equivalently, no number is both a
    Giuga and a Carmichael number) holds to the bound and stays OPEN beyond it.
    """
    import importlib.util
    path = os.path.join(
        ROOT, "02_Experimental_Implementations_and_Verification",
        "06_Miscellaneous_Experiments", "giuga_certificate.py")
    spec = importlib.util.spec_from_file_location("_giuga_cert", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    nums = mod.giuga_numbers(10 ** 5)
    assert [n for n, _, _ in nums] == [30, 858, 1722, 66198]
    assert all(c is False for _, _, c in nums)
    assert mod.is_giuga(30, [(2, 1), (3, 1), (5, 1)]) is True
    assert mod.is_giuga(6, [(2, 1), (3, 1)]) is False
    assert mod.is_carmichael(561, [(3, 1), (11, 1), (17, 1)]) is True


def test_lehmer_totient_is_a_finite_certificate():
    """G31: no composite n <= 10**6 has phi(n) | (n - 1), so Lehmer's totient
    conjecture (no composite n with phi(n) | (n - 1)) holds to the bound and
    stays OPEN beyond it; the 2-Lehmer relaxation phi(n) | (n - 1)^2 gives the
    first Carmichael numbers, so the relaxation is strictly weaker."""
    import importlib.util
    path = os.path.join(
        ROOT, "02_Experimental_Implementations_and_Verification",
        "06_Miscellaneous_Experiments", "lehmer_totient_certificate.py")
    spec = importlib.util.spec_from_file_location("_lehmer_cert", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert mod.lehmer_composites(10 ** 6) == []
    two = [d["n"] for d in mod.two_lehmer_numbers(10 ** 4)]
    assert two == [561, 1105, 1729, 2465, 6601, 8481]
    phi = mod.totient_sieve(600)
    assert phi[561] == 320 and phi[561] != 560


def test_wieferich_primes_is_a_finite_certificate():
    """G32: exact search shows 1093 and 3511 are the only Wieferich primes base 2
    below 10**6; infinitude stays OPEN."""
    import importlib.util
    path = os.path.join(
        ROOT, "02_Experimental_Implementations_and_Verification",
        "06_Miscellaneous_Experiments", "wieferich_certificate.py")
    spec = importlib.util.spec_from_file_location("_wieferich_cert", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert mod.wieferich_primes(10 ** 6) == [1093, 3511]
    assert mod.is_wieferich(1093) is True
    assert mod.is_wieferich(3511) is True
    assert mod.is_wieferich(3) is False
    assert pow(2, 1092, 1093 * 1093) == 1
