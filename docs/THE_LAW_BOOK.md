# THE LAW BOOK

## A Canonical Theory of Laws — Descriptive and Prescriptive — and of Which Work an Accurate Agent Can Administer
### — the clock-test canon for what is and is not a law, the mandate instrument for the law of man, and the residue that stays human.

> **Authority, stated plainly.** This Book is the theory of *law* in both
> senses, built entirely from repo assets. **Descriptive law** — what the
> repository has measured to be regular — is judged by the clock-test canon
> (T59, T61): laws live in invariants, conventions die under benign
> re-encoding. **Prescriptive law of man** — constitutions, statutes, codes —
> is read through the professions & text-mandate instrument
> (`professions/`, 21 pinned tests): it is the largest text mandate ever
> written, and the mandate fraction `1 − S` tells how much of it an accurate
> agent can administer. Its authority is not that it asserts an opinion about
> laws or jobs; it is that every verdict below is either `[measured]` from a
> persisted repo asset, `[hypothesis]` and so tagged, or `[honest wall]`
> outside the measure entirely. Any reader may re-argue an input; the Book
> fixes the logic.

The companion manuals are `docs/UNIVERSAL_CALENDAR.md`,
`docs/AI_PERFORMABLE_PROFESSIONS.md`, and the two prior Books
(`docs/THE_DAY_BOOK.md`, `docs/THE_MANDATE_BOOK.md`). This Book is the
crown they converge on: *what can be measured, what survives being measured,
and who administers the rest.*

---

## BOOK I — THE TWO SENSES

### Ch. 1  Two kinds of law

| Term | Meaning | Test | Example in this repo |
|---|---|---|---|
| **Descriptive law** | a regularity of the world, *discovered* | survives benign re-encoding (T59/T61) | the mirror-fold theorem, the prime count |
| **Prescriptive law of man** | a regularity of a society, *decreed* | is a text mandate (mandate fraction) | a constitution, a statute, a regulation |

The two are inverse in a precise way. A descriptive law is an invariant we
*found*; a prescriptive law is a convention we *chose to hold invariant*.
The clock test asks whether a claimed regularity is invariant under
re-encoding — that is the measure of descriptive law-ness. The mandate
instrument asks whether a written instruction set fully determines the work —
that is the measure of how much of a prescriptive law an agent can apply
without filling in tacit knowledge.

**Axiom (administration).** To *administer* a law is to map a fact situation
to a rule and produce the output the rule commands: a decision, a number, an
action, a record. Administration is text work in its whole shape — read the
rule, read the facts, apply, write. Whatever part of that is not text work is
the residue; the residue is where humans remain.

---

## BOOK II — DESCRIPTIVE LAW: WHAT IS AND IS NOT A LAW

### Ch. 2  The clock-test canon (measured)

**Canon (laws live in invariants, not conventions).** Two measured tests
define the canon. **T59 (the clock test, `clock_test.py`):** a logistic
model on calendar features — weekday/month/day/year%4 of the physical date —
"nails" the law `y = (N mod 7 == 3)` at balanced accuracy **1.0000** at the
true epoch `e0`; re-index the *same physical dates* by the 15-day
Julian/Gregorian gap and the same model drops to **0.4167** — below chance,
anti-correlated, so the alignment was pure convention. The intrinsic
arithmetic features (N mod 2/3/5/7) score 1.0000 at *both* epochs.

**T61 (the rotation test, `rotation_test.py`):** the net's law is its
relative geometry — an orthogonal rotation (a benign re-encoding) preserves
the top-8 neighbor structure **exactly** (overlap 1.0000, similarity
correlation 1.0000) even though every coordinate changes (max |Qx−x| =
0.745); a *structure-breaking* relabeling (per-coordinate abs) drops the
overlap to 0.426 — still 6.5× above chance (0.065), a sign-fold, not
collapse. The benign re-encoding separates the invariant from the
convention with a single number:

```
law-ness(e0)      = 1.0000      [measured]   (T59)
law-ness(e0+15)   = 0.4167      [measured]   (T59)
rotation overlap  = 1.0000      [measured]   (T61)
```

**Theorem (the canon's judgment rule).** A claim whose accuracy survives
benign re-encoding is candidate law; a claim that carried at 1.000 and
collapses to ~0.417 under re-encoding was never law — it was a convention
reading the clock. T61 supplies the positive half: the *relative geometry*
is the invariant, and it survives rotation exactly. `[honest wall]` T61
carries a correction of its own — abs() is a sign-fold at 0.426, not
chance, so "collapse toward chance" overstates it.

### Ch. 3  The measured ledger of descriptive claims

The repository has applied the canon to its own claims. The honest record:

**Law-grade (derived or exactly measured, `[measured]`):**

| Claim | Finding |
|---|---|
| Mirror fold = viscosity solution (T58/T63/T64) | unique solution of \|r′\|=a with C0 at both ends; cut locus EXACT; swept area `2a²TH³/6` EXACT — derived, not fitted |
| Prime count (T62) | π exact at every chain point; π(943901200001) = 35,575,526,191; endpoint prime |
| Cusp isometry (T39) | energy CV 3e-15; step ratio = φ exactly; w-plane R² = 1.0; T-sym err 0 |
| C0 conservation on the flow | H = C0 constant on the conservative flow; C_current = D/C0 is a reading, never a drift in C0 |
| Structural regularities (T55 family, T72, T74/T75, bazaar, ledger) | SUPPORTED over seeds 42/11/7 and real TCP processes, with the stated honest walls — real, but bounded to their regime |

**Nonsense-grade (REFUTED — the canon killed them):**

| Claim | Verdict |
|---|---|
| Golden spiral on a disk | REFUTED: 42.1°/29.2° turning vs golden 137.5°, pseudo-energy drift 1.00/11.81 |
| Frictionless fib-squares | REFUTED: 90° turning is a construction artifact, drift 0.96, escapes disk |
| Golden fold as a chain law (C2) | REFUTED: the retrace chain is **1/4 golden rungs**; the φ² rung is a coincidence-scale hit, P(≥1) = 0.036 |
| C0 geodesic blowups (metric_comparison, c0_cusp_flow) | REFUTED: both metrics blow up from a "stable" start — Poincare NaN, cusp ~2e13 (`metric_comparison`); repeated at ~2.7e23 (`c0_cusp_flow`) |
| Arithmetic Bekenstein shift | REFUTED and **withdrawn from the PAPER** (2026-08-04); the causal null (2026-08-08): positional, not primality |
| T65 §10.1 four-pack | MIXED, mostly REFUTED: knob inert (τ = 1.4272 identical across all curiosity_drive); no fixed point |
| Wheeler–DeWitt selection | constraint selects nothing — unshifted empty, shifted is the C₀ law relabeled |
| Polysphere learned-truths routing | NOT SUPPORTED: 0.483 vs 1.000 |

**The signature of nonsense, stated once.** A claim is nonsense by this
canon if (i) it dies under a benign re-encoding, (ii) it is a single-run
coincidence that a magnitude-matched null expects (the golden-rung test), or
(iii) it is an analogy with no falsifiable content (the entropy↔folding
mapping is "not falsifiable as stated" — the repo keeps it as analogy, not
law). `[honest wall]` Refutation is provisional: a better experiment can
resurrect a dead claim, but the dead claim's own file must then say so.

---

## BOOK III — PRESCRIPTIVE LAW OF MAN: THE CONSTITUTION AS MANDATE

### Ch. 4  The text mandate, at the scale of a constitution

A constitution is the largest written instruction set ever made. The mandate
instrument reads it directly:

```
text_mandate_fraction = 1 − S          [measured, professions/mandate.py]
```

For a profession, S is the effort-weighted tacit residue. For a legal
system, S is the part of adjudication a written rule cannot drive: equity,
discretion, credibility of live witnesses, purpose-weighing, the resolution
of deliberate vagueness. The constitution's own open-texture words — *due
process, equal protection, cruel and unusual, free speech* — are anti-mandate
devices: they instruct a *person* to judge, by design.

**Theorem (the constitution is deliberately incomplete).** A complete written
instruction set that fully determines every legal outcome is not a
constitution — it is a table. Open texture is a feature, not a gap in the
instrument: fully specifying "due process" would change the constitution.
Therefore the constitution's own structure guarantees a nonzero residue S:
the mandate fraction of the *judgment layer* is strictly less than 1 by
design. `[honest wall]`

### Ch. 5  What the law's administration layer is (measured classes)

The instrument's 14-profession verdict (`data/ai_performable_professions_data.json`,
`data/mandate_report_data.json`) already measures the professions that *are*
the law's administration: **A = 5** (copyeditor 0.990, document translator
0.980, technical writer 0.973, reporting analyst 0.970, async text support
0.960 — K ≥ 0.90, S ≤ 0.10, no gate), **B = 2** (court translator 0.977,
compliance officer 0.967 — same completeness, a credentialed human must
attest), **C = 5**, **D = 2**.

**Theorem (the administration layer is Class A).** The work of applying a
settled rule to a record — docketing, citation, compliance checking,
mechanical syllogism, drafting a decision that cites the rule — decomposes
into the language-artifact professions the instrument already measured as
fully text-mandatable. The complementarity lock makes the claim honest:

```
k + s ≤ 1  ⇒  S > 0.10  ⇒  K < 0.90
```

**Lemma (the gate moves a class, not a capability).** Add attestation to a
Class A profession and it drops to B — the instrument's own finding
(translator → court translator; filing analyst → compliance officer). The
law is full of gates by construction: notarization, court filing, sworn
testimony, licensing signatures. The machine writes the text; the human
stands. This is not a capability gap — it is a standing gap.

The mandate for the B-class legal work has the same shape the instrument
emits, with the gate marking where a human must stand:

```
MANDATE: regulated-filing compliance check
DELIVERY: a compliance determination produced from this text alone.
TASKS (each fully specified by written criteria here):
  - fetch the filing and the governing regulation (35% of effort)
  - map each required field to its rule (45% of effort)
  - emit a cited pass/fail and the exact non-conformance text (20%)
BOUNDS: no physical presence; no tacit context to infer;
        the regulation, the form, and the acceptance test are the text.
GATE: the filing is not actionable until a credentialed officer attests.
```

`[honest wall]` Like the mandate book's copyeditor template, this is the
shape of a text spec, not a full specification document.

### Ch. 6  Open texture and the judgment layer

The complementarity lock applied to law: **the judgment layer carries S by
design.** Where the rule is bright-line, the mandate fraction is ~1 and an
accurate agent administers exactly. Where the rule is a balancing test, a
credibility call, or an open-textured phrase, S > 0.10 and the work is
partial — augment, not replace. `[hypothesis]` A full legal-system
decomposition (statute-to-task, `s` per task) is not in the repo's measured
14; the pattern is the same measured pattern of the C-class professions —
live-voice support (0.750), psychotherapist (0.685), teacher (0.665),
physician (0.645) — transplanted to adjudication. `[honest wall]` This
transplant is stated as an application of the instrument, not a measured
verdict.

### Ch. 7  The three functions of law

A legal system is not one act but three functions, and the mandate
instrument classifies them separately:

| Function | What the agent can run (A) | What stays human | Basis `[measured]` |
|---|---|---|---|
| **Legislation** | drafting statutes, regulations, and rules — the technical-writer class of work | enactment: the representative's vote — consent attaches to a person | drafting ≈ A (0.973–0.990); enacting = standing, outside the measure |
| **Adjudication** | settled-rule application: docketing, citation, compliance checks, mechanical syllogism, drafting the decision | discretion, equity, credibility, open texture; and the judge's signature | bright-line ≈ A; open texture = C (Ch. 6); signing = B (gate) |
| **Enforcement** | automated rules: the bazaar removes spam, suspends by standing, finalizes the ledger | authorization (the warrant, the court order) and the physical act (restraint, arrest, service) | rules-in-code = A; authorization = B; physical act = D-shape |

**Theorem (enforcement is the repo's home turf).** The bazaar and the ledger
already *enforce* community rules in code — top-K bot-spam drops 0.75→0.00
under the karma-free + tag-to-remove rule, the 9-guardian quorum collapses
wrong-removal 0.20→0.003 while spam removal stays 0.91, and a fabricated
brigade against a standing author is REJECTED where a central 3-flag rule
would remove. Enforcement whose rules are code is Class A today. What stays
human is not the enforcement but its two ends: the *authorization* (the
gate — a person must warrant force) and the *physical act* (the D-shape:
restraint, arrest, service). The measured split of the 14 names both ends:
the machine enforces the text; the human authorizes, and the human grips.

### Ch. 8  The doctrines, read by the instruments

The law's central doctrines are not abstract — each has a measurable
mechanical core, and the repo's instruments have already measured that
core. `[hypothesis]` Each row applies a `[measured]` repo result to a
doctrine: the numbers are measured; the mapping is the hypothesis.

| Doctrine | The legal idea | The measured machine | The number |
|---|---|---|---|
| **Stare decisis (precedent)** | past decisions bind; apply the nearest case | exact retrieval + routing (T67) | grid kNN == brute force on 3 seeds; n = 100k routed at 10.35 s/step vs 160 GB all-pairs |
| **Conflict of laws / choice of law** | one act, one governing frame — never two | frame discipline (T55e MIX) | MIX collapses old-routing 0.061 / all 0.305 — never mix frames |
| **Retroactivity / ex post facto** | a rule must not re-index past acts | re-encoding (T59) | law-ness 1.0000 → 0.4167 when the rights-calendar is re-indexed |
| **Evidence / records** | the case rests on authenticated records | ledger integrity + anomaly (T70, T55g) | tamper-evident at the flipped seq; survives 50% node loss; A1–A3 SUPPORTED |
| **Judicial review / appeal** | error correction above the trier | quorum review (bazaar) | wrong-removal 0.20 → 0.003 while true removals stay 0.91 |
| **Credibility / demeanor** | the witness's live truthfulness | the live-residue split (mandate) | live voice S = 0.25 vs async text S = 0.04 — demeanor resists articulation |

**Theorem (the doctrines are measurement claims).** Each doctrine is, at its
core, an instruction about *encoding*: precedent says the encoding of past
decisions must bind the present; conflict-of-laws says exactly one frame may
encode an act; retroactivity says the temporal encoding must not move after
the act; evidence says the record's encoding must be authenticated. The
canon's three measured verdicts — re-encoding collapses conventions (T59,
1.0000 → 0.4167), frame-mixing collapses routing (T55e, 0.061/0.305), and
retrieval survives at scale (T67) — are therefore not analogies but the
*same operations* the doctrines regulate, measured. `[honest wall]` The
mapping is a reading, not a proof: a doctrine is also a value choice (why
retroactivity is forbidden), and values are not measured here — only the
mechanical core is.

### Ch. 9  The jurists, read by the canon

The book has used the jurists' own vocabulary — "open texture" is Hart's,
"validity" is Kelsen's, "hard cases" is Dworkin's. Good faith requires
acknowledging the source, and then doing what the book does everywhere:
reading the tradition through the instruments. `[hypothesis]` Each row maps
a jurist's idea to a `[measured]` repo instrument: the numbers are measured;
the mapping is the hypothesis.

1. **Hart: the rule of recognition.** Hart's claim is that a legal system
   exists where officials converge on a rule of recognition — the criterion
   that identifies valid law. The Book's canon *is* a rule of recognition
   made operational: a descriptive law is valid iff it survives benign
   re-encoding (Ch. 2 — T59 1.0000 → 0.4167 under re-indexing; T61 rotation
   1.0000); a prescriptive law is valid iff it is a text mandate (Ch. 4).
   The canon does not replace Hart's question; it answers it with an
   instrument — the recognition rule is no longer a social fact to be
   asserted, but a number to be measured.
2. **Hart: primary and secondary rules.** Primary rules impose duties;
   secondary rules confer powers — to legislate, to adjudicate, to amend.
   Map: primary rules = the mandate's operative text (Ch. 4); secondary
   rules = the gate (who may sign, Ch. 5), the standing layer (who may
   judge, Ch. 6), and the amendment protocol (Ch. 10). The bazaar's quorum
   is a secondary rule instrumented: the 9-guardian quorum lowers
   wrong-removal 0.20 → 0.003 while true removals stay 0.91 — the rule
   *about who may remove* is itself a measured machine.
3. **Dworkin: hard cases and principles.** Dworkin's hard cases are those
   the settled rules do not decide — Ch. 6's open texture by name. His
   answer, the judge who reads principles into the best justification, is
   the judgment layer. The Book's claim is narrower: the agent routes the
   hard case to the human (T74's C1 criterion), and the human decides.
   Where Dworkin gave one judge's conscience, the Book gives a measured
   division of labor. `[honest wall]` The Book does not answer Dworkin; it
   partitions the question.
4. **Fuller: the eight canons of legality.** Fuller's inner morality of law:
   a functioning law must be general, public, not retroactive, clear,
   non-contradictory, possible to obey, stable, and consistently
   administered. Here the repo is not analogizing: five of the eight are
   testable against a text mandate today. **Non-retroactivity** is T59
   (re-index the rule-calendar and measure survival — 1.0000 → 0.4167,
   below chance at e0+15). **Consistency of administration** is the
   bazaar's persistence (the quorum holds under repeated abuse).
   **Clarity** is the frame-mixing test (T55e MIX collapses 0.061/0.305
   when frames are mixed). **Publicity** is the ledger (T70: every
   rule-change is an auditable record). **Possibility of obedience** is the
   mandate's own residue declaration (Ch. 5, k + s ≤ 1). Fuller's canons
   are not a metaphor for this repository — they are a checklist, and the
   checklist has instrumented rows. `[hypothesis]` Each canon is a proposed
   benchmark against a real text; the instruments already run.

**Theorem (the jurists were writing measurements).** The great disputes of
jurisprudence are, at their mechanical core, disputes about *encoding*:
recognition is the criterion for which encodings count as law; secondary
rules are the encodings about who may change encodings; hard cases are the
encoding collisions the settled text does not resolve; Fuller's canons are
a checklist of encoding properties. The repo has measured exactly these
operations. What the Book adds is not a new jurisprudence but the
observation that the old one has testable claims. `[honest wall]`
Jurisprudence is also values — why retroactivity is forbidden, why rules
bind — and values are not measured here (Ch. 8's wall, restated).

### Ch. 10  The law of the lawgiver

The book has treated the mandate as given. A constitution is not static; it
carries its own amendment rules, and no book on machine-administered law
can omit the law of the lawgiver: who may amend, and who adjudicates
amendments.

1. **The mandate is a file.** In this repository the prescriptive
   instruments (the mandates of THE_MANDATE_BOOK) are versioned text files.
   Amendment is a change to a file; the amendment trail is the git history
   — replayable, attributable, auditable — and the ledger (T70) is the
   tamper-evident record layer beneath (tamper-evidence at the flipped seq,
   bit-identical resync after a stateless restart). `[measured]` The
   book's own constitution-analog is amended exactly this way: a commit,
   signed by a human, reviewed before merge.
2. **The amendment gate is standing, not skill.** Who may amend is not a
   capability question; it is the gate (Ch. 5). The Book's rule, consistent
   with Ch. 7's three functions: the agent drafts amendments and tests
   them; a credentialed human signs them. The agent never self-amends,
   because amendment is legislation, and legislation is the one function
   the Book never grants the agent alone — the mandate is the standing
   layer's authority. `[hypothesis]` A proposal, not a measured result.
3. **The canon is the amendment test.** The repo's precedent: a rule is law
   only insofar as it survives benign re-encoding. An amendment can be
   tested *before adoption*: re-index the amended rule's calendar, rotate
   its frame, and measure whether the amended rule still routes (T59, T61).
   An amendment whose law-ness collapses under its own re-encoding is one
   whose text is anti-correlated with itself — a defect the canon names
   before a human signs it. `[hypothesis]` The canon as a pre-signing gate;
   the instruments already run.
4. **Amendment is not administration.** The distinction is the book's spine:
   the agent administers the current mandate (rules-in-code — the bazaar
   and ledger already run them); it does not amend it. The lawgiver's law
   is therefore the deepest residue: open texture ends where the text ends
   (Ch. 6), and amendment begins. Who holds the pen is the constitution's
   final gate. `[honest wall]` This is the book's own proposal, offered
   plainly: no instrument measures consent, and amendment without consent
   is the Book's definition of tyranny by text.

---

## BOOK IV — ADMINISTRATION: WHAT AN ACCURATE AGENT CAN RUN

### Ch. 11  What is administrable (measured in the repo)

The repository already runs machine-administered rule systems, each with its
measured results:

| Institution | Instrument | Measured |
|---|---|---|
| **Governance / moderation** | bazaar hybrid + bazaar_net (quorum, standing gates) | reason-tagged downvotes raise a brigade 2.5× (S₅₀ 8→20); karma-free + tag-to-remove drops top-K bot-spam 0.75→0.00; 9-guardian quorum collapses wrong-removal 0.20→0.003 while spam removal stays 0.91; fabricated brigade on a standing author REJECTED where a central 3-flag rule removes |
| **Records / property** | ledger hash-chains (T70) | tamper-evident at the flipped seq; survives 50% node loss; bit-identical archive after a stateless restart |
| **Commerce / fraud / security** | decentral_net anomaly (T55g), internet flow (T72), polysphere MNIST | A1–A3 SUPPORTED; +7.8% spacing after 20% kill + heal; OOD/anomaly gap on real MNIST 0.663 (in-distribution 0.877 vs OOD 0.214, `data/polysphere_mnist_data.json`) |
| **Schools / assessment** | learning-creativity test (T74), learning-curve scale (T75) | held-out probe ≥0.90 at 40 exemplars; first-taught concepts keep ≥0.92 (no forgetting); novel-but-valid yield ≥0.24; creative yield interior-peaked over mutation size |
| **Time / measure** | universal calendar | every layer exact on one untruncated day axis; 27 tests |
| **Production** | packaging line (servo, quorum, energy) | IEC 61131-3:2025 ST + Python mirror pinned test-for-test |

**Theorem (the text layer of any institution is administrable).** The
governance, records, commerce, assessment, and time instruments above all
share one shape: rule in text, fact in a record, output in text or number,
residue measured and declared. Any institution's text layer has the same
shape, so the same instrument applies: **an accurate agent can administer
the text layer of any institution, and the code layer of any system whose
rules can be encoded.** This is the honest generalization of the Class A
finding — and the honest limit of it is Ch. 12.

### Ch. 12  What is not administrable

Two independent reasons close "everything," and the repo measured both.

1. **The complementarity lock (measured).** Any task with tacit residue
   S > 0.10 blocks a pure text administration. The measured split of 14
   professions — 5 fully, 2 fully-gated, 5 partial, 2 not — is the number.
2. **Open texture (by design).** The judgment layer of a constitution is
   deliberately incomplete. The bazaar experiment shows the boundary even in
   machine governance: the *rules* are code, but the 9-guardian quorum is
   *humans voting* — the machine counts, the humans stand.
3. **The legitimacy wall (outside the measure).** `[honest wall]` A
   constitution administered by an agent is not a constitution people
   consented to. Capability in text ≠ adoption; the mandate book's first
   honest wall is this Book's third. Legitimacy is not a text property and
   no instrument in the repo measures it.

### Ch. 13  Contracts and private law

Contracts are the private-law layer: a law the parties write for themselves.
They are the most administrable text in the legal stack — boilerplate,
standard forms, and clause libraries decompose into the measured
language-artifact set (copyeditor 0.990, technical writer 0.973, reporting
analyst 0.970) — and their administration is the same Class A shape: rule
(the clause) in text, fact (the record) in a record, output (the
application) in text. Standard-form contracts are already administered by
code at scale.

The repository has already done legal-text work of this layer as a
demonstrated surface:

- `docs/US7284987B2_ANALYSIS.md` — prior-art analysis of an issued patent,
  status-labelled.
- `docs/AUTO_PACKAGING_PATENTS.md` — patent/standards survey mapping
  US9718570B1 and US10532842 to the packaging line's stations, with an
  honest-wall freedom-to-operate note.

Both are the administration layer working today, in this repository: rule
(claims, statutes, standards) in text, fact (a design) in a record, output
(an analysis) in text, residue declared. `[honest wall]` They are analyses,
not filings — none is licensed legal practice, and the gate (Ch. 5) is
exactly what separates the two.

### Ch. 14  The measurement frontier

What else can be measured? The canon generates its own next instruments;
all four below are implied by what the repo already runs, and each is
stated with its status.

1. **The institutional clock test** `[hypothesis — proposed, not run]`. The
   canon applied to institutions themselves. T59 re-indexed the calendar's
   epoch and measured law-ness collapse 1.0000 → 0.4167; apply the same
   benign re-encoding to an institution's *rule-calendar* — re-index the
   dates, frames, and headings under which a regulator, a school, or a
   court issues its decisions — and measure whether the outputs survive. An
   institution that administers by convention collapses under the
   re-encoding; one that administers by invariant survives. The measurement
   is the canon's own single number: law-ness(e0) vs law-ness(e0+15). This
   is the Book's central proposal: the clock-test canon, built to judge
   physical claims, is itself a lawfulness meter for the institutions of
   man.
2. **The conditions of adoption** `[measured design space]`. Consent is
   outside the measure, but the repo measures the design features that make
   machine-administered law *eligible* for consent: auditability (the
   ledger is tamper-evident at the flipped seq and survives 50% node loss),
   error-check quorums (9-guardian wrong-removal 0.20→0.003 while spam
   removal stays 0.91), and transparency (standing-gated moderation,
   reason-tagged votes). The wall is not that adoption is impossible; it is
   that adoption has a measured, non-empty design space.
3. **The human trial bridge** `[measured — the repo runs it]`. The
   repository already turns "can it be administered" into a demonstrated
   property: `docs/HUMAN_TRIAL_INSTRUMENT.md` +
   `experiments/human_trial_pilot.py` run the T74/T75 rubric with human
   participants, and the first real human run
   (`data/human_trial_runs/HT-RUN-001.json`) graded the developer with the
   *same* `score_participant()` code that grades the machine — L1 ceiling
   0.953 and L2 no-forgetting 1.0 passed; the creativity bars correctly
   rejected the profile (mid-effort items valid but not novel). The same
   protocol, handed a mandate text instead of a species set, is the
   empirical test of text-mandatability: give the agent the mandate and
   held-out fact patterns, and measure whether it routes novel-but-valid
   cases to the correct rule (T74's C1 criterion). `[honest wall]` The
   pilot participants are simulated archetypes; the bridge proves the bars
   are attainable and discriminating, not that any agent passes them.
4. **The doctrine experiments** `[hypothesis — runnable with the repo's own
   machinery]`. The Ch. 8 mappings are readings; each can be *made* a
   measurement with instruments that already exist: a **precedent-retrieval
   benchmark** (does the T67 index, over a case corpus, retrieve the
   controlling precedent for held-out fact patterns at the T74 C1 bar?); a
   **retroactivity audit** (re-index a decision corpus's dates and measure
   whether rule-routing survives — the institutional clock test, item 1, on
   real records); a **frame-mixing corpus test** (route the same facts
   through two legal frames and measure the T55e collapse on the text
   corpus). All three are the existing experiments pointed at legal data —
   the Book's proposals become the repo's next SUPPORTED / REFUTED rows.

---

## BOOK V — THE JOBS HUMANS WOULD PARTAKE THAT THE AGENT CANNOT

### Ch. 15  The residue is the human's job

By the axioms, the work an accurate agent cannot administer is exactly the
complement of its mandate: **S** (tacit skill residue), the **gate**
(licensed standing), and the **legitimacy layer** (consent and
accountability, outside the measure). The jobs that remain are therefore not
an arbitrary list — they are the measured residue, named task by task.

### Ch. 16  The measured residue (the 9 of the 14 professions that are not Class A)

| Class | K | S | Profession | Why it stays human `[measured]` |
|---|---|---|---|---|
| B | 0.977 | 0.023 | court translator (sworn) | text complete — a sworn human must attest |
| B | 0.967 | 0.033 | compliance officer (regulated filings) | text complete — legal certification must act |
| C | 0.800 | 0.200 | software engineer | live troubleshooting of unfamiliar, partially-documented systems resists articulation |
| C | 0.750 | 0.250 | live voice support | live rapport and real-time de-escalation carry s |
| C | 0.685 | 0.315 | psychotherapist | the alliance — delivery/rapport tasks carry s = 0.60 |
| C | 0.665 | 0.335 | teacher | the live classroom is an embodied, situational environment |
| C | 0.645 | 0.355 | physician | examination is s = 0.90; diagnosis is K |
| D | 0.380 | 0.620 | surgeon | surgical execution (s = 0.80) dominates the profession |
| D | 0.350 | 0.650 | electrician (installation) | physical install (s = 0.95) dominates the profession |

### Ch. 17  The principled residue beyond the fourteen

The same instrument, extended to the unmeasured professions, gives the shape
of the human economy the agent leaves standing — `[hypothesis]` applications
of the measured classes, not measured verdicts:

| Human job | Kind of residue | Why the agent cannot take it |
|---|---|---|
| Judge, jury, magistrate | open texture + credibility | weighing "due process", "reasonable person", live witness credibility — S by the constitution's design (Ch. 6) |
| Notary, court clerk of record, sworn officer, signatory | gate / standing | text complete, but only a human can *stand* behind the attestation (B class, measured) |
| Prosecutor, defense advocate, negotiator, live interpreter | live rapport + persuasion | the measured live-voice residue (0.750) at institutional scale |
| Nurse, paramedic, firefighter, rescue | live physical response | embodied execution under real physical risk — the measured D-class shape |
| Master craftsperson: welder, machinist, carpenter, plumber | psychomotor skill | electrician's measured shape (S = 0.65) across the trades; demonstrated, not dictated |
| Classroom teacher, coach, mentor | the alliance | teacher's measured shape (S = 0.335): the live environment, not the curriculum |
| Therapist, pastoral and grief work | the alliance | psychotherapist's measured shape (S = 0.315): the rapport is the treatment |
| Political representative, community organizer | legitimacy / standing | consent is not text — the represented must recognize the representative |
| The accountable officer (hospital director, fire commander, officer of the court) | standing for consequences | the agent produces the decision text; a human bears the consequence |

**Theorem (the human economy is the residue).** The jobs humans would
partake that the agent cannot are not the jobs at the top of a skill
hierarchy — they are exactly the jobs at the bottom of the mandate
fraction: those whose S is material, those behind a gate, and those whose
value is standing rather than skill. Every such job is a *person-shaped
task*: it requires someone to whom the consequence, the rapport, or the
consent attaches. The agent can draft the opinion, the instruction, the
plan, and the record; it cannot be the one who stands.

`[honest wall]` The set is shrinking, not fixed. The mandate book's wall
three applies here: skill is not permanently tacit — instrumentation,
simulators, and teleoperation corpora erode surgical and trades S over time.
The three walls that *cannot* be eroded by corpora are the standing gate,
open texture, and consent: those fall only if humans choose to change what
they accept. The Book's claim is about the residue now, measured where the
repo has measured, extrapolated where it has not — and the extrapolation is
tagged.

### Ch. 18  The residue is earned, not inherited

The complementarity lock has an economic mirror: as the agent takes the text
layer (K), the residue — S, the gate, standing — becomes the binding
constraint, and the scarcer factor rises in value. The copyeditor's taste,
the judge's weighing, the teacher's rapport are not leftovers; they are what
the administrable layer cannot supply, and their price is set by the
mandate fraction's complement. `[hypothesis]` This is the standard
complementarity argument applied to the measured K/S split — an implication
of the split, stated as economics, not a measured result.

And the residue is not an inheritance — it is a competency that must be
held, and the repo's own instrument can grade it. The first real human run
of the T74/T75 protocol (`data/human_trial_runs/HT-RUN-001.json`) graded
the developer with the *same* `score_participant()` code that grades the
machine: the learning axes passed (L1 ceiling 0.953, L2 no-forgetting 1.0),
and the creativity bars *correctly rejected the human* — every mid-effort
item was valid (100%) but not novel (0%), creative yield 0.0. `[measured]`
The joint criterion binds on both sides: **the human who cannot produce
novel-but-valid output fails the same bar as the machine.** The residue is
human by default; it is *useful* only when the human actually holds it.

**Theorem (the agent is resettable; the human is not).** The ledger resyncs
bit-identical after a stateless restart; an agent's decision can be rolled
back and its corpus regenerated. The human bears consequences that cannot
be resynced — a judgment served, a sentence carried, a lesson the classroom
cannot rewind. This asymmetry is not skill and not standing; it is
irreversibility. It is why the standing layer (Ch. 7, Ch. 15) is
irreducible: the machine administers the text at zero personal cost, and
the human, who cannot be re-run, takes the consequence. `[honest wall]`
This is a moral claim, stated plainly, not a measured result.

---

## BOOK VI — THE THIRD CLASS, AND THE OBJECTIONS ANSWERED

### Ch. 19  Not everything is administration

The book's axiom (Ch. 1) defined administration as rule → facts → output.
Two classes followed: the administrable text layer and the human residue.
But human activity has a third class that fits neither: **the activity
whose value is the activity itself.** Sport, play, art, worship,
celebration, care within a family — these are not administration, and
asking whether an agent can "administer" them misses the point the way the
fibonacci-on-disk claim missed the disk: the value is not the output but the
experience, the practice, the presence. `[hypothesis]` This class sits
outside the axis the Book measures; the honest statement is not that it is
administrable or not, but that the question does not apply.

The same is true at the boundary of the residue. The teacher's classroom is
not only a delivery channel for curriculum — the teaching is part of the
student's experience of being taught. The surgeon's hand is part of the
patient's trust. Where the value is *in the act*, the agent has no role
that administration can name. The complementarity lock is silent here by
design: it splits work, not life.

This is the Book's final answer to "everything?" — three classes, not one:
the **text layer** (administrable, measured), the **residue** (human,
measured where the repo has measured), and the **point of the activity
itself** (outside the axis). "Everything" fails the third way: not because
the agent is incapable, but because the question was asked about the wrong
kind of thing.

### Ch. 20  Three objections, answered

The repo's culture publishes its null first; this Book does the same. The
three strongest objections, steelmanned, and the replies:

1. **The decomposition objection.** *"The A-set is an artifact of the
   `k`/`s` inputs; change the estimates and the classes move."* Reply: true
   and stated — the mandate book's wall 2. The Book's claims are about the
   *logic* (k + s ≤ 1, the complementarity lock, the classes from K/S),
   which the tests pin; the inputs are `[hypothesis]`, any reader may
   re-argue them, and every verdict moves together. The objection
   strengthens the Book: it is why no Class A verdict is asserted as fact.
2. **The tautology objection.** *"`text_mandate_fraction = 1 − S` is true
   by definition; it measures nothing new."* Reply: correct — it is the
   skill axis read backward, by design (mandate book Ch. 5). What is not a
   tautology is the *split itself* (K vs S is a substantive claim) and the
   *measured* fourteen decompositions. The formula is a lens; the lens is
   not the discovery — the assignments are.
3. **The moving-residue objection.** *"Corpora and simulators erode S; the
   residue shrinks until 'human jobs' means nothing."* Reply: BOOK VII
   wall 5 grants the erosion — skill is not permanent. But the standing
   gate, open texture, and consent do not move with the data; and the third
   class (Ch. 19) is not eroded at all because it is not a skill. The
   residue narrows, the standing layer persists, and the point of the
   activity never enters the axis.

---

## BOOK VII — HONEST WALLS

1. **Refutation is provisional.** Every REFUTED claim is a statement about
   the experiment as run; a better experiment may resurrect it, and the
   claim's own file must say so.
2. **Capability ≠ adoption.** Class A and `fully` say the agent *can* do the
   work. Whether a court, a market, or a society lets it is a gate, not a
   capability — and the deepest gate is consent, which is outside the
   measure.
3. **The legal decomposition is an application, not a verdict.** The repo
   measures 14 professions; the legal-system and human-job extensions in
   Ch. 6 and Ch. 17 are `[hypothesis]` applications of the same instrument,
   tagged as such, not new measurements — and the frontier instruments of
   Ch. 14 are proposals, not results.
4. **The bands are practical, not natural.** `S ≤ 0.10`, `FULLY = 0.90`,
   `PARTIAL = 0.50` are auditable constants. The constitution's open-texture
   words guarantee residue strictly, but *how much* residue a court of an
   agent's opinions carries is a measured question, not a decree.
5. **Skill is not permanent; standing is.** Corpora erode S. The gate, open
   texture, and consent do not move with the data — they move only with what
   humans accept.

**The Book's one-sentence law:** *A law, in both senses, is a claim to
regularity — descriptive, surviving benign re-encoding, or prescriptive,
decreed as a text mandate — and its administration belongs to an accurate
agent exactly up to the mandate fraction 1 − S: the text layer of any
institution is administrable, and the residue — tacit skill, licensed
standing, open texture, and consent — is the human job.*

---

## Appendix — the repo assets behind this Book

| Book claim | Repo asset |
|---|---|
| clock-test canon (T59 1.0000 → 0.4167; T61 rotation 1.0000) | `experiments/clock_test.py`, `rotation_test.py`, `data/clock_test_data.json`, `data/rotation_test_data.json`, `docs/THE_BOOK.md` ch. 15 |
| measured ledger of refutations | `docs/AUDIT.md`, `docs/NOVELTY_AND_CREATION.md`, `data/*_data.json` verdicts |
| complementarity lock and the 14-profession verdict | `professions/rubric.py`, `professions/professions_data.py`, `experiments/ai_performable_professions.py`, `data/ai_performable_professions_data.json` |
| the doctrines read by the instruments | `experiments/decentral_net_continual.py` (T55e MIX), `puno_flow/index.py` (T67), `experiments/clock_test.py` (T59), `puno_flow/ledger.py` (T70), `data/bazaar_hybrid_data.json`, `data/decentral_net_t67_data.json`, `data/decentral_net_continual_data.json` |
| the jurists read by the canon (Hart's recognition; Fuller's eight canons) | `experiments/clock_test.py`, `rotation_test.py`, `experiments/decentral_net_continual.py` (T55e MIX), `puno_flow/ledger.py` (T70), `professions/mandate.py` |
| the law of the lawgiver (amendment gate, the canon as amendment test) | git history of `docs/THE_MANDATE_BOOK.md`, `puno_flow/ledger.py` (T70), `experiments/clock_test.py`, `rotation_test.py` |
| mandate fraction and statuses | `professions/mandate.py`, `experiments/mandate_report.py`, `data/mandate_report_data.json` |
| machine-administered governance | `experiments/bazaar_hybrid.py`, `experiments/bazaar_net.py`, `data/bazaar_hybrid_data.json`, `data/bazaar_net_data.json` |
| contracts and the repo's own legal-text work | `docs/US7284987B2_ANALYSIS.md`, `docs/AUTO_PACKAGING_PATENTS.md` |
| the human trial bridge | `docs/HUMAN_TRIAL_INSTRUMENT.md`, `docs/LEARNING_CREATIVITY_TEST.md`, `experiments/human_trial_pilot.py`, `data/human_trial_pilot_data.json`, `data/human_trial_runs/HT-RUN-001.json` |
| machine-administered records | `puno_flow/ledger.py`, `experiments/decentral_bank*.py`, `docs/AUDIT.md` |
| machine-administered assessment | `experiments/learn_creativity_test.py`, `learn_curve_scale.py`, `docs/LEARNING_CREATIVITY_TEST.md`, `data/learn_creativity_test_data.json`, `data/learn_curve_scale_data.json` |
| machine-administered time | `calendars/`, `data/epoch_0d.json`, `data/calendar_universal_data.json`, `docs/THE_DAY_BOOK.md` |
| machine-administered production | `packaging/`, `docs/AUTO_PACKAGING_SYSTEM.md` |
| the honest-wall conventions | `docs/AUDIT.md`, `docs/NOVELTY_AND_CREATION.md` |
