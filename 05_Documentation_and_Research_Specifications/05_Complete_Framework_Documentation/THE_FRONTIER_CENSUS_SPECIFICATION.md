# The Frontier Census: a synthesised theory of the arithmetic open-status rows

**Status: mixed.** The *structure* of this note is interpretive — a synthesis of
six already-machine-checked finite certificates (Gap Ledger G30, G31, G32, G34,
G36, G37). Its *skeleton* is machine-checked in
`01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/FrontierCensus.lean`.
Every universal claim that any of those rows leaves open **stays open here**:
this theory decides nothing new about Giuga, Lehmer, Erdős–Moser, Wieferich, or
Wilson primes. What it adds is a name for what they have in common, and a
prediction-generating reading of where the difficulty lives.

## 1. The observation

Seven rows of the Gap Ledger are usually filed as unrelated open problems. Read
together they have one shape:

> a **decidable predicate** `P` on the natural numbers; a **window** `[1, N]`;
> a **census** `{ n ≤ N : P n }` the kernel returns in full; and an **open
> universal** — a claim about *all* `n` that no window settles.

Nothing about `P` is undecidable. The kernel decides the census. What it cannot
decide is the universal. The rows:

| Row | Predicate `P` | Census on the window | Window | Open universal |
|---|---|---|---|---|
| G30 Giuga | `p ∣ (n/p − 1)` for all prime `p ∣ n` | `30, 858, 1722` (≤ 10⁴) | 10⁴ | no number is Giuga **and** Carmichael |
| G31 Lehmer | `φ(n) ∣ (n − 1)`, `n` composite | `[]` (≤ 10⁴) | 10⁴ | the Lehmer set is empty |
| G31 2-Lehmer | `φ(n) ∣ (n − 1)²` | `561, 1105, 1729, 2465, 6601, 8481` | 10⁴ | (relaxation; no universal) |
| G32 Wieferich | `2^(p−1) ≡ 1 (mod p²)` | `1093, 3511` | 4000 | finitely or infinitely many? |
| G34 Erdős–Moser | `Σ_{j<m} j^k = m^k` | `[]` (4 ≤ m ≤ 80, k ≤ 12) | pinned | only `(3,1)` |
| G36 Wilson | `(p−1)! ≡ −1 (mod p²)` | `5, 13, 563` | pinned | finitely or infinitely many? |
| G29 Mersenne | `p` prime and `2^p − 1` prime | `2,3,5,7,13,17,19,31,61,89,107,127` (p ≤ 128) | 128 | finitely or infinitely many Mersenne primes? |

The census is finite evidence. The universal is the wall.

(The falsification pass of §3.1.1 shows this list is *exactly* the domain: rows
without a content-bearing first-order layer — Goldbach, twin primes, Collatz —
are not creases and are deliberately excluded.)

## 2. The formal core: a window cannot separate

The machine-checked core of the theory is one theorem, stated twice — once
abstractly, once on a live competitor:

> **`census_window_agree`.** If two decidable predicates `P`, `Q` agree at every
> `n` in `[1, N]`, their censuses on `[1, N]` are identical.

Taken alone this is `List.filter_congr` and carries little. Its *content* is the
**existence** half, which is now a theorem about *every* row:

> **`windowFlip_is_live_competitor`.** For **every** decidable predicate `P` and
> **every** window bound `N`, the window-complement flip `windowFlip N P` (equal
> to `P` on `[1, N]`, the Boolean complement of `P` above it) agrees with `P` on
> the window and is *not equivalent* to `P` globally — they differ at `N + 1`.
> Equivalently (`no_window_separates_all_rows`): for every row there exists a
> competitor with the same census but a different predicate.

So no window can ever distinguish a row from a competitor that matches it there —
including a competitor that *denies the row entirely* beyond the window. A census
is therefore never evidence for a universal; it is only ever evidence *about the
window*. The Wieferich case is the concrete instance of the same fact:

> **`wieferich_competitor_window_agree`.** The Wieferich crease `wieferichCrease`
> and the constant-`false` predicate `neverCrease` ("no Wieferich prime exists")
> agree at every `n ∈ [1, 1092]`; their censuses coincide
> (`wieferich_competitor_census_eq`). They are *globally distinct*
> (`wieferich_competitor_differs`, at 1093) and not equivalent
> (`wieferich_competitor_not_global`).

Every honest row in the Ledger is already written this way ("holds to the bound
and stays OPEN"); these theorems are that discipline as mathematics, with the
separation an outright theorem rather than an instance.

## 3. The crease

The rows differ not in their shape but in *where the difficulty lives*. Wieferich
fixes the prototype, and the corpus already proves it (G37):

- the **first-order** Fermat test `p ∣ 2^(p−1) − 1` is satisfied by *every* odd
  prime (`Wieferich.fermat_dvd`) — it discriminates nothing;
- the **second-order** test `p² ∣ 2^(p−1) − 1` isolates 1093 and 3511;
- and the no-go `first_order_not_iff_isWieferich` proves *no* first-order
  certificate can be sound-and-complete.

The Frontier Census hypothesis names the general object:

> **The crease hypothesis.** Every arithmetic open-status row is a crease: a
> first-order predicate `lin` that is true on a large, structurally simple set,
> and the census predicate `crease` that refines it. The window exhibits the
> refinement; it cannot show whether the refinement is total or void beyond it.

The new Lean module records this as the structure `Crease`, carrying `lin`,
`crease`, their two census runs, and two obligations:

- **`refine_sub`** — every crease value is a first-order value (the crease
  refines the leading description);
- **`undershoot`** — the first-order census is *strictly* longer (the leading
  test under-shooots, admitting values the crease excludes).

Both are machine-checked, per instance, by `decide`. `undershoot_instances`
bundles the Wieferich and Giuga cases. This is the per-instance shadow of G37:
G37 proves the barrier for one row universally; `Crease` records it for each row
as a computable fact.

### 3.1 The compiled creases

- **Wieferich** (`wieferichCreaseInstance`). `lin` = odd prime; `crease` =
  Wieferich. Window `[1, 4000]`: the first-order census is the 549 odd primes
  (1093 and 3511 included; 3989 is the largest), the crease census is
  `[1093, 3511]`. The undershoot is 549 − 2 = 547.
- **Giuga** (`giugaCreaseInstance`). `lin` = squarefree with ≥ 2 prime factors;
  `crease` = full Giuga condition. Window `[1, 10⁴]`: the first-order census has
  4853 members, the crease census is `[30, 858, 1722]`, so the undershoot is
  4850 — a strict sub-census of the squarefree composites.
- **Mersenne** (`mersenneCrease`, added by the falsification pass below). `lin` =
  prime exponent; `crease` = Mersenne prime exponent. On exponent window `[1, 128]`:
  the first-order census is the 31 primes ≤ 128, the crease census is
  `[2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127]`, undershoot 31 − 12 = 19. This
  is a *genuine* third crease, of the same shape as Wieferich: a first-order layer
  (`p` prime) with real arithmetic content, refined by a second-order test.

### 3.1.1 The falsification pass, corrected

The crease hypothesis was attacked directly — an attempt to build a `Crease` for
each *non*-compiled open row. The **first draft of this pass reached a wrong
conclusion**, and the module now records the correction:

| Row | candidate `lin` (first-order) | corrected outcome |
|---|---|---|
| **Mersenne** (G29) | `p` prime | **is a crease** — undershoot 19 |
| **twin primes** (G12/G26) | `p` prime (the *lower* twin) | **is a crease** — undershoot 31 (`twin_primes_are_a_crease`); the first draft's "structural fail" was wrong |
| **Goldbach** (G6) | `n` even | **is a crease** — undershoot ≥ 1 (`lin` census 50, crease census 49 on `[4,100]`) |
| **Collatz** (G12) | `n ≥ 1` | **degenerate** — every tested `n` reaches 1, so the `lin` census equals the crease census and the strict `undershoot` fails |

**The corrected lesson (`crease_is_weak`).** The `Crease` structure does **not**
exclude Goldbach or twin primes: the earlier "not a crease" claim was an error.
What the structure forbids is only the *diagonal* `lin = crease`
(`no_diagonal_crease`: a strict inequality cannot hold reflexively). So "is a
crease" is not a discriminating predicate at all — it is satisfied by any row with
a non-full census.

**The scope claim is not formalizable (`scope_not_formal`).** The previous arc
"narrowed the theory to single-integer resolvent rows". That narrowing cannot be a
theorem: **any** predicate with a non-full census admits the trivial first-order
layer `lin := n ≥ 1` (`trivial_lin_crease_witness`). Genuine open rows with no
arithmetic first-order content — e.g. Brocard's problem (`n! + 1 = m²`) — are
therefore structural creases too. "Content-bearing `lin`" is a *naturalness
judgement*, not a Lean-checkable property, so the scope-narrowing is **demoted**
from a claim to a documented reading. The theory's real content is quantitative —
the *size* of the undershoot relative to the window and its relation to each row's
open universal — not the bare existence of a `Crease`.

### 3.1.2 Undershoot monotonicity: structural, and where it fails

The prediction that undershoot is monotone under window extension splits cleanly:

- **Structural half (a theorem).** If `crease n ⟹ lin n` as *predicates* on all of
  `ℕ`, then `census_sub` gives the crease census as a sub-collection of the `lin`
  census on *every* window, and `undershoot_nonneg_of_sub` gives
  `|crease| ≤ |lin|`. Containment transfers to all window bounds.
- **Conditional half.** The monotonicity is monotone *only* while that predicate
  containment survives beyond the window. `containment_can_fail` exhibits a pair
  that contains inside `[1, 3]` but not at `4`. That failing point **is** the row's
  missing object: a value where `crease` fires but `lin` does not is exactly the
  bridge-failure that keeps the row open.

So prediction 4 is not free: its falsifier and the row's open content are the same
object. Level (structural) is proved; level (conditional) is honest.

The Lehmer, 2-Lehmer and Erdős–Moser rows are recorded as `CensusRun`s (their
first-order companions are the same predicate minus the decisive condition; the
finite evidence is what the theory needs).

### 3.2 Why the census is computed with reducing primitives

The kernel cannot bulk-decide `Nat.Prime` (trial division does not reduce over a
window), and `2^(n−1) % n²` by `Nat.pow` is too costly per value. The module
therefore primality-tests through the reducing factoriser `primeFacGo` (proved in
`Factorization.lean`) and modular-exponentiates through a tail-recursive
`powMod`. With those, the *full* Wieferich census over `[1, 4000]` reduces in
about 90s and returns `[1093, 3511]`. This is a practical note for anyone adding
a row: **the census predicate must reduce.**

### 3.3 The separation theorem: the census is a complete window invariant

`census_window_agree` says *equal on the window ⟹ equal census*. The dual is
equally sharp and is now proved (`census_separates_iff_differs`):

> **`census_separates_iff_differs`.** Two predicates have *different censuses* on
> `[1, N]` **iff** they disagree at some point of `[1, N]`.

So the census is a **complete invariant of the window** — it detects a competitor
exactly when the competitor is refuted *inside* the window, and (by
`windowFlip_is_live_competitor`) it is blind to any competitor that agrees inside,
however it behaves outside. This closes the core: the census sees the window and
*nothing but* the window, in both directions. It is the precise sense in which the
finite evidence is a snapshot, not a proof.

### 3.4 The crease fraction: a quantitative barrier with a single increase locus

A cross-row quantity surfaces from the data — the **crease fraction** `cre/lin`
(crease-census size over first-order-census size), or its inverse the **rarity
ratio** `lin/cre`. It is a step function, and its movement is now a theorem
(`crease_fraction_falls_on_lin_step`, `crease_fraction_rises_on_crease_step`):

> extending the window by a value that is `lin` but not `crease` **never raises**
> `cre/lin` (and strictly lowers it once a crease is present); extending by a value
> that *is* a crease **raises** it.

So the **only increase points of `cre/lin` are the creases themselves**: across a
window, the crease count equals the number of rise-steps, and the rarity ratio
`lin/cre` climbs monotonically between creases. This is the quantitative form of
the barrier — the open universal of a row is exactly the question of whether
`lin/cre` is eventually infinite (finitely many creases) or not. The three compiled
creases instantiate it (`compiled_crease_fractions`):

| row | lin | cre | cre/lin | rarity `lin/cre` |
|---|---|---|---|---|
| Wieferich (`[1,4000]`) | 549 | 2 | 0.0036 | 274 |
| Giuga (`[1,10⁴]`) | 4853 | 3 | 0.0006 | 1617 |
| Mersenne (`p ≤ 128`) | 31 | 12 | 0.387 | 2.6 |

The rarity ratios span three orders of magnitude — Wieferich creases are
*quadratically* rarer than Mersenne creases — yet the *shape* (a step function
rising only at creases) is identical across rows. That identical shape is the
theory's quantitative invariant; the differing rarity is what makes each row's
universal a different problem.

## 4. What this theory predicts

The synthesis is only useful if it generates falsifiable claims. It does:

1. **Windows never settle.** For *any* new arithmetic open-status row, the finite
   census is consistent with both the universal and its negation. Prediction:
   every historically-failed induction from census to universal (Pólya's `F(n) ≤
   0`, Mertens' `|M(n)| < √n`) is a `census_window_agree` instance. Falsifier: a
   row where the census value *itself* forces the universal by a theorem about
   the window.
2. **The crease is first-order-invisible.** Prediction: every proposed
   certificate for a new row will have a first-order layer that is provably
   universal (accepts every candidate), so all discriminating information lives
   at second order. Falsifier: a sound-and-complete first-order certificate for
   any row — refuting G37's method-barrier.
3. **Crease location predicts rarity.** Prediction: the density of the crease
   census is bounded by a second-order condition, so crease values are
   *quadratically* sparse relative to `lin` values. Wieferich: `lin` density
   `~1/log x`, crease density `~log log x / log x`. Falsifier: a row whose crease
   census grows at the same order as its first-order census.
4. **Undershoot is monotone, *conditionally*.** Prediction: extending the window
   of a compiled `Crease` never *decreases* the undershoot, **provided the crease
   predicate keeps refining `lin` beyond the window** (i.e. `crease n ⟹ lin n` for
   all `n`, not just inside). Under that hypothesis the first-order census grows at
   least as fast, so the difference is monotone. Verified on the compiled creases
   (Wieferich: 547 → 1004 → 1859 over `[1,4000]`/`[1,8000]`/`[1,16000]`; Giuga:
   4850 → 9894 → 20103 over `[1,10⁴]`/`[1,2·10⁴]`/`[1,4·10⁴]`). **Falsifier:** a
   value `n` beyond the window where `crease n` holds but `lin n` does not — which
   would drop the undershoot *and*, at the same stroke, exhibit exactly the
   bridge-failure that makes the row open. The monotonicity is thus not a free
   theorem: its falsifier is the row's own missing object.

   *(Note the numbers above are computed by the independent Python certificate,
   not by the kernel — a second window is too costly to `decide`. They are a
   cross-check of the claim, not a machine-checked theorem.)*

## 5. The barrier, stated honestly

The theory is a *barrier theory*, in the same family as the "shared wall" note:

> the arithmetic open rows share the skeleton **completed window + one critical
> quantity that becomes exactly marginal at the crease**, and the missing object
> is always the same: a second-order invariant that is not merely consistent with
> the census but *equivalent to it beyond the window*.

This is a **bridge-barrier**, not a method-barrier in general: the census and the
universal are two independently-defined worlds (the finite and the global) that
must be shown to coincide, and the difficulty is the bridge. G37 is the special
case where the barrier *is* a method-barrier (proved). The synthesis does not
upgrade the other rows to that status; it only observes they occupy the same
position.

## 6. What stays open

Everything the Ledger already marked open:

- Giuga's conjecture (G30), Lehmer's problem (G31), Erdős–Moser uniqueness (G34),
  Wieferich finiteness (G32), Wilson finiteness (G36), Mersenne infinitude (G29),
  odd-perfect existence (G27).
- The crease hypothesis itself is **reviewed, not proved**: that the structure is
  *universal across rows* is a synthesis on finite instances, and the module says
  so in its header and in `frontierCensusFacts` (the final entry carries the word
  `OPEN`).

## 7. Pointers

- Lean: `PunoCalculus/FrontierCensus.lean` (`census`, `WindowAgree`,
  `census_window_agree`, `windowFlip`, `windowFlip_is_live_competitor`,
  `no_window_separates_all_rows`, `wieferich_competitor_window_agree` /
  `_differs` / `_not_global`, `CensusRun`, `Crease`, `wieferichCreaseInstance`,
  `giugaCreaseInstance`, `mersenneCreaseInstance`, `no_diagonal_crease`,
  `twin_primes_are_a_crease`, `undershoot_nonneg_of_sub`, `containment_can_fail`,
  `trivial_lin_crease_witness`, `registry`, `undershoot_instances`,
  `frontierCensusFacts`).
- Primitives: `PunoCalculus/Factorization.lean` (`primeFacGo`, `totientFac`).
- Existing barrier: `PunoCalculus/Wieferich.lean`
  (`first_order_not_iff_isWieferich`), `PunoCalculus/Wilson.lean`
  (`first_order_tests_are_universal`).
- Ledger row: **G38**.
