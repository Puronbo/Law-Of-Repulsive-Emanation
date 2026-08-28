import math, random, json, os

# ============================================================
# Ch.76  Precisely Priced
# The thermodynamic uncertainty relation (TUR) sets a 2:1 floor
# on the ledger:  Var(W) >= 2 <W> / beta  for cyclic DeltaF=0
# processes with <W> > 0 (Barato-Seifert 2015; Gingrich et al.
# 2016; time-dependent form Dechant-Sasa 2018). Equivalently
# q = 2 <W>/(beta Var(W)) <= 1 : the "slack" s = 1 - q is the
# handling fee of knowing.
# Instrument A (the parabola): DRAGGED fixed-stiffness trap
# V = k(x-lambda)^2/2, k=2, lambda 0->2->0. Work is a linear
# functional of the Gaussian bath, hence EXACTLY Gaussian
# (Mazonka-Jarzynski 1999); the Gaussian Jarzynski equality
# <e^{-W}>=1 forces mu = sigma^2/2, i.e. Var(W) = 2 <W> EXACTLY:
# q = 1, slack 0, the TUR saturated with zero waste.
# Instrument B (the demon, Ch.74/75): stiffness round trip
# V = lambda x^2/2, 1->2->1, with the fair far/near bit. Any
# protocol mixing (a coin changing the return speed) adds a
# between-group variance and bends the parabola: q < 1. The
# demon pays a handling fee even when its coin works (engaged)
# or is silent (dead coin); when <W><0 the harvest leaves the
# X>0 province of the TUR and the coin's bill of Ch.75 governs.
# ============================================================

random.seed(42)

DT = 0.01
COIN = math.log(2.0)
FAR_THRESHOLD = 0.6

def moments_from(runs, m1, m2, m3, m4):
    mu = m1 / runs
    mu2 = m2 / runs - mu * mu
    if mu2 <= 0:
        return dict(mu=mu, var=0.0, skew=0.0, kurt=0.0, q=0.0)
    mu3 = m3 / runs - 3.0 * mu * (m2 / runs) + 2.0 * mu ** 3
    mu4 = m4 / runs - 4.0 * mu * (m3 / runs) + 6.0 * mu * mu * (m2 / runs) - 3.0 * mu ** 4
    sig = math.sqrt(mu2)
    skew = mu3 / (sig ** 3) if sig > 0 else 0.0
    kurt = mu4 / (mu2 * mu2) - 3.0 if mu2 > 0 else 0.0
    q = 2.0 * mu / mu2 if mu > 0 else 0.0
    return dict(mu=mu, var=mu2, skew=skew, kurt=kurt, q=q)

def run_drag(runs, tau):
    """Dragged trap V = k(x-lambda)^2/2, k=2, lambda 0->2->0, DeltaF=0,
    D = beta = 1. Work exactly Gaussian: Var = 2 <W> (the parabola)."""
    leg = tau / 2.0
    steps = max(1, int(round(leg / DT)))
    dt = leg / steps
    sig = math.sqrt(2.0 * dt)
    k = 2.0
    m1 = m2 = m3 = m4 = 0.0
    for _ in range(runs):
        x = random.gauss(0.0, 1.0 / math.sqrt(2.0))
        w = 0.0
        dla = 2.0 / steps
        for _l in (0, 1):
            lam0 = 0.0 if _l == 0 else 2.0
            for s in range(steps):
                lam_mid = lam0 + dla * (s + 0.5)
                z = random.gauss(0.0, 1.0)
                xp = x - k * (x - lam_mid) * dt + sig * z
                x = x + 0.5 * (-k * (x - lam_mid) - k * (xp - lam_mid)) * dt + sig * z
                w += k * (lam_mid - x) * dla
        m1 += w; m2 += w * w; m3 += w ** 3; m4 += w ** 4
    return moments_from(runs, m1, m2, m3, m4)

def run_stiff(runs, tau1, tau2fast, tau2slow, mode):
    """Demon trap V = lambda x^2/2, 1->2->1; bit feeds the return speed.
    mode: 'control' (fixed), 'sign', 'far' (median threshold)."""
    steps1 = max(1, int(round(tau1 / DT)))
    dt1 = tau1 / steps1
    sig1 = math.sqrt(2.0 * dt1)
    m1 = m2 = m3 = m4 = 0.0
    em = 0.0
    for _ in range(runs):
        x = random.gauss(0.0, 1.0)
        xo = x
        w = 0.0
        dl = 1.0
        for s in range(steps1):
            la = 1.0 + dl * (s + 0.5) / steps1
            z = random.gauss(0.0, 1.0)
            k1 = -la * xo
            xp = xo + k1 * dt1 + sig1 * z
            k2 = -la * xp
            x = xo + 0.5 * (k1 + k2) * dt1 + sig1 * z
            w += 0.5 * (xo * xo + x * x) * (dl / steps1) * 0.5
            xo = x
        x_mid = x
        if mode == "control":
            is_fast = True
        elif mode == "sign":
            is_fast = x_mid > 0
        else:
            is_fast = abs(x_mid) > FAR_THRESHOLD
        tau2 = tau2fast if is_fast else tau2slow
        steps2 = max(1, int(round(tau2 / DT)))
        dt2 = tau2 / steps2
        sig2 = math.sqrt(2.0 * dt2)
        dl = -1.0
        for s in range(steps2):
            la = 2.0 + dl * (s + 0.5) / steps2
            z = random.gauss(0.0, 1.0)
            k1 = -la * xo
            xp = xo + k1 * dt2 + sig2 * z
            k2 = -la * xp
            x = xo + 0.5 * (k1 + k2) * dt2 + sig2 * z
            w += 0.5 * (xo * xo + x * x) * (dl / steps2) * 0.5
            xo = x
        m1 += w; m2 += w * w; m3 += w ** 3; m4 += w ** 4
        em += math.exp(-w)
    d = moments_from(runs, m1, m2, m3, m4)
    d["J"] = em / runs
    d["lnJ"] = math.log(d["J"])
    return d

def cal_median():
    runs = 100000
    xm = []
    steps = 50
    dt1 = 0.5 / steps
    sig1 = math.sqrt(2.0 * dt1)
    for _ in range(runs):
        x = random.gauss(0.0, 1.0)
        xo = x
        for s in range(steps):
            la = 1.0 + 1.0 * (s + 0.5) / steps
            z = random.gauss(0.0, 1.0)
            k1 = -la * xo
            xp = xo + k1 * dt1 + sig1 * z
            k2 = -la * xp
            x = xo + 0.5 * (k1 + k2) * dt1 + sig1 * z
            xo = x
        xm.append(abs(x))
    xm.sort()
    return xm[runs // 2]

print("Ch.76 Precisely Priced: the TUR as the Demon's Handling Fee")
print("  TUR: Var(W) >= 2 <W>/beta (DeltaF = 0, <W> > 0); q = 2 <W>/Var <= 1")
print("  the parabola (exactly Gaussian work) saturates: q = 1, slack = 0")
print("  the coin (feedback bit) bends the parabola: q < 1 (a fee on knowing)")
print("")

print("[A] THE PARABOLA: dragged trap V = k(x-lambda)^2/2, k=2, 0->2->0")
print("  tau     <W>       Var        q=2<W>/Var   slack     skew       kurt")
A = []
for tau in [1.0, 2.0, 4.0]:
    d = run_drag(150000, tau)
    A.append((tau, d))
    print("  %.1f   %+.5f  %.5f   %.5f     %+.5f   %+.4f   %+.4f"
          % (tau, d["mu"], d["var"], d["q"], 1.0 - d["q"], d["skew"], d["kurt"]))

print("")
print("[B] THE DEMON: stiffness round trip V = lam x^2/2, 1->2->1, fair bit")
FAR_THRESHOLD = cal_median()
rcal = run_stiff(60000, 0.5, 0.35, 2.0, "far")
print("  median |x_mid| = %.4f ; coin = ln2 = %.4f" % (FAR_THRESHOLD, COIN))
print("  row            <W>        Var        q=2<W>/Var  slack     skew     kurt      lnJ       W_net")
B = []
rows = [("control 0.50", 0.5, 0.5, "control", 150000),
        ("dead sign 0.4/3", 0.4, 3.0, "sign", 150000),
        ("engaged 0.4/1.5", 0.4, 1.5, "far", 150000),
        ("engaged 0.35/2", 0.35, 2.0, "far", 150000),
        ("engaged 0.25/4", 0.25, 4.0, "far", 150000),
        ("HARVEST 0.10/8", 0.10, 8.0, "far", 120000),
        ("HARVEST 0.05/16", 0.05, 16.0, "far", 80000)]
for (name, tf, ts, mode, n) in rows:
    d = run_stiff(n, 0.5, tf, ts, mode)
    flag = "  (W<0: coins bill of Ch.75 governs)" if d["mu"] < 0 else ""
    print("  %-16s %+0.5f  %.5f  %.5f   %+.5f  %+.4f  %+.4f  %+.5f   %+.5f%s"
          % (name, d["mu"], d["var"], d["q"], 1.0 - d["q"], d["skew"], d["kurt"],
             d["lnJ"], d["mu"] + COIN, flag))
    B.append((name, tf, ts, mode, n, d))

data = {
    "chapter": 76,
    "title": "Precisely Priced: the Thermodynamic Uncertainty Relation as the Demon's Handling Fee (Barato-Seifert 2015, Gingrich et al. 2016)",
    "beta": 1.0, "delta_f": 0.0, "coin": COIN,
    "parabola": [{"tau": tau, "mean_work": d["mu"], "var": d["var"], "q": d["q"],
                  "slack": 1.0 - d["q"], "skew": d["skew"], "kurt": d["kurt"]}
                 for (tau, d) in A],
    "demon": [{"name": name, "tau_fast": tf, "tau_slow": ts, "mode": mode,
               "n": n, "mean_work": d["mu"], "var": d["var"], "q": d["q"],
               "slack": 1.0 - d["q"], "skew": d["skew"], "kurt": d["kurt"],
               "lnJ": d["lnJ"], "net_cost": d["mu"] + COIN}
              for (name, tf, ts, mode, n, d) in B],
    "threshold_median_abs_xmid": FAR_THRESHOLD,
    "removable_value": 1.0,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "tur_ledger.json")
with open(out, "w") as fh:
    json.dump(data, fh, indent=2)
print("")
print("json ->", out)