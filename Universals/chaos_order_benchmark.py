"""
T32: Chaos-order completeness benchmark.
Compute C(f) = D_f / D_d for elementary benchmarks to establish
the full range of the chaos index.
"""
import numpy as np, math

def gap_D(vals):
    gaps = [abs(vals[i+1] - vals[i]) for i in range(len(vals)-1)]
    mg, vg = float(np.mean(gaps)), float(np.var(gaps))
    return vg / mg if mg > 0 else 0

def factorise(n):
    if n == 1: return {}
    d, pf, p = n, {}, 2
    while p * p <= d:
        while d % p == 0: pf[p] = pf.get(p, 0) + 1; d //= p
        p += 1 if p == 2 else 2
    if d > 1: pf[d] = pf.get(d, 0) + 1
    return pf

def d(n, cnt=1):
    for a in factorise(n).values(): cnt *= a + 1
    return cnt

N = 100
D_d = gap_D([d(n) for n in range(1, N+1)])

np.random.seed(42)

benchmarks = {}

# --- Ordered (C near 0) ---
benchmarks["constant 1"] = [1.0] * N
benchmarks["(-1)^n"] = [(-1.0)**n for n in range(N)]
benchmarks["n mod 5"] = [float(n % 5) for n in range(N)]
benchmarks["sin(n)"] = [math.sin(n) for n in range(N)]
benchmarks["n^2 mod 7"] = [float((n*n) % 7) for n in range(N)]

# --- Arithmetic functions ---
benchmarks["omega(n)"] = [float(len(factorise(n))) for n in range(1, N+1)]
benchmarks["Omega(n)"] = [float(sum(factorise(n).values())) for n in range(1, N+1)]
benchmarks["d(n)"] = [float(d(n)) for n in range(1, N+1)]

# --- Random / chaotic ---
benchmarks["uniform U[0,1]"] = list(np.random.uniform(0, 1, N))
benchmarks["normal N(0,1)"] = list(np.random.normal(0, 1, N))

log_r = [0.5]
for i in range(N-1):
    log_r.append(4.0 * log_r[-1] * (1.0 - log_r[-1]))
benchmarks["logistic r=4"] = log_r

log_r3 = [0.5]
for i in range(N-1):
    log_r3.append(3.8 * log_r3[-1] * (1.0 - log_r3[-1]))
benchmarks["logistic r=3.8"] = log_r3

lcg = [1.0]
for i in range(N-1):
    lcg.append((lcg[-1]*1664525 + 1013904223) % (2**32) / (2**32))
benchmarks["LCG PRNG"] = lcg

benchmarks["Poisson(1)"] = [float(np.random.poisson(1)) for _ in range(N)]
benchmarks["geometric p=0.1"] = [float(np.random.geometric(0.1)) for _ in range(N)]

# --- Deterministic trend (bounded) ---
benchmarks["|sin(n)|"] = [abs(math.sin(n)) for n in range(N)]

print(f"Baseline D_d = {D_d:.4f}")
print(f"{'Benchmark':>30} {'D':>10} {'C':>10}")
print("-" * 52)
results = {}
for name, vals in benchmarks.items():
    D = gap_D(vals)
    c = D / D_d
    results[name] = c
    print(f"{name:>30} {D:>10.4f} {c:>10.4f}")

print(f"\n  C range: [{min(results.values()):.4f}, {max(results.values()):.4f}]")
print(f"  Functions with C < 1 (sub-chaotic): {sum(1 for c in results.values() if c < 1)}")
print(f"  Functions with C = 1 (critical):    {sum(1 for c in results.values() if abs(c-1) < 0.05)}")
print(f"  Functions with C > 1 (super-chaotic): {sum(1 for c in results.values() if c > 1)}")
