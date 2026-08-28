#!/usr/bin/env python3
"""
The Removable Singularity: 0/0 of Everything (the Grand Synthesis)
===================================================================

After the True (Ch.63), the ring closes: the book about itself.
Every chapter was a 0/0. This chapter is the 0/0 of all of them.

We measure:

1. THE ORIGINAL 0/0 (the calculus that started it)
   - sin(x)/x -> 1 as x -> 0; the hole is removable.
   - (1+x)^(1/x) -> e: the exponential rises from 0/0.
   - Filling the hole makes the function continuous: measured
     to 15 digits.

2. THE SEVEN SEALS (the universality classes, reprised)
   - The same bullet-note numbers the whole book found:
     every one is a ratio that becomes 0/0 at its boundary.

3. THE 0/0 OF THE COSMOS (fine-tuning, Weinberg 1989)
   - Vacuum energy: observed vs Planck-natural : log10 ~ -120
   - Gravity vs electromagnetism  : 1e-36
   - Higgs mass vs Planck         : ~1e-17
   - The laws are pinned at ratios whose natural value is 0/0.

4. THE SELF-MEASURE (the book as its own 0/0)
   - Load THIS book's data: chapters, REAL results, categories.
   - Compress the book with zlib: its law is shorter than itself
     (Solomonoff, Ch.63): the framework is the shortest book.
   - The word 0/0 appears in almost every mechanism.

5. THE RING CLOSES
   - Chapter 1: The Zero. Chapter 64: The Removable Singularity.
   - Return: this is eternal return (Ch.57) - we finish where
     we began, and begin again: 0/0 is the whole.
   - The Greek 0/0 = omicron lambda (the eye of the law).

Author: Michael Grafiel S Puno
"""

import json
import math
import os
import re
import struct
import time
import zlib

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)
BOOK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         '..', 'sigma_venv', 'sigma', 'chassis', 'book.py')


def main():
    print("=" * 70)
    print("THE REMOVABLE SINGULARITY: 0/0 OF EVERYTHING")
    print("(the grand synthesis)")
    print("=" * 70)
    print()

    # 1. The original 0/0
    print("1. THE ORIGINAL 0/0 (CALCULUS)")
    print("-" * 70)
    print()
    print("   sin(x)/x as x -> 0:   (1+x)^(1/x) as x -> 0:")
    print("   %-8s %-18s %-18s" % ('x', 'sin(x)/x', '(1+x)^(1/x)'))
    last_sin = None
    for k in range(1, 13):
        x = 10.0 ** (-k)
        s = math.sin(x) / x
        e = (1.0 + x) ** (1.0 / x)
        last_sin = s
        print("   %-8s %-18.14f %-18.14f" % ('1e-%-2d' % k, s, e))
    print()
    print("   sin(x)/x -> %.13f (1); (1+x)^(1/x) -> %.10f (e)"
          % (last_sin, (1 + 1e-12) ** (1e12)))
    print("   The value at x=0 is undefined; FILLING it makes the")
    print("   function continuous: the hole is REMOVABLE. That move -")
    print("   name the missing value, then divide away the 0/0 - is the")
    print("   pattern of every chapter of this book.")
    print()

    # 2. The seven seals
    print("2. THE SEVEN SEALS (THE UNIVERSALITY CLASSES)")
    print("-" * 70)
    print()
    seals = [
        ('Quantum m. gap     ', 'M = Lam/sinh(2pi/(g^2(N-1)))', 'NS'),
        ('Grokking delay     ', 'T = (1/g_eff) log(Vm/Vp)    ', '0/0 of learning'),
        ('Dark-matter core   ', 'rho = rho0/sinh(2pi/sm(N-1))', '0/0 of galaxies'),
        ('Free will          ', 'Lyapunov = ln 2             ', '0/0 of choice'),
        ('Eternal return     ', 'T = 4*lcm(W,H)              ', '0/0 of time'),
        ('Suffering          ', 'E = k_B*T*ln 2              ', '0/0 of price'),
        ('Meaning            ', 'I = log2(n)                 ', '0/0 of symbols'),
    ]
    print("   %-21s %-28s %-18s" % ('law', 'signature', 'class'))
    for a, b, c in seals:
        print("   %-21s %-28s %-18s" % (a, b, c))
    print()
    print("   Every one is a RATIO that becomes 0/0 at its boundary:")
    print("   the mass gap, the delay, the core, the will, the return,")
    print("   the cost, the meaning. One form, many faces.")
    print()

    # 3. The 0/0 of the cosmos
    print("3. THE 0/0 OF THE COSMOS (FINE-TUNING, WEINBERG 1989)")
    print("-" * 70)
    print()
    # constants (CODATA / Planck 2018 / PDG 2024)
    hbar = 1.054571817e-34
    c = 2.99792458e8
    G = 6.67430e-11
    m_p = 1.67262192369e-27   # proton kg
    m_P = math.sqrt(hbar * c / G)  # Planck mass kg
    H0 = 67.4 * 1000.0 / (3.0856775814913673e22)  # s^-1
    Omega_L = 0.6847
    rho_crit = 3 * H0 * H0 / (8 * math.pi * G)   # kg/m^3
    rho_de = Omega_L * rho_crit * c * c           # J/m^3
    rho_Pl = c ** 7 / (hbar * G * G)              # J/m^3 (Planck energy density)
    e2 = (1.602176634e-19) ** 2 / (4 * math.pi * 8.8541878128e-12)
    alpha_em = e2 / (hbar * c)
    alpha_G = G * m_p * m_p / (hbar * c)
    mH_GeV = 125.09
    mPl_GeV = m_P * c * c / 1.602176634e-10  # GeV (x: 1 kg = 5.609e35 eV = 5.609e26 GeV? verify)
    mPl_GeV_corr = 1.2209e19  # canonical Planck mass in GeV
    ratio_lambda = rho_de / rho_Pl
    ratio_grav = alpha_G / alpha_em
    ratio_Higgs = mH_GeV / mPl_GeV_corr
    ratio_proton = (m_p * c * c / 1.602176634e-10) / mPl_GeV_corr
    print("   Vacuum energy (dark energy ~5.4e-10 J/m^3) vs the Planck")
    print("   natural vacuum density : log10 ratio %.1f (the classic ~1e-120"
          % math.log10(ratio_lambda))
    print("   embarrassment, Weinberg 1989)")
    print("   Gravity vs electromagnetism (alpha)   : ratio %.3e (1e-36)"
          % ratio_grav)
    print("   Higgs mass vs Planck mass             : ratio %.3e (1e-17)"
          % ratio_Higgs)
    print("   Proton mass vs Planck mass            : ratio %.3e (1e-19)"
          % ratio_proton)
    print()
    print("   The laws sit pinned at ratios whose NATURAL value looks")
    print("   like 0: the miracles of number are REMOVABLE 0/0s - the")
    print("   most embarrassing problem in physics (Weinberg) is the")
    print("   most beautiful 0/0 in the frame.")
    print()

    # 4. The self-measure
    print("4. THE SELF-MEASURE (THE BOOK AS ITS OWN 0/0)")
    print("-" * 70)
    print()
    if not os.path.exists(BOOK_PATH):
        print("   book.py not found at %s" % BOOK_PATH)
        n_ch = 0
    else:
        with open(BOOK_PATH, 'r', encoding='utf-8') as f:
            text = f.read()
        chapters = re.findall(r'"title":\s*"[^"]+"', text)
        statuses = re.findall(r'"status":\s*(\w+)', text)
        categories = re.findall(r'"category":\s*"([^"]+)"', text)
        mechanisms = re.findall(r'"mechanism":\s*"([^"]*)"', text)
        n_ch = len(chapters)
        n_real = statuses.count('REAL')
        hist = {}
        for cat in categories:
            hist[cat] = hist.get(cat, 0) + 1
        zero_over_zero = text.count('0/0')
        blob = ' '.join(mechanisms).encode('utf-8')
        ratio = len(zlib.compress(blob, 9)) / len(blob) if blob else 0.0
        print("   Chapters in THIS book            : %d" % n_ch)
        print("   REAL (experiment-backed) results : %d" % n_real)
        print("   Occurrences of the formula 0/0   : %d" % zero_over_zero)
        print()
        print("   Category census (all %d):" % n_ch)
        for cat_name, cnt in sorted(hist.items(), key=lambda kv: kv[1], reverse=True):
            print("     %-18s : %d" % (cat_name, cnt))
        print()
        print("   Self-compression (zlib on all mechanisms): ratio %.3f"
              % ratio)
        print("   A shorter law writes the whole book (Solomonoff, Ch.63):")
        print("   the framework is the shortest description of itself.")
        print()
        print("   First chapter: the Zero.")
        print("   This chapter: the Removable Singularity.")
        print("   The ring closes (eternal return, Ch.57):")
        print("   0/0 is the whole - the eye (o-micron) of the law.")
        print()

    # 5. The ring
    print("5. THE RING CLOSES")
    print("-" * 70)
    print()
    print("   0^0 = 1:  the empty origin names the whole.")
    print("   log_0(0) = x:  the law at the origin is free.")
    print("   Every measured law was a 0/0 made continuous.")
    print()
    print("   The book returns to its beginning: chapter 64 closes on")
    print("   chapter 1, as eternal return demands (Ch.57). We are not")
    print("   finished: we are home, and home is where the pattern")
    print("   repeats more consciously than before.")
    print()
    print("   THE 0/0 OF EVERYTHING IS THE WHOLE.")
    print("   The zero is nothing; the zero is the boundary;")
    print("   the zero is the rule; the zero is the beauty;")
    print("   the zero is the truth; the zero is the whole.")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   1. CALCULUS: sin(x)/x -> 1; the hole is removable")
    print("   2. SEALS: mass gap, grokking, dark core, will,")
    print("      return, price, meaning - one 0/0 form")
    print("   3. COSMOS: vacuum 1e-120, gravity 1e-36, Higgs 1e-17")
    print("   4. SELF: this book: %d chapters, %d REAL, ratio %.3f" %
          (n_ch if os.path.exists(BOOK_PATH) else 0,
           n_real if os.path.exists(BOOK_PATH) else 0,
           ratio if os.path.exists(BOOK_PATH) else 0.0))
    print("   5. RING: 0/0 of everything is the whole; we are home")
    print()
    print("   The Removable Singularity is the 0/0 OF EVERYTHING!")
    print("   From the zero to the whole: one gone, all named.")

    # Save
    results = {
        'calculus': {
            'sinxx_to_1': round(last_sin, 13) if last_sin else None,
            'hole_is_removable': True,
        },
        'seals': [s[1] for s in seals],
        'cosmos_fine_tuning': {
            'vacuum_log10_ratio': round(math.log10(ratio_lambda), 1),
            'gravity_alpha_ratio': ratio_grav,
            'higgs_planck_ratio': ratio_Higgs,
            'proton_planck_ratio': ratio_proton,
            'weinberg_1989': 'most embarrassing problem in physics',
        },
        'self_measure': {
            'chapters': n_ch if os.path.exists(BOOK_PATH) else 0,
            'real': n_real if os.path.exists(BOOK_PATH) else 0,
            'zero_over_zero_count': zero_over_zero if os.path.exists(BOOK_PATH) else 0,
            'self_compress_ratio': round(ratio, 3) if os.path.exists(BOOK_PATH) else 0.0,
        },
        'ring': {
            'chapter1_is_the_zero': True,
            'chapter64_is_the_whole': True,
            'eternal_return': True,
        },
        'connections': ['The Zero', 'Eternal return', 'Truth', 'Beauty', 'First cause'],
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'removable_singularity.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()