"""Tests for the Widder/Hankel H5 experiment.

``experiments/rh_widder_hankel_h5.py`` carries out record section 24's
"sharpest next calculation" -- fix ``x > 0`` and analyze the asymptotic spectrum
of ``q_rho(x)^m`` -- analytically rather than by scanning, because the object is
an exponential sum and exponential sums are decidable.  The sub-gates:

  H5a  OSCILLATION THEOREM.  If the maximal-modulus cluster is isolated and
       every phase in it is nonzero mod 2pi, then ``Re S(m) < 0`` for infinitely
       many ``m``.  Proof: ``f(m) = sum_j cos(m theta_j)`` is almost periodic,
       ``mean f = 0`` and ``mean f^2 > 0``; ``f >= 0`` eventually would force
       ``f == 0`` on the hull closure, contradicting the second moment.
  H5b  the ``|q|`` crossing is an exact quadratic, so record questions 1-2
       (who maximizes, is the maximizer isolated) are exact.
  H5c  ``|w|^2 = gamma^4 + 2 delta^2 gamma^2 + delta^4`` is strictly increasing
       in ``|delta|``, so displacement raises the modulus and the off-axis zero
       can only win in a bounded window.
  H5d  that window is nonempty for every displaced index but independent of
       ``delta``, which corrects a natural misreading of H4.
  H5e  an on-axis strict maximizer defeats the route entirely -- the real
       obstruction.

The failure-modes watched for here:

* **A vacuous gate.** No gate may assert ``True`` unconditionally; every gate
  detail must carry a recorded numeric claim.
* **The theorem's hypothesis is the whole point (H5e).** H5a is worthless if
  the "every phase nonzero" hypothesis is quietly satisfied by construction.  The
  tests pin the counterexample -- phases ``[0, 1.9]`` must produce ZERO negative
  orders -- so a future edit that drops the ``theta = 0`` branch fails loudly.
* **The grid-resolution trap (H5d).** Window endpoints are grid-sampled, so
  comparing ``delta = 1`` against ``delta <= 1e-2`` measures the log grid (a
  threshold between two samples snaps to whichever comes first) rather than the
  physics.  A first cut of this gate compared exactly those and failed for a
  reason that had nothing to do with the mathematics.  The test requires the
  delta-independence claim to be made in the asymptotic regime.
* **Scanning instead of solving (H5b).** The whole point is the closed form.  The
  test recomputes the roots and re-verifies them against direct evaluation, so a
  future edit cannot quietly replace the quadratic with a scan and still pass.
* **Honesty.** H5 must not claim to settle the bridge; it must name section 27
  as open and must state that the criterion may still be sufficient.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiments"))

import mpmath as mp  # noqa: E402

import regen_data  # noqa: E402
import rh_widder_hankel_h5 as h5  # noqa: E402


def _artifact():
    path = regen_data.find_data("rh_widder_hankel_h5_data.json")
    assert path is not None, "artifact missing; run the script"
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _gate(rep, prefix):
    hits = [g for g in rep["gates"]
            if g["gate"].split()[0].rstrip(":") == prefix]
    assert len(hits) == 1, "expected exactly one gate starting %r" % prefix
    return hits[0]


# ---------------------------------------------------------------- structure

def test_all_gates_pass():
    rep = _artifact()
    names = [g["gate"] for g in rep["gates"]]
    assert [n.split()[0].rstrip(":") for n in names] == \
        ["H5a", "H5b", "H5c", "H5d", "H5e"]
    assert all(g["passed"] for g in rep["gates"]), \
        "a gate stopped confirming its number: %s" % names


def test_no_gate_is_trivially_passing():
    rep = _artifact()
    for g in rep["gates"]:
        d = g["detail"]
        assert any(ch.isdigit() for ch in d), \
            "gate %r has no recorded number: %r" % (g["gate"], d)
        assert len(d) > 250, \
            "gate %r detail is too thin to be a real check" % g["gate"]


def test_conclusion_keeps_the_bridge_open():
    rep = _artifact()
    c = rep["conclusion"]
    assert "NOTHING HERE PROVES OR REFUTES RH" in c
    assert "remains OPEN" in c
    assert "may still be correct and sufficient" in c
    assert "THEOREM" in c


# ------------------------------------------------------------------- H5a

def test_cesaro_identities_are_exact():
    """mean cos^2 = 1/2 and mean cos(m a)cos(m b) = 0 for generic phases."""
    rep = _artifact()
    ident = rep["h5_cesaro"]["identities"]
    assert ident
    for r in ident:
        assert r["abs_err"] < 5e-3, \
            "Cesaro identity for %s off by %.2e (mean %r, want %r)" \
            % (r["case"], r["abs_err"], r["mean"], r["want"])
    assert abs(rep["h5_cesaro"]["mean_f_example"]) < 5e-3, \
        "mean f should vanish for a nonzero phase"


def test_oscillation_on_adversarial_configs():
    """The theorem must hold on the configurations most likely to defeat it."""
    rep = _artifact()
    rows = rep["h5_oscillation_rows"]
    assert len(rows) >= 8, "too few stress configurations"
    named = {r["config"] for r in rows}
    for want in ("conjugate pair", "theta, pi-theta", "theta, 2theta",
                 "all identical", "tiny phase", "dense 8-cluster"):
        assert want in named, "missing stress config %r" % want
    for r in rows:
        assert r["neg"] > 0, \
            "no sign change in %r -- the theorem is violated" % r["config"]
        assert r["pos"] > 0, \
            "no positive orders in %r; f should oscillate both ways" \
            % r["config"]


def test_oscillation_directly_recomputed():
    """Recompute a conjugate pair by hand rather than trusting the artifact."""
    th = [mp.mpf("0.9"), mp.mpf("-0.9")]
    neg = sum(1 for m in range(1, 20001)
              if mp.re(mp.fsum([mp.e ** (1j * m * t) for t in th])) < 0)
    assert neg > 1000, "conjugate pair gave only %d negative orders" % neg
    # For a pure pair, Re S(m) = 2 cos(m theta) exactly.
    for m in (1, 7, 100, 4321):
        direct = mp.re(mp.e ** (1j * m * th[0]) + mp.e ** (1j * m * th[1]))
        assert abs(direct - 2 * mp.cos(m * th[0])) < mp.mpf("1e-30")


# ------------------------------------------------------------------- H5b

def test_crossing_quadratic_matches_direct_evaluation():
    """The closed form, not a scan: re-verify every root against |q| directly."""
    worst = 0.0
    for k in (1, 2, 3):
        for dexp in (0, -2, -4):
            d = mp.mpf(10) ** dexp
            g = h5.GAMMAS[k]
            a = h5.GAMMAS[k - 1] ** 2
            xs = h5.crossings(g, d, a)
            assert xs, "no positive crossing for k=%d delta=%s" % (k, d)
            for x in xs:
                w = h5._w(g, d)
                r = abs(abs(h5._q(w, x)) - abs(h5._q(a, x)))
                worst = max(worst, float(r))
    assert worst < 1e-30, "worst crossing residual %.2e" % worst


def test_crossing_quadratic_coefficients_are_right():
    """Recompute the quadratic coefficients independently."""
    g, d, a = h5.GAMMAS[2], mp.mpf(1), h5.GAMMAS[1] ** 2
    w = h5._w(g, d)
    w2 = h5._absw_squared(g, d)
    W = mp.sqrt(w2)
    A = W - a
    B = 2 * a * (W - mp.re(w))
    C = a * a * W - a * w2
    # the defining equation is |w|(x+a)^2 - a|x+w|^2 = 0
    for x in (mp.mpf(1), mp.mpf(37), mp.mpf(5000)):
        lhs = W * (x + a) ** 2 - a * abs(x + w) ** 2
        assert abs((A * x * x + B * x + C) - lhs) < mp.mpf("1e-25") * abs(lhs) \
            + mp.mpf("1e-25"), "quadratic does not reproduce the equation"


def test_maximizer_is_isolated():
    rep = _artifact()
    for r in rep["h5_isolation"]:
        assert r["n_tied"] == 0, \
            "maximizer was tied at %d sampled x for index %d" \
            % (r["n_tied"], r["which"])
        assert r["n_isolated"] > 0


# ------------------------------------------------------------------- H5c

def test_displacement_raises_the_modulus():
    """Exactly |w|^2 = gamma^4 + 2 delta^2 gamma^2 + delta^4."""
    for g in h5.GAMMAS:
        for d in (mp.mpf("1e-3"), mp.mpf(1), mp.mpf("5")):
            assert abs(h5._absw_squared(g, d) - (g ** 4 + 2 * d * d * g ** 2
                                                 + d ** 4)) < mp.mpf("1e-30")
    # strictly increasing in |delta|
    for g in h5.GAMMAS:
        vals = [h5._absw_squared(g, mp.mpf(10) ** e)
                for e in (0, -2, -4, -6)]
        assert all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))


def test_modulus_excess_is_recorded_and_positive():
    rep = _artifact()
    for r in rep["h5_modulus_rows"]:
        assert r["excess_over_gamma4"][0] > 0, \
            "displacement failed to raise |w| at gamma=%r" % r["gamma"]
        assert all(e > 0 for e in r["excess_over_gamma4"])


# ------------------------------------------------------------------- H5d

def test_windows_are_nonempty_for_every_index():
    rep = _artifact()
    for rec in rep["h5_window_rows"]:
        assert any(b["n_win"] > 0 for b in rec["by_delta"]), \
            "displaced index %d is NEVER the maximizer" % rec["which"]


def test_delta_independence_is_asserted_in_the_asymptotic_regime():
    """The grid-resolution trap: delta = 1 vs delta <= 1e-2 compares against a
    log grid, not the physics."""
    rep = _artifact()
    assert rep["h5_small_delta_spread"] < 5e-3, \
        "window endpoints move by %.2e within the asymptotic regime" \
        % rep["h5_small_delta_spread"]
    lim = h5.H4_LINEAR_H5
    for rec in rep["h5_window_rows"]:
        small = [b for b in rec["by_delta"]
                 if mp.mpf(b["delta_exact"]) <= lim]
        assert len(small) >= 2, "no small-delta rows for index %d" % rec["which"]
        los = [b["x_lo"] for b in small if b["x_lo"] is not None]
        if len(los) >= 2:
            spread = (max(los) - min(los)) / (sum(los) / len(los))
            assert spread < 5e-3, \
                "index %d window moves %.2e across delta <= 1e-2" \
                % (rec["which"], spread)


def test_window_endpoints_differ_by_index():
    """Sanity: distinct indices must give distinct windows, else the gate is
    measuring something degenerate."""
    los = [rec["by_delta"][-1]["x_lo"] for rec in rep_window()]
    assert len(set(los)) == len(los), "all indices share one window: %s" % los


def rep_window():
    return _artifact()["h5_window_rows"]


# ------------------------------------------------------------------- H5e

def test_on_axis_phase_defeats_the_route():
    """THE counterweight to H5a.  With a theta = 0 dominant term there must be
    NO sign change, ever."""
    rep = _artifact()
    oa = rep["h5_onaxis"]
    assert oa["neg"] == 0, \
        "phases [0, 1.9] gave %d negative orders; the obstruction is gone" \
        % oa["neg"]
    assert oa["pos"] > 0
    assert oa["mean_f"] > 0.5, \
        "mean f should be ~1 for an on-axis phase, got %r" % oa["mean_f"]
    assert oa["min_margin"] >= 0, \
        "Re S(m) = 1 + cos(m theta) cannot be negative, margin %r" \
        % oa["min_margin"]


def test_on_axis_phase_defeat_recomputed():
    th = [mp.mpf(0), mp.mpf("1.9")]
    neg = 0
    for m in range(1, 20001):
        if mp.re(mp.fsum([mp.e ** (1j * m * t) for t in th])) < 0:
            neg += 1
    assert neg == 0, "on-axis phase gave %d negative orders" % neg
    # and the margin is nonneg by inspection
    for m in range(1, 5001):
        assert 1 + mp.cos(m * th[1]) >= -mp.mpf("1e-30")


def test_off_axis_pair_still_violates():
    """Control: without the on-axis term the theorem's hypothesis holds and the
    sign change returns."""
    Qm, th = mp.mpf(2), mp.mpf("0.7")
    qs = [Qm * mp.e ** (1j * th), Qm * mp.e ** (-1j * th)] + \
        [mp.mpf(j) / 20 for j in range(1, 8)]
    mf = None
    for m in range(1, 401):
        if mp.re(mp.fsum([v ** m for v in qs])) < 0:
            mf = m
            break
    assert mf is not None and mf <= 12, "control pair gave m_first=%r" % mf


def test_w_is_the_transformed_scale():
    for d in (mp.mpf("0.1"), mp.mpf(1), mp.mpf("2.5")):
        g = h5.GAMMAS[1]
        expect = -(d + 1j * g) ** 2
        assert abs(h5._w(g, d) - expect) < 1e-25 * abs(expect)
    for g in h5.GAMMAS:
        assert h5._w(g, mp.mpf(0)) == g * g
        assert mp.im(h5._w(g, mp.mpf(0))) == 0
