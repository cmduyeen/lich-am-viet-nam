# ============================================================
# holidays.py — Danh mục ngày lễ lớn Việt Nam (Tối giản)
# ============================================================
from dataclasses import dataclass


@dataclass
class HolidayInfo:
    name: str             # Tên ngày lễ
    description: str = '' # Mô tả ngắn gọn
    is_public_holiday: bool = False  # Ngày nghỉ chính thức
    name_en: str = ''
    description_en: str = ''


# ──────────────────────────────────────────────────────────────
# 1. QUỐC LỄ DƯƠNG LỊCH (Nghỉ chính thức)
# ──────────────────────────────────────────────────────────────
FIXED_SOLAR_HOLIDAYS: dict[tuple[int, int], HolidayInfo] = {
    (1, 1):   HolidayInfo(name='Tết Dương Lịch', is_public_holiday=True, description='Nghỉ Tết Dương Lịch.',
                         name_en="New Year's Day", description_en='Gregorian New Year holiday.'),
    (4, 30):  HolidayInfo(name='Giải Phóng Miền Nam', is_public_holiday=True, description='Ngày Giải phóng miền Nam, Thống nhất đất nước.',
                         name_en='Reunification Day', description_en='Liberation of Southern Vietnam and national reunification.'),
    (5, 1):   HolidayInfo(name='Quốc Tế Lao Động', is_public_holiday=True, description='Ngày Quốc tế Lao động.',
                         name_en='International Labour Day', description_en='International Labour Day.'),
    (9, 2):   HolidayInfo(name='Quốc Khánh', is_public_holiday=True, description='Quốc khánh nước CHXHCN Việt Nam.',
                         name_en='National Day', description_en='National Day of the Socialist Republic of Vietnam.'),
}


# ──────────────────────────────────────────────────────────────
# 2. CÁC NGÀY LỄ ÂM LỊCH LỚN (Truyền thống văn hóa dân tộc)
# ──────────────────────────────────────────────────────────────
FIXED_LUNAR_HOLIDAYS: dict[tuple[int, int], HolidayInfo] = {
    # Tết Nguyên Đán
    (1, 1):   HolidayInfo(name='Mùng 1 Tết', is_public_holiday=True, description='Tết Nguyên Đán.',
                         name_en='Lunar New Year - Day 1', description_en='Vietnamese Lunar New Year.'),
    (1, 2):   HolidayInfo(name='Mùng 2 Tết', is_public_holiday=True, description='Tết Nguyên Đán.',
                         name_en='Lunar New Year - Day 2', description_en='Vietnamese Lunar New Year.'),
    (1, 3):   HolidayInfo(name='Mùng 3 Tết', is_public_holiday=True, description='Tết Nguyên Đán.',
                         name_en='Lunar New Year - Day 3', description_en='Vietnamese Lunar New Year.'),
    (1, 10):  HolidayInfo(name='Vía Thần Tài', description='Ngày vía Thần Tài (Mùng 10 tháng Giêng).',
                         name_en='God of Wealth Day', description_en='God of Wealth Day (day 10 of the first lunar month).'),
    (1, 15):  HolidayInfo(name='Rằm Tháng Giêng (Tết Nguyên Tiêu)', description='Tết Nguyên Tiêu — Rằm đầu năm.',
                         name_en='First Full Moon Festival', description_en='The first full moon festival of the lunar year (day 15 of the first lunar month).'),

    # Giỗ Tổ Hùng Vương
    (3, 10):  HolidayInfo(name='Giỗ Tổ Hùng Vương', is_public_holiday=True, description='Ngày Giỗ Tổ Hùng Vương (10/3 âm lịch).',
                         name_en='Hung Kings Commemoration Day', description_en='Commemoration of the Hung Kings (day 10 of lunar month 3).'),

    # Lễ Phật Đản
    (4, 15):  HolidayInfo(name='Lễ Phật Đản', description='Đại lễ Phật Đản (15/4 âm lịch).',
                         name_en="Buddha's Birthday", description_en="Celebration of the Buddha's birth (day 15 of lunar month 4)."),

    # Tết Đoan Ngọ
    (5, 5):   HolidayInfo(name='Tết Đoan Ngọ', description='Tết Đoan Ngọ (5/5 âm lịch).',
                         name_en='Double Fifth Festival', description_en='Traditional midyear festival (day 5 of lunar month 5).'),

    # Lễ Vu Lan
    (7, 15):  HolidayInfo(name='Lễ Vu Lan', description='Lễ Vu Lan báo hiếu (Rằm tháng 7 âm lịch).',
                         name_en='Filial Piety Festival', description_en='Festival honouring parents and ancestors (day 15 of lunar month 7).'),

    # Tết Trung Thu
    (8, 15):  HolidayInfo(name='Tết Trung Thu', description='Tết Trung Thu (Rằm tháng 8 âm lịch).',
                         name_en='Mid-Autumn Festival', description_en='Mid-Autumn Festival (day 15 of lunar month 8).'),

    # Cúng Ông Táo
    (12, 23): HolidayInfo(name='Cúng Ông Táo', description='Lễ cúng tiễn Táo Quân về trời (23 tháng Chạp).',
                         name_en='Kitchen Gods Day', description_en='Ceremony sending the Kitchen Gods to heaven (day 23 of lunar month 12).'),
}

# Đêm Giao Thừa (ngày cuối cùng của năm âm lịch: 29 hoặc 30 tháng Chạp)
GIAO_THUA = HolidayInfo(
    name='Đêm Giao Thừa',
    description='Đêm Giao Thừa đón năm mới âm lịch.',
    is_public_holiday=True,
    name_en="Lunar New Year's Eve",
    description_en='The eve of the Vietnamese Lunar New Year.',
)
