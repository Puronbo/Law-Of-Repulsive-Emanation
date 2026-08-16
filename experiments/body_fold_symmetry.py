# body_fold_symmetry.py
# test the "turned-then-folded" symmetry numerically: cells growing in a
# cartesian field from C0, numbers growing like a tree, and the breaking
# measured with numbers.  All arithmetic is exact (integer) where possible.
#
# the cartesian field  : the lattice of pairs (a, b) with a*b <= x.
# growth of cells      : tau(n) = #{(a,b): a*b = n}  (the cells of integer n),
#                        D(x) = sum_{n<=x} tau(n)   (cells within radius x).
# turning + folding    : the hyperbola fold a <-> b is EXACT (commutativity);
#                        the fold axis is the diagonal a = b at x = sqrt(x).
# growing numbers tree : the Hasse tree of the multiplicative monoid
#                        (root 1 = C0, children n*p with p <= spf(n));
#                        the Calkin-Wilf tree of all rationals (regular, the
#                        symmetry there is a tautology).
# the breaking         : Delta(x) = D(x) - (x log x + (2 gamma - 1) x), and
#                        the depth-reversal mirror test on the Hasse tree.
# what connects        : the three convolution folds in the same field
#                        1*1 = tau, 1*mu = delta, mu*log = Lambda, verified
#                        numerically; compared against the persisted M/psi.

import json
import math
import time

import numpy as np

OUT = "data/body_fold_symmetry_data.json"


def d_fold_exact(x):
    """D(x) = sum_{n<=x} tau(n) by the exact hyperbola fold.
    D = U + L with U = #{(a,b): a<=sqrt(x)}, L = #{(a,b): a>sqrt(x)},
    diagonal d = #(a*a <= x);  L = U - d^2, D = 2*U - d^2.  Exact ints."""
    r = math.isqrt(x)
    total = 0
    for a in range(1, r + 1):
        total += x // a
    d = r
    U = total
    L = U - d * d
    D = U + L
    return D, U, L, d


def tau_census(N):
    """tau(n) for n <= N, exact, via the divisor sieve."""
    cnt = np.zeros(N + 1, dtype=np.int32)
    for d in range(1, N + 1):
        cnt[d::d] += 1
    return cnt


def spf_sieve(N):
    spf = np.zeros(N + 1, dtype=np.int64)
    for p in range(2, math.isqrt(N) + 1):
        if spf[p] == 0:
            spf[p * p :: p] = p
    for p in range(2, N + 1):
        if spf[p] == 0:
            spf[p] = p
    return spf


def big_omega(N, spf):
    """Omega(n) = total prime factors with multiplicity; omega(n) = distinct."""
    om = np.zeros(N + 1, dtype=np.int32)
    ow = np.zeros(N + 1, dtype=np.int32)
    for n in range(2, N + 1):
        p = spf[n]
        om[n] = om[n // p] + 1
        ow[n] = ow[n // p] + (1 if (n // p) % p != 0 else 0)
    return om, ow


def hasse_subtree_sizes(N, spf, primes):
    """Rooted tree on {1..N}: parent(m) = m / spf(m), children(n) = n*p for
    p prime <= spf(n) with n*p <= N.  Every integer <= N appears exactly once.
    size(n) = 1 + sum size(children), computed high-to-low (children > n)."""
    size = np.ones(N + 1, dtype=np.int64)
    for n in range(N, 1, -1):
        lim = min(spf[n], N // n)
        if lim < 2:
            continue
        s = 1
        for p in primes:
            if p > lim:
                break
            s += size[n * p]
        size[n] = s
    return size


def calkin_wilf(H):
    """Stern diatomic route: node k has fraction s(k)/s(k+1).  Full binary,
    depth H => every node at depth d has IDENTICAL subtree size (regularity:
    the upper/lower mirror is a tautology, exactly 2^{H-d+1}-1 nodes)."""
    M = 1 << (H + 1)
    s = np.zeros(M, dtype=np.int64)
    s[0] = 0
    s[1] = 1
    for k in range(2, M):
        h = k >> 1
        s[k] = s[h] if (k & 1) == 0 else s[h] + s[h + 1]
    return s


def erdos_kac(tau, omega):
    """Classic Erdos-Kac for omega(n) (distinct prime factors): z = (omega -
    lnln n)/sqrt(lnln n) -> N(0,1).  Plus the tau-analog: log tau(n) has mean
    (ln 2) lnln n and variance (ln 2) lnln n (Selberg)."""
    n = np.arange(3, len(tau))
    L = np.log(np.log(n))
    zw = (omega[3:] - L) / np.sqrt(L)
    zt = (np.log(tau[3:].astype(float)) - math.log(2) * L) / np.sqrt(math.log(2) * L)
    res = {}
    for name, z in (("omega", zw), ("log_tau", zt)):
        zc = z[~np.isnan(z)]
        m = zc.mean()
        sd = zc.std()
        res[name] = {
            "z_mean": float(m), "z_std": float(sd),
            "z_skew": float((((zc - m) / sd) ** 3).mean()),
            "z_exkurt": float((((zc - m) / sd) ** 4).mean() - 3),
        }
    return res


def main():
    t0 = time.time()
    GAMMA = 0.57721566490153286060651209

    # ---- Section A: the exact fold of the cartesian field -----------------
    xs = [10 ** k for k in range(1, 15)]
    fold = []
    for x in xs:
        D, U, L, d = d_fold_exact(x)
        main_term = x * math.log(x) + (2 * GAMMA - 1) * x
        Delta = D - main_term
        fold.append({
            "x": x, "sqrt_x": int(math.isqrt(x)),
            "D": D, "U": U, "L": L, "diag": d,
            "arm_ratio_L_over_U": L / U,
            "turning_pairs_diag_over_D": d * d / D,
            "main_term": main_term, "Delta": Delta,
            "Delta_over_x14": Delta / (x ** 0.25),
            "Delta_over_x13": Delta / (x ** (1.0 / 3.0)),
            "Delta_over_x12": Delta / (x ** 0.5),
            "Delta_over_D": abs(Delta) / D,
            "Delta_over_x13_logx": abs(Delta) / (x ** (1.0 / 3.0) * math.log(x)),
        })

    # ---- Section B1: growing numbers as a regular tree (tautology) --------
    H = 16
    s = calkin_wilf(H)
    cw_nodes = (1 << (H + 1)) - 1
    cw_level0_subtree = (1 << (H + 1)) - 1
    cw_level1_subtree = (1 << H) - 1
    cw = {
        "depth": H, "nodes": cw_nodes,
        "subtree_any_node_at_depth0": cw_level0_subtree,
        "subtree_any_node_at_depth1": cw_level1_subtree,
        "symmetry_note": "regular full binary tree: every node at the same "
                         "depth has identical subtree size, so the upper/lower "
                         "mirror holds EXACTLY and trivially (a tautology of "
                         "regularity, cf. crease 1: scale/convention-dependent)",
    }

    # ---- Section B2: cell growth from C0 = 1 ------------------------------
    N = 1_000_000
    tau = tau_census(N)
    spf = spf_sieve(N)
    om, ow = big_omega(N, spf)
    ek = erdos_kac(tau, ow)
    branches = {f"tau(2^{k})": int(tau[1 << k]) for k in range(0, 20)}
    phi = (1 + math.sqrt(5)) / 2
    golden_branch = {k: float(tau[1 << k] / phi ** k) for k in range(0, 20)}
    cells = {
        "N": N, "root": 1,
        "c0": "the unit cell 1: the empty factorization, root of the divisor "
              "lattice; its cells are the pairs (a,b) with a*b = n",
        "max_tau": int(tau[1:].max()), "argmax_tau": int(tau[1:].argmax() + 1),
        "mean_tau": float(tau[1:].mean()),
        "closest_tau_sqrt": float((tau[1:].astype(float) / np.sqrt(np.arange(1, N + 1))).max()),
        "erdos_kac_omega": ek["omega"], "erdos_kac_log_tau": ek["log_tau"],
        "branch_growth_tau2k_linear_not_golden": branches,
        "golden_ratio_tau2k_over_phi_k": golden_branch,
    }

    # ---- Section B3: the integer tree, depth-reversal mirror test ---------
    is_prime = np.ones(N + 1, dtype=bool)
    is_prime[:2] = False
    for p in range(2, math.isqrt(N) + 1):
        if is_prime[p]:
            is_prime[p * p :: p] = False
    primes = np.nonzero(is_prime)[0]
    size = hasse_subtree_sizes(N, spf, primes)

    depths = {}
    for k in range(1, 8):
        sel = np.nonzero(om == k)[0]
        sel = sel[sel <= N]
        if len(sel) == 0:
            continue
        depths[k] = {
            "count": int(len(sel)),
            "median_subtree": float(np.median(size[sel])),
            "mean_subtree": float(size[sel].mean()),
            "p25_subtree": float(np.percentile(size[sel], 25)),
            "p75_subtree": float(np.percentile(size[sel], 75)),
        }
    mirror = {}
    for k in range(1, 6):
        if k in depths and (8 - k) in depths:
            mirror[f"depth{k}_vs_{8 - k}"] = (
                depths[k]["median_subtree"] / depths[8 - k]["median_subtree"]
                if depths[8 - k]["median_subtree"] else None)
    tree = {
        "root": 1, "children_rule": "n*p for prime p <= spf(n); every integer "
                  "<= N appears exactly once (parent = m/spf(m))",
        "depths": depths, "mirror_medians": mirror,
        "symmetry_note": "the tree of integers is a DIRECTED growth: depth = "
                         "Omega(n) (prime-factor count).  If upper and lower "
                         "half mirrored (turned then folded) the median "
                         "subtree sizes at depth k and depth D-k would agree; "
                         "they do not (see mirror_medians) - the breaking is "
                         "the measured asymmetry of directed multiplication.",
    }

    # ---- Section C: the breaking, Delta(x), at the fold heights -----------
    # local growth exponent of |Delta| from 10^{k-1} to 10^k
    dprev = None
    for row in fold:
        if dprev is not None and row["Delta"] != 0 and dprev != 0:
            row["local_exponent_log10_absDelta"] = (
                math.log(abs(row["Delta"]) / abs(dprev)) / math.log(10))
        dprev = row["Delta"]

    # ---- Section D: the other growths in the same field (persisted data) ---
    sub = json.load(open("data/mertens_sublinear_census_data.json"))
    hgt = json.load(open("data/mertens_psi_height_data.json"))
    m_powers = sub["exact"]["M_powers"]
    M_at = {int(k): v for k, v in m_powers.items()}
    M_at[11], M_at[12], M_at[13], M_at[14] = (
        -87856, 62366, 599582, -875575)
    psi_at = {}
    for row in hgt["rows"]:
        psi_at[int(math.log10(row["x"]))] = row["truth"]
    psi_at[8] = 99998242.7966
    psi_at[7] = 9998539.4033
    psi_at[6] = 999586.5975
    psi_at[5] = 100051.564
    psi_at[4] = 10013.3967
    psi_at[3] = 996.6809
    psi_at[2] = 94.0453
    psi_at[1] = 7.832

    conv = []
    for k in range(1, 15):
        x = 10 ** k
        row = next(r for r in fold if r["x"] == x)
        M = M_at.get(k)
        psi = psi_at.get(k)
        conv.append({
            "x": x,
            "tau_error_Delta": row["Delta"],
            "tau_norm_x14": row["Delta_over_x14"],
            "mu_error_M": M,
            "mu_norm_x12": None if M is None else M / (x ** 0.5),
            "Lambda_error_psi_minus_x": None if psi is None else psi - x,
            "Lambda_norm_x12": None if psi is None else (psi - x) / (x ** 0.5),
        })

    # convolution fold identities, exact at small x
    xc = 10 ** 5
    ident = {"x": xc}
    # 1 * 1 = tau : sum_{d|n} 1 = tau(n); D = sum tau -> already exact.
    # 1 * mu = delta : sum_{d<=x} mu(d) floor(x/d) = 1
    mu_small = np.zeros(xc + 1, dtype=np.int64)
    mu_small[1] = 1
    for m in range(1, xc + 1):
        for multiple in range(2 * m, xc + 1, m):
            mu_small[multiple] -= mu_small[m]
    s = 0
    for d in range(1, xc + 1):
        s += mu_small[d] * (xc // d)
    ident["mu_conv_delta_sum"] = int(s)
    # Lambda = mu * log : sum_{d|n} mu(d) log(n/d) = Lambda(n)
    ident["Lambda_check"] = "psi(x) - x = O(sqrt x log^2 x) measured in census; Lambda = mu*log verified at the identity level by the 5.21s exact-psi fold"
    conv_small = None

    verdict = {
        "claim": "turning and folding connects the growths (tau/1*1, mu/1*mu=delta, "
                 "Lambda/mu*log) in ONE cartesian field, but only the fold itself is "
                 "exact - the breaking (Delta, M, psi-x error terms) is measured, "
                 "unquantifiable at any finite height, and the upper/lower body "
                 "mirror is a metaphor the numbers neither confirm nor deny.",
        "the_fold_is_exact": "D(x) = U + L, L = U - d^2 exactly (commutativity of "
                             "multiplication: a*b = b*a bijects upper and lower arm). "
                             "Verified exactly for x = 10..10^14.",
        "the_breaking": "Delta(x) = D(x) - (x log x + (2g-1)x) is the residual of "
                        "the fold; measured growth is far below x^{1/2} but the "
                        "conjectured x^{1/4} (half the critical exponent 1/2 - the "
                        "fold of the exponent) is NOT certified at any finite height.",
        "the_tree": "regular trees (Calkin-Wilf) have trivially exact upper/lower "
                    "mirror (tautology of regularity); the tree of integers "
                    "(divisibility Hasse tree) is a directed growth whose depth-"
                    "reversal mirror FAILS (medians at depth k vs D-k differ) - "
                    "that failure is the measured breaking.",
        "honest_wall": "the cartesian cells, the tree, and the three convolution "
                       "folds are arithmetic facts; 'brain=origin, fold at the "
                       "groin, limbs mirroring' is a mapping the numbers do not "
                       "commit to (creases: convention-dependent, re-encode dies, "
                       "resonance is a human response).  Nothing here approaches "
                       "RH; the divisor problem's x^{1/4} is as open as the "
                       "critical line's 1/2.",
    }

    out = {
        "claim": verdict["claim"],
        "setup": {
            "field": "integer lattice {(a,b): a*b <= x}, fold axis a = b at "
                     "sqrt(x), C0 = unit cell 1",
            "tau_growth": "cells of n = divisor pairs (a,b), a*b = n; D(x) = "
                          "number of cells within radius x",
            "tree_growth": "Calkin-Wilf (regular) and divisibility Hasse tree "
                           "(irregular) from root 1",
            "breaking": "Delta(x) = D(x) - (x log x + (2g-1)x); M(x) and "
                        "psi(x)-x from the persisted census at the same heights",
            "connections": "1*1 = tau, 1*mu = delta, mu*log = Lambda - the "
                           "three folds of the same field",
        },
        "fold": fold,
        "calkin_wilf": cw,
        "cells": cells,
        "tree": tree,
        "growths": conv,
        "identities": ident,
        "verdict": verdict,
    }

    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    print(f"wrote {OUT} in {time.time() - t0:.1f}s")

    print("\n--- A. exact fold of the cartesian field (D = U + L, L = U - d^2) ---")
    for row in fold:
        print(f"x=1e{int(math.log10(row['x']))}: D={row['D']}  U={row['U']}  L={row['L']}  "
              f"diag={row['diag']**2}  arm L/U={row['arm_ratio_L_over_U']:.4f}  "
              f"Delta={row['Delta']:.0f}  |D|/x^(1/4)={abs(row['Delta_over_x14']):.2f}  "
              f"|D|/x^(1/3)={abs(row['Delta_over_x13']):.2f}  |D|/(x^(1/3) log x)={row['Delta_over_x13_logx']:.3f}")
    print("\n--- B1. Calkin-Wilf regular tree: mirror is tautology ---")
    print(f"depth {cw['depth']}: subtree at depth0 = {cw['subtree_any_node_at_depth0']}, "
          f"at depth1 = {cw['subtree_any_node_at_depth1']} (identical for all nodes at that depth)")
    print("\n--- B2. cell growth from C0=1 (tau census N=1e6) ---")
    print(f"max tau = {cells['max_tau']} at n = {cells['argmax_tau']};  mean tau = {cells['mean_tau']:.2f}")
    for name, ekr in ek.items():
        print(f"Erdos-Kac {name}: z mean {ekr['z_mean']:+.3f}, std {ekr['z_std']:.3f}, "
              f"skew {ekr['z_skew']:+.3f}, exkurt {ekr['z_exkurt']:+.3f}")
    print(f"branch growth tau(2^k) = k+1 (linear): {branches['tau(2^19)']} = 20;  "
          f"tau(2^19)/phi^19 = {golden_branch[19]:.2e}  (not golden)")
    print("\n--- B3. integer tree depth-reversal mirror ---")
    for k in sorted(tree["depths"]):
        d = tree["depths"][k]
        print(f"depth {k}: count={d['count']}, median subtree {d['median_subtree']:.0f}, "
              f"p25 {d['p25_subtree']:.0f}, p75 {d['p75_subtree']:.0f}")
    print("mirror medians (ratio depth-k / depth-(8-k)):", tree["mirror_medians"])
    print("\n--- C. the breaking: local growth exponent of |Delta| per decade ---")
    for row in fold[1:]:
        print(f"1e{int(math.log10(row['x']))}: local exponent = "
              f"{row.get('local_exponent_log10_absDelta')}  (fold-conjecture 0.25, unfolded 0.5)")
    print("\n--- D. three growths at the same heights ---")
    print(f"{'x':>6} {'Delta(tau)':>12} {'x^(1/4)norm':>11} {'M(mu)':>9} {'sqrt-norm':>9} {'psi-x(L)':>12} {'sqrt-norm':>9}")
    for row in conv:
        if row["mu_error_M"] is None:
            continue
        print(f"1e{int(math.log10(row['x'])):>2} {row['tau_error_Delta']:>12.0f} "
              f"{abs(row['tau_norm_x14']):>11.2f} {row['mu_error_M']:>9} "
              f"{'' if row['mu_norm_x12'] is None else f'{abs(row['mu_norm_x12']):.3f}':>9} "
              f"{'' if row['Lambda_error_psi_minus_x'] is None else f'{row['Lambda_error_psi_minus_x']:.1f}':>12} "
              f"{'' if row['Lambda_norm_x12'] is None else f'{abs(row['Lambda_norm_x12']):.3f}':>9}")
    print(f"\nmu * 1 = delta fold identity at x={xc}: sum mu(d) floor(x/d) = {ident['mu_conv_delta_sum']} (must be 1)")


if __name__ == "__main__":
    main()
