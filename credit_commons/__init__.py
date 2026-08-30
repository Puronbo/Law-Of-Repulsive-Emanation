"""Credit-Commons: a trust-backed mutual-credit system simulator.

Faithful to docs/CREDIT_COMMONS.md — the two-counter credit/trust model, the
conserved facilitation fee, the progressive g(d), the equity spine (§5.5) and
the action asymmetry (§5.6). Used to *test the design's claims* before any
pilot or proposal is built on top of it.
"""

from .sim import Account, Commons, TradeResult

__all__ = ["Account", "Commons", "TradeResult"]
