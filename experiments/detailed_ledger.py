import math, random, json, os

# ============================================================
# Ch.77  The Mirror at W = 0
# Detailed fluctuation theorem (Crooks 1999; Jarzynski 1997) on
# the SAME two instruments as Ch.76: for a time-reversible cyclic
# protocol, DeltaF = 0,
#    P(+W) / P(-W) = e^{W}            (the detailed ledger)
# so the "mirror graph" M(w) = ln P(w) - ln P(-w) is the STRAIGHT
# LINE M(w) = w through the origin. The ratio at w = 0 is a 0/0
# whose removable value is 1 = the slope / the TUR-tight value of
# Ch.76. The detailed ledger is rigid (FT is a theorem); the slack
# of Ch.76 lives in the SHAPE of P away from the mirror (skew of
# the stiffness instrument). We verify: (resid) the mirror slope is
# 1 within sampling + O(dt) integration error on every row; (fill)
# the central 0/0 estimator tends to 1 as the window shrinks; (fid)
# FT-identity <W e^{-W}> = -<W>; (wing) the ratio survives where the
# integral ledger of Ch.71 cannot reach; and on the Gaussian
# instrument q -> 1 (Ch.76) because there the mirror + Gaussianity
# pin Var = 2 <W>. Two ledgers, one book: the mirror balances
# exactly, the variance books the fee.
# ============================================================

random.seed(42)

DT = 0.01
BIN_H = 0.0125
LO = -20.0
NB = 4000  # covers [-20, +30); parabola w~+6, sigma~3.5 needs the +30 ceiling
FAR_MEDIAN = 0.5682  # calibrated median |x_mid| (matches Ch.74/75/76)

def histogram_run(Ws, h=BIN_H, nb=NB):
    counts = [0] * nb
    for w in Ws:
        i = int(math.floor((w - LO) / h))
        if 0 <= i < nb:
            counts[i] += 1
    return counts

def analyze_row(name, Ws):
    n = float(len(Ws))
    m1 = m2 = m3 = m4 = 0.0
    se = sj = sw = 0.0
    for w in Ws:
        m1 += w; m2 += w * w; m3 += w ** 3; m4 += w ** 4
        se += math.exp(-w)
        sj += w * math.exp(-w)
        sw += w * math.exp(-0.5 * w)
    mu = m1 / n
    var = m2 / n - mu * mu
    sig = math.sqrt(var)
    mu3 = m3 / n - 3.0 * mu * (m2 / n) + 2.0 * mu ** 3
    mu4 = m4 / n - 4.0 * mu * (m3 / n) + 6.0 * mu * mu * (m2 / n) - 3.0 * mu ** 4
    skew = mu3 / (sig ** 3)
    kurt = mu4 / (var * var) - 3.0
    q = 2.0 * mu / var if mu > 0 else 0.0
    jin = se / n
    fid = (-sj / n) / mu if mu != 0 else 0.0
    tmean = sw / se  # tilted mean under e^{-W/2}; plain FT => 0
    c = histogram_run(Ws)
    i0 = int(-LO / BIN_H)  # bin whose lower edge is w = 0

    def mirror_window(w_lo, w_hi, floor):
        # pair of bin i (w in [(i-i0)h, (i-i0+1)h)) is bin 2*i0-i-1 (the bin
        # holding w in [-(i-i0+1)h, -(i-i0)h)): w=0 is a bin EDGE
        xs, ys = [], []
        start = i0 + int(math.ceil(w_lo / BIN_H))
        stop = i0 + int(math.floor(w_hi / BIN_H)) + 1
        for i in range(start, min(stop, len(c))):
            b = c[i]
            if b < floor:
                break
            j = 2 * i0 - i - 1
            if j < 0 or c[j] < floor:
                continue
            x = (i - i0 + 0.5) * BIN_H
            y = math.log(float(b) / c[j])
            xs.append(x); ys.append(y)
        num = den = 0.0
        for x, y in zip(xs, ys):
            num += x * y; den += x * x
        slope = num / den if den > 0 else 0.0
        resid = 0.0
        for x, y in zip(xs, ys):
            resid += (y - slope * x) ** 2
        se_slope = math.sqrt(resid / (max(1, len(xs) - 1) * den)) if den > 0 else 0.0
        medev = sum(abs(y - x) for x, y in zip(xs, ys)) / float(max(1, len(xs)))
        wing = (xs[-1], ys[-1]) if xs else None
        return slope, se_slope, medev, len(xs), wing

    core = mirror_window(0.15, 0.8, 500)
    far_only = mirror_window(0.8, 20.0, 80)
    slope, se_slope = core[0], core[1]
    # central 0/0 fill: k+1 bins on the + side vs their mirror on the - side
    fills = []
    for k in (0, 1, 2):
        cpos = sum(c[i0:i0 + k + 1])
        cneg = sum(c[i0 - k - 1:i0])
        if cpos > 0 and cneg > 0:
            d = (k + 0.5) * BIN_H
            fills.append(round(math.log(float(cpos) / cneg) / d, 4))
    return dict(name=name, n=n, mu=mu, var=var, skew=skew, kurt=kurt, q=q,
                jin=jin, fid=fid, tmean=tmean, slope=slope, slope_se=se_slope,
                medev=core[2], nlox=core[3], wing=core[4], far=far_only, fills=fills)

def run_drag(runs, tau):
    """Dragged Gaussian trap V=k(x-lam)^2/2, k=2, lam 0->2->0; return W list."""
    leg = tau / 2.0
    steps = max(1, int(round(leg / DT)))
    dt = leg / steps
    sig = math.sqrt(2.0 * dt)
    k = 2.0
    out = [0.0] * runs
    dla = 2.0 / steps
    for r in range(runs):
        x = random.gauss(0.0, 1.0 / math.sqrt(2.0))
        w = 0.0
        for _l in (0, 1):
            lam0 = 0.0 if _l == 0 else 2.0
            for s in range(steps):
                lam_mid = lam0 + dla * (s + 0.5)
                z = random.gauss(0.0, 1.0)
                xp = x - k * (x - lam_mid) * dt + sig * z
                x = x + 0.5 * (-k * (x - lam_mid) - k * (xp - lam_mid)) * dt + sig * z
                w += k * (lam_mid - x) * dla
        out[r] = w
    return out

def leg1(x, tau):
    """Ramp lambda 1->2 over tau; return final position and accumulated W."""
    steps = max(1, int(round(tau / DT)))
    dt = tau / steps
    sig = math.sqrt(2.0 * dt)
    xo = x
    w = 0.0
    for s in range(steps):
        la = 1.0 + 1.0 * (s + 0.5) / steps
        z = random.gauss(0.0, 1.0)
        k1 = -la * xo
        xp = xo + k1 * dt + sig * z
        k2 = -la * xp
        x = xo + 0.5 * (k1 + k2) * dt + sig * z
        w += 0.5 * (xo * xo + x * x) * (1.0 / steps) * 0.5
        xo = x
    return x, w

def leg2(x, tau, w_in):
    """Ramp lambda 2->1 over tau; return final W total."""
    steps = max(1, int(round(tau / DT)))
    dt = tau / steps
    sig = math.sqrt(2.0 * dt)
    xo = x
    w = w_in
    for s in range(steps):
        la = 2.0 - 1.0 * (s + 0.5) / steps
        z = random.gauss(0.0, 1.0)
        k1 = -la * xo
        xp = xo + k1 * dt + sig * z
        k2 = -la * xp
        x = xo + 0.5 * (k1 + k2) * dt + sig * z
        w += 0.5 * (xo * xo + x * x) * (-1.0 / steps) * 0.5
        xo = x
    return w

def run_stiff(runs, tau1, tau2fast, tau2slow, mode):
    out = [0.0] * runs
    for r in range(runs):
        xo = random.gauss(0.0, 1.0)
        x_mid, w1 = leg1(xo, tau1)
        if mode == "control":
            is_fast = True
        elif mode == "sign":
            is_fast = x_mid > 0
        else:
            is_fast = abs(x_mid) > FAR_MEDIAN
        tau2 = tau2fast if is_fast else tau2slow
        out[r] = leg2(x_mid, tau2, w1)
    return out

def cal_median():
    runs = 100000
    vals = []
    for _ in range(runs):
        xo = random.gauss(0.0, 1.0)
        x_mid, _w = leg1(xo, 0.5)
        vals.append(abs(x_mid))
    vals.sort()
    return vals[runs // 2]

if __name__ == "__main__":
    print("Ch.77 The Mirror at W = 0: the Detailed Fluctuation Theorem on the Same Two Instruments")
    print("  FT (Crooks 1999): P(+W)/P(-W) = e^W on a time-reversible DeltaF = 0 cycle")
    print("  mirror M(w) = ln P(w) - ln P(-w) = w: slope 1, straight, through the origin")
    print("  0/0 at w = 0 with removable value 1 ; the slack of Ch.76 lives off the mirror")
    print("")
    print("calibrating far/near median...")
    m = cal_median()
    print("  median |x_mid| = %.4f\n" % m)

    rows = [
        ("PARABOLA  tau=2      ", run_drag(250000, 2.0)),
        ("ctrl stiff 0.5       ", run_stiff(250000, 0.5, 0.5, 0.5, "control")),
        ("engaged 0.35/2       ", run_stiff(200000, 0.5, 0.35, 2.0, "far")),
        ("HARVEST 0.05/16      ", run_stiff(100000, 0.5, 0.05, 16.0, "far")),
    ]

    results = []
    print("  %-20s %8s %9s %7s %7s %7s %10s %8s | %s" %
          ("row", "<W>", "Var", "skew", "kurt", "q", "mirror-s", "SE", "wing M-w"))
    for (name, Ws) in rows:
        R = analyze_row(name.split()[0].lower().replace("/", "_"), Ws)
        results.append(R)
        wing = ""
        if R["wing"]:
            wing = "%+.4f" % (R["wing"][1] - R["wing"][0])
        print("  %-20s %+8.4f %9.4f %7.3f %7.2f %7.4f %10.4f %8.4f | %s"
              % (name, R["mu"], R["var"], R["skew"], R["kurt"], R["q"],
                 R["slope"], R["slope_se"], wing))
    print("")
    print("  checks: <e^(-W)>, f-identity <We^(-W)>/-<W>, tilted mean, core-bin count, medev, central fills (->1 if FT-exact):")
    for R in results:
        far = "far-slope %.3f (%d)" % (R["far"][0], R["far"][3]) if R["far"][3] else "far n/a"
        print("  %-20s jin=%.4f  fid=%.4f  tilt=%+.4f  bins=%d  medev=%.4f  fills=%s  %s"
              % (R["name"], R["jin"], R["fid"], R["tmean"], R["nlox"], R["medev"],
                 R["fills"], far))
    data = {
        "chapter": 77,
        "title": "The Mirror at W = 0: the Detailed Fluctuation Theorem on the Same Two Instruments (Crooks 1999, Mazonka-Jarzynski 1999)",
        "notes": "Crooks FT: P(+W)/P(-W) = e^W for time-reversible DeltaF=0 cycles; the mirror M(w)=ln P(w)-ln P(-w)=w is a straight line slope 1 through origin; ratio at w=0 is 0/0 with removable value 1; TUR slack of Ch.76 lives off the mirror in the shape of P.",
        "rows": [
            {"name": r["name"], "mean_work": r["mu"], "var": r["var"], "skew": r["skew"],
             "kurt": r["kurt"], "q": r["q"], "mirror_slope": r["slope"],
             "mirror_slope_se": r["slope_se"], "mirror_max_dev": r["medev"],
             "n_mirror_bins": r["nlox"], "jarzynski_check": r["jin"],
             "ft_identity_ratio": r["fid"], "tilted_mean": r["tmean"],
             "central_fills": r["fills"],
             "far_slope": r["far"][0] if r["far"][3] else None,
             "n_far_bins": r["far"][3]}
            for r in results
        ],
        "threshold_median_abs_xmid": m,
        "removable_value": 1.0,
    }
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "detailed_ledger.json")
    with open(out, "w") as fh:
        json.dump(data, fh, indent=2)
    print("")
    print("json ->", out)