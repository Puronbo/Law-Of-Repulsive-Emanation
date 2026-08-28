import math, random, json, os

# ============================================================
# Ch.70  Stochastic Resonance: the Amplified 0/0
# Double well V(x) = x^4/4 - x^2/2   (barrier DU = 1/4, wells +-1)
# Subthreshold periodic drive A*sin(w t), A = 0.1 < critical tilt A*.
# Noise variance D plays the role of temperature (k_B T).
# Gain vs D is a 0/0: frozen (static tilt) at D->0, buried at D->inf;
# the removable value is the synchronized crossing peak.
# Committed-well counting (hysteresis 0.5) = Schmitt-trigger measure.
# ============================================================

random.seed(42)

A     = 0.1
f_s   = 0.05
w     = 2.0 * math.pi * f_s
dt    = 0.01
T     = 3500.0
N     = int(T / dt)
NREP  = 3
DU    = 0.25
ASTAR = 2.0 / (3.0 * math.sqrt(3.0))
Q     = math.sqrt(2.0) / (2.0 * math.pi)
DSTAR = DU / math.log(Q / f_s)          # where r(D) = f_s

DS  = [0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.155, 0.18, 0.20, 0.22,
       0.24, 0.30, 0.45, 0.70, 1.00, 1.50, 2.00]
KDS = [0.07, 0.085, 0.10, 0.115, 0.13]      # law regime, T=40000 s
TK  = 40000.0
NK  = int(TK / dt)


def integrate(D, driven, nsteps):
    sig = math.sqrt(2.0 * D * dt)
    x = 1.0
    cw = 1.0
    cross = 0
    cc = 0.0; sc = 0.0; xs = 0.0
    bc = 0.0; bs = 0.0; bsum = 0.0; bsq = 0.0
    for k in range(nsteps):
        t = k * dt
        f = -x * x * x + x
        if driven:
            f += A * math.sin(w * t)
        x += f * dt + sig * random.gauss(0.0, 1.0)
        cc += x * math.cos(w * t)
        sc += x * math.sin(w * t)
        xs += x
        b = 1.0 if x >= 0.0 else -1.0
        bc += b * math.cos(w * t)
        bs += b * math.sin(w * t)
        bsum += b
        bsq += 1.0
        if x > 0.5:
            if cw < 0.0:
                cross += 1
            cw = 1.0
        elif x < -0.5:
            if cw > 0.0:
                cross += 1
            cw = -1.0
    mean = xs / nsteps
    bmean = bsum / nsteps
    bvar = bsq / nsteps - bmean * bmean
    return cc, sc, mean, cross, bc, bs, bmean, bvar


def measure(D, driven, nsteps=350000, reps=NREP):
    cc = 0.0; sc = 0.0; cr = 0
    bc = 0.0; bs = 0.0; bm = 0.0; bv = 0.0
    for rep in range(reps):
        r = integrate(D, driven, nsteps)
        cc += r[0]; sc += r[1]; cr += r[3]
        bc += r[4]; bs += r[5]; bm += r[6]; bv += r[7]
    cc /= reps; sc /= reps; bc /= reps; bs /= reps; bm /= reps; bv /= reps
    cr = int(round(cr / reps))
    acont = 2.0 * math.sqrt(cc * cc + sc * sc) / N
    bAmp = 2.0 * math.sqrt(bc * bc + bs * bs) / N
    resid = max(bv - 0.5 * bAmp * bAmp, 1e-15)
    snr = (0.5 * bAmp * bAmp) / resid
    return acont, cr, bAmp, resid, snr


print("Ch.70 Stochastic Resonance: the Amplified 0/0")
print("V(x)=x^4/4-x^2/2  DU=%.2f  wells +-1  drive A=%.2f < A*=%.4f" % (DU, A, ASTAR))
print("f_s=%.3f Hz  T=%.0f s dt=%.3f (175 cycles, %d reps)  Kramers grid T=%.0f s"
      % (f_s, T, dt, NREP, TK))
print("static well response A/V''=%.3f ;  Q=sqrt2/2pi=%.6f" % (A / 2.0, Q))

print("")
print("[1] THE BELL  coherent response at f_s vs noise D (committed flips)")
print("  D     A_cont   g_c=A/A_static   SNR_b   flips/s")
cs = []
for D in DS:
    acont, cr, bAmp, resid, snr = measure(D, True)
    gc = acont / (A / 2.0)
    cs.append((D, acont, gc, snr, cr))
    print("  %5.3f  %.5f    %6.2f        %9.4f   %.3f" % (D, acont, gc, snr, cr / T))

print("")
print("[2] KRAMERS LAW  r(D) = Q exp(-DU/D), law regime only")
pk = []
for D in KDS:
    _, cr, _, _, _ = measure(D, False, nsteps=NK, reps=1)
    r = cr / TK
    rT = Q * math.exp(-DU / D)
    pk.append((1.0 / D, math.log(r)))
    print("  D=%5.3f  r_meas=%.5e  r_theory=%.5e  ratio=%.3f  flips=%d"
          % (D, r, rT, r / rT, cr))
n = len(pk)
sx = sum(p[0] for p in pk); sy = sum(p[1] for p in pk)
sxx = sum(p[0] * p[0] for p in pk); sxy = sum(p[0] * p[1] for p in pk)
slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
duMeas = -slope
ratio = duMeas / DU
print("  fit: ln r = %.4f - (%.5f)/D   DU_meas/DU = %.4f   (Kramers 1940)" % (sy / n - slope * sx / n, duMeas, ratio))

best = max(cs, key=lambda p: p[2])
print("")
print("[3] THE AMPLIFIED 0/0")
print("  g_c(D->0)   = %.2f ~ 1 : static tilt only, zero amplification" % min(cs, key=lambda p: p[0])[2])
print("  g_c(D_opt)  = %.2f at D_opt=%.3f : amplification %d%% over the floor"
      % (best[2], best[0], int(round(100.0 * (best[2] - 1.0)))))
print("  g_c(D->inf) -> 0 : signal buried under the repayment")
rb = measure(best[0], True, reps=NREP)
r_opt = rb[1] / T
rT_opt = Q * math.exp(-DU / best[0])
print("  at the peak : r_opt = %.4f Hz  r/f_s = %.3f  r/(2 f_s) = %.3f   (theory r=%.4f)"
      % (r_opt, r_opt / f_s, r_opt / (2.0 * f_s), rT_opt))
print("  matching identity r(D)=f_s : D* = %.3f ;  D_opt/D* = %.3f" % (DSTAR, best[0] / DSTAR))
print("  D_opt/(DU/2) = %.3f  : the optimum noise sits where the leak meets the signal"
      % (best[0] / (DU / 2.0)))

data = {
    "chapter": 70,
    "title": "Stochastic Resonance: the Amplified 0/0",
    "V": "x^4/4 - x^2/2",
    "DU": DU,
    "A": A,
    "a_star": ASTAR,
    "f_s": f_s,
    "Q": Q,
    "du_measured": duMeas,
    "du_ratio": ratio,
    "d_opt": best[0],
    "d_star": DSTAR,
    "d_opt_over_dstar": best[0] / DSTAR,
    "gain_peak": best[2],
    "r_opt": r_opt,
    "r_over_fs": r_opt / f_s,
    "gain_curve": [(d, g) for d, a, g, s, c in cs],
    "snr_curve": [(d, s) for d, a, g, s, c in cs],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "stochastic_resonance.json")
with open(out, "w") as fh:
    json.dump(data, fh, indent=2)
print("")
print("json ->", out)