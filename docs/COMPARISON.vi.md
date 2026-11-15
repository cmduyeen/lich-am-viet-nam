# So sánh và lựa chọn cập nhật

Đối chiếu mã nguồn ngày 15/11/2026:

- `cmduyeen/vietnamese-lunar-calendar`: `90cc099e09b591e3f87b891f2051698d942ee3e6`.
- `cmduyeen/lich-am-viet-nam`: `7246f977863a57acce94100c0ec664af0d400a32`.

| Nội dung | vietnamese-lunar-calendar | lich-am-viet-nam | Lựa chọn |
| --- | --- | --- | --- |
| Sử dụng | Nhiều chế độ, cấu hình JSON; mặc định chỉ lễ | Một lịch ghi ngày âm mỗi ngày | Giữ cách dùng đơn giản của kho đích |
| README | Nhiều tùy chọn và hướng dẫn kỹ thuật | Tiếng Việt, ngắn gọn, một URL | Giữ bản gốc, thêm README.en.md |
| Ngày âm | Tính sóc và trung khí theo GMT+7 | Lấy trực tiếp ngày âm Trung Quốc | Chuyển bộ tính GMT+7 |
| Tháng nhuận | Có xử lý riêng | Có thể lặp ngày lễ, thiếu nhãn nhuận | Không lặp lễ âm; ghi rõ tháng nhuận |
| Xuất ICS | Kiểm tra dữ liệu, ghi nguyên tử, giữ revision | Ghi trực tiếp và đổi DTSTAMP mỗi lần | Chuyển phần kiểm tra và revision |
| Tương thích | Tên tệp và UID theo hệ mới | URL và UID đã được đăng ký | Giữ viet_lunar_latest.ics và vnlunar-YYYYMMDD@cmduyeen |

Mỗi ngày vẫn chỉ có một sự kiện. Ví dụ: `2/8`, `1/8 • Mùng 1`,
`15/8 • Tết Trung Thu`. Giữ danh sách lễ dương hiện có.
Có hai cách sử dụng: đăng ký nhanh bản Việt/Anh, hoặc chạy Python chọn
ngôn ngữ và ngày lễ (kể cả ngày riêng theo tệp JSON). Cả hai đều ghi ngày âm
hằng ngày. Không chuyển lịch chỉ lễ hoặc hệ thống phát hành mới.

Bộ tính hỗ trợ ngày dân sự hiện đại 1900–2099. CLI giới hạn năm xuất
1900–2098 vì kiểm tra Giao Thừa cần đọc ngày tiếp theo.
Các trường Can Chi tháng và tiết khí phụ của API cũ vẫn dựa trên lunar-python;
chúng không được thêm vào sự kiện lịch hàng ngày trong lần cập nhật này.

Kiểm tra hồi quy gồm Tết 1968, 1985, 2007, 2026; tháng nhuận 2020;
365 sự kiện/năm 2026 ở cả hai ngôn ngữ; UID cũ; revision; ZIP ổn định;
chọn lễ; ngày riêng; nhiều lễ trùng ngày và đầu vào không hợp lệ.
