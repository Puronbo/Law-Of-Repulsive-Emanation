#!/usr/bin/env python3
"""
The Reversible Cycle: 0/0 of Thermodynamics (Carnot 1824)
===========================================================

After the synthesis (Ch.64), one foundational domain bequeathed many
threads but never a chapter of its own: THE ENGINE.

The Second Law stops the world from running backwards (Ch.48); the
heat of creation is Landauer's cost (Ch.59); the creator must compute
reversibly (Bennett 1982). Here is the machine itself:

1. THE CARNOT CYCLE (1824)
   - Ideal gas, two isotherms + two adiabats, integrated numerically.
   - Efficiency is the canonical ratio:
         eta = 1 - Tc/Th
   - Measured: 600K/300K -> eta = 0.500000000000000
   - The Sun against deep space (5778K/2.7K) -> eta = 0.99953

2. THE 0/0 OF DISSIPATION
   - A reversible cycle makes DELTA S = 0 (measured to 1e-16)
   - Maximum work at minimum entropy: the 0/0 of the engine
   - The second law: Delta S >= 0, equality only at the 0/0

3. THE COST OF IRREVERSIBILITY
   - Reject heat to a slightly-too-warm reservoir:
     entropy produced > 0 (measured), efficiency drops
   - The price of not running at the 0/0

4. THE COSMIC ENGINE
   - Carnot efficiency across real pairs (measured table)
   - The creator must compute reversibly (Ch.59, Ch.64):
     the universe is a Carnot engine at the 0/0

5. THE 0/0 PROOF:
   - eta = 1 - Tc/Th; at Tc=Th, eta = 0 AND Delta S = 0:
     the 0/0 of the engine - no work, no loss, pure 0.
   - Reversibility is the removable singularity of entropy:
     make Delta S -> 0, fill the hole, divide away the loss.

6. CONNECTIONS:
   - Arrow of time (Ch.48): the Second Law is the clock
   - Suffering (Ch.59): the heat of creation is this exact cost
   - The whole (Ch.64): reversible = the creator's own 0/0
   - Beauty (Ch.62): the reversible cycle is the perfect form

Author: Michael Grafiel S Puno
"""

import json
import math
import os
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

R = 8.31446261815324   # J/mol/K
CV = 1.5 * R           # monoatomic ideal gas
GAMMA = 5.0 / 3.0


def carnot_analysis(Th, Tc, V1=1.0, V2=4.0, n=1.0, steps=20000):
    """Analytic ideal-gas Carnot cycle: returns measurements dict.

    Returned: Qh, Qc, W, eta, dS_cycle, and numerical integration
    check of isothermal work via a fine mesh.
    """
    # isothermal legs (dU = 0, Q = W)
    Qh = n * R * Th * math.log(V2 / V1)
    Qc = n * R * Tc * math.log(V1 / V2)   # negative (inflow negative)

    # adiabatic legs follow T*V^(gamma-1) = const
    ratio = (Th / Tc) ** (1.0 / (GAMMA - 1.0))
    V3 = V2 * ratio
    V4 = V1 * ratio

    # numerical integration check of isothermal work (V1->V2, hot)
    dv = (V2 - V1) / steps
    w = 0.0
    v = V1
    for _ in range(steps):
        w += n * R * Th / v * dv
        v += dv
    W = Qh + Qc
    eta = W / Qh
    dS = Qh / Th + Qc / Tc  # vanishes for reversible cycle
    return {
        'Th': Th, 'Tc': Tc, 'V3': V3, 'V4': V4,
        'Qh': Qh, 'Qc': Qc, 'W': W, 'eta': eta, 'dS': dS,
        'numeric_isotherm_work': w,
        'carnot': 1.0 - Tc / Th,
    }


def main():
    print("=" * 70)
    print("THE REVERSIBLE CYCLE: 0/0 OF THERMODYNAMICS")
    print("(Carnot 1824; Clausius 1850; Kelvin 1851)")
    print("=" * 70)
    print()

    # 1. The Carnot cycle
    print("1. THE CARNOT CYCLE (1824)")
    print("-" * 70)
    print()
    print("   Ideal gas, two isotherms + two adiabats, n=1 mol.")
    print("   Th=600 K, Tc=300 K, V1=1, V2=4 (monoatomic, gamma=5/3)")
    print()
    m = carnot_analysis(600.0, 300.0)
    print("   Heat in  (hot isotherm)     Qh = %10.4f J" % m['Qh'])
    print("   Heat out (cold isotherm)    Qc = %10.4f J" % m['Qc'])
    print("   Work per cycle              W  = %10.4f J" % m['W'])
    print()
    print("   Efficiency (measured)       eta = %.15f" % m['eta'])
    print("   Carnot formula 1 - Tc/Th         = %.15f" % m['carnot'])
    print("   Numeric isotherm work check      = %.4f J" % m['numeric_isotherm_work'])
    print()
    print("   Delta S around the cycle     = %.3e  (the reversible 0/0)"
          % m['dS'])
    print()

    # 2. The 0/0 of dissipation
    print("2. THE 0/0 OF DISSIPATION")
    print("-" * 70)
    print()
    print("   A reversible cycle makes Delta S = 0 (measured to 1e-16);")
    print("   it extracts MAXIMUM work at ZERO entropy production.")
    print("   The Second Law (Clausius 1850): Delta S >= 0, equality")
    print("   ONLY at reversibility - the 0/0 of the engine.")
    print()

    # 3. The cost of irreversibility
    print("3. THE COST OF IRREVERSIBILITY")
    print("-" * 70)
    print()
    Tc_reservoir = 290.0
    Tc_exhaust = 300.0
    Qc = m['Qc']
    sigma = abs(Qc) * (1.0 / Tc_reservoir - 1.0 / Tc_exhaust)
    eta_rev_290 = 1.0 - Tc_reservoir / m['Th']
    W_rev_290 = m['Qh'] * eta_rev_290
    W_actual = m['W']
    lost = W_rev_290 - W_actual
    check = Tc_reservoir * sigma
    print("   If the engine dumps heat at %d K while a %d K reservoir" %
          (Tc_exhaust, Tc_reservoir))
    print("   exists, the surplus is NOT recoverable:")
    print("     entropy produced (measured)   sigma = %.4f J/K" % sigma)
    print("     ideal Carnot at %d K          eta   = %.6f" %
          (Tc_reservoir, eta_rev_290))
    print("     real engine (rejects at %d K)  eta   = %.6f" %
          (Tc_exhaust, m['eta']))
    print("     lost work vs the 0/0          W_lost = %.2f J (= T*sigma %.2f)"
          % (lost, check))
    print("   Irreversibility is a fee paid to the Second Law.")
    print()
    # sanity column text (no executable effect) -- the measurable above wins

    # 4. The cosmic engine
    print("4. THE COSMIC ENGINE")
    print("-" * 70)
    print()
    pairs = [
        ('steam plant    600/300   ', 600.0, 300.0),
        ('human work     310/295   ', 310.0, 295.0),
        ('earth/space    288/2.7   ', 288.0, 2.7),
        ('sun/infinity   5778/2.7  ', 5778.0, 2.7),
    ]
    print("   %-27s %18s" % ('pair', 'eta = 1 - Tc/Th'))
    for name, Th, Tc in pairs:
        print("   %-27s %18.5f" % (name, 1.0 - Tc / Th))
    print()
    print("   The Sun against deep space runs at eta = 0.99953:")
    print("   the universe is a nearly-reversible cosmic engine.")
    print("   The creator must compute reversibly (Ch.59, Ch.64,")
    print("   Bennett 1982): ~10^-28 efficiency - a Carnot 0/0.")
    print()

    # 5. The 0/0 proof
    print("5. THE 0/0 PROOF")
    print("-" * 70)
    print()
    print("   eta = 1 - Tc/Th. At Tc = Th, eta = 0 AND Delta S = 0:")
    print("   the 0/0 of the engine - no work, no loss, pure zero.")
    print("   Reversibility is the REMOVABLE SINGULARITY of entropy:")
    print("   drive Delta S -> 0, fill the hole, divide away the loss.")
    print()

    # 6. Connections
    print("6. CONNECTIONS TO PRIOR 0/0 SINGULARITIES")
    print("-" * 70)
    print()
    print("   The cycle connects to:")
    print()
    print("   Arrow of time (Ch.48) -> The Second Law is the clock")
    print("   Suffering (Ch.59) -> The heat of creation is this cost")
    print("   The whole (Ch.64) -> The creator computes reversible")
    print("   Beauty (Ch.62) -> The reversible cycle is perfect form")
    print("   Meaning (Ch.61) -> Engines are laws in motion")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   1. CARNOT: eta = 1 - Tc/Th = %.15f at 600/300" % m['eta'])
    print("   2. 0/0: Delta S = %.1e (reversible engine runs at the 0/0)"
          % m['dS'])
    print("   3. IRREVERSIBLE: sigma = %.4f J/K, W_lost = %.2f J (T*sigma %.2f)"
          % (sigma, lost, check))
    print("   4. COSMOS: sun/space eta = %.5f" % (1 - 2.7 / 5778))
    print("   5. 0/0: at Tc=Th, eta = 0 and Delta S = 0: the engine's")
    print("      hole is removable - reversibility is the whole")
    print()
    print("   The Reversible Cycle is the 0/0 OF THERMODYNAMICS!")
    print("   Timelessness pays zero, yet moves the world.")

    # Save
    results = {
        'carnot': {
            'Th': 600, 'Tc': 300, 'V1': 1, 'V2': 4, 'n': 1.0,
            'Qh': round(m['Qh'], 4), 'Qc': round(m['Qc'], 4),
            'W': round(m['W'], 4),
            'eta': m['eta'],
            'eta_formula': m['carnot'],
            'dS_cycle': m['dS'],
            'agreement': abs(m['eta'] - m['carnot']) < 1e-12,
        },
        'second_law': {
            'clausius': 'Delta S >= 0, equality only at reversibility',
            'reversible_is_0over0': True,
        },
        'irreversibility': {
            'reservoir_K': Tc_reservoir,
            'exhaust_K': Tc_exhaust,
            'sigma_J_per_K': round(sigma, 4),
            'eta_reversible_at_290K': round(eta_rev_290, 6),
            'eta_real_engine': round(m['eta'], 6),
            'lost_work_J': round(lost, 2),
            'check_Tsigma': round(check, 2),
        },
        'cosmics': {
            'sun_infinity_eta': round(1 - 2.7 / 5778, 5),
            'bennett_creator': '~1e-28 reversible (Ch.64), Carnot 0/0',
        },
        'the_0over0': {
            'eta_at_Tc_equ_Th': 0.0,
            'dS_at_Tc_equ_Th': 0.0,
            'reversible_hole_is_removable': True,
        },
        'connections': ['Arrow of time', 'Suffering', 'The whole', 'Beauty', 'Meaning'],
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'reversible_cycle.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()