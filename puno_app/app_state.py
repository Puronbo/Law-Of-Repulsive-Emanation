"""Puno lab - full-stack application built on puno_flow.

The toy network is the main application: a live scale-free network in R^2
that the UI drives through a JSON API.  This module is the application layer
(no HTTP) - a single NetworkApp holds one live engine plus its wiring,
ledger, and event log, and implements every action the UI can trigger:

    new / step / create / spawn / damage / heal / search / route / rewire /
    autotick / record / verify / ledger / topology

All mutation happens under a lock so the threaded HTTP server stays safe.
"""

import threading

import numpy as np

from puno_flow import FlowEngine, verify_exact
from puno_flow.apps.guard_mesh import holes
from puno_flow.apps.router import route
from puno_flow.topology import degree_sequence, hubs, preferential_attachment, topology_stats


def _clean(obj):
    """Recursively convert numpy types so the result is JSON-serializable."""
    if isinstance(obj, dict):
        return {k: _clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    return obj


class NetworkApp:
    """One live network + wiring + ledger, exposed to the HTTP layer."""

    def __init__(self, dim=2):
        self.dim = dim
        self.engine = None
        self.edges = None
        self.topology = "scale-free"
        self.recording = True
        self._cover_target = None
        self.log = []
        self.lock = threading.RLock()

    # ------------------------------------------------------------------ #
    def _log(self, msg):
        self.log.append(msg)
        if len(self.log) > 200:
            del self.log[:-200]

    # ------------------------------------------------------------------ #
    def new_network(self, n=300, k=8, mu0=0.12, topology="scale-free", m=2,
                    seed=7, settle=30):
        rng = np.random.RandomState(int(seed))
        homes = rng.uniform(-0.5, 0.5, (int(n), self.dim))
        self.engine = FlowEngine(dim=self.dim, k=int(k),
                                 mu0=float(mu0)).add_many(homes)
        self.edges = None
        self.topology = topology
        self._cover_target = None
        self._log(f"new network: n={int(n)} k={int(k)} topology={topology}")
        if topology == "scale-free":
            self.edges = preferential_attachment(
                int(n), m=int(m), rng=np.random.RandomState(int(seed) + 1))
            self._log(f"  wired scale-free: {len(self.edges)} edges (m={int(m)})")
            self.engine.flow_over(self.edges, steps=int(settle),
                                  record=self.recording)
        else:
            self.engine.settle(int(settle), record=self.recording)
        self._cover_target = self.engine.spacing()
        self._log(f"  settled {int(settle)} steps, cover target "
                  f"{self._cover_target:.4f}")
        return self.snapshot()

    def rewire(self, m=2, seed=None):
        if self.engine is None:
            raise ValueError("create a network first")
        rng = np.random.RandomState(int(seed) if seed is not None else 7)
        self.edges = preferential_attachment(self.engine.n, m=int(m), rng=rng)
        self.topology = "scale-free"
        self._log(f"rewired scale-free: {len(self.edges)} edges (m={int(m)})")
        return self.snapshot()

    def step(self, steps=10, mode="settle", mu=0.0):
        if self.engine is None:
            raise ValueError("create a network first")
        steps = max(1, int(steps))
        if mode == "over" and self.edges is not None:
            self.engine.flow_over(self.edges, steps=steps,
                                  record=self.recording)
            self._log(f"flow_over {steps} steps over fixed wiring")
        elif mode == "absorb":
            self.engine.absorb(steps, mu=float(mu), record=self.recording)
            self._log(f"absorb {steps} steps (mu={float(mu)})")
        else:
            self.engine.settle(steps, record=self.recording)
            self._log(f"settle {steps} steps")
        return self.snapshot()

    # ------------------------------------------------------------------ #
    def create(self, x, y):
        i = self.engine.create(np.array([float(x), float(y)]))
        self._log(f"created unit {i} at ({float(x):.3f},{float(y):.3f})")
        return self.snapshot()

    def spawn(self, count=3):
        if self.engine is None or self.engine.n == 0:
            raise ValueError("no units to spawn around")
        created = self.engine.spawn(int(count),
                                    rng=np.random.RandomState(1))
        self._log(f"spawned {len(created)} units around homes")
        return self.snapshot()

    def damage(self, count=10):
        count = min(int(count), self.engine.n)
        drop = np.random.RandomState(2).choice(self.engine.n, size=count,
                                               replace=False)
        mapping = self.engine.remove(drop)
        if self.edges is not None:
            new_edges = []
            for u, v in np.asarray(self.edges, dtype=int):
                nu, nv = mapping.get(int(u)), mapping.get(int(v))
                if nu is not None and nv is not None and nu != nv:
                    new_edges.append((nu, nv))
            self.edges = (np.asarray(new_edges, dtype=int)
                          if new_edges else None)
        self._log(f"damage: removed {count} units")
        return self.snapshot()

    def heal(self, steps=50):
        self.engine.heal(int(steps), record=self.recording)
        self._log(f"healed {int(steps)} steps")
        return self.snapshot()

    # ------------------------------------------------------------------ #
    def search(self, x, y, k=5):
        hits, dist = self.engine.search(np.array([float(x), float(y)]),
                                        k=int(k))
        return {"query": [float(x), float(y)],
                "hits": [[int(i), float(d)] for i, d in zip(hits, dist)]}

    def route(self, start, x, y):
        path, delivered = route(self.engine, int(start),
                                np.array([float(x), float(y)]))
        return {"path": [int(p) for p in path], "delivered": bool(delivered),
                "hops": len(path)}

    # ------------------------------------------------------------------ #
    def autotick(self, steps=3, respawn=3):
        if self.engine is None:
            raise ValueError("create a network first")
        events = []
        if self.edges is not None and self.topology == "scale-free":
            self.engine.flow_over(self.edges, steps=int(steps),
                                  record=self.recording)
        else:
            self.engine.settle(int(steps), record=self.recording)
        s = self.engine.spacing()
        if self._cover_target is not None and s > self._cover_target:
            rng = np.random.RandomState(3)
            for h in holes(self.engine)[:int(respawn)]:
                x = self.engine.q[int(h)] + rng.randn(self.dim) * 0.02
                self.engine.create(x, parent=int(h))
                events.append(f"respawned near unit {int(h)}")
            self._log(f"autotick: spacing {s:.4f} > target "
                      f"{self._cover_target:.4f}; respawned {len(events)}")
        return self.snapshot(events=events)

    def set_record(self, on=True):
        self.recording = bool(on)
        self._log(f"ledger recording {'on' if on else 'off'}")
        return self.snapshot()

    # ------------------------------------------------------------------ #
    def verify(self):
        if self.engine is None or self.engine.n == 0:
            return {"skipped": "no network"}
        if self.engine.n > 1500:
            return {"skipped": f"n={self.engine.n} too large for the "
                              "all-pairs reference"}
        ok, report = verify_exact(self.engine.q,
                                  k=min(self.engine.k, 12), steps=3)
        return {"ok": bool(ok), "report": report}

    def ledger(self):
        ok, unit, seq = self.engine.verify_ledger()
        audit = self.engine.ledger_audit()
        audit["verified"] = ok
        if not ok:
            audit["first_bad"] = {"unit": unit, "seq": seq}
        return audit

    def wiring(self):
        if self.edges is None:
            return {"wired": False}
        h_idx, h_deg = hubs(self.edges, self.engine.n, k=5)
        return {"wired": True,
                "stats": topology_stats(self.edges, self.engine.n),
                "hubs": [[int(i), int(d)]
                         for i, d in zip(h_idx, h_deg)]}

    # ------------------------------------------------------------------ #
    def snapshot(self, events=None):
        if self.engine is None or self.engine.n == 0:
            return _clean({"n": 0, "positions": [], "edges": None,
                           "degree": None, "topology": self.topology,
                           "stats": {}, "ledger": {}, "log": self.log[-30:],
                           "events": events or []})
        n = self.engine.n
        deg = degree_sequence(self.edges, n) if self.edges is not None else None
        ledger_ok = self.engine.verify_ledger()[0]
        return _clean({
            "n": n,
            "dim": self.engine.q.shape[1],
            "k": self.engine.k,
            "topology": self.topology,
            "positions": self.engine.q,
            "homes": self.engine.h,
            "edges": self.edges,
            "degree": deg,
            "stats": {
                "spacing": self.engine.spacing() if n > 1 else 0.0,
                "consensus": self.engine.consensus(),
                "finite": bool(np.isfinite(self.engine.q).all()),
                "max_r": float(np.linalg.norm(self.engine.q, axis=-1).max())
                if n else 0.0,
            },
            "ledger": {
                "chains": len(self.engine.chains.chains),
                "blocks": sum(c.length
                              for c in self.engine.chains.chains.values()),
                "verified": bool(ledger_ok),
            },
            "topology_stats": (topology_stats(self.edges, n)
                               if self.edges is not None else None),
            "log": self.log[-30:],
            "events": events or [],
        })
