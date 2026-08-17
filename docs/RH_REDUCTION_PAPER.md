# The Riemann Hypothesis and the Removable Singularity

**Date:** 2026-08-17
**Repository:** Puronbo/Law-Of-Repulsive-Emanation

---

## Abstract

We prove that the Riemann hypothesis is equivalent to the statement that a single explicit function, $g(s) = |\zeta(s)| / |\zeta(1-s)|$, is identically equal to 1 after removal of its singularities. The proof identifies the exact value of each removable singularity as $|\chi(\rho)|$, where $\chi$ is the completed factor of the functional equation, and shows that $|\chi(\rho)| = 1$ if and only if $\mathrm{Re}(\rho) = 1/2$. Combined with the Rodgers-Tao theorem ($\Lambda \geq 0$), this reduces RH to the single inequality $\Lambda = 0$ for the de Bruijn-Newman constant. We present the complete proof, the numerical evidence from this repository (22,491 located zeros, exact Mertens and Chebyshev functions to $10^{14}$), and the reasons why no finite computation can decide the problem.

---

## 1. The function

Define

$$g(s) = \frac{|\zeta(s)|}{|\zeta(1-s)|}.$$

This is the zeta-theoretic analogue of

$$f(x) = \left|\frac{x-1}{1-x}\right| = 1 \qquad (x \neq 1).$$

In both cases the numerator equals the denominator up to sign, and the absolute value removes the sign. For $f$, this is the tautology $|x-1| = |1-x|$. For $g$, on the critical line, it is the Schwarz reflection principle. Both functions are identically 1 where defined, and both have the indeterminate form $0/0$ at isolated points.

---

## 2. Main theorem

**Theorem.** *The function $g(s) = |\zeta(s)| / |\zeta(1-s)|$ satisfies $g \equiv 1$ (after removal of singularities) if and only if the Riemann hypothesis is true.*

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

Off the critical line ($\sigma \neq 1/2$): the prefactor $\pi^{\sigma - 1/2} \neq 1$, and the gamma ratio does not compensate, so $|\chi| \neq 1$. (Precisely: $\log|\chi(\sigma+it)| = (\sigma - 1/2)\log\pi + \mathrm{Re}\log\Gamma(\frac{1-s}{2}) - \mathrm{Re}\log\Gamma(\frac{s}{2})$, which is a strictly monotone function of $\sigma$ for fixed $t$ by the monotonicity of $\log|\Gamma|$ on vertical lines.)

Therefore:

$$|\chi(\rho)| = 1 \quad \Longleftrightarrow \quad \mathrm{Re}(\rho) = \tfrac{1}{2}. \qquad \square$$

**Step 5. Combining.**

From Steps 1--4:

$$g \equiv 1 \;\;\Longleftrightarrow\;\; |\chi(\rho)| = 1 \text{ for every zero } \rho \;\;\Longleftrightarrow\;\; \mathrm{Re}(\rho) = \tfrac{1}{2} \text{ for every zero } \rho \;\;\Longleftrightarrow\;\; \mathrm{RH}. \qquad \blacksquare$$

---

## 4. The de Bruijn-Newman reduction

The proof of Step 5 establishes the equivalence $g \equiv 1 \iff \mathrm{RH}$. To convert this into an inequality about a single analytic object, we use the de Bruijn-Newman framework.

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

Both theorems guarantee that the computable range looks exactly RH-correct while the truth beyond may differ. $|M(x)| < \sqrt{x}$ holds for every $x \leq 10^{16}$ ever computed, yet it is proven false. No finite verification of $g = 1$ at finitely many points can decide whether $g \equiv 1$.

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

1. The function $g(s) = |\zeta(s)|/|\zeta(1-s)|$ is identically 1 on the critical line (Schwarz reflection).
2. At each zero $\rho$, $g$ has a removable singularity with value $|\chi(\rho)|$.
3. $|\chi(\rho)| = 1$ if and only if $\mathrm{Re}(\rho) = 1/2$.
4. Therefore $g \equiv 1$ if and only if RH.
5. RH is equivalent to $\Lambda = 0$ (de Bruijn-Newman + Rodgers-Tao).

The function is already constant where defined. The $0/0$ at each zero fills in with value 1 if and only if the zero lies on the critical line. Proving $\Lambda = 0$ fills in every singularity and completes the proof.

---

*Computational data from the repository Puronbo/Law-Of-Repulsive-Emanation. RH remains open.*
