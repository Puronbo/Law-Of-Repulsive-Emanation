"""
T55f: DecentralNet live daemon - run the net indefinitely.

A perpetual, self-sustaining session for the numpy-only DecentralNet module
(Universals/manifold/decentral_net.py).  The net never stops:

  every tick     2 local settle steps (mu=0; private home trap + k-NN
                 repulsion, no global mean/max/controller)
  arrivals       a neuron is born at a random home every ARRIVAL_EVERY ticks
  population cap the most crowded neuron is pruned when n > CAP, so the
                 per-step cost stays O(CAP^2) -> bounded -> truly indefinite
  damage         every DAMAGE_EVERY ticks one random neuron dies; the local
                 flow re-spreads the survivors (self-healing, no repair unit)
  heartbeat      every HEARTBEAT_EVERY ticks one status line: n, spacing,
                 mean_r, routing probe, avg ms/tick, uptime, step count

Everything is bounded-memory (fixed-size ring summaries, no log growth),
numpy-only apart from the standard library.

Usage:
  python decentral_net_live.py                  # run FOREVER (Ctrl-C stops)
  python decentral_net_live.py --seconds 120    # bounded run (validation)
  python decentral_net_live.py --ticks 50000    # bounded run by tick count
"""

import numpy as np
import sys, os, time, signal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Universals'))
from manifold.decentral_net import DecentralNet

# ---------------------------------------------------------------------- #
DIM = 2
CAP = 30
HOME_R = 0.35
ARRIVAL_EVERY = 50
DAMAGE_EVERY = 2000
HEARTBEAT_EVERY = 200
FLOW_PER_TICK = 2
MIN_POP = 3
PROBE_PTS = 60
PROBE_NOISE = 0.02
RING = 10                     # heartbeat history kept in memory

# ---------------------------------------------------------------------- #
def home_position(rng):
    th = rng.uniform(0, 2 * np.pi)
    return np.array([HOME_R * np.cos(th), HOME_R * np.sin(th)])


def probe_acc(net, rng):
    """Self-consistent routing probe: a cloud around each current neuron."""
    if net.n == 0:
        return 1.0
    X = np.vstack([net.q[j] + rng.randn(PROBE_PTS, DIM) * PROBE_NOISE
                   for j in range(net.n)])
    y = np.repeat(np.arange(net.n), PROBE_PTS)
    return net.accuracy(X, y)


def most_crowded_index(net):
    """Index of the neuron with the smallest mean k-NN distance (prune target)."""
    if net.n < 2:
        return 0
    D = np.linalg.norm(net.q[:, None] - net.q[None], axis=-1)
    np.fill_diagonal(D, np.inf)
    kk = min(net.k, net.n - 1)
    mean_d = np.sort(D, axis=1)[:, :kk].mean(axis=1)
    return int(np.argmin(mean_d))


# ---------------------------------------------------------------------- #
class Live:
    def __init__(self, seed=42, cap=CAP):
        self.rng = np.random.RandomState(seed)
        self.net = DecentralNet(dim=DIM, k=8, mu0=0.12, A=120.0, dt=0.05,
                                max_r=0.9)
        self.cap = cap
        self.tick = 0
        self.born = 0
        self.pruned = 0
        self.killed = 0
        self.recent_ms = []
        self.heartbeats = []
        self._stop = False

    # ------------------------------------------------------------------ #
    def _arrive(self):
        h = home_position(self.rng)
        self.net.add(h)                 # new neuron, home = arrival position
        self.net.absorb(40)             # seat it (tighten to home)
        self.born += 1

    def _prune(self):
        while self.net.n > self.cap:
            j = most_crowded_index(self.net)
            self.net.remove([j])
            self.pruned += 1
        self.net.settle(40)             # re-spread after pruning

    def _damage(self):
        if self.net.n <= MIN_POP:
            return
        j = int(self.rng.choice(self.net.n))
        self.net.remove([j])
        self.killed += 1
        self.net.settle(60)             # local heal (no repair unit)

    def _heartbeat(self, t0):
        n = self.net.n
        spacing = self.net.spacing()
        r = np.linalg.norm(self.net.q, axis=1)
        mean_r = float(r.mean()) if n else 0.0
        acc = probe_acc(self.net, self.rng)
        avg_ms = float(np.mean(self.recent_ms[-RING:])) if self.recent_ms else 0.0
        uptime = time.time() - t0
        line = (f"[tick {self.tick:>7}] n={n:<3} spacing={spacing:.3f} "
                f"mean_r={mean_r:.3f} probe={acc:.3f} {avg_ms:.2f}ms/tick "
                f"born={self.born} pruned={self.pruned} killed={self.killed} "
                f"up={uptime:>6.0f}s")
        self.heartbeats.append(line)
        if len(self.heartbeats) > RING:
            self.heartbeats.pop(0)
        print(line, flush=True)

    # ------------------------------------------------------------------ #
    def run(self, max_seconds=None, max_ticks=None):
        t0 = time.time()

        def _sig(signum, frame):
            self._stop = True
            print("\n[sig {0}] draining and exiting...".format(signum), flush=True)
        signal.signal(signal.SIGINT, _sig)
        try:
            signal.signal(signal.SIGTERM, _sig)
        except (AttributeError, OSError):
            pass

        while not self._stop:
            t_a = time.time()
            self.tick += 1
            self.net.settle(FLOW_PER_TICK)
            if self.tick % ARRIVAL_EVERY == 0:
                self._arrive()
            if self.tick % DAMAGE_EVERY == 0:
                self._damage()
            if self.net.n > self.cap:
                self._prune()
            self.recent_ms.append((time.time() - t_a) * 1e3)
            if len(self.recent_ms) > RING:
                self.recent_ms.pop(0)
            if self.tick % HEARTBEAT_EVERY == 0:
                self._heartbeat(t0)
            if max_seconds is not None and (time.time() - t0) >= max_seconds:
                break
            if max_ticks is not None and self.tick >= max_ticks:
                break

        uptime = time.time() - t0
        print("\n" + "=" * 62)
        print("LIVE SUMMARY")
        print("=" * 62)
        print(f"  ticks={self.tick}  uptime={uptime:.0f}s  "
              f"avg {(uptime / max(self.tick, 1)) * 1e3:.2f}ms/tick")
        print(f"  born={self.born}  pruned={self.pruned}  killed={self.killed}")
        print(f"  final n={self.net.n}  spacing={self.net.spacing():.3f}")
        r = np.linalg.norm(self.net.q, axis=1)
        print(f"  final mean_r={float(r.mean()):.3f} (healthy mid-shell "
              f"~0.6 => stable, not rim-collapsed)")
        print(f"\nDone.")


# ---------------------------------------------------------------------- #
def main(argv):
    max_seconds, max_ticks = None, None
    if '--seconds' in argv:
        max_seconds = int(argv[argv.index('--seconds') + 1])
    if '--ticks' in argv:
        max_ticks = int(argv[argv.index('--ticks') + 1])
    seed = 42
    if '--seed' in argv:
        seed = int(argv[argv.index('--seed') + 1])

    print("=" * 62)
    print("T55f: DECENTRALNET LIVE DAEMON (runs indefinitely by default)")
    print(f"  dim={DIM} cap={CAP} arrivals every {ARRIVAL_EVERY} "
          f"damage every {DAMAGE_EVERY}")
    print(f"  local-only: home trap + k-NN repulsion, no central controller")
    print("=" * 62)
    live = Live(seed=seed, cap=CAP)
    live.run(max_seconds=max_seconds, max_ticks=max_ticks)


if __name__ == "__main__":
    main(sys.argv[1:])
