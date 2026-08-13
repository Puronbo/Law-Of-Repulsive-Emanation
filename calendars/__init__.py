"""calendars - the universal calendar.

One exact, untruncated day axis (calendars.axis) with every civilization's
calendar as a layer over it (calendars.layers), C0/C_current calibration
from repo assets only (calendars.c0), and deep pre-civilization era anchors
(calendars.deeptime).
"""

from calendars.report import build_report  # noqa: F401

__all__ = ["build_report"]
