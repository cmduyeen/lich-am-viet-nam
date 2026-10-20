<!-- SEO Metadata & Social Graph -->
<meta name="description" content="Lịch Âm Việt Nam — Đồng bộ tự động vào Google Calendar, Apple Calendar, Outlook. Chuẩn xác, tối giản, tự động duy trì 10 năm tới.">
<meta name="keywords" content="lich am viet nam, lich am google calendar, lich am apple calendar, lich am ics, dong bo lich am, cmduyeen, pinkie suite">
<meta name="author" content="cmduyeen">
<meta property="og:title" content="🌙 Lịch Âm Việt Nam — Tự Động Đồng Bộ & Tối Giản">
<meta property="og:description" content="Đồng bộ Lịch Âm Việt Nam chuẩn xác, tối giản và tự động duy trì trọn đời cho Google Calendar, Apple Calendar và Outlook.">
<meta property="og:url" content="https://github.com/cmduyeen/lich-am-viet-nam">
<meta property="og:type" content="website">

<h1 align="center">🌙 Lịch Âm Việt Nam dùng nhanh trong Google Calendar, Apple Calendar và Outlook</h1>

<p align="center">
  Đồng bộ Lịch Âm Việt Nam chuẩn xác, tối giản và tự động duy trì trọn đời.
</p>

<p align="center">
  Tiếng Việt | <a href="README.en.md">English</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-FFD1DC?style=flat" alt="License" /></a>
  <img src="https://img.shields.io/badge/Cập_nhật-Tự_động_hàng_năm-FFF0F5?style=flat&logoColor=D4698B" alt="Auto Update" />
  <img src="https://img.shields.io/badge/Dữ_liệu-10_năm_tới-FFD1DC?style=flat" alt="10 Years" />
  <img src="https://img.shields.io/badge/Định_dạng-iCalendar_.ics-FFF0F5?style=flat&logoColor=D4698B" alt="ICS Format" />
</p>

<p align="center">
  <img width="900" alt="Lịch Âm Việt Nam" src="https://github.com/user-attachments/assets/64fc3e3d-d883-4504-84a3-e5f797dbb7e2" />
</p>

---

### Lý do ra đời

Xuất phát từ lối sống tối giản — không muốn cài thêm ứng dụng phụ phiền phức, dự án ra đời để đồng bộ Lịch Âm trực tiếp vào app lịch mặc định có sẵn trên mọi thiết bị:

- **Không cần cài app** — Tích hợp thẳng vào Google Calendar, Apple Calendar có sẵn.
- **Sạch mắt & Tối giản** — Chỉ hiện ngày âm và ngày lễ lớn, không thông báo rác.
- **Tự động trọn đời** — Sẵn sàng cho 10 năm tới, tự động cập nhật không cần can thiệp.

---

### Đăng ký lịch (Subscribe URL)

Dán đường dẫn đăng ký lịch sau vào ứng dụng lịch của bạn:

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/viet_lunar_latest.ics
```

Bản tiếng Anh có tiêu đề và mô tả sự kiện riêng: xem [hướng dẫn tiếng Anh](README.en.md#subscribe).
Đường dẫn lịch tiếng Việt hiện tại không thay đổi.

#### Lịch tối giản: chỉ Rằm và Tết Nguyên Đán

- [Bản tối giản tiếng Việt](output/viet_lunar_minimal_latest.ics).
- [Bản tối giản tiếng Anh](output/viet_lunar_en_minimal_latest.ics).

Mở tệp đã chọn, nhấn **Raw**, rồi sao chép URL vào ứng dụng lịch để đăng ký.
Dùng URL của kho và nhánh đang xem; không dùng nhánh `main` của kho gốc nếu
tệp chưa được hợp nhất vào đó. Chọn một bản lịch để tránh hiển thị trùng sự kiện.

Hai bản tối giản có cùng ngày, với tiêu đề tiếng Việt:

- **Rằm**: ngày 15 của mọi tháng âm lịch, **kể cả tháng nhuận**. Đây là quy ước
  âm lịch truyền thống, **không phải thời điểm hoặc ngày trăng tròn thiên văn chính xác**.
  Tiêu đề vẫn là Rằm khi trùng Tết Trung Thu, Vu Lan hoặc ngày lễ khác.
- **Tết Nguyên Đán**: chỉ mùng 1 tháng Giêng **không nhuận**. Không gồm Giao Thừa,
  mùng 2, mùng 3 hay mùng 1 của tháng nhuận.

Sự kiện kéo dài cả ngày; phần mô tả giữ ngày âm và ghi rõ tháng nhuận nếu có.
Các bản đầy đủ và tối giản có mã sự kiện, tệp và URL riêng, không ghi đè nhau.

Tạo bản tối giản tiếng Việt (mặc định), tiếng Việt tường minh hoặc tiếng Anh:

```sh
python main.py --minimal --split
python main.py --language vi --minimal --split
python main.py --language en --minimal --split
```

Tiền tố tệp là `viet_lunar_minimal` hoặc `viet_lunar_en_minimal`, với các dạng
`_latest.ics`, `_<năm>.ics`, `_<năm đầu>_<năm cuối>.ics` và `_yearly_<năm đầu>_<năm cuối>.zip`.
`--year` chỉ tạo tệp một năm, không thay thế lịch `latest`; `--output-dir` chọn thư mục khác.
Việc dọn tệp cũ chỉ áp dụng cho ngôn ngữ và chế độ đã chọn. Workflow hằng năm
được cấu hình tạo cả bản đầy đủ và tối giản cho hai ngôn ngữ.

<details open>
<summary><b>Hướng dẫn cài đặt nhanh theo thiết bị</b></summary>
<br>

- **Apple (iPhone / iPad / Mac)**: Cài đặt → Lịch → Tài khoản → Thêm tài khoản → Khác → Thêm lịch đã đăng ký → Dán link → Lưu.
- **Google Calendar (Web / Android)**: Truy cập [calendar.google.com](https://calendar.google.com) → Nhấn biểu tượng **+** cạnh mục *Lịch khác* → Chọn *Từ URL* → Dán link.
- **Microsoft Outlook**: File → Open & Export → Import/Export → Import an iCalendar (.ics) → Dán link.

</details>

---

### Danh mục ngày lễ lớn

<details open>
<summary><b>Quốc lễ nghỉ chính thức</b></summary>
<br>

- **Tết Dương Lịch**: Ngày 1 tháng 1 Dương lịch.
- **Tết Nguyên Đán**: Đêm Giao Thừa, Mùng 1, Mùng 2, Mùng 3 Tết Âm lịch.
- **Giỗ Tổ Hùng Vương**: Ngày 10 tháng 3 Âm lịch.
- **Giải Phóng Miền Nam**: Ngày 30 tháng 4 Dương lịch.
- **Quốc Tế Lao Động**: Ngày 1 tháng 5 Dương lịch.
- **Quốc Khánh**: Ngày 2 tháng 9 Dương lịch.

</details>

<details open>
<summary><b>Lễ hội truyền thống dân tộc tiêu biểu</b></summary>
<br>

- **Cúng Ông Công Ông Táo**: Ngày 23 tháng Chạp.
- **Vía Thần Tài**: Ngày mùng 10 tháng Giêng.
- **Rằm Tháng Giêng (Tết Nguyên Tiêu)**: Ngày 15 tháng Giêng.
- **Đại Lễ Phật Đản**: Ngày 15 tháng 4 Âm lịch.
- **Tết Đoan Ngọ**: Ngày 5 tháng 5 Âm lịch.
- **Lễ Vu Lan Báo Hiếu**: Ngày 15 tháng 7 Âm lịch (Rằm tháng 7).
- **Tết Trung Thu**: Ngày 15 tháng 8 Âm lịch (Rằm tháng 8).

</details>

---

### License

- [MIT License](LICENSE) — Miễn phí và mã nguồn mở.
- Copyright © 2026 [cmduyeen](https://github.com/cmduyeen) — Pinkie Suite.

<p align="center">
  <img src="assets/signature.svg" alt="cmduyeen" width="400" />
</p>
