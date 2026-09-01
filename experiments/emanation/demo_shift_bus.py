"""Demo: two well-separated packets share ONE lane on the verified 4-rule
shift bus. The rules are NOT linear (they are AND-NOT gates); lane-sharing
is valid here only because these packets evolve with disjoint supports.

Verification is in tests/test_shift_bus.py (24 tests, all green).
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", ".."))

import shift_bus as sb

W, T = 6000, 250
lane = 12  # right-bound +1

a = {1000, 1003, 1007}
b = {4000, 4004}

ma = sb.packet_bits(a, W)
mb = sb.packet_bits(b, W)

combined = sb.share_lanes(lane, [ma, mb], W, T)

rec_a = sb.recover(combined, lane, [mb], W, T)
rec_b = combined ^ sb.read(lane, ma, W, T)

ea = sb.evolve(lane, a, W, T)
eb = sb.evolve(lane, b, W, T)

print("one lane, rule 12 (+1/step), t =", T)
print("  packet A start:", sorted(a), " end:", sorted(ea))
print("  packet B start:", sorted(b), " end:", sorted(eb))
print("  recovered A == solo A :", rec_a == sb.packet_bits(ea, W))
print("  recovered B == solo B :", rec_b == sb.packet_bits(eb, W))
print("  total bits on lane    :", bin(combined).count('1'),
      "(2 packets, 3+2 bits, disjoint supports)")
print()
print("left lane check, rule 68 (-1/step):")
c = {2000 - 7}
ec = sb.evolve(68, c, W, 7)
print("  packet C start:", sorted(c), " after 7 steps:", sorted(ec),
      "(moved left by exactly 7)")
print()
print("Nonlinearity spot-check (rule 12 = left AND NOT center):")
import random
rng = random.Random(1)
W2, T2 = 40, 5
fails = 0
for _ in range(50):
    x = rng.getrandbits(W2); y = rng.getrandbits(W2)
    if sb.read(12, x ^ y, W2, T2) != (sb.read(12, x, W2, T2)
                                      ^ sb.read(12, y, W2, T2)):
        fails += 1
print("  superposition violations on dense configs: %d/50 "
      "(expect ~all; rules are NOT linear)" % fails)