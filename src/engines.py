"""All engines share immutable results; language never enters a cache key."""
from functools import lru_cache
from korean_lunar_calendar import KoreanLunarCalendar
from lunar_python import Solar
from .models import LunarDay
from .vietnamese_astronomy import vietnamese_date


@lru_cache(maxsize=16384)
def chinese(day):
    lunar = Solar.fromYmd(day.year, day.month, day.day).getLunar()
    return LunarDay(day, lunar.getYear(), abs(lunar.getMonth()), lunar.getDay(), lunar.getMonth() < 0, lunar.getJieQi())


@lru_cache(maxsize=16384)
def vietnamese(day):
    year, month, lunar_day = vietnamese_date(day)
    return LunarDay(day, year, abs(month), lunar_day, month < 0)


@lru_cache(maxsize=16384)
def korean(day):
    calendar = KoreanLunarCalendar()
    if not calendar.setSolarDate(day.year, day.month, day.day):
        raise ValueError('Korean conversion is available through 2050-12-31')
    return LunarDay(day, calendar.lunarYear, calendar.lunarMonth, calendar.lunarDay, calendar.isIntercalation)


ENGINES = {'vietnamese': vietnamese, 'chinese': chinese, 'korean': korean}
