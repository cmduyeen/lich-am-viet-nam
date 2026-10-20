# ============================================================
# ics_generator.py — Tạo file iCalendar (.ics) Lịch Âm Việt Nam
# ============================================================
from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

import pytz
from icalendar import Calendar, Event

try:
    from .config import (
        CALENDAR_NAME, CALENDAR_DESCRIPTION,
        PRODID, CALENDAR_VERSION, TIMEZONE,
        CALENDAR_NAME_EN, CALENDAR_DESCRIPTION_EN, PRODID_EN,
        HEAVENLY_STEMS_EN, EARTHLY_BRANCHES_EN,
        MINIMAL_CALENDAR_NAME_EN, MINIMAL_CALENDAR_DESCRIPTION_EN,
        FULL_MOON_NOTE_EN, LUNAR_NEW_YEAR_NOTE_EN,
        MINIMAL_CALENDAR_NAME, MINIMAL_CALENDAR_DESCRIPTION,
        FULL_MOON_NOTE, LUNAR_NEW_YEAR_NOTE,
    )
    from .holidays import (
        FIXED_SOLAR_HOLIDAYS, FIXED_LUNAR_HOLIDAYS,
        GIAO_THUA, HolidayInfo,
    )
    from .lunar_converter import to_lunar, is_last_day_of_lunar_month, LunarDate
except ImportError:
    from config import (
        CALENDAR_NAME, CALENDAR_DESCRIPTION,
        PRODID, CALENDAR_VERSION, TIMEZONE,
        CALENDAR_NAME_EN, CALENDAR_DESCRIPTION_EN, PRODID_EN,
        HEAVENLY_STEMS_EN, EARTHLY_BRANCHES_EN,
        MINIMAL_CALENDAR_NAME_EN, MINIMAL_CALENDAR_DESCRIPTION_EN,
        FULL_MOON_NOTE_EN, LUNAR_NEW_YEAR_NOTE_EN,
        MINIMAL_CALENDAR_NAME, MINIMAL_CALENDAR_DESCRIPTION,
        FULL_MOON_NOTE, LUNAR_NEW_YEAR_NOTE,
    )
    from holidays import (
        FIXED_SOLAR_HOLIDAYS, FIXED_LUNAR_HOLIDAYS,
        GIAO_THUA, HolidayInfo,
    )
    from lunar_converter import to_lunar, is_last_day_of_lunar_month, LunarDate


def _build_event_for_day(
    d: date, lunar: LunarDate, language: str = 'vi', minimal: bool = False,
) -> Event:
    """Tạo VEVENT tối giản cho 1 ngày: Ngày âm + Ngày lễ lớn nếu có."""
    day = lunar.lunar_day
    m = lunar.lunar_month_abs

    # 1. Xác định ngày lễ lớn (nếu có)
    holiday: Optional[HolidayInfo] = None

    if not minimal:
        if m == 12 and is_last_day_of_lunar_month(d):
            holiday = GIAO_THUA
        elif (m, day) in FIXED_LUNAR_HOLIDAYS:
            holiday = FIXED_LUNAR_HOLIDAYS[(m, day)]
        elif (d.month, d.day) in FIXED_SOLAR_HOLIDAYS:
            holiday = FIXED_SOLAR_HOLIDAYS[(d.month, d.day)]

    # 2. Tiêu đề (Summary): Tối giản, tinh tế
    if minimal:
        summary = 'Rằm' if day == 15 else 'Tết Nguyên Đán'
    elif holiday:
        summary = f'{day}/{m} • {holiday.name}'
    elif day == 1:
        summary = f'{day}/{m} • Mùng 1'
    elif day == 15:
        summary = f'{day}/{m} • Rằm'
    else:
        summary = f'{day}/{m}'

    # 3. Mô tả (Description): Súc tích, không rối mắt
    desc_lines = [f'Ngày {day} tháng {m} âm lịch ({lunar.can_chi_year})']
    if minimal:
        month_label = f'{m} nhuận' if lunar.is_leap_month else str(m)
        desc_lines = [f'Ngày {day} tháng {month_label} âm lịch ({lunar.can_chi_year})']
        desc_lines.append(FULL_MOON_NOTE if day == 15 else LUNAR_NEW_YEAR_NOTE)
    elif holiday:
        desc_lines.append(f'{holiday.name}: {holiday.description}')
    description = '\n'.join(desc_lines)

    if language == 'en':
        summary = f'Lunar {day}/{m}'
        if lunar.is_leap_month:
            summary += ' (leap month)'
        if minimal:
            summary = 'Full Moon' if day == 15 else 'Lunar New Year'
        elif holiday:
            if not holiday.name_en or not holiday.description_en:
                raise ValueError(f'Missing English translation for holiday: {holiday.name}')
            summary += f' • {holiday.name_en}'
        elif day == 1:
            summary += ' • First Day of Lunar Month'
        elif day == 15:
            summary += ' • Full Moon'

        stem, branch = lunar.can_chi_year.split()
        year_name = f'{HEAVENLY_STEMS_EN[stem]} {EARTHLY_BRANCHES_EN[branch]}'
        month_label = 'leap month' if lunar.is_leap_month else 'month'
        desc_lines = [f'Lunar day {day}, {month_label} {m} ({year_name} year)']
        if minimal:
            desc_lines.append(FULL_MOON_NOTE_EN if day == 15 else LUNAR_NEW_YEAR_NOTE_EN)
        elif holiday:
            desc_lines.append(f'{holiday.name_en}: {holiday.description_en}')
        description = '\n'.join(desc_lines)

    # 4. Khởi tạo VEVENT
    event = Event()
    uid_prefix = 'vnlunar-en' if language == 'en' else 'vnlunar'
    if minimal:
        uid_prefix += '-minimal'
    event.add('uid', f"{uid_prefix}-{d.strftime('%Y%m%d')}@cmduyeen")
    event.add('summary', summary)
    event.add('description', description)
    event.add('dtstart', d)
    event.add('dtend', d + timedelta(days=1))

    # Đánh dấu ngày nghỉ lễ chính thức
    if (minimal and day == 1) or (holiday and holiday.is_public_holiday):
        event.add('x-microsoft-cdo-importance', '2')
        event.add('color', '#E53935')  # Đỏ nổi bật cho ngày nghỉ lễ
    elif day in (1, 15):
        event.add('color', '#FB8C00')  # Cam nhẹ cho Mùng 1 & Rằm
    else:
        event.add('color', '#1E88E5')  # Xanh dương trang nhã cho ngày thường

    tz = pytz.timezone(TIMEZONE)
    event.add('dtstamp', datetime.now(tz))

    return event


class LunarCalendarGenerator:
    """Tạo file .ics lịch âm Việt Nam theo khoảng năm cho trước."""

    def __init__(self, language: str = 'vi', minimal: bool = False):
        if language not in ('vi', 'en'):
            raise ValueError(f'Unsupported calendar language: {language}')
        self.language = language
        self.minimal = minimal
        self.calendar_name = CALENDAR_NAME_EN if language == 'en' else CALENDAR_NAME
        self.calendar_description = CALENDAR_DESCRIPTION_EN if language == 'en' else CALENDAR_DESCRIPTION
        if minimal:
            self.calendar_name = MINIMAL_CALENDAR_NAME_EN if language == 'en' else MINIMAL_CALENDAR_NAME
            self.calendar_description = (
                MINIMAL_CALENDAR_DESCRIPTION_EN if language == 'en' else MINIMAL_CALENDAR_DESCRIPTION
            )

    def _make_calendar(self, name: Optional[str] = None) -> Calendar:
        """Khởi tạo Calendar object với metadata chuẩn."""
        cal = Calendar()
        cal.add('prodid', PRODID_EN if self.language == 'en' else PRODID)
        cal.add('version', CALENDAR_VERSION)
        cal.add('calscale', 'GREGORIAN')
        cal.add('method',   'PUBLISH')
        cal.add('x-wr-calname', name if name is not None else self.calendar_name)
        cal.add('x-wr-timezone',  TIMEZONE)
        cal.add('x-wr-caldesc', self.calendar_description)
        cal.add('x-apple-calendar-color', '#E53935')
        return cal

    def generate_year(self, year: int) -> Calendar:
        """Tạo đối tượng Calendar cho một năm Dương lịch cụ thể."""
        cal = self._make_calendar(f'{self.calendar_name} {year}')
        start = date(year, 1, 1)
        end   = date(year, 12, 31)
        self._fill_calendar(cal, start, end)
        return cal

    def generate_range(self, start_year: int, end_year: int) -> Calendar:
        """Tạo đối tượng Calendar tổng hợp cho một khoảng thời gian nhiều năm."""
        cal = self._make_calendar(f'{self.calendar_name} {start_year}–{end_year}')
        start = date(start_year, 1, 1)
        end   = date(end_year, 12, 31)
        self._fill_calendar(cal, start, end)
        return cal

    def _fill_calendar(self, cal: Calendar, start: date, end: date) -> None:
        """Duyệt qua từng ngày trong khoảng thời gian và thêm sự kiện vào Calendar."""
        current = start
        while current <= end:
            try:
                lunar = to_lunar(current)
                if (
                    not self.minimal or lunar.lunar_day == 15
                    or (lunar.lunar_day == 1 and lunar.lunar_month_abs == 1 and not lunar.is_leap_month)
                ):
                    event = _build_event_for_day(current, lunar, self.language, self.minimal)
                    cal.add_component(event)
            except Exception as exc:
                if self.language == 'en' or self.minimal:
                    language_name = 'English' if self.language == 'en' else 'Vietnamese'
                    raise RuntimeError(f'Failed to generate {language_name} event for {current}') from exc
                print(f'[WARN] Lỗi khi xử lý ngày {current}: {exc}')
            current += timedelta(days=1)

    @staticmethod
    def save(cal: Calendar, filepath: str | Path) -> None:
        """Lưu đối tượng Calendar ra file định dạng .ics."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(cal.to_ical())
