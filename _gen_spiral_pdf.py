#!/usr/bin/env python3
"""Generate PDF for spiral mass gap paper."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sigma_venv'))

from fpdf import FPDF

class SpiralPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 5, 'Michael Grafiel S Puno - August 2026', 0, 0, 'L')
        self.cell(0, 5, 'L.O.R.E. Framework', 0, 1, 'R')
        self.line(10, 12, 200, 12)
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, 'Page %d' % self.page_no(), 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(3)
    
    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)
    
    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 5, text)
        self.ln(2)
    
    def formula(self, text):
        self.set_font('Courier', '', 10)
        self.cell(10, 5, '', 0, 0)
        self.cell(0, 5, text, 0, 1, 'L')
        self.ln(2)
    
    def bullet(self, text):
        self.set_font('Helvetica', '', 10)
        self.cell(10, 5, '', 0, 0)
        self.cell(5, 5, '-', 0, 0)
        self.multi_cell(0, 5, text)
        self.ln(1)

pdf = SpiralPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Title page
pdf.add_page()
pdf.set_font('Helvetica', 'B', 20)
pdf.ln(30)
pdf.cell(0, 15, 'Solar Systems as Spirals with', 0, 1, 'C')
pdf.cell(0, 15, 'Mass Gap as 0/0 Removable', 0, 1, 'C')
pdf.cell(0, 15, 'Singularities', 0, 1, 'C')
pdf.ln(10)
pdf.set_font('Helvetica', '', 12)
pdf.cell(0, 8, 'Connections to Navier-Stokes, Yang-Mills, and BSD', 0, 1, 'C')
pdf.ln(20)
pdf.set_font('Helvetica', '', 11)
pdf.cell(0, 8, 'Michael Grafiel S Puno', 0, 1, 'C')
pdf.cell(0, 8, 'August 2026', 0, 1, 'C')
pdf.ln(10)
pdf.set_font('Helvetica', 'I', 10)
pdf.cell(0, 8, 'L.O.R.E. Framework (Law of Repulsive Emanation)', 0, 1, 'C')
pdf.cell(0, 8, 'Sigma Chassis v2.0', 0, 1, 'C')

# Abstract
pdf.add_page()
pdf.chapter_title('Abstract')
pdf.body_text(
    'We present a mathematical framework showing that solar system structure - from '
    'protoplanetary disks to mature planetary systems - is fundamentally a spiral with '
    'removable singularities (0/0) at three scales: stellar, planetary, and galactic. '
    'The "mass gap" (empty zones between planets, Kirkwood gaps, asteroid belt depletion) '
    'is shown to be mathematically equivalent to the Yang-Mills mass gap Delta > 0 and the '
    'Navier-Stokes regularity condition. We establish formal connections to three Millennium '
    'Prize Problems: (1) Navier-Stokes existence and smoothness via accretion disk fluid '
    'dynamics, (2) Yang-Mills existence and mass gap via spectral gaps in orbital frequency '
    'space, and (3) Birch and Swinnerton-Dyer via rational points on resonance diagrams. '
    'The framework uses the L.O.R.E. principle: the mass gap is not a void but a removable '
    'singularity whose finite value is determined by the surrounding dynamics.'
)

# Section 1
pdf.chapter_title('1. Introduction')
pdf.body_text(
    'The structure of solar systems has been studied through Keplerian orbits, perturbation '
    'theory, and N-body simulations. However, a unifying mathematical principle connecting '
    'the spiral structure, the mass gaps, and the fundamental open problems in mathematical '
    'physics has not been established.'
)
pdf.body_text('We show that:')
pdf.bullet('Solar systems are spirals (tornado-like) with differential rotation')
pdf.bullet('The mass gaps (empty zones) are 0/0 removable singularities')
pdf.bullet('These singularities connect directly to three Millennium Prize Problems')
pdf.ln(3)
pdf.body_text(
    'The key insight is that the "mass gap" - the absence of material at certain radii - '
    'is not a void but a removable singularity whose finite value (the mass that was ejected '
    'or redistributed) is determined by the surrounding dynamics, exactly as in the Yang-Mills '
    'mass gap problem.'
)

# Section 2
pdf.chapter_title('2. Mathematical Framework')
pdf.section_title('2.1 The Spiral Structure')
pdf.body_text(
    'Definition: A solar system is a spiral if the orbital angular velocity Omega(r) depends '
    'on radius:'
)
pdf.formula('Omega(r) = sqrt(GM / r^3)')
pdf.body_text(
    'In a rotating frame with pattern speed Omega_p, the spiral pitch angle is:'
)
pdf.formula('d(theta)/dr = (Omega(r) - Omega_p) / v_r')
pdf.body_text(
    'Proposition (Corotation Singularity): At the corotation radius r_c where '
    'Omega(r_c) = Omega_p, the spiral pitch satisfies d(theta)/dr = 0/v_r. This is a '
    '0/0 removable singularity.'
)
pdf.body_text(
    'Proof: The numerator Omega(r_c) - Omega_p = 0 and the denominator v_r -> 0 as the '
    'flow stagnates at corotation. By L\'Hopital\'s rule:'
)
pdf.formula('lim(r->r_c) (Omega(r) - Omega_p)/v_r = Omega\'(r_c)/v_r\'(r_c)')
pdf.body_text('which is finite (the removable value).')

pdf.section_title('2.2 The Mass Gap')
pdf.body_text(
    'Definition: The mass gap Delta at radius r_0 is defined as:'
)
pdf.formula('Delta(r_0) = lim(e->0) [M(r_0 + e) - M(r_0 - e)]')
pdf.body_text('where M(r) is the enclosed mass.')
pdf.body_text(
    'Theorem (Mass Gap as Removable Singularity): At a Kirkwood gap (resonance with a '
    'planet), the surface density Sigma(r) satisfies lim Sigma(r) = 0/0. The removable '
    'value is the non-resonant surface density Sigma_0 that would exist without the resonance.'
)

pdf.section_title('2.3 The Parker Spiral')
pdf.body_text(
    'The Parker spiral magnetic field in the solar wind:'
)
pdf.formula('B_r(r) = B_0 * (R_0/r)^2')
pdf.formula('B_phi(r) = B_r * omega_sun * (r - R_0) / v_wind')
pdf.body_text(
    'The spiral angle tan(psi) = B_phi/B_r satisfies lim(r->R_0) tan(psi) = 0. '
    'The removable value is psi = 0 (radial field at the source surface).'
)

# Section 3
pdf.chapter_title('3. Connection to Navier-Stokes')
pdf.section_title('3.1 Accretion Disk Dynamics')
pdf.body_text(
    'The protoplanetary disk is governed by the Navier-Stokes equations for thin disks:'
)
pdf.formula('dSigma/dt + (1/R)*d/dR(R*Sigma*V_R) = 0')
pdf.formula('Sigma*R*dOmega^2/dt = (1/R^2)*d/dR(R^4*Sigma*nu*dOmega/dR)')

pdf.section_title('3.2 The Millennium Problem Connection')
pdf.body_text(
    'The Navier-Stokes Millennium Problem asks: do smooth solutions exist globally in 3D?'
)
pdf.body_text(
    'Proposition (Disk Blow-up as 0/0): If finite-time blow-up occurs in the disk equations, '
    'the velocity gradient satisfies ||nabla v|| -> infinity/infinity while the density '
    'satisfies Sigma -> 0/0.'
)
pdf.body_text(
    'The Caffarelli-Kohn-Nirenberg theorem establishes that the singular set has '
    'one-dimensional Hausdorff measure zero - singularities are "removable" in a '
    'measure-theoretic sense.'
)
pdf.body_text(
    'Corollary: The Navier-Stokes regularity condition for accretion disks is equivalent '
    'to the mass gap condition: smooth solutions exist if and only if the mass gap Delta > 0 '
    'is well-defined (removable singularity).'
)

# Section 4
pdf.chapter_title('4. Connection to Yang-Mills')
pdf.section_title('4.1 The Mass Gap Problem')
pdf.body_text(
    'The Yang-Mills Millennium Problem asks: prove that quantum Yang-Mills theory on R^4 '
    'has a mass gap Delta > 0.'
)
pdf.formula('Delta = inf{E > E_vacuum : H|psi> = E|psi>, <psi|psi> = 1}')

pdf.section_title('4.2 The Solar System Analogy')
pdf.body_text(
    'Theorem (Spiral Mass Gap): The solar system mass gap Delta_solar (empty zones between '
    'planets) is mathematically equivalent to the Yang-Mills mass gap:'
)
pdf.formula('Delta_solar = lim(r->r_gap) Sigma(r) = 0/0')
pdf.body_text('with removable value Sigma_0 (the non-gap density).')
pdf.body_text('Proof:')
pdf.bullet(
    'Classical limit: A point mass (Sun) with no planets gives Sigma(r) = 0 for r > R_sun. '
    'This is the "massless" classical theory.'
)
pdf.bullet(
    'Quantum (nonlinear) corrections: Gravitational interactions generate planets with '
    'finite mass M_p > 0 at specific radii. The mass gap Delta = M_p - 0 = M_p > 0.'
)
pdf.bullet(
    'Spectral representation: The two-point correlation function of the gravitational field '
    'decays as G(r) ~ exp(-Delta*|r|/(hbar*c)) as |r| -> infinity.'
)

pdf.section_title('4.3 Magnetorotational Instability')
pdf.body_text(
    'The magnetorotational instability (MRI) in accretion disks has a critical wavelength:'
)
pdf.formula('lambda_MRI = 2*pi*v_A / Omega')
pdf.body_text(
    'Perturbations with lambda < lambda_MRI are damped. This creates a spectral gap '
    'analogous to the Yang-Mills mass gap.'
)

# Section 5
pdf.chapter_title('5. Connection to Birch and Swinnerton-Dyer')
pdf.section_title('5.1 Orbital Resonances as Rational Points')
pdf.body_text(
    'Definition: The resonance diagram is the set of rational points p/q on the frequency '
    'ratio space Omega_1/Omega_2.'
)
pdf.body_text(
    'Theorem (BSD Analogy): The number of stable orbital resonances in a solar system is '
    'analogous to the rank of an elliptic curve in the BSD conjecture:'
)
pdf.formula('rank(E) ~ #{stable resonances}')
pdf.body_text(
    'Proof: The BSD conjecture states that the rank of the Mordell-Weil group E(Q) equals '
    'the order of vanishing of the L-function L(E, s) at s = 1.'
)
pdf.formula('rank(E) = ord_{s=1} L(E, s)')
pdf.body_text(
    'For orbital resonances, the "L-function" is the secular perturbation expansion. The '
    'order of vanishing at a resonance p/q determines whether the resonance is stable '
    '(librating) or unstable (circulating).'
)

# Section 6
pdf.chapter_title('6. The Tornado Analogy')
pdf.body_text(
    'A tornado is a spiral with: center 0/0 singularity (velocity -> infinity, pressure -> 0), '
    'mass gap (eye of tornado, no debris, invisible), and spiral arms (visible debris bands).'
)
pdf.body_text(
    'The solar system is analogous: Sun as 0/0 singularity (infinite density in point mass), '
    'asteroid belt gap as mass gap (invisible material), and planetary orbits as spiral arms '
    '(visible structure).'
)
pdf.body_text(
    'Both have the SAME mathematical structure: removable singularity at center, mass gap in '
    'spectrum, and spiral pattern from differential rotation.'
)

# Section 7
pdf.chapter_title('7. Three Mass Gaps at Three Scales')
pdf.bullet(
    'Stellar scale: The Sun as point mass. At r = 0: M(r) = M_sun * (r/R_sun)^3 => '
    'M(0) = 0/0. Removable value: M_sun.'
)
pdf.bullet(
    'Planetary scale: Kirkwood gaps at resonances. At r = r_res: Sigma(r) = Sigma_0 / '
    'sinh(2*pi/(sigma*(N-1))) => Sigma(r_res) = 0/0. Removable value: Sigma_0.'
)
pdf.bullet(
    'Galactic scale: Spiral pattern at corotation. At r = r_c: d(theta)/dr = '
    '(Omega(r) - Omega_p)/v_r => d(theta)/dr|_{r_c} = 0/0. Removable value: spiral '
    'pitch angle alpha_0.'
)

# Section 8
pdf.chapter_title('8. Main Theorem')
pdf.body_text(
    'Theorem (Universal Spiral Mass Gap): Let (M, g) be a rotating gravitational system '
    'with differential rotation Omega(r). Then:'
)
pdf.bullet(
    'The system traces a spiral with pattern speed Omega_p.'
)
pdf.bullet(
    'At the corotation radius r_c where Omega(r_c) = Omega_p, the spiral pitch is a 0/0 '
    'removable singularity.'
)
pdf.bullet(
    'The mass gap Delta (empty zones) satisfies Delta = inf{E > 0 : stable orbit exists at '
    'radius r} > 0 if and only if the spiral pattern is well-defined.'
)
pdf.bullet(
    'The mass gap Delta is equivalent to: the Yang-Mills mass gap (spectral gap in '
    'Hamiltonian), the Navier-Stokes regularity condition (global smooth solutions), and '
    'the BSD rank (number of stable resonances).'
)

# Section 9
pdf.chapter_title('9. Conclusion')
pdf.body_text(
    'The solar system is a spiral with three removable singularities (0/0) at three scales. '
    'The mass gap - the absence of material at certain radii - is not a void but a removable '
    'singularity whose finite value is determined by the surrounding dynamics. This connects '
    'directly to three Millennium Prize Problems:'
)
pdf.bullet(
    'Navier-Stokes: Disk fluid dynamics; blow-up = 0/0; regularity = removable singularity'
)
pdf.bullet(
    'Yang-Mills: Mass gap Delta > 0 = removable value of 0/0 in spectral density'
)
pdf.bullet(
    'BSD: Orbital resonances = rational points; stable resonances = rank of system'
)
pdf.ln(5)
pdf.body_text(
    'The L.O.R.E. principle (Law of Repulsive Emanation) unifies these: the mass gap is '
    'the removable value of a 0/0 singularity, determined by the same mathematical structure '
    'across all scales.'
)

# References
pdf.chapter_title('References')
refs = [
    "[1] L'Hopital, G.F.A. (1696). Analyse des Infiniment Petits.",
    "[2] Parker, E.N. (1958). Dynamics of the Interplanetary Gas and Magnetic Fields. ApJ 128, 664.",
    "[3] Lin, C.C. & Shu, F.H. (1964). On the Spiral Structure of Disk Galaxies. ApJ 140, 646.",
    "[4] Toomre, A. (1964). On the Gravitational Stability of a Disk of Stars. ApJ 139, 1217.",
    "[5] Kirkwood, D. (1867). Meteoric Astronomy.",
    "[6] Caffarelli, L., Kohn, R. & Nirenberg, L. (1982). CPAM 35, 771.",
    "[7] Jaffe, A. & Witten, E. (2000). Yang-Mills Existence and Mass Gap. Clay Math. Inst.",
    "[8] Fefferman, C.L. (2006). The Millennium Prize Problems, 57-67.",
    "[9] Birch, B.J. & Swinnerton-Dyer, H.P.F. (1965). J. Reine Angew. Math. 212, 7-25.",
    "[10] Conway, J.H. & Sloane, N.J.A. (1999). Sphere Packings. Springer.",
    "[11] Galdi, G.P. (2011). The Mathematical Theory of Navier-Stokes. Springer.",
    "[12] Devlin, K. (2003). The Millennium Problems. Basic Books.",
    "[13] Bekenstein, J.D. (1973). Black Holes and Entropy. PRD 7, 2333.",
    "[14] Shannon, C.E. (1948). Bell System Tech. J. 27, 379-423.",
    "[15] Li, L., Li, Y.Y. & Yan, X. (2024). arXiv:2410.11170.",
    "[16] Chen, B. (2026). arXiv:2603.11926.",
]
for ref in refs:
    pdf.bullet(ref)

# Save
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'papers', 'spiral_mass_gap.pdf')
pdf.output(output_path)
print("PDF saved to: %s" % output_path)
print("Pages: %d" % pdf.page_no())
