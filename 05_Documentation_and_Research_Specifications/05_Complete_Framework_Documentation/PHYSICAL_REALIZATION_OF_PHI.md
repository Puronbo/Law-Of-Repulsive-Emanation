# Physical realization of `Phi`: candidate measured systems

> **Scope banner.** This note is *narrative*. It makes **no physical claim**, no
> settlement claim, and it derives nothing. Read it against the authoritative
> boundary `WHAT_THIS_DOES_NOT_PROVE.md`: no Millennium problem and no physical
> law is settled here. All content is **OPEN** and is a *candidate list*, not a
> result.

Status: **OPEN** (candidate identification, not a proof). No register card is
created: by the T5 rule (`THEORY_OF_EVERYTHING.md` §6) a card C39+ requires an
expressible `(order, orientation)` reduction, which is exactly what is still
missing.

---

## 1. What is being identified

`LANDAUER_BOUND_AND_THE_REGISTER.md` states an **OPEN** claim whose **missing
entity** is the map `Phi`: a *validated physical instantiation of the register* --
a concrete dynamical system whose critical content is a `0/0` (card C17), whose
orientation is its dissipation sign (cards C10/C11), and whose one-bit erasure
cost is `k_B T ln 2`. `PunoCalculus/InformationPhi.lean` constructs `Phi` as the
register's *own model* of a thermodynamic state; §2c of that note flags the wall:
**identifying it with a measured apparatus** is the missing entity. This note
collects the measured apparatuses that already realize the two-state Landauer
part, and asks whether any of them is itself a **mixture of two or more**
channels -- which is the structure `PunoCalculus/InformationMixture.lean` checks.

## 2. Measured systems realizing the two-state (bit) Landauer content

| System | Realization | Reported quantity | Reference |
|---|---|---|---|
| Colloidal bead in a double-well trap | optical tweezers | `⟨Q⟩ → 0.72 k_B T` vs the `0.693 k_B T` bound | Bérut et al., *Nature* **483**, 187 (2012), DOI 10.1038/nature10872 |
| Electrophoretic bead in a "virtual" trap | feedback trap | information-to-energy conversion at the bit | Jun, Gavrilov, Bechhoefer, *PRL* **113**, 190601 (2014) |
| Single-electron box (SEB) | one-electron manipulation | one-bit manipulation in a nanoscale device | Koski et al., *PRL* **113**, 260601 (2014) |
| Nanomagnetic memory cells | thermally activated switching | reset heat near the bit bound | Hong et al., *Sci. Adv.* **2**, e1501492 (2016) |
| Molecular nanomagnet | single-molecule magnet | reset work `≈ ln 2` | Gaudenzi et al., *PRL* **120**, 117001 (2018) |
| Trapped ion | single-atom engine | Landauer bound in a quantum two-level system | Yan et al., *PRL* **120**, 190601 (2018) |
| Superconducting qubit + cavity | Maxwell-demon memory (two subsystems) | work below the bound; memory entropy `≫ ln 2` | Cottet et al., *PNAS* **114**, 7561 (2017) |
| Superconducting flux logic | single-flux-quantum bits | `W = 1.25 k_T`, `≈ 5.4×` the bound | Saira et al., *Phys. Rev. Research* **2**, 013249 (2020) |
| Levitated nanosphere | optomechanical memory | single-quantum Landauer erasure | Ciampini et al., *Phys. Rev. Research* **7**, 043321 (2025) |
| DNA hairpin | single-molecule folding | resetting below `k_B T ln 2` (feedback) | Ribezzi-Crivellari & Ritort, *Nat. Phys.* **15**, 660 (2019) |
| Underdamped oscillator | optomechanical | information-engine bounds | Dago et al., *PRL* **126**, 140601 (2021) |

Each measures the *cost* side (the `k_B T ln 2` quantum and its deviations). None
constructs `Phi`: none relates the register's removable value `lambda` (C17) or
orientation `r` (C10/C11) to the measured cost. Bibliographic details here are
recorded as a working list and should be re-verified before any external use.

## 3. Is the measured system a mixture of two or more?

Yes -- the measured entropy production is repeatedly found to **decompose**, which
is precisely the structure of `PunoCalculus/InformationMixture.lean`.

* **Information vs thermodynamic split.** Aimet et al., *Nature Physics* **21**,
  1326 (2025), arXiv:2407.21690: the many-body entropy production reads
  `Σ = ΔI + ΔD`, an **information term** `ΔI` plus a thermodynamic (athermality)
  term `ΔD`; equivalently `β ΔE + ΔS`. Two channels.
* **Population vs coherence split (quantum).** Xue et al. (2024): the entropy
  production decomposes as `Σ = Σ_pop + Σ_coh`, a **population** (classical) part
  plus a **coherence** (quantum) part. Two channels.
* **Single-system three-channel split.** Yan et al., *PRL* **120**, 190601 (2018),
  on the trapped ion: `ΔQ / k_B T = ΔS + I(S′:R′) + D(ρ_R′‖ρ_R)`, a weighted
  thermodynamic term plus a **mutual-information** term plus a relative-entropy
  term. Three channels.
* **Two physical subsystems.** Cottet et al., *PNAS* **114**, 7561 (2017): the
  measured object is literally two degrees of freedom -- the qubit **system `S`**
  and the demon **memory `D`** -- whose joint state is a mixture. Koski et al.,
  *PRL* **115**, 260602 (2015): **two coupled devices / reservoirs**.

So the measured realization of the register is, in every clean case, a **mixture
of two or more channels**, and the mixture carries an **information term** on top
of the weighted parts -- the exact content of `entropy_mixture`.

## 4. Which candidate is closest to `Phi`?

Ranked by how much of the missing entity it supplies:

1. **Trapped ion (Yan 2018)** -- cleanest single-system *three-channel* mixture;
  two-state content and coherence are both measured in one apparatus.
* **Superconducting qubit + cavity (Cottet 2017)** -- the clearest *two physical
  subsystems* (system + demon memory), i.e. a literal mixture of registers.
* **Quantum many-body split (Aimet 2025)** -- the cleanest *information vs
  thermodynamic* decomposition, matching `entropy_mixture`'s two-channel form.
* **Single-electron box (Koski 2014)** / **flux logic (Saira 2020)** -- the
  cleanest *state-counting* reset (`n`-state register), matching `resetCost`.

Strongest single candidate: if the register's "mixture" is read as *two physical
subsystems*, the superconducting qubit + cavity (Cottet 2017); if it is read as an
*information vs thermodynamic channel split*, the quantum many-body decomposition
(Aimet 2025). The trapped ion (Yan 2018) is the cleanest case exhibiting **three**
channels in one apparatus.

## 4b. The machine-checked part: the mixture algebra

`PunoCalculus/InformationMixture.lean` formalises exactly the decomposition these
measurements exhibit, with no physical content attached:

* `entropy_mixture` -- for a genuine mixture (`0 < t < 1`) of two positive,
  normalised probability vectors,
  `H(mix) = t * H(a) + (1 - t) * H(b) + binaryEntropy t`: the mixture's entropy is
  the weighted parts **plus** a mixing (information) term.
* `binaryEntropy_nonneg` -- the mixing term is non-negative for `0 <= t <= 1`.
* `entropy_mixture_ge` -- hence a mixture carries **at least** the weighted entropy
  of its parts; the excess is the information term.
* `entropy_mixture_half` -- a fair mixture (`t = 1/2`) adds exactly `log 2`, the
  same constant as the one-bit erase cost (`InformationBridge.resetCost_two`).

This is the classical scaffold that a measured realisation would have to
instantiate; it does **not** identify any apparatus.

## 5. Falsifier (concrete, measured)

A measured system, presented as a candidate `Phi`, that (a) is *not* a mixture --
its entropy production shows no separable information/thermodynamic (or
population/coherence) channel -- yet is claimed to satisfy the register map; **or**
(b) whose measured one-bit erasure cost is not `k_B T ln 2`, or whose measured
dissipation sign disagrees with `sign(log r)` (C10/C11). Either falsifies the
candidate instantiation of `Phi`.

## 6. Boundary

* The identification is **OPEN**; the missing entity (`Phi` as a *validated
  measured system*, not the register's own model) and the falsifier are named.
* This note makes **no physical claim** and settles **no Millennium problem**
  (`WHAT_THIS_DOES_NOT_PROVE.md`).
* No register card is created (T5).

---

## Related

* `WHAT_THIS_DOES_NOT_PROVE.md` -- the authoritative boundary.
* `LANDAUER_BOUND_AND_THE_REGISTER.md` -- the OPEN claim, its missing entity and
  falsifier, and the constructed `Phi` on the relaxation `0/0` (§2c).
* `01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/InformationMixture.lean`
  -- the machine-checked mixture algebra (§4b).
* `01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/InformationBridge.lean`
  / `InformationPhi.lean` -- the two-state and `Phi` bricks.
* `THEORY_OF_EVERYTHING.md` -- the register program (cards C1--C38; this note is
  not a card).
