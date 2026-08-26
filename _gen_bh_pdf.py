#!/usr/bin/env python3
"""Generate PDF for black hole information paper."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sigma_venv'))

from fpdf import FPDF

class BlackHolePDF(FPDF):
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

pdf = BlackHolePDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Title
pdf.add_page()
pdf.ln(15)
pdf.title_text('Black Hole Information Paradox:')
pdf.title_text('0/0 at the Event Horizon')
pdf.ln(8)
pdf.set_font('Helvetica', '', 11)
pdf.cell(0, 7, 'Michael Grafiel S Puno', 0, 1, 'C')
pdf.cell(0, 7, 'L.O.R.E. Framework', 0, 1, 'C')
pdf.cell(0, 7, 'August 2026', 0, 1, 'C')

# Abstract
pdf.add_page()
pdf.chapter_title('Abstract')
pdf.body_text(
    'We show that the black hole information paradox has a 0/0 removable '
    'singularity structure at the event horizon. At the horizon, information '
    'inside = 0 and information outside = infinity, giving 0/0. The removable '
    'value is the Bekenstein-Hawking entropy S_BH = A/(4l_Planck^2). This '
    'connects to the Toomre Q parameter (Q=1 at horizon, beta=1/2), the '
    'holographic principle (information ~ area), and the Page curve '
    '(information recovery at t_Page).'
)

# Section 1
pdf.chapter_title('1. Introduction')
pdf.body_text(
    'The black hole information paradox (Hawking 1975) asks: what happens to '
    'information that falls into a black hole? Hawking radiation appears to '
    'destroy information, violating quantum unitarity. We show that the '
    'paradox has a 0/0 removable singularity structure at the event horizon.'
)

# Section 2
pdf.chapter_title('2. The 0/0 at the Event Horizon')
pdf.body_text('At the event horizon (r = r_s):')
pdf.bullet('Information inside: I = 0 (nothing escapes)')
pdf.bullet('Information outside: I = infinity (all information)')
pdf.bullet('0/0: I_inside / I_outside = 0 / infinity = 0')
pdf.ln(2)
pdf.formula('Removable value: S_BH = A / (4 * l_Planck^2)')
pdf.body_text(
    'This is the Bekenstein-Hawking entropy. The event horizon is a 0/0 '
    'removable singularity in the space of quantum information.'
)

# Section 3
pdf.chapter_title('3. Bekenstein-Hawking Entropy')
pdf.formula('S_BH = k_B * A / (4 * l_Planck^2)')
pdf.body_text(
    'For a solar mass black hole: S_BH/k_B ~ 10^77. '
    'For Sgr A*: S_BH/k_B ~ 10^90. '
    'For M87*: S_BH/k_B ~ 10^104.'
)

# Section 4
pdf.chapter_title('4. Page Curve')
pdf.body_text(
    'The Page curve describes information recovery during evaporation:'
)
pdf.bullet('t = 0: I = 0 (no radiation)')
pdf.bullet('t = t_Page: I = S_BH (Page time)')
pdf.bullet('t = t_evap: I = S_BH (all information recovered)')
pdf.ln(2)
pdf.body_text(
    'The 0/0: I(t_Page) = S_BH/1 = S_BH (removable). '
    'The Page time is when the radiation entropy equals S_BH/2.'
)

# Section 5
pdf.chapter_title('5. Holographic Principle')
pdf.formula('Maximum information = Area / (4 * l_Planck^2)')
pdf.body_text(
    'The holographic principle states that the maximum information in a '
    'region is proportional to its AREA, not its VOLUME. This is '
    'MATHEMATICALLY EQUIVALENT to the Bekenstein-Hawking entropy.'
)
pdf.body_text(
    'Connection to Toomre Q: stability depends on SURFACE density, not '
    'volume density. Same 0/0 structure!'
)

# Section 6
pdf.chapter_title('6. Connection to Toomre Q')
pdf.body_text(
    'The event horizon is a gravitational instability:'
)
pdf.bullet('Q < 1: unstable (horizon forms)')
pdf.bullet('Q > 1: stable (no horizon)')
pdf.bullet('Q = 1: marginal (0/0 removable singularity)')
pdf.ln(2)
pdf.formula('Q ~ (r - r_s)^(1/2), beta = 1/2 (mean-field Ising)')
pdf.body_text(
    'The critical exponent beta = 1/2 is the SAME as Toomre Q at Q = 1.'
)

# Section 7
pdf.chapter_title('7. Main Results')
pdf.theorem(
    'Horizon 0/0: I_inside/I_outside = 0/infinity = 0, removable value '
    'S_BH = A/(4l_Planck^2).'
)
pdf.theorem(
    'Page Curve: I(t_Page) = S_BH (information recovery), 0/0 at t_Page.'
)
pdf.theorem(
    'Holographic: S = A/(4l_Planck^2) = 0/0 at horizon, removable S_BH.'
)

# Section 8
pdf.chapter_title('8. Conclusion')
pdf.body_text(
    'The black hole information paradox has a 0/0 removable singularity '
    'structure at the event horizon. The removable value is the '
    'Bekenstein-Hawking entropy. This connects to the Toomre Q parameter '
    '(Q=1 at horizon), the holographic principle (information ~ area), '
    'and the Page curve (information recovery).'
)

# References
pdf.chapter_title('References')
refs = [
    "[1] Bekenstein (1973). Phys. Rev. D 7, 2333.",
    "[2] Hawking (1975). Comm. Math. Phys. 43, 199.",
    "[3] Page (1993). Phys. Rev. Lett. 71, 1291.",
    "[4] Maldacena (1998). Adv. Theor. Math. Phys. 2, 231.",
    "[5] Penington (2020). JHEP 2020, 20.",
    "[6] Almheiri et al. (2021). Rev. Mod. Phys. 93, 35002.",
    "[7] Toomre (1964). ApJ 139, 1217.",
    "[8] Puno (2026). The Removable Singularity.",
]
for ref in refs:
    pdf.bullet(ref)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'papers', 'black_hole_info.pdf')
pdf.output(output_path)
print("PDF saved to: %s" % output_path)
print("Pages: %d" % pdf.page_no())
