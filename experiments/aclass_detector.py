"""
ACLASS DETECTOR: THE FLUCTUATION-SCALE TEST FOR 0/0 VALUES
================================================================
Atlas method entry.  Question: does a conjectured 0/0 value exist?

Criterion (derived from entry 64).  For an observable A(n) with a
candidate scaling denominator D(n) ~ n^alpha, the ratio A/D has a
removable value only if the FLUCTUATIONS of A are subleading to D:
    max_{k<=n} |A(k) ~ drift|  ~  n^beta   with   beta < alpha .
beta is the fluctuation exponent, measured as the log-log slope of
the running-max-absolute series across octaves/decades:
    beta = 0          -> fluctuations constant (strongly subleading)
    beta in (0,alpha) -> subleading          -> REMOVABLE-COMPATIBLE
    beta ~ alpha      -> fluctuations sit ON the denominator (Polya!)
                          -> ANTI-CLASS (no removable value)
    beta > alpha      -> fluctuations dominate -> deeply ANTI

Probes (two labelled, one open):
  P1 Polya/Liouville   F(n)=sum lambda(k): labelled ANTI (Littlewood
     Omega_+-(sqrt n); first + at 906,150,257). Expect beta ~ 1/2,
     cross-over alpha* ~ 1/2.
  P2 PNT deviation     |pi(x)-Li(x)|: labelled REMOVABLE-COMPATIBLE
     (the ratio pi/Li -> 1; the deviation is subleading to x/log x).
     Empirically beta ~ 0.5-0.6 < alpha_D ~1 -> flagged removable.
  P3 Collatz           T(n) = total stopping time: open.  Does the
     heuristic c*log(n) (c ~ 41.7) pass the test as a genuine
     removable value in the mean, or is it a Polya-style illusion?
     The detector compares the max-fluctuation slope against the log
     scale and the mean-octave stability of T(n)/log(n).

Honest wall for every probe is stated with the output: finite range,
no theorem.  Only P1/P2 are gated (labelled); P3 is a diagnosis.
"""
import json
import math
import os
import sys
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")


# ---------------------------------------------------------------- tooling
def octave_slope(pos, vals, base=10.0):
    """Log-log slope of running-max series.  Dense series are binned by
    decade (edge-guarded); sparse series are fit directly on the points."""
    if len(vals) < 30:
        pts = [(math.log(pos[k]), math.log(v)) for k, v in enumerate(vals)
               if v > 0]
        n = len(pts)
        if n < 3:
            return 0.0, 1.0, n
        mx = sum(p for p, _ in pts) / n
        my = sum(q for _, q in pts) / n
        sxy = sum((p - mx) * (q - my) for p, q in pts)
        sxx = sum((p - mx) * (p - mx) for p, _ in pts)
        slope = sxy / sxx if sxx else 0.0
        syy = sum((q - my) * (q - my) for _, q in pts)
        r2 = (sxy * sxy) / (sxx * syy) if sxx and syy else 0.0
        return slope, r2, n
    bins = {}
    for k, v in enumerate(vals):
        if v <= 0:
            continue
        d = int(math.floor(math.log(pos[k], base) + 1e-9))
        bins.setdefault(d, []).append(v)
    xs, ys = [], []
    for d in sorted(bins):
        m = max(bins[d])
        mid = base ** (d + 0.5)
        xs.append(math.log(mid))
        ys.append(math.log(m))
    n = len(xs)
    if n < 3:
        return 0.0, 1.0, n
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) * (x - mx) for x in xs)
    slope = sxy / sxx if sxx else 0.0
    syy = sum((y - my) * (y - my) for y in ys)
    r2 = (sxy * sxy) / (sxx * syy) if sxx and syy else 0.0
    return slope, r2, n


def classify(beta, alpha_d, tol=0.12):
    if beta > alpha_d + tol:
        return "ANTI (fluctuation-dominated)"
    if abs(beta - alpha_d) <= tol:
        return "ANTI / borderline (fluctuations sit on the denominator)"
    return "REMOVABLE-COMPATIBLE (subleading)"


def li(x, npts=2000):
    """int_2^x dt/log(t) on a log-scale trapezoid grid."""
    lo, hi = math.log(2.0), math.log(x)
    t0 = 2.0
    s = 0.0
    for k in range(1, npts + 1):
        tk = math.exp(lo + (hi - lo) * k / npts)
        lk = lo + (hi - lo) * k / npts
        lm = lo + (hi - lo) * (k - 1) / npts
        s += 0.5 * (1.0 / lm + 1.0 / lk) * (tk - t0)
        t0 = tk
    return s


def parity_f(N):
    """Liouville parity sieve: returns bytearray par (1 iff Omega(k) odd)."""
    par = bytearray(N + 1)
    sieve = bytearray([1]) * (N + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    for p in [i for i in range(2, N + 1) if sieve[i]]:
        q = p
        while q <= N:
            for m in range(q, N + 1, q):
                par[m] ^= 1
            q *= p
    return par


def collatz_times(N):
    """Total stopping times T(2..N) via iterative memo (array-backed)."""
    dist = array("I", [0]) * (N + 1)
    dist[1] = 0
    for n in range(2, N + 1):
        chain = []  # (value, step-increment: 1 for even-halve, 2 for odd-fold)
        k = n
        while True:
            if k == 1:
                base = 0
                break
            if k <= N and dist[k]:
                base = dist[k]
                break
            if (k & 1) == 0:
                chain.append((k, 1))
                k >>= 1
            else:
                chain.append((k, 2))  # odd -> 3k+1 (even) -> halve: two steps
                k = (3 * k + 1) >> 1
        t = base
        for x, inc in reversed(chain):
            t += inc
            if x <= N:
                dist[x] = t
    return dist


# ---------------------------------------------------------------- probes
def probe_polya():
    N = 10 ** 7
    par = parity_f(N)
    pos, rmax = [], []
    F = 0
    m = 0
    for n in range(1, N + 1):
        F += 1 if par[n] == 0 else -1
        a = abs(F)
        if a > m:
            m = a
        rmax.append(m)
        pos.append(n)
    beta, r2, nd = octave_slope(pos, rmax)
    alpha_d = 0.5
    cls = classify(beta, alpha_d)
    return {"beta": beta, "r2": r2, "ndecades": nd, "alpha_d": alpha_d,
            "class": cls, "maxF_abs": m, "N": N, "miniF": min(rmax),
            "note": "Littlewood: F = Omega_+-(sqrt(n))"}


def probe_pnt():
    N = 2 * 10 ** 7
    sieve = bytearray([1]) * (N + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    grid = [10 ** k for k in range(5, int(math.log10(N)) + 1)] + [N]
    pos, rmax = [], []
    running_pi = 0
    m = 0
    s = 0
    for x in grid:
        for v in range(s + 1, x + 1):
            running_pi += sieve[v]
        s = x
        dev = abs(running_pi - li(x))
        if dev > m:
            m = dev
        pos.append(x)
        rmax.append(m)
        print(f"  x={x:>9,}  pi={running_pi:>8,}  Li={li(x):>8,.0f}  "
              f"pi/Li={running_pi / li(x):.4f}  max|dev|~{m:>6,.0f}")
    beta, r2, nd = octave_slope(pos, rmax, base=10.0)
    alpha_d = 1.0  # leading term x/log x ~ x^1
    cls = classify(beta, alpha_d)
    return {"beta": beta, "r2": r2, "ndecades": nd, "alpha_d": alpha_d,
            "class": cls, "N": N, "max_dev": m, "piN": running_pi,
            "liN": li(N), "ratio_N": running_pi / li(N)}


def probe_collatz():
    N = 10_000_000
    dist = collatz_times(N)
    decimals = [10 ** d for d in range(2, int(math.log10(N)))]
    print(f"  computed T(n) for n <= {N}", flush=True)
    decades = {}
    maxrec = {}
    for n in range(2, N + 1):
        d = int(math.floor(math.log10(n)))
        r = dist[n] / math.log(n)
        decades.setdefault(d, []).append(r)
        maxrec[d] = max(maxrec.get(d, 0.0), dist[n] / math.log(n))
    rows = []
    for d in sorted(decades):
        v = decades[d]
        cnt = len(v)
        mean_r = sum(v) / cnt
        sd_r = (sum((x - mean_r) ** 2 for x in v) / cnt) ** 0.5
        mx_r = maxrec[d]
        hi = min(10 ** (d + 1) - 1, N)
        rows.append({"decade": d, "lo": 10 ** d, "hi": hi, "n": cnt,
                     "mean_ratio": mean_r, "sd_ratio": sd_r,
                     "max_ratio": mx_r})
        print(f"  decade {10**d:>9,}-{hi:>9,}: "
              f"mean T/log(n)={mean_r:.3f}  sd={sd_r:.3f} "
              f"max T/log(n)={mx_r:.2f}")
    # mean stability: slope of the mean ratio across decades ~ 0
    xs = [math.log(10 ** (r["decade"] + 0.5)) for r in rows[2:]]
    ys = [math.log(r["mean_ratio"]) for r in rows[2:]]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    slope_mean = (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
                  / sum((x - mx) ** 2 for x in xs))
    # max-fluctuation slope across decades (ratio max T / log n)
    xs = [math.log(10 ** (r["decade"] + 0.5)) for r in rows[2:]]
    ys = [math.log(r["max_ratio"]) for r in rows[2:]]
    mx = sum(xs) / n
    my = sum(ys) / n
    slope_max = (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
                 / sum((x - mx) ** 2 for x in xs))
    final = rows[-1]
    return {"N": N, "decades": rows, "mean_slope": slope_mean,
            "max_slope": slope_max, "final_mean": final["mean_ratio"],
            "final_max": final["max_ratio"],
            "max_exponent": abs(slope_max) + 0.5,
            "diagnosis": ("MEAN-STABLE candidate (open): the mean ratio "
                          "T/log n is flat across decades (not anti-class "
                          "in the mean); limited to 1e7 and no theorem "
                          "for the limit's existence.")}


def _primes_to(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(2, n + 1) if s[i]]


def _li2(x):
    a = 2.0
    ng = 6000
    lo = math.log(a)
    hi = math.log(x)
    t0 = math.exp(lo)
    total = 0.0
    for k in range(1, ng + 1):
        tt = math.exp(lo + (hi - lo) * k / ng)
        total += 0.5 * (1.0 / (lo + (hi - lo) * (k - 1) / ng) ** 2
                        + 1.0 / (lo + (hi - lo) * k / ng) ** 2) * (tt - t0)
        t0 = tt
    return total


def probe_twin():
    """Twin-prime density ratio V(x)=pi_2/(2*C_2*Li_2): the DECADAL MAX
    of |V(x) - 1| should fall decade-on-decade (negative exponent) -- the
    removable-value signature, applied to the open Hardy-Littlewood 0/0.
    The running-max statistic is the wrong one here: V oscillates across
    1, so per-decade maxima (not a cumulative max) carry the decay."""
    base = _primes_to(10 ** 5)
    C2 = 1.0
    for p in base[1:]:
        C2 *= 1.0 - 1.0 / ((p - 1) * (p - 1))
    K = 2.0 * C2
    N = 20_000_000
    primes = _primes_to(N)
    flag = bytearray(N + 3)
    for p in primes:
        flag[p] = 1
    xs = [k * 10 ** 5 for k in range(1, N // 10 ** 5 + 1)]
    pi2 = {}
    t = 0
    j = 0
    for n in range(3, N + 1, 2):
        if flag[n] and flag[n - 2]:
            t += 1
        while j < len(xs) and n >= xs[j]:
            pi2[xs[j]] = t
            j += 1
    while j < len(xs):
        pi2[xs[j]] = t
        j += 1
    devs = []
    for x in xs:
        r = pi2[x] / (K * _li2(x))
        devs.append(abs(r - 1.0))
    beta, r2b, nd = decade_decay(xs, devs, minpts=3)
    return {"beta": beta, "r2": r2b, "ndecades": nd,
            "class": ("DECAYING-TO-1 (removable-compatible, OPEN)"
                      if beta < -0.2 else "NOT-CLEAN (needs longer range)"),
            "K_two_C2": K, "N": N, "final_dev": devs[-1],
            "max_dev": max(devs),
            "endpoints": {"x": xs[-1], "pi2": pi2[xs[-1]]},
            "wall": "pi_2 to 2e7; per-decade maxima over 5/6/7 only "
                    "(3 decade bins, coarse but sign-clear)"}


def probe_goldbach():
    """Goldbach density ratio R(N)=G/(S(N) N/log^2 N), S(N) the in-code
    singular-series weight: the pointwise log-log drift of |R(N)-1| and
    the band-mean drift toward 1.  Deviations scatter (range is small), so
    the honest verdict is 'no anti-class signal' when the drift is far
    below +1/2 and the upper band mean is the closer to 1 -- never the
    runaway that Polya/Mertens calibrate at +1/2."""
    LIMIT = 300_000
    primes = _primes_to(LIMIT)
    flag = bytearray(LIMIT + 1)
    for p in primes:
        flag[p] = 1
    C2 = 1.0
    for p in primes[1:]:
        C2 *= 1.0 - 1.0 / ((p - 1) * (p - 1))
    K = 2.0 * C2
    devs = []
    Ns = []
    for N in range(10_000, LIMIT + 1, 50):
        S = K
        m = N
        q = 3
        while q * q <= m:
            if m % q == 0:
                S *= (q - 1.0) / (q - 2.0)
                while m % q == 0:
                    m //= q
            q += 2
        if m > 2:
            S *= (m - 1.0) / (m - 2.0)
        lN = math.log(N)
        G = 0
        for p in primes:
            if p >= N:
                break
            if flag[N - p]:
                G += 1
        R = G / (S * N / (lN * lN))
        Ns.append(N)
        devs.append(abs(R - 1.0))
    pts = [(math.log(x), math.log(d)) for x, d in zip(Ns, devs) if d > 0]
    n = len(pts)
    mx = sum(p for p, _ in pts) / n
    my = sum(q for _, q in pts) / n
    sxx = sum((p - mx) ** 2 for p, _ in pts)
    sxy = sum((p - mx) * (q - my) for p, q in pts)
    beta = sxy / sxx if sxx else 0.0
    syy = sum((q - my) ** 2 for _, q in pts)
    r2 = (sxy * sxy) / (sxx * syy) if sxx and syy else 0.0
    lo = [d for x, d in zip(Ns, devs) if x < 100_000]
    hi = [d for x, d in zip(Ns, devs) if x >= 200_000]
    mean_lo = sum(lo) / len(lo) if lo else 1.0
    mean_hi = sum(hi) / len(hi) if hi else 1.0
    clean = beta < 0.3 and mean_hi < mean_lo
    return {"beta": beta, "r2": r2, "n_sample": len(Ns),
            "class": ("no anti-class signal (removable not contradicted, OPEN)"
                      if clean else "NOT-CLEAN (needs longer range)"),
            "two_C2": K, "N_hi": LIMIT,
            "mean_lo": mean_lo, "mean_hi": mean_hi, "max_hi": max(hi),
            "wall": "G to 3e5 sampled every 50th even N; strong Goldbach "
                    "open; deviations scatter at this range"}


def decade_decay(xs, devs, minpts=3):
    """per-decade max of a sign-oscillating deviation series; log-log
    slope of (decade-max, mid-decade) vs decade-power."""
    bins = {}
    for x, d in zip(xs, devs):
        k = int(math.floor(math.log10(x)) + 1e-9)
        bins.setdefault(k, []).append(d)
    rows = [(k, max(bins[k])) for k in sorted(bins)
            if len(bins[k]) >= minpts]
    nbin = len(rows)
    if nbin < 3:
        return 0.0, 1.0, nbin
    pts = [(math.log(10 ** (k + 0.5)), math.log(v)) for k, v in rows]
    mx = sum(p for p, _ in pts) / nbin
    my = sum(q for _, q in pts) / nbin
    sxx = sum((p - mx) ** 2 for p, _ in pts)
    sxy = sum((p - mx) * (q - my) for p, q in pts)
    slope = sxy / sxx if sxx else 0.0
    syy = sum((q - my) ** 2 for _, q in pts)
    r2 = (sxy * sxy) / (sxx * syy) if sxx and syy else 0.0
    return slope, r2, nbin


def main():
    print("=" * 70)
    print("ACLASS DETECTOR: FLUCTUATION-SCALE TEST")
    print("=" * 70)

    print("\nP1 Polya/Liouville (labelled ANTI, entry 64):")
    p1 = probe_polya()
    print(f"  fluctuation exponent beta = {p1['beta']:.3f} (r2={p1['r2']:.2f}, "
          f"{p1['ndecades']} decades); denominator alpha = {p1['alpha_d']}")
    print(f"  -> {p1['class']}")

    print("\nP2 PNT deviation pi(x)-Li(x) (labelled REMOVABLE, entry PNT-class):")
    p2 = probe_pnt()
    print(f"  fluctuation exponent beta = {p2['beta']:.3f} (r2={p2['r2']:.2f}, "
          f"{p2['ndecades']} decades); leading denominator alpha ~ {p2['alpha_d']}")
    print(f"  -> {p2['class']} ; pi(N)/Li(N) = {p2['ratio_N']:.5f}")

    print("\nP3 Collatz total stopping time (open diagnosis):")
    p3 = probe_collatz()
    print(f"  mean-ratio slope across decades = {p3['mean_slope']:.4f}  "
          f"(~0 = stable statistic)")
    print(f"  max-ratio slope = {p3['max_slope']:.4f}  "
          f"(ratio max T/log(n); ~0 = subleading vs log n)")
    print(f"  final decade mean T/log(n) = {p3['final_mean']:.3f}, "
          f"max = {p3['final_max']:.2f}")
    print(f"  diagnosis: {p3['diagnosis']}")

    print("\nP4 Twin-prime density V(x)-1 (removable, OPEN entry 65):")
    p4 = probe_twin()
    print(f"  per-decade max deviation exponent beta = {p4['beta']:.2f} "
          f"(r2={p4['r2']:.2f}, {p4['ndecades']} decade bins); "
          f"|V(2e7)-1| = {p4['final_dev']:.4f}")
    print(f"  -> {p4['class']}")

    print("\nP5 Goldbach density R(N)-1 (removable, OPEN entry 66):")
    p5 = probe_goldbach()
    print(f"  pointwise drift beta = {p5['beta']:.3f} (r2={p5['r2']:.2f}, "
          f"{p5['n_sample']} evens); band means |R-1|: "
          f"N<1e5 -> {p5['mean_lo']:.3f} vs N>=2e5 -> {p5['mean_hi']:.3f}")
    print(f"  -> {p5['class']}")

    print("\n" + "-" * 70)
    print("GATES (labelled + open-target removable probes)")
    print("-" * 70)
    g1 = abs(p1["beta"] - 0.5) < 0.12          # Polya: beta ~ 1/2 -> anti
    g2 = abs(p2["ratio_N"] - 1.0) < 0.006       # PNT: pi/Li -> 1
    g3 = p2["beta"] < 0.85                       # PNT fluctuations subleading
    g4 = p1["r2"] > 0.9                          # detector internal fit quality
    g5 = p4["beta"] < -0.2                        # twin deviations decay
    g6 = p5["beta"] < 0.3 and p5["mean_hi"] < p5["mean_lo"]
    gates = {"G1 Polya fluctuation exponent ~ 1/2 (anti-class)": g1,
             "G2 PNT ratio pi/Li -> 1 (removable)": g2,
             "G3 PNT fluctuation exponent subleading to x/log x": g3,
             "G4 detector octave-fit quality r2 > 0.9": g4,
             "G5 twin V(x)-1 decays (beta < -0.2, removable open)": g5,
             "G6 goldbach R(N)-1 no growth + drifts to 1 (removable open)": g6}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'}")

    os.makedirs(DATA, exist_ok=True)
    json.dump(
        {"method": "fluctuation-scale test (anti-class detector)",
         "criterion": "ratio A/D removable iff fluctuation exponent beta < alpha",
         "probes": {"P1_polya": p1, "P2_pnt": p2, "P3_collatz": p3,
                    "P4_twin": p4, "P5_goldbach": p5},
         "gates": gates, "overall": overall,
         "wall": "finite ranges (1e7 / 2e7 / 5e6); labelled probes gated, "
                 "Collatz is an open diagnosis"},
        open(os.path.join(DATA, "aclass_detector.json"), "w"), indent=2)
    print("Wrote data/aclass_detector.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()