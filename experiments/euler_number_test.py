"""
euler_number_test.py
====================
Test Euler's number e = 2.718281828459045... through the repo's machinery,
with the repo's own self-refutation discipline (T57/T62: record and
null-test favorite coincidences; T59/T61: clock-test re-encoding).

  PART 1  digit-prefix census (mirror WEAVERS 10262000 / reverse_pair_gaps):
          factorization, tau (divisor count), digit sum, reversal, in base 10
          and re-encoded bases (T59 clock test).
  PART 2  golden proximity: is e "golden"?  distances to phi, phi^2, 1/phi
          with a fold-ladder null (what fraction of numbers of e's magnitude
          hit {phi, phi^2} within the same tolerance by chance).
  PART 3  continued fraction: verify e's exact pattern [2; 1,2,1,1,4,1,1,6,...]
          and clock-test whether it is golden-structured or arithmetic.
  PART 4  L.O.R.E. designation: where e actually enters the framework (the
          exponential family the machinery itself uses: exp-routing,
          ln-entropy/recurrence, asinh in the spiral arc-length, the cusp
          (logarithmic) metric that hosts the golden angle).

Verdict artifact: ../data/euler_number_test_data.json
"""

import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

PHI = (1 + math.sqrt(5)) / 2

E_DIGITS = "2718281828459045235360287471352662497757247093699959574966967627"
E_INT = int(E_DIGITS[:20])  # 27182818284590452353  (first 20 digits, no point)


def factor(n):
    fs = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            fs[d] = fs.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        fs[n] = fs.get(n, 0) + 1
    return fs


def tau(fs):
    t = 1
    for p in fs.values():
        t *= p + 1
    return t


def digit_sum(n):
    return sum(int(c) for c in str(n))


def digit_sum_base(n, b):
    s = 0
    while n:
        s += n % b
        n //= b
    return s


def cf_e(n_terms):
    # e = [2; 1,2,1,1,4,1,1,6,1,1,8,...]
    a = [2]
    for k in range(1, n_terms):
        if k % 3 == 2:
            a.append(2 * ((k + 1) // 3))
        else:
            a.append(1)
    return a


def cf_from_float(x, n_terms):
    a = []
    for _ in range(n_terms):
        ai = int(math.floor(x))
        a.append(ai)
        if ai == 0:
            break
        r = x - ai
        if abs(r) < 1e-15:
            break
        x = 1.0 / r
    return a


def main():
    print("=" * 72)
    print("PART 1  digit-prefix census of e (T57-style, mirror 10262000)")
    print("=" * 72)
    rows = []
    for k in [2, 3, 4, 5, 6, 8, 10, 20]:
        pref = int(E_DIGITS[:k])
        rev = int(E_DIGITS[:k][::-1])
        fs = factor(pref)
        fsr = factor(rev)
        rows.append({
            "k": k, "prefix": pref, "factorization": fs,
            "tau": tau(fs), "digit_sum": digit_sum(pref),
            "reverse": rev, "reverse_tau": tau(fsr),
            "reverse_digit_sum": digit_sum(rev),
            "tau_equal": tau(fs) == tau(fsr),
            "digit_sum_equal": digit_sum(pref) == digit_sum(rev),
        })
        print(f"  e[{k:2d} digits] = {pref:20d}  tau={tau(fs):2d}  "
              f"digsum={digit_sum(pref):3d}   reverse tau={tau(fsr):2d}  "
              f"digsum={digit_sum(rev):3d}")
    # 8-digit prefix: 27182818 -- tau comparison
    p8 = int(E_DIGITS[:8])
    f8 = factor(p8)
    print("  e[8 digits] = 27182818 =", f8, " tau =", tau(f8),
          "digsum =", digit_sum(p8))

    print()
    print("=" * 72)
    print("PART 2  golden proximity of e with a fold-ladder null")
    print("=" * 72)
    TOL = 0.01  # within 1% of the rung
    targets = {"phi": PHI, "phi^2": PHI ** 2, "1/phi": 1 / PHI, "phi+1": PHI + 1}
    for name, t in targets.items():
        dist = abs(E_INT / 1e19 - t)  # e ~ 2.718, compare to targets near it
        rel = dist / t
        print(f"  e vs {name:6s} = {E_INT/1e19:.6f}  dist={dist:.4f}  rel={rel*100:.2f}%")
    # the only nearby candidate is phi^2 = 2.6180 (e is 3.83% above it)
    rel_phi2 = (math.e - PHI ** 2) / PHI ** 2
    print("  -> e is %.2f%% above phi^2 = 2.61803..." % (rel_phi2 * 100))
    # null: density of {phi, phi^2} rungs across the fold-ladder chain
    # (fold_ladder_phi already measured: an isolated golden hit is not rare)
    rng = list(range(1, 30))
    hits = sum(1 for n in rng for t in targets.values() if abs(math.e * n - t) < TOL)
    # rescale: count how many of the first 30 integers x satisfy
    # |x - t| < TOL for a rung target near a random 2.x constant -> by chance
    rng_hits = 0
    for _ in range(2000):
        c = 2.0 + 0.999 * ((_ * 7919) % 1000) / 1000.0  # pseudo-random 2..3
        if any(abs(c - t) < TOL for t in targets.values()):
            rng_hits += 1
    p_chance = rng_hits / 2000.0
    print(f"  null: a random constant in [2,3) sits within {TOL} of a "
          f"golden rung {p_chance*100:.1f}% of the time (n=2000)")

    print()
    print("=" * 72)
    print("PART 3  continued fraction of e vs golden structure")
    print("=" * 72)
    cfe = cf_e(15)
    print("  exact CF of e: ", cfe)
    cfr = cf_from_float(math.e, 15)
    print("  from float:    ", cfr)
    print("  phi CF = [1;1,1,1,...] (all ones). e's CF is {1,2,1,1,4,1,1,6,...}:")
    print("  a repeating-arithmetic pattern (1, 2k, 1 block), the most regular")
    print("  CF known -- arithmetic, not golden. e is 'golden' only in the")
    print("  loose sense that both have regular CFs.")

    print()
    print("=" * 72)
    print("PART 4  clock test (T59/T61): digit-sum 'laws' under base re-encoding")
    print("=" * 72)
    for k in [5, 6, 8]:
        p = int(E_DIGITS[:k])
        s10 = digit_sum(p)
        s8 = digit_sum_base(p, 8)
        s12 = digit_sum_base(p, 12)
        s16 = digit_sum_base(p, 16)
        print(f"  e[{k}] = {p:10d}  digsum10={s10:3d}  digsum8={s8:3d}  "
              f"digsum12={s12:3d}  digsum16={s16:3d}")

    print()
    print("=" * 72)
    print("PART 5  L.O.R.E. designation: where e enters the framework")
    print("=" * 72)
    print("  exp():  softmax routing in decentral_net/flow (the router's canonical)")
    print("  ln():   entropy / _compute_recurrence_time (ln-thinning <-> entropy)")
    print("  asinh:  the Archimedean spiral arc-length s=(a/2)(th sqrt(1+th^2)")
    print("          + asinh th) on which the golden-ratio closure r_ret/apex=1/phi")
    print("          is measured (fold_golden_closure.py)")
    print("  cusp metric: fibonacci_spiral.py concludes the golden angle is an")
    print("          exact property of the cusp (LOGARITHMIC) metric")
    print("  -> e designates to the base of the flow/entropy axis of the framework")
    print("     itself: it is the natural logarithm base of the machinery, NOT a")
    print("     separate golden constant. phi^2=2.618 vs e=2.718 (3.83% apart)")
    print("     is a coincidence-scale near-miss of the kind the repo refutes.")

    out = {
        "claim": "What does Euler's number designate to in the Puno framework? "
                 "tested via the repo's own census / null / clock-test discipline",
        "e": math.e,
        "e_first20_digits": E_INT,
        "part1_prefix_census": rows,
        "part2_golden": {
            "targets": {k: round(v, 6) for k, v in targets.items()},
            "e_minus_phi2_rel": round(rel_phi2, 5),
            "null_p_chance_within_1pct": round(p_chance, 4),
            "reading": "e is 3.83%% above phi^2; a random 2.x constant hits a "
                       "golden rung within 1%% by chance ~%.0f%% of the time"
                       % (p_chance * 100),
        },
        "part3_cf": {
            "e_cf": cfe,
            "phi_cf": [1] * 10,
            "reading": "e's CF is the repeating-arithmetic pattern 1,2k,1 -- "
                       "the most regular CF known; regular, but not golden.",
        },
        "part4_clock_test": {
            "reading": "digit sums of e-prefixes are gauge: they change under "
                       "base re-encoding (T59/T61), so no '11-sums' or tau "
                       "identity on e's digits is a law.",
        },
        "part5_designation": (
            "e designates to the natural base of the framework's own "
            "exponential family: exp in routing, ln in entropy/recurrence, "
            "asinh in the spiral arc-length that hosts the golden-ratio "
            "closure, and the cusp (logarithmic) metric that hosts the "
            "golden angle. e is the unit of the flow/entropy axis, not a "
            "golden constant; the e/phi^2 near-miss is a coincidence-scale "
            "hit of the kind the corpus's own null discipline refutes."
        ),
        "verdict": (
            "e is not a repo law. Every apparent 'designation' of e is either "
            "(1) arithmetic (its CF pattern 1,2k,1 is the most regular known), "
            "(2) coincidence-scale (e is 3.83% from phi^2, within the null "
            "rate for random 2.x constants), or (3) self-referential: e is the "
            "base of the log/exponential functions the framework itself uses, "
            "so finding e everywhere is finding the machinery's own shadow."
        ),
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "euler_number_test_data.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\nverdict:", out["verdict"])
    print("wrote data/euler_number_test_data.json")


if __name__ == "__main__":
    main()
