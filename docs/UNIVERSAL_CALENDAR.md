# The Universal Calendar — One Axis, Every Civilization's Calendar

**Purpose:** Build the most accurate calendar possible by laying **every known
calendar of the other civilizations** over a single continuous day axis,
extending it **before human civilization** (proleptically, into the
pre-civilization eon and beyond), with **no truncation** anywhere, using
**no external references** — only the repo's own measured assets decide what
C0 is and what C_current should be.

The result is `calendars/` (a new package), a pinned test suite
(`tests/test_calendars.py`, 27 tests), an experiment
(`experiments/calendar_universal.py`) that writes the exact
`data/calendar_universal_data.json` (gitignored, regenerable), a CLI
(`puno-calendar`, alias `python -m calendars.cli`), and this document.

**Method date:** 2026-08-13.

---

## 1. The axis: exact, untruncated, proleptic

`calendars/axis.py` defines one continuous time axis in **days since the
datum** `epoch_0d` (`data/epoch_0d.json`). The day count is a
`fractions.Fraction` — every magnitude (deep past, far future) and every
sub-second precision is representable, and nothing is rounded or truncated.
When a value leaves the package it is serialized as the exact `"p/q"`
string, never a float. `[measured]` The datum is stored verbatim:

| Field | Value | Source |
|---|---|---|
| epoch_0d | `2000-10-26 10:26:20.00` | `data/epoch_0d.json` |
| unix_epoch_seconds | `972527180` | `data/epoch_0d.json` |
| MMDDYYYY / DDMMYYYY renderings | `10262000` / `26102000`, both **τ = 80**, digit-sum **11** | `data/epoch_0d.json` |
| day-of-year | **300** (= 5 × 60, sexagenary-complete) | exact proleptic arithmetic |
| weekday | **Thursday** | exact proleptic arithmetic |
| year 2000 ganzhi | **庚辰 Geng-Chen #17** | exact proleptic arithmetic |
| doy-300 ganzhi | **癸亥 Gui-Hai #60** | exact proleptic arithmetic |

The stored seconds (`972527180`) and the stored clock label (`10:26:20.00`)
agree under the corpus clock frame (UTC+8): the calendar adopts that frame so
the datum renders its own label — `date "2000-10-26 10:26:20"` returns day 0
and reads the clock back as exactly `10:26:20`. `[honest wall]` The unix
seconds themselves contain an 8-hour sub-day remainder; the corpus frame is
the single coherent reading of the stored pair, and every other instant
renders in that same frame.

Civil dates (Gregorian and Julian) are computed proleptically with Hinnant's
exact-integer `civil_from_days`/`days_from_civil` algorithms, valid at any
magnitude: the giant pre-civilization instant renders as Gregorian
`-2584311709-06-08` with no overflow and no loss.

## 2. The layers: one calendar per civilization

`calendars/layers.py` renders the same day offset D into each layer. Cycle
lengths marked `[measured]` come from the repo; the rest are stated
standard-definition encodings `[hypothesis]`, so the whole set is auditable.

| Layer | Civilization | Cycle (exact days) | Anchor |
|---|---|---|---|
| gregorian | Roman/Western civil | `146097/400` | datum → `2000-10-26`, Thursday |
| julian | Roman | `36525/100` | datum → `2000-10-26` |
| tropical | astronomical | `1826211/5000` (= 365.2422) | `SPRING_BIBLE` Ch.12 `[measured]` |
| egyptian | Egypt | `365` | 12×30 + 5 epagomenal |
| babylonian | Sumer/Babylon | `360` | sexagesimal day, τ(60) = 12 `[measured]` |
| mayan_long_count | Maya | `144000` (baktun) | 144 = 12² × 10³, corpus invariant |
| tzolkin | Maya | `260` = 13×20, τ = 12 `[measured]` | day 0 → 1 Imix |
| haab | Maya | `365` | day 0 → Pop 0 |
| chinese_sexagenary | China | `60` | year #17 庚辰, day #60 癸亥 `[measured]` |
| hebrew_metonic | Israel/Hebrew | 19 tropical years, 235 months | golden number from datum year |
| hijri_tabular | Islamic | `10631` / 30 years | mean month `10631/360` |
| persian_zoroastrian | Iran | `365` | 12×30 + 5 Gatha days |
| vedic_jovian | India | 60 × tropical year | 60-year Brihaspati cycle |
| puno_tick | this corpus | continuous | the corpus's own meta-calendar |

Periodicity is exact and pinned: 260 (tzolkin), 365 (haab/egyptian/
zoroastrian), 60 (ganzhi day), 7 (weekday), 19 years (Metonic), 30 years
(tabular Hijri), 146097 days (Gregorian 400-year cycle) all return the same
render — for positive, negative, and fractional days alike.

## 3. The Puno tick: the corpus reproduces its own ladder

The epoch seconds-of-day `37580` (`EPOCH_SECONDS_OF_DAY`, 10:26:20) is the
first rung of the corpus's tick ladder. `[measured]` Scaling by 10³ at each
step and counting divisors reproduces the ladder exactly:

`τ(37580) = 12,  τ(37580·10³) = 60,  τ(37580·10⁶) = 144,  τ(37580·10⁹) = 264,  τ(37580·10¹²) = 420,  τ(37580·10¹⁵) = 612`

This is not an interpolation — the epoch's own seconds-of-day is divisor-rich
in exactly the corpus's ladder steps (12 → 60 → 144 → 264 → 420 → 612), and
the puno_tick layer renders it for every instant.

## 4. C0 and C_current: calibrated from repo assets only

`calendars/c0.py` takes the measured constant as the calendar's own unit:

- **C0 = 24.434792** = `V(q0) = H(q0,0)` at the origin — `data/c0_law_data.json`
  `[measured]`. The calendar does not re-derive or adjust it; it *uses* it:
  one "emanation day" is C0 days.
- **C_current = D / C0**, the exact rational count of emanation units that
  have flowed from the datum by day offset D. At the datum C_current = 0 and
  the conservative-flow law holds exactly: C0 never drifts, C_current is a
  *reading*, not a change.

`[honest wall]` The README also records `24.4328733` ("classical conservative
ground state") as a **distinct measured object**; the package keeps it as a
separate constant (`C0_README`) and does not conflate the two. C_current is
serialized as an exact `"p/q"` (e.g. the datum: `"0"`; one C0-unit of days:
`"1"`), with an exact decimal expansion available for display.

## 5. Deep time: before human civilization

`calendars/deeptime.py` extends the axis before civilization using the repo's
own magnitudes. The retrace chain (`experiments/fold_ladder_phi.py`) is a
**day ladder** `[hypothesis]`: rung `730421` sits inside the `SPRING_BIBLE`
Ch.13 fifteen-day elapsed window `[730418, 730433]` (a day-count window), and
the chain's head — the prime giant **943,901,200,001** — is read directly as
a day count:

- **943,901,200,001 days ≈ 2.585 × 10⁹ years** before the datum — before
  Earth, before the stars, rendered day-for-day on the same axis the civil
  calendars use (Gregorian `-2584311709-06-08`, Tzolkin 8 Ajaw, C_current
  `-943901200001` exactly).
- The human civil window (`730421` ≈ 2000 years) and the datum itself are
  rendered identically to the deep eon — the axis has no floor and no break.

## 6. Surfaces and verification

- **Tests:** `tests/test_calendars.py` (27 tests) — epoch identity, exact
  p/q round-trips, periodicity of every layer, C0/C_current relation, the
  giant-era anchors, and rendering at extremes (0, −1/3, −giant, +10⁹ days).
  Full suite: **372 passed** (345 prior + 27 new).
- **Experiment:** `experiments/calendar_universal.py` → exact
  `data/calendar_universal_data.json` with six anchors (datum, now, window
  lo/hi, rung, giant eon), all layers, and the C0 calibration.
- **CLI:** `puno-calendar today | date YYYY-MM-DD [HH:MM:SS] | deep | layers`.

## 7. Verdict

`[measured]` The datum, C0, the tick ladder, and the chain magnitudes are
reproduced exactly from repo assets. `[hypothesis]` Civilization cycle
definitions, the day-ladder reading of the chain, and the corpus clock frame
are stated assumptions, each tagged in code and here. `[honest wall]` The
calendar's absolute long-count correlations (e.g. a GMT tzolkin offset) are
out of scope by design: every layer is anchored to the datum and is
proleptic, so the answer to "which calendar is most accurate" is *the axis
itself* — exact at every scale, before and after every civilization.
