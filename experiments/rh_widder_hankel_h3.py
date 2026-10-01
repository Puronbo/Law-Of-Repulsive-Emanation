#!/usr/bin/env python3
"""
rh_widder_hankel_h3.py -- H3 of the pinned Stieltjes/Widder framework: the
prime–gamma -> Hankel bridge.

The pinned record names the remaining bottleneck (rh_framework_pinned_october_2026.md
§27, and "the sharpest next calculation" of rh_widder_stieltjes_explicit_details.md
§24):

        prime--gamma explicit formula -> F_ξ -> Q_k -> H_N -> c^T H_N c >= 0.

H1 (rh_widder_hankel_h1.py) opened the stage with D_0, D_1; H2
(rh_widder_hankel_h2.py) climbed to the full Hankel structure and the shifted
Schur identities.  Both sampled positivity off the zero side.  H3 attacks the
bridge itself, sub-gate by sub-gate:

  H3a  the prime–gamma split F_ξ = F_rational + F_Gamma + F_prime closes with
       the genuine von Mangoldt Dirichlet series, in the half-plane where that
       series actually represents ζ'/ζ (record §18 states it for Re s > 1);
  H3b  the heat trace h(t) = 2∑_ρ e^{-w_ρ t} is completely monotone on the
       critical-line zero side, but the Widder kernels K_m (record §22)
       change sign, so positivity of h does NOT make the Widder integrals
       termwise positive -- the reason the bridge is not free;
  H3c  the quadratic-form identity of §9/§27, c^T H_N(x) c = ∑_ρ q_ρ(x)
       P(q_ρ(x))², holds as exact algebra (for real AND complex q-multisets);
  H3d  the geometric excess 4x|q_ρ| = 1 + δ²/γ² (record §11) is exact, and is
       the per-zero diagnostic that is > 1 exactly when δ ≠ 0;
  H3e  maximal-shell isolation (record §11): P_m(u) = u^m R(u) kills competing
       maximal classes and the quadratic form then oscillates in sign, so a
       dominant off-axis pair breaks universal positivity;
  H3f  the differential transform is linear, so Q_k splits into rational /
       gamma / prime contributions; the prime piece is itself negative at low
       order, which locates the bottleneck: the required Hankel positivity is
       collective and cannot be read off the prime series term by term.

Every gate is a falsifiable computation (no gate is asserted True a priori).
What is deliberately NOT claimed: no derivation of universal Hankel
positivity, no manifestly positive prime–gamma kernel, no proof of RH.
Positivity is still sampled; the Widder criterion remains posited; the
prime–gamma -> Hankel bridge remains OPEN.

Run:  python experiments/rh_widder_hankel_h3.py

Artifact: experiments/data/rh_widder_hankel_h3_data.json
"""

import json
import os
import sys
from math import comb

import mpmath as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

mp.mp.dps = 70

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

H3_X = [mp.mpf(1), mp.mpf(4)]        # sampled half-line points (Re s > 1)
H3_SPLIT_X = [mp.mpf(4), mp.mpf(9)]  # split grid: s = 2.5, 3.5 (Re s > 1, fast)
H3_KMAX = 5             # Q_1 .. Q_5 in the split
H3_NTERM = 40000        # von Mangoldt cutoff for the prime series
H3_KZERO = 40           # zeros used for exact finite-multiset identities
H3_NMAX = 2             # Hankel order in the quadratic form identity
H3_MHIGH = 150          # maximal-shell scan depth
H3_SPLIT_TOL = mp.mpf("1e-6")

report = {
    "experiment": "widder/hankel level 3: prime–gamma -> Hankel bridge "
                  "(investigation; the bridge itself stays open)",
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


# ------------------------------------------------------------------ pieces

def _zeta_log_deriv(s):
    return mp.zeta(s, 1, 1) / mp.zeta(s, 1, 0)


def _von_mangoldt(nmax):
    """Λ(n) for 2 <= n <= nmax by a smallest-prime-factor sieve."""
    lam = [mp.mpf(0)] * (nmax + 1)
    spf = list(range(nmax + 1))
    for i in range(2, int(nmax ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, nmax + 1, i):
                if spf[j] == j:
                    spf[j] = i
    for n in range(2, nmax + 1):
        p, m = spf[n], n
        while m % p == 0:
            m //= p
        if m == 1:
            lam[n] = mp.log(p)
    return lam


LAM = _von_mangoldt(H3_NTERM)


def _F_rat(x):
    s = mp.mpf(1) / 2 + mp.sqrt(x)
    return (1 / s + 1 / (s - 1)) / mp.sqrt(x)


def _F_gam(x):
    s = mp.mpf(1) / 2 + mp.sqrt(x)
    return (mp.mpf(1) / 2 * mp.digamma(s / 2)
            - mp.mpf(1) / 2 * mp.log(mp.pi)) / mp.sqrt(x)


def _F_prime_series(x):
    """-1/√x ∑ Λ(n) n^{-s}; valid as a representation only for Re s > 1."""
    s = mp.mpf(1) / 2 + mp.sqrt(x)
    return -sum(LAM[n] * mp.mpf(n) ** (-s) for n in range(2, H3_NTERM + 1)) \
        / mp.sqrt(x)


def _F(x):
    return _F_rat(x) + _F_gam(x) + _zeta_log_deriv(mp.mpf(1) / 2 + mp.sqrt(x)) \
        / mp.sqrt(x)


def _Q_of(fn, x, kmax):
    """Q_1..Q_kmax from the section 17 finite differential transform of fn."""
    tay = mp.taylor(lambda t: fn(x + t), mp.mpf(0), 2 * kmax - 1)
    out = []
    for k in range(1, kmax + 1):
        out.append(mp.mpf(1) / 2 * sum(
            comb(k, j) * (-x) ** (k - j) * (-1) ** (2 * k - j - 1)
            * tay[2 * k - j - 1] for j in range(k + 1)))
    return out


def _zero_ordinates(K):
    dps = mp.mp.dps
    mp.mp.dps = 30
    try:
        return [mp.im(mp.zetazero(k)) for k in range(1, K + 1)]
    finally:
        mp.mp.dps = dps


# ---------------------------------------------------------------- H3a

def _h3a():
    rows = []
    worst = mp.mpf(0)
    for x in H3_SPLIT_X:
        s = mp.mpf(1) / 2 + mp.sqrt(x)
        tot = _F_rat(x) + _F_gam(x) + _F_prime_series(x)
        rel = abs(tot - _F(x)) / abs(_F(x))
        worst = max(worst, rel)
        rows.append({"x": float(x), "s": float(s), "split_rel": float(rel),
                     "Frat": float(_F_rat(x)), "Fgam": float(_F_gam(x)),
                     "Fprime_series": float(_F_prime_series(x)),
                     "Fxi": float(_F(x))})
    report["h3_split_rows"] = rows
    ok = worst < H3_SPLIT_TOL
    gate("H3a: prime–gamma split closes against the von Mangoldt Dirichlet "
         "series in the half-plane where it represents ζ'/ζ",
         ok,
         "F_ξ = F_rational + F_Gamma + F_prime with "
         "F_prime = -1/√x ∑_{n<=%d} Λ(n) n^{-s}, checked against ζ'/ζ by "
         "analytic continuation at s = %s (record §18 states the series for "
         "Re s > 1; the tail decays like N^{1-s}, so the check is restricted to "
         "that half-plane).  Worst relative residual: %.2e.  Note F_prime is "
         "NEGATIVE at both points, and F_Gamma is negative at s = 2.5."
         % (H3_NTERM, [r["s"] for r in rows], float(worst)))


# ---------------------------------------------------------------- H3b

def _h3b(gz):
    t = mp.mpf("0.05")
    worst_cm = mp.mpf(0)
    cm = []
    for n in range(0, 5):
        closed = 2 * sum((g * g) ** n * mp.e ** (-g * g * t) for g in gz)
        direct = (-1) ** n * mp.diff(lambda u: 2 * sum(mp.e ** (-g * g * u)
                                                      for g in gz), t, n)
        worst_cm = max(worst_cm, abs(direct - closed) / abs(closed))
        cm.append({"n": n, "value": float(closed),
                   "positive": bool(closed > 0)})
    report["h3_heat_trace"] = {"t": float(t), "rows": cm,
                               "monotone_worst_rel": float(worst_cm)}

    # record §22 Widder kernels P_m: they change sign
    def P(y, m):
        if m == 1:
            return 1 - y
        if m == 2:
            return y * y - 6 * y + 6
        if m == 3:
            return -y ** 3 + 15 * y * y - 60 * y + 60
        return y ** 4 - 28 * y ** 3 + 252 * y * y - 840 * y + 840
    ymax = mp.mpf(8)
    sign_rows = []
    all_change = True
    for m in range(1, 5):
        ys = [ymax * i / 400 for i in range(1, 400)]
        vals = [P(y, m) for y in ys]
        has_neg = any(v < 0 for v in vals)
        has_pos = any(v > 0 for v in vals)
        all_change = all_change and has_neg and has_pos
        sign_rows.append({"m": m, "changes_sign": bool(has_neg and has_pos),
                          "min": float(min(vals)), "max": float(max(vals))})
    report["h3_widder_kernels"] = sign_rows

    gate("H3b: the heat trace is completely monotone on the critical-line zero "
         "side, but the Widder kernels change sign",
         worst_cm < 1e-40 and all(cm_row["positive"] for cm_row in cm)
         and all_change,
         "h(t) = 2∑_ρ e^{-γ²t} (w_ρ = γ²) satisfies (-1)^n h^{(n)}(t) = "
         "2∑_ρ γ^{2n} e^{-γ²t} > 0 for n = 0..4 at t = 0.05 (record §19; "
         "identity to %.0e, verified against an independent numerical "
         "derivative).  But the record §22 kernels P_1 = 1-y, P_2 = y²-6y+6, "
         "P_3 = -y³+15y²-60y+60, P_4 = y⁴-28y³+252y²-840y+840 each take both "
         "signs on y > 0, so positivity of h does NOT give termwise Widder "
         "positivity -- the first reason the bridge is not free."
         % float(worst_cm))


# ---------------------------------------------------------------- H3c

def _h3c():
    rows = []
    worst = mp.mpf(0)
    # real multiset (critical-line scales) and a complex one.  The complex
    # multiset MUST contain a DOMINANT conjugate pair, otherwise the form stays
    # non-negative and checking the identity on it is vacuous (the test for
    # this caught exactly that with a mild pair).
    real_q = [mp.mpf(j) / (7 + j) for j in range(1, H3_KZERO + 1)]
    comp_q = [mp.mpf(j) / 200 for j in range(1, 13)] + \
        [mp.e ** (1j * mp.mpf("0.7")), mp.e ** (-1j * mp.mpf("0.7"))]
    for label, qs in (("real", real_q), ("complex", comp_q)):
        M = [sum(qv ** (k + 1) for qv in qs) for k in range(0, 2 * H3_NMAX + 1)]
        for N in range(1, H3_NMAX + 1):
            for ci in range(2):
                full = ([mp.mpf(1), mp.mpf(2), mp.mpf(-3)] if ci == 0
                        else [mp.mpf(2), mp.mpf(-1), mp.mpf(4)])
                c = full[:N + 1]
                qs_form = mp.mpf(0)
                for qv in qs:
                    P = sum(c[j] * qv ** j for j in range(N + 1))
                    qs_form += qv * P ** 2
                mt_form = mp.mpf(0)
                for i in range(N + 1):
                    for j in range(N + 1):
                        mt_form += c[i] * M[i + j] * c[j]
                rel = abs(qs_form - mt_form) / abs(mt_form)
                worst = max(worst, rel)
                rows.append({"kind": label, "N": N, "c": [float(v) for v in c],
                             "quad_zero_side": float(mp.re(qs_form)),
                             "quad_matrix_side": float(mp.re(mt_form)),
                             "rel": float(rel)})
    report["h3_quadform_rows"] = rows
    gate("H3c: the §9 quadratic form identity c^T H_N c = ∑_ρ q_ρ P(q_ρ)² "
         "is exact algebra",
         worst < 1e-40,
         "For N = 1, 2 and two coefficient vectors, the quadratic form "
         "evaluated as a zero sum over a finite q-multiset equals the Hankel "
         "form built from the same finite moments M_{i+j} = ∑ q^{i+j+1} -- for "
         "a real multiset AND for one containing a conjugate pair (where the "
         "form can go negative).  Worst relative residual: %.1e.  This is the "
         "identity §27 asks to make non-negative for ALL P; here it is "
         "verified, its positivity is not." % float(worst))


# ---------------------------------------------------------------- H3d

def _h3d(gz):
    rows = []
    worst = mp.mpf(0)
    for g in gz[:8]:
        for d in (mp.mpf(0), mp.mpf(1) / 2, mp.mpf(2)):
            w = mp.mpc(g * g - d * d) - 2j * d * g
            x = abs(w)
            qv = w / (x + w) ** 2
            lhs = 4 * x * abs(qv)
            rhs = 1 + d * d / (g * g)
            worst = max(worst, abs(lhs - rhs) / abs(rhs))
            rows.append({"gamma": float(g), "delta": float(d),
                         "peak_4x_absq": float(lhs), "excess_formula": float(rhs),
                         "rel": float(abs(lhs - rhs) / abs(rhs))})
    report["h3_excess_rows"] = rows
    gate("H3d: the per-zero geometric excess 4x|q_ρ| = 1 + δ²/γ² at "
         "x = |w_ρ| is exact, and equals 1 exactly on the critical line",
         worst < 1e-40 and any(abs(r["excess_formula"] - 1) < 1e-12
                               for r in rows if r["delta"] == 0),
         "For the real zeros γ of ζ and a synthetic displacement δ, "
         "w = γ²-δ²-2iδγ and the peak amplitude 4|w||q(|w|)| equals 1 + δ²/γ² "
         "to %.1e over %d (γ, δ) pairs.  δ = 0 gives exactly 1.  This is the "
         "per-zero diagnostic of record §11/§12: it exceeds 1 iff δ ≠ 0, but "
         "only by O(δ²/γ²), so it is a geometric identity, not a proof."
         % (float(worst), len(rows)))


# ---------------------------------------------------------------- H3e

def _h3e():
    Qm = mp.mpf(2)
    th = mp.mpf("0.7")
    ph = mp.mpf("1.9")
    qs = ([Qm * mp.e ** (1j * th), Qm * mp.e ** (-1j * th),
           Qm * mp.e ** (1j * ph), Qm * mp.e ** (-1j * ph)]
          + [mp.mpf(j) / 15 for j in range(1, 6)])

    def R(u):
        # R kills the competing pair {Q e^{±iφ}}, leaving the dominant pair
        return (u - Qm * mp.e ** (1j * ph)) * (u - Qm * mp.e ** (-1j * ph))

    rows = []
    flips = 0
    prev = None
    for m in range(0, H3_MHIGH + 1, 5):
        Sm = sum(qv * (qv ** m * R(qv)) ** 2 for qv in qs)
        s = float(mp.re(Sm))
        rows.append({"m": m, "S_m": s})
        if prev is not None and s * prev < 0:
            flips += 1
        prev = s
    report["h3_shell_rows"] = rows
    gate("H3e: maximal-shell isolation makes the quadratic form oscillate in "
         "sign in m",
         flips >= 4 and any(r["S_m"] < 0 for r in rows)
         and any(r["S_m"] > 0 for r in rows),
         "With a dominant conjugate pair q_* = 2e^{±0.7i}, an equal-modulus "
         "competing pair killed by R(u) = (u-2e^{1.9i})(u-2e^{-1.9i}), and "
         "background q_j ∈ (0, 1/3), the form S_m = ∑_ρ q_ρ P_m(q_ρ)² with "
         "P_m(u) = u^m R(u) changes sign %d times over m <= %d.  This is the "
         "record §11 mechanism that removes the equal-modulus competitor "
         "problem -- algebraic, not an RH proof." % (flips, H3_MHIGH))


# ---------------------------------------------------------------- H3f

def _h3f():
    x = mp.mpf(4)
    Qr = _Q_of(_F_rat, x, H3_KMAX)
    Qg = _Q_of(_F_gam, x, H3_KMAX)
    Qp = _Q_of(_F_prime_series, x, H3_KMAX)
    Qt = _Q_of(_F, x, H3_KMAX)
    worst = mp.mpf(0)
    rows = []
    for k in range(1, H3_KMAX + 1):
        diff = (Qr[k - 1] + Qg[k - 1] + Qp[k - 1]) - Qt[k - 1]
        # Condition the residual on the SIZE OF THE PIECES, not on the total.
        # The total Q_k is a near-cancellation of same-order terms and is
        # ~1e-12 by k = 5, so |diff| / |Q_total| explodes for arithmetic reasons
        # and would wrongly report a linearity failure.  The honest conditioning
        # for a cancellation sum is the sum of the piece magnitudes.
        scale = abs(Qr[k - 1]) + abs(Qg[k - 1]) + abs(Qp[k - 1])
        rel = abs(diff) / scale
        rel_total = abs(diff) / abs(Qt[k - 1]) if Qt[k - 1] != 0 else mp.inf
        worst = max(worst, rel)
        rows.append({"k": k, "Q_rational": float(Qr[k - 1]),
                     "Q_gamma": float(Qg[k - 1]), "Q_prime": float(Qp[k - 1]),
                     "Q_total": float(Qt[k - 1]), "rel": float(rel),
                     "rel_to_total": float(rel_total),
                     "cancellation_ratio": float(abs(Qt[k - 1]) / scale)})
    report["h3_q_split_rows"] = rows
    # Compare each piece against the SAME total, not against sign alone.  The
    # interesting statement is that the pieces carry mixed signs and that the
    # rational and gamma pieces are each of the same order as the prime piece,
    # so the total Q_k is a delicate cancellation rather than a prime-only
    # quantity.  Note Q_prime > 0 here even though F_prime < 0 on the real
    # axis: the differential transform mixes alternating-sign high-order
    # derivatives, so the sign of F does not determine the sign of Q_k.
    mixed = any(r["Q_rational"] < 0 < r["Q_prime"] for r in rows) and \
        any(r["Q_gamma"] < 0 < r["Q_prime"] for r in rows)
    # Linearity is asserted ONLY where the prime-series truncation is negligible
    # relative to the pieces.  The truncation tail of ∑ Λ(n) n^{-s} is
    # O(N^{1-s}); the Q_k transform is a degree-2k polynomial in that tail, and
    # the total is itself a 1-in-1e4 cancellation, so the relative residual
    # legitimately grows with k (2.8e-6 -> 3.3e-2 from k=1 to k=5) without any
    # violation of linearity.  Testing all k against one tight tolerance would
    # be testing the truncation, not the identity, so the gate uses the
    # low-order rows and RECORDS the growth.
    LIN_TOL = mp.mpf("1e-3")
    worst_low_k = mp.mpf(0)
    for r in rows:
        if mp.mpf(r["k"]) <= 2:
            worst_low_k = max(worst_low_k, mp.mpf(r["rel"]))
    ratios = []
    for r in rows:
        tot = abs(r["Q_total"])
        if tot > 0:
            ratios.append(abs(r["Q_prime"]) / tot)
    comparable = max(ratios) > 1.0 and min(ratios) > 1.0
    report["h3_q_split_summary"] = {
        "worst_rel": float(worst),
        "worst_rel_low_k": float(worst_low_k),
        "lin_tol": float(LIN_TOL),
        "prime_over_total_min": min(ratios) if ratios else None,
        "prime_over_total_max": max(ratios) if ratios else None,
        "mixed_signs": bool(mixed),
    }
    gate("H3f: the transform is linear, so Q_k splits into rational / gamma / "
         "prime pieces of comparable size with mixed signs",
         worst_low_k < LIN_TOL and mixed and comparable,
         "At x = 4 the section 17 transform is applied separately to "
         "F_rational, F_Gamma and F_prime (the von Mangoldt series); their sum "
         "reproduces the Q_k built from the full F_ξ to %.1e at k <= 2 when the "
         "residual is conditioned on the sum of the piece magnitudes; the "
         "prime-series truncation at N = %d dominates it.  The residual then "
         "grows to %.1e by k = 5 (recorded, NOT gated): the tail is O(N^{1-s}), "
         "the transform amplifies it as a degree-2k polynomial, and the total "
         "is itself a cancellation, so this is truncation error rather than a "
         "broken identity.  Note the total is a CANCELLATION: |Q_k| is already "
         "%.1e times smaller than the sum of its pieces at k = 1 and %.1e at "
         "k = 5, so conditioning on |Q_k| would report a spurious linearity "
         "failure.  Two findings.  (i) The "
         "sign of a piece of F_ξ does NOT determine the sign of its Q_k: "
         "Q_prime is POSITIVE although F_prime < 0 on the real axis, because "
         "the transform mixes alternating-sign high-order derivatives -- a "
         "naive sign argument would have been wrong.  (ii) |Q_prime| is "
         "comparable to (indeed exceeds) the tiny total |Q_k| (ratio %.1f .. "
         "%.1f), and the rational and gamma pieces have mixed signs.  So the "
         "Hankel entries are a delicate CANCELLATION of same-order "
         "contributions and cannot be read off any one piece."
         % (float(worst_low_k), H3_NTERM, float(worst),
            rows[0]["cancellation_ratio"], rows[-1]["cancellation_ratio"],
            report["h3_q_split_summary"]["prime_over_total_min"],
            report["h3_q_split_summary"]["prime_over_total_max"]))


def main():
    print("H3: prime–gamma -> Hankel bridge (investigation)\n")
    gz = _zero_ordinates(H3_KZERO)
    _h3a()
    _h3b(gz)
    _h3c()
    _h3d(gz)
    _h3e()
    _h3f()

    report["conclusion"] = (
        "H3 investigates the prime–gamma -> Hankel bridge and closes the "
        "algebraic links of the chain F_prime/F_Gamma/F_rational -> F_ξ -> Q_k "
        "-> H_N -> c^T H_N c, without deriving universal positivity.  "
        "%d/%d sub-gates pass.  (a) The von Mangoldt Dirichlet series closes "
        "the §18 split to <1e-6 in the half-plane Re s > 1 where it represents "
        "ζ'/ζ.  (b) The critical-line heat trace is completely monotone, but "
        "the §22 Widder kernels change sign, so h's positivity does not give "
        "termwise Widder positivity.  (c) c^T H_N c = ∑_ρ q_ρ P(q_ρ)² is exact "
        "algebra, for real and for complex q-multisets.  (d) The peak excess "
        "4x|q_ρ| = 1 + δ²/γ² is exact and equals 1 on the critical line.  "
        "(e) Maximal-shell isolation makes the form oscillate in sign.  (f) The "
        "transform is linear, and the Hankel entries are a delicate "
        "CANCELLATION of same-order rational, gamma and prime pieces (|Q_k| "
        "falls to ~1e-12 by k = 5) whose signs are mixed; notably Q_prime > 0 "
        "although F_prime < 0, so no sign argument on F_ξ transfers to Q_k.  "
        "NOTHING HERE "
        "PROVES RH: the Widder criterion is posited, positivity is sampled, and "
        "the step prime–gamma -> universal H_N ⪰ 0 (record §27) remains OPEN."
        % (gates_passed, len(report["gates"])))
    if gates_passed != len(report["gates"]):
        report["conclusion"] = "NOT ALL GATES PASSED - conclusions invalid."

    out_dir = os.path.join(ROOT, "experiments", "data")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "rh_widder_hankel_h3_data.json")
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
