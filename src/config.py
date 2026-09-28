# ============================================================
# config.py — Cấu hình trung tâm cho VietLunarCalendar
# ============================================================

# Khoảng thời gian tạo lịch mặc định
DEFAULT_YEARS_AHEAD = 10  # Tạo lịch cuốn chiếu trước 10 năm từ năm hiện tại
START_YEAR = 2026
END_YEAR   = 2060

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
