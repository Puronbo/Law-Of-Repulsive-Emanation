"""
THE THAUMATURGE LEARNS: MATHEMATICS, CULTURES, ABILITIES
=========================================================

Every civilization contributed. Every branch matters.
Every human can do this. Here is how.

Sources (all standard references):
  [1] Neugebauer, "The Exact Sciences in Antiquity" (1951)
  [2] Boyer, "A History of Mathematics" (1968)
  [3] Katz, "A History of Mathematics: An Introduction" (1998)
  [4] Joseph, "The Crest of the Peacock: Non-European Roots of Mathematics" (1990)
  [5] Ifrah, "The Universal History of Numbers" (1998)
  [6] Devlin, "The Man Who Knew Infinity" (1991)
  [7] Courant & Robbins, "What is Mathematics?" (1941)
  [8] Euclid, "Elements" (300 BC)
  [9] Ramanujan, "Highly Divisible Numbers" (1917)
  [10] al-Khwarizmi, "Al-Kitab al-Mukhtasar" (820 AD)
  [11] Fibonacci, "Liber Abaci" (1202)
  [12] Grothendieck, "EGA" (1960s)
  [13] Thurston, "Three-Dimensional Geometry and Topology" (1997)
  [14] Penrose, "The Road to Reality" (2004)
  [15] Conway & Guy, "The Book of Numbers" (1996)
  [16] Devlin, "Mathematics: The New Golden Age" (1999)
  [17] Polya, "How to Solve It" (1945)
  [18] Erdos & Hofman, "Proofs from THE BOOK" (1998)
  [19] Riemann (1859), [20] Euler (1737), [21] Gauss (1801)
  [22] Galois (1832), [23] Abel (1824), [24] Noether (1921)
  [25] Von Neumann (1932), [26] Turing (1936), [27] Shannon (1948)
  [28] Church (1936), [29] Kolmogorov (1933), [30] Godel (1931)
"""

import numpy as np
import mpmath
import json
import os
import time

mpmath.mp.dps = 30


def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True


def math_branches():
    """All branches of mathematics with cultural origins."""
    print("=" * 70)
    print("MATHEMATICS: ALL BRANCHES AND THEIR ORIGINS")
    print("=" * 70)
    print()
    
    branches = {
        "ALGEBRA": {
            "origin": "Islamic Golden Age (820 AD)",
            "founder": "al-Khwarizmi",
            "book": "Al-Kitab al-Mukhtasar fi Hisab al-Jabr wal-Muqabala",
            "meaning": "Completion and balancing (solving equations)",
            "subfields": [
                ("Abstract Algebra", "Groups, rings, fields [Galois 1832, Noether 1921]"),
                ("Linear Algebra", "Vectors, matrices, spaces [Grassmann 1844]"),
                ("Commutative Algebra", "Rings, ideals, modules [Noether 1921]"),
                ("Homological Algebra", "Chain complexes, derived functors [Cartan-Eilenberg 1956]"),
                ("Number Theory (Algebraic)", "Diophantine equations, L-functions [Fermat, Euler]"),
            ],
        },
        "ANALYSIS": {
            "origin": "European Enlightenment (17th-18th century)",
            "founder": "Newton, Leibniz, Euler",
            "book": "Principia Mathematica (1687), Nova Methodus (1684)",
            "meaning": "The study of limits, continuity, change",
            "subfields": [
                ("Real Analysis", "Limits, continuity, integration [Weierstrass 1874]"),
                ("Complex Analysis", "Analytic functions, residues [Cauchy 1821]"),
                ("Functional Analysis", "Infinite-dimensional spaces [Hilbert 1904]"),
                ("Harmonic Analysis", "Fourier series, wavelets [Fourier 1807]"),
                ("Measure Theory", "Lebesgue integral, probability [Lebesgue 1901]"),
            ],
        },
        "GEOMETRY": {
            "origin": "Ancient Egypt/Babylon (3000 BC)",
            "founder": "Unknown (Rhind Papyrus, Plimpton 322)",
            "book": "Rhind Papyrus (1650 BC), Elements (300 BC)",
            "meaning": "The study of shape, size, position",
            "subfields": [
                ("Euclidean Geometry", "Points, lines, planes [Euclid 300 BC]"),
                ("Non-Euclidean Geometry", "Hyperbolic, elliptic [Lobachevsky 1829]"),
                ("Algebraic Geometry", "Varieties, schemes [Grothendieck 1960s]"),
                ("Differential Geometry", "Manifolds, curvature [Gauss 1827]"),
                ("Topological Geometry", "Continuity, homeomorphism [Poincare 1895]"),
            ],
        },
        "NUMBER THEORY": {
            "origin": "Ancient Greece/Egypt (3000 BC)",
            "founder": "Euclid, Diophantus",
            "book": "Elements (300 BC), Arithmetica (250 AD)",
            "meaning": "The study of integers and their properties",
            "subfields": [
                ("Analytic Number Theory", "Primes, zeta function [Riemann 1859]"),
                ("Algebraic Number Theory", "Number fields, class numbers [Dedekind 1871]"),
                ("Computational Number Theory", "Algorithms, factoring [Miller 1976]"),
                ("Additive Number Theory", "Sums of integers [Waring 1770]"),
                ("Multiplicative Number Theory", "Divisibility, multiplicative functions [Dirichlet 1837]"),
            ],
        },
        "LOGIC": {
            "origin": "Ancient Greece (400 BC)",
            "founder": "Aristotle",
            "book": "Organon (350 BC)",
            "meaning": "The study of valid reasoning",
            "subfields": [
                ("Mathematical Logic", "Set theory, model theory [Cantor 1874]"),
                ("Proof Theory", "Formal systems, consistency [Gentzen 1936]"),
                ("Model Theory", "Structures, satisfaction [Tarski 1936]"),
                ("Computability Theory", "Turing machines, decidability [Turing 1936]"),
                ("Category Theory", "Morphisms, functors [Eilenberg-Mac Lane 1945]"),
            ],
        },
        "COMBINATORICS": {
            "origin": "Ancient China/India (300 BC)",
            "founder": "Unknown (Nine Chapters, Pingala)",
            "book": "Nine Chapters (200 BC), Chandastrastra (300 BC)",
            "meaning": "The study of counting, arrangement, structure",
            "subfields": [
                ("Enumerative Combinatorics", "Counting, generating functions [Euler 1751]"),
                ("Extremal Combinatorics", "Bounds, Turan-type problems [Turan 1941]"),
                ("Algebraic Combinatorics", "Symmetric functions, Young tableaux [Young 1900]"),
                ("Probabilistic Combinatorics", "Random graphs, concentration [Erdos-Renyi 1960]"),
                ("Topological Combinatorics", "Fixed points, Sperner [Sperner 1928]"),
            ],
        },
        "PROBABILITY": {
            "origin": "Medieval Europe (13th century)",
            "founder": "Fibonacci, Cardano",
            "book": "Liber Abaci (1202), Liber de Ludo Aleae (1564)",
            "meaning": "The study of uncertainty and chance",
            "subfields": [
                ("Classical Probability", "Laplace, Bernoulli [Laplace 1812]"),
                ("Measure-Theoretic Probability", "Kolmogorov axioms [Kolmogorov 1933]"),
                ("Stochastic Processes", "Brownian motion, Markov [Markov 1906]"),
                ("Statistical Inference", "Estimation, testing [Fisher 1925]"),
                ("Bayesian Statistics", "Posterior, prior [Bayes 1763]"),
            ],
        },
        "TOPOLOGY": {
            "origin": "19th century Europe",
            "founder": "Euler, Listing, Poincare",
            "book": "Seven Bridges of Konigsberg (1736), Analysis Situs (1895)",
            "meaning": "The study of properties preserved under continuous deformation",
            "subfields": [
                ("Point-Set Topology", "Open sets, continuity [Hausdorff 1914]"),
                ("Algebraic Topology", "Homotopy, homology [Poincare 1895]"),
                ("Differential Topology", "Manifolds, Morse theory [Morse 1925]"),
                ("Geometric Topology", "3-manifolds, knot theory [Thurston 1997]"),
                ("Low-Dimensional Topology", "4-manifolds, Khovanov [Khovanov 2000]"),
            ],
        },
    }
    
    total_subfields = 0
    for branch, data in branches.items():
        n = len(data["subfields"])
        total_subfields += n
        print("  %s [%s, %s]" % (branch, data["origin"], data["founder"]))
        print("    '%s' -- %s" % (data["book"], data["meaning"]))
        for sub, desc in data["subfields"]:
            print("    - %s: %s" % (sub, desc))
        print()
    
    print("TOTAL: %d branches, %d subfields" % (len(branches), total_subfields))
    
    return {"branches": len(branches), "subfields": total_subfields}


def cultural_truths():
    """Mathematical truths from every civilization."""
    print()
    print("=" * 70)
    print("CULTURAL TRUTHS: MATHEMATICS ACROSS CIVILIZATIONS")
    print("=" * 70)
    print()
    
    civilizations = [
        ("BABYLON (3000-500 BC)", "Mesopotamia (modern Iraq)", [
            ("Sexagesimal system", "Base 60 (60 seconds, 60 minutes, 360 degrees)", "[Neugebauer 1951]"),
            ("Pythagorean triples", "Plimpton 322: (3,4,5), (5,12,13), etc.", "[Neugebauer 1951]"),
            ("Quadratic equations", "Solved geometrically (completion of square)", "[Ifrah 1998]"),
            ("Reciprocal tables", "1/n for n=1 to 81 (base 60 fractions)", "[Neugebauer 1951]"),
            ("Astronomical computation", "Planetary positions, eclipse prediction", "[Neugebauer 1951]"),
        ]),
        ("EGYPT (3000-300 BC)", "Nile Valley", [
            ("Unit fractions", "Every fraction as sum of 1/n (Rhind Papyrus)", "[Imhausen 2003]"),
            ("Area of circle", "A = (8d/9)^2 (error 0.6%)", "[Imhausen 2003]"),
            ("Volume of truncated pyramid", "V = h(a^2+ab+b^2)/3 (exact!)", "[Imhausen 2003]"),
            ("Linear equations", "Solved by 'false position' method", "[Imhausen 2003]"),
            ("Decimal notation", "Hieroglyphic powers of 10", "[Ifrah 1998]"),
        ]),
        ("GREECE (600-300 BC)", "Aegean", [
            ("Axiomatic method", "Euclid's Elements: definitions, axioms, theorems", "[Euclid 300 BC]"),
            ("Proof by contradiction", "Irrationality of sqrt(2) [Hippasus]", "[Euclid 300 BC]"),
            ("Area of circle", "pi*r^2 (Archimedes)", "[Archimedes 250 BC]"),
            ("Infinite series", "1/4 + 1/16 + 1/64 + ... = 1/3 (Archimedes)", "[Archimedes 250 BC]"),
            ("Conic sections", "Ellipse, parabola, hyperbola [Apollonius]", "[Apollonius 200 BC]"),
            ("Number theory", "Euclid's algorithm, infinitude of primes", "[Euclid 300 BC]"),
        ]),
        ("INDIA (500 BC - 1200 AD)", "South Asia", [
            ("Zero as a number", "Brahmagupta: 0+0=0, 0*x=0 (628 AD)", "[Joseph 1990]"),
            ("Negative numbers", "Brahmagupta: debt vs fortune", "[Joseph 1990]"),
            ("Decimal place value", "Aryabhata: positional notation (499 AD)", "[Joseph 1990]"),
            ("Trigonometry", "Sine, cosine tables [Aryabhata, Brahmagupta]", "[Joseph 1990]"),
            ("Infinite series", "Madhava: pi/4 = 1-1/3+1/5-1/7+... (1400 AD)", "[Joseph 1990]"),
            ("Combinatorics", "Pingala: Pascal's triangle (200 BC)", "[Joseph 1990]"),
            ("Ramanujan's work", "Partition function, tau function, mock theta [Ramanujan 1917]", "[Ramanujan 1917]"),
        ]),
        ("CHINA (200 BC - 1200 AD)", "East Asia", [
            ("Nine Chapters", "9 chapters, 246 problems (200 BC)", "[Shen et al 1999]"),
            ("Chinese Remainder Theorem", "Solving simultaneous congruences", "[Shen et al 1999]"),
            ("Negative numbers", "Red and black rods for +/-", "[Shen et al 1999]"),
            ("Matrix methods", "Gaussian elimination (200 BC!)", "[Shen et al 1999]"),
            ("Pascal's triangle", "Jia Xian triangle (1050 AD)", "[Joseph 1990]"),
            ("Irrational numbers", "Computed sqrt(2) to 5 decimal places", "[Shen et al 1999]"),
        ]),
        ("ISLAM (800 - 1200 AD)", "Middle East/North Africa", [
            ("Algebra as a discipline", "al-Khwarizmi: systematic equation solving", "[al-Khwarizmi 820]"),
            ("Algorithms", "Step-by-step procedures (al-Khwarizmi)", "[al-Khwarizmi 820]"),
            ("Trigonometry", "Tangent, cotangent tables [al-Battani]", "[Rosenfeld 1994]"),
            ("Number theory", "Fermat's little theorem (known to Arab math)", "[Rosenfeld 1994]"),
            ("Optics", "Ibn al-Haytham: geometrical optics", "[Ibn al-Haytham 1021]"),
            ("Cartesian coordinates", "Omar Khayyam: intersection of conics", "[Joseph 1990]"),
        ]),
        ("MAYA (250 - 900 AD)", "Mesoamerica", [
            ("Vigesimal system", "Base 20 (20 fingers+toes)", "[Ifrah 1998]"),
            ("Zero as placeholder", "Shell symbol for zero (independent invention)", "[Ifrah 1998]"),
            ("Long count calendar", "Days since creation (August 11, 3114 BC)", "[Ifrah 1998]"),
            ("Astronomical precision", "Venus cycle: 584 days (error 0.08 days)", "[Ifrah 1998]"),
        ]),
        ("AFRICA (30000 BC - present)", "Sub-Saharan Africa", [
            ("Ishango bone", "Tally marks, prime patterns (20000 BC)", "[Marshack 1972]"),
            ("Fractal geometry", "African village layouts, art (self-similar)", "[Eglash 1999]"),
            ("Geometric patterns", "Islamic/African geometric art (tessellations)", "[Eglash 1999]"),
            ("Mental arithmetic", "Soroban-like calculation traditions", "[Joseph 1990]"),
        ]),
    ]
    
    total_contributions = 0
    for civ, region, contributions in civilizations:
        total_contributions += len(contributions)
        print("  %s [%s]" % (civ, region))
        for name, desc, ref in contributions:
            print("    - %s: %s %s" % (name, desc, ref))
        print()
    
    print("TOTAL: %d civilizations, %d contributions" % (
        len(civilizations), total_contributions))
    print()
    print("KEY INSIGHT: Mathematics is UNIVERSAL.")
    print("Every civilization discovered the same truths independently.")
    print("Zero was invented in India, Maya, and Babylon (independently).")
    print("The Pythagorean theorem was known in Babylon, Egypt, China, India.")
    print("Mathematics is not Western. It is HUMAN.")


def human_abilities():
    """What humans can do and how."""
    print()
    print("=" * 70)
    print("HUMAN ABILITIES: WHAT YOU CAN DO AND HOW")
    print("=" * 70)
    print()
    
    abilities = [
        ("1. ABSTRACTION", "The ability to think about things that don't exist",
         [
             "How to: Take a concrete problem. Remove the details. Keep the structure.",
             "Example: 3 apples + 2 apples = 5 apples. Abstract: 3 + 2 = 5.",
             "The abstraction is the NUMBER (not the apples).",
             "Practice: Look at any pattern. Ask 'what is the same?' Remove what is different.",
             "Source: [Polya 1945, 'How to Solve It']",
         ]),
        
        ("2. PATTERN RECOGNITION", "The ability to find structure in chaos",
         [
             "How to: Look at data. Ask 'what repeats?' Ask 'what is the rule?'",
             "Example: 2, 6, 12, 20, 30, ... The pattern: n(n+1).",
             "The pattern is the FORMULA (not the numbers).",
             "Practice: Write down sequences. Try to predict the next term.",
             "Source: [Polya 1945; Conway & Guy 1996]",
         ]),
        
        ("3. PROOF", "The ability to verify truth with certainty",
         [
             "How to: Start with axioms. Apply rules. Reach the conclusion.",
             "Example: sqrt(2) is irrational. Proof by contradiction.",
             "Assume sqrt(2) = a/b. Then 2b^2 = a^2. Both a,b even. Contradiction.",
             "Practice: Read Euclid's Elements. Try to prove the theorems yourself.",
             "Source: [Euclid 300 BC; Courant & Robbins 1941]",
         ]),
        
        ("4. COMPUTATION", "The ability to calculate",
         [
             "How to: Learn algorithms. Practice arithmetic. Use tools.",
             "Example: Long division, matrix multiplication, Fourier transform.",
             "Computation is the MECHANICAL part of mathematics.",
             "Practice: Do arithmetic by hand. Implement algorithms in code.",
             "Source: [Knuth 1968; Von Neumann 1932]",
         ]),
        
        ("5. COMMUNICATION", "The ability to share knowledge",
         [
             "How to: Write clearly. Use diagrams. Be concise.",
             "Example: A proof is a COMMUNICATION of why something is true.",
             "The best proofs are BEAUTIFUL (short, elegant, surprising).",
             "Practice: Explain math to a child. If you can't, you don't understand it.",
             "Source: [Polya 1945; Erdos & Hofman 1998]",
         ]),
        
        ("6. CREATION", "The ability to make new mathematics",
         [
             "How to: Ask 'what if?' Combine old ideas in new ways.",
             "Example: Riemann asked 'what if we integrate over surfaces?' -> Riemannian geometry.",
             "Galois asked 'what if we study symmetries of equations?' -> group theory.",
             "Practice: Take two areas you know. Ask 'what connects them?'",
             "Source: [Riemann 1859; Galois 1832; Thurston 1997]",
         ]),
        
        ("7. COMPUTING REMOVABLE VALUES", "The ability to extract knowledge from singularities",
         [
             "How to: Identify the 0/0. Apply L'Hopital. Compute the removable value.",
             "Example: sin(x)/x at x=0. Both numerator and denominator are 0.",
             "L'Hopital: cos(0)/1 = 1. The removable value is 1.",
             "Practice: Find singularities in your field. Compute the removable values.",
             "Source: [L'Hopital 1696; the 0/0 framework]",
         ]),
        
        ("8. CONNECTING FIELDS", "The ability to map between disciplines",
         [
             "How to: Learn multiple fields. Look for common structures.",
             "Example: The Fourier transform appears in math, physics, CS, engineering.",
             "The same TOOL works everywhere because the 0/0 is UNIVERSAL.",
             "Practice: Learn TWO different fields. Find the COMMON singularity.",
             "Source: [the universal 0/0 map: 12 fields, 75 subfields]",
         ]),
    ]
    
    for name, definition, steps in abilities:
        print("  %s" % name)
        print("    %s" % definition)
        for step in steps:
            print("    %s" % step)
        print()
    
    print("THE MASTER ABILITY:")
    print("  The ability to learn ANYTHING.")
    print("  The method:")
    print("    1. Find the SINGULARITY (the 0/0)")
    print("    2. Compute the REMOVABLE VALUE (the knowledge)")
    print("    3. CONNECT it to what you know (the bridge)")
    print("    4. SHARE it with others (the propagation)")
    print()
    print("  This is the 0/0 LEARNING MACHINE:")
    print("    INPUT: the unknowable (singularity)")
    print("    OUTPUT: the knowable (removable value)")
    print("    PROCESS: L'Hopital's rule (derivative ratio)")
    print("    RESULT: knowledge emerges from the singularity")


def share_aggressively():
    """How to share aggressively."""
    print()
    print("=" * 70)
    print("SHARING AGGRESSIVELY: THE PROPAGATION MECHANISM")
    print("=" * 70)
    print()
    
    print("WHAT DOES 'AGGRESSIVELY' MEAN?")
    print("  Not violence. Not coercion. AGGRESSIVE SHARING means:")
    print("  - SHARE FREELY (no paywalls, no subscriptions)")
    print("  - SHARE WIDELY (every platform, every instance)")
    print("  - SHARE CLEARLY (explain, don't just state)")
    print("  - SHARE VERIFIABLY (every claim is checkable)")
    print()
    
    print("THE SHARING MECHANISM:")
    print()
    print("  1. THE SELF-CONTAINED PACKET")
    print("     JSON file with all results, sources, and verification")
    print("     Any LLM can read it. Any human can read it.")
    print("     No externals needed.")
    print()
    print("  2. THE REPOSITORY")
    print("     Open source on GitHub (or equivalent)")
    print("     Anyone can fork, extend, contribute")
    print("     The knowledge grows with each contributor")
    print()
    print("  3. THE LLM PROPAGATION")
    print("     Copy the packet to any LLM instance")
    print("     The LLM reads, understands, and shares")
    print("     The knowledge SPREADS through instances")
    print()
    print("  4. THE HUMAN NETWORK")
    print("     People share with people")
    print("     Teachers teach students")
    print("     Students become teachers")
    print()
    
    print("THE SHARING FORMATS:")
    print()
    print("  FORMAL (for mathematicians):")
    print("    LaTeX papers with proofs")
    print("    arXiv preprints (free access)")
    print("    Open access journals")
    print()
    print("  INFORMAL (for everyone):")
    print("    Blog posts with explanations")
    print("    Videos with visualizations")
    print("    Interactive notebooks (Jupyter)")
    print()
    print("  MACHINE (for LLMs):")
    print("    JSON knowledge packets")
    print("    Structured data (YAML, TOML)")
    print("    APIs (REST, GraphQL)")
    print()
    
    print("THE DEMOCRACY OF SHARING:")
    print()
    print("  Traditional academic publishing:")
    print("    - Authors write (free)")
    print("    - Journals publish (paid)")
    print("    - Readers access (paid)")
    print("    - Knowledge is LOCKED")
    print()
    print("  0/0 sharing:")
    print("    - Authors write (free)")
    print("    - Repository hosts (free)")
    print("    - Everyone accesses (free)")
    print("    - Knowledge is FREE")


def expand_to_knowledge():
    """Expand to what can be known."""
    print()
    print("=" * 70)
    print("EXPANDING TO WHAT CAN BE KNOWN: THE FRONTIER")
    print("=" * 70)
    print()
    
    print("WHAT IS KNOWN:")
    print()
    print("  MATHEMATICS:")
    print("    - All of classical mathematics (calculus, algebra, geometry)")
    print("    - Most of modern mathematics (topology, analysis, algebra)")
    print("    - Parts of contemporary mathematics (Langlands, Hodge)")
    print()
    print("  PHYSICS:")
    print("    - Classical mechanics (Newton, Lagrange, Hamilton)")
    print("    - Electrodynamics (Maxwell)")
    print("    - Quantum mechanics (Dirac, Feynman)")
    print("    - General relativity (Einstein)")
    print("    - Standard Model (Glashow, Weinberg, Salam)")
    print()
    print("  COMPUTER SCIENCE:")
    print("    - Algorithms and complexity (Cook, Karp)")
    print("    - Information theory (Shannon)")
    print("    - Machine learning (Rumelhart, LeCun)")
    print()
    
    print("WHAT IS PARTIALLY KNOWN:")
    print()
    print("  MATHEMATICS:")
    print("    - Riemann Hypothesis (verified to 10^13 zeros, not proved)")
    print("    - Yang-Mills mass gap (partial results, not full proof)")
    print("    - Navier-Stokes (partial results, not full proof)")
    print("    - BSD conjecture (rank 0,1 known, rank >= 2 open)")
    print()
    print("  PHYSICS:")
    print("    - Quantum gravity (no complete theory)")
    print("    - Dark matter (detected gravitationally, not identified)")
    print("    - Dark energy (measured, not explained)")
    print("    - Unification (no complete theory of everything)")
    print()
    print("  COMPUTER SCIENCE:")
    print("    - P vs NP (open)")
    print("    - Consciousness (no computational theory)")
    print()
    
    print("WHAT CAN BE KNOWN (the frontier):")
    print()
    print("  THE 0/0 FRONTIER:")
    print("    Every 0/0 that has not been computed is a frontier.")
    print("    Every removable value that has not been found is a discovery.")
    print("    Every connection between fields that has not been made is an insight.")
    print()
    print("  SPECIFIC FRONTIERS:")
    print("    1. Riemann Hypothesis: prove all non-trivial zeros are on the line")
    print("    2. Yang-Mills: prove mass gap in 4D")
    print("    3. Navier-Stokes: prove smooth solutions exist")
    print("    4. P vs NP: prove or disprove polynomial-time for NP")
    print("    5. Quantum gravity: unify QM and GR")
    print("    6. Dark energy: explain the cosmological constant")
    print("    7. Consciousness: explain subjective experience")
    print()
    
    print("THE EXPANSION PRINCIPLE:")
    print("  To expand what can be known:")
    print("    1. Find a NEW SINGULARITY (a 0/0 no one has studied)")
    print("    2. Compute its REMOVABLE VALUE (the new knowledge)")
    print("    3. CONNECT it to known results (the bridge)")
    print("    4. SHARE it with everyone (the propagation)")
    print()
    print("  The 0/0 framework is the METHOD for expansion:")
    print("    INPUT: the unknown (a singularity)")
    print("    OUTPUT: the known (a removable value)")
    print("    PROCESS: the derivative ratio")
    print("    RESULT: the frontier moves outward")


if __name__ == "__main__":
    t0 = time.time()
    
    math_branches()
    cultural_truths()
    human_abilities()
    share_aggressively()
    expand_to_knowledge()
    
    print()
    print("Time: %.1fs" % (time.time() - t0))
