# ============================================================
# ics_generator.py — Tạo file iCalendar (.ics) Lịch Âm Việt Nam
# ============================================================
from __future__ import annotations
from .colors import add_event_color

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from icalendar import Calendar, Event

try:
    from .config import (
        CALENDAR_NAME, CALENDAR_DESCRIPTION,
        PRODID, CALENDAR_VERSION, TIMEZONE,
    )
    from .holidays import (
        FIXED_SOLAR_HOLIDAYS, FIXED_LUNAR_HOLIDAYS,
        GIAO_THUA, HolidayInfo,
    )
    from .lunar_converter import to_lunar, is_last_day_of_lunar_month, LunarDate
    from .user_config import CalendarOptions
except ImportError:
    from config import (
        CALENDAR_NAME, CALENDAR_DESCRIPTION,
        PRODID, CALENDAR_VERSION, TIMEZONE,
    )
    from holidays import (
        FIXED_SOLAR_HOLIDAYS, FIXED_LUNAR_HOLIDAYS,
        GIAO_THUA, HolidayInfo,
    )
    from lunar_converter import to_lunar, is_last_day_of_lunar_month, LunarDate
    from user_config import CalendarOptions


_ZODIAC_EN = {
    'Chuột': 'Rat', 'Trâu': 'Buffalo', 'Hổ': 'Tiger', 'Mèo': 'Cat',
    'Rồng': 'Dragon', 'Rắn': 'Snake', 'Ngựa': 'Horse', 'Dê': 'Goat',
    'Khỉ': 'Monkey', 'Gà': 'Rooster', 'Chó': 'Dog', 'Heo': 'Pig',
}
_STEM_ELEMENT_EN = {
    'Giáp': 'Wood', 'Ất': 'Wood', 'Bính': 'Fire', 'Đinh': 'Fire',
    'Mậu': 'Earth', 'Kỷ': 'Earth', 'Canh': 'Metal', 'Tân': 'Metal',
    'Nhâm': 'Water', 'Quý': 'Water',
}


def _holidays_for_day(d: date, lunar: LunarDate) -> list[HolidayInfo]:
    holidays: list[HolidayInfo] = []
    if not lunar.is_leap_month:
        if lunar.lunar_month_abs == 12 and is_last_day_of_lunar_month(d):
            holidays.append(GIAO_THUA)
        lunar_holiday = FIXED_LUNAR_HOLIDAYS.get(
            (lunar.lunar_month_abs, lunar.lunar_day)
        )
        if lunar_holiday:
            holidays.append(lunar_holiday)

    solar_holiday = FIXED_SOLAR_HOLIDAYS.get((d.month, d.day))
    if solar_holiday:
        holidays.append(solar_holiday)
    return holidays


def _holiday_name(holiday: HolidayInfo, language: str) -> str:
    if language == 'en':
        return holiday.name_en or holiday.name
    return holiday.name


def _holiday_description(holiday: HolidayInfo, language: str) -> str:
    if language == 'en':
        return holiday.description_en or holiday.description
    return holiday.description


def _build_event_for_day(
    d: date,
    lunar: LunarDate,
    dtstamp: datetime,
    options: CalendarOptions,
) -> Event | None:
    """Create an all-day event when it matches the user's selected content."""
    day = lunar.lunar_day
    m = lunar.lunar_month_abs
    if options.minimal and not (day == 15 or (day == 1 and m == 1 and not lunar.is_leap_month)):
        return None
    holidays = [
        holiday for holiday in _holidays_for_day(d, lunar)
        if holiday.category in options.holiday_types
    ]

    if not options.minimal and options.lunar_days is not None and day not in options.lunar_days and not holidays:
        return None

    if options.language == 'en':
        month_name = f"Month {m}" + (" (leap)" if lunar.is_leap_month else "")
        summary = f"Lunar day {day}, {month_name}"
        if holidays:
            names = ' / '.join(_holiday_name(h, 'en') for h in holidays)
            summary += f' • {names}'
        elif day == 1:
            summary += ' • New Moon'
        elif day == 15:
            summary += ' • Full Moon'
        desc_lines = [
            f"Lunar date: {day}/{m}/{lunar.lunar_year}"
            + (" (leap month)" if lunar.is_leap_month else ""),
        ]
        zodiac = lunar.zodiac_year.split(' (', maxsplit=1)[0]
        animal = _ZODIAC_EN.get(zodiac, zodiac)
        stem = lunar.can_chi_year.split(maxsplit=1)[0]
        element = _STEM_ELEMENT_EN.get(stem)
        year_name = f"{element} {animal}" if element else animal
        desc_lines.append(f"Year of the {year_name}")
        desc_lines.extend(
            f"{_holiday_name(h, 'en')}: {_holiday_description(h, 'en')}"
            for h in holidays
        )
    else:
        if holidays:
            summary = f"{day}/{m} • {' / '.join(_holiday_name(h, 'vi') for h in holidays)}"
        elif day == 1:
            summary = f'{day}/{m} • Mùng 1'
        elif day == 15:
            summary = f'{day}/{m} • Rằm'
        else:
            summary = f'{day}/{m}'
        desc_lines = [f'Ngày {day} tháng {m} âm lịch ({lunar.can_chi_year})']
        desc_lines.extend(
            f'{_holiday_name(h, "vi")}: {_holiday_description(h, "vi")}'
            for h in holidays
        )
    if options.minimal:
        holidays = []
        if options.language == 'en':
            summary = 'Full Moon' if day == 15 else 'Lunar New Year'
            desc_lines = desc_lines[:2]
            desc_lines.append(
                'Traditional full-moon observance on lunar day 15, not the exact astronomical full moon.'
                if day == 15 else 'The first day of the first non-leap lunar month.'
            )
        else:
            summary = 'Rằm' if day == 15 else 'Tết Nguyên Đán'
            month_label = f'{m} nhuận' if lunar.is_leap_month else str(m)
            desc_lines = [f'Ngày {day} tháng {month_label} âm lịch ({lunar.can_chi_year})']
            desc_lines.append(
                'Ngày Rằm truyền thống (15 âm lịch), không phải thời điểm trăng tròn thiên văn.'
                if day == 15 else 'Mùng 1 tháng Giêng không nhuận, ngày đầu năm âm lịch.'
            )
    description = '\n'.join(desc_lines)

    event = Event()
    uid_language = '-en' if options.language == 'en' else ''
    uid_mode = '-minimal' if options.minimal else ''
    event.add('uid', f"vnlunar{uid_language}{uid_mode}-{d.strftime('%Y%m%d')}@cmduyeen")
    event.add('summary', summary)
    event.add('description', description)
    event.add('dtstart', d)
    event.add('dtend', d + timedelta(days=1))

    if (options.minimal and day == 1) or any(holiday.is_public_holiday for holiday in holidays):
        event.add('x-microsoft-cdo-importance', '2')

    if holidays and options.holiday_color is not None:
        add_event_color(event, options.holiday_color)
    elif (options.minimal and day == 1) or any(holiday.is_public_holiday for holiday in holidays):
        add_event_color(event, '#E53935')
    elif day in (1, 15):
        add_event_color(event, options.lunar_day_color)
    else:
        add_event_color(event, options.ordinary_color)

    event.add('dtstamp', dtstamp)

    return event


class LunarCalendarGenerator:
    """Tạo file .ics lịch âm Việt Nam theo khoảng năm cho trước."""

    def _make_calendar(self, name: str, options: CalendarOptions) -> Calendar:
        """Khởi tạo Calendar object với metadata chuẩn."""
        cal = Calendar()
        prodid = PRODID
        if options.language == 'en':
            prodid = '-//VietLunarCalendar//Vietnamese Lunar Calendar//EN'
        if options.minimal:
            name = name.replace('Vietnamese Lunar Calendar', 'Vietnamese Lunar Calendar (Minimal)').replace('Lịch Âm Việt Nam', 'Lịch Âm Việt Nam (Tối giản)')
        cal.add('prodid', prodid)
        cal.add('version', CALENDAR_VERSION)
        cal.add('calscale', 'GREGORIAN')
        cal.add('method',   'PUBLISH')
        cal.add('x-wr-calname',   name)
        cal.add('x-wr-timezone',  TIMEZONE)
        description = CALENDAR_DESCRIPTION
        if options.language == 'en':
            description = (
                'Vietnamese lunar calendar with lunar dates and major Vietnamese holidays. '
                'Time zone: Asia/Ho_Chi_Minh (UTC+7).'
            )
        if options.minimal:
            description = (
                'Traditional lunar day 15 and Lunar New Year only. Full Moon is not an astronomical instant. UTC+7.'
                if options.language == 'en' else
                'Chỉ ngày Rằm (15 âm lịch) và mùng 1 Tết. Rằm không phải thời điểm trăng tròn thiên văn. GMT+7.'
            )
        cal.add('x-wr-caldesc', description)
        cal.add('x-apple-calendar-color', options.calendar_color)
        return cal

    def generate_year(
        self, year: int, options: CalendarOptions | None = None
    ) -> Calendar:
        """Tạo đối tượng Calendar cho một năm Dương lịch cụ thể."""
        options = options or CalendarOptions()
        name = (
            f'Vietnamese Lunar Calendar {year}'
            if options.language == 'en'
            else f'{CALENDAR_NAME} {year}'
        )
        cal = self._make_calendar(name, options)
        start = date(year, 1, 1)
        end   = date(year, 12, 31)
        self._fill_calendar(cal, start, end, options)
        return cal

    def generate_range(
        self,
        start_year: int,
        end_year: int,
        options: CalendarOptions | None = None,
    ) -> Calendar:
        """Tạo đối tượng Calendar tổng hợp cho một khoảng thời gian nhiều năm."""
        options = options or CalendarOptions()
        if options.language == 'en':
            name = f'Vietnamese Lunar Calendar {start_year}-{end_year}'
        else:
            name = f'Lịch Âm Việt Nam {start_year}–{end_year}'
        cal = self._make_calendar(name, options)
        start = date(start_year, 1, 1)
        end   = date(end_year, 12, 31)
        self._fill_calendar(cal, start, end, options)
        return cal

    def _fill_calendar(
        self, cal: Calendar, start: date, end: date, options: CalendarOptions
    ) -> None:
        """Duyệt qua từng ngày trong khoảng thời gian và thêm sự kiện vào Calendar."""
        current = start
        dtstamp = datetime.now(timezone.utc)
        while current <= end:
            lunar = to_lunar(current)
            event = _build_event_for_day(current, lunar, dtstamp, options)
            if event is not None:
                cal.add_component(event)
            current += timedelta(days=1)

    @staticmethod
    def split_year(calendar: Calendar, year: int) -> Calendar:
        """Reuse generated events, preserving timestamps and avoiding recalculation."""
        result = Calendar()
        for key, value in calendar.items():
            result[key] = value
        name = str(calendar.get('x-wr-calname', 'Calendar'))
        import re
        result['x-wr-calname'] = re.sub(r'\d{4}[–-]\d{4}$', str(year), name)
        for event in calendar.walk('VEVENT'):
            if event.decoded('dtstart').year == year:
                result.add_component(event)
        return result

    @staticmethod
    def save(cal: Calendar, filepath: str | Path) -> None:
        """Lưu đối tượng Calendar ra file định dạng .ics."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(cal.to_ical())
