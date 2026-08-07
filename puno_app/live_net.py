"""Puno Net - an indefinite live-session service around puno_flow.FlowEngine.

The net never stops.  Each tick runs 2 local settle steps (private home
trap + k-NN repulsion; no central controller).  A neuron is born at a
random home every ARRIVAL_EVERY ticks; the most crowded neuron is pruned
while n > cap so per-step cost stays bounded; every DAMAGE_EVERY ticks one
neuron dies and the local flow re-spreads the survivors.  Everything is
bounded-memory (fixed-size ring summaries, no log growth) and runs on
numpy + the standard library.

The service is supervised as a full-stack app:

  * a background thread runs the tick loop forever (self-healing,
    checkpointing every AUTOSAVE_EVERY ticks, with checkpoint rotation)
  * a stdlib ThreadingHTTPServer exposes a JSON API + a live dashboard
    at GET /, so a process supervisor or browser can watch it
  * graceful stop: a stopfile, Ctrl-C, or POST /api/stop all drain the
    loop to --save so the session continues with no damage
  * pause / resume, on-the-fly damage and live config tuning are first-class
  * checkpoints pickle (engine + homes + RNG + counters), so tick counter,
    population and the RNG stream all carry on across restarts

Run it:

    python -m puno_app.live_net                        # serve forever
    python -m puno_app.live_net --port 8766 --save live.pkl
    python -m puno_app.live_net --load live.pkl        # resume
    puno-net --port 8766                               # installed entry point

API (all JSON):
    GET  /                      - dashboard (live_net.html)
    GET  /api/status            - full live state + counters + config
    GET  /api/metrics           - ring of heartbeats for sparklines
    GET  /api/positions         - neuron coordinates (origin ring)
    GET  /api/alerts            - recent heuristic alerts
    GET  /api/health            - supervisor probe (200 alive / 503 draining)
    POST /api/pause             - pause the tick loop
    POST /api/resume            - resume the tick loop
    POST /api/step              - {count} run N ticks synchronously
    POST /api/damage            - {count} kill N random neurons now
    POST /api/config            - live tuning: cap, home_r, arrival_every,
                                  damage_every, flow_per_tick, min_pop,
                                  heartbeat_every, mu0, k
    POST /api/checkpoint        - force a checkpoint now
    POST /api/stop              - {save: bool} drain and exit

CLI extras:
    python -m puno_app.live_net --status   # probe a running instance
"""

import argparse
import json
import os
import pickle
import sys
import time
import urllib.request
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Event, RLock, Thread
from urllib.parse import urlparse

import numpy as np

from puno_flow.engine import FlowEngine

HTML_PATH = Path(__file__).resolve().parent / "live_net.html"

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
RING = 10                     # heartbeat log kept in memory
METRIC_RING = 300             # heartbeats kept for the dashboard
AUTOSAVE_EVERY = 50000        # ticks between automatic checkpoints
KEEP_CHECKPOINTS = 3          # timestamped checkpoints kept (plus the base)

DEFAULT_CONFIG = dict(
    dim=DIM, cap=CAP, home_r=HOME_R, arrival_every=ARRIVAL_EVERY,
    damage_every=DAMAGE_EVERY, heartbeat_every=HEARTBEAT_EVERY,
    flow_per_tick=FLOW_PER_TICK, min_pop=MIN_POP,
    probe_pts=PROBE_PTS, probe_noise=PROBE_NOISE, mu0=0.12, k=8,
)

TUNABLE = {"cap", "home_r", "arrival_every", "damage_every",
           "flow_per_tick", "min_pop", "heartbeat_every", "mu0", "k"}


# ---------------------------------------------------------------------- #
def _home_position(rng, home_r):
    th = rng.uniform(0, 2 * np.pi)
    return np.array([home_r * np.cos(th), home_r * np.sin(th)])


def _probe_acc(engine, rng, pts, noise):
    """Self-consistent routing probe: a cloud around each current neuron."""
    if engine.n == 0:
        return 1.0
    X = np.vstack([engine.q[j] + rng.randn(pts, DIM) * noise
                   for j in range(engine.n)])
    y = np.repeat(np.arange(engine.n), pts)
    return float(engine.accuracy(X, y))


def _most_crowded_index(engine):
    """Index of the neuron with the smallest mean k-NN distance."""
    if engine.n < 2:
        return 0
    D = np.linalg.norm(engine.q[:, None] - engine.q[None], axis=-1)
    np.fill_diagonal(D, np.inf)
    kk = min(engine.k, engine.n - 1)
    mean_d = np.sort(D, axis=1)[:, :kk].mean(axis=1)
    return int(np.argmin(mean_d))


def _json_default(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    return str(obj)


# ---------------------------------------------------------------------- #
class LiveNetService:
    """An indefinitely-running local-only network with an HTTP face."""

    def __init__(self, seed=42, save_path=None, autosave_every=AUTOSAVE_EVERY,
                 keep_checkpoints=KEEP_CHECKPOINTS, **cfg):
        merged = dict(DEFAULT_CONFIG)
        merged.update(cfg)
        self.config = merged
        self.seed = int(seed)
        self.save_path = save_path
        self.autosave_every = int(autosave_every)
        self.keep_checkpoints = int(keep_checkpoints)

        self.rng = np.random.RandomState(self.seed)
        self.engine = FlowEngine(dim=self.config["dim"], k=self.config["k"],
                                 mu0=self.config["mu0"], use_index=True)
        self.tick = 0
        self.born = 0
        self.pruned = 0
        self.killed = 0

        self.recent_ms = deque(maxlen=RING)
        self.heartbeats = deque(maxlen=RING)
        self.metrics = deque(maxlen=METRIC_RING)
        self.alerts = deque(maxlen=RING)

        self.started_at = time.time()
        self.lock = RLock()
        self._paused = False
        self._stop = False
        self._running = False
        self._last_save_tick = 0
        self._last_alert_key = None
        self._saved_final = False

    # ------------------------------------------------------------------ #
    # helpers
    # ------------------------------------------------------------------ #
    @property
    def n(self):
        return self.engine.n

    def _mean_r(self):
        r = np.linalg.norm(self.engine.q, axis=1)
        return float(r.mean()) if self.n else 0.0

    def _spacing(self):
        return self.engine.spacing()

    def _probe(self):
        return _probe_acc(self.engine, self.rng,
                          self.config["probe_pts"], self.config["probe_noise"])

    # ------------------------------------------------------------------ #
    # dynamics (mirror T55f decentral_net_live.py exactly)
    # ------------------------------------------------------------------ #
    def _arrive(self):
        h = _home_position(self.rng, self.config["home_r"])
        self.engine.add(h)
        self.engine.absorb(40)
        self.born += 1

    def _prune(self):
        while self.engine.n > self.config["cap"]:
            j = _most_crowded_index(self.engine)
            self.engine.remove([j])
            self.pruned += 1
        self.engine.settle(40)

    def _damage(self):
        if self.engine.n <= self.config["min_pop"]:
            return
        j = int(self.rng.choice(self.engine.n))
        self.engine.remove([j])
        self.killed += 1
        self.engine.settle(60)

    def _tick(self):
        t_a = time.time()
        self.tick += 1
        self.engine.settle(self.config["flow_per_tick"])
        if self.tick % self.config["arrival_every"] == 0:
            self._arrive()
        if self.tick % self.config["damage_every"] == 0:
            self._damage()
        if self.engine.n > self.config["cap"]:
            self._prune()
        self.recent_ms.append((time.time() - t_a) * 1e3)
        if self.tick % self.config["heartbeat_every"] == 0:
            self._heartbeat()

    def tick_once(self):
        """Advance exactly one tick (caller holds no lock assumption)."""
        with self.lock:
            self._tick()

    # ------------------------------------------------------------------ #
    def _heartbeat(self):
        n = self.n
        spacing = self._spacing()
        mean_r = self._mean_r()
        probe = self._probe()
        avg_ms = float(np.mean(self.recent_ms)) if self.recent_ms else 0.0
        uptime = time.time() - self.started_at
        line = (f"[tick {self.tick:>7}] n={n:<3} spacing={spacing:.3f} "
                f"mean_r={mean_r:.3f} probe={probe:.3f} {avg_ms:.2f}ms/tick "
                f"born={self.born} pruned={self.pruned} killed={self.killed} "
                f"up={uptime:>6.0f}s")
        self.heartbeats.append(line)
        print(line, flush=True)
        self.metrics.append(dict(tick=self.tick, n=n, spacing=spacing,
                                 mean_r=mean_r, probe=probe, ms=avg_ms,
                                 born=self.born, pruned=self.pruned,
                                 killed=self.killed))
        self._alert(n, mean_r, probe)

    def _alert(self, n, mean_r, probe):
        alert = None
        if self.config["cap"] > 0 and n <= self.config["min_pop"]:
            alert = f"population floor hit: n={n}"
        elif mean_r > 0.72:
            alert = f"rim-collapse risk: mean_r={mean_r:.3f}"
        elif probe < 0.5:
            alert = f"routing quality degraded: probe={probe:.3f}"
        if alert is not None and alert != self._last_alert_key:
            self.alerts.append(alert)
            self._last_alert_key = alert
        elif alert is None:
            self._last_alert_key = None

    # ------------------------------------------------------------------ #
    # run loop
    # ------------------------------------------------------------------ #
    def run_forever(self, max_seconds=None, max_ticks=None, stopfile=None,
                    sigint=True):
        """Drive the tick loop until stopped.  May run in any thread."""
        t0 = time.time()
        self._running = True
        try:
            if sigint:
                self._register_signal_handlers()
        except (ValueError, AttributeError, OSError):
            pass
        try:
            while not self._stop:
                with self.lock:
                    if not self._paused:
                        self._tick()
                if self._paused:
                    time.sleep(0.1)
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
                if (self.save_path and self.autosave_every > 0
                        and self.tick - self._last_save_tick >= self.autosave_every):
                    self._checkpoint(save_path=self.save_path)
                    self._last_save_tick = self.tick
        finally:
            self._running = False
            if self.save_path and not self._saved_final:
                self.save(self.save_path)
                self._saved_final = True
        return self.tick

    def _register_signal_handlers(self):
        import signal
        def _sig(signum, frame):
            self._stop = True
            print(f"\n[sig {signum}] draining and exiting...", flush=True)
        signal.signal(signal.SIGINT, _sig)
        try:
            signal.signal(signal.SIGTERM, _sig)
        except (AttributeError, OSError):
            pass

    def stop(self, save=True):
        with self.lock:
            self._stop = True
        if save and self.save_path and not self._saved_final:
            self.save(self.save_path)
            self._saved_final = True

    def pause(self):
        with self.lock:
            self._paused = True
        return {"paused": True, "tick": self.tick}

    def resume(self):
        with self.lock:
            self._paused = False
        return {"paused": False, "tick": self.tick}

    def step(self, count=1):
        """Advance `count` ticks synchronously (blocking API call).  A paused
        net stays frozen: explicit stepping is also suppressed."""
        count = max(1, int(count))
        with self.lock:
            if self._paused:
                return {"tick": self.tick, "n": self.n, "paused": True}
            for _ in range(count):
                self._tick()
        return {"tick": self.tick, "n": self.n}

    def damage(self, count=1):
        count = max(0, int(count))
        with self.lock:
            for _ in range(count):
                if self.engine.n <= self.config["min_pop"]:
                    break
                j = int(self.rng.choice(self.engine.n))
                self.engine.remove([j])
                self.killed += 1
            self.engine.settle(60)
        return {"killed": self.killed, "n": self.n}

    def configure(self, **kw):
        with self.lock:
            changes = {}
            for key, value in kw.items():
                if key not in TUNABLE:
                    raise ValueError(f"not tunable at runtime: {key}")
                self.config[key] = value
                changes[key] = value
            if "mu0" in changes:
                self.engine.mu0 = changes["mu0"]
            if "k" in changes:
                self.engine.k = changes["k"]
        return {"config": dict(self.config), "tick": self.tick}

    # ------------------------------------------------------------------ #
    # checkpointing
    # ------------------------------------------------------------------ #
    def _checkpoint_state(self):
        return dict(engine=self.engine, rng=self.rng, tick=self.tick,
                    born=self.born, pruned=self.pruned, killed=self.killed,
                    config=dict(self.config), seed=self.seed)

    def save(self, path):
        """Checkpoint the full live state (engine + homes + rng + counters)."""
        with self.lock:
            state = self._checkpoint_state()
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(state, f)
        print(f"[checkpoint] state saved -> {path} at tick {state['tick']} "
              f"(n={self.engine.n})", flush=True)

    def _timestamped_path(self, path):
        stamp = time.strftime("%Y%m%d-%H%M%S")
        return path.parent / f"{path.stem}.{stamp}{path.suffix}"

    def _checkpoint(self, save_path=None, rotate=True):
        path = save_path or self.save_path
        if not path:
            raise ValueError("no checkpoint path configured "
                             "(pass --save or --load)")
        path = Path(path)
        self.save(path)
        if rotate and self.keep_checkpoints > 0:
            snap = self._timestamped_path(path)
            with self.lock:
                state = self._checkpoint_state()
            with open(snap, "wb") as f:
                pickle.dump(state, f)
            keeps = sorted(path.parent.glob(f"{path.stem}.[0-9]*{path.suffix}"))
            for old in keeps[:-self.keep_checkpoints]:
                try:
                    old.unlink()
                except OSError:
                    pass
        return str(path)

    @classmethod
    def from_checkpoint(cls, path, save_path=None):
        """Resume a checkpointed session: tick counter, population and the
        RNG stream all carry on - the cycle is continuous."""
        path = Path(path)
        with open(path, "rb") as f:
            state = pickle.load(f)
        cfg = dict(state.get("config", DEFAULT_CONFIG))
        svc = cls(seed=state.get("seed", 42),
                  save_path=save_path or str(path), **cfg)
        svc.engine = state["engine"]
        svc.rng = state["rng"]
        svc.tick = state["tick"]
        svc.born = state.get("born", 0)
        svc.pruned = state.get("pruned", 0)
        svc.killed = state.get("killed", 0)
        svc.started_at = time.time()
        return svc

    # ------------------------------------------------------------------ #
    # read views (all under the lock)
    # ------------------------------------------------------------------ #
    def status(self):
        with self.lock:
            avg_ms = float(np.mean(self.recent_ms)) if self.recent_ms else 0.0
            return dict(
                ok=True, tick=self.tick, n=self.n, cap=self.config["cap"],
                dim=self.config["dim"], k=self.config["k"], mu0=self.config["mu0"],
                home_r=self.config["home_r"], spacing=self._spacing(),
                mean_r=self._mean_r(), probe=self._probe(),
                born=self.born, pruned=self.pruned, killed=self.killed,
                avg_ms=avg_ms, recent_ms=list(self.recent_ms),
                running=self._running, paused=self._paused,
                uptime=time.time() - self.started_at,
                started_at=self.started_at, seed=self.seed,
                save_path=str(self.save_path) if self.save_path else None,
                alerts=list(self.alerts),
                heartbeats=list(self.heartbeats),
                config=dict(self.config))

    def metrics_series(self, limit=None):
        with self.lock:
            rows = list(self.metrics)
        if limit is not None and limit > 0:
            rows = rows[-int(limit):]
        return dict(
            tick=[r["tick"] for r in rows],
            n=[r["n"] for r in rows],
            spacing=[r["spacing"] for r in rows],
            mean_r=[r["mean_r"] for r in rows],
            probe=[r["probe"] for r in rows],
            ms=[r["ms"] for r in rows],
            born=[r["born"] for r in rows],
            pruned=[r["pruned"] for r in rows],
            killed=[r["killed"] for r in rows],
            length=len(rows))

    def positions(self):
        with self.lock:
            return dict(n=self.n, home_r=self.config["home_r"],
                        q=[list(map(float, p)) for p in self.engine.q])

    def health(self):
        with self.lock:
            return dict(ok=not self._stop, running=self._running,
                        paused=self._paused, tick=self.tick, n=self.n,
                        cap=self.config["cap"], up=time.time() - self.started_at)


# ---------------------------------------------------------------------- #
# HTTP layer
# ---------------------------------------------------------------------- #
def _send_json(handler, code, payload):
    body = json.dumps(payload, default=_json_default).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(body)


class LiveNetHandler(BaseHTTPRequestHandler):
    server_version = "PunoNet/1.0"
    service = None  # bound in make_server via subclassing

    def log_message(self, fmt, *args):
        sys.stderr.write("puno_net: %s\n" % (fmt % args))

    def _error(self, msg, code=400):
        _send_json(self, code, {"ok": False, "error": str(msg)})

    def _ok(self, payload):
        _send_json(self, 200, {"ok": True, **payload})

    def _post_json(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        return json.loads(raw) if raw else {}

    def _serve_html(self):
        html = HTML_PATH.read_text(encoding="utf-8")
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        svc = self.service
        if path in ("/", "/index.html"):
            self._serve_html()
        elif path == "/api/status":
            self._ok(svc.status())
        elif path == "/api/metrics":
            qs = dict(p.split("=", 1) for p in urlparse(self.path).query.split("&") if "=" in p)
            limit = int(qs.get("limit", 0))
            self._ok(svc.metrics_series(limit or None))
        elif path == "/api/positions":
            self._ok(svc.positions())
        elif path == "/api/alerts":
            with svc.lock:
                self._ok({"alerts": list(svc.alerts)})
        elif path == "/api/health":
            health = svc.health()
            code = 200 if health["ok"] else 503
            _send_json(self, code, health)
        else:
            self._error(f"unknown path {path}", 404)

    def do_POST(self):
        path = urlparse(self.path).path
        svc = self.service
        body = self._post_json()
        try:
            if path == "/api/pause":
                self._ok(svc.pause())
            elif path == "/api/resume":
                self._ok(svc.resume())
            elif path == "/api/step":
                self._ok(svc.step(body.get("count", 1)))
            elif path == "/api/damage":
                self._ok(svc.damage(body.get("count", 1)))
            elif path == "/api/config":
                allowed = {k: v for k, v in body.items() if k in TUNABLE}
                self._ok(svc.configure(**allowed))
            elif path == "/api/checkpoint":
                self._ok({"path": svc._checkpoint(rotate=True)})
            elif path == "/api/stop":
                save = bool(body.get("save", False))
                svc.stop(save=save)
                self._ok({"stopping": True, "tick": svc.tick})
            else:
                self._error(f"unknown path {path}", 404)
        except Exception as exc:
            self._error(str(exc))


def make_server(service, host="127.0.0.1", port=8766):
    _svc = service

    class BoundHandler(LiveNetHandler):
        service = _svc
    server = ThreadingHTTPServer((host, port), BoundHandler)
    server.daemon_threads = True
    return server


def start_server(service, host="127.0.0.1", port=8766,
                 max_seconds=None, max_ticks=None, stopfile=None):
    """Run the tick loop in a background thread and serve HTTP in this one."""
    done = Event()

    def _drive():
        try:
            service.run_forever(max_seconds=max_seconds, max_ticks=max_ticks,
                                stopfile=stopfile)
        finally:
            done.set()

    Thread(target=_drive, daemon=True).start()
    server = make_server(service, host, port)
    host, port = server.server_address[:2]
    Thread(target=server.serve_forever, daemon=True).start()
    print(f"Puno Net dashboard: http://{host}:{port}")
    try:
        done.wait()
    except KeyboardInterrupt:
        service.stop(save=True)
    finally:
        service.stop(save=True)
        server.shutdown()
    return service


# ---------------------------------------------------------------------- #
def _query_status(host, port):
    url = f"http://{host}:{port}/api/health"
    with urllib.request.urlopen(url, timeout=5) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    ok = payload.get("ok", False)
    print(f"Puno Net @ {host}:{port}  ok={ok} running={payload.get('running')} "
          f"paused={payload.get('paused')} tick={payload.get('tick')} "
          f"n={payload.get('n')}/{payload.get('cap')} "
          f"up={payload.get('up', 0):.0f}s")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Puno Net: indefinite live-session service + dashboard")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8766)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--cap", type=int, default=CAP)
    ap.add_argument("--home-r", type=float, default=HOME_R)
    ap.add_argument("--arrival-every", type=int, default=ARRIVAL_EVERY)
    ap.add_argument("--damage-every", type=int, default=DAMAGE_EVERY)
    ap.add_argument("--flow-per-tick", type=int, default=FLOW_PER_TICK)
    ap.add_argument("--save", default=None, help="checkpoint path")
    ap.add_argument("--load", default=None, help="resume a checkpoint")
    ap.add_argument("--seconds", type=float, default=None, help="bounded run")
    ap.add_argument("--ticks", type=int, default=None, help="bounded run")
    ap.add_argument("--stopfile", default=None)
    ap.add_argument("--status", action="store_true",
                    help="probe a running instance and exit")
    args = ap.parse_args(argv)

    if args.status:
        return _query_status(args.host, args.port)

    if not HTML_PATH.exists():
        print(f"missing dashboard file: {HTML_PATH}", file=sys.stderr)
        return 1

    if args.load:
        service = LiveNetService.from_checkpoint(
            args.load, save_path=args.save)
        print(f"[resume] loaded tick={service.tick} n={service.n} "
              f"(cycle continues, no damage)", flush=True)
    else:
        service = LiveNetService(
            seed=args.seed, save_path=args.save, cap=args.cap,
            home_r=args.home_r, arrival_every=args.arrival_every,
            damage_every=args.damage_every, flow_per_tick=args.flow_per_tick)

    start_server(service, args.host, args.port,
                 max_seconds=args.seconds, max_ticks=args.ticks,
                 stopfile=args.stopfile)
    return 0


if __name__ == "__main__":
    sys.exit(main())
