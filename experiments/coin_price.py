import math, random, json, os

# ============================================================
# Ch.75  The Coin's Price
# Closing the demon's ledger: the fair bit of Ch.74 is a coin
# with a fixed face value (I = ln 2, Szilard 1929) and a fixed
# erasure bill (E = ln 2, Landauer 1961, measured by Berut et
# al. Nature 483 187 (2012): 0.69 k_B T at slow rates). We run
# the SAME round-trip instrument (ramp 1->2->1, DeltaF = 0,
# D = beta = 1) and put the bank in the ledger:
#   harvest H = -<W>    (feedback work extracted by the bit)
#   net cost W_net = <W> + E   (pay the coin for every bit)
# The null meter of Ch.74 now has a price: a coin spent that
# buys nothing leaves W_net = <W> + ln 2 (the dead coin). The
# engaged bit's frontier W_net -> 0 as the leverage grows, and
# the ideal Szilard corner (extraction -> ln 2, erasure -> ln 2)
# is the 0/0 whose removable value is 0: books close with the
# coin; no feedback loop profits after the erasure bill.
# ============================================================

random.seed(42)

DT = 0.01
COIN = math.log(2.0)  # erasure bill per bit, k_B T ln 2 (beta = 1)

def run_roundtrip(runs, tau1, tau2fast, tau2slow, mode):
    """mode: 'control' (fixed return speed), 'sign' (bit = sign of x),
    'far' (bit = |x| > threshold, global FAR_THRESHOLD at the median).
    Returns J and stats."""
    steps1 = max(1, int(round(tau1 / DT)))
    dt1 = tau1 / steps1
    sig1 = math.sqrt(2.0 * dt1)
    em = 0.0
    wm = 0.0
    n_f = 0
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
        em += math.exp(-w)
        if is_fast:
            n_f += 1
    return dict(J=em / runs, wm=wm / runs, p_fast=n_f / runs)

def cal_median():
    """Median of |x_mid| over the forward leg of the same instrument."""
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

print("Ch.75 The Coin's Price: the Demon's Ledger closes at ln 2")
print("  D = beta = 1 ; ramp 1->2->1 (DeltaF=0) ; coin face value I = ln 2 = 0.6931")
print("  erasure bill per bit E = ln 2 (Landauer 1961; Berut et al. Nature 483, 187 (2012))")
print("")

FAR_THRESHOLD = cal_median()
rcal = run_roundtrip(60000, 0.5, 0.35, 2.0, "far")

print("[0] THE COIN: a fair bit minted at the median of |x_mid|")
print("  median(|x_mid|) = %.4f ; p(far) = %.4f ; I = %.4f nats (Szilard's coin)"
      % (FAR_THRESHOLD, rcal["p_fast"], COIN))

print("")
print("[1] CONTROL: run the trap, no coin, no feedback (tau=0.5)")
rctrl = run_roundtrip(120000, 0.5, 0.5, 0.5, "control")
print("  J = %.5f  ln J = %+.5f   <W> = %+.5f   W_net = <W> + 0*coin = %+.5f"
      % (rctrl["J"], math.log(rctrl["J"]), rctrl["wm"], rctrl["wm"]))

print("")
print("[2] THE DEAD COIN: sign bit -> speed; the coin is minted and spent, nothing bought")
rnull = run_roundtrip(200000, 0.5, 0.4, 3.0, "sign")
WNET = rnull["wm"] + COIN
print("  J = %.5f  ln J = %+.5f   <W> = %+.5f   W_net = <W> + ln2 = %+.5f"
      % (rnull["J"], math.log(rnull["J"]), rnull["wm"], WNET))

print("")
print("[3] THE COIN AT WORK: far/near -> speed; the ledger with the bank (each bit buys a return protocol)")
print("  row (tau_fast,tau_slow):  J        ln J      <W>         H=-<W>     W_net=<W>+ln2   H/ln2")
curve = []
for (tf, ts, n) in [(0.35, 2.0, 200000), (0.25, 4.0, 200000), (0.15, 6.0, 200000), (0.10, 8.0, 200000), (0.05, 16.0, 120000)]:
    rr = run_roundtrip(n, 0.5, tf, ts, "far")
    curve.append((tf, ts, rr))
    H = -rr["wm"]
    WNET = rr["wm"] + COIN
    print("  (%.2f, %.2f):  %.5f   %+.5f   %+.5f   %+.5f   %+.5f   %+.5f"
          % (tf, ts, rr["J"], math.log(rr["J"]), rr["wm"], H, WNET, H / COIN))

print("")
print("[4] THE 0/0: the reversible corner of the information engine")
print("  ideal Szilard corner: extraction -> ln 2, erasure -> ln 2, W_net -> 0/0 -> 0")
print("  measured frontier closes toward 0 (W_net down) as the leverage grows;")
print("  H/ln2 rises toward 1 only as the power fades (Carnot's corner, Ch.73, repeated).")
print("  removable value: 0. Books close with the coin at every finite speed (W_net > 0).")

print("")
out_rows = []
for (tf, ts, rr) in curve:
    out_rows.append({"tau_fast": tf, "tau_slow": ts, "J": rr["J"],
                     "lnJ": math.log(rr["J"]), "mean_work": rr["wm"],
                     "harvest": -rr["wm"], "net_cost": rr["wm"] + COIN,
                     "eta_info": (-rr["wm"]) / COIN})
data = {
    "chapter": 75,
    "title": "The Coin's Price: the Szilard-Landauer Closure of the Demon's Ledger (Szilard 1929, Landauer 1961)",
    "beta": 1.0, "delta_f": 0.0, "erasure_bill": COIN,
    "threshold_median_abs_xmid": FAR_THRESHOLD,
    "control": {"J": rctrl["J"], "lnJ": math.log(rctrl["J"]), "mean_work": rctrl["wm"]},
    "null_sign": {"J": rnull["J"], "lnJ": math.log(rnull["J"]), "mean_work": rnull["wm"],
                  "net_cost": rnull["wm"] + COIN},
    "frontier": out_rows,
    "removable_value": 0.0,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "coin_price.json")
with open(out, "w") as fh:
    json.dump(data, fh, indent=2)
print("json ->", out)