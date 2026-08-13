# AI-Performable Professions — Test Without Skill-Based Knowledge

**Purpose:** Answer the question *"which professions can be done without any
use of skill-based knowledge, so that LLMs / AI models can do them?"* The
answer is delivered as an auditable test instrument, not an opinion: a rubric
(`professions/rubric.py`) classifies a profession from its stated task
decomposition, a pinned test suite (`tests/test_professions_rubric.py`, 9
tests) locks the classification logic, and a verdict runner
(`experiments/ai_performable_professions.py`) scores a 14-profession dataset
into `data/ai_performable_professions_data.json` (gitignored, regenerable).

**Method date:** 2026-08-13.

---

## 0. Definitions (the rubric)

Following Polanyi (*"we know more than we can tell"*), work is split into two
kinds of knowledge:

| Term | Meaning | Example |
|---|---|---|
| **Knowledge work (K)** | Explicit, language-representable: recall, retrieval, reasoning, classification, composition, translation, evaluation against stated criteria | drafting a report, translating a contract, computing metrics |
| **Skill-based knowledge (S)** | Tacit, embodied, psychomotor, sensorimotor, situational — cannot be fully stated in language | physical manipulation, live-environment improvisation, face-to-face rapport, judgement under real physical risk |
| **Licensing gate** | The output is only actionable when signed/acted/held by a credentialed or situated human | diagnosis, legal filing, sworn attestation, prescription |

Every profession is decomposed into tasks `(name, share, k, s, gate)` with
`k + s ≤ 1`; the profession's knowledge fraction `K` and skill fraction `S`
are effort-weighted sums. Classification:

| Class | Rule | Meaning |
|---|---|---|
| **A** | `K ≥ 0.90`, `S ≤ 0.10`, no gate | AI-performable, **no skill-based knowledge** — the answer set |
| **B** | `K ≥ 0.90`, `S ≤ 0.10`, gate | AI-performable, but a licensed human must act |
| **C** | `K ≥ 0.50` | augment only — skill or gate is material |
| **D** | `K < 0.50` | skill-dominated |

Note `k + s ≤ 1` encodes that within a task, knowledge and skill are
complementary — so `S > 0.10` forces `K < 0.90`, and Classes A/B cannot hide
material skill behind high knowledge. `[hypothesis]` The rubric itself is
`[measured]` (pinned by tests); every profession decomposition is a stated
assumption, auditable and re-arguable.

---

## 1. Verdict (14 professions)

Run: `python experiments/ai_performable_professions.py` — artifact
`data/ai_performable_professions_data.json`.

| Class | K | S | Gate | Profession |
|---|---|---|---|---|
| A | 0.990 | 0.010 | — | copyeditor |
| A | 0.980 | 0.020 | — | translator (document, non-certified) |
| B | 0.977 | 0.023 | ⚖ court attestation | translator (court, sworn) |
| A | 0.972 | 0.028 | — | technical writer |
| A | 0.970 | 0.030 | — | data analyst (reporting) |
| B | 0.967 | 0.033 | ⚖ legal certification | compliance officer (regulated filings) |
| A | 0.960 | 0.040 | — | tier-1 text support (async) |
| C | 0.800 | 0.200 | — | software engineer |
| C | 0.750 | 0.250 | — | tier-1 voice support (live) |
| C | 0.685 | 0.315 | ⚖ licensed practice | psychotherapist |
| C | 0.665 | 0.335 | — | teacher |
| C | 0.645 | 0.355 | ⚖ prescribe/sign | physician |
| D | 0.380 | 0.620 | ⚖ licensure | surgeon |
| D | 0.350 | 0.650 | — | electrician (installation) |

**Class counts:** A=5, B=2, C=5, D=2.

### 1.1 The answer set (Class A — no skill-based knowledge, no gate)

1. **copyeditor** — line editing and fact/style checking is 99% articulated
   criteria work.
2. **translator (document, non-certified)** — transfer between language
   artifacts; no physical presence.
3. **technical writer** — research, draft, revise to stated criteria.
4. **data analyst (reporting)** — query, transform, compute, narrate.
5. **tier-1 text support (async)** — resolve from a knowledge base, escalate;
   asynchronous so no live rapport skill is required.

The common shape is unmistakable: **the output is a language artifact and the
entire effort decomposes into articulated knowledge work.** This is precisely
the class of work a language model is strongest at, and the only class where
"no skill-based knowledge" is literally satisfied.

### 1.2 The same work, gated (Class B)

Add one duty — attestation, certification, court-swearing — and the identical
work drops a class: *translator* → *court translator*, *filing analyst* →
*compliance officer*. The AI still does all the reasoning; the gate is
**social/licensing, not capability**. `[honest wall]`

### 1.3 Everything else (C/D)

- **software engineer lands at K = 0.80**, not A, because live
  troubleshooting of unfamiliar, partially-documented systems resists
  articulation — the tacit residue is real but small.
- **teacher and psychotherapist** sit in C: design/assessment is knowledge
  work, but the live alliance and classroom delivery are irreducibly
  embodied.
- **surgeon and electrician** are D: psychomotor execution dominates.
- **tier-1 voice support** (live) is C where tier-1 text support (async) is A
  — the *same knowledge base*, split solely on the live-rapport skill.

---

## 2. Honest walls

1. **Capability ≠ adoption.** Class A says the AI *can* do the work with no
   skill-based knowledge; it says nothing about whether a market, an employer,
   or a regulator will let it. That is exactly what Class B's gate exists to
   mark, and Class B professions are the boundary cases.
2. **The decompositions are stated assumptions, not measurements.** The rubric
   is deterministic and pinned by tests, but `k`/`s`/`share` values are
   `[hypothesis]` estimates. Re-run the verdicts by editing
   `experiments/ai_performable_professions.py`; the tests keep the *logic*
   honest even though the *inputs* are judgment.
3. **Skill is not fixed.** What is tacit today becomes articulated as
   instrumentation, video corpora, and simulators improve (e.g. teleoperation
   corpora eroding surgical S). Class C/D are statements about *current*
   articulability, not a permanent floor.
4. **The S ≤ 0.10 band is a practical choice.** "No *any* skill" would be
   S = 0 exactly; the band admits the residual 1–4% (editing feel, glossary
   instinct) that makes the answer set non-empty in practice while keeping the
   threshold auditable.

---

## 3. How to reproduce

```
python -m pytest tests/test_professions_rubric.py -q     # 9 tests, locks rubric logic
python experiments/ai_performable_professions.py          # writes data/ai_performable_professions_data.json
```

The package is registered in `pyproject.toml` (`packages` includes
`professions`). `data/*.json` is gitignored by convention — the verdict
artifact is regenerable, never committed.
