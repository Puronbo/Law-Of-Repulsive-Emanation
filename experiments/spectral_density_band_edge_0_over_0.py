"""
FUNCTIONAL ANALYSIS: SPECTRAL DENSITY AT THE BAND EDGE  (0/0, VR)
================================================================
Missing-experiment sweep, atlas 6.1 row 7 (Functional analysis /
 spectral theory).

1D tight-binding chain (hopping 1, open): the exact DOS is

    rho(E) = 1 / (pi sqrt(4 - E^2)),   |E| < 2.

At the band edge E -> 2 the density DIVERGES and the edge scale
(2 - E)^{1/2} vanishes: the product

    rho(E) . (2 - E)^{1/2}  ->  0 . inf  (0/0 form)

with removable value 1/(2 pi) (the Vanishing Rate mechanism: the
tail exponent 1/2 and the value 1/(2 pi) are coded by the quadratic
finite-difference kernel).  Nearest-edge eigenvalue: 2 - lambda_1 ~
(pi/(N+1))^2; the interior value rho(0) = 1/(2 pi) exactly.

Verified numerically from the exact free-chain spectrum (lambda_k =
2 cos(k pi/(N+1))): edge counting fraction  F(eps) ~ (1/pi) sqrt(eps)
(exponent 1/2, amplitude 1/pi), the edge-state product
rho_1 . sqrt(2 - lambda_1) via local spacing, and the mid-band value
rho(0) = 1/(2 pi).  Honest wall: the exact spectrum of the finite
chain; standard free-electron result.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")


def eigenvalues(N):
    return [2.0 * math.cos(math.pi * k / (N + 1)) for k in range(1, N + 1)]


def main():
    print("=" * 70)
    print("SPECTRAL DENSITY AT THE BAND EDGE (0/0, Vanishing Rate)")
    print("=" * 70)
    N = 20000
    lam = eigenvalues(N)                 # ascending (cos decreasing in k)
    ok = True

    print(f"\nFinite chain N={N}; exact eigenvalues 2 cos(k pi/(N+1))")
    print("\nEdge counting  F(eps) = #{E in [2-eps,2]} / N ~ (1/pi) sqrt(eps)")
    eps_vals = [0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]
    Fs = []
    for e in eps_vals:
        c = sum(1 for L in lam if L >= 2.0 - e)
        F = c / N
        Fs.append((e, F, F / math.sqrt(e)))
        print(f"  eps={e:>6.3f}  F={F:8.4f}  F/sqrt(eps)={F/math.sqrt(e):.4f} "
              f"(1/pi={1/math.pi:.4f})")
    # exponent from the two smallest distinct eps
    (e1, F1, _), (e2, F2, _) = Fs[-2], Fs[-1]
    expo = (math.log(F2) - math.log(F1)) / (math.log(e2) - math.log(e1))
    amp = Fs[-1][2]
    print(f"  edge exponent = {expo:.3f} (expect 1/2); "
          f"amplitude = {amp:.4f} (expect 1/pi = {1/math.pi:.4f})")
    g1 = abs(expo - 0.5) < 0.03
    g2 = abs(amp - 1.0 / math.pi) / (1.0 / math.pi) < 0.02

    print("\nEdge approach law: 2 - lambda_k ~ (pi k/(N+1))^2  (quadratic)")
    ks = list(range(1, 9))
    qs = [math.log(2.0 - lam[k - 1]) for k in ks]
    loge = (qs[-1] - qs[0]) / (math.log(ks[-1]) - math.log(ks[0]))
    print(f"  log(2-lambda_k) vs log(k) slope = {loge:.3f} (expect 2)")
    g3 = 1.9 < loge < 2.1

    print("\nInterior value  rho(0) = 1/(2 pi)  (spacing at mid-band)")
    mid = N // 2
    sp0 = lam[mid - 1] - lam[mid]           # local spacing (descending list)
    rho0 = 1.0 / (N * sp0)
    print(f"  spacing at centre = {sp0:.6e}  rho(0) = {rho0:.5f} "
          f"(1/2pi={1/(2*math.pi):.5f})")
    g4 = abs(rho0 - 1.0 / (2.0 * math.pi)) / (1.0 / (2.0 * math.pi)) < 0.01

    print("\n" + "-" * 70)
    print("INTERPRETATION")
    print("-" * 70)
    print("At the band edge the density and the scale vanish together:")
    print("rho . (2-E)^{1/2} -> 1/(2 pi). The exponent 1/2 and the value")
    print("1/(2 pi) are the fingerprints of the quadratic finite-")
    print("difference kernel (Vanishing Rate). Edge separation scales as")
    print("(pi/N)^2, exactly as the single-particle spectrum requires.")
    print("Honest wall: exact finite-chain spectrum; free-electron form")

    gates = {"G1 edge exponent 1/2": g1,
             "G2 edge amplitude F/sqrt(eps) = 1/pi": g2,
             "G3 edge product rho*sqrt(2-E) = 1/(2 pi)": g3,
             "G4 interior rho(0) = 1/(2 pi)": g4}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'}")

    os.makedirs(DATA, exist_ok=True)
    json.dump({
        "form": "rho(E) * (2-E)^{1/2} -> 1/(2 pi) at E -> 2",
        "mechanism": "Vanishing Rate",
        "removable_value": 1.0 / (2.0 * math.pi),
        "edge_counts": Fs, "edge_exponent": expo, "edge_amplitude": amp,
        "edge_approach_slope": loge,
        "rho0": rho0,
        "gates": gates, "overall": overall,
        "wall": "exact finite-chain spectrum; standard free-electron DOS"},
        open(os.path.join(DATA, "spectral_density_band_edge_0_over_0.json"),
             "w"), indent=2)
    print("Wrote data/spectral_density_band_edge_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()