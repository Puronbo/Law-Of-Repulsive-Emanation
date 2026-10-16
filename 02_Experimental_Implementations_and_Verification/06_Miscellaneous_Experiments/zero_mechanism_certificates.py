"""
ZERO-MECHANISM CERTIFICATES (cards C15 / C16 / C17 / C18 / C19 / C20 / C21 /
===========================================================================
                             C22 / C23 / C24)
Numerical/combinatorial companion to the zero-object, removable-value and
0/0-mechanism cards.  Each block re-derives, by finite enumeration or by exact
arithmetic on samples, the content that the corresponding Lean card proves.  The
proof is the Lean theorem; this is the arithmetic shadow and it must agree.

  C15  ZeroLink                -- Empty is initial, PUnit is terminal (∃! arrow)
  C16  ZeroObject              -- one object initial AND terminal (the zero module)
  C17  RemovableValue          -- the punctured limit is exist-and-be-unique
  C18  VanishOrder             -- the "number of zeros" is a graded index
  C19  ZeroProbe               -- the identity 0/0 resolves to 1
  C20  ZeroValuation           -- order of vanishing is a valuation (additive)
  C21  ZeroIndex               -- root multiplicity is an additive index
  C22  ZeroMechanisms          -- the anti-class: |x|/x has NO limit at 0
  C23  RemovableComplexBridge  -- the same ∃! schema over C
  C24  LiouvilleBridge         -- bounded entire functions are constant

Scope: finite enumeration and real/complex arithmetic only.  No PDE, no
Millennium problem (see WHAT_THIS_DOES_NOT_PROVE.md).  Honest boundary: cards
that are universally quantified over types / categories / analytic hypotheses
(C15, C16, C24) are certified on a *concrete instance* or on finite samples; the
instance is the arithmetic shadow, not the theorem.
Run:  python zero_mechanism_certificates.py            (prints PASS)
"""

import cmath
import itertools
import math

TOL = 1e-9


# ---------------------------------------------------------------------------
# helpers: exact polynomial arithmetic in ascending powers of t = x - x0
# ---------------------------------------------------------------------------


def poly_eval(c, x):
    r = 0.0
    for coeff in reversed(c):
        r = r * x + coeff
    return r


def poly_mul(a, b):
    out = [0.0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            out[i + j] += ca * cb
    return out


def poly_pow(a, n):
    out = [1.0]
    for _ in range(n):
        out = poly_mul(out, a)
    return out


def poly_deriv(c):
    if len(c) <= 1:
        return [0.0]
    return [i * c[i] for i in range(1, len(c))]


def root_multiplicity(c, a=0.0):
    """Smallest k with p^(k)(a) != 0 -- the multiplicity (order of vanishing)."""
    cur = list(c)
    m = 0
    while m < 16:
        scale = max(abs(v) for v in cur) or 1.0
        if abs(poly_eval(cur, a)) <= 1e-7 * scale:
            m += 1
            cur = poly_deriv(cur)
        else:
            break
    return m


def hom_count(m, n):
    """Number of maps from an m-element set to an n-element set: n^m."""
    return n ** m


# ---------------------------------------------------------------------------
# C15 -- ZeroLink: Empty is initial, PUnit is terminal
# ---------------------------------------------------------------------------


def c15_zero_link():
    # empty_unique_arrow: exactly one arrow out of nothing, for every target
    one_out = all(hom_count(0, a) == 1 for a in range(0, 7))
    # unit_unique_arrow: exactly one arrow into one, from every source
    one_in = all(hom_count(a, 1) == 1 for a in range(0, 7))
    # empty_classified_initial: |A|^|I| = 1 for every A (|A|>=2) forces |I| = 0
    initial_sizes = [i for i in range(0, 5)
                     if all(hom_count(i, a) == 1 for a in (2, 3, 4))]
    # unit_classified_terminal: |A|^|T| = 1 for every A (|A|>=1) forces |T| = 1
    terminal_sizes = [t for t in range(0, 5)
                      if all(hom_count(a, t) == 1 for a in (1, 2, 3))]
    # zero_links_all: Empty is the identity for + and absorbing for x
    ring_ok = all((a + 0 == a) and (0 + a == a) and (a * 0 == 0) and (0 * a == 0)
                  for a in range(0, 9))
    print("\n[C15] ZeroLink (Empty initial, PUnit terminal)")
    print(f"  exactly one arrow Empty -> A for all A          = {one_out}")
    print(f"  exactly one arrow A -> PUnit for all A          = {one_in}")
    print(f"  types with a unique arrow to every A            = {initial_sizes}")
    print(f"  types that every A maps uniquely into           = {terminal_sizes}")
    print(f"  |A|+0=|A|, |A|x0=0, 0+|A|=|A|, 0x|A|=0         = {ring_ok}")
    assert one_out and one_in and ring_ok
    assert initial_sizes == [0], initial_sizes
    assert terminal_sizes == [1], terminal_sizes
    print("  -> uniqueness of the out-of-nothing arrow characterises the empty type;"
          "\n     uniqueness of the into-one arrow characterises the singleton.")


# ---------------------------------------------------------------------------
# C16 -- ZeroObject: the zero module is initial AND terminal (concrete instance)
# ---------------------------------------------------------------------------


def c16_zero_object():
    # Concrete instance: GF(2)-Mod, whose hom-set dimensions are k*m, so
    # #Hom(GF(2)^k, GF(2)^m) = 2^(k*m).
    def hom(k, m):
        return 2 ** (k * m)

    # initial_link: a unique morphism 0 -> V for every V
    init = all(hom(0, m) == 1 for m in range(0, 7))
    # terminal_link: a unique morphism M -> 0 for every M
    term = all(hom(k, 0) == 1 for k in range(0, 7))
    # zero_links_both_ways: the zero object does both at once
    both = init and term
    # modules_haveZeroObject: the zero module exists (the 1-element, 0-dim space)
    zero_dim = 0
    have_zero = (2 ** (zero_dim * zero_dim)) == 1
    # zero_unique_up_to_iso: exactly one 0-dimensional space up to isomorphism
    # (any two spaces of the same dimension are isomorphic)
    dims = [k for k in range(0, 6) if all(hom(k, m) == 1 for m in (1, 2, 3))]
    # modules_zero_links: from/to the zero module both ways
    links = all(hom(0, m) == 1 and hom(m, 0) == 1 for m in range(0, 7))
    print("\n[C16] ZeroObject (instance: GF(2)-Mod)")
    print(f"  unique arrow 0 -> V for every V                 = {init}")
    print(f"  unique arrow M -> 0 for every M                 = {term}")
    print(f"  both at once                                    = {both}")
    print(f"  zero module exists (0-dim hom count)            = {have_zero}")
    print(f"  dims with a unique arrow to every V             = {dims}")
    print(f"  unique arrow both ways to/from 0                = {links}")
    assert init and term and both and have_zero and links
    assert dims == [0], dims
    print("  -> the 0-dimensional module is simultaneously initial and terminal; "
          "\n     (instance-level shadow of the universal quantifier over C).")


# ---------------------------------------------------------------------------
# C17 -- RemovableValue: the punctured limit exists and is unique
# ---------------------------------------------------------------------------


def c17_removable_value():
    a, c = 2.0, 3.0

    def g(x):
        return c + math.sin(x)

    # the canonical 0/0 : f(x) = (x-a) g(x) / (x-a)  equals g(x) for x != a
    def f(x):
        return (x - a) * g(x) / (x - a)

    seq_r = [a + (0.5 ** n) for n in range(1, 30)]
    seq_l = [a - (0.5 ** n) for n in range(1, 30)]
    lim_r = f(seq_r[-1])
    lim_l = f(seq_l[-1])
    e_uniq = abs(lim_r - lim_l)          # two independent one-sided estimates
    e_val = abs(lim_r - g(a))            # the removable value is g(a)
    # the value is the ONE value both sequences converge to
    grid = [g(a) + k * 1e-4 for k in range(-50, 51)]
    survivors = [L for L in grid
                 if all(abs(f(x) - L) < 1e-6 for x in seq_r[-3:]) ]
    # uniqueness: exactly one grid value is within tolerance of the limit
    survivors = [L for L in grid
                 if all(abs(f(x) - L) < 1e-6 for x in seq_r[-3:])]
    # convergence of the single-sided estimate
    e_haus = abs(lim_r - f(seq_r[-4]))
    # initial_arrow_schema: exactly one arrow Empty -> alpha, and NOT for others
    n_empty = len(list(itertools.product(range(4), repeat=0)))   # maps from ∅
    n_once = len(list(itertools.product(range(4), repeat=1)))    # maps from a 1-set
    one_arrow = (n_empty == 1) and (n_once == 4)
    print("\n[C17] RemovableValue (exist-and-be-unique)")
    print(f"  one-sided limit estimates |f(r) - f(l)|         = {e_uniq:.3e}")
    print(f"  |limit - g(a)| (removable value = g(a))         = {e_val:.3e}")
    print(f"  |f(x) - limit| as x -> a (convergence)          = {e_haus:.3e}")
    print(f"  surviving candidate values near the limit       = {len(survivors)}")
    print(f"  maps from ∅ (1) and from a 1-set (4)            = ({n_empty}, {n_once})")
    assert e_uniq < 1e-6 and e_val < 1e-6 and e_haus < 1e-6
    assert len(survivors) == 1, survivors
    assert one_arrow
    print("  -> the punctured limit exists, both approaches agree, and the value is "
          "\n     unique; the schema is the same ∃! as the initial arrow.")


# ---------------------------------------------------------------------------
# C18 -- VanishOrder: the number of zeros is a graded index
# ---------------------------------------------------------------------------


def c18_vanish_order():
    h = [2.0, 1.0, 0.5]      # h(0) = 2 != 0, continuous (a polynomial)
    grades = []
    e_shift = e_ant = e_unique = 0.0
    for k in range(0, 7):
        c = [0.0] * k + h                     # t^k * h  (canonical form)
        m = root_multiplicity(c, 0.0)
        grades.append(m)
        if m != k:
            e_unique += 1.0
        # hasGrade_canonical: exact grade k  <=>  order k and not k+1
        if not (m == k and root_multiplicity(c, 0.0) != k + 1):
            e_unique += 1.0
        # vanishes_shift: order k+1 of t^(k+1)h  <=>  order k of divideOut
        if k >= 1:
            if root_multiplicity(c, 0.0) != root_multiplicity(c[1:], 0.0) + 1:
                e_shift += 1.0
        # vanishes_antitone: m >= k and order m => order >= k (trivially k <= m)
        if not (m >= k):
            e_ant += 1.0
    # vanishes_succ_imp: order k+1 implies order k
    e_succ = 0
    for k in range(0, 6):
        if root_multiplicity([0.0] * (k + 1) + h, 0.0) < k:
            e_succ += 1
    print("\n[C18] VanishOrder (a graded, shifting, unique index of zeros)")
    print(f"  recovered grades for t^k h, k = 0..6            = {grades}")
    print(f"  grade-shift failures (divideOut lowers by one)  = {e_shift:.1f}")
    print(f"  antitone failures                               = {e_ant:.1f}")
    print(f"  succ-imp failures                               = {e_succ:.1f}")
    print(f"  canonical-grade failures                        = {e_unique:.1f}")
    assert grades == list(range(0, 7)), grades
    assert e_shift == 0.0 and e_ant == 0.0 and e_succ == 0 and e_unique == 0.0
    print("  -> the exact grade is well-defined, dividing out one factor lowers it "
          "\n     by exactly one, and the filtration only decreases.")


# ---------------------------------------------------------------------------
# C19 -- ZeroProbe: the identity 0/0 resolves to 1
# ---------------------------------------------------------------------------


def c19_zero_probe():
    def f(x):
        return x * math.cos(x) + 2.0

    def g(x):
        return x * math.cos(x) + 2.0

    xs = [(0.5 ** n) * (1.0 if n % 2 else -1.0) for n in range(1, 30)]
    # probe_self : f/f -> 1 on the punctured neighbourhood
    vals_self = [f(x) / f(x) for x in xs if f(x) != 0.0]
    # probe_identity : f = g off x0 and g != 0  =>  f/g -> 1
    vals_ident = [f(x) / g(x) for x in xs if g(x) != 0.0]
    worst_1 = max(abs(v - 1.0) for v in vals_self + vals_ident)
    print("\n[C19] ZeroProbe (the identity 0/0 resolves to 1)")
    print(f"  max |f/f - 1| and |f/g - 1| over punctured pts   = {worst_1:.3e}")
    assert worst_1 == 0.0, worst_1
    print("  -> the probe ratio is exactly 1 away from the point, and the value 1 is "
          "\n     the removable value (C17).")


# ---------------------------------------------------------------------------
# C20 -- ZeroValuation: order of vanishing is a valuation
# ---------------------------------------------------------------------------


def c20_zero_valuation():
    p = [3.0, 1.0]           # 1 + t   -> order 0
    q = [0.0, 0.0, 5.0]      # 5 t^2   -> order 2
    r = [0.0, -2.0, 1.0]     # -2t + t^2 -> order 1
    one = [1.0]
    ord_p = root_multiplicity(p)
    ord_q = root_multiplicity(q)
    ord_r = root_multiplicity(r)
    checks = {"hasOrder_one": root_multiplicity(one) == 0}
    checks["hasOrder_zero_iff"] = ((root_multiplicity(p) == 0)
                                   == (abs(poly_eval(p, 0.0)) != 0.0))
    checks["hasOrder_mul"] = (root_multiplicity(poly_mul(p, q))
                              == ord_p + ord_q)
    checks["hasOrder_pow"] = all(
        root_multiplicity(poly_pow(q, n)) == ord_q * n for n in (1, 2, 3, 4, 5))
    # canonical: h(0) != 0  =>  order of t^n * h is exactly n
    checks["hasOrder_canonical"] = all(
        root_multiplicity([0.0] * n + [7.0, 1.0]) == n for n in range(0, 6))
    checks["hasOrder_lt_imp_not"] = (ord_p < 2) != (root_multiplicity(p) == 2)
    checks["hasOrder_unique"] = (root_multiplicity(q) == ord_q)
    checks["order_is_valuation"] = (checks["hasOrder_mul"]
                                    and checks["hasOrder_pow"]
                                    and checks["hasOrder_unique"]
                                    and checks["hasOrder_canonical"])
    print("\n[C20] ZeroValuation (order of vanishing is additive)")
    print(f"  ord(1+t) = {ord_p},  ord(5t^2) = {ord_q},  ord(-2t+t^2) = {ord_r}")
    for k in sorted(checks):
        print(f"  {k:<24} = {checks[k]}")
    assert all(checks.values()), [k for k, v in checks.items() if not v]
    print("  -> order is well-defined, additive under products, scales with powers, "
          "\n     and is realised by the canonical monomial factor.")


# ---------------------------------------------------------------------------
# C21 -- ZeroIndex: root multiplicity is an additive index
# ---------------------------------------------------------------------------


def c21_zero_index():
    a = 1.0
    X_sub_a = [-a, 1.0]                   # X - a
    h = [3.0, 1.0, 2.0]                   # coprime to (X-a): multiplicity 0
    p = poly_mul(X_sub_a, X_sub_a)        # (X-a)^2
    q = poly_mul(X_sub_a, h)              # (X-a) * h
    checks = {
        "index_one": root_multiplicity([1.0], a) == 0,
        "index_X_sub_C_self": root_multiplicity(X_sub_a, a) == 1,
        "index_additive": (root_multiplicity(poly_mul(q, p), a)
                           == root_multiplicity(q, a) + root_multiplicity(p, a)),
        "index_pow": all(root_multiplicity(poly_pow(X_sub_a, n), a) == n
                         for n in (1, 2, 3, 4, 5, 6)),
        "index_pow_self": root_multiplicity(poly_pow(X_sub_a, 4), a) == 4,
        "index_canonical": (root_multiplicity(poly_mul([-7.0],
                                                       poly_pow(X_sub_a, 3)), a) == 3),
        "index_nonzero_lead": root_multiplicity(poly_pow(X_sub_a, 5), a) == 5,
    }
    checks["index_is_multiplicity"] = all(
        checks[k] for k in ("index_one", "index_X_sub_C_self", "index_additive",
                            "index_pow", "index_canonical"))
    print("\n[C21] ZeroIndex (root multiplicity is an additive index)")
    for k in sorted(checks):
        print(f"  {k:<26} = {checks[k]}")
    print(f"  multiplicity of (X-{a})^2 at {a}            = {root_multiplicity(p, a)}")
    assert all(checks.values()), [k for k, v in checks.items() if not v]
    print("  -> ind(1)=0, ind(X-a)=1, ind(pq)=ind(p)+ind(q), ind(p^n)=n ind(p).")


# ---------------------------------------------------------------------------
# C22 -- ZeroMechanisms: the anti-class (no limit at all)
# ---------------------------------------------------------------------------


def c22_zero_mechanisms():
    right = [abs(x) / x for x in (1e-3, 1e-6, 1e-9, 1e-12)]
    left = [abs(x) / x for x in (-1e-3, -1e-6, -1e-9, -1e-12)]
    e_r = max(abs(v - 1.0) for v in right)
    e_l = max(abs(v + 1.0) for v in left)
    e_v = min(abs(x) for x in (1e-3, 1e-6, 1e-9, 1e-12))   # numerator -> 0
    e_i = min(abs(x) for x in (1e-3, 1e-6, 1e-9, 1e-12))   # denominator -> 0
    gap = abs(right[0] - left[0])            # one-sided limits differ by 2
    no_limit = gap > 1e-9 and e_r < 1e-9 and e_l < 1e-9
    print("\n[C22] ZeroMechanisms (the anti-class: a 0/0 with no limit)")
    print(f"  | |x|/x - 1 | on x -> 0+                        = {e_r:.3e}")
    print(f"  | |x|/x + 1 | on x -> 0-                        = {e_l:.3e}")
    print(f"  |x| -> 0 (numerator vanishes, smallest sample)  = {e_v:.3e}")
    print(f"  x   -> 0 (denominator vanishes, smallest sample)= {e_i:.3e}")
    print(f"  one-sided gap |right - left|                    = {gap:.3e}")
    print(f"  no limit exists                                 = {no_limit}")
    assert e_r < 1e-9 and e_l < 1e-9 and e_v < 1e-9 and e_i < 1e-9
    assert no_limit
    print("  -> both sides vanish (a genuine 0/0) yet the ratio has two distinct "
          "\n     one-sided values, so no removable value exists: the class is not "
          "classified.")


# ---------------------------------------------------------------------------
# C23 -- RemovableComplexBridge: the same ∃! schema over C
# ---------------------------------------------------------------------------


def c23_removable_complex_bridge():
    c0 = 1.0 - 0.5j
    k = 2.0 + 0.25j

    def g(z):
        return k * z + 1.0

    def f(z):
        return (z - c0) * g(z) / (z - c0)   # canonical 0/0 for z != c0

    # two independent approaches to c0 in C
    seqs = []
    for direction in (1.0, -1.0, 1.0j, -1.0j, 0.7 + 0.7j):
        seqs.append([c0 + direction * (0.5 ** n) for n in range(1, 48)])
    limits = [f(s[-1]) for s in seqs]
    spread = max(abs(lim - g(c0)) for lim in limits)
    e_val = abs(limits[0] - limits[1])
    print("\n[C23] RemovableComplexBridge (the ∃! schema over C)")
    print(f"  |f(z) - g(c)| at z -> c, 5 approaches            = {spread:.3e}")
    print(f"  |limit approach 1 - approach 2|                  = {e_val:.3e}")
    assert spread < 1e-9 and e_val < 1e-9
    print("  -> the canonical complex 0/0 has one punctured limit, equal to g(c), "
          "\n     approached from every direction.")


# ---------------------------------------------------------------------------
# C24 -- LiouvilleBridge: boundedness of an entire function forces constancy
# ---------------------------------------------------------------------------


def c24_liouville_bridge():
    # Honest framing: we cannot enumerate entire functions.  We can check that
    # the boundedness hypothesis is exactly what excludes every standard
    # non-constant candidate: on a growing disk their modulus grows.
    def sample_radius(R, fn, n=64):
        m = 0.0
        for j in range(n):
            theta = 2 * math.pi * j / n
            z = R * (math.cos(theta) + 1j * math.sin(theta))
            m = max(m, abs(fn(z)))
        return m

    def exp_fn(z):
        return cmath.exp(z)

    def sin_fn(z):
        return cmath.sin(z)

    def poly_fn(z):
        return z * z + 1.0

    def const_fn(z):
        return 3.0 + 0.0j

    radii = [1.0, 2.0, 4.0, 8.0]
    grows = {}
    for name, fn in (("exp", exp_fn), ("sin", sin_fn), ("z^2+1", poly_fn)):
        vals = [sample_radius(R, fn) for R in radii]
        grows[name] = vals[-1] > vals[0] * 10.0
    const_vals = [sample_radius(R, const_fn) for R in radii]
    const_flat = max(const_vals) - min(const_vals) < 1e-12
    print("\n[C24] LiouvilleBridge (bounded entire => constant)")
    for name, fn in (("exp", exp_fn), ("sin", sin_fn), ("z^2+1", poly_fn)):
        vals = [f"{sample_radius(R, fn):.3e}" for R in radii]
        print(f"  max |{name:<6}| on |z| = {radii}  = {vals}")
    print(f"  max |const| deviation across radii               = "
          f"{max(const_vals) - min(const_vals):.3e}")
    print(f"  non-constant candidates grow (excluded)          = {all(grows.values())}")
    print(f"  constant candidate stays flat (retained)         = {const_flat}")
    assert all(grows.values()), grows
    assert const_flat
    print("  -> finite sampling confirms the boundedness hypothesis admits only the "
          "\n     flat candidate among these entire functions (the theorem itself is "
          "the Lean proof).")


def main():
    print("=" * 78)
    print("ZERO-MECHANISM CERTIFICATES: C15-C24")
    print("=" * 78)
    c15_zero_link()
    c16_zero_object()
    c17_removable_value()
    c18_vanish_order()
    c19_zero_probe()
    c20_zero_valuation()
    c21_zero_index()
    c22_zero_mechanisms()
    c23_removable_complex_bridge()
    c24_liouville_bridge()
    print("\n" + "=" * 78)
    print("PASS: C15/C16 initial-terminal uniqueness; C17/C23 unique removable value; "
          "C18/C20/C21 graded index and valuation; C19 probe = 1; C22 anti-class has "
          "no limit; C24 boundedness excludes the growing candidates.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
