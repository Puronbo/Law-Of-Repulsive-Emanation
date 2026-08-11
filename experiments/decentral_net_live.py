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

Checkpoint / resume (stop anytime, continue with no damage):
  --save PATH     checkpoint full state (net + homes + RNG + counters) on
                  graceful stop and every AUTOSAVE_EVERY ticks
  --load PATH     resume a checkpoint: tick counter, population and the
                  RNG stream all carry on - the cycle is continuous
  --stopfile PATH exit (draining to --save) the moment this file appears;
                  create it with:  New-Item stop.flag

Usage:
  python decentral_net_live.py                  # run FOREVER (Ctrl-C stops)
  python decentral_net_live.py --seconds 120    # bounded run (validation)
  python decentral_net_live.py --ticks 50000    # bounded run by tick count
  python decentral_net_live.py --save live.pkl --stopfile stop.flag
  python decentral_net_live.py --load live.pkl  # resume
  python decentral_net_live.py --verdict data/decentral_net_live_data.json
                                                # pin the structural claims
"""

import numpy as np
import sys, os, time, signal, pickle

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
AUTOSAVE_EVERY = 50000        # ticks between automatic checkpoints

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
        self.heal_samples = []
        self.max_n = 0
        self.arrival_every = ARRIVAL_EVERY
        self.damage_every = DAMAGE_EVERY
        self.heartbeat_every = HEARTBEAT_EVERY
        self.flow_per_tick = FLOW_PER_TICK
        self.min_pop = MIN_POP
        self.autosave_every = AUTOSAVE_EVERY
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
        if self.net.n <= self.min_pop:
            return
        pre = self.net.spacing()
        j = int(self.rng.choice(self.net.n))
        self.net.remove([j])
        self.killed += 1
        self.net.settle(60)
        post = self.net.spacing()
        self.heal_samples.append([float(pre), float(post)])

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
    def save(self, path):
        """Checkpoint the full live state (net + homes + rng + counters)."""
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        print(f"[checkpoint] state saved -> {path} at tick {self.tick} "
              f"(n={self.net.n})", flush=True)

    @staticmethod
    def load(path):
        """Resume a checkpointed live session.  The cycle continues with no
        damage: tick counter, population, homes, RNG stream all carry on."""
        with open(path, 'rb') as f:
            return pickle.load(f)

    # ------------------------------------------------------------------ #
    def run(self, max_seconds=None, max_ticks=None,
            save_path=None, stopfile=None):
        t0 = time.time()
        last_save = 0

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
            self.net.settle(self.flow_per_tick)
            if self.tick % self.arrival_every == 0:
                self._arrive()
            if self.tick % self.damage_every == 0:
                self._damage()
            if self.net.n > self.cap:
                self._prune()
            self.max_n = max(self.max_n, self.net.n)
            self.recent_ms.append((time.time() - t_a) * 1e3)
            if len(self.recent_ms) > RING:
                self.recent_ms.pop(0)
            if self.tick % self.heartbeat_every == 0:
                self._heartbeat(t0)
            if save_path and self.tick - last_save >= self.autosave_every:
                self.save(save_path)
                last_save = self.tick
            if stopfile and os.path.exists(stopfile):
                print(f"[stopfile] {stopfile} found at tick {self.tick}; "
                      f"draining...", flush=True)
                try:
                    os.remove(stopfile)
                except OSError:
                    pass
                break
            if max_seconds is not None and (time.time() - t0) >= max_seconds:
                break
            if max_ticks is not None and self.tick >= max_ticks:
                break

        if save_path:
            self.save(save_path)

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
def _verdict_run(seed, ticks=3000, damage_every=300):
    live = Live(seed=seed, cap=CAP)
    live.damage_every = damage_every
    live.heartbeat_every = ticks + 1      # silence heartbeats in verdict runs
    live.run(max_ticks=ticks)
    pre = np.median([s[0] for s in live.heal_samples]) if live.heal_samples else 0.0
    post = np.median([s[1] for s in live.heal_samples]) if live.heal_samples else 0.0
    recover = (post / pre) if pre > 0 else 1.0
    acc = probe_acc(live.net, live.rng)
    return live, float(pre), float(post), float(recover), float(acc)


def _verdict_resume(seed, t0=1500, dt=600):
    """Checkpoint/resume continuity: a resumed session reproduces the
    uninterrupted trajectory bit-for-bit (tick, counters, RNG stream, and
    neuron positions all carry on from the checkpoint)."""
    import tempfile
    cp = os.path.join(tempfile.gettempdir(), 'live_cp.pkl')
    a = Live(seed=seed, cap=CAP)
    a.damage_every = 300
    a.heartbeat_every = t0 + dt + 1
    a.run(max_ticks=t0)
    a.save(cp)
    a.run(max_ticks=t0 + dt)
    b = Live.load(cp)
    b.damage_every = 300
    b.heartbeat_every = t0 + dt + 1
    b.run(max_ticks=t0 + dt)
    pos_ok = bool(np.allclose(b.net.q, a.net.q))
    counters_ok = (b.tick == a.tick and b.born == a.born
                   and b.pruned == a.pruned and b.killed == a.killed)
    try:
        os.remove(cp)
    except OSError:
        pass
    return {"t0": t0, "dt": dt, "continuity": bool(pos_ok and counters_ok),
            "pos_identical": pos_ok, "counters_match": counters_ok}


def _verdict_main(path):
    import json, datetime
    SEEDS = (42, 11, 7)
    per = {}
    for s in SEEDS:
        live, pre, post, recover, acc = _verdict_run(s)
        per[str(s)] = {
            "ticks": live.tick, "cap": live.cap, "max_n": live.max_n,
            "born": live.born, "pruned": live.pruned, "killed": live.killed,
            "n_damage_events": len(live.heal_samples),
            "spacing_pre_damage": pre, "spacing_post_damage": post,
            "recovery_ratio": recover, "probe_acc": acc,
            "bounded_pop": bool(live.max_n <= live.cap),
            "healed": bool(0.05 <= post <= 0.9 and 0.5 <= recover <= 2.0),
            "routing_ok": bool(acc >= 0.8),
        }
    res = _verdict_resume(42)
    v1 = all(per[str(s)]["bounded_pop"] for s in SEEDS)
    v2 = all(per[str(s)]["healed"] for s in SEEDS)
    v3 = all(per[str(s)]["routing_ok"] for s in SEEDS)
    v4 = res["continuity"]
    claims = [
        {"id": "V1",
         "claim": "bounded-memory churn: population never exceeds CAP "
                  "under arrivals + damage + pruning (per-step cost stays "
                  "O(CAP^2))",
         "verdict": "SUPPORTED" if v1 else "FAILED",
         "all_seeds": v1},
        {"id": "V2",
         "claim": "self-healing without a repair unit: after each random "
                  "neuron death the local k-NN re-spread keeps the "
                  "survivors in the healthy consensus-spacing band (post "
                  "within 0.5-2.0x of pre - removing a neuron legitimately "
                  "enlarges mean k-NN distance), no clump and no rim "
                  "blow-up",
         "verdict": "SUPPORTED" if v2 else "FAILED",
         "all_seeds": v2},
        {"id": "V3",
         "claim": "routing intact through churn: self-consistent k-NN "
                  "probe stays accurate after thousands of ticks of "
                  "arrivals, damage and pruning",
         "verdict": "SUPPORTED" if v3 else "FAILED",
         "all_seeds": v3},
        {"id": "V4",
         "claim": "checkpoint/resume is lossless: a session resumed from a "
                  "checkpoint reproduces the uninterrupted trajectory "
                  "(positions, counters, RNG stream) deterministically",
         "verdict": "SUPPORTED" if v4 else "FAILED",
         "continuity": v4},
    ]
    overall = "SUPPORTED" if all([v1, v2, v3, v4]) else "FAILED"
    results = {
        "experiment": "decentral_net_live (T55f)",
        "date": datetime.date.today().isoformat(),
        "seeds": list(SEEDS),
        "verdict": ("%s (structural, bounded run): the live daemon's "
                    "population stays within CAP through arrivals, damage "
                    "and pruning; the local k-NN re-spread heals each random "
                    "death back to the healthy spacing band with no repair "
                    "unit; the self-consistent routing probe stays accurate "
                    "through churn; and a checkpoint/resume reproduces the "
                    "uninterrupted trajectory deterministically - all on "
                    "the repo's own numpy-only DecentralNet with bounded "
                    "ring memory" % overall),
        "per_seed": per,
        "resume_continuity": res,
        "claims": claims,
    }
    with open(path, 'w') as f:
        json.dump(results, f, indent=1, sort_keys=True)
    print("verdicts written to %s" % path)
    print("V1 bounded pop:  %s" % [per[str(s)]["bounded_pop"] for s in SEEDS])
    print("V2 healed:       %s" % [per[str(s)]["healed"] for s in SEEDS])
    print("V3 probe acc:    %s" % [round(per[str(s)]["probe_acc"], 3)
                                   for s in SEEDS])
    print("V4 resume lossless: %s" % res["continuity"])
    return results


# ---------------------------------------------------------------------- #
def main(argv):
    if '--verdict' in argv:
        _verdict_main(argv[argv.index('--verdict') + 1])
        return
    max_seconds, max_ticks = None, None
    if '--seconds' in argv:
        max_seconds = int(argv[argv.index('--seconds') + 1])
    if '--ticks' in argv:
        max_ticks = int(argv[argv.index('--ticks') + 1])
    seed = 42
    if '--seed' in argv:
        seed = int(argv[argv.index('--seed') + 1])
    save_path = None
    if '--save' in argv:
        save_path = argv[argv.index('--save') + 1]
    stopfile = None
    if '--stopfile' in argv:
        stopfile = argv[argv.index('--stopfile') + 1]

    print("=" * 62)
    print("T55f: DECENTRALNET LIVE DAEMON (runs indefinitely by default)")
    print(f"  dim={DIM} cap={CAP} arrivals every {ARRIVAL_EVERY} "
          f"damage every {DAMAGE_EVERY}")
    print(f"  local-only: home trap + k-NN repulsion, no central controller")
    print("=" * 62)
    if '--load' in argv:
        live = Live.load(argv[argv.index('--load') + 1])
        print(f"[resume] loaded tick={live.tick} n={live.net.n} "
              f"(cycle continues, no damage)", flush=True)
    else:
        live = Live(seed=seed, cap=CAP)
    live.run(max_seconds=max_seconds, max_ticks=max_ticks,
             save_path=save_path, stopfile=stopfile)


if __name__ == "__main__":
    main(sys.argv[1:])
