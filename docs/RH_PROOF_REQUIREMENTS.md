# What a proof of RH needs to be

(2026-08-16.  Written from the repo's measured position: exact M/ψ to 10^14,
22,491 located zeros to t = 20000, the explicit-formula height experiments
(Ch. 5.21r/s), the spectral comparison (Ch. 5.21u), the divisor-fold and
tree tests (Ch. 5.21t), and the AUDIT's negative certifications of the
letter's spectral constructions.)

## 1. The statement, precisely

**RH (Riemann hypothesis).**  Every nontrivial zero ρ = β + iγ of the
Riemann zeta function satisfies β = 1/2.

Equivalently: the function ζ(s) has no zeros in the half-plane
Re(s) > 1/2, and (by the functional equation) none in Re(s) < 1/2.

A proof of RH is therefore **one global statement**: a uniform bound over
ALL nontrivial zeros, or over ALL x, that no finite computation can supply
and no finite census can decide.

## 2. The equivalences the repo has measured — each is the same single fact

RH ⟺ |ψ(x) − x| ≤ C·x^{1/2}·log²x for all x ≥ 3        (von Koch 1901)
RH ⟺ M(x) = O(x^{1/2+ε}) for every ε > 0               (Littlewood 1912)
RH ⟺ π(x) = Li(x) + O(x^{1/2}·log x)
RH ⟺ S(t) = o(log t) as t → ∞,
        S(t) = (1/π)·arg ζ(1/2 + it), continuous from the axis
RH ⟺ Λ ≤ 0, where Λ is the de Bruijn–Newman constant   (de Bruijn, Newman)
         (and Λ ≥ 0 is PROVEN: Rodgers–Tao 2018)

The repo measured every one of these objects:
- exact ψ(10^11..10^14) = 100000058456.4 / … / 100000000618672.4, with
  ψ(x)−x always a small fraction of √x — the *size* RH predicts,
  but only at 4 points (Ch. 5.21s);
- M(10^k), k = 1..14, OEIS-exact; max measured |M|/√x = 0.5706 at
  x = 7,766,842,813 — never reaching even the (false) Mertens conjecture's
  bound √x (Ch. 5.21q);
- S-walk: max|S|/log t = 0.146 over t ≤ 20000 — the *rate* S(t) = o(log t)
  wants, but only over a finite interval (Ch. 5.21u).

All four quantities behave at every computable height exactly as RH
predicts.  None of that is evidence of the kind a proof needs, because:

## 3. Why no computation can ever decide RH

- **The statement is a supremum over an infinite set.**  RH fails if there
  exists ONE zero off the line, wherever it is.  Verification (Platt–Trudgian:
  all heights to 3·10^12) rules out failures only inside the checked box.
- **The two proven-false-but-never-seen theorems warn us directly.**  The
  Mertens conjecture |M(x)| < √x is PROVEN false (Odlyzko–te Riele 1985;
  Pintz: counterexample below exp(1.59e40)) yet |M(x)| < √x holds at every
  x ≤ 10^16 ever computed — the repo's census even reproduced the same
  misleading signal (max measured ratio 0.5706).  π(x) > Li(x) is PROVEN
  to occur, though π(x) < Li(x) at every computable height.  Both theorems
  are proof that the computable range can look exactly RH-correct while the
  truth beyond is different.  No finite amount of "it all works so far" has
  logical force.
- **The explicit formula is conditionally convergent and non-monotone.**
  Ch. 5.21r/s measured that truncating Σ_ρ x^ρ/ρ at T does not improve
  monotonically: at x = 10^14, T = 20000's ψ residual −88932 is worse than
  T = 10000's −80364.  There is no finite T whose value certifies any x.
  A proof cannot be "sum more zeros"; it must bound the sum of ALL of them.

## 4. The five routes, and the exact missing theorem in each

A proof must arrive as ONE of the following.  Each is a known shape; none
has been filled in.  The repo's experiments certify what each shape is NOT.

### Route A — Arithmetic (von Koch / Littlewood): prove the uniform bound
**Missing theorem:** |ψ(x) − x| ≤ C √x log²x for all x ≥ 3 (or
M(x) = O(x^{1/2+ε})).
The known path: an explicit formula whose ERROR TERM is bounded uniformly.
That error is a sum over ALL zeros; bounding it uniformly requires knowing
all zeros have β = 1/2 (or enough of them do, uniformly) — which is RH
itself.  The repo's exact arithmetic (Ch. 5.21q/s) provides the cleanest
possible target values but the path is genuinely circular unless the input
is a structural theorem about ζ (below), not arithmetic alone.

### Route B — Zero-density / argument: force the line
**Missing theorem:** N(σ, T) = 0 for σ > 1/2 (no zero off the line), or
S(t) = o(log t).
The known path: bound the variation of arg ζ(1/2 + it).  Selberg's work
gives S(t) = O(log t) unconditionally (and the mean square laws); RH is
the factor-of-log improvement.  Everything measured (S-walk 0.146) says the
improvement holds; the missing step is a global bound on the variation of
an oscillatory sum with no finite witness.  This is where the "time
reading" of Ch. 5.21u lives: the explicit formula is a Fourier sum in
u = log x with frequencies γ; a proof must bound the amplitudes' joint
effect for all u, not observe a quiet finite walk.

### Route C — Hilbert–Pólya: find the operator
**Missing theorem:** a self-adjoint (or positivity-preserving) object whose
discrete spectrum is exactly {γ_n} — then self-adjointness gives real
spectrum and the functional equation moves it to Re ρ = 1/2.
The known candidates (Berry–Keating xp; Bender–Brody; adelic/Connes
approaches) are all open; none is accepted.  The repo's own spectral
constructions were certified NOT to work (AUDIT negatives; Ch. 5.21u
measured them Poisson/integrable, the opposite family from the zeros).
Ch. 5.21u also measured the strongest positive datum: the zeros ARE
GUE-like (KS 0.037 to the Wigner surmise, level repulsion β = 1.64,
determinantal rigidity) — so the Hilbert–Pólya philosophy has empirical
backing, but resemblance is not construction.

### Route D — de Bruijn–Newman: prove Λ = 0
**Missing theorem:** Λ ≤ 0.  (Λ ≥ 0 is already PROVEN, Rodgers–Tao 2018;
RH ⟺ Λ ≤ 0.)  A proof of Λ ≤ 0 would therefore complete the proof of RH
in one line: Λ = 0.
The known path: show H_t(x) has only real zeros for every t > 0 (equivalently
no complex zero of H_t at any positive temperature), uniformly in t and x.
Numerics (Ki–Kim–Lee) give only lower bounds Λ > −1.1e-12.  No finite N
rules out a complex zero of H_t; the missing step is a repulsion/uniformity
statement over the whole family.  This is the single most self-contained
"proof needed": **one inequality for a concrete entire function, already
known to satisfy the ≥ half.**

### Route E — Structural: a new positivity or functional identity
**Missing theorem:** some positive definite kernel, determinantal
process, or exact functional identity that forces ζ ≠ 0 off the line.
The repo's Ch. 5.21t fold arithmetic (1⋆1 = τ, 1⋆μ = δ with
Σ μ(d)⌊x/d⌋ = 1 exact, μ⋆log = Λ) is exact but arithmetic-only; the
tree/body mirror failed and the golden fold failed.  Nothing in the measured
folder is a candidate identity; the honest reading is that such an identity
does not exist in the accessible finite arithmetic at all.

## 5. The single sentence

**A proof of RH = one uniform global bound.**  The most tractable complete
statement available today is:

    Prove Λ ≤ 0 for the de Bruijn–Newman function H_t (equivalently: the
    curve x ↦ H_t(x) has only real zeros for every t > 0).

because Λ ≥ 0 is already a theorem.  Its competitors are all equivalently
hard and all require a genuinely new uniform idea:

    |ψ(x) − x| ≤ C √x log²x for all x ≥ 3,
    or S(t) = o(log t) for all t,
    or a self-adjoint operator with spectrum {γ_n}.

No computation, however deep (the repo's 10^14 arithmetic, its 22,491
zeros, its explicit formulas) can enter the proof of any of these: each is
a supremum over the infinite, and each computable prefix is exactly what
the two proven-false theorems warn us not to trust.  RH remains open, and
the proof — if it exists — is a structure theorem, not a computation.
