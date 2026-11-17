# ============================================================
# config.py — Cấu hình trung tâm cho VietLunarCalendar
# ============================================================

# Khoảng thời gian tạo lịch mặc định
DEFAULT_YEARS_AHEAD = 1  # Năm hiện tại và năm kế tiếp; phạm vi tùy chọn vẫn được hỗ trợ

# Múi giờ Việt Nam
TIMEZONE = 'Asia/Ho_Chi_Minh'  # UTC+7

# Thư mục output
OUTPUT_DIR = 'output'

# Thông tin metadata của Calendar
CALENDAR_NAME = 'Lịch Âm Việt Nam'
CALENDAR_DESCRIPTION = (
    'Lịch âm Việt Nam tối giản, tự động đồng bộ trọn đời. '
    'Bao gồm ngày âm lịch, Mùng 1, Rằm và các ngày lễ lớn. '
    'Múi giờ GMT+7 — Asia/Ho_Chi_Minh.'
)
PRODID = '-//VietLunarCalendar//Vietnamese Lunar Calendar//VI'
CALENDAR_VERSION = '2.0'

# Existing subscriptions remain hosted in the original GitHub repository.
PUBLIC_FEED_BASE_URL = 'https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/'


def resolve_year_range(current_year, start_year=None, end_year=None, last_year=9998):
    """One default horizon for CLI, batch builds and custom configurations."""
    start = current_year if start_year is None else start_year
    end = min(start + DEFAULT_YEARS_AHEAD, last_year) if end_year is None else end_year
    if not 1 <= start <= end <= 9998:
        raise ValueError('years must satisfy 1 <= start <= end <= 9998')
    return start, end


# Compatibility exports for older callers; reflect the current rolling window.
from datetime import datetime
from zoneinfo import ZoneInfo
START_YEAR = datetime.now(ZoneInfo(TIMEZONE)).year
END_YEAR = START_YEAR + DEFAULT_YEARS_AHEAD
