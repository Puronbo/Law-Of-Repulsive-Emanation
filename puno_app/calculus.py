"""The Puno Calculus: a small exact + numeric calculus engine.

The engine is the shared core for the three deliverables:

1. ``puno_app.calculus_server`` -- browser dashboard (derive / integrate /
   antiderivative / definitive constant against the L.O.R.E. thesis).
2. ``puno-calculus`` CLI -- the same library surface from a terminal.
3. ``puno_app.constant_explorer`` -- prints the definitive constants that the
   project's own assets determine (C0 = V(q0) = H(q0,0), the fold mirror
   area, the epoch_0d divisor pair, the prime-count datum, the quantum E0).

L.O.R.E. thesis (the "definitive constant"): the antiderivative
``F(x) = \\int f(x) dx + C`` only has an *arbitrary* constant while the
initial condition is unknown.  When the initial condition ``(q0, V(q0))`` is
measured -- and the project measures it on the Poincare disk, see
``Universals.hamiltonian_flow.repulsion_loss`` -- the constant collapses to
``C0 = V(q0) - F(q0)``.  A definite integral is thus a constant, never a
family.

Expressions are nested tuples:

    ("num", v)   ("var",)   ("add", a, b)  ("sub", a, b)  ("mul", a, b)
    ("div", a, b) ("pow", a, b) ("sin", e) ("cos", e) ("tan", e)
    ("exp", e) ("log", e) ("sqrt", e) ("atan", e)

Dependencies: stdlib + numpy (the latter only for the asset-backed measure).
"""

from __future__ import annotations

import math
import os
import re
import sys
from typing import Optional, Tuple

# --------------------------------------------------------------------------- #
# Expression helpers
# --------------------------------------------------------------------------- #

_NUM = "num"
_VAR = "var"


def num(v: float):
    return (_NUM, float(v))


def var():
    return (_VAR,)


def _is_num(e) -> bool:
    return isinstance(e, tuple) and e[0] == _NUM


def _is_var(e) -> bool:
    return e == (_VAR,)


def _is_const(e) -> bool:
    """True when the expression has no x (a pure number, euler, pi, ...)."""
    if _is_num(e):
        return True
    if _is_var(e):
        return False
    if e[0] == "pi" or e[0] == "euler":
        return True
    return all(_is_const(a) for a in e[1:]) and bool(e[1:])


def _coef(e):
    """Split ``k * base`` -> (k, base); anything else -> (1, e)."""
    if isinstance(e, tuple) and e[0] == "mul" and _is_num(e[1]):
        return float(e[1][1]), e[2]
    return 1.0, e


# --------------------------------------------------------------------------- #
# Simplification
# --------------------------------------------------------------------------- #

def simplify(e):
    """Constant folding plus a few exact algebraic rules."""
    if _is_num(e) or _is_var(e):
        return e
    if e[0] in ("pi", "euler"):
        return e
    op = e[0]
    if op in ("sin", "cos", "tan", "exp", "log", "sqrt", "atan"):
        arg = simplify(e[1])
        if op == "log" and _is_num(arg) and float(arg[1]) == 1.0:
            return num(0)
        if op == "log" and _is_num(arg) and float(arg[1]) == math.e:
            return num(1)
        if op == "sin" and _is_num(arg) and float(arg[1]) == 0.0:
            return num(0)
        if op == "cos" and _is_num(arg) and float(arg[1]) == 0.0:
            return num(1)
        if op == "exp" and _is_num(arg) and float(arg[1]) == 0.0:
            return num(1)
        if op == "tan" and _is_num(arg) and float(arg[1]) == 0.0:
            return num(0)
        if op == "sqrt" and _is_num(arg):
            v = math.sqrt(float(arg[1]))
            return num(v)
        return (op, arg)

    a, b = simplify(e[1]), simplify(e[2])
    an = a[1] if _is_num(a) else None
    bn = b[1] if _is_num(b) else None

    if op == "add":
        if an is not None and bn is not None:
            return num(an + bn)
        if _is_num(a) and an == 0.0:
            return b
        if _is_num(b) and bn == 0.0:
            return a
        if a == b:
            return simplify(("mul", num(2), a))
        return ("add", a, b)

    if op == "sub":
        if an is not None and bn is not None:
            return num(an - bn)
        if a == b:
            return num(0)
        if _is_num(b) and bn == 0.0:
            return a
        return ("sub", a, b)

    if op == "mul":
        if an is not None and bn is not None:
            return num(an * bn)
        if (an is not None and an == 0.0) or (bn is not None and bn == 0.0):
            return num(0)
        if an is not None and an == 1.0:
            return b
        if bn is not None and bn == 1.0:
            return a
        if a == b:
            return simplify(("pow", a, num(2)))
        if _is_num(a) and b[0] == "div":          # c * (u/v) -> (c*u)/v
            return simplify(("div", ("mul", a, b[1]), b[2]))
        if _is_num(b) and a[0] == "div":
            return simplify(("div", ("mul", b, a[1]), a[2]))
        if _is_num(a):
            k, inner = _coef(b)
            if isinstance(b, tuple) and b[0] == "mul" and _is_num(b[1]):
                return simplify(("mul", num(an * float(b[1][1])), b[2]))
            if _is_num(inner):
                return num(an * float(inner[1]))
        return ("mul", a, b)

    if op == "div":
        if an is not None and bn is not None:
            if bn == 0.0:
                return ("div", a, b)
            return num(an / bn)
        if a == b:
            return num(1)
        if bn is not None and bn == 1.0:
            return a
        if an is not None and an == 0.0:
            return num(0)
        if bn is not None and a[0] == "mul" and _is_num(a[1]):
            return simplify(("mul", num(float(a[1][1]) / bn), a[2]))
        return ("div", a, b)

    if op == "pow":
        if bn is not None and bn == 0.0:
            return num(1)
        if bn is not None and bn == 1.0:
            return a
        if an is not None and bn is not None:
            return num(an ** bn)
        return ("pow", a, b)

    raise ValueError("unknown operator %r" % (op,))


# --------------------------------------------------------------------------- #
# Parser
# --------------------------------------------------------------------------- #

_TOKEN_RE = re.compile(r"""
    (?P<num>\d+\.\d+(?:[eE][+-]?\d+)?|\d+[eE][+-]?\d+|\d+)
  | (?P<pi>pi)
  | (?P<euler>e(?!xp))            # 'e' = Euler constant, not the 'exp' token
  | (?P<fun>sin|cos|tan|exp|log|sqrt|atan)
  | (?P<var>x)
  | (?P<op>[+\-*/^()])
""", re.VERBOSE)


class _Token:
    __slots__ = ("kind", "value")

    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):  # pragma: no cover - debug aid
        return "Token(%s, %r)" % (self.kind, self.value)


def _tokenize(s: str):
    toks = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch.isspace():
            i += 1
            continue
        m = _TOKEN_RE.match(s, i)
        if not m:
            raise ValueError("cannot parse character %r at offset %d" % (ch, i))
        kind = m.lastgroup
        val = m.group()
        if kind == "num":
            toks.append(_Token("num", float(val)))
        elif kind == "pi":
            toks.append(_Token("pi", None))
        elif kind == "euler":
            toks.append(_Token("euler", None))
        elif kind == "fun":
            toks.append(_Token("fun", val))
        elif kind == "var":
            toks.append(_Token("var", None))
        else:
            toks.append(_Token("op", val))
        i = m.end()
    toks.append(_Token("eof", None))
    return toks


class _Parser:
    def __init__(self, toks):
        self.toks = toks
        self.pos = 0

    def _peek(self):
        return self.toks[self.pos]

    def _next(self):
        t = self.toks[self.pos]
        self.pos += 1
        return t

    def _expect(self, value):
        t = self._next()
        if t.kind != "op" or t.value != value:
            raise ValueError("expected %r but got %s" % (value, t))
        return t

    def parse(self):
        e = self._expr()
        if self._peek().kind != "eof":
            raise ValueError("trailing input after expression")
        return e

    def _expr(self):
        e = self._term()
        while True:
            t = self._peek()
            if t.kind == "op" and t.value == "+":
                self._next()
                e = ("add", e, self._term())
            elif t.kind == "op" and t.value == "-":
                self._next()
                e = ("sub", e, self._term())
            else:
                return e

    def _term(self):
        e = self._unary()
        while True:
            t = self._peek()
            if t.kind == "op" and t.value == "*":
                self._next()
                e = ("mul", e, self._unary())
            elif t.kind == "op" and t.value == "/":
                self._next()
                e = ("div", e, self._unary())
            else:
                return e

    def _unary(self):
        t = self._peek()
        if t.kind == "op" and t.value == "-":
            self._next()
            return ("mul", num(-1), self._unary())
        if t.kind == "op" and t.value == "+":
            self._next()
            return self._unary()
        return self._power()

    def _power(self):
        base = self._primary()
        t = self._peek()
        if t.kind == "op" and t.value == "^":
            self._next()
            exp = self._unary()
            return ("pow", base, exp)
        return base

    def _primary(self):
        t = self._next()
        if t.kind == "num":
            return num(t.value)
        if t.kind == "var":
            return (_VAR,)
        if t.kind == "pi":
            return ("pi",)
        if t.kind == "euler":
            return ("euler",)
        if t.kind == "fun":
            self._expect("(")
            e = self._expr()
            self._expect(")")
            return (t.value, e)
        if t.kind == "op" and t.value == "(":
            e = self._expr()
            self._expect(")")
            return e
        raise ValueError("unexpected token %s" % (t,))


def parse(s: str):
    """Parse an expression string into an expression tuple."""
    if not isinstance(s, str) or not s.strip():
        raise ValueError("empty expression")
    return _Parser(_tokenize(s)).parse()


# --------------------------------------------------------------------------- #
# Evaluation and pretty printing
# --------------------------------------------------------------------------- #

def eval_expr(e, x: float) -> float:
    """Numerically evaluate an expression at ``x``."""
    op = e[0]
    if op == _NUM:
        return float(e[1])
    if op == _VAR:
        return float(x)
    if op == "pi":
        return math.pi
    if op == "euler":
        return math.e
    a = eval_expr(e[1], x)
    if op in ("sin", "cos", "tan", "exp", "log", "sqrt", "atan"):
        return {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
            "atan": math.atan,
        }[op](a)
    b = eval_expr(e[2], x)
    if op == "add":
        return a + b
    if op == "sub":
        return a - b
    if op == "mul":
        return a * b
    if op == "div":
        return a / b
    if op == "pow":
        return a ** b
    raise ValueError("unknown operator %r" % (op,))


def _fmt(v: float) -> str:
    if v == int(v) and abs(v) < 1e15:
        return str(int(v))
    return "%.10g" % v


def _prec_of(op: str) -> int:
    return {"add": 1, "sub": 1, "mul": 2, "div": 2, "neg": 3,
            "pow": 4}.get(op, 5)


def to_str(e, prec: int = 0) -> str:
    """Render an expression tree as a parseable string.

    ``prec`` is the minimum precedence the surrounding context requires; a
    node whose own precedence is lower is wrapped in parentheses so that
    round-tripping through the parser preserves structure.
    """
    op = e[0]
    if op == _NUM:
        s = _fmt(e[1])
    elif op == _VAR:
        s = "x"
    elif op == "pi":
        s = "pi"
    elif op == "euler":
        s = "e"
    elif op in ("sin", "cos", "tan", "exp", "log", "sqrt", "atan"):
        s = "%s(%s)" % (op, to_str(e[1]))
    elif op == "add":
        s = "%s + %s" % (to_str(e[1], 1), to_str(e[2], 2))
    elif op == "sub":
        s = "%s - %s" % (to_str(e[1], 1), to_str(e[2], 3))
    elif op == "mul":
        if _is_num(e[1]) and float(e[1][1]) == -1.0:
            s = "-%s" % to_str(e[2], 3)
        else:
            s = "%s*%s" % (to_str(e[1], 2), to_str(e[2], 3))
    elif op == "div":
        s = "%s/%s" % (to_str(e[1], 2), to_str(e[2], 4))
    elif op == "pow":
        s = "%s^%s" % (to_str(e[1], 5), to_str(e[2], 3))
    else:
        raise ValueError("unknown operator %r" % (op,))
    if _prec_of(op) < prec:
        return "(%s)" % s
    return s


# --------------------------------------------------------------------------- #
# Symbolic differentiation
# --------------------------------------------------------------------------- #

def differentiate_expr(e):
    """Exact derivative of an expression (simplified)."""
    op = e[0]
    if op == _NUM:
        return num(0)
    if op == _VAR:
        return num(1)
    if op in ("pi", "euler"):
        return num(0)
    if op in ("add", "sub"):
        d1, d2 = differentiate_expr(e[1]), differentiate_expr(e[2])
        return simplify((op, d1, d2))
    if op == "mul":
        a, b = e[1], e[2]
        return simplify(("add",
                         ("mul", differentiate_expr(a), b),
                         ("mul", a, differentiate_expr(b))))
    if op == "div":
        a, b = e[1], e[2]
        da, db = differentiate_expr(a), differentiate_expr(b)
        return simplify(("div",
                         ("sub", ("mul", da, b), ("mul", a, db)),
                         ("pow", b, num(2))))
    if op == "pow":
        a, b = e[1], e[2]
        if _is_num(b):
            n = float(b[1])
            return simplify(("mul",
                             ("mul", num(n),
                              ("pow", a, num(n - 1))),
                             differentiate_expr(a)))
        da, db = differentiate_expr(a), differentiate_expr(b)
        return simplify(("mul", ("pow", a, b),
                         ("add", ("mul", db, ("log", a)),
                          ("mul", ("mul", b, da), ("pow", a, num(-1))))))
    if op in ("sin", "cos", "tan", "exp", "log", "sqrt", "atan"):
        arg, darg = e[1], differentiate_expr(e[1])
        if op == "sin":
            return simplify(("mul", ("cos", arg), darg))
        if op == "cos":
            return simplify(("mul", ("mul", num(-1), ("sin", arg)), darg))
        if op == "tan":
            return simplify(("mul",
                             ("div", num(1),
                              ("pow", ("cos", arg), num(2))), darg))
        if op == "exp":
            return simplify(("mul", ("exp", arg), darg))
        if op == "log":
            return simplify(("mul", ("div", num(1), arg), darg))
        if op == "sqrt":
            return simplify(("mul",
                             ("div", num(1),
                              ("mul", num(2), ("sqrt", arg))), darg))
        return simplify(("mul",
                         ("div", num(1),
                          ("add", num(1), ("pow", arg, num(2)))), darg))
    raise ValueError("unknown operator %r" % (op,))


def differentiate(expr_str: str) -> Tuple[str, object]:
    """``d/dx`` of a string; returns (rendered, tree)."""
    e = parse(expr_str)
    d = simplify(differentiate_expr(e))
    return to_str(d), d


# --------------------------------------------------------------------------- #
# Symbolic antiderivative (the particular integral, integration constant 0)
# --------------------------------------------------------------------------- #

def _antideriv(e):
    """Particular antiderivative (C = 0), or ``None`` if not in the library.

    The constant is *not* added here.  The L.O.R.E. layer adds the definitive
    ``C0`` determined by the measured initial condition ``(q0, V(q0))``.
    """
    op = e[0]
    if op == _NUM:
        return ("mul", e, (_VAR,))
    if op == _VAR:
        return simplify(("div", ("pow", (_VAR,), num(2)), num(2)))
    if op == "add":
        i1, i2 = _antideriv(e[1]), _antideriv(e[2])
        return simplify(("add", i1, i2)) if i1 is not None and i2 is not None else None
    if op == "sub":
        i1, i2 = _antideriv(e[1]), _antideriv(e[2])
        return simplify(("sub", i1, i2)) if i1 is not None and i2 is not None else None
    if op == "mul":
        if _is_const(e[1]):
            i = _antideriv(e[2])
            return simplify(("mul", e[1], i)) if i is not None else None
        if _is_const(e[2]):
            i = _antideriv(e[1])
            return simplify(("mul", e[2], i)) if i is not None else None
        if e == ("mul", (_VAR,), ("exp", (_VAR,))):      # x*e^x
            return simplify(("mul", ("sub", (_VAR,), num(1)), ("exp", (_VAR,))))
        if e == ("mul", (_VAR,), ("sin", (_VAR,))):      # x*sin(x)
            return simplify(("sub", ("sin", (_VAR,)),
                             ("mul", (_VAR,), ("cos", (_VAR,)))))
        if e == ("mul", (_VAR,), ("cos", (_VAR,))):      # x*cos(x)
            return simplify(("add", ("cos", (_VAR,)),
                             ("mul", (_VAR,), ("sin", (_VAR,)))))
        return None
    if op == "div":
        a, b = e[1], e[2]
        if _is_num(a) and b == (_VAR,):                  # c / x
            return simplify(("mul", a, ("log", (_VAR,))))
        if a == num(1) and b == ("sqrt", (_VAR,)):       # 1/sqrt(x)
            return simplify(("mul", num(2), ("sqrt", (_VAR,))))
        if a == num(1) and b == simplify(("add", num(1),
                                          ("pow", (_VAR,), num(2)))):
            return ("atan", (_VAR,))
        return None
    if op == "pow":
        base, p = e[1], e[2]
        if base == (_VAR,) and _is_num(p):               # x^n
            n = float(p[1])
            if n == -1.0:
                return ("log", (_VAR,))
            return simplify(("div", ("pow", (_VAR,), num(n + 1)), num(n + 1)))
        if _is_num(base) and p == (_VAR,):               # c^x, c>0, c!=1
            c = float(base[1])
            if c > 0 and c != 1.0:
                k = math.log(c)
                return simplify(("div", ("exp", ("mul", num(k), (_VAR,))),
                                 num(k)))
        if base == ("sin", (_VAR,)) and p == num(2):     # sin^2(x)
            return simplify(("sub", ("div", (_VAR,), num(2)),
                             ("div", ("sin", ("mul", num(2), (_VAR,))),
                              num(4))))
        if base == ("cos", (_VAR,)) and p == num(2):     # cos^2(x)
            return simplify(("add", ("div", (_VAR,), num(2)),
                             ("div", ("sin", ("mul", num(2), (_VAR,))),
                              num(4))))
        return None
    if op == "exp":
        k, base = _coef(e[1])
        if base == (_VAR,):
            if k == 1.0:
                return ("exp", (_VAR,))
            return simplify(("div", ("exp", ("mul", num(k), (_VAR,))), num(k)))
        if _is_const(e[1]):                              # e^c
            return simplify(("mul", ("exp", e[1]), (_VAR,)))
        return None
    if op == "log":
        k, base = _coef(e[1])
        if base == (_VAR,):
            return simplify(("sub", ("mul", (_VAR,), ("log", e[1])), (_VAR,)))
        return None
    if op == "sin":
        k, base = _coef(e[1])
        if base == (_VAR,):
            if k == 1.0:
                return simplify(("mul", num(-1), ("cos", (_VAR,))))
            return simplify(("mul", num(-1),
                             ("div", ("cos", ("mul", num(k), (_VAR,))),
                              num(k))))
        if _is_const(e[1]):
            return simplify(("mul", ("sin", e[1]), (_VAR,)))
        return None
    if op == "cos":
        k, base = _coef(e[1])
        if base == (_VAR,):
            if k == 1.0:
                return ("sin", (_VAR,))
            return simplify(("div", ("sin", ("mul", num(k), (_VAR,))), num(k)))
        if _is_const(e[1]):
            return simplify(("mul", ("cos", e[1]), (_VAR,)))
        return None
    if op == "tan":
        if e[1] == (_VAR,):
            return simplify(("mul", num(-1), ("log", ("cos", (_VAR,)))))
        return None
    if op == "sqrt":
        if e[1] == (_VAR,):
            return simplify(("mul", num(2.0 / 3.0),
                             ("pow", (_VAR,), num(1.5))))
        return None
    if op == "atan":
        if e[1] == (_VAR,):
            return simplify(("sub", ("mul", (_VAR,), ("atan", (_VAR,))),
                             ("mul", num(0.5),
                              ("log", ("add", num(1),
                                       ("pow", (_VAR,), num(2)))))))
        return None
    return None


def antiderivative(expr_str: str) -> Tuple[Optional[str], bool]:
    """Particular antiderivative of a string.

    Returns ``(rendered or None, exact)``.  ``exact`` is False when the
    expression is outside the closed-form library (numeric fallback used).
    """
    e = parse(expr_str)
    f = _antideriv(e)
    if f is None:
        return None, False
    return to_str(simplify(f)), True


# --------------------------------------------------------------------------- #
# Numeric calculus
# --------------------------------------------------------------------------- #

def numeric_differentiate(f, x: float, h: float = 1e-5) -> float:
    """5-point central stencil, error O(h^4)."""
    return (-f(x + 2 * h) + 8 * f(x + h) - 8 * f(x - h) + f(x - 2 * h)) \
        / (12 * h)


def gauss_legendre(f, a: float, b: float, n: int = 20) -> float:
    """Gauss-Legendre quadrature on [a, b]."""
    xs = [-0.960289856497536, -0.796666477413627, -0.525532409916329,
          -0.183434642495650, 0.183434642495650, 0.525532409916329,
          0.796666477413627, 0.960289856497536]
    ws = [0.101228536290376, 0.222381034453374, 0.313706645877887,
          0.362683783378362, 0.362683783378362, 0.313706645877887,
          0.222381034453374, 0.101228536290376]
    if n >= 8 and n % 8 == 0:
        pass
    else:
        nodes, weights = _gl_nodes(n)
        xs, ws = nodes, weights
    mid = 0.5 * (a + b)
    half = 0.5 * (b - a)
    return half * sum(w * f(mid + half * t) for t, w in zip(xs, ws))


def _gl_nodes(n: int):
    """n-point Gauss-Legendre nodes/weights via Newton on Legendre roots."""
    if n <= 0:
        return [], []
    xs, ws = [], []
    for k in range(1, n + 1):
        # initial guess (Chebyshev spacing)
        x = math.cos(math.pi * (k - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for j in range(2, n + 1):
                p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
            dp = n * (x * p1 - p0) / (x * x - 1)
            step = p1 / dp
            x -= step
            if abs(step) < 1e-15:
                break
        xs.append(x)
        ws.append(2.0 / ((1 - x * x) * dp * dp))
    return xs, ws


def adaptive_simpson(f, a: float, b: float, tol: float = 1e-10,
                     depth: int = 0) -> float:
    """Adaptive Simpson quadrature; exact on cubics between panels."""
    if depth > 40:
        return 0.0
    h = b - a
    c = 0.5 * (a + b)
    fa, fb, fc = f(a), f(b), f(c)
    whole = (h / 6.0) * (fa + 4 * fc + fb)
    d = 0.5 * (a + c)
    e = 0.5 * (c + b)
    fd, fe = f(d), f(e)
    left = (h / 12.0) * (fa + 4 * fd + fc)
    right = (h / 12.0) * (fc + 4 * fe + fb)
    err = (left + right) - whole
    if abs(err) < 15 * tol:
        return left + right + err / 15.0
    return (adaptive_simpson(f, a, c, tol / 2.0, depth + 1)
            + adaptive_simpson(f, c, b, tol / 2.0, depth + 1))


def integrate_numeric(f, a: float, b: float, tol: float = 1e-10) -> float:
    """Robust numeric definite integral over [a, b]."""
    return adaptive_simpson(f, a, b, tol)


# --------------------------------------------------------------------------- #
# Limits
# --------------------------------------------------------------------------- #

def _sym_limit(e, a):
    """Symbolic limit for standard forms.  Returns (value, exact) or None.

    Handles the removable singularities that direct substitution cannot:
    ``sin(x)/x``, ``tan(x)/x``, ``(1-cos x)/x^2``, ``(e^x-1)/x``,
    ``log(1+x)/x`` at 0, and ``(1 + c/x)^x`` at infinity.
    """
    if math.isinf(a):
        s = 1.0 if a > 0 else -1.0
        if e[0] == "div" and _is_num(e[1]) and e[2] == var():
            return 0.0, True                     # c/x -> 0
        if e[0] == "pow" and e[1] == var() and _is_num(e[2]) \
                and float(e[2][1]) < 0:
            return 0.0, True                     # 1/x^n -> 0
        if e[0] == "pow":
            base, expo = e[1], e[2]
            if expo == var() and base[0] == "add" and _is_num(base[1]) \
                    and float(base[1][1]) == 1.0:
                tail = base[2]
                if tail[0] == "div" and _is_num(tail[1]) and tail[2] == var():
                    c = float(tail[1][1])
                    if s > 0:
                        return math.exp(c), True  # (1 + c/x)^x -> e^c
        return None
    if a == 0.0:
        if e[0] == "div":
            num_, den = e[1], e[2]
            if den == var() and num_[0] in ("sin", "tan"):
                k, base = _coef(num_[1])
                if base == var():
                    return float(k), True         # sin(kx)/x, tan(kx)/x -> k
            if den == ("pow", var(), num(2)) \
                    and num_ == ("sub", num(1), ("cos", var())):
                return 0.5, True                  # (1-cos x)/x^2 -> 1/2
            if den == var() and num_ == ("sub", ("exp", var()), num(1)):
                return 1.0, True                  # (e^x - 1)/x -> 1
            if den == var() and num_ == ("log", ("add", num(1), var())):
                return 1.0, True                  # log(1+x)/x -> 1
        if e[0] == "pow" and e[1] == ("add", num(1), var()) \
                and e[2] == ("div", num(1), var()):
            return math.e, True                   # (1+x)^(1/x) -> e
        return None
    return None


def _richardson(pairs):
    """Richardson (Neville) table extrapolating the sampled values to u = 0."""
    n = len(pairs)
    R = [[pairs[i][1]] for i in range(n)]
    for j in range(1, n):
        for i in range(j, n):
            h1 = pairs[i][0]
            h0 = pairs[i - j][0]
            R[i].append(R[i][j - 1]
                        + (R[i][j - 1] - R[i - 1][j - 1]) / (h0 / h1 - 1))
    return R


def _numeric_limit_seq(g, steps: int = 26, tol: float = 1e-7):
    """One-sided numeric limit by Richardson extrapolation.

    Returns ``(value, diverges)``; ``diverges`` is one of "", "+inf",
    "-inf", "oscillates".
    """
    pairs = []
    u = 1.0
    for _ in range(steps):
        try:
            y = g(u)
        except (ZeroDivisionError, ValueError, OverflowError,
                FloatingPointError):
            y = float("nan")
        if not math.isfinite(y):
            break
        pairs.append((u, y))
        u *= 0.5
    if len(pairs) < 4:
        return None, "oscillates"
    # A pole: values blow up geometrically as u halves -> divergent.
    tail = pairs[-6:]
    if len(tail) >= 3:
        mags = [abs(y) for _, y in tail]
        if min(mags) > 1e3 and max(mags) / min(mags) > 100.0:
            sign = 1.0 if tail[-1][1] > 0 else -1.0
            if all((y > 0) == (tail[-1][1] > 0) for _, y in tail):
                return None, ("+inf" if sign > 0 else "-inf")
    # Divergent growth that Richardson cannot chase (e.g. log(x) -> -inf):
    # successive differences stop shrinking instead of dying out.
    diffs = [b - a for (_, a), (_, b) in zip(pairs, pairs[1:])]
    if all(math.isfinite(d) for d in diffs[-3:]):
        if all(abs(d) > 1e-4 for d in diffs[-3:]):
            sign = 1.0 if diffs[-1] > 0 else -1.0
            return None, ("+inf" if sign > 0 else "-inf")
    R = _richardson(pairs)
    est = R[-1][-1]
    if not math.isfinite(est):
        return None, "oscillates"
    if abs(est) < tol:
        est = 0.0
    return est, ""


def _limit1(e, a, side):
    """One-sided limit of expression ``e`` as x -> a from ``side``."""
    if math.isinf(a):
        r = _sym_limit(e, a)
        if r is not None:
            return {"value": r[0], "exact": True, "diverges": ""}
        sign = 1.0 if a > 0 else -1.0
        val, div = _numeric_limit_seq(lambda u: eval_expr(e, sign / u))
        return {"value": val, "exact": False, "diverges": div}
    try:
        v = eval_expr(e, a)
        if math.isfinite(v):
            return {"value": v, "exact": True, "diverges": ""}
        div = ("+inf" if v > 0 else "-inf") if v else "oscillates"
        return {"value": None, "exact": False, "diverges": div}
    except (ZeroDivisionError, ValueError, OverflowError):
        pass
    r = _sym_limit(e, a)
    if r is not None:
        return {"value": r[0], "exact": True, "diverges": ""}
    d = 1.0 if side == "right" else -1.0
    val, div = _numeric_limit_seq(lambda u: eval_expr(e, a + d * u))
    return {"value": val, "exact": False, "diverges": div}


def limit(expr_str, x0, side: str = "both", tol: float = 1e-7) -> dict:
    """Compute ``lim_{x -> x0} f(x)``.

    ``x0`` accepts a number or the strings ``inf``, ``+inf``, ``-inf``,
    ``infinity``.  ``side`` is ``"both"``, ``"left"`` or ``"right"``.

    Returns a dict with ``value`` (None when the limit diverges or does not
    exist), ``exact``, ``exists``, the one-sided values and a ``diverges``
    descriptor.
    """
    e = parse(expr_str)
    if isinstance(x0, str):
        s = x0.strip().lower().replace("infinity", "inf").replace("infty", "inf")
        if s in ("inf", "+inf", "inf", "oo"):
            a = math.inf
        elif s in ("-inf", "-infinity", "-oo"):
            a = -math.inf
        else:
            a = float(x0)
    else:
        a = float(x0)

    if math.isinf(a):
        r = _limit1(e, a, "right" if a > 0 else "left")
        return {
            "ok": True, "expr": expr_str, "x0": a, "side": side,
            "value": r["value"], "exact": r["exact"],
            "exists": r["value"] is not None, "diverges": r["diverges"],
            "left": r["value"], "right": r["value"],
        }

    if side == "both":
        left = _limit1(e, a, "left")
        right = _limit1(e, a, "right")
        agrees = (left["value"] is not None and right["value"] is not None
                  and abs(left["value"] - right["value"])
                  <= tol * max(1.0, abs(left["value"])))
        exists = agrees
        value = left["value"] if agrees else None
        exact = bool(left["exact"] and right["exact"]) and agrees
        div = ""
        if not exists:
            parts = []
            if left["diverges"]:
                parts.append("left:%s" % left["diverges"])
            if right["diverges"]:
                parts.append("right:%s" % right["diverges"])
            div = " ".join(parts) or "oscillates"
        return {
            "ok": True, "expr": expr_str, "x0": a, "side": side,
            "value": value, "exact": exact, "exists": exists,
            "diverges": div,
            "left": left["value"], "right": right["value"],
        }
    r = _limit1(e, a, side)
    return {
        "ok": True, "expr": expr_str, "x0": a, "side": side,
        "value": r["value"], "exact": r["exact"],
        "exists": r["value"] is not None, "diverges": r["diverges"],
        "left": r["value"] if side == "left" else None,
        "right": r["value"] if side == "right" else None,
    }


# --------------------------------------------------------------------------- #
# Definite integrals (exact when possible, numeric otherwise)
# --------------------------------------------------------------------------- #

def definite_integral(expr_str: str, a: float, b: float) -> dict:
    """Compute the definite integral as a *constant*.

    Exact form comes from ``F(b) - F(a)`` with the particular F (C = 0).
    When the integrand is outside the closed-form library the value is
    integrated numerically and ``exact`` is False.
    """
    e = parse(expr_str)
    f = _antideriv(e)
    result = {
        "a": float(a), "b": float(b),
        "integrand": expr_str,
        "exact": False, "exact_value": None,
        "antiderivative": None,
        "numeric_value": None,
        "method": "adaptive Simpson",
    }
    if f is not None:
        result["exact"] = True
        result["antiderivative"] = to_str(simplify(f))
        fa, fb = eval_expr(f, a), eval_expr(f, b)
        result["exact_value"] = fb - fa
        result["method"] = "F(b) - F(a), exact"
        return result
    result["numeric_value"] = integrate_numeric(
        lambda x: eval_expr(e, x), float(a), float(b))
    return result


# --------------------------------------------------------------------------- #
# The definitive constant (L.O.R.E.)
# --------------------------------------------------------------------------- #

def definitive_constant(expr_str: str, q0: float, fq0: float) -> dict:
    """Collapse the integration constant using a known initial condition.

    Particular antiderivative F (C = 0), measured ``(q0, F(q0))``::

        C0 = F(q0) - F(q0)   measured   =>   C0 = fq0 - F(q0)

    The definitive antiderivative is ``F(x) + C0``; there is no arbitrary
    constant because the initial condition is *known*.
    """
    e = parse(expr_str)
    f = _antideriv(e)
    if f is None:
        return {"ok": False,
                "error": "integrand outside the closed-form library: "
                         "%s" % expr_str}
    f_str = to_str(simplify(f))
    f_at_q0 = eval_expr(f, float(q0))
    c0 = float(fq0) - f_at_q0
    # F(x) + C0 -> ("add", f, num(c0))
    definitive = simplify(("add", f, num(c0)))
    return {
        "ok": True,
        "expr": expr_str,
        "q0": float(q0),
        "measured_F_q0": float(fq0),
        "particular": f_str,
        "particular_at_q0": f_at_q0,
        "C0": c0,
        "definitive": to_str(definitive),
    }


# --------------------------------------------------------------------------- #
# Asset-backed measure: C0 = V(q0) = H(q0, 0) on the Poincare disk
# --------------------------------------------------------------------------- #

def _asset_positions():
    """Load the taxonomy positions from the L.O.R.E. asset.

    ``Universals`` ships inside the wheel, so the import works for an
    installed package; when running from a bare source checkout the repo
    root is added to ``sys.path`` as a fallback.
    """
    try:
        from Universals.hamiltonian_flow import (  # type: ignore
            ALPHA, POSITIONS, repulsion_loss)
        return ALPHA, POSITIONS, repulsion_loss
    except ImportError:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if root not in sys.path:
            sys.path.insert(0, root)
        from Universals.hamiltonian_flow import (  # type: ignore
            ALPHA, POSITIONS, repulsion_loss)
        return ALPHA, POSITIONS, repulsion_loss


def asset_positions() -> dict:
    """Names and coordinates of the Poincare-disk taxonomy (asset data)."""
    _, pos, _ = _asset_positions()
    return {name: [float(v[0]), float(v[1])] for name, v in pos.items()}


def lore_measure(q0=(0.0, 0.0), context=("Tech", "Silicon"), alpha=None):
    """Measure ``C0 = V(q0) = H(q0, 0)`` from the project asset.

    V is the repulsion potential (``repulsion_loss``); H is the Hamiltonian
    evaluated at kinetic energy 0, which equals V identically.  Returns the
    measured values plus the positions table for the dashboard canvas.
    """
    _, pos, repulsion_loss = _asset_positions()
    if alpha is None:
        alpha = _asset_positions()[0]
    import numpy as np  # lazy: numpy is already a project dependency
    v = repulsion_loss(np.asarray(q0, dtype=float), list(context), alpha)
    h0 = v  # H(q, p=0) == V(q) by definition of the kinetic term
    positions = {name: [float(p[0]), float(p[1])] for name, p in pos.items()}
    return {
        "ok": True,
        "source": "Universals/hamiltonian_flow.py (repo asset)",
        "alpha": float(alpha),
        "q0": [float(q0[0]), float(q0[1])],
        "context": list(context),
        "V_q0": float(v),
        "H_q0_0": float(h0),
        "C0": float(v),          # the definitive constant of the potential
        "kinetic_energy": 0.0,
        "positions": positions,
    }


def sample(expr_str: str, a: float, b: float, n: int = 200) -> list:
    """Equally spaced samples of f over [a, b] for the dashboard canvas."""
    e = parse(expr_str)
    xs, ys = [], []
    n = max(2, min(int(n), 2000))
    for i in range(n + 1):
        x = float(a) + (float(b) - float(a)) * i / n
        try:
            y = eval_expr(e, x)
        except (ValueError, ZeroDivisionError, OverflowError, FloatingPointError):
            y = None
        xs.append(x)
        ys.append(y)
    return [xs, ys]


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser(prog="python -m puno_app.calculus")
    ap.add_argument("expr")
    ap.add_argument("--mode", choices=["derive", "antideriv"],
                    default="derive")
    args = ap.parse_args()
    if args.mode == "derive":
        s, _ = differentiate(args.expr)
        print(s)
    else:
        s, exact = antiderivative(args.expr)
        print("antiderivative: %s" % (s if exact else "not in library"))
