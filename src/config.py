# ============================================================
# config.py — Cấu hình trung tâm cho VietLunarCalendar
# ============================================================

# Khoảng thời gian tạo lịch mặc định
DEFAULT_YEARS_AHEAD = 10  # Tạo lịch cuốn chiếu trước 10 năm từ năm hiện tại

# Múi giờ Việt Nam
TIMEZONE = 'Asia/Ho_Chi_Minh'  # UTC+7

# Thư mục output
OUTPUT_DIR = 'output'

# Thông tin metadata của Calendar
CALENDAR_NAME = 'Lịch Âm Việt Nam'
CALENDAR_DESCRIPTION = (
    'Lịch âm Việt Nam tối giản, tự động cập nhật qua URL. '
    'Bao gồm ngày âm lịch, Mùng 1, Rằm và các ngày lễ lớn. '
    'Múi giờ GMT+7 — Asia/Ho_Chi_Minh.'
)
PRODID = '-//VietLunarCalendar//Vietnamese Lunar Calendar//VI'
CALENDAR_VERSION = '2.0'
