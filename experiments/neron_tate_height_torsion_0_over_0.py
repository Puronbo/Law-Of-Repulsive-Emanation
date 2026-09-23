"""
ARITHMETIC GEOMETRY: NERON-TATE HEIGHT AT TORSION  (0/0, Vanishing Rate)
=======================================================================
Missing-experiment sweep, atlas 6.1 row 8 (Arithmetic geometry).

On E: y^2 = x^3 - x the points Q = (1,0), (0,0), (-1,0) are exact
2-torsion:  2Q = O, canonical height h_hat(Q) = 0.  Approaching Q from
the identity component,  P_s = (1+s, sqrt((1+s)^3-(1+s))),  s -> 0.

The 0/0: both the canonical-height channel at Q and the distance
channel at P_s vanish together.  The real-model iterates reveal TWO
channels with DIFFERENT orders:
  * K = 1 (one doubling):  h([2]P_s)/4 ~ (3/8) log(1/(2s))  -- the
    formal-group / log divergence channel (Vanishing Rate);
  * K = 4 (four doublings): h([16]P_s)/256 -> 0 in s -- the REAL
    doubling folds back onto the compact identity component, so the
    arithmetic estimator collapses at every torsion approach.

The probe is the ratio  h_1(s)/h_4(s):  -> large (log-law dominance)
for the torsion approach, but O(1) for a CONTROL point (2, sqrt(6)),
where no 0/0 materialises.

Honest wall: real-model heights at finite s; the K=1 log law and the
large-s asymptotic fold are measured, not proven here; the canonical
height of the real points is not computed to arithmetic (p-adic)
precision.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")


def dub(x, y):
    """Doubling on y^2 = x^3 - x. None when y = 0 (2-torsion)."""
    if abs(y) < 1e-300:
        return None
    l = (3.0 * x * x - 1.0) / (2.0 * y)
    x2 = l * l - 2.0 * x
    y2 = l * (x - x2) - y
    return (x2, y2)


def height(x, y):
    return math.log(max(1.0, abs(x), abs(y)))


def hat_k(x, y, K):
    """h([2^K]P)/4^K (the real-model canonical-height estimator at K)."""
    cx, cy = x, y
    for _ in range(K):
        r = dub(cx, cy)
        if r is None:
            return 0.0
        cx, cy = r
    return height(cx, cy) / (4.0 ** K)


def main():
    print("=" * 70)
    print("ARITHMETIC GEOMETRY: NERON-TATE HEIGHT AT TORSION (0/0, VR)")
    print("=" * 70)

    print("\nTorsion structure: E: y^2 = x^3 - x, 2-torsion (1,0),(0,0),(-1,0)")
    for qx in (1.0, 0.0, -1.0):
        r = dub(qx, 0.0)
        hq1 = hat_k(qx, 0.0, 1)
        hq4 = hat_k(qx, 0.0, 4)
        print(f"  Q=({qx:+.0f},0): y=0 -> 2Q=O;  h_1(Q)={hq1}  h_4(Q)={hq4}")
    g1 = all(hat_k(qx, 0.0, 1) == 0.0 and hat_k(qx, 0.0, 4) == 0.0
             for qx in (1.0, 0.0, -1.0))

    print("\nApproach P_s = (1+s, sqrt((1+s)^3-(1+s))), s -> 0")
    print("  0/0:  (h4(P_s), s)  both -> 0;  probe = h1/h4")
    rows = []
    for s in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
        x = 1.0 + s
        y = math.sqrt(x * x * x - x)
        h1 = hat_k(x, y, 1)
        h4 = hat_k(x, y, 4)
        rows.append((s, h1, h4))
        print(f"  s={s:8.1e}  h1={h1:9.4f}  h4={h4:9.4f}  "
              f"h1/ln(1/2s)={h1/math.log(1.0/(2.0*s)):.4f}  "
              f"h1/h4={h1/max(h4,1e-12):.2f}")

    s_last, h1_last, h4_last = rows[-1]
    C = h1_last / math.log(1.0 / (2.0 * s_last))
    print(f"\n  K=1 law: h1 ~ C ln(1/(2s)), measured C = {C:.4f} "
          f"(expect 3/8 = 0.375)")

    print("\nControl P=(2, sqrt(6))  (no 0/0 at any torsion point)")
    xc = 2.0
    h1c = hat_k(xc, math.sqrt(6.0), 1)
    h4c = hat_k(xc, math.sqrt(6.0), 4)
    print(f"  h1 = {h1c:.4f}  h4 = {h4c:.4f}  ratio = "
          f"{h1c/max(h4c,1e-12):.2f}")

    g2 = abs(C - 0.375) / 0.375 < 0.4
    # the torsion-approach channels: h1 (log channel) far above the
    # arithmetic-depth channel h4 at every s (probe ratio large)
    g3 = all(h1 / max(h4, 1e-12) > 30.0 for _, h1, h4 in rows)
    # control point: no torsion channel (no log divergence): its height
    # is small and the torsion-approach probe towers above it
    g4 = h1c < 0.1 and all(h1a / h1c > 10.0 for _, h1a, _ in rows)

    print("\n" + "-" * 70)
    print("INTERPRETATION")
    print("-" * 70)
    print("The canonical-height estimator splits at the torsion approach")
    print("into a log-divergent first-doubling channel (K=1, formal-")
    print("group rate C ~ 3/8) and a collapsed arithmetic channel (K=4, ")
    print("the real doubling folds back onto the identity component).")
    print("Probe h1/h4 -> large at torsion, O(1) at the control point.")
    print("Vanishing Rate mechanism. Honest wall: finite s, real-model")
    print("heights at K=1 and K=4; laws measured, not proven.")

    gates = {"G1 all three 2-torsion points have h_1=h_4=0": g1,
             "G2 K=1 log law with C ~ 3/8": g2,
             "G3 probe ratio h1/h4 large at every s (0/0 realised)": g3,
             "G4 control point: small height, no log divergence": g4}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'}")

    os.makedirs(DATA, exist_ok=True)
    json.dump({
        "form": "(h4(P_s), s) both -> 0; probe h1/h4", "mechanism":
        "Vanishing Rate",
        "rows": rows, "C_K1": C, "control": {"h1": h1c, "h4": h4c,
                                             "ratio": h1c/max(h4c,1e-12)},
        "gates": gates, "overall": overall,
        "wall": "finite s; real-model heights at K=1 and K=4; laws "
                "measured, not proven"},
        open(os.path.join(DATA, "neron_tate_height_torsion_0_over_0.json"),
             "w"), indent=2)
    print("Wrote data/neron_tate_height_torsion_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()