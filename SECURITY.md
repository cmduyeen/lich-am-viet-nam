# Thông tin riêng và bảo mật / Privacy and security

## Tiếng Việt

- Giữ ngày giỗ, sinh nhật và cấu hình cá nhân trong `.local/`. Tệp mẫu trong
  `examples/` chỉ có dữ liệu minh họa. Bản lịch tùy chỉnh mặc định lưu tại
  `.local/output/`, không phải thư mục lịch công khai.
- Không commit `.env`, token, mật khẩu, khóa riêng, báo cáo quét bí mật hoặc
  bản sao lưu kho. `.gitignore` chặn các mẫu thông dụng, nhưng không phải
  công cụ phát hiện mọi loại thông tin cá nhân.
- Workflow chỉ xuất bản các tên tệp lịch tiêu chuẩn. Khi chủ động lưu lịch
  cá nhân vào địa chỉ công khai, mọi người có thể đọc nội dung của nó.
- Workflow quét lịch sử Git bằng Gitleaks trên PR và khi đẩy `main`; không in
  giá trị tìm thấy và không tải báo cáo thô lên artifact. Quét bí mật không
  thể bảo đảm phát hiện mọi dữ liệu nhạy cảm.
- Workflow cập nhật dùng `GITHUB_TOKEN` do GitHub cấp cho lần chạy. Không cần
  thêm token cá nhân vào mã. Actions được ghim theo commit, thư viện Python
  được ghim phiên bản và hash; Dependabot đề xuất cập nhật hằng tháng.
- Nếu một khóa thật đã bị công khai, thu hồi hoặc thay khóa trước. Xóa tệp
  hiện tại không xóa được khóa khỏi lịch sử Git. Không đăng khóa vào issue,
  bình luận PR hoặc log khi báo lỗi.
- Khi commit từ máy cá nhân, dùng email `noreply` của GitHub nếu muốn giữ kín
  email cá nhân. Đổi email cho commit mới không đổi các commit cũ.

## English

Keep personal dates and configuration under `.local/`; custom exports default
to `.local/output/`. The `examples/` files are fictional templates. Git ignores
common credential, private calendar, log and backup patterns. Ignore rules and
secret scanning cannot identify every kind of private information.

The publishing workflow stages only standard public calendar filenames. Publicly
hosted personal calendars are readable by anyone. Gitleaks scans Git history on
pull requests and pushes to `main`; findings are fully redacted and raw reports
are not uploaded. The update job uses GitHub's temporary `GITHUB_TOKEN`, not a
personal token stored in source. Actions are pinned to commits, Python packages
to versions and hashes; Dependabot proposes monthly upgrades.

Revoke or rotate any exposed credential first. Deleting a file does not remove
it from Git history. Never paste credentials into issues, PR comments or logs.
Use your GitHub `noreply` address for commits to keep your personal email private;
changing it affects new commits only.
