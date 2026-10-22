# Visual artifacts — the register rendered

**Status: two self-contained HTML artifacts, both generated or hand-authored from
kernel-checked material.**  Neither claims anything that the Lean tree does not
already carry.  Both open in any browser with no server and no network access.

---

## 1. `MULTIDIMENSIONAL_MAP.html` — the register as a point cloud

**What it is.**  A rotating 3-D cloud in which **every point is a real repository
item** and **every axis is a real attribute** read out of the ledgers.  It is
generated, never hand-drawn.

**Where the data comes from** (all read by the generator at build time):

| source | what it contributes |
|---|---|
| `MODULE_LEDGER.md` | the module rows: name, category, card refs |
| `MATHEMATICAL_LINK_GRAPH.md` | the **real** `import` edges (the blue lines) |
| `THE_GAP_LEDGER.md` | the 39 open walls: tier, subject, proof-attempt kind, pins |
| `CLAIM_TRACEABILITY.md` | the 37 claim cards: type, Lean artifact, declarations |
| the Lean sources | the declaration names that carry each module |

**The five dimensions.**  Any three can be mapped onto x/y/z at runtime:

1. **category** — the nine ledger categories
2. **status** — the epistemic ladder: `machine-checked` → `partial` → `no-go` →
   `citation-only` → `empirical` → `open`
3. **depth** — the module's position in the true `import` DAG (0 = foundation)
4. **kind** — `module` / `gap` / `card`
5. **tier** — the register-debt tier (gaps only)

**Reading it.**  Blue points are modules, red are gap rows, green are claim
cards.  A red point carries a ring: it is an *open* wall.  The blue lines are the
actual `import` edges — the shape of the cloud is the shape of the dependency
structure, not an artist's impression.  Click any point to open its panel: the
Lean declarations it carries, the artifact path, the pins, and — for a gap — the
barrier and the **missing object** (the thing that does not exist as a proof).

**Current extent:** 92 modules, 39 gap rows, 37 cards, 69 real import edges,
168 points.

**Regenerate:**

```
python 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/build_multidimensional_map.py
```

The generated JSON lands in
`02_Experimental_Implementations_and_Verification/data/multidimensional_map_data.json`
(a `data/` root, per the repo's persistence standard: generated output, not
load-bearing source).  The HTML embeds the data and loads nothing external.

**Truthfulness gate.**  `test_multidimensional_map.py` re-derives the numbers
from the ledgers and asserts that the rendered page agrees: module count =
modules on disk = ledger rows; drawn edges = real import edges; every mapped gap
is a real `Gn` row; every mapped card is a real card; the HTML embeds its data
and fetches nothing.  A visualisation that drifted from its source would be
worse than no visualisation, so this is a **gate**, not a report.

---

## 2. `CHANNEL_0_the_essential_singularity_as_tv.html` — the 0/0 arc as a television

**What it is.**  The 0/0 arc rendered as a television set.  The **screen** is the
punctured neighbourhood `𝓝[≠]0`; the **dial** is the path to `0`; the
**channels** are different paths.

| channel | picture | the theorem behind it |
|---|---|---|
| `x/x` | a steady bar at **1** | `EssentialIdentity.self_ratio_limit_one` |
| `2x/x` | a steady bar at **2** | `EssentialIdentity.ratio_paths_disagree` |
| `sin(1/x)` | **never locks** — the static | `EssentialIdentity.sin_one_over_has_no_limit` |

The same screen showing contradictory pictures *is* the thesis: `0/0 = 1` was a
channel, not a fact.  The static is not a broken television — it is the honest
signal that no value exists there, only the accumulation, and
`StaticUncovered.lean` proves exactly what it is made of (the two turning-point
families, both extremes recurring at every scale).

---

## What these artifacts do **not** do

- They are **not** evidence.  The evidence is the Lean tree and the pins; these
  are readings of it.
- They are **not** a claim closure.  The red points are open walls, and they are
  open walls *because* the gap ledger says so.
- They **do not** discharge any Millennium obligation.  See
  `WHAT_THIS_DOES_NOT_PROVE.md`.
- The map's shape is a picture of the **dependency structure**, not of the
  universe.  A dense cluster means "many modules import the same things", not
  "this is settled".

## Related

- `MODULE_LEDGER.md` — the module table the map reads
- `MATHEMATICAL_LINK_GRAPH.md` — the import edges the map draws
- `THE_GAP_LEDGER.md` — the open walls the map plots
- `CLAIM_TRACEABILITY.md` — the cards the map plots
- `WHAT_THIS_DOES_NOT_PROVE.md` — the honesty rule these artifacts obey
