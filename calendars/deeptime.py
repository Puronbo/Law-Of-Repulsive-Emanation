"""calendars.deeptime - pre-civilization and deep-time era anchors.

Civilizations and their calendars are young on this axis. The corpus itself
reaches back before them: the retrace chain (experiments/fold_ladder_phi.py)
heads at the prime giant 943,901,200,001, and the calendar reads that giant
as a full emanation instant. The retrace chain is a day ladder `[hypothesis]`
- rung 730421 sits in the SPRING_BIBLE 15-day elapsed window (which is a
day-count window), so the giant is read directly as a day count, placing it
~2.585e9 years before the datum: before Earth, before the stars. The calendar
renders it exactly, day for day, on the same axis the civil calendars use.
Nothing is truncated: the axis is a Fraction line with no floor.

Two repo-internal day magnitudes bracket the human window:
  * rung 730421 (fold_ladder_phi.py CHAIN) - sits inside the SPRING_BIBLE
    Ch.13 15-day elapsed window [730418, 730433];
  * the giant 943901200001 - the deepest era in the corpus.
"""

from fractions import Fraction

from calendars.layers import frac_str

# --- repo-measured magnitudes ------------------------------------------------
GIANT = Fraction(943901200001)        # retrace chain head (prime, repo)
RUNG_730421 = Fraction(730421)        # retrace rung (repo)
WINDOW_LO = Fraction(730418)          # SPRING_BIBLE Ch.13 15-day window
WINDOW_HI = Fraction(730433)


def giant_as_days():
    """The giant read directly as a day count (`[hypothesis]` chain ladder)."""
    return GIANT


def giant_era_epoch_year():
    """Civilization-frame label for the giant era (~2.585e9 years)."""
    d = giant_as_days()
    years = d / Fraction(146097, 400)   # proleptic Gregorian mean year
    return {
        "days_before_epoch": frac_str(d),
        "days": str(GIANT),
        "years_before_epoch": frac_str(years),
        "years_decimal": str(float(years)),   # display only; p/q is exact
        "chain": "943901200001 -> 1914467 -> 730421 -> 26102 -> 10262",
    }


def era(day):
    """Era label and civilization-year count for any day offset (exact)."""
    day = Fraction(day)
    if day >= 0:
        return {
            "era": "post-datum (epoch_0d onward)",
            "days_after_epoch": frac_str(day),
            "civilization_year": frac_str(
                EPOCH_YEAR_HUMAN + day / Fraction(146097, 400)),
        }
    d = -day
    if d >= giant_as_days():
        return {
            "era": "giant-rung eon (deep pre-civilization)",
            "days_before_epoch": frac_str(d),
            "giant_days": frac_str(giant_as_days()),
            "chain_anchor": "943901200001",
        }
    return {
        "era": "pre-civilization (before the datum, calendars proleptic)",
        "days_before_epoch": frac_str(d),
        "years_before_epoch": frac_str(d / Fraction(146097, 400)),
        "window_730421": WINDOW_LO <= d <= WINDOW_HI,
    }


def window_730421():
    """The corpus's 15-day elapsed window as day offsets from the datum."""
    return {
        "lo": str(WINDOW_LO),
        "hi": str(WINDOW_HI),
        "rung": str(RUNG_730421),
        "rung_inside": WINDOW_LO <= RUNG_730421 <= WINDOW_HI,
        "span_days": str(WINDOW_HI - WINDOW_LO),
    }


EPOCH_YEAR_HUMAN = 2000
