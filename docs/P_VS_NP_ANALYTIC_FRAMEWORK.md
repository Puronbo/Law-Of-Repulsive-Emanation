# Analytic Representations and the P vs NP Question

## Status and scope

P versus NP asks whether every decision problem whose proposed solutions can be verified in polynomial time can also be solved in polynomial time. It remains open. This note distinguishes a correct analytic encoding of satisfiability from the additional computational theorem needed to resolve the question.

The discussion uses 3-SAT because it is NP-complete. A polynomial-time algorithm for 3-SAT would imply \(P=NP\).

## 1. The exact counting object

For a 3-CNF formula \(\phi\) with \(N\) variables and \(M\) clauses, define

\[
Z_\phi=\#\mathrm{SAT}(\phi)
=\sum_{x\in\{0,1\}^N}\mathbf 1[\phi(x)\text{ is true}].
\]

Then

\[
\phi\in\mathrm{SAT}\iff Z_\phi>0.
\]

The normalized satisfying fraction is

\[
p_\phi=Z_\phi/2^N.
\]

It has the exact gap

\[
p_\phi=0\quad\text{for UNSAT},
\qquad
p_\phi\ge 2^{-N}\quad\text{for SAT}.
\]

## 2. Polynomial and contour encoding

Encode false by \(z_i=-1\) and true by \(z_i=1\). For every clause \(C\), let \(u_C(\mathbf z)\) be the product of the indicator polynomials for all literals of \(C\) being false. Define

\[
P_\phi(\mathbf z)=\prod_{C\in\phi}\bigl(1-u_C(\mathbf z)\bigr).
\]

At each Boolean point \(\boldsymbol\epsilon\in\{-1,1\}^N\),

\[
P_\phi(\boldsymbol\epsilon)=
\begin{cases}
1,&\boldsymbol\epsilon\text{ satisfies }\phi,\\
0,&\text{otherwise}.
\end{cases}
\]

Let \(C_0=\{z:|z|=2\}\), oriented counterclockwise. Since

\[
\frac{2z}{z^2-1}=\frac1{z-1}+\frac1{z+1},
\]

the residues at both \(z=1\) and \(z=-1\) are one. Successive applications of the residue theorem yield

\[
Z_\phi=
\frac{1}{(2\pi i)^N}
\oint_{C_0^N}
P_\phi(\mathbf z)
\prod_{i=1}^{N}\frac{2z_i}{z_i^2-1}\,d\mathbf z.
\]

This is an exact identity. Choosing another fixed complex center \(c\) merely translates the coordinates: \(w_i=z_i-c\). Therefore a fixed constant does not alter the computational complexity; \(c=0\) is the simplest choice.

For \(|z_i|>1\), the same identity has a constant-term form:

\[
Z_\phi=
\operatorname{CT}_{\mathbf z}
\left[
P_\phi(\mathbf z)
\prod_{i=1}^{N}\frac{2}{1-z_i^{-2}}
\right].
\]

## 3. What has been tested

The identity was checked with exact rational arithmetic in two independent forms: direct Boolean evaluation and constant-term extraction from the explicitly constructed polynomial.

- All 256 subsets of the eight full 3-literal clauses on three variables were checked.
- All 5,489 four-variable formulas containing at most three distinct 3-literal clauses were checked.
- Total exact checks: 5,745; no discrepancies.

A separate numerical contour experiment on a three-variable formula with \(Z_\phi=5\) converged to the correct value as nodes per contour increased. This validates the numerical implementation on a small instance, but is not a complexity proof.

## 4. Computational cost

Writing \(P_\phi\) in factored form takes polynomial size, roughly one small factor per clause. Exact evaluation may still be expensive:

| Method | Typical cost | Source of growth |
|---|---:|---|
| Direct residue/assignment sum | \(\Theta(M2^N)\) | \(2^N\) Boolean pole combinations |
| Tensor-product quadrature | \(\Theta(MK^N\,\operatorname{poly}(B))\) | \(K\) nodes on each of \(N\) contours |
| Full polynomial expansion | Potentially exponential | Exponentially many monomials/intermediate terms |
| Structured dynamic programming | \(\operatorname{poly}(n)2^{O(w)}\) | Width \(w\) of the interaction structure |

Here \(B\) is arithmetic precision in bits and \(w\) can be a treewidth-like parameter. A notation such as \(S=2^N\) only renames the state-space size; it does not make an \(O(S)\) algorithm polynomial in the formula length.

## 5. Certified lower and upper bounds

Suppose an algorithm produces a certified interval

\[
a_\phi\le Z_\phi\le b_\phi.
\]

For the integer count \(Z_\phi\),

\[
a_\phi>0\implies\text{SAT},
\qquad
b_\phi<1\implies\text{UNSAT}.
\]

Given a numerical estimate \(\widehat Z\) and a proven error bound \(\varepsilon\), a ReLU can express a valid lower bound:

\[
L=\operatorname{ReLU}(\operatorname{Re}(\widehat Z)-\varepsilon)
=\max(0,\operatorname{Re}(\widehat Z)-\varepsilon).
\]

If \(|\widehat Z-Z_\phi|\le\varepsilon\), then \(L\le Z_\phi\), and \(L>0\) proves SAT. ReLU does not create the error certificate; the hard work is obtaining \(\varepsilon\) efficiently and rigorously.

An epistemic presentation can use

\[
S=\min(1,a_\phi),
\qquad
U=\max(0,1-b_\phi),
\qquad
Q=1-S-U.
\]

Here \(S>0\) is certified SAT support, \(U>0\) is certified UNSAT support, and \(Q\) is unresolved uncertainty. The goal of a decision procedure is to make \(Q=0\) for every input in polynomial time.

## 6. Exact statement sufficient for P = NP

It would suffice to prove the following theorem.

> There exist a deterministic algorithm \(A\) and a constant \(k\) such that, for every 3-CNF formula \(\phi\) of length \(n\), \(A\) runs in at most \(n^k\) bit operations and returns a verifiable pair \((\widehat Z,\varepsilon)\) satisfying
>
> \[
> |\widehat Z-Z_\phi|\le\varepsilon<\tfrac12.
> \]

Rounding \(\widehat Z\) would then recover the integer \(Z_\phi\), deciding 3-SAT in polynomial time. NP-completeness of 3-SAT would give \(P=NP\).

The proof must account for all resources:

1. a standard finite-bit computational model;
2. polynomial preprocessing and representation size;
3. polynomial arithmetic precision and intermediate-value size;
4. a polynomial number of samples, states, or symbolic operations;
5. a checkable global error bound; and
6. correctness on every formula, including worst-case formulas with one satisfying assignment or none.

Fixed but noncomputable real constants cannot be used to hide oracle information. A legitimate constant must have a finite, efficiently usable description.

## 7. What would prove P != NP

To prove \(P\ne NP\), one must show that no polynomial-time algorithm decides 3-SAT on all instances:

\[
\forall k\in\mathbb N,\quad
\text{3-SAT}\notin\operatorname{DTIME}(n^k).
\]

Showing that direct residues, a particular quadrature rule, ReLU bounds, or one chosen epistemic representation take exponential time only rules out those methods. It does not rule out every polynomial-time algorithm.

A stronger sufficient target is a superpolynomial lower bound on the unrestricted Boolean circuit complexity of an NP language. This remains far beyond current lower-bound techniques.

## 8. Productive directions from this framework

The framework is most naturally connected to:

- multivariate residues and constant-term extraction;
- \(\#P\) and model counting;
- symbolic computation and certified numerical analysis;
- knowledge compilation, decision diagrams, and d-DNNF;
- parameterized complexity via treewidth, clause overlap, symmetry, and low-rank structure.

The useful research question is not whether a fixed contour center is special. It is:

\[
\text{Which structural invariant keeps the residual-state or constant-term representation small?}
\]

For instance families of bounded width, branch states can be merged into a representation of size exponential in width rather than in \(N\). For arbitrary formulas, no general polynomial-size compilation or merging theorem is known.

## 9. Common pitfalls

- A compact expression is not necessarily efficiently evaluable.
- A fractional power normally creates branch points, not residue poles.
- A fixed shift \(c\) is a coordinate transformation, not a source of computational power.
- Finite experiments validate implementations, not universal asymptotic claims.
- Changing binary notation to ternary does not change the \(2^N\) Boolean assignment count.
- A numerical estimate without a rigorous error certificate cannot decide SAT exactly.
- A lower bound for one algorithm is not a lower bound for all algorithms.

## References

1. Clay Mathematics Institute, “P vs NP.” https://www.claymath.org/millennium/p-vs-np/
2. Arora and Barak, *Computational Complexity: A Modern Approach*, draft materials. https://theory.cs.princeton.edu/complexity/
3. Capelli and Mengel, “Knowledge Compilation, Width and Quantification.” https://arxiv.org/abs/1807.04263
4. Samer and Szeider, “A Fixed-Parameter Algorithm for #SAT with Parameter Incidence Treewidth.” https://arxiv.org/abs/cs/0610174
5. Simons Institute, “Lower Bounds for Unrestricted Boolean Circuits: Open Problems.” https://simons.berkeley.edu/talks/lower-bounds-unrestricted-boolean-circuits-open-problems
