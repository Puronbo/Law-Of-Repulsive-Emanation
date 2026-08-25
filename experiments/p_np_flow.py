import json, math, os, random
import numpy as np
from itertools import product

OUT = "data/p_np_flow.json"


def make_3cnf(N, clauses):
    return {"num_vars": N, "clauses": clauses}


def random_3sat(N, M, seed):
    rng = random.Random(seed)
    clauses = []
    for _ in range(M):
        vs = rng.sample(range(N), 3)
        pols = [rng.choice([True, False]) for _ in range(3)]
        clauses.append(list(zip(vs, pols)))
    return make_3cnf(N, clauses)


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


def incidence_matrix(phi):
    N = phi["num_vars"]
    M = len(phi["clauses"])
    mat = np.zeros((N, M))
    for j, cl in enumerate(phi["clauses"]):
        for vi, pol in cl:
            mat[vi, j] = 1.0 if pol else -1.0
    return mat


def interaction_graph(phi):
    N = phi["num_vars"]
    A = np.zeros((N, N))
    for cl in phi["clauses"]:
        vs = [v for v, _ in cl]
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                A[vs[i], vs[j]] += 1
                A[vs[j], vs[i]] += 1
    return A


def spectral_gap_incidence(phi):
    mat = incidence_matrix(phi)
    s = np.linalg.svd(mat, compute_uv=False)
    return float(s[-1]) if len(s) > 0 else 0.0


def spectral_gap_laplacian(phi):
    A = interaction_graph(phi)
    N = A.shape[0]
    D = np.diag(A.sum(axis=1))
    L = D - A
    evals = np.linalg.eigvalsh(L)
    evals.sort()
    return float(evals[1]) if len(evals) > 1 else 0.0


def participation_ratio(phi):
    N = phi["num_vars"]
    total = 0.0
    sum_sq = 0.0
    for asgn in product([-1, 1], repeat=N):
        P = 1.0 if brute_force_count_single(asgn, phi) else 0.0
        total += P
        sum_sq += P * P
    if sum_sq == 0:
        return 0.0
    return total * total / sum_sq


def brute_force_single(asgn, phi):
    for cl in phi["clauses"]:
        if not any(asgn[v] if p else not asgn[v] for v, p in cl):
            return False
    return True


def assignment_entropy(phi):
    N = phi["num_vars"]
    Z = 0
    for asgn in product([-1, 1], repeat=N):
        if brute_force_single(asgn, phi):
            Z += 1
    if Z == 0:
        return 0.0, 0.0
    H = math.log(Z)
    H_norm = H / (N * math.log(2)) if N > 0 else 0.0
    return H, H_norm


def run():
    results = {}

    print("Q1: Spectral gap across phase transition...")
    q1 = {}
    N = 10
    num_trials = 30
    for M in range(3, 65, 3):
        gaps = []
        laps = []
        sats = []
        Hs = []
        for trial in range(num_trials):
            phi = random_3sat(N, M, trial * 1000 + M)
            Z = brute_force_count(phi)
            sats.append(1 if Z > 0 else 0)
            gaps.append(spectral_gap_incidence(phi))
            laps.append(spectral_gap_laplacian(phi))
            _, Hn = assignment_entropy(phi)
            Hs.append(Hn)
        q1[M] = {
            "N": N, "M": M, "ratio": round(M / N, 2),
            "sat_frac": round(sum(sats) / num_trials, 3),
            "mean_spectral_gap": round(float(np.mean(gaps)), 4),
            "std_spectral_gap": round(float(np.std(gaps)), 4),
            "mean_algebraic_conn": round(float(np.mean(laps)), 4),
            "mean_H_norm": round(float(np.mean(Hs)), 4),
        }
    results["Q1_spectral_vs_density"] = q1
    print("  %d density points" % len(q1))

    print("Q2: Scaling with N at critical density...")
    q2 = {}
    ratio_fixed = 4.25
    for N in [5, 8, 10, 15, 20]:
        M = int(ratio_fixed * N)
        gs = []
        ls = []
        for trial in range(20):
            phi = random_3sat(N, M, trial * 1000 + M)
            gs.append(spectral_gap_incidence(phi))
            ls.append(spectral_gap_laplacian(phi))
        q2[N] = {
            "N": N, "M": M, "ratio": ratio_fixed,
            "mean_gap": round(float(np.mean(gs)), 4),
            "mean_lap": round(float(np.mean(ls)), 4),
        }
    results["Q2_scaling"] = q2
    print("  %d sizes" % len(q2))

    print("Q3: Entropy across transition...")
    q3 = {}
    N = 10
    for M in range(3, 65, 5):
        Hs = []
        Zs = []
        for trial in range(20):
            phi = random_3sat(N, M, trial * 1000 + M)
            Z = brute_force_count(phi)
            _, Hn = assignment_entropy(phi)
            Hs.append(Hn)
            Zs.append(Z)
        q3[M] = {
            "N": N, "M": M, "ratio": round(M / N, 2),
            "mean_H_norm": round(float(np.mean(Hs)), 4),
            "mean_logZ": round(float(np.mean([math.log(z + 1) for z in Zs])), 4),
        }
    results["Q3_entropy"] = q3
    print("  %d points" % len(q3))

    print("Q4: Flow variable (combined phase diagram)...")
    q4 = {}
    N = 10
    for M in range(3, 65, 3):
        items = []
        for trial in range(20):
            phi = random_3sat(N, M, trial * 1000 + M)
            Z = brute_force_count(phi)
            sg = spectral_gap_incidence(phi)
            sl = spectral_gap_laplacian(phi)
            _, Hn = assignment_entropy(phi)
            items.append({"sat": 1 if Z > 0 else 0, "gap": sg, "lap": sl, "H": Hn})
        sat_items = [x for x in items if x["sat"] == 1]
        unsat_items = [x for x in items if x["sat"] == 0]
        q4[M] = {
            "ratio": round(M / N, 2),
            "sat_frac": round(len(sat_items) / len(items), 3) if items else 0,
        }
        if sat_items:
            q4[M]["sat_mean_gap"] = round(float(np.mean([x["gap"] for x in sat_items])), 4)
            q4[M]["sat_mean_H"] = round(float(np.mean([x["H"] for x in sat_items])), 4)
        if unsat_items:
            q4[M]["unsat_mean_gap"] = round(float(np.mean([x["gap"] for x in unsat_items])), 4)
    results["Q4_phase_diagram"] = q4
    print("  %d points" % len(q4))

    output = {
        "experiment": "P vs NP: Flow Variables for Contour Compression",
        "Q1_spectral_vs_density": results["Q1_spectral_vs_density"],
        "Q2_scaling": results["Q2_scaling"],
        "Q3_entropy": results["Q3_entropy"],
        "Q4_phase_diagram": results["Q4_phase_diagram"],
        "key_question": "Does the spectral gap close at the SAT/UNSAT phase transition?",
        "honest_wall": "If spectral gap closes at M/N ~ 4.267, it identifies the entanglement that prevents compression. A compression flow would need to maintain nonzero gap.",
    }
    os.makedirs("data", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print("Done.")
    return output


if __name__ == "__main__":
    run()
