# Correction: `IF_C0_IS_0_OVER_0.md`

**Date:** 2026-09-29
**Status:** the C₀ half of the document is falsified; the zeta half is sound.
**Evidence:** `experiments/c0_zero_locus.py` (6/6 gates),
`experiments/c0_at_zeros.py` (5/5 gates), `experiments/chi_rho_vacuity_0_over_0.py` (PL-22).

`docs/IF_C0_IS_0_OVER_0.md` (2026-08-17) is a 20-section narrative built on one
claim: that `C₀ = V(q₀)/(N − |context|)` is a `0/0` form whose removable value
is the average energy per remaining node, that this value is unique because the
fold theorem makes the viscosity solution unique, and that it therefore mirrors
`g(s) = |ζ(s)|/|ζ(1−s)|` at the zeros of zeta.

That claim is false. The limit does not exist. Sections 1, 2, 3, 4, 5, 8 and 9
depend on it and fall with it. Sections 6 and 7 are separately wrong. The zeta
half (§2 table, §6, §9 items 1–4) is *correct* and should be kept.

---

## 1. The load-bearing error: the limit does not exist

The document asserts (§2) "The limit exists" and identifies the removable value
as "the average energy per non-context node".

The potential is defined in `Universals/hamiltonian_flow.py`:

```
V(q) = sum over non-context nodes of max(0, ALPHA - d(q,x))**2
ALPHA = 2.5,  d = Poincare-disk geodesic distance,  q0 = Origin
```

so with 10 nodes,

```
V(q0; ctx) = sum over the k nodes NOT in ctx of  (ALPHA - d(q0,x))**2
```

and `N − |ctx| = k` is the number of summands. The ratio is `V/k`, an average of
the `k` remaining terms.

The error is in treating `k → 0` as a continuous limit. `k` is a **step
function**: it takes the values 10, 9, 8, …, 1, 0. There is no continuous
parameter to take a limit along, and no reason for the average to converge.

More concretely, take any permutation of the 10 nodes and absorb them one at a
time. The average over the last `k` nodes is dominated by whichever node was
absorbed **last**, and the last node's own term is exactly the value you get:

| last node absorbed | one-step limit = its own term |
|---|---|
| Origin-region node | 6.250000 |
| Idea | 4.502584 |
| Art | 2.258699 |
| Bio | 2.020491 |
| Tech | 1.963888 |
| Music | 0.183593 |
| Mammal | 0.156648 |
| Silicon | 0.034593 |

**Nine distinct limits, spread 6.215407.** The value depends entirely on the
order of absorption, i.e. on the path. That is the definition of a
non-removable singularity. The "removable value" of §2 does not exist.

## 2. 24.434792 is not the quantity the document defines

The document's own number is quoted as the removable value (§8, §9). It is not:

- `V(q₀)` with context `{Tech, Silicon}`, as a **raw unnormalised sum**: `24.434792`
- the document's own formula `V(q₀)/(N − |ctx|) = 24.434792/8`: `3.054349`
- the actual one-step limits span: `[0.034593, 6.250000]`

So `24.434792` is neither the limit nor the average the document defines, and it
does not even lie in the range of the real limits. It is a raw sum for a
hand-picked two-node context.

## 3. The uniqueness claims collapse

- **§3, "the removable value is unique"** — false. Nine distinct limits.
- **§3, "the viscosity solution selects the unique path that gives a finite
  answer"** — false. All nine paths give finite answers; there is nothing to
  select between. The uniqueness theorem for viscosity solutions selects a
  *crease*, a different object; it does not make an average over a shrinking
  finite set well-defined.
- **§4, "the removable values are all the same number (C₀), because the 0/0
  form is invariant under the group of calendar transformations"** — false.
  A `0.01` shift of a single typed coordinate moves the value
  (base `6.250000` → `20.256122` for System, `20.204611` for Idea,
  `20.148215` for Mammal), and re-indexing alone — choosing the context —
  gives **768 distinct values** over the 1024 possible contexts of 10 nodes.
  The value is a function of the typed coordinates and of an arbitrary choice
  of which nodes are "in context".
- **§5, "consensus is the statement that all local removable values are the
  same number"** — not established. The per-site quantity is path-dependent, so
  there is no well-defined value to agree on.
- **§9, "you cannot choose C₀ because the 0/0 has no unique value without a
  path"** — the reasoning here is *right* and is the one part of §9 that
  survives on the C₀ side. But it is stated as supporting the existence of a
  measured value, when it in fact refutes it.

## 4. Origin and zeros are antipodal, not related

The document treats `q₀` as the singular point that "generates" the zeros.

- The zero set of `V` is `{q : d(q,x) >= ALPHA for every node}`, a star-shaped
  region with inner boundary `r*(θ)` spanning `0.8483 .. 0.9832` (not circular),
  covering about 86% of the disk.
- `C₀` restricted to the zero set is **identically 0**. So "C₀ for every zero"
  is a constant function and cannot encode anything about a zero's position.
- `V(q₀) = 26.433272` is the near-maximum of `V` on the disk (grid max
  `26.48`), not a zero. The origin is where the repulsion is maximal; the zeros
  are where every term has decayed to zero. They are opposite ends of the scale.

## 5. §6 is wrong independently of the 0/0 question

§6 states the error term as `π(x) − Li(x) = Σ_ρ Li(x^ρ) + ...`. This is not a
valid form. The correct explicit formula is for the Chebyshev function:

```
psi(x) = x - sum_rho x^rho/rho - log(2 pi) - (1/2)log(1 - x^-2)
```

with a `1/rho` weight and no `Li`, and `π(x)` is recovered from `ψ` by Möbius
inversion, not by a plain sum of `Li(x^ρ)`. The `1/ρ` weight is essential: it is
what makes the series converge. The rest of §6's discussion of bounded
amplitude on the line versus exponential growth off it is the standard
heuristic and is fine, but the formula it is attached to is not.

## 6. The zeta half is correct — keep it

The document's zeta claims are sound, and this repo has already established the
right boundary between what holds and what does not (PL-22,
`experiments/chi_rho_vacuity_0_over_0.py`):

- **`ζ(s)/ζ(1−s)` is genuinely removable at a zero `ρ`.** The limit is `χ(ρ)`
  and it is the same from every approach direction. Measured: the maximum
  deviation over five approach directions is `8.1e-09` at `eps = 1e-8` and
  falls linearly with `eps` (`8.1e-05`, `8.1e-07`, `8.1e-09`). So the
  document's claim that `|χ(ρ)|` is a unique removable value is **correct**.
- **`|χ(σ+it)| = 1` iff `σ = 1/2` on the strip `0 < σ < 1`.** Measured off the
  line at `t = 14.1347`: departures of `0.176, 0.041, 0.040, 0.150` at
  `σ = 0.30, 0.45, 0.55, 0.70`, and exact to `1e-41` at `σ = 1/2`. (Globally
  the form has two extra roots at `1/2 ± d(t)` for `t < t* = 6.2898`, all
  outside the strip.) So the document's "`|χ(ρ)| = 1` iff `Re(ρ) = 1/2`" is
  **correct**.
- **But it does not decide RH.** `|χ| = 1` is a property of the *whole line*: it
  holds at a non-zero impostor `1/2 + i(γ + 0.5)` to `1e-41`, where
  `|ζ| = 0.410`. So evaluating it at a zero cannot distinguish that zero from
  any other point on the line. The certification step is vacuous (PL-22 gate C),
  and the stronger claim "g ≡ 1 ⟺ RH" was already withdrawn on 2026-09-28
  (`docs/WHERE_0_OVER_0_SOLVES.md`, `docs/THE_UNIVERSAL_ZERO.md`).

**The asymmetry runs the other way from what a first reading suggests.** The
zeta `0/0` has the unique removable value that the C₀ `0/0` lacks. That is why
the analogy fails: not because the zeta side is uninformative, but because the
C₀ side is path-dependent.

## 7. What survives

- The scale itself, `V`, and the fact that its zero set is large, star-shaped,
  and non-circular.
- The fact that `C₀` is measured rather than chosen — for the trivial reason
  that it is a deterministic function of the typed coordinates.
- The viscosity-solution uniqueness theorem for the fold, as a statement about
  creases.
- §7's geometric description of the fold (smooth → singular → smooth) is a
  correct qualitative picture of a fold; it is the identification of that
  picture with a removable value that fails.
- The entire zeta half, as corrected in §6 above.

## 8. What does not survive

- "C₀ = 0/0" as a statement about a removable singularity (§1, §2, §8, §9).
- "The limit exists" and "the average energy per non-context node" as its value
  (§2, §8).
- Every uniqueness claim for that value (§3, §4, §5, §9).
- The identification of `24.434792` with any limit or average (§8, §9).
- The prime-counting formula of §6.
- Any transfer of information from the arithmetic side to the geometric side
  (§2 table, §9). The two sides do not share a structure; the zeta side has a
  removable singularity and the C₀ side does not.

---

**No Millennium Prize Problem follows from this document, and none is claimed.**
The `0/0` framing is a genuine and productive idea elsewhere in this repo — the
zeta case is a real instance of it — but on the C₀ scale the singularity is not
removable, so there is no value there to measure.

Run `python experiments/c0_zero_locus.py` to reproduce every number above.
