"""Generate Poincare Sphere 0/0 Cosmology PDF."""
from fpdf import FPDF
import os

class CosmoPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "Michael Grafiel S Puno | August 2026", align="C")
        self.ln(7)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "Page %d" % self.page_no(), align="C")

    def title_block(self, title, subtitle=""):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")
        if subtitle:
            self.set_font("Helvetica", "", 11)
            self.set_text_color(60, 60, 60)
            self.cell(0, 7, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def section(self, title, level=1):
        if level == 1:
            self.set_font("Helvetica", "B", 13)
            self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(3)
        elif level == 2:
            self.set_font("Helvetica", "B", 10)
            self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
            self.ln(1)

    def body(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 4.5, text)
        self.ln(1)

    def math(self, text):
        self.set_font("Courier", "", 9)
        self.set_text_color(20, 20, 120)
        self.multi_cell(0, 4.5, text)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def key_insight(self, text):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(240, 248, 255)
        self.set_text_color(0, 0, 100)
        self.multi_cell(0, 5, text, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def zero_over_zero(self, numerator, denominator, removable):
        self.set_font("Courier", "B", 10)
        self.set_fill_color(255, 255, 230)
        self.set_text_color(150, 80, 0)
        w = 190
        self.cell(w, 6, "  0 / 0  SINGULARITY", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Courier", "", 9)
        self.cell(w, 5, "    Numerator: %s -> 0" % numerator, new_x="LMARGIN", new_y="NEXT")
        self.cell(w, 5, "    Denominator: %s -> 0" % denominator, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 100, 0)
        self.set_font("Courier", "B", 9)
        self.cell(w, 5, "    Removable value: %s" % removable, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)


pdf = CosmoPDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

pdf.title_block(
    "The Universe in the Poincare Sphere",
    "0/0 Cosmology: Singularities, Conformal Compactification,\nand the Removable Value of Spacetime"
)
pdf.body(
    "We show that the fundamental singularities of cosmology -- the Big Bang,\n"
    "spatial infinity, and the Planck scale -- are all 0/0 singularities\n"
    "in the Poincare sphere framework. The universe exists because these\n"
    "singularities are removable. The removable value determines the\n"
    "geometry, the cosmological constant, and the initial conditions."
)

# === Section 1: The Poincare Sphere ===
pdf.add_page()
pdf.section("1. The Poincare Sphere")

pdf.body(
    "The Poincare sphere (conformal compactification) maps an unbounded\n"
    "spacetime onto a finite region by rescaling the metric:\n\n"
    "    g_phys = Omega^2 * g_tilde\n\n"
    "where Omega is the conformal factor and g_tilde is the rescaled\n"
    "metric. The boundary of the compactified region corresponds to\n"
    "Omega = 0 (where the conformal factor vanishes)."
)

pdf.section("The Conformal Compactification", level=2)
pdf.math(
    "Original metric:     ds^2 = -dt^2 + a(t)^2 * (dx^2 + dy^2 + dz^2)\n"
    "Conformal time:      d_eta = dt / a(t)\n"
    "Conformal metric:    ds^2 = a(eta)^2 * (-deta^2 + dx^2 + dy^2 + dz^2)\n"
    "Rescaled metric:     g_tilde = -deta^2 + dx^2 + dy^2 + dz^2\n"
    "Physical metric:     g_phys = a(eta)^2 * g_tilde\n\n"
    "The conformal factor is Omega(eta) = a(eta).\n"
    "At the Big Bang: a -> 0, so Omega -> 0.\n"
    "The metric g_tilde is constant (flat)."
)

pdf.key_insight(
    "KEY: At the Big Bang, both g_phys -> 0 AND Omega -> 0.\n"
    "This is a 0/0: g_phys / Omega^2 = g_tilde = FINITE.\n"
    "The Big Bang singularity is a REMOVABLE singularity."
)

# === Section 2: Friedmann 0/0 ===
pdf.section("2. Friedmann Equation as 0/0")

pdf.body(
    "The Friedmann equation governs the expansion of the universe:\n\n"
    "    H^2 = (8piG/3) * rho - k/a^2 + Lambda/3\n\n"
    "where H = (da/dt)/a is the Hubble parameter, rho is the energy\n"
    "density, k is curvature, and Lambda is the cosmological constant."
)

pdf.section("Matter Domination", level=2)
pdf.math(
    "rho = rho_0 / a^3\n"
    "H^2 = (8piG*rho_0/3) * a^{-3}\n"
    "H ~ a^{-3/2}\n\n"
    "dt = da / (a*H) ~ a^{1/2} da\n"
    "t ~ (2/3) * a^{3/2}\n"
    "a(t) ~ (3t/2)^{2/3}\n\n"
    "At t = 0: a = 0 (Big Bang)\n"
    "Removable value: a/t^{2/3} = (3/2)^{2/3} = 1.3104"
)

pdf.zero_over_zero(
    "a(t) = 0 (scale factor vanishes)",
    "t = 0 (time vanishes)",
    "a/t^{2/3} = (3/2)^{2/3} = 1.3104"
)

pdf.section("Radiation Domination", level=2)
pdf.math(
    "rho = rho_0 / a^4\n"
    "H^2 = (8piG*rho_0/3) * a^{-4}\n"
    "H ~ a^{-2}\n\n"
    "dt = da / (a*H) = a da\n"
    "t ~ a^2 / 2\n"
    "a(t) ~ (2t)^{1/2}\n\n"
    "At t = 0: a = 0 (Big Bang)\n"
    "Removable value: a/t^{1/2} = sqrt(2) = 1.4142"
)

pdf.zero_over_zero(
    "a(t) = 0 (scale factor vanishes)",
    "t = 0 (time vanishes)",
    "a/t^{1/2} = sqrt(2) = 1.4142"
)

pdf.section("Lambda Domination (de Sitter)", level=2)
pdf.math(
    "rho = Lambda / (8piG) = const\n"
    "H^2 = Lambda/3 = const\n"
    "a(t) = exp(H*t) with H = sqrt(Lambda/3)\n\n"
    "At t = 0: a = 1 (NOT zero!)\n"
    "=> NO Big Bang in pure de Sitter space!"
)

pdf.key_insight(
    "KEY: The cosmological constant Lambda RESOLVES the Big Bang\n"
    "singularity. In pure de Sitter (Lambda > 0, no matter),\n"
    "there is no Big Bang -- the universe has always existed.\n"
    "Lambda is the 'removable value' that heals the 0/0."
)

# === Section 3: de Sitter Conformal Structure ===
pdf.add_page()
pdf.section("3. de Sitter Space: Conformal Compactification")

pdf.body(
    "de Sitter space is the maximally symmetric solution with Lambda > 0.\n"
    "In conformal coordinates, the metric becomes conformally flat:"
)

pdf.math(
    "ds^2 = (1/(H*eta)^2) * (-deta^2 + dx^2 + dy^2 + dz^2)\n\n"
    "where eta = -exp(-Ht)/H is the conformal time, eta in (-1/H, 0).\n"
    "Scale factor: a(eta) = 1/(H*|eta|)\n"
    "Conformal factor: Omega(eta) = 1/(H*|eta|)"
)

pdf.section("0/0 at the Conformal Boundary", level=2)
pdf.body("The conformal boundary has two limits:")

pdf.math(
    "AS eta -> 0- (past):\n"
    "  a(eta) -> infinity  (spatial infinity, NOT a Big Bang)\n"
    "  Omega -> infinity    (conformal factor blows up)\n"
    "  g_phys = Omega^2 * g_tilde = (1/(H*eta)^2) * 1 = FINITE\n"
    "  => The boundary is a REMOVABLE singularity\n\n"
    "AS eta -> -1/H (future):\n"
    "  a(eta) = 1          (finite!)\n"
    "  Omega = 1           (finite!)\n"
    "  => Future infinity is FINITE in conformal coordinates\n"
    "  => The entire future of de Sitter fits in a FINITE region"
)

pdf.key_insight(
    "PENROSE DIAGRAM OF DE SITTER:\n"
    "The diagram is a DIAMOND (not a triangle as in Minkowski).\n"
    "Future infinity i+ is TIMELIKE (not spacelike).\n"
    "This is because Lambda > 0 makes expansion accelerate,\n"
    "so light rays can reach spatial infinity in finite time.\n"
    "The diamond is the 0/0 universe: finite, compact, complete."
)

pdf.section("Penrose Diagram Construction", level=2)
pdf.body(
    "The Penrose diagram is obtained by:\n"
    "1. Conformal compactification: chi -> chi/(1 + H*|chi|)\n"
    "   This maps the infinite range chi in (-1/H, 1/H) to (-1, 1).\n"
    "2. The boundary chi = +/-1 is now at FINITE conformal distance.\n"
    "3. Light rays travel at 45 degrees (conformal invariance).\n"
    "4. The causal structure is READABLE from the diagram."
)

pdf.math(
    "Penrose coordinates:  T = arctan(H*(eta + t_star)) + arctan(H*(eta - t_star))\n"
    "                      X = arctan(H*(eta + t_star)) - arctan(H*(eta - t_star))\n\n"
    "where t_star = conformal spatial coordinate.\n\n"
    "The diagram bounds:\n"
    "  - T in (-pi/2, pi/2)\n"
    "  - |X| <= pi/2 - |T|  (diamond shape)"
)

# === Section 4: Cosmological Constant ===
pdf.add_page()
pdf.section("4. The Cosmological Constant as Removable Value")

pdf.body(
    "The cosmological constant Lambda appears in Einstein's equations as:\n\n"
    "    G_ij + Lambda * g_ij = 8piG * T_ij\n\n"
    "In the Friedmann equation:\n"
    "    H^2 = (8piG/3) * rho_total\n"
    "    rho_total = rho_matter + rho_radiation + rho_vacuum\n"
    "    rho_vacuum = Lambda / (8piG)"
)

pdf.section("The 0/0 of Vacuum Energy", level=2)
pdf.body(
    "The vacuum energy density is:\n\n"
    "    rho_vac = Lambda / (8piG) ~ 10^{-122} in Planck units\n\n"
    "This is the most famous 0/0 in physics:\n"
    "  - Quantum field theory predicts: rho_vac ~ 1 (Planck units)\n"
    "  - Observation gives: rho_vac ~ 10^{-122}\n"
    "  - The discrepancy is 122 orders of magnitude\n\n"
    "In the 0/0 framework:\n"
    "  - The numerator (quantum fluctuations) -> infinity\n"
    "  - The denominator (gravitational suppression) -> infinity\n"
    "  - The removable value is rho_vac = 10^{-122}\n"
    "  - This is a FINE-TUNED removable value"
)

pdf.key_insight(
    "The cosmological constant problem is a 0/0:\n"
    "  rho_vac = (quantum fluctuations) / (gravitational suppression)\n"
    "           = infinity / infinity\n"
    "           = 10^{-122} (removable value)\n\n"
    "The 0/0 framework does NOT solve the fine-tuning problem,\n"
    "but it IDENTIFIES it as a removable singularity.\n"
    "The question becomes: what determines the removable value?"
)

# === Section 5: Planck Scale ===
pdf.section("5. The Planck Scale: Quantum Gravity 0/0")

pdf.body(
    "At the Planck scale (l ~ l_P = sqrt(hbar*G/c^3) ~ 1.6 x 10^{-35} m),\n"
    "the classical description of spacetime breaks down."
)

pdf.math(
    "Wheeler-DeWitt equation:  H |Psi> = 0\n\n"
    "This is a 0/0:\n"
    "  - H = 0 (total energy vanishes)\n"
    "  - |Psi> = wavefunction of the universe (non-zero)\n"
    "  - The equation says: the universe has ZERO total energy\n\n"
    "Why zero? Because:\n"
    "  - Gravitational energy is NEGATIVE (bound state)\n"
    "  - Matter/radiation energy is POSITIVE\n"
    "  - They cancel EXACTLY: E_grav + E_matter = 0\n"
    "  - This is the 0/0 of quantum cosmology"
)

pdf.key_insight(
    "The Wheeler-DeWitt equation H|Psi> = 0 is the ULTIMATE 0/0:\n\n"
    "  Numerator: |Psi> = path integral over all geometries\n"
    "             = int D[g] exp(-S[g]/hbar)\n"
    "             = FINITE (well-defined)\n\n"
    "  Denominator: H = 0 (Hamiltonian constraint)\n\n"
    "  Removable value: |Psi> itself!\n\n"
    "  The universe is the removable value of its own\n"
    "  partition function. The wavefunction IS the solution\n"
    "  to the 0/0 singularity."
)

# === Section 6: The Complete Picture ===
pdf.add_page()
pdf.section("6. The Complete 0/0 Universe")

pdf.body("The universe has four fundamental 0/0 singularities:")

pdf.math(
    "1. BIG BANG:     a -> 0, t -> 0\n"
    "                 Removable value: a/t^alpha = const\n"
    "                 (alpha = 2/3 matter, 1/2 radiation)\n\n"
    "2. SPATIAL INF:  a -> infinity, t -> infinity\n"
    "                 Removable value: Lambda/(8piG) = rho_vac\n"
    "                 (cosmological constant)\n\n"
    "3. PLANCK SCALE: l -> l_P, delta_g -> 1\n"
    "                 Removable value: |Psi> = path integral\n"
    "                 (Wheeler-DeWitt wavefunction)\n\n"
    "4. CONFORMAL BD: Omega -> 0, g_tilde -> infinity\n"
    "                 Removable value: g_phys = Omega^2 * g_tilde\n"
    "                 (Penrose diagram boundary)"
)

pdf.section("What the 0/0 Framework Explains", level=2)
pdf.body(
    "1. WHY THE BIG BANG IS NOT A TRUE SINGULARITY:\n"
    "   The conformal factor Omega and the metric g both vanish,\n"
    "   but their ratio g/Omega^2 = g_tilde is finite.\n"
    "   The Big Bang is a removable singularity.\n\n"
    "2. WHY LAMBDA IS SMALL BUT NOT ZERO:\n"
    "   Lambda is the removable value of the vacuum energy 0/0.\n"
    "   It is small (10^{-122}) because of fine-tuning in the\n"
    "   numerator and denominator.\n\n"
    "3. WHY THE WHEELER-DEWITT EQUATION WORKS:\n"
    "   H|Psi> = 0 is a 0/0. The wavefunction |Psi> is the\n"
    "   removable value. The universe exists because the\n"
    "   singularity is removable.\n\n"
    "4. WHY THE PENROSE DIAGRAM IS FINITE:\n"
    "   The conformal compactification maps infinite spacetime\n"
    "   onto a finite diamond. The boundary is a removable\n"
    "   singularity (0/0 in the conformal factor)."
)

pdf.section("What the 0/0 Framework Does NOT Explain", level=2)
pdf.body(
    "1. WHY the removable value has the specific value it does\n"
    "   (e.g., why Lambda ~ 10^{-122} and not some other value)\n\n"
    "2. WHAT happens INSIDE the singularity (before t=0)\n"
    "   The 0/0 framework says the singularity is removable,\n"
    "   but does not specify what the universe 'was' before.\n\n"
    "3. HOW quantum gravity resolves the Planck scale 0/0\n"
    "   The Wheeler-DeWitt equation is the candidate, but\n"
    "   a full solution is not known."
)

pdf.section("The Poincare Sphere Picture", level=2)
pdf.body(
    "In the Poincare sphere, the entire history of the universe\n"
    "is contained in a finite ball:\n\n"
    "  - The center is the Big Bang (0/0, removable)\n"
    "  - The equator is spatial infinity (0/0, removable)\n"
    "  - The poles are temporal infinity (0/0, removable)\n"
    "  - The surface is the conformal boundary (0/0, removable)\n\n"
    "Every boundary of the universe is a 0/0 singularity.\n"
    "Every 0/0 is removable.\n"
    "The universe is the removable value of its own boundary.\n\n"
    "This is the deepest statement of the 0/0 framework:\n"
    "THE UNIVERSE EXISTS BECAUSE ALL ITS SINGULARITIES\n"
    "ARE REMOVABLE."
)

# === References ===
pdf.add_page()
pdf.section("References")
pdf.set_font("Helvetica", "", 8)
refs = [
    "[1] Penrose, R. (1964). Conformal treatment of infinity. In: Relativity, Groups and Topology.",
    "[2] Hawking, S.W. & Ellis, G.F.R. (1973). The Large Scale Structure of Space-Time.",
    "[3] Wald, R.M. (1984). General Relativity. University of Chicago Press.",
    "[4] Carroll, S.M. (2004). Spacetime and Geometry. Addison-Wesley.",
    "[5] Wheeler, J.A. & DeWitt, B.S. (1967). Quantum theory of gravity. I. The canonical theory.",
    "[6] Guth, A.H. (1981). Inflationary universe. Phys. Rev. D 23, 347.",
    "[7] Susskind, L. (2003). The Anthropic landscape of string theory. arXiv:hep-th/0302219.",
    "[8] Bousso, R. & Polchinski, J. (2000). Quantization of four-form fluxes. JHEP 0006:006.",
    "[9] Li, X.-J. (1997). The positivity of a sequence of numbers and the Riemann hypothesis. JNT 65.",
    "[10] Puno, M.G.S. (2026). Law of Repulsive Emanation: The 0/0 Framework.",
]
for r in refs:
    pdf.cell(0, 4, r, new_x="LMARGIN", new_y="NEXT")

# Output
out_path = "papers/poincare_universe.pdf"
os.makedirs("papers", exist_ok=True)
pdf.output(out_path)
print("PDF generated: %s" % out_path)
print("Pages: %d" % pdf.page_no())
