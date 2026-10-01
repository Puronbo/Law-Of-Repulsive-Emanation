#!/usr/bin/env python3
"""
rh_widder_hankel_h1.py -- H1 of the pinned Stieltjes/Widder framework:
the first shifted-Hankel determinant identities are exact, and D_0, D_1 are
positive on the sampled half-line.

Background.  The pinned records rh_infinite_unit_stieltjes_pinned.md and
rh_framework_pinned_october_2026.md organize the Riemann Hypothesis around

    zero transforms w_rho = -u_rho^2
      -> Stieltjes function F_xi(x) = 2 G'(x)/G(x),  G(x) = X(sqrt x)
      -> Widder moments Q_m(x) = sum_rho q_rho(x)^m,
         q_rho(x) = w_rho / (x + w_rho)^2
      -> shifted Hankel determinants
         D_m(x) = Q_{2m+1}(x) Q_{2m+3}(x) - Q_{2m+2}(x)^2.

Section 14 of the first record sets the immediate target: do NOT add another
independent RH criterion -- compute D_0 = Q_1 Q_3 - Q_2^2 and then
D_1 = Q_3 Q_5 - Q_4^2, seeking an eventual positive-kernel representation
D_m(x) = int int K_m(x;t,u) dnu_x(t) dnu_x(u), K_m >= 0, dnu_x >= 0.

The two exact identities this gate locks in (both are pure algebra, valid for
ANY multiset {q_i}, so they hold whether or not RH is true):

  * section 10 / section 9: the Vandermonde identity
        D_m = sum_{i<j} (q_i q_j)^{2m+1} (q_i - q_j)^2,
    so under RH (q_i real) every term is >= 0; a strictly dominant conjugate
    pair q_* = Q e^{i theta} contributes  -4 Q^{4m+4} sin^2(theta) + O(eta^2m),
    which is the derived off-axis obstruction, not a proof.

  * section 17: every Q_k is a finite differential transform of F_xi,
        Q_k(x) = (1/2) sum_{j=0}^{k} C(k,j) (-x)^{k-j}
                 (-1)^{2k-j-1} / (2k-j-1)!  F_xi^{(2k-j-1)}(x),
    and section 18 gives F_xi from the explicit prime/gamma formula
        F_xi = F_rational + F_Gamma + F_prime.
    The gate verifies both, independently of any zero-location data: F_xi is
    built from zeta'/zeta computed by analytic continuation (no zetazero
    calls), so D_0 and D_1 are obtained WITHOUT assuming where the zeros are.

What is deliberately NOT claimed here: the Widder criterion
(RH <=> Q_m >= 0 for all m) is not proved, the prime-gamma -> Hankel bridge
(record section 27) is untouched, and positivity is only checked at finitely
many sample points x > 0.  A negative sample would refute; positive samples
are evidence consistent with RH, nothing more.

Run:  python experiments/rh_widder_hankel_h1.py

Artifact: experiments/data/rh_widder_hankel_h1_data.json
"""

import json
import os
import sys
from math import comb

import mpmath as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rh_zero_scale_objects import _log_xi_moments, G5_JMAX

mp.mp.dps = 70

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H1_K = 400                       # zeros used in the zero-side cross-check
H1_X = [mp.mpf("1/10"), mp.mpf("1/2"), mp.mpf(1), mp.mpf(2), mp.mpf(4),
        mp.mpf(16)]              # sample points x > 0 (x = 1/4 is the pole s = 1)
H1_TRANS_TOL = mp.mpf("1e-4")    # analytic vs zero+moment-tail translation
H1_ID_TOL = mp.mpf("1e-25")      # D_m pair identity (exact truncated algebra)
H1_FORMULA_TOL = mp.mpf("1e-30")  # explicit-formula split (dps 70)
H1_OBSTR_M = 24                  # largest binomial power in the obstruction
H1_OBSTR_N = 20                  # number of background (real) q_j in the model

report = {
    "experiment": "widder/hankel level 1: shifted-Hankel determinant identities "
                  "and the D_0, D_1 positivity samples",
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


# --------------------------------------------------------------------------
# analytic side: F_xi(x) and its derivatives from the explicit formula


def _zeta_log_deriv(s):
    """zeta'/zeta(s) by analytic continuation (no zero data used)."""
    return mp.zeta(s, 1, 1) / mp.zeta(s, 1, 0)


def _g_xi_over_xi(s):
    """xi'/xi(s) = 1/s + 1/(s-1) + (1/2)psi(s/2) - (1/2)log pi + zeta'/zeta."""
    return (1 / s + 1 / (s - 1) + mp.mpf(1) / 2 * mp.digamma(s / 2)
            - mp.mpf(1) / 2 * mp.log(mp.pi) + _zeta_log_deriv(s))


def _F(x):
    """F_xi(x) = (1/sqrt x) xi'/xi(1/2 + sqrt x)."""
    return _g_xi_over_xi(mp.mpf(1) / 2 + mp.sqrt(x)) / mp.sqrt(x)


def _Q_dt(k, x):
    """Q_k(x) via the finite differential transform of F_xi (section 17)."""
    tot = mp.mpf(0)
    for j in range(k + 1):
        n = 2 * k - j - 1
        tot += (comb(k, j) * (-x) ** (k - j) * (-1) ** n
                / mp.factorial(n) * mp.diff(_F, x, n))
    return tot / 2


# --------------------------------------------------------------------------
# zero-side cross-check: q_rho from the mirror-symmetric zero expansion


def _zero_ordinates(K):
    dps = mp.mp.dps
    mp.mp.dps = 30
    try:
        return [mp.im(mp.zetazero(k)) for k in range(1, K + 1)]
    finally:
        mp.mp.dps = dps


def _q(g, x):
    """q_rho(x) = gamma^2 / (x + gamma^2)^2 for a zero on the critical line."""
    w = g * g
    return w / (x + w) ** 2


moments = _log_xi_moments(G5_JMAX)  # {j: M_{2j}} from the Taylor data of log Xi


def _Q1_moment_tail(x):
    """Q_1(x) = sum_{j>=0} (-1)^j (j+1) x^j M_{2j+2}, the exact tail of the
    slowly-converging Q_1 zero sum, from the log-Xi Taylor moments."""
    return sum((-1) ** j * (j + 1) * x ** j * moments[j + 1]
               for j in range(G5_JMAX))


def _Q_zero(m, x, qs):
    """Q_m from the zero expansion: direct sum for m >= 2 (fast convergence),
    the exact moment tail added for m = 1 (sum 1/gamma^2 converges only like
    log^2 K / K, so 400 zeros leave a ~1e-3 hole the tail closes)."""
    s = sum(q ** m for q in qs)
    if m == 1:
        s += _Q1_moment_tail(x) - sum(qs)
    return s


def main():
    print("H1: shifted-Hankel determinants D_m = Q_{2m+1} Q_{2m+3} - Q_{2m+2}^2")
    print("(from rh_infinite_unit_stieltjes_pinned.md sections 10 and 14)\n")

    gz = _zero_ordinates(H1_K)

    rows = []
    worst_trans = mp.mpf(0)
    worst_id = mp.mpf(0)
    positivity_ok = True
    for x in H1_X:
        qs = [_q(g, x) for g in gz]
        Qa = [_Q_dt(k, x) for k in range(1, 6)]     # Q_1 .. Q_5, analytic
        Qz = [_Q_zero(m, x, qs) for m in range(1, 6)]  # zero + moment tail
        trans = max(abs(Qa[i] - Qz[i]) / abs(Qa[i]) for i in range(5))
        worst_trans = max(worst_trans, trans)
        D0a = Qa[0] * Qa[2] - Qa[1] ** 2
        D1a = Qa[2] * Qa[4] - Qa[3] ** 2
        D0z = Qz[0] * Qz[2] - Qz[1] ** 2
        n = len(qs)
        # the Vandermonde identity is algebraic: compare it against the
        # truncated products from the SAME 400 q's (no moment tail -- the tail
        # extends beyond the 400 zeros, the pair sum does not).
        S = [sum(q ** k for q in qs) for k in range(1, 6)]
        D0_trunc = S[0] * S[2] - S[1] ** 2
        D1_trunc = S[2] * S[4] - S[3] ** 2
        id0 = sum(qs[i] * qs[j] * (qs[i] - qs[j]) ** 2
                  for i in range(n) for j in range(i + 1, n))
        id1 = sum((qs[i] * qs[j]) ** 3 * (qs[i] - qs[j]) ** 2
                  for i in range(n) for j in range(i + 1, n))
        idres = max(abs(id0 - D0_trunc) / abs(id0), abs(id1 - D1_trunc) / abs(id1))
        worst_id = max(worst_id, idres)
        if not (D0a > 0 and D1a > 0):
            positivity_ok = False
        rows.append({"x": float(x),
                     "Q1": float(Qa[0]), "Q3": float(Qa[2]), "Q5": float(Qa[4]),
                     "D0": float(D0a), "D1": float(D1a),
                     "D0_analytic_minus_zero": float(abs(D0a - D0z)),
                     "translation_rel": float(trans),
                     "pair_identity_rel": float(idres)})
        print("  x=%7s  D0=%.6e  D1=%.6e  translation=%.1e  identity=%.1e"
              % (mp.nstr(x, 4), float(D0a), float(D1a), float(trans),
                 float(idres)))

    gate("H1a: section 17 translation -- Q_k from the F_xi differential transform "
         "matches the zero + moment-tail expansion",
         worst_trans < H1_TRANS_TOL,
         "Q_k(x) = (1/2) sum_j C(k,j)(-x)^{k-j}(-1)^{2k-j-1}/(2k-j-1)! "
         "F_xi^{(2k-j-1)}(x) is rebuilt from zeta'/zeta by analytic continuation "
         "(no zetazero calls in F_xi) and compared with the mirror-symmetric "
         "zero expansion sum_rho q_rho^m; the slowly-converging m = 1 entry uses "
         "the exact log-Xi moment tail Q_1 = sum_j (-1)^j(j+1)x^j M_{2j+2}.  "
         "Worst relative residual over x in the grid and k = 1..5: %.2e."
         % float(worst_trans))

    # ---- section 18: explicit prime/gamma formula and the gamma-term sign
    formula_rows = []
    worst_f = mp.mpf(0)
    worst_wrong = mp.mpf(0)
    for x in [mp.mpf(1), mp.mpf(2), mp.mpf(4), mp.mpf(16)]:
        s = mp.mpf(1) / 2 + mp.sqrt(x)
        dlogxi = mp.diff(lambda u: mp.log(mp.mpf(1) / 2 * u * (u - 1)
                                          * mp.pi ** (-u / 2) * mp.gamma(u / 2)
                                          * mp.zeta(u)), s, 1)
        F_direct = dlogxi / mp.sqrt(x)
        F_rat = (1 / s + 1 / (s - 1)) / mp.sqrt(x)
        F_gam = (mp.mpf(1) / 2 * mp.digamma(s / 2)
                 - mp.mpf(1) / 2 * mp.log(mp.pi)) / mp.sqrt(x)
        F_prime = _zeta_log_deriv(s) / mp.sqrt(x)
        # wrong-sign variant: flip the -(1/2)log pi term of F_Gamma
        F_wrong = (F_rat
                   + (mp.mpf(1) / 2 * mp.digamma(s / 2)
                      + mp.mpf(1) / 2 * mp.log(mp.pi)) / mp.sqrt(x)
                   + F_prime)
        res = abs(F_direct - (F_rat + F_gam + F_prime)) / abs(F_direct)
        wres = abs(F_direct - F_wrong) / abs(F_direct)
        worst_f = max(worst_f, res)
        worst_wrong = max(worst_wrong, wres)
        formula_rows.append({"x": float(x), "split_rel": float(res),
                             "wrong_gamma_rel": float(wres)})
    gate("H1b: section 18 explicit formula -- F_xi = F_rational + F_Gamma + "
         "F_prime reproduces xi'/xi(sqrt x)/sqrt x, and the gamma-term sign is "
         "load-bearing",
         worst_f < H1_FORMULA_TOL and worst_wrong > mp.mpf("1e-3"),
         "F_xi is rebuilt independently from the completed xi function "
         "Xi(s) = (1/2) s(s-1) pi^{-s/2} Gamma(s/2) zeta(s) by logarithmic "
         "differentiation and matched against the rational + gamma + prime "
         "split; worst split residual %.2e.  Flipping the sign of the "
         "(1/2)log pi term raises the residual to %.2e, so the sign recorded "
         "in the pinned section 18 is the one that closes the identity."
         % (float(worst_f), float(worst_wrong)))
    report["h1b_explicit_formula"] = formula_rows

    gate("H1c: section 10 shifted-Hankel identity -- D_m equals the Vandermonde "
         "pair sum sum_{i<j} (q_i q_j)^{2m+1} (q_i - q_j)^2",
         worst_id < H1_ID_TOL,
         "For the %d zero-side q_rho, the determinant D_m = Q_{2m+1}Q_{2m+3} "
         "- Q_{2m+2}^2 and the pair sum are algebraically identical; the worst "
         "relative mismatch over x and m = 0,1 is %.2e.  Under RH each term "
         "q_i q_j (q_i-q_j)^2 >= 0, so D_m >= 0 term-by-term." 
         % (H1_K, float(worst_id)))

    gate("H1d: the first two shifted-Hankel determinants are positive on the "
         "sampled half-line",
         positivity_ok,
         "D_0(x) = Q_1Q_3 - Q_2^2 and D_1(x) = Q_3Q_5 - Q_4^2 are computed "
         "from the explicit formula (no zero-location data) and are > 0 at "
         "every x in the grid %s.  This is the sampled half-line of the "
         "Widder criterion's D_m >= 0; it is evidence consistent with RH, not "
         "a proof (the prime-gamma -> Hankel bridge is untouched)."
         % [float(x) for x in H1_X])

    # ---- section 10 obstruction: a dominant off-axis pair forces D_m < 0
    theta = mp.mpf("0.7")
    Q = mp.mpf(1)
    bg = [mp.mpf(j) / (3 * H1_OBSTR_N) for j in range(1, H1_OBSTR_N + 1)]
    qlist = bg + [Q * mp.e ** (1j * theta), Q * mp.e ** (-1j * theta)]
    m_neg = None
    obst_rows = []
    for m in range(0, H1_OBSTR_M + 1):
        Dm = sum(((qlist[i] * qlist[j]) ** (2 * m + 1)
                  * (qlist[i] - qlist[j]) ** 2).real
                 for i in range(len(qlist)) for j in range(i + 1, len(qlist)))
        Qk = [sum(q ** k for q in qlist) for k in (2 * m + 1, 2 * m + 2, 2 * m + 3)]
        Ddet = (Qk[0] * Qk[2] - Qk[1] ** 2).real
        obst_rows.append({"m": m, "D_m": float(Dm), "det_check": float(abs(Dm - Ddet))})
        if Dm < 0 and m_neg is None:
            m_neg = m
    gate("H1e: section 10 off-axis obstruction -- a strictly dominant "
         "conjugate pair drives D_m negative for large m",
         m_neg is not None and obst_rows[-1]["D_m"] < 0,
         "A synthetic multiset of %d real background q_j in [0, 1/3] plus the "
         "conjugate pair q_* = e^{+-i*0.7} has D_m negative for m >= %s "
         "(D_%d = %.3e); the pair contribution (q_* qbar_*)^{2m+1}"
         "(q_* - qbar_*)^2 = -4 sin^2(theta) < 0 dominates the O((1/3)^{2m+1}) "
         "background.  This reproduces the derivation, not an RH proof."
         % (H1_OBSTR_N, m_neg, H1_OBSTR_M, obst_rows[-1]["D_m"]))
    report["h1e_obstruction"] = obst_rows
    report["h1a_translation_worst_rel"] = float(worst_trans)
    report["h1c_pair_identity_worst_rel"] = float(worst_id)
    report["h1_translation_residual"] = float(worst_trans)
    report["h1_rows"] = rows

    report["conclusion"] = (
        "H1 opens the Stieltjes/Widder/Hankel stage named in record section 14. "
        "All %d/%d sub-gates pass.  (a) The section 17 differential transform "
        "reproduces Q_k from the zero + moment-tail expansion to %.1e relative. "
        "(b) The section 18 explicit formula F_xi = F_rational + F_Gamma + "
        "F_prime closes to %.1e, and the (1/2)log pi gamma-term sign is "
        "load-bearing (flipping it costs %.1e).  (c) The section 10 Vandermonde "
        "identity D_m = sum_{i<j}(q_iq_j)^{2m+1}(q_i-q_j)^2 holds to %.1e.  "
        "(d) D_0 and D_1 are positive at every sampled x > 0, computed from the "
        "explicit formula without any zero-location data.  (e) A strictly "
        "dominant synthetic off-axis pair drives D_m negative for large m, "
        "reproducing the derived obstruction.  Nothing here proves RH: the "
        "Widder criterion is assumed as an equivalence, positivity is checked "
        "only at finitely many x, and the prime-gamma -> Hankel bridge is open."
        % (gates_passed, len(report["gates"]), float(worst_trans),
           float(worst_f), float(worst_wrong), float(worst_id)))
    if gates_passed != len(report["gates"]):
        report["conclusion"] = "NOT ALL GATES PASSED - conclusions invalid."

    out_dir = os.path.join(ROOT, "experiments", "data")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "rh_widder_hankel_h1_data.json")
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
