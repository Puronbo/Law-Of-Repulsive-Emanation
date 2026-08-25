import json, math, os, random, time
from itertools import product, combinations

OUT = "data/p_np_contour.json"


def make_3cnf(N, clauses):
    return {"num_vars": N, "clauses": clauses}


def brute_force_count(phi):
    N = phi["num_vars"]
    c = 0
    for a in product([False, True], repeat=N):
        sat = True
        for cl in phi["clauses"]:
            if not any(a[v] if p else not a[v] for v, p in cl):
                sat = False
                break
        if sat:
            c += 1
    return c


def evaluate_P(phi, zv):
    r = 1.0 + 0j
    for cl in phi["clauses"]:
        u = 1.0 + 0j
        for vi, pol in cl:
            u *= (1.0 - zv[vi]) / 2.0 if pol else (1.0 + zv[vi]) / 2.0
        r *= (1.0 - u)
    return r


def boolean_sum(phi):
    N = phi["num_vars"]
    total = 0
    for asgn in product([-1, 1], repeat=N):
        total += round(evaluate_P(phi, list(asgn)).real)
    return total


def clause_degree(phi):
    d = [0] * phi["num_vars"]
    for cl in phi["clauses"]:
        for v, _ in cl:
            d[v] += 1
    return d


def approx_treewidth(phi):
    N = phi["num_vars"]
    adj = [set() for _ in range(N)]
    for cl in phi["clauses"]:
        vs = [v for v, _ in cl]
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                adj[vs[i]].add(vs[j])
                adj[vs[j]].add(vs[i])
    eliminated = set()
    maxd = 0
    for _ in range(N):
        bv, bd = -1, N + 1
        for v in range(N):
            if v in eliminated:
                continue
            d = len(adj[v] - eliminated)
            if d < bd:
                bd, bv = d, v
        if bv < 0:
            break
        neighbors = adj[bv] - eliminated
        for x in neighbors:
            for y in neighbors:
                if x != y:
                    adj[x].add(y)
        eliminated.add(bv)
        maxd = max(maxd, bd)
    return maxd


def random_3sat(N, M, seed):
    rng = random.Random(seed)
    clauses = []
    for _ in range(M):
        vs = rng.sample(range(N), 3)
        pols = [rng.choice([True, False]) for _ in range(3)]
        clauses.append(list(zip(vs, pols)))
    return make_3cnf(N, clauses)


def mc_contour(phi, R=2.0, nsamp=50000, seed=42):
    rng = random.Random(seed)
    N = phi["num_vars"]
    total = 0.0 + 0j
    for _ in range(nsamp):
        ts = [rng.uniform(0, 2 * math.pi) for _ in range(N)]
        zs = [R * complex(math.cos(t), math.sin(t)) for t in ts]
        P = evaluate_P(phi, zs)
        kprod = 1.0 + 0j
        for i in range(N):
            z = zs[i]
            kprod *= 2 * z / (z * z - 1) * z
        total += P * kprod
    return total / nsamp


def run():
    results = {}

    print("Q1: All 3-var formulas...")
    all_cl = []
    for p1 in [True, False]:
        for p2 in [True, False]:
            for p3 in [True, False]:
                all_cl.append([(0, p1), (1, p2), (2, p3)])
    q1 = {"total": 0, "match": 0, "mismatch": 0}
    for r in range(1, len(all_cl) + 1):
        for combo in combinations(range(len(all_cl)), r):
            phi = make_3cnf(3, [all_cl[i] for i in combo])
            zb = brute_force_count(phi)
            zz = boolean_sum(phi)
            q1["total"] += 1
            if zb == zz:
                q1["match"] += 1
            else:
                q1["mismatch"] += 1
    results["Q1"] = q1
    print("  %d formulas, %d match, %d mismatch" % (q1["total"], q1["match"], q1["mismatch"]))

    print("Q2: Random 3-SAT...")
    q2 = {}
    for N in [5, 8, 10, 12]:
        for ratio in [3.0, 4.25, 5.0]:
            M = int(ratio * N)
            phi = random_3sat(N, M, 42)
            zb = brute_force_count(phi)
            zz = boolean_sum(phi)
            deg = clause_degree(phi)
            tw = approx_treewidth(phi)
            key = "N%d_M%d" % (N, M)
            q2[key] = {"N": N, "M": M, "ratio": ratio, "Z": zb,
                        "match": zb == zz, "maxdeg": max(deg), "treewidth": tw}
    results["Q2"] = q2
    all_match = all(v["match"] for v in q2.values())
    print("  %d formulas, all match=%s" % (len(q2), all_match))

    print("Q3: Phase transition...")
    q3 = {}
    for N in [7, 10]:
        step = max(1, N // 3)
        for M in range(2, int(6.5 * N), step):
            fracs = []
            for trial in range(25):
                phi = random_3sat(N, M, trial * 1000 + M)
                fracs.append(1 if brute_force_count(phi) > 0 else 0)
            frac = round(sum(fracs) / len(fracs), 3)
            q3["N%d_M%d" % (N, M)] = {"N": N, "M": M,
                                         "ratio": round(M / N, 2),
                                         "sat_frac": frac}
    results["Q3"] = q3
    print("  %d density points" % len(q3))

    print("Q4: Structural invariants...")
    q4 = {}
    for N in [5, 8, 10, 15, 20]:
        for ratio in [3.0, 4.25]:
            M = int(ratio * N)
            phi = random_3sat(N, M, 42)
            deg = clause_degree(phi)
            tw = approx_treewidth(phi)
            ov = [[0] * N for _ in range(N)]
            for cl in phi["clauses"]:
                vs = [v for v, _ in cl]
                for i in range(len(vs)):
                    for j in range(i + 1, len(vs)):
                        ov[vs[i]][vs[j]] += 1
                        ov[vs[j]][vs[i]] += 1
            max_pair = max(max(row) for row in ov) if N > 0 else 0
            q4["N%d_r%s" % (N, ratio)] = {
                "N": N, "M": M, "treewidth": tw,
                "maxdeg": max(deg),
                "meandeg": round(sum(deg) / N, 1),
                "max_pair_ov": max_pair
            }
    results["Q4"] = q4
    print("  %d configs" % len(q4))

    print("Q5: MC contour convergence...")
    q5 = {}
    for N in [3, 4, 5]:
        phi = random_3sat(N, 3 * N, 42)
        Z_exact = brute_force_count(phi)
        for nsamp in [1000, 5000, 20000, 100000]:
            zmc = mc_contour(phi, nsamp=nsamp, seed=42)
            err = abs(zmc.real - Z_exact)
            q5["N%d_s%d" % (N, nsamp)] = {
                "N": N, "nsamp": nsamp, "Z_exact": Z_exact,
                "Z_mc": round(zmc.real, 4), "error": round(err, 4)
            }
    results["Q5"] = q5
    print("  %d convergence points" % len(q5))

    output = {
        "experiment": "P vs NP: Contour Integral Identity for #SAT",
        "Q1_identity": results["Q1"],
        "Q2_random_3sat": results["Q2"],
        "Q3_phase_transition": results["Q3"],
        "Q4_structural": results["Q4"],
        "Q5_mc_convergence": results["Q5"],
        "key_insight": (
            "Z_phi exact contour identity costs O(K^N) quadrature or O(2^N) Boolean. "
            "P=NP iff state-space compressible to poly(N)."
        ),
        "honest_wall": (
            "Identity reformulates #SAT as multidimensional residue. "
            "Algorithmically equivalent to enumeration. No polynomial-size "
            "compilation theorem known for general formulas."
        ),
    }
    os.makedirs("data", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print("Done.")
    return output


if __name__ == "__main__":
    run()
