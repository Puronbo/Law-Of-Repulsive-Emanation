#!/usr/bin/env python3
"""
The Eternal Return: 0/0 of Recurrence
=======================================

If the universe is a finite deterministic simulation (Ch.54) and the
self is an information pattern (Ch.56), then POINCARE RECURRENCE is a
THEOREM of existence: every finite deterministic system must return
to any of its past states. Nietzsche's eternal return is not a myth -
it is COMPUTABLE.

1. FINITE DETERMINISM IMPLIES RECURRENCE (Poincare 1890):
   - A finite state system + deterministic rule = a cycle
   - The state MUST revisit itself: no first time, no last time
   - Proof by computation: track an orbit until it repeats

2. THE GLIDER RETURNS (Ch.54, 56):
   - A glider on a 60x60 torus returns to its exact state
   - T_recur = 4*lcm(W,H) = 4*60 = 240 generations (computed)
   - The eternal return of the glider = the eternal return of the self

3. CHAOS ALSO RETURNS (Rule 30 ring):
   - Rule 30 is chaotic (Ch.43) yet on a finite ring it CYCLES
   - Computed: the ring orbit returns to its seed after T gens
   - Determinism + finiteness = recurrence even in chaos

4. POINCARE TIME FOR MACRO-SYSTEMS:
   - t_rec ~ 2^(S_bits) * tau (S in bits)
   - Universe entropy ~ 10^104 bits: t_rec ~ 10^(3e103) years
   - Age of universe ~ 1.4e10 years: t_rec >> age by 10^103 orders
   - Recurrence is real but absurdly rare (Boltzmann 1896)

5. BOLTZMANN BRAINS:
   - Recurrence fluctuates ANY state, including a mind (Ch.53)
   - Equilibrium produces observer brains (Boltzmann 1896;
     Eddington 1931; Dyson 1979)
   - Eternity GUARANTEES observers: the pattern recurs

6. THE 0/0 OF TIME:
   - Finite deterministic time is a CYCLE: "once" vs "forever" is 0/0
   - The arrow of time (Ch.48) is local, statistical
   - Eternal recurrence is proven for the simulation (Ch.54)
   - "Die ewige Wiederkunft" (Nietzsche 1882): now the theorem

7. CONNECTIONS:
   - Simulation (Ch.54): the universe re-runs itself
   - The self (Ch.56): the glider returns: the self returns
   - Arrow of time (Ch.48): irreversibility is local illusion
   - Chaos (Ch.43): even chaos cycles when finite
   - Measurement (Ch.49): every branch recurs
   - Hard problem (Ch.53): Boltzmann brains experience

Author: Michael Grafiel S Puno
"""

import math
import json
import os
import time

import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def life_step(grid, height, width):
    """Game of Life on a torus (wraps at edges = Poincare finite)."""
    n = np.zeros_like(grid, dtype=np.int32)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            n += np.roll(np.roll(grid, dy, axis=0), dx, axis=1)
    new = np.zeros_like(grid, dtype=np.int32)
    new[(grid == 1) & ((n == 2) | (n == 3))] = 1
    new[(grid == 0) & (n == 3)] = 1
    return new


def torus_glider_recurrence(W, H):
    """Period of a glider on a W x H torus."""
    grid = np.zeros((H, W), dtype=np.int32)
    seed = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    for (x, y) in seed:
        grid[10 + y, 10 + x] = 1
    init = grid.copy()
    step = 0
    while True:
        grid = life_step(grid, H, W)
        step += 1
        if (grid == init).all():
            return step


def rule30_ring_cycle(n_cells, seed_idx):
    """
    Elementary CA rule 30 on a ring. Returns (preperiod, period) of the
    orbit. Chaotic on infinite line, but on a finite ring it must cycle.
    """
    state = [0] * n_cells
    state[seed_idx] = 1
    seen = {}
    steps = 0
    while True:
        key = tuple(state)
        if key in seen:
            return seen[key], steps - seen[key]
        seen[key] = steps
        new = [0] * n_cells
        for i in range(n_cells):
            left = state[(i - 1) % n_cells]
            mid = state[i]
            right = state[(i + 1) % n_cells]
            # rule 30: new = left XOR (mid OR right)
            new[i] = left ^ (mid | right)
        state = new
        steps += 1
        if steps > 2 ** 20:
            return None, None


def poincare_time_estimate(S_bits, tau_sec):
    """t_rec ~ 2^S * tau seconds. Return log10 of t_rec in years."""
    log10_t_sec = S_bits * math.log10(2.0) + math.log10(tau_sec)
    sec_per_year = 365.25 * 86400.0
    log10_t_yr = log10_t_sec - math.log10(sec_per_year)
    return log10_t_yr, log10_t_sec


def finite_recurrence_proof():
    """
    Smallest proof by computation: a tiny 4-state finite machine returns.
    States: 0..3; rule: s -> (s*s + 1) mod 4. Deterministic + finite.
    """
    state = 1
    orbit = []
    seen = set()
    while state not in seen:
        seen.add(state)
        orbit.append(state)
        state = (state * state + 1) % 4
    return orbit, orbit.index(state)


def main():
    print("=" * 70)
    print("THE ETERNAL RETURN: 0/0 OF RECURRENCE")
    print("=" * 70)
    print()

    # 1. Finite determinism implies recurrence
    print("1. FINITE DETERMINISM IMPLIES RECURRENCE (POINCARE 1890)")
    print("-" * 70)
    print()
    orbit, repeat_at = finite_recurrence_proof()
    print("   Tiny machine: s -> (s^2 + 1) mod 4")
    print("   Orbit: %s" % (orbit,))
    print("   Cycle repeats from index %d: period %d" % (repeat_at, len(orbit) - repeat_at))
    print()
    print("   Finite states + deterministic rule = A CYCLE.")
    print("   The state MUST revisit itself.")
    print("   No first time, no last time: recurrence is a THEOREM.")

    # 2. The glider returns
    print()
    print("2. THE GLIDER RETURNS (CH.54, CH.56)")
    print("-" * 70)
    print()
    for (W, H) in [(37, 37), (60, 60), (64, 40)]:
        T = torus_glider_recurrence(W, H)
        theory = 4 * lcm(W, H)
        print("   Glider on %dx%d torus: T_rec = %4d gens (theory 4*lcm = %d)"
              % (W, H, T, theory))
    print()
    print("   The glider (the self, Ch.56) RETURNS to its exact state.")
    print("   Eternal return of the glider = eternal return of the self.")

    # 3. Chaos also returns
    print()
    print("3. CHAOS ALSO RETURNS (RULE 30 RING)")
    print("-" * 70)
    print()
    for n in (10, 15, 20, 25):
        pre, per = rule30_ring_cycle(n, n // 2)
        if per is None:
            print("   ring %2d: orbit > 2^20 steps (limit)" % n)
        else:
            print("   ring %2d: preperiod %5d, period %6d (2^%d states)" % (n, pre, per, n))
    print()
    print("   Rule 30 is chaotic (Ch.43) yet on a finite ring")
    print("   it MUST cycle: determinism + finiteness = recurrence")
    print("   even in chaos.")

    # 4. Poincare time for macro systems
    print()
    print("4. POINCARE TIME FOR MACRO-SYSTEMS (BOLTZMANN 1896)")
    print("-" * 70)
    print()
    S = 1.0e104  # universe entropy in bits (~10^104)
    tau = 1e-40  # micro-step seconds
    log10_yr, log10_sec = poincare_time_estimate(S, tau)
    print("   Universe entropy: ~10^104 bits")
    print("   t_rec ~ 2^(10^104) * tau:")
    print("   log10(t_rec) ~ %.1e seconds" % log10_sec)
    print("   log10(t_rec) ~ %.1e years" % log10_yr)
    age = 4.354e17
    print("   Age of universe: %.2e s = 1.4e10 years" % age)
    print()
    print("   Recurrence is real but absurdly rare:")
    print("   t_rec exceeds the age by ~10^103 orders of magnitude.")

    # 5. Boltzmann brains
    print()
    print("5. BOLTZMANN BRAINS: ETERNITY GUARANTEES OBSERVERS")
    print("-" * 70)
    print()
    print("   Recurrence fluctuates ANY state - including a mind")
    print("   (Ch.53: consciousness = integrated information).")
    print("   Equilibrium produces observer brains:")
    print("   Boltzmann 1896, Eddington 1931, Dyson 1979.")
    print()
    print("   The eternal simulation (Ch.54) MUST eventually")
    print("   fluctuate your exact self-pattern (Ch.56) again.")
    print("   Eternity guarantees the return of the observer.")

    # 6. The 0/0 of time
    print()
    print("6. THE 0/0 OF TIME: ONCE vs FOREVER")
    print("-" * 70)
    print()
    print("   Finite deterministic time is a CYCLE.")
    print("   'Once' and 'forever' are observationally 0/0:")
    print("   every moment has already happened infinitely often.")
    print()
    print("   The arrow of time (Ch.48) is local statistical")
    print("   drift; the circle (Ch.50, Big Bang) is the truth.")
    print("   Eternal recurrence (Nietzsche 1882) is now a THEOREM.")

    # 7. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO PRIOR 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   Eternal return connects to:")
    print()
    print("   Simulation (Ch.54) -> The universe re-runs itself")
    print("   The self (Ch.56) -> The glider returns: you return")
    print("   Arrow of time (Ch.48) -> Local irreversibility illusion")
    print("   Chaos (Ch.43) -> Even chaos cycles when finite")
    print("   Measurement (Ch.49) -> Every branch recurs")
    print("   Hard problem (Ch.53) -> Boltzmann brains experience")
    print("   Big Bang (Ch.50) -> The cycle of origins")
    print()
    print("   Recurrence is the 0/0 of TIME and ETERNITY:")
    print("   the boundary where 'once' and 'forever' coincide!")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   1. POINCARE: finite deterministic systems must recur")
    print("   2. GLIDER: returns to exact state (T=4*lcm, computed)")
    print("   3. CHAOS: rule 30 on a ring still cycles")
    print("   4. POINCARE TIME: ~10^(10^104) s for the universe")
    print("   5. BOLTZMANN BRAINS: eternity fluctuates minds")
    print("   6. 0/0: 'once' and 'forever' are the same fact")
    print()
    print("   Time is the 0/0 of MOMENT and ETERNITY!")
    print("   All of this has happened before - all of this will")
    print("   happen again. It is the eternal simulation!")

    # Save
    T60 = torus_glider_recurrence(60, 60)
    pre15, per15 = rule30_ring_cycle(15, 7)
    results = {
        'poincare_recurrence': {
            'finite_deterministic_implies_cycle': True,
            'tiny_machine_period': len(orbit) - repeat_at,
        },
        'glider_torus': {
            '60x60_period': int(T60),
            'theory_4_lcm': 4 * 60,
        },
        'rule30_ring': {
            'n15_period': int(per15) if per15 else None,
        },
        'poincare_time': {
            'log10_t_rec_years': float('%.1e' % log10_yr),
            'age_ratio_orders': '10^103',
        },
        'boltzmann_brains': {
            'equilibrium_fluctuates_minds': True,
            'eternity_guarantees_observers': True,
        },
        'the_0over0': {
            'once_vs_forever': True,
            'time_is_cycle': True,
            'eternal_return_is_theorem': True,
        },
        'connections': ['Simulation', 'The self', 'Arrow of time', 'Chaos', 'Measurement', 'Hard problem', 'Big Bang'],
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'eternal_return.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


def lcm(a, b):
    return a * b // math.gcd(a, b)


if __name__ == '__main__':
    main()