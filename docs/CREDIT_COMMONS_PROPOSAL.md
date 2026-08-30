# The Credit-Commons Proposal

A measured, validated design for a trust-backed mutual-credit currency that
*wins by use* — no external wallet, no external money after a one-shot seed,
payable from merchant terminals with only a recallable account number — where
value is created by trade, given to those who join and serve, and governed
toward **equity for all**.

Companion documents:
- `docs/CREDIT_COMMONS.md` — the full design specification (14 hard gates).
- `credit_commons/sim.py` — the simulator this proposal's numbers come from.
- `credit_commons/tune.py` — the tuning experiments.
- `docs/CREDIT_COMMONS_PILOT.md` — the real-world pilot framework.

---

## 1. What this is, and why it is not a "coin"

The core claim, stated plainly:

> **Money is the memory that you have served; trust is the permission to be
> served before you have. Buying converts permission into memory; selling
> rebuilds permission. Neither is external; every credit is a debt somewhere,
> and every debt is allowed only to the depth of the community's trust in you.**

This proposal is **not a token launch**. It is a *system* whose output happens
to be a usable internal currency. That ordering matters — a currency released
before the system exists has no anchors, no trust loop, and no equity spine; it
is a coupon with delusions. The currency is the shadow of the system, not a
product to be marketed first (see §7, sequencing).

---

## 2. The mechanism in six lines

1. **Two counters, never one.** Every account has a signed **credit** (money)
   and a non-negative **trust** (spending ceiling). You can buy down to
   `credit = -trust`, not beyond.
2. **The trade is atomic and conserved.** Buyer pays `X`; seller receives
   `X - fee`; the `fee` is fully redistributed (terminal, referral, validation,
   a use-side consumer floor) with any remainder to a commons reserve — **no
   money is minted by a trade** (gate 6).
3. **The unit is a benchmark, not a float.** One unit is a published in-network
   service basket; relative prices are set bilaterally against it; the unit is
   **never redeemable for outside money** (gate 0).
4. **Trust is primary; money is its shadow.** Trust is rebuilt by contribution
   and by consuming in-network necessity; it is drawn by buying, progressively
   with depth; it regenerates through a baseline floor.
5. **Equity is the spine (§5.5).** Necessity consumption is contribution, not
   cost. `g(d)` and the taper are progressive. The fee keeps a use-side floor.
   Grants give most to those with least.
6. **Action is asymmetric both ways (§5.6).** Positive action is weighted in
   *magnitude* (`r' = r·(1+α)`); negative action is weighted in
   *irreversibility* (a committed harm scars trust permanently). Rewards pull,
   debts scar.

---

## 3. Measured properties (from the simulator)

All numbers below come from `credit_commons/` — a 24-member, 3000-round
community (and targeted pilots). They are tests of the *design*, not of the code.

### 3.1 Stability: no runaway concentration

- **Gini of trust** ≈ **0.05–0.13** across 8 independent seeds and across every
  parameter setting swept (`alpha`, `gdepth`, `floor`, `f`, `I`). A Gini of 1 is
  total concentration; ~0.1 is a strikingly *flat* distribution. **The floor +
  progressive `g(d)` prevent the rich-get-richer equilibrium** that plagues
  naive trust loops.
- **Mintage is exactly conserved**: `sum(credit) + reserve == total_credit`
  holds to machine precision after arbitrary trades; `total_credit` never changes
  from a trade. No inflation, no free-minting.

### 3.2 Asymmetry works as specified (gate 14)

In a 200-good-actions-vs-200-harms comparison:
- an honest **contributor's trust** rose to **28.3**;
- an **abuser's trust** fell to **21.1** and carries a **permanent irreversibility
  scar of `I·h = 6.0`** that no number of later positive trades erases.

The positive bias (`α`) and the irreversible scar (`I`) are both real, not
cosmetic: contributors are pulled up; free-riders are marked for life.

### 3.3 Equity, sustained honestly

- In mixed communities, **100% of members** finish with trust above threshold
  (`poor_ok = 100%` across all runs).
- A **pure necessity consumer** (never contributes) is **never left without basic
  needs**: the necessity-protection ceiling keeps them buying, and the commons
  bridge them with **Phase-2 progressive grants** from the reserve. This is the
  honest division — standing is protected for free, but *credit* is real debt
  that the community collectively funds, not infinite free leverage for a
  never-contributor (which would be the sybil/free-money hole).

### 3.4 The one finding that changed the design

The simulation forced an honest correction to the "necessity is free" intuition:
a consumer who *never* contributes will always out-spend any finite credit line —
and **that is correct**. Issuing them unlimited necessity credit would be a sybil
hole. The resulting design therefore splits necessity-protection into **standing**
(protected, never penalized) and **credit** (grant-funded by the commons). This
is the difference between protecting dignity and minting free money, and the
model made it unambiguous.

---

## 4. The 14 hard gates (condensed)

0. Unit is a benchmark, never a redemption promise.
1. One-shot seed is capped.
2. Donations are in-network credit.
3. Seed-bought anchors accept in-network credit at in-network prices.
4. Trust is spendable-only and bounded.
5. Draw-down is committed + lockout.
6. Mintage is conserved — emission is grants, not free-minting.
7. Fork-free, writable from any single surviving point (provisional authority).
8. New/child accounts need a sponsor (family is the standing sponsor).
9. Tier buy-in buys responsibility/weight, not extraction.
10. Network appropriation is by the rule, not a person.
11. One family per person; shared trust bounded; anchor is enhancer not gate.
12. Governance weight is capped (one-person-one-vote floor, per-account cap).
13. The pro-poor spine is load-bearing, not charity.
14. Positive weighted in magnitude, negative in irreversibility.

---

## 5. Why this is the correct sequencing and governance

**Sequencing (see also §7 and the pilot doc):** system first as a small closed
commons; the currency emerges inside it; growth is community-to-community. A
standalone token is explicitly rejected.

**Governance:** trust-weighted, but capped against capture (gate 12). Capital may
earn and hold weight, never *capture* the rules. The one-person-one-vote floor
guarantees even the smallest member retains a voice.

---

## 6. Open items (honest)

These are *not* design flaws — they are decisions that require real pilot data,
and must not be fabricated in advance:

- **The magnitude of the parameters** (`α`, `g(d)`, `r`, `f`, `I`, grant size).
  The simulator proves the *structure* is stable across a wide band; the *point
  values* should be tuned to a live community's trading data, not invented here.
- **The in-network prices of the benchmark basket** (§2.6) — a community-specific
  calibration.
- **Identity verification for family/nodes** (gate 11) — a real-world primitive,
  not a maths problem.

---

## 7. Recommended path to reality

1. **Pilot one community** (`docs/CREDIT_COMMONS_PILOT.md`): ~24–100 members, a
   few real anchors, terminals or web checkout, the trust loop live.
2. **Collect real trade data** and **re-tune the parameters** the simulator
   proved structurally sound.
3. **Prove the equity spine in the field**: measure `Gini(trust)`,
   `poor_ok%`, grant frequency, reserve growth.
4. **Only then expand** community-to-community. Never launch a standalone coin.
