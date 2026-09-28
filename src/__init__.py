# src — Gói mã nguồn cốt lõi VietLunarCalendar
"""
Gói module hỗ trợ chuyển đổi lịch âm, dữ liệu ngày lễ và tạo file iCalendar (.ics).
"""
from .config import START_YEAR, END_YEAR, OUTPUT_DIR, DEFAULT_YEARS_AHEAD
from .lunar_converter import to_lunar, LunarDate
from .holidays import HolidayInfo
from .ics_generator import LunarCalendarGenerator

__all__ = [
    'START_YEAR',
    'END_YEAR',
    'OUTPUT_DIR',
    'DEFAULT_YEARS_AHEAD',
    'to_lunar',
    'LunarDate',
    'HolidayInfo',
    'LunarCalendarGenerator',
]
