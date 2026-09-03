"""calendars_audit: the second real-subsystem audit -- the universal
calendar's exactness properties certified as machine-readable statements.

Audited invariants (pure integer/Fraction arithmetic, deterministic, no I/O):
    L18_gregorian_roundtrip:  gregorian_ymd(civil_to_days(y,m,d)) == (y,m,d)
        over one full Gregorian cycle (146097 days = 400 years, covering
        every leap-year case exactly once);
    L19_julian_roundtrip:    julian_ymd over one Julian cycle (1461 days);
    L20_tzolkin_periodicity: render(d)["tzolkin"] == render(d+260)["tzolkin"]
        exhaustively over d in 0..999 (the 260-day sacred round);
    L21_gregorian_monotonicity: gregorian_ymd(d+1) > gregorian_ymd(d)
        (lexicographic) over d in 0..146096;
    L22_day_of_year_consistent: 1 <= day_of_year(y,m,d) <= 366 for every
        date in the Gregorian cycle.
HONEST NEGATIVE (rejected, not introduced):
    L23_tropical_integer: "tropical year is an exact integer" -- FALSE at
    day=1 (year_fraction != 0); the code correctly uses 365.2422.
"""
from fractions import Fraction

from calendars.axis import civil_to_days, gregorian_ymd, julian_ymd, julian_to_days
from calendars.axis import day_of_year as _doy
from calendars import layers

_GREG_CYCLE = 146097   # 400-year Gregorian cycle: days 0..146096
_JUL_CYCLE = 1461      # 4-year Julian cycle:    days 0..1460
_TZOL_WINDOW = 1000    # tzolkin periodicity check: days 0..999


def _greg_roundtrip(day):
    y, m, d = gregorian_ymd(day)
    return gregorian_ymd(civil_to_days(y, m, d)) == (y, m, d)


def _jul_roundtrip(day):
    y, m, d = julian_ymd(day)
    return julian_ymd(julian_to_days(y, m, d)) == (y, m, d)


def _tzol_periodic(day):
    return (layers.render(day)["tzolkin"]
            == layers.render(day + 260)["tzolkin"])


def _greg_mono(day):
    d1 = gregorian_ymd(day)
    d2 = gregorian_ymd(day + 1)
    return d2 > d1


def _doy_ok(day):
    y, m, d = gregorian_ymd(day)
    doy = _doy(y, m, d)
    return 1 <= doy <= 366


def _tropical_is_integer_claim(day):
    """The false candidate law: 'tropical year is an exact integer',
    i.e. year_fraction == 0 at every day.  TRUE at day=0 (the datum),
    FALSE at day=1 (year_fraction != 0) -- HONEST_NEGATIVE with
    first_failure at day=1."""
    yf = layers.render(day)["tropical"]["year_fraction"]
    return Fraction(yf) == 0


def _certify(label, meta, pred, domain):
    from experiments.emanation import law_checker as lc
    return lc.certify_statement(label, meta, pred, list(domain))


def calendar_certificates():
    """All six calendar statement certificates (5 PASS + 1 HONEST_NEGATIVE)."""
    certs = []
    certs.append(_certify(
        "L18_gregorian_roundtrip",
        {"domain": "Gregorian roundtrip: gregorian_ymd(civil_to_days(y,m,d))"
                   " == (y,m,d) for all integer days 0..146096 "
                   "(one full 400-year cycle; every leap-year case once)",
         "method": "exhaustive, pure integer arithmetic (Hinnant algorithm)"},
        _greg_roundtrip, range(_GREG_CYCLE)))
    certs.append(_certify(
        "L19_julian_roundtrip",
        {"domain": "Julian roundtrip over one 4-year Julian cycle "
                   "(days 0..1460)",
         "method": "exhaustive"},
        _jul_roundtrip, range(_JUL_CYCLE)))
    certs.append(_certify(
        "L20_tzolkin_periodicity",
        {"domain": "Tzolkin 260-day sacred round: render(d) == render(d+260) "
                   "for all d in 0..999",
         "method": "exhaustive"},
        _tzol_periodic, range(_TZOL_WINDOW)))
    certs.append(_certify(
        "L21_gregorian_monotonicity",
        {"domain": "Gregorian date ordering: gregorian_ymd(d+1) > "
                   "gregorian_ymd(d) for all d in 0..146096 (lexicographic)",
         "method": "exhaustive"},
        _greg_mono, range(_GREG_CYCLE - 1)))
    certs.append(_certify(
        "L22_day_of_year_consistent",
        {"domain": "day_of_year(y,m,d) in 1..366 for every date in the "
                   "400-year Gregorian cycle",
         "method": "exhaustive"},
        _doy_ok, range(_GREG_CYCLE)))
    certs.append(_certify(
        "L23_tropical_integer",
        {"domain": "candidate: tropical year is an exact integer "
                   "(year_fraction == 0 at every day); expected HONEST_NEGATIVE",
         "method": "exhaustive over days 0..999"},
        _tropical_is_integer_claim, range(_TZOL_WINDOW)))
    return certs