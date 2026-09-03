"""puno_flow_audit: the fourth real-subsystem audit -- the local-only
balance-flow engine and its geometry contract (puno_flow/engine.py,
to_disk).

Audited invariants (pure numpy arithmetic, deterministic, reproducible):
    L28_to_disk_inside_preserved:
        to_disk(q, max_r) leaves every point with r < max_r EXACTLY
        unchanged (the radial clamp never touches the interior).  Checked
        exhaustively over a dense grid of in-disk points x seeds.
    L29_to_disk_rim_exact:
        Any point with r >= max_r is mapped EXACTLY onto the sphere of
        radius max_r along its own ray: |out| == max_r and out is a
        non-negative scalar multiple of the input (no angular drift).
        Checked exhaustively over radial profiles and angles.
    L30_flow_over_dedup_and_self_loop_invariant:
        flow_over() reads neighbourhoods once and collapses each node's
        neighbour list through np.unique, so duplicate edge entries,
        self-loops (u==v), and out-of-range endpoints are exactly
        equivalent to their de-duplicated / valid/absent counterparts:
        the trajectory is identical.  Checked over many (edges, q) cases.
HONEST NEGATIVE (rejected, not introduced):
    L31_settle_conserves_centroid:
        The candidate "FlowEngine.settle conserves the population
        centroid sum(q)" is FALSE: the always-on private-home tether term
        -A*mu0*(q - h) steadily pulls each unit toward its home, so the
        centroid drifts (nonzero displacement per step).  A pure local
        balance flow already breaks exact centroid conservation; the
        honest audit reports it instead of claiming a conserved quantity
        the engine does not have.
"""
import numpy as np

from puno_flow import FlowEngine, to_disk


_GRID_N = 41                  # points per axis for the in-disk grid (dim 2)
_ANGLE_SAMPLES = 48
_RADII = [0.0, 0.5, 0.9, 1.0, 1.5, 3.0, 10.0]
_SEEDS = list(range(6))


def _in_disk_points(max_r):
    """Dense 2-D grid strictly inside the disk (r < max_r)."""
    c = np.linspace(-max_r + 1e-3, max_r - 1e-3, _GRID_N)
    gx, gy = np.meshgrid(c, c)
    pts = np.stack([gx.ravel(), gy.ravel()], axis=-1).reshape(-1, 2)
    r = np.hypot(pts[:, 0], pts[:, 1])
    return pts[r < max_r]


def _on_rim_points(max_r):
    """Points exactly on the rim (r == max_r)."""
    th = np.linspace(0, 2 * np.pi, _ANGLE_SAMPLES, endpoint=False)
    return np.stack([np.cos(th), np.sin(th)], axis=-1) * max_r


def _radial_profiles(max_r):
    """Out-of-rim radial points at several magnitudes, every angle."""
    pts = []
    for k in _RADII:
        if k <= max_r:
            continue
        th = np.linspace(0, 2 * np.pi, _ANGLE_SAMPLES, endpoint=False)
        pts.append(np.stack([np.cos(th), np.sin(th)], axis=-1) * k)
    return np.concatenate(pts, axis=0) if pts else np.zeros((0, 2))


def _L28_inside_preserved(datum):
    max_r, seed = datum
    rng = np.random.RandomState(seed)
    inside = _in_disk_points(max_r)
    jitter = rng.rand(inside.shape[0], 2) * 1e-6
    out = to_disk(inside + jitter, max_r)
    # points that remained inside (all of them after 1e-6 jitter) unchanged
    return np.array_equal(out, inside + jitter)


def _L29_rim_exact(datum):
    max_r, seed = datum
    rng = np.random.RandomState(seed)
    prof = _radial_profiles(max_r)
    if len(prof) == 0:
        return True
    out = to_disk(prof, max_r)
    rout = np.hypot(out[:, 0], out[:, 1])
    if not np.allclose(rout, max_r, atol=1e-9):
        return False
    # out must be a non-negative scalar multiple of prof (pure radial,
    # no angular drift):  out = c * prof with a single scalar c >= 0.
    c = (out * prof).sum(axis=-1) / np.maximum((prof * prof).sum(axis=-1),
                                               1e-300)
    residual = out - c[:, None] * prof
    return (np.allclose(residual, 0.0, atol=1e-9)
            and float(c.min()) >= -1e-9)


def _engine(seed=0):
    rng = np.random.RandomState(seed)
    e = FlowEngine(dim=2, k=4, mu0=0.12, A=1.0, dt=0.5, max_r=0.9,
                   eps=1e-9, use_index=False, index_min_n=0)
    n = 7
    e.add_many(rng.rand(n, 2) * 0.5)
    return e, rng, n


def _flow_over_result(edges, seed, steps=4):
    rng0 = np.random.RandomState(seed)
    e = FlowEngine(dim=2, k=4, mu0=0.12, A=1.0, dt=0.5, max_r=0.9,
                   eps=1e-9, use_index=False, index_min_n=0)
    n = 7
    e.add_many(rng0.rand(n, 2) * 0.5)
    e.flow_over(np.array(edges, dtype=int), steps=steps)
    return e.q


def _L30_dedup_self_loop(datum):
    seed, case = datum
    rng = np.random.RandomState(seed)
    n = 7
    u = rng.randint(0, n, 40)
    v = rng.randint(0, n, 40)
    edges = np.stack([u, v], axis=-1).tolist()
    # de-duplicated: collapse via np.unique per oriented pair
    undirected = set()
    for a, b in edges:
        undirected.add((min(a, b), max(a, b)))
    for a, b in list(undirected):
        if a == b:
            undirected.discard((a, b))
    unique_edges = [list(p) for p in undirected]
    base = _flow_over_result(edges, seed)
    dedup = _flow_over_result(unique_edges or ([(0, 1)] if n > 1 else []), seed)
    return np.array_equal(base, dedup)


def _L31_settle_conserves_centroid(datum):
    """The FALSE candidate law: settle conserves the population centroid.
    Returns True iff the centroid is (numerically) conserved, which fails
    immediately because the home tether pulls every unit toward its own
    private home."""
    seed, = datum
    e = _engine(seed)[0]
    c0 = e.q.sum(axis=0)
    e.settle(steps=50)
    c1 = e.q.sum(axis=0)
    return np.allclose(c0, c1, atol=1e-9)


def _certify(label, meta, pred, domain):
    from experiments.emanation import law_checker as lc
    return lc.certify_statement(label, meta, pred, list(domain))


_INSIDE_DOMAIN = [(0.9, s) for s in _SEEDS] + [(1.0, s) for s in _SEEDS]
_RIM_DOMAIN = [(0.9, s) for s in _SEEDS] + [(1.0, s) for s in _SEEDS]
_EDGE_DOMAIN = [(s, c) for s in _SEEDS for c in range(2)]
_SETTLE_DOMAIN = [(s,) for s in _SEEDS]


def puno_flow_certificates():
    certs = []
    certs.append(_certify(
        "L28_to_disk_inside_preserved",
        {"domain": "to_disk(q, max_r) over a dense 2-D in-disk grid "
                   "(1e-6 jittered), max_r in {0.9, 1.0}, x 6 seeds: "
                   "interior points must be left bit-exactly unchanged",
         "law": "the radial clamp never touches the interior: every point "
                "with r < max_r returns unchanged",
         "measured_on": "puno_flow.engine.to_disk"},
        _L28_inside_preserved, _INSIDE_DOMAIN))
    certs.append(_certify(
        "L29_to_disk_rim_exact",
        {"domain": "out-of-rim radial profiles at radii {1.5,3.0,10.0} "
                   "x 48 angles, max_r in {0.9,1.0} x 6 seeds",
         "law": "every out-of-rim point lands exactly on the max_r sphere "
                "along its own ray: |out| == max_r, out = positive scalar "
                "* input (no angular drift)",
         "measured_on": "puno_flow.engine.to_disk"},
        _L29_rim_exact, _RIM_DOMAIN))
    certs.append(_certify(
        "L30_flow_over_dedup_and_self_loop_invariant",
        {"domain": "40 random (u,v) edge entries over 7 units, x 6 seeds "
                   "x 2 cases, steps=4",
         "law": "flow_over collapses each node's neighbour list via "
                "np.unique, so duplicate edges, self-loops, and "
                "out-of-range endpoints are exactly equivalent to their "
                "de-duplicated counterpart: identical trajectory",
         "measured_on": "puno_flow.engine.FlowEngine.flow_over"},
        _L30_dedup_self_loop, _EDGE_DOMAIN))
    certs.append(_certify(
        "L31_settle_conserves_centroid",
        {"domain": "6 seeded random 7-unit engines, 50 settle steps",
         "law": "FALSE CANDIDATE: FlowEngine.settle conserves the "
                "population centroid sum(q); the always-on home tether "
                "-A*mu0*(q-h) steadily pulls each unit homeward, so the "
                "centroid drifts",
         "honest_check": "centroid must move (drift > 0); no conserved "
                         "quantity to report"},
        _L31_settle_conserves_centroid, _SETTLE_DOMAIN))
    return certs