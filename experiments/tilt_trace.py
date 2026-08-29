#!/usr/bin/env python3
"""Ch.80 The Tilt Traces the Curve: the Biased Ensemble as the Estimator of
the Mirror -- the Legendre identity at every t (a direct companion to the
cumulant ladder of Ch.78 and the rate function of Ch.79).

The rate function of Ch.79, I(a) = sup_t[ a t - F(t) ], is a LEGENDRE-FENCHEL
conjugate: the CGF F(t) = ln <e^{-tW}> and I(a) carry the same mirror.  The
way the tilt of Ch.78 is actually USED to measure the tail is the inverse
route: fix a tilt t, reweight by e^{-tW}, measure the tilted mean
    a(t) = <W e^{-tW}> / <e^{-tW}> = -F'(t)
and read the rate function at that point by the Legendre identity
    I(a(t)) = a(t) t - F(t)   (with sign chosen so I >= 0, min 0).

Sweeping t therefore TRACES the whole mirror curve a -> I(a), and:

  1. For Gaussian work, a(t) = mu - sig^2 t is LINEAR in t and
     I(a(t)) = sig^2 t^2 / 2 = the Ch.79 quadratic, exactly.
  2. The tilted VARIANCE V(t) = -F''(t) = <W^2 e^{-tW}>/<e^{-tW}> - a(t)^2
     is CONSTANT = sig^2 for Gaussian -- Ch.78's n=2 invariance, at EVERY
     slice t, not just t=1.  (For the non-Gaussian control it varies, the
     tail deposit arriving one rung at a time.)
  3. The 0/0 in the tail is RESOLVED BY THE TILT: the empty n>=3 cumulants
     of Ch.78 (Gaussian) and the empty higher curvature of I (Ch.79) mean
     a(t) traces a STRAIGHT LINE and I is exactly quadratic -- the tilt
     "trades" a curve for one number (a(t)) that moves linearly.
  4. The zero-mean tilt t* where a(t*) = 0 is a FREEZING PRICE: it is the
     tilt at which the net work vanishes on average.  For the parabola
     t* = mu / sig^2 ~ 0.5 (the mirror's own center W=0, Ch.77);
     for the coin the demon SHIFTS t* -- the price of knowing.

Instruments: same Heun SRK2, seed 42, Ch.76-79 rows.  We reuse the
measured parabola parameters and re-sample the control / engaged / harvest
rows, then at a grid of tilts t in [-2, 3] report a(t), V(t), I(a(t)).
"""
import os
import sys
import json
import math
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import detailed_ledger as dl

SEED = 42
FAR_MEDIAN = dl.FAR_MEDIAN


def tilted_mean(sample, t):
    """<W e^{-tW}> / <e^{-tW}>, the mean work under the e^{-tW} tilt."""
    s0 = 0.0
    s1 = 0.0
    for w in sample:
        ew = math.exp(-t * w)
        s0 += ew
        s1 += w * ew
    return s1 / s0


def swept(sample, tgrid):
    n = float(len(sample))
    res = []
    for t in tgrid:
        s0 = 0.0
        s1 = 0.0
        s2 = 0.0
        for w in sample:
            ew = math.exp(-t * w)
            s0 += ew
            s1 += w * ew
            s2 += w * w * ew
        S0 = s0 / n
        a = s1 / s0                     # tilted mean
        m2 = s2 / s0                    # <W^2> under tilt
        V = m2 - a * a                  # tilted variance
        F = math.log(S0)
        I = a * t - F                   # Legendre identity (sign to I>=0)
        res.append((round(t, 3), round(a, 5), round(V, 5),
                    round(I, 5), round(F, 5)))
    return res


def main():
    random.seed(SEED)
    print("Ch.80 The Tilt Traces the Curve: the Biased Ensemble as the Mirror")
    print("  a(t) = <W e^{-tW}>/<e^{-tW}> = -F'(t) ;  V(t) = -F''(t)")
    print("  I(a(t)) = a(t) t - F(t)  (Legendre identity, Ch.79 dual)")

    out = {"seed": SEED, "median": FAR_MEDIAN, "rows": {}} 

    # ---- 0. analytic Gaussian parabola reference -------------------------
    mu = 5.977339
    sig2 = 12.044408
    tstar = mu / sig2
    print("\n  PARABOLA reference (analytic Gaussian, mu=%.4f sig^2=%.4f)"
          % (mu, sig2))
    print("    a(t) = mu - sig^2 t  (linear) ;  V(t) = sig^2 (constant, Ch.78 n=2)")
    print("    t* (zero mean, a=0) = mu/sig^2 = %.4f ~ 1/2 (the mirror center W=0)"
          % tstar)
    out["rows"]["parabola"] = {
        "mu": mu, "sig2": sig2, "tstar": round(tstar, 4),
        "a_linear": True, "V_constant": True,
        "I_quadratic": True,
        "k1_tilde": round(mu - sig2, 4),  # a(1) = Ch.78 k~_1
    }

    # ---- grid of tilts for the measured rows ------------------------------
    tg = [-2.0, -1.0, 0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
    print("\n   tilt grid: %s" % tg)

    # ---- control round trip (q = 0.90, matches Ch.76/79) ------------------
    print("\n  running control round trip 250k ...")
    ctrl = dl.run_stiff(250000, 0.5, 0.5, 0.5, "control")
    mctrl = sum(ctrl) / len(ctrl)
    vctrl = sum((w - mctrl) ** 2 for w in ctrl) / len(ctrl)
    cres = swept(ctrl, tg)
    print("    mu=%.4f sig^2=%.4f q=%.4f" % (mctrl, vctrl, 2 * mctrl / vctrl))
    print("    t     a(t)       V(t)      I(a(t))    F(t)")
    for (t, a, V, I, F) in cres:
        print("    %+5.2f %+10.4f %9.4f %10.4f %+10.4f" % (t, a, V, I, F))
    out["rows"]["control"] = {
        "mu": round(mctrl, 4), "sig2": round(vctrl, 4),
        "q": round(2 * mctrl / vctrl, 4),
        "sweep": cres,
    }

    # find zero-mean tilt for control by interpolation on a(t) vs t
    a0_c = None
    for i in range(len(cres) - 1):
        t1, a1, _, _, _ = cres[i]
        t2, a2, _, _, _ = cres[i + 1]
        if (a1 > 0) != (a2 > 0):
            a0_c = round(t1 + (0 - a1) * (t2 - t1) / (a2 - a1), 4)
            break
    out["rows"]["control"]["tstar_interp"] = a0_c
    print("    interp t* (a=0) = %s" % (str(a0_c) if a0_c else "outside grid"))

    # ---- engaged 0.35/2 ---------------------------------------------------
    print("\n  running engaged 0.35/2 200k ...")
    eng = dl.run_stiff(200000, 0.5, 0.35, 2.0, "median")
    meng = sum(eng) / len(eng)
    veng = sum((w - meng) ** 2 for w in eng) / len(eng)
    eres = swept(eng, tg)
    print("    mu=%.4f sig^2=%.4f" % (meng, veng))
    print("    t     a(t)       V(t)      I(a(t))    F(t)")
    for (t, a, V, I, F) in eres:
        print("    %+5.2f %+10.4f %9.4f %10.4f %+10.4f" % (t, a, V, I, F))
    out["rows"]["engaged"] = {"mu": round(meng, 4), "sig2": round(veng, 4),
                              "sweep": eres}

    # ---- harvest 0.05/16 --------------------------------------------------
    print("\n  running harvest 0.05/16 100k ...")
    har = dl.run_stiff(100000, 0.5, 0.05, 16.0, "median")
    mhar = sum(har) / len(har)
    vhar = sum((w - mhar) ** 2 for w in har) / len(har)
    hres = swept(har, tg)
    print("    mu=%.4f sig^2=%.4f" % (mhar, vhar))
    for (t, a, V, I, F) in hres:
        print("    %+5.2f %+10.4f %9.4f %10.4f %+10.4f" % (t, a, V, I, F))
    out["rows"]["harvest"] = {"mu": round(mhar, 4), "sig2": round(vhar, 4),
                              "sweep": hres}

    # ---- summary of the pattern -------------------------------------------
    print("\n  PATTERN: the tilt is the coordinate that traces the mirror curve.")
    print("  parabola: a(t) linear (slope -sig^2), V(t) constant -> I exact quadratic")
    print("  control:  V(t) varies with t (the n>=3 deposit arrives one rung at a time)")
    print("  coin:     shifts the zero-mean tilt t* (the price of knowing)")

    # ---- antisymmetry of a(t) about t = 1/2 (the mirror, in tilt space) --
    def antisym(sample, ts, tmir=0.5):
        """Report a(t) + a(1-t) for a grid: == 0 iff a(t) = -a(1-t)."""
        resid = []
        for t in ts:
            m = tmir
            a1 = tilted_mean(sample, t)
            a2 = tilted_mean(sample, 1.0 - t)
            resid.append((round(t, 3), round(a1, 4), round(a2, 4),
                          round(a1 + a2, 4)))
        return resid

    print("\n  ANTISYMMETRY  a(t) + a(1-t)  (exchange F(t)=F(1-t) forces a(1/2)=0)")
    print("    control (q=0.90, reversible -> mirror holds):")
    for (t, a1, a2, s) in antisym(ctrl, [0.0, 0.25, 0.4, 0.5]):
        print("      t=%4.2f  a(t)=%+8.4f a(1-t)=%+8.4f sum=%+7.4f"
              % (t, a1, a2, s))
    print("    engaged (coin -> breaks plain mirror):")
    for (t, a1, a2, s) in antisym(eng, [0.0, 0.25, 0.5]):
        print("      t=%4.2f  a(t)=%+8.4f a(1-t)=%+8.4f sum=%+7.4f"
              % (t, a1, a2, s))
    print("    harvest (strong coin):")
    for (t, a1, a2, s) in antisym(har, [0.0, 0.25, 0.5]):
        print("      t=%4.2f  a(t)=%+8.4f a(1-t)=%+8.4f sum=%+7.4f"
              % (t, a1, a2, s))
    out["antisymmetry"] = {
        "control": [[t, a1, a2, s] for (t, a1, a2, s)
                    in antisym(ctrl, [0.0, 0.25, 0.4, 0.5])],
        "engaged": [[t, a1, a2, s] for (t, a1, a2, s)
                    in antisym(eng, [0.0, 0.25, 0.5])],
        "harvest": [[t, a1, a2, s] for (t, a1, a2, s)
                    in antisym(har, [0.0, 0.25, 0.5])],
    }

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "tilt_trace.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print("\njson -> %s" % path)


if __name__ == "__main__":
    main()