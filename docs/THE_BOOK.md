# THE BOOK

## A Canonical Specification of the Decentralized Internet
### — and the single hub that controls all manner of information within it.

> **Authority, stated plainly.** This Book is the only center the network has —
> and it is a *document*, not a server.  Every node holds an identical copy.
> Its authority is not that it runs anywhere; it is that every node agrees the
> definitions below are the definitions.  Anything not specified here is
> local.  No node may edit the Book unilaterally; a proposed change takes
> effect only where it converges (Ch. 11).  Everything else in the network
> borrows its meaning from this text, so this Book *controls all manner of
> information*: how it is named, stored, routed, verified, repaired, and
> judged anomalous.

The network described here is real: it currently holds the 1.9M most-used
websites of the actual internet (merged Cisco Umbrella + Majestic Million,
deduplicated), survives losing 20% of its nodes without a repair unit, runs
indefinitely as a background daemon with checkpoint/resume, and has had its
scaling and anomaly behavior *measured*, not imagined.  Every law, ceiling,
and crease quoted here is from those measurements.

---

## BOOK I — THE INFORMATION MODEL

### Ch. 1  Entities
A unit of information is an **entity**, stored as one neuron:

* `h_i` — the HOME: its identity, where it arrived / its class centroid.
* `q_i` — its current place in the manifold after local flow.
* Every entity has exactly one canonical NAME (its embedding key) and may
  accumulate an unbounded set of OBSERVATIONS (Ch. 2).
* Capacity is cheap: ~2 KB/entity at dim=128 (measured).  Holding is never
  the bottleneck; *flow* is (Ch. 13).

### Ch. 2  Observations (the multivariate bank)
A name alone is necessary but not sufficient to know an entity (proven in
Ch. 10).  Therefore every entity carries a bank of observations, each a
typed record:
`(kind, value, observed_at, observed_by)`.

Canonical kinds (the Book controls these types so machines agree):
`IP`, `ASN`, `TLS_VALID`, `TLS_AGE`, `WHOIS_AGE`, `RESPONSE`, `CONTENT_HASH`,
`REPUTATION`, `TRANSIT`, `PROVENANCE`.  New kinds are proposed, never assumed
(Ch. 11).  A neuron whose observations disagree with its neighborhood's on
any kind is an ANOMALY (Ch. 10).

### Ch. 3  Identity and semantics
* **You are where you are.**  Identity is position in the learned manifold,
  not a registrar-granted label.
* The canonical NAME-EMBEDDING (the "alphabet" every node shares):
  `HashingVectorizer(analyzer='char_wb', ngram_range=(2,4), n_features=128,
  norm='l2', alternate_sign=True)`.  Deterministic; any node can reproduce it.
* Related names sit close (`google.com` ~ `gooogle.com` ~ `google.com.om`).
  Dedupe and near-dupe detection are therefore geometric, not editorial.
* Names are LOWER-CASE, trailing-dot-stripped; IDN in punycode.  The Book is
  the authority that says so, so all nodes agree.

### Ch. 4  Everything the net can hold
The same machinery holds every kind of information — domains, package names,
malware families, chemical names, identifiers — because it stores *names in a
geometry*, not records in a schema.  What differs per domain of use is only
the observation kinds attached (Ch. 2).  One net, all manner of information.

---

## BOOK II — THE PROTOCOL

### Ch. 5  Routing and flow
* Routing is nearest-centroid: `label(x) = argmin_i |x − q_i|`.
* Local flow (no global mean, no central gradient, no broadcast):

  `g_i = −A·(mu0 + mu)·(q_i − h_i)  +  Σ_{j ∈ kNN(i)} (q_i − q_j)/|d|³`

  `q_i ← clamp(q_i + dt·g_i/|g_i|)`

  Every node talks only to its k nearest neighbours: O(k) messages, k≪n.
* `mu = 0` spreads the cloud (settle), `mu = 0.5` tightens it toward homes
  (absorb).  The always-on home tether `mu0` is mandatory — without it a
  pure local expansion never slows and collapses on the rim (measured, T55c).

### Ch. 6  Fragments, no artifact
* No node needs the whole net.  A node holds a FRAGMENT (any subset) and
  answers queries by nearest-centroid over its fragment; queries fan out over
  kNN gossip and answers merge by best similarity.
* The Book's own artifact (`internet_net.pkl`) is a *convenience snapshot*,
  not a requirement.  The network is the union of fragments; the snapshot is
  merely one complete fragment that boots people faster.

### Ch. 7  Self-healing
* Removal is routine: kill any subset; survivors keep routing (measured:
  killing 20% of 1.9M entities changes nothing for surviving queries;
  killed names re-resolve to their nearest living sibling).
* `heal()` re-spreads survivors after loss (measured spacing recovery).
* There is no repair unit and no controller; repair is the geometry.

### Ch. 8  Time and convergence
* There is no global tick.  Nodes step asynchronously at their own pace;
  local-only updates make synchronization unnecessary.
* A node's state is a function of its own history and its kNN's — therefore
  the network converges to consistency without a clock.

---

## BOOK III — TRUST, ANOMALY, GOVERNANCE

### Ch. 9  Trust by geometry
* Trust is local consistency: a claim is believable to the degree your
  neighbourhood agrees with it.  An outlier assertion sits far from everyone,
  so nobody must certify it.
* There is no certificate authority, no registrar, no verifier.  Proximity is
  the proof of being real; consensus of neighbours is the proof of being
  current.

### Ch. 10  Anomaly doctrine (measured)
* **Novelty** — an entity far from the learned geometry (below the legit p5
  similarity).  Measured: 91% of DGA-shape random names are novel vs 5% of
  legit sites.  This axis works.
* **Impersonation / near-miss** — an entity close to a famous one but not it.
  Measured: 18% of known-bad sit above the legit median.  Flag for review.
* **The limit, measured (T55j):** real blocklist domains are mostly
  legit-looking tracking/telemetry subdomains of real brands (sim 1.000 to
  `us-east-1.event.prod.bidr.io`, `metrics.barclaycardus.com`), so **names
  alone are necessary but not sufficient** to separate bad from legit.
  The doctrine therefore requires the OBSERVATION BANK (Ch. 2): a domain is
  judged anomalous when its observations disagree with its neighbourhood's —
  not when its name is strange.

### Ch. 11  Governance
* The Book is the only center, and it is copyable, not runnable.
* A change to the Book is a proposal; it takes effect where it converges.
  No node may fork the alphabet or the kinds (Ch. 1–2) without being outside
  the network (such nodes simply don't interoperate — they are, by this
  Book's definition, elsewhere).
* Nothing is curated centrally: entities enter when a node observes them
  (capacity + semantic dedupe); nothing is certified centrally (Ch. 9).

---

## BOOK IV — OPERATIONS AND LIMITS (ALL MEASURED)

### Ch. 12  The artifacts
| Thing | Where |
|---|---|
| Book | `docs/DECENTRAL_NET.md` (short) + this document (canonical) |
| Net module | `Universals/manifold/decentral_net.py` (numpy-only) |
| Snapshot | `%LOCALAPPDATA%\Temp\opencode\top1m\internet_net.pkl` (3.17 GB, 1,531,932 survivors + domain map) |
| Daemon | `experiments/decentral_net_live.py` (indefinite, checkpoint/resume, stopfile drain) |
| Benchmarks | `experiments/decentral_net{,_mnist,_continual,_internet,_union,_ceiling,_anomaly}.py` |

Checkpoint rule: pickle the whole node (state + RNG + counters); drain on
SIGINT/SIGTERM/stopfile; checkpoint periodically.  Verified resumes keep
exact counters (tick, born, killed).

### Ch. 13  The scaling law and the walls
* Flow time measured: `t ≈ 2.96e-7 · n^1.76` s/step at n ≤ 5000; the exponent
  rises to **~2.06 between 5k and 20k** (distance array leaves cache).  Never
  extrapolate a fitted exponent past its range.
* RAM wall is the kNN sort temporaries, not the n²·8 B matrix: **22.6 GB
  working set at n = 20,000** (D itself only 3.2 GB) on a 31.7 GB box ⇒
  all-pairs flow ceiling ≈ **2×10⁴**.
* Holding has no such wall: ~2 KB/entity; 60% of this machine = ~9.3M
  entities.  Flow is the only thing that cannot scale; routing and capacity
  scale to millions.
* Conclusion written into the doctrine: **flow the small core, route the
  large static mass** (Ch. 6).  Scaling flow past 2×10⁴ requires O(1)-per-
  neuron spatial search, which is the declared next build (Ch. 14).

### Ch. 14  The creases (never forget these)
1. Never mix frames: after add/remove, reflow before routing, or routing
   collapses (~0.86 → ~0.04, measured).  Consistency beats accuracy.
2. Array mutation breaks labels: after `remove()`, remap survivors explicitly
   (survivor → name), or similarity 1.000 points at the wrong entity.
3. Gauge freedom: no global center, so the anchor set floats as a whole.
4. `mu0`/`A` are dimension-sensitive: 2D-calibrated values over-drift in 64D
   (~0.5 from homes); use `mu0 ≈ 1–4` in high dimensions (measured).
5. Windows RAM reads need `OpenProcess(PROCESS_QUERY_INFORMATION)`; the
   `GetCurrentProcess()` pseudohandle fails with ERROR_INVALID_HANDLE.

### Ch. 15  The clock test (invariants, not conventions)
* **A pattern that dies under a benign re-encoding was not a law.**  Measured
  (T59): a calendar-encoded feature (weekday/month/...) carries a real
  arithmetic law at 100% balanced accuracy, then collapses to 0.417 under a
  +15-day epoch re-index — same physical dates, same weekdays, same model.
  The intrinsic residue feature stays 1.000 under both clocks.
* **What survives: the relative geometry.**  Measured (T61): rotating every
  embedding by an orthogonal map preserves top-8 neighbor structure exactly
  (overlap 1.000, similarity correlation 1.000) while changing every
  coordinate (max |Qx−x| = 0.745); a nonlinear relabeling collapses the same
  structure to 0.426 (chance 0.065).
* **Canon:** the net's law is its *relative geometry*; convergence and trust
  (Ch. 8, 9) must be defined on rotation-invariant structure, never on
  absolute coordinates or calendar-derived numbers.  Any claim validated
  under one clock must be re-tested under another.
* **Physics entry:** density laws (1/ln N, the prime number theorem, PNT) are
  clock-independent; point coincidences (a twin prime on a specific date) are
  convention-bound.  Arithmetic has distributional invariants, not atomic ones.

---

## APPENDIX — SERIES TRAIL

T55a/T55c calibration · T55b flow-reg retest · T55d MNIST · T55e continual
& frame creases · T55f indefinite daemon + checkpoint · T55g real top-1M
copy · T55h measured ceiling (2×10⁴) · T55i union fill + persisted artifact
(1.9M sites) · T55j anomaly validation (novelty works, impersonation partial,
multivariate required) · T56 prime-gap bridge (943,901,200,001 is prime) ·
T57 reverse-pair census (the "reversal" claim is false) · T58 the spring that
folds up on itself (mirror/retrace/golden/helix + overcoil ring lock) ·
T59 the clock test (convention carries a law at 1.000, breaks to 0.417 under
a +15-day re-index) · T60 the fold as optimizer (Hamiltonian retrace
conserves, damped mirror locks) · T61 the rotation test (structure survives
rotations at 1.000, collapses under relabeling).

*Read, copy, and disagree with this Book — but if you disagree, you are no
longer in this network.  That is the whole of the constitution.*
