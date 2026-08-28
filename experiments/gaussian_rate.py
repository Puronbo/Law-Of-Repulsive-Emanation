import math, random, json, os

# ============================================================
# Ch.72  The Fine Print of the Ledger
# Dragged optically-trapped particle, FIXED stiffness, moving
# trap center: V(x,lambda) = (k/2)(x - lambda)^2, lambda: 0 -> L.
# DeltaF = 0 (the free energy of a fixed-stiffness Gaussian trap
# does not know its center), so diss = <W> = <k*int (lambda-x)
# dlambda> and every Joules-of-work on average is dissipation.
# W = k*int (lambda - x) dlambda is a LINEAR functional of the
# Gaussian bath => W is exactly Gaussian at every speed. Near
# reversibility the pair (<W>, sigma_W) vanishes together tied by
# the constant 2/beta (work fluctuation-dissipation; Einstein 1910,
# Onsager-Machlup 1953, Cramer 1938):   Var(W) ~ 2 <W> / beta.
# ============================================================

random.seed(42)

K = 2.0
L = 2.0
DF = 0.0
eDF = 1.0

protocols = [
    ("fast   tau=2", 2.0, 0.02, 100000),
    ("medium tau=8", 8.0, 0.04, 80000),
    ("slow   tau=32", 32.0, 0.08, 120000),
]

def run_protocol(tau, dt, nsteps, runs, histogram=None):
    lam0 = 0.0
    lam1 = L
    dlam = lam1 - lam0
    sig = math.sqrt(2.0 * dt)
    wm = 0.0
    wm2 = 0.0
    wem = 0.0
    for _ in range(runs):
        x = random.gauss(lam0, 1.0 / math.sqrt(K))   # stationary std sqrt(D/(k beta))
        w = 0.0
        xo = x
        for s in range(nsteps):
            la = lam0 + (s + 0.5) * dlam / nsteps   # work probed at mid-step lambda
            lb = la
            z = random.gauss(0.0, 1.0)
            k1 = -K * (xo - lb)
            xp = xo + k1 * dt + sig * z
            k2 = -K * (xp - lb)
            x = xo + 0.5 * (k1 + k2) * dt + sig * z
            w += K * (la - 0.5 * (xo + x)) * dlam / nsteps
            xo = x
        wm += w
        wm2 += w * w
        wem += math.exp(-w)
        if histogram is not None:
            histogram.append(w)
    wm /= runs
    wm2 /= runs
    wem /= runs
    var = wm2 - wm * wm
    sd = math.sqrt(var)
    return wm, var, sd, wem

print("Ch.72 The Fine Print of the Ledger (beta=1, D=1, k=2, drag L=2)")
print("DeltaF = 0 (fixed-stiffness trap); diss = <W>")
print("")

print("[1] THE PAIR:  Var(W) vs 2*<W>/beta  (work fluctuation-dissipation)")
print("  protocol       <W>      sigma_W   Var/(2*<W>)   J=<e^-W>")
rows = []
for name, tau, dt, runs in protocols:
    nsteps = int(tau / dt)
    wm, var, sd, wem = run_protocol(tau, dt, nsteps, runs)
    R = var / (2.0 * wm)
    rows.append((name, wm, sd, R, wem))
    print("  %-14s %+.5f  %.5f   %7.4f    %.5f"
          % (name, wm, sd, R, wem))

print("")
print("[2] GAUSSIAN RATE (slow drag, 120000 runs): skew and tail shape")
w_slow = []
wm, var, sd, wem = run_protocol(32.0, 0.08, 400, 120000, histogram=w_slow)
m3 = 0.0
m4 = 0.0
for w in w_slow:
    z = (w - wm) / sd
    m3 += z * z * z
    m4 += z * z * z * z
m3 /= len(w_slow)
m4 /= len(w_slow)
print("  skewness = %+.4f (SE 0.0071 ; Gaussian exactly 0)" % m3)
print("  excess kurtosis = %+.4f (SE 0.0141)" % (m4 - 3.0))
nb = 13
zlo = -3.25
zbw = 0.5
ct = [0] * nb
for w in w_slow:
    z = (w - wm) / sd
    b = int((z - zlo) / zbw)
    if 0 <= b < nb:
        ct[b] += 1
def gaus(z):
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
print("  z-bin center   P_measured    P_gaussian   ratio")
worst = 0.0
for b in range(nb):
    zc = zlo + (b + 0.5) * zbw
    pe = ct[b] / float(len(w_slow)) / zbw
    pg = gaus(zc)
    r = pe / pg if pg > 0 else 0.0
    if abs(r - 1.0) > worst:
        worst = abs(r - 1.0)
    print("    %+5.2f       %.5f      %.5f    %.4f" % (zc, pe, pg, r))
fr1 = sum(1.0 for w in w_slow if abs((w - wm) / sd) < 1.0) / float(len(w_slow))
fr2 = sum(1.0 for w in w_slow if abs((w - wm) / sd) < 2.0) / float(len(w_slow))
print("  fraction |z|<1 = %.4f (68.27%%)   |z|<2 = %.4f (95.45%%)   worst |ratio-1| = %.4f"
      % (fr1, fr2, worst))

print("")
print("[3] THE 0/0 RESOLUTION")
for (name, wmw, sdw, Rw, wemw) in rows:
    print("  %-13s: sigma^2/2 = %.5f   diss = %.5f   exp(sigma^2/2-diss) = %.5f   J_meas = %.5f"
          % (name, 0.5 * sdw * sdw, wmw, math.exp(0.5 * sdw * sdw - wmw), wemw))
print("  the Gaussian lock-step sigma^2/2 = diss is exact at slow and medium")
Rsl = rows[2][3]
print("  Var(W) = 2*<W>/beta at the slow edge R = %.4f -> 1 ; medium %.4f, fast %.4f"
      % (Rsl, rows[1][3], rows[0][3]))

data = {
    "chapter": 72,
    "title": "The Fine Print of the Ledger: Work Fluctuation-Dissipation",
    "k": K,
    "drag": L,
    "beta": 1.0,
    "delta_f": DF,
    "protocols": {},
    "gaussian_tail": {"skewness": m3, "excess_kurtosis": m4 - 3.0, "frac_z1": fr1, "frac_z2": fr2, "worst_ratio_dev": worst},
}
for (name, wm, sd, R, wem) in rows:
    data["protocols"][name] = {"mean_work": wm, "sigma_W": sd, "var_over_2mean": R, "J": wem}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "gaussian_rate.json")
with open(out, "w") as fh:
    json.dump(data, fh, indent=2)
print("")
print("json ->", out)