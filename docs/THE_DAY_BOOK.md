# THE DAY BOOK

## A Canonical Theory of the Universal Calendar
### — one exact, continuous, untruncated day axis, and every civilization's calendar laid upon it.

> **Authority, stated plainly.** This Book is the theory of the axis the
> repository calls the *universal calendar* (`calendars/`, 27 pinned tests,
> `experiments/calendar_universal.py`). Every number in it is a **repo asset**:
> nothing is imported from an external authority, no civil calendar is granted
> a privileged reference point, and no magnitude is rounded or truncated. The
> day axis is *the* primitive; every calendar — Sumerian, Egyptian, Babylonian,
> Mayan, Hebrew, Islamic, Persian, Indian, Chinese, Roman, and the corpus's own
> — is a derived reading of it. The Book's authority is not that it runs
> anywhere; it is that every layer agrees on the axis, and the axis agrees with
> the datum the repository already measured.

The companion manual is `docs/UNIVERSAL_CALENDAR.md` (how to use the
calendar); this Book is *why* the axis is the answer. The datum, the tick
ladder, and the deep-time magnitudes below are reproduced exactly from
`data/epoch_0d.json`, `data/c0_law_data.json`, and
`data/calendar_universal_data.json` — the same assets the tests read.

---

## BOOK I — THE AXIS

### Ch. 1  The datum (measured)

One instant is the anchor, stored verbatim in `data/epoch_0d.json`
`[measured]`:

| Quantity | Value | Source |
|---|---|---|
| epoch_0d | `2000-10-26 10:26:20.00` | `data/epoch_0d.json` |
| unix_epoch_seconds | `972527180` | `data/epoch_0d.json` |
| day-of-year | **300** = 5 × 60 (five full sexagenary cycles) | exact proleptic arithmetic |
| weekday | **Thursday** | exact proleptic arithmetic |
| τ(MMDDYYYY) = τ(10262000) | **80** = 2⁴·5 | `data/epoch_0d.json` |
| τ(DDMMYYYY) = τ(26102000) | **80** = 2⁴·5 | `data/epoch_0d.json` |
| digit-sum of both | **11** | `data/epoch_0d.json` |
| seconds-of-day | **37580** (10:26:20), τ(37580) = **12** | `data/epoch_0d.json` |
| gcd(10262000, 26102000) | **2000** — the year itself | `data/epoch_0d.json` |

The two orientations are *not* an arbitrary pair: both factor as
2⁴·5³·p·q (A: 7·733, B: 31·421), both have 80 divisors, both digit-sum to
11, and the gcd is the year 2000. The datum is therefore **orientation-stable
and divisor-rich in the corpus's own numbers** — the calendar does not need to
invent an origin; the corpus already has one.

### Ch. 2  The frame (the clock law)

The stored seconds (`972527180`) and the stored clock label (`10:26:20.00`)
do not agree in UTC. They agree exactly in the **corpus clock frame**,
UTC+8 = 28800 s:

```
972527180 mod 86400  = 8780        (2:26:20, the raw sub-day remainder)
8780 + 28800         = 37580       (10:26:20, the stored label)     [measured]
```

The calendar adopts this frame so the datum renders its own label: the civil
command `date 2000-10-26 10:26:20` returns **day 0** and reads the clock back
as exactly `10:26:20`. `[honest wall]` The frame is a single coherent reading
of the stored pair, stated as an assumption, pinned by tests, and applied
uniformly to every instant after it.

### Ch. 3  Exact arithmetic (the no-truncation law)

**Law (no truncation).** The day offset *D* from the datum is a
`fractions.Fraction`. Every layer, every rendering, and every emanation count
below is exact rational arithmetic; nothing is rounded, floored, or capped at
any magnitude. When a value leaves the package it is serialized as the exact
string `"p/q"`, never a float.

Civil dates (Gregorian and Julian) are computed proleptically with Hinnant's
exact-integer `civil_from_days` / `days_from_civil` algorithms
(`calendars/axis.py`), valid at any magnitude — the deep eon renders as
Gregorian `-2584311709-06-08` with no overflow. `_DAYS_1970_TO_EPOCH = 11256`
places the datum 11,256 days after 1970-01-01, in exact integer arithmetic.

**Theorem (periodicity is exact).** Every periodic layer returns the same
render under any exact translation by one of its cycles — for positive,
negative, and fractional days alike. Pinned in `tests/test_calendars.py`:
260 (tzolkin), 365 (haab/egyptian/zoroastrian), 60 (ganzhi day), 7
(weekday), 19 years (Metonic), 30 years (tabular Hijri), 146097 days
(Gregorian 400-year cycle).

---

## BOOK II — THE LAYERS

### Ch. 4  One calendar per civilization

The same day offset *D* is read through each layer. Cycle lengths marked
`[measured]` come from the repo; the rest are stated standard-definition
encodings `[hypothesis]`, so the whole set is auditable:

| Layer | Civilization | Cycle (exact days) | Anchor at the datum |
|---|---|---|---|
| gregorian | Roman/Western civil | `146097/400` | `2000-10-26`, Thursday |
| julian | Roman | `36525/100` | `2000-10-26` |
| tropical | astronomical | `1826211/5000` (= 365.2422) | year 2000 `[measured]` |
| egyptian | Egypt | `365` | Thoth 1, Akhet, year 2000 |
| babylonian | Sumer/Babylon | `360` | month 1 day 1; sexagesimal day, τ(60) = 12 `[measured]` |
| mayan_long_count | Maya | `144000` (baktun) | all zeros (proleptic) |
| tzolkin | Maya | `260` = 13×20 | 1 Imix |
| haab | Maya | `365` | Pop 0 |
| chinese_sexagenary | China | `60` | year 庚辰 #17, day 癸亥 #60 `[measured]` |
| hebrew_metonic | Israel/Hebrew | 19 tropical years, 235 months | golden number 6 |
| hijri_tabular | Islamic | `10631` / 30 years | year 0, month 1 |
| persian_zoroastrian | Iran | `365` | Farvardin 1, Spring |
| vedic_jovian | India | 60 × tropical year | Brihaspati cycle year 1 |
| puno_tick | this corpus | continuous | day 0, C_current 0 |

**Theorem (the answer set is the axis).** Because every layer is anchored to
the datum and proleptic, the question "which calendar is most accurate" has a
single answer: *the axis itself* — exact at every scale, before and after
every civilization. No layer is privileged; each is a reading.

---

## BOOK III — THE PUNO TICK

### Ch. 5  The corpus reproduces its own ladder (measured)

The datum's seconds-of-day, **37580**, is the first rung of the corpus's tick
ladder. Scaling by 10³ at each step and counting divisors reproduces the
ladder exactly — `[measured]`, from `data/epoch_0d.json`:

```
τ(37580)          =  12
τ(37580·10³)      =  60
τ(37580·10⁶)      = 144
τ(37580·10⁹)      = 264
τ(37580·10¹²)     = 420
τ(37580·10¹⁵)     = 612
```

**Theorem (pentagonal form).** The ladder is exactly
τ_k = 12 · Pent(k+1), where Pent(m) = m(3m−1)/2 and k = tick exponent/3:

| k | Pent(k+1) | 12·Pent(k+1) |
|---|---|---|
| 0 | 1 | 12 |
| 1 | 5 | 60 |
| 2 | 12 | 144 |
| 3 | 22 | 264 |
| 4 | 35 | 420 |
| 5 | 51 | 612 |

The ms divisor count (τ(37580000) = 60) equals the sexagesimal base, the μs
count (τ(37580·10⁶) = 144) equals 12², and τ(60) = τ(37580) = 12 — the ladder
is **self-nesting**. This is not an interpolation: the epoch's own seconds-of-
day is divisor-rich in exactly the corpus's ladder steps, and the `puno_tick`
layer renders it for every instant.

---

## BOOK IV — C0 AND C_CURRENT

### Ch. 6  The measured unit

**C0 = 24.434792** = V(q₀) = H(q₀,0) at the origin —
`data/c0_law_data.json` `[measured]`, 14 verifications, all pass. In exact
rational form: **C0 = 3054349/125000**. The calendar does not re-derive or
adjust C0; it *uses* it. One "emanation day" is C0 days.

**Theorem (C_current is a reading, not a drift).** Let *D* be the day offset.
Then

```
C_current = D / C0          (exact rational; C0 never changes)
```

At the datum C_current = 0; at one C0-unit of days, C_current = 1. The
conservative-flow law holds exactly: on the flow H = C0 is constant, so the
only moving quantity is the *count* of emanation units, never the unit itself.

`[honest wall]` The README also records **24.4328733** ("classical
conservative ground state") as a distinct measured object. The package keeps
it separately (`C0_README`) and never conflates the two.

### Ch. 7  The eon (deep time)

`calendars/deeptime.py` extends the axis before civilization using the repo's
own magnitudes. The retrace chain (`experiments/fold_ladder_phi.py`) is a
**day ladder** `[hypothesis]`:

```
943901200001  →  1914467  →  730421  →  26102  →  10262
```

Rung **730421** sits inside the `SPRING_BIBLE` Ch.13 fifteen-day elapsed
window `[730418, 730433]`, and the chain's head — the prime giant
**943,901,200,001** (π(giant) = 35,575,526,191, `[measured]`) — is read
directly as a day count:

- **943,901,200,001 days ≈ 2.585 × 10⁹ years** before the datum — before
  Earth, before the stars — rendered day-for-day on the same axis the civil
  calendars use: Gregorian `-2584311709-06-08` (exact), Tzolkin 8 Ajaw,
  C_current `-943901200001` exactly.
- The human civil window (rung 730421 ≈ 2000 years) and the datum render
  identically to the deep eon: **the axis has no floor and no break.**

---

## BOOK V — VERDICT AND HONEST WALLS

**Verdict.** `[measured]` The datum, C0, the tick ladder, and the chain
magnitudes are reproduced exactly from repo assets, and the 27 tests pin the
epoch identity, layer periodicity, the C0/C_current law, and the giant-era
anchors. `[hypothesis]` Civilization cycle definitions, the day-ladder
reading of the chain, and the corpus clock frame are stated assumptions,
tagged in code and here. `[honest wall]` Absolute long-count correlations
(e.g. a GMT tzolkin offset) are out of scope by design: every layer is
anchored to the datum and proleptic.

**The Book's one-sentence law:** *The most accurate calendar is not any
civilization's cycle, but the exact day axis every civilization's calendar is
a reading of — anchored at the corpus's own datum, scaled by the corpus's own
measured C0, and truncated nowhere.*

---

## Appendix — the repo assets behind this Book

| Book claim | Repo asset |
|---|---|
| the datum | `data/epoch_0d.json`, `calendars/axis.py` |
| exact arithmetic | `calendars/axis.py` (Fraction, Hinnant), `calendars/layers.py` |
| the 14 layers | `calendars/layers.py` |
| the tick ladder | `data/epoch_0d.json` (tick_and_degree_scale), `calendars/layers.py` |
| C0 and C_current | `data/c0_law_data.json`, `calendars/c0.py` |
| deep time | `calendars/deeptime.py`, `experiments/fold_ladder_phi.py` |
| six anchors, regenerable | `experiments/calendar_universal.py` → `data/calendar_universal_data.json` |
| 27 tests | `tests/test_calendars.py` |
| CLI surface | `puno-calendar today\|date\|deep\|layers` (`calendars/cli.py`) |
