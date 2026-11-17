# 🌙 Lịch âm Việt Nam

[Tiếng Việt](README.md) · [English](README.en.md)

![Lịch âm Việt Nam](assets/lunar-calendar-cover.png)

Lịch âm Việt Nam theo múi giờ GMT+7, hiển thị bằng **tiếng Việt hoặc tiếng Anh**. Mỗi ngày có một sự kiện, gồm ngày âm và các dịp lễ tương ứng. Hai bản có cùng ngày; chỉ khác ngôn ngữ hiển thị.

## Đăng ký lịch

**Tiếng Việt**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_latest.ics
```

**Tiếng Anh**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_en_latest.ics
```

Dán một trong hai link vào mục **Thêm lịch từ URL / Đăng ký lịch** trong Google Calendar, Apple Calendar hoặc Outlook. Chỉ cần chọn một ngôn ngữ để tránh nhìn thấy hai bộ sự kiện. Nhập tệp ICS là bản chụp và không tự cập nhật theo URL.

### Thêm vào Google Calendar trong 4 bước

1. Sao chép link **tiếng Việt hoặc tiếng Anh** ở trên.
2. Mở [Google Calendar](https://calendar.google.com/) bằng trình duyệt trên máy tính.
3. Bên cạnh **Lịch khác**, nhấn **+ → Từ URL**.
4. Dán link, nhấn **Thêm lịch**. Lịch sẽ xuất hiện trong **Lịch khác**.

![Lịch âm tiếng Việt trong Google Calendar](assets/screenshots/google-calendar-vi.png)

**Video thao tác trực tiếp trên Google Calendar**

https://github.com/user-attachments/assets/77db24f7-752b-4ab0-9a5d-4c3d2b17af45

Thêm lần đầu trên máy tính, rồi mở ứng dụng Google Calendar cùng tài khoản trên điện thoại. Xem [hướng dẫn của Google](https://support.google.com/calendar/answer/37100?hl=vi).

Lịch mặc định gồm năm hiện tại và năm kế tiếp. Ứng dụng lịch quyết định thời điểm làm mới. Các thay đổi trong repo chỉ xuất hiện ở URL sau khi được đưa lên nhánh `main`.

## Tạo lịch bằng Python

Cần Python 3.11 trở lên:

```powershell
python -m pip install --require-hashes -r requirements.txt
python generate_all.py
```

Lệnh trên tạo đúng hai feed Việt–Anh trong `output/`. Chạy lại khi dữ liệu không đổi:

```powershell
python generate_all.py --if-needed
```

Chỉ tạo một ngôn ngữ hoặc xuất bản chụp từng năm:

```powershell
python main.py --language vi
python main.py --language en
python main.py --language vi --split --output-dir exports
```

## Chọn ngày lễ và thêm ngày riêng

```powershell
python main.py --language vi --list-holidays
python main.py --language en --holidays mid-autumn
python main.py --language vi --custom-holidays .local/holidays.json
```

Tệp ngày riêng theo [mẫu JSON](examples/holidays.json). Lịch tùy chỉnh mặc định được lưu trong `.local/output/`, được Git bỏ qua. Không đưa dữ liệu riêng lên repo công khai.

Ngày lễ là dịp kỷ niệm, không phải lịch nghỉ bù hoặc bảng tính ngày nghỉ hưởng lương. Xem [danh mục ngày lễ](docs/HOLIDAYS.md).

## Vận hành

GitHub Actions kiểm thử trước khi xuất bản, chạy hằng năm và khi mã nguồn thay đổi. Lần chạy không có thay đổi sẽ bỏ qua việc tạo và commit dữ liệu. Xem [tự động hóa](docs/AUTOMATION.md), [vận hành](docs/OPERATIONS.md), [kiểm tra phát hành](docs/RELEASE.md) và [bảo mật](SECURITY.md).

[MIT](LICENSE) · [cmduyeen](https://github.com/cmduyeen)
