"""
B3: THE LOGARITHMIC CORRIDOR (executed + corrected)
====================================================

Claim under test (heuristic from section 4/5.3): slowly-varying
corrections L(s) to the focusing rate modify the Kolmogorov ratio
by some power of L. The exact answer, derivable in one line:

    u(x,s) = lambda(s) * F(lambda(s) * x)   is a PURE DILATION,
    so for every d and EVERY positive lambda(s) -- power, log,
    arbitrary:

        K[u_s] = K[F] * lambda(s)^((d-1)/3)      (EXACT identity)

Consequences:
    d=1: K INVARIANT under all dilation families INCLUDING
         logarithmic ones. The earlier heuristic claim of
         (log 1/s)^(2/3) growth in d=1 was WRONG (an algebra slip:
         |grad u|^2 scales as lambda^4, not lambda^2*L^2).
    d=3: gain is L^((d-1)/3) = L^(2/3), not L^(d+1)/3.
    Corridor has NO MEMORY: the rate depends only on the
    instantaneous scale lambda, never on gamma or history.

Verified below by independent grid construction at multiple s,
gamma, d.
"""
import numpy as np
import json, os


def K_of_snapshot(d, lam, A=1.0, w=1.0, n=None):
    """K for u(x) = lam * F(lam*x), F Gaussian width w; grid built fresh."""
    ws = w / lam
    if n is None:
        n = {1: 4096, 2: 384, 3: 96}[d]
    axis = np.linspace(-5 * ws, 5 * ws, n)
    h = axis[1] - axis[0]
    coords = np.meshgrid(*([axis] * d), indexing="ij")
    r2 = sum(c ** 2 for c in coords)
    U = lam * A * np.exp(-r2 / (2 * ws ** 2))
    g2 = np.zeros_like(U)
    for ax in range(d):
        g2 += np.gradient(U, h, axis=ax) ** 2
    eps = float(np.sum(g2) * h ** d)          # nu=1 absorbed
    u_inf = float(np.max(np.abs(U)))
    return u_inf / max(eps, 1e-300) ** (1.0 / 3.0)


def main():
    print("=" * 70)
    print("B3 LOGARITHMIC CORRIDOR: exact dilation identity test")
    print("prediction: K(s) = K[F] * lambda(s)^((d-1)/3), no memory")
    print("=" * 70)
    results = []
    for d in (1, 2, 3):
        K_F = K_of_snapshot(d, lam=1.0)       # reference at lambda=1
        for gamma in (0.0, 0.5, 1.0):
            rows = []
            for s in np.logspace(-0.2, -4, 10):
                lam = s ** (-0.75) * (np.log(1 / s)) ** gamma
                Ks = K_of_snapshot(d, lam)
                rows.append({"s": float(s), "lam": float(lam),
                             "K": float(Ks)})
            # fit log K vs log lam -> slope should be (d-1)/3 EXACTLY
            lx = np.log([r["lam"] for r in rows])
            ly = np.log([r["K"] for r in rows])
            slope = float(np.polyfit(lx, ly, 1)[0])
            pred = (d - 1) / 3.0
            ok = abs(slope - pred) < 5e-3
            results.append({"d": d, "gamma": gamma, "slope": slope,
                            "predicted": pred})
            print(f"d={d} gamma={gamma:.1f}: slope {slope:+.5f} "
                  f"vs predicted {pred:+.5f}  "
                  f"{'MATCH' if ok else 'MISMATCH'}")
        print()

    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("1. Slope depends ONLY on d -- never on gamma: the corridor")
    print("   has no memory. Log corrections act solely through the")
    print("   instantaneous scale.")
    print("2. Corrected exponent: L^((d-1)/3). The earlier heuristic")
    print("   L^((d+1)/3) was an algebra slip (lambda^4 vs lambda^2).")
    print("3. d=1 is invariant under ARBITRARY dilation families --")
    print("   power, logarithmic, or otherwise. The one-dimensional")
    print("   invariance (R3) is stronger than previously stated:")
    print("   even logarithmic corrections cannot move the ratio.")
    print("=" * 70)

    os.makedirs("data", exist_ok=True)
    with open("data/log_corridor.json", "w") as fh:
        json.dump(results, fh, indent=2)


if __name__ == "__main__":
    main()
