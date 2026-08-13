"""calendars.layers - one calendar layer per civilization, all over one axis.

Every layer renders the same exact day offset D (calendars.axis) into that
civilization's calendar. Cycle lengths are exact rationals. Values marked
`[measured]` come from the repo (data/epoch_0d.json, WEAVERS_SCRIBE Ch.2);
the rest are stated standard-definition encodings `[hypothesis]` so the
whole set stays auditable. Absolute long-count/epoch correlations (e.g. a
GMT tzolkin correlation) are deliberately out of scope: each layer is
anchored to the datum D=0 and is proleptic (it also renders before the
civilization existed, and into the far future) - nothing is truncated.
"""

from fractions import Fraction

from calendars.axis import (
    EPOCH_DAY_OF_YEAR,
    EPOCH_YEAR,
    EPOCH_SECONDS_OF_DAY,
    FRAME_OFFSET_SECONDS,
    day_of_year,
    day_to_unix_seconds,
    gregorian_ymd,
    julian_ymd,
    weekday,
)

# --- repo-measured constants ------------------------------------------------
TROPICAL_YEAR = Fraction(3652422, 10000)   # 365.2422 d (SPRING_BIBLE Ch.12)
GREGORIAN_YEAR = Fraction(146097, 400)     # 365.2425 d civil leap rule
JULIAN_YEAR = Fraction(36525, 100)         # 365.25 d
SEXAGESIMAL_BASE = 60                      # tau(60) = 12 (WEAVERS_SCRIBE Ch.2)
TZOLKIN_LENGTH = Fraction(260)             # 13 x 20, tau = 12 (repo)
HAAB_LENGTH = Fraction(365)
EGYPTIAN_YEAR = Fraction(365)
MAYAN_BAKTUN = Fraction(144000)            # 144 = 12^2 x 10^3 (corpus invariant)
CHINESE_CYCLE = Fraction(60)
METONIC_YEARS = 19
METONIC_MONTHS = 235
HEBREW_MONTH = METONIC_YEARS * TROPICAL_YEAR / METONIC_MONTHS
HIJRI_30Y = Fraction(10631)                # 30 years, 11 leap days (tabular)
HIJRI_MONTH = HIJRI_30Y / 360
JOVIAN_CYCLE = Fraction(60)                # 60-year Vedic Brihaspati cycle


def frac_str(x):
    """Exact p/q string - fractions are never floated (no truncation)."""
    f = Fraction(x)
    if f.denominator == 1:
        return str(f.numerator)
    return "%d/%d" % (f.numerator, f.denominator)


def _div(x, d):
    return Fraction(x) // d


def _mod(x, d):
    return Fraction(x) % d


def _ifloor(x):
    """Floor of a Fraction as a Python int (correct for negative values)."""
    f = Fraction(x)
    return f.numerator // f.denominator


def _tau(n):
    """Exact divisor count of a non-negative integer."""
    n = int(n)
    if n < 0:
        n = -n
    if n == 0:
        return 0
    t = 1
    p = 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        t *= e + 1
        p += 1 if p == 2 else 2
    if n > 1:
        t *= 2
    return t


# --- cycle/name tables -------------------------------------------------------
EGYPTIAN_MONTHS = ["Thoth", "Phaophi", "Athyr", "Choeac",
                   "Tybi", "Mechir", "Phamenoth", "Pharmuthi",
                   "Pachon", "Payni", "Epiphi", "Mesore"]
EGYPTIAN_SEASONS = ["Akhet", "Peret", "Shemu"]
ZOROASTRIAN_MONTHS = ["Farvardin", "Ordibehesht", "Khordad", "Tir",
                      "Mordad", "Shahrivar", "Mehr", "Aban",
                      "Azar", "Dey", "Bahman", "Esfand"]
TZOLKIN_NAMES = ["Imix", "Ik'", "Ak'b'al", "K'an", "Chikchan", "Kimi",
                 "Manik'", "Lamat", "Muluk", "Ok", "Chuwen", "Eb'",
                 "Ben", "Ix", "Men", "Kib", "Kab'an", "Etz'nab'",
                 "Kawak", "Ajaw"]
HAAB_MONTHS = ["Pop", "Wo'", "Sip", "Sotz'", "Sek", "Xul", "Yaxkin",
               "Mol", "Ch'en", "Yax", "Sak", "Keh", "Mak", "K'ank'in",
               "Muwan", "Pax", "K'ayab", "Kumk'u", "Wayeb"]
STEMS = ["Jia\u7532", "Yi\u4e59", "Bing\u4e19", "Ding\u4e01", "Wu\u620a",
         "Ji\u5df1", "Geng\u5e9a", "Xin\u8f9b", "Ren\u58ec", "Gui\u7678"]
BRANCHES = ["Zi\u5b50", "Chou\u4e11", "Yin\u5bc5", "Mao\u536f", "Chen\u8fb0",
            "Si\u5df3", "Wu\u5348", "Wei\u672a", "Shen\u7533", "You\u9149",
            "Xu\u620c", "Hai\u4ea5"]
STROKE = ["\u7532\u5b50", "\u4e59\u4e11", "\u4e19\u5bc5", "\u4e01\u536f",
          "\u620a\u8fb0", "\u5df1\u5df3", "\u5e9a\u5348", "\u8f9b\u672a",
          "\u58ec\u7533", "\u7678\u9149", "\u7532\u620c", "\u4e59\u4ea5",
          "\u4e19\u5b50", "\u4e01\u4e11", "\u620a\u5bc5", "\u5df1\u536f",
          "\u5e9a\u8fb0", "\u8f9b\u5df3", "\u58ec\u5348", "\u7678\u672a",
          "\u7532\u7533", "\u4e59\u9149", "\u4e19\u620c", "\u4e01\u4ea5",
          "\u620a\u5b50", "\u5df1\u4e11", "\u5e9a\u5bc5", "\u8f9b\u536f",
          "\u58ec\u8fb0", "\u7678\u5df3", "\u7532\u5348", "\u4e59\u672a",
          "\u4e19\u7533", "\u4e01\u9149", "\u620a\u620c", "\u5df1\u4ea5",
          "\u5e9a\u5b50", "\u8f9b\u4e11", "\u58ec\u5bc5", "\u7678\u536f",
          "\u7532\u8fb0", "\u4e59\u5df3", "\u4e19\u5348", "\u4e01\u672a",
          "\u620a\u7533", "\u5df1\u9149", "\u5e9a\u620c", "\u8f9b\u4ea5",
          "\u58ec\u5b50", "\u7678\u4e11", "\u7532\u5bc5", "\u4e59\u536f",
          "\u4e19\u8fb0", "\u4e01\u5df3", "\u620a\u5348", "\u5df1\u672a",
          "\u5e9a\u7533", "\u8f9b\u9149", "\u58ec\u620c", "\u7678\u4ea5"]
# 2000 = Geng-Chen #17, so index 16 (0-based) = 17 (1-based): stroke[16] = GengChen
_GANZHI_YEAR_EPOCH_INDEX = 16          # year 2000 = #17 (repo-measured)
_DAY_300_GANZHI_INDEX = 59             # day 300 = #60 Guihai (repo-measured)


def _year_ganzhi(day):
    """Sexagenary year index (0-based) for a day offset."""
    year = EPOCH_YEAR + _div(day, TROPICAL_YEAR)
    return _mod(year - 2000 + _GANZHI_YEAR_EPOCH_INDEX, 60)


def _day_ganzhi(day):
    """Sexagenary day index (0-based), anchored so epoch doy 300 = #60."""
    return _mod(day - EPOCH_DAY_OF_YEAR + _DAY_300_GANZHI_INDEX, 60)


# --- layer definitions -------------------------------------------------------
LAYERS = {}


def _register(layer):
    LAYERS[layer["key"]] = layer
    return layer


def _time_of_day(day):
    """Seconds-of-day (exact, corpus clock frame) plus h/m/s reading.

    The datum's stored seconds (972527180) and its clock label (10:26:20.00)
    agree under the corpus frame offset (FRAME_OFFSET_SECONDS); every other
    instant renders in that same frame. Exact Fraction arithmetic.
    """
    sod = (day_to_unix_seconds(Fraction(day)) + FRAME_OFFSET_SECONDS) % 86400
    h = int(sod // 3600)
    m = int((sod % 3600) // 60)
    s = int(sod % 60)
    return {
        "seconds_of_day": frac_str(sod),
        "hh_mm_ss": "%02d:%02d:%02d" % (h, m, s),
        "sexagesimal_hits_60": _tau(sod) == 60,   # ms of epoch, repo Ch.2
        "tau_seconds_of_day": _tau(sod),
    }


_register(_layer := {
    "key": "gregorian",
    "name": "Gregorian (proleptic)",
    "civilization": "Roman/Western civil",
    "cycle_days": frac_str(GREGORIAN_YEAR),
    "render": lambda day: {
        "ymd": "%d-%02d-%02d" % gregorian_ymd(day),
        "day_of_year": day_of_year(*gregorian_ymd(day)),
        "weekday": weekday(day),
        "elapsed_gregorian_days": frac_str(day),
    },
})

_register(_layer := {
    "key": "julian",
    "name": "Julian (proleptic)",
    "civilization": "Roman",
    "cycle_days": frac_str(JULIAN_YEAR),
    "render": lambda day: {
        "ymd": "%d-%02d-%02d" % julian_ymd(day),
        "weekday": weekday(day),
    },
})

_register(_layer := {
    "key": "tropical",
    "name": "Mean tropical year",
    "civilization": "astronomical (repo SPRING_BIBLE Ch.12)",
    "cycle_days": frac_str(TROPICAL_YEAR),
    "render": lambda day: {
        "year": EPOCH_YEAR + _ifloor(day / TROPICAL_YEAR),
        "year_fraction": frac_str(_mod(day, TROPICAL_YEAR) / TROPICAL_YEAR),
        "years_since_epoch": frac_str(day / TROPICAL_YEAR),
    },
})

_register(_layer := {
    "key": "egyptian",
    "name": "Egyptian civil",
    "civilization": "Egypt",
    "cycle_days": frac_str(EGYPTIAN_YEAR),
    "render": lambda day: _egyptian_render(day, EGYPTIAN_MONTHS,
                                           EGYPTIAN_SEASONS, "epagomenal"),
})

_register(_layer := {
    "key": "babylonian",
    "name": "Babylonian schematic (360d) + sexagesimal day",
    "civilization": "Sumer/Babylon (sexagesimal, tau=12 - repo)",
    "cycle_days": frac_str(Fraction(360)),
    "render": lambda day: {
        "year": EPOCH_YEAR + _ifloor(day / 360),
        "month": int(_div(_mod(day, 360), 30)) + 1,
        "day_of_month": int(_mod(day, 30)) + 1,
        "sexagesimal_day": {
            "base": SEXAGESIMAL_BASE,
            "tau_base": _tau(SEXAGESIMAL_BASE),      # = 12 (repo)
            **{k: v for k, v in _time_of_day(day).items()
               if k != "sexagesimal_hits_60"},
        },
    },
})

_register(_layer := {
    "key": "mayan_long_count",
    "name": "Mayan Long Count",
    "civilization": "Maya (vigesimal, 80 = 4x20 - repo)",
    "cycle_days": frac_str(MAYAN_BAKTUN),
    "render": lambda day: {
        "baktun": _ifloor(day / 144000),
        "katun": _ifloor(day / 7200) % 20,
        "tun": _ifloor(day / 360) % 20,
        "uinal": _ifloor(day / 20) % 18,
        "kin": _ifloor(day % 20),
        "note": "proleptic relative count; absolute correlation out of scope",
    },
})

_register(_layer := {
    "key": "tzolkin",
    "name": "Tzolkin (260)",
    "civilization": "Maya (13 x 20, tau = 12 - repo)",
    "cycle_days": frac_str(TZOLKIN_LENGTH),
    "render": lambda day: {
        "number": int(day % 13) + 1,
        "name": TZOLKIN_NAMES[int(day % 20)],
        "tau": _tau(260),
    },
})

_register(_layer := {
    "key": "haab",
    "name": "Haab (365)",
    "civilization": "Maya",
    "cycle_days": frac_str(HAAB_LENGTH),
    "render": lambda day: {
        "month": HAAB_MONTHS[int(day % 365) // 20],
        "day_of_month": int(day % 365) % 20,
        "wayeb": bool(int(day % 365) >= 360),
    },
})

_register(_layer := {
    "key": "chinese_sexagenary",
    "name": "Chinese sexagenary (ganzhi)",
    "civilization": "China (year 2000 = Geng-Chen #17, doy 300 = #60 - repo)",
    "cycle_days": frac_str(CHINESE_CYCLE),
    "render": lambda day: {
        "year_index_1based": int(_year_ganzhi(day)) + 1,
        "year_ganzhi": STROKE[int(_year_ganzhi(day))],
        "day_index_1based": int(_day_ganzhi(day)) + 1,
        "day_ganzhi": STROKE[int(_day_ganzhi(day))],
    },
})

_register(_layer := {
    "key": "hebrew_metonic",
    "name": "Hebrew lunisolar (mean Metonic)",
    "civilization": "Israel/Hebrew (19-year, 235-month cycle)",
    "cycle_days": frac_str(METONIC_YEARS * TROPICAL_YEAR),
    "render": lambda day: {
        "year": EPOCH_YEAR + _ifloor(day / TROPICAL_YEAR),
        "golden_number": int(_mod(EPOCH_YEAR + _ifloor(day / TROPICAL_YEAR),
                                  19)) + 1,
        "mean_month": frac_str(day / HEBREW_MONTH),
        "month_in_cycle": int(_div(day, HEBREW_MONTH) % 235) + 1,
    },
})

_register(_layer := {
    "key": "hijri_tabular",
    "name": "Hijri (tabular 30-year)",
    "civilization": "Islamic (30 years, 10631 days, 11 leap)",
    "cycle_days": frac_str(HIJRI_30Y),
    "render": lambda day: {
        "year_in_cycle": int(_div(day, TROPICAL_YEAR) % 30),
        "month": int(_div(day, HIJRI_MONTH) % 12) + 1,
        "mean_month": frac_str(day / HIJRI_MONTH),
    },
})

_register(_layer := {
    "key": "persian_zoroastrian",
    "name": "Persian / Zoroastrian (365)",
    "civilization": "Iran (12 x 30 + 5 Gatha days)",
    "cycle_days": frac_str(EGYPTIAN_YEAR),
    "render": lambda day: _egyptian_render(day, ZOROASTRIAN_MONTHS,
                                           ["Spring", "Summer", "Autumn"],
                                           "Gatha"),
})

_register(_layer := {
    "key": "vedic_jovian",
    "name": "Vedic Jovian (60-year Brihaspati cycle)",
    "civilization": "India (Sulba-sutras, 60-year cycle - repo Ch.3)",
    "cycle_days": frac_str(JOVIAN_CYCLE * TROPICAL_YEAR),
    "render": lambda day: {
        "cycle_year": int(_div(day, TROPICAL_YEAR) % 60) + 1,
        "jupiter_years": frac_str(day / (12 * TROPICAL_YEAR)),
    },
})

_register(_layer := {
    "key": "puno_tick",
    "name": "Puno tick meta-calendar",
    "civilization": "this corpus (tick ladder 12/60/144/264/420/612, Ch.2)",
    "cycle_days": "continuous",
    "render": lambda day: {
        "day_of_epoch": frac_str(day),
        "tau_integer_day": _tau(int(day)),
        "sexagesimal_base_tau": _tau(SEXAGESIMAL_BASE),      # 12
        "tzolkin_tau": _tau(260),                             # 12
        "baktun_kin": int(144000),                            # 144 = 12^2 x 10^3
        "tick_ladder": [_tau(EPOCH_SECONDS_OF_DAY),
                        _tau(EPOCH_SECONDS_OF_DAY * 10**3),
                        _tau(EPOCH_SECONDS_OF_DAY * 10**6),
                        _tau(EPOCH_SECONDS_OF_DAY * 10**9),
                        _tau(EPOCH_SECONDS_OF_DAY * 10**12),
                        _tau(EPOCH_SECONDS_OF_DAY * 10**15)],
    },
})


def _egyptian_render(day, months, seasons, extra_name):
    d = int(_mod(day, 365))
    if d >= 360:
        return {"month": extra_name, "day": d - 360 + 1, "season": extra_name}
    month = d // 30
    return {
        "month": months[month],
        "day": d % 30 + 1,
        "season": seasons[month // 4],
        "year": EPOCH_YEAR + _ifloor(day / 365),
    }


def render(day, key=None):
    """Render a day offset in every layer (or one layer by key)."""
    if key is not None:
        return {key: LAYERS[key]["render"](day)}
    return {k: v["render"](day) for k, v in LAYERS.items()}
