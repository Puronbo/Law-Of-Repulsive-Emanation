# LANDAUER BOUND AND THE REGISTER

> **Scope note (read first).** This document states an **OPEN** claim in the
> register's card format (statement / missing entity / falsifier). It is **not**
> proved here, makes **no** physical claim, and settles **no** Millennium problem.
> The authoritative statement of what this project does and does not prove is
> [`WHAT_THIS_DOES_NOT_PROVE.md`](WHAT_THIS_DOES_NOT_PROVE.md).

**Status: Conjecture / Open.** The claim below is not proved here and is **not** a
register card: the claim asserts nothing that this repository has verified. Its
only machine-checked inputs are the register's own orientation sign (cards
**C10/C11**) and its removable value (card **C17**). By the program's own **T5**
rule (`THEORY_OF_EVERYTHING.md` §6), a new card C39+ is admitted only if it is
expressible via `(order, orientation)`; the claim here is the *statement of what
would be needed* to satisfy such a reduction, not a proof that it holds.

---

## 1. The claim (precise, falsifiable, OPEN)

**Claim (the Landauer–register bridge).** There exists a map `Phi` from register
states -- the pair `(order a, orientation r)` plus a `0/0` removable value
`lambda` (card C17) -- to thermodynamic states, such that:

1. `Phi(lambda)` is the equilibrium free-energy ratio of the modeled system;
2. `sign(log r)` (card C10/C11) equals the sign of the modeled entropy production;
3. the minimum work to erase one bit of the modeled critical content at
   temperature `T` is exactly `k_B T ln 2`.

If such a `Phi` exists and (1)–(3) hold, the Landauer bound and the register are
linked by a theorem. Until then the link is unproven.

---

## 2. What is established (verified inputs -- none of which is the bridge)

* **Landauer (1961):** erasing one bit at temperature `T` costs at least
  `k_B T ln 2`.
* **Nature Physics 21, 1326 (2025)**, arXiv:2407.21690 (Aimet et al.): the
  entropy production in the quantum many-body regime decomposes into an
  information term and a thermodynamic term.
* **q-desic:** Koch, Riahinia, Rincon, Phys. Rev. D 112, 084056 (2025),
  arXiv:2510.00117: quantum-corrected geodesics; deviations become large at
  cosmological scale only with the cosmological constant.
* **Register:** the orientation sign `sign(log r)` (cards C10/C11,
  `PunoCalculus/OrientationLaw.lean`, `PunoCalculus/OrientationBoundedness.lean`)
  and the `0/0` removable value `lambda` (card C17, `PunoCalculus/RemovableValue.lean`).
  The two-state instance of the schema is formalised in
  `PunoCalculus/InformationBridge.lean` (see §2b).

Each supplies one half. **None of them provides `Phi`.**

---

## 2b. What *is* machine-checked: the two-state (bit) instance

`PunoCalculus/InformationBridge.lean` formalises the arithmetic of the simplest
instance -- the **two-state (bit) register** -- and ties it to the register's own
orientation sign:

* `binaryEntropy_half` -- a fair bit carries `log 2` nats;
* `resetCost_two` -- resetting a two-state register costs `k_B T log 2`;
* `resetCost_eq_neg_orientation` -- `resetCost k_B T n = -k_B T * orientation (1/n)`,
  i.e. the cost is minus the scaled orientation;
* `orientation_reset_nonpos` -- for every `n >= 1`, `orientation (1/n) <= 0`
  (a reset is dissipative in the register's sense).

What this **does** establish: the two-state arithmetic is exact, and the reset
cost carries the *same* constant `ln 2` and the *sign* of the register
orientation. What it does **not** establish: it does not construct `Phi`, and it
does **not** derive the Landauer bound (that stays the cited physical input). The
map `Phi` remains the named missing entity of §3.

---

## 3. The missing entity (what would have to be proved or measured)

**Missing entity.** The map **`Phi`** -- a *validated physical instantiation of the
register*: a concrete dynamical system whose critical content is a `0/0` (C17) and
whose orientation is its dissipation sign (C10/C11), together with a proof (or a
measurement) that its one-bit erasure cost equals `k_B T ln 2` and satisfies
(1)–(3) above. Equivalently: a structure-preserving map from register states to
thermodynamic states that carries the removable value `lambda` to the free-energy
ratio and the orientation sign to the entropy-production sign.

**Falsifier.** A register state `(a, r, lambda)` whose realized one-bit erasure
cost is not `k_B T ln 2`, or whose `sign(log r)` disagrees with the sign of the
system's entropy production.

**Why the cited works do not close it.** Landauer supplies the bound (3) but no
register map; the 2025 many-body experiment supplies the entropy decomposition
but no register map; q-desic supplies quantum-corrected motion but no register
map. None constructs `Phi`, and none relates `lambda` or `r` to a cost.

---

## 3b. What is *not* established (narrative)

Kept outside the boundary, with no supporting result:

* "the universe is a **self-computing system**";
* "information **has weight / mass**"; 
* "gravity, matter, and the **human mind** are the same currency".

No card in `EXPLICIT_CLAIMS.md` rests on any of this.

---

## 4. Sources to discount

Two references that circulated with this topic are **unverified** and must not be
cited:

* a ResearchGate item titled "... That Lead to Utopian Earth" -- the title alone
  disqualifies it as a source;
* `roadtoomega.substack.com`, "The Unifying Theory of Reality" -- self-published,
  not peer-reviewed.

Recorded here only so they are not mistaken for supporting evidence.

---

## 5. Boundary

* The claim is **OPEN**; the missing entity (`Phi`) and the falsifier are named,
  so the claim can fail.
* This note makes **no physical claim** and settles **no Millennium problem**
  (`WHAT_THIS_DOES_NOT_PROVE.md`).
* Machine-checked content it relies on: cards **C10/C11** (orientation) and
  **C17** (removable value).
* No register card is created (T5): the note states what a card *would* need, and
  that is not yet proved.

---

## Related

* `WHAT_THIS_DOES_NOT_PROVE.md` -- the authoritative boundary.
* `THEORY_OF_EVERYTHING.md` -- the register program (cards C1--C38; this note is
  not a card).
* `02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/landauer_orientation.py`
  -- structural companion (prints the constraint, `PASS`).
* `01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/InformationBridge.lean`
  -- the two-state Lean instance (§2b).
* `EXPLICIT_CLAIMS.md` / `CLAIM_TRACEABILITY.md` -- cards C10, C11, C17.
* `landauer_orientation.py` -- the structural companion script.
