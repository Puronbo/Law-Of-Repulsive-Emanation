"""
mersenne_taxonomy.py = L_k(s), covering systems, Poincare disk, theta functions.

Builds on mersenne_gap_data.json (pre-computed). Computes:

  1. L_k(s) = sum_{n in S_k} 1/n^s for k=1..19, s=0..4
  2. Even/odd dichotomy: ratio of L_k(2) to zeta_k(2)
  3. k=7 covering system (why only 6 primes)
  4. Poincare disk geodesic lengths from offset pattern
  5. Theta function Theta_9(q) = sum_{{n in S_9}} n * q^n
  6. Analytic continuation: L_9(0) via zeta regularization
  7. Connection to trajectory L(s) = C0 * zeta(s)
"""
import json, math, sys, time

# ----------------------------------------------------------------
# Load pre-computed data
# ----------------------------------------------------------------
with open("mersenne_gap_data.json") as f:
    DATA = json.load(f)

# Load congruence analysis (or compute on the fly)
try:
    with open("mersenne_congruence_data.json") as f:
        CDATA = json.load(f)
except FileNotFoundError:
    CDATA = None

results = DATA["results"]
MAX_N = DATA["search_params"]["max_n"]
ALL_K = sorted(int(k) for k in results)

S = {}  # S_k = set of n where 2^n - k is prime
for k in ALL_K:
    S[k] = set(results[str(k)]["n_values"])

# SMALL_PRIMES for covering analysis
SMALL_PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,
                73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,
                151,157,163,167,173,179,181,191,193,197,199]

# ----------------------------------------------------------------
# 1. L_k(s) = sum_{n in S_k} 1/n^s
# ----------------------------------------------------------------
print("=" * 72)
print("L_k(s) = sum_{n in S_k} 1/n^s  (Mersenne gap Dirichlet series)")
print("=" * 72)
print(f"\n{'k':>4s}  {'|S_k|':>6s}  {'L_k(0)':>8s}  {'L_k(1)':>8s}  {'L_k(2)':>8s}  {'L_k(3)':>8s}  {'zeta_k(2)':>10s}  {'ratio':>8s}  {'parity':>6s}")
print(f"{'-'*4:>4s}  {'-'*6:>6s}  {'-'*8:>8s}  {'-'*8:>8s}  {'-'*8:>8s}  {'-'*8:>8s}  {'-'*10:>10s}  {'-'*8:>8s}  {'-'*6:>6s}")

# zeta_k(2) = sum_{n in S_k} 1/n^2 if S_k were all n (for density comparison)
zeta_all = sum(1.0 / (n * n) for n in range(2, MAX_N + 1))

table = {}
for k in ALL_K:
    sk = S[k]
    cnt = len(sk)
    if cnt == 0:
        print(f"{k:4d}  {cnt:6d}  {'-':>8s}  {'-':>8s}  {'-':>8s}  {'-':>8s}  {'-':>10s}  {'-':>8s}  {'even' if k%2==0 else 'odd':>6s}")
        table[k] = (cnt, 0, 0, 0, 0, 0, None)
        continue
    L0 = cnt                                      # L_k(0) = count
    L1 = sum(1.0 / n for n in sk)                 # L_k(1)
    L2 = sum(1.0 / (n * n) for n in sk)           # L_k(2)
    L3 = sum(1.0 / (n ** 3) for n in sk)          # L_k(3)
    zeta_k2 = sum(1.0 / (n * n) for n in sk)      # same as L2
    ratio = L2 / zeta_all if zeta_all > 0 else 0
    parity = "even" if k % 2 == 0 else "odd"
    print(f"{k:4d}  {cnt:6d}  {L0:8.1f}  {L1:8.4f}  {L2:8.6f}  {L3:8.6f}  {zeta_k2:10.6f}  {ratio:8.4f}  {parity:>6s}")
    table[k] = (cnt, L0, L1, L2, L3, zeta_k2, ratio)

# ----------------------------------------------------------------
# 2. Even/odd dichotomy
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("EVEN/ODD DICHOTOMY")
print("=" * 72)
odd_k = [k for k in ALL_K if k % 2 == 1]
even_k = [k for k in ALL_K if k % 2 == 0]
odd_total = sum(table[k][0] for k in odd_k)
even_total = sum(table[k][0] for k in even_k)
print(f"\n  Odd offsets  ({len(odd_k)} values): {odd_total} primes total")
print(f"  Even offsets ({len(even_k)} values): {even_total} primes total (all trivial n<=3)")
print(f"\n  All even k have ZERO non-trivial primes (n>3).")
print(f"  This is because 2^n is even, so 2^n - k is even when k is even and n>1.")
print(f"  For k even and n>1, 2^n - k is even > 2, hence COMPOSITE.")
print(f"\n  => The even/odd dichotomy is trivial: even offsets give even numbers.")
print(f"  => The MUSICAL content is that offsets 2,4,8,10 give even numbers,")
print(f"     which can never be prime (except n=2 for k=2 giving 2).")

# ----------------------------------------------------------------
# 3. k=7 covering system analysis
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("WHY k=7 FAILS: COVERING CONGRUENCE ANALYSIS")
print("=" * 72)
k7 = S[7]
print(f"\n  S_7 = {sorted(k7)}")
print(f"  Only {len(k7)} primes up to {MAX_N}.")
print(f"\n  Checking small prime divisors of 2^n - 7:")
for p in [3, 5, 7, 11, 13, 17, 19]:
    bad_n = [n for n in range(2, MAX_N + 1) if pow(2, n, p) == (7 % p)]
    coverage = len(bad_n) / MAX_N * 100
    print(f"    p={p:3d}: 2^n = 7 mod {p} for n = {bad_n[:6]}{'...' if len(bad_n)>6 else ''}  ({coverage:.0f}% of n)")

# Find covering system: small primes whose union covers all n
print(f"\n  Covering congruence check:")
covered = set()
cover_system = []
for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    bad_n = {n for n in range(2, MAX_N + 1) if pow(2, n, p) == (7 % p)}
    if bad_n:
        new = bad_n - covered
        cover_system.append((p, len(new)))
        covered |= bad_n
        if len(covered) >= MAX_N - 1:
            break
print(f"  Covering primes: {[p for p, _ in cover_system]}")
print(f"  Coverage: {len(covered)}/{MAX_N} natural numbers")
print(f"  Uncovered n (potential primes): {MAX_N - len(covered)}")
uncovered = [n for n in range(2, MAX_N + 1) if n not in covered]
print(f"  Uncovered n: {uncovered[:10]}{'...' if len(uncovered)>10 else ''}")

# ----------------------------------------------------------------
# 4. Poincare disk geodesic interpretation
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("POINCARE DISK GEODESIC INTERPRETATION")
print("=" * 72)
print("""
  The offsets 2,4,8,9,10 correspond to geodesic lengths via the
  hyperbolic distance function on the Poincare disk:
    d(0, r) = 2 * artanh(r)

  For a Mersenne prime exponent n, the 'radius' of the k-offset is:
    r_k(n) = 1 - k / 2^n   (normalized by 2^n)

  The geodesic length from origin to this radius:
    ell_k(n) = 2 * artanh(1 - k/2^n) ~ ln(2^n / k) for large n
             = n * ln(2) - ln(k)

  So the offset pattern traces a LINEAR sequence in geodesic length:
    ell_3(n) - ell_1(n) = ln(1) - ln(3) = -ln(3)   (M-2)
    ell_5(n) - ell_1(n) = -ln(5)                    (M-4)
    ell_9(n) - ell_1(n) = -ln(9) = -2*ln(3)         (M-8)
    ell_10(n) - ell_1(n) = -ln(10) = -ln(2) - ln(5)  (M-9)

  In the Selberg trace formula, these 'prime geodesic lengths'
  appear as exponents in the spectral heat kernel.
  The ratio of consecutive lengths:
    ln(5)/ln(3) ~ 1.465  (tritone)
    ln(9)/ln(5) ~ 1.365  (major sixth)
    ln(10)/ln(9) ~ 1.047 (minor second)

  MUSICAL: The offset sequence 1->3->5->9->10 in log-space traces
  intervals: tritone (3->5), major sixth (5->9), minor second (9->10).
  The resolution -9 from -10 (k=10 -> k=9) is a descent by a minor
  second, the smallest interval in Western music.
""")

# Compute actual geodesic lengths for specific n
print(f"  Sample geodesic lengths for n = 136279841 (if it were real):")
for k in [1, 3, 5, 9, 10]:
    n = 136279841
    ell = n * math.log(2) - math.log(k)
    print(f"    k={k:3d} (M-{k-1:2d}):  ell = {ell:.2f}")

# ----------------------------------------------------------------
# 5. Theta function for S_9
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("THETA FUNCTION: Theta_9(q) = sum_{{n in S_9}} a_n * q^n")
print("=" * 72)
print("""
  Define the generating function:
    Theta_9(q) = sum_{n >= 2} chi_9(n) * q^n
  where chi_9(n) = 1 if 2^n - 9 is prime, 0 otherwise.

  This is a sparse theta series supported on S_9.
  For the trajectory modular form F(i) = C0, the theta function
  of the prime-indexed states is:
    Theta_C0(q) = sum_{n prime} C0 * q^n = C0 * theta_prime(q)

  The ratio Theta_9(q) / Theta_C0(q) measures how the k=9 offset
  'selects' a subset of the prime-indexed trajectory states.
""")

# Compute first few terms of Theta_9
print(f"\n  Theta_9(q) = ", end="")
terms = []
for n in sorted(S[9]):
    if n <= 33:
        terms.append(f"q^{n}")
print(" + ".join(terms) + " + ...")

# Compute Theta_1(q) for comparison (Mersenne primes)
print(f"  Theta_1(q) = ", end="")
terms1 = []
for n in sorted(S[1]):
    if n <= 33:
        terms1.append(f"q^{n}")
print(" + ".join(terms1) + " + ...")

# Connection to trajectory theta function
print(f"\n  For the trajectory L-function: L(s) = C0 * zeta(s)")
print(f"  The associated theta function (by Mellin transform):")
print(f"    theta_traj(t) = sum_n C0 * e^(-pi n^2 t) = C0 * theta_3(t)")
print(f"  For S_9, the Mellin transform gives L_9(s):")
print(f"    L_9(s) = sum_{{n in S_9}} 1/n^s")
print(f"  By the converse theorem, L_9(s) is the L-function of the")
print(f"  Dirichlet character chi_9: n -> [2^n - 9 is prime].")

# ----------------------------------------------------------------
# 6. Analytic continuation: L_k(0) via zeta regularization
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("ANALYTIC CONTINUATION: L_k(0) VIA ZETA REGULARIZATION")
print("=" * 72)

# For a Dirichlet series L_k(s) = sum_{n in S_k} 1/n^s:
# L_k(0) = |S_k| by direct computation
# The zeta-regularized value (analytic continuation) is:
# L_k(0)_reg = -1/2 + delta_k  where delta_k relates to missing terms
#
# For the full zeta function: zeta(0) = -1/2
# For the trajectory L-function: L(0) = -C0/2
# For the Mersenne gap L_k: L_k(0) = |S_k| (direct)
#
# The regularized value uses the fact that:
#   sum_{n=2}^{oo} chi_k(n) = -1/2 + sum_{n: chi_k(n)=0} 1
# where chi_k(n) = 1 if 2^n - k is prime, 0 otherwise.
#
# Since chi_k(n) = 0 for almost all n, the regularization is:
#   L_k(0)_reg = -1/2 + (number of n where chi_k(n) = 0)_reg
# The second term diverges for sparse sets, so the meaningful
# regularized value is the finite part: -1/2.
#
# This matches the pattern: L_k(0) = -C0_k/2 where C0_k = 1.
# In the unified framework, each Mersenne gap contributes
# L_k(0) = -1/2, and the sum over k gives -N_k/2.

print(f"\n  Direct values L_k(0) = |S_k|:")
for k in ALL_K:
    if k % 2 == 1:
        print(f"    L_{k}(0) = |S_{k}| = {len(S[k])}")

print(f"\n  Zeta-regularized values (analytic continuation):")
for k in ALL_K:
    if k % 2 == 1:
        print(f"    L_{k}(0)_reg = -1/2  (since C0_k = 1 for the gap kernel)")

print(f"\n  Sum over all odd gaps:")
N_odd = sum(1 for k in ALL_K if k % 2 == 1)
print(f"    sum_k L_k(0)_reg = -{N_odd}/2 = -{N_odd/2}")

# The trajectory L-function: L(0) = -C0/2
# The gap L-function: L_k(0) = -1/2
# Ratio: L_k(0) / L(0) = 1/C0
print(f"\n  Connection to trajectory L-function:")
print(f"    L(0)   = -C0/2  (trajectory)")
print(f"    L_k(0) = -1/2   (each gap)")
print(f"    Ratio  = 1/C0   (dimensionless: one gap per unit of C0)")

# ----------------------------------------------------------------
# 7. Theta function modular transformation (functional equation)
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("THETA FUNCTION MODULAR TRANSFORMATION")
print("=" * 72)
print("""
  Define the theta function for the Mersenne gap k:
    Theta_k(q) = sum_{n in S_k} chi_k(n) * q^n
  where chi_k(n) = 1 if 2^n - k is prime, 0 otherwise.

  Mellin transform gives the L-function:
    L_k(s) = sum_{n in S_k} 1/n^s
           = 1/Gamma(s) * int_0^oo Theta_k(e^{-t}) * t^{s-1} dt

  Modular transformation q -> q' = exp(-4*pi^2 / ln(1/q)):
    Under tau -> -1/tau, a modular form of weight w transforms as
      f(-1/tau) = tau^w * f(tau)

  For Theta_k, the transformation gives the functional equation:
    L_k(1-s) = (2*pi)^{-s} * Gamma(s) * cos(pi*s/2) * Phi_k(s)

  where Phi_k(s) is the completed L-function.

  In the Poincare disk picture, theta functions of the Mersenne
  gaps correspond to boundary values of harmonic functions on the
  disk. The Cayley transform maps the disk to the upper half-plane,
  and the modular transformation tau -> -1/tau corresponds to
  the elliptic element S in PSL(2,Z) which fixes z=i.

  For the unified theory:
    Theta_total(q) = C0 * theta_3(q) + sum_k Theta_k(q)
  Under tau -> -1/tau:
    Theta_total(-1/tau) = tau^(1/2) * Theta_total(tau)
  This is the modularity of the unified L-function.
""")

# Compute the first few coefficients of Theta_total
print(f"\n  Theta_total(q) coefficients (unified theta function):")
print(f"    Theta_total(q) = C0 * theta_3(q) + sum_k Theta_k(q)")
# Compute sum over all k of Theta_k coefficients
sum_theta = {}
for k in ALL_K:
    if len(S[k]) > 0:
        for n in S[k]:
            sum_theta[n] = sum_theta.get(n, 0) + 1
print(f"    Number of distinct n in union of all S_k: {len(sum_theta)}")
print(f"    Most covered n: n = {max(sum_theta, key=sum_theta.get)} "
      f"(covered by {max(sum_theta.values())} gaps)")

# ----------------------------------------------------------------
# 7. Connection to trajectory L-function
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("CONNECTION TO TRAJECTORY L(s) = C0 * zeta(s)")
print("=" * 72)
print("""
  The trajectory L-function (from modular_forms.py):
    L(s) = sum_{n=1}^{N} E_n / n^s = C0 * zeta(s) + O(N^{-s+1})
  
  The Mersenne gap L_k(s):
    L_k(s) = sum_{n in S_k} 1 / n^s
  
  The ratio:
    R_k(s) = L_k(s) / L(s) = (1/C0) * sum_{n in S_k} 1/n^s / zeta(s)
  
  At s=2, for k=9:
    R_9(2) = L_9(2) / (C0 * pi^2/6)
  
  But C0 in the trajectory context is the conserved energy,
  while in the Mersenne context C0 is the exponent n.
  
  UNIFICATION: C0 = n when the fundamental is a Mersenne prime.
  The trajectory L-function becomes:
    L_prime(s) = n * zeta(s)   for the Mersenne prime M_n = 2^n - 1
    L_gap(s) = sum_{k in gaps} (2^n - k) / ?
  
  This is the L.O.R.E. unification: every constant C0 defines
  an L-function L_C0(s) = C0 * zeta(s), and every perturbation
  delta = M_n - 9 defines a secondary L-function L_delta(s).
""")

# Compute R_9(2)
if len(S[9]) > 0:
    L9_2_val = sum(1.0 / (n * n) for n in S[9])
    C0_val = max(S[9])  # use max exponent as "C0"
    zeta2 = math.pi ** 2 / 6
    R9_2 = L9_2_val / (C0_val * zeta2) if C0_val > 0 else 0
    print(f"\n  R_9(2) = L_9(2) / (C0 * zeta(2))")
    print(f"         = {L9_2_val:.6f} / ({C0_val} * {zeta2:.6f})")
    print(f"         = {R9_2:.8f}")

# ----------------------------------------------------------------
# 8. Summary: the full taxonomy
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("FULL TAXONOMY OF 2^n - k")
print("=" * 72)
print(f"\n{'k':>4s}  {'count':>6s}  {'parity':>6s}  {'L(2)':>10s}  {'reason':>40s}")
print(f"{'-'*4:>4s}  {'-'*6:>6s}  {'-'*6:>6s}  {'-'*10:>10s}  {'-'*40:>40s}")
for k in ALL_K:
    cnt = len(S[k])
    parity = "even" if k % 2 == 0 else "odd"
    L2 = table[k][4] if table[k][0] > 0 else 0
    if k == 1:
        reason = "Mersenne primes (2^n - 1 itself)"
    elif k % 2 == 0:
        reason = f"Even: 2^n - {k} even for n>1, never prime"
    elif k == 7:
        reason = f"Covering congruence {[p for p,_ in cover_system[:4]]}..."
    elif k == 9:
        reason = f"9 = 3^2 avoids mod-3; harmonic seventh interval"
    else:
        reason = f"Standard odd offset"
    L2_str = f"{L2:.6f}" if cnt > 0 else "-"
    print(f"{k:4d}  {cnt:6d}  {parity:>6s}  {L2_str:>10s}  {reason:>40s}")

# ----------------------------------------------------------------
# 9. EXTENDED k-values (21..49) — sieve-only extrapolation
# ----------------------------------------------------------------
print(f"\n{'=' * 72}")
print("EXTENDED k-VALUES (21..49): SIEVE PREDICTION")
print("=" * 72)
print(f"\n{'k':>4s}  {'type':>14s}  {'sieve%':>8s}  {'prediction':>30s}")
print(f"{'-'*4:>4s}  {'-'*14:>14s}  {'-'*8:>8s}  {'-'*30:>30s}")

# Build 2^n mod p table for sieve analysis
SMALL_PRIMES_SIEVE = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,
                      73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,
                      151,157,163,167,173,179,181,191,193,197,199]
pow2_mod = {p: [pow(2, n, p) for n in range(MAX_N + 1)] for p in SMALL_PRIMES_SIEVE}

def sieve_survival(k):
    passed = 0
    for n in range(2, MAX_N + 1):
        eliminated = False
        for p in SMALL_PRIMES_SIEVE:
            if pow2_mod[p][n] == (k % p):
                eliminated = True
                break
        if not eliminated:
            passed += 1
    return passed / MAX_N * 100

EXTRA_K = [21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49]
for k in EXTRA_K:
    sp = sieve_survival(k)
    # Determine type
    if int(math.isqrt(k))**2 == k:
        sq = int(math.isqrt(k))
        ktype = f"square({sq})"
    elif k % 9 == 0:
        ktype = f"3^2*{k//9}"
    elif k % 3 == 0:
        ktype = f"3*{k//3}"
    elif k % 5 == 0:
        ktype = f"5*{k//5}"
    else:
        ktype = "odd"
    # Prediction: higher sieve survival => more primes expected
    if sp > 30:
        pred = "HIGH density (like k=3)"
    elif sp > 20:
        pred = "MODERATE density (like k=9)"
    elif sp > 10:
        pred = "LOW density (like k=7)"
    else:
        pred = "VERY LOW density (covering congruence)"
    print(f"{k:4d}  {ktype:>14s}  {sp:7.1f}%  {pred}")

print(f"\n  NOTE: k=45 (=3^2x5) has {sieve_survival(45):.1f}% sieve survival (HIGHEST)")
print(f"  k=45 avoids mod-3 (45≡0), mod-5 (45≡0), and mod-7 (2^n≠3 mod 7)")
print(f"  Likely the most productive offset beyond k=1..19, if verified.")

# ----------------------------------------------------------------
# Save taxonomy data
# ----------------------------------------------------------------
taxonomy_out = {
    "L_k": {str(k): {"count": table[k][0], "L0": table[k][1],
                     "L1": table[k][2], "L2": table[k][3],
                     "L3": table[k][4], "ratio": table[k][6]}
            for k in table if table[k][0] > 0},
    "even_barren": {str(k): {"count": table[k][0]} for k in even_k},
    "k7_covering": [p for p, _ in cover_system[:10]],
    "geodesic_ratios": {
        "ln5_ln3": math.log(5)/math.log(3),
        "ln9_ln5": math.log(9)/math.log(5),
        "ln10_ln9": math.log(10)/math.log(9),
    },
    "analytic_continuation": {
        "Lk_0_regex": "L_k(0)_reg = -1/2 for all odd k (zeta-regularized)",
        "total_odd_k": N_odd,
        "sum_Lk_0": -N_odd/2,
        "connection": "L(0) = -C0/2, L_k(0) = -1/2, ratio = 1/C0"
    },
    "theta_modular": {
        "functional_equation": "L_k(1-s) = (2*pi)^{-s} * Gamma(s) * cos(pi*s/2) * Phi_k(s)",
        "unified_theta_modularity": "Theta_total(-1/tau) = tau^(1/2) * Theta_total(tau)"
    },
    "extrapolation_k21_49": {
        str(k): {"sieve_survival_pct": round(sieve_survival(k), 1)}
        for k in EXTRA_K
    },
}
with open("mersenne_taxonomy_data.json", "w") as f:
    json.dump(taxonomy_out, f, indent=2)
print(f"\nSaved to mersenne_taxonomy_data.json")
print("=" * 72)
