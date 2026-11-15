# ============================================================
# holidays.py — Danh mục ngày lễ lớn Việt Nam (Tối giản)
# ============================================================
from dataclasses import dataclass


@dataclass
class HolidayInfo:
    name: str             # Tên ngày lễ
    description: str = '' # Mô tả ngắn gọn
    is_public_holiday: bool = False  # Dịp lễ chính thức; không phải lịch nghỉ bù
    start_year: int = 1


# ──────────────────────────────────────────────────────────────
# 1. QUỐC LỄ DƯƠNG LỊCH (Nghỉ chính thức)
# ──────────────────────────────────────────────────────────────
FIXED_SOLAR_HOLIDAYS: dict[tuple[int, int], HolidayInfo] = {
    (1, 1):   HolidayInfo(name='Tết Dương Lịch', is_public_holiday=True, description='Nghỉ Tết Dương Lịch.'),
    (4, 30):  HolidayInfo(name='Giải Phóng Miền Nam', is_public_holiday=True, description='Ngày Giải phóng miền Nam, Thống nhất đất nước.'),
    (5, 1):   HolidayInfo(name='Quốc Tế Lao Động', is_public_holiday=True, description='Ngày Quốc tế Lao động.'),
    (9, 2):   HolidayInfo(name='Quốc Khánh', is_public_holiday=True, description='Quốc khánh nước CHXHCN Việt Nam.'),
    (2, 14):  HolidayInfo(name='Lễ Tình nhân', description='Ngày lễ tình nhân 14/2.'),
    (3, 8):   HolidayInfo(name='Quốc tế Phụ nữ', description='Ngày Quốc tế Phụ nữ 8/3.'),
    (6, 1):   HolidayInfo(name='Quốc tế Thiếu nhi', description='Ngày Quốc tế Thiếu nhi 1/6.'),
    (6, 28):  HolidayInfo(name='Gia đình Việt Nam', description='Ngày Gia đình Việt Nam 28/6.'),
    (10, 20): HolidayInfo(name='Phụ nữ Việt Nam', description='Ngày Phụ nữ Việt Nam 20/10.'),
    (11, 20): HolidayInfo(name='Nhà giáo Việt Nam', description='Ngày Nhà giáo Việt Nam 20/11.'),
    (11, 24): HolidayInfo(name='Văn hóa Việt Nam', is_public_holiday=True, start_year=2026,
                          description='Ngày Văn hóa Việt Nam 24/11, áp dụng từ năm 2026 theo Nghị quyết 28/2026/QH16.'),
    (12, 24): HolidayInfo(name='Đêm Giáng sinh', description='Đêm Giáng sinh 24/12.'),
    (12, 25): HolidayInfo(name='Giáng sinh', description='Lễ Giáng sinh 25/12.'),
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
    (1, 15):  HolidayInfo(name='Tết Nguyên Tiêu', description='Tết Nguyên Tiêu — Rằm đầu năm.'),

    (3, 3):   HolidayInfo(name='Tết Hàn thực', description='Tết Hàn thực, mùng 3 tháng 3 âm lịch.'),
    (10, 15): HolidayInfo(name='Tết Hạ nguyên', description='Tết Hạ nguyên, rằm tháng 10 âm lịch.'),

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
    is_public_holiday=False,
)
