import math, random, json, os

# ============================================================
# Ch.73  The Engine and Its Fine Print
# Harmonic-trap heat engine, full closed cycle, overdamped OU:
#   hot isotherm   lambda 4->1 at T_h=2 (expansion, work out)
#   adiabat        lambda 1->0.5 instant (cools to T_c=1)
#   cold isotherm  lambda 0.5->2 at T_c=1 (compression, work in)
#   adiabat        lambda 2->4 instant (reheats to T_h)
# DeltaF = 0 on each isotherm; the work comes from the thermal
# gradient T_h/T_c = 2. The 0/0 pair (P -> 0, eta -> eta_C=1/2):
# only the zero-power machine reaches Carnot; the removable
# singularity is the efficiency at maximum power, bounded by
# eta_C/(2-eta_C) = 1/3 (Schmiedl-Seifert 2008) in the Gaussian
# regime - the FDT lock-step of Ch.72 pricing the throughput.
# ============================================================

random.seed(42)

T_H, T_C = 2.0, 1.0
L_HS, L_HE = 4.0, 1.0  # hot expansion 4 -> 1
L_CS, L_CE = 0.5, 2.0  # cold compression 0.5 -> 2

ETA_C = 1.0 - T_C / T_H
ETA_MP = ETA_C / (2.0 - ETA_C)

WO_QUASI = (T_H / 2.0) * math.log(L_HS / L_HE) - (T_C / 2.0) * math.log(L_CE / L_CS)
QI_QUASI = (T_H / 2.0) * math.log(L_HS / L_HE)

def isotherm(x, lam_start, lam_end, T, t_iso, p=1.0, dt=0.01):
    """One isothermal stroke from current x. Heun (SRK2), lambda(u)=lambda_s+dl*u^p.
    Returns (x_final, w, du)."""
    steps = max(1, int(round(t_iso / dt)))
    dt_i = t_iso / steps
    sig = math.sqrt(2.0 * T * dt_i)
    xo = x
    u0 = 0.5 * lam_start * xo * xo
    w = 0.0
    dl = lam_end - lam_start
    for s in range(steps):
        ua = s / steps
        ub = (s + 1) / steps
        um = 0.5 * (ua + ub)
        la = lam_start + dl * (ua ** p)
        lb = lam_start + dl * (ub ** p)
        lm = lam_start + dl * (um ** p)
        dL = lb - la
        z = random.gauss(0.0, 1.0)
        k1 = -lm * xo
        xp = xo + k1 * dt_i + sig * z
        k2 = -lm * xp
        x = xo + 0.5 * (k1 + k2) * dt_i + sig * z
        w += 0.25 * (xo * xo + x * x) * dL
        xo = x
    du = 0.5 * lam_end * x * x - u0
    return x, w, du

def engine_steady(t_h, t_c, cycles, runs, p=1.0):
    """Full closed cycle. Adiabats are instant lambda jumps at frozen x.
    Returns means over cycles (average of cycles 1..cycles-1)."""
    dt = 0.01 if max(t_h, t_c) <= 2.0 else 0.02
    acc = None
    for _ in range(runs):
        x = random.gauss(0.0, math.sqrt(T_H / L_HS))
        for k in range(cycles):
            x, w_h, du_h = isotherm(x, L_HS, L_HE, T_H, t_h, p, dt)
            x1 = x
            w_a1 = 0.5 * (L_CS - L_HE) * x1 * x1
            x, w_c, du_c = isotherm(x, L_CS, L_CE, T_C, t_c, p, dt)
            x2 = x
            w_a2 = 0.5 * (L_HS - L_CE) * x2 * x2
            q_h = du_h - w_h
            q_c = du_c - w_c
            w_net = w_h + w_c + w_a1 + w_a2
            if acc is None:
                acc = [0.0] * 7
            if k >= 1:
                acc[0] += w_net
                acc[1] += q_h
                acc[2] += q_c
                acc[3] += w_a1
                acc[4] += w_a2
                acc[5] += w_h
                acc[6] += w_c
    n = runs * (cycles - 1)
    wn = acc[0] / n
    qh = acc[1] / n
    qc = acc[2] / n
    eta = -wn / qh if qh > 0 else float("nan")
    return dict(w_net=wn, q_hot=qh, q_cold=qc, w_ad1=acc[3] / n, w_ad2=acc[4] / n,
                w_h=acc[5] / n, w_c=acc[6] / n, eta=eta)

print("Ch.73 The Engine and Its Fine Print (harmonic trap, overdamped, full cycle)")
print("  T_h=%.1f T_c=%.1f  eta_C=%.4f  max-power bound eta_C/(2-eta_C)=%.4f"
      % (T_H, T_C, ETA_C, ETA_MP))
print("  quasistatic: W_out=%.4f  Q_in=%.4f  eta=%.4f  (adiabats zero net)"
      % (WO_QUASI, QI_QUASI, WO_QUASI / QI_QUASI))
print("")

print("[1] THE FRONTIER (linear lambda, equal split, steady cycles)")
front = []
for t in [0.5, 1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]:
    runs = {0.5: 60000, 1.0: 50000, 2.0: 40000, 2.5: 30000, 3.0: 30000,
            3.5: 25000, 4.0: 30000, 5.0: 24000, 6.0: 22000, 8.0: 20000}[t]
    r = engine_steady(t, t, 5, runs)
    front.append({"t": t, "W_out": -r["w_net"], "Q_in": r["q_hot"], "eta": r["eta"],
                  "P": -r["w_net"] / (2 * t)})
    print("  t=%-4.2f W_out=%+.5f Q_in=%.5f P=%+.5f eta=%.4f (second law W_out<=%.4f)"
          % (t, -r["w_net"], r["q_hot"], -r["w_net"] / (2 * t), r["eta"], r["q_hot"] * ETA_C))
pmax = max(front, key=lambda r: r["P"])
print("  max power (linear, equal split): P=%.5f at t=%.2f, eta(P_max)=%.4f (bound %.4f)"
      % (pmax["P"], pmax["t"], pmax["eta"], ETA_MP))
print("")

print("[2] PROTOCOL OPTIMIZATION AT MAXIMUM POWER (fine split x shape, t_total=4.0)")
best = None
for th in [1.2, 1.6, 2.0, 2.4]:
    for p in [0.3, 0.5, 0.7, 1.0]:
        r = engine_steady(th, 4.0 - th, 4, 15000, p)
        P = -r["w_net"] / 4.0
        if P > 0 and (best is None or P > best[0]):
            best = (P, r, th, p)
print("  optimizer: P=%.5f at t_h=%.2f t_c=%.2f p=%.1f -> eta(P_max)=%.4f (1/3=%.4f)"
      % (best[0], best[2], 4.0 - best[2], best[3], best[1]["eta"], ETA_MP))
print("  ratio eta_meas/eta_bound = %.4f" % (best[1]["eta"] / ETA_MP))
print("  adiabat audit: w_ad1=%.5f w_ad2=%.5f (net %.5f, quasistatic 0)"
      % (best[1]["w_ad1"], best[1]["w_ad2"], best[1]["w_ad1"] + best[1]["w_ad2"]))
print("")

print("[3] THE REVERSIBLE CORNER (slow limit)")
r8 = None
import builtins
for fr in front:
    if fr["t"] == 8.0:
        r8 = fr
print("  t=8: eta=%.4f -> eta_C=%.4f ;  P=%.5f -> 0" % (r8["eta"], ETA_C, r8["P"]))

data = {
    "chapter": 73,
    "title": "The Engine and Its Fine Print: Power Prices the Reversible Corner",
    "T_h": T_H, "T_c": T_C, "eta_C": ETA_C, "eta_MP_bound": ETA_MP,
    "quasistatic": {"W_out": WO_QUASI, "Q_in": QI_QUASI},
    "frontier": front,
    "optimized_max_power": {"P": best[0], "t_h": best[2], "t_c": 4.0 - best[2],
                            "p": best[3], "eta": best[1]["eta"],
                            "w_ad1": best[1]["w_ad1"], "w_ad2": best[1]["w_ad2"]},
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "carnot_engine.json")
with open(out, "w") as fh:
    json.dump(data, fh, indent=2)
print("")
print("json ->", out)