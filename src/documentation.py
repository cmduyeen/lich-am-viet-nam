"""Generate country-specific English/native guides from shared calendar profiles.

Run from the project root: python -m src.documentation
Edit the locale copy here before regenerating translated country pages.
"""
from dataclasses import dataclass
import json
import os
from pathlib import Path
from .config import PUBLIC_FEED_BASE_URL, DEFAULT_YEARS_AHEAD
from .localization import LOCALES, title as festival_title
from .naming import output_prefix
from .profiles import PROFILES, RULES, FESTIVAL_SOURCES
from .user_config import CalendarOptions

ROOT = Path(__file__).resolve().parents[1]
LANGUAGE_NAMES = {'en':'English','vi':'Tiếng Việt','zh-Hans':'简体中文','zh-Hant':'繁體中文','ko':'한국어','ms':'Bahasa Melayu'}
TEXT = {
'en': dict(all='All countries',intro='Copy the URL below and subscribe in your calendar app.',subscribe='1. Subscribe by URL',festival='Lunar festivals only',paste='Paste it into Subscribe by URL in Google Calendar, Apple Calendar or Outlook, then save. Downloading and importing an ICS file does not receive automatic updates.',available='New links become available after these files are published to main.',more='Other calendars: lunar days 1 and 15 / every lunar day',observances='Festivals + lunar days 1 and 15',daily='Every lunar day + festivals',custom='2. Customize with Python',root='Run commands from the project root',setup='First time? Set up Python 3.11+',setup_text='Download the repository, open the root folder containing main.py, and create a virtual environment. Activate it before installing the pinned dependencies.',json='Edit your configuration',json_text='Use this folder’s calendar.config.json. CLI options override JSON. The English command below explicitly selects English; the stored configuration uses the native display language.',options='Use --year or --start/--end for dates, --lunar-days all/none/1,15 for background days, --holiday-types lunar/solar/all/none for categories, --split for yearly files and ZIP, and --output-dir for another folder. Colors accept #RRGGBB via --calendar-color, --holiday-color, --lunar-day-color and --ordinary-color.',auto='Automatic updates on your fork',auto_steps=['Fork the repository and commit your configuration.','Enable Actions and allow the workflow to write repository contents.','Set CUSTOM_CONFIG to the configuration path shown below.','Complete the release checklist, then set PUBLISH_LUNAR_FEEDS to true. Run Update Lunar Calendars; custom_config can override the path for a manual run.','Use the printed filename with your own fork’s raw main/output URL. Annual runs reuse CUSTOM_CONFIG.'],know='Coverage and help',range='Supported years: {first}–{last}. The default rolling calendar covers {window} consecutive years starting with the current year, within these limits.',rules='Calendar rules: {engine}; reference timezone: {timezone}. Traditional day 15 is not the exact astronomical full moon. Leap months do not repeat festivals.',faq='If a URL is unavailable, confirm the file is on main in the correct repository. App refresh intervals vary. Unsupported options raise an error; color support depends on the app.',status='Independent native-language review and live Google/Apple/Outlook subscription tests remain pending. These are candidate feeds until the release checks are complete.',legacy='Existing Vietnamese full and minimal subscriptions keep their filenames and UID formats. Running main.py without --country preserves the legacy mode; --minimal cannot be combined with --content.',read='Shared technical documentation',extra='Additional display language',source='Source calendar',variant='This guide accompanies the Traditional Chinese display edition; its dates and festival catalog remain those of the CN source profile.'),
'vi': dict(all='Tất cả quốc gia',intro='Sao chép link dưới đây và dán vào ứng dụng lịch để đăng ký.',subscribe='1. Thêm lịch bằng liên kết',festival='Chỉ ngày lễ âm lịch',paste='Dán vào mục Thêm lịch từ URL hoặc Đăng ký lịch bằng URL trong Google Calendar, Apple Calendar hay Outlook rồi lưu. Tải và nhập file ICS không tự nhận cập nhật.',available='Link mới hoạt động sau khi các tệp được công bố lên nhánh main.',more='Lịch khác: mùng 1, rằm / ngày âm hằng ngày',observances='Ngày lễ + mùng 1, rằm',daily='Ngày âm hằng ngày + ngày lễ',custom='2. Tùy chỉnh bằng Python',root='Chạy lệnh từ thư mục gốc dự án',setup='Lần đầu dùng? Cài môi trường Python 3.11+',setup_text='Tải repo, mở thư mục gốc chứa main.py rồi tạo môi trường ảo. Kích hoạt môi trường trước khi cài dependencies đã khóa phiên bản.',json='Chỉnh file cấu hình',json_text='Dùng calendar.config.json trong thư mục này. CLI được ưu tiên hơn JSON; có thể đổi language thành en khi cần lịch tiếng Anh.',options='Dùng --year hoặc --start/--end để chọn năm; --lunar-days all/none/1,15 chọn ngày nền; --holiday-types lunar/solar/all/none chọn nhóm lễ; --split tạo tệp từng năm và ZIP; --output-dir đổi thư mục. Các màu #RRGGBB dùng với --calendar-color, --holiday-color, --lunar-day-color và --ordinary-color.',auto='Tự cập nhật trên fork của bạn',auto_steps=['Fork repo và commit file cấu hình.','Bật Actions và cho phép workflow ghi nội dung repo.','Đặt CUSTOM_CONFIG thành đường dẫn cấu hình bên dưới.','Hoàn tất checklist phát hành rồi đặt PUBLISH_LUNAR_FEEDS thành true. Chạy Update Lunar Calendars; custom_config có thể ghi đè đường dẫn cho lần chạy thủ công.','Lấy tên file được in ra để tạo URL raw main/output của fork. Các lần chạy hằng năm dùng CUSTOM_CONFIG.'],know='Phạm vi và trợ giúp',range='Phạm vi hỗ trợ: {first}–{last}. Mặc định tạo {window} năm liên tiếp, bắt đầu từ năm hiện tại, trong giới hạn này.',rules='Bộ lịch: {engine}; múi giờ tham chiếu: {timezone}. Rằm là ngày 15 truyền thống, không phải thời điểm trăng tròn thiên văn. Không lặp lễ trong tháng nhuận.',faq='Nếu link chưa mở được, kiểm tra file đã có trên main của đúng repo. Chu kỳ làm mới do ứng dụng quyết định. Tùy chọn không hỗ trợ sẽ báo lỗi; màu tùy ứng dụng.',status='Vẫn cần rà soát bởi người bản ngữ và thử đăng ký thực tế trên Google/Apple/Outlook trước khi phát hành chính thức.',legacy='Feed Việt Nam đầy đủ và tối giản cũ giữ tên file và định dạng UID. Chạy main.py không có --country giữ chế độ cũ; --minimal không dùng cùng --content.',read='Tài liệu kỹ thuật dùng chung',extra='Ngôn ngữ hiển thị khác',source='Lịch nguồn',variant=''),
'zh-Hans': dict(all='全部地区',intro='复制下方链接，粘贴到日历应用中订阅。',subscribe='1. 通过链接订阅',festival='仅农历节日',paste='粘贴到 Google Calendar、Apple Calendar 或 Outlook 的“通过 URL 订阅”栏并保存。下载后导入 ICS 不会自动更新。',available='新链接在文件发布到 main 分支后可用。',more='其他日历：初一、十五／每日农历',observances='节日＋初一、十五',daily='每日农历＋节日',custom='2. 使用 Python 自定义',root='请在项目根目录运行命令',setup='首次使用？设置 Python 3.11+ 环境',setup_text='下载仓库，打开包含 main.py 的根目录并创建虚拟环境。激活环境后安装已锁定的依赖。',json='修改配置文件',json_text='使用本目录的 calendar.config.json。命令行参数优先于 JSON；需要英文时可将 language 改为 en。',options='--year 或 --start/--end 选择年份；--lunar-days all/none/1,15 选择日期；--holiday-types lunar/solar/all/none 选择类别；--split 生成分年文件与 ZIP；--output-dir 指定目录。四个 --*-color 选项接受 #RRGGBB。',auto='在自己的 fork 中自动更新',auto_steps=['Fork 仓库并提交配置。','启用 Actions 并允许工作流写入仓库。','将 CUSTOM_CONFIG 设为下方配置路径。','完成发布清单后将 PUBLISH_LUNAR_FEEDS 设为 true，运行 Update Lunar Calendars；手动 custom_config 可覆盖本次路径。','用输出文件名创建自己 fork 的 raw main/output 链接。每年任务使用 CUSTOM_CONFIG。'],know='范围与帮助',range='支持 {first}–{last} 年。默认从当年开始连续覆盖 {window} 年，不超出支持范围。',rules='历法：{engine}；参考时区：{timezone}。农历十五并非天文满月时刻；闰月不重复节日。',faq='链接不可用时确认文件位于正确仓库的 main 分支。刷新间隔由应用决定。不支持的选项会报错；颜色支持因应用而异。',status='正式发布前，仍需母语审校及 Google/Apple/Outlook 实际订阅测试。',legacy='',read='共享技术文档',extra='其他显示语言',source='来源历法',variant=''),
'zh-Hant': dict(all='全部地區',intro='複製下方連結，貼到日曆應用程式訂閱。',subscribe='1. 透過連結訂閱',festival='僅農曆節日',paste='貼到 Google Calendar、Apple Calendar 或 Outlook 的「透過 URL 訂閱」欄並儲存。下載後匯入 ICS 不會自動更新。',available='新連結在檔案發布到 main 分支後可用。',more='其他日曆：初一、十五／每日農曆',observances='節日＋初一、十五',daily='每日農曆＋節日',custom='2. 使用 Python 自訂',root='請在專案根目錄執行指令',setup='首次使用？設定 Python 3.11+ 環境',setup_text='下載儲存庫，開啟包含 main.py 的根目錄並建立虛擬環境。啟用環境後安裝已鎖定的相依套件。',json='修改設定檔',json_text='使用本目錄的 calendar.config.json。指令列參數優先於 JSON；需要英文時可將 language 改為 en。',options='--year 或 --start/--end 選年份；--lunar-days all/none/1,15 選日期；--holiday-types lunar/solar/all/none 選類別；--split 產生分年檔及 ZIP；--output-dir 指定目錄。四個 --*-color 選項接受 #RRGGBB。',auto='在自己的 fork 自動更新',auto_steps=['Fork 儲存庫並提交設定。','啟用 Actions 並允許工作流程寫入儲存庫。','將 CUSTOM_CONFIG 設為下方設定路徑。','完成發布清單後，將 PUBLISH_LUNAR_FEEDS 設為 true，執行 Update Lunar Calendars；手動 custom_config 可覆寫該次路徑。','用輸出的檔名建立自己 fork 的 raw main/output 連結。每年工作使用 CUSTOM_CONFIG。'],know='範圍與協助',range='支援 {first}–{last} 年。預設從當年開始連續涵蓋 {window} 年，不超出支援範圍。',rules='曆法：{engine}；參考時區：{timezone}。農曆十五並非天文滿月時刻；閏月不重複節日。',faq='連結無法使用時，確認檔案位於正確儲存庫的 main 分支。更新頻率由應用程式決定。不支援的選項會報錯；色彩依應用程式而異。',status='正式發布前，仍需母語審校及 Google/Apple/Outlook 實際訂閱測試。',legacy='',read='共用技術文件',extra='其他顯示語言',source='來源曆法',variant='此版本採中國曆法與節日清單。繁體中文只改變顯示語言，不會改用臺灣、香港或澳門的節日設定。'),
'ko': dict(all='모든 지역',intro='아래 URL을 복사해 달력 앱에 붙여 넣고 구독하세요.',subscribe='1. URL로 구독',festival='음력 명절만',paste='Google Calendar, Apple Calendar 또는 Outlook의 URL로 구독 입력란에 붙여 넣고 저장하세요. 다운로드한 ICS 파일 가져오기는 자동 갱신되지 않습니다.',available='새 링크는 파일이 main 브랜치에 게시된 뒤 사용할 수 있습니다.',more='다른 달력: 초하루·보름 / 매일의 음력',observances='명절 + 초하루·보름',daily='매일의 음력 + 명절',custom='2. Python으로 맞춤 설정',root='프로젝트 루트 폴더에서 명령을 실행하세요',setup='처음 사용하시나요? Python 3.11+ 환경 설정',setup_text='저장소를 다운로드하고 main.py가 있는 루트 폴더에서 가상 환경을 만드세요. 환경을 활성화한 뒤 고정된 의존성을 설치하세요.',json='설정 파일 수정',json_text='이 폴더의 calendar.config.json을 사용하세요. 명령줄 옵션이 JSON보다 우선하며 영어는 language를 en으로 설정하세요.',options='--year 또는 --start/--end로 연도, --lunar-days all/none/1,15로 날짜, --holiday-types lunar/solar/all/none으로 분류를 선택합니다. --split은 연도별 파일과 ZIP, --output-dir은 출력 폴더입니다. 네 가지 --*-color 옵션은 #RRGGBB 형식입니다.',auto='내 fork에서 자동 갱신',auto_steps=['저장소를 fork하고 설정 파일을 커밋하세요.','Actions를 활성화하고 저장소 쓰기 권한을 주세요.','CUSTOM_CONFIG를 아래 설정 경로로 지정하세요.','출시 점검표 완료 후 PUBLISH_LUNAR_FEEDS를 true로 설정하고 Update Lunar Calendars를 실행하세요. 수동 custom_config는 해당 실행에만 적용됩니다.','출력 파일명으로 본인 fork의 raw main/output URL을 만드세요. 연간 작업은 CUSTOM_CONFIG를 사용합니다.'],know='범위와 도움말',range='지원 범위: {first}–{last}년. 기본 범위는 올해부터 연속 {window}년이며 지원 한도를 넘지 않습니다.',rules='역법: {engine}; 기준 시간대: {timezone}. 음력 보름은 천문학적 보름달 시각과 다릅니다. 윤달에 명절을 반복하지 않습니다.',faq='링크가 없으면 올바른 저장소의 main 브랜치를 확인하세요. 갱신 간격과 색상은 앱에 따라 다릅니다. 지원하지 않는 옵션은 오류로 알립니다.',status='공식 배포 전 원어민 검토와 Google/Apple/Outlook 실제 구독 검사가 필요합니다.',legacy='',read='공유 기술 문서',extra='추가 표시 언어',source='원본 달력',variant=''),
'ms': dict(all='Semua negara',intro='Salin URL di bawah dan tampal dalam aplikasi kalendar untuk melanggan.',subscribe='1. Langgan melalui URL',festival='Perayaan lunar sahaja',paste='Tampal dalam Subscribe from web atau From URL di Google Calendar, Apple Calendar atau Outlook, kemudian simpan. Import fail ICS tidak menerima kemas kini automatik.',available='Pautan baharu tersedia selepas fail diterbitkan ke cabang main.',more='Kalendar lain: hari pertama dan ke-15 / setiap tarikh lunar',observances='Perayaan + hari pertama dan ke-15',daily='Setiap tarikh lunar + perayaan',custom='2. Sesuaikan dengan Python',root='Jalankan arahan dari folder akar projek',setup='Kali pertama? Sediakan Python 3.11+',setup_text='Muat turun repositori dan buka folder akar yang mengandungi main.py. Cipta serta aktifkan persekitaran maya sebelum memasang kebergantungan terkunci.',json='Sunting konfigurasi',json_text='Gunakan calendar.config.json dalam folder ini. Pilihan CLI mengatasi JSON; tukar language kepada en untuk bahasa Inggeris.',options='Gunakan --year atau --start/--end untuk tahun, --lunar-days all/none/1,15 untuk tarikh, --holiday-types lunar/solar/all/none untuk kategori, --split untuk fail tahunan dan ZIP, serta --output-dir untuk folder. Empat pilihan --*-color menerima #RRGGBB.',auto='Kemas kini automatik pada fork anda',auto_steps=['Fork repositori dan komit konfigurasi.','Aktifkan Actions dan kebenaran menulis repositori.','Tetapkan CUSTOM_CONFIG kepada laluan konfigurasi di bawah.','Selepas senarai semak keluaran selesai, tetapkan PUBLISH_LUNAR_FEEDS kepada true dan jalankan Update Lunar Calendars. Input manual custom_config mengatasi laluan untuk larian itu sahaja.','Gunakan nama fail output pada URL raw main/output fork anda. Jadual tahunan menggunakan CUSTOM_CONFIG.'],know='Liputan dan bantuan',range='Julat sokongan: {first}–{last}. Lalai meliputi {window} tahun berturut-turut bermula tahun semasa dalam had ini.',rules='Kalendar: {engine}; zon waktu rujukan: {timezone}. Hari ke-15 lunar bukan waktu bulan purnama astronomi yang tepat. Perayaan tidak diulang pada bulan lompat.',faq='Jika URL tiada, semak cabang main repositori yang betul. Sela muat semula dan warna bergantung pada aplikasi. Pilihan yang tidak disokong menghasilkan ralat.',status='Semakan penutur asli dan ujian langganan sebenar Google/Apple/Outlook masih diperlukan sebelum penerbitan rasmi.',legacy='',read='Dokumentasi teknikal bersama',extra='Bahasa paparan tambahan',source='Kalendar sumber',variant=''),
}


NOTES = {
'en': ('The rolling subscription retains the current year and next year. Older years leave the feed when it rolls forward. Keep historical snapshots with --split --output-dir exports; output/ is managed and dated exports there are retired by the next standard batch build.', 'Scheduled generation is annual, January 1 at 00:00 UTC; code/data changes and manual runs can rebuild immediately. Public GitHub repositories can have schedules disabled after 60 inactive days. Keep the workflow enabled and monitored, or use an external scheduler that enables the workflow when needed and calls workflow_dispatch.'),
'vi': ('Feed đăng ký chỉ giữ năm hiện tại và năm kế tiếp. Năm cũ sẽ rời feed khi chuyển phạm vi. Muốn lưu lịch cũ, dùng --split --output-dir exports; output/ do chương trình quản lý, các bản xuất có năm ở đó sẽ được dọn khi tạo bộ feed tiêu chuẩn.', 'Lịch chạy hằng năm vào ngày 1/1, dự kiến 07:00 giờ Việt Nam; khi sửa code/dữ liệu hoặc chạy thủ công có thể tạo lại ngay. GitHub có thể tắt lịch chạy của repo công khai sau 60 ngày không hoạt động. Cần duy trì, theo dõi workflow hoặc dùng lịch ngoài để bật lại workflow khi cần rồi gọi workflow_dispatch.'),
'zh-Hans': ('滚动订阅仅保留当年和下一年；更新年份后，旧年会从订阅中移除。用 --split --output-dir exports 保存历史快照；output/ 由程序管理，其中带年份的导出会在下次标准构建时清理。', '计划每年1月1日00:00 UTC生成；修改代码或数据、手动运行均可立即重建。公开GitHub仓库连续60天无活动可能停用计划任务，请维护和监控工作流，或由外部调度器在需要时启用工作流，再调用 workflow_dispatch。'),
'zh-Hant': ('滾動訂閱僅保留當年和下一年；更新年份後，舊年會從訂閱移除。以 --split --output-dir exports 儲存歷史快照；output/ 由程式管理，其中帶年份的匯出會在下次標準建置時清理。', '預定每年1月1日00:00 UTC產生；修改程式或資料、手動執行皆可立即重建。公開GitHub儲存庫連續60天無活動可能停用排程，請維護及監控工作流程，或由外部排程器在需要時啟用工作流程，再呼叫 workflow_dispatch。'),
'ko': ('구독에는 올해와 내년만 유지하며 범위 갱신 시 이전 연도는 제거됩니다. --split --output-dir exports로 과거 스냅샷을 보관하세요. output/의 연도별 내보내기는 다음 표준 빌드에서 정리됩니다.', '매년 1월1일 00:00 UTC에 생성하도록 예약되며 코드·데이터 변경이나 수동 실행으로 즉시 재생성할 수 있습니다. 공개 GitHub 저장소가 60일간 비활성 상태이면 예약이 해제될 수 있습니다. 워크플로를 유지·모니터링하거나 외부 스케줄러에서 필요 시 워크플로를 활성화한 후 workflow_dispatch를 호출하세요.'),
'ms': ('Langganan hanya menyimpan tahun semasa dan tahun berikutnya; tahun lama dikeluarkan apabila julat bergerak. Simpan sejarah dengan --split --output-dir exports. Fail bertarikh dalam output/ diurus dan dibersihkan oleh binaan standard berikutnya.', 'Penjanaan dijadualkan setiap 1 Januari 00:00 UTC; perubahan kod/data atau larian manual boleh menjana semula serta-merta. Jadual repositori GitHub awam boleh dilumpuhkan selepas 60 hari tidak aktif. Selenggara dan pantau aliran kerja atau gunakan penjadual luar untuk mengaktifkan aliran kerja apabila perlu dan memanggil workflow_dispatch.'),
}

@dataclass(frozen=True)
class Guide:
    folder: str
    source: str
    native: str
    residence: str | None = None

    def settings(self, language):
        return dict(country=self.residence or self.source, tradition=PROFILES[self.source].tradition,
                    language=language, content='festivals')


GUIDES = (
    Guide('vietnam','VN','vi'), Guide('china','CN','zh-Hans'),
    Guide('taiwan','TW','zh-Hant'), Guide('hong-kong','HK','zh-Hant'),
    Guide('macao','MO','zh-Hant'), Guide('south-korea','KR','ko'),
    Guide('singapore','SG','zh-Hans'), Guide('malaysia','MY','ms'),
    Guide('united-states/vietnamese','VN','vi','US'),
    Guide('united-states/chinese','CN','zh-Hans','US'),
    Guide('united-states/chinese-traditional','CN','zh-Hant','US'),
    Guide('united-states/korean','KR','ko','US'),
)


def relative(target, parent):
    return os.path.relpath(target, parent).replace('\\','/')


def feed(guide, language, content):
    options=CalendarOptions.from_mapping({**guide.settings(language),'content':content})
    return PUBLIC_FEED_BASE_URL+output_prefix(options)+'_latest.ics'


def code_url(guide, language, content):
    return ['```text',feed(guide,language,content),'```','']


def guide_text(guide, language):
    t=TEXT[language]
    folder=ROOT/guide.folder
    profile=PROFILES[guide.source]
    native=f'README.{guide.native}.md'
    home=relative(ROOT/'README.md',folder)
    link=lambda target: relative(ROOT/target,folder)
    title=LOCALES[language]['country_names'][guide.source]+' — '+LOCALES[language]['daily']
    if guide.residence:
        title=LOCALES[language]['country_names'][guide.residence]+' — '+title
        if language=='en' and guide.native=='zh-Hant': title+=' (Traditional Chinese edition)'
    lines=[f'[English](README.md) · [{LANGUAGE_NAMES[guide.native]}]({native}) · [{t["all"]}]({home})','',f'# 🌙 {title}','',t['intro'],'',f'## {t["subscribe"]}','',t['festival'],'',*code_url(guide,language,'festivals'),t['paste'],'',f'> {t["available"]}','']
    if guide.residence:
        lines += [LOCALES[language]['residence_note'],'']
        if guide.source=='CN' and guide.native=='zh-Hant' and t['variant']:
            lines += [t['variant'],'']
    elif guide.source in ('SG','MY'):
        lines += [LOCALES[language]['notice'],'']
    lines += ['<details>',f'<summary>{t["more"]}</summary>','']
    for content in ('observances','daily'):
        lines += [f'**{t[content]}**','',*code_url(guide,language,content)]
    lines += ['</details>','']
    # Malaysia publishes an extra Chinese locale; keep its URLs discoverable
    # without introducing a third README language in the country folder.
    if guide.source=='MY' and language=='en':
        lines += ['<details>',f'<summary>{t["extra"]}: 简体中文</summary>','']
        for content in ('festivals','observances','daily'):
            lines += [f'**{content}**','',*code_url(guide,'zh-Hans',content)]
        lines += ['</details>','']
    catalog_labels = {
        'en': ('Included lunar festivals', 'Lunar date (day/month)', 'Festival', 'Last day of lunar year'),
        'vi': ('Các ngày lễ âm lịch có trong lịch', 'Ngày/tháng âm', 'Ngày lễ', 'Ngày cuối năm âm lịch'),
        'zh-Hans': ('包含的农历节日', '农历日/月', '节日', '农历年最后一天'),
        'zh-Hant': ('包含的農曆節日', '農曆日/月', '節日', '農曆年最後一天'),
        'ko': ('포함된 음력 명절', '음력 일/월', '명절', '음력 한 해의 마지막 날'),
        'ms': ('Perayaan lunar yang disertakan', 'Tarikh lunar (hari/bulan)', 'Perayaan', 'Hari terakhir tahun lunar'),
    }
    heading, date_label, event_label, eve_label = catalog_labels[language]
    source_label = {'en':'Sources and festival rules','vi':'Nguồn và quy tắc ngày lễ','zh-Hans':'来源与节日规则','zh-Hant':'來源與節日規則','ko':'출처 및 명절 규칙','ms':'Sumber dan peraturan perayaan'}[language]
    lines += ['<details>', f'<summary>{heading}</summary>', '',
              f'| {date_label} | {event_label} |', '| --- | --- |']
    for month, day, identity in sorted(RULES[guide.source]):
        lines.append(f'| {day}/{month} | {festival_title(guide.source,language,identity)} |')
    lines += [f'| {eve_label} | {festival_title(guide.source,language,"new_year_eve")} |', '',
              f'[{source_label}]({link("docs/FESTIVALS.md")})', '', '</details>', '']
    lines += [f'## {t["custom"]}','',f'{t["root"]}: [lunar-calender]({home}).','','<details>',f'<summary>{t["setup"]}</summary>','',t['setup_text'],'','```powershell','python -m venv .venv','```','','Windows PowerShell:','','```powershell','.venv\\Scripts\\Activate.ps1','python -m pip install --require-hashes -r requirements.txt','```','','macOS / Linux:','','```bash','source .venv/bin/activate','python -m pip install --require-hashes -r requirements.txt','```','','</details>','']
    stable_notes={'en': 'Set feed_name to a stable name such as family in your JSON before subscribing. The URL stays custom_family_latest.ics when settings change; keep this name unique.', 'vi': 'Thêm "feed_name": "family" vào JSON trước khi đăng ký. URL custom_family_latest.ics giữ nguyên khi đổi tùy chỉnh; mỗi lịch dùng một tên riêng.', 'zh-Hans': '订阅前在 JSON 中设置 "feed_name": "family"。修改设置后 URL custom_family_latest.ics 保持不变；每个日历使用独立名称。', 'zh-Hant': '訂閱前在 JSON 中設定 "feed_name": "family"。修改設定後 URL custom_family_latest.ics 維持不變；每個日曆使用獨立名稱。', 'ko': '구독 전에 JSON에 "feed_name": "family"를 설정하세요. 설정을 바꿔도 custom_family_latest.ics URL은 유지됩니다. 달력마다 고유한 이름을 사용하세요.', 'ms': 'Tetapkan "feed_name": "family" dalam JSON sebelum melanggan. URL custom_family_latest.ics kekal apabila tetapan berubah; gunakan nama unik bagi setiap kalendar.'}
    path=f'{guide.folder}/calendar.config.json'
    lines += ['```powershell',f'python main.py --config {path} --language {language}','```','','<details>',f'<summary>{t["json"]}</summary>','',t['json_text'],'',stable_notes[language],'','```json',json.dumps(guide.settings(language),ensure_ascii=False,indent=2),'```','',t['options'],'','```powershell',f'python main.py --config {path} --language {language} --year 2027 --split --output-dir exports',f'python main.py --config {path} --language {language} --lunar-days 1,15', 'python main.py --countries VN,CN,KR --language en','```','',f'[calendar.config.json](calendar.config.json)','','</details>','','<details>',f'<summary>{t["auto"]}</summary>','']
    lines += [f'{i}. {step}' for i,step in enumerate(t['auto_steps'],1)]
    lines += ['',NOTES[language][1],'','```text',path,'```','','</details>','',f'## {t["know"]}','',LOCALES[language]['notice'],'',NOTES[language][0],'',t['range'].format(first=profile.first_year,last=profile.last_year,window=DEFAULT_YEARS_AHEAD+1),'',t['rules'].format(engine=profile.tradition,timezone=profile.timezone),'',t['status'],'','<details>','<summary>FAQ</summary>','',t['faq']]
    if guide.source=='VN' and not guide.residence and t['legacy']: lines += ['',t['legacy']]
    lines += ['','</details>','',f'**{t["read"]}**'+(' · English' if language!='en' else ''),'',f'[Feeds]({link("docs/FEEDS.md")}) · [Development]({link("docs/DEVELOPMENT.md")}) · [Automation]({link("docs/AUTOMATION.md")}) · [Release]({link("docs/RELEASE.md")}) · [Sources]({link("tests/fixtures/README.md")}) · [index.json]({link("output/index.json")})','',f'[cmduyeen](https://github.com/cmduyeen) · [MIT]({link("LICENSE")})','']
    return '\n'.join(lines)


def generate():
    for guide in GUIDES:
        folder=ROOT/guide.folder
        folder.mkdir(parents=True,exist_ok=True)
        (folder/'README.md').write_text(guide_text(guide,'en'),encoding='utf-8')
        (folder/f'README.{guide.native}.md').write_text(guide_text(guide,guide.native),encoding='utf-8')
        (folder/'calendar.config.json').write_text(json.dumps(guide.settings(guide.native),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    root=['# 🌙 Global Lunar Calendars','','Choose a region, then open a country guide. Each guide has an English version, a native-language version and a copyable calendar URL.','','## 1. Choose your calendar','']
    for region,codes in [('East Asia',('CN','TW','HK','MO','KR')),('Southeast Asia',('VN','SG','MY'))]:
        root += ['<details>',f'<summary><strong>{region}</strong></summary>','']
        for code in codes:
            guide=next(g for g in GUIDES if g.source==code and not g.residence)
            root += [f'- **{PROFILES[code].name}** — [English]({guide.folder}/README.md) · [{LANGUAGE_NAMES[guide.native]}]({guide.folder}/README.{guide.native}.md)']
        root += ['','</details>','']
    root += ['<details>','<summary><strong>North America</strong></summary>','','- **[United States](united-states/README.md)** — choose Vietnamese, Chinese or Korean tradition.','','</details>','','## 2. Customize with Python','','One shared generator; no separate country applications. Run from this root folder after installing Python 3.11+ and requirements.txt:','','```powershell','python main.py --config vietnam/calendar.config.json','python main.py --country US --tradition vietnamese --language en','```','','Configurations live next to each country’s two guides. Generated calendars stay in output/ so existing subscription URLs remain stable. Defaults cover the current year and next year; scheduled generation is annual, with immediate rebuilds for fixes. Yearly files and ZIPs are optional via --split --output-dir exports. A local folder rename does not rename the GitHub repository or publish new URLs.','','## Status and development','','New feeds require publication to main before subscription. Native-language review and live calendar-app checks are still pending. Nigeria, Egypt, Brazil and Mexico are roadmap markets, not supported calendar profiles.','','[Development](docs/DEVELOPMENT.md) · [Automation](docs/AUTOMATION.md) · [Feed inventory](output/index.json) · [Release checklist](docs/RELEASE.md) · [MIT](LICENSE)','','[cmduyeen](https://github.com/cmduyeen)','']
    (ROOT/'README.md').write_text('\n'.join(root),encoding='utf-8')
    us=['# United States — community lunar calendars','','English is the main guide language here. Choose the tradition and community language you use. These calendars keep original festival dates; they are not US federal/state holiday schedules.','','## Choose a community','']
    for guide in (g for g in GUIDES if g.residence):
        name={'vi':'Vietnamese','zh-Hans':'Chinese · Simplified','zh-Hant':'Chinese · Traditional','ko':'Korean'}[guide.native]
        child=guide.folder.split('/',1)[1]
        us += [f'- **{name}** — [English]({child}/README.md) · [{LANGUAGE_NAMES[guide.native]}]({child}/README.{guide.native}.md)']
    us += ['','## Custom generation','','```powershell','python main.py --country US --tradition vietnamese --language vi','python main.py --country US --tradition chinese --language zh-Hant','python main.py --country US --tradition korean --language ko','```','','US feeds use English by default. A tradition is required; the source calendars remain distinct. All-day dates do not move to a previous date because of US timezones. Do not subscribe to both the original and US counterpart unless you want overlapping events.','','[All countries](../README.md) · [Sources and release checks](../docs/RELEASE.md)','']
    (ROOT/'united-states'/'README.md').write_text('\n'.join(us),encoding='utf-8')


if __name__=='__main__':
    generate()
