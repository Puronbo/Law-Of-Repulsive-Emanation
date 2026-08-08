"""
bridge_extension.py
===================
Resolve README's open question: "Whether this framework extends beyond 2^n-k
to arbitrary primes is open."

The C7 bridge maps a Mersenne-gap prime p = 2^n - k (k small, odd) to a
geodesic length  L = n*ln2 - ln(k)  and a Selberg eigenvalue
    lambda = 1/4 + L^2.
The claim side-channels "spectral resonances": 6 of the 186 census primes
have lambda within 0.01 of an integer (rate 3.23%).

The bridge extends UNIQUELY to arbitrary primes: every prime p with
2^(n-1) < p < 2^n has exactly one representation p = 2^n - k with
0 < k < 2^(n-1)  (k = 2^n - p).  So define, for every prime,
    L(p) = n*ln2 - ln(2^n - p),   lambda(p) = 1/4 + L(p)^2.
This is the natural generalization of the C7 bridge; the 2^n-k family is the
special case k << 2^n.

Decisions:
  (a) Is the census near-integer rate (6/186 = 3.23%) itself above the
      uniform-fractional null (2 eps = 0.02 for eps=0.01)?  (binomial test)
  (b) Does the extended bridge over ALL primes (up to 10^8, ~5.76M primes)
      show a near-integer rate above the uniform null?
  (c) If (b) is null-ish but the census is elevated, is the elevation due to
      the k-small restriction (large L, where fractional parts can cluster)?
      Test against a magnitude-matched random-prime control and a
      small-k-restricted subpopulation.
  (d) Matched random-integer control: integers with the SAME n-distribution
      as the primes (uniform k = 2^n - m for m uniform in (2^(n-1), 2^n)),
      run through the same bridge.  This isolates whether any elevation is
      prime-specific or is an artifact of the bridge arithmetic on ANY
      integers near powers of two.
  (e) Prime-specific elevation: primes vs (d) at equal sample size (two-
      proportion z-test).

Verdict artifact: ../data/bridge_extension_data.json
"""
import json, math, os
import numpy as np
from scipy.stats import binomtest, chisquare

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

EPS = 0.01


def bridge_lambda(n, k):
    L = n * math.log(2.0) - math.log(k)
    return 0.25 + L * L


def frac_dist_to_int(x):
    f = x - math.floor(x)
    return min(f, 1.0 - f)


def sieve_primes(limit):
    """numpy sieve -> sorted int64 array of primes <= limit."""
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    return np.nonzero(sieve)[0]


def main():
    census = json.load(open(os.path.join(DATA, "googol_census_all_k_c7.json")))
    entries = census["all_entries"]
    n_census = len(entries)                 # 186
    near_census = [e for e in entries if e["near_int"]]
    rate_census = len(near_census) / n_census
    print("=" * 72)
    print("C7 BRIDGE EXTENSION TO ARBITRARY PRIMES")
    print("=" * 72)
    print("census: %d primes 2^n-k < 10^100, n<=%d;  near-integer(%.2f) rate "
          "%.4f (%d/%d)"
          % (n_census, census["n_max"], EPS, rate_census,
             len(near_census), n_census))

    # (a) census vs uniform-null binomial
    bt = binomtest(len(near_census), n_census, 2 * EPS, alternative="greater")
    print("(a) census vs uniform-frac null 0.02: p=%.4f (one-sided binomial)"
          % bt.pvalue)

    # (b) extended bridge over all primes <= 10^8
    LIMIT = 10 ** 8
    primes = sieve_primes(LIMIT)
    ns = np.floor(np.log2(primes.astype(np.float64)) + 1).astype(np.int64)
    kk = (np.left_shift(np.int64(1), ns) - primes.astype(np.int64)).astype(
        np.float64)
    L_all = ns.astype(np.float64) * math.log(2.0) - np.log(kk)
    lam_all = 0.25 + L_all * L_all
    dist = np.minimum(lam_all - np.floor(lam_all), 1.0 - (lam_all - np.floor(lam_all)))
    near = dist < EPS
    n_all = int(primes.size)
    n_near_all = int(near.sum())
    rate_all = n_near_all / n_all
    bt_all = binomtest(n_near_all, n_all, 2 * EPS, alternative="greater")
    print("(b) extended bridge, all primes <= 1e8 (N=%d): near-integer rate "
          "%.5f (%d/%d)  p=%.2f vs uniform null 0.02"
          % (n_all, rate_all, n_near_all, n_all, bt_all.pvalue))

    # histogram of fractional distances vs uniform expectation
    fracs = lam_all - np.floor(lam_all)
    hist, _ = np.histogram(fracs, bins=10, range=(0, 1))
    exp = np.full(10, n_all / 10.0)
    chi2, chi2p = chisquare(hist, exp)
    print("    frac(lambda) uniformity: chi2=%.1f p=%.3f over 10 bins"
          % (chi2, chi2p))

    # (c) the 2^n-k special population: k small (k < 30), the census rule.
    #     extended-bridge primes with k < 30 (i.e. within 30 below a power
    #     of two) restricted to n <= 332: compare to census rate.
    smallk = kk < 30
    n_lo = 2
    n_hi = 332
    in_range = (ns >= n_lo) & (ns <= n_hi)
    sel = smallk & in_range
    n_sel = int(sel.sum())
    near_sel = int((dist[sel] < EPS).sum())
    rate_sel = near_sel / n_sel if n_sel else 0.0
    bt_sel = binomtest(near_sel, n_sel, 2 * EPS, alternative="greater") if n_sel else None
    print("(c) k<30, 2<=n<=332 subset of extended bridge (N=%d): near-int "
          "rate %.4f (%d/%d)  p=%.3f"
          % (n_sel, rate_sel, near_sel, n_sel,
             bt_sel.pvalue if bt_sel else float("nan")))

    # (d) k-small restriction is what the census used: rate over all primes
    #     with k < 30 (any n up to 27, since 2^27 ~ 1.3e8; n<=26 keeps below
    #     the limit for all k<30).
    sel2 = kk < 30
    n_sel2 = int(sel2.sum())
    near_sel2 = int((dist[sel2] < EPS).sum())
    rate_sel2 = near_sel2 / n_sel2 if n_sel2 else 0.0
    bt_sel2 = binomtest(near_sel2, n_sel2, 2 * EPS, alternative="greater") if n_sel2 else None
    print("(d) k<30, any n<=26 (N=%d): near-int rate %.4f (%d/%d)  p=%.3f"
          % (n_sel2, rate_sel2, near_sel2, n_sel2,
             bt_sel2.pvalue if bt_sel2 else float("nan")))

    # (d) matched random-integer control (uniform k in each n-bin)
    counts = np.bincount(ns, minlength=int(ns.max()) + 1)
    rng = np.random.default_rng(42)
    kk_c = np.empty(0)
    ns_c = np.empty(0, dtype=np.int64)
    for n in range(2, len(counts)):
        c = int(counts[n])
        if c == 0:
            continue
        ns_c = np.concatenate([ns_c, np.full(c, n, dtype=np.int64)])
        kk_c = np.concatenate([kk_c, rng.integers(1, 2 ** (n - 1), size=c)])
    kk_c = kk_c.astype(np.float64)
    L_c = ns_c.astype(np.float64) * math.log(2.0) - np.log(kk_c)
    lam_c = 0.25 + L_c * L_c
    dist_c = np.minimum(lam_c - np.floor(lam_c), 1.0 - (lam_c - np.floor(lam_c)))
    near_c = dist_c < EPS
    n_c_ctrl = int(ns_c.size)
    n_near_c = int(near_c.sum())
    rate_c = n_near_c / n_c_ctrl
    print("(d) matched random-integer control (N=%d): near-int rate %.5f "
          "(%d/%d)" % (n_c_ctrl, rate_c, n_near_c, n_c_ctrl))

    # (e) two-proportion z-test: primes vs random-integer control
    p1, p2 = rate_all, rate_c
    se = math.sqrt(p1 * (1 - p1) / n_all + p2 * (1 - p2) / n_c_ctrl)
    z = (p1 - p2) / se
    from scipy.stats import norm as _norm
    p_elev = float(_norm.sf(abs(z)) * 2)
    print("(e) primes vs random-int control: z=%.1f  p=%.3g  (elevation %.5f)"
          % (z, p_elev, p1 - p2))

    # verdict logic: uniform-null rate is 0.02; both tails count, so the
    # expected near-integer fraction under uniformity is exactly 0.02.
    sig = 0.01
    census_elevated = bt.pvalue < sig
    ext_elevated = bt_all.pvalue < sig
    prime_specific = p_elev < sig
    if not census_elevated and not ext_elevated:
        core = ("NEUTRAL-NULL: neither the census (6/186, p=%.3f) nor the "
                "extended bridge over %.1fM primes (%.5f, p=%.2f) rises above "
                "the 0.02 uniform-fractional null at alpha=%.2f. The "
                "'6 spectral resonances' are the expected ~3.7 under "
                "uniformity, not structure.")
        core = core % (bt.pvalue, n_all / 1e6, rate_all, bt_all.pvalue, sig)
    elif census_elevated and not ext_elevated:
        core = ("CENSUS-ONLY ELEVATION: the 2^n-k census sits above the null "
                "(p=%.3f) but the extended bridge over %.1fM arbitrary "
                "primes is null (%.5f, p=%.2f). The resonance is an artifact "
                "of the k<30 restriction (the (c)/(d) subsets test this) or "
                "of the tiny n=186 sample, NOT a property of primes in "
                "general -- the framework does not extend.")
        core = core % (bt.pvalue, n_all / 1e6, rate_all, bt_all.pvalue)
    elif not census_elevated and ext_elevated:
        if prime_specific:
            core = ("EXTENDED ELEVATION, PRIME-SPECIFIC (census p=%.3f, ext "
                    "%.5f, primes-vs-random p=%.3g): the near-integer "
                    "resonance is generic across primes at a small elevation "
                    "ABOVE the bridge-on-any-integer baseline. The framework "
                    "trivially extends -- every prime p has the unique "
                    "representation p = 2^n - k -- but the effect is not "
                    "special to the 2^n-k family; it is the bridge arithmetic "
                    "plus a small prime residue bias.")
            core = core % (bt.pvalue, rate_all, p_elev)
        else:
            core = ("EXTENDED ELEVATION, NOT PRIME-SPECIFIC (census p=%.3f, "
                    "ext %.5f, primes-vs-random p=%.2f): the near-integer "
                    "rate is an artifact of the bridge formula applied to "
                    "ANY integer near a power of two, reproduced at the same "
                    "rate by a matched random-integer control. The framework "
                    "extends trivially but carries no prime content.")
            core = core % (bt.pvalue, rate_all, p_elev)
    else:
        core = ("BOTH ELEVATED: near-integer resonance is generic across "
                "primes (census p=%.3f, extended p=%.2f) -- the framework "
                "extends but loses its distinctive 2^n-k content.")
        core = core % (bt.pvalue, bt_all.pvalue)

    verdict = core
    print("\nverdict:", verdict)

    out = {
        "claim": ("README/T19: 'whether this framework extends beyond 2^n-k "
                  "to arbitrary primes is open' -- C7 bridge, generalized by "
                  "the unique p = 2^n - k representation of every prime"),
        "setup": {"eps": EPS, "prime_limit": LIMIT, "census_n": n_census,
                  "census_near_int": len(near_census)},
        "census": {"near_int_rate": round(rate_census, 5),
                   "binom_p_gt_uniform": float(bt.pvalue),
                   "uniform_null_rate": 2 * EPS,
                   "expected_near_int_under_null": 2 * EPS * n_census},
        "extended": {"n_primes": n_all, "near_int_rate": round(rate_all, 6),
                     "n_near_int": n_near_all,
                     "binom_p_gt_uniform": float(bt_all.pvalue),
                     "frac_uniform_chi2": round(float(chi2), 2),
                     "frac_uniform_p": round(float(chi2p), 4)},
        "subsets": {
            "k_lt_30_n_2_332": {"n": n_sel, "near": near_sel,
                                "rate": round(rate_sel, 5),
                                "binom_p": float(bt_sel.pvalue) if bt_sel else None},
            "k_lt_30_any_n": {"n": n_sel2, "near": near_sel2,
                              "rate": round(rate_sel2, 5),
                              "binom_p": float(bt_sel2.pvalue) if bt_sel2 else None},
        },
        "random_integer_control": {"n": n_c_ctrl, "near_int_rate": round(rate_c, 6),
                                   "n_near_int": n_near_c},
        "prime_vs_random": {"z": round(z, 2), "p": round(p_elev, 4),
                            "elevation": round(p1 - p2, 6),
                            "prime_specific": bool(prime_specific)},
        "verdict": verdict,
    }
    with open(os.path.join(DATA, "bridge_extension_data.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote data/bridge_extension_data.json")


if __name__ == "__main__":
    main()
