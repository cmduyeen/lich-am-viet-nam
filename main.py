# main.py — Điểm bắt đầu (Entry point) tạo Lịch Âm Việt Nam
# ============================================================
"""
Công cụ tạo file iCalendar (.ics) cho lịch âm Việt Nam.
Tự động tính toán cuốn chiếu 10 năm tới phục vụ đồng bộ tự động qua URL.

Cách dùng:
    python main.py                          # Tạo file tổng hợp 10 năm tới và cập nhật viet_lunar_latest.ics
    python main.py --split                  # Tạo thêm các file riêng lẻ từng năm và file zip
    python main.py --start 2026 --end 2036  # Tạo lịch cho khoảng năm tùy chọn
    python main.py --year 2027              # Chỉ tạo lịch cho một năm cụ thể
"""
import argparse
import re
import sys
import time
from src.ics import create_zip
from src.files import atomic_write
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

# Đảm bảo đường dẫn gốc của project luôn nằm trong sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

from src.config import OUTPUT_DIR, DEFAULT_YEARS_AHEAD
from src.ics_generator import LunarCalendarGenerator
from src.calendar_options import HOLIDAYS, load_custom_holidays, select_holidays


def print_banner():
    banner = r"""
╔══════════════════════════════════════════════════════════╗
║         🌙  LỊCH ÂM VIỆT NAM — iCalendar Generator       ║
║              Múi giờ GMT+7 (Asia/Ho_Chi_Minh)             ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)


def format_size(path: Path) -> str:
    """Trả về kích thước file dạng KB / MB."""
    size = path.stat().st_size
    if size >= 1_048_576:
        return f'{size / 1_048_576:.2f} MB'
    return f'{size / 1024:.1f} KB'


def count_events(filepath: Path) -> int:
    """Đếm số VEVENT trong file .ics."""
    count = 0
    with filepath.open('rb') as file:
        for line in file:
            if line.strip() == b'BEGIN:VEVENT':
                count += 1
    return count


def create_zip_archive(files: list[Path], output_zip: Path):
    """Nén danh sách các file .ics vào một file nén định dạng .zip."""
    create_zip(files, output_zip)
    return output_zip


def cleanup_past_files(output_path: Path, current_year: int, prefix='viet_lunar') -> list[str]:
    """
    Tự động xóa các file của những năm đã qua để giữ thư mục output luôn sạch sẽ.
    - Xóa file lẻ từng năm: viet_lunar_{year}.ics nếu year < current_year
    - Xóa file tổng hợp cũ: viet_lunar_{start}_{end}.ics nếu start < current_year
    - Xóa file zip cũ: viet_lunar_yearly_{start}_{end}.zip nếu start < current_year
    """
    removed: list[str] = []
    if not output_path.exists():
        return removed

    single_year_re = re.compile(r'^' + re.escape(prefix) + r'_(\d{4})\.ics$')
    range_ics_re = re.compile(r'^' + re.escape(prefix) + r'_(\d{4})_(\d{4})\.ics$')
    range_zip_re = re.compile(r'^' + re.escape(prefix) + r'_yearly_(\d{4})_(\d{4})\.zip$')

    for file in output_path.iterdir():
        if not file.is_file():
            continue

        # 1. File lẻ từng năm đã qua
        m_single = single_year_re.match(file.name)
        if m_single and int(m_single.group(1)) < current_year:
            file.unlink()
            removed.append(file.name)
            continue

        # 2. File tổng hợp cũ có năm bắt đầu đã qua
        m_range = range_ics_re.match(file.name)
        if m_range and int(m_range.group(1)) < current_year:
            file.unlink()
            removed.append(file.name)
            continue

        # 3. File zip cũ có năm bắt đầu đã qua
        m_zip = range_zip_re.match(file.name)
        if m_zip and int(m_zip.group(1)) < current_year:
            file.unlink()
            removed.append(file.name)
            continue

    return removed


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(
        description='Tạo file iCalendar (.ics) Lịch Âm Việt Nam',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        '--start', type=int, default=None,
        help=f'Năm bắt đầu (mặc định: năm hiện tại)',
    )
    parser.add_argument(
        '--end', type=int, default=None,
        help=f'Năm kết thúc (mặc định: năm bắt đầu + {DEFAULT_YEARS_AHEAD} năm)',
    )
    parser.add_argument(
        '--year', type=int, default=None,
        help='Chỉ tạo file cho 1 năm cụ thể (ghi đè --start / --end)',
    )
    parser.add_argument(
        '--split', action='store_true',
        help='Tạo file riêng cho từng năm (ngoài file tổng hợp)',
    )
    parser.add_argument(
        '--output-dir', type=str, default=None,
        help='Thư mục xuất: output cho lịch chuẩn; .local/output cho lịch tùy chỉnh',
    )
    parser.add_argument('--language', choices=('vi', 'en'), default='vi', help='Ngôn ngữ lịch: vi hoặc en')
    parser.add_argument('--holidays', default='all', help='all, none hoặc các mã lễ cách nhau bằng dấu phẩy')
    parser.add_argument('--custom-holidays', type=Path, help='Tệp JSON ngày lễ riêng (âm hoặc dương lịch)')
    parser.add_argument('--list-holidays', action='store_true', help='Liệt kê mã ngày lễ rồi thoát')
    args = parser.parse_args()
    if args.list_holidays:
        for id, rule in HOLIDAYS.items():
            print(f'{id}: {rule.name(args.language)}')
        return
    try:
        select_holidays(args.holidays)
        custom = load_custom_holidays(args.custom_holidays) if args.custom_holidays else ()
    except (ValueError, OSError) as error:
        parser.error(str(error))
    customized = args.holidays != 'all' or args.custom_holidays is not None
    prefix = ('viet_lunar_custom_' + args.language) if customized else (
        'viet_lunar' if args.language == 'vi' else 'viet_lunar_en'
    )

    print_banner()

    # Xử lý tham số năm (Mặc định: Năm hiện tại -> +10 năm cuốn chiếu)
    current_year = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).year

    if args.year is not None:
        start_year = end_year = args.year
    else:
        start_year = args.start if args.start is not None else current_year
        end_year = args.end if args.end is not None else (start_year + DEFAULT_YEARS_AHEAD)

    if not (1900 <= start_year <= end_year <= 2098):
        parser.error('Khoảng năm hỗ trợ: 1900–2098; năm bắt đầu phải không lớn hơn năm kết thúc.')

    default_output = ROOT_DIR / ('.local/output' if customized else OUTPUT_DIR)
    output_path = Path(args.output_dir) if args.output_dir else default_output
    output_path.mkdir(parents=True, exist_ok=True)

    gen = LunarCalendarGenerator(args.language, args.holidays, custom)
    total_files: list[Path] = []

    print(f'📅 Khoảng thời gian : {start_year} → {end_year}')
    print(f'📂 Thư mục output   : {output_path.name}')
    print()

    # ── 1. Tạo file riêng từng năm (nếu yêu cầu --split hoặc --year) ─
    if args.split or args.year:
        years = range(start_year, end_year + 1)
        iter_years = tqdm(years, desc='Đang tạo file từng năm', unit='năm') \
            if HAS_TQDM else years

        yearly_files: list[Path] = []
        for year in iter_years:
            t0 = time.time()
            cal = gen.generate_year(year)
            fname = output_path / f'{prefix}_{year}.ics'
            gen.save(cal, fname)
            yearly_files.append(fname)
            total_files.append(fname)
            elapsed = time.time() - t0
            if not HAS_TQDM:
                print(f'  ✅ {fname.name}  ({format_size(fname)}, {elapsed:.1f}s)')

        # Nén vào file zip nếu dùng --split (nhiều hơn 1 năm)
        if args.split and len(yearly_files) > 1:
            zip_name = output_path / f'{prefix}_yearly_{start_year}_{end_year}.zip'
            print(f'\n📦 Đang nén {len(yearly_files)} file vào {zip_name.name}...')
            create_zip_archive(yearly_files, zip_name)
            total_files.append(zip_name)
            print(f'  ✅ Đã tạo file zip ({format_size(zip_name)})')

    # ── 2. Tạo file tổng hợp & viet_lunar_latest.ics ───────────────
    if not args.year:
        suffix = f'{start_year}_{end_year}'
        if start_year == end_year:
            suffix = str(start_year)

        print(f'\n⏳ Đang tạo file tổng hợp {start_year}–{end_year} '
              f'({end_year - start_year + 1} năm)...')
        t0 = time.time()
        cal = gen.generate_range(start_year, end_year)

        # Lưu file tên theo khoảng năm
        fname = output_path / f'{prefix}_{suffix}.ics'
        gen.save(cal, fname)
        total_files.append(fname)

        # Cập nhật file viet_lunar_latest.ics phục vụ link URL cố định
        latest_fname = output_path / f'{prefix}_latest.ics'
        atomic_write(latest_fname, fname.read_bytes())
        total_files.append(latest_fname)

        elapsed = time.time() - t0
        print(f'  ✅ Hoàn thành trong {elapsed:.1f}s')

    # Chỉ dọn tệp cũ sau khi tạo lịch thành công.
    cleanup_past_files(output_path, min(current_year, start_year), prefix)

    # ── 3. Tổng kết ────────────────────────────────────────────────
    print()
    print('═' * 55)
    print('📊 KẾT QUẢ:')
    for fp in total_files:
        n_events = count_events(fp) if fp.suffix == '.ics' else 0
        print(f'   📄 {fp.name}')
        print(f'      → {n_events:,} events  |  {format_size(fp)}')
    print('═' * 55)
    print()
    print('🎉 Hoàn thành!')


if __name__ == '__main__':
    main()
