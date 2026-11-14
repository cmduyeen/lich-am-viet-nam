# ============================================================
# holidays.py — Danh mục ngày lễ lớn Việt Nam (Tối giản)
# ============================================================
from dataclasses import dataclass


@dataclass
class HolidayInfo:
    name: str             # Tên ngày lễ
    description: str = '' # Mô tả ngắn gọn
    is_public_holiday: bool = False  # Ngày nghỉ chính thức
    category: str = 'lunar'
    name_en: str = ''
    description_en: str = ''


# ──────────────────────────────────────────────────────────────
# 1. QUỐC LỄ DƯƠNG LỊCH (Nghỉ chính thức)
# ──────────────────────────────────────────────────────────────
FIXED_SOLAR_HOLIDAYS: dict[tuple[int, int], HolidayInfo] = {
    (1, 1): HolidayInfo(
        name='Tết Dương Lịch', description='Nghỉ Tết Dương Lịch.', is_public_holiday=True,
        category='solar', name_en="New Year's Day",
        description_en='New Year holiday.',
    ),
    (4, 30): HolidayInfo(
        name='Giải Phóng Miền Nam',
        description='Ngày Giải phóng miền Nam, Thống nhất đất nước.',
        is_public_holiday=True, category='solar',
        name_en='Reunification Day',
        description_en='Commemorates the reunification of Vietnam.',
    ),
    (5, 1): HolidayInfo(
        name='Quốc Tế Lao Động', description='Ngày Quốc tế Lao động.',
        is_public_holiday=True, category='solar',
        name_en='International Labour Day',
        description_en='International Workers Day.',
    ),
    (9, 2): HolidayInfo(
        name='Quốc Khánh', description='Quốc khánh nước CHXHCN Việt Nam.',
        is_public_holiday=True, category='solar',
        name_en='Vietnam National Day',
        description_en='National Day of the Socialist Republic of Vietnam.',
    ),
}


# ──────────────────────────────────────────────────────────────
# 2. CÁC NGÀY LỄ ÂM LỊCH LỚN (Truyền thống văn hóa dân tộc)
# ──────────────────────────────────────────────────────────────
FIXED_LUNAR_HOLIDAYS: dict[tuple[int, int], HolidayInfo] = {
    # Tết Nguyên Đán
    (1, 1): HolidayInfo(
        name='Mùng 1 Tết', is_public_holiday=True, description='Tết Nguyên Đán.',
        name_en='Lunar New Year', description_en='The first day of Lunar New Year.',
    ),
    (1, 2): HolidayInfo(
        name='Mùng 2 Tết', is_public_holiday=True, description='Tết Nguyên Đán.',
        name_en='Lunar New Year Holiday', description_en='The second day of Lunar New Year.',
    ),
    (1, 3): HolidayInfo(
        name='Mùng 3 Tết', is_public_holiday=True, description='Tết Nguyên Đán.',
        name_en='Lunar New Year Holiday', description_en='The third day of Lunar New Year.',
    ),
    (1, 10): HolidayInfo(
        name='Vía Thần Tài', description='Ngày vía Thần Tài (Mùng 10 tháng Giêng).',
        name_en='God of Wealth Day',
        description_en='Traditional observance on the 10th day of the first lunar month.',
    ),
    (1, 15): HolidayInfo(
        name='Rằm Tháng Giêng (Tết Nguyên Tiêu)',
        description='Tết Nguyên Tiêu — Rằm đầu năm.',
        name_en='Lantern Festival (First Full Moon)',
        description_en='The first full moon observance of the lunar year.',
    ),

    # Giỗ Tổ Hùng Vương
    (3, 10): HolidayInfo(
        name='Giỗ Tổ Hùng Vương', is_public_holiday=True,
        description='Ngày Giỗ Tổ Hùng Vương (10/3 âm lịch).',
        name_en='Hung Kings Commemoration Day',
        description_en='Commemorates the Hung Kings on the 10th day of the third lunar month.',
    ),

    # Lễ Phật Đản
    (4, 15): HolidayInfo(
        name='Lễ Phật Đản', description='Đại lễ Phật Đản (15/4 âm lịch).',
        name_en='Buddha Day', description_en="Buddha's Birthday (15th day of the fourth lunar month).",
    ),

    # Tết Đoan Ngọ
    (5, 5): HolidayInfo(
        name='Tết Đoan Ngọ', description='Tết Đoan Ngọ (5/5 âm lịch).',
        name_en='Double Fifth Festival',
        description_en='Traditional observance on the fifth day of the fifth lunar month.',
    ),

    # Lễ Vu Lan
    (7, 15): HolidayInfo(
        name='Lễ Vu Lan', description='Lễ Vu Lan báo hiếu (Rằm tháng 7 âm lịch).',
        name_en='Vu Lan Festival',
        description_en='A day of filial gratitude on the 15th day of the seventh lunar month.',
    ),

    # Tết Trung Thu
    (8, 15): HolidayInfo(
        name='Tết Trung Thu', description='Tết Trung Thu (Rằm tháng 8 âm lịch).',
        name_en='Mid-Autumn Festival',
        description_en='Traditional festival on the 15th day of the eighth lunar month.',
    ),

    # Cúng Ông Táo
    (12, 23): HolidayInfo(
        name='Cúng Ông Táo',
        description='Lễ cúng tiễn Táo Quân về trời (23 tháng Chạp).',
        name_en='Kitchen Gods Day',
        description_en='The Kitchen Gods are traditionally sent to heaven on this day.',
    ),
}

# Đêm Giao Thừa (ngày cuối cùng của năm âm lịch: 29 hoặc 30 tháng Chạp)
GIAO_THUA = HolidayInfo(
    name='Đêm Giao Thừa',
    description='Đêm Giao Thừa đón năm mới âm lịch.',
    is_public_holiday=True,
    name_en="Lunar New Year's Eve",
    description_en='The final day of the lunar year.',
)
