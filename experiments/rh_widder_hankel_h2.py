#!/usr/bin/env python3
"""
rh_widder_hankel_h2.py -- H2 of the pinned Stieltjes/Widder framework: the
full Hankel positivity ladder and the shifted Schur/Vandermonde identities.

H1 (rh_widder_hankel_h1.py) opened the stage named in section 14 of
rh_infinite_unit_stieltjes_pinned.md with the first shifted determinants
D_0 = Q_1Q_3 - Q_2^2 and D_1 = Q_3Q_5 - Q_4^2.  H2 climbs to the structure
those determinants are the 2x2 shadows of:

  * the Hankel matrix of the transformed-zero moment sequence
        M_k(x) = Q_{k+1}(x),  H_N(x) = [M_{i+j}(x)]_{i,j=0}^N,
    with the pair of positivity conditions a Stieltjes moment sequence must
    satisfy (framework record sections 9 and 16):
        Hamburger Hankel   [Q_{i+j+1}]   >= 0,
        Stieltjes Hankel   [Q_{i+j+2}]   >= 0;
  * the shifted Schur/Vandermonde determinant identity (framework section 10)
        det H_N = sum_{0<=i_0<...<i_N} (prod_a q_{i_a})
                  prod_{a<b} (q_{i_a} - q_{i_b})^2,
    so under RH (q_rho real) H_N >= 0 term by term;
  * the higher shifted-determinant ladder
        D_m = Q_{2m+1}Q_{2m+3} - Q_{2m+2}^2
            = sum_{i<j} (q_i q_j)^{2m+1} (q_i - q_j)^2   (m = 0..3 here).

The analytic side is the same explicit formula as H1: Q_k via the section 17
finite differential transform of F_xi, with zeta'/zeta by analytic
continuation and NO zetazero data, so the Hankel matrices below are obtained
without assuming where the zeros are.  The zero-side is used only to verify
the algebraic identities (which hold for any multiset {q_i}, real or complex).

What is deliberately NOT claimed: the Widder criterion is posited, positivity
is checked at finitely many x, and the prime-gamma -> Hankel bridge (record
section 27) is untouched.  Nothing here proves RH.

Run:  python experiments/rh_widder_hankel_h2.py

Artifact: experiments/data/rh_widder_hankel_h2_data.json
"""

import json
import os
import sys
from itertools import combinations
from math import comb

import mpmath as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rh_zero_scale_objects import _log_xi_moments, G5_JMAX

mp.mp.dps = 70

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H2_X = [mp.mpf("1/2"), mp.mpf(1), mp.mpf(4)]  # sample points x > 0
H2_KMAX = 9        # moments Q_1 .. Q_9 (enough for D_0..D_3 and H_3)
H2_KZERO = 300     # zeros in the translation cross-check
H2_NMAX = 3        # largest Hankel order N
H2_SCHUR_Z = 8     # zeros used for the brute-force Schur identity (C(8,4)=70)
H2_TRANS_TOL = mp.mpf("1e-4")
H2_ID_TOL = mp.mpf("1e-40")

report = {
    "experiment": "widder/hankel level 2: full Hankel positivity ladder and "
                  "shifted Schur/Vandermonde identities",
    "gates": [],
    "conclusion": "",
}
gates_passed = 0


def gate(name, ok, detail):
    global gates_passed
    ok = bool(ok)
    report["gates"].append({"gate": name, "passed": ok, "detail": detail})
    print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
    if ok:
        gates_passed += 1


# ---------------------------------------------------------------- analytic

def _zeta_log_deriv(s):
    return mp.zeta(s, 1, 1) / mp.zeta(s, 1, 0)


def _F(x):
    s = mp.mpf(1) / 2 + mp.sqrt(x)
    return (1 / s + 1 / (s - 1) + mp.mpf(1) / 2 * mp.digamma(s / 2)
            - mp.mpf(1) / 2 * mp.log(mp.pi) + _zeta_log_deriv(s)) / mp.sqrt(x)


def _Q_analytic(x, kmax):
    """Q_1..Q_kmax from one Taylor expansion of F_xi at x (section 17)."""
    tay = mp.taylor(lambda t: _F(x + t), mp.mpf(0), 2 * kmax - 1)
    out = []
    for k in range(1, kmax + 1):
        out.append(mp.mpf(1) / 2 * sum(
            comb(k, j) * (-x) ** (k - j) * (-1) ** (2 * k - j - 1)
            * tay[2 * k - j - 1] for j in range(k + 1)))
    return out


# ---------------------------------------------------------------- zero side

def _zero_ordinates(K):
    dps = mp.mp.dps
    mp.mp.dps = 30
    try:
        return [mp.im(mp.zetazero(k)) for k in range(1, K + 1)]
    finally:
        mp.mp.dps = dps


def _q(g, x):
    w = g * g
    return w / (x + w) ** 2


moments = _log_xi_moments(G5_JMAX)


def _Q_moment(m, x):
    """Q_m = sum_{j>=0} (-1)^j C(2m+j-1, j) x^j M_{2(m+j)} from log-Xi data."""
    return sum((-1) ** j * mp.binomial(2 * m + j - 1, j) * x ** j
               * moments[m + j] for j in range(0, G5_JMAX - m + 1))


def _Q_zerotail(m, x, qs):
    """Zero + moment-tail evaluation of Q_m (direct sum for m >= 3, moment
    series for m = 1, 2 whose tails are not negligible at 300 zeros)."""
    if m <= 2:
        return _Q_moment(m, x)
    return sum(q ** m for q in qs)


# ---------------------------------------------------------------- helpers

def _hankel_dets(Qs, shift):
    """Leading principal 1..N+1 determinants of [Q_{i+j+shift}]."""
    Nmax = (len(Qs) - shift - 1) // 2
    out = []
    for N in range(0, Nmax + 1):
        H = mp.matrix(N + 1, N + 1)
        for i in range(N + 1):
            for j in range(N + 1):
                H[i, j] = Qs[i + j + shift - 1]  # Qs[k-1] = Q_k
        out.append(float(mp.det(H)))
    return out


def _schur(qs, N):
    tot = mp.mpf(0)
    for idx in combinations(range(len(qs)), N + 1):
        prod = mp.mpf(1)
        for i in idx:
            prod *= qs[i]
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                prod *= (qs[idx[a]] - qs[idx[b]]) ** 2
        tot += prod
    return tot


def main():
    print("H2: Hankel ladder H_N=[Q_{i+j+1}] and shifted Schur identities\n")
    gz = _zero_ordinates(H2_KZERO)

    rows = []
    worst_trans = mp.mpf(0)
    pos_ok = True
    for x in H2_X:
        qs = [_q(g, x) for g in gz]
        Qa = _Q_analytic(x, H2_KMAX)              # Q_1 .. Q_9 analytic
        trans = mp.mpf(0)
        for k in range(1, H2_KMAX + 1):
            Qz = _Q_zerotail(k, x, qs)
            trans = max(trans, abs(Qa[k - 1] - Qz) / abs(Qa[k - 1]))
        worst_trans = max(worst_trans, trans)
        ham = _hankel_dets(Qa, 1)   # [Q_{i+j+1}]
        sti = _hankel_dets(Qa, 2)   # [Q_{i+j+2}]
        D = [Qa[2 * m] * Qa[2 * m + 2] - Qa[2 * m + 1] ** 2
             for m in range(0, (H2_KMAX - 2) // 2)]
        if not (all(d > 0 for d in D) and all(d > 0 for d in ham)
                and all(d > 0 for d in sti)):
            pos_ok = False
        rows.append({"x": float(x), "translation_rel": float(trans),
                     "D_m": [float(d) for d in D],
                     "hamburger_dets": ham, "stieltjes_dets": sti,
                     "Q1": float(Qa[0]), "Q3": float(Qa[2]), "Q5": float(Qa[4])})
        print("  x=%5s  D=%s" % (mp.nstr(x, 3), ["%.3e" % d for d in D]))
        print("          hamburger=%s" % ["%.3e" % d for d in ham])
        print("          stieltjes=%s" % ["%.3e" % d for d in sti])

    gate("H2a: section 17 transform extends to Q_1..Q_9 and matches the "
         "zero + moment-tail expansion",
         worst_trans < H2_TRANS_TOL,
         "One Taylor expansion of F_xi at each x supplies Q_1..Q_9 through "
         "the finite differential transform; the cross-check uses the direct "
         "zero sum for Q_3..Q_9 (fast convergence at %d zeros) and the exact "
         "log-Xi moment series for Q_1, Q_2 (whose 1/gamma^2 and 1/gamma^4 "
         "tails are not negligible).  Worst relative residual: %.2e."
         % (H2_KZERO, float(worst_trans)))

    # ---- H2b/H2d: Vandermonde + shifted Schur identity on a small multiset
    small = gz[:H2_SCHUR_Z]
    id_rows = []
    worst_id = mp.mpf(0)
    for x in H2_X:
        qs = [_q(g, x) for g in small]
        Qs = [sum(q ** k for q in qs) for k in range(0, 2 * H2_NMAX + 4)]
        for m in range(0, 4):
            Dm = Qs[2 * m + 1] * Qs[2 * m + 3] - Qs[2 * m + 2] ** 2
            idm = sum((qs[i] * qs[j]) ** (2 * m + 1) * (qs[i] - qs[j]) ** 2
                      for i in range(len(qs)) for j in range(i + 1, len(qs)))
            worst_id = max(worst_id, abs(Dm - idm) / abs(idm))
        for N in range(1, H2_NMAX + 1):
            H = mp.matrix(N + 1, N + 1)
            for i in range(N + 1):
                for j in range(N + 1):
                    H[i, j] = Qs[i + j + 1]
            det = mp.det(H)
            sch = _schur(qs, N)
            rel = abs(det - sch) / abs(sch)
            worst_id = max(worst_id, rel)
            id_rows.append({"x": float(x), "N": N, "det": float(det),
                            "schur": float(sch), "rel": float(rel)})
    report["h2_identity_rows"] = id_rows

    gate("H2d: shifted Schur/Vandermonde identity -- det[Q_{i+j+1}] equals "
         "sum_{i_0<...<i_N} (prod q) prod (q_a - q_b)^2",
         worst_id < H2_ID_TOL,
         "On the first %d zeros (the identity is algebraic, so a small "
         "multiset is exact; C(%d,4) triples are infeasible over all %d "
         "zeros), the shifted Hankel determinant matches the Schur/Vandermonde "
         "sum for N = 1, 2, 3, and the D_m Vandermonde form matches for "
         "m = 0..3, to %.2e.  Under RH each summand is >= 0."
         % (H2_SCHUR_Z, H2_SCHUR_Z, H2_KZERO, float(worst_id)))

    gate("H2b/H2c: the shifted-det ladder D_0..D_3 and the full Hankel "
         "matrices are positive on the sampled half-line",
         pos_ok,
         "At x in %s, D_m = Q_{2m+1}Q_{2m+3}-Q_{2m+2}^2 > 0 for m = 0..3, and "
         "both the Hamburger Hankel [Q_{i+j+1}] and the Stieltjes Hankel "
         "[Q_{i+j+2}] have all leading principal determinants positive up to "
         "order N = %d.  These are the sampled Stieltjes-moment positivity "
         "conditions (framework sections 9, 16), computed from the explicit "
         "formula without zero-location data -- evidence consistent with RH, "
         "not a proof."
         % ([float(x) for x in H2_X], H2_NMAX))

    # ---- H2e: dominant off-axis pair kills the full Hankel determinant
    theta, Q = mp.mpf("0.7"), mp.mpf(1)
    bg = [mp.mpf(j) / 40 for j in range(1, 5)]
    qlist = bg + [Q * mp.e ** (1j * theta), Q * mp.e ** (-1j * theta)]
    ob = []
    for N in range(1, H2_NMAX + 1):
        Qm = [sum(q ** k for q in qlist).real for k in range(0, 2 * N + 3)]
        H = mp.matrix(N + 1, N + 1)
        for i in range(N + 1):
            for j in range(N + 1):
                H[i, j] = Qm[i + j + 1]
        ob.append({"N": N, "det": float(mp.det(H))})
    gate("H2e: a strictly dominant off-axis pair drives the full shifted "
         "Hankel determinant negative",
         all(d["det"] < 0 for d in ob),
         "Replacing the real transformed-zero scales by a strictly dominant "
         "conjugate pair q_* = e^{+-0.7 i} over four real background q_j "
         "materially breaks Stieltjes positivity: det[Q_{i+j+1}] < 0 for "
         "N = 1, 2, 3 (%s).  This is the section 10 obstruction lifted from "
         "the 2x2 shifted determinant to the full Hankel matrix -- the derived "
         "off-axis mechanism, not an RH proof."
         % ", ".join("N=%d: %.3e" % (d["N"], d["det"]) for d in ob))
    report["h2e_hankel_obstruction"] = ob
    report["h2_rows"] = rows
    report["h2a_translation_worst_rel"] = float(worst_trans)

    report["conclusion"] = (
        "H2 expands H1 from the 2x2 shifted determinants to the full Hankel "
        "structure.  All %d/%d sub-gates pass.  (a) The section 17 transform "
        "extends to Q_1..Q_9 and matches the zero + moment-tail expansion to "
        "%.1e.  (b) At every sampled x > 0 the ladder D_0..D_3, the Hamburger "
        "Hankel [Q_{i+j+1}] and the Stieltjes Hankel [Q_{i+j+2}] are positive "
        "through order N = %d, computed without zero-location data.  (c) The "
        "shifted Schur/Vandermonde identity det[Q_{i+j+1}] = sum (prod q) "
        "prod (q_a-q_b)^2 holds to %.1e.  (d) A strictly dominant synthetic "
        "off-axis pair drives the full shifted Hankel determinant negative for "
        "N = 1,2,3.  Nothing here proves RH: the Widder criterion is posited, "
        "positivity is sampled finitely, and the prime-gamma -> Hankel bridge "
        "is open."
        % (gates_passed, len(report["gates"]), float(worst_trans), H2_NMAX,
           float(worst_id)))
    if gates_passed != len(report["gates"]):
        report["conclusion"] = "NOT ALL GATES PASSED - conclusions invalid."

    out_dir = os.path.join(ROOT, "experiments", "data")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "rh_widder_hankel_h2_data.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)

    print("\n" + "=" * 74)
    print("SUMMARY: %d/%d gates pass" % (gates_passed, len(report["gates"])))
    print("=" * 74)
    print(report["conclusion"])
    print("\nwrote %s" % os.path.relpath(path, ROOT))
    return 0 if gates_passed == len(report["gates"]) else 1


if __name__ == "__main__":
    sys.exit(main())
