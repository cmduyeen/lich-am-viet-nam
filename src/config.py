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

CALENDAR_NAME_EN = 'Vietnamese Lunar Calendar'
CALENDAR_DESCRIPTION_EN = (
    'A minimalist Vietnamese lunar calendar with automatic subscription updates. '
    'Includes lunar dates, first days of lunar months, full moons and major holidays. '
    'Time zone GMT+7 - Asia/Ho_Chi_Minh.'
)
PRODID_EN = '-//VietLunarCalendar//Vietnamese Lunar Calendar//EN'

MINIMAL_CALENDAR_NAME_EN = 'Vietnamese Lunar Calendar - Minimal'
MINIMAL_CALENDAR_NAME = 'Lịch Âm Việt Nam - Tối Giản'
MINIMAL_CALENDAR_DESCRIPTION = (
    'Chỉ gồm Rằm (ngày 15 âm lịch, kể cả tháng nhuận) và Mùng 1 Tết Nguyên Đán '
    '(tháng Giêng không nhuận). Không phải thời điểm trăng tròn thiên văn chính xác. '
    'Múi giờ GMT+7 - Asia/Ho_Chi_Minh.'
)
FULL_MOON_NOTE = 'Ngày 15 âm lịch theo truyền thống, không phải thời điểm trăng tròn thiên văn chính xác.'
LUNAR_NEW_YEAR_NOTE = 'Ngày đầu năm âm lịch (mùng 1 tháng Giêng không nhuận).'

MINIMAL_CALENDAR_DESCRIPTION_EN = (
    "Full Moon (traditional lunar day 15, including leap months) and Lunar New Year's Day only. "
    'Not exact astronomical full moon times. Time zone GMT+7 - Asia/Ho_Chi_Minh.'
)
FULL_MOON_NOTE_EN = 'Traditional lunar day 15, not an exact astronomical full moon time.'
LUNAR_NEW_YEAR_NOTE_EN = 'First day of the lunar year (non-leap month 1).'

HEAVENLY_STEMS_EN = {
    'Giáp': 'Yang Wood', 'Ất': 'Yin Wood',
    'Bính': 'Yang Fire', 'Đinh': 'Yin Fire',
    'Mậu': 'Yang Earth', 'Kỷ': 'Yin Earth',
    'Canh': 'Yang Metal', 'Tân': 'Yin Metal',
    'Nhâm': 'Yang Water', 'Quý': 'Yin Water',
}
EARTHLY_BRANCHES_EN = {
    'Tý': 'Rat', 'Sửu': 'Buffalo', 'Dần': 'Tiger', 'Mão': 'Cat',
    'Thìn': 'Dragon', 'Tỵ': 'Snake', 'Ngọ': 'Horse', 'Mùi': 'Goat',
    'Thân': 'Monkey', 'Dậu': 'Rooster', 'Tuất': 'Dog', 'Hợi': 'Pig',
}
