# ============================================================
# lunar_converter.py — Chuyển đổi Dương lịch sang Âm lịch Việt Nam
#   Sử dụng thư viện lunar-python (thuật toán Jean Meeus, GMT+7)
# ============================================================
from __future__ import annotations
from datetime import date, timedelta
from dataclasses import dataclass
from typing import Optional

from lunar_python import Solar


# ──────────────────────────────────────────────────────────────
# Bảng tra cứu tiếng Việt
# ──────────────────────────────────────────────────────────────

# Thiên Can (Heavenly Stems)
THIEN_CAN: dict[str, str] = {
    '甲': 'Giáp', '乙': 'Ất',  '丙': 'Bính', '丁': 'Đinh',
    '戊': 'Mậu',  '己': 'Kỷ',  '庚': 'Canh', '辛': 'Tân',
    '壬': 'Nhâm', '癸': 'Quý',
}

# Địa Chi (Earthly Branches)
DIA_CHI: dict[str, str] = {
    '子': 'Tý',  '丑': 'Sửu', '寅': 'Dần', '卯': 'Mão',
    '辰': 'Thìn','巳': 'Tỵ',  '午': 'Ngọ', '未': 'Mùi',
    '申': 'Thân','酉': 'Dậu', '戌': 'Tuất','亥': 'Hợi',
}

# Con giáp (Zodiac animals)
CON_GIAP: dict[str, str] = {
    '鼠': 'Chuột (Tý)',   '牛': 'Trâu (Sửu)',  '虎': 'Hổ (Dần)',
    '兔': 'Mèo (Mão)',    '龙': 'Rồng (Thìn)', '蛇': 'Rắn (Tỵ)',
    '马': 'Ngựa (Ngọ)',   '羊': 'Dê (Mùi)',    '猴': 'Khỉ (Thân)',
    '鸡': 'Gà (Dậu)',     '狗': 'Chó (Tuất)',  '猪': 'Heo (Hợi)',
}

# Tiết Khí (24 Solar Terms)
TIET_KHI: dict[str, str] = {
    '冬至': 'Đông Chí',    '小寒': 'Tiểu Hàn',   '大寒': 'Đại Hàn',
    '立春': 'Lập Xuân',    '雨水': 'Vũ Thủy',    '惊蛰': 'Kinh Trập',
    '春分': 'Xuân Phân',   '清明': 'Thanh Minh',  '谷雨': 'Cốc Vũ',
    '立夏': 'Lập Hạ',      '小满': 'Tiểu Mãn',   '芒种': 'Mang Chủng',
    '夏至': 'Hạ Chí',      '小暑': 'Tiểu Thử',   '大暑': 'Đại Thử',
    '立秋': 'Lập Thu',     '处暑': 'Xử Thử',     '白露': 'Bạch Lộ',
    '秋分': 'Thu Phân',    '寒露': 'Hàn Lộ',     '霜降': 'Sương Giáng',
    '立冬': 'Lập Đông',    '小雪': 'Tiểu Tuyết', '大雪': 'Đại Tuyết',
}

# Tên tháng âm lịch tiếng Việt
LUNAR_MONTH_NAMES: dict[int, str] = {
    1: 'Tháng Giêng', 2: 'Tháng Hai',   3: 'Tháng Ba',
    4: 'Tháng Tư',    5: 'Tháng Năm',   6: 'Tháng Sáu',
    7: 'Tháng Bảy',   8: 'Tháng Tám',   9: 'Tháng Chín',
    10: 'Tháng Mười', 11: 'Tháng Mười Một', 12: 'Tháng Chạp',
}

# Ngày âm lịch (Mùng X / Ngày X)
def lunar_day_name(day: int) -> str:
    """Trả về tên ngày âm lịch (ví dụ: Mùng 1, Ngày 15)."""
    if day == 1:
        return 'Mùng 1'
    elif day <= 10:
        return f'Mùng {day}'
    else:
        return f'Ngày {day}'


# ──────────────────────────────────────────────────────────────
# Dataclass kết quả chuyển đổi
# ──────────────────────────────────────────────────────────────

@dataclass
class LunarDate:
    """Đối tượng chứa thông tin chi tiết về ngày âm lịch."""
    # Ngày dương lịch gốc
    solar_date: date

    # Thông tin âm lịch
    lunar_year: int
    lunar_month: int        # Tháng âm, tháng nhuận mang giá trị âm trong lunar_python
    lunar_day: int
    is_leap_month: bool

    # Can Chi (đã chuyển ngữ sang Tiếng Việt)
    can_chi_year: str       # ví dụ: "Bính Ngọ"
    can_chi_month: str      # ví dụ: "Giáp Dần"
    can_chi_day: str        # ví dụ: "Canh Tý"

    # Con giáp của năm
    zodiac_year: str        # ví dụ: "Ngựa (Ngọ)"

    # Tiết Khí (nếu có)
    solar_term: Optional[str]  # ví dụ: "Lập Xuân" hoặc None

    # ── Các thuộc tính tính toán ───────────────────────────

    @property
    def lunar_month_abs(self) -> int:
        """Tháng âm dương tính (bỏ dấu âm của tháng nhuận)."""
        return abs(self.lunar_month)

    @property
    def month_name_vn(self) -> str:
        """Tên tháng âm lịch tiếng Việt."""
        name = LUNAR_MONTH_NAMES.get(self.lunar_month_abs, f'Tháng {self.lunar_month_abs}')
        if self.is_leap_month:
            name = f'{name} Nhuận'
        return name

    @property
    def day_name_vn(self) -> str:
        """Tên ngày âm lịch tiếng Việt."""
        return lunar_day_name(self.lunar_day)

    @property
    def full_date_vn(self) -> str:
        """Chuỗi ngày tháng âm lịch đầy đủ tiếng Việt."""
        return f'{self.day_name_vn} {self.month_name_vn} Năm {self.can_chi_year}'

    def build_description_footer(self) -> str:
        """Tạo phần thông tin chi tiết âm lịch cho phần mô tả sự kiện."""
        lines = [
            '─' * 40,
            f'📅 ÂM LỊCH: {self.full_date_vn}',
            f'🔢 Ngày: {self.lunar_day}/{self.lunar_month_abs}/{self.lunar_year}',
            f'✨ Can Chi Ngày: {self.can_chi_day}',
            f'🌙 Can Chi Tháng: {self.can_chi_month}',
            f'🐉 Can Chi Năm: {self.can_chi_year} — Năm {self.zodiac_year}',
        ]
        if self.solar_term:
            lines.append(f'☀️ Tiết Khí: {self.solar_term}')
        if self.is_leap_month:
            lines.append(f'📌 Ghi chú: Tháng Nhuận {self.lunar_month_abs}')
        lines.append('─' * 40)
        return '\n'.join(lines)


# ──────────────────────────────────────────────────────────────
# Helper: chuyển chuỗi Ganzhi Hán → tiếng Việt
# ──────────────────────────────────────────────────────────────

def _ganzhi_to_viet(gz: str) -> str:
    """Chuyển Can Chi dạng 2 ký tự Hán sang tiếng Việt."""
    if not gz or len(gz) < 2:
        return gz
    can = THIEN_CAN.get(gz[0], gz[0])
    chi = DIA_CHI.get(gz[1], gz[1])
    return f'{can} {chi}'


def _zodiac_to_viet(zh: str) -> str:
    """Chuyển tên con giáp Hán sang tiếng Việt."""
    return CON_GIAP.get(zh, zh)


def _tietKhi_to_viet(tk: str) -> Optional[str]:
    """Chuyển tên Tiết Khí Hán sang tiếng Việt, trả về None nếu không có."""
    if not tk:
        return None
    return TIET_KHI.get(tk, tk) if tk else None


# ──────────────────────────────────────────────────────────────
# Hàm chuyển đổi chính
# ──────────────────────────────────────────────────────────────

def to_lunar(d: date) -> LunarDate:
    """
    Chuyển đổi một ngày dương lịch sang âm lịch Việt Nam (GMT+7).

    Args:
        d: Ngày dương lịch cần chuyển đổi.

    Returns:
        LunarDate: Đối tượng chứa đầy đủ thông tin âm lịch.
    """
    solar = Solar.fromYmd(d.year, d.month, d.day)
    lunar = solar.getLunar()

    raw_month = lunar.getMonth()   # Tháng nhuận trả về số âm (e.g. -4 = nhuận tháng 4)
    is_leap   = raw_month < 0      # Tháng nhuận khi month < 0

    gz_year  = lunar.getYearInGanZhi()
    gz_month = lunar.getMonthInGanZhi()
    gz_day   = lunar.getDayInGanZhi()

    # Con giáp — getYearShengXiao() trả về con giáp âm lịch (đúng) e.g. '马'=Ngựa (Ngọ)
    try:
        zodiac_raw = lunar.getYearShengXiao()
        zodiac_vn  = _zodiac_to_viet(zodiac_raw)
    except Exception:
        zodiac_vn = '?'

    # Tiết Khí — getJieQi() trả về string rỗng nếu không phải tiết khí
    try:
        tietKhi_raw = lunar.getJieQi()
        tietKhi_vn  = _tietKhi_to_viet(tietKhi_raw) if tietKhi_raw else None
    except Exception:
        tietKhi_vn = None

    return LunarDate(
        solar_date    = d,
        lunar_year    = lunar.getYear(),
        lunar_month   = raw_month,
        lunar_day     = lunar.getDay(),
        is_leap_month = is_leap,
        can_chi_year  = _ganzhi_to_viet(gz_year),
        can_chi_month = _ganzhi_to_viet(gz_month),
        can_chi_day   = _ganzhi_to_viet(gz_day),
        zodiac_year   = zodiac_vn,
        solar_term    = tietKhi_vn,
    )


def is_last_day_of_lunar_month(d: date) -> bool:
    """Kiểm tra xem ngày d có phải ngày cuối tháng âm lịch không."""
    tomorrow = d + timedelta(days=1)
    tomorrow_lunar = to_lunar(tomorrow)
    return tomorrow_lunar.lunar_day == 1
