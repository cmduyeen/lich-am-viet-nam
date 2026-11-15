**Tiếng Việt** · [English](README.en.md)

<h1 align="center">🌙 Lịch Âm Việt Nam</h1>

<p align="center">
  Lịch âm và ngày lễ Việt Nam, đồng bộ với ứng dụng lịch yêu thích bằng một liên kết.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/Gi%E1%BA%A5y_ph%C3%A9p-MIT-FFD1DC?style=flat" alt="Giấy phép MIT" /></a>
  <img src="https://img.shields.io/badge/C%E1%BA%ADp_nh%E1%BA%ADt-H%C3%A0ng_n%C4%83m-FFF0F5?style=flat" alt="Cập nhật hàng năm" />
  <img src="https://img.shields.io/badge/Ph%E1%BA%A1m_vi-10_n%C4%83m_t%E1%BB%9Bi-FFD1DC?style=flat" alt="10 năm tiếp theo" />
  <img src="https://img.shields.io/badge/%C4%90%E1%BB%8Bnh_d%E1%BA%A1ng-iCalendar_(.ics)-FFF0F5?style=flat" alt="Định dạng iCalendar" />
</p>

<p align="center">
  <img width="900" alt="Minh họa Lịch Âm Việt Nam" src="https://github.com/user-attachments/assets/64fc3e3d-d883-4504-84a3-e5f797dbb7e2" />
</p>

---

## 1. Thêm nhanh bằng liên kết

Sao chép liên kết và chọn **Thêm lịch từ URL** hoặc **Đăng ký lịch bằng URL** trong ứng dụng lịch của bạn:

**Tiếng Việt**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_latest.ics
```

**English**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_en_latest.ics
```

Sau đó dán liên kết và lưu. Hãy đăng ký bằng URL để ứng dụng tự nhận các lần cập nhật, thay vì tải tệp `.ics` về máy. Tương thích với Google Calendar, Apple Calendar, Outlook và các ứng dụng hỗ trợ iCalendar.

Chỉ cần chọn **một** ngôn ngữ. Ví dụ cùng ngày Trung Thu: `15/8 • Tết Trung Thu` hoặc `15/8 • Mid-Autumn Festival`. Liên kết tiếng Việt cũ vẫn dùng được.

### Nội dung lịch

- Ngày âm lịch tương ứng với từng ngày dương lịch.
- Ngày mùng 1, ngày rằm và đêm Giao Thừa.
- Ngày lễ lớn: Tết Dương lịch, Tết Nguyên Đán, Giỗ Tổ Hùng Vương, Ngày Giải phóng miền Nam, Ngày Quốc tế Lao động và Quốc khánh.
- Dịp truyền thống: Ông Công Ông Táo, Vía Thần Tài, Tết Nguyên Tiêu, Phật Đản, Tết Đoan Ngọ, Vu Lan và Tết Trung Thu.

Dữ liệu sử dụng múi giờ Việt Nam (GMT+7), được cập nhật tự động hằng năm và duy trì cho 10 năm tiếp theo.


## 2. Tự tạo lịch bằng Python

Dùng Python 3.11 trở lên, tải mã nguồn rồi cài thư viện:

```sh
git clone https://github.com/cmduyeen/lich-am-viet-nam.git
cd lich-am-viet-nam
python -m pip install -r requirements.txt
```

**Chọn ngôn ngữ**, mặc định có tất cả lễ:

```sh
python main.py --language vi
python main.py --language en
```

**Chọn ngày lễ** muốn ghi kèm (ví dụ Tết và Trung Thu):

```sh
python main.py --language vi --holidays tet-1,tet-2,tet-3,mid-autumn
```

Đổi `vi` thành `en` để tạo bản tiếng Anh. Dùng `--holidays none` để chỉ ghi ngày âm, mùng 1 và rằm. Mọi lựa chọn đều giữ lịch âm **hằng ngày**.

<details>
<summary>Mã ngày lễ và cách thêm ngày riêng</summary>

Xem toàn bộ mã lễ:

```sh
python main.py --list-holidays --language vi
```

| Mã | Ngày lễ |
| --- | --- |
| `tet-1`, `tet-2`, `tet-3` | Mùng 1, 2, 3 Tết |
| `new-year-eve` | Giao Thừa |
| `god-of-wealth` | Vía Thần Tài |
| `first-full-moon` | Tết Nguyên Tiêu |
| `hung-kings` | Giỗ Tổ Hùng Vương |
| `buddha-birthday` | Phật Đản |
| `doan-ngo` | Tết Đoan Ngọ |
| `vu-lan` | Vu Lan |
| `mid-autumn` | Trung Thu |
| `kitchen-gods` | Ông Công Ông Táo |
| `new-year` | Tết Dương lịch |
| `reunification` | Ngày Giải phóng miền Nam |
| `labour-day` | Quốc tế Lao động |
| `national-day` | Quốc khánh |

Sao chép và sửa [examples/holidays.json](examples/holidays.json) để thêm ngày giỗ, sinh nhật hoặc ngày kỷ niệm. Mỗi ngày có `calendar` là `lunar` (âm lịch) hoặc `solar` (dương lịch), `month`, `day`, và tên bằng `vi`/`en`:

```json
[
  {
    "calendar": "lunar",
    "month": 3,
    "day": 12,
    "name": {"vi": "Ngày giỗ gia đình", "en": "Family memorial day"}
  }
]
```

```sh
python main.py --language vi --holidays tet-1,mid-autumn --custom-holidays examples/holidays.json
```

Ngày riêng được thêm vào các lễ đã chọn. Lễ âm chỉ áp dụng ở tháng thường; ngày 30 chỉ có trong tháng đủ, ngày 29/2 dương chỉ có trong năm nhuận. Nếu nhiều lễ trùng ngày, chúng được ghi kèm trong **một** sự kiện.

</details>

Tệp nằm trong `output/`: mặc định là `viet_lunar_latest.ics` (Việt) hoặc `viet_lunar_en_latest.ics` (Anh). Khi chọn lễ hoặc thêm ngày riêng, tệp là `viet_lunar_custom_vi_latest.ics` hoặc `viet_lunar_custom_en_latest.ics`, giữ riêng với lịch đăng ký nhanh.

Có thể thêm `--year 2027` để xuất riêng năm 2027, `--start 2026 --end 2036` để chọn khoảng năm, `--split` để xuất từng năm kèm ZIP, hoặc `--output-dir my-calendar` để đổi thư mục. Với `--year`, tệp được đặt theo năm thay vì `latest`.

Nhập tệp `.ics` vừa tạo vào ứng dụng lịch. Muốn bản tùy chỉnh tự đồng bộ qua URL, bạn cần lưu tệp trên địa chỉ công khai cố định và chạy lại Python khi muốn cập nhật; các URL thêm nhanh ở trên được kho tự cập nhật hằng năm.

---

<p align="center">
  Phần mềm mã nguồn mở theo giấy phép <a href="LICENSE">MIT</a>.
</p>
