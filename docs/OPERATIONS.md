# Vận hành và bảo trì

## Tiếng Việt

Kho được tổ chức như sau:

| Thư mục / tệp | Vai trò |
| --- | --- |
| `README.md`, `README.en.md` | Đăng ký nhanh và hướng dẫn Python bằng Việt/Anh |
| `main.py` | Lệnh tạo lịch |
| `src/` | Tính ngày âm, ngày lễ, xuất và kiểm tra ICS |
| `tests/` | Kiểm tra hồi quy và bảo vệ bản tùy chỉnh |
| `examples/` | Mẫu minh họa, không chứa dữ liệu riêng |
| `assets/screenshots/` | Ảnh Google Calendar riêng cho Việt/Anh, chỉ giữ phần lịch công khai |
| `output/` | Lịch công khai; giữ các tên tệp cũ để bảo toàn URL |
| `.local/` | Ngày riêng, lịch tự tạo; được bỏ qua bởi Git |
| `.github/` | Tự động cập nhật, kiểm thử, quét bí mật và Dependabot |

GitHub Actions chạy lúc 07:17 giờ Việt Nam ngày 1 hằng tháng, khi mã tạo lịch
trên `main` thay đổi, hoặc khi chọn **Run workflow** trong tab Actions.
GitHub có thể trì hoãn lịch chạy do hàng đợi. Máy tính cá nhân không cần bật.

Workflow kiểm thử trước, tạo hai ngôn ngữ, ghi `output/update-status.json`,
rồi chỉ thêm các tên tệp lịch chuẩn vào commit. Tệp tùy chỉnh không nằm trong
danh sách được xuất bản. Trạng thái cập nhật được ghi mỗi tháng, kể cả khi
nội dung lịch không đổi, giúp duy trì hoạt động của kho.

GitHub có thể tắt lịch chạy ở kho công khai không hoạt động trong 60 ngày:
[tài liệu GitHub](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows).
Nếu workflow bị tắt, cần bật lại trong Actions.

Tự động hóa không có nghĩa là không bao giờ cần bảo trì. Nó còn phụ thuộc
GitHub, phiên bản Python, thư viện và quyền của workflow. Dependabot kiểm tra
thư viện và Actions hằng tháng, mở PR cập nhật để kiểm thử và xem xét; không tự
merge các bản nâng cấp. Nếu Actions báo đỏ, cần kiểm tra nguyên nhân và chạy lại
sau khi sửa. Không đổi URL đăng ký khi cập nhật mã.

Bộ tính hiện hỗ trợ xuất năm 1900–2098. Với cửa sổ mặc định năm hiện tại cộng
10 năm, cần mở rộng và kiểm chứng phạm vi trước năm 2089. Đây không phải cam kết
tự chạy vô thời hạn.

Người đăng ký qua URL nhận bản mới khi ứng dụng lịch làm mới dữ liệu. Bản nhập
từ tệp ICS là bản chụp, không tự theo dõi URL.

## English

`src/` contains calendar logic; `tests/` verifies behavior; `examples/` contains
fictional templates; `output/` contains public feeds and compatible legacy
exports; `.local/` holds personal files ignored by Git. `.github/` contains
automation and dependency update configuration.

GitHub Actions refreshes both languages at 07:17 Vietnam time on the first day
of each month, on relevant changes to `main`, or on manual dispatch. GitHub may
delay scheduled jobs. Tests run before generation. Only standard public export
filenames are staged; personal calendars are excluded. The monthly status file
records a successful refresh and maintains repository activity.

Automation still depends on GitHub availability, Python, dependencies and
workflow permissions. Public repositories with 60 days of inactivity can have
their schedules disabled. Dependabot proposes monthly updates for review and
testing; it does not merge upgrades automatically. Check failed Actions runs
and re-enable disabled workflows when needed.

The supported export range is 1900–2098. The default rolling ten-year-ahead
window needs an extension and further validation before 2089. URL subscriptions
refresh according to the calendar app's schedule; imported ICS files are static.
