"""One all-day event per date, with optional Vietnamese or English holidays."""
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import re

from icalendar import Calendar, Event

from .calendar_options import select_holidays
from .config import CALENDAR_DESCRIPTION, CALENDAR_VERSION, PRODID, TIMEZONE
from .ics import write_calendar
from .lunar_converter import to_lunar


def _build_event_for_day(d, lunar, dtstamp, language='vi', holidays=None):
    day, month = lunar.lunar_day, lunar.lunar_month_abs
    rules = select_holidays() if holidays is None else holidays
    # A single event can include multiple holidays falling on the same date.
    matches = []
    for rule in rules:
        if rule.calendar == 'solar':
            matched = (d.month, d.day) == (rule.month, rule.day)
        elif rule.calendar == 'lunar':
            matched = not lunar.is_leap_month and (month, day) == (rule.month, rule.day)
        else:
            matched = to_lunar(d + timedelta(days=1)).lunar_year != lunar.lunar_year
        if matched:
            matches.append(rule)

    leap = (' nhuận' if language == 'vi' else ' (leap)') if lunar.is_leap_month else ''
    summary = f'{day}/{month}{leap}'
    if matches:
        summary += ' • ' + ' • '.join(rule.name(language) for rule in matches)
    elif day in (1, 15):
        label = {1: 'Mùng 1', 15: 'Rằm'} if language == 'vi' else {
            1: 'First lunar day', 15: '15th lunar day'
        }
        summary += ' • ' + label[day]

    description = (
        f'Ngày {day} tháng {month} âm lịch ({lunar.can_chi_year})'
        if language == 'vi' else
        f'Lunar day {day}, month {month}, year {lunar.lunar_year}'
    )
    lines = [description]
    if lunar.is_leap_month:
        lines.append('Tháng nhuận' if language == 'vi' else 'Leap lunar month')
    for rule in matches:
        detail = rule.description(language)
        lines.append(f'{rule.name(language)}: {detail}' if detail else rule.name(language))

    event = Event()
    prefix = 'vnlunar' if language == 'vi' else 'vnlunar-en'
    event.add('uid', f'{prefix}-{d:%Y%m%d}@cmduyeen')
    parameters = {'LANGUAGE': 'en'} if language == 'en' else {}
    event.add('summary', summary, parameters=parameters)
    event.add('description', '\n'.join(lines), parameters=parameters)
    event.add('dtstart', d)
    event.add('dtend', d + timedelta(days=1))
    if any(rule.public for rule in matches):
        event.add('x-microsoft-cdo-importance', '2')
        color = '#E53935'
    else:
        color = '#FB8C00' if day in (1, 15) else '#1E88E5'
    event.add('color', color)
    event.add('dtstamp', dtstamp)
    return event


class LunarCalendarGenerator:
    """Generate every lunar day; holiday selection only changes annotations."""

    def __init__(self, language='vi', holidays='all', custom_holidays=()):
        if language not in ('vi', 'en'):
            raise ValueError('Language must be vi or en')
        self.language = language
        self.holidays = select_holidays(holidays) + tuple(custom_holidays)

    def _make_calendar(self, name):
        cal = Calendar()
        cal.add('prodid', PRODID)
        cal.add('version', CALENDAR_VERSION)
        cal.add('calscale', 'GREGORIAN')
        cal.add('method', 'PUBLISH')
        cal.add('x-wr-calname', name)
        cal.add('x-wr-timezone', TIMEZONE)
        description = CALENDAR_DESCRIPTION if self.language == 'vi' else (
            'Daily Vietnamese lunar dates with selected holidays. '
            'Dates follow Vietnam time (GMT+7).'
        )
        cal.add('x-wr-caldesc', description)
        cal.add('x-apple-calendar-color', '#E53935')
        return cal

    def generate_year(self, year):
        return self.generate_range(year, year)

    def generate_range(self, start_year, end_year):
        if not 1900 <= start_year <= end_year <= 2098:
            raise ValueError('Supported year range: 1900–2098')
        title = 'Lịch Âm Việt Nam' if self.language == 'vi' else 'Vietnamese Lunar Calendar'
        years = str(start_year) if start_year == end_year else f'{start_year}–{end_year}'
        cal = self._make_calendar(f'{title} {years}')
        current, end = date(start_year, 1, 1), date(end_year, 12, 31)
        stamp = datetime.now(timezone.utc)
        while current <= end:
            cal.add_component(_build_event_for_day(
                current, to_lunar(current), stamp, self.language, self.holidays
            ))
            current += timedelta(days=1)
        return cal

    @staticmethod
    def save(cal, filepath):
        filepath = Path(filepath)
        match = re.fullmatch(r'(.+?)_(?:\d{4}(?:_\d{4})?|latest)\.ics', filepath.name)
        latest = match.group(1) + '_latest.ics' if match else filepath.name
        previous = filepath if filepath.exists() else filepath.with_name(latest)
        write_calendar(cal, filepath, previous=previous)
