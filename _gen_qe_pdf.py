#!/usr/bin/env python3
"""Generate PDF for quantum entanglement paper."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sigma_venv'))

from fpdf import FPDF

class QuantumPDF(FPDF):
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

pdf = QuantumPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Title
pdf.add_page()
pdf.ln(15)
pdf.title_text('Quantum Entanglement:')
pdf.title_text('0/0 at the AdS/CFT Boundary')
pdf.ln(8)
pdf.set_font('Helvetica', '', 11)
pdf.cell(0, 7, 'Michael Grafiel S Puno', 0, 1, 'C')
pdf.cell(0, 7, 'L.O.R.E. Framework', 0, 1, 'C')
pdf.cell(0, 7, 'August 2026', 0, 1, 'C')

# Abstract
pdf.add_page()
pdf.chapter_title('Abstract')
pdf.body_text(
    'We show that quantum entanglement has a 0/0 removable singularity '
    'structure at the AdS/CFT boundary. The Ryu-Takayanagi formula '
    'S_A = Area/(4G_N) gives S_A = 0 in the bulk and infinity on the '
    'boundary, with removable value S_A at the horizon. This connects '
    'to the Toomre Q parameter (Q=1 at horizon, beta=1/2), the '
    'holographic bound (S_max ~ L^{d-1}), and ER=EPR (Einstein-Rosen '
    'bridges = Einstein-Podolsky-Rosen pairs).'
)

# Section 1
pdf.chapter_title('1. Introduction')
pdf.body_text(
    'The Ryu-Takayanagi formula (2006) relates entanglement entropy in '
    'a boundary CFT to the area of a minimal surface in the bulk AdS '
    'space: S_A = Area(gamma_A)/(4G_N). We show this has a 0/0 structure '
    'at the AdS/CFT boundary.'
)

# Section 2
pdf.chapter_title('2. The 0/0 at the Boundary')
pdf.body_text('The Ryu-Takayanagi formula:')
pdf.formula('S_A = Area(gamma_A) / (4 * G_N)')
pdf.bullet('In the bulk (AdS): S_A = 0 (no entanglement)')
pdf.bullet('On the boundary (CFT): S_A = infinity (maximum)')
pdf.bullet('At the boundary (removable): S_A = Area/(4G_N)')
pdf.ln(2)
pdf.body_text(
    'This is a 0/0 REMOVABLE SINGULARITY in the space of quantum '
    'entanglement.'
)

# Section 3
pdf.chapter_title('3. Holographic Bound')
pdf.formula('S_max = L^{d-1} / (4 * G_N)')
pdf.body_text(
    'The holographic bound: maximum entanglement in a region of size L '
    'is proportional to its AREA, not VOLUME. This is the same 0/0 '
    'structure as Ryu-Takayanagi.'
)

# Section 4
pdf.chapter_title('4. Entanglement Wedge')
pdf.body_text(
    'The entanglement wedge is the bulk region reconstructable from '
    'boundary data:'
)
pdf.bullet('r < r_s: wedge = 0 (no reconstruction)')
pdf.bullet('r > r_s: wedge = r - r_s (reconstructable)')
pdf.bullet('r = r_s: 0/0 removable singularity')
pdf.ln(2)
pdf.body_text(
    'At the horizon, the entanglement wedge has a 0/0 removable singularity '
    'with removable value r - r_s.'
)

# Section 5
pdf.chapter_title('5. Connection to Toomre Q')
pdf.body_text(
    'The Ryu-Takayanagi formula is a 0/0 like Toomre Q:'
)
pdf.bullet('Toomre: Q < 1 unstable, Q > 1 stable, Q = 1 marginal (0/0)')
pdf.bullet('RT: S_A = 0 bulk, S_A = inf boundary, S_A = Area/(4G_N) removable')
pdf.ln(2)
pdf.formula('Both have critical exponent beta = 1/2!')
pdf.body_text(
    'Near the horizon: S_A ~ (r - r_s)^(1/2). '
    'Near Q=1: Gamma ~ (1-Q)^(1/2). Same 0/0 structure!'
)

# Section 6
pdf.chapter_title('6. ER = EPR')
pdf.body_text(
    'Maldacena & Susskind (2013): ER = EPR. '
    'Einstein-Rosen bridges = Einstein-Podolsky-Rosen pairs.'
)
pdf.bullet('At the horizon: ER bridge = EPR pair (0/0)')
pdf.bullet('Removable value: S_BH = Area/(4G_N)')
pdf.bullet('Same as Ryu-Takayanagi!')
pdf.ln(2)
pdf.body_text(
    'The ER=EPR conjecture is a 0/0 removable singularity in the space '
    'of quantum geometry.'
)

# Section 7
pdf.chapter_title('7. Main Results')
pdf.theorem(
    'RT 0/0: S_A = Area/(4G_N) = 0/0 at boundary, removable S_A.'
)
pdf.theorem(
    'Holographic Bound: S_max = L^{d-1}/(4G_N) = 0/0, removable S_max.'
)
pdf.theorem(
    'ER=EPR: ER bridge = EPR pair = 0/0 at horizon, removable S_BH.'
)

# Section 8
pdf.chapter_title('8. Conclusion')
pdf.body_text(
    'Quantum entanglement has a 0/0 removable singularity structure at '
    'the AdS/CFT boundary. The Ryu-Takayanagi formula, holographic bound, '
    'and ER=EPR conjecture all share this structure. The critical exponent '
    'beta=1/2 connects to the Toomre Q parameter.'
)

# References
pdf.chapter_title('References')
refs = [
    "[1] Ryu & Takayanagi (2006). Phys. Rev. Lett. 96, 181602.",
    "[2] Maldacena (1998). Adv. Theor. Math. Phys. 2, 231.",
    "[3] Almheiri et al. (2015). JHEP 2015, 16.",
    "[4] Maldacena & Susskind (2013). Fortschr. Phys. 61, 781.",
    "[5] Bekenstein (1973). Phys. Rev. D 7, 2333.",
    "[6] Hawking (1975). Comm. Math. Phys. 43, 199.",
    "[7] Toomre (1964). ApJ 139, 1217.",
    "[8] Puno (2026). The Removable Singularity.",
]
for ref in refs:
    pdf.bullet(ref)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'papers', 'quantum_entanglement.pdf')
pdf.output(output_path)
print("PDF saved to: %s" % output_path)
print("Pages: %d" % pdf.page_no())
