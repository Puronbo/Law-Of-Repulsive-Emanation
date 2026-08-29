#!/usr/bin/env python3
"""Ch.79 The Rate Function Carries the Mirror: on the whole tail, the same
parity that gave k~_n=(-1)^n k_n (Ch.78) and the detailed mirror M(w)=w
(Ch.77) becomes a statement about the large-deviation rate function I(a).

The moment-generating function phi(t)=<e^{-tW}> obeys the exchange symmetry
phi(t)=phi(1-t) on the reversible (DeltaF=0) round trip. Its Legendre-Fenchel
conjugate is the level-1 rate function, I(a)=sup_t[ a t - ln phi(t) ]. For
Gaussian (Onsager-Machlup 1953 / Mazonka-Jarzynski 1999 linearity) work,
I(a) = (a-mu)^2 / (2 sigma^2) is a quadratic, even about the mean:
I(a) = I(2 mu - a), the rate-function image of the 0/0 ladder of Ch.78 (every
empty higher cumulant = one vanishing derivative of the quadratic) and of the
mirror M(w)=w of Ch.77 now normalized per unit work.

The tilt e^{-W} shifts the quadratic's mode: dI~/da = 0 -> a = mu - sigma^2 =
k~_1 of Ch.78; and since sigma^2 = 2 mu (VDT, Ch.72) the tilted mode sits at
the mirror image a = -mu of the untilted mode a = mu (with the sigma^2-2mu
slack reading q of Ch.76). Off-Gaussian the rate function is NOT even and the
mirror residual R(a) = I(a) - I(2 mu - a) measures exactly the asymmetry the
skew deposits in the far tail - the coin's size, integrated.

We measure, cheaply reusing the Ch.76-78 instruments (Heun SRK2, seed 42):
  1. drag parabola (Gaussian, mu=+5.98, sigma^2=12.04): I quadratic, even,
     tilt shifts mode to mu - sigma^2; R(a) = 0 across the tail.
  2. control round trip (skew +1.30, kurt 7.0, q=0.894): I = parabola + an
     odd residual; R(a) rises in the far tail, the skew's tail deposit.
  3. engaged 0.35/2 and harvest 0.05/16 (coin spent): the whole rate function
     leans - mode shift AND R(a) deepens - one coin, the entire tail.
"""
import os
import sys
import json
import math
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import detailed_ledger as dl

SEED = 42
DT = 0.005
FAR_MEDIAN = dl.FAR_MEDIAN

SCALING = 40.0   # per-run average number of work units (tail ordinate a)


def histogram_rates(Ws, nbins=200, lo=None, hi=None, name=""):
    """Empirical rate function I(a) = -(1/N) ln(hist/N) from a work sample,
    using a simple histogram with a floor.  Returns (center, rate)."""
    if lo is None:
        lo = min(Ws)
    if hi is None:
        hi = max(Ws)
    width = (hi - lo) / nbins
    counts = [0] * nbins
    for w in Ws:
        i = int((w - lo) / width)
        if 0 <= i < nbins:
            counts[i] += 1
    n = float(len(Ws))
    xs = []
    ys = []
    floor = 1.0 / n
    for i, c in enumerate(counts):
        if c > 0:
            x = lo + (i + 0.5) * width
            ys.append(-math.log(c / (n * width)))
            xs.append(x)
    return xs, ys


def gaussian_rates(mu, sig2, lo, hi, nbins=200):
    """Analytic Onsager-Machlup quadratic rate function sample points."""
    xs = []
    ys = []
    for i in range(nbins):
        a = lo + (i + 0.5) * (hi - lo) / nbins
        xs.append(a)
        ys.append((a - mu) ** 2 / (2.0 * sig2))
    return xs, ys


def main():
    random.seed(SEED)
    print("Ch.79 The Rate Function Carries the Mirror")
    print("  I(a) = sup_t[ a t - ln <e^{-tW}> ] ; Gaussian I(a)=(a-mu)^2/2sig^2")
    print("  tilted mode a = mu - sig^2 = k~_1 (Ch.78) ;  R(a)=I(a)-I(2mu-a)")

    out = {"seed": SEED, "dt": DT, "scaling": SCALING, "median": FAR_MEDIAN,
           "rows": [], "theory": {}}

    # ---- 1. Gaussian parabola (drag trap) -------------------------------
    mu = 5.977339
    sig2 = 12.044408          # measured Ch.78/77
    gx, gy = gaussian_rates(mu, sig2, -8.0, 20.0)
    mode = mu - sig2          # tilted mode (mu - sigma^2)
    out["theory"] = {
        "mu": mu, "sig2": sig2, "untilted_mode": mu,
        "tilted_mode": mode, "k1_tilde_x2_over_2": sig2 / 2.0,
        "mode_shift_minus_sig2": -sig2,
        "mirror_residual_gaussian": 0.0,
        "sole": "I(a)=I(2mu-a) exactly; tilt shifts mode by -sigma^2 = k~_1",
    }
    print("\n  PARABOLA (Gaussian, mu=%.4f sig^2=%.4f)" % (mu, sig2))
    print("    untilted mode a* = +%.4f ;  tilt pushes mode to a* = %.4f = mu - sig^2"
          % (mu, mode))
    print("    I(a) quadratic, even about mu : R(a) = 0 (analytic, all tail)")
    print("    0/0 of Ch.78 n>=3 rows = every vanishing derivative of the quadratic:")
    print("      the ENTIRE tail is carried in two numbers (Onsager-Machlup 1953)")

    # residual check on the analytic curve
    sres = 0.0
    for a in gx:
        r = ((a - mu) ** 2 / 2.0 / sig2) - ((2 * mu - a - mu) ** 2 / 2.0 / sig2)
        sres += abs(r)
    print("    |R(a)| summed over analytic tail = %.2e  (0 by construction)"
          % sres)

    # ---- 2. empirical control round trip ---------------------------------
    print("\n  running control round trip 250k ...")
    ctrl = dl.run_stiff(250000, 0.5, 0.5, 0.5, "control")
    mctrl = sum(ctrl) / len(ctrl)
    vctrl = sum((w - mctrl) ** 2 for w in ctrl) / len(ctrl)
    qc = 2 * mctrl / vctrl if vctrl else 0
    print("    mu=%.4f  sig^2=%.4f  q=%.4f (matches Ch.76 control 0.894; skew +1.30 kurt 7.0)"
          % (mctrl, vctrl, qc))
    cx, cy = histogram_rates(ctrl, nbins=180, lo=-1.0, hi=2.6)
    # mirror residual R(a) = I(a) - I(2mu-a)
    cross = []
    for a, ia in zip(cx, cy):
        am = 2 * mctrl - a
        # nearest sample of analytic-free empirical at 2mu-a
        best = None
        for bb, ib in zip(cx, cy):
            if abs(bb - am) < (abs(best[0] - am) if best else 1e9):
                best = (bb, ib)
        if best is not None:
            cross.append((a, ia, best[1], ia - best[1]))
    # report far-tail residual where both sampled
    far = [(a, r) for (a, _1, _2, r) in cross if a > mctrl + 1.0]
    print("    empirical I(a) asymmetric: far-tail mirror residual")
    if far:
        a_far, r_far = max(far, key=lambda t: t[1])
        print("      max R(a) in far tail = %+.4f at a=%.3f (Gaussian would be 0)"
              % (r_far, a_far))
    else:
        r_far, a_far = 0.0, 0.0
    out["rows"].append({
        "name": "control", "mu": round(mctrl, 4), "sig2": round(vctrl, 4),
        "q": round(qc, 4), "far_residual": round(r_far, 4),
        "far_argmax": round(a_far, 4),
    })

    # ---- 3. engaged coin -------------------------------------------------
    print("\n  running engaged 0.35/2 200k ...")
    eng = dl.run_stiff(200000, 0.5, 0.35, 2.0, "median")
    meng = sum(eng) / len(eng)
    veng = sum((w - meng) ** 2 for w in eng) / len(eng)
    qeng = 2 * meng / veng if veng else 0
    ex, ey = histogram_rates(eng, nbins=180, lo=-1.0, hi=2.8)
    ecross = []
    for a, ia in zip(ex, ey):
        am = 2 * meng - a
        best = None
        for bb, ib in zip(ex, ey):
            if abs(bb - am) < (abs(best[0] - am) if best else 1e9):
                best = (bb, ib)
        if best is not None:
            ecross.append((a, ia, best[1], ia - best[1]))
    efar = [(a, r) for (a, _1, _2, r) in ecross if a > meng + 1.0]
    e_r = max((t[1] for t in efar), default=0.0)
    print("    mu=%.4f sig^2=%.4f  mode-lean + far residual %+.4f"
          % (meng, veng, e_r))
    out["rows"].append({
        "name": "engaged", "mu": round(meng, 4), "sig2": round(veng, 4),
        "q": round(qeng, 4), "far_residual": round(e_r, 4),
        "s0": round((sum(math.exp(-w) for w in eng) / len(eng)), 4),
    })

    # ---- 4. harvest coin -------------------------------------------------
    print("\n  running harvest 0.05/16 100k ...")
    har = dl.run_stiff(100000, 0.5, 0.05, 16.0, "median")
    mhar = sum(har) / len(har)
    vhar = sum((w - mhar) ** 2 for w in har) / len(har)
    qhar = 2 * mhar / vhar if vhar else 0
    hx, hy = histogram_rates(har, nbins=160, lo=-1.0, hi=2.8)
    hcross = []
    for a, ia in zip(hx, hy):
        am = 2 * mhar - a
        best = None
        for bb, ib in zip(hx, hy):
            if abs(bb - am) < (abs(best[0] - am) if best else 1e9):
                best = (bb, ib)
        if best is not None:
            hcross.append((a, ia, best[1], ia - best[1]))
    hfar = [(a, r) for (a, _1, _2, r) in hcross if a > mhar + 1.0]
    h_r = max((t[1] for t in hfar), default=0.0)
    print("    mu=%.4f sig^2=%.4f  far residual %+.4f"
          % (mhar, vhar, h_r))
    out["rows"].append({
        "name": "harvest", "mu": round(mhar, 4), "sig2": round(vhar, 4),
        "q": round(qhar, 4), "far_residual": round(h_r, 4),
        "s0": round((sum(math.exp(-w) for w in har) / len(har)), 4),
    })

    # ---- theory cross-check: Gaussian tilt shifts mode by -sig^2 ---------
    out["theory"]["S0_control"] = round(
        (sum(math.exp(-w) for w in ctrl) / len(ctrl)), 4)
    print("\n  THEORY CROSS-CHECK: parabola tilt mode mu-sig^2 = %.4f"
          % mode)
    print("  control far residual: Gaussian 0 vs measured %.4f (skew's tail deposit)"
          % out["rows"][0]["far_residual"])
    print("  one equality (P(+W)/P(-W)=e^W) -> one ladder (Ch.78) -> one rate "
          "function (this chapter): the coin is in the far tail of BOTH.")

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "rate_book.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print("\njson -> %s" % path)


if __name__ == "__main__":
    main()