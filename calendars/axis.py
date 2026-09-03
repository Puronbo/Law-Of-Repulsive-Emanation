"""calendars.axis - one exact, untruncated day axis for every calendar.

All calendars in this package are layers over a single continuous time axis
measured in days since the corpus datum epoch_0d (2000-10-26 10:26:20.00,
unix 972527180 - data/epoch_0d.json, `[measured]`). The axis uses exact
rational arithmetic (fractions.Fraction): any magnitude (deep past, far
future) and any sub-second precision is representable, nothing is rounded or
truncated. When a report serializes a Fraction it writes the exact "p/q"
string, never a float.

    D = 0            epoch_0d instant
    D < 0            before the datum (pre-civilization, deep time)
    D > 0            after the datum
"""

from fractions import Fraction
from time import time

# --- repo-measured anchors (data/epoch_0d.json, WEAVERS_SCRIBE Ch.2) ---------
EPOCH_SECONDS = Fraction(972527180)   # unix seconds at 2000-10-26 10:26:20.00
SECONDS_PER_DAY = Fraction(86400)     # the sexagesimal day: 24*60*60
EPOCH_YEAR = 2000
EPOCH_MONTH = 10
EPOCH_DAY_OF_MONTH = 26
EPOCH_DAY_OF_YEAR = 300              # = 5 x 60 sexagenary cycles exactly
EPOCH_WEEKDAY = "Thursday"           # Jupiter's day, the sexagesimal patron
EPOCH_SECONDS_OF_DAY = 37580         # 10:26:20.00
EPOCH_SECONDS_MOD_DAY = Fraction(972527180) % 86400   # = 8780 (unix remainder)
FRAME_OFFSET_SECONDS = 28800         # corpus clock frame (UTC+8): the stored
                                     # seconds 972527180 and the label
                                     # 10:26:20.00 agree under this frame.

# --- civil-to-rational conversions -------------------------------------------
# Epoch day D=0 sits at civil date 2000-10-26. days_since_1970 for that date
# is 11256; we define EPOCH as our own origin regardless.
_DAYS_1970_TO_EPOCH = Fraction(11256)


def unix_seconds_to_day(fraction_seconds):
    """unix seconds (Fraction) -> day offset from epoch_0d (exact Fraction)."""
    return (Fraction(fraction_seconds) - EPOCH_SECONDS) / SECONDS_PER_DAY


def day_to_unix_seconds(day):
    """day offset from epoch_0d -> unix seconds (exact Fraction)."""
    return Fraction(day) * SECONDS_PER_DAY + EPOCH_SECONDS


def days_since_1970(day):
    """day offset -> exact day count from 1970-01-01 (civil, proleptic)."""
    return Fraction(day) + _DAYS_1970_TO_EPOCH


def now_day():
    """Current instant as a day offset from epoch_0d (exact Fraction)."""
    return unix_seconds_to_day(Fraction(int(time() * 1e6), 10**6))


# --- proleptic civil algorithms (exact integer arithmetic) -------------------
def _civil_ymd(days_since_1970_int):
    """Proleptic Gregorian civil date from an integer day count.

    Howard Hinnant's days_from_civil/civil_from_days algorithms - exact
    integer arithmetic, valid for any magnitude (no truncation).
    """
    z = days_since_1970_int + 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + 3 if mp < 10 else mp - 9
    return (y + (1 if m <= 2 else 0), m, d)


def _julian_ymd(days_since_1970_int):
    """Proleptic Julian civil date from an integer day count (365.25 days)."""
    z = days_since_1970_int + 719468
    # Julian: leap every 4 years, era length 1461 (4 Julian years)
    era = (z if z >= 0 else z - 1460) // 1461
    doe = z - era * 1461
    yoe = (doe - doe // 1460) // 365
    y = yoe + era * 4
    doy = doe - (365 * yoe + yoe // 4)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + 3 if mp < 10 else mp - 9
    return (y + (1 if m <= 2 else 0), m, d)


def civil_to_days(y, m, d):
    """Proleptic Gregorian civil date -> days since epoch_0d (exact int)."""
    # Hinnant days_from_civil (inverse of _civil_ymd)
    y -= 1 if m <= 2 else 0
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return doe + era * 146097 - 719468 - int(_DAYS_1970_TO_EPOCH)


def julian_to_days(y, m, d):
    """Proleptic Julian civil date -> days since epoch_0d (exact int).
    Inverse of julian_ymd; leap year every 4 years (no century exception)."""
    y -= 1 if m <= 2 else 0
    era = (y if y >= 0 else y - 3) // 4
    yoe = y - era * 4
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 + doy
    return doe + era * 1461 - 719468 - int(_DAYS_1970_TO_EPOCH)


def gregorian_ymd(day):
    """Proleptic Gregorian (y, m, d) for a day offset (exact for integers).

    For non-integer days the integer floor is used (the date portion); the
    time-of-day comes from the fractional part.
    """
    return _civil_ymd(int(days_since_1970(day)))


def julian_ymd(day):
    return _julian_ymd(int(days_since_1970(day)))


def day_of_year(y, m, d):
    """Exact 1-based day-of-year for a proleptic Gregorian date."""
    days = [31, 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return sum(days[:m - 1]) + d


def weekday(day):
    """Weekday name anchored at the datum (Thursday, repo-measured)."""
    names = ["Thursday", "Friday", "Saturday", "Sunday", "Monday",
             "Tuesday", "Wednesday"]
    return names[int(Fraction(day) % 7)]
