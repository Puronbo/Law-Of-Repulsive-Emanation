#!/usr/bin/env python3
"""
Linear spectral-stability harness: domain scan, twin eigensolvers, numerical abscissa
=====================================================================================

A small, dependency-light toolkit packaging the four numerical primitives that
``Linear Stability of Candidate Swirl Profiles.md`` validated -- and whose
failure modes that note paid for:

1. a matrix-free operator interface plus a sparse Arnoldi leading eigenvalue
   (``scipy.sparse.linalg.eigs``), checked for grid convergence;
2. an independent dense eigendecomposition used as a cross-check on interior
   degrees of freedom (boundary values padded, never carried as formal
   unknowns) -- the two-solver discipline whose shared blind spot the note's
   Critical Self-Assessment exposed;
3. the numerical abscissa ``omega(A) = lambda_max((A + A^T)/2)`` for non-normal
   transient growth -- the Extension-VI signature that a negative spectrum does
   not bound instantaneous growth;
4. a domain-size scan with convergence tracking -- the check that caught the
   40--90% box-truncation underestimates of the original note.

Every primitive is exercised against a KNOWN-ANSWER operator, the 1-D Dirichlet
diffusion operator, whose finite-difference spectrum is closed-form::

    lambda_k = -(4 nu / h^2) sin^2( k pi / (2 (n+1)) ),   k = 1..n

so the two eigensolvers are verified against an exact formula before they are
trusted on any caller-supplied operator. Adding a first-order upwind advection
term makes the operator non-normal, which turns the abscissa/eigenvalue gap into
a genuine quantity (the possible-transient-growth indicator) rather than zero.

Honesty: this is a QA tool. It reports eigenvalues, abscissas and convergence
data. It does not certify the stability of any real flow, and it makes no claim
about the Navier--Stokes Millennium problem.

Author: Michael Grafiel S Puno
"""

from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import LinearOperator, eigs

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


# --------------------------------------------------------------------------
# Operator interface
# --------------------------------------------------------------------------
class MatrixFreeOperator:
    """A square operator acting on a flat vector of length ``n``.

    Subclasses assign ``self.n`` and implement :meth:`apply` (one matvec).
    ``to_dense`` builds the full matrix by applying the operator to every basis
    vector -- the same "independent implementation" used by the note's dense
    cross-check.
    """

    n = None  # set by subclasses in __init__

    def apply(self, x):  # pragma: no cover - interface
        raise NotImplementedError

    def to_dense(self, dtype=float):
        n = self.n
        cols = []
        for j in range(n):
            e = np.zeros(n, dtype=dtype)
            e[j] = 1.0
            cols.append(np.asarray(self.apply(e), dtype=dtype))
        return np.column_stack(cols)


class DirichletDiffusion1D(MatrixFreeOperator):
    """``nu * d^2/dx^2`` on ``(0, L)`` with homogeneous Dirichlet BCs,
    second-order finite differences.

    The interior unknowns sit at ``x_i = i h``, ``i = 1..n``, with
    ``h = L / (n + 1)``.  An optional nilpotent one-directional coupling term
    ``couple`` (a pure "shift-up" that is strictly triangular, hence has
    spectrum {0}) makes the operator non-normal; the default ``couple = 0`` is
    self-adjoint and negative definite.
    """

    def __init__(self, n_interior, L=1.0, nu=1.0, couple=0.0):
        self.n = int(n_interior)
        self.L = float(L)
        self.nu = float(nu)
        self.couple = float(couple)
        self.h = self.L / (self.n + 1)

    def apply(self, x):
        x = np.asarray(x, dtype=float)
        n, h, nu = self.n, self.h, self.nu
        xm = np.concatenate(([0.0], x[:-1]))
        xp = np.concatenate((x[1:], [0.0]))
        lap = (xm - 2.0 * x + xp) / (h * h)
        out = nu * lap
        if self.couple != 0.0:
            y = np.empty(n)
            y[0] = 0.0
            y[1:] = x[:-1]
            out = out + self.couple * y
        return out

    def closed_form_spectrum(self):
        """Exact FD eigenvalues of the self-adjoint diffusion operator
        (``couple = 0``): ``lambda_k = -(4 nu / h^2) sin^2(k pi / (2(n+1)))``."""
        if self.couple != 0.0:
            raise ValueError("closed form is only for the symmetric (couple = 0) case")
        k = np.arange(1, self.n + 1)
        return -(4.0 * self.nu / (self.h * self.h)) * np.sin(
            k * np.pi / (2.0 * (self.n + 1))
        ) ** 2


# --------------------------------------------------------------------------
# Eigensolvers (two independent implementations)
# --------------------------------------------------------------------------
def leading_eigenvalues_arnoldi(op, k=1):
    """Matrix-free Arnoldi: ``k`` eigenvalues of largest real part, sorted."""
    linop = LinearOperator((op.n, op.n), matvec=op.apply, dtype=float)
    vals = eigs(linop, k=k, which="LR", return_eigenvectors=False)
    return vals[np.argsort(-vals.real)]


def spectrum_dense(op):
    """Independent dense eigendecomposition (full spectrum, sorted by real part)."""
    vals = np.linalg.eigvals(op.to_dense())
    return vals[np.argsort(-vals.real)]


def numerical_abscissa(op):
    """``omega(A) = lambda_max((A + A^T)/2)``: the sharp instantaneous growth
    rate in the Euclidean inner product.  For a self-adjoint negative-definite
    operator it equals the spectral abscissa; for a non-normal operator it can
    exceed it, which is possible transient growth despite a stable spectrum."""
    A = op.to_dense()
    S = 0.5 * (A + A.T)
    return float(np.linalg.eigvalsh(S)[-1])


def domain_scan(op_factory, Ls, use_arnoldi=True):
    """Leading eigenvalue versus domain size, with successive increments.

    Reproduces the note's domain-convergence discipline: the operator is rebuilt
    on each box size and the leading eigenvalue tracked until the increments
    shrink.  Returns ``(Ls, leading, increments)``.
    """
    leading = []
    for L in Ls:
        op = op_factory(L)
        solver = leading_eigenvalues_arnoldi if use_arnoldi else spectrum_dense
        leading.append(float(np.real(solver(op, k=1)[0]) if use_arnoldi else np.real(solver(op)[0])))
    leading = np.asarray(leading)
    increments = np.abs(np.diff(leading))
    return list(Ls), leading, increments


# --------------------------------------------------------------------------
# Default self-check suite (known-answer operator)
# --------------------------------------------------------------------------
def run_checks(n_interior=24, L=np.pi, nu=1.0, couple=3.0,
               Ls=(2.0, 4.0, 8.0, 16.0, 32.0)):
    """Exercise all four primitives on known-answer operators; return a report.

    Every assertion below has an exact reference:
      * the diffusion spectrum has a closed form (Arnoldi and dense both check);
      * the self-adjoint abscissa must equal the spectral abscissa (gap 0);
      * the coupled operator is non-normal, so its abscissa must exceed its
        spectral abscissa (the transient-growth gap);
      * the domain scan must show shrinking increments.
    """
    report = {"verdict": "PASS", "checks": {}}

    def check(name, ok, detail):
        report["checks"][name] = {"ok": bool(ok), "detail": detail}
        if not ok:
            report["verdict"] = "FAIL"

    # --- 1. known-answer spectrum: Arnoldi vs dense vs closed form -----------
    op = DirichletDiffusion1D(n_interior, L=L, nu=nu)
    lam_arn = leading_eigenvalues_arnoldi(op, k=1)
    dense = spectrum_dense(op)
    closed = np.sort(op.closed_form_spectrum())[::-1]

    rel_arn = abs(lam_arn[0].real - closed[0]) / abs(closed[0])
    check("arnoldi_matches_closed_form", rel_arn < 1e-8,
          {"arnoldi": float(lam_arn[0].real), "closed_form": float(closed[0]),
           "rel_err": float(rel_arn)})

    # full-spectrum dense check against the closed form (same size -> same k)
    rel_dense = np.max(np.abs(dense.real - closed) / np.abs(closed))
    check("dense_matches_closed_form", rel_dense < 1e-8,
          {"max_rel_err": float(rel_dense), "n": int(op.n)})

    # --- 2. self-adjoint abscissa == spectral abscissa (gap 0) ---------------
    ab_sym = numerical_abscissa(op)
    gap_sym = abs(ab_sym - closed[0])
    check("self_adjoint_abscissa_equals_spectrum", gap_sym < 1e-8,
          {"abscissa": float(ab_sym), "spectral_abscissa": float(closed[0]),
           "gap": float(gap_sym)})

    # --- 3. non-normal operator: abscissa > spectral abscissa ----------------
    op_nn = DirichletDiffusion1D(n_interior, L=L, nu=nu, couple=couple)
    spec_nn = float(np.real(spectrum_dense(op_nn)[0]))
    ab_nn = numerical_abscissa(op_nn)
    gap_nn = ab_nn - spec_nn
    check("nonnormal_abscissa_exceeds_spectrum", gap_nn > 1e-6,
          {"abscissa": float(ab_nn), "spectral_abscissa": spec_nn,
           "transient_growth_gap": float(gap_nn), "couple": float(couple)})

    # --- 4. domain scan: increments shrink ----------------------------------- #
    def factory(Lbox):
        # fixed grid spacing h = 1/16, interior count grows with the box
        return DirichletDiffusion1D(int(round(Lbox * 16)) - 1, L=Lbox, nu=nu)

    boxes, leading, increments = domain_scan(factory, list(Ls))
    increasing = bool(np.all(np.diff(leading) >= -1e-12))
    # increments shrink toward the continuum limit
    shrink = bool(increments[-1] < increments[0]) if len(increments) > 1 else False
    check("domain_scan_tracks_and_converges", increasing and shrink,
          {"boxes": [float(b) for b in boxes],
           "leading": [float(v) for v in leading],
           "increments": [float(v) for v in increments],
           "increasing": increasing, "increments_shrink": shrink})

    report["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Linear spectral-stability harness")
    parser.add_argument("--n", type=int, default=24, help="interior grid points")
    parser.add_argument("--L", type=float, default=float(np.pi), help="domain length")
    parser.add_argument("--nu", type=float, default=1.0, help="diffusivity")
    parser.add_argument("--couple", type=float, default=3.0,
                        help="nilpotent one-directional coupling (non-normality)")
    parser.add_argument("--json", action="store_true", help="write artifact JSON")
    args = parser.parse_args(argv)

    report = run_checks(n_interior=args.n, L=args.L, nu=args.nu, couple=args.couple)

    print("=" * 68)
    print("  Linear spectral-stability harness -- known-answer self-checks")
    print("=" * 68)
    for name, rec in report["checks"].items():
        mark = "PASS" if rec["ok"] else "FAIL"
        print("  [%s] %s" % (mark, name))
        print("         %s" % rec["detail"])
    print("-" * 68)
    print("  OVERALL: %s" % report["verdict"])
    print("=" * 68)

    if args.json:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        path = os.path.join(OUTPUT_DIR, "stability_harness.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, default=str)
        print("  artifact: %s" % path)

    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
