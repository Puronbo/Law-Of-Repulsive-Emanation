"""
3D critical surface of f(R) gravity.
From Codello et al (arXiv:0705.1769), eq.11.
"""
import math

# FP values (n=6 truncation, table from 0705.1769)
g0_star = 0.00505
g1_star = -0.0208
g2_star = 0.00014

# Critical surface coefficients (eq.11)
cs = {
    3: ( 0.00127,  0.190,  0.607,  1.265),
    4: (-0.00646, -0.732, -0.0156, 1.880),
    5: (-0.0155,  -1.132, -0.846,  0.276),
    6: (-0.0137,  -0.594, -0.932, -1.283),
}

print("=" * 70)
print("THE 3D CRITICAL SURFACE AND TRAJECTORY SELECTION")
print("=" * 70)
print()
print("From Codello et al (arXiv:0705.1769, arXiv:0805.2909):")
print("The UV critical surface of f(R) gravity is 3-dimensional.")
print("The irrelevant couplings g3-g6 are linear functions of g0,g1,g2.")
print()

# Verify FP values on critical surface
print("VERIFICATION: FP on critical surface")
print("-" * 50)
for i in range(3, 7):
    a, b0, b1, b2 = cs[i]
    gi = a + b0 * g0_star + b1 * g1_star + b2 * g2_star
    print("  g%d = %.5f (linear approx)" % (i, gi))

print()
print("Table 1 values (n=6):")
print("  g3 = -0.0102, g4 = -0.00957, g5 = -0.00359, g6 = 0.00246")
print()

# Map to EH parameters
# f(R) = g0 + g1*R + g2*R^2 + ...
# Near FP: g1 = -Z = -1/(16pi*G), g0 = 2*Lambda*Z
# So G = -1/(16*pi*g1), Lambda = g0/(-2*g1)
G_tilde = -1.0 / (16 * math.pi * g1_star)
L_tilde = -g0_star / (2 * g1_star)
LG = G_tilde * L_tilde

print("MAPPING TO EH PARAMETERS")
print("-" * 50)
print("  g1* = %.5f  =>  G~* = -1/(16*pi*g1) = %.4f" % (g1_star, G_tilde))
print("  g0* = %.5f  =>  L~* = -g0/(2*g1) = %.4f" % (g0_star, L_tilde))
print("  G~* x L~* = %.4f" % LG)
print("  Table III: G~*=0.949, L~*=0.120, G~*xL~*=0.114")
print()

# Key insight: the critical surface is a 3D PLANE in 7D coupling space
# Trajectories on this plane have g3-g6 determined by g0,g1,g2.
# The trajectory is SELECTED by choosing initial (g0,g1,g2) at some UV scale.
# Matching to low energy (G_N, Lambda_obs) fixes 2 of 3 parameters.
# The 3rd parameter (g2, the R^2 coupling) is free -- this is the
# trajectory selection freedom in the f(R) truncation.

print("=" * 70)
print("TRAJECTORY SELECTION IN f(R) GRAVITY")
print("=" * 70)
print()
print("The 3D critical surface means:")
print("  - 3 free parameters at the UV fixed point")
print("  - Matching to G_N and Lambda_obs fixes 2 of 3")
print("  - The 3rd parameter (g2, R^2 coupling) is OBSERVATIONALLY FREE")
print()
print("This is the f(R) version of the CC problem:")
print("  The framework PREDICTS the UV structure (FP, critical exponents,")
print("  critical surface). The IR values depend on trajectory selection")
print("  within the 3-parameter family.")
print()

# What matters for suppression
print("WHAT MATTERS FOR THE G~xL~ SUPPRESSION")
print("-" * 50)
print()
print("The product G~xL~ = G~(k) x L~(k) along the flow:")
print()
print("  At the FP: G~* x L~* = 0.12 (any truncation)")
print("  At the IR: G_obs x L_obs = 2.77e-122")
print("  Required suppression: 4e120")
print()
print("The R^2 coupling (g2) provides an EXTRA degree of freedom")
print("that the EH truncation lacks. In the EH truncation:")
print("  - Only 2 directions (G, L)")
print("  - Product plateaus at 10^-4")
print("  - Cannot reach 10^-122")
print()
print("In the f(R) truncation:")
print("  - 3 directions (G, L, g2)")
print("  - g2 can carry energy away from the G-L product")
print("  - The R^2 term modifies the beta functions of G and L")
print("  - This COULD provide additional suppression")
print()
print("But we cannot compute this without the explicit beta functions.")
print()

# The honest state
print("=" * 70)
print("HONEST STATEMENT")
print("=" * 70)
print()
print("What we KNOW:")
print("  1. The UV FP exists with G~*xL~* = 0.12 (scheme-independent)")
print("  2. The critical surface is 3D (3 free parameters)")
print("  3. The EH truncation achieves 3/121 orders of suppression")
print("  4. The f(R) critical surface provides the STRUCTURE for")
print("     additional suppression via the R^2 coupling")
print()
print("What we CANNOT compute:")
print("  1. The explicit f(R) beta functions (CAS-derived, not published)")
print("  2. The full nonlinear trajectory from UV to IR")
print("  3. Whether g2 provides the remaining 118 orders of suppression")
print()
print("What would resolve the problem:")
print("  1. Re-derive f(R) beta functions using a CAS (Mathematica/SageMath)")
print("     The method is clear: Wetterich eq + heat kernel + optimized cutoff")
print("     Codello 2009 eq.(119) describes the procedure")
print("  2. Integrate the 3D flow on the critical surface from UV to IR")
print("  3. Compute G~xL~ along the trajectory and check suppression")
print()
print("This is a concrete, well-defined CAS project:")
print("  Input: Wetterich equation (eq.1) + f(R) truncation (eq.6)")
print("  Method: Heat kernel expansion (eq.124) + optimized cutoff")
print("  Output: beta_0(g0..g6), beta_1(g0..g6), beta_2(g0..g6)")
print("  Then: substitute critical surface (eq.11) to get 3D flow")
print("  Then: integrate and compute G~xL~ along trajectory")
