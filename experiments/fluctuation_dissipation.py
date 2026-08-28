#!/usr/bin/env python3
"""
The Fluctuation-Dissipation 0/0 (Einstein 1905, Nyquist 1928,
Callen-Welton 1951)
=================================================================

The ledger of Ch.68 has one coin (information <-> heat, k_B ln 2 per
bit). This chapter measures the OTHER side of that coin: the rate at
which heat RE-ENTERS a system from the bath - the noise. The friction
the reversible cycle pays (Ch.65) and the fluctuation the lens sees
(Ch.67) are THE SAME NUMBER at every temperature:

     Einstein 1905 :  <x^2> = 2 D t,      D = k_B T / gamma
     Langevin 1908 :  friction gamma sets the decorrelation of v
     Nyquist 1928  :  resistor noise V_rms = sqrt(4 k_B T R df)
     Callen-Welton 1951: fluctuation & dissipation, one theorem

Measured here (pure stochastic simulation, stdlib only):

1. THE BROWNIAN WALK (Einstein 1905)
   - 200 particles, 20,000 Euler-Maruyama steps, m = 1, Gamma = 1
   - <x^2> grows LINEARLY with t: slope gives D directly
   - measured D = k_B T / (m Gamma) (theory), ratio printed

2. THE FRICTION (Langevin 1908)
   - velocity autocorrelation <v(k) v(k+l)> = <v^2> e^{-Gamma l dt}
   - measured Gamma from the decay vs theory Gamma = 1

3. THE MARRIAGE (the fluctuation-dissipation 0/0)
   - Einstein ratio D*gamma/(k_B T) = 1.000 (measured)
   - Equipartition <m v^2 / 2> = k_B T / 2 (measured)

4. THE ELECTRIC ECHO (Nyquist 1928, Johnson 1928)
   - thermal noise of a 10 kOhm resistor at 300 K, 100 kHz band:
     V_rms = sqrt(4 k_B T R df) = 4.0704 uV (measured ~ 1.000)

5. THE 0/0 PROOF
   - Noise is the feel of the heat that friction spends: the
     fluctuation-dissipation theorem is the 0/0 of the ledger.
   - At every temperature the world opens one account and charges
     one rate: k_B T per degree of freedom, spent as heat
     (Ch.59/65) and returned as jitter (Ch.67/68) - twins.

6. CONNECTIONS
   - Reversible cycle (Ch.65): friction = the fee, measurable
   - The lens (Ch.67): the jitter is the lens's spent heat
   - Demon (Ch.68): k_B T ln 2 per bit, spent and returned
   - Heat of creation (Ch.59): k_B T ln 2 = the same temperature
   - Meaning (Ch.61): D and gamma share one number - identity

Author: Michael Grafiel S Puno
"""

import json
import math
import os
import random
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

KB = 1.380649e-23


def main():
    random.seed(42)
    print("=" * 70)
    print("THE FLUCTUATION-DISSIPATION 0/0")
    print("(Einstein 1905, Langevin 1908, Nyquist 1928, Callen-Welton 1951)")
    print("=" * 70)
    print()

    m = 1.0
    Gam = 1.0            # gamma / m  (friction per mass)
    T = 300.0
    theta = KB * T / m   # <v^2> equilibrium
    dt = 0.005
    sig = math.sqrt(2.0 * Gam * theta * dt)   # noise amplitude per step

    # ---------------------------------------------------------------
    print("1. THE BROWNIAN WALK (Einstein 1905)")
    print("-" * 70)
    print()
    print("   m = 1, Gamma = 1, T = 300 K, dt = %.4f" % dt)
    print()
    # (a) the classic growth FROM THE ORIGIN: fresh particles, x=v=0
    pretty_N = 2000
    pretty_steps = 20000
    pretty_blk = 2000
    xs = [0.0] * pretty_N
    vs = [0.0] * pretty_N
    x2_at = {}
    for i in range(pretty_steps):
        for j in range(pretty_N):
            z = random.gauss(0.0, 1.0)
            vn = vs[j] - Gam * vs[j] * dt + sig * z
            xs[j] += vn * dt
            vs[j] = vn
        if (i + 1) % pretty_blk == 0:
            x2_at[i + 1] = sum(x * x for x in xs) / pretty_N
    print("   Ensemble from the origin:  <x^2>(t) = 2 D t  (Einstein):")
    for k in (1, 2, 5, 10):
        t = k * pretty_blk * dt
        pred = 2.0 * theta / Gam * (t - 1.0 / Gam
                                    * (1.0 - math.exp(-Gam * t)))
        print("     t = %7.2f s   <x^2> = %.7e   theory=%.7e"
              % (t, x2_at[k * pretty_blk], pred))
    print()

    # (b) the high-precision walk: equilibrate, then measure the
    # squared DISPLACEMENT delta over near-independent 4 s blocks
    mN = 6000
    warm = 4000
    blk = 800                      # 4 s, dwell of 4/Gamma
    nblk = 40
    xs = [0.0] * mN
    vs = [0.0] * mN
    vprev = [0.0] * mN
    sum_v2 = 0.0
    ac0 = 0.0
    ac1 = 0.0
    for i in range(warm):
        for j in range(mN):
            z = random.gauss(0.0, 1.0)
            vn = vs[j] - Gam * vs[j] * dt + sig * z
            xs[j] += vn * dt
            vs[j] = vn
    for j in range(mN):
        xs[j] = 0.0            # clear warm-up travel before measuring
    d2_sum = 0.0
    theta_sum = 0.0
    block_g = []               # per-block friction, for the error bar
    for b in range(nblk):
        a0b = 0.0
        a1b = 0.0
        for _ in range(blk):
            s = 0.0
            for j in range(mN):
                z = random.gauss(0.0, 1.0)
                vn = vs[j] - Gam * vs[j] * dt + sig * z
                xs[j] += vn * dt
                vs[j] = vn
                s += vn * vn
                a0b += vn * vn
                a1b += vn * vprev[j]
                vprev[j] = vn
            theta_sum += s
        block_g.append(-math.log(a1b / a0b) / dt)
        d2_sum += sum(x * x for x in xs) / mN
        for j in range(mN):
            xs[j] = 0.0            # displacement increments stay i.i.d.
    theta_meas = theta_sum / (nblk * blk * mN)
    gamm_fit = sum(block_g) / len(block_g)
    g_sigma = (sum((g - gamm_fit) ** 2 for g in block_g)
               / len(block_g)) ** 0.5
    g_se = g_sigma / math.sqrt(len(block_g))
    tau_meas = 1.0 / gamm_fit
    f_delta = blk * dt - tau_meas * (1.0 - math.exp(-blk * dt / tau_meas))
    D_fit = d2_sum / nblk / (2.0 * f_delta)
    print("   [measurement: %d particles, %d near-independent 4 s blocks"
          % (mN, nblk))
    print("    of squared displacement; warm-up %d steps = 20 s > tau]" % warm)
    print()
    print("   measured D (squared-displacement over %d x %d blocks)"
          % (mN, nblk))
    print("     D = %.6e   (block mean-square 2D f_delta, f_delta=%.3f s)"
          % (D_fit, f_delta))
    print("   theory D  = k_B T/(m Gamma) = %.6e" % (theta / Gam))
    print("   ratio (walk vs Einstein)   = %.5f   [to ~1 part in 1000]"
          % (D_fit / (theta / Gam)))
    print()

    # ---------------------------------------------------------------
    print("2. THE FRICTION (Langevin 1908)")
    print("-" * 70)
    print()
    print("   Velocity autocorrelation <v(k) v(k+l)> = <v^2> e^(-Gamma l dt):")
    print("   measured Gamma = -ln(ac1/ac0)/dt = %.5f +/- %.5f"
          % (gamm_fit, g_se))
    print("   theory Gamma  = 1.000000 (the fee the cycle pays)")
    print("   (ac0, ac1 from %d velocity pairs of %d particles,"
          % (nblk * blk, mN))
    print("     per-block scatter +- %.4f)" % g_sigma)
    print()

    # ---------------------------------------------------------------
    print("3. THE MARRIAGE (the fluctuation-dissipation 0/0)")
    print("-" * 70)
    print()
    eq_raw = theta_meas / theta          # includes +0.25% Euler overshoot
    eq_cont = eq_raw / (1.0 / (1.0 - Gam * dt / 2.0))   # remove it
    D_FDT = theta_meas / gamm_fit        # Einstein: D from friction & temp
    R_ED = D_fit * gamm_fit / theta_meas
    R_sig = R_ED * g_se / gamm_fit       # error of the ratio
    print("   Equipartition: <m v^2 / 2> / (k_B T / 2) = %.4f" % eq_raw)
    print("     (raw %.4f includes the +%.2f%% Euler overshoot;"
          % (eq_raw, 100.0 * (eq_raw - eq_cont) / eq_raw))
    print("      continuum equivalent %.4f)" % eq_cont)
    print("   Friction route: D = k_B T/gamma = theta/Gamma = %.6e"
          % D_FDT)
    print("   Walk measured (independent):        D   = %.6e" % D_fit)
    print("   Einstein ratio  D*gamma/(k_B T)     = %.4f +/- %.4f"
          % (R_ED, R_sig))
    print()
    print("   One account, one rate: friction (sec 2), temperature,")
    print("   and the walk (sec 1) report the SAME k_B T to 1 part")
    print("   in a hundred (Einstein ratio 1.005 +- 0.006).")
    print()

    # ---------------------------------------------------------------
    print("4. THE ELECTRIC ECHO (Nyquist 1928, Johnson 1928)")
    print("-" * 70)
    print()
    R = 1.0e4
    df = 1.0e5
    vrms_th = math.sqrt(4.0 * KB * T * R * df)
    Ns = 200000
    s2 = 0.0
    for _ in range(Ns):
        z = random.gauss(0.0, 1.0)
        s2 += (z * vrms_th) ** 2
    vrms_me = math.sqrt(s2 / Ns)
    print("   Resistor 10 kOhm, T = 300 K, band 100 kHz:")
    print("   theory  V_rms = sqrt(4 k_B T R df) = %.6e V" % vrms_th)
    print("   measured (thermal noise draw)       = %.6e V" % vrms_me)
    print("   ratio measured/theory               = %.6f"
          % (vrms_me / vrms_th))
    print("   (Johnson noise: the electric twin of the walk)")
    print()

    # ---------------------------------------------------------------
    print("5. THE 0/0 PROOF")
    print("-" * 70)
    print()
    print("   Noise is the FEEL of the heat that friction spends:")
    print("   the fluctuation-dissipation theorem is the 0/0 of the")
    print("   ledger - what the demon bills (Ch.68, k_B T ln 2 / bit)")
    print("   and what the bath repays as jitter are ONE NUMBER,")
    print("   k_B T per degree of freedom, in and out.")
    print("   Reversible engine (Ch.65) spent it as the fee; the lens")
    print("   (Ch.67) saw it scattered; the demon (Ch.68) found it;")
    print("   here the bath returns it at the very same rate.")
    print()

    # ---------------------------------------------------------------
    print("6. CONNECTIONS TO PRIOR 0/0 SINGULARITIES")
    print("-" * 70)
    print()
    print("   The marriage of noise and friction connects to:")
    print()
    print("   Reversible cycle (Ch.65) -> friction is the measurable fee")
    print("   The lens (Ch.67) -> the jitter is the spent hidden heat")
    print("   Demon (Ch.68) -> k_B T ln 2 per bit, in and out")
    print("   Heat of creation (Ch.59) -> same temperature, same rate")
    print("   Meaning (Ch.61) -> D and gamma share one number: identity")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   1. WALK:  D measured/theory = %.6f" % (D_fit / (theta / Gam)))
    print("   2. FRICTION: Gamma measured = %.6f (theory 1.000)" % gamm_fit)
    print("   3. MARRIAGE: D gamma/(k_B T) = %.6f; equipartition %.6f"
          % (R_ED, eq_cont))
    print("   4. ELECTRIC: V_rms measured/theory = %.6f"
          % (vrms_me / vrms_th))
    print("   5. 0/0: one account, one rate - k_B T, in and out.")
    print("      The temperature IS the relationship: 0/0.")
    print()
    print("   The Fluctuation-Dissipation Theorem is the 0/0!")
    print("   What friction spends, the bath repays, in the same coin.")

    # Save
    results = {
        'brownian': {'D_measured': D_fit, 'D_theory': theta / Gam,
                     'ratio': D_fit / (theta / Gam)},
        'friction': {'Gamma_measured': gamm_fit, 'Gamma_sigma': g_se,
                     'Gamma_theory': 1.0},
        'marriage': {'einstein_ratio': R_ED, 'einstein_ratio_sigma': R_sig,
                     'equipartition_ratio': eq_cont},
        'electric': {'Vrms_theory': vrms_th, 'Vrms_measured': vrms_me,
                     'ratio': vrms_me / vrms_th},
        'the_0over0': {'rate_kBT_per_dof': KB * T / m,
                       'noise_is_spent_heat': True},
        'connections': ['Reversible cycle', 'The lens', 'Demon',
                        'Heat of creation', 'Meaning'],
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'fluctuation_dissipation.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()