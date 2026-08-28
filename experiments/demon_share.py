import math, random, json, os

# ============================================================
# Ch.74  The Demon's Share
# The exponential ledger under feedback: one bit (I = ln 2) is
# worth nothing if it cannot act, and worth the whole ledger's
# overshoot when it predicts the work. Control: ramp 1->2->1
# round trip (DeltaF = 0), <e^{-W}> = 1 exactly (Jarzynski).
# BIT 1 (sign of x) is statistically irrelevant to a symmetric
# trap - feeding it to the return speed changes nothing (the
# null measurement: unused information is unheard).
# BIT 2 (|x| above/below the median of |x|) predicts the work
# of the return: a far particle releases a big negative W over
# a fast expansion, a near particle returns almost freely.
# Feeding that bit to the return speed makes the ledger pay:
# J = <e^{-W}> rises 1 -> ~2 with leverage, bounded by e^I.
# Generalized second law with feedback (Sagawa-Ueda 2008/2010;
# toyabe et al. Nature Phys. 6, 988 (2010) measured the same
# coin: work per bit ~ ln2 k_BT).
# ============================================================

random.seed(42)

DT = 0.01

def run_roundtrip(runs, tau1, tau2fast, tau2slow, mode):
    """mode: 'control' (fixed return speed), 'sign' (bit = sign of x),
    'far' (bit = |x| > median). 'far' needs the median of |x_mid| passed in
    as tau2slow... we pass a threshold via global. Returns J and stats."""
    steps1 = max(1, int(round(tau1 / DT)))
    dt1 = tau1 / steps1
    sig1 = math.sqrt(2.0 * dt1)
    em = 0.0
    em_f = 0.0
    em_s = 0.0
    n_f = 0
    n_s = 0
    wm = 0.0
    wm_f = 0.0
    wm_s = 0.0
    for _ in range(runs):
        x = random.gauss(0.0, 1.0)
        xo = x
        w1 = 0.0
        dl = 1.0
        for s in range(steps1):
            la = 1.0 + dl * (s + 0.5) / steps1
            z = random.gauss(0.0, 1.0)
            k1 = -la * xo
            xp = xo + k1 * dt1 + sig1 * z
            k2 = -la * xp
            x = xo + 0.5 * (k1 + k2) * dt1 + sig1 * z
            w1 += 0.5 * (xo * xo + x * x) * (dl / steps1) * 0.5
            xo = x
        x_mid = x
        if mode == "control":
            is_fast = True
        elif mode == "sign":
            is_fast = x_mid > 0
        elif mode == "far":
            is_fast = abs(x_mid) > FAR_THRESHOLD
        else:
            is_fast = True
        tau2 = tau2fast if is_fast else tau2slow
        steps2 = max(1, int(round(tau2 / DT)))
        dt2 = tau2 / steps2
        sig2 = math.sqrt(2.0 * dt2)
        w2 = 0.0
        dl = -1.0
        for s in range(steps2):
            la = 2.0 + dl * (s + 0.5) / steps2
            z = random.gauss(0.0, 1.0)
            k1 = -la * xo
            xp = xo + k1 * dt2 + sig2 * z
            k2 = -la * xp
            x = xo + 0.5 * (k1 + k2) * dt2 + sig2 * z
            w2 += 0.5 * (xo * xo + x * x) * (dl / steps2) * 0.5
            xo = x
        w = w1 + w2
        wm += w
        ew = math.exp(-w)
        em += ew
        if is_fast:
            n_f += 1
            em_f += ew
            wm_f += w
        else:
            n_s += 1
            em_s += ew
            wm_s += w
    return dict(J=em / runs, J_f=em_f / max(1, n_f), J_s=em_s / max(1, n_s),
                n_f=n_f, n_s=n_s, p_fast=n_f / runs,
                wm=wm / runs, wm_f=wm_f / max(1, n_f), wm_s=wm_s / max(1, n_s))

print("Ch.74 The Demon's Share: One Bit on the Ledger")
print("  D = beta = 1 ; ramp 1->2->1 (DeltaF=0) ; control <e^-W> = 1 exact")
print("")

FAR_THRESHOLD = 0.6   # reset to the median(|x_mid|) found in block [0] below

print("[0] THE BIT: a fair bit cut at the median of |x_mid|")
med_runs = 100000
xm = []
steps = 50
dt1 = 0.5 / steps
sig1 = math.sqrt(2.0 * dt1)
for _ in range(med_runs):
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
FAR_THRESHOLD = xm[med_runs // 2]
r = run_roundtrip(60000, 0.5, 0.35, 2.0, "far")
print("  median(|x_mid|) = %.4f ; cut there -> fair bit: p(far) = %.4f"
      % (FAR_THRESHOLD, r["p_fast"]))
print("  I = ln 2 = %.4f nats ; ceiling for this bit: J <= e^I = %.4f"
      % (math.log(2.0), 2.0))

print("")
print("[1] CONTROL (no feedback): round-trip ledger")
control_rows = []
for tau in [0.5, 1.0]:
    r = run_roundtrip(120000, 0.5, tau, tau, "control")
    control_rows.append((tau, r))
    print("  tau=%.2f: J = <e^-W> = %.5f  (1.000 exact; ln J = %+.5f)  <W> = %+.5f"
          % (tau, r["J"], math.log(r["J"]), r["wm"]))

print("")
print("[2] NULL METER: sign bit -> return speed (unused info is unheard)")
r0 = run_roundtrip(200000, 0.5, 0.4, 3.0, "sign")
print("  J = %.5f  ln J = %+.5f   p(fast)=%.4f   <W> = %+.5f"
      % (r0["J"], math.log(r0["J"]), r0["p_fast"], r0["wm"]))

print("")
print("[3] THE ENGAGED BIT: far/near -> return speed (the ledger pays)")
print("  expected ceiling J <= e^{ln2} = 2.000 per bit (Sagawa-Ueda 2010)")
curve = []
for (tf, ts) in [(0.35, 2.0), (0.25, 4.0), (0.15, 6.0), (0.10, 8.0)]:
    rr = run_roundtrip(200000, 0.5, tf, ts, "far")
    curve.append((tf, ts, rr))
    print("  fast %.2f / slow %.2f: J = %.4f   ln J = %.4f   p(far)=%.4f   <W> = %+.5f"
          % (tf, ts, rr["J"], math.log(rr["J"]), rr["p_fast"], rr["wm"]))
J_act = curve[-1][2]["J"]
print("  J_act/J_control = %.3f ;  J_act/e^{ln2} = %.3f" % (J_act, J_act / 2.0))

print("")
print("[4] THE 0/0 RESOLUTION")
print("  no bit: J = 1 ;  a bit in hand that cannot act keeps J = 1 ;")
print("  a bit that predicts the work raises J toward e^I - information")
print("  is currency only when spent causally (books close with I).")

data = {
    "chapter": 74,
    "title": "The Demon's Share: Unused Information Is Unheard (Sagawa-Ueda 2008/2010)",
    "beta": 1.0, "delta_f": 0.0, "I_bit": math.log(2.0),
    "threshold_median_abs_xmid": FAR_THRESHOLD,
    "control": [{"tau": tau, "J": r["J"], "lnJ": math.log(r["J"]),
                 "mean_work": r["wm"]} for (tau, r) in control_rows],
    "null_sign": {"J": r0["J"], "lnJ": math.log(r0["J"]),
                  "p_fast": r0["p_fast"], "mean_work": r0["wm"]},
    "engaged_curve": [{"tau_fast": tf, "tau_slow": ts, "J": rr["J"],
                       "lnJ": math.log(rr["J"]), "p_far": rr["p_fast"],
                       "mean_work": rr["wm"]} for (tf, ts, rr) in curve],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "demon_share.json")
with open(out, "w") as fh:
    json.dump(data, fh, indent=2)
print("")
print("json ->", out)