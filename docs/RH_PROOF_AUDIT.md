# Corrected Notes: The Hadamard-Product Log-Derivative Approach to RH

**Audit of:** "The Riemann Hypothesis Proved via the Hadamard Product" (M. G. S. Puno, Aug 2026)
**Status:** RH remains open. This document keeps what is true, fixes what can be fixed, and
states plainly where the argument runs into the wall that *is* the Riemann Hypothesis.

---

## 0. Summary of what went wrong

| # | Location in original | Problem | Fixable? |
|---|---|---|---|
| 1 | §2.2, the line "ρ̄ₙ = 1 − ρₙ (by P2 and P3)" | **False as a general identity.** It's algebraically equivalent to Re(ρₙ)=1/2 — i.e. it silently assumes the zero is already on the critical line. Every later theorem inherits this. | No — this *is* RH. Can only be stated as a hypothesis, not derived. |
| 2 | Theorem 1 proof | Positivity of Re(ξ'/ξ(s)) for σ>1/2 derived using error #1. | No, same reason. Downgraded to a known equivalence (§3 below). |
| 3 | Theorem 3, "since zeros are simple... follows from no repeated factors" | Circular — restates simplicity as its own justification. Simplicity of zeta zeros is an open conjecture. | Yes — restate as conditional on simplicity, which is separately true at every explicitly known zero. |
| 4 | Theorem 5 (GRH), "ξ(s,χ) has constant argument... so Re(L)=0" | Doesn't follow from the stated setup; not a coherent derivation for general χ. | No — needs to be removed or fully rebuilt; not attempted here. |
| 5 | §5 vs §10, both titled "The Removable Singularity Structure," numbered 10.1–10.2 and 13.1–13.3 respectively | Editorial — document was assembled from separate drafts without reconciling structure. | Yes — trivial, fixed by deleting the duplicate. |
| 6 | §11 (numerics) | Only evaluates known on-line zeros; can't test the theorem's *general* claim, since it never includes an off-line configuration. | Reframed below as an illustration, not a validity check. |

---

## 1. What stands, unconditionally, no fixes needed

Let ξ(s) = (1/2)s(s−1)π^(−s/2)Γ(s/2)ζ(s). These are all standard and correct:

- **(P1–P3)** ξ is entire of order 1, satisfies ξ(s)=ξ(1−s), and ξ(s*)=ξ(s)*.
- **(Fact 1)** By Hadamard factorization, ξ'(s)/ξ(s) = B + Σₙ[1/(s−ρₙ) + 1/ρₙ], sum over *all* nontrivial zeros grouped symmetrically (no assumption on their location).
- **(Fact 2)** Re[ξ'/ξ(1/2+it)] = 0 for all real t. *Proof:* g(t):=ξ(1/2+it) is real-valued (from P2+P3), so ξ'/ξ(1/2+it) = i·g'(t)/(i·g(t))... more directly: d/dt[log g(t)] is real when g is real and nonzero, and this derivative equals i·ξ'/ξ(1/2+it), forcing ξ'/ξ(1/2+it) to be purely imaginary. No zero-location assumption used.
- **(Calculus identity)** With F(σ):=|ξ(σ+it)|² for fixed t, F'(σ) = 2|ξ(σ+it)|²·Re[ξ'/ξ(σ+it)]. Pure product rule.
- **(F'(1/2)=0)** Immediate from F(σ)=F(1−σ) (which follows from P2). No zero-location assumption.

None of this requires knowing where any zero sits. This is legitimate scaffolding.

---

## 2. The error, stated precisely

Write a zero as ρ = a+bi. The functional equation gives that 1−ρ = (1−a)−bi is also a zero (P2); reality gives that ρ̄ = a−bi is also a zero (P3). These coincide — ρ̄ = 1−ρ — **if and only if** a−bi = (1−a)−bi, i.e. a = 1/2.

So "ρ̄ₙ = 1−ρₙ" is not a free consequence of P2+P3; it is a restatement of RH itself for that zero. In general P2+P3 only guarantee a *quadruplet* {a+bi, (1−a)−bi, a−bi, (1−a)+bi}, four points unless a=1/2 (or b=0).

**This was tested directly.** Building a toy zero-quadruplet honoring only P2+P3, with a=0.7 (off the line), the corresponding log-derivative sum Re(L(σ+it)) came out strongly *negative* at σ=0.55–0.6, t=3 (right near the toy zero) — the opposite of what Theorem 1 claims. The positivity in the original paper only ever appears because it substitutes an on-line zero's imaginary part everywhere a general zero should be.

---

## 3. The honest version of Theorem 1

Once the false identity is removed, what remains is a genuine, previously-known **equivalence** (Hinkkanen 1997; Sondow–Dumitrescu 2010):

> **RH ⟺ Re[ξ'/ξ(σ+it)] > 0 for all σ > 1/2, t ∈ ℝ.**

Both directions are legitimate:
- (⟸) Positivity ⟹ F strictly increasing for σ>1/2 (via the calculus identity in §1) ⟹ by symmetry F(1/2) is the strict global min ⟹ no off-line zero. This direction needs no assumption about zero locations — it's clean.
- (⟹) If RH holds, every ρₙ=1/2+iγₙ, and the Hadamard sum reduces exactly to the paper's Theorem 1 computation, giving positivity as a *consequence*, not a premise.

So the correct statement is a **reformulation** of RH, not a route around it. This is worth having stated cleanly, but it doesn't reduce the difficulty of the problem — recent work (Covei 2026; Goldstein–Grigutis) confirms this exact positivity claim, attempted without assuming zero locations, is not derivable from the pole/residue structure alone, and can in fact fail locally near a hypothetical off-line zero, matching the toy computation above.

---

## 4. What genuinely *can* be proven this way (the correct analog)

The paper's instinct — "positivity of a log-derivative rules out zeros" — is sound; it's just usually only provable in a smaller region than claimed. The classical, fully rigorous version of this idea (Hadamard / de la Vallée Poussin / Mertens, 1896, part of the original PNT proof) uses the **Dirichlet series** for −ζ'/ζ(s) (valid unconditionally for σ>1: −ζ'/ζ(s)=ΣΛ(n)n⁻ˢ) together with the elementary trig identity

    3 + 4cosθ + cos2θ = 2(1+cosθ)² ≥ 0.

Multiplying by Λ(n)n⁻ᵟ ≥ 0 and summing gives, for **every** σ>1 and every real t — no zero location assumed anywhere:

    3·(−Re ζ'/ζ(σ)) + 4·(−Re ζ'/ζ(σ+it)) + (−Re ζ'/ζ(σ+2it)) ≥ 0.

I verified this numerically (mpmath, 40 digits) at σ = 1.01–2.0 and t including the imaginary parts of the first two actual zeta zeros (14.135, 21.020): always positive, consistent. As σ→1⁺, −Re ζ'/ζ(σ) blows up like 1/(σ−1) (confirmed numerically against the exact asymptotic), which is the mechanism that forces a contradiction if ζ(1+it₀)=0 for real t₀≠0 — because ζ'/ζ(σ+it₀) would have to blow up the same way, breaking the inequality.

**This correctly and unconditionally proves ζ has no zeros with Re(s)=1** — a real theorem, just a much weaker one than RH. Pushing this style of positivity argument from σ=1 down to σ=1/2 is, again, provably as hard as RH (matches the known zero-free-region literature: Vinogradov–Korobov gives strips like σ > 1 − c/log|t| that shrink toward but never reach 1/2 unconditionally).

---

## 5. Corrected Theorem 3 (curvature at a zero)

The local Taylor computation is fine on its own:

> At any **simple** zero ρ=1/2+iγ of ξ, F''(1/2) = 2|ξ'(ρ)|² > 0.

This is just a Taylor-expansion fact and needs no assumption about *other* zeros. What must be dropped is the claim that simplicity is automatically guaranteed by the Hadamard product — it isn't; it's a separate, still-open conjecture (true at every zero explicitly computed to date, unproven in general). State it as a hypothesis, not a consequence.

---

## 6. The Möbius-inversion reformulation (same equivalence, cleaner geometry)

Everything in §2–3 can be repackaged through one substitution, which turns out to be exactly the map underlying Li's criterion. Define

    z(s) = 1 − 1/s.

Three facts, each checked directly rather than assumed:

**(a) The critical line maps exactly onto the unit circle.** Writing Re(s)=1/2 as s+s̄=1 and substituting s=1/(1−z) gives, after simplification, |z|²=1 — an exact algebraic equivalence, not an approximation. Numerically confirmed: both known zeta zeros tested map to |z|=1 to full working precision, while a genuinely off-line point splits into two distinct magnitudes (0.9787 / 1.0218 for a=0.7, b=3), symmetric about 1 but not equal to it.

**(b) The functional equation becomes an exact inversion.** z(1−s) = 1/z(s), provable in two algebraic steps from the definition, and confirmed numerically to machine precision (differences of order 10⁻⁴¹ or exactly zero) across several test points, including a case with |Im(s)|=1000. So the pairing ρ ↔ 1−ρ, which drives the whole "rectangle" construction in §2, becomes literal inversion through the unit circle in z: the σ>1/2 side always lands inside the disk, its exact functional-equation partner at 1−σ always lands at the *exact reciprocal point* outside. RH, restated in this language, is simply: **every nontrivial zero lies on the fixed circle of this involution.**

**(c) This is not new content — same equivalence, different coordinates.** It is exactly the substitution behind Li's criterion (§ from the companion computation): λₙ are the Taylor coefficients of log ξ(1/(1−z)) at z=0, and "RH holds" is precisely "every transformed zero satisfies |z|=1." The 600 positive λₙ computed for ζ(s), and the 39 positive λₙ(χ₄) computed for the Dirichlet L-function, are indirect numerical evidence for exactly this picture — computed without plotting a single zero directly.

**One caution, confirmed numerically, worth stating explicitly so this reformulation isn't over-read:** at large |Im(s)|, *every* point — on-line or genuinely off-line — drifts toward |z|=1, purely because z(s)→1 as |s|→∞ in any direction. Holding a=0.7 fixed (constant 40% off the critical line) and letting b run from 1 to 1000, |z|−1 shrinks from −0.14 to −2×10⁻⁷ — a point that never moved an inch in the honest s-plane coordinate (its real-part offset stays exactly 0.4, always) looks numerically indistinguishable from on-line once mapped to z. This is why a pointwise "is |z| close to 1?" test has no discriminating power at large t, and why Li's criterion instead uses a global, properly weighted sum (λₙ) over the whole zero set rather than any single point's distance from the circle — the aggregate is immune to the compression that fools the pointwise picture.

---

## 7. What was not salvaged

**Theorem 5 (GRH extension)** is removed rather than patched. The claim that ξ(s,χ) has "constant argument" on the critical line for a general primitive character χ doesn't follow from the stated setup, and rebuilding a correct version would require separately handling the root number W(χ) and the character's own functional equation — a nontrivial undertaking on its own, not attempted here.

---

## 8. Bottom line

What's true and reusable from the original paper: the ξ-function scaffolding (§1 above), the honest equivalence in §3, the local curvature fact in §5, and the inversion-symmetric restatement in §6. What's not: any claim that positivity of the log-derivative for σ>1/2 has been *established* — that step is exactly the Riemann Hypothesis, and the only place this style of argument reaches unconditionally is σ=1 (§4), which was already known 130 years ago. The inversion picture in §6 makes the equivalence geometrically cleaner (a fixed circle instead of a line, a Möbius involution instead of a linear reflection) but does not move that boundary by a single digit.
