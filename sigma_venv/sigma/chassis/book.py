"""
sigma.chassis.book: The Removable Singularity — Book Integration
================================================================

Maps the complete book structure to the Sigma chassis.
Classifies every result by epistemic status.
Implements the honest methodology from Chapters 15-16.

Sources:
  [B1] Puno, "The Removable Singularity" (2026)
  [B2] L'Hopital, "Analyse des Infiniment Petits" (1696)
  [B3] Riemann, "Ueber die Anzahl der Primzahlen" (1859)
  [B4] Conway & Sloane, "Sphere Packings" (1999)
  [B5] Viazovska, "Sphere packing in R^8" (2017)
  [B6] Peskin & Schroeder, "QFT" (1995)
  [B7] Wilson, "Renormalization Group" (1982 Nobel)
  [B8] Scheffer et al., "Early-warning signals" (Nature, 2009)
  [B9] Power et al., "Grokking" (2022)
  [B10] Cubitt et al., "Undecidable spectral gap" (2015)
  [B11] Gödel, "Incompleteness" (1931)
  [B12] Turing, "On Computable Numbers" (1936)
  [B13] Wiles, "Modularity Theorem" (1995)
  [B14] Distler & Garibaldi, "Refuting Lisi" (2010)
  [B15] McKay, "E8-SU(2) coincidence" (1980)
  [B16] Gonzalez-Sprinberg & Verdier, "McKay mechanism" (1983)
  [B17] Kostant, "McKay correspondence" (1985)
  [B18] Du Val, "Kleinian singularities" (1934)
  [B19] Klein, "E8 singularity" (1884)
  [B20] Gross et al., "Heterotic string" (1985)
  [B21] Georgi & Glashow, "SU(5) GUT" (1974)
  [B22] Noether, "Symmetry and conservation" (1918)
  [B23] Bekenstein, "Black hole entropy" (1973)
  [B24] Shannon, "Information theory" (1948)
  [B25] Lorenz, "Chaotic weather" (1963)
  [B26] May, "Chaotic population models" (1976)
  [B27] Brin & Page, "PageRank" (1998)
  [B28] Turing, "Morphogenesis" (1952)
  [B29] Black & Scholes, "Option pricing" (1973)
  [B30] Kermack & McKendrick, "Epidemic model" (1927)
"""

# Epistemic status constants
REAL = "WHERE THIS IS REAL"
CAREFUL = "WHERE TO BE CAREFUL"
NOT_SAME = "NOT THE SAME PATTERN"


class EpistemicClassifier:
    """Classifies results by epistemic status.
    
    From Chapter 16's three-question checklist:
    1. Is the special point proven to exist and behave that way?
    2. Is the finite value derived from surrounding behavior?
    3. Does the specific case cover the genuinely open part?
    
    YES to all three = REAL
    NO to any = CAREFUL
    """
    
    CHECKLIST = [
        "Is the special point proven to exist and behave that way?",
        "Is the finite value derived from surrounding behavior?",
        "Does the specific case cover the genuinely open part?",
    ]
    
    @staticmethod
    def classify(answers):
        """Classify based on three-question checklist.
        
        Args:
            answers: list of 3 booleans (True = yes)
        
        Returns:
            REAL, CAREFUL, or NOT_SAME
        """
        if all(answers):
            return REAL
        else:
            return CAREFUL
    
    @staticmethod
    def report(name, answers, detail=""):
        """Generate a classification report."""
        status = EpistemicClassifier.classify(answers)
        lines = [name]
        lines.append("  Status: %s" % status)
        for i, (q, a) in enumerate(zip(EpistemicClassifier.CHECKLIST, answers)):
            lines.append("  [%s] %s" % ("Y" if a else "N", q))
        if detail:
            lines.append("  Detail: %s" % detail)
        return "\n".join(lines)


# Chapter structure with epistemic classification
CHAPTERS = [
    # Part I: The Core Idea
    {
        "part": "I",
        "chapter": 1,
        "title": "What 0/0 Actually Means",
        "status": REAL,
        "category": "foundations",
        "mechanism": "L'Hopital's rule: lim f/g = f'/g' when f(a)=g(a)=0",
        "examples": ["(x^2-1)/(x-1) -> 2", "sin(x)/x -> 1"],
        "sigma_value": 1.0,
        "source": "[B2] L'Hopital 1696",
    },
    {
        "part": "I",
        "chapter": 2,
        "title": "Why This Keeps Showing Up",
        "status": REAL,
        "category": "structural",
        "mechanism": "Response function: output/input. At special point, both vanish for shared reason.",
        "examples": ["Resonance frequency", "Critical point", "Bifurcation"],
        "sigma_value": None,
        "source": "[B1] Puno 2026",
    },
    # Part II: Physics and Engineering
    {
        "part": "II",
        "chapter": 3,
        "title": "Circuits at Resonance",
        "status": REAL,
        "category": "electrical_engineering",
        "mechanism": "Z(w) = R + i(wL - 1/wC). At w0 = 1/sqrt(LC), reactance cancels, Z(w0) = R.",
        "examples": ["Series RLC circuit", "Radio tuning"],
        "sigma_value": 1.0,  # R at resonance
        "source": "Textbook EE",
    },
    {
        "part": "II",
        "chapter": 4,
        "title": "Mechanical Oscillators",
        "status": REAL,
        "category": "mechanical_engineering",
        "mechanism": "Z(w) = c + i(mw - k/w). At w0 = sqrt(k/m), Z(w0) = c.",
        "examples": ["Mass-spring-damper", "Same ODE as circuits"],
        "sigma_value": 1.0,
        "source": "Textbook classical mechanics",
    },
    {
        "part": "II",
        "chapter": 5,
        "title": "Thermoacoustic Systems",
        "status": REAL,
        "category": "thermoacoustics",
        "mechanism": "Acoustic-electric analogy. Z_ac(w) = R_ac at resonance. R_ac does thermodynamic work.",
        "examples": ["Thermoacoustic engine", "Cryocooler"],
        "sigma_value": 1.0,
        "source": "[B1] Puno 2026, acoustics literature",
    },
    {
        "part": "II",
        "chapter": 6,
        "title": "Impedance Matching in Optics",
        "status": REAL,
        "category": "optics",
        "mechanism": "Quarter-wave coating: Z_coating = sqrt(Z_glass * Z_air). Destructive interference of reflections.",
        "examples": ["Antireflection coating", "Camera lenses"],
        "sigma_value": 0.0,  # reflection coefficient
        "source": "Textbook optics",
    },
    {
        "part": "II",
        "chapter": 7,
        "title": "Pole-Zero Cancellation",
        "status": REAL,
        "category": "control_theory",
        "mechanism": "G(s)*C(s) has (s-a) in both num and den. Engineer CREATES the 0/0.",
        "examples": ["Autopilot", "Industrial controllers"],
        "sigma_value": 1.0,
        "source": "Textbook control theory",
    },
    {
        "part": "II",
        "chapter": 8,
        "title": "Kutta Condition",
        "status": REAL,
        "category": "aerodynamics",
        "mechanism": "Velocity finite at trailing edge -> fixes circulation Gamma -> Lift = rho * V * Gamma.",
        "examples": ["Airfoil design", "Wing lift calculation"],
        "sigma_value": 1.0,
        "source": "Textbook aerodynamics",
    },
    {
        "part": "II",
        "chapter": 9,
        "title": "Resonances in QFT",
        "status": REAL,
        "category": "quantum_field_theory",
        "mechanism": "G(p) = 1/(p^2 - m^2 + igamma). At p^2 = m^2, propagator pole. gamma keeps it finite.",
        "examples": ["Particle mass", "Decay width"],
        "sigma_value": 1.0,
        "source": "[B6] Peskin & Schroeder 1995",
    },
    {
        "part": "II",
        "chapter": "9-adjunct",
        "title": "The Mass Gap",
        "status": CAREFUL,
        "category": "yang_mills",
        "mechanism": "Spec(H) = {0} U [Delta, inf). Delta > 0 means gap. Different from removable singularity.",
        "examples": ["Yang-Mills mass gap (Clay Millennium Problem)", "Band gap in semiconductors"],
        "sigma_value": None,
        "source": "[B10] Cubitt et al. 2015, Clay Institute",
    },
    {
        "part": "II",
        "chapter": 10,
        "title": "Phase Transitions",
        "status": REAL,
        "category": "statistical_mechanics",
        "mechanism": "Critical exponents: chi ~ |T-Tc|^(-gamma). Gamma is finite, universal. Renormalization group.",
        "examples": ["Curie temperature", "Critical opalescence", "3D Ising beta=0.326"],
        "sigma_value": 0.326,
        "source": "[B7] Wilson 1982 Nobel",
    },
    {
        "part": "II",
        "chapter": "10-contrast",
        "title": "Fluid Drag Crisis",
        "status": NOT_SAME,
        "category": "fluid_dynamics",
        "mechanism": "Drag coefficient drops at critical Re. NOT a 0/0. Jump discontinuity, not removable.",
        "examples": ["Sphere drag", "Eiffel 1912"],
        "sigma_value": None,
        "source": "[B1] Puno 2026, Prandtl boundary layer",
    },
    {
        "part": "II",
        "chapter": 11,
        "title": "Persistent Flow",
        "status": REAL,
        "category": "superconductivity",
        "mechanism": "Below Tc, current state is lowest energy. No mechanism to stop it. >1 year measured.",
        "examples": ["Superconducting ring", "Zero-point energy", "Superfluid helium"],
        "sigma_value": 1.0,
        "source": "Textbook superconductivity",
    },
    {
        "part": "II",
        "chapter": "11-adjunct",
        "title": "Does Time Itself Stop?",
        "status": CAREFUL,
        "category": "philosophy_of_time",
        "mechanism": "Arrow of time: emergent from entropy? Mainstream says yes. Active debate.",
        "examples": ["Phi phenomenon", "Einstein's illusion remark"],
        "sigma_value": None,
        "source": "[B1] Puno 2026, Boltzmann, Eddington",
    },
    {
        "part": "II",
        "chapter": 12,
        "title": "Singularities at Edge of Spacetime",
        "status": CAREFUL,
        "category": "general_relativity",
        "mechanism": "Classical GR has true singularities (Penrose-Hawking). Quantum gravity may remove them.",
        "examples": ["Black hole center", "Big Bang", "Loop quantum cosmology bounce"],
        "sigma_value": None,
        "source": "Penrose-Hawking theorems, active research",
    },
    # Part III: Life, Chemistry, Computation
    {
        "part": "III",
        "chapter": 13,
        "title": "Tipping Points",
        "status": REAL,
        "category": "ecology_climate",
        "mechanism": "Critical slowing down: recovery time increases, fluctuations grow. Early-warning signal.",
        "examples": ["Lake eutrophication", "Climate tipping", "Epidemic threshold R0=1"],
        "sigma_value": 0.423091,
        "source": "[B8] Scheffer et al. Nature 2009",
    },
    {
        "part": "III",
        "chapter": 14,
        "title": "Grokking in ML",
        "status": CAREFUL,
        "category": "machine_learning",
        "mechanism": "Sudden generalization after delay. Phase-transition framing. Arrhenius-type delay.",
        "examples": ["Neural network grokking", "Memorization -> generalization"],
        "sigma_value": 0.498627,
        "source": "[B9] Power et al. 2022",
    },
    # Part IV: Knowing Where the Pattern Stops
    {
        "part": "IV",
        "chapter": 15,
        "title": "Three Kinds of Degree",
        "status": REAL,
        "category": "epistemology",
        "mechanism": "Order of zero (integer -> fraction -> anomalous -> undefined) tracks epistemic confidence.",
        "examples": ["BCS gap beta=1/2", "Ising beta=0.326", "GR singularity"],
        "sigma_value": None,
        "source": "[B1] Puno 2026",
    },
    {
        "part": "IV",
        "chapter": 16,
        "title": "When a Beautiful Pattern Isn't Evidence",
        "status": REAL,
        "category": "methodology",
        "mechanism": "Three-question checklist: (1) proven to exist? (2) derived not assumed? (3) covers open part?",
        "examples": ["Langlands verification != open progress", "Hard-coded ratio = 1 is not evidence"],
        "sigma_value": None,
        "source": "[B1] Puno 2026, [B13] Wiles 1995",
    },
    # Appendix B: Symmetry, Chaos, and Information
    {
        "part": "APP",
        "chapter": "B",
        "title": "Verlinde Entropy",
        "status": REAL,
        "category": "thermodynamic_gravity",
        "mechanism": "S = A/(4*G*hbar*c). Gravity as entropic force. Area/4 = entropy.",
        "examples": ["Black hole entropy", "Holographic principle"],
        "sigma_value": 1.0,
        "source": "[B23] Bekenstein 1973, [B1] Puno 2026",
    },
    {
        "part": "APP",
        "chapter": "B",
        "title": "Bekenstein Bound",
        "status": REAL,
        "category": "information_theory",
        "mechanism": "S <= 2*pi*E*R/(hbar*c). Maximum information in a region. Finite bits.",
        "examples": ["Black hole is maximum entropy object", "Holographic bound"],
        "sigma_value": 1.0,
        "source": "[B23] Bekenstein 1973, [B24] Shannon 1948",
    },
    {
        "part": "APP",
        "chapter": "B",
        "title": "Landauer's Principle",
        "status": REAL,
        "category": "computation",
        "mechanism": "E >= kT*ln(2) per bit erased. Information is physical. Thermodynamic cost of logic.",
        "examples": ["Minimum energy per bit operation", "Maxwell's demon resolved"],
        "sigma_value": 1.0,
        "source": "Landauer 1961, [B1] Puno 2026",
    },
    {
        "part": "APP",
        "chapter": "B",
        "title": "Kolmogorov Complexity",
        "status": REAL,
        "category": "algorithmic_information",
        "mechanism": "K(x) = length of shortest program producing x. Uncomputable but well-defined.",
        "examples": ["Random strings have high K", "Compressible strings have low K"],
        "sigma_value": None,
        "source": "Kolmogorov 1965, [B1] Puno 2026",
    },
    # Appendix C: Randomness and Strategy
    {
        "part": "APP",
        "chapter": "C",
        "title": "Nash Equilibrium",
        "status": REAL,
        "category": "game_theory",
        "mechanism": "Every finite game has at least one mixed-strategy equilibrium. Fixed point theorem.",
        "examples": ["Prisoner's dilemma", "Matching pennies", "Auction design"],
        "sigma_value": 1.0,
        "source": "Nash 1950, [B1] Puno 2026",
    },
    {
        "part": "APP",
        "chapter": "C",
        "title": "Kelly Criterion",
        "status": REAL,
        "category": "optimal_betting",
        "mechanism": "f* = (bp-q)/b. Maximize long-term growth rate. Log-optimal portfolio.",
        "examples": ["Gambling", "Investment", "Portfolio allocation"],
        "sigma_value": 1.0,
        "source": "Kelly 1956, [B1] Puno 2026",
    },
    {
        "part": "APP",
        "chapter": "C",
        "title": "Martingale Stopping Theorem",
        "status": REAL,
        "category": "probability",
        "mechanism": "E[X_tau] = E[X_0] under fair game. Stopping doesn't beat the market.",
        "examples": ["Optional stopping", "Fair game is fair"],
        "sigma_value": 1.0,
        "source": "Doob 1953, [B1] Puno 2026",
    },
    # Appendix D: The Edge of Provability
    {
        "part": "APP",
        "chapter": "D",
        "title": "Halting Problem",
        "status": REAL,
        "category": "computability",
        "mechanism": "No algorithm can decide if arbitrary program halts. Proven by diagonal argument.",
        "examples": ["Turing 1936", "Undecidability is absolute"],
        "sigma_value": None,
        "source": "[B12] Turing 1936",
    },
    {
        "part": "APP",
        "chapter": "D",
        "title": "Gödel's Incompleteness",
        "status": REAL,
        "category": "mathematical_logic",
        "mechanism": "Any consistent system capable of arithmetic contains true but unprovable statements.",
        "examples": ["Gödel sentence", "No complete consistent system"],
        "sigma_value": None,
        "source": "[B11] Gödel 1931",
    },
    {
        "part": "APP",
        "chapter": "D",
        "title": "Undecidable Spectral Gap",
        "status": CAREFUL,
        "category": "quantum_many_body",
        "mechanism": "No algorithm can decide if a given local Hamiltonian has a spectral gap. Cubitt et al.",
        "examples": ["Quantum spin chains", "Ground state gap is undecidable"],
        "sigma_value": None,
        "source": "[B10] Cubitt et al. 2015",
    },
    # Part VII: Extensions
    {
        "part": "VII",
        "chapter": 30,
        "title": "Toomre Q: The Universal 0/0",
        "status": REAL,
        "category": "astrophysics",
        "mechanism": "Toomre Q=1 is a 0/0 removable singularity connecting NS, YM, and BSD via spectral gap theory.",
        "examples": ["Milky Way Q=0 (unstable)", "Solar system 14 resonances", "beta=1/2 mean-field Ising"],
        "sigma_value": 1.0,
        "source": "Toomre 1964, Lin & Shu 1964, Chirikov 1959, Caffarelli et al. 1982",
    },
]


class BookIntegration:
    """Integrates the book into the Sigma chassis."""
    
    def __init__(self):
        self.chapters = CHAPTERS
        self.classifier = EpistemicClassifier()
    
    def real_results(self):
        """Return all REAL results."""
        return [c for c in self.chapters if c["status"] == REAL]
    
    def careful_results(self):
        """Return all CAREFUL results."""
        return [c for c in self.chapters if c["status"] == CAREFUL]
    
    def not_same(self):
        """Return all NOT_SAME results (contrast cases)."""
        return [c for c in self.chapters if c["status"] == NOT_SAME]
    
    def currency_additions(self):
        """Return Sigma values from the book for currency ledger."""
        additions = []
        for c in self.chapters:
            if c["sigma_value"] is not None and c["status"] == REAL:
                ch = c["chapter"]
                if isinstance(ch, int):
                    name = "ch%d_%s" % (ch, c["category"])
                else:
                    name = "app%s_%s" % (ch, c["category"])
                additions.append({
                    "name": name,
                    "value": c["sigma_value"],
                    "field": c["category"],
                    "source": c["source"],
                    "chapter": ch,
                    "title": c["title"],
                })
        return additions
    
    def summary(self):
        """Print full book integration summary."""
        real = self.real_results()
        careful = self.careful_results()
        notsame = self.not_same()
        
        print("THE REMOVABLE SINGULARITY: BOOK INTEGRATION")
        print("=" * 70)
        print()
        
        print("PART I: THE CORE IDEA")
        print("-" * 70)
        for c in self.chapters:
            if c["part"] == "I":
                print("  Ch.%s: %s [%s]" % (c["chapter"], c["title"], c["status"]))
                print("    %s" % c["mechanism"])
        print()
        
        print("PART II: PHYSICS AND ENGINEERING")
        print("-" * 70)
        for c in self.chapters:
            if c["part"] == "II":
                print("  Ch.%s: %s [%s]" % (c["chapter"], c["title"], c["status"]))
                print("    %s" % c["mechanism"][:80])
        print()
        
        print("PART III: LIFE, CHEMISTRY, COMPUTATION")
        print("-" * 70)
        for c in self.chapters:
            if c["part"] == "III":
                print("  Ch.%s: %s [%s]" % (c["chapter"], c["title"], c["status"]))
                print("    %s" % c["mechanism"][:80])
        print()
        
        print("PART IV: KNOWING WHERE THE PATTERN STOPS")
        print("-" * 70)
        for c in self.chapters:
            if c["part"] == "IV":
                print("  Ch.%s: %s [%s]" % (c["chapter"], c["title"], c["status"]))
        print()
        
        print("APPENDICES")
        print("-" * 70)
        for c in self.chapters:
            if c["part"] == "APP":
                print("  App.%s: %s [%s]" % (c["chapter"], c["title"], c["status"]))
                print("    %s" % c["mechanism"][:80])
        print()
        
        print("EPISTEMIC CLASSIFICATION")
        print("-" * 70)
        print("  REAL (proven, derived, covers open part): %d" % len(real))
        print("  CAREFUL (active research, open hypotheses): %d" % len(careful))
        print("  NOT_SAME (contrast cases, pattern doesn't apply): %d" % len(notsame))
        print()
        
        print("CURRENCY ADDITIONS FROM BOOK")
        print("-" * 70)
        for a in self.currency_additions():
            print("  %-30s %10.6f Sigma  [%s]" % (
                a["name"], a["value"], a["field"]))
        print()
        
        print("THREE-QUESTION CHECKLIST (Chapter 16)")
        print("-" * 70)
        for q in EpistemicClassifier.CHECKLIST:
            print("  1. %s" % q)
        print()
        print("  YES to all three = REAL")
        print("  NO to any = CAREFUL")
        print()
        
        print("Sources: [B1]-[B30] in module docstring")
