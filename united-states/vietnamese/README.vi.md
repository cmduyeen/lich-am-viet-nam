[English](README.md) · [Tiếng Việt](README.vi.md) · [Tất cả quốc gia](../../README.md)

# 🌙 Hoa Kỳ — Việt Nam — Lịch âm

Sao chép link dưới đây và dán vào ứng dụng lịch để đăng ký.

## 1. Thêm lịch bằng liên kết

Chỉ ngày lễ âm lịch

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_us_vietnamese_vi_festivals_latest.ics
```

Dán vào mục Thêm lịch từ URL hoặc Đăng ký lịch bằng URL trong Google Calendar, Apple Calendar hay Outlook rồi lưu. Tải và nhập file ICS không tự nhận cập nhật.

> Link mới hoạt động sau khi các tệp được công bố lên nhánh main.

Dành cho cộng đồng tại Hoa Kỳ. Ngày lễ theo hệ lịch gốc, không phải ngày nghỉ chính thức của Mỹ. Sự kiện cả ngày không được dịch sang ngày khác theo múi giờ.

<details>
<summary>Lịch khác: mùng 1, rằm / ngày âm hằng ngày</summary>

**Ngày lễ + mùng 1, rằm**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_us_vietnamese_vi_observances_latest.ics
```

**Ngày âm hằng ngày + ngày lễ**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_us_vietnamese_vi_daily_latest.ics
```

</details>

<details>
<summary>Các ngày lễ âm lịch có trong lịch</summary>

| Ngày/tháng âm | Ngày lễ |
| --- | --- |
| 1/1 | Tết Nguyên Đán |
| 2/1 | Mùng 2 Tết |
| 3/1 | Mùng 3 Tết |
| 7/1 | Tết Khai Hạ |
| 10/1 | Vía Thần Tài |
| 15/1 | Tết Nguyên Tiêu |
| 3/3 | Tết Hàn Thực |
| 10/3 | Giỗ Tổ Hùng Vương |
| 15/4 | Lễ Phật Đản |
| 5/5 | Tết Đoan Ngọ |
| 15/7 | Tết Trung Nguyên |
| 15/7 | Lễ Vu Lan |
| 15/8 | Tết Trung Thu |
| 23/12 | Cúng Ông Táo |
| Ngày cuối năm âm lịch | Đêm Giao Thừa |

[Nguồn và quy tắc ngày lễ](../../docs/FESTIVALS.md)

</details>

## 2. Tùy chỉnh bằng Python

Chạy lệnh từ thư mục gốc dự án: [lunar-calender](../../README.md).

<details>
<summary>Lần đầu dùng? Cài môi trường Python 3.11+</summary>

Tải repo, mở thư mục gốc chứa main.py rồi tạo môi trường ảo. Kích hoạt môi trường trước khi cài dependencies đã khóa phiên bản.

```powershell
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --require-hashes -r requirements.txt
```

macOS / Linux:

```bash
source .venv/bin/activate
python -m pip install --require-hashes -r requirements.txt
```

</details>

```powershell
python main.py --config united-states/vietnamese/calendar.config.json --language vi
```

<details>
<summary>Chỉnh file cấu hình</summary>

Dùng calendar.config.json trong thư mục này. CLI được ưu tiên hơn JSON; có thể đổi language thành en khi cần lịch tiếng Anh.

Thêm "feed_name": "family" vào JSON trước khi đăng ký. URL custom_family_latest.ics giữ nguyên khi đổi tùy chỉnh; mỗi lịch dùng một tên riêng.

```json
{
  "country": "US",
  "tradition": "vietnamese",
  "language": "vi",
  "content": "festivals"
}
```

Dùng --year hoặc --start/--end để chọn năm; --lunar-days all/none/1,15 chọn ngày nền; --holiday-types lunar/solar/all/none chọn nhóm lễ; --split tạo tệp từng năm và ZIP; --output-dir đổi thư mục. Các màu #RRGGBB dùng với --calendar-color, --holiday-color, --lunar-day-color và --ordinary-color.

```powershell
python main.py --config united-states/vietnamese/calendar.config.json --language vi --year 2027 --split --output-dir exports
python main.py --config united-states/vietnamese/calendar.config.json --language vi --lunar-days 1,15
python main.py --countries VN,CN,KR --language en
```

[calendar.config.json](calendar.config.json)

</details>

<details>
<summary>Tự cập nhật trên fork của bạn</summary>

1. Fork repo và commit file cấu hình.
2. Bật Actions và cho phép workflow ghi nội dung repo.
3. Đặt CUSTOM_CONFIG thành đường dẫn cấu hình bên dưới.
4. Hoàn tất checklist phát hành rồi đặt PUBLISH_LUNAR_FEEDS thành true. Chạy Update Lunar Calendars; custom_config có thể ghi đè đường dẫn cho lần chạy thủ công.
5. Lấy tên file được in ra để tạo URL raw main/output của fork. Các lần chạy hằng năm dùng CUSTOM_CONFIG.

Lịch chạy hằng năm vào ngày 1/1, dự kiến 07:00 giờ Việt Nam; khi sửa code/dữ liệu hoặc chạy thủ công có thể tạo lại ngay. GitHub có thể tắt lịch chạy của repo công khai sau 60 ngày không hoạt động. Cần duy trì, theo dõi workflow hoặc dùng lịch ngoài để bật lại workflow khi cần rồi gọi workflow_dispatch.

```text
united-states/vietnamese/calendar.config.json
```

</details>

## Phạm vi và trợ giúp

Ngày lễ truyền thống; không phải lịch nghỉ chính thức hoặc nghỉ bù.

Feed đăng ký chỉ giữ năm hiện tại và năm kế tiếp. Năm cũ sẽ rời feed khi chuyển phạm vi. Muốn lưu lịch cũ, dùng --split --output-dir exports; output/ do chương trình quản lý, các bản xuất có năm ở đó sẽ được dọn khi tạo bộ feed tiêu chuẩn.

Phạm vi hỗ trợ: 1901–2099. Mặc định tạo 2 năm liên tiếp, bắt đầu từ năm hiện tại, trong giới hạn này.

Bộ lịch: vietnamese; múi giờ tham chiếu: Asia/Ho_Chi_Minh. Rằm là ngày 15 truyền thống, không phải thời điểm trăng tròn thiên văn. Không lặp lễ trong tháng nhuận.

Vẫn cần rà soát bởi người bản ngữ và thử đăng ký thực tế trên Google/Apple/Outlook trước khi phát hành chính thức.

<details>
<summary>FAQ</summary>

Nếu link chưa mở được, kiểm tra file đã có trên main của đúng repo. Chu kỳ làm mới do ứng dụng quyết định. Tùy chọn không hỗ trợ sẽ báo lỗi; màu tùy ứng dụng.

</details>

**Tài liệu kỹ thuật dùng chung** · English

[Feeds](../../docs/FEEDS.md) · [Development](../../docs/DEVELOPMENT.md) · [Automation](../../docs/AUTOMATION.md) · [Release](../../docs/RELEASE.md) · [Sources](../../tests/fixtures/README.md) · [index.json](../../output/index.json)

[cmduyeen](https://github.com/cmduyeen) · [MIT](../../LICENSE)
