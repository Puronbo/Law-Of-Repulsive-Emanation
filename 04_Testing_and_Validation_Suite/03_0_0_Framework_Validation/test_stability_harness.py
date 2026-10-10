"""Regression tests for experiments/stability_harness.py.

The harness packages the four numerical primitives validated on the reduced
(u1, omega1) swirl system (``Linear Stability of Candidate Swirl Profiles.md``):
matrix-free Arnoldi, an independent dense eigendecomposition, the numerical
abscissa for non-normal transient growth, and the domain-size convergence scan
that caught the note's 40-90% box-truncation underestimates.

Pinned here, against a KNOWN-ANSWER operator whose finite-difference spectrum is
closed-form (``lambda_k = -(4 nu/h^2) sin^2(k pi/(2(n+1)))``):

  * both eigensolvers agree with the closed form to ~1e-14 (twin-method)
  * the self-adjoint abscissa equals the spectral abscissa (gap 0)
  * the nilpotently-coupled (non-normal) operator shows abscissa > spectrum
  * the domain scan is monotone with shrinking increments
  * the default self-check suite reports OVERALL PASS

No claim about real-flow stability or the Navier-Stokes Millennium problem is
made or pinned here.
"""

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "02_Experimental_Implementations_and_Verification"))

import numpy as np  # noqa: E402

import experiments.stability_harness as sh  # noqa: E402


@pytest.fixture(scope="module")
def base_op():
    return sh.DirichletDiffusion1D(24, L=np.pi, nu=1.0)


def test_arnoldi_matches_closed_form(base_op):
    closed = np.sort(base_op.closed_form_spectrum())[::-1]
    lam = sh.leading_eigenvalues_arnoldi(base_op, k=1)
    rel = abs(lam[0].real - closed[0]) / abs(closed[0])
    assert rel < 1e-8


def test_dense_matches_closed_form(base_op):
    closed = np.sort(base_op.closed_form_spectrum())[::-1]
    dense = sh.spectrum_dense(base_op)
    rel = np.max(np.abs(dense.real - closed) / np.abs(closed))
    assert rel < 1e-8


def test_self_adjoint_abscissa_equals_spectrum(base_op):
    closed = np.sort(base_op.closed_form_spectrum())[::-1]
    ab = sh.numerical_abscissa(base_op)
    assert abs(ab - closed[0]) < 1e-8


def test_nonnormal_abscissa_gap_positive():
    op = sh.DirichletDiffusion1D(24, L=np.pi, nu=1.0, couple=3.0)
    spec = float(np.real(sh.spectrum_dense(op)[0]))
    ab = sh.numerical_abscissa(op)
    assert ab > spec + 1e-6


def test_domain_scan_increments_shrink():
    def factory(Lbox):
        return sh.DirichletDiffusion1D(int(round(Lbox * 16)) - 1, L=Lbox, nu=1.0)

    boxes, leading, increments = sh.domain_scan(factory, [2.0, 4.0, 8.0, 16.0, 32.0])
    assert np.all(np.diff(leading) >= -1e-12)
    assert increments[-1] < increments[0]


def test_run_checks_verdict_pass():
    report = sh.run_checks()
    assert report["verdict"] == "PASS"
    assert len(report["checks"]) == 5
    assert all(rec["ok"] for rec in report["checks"].values())