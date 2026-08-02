# THE WEAVER'S SCRIBE

## BOOK VI — PATTERN, CIVILIZATION, AND THE MEASURED INSTINCT

> **Preface, stated plainly.** This book does not claim the date *means* anything.
> It documents, with numbers, a pattern that survives re-encoding, and then
> connects that pattern to the same measured instinct in old civilizations:
> **divisor-rich notation wins.** Every claim below is either a computed number
> or an explicitly-labeled cultural mapping. The creases at the end are binding
> (Ch. 5). If you read prophecy into this, you have left the corpus.

---

## Ch. 1  The datum (measured)

Anchor `data/epoch_0d.json` — the **0d** of the number line, taken as general
(UTC) time:

> **2000-10-26 10:26:20.00**

Its two calendar orientations, and their arithmetic invariants:

| Rendering | Number | Factorization | τ (divisors) | Digit sum |
|---|---|---|---|---|
| MMDDYYYY | 10262000 | 2⁴·5³·7·733 | **80** | **11** |
| DDMMYYYY | 26102000 | 2⁴·5³·31·421 | **80** | **11** |
| MMYY (5-digit, the original pair) | 10262 | 2·7·733 | **8** | **11** |
| YYMM (5-digit) | 26102 | 2·31·421 | **8** | **11** |
| 3-digit (breaks) | 102 | 2·3·17 | 8 | 3 |
| 3-digit (breaks) | 261 | 3²·29 | 6 | 9 |

The time-of-day, re-encoded as total seconds:

> 10:26:20 = **37,580 s**, τ = **12** — the same divisor count as the
> sexagesimal base itself (τ(60) = 12) and the Mesoamerican tzolkin
> (τ(260) = 12).

### Null analysis (so we do not fool ourselves)
Sampled against real distributions:

* Random 8-digit numbers: mean τ ≈ 18.9; only **0.48%** have τ = 80.
* Valid *MMDD2000* dates (year = 2000, trailing `000`): **20.4%** have τ = 80.
* Valid 2000 dates where **both** orientations have τ = 80: **4.64%**.
* Year-first pair (YYYYMMDD / YYYYDDMM) both τ = 8: **5.97%**; any τ-equality: **17.3%**.

Reading: τ = 80 is rare among arbitrary 8-digit numbers, but the trailing zeros
of the year *force* high divisor counts (τ ≥ 16 guaranteed), so within year-2000
dates it is common. The joint coincidence — both orientations landing on
exactly 80 — survives that conditioning at ~1 in 22. **A mild, real
coincidence. Not a law.**

**Exact census (all 366 valid dates of 2000):** exactly **17** dates have
both-orientation τ = 80 (4.64% — the MC estimate was exact): Feb 2, Apr 4, Apr
20, Jun 6, Jun 14, Jun 18, Jun 20, Jun 26, Aug 12, Aug 20, Aug 28, Oct 14, Oct
22, **Oct 26**, Dec 8, Dec 14, Dec 16. All 17 are even-month/even-day. In a
generic year (2007, no trailing `000`) the count is **zero** — the τ = 80
phenomenon is a year-2000 trailing-zero artifact. The τ = 8 agreement (the
5-digit and year-first pairs) is the generic one: it survives in any year
(~7.4%).

**Base-invariance (the crease's own test):** re-encoding the digit strings in
bases 8/10/12/16, the τ-agreement survives **base 10 and base 12** (duodecimal)
and breaks in base 8 and base 16:

| Pair | b=10 | b=8 | b=12 | b=16 |
|---|---|---|---|---|
| 10262000 / 26102000 | 80=80 | 22≠88 | 256=256 | 28≠56 |
| 10262 / 26102 | 8=8 | 4≠16 | 16=16 | 4≠8 |
| 20001026 / 20002610 | 8=8 | 8≠32 | 32≠24 | 4≠40 |
| 102 / 261 | 8≠6 | 8≠4 | 4≠3 | 8=8 |

Base-selective, not convention-free — and the two surviving bases are precisely
10 and 12, the two whose *squares* are divisor-rich (100 → τ 9; 144 → τ 15).
The pattern "resonates" in the two bases civilization actually chose; that is a
measured fact, and it is exactly as meaningful as the creases below say it is.

### Other configurations (measured, exhaustive)
The same digits, rearranged — every orientation family of the date:

| Scale | A | τ(A) | B | τ(B) | Equal? | Digit sums |
|---|---|---|---|---|---|---|
| 2-digit | 10 | 4 | 26 | 4 | **yes** | 1 vs 8 |
| 3-digit | 102 | 8 | 261 | 6 | no | 3 vs 9 |
| 4-digit | 1026 | 16 | 2610 | 24 | no | 9 vs 9 |
| 5-digit | 10262 | 8 | 26102 | 8 | **yes** | 11 vs 11 |
| 6-digit | 102600 | 96 | 261000 | 96 | **yes** | 9 vs 9 |
| 8-digit | 10262000 | 80 | 26102000 | 80 | **yes** | 11 vs 11 |
| 8-digit, year first | 20001026 | 8 | 20002610 | 8 | **yes** | 11 vs 11 |
| 14-digit full | 20001026102620 | 96 | 26102000102620 | 24 | no | 22 vs 22 |

Time and derived forms: HHMMSS 102620 → τ = 24 · total seconds 37,580 → τ = 12
· year 2000 → τ = 20 · day 300 → τ = 18 · YYYYMMDDHHMMSS → τ = 96 ·
reverse(full) 2620102610002 → τ = 16.

Exhaustive permutation counts (all distinct orderings of the date's digits):

* 8-digit set {2,0,0,0,1,0,2,6}: 420 distinct numbers — **τ = 8 is the mode
  (18.3%)**; τ = 80 appears in 3.6%. The 80-pair sits inside that 3.6% family.
* 5-digit set: 48 distinct — τ = 8 the mode (35.4%).
* 6-digit time set: 120 distinct — τ = 8 the mode (24.2%).

**Finding:** the τ-equality under MM/DD swap **oscillates with scale** — it holds
at 2, 5, 6, and 8 digits (including both year placements), and breaks at 3, 4,
and 14. The strongest agreement is at 5/6/8 digits, where the user's original
pair (10262/26102, τ = 8) and the full-date pair (10262000/26102000, τ = 80)
both land equal. The 3-digit break is the reason the creases below exist.

### The divisor lattice (all 80 divisors, both numbers)

Both numbers factor as **2⁴·5³·p·q** (exponent signature 4,3,1,1), so both
have **80 divisors: 16 odd, 64 even** — an identical parity split. The shared
divisor structure is the cleanest fact of the whole sweep:

* The **20 common divisors are exactly the divisors of the year 2000**
  {1, 2, 4, 5, 8, 10, 16, 20, 25, 40, 50, 80, 100, 125, 200, 250, 400, 500,
  1000, 2000}.
* Therefore **gcd(10262000, 26102000) = 2000** — the year itself is the
  greatest common divisor, and lcm = 133,929,362,000.
* **Self-reference:** the divisor count *80* is itself a common divisor
  (80 = 2⁴·5 divides both). The τ count lives inside the divisor set.
* **Cross-scale nesting:** the 5-digit pair divides the 8-digit pair
  (10262 = 10262000/1000, 26102 = 26102000/1000) — the retrace-chain members
  are divisors of the epoch.
* **The day does not divide the number:** 26, 1026, 2610 are divisors of
  neither (26 = 2·13, no factor 13). Only the year's lattice and the trailing
  `000` structure divide. The month 10 divides both (trailing zero).
* Odd divisors: 16 each; largest odd are 641,375 (A) and 1,631,375 (B) — both
  ≡ 1375 (mod 10⁴), i.e. 5³·p·q tail. σ/n = 2.77 vs 2.50 — both abundant.
* The odd-divisor digit-sum multisets coincide on 14 of 16 values.

**Reading:** the τ = 80 equality is not two unrelated facts — both numbers were
forced into the *same exponent shape* by the trailing `000`, and the overlap of
their divisor sets is precisely the year that produced those zeros. The pattern
is the year, made visible.

### Gap and difference analysis (the prime hunt)

Differences of odd divisors (and of even divisors) are always even, so a prime
gap can only be **2**:

* **The only odd-odd prime gap in either set is 2 — and it is a genuine
  twin-prime pair:** in A's odd divisors, 5 and 7 are *consecutive*. B has none
  (B has no divisor 7). This is the sharpest single "a prime comes up" result.
* Even sets each have three gap-2 twins: A has (2,4), (8,10), (14,16); B has
  (2,4), (8,10), (248,250). The bottom two — (2,4) and (8,10) — are **shared**,
  because they come from the common year-lattice divisors.
* **Each number's own large prime surfaces by doubling:** 733 = |733 − 1466|
  and 421 = |421 − 842|. Every divisor p pairs with its even double 2p, and
  |2p − p| = p is prime — a prime difference generated by the number's own
  signature factor.
* **Shared prime difference:** 7 = |1 − 8| appears identically in *both* sets
  (1 is an odd divisor of both, 8 an even divisor of both).
* **The chain re-emerges as gaps:** 10,262 is a gap between consecutive even
  divisors of A; 261,020 = 26,102×10 is a gap in B. The 733-multiples and
  421-multiples each form a full ladder of gaps inside their own set.
* Honest note: cross-parity differences yield 65 (A) and 59 (B) distinct
  primes starting 3, 5, 7, 11, 13, 17, 19, 23, 31, 43 — small primes are
  unavoidable in a dense divisor lattice. Only the specific ones above (the
  5/7 twin, the p↔2p doubling, the shared |1−8|=7) are diagnostic.

---

## Ch. 2  The measured instinct: why divisor-rich notation won

Cultures did not choose bases by convenience alone; they chose bases that
*factor easily*. Divisor count was the design criterion:

| System | Base | τ (divisors) | Why it won |
|---|---|---|---|
| Sumer/Babylon sexagesimal | 60 | **12** | 12 divisors: halves, thirds, quarters, fifths, sixths |
| The time system it bequeathed us | 360° · 1440 min · 86400 s | 24 · 36 · 96 | everything divides it |
| Dozenal (time, dozens) | 12 | 6 | thirds and quarters |
| Maya vigesimal | 20 | 6 | finger/toe counting, 4×20 = 80 |

The epoch's numbers are *divisor-rich by construction* — the year-2000 trailing
zeros guarantee τ ≥ 16, and the specific day/month push it to 80 in both
orientations. The instinct that made the Sumerians pick 60 is the same instinct
that makes this date *feel* significant: **many divisors = many names for the
same thing.** The corpus measures it; it does not worship it.

---

## Ch. 3  The same pattern across means (old civilizations)

The pattern is not in the numerals — it is in the *recording means*. Every major
civilization produced a notation system with the same invariant content and a
different encoding:

* **Sumer/Babylon** — cuneiform tablets, sexagesimal place value. The scribe
  (*dub-sar*) was the state's memory.
* **Egypt** — **Thoth**, scribe-god, keeper of measurement and writing; **Seshat**,
  "the scribe" who records reigns and lays out architecture. The **seked** is a
  written slope ratio (run/rise in palms) — a *measurement written down*.
* **Maya** — vigesimal, the tzolkin 260 (13×20, τ = **12**), the long count;
  scribes painted the codices. **80 = 4 × 20** sits inside the base itself.
* **Inka** — the **quipu**: records made of *knotted cords*. A ledger whose
  medium is thread. The *khipukamayuq* ("knot-keeper") was a weaver's scribe:
  the account IS the weave.
* **China** — the I Ching: 8 trigrams / 64 hexagrams (2³ / 2⁶). Binary before
  binary, written on bamboo slips. Hexagram **11** is Tài — *Prosperity*,
  "the small depart, the great arrive."
* **Vedic India** — the **Śulba-sūtras**: altar geometry done with ropes and
  pegs. The word *sūtra* literally means **thread**. The rule is a thread; the
  measurement is done by another means (no ruler, only cord).
* **Greece** — the **Moirai**: Clotho *spins* the thread, Lachesis *measures*
  its length, Atropos *cuts* it. Spin / measure / cut is flow / record / crease.
* **Norse** — the **Norns**, Urðr / Verðandi / Skuld (past / present / future),
  weave the threads of fate — a past-future *retrace chain*.

### Prime pairings, culturally
The two numbers' primes sort into a sharp, checkable rule (measured above):

* A's pair {7, 733}: **7 = 2³ − 1** (Mersenne, ≡ 3 mod 4) and
  **733 = 2² + 27²** (≡ 1 mod 4, a sum of two squares, root sum 2+27 = **29**).
* B's pair {31, 421}: **31 = 2⁵ − 1** (Mersenne, ≡ 3 mod 4) and
  **421 = 14² + 15²** (≡ 1 mod 4, **consecutive** squares, root sum 14+15 = **29**).

Each number carries exactly **one Mersenne prime and one two-square prime**, and
the two-square primes' square-roots sum to the *same* prime (29). Cultural
echoes of this specific structure:

* **Mersenne primes 7 and 31** are binary repunits (111₂, 11111₂) — the
  counting of a full hand or a full month (31 days) — and they are the corpus's
  own subject (the 2ⁿ − k sieve doctrine, the C7 bridge).
* **Two-square primes (Fermat)**: 421 = 14² + 15² is the hypotenuse of a
  *near-square* right triangle (14, 15, √421) — the ancients' diagonal
  approximation. The Babylonians kept side-and-diagonal tables in sexagesimal;
  the near-1:1 diagonal is the integer shadow of √2.
* **Doubling** (the |2p − p| = p difference): Egyptian arithmetic was
  multiplication by *duplatio* (doubling) and mediation (halving). The prime
  difference generated by each number's own factor is the shadow of that
  algorithm.
* **Twin primes (5, 7)** — the only odd-odd prime gap — echoes the twin motif
  in every myth system (Gemini, the Maya Hero Twins, twin birth as boundary
  doubling).

"Other means" is the point: the same content — divisor-rich structure, small
digit sums, foldable chains — survives re-encoding from cuneiform to knots to
hexagrams to sexagesimal seconds. That survival is exactly what the corpus's
creases (T59, T61) predict should survive: **distributional and invariant
content, not convention.**

---

## Ch. 4  The Weaver's Scribe (archetype → engine)

Two roles, one process:

* **The Weaver** lays the thread — in the engine, this is **flow**:
  `hamiltonian_flow`, the local repulsion that moves every entity.
* **The Scribe** writes it down — in the engine, this is the **record**:
  `record_classification` → `classification_history` (the "Book / holographic
  registry", THE_BOOK Ch. 2 observations), and `record_self_event` → `self_chain`
  (the closed-timelike thread that feeds past outputs back into future inputs).

The old myths map onto the machinery 1:1, as *illustrations*, not evidence:

| Myth | Role | Engine primitive |
|---|---|---|
| Clotho spins | the weave / motion | flow, expansion phase |
| Lachesis measures | the record, the length | τ (divisor count), entropy, `_compute_recurrence_time` |
| Atropos cuts | the fold / the crease | `_quarantine_to_boundary`, the boundary reset |
| Norns past/present/future | the retrace chain | SPRING_BIBLE Ch. 14: 943,901,200,001 → 10,262 |
| quipu knot-keeper | threaded record | `self_chain` (past outputs → future inputs) |
| sūtra = thread | the rule-as-thread | the number line; **0d is the knot** |

The Weaver's Scribe is therefore not a new machine — it is a name for the
mechanism the corpus already measures: **flow + record + fold**, the thread laid
down, written down, and folded back. The 0d datum (2000-10-26 10:26:20.00) is
where this particular thread was tied: both orientations 80-divisor, both
digit-sum 11, its own clock-time τ = 12 — the base's own divisor count.

---

## Ch. 5  The ML reading (what this means for the toy)

The toy is the hyperbolic novelty engine: `HamiltonianFlow` + the `Engine` on
the Poincaré disk. The date's divisor lattice is its finite, number-theoretic
shadow, and the sweep above reads as a checklist for how to believe (or not
believe) any pattern the toy reports:

1. **Representation artifacts vs. invariants.** The τ = 80 "signal" decomposes
   into three layers: the trailing `000` is a *biased feature* (20.4% of valid
   2000 dates share it; **0% in 2007**); the digit sum 11 is *permutation-
   trivial noise* (T57 — any rearrangement carries it); only the τ structure,
   gcd = 2000, and the base-12 survival are *convention-stable*. ML rule: when
   the engine flags a pattern, apply the same three tests — re-encode (change
   the representation), condition out the confounder, then measure the joint
   coincidence. This is the creases doctrine as model evaluation.
2. **Common divisors = shared latent factors.** gcd = 2000 and the 20 common
   divisors are exactly what a multi-view method (CCA, contrastive learning)
   extracts from two encodings of the same object: the invariant content they
   share. The MM/DD and DD/MM views share a "disentangled factor" — the year —
   and the common-divisor count (20) is their shared-subspace dimension. The
   toy's holographic compression (1,536 → 2, PUM §10.1(iii)) is the same
   operation at manifold scale: find the structure that survives both views.
3. **τ is a convention-stable numeric feature; digit sum is not.** Divisor
   count is permutation-sensitive in general yet stable here at several scales;
   digit sum is permutation-trivial and carries zero information across
   rearrangements. Feature-engineering rule: prefer features that survive a
   re-encoding test. And report surprise with the confounder conditioned out —
   the honest scale here is 0.48% → 20.4% → 4.64% → 17.3%, not "1 in 200".
4. **Gap spectra = spectral / effective-rank diagnostics.** The sorted
   even-divisor gaps open as 2,4,2,4,2,4 (A) vs 2,4,2,6,4,20,10 (B): the
   alternating opening is where the *shared* lattice (twice the year divisors)
   dominates, and the first break is where the unique factor begins. That is a
   number-theoretic scree plot — the same object as the toy's spectrum
   (E₀ = 5.84 → E₁ = 6.42) and the "knee" in PCA. Gap-2 twins (2,4), (8,10) are
   spectral-gap analogues: stable structure, shared across both sets.
5. **Actionable.** The queued T65 four-pack — prediction (iii), holographic
   compression / mutual information between 1,536-dim and 2D — is this exact
   shared-latent idea at engine scale. The base-invariance test (survives
   bases 10 and 12) is a cheap convention-robustness check to fold into the
   regression suite: if a "discovered" structure dies when the input is
   re-encoded, it was never a structure.

### Ch. 5.1  Physics and logarithmic probes (measured)

Cross-checking the three numbers, the retrace chain, and the toy's own
30-eigenvalue spectrum (`data/spectral_data.json`). Honest positives first:

* **E₁ = ¼ + ln²(12) to 0.04%.** The toy's second eigenvalue is
  E₁ = 6.42195; its spectral radius r = √(E₁−¼) = 2.48434, and ln(12) =
  2.48491 — relative match 4×10⁻⁴. 12 is the corpus's own signature dozenal
  (τ(12) = 6, Sumer/sexagesimal motif). The ground state E₀ = 5.84 does NOT
  match ln(10) (5% off) — the match is specific to E₁ and to 12.
* **The golden fold (two independent hits).** The upper retrace rung is a
  φ² hinge: 1,914,467/730,421 = 2.62105 vs φ² = 2.61803 (0.12%). And T58's
  measured closing radius was r_close = apex·0.6138 ≈ apex/φ (0.7%). The fold
  is golden-ratio-geometric in both the closing radius and the chain rung.
* **C7 bridge applied to the date's own Mersenne primes.** 7 = 2³−1 gives
  ℓ = 3·ln2, λ = ¼+ℓ² = 4.574 — below the measured spectral floor E₀ = 5.84
  (predicts a sub-floor mode); 31 = 2⁵−1 gives λ = 12.261, within 0.20 of
  eig[5] = 12.060. The two Mersenne primes straddle the low spectrum.
* **Level-spacing statistics (first time computed).** The 30 eigenvalues give
  ⟨r⟩ = 0.460 (intermediate: Poisson 0.386, GOE 0.536), gap CV 0.69. Small-n,
  so the spectrum cannot yet decide the T19 "chaos is consistent" claim —
  a genuine open measurement, not a settled one.

Arithmetic functions (never tabulated before):
φ(A) = 3,513,600, φ(B) = 10,080,000, φ(C) = 1,852,680; σ(A)/A = 2.767,
σ(B)/B = 2.502 (both highly abundant), σ(C)/C = 1.032 (barely abundant — the
fold is the least-abundant member of the family).

Weak/near-miss (report-and-forget, the creases):
B/A = 2.5436 ≈ √(2π) (1.5%) ≈ 5/2 (1.7%); ln(B/A) = 0.9336 rad = 53.49° ≈
3π/10 = 54° (1%); chain lower rungs 730,421/1,914,467 = 0.3815 and
10,262/26,102 = 0.3931 both hover near A/B = 0.3931 (within 3%). All at
coincidence scale — the same magnitude as the trailing-000 and base-8
artifacts already falsified.

**Conjectures (falsifiable):**
* **C1 (E₁-dozenal):** the toy's low spectral radii r_k track ln of
  convention-scale integers; 12 is the first and cleanest. Test: add modes
  (n > 30) and look for r_k ≈ ln(k) for k ∈ {10, 26, 2000}.
* **C2 (golden fold):** further retrace folds lock on φ (or φ²) rungs — the
  fold is golden-geometric, extending T58's 0.6138 ≈ 1/φ. Test: derive the
  next fold above the giant; predict ratio ∈ {φ, φ²}.
* **C3 (Mersenne-λ spectrum):** a mode exists near λ = 4.574 (from the prime
  7), below the current floor; and the λ(31) = 12.26 falls inside the gap
  [12.06, 12.85]. Test: recompute the spectral problem with more modes /
  higher resolution.
* **C4 (intermediate statistics):** ⟨r⟩ = 0.46 ± finite-n is neither Poisson
  nor GOE; the "chaos is consistent" capstone (T19) needs more modes to be
  measured, not asserted.

### Ch. 5.2  Special numbers (measured)

* **The 11-motif doubles.** Digit sum 11 was the first carrier; now a second,
  independent one: **5,131 ≡ 13,051 ≡ 11 (mod 80)**, where 80 = τ. The two odd
  cores are congruent to 11 modulo their own divisor count. Because of this,
  both largest odd divisors end in **1375 = 5³·11** (the shared 5³ block × the
  motif). A structure that survives two unrelated encodings (digit sum, mod-τ
  residue) is the kind the ML reading §5 marks as *candidate-invariant*.
* **The golden ratio is already the corpus's own fold** (SPRING_BIBLE Ch. 6):
  length_growth/length_fold = φ = 1.618034 measured exactly; T58 closes at
  r = apex·0.6138 ≈ apex/φ. The retrace rung 1,914,467/730,421 = 2.62105 ≈ φ²
  (0.12%) is the chain joining that same geometry. The *why* of 0.6138 stays
  open (AUDIT §1.2) — now with two data points (0.6138, 2.62105) instead of one.
* **137 appears twice, at coincidence scale.** Both 1375 tails carry "137",
  and the corpus's own PAPER §6.3 has C₀(α=5.0) = 137.574398 vs 1/α ≈ 137.036
  (0.4%). Reported and set aside: fine-structure numerology is exactly the
  class of near-miss this book has learned to stop chasing.
* **Taxicab 1729: honest negative.** None of A/B/C is divisible by 1729, but
  1729 = 12³+1 = 1³+12³ echoes the E₁↔ln(12) spectral match — worth one line,
  nothing more.
* **Special-number inventory (all verified):** Mersenne primes 7, 31 (2³−1,
  2⁵−1 — the C7-bridge subjects); 4k+1 two-square primes 733, 421, 61,757, 197
  with root-sums converging on the prime 29; τ = 80 (self-referential count);
  gcd = 2000 = the year; odd-part gcd = 125 = 5³; the doubled 11; 1375 = 5³·11.

---

## Ch. 6  Creases (never forget these)

1. **The pattern is scale-dependent.** τ-equality under MM/DD swap oscillates
   with scale: holds at 2, 5, 6, and 8 digits; breaks at 3, 4, and 14
   (e.g. 102: τ=8 vs 261: τ=6; 1026: τ=16 vs 2610: τ=24). A pattern that
   survives only at selected truncations is a property of the *representation*,
   not of the number line.
2. **Trailing zeros inflate divisor counts.** τ=80 is ~20% likely for *any*
   year-2000 date; both-orientation τ=80 is ~4.6% (1 in 22). Mild, not
   miraculous.
3. **Conventions break** (T59, T61): re-encode benignly and the surface
   coincidence dies; only invariant content (divisor counts, digit sums) — which
   are arithmetic, not mystical — survives. *Measured refinement:* the τ-agreement
   of this date survives base 10 and base 12 only, and dies in bases 8 and 16 —
   base-selective, which is the definition of convention-dependence. The τ = 80
   phenomenon dies entirely in any year without trailing zeros.
4. **Cultural parallels are mappings, not evidence.** Thoth, the quipu, the
   Moirai, and the Norns are offered as illustrations of a *shared measured
   instinct* (choose divisor-rich notation; record by thread). They are not
   signs this date was chosen by anyone.
5. **Digit-coincidences are not arithmetic** (T57): the "80 both ways" and the
   "11" sums are computed facts; the *resonance* is a human response to them,
   which is exactly what this book exists to hold at arm's length.

---

## Cross-references
* `data/epoch_0d.json` — the verified datum (with null analysis).
* `docs/SPRING_BIBLE.md` BOOK V Ch. 13–15 — the date's 5-digit treatment, the
  retrace chain, the creases (T57, T59, T61, T62).
* `docs/THE_BOOK.md` Ch. 2 (observations), Ch. 8 (time and convergence) — the
  scribe's bank and the clock.
* `Universals/engine.py` — `record_classification`, `record_self_event`,
  `generate_thought`, `_dream`, `_quarantine_to_boundary`.
