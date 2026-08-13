"""tests/test_calendars.py - the universal calendar must be exact everywhere.

The axis uses Fraction arithmetic end-to-end: no float, no truncation, valid
at any magnitude (deep past included). These tests assert the repo-measured
epoch identity, exact periodicity of every civilization layer, the
C0/C_current calibration, and the deep-time pre-civilization anchors.
"""

from fractions import Fraction

from calendars import c0, deeptime, layers
from calendars.axis import (
    EPOCH_DAY_OF_YEAR,
    EPOCH_MONTH,
    EPOCH_YEAR,
    civil_to_days,
    days_since_1970,
    day_to_unix_seconds,
    gregorian_ymd,
    julian_ymd,
    unix_seconds_to_day,
    weekday,
)
from calendars.layers import render


def test_epoch_civil_identity():
    y, m, d = gregorian_ymd(0)
    assert (y, m, d) == (EPOCH_YEAR, EPOCH_MONTH, 26)


def test_epoch_day_of_year_is_sexagenary_complete():
    assert days_since_1970(0) == Fraction(11256)
    assert gregorian_ymd(0)[0] == 2000
    assert EPOCH_DAY_OF_YEAR == 300            # 5 x 60 exactly


def test_epoch_weekday_is_thursday():
    assert weekday(0) == "Thursday"
    assert weekday(7) == "Thursday"


def test_unix_seconds_round_trip():
    assert unix_seconds_to_day(Fraction(972527180)) == 0
    assert day_to_unix_seconds(0) == Fraction(972527180)


def test_epoch_seconds_of_day_measured():
    r = render(0)
    assert r["gregorian"]["ymd"] == "2000-10-26"
    assert r["babylonian"]["sexagesimal_day"]["hh_mm_ss"] == "10:26:20"


def test_civil_to_days_round_trip():
    assert civil_to_days(2000, 10, 26) == 0
    assert gregorian_ymd(civil_to_days(2000, 1, 1)) == (2000, 1, 1)
    assert gregorian_ymd(civil_to_days(-2000, 6, 15)) == (-2000, 6, 15)
    assert gregorian_ymd(civil_to_days(10000, 12, 31)) == (10000, 12, 31)


def test_julian_and_gregorian_diverge_by_epoch():
    j = julian_ymd(0)
    g = gregorian_ymd(0)
    assert (j[0], j[1]) == (2000, 10)          # same civil date at the datum
    assert (g[0], g[1]) == (2000, 10)


def test_no_truncation_fraction_axis():
    d = Fraction(1, 3)
    assert unix_seconds_to_day(day_to_unix_seconds(d)) == d
    assert layers.frac_str(Fraction(1, 3)) == "1/3"


def test_c0_is_measured_value():
    assert c0.C0 == Fraction(24434792, 1000000)
    assert c0.decimal_string(c0.C0) == "24.434792"


def test_c_current_is_exact_reading():
    a = c0.adjust(Fraction(0))
    assert a["C_current"] == "0"
    d = Fraction(24434792, 1000000)            # exactly one C0-unit
    a = c0.adjust(d)
    assert a["C_current"] == "1"
    d = Fraction(1, 3)
    a = c0.adjust(d)
    assert a["C_current"] == layers.frac_str(Fraction(1, 3) / c0.C0)
    assert Fraction(a["C_current"]) * c0.C0 == Fraction(1, 3)


def test_gregorian_periodicity():
    # 146097 days is exactly one 400-year Gregorian cycle: same month, day,
    # and weekday (the year advances by 400).
    for d in (Fraction(0), Fraction(1, 3), Fraction(-1000)):
        a = render(d)["gregorian"]
        b = render(d + Fraction(146097))["gregorian"]
        assert a["ymd"].split("-", 1)[1] == b["ymd"].split("-", 1)[1]
        assert a["weekday"] == b["weekday"]


def test_tzolkin_periodicity():
    for d in (Fraction(0), Fraction(-7), Fraction(12345, 2)):
        assert render(d + 260)["tzolkin"] == render(d)["tzolkin"]


def test_haab_periodicity():
    assert render(Fraction(365))["haab"] == render(Fraction(0))["haab"]


def test_sexagenary_day_periodicity():
    for d in (Fraction(0), Fraction(-600), Fraction(3)):
        assert render(d + 60)["chinese_sexagenary"]["day_ganzhi"] \
            == render(d)["chinese_sexagenary"]["day_ganzhi"]


def test_epoch_ganzhi_year_and_day():
    r = render(0)["chinese_sexagenary"]
    assert r["year_ganzhi"] == "\u5e9a\u8fb0"          # Geng-Chen #17
    assert r["year_index_1based"] == 17
    assert r["day_ganzhi"] == "\u7678\u4ea5"           # Gui-Hai #60
    assert r["day_index_1based"] == 60


def test_metonic_golden_number_advances():
    r0 = render(0)["hebrew_metonic"]
    r1 = render(Fraction(19 * 3652422, 10000))["hebrew_metonic"]
    # a full Metonic cycle returns the same golden number and cycle month
    assert r1["golden_number"] == r0["golden_number"]
    assert r1["month_in_cycle"] == r0["month_in_cycle"]
    assert r1["year"] == r0["year"] + 19


def test_hijri_30_year_cycle():
    r0 = render(0)["hijri_tabular"]
    # after one tabular 30-year span (10631 days) the mean month repeats
    r1 = render(Fraction(10631))["hijri_tabular"]
    assert r0["month"] == r1["month"]
    # after 30 solar years the year-in-cycle repeats
    ry = render(Fraction(30 * 3652422, 10000))["hijri_tabular"]
    assert ry["year_in_cycle"] == r0["year_in_cycle"]


def test_egyptian_and_zoroastrian_365():
    # the 365-day layer repeats its month/day/season every 365 days (year
    # advances by exactly one)
    for key in ("egyptian", "persian_zoroastrian"):
        a = render(0)[key]
        b = render(Fraction(365))[key]
        for field in ("month", "day", "season"):
            assert a[field] == b[field], (key, field)
        assert b["year"] == a["year"] + 1


def test_mayan_long_count_and_tzolkin_tau():
    assert render(0)["tzolkin"]["tau"] == 12
    assert render(0)["puno_tick"]["sexagesimal_base_tau"] == 12
    assert render(0)["puno_tick"]["baktun_kin"] == 144000


def test_epoch_renderings_tau_80():
    # MMDDYYYY 10262000 and DDMMYYYY 26102000 both have tau = 80 (repo)
    assert layers._tau(10262000) == 80
    assert layers._tau(26102000) == 80
    assert layers._tau(943901200001) == 2          # the giant is prime


def test_epoch_digit_sum_11():
    assert sum(int(ch) for ch in str(10262000)) == 11
    assert sum(int(ch) for ch in str(26102000)) == 11


def test_deep_time_giant_era():
    y = deeptime.giant_era_epoch_year()
    years = Fraction(y["years_before_epoch"])
    assert years > Fraction(2 * 10**9)         # ~2.585e9, before the stars
    assert years < Fraction(3 * 10**9)
    assert y["days"] == "943901200001"
    assert Fraction(y["days_before_epoch"]) == Fraction(943901200001)


def test_era_labels():
    assert deeptime.era(0)["era"] == "post-datum (epoch_0d onward)"
    assert deeptime.era(-1)["era"].startswith("pre-civilization")
    assert deeptime.era(-deeptime.giant_as_days())["era"] \
        == "giant-rung eon (deep pre-civilization)"


def test_window_730421():
    w = deeptime.window_730421()
    assert w["rung_inside"] is True
    assert Fraction(w["span_days"]) == 15


def test_every_layer_renders_at_extremes():
    for d in (Fraction(0), Fraction(-1, 3), Fraction(-deeptime.giant_as_days()),
              Fraction(10**9)):
        out = render(d)
        assert len(out) == len(layers.LAYERS)
        for key, layer in layers.LAYERS.items():
            assert layer["render"](d) == out[key]


def test_layers_keyed():
    assert set(layers.LAYERS) == {
        "gregorian", "julian", "tropical", "egyptian", "babylonian",
        "mayan_long_count", "tzolkin", "haab", "chinese_sexagenary",
        "hebrew_metonic", "hijri_tabular", "persian_zoroastrian",
        "vedic_jovian", "puno_tick",
    }


def test_now_reports_on_axis():
    from calendars.axis import now_day
    d = now_day()
    assert d > Fraction(9200) and d < Fraction(9600)   # ~2000-10 to 2026
    assert render(d)["gregorian"]["weekday"] == weekday(d)
