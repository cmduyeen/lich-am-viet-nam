# ============================================================
# holidays.py — Danh mục ngày lễ lớn Việt Nam (Tối giản)
# ============================================================
from dataclasses import dataclass


@dataclass
class HolidayInfo:
    name: str             # Tên ngày lễ
    description: str = '' # Mô tả ngắn gọn
    is_public_holiday: bool = False  # Ngày nghỉ chính thức


# ──────────────────────────────────────────────────────────────
# 1. QUỐC LỄ DƯƠNG LỊCH (Nghỉ chính thức)
# ──────────────────────────────────────────────────────────────
FIXED_SOLAR_HOLIDAYS: dict[tuple[int, int], HolidayInfo] = {
    (1, 1):   HolidayInfo(name='Tết Dương Lịch', is_public_holiday=True, description='Nghỉ Tết Dương Lịch.'),
    (4, 30):  HolidayInfo(name='Giải Phóng Miền Nam', is_public_holiday=True, description='Ngày Giải phóng miền Nam, Thống nhất đất nước.'),
    (5, 1):   HolidayInfo(name='Quốc Tế Lao Động', is_public_holiday=True, description='Ngày Quốc tế Lao động.'),
    (9, 2):   HolidayInfo(name='Quốc Khánh', is_public_holiday=True, description='Quốc khánh nước CHXHCN Việt Nam.'),
}


# ──────────────────────────────────────────────────────────────
# 2. CÁC NGÀY LỄ ÂM LỊCH LỚN (Truyền thống văn hóa dân tộc)
# ──────────────────────────────────────────────────────────────
FIXED_LUNAR_HOLIDAYS: dict[tuple[int, int], HolidayInfo] = {
    # Tết Nguyên Đán
    (1, 1):   HolidayInfo(name='Mùng 1 Tết', is_public_holiday=True, description='Tết Nguyên Đán.'),
    (1, 2):   HolidayInfo(name='Mùng 2 Tết', is_public_holiday=True, description='Tết Nguyên Đán.'),
    (1, 3):   HolidayInfo(name='Mùng 3 Tết', is_public_holiday=True, description='Tết Nguyên Đán.'),
    (1, 10):  HolidayInfo(name='Vía Thần Tài', description='Ngày vía Thần Tài (Mùng 10 tháng Giêng).'),
    (1, 15):  HolidayInfo(name='Rằm Tháng Giêng (Tết Nguyên Tiêu)', description='Tết Nguyên Tiêu — Rằm đầu năm.'),

    # Giỗ Tổ Hùng Vương
    (3, 10):  HolidayInfo(name='Giỗ Tổ Hùng Vương', is_public_holiday=True, description='Ngày Giỗ Tổ Hùng Vương (10/3 âm lịch).'),

    # Lễ Phật Đản
    (4, 15):  HolidayInfo(name='Lễ Phật Đản', description='Đại lễ Phật Đản (15/4 âm lịch).'),

    # Tết Đoan Ngọ
    (5, 5):   HolidayInfo(name='Tết Đoan Ngọ', description='Tết Đoan Ngọ (5/5 âm lịch).'),

    # Lễ Vu Lan
    (7, 15):  HolidayInfo(name='Lễ Vu Lan', description='Lễ Vu Lan báo hiếu (Rằm tháng 7 âm lịch).'),

    # Tết Trung Thu
    (8, 15):  HolidayInfo(name='Tết Trung Thu', description='Tết Trung Thu (Rằm tháng 8 âm lịch).'),

    # Cúng Ông Táo
    (12, 23): HolidayInfo(name='Cúng Ông Táo', description='Lễ cúng tiễn Táo Quân về trời (23 tháng Chạp).'),
}

# Đêm Giao Thừa (ngày cuối cùng của năm âm lịch: 29 hoặc 30 tháng Chạp)
GIAO_THUA = HolidayInfo(
    name='Đêm Giao Thừa',
    description='Đêm Giao Thừa đón năm mới âm lịch.',
    is_public_holiday=True,
)
