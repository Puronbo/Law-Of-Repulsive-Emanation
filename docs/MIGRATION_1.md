# Migration Instructions: Import Hyperbolic Engine v2

Give this whole file to your coding assistant (Claude Code, Cursor, etc.)
along with the v2 files below. It tells the assistant exactly what changed,
why, and how to merge it into your existing repo safely.

## Context for the AI agent

This repo contains a hyperbolic-geometry novelty/anomaly detection
prototype (Poincare disk embeddings + topic anchors + entropy-based
quarantine). The original implementation computed gradients via manual
finite differences and processed packets one at a time in a Python loop.
It has been rewritten to use PyTorch autograd and vectorized batch
processing, with the logic split into a small `manifold` package plus
`engine.py`, and covered by unit tests.

**Your job:** merge the new files into this repo, replacing the old
engine, without breaking anything else that depends on it.

## Files being introduced

```
manifold/__init__.py     # new
manifold/poincare.py     # new — geodesic_distance, project_to_disk, riemannian_scale
engine.py                # replaces the old hyperbolic_engine.py / train.py
tests/test_engine.py     # new
requirements.txt         # merge with existing, don't overwrite
index.html               # dashboard — only replace if you haven't customized yours
```

## Step-by-step

1. **Locate the old implementation.** Search the repo for the old
   entry points — likely named something like `hyperbolic_engine.py`,
   `universal_engine.py`, or `train.py` — and any place that imports a
   class called `UniversalHyperbolicEngine` or `HyperbolicMapper`.

2. **Add the new `manifold/` package** at the repo root (or under
   `src/` if that's the existing convention — match whatever layout
   the repo already uses).

3. **Add `engine.py`.** If the repo already has a file with that name
   doing something unrelated, rename the new one (e.g. `novelty_engine.py`)
   and update the class import in step 4 accordingly.

4. **Update all call sites.** Anywhere the old code did:
   ```python
   from hyperbolic_engine import UniversalHyperbolicEngine
   engine = UniversalHyperbolicEngine()
   engine.process_stream_packet(source, content, raw_vector, entropy_risk)
   ```
   replace with:
   ```python
   from engine import NoveltyDetectionEngine, Packet
   engine = NoveltyDetectionEngine()
   verdicts = engine.evaluate_batch([Packet(source, content, tuple(raw_vector), entropy_risk)])
   ```
   Note the API is now batch-first — if the old code called
   `process_stream_packet` once per item in a loop, collect all the
   `Packet`s first and call `evaluate_batch()` once for the whole list.
   That's where the speedup comes from; calling it once per item in a
   loop still works but throws away the vectorization benefit.

5. **Delete the old finite-difference engine and the separate/broken
   PyTorch `train.py`** once call sites are updated — `engine.py` now
   covers both roles (JSON export via `export_manifest()` and direct
   tensor training, since the underlying weights are just
   `Packet.vector` tensors run through the same `manifold` math).

6. **Merge `requirements.txt`.** Add `torch>=2.0` and `pytest>=7.0` to
   the existing file rather than overwriting it — check for version
   conflicts with anything else in the repo that pins `torch`.

7. **Drop in `tests/test_engine.py`** next to the repo's existing test
   directory (adjust the `sys.path.insert` at the top if the repo uses
   a proper installed package instead of path hacking).

8. **Only replace `index.html`** if it hasn't been customized — diff it
   against the existing dashboard first. It expects to `fetch()` a
   `web_data.json` in the same directory it's served from.

## Verification checklist (run these after merging)

```bash
pip install -r requirements.txt

# 1. Engine runs and produces sane output
python3 engine.py
# expect: KNOWN verdicts at low-to-mid radius for coherent content,
#         ANOMALY verdicts at r >= 0.85 for high-entropy content

# 2. Tests pass
python3 -m pytest tests/ -v
# expect: 7 passed

# 3. Old and new radii match for the same input (regression check)
# — if you have logged output from the old engine for the same demo
# packets, radii should match to ~3 decimal places; the math is
# unchanged, only the gradient computation method is.
```

## Things the agent should flag back to you, not silently resolve

- Any other module in the repo importing `UniversalHyperbolicEngine`,
  `HyperbolicMapper`, or calling `process_stream_packet` directly —
  these need their call sites updated per step 4, and the agent should
  list every file it changed rather than doing a silent find-replace.
- If the repo's `web_data.json` schema is consumed by anything besides
  `index.html` (e.g. another service), confirm the field names still
  match — `export_manifest()` produces the same shape (`id`, `label`,
  `x`, `y`, `type`), with one addition: each non-anchor record now also
  includes `"source"` and `"radius"`.
- If CI pins a specific PyTorch version incompatible with `torch>=2.0`,
  don't force-upgrade it — report the conflict.
