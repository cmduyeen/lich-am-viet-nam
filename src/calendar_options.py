"""Bilingual holiday selection and optional personal annual dates."""

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .holidays import FIXED_LUNAR_HOLIDAYS, FIXED_SOLAR_HOLIDAYS, GIAO_THUA


@dataclass(frozen=True)
class HolidayRule:
    id: str
    calendar: str
    month: int
    day: int
    name_vi: str
    name_en: str
    description_vi: str = ''
    description_en: str = ''
    public: bool = False
    start_year: int = 1

    def name(self, language):
        return self.name_vi if language == 'vi' else self.name_en

    def description(self, language):
        return self.description_vi if language == 'vi' else self.description_en


_ENGLISH = [
    ('new-year', 'solar', 1, 1, "New Year's Day", 'The first day of the Gregorian year.'),
    ('reunification', 'solar', 4, 30, 'Reunification Day', 'Reunification of Vietnam.'),
    ('labour-day', 'solar', 5, 1, "International Workers' Day", "International Workers' Day."),
    ('national-day', 'solar', 9, 2, 'National Day', "Vietnam's National Day."),
    ('tet-1', 'lunar', 1, 1, 'Lunar New Year — Day 1', 'The first day of Vietnamese Lunar New Year.'),
    ('tet-2', 'lunar', 1, 2, 'Lunar New Year — Day 2', 'The second day of Vietnamese Lunar New Year.'),
    ('tet-3', 'lunar', 1, 3, 'Lunar New Year — Day 3', 'The third day of Vietnamese Lunar New Year.'),
    ('god-of-wealth', 'lunar', 1, 10, 'God of Wealth Day', 'The tenth day of the first lunar month.'),
    ('first-full-moon', 'lunar', 1, 15, 'First Full Moon Festival', 'The fifteenth day of the first lunar month.'),
    ('hung-kings', 'lunar', 3, 10, "Hung Kings' Commemoration Day", 'Commemorating the Hung Kings.'),
    ('buddha-birthday', 'lunar', 4, 15, "Buddha's Birthday", 'Observed on the fifteenth day of the fourth lunar month in Vietnam.'),
    ('doan-ngo', 'lunar', 5, 5, 'Doan Ngo Festival', 'The fifth day of the fifth lunar month.'),
    ('vu-lan', 'lunar', 7, 15, 'Vu Lan Festival', 'A Vietnamese Buddhist festival honoring parents and ancestors.'),
    ('mid-autumn', 'lunar', 8, 15, 'Mid-Autumn Festival', 'The fifteenth day of the eighth lunar month.'),
    ('kitchen-gods', 'lunar', 12, 23, 'Kitchen Gods Day', 'The twenty-third day of the twelfth lunar month.'),
    ('valentine', 'solar', 2, 14, "Valentine's Day", 'A celebration of love on February 14.'),
    ('international-women', 'solar', 3, 8, "International Women's Day", 'International Women’s Day on March 8.'),
    ('children', 'solar', 6, 1, "Children's Day", 'Children’s Day, observed on June 1 in Vietnam.'),
    ('family', 'solar', 6, 28, 'Vietnamese Family Day', 'Vietnamese Family Day on June 28.'),
    ('vietnamese-women', 'solar', 10, 20, "Vietnamese Women's Day", 'Vietnamese Women’s Day on October 20.'),
    ('teachers', 'solar', 11, 20, "Vietnamese Teachers' Day", 'Vietnamese Teachers’ Day on November 20.'),
    ('culture', 'solar', 11, 24, 'Vietnam Culture Day', 'Vietnam Culture Day on November 24, effective from 2026 under Resolution 28/2026/QH16.'),
    ('christmas-eve', 'solar', 12, 24, 'Christmas Eve', 'Christmas Eve on December 24.'),
    ('christmas', 'solar', 12, 25, 'Christmas', 'Christmas on December 25.'),
    ('han-thuc', 'lunar', 3, 3, 'Han Thuc Festival', 'The third day of the third lunar month.'),
    ('ha-nguyen', 'lunar', 10, 15, 'Ha Nguyen Festival', 'The fifteenth day of the tenth lunar month.'),
    ('new-year-eve', 'eve', 0, 0, "Lunar New Year's Eve", 'The last day of the Vietnamese lunar year.'),
]


def _catalog():
    result = {}
    for id, calendar, month, day, name, description in _ENGLISH:
        original = GIAO_THUA if calendar == 'eve' else (
            FIXED_LUNAR_HOLIDAYS if calendar == 'lunar' else FIXED_SOLAR_HOLIDAYS
        )[(month, day)]
        result[id] = HolidayRule(id, calendar, month, day, original.name, name,
                                 original.description, description, original.is_public_holiday, original.start_year)
    return result


HOLIDAYS = _catalog()


def select_holidays(value='all'):
    if value == 'all':
        return tuple(HOLIDAYS.values())
    if value == 'none':
        return ()
    ids = [item.strip() for item in value.split(',')]
    unknown = set(ids) - HOLIDAYS.keys()
    if unknown:
        raise ValueError('Unknown holiday IDs: ' + ', '.join(sorted(unknown)))
    return tuple(HOLIDAYS[id] for id in dict.fromkeys(ids))


def load_custom_holidays(path):
    """Annual dates in regular lunar months, or Gregorian month/day dates."""
    data = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    if not isinstance(data, list):
        raise ValueError('Custom holidays must be a JSON list')
    result = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError('Each custom holiday must be an object')
        calendar = item.get('calendar')
        month, day = item.get('month'), item.get('day')
        if calendar not in ('lunar', 'solar'):
            raise ValueError('Custom calendar must be lunar or solar')
        if type(month) is not int or type(day) is not int:
            raise ValueError('Custom month and day must be integers')
        if calendar == 'lunar':
            if not (1 <= month <= 12 and 1 <= day <= 30):
                raise ValueError('Invalid lunar month/day')
        else:
            date(2000, month, day)  # February 29 is allowed in leap years.
        names = item.get('name')
        if not isinstance(names, dict) or any(
            not isinstance(names.get(lang), str) or not names[lang].strip()
            for lang in ('vi', 'en')
        ):
            raise ValueError('Custom name must contain nonempty vi and en strings')
        result.append(HolidayRule(f'custom-{index}', calendar, month, day,
                                  names['vi'].strip(), names['en'].strip()))
    return tuple(result)
