"""calendars.c0 - C0 and C_current calibrated from repo assets only.

The calendar is an emanation clock: it counts how many units of the corpus's
own constant have emanated from the datum. C0 is measured, not chosen
(data/c0_law_data.json, origin: C0 = V(q0) = H(q0,0) = 24.434792); the
calendar uses C0 itself as a time unit - one "emanation day" is C0 days -
and C_current is the exact rational reading of how many such units have
emanated by a given instant:

    emanation_count(D) = D / C0        (exact Fraction, D = day offset)
    C_current          = emanation_count(D)

At the datum D=0 the count is 0, so C_current = 0 and the law C0 = C0 holds
exactly (the conservative flow conserves H). C_current is a *reading* of
accumulated emanational time, not a change in C0 - the constant itself never
drifts. [honest wall]
"""

from fractions import Fraction

# --- measured constants (repo) ----------------------------------------------
C0 = Fraction(24434792, 10**6)        # 24.434792, data/c0_law_data.json origin
C0_README = Fraction(244328733, 10**7)  # 24.4328733, README "classical
                                        # conservative ground state" - a
                                        # distinct measured object, kept apart
C0_UNIT_DAYS = C0


def emanation_count(day):
    """Exact rational number of C0-units emanated from the datum."""
    return Fraction(day) / C0


def c_current(day):
    """The current reading of the emanation constant at day offset D."""
    return emanation_count(day)


def decimal_string(frac, places=60):
    """Exact decimal expansion of frac to `places` digits (no rounding loss
    in the p/q representation - this is only a display view)."""
    frac = Fraction(frac)
    sign = "-" if frac < 0 else ""
    frac = abs(frac)
    whole, rem = divmod(frac.numerator, frac.denominator)
    digits = []
    for _ in range(places):
        rem *= 10
        d, rem = divmod(rem, frac.denominator)
        digits.append(str(d))
    return "%s%d.%s" % (sign, whole, "".join(digits).rstrip("0") or "0")


def adjust(day):
    """The C0/C_current calibration for a day offset (exact strings)."""
    n = emanation_count(day)
    return {
        "C0": str(C0),                     # exact p/q of 24.434792
        "C0_decimal": decimal_string(C0),
        "C0_unit_days": str(C0_UNIT_DAYS),
        "emanation_count": str(n),         # exact p/q
        "C_current": str(n),               # exact p/q - never truncated
        "C_current_decimal": decimal_string(n),
        "law": "C0 = V(q0) = H(q0, 0); on the conservative flow H = C0 "
               "exactly, so C_current is the emanation count D/C0, not a "
               "drift in C0.",
    }
