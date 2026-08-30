# The Credit-Commons Pilot Framework

A concrete, honest plan for taking the design (`docs/CREDIT_COMMONS.md`, with
the validated simulator in `credit_commons/`) into a small real community. The
pilot exists to **tune the parameters and prove the equity spine in the field**,
not to launch a currency.

Reference: `docs/CREDIT_COMMONS_PROPOSAL.md` §7 — pilot one community, collect
real trade data, re-tune, prove equity, then (and only then) expand.

---

## 1. Objectives (ranked, non-negotiable)

1. **Prove the equity spine with real people** — the poorest member must be able
   to meet basic needs with preserved standing (gate 13) and without being asked
   to do something unfair.
2. **Tune the free parameters from data** — `α`, `g(d)`, `r`, `f`, `I`, grant
   size. The simulator proves structure; the field fixes magnitude.
3. **Prove the asymmetry** — contributors visibly rise; abuses visibly scar
   (gate 14).
4. **Do not** create an inflationary free-money sink; do not let a rich member
   capture governance (gates 1, 6, 12).

---

## 2. Choosing the pilot community

The community is the unit, not a market. Criteria:

- **Bounded and known**: 24–100 members (the simulator's tested scale), a
  defined geography or trade-group with existing relationships (a cooperative,
  a farming association, a local merchant guild, a housing cooperative — not an
  anonymous open crowd). Known relationships give honest trust anchors.
- **A real recurring need** the commons anchors serve — food, transport,
  repair, care — so the unit has daily *use*.
- **At least 2–5 real anchors** (§2.5) willing to accept the unit at published
  in-network prices: a shop, a repair/service provider, a producer. **These are
  the load-bearing reality** — the unit is worth something *because* they accept
  it.
- **A mix of tiers** — a few businesses/producers, many individuals, and
  deliberately **some who are economically vulnerable** (to test the equity
  spine rather than assume it).

---

## 3. Onboarding (Phase 0 — one-shot seed)

- Each member buys in **once, capped** (gate 1): a small seed that opens a credit
  line + trust boot.
- **Tiers** (§1.5): individual / business / producer. Higher tier buys
  responsibility/weight, not extraction (gate 9). E-commerce joins as Business.
- **Families** (§1.7): whole households join as family nodes; a child's trust is
  derived from the family aggregate (standing sponsor, gate 8/11). **The anchor
  is an enhancer, not a gate** — an unanchored individual's floor trust still
  lets them function.
- **Grants first**: before judging equity, *give* accounts + trust to those who
  cannot pay (children, unbanked). Progressive grants give most to those with
  least (gate 13).

---

## 4. Running the loop

- **Terminals or web checkout** only; account number + memorized PIN; short-lived
  one-time online challenges — **never offline cash** (§6). Credentials are
  revocable and throttled; a stolen PIN dies in seconds and costs at most the
  draw-down of a throttled account.
- **Necessity is protected** (E1): a reserved trust fraction covers food/
  medicine/transport; the commons grants credit for it from the reserve, so no
  one starves and no one gets free unlimited leverage.
- **Action asymmetry live** (§5.6): contribution rewards bias upward
  (`r' = r·(1+α)`); fraud/default scars irreversibly (`I`).

---

## 5. Equity gates the pilot must hold

These are observed, not assumed:

- **Gini(trust) stays low** (target ≈ 0.1–0.3, the simulator's structural band
  at 0.05–0.13; widen only if justified by data).
- **poor_ok% = 100%**: no member's trust is driven below a living threshold by
  necessity spending; grants keep true non-contributors fed *without* granting
  unlimited credit (no sybil hole).
- **The fee keeps a use-side floor** (E3): active consumers are paid for being
  active, not only capital providers.
- **Governance cannot be captured**: one-person-one-vote floor + per-account cap
  (gate 12) verified in how the fee split and dispute rules actually change.

---

## 6. What to measure (the pilot's output)

| Metric | Why | Target |
|---|---|---|
| Gini(trust) over time | no runaway concentration | 0.1–0.3 |
| poor_ok% | equity spine | 100% |
| Grant frequency per non-contributor | calibration of grants vs. free-money | moderate, data-driven |
| Reserve growth | commons self-funds Phase 2 | positive, not runaway |
| Trades per member per week | `wins by use` flywheel turning | rising |
| Abuse/fraud events & scar effects | asymmetry working | low, visibly scarred |
| Fee split received by consumers | E3 use-side floor real | non-trivial share |

**Decision rule for the pilot's end:** the pilot succeeds if, after one full
credit cycle, the equity metrics hold *and* the parameters are tuned. It is then
**expanded to a second community** — never marketed as a new coin.

---

## 7. Guardrails (when to stop or correct)

- If `Gini(trust)` trends toward 1 → the floor/progressive-`g` needs raising;
  halt expansion, fix the loop.
- If grant frequency explodes (near-freeloading) → grants are doing the work of
  credit; rebalance toward contribution rewards (gate 14's spirit).
- If a member acquires a governance majority → gate 12 is broken in practice;
  halt, re-cap, restore the floor.
- If anchors stop accepting the unit → the "backed by real capacity" claim
  (gate 3) has failed; that is the single most serious red flag, and it ends the
  pilot unless anchors are restored or re-priced.

---

## 8. Cadence

- **Weeks 1–4:** recruit community, onboard tiers + families, seed once, stand
  up 2–5 anchors, open grants.
- **Weeks 5–16:** run the loop; measure weekly (metrics above); re-tune `α`,
  `g`,`r`,`f`,`I`, grant size monthly from the data.
- **Week 16 review:** hold all §5 gates or fix; if held, decide second community.

The pilot is a *living experiment*, consistent with the design's own self-image:
replicable, self-healing, collectively owned — and it sheds members, never the
system.
