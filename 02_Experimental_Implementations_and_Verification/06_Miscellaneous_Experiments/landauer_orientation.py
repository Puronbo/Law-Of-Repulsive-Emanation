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

Structural correspondence (NOT a physical identification): each is a discrete
cost with a direction -- a positive quantum (ln 2) and a sign (the side). The
register's orientation is that sign; the Landauer cost is the magnitude of one
crossing. This script asserts only the structural facts.

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

    print("Structural correspondence (NOT a physical identification):")
    print("  positive quantum (ln 2)  <=>  Landauer cost per bit")
    print("  direction sign(log r)    <=>  register orientation side")
    print("PASS")


if __name__ == "__main__":
    main()
