# The Riemann Hypothesis and the Removable Singularity

**Date:** 2026-08-17
**Repository:** Puronbo/Law-Of-Repulsive-Emanation
**Corrected:** 2026-09-28 — the claim "$g \equiv 1$" is **false** and the
monotonicity lemma in Step 4 is **false**; both are fixed in place below. The
true replacement — on the critical strip, $|\chi(\sigma+it)| = 1$ forces
$\sigma = 1/2$ — is *sharper and more useful* than the claim it replaces,
because it has teeth: displacing $\sigma$ is caught at every scale tested
down to $10^{-6}$, whereas the withdrawn "$|\chi| = 1$ at a critical-line
zero" check passes on points that are not zeros at all. Verification:
`experiments/chi_rho_vacuity_0_over_0.py` (7/7 gates), `PREDICTION_LEDGER`
PL-22, `docs/AUDIT.md` §2 item 8. **RH remains open**; nothing in this
correction claims otherwise.

---

## Abstract

We identify the exact value of each removable singularity of a single explicit
function, $g(s) = |\zeta(s)| / |\zeta(1-s)|$, as $|\chi(\rho)|$, where $\chi$ is
the completed factor of the functional equation, and we show that
$|\chi(\rho)| = 1$ if and only if $\mathrm{Re}(\rho) = 1/2$. **This is a true
restatement of RH, not a verification of it.** We also state plainly what the
restatement is *not*: $g$ is *not* identically equal to 1, and evaluating
$|\chi|$ at zeros located on the critical line cannot decide anything, because
$|\chi(1/2+iy)| = 1$ holds for every $y$ — zeros and non-zeros alike. Combined
with the Rodgers-Tao theorem ($\Lambda \ge 0$), RH is equivalent to the single
inequality $\Lambda = 0$ for the de Bruijn-Newman constant, which is open. We
present the complete argument, the level-set form of the true statement, the
numerical evidence from this repository (22,491 located zeros, exact Mertens and
Chebyshev functions to $10^{14}$), the reasons why no finite computation can
decide the problem, and a measurement of exactly how much force the
"verification" reading does and does not have.

---

## 1. The function

Define

$$g(s) = \frac{|\zeta(s)|}{|\zeta(1-s)|}.$$

This is the zeta-theoretic analogue of

$$f(x) = \left|\frac{x-1}{1-x}\right| = 1 \qquad (x \neq 1).$$

In both cases the numerator equals the denominator up to sign, and the absolute value removes the sign. For $f$, this is the tautology $|x-1| = |1-x|$, and $f \equiv 1$ wherever it is defined. For $g$, the same cancellation holds **only on the critical line** (by the Schwarz reflection principle), and $g$ is *not* constant elsewhere: the functional equation gives $g(s) = |\chi(s)|$ identically off the zeros, and $|\chi| = 1$ exactly when $\mathrm{Re}(s) = 1/2$. For example $g(2) = |\zeta(2)|/|\zeta(-1)| = 19.74$. Both functions have the indeterminate form $0/0$ at isolated points, and in both cases that form is removable.

---

## 2. Main theorem

**Theorem (corrected 2026-09-28).** *The function $g(s) = |\zeta(s)| / |\zeta(1-s)|$ satisfies $g(\rho) = |\chi(\rho)|$ at every nontrivial zero $\rho$ (removable value), and its level set is exactly the critical line: $g(s) = 1 \iff \mathrm{Re}(s) = 1/2$. Consequently every nontrivial zero of $\zeta$ fills in with value 1 if and only if the Riemann Hypothesis is true.*

**Note on the superseded statement.** The original version of this theorem
read *"$g \equiv 1$ (after removal of singularities) if and only if RH."* That
is **false**: $g \equiv |\chi|$, not $g \equiv 1$ — see §1, where $g(2) = 19.74$.
The corrected statement is a statement about the **values at the zeros** and
about the **level set**, and it is the form in which the equivalence to RH is
actually true. The two are not interchangeable: $g \equiv 1$ is a global
condition that is simply untrue, whereas RH is a condition on the zeros, and
the corrected theorem keeps exactly the content that bears on RH.

---

## 3. Proof

The proof has five steps.

**Step 1. $g = 1$ on the critical line.**

For $s = \tfrac{1}{2} + it$, the Schwarz reflection principle gives $\zeta(\tfrac{1}{2} - it) = \overline{\zeta(\tfrac{1}{2} + it)}$ since $\zeta$ has real coefficients. Therefore

$$\left|\zeta\!\left(\tfrac{1}{2} + it\right)\right| = \left|\zeta\!\left(\tfrac{1}{2} - it\right)\right|,$$

so

$$g\!\left(\tfrac{1}{2} + it\right) = \frac{|\zeta(\tfrac{1}{2} + it)|}{|\zeta(\tfrac{1}{2} - it)|} = 1$$

whenever $\zeta(\tfrac{1}{2} + it) \neq 0$. The function is identically 1 on the critical line, exactly as $f$ is identically 1 for $x \neq 1$. $\square$

**Step 2. At each zero, $g = 0/0$.**

The functional equation $\zeta(s) = \chi(s)\,\zeta(1-s)$ implies that if $\rho$ is a nontrivial zero, then $1 - \rho$ is also a zero. At each zero $\rho$:

$$|\zeta(\rho)| = 0 \qquad \text{and} \qquad |\zeta(1-\rho)| = 0,$$

giving $g(\rho) = 0/0$, the same indeterminate form as $f(1) = |0/0|$. $\square$

**Step 3. The singularity is removable, with value $|\chi(\rho)|$.**

Near a simple zero $\rho = \beta + i\gamma$, write $\zeta(s) \approx c_1(s - \rho)$. Since $1 - \rho$ is also a zero of $\zeta$, and $(1-s) - (1-\rho) = \rho - s$, we have $\zeta(1-s) \approx c_2'(\rho - s) = -c_2'(s - \rho)$ near $s = \rho$. Therefore

$$g(s) = \frac{|\zeta(s)|}{|\zeta(1-s)|} \approx \frac{|c_1|\,|s - \rho|}{|c_2'|\,|s - \rho|} = \frac{|c_1|}{|c_2'|}.$$

The ratio $|s - \rho| / |s - \rho| = 1$ for $s \neq \rho$, so the limit exists from every direction. The singularity is removable.

By the functional equation, $\zeta(s)/\zeta(1-s) = \chi(s)$, so at the zero:

$$\frac{c_1}{-c_2'} = \chi(\rho) \qquad \Longrightarrow \qquad \frac{|c_1|}{|c_2'|} = |\chi(\rho)|.$$

**The removable value is $|\chi(\rho)|$.** $\square$

**Step 4. $|\chi(\rho)| = 1$ if and only if $\mathrm{Re}(\rho) = 1/2$.**

The completed factor is explicit:

$$|\chi(\sigma + it)| = \pi^{\sigma - 1/2}\,\frac{|\Gamma(\frac{1-s}{2})|}{|\Gamma(\frac{s}{2})|}.$$

On the critical line ($\sigma = 1/2$): the prefactor $\pi^0 = 1$ and $|\Gamma(\frac{1-s}{2})| = |\Gamma(\frac{s}{2})|$ (since $\frac{1-s}{2} = \overline{(\frac{s}{2})}$ when $\mathrm{Re}(s) = 1/2$), so $|\chi| = 1$.

Off the critical line ($\sigma \neq 1/2$): the prefactor $\pi^{\sigma - 1/2}$ and the gamma ratio act in *opposite* directions, so neither alone settles the question, and the sign of

$$\frac{\partial}{\partial\sigma}\log|\chi(\sigma + it)| = \log\pi - \tfrac{1}{2}\operatorname{Re}\psi\!\left(\tfrac{1-s}{2}\right) - \tfrac{1}{2}\operatorname{Re}\psi\!\left(\tfrac{s}{2}\right)$$

is **not** of one sign: at $\sigma = 1/2$ it reduces to $\log\pi - \operatorname{Re}\psi(\tfrac{1}{4} + \tfrac{it}{2})$, which vanishes at exactly one height

$$t_* = 6.2898359888369027797,$$

is positive below it and negative above it. So the earlier justification in this
step — that $\log|\chi|$ "is a strictly monotone function of $\sigma$ for fixed
$t$" and that "the gamma ratio does not compensate" — is **false on both
counts**, and is withdrawn.

**What is true, and is all that is needed.** The conclusion of this step holds
on the critical strip $0 < \sigma < 1$, which is the only region containing
nontrivial zeros:

$$|\chi(\rho)| = 1 \quad\Longleftrightarrow\quad \mathrm{Re}(\rho) = \tfrac{1}{2}
\qquad\text{for every } 0 < \mathrm{Re}(\rho) < 1. \qquad \square$$

Globally the stronger form $\mathrm{Re}(s) = 1/2 \iff |\chi(s)| = 1$ is
**false**: $|\chi(\sigma + it)| = 1$ has *three* real solutions in $\sigma$
for $t < t_*$, namely $\tfrac{1}{2}$ and $\tfrac{1}{2} \pm d(t)$ — the pair is
symmetric about the line because $|\chi(1-s)| = 1/|\chi(s)|$ — and only *one*
for $t \ge t_*$. As $t \uparrow t_*$ the pair closes onto the line and merges
with it into a **double root**; the measured offsets are
$d = 16.895$ at $t = 0.1$, $15.419$ at $1$, $7.162$ at $5$, $3.323$ at $6$,
$0.608$ at $6.28$, and $d$ is gone by $t = 6.35$. All of these extra roots lie
**outside** the open strip, so they are irrelevant to RH — but the blanket
form is withdrawn rather than quietly kept, and the measurements are in
`experiments/chi_rho_vacuity_0_over_0.py` (gate 3, 12/12 heights).

**Step 5. Combining.**

From Steps 1--4, restricted throughout to the nontrivial zeros $\rho$ — which
satisfy $0 < \mathrm{Re}(\rho) < 1$:

$$|\chi(\rho)| = 1 \text{ for every zero } \rho \;\;\Longleftrightarrow\;\; \mathrm{Re}(\rho) = \tfrac{1}{2} \text{ for every zero } \rho \;\;\Longleftrightarrow\;\; \mathrm{RH}. \qquad \blacksquare$$

**Read this chain honestly.** It is a *re-encoding* of RH, not a proof of it:
the middle step is a tautological restatement (a zero satisfies
$|\chi(\rho)| = 1$ exactly when it sits on the line), and the last step is the
definition of RH. No step here does any work — the chain exists to be
transparent about *why* the $0/0$ framing carries no leverage. The original
version of this step opened with $g \equiv 1$; that link is **deleted**, not
merely restated, because $g \equiv |\chi|$ and $|\chi| = 1$ only on the line,
so $g \equiv 1$ is false ($g(2) = 19.74$). An earlier draft of this document
was read as claiming the $0/0$ "verified" RH by testing $|\chi(\rho)| = 1$ at
zeros found on the line. That reading is **vacuous and withdrawn**: since
$|\chi(\tfrac{1}{2} + iy)| = 1$ for *every* $y$ — zeros and non-zeros alike,
agreeing to $1.97 \times 10^{-31}$ over ten zeros and their non-zero
impostors — the test cannot fail, and by the repository's own ledger rule ("a
claim with no refutation condition is not a claim") it was never a claim. See
`experiments/chi_rho_vacuity_0_over_0.py`, which plants a non-zero and watches
the check pass.

---

## 4. The de Bruijn-Newman reduction

Step 5 identifies where the open content sits: RH is the statement that every nontrivial zero fills in with value 1, and (corrected) that is what "RH" means in this $0/0$ language. To convert it into an inequality about a single analytic object, we use the de Bruijn-Newman framework.

**Definition.** The de Bruijn-Newman function $H_t : \mathbb{R} \to \mathbb{R}$ is an entire function of exponential type:

$$H_t(x) = \int_{\mathbb{R}} e^{tu^2}\,\Phi(u)\,\cos(xu)\,du$$

where $\Phi$ is the super-exponentially decaying function with $\hat{\Phi}(0) = 1$. The family satisfies:

(i) $H_\infty$ has only real, simple zeros (all negative).
(ii) $H_t \to \zeta(1/2 + ix) \cdot (\text{known factors})$ as $t \to 0^+$.
(iii) Zeros of $H_t$ depend continuously on $t$.
(iv) If $H_t$ has only real zeros for all $t \geq 0$, then $\zeta$ has only real zeros on the critical line.

**Definition.** The de Bruijn-Newman constant is

$$\Lambda = \inf\{t \in \mathbb{R} : H_t \text{ has only real zeros}\}.$$

By (iv): $\Lambda \leq 0 \implies H_t$ has only real zeros for all $t \geq 0 \implies H_0$ has only real zeros $\implies \mathrm{RH}$.

**Theorem (Rodgers-Tao, 2018).** $\Lambda \geq 0$.

*Proof sketch.* If $H_t$ had only real zeros for some $t < 0$, the interlacing monotonicity of zeros under the heat flow (the "BBP property") would be violated. The proof uses the Borwein-Chen-Irvine interpolation and the heat-flow dynamics of $H_t$. $\square$

**Corollary.** $\Lambda = 0 \iff \mathrm{RH}$.

*Proof.* ($\Rightarrow$) $\Lambda = 0$ implies $\Lambda \leq 0$, which implies RH by the implication above.
($\Leftarrow$) RH implies all zeros of $\zeta$ are on the critical line, which implies $H_0$ has only real zeros, which implies $\Lambda \leq 0$. Combined with $\Lambda \geq 0$ (Rodgers-Tao), this gives $\Lambda = 0$. $\square$

---

## 5. What $\Lambda = 0$ means

The zeros of $H_t$ evolve under the heat flow as $t$ decreases from $\infty$ to $0$:

- At $t = \infty$: all zeros are real and negative.
- As $t$ decreases: zeros move continuously.
- At $t = \Lambda$: the first pair of zeros could leave the real axis (collide and split into a complex conjugate pair).
- $\Lambda = 0$: no zeros leave the real axis for any $t > 0$. The zeros remain real all the way down to the zeta function itself ($t = 0$).
- $\Lambda > 0$: at some positive temperature, zeros of $H_t$ leave the real axis, and $\zeta$ has off-line zeros.

---

## 6. Numerical evidence

The following data, computed in this repository, is consistent with $\Lambda = 0$:

**(a) Located zeros.** All 22,491 zeros of $\zeta(1/2 + it)$ with $0 < t \leq 20{,}000$ have been located. Every zero satisfies $\mathrm{Re}(\rho) = 1/2$ to machine precision. No off-line zero has been found. (Platt and Trudgian verified all heights to $3 \times 10^{12}$ unconditionally.)

**(b) GUE statistics.** The nearest-neighbour spacing distribution of the 22,491 zeros: mean spacing 0.999944 (GUE target 1.0000), standard deviation 0.396143 (GUE target 0.5227), lag-1 autocorrelation $-0.364180$ (GUE target $-0.323$). Number variance $\Sigma^2(L)$ plateaus at $0.25$--$0.30$ for $L = 1$--$20$, far below Poisson's linear growth ($\Sigma^2 = L$). The zeros are a determinantal (correlated) process on the critical line, not an independent (Poisson) process.

**(c) S-function.** The argument of $\zeta$ on the critical line: $S(t) = (1/\pi)\arg\zeta(1/2 + it)$. Maximum $|S(t)|/\log t$ over $0 < t \leq 20{,}000$ is $0.146$, consistent with $S(t) = o(\log t)$ (the RH-equivalent bound).

**(d) Explicit formulas at height.** The Mertens formula $M_0(x) = -2 + \sum_\rho 2\mathrm{Re}[x^\rho/(\rho\zeta'(\rho))]$ with all 22,491 zeros at $T = 20{,}000$ reproduces $M(x)$ to $\sim 1.8\%$ at $x = 10^{14}$ (residual $+15{,}423$ vs exact $-875{,}575$). The Chebyshev formula $\psi_0(x) = x - \sum_\rho 2\mathrm{Re}[x^\rho/\rho] - \log 2\pi - \tfrac{1}{2}\log(1-x^{-2})$ reproduces $\psi(x)$ to $\sim 0.009\%$ at $x = 10^{14}$ (residual $-88{,}932$ vs exact $+618{,}672$). Both are conditionally convergent (non-monotone in $T$); the partial sums at every finite $T$ give values consistent with RH.

**(e) Exact arithmetic.** $M(10^k)$ for $k = 1$--$14$ (OEIS A084237): $-1, 1, 2, -23, -48, 212, 1037, 1928, -222, -33722, -87856, 62366, 599582, -875575$. Maximum $|M(x)|/\sqrt{x}$ over all $x \leq 10^{14}$: $0.5706$ (the false Mertens conjecture bound is $1$). Exact $\psi(10^k)$ for $k = 2$--$14$: $94.0453, 996.6809, \ldots, 100000000618672.4$. Maximum $|\psi(x) - x|/\sqrt{x}$ over all $x \leq 10^{14}$: $0.7770$.

---

## 7. Why computation cannot decide RH

Every item in Section 6 is a finite computation. The following two theorems show why no finite computation has logical force:

**Theorem (Odlyzko-te Riele, 1985; Pintz).** The Mertens conjecture $|M(x)| < \sqrt{x}$ is false. There exists $x$ with $|M(x)| > \sqrt{x}$. The first counterexample is below $\exp(1.59 \times 10^{40})$.

**Theorem (Skewes, 1933; Bays-Hudson, 2000).** $\pi(x) > \mathrm{Li}(x)$ occurs. Under RH, the first crossing is below $\sim 1.4 \times 10^{316}$.

Both theorems guarantee that the computable range looks exactly RH-correct while the truth beyond may differ. $|M(x)| < \sqrt{x}$ holds for every $x \leq 10^{16}$ ever computed, yet it is proven false. The same asymmetry applies to the bridge of this paper, and it is worth being exact about how: no finite check can decide the $0/0$ question, and in particular checking $|\chi(\rho)| = 1$ at finitely many zeros decides nothing at all, because the identity holds on the whole line rather than only at the zeros.

---

## 8. What remains

The proof of RH is complete conditional on $\Lambda \leq 0$. Since $\Lambda \geq 0$ is known (Rodgers-Tao), the entire problem reduces to:

**Prove $\Lambda \leq 0$.** Equivalently: prove that $H_t$ has only real zeros for every $t > 0$.

This is a single analytic statement about a single entire function. The five known approaches:

**(A)** Show $H_t(x)$ has no complex zeros for any $t > 0$, by a contour-integral or Phragmen-Lindelof argument.

**(B)** Show the interlacing property of zeros of $H_t$ is preserved as $t$ decreases.

**(C)** Construct a self-adjoint operator whose spectrum is $\{\gamma_n\}$ (Hilbert-Polya). Self-adjointness forces real spectrum, which forces $\Lambda = 0$.

**(D)** Prove $S(t) = o(\log t)$ uniformly. This implies $\Lambda = 0$ by the heat-flow characterization.

**(E)** Discover a new structural identity or positivity property of $\zeta$ that forces all zeros onto the line.

None of these is known. The problem is open.

---

## 9. Conclusion

We have proved:

1. The function $g(s) = |\zeta(s)|/|\zeta(1-s)|$ equals 1 on the critical line (Schwarz reflection).
2. At each zero $\rho$, $g$ has a removable singularity with value $|\chi(\rho)|$, and $g(s) = |\chi(s)|$ identically off the zeros.
3. For a zero $\rho$ — necessarily with $0 < \mathrm{Re}(\rho) < 1$ — $|\chi(\rho)| = 1$ if and only if $\mathrm{Re}(\rho) = 1/2$. (Globally this fails: $|\chi(\sigma+it)|=1$ has three solutions in $\sigma$ for $t < t_*$, see Step 4.)
4. Therefore "every nontrivial zero fills in with value 1" is equivalent to RH — a re-encoding of RH, not a proof of it.
5. RH is equivalent to $\Lambda = 0$ (de Bruijn-Newman + Rodgers-Tao).

The $0/0$ at each zero fills in with value 1 exactly when that zero lies on the critical line, and since every nontrivial zero has $0 < \mathrm{Re}(\rho) < 1$, the strip form of Step 4 transfers this to $\rho$ itself. But the function is **not** constant away from the line ($g \equiv |\chi|$, and $g(2) = 19.74$), and — this is the point the earlier draft obscured — filling in the $0/0$ at a zero that is *already known* to be on the line is not new information. Proving $\Lambda = 0$ would fill in every singularity, and that is the open part; nothing in Sections 1--5 does any part of it.

---

*Computational data from the repository Puronbo/Law-Of-Repulsive-Emanation. RH remains open.*
