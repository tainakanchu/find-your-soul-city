"""Daylight module: pure computation, no network."""

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from soulcity_etl import daylight as d


def test_singapore_sunset_is_stable_around_19h():
    tz = d._zone("Asia/Singapore")
    for day in (d.JUNE, d.DECEMBER):
        h = d._decimal_hours(d.sunset_local(1.35, 103.82, tz, day), day)
        assert 19.0 < h < 19.3


def test_reykjavik_sunset_after_midnight_is_above_24():
    tz = d._zone("Atlantic/Reykjavik")
    assert 24.0 < d._decimal_hours(d.sunset_local(64.15, -21.94, tz, d.JUNE), d.JUNE) < 24.2


def test_polar_day_raises():
    tz = d._zone("Arctic/Longyearbyen")
    try:
        d.sunset_local(78.2, 15.6, tz, d.JUNE)
    except ValueError:
        return
    raise AssertionError("expected ValueError for midnight sun")


def test_standard_offset_ireland_morocco_sydney():
    assert d.standard_offset_h(d._zone("Europe/Dublin")) == 0
    assert d.standard_offset_h(d._zone("Africa/Casablanca")) == 1
    assert d.standard_offset_h(d._zone("Australia/Sydney")) == 10


def test_sunrise_equation_agrees_with_astral():
    tz = d._zone("Europe/Madrid")
    a = d._decimal_hours(d.sunset_local(40.4, -3.7, tz, d.JUNE), d.JUNE)
    b = d.independent_sunset_local_h(40.4, -3.7, tz, d.JUNE)
    assert abs(a - b) * 60 < 2
    assert dt.date(2025, 3, 20) == d.EQUINOX
