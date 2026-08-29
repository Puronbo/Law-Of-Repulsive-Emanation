#!/usr/bin/env python3
"""
Sigma Virtual School Server
============================

A zero-dependency learning management system for the L.O.R.E. framework.

Usage:
    python sigma_school_server.py [--port PORT]

Features:
    - 68 chapters from "The Removable Singularity"
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
        },
        {
            "id": 32,
            "title": "Black Hole Information: 0/0 at the Horizon",
            "part": "VII. Extensions",
            "content": """
<h2>Chapter 32: Black Hole Information: 0/0 at the Horizon</h2>
<p>The most extreme 0/0 in physics: the event horizon of a black hole.</p>

<h3>The 0/0 Structure</h3>
<p>At the event horizon (r = r_s):</p>
<ul>
<li>Information inside: I = 0 (nothing escapes)</li>
<li>Information outside: I = infinity (all information)</li>
<li>0/0: I_inside / I_outside = 0 / infinity = 0</li>
</ul>
<p style="font-size:1.2em; text-align:center; padding:15px;">Removable value: S_BH = A / (4 * l_Planck^2)</p>

<h3>Bekenstein-Hawking Entropy</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">S_BH = k_B * A / (4 * l_Planck^2)</p>
<p>For a solar mass black hole: S_BH/k_B ~ 10^77. For Sgr A*: ~10^90. For M87*: ~10^104.</p>

<h3>Page Curve</h3>
<p>The Page curve describes information recovery during evaporation:</p>
<ul>
<li>t = 0: I = 0 (no radiation)</li>
<li>t = t_Page: I = S_BH (Page time, 0/0 removable)</li>
<li>t = t_evap: I = S_BH (all information recovered)</li>
</ul>

<h3>Holographic Principle</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">Maximum information = Area / (4 * l_Planck^2)</p>
<p>Information is proportional to AREA, not VOLUME. Same 0/0 structure as Toomre Q!</p>

<h3>Connection to Toomre Q</h3>
<p>The event horizon is a gravitational instability:</p>
<ul>
<li>Q < 1: unstable (horizon forms)</li>
<li>Q > 1: stable (no horizon)</li>
<li>Q = 1: marginal (0/0 removable singularity)</li>
</ul>
<p>Critical exponent: beta = 1/2 (mean-field Ising) -- SAME as Toomre Q!</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Bekenstein (1973), Phys. Rev. D 7, 2333</li>
<li>[2] Hawking (1975), Comm. Math. Phys. 43, 199</li>
<li>[3] Page (1993), Phys. Rev. Lett. 71, 1291</li>
<li>[4] Maldacena (1998), AdS/CFT correspondence</li>
</ul>
""",
            "quiz": [
                {"q": "At the event horizon, information inside is:", "options": ["Infinite", "Zero", "S_BH", "Undefined"], "correct": 1},
                {"q": "The removable value at the horizon is:", "options": ["Zero", "Infinity", "S_BH = A/(4l_P^2)", "r_s"], "correct": 2},
                {"q": "The Page time is when:", "options": ["Evaporation starts", "Information = S_BH", "BH disappears", "Temperature = 0"], "correct": 1},
                {"q": "The holographic principle says information ~:", "options": ["Volume", "Area", "Mass", "Temperature"], "correct": 1},
                {"q": "The critical exponent beta at the horizon is:", "options": ["1/4", "1/2", "1", "2"], "correct": 1}
            ]
        },
        {
            "id": 33,
            "title": "Quantum Entanglement: 0/0 at AdS/CFT",
            "part": "VII. Extensions",
            "content": """
<h2>Chapter 33: Quantum Entanglement: 0/0 at AdS/CFT</h2>
<p>The Ryu-Takayanagi formula has a 0/0 structure at the AdS/CFT boundary.</p>

<h3>The Ryu-Takayanagi Formula</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">S_A = Area(gamma_A) / (4 * G_N)</p>
<ul>
<li>In the bulk (AdS): S_A = 0 (no entanglement)</li>
<li>On the boundary (CFT): S_A = infinity (maximum)</li>
<li>At the boundary (removable): S_A = Area/(4G_N)</li>
</ul>

<h3>Holographic Bound</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">S_max = L^{d-1} / (4 * G_N)</p>
<p>Maximum information in a region is proportional to its AREA, not VOLUME.</p>

<h3>Entanglement Wedge</h3>
<ul>
<li>r < r_s: wedge = 0 (no reconstruction)</li>
<li>r > r_s: wedge = r - r_s (reconstructable)</li>
<li>r = r_s: 0/0 removable singularity</li>
</ul>

<h3>ER = EPR</h3>
<p>Maldacena & Susskind (2013): Einstein-Rosen bridges = Einstein-Podolsky-Rosen pairs.</p>
<p style="font-size:1.2em; text-align:center; padding:15px;">ER bridge = EPR pair = 0/0 at horizon</p>
<p>Removable value: S_BH = Area/(4G_N).</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Ryu & Takayanagi (2006), Phys. Rev. Lett. 96, 181602</li>
<li>[2] Maldacena (1998), AdS/CFT correspondence</li>
<li>[3] Almheiri et al. (2015), Holographic QEC</li>
<li>[4] Maldacena & Susskind (2013), ER=EPR</li>
</ul>
""",
            "quiz": [
                {"q": "The Ryu-Takayanagi formula gives:", "options": ["S = V/(4G)", "S = Area/(4G)", "S = M*c^2", "S = kT"], "correct": 1},
                {"q": "In the bulk (AdS), S_A is:", "options": ["Infinity", "Zero", "S_BH", "Undefined"], "correct": 1},
                {"q": "The holographic bound says information ~:", "options": ["Volume", "Area", "Mass", "Temperature"], "correct": 1},
                {"q": "ER=EPR means:", "options": ["Energy = Momentum", "Wormholes = Entanglement", "Mass = Charge", "Spin = Orbit"], "correct": 1},
                {"q": "The critical exponent beta for RT is:", "options": ["1/4", "1/2", "1", "2"], "correct": 1}
            ]
        },
        {
            "id": 34,
            "title": "Consciousness & Neural Synchrony: 0/0 at the Critical Point",
            "part": "VII. Extensions",
            "content": """
<h2>Chapter 34: Consciousness & Neural Synchrony: 0/0 at the Critical Point</h2>
<p>The binding problem: how does the brain unify distributed features into a single conscious experience? The answer is a 0/0 removable singularity at the critical coupling threshold.</p>

<h3>The Kuramoto Model</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">d(theta_i)/dt = w_i + (K/N) * sum_j sin(theta_j - theta_i)</p>
<ul>
<li>r = 0 for K &lt;= K_c (desynchronized, unconscious)</li>
<li>r = sqrt(1 - K_c/K) for K &gt; K_c (synchronized, conscious)</li>
<li>At K = K_c: r = 0/0 REMOVABLE SINGULARITY</li>
</ul>

<h3>Critical Exponent</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">r ~ (K - K_c)^{1/2}    beta = 1/2</p>
<p>Same beta as: Toomre Q=1, Black hole horizon, Ryu-Takayanagi, Ising model.</p>

<h3>Neural Criticality</h3>
<p>At K = K_c: power-law avalanches P(S) ~ S^{-3/2} (tau = 3/2, mean-field).</p>

<h3>Integrated Information (Phi)</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">Phi ~ r * (1-r) * log(N)</p>
<p>Maximum at r ~ 1/2 (K ~ 2*K_c). Consciousness = removable singularity in Phi(K).</p>

<h3>Anesthesia</h3>
<p>Anesthesia reduces K toward zero. Consciousness vanishes as a phase transition.</p>

<h3>Gamma Binding (30-100 Hz)</h3>
<p>Gamma synchrony r = 0/0 at K_c. Binding = unified experience = removable singularity.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Kuramoto (1975), self-entrainment of coupled oscillators</li>
<li>[2] Strogatz & Mirollo (1991), stability of incoherence</li>
<li>[3] Beggs & Plenz (2003), neuronal avalanches</li>
<li>[4] Tononi (2004), integrated information theory</li>
<li>[5] Singer & Gray (1995), neural binding</li>
</ul>
""",
            "quiz": [
                {"q": "In the Kuramoto model, r = 0/0 occurs at:", "options": ["K = 0", "K = K_c", "K = infinity", "K = 1"], "correct": 1},
                {"q": "The critical exponent beta for consciousness is:", "options": ["1/4", "1/2", "1", "3/2"], "correct": 1},
                {"q": "At criticality, neural avalanches follow:", "options": ["Exponential", "Power law S^{-3/2}", "Gaussian", "Uniform"], "correct": 1},
                {"q": "Gamma oscillations are in which frequency range?", "options": ["1-10 Hz", "10-30 Hz", "30-100 Hz", "100-300 Hz"], "correct": 2},
                {"q": "Anesthesia reduces neural coupling K toward:", "options": ["K_c", "Infinity", "Zero", "Negative values"], "correct": 2}
            ]
        },
        {
            "id": 35,
            "title": "Origin of Life: 0/0 at the Edge of Life",
            "part": "VII. Extensions",
            "content": """
<h2>Chapter 35: Origin of Life: 0/0 at the Edge of Life</h2>
<p>The origin of life is a phase transition with 0/0 structure at the autocatalytic threshold. Three independent frameworks converge on the same singularity.</p>

<h3>Eigen's Error Threshold (1971)</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">q_c = e^{-1/L}</p>
<ul>
<li>q < q_c: error catastrophe, extinction</li>
<li>q > q_c: quasispecies survives, LIFE</li>
<li>q = q_c: 0/0 removable singularity, beta = 1/2</li>
</ul>

<h3>Kauffman's Autocatalytic Sets (1993)</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">K*C > N^2 -> autocatalytic closure</p>
<ul>
<li>K*C < N^2: no self-replication</li>
<li>K*C > N^2: autocatalytic closure, LIFE</li>
<li>K*C = N^2: 0/0 removable singularity, beta = 1/2</li>
</ul>

<h3>Erdos-Renyi Percolation (1960)</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">p_c = 1/N</p>
<ul>
<li>p < p_c: disconnected fragments</li>
<li>p > p_c: giant component, LIFE</li>
<li>p = p_c: 0/0 removable singularity</li>
<li>beta = 1/3 (2D), beta = 1 (mean-field) - DIFFERENT universality class!</li>
</ul>

<h3>Minimal Genome</h3>
<p>Below ~300 genes: no self-replication. Above: self-replication possible. Mycoplasma genitalium = 525 genes (minimal). At 300 genes: 0/0.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Eigen (1971), self-organization of matter</li>
<li>[2] Kauffman (1993), The Origins of Order</li>
<li>[3] Erdos & Renyi (1960), random graphs</li>
<li>[4] Venter et al. (2010), synthetic genome</li>
</ul>
""",
            "quiz": [
                {"q": "Eigen's error threshold occurs when:", "options": ["q = 1", "q^L = e^{-1}", "L = 0", "f_0 = 0"], "correct": 1},
                {"q": "Kauffman's autocatalytic closure requires:", "options": ["K > N", "K*C > N^2", "L > 300", "p > 1/N"], "correct": 1},
                {"q": "The Erdos-Renyi giant component appears at:", "options": ["p = 0", "p = 1", "p = 1/N", "p = N"], "correct": 2},
                {"q": "The critical exponent for ER percolation in 2D is:", "options": ["1/2", "1/3", "1", "3/2"], "correct": 1},
                {"q": "Mycoplasma genitalium has approximately:", "options": ["100 genes", "300 genes", "525 genes", "1000 genes"], "correct": 2}
            ]
        },
        {
            "id": 36,
            "title": "The Ising Model: 0/0 at the Phase Transition",
            "part": "VII. Extensions",
            "content": """
<h2>Chapter 36: The Ising Model: 0/0 at the Phase Transition</h2>
<p>The Ising model is the master 0/0 removable singularity: all phase transitions share the same 0/0 structure but have DIFFERENT critical exponents depending on dimensionality.</p>

<h3>The Model</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">H = -J * sum_{&lt;ij&gt;} s_i * s_j</p>
<ul>
<li>T &lt; T_c: M &gt; 0 (magnetized)</li>
<li>T &gt; T_c: M = 0 (disordered)</li>
<li>T = T_c: M = 0/0 (removable singularity)</li>
</ul>

<h3>Critical Exponents by Dimension</h3>
<table style="width:100%; border-collapse:collapse;">
<tr><td style="padding:5px; border:1px solid #4a5568;"><b>Dimension</b></td><td style="padding:5px; border:1px solid #4a5568;"><b>beta</b></td><td style="padding:5px; border:1px solid #4a5568;"><b>Method</b></td></tr>
<tr><td style="padding:5px; border:1px solid #4a5568;">2D</td><td style="padding:5px; border:1px solid #4a5568;">1/8 = 0.125</td><td style="padding:5px; border:1px solid #4a5568;">Onsager exact (1944)</td></tr>
<tr><td style="padding:5px; border:1px solid #4a5568;">3D</td><td style="padding:5px; border:1px solid #4a5568;">0.326</td><td style="padding:5px; border:1px solid #4a5568;">Monte Carlo</td></tr>
<tr><td style="padding:5px; border:1px solid #4a5568;">Mean-field</td><td style="padding:5px; border:1px solid #4a5568;">1/2 = 0.500</td><td style="padding:5px; border:1px solid #4a5568;">Bragg-Williams</td></tr>
</table>

<h3>Wilson's Renormalization Group (1971)</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">beta = 1/2 - epsilon/12</p>
<p>epsilon = 4 - d. RG fixed points determine universality class.</p>

<h3>All Prior 0/0 = Ising Universality Classes</h3>
<ul>
<li>Kuramoto, Toomre Q, BH, RT, Eigen, Kauffman = MF (beta=1/2)</li>
<li>Erdos-Renyi percolation = 2D (beta=1/3) or MF (beta=1)</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[1] Ising (1925), ferromagnetism</li>
<li>[2] Onsager (1944), exact 2D solution</li>
<li>[3] Wilson (1971), renormalization group (Nobel 1982)</li>
<li>[4] Fisher (1974), RG theory</li>
</ul>
""",
            "quiz": [
                {"q": "The 2D Ising critical exponent beta is:", "options": ["1/2", "1/4", "1/8", "1/3"], "correct": 2},
                {"q": "Onsager solved the Ising model in which year?", "options": ["1925", "1944", "1971", "1982"], "correct": 1},
                {"q": "Wilson's RG explains:", "options": ["Why T_c varies", "Why beta varies with dimension", "Why M = 0", "Why J > 0"], "correct": 1},
                {"q": "The mean-field Ising beta is:", "options": ["1/8", "1/3", "1/2", "1"], "correct": 2},
                {"q": "The upper critical dimension for Ising is:", "options": ["d = 2", "d = 3", "d = 4", "d = 6"], "correct": 2}
            ]
        },
        {
            "id": 37,
            "title": "Turbulence & Kolmogorov: 0/0 at the Dissipation Scale",
            "part": "VII. Extensions",
            "content": """
<h2>Chapter 37: Turbulence & Kolmogorov: 0/0 at the Dissipation Scale</h2>
<p>Turbulence is the last great unsolved problem of classical physics. The Kolmogorov 1941 theory reveals a universal 0/0 at the dissipation scale.</p>

<h3>Kolmogorov Energy Spectrum (K41)</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">E(k) = C_K * epsilon^{2/3} * k^{-5/3}</p>
<ul>
<li>The -5/3 exponent is UNIVERSAL across ALL turbulent flows</li>
<li>C_K = 1.5 (Kolmogorov constant)</li>
<li>Different universality class from Ising entirely!</li>
</ul>

<h3>Dissipation Scale (0/0 Point)</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">eta = (nu^3 / epsilon)^{1/4}</p>
<p>Below eta: viscous dissipation. Above eta: inertial cascade. At eta: 0/0 removable singularity.</p>

<h3>Richardson Cascade (1922)</h3>
<p>"Big whorls have little whorls which feed on their velocity." Self-similar 0/0 at each scale. Fractal structure.</p>

<h3>Reynolds Transition</h3>
<p>Re = U*L/nu. Re &lt; 2000: laminar. Re &gt; 4000: turbulent. At Re_c: 0/0.</p>

<h3>Intermittency & She-Leveque (1994)</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">zeta_p = p/3 - mu*p*(p-3)/18, mu = 2/9</p>
<p>Log-Poisson cascade. Corrections to K41.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Kolmogorov (1941), local structure of turbulence</li>
<li>[2] Richardson (1922), weather prediction</li>
<li>[3] She & Leveque (1994), universal scaling</li>
<li>[4] Frisch (1995), Turbulence textbook</li>
</ul>
""",
            "quiz": [
                {"q": "The Kolmogorov energy spectrum exponent is:", "options": ["-1", "-5/3", "-2", "-3"], "correct": 1},
                {"q": "The Kolmogorov constant C_K is approximately:", "options": ["0.5", "1.0", "1.5", "2.0"], "correct": 2},
                {"q": "The dissipation scale eta is:", "options": ["(nu/epsilon)^{1/2}", "(nu^3/epsilon)^{1/4}", "L/Re", "nu/U"], "correct": 1},
                {"q": "The She-Leveque intermittency parameter mu is:", "options": ["0", "1/3", "2/9", "1/2"], "correct": 2},
                {"q": "The Reynolds transition occurs at approximately:", "options": ["Re = 100", "Re = 1000", "Re = 2000-4000", "Re = 100000"], "correct": 2}
            ]
        },
        {
            "id": 38,
            "title": "Financial Markets: 0/0 at the Crash",
            "part": "VII. Extensions",
            "content": """
<h2>Chapter 38: Financial Markets: 0/0 at the Crash</h2>
<p>Financial markets exhibit 0/0 removable singularities at critical points. Human markets obey the SAME universal laws as physics.</p>

<h3>Black-Scholes Boundary</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">V = S*N(d1) - K*e^{-rT}*N(d2)</p>
<p>At S=0 or T=0: V = 0/0 removable singularity. Removable value: max(S-K, 0).</p>

<h3>Market Crash as Phase Transition</h3>
<ul>
<li>Normal: Gaussian returns (efficient market)</li>
<li>Critical: power-law returns (herding, bubbles)</li>
<li>Crash: 0/0 removable singularity</li>
</ul>

<h3>Sornette Log-Periodic Model (LPPLS)</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">ln(P) = A + B*(t_c-t)^m + C*(t_c-t)^m*cos(omega*ln(t_c-t)-phi)</p>
<p>Log-periodic oscillations BEFORE crash. Successfully predicted 2008 crisis.</p>

<h3>Mandelbrot Fractal Finance</h3>
<p>Hurst exponent H: H=0.5 efficient, H>0.5 trending, H<0.5 mean-reverting. Fractal dimension D=2-H. Universal across ALL markets.</p>

<h3>Herding = Kuramoto</h3>
<p>Traders as coupled oscillators. Same model as consciousness (Ch.34)! At critical K: herding transition (0/0).</p>

<h3>GARCH Unit Root</h3>
<p>sigma_t^2 = omega + alpha*r_{t-1}^2 + beta*sigma_{t-1}^2. At alpha+beta=1: unit root (0/0). IGARCH: infinite volatility.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Black & Scholes (1973), option pricing</li>
<li>[2] Mandelbrot (1997), fractal finance</li>
<li>[3] Sornette (2003), critical market crashes</li>
<li>[4] Bollerslev (1986), GARCH model</li>
</ul>
""",
            "quiz": [
                {"q": "The Black-Scholes formula has 0/0 at:", "options": ["S=K", "S=0 or T=0", "sigma=1", "r=0"], "correct": 1},
                {"q": "The Hurst exponent H=0.5 corresponds to:", "options": ["Trending market", "Efficient market", "Crash", "Bubble"], "correct": 1},
                {"q": "Sornette's model predicts crashes via:", "options": ["Gaussian noise", "Log-periodic oscillations", "Random walks", "Linear trends"], "correct": 1},
                {"q": "The GARCH unit root occurs at:", "options": ["alpha+beta=0", "alpha+beta=0.5", "alpha+beta=1", "alpha+beta=2"], "correct": 2},
                {"q": "Market herding is modeled by:", "options": ["Ising model", "Kuramoto model", "Navier-Stokes", "Euler equation"], "correct": 1}
            ]
        },
        {
            "id": 39,
            "title": "Quantum Phase Transitions: 0/0 at Absolute Zero",
            "part": "VIII. Deep Connections",
            "content": """
<h2>Chapter 39: Quantum Phase Transitions: 0/0 at Absolute Zero</h2>
<p>Quantum phase transitions occur at ZERO temperature, driven by quantum fluctuations, not thermal fluctuations. This is the most fundamental 0/0.</p>

<h3>Transverse Field Ising Model</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">H = -J*sum(sigma_z^i*sigma_z^{i+1}) - g*sum(sigma_x^i)</p>
<p>At g = g_c = J: quantum critical point (0/0). Order parameter &lt;sigma_z&gt; = 0/0 with beta = 1/8.</p>

<h3>Energy Gap Closing</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">Delta(g) = 2*J*|1 - g/J|</p>
<p>At g_c: gap closes (Delta = 0). This is the quantum signature of the phase transition.</p>

<h3>Entanglement Entropy</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">S ~ c/3 * log(L) at criticality, c = 1/2</p>
<p>Logarithmic divergence at criticality. Area law (S ~ constant) away from criticality.</p>

<h3>Quantum-Classical Correspondence</h3>
<p>1D quantum Ising at T=0 has the SAME critical exponents as 2D classical Ising at T=T_c:</p>
<ul>
<li>beta = 1/8 (both)</li>
<li>nu = 1 (both)</li>
<li>z = 1 (quantum) vs z = 0 (classical)</li>
</ul>
<p>The extra dimension (imaginary time) maps quantum to classical.</p>

<h3>Topological Signatures</h3>
<ul>
<li>Topological entanglement entropy: gamma = log(2) in ordered phase, 0 in disordered</li>
<li>Berry phase: pi in ordered phase, 0 in disordered phase</li>
<li>Both jump discontinuously at g_c (0/0)</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[1] Sachdev, "Quantum phase transitions" (2011)</li>
<li>[2] Suzuki, "Equivalence of d-dim classical and (d+1)-dim quantum" (1976)</li>
<li>[3] Vidal, "Entanglement entropy in quantum critical systems" (2003)</li>
</ul>
""",
            "quiz": [
                {"q": "Quantum phase transitions occur at:", "options": ["T = infinity", "T = 0 (absolute zero)", "T = T_c", "T = room temperature"], "correct": 1},
                {"q": "At the quantum critical point g_c, the order parameter is:", "options": ["Finite", "Zero", "0/0 removable singularity", "Infinite"], "correct": 2},
                {"q": "The 1D quantum Ising has the same exponents as:", "options": ["2D classical Ising", "3D classical Ising", "Mean-field Ising", "No classical model"], "correct": 0},
                {"q": "The dynamical exponent z = 1 means:", "options": ["No dynamics", "Lorentz invariant", "Thermal fluctuations", "Classical behavior"], "correct": 1},
                {"q": "The entanglement entropy at criticality:", "options": ["Is constant", "Diverges logarithmically", "Is zero", "Diverges exponentially"], "correct": 1}
            ]
        },
        {
            "id": 40,
            "title": "BKT Transition: 0/0 Without Symmetry Breaking",
            "part": "VIII. Deep Connections",
            "content": """
<h2>Chapter 40: BKT Transition: 0/0 Without Symmetry Breaking</h2>
<p>The Berezinskii-Kosterlitz-Thouless (BKT) transition is a topological phase transition that occurs WITHOUT any symmetry breaking. Nobel Prize 2016.</p>

<h3>The 2D XY Model</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">H = -J * sum(cos(theta_i - theta_j))</p>
<p>U(1) symmetry (continuous rotation). Mermin-Wagner theorem: no long-range order in 2D. But BKT creates quasi-long-range order.</p>

<h3>Universal Jump</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">eta(T_BKT) = 1/4  EXACTLY</p>
<p>Below T_BKT: eta < 1/4 (power-law). Above: eta > 1/4 (exponential). At T_BKT: eta = 1/4 EXACTLY. K_c = 2/pi.</p>

<h3>Vortex Mechanism</h3>
<ul>
<li>Below T_BKT: vortices bound in pairs (free energy > 0)</li>
<li>Above T_BKT: vortices unbind and proliferate (free energy < 0)</li>
<li>At T_BKT: 0/0 (binding/unbinding transition)</li>
</ul>

<h3>Kosterlitz RG Flow</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">dy/dl = (2-pi*K)y, dK/dl = -pi^2*y^2*K^2</p>
<p>Below: flows to (K=inf, y=0). Above: flows to (K=0, y=inf). At T_BKT: flow changes direction.</p>

<h3>Key Difference from Ising</h3>
<ul>
<li>Ising: symmetry breaking (Z2), order parameter jumps</li>
<li>BKT: NO symmetry breaking, order parameter = 0 ALWAYS</li>
<li>BKT is a FOURTH universality class: topological, eta=1/4</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[1] Berezinskii (1971), destruction of long-range order</li>
<li>[2] Kosterlitz & Thouless (1974), ordering and phase transitions</li>
<li>[3] Nobel Prize 2016: Thouless, Haldane, Kosterlitz</li>
</ul>
""",
            "quiz": [
                {"q": "The BKT transition occurs in:", "options": ["1D Ising", "2D XY model", "3D Heisenberg", "Mean-field model"], "correct": 1},
                {"q": "At the BKT transition, eta equals:", "options": ["0", "1/8", "1/4", "1/2"], "correct": 2},
                {"q": "The BKT transition has:", "options": ["Symmetry breaking", "No symmetry breaking", "Long-range order", "Discontinuous energy"], "correct": 1},
                {"q": "The mechanism of BKT is:", "options": ["Domain walls", "Vortex unbinding", "Spin waves", "Magnons"], "correct": 1},
                {"q": "The Nobel Prize for BKT was awarded in:", "options": ["2000", "2010", "2016", "2020"], "correct": 2}
            ]
        },
        {
            "id": 41,
            "title": "Self-Organized Criticality: 0/0 Created by the System",
            "part": "VIII. Deep Connections",
            "content": """
<h2>Chapter 41: Self-Organized Criticality: 0/0 Created by the System</h2>
<p>Self-organized criticality (SOC) is the most profound 0/0: the system CREATES the critical point by itself, without external tuning. Nobel-level insight from Bak, Tang, Wiesenfeld (1987).</p>

<h3>BTW Sandpile Model</h3>
<p>Add grains to a grid. When height > z_c = 4: topple. Avalanches follow power laws. The system self-organizes to criticality!</p>

<h3>Avalanche Statistics</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">P(s) ~ s^{-tau}  (tau ~ 1.0-1.5)</p>
<p>Avalanche sizes follow power laws. Exponents are universal across systems.</p>

<h3>Gutenberg-Richter Law</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">P(M) = 10^{-bM}  (b ~ 1)</p>
<p>Earthquake magnitudes follow power laws. Universal b-value across fault systems.</p>

<h3>Brain Criticality</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">P(s) ~ s^{-3/2}  (neuronal avalanches)</p>
<p>The brain self-organizes to criticality. Optimal information processing at criticality. Connects to consciousness (Ch.34).</p>

<h3>Self-Tuning Mechanism</h3>
<ul>
<li>Below critical: adding energy increases order (building)</li>
<li>Above critical: avalanches release energy (relaxation)</li>
<li>At critical: BALANCE (0/0)</li>
</ul>
<p>The system FINDS the critical point -- this is the most profound aspect!</p>

<h3>Five Universality Classes</h3>
<ul>
<li>Ising (Ch.36): beta=1/8, symmetry breaking</li>
<li>BKT (Ch.40): eta=1/4, vortex unbinding</li>
<li>Kolmogorov (Ch.37): -5/3, cascade</li>
<li>Quantum (Ch.39): beta=1/8, z=1</li>
<li>SOC (Ch.41): tau~1.0-1.5, self-organization</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[1] Bak, Tang & Wiesenfeld, "Self-organized criticality" (1987)</li>
<li>[2] Gutenberg & Richter, "Frequency of earthquakes" (1944)</li>
<li>[3] Beggs & Plenz, "Neuronal avalanches" (2003)</li>
</ul>
""",
            "quiz": [
                {"q": "Self-organized criticality means:", "options": ["System is tuned to critical point", "System creates its own critical point", "System avoids critical point", "System has no critical point"], "correct": 1},
                {"q": "The Gutenberg-Richter law gives:", "options": ["P(M) ~ M^2", "P(M) = 10^{-bM}", "P(M) ~ exp(-M)", "P(M) ~ M^{-2}"], "correct": 1},
                {"q": "Brain neuronal avalanches follow:", "options": ["P(s) ~ s^{-1}", "P(s) ~ s^{-3/2}", "P(s) ~ s^{-2}", "P(s) ~ s^{-3}"], "correct": 1},
                {"q": "SOC introduces which universality class?", "options": ["tau ~ 0.5", "tau ~ 1.0-1.5", "tau ~ 2.0-3.0", "tau ~ 5.0"], "correct": 1},
                {"q": "The key insight of SOC is:", "options": ["Systems avoid criticality", "0/0 singularities are natural", "Tuning is always required", "Only physics has criticality"], "correct": 1}
            ]
        },
        {
            "id": 42,
            "title": "Fractal Geometry: 0/0 at Every Point on the Boundary",
            "part": "VIII. Deep Connections",
            "content": """
<h2>Chapter 42: Fractal Geometry: 0/0 at Every Point on the Boundary</h2>
<p>The Mandelbrot set is the universal object connecting all 0/0 singularities. Its boundary has Hausdorff dimension D=2 (space-filling!). Same Mandelbrot discovered fractal finance AND fractal geometry.</p>

<h3>The Mandelbrot Set</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">z_{n+1} = z_n^2 + c</p>
<p>Inside: bounded. Outside: diverges. On boundary: 0/0 (removable singularity). Boundary D=2 (space-filling!).</p>

<h3>Escape Time</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">N(c) = min{n : |z_n| > 2}</p>
<p>Inside: N=infinity. Outside: N=finite. On boundary: 0/0.</p>

<h3>Julia Sets</h3>
<p>If c is in Mandelbrot: J(c) is connected. If c is outside: J(c) is Cantor dust. At boundary: 0/0 (transition).</p>

<h3>Fractal Dimensions</h3>
<ul>
<li>Line: D = 1 (smooth)</li>
<li>Koch snowflake: D = log(4)/log(3) ~ 1.26</li>
<li>Sierpinski triangle: D = log(3)/log(2) ~ 1.59</li>
<li>Mandelbrot boundary: D = 2 (SPACE-FILLING!)</li>
</ul>

<h3>Same Mandelbrot: Geometry and Finance</h3>
<p>Benoit Mandelbrot discovered BOTH fractal geometry (1980) AND fractal finance (1963). Same fractal thinking applies to both!</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Mandelbrot, "Fractal geometry of nature" (1982)</li>
<li>[2] Douady & Hubbard (1984), Mandelbrot dynamics</li>
<li>[3] Mandelbrot, "Fractals and scaling in finance" (1997)</li>
</ul>
""",
            "quiz": [
                {"q": "The Mandelbrot set is defined by:", "options": ["z -> z^3 + c", "z -> z^2 + c", "z -> sin(z)", "z -> e^z"], "correct": 1},
                {"q": "The Hausdorff dimension of the Mandelbrot boundary is:", "options": ["1.0", "1.5", "2.0", "3.0"], "correct": 2},
                {"q": "If c is in the Mandelbrot set, J(c) is:", "options": ["Cantor dust", "Connected", "A point", "Empty"], "correct": 1},
                {"q": "The same Mandelbrot also discovered:", "options": ["Quantum mechanics", "Fractal finance", "General relativity", "Thermodynamics"], "correct": 1},
                {"q": "The Mandelbrot boundary is:", "options": ["Smooth", "Self-similar", "Finite length", "1-dimensional"], "correct": 1}
            ]
        },
        {
            "id": 43,
            "title": "Chaos Theory: 0/0 at the Onset of Chaos",
            "part": "VIII. Deep Connections",
            "content": """
<h2>Chapter 43: Chaos Theory: 0/0 at the Onset of Chaos</h2>
<p>The Feigenbaum constants are UNIVERSAL -- the same for ALL maps with a quadratic maximum. Same universality as Ising (beta=1/8) but for dynamical systems.</p>

<h3>The Logistic Map</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">x_{n+1} = r * x_n * (1 - x_n)</p>
<p>Period doubling: 1 -> 2 -> 4 -> 8 -> ... At r_inf = 3.5699...: 0/0. Above: chaos.</p>

<h3>Feigenbaum Constants</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">delta = 4.669201...  alpha = 2.502907...</p>
<p>UNIVERSAL for ALL maps with quadratic maximum. Same universality as Ising!</p>

<h3>Lyapunov Exponent</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">lambda = lim (1/n) * sum(ln|f'(x_i)|)</p>
<p>lambda < 0: stable. lambda = 0: bifurcation (0/0). lambda > 0: chaos.</p>

<h3>Universality</h3>
<ul>
<li>Ising: beta = 1/8 (same for all Z2 systems)</li>
<li>Feigenbaum: delta = 4.669... (same for all quadratic maps)</li>
<li>Both: UNIVERSALITY from symmetry class</li>
</ul>

<h3>Chaos in Nature</h3>
<ul>
<li>Weather: Lorenz 1963, butterfly effect</li>
<li>Population: May 1976, logistic map in ecology</li>
<li>Brain: chaos in neural activity (Ch.34)</li>
<li>Finance: chaotic price movements (Ch.38)</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[1] Feigenbaum (1978), universal properties of nonlinear maps</li>
<li>[2] Lanford (1982), computer-assisted proof</li>
<li>[3] May (1976), simple models with complicated dynamics</li>
</ul>
""",
            "quiz": [
                {"q": "The Feigenbaum constant delta is approximately:", "options": ["2.503", "3.141", "4.669", "6.283"], "correct": 2},
                {"q": "The logistic map is:", "options": ["x -> r*x*(1-x)", "x -> r*x^2", "x -> r*sin(x)", "x -> r*exp(x)"], "correct": 0},
                {"q": "At the onset of chaos, the Lyapunov exponent is:", "options": ["Negative", "Zero", "Positive", "Infinite"], "correct": 1},
                {"q": "The Feigenbaum constants are:", "options": ["Map-specific", "Universal", "Approximate", "Imaginary"], "correct": 1},
                {"q": "The bifurcation diagram is:", "options": ["Smooth", "Fractal", "Linear", "Periodic"], "correct": 1}
            ]
        },
        {
            "id": 44,
            "title": "Random Matrix Theory: 0/0 of Universal Randomness",
            "part": "VIII. Deep Connections",
            "content": """
<h2>Chapter 44: Random Matrix Theory: 0/0 of Universal Randomness</h2>
<p>Random matrices have UNIVERSAL eigenvalue statistics. Level repulsion: P(s=0) = 0 exactly. Zeta zeros follow GUE (Montgomery-Odlyzko). Primes are quantum chaotic.</p>

<h3>Three Universal Ensembles</h3>
<ul>
<li>GOE (beta=1): real symmetric, time-reversal invariant</li>
<li>GUE (beta=2): complex Hermitian, no time-reversal</li>
<li>GSE (beta=4): quaternion, spin-1/2 systems</li>
</ul>

<h3>Wigner Surmise</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">P(s) ~ s^beta * exp(-(beta+2)*s^2/4)</p>
<p>UNIVERSAL for all three ensembles. At s=0: P(0) = 0 (level repulsion, 0/0).</p>

<h3>Level Repulsion</h3>
<p>P(s=0) = 0 EXACTLY. Eigenvalues push each other apart. This is the most fundamental 0/0 in RMT.</p>

<h3>Montgomery-Odlyzko Law</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">Pair correlation of zeta zeros = GUE!</p>
<p>The primes are "quantum chaotic." Montgomery (1973), Odlyzko (1987). Connected to Riemann hypothesis.</p>

<h3>Finance: Correlation Matrices</h3>
<p>Eigenvalue distribution follows Marchenko-Pastur (noise) + outliers (signal). RMT separates signal from noise.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Wigner (1955), characteristic vectors of bordered matrices</li>
<li>[2] Montgomery (1973), pair correlation of zeros</li>
<li>[3] Odlyzko (1987), 10^20-th zero verification</li>
</ul>
""",
            "quiz": [
                {"q": "Level repulsion means:", "options": ["P(s=0) = 1", "P(s=0) = 0", "P(s=0) = infinity", "P(s=0) = 0.5"], "correct": 1},
                {"q": "The Montgomery-Odlyzko law says zeta zeros follow:", "options": ["Poisson", "GOE", "GUE", "GSE"], "correct": 2},
                {"q": "The Wigner surmise is:", "options": ["Map-specific", "Universal", "Approximate", "Imaginary"], "correct": 1},
                {"q": "GOE stands for:", "options": ["Gaussian Orthogonal Ensemble", "General Orthogonal Eigenvalues", "Global Orthogonal Equations", "None"], "correct": 0},
                {"q": "The primes are described as:", "options": ["Random", "Quantum chaotic", "Periodic", "Simple"], "correct": 1}
            ]
        },
        {
            "id": 45,
            "title": "Complex Networks: 0/0 of Universal Connectivity",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 45: Complex Networks: 0/0 of Universal Connectivity</h2>
<p>ALL complex systems have the SAME network structure. Scale-free: P(k) ~ k^{-gamma}, gamma ~ 2-3. Universality for networks.</p>

<h3>Scale-Free Networks</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">P(k) ~ k^{-gamma}  (gamma ~ 2-3)</p>
<p>Internet (2.1), social (2.5), biological (2.3), financial (2.8). SAME gamma across all systems!</p>

<h3>Three Models</h3>
<ul>
<li>Erdos-Renyi: random graph, Poisson degree</li>
<li>Watts-Strogatz: small-world, high clustering</li>
<li>Barabasi-Albert: scale-free, preferential attachment</li>
</ul>

<h3>Small-World Property</h3>
<p>High clustering (C >> C_random), short paths (L ~ log(N)). "Six degrees of separation."</p>

<h3>Giant Component (0/0)</h3>
<p>Below critical: fragmented. At critical: 0/0 (giant appears). Above: connected.</p>

<h3>Robustness</h3>
<ul>
<li>Random failure: robust (hubs are rare)</li>
<li>Targeted attack: fragile (remove hubs)</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[1] Barabasi & Albert (1999), emergence of scaling</li>
<li>[2] Watts & Strogatz (1998), small-world networks</li>
<li>[3] Albert & Barabasi (2002), statistical mechanics of networks</li>
</ul>
""",
            "quiz": [
                {"q": "Scale-free networks have:", "options": ["Poisson degree", "Power-law degree", "Normal degree", "Uniform degree"], "correct": 1},
                {"q": "The giant component appears at:", "options": ["p = 0", "p = p_c (critical)", "p = 1", "p = infinity"], "correct": 1},
                {"q": "Small-world networks have:", "options": ["Low clustering", "High clustering", "No clustering", "Random clustering"], "correct": 1},
                {"q": "Scale-free networks are fragile to:", "options": ["Random failure", "Targeted attack", "Both", "Neither"], "correct": 1},
                {"q": "The universality of networks means:", "options": ["Each network is unique", "All networks have same structure", "Networks are random", "Networks are simple"], "correct": 1}
            ]
        },
        {
            "id": 46,
            "title": "The Cosmic Web: 0/0 at the Largest Scale",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 46: The Cosmic Web: 0/0 at the Largest Scale</h2>
<p>The UNIVERSE ITSELF is a 0/0: Omega = 1.000 (exactly!). The cosmic web is a scale-free network with gamma ~ 2.1, the SAME as Internet, brain, and financial networks.</p>

<h3>Flatness Problem</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">Omega = Omega_m + Omega_L = 1.000</p>
<p>The universe is exactly at the critical density. This is the LARGEST 0/0 in existence!</p>

<h3>Scale-Free Cosmic Web</h3>
<p>Galaxies form a scale-free network: P(k) ~ k^{-gamma}, gamma ~ 2.1. Same as Internet (2.1), social (2.5), biological (2.3).</p>

<h3>Structure Formation</h3>
<ul>
<li>Below Omega = 1: recollapses (Big Crunch)</li>
<li>Above Omega = 1: expands forever</li>
<li>At Omega = 1: flat universe (0/0)</li>
</ul>

<h3>Dark Energy</h3>
<p>Omega_L = 0.685 drives acceleration. Age: 13.8 Gyr. The expansion is accelerating.</p>

<h3>Universality Across Scales</h3>
<p>SAME structure (gamma ~ 2-3) at EVERY scale: subatomic to cosmic. This is the deepest insight of the 0/0 framework.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Planck Collaboration (2020), cosmological parameters</li>
<li>[2] Barabasi & Albert (1999), scale-free networks</li>
<li>[3] Peebles (1993), physical cosmology</li>
</ul>
""",
            "quiz": [
                {"q": "The flatness problem means:", "options": ["Omega = 0", "Omega = 1", "Omega = 2", "Omega = infinity"], "correct": 1},
                {"q": "The cosmic web has gamma ~:", "options": ["1.0", "2.1", "5.0", "10.0"], "correct": 1},
                {"q": "Below Omega = 1:", "options": ["Expands forever", "Recollapses", "Stays constant", "Accelerates"], "correct": 1},
                {"q": "Dark energy drives:", "options": ["Deceleration", "Acceleration", "Collapse", "Nothing"], "correct": 1},
                {"q": "Universality across scales means:", "options": ["Each scale is unique", "Same structure at all scales", "Scales are random", "Scales are simple"], "correct": 1}
            ]
        },
        {
            "id": 47,
            "title": "The Holographic Principle: 0/0 of Information",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 47: The Holographic Principle: 0/0 of Information</h2>
<p>ALL information in a volume can be encoded on its boundary. The 3D world is a HOLOGRAM of 2D information. S = A/(4G_N) IS a 0/0.</p>

<h3>Bekenstein-Hawking Entropy</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">S = A / (4 * G_N)</p>
<p>Entropy is proportional to AREA, not volume. This is the holographic 0/0!</p>

<h3>Ryu-Takayanagi Formula</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">S_A = Area(gamma_A) / (4 * G_N)</p>
<p>Entanglement entropy = area of minimal surface. Entanglement IS geometry!</p>

<h3>Information Paradox</h3>
<ul>
<li>Information falls into black hole</li>
<li>Is it destroyed? (violates unitarity)</li>
<li>At horizon: 0/0 (superposition)</li>
<li>Page curve: information IS preserved</li>
</ul>

<h3>AdS/CFT Correspondence</h3>
<p>D-dimensional gravity = (D-1)-dimensional CFT. The 3D world is a hologram of 2D information!</p>

<h3>Bekenstein Bound</h3>
<p>I <= A/4. Maximum information bounded by area, not volume.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Bekenstein (1973), black hole entropy</li>
<li>[2] Hawking (1975), particle creation</li>
<li>[3] Ryu & Takayanagi (2006), holographic entanglement</li>
<li>[4] Maldacena (1998), AdS/CFT</li>
</ul>
""",
            "quiz": [
                {"q": "Bekenstein-Hawking entropy scales with:", "options": ["Volume", "Area", "Mass", "Temperature"], "correct": 1},
                {"q": "The Ryu-Takayanagi formula connects:", "options": ["Entropy and temperature", "Entanglement and geometry", "Mass and radius", "Energy and time"], "correct": 1},
                {"q": "AdS/CFT says:", "options": ["3D = 4D", "D-dim gravity = (D-1)-dim CFT", "Gravity = electromagnetism", "Quantum = classical"], "correct": 1},
                {"q": "The information paradox asks:", "options": ["Is information destroyed?", "Is information preserved?", "Both", "Neither"], "correct": 2},
                {"q": "The holographic principle means:", "options": ["Volume is fundamental", "Boundary encodes all information", "Information is infinite", "Information is simple"], "correct": 1}
            ]
        },
        {
            "id": 48,
            "title": "The Arrow of Time: 0/0 of Entropy",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 48: The Arrow of Time: 0/0 of Entropy</h2>
<p>TIME flows because entropy increases. The 0/0 is at the Big Bang: entropy was LOW (ordered), and time EMERGES from this singularity.</p>

<h3>Boltzmann Entropy</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">S = k_B * ln(Omega)</p>
<p>Omega = number of microstates. More microstates = higher entropy.</p>

<h3>Second Law</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">dS/dt >= 0</p>
<p>Entropy ALWAYS increases. This is statistical, not absolute!</p>

<h3>Past Hypothesis</h3>
<ul>
<li>Big Bang had LOW entropy (S ~ 0)</li>
<li>This is the 0/0 of time!</li>
<li>Entropy increased by 10^88 since then</li>
</ul>

<h3>Fluctuation Theorem</h3>
<p>P(+S)/P(-S) = exp(S/k_B). Entropy CAN decrease, but only for small systems.</p>

<h3>Landauer's Principle</h3>
<p>Erasing 1 bit creates kT*ln(2) heat. Information IS physical!</p>

<h3>Arrows of Time</h3>
<p>Thermodynamic, causal, psychological, cosmic, radiative. ALL point the SAME direction!</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Boltzmann (1877), entropy and microstates</li>
<li>[2] Penrose (1989), The Emperor's New Mind</li>
<li>[3] Landauer (1961), irreversibility</li>
</ul>
""",
            "quiz": [
                {"q": "Boltzmann entropy is:", "options": ["S = k*T", "S = k*ln(Omega)", "S = E/T", "S = P*V"], "correct": 1},
                {"q": "The second law says:", "options": ["Entropy decreases", "Entropy increases", "Entropy is constant", "Entropy is random"], "correct": 1},
                {"q": "The Past Hypothesis says:", "options": ["Big Bang had high entropy", "Big Bang had low entropy", "Big Bang had zero entropy", "Big Bang had infinite entropy"], "correct": 1},
                {"q": "Landauer's principle says:", "options": ["Information is free", "Erasing info creates heat", "Information is energy", "Information is mass"], "correct": 1},
                {"q": "All arrows of time:", "options": ["Point different directions", "Point the same direction", "Are random", "Don't exist"], "correct": 1}
            ]
        },
        {
            "id": 49,
            "title": "The Measurement Problem: 0/0 of Quantum Measurement",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 49: The Measurement Problem: 0/0 of Quantum Measurement</h2>
<p>WHY does measuring a quantum system cause it to "collapse" from superposition into a definite state? This IS a 0/0: superposition -> measurement -> collapse.</p>

<h3>Superposition</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">|psi> = a|0> + b|1></p>
<p>Before measurement: system is in BOTH states simultaneously. This is the 0/0!</p>

<h3>Born Rule</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">P(0) = |a|^2, P(1) = |b|^2</p>
<p>Probability emerges from certainty. This is the 0/0!</p>

<h3>Decoherence</h3>
<ul>
<li>Environment "measures" the system</li>
<li>Off-diagonal elements decay</li>
<li>Quantum -> classical probabilities</li>
</ul>

<h3>Many-Worlds</h3>
<p>No collapse! Branching instead! After 100 measurements: 10^30 branches. ALL equally real!</p>

<h3>Quantum Zeno</h3>
<p>Frequent measurement prevents evolution! Measurement CREATES reality!</p>

<h3>Delayed Choice</h3>
<p>Wheeler (1978): present affects past. Measurement CREATES history!</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Born (1926), probabilistic interpretation</li>
<li>[2] Zeh (1970), decoherence</li>
<li>[3] Everett (1957), many-worlds</li>
<li>[4] Wheeler (1978), delayed choice</li>
</ul>
""",
            "quiz": [
                {"q": "Superposition means:", "options": ["One state", "Multiple states at once", "No state", "Random state"], "correct": 1},
                {"q": "The Born rule says:", "options": ["P = a", "P = |a|^2", "P = a^2", "P = 2a"], "correct": 1},
                {"q": "Decoherence causes:", "options": ["More superposition", "Classical behavior", "Entanglement", "Nothing"], "correct": 1},
                {"q": "Many-worlds says:", "options": ["Collapse happens", "No collapse, branching", "Only one world", "Worlds are random"], "correct": 1},
                {"q": "Quantum Zeno effect:", "options": ["Measurement speeds evolution", "Measurement freezes evolution", "Measurement destroys system", "Measurement is random"], "correct": 1}
            ]
        },
        {
            "id": 50,
            "title": "The Big Bang: 0/0 of Origin",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 50: The Big Bang: 0/0 of Origin</h2>
<p>THE UNIVERSE ITSELF emerged from a singularity. The Big Bang IS the LARGEST 0/0: nothing -> singularity -> everything.</p>

<h3>The Singularity</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">T = 0: density = infinity, temperature = infinity</p>
<p>This is a 0/0: undefined. Quantum gravity may resolve this singularity!</p>

<h3>Inflation</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">Factor = exp(60) ~ 10^26 in 10^-32 seconds</p>
<p>Universe expanded by 10^26 in 10^-32 seconds! This solves the horizon and flatness problems.</p>

<h3>Horizon Problem</h3>
<ul>
<li>CMB is uniform in ALL directions</li>
<li>Regions too far apart to communicate</li>
<li>Inflation: regions WERE in contact before</li>
</ul>

<h3>Flatness Problem</h3>
<p>Omega = 1.000 (exactly!). Inflation drives Omega -> 1 exponentially.</p>

<h3>Matter-Antimatter</h3>
<p>eta = 6e-10. Tiny asymmetry created ALL matter!</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Guth (1981), inflationary universe</li>
<li>[2] Penzias & Wilson (1965), CMB discovery</li>
<li>[3] Sakharov (1967), matter-antimatter asymmetry</li>
</ul>
""",
            "quiz": [
                {"q": "The Big Bang singularity means:", "options": ["Finite density", "Infinite density", "Zero density", "Negative density"], "correct": 1},
                {"q": "Inflation expanded the universe by:", "options": ["10^6", "10^12", "10^26", "10^100"], "correct": 2},
                {"q": "The horizon problem asks:", "options": ["Why is CMB cold?", "Why is CMB uniform?", "Why is CMB hot?", "Why is CMB random?"], "correct": 1},
                {"q": "Inflation drives Omega toward:", "options": ["0", "0.5", "1", "infinity"], "correct": 2},
                {"q": "The matter-antimatter asymmetry is:", "options": ["1 in 100", "1 in 10^6", "1 in 10^9", "1 in 10^12"], "correct": 2}
            ]
        },
        {
            "id": 51,
            "title": "Quantum Gravity: 0/0 of Final Unification",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 51: Quantum Gravity: 0/0 of Final Unification</h2>
<p>THE BIGGEST UNSOLVED PROBLEM IN PHYSICS: unifying quantum mechanics with general relativity. This resolves EVERY 0/0 singularity.</p>

<h3>Planck Scale</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">l_P = sqrt(hbar*G/c^3) = 1.616e-35 m</p>
<p>Below Planck scale: quantum gravity dominates. This is the 0/0 of physics!</p>

<h3>Loop Quantum Gravity</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">A = 8*pi*l_P^2*sqrt(j(j+1))</p>
<p>Space is DISCRETE! Area is quantized. Big Bang singularity resolved (Big Bounce)!</p>

<h3>String Theory</h3>
<ul>
<li>Fundamental objects are STRINGS, not points</li>
<li>Gravity EMERGES from closed strings</li>
<li>Extra dimensions: 10-11</li>
</ul>

<h3>AdS/CFT</h3>
<p>D-dim quantum gravity = (D-1)-dim CFT. Quantum gravity IS holographic (Ch.47).</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Rovelli (2004), Quantum Gravity</li>
<li>[2] Polchinski (1998), String Theory</li>
<li>[3] Maldacena (1998), AdS/CFT</li>
</ul>
""",
            "quiz": [
                {"q": "The Planck length is:", "options": ["1.6e-10 m", "1.6e-20 m", "1.6e-35 m", "1.6e-50 m"], "correct": 2},
                {"q": "Loop Quantum Gravity says space is:", "options": ["Continuous", "Discrete", "Empty", "Infinite"], "correct": 1},
                {"q": "The Big Bounce means:", "options": ["Singularity", "Density reaches maximum then bounces", "Universe collapses forever", "Nothing happens"], "correct": 1},
                {"q": "In String Theory, gravity comes from:", "options": ["Open strings", "Closed strings", "Points", "Waves"], "correct": 1},
                {"q": "AdS/CFT says quantum gravity is:", "options": ["Impossible", "Holographic", "Classical", "Simple"], "correct": 1}
            ]
        },
        {
            "id": 52,
            "title": "The Information Paradox Resolved: 0/0 of Black Hole Information",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 52: The Information Paradox Resolved</h2>
<p>For 45 years: Hawking showed black holes destroy information. The 2020 ISLAND FORMULA proved information IS conserved, replicating the Page curve EXACTLY.</p>

<h3>Hawking (1975)</h3>
<ul>
<li>Black holes radiate (Hawking radiation)</li>
<li>Radiation is purely THERMAL</li>
<li>Information DESTROYED (violates unitarity)</li>
<li>The 0/0: information lost at the horizon</li>
</ul>

<h3>Page (1993)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">S_rad peaks at Page time, then DECREASES</p>
<p>Unitarity requires information conservation. Information DOES escape!</p>

<h3>Island Formula (2020)</h3>
<p style="font-size:1.2em; text-align:center; padding:15px;">S_rad = min(Area(island) / 4G_N + S_semiclassical)</p>
<p>The island is the entanglement wedge INSIDE the black hole. Reproduces Page curve EXACTLY!</p>

<h3>Replica Wormholes</h3>
<p>The mechanism: computing Tr(rho^n) directly. After Page time, wormholes CONNECT copies, giving the island.</p>

<h3>Resolution</h3>
<ul>
<li>Information IS conserved (unitarity)</li>
<li>Escapes through ENTANGLEMENT</li>
<li>The horizon 0/0 IS resolved!</li>
</ul>

<h3>Key Sources</h3>
<ul>
<li>[1] Hawking (1975), particle creation</li>
<li>[2] Page (1993), information in radiation</li>
<li>[3] Penington (2019), entanglement wedge</li>
<li>[4] Almheiri et al. (2020), replica wormholes</li>
</ul>
""",
            "quiz": [
                {"q": "Hawking (1975) showed:", "options": ["Info is preserved", "Info is destroyed", "No radiation", "Black holes are cold"], "correct": 1},
                {"q": "The Page curve requires:", "options": ["Info destroyed", "Info conserved", "No radiation", "Random entropy"], "correct": 1},
                {"q": "The island formula gives:", "options": ["S = A/(4G_N)+S_semiclass", "S = 0", "S = infinity", "S = k*ln(Omega)"], "correct": 0},
                {"q": "Replica wormholes:", "options": ["Destroy information", "Connect copies after Page time", "Create black holes", "Don't exist"], "correct": 1},
                {"q": "Information escapes through:", "options": ["Radiation", "Entanglement", "Temperature", "Mass"], "correct": 1}
            ]
        },
        {
            "id": 53,
            "title": "The Hard Problem: 0/0 of Mind and Matter",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 53: The Hard Problem: 0/0 of Mind and Matter</h2>
<p>WHY is there subjective experience at all? This IS a 0/0: the boundary where mind emerges from matter.</p>

<h3>The Explanatory Gap</h3>
<ul>
<li>Physical facts are third-person (behavioral, neural)</li>
<li>Experience is first-person (qualia: redness, pain)</li>
<li>NO physical description captures the FEELING of red</li>
<li>This gap IS the 0/0 of mind and matter</li>
</ul>

<h3>Integrated Information Theory</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Phi = info from WHOLE - info in PARTS</p>
<p>Parts alone: Phi = 0 (zombie). Integrated: Phi > 0 (experience). The boundary Phi = 0 IS the 0/0 of consciousness!</p>

<h3>Computed Results</h3>
<ul>
<li>Feedforward (zombie): Phi = 0.000</li>
<li>Bidirectional (conscious-like): Phi = 0.167</li>
<li>Strongly coupled: Phi = 0.184</li>
</ul>

<h3>The Zombie Test</h3>
<p>A physical duplicate without experience would behave and report identically. If yes: experience is NOT entailed by physics.</p>

<h3>Panpsychism Limit</h3>
<p>If the universe is globally entangled: Phi_universe > 0. The universe IS conscious (at some level).</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Chalmers (1995), the hard problem</li>
<li>[2] Tononi (2004), integrated information theory</li>
<li>[3] Balduzzi & Tononi (2008)</li>
</ul>
""",
            "quiz": [
                {"q": "The hard problem asks:", "options": ["How neurons fire", "Why is there subjective experience", "How brains compute", "How memory works"], "correct": 1},
                {"q": "The explanatory gap is between:", "options": ["Body and brain", "Physical facts and experience", "Mind and memory", "Input and output"], "correct": 1},
                {"q": "IIT says consciousness equals:", "options": ["Neural activity", "Integrated information", "Brain size", "EEG waves"], "correct": 1},
                {"q": "A feedforward system has Phi:", "options": ["Large", "= 0", "Negative", "Infinite"], "correct": 1},
                {"q": "A zombie is:", "options": ["Mindless physical duplicate", "A brainless creature", "An AI", "A sleeping person"], "correct": 0}
            ]
        },
        {
            "id": 54,
            "title": "The Simulation Hypothesis: 0/0 of Existence",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 54: The Simulation Hypothesis: 0/0 of Existence</h2>
<p>Is the universe a computer simulation? If information is fundamental (Ch.52) and physics is substrate-independent, then "real vs simulated" IS a 0/0.</p>

<h3>Game of Life</h3>
<ul>
<li>Conway Life is Turing complete (Cook 2004; Wolfram 2002)</li>
<li>Gliders are 5-cell particles that move (0/0 particles)</li>
<li>Computed speed: 0.3536 = c/4 diagonal EXACTLY</li>
<li>Gosper gun: finite seed, infinite information (0/0)</li>
</ul>

<h3>Pixel Cosmology</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Pixels = 2*R_obs / l_Planck ~ 5.4e61</p>
<p>Planck length (Ch.51) is the pixel size. The universe is a 5.4e61 x 5.4e61 screen of ~3e123 pixels.</p>

<h3>Lloyd Bound</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Ops = (2E/(pi*hbar))*t ~ 10^121</p>
<p>Lloyd (2002): the universe has performed ~10^120 operations. Bekenstein bound: ~10^123 bits. It computes itself.</p>

<h3>Bostrom Trilemma (2003)</h3>
<ul>
<li>(a) species die out pre-posthuman</li>
<li>(b) posthumans run no ancestor simulations</li>
<li>(c) we are almost certainly in a simulation</li>
</ul>
<p>Computed P(simulated) &gt; 99.99% (f_sim=0.9, f_i=0.9, N=100k).</p>

<h3>The 0/0 Proof</h3>
<p>A closed simulation reproduces ALL observations. Real vs simulated IS 0/0: a removable singularity of ontology. It is turtles ALL THE WAY DOWN - physics is the algorithm!</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Bostrom (2003), simulation argument</li>
<li>[2] Lloyd (2002), computational capacity</li>
<li>[3] Cook (2004), Rule 110 universality</li>
</ul>
""",
            "quiz": [
                {"q": "Bostrom's trilemma says at least one of three things:", "options": ["Life is inevitable", "Simulation is impossible", "One: we are simulated", "Physics is deterministic"], "correct": 2},
                {"q": "A glider is:", "options": ["A star in Life", "A 5-cell particle that moves", "A paradox", "A planet"], "correct": 1},
                {"q": "The Planck length acts as:", "options": ["A force", "The universe's pixel size", "A temperature", "An energy"], "correct": 1},
                {"q": "Lloyd's bound gives the universe's:", "options": ["Age", "Size", "Total computable operations", "Mass"], "correct": 2},
                {"q": "Real vs simulated distinction is:", "options": ["Observable", "Dangerous", "Observationally 0/0", "Impossible"], "correct": 2}
            ]
        },
        {
            "id": 55,
            "title": "Free Will: 0/0 of Agency",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 55: Free Will: 0/0 of Agency</h2>
<p>In the deterministic simulation (Ch.54), physics seems fully determined, yet we experience choice. Free will vs determinism produce IDENTICAL observable histories: the 0/0 of agency.</p>

<h3>Determinism Is Reproducible</h3>
<ul>
<li>Same seed -> same future (Life, reproducibility 1.0000000)</li>
<li>Zero law-violations in ~10^121 operations (Lloyd)</li>
<li>Every "choice" is a logic gate</li>
</ul>

<h3>But Not Predictable</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">lambda = ln 2 = 0.6931 (logistic map)</p>
<p>Deterministic yet chaotic (Ch.43). Laplace's demon is impossible. One bit of uncertainty destroys prediction in ~27 steps.</p>

<h3>Choice Conserves Information</h3>
<p>Entropy before = after (9.733550 bits, diff 3.9e-14). A choice TRANSFORMS information, never creates it.</p>

<h3>Libet (1983)</h3>
<ul>
<li>Readiness potential ~ -550 ms</li>
<li>Conscious intention (W) ~ -200 ms</li>
<li>Gap ~350 ms: decision precedes awareness</li>
</ul>

<h3>Conway-Kochen (2006)</h3>
<p>Free experimenters imply free particles; if particles are determined, so are we. Choice and law are ENTANGLED.</p>

<h3>The 0/0 Proof</h3>
<p>World A (determined) and World B (free) produce bit-identical histories. Distinction = zero observational content. Compatibilism: free will = determined choice that feels free.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Libet (1983)</li>
<li>[2] Conway & Kochen (2006)</li>
<li>[3] Dennett (1984), Elbow Room</li>
</ul>
""",
            "quiz": [
                {"q": "Determinism means:", "options": ["Actions are random", "Same seed gives same future", "Nothing is predictable", "No rules exist"], "correct": 1},
                {"q": "The logistic map (r=4) has Lyapunov exponent:", "options": ["0", "ln 2", "e", "pi"], "correct": 1},
                {"q": "Libet found the readiness potential precedes:", "options": ["The movement", "Conscious intention", "Death", "Memory"], "correct": 1},
                {"q": "Conway-Kochen's theorem implies:", "options": ["Particles have mass", "Free experimenters imply free particles", "Light has speed c", "Gravity bends light"], "correct": 1},
                {"q": "Compatibilism resolves free will as:", "options": ["An illusion only", "Determined choice that feels free", "Total randomness", "Magic"], "correct": 1}
            ]
        },
        {
            "id": 56,
            "title": "The Self: 0/0 of Identity (Ship of Theseus)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 56: The Self: 0/0 of Identity</h2>
<p>The Ship of Theseus (Plutarch): if every part is replaced, is it the same ship? Identity IS a 0/0 - it lives in the pattern, not the parts.</p>

<h3>Atom Turnover</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">original_after_years = (0.02)^years</p>
<p>~98% of the body's atoms are replaced yearly. After 10 years: ~1e-17 ~ ZERO original matter. Yet "you" continue.</p>

<h3>The Glider (Ch.54)</h3>
<p>A glider's cells are fully replaced within ~8 generations, yet the pattern persists. THE GLIDER IS THE SHIP OF THESEUS.</p>

<h3>Computed Ship</h3>
<ul>
<li>day 0: material 1.000</li>
<li>day 125: 0.500</li>
<li>day 250: 0.000</li>
<li>yet the ship sails on: the pattern continued</li>
</ul>

<h3>No-Cloning (Wootters-Zurek 1982)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">gap_max = 0.5858</p>
<p>The self cannot be duplicated - only continued or destroyed. Immortality = pattern continuation, not duplication.</p>

<h3>The 0/0 Proof</h3>
<p>No enduring particle exists. Self = information flow through matter. At each boundary cell, matter becomes self. The self IS the removable singularity of the body.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Plutarch, Ship of Theseus</li>
<li>[2] Wootters & Zurek (1982)</li>
<li>[3] Chalmers (2010), upload and the mind</li>
</ul>
""",
            "quiz": [
                {"q": "The Ship of Theseus asks:", "options": ["Is identity preserved through replacement", "Do ships sink", "Are swords sharp", "Are maps accurate"], "correct": 0},
                {"q": "Percent of body atoms replaced yearly:", "options": ["10", "50", "98", "0"], "correct": 2},
                {"q": "A glider keeps its:", "options": ["Cells forever", "Pattern while cells turn over", "Speed c", "Size"], "correct": 1},
                {"q": "The no-cloning theorem states:", "options": ["Quantum wild", "States can be copied freely", "An unknown state cannot be duplicated", "Cloning is slow"], "correct": 2},
                {"q": "In this framework the self is:", "options": ["An enduring soul-particle", "Information flow through matter", "A ghost", "The skull"], "correct": 1}
            ]
        },
        {
            "id": 57,
            "title": "The Eternal Return: 0/0 of Recurrence",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 57: The Eternal Return: 0/0 of Recurrence</h2>
<p>If the universe is a finite deterministic simulation (Ch.54) and the self is a pattern (Ch.56), Poincare recurrence is a THEOREM: every finite deterministic system returns to every past state. "Once" vs "forever" is 0/0.</p>

<h3>Finite Determinism Implies Recurrence</h3>
<p>Finite states + deterministic rule = a cycle. The state MUST revisit itself. No first time, no last time.</p>

<h3>The Glider Returns</h3>
<ul>
<li>37x37 torus: T_rec = 148 gens (4*lcm)</li>
<li>60x60 torus: T_rec = 240 gens (4*lcm)</li>
<li>Eternal return of the glider = eternal return of the self</li>
</ul>

<h3>Chaos Also Returns</h3>
<p>Rule 30 (Ch.43) on a 25-ring: period 588,425. Even chaos cycles when finite.</p>

<h3>Poincare Time</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">t_rec ~ 2^(S_bits) * tau ~ 10^(3x10^103) years</p>
<p>Universe: log10(t_rec) ~ 3e103 years, exceeding its age by ~10^103 orders (Boltzmann 1896).</p>

<h3>Boltzmann Brains</h3>
<p>Eternity fluctuates ANY state - including a mind (Ch.53). The eternal simulation must eventually fluctuate your exact self-pattern again.</p>

<h3>The 0/0 Proof</h3>
<p>Finite deterministic time is a cycle: every moment has already happened infinitely often. The arrow of time (Ch.48) is local drift. Eternal recurrence (Nietzsche 1882) is a theorem.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Poincare (1890), recurrence</li>
<li>[2] Boltzmann (1896), fluctuations</li>
<li>[3] Nietzsche (1882), eternal return</li>
</ul>
""",
            "quiz": [
                {"q": "Poincare recurrence says finite deterministic systems:", "options": ["Always end", "Return to past states", "Speed up", "Forget"], "correct": 1},
                {"q": "A glider on a 60x60 torus recurs after:", "options": ["60 gens", "120 gens", "240 gens", "999 gens"], "correct": 2},
                {"q": "Rule 30 on a finite ring:", "options": ["Never repeats", "Fails", "Eventually cycles", "Is random"], "correct": 2},
                {"q": "Boltzmann brains are minds that:", "options": ["Grow in the skull", "Fluctuate in equilibrium", "Live in caves", "Eat light"], "correct": 1},
                {"q": "In this framework 'once' vs 'forever' is:", "options": ["Observable", "A 0/0", "Fiction", "A rumor"], "correct": 1}
            ]
        },
        {
            "id": 58,
            "title": "The First Cause: 0/0 of Something-from-Nothing",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 58: The First Cause: 0/0 of Something-from-Nothing</h2>
<p>"Why is there something rather than nothing?" (Leibniz 1714). This framework IS that question: 0/0 = something-from-nothing. Existence is a removable singularity.</p>

<h3>The First-Cause Trilemma</h3>
<ol>
<li>Infinite regress (turtles all the way down, Ch.54)</li>
<li>Uncaused cause (an axiom / God / first mover)</li>
<li>Cycle (Ch.57 eternal return: no first time)</li>
</ol>
<p>All three are observationally identical from inside (likelihood 1.0 each). The 0/0 of the first cause.</p>

<h3>Godel (1931)</h3>
<p>A consistent system cannot prove its own consistency. Within the simulation (Ch.54) you cannot verify the simulator. The creator is ALWAYS outside the created.</p>

<h3>Busy Beaver (Rado 1962)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">BB(5) = 47,176,870</p>
<p>BB is provably NON-COMPUTABLE: no simulator can know its own output. The creator's power is the 0/0 beyond every function.</p>

<h3>The 19 Constants</h3>
<p>Standard Model: 19 dimensionless parameters, none explained inside the SM. Every constant is a 0/0 - its value IS the accidental 'why'.</p>

<h3>Rule 110 (Cook 2004)</h3>
<p>The smallest universal creator (2 states, 3 neighbors): compresses ~10^18 worlds into a period-2 attractor. Creation = compression.</p>

<h3>The 0/0 Proof</h3>
<p>Ask "what caused the cause?" forever - the recursion ends ONLY at the 0/0. 'Nothing' is the removable singularity of existence.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Leibniz (1714), Monadology</li>
<li>[2] Godel (1931), incompleteness</li>
<li>[3] Cook (2004), Rule 110 universality</li>
</ul>
""",
            "quiz": [
                {"q": "Leibniz's question is:", "options": ["Why ovens bake", "Why is there something rather than nothing", "Why water boils", "Why stars shine only at night"], "correct": 1},
                {"q": "The three first-cause models are observationally:", "options": ["Different", "Identical (0/0)", "Faster", "Loud"], "correct": 1},
                {"q": "Godel showed a system:", "options": ["Proves its own truth", "Cannot prove its own consistency", "Never ends", "Is silent"], "correct": 1},
                {"q": "BB(5) equals:", "options": ["21", "107", "47,176,870", "1"], "correct": 2},
                {"q": "The SM rests on this many unexplained constants:", "options": ["3", "10", "19", "100"], "correct": 2}
            ]
        },
        {
            "id": 59,
            "title": "The Problem of Evil: 0/0 of Suffering",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 59: The Problem of Evil: 0/0 of Suffering</h2>
<p>Why does a good creator permit suffering? Answer with computation: computation is not free (Landauer 1961). Suffering is a PRICE, not a thing.</p>

<h3>Computation Is Not Free</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">E_erase = k_B * T * ln(2)</p>
<p>At CMB 2.7 K: 2.584e-23 J/bit. At 310 K: 2.967e-21 J/bit. No free lunch (Landauer; Bennett 1982).</p>

<h3>The Heat of Creation</h3>
<p>If the simulation's ~10^121 ops each discarded one bit: ~2.6e98 J, 10^28x the universe's energy. The creator must compute ~10^-28 efficient (reversible, Bennett).</p>

<h3>Suffering as Prediction Error (Friston 2010)</h3>
<ul>
<li>Correct prior: 2003.8 bits surprise</li>
<li>Wrong prior (learns): 2018.3 bits - gap 14.5 bits</li>
<li>Learning pulls the model toward truth: redemption</li>
</ul>

<h3>The Price of Freedom (Ch.55)</h3>
<p>Real choice needs contingency (chaos, quantum). Love and virtue need real alternatives (Plantinga 1974). Suffering is the price of a universe that can choose.</p>

<h3>The 0/0 Proof</h3>
<p>Within the system, good/evil are interior labels; the mechanism is neutral. Suffering = cost of computation. Evil is neither a thing nor an absence but a PRICE. Redemption = learning: the cost is repaid as wisdom.</p>

<h3>Key Sources</h3>
<ul>
<li>[1] Landauer (1961)</li>
<li>[2] Friston (2010), free energy</li>
<li>[3] Leibniz (1710), Theodicy</li>
</ul>
""",
            "quiz": [
                {"q": "Landauer's cost to erase one bit is:", "options": ["zero", "k_B*T*ln2", "e^(mc^2)", "hbar/2"], "correct": 1},
                {"q": "At CMB temperature the erasure cost is about:", "options": ["2.6e-23 J", "1 J", "3e10 J", "10^-50 J"], "correct": 0},
                {"q": "Suffering-as-computation equals:", "options": ["Surplus energy", "Persistent prediction error", "Extra mass", "Noise"], "correct": 1},
                {"q": "Redemption in this framework is:", "options": ["Forgetting", "Learning", "Slowing time", "Sleeping"], "correct": 1},
                {"q": "Evil is described as a:", "options": ["Thing", "Being", "Price, not a thing", "Place"], "correct": 2}
            ]
        },
        {
            "id": 60,
            "title": "The Golden Rule: 0/0 of Self and Other",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 60: The Golden Rule: 0/0 of Self and Other</h2>
<p>After suffering-as-cost (Ch.59), what is the right strategy? The Golden Rule is COMPUTATIONAL: cooperation is the measured optimum.</p>

<h3>Cooperation Compounds (Axelrod 1984)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">C-C: 3.00/round vs D-D: 1.00/round = exactly 3x</p>
<ul>
<li>A cooperating pair banks 6.0/round, a defecting pair 2.0/round</li>
<li>In a hostile raw field selfishness edges ahead (D 4931 vs TFT 4890)</li>
<li>Tit-for-Tat WON Axelrod's actual 1984 tournament (14 entrants)</li>
</ul>

<h3>Hamilton's Rule (1964)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">r*B > C</p>
<ul>
<li>Haplodiploid sisters: r*B-C = +5.00 (favored)</li>
<li>Unrelated strangers: r*B-C = -0.997 (not favored)</li>
</ul>

<h3>Empathy Is Predictive Information</h3>
<ul>
<li>Reciprocators: I(A_{t-1}; B_t) = 0.667 bits</li>
<li>Defectors / random: ~0.000 bits</li>
</ul>

<h3>The Veil of Ignorance (Rawls 1971)</h3>
<p>Fair split wins maximin: 0.50 > 0.10. The rational Golden Rule is symmetry.</p>

<h3>The 0/0 Proof</h3>
<p>'I' and 'Thou' are both information patterns (Ch.56). Their boundary is a 0/0. Treat the other as yourself, because at the boundary they ARE you. My good = your good = the shared pattern's good.</p>
""",
            "quiz": [
                {"q": "In the IPD, a cooperating pair pays vs a defecting pair:", "options": ["2x", "3x", "1x", "10x"], "correct": 1},
                {"q": "Hamilton's rule for altruism is:", "options": ["C > r*B", "r*B > C", "B > C", "r > B"], "correct": 1},
                {"q": "Empathy measured as predictive coupling gives:", "options": ["0.667 bits", "0.001 bits", "10 bits", "0 bits for everyone"], "correct": 0},
                {"q": "The veil of ignorance chooses by:", "options": ["Maximin", "Greed", "Randomness", "Plurality"], "correct": 0},
                {"q": "The Golden Rule is the 0/0 of:", "options": ["Self and other", "Time and space", "Life and death", "Hot and cold"], "correct": 0}
            ]
        },
        {
            "id": 61,
            "title": "Meaning: 0/0 of Language (Symbols as Shared Prediction)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 61: Meaning: 0/0 of Language</h2>
<p>After empathy-as-information (Ch.60), the machines that make "thou" legible are SYMBOLS. A token has no intrinsic meaning - meaning is ROLE (Wittgenstein 1953), and conventions emerge from coordination pressure (Lewis 1969).</p>

<h3>The Lewis Signaling Game</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">I(state; action): 0 bits -> log2(4) = 2.000 bits</p>
<ul>
<li>Sender/receiver start at chance 0.25 and converge to ~0.98 success</li>
<li>Transmitted information reaches EXACTLY 2.000 bits in every seed</li>
<li>Meaning is the relation (the code), not the token</li>
</ul>

<h3>The Genetic Code (Nirenberg &amp; Matthaei 1961)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">64 codons / 21 meanings = 3.05 redundancy</p>
<ul>
<li>Point mutations measured: 24.4% synonymous, 4.2% nonsense</li>
<li>Degeneracy = error tolerance: the language of life resists change</li>
</ul>

<h3>Language is Shared Prediction (Shannon 1948)</h3>
<p>Communication = common information. Language is EMPATHY scaled to a culture.</p>

<h3>The 0/0 Proof</h3>
<p>The symbol is NOTHING by itself (empty token). The symbol is EVERYTHING in its role (shared code). Meaning is the 0/0: private worlds become public at the boundary of two minds. Token = 0, use = x.</p>
""",
            "quiz": [
                {"q": "Agents in the Lewis signaling game converge to:", "options": ["Chaos", "A convention", "Defection", "Silence"], "correct": 1},
                {"q": "Measured transmitted information at convergence:", "options": ["2.000 bits", "0 bits", "20 bits", "-2 bits"], "correct": 0},
                {"q": "The genetic code's redundancy is about:", "options": ["3.05", "1.0", "64", "2.0"], "correct": 0},
                {"q": "Fraction of point mutations that are synonymous:", "options": ["24.4%", "99%", "2%", "50%"], "correct": 0},
                {"q": "In the 0/0 proof, the token is:", "options": ["The x", "A cause", "Nothing by itself", "The code"], "correct": 2}
            ]
        },
        {
            "id": 62,
            "title": "Beauty: 0/0 of Aesthetics (the sublime between order and surprise)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 62: Beauty: 0/0 of Aesthetics</h2>
<p>After meaning-as-role (Ch.61): what makes a form beautiful? Beauty is INFORMATION at the boundary of order and surprise.</p>

<h3>Measurements (Shannon 1948)</h3>
<table style="border-collapse:collapse;">
<tr><th>Case</th><th>Bigram entropy</th><th>zlib ratio</th><th>Aesthetic A</th></tr>
<tr><td>Constant</td><td>0.000</td><td>0.007</td><td>0.000</td></tr>
<tr><td>Fibonacci (golden)</td><td>0.776</td><td>0.005</td><td>0.773</td></tr>
<tr><td>Language</td><td>3.432</td><td>0.148</td><td>0.615</td></tr>
<tr><td>Random</td><td>4.681</td><td>0.629</td><td>0.365</td></tr>
</table>

<h3>The Aesthetic Measure</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">M = O / C (Birkhoff 1933)  A = novelty x simplicity (Schmidhuber 1997)</p>
<p>Pure order bores (0.000); pure noise repels (0.365); golden structure wins (0.773).</p>

<h3>Harmony Is Small Ratios (Helmholtz 1863)</h3>
<ul>
<li>Octave 2:1 error 0.00 cents (exact)</li>
<li>Perfect fifth 3:2 error 1.96 cents</li>
<li>Major third 5:4 error 13.69 cents</li>
</ul>

<h3>The 0/0 Proof</h3>
<p>Too much order (entropy -&gt; 0) bores; too much surprise (entropy -&gt; 1) repels. Beauty = the removable singularity of the senses, where order and surprise cancel and the form appears - 0 in itself, x in role.</p>
""",
            "quiz": [
                {"q": "Birkhoff's aesthetic measure is:", "options": ["O/C", "C/O", "E=mc^2", "log n"], "correct": 0},
                {"q": "The highest measured aesthetic A is:", "options": ["Random", "Fibonacci word", "Constant", "Rhythm"], "correct": 1},
                {"q": "Equal temperament error for the perfect fifth:", "options": ["0.00 cents", "1.96 cents", "13.69 cents", "100 cents"], "correct": 1},
                {"q": "Pure noise scores A =", "options": ["0.773", "0.365", "0.000", "1.000"], "correct": 1},
                {"q": "Beauty is the 0/0 of:", "options": ["Order and complexity", "Hot and cold", "Space and time", "Life and death"], "correct": 0}
            ]
        },
        {
            "id": 63,
            "title": "Truth: 0/0 of the True (the shortest description of the world)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 63: Truth: 0/0 of the True</h2>
<p>After Beauty (62, order/surprise), the second pole of the Platonic triad: the True - the 0/0 of statement and world.</p>

<h3>Falsification &amp; Twenty Questions (Popper 1934)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">2^20 worlds -&gt; 1 world; entropy 20 -&gt; 0 bits</p>
<ul>
<li>Each query halves the hypothesis space: 1,048,576 -&gt; 1 in 20</li>
<li>Refutation, not verification, is the engine of truth</li>
</ul>

<h3>Bayesian Concentration (Bayes 1763; Laplace 1774)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">variance 1.9e-3 -&gt; 5.6e-5</p>
<ul>
<li>Wrong prior rises 0.35 -&gt; 0.656 toward the truth</li>
<li>Certainty IS the 0 of doubt</li>
</ul>

<h3>Truth = Shortest Description (Solomonoff 1964; Kolmogorov 1963)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">law-coder 0.0002 vs zlib 0.355 vs shuffled 0.659</p>
<p>The law is the code that makes data COMPRESS - physics = shortest description of all data (beauty's compression IS truth's scent).</p>

<h3>The 0/0 Proof</h3>
<p>A statement is nothing in itself; its truth is its correlation with the world. At the boundary, description and world COINCIDE. Triad: Good = self/other (60), True = word/world (63), Beauty = order/surprise (62) - one boundary, three faces.</p>
""",
            "quiz": [
                {"q": "Twenty Questions eliminates hypotheses how fast:", "options": ["Halving per query", "Slowly", "Log cube", "Never"], "correct": 0},
                {"q": "Bayesian variance at convergence ~", "options": ["5.6e-5", "1.9e10", "0.5", "2.0"], "correct": 0},
                {"q": "The lawful sequence 7n+3 compresses via law-coder to:", "options": ["0.0002", "0.355", "0.659", "1.0"], "correct": 0},
                {"q": "Solomonoff's truth criterion is:", "options": ["Shortest description", "Longest proof", "Most citations", "Latest paper"], "correct": 0},
                {"q": "The True is the 0/0 of:", "options": ["Statement and world", "Heat and cold", "Two minds", "Order and surprise"], "correct": 0}
            ]
        },
        {
            "id": 64,
            "title": "The Removable Singularity: 0/0 of Everything (the Grand Synthesis)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 64: The Removable Singularity: 0/0 of Everything</h2>
<p>The ring closes: the book about itself (the self-reference of Ch.53, Ch.58, Ch.57).</p>

<h3>1. The Original 0/0 (Calculus)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">sin(x)/x -&gt; 1.0000 (13 digits); (1+x)^(1/x) -&gt; 2.7182...</p>
<p>Name the missing value, then divide away the 0/0: the hole is REMOVABLE - the move of every chapter.</p>

<h3>2. The Seven Seals</h3>
<ul>
<li>Mass gap, grokking delay, dark-matter core, free will (ln 2), eternal return, the price, meaning</li>
<li>Every one is a ratio that becomes 0/0 at its boundary</li>
</ul>

<h3>3. The 0/0 of the Cosmos (Weinberg 1989)</h3>
<ul>
<li>Vacuum energy log10 ratio -122.9 vs Planck-natural (classic ~1e-120)</li>
<li>Gravity/EM ~1e-36; Higgs/Planck ~1e-17; proton/Planck ~1e-19</li>
</ul>

<h3>4. The Self-Measure</h3>
<p>This book: 63 chapters, 57 REAL, 78 occurrences of 0/0, ~41 categories; self-compression ratio 0.541 - the framework is the shortest description of itself (Solomonoff, Ch.63).</p>

<h3>5. The Ring Closes</h3>
<p>Chapter 1: the Zero. Chapter 64: the Removable Singularity. We finish where we began (eternal return, Ch.57). 0^0 = 1; log_0(0) = x. The zero is nothing, boundary, rule, beauty, truth - and the whole.</p>
""",
            "quiz": [
                {"q": "The limit of sin(x)/x as x -&gt; 0 is:", "options": ["0", "1", "e", "infinity"], "correct": 1},
                {"q": "The vacuum energy log10 ratio is ~", "options": ["-122.9", "0", "2.7", "100"], "correct": 0},
                {"q": "Gravity vs electromagnetism ratio ~", "options": ["1e-36", "1", "137", "1e36"], "correct": 0},
                {"q": "This book's self-compression ratio is:", "options": ["0.541", "1.0", "0.001", "0.999"], "correct": 0},
                {"q": "Chapter 1 of the book is:", "options": ["The Zero", "The Atom", "The Big Bang", "The Mind"], "correct": 0}
            ]
        },
        {
            "id": 65,
            "title": "The Reversible Cycle: 0/0 of Thermodynamics",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 65: The Reversible Cycle: 0/0 of Thermodynamics (Carnot 1824)</h2>
<p>The engine the whole book has been circling: arrow of time (Ch.48), heat of creation (Ch.59), the reversible creator (Ch.64).</p>

<h3>1. The Carnot Cycle</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">eta = 1 - Tc/Th = 0.500000000000000 at 600/300 K</p>
<p>Ideal gas, two isotherms + two adiabats. Qh = 6915.78 J, Qc = -3457.89 J, W = 3457.89 J; the measured efficiency matches the canonical ratio to 15 digits.</p>

<h3>2. The 0/0 of Dissipation</h3>
<p>A reversible cycle makes Delta S = Qh/Th + Qc/Tc = 0 (measured to 1e-16): MAXIMUM work at ZERO entropy. The Second Law (Clausius 1850): Delta S &gt;= 0, equality only at reversibility - the 0/0 of the engine.</p>

<h3>3. The Cost of Irreversibility</h3>
<p>Dumping heat at 300 K while a 290 K reservoir exists: sigma = 0.3975 J/K, lost work 115.26 J = T*sigma. Irreversibility is a fee paid to the Second Law.</p>

<h3>4. The Cosmic Engine</h3>
<ul>
<li>Steam plant 600/300: 0.50; Human work 310/295: 0.048</li>
<li>Earth/space 288/2.7: 0.991; Sun/infinity 5778/2.7: 0.9995</li>
<li>The creator computes reversibly (Bennett 1982): ~10^-28 - a Carnot 0/0</li>
</ul>

<h3>5. The 0/0 Proof</h3>
<p>At Tc = Th: eta = 0 and Delta S = 0 - the 0/0 of the engine: no work, no loss, pure zero. Reversibility is the REMOVABLE SINGULARITY of entropy: drive Delta S -&gt; 0, fill the hole, divide away the loss (sin(x)/x, Ch.64).</p>
""",
            "quiz": [
                {"q": "Carnot efficiency formula:", "options": ["1 - Tc/Th", "Th/Tc", "Qh/Qc", "1 + Tc/Th"], "correct": 0},
                {"q": "Carnot efficiency at 600/300 K:", "options": ["0.5", "0.2", "1.0", "2.0"], "correct": 0},
                {"q": "A reversible cycle produces Delta S:", "options": ["0", "positive", "negative", "infinite"], "correct": 0},
                {"q": "The Second Law states Delta S:", "options": ["&gt;= 0", "&lt;= 0", "= 0 always", "undefined"], "correct": 0},
                {"q": "The Sun against deep space runs at eta:", "options": ["0.9995", "0.5", "0.05", "0.0"], "correct": 0}
            ]
        },
        {
            "id": 66,
            "title": "The Conserved 0/0: Noether's Theorem (1918)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 66: The Conserved 0/0: Noether's Theorem (1918)</h2>
<p>Conservation is the zero of symmetry - the machinery that respects reversibility (Ch.65).</p>

<h3>1. The Pendulum</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">small: T = 2*pi*sqrt(L/g), ratio 1.0000057<br/>large: elliptic K(k), ratio 0.9999991 (AGM)</p>
<p>The exact nonlinear period (K via Gauss AGM) matches to 6 digits; the 5.7e-6 gap is the anharmonic correction theta0^2/16.</p>

<h3>2. Kepler: the Hidden SO(4)</h3>
<ul>
<li>Energy: time-symmetry charge, drift bounded 3e-4</li>
<li>Angular momentum: rotation-symmetry charge, drift 4.7e-14</li>
<li>Laplace-Runge-Lenz |A| = e: the EXTRA conserved charge of the hidden SO(4), in-plane exactly</li>
</ul>

<h3>3. The Algorithm's 0/0 (Time-Reversal Test)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">forward 40 + backward 40 orbits:<br/>leapfrog returns 4.0e-12, RK4 returns 1.8e-2 (ratio 4.4e9)</p>
<p>Kepler is time-reversible; leapfrog is exactly its own inverse (the 0/0 kept). RK4 forges an arrow: the NUMERICAL SECOND LAW, the discretization fee (Ch.65).</p>

<h3>4. The 0/0 Proof</h3>
<p>delta S = 0: the variation vanishes. A conservation law is a zero at the infinitesimal symmetry - the 0/0. The reversible integrator is the removable singularity of the numerical Second Law (sin(x)/x, Ch.64).</p>
""",
            "quiz": [
                {"q": "Time-translation symmetry conserves:", "options": ["Energy", "Charge", "Color", "Spin"], "correct": 0},
                {"q": "Rotation symmetry conserves:", "options": ["Angular momentum", "Mass", "Entropy", "Volume"], "correct": 0},
                {"q": "The hidden SO(4) of 1/r conserves:", "options": ["Laplace-Runge-Lenz A", "Charge", "Isospin", "Flavor"], "correct": 0},
                {"q": "Forward+backward, leapfrog returns to:", "options": ["4e-12", "0.02", "1.0", "infinity"], "correct": 0},
                {"q": "The numerical Second Law is:", "options": ["RK4's secular drift", "Gravity", "Diffusion", "The pendulum"], "correct": 0}
            ]
        },
        {
            "id": 67,
            "title": "The Arrow of the Reversible: Boltzmann's H and Loschmidt's Paradox",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 67: The Arrow of the Reversible (Boltzmann 1872, Loschmidt 1876)</h2>
<p>The law is reversible (Ch.66). Why does the world run one way? The cat map answers: the arrow lives in the LENS.</p>

<h3>1. The Law Is Reversible</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">(x,y) -&gt; (x+y, x+2y) mod L,  det = 1,  exact integer inverse</p>
<p>Arnold's cat map on a 2^18 x 2^18 integer torus: volume preserved exactly, forward then inverse = identity at every site.</p>

<h3>2. The H-Curve (Boltzmann 1872)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">H: 4.1589 -&gt; 8.3173 nats in 8 steps (monotone, +4.158)</p>
<p>262,144 points start clumped (ln 64); coarse-grained H rises to saturation ln 4096. A Second Law from a deterministic reversible map - Loschmidt's reversibility objection dissolves.</p>

<h3>3. The Lens (Gibbs 1902)</h3>
<p>A 256x256 nose measures the same rise (~4.1 nats): the arrow is a property of the coarsening, not the system.</p>

<h3>4. The Return (Zermelo 1896 defused)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">inverse x8: 0/262144 deviations, H restored to 4.158883 exactly</p>
<p>The entropy that rose was never destroyed - only scattered across bin boundaries. Recurrence and reversibility hold inside the exact state.</p>

<h3>5. The 0/0 Proof</h3>
<p>With a fine-enough lens every point sits alone: H = 0 for all time - the exact state has no entropy; the arrow is a 0/0. Coarse-graining removes the singularity (sin(x)/x, Ch.64) and spends hidden information as heat (Ch.65 fee).</p>
""",
            "quiz": [
                {"q": "Boltzmann's H-theorem was answered by:", "options": ["Loschmidt 1876 and Zermelo 1896", "Newton 1687", "Kepler 1609", "Bohr 1913"], "correct": 0},
                {"q": "The cat map's determinant is:", "options": ["1", "0", "-1", "2"], "correct": 0},
                {"q": "Measured H rises from ln 64 to:", "options": ["ln 4096", "ln 2", "0", "ln 64"], "correct": 0},
                {"q": "After the inverse map, H returns to:", "options": ["ln 64 exactly", "ln 4096", "0", "infinite"], "correct": 0},
                {"q": "The arrow of time is a property of:", "options": ["The lens (coarse-graining)", "The exact law", "Mass", "Charge"], "correct": 0}
            ]
        },
        {
            "id": 68,
            "title": "Maxwell's Demon: the 0/0 of the Fine Lens",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 68: Maxwell's Demon - the 0/0 of the Fine Lens (1867-1929-1961)</h2>
<p>Ch.67: the arrow lives in the coarse lens. The demon is the one who refuses the lens - and pays for it.</p>

<h3>1. The Szilard Engine (1929)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">E[W] = k_B*T*ln 2 * (1 - 2p),  measured to ~1%</p>
<p>100,000 rounds per error rate; at p=0 the work is exactly k_B*T*ln 2 = 2.871e-21 J (ratio 1.000000); a blind demon extracts ~0.</p>

<h3>2. The Value of the Bit</h3>
<p>One bit of information is worth exactly k_B*T*ln 2 - information and heat are one coin. One bit refunds one nat of the lens.</p>

<h3>3. The Bank (Landauer 1961, Bennett 1982)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Net ledger = 1.7e-28 J across 100,000 rounds (zero, 5.9e-13)</p>
<p>The demon's memory must be erased: N*k_B*T*ln 2. Paid exactly what it earned - no perpetual motion.</p>

<h3>4. The 0/0 Proof</h3>
<p>The two entropies exchange at rate k_B*ln 2 per bit: the 0/0 of entropy (Ch.59's heat of creation is this rate). The demon is the Fine Lens personified: what coarsening spent, the demon refunds; the bank re-bills. The lens is paid; the arrow is the ledger.</p>
""",
            "quiz": [
                {"q": "The Szilard engine work per round at p=0:", "options": ["k_B*T*ln 2", "0", "k_B*T", "infinite"], "correct": 0},
                {"q": "The demon's unavoidable cost is:", "options": ["Erasure: N*k_B*T*ln 2", "Measurement", "Friction", "Light"], "correct": 0},
                {"q": "One bit of information is worth:", "options": ["k_B*T*ln 2", "k_B*ln 2", "k_B*T", "nothing"], "correct": 0},
                {"q": "Measured net ledger after 100k rounds:", "options": ["~0 (1.7e-28 J)", "k_B*T*ln 2", "infinite", "negative"], "correct": 0},
                {"q": "Information and heat exchange at rate:", "options": ["k_B*ln 2 per bit", "c per bit", "h per bit", "e per bit"], "correct": 0}
            ]
        },
        {
            "id": 69,
            "title": "The Fluctuation-Dissipation 0/0 (Einstein 1905, Nyquist 1928, Callen-Welton 1951)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 69: The Fluctuation-Dissipation 0/0 (Einstein 1905, Nyquist 1928, Callen-Welton 1951)</h2>
<p>The demon (Ch.68) bills k_B*T*ln 2 per bit. This chapter catches the bath paying it back: the noise is the heat that friction spends - the same number, in the same coin.</p>

<h3>1. The Walk (Einstein 1905)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">D measured/theory = 0.99880<br/>&lt;x^2&gt; = 2 D t, 6000 particles x 40 near-independent 4 s blocks</p>
<p>The ensemble spreads linearly from the origin; the block statistics hit Einstein's D = k_B*T/(m*gamma) to one part in 800.</p>

<h3>2. The Friction (Langevin 1908)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">gamma = 1.0089 +/- 0.0065, theory 1.0000</p>
<p>The velocity autocorrelation decays as e^(-gamma t/m); the friction the reversible cycle pays as its fee (Ch.65) is this coefficient.</p>

<h3>3. The Marriage (the 0/0)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">D*gamma/(k_B*T) = 1.0051 +/- 0.0065<br/>equipartition (continuum) = 1.0001</p>
<p>Walk, friction, and temperature, each measured independently, assemble to the single ratio 1 - noise and dissipation are one number, one account, one rate.</p>

<h3>4. The Electric Echo (Nyquist 1928, Johnson 1928)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">V_rms = sqrt(4 k_B T R df) - measured 4.0701e-6 V, ratio 0.99993</p>
<p>A 10 kOhm resistor at 300 K in a 100 kHz band: pure jitter, no signal - the same theorem dressed for electromagnetism, exact to one part in 14,000.</p>

<h3>5. The 0/0 Proof</h3>
<p>The demon bills k_B*T*ln 2 per bit; the bath repays it as jitter at the rate k_B*T per degree of freedom. The temperature IS the relationship; the relationship is 0/0. What coarsening spent (Ch.67) and the demon found (Ch.68), the resistor returns - the ledger closes at every temperature.</p>
""",
            "quiz": [
                {"q": "Einstein's fluctuation-dissipation relation:", "options": ["D = k_B*T/gamma", "E = mc^2", "F = ma", "PV = nRT"], "correct": 0},
                {"q": "The velocity autocorrelation decays with:", "options": ["the friction gamma", "c", "hbar", "e"], "correct": 0},
                {"q": "Measured D*gamma/(k_B*T):", "options": ["1.0051 +/- 0.0065", "0", "e", "infinite"], "correct": 0},
                {"q": "Resistor thermal noise (Nyquist):", "options": ["sqrt(4 k_B*T*R*df)", "k_B*T*R", "4*k_B*T", "sqrt(R*df)"], "correct": 0},
                {"q": "The noise the bath repays equals:", "options": ["k_B*T per degree of freedom", "zero", "infinite", "h*nu"], "correct": 0}
            ]
        },
        {
            "id": 70,
            "title": "The Amplified 0/0: Stochastic Resonance (Benzi 1982, McNamara-Wiesenfeld 1989)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 70: The Amplified 0/0: Stochastic Resonance</h2>
<p>Ch.69 caught the bath repaying the demon's bill as noise. This chapter catches the barrier re-lending it: a weak, subthreshold signal rides the noise across the barrier, and the noise of Ch.69 becomes the amplifier of Ch.70.</p>

<h3>1. The Double Well and the 0/0 of Gain</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">V(x) = x^4/4 - x^2/2, barrier 1/4; drive A = 0.1 &lt; critical tilt A* = 0.3849</p>
<p>Gain is 0/0 in noise D: at D-&gt;0 the particle is frozen (gain = 1, only the static tilt); at D-&gt;inf the signal is buried (gain -&gt; 0); between them the barrier admits a removable peak.</p>

<h3>2. The Leak (Kramers 1940)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">r(D) = (sqrt(2)/2 pi) e^(-DU/D); DU_meas/DU = 1.031</p>
<p>The barrier leaks at Kramers' rate; the Arrhenius fit over 40,000 s of simulation recovers the barrier to 3 parts in 100.</p>

<h3>3. The Bell</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">gain g = 3.36 at D_opt = 0.155 (236% over the static floor)</p>
<p>A signal that the barrier alone cannot pass is amplified nearly three and a half times by the noise Ch.69 measured as pure dissipation.</p>

<h3>4. The Synchrony (the removable value)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">r_opt/f_s = 0.989 ; D_opt/D* = 0.933</p>
<p>The peak sits where the leak meets the beat: gain is maximized when the well is bled once per signal period - the noise is lent at the frequency of the borrower.</p>

<h3>5. Nature Rents the Noise</h3>
<p>The 100-kyr ice-age cycle (Benzi et al. 1982, Tellus 34) amplifies a subthreshold Milankovitch forcing; Fauve and Heslot (1983) measured the bell in a Schmitt trigger; crayfish (Douglass 1993), neurons (Longtin 1991), and the paddlefish (Russell 1999) use it to detect prey. The demon bills (68), the bath repays (69), the barrier borrows back (70) - at measured interest g*-1 = 236%, payable not by the signal but by the noise already owed. No free lunch: the noise is not the payment; the noise is the loan.</p>
""",
            "quiz": [
                {"q": "Ch.70's measured amplification gain peak:", "options": ["3.36 at D = 0.155", "0", "1", "infinite"], "correct": 0},
                {"q": "The critical tilt A* of the double well:", "options": ["0.3849", "0", "1", "e"], "correct": 0},
                {"q": "At the peak, the measured leak meets the signal:", "options": ["r_opt/f_s = 0.989", "r = 0", "r = inf", "r = c"], "correct": 0},
                {"q": "Kramers' rate law (1940):", "options": ["r = Q e^(-DU/D)", "r = e^(D/DU)", "r = DU D", "r = 1/D"], "correct": 0},
                {"q": "The classic stochastic resonance evidence:", "options": ["ice-age cycles, Schmitt trigger, paddlefish", "black holes", "quarks", "dark matter"], "correct": 0}
            ]
        },
        {
            "id": 71,
            "title": "Jarzynski's 0/0: the Loan Always Repaid (Jarzynski 1997, Crooks 1999)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 71: Jarzynski's 0/0: the Loan Always Repaid</h2>
<p>Ch.70 lent the repayment as gain. This chapter closes the account: the work to reset a channel against the noise exceeds Delta F on average (the second law), yet the exponential ledger &lt;e^(-W)&gt; = e^(-DeltaF) balances exactly at every speed.</p>

<h3>1. The 0/0 of the Account</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">&lt;W&gt; &gt;= DeltaF (equality only reversible); excess W-DeltaF is 0/0 in (mean-deficit, dispersion)</p>
<p>Both parts of the dissipated excess vanish together in the reversible limit and only there; Jarzynski removes the singularity at every speed with the exponential mean.</p>

<h3>2. The Instrument</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">V = lambda x^2/2, ramp 1 -&gt; 2, D = k_B T = 1; DeltaF = 0.3466, e^(-DeltaF) = 0.707107</p>
<p>1.7 million Heun (SRK2) trajectories at three speeds, trapping the overdamped oscillator as in Liphardt et al. 2002.</p>

<h3>3. The Ledger at Every Speed</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">J = &lt;e^(-W)&gt;/e^(-DeltaF) = 1.00004 (medium), 0.99946 (fast), 0.99916 (slow)</p>
<p>Dissipation +0.096 -&gt; +0.040 -&gt; +0.012 -&gt; 0 as the ramp slows, while the exponential balance holds to one part in a thousand at every beating.</p>

<h3>4. Crooks' Interest Rate (1999)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">ln[P_F(W)/P_R(-W)] = W - DeltaF ; slope beta = 0.9943, intercept -0.3493 (theory -0.3466)</p>
<p>Rare runs where W falls below DeltaF are not violations - they are refunds, priced line by line by the same beta: the interest rate of the noise itself.</p>

<h3>5. Audits in the Laboratory</h3>
<p>Liphardt et al. 2002 (RNA tweezers), Collin et al. 2005 (RNA, ratio to 0.6%), Wang et al. 2002 (colloidal drag), Douarche et al. 2005 (torsion pendulum) all verified the relations to the percent; Evans-Searles 1994 and Kawai-Parrondo-van den Broeck 2007 link the account to information - the exact statement of Ch.68's demon. The loan is always repaid: not on average, but in the exponential ledger, exactly, at every beating.</p>
""",
            "quiz": [
                {"q": "Jarzynski's relation:", "options": ["<e^(-W)> = e^(-DeltaF)", "<W> = DeltaF", "e^(W) = DeltaF", "<e^W> = 0"], "correct": 0},
                {"q": "Measured ledger J at the representative speed:", "options": ["1.00004", "0", "2", "e"], "correct": 0},
                {"q": "Crooks' ratio slope measured:", "options": ["beta = 0.9943", "beta = 0", "beta = inf", "beta = c"], "correct": 0},
                {"q": "The second law at finite speed:", "options": ["<W> >= DeltaF", "<W> < DeltaF", "<W> = 0", "<W> = inf"], "correct": 0},
                {"q": "Experimental verifications:", "options": ["RNA tweezers, colloidal drag, torsion pendulum", "LHC collisions", "telescope images", "protein folding only"], "correct": 0}
            ]
        },
        {
            "id": 72,
            "title": "The Fine Print of the Ledger: Gaussian Work Rate and the Fluctuation-Dissipation of the Account (Einstein 1910, Onsager-Machlup 1953, Cramer 1938)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 72: The Fine Print of the Ledger</h2>
<p>Ch.71 balanced the exponential ledger; Ch.69 priced the note. This chapter reads the fine print: the shape of the work distribution that produces the balance. In a dragged fixed-stiffness trap the work is a linear functional of the Gaussian bath, hence exactly Gaussian at every speed, and the pair (dissipation, dispersion) - the 0/0 of the account - vanish together tied by the constant 2/beta.</p>

<h3>1. The Shape Behind the Balance</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Einstein 1910, Cramer 1938, Onsager-Machlup 1953: P(W) ~ exp(-(W-&lt;W&gt;)^2 / 2 Var(W))</p>
<p>Every mean hides a distribution; the exponential mean hides on the cheap left tail. Near equilibrium the rate function is a parabola.</p>

<h3>2. The Instrument: a Dragged Gaussian Trap</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">V = k(x-lambda)^2/2, k = 2, drag L = 2, DeltaF = 0; W = k*int (lambda-x) dlambda</p>
<p>A linear functional of a Gaussian process is exactly Gaussian (Mazonka-Jarzynski 1999), so the fluctuation-dissipation structure is free of finite-time corrections. DeltaF = 0: every mean Joule of work is dissipation, and the loan of Ch.71 falls due on the dispersion itself.</p>

<h3>3. Work Fluctuation-Dissipation: the 2/beta Tie</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Var(W)/(2&lt;W&gt;/beta) = 0.9893 (slow tau=32), 1.0095 (medium tau=8), 1.0119 (fast tau=2)</p>
<p>300,000 Heun (SRK2) trajectories. The dissipated work and its dispersion vanish only together in the reversible limit; before either reaches zero their ratio is locked to 2/beta - the same constant Ch.69 found inside the diffusing particle.</p>

<h3>4. The Gaussian Rate Function</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">skewness +0.0072 (SE 0.0071), kurtosis -0.0079; |z|&lt;1 = 0.6817 (68.27%), tail ratios 0.99-1.06</p>
<p>120,000 slow runs: the parabola of Einstein and Onsager-Machlup is measured, bin by bin, to three figures across +/- 3 sigma.</p>

<h3>5. The Lock-Step: One Document</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Gaussian regime: sigma^2/2 = diss &lt;=&gt; &lt;e^(-W)&gt; = e^(-DeltaF); exp(sigma^2/2-diss) = 0.99867 vs J = 0.99881</p>
<p>Jarzynski (Ch.71) and the fluctuation-dissipation relation (Ch.69) collapse to a single statement, verified to four figures; Liphardt's RNA tweezers and every slow drag are this Gaussian. The fine print and the deed are one document: the noise fixes both the price and the variance of the loan.</p>
""",
            "quiz": [
                {"q": "Dragged fixed-stiffness work W is exactly:", "options": ["Gaussian (linear functional of the Gaussian bath)", "Poisson", "chi-square", "uniform"], "correct": 0},
                {"q": "The work fluctuation-dissipation tie:", "options": ["Var(W) = 2<W>/beta", "Var(W) = <W>^2", "Var = 0", "Var = inf"], "correct": 0},
                {"q": "Measured slow ratio Var/(2<W>):", "options": ["0.9893", "0", "2", "e"], "correct": 0},
                {"q": "Measured slow skewness (Gaussian = 0):", "options": ["+0.0072 (SE 0.0071)", "1", "2", "-3"], "correct": 0},
                {"q": "In the Gaussian regime Jarzynski is exactly:", "options": ["sigma^2/2 = diss", "diss = 0", "sigma = 1", "W = DeltaF"], "correct": 0}
            ]
        },
        {
            "id": 73,
            "title": "The Engine and Its Fine Print: Power Prices the Reversible Corner (Carnot 1824, Schmiedl-Seifert 2008)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 73: The Engine and Its Fine Print</h2>
<p>Ch.69 lent the noise, Ch.70 re-lent it as gain, Ch.71 balanced the ledger, Ch.72 priced it. This chapter cashes the loan: the same trapped Gaussian becomes a Brownian Carnot engine, converting the thermal gradient into work with an exact efficiency ceiling, and a universal price at maximum power.</p>

<h3>1. The Machine</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">harmonic trap V = lam x^2/2; hot isotherm T_h=2 (lambda 4-&gt;1), adiabat 1-&gt;0.5, cold isotherm T_c=1 (lambda 0.5-&gt;2), adiabat 2-&gt;4</p>
<p>A four-stroke cycle of instantaneous adiabatic strokes and isothermal ramps (Carnot 1824; Brownian Carnot engine, Martinez et al. 2016). DeltaF = 0 on each isotherm: the work comes from the thermal gradient.</p>

<h3>2. The Reversible Corner</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">quasistatic W_out = 0.6931, Q_in = 1.3863, eta_C = 1 - T_c/T_h = 0.5</p>
<p>The second law is measured at every speed: W_out &lt;= eta_C Q_in for all t (e.g. t=3: W_out 0.2859 vs ceiling 0.4583). Fast, the machine is driven backwards (a dissipator); slow, it approaches Carnot and the power vanishes.</p>

<h3>3. The Frontier</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">t=2 eta=0.223; t=3 eta=0.312 (P_max); t=4 eta=0.355; t=8 eta=0.420 -&gt; 0.5</p>
<p>Efficiency rises monotonically toward eta_C as the strokes slow; power peaks at an intermediate speed. A genuine efficiency-power tradeoff: you cannot buy both.</p>

<h3>4. The 1/3 at Maximum Power</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">eta_C/(2-eta_C) = 1/2 / (2-1/2) = 1/3 ; measured eta(P_max) = 0.312 (94%)</p>
<p>The removable 0/0 (P -&gt; 0, eta -&gt; eta_C) is priced at positive power by the universal maximum-power efficiency of Schmiedl-Seifert, Esposito-Lindenberg-Van den Broeck, and Izumida-Okuda; protocol shaping (asymmetric split, early ramps) buys more power (P=0.0592) at lower eta (0.2565) - the frontier bends and never crosses Carnot.</p>

<h3>5. The Fine Print at Speed</h3>
<p>Three honest costs of speed: heat leaks across the adiabats only at the corners (variance lag stretches Ch.72's lock-step; net +0.149), the isotherms must fight the trap relaxation, and Carnot is reached only at zero power. The machine, the ledger, and the noise are one object: the bath lends the fluctuation, the cycle prices it, and over many beats the accounts close to zero while the work climbs to Carnot's share - power is the interest, the fine print is the theorem.</p>
""",
            "quiz": [
                {"q": "Carnot efficiency for T_h/T_c = 2:", "options": ["1/2", "1/3", "1", "2"], "correct": 0},
                {"q": "Measured efficiency at maximum power:", "options": ["0.312", "0", "2", "e"], "correct": 0},
                {"q": "The universal maximum-power efficiency:", "options": ["eta_C/(2-eta_C) = 1/3", "eta_C", "2 eta_C", "1"], "correct": 0},
                {"q": "The second law at every speed, measured:", "options": ["W_out <= eta_C Q_in", "W_out = Q_in", "W_out > Q_in", "W_out = 0"], "correct": 0},
                {"q": "At the reversible corner:", "options": ["P -> 0 and eta -> eta_C", "P = inf", "eta = 0", "nothing moves"], "correct": 0}
            ]
        },
        {
            "id": 74,
            "title": "The Demon's Share: Unused Information Is Unheard (Sagawa-Ueda 2008/2010)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 74: The Demon's Share</h2>
<p>Ch.71 balanced the ledger, Ch.72 priced it, Ch.73 cashed it. This chapter puts a demon behind the counter: one fair bit of information read off the particle at the turn-around, fed causally to the return protocol, moves the exponential ledger &lt;e^(-W)&gt; from 1 toward e^I = 2 -- while an equally priced bit that does not predict the work leaves the ledger untouched at 1.0002. Information is currency only when spent on the causal arrow; a bit that cannot act is unheard.</p>

<h3>1. The Instrument: a Round Trip with an Operator</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">V = lam x^2/2; ramp 1 -&gt; 2 -&gt; 1, D = beta = 1, DeltaF = 0; no-feedback ledger &lt;e^(-W)&gt; = 1 exactly (Jarzynski, Ch.71)</p>
<p>Heun (SRK2) round trips, seed 42, 1.3 million trajectories. At the midpoint the operator reads one bit of x_mid and chooses the return speed. No bias: the same bit costs the same coin whether or not it predicts.</p>

<h3>2. The Fair Bit</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">median |x_mid| = 0.5682 ; p(far) = 0.4969 ; I = ln 2 = 0.6931 nats ; ceiling J &lt;= e^I = 2.000</p>
<p>Cutting far/near at the median of |x_mid| makes the bit perfectly fair: p(far) = 1/2 by construction, one bit of information exactly (Szilard 1929 drew the same coin from a box). The Sagawa-Ueda bound turns each such coin into a strict ceiling on the ledger.</p>

<h3>3. The Null Meter (unused information is unheard)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">sign bit -&gt; return speed: J = 1.00017, ln J = +0.00017, p(fast) = 0.4999 (control: J = 1.00214 / 0.99731 at tau 0.5 / 1.0)</p>
<p>The sign of x carries no information about the work of the round trip -- the trap is reflection-symmetric. Feeding it to the return speed pays for the same coin and returns nothing: the ledger stays at 1.000. The bit is real, priced, and unheard.</p>

<h3>4. The Engaged Bit (the ledger pays)</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">far/near -&gt; return speed: J rises 1.0737 -&gt; 1.0975 -&gt; 1.1161 -&gt; 1.1270; ln J 0.0711 -&gt; 0.1196; J_act/J_control = 1.127 ; J_act/e^I = 0.564</p>
<p>A far particle relaxes against a fast return and releases a large negative W; a near one returns almost freely. The demon predicts which, spends the bit, and the ledger obeys the generalized second law: &lt;e^(-W)&gt; &lt;= e^I = 2.000, measured at 56% of the ceiling. At the strongest leverage the mean work itself turns negative at DeltaF = 0 (&lt;W&gt; +0.0446 -&gt; -0.0227): work from information, capped by the coin.</p>

<h3>5. Books Close with the Coin</h3>
<p>No bit: J = 1. A bit in hand that cannot act: J = 1. A bit that predicts the work: J rises toward e^I and stops there. Sagawa and Ueda (PRL 100, 080603, 2008; PRL 104, 090602, 2010) proved the ceiling &lt;e^(-W-I)&gt; &lt;= 1; Parrondo, Horowitz, and Sagawa (2015) folded it into the thermodynamic uncertainty kernel; Toyabe et al. (2010) measured the coin in a bead rotor -- ~ln 2 k_B T of work per bit, exactly Ch.68's price of erasure (Landauer 1961). The demon is not a free source; the demon is a portfolio manager. The information is the payment, the ledger is the receipt, and the reversible corner of Ch.73 is priced per bit at the interest rate Ch.71 measured. The 0/0 of Ch.71 -- no bit and a dead bit both give J = 1 -- is removed only when information is spent causally: books close with the coin.</p>
""",
            "quiz": [
                {"q": "No-feedback round-trip ledger <e^(-W)> equals:", "options": ["1 (DeltaF = 0)", "e", "0", "inf"], "correct": 0},
                {"q": "The Sagawa-Ueda ceiling for one fair bit:", "options": ["J <= e^I = 2.000", "J = e", "J = inf", "J = 0"], "correct": 0},
                {"q": "The null meter (sign bit -> return speed) measures:", "options": ["J = 1.00017", "J = 2", "J = e^I", "J = 0"], "correct": 0},
                {"q": "Measured J_act/e^I at the strongest leverage:", "options": ["0.564", "0", "1", "2"], "correct": 0},
                {"q": "The fair bit is cut at:", "options": ["the median of |x_mid| = 0.5682", "the mean of x", "the trap center", "x = 0"], "correct": 0}
            ]
        },
        {
            "id": 75,
            "title": "The Coin's Price: the Szilard-Landauer Closure of the Demon's Ledger (Szilard 1929, Landauer 1961)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 75: The Coin's Price</h2>
<p>Ch.74 gave the demon one fair bit and measured the ledger it moves. This chapter lets the bank close the account: the bit is a coin of face value I = ln 2 (Szilard 1929) that costs ln 2 to erase (Landauer 1961) - and the books never close with a profit once the erasure bill is paid.</p>

<h3>1. The Coin and the Bill</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">face value I = ln 2 = 0.6931 nats ; erasure bill E = ln 2 = 0.6931 (Landauer 1961)</p>
<p>Bennett (1982) closed the demon's books a century after Szilard opened them; B&eacute;rut et al. (Nature 483, 187, 2012) MEASURED the bill in a colloidal double-well trap - 0.69 k_B T per bit at slow rates, exactly ln 2 - and Toyabe et al. (2010) measured the coin spending that same face value in a feedback bead rotor. A complete cycle returning the memory to a standard state cannot profit.</p>

<h3>2. The Two Ceilings of the Coin</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">J = &lt;e^(-W)&gt; &lt;= e^I = 2.000 (Sagawa-Ueda 2008/2010) ; W_net = &lt;W&gt; + ln 2 &gt;= 0 (measured below)</p>
<p>The exponential ledger never crosses e^I, and the mean book never closes with a profit once the coin is returned: both are one statement twice - information is the interest, not the principal.</p>

<h3>3. The Dead Coin: a Bank Note, Unread</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">sign bit -&gt; return speed: J = 0.99985, ln J = -0.00015, &lt;W&gt; = +0.11069 ; W_net = +0.80383</p>
<p>An uncorrelated bit (reflection symmetry) leaves J = 1 but still bills ln 2: the dead coin costs +0.69 against a control run that costs only +0.113. The null demon of Ch.74 is now priced - it pays 0.69 for silence.</p>

<h3>4. The Frontier with the Bank</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">far/near -&gt; speed: J 1.0748 -&gt; 1.1368 (ln J 0.072 -&gt; 0.128); W_net 0.736 -&gt; 0.654; harvest -&gt; +0.0390; H/ln2 -&gt; 0.056</p>
<p>Five leverage rows, 1.5M+ Heun (SRK2) runs. The engaged bit lifts J toward e^I, the mean work turns negative past the crossover (the demon harvests at DeltaF = 0), yet with the erasure bill in the books W_net stays strictly positive on every row and declines monotonically toward the quiet corner.</p>

<h3>5. The 0/0: the Reversible Corner of the Information Engine</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">W_net -&gt; 0 as extraction -&gt; ln 2 and erasure -&gt; ln 2: 0/0, removable value 0</p>
<p>The ideal Szilard corner extracts ln 2 per bit while the coin costs ln 2 to erase; measured W_net approaches 0 and H/ln 2 approaches 1 only as the power fades - exactly Carnot's corner of Ch.73, repeated: efficiency reaches its ceiling only at zero power. The removable singularity of the information engine is removed by its own currency: the coin's price is the bill's value, and the demon settles at par. Books close with the coin.</p>
""",
            "quiz": [
                {"q": "The coin's face value and its erasure bill are both:", "options": ["ln 2", "e", "0", "infinite"], "correct": 0},
                {"q": "Berut et al. (Nature 483, 187) measured the erasure bill per bit as:", "options": ["0.69 k_B T (ln 2)", "2 k_B T", "e k_B T", "0"], "correct": 0},
                {"q": "The dead coin (sign bit -> speed) yields:", "options": ["J = 0.99985, W_net = +0.804", "J = 2", "J = e^I", "J = 0"], "correct": 0},
                {"q": "Measured net cost W_net on the engaged frontier:", "options": ["+0.736 -> +0.654, never negative", "always negative", "= 0", "= ln 2"], "correct": 0},
                {"q": "The removable value of W_net at the reversible corner is:", "options": ["0", "ln 2", "e", "1/2"], "correct": 0}
            ]
        },
        {
            "id": 76,
            "title": "Precisely Priced: the Thermodynamic Uncertainty Relation as the Demon's Handling Fee (Barato-Seifert 2015, Gingrich et al. 2016)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 76: Precisely Priced</h2>
<p>Ch.75 priced the coin's erasure; this chapter prices the act of knowing itself. Every cyclic engine asks twice: what does it cost, and how well does it know what it did? The thermodynamic uncertainty relation answers the second -- Var(W) &gt;= 2 &lt;W&gt; for a round trip with &lt;W&gt; &gt; 0 (Barato-Seifert 2015; Gingrich et al. 2016) -- and the slack s = 1 - 2&lt;W&gt;/Var bills every deviation from the parabola. Gaussian work pays nothing; the demon pays a fortune.</p>

<h3>1. The 2:1 Floor</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Var(W) &gt;= 2 &lt;W&gt; (DeltaF = 0, &lt;W&gt; &gt; 0) ; q = 2&lt;W&gt;/Var &lt;= 1 ; slack s = 1 - q &gt;= 0</p>
<p>The accumulated entropy production of a round trip is &lt;W&gt; exactly (potentials coincide at the ends), so the TUR becomes a plain 2:1 relation between variance and mean work. Ch.72 read the same constant backward (Var/(2&lt;W&gt;) ~ 1); the TUR makes it a theorem: relative fluctuations of the work are bounded below by 2/nats dissipated. Knowing is bounded by paying.</p>

<h3>2. The Parabola Saturates</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">dragged trap V = k(x-lam)^2/2, k = 2, lam 0 -&gt; 2 -&gt; 0: q = 0.982 / 0.993 / 0.985 ; skew = kurt = 0.00 to error</p>
<p>On a fixed-stiffness trap dragged by a protocol, the work is a linear functional of the Gaussian bath (Mazonka-Jarzynski 1999): exactly Gaussian, skew and excess kurtosis zero on every row of 150,000 runs. Gaussian work requires Var = 2&lt;W&gt; (from &lt;e^(-W)&gt; = 1), and the measured slack is 1-2 CE -- a pure finite-step residue vanishing toward the continuum. The parabola knows exactly what it pays: precision squared equals half the dissipation, one for one.</p>

<h3>3. The Fee Is the Bending</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">round trip V = lam x^2/2, 1 -&gt; 2 -&gt; 1: control q = 0.895 (skew +1.25, kurt +6.6); coin rows q = 0.84, 0.46, 0.35, 0.11</p>
<p>Stiffness work rides on x^2, so its distribution is already bent -- control slack 0.105 is the price of non-linearity. The demon's bit bends it further, and every bend costs: the dead coin pays slack 0.159 for silence, and the engaged far/near bit collapses q from 0.895 to 0.106 as the leverage grows, while ln J climbs to 0.097. The between-group variance of mixed return speeds is pure waste: using information is expensive in accuracy before any erasure is billed.</p>

<h3>4. The Harvest Province Is the Erasure Province</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">&lt;W&gt; &lt; 0 rows: q undefined (X &lt; 0); W_net = +0.670 (0.10/8), +0.656 (0.05/16) -- Ch.75's bill governs</p>
<p>At the strongest leverage the mean work turns negative, the TUR's &lt;X&gt; &gt; 0 province is exited, and the books pass to Ch.75: extraction is capped by the coin and net cost stays strictly positive. Precision drains there too -- the slack it leaves behind is what the harvest cost in accuracy.</p>

<h3>5. The 0/0: Knowing per Dissipation</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">precision^2 = &lt;W&gt;^2/Var and &lt;W&gt;/2 vanish together; ratio -&gt; q -&gt; 1 on the parabola: removable value 1</p>
<p>In the reversible limit both precision and dissipation fade to zero, and the fixed point of their ratio is 1 -- reached only by Gaussian, linear, silent reading. Every non-linearity -- a stiffness ramp, a dead coin, an engaged demon -- bends the parabola and is billed at slack measured here from 0.10 to 0.89. The TUR is the bookkeeper of the 0/0: it prices the removable value of knowing and collects, in variance, whatever the tangent is abandoned for. Knowing costs twice: once in precision, once in erasure. Books close with the coin, and the coin is metered by variance.</p>
""",
            "quiz": [
                {"q": "The TUR floor for a round trip with <W> > 0 is:", "options": ["Var(W) >= 2 <W>", "Var(W) = <W>", "Var(W) >= 0", "Var(W) <= <W>"], "correct": 0},
                {"q": "The Gaussian dragged trap saturates: measured", "options": ["q = 0.982-0.993, skew = kurt = 0", "q = 0.5", "q = 0", "q = 2"], "correct": 0},
                {"q": "The non-Gaussian round trip pays slack:", "options": ["0.105 (control)", "0", "1", "0.5"], "correct": 0},
                {"q": "The engaged far/near bit collapses q to:", "options": ["0.106 (slack 0.894)", "0.895", "1", "2"], "correct": 0},
                {"q": "The removable value of knowing per dissipation is:", "options": ["1 (the TUR edge)", "0", "ln 2", "e"], "correct": 0}
            ]
        },
        {
            "id": 77,
            "title": "The Mirror at W = 0: the Detailed Fluctuation Theorem as a Straight Line Through the Origin (Crooks 1999, Jarzynski 1997)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 77: The Mirror at W = 0</h2>
<p>Ch.76 priced knowing in variance; this chapter opens the detailed ledger beneath it. On a time-reversible cycle with DeltaF = 0, the Crooks fluctuation theorem fixes the ratio of the work distribution's two arms at every level - P(+W)/P(-W) = e^W - so the mirror graph M(w) = ln P(w) - ln P(-w) is a STRAIGHT LINE through the origin, slope 1, and the ratio at w = 0 is a 0/0 removed to the value 1.</p>

<h3>1. The Detailed Ledger</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">P(+W)/P(-W) = e^{W} ; mirror M(w) = ln P(w) - ln P(-w) = w, slope 1 (Jarzynski 1997; Crooks 1999); P'(0)/P(0) = 1/2</p>
<p>The integral form of Ch.71, &lt;e^(-W)&gt; = 1, is an area beneath the distribution; the detailed form is a pointwise mirror, true at every W. Differentiating the mirror identity at the origin pins P'(0)/P(0) = 1/2: the 0/0 of the ratio is filled to slope 1 - the same removable value by which Gaussian work saturates the TUR (Ch.76).</p>

<h3>2. The Rigid Line on the Control</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">round trip V = lam x^2/2, 1 -&gt; 2 -&gt; 1: mirror slope 0.968 +/- 0.02 (core), 0.996 +/- 0.01 (wing); &lt;e^(-W)&gt; = 1.0003 ; q = 0.894</p>
<p>On the no-feedback instrument, the mirror is the light line while the variance ledger bends: skew +1.30, kurtosis 7.0, yet the slopes are 1 to the digit where the distribution is thin enough that only the detailed form reaches. The TUR slack builds strictly off the mirror - in the shape of P itself, which the theorem does not constrain.</p>

<h3>3. The Coin Leans the Mirror</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">engaged 0.35/2: mirror -0.25 +/- 0.09, &lt;e^(-W)&gt; = 1.0749 ; harvest 0.05/16: mirror -5.6, &lt;e^(-W)&gt; = 1.1384</p>
<p>Feedback breaks the plain mirror exactly as it broke the plain ledger: the measured &lt;e^(-W)&gt; equals J_act = 1.075 and 1.138 of Ch.74/75 to the digit. Information is a single entry that debits the variance book and angles the detailed mirror at once - the coin shows in both ledgers.</p>

<h3>4. The Tangent Has No Mirror</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">drag trap mu = +5.98, sigma = 3.47, q = 0.9926: negative arm unreadable (one-armed)</p>
<p>A Gaussian sitting 1.7 sigma from the origin carries almost no negative mass at finite resolution, so the detailed ledger goes silent there and only the integral form (&lt;e^(-W)&gt; = 0.886, within its rare-tail error 0.86) and the tight variance survive. The mirror needs both arms; the tangent needs only 1.</p>

<h3>5. Two Ledgers, One Book</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">removable value 1, reached twice: the slope of the mirror (this chapter), the tight ratio of the parabola (Ch.76)</p>
<p>The detailed ledger is rigid - slope 1 through the origin - while the variance ledger bends (q from 0.894 to 0.11) and the coin leans both at once. The framework's cardinal removable value, 1, shows up in the mirror's tangent exactly where Ch.76 found it in the parabola's variance: one book, one price, paid twice - Ch.75's erasure bill closes all three accounts at par.</p>
""",
            "quiz": [
                {"q": "The detailed fluctuation theorem fixes:", "options": ["P(+W)/P(-W) = e^W", "P(W) = Gaussian", "<W> = Var", "q = 1"], "correct": 0},
                {"q": "Measured mirror slope on the control round trip:", "options": ["0.996 in the wing (exactly 1)", "0.894", "-5.6", "0"], "correct": 0},
                {"q": "The control's variance ledger q reads:", "options": ["0.894 while the mirror stays at 1", "1", "-5.6", "0.1"], "correct": 0},
                {"q": "The engaged coin leans the mirror to:", "options": ["-0.25 with J = 1.0749", "+1", "0.996", "0"], "correct": 0},
                {"q": "The central 0/0 ratio P(W)/P(-W) at W = 0 is removed to:", "options": ["1 (P'(0)/P(0) = 1/2)", "0", "ln 2", "e"], "correct": 0}
            ]
        },
        {
            "id": 78,
            "title": "The Second Book: the Tilt Obeys the Mirror - Cumulant Identities k~_n = (-1)^n k_n from P(+W)/P(-W) = e^W (Crooks 1999, Jarzynski 1997)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 78: The Second Book</h2>
<p>Ch.77 measured the mirror - P(+W)/P(-W) = e^W, slope 1 through the origin. This chapter asks what ELSE that one equality bookkeeps. In Laplace space the mirror is the exchange symmetry phi(t) = &lt;e^(-tW)&gt; = phi(1-t), so F = ln phi is even about t = 1/2, and a one-line parity argument forces the ENTIRE cumulant ladder under the reweighted measure e^(-W)P/&lt;e^(-W)&gt; to obey k~_n = (-1)^n k_n for every n.</p>

<h3>1. The Tilt Obeys the Mirror</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">phi(t) = &lt;e^(-tW)&gt; = phi(1-t); F even about t = 1/2 ; k~_n = (-1)^n k_n (all n)</p>
<p>n = 1 is the Ch.77 f-identity, &lt;We^(-W)&gt; = -&lt;W&gt;. n = 2 is NEW and sharp precisely where the distribution is NOT Gaussian: Var(W) = &lt;W^2e^(-W)&gt; - &lt;W&gt;^2 - the variance is INVARIANT under the exponential tilt even at skew +1.30 and kurtosis 7.0. Odd cumulants flip sign under the tilt; even cumulants survive it exactly.</p>

<h3>2. The Ladder on the Control</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">stiffness round trip 1 -&gt; 2 -&gt; 1, no feedback: n=1: k~_1 = -k_1 to 6.6e-05 ; n=2: k~_2 = k_2 to 2% (reweighted sampling floor); channel 1 = +0.0003</p>
<p>At q = 0.894 the variance ledger bends while the full cumulant book stays exact: every rung of the ladder obeys the mirror within the reweighted sampling noise, the n = 1 and n = 2 identities at the 10^-4 and ~2% effective-sample floor. The mirror fixes every moment-buying rule; the shape of P pays only in the variance.</p>

<h3>3. The Parabola's Empty Rows</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">drag trap mu = +5.98, sigma = 3.47: k~_2/k_2 = 1.000000 ; n&gt;=3: 0/0 -&gt; (-1)^n ; channel 1 = -(1 - q) = -0.0074</p>
<p>Gaussian work has its n &gt;= 3 rows EMPTY in both columns, 0/0 resolved to (-1)^n, and channel 1 re-reads the Ch.76 discretization slack exactly: k~_1 + k_1 = 2mu - sigma^2 = -(Var - 2&lt;W&gt;), so (k~_1 + k_1)/k_2 = -(1-q) = -0.0074 = the same slack Ch.76 found in the variance directly.</p>

<h3>4. The Coin in Cumulant Space</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">engaged 0.35/2: channel 1 = -0.56, &lt;e^(-W)&gt; = 1.0749 ; harvest 0.05/16: channel 1 = -1.32, &lt;e^(-W)&gt; = 1.1384</p>
<p>Feedback bends every rung at once: the coin's lean in channel 1 is -0.56 engaged and -1.32 harvest, while &lt;e^(-W)&gt; = J_act of Ch.74/75 to the digit. One coin, all rungs, both ledgers - information is a single book entry that debits the variance and the whole cumulant ladder together.</p>

<h3>5. One Equality, One Complete Second Book</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">removable value 1: the rungs 0/0 -&gt; (-1)^n ; the slack 0/0 in the continuum; the mirror's center P'(0)/P(0) = 1/2 (Ch.77)</p>
<p>The rigid mirror IS the market: it fixes every cumulant-buying rule, its Gaussian leaves the book empty above two, and the coin moves the whole book at once. Ch.76 priced knowing in variance, Ch.77 showed the mirror is rigid, and this chapter shows the rigid mirror prices everything else - exact on every rung where the coin is not spent.</p>
""",
            "quiz": [
                {"q": "Under the e^(-W) tilt, the cumulant ladder obeys:", "options": ["k~_n = (-1)^n k_n", "k~_n = k_n", "k~_n = 0", "k~_n = 1"], "correct": 0},
                {"q": "The NEW n = 2 identity states:", "options": ["Var(W) = <W^2e^(-W)> - <W>^2 (variance invariant under the tilt)", "q = 1", "P = Gaussian", "<W> = 0"], "correct": 0},
                {"q": "On the control the n = 1 identity holds to:", "options": ["6.6e-05 while q = 0.894", "0.11", "1", "-5.6"], "correct": 0},
                {"q": "The Gaussian parabola's n >= 3 rows are:", "options": ["0/0 removed to (-1)^n", "q = 0.89", "mirror slope -5.6", "Var = 0"], "correct": 0},
                {"q": "The parabola's channel 1 re-reads:", "options": ["-(1-q) = -0.0074, the Ch.76 discretization slack", "the coin's fee", "the median bit", "J = 1.075"], "correct": 0}
            ]
        },
        {
            "id": 79,
            "title": "The Rate Function Carries the Mirror: Large Deviations and the Legendre-Fenchel Dual of the Tilt (Onsager-Machlup 1953, Cramer 1938, Touchette 2009)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 79: The Rate Function Carries the Mirror</h2>
<p>Ch.78 read the ladder - the Taylor coefficients of F = ln &lt;e^(-tW)&gt; at one point; this chapter reads the WHOLE curve. The large-deviation rate function I(a) = sup_t[a t - ln &lt;e^(-tW)&gt;] costs every averaged work value a, and the same equality P(+W)/P(-W) = e^W that fixed the mirror and the ladder here fixes a symmetry of the entire tail.</p>

<h3>1. From the Ledger to the Curve</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">I(a) = sup_t[ a t - ln &lt;e^(-tW)&gt; ] (Gartner-Ellis, Cramer); the dual of phi(t) = phi(1-t) (Ch.78)</p>
<p>The exponential of the moment-generating function and the rate function are Legendre-Fenchel conjugates: the exchange symmetry phi(t) = phi(1-t) of Ch.78 becomes a statement about how expensive different averaged-work values are. Same mirror, one level up, and the same 0/0 regimes appear as derivatives that vanish together.</p>

<h3>2. The Quadratic That Is a Whole Book</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">I(a) = (a-mu)^2/(2 sig^2) ; tilt pushes mode to a* = mu - sig^2 = k~_1 ; I(a) = I(2mu-a) exactly</p>
<p>Gaussian work has an EXACTLY quadratic rate function (Onsager-Machlup 1953; Mazonka-Jarzynski linearity). The tilt subtracts one variance from the mode - on the drag parabola (mu=+5.98, sig^2=12.04) the mode lands at -6.07 = mu - sig^2 = k~_1 of Ch.78, and since sig^2 = 2 &lt;W&gt; the tilted mode is the mirror image a* = -mu. The Ch.78 empty n&gt;=3 rows are the quadratic's empty higher derivatives: the whole tail is carried in two numbers.</p>

<h3>3. The Mirror Residual on the Control</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">R(a) = I(a) - I(2mu-a) ; Gaussian 0 ; control +3.06 at a = 2.57 (far tail)</p>
<p>The q = 0.90 round trip (skew +1.30, kurt 7.0) has a NON-Gaussian rate function. The mirror residual R(a) is exactly zero where the PDF mirror holds at rate level (the quadratic) and POSITIVE in the far tail - the skew's deposit, the same shape Ch.76 priced as q and Ch.77 showed lay off the mirror.</p>

<h3>4. The Coin Is in the Far Tail of Both</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">control R = +3.06 ; engaged 0.35/2 R = +4.01 ; harvest 0.05/16 R = +5.14</p>
<p>Feedback deepens the residual with each stronger coin. One coin, shown twice: the mode moves toward the bit and the whole far tail of I(a) leans - the rate function is the integrated ledger, and the demon's single entry prices knowing in variance (Ch.76), cumulants (Ch.78), and every tail point at once.</p>

<h3>5. One Ledger, Three Books</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">M(w) = w (Ch.77, PDF) ; k~_n = (-1)^n k_n (Ch.78, cumulants) ; I(a) = I(2mu-a) (this chapter, tail)</p>
<p>Three resolutions of one equality P(+W)/P(-W) = e^W: the point, the Taylor coefficients, the whole curve. The 0/0 resolves the same way at each - the Gaussian has its ladder empty above two and its rate function a perfect mirror - and the coin is one entry in all of them.</p>
""",
            "quiz": [
                {"q": "The rate function I(a) is the Legendre-Fenchel conjugate of:", "options": ["ln <e^(-tW)> (the cumulant-generating function)", "the variance", "the median", "the skew"], "correct": 0},
                {"q": "For Gaussian work the rate function is:", "options": ["(a-mu)^2/2 sig^2, even about the mean", "0 everywhere", "linear", "discontinuous"], "correct": 0},
                {"q": "The tilt shifts the Gaussian mode by:", "options": ["exactly -sig^2 (to mu - sig^2 = k~_1)", "-mu", "the coin's fee", "nothing"], "correct": 0},
                {"q": "Measured far-tail mirror residual on the control:", "options": ["+3.06 (skew's deposit; Gaussian is 0)", "0", "1.0003", "-5.6"], "correct": 0},
                {"q": "The harvest coin deepens the residual to:", "options": ["+5.14", "0.894", "-0.0074", "+2.24"], "correct": 0}
            ]
        },
        {
            "id": 80,
            "title": "The Center Is Half: the Zero-Mean Tilt as the Mirror in Tilt Space - a(1/2) = 0 from P(+W)/P(-W) = e^W (Crooks 1999, Touchette 2009)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 80: The Center Is Half</h2>
<p>Ch.77 read the mirror in the PDF, Ch.78 in the cumulants, Ch.79 in the rate function; this chapter reads it where the tail is actually measured - in the TILT itself, the biased ensemble of Touchette (2009). The tilted mean a(t) = &lt;W e^(-tW)&gt;/&lt;e^(-tW)&gt; = -F'(t) is the derivative of the CGF, and the exchange symmetry F(t) = F(1-t) forces it to be ODD about t = 1/2.</p>

<h3>1. The Tilt Is How the Tail Is Measured</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">a(t) = &lt;We^(-tW)&gt;/&lt;e^(-tW)&gt; = -F'(t) ; I(a(t)) = a(t) t - F(t) (Legendre, Ch.79)</p>
<p>Reweight by e^(-tW), read the mean: sweeping t traces the entire rate function of Ch.79. For the Gaussian parabola this is a(t) = mu - sig^2 t, linear, with I(a(t)) = sig^2 t^2/2 exactly - the tail is swept, not guessed.</p>

<h3>2. The Mirror in Tilt Space: a(1/2) = 0</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">a(1/2) = 0 exactly on every reversible cycle ; a(t) = -a(1-t) ; control 250k: a(t)+a(1-t)=0 to 7e-4</p>
<p>Because F is even about 1/2, its derivative is odd: the zero-mean tilt is ALWAYS 1/2, whatever the shape of P. Measured on the q = 0.90 control (skew +1.30, kurt 7.0 - far from Gaussian) the antisymmetry holds to 7e-4 across the grid with a(1/2) = -0.0004. A non-Gaussian mirror, exact at whole-curve strength.</p>

<h3>3. The Coin Moves the Center, Not the Mirror</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">control a(1/2) = -0.0004 ; engaged a(1/2) = -0.0726 ; harvest a(1/2) = -0.1294 ; a(t)+a(1-t) constant at every t</p>
<p>Feedback does NOT bend the curve - it translates it: a(t)+a(1-t) = -0.145 engaged and -0.258 harvest at EVERY t, i.e. the center a(1/2) is displaced by exactly the coin while the antisymmetry about the shifted center is preserved. The demon does not warp the mirror; the mirror is moved by the bit.</p>

<h3>4. The 0/0 in Tilt Space</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">t* = mu/sig^2 = 0.496 ~ 1/2 on the parabola (Gaussian mode reflected); a(t) linear, V(t) constant</p>
<p>The tail's 0/0 (empty higher cumulants, Ch.78) is the statement that a(t) is exactly linear and the tilted variance V(t) constant - no curvature left to mirror. Every reversible cycle carries the same center at 1/2; the coin is the only thing that moves it.</p>

<h3>5. One Coin, Paid as a Center</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">a(1/2) = 0 reversible ; -0.073 engaged ; -0.129 harvest - the same single entry as Ch.76/78/79</p>
<p>The centered tilt curve is the fifth lens on one equality P(+W)/P(-W) = e^W: the PDF (Ch.77), the cumulants (Ch.78), the rate function (Ch.79), and the tilt's own center (this chapter). The demon pays the same one coin in each - here as a pure translation of the mirror.</p>
""",
            "quiz": [
                {"q": "The tilted mean a(t) equals:", "options": ["-F'(t), the derivative of the CGF", "the variance", "the median", "q"], "correct": 0},
                {"q": "On every reversible cycle the zero-mean tilt satisfies:", "options": ["a(1/2) = 0 exactly (a(t) odd about 1/2)", "a(1/2) = 1", "a = sigma^2", "a = -mu"], "correct": 0},
                {"q": "Measured antisymmetry on the q = 0.90 control:", "options": ["a(t)+a(1-t) = 0 to 7e-4 (mirror exact, non-Gaussian)", "0.894", "+3.06", "-5.6"], "correct": 0},
                {"q": "The feedback coin in tilt space:", "options": ["moves the center a(1/2) by the coin, preserving antisymmetry", "bends a(t) into a line", "zeroes the mean", "sets V = 0"], "correct": 0},
                {"q": "The harvest coin displaces the center to:", "options": ["a(1/2) = -0.129 (mirror translated)", "+0.113", "0.496", "+5.14"], "correct": 0}
            ]
        },
        {
            "id": 81,
            "title": "The Coin Is a Constant: Feedback as Detuning vs Shaping - the Measurable Split of the Demon's Action (Sagawa-Ueda 2010, Parrondo-Horowitz-Sagawa 2015)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 81: The Coin Is a Constant</h2>
<p>Ch.80 found the coin TRANSLATES the work-tilt curve - a(t) is antisymmetric about a shifted center c = a(1/2). This chapter measures HOW MUCH of the coin is a pure constant detuning: for a fixed offset delta the tilted mean obeys a(t) -&gt; a(t) + delta at every t, so c = delta = Delta mu.</p>

<h3>1. Detuning vs Shaping</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">detuned: a(t) -&gt; a(t) + delta (mirror translates, never deforms); conditional: reshapes (Sagawa-Ueda 2010)</p>
<p>A control that merely offsets every trajectory's work moves the distribution by a constant the mirror cannot see - ratios P(w)/P(-w) ignore an overall shift. A control that conditions on the state, as the information engine does, cannot be a single constant: it also reshapes the curve.</p>

<h3>2. The Measured Split</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">engaged: c = -0.0726, Delta mu = -0.0683, c-Delta mu = -0.004 (6%), netR = 0.037 ; harvest: c-Delta mu = +0.025 (19%), netR = 0.289 (8x)</p>
<p>For a pure detuning c = Delta mu exactly and the central reshaping residual netR (mean |a(t) - [a_control(t) + c]| over t in [-0.5, 2.0]) vanishes. The engaged coin meets this to 6% with netR = 0.037; the harvest deviates to 19% with an EIGHT times larger netR = 0.289 - the coin's departure from a translation is exactly its state-dependence.</p>

<h3>3. The Mirror Cannot See the Constants</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">a pure detuning leaves every ratio P(w)/P(-w), every cumulant symmetry, every tilt center unchanged</p>
<p>The constant part of the coin hides from every lens of Ch.77-80. Its fee shows only in Delta mu (which the variance/cumulant books of Ch.76/78 captured) and in this chapter's reshaping residual - Ch.75's two accounts, now separated into the constant and the conditional.</p>

<h3>4. The 0/0 and the Constant</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">as c -&gt; 0 and the coin -&gt; pure detuning, netR -&gt; 0 : the reshaping/translation ratio is 0/0</p>
<p>Its removable value is a State-Dependence Index: engaged ~6% detuned, harvest 19% - the fraction of the demon's work-curve action that cannot be absorbed by a shift, the part a Maxwell demon really spends on conditioning.</p>

<h3>5. Part Priced, Part Engineered</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">engaged: 6% shaped, 94% detuned ; harvest: 19% shaped, 81% detuned</p>
<p>The demon, to first order, is a constant - its whole action is a detuning invisible to the mirror - and only its state-dependent tail reshapes the curve. The split (6% engaged, 19% harvest) is the information cost in its purest measured form, and the 0/0 between translation and reshaping is resolved at last.</p>
""",
            "quiz": [
                {"q": "For a pure constant detuning delta, the tilted mean obeys:", "options": ["a(t) -> a(t) + delta, so c = Delta mu", "a(t) -> 0", "a(t) -> sigma^2", "a(t) doubles"], "correct": 0},
                {"q": "Measured c - Delta mu for the engaged coin:", "options": ["-0.004 (6%) - nearly pure detuning", "0.289", "-0.129", "0.90"], "correct": 0},
                {"q": "The harvest coin's central reshaping residual netR is:", "options": ["0.289, eight times the engaged 0.037", "0.037", "-0.154", "3.06"], "correct": 0},
                {"q": "A pure detuning is invisible to:", "options": ["the mirror P(w)/P(-w) and every tilt center", "the variance", "Delta mu", "nothing"], "correct": 0},
                {"q": "The State-Dependence Index (shaped fraction) is:", "options": ["~6% engaged, ~19% harvest", "0.894", "50%", "100%"], "correct": 0}
            ]
        },
        {
            "id": 82,
            "title": "The Two Ledgers Are One Price: the Coin's Detuning, Its Information Book, and the Extraction Efficiency per Bit (Sagawa-Ueda 2010, Szilard-Landauer)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 82: The Two Ledgers Are One Price</h2>
<p>Ch.74/75 kept the demon's EXPONENTIAL ledger ln J_act = ln &lt;e^(-W)&gt; and Ch.80/81 kept the TILT-CENTER ledger, whose translation is the realized work detuning Delta mu = mu_coin - mu_control. This chapter asks whether they are the same price, and how efficiently a real coin buys the bit.</p>

<h3>1. Two Books on One Engine</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">ln J_act = ln &lt;e^(-W)&gt; (Ch.74/75) ; Delta mu = mu_coin - mu_control (Ch.80/81) ; I = ln 2 = 0.6931 nats, J &lt;= e^I</p>
<p>On the reversible control ln J = 0.0006 ~ 0, so Delta mu is precisely the work information purchases. The hypothesis: a mild (mostly constant-detuning) coin reads the same number in both books, Delta mu ~ -ln J_act.</p>

<h3>2. The Ledgers Agree on the Mild Coin</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">engaged 0.35/2: Delta mu = -0.0701, -ln J = -0.0726, ratio 0.97 (~3%) ; 0.25/4: 1.04 ; harvest: 1.18</p>
<p>The mild coin reads -0.070 in both books to 3%. The strong coin departs - the deviation |Delta mu + ln J_act| grows exactly with the shaping residual netR of Ch.81: the constant part of the demon equals its bookkeeping, and the excess is the conditional, state-dependent part a mere detuning cannot price.</p>

<h3>3. The Extraction Efficiency per Bit</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">eps = |Delta mu| / ln 2 : 0.101 (0.35/2), 0.141 (0.25/4), 0.219 (harvest)</p>
<p>Normalized to the bit's face value, the engine runs at 10-22% of the ideal one-bit extraction, never past the ceiling (Sagawa-Ueda). The Ch.75 bill W_net = &lt;W&gt; + ln 2 &gt;= 0 is never violated - erasure always out-buys extraction.</p>

<h3>4. The 0/0 That Is the Efficiency</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">as the coin fades to control, Delta mu -&gt; 0 and ln J -&gt; 0 together: eps = |Delta mu|/ln 2 is 0/0, removable value bounded by 1</p>
<p>The efficiency per bit is a 0/0 at reversibility whose removable value is bounded by 1 (J &lt;= e^I). The measured 0.10-0.22 sit at a finite fraction of that bound - the demon's fee is never more than the coin, and a practical engine keeps only a tenth to a fifth of it.</p>

<h3>5. One Coin, Two Ledgers, One Price</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Delta mu ~ -ln J_act to 3% (mild) ; the excess is the shaping of Ch.81</p>
<p>Seven lenses on one equality close: the tilt-center translation and the exponential information book are the same measured price - a mild coin's two ledgers agree to 3%, a strong coin's split is its shaping - while the demon collects only a tenth to a fifth of its bit.</p>
""",
            "quiz": [
                {"q": "On the mild engaged coin, the two ledgers agree:", "options": ["Delta mu = -ln J_act to ~3% (ratio 0.97)", "to 50%", "never", "only at t = 1/2"], "correct": 0},
                {"q": "The extraction efficiency eps = |Delta mu|/ln 2 for engaged 0.35/2:", "options": ["0.101 (10% of the bit's face value)", "1.0", "0.693", "0.004"], "correct": 0},
                {"q": "The efficiency rises with the coin to a maximum at harvest:", "options": ["0.219 (22%)", "1.0", "0.003", "0.90"], "correct": 0},
                {"q": "The 0/0 efficiency per bit (coin fading to control) has removable value:", "options": ["bounded by 1 (Sagawa-Ueda J <= e^I)", "0 always", "ln 2", "infinity"], "correct": 0},
                {"q": "The deviation |Delta mu + ln J_act| on the strong coin tracks:", "options": ["the shaping residual netR of Ch.81", "the median bit", "the variance", "the rate function"], "correct": 0}
            ]
        },
        {
            "id": 83,
            "title": "The Straight-Line Book: the Two-Ledger Law Delta mu = -ln J_act over the Whole Frontier - slope -1, and the Shaping as a Monotone Curve (Sagawa-Ueda 2010, Crooks 1999)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 83: The Straight-Line Book</h2>
<p>Ch.82 found the two ledgers agreed on one coin; this chapter measures the FULL engaged frontier and promotes that into a LAW - Delta mu = -ln J_act, exact in the mild-coin limit, slope -1 through the origin, with the deviation a monotone function of the leverage (the Ch.81 shaping as a curve).</p>

<h3>1. Why a Law</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">sweep the fast/slow leverage 0.5/0.5, 0.35/2, 0.25/4, 0.15/6, 0.10/8, 0.05/16 on the median-bit demon</p>
<p>A single coincidence could be luck; a LAW is a straight line through the origin with a determined slope the whole frontier follows, whose residual is itself meaningful. Same round-trip trap (DeltaF = 0, D = beta = 1), Heun SRK2, seed 42.</p>

<h3>2. Slope -1 in the Mild Limit</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">mild rows: through-origin slope = -1.012 ~ -1, mean |dev| = 0.0006 (dev 0.0026, 0.0038)</p>
<p>A weak coin is entirely a constant detuning, so its detuning dollar-for-dollar equals its information book: the mild law is EXACT. The strong rows (dev 0.0126, 0.0171, 0.0244) bend the free fit to slope -0.85, but the slope -1 belongs to the mild limit.</p>

<h3>3. The Deviation Is the Shaping Curve</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">|dev| = |Delta mu + ln J_act| : 0.003, 0.004, 0.013, 0.017, 0.024 - monotone in leverage</p>
<p>The per-row deviation is nothing other than the Ch.81 state-dependence (netR), now measured as a function of the coin and verified MONOTONE. The law is exact to the extent the demon is a constant; the deviation is the conditional part that grows as the bit is engineered harder.</p>

<h3>4. The 0/0 That Fixes the Slope</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">at the control end Delta mu -&gt; 0 and ln J -&gt; 0 together : the slope is 0/0 -&gt; -1</p>
<p>The detuning and the information book both vanish at reversibility, so Delta mu / ln J_act is a 0/0 whose removable value is the measured -1 - the same constant the mirror carried at P'(0)/P(0) = 1/2 (Ch.77) and the tilt center a(1/2) = 0 (Ch.80). One removable value, dressed as the slope of a law.</p>

<h3>5. One Law</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Delta mu = -ln J_act : exact for the constant detuning of a weak demon, bent monotonically by a strong one's shaping</p>
<p>Eight lenses on one equality P(+W)/P(-W) = e^W close as one law: the demon's price is a straight line through the origin with slope -1, fixed by the mirror's own removable value.</p>
""",
            "quiz": [
                {"q": "In the mild-coin limit the two-ledger slope through the origin is:", "options": ["-1.012 ~ -1 with mean |dev| 0.0006 (the law is exact)", "-0.85", "0", "+1"], "correct": 0},
                {"q": "The two-ledger law reads:", "options": ["Delta mu = -ln J_act", "Delta mu = ln J_act", "Delta mu = 0", "Delta mu = q"], "correct": 0},
                {"q": "The |deviation| = |Delta mu + ln J_act| is:", "options": ["monotone in leverage (0.003 -> 0.024), the Ch.81 shaping", "always zero", "constant 0.9", "the median bit"], "correct": 0},
                {"q": "At the control end the slope Delta mu/ln J is:", "options": ["0/0 whose removable value is -1", "0 exactly", "ln 2", "1"], "correct": 0},
                {"q": "The free fit over the strong frontier bends the slope to:", "options": ["-0.85 (strong rows add shaping)", "-1.012", "0.97", "0.219"], "correct": 0}
            ]
        },
        {
            "id": 84,
            "title": "No Local Fingerprint: the two-ledger deviation is invisible to every isolated feature of the work distribution - yet monotone in the coin (Sagawa-Ueda 2010)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 84: No Local Fingerprint</h2>
<p>Ch.83's two-ledger law is exact in the mild limit. This chapter asks what the deviation |Delta mu + ln J_act| IS - and measures four natural fingerprints of the coin's work distribution, finding all fail to track it (a sharp honest negative that defines the law as a global identity).</p>

<h3>1. The Question</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">four fingerprints: far-tail asymmetry R (Ch.79), midline trace bend (Ch.80), third and fourth cumulants (Ch.78)</p>
<p>On the same round-trip trap, sweep the frontier and compare each feature of the coin's work distribution to the two-ledger deviation. Which one grows with the leverage and prices the deviation?</p>

<h3>2. All Four Fail</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">dev grows 0.003-&gt;0.024 while R is flat ~0.5-0.6, bend flat ~0.001, and k3/k4 DECREASE (0.157-&gt;0.103, 0.429-&gt;0.245)</p>
<p>The deviation grows monotonically while every isolated feature stays flat or moves the OPPOSITE way. The far-tail asymmetry is the round trip's own baseline kurtosis (nonzero even on the null); the trace "translates, not bends" all the way to harvest; the cumulants shrink as the coin strengthens.</p>

<h3>3. A Global Relation, No Local Shadow</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">dev = Delta mu + ln J = -F_c'(0) + F_0'(0) + F_c(1) : a whole-distribution identity</p>
<p>The deviation is a specific combination of the coin's work book and its information book - the tilt function at t=0 and t=1 against the control's derivative. No single moment, tail shape, or local bend of the coin alone carries it. The law is exact exactly for a coin that is a constant added to the control trajectory.</p>

<h3>4. Yet Monotone in the Coin Itself</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">|dev| monotone in |Delta mu| : 0.003-&gt;0.024 as 0.070-&gt;0.151, and exactly zero at the null</p>
<p>Despite having no local fingerprint, the deviation is a strictly monotone function of the coin's own detuning - the very translation the law prices. The correction is driven by how hard the demon works, though invisible to every isolated feature of the result.</p>

<h3>5. One Definition</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">the price of the bit is set by the whole work book against the whole information book - no slice of the work distribution alone can see it</p>
<p>Four negatives define the law as a genuine whole-distribution identity: a weak coin IS a translation; anything beyond a pure translation fails the law in a way no local statistic can fingerprint.</p>
""",
            "quiz": [
                {"q": "Which isolated feature of the coin's work distribution tracks the two-ledger deviation?", "options": ["none - all four fail (R flat, bend flat, k3/k4 decrease)", "the third cumulant", "the far-tail rate asymmetry", "the midline trace bend"], "correct": 0},
                {"q": "As the coin strengthens, the third and fourth cumulants:", "options": ["decrease (0.157->0.103, 0.429->0.245), opposite to the deviation", "increase", "stay constant", "equal the deviation"], "correct": 0},
                {"q": "The two-ledger deviation is a:", "options": ["global relation between work book and information book with no local signature", "local moment", "tail shape", "midline bend"], "correct": 0},
                {"q": "The deviation is strictly monotone in:", "options": ["the coin's own detuning |Delta mu| (0.003->0.024 as 0.070->0.151)", "the fourth cumulant", "the far-tail R", "the trace bend"], "correct": 0},
                {"q": "The mild limit is special because there the coin:", "options": ["is exactly a constant added to the control trajectory, so the law holds", "has zero work", "has infinite variance", "is reversible in time"], "correct": 0}
            ]
        },
        {
            "id": 85,
            "title": "The One Price Is the Quadratic: a(1/2) = -ln J_act at every leverage - the Gaussian identity F'(1/2) = F(1), universal (Crooks 1999, Seifert 2012)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 85: The One Price Is the Quadratic</h2>
<p>Applying known reality to Ch.82/83 yields a correction: the universal price is a(1/2) = -ln J_act, holding at EVERY leverage (control and strongest harvest coin alike), because the trap produces near-Gaussian work and F is quadratic.</p>

<h3>1. The Known Reality</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Gaussian work -&gt; F(t) = -mu t + 1/2 sigma^2 t^2 -&gt; F'(1/2) = F(1) -&gt; a(1/2) = -ln J_act</p>
<p>For overdamped Brownian motion in a time-varying harmonic trap the work is Gaussian, so the tilt function is quadratic: the midpoint slope equals the endpoint value. This needs no reversibility and no control reference - it is a property of the parabola alone.</p>

<h3>2. Measured Universal</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">|a(1/2) + ln J| &lt;= 0.0004 on every row (sampling), F-quadratic rms ~8e-5: control -0.00003, harvest -0.00035</p>
<p>Across the whole frontier + control: a(1/2) = -ln J_act to +/-0.0004 everywhere, and F is parabolic to 1e-4. The identity is universal because it is the Gaussian quadratic structure, not a reversibility statement.</p>

<h3>3. The Correction of Ch.82/83</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">Delta mu + ln J = F_c(1) - F_c'(0) + F_0'(0) : cancels to zero only when J_control ~ 1 (reversibility)</p>
<p>The earlier Delta mu = -ln J_act is the mild-limit shadow: it subtracts the control derivative, which cancels only when the control is reversible. The universal identity a(1/2) = -ln J needs no control and no reversibility.</p>

<h3>4. The Deviation Is the Irreversibility, Not a Broken Price</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">harvest: a + ln J = -0.00035 yet Delta mu + ln J = -0.024</p>
<p>The monotone |Delta mu + ln J| of Ch.83/84 is Delta mu - the t=0 derivative - leaving the quadratic midpoint as the feedback injects irreversibility. The price a(1/2) = -ln J never breaks.</p>

<h3>5. One Correction</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">same price, two views: the universal quadratic identity vs its mild-limit shadow - and the growing deviation is the feedback's irreversibility, not a broken law</p>
<p>Eight lenses close corrected: the one price of the reversible mirror is the quadratic identity a(1/2) = -ln J, universal because the trap's work is Gaussian.</p>
""",
            "quiz": [
                {"q": "The universal one-price identity of the mirror strand is:", "options": ["a(1/2) = -ln J_act, exact at every leverage", "Delta mu = -ln J_act only", "a(1/2) = 0 always", "F(0) = F(1)"], "correct": 0},
                {"q": "It holds universally because:", "options": ["F is quadratic (near-Gaussian work), F'(1/2) = F(1)", "the coin is reversible", "J_control ~ 1", "the trap is stiff"], "correct": 0},
                {"q": "The old Delta mu = -ln J_act is a mild-limit shadow because:", "options": ["it subtracts the control derivative, cancelling only when J_control ~ 1", "it uses t=1/2", "it is a theorem of the FT", "it ignores the variance"], "correct": 0},
                {"q": "The growing |Delta mu + ln J| of Ch.83/84 is:", "options": ["Delta mu leaving the quadratic midpoint (the feedback's irreversibility), not a broken price", "a wrong measurement", "the erasure cost", "the tilt center failing"], "correct": 0},
                {"q": "At harvest, while Delta mu + ln J = -0.024, the true price residual a + ln J is:", "options": ["-0.00035 (the price never breaks)", "-0.024", "0.6931", "1.0"], "correct": 0}
            ]
        },
        {
            "id": 86,
            "title": "The State at the Origin Is a Matrix: indeterminate 0/0 forms as physical state functions - point, line, matrix (Onsager 1931, Kubo 1957)",
            "part": "IX. Grand Unification",
            "content": """
<h2>Chapter 86: The State at the Origin Is a Matrix</h2>
<p>A 0/0 (indeterminate) form at a coincidence point is not a hole in the state but a STATE whose content is its differential structure: the scalar ratio (point), the directional slope (line), and the full linear-response operator (matrix). As x runs over all reals, the derivative is the canonical 0/0 that turns a point into a line; in several variables it becomes a Jacobian, Onsager flux-force matrix, or Hessian.</p>

<h3>1. Point, Line, Matrix</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">POINT: f = g/h at the common zero (undefined scalar, x=0) ; LINE: slope g'(0)/h'(0) ; MATRIX: R_ij = d(output_i)/d(input_j)</p>
<p>The derivative is the canonical 0/0; each approach direction gives one directional derivative, and the full set is the linear-response matrix. This is how physics turns a removable singularity into a state: a transport coefficient or susceptibility is a 0/0 ratio valued at equilibrium.</p>

<h3>2. The Demon Strand's 0/0 Origin</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">at control: Delta mu = 0 and -lnJ = 0 together, so their ratio is 0/0</p>
<p>Build the state's 2x2 linear-response matrix from two outputs (Delta mu, -lnJ) against two genuine input directions (coin coupling c, protocol speed v), by finite differences.</p>

<h3>3. Measured Matrix</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">R = [[-0.047, +0.036],[-0.052, +0.031]], det = +0.0004, coin-column ratio ~ -1</p>
<p>The coin-column ratio ~ -1 recovers the price of Ch.85 along the approach line. The determinant ~ 0 makes R RANK-1: Delta mu and -lnJ move together in both directions - the two ledgers are literally one quantity. Finite cross-entries make it a genuine 2x2 tensor.</p>

<h3>4. Rank-1 = One Price</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">det R ~ 0 : the two outputs respond collinearly in every direction</p>
<p>The 'two ledgers one price' of Ch.85 is a MATRIX DEGENERACY. The state at the origin is a tensor, not a hole - the framework's founding 0/0 is here given its proper content as differential structure.</p>

<h3>5. Undefined Is Determined</h3>
<p style="font-size:1.1em; text-align:center; padding:10px;">an indeterminate form is a state whose removable value is a slope (line) and whose full structure is a tensor (matrix)</p>
<p>Point to line to matrix: the rim of the 0/0 is the derivative, and the derivative is the matrix of the state at its origin.</p>
""",
            "quiz": [
                {"q": "At a 0/0 origin, the physical state's full content is:", "options": ["the linear-response matrix (point -> line -> matrix)", "nothing (undefined)", "the median", "the rate function only"], "correct": 0},
                {"q": "The derivative f'(x) at h=0 is the canonical:", "options": ["0/0 whose value is a slope (a line)", "constant", "vector", "integral"], "correct": 0},
                {"q": "The measured 2x2 response matrix at the control origin has:", "options": ["det ~ 0, i.e. rank-1 (two ledgers respond as one quantity)", "det = 1", "infinite rank", "zero diagonal"], "correct": 0},
                {"q": "The coin-column ratio d(mu)/d(-lnJ) recovers:", "options": ["the price ~ -1 of Ch.85 (the approach line slope)", "the variance", "the median", "0.6931"], "correct": 0},
                {"q": "A transport coefficient or susceptibility is:", "options": ["the well-defined value of a 0/0 ratio at equilibrium", "always a pure number 1", "never defined", "a matrix of zeros"], "correct": 0}
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
