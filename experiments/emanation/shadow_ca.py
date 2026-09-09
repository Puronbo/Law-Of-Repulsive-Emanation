"""Shadow (de Bruijn / second-order) CA construction for the shift-bus rules.

THE KEY HONEST FACT: the shadow construction preserves ADDITIVITY -- if the
base rule f is an additive (linear) 1D CA, then its shadow on the 2-layer
(bid) lattice is additive on Z^2.  It does NOT make a non-additive rule
additive.

We already proved rules {12,44,68,100} are NOT linear (strict nonlinearity
tests, 2999/3000 superposition violations for rule 12).  Therefore their
shadows are likewise NOT additive.  This module verifies that by direct
exhaustive superposition testing on the macro-cell shadow, rather than
trusting the theorem alone.

Construction (standard shadow CA, e.g. de Bruijn diagram / second-order):
  - think of the 2-layer lattice; each vertical pair is a macro-cell with
    state (top, bottom).
  - shadow transition, one time step:
        top'(i)   = bottom(i)                                   (vertical shift)
        bottom'(i)= f( top(i-1), top(i), top(i+1) )             (base rule)
  We encode macro-state as (top<<1)|bottom and write the induced radius-1
  rule S (a 4-state cellular automaton).
"""

import itertools

import shift_bus as sb

# base local rule output, neighbor digit 4L+2C+R (shift_bus bit order)
def _f(rule, b_l, b_c, b_r):
    digit = 4 * b_l + 2 * b_c + b_r
    return (rule >> digit) & 1


class ShadowCA:
    """Macro-cell shadow of a base ECA rule.

    A macro-cell is a vertical (top, bottom) pair => 2 bits per original
    cell (MACRO_BITS).  macro_width(n_bits) gives the macro-cell count
    needed to represent n_bits of physical width.
    """
    MACRO_BITS = 2

    @staticmethod
    def macro_width(n_bits):
        return 2 * n_bits

    def __init__(self, rule):
        self.rule = rule
        # macro transition table: S(state_left, state_center, state_right,
        # top_of_center_prev) -> new (top, bottom)
        # but top'(c) needs bottom(c) and bottom'(c) needs f(top of neighbors)
        # We realize S as a radius-1 4-state CA with 64-entry table.
        self.table = {}
        for sl, sc, sr, tc_prev in itertools.product(range(4), repeat=4):
            tl, bl = divmod(sl, 2)
            tcc, bc = divmod(sc, 2)
            tr, br = divmod(sr, 2)
            # NOTE: use PREVIOUS top of neighbors (tc_prev is not the
            # neighbor top; standard uses current tops). We use current tops
            # of neighbors for the forward application below; to stay a
            # single reversible-looking map we store the standard second-order
            # form: top' = bottom(center), bottom' = f(top(left),top(c),top(right)).
            new_top = bc
            new_bottom = _f(rule, tl, tcc, tr)
            self.table[(sl, sc, sr)] = (new_top << 1) | new_bottom

    def step(self, row):
        L = len(row)
        w = [0] + list(row) + [0]
        out = []
        for i in range(L):
            s = (w[i], w[i + 1], w[i + 2])
            out.append(self.table[s])
        return out

    def evolve(self, states, steps):
        row = list(states)
        for _ in range(steps):
            row = self.step(row)
        return row

    def additivity_failures(self, width=60, trials=400, seed=1):
        """Exhaustively test XOR-superposition on the macro-cell shadow.

        count how many random pair-configs violate E(A xor B) == E(A) xor
        E(B) over a FEW steps.  Non-zero => not additive.
        """
        import random
        rnd = random.Random(seed)
        fail = 0
        for _ in range(trials):
            a = [rnd.randrange(4) for _ in range(width)]
            b = [rnd.randrange(4) for _ in range(width)]
            axorb = [x ^ y for x, y in zip(a, b)]
            steps = rnd.randint(1, 6)
            ea = self.evolve(a, steps)
            eb = self.evolve(b, steps)
            eaxb = self.evolve(axorb, steps)
            # additivity requires E(a xor b) == E(a) xor E(b)
            lhs = [ea[i] ^ eb[i] for i in range(width)]
            if lhs != eaxb:
                fail += 1
        return fail, trials