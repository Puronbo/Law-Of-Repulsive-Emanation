import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import RULES, SolitonECA  # noqa: E402


def ghost_step(rule, state):
    n = len(state)
    out = []
    for i in range(n):
        left = state[i - 1] if i > 0 else 0
        right = state[i + 1] if i < n - 1 else 0
        neighborhood = (left << 2) | (state[i] << 1) | right
        out.append((rule >> neighborhood) & 1)
    return out


def lcg():
    state = 98765431
    while True:
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        yield state


assert len(RULES) == 32
seed = lcg()
for rule in RULES:
    for width in (3, 4, 5, 6, 7, 8, 9):
        for _ in range(12):
            initial = [next(seed) & 1 for _ in range(width)]
            engine = SolitonECA(rule, width, initial)
            reference = list(initial)
            for _ in range(6):
                reference = ghost_step(rule, reference)
                assert list(engine.step()) == reference

# Rule 204 is identity: blocks and isolated cells keep position and value.
block = [0] * 19
for i in (5, 6, 7, 8):
    block[i] = 1
engine = SolitonECA(204, 19, block)
for _ in range(10):
    assert list(engine.step()) == block

# Complement twins swap black and white on the same configuration.
for rule in RULES:
    twin = 255 - rule
    state = (0, 1, 0, 1, 1, 0, 1)
    a = ghost_step(rule, list(state))
    b = ghost_step(twin, list(state))
    assert a == [1 - x for x in b]

print("eca engine validation passed")