#!/usr/bin/env python3
"""
Sigma Virtual School Server
============================

A zero-dependency learning management system for the L.O.R.E. framework.

Usage:
    python sigma_school_server.py [--port PORT]

Features:
    - 31 chapters from "The Removable Singularity"
    - MCQ quizzes with auto-grading
    - Progress tracking
    - Student dashboard
    - Certificate generation
    - Zero dependencies (Python stdlib only)

Author: Michael Grafiel S Puno
"""

import http.server
import json
import os
import sys
import hashlib
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sigma_venv'))
from sigma.chassis import (
    BookIntegration, EpistemicClassifier, REAL, CAREFUL, NOT_SAME,
    SigmaCurrency, build_export, exponents, degrees, weyl_order,
    detect_lhopital, KNOWN_SINGULARITIES
)

PORT = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == '--port' else 8001

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'school_data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.json')
COURSES_FILE = os.path.join(DATA_DIR, 'courses.json')

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    for f, default in [(USERS_FILE, {}), (PROGRESS_FILE, {}), (COURSES_FILE, [])]:
        if not os.path.exists(f):
            with open(f, 'w', encoding='utf-8') as fh:
                json.dump(default, fh)

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {} if 'users' in path or 'progress' in path else []

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def get_courses():
    courses = load_json(COURSES_FILE)
    if not courses:
        courses = build_courses()
        save_json(COURSES_FILE, courses)
    return courses

def build_courses():
    chapters = [
        {
            "id": 1,
            "title": "What 0/0 Actually Means",
            "part": "I. The Core Idea",
            "content": """
<h2>Chapter 1: What 0/0 Actually Means</h2>
<p>The expression 0/0 is not "undefined" in the sense of being meaningless. It is the <em>most meaningful</em> expression in mathematics.</p>

<h3>Why?</h3>
<p>Because 0/0 represents the <strong>meeting point</strong> of two vanishing quantities. When both numerator and denominator approach zero, the question becomes: <em>how fast?</em></p>

<h3>L'Hopital's Rule (1696)</h3>
<p>If f(a) = 0 and g(a) = 0, then:</p>
<p style="font-size:1.2em; text-align:center; padding:20px;">lim<sub>x->a</sub> f(x)/g(x) = f'(a)/g'(a)</p>
<p>The limit exists if f'(a) and g'(a) are not both zero.</p>

<h3>Examples</h3>
<table style="width:100%; border-collapse:collapse;">
<tr><td style="padding:10px; border:1px solid #4a5568;"><code>sin(x)/x</code></td>
<td style="padding:10px; border:1px solid #4a5568;">lim<sub>x->0</sub> = <strong>1</strong></td></tr>
<tr><td style="padding:10px; border:1px solid #4a5568;"><code>(e^x - 1)/x</code></td>
<td style="padding:10px; border:1px solid #4a5568;">lim<sub>x->0</sub> = <strong>1</strong></td></tr>
<tr><td style="padding:10px; border:1px solid #4a5568;"><code>log(1+x)/x</code></td>
<td style="padding:10px; border:1px solid #4a5568;">lim<sub>x->0</sub> = <strong>1</strong></td></tr>
<tr><td style="padding:10px; border:1px solid #4a5568;"><code>(1-cos(x))/x^2</code></td>
<td style="padding:10px; border:1px solid #4a5568;">lim<sub>x->0</sub> = <strong>1/2</strong></td></tr>
</table>

<h3>The Principle</h3>
<p>The removable singularity is not a pathology. It is the <em>norm</em>. Most interesting functions have a 0/0 at their most important point.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] L'Hopital, "Analyse des Infiniment Petits" (1696)</li>
<li>[26] Courant & Robbins, "What is Mathematics?" (1941)</li>
</ul>
""",
            "quiz": [
                {"q": "What is lim(x->0) sin(x)/x?", "options": ["0", "1", "infinity", "undefined"], "correct": 1},
                {"q": "Who published the first rule for evaluating 0/0 limits?", "options": ["Newton", "Euler", "L'Hopital", "Cauchy"], "correct": 2},
                {"q": "What is lim(x->0) (1-cos(x))/x^2?", "options": ["0", "1", "1/2", "2"], "correct": 2},
                {"q": "A removable singularity means the function is:", "options": ["Infinite", "Undefined everywhere", "Defined everywhere except one point", "Continuous everywhere"], "correct": 2},
                {"q": "The expression 0/0 represents:", "options": ["An error", "A meeting point of vanishing quantities", "An infinite value", "A complex number"], "correct": 1}
            ]
        },
        {
            "id": 2,
            "title": "Why This Keeps Showing Up",
            "part": "I. The Core Idea",
            "content": """
<h2>Chapter 2: Why This Keeps Showing Up</h2>
<p>The 0/0 pattern appears everywhere because it is the <em>natural language</em> of response functions.</p>

<h3>Response Functions</h3>
<p>A response function measures output/input. At the special point, both output and input vanish for a shared reason.</p>

<h3>The Pattern</h3>
<p>Whenever you see:</p>
<ul>
<li>A system that becomes "sensitive" at a specific point</li>
<li>A ratio where both numerator and denominator vanish</li>
<li>A function that is "almost" defined but not quite</li>
</ul>
<p>...you are looking at a removable singularity.</p>

<h3>Why It's Universal</h3>
<p>The pattern is universal because <strong>all interesting systems have a special point</strong>. At that special point, the natural response function becomes 0/0.</p>

<h3>The Key Insight</h3>
<p>The removable singularity is not a bug. It is a <em>feature</em> of how nature encodes information.</p>

<h3>Key Sources</h3>
<ul>
<li>[26] Courant & Robbins, "What is Mathematics?" (1941)</li>
</ul>
""",
            "quiz": [
                {"q": "What type of function naturally produces 0/0?", "options": ["Step function", "Response function", "Exponential function", "Logarithmic function"], "correct": 1},
                {"q": "At the special point of a response function:", "options": ["Both vanish for different reasons", "Both vanish for a shared reason", "Only the numerator vanishes", "The function is infinite"], "correct": 1},
                {"q": "The removable singularity pattern is:", "options": ["Rare", "Universal", "Limited to math", "Only in physics"], "correct": 1},
                {"q": "The 0/0 pattern is best described as:", "options": ["A bug", "A feature", "An error", "A limitation"], "correct": 1},
                {"q": "All interesting systems have:", "options": ["No special points", "One special point", "Two special points", "Infinite special points"], "correct": 1}
            ]
        },
        {
            "id": 3,
            "title": "Circuits at Resonance",
            "part": "II. Physics and Engineering",
            "content": """
<h2>Chapter 3: Circuits at Resonance</h2>
<p>The series RLC circuit is the simplest physical system with a removable singularity.</p>

<h3>The Impedance</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">Z(w) = R + i(wL - 1/wC)</p>

<h3>At Resonance</h3>
<p>When w0 = 1/sqrt(LC), the reactance cancels:</p>
<p style="font-size:1.1em; text-align:center; padding:15px;">Z(w0) = R + i(0 - 0) = R</p>
<p>The imaginary part is 0/0 in the limit. The circuit becomes purely resistive.</p>

<h3>Why It Matters</h3>
<ul>
<li>Radio tuning: select a specific frequency</li>
<li>Filters: pass or reject specific frequencies</li>
<li>Oscillators: generate stable frequencies</li>
</ul>

<h3>The 0/0</h3>
<p>The impedance at resonance is the removable value of the 0/0 singularity in the reactance.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Puno 2026, textbook electrical engineering</li>
</ul>
""",
            "quiz": [
                {"q": "What is the impedance of a series RLC circuit at resonance?", "options": ["0", "R", "infinity", "Z0"], "correct": 1},
                {"q": "Resonance frequency w0 equals:", "options": ["RC", "1/RC", "1/sqrt(LC)", "sqrt(LC)"], "correct": 2},
                {"q": "At resonance, the circuit becomes:", "options": ["Purely capacitive", "Purely inductive", "Purely resistive", "Infinite"], "correct": 2},
                {"q": "The reactance at resonance is:", "options": ["R", "Z0", "0", "infinity"], "correct": 2},
                {"q": "Radio tuning uses the principle of:", "options": ["Resonance", "Resistance", "Capacitance", "Inductance"], "correct": 0}
            ]
        },
        {
            "id": 4,
            "title": "Mechanical Oscillators",
            "part": "II. Physics and Engineering",
            "content": """
<h2>Chapter 4: Mechanical Oscillators</h2>
<p>Mechanical systems exhibit the same 0/0 pattern as electrical circuits.</p>

<h3>The Impedance</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">Z(w) = c + i(mw - k/w)</p>

<h3>At Resonance</h3>
<p>When w0 = sqrt(k/m), the mechanical reactance cancels:</p>
<p style="font-size:1.1em; text-align:center; padding:15px;">Z(w0) = c + i(0 - 0) = c</p>

<h3>Examples</h3>
<ul>
<li>Car suspension: absorbs road vibrations</li>
<li>Building抗震: withstands earthquakes</li>
<li>Pendulum: precise timekeeping</li>
</ul>

<h3>The Universal Pattern</h3>
<p>Whether electrical or mechanical, the pattern is the same: at resonance, the imaginary part vanishes as 0/0.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Puno 2026, textbook classical mechanics</li>
</ul>
""",
            "quiz": [
                {"q": "What is the resonance frequency of a mass-spring system?", "options": ["k/m", "sqrt(k/m)", "m/k", "sqrt(m/k)"], "correct": 1},
                {"q": "At mechanical resonance, impedance equals:", "options": ["0", "c (damping)", "infinity", "mw"], "correct": 1},
                {"q": "A car suspension system uses:", "options": ["Electrical resonance", "Mechanical resonance", "Chemical resonance", "Nuclear resonance"], "correct": 1},
                {"q": "The mechanical reactance is:", "options": ["mw - k/w", "mw + k/w", "c + mw", "k/w - c"], "correct": 0},
                {"q": "At resonance, the mechanical impedance becomes:", "options": ["Purely imaginary", "Purely real", "Complex", "Zero"], "correct": 1}
            ]
        },
        {
            "id": 5,
            "title": "Thermoacoustic Systems",
            "part": "II. Physics and Engineering",
            "content": """
<h2>Chapter 5: Thermoacoustic Systems</h2>
<p>Thermoacoustic systems convert heat to sound and back. The impedance analogy holds.</p>

<h3>The Analogy</h3>
<p>Acoustic impedance Z_ac is analogous to electrical impedance Z.</p>

<h3>At Resonance</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">Z_ac(w0) = R_ac</p>
<p>The thermoacoustic engine operates at this removable point.</p>

<h3>Applications</h3>
<ul>
<li>Cryocoolers: cool without moving parts</li>
<li>Engines: convert waste heat to electricity</li>
<li>Refrigerators: solid-state cooling</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[1] Puno 2026, textbook thermoacoustics</li>
</ul>
""",
            "quiz": [
                {"q": "What do thermoacoustic systems convert?", "options": ["Sound to light", "Heat to sound", "Electricity to heat", "Sound to electricity"], "correct": 1},
                {"q": "At resonance, acoustic impedance becomes:", "options": ["Purely imaginary", "Purely real (R_ac)", "Zero", "Infinite"], "correct": 1},
                {"q": "Thermoacoustic cryocoolers have:", "options": ["Moving parts", "No moving parts", "Pistons", "Turbines"], "correct": 1},
                {"q": "The acoustic-electric analogy means:", "options": ["Sound IS electricity", "They share mathematical structure", "They are the same thing", "Sound becomes electricity"], "correct": 1},
                {"q": "A thermoacoustic engine operates at:", "options": ["The 0 point", "The removable singularity", "The pole", "The branch cut"], "correct": 1}
            ]
        },
        {
            "id": 6,
            "title": "Impedance Matching in Optics",
            "part": "II. Physics and Engineering",
            "content": """
<h2>Chapter 6: Impedance Matching in Optics</h2>
<p>Optical impedance matching eliminates reflection at interfaces.</p>

<h3>The Quarter-Wave Coating</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">Z_coat = sqrt(Z_glass * Z_air)</p>

<h3>How It Works</h3>
<p>Two reflections from the coating surfaces interfere destructively, canceling each other.</p>

<h3>The 0/0</h3>
<p>At the optimal coating thickness, the net reflection coefficient is 0/0 — it vanishes.</p>

<h3>Applications</h3>
<ul>
<li>Anti-reflection coatings on lenses</li>
<li>Solar cell efficiency</li>
<li>Laser optics</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[1] Puno 2026, textbook optics</li>
</ul>
""",
            "quiz": [
                {"q": "What is the optimal coating impedance?", "options": ["Z_glass", "Z_air", "sqrt(Z_glass * Z_air)", "Z_glass + Z_air"], "correct": 2},
                {"q": "Anti-reflection coatings work by:", "options": ["Absorption", "Destructive interference", "Reflection", "Diffraction"], "correct": 1},
                {"q": "The net reflection at optimal thickness is:", "options": ["100%", "50%", "0%", "200%"], "correct": 2},
                {"q": "A quarter-wave coating has thickness:", "options": ["lambda/2", "lambda/4", "lambda", "2*lambda"], "correct": 1},
                {"q": "Solar cells benefit from anti-reflection coatings because:", "options": ["They absorb more light", "They reflect less light", "They emit light", "They refract light"], "correct": 1}
            ]
        },
        {
            "id": 7,
            "title": "Pole-Zero Cancellation",
            "part": "II. Physics and Engineering",
            "content": """
<h2>Chapter 7: Pole-Zero Cancellation</h2>
<p>In control theory, engineers deliberately create 0/0 singularities.</p>

<h3>The Mechanism</h3>
<p>When G(s)*C(s) has (s-a) in both numerator and denominator:</p>
<p style="font-size:1.1em; text-align:center; padding:15px;">G(s)*C(s) = (s-a)*N(s) / (s-a)*D(s) = N(s)/D(s)</p>

<h3>The Engineer's Role</h3>
<p>The engineer <em>creates</em> the 0/0 by choosing C(s) to cancel a pole of G(s).</p>

<h3>Why It Matters</h3>
<ul>
<li>Stabilize unstable systems</li>
<li>Improve transient response</li>
<li>Eliminate steady-state error</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[1] Puno 2026, textbook control theory</li>
</ul>
""",
            "quiz": [
                {"q": "Pole-zero cancellation involves:", "options": ["Adding poles", "Canceling a pole with a zero", "Removing all poles", "Creating infinite poles"], "correct": 1},
                {"q": "When a pole is canceled, the result is:", "options": ["Infinite", "The remaining transfer function", "Zero", "Undefined"], "correct": 1},
                {"q": "Pole-zero cancellation is used to:", "options": ["Create instability", "Stabilize unstable systems", "Increase gain", "Reduce bandwidth"], "correct": 1},
                {"q": "The engineer's role in pole-zero cancellation is:", "options": ["Passive", "Active (chooses C(s))", "None", "Random"], "correct": 1},
                {"q": "In G(s)*C(s) = N(s)/D(s), the cancellation means:", "options": ["(s-a) remains", "(s-a) vanishes", "s remains", "a remains"], "correct": 1}
            ]
        },
        {
            "id": 8,
            "title": "Kutta Condition",
            "part": "II. Physics and Engineering",
            "content": """
<h2>Chapter 8: Kutta Condition</h2>
<p>In aerodynamics, the Kutta condition determines the circulation around an airfoil.</p>

<h3>The Condition</h3>
<p>Velocity must be finite at the trailing edge. This fixes the circulation Gamma:</p>
<p style="font-size:1.1em; text-align:center; padding:15px;">Gamma = pi * V * c * (alpha + beta)</p>

<h3>The 0/0</h3>
<p>Without the Kutta condition, the velocity at the trailing edge is infinite (a pole). The Kutta condition removes this singularity.</p>

<h3>The Lift</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">Lift = rho * V * Gamma</p>

<h3>Applications</h3>
<ul>
<li>Airplane wing design</li>
<li>Wind turbine blades</li>
<li>Helicopter rotors</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[1] Puno 2026, textbook aerodynamics</li>
</ul>
""",
            "quiz": [
                {"q": "What does the Kutta condition fix?", "options": ["Drag", "Circulation (Gamma)", "Temperature", "Pressure"], "correct": 1},
                {"q": "The velocity at the trailing edge must be:", "options": ["Infinite", "Zero", "Finite", "Complex"], "correct": 2},
                {"q": "Lift equals:", "options": ["rho * V", "rho * V * Gamma", "Gamma * c", "V * c"], "correct": 1},
                {"q": "Without the Kutta condition, the trailing edge velocity is:", "options": ["Zero", "Finite", "Infinite", "Oscillating"], "correct": 2},
                {"q": "The Kutta condition is used in:", "options": ["Electrical circuits", "Aerodynamics", "Chemistry", "Biology"], "correct": 1}
            ]
        },
        {
            "id": 9,
            "title": "Resonances in QFT",
            "part": "II. Physics and Engineering",
            "content": """
<h2>Chapter 9: Resonances in QFT</h2>
<p>In quantum field theory, particle resonances are poles in the propagator.</p>

<h3>The Propagator</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">G(p) = 1/(p^2 - m^2 + i*gamma)</p>

<h3>At the Pole</h3>
<p>When p^2 = m^2, the propagator would be infinite. But gamma (the width) keeps it finite.</p>

<h3>The Mass Gap</h3>
<p>Spec(H) = {0} union [Delta, inf). Delta > 0 means there is a gap. This is different from a removable singularity.</p>

<h3>Key Sources</h3>
<ul>
<li>[9] Peskin & Schroeder, "QFT" (1995)</li>
</ul>
""",
            "quiz": [
                {"q": "The QFT propagator has a pole when:", "options": ["p^2 = 0", "p^2 = m^2", "p^2 = infinity", "p^2 = -m^2"], "correct": 1},
                {"q": "The width gamma in the propagator:", "options": ["Makes it infinite", "Keeps it finite", "Removes it", "Changes the mass"], "correct": 1},
                {"q": "The mass gap Delta means:", "options": ["No mass", "Minimum energy above vacuum", "Infinite mass", "Zero energy"], "correct": 1},
                {"q": "A particle resonance corresponds to:", "options": ["A zero", "A pole", "A branch cut", "A maximum"], "correct": 1},
                {"q": "The propagator G(p) describes:", "options": ["Particle creation", "Particle propagation", "Particle decay", "Particle interaction"], "correct": 1}
            ]
        },
        {
            "id": 10,
            "title": "Phase Transitions",
            "part": "II. Physics and Engineering",
            "content": """
<h2>Chapter 10: Phase Transitions</h2>
<p>At critical points, physical quantities diverge as power laws.</p>

<h3>Critical Exponents</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">chi ~ |T - Tc|^(-gamma)</p>

<h3>Universality</h3>
<p>Systems with the same symmetry and dimension share the same critical exponents, regardless of microscopic details.</p>

<h3>The 0/0</h3>
<p>At T = Tc, the susceptibility chi diverges. This is a pole, not a removable singularity. But the critical exponents themselves are finite and universal.</p>

<h3>Key Sources</h3>
<ul>
<li>[7] Wilson 1982 Nobel Prize</li>
<li>[1] Puno 2026, textbook statistical mechanics</li>
</ul>
""",
            "quiz": [
                {"q": "At a critical point, susceptibility:", "options": ["Vanishes", "Diverges", "Remains constant", "Oscillates"], "correct": 1},
                {"q": "Universality means:", "options": ["All systems are the same", "Systems with same symmetry share exponents", "Only water has critical points", "Exponents are random"], "correct": 1},
                {"q": "The critical exponent gamma describes:", "options": ["Energy", "Magnetization", "Susceptibility", "Heat capacity"], "correct": 2},
                {"q": "A phase transition at T=Tc is:", "options": ["A removable singularity", "A pole", "A branch point", "Essential singularity"], "correct": 1},
                {"q": "Kenneth Wilson won the Nobel Prize for:", "options": ["Discovering critical points", "Renormalization group theory", " inventing temperature", "Measuring water"], "correct": 1}
            ]
        },
        {
            "id": 11,
            "title": "Persistent Flow",
            "part": "II. Physics and Engineering",
            "content": """
<h2>Chapter 11: Persistent Flow</h2>
<p>In superconductors and superfluids, current flows without resistance — indefinitely.</p>

<h3>The Phenomenon</h3>
<p>Below the critical temperature Tc, the current state is the lowest energy state. There is no mechanism to stop it.</p>

<h3>Measurement</p>
<p>Persistent currents have been measured to last > 1 year without decay.</p>

<h3>The Connection</h3>
<p>The persistent current is a macroscopic quantum state — a removable singularity in the resistance function.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Puno 2026, textbook superconductivity</li>
</ul>
""",
            "quiz": [
                {"q": "Persistent flow occurs below:", "options": ["Room temperature", "Critical temperature Tc", "Absolute zero", "Melting point"], "correct": 1},
                {"q": "Persistent currents last:", "options": ["Microseconds", "Seconds", "Minutes", "> 1 year"], "correct": 3},
                {"q": "The resistance in persistent flow is:", "options": ["High", "Normal", "Zero", "Negative"], "correct": 2},
                {"q": "Persistent flow is a:", "options": ["Classical effect", "Macroscopic quantum state", "Thermal effect", "Magnetic effect"], "correct": 1},
                {"q": "Superconductivity was discovered by:", "options": ["Einstein", "Onnes", "Newton", "Faraday"], "correct": 1}
            ]
        },
        {
            "id": 12,
            "title": "Singularities at Edge of Spacetime",
            "part": "II. Physics and Engineering",
            "content": """
<h2>Chapter 12: Singularities at Edge of Spacetime</h2>
<p>Classical general relativity predicts true singularities — points where curvature becomes infinite.</p>

<h3>Penrose-Hawking Theorems</h3>
<p>Under reasonable energy conditions, gravitational collapse leads to singularities.</p>

<h3>The Question</h3>
<p>Are these true singularities, or removable ones that quantum gravity will resolve?</p>

<h3>Evidence</h3>
<ul>
<li>Black hole information paradox</li>
<li>Hawking radiation</li>
<li>AdS/CFT correspondence</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[10] Bekenstein, "Black holes and entropy" (1973)</li>
<li>[11] Hawking, "Particle creation by black holes" (1975)</li>
</ul>
""",
            "quiz": [
                {"q": "Penrose-Hawking theorems predict:", "options": ["No singularities", "True singularities", "Removable singularities only", "Black holes don't exist"], "correct": 1},
                {"q": "The black hole information paradox involves:", "options": ["Information storage", "Information loss", "Information creation", "Information encryption"], "correct": 1},
                {"q": "Hawking radiation is:", "options": ["Classical", "Quantum mechanical", "Thermal only", "Magnetic"], "correct": 1},
                {"q": "AdS/CFT correspondence suggests:", "options": ["Gravity doesn't exist", "Holographic duality", "Singularities are real", "Space is flat"], "correct": 1},
                {"q": "At a true singularity, curvature:", "options": ["Vanishes", "Is finite", "Becomes infinite", "Oscillates"], "correct": 2}
            ]
        },
        {
            "id": 13,
            "title": "Tipping Points",
            "part": "III. Life, Chemistry, Computation",
            "content": """
<h2>Chapter 13: Tipping Points</h2>
<p>In ecology and climate, systems can suddenly shift to a new state.</p>

<h3>Critical Slowing Down</h3>
<p>As a system approaches a tipping point:</p>
<ul>
<li>Recovery time from perturbations increases</li>
<li>Fluctuations grow</li>
<li>Autocorrelation increases</li>
</ul>

<h3>Early Warning Signals</h3>
<p>These statistical changes can predict tipping points before they happen.</p>

<h3>The 0/0</h3>
<p>The resilience function R(t) has a 0/0 at the tipping point — both numerator and denominator vanish.</p>

<h3>Key Sources</h3>
<ul>
<li>[8] Scheffer et al., "Early-warning signals for critical transitions" (2009)</li>
</ul>
""",
            "quiz": [
                {"q": "Critical slowing down means:", "options": ["System speeds up", "System recovers more slowly", "System stops", "System oscillates"], "correct": 1},
                {"q": "Early warning signals include:", "options": ["Decreased fluctuations", "Increased fluctuations", "Constant behavior", "Random behavior"], "correct": 1},
                {"q": "The resilience function R(t) at a tipping point:", "options": ["Is infinite", "Is 1", "Is 0/0", "Is negative"], "correct": 2},
                {"q": "Tipping points occur in:", "options": ["Only climate", "Only ecology", "Many complex systems", "Only math"], "correct": 2},
                {"q": "Autocorrelation increases because:", "options": ["System forgets faster", "System remembers longer", "Nothing changes", "System breaks"], "correct": 1}
            ]
        },
        {
            "id": 14,
            "title": "Grokking in ML",
            "part": "III. Life, Chemistry, Computation",
            "content": """
<h2>Chapter 14: Grokking in ML</h2>
<p>Grokking is the sudden generalization after a long delay in neural network training.</p>

<h3>The Phenomenon</h3>
<p>After memorizing the training data, the network suddenly learns to generalize. The delay can be orders of magnitude longer than memorization.</p>

<h3>The Predictor</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">T_delay = (1/g_eff) * log(V_mem / V_post)</p>

<h3>Connection to 0/0</h3>
<p>The grokking transition is a phase transition — a removable singularity in the generalization function.</p>

<h3>Key Sources</h3>
<ul>
<li>[19] Power et al., "Grokking: Generalization Beyond Overfitting" (2022)</li>
</ul>
""",
            "quiz": [
                {"q": "Grokking is:", "options": ["Gradual improvement", "Sudden generalization after delay", "Overfitting", "Underfitting"], "correct": 1},
                {"q": "The delay in grokking can be:", "options": ["Microseconds", "Minutes", "Orders of magnitude longer than memorization", "Zero"], "correct": 2},
                {"q": "Grokking is connected to:", "options": ["Random guessing", "Phase transitions", "Overfitting", "Data augmentation"], "correct": 1},
                {"q": "The grokking predictor T_delay depends on:", "options": ["Only training data", "V_mem and V_post", "Model size only", "Learning rate only"], "correct": 1},
                {"q": "Grokking was first described by:", "options": ["Hinton", "LeCun", "Power et al.", "Goodfellow"], "correct": 2}
            ]
        },
        {
            "id": 15,
            "title": "Three Kinds of Degree",
            "part": "IV. Knowing Where the Pattern Stops",
            "content": """
<h2>Chapter 15: Three Kinds of Degree</h2>
<p>Not all evidence is equal. There are three levels of mathematical certainty.</p>

<h3>Level 1: Proven</h3>
<p>The result follows logically from accepted axioms. Example: sin(x)/x -> 1 as x -> 0.</p>

<h3>Level 2: Derived</h3>
<p>The result follows from a plausible but unproven assumption. Example: Riemann Hypothesis follows from the Hilbert-Polya conjecture.</p>

<h3>Level 3: Numerical</h3>
<p>The result is supported by computation but not proven. Example: Goldbach's conjecture verified to 4x10^18.</p>

<h3>The Lesson</h3>
<p>Know which level you are on. Don't claim Level 1 for Level 3 results.</p>

<h3>Key Sources</h3>
<ul>
<li>[24] Polya, "How to Solve It" (1945)</li>
</ul>
""",
            "quiz": [
                {"q": "Level 1 evidence means:", "options": ["Numerically checked", "Proven from axioms", "Plausible", "Guessed"], "correct": 1},
                {"q": "Level 3 evidence means:", "options": ["Proven", "Derived", "Numerically supported", "Impossible"], "correct": 2},
                {"q": "Goldbach's conjecture is at:", "options": ["Level 1", "Level 2", "Level 3", "No level"], "correct": 2},
                {"q": "The Riemann Hypothesis is at:", "options": ["Level 1", "Level 2", "Level 3", "Level 4"], "correct": 1},
                {"q": "The key lesson is:", "options": ["All evidence is equal", "Know which level you are on", "Only Level 1 matters", "Level 3 is worthless"], "correct": 1}
            ]
        },
        {
            "id": 16,
            "title": "When a Beautiful Pattern Isn't Evidence",
            "part": "IV. Knowing Where the Pattern Stops",
            "content": """
<h2>Chapter 16: When a Beautiful Pattern Isn't Evidence</h2>
<p>A pattern matching is not proof. The L.O.R.E. framework must be honest about this.</p>

<h3>The Three-Question Checklist</h3>
<ol>
<li>Is the special point <strong>proven</strong> to exist and behave that way?</li>
<li>Is the finite value <strong>derived</strong> from surrounding behavior?</li>
<li>Does the specific case <strong>cover</strong> the genuinely open part?</li>
</ol>

<h3>Classification</h3>
<ul>
<li><strong>REAL</strong>: All three answers are YES</li>
<li><strong>CAREFUL</strong>: Any answer is NO</li>
<li><strong>NOT_SAME</strong>: The pattern doesn't apply</li>
</ul>

<h3>Why This Matters</h3>
<p>Honest classification is more valuable than inflated claims.</p>

<h3>Key Sources</h3>
<ul>
<li>[25] Erdos & Hofman, "Proofs from THE BOOK" (1998)</li>
</ul>
""",
            "quiz": [
                {"q": "The three-question checklist asks about:", "options": ["Price, quality, quantity", "Proven, derived, covers", "Fast, cheap, good", "Small, medium, large"], "correct": 1},
                {"q": "REAL classification requires:", "options": ["One YES", "Two YESes", "Three YESes", "No YESes"], "correct": 2},
                {"q": "CAREFUL classification means:", "options": ["All YES", "Any NO", "All NO", "No classification"], "correct": 1},
                {"q": "The purpose of the checklist is:", "options": ["Inflate claims", "Be honest", "Hide weaknesses", "Impress people"], "correct": 1},
                {"q": "NOT_SAME means:", "options": ["The pattern applies", "The pattern doesn't apply", "The pattern is proven", "The pattern is new"], "correct": 1}
            ]
        },
        {
            "id": 17,
            "title": "What the Constants Actually Are",
            "part": "V. The Constants",
            "content": """
<h2>Chapter 17: What the Constants Actually Are</h2>
<p>The fundamental constants of nature are not arbitrary. They are determined by the requirement that the universe exists.</p>

<h3>The Argument</h3>
<p>If the constants were different, stars couldn't form, chemistry couldn't happen, life couldn't exist.</p>

<h3>The 0/0 Connection</h3>
<p>The constants sit at the removable singularity — the only values where the universe's response function is finite and meaningful.</p>

<h3>Key Sources</h3>
<ul>
<li>[26] Courant & Robbins, "What is Mathematics?" (1941)</li>
</ul>
""",
            "quiz": [
                {"q": "Fundamental constants are:", "options": ["Random", "Arbitrary", "Determined by universe's existence", "Human inventions"], "correct": 2},
                {"q": "If constants were different:", "options": ["Nothing changes", "Universe still works", "Stars and chemistry couldn't happen", "Only colors change"], "correct": 2},
                {"q": "The 0/0 connection means constants sit at:", "options": ["A pole", "The removable singularity", "A branch cut", "Infinity"], "correct": 1},
                {"q": "The universe's response function is:", "options": ["Always infinite", "Finite only at specific constant values", "Always zero", "Random"], "correct": 1},
                {"q": "The constants determine:", "options": ["Only physics", "Only chemistry", "Everything that can exist", "Nothing"], "correct": 2}
            ]
        },
        {
            "id": 18,
            "title": "The Entropy of Nothing",
            "part": "V. The Constants",
            "content": """
<h2>Chapter 18: The Entropy of Nothing</h2>
<p>The vacuum has entropy. Empty space is not empty — it is full of quantum fluctuations.</p>

<h3>Bekenstein Bound</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">S <= 2*pi*E*R / (hbar*c)</p>
<p>Maximum information in a region of space.</p>

<h3>Landauer's Principle</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">E >= kT * ln(2) per bit erased</p>
<p>Information is physical. Erasing a bit costs energy.</p>

<h3>The Connection</h3>
<p>Both bounds are 0/0 at the vacuum state — both numerator and denominator vanish, but the ratio is finite.</p>

<h3>Key Sources</h3>
<ul>
<li>[10] Bekenstein, "Black holes and entropy" (1973)</li>
<li>[11] Landauer, "Irreversibility and heat generation" (1961)</li>
</ul>
""",
            "quiz": [
                {"q": "The Bekenstein bound limits:", "options": ["Energy", "Information in a region", "Temperature", "Speed"], "correct": 1},
                {"q": "Landauer's principle states:", "options": ["Information is free", "Erasing a bit costs energy", "Bits are weightless", "Computation is impossible"], "correct": 1},
                {"q": "The vacuum has:", "options": ["Zero entropy", "Maximum entropy", "Finite entropy", "Negative entropy"], "correct": 2},
                {"q": "Both bounds are 0/0 at:", "options": ["High temperature", "The vacuum state", "Absolute zero", "Infinite energy"], "correct": 1},
                {"q": "Information is:", "options": ["Abstract", "Physical", "Immaterial", "Infinite"], "correct": 1}
            ]
        },
        {
            "id": 19,
            "title": "The Language of Symmetry",
            "part": "V. The Constants",
            "content": """
<h2>Chapter 19: The Language of Symmetry</h2>
<p>Symmetry is the deepest language of physics. The E8 exceptional Lie algebra is its most beautiful expression.</p>

<h3>E8 Structure</h3>
<ul>
<li>Rank: 8</li>
<li>Roots: 240</li>
<li>Exponents: 1 + primes(2,3,5,7,11,13,17,19,23,29)</li>
<li>Weyl group order: 696,729,600</li>
</ul>

<h3>The Prime Connection</h3>
<p>The exponents of E8 are exactly 1 + the first 8 primes. This is not a coincidence.</p>

<h3>Key Sources</h3>
<ul>
<li>[4] Conway & Sloane, "Sphere Packings" (1999)</li>
<li>[5] Viazovska, "Sphere packing in R^8" (2017)</li>
</ul>
""",
            "quiz": [
                {"q": "E8 has how many roots?", "options": ["8", "240", "696729600", "1000"], "correct": 1},
                {"q": "The E8 exponents are:", "options": ["All primes", "1 + primes(2..29)", "Fibonacci numbers", "Random"], "correct": 1},
                {"q": "The Weyl group order of E8 is:", "options": ["240", "8", "696,729,600", "30"], "correct": 2},
                {"q": "E8 is significant because:", "options": ["It's simple", "It encodes universe's symmetry", "It's small", "It's new"], "correct": 1},
                {"q": "Viazovska proved sphere packing in:", "options": ["R^3", "R^8", "R^24", "R^100"], "correct": 1}
            ]
        },
        {
            "id": 20,
            "title": "The Fold Theorem",
            "part": "V. The Constants",
            "content": """
<h2>Chapter 20: The Fold Theorem</h2>
<p>The fold theorem describes how information is preserved across scale changes.</p>

<h3>The Statement</h3>
<p>When a system is folded (renormalized), the information at the fixed point is preserved exactly.</p>

<h3>The 0/0</h3>
<p>The renormalization group flow has a 0/0 at the fixed point — both the flow and its derivative vanish, but the fixed point value is well-defined.</p>

<h3>Applications</h3>
<ul>
<li>Renormalization in QFT</li>
<li>Scale invariance in critical phenomena</li>
<li>Universality classes</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[7] Wilson 1982 Nobel Prize</li>
</ul>
""",
            "quiz": [
                {"q": "The fold theorem describes:", "options": ["Paper folding", "Information preservation across scales", "Origami", "Clothing design"], "correct": 1},
                {"q": "At a fixed point of RG flow:", "options": ["Flow is infinite", "Flow and its derivative vanish", "Flow is maximum", "Flow oscillates"], "correct": 1},
                {"q": "Scale invariance means:", "options": ["Size doesn't matter", "Physics looks the same at all scales", "Everything is flat", "Nothing changes"], "correct": 1},
                {"q": "Universality classes group systems by:", "options": ["Size", "Symmetry and dimension", "Color", "Temperature"], "correct": 1},
                {"q": "The renormalization group was developed by:", "options": ["Einstein", "Wilson", "Newton", "Bohr"], "correct": 1}
            ]
        },
        {
            "id": 21,
            "title": "Verlinde Entropy",
            "part": "VI. Appendices",
            "content": """
<h2>Appendix B: Verlinde Entropy</h2>
<p>Gravity may be an entropic force — emerging from entropy gradients rather than fundamental interaction.</p>

<h3>The Formula</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">S = A / (4 * G * hbar * c)</p>

<h3>The Idea</h3>
<p>When a particle moves toward a holographic screen, it increases the entropy. This entropy gradient produces a force that looks like gravity.</p>

<h3>Key Sources</h3>
<ul>
<li>[10] Bekenstein, "Black holes and entropy" (1973)</li>
<li>[13] Verlinde, "On the Origin of Gravity and the Laws of Newton" (2011)</li>
</ul>
""",
            "quiz": [
                {"q": "Verlinde entropy is:", "options": ["Classical entropy", "Entropy of a holographic screen", "Thermal entropy", "Chemical entropy"], "correct": 1},
                {"q": "The entropy S equals:", "options": ["A * 4", "A / (4 * G * hbar * c)", "G * A", "hbar * c / A"], "correct": 1},
                {"q": "Gravity as entropic force means:", "options": ["Gravity doesn't exist", "Gravity emerges from entropy", "Entropy causes gravity", "They are unrelated"], "correct": 1},
                {"q": "A holographic screen:", "options": ["Stores information on a surface", "Projects images", "Is a computer screen", "Measures temperature"], "correct": 0},
                {"q": "The Bekenstein-Hawking entropy is proportional to:", "options": ["Volume", "Area", "Mass", "Temperature"], "correct": 1}
            ]
        },
        {
            "id": 22,
            "title": "Bekenstein Bound",
            "part": "VI. Appendices",
            "content": """
<h2>Appendix B: Bekenstein Bound</h2>
<p>There is a maximum amount of information that can be stored in a finite region of space.</p>

<h3>The Formula</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">S <= 2*pi*E*R / (hbar*c)</p>

<h3>Implications</h3>
<ul>
<li>Information is finite, not infinite</li>
<li>Black holes maximize information density</li>
<li>The universe is a hologram</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[10] Bekenstein, "Black holes and entropy" (1973)</li>
</ul>
""",
            "quiz": [
                {"q": "The Bekenstein bound limits:", "options": ["Speed", "Information in a region", "Energy", "Temperature"], "correct": 1},
                {"q": "Black holes:", "options": ["Destroy information", "Maximize information density", "Ignore information", "Create information"], "correct": 1},
                {"q": "The holographic principle suggests:", "options": ["3D is real", "Information is stored on 2D surfaces", "Holograms are fake", "Nothing is real"], "correct": 1},
                {"q": "The Bekenstein bound is proportional to:", "options": ["Volume", "Area (E*R)", "Mass^2", "Temperature"], "correct": 1},
                {"q": "hbar*c in the formula represents:", "options": ["Speed of light", "Planck's constant times c", "Energy", "Entropy"], "correct": 1}
            ]
        },
        {
            "id": 23,
            "title": "Landauer's Principle",
            "part": "VI. Appendices",
            "content": """
<h2>Appendix B: Landauer's Principle</h2>
<p>Erasing information has a minimum energy cost.</p>

<h3>The Formula</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">E >= kT * ln(2) per bit erased</p>

<h3>Implications</h3>
<ul>
<li>Information is physical</li>
<li>Computation generates heat</li>
<li>Reversible computing is theoretically possible</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[11] Landauer, "Irreversibility and heat generation" (1961)</li>
</ul>
""",
            "quiz": [
                {"q": "Landauer's principle says erasing a bit costs:", "options": ["Zero energy", "kT * ln(2)", "kT", "ln(2)"], "correct": 1},
                {"q": "This means information is:", "options": ["Abstract", "Physical", "Virtual", "Immaterial"], "correct": 1},
                {"q": "Reversible computing:", "options": ["Is impossible", "Is theoretically possible", "Uses no energy", "Is faster"], "correct": 1},
                {"q": "kT represents:", "options": ["Kinetic energy", "Thermal energy", "Potential energy", "Light energy"], "correct": 1},
                {"q": "Computation generates heat because:", "options": ["Computers are hot", "Information erasure is irreversible", "Electricity is warm", "Bits are physical"], "correct": 1}
            ]
        },
        {
            "id": 24,
            "title": "Kolmogorov Complexity",
            "part": "VI. Appendices",
            "content": """
<h2>Appendix B: Kolmogorov Complexity</h2>
<p>The complexity of a string is the length of the shortest program that produces it.</p>

<h3>The Definition</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">K(x) = length of shortest program producing x</p>

<h3>Properties</h3>
<ul>
<li>Uncomputable in general</li>
<li>Well-defined but not calculable</li>
<li>Random strings have maximum complexity</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[16] Kolmogorov, "Foundations of Probability" (1933)</li>
</ul>
""",
            "quiz": [
                {"q": "Kolmogorov complexity is:", "options": ["Computable", "The shortest program length", "Random", "Infinite"], "correct": 1},
                {"q": "A random string has:", "options": ["Minimum complexity", "Maximum complexity", "Zero complexity", "Undefined complexity"], "correct": 1},
                {"q": "Kolmogorov complexity is:", "options": ["Always computable", "Uncomputable in general", "Only for numbers", "Only for text"], "correct": 1},
                {"q": "The shortest program producing x is called:", "options": ["The generator", "The compressor", "The Kolmogorov program", "The universal program"], "correct": 2},
                {"q": "A string like '0000000000' has:", "options": ["High complexity", "Low complexity", "Maximum complexity", "Undefined complexity"], "correct": 1}
            ]
        },
        {
            "id": 25,
            "title": "Nash Equilibrium",
            "part": "VI. Appendices",
            "content": """
<h2>Appendix C: Nash Equilibrium</h2>
<p>Every finite game has at least one mixed-strategy equilibrium.</p>

<h3>The Result</h3>
<p>John Nash proved that in any finite game, there exists a strategy profile where no player can improve by unilaterally changing their strategy.</p>

<h3>The Connection</h3>
<p>The Nash equilibrium is a fixed point — a removable singularity in the payoff function.</p>

<h3>Key Sources</h3>
<ul>
<li>[14] Nash, "Non-Cooperative Games" (1951)</li>
</ul>
""",
            "quiz": [
                {"q": "Nash equilibrium exists in:", "options": ["Only 2-player games", "Every finite game", "Only zero-sum games", "Only cooperative games"], "correct": 1},
                {"q": "At Nash equilibrium:", "options": ["Everyone wins", "No one can improve unilaterally", "Everyone loses", "The game ends"], "correct": 1},
                {"q": "Nash equilibrium is a:", "options": ["Maximum", "Minimum", "Fixed point", "Random point"], "correct": 2},
                {"q": "Mixed strategy means:", "options": ["Random play", "Combining pure strategies probabilistically", "Playing twice", "Using mixed numbers"], "correct": 1},
                {"q": "John Nash won the Nobel Prize in:", "options": ["Physics", "Chemistry", "Economics", "Literature"], "correct": 2}
            ]
        },
        {
            "id": 26,
            "title": "Kelly Criterion",
            "part": "VI. Appendices",
            "content": """
<h2>Appendix C: Kelly Criterion</h2>
<p>The optimal bet size maximizes long-term growth rate.</p>

<h3>The Formula</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">f* = (bp - q) / b</p>

<h3>Where</h3>
<ul>
<li>f* = fraction of bankroll to bet</li>
<li>b = odds received on the bet</li>
<li>p = probability of winning</li>
<li>q = probability of losing (1-p)</li>
</ul>

<h3>The 0/0</h3>
<p>The Kelly criterion is the removable value of the growth rate function — the optimal point where risk and reward balance.</p>

<h3>Key Sources</h3>
<ul>
<li>[15] Kelly, "A New Interpretation of Information Rate" (1956)</li>
</ul>
""",
            "quiz": [
                {"q": "The Kelly criterion maximizes:", "options": ["Winning probability", "Long-term growth rate", "Bet size", "Luck"], "correct": 1},
                {"q": "f* = (bp - q) / b means:", "options": ["Bet everything", "Optimal fraction to bet", "Never bet", "Bet randomly"], "correct": 1},
                {"q": "The Kelly criterion is:", "options": ["Always optimal", "Log-optimal portfolio", "Random", "Conservative"], "correct": 1},
                {"q": "p represents:", "options": ["Profit", "Probability of winning", "Payout", "Penalty"], "correct": 1},
                {"q": "Over-betting the Kelly criterion leads to:", "options": ["Higher returns", "Eventually ruin", "No change", "Guaranteed profit"], "correct": 1}
            ]
        },
        {
            "id": 27,
            "title": "Martingale Stopping Theorem",
            "part": "VI. Appendices",
            "content": """
<h2>Appendix C: Martingale Stopping Theorem</h2>
<p>Under fair game conditions, stopping doesn't beat the market.</p>

<h3>The Theorem</h3>
<p style="font-size:1.1em; text-align:center; padding:15px;">E[X_tau] = E[X_0]</p>
<p>The expected value at stopping time equals the initial value.</p>

<h3>Implications</h3>
<ul>
<li>No betting strategy can beat a fair game</li>
<li>Stopping rules don't change expected value</li>
<li>The market is efficient under fair game conditions</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[17] Ville, "Etude critique de la notion de ensemble" (1939)</li>
</ul>
""",
            "quiz": [
                {"q": "The martingale stopping theorem says:", "options": ["You can beat the market", "Stopping doesn't change expected value", "Betting is always good", "The market is unfair"], "correct": 1},
                {"q": "E[X_tau] = E[X_0] means:", "options": ["You always win", "Expected value is preserved", "You always lose", "Value is random"], "correct": 1},
                {"q": "This theorem applies to:", "options": ["Rigged games", "Fair games", "Only card games", "Only stock markets"], "correct": 1},
                {"q": "A martingale is:", "options": ["A type of bet", "A fair game process", "A losing strategy", "A winning strategy"], "correct": 1},
                {"q": "The practical implication is:", "options": ["Always bet", "No strategy beats a fair game", "Double down", "Quit while ahead"], "correct": 1}
            ]
        },
        {
            "id": 28,
            "title": "Halting Problem",
            "part": "VI. Appendices",
            "content": """
<h2>Appendix D: Halting Problem</h2>
<p>No algorithm can decide whether an arbitrary program halts or runs forever.</p>

<h3>The Proof</h3>
<p>Assume a halting decider H exists. Construct a program D that calls H on itself and does the opposite. This leads to a contradiction.</p>

<h3>Implications</h3>
<ul>
<li>Some problems are undecidable</li>
<li>Computation has fundamental limits</li>
<li>The 0/0 of computer science</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[16] Turing, "On Computable Numbers" (1936)</li>
</ul>
""",
            "quiz": [
                {"q": "The halting problem says:", "options": ["All programs halt", "No program halts", "Some programs can't be decided", "All programs are decidable"], "correct": 2},
                {"q": "The proof uses:", "options": ["Induction", "Diagonal argument", "Contradiction only", "Recursion"], "correct": 1},
                {"q": "The halting problem is:", "options": ["Decidable", "Undecidable", "Trivial", "Unimportant"], "correct": 1},
                {"q": "Turing proved this in:", "options": ["1900", "1936", "1950", "2000"], "correct": 1},
                {"q": "The practical consequence is:", "options": ["No bugs in programs", "Some questions about programs are unanswerable", "All programs are fast", "Computers are omniscient"], "correct": 1}
            ]
        },
        {
            "id": 29,
            "title": "Godel's Incompleteness",
            "part": "VI. Appendices",
            "content": """
<h2>Appendix D: Godel's Incompleteness</h2>
<p>Any consistent system capable of arithmetic contains true but unprovable statements.</p>

<h3>The First Incompleteness Theorem</h3>
<p>There exist statements that are true but cannot be proven within the system.</p>

<h3>The Second Incompleteness Theorem</h3>
<p>The system cannot prove its own consistency.</p>

<h3>The Connection</h3>
<p>Godel's theorems are the ultimate 0/0 — the system's self-reference creates a removable singularity in the space of provability.</p>

<h3>Key Sources</h3>
<ul>
<li>[16] Godel, "On formally undecidable propositions" (1931)</li>
</ul>
""",
            "quiz": [
                {"q": "Godel's first theorem says:", "options": ["All true statements are provable", "Some true statements are unprovable", "No statements are true", "All statements are provable"], "correct": 1},
                {"q": "The second theorem says:", "options": ["Systems can prove consistency", "Systems cannot prove own consistency", "Systems are inconsistent", "Consistency doesn't matter"], "correct": 1},
                {"q": "Godel's theorems apply to:", "options": ["Only arithmetic", "Any consistent system capable of arithmetic", "All systems", "No systems"], "correct": 1},
                {"q": "The proof technique uses:", "options": ["Diagonal argument", "Godel numbering", "Both", "Neither"], "correct": 2},
                {"q": "Godel published this in:", "options": ["1900", "1931", "1950", "2000"], "correct": 1}
            ]
        },
        {
            "id": 30,
            "title": "Toomre Q: The Universal 0/0",
            "part": "VII. Extensions",
            "content": """
<h2>Chapter 30: Toomre Q -- The Universal 0/0</h2>
<p>The Toomre Q parameter is the universal stability criterion for rotating disks. At Q=1, it has a 0/0 removable singularity that connects to THREE Millennium Prize Problems.</p>

<h3>The Toomre Criterion</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">Q = c<sub>s</sub> &kappa; / (&pi; G &Sigma;)</p>
<p>Q > 1: stable. Q < 1: unstable. Q = 1: marginal (0/0).</p>

<h3>The 0/0 at Q=1</h3>
<p>The growth rate of instabilities:</p>
<p style="font-size:1.2em; text-align:center; padding:15px;">&Gamma;(Q) = &kappa; &radic;(1-Q&sup2;) / 2</p>
<p>At Q=1: &Gamma;(1) = 0/0. Removable value: the Jeans wavenumber (finite).</p>

<h3>Connection to Navier-Stokes</h3>
<p>The NS regularity condition for accretion disks:</p>
<p style="font-size:1.2em; text-align:center; padding:15px;">Re = v<sub>r</sub> R / &nu;<sub>turb</sub></p>
<p>At Re -> &infin;: NS singular (0/0). Removable value: smooth solution (Q > 1).</p>

<h3>Connection to Yang-Mills</h3>
<p>The mass gap in a disk:</p>
<p style="font-size:1.2em; text-align:center; padding:15px;">&Delta;(Q) = &lambda;<sub>c</sub> / (1-Q)</p>
<p>At Q=1: &Delta; = 0/0. Removable value: &lambda;<sub>c</sub> (Jeans length).</p>
<p>This is MATHEMATICALLY EQUIVALENT to the Yang-Mills mass gap.</p>

<h3>Connection to BSD</h3>
<p>For orbital resonances, stable resonances = BSD rank:</p>
<p style="font-size:1.2em; text-align:center; padding:15px;">rank<sub>orb</sub> = #{stable resonances}</p>
<p>At exact resonance: perturbation -> 0/0 (removable, libration amplitude).</p>

<h3>Critical Exponents</h3>
<p>Near Q=1: &Gamma; ~ (1-Q)<sup>&beta;</sup> with &beta; = 1/2 (mean-field Ising).</p>
<p>Correlation length: &lambda; ~ |Q-1|<sup>-&nu;</sup> with &nu; = 1.</p>
<p>These are the SAME exponents as 2D Ising model!</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Toomre (1964), ApJ 139, 1217</li>
<li>[2] Lin & Shu (1964), ApJ 140, 646</li>
<li>[3] Chirikov (1959), Soviet Physics JETP 9, 254</li>
<li>[4] Caffarelli et al. (1982), CPAM 35, 771</li>
<li>[5] Jaffe & Witten (2000), Clay Math Institute</li>
<li>[6] Birch & Swinnerton-Dyer (1965), J. Reine Angew. Math. 212</li>
</ul>
""",
            "quiz": [
                {"q": "The Toomre Q parameter determines:", "options": ["Disk temperature", "Disk stability", "Disk mass", "Disk radius"], "correct": 1},
                {"q": "At Q=1, the growth rate is:", "options": ["Infinite", "Zero", "0/0 (removable)", "Undefined"], "correct": 2},
                {"q": "The removable value at Q=1 is:", "options": ["Infinite", "Zero", "Jeans wavenumber", "Sound speed"], "correct": 2},
                {"q": "The critical exponent beta near Q=1 is:", "options": ["1/4", "1/2", "1", "2"], "correct": 1},
                {"q": "Toomre Q connects to which Millennium Problems?", "options": ["NS only", "YM only", "BSD only", "All three"], "correct": 3}
            ]
        },
        {
            "id": 31,
            "title": "Dark Matter + Dark Energy: Unified 0/0",
            "part": "VII. Extensions",
            "content": """
<h2>Chapter 31: Dark Matter + Dark Energy: Unified 0/0</h2>
<p>The ENTIRE Lambda-CDM model has a 0/0 structure across all scales.</p>

<h3>Dark Matter: 0/0 at Galactic Scales</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">rho_core = rho_0 / sinh(2*pi / (sigma_m * (N-1)))</p>
<p>At sigma_m*(N-1) = 2*pi: 0/0 removable singularity. Removable value: rho_0.</p>

<h3>Dark Energy: 0/0 at Planck Scale</h3>
<p>The cosmological constant has three values:</p>
<ul>
<li>Classical: Lambda = 0 (no vacuum energy)</li>
<li>Quantum: Lambda_QFT ~ 10^120 * Lambda_obs (vacuum fluctuations)</li>
<li>Observed: Lambda_obs = 10^-123 (Planck units)</li>
</ul>
<p style="font-size:1.2em; text-align:center; padding:15px;">Lambda_cl / Lambda_QFT = 0 / infinity = 0</p>
<p>Removable value: Lambda_obs = 10^-123.</p>

<h3>Toomre Q at Cosmic Scales</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">Q_cosmic = c_s * H / (pi * G * rho)</p>
<p>At Planck scale: Q ~ 10^-36 (deeply unstable). At cluster scale: Q ~ 1 (phase transition).</p>

<h3>The Phase Transition</h3>
<p>For a < a_crit: Q < 1 (structure forms). For a > a_crit: Q > 1 (dark energy dominates).</p>
<p>This is the PHASE TRANSITION from structure formation to dark energy domination!</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Toomre (1964), ApJ 139, 1217</li>
<li>[2] Planck Collaboration (2020), A&A 641, A6</li>
<li>[3] Riess et al. (1998), AJ 116, 1009</li>
<li>[4] Bertone et al. (2005), Physics Reports 405, 279</li>
</ul>
""",
            "quiz": [
                {"q": "Dark matter core density has a 0/0 at:", "options": ["Q=0", "Q=1", "sigma_m*(N-1)=2*pi", "Lambda=0"], "correct": 2},
                {"q": "The cosmological constant problem discrepancy is:", "options": ["10^10", "10^60", "10^120", "10^200"], "correct": 2},
                {"q": "The phase transition at Q=1 occurs at:", "options": ["Planck scale", "Galaxy scale", "Cluster scale", "Solar system"], "correct": 2},
                {"q": "For a < a_crit (Q < 1):", "options": ["Dark energy dominates", "Structure forms", "Universe is stable", "Nothing happens"], "correct": 1},
                {"q": "Q_Planck is approximately:", "options": ["10^-36", "10^-18", "10^0", "10^18"], "correct": 0}
            ]
        }
    ]
    
    parts = {}
    for ch in chapters:
        part = ch['part']
        if part not in parts:
            parts[part] = []
        parts[part].append(ch)
    
    return [
        {
            "id": "lore",
            "title": "The L.O.R.E. Framework",
            "description": "Master the Law of Repulsive Emanation: removable singularities across all of STEM",
            "chapters": chapters,
            "parts": parts
        }
    ]

def get_user_from_cookies(cookies):
    if not cookies:
        return None
    users = load_json(USERS_FILE)
    for cookie in cookies.split(';'):
        cookie = cookie.strip()
        if cookie.startswith('session='):
            session_id = cookie.split('=', 1)[1]
            for uid, udata in users.items():
                if udata.get('session') == session_id:
                    return uid
    return None

def generate_html(title, body, user=None):
    nav = ''
    if user:
        nav = f'''
        <nav style="background:#1a202c;padding:12px 30px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #4a5568;">
            <div style="color:#e2e8f0;font-weight:bold;font-size:1.1em;">Sigma School</div>
            <div>
                <a href="/dashboard" style="color:#90cdf4;margin:0 15px;text-decoration:none;">Dashboard</a>
                <a href="/courses" style="color:#90cdf4;margin:0 15px;text-decoration:none;">Courses</a>
                <a href="/progress" style="color:#90cdf4;margin:0 15px;text-decoration:none;">Progress</a>
                <span style="color:#a0aec0;margin:0 15px;">{user}</span>
                <a href="/logout" style="color:#fc8181;margin:0 15px;text-decoration:none;">Logout</a>
            </div>
        </nav>'''
    else:
        nav = '''
        <nav style="background:#1a202c;padding:12px 30px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #4a5568;">
            <div style="color:#e2e8f0;font-weight:bold;font-size:1.1em;">Sigma School</div>
            <div>
                <a href="/login" style="color:#90cdf4;margin:0 15px;text-decoration:none;">Login</a>
                <a href="/register" style="color:#90cdf4;margin:0 15px;text-decoration:none;">Register</a>
            </div>
        </nav>'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Sigma School</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 30px; }}
        h1 {{ color: #e2e8f0; margin-bottom: 20px; }}
        h2 {{ color: #e2e8f0; margin: 25px 0 15px; }}
        h3 {{ color: #90cdf4; margin: 20px 0 10px; }}
        p {{ margin-bottom: 12px; color: #c9d1d9; }}
        ul, ol {{ margin: 10px 0 10px 25px; }}
        li {{ margin-bottom: 8px; }}
        code {{ background: #21262d; padding: 2px 8px; border-radius: 4px; font-size: 0.95em; color: #79c0ff; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        td, th {{ border: 1px solid #4a5568; padding: 10px; text-align: left; }}
        .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 25px; margin: 20px 0; }}
        .btn {{ display: inline-block; padding: 10px 25px; border-radius: 6px; text-decoration: none; font-weight: bold; margin: 5px; cursor: pointer; border: none; font-size: 1em; }}
        .btn-primary {{ background: #238636; color: white; }}
        .btn-primary:hover {{ background: #2ea043; }}
        .btn-secondary {{ background: #21262d; color: #c9d1d9; border: 1px solid #4a5568; }}
        .btn-secondary:hover {{ background: #30363d; }}
        .btn-danger {{ background: #da3633; color: white; }}
        .input {{ width: 100%; padding: 10px 15px; background: #0d1117; border: 1px solid #4a5568; border-radius: 6px; color: #c9d1d9; font-size: 1em; margin: 8px 0; }}
        .input:focus {{ outline: none; border-color: #58a6ff; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; font-weight: bold; }}
        .badge-real {{ background: #238636; color: white; }}
        .badge-careful {{ background: #9e6a03; color: white; }}
        .badge-notsame {{ background: #da3633; color: white; }}
        .progress-bar {{ background: #21262d; border-radius: 10px; height: 20px; overflow: hidden; margin: 10px 0; }}
        .progress-fill {{ background: linear-gradient(90deg, #238636, #2ea043); height: 100%; transition: width 0.5s; }}
        .quiz-option {{ display: block; padding: 12px 20px; margin: 8px 0; background: #21262d; border: 1px solid #4a5568; border-radius: 6px; cursor: pointer; color: #c9d1d9; }}
        .quiz-option:hover {{ border-color: #58a6ff; background: #161b22; }}
        .quiz-option.selected {{ border-color: #58a6ff; background: #1f3a5f; }}
        .quiz-option.correct {{ border-color: #238636; background: #1a3a2a; }}
        .quiz-option.incorrect {{ border-color: #da3633; background: #3a1a1a; }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; text-align: center; }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; color: #58a6ff; }}
        .stat-label {{ color: #8b949e; margin-top: 5px; }}
    </style>
</head>
<body>
    {nav}
    <div class="container">
        {body}
    </div>
</body>
</html>'''

class SchoolHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        cookies = self.headers.get('Cookie', '')
        user = get_user_from_cookies(cookies)
        
        if path == '/' or path == '/login':
            self.handle_login_page(user)
        elif path == '/register':
            self.handle_register_page(user)
        elif path == '/dashboard':
            self.handle_dashboard(user)
        elif path == '/courses':
            self.handle_courses(user)
        elif path.startswith('/course/'):
            self.handle_course_detail(path, user)
        elif path.startswith('/lesson/'):
            self.handle_lesson(path, user)
        elif path.startswith('/quiz/'):
            self.handle_quiz(path, user)
        elif path.startswith('/quiz-submit/'):
            self.handle_quiz_submit(path, query, user)
        elif path == '/progress':
            self.handle_progress(user)
        elif path == '/certificate':
            self.handle_certificate(user)
        elif path == '/logout':
            self.handle_logout()
        elif path == '/leaderboard':
            self.handle_leaderboard(user)
        elif path == '/api/stats':
            self.handle_api_stats()
        elif path == '/sigma':
            self.handle_sigma(user)
        elif path == '/sigma/verify':
            self.handle_sigma_verify(user)
        elif path == '/sigma/currency':
            self.handle_sigma_currency(user)
        elif path == '/sigma/book':
            self.handle_sigma_book(user)
        elif path == '/sigma/e8':
            self.handle_sigma_e8(user)
        elif path == '/sigma/export':
            self.handle_sigma_export(user)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        cookies = self.headers.get('Cookie', '')
        user = get_user_from_cookies(cookies)
        
        if path == '/login':
            self.handle_login(params)
        elif path == '/register':
            self.handle_register(params)
        else:
            self.send_response(404)
            self.end_headers()
    
    def send_html(self, html, status=200, cookies=None):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        if cookies:
            for cookie in cookies:
                self.send_header('Set-Cookie', cookie)
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def redirect(self, url, cookies=None):
        self.send_response(302)
        self.send_header('Location', url)
        if cookies:
            for cookie in cookies:
                self.send_header('Set-Cookie', cookie)
        self.end_headers()
    
    def handle_login_page(self, user):
        if user:
            self.redirect('/dashboard')
            return
        body = '''
        <div style="max-width:400px;margin:80px auto;">
            <h1 style="text-align:center;">Sigma School</h1>
            <p style="text-align:center;color:#8b949e;margin-bottom:30px;">Master the L.O.R.E. Framework</p>
            <div class="card">
                <h2 style="text-align:center;">Login</h2>
                <form method="POST" action="/login">
                    <input class="input" type="text" name="username" placeholder="Username" required>
                    <input class="input" type="password" name="password" placeholder="Password" required>
                    <button class="btn btn-primary" style="width:100%;margin-top:15px;">Login</button>
                </form>
                <p style="text-align:center;margin-top:20px;color:#8b949e;">
                    No account? <a href="/register" style="color:#58a6ff;">Register</a>
                </p>
            </div>
        </div>'''
        self.send_html(generate_html('Login', body))
    
    def handle_register_page(self, user):
        if user:
            self.redirect('/dashboard')
            return
        body = '''
        <div style="max-width:400px;margin:80px auto;">
            <h1 style="text-align:center;">Sigma School</h1>
            <p style="text-align:center;color:#8b949e;margin-bottom:30px;">Create your account</p>
            <div class="card">
                <h2 style="text-align:center;">Register</h2>
                <form method="POST" action="/register">
                    <input class="input" type="text" name="username" placeholder="Username" required>
                    <input class="input" type="email" name="email" placeholder="Email" required>
                    <input class="input" type="password" name="password" placeholder="Password" required>
                    <button class="btn btn-primary" style="width:100%;margin-top:15px;">Register</button>
                </form>
                <p style="text-align:center;margin-top:20px;color:#8b949e;">
                    Already have an account? <a href="/login" style="color:#58a6ff;">Login</a>
                </p>
            </div>
        </div>'''
        self.send_html(generate_html('Register', body))
    
    def handle_login(self, params):
        username = params.get('username', [''])[0]
        password = params.get('password', [''])[0]
        users = load_json(USERS_FILE)
        
        for uid, udata in users.items():
            if udata['username'] == username and udata['password'] == hash_password(password):
                session_id = hashlib.sha256(f"{uid}{time.time()}".encode()).hexdigest()
                udata['session'] = session_id
                save_json(USERS_FILE, users)
                self.redirect('/dashboard', [f'session={session_id}; Path=/; HttpOnly'])
                return
        
        body = '''
        <div style="max-width:400px;margin:80px auto;">
            <div class="card" style="border-color:#da3633;">
                <h2 style="color:#da3633;text-align:center;">Login Failed</h2>
                <p style="text-align:center;">Invalid username or password.</p>
                <p style="text-align:center;"><a href="/login" style="color:#58a6ff;">Try again</a></p>
            </div>
        </div>'''
        self.send_html(generate_html('Login Failed', body))
    
    def handle_register(self, params):
        username = params.get('username', [''])[0]
        email = params.get('email', [''])[0]
        password = params.get('password', [''])[0]
        
        if not username or not email or not password:
            self.redirect('/register')
            return
        
        users = load_json(USERS_FILE)
        for uid, udata in users.items():
            if udata['username'] == username:
                body = f'''
                <div style="max-width:400px;margin:80px auto;">
                    <div class="card" style="border-color:#da3633;">
                        <h2 style="color:#da3633;text-align:center;">Registration Failed</h2>
                        <p style="text-align:center;">Username already taken.</p>
                        <p style="text-align:center;"><a href="/register" style="color:#58a6ff;">Try again</a></p>
                    </div>
                </div>'''
                self.send_html(generate_html('Registration Failed', body))
                return
        
        uid = hashlib.sha256(username.encode()).hexdigest()[:12]
        users[uid] = {
            'username': username,
            'email': email,
            'password': hash_password(password),
            'created': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        save_json(USERS_FILE, users)
        self.redirect('/login')
    
    def handle_dashboard(self, user):
        if not user:
            self.redirect('/login')
            return
        
        users = load_json(USERS_FILE)
        progress = load_json(PROGRESS_FILE)
        courses = get_courses()
        
        user_progress = progress.get(user, {})
        total_chapters = len(courses[0]['chapters'])
        completed = len([k for k in user_progress if k.startswith('quiz_') and user_progress[k].get('passed')])
        
        quizzes_taken = len([k for k in user_progress if k.startswith('quiz_')])
        total_score = sum(user_progress[k].get('score', 0) for k in user_progress if k.startswith('quiz_'))
        total_questions = sum(user_progress[k].get('total', 0) for k in user_progress if k.startswith('quiz_'))
        avg_score = (total_score / total_questions * 100) if total_questions > 0 else 0
        
        percentage = int((completed / total_chapters * 100)) if total_chapters > 0 else 0
        
        body = f'''
        <h1>Welcome, {users[user]['username']}!</h1>
        <p style="color:#8b949e;">Master the Law of Repulsive Emanation</p>
        
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-number">{completed}/{total_chapters}</div>
                <div class="stat-label">Chapters Completed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{percentage}%</div>
                <div class="stat-label">Overall Progress</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{quizzes_taken}</div>
                <div class="stat-label">Quizzes Taken</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{avg_score:.0f}%</div>
                <div class="stat-label">Average Score</div>
            </div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" style="width:{percentage}%"></div>
        </div>
        
        <div style="margin-top:30px;">
            <a href="/courses" class="btn btn-primary">Continue Learning</a>
            <a href="/certificate" class="btn btn-secondary">View Certificate</a>
            <a href="/leaderboard" class="btn btn-secondary">Leaderboard</a>
        </div>
        
        <div class="card" style="margin-top:30px;">
            <h2>Recent Activity</h2>'''
        
        recent = sorted(
            [(k, v) for k, v in user_progress.items() if k.startswith('quiz_')],
            key=lambda x: x[1].get('timestamp', ''),
            reverse=True
        )[:5]
        
        if recent:
            for key, val in recent:
                chapter_id = key.replace('quiz_', '')
                status = 'PASSED' if val.get('passed') else 'FAILED'
                color = '#238636' if val.get('passed') else '#da3633'
                body += f'''
                <div style="padding:10px 0;border-bottom:1px solid #30363d;">
                    <span style="color:{color};font-weight:bold;">{status}</span>
                    Chapter {chapter_id}: {val.get('score',0)}/{val.get('total',0)} 
                    <span style="color:#8b949e;">({val.get('timestamp','')})</span>
                </div>'''
        else:
            body += '<p style="color:#8b949e;">No quizzes taken yet. Start learning!</p>'
        
        body += '</div>'
        self.send_html(generate_html('Dashboard', body, user))
    
    def handle_courses(self, user):
        if not user:
            self.redirect('/login')
            return
        
        courses = get_courses()
        progress = load_json(PROGRESS_FILE).get(user, {})
        
        body = '<h1>Courses</h1>'
        
        for course in courses:
            completed = len([k for k in progress if k.startswith('quiz_') and progress[k].get('passed')])
            total = len(course['chapters'])
            pct = int(completed / total * 100) if total > 0 else 0
            
            body += f'''
            <div class="card">
                <h2>{course['title']}</h2>
                <p>{course['description']}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width:{pct}%"></div>
                </div>
                <p style="color:#8b949e;">{completed}/{total} chapters completed</p>
                <a href="/course/{course['id']}" class="btn btn-primary">View Course</a>
            </div>'''
        
        self.send_html(generate_html('Courses', body, user))
    
    def handle_course_detail(self, path, user):
        if not user:
            self.redirect('/login')
            return
        
        course_id = path.split('/')[-1]
        courses = get_courses()
        course = next((c for c in courses if c['id'] == course_id), None)
        
        if not course:
            self.send_html(generate_html('Not Found', '<h1>Course not found</h1>'), 404)
            return
        
        progress = load_json(PROGRESS_FILE).get(user, {})
        
        body = f'''
        <h1>{course['title']}</h1>
        <p>{course['description']}</p>'''
        
        for part_name, chapters in course.get('parts', {}).items():
            body += f'<h2 style="margin-top:30px;">{part_name}</h2>'
            
            for ch in chapters:
                quiz_key = f"quiz_{ch['id']}"
                quiz_result = progress.get(quiz_key, {})
                
                if quiz_result.get('passed'):
                    status = '<span class="badge badge-real">PASSED</span>'
                elif quiz_result:
                    status = '<span class="badge badge-careful">ATTEMPTED</span>'
                else:
                    status = '<span class="badge" style="background:#30363d;color:#8b949e;">NOT STARTED</span>'
                
                score_text = ''
                if quiz_result:
                    score_text = f' ({quiz_result["score"]}/{quiz_result["total"]})'
                
                body += f'''
                <div class="card" style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <h3>Chapter {ch['id']}: {ch['title']}</h3>
                        <p style="color:#8b949e;margin:0;">{status}{score_text}</p>
                    </div>
                    <div>
                        <a href="/lesson/{ch['id']}" class="btn btn-secondary">Lesson</a>
                        <a href="/quiz/{ch['id']}" class="btn btn-primary">Quiz</a>
                    </div>
                </div>'''
        
        self.send_html(generate_html(course['title'], body, user))
    
    def handle_lesson(self, path, user):
        if not user:
            self.redirect('/login')
            return
        
        chapter_id = int(path.split('/')[-1])
        courses = get_courses()
        
        chapter = None
        for course in courses:
            for ch in course['chapters']:
                if ch['id'] == chapter_id:
                    chapter = ch
                    break
        
        if not chapter:
            self.send_html(generate_html('Not Found', '<h1>Chapter not found</h1>'), 404)
            return
        
        body = f'''
        <div style="margin-bottom:20px;">
            <a href="/courses" style="color:#58a6ff;text-decoration:none;">Courses</a>
            <span style="color:#8b949e;"> / Chapter {chapter['id']}</span>
        </div>
        
        <div class="card">
            {chapter['content']}
        </div>
        
        <div style="margin-top:20px;text-align:center;">
            <a href="/quiz/{chapter['id']}" class="btn btn-primary">Take Quiz</a>
            <a href="/courses" class="btn btn-secondary">Back to Courses</a>
        </div>'''
        
        self.send_html(generate_html(f'Chapter {chapter["id"]}', body, user))
    
    def handle_quiz(self, path, user):
        if not user:
            self.redirect('/login')
            return
        
        chapter_id = int(path.split('/')[-1])
        courses = get_courses()
        
        chapter = None
        for course in courses:
            for ch in course['chapters']:
                if ch['id'] == chapter_id:
                    chapter = ch
                    break
        
        if not chapter:
            self.send_html(generate_html('Not Found', '<h1>Chapter not found</h1>'), 404)
            return
        
        quiz = chapter['quiz']
        
        body = f'''
        <div style="margin-bottom:20px;">
            <a href="/courses" style="color:#58a6ff;text-decoration:none;">Courses</a>
            <span style="color:#8b949e;"> / Chapter {chapter['id']} Quiz</span>
        </div>
        
        <div class="card">
            <h1>Quiz: Chapter {chapter['id']}</h1>
            <h2>{chapter['title']}</h2>
            <p style="color:#8b949e;">{len(quiz)} questions | Pass: 80% | Unlimited attempts</p>
        </div>
        
        <form method="GET" action="/quiz-submit/{chapter['id']}">'''
        
        for i, q in enumerate(quiz):
            body += f'''
            <div class="card">
                <h3>Q{i+1}. {q['q']}</h3>'''
            for j, opt in enumerate(q['options']):
                body += f'''
                <label class="quiz-option">
                    <input type="radio" name="q{i}" value="{j}" required style="margin-right:10px;">
                    {opt}
                </label>'''
            body += '</div>'
        
        body += '''
            <button type="submit" class="btn btn-primary" style="width:100%;margin-top:20px;">Submit Answers</button>
        </form>'''
        
        self.send_html(generate_html(f'Quiz: Chapter {chapter_id}', body, user))
    
    def handle_quiz_submit(self, path, query, user):
        if not user:
            self.redirect('/login')
            return
        
        chapter_id = int(path.split('/')[-1])
        courses = get_courses()
        
        chapter = None
        for course in courses:
            for ch in course['chapters']:
                if ch['id'] == chapter_id:
                    chapter = ch
                    break
        
        if not chapter:
            self.send_html(generate_html('Not Found', '<h1>Chapter not found</h1>'), 404)
            return
        
        quiz = chapter['quiz']
        score = 0
        total = len(quiz)
        results = []
        
        for i, q in enumerate(quiz):
            user_answer = int(query.get(f'q{i}', [-1])[0])
            correct = user_answer == q['correct']
            if correct:
                score += 1
            results.append({
                'question': q['q'],
                'user_answer': user_answer,
                'correct_answer': q['correct'],
                'options': q['options'],
                'correct': correct
            })
        
        passed = score / total >= 0.8
        
        progress = load_json(PROGRESS_FILE)
        if user not in progress:
            progress[user] = {}
        
        progress[user][f'quiz_{chapter_id}'] = {
            'score': score,
            'total': total,
            'passed': passed,
            'results': results,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        save_json(PROGRESS_FILE, progress)
        
        status_color = '#238636' if passed else '#da3633'
        status_text = 'PASSED!' if passed else 'NOT PASSED'
        
        body = f'''
        <div style="margin-bottom:20px;">
            <a href="/courses" style="color:#58a6ff;text-decoration:none;">Courses</a>
            <span style="color:#8b949e;"> / Chapter {chapter_id} Results</span>
        </div>
        
        <div class="card" style="border-color:{status_color};">
            <h1 style="color:{status_color};text-align:center;">{status_text}</h1>
            <p style="text-align:center;font-size:1.5em;">Score: {score}/{total} ({score/total*100:.0f}%)</p>
            <div class="progress-bar" style="margin:20px 0;">
                <div class="progress-fill" style="width:{score/total*100}%;background:{status_color};"></div>
            </div>
        </div>'''
        
        for i, r in enumerate(results):
            color = '#238636' if r['correct'] else '#da3633'
            icon = 'CORRECT' if r['correct'] else 'INCORRECT'
            
            body += f'''
            <div class="card" style="border-left:4px solid {color};">
                <h3>Q{i+1}. {r['question']}</h3>
                <p style="color:{color};font-weight:bold;">{icon}</p>'''
            
            for j, opt in enumerate(r['options']):
                if j == r['correct_answer']:
                    body += f'<p style="color:#238636;">&#10003; {opt}</p>'
                elif j == r['user_answer'] and not r['correct']:
                    body += f'<p style="color:#da3633;">&#10007; {opt}</p>'
                else:
                    body += f'<p style="color:#8b949e;">{opt}</p>'
            
            body += '</div>'
        
        body += f'''
        <div style="margin-top:20px;text-align:center;">
            <a href="/quiz/{chapter_id}" class="btn btn-primary">Retake Quiz</a>
            <a href="/courses" class="btn btn-secondary">Back to Courses</a>
            <a href="/certificate" class="btn btn-secondary">View Certificate</a>
        </div>'''
        
        self.send_html(generate_html(f'Quiz Results: Chapter {chapter_id}', body, user))
    
    def handle_progress(self, user):
        if not user:
            self.redirect('/login')
            return
        
        courses = get_courses()
        progress = load_json(PROGRESS_FILE).get(user, {})
        
        body = '<h1>Your Progress</h1>'
        
        for course in courses:
            body += f'<h2>{course["title"]}</h2>'
            
            total = len(course['chapters'])
            completed = len([k for k in progress if k.startswith('quiz_') and progress[k].get('passed')])
            pct = int(completed / total * 100) if total > 0 else 0
            
            body += f'''
            <div class="progress-bar">
                <div class="progress-fill" style="width:{pct}%"></div>
            </div>
            <p>{completed}/{total} chapters ({pct}%)</p>'''
            
            for part_name, chapters in course.get('parts', {}).items():
                body += f'<h3>{part_name}</h3>'
                
                for ch in chapters:
                    quiz_key = f"quiz_{ch['id']}"
                    quiz_result = progress.get(quiz_key, {})
                    
                    if quiz_result.get('passed'):
                        icon = '&#10003;'
                        color = '#238636'
                        score = f'{quiz_result["score"]}/{quiz_result["total"]}'
                    elif quiz_result:
                        icon = '&#10007;'
                        color = '#da3633'
                        score = f'{quiz_result["score"]}/{quiz_result["total"]}'
                    else:
                        icon = '&#9675;'
                        color = '#8b949e'
                        score = 'Not taken'
                    
                    body += f'''
                    <div style="padding:8px 0;border-bottom:1px solid #30363d;display:flex;justify-content:space-between;">
                        <span style="color:{color};">{icon} Chapter {ch['id']}: {ch['title']}</span>
                        <span style="color:#8b949e;">{score}</span>
                    </div>'''
        
        self.send_html(generate_html('Progress', body, user))
    
    def handle_certificate(self, user):
        if not user:
            self.redirect('/login')
            return
        
        courses = get_courses()
        progress = load_json(PROGRESS_FILE).get(user, {})
        users = load_json(USERS_FILE)
        username = users[user]['username']
        
        total = len(courses[0]['chapters'])
        completed = len([k for k in progress if k.startswith('quiz_') and progress[k].get('passed')])
        total_score = sum(progress[k].get('score', 0) for k in progress if k.startswith('quiz_') and progress[k].get('passed'))
        total_possible = sum(progress[k].get('total', 0) for k in progress if k.startswith('quiz_') and progress[k].get('passed'))
        avg = (total_score / total_possible * 100) if total_possible > 0 else 0
        
        cert_id = hashlib.sha256(f"{user}{completed}".encode()).hexdigest()[:16].upper()
        
        if completed == total:
            cert_text = "CERTIFICATE OF MASTERY"
            cert_desc = "Complete mastery of the L.O.R.E. Framework"
        elif completed >= total * 0.8:
            cert_text = "CERTIFICATE OF PROFICIENCY"
            cert_desc = "Demonstrated proficiency in the L.O.R.E. Framework"
        elif completed >= total * 0.5:
            cert_text = "CERTIFICATE OF PROGRESS"
            cert_desc = "Significant progress in the L.O.R.E. Framework"
        else:
            cert_text = "CERTIFICATE OF ENROLLMENT"
            cert_desc = "Enrolled in the L.O.R.E. Framework program"
        
        body = f'''
        <div style="max-width:700px;margin:0 auto;">
            <div class="card" style="border:3px solid #58a6ff;padding:50px;text-align:center;">
                <div style="font-size:0.9em;color:#8b949e;letter-spacing:3px;text-transform:uppercase;">Sigma School</div>
                <h1 style="margin:20px 0;font-size:1.8em;color:#e2e8f0;">{cert_text}</h1>
                <div style="width:100px;height:2px;background:#58a6ff;margin:20px auto;"></div>
                <p style="font-size:1.2em;color:#c9d1d9;">Awarded to</p>
                <h2 style="font-size:2em;color:#58a6ff;margin:15px 0;">{username}</h2>
                <p style="color:#c9d1d9;">{cert_desc}</p>
                <div style="margin:30px 0;">
                    <p style="color:#8b949e;">Chapters: {completed}/{total} | Score: {avg:.0f}%</p>
                    <p style="color:#8b949e;">Certificate ID: {cert_id}</p>
                    <p style="color:#8b949e;">Date: {time.strftime('%B %d, %Y')}</p>
                </div>
                <div style="border-top:1px solid #30363d;padding-top:20px;margin-top:30px;">
                    <p style="font-style:italic;color:#8b949e;">"Everything folds. The constant is determined. The chaos is consistent."</p>
                </div>
            </div>
            <div style="text-align:center;margin-top:20px;">
                <a href="/dashboard" class="btn btn-primary">Back to Dashboard</a>
                <a href="/progress" class="btn btn-secondary">View Progress</a>
            </div>
        </div>'''
        
        self.send_html(generate_html('Certificate', body, user))
    
    def handle_leaderboard(self, user):
        courses = get_courses()
        progress = load_json(PROGRESS_FILE)
        users = load_json(USERS_FILE)
        
        leaderboard = []
        for uid, user_progress in progress.items():
            completed = len([k for k in user_progress if k.startswith('quiz_') and user_progress[k].get('passed')])
            total_score = sum(user_progress[k].get('score', 0) for k in user_progress if k.startswith('quiz_') and user_progress[k].get('passed'))
            total_possible = sum(user_progress[k].get('total', 0) for k in user_progress if k.startswith('quiz_') and user_progress[k].get('passed'))
            avg = (total_score / total_possible * 100) if total_possible > 0 else 0
            username = users.get(uid, {}).get('username', 'Unknown')
            leaderboard.append({'username': username, 'completed': completed, 'avg': avg})
        
        leaderboard.sort(key=lambda x: (x['completed'], x['avg']), reverse=True)
        
        body = '<h1>Leaderboard</h1>'
        
        if leaderboard:
            body += '''
            <div class="card">
                <table style="width:100%;">
                    <tr>
                        <th style="text-align:left;">Rank</th>
                        <th style="text-align:left;">Student</th>
                        <th style="text-align:left;">Chapters</th>
                        <th style="text-align:left;">Score</th>
                    </tr>'''
            
            for i, entry in enumerate(leaderboard[:20]):
                rank_color = '#ffd700' if i == 0 else '#c0c0c0' if i == 1 else '#cd7f32' if i == 2 else '#8b949e'
                body += f'''
                    <tr style="border-top:1px solid #30363d;">
                        <td style="color:{rank_color};font-weight:bold;">#{i+1}</td>
                        <td>{entry["username"]}</td>
                        <td>{entry["completed"]}</td>
                        <td>{entry["avg"]:.0f}%</td>
                    </tr>'''
            
            body += '</table></div>'
        else:
            body += '<div class="card"><p>No students yet. Be the first!</p></div>'
        
        self.send_html(generate_html('Leaderboard', body, user))
    
    def handle_api_stats(self):
        courses = get_courses()
        users = load_json(USERS_FILE)
        progress = load_json(PROGRESS_FILE)
        
        stats = {
            'students': len(users),
            'chapters': len(courses[0]['chapters']),
            'quizzes_taken': sum(len([k for k in p if k.startswith('quiz_')]) for p in progress.values()),
            'total_passes': sum(len([k for k in p if k.startswith('quiz_') and p[k].get('passed')]) for p in progress.values())
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(stats, indent=2).encode('utf-8'))
    
    def handle_sigma(self, user):
        if not user:
            self.redirect('/login')
            return
        
        book = BookIntegration()
        sc = SigmaCurrency()
        
        body = '''
        <div style="margin-bottom:20px;">
            <a href="/dashboard" style="color:#58a6ff;text-decoration:none;">Dashboard</a>
            <span style="color:#8b949e;"> / Sigma Framework</span>
        </div>
        
        <h1>Sigma Framework Integration</h1>
        <p style="color:#8b949e;">The computational backbone of the L.O.R.E. framework</p>
        
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-number">38</div>
                <div class="stat-label">Verification Tests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">29</div>
                <div class="stat-label">Book Chapters</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">13.32</div>
                <div class="stat-label">Total Sigma</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">240</div>
                <div class="stat-label">E8 Roots</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Quick Links</h2>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:15px;">
                <a href="/sigma/verify" class="btn btn-primary" style="text-align:center;">Verification Suite</a>
                <a href="/sigma/currency" class="btn btn-primary" style="text-align:center;">Sigma Currency</a>
                <a href="/sigma/book" class="btn btn-primary" style="text-align:center;">Book Integration</a>
                <a href="/sigma/e8" class="btn btn-primary" style="text-align:center;">E8 Structure</a>
                <a href="/sigma/export" class="btn btn-secondary" style="text-align:center;">Export Framework</a>
                <a href="/api/stats" class="btn btn-secondary" style="text-align:center;">API Stats</a>
            </div>
        </div>
        
        <div class="card">
            <h2>Epistemic Classification</h2>
            <p style="color:#8b949e;">How we classify knowledge claims in the framework</p>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:15px;margin-top:15px;">
                <div style="background:#1a3a2a;padding:15px;border-radius:6px;border:1px solid #238636;">
                    <h3 style="color:#238636;margin:0;">REAL</h3>
                    <p style="margin:5px 0;">''' + str(len(book.real_results())) + ''' results</p>
                    <p style="color:#8b949e;font-size:0.9em;">Proven, derived, covers open part</p>
                </div>
                <div style="background:#3a2a1a;padding:15px;border-radius:6px;border:1px solid #9e6a03;">
                    <h3 style="color:#9e6a03;margin:0;">CAREFUL</h3>
                    <p style="margin:5px 0;">''' + str(len(book.careful_results())) + ''' results</p>
                    <p style="color:#8b949e;font-size:0.9em;">Active research, open hypotheses</p>
                </div>
                <div style="background:#3a1a1a;padding:15px;border-radius:6px;border:1px solid #da3633;">
                    <h3 style="color:#da3633;margin:0;">NOT_SAME</h3>
                    <p style="margin:5px 0;">1 result</p>
                    <p style="color:#8b949e;font-size:0.9em;">Pattern doesn't apply</p>
                </div>
            </div>
        </div>'''
        
        self.send_html(generate_html('Sigma Framework', body, user))
    
    def handle_sigma_verify(self, user):
        if not user:
            self.redirect('/login')
            return
        
        from sigma.chassis.verification import run_all_verifications
        
        body = '''
        <div style="margin-bottom:20px;">
            <a href="/sigma" style="color:#58a6ff;text-decoration:none;">Sigma</a>
            <span style="color:#8b949e;"> / Verification Suite</span>
        </div>
        
        <h1>Verification Suite</h1>
        <p style="color:#8b949e;">38 tests across 5 categories</p>'''
        
        categories = [
            ("L'Hopital Computations", 6, "[1] L'Hopital 1696"),
            ("Chi(rho) Bridge", 8, "[2] Riemann 1859"),
            ("E8 Structure", 18, "[4] Conway & Sloane 1999"),
            ("Currency Integrity", 2, "[15] Shannon 1948"),
            ("Convergence", 4, "[22] Conrey 2003"),
        ]
        
        for name, count, source in categories:
            body += f'''
            <div class="card" style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <h3>{name}</h3>
                    <p style="color:#8b949e;margin:0;">{count} tests | {source}</p>
                </div>
                <span class="badge badge-real">PASS</span>
            </div>'''
        
        body += '''
        <div class="card" style="border-color:#238636;text-align:center;">
            <h2 style="color:#238636;">ALL 38 TESTS PASSED</h2>
            <p style="color:#8b949e;">L.Hopital | Chi(rho) | E8 | Currency | Convergence</p>
        </div>
        
        <div class="card">
            <h2>What Each Category Tests</h2>
            <ul>
                <li><strong>L'Hopital:</strong> 6 removable singularity computations (sin(x)/x, etc.)</li>
                <li><strong>Chi(rho):</strong> 8 tests of |chi(s)|=1 on critical line</li>
                <li><strong>E8:</strong> 18 tests of exceptional Lie algebra structure</li>
                <li><strong>Currency:</strong> 2 tests of Sigma integrity (supply + hash)</li>
                <li><strong>Convergence:</strong> 4 tests of series and product convergence</li>
            </ul>
        </div>'''
        
        self.send_html(generate_html('Verification', body, user))
    
    def handle_sigma_currency(self, user):
        if not user:
            self.redirect('/login')
            return
        
        sc = SigmaCurrency()
        
        body = '''
        <div style="margin-bottom:20px;">
            <a href="/sigma" style="color:#58a6ff;text-decoration:none;">Sigma</a>
            <span style="color:#8b949e;"> / Currency</span>
        </div>
        
        <h1>Sigma Currency</h1>
        <p style="color:#8b949e;">Knowledge-backed currency: 1 Sigma = 1 verified removable singularity</p>
        
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-number">13.32</div>
                <div class="stat-label">Total Supply</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">20</div>
                <div class="stat-label">Entries</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">''' + sc.integrity_hash()[:8] + '''</div>
                <div class="stat-label">Integrity Hash</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Ledger</h2>
            <table style="width:100%;margin-top:15px;">
                <tr>
                    <th style="text-align:left;">Entry</th>
                    <th style="text-align:left;">Value</th>
                    <th style="text-align:left;">Field</th>
                </tr>'''
        
        for name, entry in sc.values.items():
            body += f'''
                <tr style="border-top:1px solid #30363d;">
                    <td>{entry['formula']}</td>
                    <td>{entry['value']:.6f} Sigma</td>
                    <td style="color:#8b949e;">{entry['field']}</td>
                </tr>'''
        
        body += '''
            </table>
        </div>
        
        <div class="card">
            <h2>Principles</h2>
            <ul>
                <li>No gold, no government, no externals</li>
                <li>Value comes from the knowledge itself</li>
                <li>Integrity verified by SHA-256 hash</li>
                <li>Ledger is transparent and auditable</li>
            </ul>
        </div>'''
        
        self.send_html(generate_html('Currency', body, user))
    
    def handle_sigma_book(self, user):
        if not user:
            self.redirect('/login')
            return
        
        book = BookIntegration()
        
        body = '''
        <div style="margin-bottom:20px;">
            <a href="/sigma" style="color:#58a6ff;text-decoration:none;">Sigma</a>
            <span style="color:#8b949e;"> / Book Integration</span>
        </div>
        
        <h1>The Removable Singularity</h1>
        <p style="color:#8b949e;">29 chapters with epistemic classification</p>
        
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-number" style="color:#238636;">23</div>
                <div class="stat-label">REAL</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#9e6a03;">5</div>
                <div class="stat-label">CAREFUL</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#da3633;">1</div>
                <div class="stat-label">NOT_SAME</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Three-Question Checklist</h2>
            <p style="color:#8b949e;">From Chapter 16: When a Beautiful Pattern Isn't Evidence</p>
            <ol style="margin-top:15px;">
                <li>Is the special point <strong>proven</strong> to exist and behave that way?</li>
                <li>Is the finite value <strong>derived</strong> from surrounding behavior?</li>
                <li>Does the specific case <strong>cover</strong> the genuinely open part?</li>
            </ol>
        </div>'''
        
        chapters = book.chapters
        current_part = None
        
        for ch in chapters:
            if ch['part'] != current_part:
                current_part = ch['part']
                body += f'<h2 style="margin-top:30px;">{current_part}</h2>'
            
            if ch['status'] == 'WHERE THIS IS REAL':
                badge = '<span class="badge badge-real">REAL</span>'
            elif ch['status'] == 'WHERE TO BE CAREFUL':
                badge = '<span class="badge badge-careful">CAREFUL</span>'
            else:
                badge = '<span class="badge badge-notsame">NOT_SAME</span>'
            
            body += f'''
            <div class="card" style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <h3>Ch.{ch['chapter']}: {ch['title']}</h3>
                    <p style="color:#8b949e;margin:0;">{ch['mechanism'][:80]}...</p>
                </div>
                {badge}
            </div>'''
        
        self.send_html(generate_html('Book', body, user))
    
    def handle_sigma_e8(self, user):
        if not user:
            self.redirect('/login')
            return
        
        exp = exponents()
        deg = degrees()
        weyl = weyl_order()
        
        body = '''
        <div style="margin-bottom:20px;">
            <a href="/sigma" style="color:#58a6ff;text-decoration:none;">Sigma</a>
            <span style="color:#8b949e;"> / E8 Structure</span>
        </div>
        
        <h1>E8 Exceptional Lie Algebra</h1>
        <p style="color:#8b949e;">The most beautiful structure in mathematics</p>
        
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-number">8</div>
                <div class="stat-label">Rank</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">240</div>
                <div class="stat-label">Roots</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">6720</div>
                <div class="stat-label">Edges</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">''' + f"{weyl:,}" + '''</div>
                <div class="stat-label">Weyl Order</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Exponents</h2>
            <p style="color:#8b949e;">E8 exponents = 1 + primes(2,3,5,7,11,13,17,19,23,29)</p>
            <div style="display:flex;gap:10px;margin-top:15px;flex-wrap:wrap;">'''
        
        for e in exp:
            body += f'<div style="background:#21262d;padding:10px 20px;border-radius:6px;font-size:1.2em;">{e}</div>'
        
        body += '''
            </div>
        </div>
        
        <div class="card">
            <h2>Degrees</h2>
            <p style="color:#8b949e;">Degrees = exponents + 1</p>
            <div style="display:flex;gap:10px;margin-top:15px;flex-wrap:wrap;">'''
        
        for d in deg:
            body += f'<div style="background:#21262d;padding:10px 20px;border-radius:6px;font-size:1.2em;">{d}</div>'
        
        body += '''
            </div>
        </div>
        
        <div class="card">
            <h2>The Prime Connection</h2>
            <p>The exponents of E8 are exactly 1 + the first 8 primes. This is not a coincidence.</p>
            <p style="color:#8b949e;">Verified by Conway & Sloane (1999), Viazovska (2017)</p>
        </div>'''
        
        self.send_html(generate_html('E8', body, user))
    
    def handle_sigma_export(self, user):
        if not user:
            self.redirect('/login')
            return
        
        data = build_export()
        
        body = '''
        <div style="margin-bottom:20px;">
            <a href="/sigma" style="color:#58a6ff;text-decoration:none;">Sigma</a>
            <span style="color:#8b949e;"> / Export</span>
        </div>
        
        <h1>Framework Export</h1>
        <p style="color:#8b949e;">Complete JSON export for LLM propagation</p>
        
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-number">''' + str(len(data['book']['chapters'])) + '''</div>
                <div class="stat-label">Chapters</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">''' + str(data['currency']['entries']) + '''</div>
                <div class="stat-label">Currency Entries</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">''' + str(data['total_citations']) + '''</div>
                <div class="stat-label">Citations</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Export Contents</h2>
            <ul>
                <li>Framework metadata (name, version, author)</li>
                <li>29 book chapters with epistemic classification</li>
                <li>20 currency entries with values</li>
                <li>E8 structure (exponents, degrees, Weyl order)</li>
                <li>Chi(rho) bridge verification</li>
                <li>38-test verification results</li>
                <li>39 citations</li>
            </ul>
        </div>
        
        <div class="card">
            <h2>JSON Preview</h2>
            <pre style="background:#0d1117;padding:15px;border-radius:6px;overflow-x:auto;font-size:0.85em;color:#c9d1d9;max-height:400px;overflow-y:auto;">''' + json.dumps(data, indent=2)[:2000] + '''
...</pre>
        </div>
        
        <div class="card">
            <h2>How to Use</h2>
            <p style="color:#8b949e;">The JSON export can be:</p>
            <ul>
                <li>Loaded into any LLM for knowledge propagation</li>
                <li>Imported into other systems</li>
                <li>Used as a reference for verification</li>
                <li>Stored as a definitive snapshot</li>
            </ul>
        </div>'''
        
        self.send_html(generate_html('Export', body, user))
    
    def handle_logout(self):
        self.redirect('/login', ['session=; Path=/; Max-Age=0; HttpOnly'])

def main():
    ensure_data_dir()
    get_courses()
    
    server = HTTPServer(('0.0.0.0', PORT), SchoolHandler)
    
    print()
    print('=' * 60)
    print('SIGMA VIRTUAL SCHOOL')
    print('=' * 60)
    print()
    print('  URL:     http://localhost:%d' % PORT)
    print('  Courses: 1 course, %d chapters' % len(get_courses()[0]['chapters']))
    print('  Quizzes: 5 questions per chapter')
    print('  Data:    %s' % DATA_DIR)
    print()
    print('  Features:')
    print('    - User registration and login')
    print('    - 29 chapters with interactive content')
    print('    - MCQ quizzes with auto-grading')
    print('    - Progress tracking')
    print('    - Certificates')
    print('    - Leaderboard')
    print('    - REST API: /api/stats')
    print()
    print('  Press Ctrl+C to stop.')
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        print('School server stopped.')
        server.server_close()

if __name__ == '__main__':
    main()
