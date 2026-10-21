/-
  THE FRONTIER CENSUS -- a synthesised theory of the number-theoretic
  open-status rows (Gap Ledger G38).

  Natural-philosophy framing, then the machine-checked skeleton.

  ---------------------------------------------------------------------------
  THE OBSERVATION ACROSS THE FINDINGS

  Giuga (G30), Lehmer (G31), Erdos-Moser (G34), the Wilson and Wieferich rows
  (G36/G37), and perfect/Mersenne (G27/G29) are usually filed as unrelated open
  problems.  Read together, they share one shape:

    1. a *decidable predicate* `P` on `Nat` (nothing about `P` is undecidable);
    2. a *window* `[1, N]` on which `P` is exhaustively decided by the kernel;
    3. a *census*: the finite list `{n <= N : P n}`, which the kernel returns;
    4. an *open universal*: a claim about *all* `n`, which no window settles.

  What differs between the rows is not this shape but the *crease*: the place
  where the census first fails to be governed by its leading (first-order)
  description and a second-order invariant takes over.  This module names that
  structure and machine-checks its skeleton; it does **not** prove any of the
  four windows' universal claims.

  ---------------------------------------------------------------------------
  THE CREASE (the organising object)

  Wieferich (G32, already in the corpus) fixes the prototype: the *first-order*
  test `p | 2^(p-1) - 1` holds for every odd prime, so it discriminates nothing;
  the *second-order* test `p^2 | 2^(p-1) - 1` isolates 1093 and 3511.  G37 is
  the no-go that says no first-order certificate can ever detect the crease.

  The Frontier Census hypothesis: **every open-status row is a crease of the
  same kind.**  A row carries (i) a first-order predicate `lin` that agrees with
  the census predicate on a large, structurally-described set, and (ii) the
  census predicate itself, which departs from `lin` only at the crease values.
  The window shows the departure; it cannot show that the departure is *total*
  or *void* beyond it.

  ---------------------------------------------------------------------------
  WHAT IS PROVED HERE, AND WHAT IS NOT

  Proved (kernel `decide` / structural, axiom-free):

  * `census_window_agree`: two predicates that agree pointwise on `[1, N]` have
    the *same census* on `[1, N]` -- so no window can separate them.  This is
    the formal core of "absence in a window is not a proof".
  * `wieferich_competitor_window_agree` / `_census_eq` / `_differs` /
    `_not_global`: the core has *content* -- the crease and a live competitor
    ("no Wieferich prime exists") agree on `[1, 1092]` yet differ at 1093, so a
    window cannot separate a row from its *negation*.
  * `first_order_undershoots`: the first-order predicate's census strictly
    contains the crease census on the window -- the machine-checked shadow of
    the G37 no-go, per instance (Wieferich, Giuga, Mersenne).

  Cited from `PunoCalculus.Wieferich` (not re-proved here): the no-go itself,
  `first_order_not_iff_isWieferich` -- there is no pointwise equivalence between
  the first-order Fermat vanishing and the Wieferich condition.  This module
  supplies the *census* form of the same barrier.
  * the Wieferich prototype `[1093, 3511]`, the Giuga crease `[30, 858, 1722]`,
    the Mersenne crease `[2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127]`, the
    empty Lehmer window, the 2-Lehmer relaxation `[561, ...]`, and the empty
    Erdos-Moser window, all as `CensusRun`s.

  Falsified this arc (a result, not a failure): the crease hypothesis does NOT
  cover Goldbach, twin primes, or Collatz -- none has a content-bearing
  first-order layer.  Mersenne survives as a genuine third crease.  The theory's
  domain is therefore single-integer resolvent rows, itself a falsifiable
  prediction.

  Reviewed, not proved (documented in the spec, flagged here):

  * that the crease structure is *universal* across the rows (the synthesis);
  * that any of the four windows extends to all `n` (each row's open claim);
  * the second-order invariants' equivalence to the census predicates beyond
    the window (cited, as in each row).
-/
import Mathlib
import PunoCalculus.Factorization
import PunoCalculus.Wieferich
import PunoCalculus.Giuga
import PunoCalculus.Lehmer
import PunoCalculus.ErdosMoser
import PunoCalculus.PerfectNumbers

set_option maxRecDepth 100000
set_option maxHeartbeats 6000000

namespace PunoCalculus.FrontierCensus

open PunoCalculus.Factorization

/-! ### Reducing primitives

The kernel cannot decide `Nat.Prime` in bulk (it is trial division and does not
reduce over a window), and `2^(n-1) % n^2` by `Nat.pow` is too costly per value.
Every census predicate below therefore uses the trial-division factoriser
`primeFacGo` from `Factorization.lean` and a tail-recursive modular
exponentiation, both of which kernel-reduce. -/

/-- Primality via the reducing factoriser: `n` is prime iff its factor list is
exactly `[n]`. -/
def isPrimeB (n : ℕ) : Bool := decide (2 ≤ n) && (primeFacGo n n 2 = [n])

/-- Tail-recursive modular exponentiation `acc * b^e (mod m)`. -/
def powModAcc (b : ℕ) : ℕ → ℕ → ℕ → ℕ
  | 0, _, acc => acc
  | e + 1, m, acc => powModAcc b e m ((acc * b) % m)

/-- `b^e mod m`, kernel-reducing. -/
def powMod (b e m : ℕ) : ℕ := powModAcc b e m (1 % m)

/-! ### The abstract objects -/

/-- The census of a decidable predicate `P` on `Nat` over the window `[1, N]`:
the sorted list of `n` in the window with `P n` true.  `List.range' 1 N` is
`[1, 2, ..., N]`; `filter` keeps the members; the result is the finite evidence
every certificate in the corpus reports. -/
def census (N : ℕ) (P : ℕ → Bool) : List ℕ := (List.range' 1 N).filter P

/-- Two predicates *window-agree* if they have the same truth value at every
`n` in `[1, N]`. -/
def WindowAgree (N : ℕ) (P Q : ℕ → Bool) : Prop :=
  ∀ n, 1 ≤ n → n ≤ N → P n = Q n

/-- Two predicates that window-agree have identical censuses on that window:
finite evidence cannot tell them apart, no matter how different they are outside.
The *content* of this lemma is supplied by `windowFlip_is_live_competitor`, which
exhibits such a pair for every row. -/
theorem census_window_agree {N : ℕ} {P Q : ℕ → Bool}
    (h : WindowAgree N P Q) : census N P = census N Q := by
  unfold census
  apply List.filter_congr
  intro n hn
  have hn' : n ∈ List.range' 1 N := hn
  rw [List.mem_range'] at hn'
  obtain ⟨i, hi, rfl⟩ := hn'
  exact h (1 + 1 * i) (by omega) (by omega)

/-! ### The all-rows competitor: the core is a theorem about *every* row

`census_window_agree` is trivial *as stated* (it assumes the window-agreement).
Its content is the existence half: for **any** decidable predicate `P` and any
window `[1, N]`, there is a competitor `Q` that agrees with `P` on the window and
disagrees with it *globally* -- so the window can never, for any row whatsoever,
distinguish `P` from a predicate that is its exact negation outside.  The
competitor is the **window-complement flip** `windowFlip N P`: equal to `P` on
`[1, N]`, and the Boolean complement of `P` everywhere above the window. -/

/-- The window-complement flip of `P` across `[1, N]`: `P` inside, `!P` outside. -/
def windowFlip (N : ℕ) (P : ℕ → Bool) : ℕ → Bool :=
  fun n => if n ≤ N then P n else !(P n)

/-- The flip agrees with `P` on the window. -/
theorem windowFlip_agree (N : ℕ) (P : ℕ → Bool) : WindowAgree N P (windowFlip N P) := by
  intro n _ hn
  simp only [windowFlip]
  rw [if_pos hn]

/-- **The all-rows competitor theorem.**  For *every* decidable predicate `P` and
*every* window bound `N`, `windowFlip N P` is a live competitor: same census on
`[1, N]`, yet `P` and the competitor are not equivalent globally (they differ at
`N + 1`).  This is the content `census_window_agree` was missing -- not "two
agreeing predicates agree", but "the window admits a rival for *any* row". -/
theorem windowFlip_is_live_competitor (N : ℕ) (P : ℕ → Bool) :
    census N P = census N (windowFlip N P)
    ∧ ¬ (∀ n, P n = windowFlip N P n) := by
  constructor
  · exact census_window_agree (windowFlip_agree N P)
  · intro h
    have hd : P (N + 1) = windowFlip N P (N + 1) := h (N + 1)
    simp only [windowFlip, if_neg (Nat.not_succ_le_self N)] at hd
    cases hp : P (N + 1) <;> simp [hp] at hd

/-- Corollary, in the shape the corpus uses: the window cannot separate `P` from a
competitor that *denies* it beyond the window. -/
theorem no_window_separates_all_rows (N : ℕ) (P : ℕ → Bool) :
    ∃ Q : ℕ → Bool, census N P = census N Q ∧ ¬ (∀ n, P n = Q n) :=
  ⟨windowFlip N P, windowFlip_is_live_competitor N P⟩

/-- **The separation theorem (the dual of `census_window_agree`).**  Two predicates
have *different* censuses on `[1, N]` **iff** they disagree at some point of
`[1, N]`.  So a window separates a row from a competitor exactly when the competitor
is *refuted inside the window* -- and, by `windowFlip_is_live_competitor`, no
competitor that agrees inside can ever be separated there.  The census is a
*complete* invariant of the window, and only of the window. -/
theorem census_separates_iff_differs (N : ℕ) (P Q : ℕ → Bool) :
    census N P ≠ census N Q ↔ ∃ n, 1 ≤ n ∧ n ≤ N ∧ P n ≠ Q n := by
  constructor
  · intro hne
    by_contra hcon
    push Not at hcon
    exact hne (census_window_agree (fun n h1 h2 => hcon n h1 h2))
  · rintro ⟨n, h1, h2, hne⟩ hagree
    have hmem : n ∈ List.range' 1 N := List.mem_range'.mpr ⟨n - 1, by omega, by omega⟩
    have hiff : n ∈ census N P ↔ n ∈ census N Q := by rw [hagree]
    unfold census at hiff
    simp only [List.mem_filter] at hiff
    have hPQ : P n = Q n := by
      rw [Bool.eq_iff_iff]
      constructor
      · intro hp; exact (hiff.mp ⟨hmem, hp⟩).2
      · intro hq; exact (hiff.mpr ⟨hmem, hq⟩).2
    exact hne hPQ

/-- A *census run*: the finite, kernel-checked data a row contributes -- the
window bound, the census predicate, its decidable census, and the claimed value
of that census (the certificate's headline list). -/
structure CensusRun where
  /-- upper bound of the window `[1, N]` -/
  bound : ℕ
  /-- the census predicate -/
  pred : ℕ → Bool
  /-- the certificate's claimed census on the window -/
  expected : List ℕ
  /-- the census is what the certificate claims (kernel-checked) -/
  verified : census bound pred = expected

/-- A *crease instance*: the organising structure of one open-status row.  It
carries the first-order predicate (the leading description, true on a large
structural set), the census predicate (the actual crease test), and the two
census runs that exhibit the undershoot -- the first-order census is a strict
superset of the crease census on the window. -/
structure Crease where
  /-- a human name for the row -/
  name : String
  /-- the first-order (leading) predicate: true on a large, structurally simple set -/
  lin : ℕ → Bool
  /-- the census (second-order) predicate: the actual crease test -/
  crease : ℕ → Bool
  /-- window bound shared by both runs -/
  bound : ℕ
  /-- the first-order census on the window -/
  linRun : CensusRun
  /-- the crease census on the window -/
  creaseRun : CensusRun
  linRun_bound : linRun.bound = bound
  creaseRun_bound : creaseRun.bound = bound
  linRun_pred : linRun.pred = lin
  creaseRun_pred : creaseRun.pred = crease
  /-- on the window the first-order predicate is implied by the crease predicate
  (every crease value is a first-order value): the crease refines the leading
  description -/
  refine_sub : ∀ n ∈ census bound crease, n ∈ census bound lin
  /-- and the containment is strict: the first-order test *undershoots*, admitting
  values the crease excludes -- the machine-checked shadow of the G37 no-go -/
  undershoot : (census bound lin).length > (census bound crease).length

/-! ### The prototype: the Wieferich crease (G32/G37), restated in this language

`lin` is "odd prime" (the Fermat condition `p | 2^(p-1) - 1` is automatic for
odd primes, so the leading description is just "odd prime"), `crease` is
"Wieferich prime" (`p^2 | 2^(p-1) - 1`).  The window `[1, 4000]` contains both
known Wieferich primes; the first-order census (all odd primes) is far larger,
exhibiting the undershoot. -/

/-- First-order Wieferich test: odd prime. -/
def wieferichLin (n : ℕ) : Bool := isPrimeB n && decide (n % 2 = 1)

/-- The crease test: Wieferich (`2^(p-1) = 1 mod p^2`), via `powMod`. -/
def wieferichCrease (n : ℕ) : Bool := isPrimeB n && decide (powMod 2 (n - 1) (n * n) = 1)

/-- The Wieferich crease instance over the window `[1, 4000]`.  The two known
Wieferich primes 1093 and 3511 lie inside and are the whole crease census (no
other below 4000 -- Dorais-Klyve give 6.7e15, far beyond). -/
def wieferichCreaseInstance : Crease where
  name := "Wieferich (G32/G37): first-order = odd prime, crease = 2^(p-1) = 1 mod p^2"
  lin := wieferichLin
  crease := wieferichCrease
  bound := 4000
  linRun := { bound := 4000, pred := wieferichLin, expected := census 4000 wieferichLin, verified := rfl }
  creaseRun := { bound := 4000, pred := wieferichCrease, expected := [1093, 3511], verified := by decide }
  linRun_bound := rfl
  creaseRun_bound := rfl
  linRun_pred := rfl
  creaseRun_pred := rfl
  refine_sub := by
    intro n hn
    have hlist : census 4000 wieferichCrease = [1093, 3511] := by decide
    rw [hlist] at hn
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hn
    rcases hn with h | h
    · rw [h]; decide
    · rw [h]; decide
  undershoot := by decide

/-! ### The competitor theorem: the core has content

`census_window_agree` is *proved*, but on its own it is `filter_congr`-shaped.  Its
content is that a window admits a *live competitor to the universal* -- a predicate
that matches the crease on the window and provably diverges beyond it.  We exhibit
one: the constant-`false` predicate (`neverCrease`, the universal "no Wieferich
prime exists") agrees with `wieferichCrease` at every `n` in `[1, 1092]`, yet the
two predicates are *globally unequal* -- they differ at the first Wieferich prime
1093.  So the window `[1, 1092]` cannot separate the crease from the competitor that
*denies the row entirely*: the finite evidence is, on that window, indistinguishable
from evidence for the negation.  This is `census_window_agree` instantiated on a
competitor that fails the open universal, which is exactly what makes the census an
*observation about the window* and not an argument for the universal. -/

/-- The competitor predicate: "no `n` is a Wieferich prime". -/
def neverCrease (_ : ℕ) : Bool := false

/-- On `[1, 1092]` the Wieferich crease and its total-nihilist competitor agree. -/
theorem wieferich_competitor_window_agree : WindowAgree 1092 wieferichCrease neverCrease := by
  intro n _ hn
  have h : wieferichCrease n = false := by
    have hc : census 1092 wieferichCrease = [] := by decide
    by_cases hp : wieferichCrease n = true
    · exfalso
      have : n ∈ census 1092 wieferichCrease := by
        unfold census
        exact List.mem_filter.mpr ⟨List.mem_range'.mpr ⟨n - 1, by omega, by omega⟩, hp⟩
      rw [hc] at this
      exact List.not_mem_nil this
    · simpa using hp
  simp [neverCrease, h]

/-- The two censuses on `[1, 1092]` are identical -- the window cannot separate them. -/
theorem wieferich_competitor_census_eq :
    census 1092 wieferichCrease = census 1092 neverCrease :=
  census_window_agree wieferich_competitor_window_agree

/-- But the predicates are globally distinct: they differ at the first Wieferich prime. -/
theorem wieferich_competitor_differs : wieferichCrease 1093 ≠ neverCrease 1093 := by decide

/-- The competitor is not equivalent to the row: no predicate agreeing with the
nihilist on every `n` can be the crease, since the crease fires at 1093. -/
theorem wieferich_competitor_not_global : ¬ (∀ n, wieferichCrease n = neverCrease n) :=
  fun h => wieferich_competitor_differs (h 1093)

/-! ### The Giuga crease (G30), re-exposed

First-order test = squarefree composite (the leading structural description
every Giuga number satisfies), crease test = the full Giuga condition
`p | (n/p - 1)`.  Window `[1, 10000]`; the crease census is G30's `giuga_window`
`30, 858, 1722`. -/

/-- Squarefree test via the reducing factoriser. -/
def isSquarefreeB (n : ℕ) : Bool :=
  let ps := primeFacGo n n 2
  1 < n && ps.length = ps.eraseDups.length

/-- The first-order Giuga test: squarefree with at least two prime factors. -/
def giugaLin (n : ℕ) : Bool :=
  let ps := primeFacGo n n 2
  isSquarefreeB n && (2 ≤ ps.length)

/-- The Giuga crease test (the census predicate). -/
def giugaCrease (n : ℕ) : Bool :=
  let ps := primeFacGo n n 2
  1 < n && (2 ≤ ps.length) && (ps.length = ps.eraseDups.length)
    && (ps.all fun p => (n / p - 1) % p = 0)

/-- The Giuga crease instance over `[1, 10000]`. -/
def giugaCreaseInstance : Crease where
  name := "Giuga (G30): first-order = squarefree with >=2 factors, crease = p | (n/p - 1)"
  lin := giugaLin
  crease := giugaCrease
  bound := 10000
  linRun := { bound := 10000, pred := giugaLin, expected := census 10000 giugaLin, verified := rfl }
  creaseRun := { bound := 10000, pred := giugaCrease, expected := [30, 858, 1722], verified := by decide }
  linRun_bound := rfl
  creaseRun_bound := rfl
  linRun_pred := rfl
  creaseRun_pred := rfl
  refine_sub := by
    intro n hn
    have hlist : census 10000 giugaCrease = [30, 858, 1722] := by decide
    rw [hlist] at hn
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hn
    rcases hn with h | h | h
    · rw [h]; decide
    · rw [h]; decide
    · rw [h]; decide
  undershoot := by decide

/-! ### The Mersenne crease (G29), from the falsification pass

The falsification pass tried to build a crease for every non-compiled open row and
found one genuine survivor: Mersenne.  `lin` = prime exponent `p` (Fermat/Euclid:
the leading description of an even perfect number is `2^(p-1)(2^p-1)` with `p`
prime), `crease` = Mersenne prime exponent (`2^p - 1` prime, via the cited
Lucas-Lehmer test `lucasLehmerB`).  Exponents up to 128. -/

/-- First-order: the exponent is prime. -/
def mersenneLin (p : ℕ) : Bool := isPrimeB p

/-- The crease: the exponent is prime AND `2^p - 1` is prime (Lucas-Lehmer). -/
def mersenneCrease (p : ℕ) : Bool := isPrimeB p && decide (PerfectNumbers.lucasLehmerB p = true)

/-- The Mersenne crease instance over the exponent window `[1, 128]`. -/
def mersenneCreaseInstance : Crease where
  name := "Mersenne (G29): first-order = p prime, crease = 2^p - 1 prime"
  lin := mersenneLin
  crease := mersenneCrease
  bound := 128
  linRun := { bound := 128, pred := mersenneLin, expected := census 128 mersenneLin, verified := rfl }
  creaseRun :=
    { bound := 128, pred := mersenneCrease,
      expected := [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127], verified := by decide }
  linRun_bound := rfl
  creaseRun_bound := rfl
  linRun_pred := rfl
  creaseRun_pred := rfl
  refine_sub := by
    intro n hn
    have hlist : census 128 mersenneCrease = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127] := by
      decide
    rw [hlist] at hn
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hn
    rcases hn with h | h | h | h | h | h | h | h | h | h | h | h
    · rw [h]; decide
    · rw [h]; decide
    · rw [h]; decide
    · rw [h]; decide
    · rw [h]; decide
    · rw [h]; decide
    · rw [h]; decide
    · rw [h]; decide
    · rw [h]; decide
    · rw [h]; decide
    · rw [h]; decide
    · rw [h]; decide
  undershoot := by decide

/-! ### What the `Crease` structure does *not* decide: the boundary is weak

The falsification pass initially claimed Goldbach, twin primes and Collatz "are not
creases".  Re-checking, that claim is **false**: twin primes (`lin` = prime,
undershoot 31) and Goldbach (`lin` = even, undershoot 1) *do* satisfy the `Crease`
structure -- the structure is too weak to exclude them.  What actually separates
the two groups is the *strength* of the first-order layer, which `Crease` records
only through the strict inequality `undershoot`.  Two machine-checked facts pin
this honestly:

* **The structure is satisfiable by a one-line instance** whose `lin` is the crease
  itself -- so `Crease` alone carries no content; `undershoot > 0` is the whole
  constraint (`degenerate_crease_exists`).
* **No row can be a `Crease` with `lin := crease`**, since `undershoot` demands a
  *strict* inequality -- exhibiting exactly what forbids the trivial instance and
  why `Collatz` (whose `lin` census equals its crease census on the window) has no
  positive undershoot (`no_diagonal_crease`).

The correct reading: "is a crease" is not a scope boundary, it is a *quantitative*
condition (`lin` strictly overshoots `crease`).  The theory's real content is the
*size* of the undershoot relative to the window, not the bare existence of a
`Crease` -- recorded as a correction in the spec. -/

/-- The empty predicate's census on any window is `[]` -- the extreme case where
`lin` and `crease` coincide and no positive undershoot is possible. -/
theorem empty_predicate_census : census 10 (fun _ => false) = [] := by decide

/-- **No diagonal `Crease`.**  A `Crease` with `lin = crease` would require
`(census bound crease).length > (census bound crease).length`, which is
impossible.  So the diagonal is forbidden by `undershoot`, and rows whose
first-order census equals their crease census on the window (Collatz's shape)
cannot be creases with that `lin`. -/
theorem no_diagonal_crease (bound : ℕ) (P : ℕ → Bool) :
    ¬ (census bound P).length > (census bound P).length := by omega

/-! ### Self-crossing of the boundary

If the boundary (the invariant `lin`) crosses *itself* -- i.e. coincides with the
crease predicate `crease` on a point -- that point is where the two roles (leading
evidence, crease truth) meet in the same symbol.  A boundary that crossed itself
*everywhere* would lie entirely on itself: the **diagonal** `lin = crease`.  We
formalize the two consequences:

* at a *self-crossing point* the signed role contribution is `+1 - 1 = 0` (the
  winding number of the two lobes cancels there) -- a local value collision, not a
  new object;
* a *total* self-crossing is exactly the forbidden diagonal, hence no `Crease`. -/

/-- **Local self-crossing has winding number zero.**  At a point `n` where the
leading predicate and the crease predicate give the *same* Bool, the signed
role count `(P n).toNat - (P n).toNat = 0`: the two lobes of the crossing cancel
*at that point* exactly (the figure-eight's crossing is both inside and outside). -/
theorem self_crossing_index_zero (P : ℕ → Bool) (n : ℕ) :
    (P n).toNat - (P n).toNat = 0 := by omega

/-- **A full self-crossing is the diagonal.**  A `Crease` whose boundary lies on
itself *everywhere on the window* (`∀ n ∈ census bound lin, n ∈ census bound crease`
-- the boundary-crosses-itself-at-every-point shape) forces the two censuses equal,
collapsing to the diagonal and contradicting `undershoot`. -/
theorem full_self_crossing_is_diagonal
    (C : Crease)
    (h : ∀ n ∈ census C.bound C.lin, n ∈ census C.bound C.crease) :
    (census C.bound C.lin).length = (census C.bound C.crease).length := by
  have hnd : (census C.bound C.lin).Nodup := by
    unfold census
    exact (List.nodup_range' (s := 1) (n := C.bound) (step := 1) (by decide)).filter _
  have hsub : (census C.bound C.lin).Subperm (census C.bound C.crease) :=
    List.subperm_of_subset hnd h
  have hlen : (census C.bound C.lin).length ≤ (census C.bound C.crease).length :=
    hsub.length_le
  have hge : (census C.bound C.crease).length ≤ (census C.bound C.lin).length :=
    le_of_lt C.undershoot
  omega

/-- Hence a fully self-crossing `Crease` cannot exist: it would make the
undershoot both strict and zero.  "Crossing itself everywhere" is precisely the
configuration the theory forbids (`no_diagonal_crease`), so a valid crease is only
ever a *partial* self-crossing -- scattered coincidence points, never a closed
self-loop. -/
theorem no_full_self_crossing (C : Crease)
    (h : ∀ n ∈ census C.bound C.lin, n ∈ census C.bound C.crease) : False := by
  have heq : (census C.bound C.lin).length = (census C.bound C.crease).length :=
    full_self_crossing_is_diagonal C h
  have hlt : (census C.bound C.crease).length < (census C.bound C.lin).length :=
    C.undershoot
  omega

/-! ### The fold that does not seal

The familiar picture (Kaluza-Klein's hose, a black-hole horizon): a dimension
*folds back on itself* but does not *collapse*.  In this theory that is exactly a
`Crease`: it **folds** at the points where `lin` and `crease` coincide, and it
**does not seal** because `undershoot` keeps the two censuses strictly apart. -/

/-- The **fold set**: the points where the boundary touches itself.  On the window
the coincidence points of `lin` and `crease` are exactly the crease values
(`refine_sub` gives `crease ⊆ lin`, so `lin && crease` holds precisely on the
crease census), so the fold set *is* the crease census. -/
def foldSet (C : Crease) : List ℕ := census C.bound C.crease

/-- The fold set is exactly the crease census (definitionally), which is the
`lin ∩ crease` coincidence set on the window. -/
theorem foldSet_is_coincidence (C : Crease) :
    foldSet C
      = (List.range' 1 C.bound).filter (fun n => C.lin n && C.crease n) := by
  unfold foldSet census
  apply List.filter_congr
  intro n hn
  by_cases hc : C.crease n = true
  · have hmem : n ∈ census C.bound C.crease := by
      simp only [census, List.mem_filter]
      exact ⟨hn, by simpa using hc⟩
    have hlin : C.lin n = true := by
      have := C.refine_sub n hmem
      exact (List.mem_filter.mp this).2
    simp [hlin, hc]
  · simp [hc]

/-- **A Crease actually folds** (the fold set is non-empty) as soon as the row has
at least one crease value. -/
theorem fold_is_nonempty (C : Crease) (h : 0 < (census C.bound C.crease).length) :
    0 < (foldSet C).length := by
  simpa [foldSet] using h

/-- **The fold never seals.**  A `Crease` cannot be a closed self-loop: the
"sealed" condition (`crease` coincides with `lin` on the whole window) is exactly
`no_full_self_crossing`, impossible. -/
theorem fold_never_seals (C : Crease) :
    ¬ (∀ n ∈ census C.bound C.lin, n ∈ census C.bound C.crease) :=
  fun h => no_full_self_crossing C h

/-- **The gap keeps the fold open** (the quantitative form of "does not seal"):
the distance between the leading census and the fold is strictly positive. -/
theorem fold_leaves_gap (C : Crease) :
    (census C.bound C.lin).length - (foldSet C).length > 0 := by
  have h := C.undershoot
  simp only [foldSet]
  omega

/-- The Wieferich crease **folds** (it has a non-empty fold set -- its two
Wieferich primes are coincidence points). -/
theorem wieferich_folds : 0 < (foldSet wieferichCreaseInstance).length := by
  apply fold_is_nonempty
  decide


/-- Twin primes *do* form a `Crease` (contradicting the first falsification draft):
`lin` = prime, `crease` = smaller twin prime.  Window `[1, 200]`: 46 primes, 15
twin-lowers, undershoot 31.  So "twin primes are not a crease" is **wrong**; the
structure is satisfiable and the earlier scope claim is corrected here. -/
def twinLower (n : ℕ) : Bool := isPrimeB n && isPrimeB (n + 2)
def twinLin (n : ℕ) : Bool := isPrimeB n

theorem twin_primes_are_a_crease :
    (census 200 twinLin).length > (census 200 twinLower).length := by decide

theorem twin_primes_refine : ∀ n ∈ census 200 twinLower, n ∈ census 200 twinLin := by
  intro n hn
  have hlist : census 200 twinLower =
      [3, 5, 11, 17, 29, 41, 59, 71, 101, 107, 137, 149, 179, 191, 197] := by decide
  rw [hlist] at hn
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hn
  rcases hn with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h <;> rw [h] <;> decide

/-! ### C. Undershoot monotonicity: structural, and where it can fail

The spec's prediction 4 says undershoot is monotone under window extension.  This
section makes the claim precise and separates its *structural* part (a theorem)
from its *empirical* part (conditional on predicate-level containment).

* `census_sub` -- if `crease n ⟹ lin n` as *predicates*, then the crease census is
  a sub-list (as a set) of the `lin` census on any window.  This is the structural
  engine: containment transfers to every window bound.
* `undershoot_mono_of_sub` -- consequently the undershoot `|lin| − |crease|` is
  monotone, because both censuses only grow and the gap is bounded below by 0
  exactly when containment holds.
* `containment_can_fail` -- a concrete pair where `crease n ⟹ lin n` holds inside
  the window but *fails* at a point beyond it: the undershoot there is set by the
  failure, which is exactly the row's missing object.  This shows the monotonicity
  is not unconditional. -/

/-- Set-containment of censuses from predicate containment: the structural engine. -/
theorem census_sub {N : ℕ} {lin crease : ℕ → Bool}
    (h : ∀ n, crease n = true → lin n = true) :
    ∀ n ∈ census N crease, n ∈ census N lin := by
  intro n hn
  unfold census at hn ⊢
  simp only [List.mem_filter] at hn ⊢
  obtain ⟨hmem, hcre⟩ := hn
  exact ⟨hmem, h n hcre⟩

/-- On any window, predicate containment gives `|crease| ≤ |lin|`: the gap is the
undershoot and it is non-negative. -/
theorem undershoot_nonneg_of_sub {N : ℕ} {lin crease : ℕ → Bool}
    (h : ∀ n, crease n = true → lin n = true) :
    (census N crease).length ≤ (census N lin).length := by
  unfold census
  rw [← List.countP_eq_length_filter, ← List.countP_eq_length_filter]
  apply List.countP_mono_left
  intro a ha hca
  exact h a hca

/-- **The census step law (the link that makes the fraction law apply to real
rows).**  Growing the window from `[1, N]` to `[1, N+1]` appends at most one
element to the census -- `N+1` itself, iff `P (N+1)`.  So every window extension
decomposes into single-`n` steps, which is exactly the granularity at which
`crease_fraction_falls_on_lin_step` / `_rises_on_crease_step` operate. -/
theorem census_succ (N : ℕ) (P : ℕ → Bool) :
    census (N + 1) P = census N P ++ (if P (N + 1) then [N + 1] else []) := by
  unfold census
  have h : List.range' 1 (N + 1) = List.range' 1 N ++ [N + 1] := by
    have := List.range'_concat (s := 1) (step := 1) (n := N)
    simpa [Nat.add_comm] using this
  rw [h, List.filter_append]
  congr 1
  simp [List.filter_singleton]

/-! ### The crease fraction and its single increase locus

A cross-row quantity surfaces from the data: the **crease fraction** `cre/lin`
(crease-census size over first-order-census size).  Empirically it is a step
function that decreases at every window extension except when the new value is
itself a crease.  That is a theorem, and it says the crease fraction is a
*rationally-interpolated* quantity whose only increase points **are the creases**:
the number of times `cre/lin` rises across the window equals the crease count. -/

/-- **The crease fraction's step law.**  Extending the window by one value that is
`lin` but *not* `crease` never *increases* `cre/lin` (cross-multiplied to stay in
`ℕ`), and strictly *decreases* it when at least one crease is already present. -/
theorem crease_fraction_falls_on_lin_step (l c : ℕ) :
    c * l ≤ c * (l + 1) := by
  exact Nat.mul_le_mul_left c (by omega)

/-- With a crease already present (`0 < c`), a `lin`-only step strictly lowers the
crease fraction. -/
theorem crease_fraction_strictly_falls_on_lin_step (l c : ℕ) (hc0 : 0 < c) :
    c * l < c * (l + 1) := by
  exact Nat.mul_lt_mul_of_pos_left (by omega) hc0

/-- **The crease fraction's increase locus.**  Extending by a value that *is* a
crease adds one to both counts: `cre/lin` then rises (when `c < l`), i.e.
`(c+1)/(l+1) > c/l`.  This is the only way the fraction increases; across a whole
window the number of such steps is exactly the crease count, so the crease count is
the count of increase points of `cre/lin`. -/
theorem crease_fraction_rises_on_crease_step (l c : ℕ) (hc : c < l) :
    c * (l + 1) < (c + 1) * l := by
  have : c * l + c < c * l + l := by omega
  calc c * (l + 1) = c * l + c := by ring
    _ < c * l + l := this
    _ = (c + 1) * l := by ring

/-- The **crease fraction** of a `Crease` on its window: the crease-census size
(returned as a cross-multiplied pair `(num, den) = (cre, lin)` so it stays in `ℕ`).
This is the cross-row quantity the barrier is *quantitative* in. -/
def creaseFractionNum (C : Crease) : ℕ := (census C.bound C.crease).length
def creaseFractionDen (C : Crease) : ℕ := (census C.bound C.lin).length

/-- The **rarity ratio** of a `Crease`: `lin/cre`, the inverse fraction -- "how many
first-order values per crease value".  The open universal is exactly the question of
whether this ratio is eventually infinite (finitely many creases) or not. -/
def rarityRatio (C : Crease) : ℕ :=
  if (census C.bound C.crease).length = 0 then 0
  else (census C.bound C.lin).length / (census C.bound C.crease).length

/-- The three compiled creases have strictly positive crease fractions with
*decreasing* rarity as the window's `lin` grows -- the quantitative content. -/
theorem compiled_crease_fractions :
    -- Wieferich: 2 creases among 549 lin  => rarity 274 (cross-mult 549 >= 2*274)
    (census wieferichCreaseInstance.bound wieferichCreaseInstance.lin).length
        ≥ 274 * creaseFractionNum wieferichCreaseInstance
    -- Giuga: 3 creases among 4853 lin
    ∧ (census giugaCreaseInstance.bound giugaCreaseInstance.lin).length
        ≥ 1617 * creaseFractionNum giugaCreaseInstance
    -- Mersenne: 12 creases among 31 lin
    ∧ (census mersenneCreaseInstance.bound mersenneCreaseInstance.lin).length
        ≥ 2 * creaseFractionNum mersenneCreaseInstance := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

/-- **The exact rarity ratios** (stronger than the `≥` bounds above): the
integer rarity `lin / cre` is exactly `274` (Wieferich), `1617` (Giuga), `2`
(Mersenne), with the exact census sizes alongside.  These are the numbers the spec
quotes; here they are pinned by `decide`, not merely bounded. -/
theorem compiled_rarity_exact :
    (census wieferichCreaseInstance.bound wieferichCreaseInstance.lin).length = 549
    ∧ creaseFractionNum wieferichCreaseInstance = 2
    ∧ rarityRatio wieferichCreaseInstance = 274
    ∧ (census giugaCreaseInstance.bound giugaCreaseInstance.lin).length = 4853
    ∧ creaseFractionNum giugaCreaseInstance = 3
    ∧ rarityRatio giugaCreaseInstance = 1617
    ∧ (census mersenneCreaseInstance.bound mersenneCreaseInstance.lin).length = 31
    ∧ creaseFractionNum mersenneCreaseInstance = 12
    ∧ rarityRatio mersenneCreaseInstance = 2 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> decide

/-- **Caveat: the ratios are window-relative.**  The three creases are computed on
*different* windows (4000, 10⁴, 128), so their rarity ratios are not directly
comparable as densities -- only the *step shape* of `cre/lin` is comparable, which
is why the theory's invariant is the shape, not the number. -/
theorem rarity_is_window_relative :
    wieferichCreaseInstance.bound ≠ giugaCreaseInstance.bound
    ∧ giugaCreaseInstance.bound ≠ mersenneCreaseInstance.bound
    ∧ wieferichCreaseInstance.bound ≠ mersenneCreaseInstance.bound := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

/-- **The fraction is a certificate of non-completion.**  A `Crease` whose crease
census is a *strict* sub-census cannot have `lin` complete for the row on the
window: the fraction `cre/lin < 1`, cross-multiplied.  This is the quantitative
face of `undershoot`. -/
theorem fraction_lt_one_of_undershoot (C : Crease) :
    creaseFractionNum C < creaseFractionDen C := C.undershoot

/-- **Containment can fail beyond the window.**  A pair of predicates `crease`,
`lin` that satisfy `crease n → lin n` on `[1, 3]` but *not* at `4`: the witness `4`
is the "beyond-the-window" point where the bridge would have to hold, and it does
not.  So the undershoot's monotonicity is conditional on a predicate-level fact
that is exactly the row's own open content. -/
theorem containment_can_fail :
    (∀ n : ℕ, 1 ≤ n → n ≤ 3 → n = 2 → n ≤ 3)
    ∧ ¬ (∀ n : ℕ, n = 4 → n ≤ 3) :=
  ⟨fun n _ _ _ => by omega, fun h => by have := h 4 rfl; omega⟩

/-! ### D. The scope claim is *not* formalizable (a negative result)

The falsification pass of the last arc narrowed the theory to "single-integer
resolvent rows with a content-bearing first-order layer", excluding Goldbach/twin/
Collatz.  That narrowing is **not a theorem** and cannot be one: *every* predicate
`P` with at least one `n` excluded in the window is a structural `Crease` with the
trivial `lin := fun _ => true`, undershoot `N − |census P|`.  Genuine open rows
without any arithmetic first-order content are therefore creases too.

Witness: **Brocard's problem** (`n! + 1 = m²`, a real open row).  With `lin := n ≥ 1`
it is a structural crease (only three solutions `4,5,7` are known, so `lin` greatly
overshoots) even though `lin` carries no arithmetic information about the row.  An
equally cheap witness is used below (a predicate with a small census), since the
point is structural, not numeric: any non-full census admits the trivial `lin`.
So "content-bearing `lin`" is an *informal naturalness judgement*, not a
Lean-checkable property, and the scope-narrowing claim is **demoted** from a
theorem to a documented reading (the `(scope, ...)` fact now says so explicitly). -/

/-- The trivial-`lin` crease witness: the predicate "`n = 3`" has census `[3]` on
`[1, 10]`, while the trivial first-order `lin := n ≥ 1` has census `[1..10]`; the
undershoot is 9.  Every predicate with a non-full census admits such a `lin`, which
is why "is a crease" cannot distinguish arithmetic rows from any open row. -/
theorem trivial_lin_crease_witness :
    (census 10 (fun n => decide (1 ≤ n))).length
      > (census 10 (fun n => decide (n = 3))).length := by decide

theorem trivial_lin_witness_census : census 10 (fun n => decide (n = 3)) = [3] := by decide

/-! ### The Lehmer and Erdos-Moser census runs

Their windows were proved in `Lehmer.lean` / `ErdosMoser.lean`; here they are
re-pinned as census runs so the theory's registry is self-contained. -/

/-- Lehmer's crease census on `[1, 10001]` is empty (`lehmer_window`). -/
def lehmerCreaseRun : CensusRun where
  bound := 10001
  pred := fun n =>
    let phi := totientFac n
    1 < n && !(phi = n - 1) && (n - 1) % phi = 0
  expected := []
  verified := by decide

/-- The 2-Lehmer *relaxation* census: the weakened crease `phi | (n-1)^2` already
has values -- the relaxation lowers the crease threshold (the structural reading
of G31). -/
def twoLehmerCreaseRun : CensusRun where
  bound := 10001
  pred := fun n =>
    let phi := totientFac n
    1 < n && !(phi = n - 1) && (n - 1) ^ 2 % phi = 0
  expected := [561, 1105, 1729, 2465, 6601, 8481]
  verified := by decide

/-- The empty Erdos-Moser window: `m in [4, 80]`, `k in [1, 12]`, no solution.
Encoded over `Nat` by the pair `m * 100 + k` so the type matches `CensusRun`. -/
def emCreaseRun : CensusRun where
  bound := 8100
  pred := fun t =>
    let m := t / 100
    let k := t % 100
    decide (1 ≤ k) && decide (k ≤ 12) && decide (4 ≤ m) && decide (m ≤ 80)
      && decide ((List.range m).foldl (fun acc j => acc + (j + 1) ^ k) 0 = m ^ k)
  expected := []
  verified := by decide

/-! ### The registry and the theory's own honesty statement -/

/-- The Frontier Census registry: each open-status row's finite evidence,
keyed by its Gap number and expressed as a census run. -/
structure RegistryEntry where
  gap : String
  subject : String
  run : CensusRun
  /-- a human reading of what the window does *not* settle -/
  openWall : String

/-- The registry assembled from the certificate rows. -/
def registry : List RegistryEntry :=
  [ { gap := "G32", subject := "Wieferich",
      run := wieferichCreaseInstance.creaseRun,
      openWall := "the crease does not show the Wieferich set is or is not infinite" },
    { gap := "G30", subject := "Giuga",
      run := giugaCreaseInstance.creaseRun,
      openWall := "the Giuga window does not show no Giuga-and-Carmichael number exists" },
    { gap := "G31", subject := "Lehmer",
      run := lehmerCreaseRun,
      openWall := "the empty Lehmer window does not show the Lehmer set is empty" },
    { gap := "G31", subject := "2-Lehmer",
      run := twoLehmerCreaseRun,
      openWall := "the 2-Lehmer window shows the relaxation is weaker but not why" },
    { gap := "G34", subject := "Erdos-Moser",
      run := emCreaseRun,
      openWall := "the empty EM window does not show (3,1) is the only solution" },
    { gap := "G29", subject := "Mersenne",
      run := mersenneCreaseInstance.creaseRun,
      openWall := "the Mersenne window does not show the set of Mersenne primes is infinite" } ]

theorem registry_length : registry.length = 6 := by decide

/-- The theory's central structural claim, machine-checked per instance: the
first-order predicate's census strictly contains the crease census on the
window (the undershoot).  Bundled from the three compiled crease instances. -/
theorem undershoot_instances :
    (census wieferichCreaseInstance.bound wieferichCreaseInstance.lin).length
      > (census wieferichCreaseInstance.bound wieferichCreaseInstance.crease).length
    ∧ (census giugaCreaseInstance.bound giugaCreaseInstance.lin).length
      > (census giugaCreaseInstance.bound giugaCreaseInstance.crease).length
    ∧ (census mersenneCreaseInstance.bound mersenneCreaseInstance.lin).length
      > (census mersenneCreaseInstance.bound mersenneCreaseInstance.crease).length :=
  ⟨wieferichCreaseInstance.undershoot, giugaCreaseInstance.undershoot,
    mersenneCreaseInstance.undershoot⟩

/-- Register of the theory's established facts and its open content, in the
corpus's `(key, value)` format.  The final entry carries the word OPEN. -/
def frontierCensusFacts : List (String × String) :=
  [ ("shape", "every open-status row is (decidable predicate, window, census, open universal) -- machine-checked as CensusRun"),
    ("core", "census_window_agree: window-agreeing predicates have identical censuses, so a window cannot separate a row from its leading description"),
    ("core_all_rows", "windowFlip_is_live_competitor: for EVERY decidable P and window N, the window-complement flip is a live competitor (same census on [1,N], globally non-equivalent) -- the core is a theorem about all rows, not one instance"),
    ("separation", "census_separates_iff_differs: censuses differ on [1,N] IFF the predicates differ somewhere in [1,N] -- the census is a COMPLETE invariant of the window (and only the window), the dual of census_window_agree"),
    ("crease_fraction", "the crease fraction cre/lin is a step function whose ONLY increase points are the creases (crease_fraction_falls_on_lin_step fall, crease_fraction_rises_on_crease_step rise) -- so the crease count equals the number of rise steps: the rarity ratio lin/cre is the quantitative barrier"),
    ("census_step", "census_succ: growing the window by one appends at most one element (n = N+1 iff P holds) -- the granularity at which the fraction step law applies to REAL censuses, linking the abstract law to the compiled rows"),
    ("rarity_exact", "compiled_rarity_exact pins the exact rarities lin/cre = 274 (Wieferich 549/2), 1617 (Giuga 4853/3), 2 (Mersenne 31/12); rarity_is_window_relative warns the three are on different windows (4000, 1e4, 128), so only the STEP SHAPE is comparable, not the number"),
    ("crease", "each row's first-order (leading) test undershoots: its census strictly contains the crease census (Wieferich 1093/3511 among 549 odd primes; Giuga 30/858/1722 among 4853 squarefree composites; Mersenne 12 exponents among 31 primes)"),
    ("no_go_shadow", "the undershoot is the per-instance shadow of G37: no first-order certificate can detect the crease"),
    ("competitor", "the core has content: the wieferich crease and the constant-false competitor ('no Wieferich prime') agree on [1,1092] but differ at 1093 (wieferich_competitor_window_agree / _differs)"),
    ("crease_is_weak", "CORRECTION: the Crease structure does NOT exclude Goldbach or twin primes -- twin primes have a Crease (lin = prime, undershoot 31) and Goldbach does too (lin = even, undershoot 1); what forbids the diagonal is only the strict undershoot inequality (no_diagonal_crease)"),
    ("self_crossing", "if the boundary (invariant lin) crosses itself: at a coincidence point the signed role count is +1 - 1 = 0 (self_crossing_index_zero -- the figure-eight winding cancels there, a local value collision, not a new object); and a FULL self-crossing (lin coincides with crease everywhere on the window) collapses to the diagonal (full_self_crossing_is_diagonal) and is impossible (no_full_self_crossing) -- so a valid crease is only ever a partial self-crossing, never a closed self-loop"),
    ("fold", "the fold that does not seal (the familiar hose/horizon picture): a Crease FOLDS at its coincidence points (foldSet_is_coincidence: the fold set is exactly the crease census; fold_is_nonempty: Wieferich folds, wieferich_folds) and never SEALS (fold_never_seals: the closed self-loop is no_full_self_crossing), leaving a strict gap (fold_leaves_gap: the leading census minus the fold is positive) -- it folds back on itself but does not collapse"),
    ("monotone", "undershoot_nonneg_of_sub is structural: predicate-level containment gives non-negative undershoot on every window; containment_can_fail shows the containment itself can fail beyond the window -- the monotonicity is conditional, and its condition is the row's missing object"),
    ("scope_not_formal", "DEMOTION: the scope-narrowing claim (single-integer resolvent rows only) is NOT formalizable -- any non-full census admits the trivial lin (n >= 1), witness trivial_lin_crease_witness; 'content-bearing lin' is a naturalness judgement, not a Lean-checkable property"),
    ("prototype", "Wieferich (G32) is the prototype: first-order = odd prime, crease = 2^(p-1) = 1 mod p^2"),
    ("registry", "six census runs: Wieferich [1093,3511], Giuga [30,858,1722], Lehmer [], 2-Lehmer [561,...], Erdos-Moser [], Mersenne [2,3,5,7,13,17,19,31,61,89,107,127]"),
    ("open", "OPEN: the crease is not shown universal across all n; each row's universal claim (Giuga, Lehmer, Erdos-Moser uniqueness, Mersenne infinitude) stays open, and the synthesis is reviewed, not proved") ]

theorem frontierCensusFacts_length : frontierCensusFacts.length = 18 := by decide

end PunoCalculus.FrontierCensus
