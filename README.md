**Tiếng Việt** · [English](README.en.md)

<h1 align="center">🌙 Lịch Âm Việt Nam</h1>

<p align="center">
  Lịch âm và ngày lễ Việt Nam, đồng bộ với Google Calendar, Apple Calendar, Microsoft Outlook bằng một liên kết URL duy nhất (.ics). Tự động cập nhật hằng tháng, hoàn toàn miễn phí và không quảng cáo.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/Gi%E1%BA%A5y_ph%C3%A9p-MIT-FFD1DC?style=flat" alt="Giấy phép MIT" /></a>
  <img src="https://img.shields.io/badge/C%E1%BA%ADp_nh%E1%BA%ADt-H%C3%A0ng_th%C3%A1ng-FFF0F5?style=flat" alt="Cập nhật hằng tháng" />
  <img src="https://img.shields.io/badge/Ph%E1%BA%A1m_vi-10_n%C4%83m_t%E1%BB%9Bi-FFD1DC?style=flat" alt="10 năm tiếp theo" />
  <img src="https://img.shields.io/badge/%C4%90%E1%BB%8Bnh_d%E1%BA%A1ng-iCalendar_(.ics)-FFF0F5?style=flat" alt="Định dạng iCalendar" />
</p>

<p align="center">
  <a href="assets/screenshots/google-calendar-vi.png"><img width="1100" alt="Lịch âm hằng ngày cùng lễ âm và lễ dương trên Google Calendar" src="assets/screenshots/google-calendar-vi.png" /></a>
  <br /><em>Lịch Việt Nam · VI — Google Calendar, tháng 11/2026.</em>
</p>

### Điểm nổi bật

- 🔄 **Tự động cập nhật**: Đăng ký một lần qua URL, lịch tự động đồng bộ hằng tháng và duy trì liên tục cho 10 năm tiếp theo.
- 📅 **Lịch âm hằng ngày**: Ghi chú ngày âm (ví dụ: `15/8`) cho toàn bộ 365/366 ngày trong năm, kèm mùng 1, ngày rằm và đêm Giao Thừa.
- 🎋 **Đầy đủ ngày lễ**: Bao gồm các ngày lễ lớn, dịp truyền thống âm lịch và các ngày kỷ niệm dương lịch phổ biến tại Việt Nam.
- 📱 **Đa nền tảng**: Tương thích hoàn hảo với Google Calendar, Apple Calendar (iPhone, iPad, Mac), Microsoft Outlook và mọi ứng dụng hỗ trợ iCalendar (.ics).
- 🌏 **Phù hợp người Việt toàn cầu**: Thiết lập sự kiện cả ngày chuẩn theo múi giờ Việt Nam (GMT+7), kiều bào tại Mỹ, Úc, Nhật... không lo bị nhảy lệch ngày.
- 🛡️ **Bảo mật & Không quảng cáo**: Mã nguồn mở 100%, không chứa quảng cáo, không theo dõi người dùng, an toàn cho lịch cá nhân.

---

## 1. Thêm nhanh bằng liên kết

Sao chép liên kết và chọn **Thêm lịch từ URL** hoặc **Đăng ký lịch bằng URL** trong ứng dụng lịch của bạn:

**Tiếng Việt — Lịch Việt Nam · VI**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_latest.ics
```

**English — Vietnam Calendar · EN**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_en_latest.ics
```

Sau đó dán liên kết và lưu. Hãy đăng ký bằng URL để ứng dụng tự nhận các lần cập nhật, thay vì tải tệp `.ics` về máy. Tương thích với Google Calendar, Apple Calendar, Outlook và các ứng dụng hỗ trợ iCalendar.

Chỉ cần chọn **một** ngôn ngữ. Ví dụ cùng ngày Trung Thu: `15/8 • Tết Trung Thu` hoặc `15/8 • Mid-Autumn Festival`. Liên kết tiếng Việt cũ vẫn dùng được.

<details>
<summary><strong>Hướng dẫn chi tiết từng bước cho từng ứng dụng lịch</strong></summary>

#### Google Calendar (Máy tính, Android và iPhone)
1. Mở [Google Calendar](https://calendar.google.com/) trên trình duyệt web máy tính.
2. Ở cột bên trái, cạnh mục **Lịch khác** (Other calendars), nhấn vào biểu tượng **+** rồi chọn **Từ URL** (From URL).
3. Dán liên kết `.ics` ở trên vào ô **URL của lịch** rồi nhấn **Thêm lịch**.
4. Mở ứng dụng Google Calendar trên điện thoại: vào **Cài đặt** -> chọn tài khoản Google của bạn -> tích chọn hiển thị lịch vừa thêm và bật **Đồng bộ hóa** (Sync).

#### Apple Calendar (iPhone, iPad và macOS)
- **Trên iPhone / iPad (iOS)**:
  1. Mở **Cài đặt** (Settings) -> cuộn xuống chọn **Lịch** (Calendar) -> **Tài khoản Lịch** (hoặc **Tài khoản** -> **Thêm tài khoản**).
  2. Chọn **Khác** (Other) -> **Thêm lịch đã đăng ký** (Add Subscribed Calendar).
  3. Dán liên kết `.ics` vào ô **Máy chủ** (Server) -> nhấn **Tiếp theo** (Next) -> nhấn **Lưu** (Save).
- **Trên máy Mac (macOS)**:
  1. Mở ứng dụng **Lịch** (Calendar).
  2. Trên thanh menu trên cùng, chọn **Tệp** (File) -> **Đăng ký Lịch Mới...** (New Calendar Subscription...).
  3. Dán liên kết `.ics` -> nhấn **Đăng ký** (Subscribe) -> chọn tần suất Tự động làm mới là **Hằng ngày** -> nhấn **OK**.

#### Microsoft Outlook (Bản web và phần mềm máy tính)
- **Outlook trên trình duyệt web**:
  1. Truy cập [Outlook Calendar](https://outlook.live.com/calendar/) -> nhấn **Thêm lịch** (Add calendar).
  2. Chọn **Đăng ký từ web** (Subscribe from web) -> dán liên kết `.ics` -> đặt tên lịch rồi nhấn **Nhập** (Import).
- **Outlook phần mềm máy tính (Desktop App)**:
  1. Mở thẻ Calendar -> chọn **Add Calendar** trên thanh công cụ -> chọn **From Internet...**
  2. Dán liên kết `.ics` -> nhấn **OK** -> xác nhận đăng ký.

</details>

### Một lịch cho tất cả

- Ngày âm lịch **hằng ngày**; lễ âm và lễ dương ghi kèm trong cùng sự kiện.
- Ngày mùng 1, ngày rằm và đêm Giao Thừa.
- Ngày lễ lớn: Tết Dương lịch, Tết Nguyên Đán, Giỗ Tổ Hùng Vương, Ngày Giải phóng miền Nam, Ngày Quốc tế Lao động và Quốc khánh.
- Dịp truyền thống: Ông Công Ông Táo, Vía Thần Tài, Nguyên Tiêu, Hàn thực, Phật Đản, Đoan Ngọ, Vu Lan, Trung Thu và Hạ nguyên.
- Dịp dương lịch: Valentine, 8/3, 1/6, 28/6, 20/10, 20/11, Ngày Văn hóa Việt Nam 24/11 (từ 2026) và Giáng sinh.

Ví dụ: `12/10 • Nhà giáo Việt Nam`. Nhiều lễ trùng ngày vẫn chỉ có **một** sự kiện. [Danh mục và nguồn đối chiếu](docs/HOLIDAYS.md). Đây là lịch ngày lễ và dịp kỷ niệm; lịch nghỉ bù/hoán đổi làm việc cần theo thông báo từng năm.

Dữ liệu sử dụng múi giờ Việt Nam (GMT+7), được cập nhật tự động lúc 07:17 ngày 1 hằng tháng (giờ Việt Nam) và duy trì cho 10 năm tiếp theo.


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
| `valentine` | Lễ Tình nhân |
| `international-women` | Quốc tế Phụ nữ |
| `children` | Quốc tế Thiếu nhi |
| `family` | Gia đình Việt Nam |
| `vietnamese-women` | Phụ nữ Việt Nam |
| `teachers` | Nhà giáo Việt Nam |
| `culture` | Văn hóa Việt Nam (từ 2026) |
| `christmas-eve`, `christmas` | Đêm Giáng sinh, Giáng sinh |
| `han-thuc`, `ha-nguyen` | Hàn thực, Hạ nguyên |

Sao chép [examples/holidays.json](examples/holidays.json) thành `.local/holidays.json` rồi sửa bản riêng này để thêm ngày giỗ, sinh nhật hoặc ngày kỷ niệm. Mỗi ngày có `calendar` là `lunar` (âm lịch) hoặc `solar` (dương lịch), `month`, `day`, và tên bằng `vi`/`en`:

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
python main.py --language vi --holidays tet-1,mid-autumn --custom-holidays .local/holidays.json
```

Ngày riêng được thêm vào các lễ đã chọn. Lễ âm chỉ áp dụng ở tháng thường; ngày 30 chỉ có trong tháng đủ, ngày 29/2 dương chỉ có trong năm nhuận. Nếu nhiều lễ trùng ngày, chúng được ghi kèm trong **một** sự kiện.

</details>

Lịch chuẩn nằm trong `output/`: mặc định là `viet_lunar_latest.ics` (Việt) hoặc `viet_lunar_en_latest.ics` (Anh). Khi chọn lễ hoặc thêm ngày riêng, tệp được lưu trong `.local/output/` (không đưa lên Git), với tên `viet_lunar_custom_vi_latest.ics` hoặc `viet_lunar_custom_en_latest.ics`, giữ riêng với lịch đăng ký nhanh.

Có thể thêm `--year 2027` để xuất riêng năm 2027, `--start 2026 --end 2036` để chọn khoảng năm, `--split` để xuất từng năm kèm ZIP, hoặc `--output-dir my-calendar` để đổi thư mục. Với `--year`, tệp được đặt theo năm thay vì `latest`.

Nhập tệp `.ics` vừa tạo vào ứng dụng lịch. Muốn bản tùy chỉnh tự đồng bộ qua URL, bạn cần lưu tệp trên địa chỉ công khai cố định và chạy lại Python khi muốn cập nhật; các URL thêm nhanh ở trên được kho tự cập nhật hằng tháng. Ngày riêng trong lịch công khai sẽ được mọi người đọc; hãy giữ lịch cá nhân ở `.local/` nếu không muốn công khai.


## 3. Câu hỏi thường gặp (FAQ)

<details>
<summary><strong>Tại sao nên đăng ký bằng URL thay vì tải tệp .ics về nhập vào máy?</strong></summary>

Khi đăng ký bằng liên kết URL, ứng dụng lịch sẽ định kỳ tải dữ liệu mới nhất từ kho lưu trữ. Lịch được duy trì liên tục cho 10 năm tiếp theo và tự động cập nhật khi có bổ sung hoặc điều chỉnh ngày lễ. Ngược lại, nếu bạn tải tệp `.ics` về máy và nhập (import), các sự kiện sẽ bị ghi cứng vào dữ liệu cá nhân, không thể tự cập nhật và dễ gây trùng lặp sự kiện mỗi năm.
</details>

<details>
<summary><strong>Người Việt đang sinh sống tại nước ngoài (Mỹ, Úc, Nhật...) có bị lệch ngày âm không?</strong></summary>

Không bị lệch ngày. Toàn bộ các sự kiện trong lịch được thiết kế dưới dạng **sự kiện cả ngày** (All-Day Event) gắn liền với ngày tương ứng theo múi giờ Việt Nam (GMT+7). Khi hiển thị trên thiết bị cá nhân của bạn ở bất kỳ quốc gia nào, sự kiện vẫn xuất hiện đúng ngày dương lịch mà ngày âm lịch đó diễn ra tại Việt Nam, giúp kiều bào theo dõi chính xác ngày giỗ, rằm, mùng 1 và Tết truyền thống.
</details>

<details>
<summary><strong>Lịch âm được tính toán dựa trên thuật toán nào?</strong></summary>

Dữ liệu âm lịch được xây dựng dựa trên thuật toán thiên văn kinh điển và chuẩn xác của TS. Hồ Ngọc Đức (Viện Công nghệ Thông tin), kết hợp cơ sở múi giờ chuẩn UTC+7 (Hà Nội). Danh mục các ngày lễ và kỷ niệm được đối chiếu chính thức theo Bộ luật Lao động số 45/2019/QH14 và các nghị quyết quy phạm pháp luật hiện hành của Việt Nam (xem chi tiết tại [docs/HOLIDAYS.md](docs/HOLIDAYS.md)).
</details>

<details>
<summary><strong>Lịch có hiển thị ngày nghỉ bù hoặc hoán đổi ngày làm việc không?</strong></summary>

Đây là lịch ghi nhận ngày âm lịch, ngày lễ truyền thống và dịp kỷ niệm văn hóa. Lịch nghỉ bù hoặc các đợt hoán đổi ngày làm việc do Chính phủ quyết định hằng năm theo từng tình hình thực tế, vì vậy dự án giữ nguyên tắc trung thực với ngày lễ gốc và không suy diễn lịch nghỉ bù khi chưa có thông báo chính thức.
</details>

<details>
<summary><strong>Dự án có thu thập dữ liệu cá nhân hay chứa quảng cáo không?</strong></summary>

Hoàn toàn không. Dự án là mã nguồn mở 100% phi thương mại, không chèn quảng cáo, không chứa mã theo dõi và không thu thập bất kỳ dữ liệu cá nhân nào. Nếu bạn tự tạo lịch riêng kèm ngày giỗ hoặc sinh nhật bằng Python, dữ liệu cá nhân được lưu hoàn toàn cục bộ trên máy bạn tại thư mục `.local/` (đã được cấu hình tự động loại trừ khỏi Git).
</details>

---

[Vận hành và bảo trì](docs/OPERATIONS.md) · [Bảo vệ thông tin riêng](SECURITY.md)

<p align="center">
  Phần mềm mã nguồn mở theo giấy phép <a href="LICENSE">MIT</a>.
</p>
