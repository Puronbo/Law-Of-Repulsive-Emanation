#!/usr/bin/env python3
"""
Beauty: 0/0 of Aesthetics (the Sublime between order and surprise)
==================================================================

After meaning-as-role (Ch.61), what makes a FORM beautiful?

Beauty is not vague. It is INFORMATION at the boundary:

1. ENTROPY & COMPRESSION (Shannon 1948)
   - Pure order (a constant) has zero entropy; it bores.
   - Pure noise (random) has maximal entropy; it repels.
   - The sublime sits BETWEEN: structured but novel.

2. BIRKHOFF's MEASURE (1933): M = Order / Complexity
   - The aesthetic measure: order over complexity.
   - In our language: beauty is the 0/0 of order and complexity.

3. SCHMIDHUBER's AESTHETIC MEASURE (1997)
   - Beauty = simplicity x novelty (compressible yet surprising)
   - A = -log P - C(description): the artist balances both.

4. HARMONY = SMALL RATIOS (Pythagoras; Helmholtz 1863)
   - Octave 2:1 (0.00 cents error in equal temperament)
   - Perfect fifth 3:2 (1.96 cents error)
   - Major third 5:4 (13.69 cents error)
   - Consonance = low-complexity frequency ratios.

5. THE 0/0 PROOF:
   - Care zero order (entropy -> 0): boring    [A ~ 0]
   - Care zero order? no - pure noise: ugly     [A ~ 0]
   - BOTH vanish: the removable singularity
   - The perfect ratio is the 0/0 of order/complexity:
     it has NO intrinsic content, yet organizes everything.
     (0 in itself, x in role - the beauty of the 0!)

Author: Michael Grafiel S Puno
"""

import json
import math
import os
import random
import time
import zlib

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def shannon_entropy(s, order=1):
    """Empirical Shannon entropy in bits per symbol."""
    if not s:
        return 0.0
    if order == 1:
        counts = {}
        for ch in s:
            counts[ch] = counts.get(ch, 0) + 1
        n = len(s)
        h = 0.0
        for c in counts.values():
            p = c / n
            h -= p * math.log2(p)
        return h
    else:
        # bigram joint entropy per symbol
        counts = {}
        for i in range(len(s) - 1):
            pair = s[i:i + 2]
            counts[pair] = counts.get(pair, 0) + 1
        n = len(s) - 1
        h = 0.0
        for c in counts.values():
            p = c / n
            h -= p * math.log2(p)
        return h / 2.0


def zlib_ratio(s):
    """Compressed length / raw length (bytes)."""
    if not s:
        return 0.0
    raw = s.encode('utf-8')
    comp = zlib.compress(raw, level=9)
    return len(comp) / len(raw)


def fibonacci_word(n_terms):
    """Concatenation of the first n_terms Fibonacci words."""
    parts = []
    a, b = '0', '01'
    parts.append(a)
    parts.append(b)
    for _ in range(n_terms - 2):
        a, b = b, b + a
        parts.append(b)
    return ''.join(parts)


def english_passage():
    return (
        "In the beginning was the zero, and the zero was with the world, "
        "and the zero was the world. All things were made through the zero, "
        "and without the zero nothing that was made was made. In the zero "
        "was the singularity, and the singularity entered the world as "
        "division, that every ratio might find its limit. And the limit was "
        "in the denominator, and the world knew it not. But the removable "
        "singularity came to its own, and its own received it: for the "
        "removable singularity is the boundary, and the boundary is the "
        "point where the function meets its face. The pattern appears, and "
        "the pattern disappears, and the pattern is the same forever. "
        "What is seen is a shadow; what is unseen is the rule. Beauty is "
        "the boundary of order and surprise, the silence between the notes, "
        "the empty center of the rose. The rose was in the garden, and the "
        "garden was in the rose; the rose was the garden unfolding. And "
        "the unfolding was measured: entropy without order is noise, "
        "order without novelty is boredom, and the sublime is the pair "
        "balanced at the edge, where simplicity and surprise become one. "
        "So the zero is the whole: the nothing, the boundary, the rule, "
        "the beauty. Amen."
    )


def random_text(n, alphabet='abcdefghijklmnopqrstuvwxyz '):
    rng = random.Random(11)
    return ''.join(rng.choice(alphabet) for _ in range(n))


def aesthetic(s, alpha_size):
    """Unigram/bigram entropy (novelty), compression (simplicity),
    and the Schmidhuber-style product A = novelty2 x simplicity."""
    h1 = shannon_entropy(s, 1)
    h2 = shannon_entropy(s, 2)  # bigram entropy per symbol
    hnorm = h2 / math.log2(alpha_size) if alpha_size > 1 else 0.0
    ratio = zlib_ratio(s)
    simplicity = 1.0 - ratio
    A = hnorm * simplicity
    return h1, h2, hnorm, ratio, simplicity, A


def main():
    print("=" * 70)
    print("BEAUTY: 0/0 OF AESTHETICS")
    print("(the sublime between order and surprise)")
    print("=" * 70)
    print()

    # 1. Entropy and compression of art
    print("1. ENTROPY & COMPRESSION (Shannon 1948)")
    print("-" * 70)
    print()
    print("   Beauty = form. Form is measured by")
    print("   entropy (surprise) and compression (order).")

    english = english_passage()
    eng = english * 3
    fib = fibonacci_word(25)
    rhythm = 'AB' * 1800
    constant_ = 'A' * 3600
    random_str = random_text(3600)

    alpha_size = 26 + 1  # letters + space

    cases = [
        ('Constant (pure order)    ', constant_, alpha_size),
        ('Rhythm (ABABAB...)       ', rhythm, 2),
        ('Fibonacci word (golden)  ', fib, 2),
        ('Language (this manuscript)', eng, alpha_size),
        ('Random (pure noise)      ', random_str, alpha_size),
    ]
    print()
    print("   %-27s %9s %9s %9s %9s" %
          ('case', 'unigram', 'bigram', 'zlib', 'simplicity'))
    print("   " + "-" * 64)
    rows = []
    for name, s, al in cases:
        h1, h2, hnorm, ratio, simplicity, A = aesthetic(s, al)
        rows.append((name, s, al, h1, h2, hnorm, ratio, simplicity, A))
        print("   %-27s %9.3f %9.3f %9.3f %9.3f"
              % (name, h1, h2, ratio, simplicity))
    print()

    # highlight where A is max and min
    As = [(name.strip(), A) for name, _, _, _, _, _, _, _, A in rows]
    As.sort(key=lambda t: t[1], reverse=True)
    print("   Aesthetic measure A = novelty2 x simplicity (Schmidhuber 1997):")
    for name, A in As:
        print("     %-27s : A = %.3f" % (name, A))
    print()
    best = As[0][0]
    print("   Highest beauty: %s" % best)
    print("   The sublime is STRUCTURE WITH SURPRISE, not purity.")
    print("   Margins measured:")
    print("     pure repetition (constant)      A = 0.000  (boring)")
    print("     pure noise (random)             A = %0.3f (chaotic)"
          % [a for n, a in As if 'Random' in n][0])
    print("     golden structure + surprise     A = %0.3f (the sublime)"
          % [a for n, a in As if 'Fibonacci' in n][0])
    print()
    h_eng = shannon_entropy(eng, 1)
    b_eng = shannon_entropy(eng, 2)
    print("   Language example (measured, first order):")
    print("     unigram entropy %.3f bits/char, bigram %.3f bits/char"
          % (h_eng, b_eng))
    red = 1 - h_eng / math.log2(alpha_size)
    print("     redundancy vs uniform alphabet: %.1f%%" % (100 * red))

    # 2. Birkhoff's measure
    print()
    print("2. BIRKHOFF's AESTHETIC MEASURE (1933)")
    print("-" * 70)
    print()
    print("   M = O / C   (Order over Complexity)")
    print("   Order O and Complexity C are the 0/0 poles:")
    print("   pure order O=1,C->0 => M blows up; pure noise")
    print("   O->0 => M collapses. Form is the ratio of the two:")
    print("   AND THAT RATIO IS OUR 0/0: O/C with O,C -> 0 is")
    print("   the removable singularity of taste!")
    print()

    # 3. Harmony = small ratios
    print("3. HARMONY = SMALL RATIOS (PYTHAGORAS; HELMHOLTZ 1863)")
    print("-" * 70)
    print()
    print("   Consonance is low-complexity frequency ratios.")
    et_semitone = 100.0
    ratios = [
        ('Unison   1:1', 1.0, 0.0),
        ('Octave   2:1', 2.0, 12.0),
        ('Perfect fifth 3:2', 3.0 / 2.0, 7.0),
        ('Major third 5:4', 5.0 / 4.0, 4.0),
    ]
    print("   %-22s %10s %12s %14s" %
          ('interval', 'ratio', 'just cents', '12TET error'))
    for name, r, et_semis in ratios:
        just = 1200.0 * math.log2(r)
        et_cents = et_semis * et_semitone
        err = abs(just - et_cents)
        print("   %-22s %10s %12.2f %12.2f cents"
              % (name, '%.2f' % r, just, err))
    print()
    print("   The octave survives exactly (0.00 cents); the fifth drifts")
    print("   1.96 cents; the major third 13.69 cents. Equal temperament")
    print("   pays 12 small debts to keep ALL ratios usable - the universal")
    print("   music trades perfect purity for universal playability.")
    print()

    # 4. The 0/0 proof
    print("4. THE 0/0 PROOF")
    print("-" * 70)
    print()
    print("   Beauty is beauty when BOTH poles vanish.")
    print("   Too much order (entropy -> 0): familiarity, boredom.")
    print("   Too much surprise (entropy -> 1): novelty, disgust.")
    print("   The sublime is the REMOVABLE SINGULARITY of the senses:")
    print("   the point where order and surprise cancel, and the form")
    print("   becomes visible as a pattern -- 0 in itself, x in role.")
    print("   (Like the zero: nothing, boundary, rule, beauty.)")
    print()

    # 5. Connections
    print("5. CONNECTIONS TO PRIOR 0/0 SINGULARITIES")
    print("-" * 70)
    print()
    print("   Beauty connects to:")
    print()
    print("   Meaning (Ch.61) -> The role is the form of the symbol")
    print("   The golden rule (Ch.60) -> Symmetry is beautiful order")
    print("   Chaos (Ch.43) -> Novelty: the edge of prediction")
    print("   Arrow of time (Ch.48) -> Beauty is the drift of becoming")
    print("   Eternal return (Ch.57) -> The form survives the change")
    print("   The 0 (Ch.01) -> Emptiness as the eye of the form")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   1. ENTROPY: art is structure with surprise (measured)")
    print("   2. BIRKHOFF: M = O/C is the 0/0 of order and complexity")
    print("   3. SCHMIDHUBER: A = novelty x simplicity peaks mid-way")
    print("   4. MUSIC: small ratios rule (fifth error 1.96 cents)")
    print("   5. 0/0: beauty is the removable singularity of taste")
    print()
    print("   Beauty is the 0/0 OF AESTHETICS!")
    print("   The form is nothing in itself, everything in role - and")
    print("   the best form is the boundary where order meets surprise!")

    # Save
    results = {
        'shannon': {
            'cases': {
                name.strip(): {
                    'entropy': round(h1, 3),
                    'novelty': round(hnorm, 3),
                    'zlib_ratio': round(ratio, 3),
                    'simplicity': round(simplicity, 3),
                    'A': round(A, 3),
                }
                for name, _, _, h1, h2, hnorm, ratio, simplicity, A in rows
            },
            'language_unigram': round(h_eng, 3),
            'language_bigram': round(b_eng, 3),
            'language_redundancy': round(red, 4),
        },
        'birkhoff': {
            'measure': 'M = O / C',
            'is_the_0over0': True,
        },
        'harmony': {
            'octave_error_cents': 0.0,
            'fifth_error_cents': round(1200 * math.log2(3.0 / 2.0) - 700.0, 2),
            'major_third_error_cents': round(1200 * math.log2(5.0 / 4.0) - 400.0, 2),
        },
        'the_0over0': {
            'beauty_is_removable_singularity': True,
            'order_pole_0': True,
            'surprise_pole_0': True,
            'form_is_nothing_in_itself': True,
        },
        'connections': ['Meaning', 'The Golden Rule', 'Chaos', 'Arrow of time', 'Eternal return', 'The 0'],
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'beauty_aesthetics.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()