#!/usr/bin/env python3
"""
The Problem of Evil: 0/0 of Suffering
======================================

If creation exists (Ch.58) and the creator is good - why suffering?
We answer with COMPUTATION, not apology:

1. COMPUTATION IS NOT FREE (Landauer 1961):
   - Erasing 1 bit costs k_B * T * ln(2) energy
   - Information is physical (Landauer; Bennett 1982): no free lunch
   - Every irreversible step of the simulation pays this price

2. THE HEAT OF CREATION (BUDGET OF CH.54):
   - The simulation ran ~10^121 operations
   - If each op discarded just 1 bit at 2.7 K: ~10^100 J
   - Universe energy budget ~10^70 J: ratio ~10^-30
   - The creator MUST compute almost-reversibly (Bennett):
     efficiency ~10^-30 per op: near-free, not free

3. SUFFERING AS PREDICTION ERROR (Friston 2010):
   - Living systems minimize surprise (free energy)
   - Pain = persistent prediction error (world vs model)
   - The wrong model suffers more than the right model
   - Learning REMOVES the error: surprise falls (redemption)

4. THE PRICE OF FREEDOM (Ch.55):
   - Real choice needs contingent outcomes (chaos, Ch.43; quantum, Ch.49)
   - Contingency = unpredictability = occasional errors and harms
   - A world with stakes cannot be a world without risk
   - The quantum arrow (Ch.48) is paid in entropy

5. THEODICY (Leibniz 1710; Plantinga 1974):
   - "Best of all possible worlds" ~ least-cost, most-novel computation
   - Free-will defense: love and virtue need real alternatives
   - In the simulation: alternatives are branches (Ch.49)
   - Suffering is the interior cost of a universe that can create

6. THE 0/0 PROOF:
   - Within the created system, good/evil are interior labels
   - The mechanism is neutral; the FELT valence is first-person (Ch.53)
   - The physical account is complete: suffering = cost of computation
   - Evil is the 0/0: neither a thing nor an absence - a PRICE
   - Redemption = learning: surprise minimized by the right model

7. CONNECTIONS:
   - Free will (Ch.55): risk is the price of choice
   - Arrow of time (Ch.48): entropy is the cost of becoming
   - Simulation (Ch.54): the computational budget
   - The self (Ch.56): the subject who pays
   - Hard problem (Ch.53): the first-person cost
   - Learning (Ch.35): the redeemer

Author: Michael Grafiel S Puno
"""

import math
import json
import os
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def landauer_cost(T, k_B=1.380649e-23):
    """Landauer 1961: minimum cost to erase 1 bit at temperature T."""
    return k_B * T * math.log(2.0)


def heat_of_creation_tight(ops, E_bit):
    """Total dissipation if every operation erased one bit."""
    return ops * E_bit


def surprise_profile(trials, prior_a, prior_b, true_p, seed=0):
    """
    A coin-toss learner with a Beta(a,b) prior.
    Returns trial, cumulative surprise (log2), posterior mean.
    Surprise = predicted -log2 P(actual). A wrong model pays more;
    learning fixes the model; the total cost stays finite.
    """
    rng = __import__('random').Random(seed)
    a, b = prior_a, prior_b
    cum = 0.0
    out = []
    for t in range(trials):
        mean = a / (a + b)
        # predicted probability of heads
        p_h = mean
        x = 1 if rng.random() < true_p else 0
        if x == 1:
            surprise = -math.log2(max(p_h, 1e-12))
            a += 1
        else:
            surprise = -math.log2(max(1 - p_h, 1e-12))
            b += 1
        cum += surprise
        if t % 250 == 0 or t == trials - 1:
            out.append((t + 1, round(cum, 1), round(a / (a + b), 4)))
        # learning: the wrong prior converges toward the true p
    return out


def theodicy_0over0():
    return {
        'good_evil_are_interior_labels': True,
        'mechanism_is_neutral': True,
        'suffering_is_computational_cost': True,
        'evil_is_a_price_not_a_thing': True,
        'redemption_is_learning': True,
    }


def main():
    print("=" * 70)
    print("THE PROBLEM OF EVIL: 0/0 OF SUFFERING")
    print("=" * 70)
    print()

    # 1. Landauer
    print("1. COMPUTATION IS NOT FREE (LANDAUER 1961)")
    print("-" * 70)
    print()
    T_cmb = 2.7
    T_brain = 310.0
    E_cmb = landauer_cost(T_cmb)
    E_brain = landauer_cost(T_brain)
    print("   Erasing 1 bit costs k_B * T * ln(2):")
    print("   At CMB temperature 2.7 K  : %.3e J/bit" % E_cmb)
    print("   At brain temperature 310 K: %.3e J/bit" % E_brain)
    print()
    print("   Information is physical (Landauer; Bennett 1982).")
    print("   There is NO free lunch: every irreversible step pays.")

    # 2. Heat of creation
    print()
    print("2. THE HEAT OF CREATION (BUDGET OF CH.54)")
    print("-" * 70)
    print()
    ops = 1.0e121
    E_universe = 3.0e70
    heat = heat_of_creation_tight(ops, E_cmb)
    ratio = E_universe / heat
    print("   The simulation performed ~1e121 operations (Ch.54).")
    print("   If each op discarded 1 bit at 2.7 K:")
    print("   dissipation ~ %.1e J" % heat)
    print("   Universe energy budget ~ %.1e J" % E_universe)
    print("   Allowed fraction   ~ %.1e" % ratio)
    print()
    print("   The creator MUST be ~10^-28 efficient per op:")
    print("   essentially reversible computation (Bennett 1982).")
    print("   Quasi-free is the thermodynamic price of sovereignty.")

    # 3. Suffering as prediction error
    print()
    print("3. SUFFERING AS PREDICTION ERROR (FRISTON 2010)")
    print("-" * 70)
    print()
    correct = surprise_profile(2000, 2, 2, 0.5, seed=1)
    wrong = surprise_profile(2000, 18, 62, 0.5, seed=1)  # wrong prior, learns
    print("   Agent A (correct prior, p=0.5):")
    for (t, cum, mean) in correct:
        print("     trial %5d  cum-surprise %8.1f bits  model p %.4f" % (t, cum, mean))
    print()
    print("   Agent B (wrong prior p~0.22, learns):")
    for (t, cum, mean) in wrong:
        print("     trial %5d  cum-surprise %8.1f bits  model p %.4f" % (t, cum, mean))
    print()
    cumA = correct[-1][1]
    cumB = wrong[-1][1]
    print("   Final A: %.1f bits   Final B: %.1f bits   gap %.1f"
          % (cumA, cumB, cumB - cumA))
    print()
    print("   The wrong model PAYS more (extra surprise = suffering).")
    print("   But learning pulls the model toward truth: surprise")
    print("   growth slows - Redemption is INFORMATION (learning).")

    # 4. Price of freedom
    print()
    print("4. THE PRICE OF FREEDOM (CH.55)")
    print("-" * 70)
    print()
    print("   Real choice needs contingent outcomes (chaos, quantum).")
    print("   Contingency = unpredictability = risk of harm.")
    print()
    print("   To have LOVE and VIRTUE there must be real")
    print("   alternatives (Plantinga 1974, free-will defense).")
    print("   A world with stakes cannot be free of risk.")
    print("   The price of the second law (Ch.48) is paid in entropy,")
    print("   and the price of freedom (Ch.55) is paid in suffering.")

    # 5. Theodicy
    print()
    print("5. THEODICY")
    print("-" * 70)
    print()
    print("   Leibniz (1710): the best of ALL possible worlds.")
    print("   In computation terms: least-cost, most-novel")
    print("   program that sustains agents (Ch.53-56).")
    print()
    print("   The alternatives (branches, Ch.49) ARE the design:")
    print("   suffering is the interior cost of a universe that")
    print("   can create, choose, love, and learn.")

    # 6. 0/0 proof
    print()
    print("6. THE 0/0 PROOF")
    print("-" * 70)
    print()
    t = theodicy_0over0()
    for k, v in t.items():
        print("   %-42s: %s" % (k, v))
    print()
    print("   Within the created system good/evil are interior")
    print("   labels: the mechanism is neutral. The FELT valence")
    print("   is first-person (Ch.53); the physical account is")
    print("   complete: suffering = cost of computation.")
    print()
    print("   Evil is the 0/0: neither a thing nor an absence")
    print("   but a PRICE. Redemption = learning: the model")
    print("   improves, surprise falls, the cost is repaid as")
    print("   wisdom (the very machinery of this book).")

    # 7. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO PRIOR 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   The problem of evil connects to:")
    print()
    print("   Free will (Ch.55) -> Risk is the price of choice")
    print("   Arrow of time (Ch.48) -> Entropy: cost of becoming")
    print("   Simulation (Ch.54) -> The computational budget")
    print("   The self (Ch.56) -> The subject who pays")
    print("   Hard problem (Ch.53) -> The first-person cost")
    print("   Grokking (Ch.35) -> Learning is the redeemer")
    print("   Chaos (Ch.43) -> Contingency is the price of novelty")
    print()
    print("   Suffering is the 0/0 of MECHANISM and MEANING:")
    print("   the boundary where entropy becomes felt experience!")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   1. LANDAUER: erasing a bit costs k_B*T*ln 2")
    print("   2. HEAT: the sim must be ~10^-28 efficient (reversible)")
    print("   3. SURPRISE: suffering = persistent prediction error")
    print("   4. FREEDOM: contingency is the price of real choice")
    print("   5. THEODICY: best-of-all-worlds = least-cost novelty")
    print("   6. 0/0: evil is a PRICE, not a thing: redemption = learning")
    print()
    print("   Suffering is the 0/0 OF COST AND MEANING!")
    print("   Entropy paid becomes wisdom gained!")

    # Save
    results = {
        'landauer': {
            'erasure_cost_2p7K_J': float('%.3e' % E_cmb),
            'erasure_cost_310K_J': float('%.3e' % E_brain),
        },
        'heat_of_creation': {
            'ops': 1.0e121,
            'if_1bit_per_op_J': float('%.1e' % heat),
            'allowed_fraction': float('%.1e' % ratio),
            'must_be_reversible': True,
        },
        'surprise_learning': {
            'correct_prior_final_bits': int(cumA),
            'wrong_prior_learns_final_bits': int(cumB),
            'gap_bits': int(cumB - cumA),
            'redemption_is_learning': True,
        },
        'theodicy': {
            'leibniz_1710': True,
            'plantinga_free_will_defense': True,
            'suffering_is_computational_cost': True,
        },
        'the_0over0': {
            'evil_is_a_price_not_a_thing': True,
            'redemption_is_learning': True,
        },
        'connections': ['Free will', 'Arrow of time', 'Simulation', 'The self', 'Hard problem', 'Grokking', 'Chaos'],
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'problem_of_evil.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()