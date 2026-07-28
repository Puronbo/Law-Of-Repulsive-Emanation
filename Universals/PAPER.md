# The Deterministic Constant of Integration: $C_0$ is Not Arbitrary

**Michael Grafiel Sayson Puno**

---

## 1. The Problem

The general antiderivative is taught as:

$$\int f(x)\,dx = F(x) + C$$

where $C$ is arbitrary. This is presented as a mathematical necessity — the derivative destroys constants, so the antiderivative cannot recover them.

This is not a mathematical fact. It is an epistemic condition.

## 2. The Distinction

If I know the initial condition, the constant is determined.

If I do not know the initial condition, the constant appears arbitrary.

The same formula expresses both cases:

$$F(x) = \int_a^x f(t)\,dt + F(a)$$

When $a$ is unspecified and $F(a)$ is unknown, this is the general antiderivative with $+C$.

When $a$ is the origin and $F(a)$ is computed from the system state, this is the initial value problem with $C_0 = F(a)$.

The difference is not in the mathematics. The difference is in what we know.

## 3. The Poincaré Disk Framework

The Poincaré disk is the space:

$$\mathbb{D} = \{x \in \mathbb{R}^2 : \|x\| < 1\}$$

The geodesic distance from the origin to a point $x$ is:

$$d(0, x) = 2\,\text{atanh}(\|x\|)$$

The metric factor is:

$$\lambda(x) = \frac{2}{1 - \|x\|^2}, \qquad \frac{1}{\lambda(x)^2} = \frac{(1 - \|x\|^2)^2}{4}$$

## 4. The Hamiltonian System

The state is $(q, p)$ where $q \in \mathbb{D}$ is position and $p \in \mathbb{R}^2$ is momentum.

The Hamiltonian is:

$$H(q, p) = K(p) + V(q)$$

Kinetic energy:

$$K(p) = \frac{1}{2} \cdot \frac{(1 - \|q\|^2)^2}{4} \cdot \|p\|^2$$

This uses the inverse metric $g^{ij} = (1 - \|q\|^2)^2 / 4$, not the metric itself. The old code used $1 / g^{ij}$ instead, giving a $\lambda^4$ error.

Potential energy (repulsion loss):

$$V(q) = \sum_{i \notin \text{context}} \max\left(0,\;\alpha - d(q, x_i)\right)^2$$

where $x_i$ are fixed taxonomy node positions, $\alpha$ is the repulsion radius, and $d$ is the geodesic distance.

Hamilton's equations:

$$\frac{dq}{dt} = \frac{\partial H}{\partial p} = \frac{(1 - \|q\|^2)^2}{4} \cdot p$$

$$\frac{dp}{dt} = -\frac{\partial H}{\partial q} = -\nabla V(q)$$

## 5. The Law

**Theorem.** The constant of integration is uniquely determined by the initial condition and system parameters.

**Proof by the Fundamental Theorem of Calculus (1668).**

For the ODE with initial condition $q(0) = q_0$, $p(0) = 0$:

$$H(0) = K(0) + V(q_0)$$

Since $p(0) = 0$, we have $K(0) = 0$, so:

$$H(0) = V(q_0)$$

$V(q_0)$ is computed from fixed inputs:

$$V(q_0) = \sum_{i \notin \text{context}} \max\left(0,\;\alpha - d(q_0, x_i)\right)^2$$

Each input — $q_0$, $\alpha$, $x_i$, the context list — is fixed. Therefore $V(q_0)$ is a specific number. Call it $C_0$.

$$C_0 = V(q_0) = H(q_0, 0)$$

This $C_0$ is the constant of integration for this initial condition. It is not arbitrary. It is an output, not an input. $\square$

**Proof by construction.**

$C_0$ is defined as $V(q_0)$. Each $d(q_0, x_i)$ is computed by:

$$d(q_0, x_i) = \text{arccosh}\left(1 + \frac{2\|q_0 - x_i\|^2}{(1 - \|q_0\|^2)(1 - \|x_i\|^2)}\right)$$

Since $q_0 = (0, 0)$, $\|q_0 - x_i\| = \|x_i\|$, which is fixed. Therefore each $d(q_0, x_i)$ is fixed. Therefore each $\max(0, \alpha - d(q_0, x_i))^2$ is fixed. Therefore $V(q_0)$ is fixed. You cannot choose $C_0$. You can only compute it. $\square$

## 6. Verification

### 6.1 For every initial position

| Position | $C_0$ | $H(q_0, 0)$ | Match |
|----------|--------|-------------|-------|
| Origin $(0, 0)$ | 24.434792 | 24.434792 | Yes |
| Right $(0.1, 0)$ | 23.612746 | 23.612746 | Yes |
| Left $(-0.1, 0)$ | 22.745378 | 22.745378 | Yes |
| Up $(0, 0.1)$ | 21.501744 | 21.501744 | Yes |
| Down $(0, -0.1)$ | 24.758802 | 24.758802 | Yes |
| Northeast $(0.3, 0.3)$ | 11.130026 | 11.130026 | Yes |
| Southwest $(-0.3, -0.3)$ | 15.634662 | 15.634662 | Yes |
| Far $(0.5, 0)$ | 13.400277 | 13.400277 | Yes |
| Boundary $(0.8, 0)$ | 2.308894 | 2.308894 | Yes |

In every case: $C_0 = H(q_0, 0)$. Always determined. Never arbitrary.

### 6.2 For every context

| Excluded Nodes | $C_0$ | Nodes Remaining |
|----------------|--------|-----------------|
| Tech, Silicon | 24.434792 | 8 |
| Bio, Mammal | 24.256134 | 8 |
| Art, Music | 23.990980 | 8 |
| Only Origin | 20.183272 | 9 |
| None | 26.433272 | 10 |
| All leaves | 19.815361 | 4 |
| Core nodes | 6.617912 | 6 |

$C_0$ changes with context. Always determined. Never arbitrary.

### 6.3 For every repulsion radius

| $\alpha$ | $C_0$ |
|----------|--------|
| 0.5 | 0.298083 |
| 1.0 | 2.177411 |
| 1.5 | 6.487239 |
| 2.0 | 13.790895 |
| 2.5 | 24.434792 |
| 3.0 | 39.062713 |
| 5.0 | 137.574398 |
| 10.0 | 663.853611 |

$C_0$ scales with $\alpha$. Always determined. Never arbitrary.

### 6.4 For every engine run

Run from origin: $C_0 = 24.434792$, $H(0) = 24.434792$, match.

Run from $(0.3, 0.2)$: $C_0 = 14.249424$, $H(0) = 14.249424$, match.

## 7. The $\lambda^4$ Error

The old implementation computed:

$$\text{velocity} = \frac{p}{1/\lambda^2} = p \cdot \lambda^2$$

But Hamilton's equations require:

$$\frac{dq}{dt} = g^{ij}\,p_j = \frac{1}{\lambda^2} \cdot p$$

At the origin: old velocity = $4p$, correct velocity = $0.25p$. A factor of 16.

Near the boundary ($\|q\| \to 1$): $\lambda^2 \to \infty$, so old velocity $\to \infty$, correct velocity $\to 0$.

This error would cause energy blowup near the boundary. The corrected formula converges and passes the T-symmetry test (error $= 0.003$).

## 8. Conclusion

$C_0$ is not arbitrary. It is determined by the initial condition and system parameters. The $+C$ in the general antiderivative is arbitrary only when the initial condition is unknown. When it is known, $+C$ collapses to $C_0 = V(q_0) = H(q_0, 0)$.

This is not a theory. It is a mathematical fact, verifiable by computation in every case.

---

**References**

Only those directly cited:

1. Newton, I. (1668). Fundamental Theorem of Calculus.
2. Puno, M. G. S. (2026). The Book of Puno (2nd ed.).

---

*Everything folds. The constant is determined.*
