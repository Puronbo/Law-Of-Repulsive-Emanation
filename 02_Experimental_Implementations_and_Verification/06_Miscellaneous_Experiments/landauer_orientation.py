"""Landauer bound and the register's orientation sign (structural, NOT physical).

Deterministic, stdlib-only structural note. It records two facts and their
*structural* correspondence -- it makes no physical claim and touches no
Millennium problem (see the scope boundary
05_Documentation_and_Research_Specifications/05_Complete_Framework_Documentation/WHAT_THIS_DOES_NOT_PROVE.md).

Fact 1 (Landauer, 1961). Erasing one bit at temperature T dissipates at least
    E_bit = k_B * T * ln 2
joules. The discrete quantum of the cost is ln 2.

Fact 2 (the register, cards C10/C11, machine-checked). For a geometric content
orbit with multiplier r, the log-growth is log r and the orientation is its sign:
    r <= 1  <=>  log r <= 0  <=>  content non-increasing (dissipative, bounded)
    r >  1  <=>  log r >  0  <=>  content increasing   (repelling, unbounded)

Open bridge (NOT proved here): the claim that the Landauer quantum and the
register's orientation sign are one structure is OPEN, with a named missing
entity -- a register-to-thermodynamics map Phi; see
LANDAUER_BOUND_AND_THE_REGISTER.md. This script asserts only the two structural
facts above and does not prove the bridge.

Prints a single PASS marker on success.
"""

import math

K_B = 1.380649e-23  # Boltzmann constant, J/K (exact, SI 2019)


def landauer_energy(temperature_k):
    """Minimum energy to erase one bit at temperature T (Landauer, 1961)."""
    return K_B * temperature_k * math.log(2.0)


def orientation_side(r):
    """Register side: (log r, 'dissipative' | 'neutral' | 'repelling')."""
    lr = math.log(r)
    if lr < 0.0:
        return lr, "dissipative"
    if lr > 0.0:
        return lr, "repelling"
    return lr, "neutral"


def main():
    t = 300.0
    e_bit = landauer_energy(t)
    print("Landauer: erasing one bit at T = %.1f K costs at least %.6e J"
          % (t, e_bit))
    print("  discrete quantum of the cost = ln 2 = %.6f (nats)" % math.log(2.0))
    assert e_bit > 0.0

    print("Register orientation (cards C10/C11):")
    for r in (0.5, 1.0, 2.0):
        lr, side = orientation_side(r)
        print("  r = %4.1f -> log r = %+0.4f -> content %s (%s)"
              % (r, lr, "non-increasing" if lr <= 0.0 else "increasing", side))

    # Structural facts: mirror logGrowth_nonpos_of_dissipative / _pos.
    assert orientation_side(0.5)[0] < 0.0
    assert orientation_side(1.0)[0] == 0.0
    assert orientation_side(2.0)[0] > 0.0

    print("Open bridge (NOT proved here): a register<->thermodynamics map Phi is")
    print("the missing entity (see LANDAUER_BOUND_AND_THE_REGISTER.md); the two")
    print("structural facts above are asserted, the bridge is OPEN.")
    print("PASS")


if __name__ == "__main__":
    main()
