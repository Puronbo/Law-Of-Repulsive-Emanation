# The Credit-Commons: A Trust-Backed Mutual-Credit System

A self-contained design for a currency that *wins by use* — no external wallet,
no external money (after a one-shot seed), payable from merchant terminals with
only a recallable account number, where value is created by trade and given to
those who join and serve.

The system is a **living thing**: it uses the seed money of joiners to acquire
real stores and producers as in-network commerce, lets e-commerce enter through
the same door, and is engineered to survive and heal so the ledger stays online
even from a single surviving point.

Author note: written to be read in one sitting. Every section is a decision,
not a pondering.

---

## 0. The one-line law

**Money is the memory that you have served; trust is the permission to be
served before you have. Buying converts permission into memory; selling
rebuilds permission. Neither is external; every credit is a debt somewhere,
and every debt is allowed only to the depth of the community's trust in you.**

---

## 1. Two counters, never one

Every participant has exactly two numbers. They are coupled but opposite, and
must never be merged:

| Quantity | Meaning | Goes up when | Goes down when |
|---|---|---|---|
| **Credit** (the "money") | what you may/do spend | you sell (network owes you) | you buy (you owe the network) |
| **Trust** (the standing) | how far you may spend before repaying | you contribute/sell/refer | you draw down by buying |

- Credit is signed: positive = others owe you; negative = you owe the network.
- Trust is the **ceiling on negative credit**. You can buy down to
  `credit = -trust`, not beyond.
- Spending power = `trust` (roughly). Contribution rebuilds trust.

---

## 1.5 Tiers of entry (buy in by level/rank)

Entry is **by level, not flat** — an individual, a business, or a producer buys
in at different rank and receives different benefits. The trust/credit split is
the same; the **scale, gating, and governance weight** differ.

| Tier | Buy-in | Gets | Governs | Trade flow |
|---|---|---|---|---|
| **Individual** | smallest seed | personal credit + trust | 1 vote | peer-to-peer spend |
| **Business** (retail) | mid seed, merchant terminal | merchant fee-discounts, terminal-providing role, larger credit | weighted vote | sells to individuals, aggregates |
| **Producer** (manufacturer/agriculture/service) | largest seed, a store | can be **purchased with seed money** (§2.5), supplier role, biggest trust ceiling | largest weight | sells goods into the network, anchors supply |

- Buying in *higher* buys **more responsibility and more right to enable trade**,
  not more power to extract — the creative-benefit asymmetry is exactly the
  governance weighting. A rich individual cannot out-vote a producer by paying
  more at the same rank; they must *enter at a rank that makes them a producer*.
- **E-commerce joins through the same door**: an online shop buys in as a
  **Business tier**, plugs its terminal (web/API checkout) into the network, and
  settles in the same ledger. The one-shot seed + in-network-only credit rules
  are identical — e-commerce is just a terminal that happens to be a webpage.

### 1.6 Networks inside accounts (individualized nested ledgers)

A business or producer is not a single person — it is a **network of individual
accounts**, and its credit/trust is **appropriated by the system across those
individuals**, not by one controller. This generalizes the tiers into one
recursive rule: **every account can itself be a network of other accounts.**

- **A producer with workers = one producer-account whose members are the
  workers.** Each worker has their *own* individual account (credit, trust,
  voting weight). The producer's *collective* credit/trust is a **derived
  account** assembled from its members — not a private vault.
- **Who decides the split?** By the **system, objectively** — never by one
  person setting arbitrary wages. The split follows **measured contribution** to
  the network's trade:
  - portion of the producer's in-network output each member enabled (labor,
    procurement, delivery, validation, referral);
  - captured by per-member contribution counters, consensus-verifiable;
  - so "appropriation" = **a formula, not an order**.
- **The system is the honest arbiter:** because the appropriation rule is
  public, local, and computed from measured contribution, no member (not even
  the "owner") can capture the whole — a producer's credit is genuinely owned by
  the network of people who produce it.
- **Nesting is unbounded:** a business may hold stores, which hold staff; each
  store is its own derived account within the business, and the business within
  any larger cooperative. The recursion bottoms out at **individual accounts**
  (the only ones with a human face and a PIN).
- **Hard gate:** a network account must be **transparent and objective** — the
  contribution→appropriation rule is fixed and public, so "the system
  appropriates" means "the rule distributes by measured contribution," never
  "some overseer decides."

### 1.7 Family nodes (household accounts)

The unit that joins need not be an individual — it can be an **entire immediate
family**. Families connect into one shared unit (or many accounts bound into a
family group), which changes how grants and resource-sharing work, because real
people organize resources in households.

Two forms, both supported:

1. **Unified family account** — one handle/PIN for the whole household, spent by
   the unit, with member rules governing who may spend and how far.
2. **Family-bounded accounts** — each member keeps their **own** account
   (credible, trust, vote) but is **bound into a family group** that may:
   - **share resources freely** — transfer credit/trust among members within
     the group;
   - **receive grants as a unit** — a child's grant is computed against the
     family's aggregate standing, not a lone zero-history individual;
   - **pool governance weight** — the family votes as one household.

**Family is the standing sponsor.** The child-with-no-history problem of §2 is
solved structurally: within a family group, a child's trust is **derived from
the family's aggregate** until their own contribution earns them independent
trust. The family is the automatic, always-present sponsor, so a grant becomes
*usable* rather than *issued-but-stranded*.

**Sharing is the point.** Binding accounts into a family exists so members can
**share their resources with each other** — a parent funds a child's schooling,
a sibling's need, a household's purchase — with near-zero friction, because the
transfer is internal to the group.

**Hard gates:**
- A person may belong to **at most one** family group (no double-dipping the
  aggregate); leaving/joining is deliberate and auditable.
- **Family pooling requires a verification anchor.** "One family per person"
  and "no double-counting" cannot be enforced by a device-less PIN alone (a
  person could join many families) — so a family group must be **anchored by a
  trusted vouching member** (or a verified identity the community accepts), the
  same primitive §5 uses for sponsorship. Without such an anchor, **family
  pooling must be limited to credit-sharing only, never shared-trust mining**;
  the claim "one family per person is enforceable" is dropped, because
  device-less identity cannot guarantee it. This is the honest resolution of
  identity vs. pooling. **Crucially, the anchor is an enhancer, not a gate (E3):**
  an un-anchored individual's floor trust still lets them trade and be granted —
  family pooling adds, it does not exclude.
- **Shared trust is bounded and never infinite** — a family cannot mint trust
  for its members beyond what the aggregate actually holds, or grants become
  free leverage for everyone.
- The **individual always remains first-class**: binding into a family is
  optional and reversible; the individual account (their own trust, credit, and
  vote) does not vanish inside the family — it is *augmented* by belonging.

---

## 2. The lifecycle: three honest phases

This is the whole issuance story, and it is the part most such systems fail —
so it is gated and explicit.

### Phase 0 — One-shot seed (bounded, one-time)
- An entrant joins by a **single external→internal conversion**: they (or a
  sponsor) bring *outside* value once.
- In exchange they receive: a **credit line** (initial credit) and a **trust
  boot** (starting trust).
- **Hard gate:** this conversion is *finite and capped*. Outside money buys a
  starter credit + trust, **never compounding power**. Rich entrants cannot
  dominate by injecting more; the cap is per-account and permanent.
- Rationale: an external anchor at the *moment of entry only* answers "how does
  anyone start?" without making the currency externally pegged.

### Phase 1 — Self-funding ("the system gets lighter")
- Once circulation is robust, internal revenue — the facilitation fee `f` (§4),
  and the trust-rebuild earned by contributing — exceeds what new joiners need.
- From here, **new entrants are funded internally**, no outside money required.
- This is where "wins by use" matures: rewards flow from *inside* the system.

### Phase 2 — Redistribution (grants, progressive)
- With internal surplus, **accounts and trust are granted** to children, the
  unbanked, and those who cannot pay.
- Beneficiaries get: an opened account + a trust grant + a **sponsor** who
  vouches (a grant with no earning history needs a vouching guardian).
- **Grants are progressive (the goal of equity):** the smaller one's existing
  trust and credit, the larger the grant and the gentler the taper applied to
  it. The system **gives most to those with least**, so the floor trust (E3)
  lets even an un-anchored individual function — a verification anchor (family,
  sponsor) is an *enhancer* of grants and governance, never a prerequisite, or
  the unbanked are excluded at the door the system exists to open.
- **Donations** open *accounts and trust* for others. **Hard gate:** donations
  are **in-network credit donations**, not unlimited outside inflow — or the
  endogenous purity of Phase 1 quietly reverts to Phase 0.

### Phase 2.5 — Seed money becomes the economy itself
- The **collected seed money of joiners is not idle** — it is used to
  **acquire real stores and producers** that operate **inside** the system:
  buy a shop, a producer's output, a supplier. These become **in-network
  anchors** that reliably take payment in the currency, which is what makes the
  currency *buy real things* and therefore valuable.
- This is the strongest form of "wins by use": the money that *creates* the
  currency (the seed) also *guarantees what it can buy*. The commons owns real
  capacity, so the unit is backed by **actual stores and production**, not by
  faith or scarcity.
- **E-commerce enters the same way** — the seed/buy-in acquires or onboards
  online sellers as **Business-tier** anchors ($1.5), so the web is as native to
  the ledger as a physical terminal.
- **Hard gate:** acquired stores/producers must **accept in-network credit**
  and their output enters at **in-network prices** — otherwise the seed only
  creates an external-money backdoor and the "backed by real capacity" claim is
  false.
- **The circle is closed by a stated acquisition rule.** Spending *outside*
  seed money to buy a store hands outside money to the seller — so the purchase
  is a genuine use of the commons' capital, not a free lunch. It is **only a net
  win** if the acquired capacity **yields more spendable in-network value than
  it cost**, i.e. it must earn at in-network prices over its life. To keep this
  honest, the commons acquires capacity **preferentially from in-network
  sellers** (who accept the unit and keep wealth inside), sets a published
  in-network price for the acquired output, and treats any purchase as an
  **investment with a payback condition** — if the asset cannot pay back its own
  cost in in-network credit within a stated horizon, it must be released or
  re-priced, rather than held as a permanent capital sink draining the commons.

---

## 2.6 The unit: a benchmark, not a float (pricing / unit-of-account)

Every currency needs a defined **unit of account** — before this, "X units" and
all the `g`, `r`, `f`, grant, and in-network-price numbers have no meaning.
This section fixes it. Decision: **the unit is anchored to a benchmark basket of
in-network service, not to any external float.**

**The unit is a service-hour basket.** One unit is defined as the network's
median in-network service quantum — a fixed, published basket of common
in-network services (e.g. one standard repair, one standard transport leg, one
standard hour of a basic service). The basket is re-weighted by the network, but
**the unit never floats to an external price and is never redeemable for outside
money** — this is the price paid for full external independence, and it is
exactly what the ethos requires.

**Relative prices are local, not oracular.** Buyer and seller already agree
bilaterally on `X` for a trade (§3 step 1). Relative prices may deviate from the
basket (a skilled repair is worth more units than an unskilled hour) — the
basket fixes the *mean* unit, not each trade. No global price oracle is needed,
because low-frequency retail does not produce a liquid continuous price; local
agreement against a stable benchmark is enough.

**All constants cite the basket.** `g`, `r`, `f`, grant sizes, and in-network
anchor prices are expressed *relative to the unit* and audited against the
benchmark so a drift in the mean unit is corrected by re-weighting, not by
allowing the unit itself to float.

**Rejected alternatives, and why:**
- *External parity statement* (1 unit = 1 outside unit, Sardex-style accounting):
  pragmatically stable, but it keeps an external measure in the ledger's
  definition, quietly reintroducing the anchor the system removes in Phase 1.
  The commons may *measure* in any unit a community prefers, but the currency's
  unit is defined by the basket.
- *Endogenous float against an in-network goods market:* the only fully
  market-bearing option, but retail P2P has no liquid order-book to price it;
  building one is heavy machinery for an economy of small heterogeneous trades,
  and invites manipulation. Over-engineered for this system.

**Hard gate:** the unit must remain a **benchmark, never a redemption promise** —
if an in-network unit can be exchanged back into outside money at a fixed rate,
the external anchor returns and Phase 1's purity is broken (same failing as
gate 3).

---

## 3. The trade flow (atomic, escrow-free)

1. Buyer **B** and seller **S** agree a trade for `X` units.
2. Both authenticate on a terminal (merchant-provided): **account number +
   memorized PIN**, with a **short-lived one-time challenge** bound to the
   current time-slot and merchant (see §6).
3. The ledger, atomically:
   - `credit[S] += X`
   - `credit[B] -= X`   (rejected if `credit[B] < -trust[B]`)
   - `trust[B] -= g·X`  (draw-down; `g` small, the "trust drop")
   - `trust[S] += r·X`  (rebuild; `r` small, the "contribution reward")
4. A facilitation fee `f·X` is **charged to the trade and conserved** — it is
   not minted from nothing. It is split among the contributors who made the
   trade possible (terminal-providing merchant, referral chain,
   consensus/validation nodes, liquidity/trust holders), funded either from
   `credit[B]` as agreed or as a small spread in `X`, so total in-network credit
   is conserved across the trade.
5. Use *creates circulation*, not money out of thin air: emission is conserved —
   every unit in circulation is funded by a seed, a grant, or a settled trade's
   counterpart, never by an unbounded `f` free-mint. Any desire for supply growth
   is met by **grants (§2.5)**, not by dilutive mintage, so the unit's value is
   not silently inflated.

---

## 4. Compensation = "joiner's reward" (wins by use)

- The only way to **earn** is to **enable other people's trade**: route it,
  validate it, provide the terminal, refer a counterparty, or hold/back trust.
- The only place to **spend** is the network. So holding surplus is useless
  unless someone else can use it → the currency is *structurally* a medium,
  not a hoard.
- **Trust-weighted governance:** trust is not just borrowing power — it is
  **voting power** over the fee split `f` and dispute rules. The heavy
  contributors steer the rules, which is itself a form of being paid. **But
  weighting is capped against capture:** every **individual** vote is floored at
  one (no account's weight may dilute the smallest member below a fixed
  minimum), and no single account or family may hold more than a **hard cap** of
  the total vote. Trust weight must never let the heaviest contributors rewrite
  the rules to extract the pool — that would silently undo "owned by the
  network."
- **The fee split is capped per class with a use-side floor (E3):** capital
  contributors (terminals, referral networks, liquidity) may earn, but a floor of
  `f` is reserved for non-capital, use-side contributors — validation by small
  nodes, dispute participation, and active in-network consumers — so the people
  who merely *use* the network are never only paying into it.

### The privilege taper (soft anti-hoard, no tax, progressive)
- A **positive** credit balance held **idle for long** slowly has its trust
  *normalized downward* — not money decaying (Gesell's demurrage), but an
  **idle-surplus privilege taper**: unproductive surplus is gently discouraged.
- **The taper is progressive in surplus (E2):** negligible for modest balances,
  meaningful only for large idle hoards. A small saver is never punished; a
  large accumulator is gently pulled back toward use.
- Effect: use is the only durable way to hold status — and the poor saver is
  never penalized for not being a rich trader.

---

## 5. Trust — the algorithm's heart

Trust is primary; money is its shadow. Keep the rule **local and objective**:

```
trust_next = trust +  r'·(value contributed to others)     # r' = r·(1+α), positive-biased
                      - g(d)·(value drawn by buying)       # g progressive in depth d
                      - taper·(idle positive surplus)
                      - penalty·(unresolved dispute)
                      - I·(committed harm h)               # IRREVERSIBLE, r' cannot erase
                      + floor·(baseline regeneration)
                      + n·(in-network necessity consumed)  # necessity use REBUILDS trust

buy denied while  credit <= -trust.
```

- **Contribution** = selling, referring a new trade, validating, providing a
  terminal, **consuming in-network necessity**, or vouching (sponsorship).
  **Necessity consumption counts as contribution**, not as pure draw-down —
  a person buying food, medicine, or transport in-network carries the network
  just as a seller does, so it must not erode their standing.
- **Positive action is weighted in magnitude — the `r'` bias (α > 0).** The
  reward for contributing carries a positive bias over the raw value, so an
  active, honest member's trust *trends upward*: being constructively engaged is
  better than being passive. This is the "weight positive more heavily" half —
  generosity toward use.
- **Negative action is weighted in kind — the `I` irreversibility.** A committed
  harm `h` (fraud, default, abuse of a rejected draw) imposes a hard `I` term
  that **positive reward `r'` cannot erase** — exactly as irreversibility in
  nature cannot un-burn the toast. It carves a permanent notch in trust that only
  very slow, hard redemption lifts, and never fully resets. This is the "weight
  negative more heavily" half — but in *reversibility*, not in magnitude, so one
  misdeed cannot be laundered by a lifetime of later kindness while still cost- 
  meaningful over leverage (bound via `g(d)` above). Balanced: constructive actors
  are pulled up and in; abusers carry a scar positivity can never wipe away.
- **Draw-down `g` is progressive in depth, not flat.** The deeper one goes into
  negative credit, the higher `g(d)` becomes; at the necessity baseline `g` is at
  its floor. This bounds how far anyone may over-leverage (stability) while
  *not* punishing the poor consumer who must draw to live (equity). See §5.5.
- **Trust has a regenerating floor.** Because *selling* is the main trust
  rebuilder, and *buying* needs trust, a pure contribution loop can cold-start-
  stall or statically concentrate in the already-trusted. The `floor` term
  **regenerates a small baseline trust over time regardless of sales**, and
  non-sales contributions (validation, vouching, referral) count fully toward
  `r` — so trust is earned by *serving the network*, not only by having sold.
  This is the antidote to a rich-get-richer static equilibrium.
- **Draw-down drop** is *committed and painful to reverse* for a **lockout
  period** unless the value is returned (fraud deterrent). Actual **harm**
  (fraud, default, abuse) goes further: it is not merely locked out for a period
  but scored by the **irreversible `I` term (see §5.6)** — positive reward cannot
  wipe it away.
- New/child accounts: trust starts at a **low baseline** and is raised by a
  **sponsor's voucher** — so grants are usable without being infinite.

---

## 5.5 Equity — the pro-poor spine (applies to every trade, every account)

The system pursues **equity for all**, not just stability. Stability with a
regressive bias is concentration dressed as order. Every mechanism that touches
all accounts is therefore governed by three equity rules, so the design's tail
(who ends up with standing) is not silently shaped by who started rich.

**E1. Consumption of in-network necessity is contribution, never cost.**
The person buying food, medicine, transport, or schooling in-network carries the
network as much as the seller. Such use: rebuilds trust (the `n` term), does
not invoke the progressive `g(d)` at its deep floor, draws against a
**necessity-protection ceiling** (a reserved fraction of trust immune to the hard
gate, so the poorest always meet basic needs), and is immune to the idle-surplus
taper (one cannot be penalized for spending to live). A network that punishes its
neediest active members is not equitable, and it is not stable — it loses them.

**Necessity protection is two-part, and that is the honest division (validated
by simulation):** the `n` term protects **standing** (the needy are never
penalized for needing), while the *credit* they draw is **real debt that the
commons collectively funds via Phase-2 grants** from the reserve. This is
deliberate: a never-contributor cannot be given *unlimited* credit (that is the
sybil/free-money hole gate 1 forbids), so the network protects their dignity and
their ability to live while using the commons surplus — not infinite leverage.

**E2. The draw-down `g(d)` and the taper are progressive, never flat.**
- `g` rises with *depth of borrowing*, so over-leverage is bounded (stability)
  but the shallow, necessary borrowing of the poor is near-free (equity).
- The idle-surplus taper is **progressive in surplus**: it stays negligible for
  modest balances and only grows for *large* hoards. A small saver is never
  punished; a large idle hoarder is gently discouraged. This is the opposite of
  the naive flat taper, which would nick the poor saver while sparing the rich
  accumulator.

**E3. The `f` fee and governance weight prefer use over holdings.**
- The facilitation fee's split is **capped per contributor class**, and a
  **floor of the fee is reserved for non-capital, use-side contributors** —
  validation by small nodes, dispute participation, and active in-network
  consumers. Capital (terminal-holding, referral networks) may earn, but it may
  not *capture* the split, or "wins by use" becomes "wins by having."
- Governance weight already enforces a **one-person one-vote floor** and a
  **hard per-account/family cap** (gate 12); under E3 the cap is the *default*
  guarantee of equity, not an exception.

**Why equity is also stability.** A regressive trust loop drives the poor out
(the buyer whose trust erodes, whose taper cuts), shrinking the network's active
base and concentrating standing in a few. The pro-poor spine keeps the broadest
set of active members solvent and trusted — which is what a mutual-credit network
*is*: the wider and more equal the trusted base, the more trades clear, and the
more stable the whole. Equity here is not charity layered on top; it is the
load-bearing condition of the network's own survival.

---

## 5.6 Asymmetry of action — positive weighted in magnitude, negative weighted
in kind (the natural philosopher's law)

**Known realities, applied.** Thermodynamic irreversibility is the first known
reality: a reversal you can *buy back* is not a cost. You cannot un-burn the
toast with a later good deed. The second known reality is the empirical failure
modes of real mutual-credit/LETS systems: weight positive too lightly and no one
stays engaged; weight negative too lightly and free-riders and abusers unravel
the pool. The stable attractor is neither — it is the **two-sided asymmetry**:

- **Positive (constructive) action is weighted heavily in MAGNITUDE.** The
  reward carries a positive bias `r' = r·(1+α)` with `α > 0`, so an active and
  honest member's trust *trends upward* over time — being constructively engaged
  is genuinely better than being passive. Use is rewarded generously.
- **Negative (harmful) action is weighted heavily in KIND (irreversibility).** A
  committed harm `h` — fraud, default, abuse of a rejected draw-down — imposes a
  hard `I` term that **positive reward cannot erase**. It carves a permanent
  notch in trust that only very slow, difficult redemption lifts, and never
  resets to zero. One cannot launder a serious misdeed with a lifetime of later
  kindness.

This is the correct reading of "weight positive against negative more heavily":
positive action dominates in *magnitude of reward*, negative action dominates in
*irreversibility of cost*. Both pull toward constructive behavior, and neither is
symmetric. It does not contradict equity (§5.5): the irreversible `I` targets
**choice-harms** — fraud, default, abuse — never the necessity-consumption of the
poor, which is protected as positive action (E1). The poor consumer is helped;
the free-rider is scarred; the honest engaged member rises. The physics, the
economics, and the ethics agree: **rewards pull, debts scar.**

---

## 6. Security with "a few numbers, no device"

The hard truth: memorizable secret = low entropy = brute-forceable. The design
survives because **it is *never* offline cash**:

- Authentication is always **live** against the ledger: per-account **rate
  limit**, **per-account throttle**, and a **short-lived one-time challenge**
  (time-slot + merchant bound).
- Every credential used is **revocable and short-lived**; a stolen token dies
  in seconds and cannot replay.
- There is **no storable crypto-token to seize** — the money is a *directed
  credit on a replicated book*, revoked by notarizing a replay/fraud and
  re-running consensus. A stolen PIN costs, at most, the draw-down limit of a
  throttled, revocable account.
- **The merchant's untrusted terminal never holds long-term secrets** — only
  one-time, expiring, use-once challenges.

---

## 7. The epoch anchor (settled honestly)

**`2000-10-26T10:26:20.000Z`** is adopted **once, as the documented genesis
epoch** — the single fixed, public, reproducible anchor:
- genesis timestamp and protocol birthday;
- the seed for **deterministic, reproducible** random/testing constants;
- the origin from which all **time-slots** (used in one-time challenges) and
  **transaction-ids** are derived.

**Hard rule / caution:** the epoch is a *conventional constant*, exactly as
strong as any other deterministic epoch. Its digits are **not** treated as
cryptographic material — they are public, so they must never seed secrets,
generate identities, or "strengthen" the ledger. Using *coincidence* as
security would be fragility; using *determinism and auditable reproduction* is
infrastructure strength. The digits earn their place only as a stable, cited
boundary condition.

---

## 7.5 A living thing that survives being destroyed

The system is designed to **not die when people attack or abandon it** — it is
a living ledger, not a shrine.

- **Everything is replicable and self-healing:** every node keeps a full
  history; any node that reappears is **caught up by any surviving peer**; any
  surviving point (even one) can **regrow the network**, because the ledgers and
  rules are not owned by any single host.
- **Single-point persistence:** the protocol must be able to **keep the ledger
  online from a single point** — one honest node can serve the whole book and
  accept writes while the network heals. This means: no single-vendor lock-in,
  no "dead because the server is gone," no "dead because the founder left."
- **Lone-survivor authority is provisional, not final.** A single point may
  *accept writes and serve the book* (availability), but it is only
  **provisional authority**: its writes are **ratified on rejoin** by any
  surviving peer, and double-spend is prevented by hashing each write onto the
  prior chain so two survivors cannot diverge without a detectable fork. The
  survivor alone can keep commerce alive, but it cannot *unilaterally* finalize
  governance rule-changes or rewrite history — those require the network to
  reconvene. This resolves the tension between "always writable from one point"
  and "no single host owns the rules."
- **Swarm ownership of anchors:** the stores/producers purchased with seed money
  are **collectively owned by the commons** ($2.5) — so if individuals leave or
  are lost, the real economy they bought **remains with the network** and keeps
  accepting its currency. The system's wealth does not die with its members.
- **Liveness as a hard requirement:** the ledger must be **fork-free and always
  writable** — if a survivor cannot write, the system is dead; therefore
  availability and recovery are treated as *infrastructure*, not options.
- **Graceful degradation by rank:** if the network shrinks, the **tiers** ($1.5)
  collapse first and the core commons last — a producer's anchor survives an
  individual's exit, so the "living thing" sheds members, not the system.

---

## 8. Hard gates that cannot be waived (the "if `X` then you fail" list)

0. **The unit is a benchmark, never a redemption promise** — it is anchored to an
   in-network service basket, never exchangeable back into outside money at a
   fixed rate, or the external anchor returns and Phase 1's purity is broken.
1. **One-shot seed must be capped** — else outside money becomes power forever.
2. **Donations must be in-network credit** — else Phase 1 reverts to Phase 0.
3. **Seed-bought stores/producers must accept in-network credit at in-network
   prices** — else the "backed by real capacity" claim is a false backdoor.
4. **Trust must be spendable-only** (can't be hoarded as a weapon) and
   **bounded** — so no single actor can wreck the pool.
5. **Draw-down drop is committed + lockout** — else buy-and-flee is free.
6. **Mintage is conserved** — the facilitation fee is charged to the trade, not
   minted ex nihilo; supply growth comes from grants, not dilutive free-minting,
   or the unit's value is silently inflated.
7. **Ledger must be fork-free and always writable from any single surviving
   point** — availability and recovery are infrastructure, not options.
   Lone-survivor writes are **provisional and ratified on rejoin**; a lone point
   can serve commerce but cannot unilaterally finalize rule-changes.
8. **New/child accounts need a sponsor** — a grant with no earning history is
   unusable without a vouching guardian.
9. **Tier buy-in buys responsibility and weight, not extraction** — a higher
   rank must come from becoming a producer/anchor, not from paying more at the
   same level.
10. **Network appropriation is the rule, not the person** — a business/producer's
    credit is distributed among its member accounts by a public, objective,
    measured-contribution formula; no single owner may capture it, or the
    "owned by the network" claim is false.
11. **One family per person, shared trust is bounded** — no double-counting the
    aggregate, and the family is the standing sponsor for its members' grants
    without minting unbounded leverage.
12. **Governance weight is capped against capture** — every individual vote is
    floored at one and no account or family may hold more than a hard cap of
    total vote, so the heaviest contributors cannot rewrite the rules to extract
    the pool.
13. **The pro-poor spine is load-bearing, not charity** (§5.5) — necessity
    consumption rebuilds trust; `g` and the taper are progressive; the `f` split
    reserves a use-side floor; grants give most to those with least; and a
    verification anchor is an enhancer, never a prerequisite. A regressive trust
    loop is forbidden, because it drives the neediest members out and
    concentrates standing — which is both inequitable *and* unstable.
14. **Positive is weighted in magnitude, negative in irreversibility** (§5.6) —
    constructive action carries a positive bias `r'=r·(1+α)`; committed harm
    carries an irreversible `I` scar that reward cannot erase. Without both, the
    system drifts to free-riding (little negative weight) or desertion (little
    positive weight); with both it pulls toward constructive action. The `I` term
    targets choice-harms only, never necessity-consumption, so it strengthens
    rather than contradicts equity.

---

## 9. The picture in one paragraph

The system is a **trust-backed mutual-credit commons**. It is seeded **once**
per entrant by a capped external conversion — bought in by **tier**: individual,
business, or producer, each gaining proportionally more right to enable trade
and a larger governance weight. Every account can itself be a **network of
individual accounts** — a producer's credit is appropriated among its workers by
the **system's own measured-contribution rule**, not by a single owner, and
nesting recurses down to the individual (the only account with a human face and
a PIN). The smallest meaningful unit is the **family**: whole households join as
**family nodes** — members keep their own accounts but are bound into one group
that shares resources, pools its vote, and is the **standing sponsor** for its
children's grants. The collected seed money is then spent on **real stores and producers
owned by the commons**, which accept the currency at in-network prices and give
it actual purchasing power; e-commerce joins through the same door as a
Business-tier anchor. Its unit is a **benchmark service basket** — defined
in-network, never redeemable for outside money, with relative prices set
bilaterally against it (§2.6). The system becomes **self-funding** as
its internal fees out-grow its needs, then **redistributes** by granting
accounts and trust to children and the unbanked (funded by sponsors and
in-network donations). Spending is bound by trust; trust is rebuilt only by
serving — and by **consuming in-network necessity**, which carries the network
just as selling does. **Equity is the spine, not charity**: the draw-down and
taper are **progressive** (the poor consumer is never penalized for living; the
large idle hoard is gently pulled back to use), grants **give most to those with
least**, and the fee split reserves a **use-side floor** so the people who merely
use the network are never only paying into it. **Action is asymmetric both ways
(§5.6)**: positive action is weighted in **magnitude** — the reward `r'=r·(1+α)`
makes the honest, engaged member's trust trend upward — while negative action is
weighted in **irreversibility** — a committed fraud or default carves a permanent
scar that no later kindness can erase. Surplus idling is gently tapered;
the people who enable the most trade steer the rules and are paid for doing so.
The whole thing runs on a
merchant-provided terminal (or a webpage) with a recallable account number and a
PIN, secured not by secrecy but by throttled, revocable, one-time online
challenges, anchored to a single documented genesis epoch —
`2000-10-26T10:26:20.000Z`. It is a **living thing**: replicable, self-healing,
collectively owning its anchors, and able to keep the ledger online from any
single surviving point. Money is the memory of service; trust is the permission
to be served; use is the only law.
