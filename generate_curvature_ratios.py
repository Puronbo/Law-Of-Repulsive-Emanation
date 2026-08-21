"""
Generate curvature formula ratios for Curvature.lean.

Verifies the corrected formula F''(1/2) = 2*|xi|^2*L' where L' = sum 1/(t-gn)^2.
Computes F''(1/2) / (2*|xi|^2*L') at several t values away from zeros.

If the corrected formula is right, this ratio should be 1.0 in the limit
of infinitely many zeros. With 100 zeros, it converges rapidly for large t.

Output values are hardcoded into PunoCalculus/PunoCalculus/Curvature.lean.
"""
import mpmath
mpmath.mp.dps = 30

def xi_val(s):
    return (mpmath.mpf(1)/2 * s * (s-1)
            * mpmath.power(mpmath.pi, -s/2)
            * mpmath.gamma(s/2)
            * mpmath.zeta(s))

# First 100 imaginary parts of nontrivial zeta zeros
gn = [float(mpmath.zetazero(k).imag) for k in range(1, 101)]

h = mpmath.mpf('1e-6')

print("t       | F''(1/2) num   | 2*|xi|^2*S     | ratio")
print("--------|----------------|----------------|-------")

for t_val in [10, 20, 50, 100]:
    t = mpmath.mpf(t_val)

    def F(sig):
        s = sig + t*mpmath.mpc(0,1)
        v = xi_val(s)
        return (v * v.conjugate()).real

    sig = mpmath.mpf('0.5')
    F_pp = float((F(sig+h) - 2*F(sig) + F(sig-h)) / h**2)

    s_half = sig + t*mpmath.mpc(0,1)
    xi_at_half = xi_val(s_half)
    abs_xi_sq = float((xi_at_half * xi_at_half.conjugate()).real)

    S = float(sum([(t - mpmath.mpf(str(g)))**(-2) for g in gn]))

    formula = 2.0 * abs_xi_sq * S
    ratio = formula / F_pp if F_pp != 0 else float('inf')

    print(f"t={t_val:<4} | {F_pp:14.6e} | {formula:14.6e} | {ratio:.6f}")

print()
print("These ratios go into Curvature.lean's verifyRatioConverges.")
