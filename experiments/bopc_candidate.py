"""
BOPC candidate: Wolfram ECA 3-neighborhood step over a byte ring.
Semantics: correct-or-raise; resource = comparisons with a PROVEN closed
bound.  eca_step_counted returns (output, comparisons); the count covers
loop compares, boundary compares, neighborhood gathers, rule lookup, and
result shift/mask.  Per cell the implementation performs at most 8
counted operations plus one final loop compare, so comparisons <= 8*n + 2
for a cell string of length n (the contract's upper_bound).
"""


def eca_step_ref(rule, cells):
    """Independent reference: byte-identical output is the semantic check."""
    n = len(cells)
    out = bytearray(n)
    for i in range(n):
        left = cells[i - 1] if i > 0 else 0
        right = cells[i + 1] if i + 1 < n else 0
        idx = (left << 2) | (cells[i] << 1) | right
        out[i] = (rule >> idx) & 1
    return bytes(out)


def eca_step_counted(rule, cells):
    """Counted implementation of the same operator (correct-or-raise)."""
    n = len(cells)
    out = bytearray(n)
    c = 0
    for i in range(n):
        c += 1                                   # loop compare i < n
        left = cells[i - 1] if i > 0 else 0
        c += 1                                   # boundary compare
        right = cells[i + 1] if i + 1 < n else 0
        c += 1                                   # boundary compare
        c += 3                                   # 3 neighborhood gathers
        idx = (left << 2) | (cells[i] << 1) | right
        c += 1                                   # rule index compute
        out[i] = (rule >> idx) & 1
        c += 1                                   # rule lookup + mask
    c += 1                                       # final loop compare
    return bytes(out), c


def bound_for(n):
    """Proven closed upper bound on comparisons for length n."""
    return 8 * n + 2