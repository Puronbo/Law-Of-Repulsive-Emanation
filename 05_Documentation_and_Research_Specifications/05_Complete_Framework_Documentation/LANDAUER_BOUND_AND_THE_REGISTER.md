# LANDAUER BOUND AND THE REGISTER

> **Scope note (read first).** This document is *interpretive narrative*: it
> separates established physics from an unsupported reading, and it does **not**
> claim a physical unification or settle any Millennium problem. The authoritative
> statement of what this project does and does not prove is
> [`WHAT_THIS_DOES_NOT_PROVE.md`](WHAT_THIS_DOES_NOT_PROVE.md).

**Status: interpretive (structural).** The only machine-checked content this note
leans on is the register's own orientation sign (cards **C10/C11`**,
`PunoCalculus/OrientationLaw.lean`, `PunoCalculus/DissipativeFlow.lean`,
`PunoCalculus/OrientationBoundedness.lean`). The physical reading is a map, not a
theorem.

---

## 1. What is established (verified anchors)

- **Landauer's principle (Landauer, 1961).** Erasing one bit at temperature `T`
> dissipates at least `E_bit = k_B * T * ln(2)`. The discrete quantum of the cost
> is `ln 2`. This is established statistical mechanics.

- **Landauer in the quantum many-body regime.** Aimet, Tajik, Schüttelkopf,
  Sabino, Sotiriadis, Guarnieri, Schmiedmayer, Eisert, *Experimentally probing
  Landauer's principle in the quantum many-body regime*, **Nature Physics 21,
  1326 (2025)**, arXiv:2407.21690 (TU Wien / Freie Universität Berlin). An
  ultracold Bose-gas quantum field simulator; the paper decomposes the entropy
  production into an information term and a thermodynamic term.

- **q-desics (quantum-corrected geodesics).** Koch, Riahinia, Rincon,
  *Geodesics in quantum gravity*, **Phys. Rev. D 112, 084056 (2025)**,
  arXiv:2510.00117 (TU Wien). If the metric is quantized and operators are
  averaged after variation, particles obey a modified equation of motion (the
  *q-desic*) rather than the geodesic of the averaged metric. The deviations are
  tiny for ordinary gravity and become large at cosmological scales only when the
  cosmological constant is included.

These three are real, published results. The register's own orientation sign
(card **C10/C11**) is real and machine-checked.

---

## 2. What is *not* established (narrative)

The following are **interpretive**, not proven, and are kept outside the boundary:

* "The universe is a **self-computing system**." The cited experiments show that
  quantum fields behave *information-theoretically*, and that geodesics receive
  quantum corrections. They do not establish computation as the fundamental
  substrate.
* "Information **has weight / mass**." Landauer gives a minimum *energy*
  dissipation; via `E = m c^2` that energy corresponds to a (tiny) mass. "Mass of
  information" is a compression, not a theorem.
* "Gravity, matter, and the **human mind** are the same currency." No experiment
  in either paper touches cognition. This is philosophy.

No card in `EXPLICIT_CLAIMS.md` rests on any of this.

---

## 3. Structural correspondence to the register (the honest part)

What *can* be said is a structural analogy between two independently established
objects -- nothing more:

| Register (machine-checked) | Landauer / q-desic (published) | Status |
|---|---|---|
| removable value of a `0/0` (card C17) | the discrete quantum `ln 2` per erased bit | analogy |
| orientation `r`, with `sign(log r)` (card C10/C11) | direction of dissipation (irreversible processing) | analogy |
| `r <= 1` attracting/bounded, dissipative | settles toward equilibrium, entropy produced | analogy |
| `r > 1` repelling/unbounded | drives away from equilibrium | analogy |
| dark energy = `0` / the center | the cosmological constant is the knob that makes q-desic deviations visible at large scale | analogy |

The companion script `02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/landauer_orientation.py`
asserts *only* the two structural facts (the positive quantum `ln 2`, and the sign
of `log r`), then states the correspondence as an analogy. It makes no physical
identification.

**Read literally, the analogy is: a discrete cost (`ln 2`) with a direction (the
side).** The register already has the direction half machine-checked; the Landauer
half supplies the magnitude. Neither half proves the other.

---

## 4. Sources to discount

Two references that circulated with this synthesis are **unverified** and should
not be cited:

* a ResearchGate item titled "... That Lead to Utopian Earth" -- the title alone
  disqualifies it as a source;
* `roadtoomega.substack.com`, "The Unifying Theory of Reality" -- self-published,
  not peer-reviewed.

These are not credible and are recorded here only so they are not mistaken for
supporting evidence.

---

## 5. Boundary

* This note is **interpretive** and makes **no physical claim** and **no
  Millennium claim**; see `WHAT_THIS_DOES_NOT_PROVE.md`.
* The machine-checked content it touches is card **C10/C11** (orientation sign),
  already certified in `EXPLICIT_CLAIMS.md` and `CLAIM_TRACEABILITY.md`.
* No register card is created here: by the program's own **T5** rule
  (`THEORY_OF_EVERYTHING.md` §6), a new card C39+ is admitted only if it is
  expressible via `(order, orientation)`. The Landauer/q-desic reading is an
  analogy, not a proof of such a reduction, so it stays a note.

---

## Related

* `WHAT_THIS_DOES_NOT_PROVE.md` -- the authoritative boundary.
* `THEORY_OF_EVERYTHING.md` -- the register program (cards C1--C38; this note is
  not a card).
* `EXPLICIT_CLAIMS.md` / `CLAIM_TRACEABILITY.md` -- cards C10 and C11 (orientation).
* `landauer_orientation.py` -- the structural companion script.
