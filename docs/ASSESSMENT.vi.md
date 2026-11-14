# Đánh giá sản phẩm lịch âm

Ngày đánh giá: 14/11/2026. Phạm vi: ba thư mục local calendar-lunar-vietnamese, calendar-lunar-chinese và lunar-calender; đồng thời kiểm tra feed Việt Nam công khai trên GitHub. Đây là đánh giá kỹ thuật và trải nghiệm sản phẩm, chưa phải chứng nhận lịch chính thức hay kết quả thử người dùng.

## Kết luận điều hành

lunar-calender nên là dự án phát triển chính. Hai thư mục cũ phù hợp làm bản đối chiếu và cơ sở tương thích; tiếp tục phát triển cả ba riêng biệt sẽ khiến các bản sửa lệch nhau. Bản mới đã đạt mức beta kỹ thuật có kiểm thử. Những phần cần đóng trước khi công bố rộng gồm: đối chiếu thêm dữ liệu lịch độc lập, rà soát bản ngữ, kiểm thử đăng ký/cập nhật thực tế trên ba ứng dụng lịch.

Yêu cầu giữ nhẹ đã được áp dụng: mặc định năm hiện tại và năm kế tiếp, giữ URL latest, bỏ bản xuất có năm và ZIP khỏi bộ tạo tiêu chuẩn, chạy định kỳ hằng năm và vẫn cho phép tạo lại khi sửa dữ liệu hoặc chạy thủ công. Phạm vi năm tùy chỉnh vẫn dùng được.

## Số liệu đã kiểm tra

| Chỉ tiêu | Hiện trạng |
| --- | --- |
| Bộ chuyển đổi âm lịch | 3: Việt Nam UTC+7, Trung Quốc UTC+8, Hàn Quốc |
| Hồ sơ nguồn | 8: VN, CN, TW, HK, MO, KR, SG, MY |
| Thị trường nơi sinh sống | Mỹ, dùng truyền thống Việt/Trung/Hàn; không phải bộ lịch Mỹ mới |
| Feed đăng ký | 77, trong đó 21 cho cộng đồng tại Mỹ |
| Nội dung feed | 25 festivals gồm một feed gộp; 24 observances; 24 daily; 4 feed tương thích cũ |
| Ngôn ngữ | 6: en, vi, zh-Hans, zh-Hant, ko, ms |
| Hướng dẫn | 26 trang gồm cặp Anh/bản ngữ và các trang chỉ mục |
| Kiểm thử | 66 test qua; gồm chuyển năm, UID, bộ lọc, bản dịch, ICS và rollback khi dọn tệp |
| Phạm vi mặc định hiện tại | 2026–2027 |
| Tệp đầu ra | 130 → 78 tệp |
| Dung lượng output | 60,84 → 10,36 MiB, giảm khoảng 83% |
| Tạo bộ feed sau thay đổi | Lần chuyển đổi đầu khoảng 52,72 giây; lần lặp khoảng 25,65 giây trên môi trường kiểm tra |
| Tính ổn định | Lần tạo lặp: 0 tệp thay đổi |

77 feed là các tổ hợp quốc gia/truyền thống/ngôn ngữ/chế độ, không phải 77 quốc gia hay 77 hệ lịch. Các con số hiệu năng là mẫu đo cục bộ, không phải cam kết tốc độ trên mọi máy hoặc tốc độ làm mới của Google/Apple/Outlook.

## Đánh giá từng sản phẩm

### Bản Việt Nam cũ

Điểm mạnh là bài toán rõ, URL đăng ký đơn giản và có một feed đang công khai. Bản local đã có nhiều nâng cấp, nhưng thư mục này không có .git tại thời điểm kiểm tra và không đồng nhất với dữ liệu đang phục vụ trên GitHub.

Điểm cần ưu tiên là chênh lệch ngày Tết 2030: feed công khai hiện ghi mùng 1 Tết vào 03/02/2030, còn bộ tính UTC+7 local trả về 02/02/2030. Dữ liệu [USNO](https://aa.usno.navy.mil/calculated/moon/phases?year=2030) ghi điểm sóc ngày 02/02 lúc 16:07 UT, tương ứng 23:07 cùng ngày tại UTC+7 và 00:07 ngày hôm sau tại UTC+8. Điều này củng cố nguyên nhân lệch múi giờ; vẫn cần chốt bộ đáp án Việt Nam độc lập trước khi phát hành sửa dữ liệu hàng loạt.

Khuyến nghị: duy trì URL cũ bằng dữ liệu đã kiểm chứng, chuyển phát triển chính sang dự án chung và có hướng dẫn chuyển feed rõ ràng. Không nên xem việc local đã sửa là người đăng ký đã nhận được bản sửa.

### Bản Trung Quốc cũ

Code nhỏ, dễ đọc và phạm vi văn hóa được giải thích rõ. Tuy nhiên không tìm thấy bộ test tự động trong thư mục này.

Đã tái hiện lỗi: ngày 27/06/2028 được ghi là “闰五月初五 · 端午节”, tức lễ Đoan Ngọ bị lặp trong tháng 5 nhuận. Nguyên nhân là tra ngày lễ bằng trị tuyệt đối tháng mà không loại tháng nhuận trong src/calendar_generator.py của repo cũ. Pipeline mới đã loại trường hợp này.

DTSTAMP trong bản cũ cũng được tạo lại theo giờ chạy, nên dữ liệu có thể thay đổi dù nội dung lịch không đổi. Khuyến nghị sửa lỗi tháng nhuận nếu feed cũ còn được duy trì, sau đó dùng bộ dữ liệu chung làm nguồn chính để giảm bảo trì song song.

### Dự án lunar-calender

Đây là nền tảng phù hợp nhất để tiếp tục. Mỗi quốc gia có thư mục và cặp README Anh/bản ngữ, cấu hình riêng; code chỉ có một lõi chung. Mỹ được mô hình hóa như nơi sinh sống và giữ nguyên lịch nguồn. UID phân biệt feed nguồn và feed Mỹ, đồng thời ổn định qua bản dịch và thứ tự chọn quốc gia.

Mức hiện tại là beta kỹ thuật. Chưa có dữ liệu thử người dùng chứng minh khả năng tìm và đăng ký feed nhanh; chưa có kiểm thử đăng ký thực tế được ghi nhận trong release checklist. Thư mục local mới không có .git và chưa được công bố thành repo mới.

## Các vấn đề đã tái hiện và trạng thái

| Mức | Vấn đề | Trạng thái |
| --- | --- | --- |
| Ưu tiên cao | Feed Việt Nam công khai khác bộ tính UTC+7 local tại Tết 2030 | Cần đối chiếu và phát hành bản sửa đã kiểm chứng |
| Ưu tiên cao | Bản Trung Quốc cũ lặp lễ trong tháng nhuận | Tái hiện được; pipeline mới đã tránh; repo cũ chưa sửa trong lượt này |
| Ưu tiên trước phát hành | COLOR xuất mã hex thay vì tên màu CSS3 theo RFC 7986 | Đã sửa: tên màu CSS chuẩn gần nhất; RGB gốc ở X-LUNAR-COLOR, màu theo ứng dụng |
| Đã xử lý | --country VN không ghi đè được JSON đang chọn countries nhiều nước | Đã sửa và có test |
| Đã xử lý | JSON lunar_days [1, true] hoặc [1, 1.0] có thể lọt kiểm tra do khử trùng lặp trước kiểm tra kiểu | Đã sửa và có test |
| Đã xử lý | Bộ xuất mặc định lớn, tạo nhiều bản theo khoảng năm và ZIP | Mặc định hai năm, chỉ latest và index; snapshot là tùy chọn |

Theo [RFC 7986, mục COLOR](https://www.rfc-editor.org/rfc/rfc7986.html#section-5.9), COLOR dùng tên màu CSS3. Xuất COLOR:#E53935 chưa đúng dạng đó. Vì vậy câu “ICS hợp lệ” trước đây chỉ nên hiểu là qua bộ kiểm tra hiện có và parser của dự án, không đồng nghĩa đã đạt toàn bộ chuẩn hoặc tương thích mọi ứng dụng. Bản local đã chuyển COLOR sang tên màu chuẩn và giữ RGB gốc trong X-LUNAR-COLOR.

## Độ chính xác và giới hạn bằng chứng

- Trung Quốc đã được đối chiếu 1.825 ngày từ năm bảng HKO: 2026, 2027, 2030, 2033, 2034. Có kiểm tra tháng nhuận đặc biệt 2033.
- Việt Nam có ba mốc lịch sử trong fixture và kiểm tra liên tục tháng dài 29/30 ngày giai đoạn 2026–2036. Kiểm tra tính liên tục không thay thế bảng đáp án độc lập.
- Hàn Quốc có các mốc chính thức năm 2026 và một fixture upstream bổ sung. Không nên coi fixture của cùng thư viện là kiểm chứng độc lập toàn bộ.
- Giới hạn tính toán 1901–2099 và Hàn Quốc đến 2050 không có nghĩa mọi ngày trong toàn phạm vi đã được đối chiếu độc lập.
- Chưa có rà soát bản ngữ độc lập hoàn tất; danh mục ngày lễ được chọn lọc, không bao phủ mọi vùng, tôn giáo và truyền thống.

Nên ưu tiên bảng đối chiếu trọn năm độc lập cho Việt Nam và Hàn Quốc, đặc biệt trong phạm vi hai năm đang phục vụ. Cần tách độ đúng của ngày âm, quy tắc chọn lễ và chất lượng bản dịch thành ba loại kiểm tra riêng.

## Trải nghiệm người dùng và phạm vi sản phẩm

Điểm tốt: trang chủ là danh sách khu vực thu gọn; vào từng nước chỉ còn hai ngôn ngữ, một URL mặc định có thể copy và một cách tùy chỉnh bằng code. Mặc định chỉ lễ âm lịch giúp lịch cá nhân ít bị lấp đầy bởi sự kiện hằng ngày.

Cần làm rõ: SG/MY mới là hồ sơ truyền thống Trung Quốc, không phải toàn bộ ngày lễ của hai nước. Mỹ mới hỗ trợ cộng đồng Việt/Trung/Hàn, không phải lịch nghỉ liên bang hay tiểu bang. Lịch Trung Quốc dùng chữ phồn thể tại Mỹ vẫn giữ danh mục CN, không tự chuyển sang danh mục Đài Loan/Hồng Kông/Ma Cao.

Feed hai năm sẽ bỏ năm cũ khi chuyển phạm vi. Người cần lịch sử nên lưu snapshot với --split --output-dir exports. Tùy chọn này phải được giải thích rõ vì đăng ký URL không phải bản lưu trữ vĩnh viễn.

Nigeria, Ai Cập, Brazil và Mexico hiện chỉ nằm trong lộ trình. Thêm tên nước hoặc thư mục trống không tạo ra một sản phẩm đã được hỗ trợ.

## Tự động hóa và vận hành

Workflow hiện dự kiến chạy ngày 1/1 lúc 00:00 UTC, tức 07:00 giờ Việt Nam; vẫn chạy khi code/dữ liệu đổi hoặc khi kích hoạt thủ công. Thời điểm thực thi có thể trễ.

Có một điều kiện quan trọng: [GitHub tự tắt schedule của repo công khai sau 60 ngày không có hoạt động](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows). Vì vậy cron hằng năm không đủ để bảo đảm tự động vô thời hạn trên repo bị bỏ yên. Cần duy trì và theo dõi repo, hoặc dùng lịch ngoài có khả năng bật lại workflow khi cần rồi kích hoạt workflow_dispatch. Dự án chưa cấu hình một dịch vụ kích hoạt bên ngoài.

Tại lượt kiểm tra GitHub ngày 14/11/2026, chỉ 1/77 tên feed local có trong thư mục output của repo lich-am-viet-nam: viet_lunar_latest.ics. Đây là kiểm tra sự hiện diện tên tệp, không khẳng định nội dung public trùng byte với local. Các link mới trong README chưa dùng được trước khi tệp được công bố lên main.

Bộ xuất có staging, ghi tệp nguyên tử, rollback và dọn tệp theo đúng prefix. Đây là nền tảng tốt; vẫn cần thử tình huống cập nhật thật, xóa sự kiện khỏi feed, chuyển năm, lỗi mạng và phục hồi trên ba ứng dụng lịch.

## SEO và khả năng mở rộng

Thư mục riêng và liên kết hai chiều giữa bản Anh/bản ngữ tạo cấu trúc nội dung dễ phát triển. Chúng chưa tạo ra website được triển khai hay cấu hình SEO quốc tế. Khi có website cần URL canonical, lựa chọn ngôn ngữ và khai báo các bản thay thế phù hợp, ví dụ hreflang theo [hướng dẫn Google](https://developers.google.com/search/docs/specialty/international/localized-versions).

Nội dung hiện còn mang tính hướng dẫn mẫu. Nên bổ sung thông tin riêng có ích cho từng nước: các lễ được chọn, quy tắc vùng miền, ví dụ năm hiện tại và giới hạn cụ thể. Không nên coi việc tăng số thư mục, feed hoặc bản dịch là bằng chứng tăng trưởng người dùng.

## Thứ tự triển khai tiếp theo

1. Chốt dữ liệu UTC+7 và xử lý các sai khác ở feed đang công khai; sửa xuất COLOR đúng chuẩn.
2. Hoàn tất đối chiếu lịch độc lập và rà soát bản ngữ cho các hồ sơ đầu tiên.
3. Thử đăng ký, cập nhật cùng UID, xóa sự kiện và chuyển năm trên Google Calendar, Apple Calendar, Outlook.
4. Công bố một nguồn repo chính, kiểm tra URL thực tế và giữ các feed tương thích cần thiết.
5. Xác định cách duy trì lịch tự động nếu repo công khai ít hoạt động.
6. Sau đó mở rộng nhóm Phật giáo hoặc lịch Hồi giáo theo thị trường đã chọn, với nguồn xác nhận địa phương riêng.

Đề xuất sản phẩm: giữ một lõi chung và phạm vi phục vụ nhỏ, làm chắc ngày lễ và đăng ký URL trước. Với mặc định hai năm, vấn đề dung lượng đã giảm đáng kể; các ưu tiên lớn còn lại là dữ liệu độc lập, khả năng tương thích và vận hành thật.

## Kiểm tra luồng chạy bổ sung

Đã thêm feed_name / --feed-name để URL tùy chỉnh không đổi khi sửa cấu hình; cấu hình lỗi ở batch dừng trước khi ghi output và trả lỗi CLI gọn. Tên trùng nhưng cấu hình khác bị từ chối. Bản xuất COLOR nay dùng tên màu CSS trong bảng màu nhẹ, giữ RGB yêu cầu ở X-LUNAR-COLOR; ứng dụng có thể bỏ qua màu. Các thay đổi này không thay đổi ngày hay UID. Kiểm thử ứng dụng lịch và công bố GitHub vẫn chưa thực hiện.

Kết quả chạy bổ sung: 66/66 test qua. Sinh lại 77 feed thành công; so sánh toàn bộ UID, DTSTART, DTEND trước/sau không đổi. Lần sinh thứ hai: 0 file thay đổi. Thử CLI tạo custom_family_latest.ics rồi đổi màu: giữ URL, ngày và UID; SEQUENCE tăng đúng. Hai lượt build kèm đối chiếu mất 68,33 giây trên máy kiểm tra.

## Bản hoàn thiện với automation bằng code

Dự án hiện có .venv riêng, không phụ thuộc hai thư mục code cũ. 86/86 test qua trong môi trường mới. Kiểm thử thành phẩm dùng parser ICAL.js độc lập và Edge headless đã đọc 77 feed / 21.192 sự kiện, kiểm tra URL tải lại không trùng UID, bốn múi giờ, bố cục README và ảnh chụp không có con trỏ. Danh mục lễ mới và nguồn nằm ở FESTIVALS.md; các sự kiện trùng ngày không bị ghi đè.

Automation sử dụng GitHub Actions và src/maintenance.py, có bộ cài Windows Task Scheduler mỗi năm một lần. Không có automation ChatGPT. Guard xử lý workflow bị GitHub tắt do không hoạt động; bỏ qua dữ liệu đã đủ năm và lần build đang chạy. Chạy lại có --if-needed mất khoảng 0,4 giây trên máy thử; ép build thật vẫn cho 0 file thay đổi. Không có commit giữ hoạt động giả, dịch vụ thu phí hoặc server chạy nền. Xem AUTOMATION.md và evidence/ để tái hiện.
