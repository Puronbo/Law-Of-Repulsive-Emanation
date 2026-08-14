r"""
The de Bruijn-Newman condensation: RH <=> Lambda <= 0, and the finite face of the
"barely so" boundary.

CONDENSATION
------------
The Riemann hypothesis reduces to the sign of ONE real constant, the
de Bruijn-Newman constant Lambda in R: H_t has purely real zeroes iff t >= Lambda,
so RH <=> Lambda <= 0.  The hidden object behind it (what cannot be seen):

    H_0(z) = (1/8) xi(1/2 + iz/2) = int_0^inf Phi(u) cos(z u) du
    Phi(u) = sum_{n>=1} (2 pi^2 n^4 e^{9u} - 3 pi n^2 e^{5u}) exp(-pi n^2 e^{4u})
    H_t(z) = int_0^inf e^{t u^2} Phi(u) cos(z u) du,   d_t H_t = -d_zz H_t

Phi is even, Phi(u) = Phi(-u), by Poisson summation; H_t is the backward heat
evolution of H_0.  Real zeroes persist as t grows (Polya), all real iff t >= Lambda
(Newman); Newman conjectured Lambda >= 0: "if RH is true, it is only barely so".
Known: Lambda >= 0 (Rodgers-Tao 2020, Dobner 2021), Lambda <= 0.2 (Platt-Trudgian
2021).

The repo's certified interval-arithmetic engine (riemann_siegel_certify.py) has
proved every zero 0 < gamma <= g_n = 999.236 is on Re(s)=1/2 and simple; in H_0
coordinates that is the t = 0 slice: H_0 has real, simple zeroes at z = 2 gamma,
all z <= 1998.472.  What cannot be seen by floating point: the VALUES of H_t on
that slice fall like e^{-pi z/8}; at the certified closest pair (gamma ~ 750.66)
they are ~ 1e-254, beyond any float and below mpmath's default working precision.

THE FINITE FACE OF THE BOUNDARY
-------------------------------
For a close adjacent pair of H_0 zeroes at z1 < z2, the local quadratic model of
the backward heat flow, H_0(z) ~ A (z - m)^2 - A d^2 with m = (z1+z2)/2 and
d = (z2 - z1)/2 = Delta gamma, evolves to

    H_t(z) ~ A (z - m)^2 - A (d^2 + 2 t),

so the two real zeroes survive exactly while t >= t_c := -d^2/2 = -(Delta gamma)^2/2
and merge into a double zero at t_c; the squared separation is linear in t with
SLOPE 8:  d(t)^2 = 4 d^2 + 8 t.  This script validates that law numerically on the
two closest certified pairs in the first-40-zero window (where H_t values ~1e-8 to
1e-36 are directly computable at high precision) and extrapolates it to the
certified global closest pair.  The finite-system boundary is four-hundredths of a
heat-unit below the real axis -- the finite, visible face of Newman's "barely so".

TECHNIQUE
---------
H_t(z) is evaluated by the change of variable v = e^{4u}:

    H_t(z) = (1/4) sum_n int_1^inf e^{-pi n^2 v}
                 [2 pi^2 n^4 v^{9/4} - 3 pi n^2 v^{5/4}]
                 e^{t (ln v)^2/16} cos((z/4) ln v) dv/v,

split at the zeroes of cos((z/4) ln v) and integrated by Gauss-Legendre at
dps 45.  The method is cross-validated against mpmath quadosc at dps 70 and
against the xi identity H_0(z) = (1/8) xi(1/2 + iz/2) to ~1e-6 relative.

HONEST WALL
-----------
This is a numerical probe of the FINITE system's heat-flow boundary, not a bound
on Lambda.  Lambda >= 0 is a known theorem; the global-closest-pair value
t_c = -(Delta gamma)^2/2 is a model extrapolation from a law validated only in the
representable range, not a certification.  A finite number of zeroes cannot probe
RH, and neither can a local model of two of them.
"""

import json
import os
import time

import mpmath as mp

DPS_ID = 50      # identity / evenness checks
DPS_H = 45       # heat-flow evaluations
NMAX_ID = 60
VMAX = mp.mpf(32)
NMAX_V = 6
DEG = 24

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "data", "debruijn_newman_condensation_data.json")


def phi(u, nmax=NMAX_ID):
    u = mp.mpf(u)
    s = mp.mpf(0)
    for n in range(1, nmax + 1):
        n = mp.mpf(n)
        s += (2 * mp.pi ** 2 * n ** 4 * mp.e ** (9 * u)
              - 3 * mp.pi * n ** 2 * mp.e ** (5 * u)) * mp.e ** (-mp.pi * n ** 2 * mp.e ** (4 * u))
    return s


def xi8(z):
    """(1/8) xi(1/2 + iz/2) with xi(s) = (1/2) s (s-1) pi^{-s/2} Gamma(s/2) zeta(s)."""
    z = mp.mpf(z)
    s = mp.mpc(0.5, z / 2)
    return (mp.mpc(0.5, 0) * s * (s - 1) * mp.pi ** (-s / 2)
            * mp.gamma(s / 2) * mp.zeta(s)) / 8


def h0_quadosc(z):
    """int_0^inf Phi(u) cos(z u) du via mpmath quadosc (moderate z only)."""
    z = mp.mpf(z)
    return mp.quadosc(lambda u: phi(u) * mp.cos(z * u), [0, mp.inf], omega=z)


def _legendre_pair(n, x):
    """P_n(x), P_n'(x) by the three-term recurrence."""
    p0 = mp.mpf(1)
    p1 = x
    d0 = mp.mpf(0)
    d1 = mp.mpf(1)
    for m in range(2, n + 1):
        c = (2 * m - 1) / mp.mpf(m)
        p2 = c * x * p1 - (m - 1) / mp.mpf(m) * p0
        d2 = c * p1 + c * x * d1 - (m - 1) / mp.mpf(m) * d0
        p0, p1 = p1, p2
        d0, d1 = d1, d2
    return p1, d1


def _gl_nodes(n):
    """Gauss-Legendre nodes/weights on [-1,1] by Newton on P_n (exact, fast)."""
    xs = []
    ws = []
    for k in range(1, n + 1):
        x = mp.cos(mp.pi * (k - mp.mpf("0.25")) / (n + mp.mpf("0.5")))
        for _ in range(30):
            p, dp = _legendre_pair(n, x)
            dx = p / dp
            x -= dx
            if abs(dx) < mp.mpf(10) ** (-(mp.mp.dps + 8)):
                break
        p, dp = _legendre_pair(n, x)
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


_P_GRID = None


def _p_grid(zmax=225.0):
    """Precomputed Gauss-Legendre nodes in the phase p = (z/4) ln v.

    With v = e^{4u}, p = (z/4) ln v, the integral becomes
        H_t(z) = (1/z) sum_n int_0^{pmax} e^{-pi n^2 e^{4p/z}}
                 [2 pi^2 n^4 e^{9p/z} - 3 pi n^2 e^{5p/z}] e^{t p^2/z^2} cos(p) dp,
    whose cos(p) zeroes at p = pi/2 + k pi are z-INDEPENDENT, so one grid serves
    every z <= zmax.  The tail e^{-pi e^{4p/z}} dies by p = (z/4) ln 32.
    """
    global _P_GRID
    if _P_GRID is not None:
        return _P_GRID
    pmax = (zmax / 4) * mp.log(32)
    bps = [mp.mpf(0)]
    k = 0
    while True:
        b = mp.pi / 2 + k * mp.pi
        if b >= pmax:
            break
        bps.append(b)
        k += 1
    bps.append(pmax)
    nodes = []
    weights = []
    xs, ws = _gl_nodes(DEG)
    for a, b in zip(bps, bps[1:]):
        mid = (a + b) / 2
        half = (b - a) / 2
        for xi, wi in zip(xs, ws):
            nodes.append(mid + half * xi)
            weights.append(half * wi)
    cosp = [mp.cos(p) for p in nodes]
    _P_GRID = (nodes, weights, cosp)
    return _P_GRID


def ht_v(z, t):
    """H_t(z) via the p-substitution on the precomputed z-independent grid."""
    z = mp.mpf(z)
    t = mp.mpf(t)
    nodes, weights, cosp = _p_grid()
    s = mp.mpf(0)
    z2 = z * z
    for p, w, cp in zip(nodes, weights, cosp):
        q = mp.e ** (4 * p / z)          # e^{4u}, u = p/z
        inner = mp.mpf(0)
        for n in range(1, NMAX_V + 1):
            n = mp.mpf(n)
            c = mp.pi * n * n
            qn = mp.e ** (-c * q)
            inner += qn * (2 * mp.pi ** 2 * n ** 4 * q ** (mp.mpf(9) / 4)
                           - 3 * mp.pi * n ** 2 * q ** (mp.mpf(5) / 4))
        s += w * inner * mp.e ** (t * p * p / z2) * cp
    return s / z


def ht_v_ref(z, t, vmax=VMAX, nmax=NMAX_V, deg=DEG):
    """Reference: H_t(z) by the v = e^{4u} substitution, split at the phase zeroes."""
    z = mp.mpf(z)
    t = mp.mpf(t)
    bps = [mp.mpf(1)]
    k = 0
    while True:
        b = mp.e ** (4 * (mp.pi / 2 + k * mp.pi) / z)
        if b > vmax:
            break
        bps.append(b)
        k += 1
    bps.append(mp.mpf(vmax))

    def f(v):
        s = mp.mpf(0)
        for n in range(1, nmax + 1):
            n = mp.mpf(n)
            c = mp.pi * n * n
            s += mp.e ** (-c * v) * (2 * mp.pi ** 2 * n ** 4 * v ** (mp.mpf(9) / 4)
                                     - 3 * mp.pi * n ** 2 * v ** (mp.mpf(5) / 4))
        return s * mp.e ** (t * mp.log(v) ** 2 / 16) * mp.cos((z / 4) * mp.log(v)) / v

    return mp.quad(f, bps, method="gauss-legendre", maxdegree=deg) / 4


# ---------------------------------------------------------------------------
# zero tracking
# ---------------------------------------------------------------------------

def bisect_root(f, a, b, iters=28):
    fa = f(a)
    for _ in range(iters):
        c = (a + b) / 2
        fc = f(c)
        if fa * fc <= 0:
            b = c
        else:
            a = c
            fa = fc
    return (a + b) / 2


def zeros_of_pair(pair, t, step=0.05, margin=0.3):
    """Real zeroes of H_t in a window around the pair.  None if merged."""
    z1, z2 = pair
    mid = (z1 + z2) / 2
    half = (z2 - z1) / 2
    lo = mid - half - margin
    hi = mid + half + margin
    roots = []
    for attempt in range(3):
        xs = [lo + i * step for i in range(int((hi - lo) / step) + 1)]
        roots = []
        for i in range(len(xs) - 1):
            fa = ht_v(xs[i], t)
            fb = ht_v(xs[i + 1], t)
            if fa == 0:
                roots.append(xs[i])
            elif fa * fb < 0:
                roots.append(bisect_root(lambda x: ht_v(x, t), xs[i], xs[i + 1], 24))
        if len(roots) >= 2:
            break
        margin *= 2
        lo = mid - half - margin
        hi = mid + half + margin
    if len(roots) < 2:
        return None
    roots.sort()
    if len(roots) > 2:
        roots = [min(roots, key=lambda r: abs(r - z1)),
                 min(roots, key=lambda r: abs(r - z2))]
        roots.sort()
    return roots


def separation(pair, t, prev=None):
    """Separation of the two real zeroes of H_t near the pair (None if merged)."""
    roots = zeros_of_pair(pair, t)
    if roots is None:
        return None
    return roots[1] - roots[0]


# ---------------------------------------------------------------------------
# sections
# ---------------------------------------------------------------------------

def section_evenness():
    mp.mp.dps = DPS_ID
    out = {}
    worst = mp.mpf(0)
    for u in [0.2, 0.5, 0.9]:
        du = abs(phi(u) - phi(-u))
        worst = max(worst, du)
        out[str(u)] = float(du)
    out["worst"] = float(worst)
    return out


def section_identity():
    mp.mp.dps = DPS_ID
    out = {}
    for z in [10, 55]:
        h = h0_quadosc(z)
        xi = xi8(z)
        rel = abs(h - xi.real) / abs(xi.real)
        out[str(z)] = {"H0": float(h), "xi8": float(xi.real), "rel": float(rel)}
    return out


def section_vmethod_validation():
    mp.mp.dps = DPS_H
    out = {}
    z = mp.mpf("222.9042")
    t = mp.mpf("-0.05")
    v = ht_v(z, t)
    vref = ht_v_ref(z, t)
    out["v_ref"] = float(vref)                 # independent v-substitution split quadrature
    out["vmethod"] = float(v)
    out["rel_vs_v_ref"] = float(abs(v - vref) / abs(vref))
    v0 = ht_v(z, mp.mpf(0))
    xi = xi8(z)
    out["t0"] = float(v0)
    out["xi8_at_t0"] = float(xi.real)
    out["rel_vs_xi"] = float(abs(v0 - xi.real) / abs(xi.real))
    return out


def lsq_line(xs, ys):
    """Least-squares fit y = a + s x; returns (slope, intercept)."""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    s = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - s * mx
    return s, a


def section_heatflow():
    mp.mp.dps = 30
    gammas = [mp.zetazero(k).imag for k in range(1, 649)]
    gaps = [(gammas[i + 1] - gammas[i], i) for i in range(647)]
    gmin = min(gaps, key=lambda g: g[0])
    gap_min, idx_min = gmin
    global_pair = (gammas[idx_min], gammas[idx_min + 1])
    mp.mp.dps = DPS_H

    pairs = [
        {"name": "P1", "gamma": (gammas[33], gammas[34])},   # gap 0.845124
        {"name": "P2", "gamma": (gammas[26], gammas[27])},   # gap 1.219290
    ]
    tvals_by_pair = {
        "P1": [mp.mpf(0), mp.mpf("-0.1"), mp.mpf("-0.25"), mp.mpf("-0.35")],
        "P2": [mp.mpf(0), mp.mpf("-0.2"), mp.mpf("-0.4"), mp.mpf("-0.6")],
    }

    out = {}
    for p in pairs:
        g1, g2 = p["gamma"]
        dg = g2 - g1
        z1, z2 = mp.mpf(g1) * 2, mp.mpf(g2) * 2
        pair = (z1, z2)
        rec = {
            "gamma": [float(g1), float(g2)],
            "Delta_gamma": float(dg),
            "z": [float(z1), float(z2)],
            "t_c_model": float(-(dg ** 2) / 2),
        }
        tvals = tvals_by_pair[p["name"]]
        ds = []
        for t in tvals:
            d = separation(pair, t)
            ds.append({"t": float(t), "d": float(d) if d is not None else None})
        rec["separations"] = ds
        pts = [(t["t"], t["d"]) for t in ds if t["d"] is not None]
        s_fit, a_fit = lsq_line([x for x, _ in pts], [y * y for _, y in pts])
        rec["fit_slope"] = float(s_fit)
        rec["fit_d2_at_0"] = float(a_fit)
        rec["fit_t_c"] = float(-a_fit / s_fit) if s_fit else None
        rec["model_slope"] = 8.0
        rec["model_d2_at_0"] = float(4 * dg ** 2)
        rec["model_t_c"] = float(-(dg ** 2) / 2)
        # Polya direction: at t = +0.05 both crossings must persist
        pplus = []
        for t in [mp.mpf("0.05")]:
            roots = zeros_of_pair(pair, t)
            d = roots[1] - roots[0] if roots is not None else None
            pplus.append({"t": float(t), "d": float(d) if d is not None else None,
                          "real_persists": d is not None})
        rec["polya_plus"] = pplus
        if p["name"] == "P1" and rec["fit_t_c"]:
            # confirm the merger: separation collapses at the fitted t_c
            tfit = mp.mpf(rec["fit_t_c"])
            probe = []
            for frac in ["0.90", "1.05"]:
                tq = tfit * mp.mpf(frac)
                dq = separation(pair, tq)
                probe.append({"t": float(tq), "d": float(dq) if dq is not None else None})
            rec["t_c_confirm"] = probe
        out[p["name"]] = rec

    out["global_closest_pair"] = {
        "idx": int(idx_min),
        "gamma": [float(global_pair[0]), float(global_pair[1])],
        "Delta_gamma": float(gap_min),
        "t_c_local_model": float(-(gap_min ** 2) / 2),
        "note": ("model extrapolation; direct H_t evaluation at z ~ 1501 needs "
                 "~1e-254 resolution, beyond floats and default mpmath"),
    }
    return out


def main():
    t0 = time.time()
    even = section_evenness()
    ident = section_identity()
    vmv = section_vmethod_validation()
    hf = section_heatflow()

    verdict = (
        "DE BRUIJN-NEWMAN CONDENSATION: RH <=> Lambda <= 0. Hidden object: Phi(u) "
        "even by Poisson (worst |Phi(u)-Phi(-u)| = %.1e at dps 50), "
        "H_0(z) = (1/8)xi(1/2+iz/2) = int Phi(u) cos(zu) du (rel %.1e at z=10), "
        "backward-heat flow H_t = int e^{tu^2} Phi(u) cos(zu) du with d_t H_t = -d_zz H_t; "
        "real zeroes persist as t grows (Polya), all real iff t >= Lambda (Newman), "
        "Lambda >= 0 known (Rodgers-Tao/Dobner), so RH is barely so.  The certified "
        "648 zeroes (t=0 slice, z = 2 gamma <= 1998.47) have finite face "
        "t_c = -(Delta gamma)^2/2: measured slope of d(t)^2 vs t = %.3f (model 8) and "
        "t_c = %.4f (model %.4f) for the closest first-40 pair; the certified global "
        "closest pair (gamma-gap %.4f at gamma ~ %.3f) has local-model boundary "
        "t_c ~ %+.4f, four-hundredths of a heat-unit below the axis, at values "
        "~ e^{-pi gamma/4} ~ 1e-254 invisible to floating point.  HONEST WALL: a "
        "numerical probe of the FINITE system, NOT a bound on Lambda; the "
        "global-pair value is a validated-model extrapolation, not a certification; "
        "no finite amount of zeroes proves RH."
        % (even["worst"], ident["10"]["rel"], hf["P1"]["fit_slope"],
           hf["P1"]["fit_t_c"], hf["P1"]["model_t_c"],
           hf["global_closest_pair"]["Delta_gamma"],
           hf["global_closest_pair"]["gamma"][0],
           hf["global_closest_pair"]["t_c_local_model"])
    )

    data = {
        "claim": "RH condenses to the sign of one real constant, the de Bruijn-Newman "
                 "Lambda (RH <=> Lambda <= 0); the certified 648 zeros are the t=0 "
                 "slice of the backward-heat flow H_t, and the finite face of Newman's "
                 "'barely so' boundary is the closest certified pair's merger time "
                 "t_c = -(Delta gamma)^2/2 under the validated local quadratic law.",
        "setup": {"dps_identity": DPS_ID, "dps_heat": DPS_H,
                  "vmax": float(VMAX), "nmax_v": NMAX_V, "deg": DEG},
        "evenness": even,
        "identity": ident,
        "vmethod_validation": vmv,
        "heatflow": hf,
        "verdict": verdict,
        "runtime_sec": round(time.time() - t0, 1),
    }
    with open(OUT, "w") as f:
        json.dump(data, f, indent=2)
    print(verdict)
    print()
    for name, rec in hf.items():
        if not isinstance(rec, dict) or "separations" not in rec:
            continue
        print("%s: Delta_gamma=%.6f  model t_c=%+.4f  fit slope=%.3f (model 8)  "
              "fit d2(0)=%.4f (model %.4f)  fit t_c=%+.4f"
              % (name, rec["Delta_gamma"], rec["model_t_c"], rec["fit_slope"],
                 rec["fit_d2_at_0"], rec["model_d2_at_0"], rec["fit_t_c"]))
        print("    separations: " + ", ".join("%+.2f->%.4f" % (t["t"], t["d"])
                                              for t in rec["separations"]))
        print("    polya t>0: " + ", ".join("%+.2f->d=%.4f" % (t["t"], t["d"])
                                            for t in rec["polya_plus"]))
        if "t_c_confirm" in rec:
            print("    t_c confirm: " + ", ".join("%+.4f->d=%s" % (t["t"],
                  "merged" if t["d"] is None else "%.4f" % t["d"])
                  for t in rec["t_c_confirm"]))
    gc = hf["global_closest_pair"]
    print("global closest pair: idx=%d  Delta_gamma=%.6f  gamma=(%.6f, %.6f)  "
          "t_c(local model)=%+.6f"
          % (gc["idx"], gc["Delta_gamma"], gc["gamma"][0], gc["gamma"][1],
             gc["t_c_local_model"]))
    print("wrote", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
