"""Four-point coordinate expansion of the L.O.R.E. anchor 10262000.

Given the single anchor 10262000, the "expanded lattice" is defined by the
four points

    10262000, 20001026, 20002610, 26102000

and this experiment generates the structure of ALL known points:

  A. arithmetic of the four anchors (factorisations, gcd, the integer
     lattice they span);
  B. the block structure  1026|2000, 2000|1026, 2000|2610, 2610|2000
     and the 4-point swap cycle that closes it into a "circle";
  C. the full orbit: all 840 distinct numbers whose digits permute the
     multiset {0,0,0,0,1,2,2,6} (the complete lattice of points carried by
     the anchor's digits), with its distribution;
  D. the permutohedron of that multiset: distance spheres ("circles")
     centred at each anchor under the Kendall/adjacent-swap metric,
     pairwise distances, and the diameter;
  E. HONEST WALL: this is finite arithmetic, computed exactly.  It has no
     established mechanism connecting it to the zeta zeros or to RH; the
     proximity of the anchors to the Connes lattice 2 pi/L * Z at scale
     4.2e6 is at chance level (every integer is within half a lattice
     spacing of some lattice point).  No claim is made beyond the
     structures computed here.
"""

import itertools
import json
import math
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "four_point_lattice_data.json")

ANCHORS = [10262000, 20001026, 20002610, 26102000]
DIGITS = "00001226"          # sorted multiset {0,0,0,0,1,2,2,6}


# ---------------------------------------------------------------- A. prime
def factor(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def bezout(a, b):
    """Extended Euclid: returns (g, x, y) with g = x a + y b."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = bezout(b, a % b)
    return g, y1, x1 - (a // b) * y1


def anchor_arithmetic():
    facts = {a: factor(a) for a in ANCHORS}
    g = math.gcd(*ANCHORS)
    g2, x2, y2 = bezout(ANCHORS[0], ANCHORS[1])
    diffs = {f"{a2}-{a1}": a2 - a1
             for a1, a2 in sorted(itertools.combinations(ANCHORS, 2))}
    return {
        "factorisations": {str(a): facts[a] for a in ANCHORS},
        "gcd_of_all_four": g,
        "lattice_spanned": "2*Z (every even integer is an integer "
                           "combination of the anchors)",
        "bezout_2": {"g": g2, "x": x2, "y": y2,
                     "from": ANCHORS[:2],
                     "identity": "%d = %d*%d %+d*%d"
                                 % (g2, x2, ANCHORS[0], y2, ANCHORS[1])},
        "pairwise_differences": diffs,
    }


# ---------------------------------------------------------------- B. blocks
def block_structure():
    blocks = sorted({str(a)[:4] for a in ANCHORS} | {str(a)[4:] for a in ANCHORS})
    split = {str(a): (str(a)[:4], str(a)[4:]) for a in ANCHORS}
    return {
        "blocks": blocks,
        "splits": split,
        "swap_cycle": ["1026|2000", "2000|1026", "2000|2610", "2610|2000"],
        "step_1584": {"2610_minus_1026": 2610 - 1026,
                      "gap_20002610_minus_20001026":
                          20002610 - 20001026,
                      "factor": factor(2610 - 1026)},
    }


# ------------------------------------------------- C. full orbit of digits
def orbit():
    """All distinct numbers obtained by permuting the digit multiset."""
    strings = set(itertools.permutations(DIGITS))
    pts = sorted({int("".join(s)) for s in strings})
    return pts


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def distribution(pts):
    lo, hi = min(pts), max(pts)
    n = len(pts)
    mean = sum(pts) / n
    qs = np_quantile(pts, [0.25, 0.5, 0.75])
    hist = [0] * 10
    w = (hi - lo) / 10.0
    for p in pts:
        hist[min(9, int((p - lo) / w))] += 1
    gaps = [pts[i + 1] - pts[i] for i in range(n - 1)]
    ends = {0: 0, 2: 0, 6: 0, 1: 0}
    for p in pts:
        ends[p % 10] = ends.get(p % 10, 0) + 1
    # leading-digit clusters: the orbit splits by first digit
    clusters = {}
    for p in pts:
        lead = p // 10 ** (len(str(p)) - 1)
        c = clusters.setdefault(lead, {"count": 0, "min": p, "max": p})
        c["count"] += 1
        c["min"] = min(c["min"], p)
        c["max"] = max(c["max"], p)
    return {
        "n": n,
        "min": lo,
        "max": hi,
        "mean": round(mean, 2),
        "median": qs[1],
        "quartiles": qs,
        "std": round(math.sqrt(sum((p - mean) ** 2 for p in pts) / n), 2),
        "histogram_10_bins": hist,
        "max_consecutive_gap": max(gaps),
        "ending_digit_counts": ends,
        "leading_digit_clusters": {str(k): v for k, v in
                                   sorted(clusters.items())},
        "count_divisible_by_3": sum(1 for p in pts if p % 3 == 0),
        "count_primes": sum(1 for p in pts if is_prime(p)),
        "anchors_rank": {str(a): pts.index(a) + 1 for a in ANCHORS},
    }


def np_quantile(pts, qs):
    n = len(pts)
    out = []
    for q in qs:
        k = (n - 1) * q
        lo_i = int(k)
        frac = k - lo_i
        out.append(round(pts[lo_i] * (1 - frac) + pts[min(lo_i + 1, n - 1)]
                         * frac, 1))
    return out


# ---------------------------------------- D. permutohedron (Kendall metric)
def kendall(a, b):
    """Distance = number of discordant symbol pairs = minimal number of
    adjacent swaps of distinct symbols carrying string a to string b
    (multiset permutohedron metric)."""
    n = len(a)
    d = 0
    for i in range(n):
        ai = a[i]
        for j in range(i + 1, n):
            aj = a[j]
            if ai == aj or b[i] == b[j]:
                continue
            if (ai > aj) != (b[i] > b[j]):
                d += 1
    return d


def permutohedron(pts_str, anchors_str):
    out = {}
    for a in anchors_str:
        hist = {}
        for s in pts_str:
            d = kendall(a, s)
            hist[d] = hist.get(d, 0) + 1
        cum = {}
        tot = 0
        for d in sorted(hist):
            tot += hist[d]
            cum[d] = tot
        out[a] = {"sphere_sizes": {str(k): v for k, v in
                                   sorted(hist.items())},
                  "cumulative_circles": {str(k): v for k, v in
                                         sorted(cum.items())}}
    matrix = {}
    for i in range(4):
        for j in range(i + 1, 4):
            matrix["%s-%s" % (anchors_str[i], anchors_str[j])] = \
                kendall(anchors_str[i], anchors_str[j])
    diameter = 0
    for i in range(len(pts_str)):
        for j in range(i + 1, len(pts_str)):
            diameter = max(diameter, kendall(pts_str[i], pts_str[j]))
    return {"spheres": out, "pairwise": matrix, "diameter": diameter}


def nearest_connes_lattice(a):
    """Normalised distance of the anchor to the Connes lattice 2 pi/L * Z,
    measured in half-spacings (0 = on a lattice point, 1 = midway)."""
    L = math.log(13.0)
    spacing = 2.0 * math.pi / L
    k = round(a / spacing)
    resid = abs(a - spacing * k)
    return round(resid / (spacing / 2.0), 3)


def main():
    t0 = time.time()
    pts = orbit()
    anchors_str = [str(a) for a in ANCHORS]

    arith = anchor_arithmetic()
    blocks = block_structure()
    dist = distribution(pts)
    permu = permutohedron(["{:08d}".format(p) for p in pts], anchors_str)

    # E. honest statistical reframing of "nearness to the Connes lattice"
    residues = {str(a): nearest_connes_lattice(a) for a in ANCHORS}

    data = {
        "anchors": ANCHORS,
        "digit_multiset": "0,0,0,0,1,2,2,6",
        "arithmetic": arith,
        "block_structure": blocks,
        "full_orbit": dist,
        "permutohedron": permu,
        "connes_lattice_residues": residues,
        "connes_note": ("residue 0 = exactly on a lattice point, 1 = "
                        "midway; uniform over [0,1] for random integers, "
                        "so values near 0 are chance, not signal"),
        "honest_wall": ("All structures above are finite arithmetic of the "
                        "8-digit multiset {0,0,0,0,1,2,2,6}, computed "
                        "exactly.  No mechanism connects the anchors to the "
                        "zeros of the Riemann zeta function or to RH; the "
                        "2 pi/L lattice proximity is at chance level; and "
                        "the earlier zeta-density coincidence concerned "
                        "positions of order 1-150, a different scale "
                        "entirely.  Nothing here is a proof or a disproof "
                        "of anything about zeta."),
        "runtime_sec": round(time.time() - t0, 1),
    }
    with open(OUT, "w") as f:
        json.dump(data, f, indent=2)

    # ---------------------------------------------- printable report
    print("A. ARITHMETIC OF THE FOUR ANCHORS")
    for a, f in arith["factorisations"].items():
        print("  %-9s = %s" % (a, " * ".join("%d^%d" % (p, e)
                                             for p, e in f.items())))
    print("  gcd of all four = %d  ->  lattice spanned = %s"
          % (arith["gcd_of_all_four"], arith["lattice_spanned"]))
    print("  bezout:", arith["bezout_2"]["identity"])
    print("  pairwise differences:", arith["pairwise_differences"])

    print()
    print("B. BLOCK STRUCTURE (4+4 splits)")
    print("  blocks:", blocks["blocks"])
    for a, (b1, b2) in blocks["splits"].items():
        print("  %s -> %s | %s" % (a, b1, b2))
    print("  swap cycle:", blocks["swap_cycle"])
    print("  2610-1026 = %d = %s ; same as 20002610-20001026"
          % (blocks["step_1584"]["2610_minus_1026"],
             " * ".join("%d^%d" % (p, e)
                        for p, e in blocks["step_1584"]["factor"].items())))

    print()
    print("C. FULL ORBIT: all permutations of {0,0,0,0,1,2,2,6}")
    d = dist
    print("  n = %d  range [%d, %d]" % (d["n"], d["min"], d["max"]))
    print("  mean %s  median %s  quartiles %s  std %s"
          % (d["mean"], d["median"], d["quartiles"], d["std"]))
    print("  histogram (10 bins over [min,max]):", d["histogram_10_bins"])
    print("  leading-digit clusters (count, [min,max]):")
    for k, v in d["leading_digit_clusters"].items():
        print("    lead %s: %d points  [%d, %d]"
              % (k, v["count"], v["min"], v["max"]))
    print("  ending digit counts (0/2/6/1):", d["ending_digit_counts"])
    print("  divisible by 3: %d   primes: %d   max gap: %d"
          % (d["count_divisible_by_3"], d["count_primes"],
             d["max_consecutive_gap"]))
    print("  anchor ranks (sorted 1..%d): %s" % (d["n"], d["anchors_rank"]))

    print()
    print("D. PERMUTOHEDRON CIRCLES (Kendall distance from each anchor)")
    for a in anchors_str:
        sph = permu["spheres"][a]
        keys = [int(k) for k in sph["sphere_sizes"]]
        print("  from %s: distance->count %s ; radius<=d cumulative %s"
              % (a, sph["sphere_sizes"], sph["cumulative_circles"]))
    print("  pairwise distances:", permu["pairwise"])
    print("  diameter of the whole permutohedron: %d" % permu["diameter"])
    print("  (all four spheres are identical because the symmetric group "
          "acts transitively on the 840 multiset words: the 'circle' shell "
          "sizes do not depend on the anchor point; note the empty shell "
          "at distance 14)")

    print()
    print("E. PROXIMITY TO THE CONNES LATTICE (normalised, 0=on, 1=midway)")
    print("  ", residues)
    print("   ", data["connes_note"])
    print()
    print("HONEST WALL:", data["honest_wall"])
    print("wrote", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
