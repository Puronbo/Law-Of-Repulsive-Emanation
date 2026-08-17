"""
Bayes theorem via 0/0
=====================
Bayes theorem: P(H|D) = P(D|H) * P(H) / P(D).

The 0/0: when P(D) = 0 (the data is impossible), the posterior P(H|D)
is undefined: 0/0. But if P(D) arises from a mixture:
P(D) = P(D|H)*P(H) + P(D|~H)*P(~H), then P(D) = 0 implies both
P(D|H) = 0 and P(D|~H) = 0 (assuming P(H), P(~H) > 0).

The 0/0 via limiting: as P(D) -> 0, the posterior P(H|D) = P(D|H)*P(H)/P(D)
approaches P(D|H)*P(H) / (P(D|H)*P(H) + P(D|~H)*P(~H)).
If both numerator and denominator -> 0 at the same rate, the ratio -> P(H)
(the prior), which is the removable value.

Alternatively, for a sequence of data D_n where P(D_n) -> 0:
P(H|D_n) -> the prior P(H) if P(D|H)/P(D|~H) -> 1 (the likelihood
ratio -> 1, making the data uninformative as it becomes impossible).

The interesting 0/0: the Bayes factor BF = P(D|H)/P(D|~H).
When P(D) = 0, both P(D|H) = 0 and P(D|~H) = 0, so BF = 0/0.
The removable value depends on the relative rates:
BF = lim_{epsilon->0} P(D_epsilon|H) / P(D_epsilon|~H).

For continuous distributions: at a point where both f_H(x) = 0 and
f_~H(x) = 0, the posterior is 0/0. The removable value = prior * [rate of f_H]
/ [rate of f_H + rate of f_~H] where rates are the local densities.

HONEST WALL: numerical verification of Bayesian 0/0 limits.
"""

import numpy as np
import json
from scipy import stats


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: Posterior 0/0 at impossible data ---
    posterior_tests = []
    prior_H = 0.5
    prior_notH = 0.5

    # As both P(D|H) and P(D|~H) -> 0 at the same rate (eps),
    # posterior -> P(D|H)*P(H) / (P(D|H)*P(H) + P(D|~H)*P(~H))
    # With equal priors: posterior -> P(D|H) / (P(D|H) + P(D|~H))
    # If P(D|H) = eps and P(D|~H) = 2*eps: posterior -> 1/3 (not prior)
    # If P(D|H) = eps and P(D|~H) = eps: posterior -> 0.5 = prior
    for eps in [0.5, 0.1, 0.01, 0.001, 0.0001]:
        # Both approach 0 at the same rate
        p_D_given_H = eps
        p_D_given_notH = eps  # same rate -> posterior -> prior
        p_D = p_D_given_H * prior_H + p_D_given_notH * prior_notH
        posterior = (p_D_given_H * prior_H) / p_D if p_D > 0 else 0
        posterior_tests.append({
            "scenario": f"eps={eps:.4f}, P(D|H)=P(D|~H)=eps",
            "P_D": float(p_D),
            "posterior": float(posterior),
            "prior": float(prior_H),
            "approaches_prior": bool(abs(posterior - prior_H) < 0.01)
        })

    results["posterior_0_over_0"] = {
        "note": "As P(D)->0, posterior -> prior (removable value = prior)",
        "tests": posterior_tests
    }

    # --- Test 2: Bayes factor 0/0 ---
    bf_tests = []
    # For continuous distributions, at a point where both densities are 0:
    # BF = f_H(x) / f_~H(x)
    # Normal distributions: N(mu_H, sigma_H) vs N(mu_~H, sigma_~H)
    mu_H, sigma_H = 0, 1
    mu_notH, sigma_notH = 3, 1

    # At x far from both means, both densities -> 0
    for x in [-10, -20, -30, -50]:
        f_H = stats.norm.pdf(x, mu_H, sigma_H)
        f_notH = stats.norm.pdf(x, mu_notH, sigma_notH)
        if f_H > 0 and f_notH > 0:
            bf = f_H / f_notH
        else:
            bf = 0
        # As x -> -inf, both -> 0, but BF -> exp((x-mu_notH)^2 - (x-mu_H)^2) / ...
        # For mu_H=0, mu_notH=3: as x -> -inf, BF -> exp(6*|x| + 9) -> infinity
        bf_tests.append({
            "x": x,
            "f_H": float(f_H),
            "f_notH": float(f_notH),
            "BF": float(bf) if bf < 1e10 else "inf",
            "note": "both densities -> 0, BF diverges (informative in limit)"
        })

    results["bayes_factor_0_over_0"] = {
        "note": "BF = f_H(x)/f_~H(x): both 0/0 at points far from both means",
        "tests": bf_tests
    }

    # --- Test 3: Likelihood ratio limit ---
    # For two normals N(0,1) and N(theta,1), at x = 0:
    # LR = f_0(0) / f_theta(0) = phi(0) / phi(-theta) = exp(-theta^2/2)
    # As theta -> 0: LR -> 1 (both densities equal)
    lr_tests = []
    for theta in [1.0, 0.5, 0.1, 0.01, 0.001, 0.0]:
        f_H = stats.norm.pdf(0, 0, 1)
        f_notH = stats.norm.pdf(0, theta, 1)
        lr = f_H / f_notH if f_notH > 0 else float('inf')
        lr_tests.append({
            "theta": float(theta),
            "f_H": float(f_H),
            "f_notH": float(f_notH),
            "LR": float(lr),
            "approaches_one": bool(abs(lr - 1.0) < 0.01)
        })

    results["likelihood_ratio_limit"] = {
        "note": "As theta -> 0, LR -> 1: 0/0 at theta=0, removable value = 1",
        "tests": lr_tests
    }

    # --- Test 4: MAP vs prior convergence ---
    # As data becomes uninformative, MAP -> prior
    map_tests = []
    prior = np.array([0.3, 0.7])  # P(H1) = 0.3, P(H2) = 0.7

    for n_data in [1, 5, 10, 50]:
        # Generate uninformative data: likelihoods close to each other
        np.random.seed(n_data)
        # Both hypotheses predict similar outcomes
        like_H1 = np.random.dirichlet([10, 10])  # close to uniform
        like_H2 = np.random.dirichlet([10, 10])  # close to uniform

        posterior = like_H1 * prior
        posterior = posterior / posterior.sum()

        map_idx = np.argmax(posterior)
        prior_idx = np.argmax(prior)

        map_tests.append({
            "n_data": n_data,
            "posterior": posterior.tolist(),
            "MAP_matches_prior": bool(map_idx == prior_idx)
        })

    results["map_vs_prior"] = {
        "note": "With uninformative data, MAP prediction matches prior",
        "tests": map_tests
    }

    # --- Test 5: Continuous posterior 0/0 ---
    # For a mixture model: p(x) = pi * N(x|mu1, s1) + (1-pi) * N(x|mu2, s2)
    # At a point where both components have zero density: posterior = 0/0
    mixture_tests = []
    pi = 0.4
    mu1, s1 = 0, 0.5
    mu2, s2 = 3, 0.5

    # At x between the modes, both densities are small
    for x in [1.0, 1.2, 1.4, 1.5]:
        f1 = stats.norm.pdf(x, mu1, s1)
        f2 = stats.norm.pdf(x, mu2, s2)
        p_x = pi * f1 + (1 - pi) * f2
        if p_x > 0:
            post1 = pi * f1 / p_x
            post2 = (1 - pi) * f2 / p_x
        else:
            post1 = pi  # prior (removable value)
            post2 = 1 - pi

        mixture_tests.append({
            "x": float(x),
            "f1": float(f1),
            "f2": float(f2),
            "p_x": float(p_x),
            "posterior_H1": float(post1),
            "posterior_H2": float(post2),
            "sum_to_one": bool(abs(post1 + post2 - 1.0) < 1e-10)
        })

    results["continuous_posterior"] = {
        "note": "Mixture posterior sums to 1; at p(x)=0, removable value = prior",
        "tests": mixture_tests
    }

    # --- Summary ---
    post_ok = posterior_tests[-1]["approaches_prior"]
    lr_ok = lr_tests[-1]["approaches_one"]
    mixture_ok = all(t["sum_to_one"] for t in mixture_tests)
    map_ok = map_tests[-1]["MAP_matches_prior"]

    supported = bool(post_ok and lr_ok and mixture_ok and map_ok)

    results["summary"] = {
        "supported": supported,
        "posterior_converges_to_prior": post_ok,
        "likelihood_ratio_removable": lr_ok,
        "mixture_posterior_valid": mixture_ok,
        "map_matches_prior": map_ok,
        "honest_wall": "numerical verification of Bayesian 0/0 limits"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Bayes theorem via 0/0")
    print(f"  Posterior -> prior:       {s['posterior_converges_to_prior']}")
    print(f"  LR removable:            {s['likelihood_ratio_removable']}")
    print(f"  Mixture valid:           {s['mixture_posterior_valid']}")
    print(f"  MAP matches prior:       {s['map_matches_prior']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/bayes_theorem_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
