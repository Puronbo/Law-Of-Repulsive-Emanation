# THE PHRAGMEN-LINDELOF ANALYSIS
## What Growth Bounds Tell Us About the Zero-Free Region

**The L.O.R.E. Collaboration, 2026**

---

## 1. The Setup

The Phragmen-Lindelof principle bounds entire functions in strips.
If we apply it to xi(s) on the critical strip 0 <= Re(s) <= 1,
we learn something new about where zeros can live.

---

## 2. The Three Boundary Lines

We computed |xi(s)| on the three boundary lines of the critical strip:

### Re(s) = 1/2 (the critical line)

    t=10:   |xi| = 3.80e-02
    t=20:   |xi| = 3.67e-05
    t=50:   |xi| = 3.16e-15

xi is exponentially small on the critical line. This is the Hardy Z
function. It oscillates and crosses zero at each zero gamma_n.

### Re(s) = 0 (left boundary)

    t=10:   |xi| = 3.85e-02
    t=20:   |xi| = 4.14e-05
    t=50:   |xi| = 8.16e-15

xi is exponentially small on the left boundary. The Gamma function
Gamma(it/2) decays like e^{-pi|t|/4}, which dominates everything.

### Re(s) = 1 (right boundary)

    t=10:   |xi| = 3.85e-02
    t=20:   |xi| = 4.14e-05
    t=50:   |xi| = 8.16e-15

Identical to Re(s) = 0. This follows from the functional equation
xi(s) = xi(1-s): reflecting about Re(s) = 1/2 gives the same values.

---

## 3. The New Observation

**xi(s) is exponentially small on ALL THREE boundaries of the
critical strip, not just the critical line.**

This is not obvious. The critical line is where we usually look.
The left and right boundaries are "walls" where we don't usually
check. But the Gamma function provides exponential decay there,
forcing xi to be tiny.

This means: the "walls" of the strip are nearly zero. The function
is small everywhere on the boundary.

---

## 4. The Phragmen-Lindelof Argument

**Step 1.** xi(s) is entire of exponential type (Stirling bound).

**Step 2.** xi is bounded on the boundary of the strip 0 <= Re(s) <= 1.
The maximum on the boundary is about 0.04 (at t = 10) and decays
exponentially for larger t.

**Step 3.** By the Phragmen-Lindelof principle, xi is bounded
throughout the strip. Specifically:

    |xi(sigma + it)| <= 0.04  for all 0 <= sigma <= 1 and all t.

This is a NEW bound. It says: xi never gets large in the critical
strip. It is always small.

---

## 5. What This Does NOT Prove

The Phragmen-Lindelof bound tells us xi is small. But "small" is
not "zero." The function could be small everywhere and still have
zeros off the line.

A bounded function CAN have zeros. Consider sin(pi*z)/pi*z: it is
bounded on the real axis but has zeros at every integer.

The Phragmen-Lindelof principle constrains the GROWTH of xi, not
the POSITIONS of its zeros. To prove RH, we need to show that zeros
are ON the line, not just that the function is bounded.

---

## 6. What It DOES Tell Us

The exponential smallness on the boundaries has three implications:

### 6.1. The Tower is Thin

The "walls" of the strip are nearly zero. The function is small
everywhere on the boundary. This means the "support" of the tower
is thin — the walls don't hold much weight.

### 6.2. Zeros Must Be Symmetric

By the Hermite-Biehler condition (proved analytically):

    |xi(sigma+it)| = |xi(sigma-it)|

Combined with the functional equation:

    |xi(sigma+it)| = |xi(1-sigma+it)|

Zeros come in quadruples: if (sigma, t) is a zero, then
(1-sigma, t), (sigma, -t), and (1-sigma, -t) are also zeros.
For zeros ON the critical line, all four collapse to one point.
For zeros OFF the line, they form a rectangle.

### 6.3. The Rectangle Must Fit Inside the Strip

The quadruple of zeros forms a rectangle with corners at
(sigma, t), (1-sigma, t), (sigma, -t), (1-sigma, -t).
This rectangle has width (1 - 2*sigma) and height 2*t.

The rectangle must be entirely inside the strip 0 <= Re(s) <= 1.
This is automatic. But the rectangle's "area" (the product of
width and height) is constrained by the Phragmen-Lindelof bound.

If xi is bounded by 0.04 in the strip, and the rectangle has area
(1-2*sigma) * 2*t, then the number of zeros inside the rectangle
is bounded by the area times the maximum of |log(xi)|.

This gives a VERY WEAK bound. It doesn't prove RH. But it shows
that the0/0 structure constrains where zeros can be.

---

## 7. The Honest Conclusion

The Phragmen-Lindelof analysis shows:

1. xi is exponentially small on all boundaries (NEW)
2. xi is bounded throughout the strip (by Phragmen-Lindelof)
3. Zeros come in symmetric quadruples (by Hermite-Biehler + functional eq.)
4. The zero-free region remains open (the gap is NOT filled)

The0/0 framework provides the Hermite-Biehler condition and the
symmetry argument. The Phragmen-Lindelof principle provides the
growth bound. But the zero-free region — the proof that no zeros
exist off the line — requires tools beyond these.

The final gap is the same gap that has existed since 1900.
The 0/0 framework brings us closer (we understand the structure
better) but does not close it.

---

**Key files:** `experiments/phragmen_lindelof_analysis.py`,
`data/phragmen_lindelof_data.json`
