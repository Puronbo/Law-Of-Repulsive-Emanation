import math, random, json, os

# ============================================================
# Ch.71  Jarzynski's 0/0: the Loan Always Repaid
# Jarzynski 1997, Crooks 1999
# Overdamped trap V(x,lambda) = lambda*x^2/2, stiffness ramp 1 -> 2
# at three speeds; heat bath D = k_B T = 1 (beta = 1).
# The dissipated work W - DeltaF is 0/0: mean-deficit and dispersion
# vanish together only at the reversible speed, yet the exponential
# ledger <e^{-W}> = e^{-DeltaF} balances exactly at EVERY speed.
# Heun integrator (SRK2) + trapezoidal work kill the O(dt) bias.
# ============================================================

random.seed(42)

LI = 1.0
LF = 2.0
DL = LF - LI
DF = 0.5 * math.log(LF / LI)          # free energy of the ramp
eDF = math.exp(-DF)                    # target for <e^{-W}>

protocols = [
    ("fast   tau=0.5", 0.5, 0.005, 400000),
    ("medium tau=2.0", 2.0, 0.010, 120000),
    ("slow  tau=8.0", 8.0, 0.020, 50000),
]

def run_protocol(tau, dt, nsteps, runs, reverse=False):
    lam0 = LF if reverse else LI
    lam1 = LI if reverse else LF
    dlam = lam1 - lam0
    sig = math.sqrt(2.0 * dt)
    wm = 0.0
    wm2 = 0.0
    wem = 0.0
    we2 = 0.0
    for _ in range(runs):
        x = random.gauss(0.0, 1.0 / math.sqrt(lam0))  # stationary var 1/lam0
        w = 0.0
        xo = x
        for k in range(nsteps):
            la = lam0 + k * dlam / nsteps
            lb = lam0 + (k + 1) * dlam / nsteps
            z = random.gauss(0.0, 1.0)
            k1 = -la * xo
            xp = xo + k1 * dt + sig * z
            k2 = -lb * xp
            x = xo + 0.5 * (k1 + k2) * dt + sig * z
            w += 0.5 * (xo * xo + x * x) * 0.5 * dlam / nsteps
            xo = x
        wm += w
        wm2 += w * w
        ew = math.exp(-w)
        wem += ew
        we2 += ew * ew
    wm /= runs
    wm2 /= runs
    wem /= runs
    we2 /= runs
    varW = wm2 - wm * wm
    seJ = math.sqrt((we2 - wem * wem) / runs)
    return wm, varW, wem, seJ

print("Ch.71 Jarzynski's 0/0: the Loan Always Repaid (beta=1, D=1)")
print("V(x,lambda)=lambda x^2/2, ramp 1 -> 2    DeltaF = %.4f   e^(-DeltaF) = %.6f"
      % (DF, eDF))
print("")

results = {}
print("[1] THE LEDGER AT EVERY SPEED")
print("  protocol       <W>       W-DeltaF    sigma_W   <e^-W>    J=<e^-W>/e^-DF")
for name, tau, dt, runs in protocols:
    nsteps = int(tau / dt)
    wm, varW, wem, seJ = run_protocol(tau, dt, nsteps, runs)
    j = wem / eDF
    results[name] = {
        "tau": tau, "dt": dt, "runs": runs, "mean_work": wm,
        "dissipation": wm - DF, "sigma_W": math.sqrt(varW),
        "mean_exp_negW": wem, "J": j, "se_J": seJ / eDF,
    }
    print("  %-14s %.5f   %+7.4f   %.5f   %.6f   %.5f +/- %.4f"
          % (name, wm, wm - DF, math.sqrt(varW), wem, j, seJ / eDF))

print("")
print("[2] CROOKS: the interest rate of the loan")
tau, dt, runs = 2.0, 0.01, 120000
nsteps = int(tau / dt)
binw = 0.2
wmin = -0.4
wmax = 1.6
nb = int((wmax - wmin) / binw)
hf = [0] * nb
hr = [0] * nb

def hist_fill(runs, reverse, h):
    lam0 = LF if reverse else LI
    lam1 = LI if reverse else LF
    dlam = lam1 - lam0
    sig = math.sqrt(2.0 * dt)
    for _ in range(runs):
        x = random.gauss(0.0, 1.0 / math.sqrt(lam0))
        w = 0.0
        xo = x
        for k in range(nsteps):
            la = lam0 + k * dlam / nsteps
            lb = lam0 + (k + 1) * dlam / nsteps
            z = random.gauss(0.0, 1.0)
            k1 = -la * xo
            xp = xo + k1 * dt + sig * z
            k2 = -lb * xp
            x = xo + 0.5 * (k1 + k2) * dt + sig * z
            w += 0.5 * (xo * xo + x * x) * 0.5 * dlam / nsteps
            xo = x
        wb = w if not reverse else -w
        b = int((wb - wmin) / binw)
        if 0 <= b < nb:
            h[b] += 1

hist_fill(runs, False, hf)
hist_fill(runs, True, hr)
pts = []
for b in range(nb):
    if hf[b] >= 30 and hr[b] >= 30:
        wc = wmin + (b + 0.5) * binw
        ratio = hf[b] / float(hr[b])
        pts.append((wc, math.log(max(ratio, 1e-300)), hf[b], hr[b]))
print("  bin   W       ln[P_F(W)/P_R(-W)]   theory W-DeltaF   (n_f, n_r)")
for wc, lr, nf, nr in pts:
    print("  %4.2f  %8.4f            %8.4f        (%d, %d)" % (wc, lr, wc - DF, nf, nr))
if len(pts) >= 3:
    n = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] * p[0] for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    inter = (sy - slope * sx) / n
    print("  linear fit over %d bins: ln ratio = %.4f + (%.4f) W  ->  beta = %.4f (theory 1.0000)"
          % (n, inter, slope, slope))
    results["crooks_beta"] = slope
    results["crooks_bins"] = [{"W": wc, "ln_ratio": lr, "n_f": nf, "n_r": nr} for wc, lr, nf, nr in pts]
else:
    print("  too few overlapping bins for a slope")

print("")
print("[3] THE 0/0 RESOLUTION")
print("  W - DeltaF -> 0 as tau -> inf (reversible), but the exponential")
print("  mean does NOT commute with the exponent: <e^(-W)> = e^(-DeltaF)")
print("  exactly at fast, medium, and slow alike. Dissipation is on average")
print("  always positive (the second law), yet Crooks' ratio prices the")
print("  rare refunds: P_F(W)/P_R(-W) = e^(W-DeltaF), slope beta.")

data = {
    "chapter": 71,
    "title": "Jarzynski's 0/0: the Loan Always Repaid",
    "lambda_i": LI,
    "lambda_f": LF,
    "beta": 1.0,
    "delta_f": DF,
    "e_minus_delta_f": eDF,
    "protocols": results,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "jarzynski.json")
with open(out, "w") as fh:
    json.dump(data, fh, indent=2)
print("")
print("json ->", out)