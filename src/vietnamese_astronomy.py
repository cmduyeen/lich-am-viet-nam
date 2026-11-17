"""Modern Vietnamese lunar dates from astronomical new moons and solar terms.

Uses the existing lunar-python ephemeris, converting instants to UTC+7 BEFORE
assigning civil days. Month 11 contains the winter solstice; the first month
without a principal solar term is intercalary when there are 13 months.
Supported modern civil-calendar interval: 1900-2099.
"""
from datetime import date
from functools import lru_cache
from math import floor, pi
from lunar_python.util import ShouXingUtil as Astronomy

J2000 = 2451545
TIME_OFFSET = 7 / 24
SYNODIC_MONTH = 29.530588853


def _julian_day(value):
    return value.toordinal() + 1721425


@lru_cache(maxsize=8192)
def _new_moon_day(index):
    terrestrial = Astronomy.msaLonT(index * 2 * pi) * 36525
    universal = terrestrial - Astronomy.dtT(terrestrial)
    return floor(universal + J2000 + TIME_OFFSET + 0.5)


@lru_cache(maxsize=8192)
def _solar_sector(day):
    universal = day - 0.5 - TIME_OFFSET - J2000
    terrestrial = universal + Astronomy.dtT(universal)
    longitude = Astronomy.saLon(terrestrial / 36525, -1) % (2 * pi)
    return floor(longitude / (pi / 6))


def _month_start(day):
    # The mean synodic estimate can lie on either side of a civil-day boundary.
    # Bracket actual astronomical new moons instead of assuming one correction.
    index = floor((day - 2451550.09765) / SYNODIC_MONTH)
    while _new_moon_day(index) > day:
        index -= 1
    while _new_moon_day(index + 1) <= day:
        index += 1
    return _new_moon_day(index), index


@lru_cache(maxsize=256)
def _month_eleven(year):
    day = _julian_day(date(year, 12, 31))
    moon, index = _month_start(day)
    if _solar_sector(moon) >= 9:
        moon = _new_moon_day(index - 1)
    return moon


@lru_cache(maxsize=256)
def _leap_offset(month_eleven):
    index = round((month_eleven - 2451550.09765) / SYNODIC_MONTH)
    previous = _solar_sector(_new_moon_day(index + 1))
    for offset in range(2, 15):
        sector = _solar_sector(_new_moon_day(index + offset))
        if sector == previous:
            return offset - 1
        previous = sector
    raise ValueError('Unable to determine Vietnamese leap month')


@lru_cache(maxsize=8192)
def vietnamese_date(value):
    if not 1900 <= value.year <= 2099:
        raise ValueError('Vietnamese astronomical conversion supports 1900-2099')
    day = _julian_day(value)
    start, index = _month_start(day)
    first = last = _month_eleven(value.year)
    if first >= start:
        year = value.year
        first = _month_eleven(value.year - 1)
    else:
        year = value.year + 1
        last = _month_eleven(value.year + 1)
    offset = floor((start - first) / 29)
    month, leap = offset + 11, False
    if last - first > 365:
        extra = _leap_offset(first)
        if offset >= extra:
            month = offset + 10
            leap = offset == extra
    if month > 12:
        month -= 12
    if month >= 11 and offset < 4:
        year -= 1
    return year, -month if leap else month, day - start + 1
