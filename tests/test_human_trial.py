"""Tests for the T74 human trial runner: session builder, answer mapping,
scoring glue, and the stdlib HTTP app.

The runner makes the T74 human protocol runnable in a browser:
  - build_session() is a deterministic plan (L1 probes, recheck, creativity),
  - build_answers() maps the human's recorded inputs onto the schema that
    score_participant() - the SAME code that grades the machine - consumes,
  - the HTTP server serves the single-page app and POST /api/score grades a
    recorded sheet on the engine's bars.
"""

import json
import threading
import urllib.error
import urllib.request

import numpy as np
import pytest

from puno_app.human_trial import (
    build_answers, build_session, grade,
)
from puno_app.human_trial_ui import make_server


def _perfect_sheet(session, n_creative=1):
    """Session-consistent answer key: exact routing plus mid-effort creative
    items (novel outward tweaks), like the pilot's 'perfect' archetype."""
    from experiments.human_trial_pilot import _taught, _outward_unit, memory
    l1 = {name: [c] * len(session["l1"]["probe_idx"])
          for c, name in enumerate(session["meta"]["concepts"])}
    rc = {name: [session["meta"]["concepts"].index(name)] *
          len(session["recheck"]["probe_idx"])
          for name in session["recheck"]["concepts"]}
    exemplars, probes = _taught(42)
    mem_pts, _ = memory(exemplars)
    rng = np.random.default_rng(7)
    items = []
    for c in range(len(session["meta"]["concepts"])):
        for _ in range(n_creative):
            src = mem_pts[rng.integers(c * 40, (c + 1) * 40)]
            move = src + 0.12 * _outward_unit(src, rng)
            items.append({"level": "mid",
                          "concept": session["meta"]["concepts"][c],
                          "x": float(move[0]), "y": float(move[1])})
    return build_answers(session, l1, rc, items)


# ---------------------------------------------------------------------- #
# Session plan
# ---------------------------------------------------------------------- #
class TestSession:
    def test_deterministic(self):
        assert build_session(20260812) == build_session(20260812)

    def test_seed_changes_probes(self):
        a = build_session(1)["l1"]["probe_idx"]
        b = build_session(2)["l1"]["probe_idx"]
        assert a != b

    def test_schema(self):
        s = build_session()
        assert len(s["meta"]["concepts"]) == 8
        assert set(s["meta"]["thresholds"]) == {
            "novelty_thr", "accept_r", "spacing_mean", "spacing_std"}
        assert set(s["meta"]["bars"]) == {
            "L1_ceiling", "L2_no_forgetting", "C1_mid_creative",
            "C2_novel_min", "C2_creative_max"}
        assert all(len(v) == 40 for v in s["teaching"].values())
        assert all(len(v) == 8 for v in s["l1"]["probes"].values())
        assert s["recheck"]["concepts"] == ["Species A", "Species B"]
        assert {k: len(v) for k, v in s["recheck"]["probes"].items()} == \
            {"Species A": 4, "Species B": 4}
        # 3 effort levels x 8 concepts x 2 prompts
        assert len(s["creativity"]) == 48
        levels = {it["level"] for it in s["creativity"]}
        assert levels == {"trivial", "mid", "wild"}


# ---------------------------------------------------------------------- #
# Answer mapping + scoring (the SAME scorer that grades the machine)
# ---------------------------------------------------------------------- #
class TestScoring:
    def test_build_answers_round_trip(self):
        s = build_session()
        l1 = {n: [c] * 8 for c, n in enumerate(s["meta"]["concepts"])}
        rc = {"Species A": [0] * 4, "Species B": [1] * 4}
        a = build_answers(s, l1, rc, [])
        assert set(a["probe_labels"]) == set(s["meta"]["concepts"])
        assert set(a["sequential"]) == {str(k) for k in range(1, 9)}
        # A and B appear in every stage that includes them, later concepts empty
        assert a["sequential"]["1"]["Species A"] == [0] * 4
        assert a["sequential"]["2"]["Species B"] == [1] * 4
        assert a["sequential"]["8"]["Species C"] == []
        assert a["creative_items"] == {"trivial": [], "mid": [], "wild": []}

    def test_perfect_sheet_attains_all_bars(self):
        s = build_session()
        r = grade(s, _perfect_sheet(s))
        assert r["l1_ok"] is True and r["l2_ok"] is True
        assert r["c1_ok"] is True and r["c2_ok"] is True
        assert r["c3_ok"] is True
        assert r["l1_ceiling"] == 1.0
        assert r["l2_min"] == 1.0

    def test_random_sheet_fails(self):
        s = build_session()
        rng = np.random.default_rng(0)
        l1 = {n: [int(rng.integers(0, 8)) for _ in range(8)]
              for n in s["meta"]["concepts"]}
        rc = {n: [int(rng.integers(0, 8)) for _ in range(4)]
              for n in ("Species A", "Species B")}
        a = build_answers(s, l1, rc, [])
        r = grade(s, a)
        assert r["l1_ok"] is False and r["c1_ok"] is False
        assert r["l1_ceiling"] <= 0.30

    def test_archived_real_run_reproduces_verdict(self):
        """Re-grade the first real human run (HT-RUN-001) with the current
        scorer: learning passes, creativity fails because every mid item was
        inside the taught core (valid but not novel)."""
        from pathlib import Path
        path = Path(__file__).resolve().parents[1] / "data" / \
            "human_trial_runs" / "HT-RUN-001.json"
        if not path.exists():
            pytest.skip("real run artifact not present")
        run = json.loads(path.read_text(encoding="utf-8"))
        s = build_session()
        r = grade(s, run["answers"])
        arch = run["verdict"]
        for k in ("l1_ceiling", "l2_min", "l1_ok", "l2_ok", "c1_ok",
                  "c2_ok", "c3_ok"):
            assert r[k] == arch[k], k
        # the discriminating signature: mid items valid but never novel
        assert r["l1_ok"] is True and r["l2_ok"] is True
        assert r["c1_ok"] is False and r["c3_ok"] is False
        assert r["yield"]["mid"]["novel"] == 0.0
        assert r["yield"]["mid"]["valid"] == 1.0


# ---------------------------------------------------------------------- #
# HTTP app
# ---------------------------------------------------------------------- #
def _get(port, path):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}",
                                timeout=30) as resp:
        return resp.status, resp.read()


def _post(port, path, body):
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}",
        data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


@pytest.fixture(scope="module")
def server():
    srv = make_server("127.0.0.1", 0)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield port
    srv.shutdown()


class TestHttp:
    def test_dashboard_served(self, server):
        code, html = _get(server, "/")
        assert code == 200
        assert b"Learning &amp; Creativity" in html
        assert b"/api/session" in html and b"/api/score" in html

    def test_html_data_flow_pins(self, server):
        """The page's routing/answer flow must keep the exact fixes that made
        the L1/recheck screens render: routeList iterates concepts as (name, c)
        (a swapped (c, name) makes S.l1.probes[name] an index -> undefined ->
        blank probe screen), and the recheck answer dict is initialized with a
        per-concept key (an empty dict crashes the recheck handler)."""
        _, html = _get(server, "/")
        text = html.decode("utf-8")
        assert "S.meta.concepts.forEach((name, c) => {" in text
        assert "const probes = S.l1.probes[name];" in text
        assert "RC_ANSWERS = {};\n    S.recheck.concepts.forEach(n => RC_ANSWERS[n] = []);" in text
        # the broken variants must not be present
        assert "S.meta.concepts.forEach((c,name) => {" not in text

    def test_session_endpoint(self, server):
        code, raw = _get(server, "/api/session")
        assert code == 200
        s = json.loads(raw)
        assert len(s["meta"]["concepts"]) == 8
        assert len(s["creativity"]) == 48

    def test_score_endpoint_attains_bars(self, server):
        s = json.loads(urllib.request.urlopen(
            f"http://127.0.0.1:{server}/api/session",
            timeout=30).read().decode("utf-8"))
        code, r = _post(server, "/api/score", _perfect_sheet(s))
        assert code == 200 and r["ok"] is True
        for k in ("l1_ok", "l2_ok", "c1_ok", "c2_ok", "c3_ok"):
            assert r[k] is True

    def test_bad_answers_400(self, server):
        with pytest.raises(urllib.error.HTTPError) as exc:
            _post(server, "/api/score", {"probe_labels": {}})
        assert exc.value.code == 400

    def test_unknown_path_404(self, server):
        with pytest.raises(urllib.error.HTTPError) as exc:
            _get(server, "/api/nope")
        assert exc.value.code == 404
