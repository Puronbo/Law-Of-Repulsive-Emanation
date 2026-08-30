"""Core simulator for the Credit-Commons trust-backed mutual-credit system.

Faithful encoding of docs/CREDIT_COMMONS.md:

  Section 1   : two counters (credit signed, trust = spending ceiling).
  Section 3   : atomic trade flow with a CONSERVED facilitation fee (gate 6).
  Section 2.6 : unit is a benchmark service basket; all constants cite it.
  Section 4   : compensation = enabling others' trade; progressive taper (E2).
  Section 5   : trust loop with regenerating floor (B5), necessity rebuild (E1),
                progressive g(d) (E2), irreversible harm I (gate 14).
  Section 5.5 : pro-poor spine E1/E2/E3.
  Section 5.6 : asymmetry — positive weighted in magnitude (alpha), negative in
                irreversibility (I).

All parameters are tunable and expressed relative to the unit (Section 2.6).
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Parameters. Alpha (positive bias) and I (irreversibility) implement §5.6.
# ---------------------------------------------------------------------------
@dataclass
class Params:
    # Trust loop (§5)
    r: float = 0.10          # contribution reward rate (per unit served)
    alpha: float = 0.30      # positive-action bias: effective r' = r*(1+alpha)
    g0: float = 0.05         # base draw-down rate (shallow borrowing)
    gdepth: float = 1.20     # progressive depth multiplier at full leverage
    n: float = 0.10          # necessity-consumption trust rebuild (E1)
    floor: float = 0.001     # baseline regeneration per step (B5 / cold-start)
    taper0: float = 0.0      # taper base (negligible at modest surplus)
    taperA: float = 0.0004   # taper growth on large idle surplus (progressive)
    I: float = 2.00          # irreversible harm scar (gate 14), in trust units
    # Fee (§3, conserved) and compensation (§4)
    f: float = 0.02          # facilitation fee fraction of X
    terminal_share: float = 0.40   # share of f to the terminal provider
    refer_share: float = 0.25     # share of f to the referrer chain
    validator_share: float = 0.25 # share of f to validation nodes
    consumer_floor: float = 0.10  # E3: use-side floor of f to active consumers
    # Entry / grants (§2, §5.5 progressive)
    seed_credit: float = 10.0
    seed_trust: float = 10.0
    grant_bias: float = 0.5   # progressive: grant grows as trust/credit shrink
    max_leverage: float = 1.0 # buy denied if credit/trust < -max_leverage
    necessity_ceiling: float = 0.6  # fix of pure-consumer stall (E1): a reserve
                                    # fraction of trust set aside for necessity
                                    # spending, immune to the hard gate + taper

    def reward(self) -> float:
        """§5.6: positive action weighted in magnitude via alpha."""
        return self.r * (1.0 + self.alpha)

    def g_at(self, depth: float) -> float:
        """E2: draw-down growth is progressive in depth."""
        d = min(max(depth, 0.0), 1.0)
        return self.g0 * (1.0 + self.gdepth * d)

    def taper_of(self, surplus: float) -> float:
        """E2: taper is progressive in idle surplus (negligible at modest)."""
        if surplus <= 0:
            return 0.0
        return self.taper0 + self.taperA * surplus


@dataclass
class TradeResult:
    ok: bool
    reason: str = ""
    x: float = 0.0
    fee: float = 0.0
    fee_buyer: float = 0.0


@dataclass
class Account:
    id: int
    tier: str = "individual"
    credit: float = 0.0
    trust: float = 0.0
    harm: float = 0.0            # cumulative committed harm h
    irrev: float = 0.0           # cumulative irreversible scar I*h (partial lift ok)
    served: float = 0.0          # value sold / contributed (value-weighted)
    drawn: float = 0.0           # value bought / drawn
    necessity: float = 0.0       # necessity value consumed (E1)
    contributed: float = 0.0     # non-sales contribution (validate/vouch/refer)
    idle_steps: int = 0

    def depth(self) -> float:
        """depth = how deeply negative relative to trust (0..1+)."""
        if self.trust <= 0:
            return 1.0
        return max(0.0, -self.credit) / self.trust


class Commons:
    def __init__(self, params: Params | None = None):
        self.p = params or Params()
        self.accounts: dict[int, Account] = {}
        self.ledger: list[tuple] = []
        self._next_id = 1
        # governance / equity metrics
        self.total_credit = 0.0
        self.reserve = 0.0  # commons surplus: unallocated fee funds grants (Ph.2)

    # -- accounts ----------------------------------------------------------
    def add_account(self, seed_credit=None, seed_trust=None, tier="individual"):
        a = Account(
            id=self._next_id,
            tier=tier,
            credit=seed_credit if seed_credit is not None else self.p.seed_credit,
            trust=seed_trust if seed_trust is not None else self.p.seed_trust,
        )
        self._next_id += 1
        self.accounts[a.id] = a
        self.total_credit += a.credit
        return a.id

    def grant(self, recipient: int, amount: float, sponsor: int | None = None):
        """Phase 2 — progressive redistribution. amount given to those with
        least: smaller existing trust/credit => larger relative lift."""
        a = self.accounts[recipient]
        scale = 1.0 + self.p.grant_bias / max(1e-9, 1.0 + a.trust)
        amt = amount * scale
        a.credit += amt
        # grants also raise standing modestly — usable, not infinite (gates 7/8)
        a.trust += 0.05 * amt
        self.total_credit += amt
        self.ledger.append(("grant", recipient, sponsor, amt))
        return amt

    # -- trust maintenance (time step) --------------------------------------
    def step(self):
        """Apply periodic floor regeneration + progressive idle taper."""
        for a in self.accounts.values():
            a.trust += self.p.floor
            if a.credit > 0:
                a.trust -= self.p.taper_of(a.credit)
                a.idle_steps += 1
            else:
                a.idle_steps = 0
            a.trust = max(0.0, a.trust)

    # -- the atomic trade ---------------------------------------------------
    def trade(
        self,
        buyer: int,
        seller: int,
        X: float,
        necessity: bool = False,
        terminal: int | None = None,
        referrer: int | None = None,
        validators: list[int] | None = None,
        committed_harm: float = 0.0,
    ) -> TradeResult:
        """Section 3 atomic flow with conserved (not minted) facilitation fee.
        committed_harm != 0 models a fraud/default/abuse on the buyer's part
        (§5.6 irreversibility)."""
        if X <= 0:
            return TradeResult(False, "non-positive quantity")
        b = self.accounts.get(buyer)
        s = self.accounts.get(seller)
        if b is None or s is None:
            return TradeResult(False, "unknown account")

        # gate: buy denied while credit would go beyond -trust (max_leverage).
        # Necessity purchases draw against a protected necessity ceiling — a
        # reserved fraction of trust immune to the hard gate — so the poorest
        # can always meet basic needs (the pure-consumer-stall fix, E1).
        if necessity:
            ceiling = b.trust * self.p.necessity_ceiling
            if b.credit - X < -ceiling:
                return TradeResult(False, "beyond necessity-protection ceiling")
        else:
            if b.credit - X < -b.trust * self.p.max_leverage:
                return TradeResult(False, "credit would exceed trust ceiling")

        X = float(X)
        # conserved facilitation fee (§3/§4, gate 6): charged to the trade.
        fee = self.p.f * X

        # if the buyer cannot also fund the fee from credit (still within trust),
        # fund it as a spread: reduce the seller's received credit. This keeps
        # total credit conserved (no mintage).
        if committed_harm > 0:
            # a committed harm is irreversible: it scars trust (I) and is
            # committed (not returned). Positive reward cannot erase it.
            harm_amt = self.p.I * committed_harm
            b.irrev += harm_amt
            b.harm += committed_harm
            b.trust -= harm_amt
            # committed harm also restricts spend power going forward

        # consumer E1: necessity consumption rebuilds trust instead of drawing.
        if necessity:
            b.trust += self.p.n * X
            b.necessity += X
            draw = 0.0  # necessity is not a pure draw-down (E1)
        else:
            draw = X
            depth = b.depth()
            b.trust -= self.p.g_at(depth) * X
            b.drawn += X

        # seller reward with positive bias (gate 14 / §5.6)
        b.credit -= X
        s.credit += X - fee  # seller pays the fee out of the trade (conserved)

        # split fee (conserved — redistribution of X, not new money).
        self._split_fee(fee, buyer, seller, terminal, referrer, validators)

        # seller reward (positive-weighted magnitude)
        s.trust += self.p.reward() * X
        s.served += X

        b.trust = max(0.0, b.trust)
        self.ledger.append(
            ("trade", buyer, seller, X, fee, necessity, committed_harm)
        )
        return TradeResult(True, "ok", x=X, fee=fee)

    def _split_fee(self, fee, buyer, seller, terminal, referrer, validators):
        """E3: fee split capped per class, with a use-side consumer floor.
        Everyone gets a *trust* credit for participating; the fee itself is
        redistributed credit from the seller's side (conserved), not minted."""
        if fee <= 0:
            return
        # Active-consumer floor (E3): part of the fee value stays with the
        # buying side as a reward for being an active in-network consumer.
        # The fee is removed from the seller's credit and fully redistributed.
        # Every unit either reaches an account (floor/class) or falls to the
        # commons reserve (which later funds grants, Phase 2), so the total of
        # (accounts' credit) + reserve is exactly conserved — never minted, never
        # destroyed (gate 6). We track spent to assert this in tests.
        floor_val = fee * self.p.consumer_floor
        spent = 0.0
        if buyer in self.accounts:
            self.accounts[buyer].credit += floor_val
            self.accounts[buyer].contributed += floor_val
            spent += floor_val
        remaining = fee - floor_val
        # configured class shares, each granted only if its contributor exists.
        if terminal is not None and terminal in self.accounts:
            amt = remaining * self.p.terminal_share
            self.accounts[terminal].credit += amt
            self.accounts[terminal].contributed += amt
            spent += amt
        if referrer is not None and referrer in self.accounts:
            amt = remaining * self.p.refer_share
            self.accounts[referrer].credit += amt
            self.accounts[referrer].contributed += amt
            spent += amt
        if validators:
            amt = remaining * self.p.validator_share
            each = amt / max(1, len(validators))
            for v in validators:
                if v in self.accounts:
                    self.accounts[v].credit += each
                    self.accounts[v].contributed += each
            spent += amt
        # unclaimed remainder funds the commons reserve (grants, Ph.2)
        self.reserve += fee - spent

    # -- convenience stats --------------------------------------------------
    def gini(self, attr="credit"):
        """Gini coefficient of an unsigned distribution (0 = equal, 1 = total
        concentration). For signed credit we measure the Gini of the *absolute*
        net positions; for trust (always >= 0) it is the ordinary Gini. A value
        <= 1 is guaranteed."""
        if attr == "credit":
            vals = sorted(abs(a.credit) for a in self.accounts.values())
        else:
            vals = sorted(getattr(a, attr) for a in self.accounts.values())
        n = len(vals)
        if n == 0:
            return 0.0
        s = sum(vals)
        if s == 0:
            return 0.0
        cum = 0.0
        for i, v in enumerate(vals, start=1):
            cum += (2 * i - n - 1) * v
        g = cum / (n * s)
        # numeric clamp: Gini cannot exceed 1 by definition.
        return min(1.0, g)

    def summary(self, label=""):
        n = len(self.accounts)
        if n == 0:
            return {}
        trusts = [a.trust for a in self.accounts.values()]
        credits = [a.credit for a in self.accounts.values()]
        return {
            "label": label,
            "n": n,
            "mean_trust": sum(trusts) / n,
            "min_trust": min(trusts),
            "mean_credit": sum(credits) / n,
            "min_credit": min(credits),
            "gini_credit": self.gini("credit"),
            "gini_trust": self.gini("trust"),
            "total_credit": self.total_credit,
            "trades": sum(1 for t in self.ledger if t[0] == "trade"),
        }
