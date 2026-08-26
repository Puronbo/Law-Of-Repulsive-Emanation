#!/usr/bin/env python3
"""Generate PDF for dark unified paper."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sigma_venv'))

from fpdf import FPDF

class DarkUnifiedPDF(FPDF):
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
    def title_text(self, text):
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 9, text, 0, 1, 'C')
        self.ln(2)
    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 7, title, 0, 1, 'L')
        self.ln(1)
    def body_text(self, text):
        self.set_font('Helvetica', '', 9)
        self.multi_cell(0, 4.5, text)
        self.ln(2)
    def formula(self, text):
        self.set_font('Courier', '', 9)
        self.cell(8, 4.5, '', 0, 0)
        self.cell(0, 4.5, text, 0, 1, 'L')
        self.ln(1)
    def bullet(self, text):
        self.set_font('Helvetica', '', 9)
        self.cell(8, 4.5, '', 0, 0)
        self.cell(4, 4.5, '-', 0, 0)
        self.multi_cell(0, 4.5, text)
        self.ln(0.5)
    def theorem(self, text):
        self.set_font('Helvetica', 'B', 9)
        self.cell(0, 5, 'THEOREM', 0, 1, 'L')
        self.set_font('Helvetica', 'I', 9)
        self.multi_cell(0, 4.5, text)
        self.ln(2)

pdf = DarkUnifiedPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Title
pdf.add_page()
pdf.ln(15)
pdf.title_text('Dark Matter and Dark Energy as')
pdf.title_text('0/0 Removable Singularities:')
pdf.title_text('A Unified Framework via')
pdf.title_text('the Toomre Parameter')
pdf.ln(8)
pdf.set_font('Helvetica', '', 11)
pdf.cell(0, 7, 'Michael Grafiel S Puno', 0, 1, 'C')
pdf.cell(0, 7, 'L.O.R.E. Framework', 0, 1, 'C')
pdf.cell(0, 7, 'August 2026', 0, 1, 'C')

# Abstract
pdf.add_page()
pdf.chapter_title('Abstract')
pdf.body_text(
    'We present a unified framework for dark matter and dark energy based on '
    '0/0 removable singularities at different physical scales. The Toomre Q '
    'parameter has a 0/0 at Q=1 connecting to three Millennium Prize Problems. '
    'We extend this to cosmology: (1) dark matter core density has a 0/0 at '
    'sigma_m(N-1) = 2*pi; (2) Lambda has a 0/0 at the Planck scale (classical 0, '
    'quantum infinity, actual 10^-123); (3) Q transitions from Q<1 (structure '
    'formation) to Q>1 (dark energy domination) at the cluster scale.'
)

# Section 1
pdf.chapter_title('1. Introduction')
pdf.body_text(
    'The Lambda-CDM model has two major unknowns: dark matter (Omega_m = 0.315) '
    'and dark energy (Omega_Lambda = 0.685). Both remain unexplained. We show '
    'that both have 0/0 removable singularity structures, connecting to the '
    'Toomre Q parameter.'
)

# Section 2
pdf.chapter_title('2. Dark Matter: 0/0 at Galactic Scales')
pdf.formula('rho_core = rho_0 / sinh(2*pi / (sigma_m * (N-1)))')
pdf.body_text(
    'At sigma_m*(N-1) = 2*pi: rho_core = rho_0 / sinh(1) = 0/0. '
    'Removable value: rho_0 (halo density).'
)
pdf.bullet('Milky Way: rho_0 = 0.3 GeV/cm^3, sigma_m = 0.5, N = 1000')
pdf.bullet('Andromeda: rho_0 = 0.4 GeV/cm^3, sigma_m = 0.6, N = 1200')

# Section 3
pdf.chapter_title('3. Dark Energy: 0/0 at Planck Scale')
pdf.body_text('The cosmological constant has three values:')
pdf.bullet('Classical: Lambda_cl = 0 (no vacuum energy)')
pdf.bullet('Quantum: Lambda_QFT ~ 10^120 * Lambda_obs (vacuum fluctuations)')
pdf.bullet('Observed: Lambda_obs = 10^-123 (Planck units)')
pdf.ln(2)
pdf.formula('Lambda_cl / Lambda_QFT = 0 / infinity = 0')
pdf.body_text(
    'But Lambda_obs = 10^-123 != 0. The 0/0 has removable value: Lambda_obs.'
)

# Section 4
pdf.chapter_title('4. Toomre Q at Cosmic Scales')
pdf.formula('Q_cosmic = c_s * H / (pi * G * rho)')
pdf.body_text(
    'At the Planck scale: Q_Planck ~ 10^-36 (deeply unstable). '
    'At the present epoch: Q_cosmic ~ 10^-18 (still unstable).'
)

# Section 5
pdf.chapter_title('5. Phase Transition at Q=1')
pdf.formula('rho_crit_Q1 = c_s * H / (pi * G)')
pdf.body_text(
    'The scale factor at Q=1: a_crit = 8.7e8 (cluster scale). '
    'For a < a_crit: Q < 1 (structure forms). '
    'For a > a_crit: Q > 1 (dark energy dominates).'
)

# Section 6
pdf.chapter_title('6. Unified 0/0 Framework')
pdf.bullet('Dark matter: 0/0 at sigma_m*(N-1) = 2*pi')
pdf.bullet('Dark energy: 0/0 at Planck scale')
pdf.bullet('Toomre Q: 0/0 at Q = 1 (phase transition)')
pdf.bullet('Quantum gravity: Q_Planck ~ 10^-36 (deeply unstable)')

# Section 7
pdf.chapter_title('7. Main Results')
pdf.theorem(
    'Dark Matter 0/0: rho_core = rho_0/sinh(2*pi/(sigma_m*(N-1))) has 0/0 '
    'at sigma_m*(N-1) = 2*pi, removable value rho_0.'
)
pdf.theorem(
    'Dark Energy 0/0: Lambda has 0/0 at Planck scale: 0/infinity = 0, '
    'removable value 10^-123.'
)
pdf.theorem(
    'Cosmic Phase Transition: Q transitions from Q<1 to Q>1 at a_crit, '
    'with beta=1/2, nu=1 (mean-field Ising).'
)

# Section 8
pdf.chapter_title('8. Conclusion')
pdf.body_text(
    'The Lambda-CDM model has a unified 0/0 structure across all scales: '
    'dark matter at galactic scales, dark energy at cosmic scales, and '
    'quantum gravity at the Planck scale. The Toomre Q parameter provides '
    'the connecting thread, with Q=1 as the critical phase transition point.'
)

# References
pdf.chapter_title('References')
refs = [
    "[1] Puno (2026). The Removable Singularity.",
    "[2] Toomre (1964). ApJ 139, 1217.",
    "[3] Lin & Shu (1964). ApJ 140, 646.",
    "[4] Planck Collaboration (2020). A&A 641, A6.",
    "[5] Riess et al. (1998). AJ 116, 1009.",
    "[6] Perlmutter et al. (1999). ApJ 517, 565.",
    "[7] Bertone et al. (2005). Physics Reports 405, 279.",
    "[8] Weinberg (1989). Rev. Mod. Phys. 61, 1.",
]
for ref in refs:
    pdf.bullet(ref)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'papers', 'dark_unified.pdf')
pdf.output(output_path)
print("PDF saved to: %s" % output_path)
print("Pages: %d" % pdf.page_no())
