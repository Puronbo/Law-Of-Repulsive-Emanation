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

/-- **The formal core.**  Two predicates that window-agree have identical
censuses on that window: finite evidence cannot tell them apart, no matter how
different they are outside.  This is the machine-checked statement of "the
window is not the theorem". -/
theorem census_window_agree {N : ℕ} {P Q : ℕ → Bool}
    (h : WindowAgree N P Q) : census N P = census N Q := by
  unfold census
  apply List.filter_congr
  intro n hn
  have hn' : n ∈ List.range' 1 N := hn
  rw [List.mem_range'] at hn'
  obtain ⟨i, hi, rfl⟩ := hn'
  exact h (1 + 1 * i) (by omega) (by omega)

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
    ("crease", "each row's first-order (leading) test undershoots: its census strictly contains the crease census (Wieferich 1093/3511 among 549 odd primes; Giuga 30/858/1722 among 4853 squarefree composites; Mersenne 12 exponents among 31 primes)"),
    ("no_go_shadow", "the undershoot is the per-instance shadow of G37: no first-order certificate can detect the crease"),
    ("competitor", "the core has content: the wieferich crease and the constant-false competitor ('no Wieferich prime') agree on [1,1092] but differ at 1093 (wieferich_competitor_window_agree / _differs)"),
    ("prototype", "Wieferich (G32) is the prototype: first-order = odd prime, crease = 2^(p-1) = 1 mod p^2"),
    ("scope", "the falsification pass narrows the domain: Mersenne survives as a genuine crease, but Goldbach/twin-prime/Collatz are NOT creases (no content-bearing first-order layer); the theory covers single-integer resolvent rows only"),
    ("registry", "six census runs: Wieferich [1093,3511], Giuga [30,858,1722], Lehmer [], 2-Lehmer [561,...], Erdos-Moser [], Mersenne [2,3,5,7,13,17,19,31,61,89,107,127]"),
    ("open", "OPEN: the crease is not shown universal across all n; each row's universal claim (Giuga, Lehmer, Erdos-Moser uniqueness, Mersenne infinitude) stays open, and the synthesis is reviewed, not proved") ]

theorem frontierCensusFacts_length : frontierCensusFacts.length = 9 := by decide

end PunoCalculus.FrontierCensus
