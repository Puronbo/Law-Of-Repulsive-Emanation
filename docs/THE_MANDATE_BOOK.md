# THE MANDATE BOOK

## A Canonical Theory of Which Work Is AI-Performable, and Which Is Text-Mandatable
### — the measure of tacit skill in fourteen professions, and what a written instruction set can and cannot drive.

> **Authority, stated plainly.** This Book is the theory behind the
> *professions & text-mandate* instrument (`professions/`, 21 pinned tests,
> `experiments/ai_performable_professions.py`, `experiments/mandate_report.py`).
> Its authority is not that it asserts an opinion about professions; it is
> that the rubric below is a **deterministic function** of a stated task
> decomposition, the decompositions are auditable `[hypothesis]` inputs, and
> the verdicts are reproduced from persisted repo assets
> (`data/ai_performable_professions_data.json`,
> `data/mandate_report_data.json`). Any reader may re-argue an input; the
> Book fixes the *logic*, and the tests keep the logic honest.

The companion manual is `docs/AI_PERFORMABLE_PROFESSIONS.md` (how to use and
reproduce the instrument); this Book is *why* the answer set is what it is.

---

## BOOK I — THE DICHOTOMY

### Ch. 1  Two kinds of knowledge

Following Polanyi — *"we know more than we can tell"* — work is split into
two kinds of knowledge, and the split is exhaustive:

| Term | Meaning | Example |
|---|---|---|
| **Knowledge work (K)** | Explicit, language-representable: recall, retrieval, reasoning, classification, composition, translation, evaluation against stated criteria | drafting a report, translating a contract, computing metrics |
| **Skill-based knowledge (S)** | Tacit, embodied, psychomotor, sensorimotor, situational — cannot be fully stated in language | physical manipulation, live-environment improvisation, face-to-face rapport, judgement under real physical risk |

**Axiom (complementarity).** Every profession is decomposed into tasks
`(name, share, k, s, gate)` with

```
k + s ≤ 1
```

within each task — knowledge and skill are *complementary* fractions of the
same effort. A task cannot demand more than all of the worker. `[hypothesis]`
The decompositions in `professions/professions_data.py` are stated estimates;
the rubric that consumes them is `[measured]` — pinned by tests.

**Definition (profession fractions).** With effort-shares normalized to sum
to 1, the profession's knowledge fraction K and skill fraction S are the
effort-weighted sums; a licensing **gate** exists iff any task carries
`gate=True` with positive share:

```
K = Σ share_i · k_i        S = Σ share_i · s_i
gate = ∃ i : gate_i and share_i > 0
```

(`professions/rubric.py`.)

**Lemma (the complementarity lock).** Since `k + s ≤ 1` per task and the
same inequality survives effort-weighting, `S > 0.10 ⇒ K < 0.90`. A
profession whose skill fraction clears a tenth **cannot** also clear nine-
tenths knowledge. This single inequality is what makes the answer set honest:
Classes A/B cannot hide material skill behind high knowledge.

---

## BOOK II — THE CLASSES

### Ch. 2  The four classes

| Class | Rule | Meaning |
|---|---|---|
| **A** | `K ≥ 0.90`, `S ≤ 0.10`, no gate | AI-performable, **no skill-based knowledge** — the answer set |
| **B** | `K ≥ 0.90`, `S ≤ 0.10`, a gate | AI-performable, but a licensed human must act |
| **C** | `K ≥ 0.50` | augment only — skill or gate is material |
| **D** | `K < 0.50` | skill-dominated |

**Theorem (the answer set is the language-artifact set).** Class A is exactly
the set of professions whose output is a language artifact and whose whole
effort decomposes into articulated knowledge work — the class of work a
language model is strongest at, and the only class where "no skill-based
knowledge" is literally satisfied. Proof is by the complementarity lock: any
profession carrying live presence, live rapport, or embodied execution has
material `s` on some task, so its S exceeds the 0.10 band and it cannot be A.

**Theorem (the gate moves a class, not a capability).** Add one task —
attestation, certification, court-swearing — to a Class A profession and the
identical reasoning drops to B: `translator` → `court translator`,
`filing analyst` → `compliance officer`. Class B is the instrument's own
statement that **capability and social license are different axes**.

---

## BOOK III — THE MEASURED VERDICT

### Ch. 3  Fourteen professions

Run `experiments/ai_performable_professions.py`; the verdict persists to
`data/ai_performable_professions_data.json` `[measured]` (regenerable,
gitignored). Class counts: **A=5, B=2, C=5, D=2.**

| Class | K | S | Gate | Profession |
|---|---|---|---|---|
| A | 0.990 | 0.010 | — | copyeditor |
| A | 0.980 | 0.020 | — | translator (document, non-certified) |
| B | 0.977 | 0.023 | ⚖ sworn attestation | translator (court, sworn) |
| A | 0.972 | 0.028 | — | technical writer |
| A | 0.970 | 0.030 | — | data analyst (reporting) |
| B | 0.967 | 0.033 | ⚖ legal certification | compliance officer (regulated filings) |
| A | 0.960 | 0.040 | — | tier-1 text support (async) |
| C | 0.800 | 0.200 | — | software engineer |
| C | 0.750 | 0.250 | — | tier-1 voice support (live) |
| C | 0.685 | 0.315 | — | psychotherapist |
| C | 0.665 | 0.335 | — | teacher |
| C | 0.645 | 0.355 | — | physician |
| D | 0.380 | 0.620 | — | surgeon |
| D | 0.350 | 0.650 | — | electrician (installation) |

(The instrument's `gate` flag marks the two Class B professions. The
`GATE_NOTES` map in `professions/professions_data.py` additionally records
the licensing *context* — e.g. physician prescribe/sign, surgeon credentialing,
psychotherapist duty of care — as a documented fact, distinct from the flag.)

### Ch. 4  Reading the verdict

- **The answer set (Class A).** copyeditor, document translator, technical
  writer, reporting analyst, async tier-1 text support. Every one has the
  same shape: *output is a language artifact, no physical presence, no live
  rapport*. The complementarity lock and the 0.10 band put them here; the
  residual 1–4% skill (editing feel, glossary instinct) is admitted by the
  band rather than hidden behind knowledge.
- **The same work, gated (Class B).** court translator (0.977) and compliance
  officer (0.967) do the same reasoning at the same K — the gate is
  social/licensing, not capability. `[honest wall]`
- **Augment only (C).** software engineer lands at **K = 0.80**, not A,
  because live troubleshooting of unfamiliar, partially-documented systems
  resists articulation (tacit residue is real but small). Teacher and
  psychotherapist lose most of their value in the *alliance* — the live
  delivery/rapport tasks carry s = 0.60. Physician is C because examination
  is s = 0.90 and diagnosis is K.
- **Skill-dominated (D).** surgeon and electrician: surgical execution
  (s = 0.80) and physical install (s = 0.95) dominate their professions.
- **The clean split (async vs live).** tier-1 text support (async) is A
  (0.960); tier-1 voice support (live) is C (0.750) — the *same knowledge
  base*, split solely on the live-rapport skill.

---

## BOOK IV — THE MANDATE

### Ch. 5  The mandate fraction (the theorem)

A profession is **text-mandatable** when a complete written instruction set —
the *mandate* — fully determines the work: an agent handed only the text can
produce the output, with no tacit, embodied, or situational knowledge to fill
in. Within each task the skill fraction `s` is exactly the part a written
mandate cannot drive, so

```
text_mandate_fraction = 1 − S
```

**Theorem.** The mandate fraction is the effort-weighted complement of the
skill fraction (`professions/mandate.py`). It is the *same number* the rubric
already computes — the mandate is not a second opinion on the profession; it
is the skill axis read backward.

### Ch. 6  The statuses

| Status | Rule | Meaning |
|---|---|---|
| `fully` | mandate ≥ 0.90, no gate | the written spec is complete (5 of 14) |
| `fully-gated` | mandate ≥ 0.90, a gate | text complete, licensed actor must act (2 of 14) |
| `partial` | mandate ≥ 0.50 | knowledge half mandatable, live/embodied half is not (5 of 14) |
| `not` | mandate < 0.50 | skill-dominated; demonstrated, not dictated (2 of 14) |

**The 5 fully-mandatable professions** (mandate = 1 − S):

| Profession | Mandate |
|---|---|
| copyeditor | 0.990 |
| translator (document, non-certified) | 0.980 |
| technical writer | 0.973 |
| data analyst (reporting) | 0.970 |
| tier-1 text support (async) | 0.960 |

**The 2 fully-gated** (same completeness, but the output is not actionable
until a credentialed human attests): court translator (0.977), compliance
officer (0.967).

**The 5 partial** (skill residue blocks a pure text hand-off): software
engineer (0.800), tier-1 voice support (0.750), psychotherapist (0.685),
teacher (0.665), physician (0.645).

**The 2 not** (text alone is not a usable spec): surgeon (0.380),
electrician (0.350).

### Ch. 7  The written mandate

For fully / fully-gated professions, `write_mandate` emits the *shape* of the
mandate — delivery, tasks, bounds, gate — the text a real spec would complete
with the actual criteria:

```
MANDATE: copyeditor
DELIVERY: a language artifact produced from this text alone.
TASKS (each fully specified by written criteria here):
  - line edit (60% of effort)
  - fact and style check (40% of effort)
BOUNDS: no physical presence; no tacit context to infer;
        every rule, style, and acceptance test stated in text.
GATE: none - the output is actionable on the strength of this text alone.
```

For partial/not professions, `write_mandate` returns None and
`residue_tasks` names the tasks whose `s > 0` blocks the text hand-off —
the Book states *which* skill blocks, not just that one does.
`[honest wall]` Generated mandates are **templates** — the shape of a text
spec, not full specification documents.

---

## BOOK V — HONEST WALLS

1. **Capability ≠ adoption.** Class A says the AI *can* do the work with no
   skill-based knowledge. It says nothing about whether a market, an employer,
   or a regulator will let it — that is exactly what the Class B gate marks.
2. **The decompositions are stated assumptions, not measurements.** The
   rubric is deterministic and pinned by tests; the `k`/`s`/`share` inputs
   are `[hypothesis]` estimates. Edit `professions/professions_data.py` and
   every verdict, artifact, CLI report, and dashboard change together.
3. **Skill is not fixed.** What is tacit today becomes articulated as
   instrumentation, video corpora, and simulators improve (e.g. teleoperation
   corpora eroding surgical S). Classes C/D state *current* articulability,
   not a permanent floor.
4. **The bands are practical, not natural.** `S ≤ 0.10` and
   `mandate ≥ 0.90` admit the residual 1–4% that makes the answer set
   non-empty; a strict "no *any* skill" reading would be S = 0 exactly. The
   thresholds are auditable constants (`FULLY = 0.90`, `PARTIAL = 0.50`),
   not hidden.

**The Book's one-sentence law:** *The measure of whether work can be done
without skill-based knowledge — and mandated through text — is the effort-
weighted tacit residue S: where it stays under a tenth and no licensed human
must act, the work is fully AI-performable; the mandate fraction 1 − S tells
exactly how much of the profession a written instruction set can drive.*

---

## Appendix — the repo assets behind this Book

| Book claim | Repo asset |
|---|---|
| the rubric and the complementarity lock | `professions/rubric.py` |
| the 14 decompositions | `professions/professions_data.py` |
| the A/B/C/D verdict | `experiments/ai_performable_professions.py` → `data/ai_performable_professions_data.json` |
| mandate fraction and statuses | `professions/mandate.py` |
| mandate report + templates | `experiments/mandate_report.py` → `data/mandate_report_data.json` |
| shared builder (CLI + dashboard + experiment) | `professions/report.py` |
| 21 tests | `tests/test_professions_rubric.py` (9), `tests/test_professions_mandate.py` (12) |
| CLI surface | `puno mandates` / `puno-mandates` (`puno_cli.py`, `puno_app/mandates_server.py`) |
| web surface | `puno_app/mandates_server.py` + `mandates.html` |
