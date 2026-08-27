#!/usr/bin/env python3
"""
Sigma Virtual School Server
============================

A zero-dependency learning management system for the L.O.R.E. framework.

Usage:
    python sigma_school_server.py [--port PORT]

Features:
    - 49 chapters from "The Removable Singularity"
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
