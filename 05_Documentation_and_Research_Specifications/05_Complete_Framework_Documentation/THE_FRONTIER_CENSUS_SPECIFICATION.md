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

Taken alone this is `List.filter_congr` and carries little. Its *content* is
supplied by a companion theorem that exhibits a **live competitor** — a predicate
that matches the crease on the window yet provably diverges beyond it, so the
finite evidence is, on that window, indistinguishable from evidence for the
*negation* of the row:

> **`wieferich_competitor_window_agree`.** The Wieferich crease `wieferichCrease`
> and the constant-`false` predicate `neverCrease` ("no Wieferich prime exists")
> agree at every `n ∈ [1, 1092]`; their censuses coincide
> (`wieferich_competitor_census_eq`). They are *globally distinct*
> (`wieferich_competitor_differs`, at 1093) and not equivalent
> (`wieferich_competitor_not_global`).

So no window can ever distinguish a row from a competitor that matches it on the
window — including a competitor that *denies the row entirely*. A census is
therefore never evidence for a universal; it is only ever evidence *about the
window*. Every honest row in the Ledger is already written this way ("holds to the
bound and stays OPEN"); this theorem pair is that discipline as mathematics, with
the separation made concrete rather than merely asserted.

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

### 3.1.1 The falsification pass: which rows are creases and which are not

The crease hypothesis was attacked directly — an attempt to build a `Crease` for
each *non*-compiled open row, with the honest result recorded:

| Row | candidate `lin` (first-order) | outcome |
|---|---|---|
| **Mersenne** (G29) | `p` prime | **survives** — undershoot 19, a real crease |
| **Goldbach** (G6) | `n` even | **degenerate** — on `[4,100]` the crease census *equals* the `lin` census (49 = 49); `lin` carries no content |
| **twin primes** (G12/G26) | none on single `n` | **structural fail** — the census is over *pairs*; no first-order `n`-predicate refines it |
| **Collatz** (G12) | `n ≥ 1` | **degenerate** — every tested `n` reaches 1, so `lin` is trivial and the crease set is the whole window |

**Scope narrowing (a result, not a failure).** The crease hypothesis is
therefore *not* a claim about arithmetic open rows in general. It is a theory of
**single-integer resolvent rows whose universal layer is a genuine first-order
theorem** — Wieferich, Wilson, Giuga, Lehmer, Mersenne. The rows it does *not*
cover (Goldbach, twin primes, Collatz) fail for a principled reason: they have no
content-bearing first-order layer (they are density or dynamical statements, not
resolvent statements). The theory's domain is thus itself a falsifiable
prediction, and the falsification pass pinned it.

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
  `census_window_agree`, `wieferich_competitor_window_agree` /
  `_differs` / `_not_global`, `CensusRun`, `Crease`, `wieferichCreaseInstance`,
  `giugaCreaseInstance`, `mersenneCreaseInstance`, `registry`,
  `undershoot_instances`, `frontierCensusFacts`).
- Primitives: `PunoCalculus/Factorization.lean` (`primeFacGo`, `totientFac`).
- Existing barrier: `PunoCalculus/Wieferich.lean`
  (`first_order_not_iff_isWieferich`), `PunoCalculus/Wilson.lean`
  (`first_order_tests_are_universal`).
- Ledger row: **G38**.
